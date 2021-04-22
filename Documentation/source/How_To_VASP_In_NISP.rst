
.. _How_To_VASP_In_NISP:

How to perform NISP with VASP calculations
==========================================

In this article, we will look at how to run NISP where VASP is used to locally optimise nanoclusters. The ``Interpolation_Script.py`` python script that is used is the same as shown previously in :ref:`How_To_Run_NISP`, but with an extra component. An example of a ``Interpolation_Script.py`` python script that uses VASP is shown below:

.. literalinclude:: VASP_Interpolation_Script.py
	:language: python
	:caption: Interpolation_Script.py
	:tab-width: 4
	:linenos:

The ``input_information`` dictionary
------------------------------------

The extra component has been included in the ``input_information`` dictionary is the ``slurm_information``. ``slurm_information`` is a dictionary that contains all the information that is needed to create the ``submit.sl`` files required to submit VASP calculations to slurm. The following information is need in the ``'slurm_information'`` dictionary:

* **project** (*str.*): This is the name of the project that you want to submit this job to.
* **time** (*str.*): This is the amount of time you want to give to your slurm jobs, given as ``'HH:MM:SS'``, where ``'HH:MM:SS'`` is the hours, minutes, and seconds you want to give to a job. 
* **nodes** (*str.*): This is the number of nodes that you would like to give to a job.
* **ntasks_per_node** (*str./int*): This is the number of cpus that you give to a job. 
* **mem-per-cpu** (*str.*): This is the amount of momeory you are giving to your job per cpu

The following can also be included in ``'slurm_information'`` dictionary, but these are default value for these if you do not give a value for them.

* **partition** (*str.*): This is the partition that is given to your job. See `Mahuika Slurm Partitions <https://support.nesi.org.nz/hc/en-gb/articles/360000204076-Mahuika-Slurm-Partitions>`_ for more information about partition on NeSI (Default: ``'large'``).
* **email** (*str.*): This is the email address you would like notifications about your slurm job to be sent to (Default: ``''``).
* **vasp_version** (*str.*): This is the version of VASP that you would like to load in on slurm (Default: ``'VASP/5.4.4-intel-2017a'``).
* **vasp_execution** (*str.*): This is the name of the vasp program that you execute (Default: ``'vasp_std'``).

Make sure that you include ``'slurm_information'`` in ``input_information`` by writing in ``Interpolation_Script.py``

.. code-block:: python

	input_information['Slurm Information'] = slurm_information

An example of these parameters in ``Interpolation_Script.py`` is given below:

.. literalinclude:: VASP_Interpolation_Script.py
	:caption: Interpolation_Script.py
	:language: python
	:tab-width: 4
	:linenos:
	:lineno-start: 9
	:lines: 9-20

Other files that you will need
------------------------------

You will also need to give NISP some other files that are needed by VASP to perform calculations. In the same place where you place your ``Interpolation_Script.py`` file, you want to create another folder called ``VASP_Files``. In this ``VASP_Files`` folder you want to include the following files:

* ``INCAR``: This contains all the setting that are required by VASP to perform calculations. 
* ``POTCAR``: This is the file that contains the information required to locally optimise a nanocluster with DFT using a certain functional.
* ``KPOINTS``: This contain the information used to specify the Bloch vectors (k-points) that will be used to sample the Brillouin zone in your calculation.

These files will be copied by NISP into each nanocluster folder. See `an example of a setup of NISP for VASP here <https://github.com/GardenGroupUO/NISP/tree/main/Examples/VASP>`_. 


What to do after you have run NISP
----------------------------------

After you run NISP, this will create a new folder called ``VASP_Clusters``, which contains subfolders of all your nanoclusters. Each subfolder will contain a ``POSCAR``, ``INCAR``, ``POTCAR``, ``KPOINTS``, and ``submit.sl`` that are needed by VASP to perform DFT calculations. Each nanocluster is ready to be locally optimised with VASP.

You will find that there are many nanoclusters are created by NISP. To submit all of these nanoclusters for local minimisation by VASP, you can execute the program called ``Run_submitSL_slurm.py`` which will execute all of your nanocluster DFT optimisations to slurm. To run this script, type ``Run_submitSL_slurm.py`` into the terminal inside of your newly created ``VASP_Clusters`` folder. See  :ref:`Installation of NISP <Installation>` for how to use this ``Run_submitSL_slurm.py`` script. 