import os,sys
import ROOT as rt

# SPECIFY FOLDER WHERE INPUT DATA LIVES
# ------------------------------------------------------------------------

TUFTS="/cluster/kappa/90-days-archive/wongjiradlab/larbys/data"
MCCAFFREY="/mnt/sdb/larbys/data"
DAVIS="/media/data/larbys/data"

DATAFOLDER="__unset__"
try:
    LOCAL_MACHINE=os.popen("uname -n").readlines()[0].strip()
    if LOCAL_MACHINE not in ["mccaffrey","login001","davis"]:
        raise RuntimeError("unrecognized machine")

    if LOCAL_MACHINE=="mccaffrey":
        DATAFOLDER=MCCAFFREY
    elif LOCAL_MACHINE=="login001":
        DATAFOLDER=TUFTS
    elif LOCAL_MACHINE=="davis":
        DATAFOLDER=DAVIS

except:
    print "Could not get machine name"
    LOCAL_MACHINE=os.popen("uname -n").readlines()[0].strip()
    print LOCAL_MACHINE
    sys.exit(-1)

if DATAFOLDER=="__unset__":
    raise RuntimeError("Didnt set DATAFOLDER properly.")



# Comparison samples
#SSNET_FOLDER=DATAFOLDER+"/comparison_samples/1mu1p/out_week080717/ssnet_mcc8"
#SSNET_FOLDER=DATAFOLDER+"/comparison_samples/1e1p/out_week080717/ssnet_small_mcc8"
#SSNET_FOLDER=DATAFOLDER+"/comparison_samples/ncpizero/out_week080717/ssnet_mcc8"
#SSNET_FOLDER=DATAFOLDER+"/comparison_samples/extbnb/out_week082817/ssnet_mcc8"
#SSNET_FOLDER=DATAFOLDER+"/comparison_samples/extbnb_wprecuts/out_week082817/ssnet_mcc8"
#SSNET_FOLDER=DATAFOLDER+"/comparison_samples/corsika/out_week082817/ssnet_mcc8"
#SSNET_FOLDER=DATAFOLDER+"/bnbdata_5e19/out_week082817/ssnet_small_mcc8"
SSNET_FOLDER=DATAFOLDER+"/comparison_samples/extbnb_wprecuts_reprocess/out_week10132017/ssnet_p09"


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

# Parse current folders
jobfolders = os.listdir(".")
runningids = []
for f in jobfolders:
    if "slurm_ssnet_job" not in f:
        continue
    runid = int(f.split("_")[-1][3:])
    print runid
    runningids.append(runid)
        
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

print "Remaining list: ",len(rerun_list)

for runid in runningids:
    if runid in rerun_list:
        print "Running Job?: ",runid
        rerun_list.remove(runid)
print "Remaining after running jobs removed: ",len(rerun_list)

frerun = open("rerunlist.txt",'w')
for jobid in rerun_list:
    print >> frerun,jobid
frerun.close()
