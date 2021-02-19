from NISP import Run_Interpolation_Scheme 
from RunMinimisation_Pt import Minimisation_Function

input_information = {}
input_information['Element Type'] = 'Pt'
input_information['Cohesive Energy'] = -5.89233884824
input_information['Maximum No. of Atoms'] = 1000
input_information['Local Optimiser'] = Minimisation_Function
input_information['Manual Mode'] = 'VASP'

output_information = {}
output_information['Upper No of Atom Range']   = 450
output_information['Lower No of Atom Range']   = 350
output_information['Upper Delta Energy Range'] = None #2.8
output_information['Lower Delta Energy Range'] = None #2.2
output_information['Size to Interpolate Over'] = [37,400]#[37,38,44,55,147,40,888,1399]

no_of_cpus = 1
filename_prefix = ''

Run_Interpolation_Scheme(input_information=input_information,output_information=output_information,no_of_cpus=no_of_cpus,filename_prefix=filename_prefix)
