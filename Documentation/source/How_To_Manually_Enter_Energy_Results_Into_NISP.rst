
.. _How_To_Manually_Enter_Energy_Results_Into_NISP:

How to manually enter energy results into NISP
==============================================

It is also possible to run NISP in manual mode, where NISP creates xyz files of all your nanoclusters, and a ``Au_Max_Size_YYYY_atoms_interpolation_scheme_input_file.txt``, where ``YYYY`` is the maximum size cluster that you have chosen to measure up to. In this article, we will look at how to run NISP in manual mode. An example of a ``Interpolation_Script.py`` python script that is set to manual mode is shown below:

.. literalinclude:: Manual_Mode_Interpolation_Script.py
	:language: python
	:caption: Interpolation_Script.py
	:tab-width: 4
	:linenos:

Here, ``input_information['Local Optimiser'] = 'Manual Mode'``

What to do after you have run NISP
----------------------------------

Once you have run NISP, you will find that NISP will have made a folder called ``Clusters`` and a file called ``Au_Max_Size_YYYY_atoms_interpolation_scheme_input_file.txt``, where ``YYYY``. 

* ``Clusters``: This folder contains all the ``xyz`` files of the clusters that you need to obtain energies for. 
* ``Au_Max_Size_YYYY_atoms_interpolation_scheme_input_file.txt``: This is the file that you want to place all the energies for each nanocluster in this list. 

What to do once you have got all the energies of your nanoclusters
------------------------------------------------------------------

Once you have obtained all the energies for each of the nanoclusters in the ``Clusters`` folder, you want to add these energies to the right most side of each column of the ``Au_Max_Size_YYYY_atoms_interpolation_scheme_input_file.txt`` column. For example, you want to place your energies into each place in the file below where ``______`` is given

.. code-block:: bash

	Element: Au Max_Size: 2000
	Enter the energies of the clusters below to the right most of each line (not the delta energies, NISP can do that for you later)
	------------------------------
	Icosahedron
	13      2           ______
	55      3           ______
	147     4           ______
	309     5           ______
	561     6           ______
	923     7           ______
	1415    8           ______
	Octahedron
	6       (2, 0)      ______
	19      (3, 0)      ______
	13      (3, 1)      ______
	44      (4, 0)      ______
	38      (4, 1)      ______
	85      (5, 0)      ______
	79      (5, 1)      ______
	55      (5, 2)      ______
	146     (6, 0)      ______
	...     
	Decahedron
	7       (2, 1, 0)   ______
	49      (2, 1, 1)   ______
	156     (2, 1, 2)   ______
	358     (2, 1, 3)   ______
	685     (2, 1, 4)   ______
	13      (2, 2, 0)   ______
	75      (2, 2, 1)   ______
	212     (2, 2, 2)   ______
	454     (2, 2, 3)   ______
	831     (2, 2, 4)   ______
	1373    (2, 2, 5)   ______
	19      (2, 3, 0)   ______
	101     (2, 3, 1)   ______
	268     (2, 3, 2)   ______
	550     (2, 3, 3)   ______
	977     (2, 3, 4)   ______
	1579    (2, 3, 5)   ______
	25      (2, 4, 0)   ______
	127     (2, 4, 1)   ______
	324     (2, 4, 2)   ______
	646     (2, 4, 3)   ______
	1123    (2, 4, 4)   ______
	1785    (2, 4, 5)   ______
	31      (2, 5, 0)   ______
	153     (2, 5, 1)   ______
	380     (2, 5, 2)   ______
	742     (2, 5, 3)   ______
	1269    (2, 5, 4)   ______
	1991    (2, 5, 5)   ______
	23      (3, 1, 0)   ______
	100     (3, 1, 1)   ______
	262     (3, 1, 2)   ______
	539     (3, 1, 3)   ______
	961     (3, 1, 4)   ______
	39      (3, 2, 0)   ______
	146     (3, 2, 1)   ______
	348     (3, 2, 2)   ______
	675     (3, 2, 3)   ______
	1157    (3, 2, 4)   ______
	1824    (3, 2, 5)   ______
	55      (3, 3, 0)   ______
	192     (3, 3, 1)   ______
	434     (3, 3, 2)   ______
	811     (3, 3, 3)   ______
	1353    (3, 3, 4)   ______
	71      (3, 4, 0)   ______
	238     (3, 4, 1)   ______
	...