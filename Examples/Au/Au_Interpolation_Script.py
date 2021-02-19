from NanoIS import Run_Interpolation_Scheme 
from RunMinimisation_Au import Minimisation_Function

input_information = {}
input_information['Element Type'] = 'Au'
input_information['Cohesive Energy'] = -3.82819360826 #-3.82819360826
input_information['Maximum No. of Atoms'] = 2000
input_information['Local Optimiser'] = Minimisation_Function

sizes_to_interpolate = [561,742,923]#[37,38,44,55,147,40,888,1399]

plot_information = {}
plot_information['Upper No of Atom Range']   = None
plot_information['Lower No of Atom Range']   = None
plot_information['Upper Delta Energy Range'] = None
plot_information['Lower Delta Energy Range'] = None

no_of_cpus = 4
filename = ''

Run_Interpolation_Scheme(input_information=input_information,sizes_to_interpolate=sizes_to_interpolate,plot_information=plot_information,no_of_cpus=no_of_cpus,filename=filename)
