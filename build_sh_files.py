import subprocess
import sys


PYTHON_EXE = '/home/araldiel/anaconda/envs/conservation/bin/python'
COMMON_DIR = '/zenodotus/dat02/elemento_lab_scratch/oelab_scratch_scratch007/araldiel/data_EAXS/'
MER_CONVERSION_PY_FILE = '/home/araldiel/python-tools/mer_conservation/mer_conservation.py'
SEQUENCE_FILE_PATTERN = COMMON_DIR + 'Elisa_2012_07_06/s_{seq_count}_sequence.txt.gz.noadapt'
COUNT_FILE_PATTERN = COMMON_DIR + 'Elisa_2012_07_06/s_{seq_count}_sequence.txt.gz.noadapt.mercount-{mer_count}mer.2'
SH_FILE_NAME = COMMON_DIR + 'Elisa_2012_07_06/s_{seq_count}_sequence_mercount_{mer_count}mer.sh'

CONSTANTS = {
    'PYTHON_EXE': PYTHON_EXE,
    'MER_CONVERSION_PY_FILE': MER_CONVERSION_PY_FILE,
    'SEQUENCE_FILE_PATTERN': SEQUENCE_FILE_PATTERN,
    'COUNT_FILE_PATTERN': COUNT_FILE_PATTERN,
    'mer_count': sys.argv[1],
    'cpu_count': sys.argv[2],
    'seq_count': '{seq_count}',
}

FILE_TXT = """\
#!/bin/bash -l
#$ -N s_{seq_count}-{mer_count}mer                   # Name of job
#$ -l h_vmem=4G                  # Requested Memory
#$ -l h_rt=24:00:00              # Requested CPU time
#$ -pe openmpi {cpu_count}       # number of cores
#$ -cwd                          #
#$ -j y                          # Join stdout & stderr
#$ -m bea                        # Notify on begin, end, abort
#$ -M paul.logston@gmail.com,elisa.araldi@yale.edu

mpirun -np $NSLOTS \\\n\
{PYTHON_EXE} \\\n\
{MER_CONVERSION_PY_FILE} -p $NSLOTS \\\n\
{SEQUENCE_FILE_PATTERN} \\\n\
{COUNT_FILE_PATTERN} {mer_count}
"""

FILE_TXT = FILE_TXT.format(**CONSTANTS)
file_body_template = FILE_TXT.format(**CONSTANTS)

file_name_template = SH_FILE_NAME.format(**CONSTANTS)

for i in range(1, 13):
    with open(file_name_template.format(seq_count=i), 'w') as fp:
        fp.write(file_body_template.format(seq_count=i))
    cmd = '/opt/sge/bin/lx26-amd64/qsub ' + file_name_template.format(seq_count=i)
    print(cmd)
    print(subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True))

