from beam_package.beam.beam import Beam
from sys import argv

file = argv[1]
print()
print(" "*12,"#"*6," Beam Reaction Solver ","#"*6)

print("parsing json...")
b = Beam(json_path=file)
b.evaluate_json()
print("Input:")
print(b.load_table)
print("\n")
print("Reactions:")
b.calc_reaction()
print("\nOutput:")
print(b.load_table)
