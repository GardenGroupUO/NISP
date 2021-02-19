from NanoIS import Run_Interpolation_Scheme 
from RunMinimisation_Au import Minimisation_Function

input_information = {}
input_information['Element Type'] = 'Au'
input_information['Cohesive Energy'] = -3.82819360826 #-3.82819360826
input_information['Maximum No. of Atoms'] = 2000
input_information['Local Optimiser'] = Minimisation_Function

output_information = {}
output_information['Upper No of Atom Range']   = None
output_information['Lower No of Atom Range']   = None
output_information['Upper Delta Energy Range'] = None
output_information['Lower Delta Energy Range'] = None
output_information['Size to Interpolate Over'] = [561,742,923]#[37,38,44,55,147,40,888,1399]
output_information['Filename Prefix'] = ''

no_of_cpus = 4

Run_Interpolation_Scheme(input_information=input_information,output_information=output_information,no_of_cpus=no_of_cpus)
