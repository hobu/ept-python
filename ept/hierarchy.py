import copy

class Bounds(object):
    def __init__(self, *args):
        self.coords = args
    def __repr__(self):
        return repr(self.coords)


class Key(object):
    def __init__(self, k=None):
        self.ids = [0, 0, 0]
        self.coords = [0.0 for i in range(6)]
        self.d = 0
        self.count = 0

        if k:
            if isinstance(k, Key):
                self.d = k.d
                self.ids = k.ids
                self.coords = k.coords

            elif len(k):
                self.d, x, y, z = [int(t) for t in k.split('-')]

                self.ids[0] = x
                self.ids[1] = y
                self.ids[2] = z

    def id(self):
        return '%d-%d-%d-%d' % (self.d, self.ids[0], self.ids[1], self.ids[2])

    def __repr__(self):
        minx = self.coords[0]; miny = self.coords[1]; minz = self.coords[2]
        maxx = self.coords[3]; maxy = self.coords[4]; maxz = self.coords[5]

        return "id: %s, box3d(%.3f %.3f %.3f %.3f %.3f %.3f) %d" % (self.id(), minx, miny, minz, maxx, maxy, maxz, self.count)

    def contains(self, other):
        return  self.coords[0] <= other.coords[0] and self.coords[3] <= other.coords[3] and \
                self.coords[1] <= other.coords[1] and self.coords[4] <= other.coords[4] and \
                self.coords[2] <= other.coords[2] and self.coords[5] <= other.coords[5]

    def overlaps(self, other):
        return  self.coords[0] <= other.coords[3] and self.coords[3] >= other.coords[0] and \
                self.coords[1] <= other.coords[4] and self.coords[4] >= other.coords[1] and \
                self.coords[2] <= other.coords[5] and self.coords[5] >= other.coords[2]

    def bisect(self, direction):

        key = copy.deepcopy(Key(self))

        key.d = key.d + 1

        def step(i):
            key.ids[i] = key.ids[i] * 2

            mid = key.coords[i] + (key.coords[i+3] - key.coords[i])/2.0

            positive = bool(direction & (int(1) << i))
            if positive:
                key.coords[i] = mid
                key.ids[i] = key.ids[i] + 1
            else:
                key.coords[i + 3] = mid

        for i in range(3):
            step(i)

        return key

