from pandas import DataFrame


#  id	Load Value	Type	Pos 0	Pos 1	Span	Point Load	Arm	Sign(moment)	moment		q	V	M	theta	deflection

class LoadTable(DataFrame):
    COLUMNS = [
        'Id',
        'exponent',
        'load',
        'pos0',
        'pos1',
        'span',
        'point_load',
        'moment_arm',
        'moment'
    ]

    def __init__(self, **kwargs):
        super().__init__(columns=LoadTable.COLUMNS, **kwargs)
