#!/bin/bash
#
#SBATCH --job-name=ssnet
#SBATCH --output=ssnet_log.txt
#
#SBATCH --ntasks=1
#SBATCH --time=60:00
#SBATCH --mem-per-cpu=4000

module load singularity

srun singularity exec /cluster/kappa/90-days-archive/wongjiradlab/larbys/images/singularity-dllee-ubuntu/singularity-dllee-ssnet.img bash -c "cd /cluster/home/twongj01/grid_jobs/ssnet && source run_job.sh /cluster/home/twongj01/grid_jobs/ssnet /cluster/home/twongj01/grid_jobs/ssnet/inputlists /cluster/kappa/90-days-archive/wongjiradlab/larbys/data/out_ssnet/mcc8numu /cluster/home/twongj01/grid_jobs/ssnet/jobidlist.txt"
