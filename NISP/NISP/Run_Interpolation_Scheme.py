#####################################################################################
#
# Geoffrey Weal, Get_Interpolation_Data.py, 28/4/2018
# This program is designed to create a plot of the rules
# connecting the complete structures of Decahedron, Octahedron 
# and Icosahedron cluster using Annas Interpolation Scheme.
#
# This algorithm works by creating an instance of Get_Interpolation_Data
#
#####################################################################################

print('Loading matplotlib')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
print('Loading nanocluster modules')
from NISP.NISP.Cluster import get_cluster, Cluster
print('Loading the interpolation rules')
from NISP.NISP.Interpolation_rules import Rule_deca_reent, Rule_deca_plane, Rule_deca_111
from NISP.NISP.Interpolation_rules import Rule_octa_111, Rule_octa_fcc
from NISP.NISP.Interpolation_rules import Rule_ico
print('Loading Connection modules')
from NISP.NISP.Interpolation_Connection import make_connection
print('Loading icosahedral, decahedral, and octahedral methods')
from NISP.NISP.motif_methods import no_of_atoms_to_make_ico
from NISP.NISP.motif_methods import no_of_atoms_to_make_deca
from NISP.NISP.motif_methods import no_of_atoms_to_make_octa
print('Loading methods for manual mode')
from NISP.NISP.Manual_Mode import write_files_for_manual_mode
print('Loading os, timing, and multiprocessing modules')
import os, time
import multiprocessing as mp
print('Beginning Interpolation Program')

def check_value(value,plot_information,default):
	if value in plot_information:
		return plot_information[value]
	else:
		return default

# This is the main class from this program. This is the program that does everything
class Run_Interpolation_Scheme:
	'''
	This program is designed to run and give the results of the interpolation scheme as described in A. L. Garden, A. Pedersen, H. Jónsson, “Reassignment of ‘magic numbers’ of decahdral and FCC structural motifs”, Nanoscale, 10, 5124-5132 (2018).
	'''
	def __init__(self,input_information,output_information={},no_of_cpus=1,filename_prefix=''):
		self.setup_for_input_data(input_information,no_of_cpus,filename_prefix)
		self.get_input_data()
		self.setup_for_running_interpolation(output_information,filename_prefix)
		self.run_interpolation()

	# ------------------------------------------------------------------------------------------------------------------
	# The following definitions are those for setting up the program

	def setup_for_input_data(self,input_information,no_of_cpus,filename_prefix):
		self.input_information = input_information
		self.element = self.input_information['Element Type']
		self.e_coh = self.input_information['Cohesive Energy']
		self.maximum_size = self.input_information['Maximum No. of Atoms']
		self.local_optimiser = check_value('Local Optimiser',self.input_information,None)
		self.manual_mode = check_value('Manual Mode',self.input_information,False)
		self.no_of_cpus = no_of_cpus
		self.filename_prefix = filename_prefix
		if self.filename_prefix == '':
			self.filename_prefix = str(self.element) + '_Max_Size_' + str(self.maximum_size)
		input_file_suffix =   '_atoms_interpolation_scheme_input_file.txt'
		results_file_suffix = '_atoms_interpolation_scheme_results_file.txt'
		self.input_information_file    = self.filename_prefix + input_file_suffix
		self.delta_energy_results_file = self.filename_prefix + results_file_suffix

	def setup_for_running_interpolation(self,output_information,filename_prefix):
		self.output_information = output_information
		self.sizes_to_interpolate = check_value('Size to Interpolate Over',self.output_information,[])
		for size_to_interpolate in self.sizes_to_interpolate:
			if size_to_interpolate >= self.maximum_size:
				print('The sizes in sizes_to_interpolate must be less than maximum_size')
				print('sizes_to_interpolate = ' + str(self.sizes_to_interpolate))
				print('maximum_size = ' + str(self.maximum_size))
				exit('')
			if size_to_interpolate <= 0:
				print('The sizes in sizes_to_interpolate must be greater than 0')
				print('sizes_to_interpolate = ' + str(sizes_to_interpolate))
				exit('')
		# -----------------------------------------------------------------
		self.higherNoAtomRange = check_value('Upper No of Atom Range',  self.output_information,None) 
		self.lowerNoAtomRange  = check_value('Lower No of Atom Range',  self.output_information,None) 
		if self.lowerNoAtomRange == None:
			self.lowerNoAtomRange = 0
		self.higherDERange     = check_value('Upper Delta Energy Range',self.output_information,None) 
		self.lowerDERange      = check_value('Lower Delta Energy Range',self.output_information,None) 
		# -----------------------------------------------------------------

	# ------------------------------------------------------------------------------------------------------------------------------
	# The following def will write all the files that you need for manual mode

	def write_manual_files(self):
		write_files_for_manual_mode(self.element,self.e_coh,self.maximum_size,self.manual_mode,self.input_information_file)

	# ------------------------------------------------------------------------------------------------------------------------------
	# The following defs are for obtaining the delta energies of all combinations of icosahedral, decahedral and octahedral clusters 

	def get_input_data(self):
		if os.path.exists(self.delta_energy_results_file):
			self.input_from_file(self.delta_energy_results_file,False)
		elif self.manual_mode and os.path.exists(self.input_information_file):
			self.input_from_file(self.input_information_file,   True)
		elif not (self.manual_mode in [False,'F','f','false','FALSE','False']):
			self.write_manual_files()
		else:
			self.input_with_calculator()

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
			task = tasks[index]
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
		previous_value_of_r = -1
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
			task = tasks[index]
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
			task = tasks[index]
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




	def input_from_file(self,input_file,manual_mode_file_found):
		print('--------------------------------------------------')
		if manual_mode_file_found:
			print('Found the file called '+str(input_file))
			print('This file was made because you want to run NISP in manual mode')
			print()
			print('To be used, it needs to contain:')
			print('\t* The various perfect closed shell icosahedral, decahedral, and octahedral clusters.')
			print('\t* The parameters used to make those clusters')
			print('\t* You need to enter the energy of the clusters after these')
		else:
			print('Found the file called '+str(input_file))
			print('This file was made from the first time you ran the interpolation scheme')
			print()
			print('This file contained all the information required to perform the interpolation scheme')
			print('It contains:')
			print('\t* The various perfect closed shell icosahedral, decahedral, and octahedral clusters.')
			print('\t* The parameters used to make those clusters')
			print('\t* The delta energy of the cluster with your chosen potential')
		print('--------------------------------------------------')
		self.ico_data  = []; self.magic_numbers = []
		self.deca_data = []; self.deca_magic = []
		self.octa_data = []; self.octa_magic = []
		self.maximum_size = -1
		motif_type = ''; #inputting = None
		with open(input_file,'r') as file:
			text_details = file.readline()
			self.element = text_details.split()[1]
			self.maximum_size = int(text_details.split()[3])
			if manual_mode_file_found:
				file.readline()
			file.readline()
			line_count = 0
			for line in file:
				line_count += 1
				if line == 'Icosahedron\n':
					inputting = self.ico_data
					motif_type = 'Icosahedron'
				elif line == 'Decahedron\n':
					inputting = self.deca_data
					motif_type = 'Decahedron'
				elif line == 'Octahedron\n':
					inputting = self.octa_data
					motif_type = 'Octahedron'
				else:
					datum = line.rstrip().split('\t')
					noAtoms = int(datum[0])
					if noAtoms > self.maximum_size:
						self.maximum_size = noAtoms
					try:
						if motif_type == 'Icosahedron':
							motif_details = [int(datum[1])]
							delta_energy  =  float(datum[2])
						elif motif_type == 'Decahedron':
							motif_details = [int(datum[1]), int(datum[2]), int(datum[3])]
							delta_energy  =  float(datum[4])
						elif motif_type == 'Octahedron':
							motif_details = [int(datum[1]), int(datum[2])]
							delta_energy  = float(datum[3])
					except IndexError as exception_message:
						if manual_mode_file_found:
							tostring  = 'Error when inputting data from '+str(input_file)+'.\n'
							tostring += 'One of your entries in this file was not filled in completely.\n'
							tostring += 'Check line '+str(line_count)+' of '+str(input_file)+' and see if you have filled this in completely.\n'
							tostring += str(exception_message)
							raise IndexError(tostring)
						else:
							raise IndexError(exception_message)
					#motif_details = eval('['+','.join(datum[1:-1])+']')
					#delta_energy = float(datum[-1].split('\n')[0])
					cluster = Cluster(motif_type,motif_details,no_atoms=noAtoms,delta_energy=delta_energy)
					inputting.append(cluster)
		self.magic_numbers = [x.no_atoms for x in self.ico_data]
		self.deca_magic = [x for x in self.deca_data if x.no_atoms in self.magic_numbers]
		self.octa_magic = [x for x in self.octa_data if x.no_atoms in self.magic_numbers]

	# ------------------------------------------------------------------------------------------------------------------------------

	def run_interpolation(self):
		self.deca_data. sort(key=lambda x:x.no_atoms)
		self.octa_data. sort(key=lambda x:x.no_atoms)
		self.ico_data.  sort(key=lambda x:x.no_atoms)
		self.deca_magic.sort(key=lambda x:x.no_atoms)
		self.octa_magic.sort(key=lambda x:x.no_atoms)

		self.print_cluster(self.ico_data)
		self.print_cluster(self.octa_data)
		self.print_cluster(self.deca_data)
		self.print_cluster(self.octa_magic,magic=True)
		self.print_cluster(self.deca_magic,magic=True)
		self.output_to_file()

		self.deca_connections = []; self.octa_connections = []; self.ico_connections = []
		self.ico_connections  += make_connection('ico',self.ico_data,Rule_ico)
		self.octa_connections += make_connection('octa_111',self.octa_data,Rule_octa_111)
		self.octa_connections += make_connection('octa_fcc',self.octa_data,Rule_octa_fcc)
		self.deca_connections += make_connection('reent',self.deca_data,Rule_deca_reent)
		self.deca_connections += make_connection('plane',self.deca_data,Rule_deca_plane)
		self.deca_connections += make_connection('deca_111',self.deca_data,Rule_deca_111)

		self.print_connections()
		self.make_interpolation_plot()
		self.get_intersections()
		print('Finished Annas Interpolation Scheme.')
		print('------------------------------------------------------------')

	# This method will ... 
	def print_cluster(self,data,magic=False):
		print('----------------------------------')
		to_print = ''
		if magic == True:
			to_print += 'Magic '
		to_print += data[0].motif + ' Data'
		print(to_print)
		print('no atoms\tMotif Dets\tdelta energy (eV)')
		for cluster in data:
			print(str(cluster.no_atoms) +'\t\t'+ str(cluster.motif_details) +'\t\t'+ str(cluster.delta_energy))
		print('----------------------------------')

	def output_to_file(self):
		with open(self.delta_energy_results_file,'w') as file:
			file.write('Element: '+str(self.element)+' Max_Size: '+str(self.maximum_size)+'\n')
			file.write('------------------------------\n')
			file.write('Icosahedron\n')
			for ico_datum in self.ico_data:
				file.write(str(ico_datum.no_atoms)+'\t'+str(ico_datum.motif_details[0])+'\t'+str(ico_datum.delta_energy)+'\n')
			file.write('Octahedron\n')
			for octa_datum in self.octa_data:
				l = str(octa_datum.motif_details[0]); c = str(octa_datum.motif_details[1])
				file.write(str(octa_datum.no_atoms)+'\t'+l+'\t'+c+'\t'+str(octa_datum.delta_energy)+'\n')
			file.write('Decahedron\n')
			for deca_datum in self.deca_data:
				p = str(deca_datum.motif_details[0]); q = str(deca_datum.motif_details[1]); r = str(deca_datum.motif_details[2])
				file.write(str(deca_datum.no_atoms)+'\t'+p+'\t'+q+'\t'+r+'\t'+str(deca_datum.delta_energy)+'\n')
			
	def print_connections(self):
		print('-------------------------------------------------------')
		print('Number of Ico connections: ' + str(len(self.ico_connections)))
		for ico_connection in self.ico_connections:
			print(ico_connection)
		print('-------------------------------------------------------')
		print('Number of Deca connections: ' + str(len(self.deca_connections)))
		for deca_connection in self.deca_connections:
			print(deca_connection)
		print('-------------------------------------------------------')
		print('Number of Octa connections: ' + str(len(self.octa_connections)))
		for octa_connection in self.octa_connections:
			print(octa_connection)
		print('-------------------------------------------------------')

	def make_interpolation_plot(self):
		print('Making interaction plots.')
		a4_dims = (11.7, 8.27)
		fig1 = plt.figure(figsize=a4_dims)
		ax1 = fig1.add_subplot(111)
		def make_plot(ax,data,color,point_type,label):
			no_atoms = []
			delta_energies = []
			for datum in data:
				no_atoms.append(datum.no_atoms)
				delta_energies.append(datum.delta_energy)
			ax.plot(no_atoms, delta_energies, point_type, color=color,label='_nolegend_')
			
		def make_lines(ax,connection_data,color,point_type,label):
			for connection in connection_data:
				no_atoms = [connection.cluster_start.no_atoms,connection.cluster_end.no_atoms]
				delta_energies = [connection.cluster_start.delta_energy,connection.cluster_end.delta_energy]
				if connection.type_of_connection in ['reent', 'plane', 'octa_fcc', 'ico']:
					line_type = '-'
				elif connection.type_of_connection in ['deca_111','octa_111']:
					line_type = '-.'
				else:
					print('error')
					import pdb; pdb.set_trace()
					exit()
				ax.plot(no_atoms, delta_energies, point_type + line_type, color=color,label='_nolegend_')

		make_lines(ax1,self.ico_connections,'black','o','Icosahedron')
		make_plot(ax1,self.ico_data,'black','s','Icosahedron')

		make_lines(ax1,self.deca_connections,'red','o','Icosahedron')
		make_plot(ax1,self.deca_data,'red','o','Decahedron')
		make_plot(ax1,self.deca_magic,'red','s','Magic Decahedron')

		make_lines(ax1,self.octa_connections,'blue','o','Icosahedron')
		make_plot(ax1,self.octa_data,'blue','o','Octahedron')
		make_plot(ax1,self.octa_magic,'blue','s','Magic Octahedron')

		custom_lines = [Line2D([0], [0], color='black', lw=1),
		                Line2D([0], [0], color='red', lw=1),
		                Line2D([0], [0], color='red', lw=1, linestyle='-.'),
		                Line2D([0], [0], color='blue', lw=1),
		                Line2D([0], [0], color='blue', lw=1, linestyle='-.')]
		custom_names = ['Icosahedron','Decahedron Rule 1','Decahedron Rule 2','Octahedron Rule 1','Octahedron Rule 2']
		ax1.set_xlabel('No of Atoms in Cluster')
		ax1.set_ylabel(r'$\Delta$ (eV)')
		ax1.set_xlim(left=self.lowerNoAtomRange,right=self.higherNoAtomRange)
		ax1.set_ylim(bottom=self.lowerDERange,top=self.higherDERange)
		plt.legend(custom_lines,custom_names,loc='best',fancybox=True,framealpha=1, shadow=True, borderpad=1)
		plt.savefig(self.filename_prefix + '_Interpolation_Scheme.png')
		plt.savefig(self.filename_prefix + '_Interpolation_Scheme.svg')

		for size_to_interpolate in self.sizes_to_interpolate:
			ax1.axvline(x=size_to_interpolate,ymin=0,ymax=1, color='green', lw=1, linestyle='-')
		if len(self.sizes_to_interpolate) > 0:
			custom_lines.append(Line2D([0], [0], color='green', lw=1, linestyle='-'))
			custom_names.append('Interpolation Line')
		plt.savefig(self.filename_prefix + '_Interpolation_Scheme_with_lines.png')
		plt.savefig(self.filename_prefix + '_Interpolation_Scheme_with_lines.svg')
		#plt.show()

	def get_intersections(self):
		print('Making interaction analysis files.')
		for size_to_interpolate in self.sizes_to_interpolate:
			def get_and_write_exact_clusters(Interpolation_details,motif_data,motif):
				exact_clusters = []
				for cluster in motif_data:
					if cluster.no_atoms == size_to_interpolate:
						exact_clusters.append(cluster)
				if not len(exact_clusters) == 0:
					self.Interpolation_details.write('------------------\n')
					Interpolation_details.write('The ' + motif + ' motif has a cluster(s) with the exact number of atoms.\n')
					for exact_cluster in exact_clusters:
						Interpolation_details.write(exact_cluster.__str__())

			def get_intersections_of_a_motif(motif_connections):
				relavant_connections = []
				for connection in motif_connections:
					if connection.cluster_end.no_atoms < size_to_interpolate and size_to_interpolate < connection.cluster_start.no_atoms:
						relavant_connections.append(connection)
				relavant_connections.sort(key = lambda x: x.energy)
				return relavant_connections
			relavant_ico_connections  = get_intersections_of_a_motif(self.ico_connections)
			relavant_deca_connections = get_intersections_of_a_motif(self.deca_connections)
			relavant_octa_connections = get_intersections_of_a_motif(self.octa_connections)

			def write_connection_details(relavant_connections, motif):
				string_to_return = ''
				for relavant_connection in relavant_connections:
					string_to_return += relavant_connection.__str__() + '\n'
					start_details = relavant_connection.cluster_start.motif_details
					atom_diff = relavant_connection.cluster_start.no_atoms - size_to_interpolate
					string_to_return += 'Number of atoms to remove from ' + motif + ' ' + str(start_details) + ': ' + str(atom_diff) + '\n'
				return string_to_return

			self.Interpolation_details = open(self.filename_prefix+'_Clusters_interpolated_at_size_'+str(size_to_interpolate)+'.txt','w')
			self.Interpolation_details.write('------------------------------------\n')
			self.Interpolation_details.write('------------------------------------\n')
			self.Interpolation_details.write('Icosahedral Interpolation\n')
			self.Interpolation_details.write(write_connection_details(relavant_ico_connections,'ico'))
			get_and_write_exact_clusters(self.Interpolation_details,self.ico_data,'ico')
			self.Interpolation_details.write('------------------------------------\n')
			self.Interpolation_details.write('------------------------------------\n')
			self.Interpolation_details.write('Decahedral Interpolation\n')
			self.Interpolation_details.write(write_connection_details(relavant_deca_connections,'deca'))
			get_and_write_exact_clusters(self.Interpolation_details,self.deca_data,'deca')
			self.Interpolation_details.write('------------------------------------\n')
			self.Interpolation_details.write('------------------------------------\n')
			self.Interpolation_details.write('Octahedral Interpolation\n')
			self.Interpolation_details.write(write_connection_details(relavant_octa_connections,'octa'))
			get_and_write_exact_clusters(self.Interpolation_details,self.octa_data,'octa')
			self.Interpolation_details.write('------------------------------------\n')
			self.Interpolation_details.write('------------------------------------\n')
			self.Interpolation_details.close()