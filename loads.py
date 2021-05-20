class DIRECTION:
    '''Global Sign Convention'''
    UP = 1
    DOWN = -1
    CW = 1
    ACW = -1


class SINGULARITY_EXPONENT:
    '''<x - a>**n here n is singularity exponent'''
    UVL = 1
    UDL = 0
    POINT_LOAD = -1
    MOMENT = -2


class LoadBase:
    ROTATION = -1

    def __init__(self, exponent_, load_magnitude=0, direction=DIRECTION.DOWN, start=0, end=0, index_tuple=None) -> None:
        '''index_tuple -> P|M|D|V , Class.IDX'''
        self.exponent_ = exponent_
        self.absolute_load_magnitude = load_magnitude
        self.s = start
        self.e = end
        self.direction = direction
        self.idx_tuple = index_tuple

    @property
    def pos0(self):
        return min(self.s, self.e) if self.e else max(self.s, self.e)

    @property
    def pos1(self):
        return max(self.s, self.e) if self.s and self.e else self.s

    @property
    def load(self):
        return self.absolute_load_magnitude * self.direction

    @property
    def span(self):
        return abs(self.pos1 - self.pos0)

    @property
    def point_load(self):
        return self.load

    @property
    def moment_arm(self):
        return self.pos0 * self.ROTATION

    @property
    def moment(self):
        return self.point_load * self.moment_arm if self.moment_arm else self.point_load

    @property
    def unique_id(self):
        return self.idx_tuple[0] + str(self.idx_tuple[1])

    def __repr__(self, child_name) -> str:
        return f"ID:{self.unique_id}\n{child_name}(load={self.load}, pos0={self.pos0}, pos1={self.pos1},\n\tmoment={self.moment}, moment_arm={self.moment_arm},\n\tpoint_load={self.point_load},span={self.span},\n\texponent={self.exponent_})"


class PointLoad(LoadBase):
    EXPONENT = SINGULARITY_EXPONENT.POINT_LOAD
    END = 0
    IDX = 0
    SYMBOL = 'P'

    def __init__(self, load_magnitude, direction, position) -> None:
        PointLoad.IDX += 1
        super().__init__(self.EXPONENT, load_magnitude=load_magnitude,
                         direction=direction, start=position, end=self.END, index_tuple=(self.SYMBOL, self.IDX))

    def __repr__(self) -> str:
        return super().__repr__(PointLoad.__name__)


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

    def __repr__(self) -> str:
        return super().__repr__(Moment.__name__)


class Udl(LoadBase):
    EXPONENT = SINGULARITY_EXPONENT.UDL
    IDX = 0
    SYMBOL = 'D'
    



if __name__ == '__main__':
    p = PointLoad(50, DIRECTION.UP, 15)
    p2 = PointLoad(100, DIRECTION.DOWN, 20)

    m1 = Moment(220, DIRECTION.ACW, 40)
    m2 = Moment(450, DIRECTION.CW, 6)

    print(*[x.__dict__ for x in [p, p2, m1, m2]], sep='\n')
