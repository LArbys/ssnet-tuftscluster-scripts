import os,sys,time

import ROOT as rt
rt.gSystem.Load("libGeo2D_Core.so")
from larcv import larcv
import caffe
from caffe.image2d_data_layer import Image2DLayer as il

# Check GPU availability before heavy lib loading
from choose_gpu import pick_gpu
GPUMEM = 10000
GPUID = pick_gpu(mem_min=GPUMEM,caffe_gpuid=True)
if GPUID < 0:
    sys.stderr.write('No GPU available with memory > %d\n' % GPUMEM)
    sys.stderr.flush()
    sys.exit(1)

GPUID=0
#caffe.set_device(GPUID)
caffe.set_mode_gpu()


import numpy as np
#import matplotlib 
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
os.environ['GLOG_minloglevel'] = '2' # set message level to warning 

print "MODULES LOADED"


PROTO  = None
MODEL  = None
OUTCFG = 'pyana_out.cfg'
MASK_ADC = True
MASK_THRESH = 10.
SKIP_CH = [0]

MODELMAP={'plane0' : 'pretrain_segmentation_tskeyspweights_plane0.caffemodel.h5',
          'plane1' : 'pretrain_segmentation_tskeyspweights_plane1.caffemodel.h5',
          'plane2' : 'pretrain_segmentation_tskeyspweights_plane2.caffemodel.h5'}
PLANEID=''
MODEL=''
OUTFILESTEM='larcv_fcn'

flist=rt.std.vector('string')()
PROTO = "pyana_mcc8.prototxt"
PLANEID= "plane0"
MODEL=MODELMAP[PLANEID]
OUTFILESTEM="slurm_testjob/ssnetout"
os.system("mkdir -p slurm_testjob")

INCFG  = 'pyana_in_%s.cfg' % PLANEID
print "Using input config:",INCFG
debug = 'debug' in sys.argv
print "Out file stem: ",OUTFILESTEM
print "GPU MODE: using GPU #",GPUID

flist.push_back( "/home/taritree/larbys/data/comparison_samples/1mu1p/supera_links/larcv_mc_005003603.root" )
flist.push_back( "/home/taritree/larbys/data/comparison_samples/1mu1p/out_week080717/tagger/taggerout_larcv_5003603.root" )

out_proc = larcv.ProcessDriver('OutputProcessDriver')
out_proc.configure(OUTCFG)
py_image_maker = out_proc.process_ptr(out_proc.process_id("PyImageStitcher"))
py_image_maker.set_producer_name('uburn_%s' % PLANEID)
out_proc.override_output_file('%s_%s.root'%(OUTFILESTEM,PLANEID) )
out_proc.initialize()

in_proc = larcv.ProcessDriver('InputProcessDriver')
in_proc.configure(INCFG)
in_proc.override_input_file(flist)

# put copy of input file in same folder as output
inputcopy_path = os.path.dirname( '%s_%s.root'%(OUTFILESTEM,PLANEID) ) + "/ssnet_input.root"
in_proc.override_output_file(inputcopy_path)
in_proc.initialize()

cropper = in_proc.process_ptr(in_proc.process_id("MultiROICropper"))
il._rows = cropper.target_rows()
il._cols = cropper.target_cols()

print "Loading Net"
print "  Proto: ",PROTO
print "  Model: ",MODEL
print "  Mode: ",caffe.TEST

#Net('pyana_mcc8.prototxt', 1, weights='pretrain_segmentation_tskeyspweights_plane0.caffemodel.h5')

#net = caffe.Net( PROTO, MODEL, caffe.TEST)
net = caffe.Net( PROTO, 1, weights=MODEL )

num_events = in_proc.io().get_n_entries()

print
print 'Total number of events:',num_events
print

raw_input()

event_counter = 0
stop_counter  = None

num_event_with_roi = 0.
num_roi = 0.

while event_counter < num_events:
    in_proc.process_entry(event_counter,True)

    img_v = cropper.get_cropped_image()
    sys.stdout.write('Processing entry %d/%d w/ %d ROIs        \r' % (event_counter,num_events,img_v.size()))
    sys.stdout.flush()
    
    num_roi += img_v.size()
    if img_v.size() > 0: num_event_with_roi+=1
    else: 
        # --------------------------------------------------------------------------------------
        # block in container processing to handle empty images
        in_proc.io().read_entry(event_counter,True)
        event_croi = in_proc.io().get_data( larcv.kProductROI, "croi" )
        (run,subrun,event) = (event_croi.run(), event_croi.subrun(), event_croi.event())
        print 'run',run,'subrun',subrun,'event',event," num rois=",event_croi.ROIArray().size()
        py_image_maker.set_id(run, subrun, event)
        out_proc.process_entry()
        in_proc.io().save_entry()
        # ----------------------------------------------------------------------------------------
        event_counter += 1
        continue

    for roi_idx in xrange(img_v.size()):

        il._image2d = img_v[roi_idx]
        print "Set image. now run forward."
        raw_input()
        net.forward()

        adcimg  = net.blobs["data"].data
        softmax = net.blobs["softmax"].data

        if debug:
            adcpng = plt.imshow(adcimg[0][0])
            adcpng.write_png('entry%04d_%04d.png' % (event_counter,roi_idx))

        img_array = softmax[0]
        out_ch = 0
        for ch in xrange(len(img_array)):
            if ch in SKIP_CH: continue

            img = img_array[ch]
            if MASK_ADC:
                img *= (adcimg[0][0] > MASK_THRESH)

            #py_image_maker.append_ndarray_meta(img.transpose(),img_v[roi_idx].meta(),out_ch)
            py_image_maker.append_ndarray_meta(img,img_v[roi_idx].meta(),out_ch)
            out_ch += 1
            
            if debug:
                png=plt.imshow(img)
                png.write_png('entry%06d_ch%02d.png' % ((ibatch * BATCH_CTR),ch))

    event_id = in_proc.io().last_event_id()
    #event_id = in_proc.io().event_id()
    (run,subrun,event) = (event_id.run(), event_id.subrun(), event_id.event())
    print 'run',run,'subrun',subrun,'event',event," num rois=",img_v.size()

    py_image_maker.set_id(run, subrun, event)
    out_proc.process_entry()
    event_counter += 1

    if stop_counter and event_counter >= stop_counter:
        break

frac_event_with_roi = (int(float(num_event_with_roi)/float(event_counter)*10000.))/100.
average_num_roi_total = num_roi / float(event_counter)
average_num_roi = num_roi / float(num_event_with_roi)

print
print '# events processed:',event_counter
print '# event w/ ROI:    ',num_event_with_roi,'(',frac_event_with_roi,'% )'
print '# ROI processed:   ',num_roi,'(',average_num_roi,'ROI per event, or total average',average_num_roi_total,')'
print

out_proc.finalize()
in_proc.finalize()
sys.exit(0)
