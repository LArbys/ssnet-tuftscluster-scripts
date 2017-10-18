#!/bin/bash

let processid=$1
let gpuid=$2
echo "Spawning job for processid=${processid}"

WORKDIR=/home/taritree/dllee_selection/ssnet-tuftscluster-scripts
INPUTLISTS=${WORKDIR}/inputlists
JOBIDLIST=${WORKDIR}/rerunlist.txt
DATAFOLDER=/media/data/larbys/data

#OUTDIR=${DATAFOLDER}/comparison_samples/ncpizero/out_week080717/ssnet_mcc8/
OUTDIR=${DATAFOLDER}/comparison_samples/extbnb_wprecuts/out_week082817/ssnet_mcc8/
#OUTDIR=${DATAFOLDER}/comparison_samples/1e1p/out_week080717/ssnet_small_mcc8/
#OUTDIR=${DATAFOLDER}/bnbdata_5e19/out_week082817/ssnet_mcc8/
#OUTDIR=${DATAFOLDER}/bnbdata_5e19/out_week082817/ssnet_small_mcc8/

mkdir -p $OUTDIR

rm -f log_mccaffery_job.txt
echo "launching job=$i" && export SLURM_PROCID=$processid && export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/usr/local/nvidia && cd ${WORKDIR} && nohup nice -n 10 ./run_gpu_job.sh ${WORKDIR} ${INPUTLISTS} ${OUTDIR} ${JOBIDLIST} ${gpuid} >> log_mccaffery_job.txt 2>&1 &
