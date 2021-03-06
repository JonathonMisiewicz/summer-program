#__author__ = "mbowman"

import sys
sys.path.insert(0, '../../extra-files')

import masses as m

import numpy as np

class Molecule(object):
 
	def __init__(self, mole_str, units="angstrom"):
		"""
		Generates an instance of a molecule
		:param mole_str: string (typically .xyz file) describing a molecule
		:param units: units for geometry, angstrom or bohr (default is angstrom) 	
		"""	
		self.parse_molecule(mole_str)

	def parse_molecule(self, mole_str):
		"""
		Parses data from .xyz file to change class attributes
		:param mole_str: string (typically .xyz file) describing a molecule
		"""
		lines = mole_str.strip().split("\n")
		self.natom = int(lines[0])
		if lines[1].lower() == "angstrom":
			self.units = "angstrom"
		elif lines[1].lower() == "bohr":
			self.units = "bohr" 
		self.labels = [i.strip().split(" ")[0].strip() for i in lines[2:]]
		self.masses =  [m.get_mass( l ) for l in self.labels ]
		self.charges = [m.get_charge( l ) for l in self.labels ]
		tempArray = [i.split("   ")[1:4] for i in lines[2:]]
		for a in range(len(tempArray)):
			for b in range(len(tempArray[a])):
				tempArray[a][b] = float(tempArray[a][b]
)
		self.geom = np.array(tempArray)

	def to_bohr(self):
		"""
		Changes units of geometry to Bohr, adjusts geometry matrix accordingly
		"""
		if self.units == "angstrom":
			self.geom *= 1.88973
			self.units = "bohr"
	
	def to_angstrom(self):
		"""
		Changes units of geometry to Angstrom, adjusts geometry matrix accordingly
		"""
		if self.units == "bohr":
			self.geom /= 1.88973
			self.units = "angstrom"
	
	def xyz_string(self):
		"""
		Prints out data as it would appear in a .xyz file
		"""
		tempString = "%s\n%s\n" % (self.natom, self.units.title())
		for l in range(len(self.labels)):
			tempString += self.labels[l] + " " 
			tempString += '{0:16.10f}'.format(self.geom[l][0])
			tempString += '{0:16.10f}'.format(self.geom[l][1])
			tempString += '{0:16.10f}'.format(self.geom[l][2])
			tempString += "\n"
		return tempString
	
	def copy(self):
		"""
		Returns copy of self
		"""
		tempMol = Molecule(self.xyz_string())
		return tempMol
	
	def __len__(self):
		"""
		Overrides len(str) to instead return the number of atoms
		"""
		return self.natom

	def __str__(self):
		"""
		Overrides str() to instead return the Molecule object in a pretty format
		"""
		row =  "+---+------------------+------------------+------------------+ \n"
		tempString = ""
		tempString += row
		tempString += "| X | x-coordnate      | y-coordinate     | z-coordinate     | \n"
		tempString += row
		for l in range(len(self.labels)):
			tempString += "| " + self.labels[l] + " |"
			for a in range(3):
				tempString += ' {0:16.10f} |'.format(self.geom[l][a])
			tempString += '\n'
			tempString += row
		return tempString
 
	def __print__(self):
		"""
		Overrides print() to print the result of __str__ 
		"""
		print str()

	def __repr__(self):
		"""
		Overrides repr() to reurn .xyz format instead
		"""
		return xyz_string()
	
	def __add__(mol1, mol2):
		"""
		Overrides addition, combining two molecule objects to create a new molecule object
		The units for the new molecule object are equivalent to the first molecule
		This method does not currently check for redundancies
		:param mol1: First molecule instance, units taken from here
		:param mol2: Second molecule instance, units must be converted before addition
		"""
		tempMol = mol1.copy()
		tempMol.natom += mol2.natom
		tempMol.masses += mol2.masses
		tempMol.charges += mol2.charges
		tempMol.labels += mol2.labels
		tempMol2 = mol2.copy()
		if tempMol.units == "angstrom":
			tempMol2.to_angstrom
		elif tempMol.units == "bohr":
			tempMol2.to_bohr
		tempMol.geom = np.concatenate((mol1.geom, mol2.geom), axis=0)
		return tempMol

#Used to test Molecule class
if __name__ == "__main__":
	mole_str = open("../../extra-files/molecule.xyz").read()
	mol = Molecule(mole_str)
	print mol
