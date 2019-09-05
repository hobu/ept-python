import unittest

from ept.endpoint import Endpoint

class TestRemoteEndpoint(unittest.TestCase):

    def setUp(self):
#        self.e = Endpoint('http://entwine.io/data/ept-star')
        self.e = Endpoint('https://raw.githubusercontent.com/PDAL/data/master/entwine/data/ept-star/')

    def test_info(self):
        self.assertEqual(self.e.remote, True)

    def test_fetch(self):
        d = self.e.get('/ept.json')
        self.assertEqual(len(d), 2192)

class TestLocalEndpoint(unittest.TestCase):

    def setUp(self):
        self.e = Endpoint('test/ept-star')

    def test_info(self):
        self.assertEqual(self.e.remote, False)

    def test_fetch(self):
        d = self.e.get('/ept.json')
        self.assertEqual(len(d), 2192)


if __name__ == '__main__':
    unittest.main()
