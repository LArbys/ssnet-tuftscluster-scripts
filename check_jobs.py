import os,sys
import ROOT as rt

# Check job id list. Check output folder. Check that tagger output files have entries (and same number of entries)
# based on checks, will produce rerun list

# MCC8.1 nue+cosmic: Maccfrey
#SSNET_FOLDER="/home/taritree/larbys/data/mcc8.1/nue_1eNpfiltered/out_week0626/ssnet"

# MCC8.1 nue only: Tufts
SSNET_FOLDER="/cluster/kappa/90-days-archive/wongjiradlab/larbys/data/mcc8.1/nue_nocosmic_1eNpfiltered/out_week0626/ssnet"

files = os.listdir(SSNET_FOLDER)

file_dict = {}
for f in files:
    f.strip()
    idnum = int(f.split("_")[-1].split(".")[0])
    if idnum not in file_dict:
        file_dict[idnum] = {"larcv":None,"larlite":None}
    if "larcv" in f or "ssnet_out" in f:
        file_dict[idnum]["larcv"] = SSNET_FOLDER+"/"+f
    elif "larlite" in f:
        file_dict[idnum]["larlite"] = SSNET_FOLDER+"/"+f

ids = file_dict.keys()
ids.sort()


rerun_list = []
good_list = []
for fid in ids:
    try:
        rfile_larcv = rt.TFile( file_dict[fid]["larcv"] )

        tree = rfile_larcv.Get("image2d_wire_tree")
        nentries_larcv = tree.GetEntries()

        tree = rfile_larcv.Get("image2d_uburn_plane0_tree")
        nentries_uburn0 = tree.GetEntries()

        tree = rfile_larcv.Get("image2d_uburn_plane1_tree")
        nentries_uburn1 = tree.GetEntries()

        tree = rfile_larcv.Get("image2d_uburn_plane2_tree")
        nentries_uburn2 = tree.GetEntries()
        
        if (nentries_larcv==0 or nentries_uburn0==0 or nentries_uburn1==0 or nentries_uburn2==0
            or nentries_uburn0!=nentries_larcv or nentries_uburn1!=nentries_larcv or nentries_uburn2!=nentries_larcv):
            raise RuntimeError("oops")
        
        good_list.append(fid)
    except:
        print "Not ok: ",fid
        rerun_list.append(fid)
        continue

print "Goodlist: ",len(good_list)
print "Rerunlist: ",len(rerun_list)

# read in jobidlist
fjobid = open("jobidlist.txt",'r')
ljobid = fjobid.readlines()
for l in ljobid:
    jobid = int(l.strip())
    if jobid in good_list or jobid in rerun_list:
        continue
    else:
        rerun_list.append(jobid)
fjobid.close()


frerun = open("rerunlist.txt",'w')
for jobid in rerun_list:
    print >> frerun,jobid
frerun.close()
