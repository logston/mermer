import argparse
from itertools import product
import multiprocessing
import sys
import time


def get_conservation(tup):
    start_ts = time.time()

    p = multiprocessing.current_process()

    lines, permutation = tup 
    line_counter = 0
    counter = 0
    len_permutation = len(permutation)
    for line in lines:
        line_counter += 1
        for i in range(len(line) - len_permutation + 1):
            if line[i:i + len_permutation] == permutation:
                counter += 1
   
    end_ts = time.time()

    lock.acquire()
    sys.stdout.write('{},{},{},{},{},{},{}\n'
                     ''.format(p.pid, permutation, counter,
                               start_ts, end_ts, end_ts - start_ts,
                               line_counter))
                               
    sys.stdout.flush()
    lock.release()

    return permutation

 
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
    expected_perm_count = pow(4, mer_count)
    if expected_perm_count != len(permutations):
        raise ValueError('Number of permutations for {}-mer combos is wrong: {}'
                         ''.format(mer_count, len(permutations)))
    sys.stdout.write('{} perumtations.\n'.format(len(permutations)))
    sys.stdout.flush()  
    return permutations


def worker_init(l):
    """Add lock to worker globals"""
    global lock
    lock = l


def run_pool(lines, permutations, cpu_count):
    sys.stdout.write('# Gathering args... ')
    sys.stdout.flush()   
    args = ((lines, per) for per in permutations)
 
    sys.stdout.write('throwing to pool...\n')
    sys.stdout.write('pid,permutation,count,start_ts,end_ts,duration,lines\n')
    sys.stdout.flush()   
    l = multiprocessing.Lock()
    pool = multiprocessing.Pool(initializer=worker_init, 
                                initargs=(l,),
                                processes=cpu_count)
    results = pool.map(get_conservation, args)
    sys.stdout.write('# Done.\n')
    sys.stdout.write('# {} permutations scanned for.\n'.format(len(results)))
    sys.stdout.flush()
    perms_left = set(permutations) - set(results)
    if perms_left:
        raise RuntimeError('Expected {} permutations to be scanned for.'
                           ' Permutations missing: {}'.format(perms_left))


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
    
    run_pool(lines, permutations, args.process_count)


if  __name__ == '__main__':
    main()

