# The information about the NISP program

__name__    = 'The Nanocluster Interpolation Scheme (NISP)'
__version__ = '1.3.6'
__author__  = "Dr. Geoffrey R. Weal, Dr. Anna L. Garden, Dr. Andreas Pedersen and Prof. Hannes Jo'nsson"

import sys
if sys.version_info[0] == 2:
	toString = ''
	toString += '\n'
	toString += '================================================'+'\n'
	toString += 'This is the NISP Program'+'\n'
	toString += 'Version: '+str(__version__)+'\n'
	toString += '\n'
	toString += 'The NISP program requires Python3. You are attempting to execute this program in Python2.'+'\n'
	toString += 'Make sure you are running the NISP program in Python3 and try again'+'\n'
	toString += 'This program will exit before beginning'+'\n'
	toString += '================================================'+'\n'
	raise ImportError(toString)
if sys.version_info[1] < 4:
	toString = ''
	toString += '\n'
	toString += '================================================'+'\n'
	toString += 'This is the NISP Program'+'\n'
	toString += 'Version: '+str(__version__)+'\n'
	toString += '\n'
	toString += 'The NISP program requires Python 3.4 or greater.'+'\n'
	toString += 'You are using Python '+str('.'.join(sys.version_info))
	toString += '\n'
	toString += 'Use a version of Python 3 that is greater or equal to Python 3.4.\n'
	toString += 'This program will exit before beginning'+'\n'
	toString += '================================================'+'\n'
	raise ImportError(toString)

# ------------------------------------------------------------------------------------------------------------------------

# A check for ASE
import importlib
python_version = 3.4

ase_spec = importlib.util.find_spec("ase")
found = ase_spec is not None

if not found:
	toString = ''
	toString += '\n'
	toString += '================================================'+'\n'
	toString += 'This is the NISP Program'+'\n'
	toString += 'Version: '+str(__version__)+'\n'
	toString += '\n'
	toString += 'The NISP program requires ASE.'+'\n'
	toString += '\n'
	toString += 'Install ASE through pip by following the instruction in https://nisp.readthedocs.io/en/latest/Installation.html'+'\n'
	toString += 'These instructions will ask you to install ase by typing the following into your terminal\n'
	toString += 'pip3 install --user --upgrade ase\n'
	toString += '\n'
	toString += 'This program will exit before beginning'+'\n'
	toString += '================================================'+'\n'
	raise ImportError(toString)	

packaging_spec = importlib.util.find_spec("packaging")
found = packaging_spec is not None

if not found:
	toString = ''
	toString += '\n'
	toString += '================================================'+'\n'
	toString += 'This is the NISP Program'+'\n'
	toString += 'Version: '+str(__version__)+'\n'
	toString += '\n'
	toString += 'The NISP program requires the "packaging" program.'+'\n'
	toString += '\n'
	toString += 'Install packaging through pip by following the instruction in https://nisp.readthedocs.io/en/latest/Installation.html'+'\n'
	toString += 'These instructions will ask you to install packaging by typing the following into your terminal\n'
	toString += 'pip3 install --user --upgrade packaging\n'
	toString += '\n'
	toString += 'This program will exit before beginning'+'\n'
	toString += '================================================'+'\n'
	raise ImportError(toString)	

import ase
ase_version_minimum = '3.19.0'
from packaging import version
#from distutils.version import StrictVersion
#if StrictVersion(ase.__version__) < StrictVersion(ase_version_minimum):
if version.parse(ase.__version__) < version.parse(ase_version_minimum):
	toString = ''
	toString += '\n'
	toString += '================================================'+'\n'
	toString += 'This is the NISP Program'+'\n'
	toString += 'Version: '+str(__version__)+'\n'
	toString += '\n'
	toString += 'The NISP program requires ASE greater than or equal to '+str(ase_version_minimum)+'.'+'\n'
	toString += 'The current version of ASE you are using is '+str(ase.__version__)+'.'+'\n'
	toString += '\n'
	toString += 'Install ASE through pip by following the instruction in https://nisp.readthedocs.io/en/latest/Installation.html'+'\n'
	toString += 'These instructions will ask you to install ase by typing the following into your terminal\n'
	toString += 'pip3 install --user --upgrade ase\n'
	toString += '\n'
	toString += 'This program will exit before beginning'+'\n'
	toString += '================================================'+'\n'
	raise ImportError(toString)

# ------------------------------------------------------------------------------------------------------------------------

__author_email__ = 'anna.garden@otago.ac.nz'
__license__ = 'GNU AFFERO GENERAL PUBLIC LICENSE'
__url__ = 'https://github.com/GardenGroupUO/NISP'
__doc__ = 'See https://nisp.readthedocs.io/en/latest/ for the documentation on this program'

from NISP.NISP.Run_Interpolation_Scheme import Run_Interpolation_Scheme 
__all__ = ['Run_Interpolation_Scheme']

# ------------------------------------------------------------------------------------------------------------------------
