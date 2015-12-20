import argparse
import collections
from itertools import product
import sys
import time


def get_sequence_lines(file_name):
    """
    Parse ``file_name`` (fastq) file for nucleotide strings.
    """
    sys.stdout.write('# Reading sequence file "{}" ... '.format(file_name))
    sys.stdout.flush()
    with open(file_name) as fp:
        lines = fp.read().split('\n')
    sys.stdout.write('Done.\n')
    sys.stdout.flush()

    sys.stdout.write('# Gathering sequences ... ')
    sys.stdout.flush()
    lines = [line for i, line in enumerate(lines) if not (i -1) % 4]
    sys.stdout.write('{} sequences to search.\n'.format(len(lines)))
    sys.stdout.flush()
    return lines


def get_mer_permutations(mer_count):
    permutations = [''.join(p) for p in product('ATGC', repeat=mer_count)]
    expected_perm_count = pow(4, mer_count)

    if expected_perm_count != len(permutations):
        raise ValueError('Number of permutations for {}-mer combos is wrong: {}'
                         ''.format(mer_count, len(permutations)))

    return permutations


def get_counts(lines, mer_length):

    counter = collections.defaultdict(int)
    possible_permutations_count = 0

    for line in lines:
        last_offset = len(line) - mer_length + 1
        for offset in range(last_offset):
            mer = line[offset:offset + mer_length]
            counter[mer] += 1
        possible_permutations_count += last_offset

    return counter, possible_permutations_count


def run_count(lines, mer_length):
    start_ts = time.time()

    sys.stdout.write('# Running {}-mer search.\n'.format(mer_length))
    sys.stdout.write('# Searching {} nucleotide strings (started at {}) ... '
                     ''.format(len(lines), start_ts))
    sys.stdout.flush()

    counter, possible_permutations_count = get_counts(lines, mer_length)

    duration = time.time() - start_ts

    sys.stdout.write('took {} seconds\n'.format(duration))
    sys.stdout.write('# Found {} possible permutations\n'
                     ''.format(possible_permutations_count))
    sys.stdout.write('# Getting permutations ... ')
    sys.stdout.flush()

    valid_permutations = get_mer_permutations(mer_length)

    sys.stdout.write('{} permutations.\n'.format(len(valid_permutations)))

    sys.stdout.write('permutation,count\n')
    sys.stdout.flush()

    for permutation, count in counter.items():
        if permutation not in valid_permutations:
            continue
        sys.stdout.write('{},{}\n'.format(permutation, count))

    sys.stdout.write('# Done.\n')
    sys.stdout.flush()


def main():
    parser = argparse.ArgumentParser(
        description='Count occurrences of n-mer in data'
    )
    parser.add_argument('infile',
                        help='Sequence file to search for n-mers')
    parser.add_argument('mer_length',
                        type=int,
                        help='Length of n-mer (in nucleotides)')
    args = parser.parse_args()

    lines = get_sequence_lines(args.infile)

    run_count(lines, args.mer_length)


if  __name__ == '__main__':
    main()


