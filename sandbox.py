from beam_package.loads.common_loads import *
from beam_package.utils.sign_convention import DIRECTION
from beam_package.beam.beam import Beam
import json


# b = Beam(length=20)
# b.add_support(0, 'pin')
# b.add_support(20, 'roller')

# b.add_load(PointLoad(50, DIRECTION.DOWN, 5))
# b.add_load(Udl(10, DIRECTION.DOWN, 0, 10))
# b.add_load(Uvl(20, DIRECTION.DOWN, 10, 15))
# b.add_load(Moment(400, DIRECTION.ACW, 16.5))
# print(b.load_table)
# print('\n'*4)
# b.calc_reaction(upadate=True)
# print(b.load_table)

file = './beam_test_data.json'
file = './beam_test_data_2.json'
b = Beam(json_path=file)
# print(b.length)
b.evaluate_json()
print(b.load_table)
b.calc_reaction()
print(b.load_table)