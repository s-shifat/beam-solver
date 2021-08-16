from beam_package.utils.dataholder import LoadTable
from beam_package.utils.sign_convention import DIRECTION


class LoadBase:
    ROTATION_ADJUSTMENT = -1

    def __init__(self, exponent_, load_magnitude=0, direction=DIRECTION.UP, start=0, end=0, index_tuple=None) -> None:
        """index_tuple -> P|M|D|V , Class.IDX"""
        self.df = LoadTable()
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
        return self.pos0 * self.ROTATION_ADJUSTMENT

    @property
    def moment(self):
        return self.point_load * self.moment_arm if self.moment_arm else self.point_load

    @property
    def unique_id(self):
        if self.idx_tuple:
            return self.idx_tuple[0] + str(self.idx_tuple[1])
        return

    @property
    def load_table(self):
        if len(self.df) == 0:
            self.df = self.df.append(LoadTable(data=[[
                self.unique_id,
                self.exponent_,
                self.load,
                self.pos0,
                self.pos1,
                self.span,
                self.point_load,
                self.moment_arm,
                self.moment
            ]]))
        return self.df

    def __repr__(self):
        return self.load_table.__repr__()
