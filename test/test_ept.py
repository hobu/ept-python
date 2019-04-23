import unittest

from ept.ept import EPT

class TestEPT(unittest.TestCase):

    def setUp(self):
        self.e = EPT('test/ept-star')

    def test_info(self):
        self.assertEqual(len(self.e.info), 518862)
        self.assertEqual(self.e.info.span, 128)
        self.assertEqual(self.e.info.version, '1.0.0')
        self.assertEqual(self.e.info.datatype,'laszip')
        self.assertEqual(self.e.info.hierarchytype,'json')

    def test_srs(self):
        self.assertEqual(self.e.info.srs.is_projected, True)
        self.assertEqual(self.e.info.srs.datum.name, 'World Geodetic System 1984')
        self.assertEqual(self.e.info.srs.name, 'WGS 84 / Pseudo-Mercator')
        self.assertEqual(self.e.info.srs.to_epsg(), 3857)

    def test_bounds(self):
        self.assertAlmostEqual(self.e.info.bounds[0], 515363)
        self.assertAlmostEqual(self.e.info.bounds[1], 4918339)
        self.assertAlmostEqual(self.e.info.bounds[2], 2309)
        self.assertAlmostEqual(self.e.info.bounds[3], 515407)
        self.assertAlmostEqual(self.e.info.bounds[4], 4918383)
        self.assertAlmostEqual(self.e.info.bounds[5], 2353)

    def test_conforming(self):
        self.assertAlmostEqual(self.e.info.conforming[0], 515368)
        self.assertAlmostEqual(self.e.info.conforming[1], 4918340)
        self.assertAlmostEqual(self.e.info.conforming[2], 2322)
        self.assertAlmostEqual(self.e.info.conforming[3], 515402)
        self.assertAlmostEqual(self.e.info.conforming[4], 4918382)
        self.assertAlmostEqual(self.e.info.conforming[5], 2339)

    def test_schema(self):
        s = self.e.info.schema
        self.assertEqual(len(s), 14)

        dtype = s.dtype
        self.assertEqual(dtype.itemsize, 38)

    def test_count(self):
        e = EPT('test/ept-star')
        e.count()

if __name__ == '__main__':
    unittest.main()
