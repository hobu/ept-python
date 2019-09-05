import unittest

from ept.ept import EPT
from ept.hierarchy import Bounds

class TestEPT(unittest.TestCase):

    def setUp(self):
        self.e = EPT('test/ept-star')
#        self.e = EPT('http://entwine.io/data/ept-star')
#        self.e = Endpoint('https://raw.githubusercontent.com/PDAL/data/master/entwine/data/ept-star/')

    def test_info(self):
        self.assertEqual(len(self.e.info), 518862)
        self.assertEqual(self.e.info.span, 128)
        self.assertEqual(self.e.info.version, '1.0.0')
        self.assertEqual(self.e.info.datatype,'laszip')
        self.assertEqual(self.e.info.hierarchytype,'json')
#
    def test_srs(self):
        self.assertEqual(self.e.info.srs.is_projected, True)
        self.assertEqual(self.e.info.srs.datum.name, 'World Geodetic System 1984')
        self.assertEqual(self.e.info.srs.name, 'WGS 84 / Pseudo-Mercator')
        self.assertEqual(self.e.info.srs.to_epsg(), 3857)
#
    def test_bounds(self):
        self.assertAlmostEqual(self.e.info.bounds[0], 515363)
        self.assertAlmostEqual(self.e.info.bounds[1], 4918339)
        self.assertAlmostEqual(self.e.info.bounds[2], 2309)
        self.assertAlmostEqual(self.e.info.bounds[3], 515407)
        self.assertAlmostEqual(self.e.info.bounds[4], 4918383)
        self.assertAlmostEqual(self.e.info.bounds[5], 2353)
#
    def test_conforming(self):
        self.assertAlmostEqual(self.e.info.conforming[0], 515368)
        self.assertAlmostEqual(self.e.info.conforming[1], 4918340)
        self.assertAlmostEqual(self.e.info.conforming[2], 2322)
        self.assertAlmostEqual(self.e.info.conforming[3], 515402)
        self.assertAlmostEqual(self.e.info.conforming[4], 4918382)
        self.assertAlmostEqual(self.e.info.conforming[5], 2339)
#
    def test_schema(self):
        s = self.e.info.schema
        self.assertEqual(len(s), 14)
#
        dtype = s.dtype
        self.assertEqual(dtype.itemsize, 38)
#
    def test_count(self):
        e = EPT('test/ept-star')
        self.assertEqual(e.count(), 518862)
        self.assertEqual(len(e.overlaps_dict),65)
#
    def test_boundedCount(self):
        e = EPT('test/ept-star')
        b = Bounds(515380, 4918350, 2320, 515400, 4918370, 2325)
        e.queryBounds = b
        self.assertEqual(e.count(), 208375)
#        self.assertEqual(e.count(), 45930) # real count for this box
#
    def test_boundedDepth(self):
        e = EPT('test/ept-star')
#        e = EPT('http://entwine.io/data/ept-star')
#
        e.depthEnd = 3
        self.assertEqual(e.count(), 303955)
        self.assertEqual(len(e.overlaps_dict),27)
#
    def test_boundedResolution(self):
        e = EPT('test/ept-star')
#        e = EPT('http://entwine.io/data/ept-star')
#
        e.queryResolution = 0.1
        self.assertEqual(e.count(), 303955)

    def test_data(self):
        e = EPT('test/ept-star')
#        e = EPT('http://entwine.io/data/ept-star')
        d = e.data()
        print (d[0])


if __name__ == '__main__':
    unittest.main()
