import argparse
from itertools import product
import multiprocessing
import sys


def get_conservation(tup):
    p = multiprocessing.current_process()
    lines, permutation = tup 
    counter = 0
    len_permutation = len(permutation)
    for line in lines:
        for i in xrange(len(line) - len_permutation + 1):
            if line[i:i + len_permutation] == permutation:
                counter += 1
    sys.stdout.write('{},{},{}\n'.format(p.pid, permutation, counter)) 
    sys.stdout.flush()


def start_pool(lines, permutations, cpu_count):
    sys.stdout.write('# Gathering args... ')
    sys.stdout.flush()   
    args = ((lines, per) for per in permutations)
 
    sys.stdout.write('throwing to pool...\n')
    sys.stdout.write('{},{},{}\n'.format('pid', 'permutation', 'count')) 
    sys.stdout.flush()   
    pool = multiprocessing.Pool(processes=cpu_count)
    pool.map(get_conservation, args)
  
 
def get_sequence_lines(file_name):
    sys.stdout.write('# Reading sequence file "{}" ... '.format(file_name))
    sys.stdout.flush()
    with open(file_name) as fp:
        file_lines = fp.read()
    sys.stdout.write('Done.\n')
    sys.stdout.flush()

    sys.stdout.write('# Gathering sequences ... ')
    sys.stdout.flush()   
    lines = [] 
    for i, line in enumerate(file_lines.split('\n')):
        offset_i = i - 1
        if not offset_i % 4:
            lines.append(line)
    sys.stdout.write('{} sequences to search.\n'.format(len(lines)))
    sys.stdout.flush()
    return lines


def get_mer_permutations(mer_count):
    sys.stdout.write('# Getting perumtations ... ')
    sys.stdout.flush()  
    permutations = [''.join(p) for p in product('ATGC', repeat=mer_count)]
    sys.stdout.write('{} perumtations.\n'.format(len(permutations)))
    sys.stdout.flush()  
    return permutations
          
 
def main():
    parser = argparse.ArgumentParser(description='Count occurrances of n-mer in data')
    parser.add_argument('file',
                        help='Sequence file to search for n-mers')
    parser.add_argument('mer_count',
                        type=int, 
                        help='Length of n-mer (in nucleotides)')
    parser.add_argument('-p', '--process-count', 
                        dest='process_count',
                        type=int,
                        default=1,
                        help='Number of processes to start')
    args = parser.parse_args()

    sys.stdout.write('# Running {}-mer search with {} processes.\n'
                     ''.format(args.mer_count, 
                               args.process_count))
    sys.stdout.flush() 

    permutations = get_mer_permutations(args.mer_count) 
  
    lines = get_sequence_lines(args.file)
    
    start_pool(lines, permutations, args.process_count)

    sys.stdout.write('# Done.\n')
    sys.stdout.flush()


if  __name__ == '__main__':
    main()

