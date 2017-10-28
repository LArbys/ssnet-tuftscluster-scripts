import os,sys

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


# COMPARISON SAMPLES
# ------------------

# 1e1p
#LARCV_SOURCE=DATAFOLDER+"/comparison_samples/1e1p/supera_links"
#TAGGER_SOURCE=DATAFOLDER+"/comparison_samples/1e1p/out_week080717/tagger"

#LARCV_SOURCE=DATAFOLDER+"/larbys/data/comparison_samples/inclusive_elec/supera_links"
#TAGGER_SOURCE=DATAFOLDER+"/larbys/data/comparison_samples/inclusive_elec/out_week080717/tagger"

#LARCV_SOURCE =DATAFOLDER+"/comparison_samples/ncpizero/supera_links"
#TAGGER_SOURCE=DATAFOLDER+"/comparison_samples/ncpizero/out_week080717/tagger"

#LARCV_SOURCE =DATAFOLDER+"/comparison_samples/extbnb/supera_wpmtprecut"
#TAGGER_SOURCE=DATAFOLDER+"/comparison_samples/extbnb/out_week082817/tagger"
#LARCV_SOURCE =DATAFOLDER+"/comparison_samples/extbnb_wprecuts/supera"
#TAGGER_SOURCE=DATAFOLDER+"/comparison_samples/extbnb_wprecuts/out_week082817/tagger"
LARCV_SOURCE =DATAFOLDER+"/comparison_samples/extbnb_wprecuts_reprocess/supera_p09"
TAGGER_SOURCE=DATAFOLDER+"/comparison_samples/extbnb_wprecuts_reprocess/out_week10132017/tagger_p09"

#LARCV_SOURCE =DATAFOLDER+"/comparison_samples/corsika/supera_wpmtprecut"
#TAGGER_SOURCE=DATAFOLDER+"/comparison_samples/corsika/out_week082817/tagger"

# 5e19 BNB sample (test). With PMT Precuts.
#LARCV_SOURCE =DATAFOLDER+"/bnbdata_5e19/supera"
#TAGGER_SOURCE=DATAFOLDER+"/bnbdata_5e19/out_week082817/tagger"


# We parse folder contents for larcv and larlite files
# We keep them in a dictionary
job_dict = {} # key=jobid, value=dict{"larlite":[],"larcv":[]}

files = os.listdir(LARCV_SOURCE)
for f in files:
    f = f.strip()
    if ".root" not in f or "larcv" not in f:
        continue
    fpath = LARCV_SOURCE + "/" + f
    fileid = int(f.split(".")[-2].split("_")[-1])
    #print f.strip(),fileid
    if fileid not in job_dict:
        job_dict[fileid] = {"larcv":[],"tagger":[]}
    job_dict[fileid]["larcv"].append(fpath)

files = os.listdir(TAGGER_SOURCE)
for f in files:
    f = f.strip()
    if ".root" not in f or "taggerout_larcv" not in f:
        continue
    fpath = TAGGER_SOURCE + "/" + f
    try:
        fileid = int(f.split(".")[-2].split("_")[-1])
    except:
        print "could not parse ",fpath
        continue
    #print f.strip(),fileid
    if fileid not in job_dict:
        job_dict[fileid] = {"larcv":[],"tagger":[]}
    job_dict[fileid]["tagger"].append(fpath)

fileid_list = job_dict.keys()
fileid_list.sort()

print "Making input files for ",len(fileid_list)," jobs."

jobidlist = open("jobidlist.txt",'w')
os.system("mkdir -p inputlists")
os.system("rm -f inputlists/*")
for jobid,fileid in enumerate(fileid_list):
    if len(job_dict[fileid]["larcv"])==1 and len(job_dict[fileid]["tagger"])==1:
        flarcv = open("inputlists/inputlist_%04d.txt"%(fileid),'w')
        print >> flarcv,job_dict[fileid]["larcv"][0]
        print >> flarcv,job_dict[fileid]["tagger"][0]
        flarcv.close()    
        print >> jobidlist,fileid

jobidlist.close()

