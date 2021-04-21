from NISP.NISP.Cluster import Cluster

from NISP.NISP.motif_methods import no_of_atoms_to_make_ico
from NISP.NISP.motif_methods import no_of_atoms_to_make_deca
from NISP.NISP.motif_methods import no_of_atoms_to_make_octa

def input_from_procesed_VASP_files(element,local_optimiser,e_coh,maximum_size):

	ico_details,  magic_numbers = Get_Energies_Of_Icosahedrons(maximum_size)
	deca_details                = Get_Energies_Of_Decahedrals(maximum_size, magic_numbers)
	octa_details                = Get_Energies_Of_Octahedrals(maximum_size, magic_numbers)

	motif_types = ['Ico', 'Deca', 'Octa']
	full_names_of_motifs    = {'Ico': 'Icosahedron', 'Deca': 'Decahedron', 'Octa': 'Octahedron'}
	all_details_to_process  = {'Ico': ico_details, 'Deca': deca_details, 'Octa': octa_details}
	data_to_obtain          = {'Ico': [], 'Deca': [], 'Octa': []}
	issues_with_data        = {motif_type: [] for motif_type in motif_types}
	for motif_type in motif_types:
		full_name_of_motif = full_names_of_motifs[motif_type]
		details_to_process = all_details_to_process[motif_type]
		data = data_to_obtain[motif_type]
		issues_with_datum = issues_with_data[motif_type]
		for detail, no_atoms in details_to_process:
			name = motif_type+'_'+'_'.join([str(xx) for xx in detail])
			DFT_energy, data_obtained_successfully = get_VASP_energy(name)
			if data_obtained_successfully:
				delta_energy = get_Delta_Energy(DFT_energy,no_atoms,e_coh)
				vasp_cluster_data = Cluster(full_name_of_motif,detail,no_atoms=no_atoms,delta_energy=delta_energy)
				data.append(vasp_cluster_data)
			else:
				issues_with_datum.append(name)

	did_all_finish = [(not len(xx) == 0) for xx in issues_with_data.values()]
	if any(did_all_finish):
		print('======================================================================')
		print('Error when processing the data from VASP calculation.')
		print('The following VASP files either did not complete or there was a problem that meant that VASP did not converge.')
		print()
		for motif_type in motif_types:
			issues_with_datum = issues_with_data[motif_type]
			if not len(issues_with_datum) == 0:
				print(motif_type)
				print('-'*len(motif_type))
				for cluster_name in issues_with_datum:
					print(cluster_name)
				print()
		print('Check this out before trying to run NISP again')
		print()
		print('NISP will finish without completing.')
		print('======================================================================')
		exit()
	
	ico_data  = data_to_obtain['Ico']
	deca_data = data_to_obtain['Deca']
	octa_data = data_to_obtain['Octa']

	deca_magic = obtain_cluster_magic_data(deca_data, magic_numbers)
	octa_magic = obtain_cluster_magic_data(octa_data, magic_numbers)

	return ico_data, magic_numbers, octa_data, octa_magic, deca_data, deca_magic

def get_VASP_energy(name):
	path = 'VASP_Clusters/'+name+'/OUTCAR'
	# do stuff # need to write
	raise Exception('This method (get_VASP_energy in input_from_procesed_VASP_files) is still to be written, to come back to later on')
	DFT_energy = 0.0
	data_obtained_successfully = False
	return DFT_energy, data_obtained_successfully

def get_Delta_Energy(energy,no_atoms,e_coh):
	"""
	Get Delta Energy
	"""
	delta_energy = (energy - no_atoms*e_coh)/(no_atoms**(2.0/3.0))
	return delta_energy

def Get_Energies_Of_Icosahedrons(maximum_size):
	print('============================================================')
	print('Types of Icosahedral Clusters that information will be gather from during processing')
	print('no atoms\tno of shells')
	noshells = 2
	magic_numbers = []
	ico_details = []
	while True:
		no_atoms = no_of_atoms_to_make_ico(noshells)
		if no_atoms > maximum_size:
			break
		print(str(no_atoms) + ' \tnoshells: ' + str(noshells))
		ico_detail = (noshells,)
		datum = (ico_detail, no_atoms)
		ico_details.append(datum)
		magic_numbers.append(no_atoms)
		noshells += 1
	print('============================================================')
	return ico_details, magic_numbers

# This will obtain all the delta energies of all the decahedral clusters that can be made with a cluster number less than 
# an atom size of maximum_size. 
def Get_Energies_Of_Decahedrals(maximum_size, magic_numbers):
	print('============================================================')
	print('Types of Decahedral Clusters that information will be gather from during processing')
	print('no atoms\tp\tq\tr')
	P_START = 2; Q_ORIGINAL = 1; R_ORIGINAL = 0
	
	p = P_START # p is the atom length along the 100_face_normal_to_5_fold_axis
	q = Q_ORIGINAL # q is the atom length along the 100_face_parallel_to_5_fold_axis
	r = R_ORIGINAL # r is the marks_reenterance_depth
	#previous_value_of_r = -1
	deca_details = []
	while True:
		no_atoms = no_of_atoms_to_make_deca(p,q,r)
		if (r == R_ORIGINAL and q == Q_ORIGINAL) and (no_atoms > maximum_size):
			break
		previous_value_of_r = r 
		# From now on, at some point r (and potenitally p and q) will be modified to reflect that for the next cluster to sample
		if no_atoms <= maximum_size:
			print(str(no_atoms) + '\t\tp: ' + str(p) + ' \tq: ' + str(q) + ' \tr: ' + str(r))# + '\t,Calculate: ' + str(no_atoms < maximum_size) + '\t,previous r: ' + str(previous_value_of_r)
			deca_detail = (p,q,r)
			datum = (deca_detail, no_atoms)
			deca_details.append(datum)
			r += 1 # r is now the value of r for the next cluster that will be made using this algorithm.
			if (r > q + 3):
				r = 0; q += 1
		else:
			r = 0; q += 1 # r and q are changed to reflect the next cluster
		if (q > p + 3) or (previous_value_of_r == 0 and r == 0):
			q = 1; p += 1 # p and q are changed to reflect the next cluster
	print('============================================================')
	return deca_details

# This will obtain all the delta energies of all the octahedral clusters that can be made with a cluster number less than 
# an atom size of maximum_size. 
def Get_Energies_Of_Octahedrals(maximum_size, magic_numbers):
	def get_max_cutoff_value(length):
		max_cutoff = (length-1.0)/2.0 - 0.5*((length-1.0)%2.0)
		if not max_cutoff%1 == 0:
			print('Error in Get_Interpolation_Data, at def Get_Energies_Of_Octahedrals, at def get_max_cutoff_value: max_cutoff did not come out as an interger.\nCheck this.\nmax_cutoff = '+str(max_cutoff))
			import pdb; pdb.set_trace()
			exit()
		return int(max_cutoff)
	print('============================================================')
	print('Types of Octahedral Clusters that information will be gather from during processing')
	print('no atoms\tlength\tcutoff')
	length = 2; cutoff = get_max_cutoff_value(length); cutoff_max = cutoff
	octa_details = []
	while True:
		no_atoms = no_of_atoms_to_make_octa(length,cutoff)
		if (no_atoms > maximum_size) and (cutoff == cutoff_max):
			break
		if no_atoms <= maximum_size:
			print(str(no_atoms)+' \tlength: ' + str(length) + ' \tcutoff = ' + str(cutoff))
			octa_detail = (length,cutoff)
			datum = (octa_detail, no_atoms)
			octa_details.append(datum)
		cutoff -= 1
		if cutoff < 0 or no_atoms > maximum_size:
			length += 1
			cutoff = get_max_cutoff_value(length)
			cutoff_max = cutoff
	print('============================================================')
	return octa_details

def obtain_cluster_magic_data(data,magic_numbers):
	magic = []
	for cluster in data:
		no_atoms = cluster.no_atoms
		if no_atoms in magic_numbers:
			magic.append(cluster) 
	return magic