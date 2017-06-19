SSNet Grid Jobs for Tufts Cluster using Slurm

## Steps

* make jobs list using make_inputlists.py
* clone ssnet_example to /cluster/home/[username] directory
* copy jobidlist.txt to ssnet_example dir
* copy inputlists folder to ssnet_example dir
* edit pyana_planeX.cfg to use proper producer names (i.e. tree names)
* edit submit.sh: cd [path to ssnet_example folder] [path to inputlists] [path to output dir] [path to job id list]. Example:

      "cd /cluster/home/twongj01/grid_jobs/ssnet && source run_job.sh /cluster/home/twongj01/grid_jobs/ssnet/inputlists /cluster/kappa/90-days-archive/wongjiradlab/larbys/data/out_ssnet/mcc8numu /cluster/home/twongj01/grid_jobs/ssnet/jobidlist.txt"

* make output directory if needed
* edit run_job.sh?
