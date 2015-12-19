import argparse
from itertools import product
import multiprocessing
import sys
import time


def get_conservation(tup):
    p = multiprocessing.current_process()

    lines, permutation = tup

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
    duration = end_ts - start_ts

    args = (p.pid, permutation, 
            found_permutations, possible_permutations, 
            start_ts, duration)

    lock.acquire()
    sys.stdout.write('{}\n'.format(','.join(str(a) for a in args)))
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
    headers = ('pid,permutation,'
               'found_permutations,possible_permutations,'
               'start_ts,duration')
    sys.stdout.write(headers + '\n')
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
    parser = argparse.ArgumentParser(
	description='Count occurrances of n-mer in data'
    )
    parser.add_argument('infile',
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
                     ''.format(args.mer_count, args.process_count))
    sys.stdout.flush()

    permutations = get_mer_permutations(args.mer_count)

    lines = get_sequence_lines(args.infile)

    sys.stdout.write('# Lines ID {}\n'.format(id(lines)))

    sys.stdout.write('# Running run_pool at {}/{}\n'
                     ''.format(datetime.now(), time.time()))
    run_pool(lines, permutations, args.process_count)


if  __name__ == '__main__':
    main()


