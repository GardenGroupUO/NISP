from NISP import Run_Interpolation_Scheme

input_information = {}
input_information['Element Type'] = 'Au'
input_information['Cohesive Energy'] = -3.82819360826 #-3.82819360826
input_information['Maximum No. of Atoms'] = 2000
input_information['Local Optimiser'] = 'Manual Mode'

output_information = {}
output_information['Plot upper No of atom limit']   = None
output_information['Plot lower No of atom limit']   = None
output_information['Plot upper delta energy limit'] = None
output_information['Plot lower delta energy limit'] = None
output_information['Sizes to obtain instructions to create clusters for'] = [561,742,923]#[37,38,44,55,147,40,888,1399]

no_of_cpus = 1
filename_prefix = ''

Run_Interpolation_Scheme(input_information=input_information,output_information=output_information,no_of_cpus=no_of_cpus,filename_prefix=filename_prefix)
