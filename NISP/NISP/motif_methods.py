

def no_of_atoms_to_make_ico(noshells):
	if noshells < 1:
		raise ValueError("The number of shells must be equal to or greater than one.")
	xx = noshells - 1.0
	noAtoms = (2.0*xx + 1.0)*(5.0*xx**2.0 + 5.0*xx + 3.0)/3.0
	if not noAtoms%1 == 0:
		print('Error in Get_Interpolation_Data.py, class Get_Interpolation_Data, def no_of_atoms_to_make_ico.')
		print('noAtom does not seem to be an pure integer form. Check this.')
		print('noAtoms = ' + str(noAtoms))
		import pdb; pdb.set_trace()
		exit()
	return int(noAtoms)

def no_of_atoms_to_make_deca(p,q,r):
	# Using source code from ase
	if p < 1 or q < 1:
		raise ValueError("p and q must be greater than 0.")
	if r < 0:
		raise ValueError("r must be greater than or equal to 0.")
	h = p + q + 2*r - 1
	g = h - q + 1 # p + 2*r
	noAtoms = 0
	for j in range(h):
		noAtoms += 1
	for n in range(1, h):
		if n < g:
			for m in range(5):
				for i in range(n):
					if n - i < g - r and i < g - r:
						for j in range(h-n):
							noAtoms += 1
	if not noAtoms%1 == 0:
		print('Error in Get_Interpolation_Data.py, class Get_Interpolation_Data, def no_of_atoms_to_make_deca.')
		print('noAtom does not seem to be an pure integer form. Check this.')
		print('noAtoms = ' + str(noAtoms))
		import pdb; pdb.set_trace()
		exit()
	return int(noAtoms)

def no_of_atoms_to_make_octa(length,cutoff):
	if length < 2:
		raise ValueError("The lenght must be greater than one.")
	if cutoff < 0 or length < 2 * cutoff + 1:
		raise ValueError("The cutoff must fullfill: > 0 and <= (length - 1) / 2.")
	noAtoms = float(length)*(2.0*length**2.0 + 1.0)/3.0
	noAtoms -= 6.0*(cutoff*(cutoff+1.0)*(2.0*cutoff+1.0)/6.0)
	if not noAtoms%1 == 0:
		print('Error in Get_Interpolation_Data.py, class Get_Interpolation_Data, def no_of_atoms_to_make_octa.')
		print('noAtom does not seem to be an pure integer form. Check this.')
		print('noAtoms = ' + str(noAtoms))
		import pdb; pdb.set_trace()
		exit()
	return int(noAtoms)