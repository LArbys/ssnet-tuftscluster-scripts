import os,sys

# SPECIFY FOLDER WHERE INPUT DATA LIVES
#LARCV_SOURCE="/cluster/kappa/90-days-archive/wongjiradlab/larbys/data/mcc8/calmod_mcc8_bnb_nu_cosmic_v06_26_01_run01.09000_run01.09399_v01_p00_out"
#TAGGER_SOURCE="/cluster/kappa/90-days-archive/wongjiradlab/larbys/data/out/mcc8numu/"

# NUE MCCAFFERY
LARCV_SOURCE="/home/taritree/larbys/data/mcc8.1/nue_1eNpfiltered/supera"
TAGGER_SOURCE="/home/taritree/larbys/data/mcc8.1/nue_1eNpfiltered/out_week0626/tagger"

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
    fileid = int(f.split(".")[-2].split("_")[-1])
    #print f.strip(),fileid
    if fileid not in job_dict:
        job_dict[fileid] = {"larcv":[],"tagger":[]}
    job_dict[fileid]["tagger"].append(fpath)

fileid_list = job_dict.keys()
fileid_list.sort()

jobidlist = open("jobidlist.txt",'w')
os.system("mkdir -p inputlists")
for jobid,fileid in enumerate(fileid_list):
    if len(job_dict[fileid]["larcv"])==1 and len(job_dict[fileid]["tagger"])==1:
        flarcv = open("inputlists/inputlist_%03d.txt"%(fileid),'w')
        print >> flarcv,job_dict[fileid]["larcv"][0]
        print >> flarcv,job_dict[fileid]["tagger"][0]
        flarcv.close()    
        print >> jobidlist,fileid

jobidlist.close()

