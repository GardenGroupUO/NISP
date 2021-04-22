from NISP.NISP.Cluster import Cluster

def get_interpolation_data_from_ase_from_file(input_file,manual_mode_file_found):
	gidf_ASE_ff = Get_Interpolation_Data_From_ASE_From_File()
	gidf_ASE_ff.input_from_file(input_file,manual_mode_file_found)
	ico_data, magic_numbers, deca_data, deca_magic, octa_data, octa_magic, element, maximum_size = gidf_ASE_ff.get_information()
	return ico_data, magic_numbers, deca_data, deca_magic, octa_data, octa_magic, element, maximum_size

class Get_Interpolation_Data_From_ASE_From_File:
	def __init__(self):
		pass

	def get_information(self):
		return self.ico_data, self.magic_numbers, self.deca_data, self.deca_magic, self.octa_data, self.octa_magic, self.element, self.maximum_size

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
							tostring += 'Some of the other entries in you "'+str(input_file)+'" file may also be missing. Check your "'+str(input_file)+'" completely and then run NISP again.'
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