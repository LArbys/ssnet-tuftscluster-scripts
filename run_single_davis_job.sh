#!/bin/bash

let processid=$1
echo "Spawning job for processid=${processid}"

#SINGULARITY_IMG=/home/taritree/containers/singularity-dllee-ssnet/singularity-dllee-ssnet-nvidia375.39_fix.img
WORKDIR=/home/taritree/dllee_selection/ssnet-tuftscluster-scripts
INPUTLISTS=${WORKDIR}/inputlists
JOBIDLIST=${WORKDIR}/rerunlist.txt

#OUTDIR=/home/taritree/larbys/data/mcc8.1/numu_1muNpfiltered/out_week071017/ssnet/
OUTDIR=/home/taritree/larbys/data/comparison_samples/1mu1p/out_week080717/ssnet_mcc8/

mkdir -p $OUTDIR

rm -f log_mccaffery_job.txt
echo "launching job=$i" && export SLURM_PROCID=$processid && export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/usr/local/nvidia && cd ${WORKDIR} && nohup nice -n 10 ./run_gpu_job.sh ${WORKDIR} ${INPUTLISTS} ${OUTDIR} ${JOBIDLIST} >> log_mccaffery_job.txt 2>&1 &
