#!/bin/bash
#
#SBATCH --job-name=ssnet
#SBATCH --output=ssnet_log.txt
#
#SBATCH --ntasks=100
#SBATCH --time=8:00:00
#SBATCH --mem-per-cpu=4000

CONTAINER=/cluster/kappa/90-days-archive/wongjiradlab/larbys/images/singularity-dllee-ubuntu/singularity-dllee-ssnet.img
WORKDIR=/cluster/kappa/90-days-archive/wongjiradlab/grid_jobs/ssnet-tuftscluster-scripts
INPUTLISTDIR=${WORKDIR}/inputlists
JOBLIST=${WORKDIR}/rerunlist.txt

#OUTDIR=/cluster/kappa/90-days-archive/wongjiradlab/larbys/data/mcc8.1/numu_1muNpfiltered/out_week071017/ssnet
OUTDIR=/cluster/kappa/90-days-archive/wongjiradlab/larbys/data/mcc8.1/nue_1eNpfiltered/out_week071017/ssnet

module load singularity

srun singularity exec ${CONTAINER} bash -c "cd ${WORKDIR} && source run_job.sh ${WORKDIR} ${INPUTLISTDIR} ${OUTDIR} ${JOBLIST}"