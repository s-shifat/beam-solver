import numpy as np

class Singularity:
    def __init__(self, x, a, n) -> None:
        self.x = x
        self.a = a
        self. n = n

    @property
    def value(self):
        if self.n < 0:
            if self.x != self.a:
                return 0
            elif self.x == self.a:
                return 0  # mathematically np.NaN though!
        elif self.n >= 0:
            if self.x < self.a:
                return 0
            elif self.x >= self.a:
                return (self.x - self.a) ** self.n

def integrate(sing_obj):
    if sing_obj.n == -2:
        return Singularity(arr, a, -1)
    elif n == -1:
        return singular_x(arr, a, 0)
    elif n >= 0:
        return singular_x(arr, a, n + 1) / (n + 1)
