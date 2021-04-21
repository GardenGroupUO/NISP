import sys
if sys.version_info[0] == 2:
	raise ImportError('The Nanocluster Interpolation Scheme requires Python3. This is Python2.')

__name__    = 'The Nanocluster Interpolation Scheme (NISP)'
__version__ = '1.3.4'
__author__  = "Geoffrey R. Weal, Dr. Anna L. Garden, Dr. Andreas Pedersen and Prof. Hannes Jo'nsson"

__author_email__ = 'anna.garden@otago.ac.nz'
__license__ = 'GNU AFFERO GENERAL PUBLIC LICENSE'
__url__ = 'https://github.com/GardenGroupUO/NISP'
__doc__ = 'See https://nisp.readthedocs.io/en/latest/ for the documentation on this program'

from NISP.NISP.Run_Interpolation_Scheme import Run_Interpolation_Scheme 
__all__ = ['Run_Interpolation_Scheme']
