'''
RunMinimisation.py, GRW, 8/6/17
 
'''
import sys, time
from asap3.Internal.BuiltinPotentials import Gupta
from ase.optimize import BFGS, FIRE

def Minimisation_Function(cluster):
	####################################################################################################################
	cluster.pbc = False
	####################################################################################################################
	# Perform the local optimisation method on the cluster.
	# Parameter sequence: [p, q, a, xi, r0]
	Pt_parameters = {'Pt': [10.71, 3.845, 0.27443, 2.6209, 2.77]}
	Gupta_parameters = Pt_parameters
	cutoff = 1000
	calculator = Gupta(Gupta_parameters, cutoff=cutoff, debug=False)
	cluster.set_calculator(calculator)
	dyn = FIRE(cluster,logfile=None)
	startTime = time.time(); converged = False
	try:
		dyn.run(fmax=0.01,steps=5000)
		converged = dyn.converged()
		if not converged:
			errorMessage = 'The optimisation of cluster ' + str(cluster_name) + ' did not optimise completely.'
			print(errorMessage, file=sys.stderr)
			print(errorMessage)
	except:
		print('Local Optimiser Failed for some reason.')
	endTime = time.time()
	return cluster
