import numpy as np
from beam_package.loads.common_loads import Load


class Beam:
    def __init__(self, length, segments=1000):
        self.length = length
        self.segments = segments
        self.x = np.linspace(start=0, stop=self.length, num=self.segments)

    def add_load(self):
        return
