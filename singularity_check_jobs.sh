#!/bin/bash

CONTAINER=/cluster/kappa/90-days-archive/wongjiradlab/larbys/images/dllee_unified/singularity-dllee-unified-071017.img
WORKDIR=/cluster/kappa/90-days-archive/wongjiradlab/grid_jobs/ssnet-tuftscluster-scripts


#CONTAINER=/home/taritree/containers/singularity-dllee-ssnet/singularity-dllee-ssnet-nvidia375.39.img
#WORKDIR=/home/taritree/dllee_selection/ssnet-tuftscluster-scripts

module load singularity

singularity exec -B /media:/media ${CONTAINER} bash -c "source /usr/local/bin/thisroot.sh && cd ${WORKDIR} && python check_jobs.py"

