import json
from pyproj import CRS

from .schema import Schema


class Info(object):

    def __init__(self, data):
        self.data = json.loads(data)

    def __len__(self):
        return int(self.data['points'])

    def get_schema(self):
        return Schema(self.data['schema'])
    schema = property(get_schema)

    def get_span(self):
        return int(self.data['span'])
    span = property(get_span)

    def get_version(self):
        return self.data['version']
    version = property(get_version)

    def get_bounds(self):
        return self.data['bounds']
    bounds = property(get_bounds)

    def get_conforming(self):
        return self.data['boundsConforming']
    conforming = property(get_conforming)

    def get_datatype(self):
        return self.data['dataType']
    datatype = property(get_datatype)

    def get_hierarchytype(self):
        return self.data['hierarchyType']
    hierarchytype = property(get_hierarchytype)

    def get_srs(self):
        wkt = self.data['srs']['wkt']
        crs = CRS.from_user_input(wkt)
        return crs
    srs = property(get_srs)
