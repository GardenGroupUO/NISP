from sys import exit
# This section of he code is responsible for creating the connections between clusters

# This method will create all the conenctions between clusters.
def make_connection(name,data,Rule):
	connections = []
	for index1 in range(0,len(data)):
		for index2 in range(index1+1,len(data)):
			cluster1_details = data[index1].motif_details
			cluster2_details = data[index2].motif_details
			if Rule(cluster1_details,cluster2_details) or Rule(cluster2_details,cluster1_details):
				connection = Interpolation_Connection(data[index1],data[index2],name)
				connections.append(connection)
	return connections

# This class contains all the information needed to record all the connections between clusters in the interpolatino scheme.
class Interpolation_Connection:
	def __init__(self,cluster1,cluster2,type_of_connection):
		#import pdb; pdb.set_trace()
		if not cluster1.motif == cluster2.motif:
			print('Error: Cluster1 and Cluster2 are the same motif (???).')
			import pdb; pdb.set_trace()
			exit()
		self.motif = cluster1.motif
		if cluster2.no_atoms > cluster1.no_atoms:
			self.cluster_start = cluster2
			self.cluster_end = cluster1
		elif cluster1.no_atoms > cluster2.no_atoms:
			self.cluster_start = cluster1
			self.cluster_end = cluster2
		else:
			print('Error: Cluster1 and Cluster2 are the same size (???).')
			import pdb; pdb.set_trace()
			exit()
		self.type_of_connection = type_of_connection
		self.energy = (cluster1.delta_energy + cluster2.delta_energy)/2.0

	def __str__(self):
		if self.type_of_connection in ['reent', 'plane']:
			#line_type = 'Solid'
			removal_method = '100 Facet or from Corners'
		elif self.type_of_connection in ['deca_111','octa_111']:
			#line_type = 'Dashed'
			removal_method = '111 Facet'
		elif self.type_of_connection in ['octa_fcc']:
			removal_method = '100 Facet'
		elif self.type_of_connection in ['ico']:
			removal_method = '111 Facet'
		else:
			print('error')
			import pdb; pdb.set_trace()
			exit()
		#cluster_string = '-------------------------------------\n'
		cluster_string =  'motif: ' + str(self.cluster_start.motif) + ', '
		cluster_string += 'type_of_connection: ' + str(self.type_of_connection) + ', '
		cluster_string += 'Remove atoms from: ' + str(removal_method) + ', '
		cluster_string += 'motif start details: ' + str(self.cluster_start.motif_details) + ', '
		cluster_string += 'motif end details: ' + str(self.cluster_end.motif_details) + ', '
		cluster_string += 'interpolation energy: ' + str(self.energy) + '.'
		#cluster_string += '-------------------------------------\n'
		return cluster_string