######################################################################################################
######################################################################################################
######################################################################################################
# These are all the rules that connect clusters together.
######################################################################################################
# This method will add the entries of two lists together.
def sum_of_lists(list1,list2):
	return [x + y for x, y in zip(list1, list2)]
###################################################
# Decahedron rules
###################################################
# 
def Rule_deca_reent(cluster1_details,cluster2_details):
	return cluster1_details == sum_of_lists(cluster2_details,[-2,0,1])
#
def Rule_deca_plane(cluster1_details,cluster2_details):
	p1 = cluster1_details[0]; q1 = cluster1_details[1]; r1 = cluster1_details[2]
	p2 = cluster2_details[0]; q2 = cluster2_details[1]; r2 = cluster2_details[2]
	test1 = p1 == p2-1 and q1 == q2 + 1 and r1 == 0 and r2 == 0
	test2 = cluster1_details == sum_of_lists(cluster2_details,[1,1,-1])
	return test1 or test2
#
def Rule_deca_111(cluster1_details,cluster2_details):
	return cluster1_details == sum_of_lists(cluster2_details,[0,-2,0])
###################################################
# Octahedron rules
###################################################
#
def Rule_octa_111(cluster1_details,cluster2_details):
	length1 = cluster1_details[0]; cutoff1 = cluster1_details[1]
	length2 = cluster2_details[0]; cutoff2 = cluster2_details[1]
	test1 = length1 == length2-1 and cutoff1 == 0 and cutoff2 == 0
	test2 = length1 == length2-2 and cutoff1 == 0 and cutoff2 == 1
	test3 = length1 == length2-2 and cutoff1 == cutoff2-2 and cutoff2 > 1
	return test1 or test2 or test3
#
def Rule_octa_fcc(cluster1_details,cluster2_details):
	return cluster1_details == sum_of_lists(cluster2_details,[0,-1])
###################################################
# Icosahedron rules
###################################################
#
def Rule_ico(cluster1_details,cluster2_details):
	return cluster1_details == sum_of_lists(cluster2_details,[1])
######################################################################################################
######################################################################################################
######################################################################################################

def sort_data_by_noAtoms(data):
	sorted_data_by_noAtoms = sorted(data,key=lambda x:len(x.cluster))
	#sorted_data_by_noAtoms = sorted(data,key=lambda x: x.no_atoms)
	return sorted_data_by_noAtoms


