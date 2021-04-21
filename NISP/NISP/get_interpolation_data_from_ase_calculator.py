import time
import multiprocessing as mp

from NISP.NISP.Cluster import get_cluster, Cluster
from NISP.NISP.motif_methods import no_of_atoms_to_make_ico
from NISP.NISP.motif_methods import no_of_atoms_to_make_deca
from NISP.NISP.motif_methods import no_of_atoms_to_make_octa

def get_interpolation_data_from_ase_calculator(element,local_optimiser,e_coh,maximum_size,no_of_cpus):
	gidf_ASE_c = Get_Interpolation_Data_From_ASE_Calculator(element,local_optimiser,e_coh,maximum_size,no_of_cpus)
	gidf_ASE_c.input_with_calculator()
	ico_data, magic_numbers, octa_data, octa_magic, deca_data, deca_magic = gidf_ASE_c.get_data()
	return ico_data, magic_numbers, octa_data, octa_magic, deca_data, deca_magic

class Get_Interpolation_Data_From_ASE_Calculator:
	def __init__(self,element,local_optimiser,e_coh,maximum_size,no_of_cpus):
		self.element = element
		self.local_optimiser = local_optimiser
		self.e_coh = e_coh
		self.maximum_size = maximum_size
		self.no_of_cpus = no_of_cpus

	def get_data(self):
		return self.ico_data, self.magic_numbers, self.octa_data, self.octa_magic, self.deca_data, self.deca_magic 

	def input_with_calculator(self):
		self.ico_data,  self.magic_numbers = self.Get_Energies_Of_Icosahedrons()
		self.octa_data, self.octa_magic    = self.Get_Energies_Of_Octahedrals()
		self.deca_data, self.deca_magic    = self.Get_Energies_Of_Decahedrals()
		
	# This will obtain all the delta energies of all the icosahedral clusters that can be made with a cluster number less than 
	# an atom size of maximum_size. 
	def Get_Energies_Of_Icosahedrons(self):
		print('============================================================')
		print('Starting Obtaining Icosahedral Delta Energies')
		print('no atoms\tno of shells')
		noshells = 2
		magic_numbers = []
		tasks = []
		while True:
			no_atoms = no_of_atoms_to_make_ico(noshells)
			if no_atoms > self.maximum_size:
				break
			print(str(no_atoms) + ' \tnoshells: ' + str(noshells))
			tasks.append(['Icosahedron',[noshells],self.element,self.local_optimiser,self.e_coh,no_atoms])
			magic_numbers.append(no_atoms)
			noshells += 1
		for index in range(len(tasks)):
			#task = tasks[index]
			tasks[index] = tuple(tasks[index] + [len(tasks)])
		print('============================================================')
		print('Performing Tasks')
		start_time = time.time()
		ico_data = self.obtain_cluster_data(tasks)
		end_time = time.time()
		print('Time taken to get Icosahedral data was '+str(end_time - start_time)+' s.')
		print('Ending Obtaining Icosahedral Delta Energies')
		print('============================================================')
		return ico_data, magic_numbers

	# This will obtain all the delta energies of all the decahedral clusters that can be made with a cluster number less than 
	# an atom size of maximum_size. 
	def Get_Energies_Of_Decahedrals(self):
		print('============================================================')
		print('Starting Obtaining Decahedral Delta Energies')
		print('no atoms\tp\tq\tr')
		P_START = 2; Q_ORIGINAL = 1; R_ORIGINAL = 0
		
		p = P_START # p is the atom length along the 100_face_normal_to_5_fold_axis
		q = Q_ORIGINAL # q is the atom length along the 100_face_parallel_to_5_fold_axis
		r = R_ORIGINAL # r is the marks_reenterance_depth
		#previous_value_of_r = -1
		#deca_data = []; 
		deca_magic = []
		tasks = []
		while True:
			no_atoms = no_of_atoms_to_make_deca(p,q,r)
			if (r == R_ORIGINAL and q == Q_ORIGINAL) and (no_atoms > self.maximum_size):
				break
			previous_value_of_r = r 
			# From now on, at some point r (and potenitally p and q) will be modified to reflect that for the next cluster to sample
			if no_atoms <= self.maximum_size:
				print(str(no_atoms) + '\t\tp: ' + str(p) + ' \tq: ' + str(q) + ' \tr: ' + str(r))# + '\t,Calculate: ' + str(no_atoms < maximum_size) + '\t,previous r: ' + str(previous_value_of_r)
				deca_details = [p,q,r]
				tasks.append(['Decahedron',deca_details,self.element,self.local_optimiser,self.e_coh,no_atoms])
				r += 1 # r is now the value of r for the next cluster that will be made using this algorithm.
				if (r > q + 3):
					r = 0; q += 1
			else:
				r = 0; q += 1 # r and q are changed to reflect the next cluster
			if (q > p + 3) or (previous_value_of_r == 0 and r == 0):
				q = 1; p += 1 # p and q are changed to reflect the next cluster
		for index in range(len(tasks)):
			#task = tasks[index]
			tasks[index] = tuple(tasks[index] + [len(tasks)])
		print('============================================================')
		print('Performing Tasks')
		start_time = time.time()
		deca_data = self.obtain_cluster_data(tasks)
		deca_magic = self.obtain_cluster_magic_data(deca_data)
		end_time = time.time()
		print('Time taken to get Decahedral data was '+str(end_time - start_time)+' s.')
		print('Ending Starting Obtaining Decahedral Delta Energies')
		print('============================================================')
		return deca_data, deca_magic

	# This will obtain all the delta energies of all the octahedral clusters that can be made with a cluster number less than 
	# an atom size of maximum_size. 
	def Get_Energies_Of_Octahedrals(self):
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
		#octa_data = []; 
		octa_magic = []
		tasks = []
		while True:
			no_atoms = no_of_atoms_to_make_octa(length,cutoff)
			if (no_atoms > self.maximum_size) and (cutoff == cutoff_max):
				break
			if no_atoms <= self.maximum_size:
				print(str(no_atoms)+' \tlength: ' + str(length) + ' \tcutoff = ' + str(cutoff))
				octa_details = [length,cutoff]
				tasks.append(['Octahedron',octa_details,self.element,self.local_optimiser,self.e_coh,no_atoms])
			cutoff -= 1
			if cutoff < 0 or no_atoms > self.maximum_size:
				length += 1
				cutoff = get_max_cutoff_value(length)
				cutoff_max = cutoff
		for index in range(len(tasks)):
			#task = tasks[index]
			tasks[index] = tuple(tasks[index] + [len(tasks)])
		print('============================================================')
		print('Performing Tasks')
		start_time = time.time()
		octa_data  = self.obtain_cluster_data(tasks)
		octa_magic = self.obtain_cluster_magic_data(octa_data)
		end_time = time.time()
		print('Time taken to get Octahedral data was '+str(end_time - start_time)+' s.')
		print('Ending Obtaining Octahedral Delta Energies')
		print('============================================================')
		return octa_data, octa_magic

	def obtain_cluster_data(self,tasks):
		if self.no_of_cpus > 1:
			pool = mp.Pool(processes=self.no_of_cpus)
			manager = mp.Manager()
			counter = manager.Value('i', 0)
			tasks = [(task+(counter,)) for task in tasks]
			results = pool.map_async(get_cluster, tasks)
			results.wait()
			pool.close()
			pool.join()
			data = results.get()
		else:
			from NISP.NISP.Counter import Counter
			counter = Counter()
			data = [get_cluster(task+(counter,)) for task in tasks]
		return data

	def obtain_cluster_magic_data(self,data):
		magic = []
		for cluster in data:
			no_atoms = cluster.no_atoms
			if no_atoms in self.magic_numbers:
				magic.append(cluster) 
		return magic