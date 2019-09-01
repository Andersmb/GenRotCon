# coding=utf-8

import math
import sys

# Dict containing all atomic weights of the elements, which will be used to calculate the centers of mass
# Hard coded to make the script more transferable (i.e. don't need libraries such as chempy or mendeleev)

atomic_mass = {'H': 1.008,
 'He': 4.002602,
 'Li': 6.94,
 'Be': 9.0121831,
 'B': 10.81,
 'C': 12.011,
 'N': 14.007,
 'O': 15.999,
 'F': 18.998403163,
 'Ne': 20.1797,
 'Na': 22.98976928,
 'Mg': 24.305,
 'Al': 26.9815385,
 'Si': 28.085,
 'P': 30.973761998,
 'S': 32.06,
 'Cl': 35.45,
 'Ar': 39.948,
 'K': 39.0983,
 'Ca': 40.078,
 'Sc': 44.955908,
 'Ti': 47.867,
 'V': 50.9415,
 'Cr': 51.9961,
 'Mn': 54.938044,
 'Fe': 55.845,
 'Co': 58.933194,
 'Ni': 58.6934,
 'Cu': 63.546,
 'Zn': 65.38,
 'Ga': 69.723,
 'Ge': 72.63,
 'As': 74.921595,
 'Se': 78.971,
 'Br': 79.904,
 'Kr': 83.798,
 'Rb': 85.4678,
 'Sr': 87.62,
 'Y': 88.90584,
 'Zr': 91.224,
 'Nb': 92.90637,
 'Mo': 95.95,
 'Tc': 97.90721,
 'Ru': 101.07,
 'Rh': 102.9055,
 'Pd': 106.42,
 'Ag': 107.8682,
 'Cd': 112.414,
 'In': 114.818,
 'Sn': 118.71,
 'Sb': 121.76,
 'Te': 127.6,
 'I': 126.90447,
 'Xe': 131.293,
 'Cs': 132.90545196,
 'Ba': 137.327,
 'La': 138.90547,
 'Ce': 140.116,
 'Pr': 140.90766,
 'Nd': 144.242,
 'Pm': 144.91276,
 'Sm': 150.36,
 'Eu': 151.964,
 'Gd': 157.25,
 'Tb': 158.92535,
 'Dy': 162.5,
 'Ho': 164.93033,
 'Er': 167.259,
 'Tm': 168.93422,
 'Yb': 173.045,
 'Lu': 174.9668,
 'Hf': 178.49,
 'Ta': 180.94788,
 'W': 183.84,
 'Re': 186.207,
 'Os': 190.23,
 'Ir': 192.217,
 'Pt': 195.084,
 'Au': 196.966569,
 'Hg': 200.592,
 'Tl': 204.38,
 'Pb': 207.2,
 'Bi': 208.9804,
 'Po': 209.0,
 'At': 210.0,
 'Rn': 222.0,
 'Fr': 223.0,
 'Ra': 226.0,
 'Ac': 227.0,
 'Th': 232.0377,
 'Pa': 231.03588,
 'U': 238.02891,
 'Np': 237.0,
 'Pu': 244.0,
 'Am': 243.0,
 'Cm': 247.0,
 'Bk': 247.0,
 'Cf': 251.0,
 'Es': 252.0,
 'Fm': 257.0,
 'Md': 258.0,
 'No': 259.0,
 'Lr': 262.0,
 'Rf': 267.0,
 'Db': 268.0,
 'Sg': 271.0,
 'Bh': 274.0,
 'Hs': 269.0,
 'Mt': 276.0,
 'Ds': 281.0,
 'Rg': 281.0,
 'Cn': 285.0,
 'Nh': 286.0,
 'Fl': 289.0,
 'Mc': 288.0,
 'Lv': 293.0,
 'Ts': 294.0,
 'Og': 294.0}


def load_xyz(filename):
    """
    Load the xyz file.
    :param filename: str: path to the tile
    :return: tuple: ([atomic_labels], [coordinates])
    """
    with open(filename) as f:
        xyz = [line.split() for line in f.readlines()[2:]]

    atoms = []
    for i, line in enumerate(xyz):
        atoms.append(line[0])
        del(xyz[i][0])

    coords = [list(map(float, atom)) for atom in xyz]
    return atoms, coords


def quaternion_rotation(angle=math.pi/2, axis=(1.0, 0.0, 0.0), coordinates=[]):
    """
    First compute the center of mass (com).
    Then translate molecule such that the center of mass is in the origin.
    Finally perform the quaternion rotation by "angle" radians around "axis".

    :param angle: by how many radians should the molecule be rotated?
    :param axis: tuple or list: rotate around this (unit!) vector
    :param coordinates: list: the pre-rotated atomic coordinates
    :return: list: rotated x, y, z coordinates of all atoms
    """
    # Compute the center of mass (com)
    com = [0, 0, 0]
    com[0] = sum([atomic_mass[atom] * coord[0] for atom, coord in zip(atoms, coordinates)]) / sum(
        [atomic_mass[atom] for atom in atoms])
    com[1] = sum([atomic_mass[atom] * coord[1] for atom, coord in zip(atoms, coordinates)]) / sum(
        [atomic_mass[atom] for atom in atoms])
    com[2] = sum([atomic_mass[atom] * coord[2] for atom, coord in zip(atoms, coordinates)]) / sum(
        [atomic_mass[atom] for atom in atoms])

    # Translate atomic coordinates so that COM is at the origo
    coords_translated = [[0, 0, 0] for i in range(len(coordinates))]
    for i, line in enumerate(coords_translated):
        for j in range(3):
            if j == 0:    # x
                coords_translated[i][0] = coords[i][j] - com[0]
            elif j == 1:  # y
                coords_translated[i][1] = coords[i][j] - com[1]
            elif j == 2:  # z
                coords_translated[i][2] = coords[i][j] - com[2]

    # Some shorthands for implementation of rotation formula
    gamma = math.cos(angle/2)
    theta = math.sin(angle/2)
    x = axis[0]  # Axis of rotation, x element
    y = axis[1]  # Axis of rotation, y element
    z = axis[2]  # Axis of rotation, z element

    # Perform the quaternion rotation
    coords_rot = [[] for i in range(len(coordinates))]
    for i, atom in enumerate(coordinates):
        px = atom[0]  # x element of vector to rotate
        py = atom[1]  # y element of vector to rotate
        pz = atom[2]  # z element of vector to rotate

        # Compute the x, y, and z elements of the rotated vector
        px_rot = px*theta**2 * (x**2 - y**2 - z**2) + 2*x*theta**2 * (y*py + z*pz) + 2*gamma*theta * (y*pz - z*py) \
                 + px*gamma**2

        py_rot = py*theta**2 * (y**2 - z**2 - x**2) + 2*y*theta**2 * (x*px + z*pz) + 2*gamma*theta * (z*px - x*pz) \
                 + py*gamma**2

        pz_rot = pz*theta**2 * (z**2 - y**2 - x**2) + 2*z*theta**2 * (x*px + y*py) + 2*gamma*theta * (x*py - y*px) \
                 + pz*gamma**2

        coords_rot[i] = [px_rot, py_rot, pz_rot]

    return coords_rot


help = ["--help", "-help", "-h", "-H", "h", "H", "help", "Help", "HELP", "--HELP"]
msg = """
SUMMARY
This script generates rotated conformers of the given molecule in each of the three dimensions.

REQUIREMENTS
Python version required: 2.6 or higher
It assumes the coordinates are given in a standard XYZ file, and that the atomic labels
in the first column are correctly typed atomic symbols 
(e.g. "H", not "h" or "1"; "Ca" not "ca" or "CA" or "20")

BACKGROUND INFORMATION
See Wheeler et al (2019, ChemRxiv) for more information
on the integration grid's variance to molecular orientation: 
https://doi.org/10.26434/chemrxiv.8864204.v5

USAGE
Run this script as follows:
$ python grc.py <coordinates.xyz>

You can change the number of conformers to generate by editing the variable "INCREMEMENT" in this script.

For this help message, run
$ python3 grc.py <arg>

where <arg> is one of
["--help", "-help", "-h", "-H", "h", "H", "help", "Help", "HELP", "--HELP"]

AUTHOR INFORMATION
|==========================================|
|This script was made by                   |
|Anders Brakestad                          |
|PhD Candidate in Computational Chemistry  |
|UiT The Arctic University of Tromsø       |
|anders.m.brakestad@uit.no                 |
|==========================================|
"""

if sys.argv[1] in help:
    sys.exit(msg)

# Load XYZ file
xyzfile = sys.argv[1]
assert xyzfile.endswith(".xyz"), "The molecular structure must be in an XYZ file: https://en.wikipedia.org/wiki/XYZ_file_format"
atoms, coords = load_xyz(xyzfile)

# Generate rotations in increments around x, y, and z axis
dims = {"x": [1, 0, 0],
        "y": [0, 1, 0],
        "z": [0, 0, 1]}

INCREMENT = 10  # This defines the number of rotations to perform in each dimension: n = 90 / INCREMENT
assert isinstance(INCREMENT, int), "The increment must be an integer!"

for dim in dims:
    for angle in range(INCREMENT, 90, INCREMENT):
        rad = angle * math.pi / 180
        coords_rot = quaternion_rotation(angle=rad, coordinates=coords, axis=dims[dim])

        outputname = xyzfile.split(".")[0] + "_{}_{}.xyz".format(dim, angle)
        with open(outputname, "w") as f:
            f.write("{}\n".format(len(coords_rot)))
            f.write("Rotated by {} degrees around {} axis\n".format(angle, dim))
            for atom, coord in zip(atoms, coords_rot):
                f.write("{} {}\n".format(atom, ' '.join(list(map(str, coord)))))

print("Number of rotational conformers generated: {}".format(3 * len(range(INCREMENT, 90, INCREMENT))))

if "-animation" in sys.argv or "--animation" in sys.argv:
    with open("animation.xyz", "w") as f:
        for angle in range(360):
            rad = angle * math.pi / 180
            rot = quaternion_rotation(angle=rad, axis=[1, 0, 0], coordinates=coords)

            f.write("{}\n".format(len(rot)))
            f.write("\n")
            for atom, coord in zip(atoms, rot):
                f.write("{} {}\n".format(atom, ' '.join(list(map(str, coord)))))