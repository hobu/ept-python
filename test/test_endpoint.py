import json
import unittest

from ept.endpoint import Endpoint

class TestRemoteEndpoint(unittest.TestCase):

    def setUp(self):
        self.e = Endpoint('https://raw.githubusercontent.com/PDAL/data/master/entwine/data/ept-star/')

    def test_info(self):
        self.assertEqual(self.e.remote, True)

    def test_fetch(self):
        d = self.e.get('/ept.json').replace(b"\r", b"")
        self.assertEqual(len(d), 2192)

class TestQueryParamEndpoint(unittest.TestCase):

    def setUp(self):
        self.e = Endpoint('https://httpbin.org', 'q=42')

    def test_info(self):
        self.assertEqual(self.e.remote, True)
        self.assertEqual(self.e.query, 'q=42')

    def test_fetch(self):
        j = json.loads(self.e.get('/anything'))
        # Our query parameters are parsed out into response.args.q, make sure
        # that they are forwarded properly.
        self.assertEqual(j['args']['q'], '42')

class TestLocalEndpoint(unittest.TestCase):

    def setUp(self):
        self.e = Endpoint('test/ept-star')

    def test_info(self):
        self.assertEqual(self.e.remote, False)

    def test_fetch(self):
        d = self.e.get('/ept.json').replace(b"\r", b"")
        self.assertEqual(len(d), 2192)


if __name__ == '__main__':
    unittest.main()
