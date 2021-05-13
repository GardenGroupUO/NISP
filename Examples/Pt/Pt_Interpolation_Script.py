from NISP import Run_Interpolation_Scheme 
from RunMinimisation_Pt import Minimisation_Function

input_information = {}
input_information['Element Type'] = 'Pt'
input_information['Cohesive Energy'] = -5.89233884824
input_information['Maximum No. of Atoms'] = 1000
input_information['Local Optimiser'] = Minimisation_Function

output_information = {}
output_information['Plot upper No of atom limit']   = 450
output_information['Plot lower No of atom limit']   = 350
output_information['Plot upper delta energy limit'] = None
output_information['Plot lower delta energy limit'] = None
output_information['Sizes to obtain instructions to create clusters for'] = [37,400]

no_of_cpus = 1
filename_prefix = ''

Run_Interpolation_Scheme(input_information=input_information,output_information=output_information,no_of_cpus=no_of_cpus,filename_prefix=filename_prefix)
