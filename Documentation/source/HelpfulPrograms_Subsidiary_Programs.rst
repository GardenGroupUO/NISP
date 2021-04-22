
.. _HelpfulPrograms_Subsidiary_Programs:

Helpful Programs to run NISP
############################

As well as the genetic algorithm, we have included a bunch of programs that can be used to create all the scripts that are needed to run the genetic algorithm. In this articles, we will introduce all of the program that can be used to create these scripts and to run them all in mass. Example files for running many of these programs can be found in Examples/CreateSets. Some of these programs can also be run by typing the program you want to run into the terminal from whatever directory you are in. 

The scripts and programs that we will be mentioned here are:

.. contents::
    :depth: 1
    :local:

.. _What_to_make_sure_is_done_before_running_any_of_these_scripts:

What to make sure is done before running any of these scripts. 
**************************************************************

If you installed NISP through pip3
----------------------------------

If you installed the NISP program with ``pip3``, these scripts will be installed in your bin. You do not need to add anything into your ``~/.bashrc``. You are all good to go. 

If you performed a Manual installation
--------------------------------------

If you have manually added this program to your computer (such as cloning this program from Github), you will need to make sure that you have included the ``Subsidiary_Programs`` folder into your ``PATH`` in your ``~/.bashrc`` file. All of these program can be found in the ``Subsidiary_Programs`` folder. To execute these programs from the ``Subsidiary_Programs`` folder, you must include the following in your ``~/.bashrc``:

.. code-block:: bash

	export PATH_TO_NISP="<Path_to_NISP>" 

where ``<Path_to_NISP>"`` is the path to get to the genetic algorithm program. Also include somewhere before this in your ``~/.bashrc``:

.. code-block:: bash

	export PATH="$PATH_TO_NISP"/NISP/Subsidiary_Programs:$PATH

See more about this in :ref:`Installation of NISP <Installation>`. 

.. _Run_submitSL_slurm_py:

``Run_submitSL_slurm.py`` - How to execute all Trials using the JobArray Slurm Job Submission Scheme
****************************************************************************************************

It is possible to perform this interpolation scheme using the energies of nanoclusters that have be obtained with DFT using VASP. If you select your ``'Local Optimiser'`` input in your ``input_information`` dictionary to be ``'VASP'``, NISP will create a bunch of icosahedral, decahedral, and octahedral nanoclusters that are setup to run VASP calculations upon. This includes a POSCAR and submit.sl file, as well as POTCAR, INCAR, and KPOINTS files that you provide. Many nanoclusters are created to be used in the interpolation scheme, and therefore a lot of submit.sl file to submit to slurm. 

To make this easier for the user, NISP has been included with the ``Run_submitSL_slurm.py`` script, which is designed to submit all your VASP calculations to slurm. This script will walk through all subdirectories from the directory you run this from and will run all your submit.sl scripts for you automatically. All you need to do is to move into the ``VASP_Clusters`` folder that has been created by slurm and enter ``Run_submitSL_slurm.py`` into the terminal, press enter, and watch all your NISP nanocluster be submitted to slurm. 

There is one input that you can pass into the program. The ``Run_mass_submitSL_slurm.py`` program is designed to wait one minute between submitting jobs. This is because you can cause slurm issues if too many jobs are submitted at once. However, you can override this if you enter in ``False`` as the first argument. This will tell ``Run_submitSL_slurm.py`` to keep submitting jobs without waiting one minute between them. 

Note that you will notice that if you submit too many jobs, or if you submit too many jobs too quickly, you will get problems with slurm that you are submitting too many jobs or submitting them too quickly. This is all dependent on how slurm is set up. This has been covered by the program, and will tell you how long it will be waiting when it is waiting. Do not stop the program while it is submitting jobs. If you do quit before it has finished, it will make resubmitting jobs difficult. 

The following variables can be different for different people. Feel free to change the following variables in your ``Subsidiary_Programs/Run_submitSL_slurm.py`` as you need

* **Max_jobs_in_queue_at_any_one_time** (*int*): This is the maximum number of jobs that slurm allows you to have in your queue. This is usually set by default to 1000. I personally have set this to 10,000 and this is what is current set in ``Run_submitSL_slurm.py``. Default: 10,000
* **time_to_wait_before_next_submission** (*float*): This is the amount of time that this program waits after submitting a job, before continuing on. This is given in seconds. **Do not set this to less than 10 seconds.** Default: 20.0 (seconds)
* **time_to_wait_max_queue** (*float*): This is the amount of time that this program waits after it has found that the maximum number of jobs have been submitted to the queue. ``Run_submitSL_slurm.py`` will wait for this amount of time before continuing again. This is given in seconds. **Do not set this to less than 10 seconds.** Default: 60.0 (seconds)

Problems can occur every so often when submitting jobs to slurm, but these are generally internet connectivity problems or slurm hanging problems that resolve themselves after a few tens of seconds. There are two other variables that determine how ``Run_submitSL_slurm.py`` will deal with issues. 

* **time_to_wait_before_next_submission_due_to_temp_submission_issue** (*float*): This is the amount of time that this program waits after it has experienced an error in submitting a job. This is given in seconds. **Do not set this to less than 10 seconds.** Default: 10.0 (seconds)
* **number_of_consecutive_error_before_exitting** (*int*): This is the number of times that ``Run_mass_submitSL_slurm.py`` will attempt to resubmit a job to slurm before it will give up. After this many consecutive errors arising, some systematic error is likely occuring. In this case, ``Run_mass_submitSL_slurm.py`` will print the directories of all the jobs that were not submitted and then close. 

Hopefully running ``Run_submitSL_slurm.py`` will submit all your genetic algorithm trials. 

The names of the jobs can be quite big. When looking in ``squeue`` to see how things are going, it is sometimes useful to expand the names in the squeue output. This can be done as shown below:

.. code-block:: bash
	
	squeue -o "%.20i %.9P %.5Q %.50j %.8u %.8T %.10M %.11l %.6D %.4C %.6b %.20S %.20R %.8q" -u $USER --sort=+i

Here, after ``-o``, ``i`` specifies the job ID and ``j`` specifies the job name. You can change this number to the number of characters this will display. Here ``%.20i`` indicates that ``squeue`` will dedicate 20 characters to displaying the job ID and ``%.50j`` indicates that ``squeue`` will dedicate 50 characters to displaying the name of the job. 

