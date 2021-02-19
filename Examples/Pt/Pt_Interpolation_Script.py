from NanoIS import Run_Interpolation_Scheme 
from RunMinimisation_Pt import Minimisation_Function

input_information = {}
input_information['Element Type'] = 'Pt'
input_information['Cohesive Energy'] = -5.89233884824
input_information['Maximum No. of Atoms'] = 1000
input_information['Local Optimiser'] = Minimisation_Function

sizes_to_interpolate = [37,400]#[37,38,44,55,147,40,888,1399]

plot_information = {}
plot_information['Upper No of Atom Range']   = 450
plot_information['Lower No of Atom Range']   = 350
plot_information['Upper Delta Energy Range'] = None #2.8
plot_information['Lower Delta Energy Range'] = None #2.2

no_of_cpus = 1
filename = ''

Run_Interpolation_Scheme(input_information=input_information,sizes_to_interpolate=sizes_to_interpolate,plot_information=plot_information,no_of_cpus=no_of_cpus,filename=filename)
