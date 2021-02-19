import os
from shutil import rmtree

from ase.io import write
from ase.cluster.icosahedron import Icosahedron
from ase.cluster.decahedron import Decahedron
from ase.cluster.octahedron import Octahedron

from NISP.NISP.motif_methods import no_of_atoms_to_make_ico
from NISP.NISP.motif_methods import no_of_atoms_to_make_deca
from NISP.NISP.motif_methods import no_of_atoms_to_make_octa

def write_files_for_manual_mode(element,e_coh,maximum_size,manual_mode,input_information_file):
	if manual_mode.lower() == 'vasp':
		manual_mode = 'vasp'
		filename_suffix = ''
	elif manual_mode == 'xyz':
		filename_suffix = '.xyz'
	else:
		print('Error in def write_files_for_manual_mode, in Manual_Mode.py')
		print('The entry for Manual Mode in the input_information dictionary must be one of the following:')
		print('\t* "VASP" - Obtain clusters as POSCARs.')
		print('\t* "xyz"  - Obtain clusters as xyz files.')
		print('\t* False  - Do not perform manual mode in NISP.')
		print('Sort this out.')
		exit('This program will finished without completing.')
	folder = 'clusters'
	if os.path.exists(folder):
		rmtree(folder)
	os.mkdir(folder)
	write_start_of_manual_mode_file(element,maximum_size,input_information_file)
	write_icosahedral_cluster(element,e_coh,maximum_size,manual_mode,filename_suffix,input_information_file,folder)
	write_octahedral_cluster (element,e_coh,maximum_size,manual_mode,filename_suffix,input_information_file,folder)
	write_decahedral_cluster (element,e_coh,maximum_size,manual_mode,filename_suffix,input_information_file,folder)
	print('Have finished making the '+str(input_information_file)+' file.')
	print('Obtain the energies of the clusters that have been added to the '+str(folder)+' folder and then add these energies to associated cluster in the '+str(input_information_file)+' file.')
	print('This program will not finish here')
	exit()

def write_start_of_manual_mode_file(element,maximum_size,input_information_file):
	with open(input_information_file,'w') as input_file:
		input_file.write('Element: '+str(element)+' Max_Size: '+str(maximum_size)+'\n')
		input_file.write('Enter the energies of the clusters below to the right most of each line (not the delta energies, NISP can do that for you later)'+'\n')
		input_file.write('------------------------------'+'\n')

def write_icosahedral_cluster(element,e_coh,maximum_size,manual_mode,filename_suffix,input_information_file,folder):
	print('============================================================')
	print('Starting Obtaining Icosahedral Delta Energies')
	print('no atoms\tno of shells')
	noshells = 2
	all_ico_details = []
	while True:
		no_atoms = no_of_atoms_to_make_ico(noshells)
		if no_atoms > maximum_size:
			break
		#---------------------------------------------------------------------------------
		# Make cluster
		print('Make icosahedral cluster: '+str(no_atoms) + ' \tnoshells: ' + str(noshells))
		cluster = Icosahedron(element,noshells=noshells)
		cluster.center(vacuum=10.0)
		name = 'Ico_'+str(no_atoms)+filename_suffix
		if manual_mode == 'vasp':
			os.mkdir(folder+'/'+name)
			write(folder+'/'+name+'/'+'POSCAR',cluster,format='vasp')
		else:
			write(name,cluster,manual_mode)
		#---------------------------------------------------------------------------------
		# make data for details
		no_atoms = len(cluster)
		ico_details = (no_atoms, noshells)
		all_ico_details.append(ico_details)
		#---------------------------------------------------------------------------------
		noshells += 1
		#---------------------------------------------------------------------------------
	print('============================================================')
	with open(input_information_file,'a') as input_file:
		input_file.write('Icosahedron\n')
		all_ico_details.sort()
		for no_atoms, noshells in all_ico_details:
			input_file.write(str(no_atoms)+'\t'+str(noshells)+'\t\n')

def write_decahedral_cluster(element,e_coh,maximum_size,manual_mode,filename_suffix,input_information_file,folder):
	print('============================================================')
	print('Starting Obtaining Decahedral Delta Energies')
	print('no atoms\tp\tq\tr')
	P_START = 2; Q_ORIGINAL = 1; R_ORIGINAL = 0
	
	p = P_START # p is the atom length along the 100_face_normal_to_5_fold_axis
	q = Q_ORIGINAL # q is the atom length along the 100_face_parallel_to_5_fold_axis
	r = R_ORIGINAL # r is the marks_reenterance_depth
	previous_value_of_r = -1

	all_deca_details = []
	while True:
		no_atoms = no_of_atoms_to_make_deca(p,q,r)
		if (r == R_ORIGINAL and q == Q_ORIGINAL) and (no_atoms > maximum_size):
			break
		previous_value_of_r = r 
		# From now on, at some point r (and potenitally p and q) will be modified to reflect that for the next cluster to sample
		if no_atoms <= maximum_size:
			print('Make decahedral cluster: '+str(no_atoms) + '\t\tp: ' + str(p) + ' \tq: ' + str(q) + ' \tr: ' + str(r))# + '\t,Calculate: ' + str(no_atoms < maximum_size) + '\t,previous r: ' + str(previous_value_of_r)
			#---------------------------------------------------------------------------------
			# Make cluster
			cluster = Decahedron(element,p=p,q=q,r=r)
			cluster.center(vacuum=10.0)
			name = 'Deca_'+str(p)+'_'+str(q)+'_'+str(r)+filename_suffix
			if manual_mode == 'vasp':
				os.mkdir(folder+'/'+name)
				write(folder+'/'+name+'/'+'POSCAR',cluster,format='vasp')
			else:
				write(name,cluster,manual_mode)
			#---------------------------------------------------------------------------------
			# make data for details
			deca_parameters = (p,q,r)
			deca_details = (no_atoms, deca_parameters)
			all_deca_details.append(deca_details)
			#---------------------------------------------------------------------------------
			r += 1 # r is now the value of r for the next cluster that will be made using this algorithm.
			if (r > q + 3):
				r = 0; q += 1
		else:
			r = 0; q += 1 # r and q are changed to reflect the next cluster
		if (q > p + 3) or (previous_value_of_r == 0 and r == 0):
			q = 1; p += 1 # p and q are changed to reflect the next cluster
	print('============================================================')
	with open(input_information_file,'a') as input_file:
		input_file.write('Decahedron\n')
		all_deca_details.sort()
		for no_atoms, (p, q, r) in all_deca_details:
			input_file.write(str(no_atoms)+'\t'+str(p)+'\t'+str(q)+'\t'+str(r)+'\t\n')

def write_octahedral_cluster(element,e_coh,maximum_size,manual_mode,filename_suffix,input_information_file,folder):
	def get_max_cutoff_value(length):
		max_cutoff = (length-1.0)/2.0 - 0.5*((length-1.0)%2.0)
		if not max_cutoff%1 == 0:
			print('Error in Get_Interpolation_Data, at def Get_Energies_Of_Octahedrals, at def get_max_cutoff_value: max_cutoff did not come out as an interger.\nCheck this.\nmax_cutoff = '+str(max_cutoff))
			import pdb; pdb.set_trace()
			exit()
		return int(max_cutoff)
	print('============================================================')
	print('Starting Obtaining Octahedral Delta Energies')
	print('no atoms\tlength\tcutoff')
	length = 2; cutoff = get_max_cutoff_value(length); cutoff_max = cutoff

	all_octa_details = []
	while True:
		no_atoms = no_of_atoms_to_make_octa(length,cutoff)
		if (no_atoms > maximum_size) and (cutoff == cutoff_max):
			break
		if no_atoms <= maximum_size:
			print(str(no_atoms)+' \tlength: ' + str(length) + ' \tcutoff = ' + str(cutoff))
			#---------------------------------------------------------------------------------
			# Make cluster
			cluster = Octahedron(element,length=length,cutoff=cutoff)
			cluster.center(vacuum=10.0)
			name = 'Octa_'+str(length)+'_'+str(cutoff)+filename_suffix
			if manual_mode == 'vasp':
				os.mkdir(folder+'/'+name)
				write(folder+'/'+name+'/'+'POSCAR',cluster,format='vasp')
			else:
				write(name,cluster,manual_mode)
			#---------------------------------------------------------------------------------
			# make data for details
			octa_parameters = (length,cutoff)
			octa_details = (no_atoms, octa_parameters)
			all_octa_details.append(octa_details)
			#---------------------------------------------------------------------------------
		cutoff -= 1
		if cutoff < 0 or no_atoms > maximum_size:
			length += 1
			cutoff = get_max_cutoff_value(length)
			cutoff_max = cutoff
	print('============================================================')
	with open(input_information_file,'a') as input_file:
		input_file.write('Octahedron\n')
		all_octa_details.sort()
		for no_atoms, (length, cutoff) in all_octa_details:
			input_file.write(str(no_atoms)+'\t'+str(length)+'\t'+str(cutoff)+'\t\n')