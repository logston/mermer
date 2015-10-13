import argparse
from itertools import product
import os
import socket
import sys
import time

from mpi4py import MPI


COMM = MPI.COMM_WORLD
RANK = COMM.Get_rank()
SIZE = COMM.Get_size()


def calculate_conservation(infile, rank, mer_count):
    s = time.time()
    lines = get_sequence_lines(infile) 
    e = time.time()
    sys.stdout.write('Getting sequence lines took {} on rank {}\n'
                     ''.format(e - s, rank))
    sys.stdout.flush()

    s = time.time()
    permutations = get_mer_permutations(mer_count, rank)
    e = time.time()
    sys.stdout.write('Getting permutations took {} on rank {}\n'
                     ''.format(e - s, rank))
    sys.stdout.flush()

    for j, permutation in enumerate(permutations):
        start_ts = time.time()
    
        found_permutations = 0
        len_permutation = len(permutation)
        possible_permutations = 0
        for line in lines:
            len_line = len(line)

            possible_perms_in_line = len_line - len_permutation + 1
            possible_permutations += possible_perms_in_line

            for i in range(possible_perms_in_line):
                if line[i:i + len_permutation] == permutation:
                    found_permutations += 1
       
        end_ts = time.time()
    
        data = (socket.gethostname(), os.getpid(), RANK,
                j, permutation, found_permutations, possible_permutations,
                start_ts, end_ts - start_ts)
     
        COMM.send(data, dest=0)
    

def get_mer_permutations(mer_count, rank):
    permutations = sorted(''.join(p) for p in product('ATGC', repeat=mer_count))
    
    start_offset = rank - 1
   
    permutations = permutations[start_offset::mer_count - 1]

    return permutations

 
def get_sequence_lines(file_name):
    with open(file_name) as fp:
        file_lines = fp.read()

    lines = []
    for i, line in enumerate(file_lines.split('\n')):
        offset_i = i - 1
        if not offset_i % 4:
            lines.append(line)

    return lines


def write_headers(args):
    with open(args.outfile, 'w') as fp:
        fp.write('# Running {}-mer search with {} processes.\n'
                 ''.format(args.mer_count, args.process_count))
        fp.write('host,pid,rank,'
                 'perm_iter_id,permutation,count,found_permutations,'
                 'start_ts,duration\n')


def write_footers(outfile, len_results):
    with open(outfile, 'a') as fp:
        fp.write('# Done.\n')
        fp.write('# {} results recieved.\n'.format(len_results))


def main():
    parser = argparse.ArgumentParser(description='Count occurrances of n-mer in data')
    parser.add_argument('infile',
                        help='Sequence file to search for n-mers')
    parser.add_argument('outfile',
                        help='Results file') 
    parser.add_argument('mer_count',
                        type=int, 
                        help='Length of n-mer (in nucleotides)')
    parser.add_argument('-p', '--process-count', 
                        dest='process_count',
                        type=int,
                        default=1,
                        help='Number of processes to start')
    args = parser.parse_args()

    if not RANK:
        write_headers(args)
    
    len_results = 0
    if not RANK:
        # root, start recieving data
        with open(args.outfile, 'a', buffering=1) as fp:
            flush_t = -1
            for i in range(pow(4, args.mer_count)):
                s = time.time() 
                data = COMM.recv(source=MPI.ANY_SOURCE)
                data = ','.join(str(d) for d in data) + '\n'
                fp.write(data)
                e = time.time()
                flush_s = time.time()
                sys.stdout.write('Last flush took {}. Wait and write took {}.\n'
                                 ''.format(flush_t, e - s))
                sys.stdout.flush()
                flush_e = time.time()
                flush_t = flush_e - flush_s
        len_results = i
    else:
        # worker, start parsing file
       calculate_conservation(args.infile, RANK, args.mer_count)
 
    if not RANK:
        write_footers(args.outfile, len_results)


if  __name__ == '__main__':
    main()

