
.. _How_to_obtain_cohesive_energies:

How to obtain cohesive energies
###############################

One of the pieces of information that is needed to obtain delta energies for this program is the cohesive energy for the crystal structure for the metal of interest. This is the energy for a crystal in a cell with periodic boundary conditions divided by the number of atoms in the cell (given as eV/atom). 

We have developed a program designed to help you to obtain the cohesive energy called LatticeFinder. You can find LatticeFinder at github.com/GardenGroupUO/LatticeFinder and documentation at latticefinder.readthedocs.io

Provided in the LatticeFinder Github repository are examples of *Run_LatticeFinder.py*. Find these various examples at https://github.com/GardenGroupUO/LatticeFinder/tree/main/Examples. These examples with their accompanying results are also given in https://github.com/GardenGroupUO/LatticeFinder_Examples/tree/main/Examples

We have also developed a Jupyter notebook with some examples of various *Run_LatticeFinder.py* that you can play with and muck around with. The Github repository for this Jupyter notebook can also be found at https://github.com/GardenGroupUO/LatticeFinder. 

Along with this Jupyter notebook, we have also implemented this Jupyter notebook into Binder. Binder (https://mybinder.org/) is an interactive online platform that allows you to use Jupyter notebooks on an web browser without having to set up anything. It does all the setting up on a virtual computer for you. If you want to play around with the LatticeFinder program before you download it on your computer or if you need help when things go wrong using LatticeFinder on your computer, Binder+Jupyter is the best way to do this. **It is recommended that you try out the LatticeFinder program on Binder if you are interested or intending on using the LatticeFinder program**.

The Binder webpage can be found at: 

.. image:: https://mybinder.org/badge_logo.svg
   :target: https://mybinder.org/v2/gh/GardenGroupUO/LatticeFinder/main?urlpath=lab
   :alt: Binder

This will load a Binder page that will allow you to play about with LatticeFinder interactively in Binder. This Binder page may load quickly, or it may take 1 to 2 minutes to load. Don't refresh the page as Binder takes a good amount of time to load. Get a coffee or a cup of tea while you wait. 

Once this is done you will see a Jupyter notebook that you can interact with. Mess around with it as much as you want!
