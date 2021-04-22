
.. _Example_data_from_NISP:

Examples of data that the NISP program gives
============================================

Once NISP has completed or once VASP is able to get or has been given all the energies of nanoclusters, NISP will give a set of plots and data. Examples of these can be found on the github page (`Click here to see examples of all of these plots and text files <https://github.com/GardenGroupUO/NISP/tree/main/Documentation/source/results>`_) and given below.


Firstly, NISP will output a series of plots and text files about various features of the nanoclusters. The first plot that is given is the interpolation scheme plot, which shows all the estimated energies of nanoclusters across the size range of nanoclusters that you are measuring across. An example of this for Au nanoclusters, using the RGL potetial with parameters from Baletto *et al.* `DOI: 10.1063/1.1448484 <https://doi.org/10.1063/1.1448484>`_, is shown below:

.. image:: results/Au_Max_Size_2000_Interpolation_Scheme.png
  :width: 700
  :alt: Interpolation Scheme Plot
  :align: center

The second plot is the same nterpolation scheme plot shown above, but with lines through it at the places that you want to obtain cluster with the particular number of atoms that you desire. 

.. image:: results/Au_Max_Size_2000_Interpolation_Scheme_with_lines.png
  :width: 700
  :alt: Interpolation Scheme Plot with lines for nanoclusters with a particular number of atoms
  :align: center


Secondly, there are also text documents that contain various information from the NISP program. The first are a txt file that contains all the delta energies of the various nanoclusters that you calculated. An example is given below

.. include:: results/Au_Max_Size_2000_atoms_interpolation_scheme_results_file.txt
   :literal:

As well as this txt document, NISP will also give a set of other text documents that give instructions about how to remove atoms from certain nanoclusters in order to get icosahedral, decahedral, and octahedral nanoclusters with the particular number of atoms that you desire. This is based on the clusters of particular numbers of atoms that you have given in ``output_information['Size to Interpolate Over']``. An example is given below

.. include:: results/Au_Max_Size_2000_Clusters_interpolated_at_size_742.txt
   :literal:

