from NISP import Run_Interpolation_Scheme

input_information = {}
input_information['Element Type'] = 'Au'
input_information['Cohesive Energy'] = -3.82819360826 #-3.82819360826
input_information['Maximum No. of Atoms'] = 400
input_information['Local Optimiser'] = 'VASP'

slurm_information = {}
slurm_information['project'] = 'uoo00084'
slurm_information['time'] = '72:00:00'
slurm_information['nodes'] = 1
slurm_information['ntasks_per_node'] = 16
slurm_information['mem-per-cpu'] = '4G'
slurm_information['partition'] = 'large'
slurm_information['email'] = 'geoffreywealslurmnotifications@gmail.com'
slurm_information['vasp_version'] = 'VASP/5.4.4-intel-2017a'
slurm_information['vasp_execution'] = 'vasp_std'

input_information['Slurm Information'] = slurm_information

output_information = {}
output_information['Plot upper No of atom limit']   = None
output_information['Plot lower No of atom limit']   = None
output_information['Plot upper delta energy limit'] = None
output_information['Plot lower delta energy limit'] = None
output_information['Sizes to obtain instructions to create clusters for'] = [37,38,44,55,147,40]

no_of_cpus = 1
filename_prefix = ''

Run_Interpolation_Scheme(input_information=input_information,output_information=output_information,no_of_cpus=no_of_cpus,filename_prefix=filename_prefix)
