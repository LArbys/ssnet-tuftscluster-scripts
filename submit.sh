#!/bin/bash
#
#SBATCH --job-name=ssnet
#SBATCH --output=ssnet_log.txt
#
#SBATCH --ntasks=1
#SBATCH --time=8:00:00
#SBATCH --mem-per-cpu=8000

#CONTAINER=/cluster/kappa/90-days-archive/wongjiradlab/larbys/images/singularity-dllee-ubuntu/singularity-dllee-ssnet.img
#CONTAINER=/cluster/kappa/90-days-archive/wongjiradlab/larbys/images/singularity-dllee-ubuntu/singularity-dllee-ssnet-nvidia375.39-cpuonly.img
CONTAINER=/cluster/kappa/90-days-archive/wongjiradlab/larbys/images/singularity-dllee-ssnet/singularity-dllee-ssnet-nvidia384.66.img
WORKDIR=/cluster/kappa/90-days-archive/wongjiradlab/grid_jobs/ssnet-tuftscluster-scripts
INPUTLISTDIR=${WORKDIR}/inputlists
JOBLIST=${WORKDIR}/rerunlist.txt

OUTDIR=/cluster/kappa/90-days-archive/wongjiradlab/larbys/data/comparison_samples/extbnb_wprecuts_reprocess/out_week10132017/ssnet_p09

module load singularity

singularity exec ${CONTAINER} bash -c "export SLURM_PROCID=1 && cd ${WORKDIR} && source run_job.sh ${WORKDIR} ${INPUTLISTDIR} ${OUTDIR} ${JOBLIST}"
