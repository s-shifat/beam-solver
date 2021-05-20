class DIRECTION:
    UP = 1
    DOWN = -1
    CW = 1
    ACW = -1


class LOAD_TYPES:
    UVL = 1
    UDL = 0
    POINT_LOAD = -1
    MOMENT = -2


class LoadBase:
    ROTATION = -1

    def __init__(self, type_, load_value=0, direction=DIRECTION.DOWN, start=0, end=0) -> None:
        self.type_ = type_
        self.load_value = load_value
        self.pos0 = min(start, end) if end else max(start, end)
        self.pos1 = max(start, end) if start and end else end
        self.direction = direction

    @property
    def load(self):
        return self.load_value * self.direction

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
        return self.point_load * self.moment_arm


class PointLoad(LoadBase):
    TYPE = LOAD_TYPES.POINT_LOAD
    END = 0

    def __init__(self, load_value, direction, position) -> None:
        super().__init__(self.TYPE, load_value=load_value,
                         direction=direction, start=position, end=self.END)


class Moment(LoadBase):
    TYPE = LOAD_TYPES.MOMENT
    END = 0

    def __init__(self, load_value, direction, position) -> None:
        super().__init__(self.TYPE, load_value=load_value,
                         direction=direction, start=position, end=self.END)

        self.moment_arm = 0


if __name__ == '__main__':
    load = PointLoad(50, DIRECTION.UP, 15)
    # print(dir(load))
    print(load.__dict__)
    print(load.moment)
