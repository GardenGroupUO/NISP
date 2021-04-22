# The Nanocluster Interpolation Scheme Program (NISP)

[![Citation](https://img.shields.io/badge/Citation-click%20here-green.svg)](https://doi.org/10.1039/C7NR09440J)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/NISP)](https://docs.python.org/3/)
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/GardenGroupUO/NISP)](https://github.com/GardenGroupUO/NISP)
[![PyPI](https://img.shields.io/pypi/v/NISP)](https://pypi.org/project/NISP/)
[![Conda](https://img.shields.io/conda/v/gardengroupuo/nisp)](https://anaconda.org/GardenGroupUO/nisp)
[![Documentation](https://img.shields.io/badge/Docs-click%20here-brightgreen)](https://nisp.readthedocs.io/en/latest/)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/GardenGroupUO/NISP/main?urlpath=lab)
[![Licence](https://img.shields.io/github/license/GardenGroupUO/NISP)](https://www.gnu.org/licenses/agpl-3.0.en.html)
[![LGTM Grade](https://img.shields.io/lgtm/grade/python/github/GardenGroupUO/NISP)](https://lgtm.com/projects/g/GardenGroupUO/NISP/context:python)

Authors: Dr. Anna L. Garden (University of Otago, Dunedin, New Zealand), Dr. Andreas Pedersen, and  Hannes Jónsson (University of Iceland, Reykjavík, Iceland)

Group pages: https://blogs.otago.ac.nz/annagarden/ , https://notendur.hi.is/hj/

Page to cite with work from: A. L. Garden, A. Pedersen, H. Jónsson, “Reassignment of ‘magic numbers’ of decahedral and FCC structural motifs”, Nanoscale, 10, 5124-5132 (2018), [DOI: 10.1039/C7NR09440J](https://doi.org/10.1039/C7NR09440J)

## What is NISP

The Nanocluster Interpolation Scheme Program (NISP) is designed to perform an interpolation scheme that can give an idea of icosahedral, decahedral, and octahedral clusters that can be formed with a given number of atoms. 

This scheme is based on the work by Garden *et al.* as described in "Reassignment of ‘magic numbers’ for Au clusters of decahedral and FCC structural motifs", A. L. Garden, A. Pedersen, H. Jónsson, “Reassignment of ‘magic numbers’ of decahedral and FCC structural motifs”, Nanoscale, 10, 5124-5132 (2018), [DOI: 10.1039/C7NR09440J](https://doi.org/10.1039/C7NR09440J)

See https://doi.org/10.1039/C7NR09440J for more information on this scheme.

## Try NISP before you Clone/Pip/Conda (on Binder/Jupter Notebooks)!

If you are new to NISP, it is recommended try it out by running NISP live on our interactive Jupyter+Binder page before you download it. On Jupyter+Binder, you can play around with NISP on the web. You do not need to install anything to try NISP out on Jupyter+Binder.

Click the Binder button below to try NISP out on the web! (The Binder page may load quickly or may take 1 or 2 minutes to load)

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/GardenGroupUO/NISP/main?urlpath=lab)

## Installation

It is recommended to read the installation page before using the NISP program. 

[nisp.readthedocs.io/en/latest/Installation.html](https://nisp.readthedocs.io/en/latest/Installation.html)

Note that you can install NISP through ``pip3`` and ``conda``. See the [installation instructions](https://nisp.readthedocs.io/en/latest/Installation.html) on how to do this. 

## Output files that are created by NISP

Examples of the plots that are created are shown below. The first of these is the interpolation scheme plot, which shows all the estimated energies of nanoclusters across the size range of nanoclusters that you are measuring across. An example of this for Au nanoclusters, using the RGL potetial with parameters from Baletto *et al.* ([DOI: 10.1063/1.1448484](https://doi.org/10.1063/1.1448484)), is shown below:

<p align="center">
	<img src="https://github.com/GardenGroupUO/NISP/blob/main/Documentation/source/results/Au_Max_Size_2000_Interpolation_Scheme.png">
</p>

The second plot is the same nterpolation scheme plot shown above, but with lines through it at the places that you want to obtain cluster with the particular number of atoms that you desire. 

<p align="center">
	<img src="https://github.com/GardenGroupUO/NISP/blob/main/Documentation/source/results/Au_Max_Size_2000_Interpolation_Scheme_with_lines.png">
</p>

There are also text documents that contain the delta energies of the various nanoclusters that you calculated, as well as instructions about how to remove atoms from certain nanoclusters in order to get icosahedral, decahedral, and octahedral nanoclusters with the particular number of atoms that you desire. [Click here to see examples of all of these plots and text files.](https://github.com/GardenGroupUO/NISP/tree/main/Documentation/source/results)

## Where can I find the documentation for NISP

All the information about this program is found online at [nisp.readthedocs.io/en/latest/](https://nisp.readthedocs.io/en/latest/). Click the button below to also see the documentation: 

[![Documentation](https://img.shields.io/badge/Docs-click%20here-brightgreen)](https://nisp.readthedocs.io/en/latest/)

## About

<div align="center">

| Python | [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/NISP)](https://docs.python.org/3/) | 
|:----------------------:|:-------------------------------------------------------------:|
| Repositories | [![GitHub release (latest by date)](https://img.shields.io/github/v/release/GardenGroupUO/NISP)](https://github.com/GardenGroupUO/NISP) [![PyPI](https://img.shields.io/pypi/v/NISP)](https://pypi.org/project/NISP/) [![Conda](https://img.shields.io/conda/v/gardengroupuo/nisp)](https://anaconda.org/GardenGroupUO/nisp) |
| Documentation | [![Documentation](https://img.shields.io/badge/Docs-click%20here-brightgreen)](https://nisp.readthedocs.io/en/latest/) [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/GardenGroupUO/Organisms_Jupyter_Examples/main?urlpath=lab) | 
| Citation | [![Citation](https://img.shields.io/badge/Citation-click%20here-green.svg)](https://doi.org/10.1039/C7NR09440J) | 
| Tests | [![LGTM Grade](https://img.shields.io/lgtm/grade/python/github/GardenGroupUO/NISP)](https://lgtm.com/projects/g/GardenGroupUO/NISP/context:python)
| License | [![Licence](https://img.shields.io/github/license/GardenGroupUO/NISP)](https://www.gnu.org/licenses/agpl-3.0.en.html) |
| Authors | Geoffrey R. Weal, Dr. Anna L. Garden, Dr. Andreas Pedersen and Prof. Hannes Jónsson |
| Group Website | https://blogs.otago.ac.nz/annagarden/ |

</div>
