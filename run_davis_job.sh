#!/bin/bash

let numjobs=$1
echo "Spawning ${numjobs} jobs"

SINGULARITY_IMG=/home/taritree/containers/singularity-dllee-ssnet/singularity-dllee-ssnet-nvidia375.39_fix.img
WORKDIR=/home/taritree/dllee_selection/ssnet-tuftscluster-scripts
INPUTLISTS=${WORKDIR}/inputlists
JOBIDLIST=${WORKDIR}/rerunlist.txt

#OUTDIR=/home/taritree/larbys/data/mcc8.1/numu_1muNpfiltered/out_week071017/ssnet/
#OUTDIR=/home/taritree/larbys/data/comparison_samples/1mu1p/out_week080717/ssnet_mcc8/
OUTDIR=

mkdir -p $OUTDIR

rm -f log_mccaffery_job.txt
for (( i=0; i<$numjobs; i++ ))
do
    #SLURM_PROCID=$i ./mccaffe_test.sh &
    #echo "launching job=$i" && nice -n 10 singularity exec $SINGULARITY_IMG bash -c "export SLURM_PROCID=$i && export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/usr/local/nvidia && cd ${WORKDIR} && source run_gpu_job.sh ${WORKDIR} ${INPUTLISTS} ${OUTDIR} ${JOBIDLIST}" >> log_mccaffery_job.txt 2>&1 &
    echo "launching job=$i" && export SLURM_PROCID=$i && export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/usr/local/nvidia && cd ${WORKDIR} && nohup nice -n 10 ./run_gpu_job.sh ${WORKDIR} ${INPUTLISTS} ${OUTDIR} ${JOBIDLIST} >> log_mccaffery_job.txt 2>&1 &
done
