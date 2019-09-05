

import laspy


class LAZ(object):

    def __init__(self, bytes):
        d = laspy.File.File(None)
        self.bytes = _bytes
