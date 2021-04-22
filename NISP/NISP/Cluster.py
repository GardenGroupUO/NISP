from sys import exit
from NISP.NISP.Manual_Mode import get_diameter

def get_cluster(task):
	motif, motif_details, element, local_optimiser, e_coh, no_atoms, no_of_tasks, counter = task
	print('Starting '+str([motif, motif_details, element]))
	cluster = Cluster(motif,motif_details,element=element,local_optimiser=local_optimiser,e_coh=e_coh,no_atoms=None,delta_energy=None,debug=False,get_energy=True)
	if not no_atoms == len(cluster):
		print('Error in Get_Energies_Of_Decahedrals')
		print('no_atoms and len(cluster) are not the same')
		print('This likely means that something is wrong in the way atoms are counted in def no_of_atoms_to_make_deca')
		print('no_atoms = '+str(no_atoms))
		print('len(cluster) = '+str(len(cluster)))
		print('check this.')
		import pdb; pdb.set_trace()
		print('This program will exit without completing')
		raise Exception()
	print('Finished '+str([motif, motif_details, element]))
	counter.value += 1
	print('Finished '+str(counter.value)+'/'+str(no_of_tasks)+' tasks')
	return cluster

def get_Delta_Energy(energy,cluster,e_coh):
	"""
	Get Delta Energy
	"""
	delta_energy = (energy - len(cluster)*e_coh)/(len(cluster)**(2.0/3.0))
	return delta_energy

class Cluster:
	"""
	This class is designed to hold all the information we need to record about clusters:
	Inputs
	(str) motif - the motif you want to get the number of atoms required to create it.
	(list) motif_details - the information required for the motif of interest
	(atoms) cluster - A cluster to sample
	(int) no_atoms - the number of atoms in the cluster
	(Calculator) calculator - The calculator to use 
	(float) e_coh - The cohesive energy of the cluster
	(float) delta_energy - The delta energy of the cluster.
	(boolean) debug - Print any information to help us if we need to.
	Output
	(int) noAtoms - the number of atoms required to make the cluster of interest
	"""
	def __init__(self,motif,motif_details,element=None,local_optimiser=None,e_coh=None,no_atoms=None,delta_energy=None,debug=False,get_energy=False):
		if debug:
			print('cluster: '+str(cluster))
			print('no_atoms: '+str(no_atoms))
			print('local_optimiser: '+str(local_optimiser))
			print('e_coh: '+str(e_coh))
			print('delta_energy: '+str(delta_energy))
		self.motif = motif
		self.motif_details = motif_details
		self.get_energy = get_energy
		# Calculate the delta energy of the clusters
		if not (element is None and local_optimiser is None and e_coh is None) and (no_atoms is None and delta_energy is None):
			if motif == 'Icosahedron':
				if isinstance(motif_details,list):
					noshells = motif_details[0]
				else:
					noshells = motif_details
				from ase.cluster.icosahedron import Icosahedron
				cluster = Icosahedron(element,noshells=noshells)
			elif motif == 'Octahedron':
				length = motif_details[0]; cutoff = motif_details[1]
				from ase.cluster.octahedron import Octahedron
				cluster = Octahedron(element,length=length,cutoff=cutoff)
			elif motif == 'Decahedron':
				p = motif_details[0]; q = motif_details[1]; r = motif_details[2]
				from ase.cluster.decahedron import Decahedron
				cluster = Decahedron(element,p=p,q=q,r=r)
			else:
				print('Error in Get_Interpolation_Data.py, in class Cluster, in def __init__')
				print('No valid motif type has been entered, must be either Icosahedron, Octahedron, Decahedron.')
				print('Check this.')
				print('motif = ' + str(motif))
				import pdb; pdb.set_trace()
				exit()
			self.post_creating_cluster(cluster)
			self.no_atoms = len(cluster)
			cluster = local_optimiser(cluster)
			if self.get_energy:
				energy = cluster.get_potential_energy()
				self.delta_energy = get_Delta_Energy(energy,cluster,e_coh)
		elif (element is None and local_optimiser is None and e_coh is None) and not (no_atoms is None and delta_energy is None):
			self.no_atoms = no_atoms
			self.delta_energy = delta_energy
		else:
			print('Error in Get_Interpolation_Data.py, in class Cluster, in def __init__')
			print('Error in Cluster')
			print('motif: '+str(motif))
			print('motif_details: '+str(motif_details))
			print('element: '+str(element))
			print('local_optimiser: '+str(local_optimiser))
			print('e_coh: '+str(e_coh))
			print('no_atoms: '+str(no_atoms))
			print('delta_energy: '+str(delta_energy))
			exit()

	def __str__(self):
		cluster_string = ''
		cluster_string += 'No. Atoms: ' + str(self.no_atoms) + '.\n'
		cluster_string += 'Motif Type: ' + str(self.motif) + '.\n'
		cluster_string += 'Motif details: ' + str(self.motif_details) + '.\n'
		if self.get_energy:
			cluster_string += 'Delta Energy (eV): ' + str(self.delta_energy) + '.\n'
		return cluster_string

	def __repr__(self):
		cluster_representation = '{'+str(self.no_atoms)+' '+str(self.motif)+': '+str(self.motif_details)
		if self.get_energy:
			cluster_representation += ' ('+str(self.delta_energy)+' eV)}'
		else:
			cluster_representation += '}'
		return cluster_representation

	def __len__(self):
		return self.no_atoms

	def post_creating_cluster(self,cluster):
		#diameter_of_cluster = get_diameter(cluster)
		#cluster.center(vacuum=diameter_of_cluster)
		self.make_cell(cluster)
		cluster.center(vacuum=10)
		cluster.set_pbc(False)

	def make_cell(self,cluster):
			cluster_cell = cluster.get_cell()
			for index in range(len(cluster_cell)):
				if cluster_cell[index][index] == 0:
					cluster_cell[index][index] = 1
			cluster.set_cell(cluster_cell)