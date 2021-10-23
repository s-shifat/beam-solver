import numpy as np

class Singularity:
    def __init__(self, points_along_lenght: np.ndarray, a, n):
        self.arr = points_along_lenght
        self.a = a
        self.n = n
        self.matrix = np.array(list(map(lambda x: self.singular_unit(x, a, n), self.arr)))

    @staticmethod
    def singular_unit(x, a, n):
        """
            format: <x-a>^n
            logic: by definition http://www.eng.uwaterloo.ca/~syde06/singularity-functions.pdf#page=1
        """
        if n < 0:
            if x != a:
                return 0
            elif x == a:
                return 0  # mathematically np.NaN though!
        elif n >= 0:
            if x < a:
                return 0
            elif x >= a:
                return (x - a) ** n  # possibility of 0**0