from itertools import product


def get_permutations(mer_count):
    return [''.join(p) for p in product('ATGC', repeat=mer_count)]


def get_conservation(fp, per):
    counter = 0
    for i, line in enumerate(fp.readlines()):
        j = i - 1
        if not j % 4:
            if per in line:
                counter += 1
    return counter
            
    
if  __name__ == '__main__':
    import sys
    permutations = get_permutations(int(sys.argv[2]))
    for per in permutations:
        print('Getting conservation for: {}'.format(per))
        with open(sys.argv[1]) as fp:
            conservation = get_conservation(fp, per)
            print('Conservation for {}: {}'.format(per, conservation)) 
    print('Done.')
    
