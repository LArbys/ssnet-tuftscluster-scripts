import os,sys,time
from choose_gpu import pick_gpu

# This script is meant to shepard SSNET jobs through the available cards.
# Currently, 3 SSNET jobs can fit on one card

# first get jobid list

frerunlist = open("rerunlist.txt",'r')
lrerunlist = frerunlist.readlines()
jobids = []
for l in lrerunlist:
    jobids.append(int(l.strip()))

print "number of remaining jobs: ",len(jobids)

runningids = []
runningprocs = []

# event loop
# really dumb. we loop every X seconds and check how much memory is available on the gpu. 
# if memory available, we add a job. move id from jobids to runningids
# we need to pick an X where there is enough time for the gpu to load the job. else we cause a disaster.

waitsec = 30

while len(jobids)>0:
    available_gpu = pick_gpu(mem_min=6000,caffe_gpuid=True)
    if available_gpu>=0:
        print "Available GPU (",available_gpu,")"
        jobid = jobids.pop()
        procid = len(jobids)
        os.system( "./run_single_davis_job.sh %d"%(procid) )
        runningids.append(jobid)
        runningprocs.append(procid)
    else:
        print "No space right now"
    print "Now wait %d seconds for job to launch."%(waitsec)
    print "Job IDs left: ",len(jobids)
    time.sleep(waitsec)
    
