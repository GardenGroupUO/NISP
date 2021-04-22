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
print('Loading the interpolation rules')
from NISP.NISP.Interpolation_rules import Rule_deca_reent, Rule_deca_plane, Rule_deca_111
from NISP.NISP.Interpolation_rules import Rule_octa_111, Rule_octa_fcc
from NISP.NISP.Interpolation_rules import Rule_ico
print('Loading Connection modules')
from NISP.NISP.Interpolation_Connection import make_connection
print('Loading os, timing, and multiprocessing modules')

import os, time
from sys import exit
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
		self.check_local_optimiser_entry()
		self.no_of_cpus = no_of_cpus
		self.filename_prefix = filename_prefix
		if self.filename_prefix == '':
			self.filename_prefix = str(self.element) + '_Max_Size_' + str(self.maximum_size)
		input_file_suffix =   '_atoms_interpolation_scheme_input_file.txt'
		results_file_suffix = '_atoms_interpolation_scheme_results_file.txt'
		self.input_information_file    = self.filename_prefix + input_file_suffix
		self.delta_energy_results_file = self.filename_prefix + results_file_suffix

	def check_local_optimiser_entry(self):
		if isinstance(self.local_optimiser,str):
			self.local_optimiser = self.local_optimiser.lower()
			if self.local_optimiser == 'vasp':
				self.get_slurm_information()
			elif self.local_optimiser == 'manual mode':
				sort_manual_mode_by = 'sort manual mode by'
				if sort_manual_mode_by in self.local_optimiser:
					self.sort_manual_mode_by = self.local_optimiser[sort_manual_mode_by]
				else:
					self.sort_manual_mode_by = 'base details'

	def get_slurm_information(self):
		self.slurm_information = check_value('Slurm Information',self.input_information,None)
		if (self.slurm_information == None) or (not isinstance(self.slurm_information,dict)):
			print('=====================================================================')
			print('Error in the Slurm Information given')
			print()
			if self.slurm_information == None:
				print('You have not given an input for Slurm Information in the input_information dictionary.')
				print('You need to give a dictionary that gives the information required for the submit.sl files for running VASP calculations in slurm.')
			elif not isinstance(self.slurm_information,dict):
				print('The Slurm Information input needs to be a dictionary that includes all the information required to create the submit.sl files for running VASP calculations in slurm.')
				print('You have set the Slurm Information input as:'+str(self.slurm_information))
			print()
			print('See XXX for more information about what to put in for this dictionary.')
			print()
			print('This program will finish without completing')
			print('=====================================================================')
			exit()
		enteries_to_check = ['project','time','nodes','ntasks_per_node','mem-per-cpu']
		issues = []
		for entry_to_check in enteries_to_check:
			issues.append(not entry_to_check in self.slurm_information)
		if any(issues):
			print('=====================================================================')
			print('Error in the Slurm Information given')
			print()
			print('You need to include the following in your Slurm Information:')
			print()
			for index in range(len(enteries_to_check)):
				entry_to_check = enteries_to_check[index]
				issue = issues[index]
				print(entry_to_check+': '+str('You have this' if issue else 'You have not included this. You need to give this'))
			print()
			print('See XXX for more information about what to put in for this dictionary.')
			print()
			print('This program will finish without completing')
			print('=====================================================================')
			exit()
		inputs_to_check = (('partition', 'large'), ('email', ''), ('vasp_version', 'VASP/5.4.4-intel-2017a'), ('vasp_execution', 'vasp_std'))
		for input_to_check, default in inputs_to_check:
			if not input_to_check in self.slurm_information:
				self.slurm_information[input_to_check] = default

	# ------------------------------------------------------------------------------------------------------------------------------
	# The following defs are for obtaining the delta energies of all combinations of icosahedral, decahedral and octahedral clusters 

	def get_input_data(self):
		if self.local_optimiser == 'vasp':
			if os.path.exists(self.delta_energy_results_file):
				# If data has already been obtained, get data from file
				self.input_from_file(self.delta_energy_results_file,False)	
			elif 'VASP_Clusters' in os.listdir('.'):
				# Get all the information that is needed from processing all VASP calculations
				self.input_from_procesed_VASP_files()	
			else:
				# Write all the files that are needed to run VASP calculations on
				self.write_files_for_manual_or_vasp_entry('vasp',self.slurm_information)
		elif self.local_optimiser == 'manual mode':
			if os.path.exists(self.input_information_file):
				# If data has already been obtained, get data from file
				self.input_from_file(self.input_information_file,True)	
			else:
				# write all the files that are needed for a manual entry of data
				self.write_files_for_manual_or_vasp_entry('xyz',None)
		else:
			if os.path.exists(self.delta_energy_results_file):
				# If data has already been obtained, get data from file
				self.input_from_file(self.delta_energy_results_file,False)
			else:
				# Perform calculation with ASE based calculator
				self.input_with_calculator()

	def input_from_procesed_VASP_files(self):
		from NISP.NISP.input_from_procesed_VASP_files import input_from_procesed_VASP_files
		self.ico_data, self.magic_numbers, self.octa_data, self.octa_magic, self.deca_data, self.deca_magic = input_from_procesed_VASP_files(self.element,self.local_optimiser,self.e_coh,self.maximum_size)

	def write_files_for_manual_or_vasp_entry(self,writing_format,slurm_information):
		from NISP.NISP.Manual_Mode import write_files_for_manual_mode
		write_files_for_manual_mode(self.element,self.e_coh,self.maximum_size,writing_format,self.input_information_file,slurm_information=slurm_information,sort_manual_mode_by=self.sort_manual_mode_by)

	def input_with_calculator(self):
		from NISP.NISP.get_interpolation_data_from_ase_calculator import get_interpolation_data_from_ase_calculator
		self.ico_data, self.magic_numbers, self.octa_data, self.octa_magic, self.deca_data, self.deca_magic = get_interpolation_data_from_ase_calculator(self.element,self.local_optimiser,self.e_coh,self.maximum_size,self.no_of_cpus)

	def input_from_file(self,input_file,manual_mode_file_found):
		from NISP.NISP.get_interpolation_data_from_ase_from_file import get_interpolation_data_from_ase_from_file
		self.ico_data, self.magic_numbers, self.deca_data, self.deca_magic, self.octa_data, self.octa_magic, self.element, self.maximum_size = get_interpolation_data_from_ase_from_file(input_file,manual_mode_file_found)

	# ------------------------------------------------------------------------------------------------------------------------------
	# Set up all the inputs required to make plots and other data from the interpolation scheme

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
		if self.lowerNoAtomRange is None:
			self.lowerNoAtomRange = 0
		self.higherDERange     = check_value('Upper Delta Energy Range',self.output_information,None) 
		self.lowerDERange      = check_value('Lower Delta Energy Range',self.output_information,None) 
		# -----------------------------------------------------------------

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
		fontsize_label = 20
		ax1.set_xlabel('No. of Atoms (#)', fontsize=fontsize_label)
		ax1.set_ylabel(r'$\Delta$ ($eV$)', fontsize=fontsize_label)
		fontsize_ticks = 16
		ax1.tick_params(axis='both', which='major', labelsize=fontsize_ticks)
		ax1.set_xlim(left=self.lowerNoAtomRange,right=self.higherNoAtomRange)
		ax1.set_ylim(bottom=self.lowerDERange,top=self.higherDERange)
		plt.legend(custom_lines,custom_names,loc='best',fancybox=True,framealpha=1, shadow=True, borderpad=1)
		plt.tight_layout()
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