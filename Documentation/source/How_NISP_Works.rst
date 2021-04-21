
.. _How_NISP_Works:

How the Nanocluster Interpolation Scheme Program (NISP) works
=============================================================

The NISP program is an interpolation scheme that is designed to give an approximate guide for the estimated energies of unsymmetric nanoclusters based on energetic trends between perfect, closed-shell nanoclusters. 

This program will create all the perfect, close shell icosahedral, decahedral, and octahedral clusters that can be created between 13 atoms and an upper atom number limit. These nanoclusters are locally optimised using either an ASE, an ASE-integrated calculator, or with VASP. 

After the nanoclusters are locally optimised, the delta energy is obtained for each nanocluster before providing plots and text files that indicate the estimated energies of perfect, closed-shell and unsymmetric nanoclusters and how to remove atoms from the larger perfect closed-shell nanocluster to give unsymmetric nanoclusters with a certain number of atoms. 

See “Reassignment of ‘magic numbers’ of decahedral and FCC structural motifs” (`DOI: 10.1039/C7NR09440J <https://doi.org/10.1039/C7NR09440J>`_) for more information about how this interpolation scheme works. 
