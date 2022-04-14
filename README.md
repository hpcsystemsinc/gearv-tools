# gearv-tools
Assistive tools for [GEAR-V](https://www.hpc.co.jp/chem/software/gear-v/) are placed in this repository.

## POSCAR_fractional2cartesian.py
This is a program that converts the atomic coordinates of POSCAR in VASP.

[VASP's POSCAR supports](https://www.vasp.at/wiki/index.php/POSCAR) fractional coordinates and cartesian coordinates as coordinates for writing atomic coordinates. However, GEAR-V only supports cartesian coordinates. This program converts POSCAR, which describes atomic coordinates in fractional coordinates, to POSCAR, which describes atomic coordinates in cartesian coordinates, and outputs it to standard output.

__Usage: POSCAR_fractional2cartesian.py &lt;path to POSCAR&gt;__
