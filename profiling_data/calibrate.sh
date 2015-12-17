#!/bin/bash -l
#$ -N calibrate                   # Name of job
#$ -l h_vmem=1G                  # Requested Memory
#$ -l h_rt=24:00:00              # Requested CPU time
#$ -pe smp 2                     # number of cores
#$ -cwd                          #
#$ -j y                          # Join stdout & stderr
#$ -m bea                        # Notify on begin, end, abort
#$ -M paul.logston@gmail.com

/home/araldiel/anaconda/envs/conservation/bin/python \
/zenodotus/dat02/elemento_lab_scratch/oelab_scratch_scratch007/araldiel/data_EAXS/Elisa_2012_07_06/calibrate.py

