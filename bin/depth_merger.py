# depth_merger.py combines all counts from multiple depth file

import argparse
import sys


#########
# funcs #
#########

def read_depth_file(filepath):
	depth_dict = {}
	target_name = None
	with open(filepath, 'r') as fin:
		for line in fin:
			parts = line.strip().split('\t')

			if len(parts) != 3:
				print(f"[D merger] Error: Non-standard depth file {filepath}")
				sys.exit(1)
			seq_name, pos, count = parts

			if target_name is None:
				target_name = seq_name
			elif seq_name != target_name:
				print(f"[D merger] Error: Multiple targets in {filepath}")
				sys.exit(1)
			depth_dict[int(pos)] = int(count)

	return target_name, depth_dict


############
# argparse #
############

parser = argparse.ArgumentParser(description="Combine multiple depth files into one")
parser.add_argument('-i', '--input', nargs='+', required=True,
	help="Input depth files in tab-delimited cols: target pos count")
parser.add_argument('-o', '--output', default='./combined.dep',
	help="Output combined depth file")
args = parser.parse_args()


######
# in #
######

all_depths = []
target_name = None

for f in args.input:
	seq, depth = read_depth_file(f)

	if target_name is None:
		target_name = seq
	elif seq != target_name:
		print(f"[D merger] Error: Target mismatch: {seq} != {target_name}")
		sys.exit(1)

	all_depths.append(depth)

length_set = {len(d) for d in all_depths}
if len(length_set) != 1:
	print(f"[D merger] Error: Depth files have different number of positions {' '.join(str(l) for l in length_set)}")
	sys.exit(1)

positions = sorted(all_depths[0].keys())
for d in all_depths[1:]:
	if sorted(d.keys()) != positions:
		print("[D merger] Error: Position mismatch between depth files")
		sys.exit(1)

combined = {}
for pos in positions:
	combined[pos] = sum(d[pos] for d in all_depths)


#######
# out #
#######

with open(args.output, 'w') as out:
	for pos in positions:
		out.write(f"{target_name}\t{pos}\t{combined[pos]}\n")
