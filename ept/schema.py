import numpy

class Schema(object):
    def __init__(self, data):
        self.dimensions = self._get_dimensions(data)

    def __len__(self):
        return len(self.dimensions)

    def _get_dimensions(self, data):
        dimensions = {}
        for d in data:
            name = d['name']

            kind = 'i'
            if d['type'] == 'unsigned':
                kind = 'u'
            elif d['type'] == 'signed':
                kind = 'i'
            elif d['type'] == 'float':
                kind = 'f'
            else:
                raise TypeError("Unrecognized type '%s'. Unable to convert to numpy dtype" % d['type'])

            d['dtype'] = kind+str(d['size'])

            dimensions[name] = d

        return dimensions


    def get_dtype(self):
        dt = []
        for d in self.dimensions:
            dim = self.dimensions[d]
            dt.append((dim['name'], dim['dtype']))

#        import pdb;pdb.set_trace()
        return numpy.dtype(dt)
    dtype = property(get_dtype)


