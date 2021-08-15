from os import pardir
from numpy.linalg import inv
from pandas.core.accessor import DirNamesMixin
from beam_package.loads.common_loads import *
from beam_package.utils.sign_convention import DIRECTION
from beam_package.beam.beam import Beam
import numpy as np


class P:
    def __init__(self, **kwargs) -> None:
        self.name = kwargs['name']
        self.age = kwargs['age']


params = {
    'load_magnitude': 200,
    'direction': DIRECTION.UP,
    'start': 10,
    'end': 30
}

b = Beam(length=20)
b.add_support(0, 'pin')
b.add_support(20, 'roller')

b.add_load(PointLoad(50, DIRECTION.DOWN, 5))
b.add_load(Udl(10, DIRECTION.DOWN, 0, 10))
b.add_load(Uvl(20, DIRECTION.DOWN, 10, 15))
b.add_load(Moment(400, DIRECTION.ACW, 16.5))
print(b.load_table)
print('\n'*4)
# print(b.load_table['point_load'].sum())k

table = (b.load_table.iloc[:,1:]).copy()
knowns = table.dropna()
unkowns = table[table['load'].isna()]
print(knowns, '\n'*2, unkowns)

# inv_matrix = np.linalg.inv(np.array([
#     [1,1],
#     np.array(unkowns['pos0'])
# ]))
# inv_matrix = np.array([[1,1], np.array(unkowns['moment_arm'])])

sum_matrix = np.array([
    [knowns[knowns['exponent'] != -2]['point_load'].sum()],
    [knowns['moment'].sum()]
], dtype=np.float64)


inv_matrix = np.array(
    [[1,1],
    unkowns['moment_arm']],
    dtype=np.float64)
print(inv_matrix)

print('\n'*2, inv_matrix, '\n' ,sum_matrix)
inv_matrix = np.linalg.inv(inv_matrix)
solution = np.dot(inv_matrix, sum_matrix)
adjustment = np.array([[-1],[-1]])
solution = adjustment*solution
print('Solution:', solution)





