.. The Otago Research Genetic Algorithm for Nanoclusters, Including Structural Methods and Similarity (Organisms) documentation master file, created by
   sphinx-quickstart on Mon Oct  1 08:10:30 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to the Nanocluster Interpolation Scheme Program (NISP) documentation!
#############################################################################


.. image:: https://img.shields.io/pypi/pyversions/NISP
   :target: https://docs.python.org/3/
   :alt: Python Version


.. image:: https://img.shields.io/github/v/release/GardenGroupUO/NISP
   :target: https://github.com/GardenGroupUO/NISP
   :alt: GitHub release (latest by date)


.. image:: https://img.shields.io/pypi/v/NISP
   :target: https://pypi.org/project/NISP/
   :alt: PyPI


.. image:: https://img.shields.io/conda/v/gardengroupuo/nisp
   :target: https://anaconda.org/GardenGroupUO/nisp
   :alt: Conda


.. image:: https://mybinder.org/badge_logo.svg
   :target: https://mybinder.org/v2/gh/GardenGroupUO/Organisms_Jupyter_Examples/main?urlpath=lab
   :alt: Binder


.. image:: https://img.shields.io/github/license/GardenGroupUO/NISP
   :target: https://www.gnu.org/licenses/agpl-3.0.en.html
   :alt: Licence


.. .. image:: https://img.shields.io/lgtm/grade/python/github/GardenGroupUO/NISP
..     :target: https://lgtm.com/projects/g/GardenGroupUO/NISP/context:python
..     :alt: LGTM Grade



This documentation is designed to guide the user to use the Nanocluster Interpolation Scheme Program (NISP). This algorithm is designed to perform the interpolation scheme described in:

  *A. L. Garden, A. Pedersen, H. Jónsson, “Reassignment of ‘magic numbers’ of decahedral and FCC structural motifs”, Nanoscale, 10, 5124-5132 (2018),* `https://doi.org/10.1039/C7NR09440J <https://doi.org/10.1039/C7NR09440J>`_

This interpolation scheme creates all the perfect, close shell icosahedral, decahedral, and octahedral clusters that can be created between 13 atoms and an upper atom number limit. These clusters are locally optimised before the delta energy is obtained. 

The algorithm was designed by Dr Anna Garden of the University of Otago, Dunedin, New Zealand, and Dr. Andreas Pedersen and Prof. Hannes Jónsson of the University of Iceland. The Github page for this program can be found at `github.com/GardenGroupUO/NISP <https://github.com/GardenGroupUO/NISP>`_. 

Dr Anna Garden: `blogs.otago.ac.nz/annagarden <https://blogs.otago.ac.nz/annagarden/>`_
Dr Andreas Pedersen: `https://dk.linkedin.com/in/andreas-pedersen-a847025 <https://dk.linkedin.com/in/andreas-pedersen-a847025>`_
Prof Hannes Jónsson: `english.hi.is/staff/hj <https://english.hi.is/staff/hj>`_

**If you are new to the NISP program, it is recommended try it out by running NISP live on our interactive Jupyter+Binder page before you download it. On Jupyter+Binder, you can play around with the NISP program on the web. You do not need to install anything to try NISP out on Jupyter+Binder.** 

**Click the Binder button below to try NISP out on the web! (The Binder page may load quickly or may take 1 or 2 minutes to load)**


.. image:: https://mybinder.org/badge_logo.svg
   :target: https://mybinder.org/v2/gh/GardenGroupUO/NISP/main?urlpath=lab
   :alt: Binder


Table of Contents
=================

.. toctree::
   :maxdepth: 2

   How_NISP_Works
   Installation
   How_To_Run_NISP
   Local_Minimisation_Function
   How_to_obtain_cohesive_energies
   How_To_Manually_Enter_Energy_Results_Into_NISP
   Examples_of_Running_NISP
   NISP_Files
   genindex
   py-modindex

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`