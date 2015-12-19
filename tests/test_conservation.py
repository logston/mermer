import unittest

from smp import occurrences
from smp import get_conservation


class OccurrencesTC(unittest.TestCase):
    def test_occrrences(self):
        count = occurrences('TTCANAGTGGCTAAGTTCTGC', 'TTC')
        self.assertEqual(count, 2)


class ConservationTC(unittest.TestCase):
    def test_get_conservation(self):
        lines = [
            'TTCANAGTGGCTAAGTTCTGC',
            'AACANTCAACGCTGTCGGTGAGTT',
            'ATTCNAGTGATTTAGCTTATAGGT',
        ]
        permutations = ('AA', 'AC', 'TC')
        expected = ((3, 66), (2, 66), (5, 66))
        for i, permutation in enumerate(permutations):
            results = get_conservation(lines, permutation)
            self.assertEqual(results, expected[i])

