'''
Geoffrey Weal, Create_submitSL_slurm_Main.py, 10/02/2021

This program is designed to create the various forms of submit.sl/mass_submit.sl files that could be used to submit genetic algorithm trials to slurm.
'''

def make_submitSL(local_path,project,time,nodes,ntasks_per_node,mem_per_cpu,partition='large',email='',vasp_version='VASP/5.4.4-intel-2017a',vasp_execution='vasp_std'):
    # create name for job
    print("creating submit.sl for "+str(local_path))
    name = 'Getting_Lattice_Constant_Data_'+local_path.replace('/','_')
    # writing the submit.sl script
    with open(local_path+"/submit.sl", "w") as submitSL:
        submitSL.write('#!/bin/bash -e\n')
        submitSL.write('#SBATCH -J ' + str(name) + '\n')
        submitSL.write('#SBATCH -A ' + str(project) + '         # Project Account\n')
        submitSL.write('#SBATCH --partition ' + str(partition) + '\n')
        submitSL.write('\n')
        submitSL.write('#SBATCH --time=' + str(time) + '     # Walltime\n')
        submitSL.write('#SBATCH --nodes=' + str(nodes) + '\n')
        submitSL.write('#On VASP, Ben Roberts recommends using the same number\n')
        submitSL.write('#of tasks on all nodes, even if this makes scheduling\n')
        submitSL.write('#a little more difficult\n')
        submitSL.write('#SBATCH --ntasks-per-node=' + str(ntasks_per_node) + '\n')
        submitSL.write('#SBATCH --mem-per-cpu=' + str(mem_per_cpu) + '\n')
        #submitSL.write('#SBATCH -C sb\n')
        submitSL.write('\n')
        #submitSL.write("#SBATCH --hint=nomultithread    # don't use hyperthreading"+'\n')
        submitSL.write('#SBATCH --output=slurm-%j.out      # %x and %j are replaced by job name and ID'+'\n')
        submitSL.write('#SBATCH --error=slurm-%j.err'+'\n')
        if not email == '':
            submitSL.write('#SBATCH --mail-user=' + str(email) + '\n')
            submitSL.write('#SBATCH --mail-type=ALL\n')
        submitSL.write('#SBATCH --hint nomultithread\n')
        submitSL.write('\n')
        submitSL.write('module load '+str(vasp_version)+'\n')
        submitSL.write('srun -K '+str(vasp_execution)+'\n')
