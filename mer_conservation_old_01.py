from itertools import product
from multiprocessing import Pool
import sys


def get_permutations(mer_count):
    return [''.join(p) for p in product('ATGC', repeat=mer_count)]


def get_conservation(per):
    sys.stdout.write('Getting conservation for: {}\n'.format(per))
    sys.stdout.flush()
    counter = 0
    with open(sys.argv[1]) as fp:
        for i, line in enumerate(fp.readlines()):
            j = i - 1
            if not j % 4:
                if per in line:
                    counter += 1
    sys.stdout.write('Conservation for {}: {}\n'.format(per, counter)) 
    sys.stdout.flush()
          
 
if  __name__ == '__main__':
    sys.stdout.write('Getting perumtations\n')
    sys.stdout.flush() 
    mer_count = int(sys.argv[2])
    permutations = get_permutations(mer_count)
    sys.stdout.write('Received permutations\n')
    sys.stdout.flush()

    pool = Pool(processes=int(sys.argv[3]))
    pool.map(get_conservation, permutations)

    sys.stdout.write('Done.\n')
    sys.stdout.flush()

