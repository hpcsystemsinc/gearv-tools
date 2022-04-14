#! /usr/bin/python

import sys
import os
import shutil
import subprocess
import tarfile
import math

# @function convertF2C convert a fractional coordinate into a cartesian coordinate
# @param lattice_a list[ax, ay, az] of 1st lattice vector
# @param lattice_b list[bx, by, bz] of 2nd lattice vector
# @param lattice_c list[cx, cy, cz] of 3rd lattice vector
# @param x x in fractional coordinate
# @param y y in fractional coordinate
# @param z z in fractional coordinate
# @return [x, y, z] in cartesian coordinate
def convertF2C(lattice_a, lattice_b, lattice_c, x, y, z):
	ax = lattice_a[0]
	ay = lattice_a[1]
	az = lattice_a[2]
        #print('DEBUG: a[{}, {}, {}]'.format(ax, ay, az))
	bx = lattice_b[0]
	by = lattice_b[1]
	bz = lattice_b[2]
        #print('DEBUG: b[{}, {}, {}]'.format(bx, by, bz))
	cx = lattice_c[0]
	cy = lattice_c[1]
	cz = lattice_c[2]
        #print('DEBUG: c[{}, {}, {}]'.format(cx, cy, cz))
	alen = math.sqrt(ax*ax+ay*ay+az*az)
	#print('DEBUG: alen = {}'.format(alen))
	blen = math.sqrt(bx*bx+by*by+bz*bz)
	#print('DEBUG: blen = {}'.format(blen))
	clen = math.sqrt(cx*cx+cy*cy+cz*cz)
	#print('DEBUG: clen = {}'.format(clen))

	# lattice angles in radian
	# alpha : angle between b and c
	alpha = math.acos(((bx*cx)+(by*cy)+(bz*cz)) / (blen*clen))
	#print('DEBUG: alpha = {}'.format(alpha))
	# beta  : angle between a and c
	beta  = math.acos(((ax*cx)+(ay*cy)+(az*cz)) / (alen*clen))
	#print('DEBUG: beta  = {}'.format(beta))
	# gamma : angle between a and b
	gamma = math.acos(((ax*bx)+(ay*by)+(az*bz)) / (alen*blen))
	#print('DEBUG: gamma = {}'.format(gamma))

	# temporary variable v
	cos_alpha = math.cos(alpha)
	cos_beta  = math.cos(beta)
	cos_gamma = math.cos(gamma)
	v_square = 1.0
	v_square = v_square - (cos_alpha*cos_alpha)
	v_square = v_square - (cos_beta*cos_beta)
	v_square = v_square - (cos_gamma*cos_gamma)
	v_square = v_square + (2.0*cos_alpha*cos_beta*cos_gamma)
	v = math.sqrt(v_square)
	#print('DEBUG: v = {}'.format(v))

	# left matrix
	sin_gamma = math.sin(gamma)
	col1_x = alen
	col1_y = 0.0
	col1_z = 0.0
	col2_x = blen*cos_gamma
	col2_y = blen*sin_gamma
	col2_z = 0.0
	col3_x = clen*cos_beta
	col3_y = (clen*(cos_alpha-(cos_beta*cos_gamma))) / sin_gamma
	col3_z = (clen*v) / sin_gamma

	# matrix-vector multiply
	result_x = col1_x * x + col2_x * y + col3_x * z
	result_y = col1_y * x + col2_y * y + col3_y * z
	result_z = col1_z * x + col2_z * y + col3_z * z
	return [result_x, result_y, result_z]

#####################################################################

# Argument required
if len(sys.argv) < 2:
	sys.exit(1) # Do nothing

# Get argument and set directory variables
poscar_path = sys.argv[1]

# Read fractional POSCAR
with open(poscar_path) as f:
	comment = f.readline().strip()
	print(comment)

	scaling_factor = f.readline().strip()
	print(scaling_factor)

	a_line = f.readline().strip()
	print(a_line)
	lattice_a = [float(item) for item in a_line.strip().split()]

	b_line = f.readline().strip()
	print(b_line)
	lattice_b = [float(item) for item in b_line.strip().split()]

	c_line = f.readline().strip()
	print(c_line)
	lattice_c = [float(item) for item in c_line.strip().split()]

	# This line can be omitted.
	elements = f.readline().strip()
	print(elements)
	if elements.replace(' ','').isdigit() == False:
		numatoms = f.readline().strip()
		print(numatoms)

	# Loop here:
	is_frac = True
	while True:
		line = f.readline()
		if line == '':
			break

		striped = line.strip()
		chars = striped.replace(' ', '')
		first_char = chars[:1].lower()

		# Pattern 1: "Selective dynamics" -> no changes needed.
		if first_char == 's':
			print(striped)
		# Pattern 2: "Caltesian" -> no changes needed.
		elif first_char == 'c':
			is_frac = False
			print(striped)
		# Pattern 3: "Direct" -> after this line, conversion needed.
		elif first_char == 'd':
			is_frac = True
			print('Cartesian')
		# Pattern 4: coordinate
		elif first_char.isdigit():
			# If conversion is needed, do it.
			if is_frac:
				frac_coord = striped.split()
				# Pattern 4.A: x y z -> convert
				if len(frac_coord) == 3:
					cart_coord = convertF2C(lattice_a, lattice_b, lattice_c, float(frac_coord[0]), float(frac_coord[1]), float(frac_coord[2]))
					print('{:>19.9f} {:>19.9f} {:>19.9f}'.format(cart_coord[0], cart_coord[1], cart_coord[2]))
				# Pattern 4.B: x y z T|F T|F T|F -> convert, and just add the T|F as it is
				else:
					cart_coord = convertF2C(lattice_a, lattice_b, lattice_c, float(frac_coord[0]), float(frac_coord[1]), float(frac_coord[2]))
					print('{:>19.9f} {:>19.9f} {:>19.9f} {} {} {}'.format(cart_coord[0], cart_coord[1], cart_coord[2]), frac_coord[3], frac_coord[4], frac_coord[5])
			# Otherwise no changes needed.
			else:
				print(striped)
		# Unknown pattern. Just print as it is.
		else:
			print(striped)

# End of file
