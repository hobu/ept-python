import unittest

from ept.info import Info
from ept.hierarchy import Key
#from ept.hierarchy  import Key, Box

class TestKey(unittest.TestCase):

    def test_parse(self):
        k = Key()
        self.assertEqual(k.d, 0)

        with self.assertRaises(ValueError):
            k = Key('d-0-0-0')

        with self.assertRaises(ValueError):
            k = Key('0-0-0-0-0')

        with self.assertRaises(ValueError):
            k = Key('0-0')

    def test_id(self):
        k = Key('1-2-3-4')
        self.assertEqual(k.ids[0], 2)
        self.assertEqual(k.ids[1], 3)
        self.assertEqual(k.ids[2], 4)
        with self.assertRaises(IndexError):
            k.ids[3]


    def test_id_setting(self):
        k = Key('1-2-3-4')

        self.assertEqual(k.ids[0], 2)
        k.ids[0] = k.ids[0]+1
        self.assertEqual(k.ids[0], 3)
        self.assertEqual(k.id(), '1-3-3-4')

    def test_equal(self):
        k = Key('1-2-3-4')
        self.assertEqual(k.id(), '1-2-3-4')
        k = Key(k.id())
        self.assertEqual(k.id(), '1-2-3-4')

    def test_bounds(self):
        k = Key()
        k.coords = [
                515363,
                4918339,
                2309,
                515407,
                4918383,
                2353
        ]

        for direction in range(8):
            k.bisect(direction)

    def test_hash(self):
        k = Key()
        d = {k, 42}


if __name__ == '__main__':
    unittest.main()
