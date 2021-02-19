#!/bin/bash -e
#SBATCH -J AIS_Au_Gupta
#SBATCH -A uoo00084         # Project Account

#SBATCH --partition=large
#SBATCH --time=12:00:00     # Walltime
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=8
#SBATCH --mem-per-cpu=500MB

#SBATCH --output=slurmjob_%A.out
#SBATCH --error=slurmjob_%A.err
#SBATCH --mail-user=geoffreywealslurmnotifications@gmail.com
#SBATCH --mail-type=ALL

#SBATCH --hint=nomultithread

######################
# Begin work section #
######################

module load Python/2.7.14-gimkl-2017a

python Au_Interpolation_Data.py
