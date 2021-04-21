'''
RunMinimisation.py, GRW, 8/6/17
 
This script is designed to locally optimise clusters.
'''
#import time
from asap3.Internal.BuiltinPotentials import Gupta
from ase.optimize import FIRE
from ase.io import write

def Minimisation_Function(cluster):
	cluster.pbc = False
	# Perform the local optimisation method on the cluster.
	# Parameter sequence: [p, q, a, xi, r0]
	Pt_parameters = {'Pt': [10.71, 3.845, 0.27443, 2.6209, 2.77]}
	Gupta_parameters = Pt_parameters
	cutoff = 1000
	calculator = Gupta(Gupta_parameters, cutoff=cutoff, debug=False)
	cluster.set_calculator(calculator)
	original_cluster = cluster.copy()
	dyn = FIRE(cluster,logfile=None)
	#startTime = time.time(); 
	converged = False
	try:
		dyn.run(fmax=0.01,steps=5000)
		converged = dyn.converged()
		if not converged:
			cluster_name = 'issue_cluster.xyz'
			errorMessage = 'The optimisation of cluster ' + str(original_cluster) + ' did not optimise completely.\n'
			errorMessage += 'The cluster of issue before optimisation has been saved as: '+str(cluster_name)
			write(cluster_name,original_cluster)
			raise Exception(errorMessage)
	except Exception as exception_message:
		cluster_name = 'issue_cluster.xyz'
		errorMessage = 'The optimisation of cluster ' + str(original_cluster) + ' did not optimise completely.\n'
		errorMessage += 'The cluster of issue before optimisation has been saved as: '+str(cluster_name)+'\n'
		errorMessage += exception_message
		write(cluster_name,original_cluster)
		raise Exception(errorMessage)
	#endTime = time.time()
	return cluster
