#
# LAS/LAZ module
#

import laspy


class LAZ(object):
    def __init__(self, bytes):
        self.las = laspy.read(bytes)
