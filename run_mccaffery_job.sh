#!/bin/bash

let numjobs=$1
echo "Spawning ${numjobs} jobs"

SINGULARITY_IMG=/home/taritree/larbys/images/dllee_ssnet/singularity-dllee-ssnet.img
WORKDIR=/home/taritree/dllee_integration/ssnet-tuftscluster-scripts
INPUTLISTS=${WORKDIR}/inputlists
OUTDIR=/home/taritree/larbys/data/mcc8.1/nue_1eNpfiltered/out_week0626/ssnet/
JOBIDLIST=${WORKDIR}/rerunlist.txt

mkdir -p $OUTDIR

rm -f log_mccaffery_job.txt
for (( i=0; i<$numjobs; i++ ))
do
    #SLURM_PROCID=$i ./mccaffe_test.sh &
    echo "launching job=$i" && singularity exec $SINGULARITY_IMG bash -c "export SLURM_PROCID=$i && cd ${WORKDIR} && source run_job.sh ${WORKDIR} ${INPUTLISTS} ${OUTDIR} ${JOBIDLIST}" >> log_mccaffery_job.txt 2>&1 &
done
