from NanoIS import Run_Interpolation_Scheme 
from RunMinimisation_Cu import Minimisation_Function

input_information = {}
input_information['Element Type'] = 'Cu'
input_information['Cohesive Energy'] = -3.55114216002
input_information['Maximum No. of Atoms'] = 1000
input_information['Local Optimiser'] = Minimisation_Function

output_information = {}
output_information['Upper No of Atom Range']   = 2
output_information['Lower No of Atom Range']   = 500
output_information['Upper Delta Energy Range'] = 2.8
output_information['Lower Delta Energy Range'] = 2.2
output_information['Size to Interpolate Over'] = [37,78]
output_information['Filename Prefix'] = ''

no_of_cpus = 1

Run_Interpolation_Scheme(input_information=input_information,output_information=output_information,no_of_cpus=no_of_cpus)
