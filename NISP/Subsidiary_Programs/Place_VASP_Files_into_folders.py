#!/usr/bin/python
'''
Geoffrey Weal, make_finish_files.py, 10/02/2021

This program will put all the input files you need for VASP into all the cluster folders.
'''
import os, sys
from os import copyfile

VASP_Input_Files = 'VASP_Input_Files'
files_to_copy = os.listdir(VASP_Input_Files)

cluster_folders = []
for folder in os.listdir('.'):
	if os.path.isdir('./'+folder) and (folder.startswith('Ico_') or folder.startswith('Deca_') or folder.startswith('Octa_'))
		cluster_folders.append(folder)

for cluster_folder in cluster_folders:
	print('Copying files from '+VASP_Input_Files+' to '+cluster_folder)
	for file_to_copy in files_to_copy:
		copyfile(VASP_Input_Files+'/'+file_to_copy,cluster_folder+'/'+file_to_copy)