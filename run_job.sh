#!/bin/sh

# REMEMBER, WE ARE IN THE CONTAINER RIGHT NOW
# This means we access the next work drives through some mounted folders
# The submit command also moved us to right local folder

# expect to be in: ~/grid_jobs/ssnet


# Get arguments
jobdir=$1
inputlist_dir=$2
output_dir=$3
jobid_list=$4

# setup the container software
# ----------------------------

# ROOT6
source /usr/local/bin/thisroot.sh

# SSNet Example Software
cd /usr/local/larbys/ssnet_example/sw/
echo $PWD
source ./setup.sh

# go to job dir
# -------------
cd $jobdir

echo "CURRENT DIR: "$PWD

# check that the process number is greater than the number of job ids
let NUM_PROCS=`cat ${jobid_list} | wc -l`
echo "number of processes: $NUM_PROCS"
if [ "$NUM_PROCS" -lt "${SLURM_PROCID}" ]; then
    echo "No Procces ID to run."
    return
fi

# Get job id
let "proc_line=${SLURM_PROCID}+1"
let jobid=`sed -n ${proc_line}p ${jobid_list}`
echo "JOBID ${jobid}"

# make path to input list
inputlist=`printf ${inputlist_dir}/inputlist_%04d.txt ${jobid}`

# get input files
larcv_file=`sed -n 1p ${inputlist}`
tagger_file=`sed -n 2p ${inputlist}`

slurm_folder=`printf slurm_ssnet_job%04d ${jobid}`
mkdir -p ${slurm_folder}

# Make log file
logfile=`printf ${slurm_folder}/log_%04d.txt ${jobid}`

# echo into it
echo "RUNNING SSNET JOB ${jobid}" > $logfile
echo "larcv file: ${larcv_file}" >> $logfile
echo "tagger file: ${tagger_file}" >> $logfile

# temp output file
outfile_temp=`printf ${slurm_folder}/ssnet_out_%04d.root ${jobid}`

echo "temporary output file: ${outfile_temp}" >> $logfile

# define output
outfile_ssnet=`printf ${output_dir}/ssnetout_larcv_%04d.root ${jobid}`
echo "final output location: ${outfile_ssnet}" >> $logfile

# command
#echo "RUNNING: python run_ssnet.py ${outfile_temp} ${larcv_file} ${tagger_file}" >> $logfile
echo "RUNNING: python run_ssnet_mcc8.py ${outfile_temp} ${larcv_file} ${tagger_file}" >> $logfile

# RUN
#python run_ssnet.py ${outfile_temp} ${larcv_file} ${tagger_file} >> $logfile 2>&1
python run_ssnet_mcc8.py ${outfile_temp} ${larcv_file} ${tagger_file} >> $logfile 2>&1
#python run_ssnet_mcc8.py ${outfile_temp} ${larcv_file} ${tagger_file}

# COPY DATA
cp $outfile_temp $outfile_ssnet

# clean up
#cd ../
#rm -r $slurm_folder
