class LoadBase:
    ROTATION = -1

    def __init__(self, exponent_, load_magnitude, direction, start, end, index_tuple=None) -> None:
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

