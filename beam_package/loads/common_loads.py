from beam_package.loads.loadbase import LoadBase
from beam_package.utils.sign_convention import DIRECTION
from beam_package.singularity.exponents import SINGULARITY_EXPONENT


class PointLoad(LoadBase):
    EXPONENT = SINGULARITY_EXPONENT.POINT_LOAD
    END = 0
    IDX = 0
    SYMBOL = 'P'

    def __init__(self, load_magnitude, direction, position) -> None:
        PointLoad.IDX += 1
        super().__init__(self.EXPONENT, load_magnitude=load_magnitude,
                         direction=direction, start=position, end=self.END, index_tuple=(self.SYMBOL, self.IDX))


class Moment(LoadBase):
    EXPONENT = SINGULARITY_EXPONENT.MOMENT
    END = 0
    IDX = 0
    SYMBOL = 'M'

    def __init__(self, load_magnitude, direction, position) -> None:
        Moment.IDX += 1
        super().__init__(self.EXPONENT, load_magnitude=load_magnitude,
                         direction=direction, start=position, end=self.END, index_tuple=(self.SYMBOL, self.IDX))

    @property
    def moment_arm(self):
        return 0


class Udl(LoadBase):
    EXPONENT = SINGULARITY_EXPONENT.UDL
    IDX = 0
    SYMBOL = 'UDL'

    def __init__(self, load_magnitude, direction, start, end) -> None:
        super().__init__(exponent_=self.EXPONENT, load_magnitude=load_magnitude,
                         direction=direction, start=start, end=end, index_tuple=(self.SYMBOL, self.IDX))
        self.s = start
        self.e = end
    @property
    def pos0(self):
        return min(self.s, self.e)

    @property
    def pos1(self):
        return max(self.s, self.e)

    @property
    def moment_arm(self):
        return (self.pos0 + self.span / 2) * self.ROTATION_ADJUSTMENT

    @property
    def point_load(self):
        return self.load * self.span


class Uvl(LoadBase):
    EXPONENT = SINGULARITY_EXPONENT.UVL
    IDX = 0
    SYMBOL = 'UVL'

    def __init__(self, peak_load_magnitude, direction, zero_position, peak_position) -> None:
        super().__init__(exponent_=self.EXPONENT, load_magnitude=peak_load_magnitude,
                         direction=direction, start=zero_position, end=peak_position,
                         index_tuple=(self.SYMBOL, self.IDX))

        self.zero_position = self.s
        self.peak_position = self.e
        self.peak_is_far = self.peak_position > self.zero_position
        # print('Left:', self.peak_is_far)
        self.value = self.direction * self.absolute_load_magnitude

    @property
    def load(self):
        m = self.value / self.span
        return m  # slope for singularity function

    @property
    def moment_arm(self):
        distance = self.span * (2 / 3) if self.peak_is_far else self.span * (1 / 3)
        return (self.pos0 + distance) * self.ROTATION_ADJUSTMENT

    @property
    def point_load(self):
        return 0.5 * self.value * self.span


if __name__ == '__main__':
    p = PointLoad(50, DIRECTION.UP, 15)
    p2 = PointLoad(100, DIRECTION.DOWN, 20)

    m1 = Moment(220, DIRECTION.ACW, 40)
    m2 = Moment(450, DIRECTION.CW, 6)

    load_params = {
        'load_magnitude': 20,
        'direction': -1,
        'start': 10,
        'end': 50
    }