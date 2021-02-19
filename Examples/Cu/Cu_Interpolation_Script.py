from NanoIS import Run_Interpolation_Scheme 
from RunMinimisation_Cu import Minimisation_Function

input_information = {}
input_information['Element Type'] = 'Cu'
input_information['Cohesive Energy'] = -3.55114216002
input_information['Maximum No. of Atoms'] = 1000
input_information['Local Optimiser'] = Minimisation_Function

sizes_to_interpolate = [37,78]

plot_information = {}
plot_information['Upper No of Atom Range']   = 2
plot_information['Lower No of Atom Range']   = 500
plot_information['Upper Delta Energy Range'] = 2.8
plot_information['Lower Delta Energy Range'] = 2.2

no_of_cpus = 1
filename = ''

Run_Interpolation_Scheme(input_information=input_information,sizes_to_interpolate=sizes_to_interpolate,plot_information=plot_information,no_of_cpus=no_of_cpus,filename=filename)
