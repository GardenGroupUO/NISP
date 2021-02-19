
.. _How_To_Run_NISP:

*Interpolation_Script.py* - How to run NISP
###########################################

In this article, we will look at how to run NISP. NISP is run through the ``Interpolation_Script.py`` python script. You can find examples of ``Run.py`` files at `github.com/GardenGroupUO/Organisms <https://github.com/GardenGroupUO/Organisms>`_ under ``Examples``. Also, you can try out this program by running an example script through a Jupyter notebook. See :ref:` Examples of running NISP <Examples_of_Running_NISP>` to get access to examples of running NISP through this Jupyter notebook!

Running the ``Interpolation_Script.py`` script
**********************************************

We will explain how the ``Interpolation_Script.py`` code works by running though the example shown below:

.. literalinclude:: Interpolation_Script.py
	:language: python
	:caption: Interpolation_Script.py
	:name: Interpolation_Script.py
	:tab-width: 4
	:linenos:

Lets go through each part of the ``Interpolation_Script.py`` file one by one to understand how to use it. 

1) Input information for the interpolation scheme
=================================================

We first load the information required by the interpolation scheme. All this information is loaded as entries into the dictionary called ``input_information``. 

The pieces of information required in ``input_information`` are:

* **Element Type** (*str.*): This is the type of element that the cluster is made up of.
* **Cohesive Energy** (*float*): This is the cohesive energy of the element you are using. See :ref:`How_to_obtain_cohesive_energies` to find about about how to obtain cohesive energies. 
* **Maximum No. of Atoms** (*int*): The number of offspring generated per generation. 
* **Local Optimiser** (*def*): This is a local optimisation method that you will locally optimise clusters with as well as their delta energies. See :ref:`Local_Minimisation_Function` for information about the local optimiser. If you do not want to give a local optimiser, either set ``input_information['Local Optimiser'] = None``, or do not enter an entry for ``input_information['Local Optimiser']`` into your ``Interpolation_Script.py`` script. Do this if you want to input your data into NISP manually. 
* **Manual Mode** (*bool* or *str.*): This indicates that you do not not want NISP to automatically locally optimise the clusters that are made and get their energies. If ``Manual Mode`` is set to ``False``, NISP will perform all the calculation needed, you just need to provide a local optimiser definition. The other options that you can set ``Manual Mode`` to are:
	* ``'VASP'``: This will format the cluster file as POSCARs and will place those POSCARs into organised folders.
	* ``'xyz'``:  This will format all the clusters as xyz files.
	All these files and subdirectories will be placed into a folder called ``clusters``. 





the program will make all the clusters that you would like to manually locally optimise and get the energies of, as well as an input file for you to input those energies into. If you have already run this program once and got the input file, this tag will tell NISP to look through the input file and get all the data from it to make the interpolation scheme plots and results files. 

An example of these parameters in ``Interpolation_Script.py`` is given below:

.. literalinclude:: Interpolation_Script.py
	:language: python
	:tab-width: 4
	:linenos:
	:lineno-start: 4
	:lines: 4-9

2) Plotting information for the interpolation scheme
====================================================

We then load the information required by the interpolation scheme to plot the results from the interpolation scheme. The sizes of all the clusters that you would like to obtain possible clusters for are also inputted here and given as txt files. 

All this information is loaded as entries into the dictionary called ``output_information``. 

The pieces of information required in ``output_information`` are:

* **Upper No of Atom Range** (*int*): This is the upper size range that you would like to plot. 
* **Lower No of Atom Range** (*int*): This is the lower size range that you would like to plot. 
* **Upper Delta Energy Range** (*float*): This is the upper delta energy range that you would like to plot. 
* **Lower Delta Energy Range** (*float*): This is the lower delta energy range that you would like to plot. 
* **Size to Interpolate Over** (*list of ints*): These are all the sizes of clusters that you would like to obtain possible clusters for, including perfect, open-shell, and close-shell clusters. 
* **Filename Prefix** (*str.*): This is the prefix of the name that you want to give to files that are create by the NISP program. This does not need to be given, as there is a default prefix given. The default filename prefix includes the element of the cluster as well as the maximum no. of atoms that the program was run up to. 

An example of these parameters in ``Interpolation_Script.py`` is given below:

.. literalinclude:: Interpolation_Script.py
	:language: python
	:tab-width: 4
	:linenos:
	:lineno-start: 11
	:lines: 11-17

3) The number of CPUs used by the program
=========================================

NISP can run for a long time, especially if you have set **Maximum No. of Atoms** to over 1000 atoms. Therefore, it is possible to run this program for a while. Therefore, it is possible to parallelise this program so that it run a bit faster. This can be set by setting the ``no_of_cpus`` variable. ``no_of_cpus`` must be set to an int. The default value for the ``no_of_cpus`` variable is ``1``. 

An example of ``no_of_cpus`` in ``Interpolation_Script.py`` is given below:

.. literalinclude:: Interpolation_Script.py
	:language: python
	:tab-width: 4
	:linenos:
	:lineno-start: 19
	:lines: 19

Run NISP!
=========

You have got to the end of all the parameter setting stuff. Now on to running NISP. The next part of the ``Interpolation_Script.py`` script tells NISP to run. This is written as follows in the ``Interpolation_Script.py``:

.. literalinclude:: Interpolation_Script.py
	:language: python
	:tab-width: 4
	:linenos:
	:lineno-start: 21
	:lines: 21