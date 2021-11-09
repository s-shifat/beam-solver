from beam_package.loads.common_loads import *
from beam_package.utils.sign_convention import DIRECTION
from beam_package.beam.beam import Beam
import json
import sys


# file = './beam_test_data.json'
# file = './beam_test_data_2.json'
#file = './beam_test_data_4.json'
file = sys.argv[1]
b = Beam(json_path=file)
b.evaluate_json()
print(b.load_table)
b.calc_reaction()
print(b.load_table)
b.draw()
