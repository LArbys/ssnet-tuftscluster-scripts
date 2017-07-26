#!/bin/bash
#
#SBATCH --job-name=ssnet
#SBATCH --output=ssnet_log.txt
#
#SBATCH --ntasks=1
#SBATCH --time=16:00:00
#SBATCH --mem-per-cpu=4000

CONTAINER=/cluster/kappa/90-days-archive/wongjiradlab/larbys/images/singularity-dllee-ubuntu/singularity-dllee-ssnet.img
WORKDIR=/cluster/kappa/90-days-archive/wongjiradlab/grid_jobs/ssnet-tuftscluster-scripts
INPUTLISTDIR=${WORKDIR}/inputlists
JOBLIST=${WORKDIR}/rerunlist.txt

#OUTDIR=/cluster/kappa/90-days-archive/wongjiradlab/larbys/data/mcc8.1/numu_1muNpfiltered/out_week071017/ssnet
OUTDIR=/cluster/kappa/90-days-archive/wongjiradlab/larbys/data/mcc8.1/nue_1eNpfiltered/out_week072517/ssnet_mcc8

module load singularity
srun singularity exec ${CONTAINER} bash -c "cd ${WORKDIR} && source run_job.sh ${WORKDIR} ${INPUTLISTDIR} ${OUTDIR} ${JOBLIST}"

#singularity exec ${CONTAINER} bash -c "export SLURM_PROCID=1 && cd ${WORKDIR} && source run_job.sh ${WORKDIR} ${INPUTLISTDIR} ${OUTDIR} ${JOBLIST}"
