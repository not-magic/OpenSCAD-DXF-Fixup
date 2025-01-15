import ezdxf
import math
import sys
import os

doc = ezdxf.readfile(sys.argv[1])

msp = doc.modelspace()

vert_db = {}

circle_cutoff = 0.1
# this means all segments of a group must be < 2mm to be considered a circle
line_cutoff_dist_sq = 2*2

def add_line(pos, line):
	global vert_db

	try:
		vert_db[pos].append(entity)
	except:
		vert_db[pos] = [entity]


for idx, entity in enumerate(msp):
	if isinstance(entity, ezdxf.entities.Line):
		add_line(entity.dxf.start, entity)
		add_line(entity.dxf.end, entity)

# now build some groups of connected lines

grouped_lines = set()

groups = []

for pos, lines in vert_db.items():

	current_verts = set()
	current_verts.add(pos)

	current_group = set()
	lines_to_process = set(lines) - grouped_lines

	while lines_to_process:

		current_line = lines_to_process.pop()

		if current_line in current_group:
			continue

		current_group.add(current_line)
		lines_to_process |= (set(vert_db[current_line.dxf.start]) - current_group)
		lines_to_process |= (set(vert_db[current_line.dxf.end]) - current_group)

	if current_group:
		grouped_lines |= current_group
		groups.append(current_group)


line_groups = []
circle_groups = []

# process what these groups could be, try to find circles
for idx, group in enumerate(groups):

	avg_pos = [0.0, 0.0]
	can_be_circle = True

	for line in group:
		avg_pos[0] += line.dxf.start.x
		avg_pos[1] += line.dxf.start.y
		avg_pos[0] += line.dxf.end.x
		avg_pos[1] += line.dxf.end.y

		# check the line length, it must be < 2 to be considered a circle
		dx = line.dxf.end.x - line.dxf.start.x
		dy = line.dxf.end.y - line.dxf.start.y

		if dx*dx + dy*dy > line_cutoff_dist_sq:
			can_be_circle = False
			break

	if can_be_circle:
		avg_pos[0] /= len(group) * 2;
		avg_pos[1] /= len(group) * 2;

		# now see if the average distance to all points is very similar
		def calc_distance(pt):
			dx = pt.x - avg_pos[0]
			dy = pt.y - avg_pos[1]
			return dx*dx + dy*dy

		dist0 = calc_distance(list(group)[0].dxf.start)

		for line in group:

			if abs(calc_distance(line.dxf.start) - dist0) > circle_cutoff:
				can_be_circle = False
				break;

			if abs(calc_distance(line.dxf.end) - dist0) > circle_cutoff:
				can_be_circle = False
				break;

	if can_be_circle:
		circle_groups.append({
			"center": avg_pos,
			"radius": math.sqrt(dist0)
			})

	else:
		line_groups.append(group)


print(f"Found {len(line_groups)} line groups and {len(circle_groups)} circles")

# create a new DXF with circles actually being circles
newdoc = ezdxf.new()
newmsp = newdoc.modelspace()

for idx, lines in enumerate(line_groups):
	for line in lines:
		newmsp.add_line((line.dxf.start.x, line.dxf.start.y), (line.dxf.end.x, line.dxf.end.y))

for circle in circle_groups:
	newmsp.add_circle((circle['center'][0], circle['center'][1]), radius=circle['radius'])

output_path = os.path.splitext(sys.argv[1])[0] + "_fixed.dxf"
newdoc.saveas(output_path)
print(f"Wrote {output_path}")