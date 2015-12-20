import unittest

from smp import get_counts


class CountTC(unittest.TestCase):
    def test_get_counts(self):
        lines = [
            'TTCANAGTGGCTAAGTTCTGC',
        ]
        counter, possible_count = get_counts(lines, 2)
        self.assertEqual(possible_count, 20)
        counter = dict(counter)
        expected = {
            'AA': 1, 'AC': 0, 'AG': 2, 'AN': 1, 'AT': 0,
            'CA': 1, 'CC': 0, 'CG': 0, 'CN': 0, 'CT': 2,
            'GA': 0, 'GC': 2, 'GG': 1, 'GN': 0, 'GT': 2,
            'NA': 1, 'NC': 0, 'NG': 0, 'NN': 0, 'NT': 0,
            'TA': 1, 'TC': 2, 'TG': 2, 'TN': 0, 'TT': 2,
        }
        expected = {k: v for k, v in expected.items() if v}
        self.assertEqual(counter, expected)

