'''
RunMinimisation.py, GRW, 8/6/17
 
This script is designed to locally optimise clusters.
'''
import time
from ase.io import write
from subprocess import Popen

def Minimisation_Function(cluster):
	cluster.pbc = What_you_want # make sure that the periodic boundry conditions are set off
	# -----------------------------------------------------
	# Perform any pre-optimisation work here
	# -----------------------------------------------------
	startTime = time.time(); converged = False
	try:
		Popen(['run','external','program'])
	except Exception as exception_message:
		cluster_name = 'issue_cluster.xyz'
		errorMessage = 'The optimisation of cluster ' + str(original_cluster) + ' did not optimise completely.\n'
		errorMessage += 'The cluster of issue before optimisation has been saved as: '+str(cluster_name)+'\n'
		errorMessage += exception_message
		write(cluster_name,original_cluster)
		raise Exception(errorMessage)
	endTime = time.time()
	# -----------------------------------------------------
	# Perform any post-optimisation work here
	# -----------------------------------------------------
	return cluster
