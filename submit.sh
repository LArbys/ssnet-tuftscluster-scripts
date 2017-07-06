#!/bin/bash
#
#SBATCH --job-name=ssnet
#SBATCH --output=ssnet_log.txt
#
#SBATCH --ntasks=20
#SBATCH --time=8:00:00
#SBATCH --mem-per-cpu=4000

module load singularity
srun singularity exec /cluster/kappa/90-days-archive/wongjiradlab/larbys/images/singularity-dllee-ubuntu/singularity-dllee-ssnet.img bash -c "cd /cluster/home/twongj01/grid_jobs/ssnet-tuftscluster-scripts && source run_job.sh /cluster/home/twongj01/grid_jobs/ssnet-tuftscluster-scripts /cluster/home/twongj01/grid_jobs/ssnet-tuftscluster-scripts/inputlists /cluster/kappa/90-days-archive/wongjiradlab/larbys/data/mcc8.1/numu_1muNpfiltered/out_week0626/ssnet /cluster/home/twongj01/grid_jobs/ssnet-tuftscluster-scripts/rerunlist.txt"
