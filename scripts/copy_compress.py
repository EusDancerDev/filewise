#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module for Copying and Managing Files from High-Level Directories

Note: This module is designed to work seamlessly within a package, but can be
moved and executed from any path as needed. It uses external functions from
'filewise' and 'pygenutils'.

Workflow Overview:
1. Defines input parameters for file searching, copying, renaming, and compressing.
2. Deletes specified files in the current directory to avoid conflicts.
3. Searches for files in a specified high-level directory and identifies the directories 
   they are located in.
4. Copies the identified files to the current directory.
5. Renames the copied files if necessary.
6. Compresses the files if the 'compress' option is set to True.
"""

#----------------#
# Import modules #
#----------------#

import time

#-----------------------#
# Import custom modules #
#-----------------------#

from filewise.file_operations import ops_handler, path_utils
from pygenutils.arrays_and_lists import conversions
from pygenutils.operative_systems.os_operations import run_system_command

# Create aliases #
#----------------#

flatten_to_string = conversions.flatten_to_string

copy_files = ops_handler.copy_files
remove_files = ops_handler.remove_files
rename_objects = ops_handler.rename_objects

find_dirs_with_files = path_utils.find_dirs_with_files

#-------------------#
# Define parameters #
#-------------------#

high_level_path = "/home/username/Documents"  # High-level directory to search
extensions = ["jpg", "pdf", "zip"]  # Extensions to work with

dirs_to_exclude = None  # Optionally exclude directories

compress = True  # Option to compress the files
output_zip_file = f"compressed_file.{extensions[-1]}"  # Default output zipped file

# List of file names to search #
#------------------------------#

file_list_orig = [
    f"2023_garbiago.{extensions[0]}",
    f"Jon_Ander_Gabantxo_betea.{extensions[1]}",
    f"NAN_aurrealdea.{extensions[0]}",
    f"NAN_atzealdea.{extensions[0]}",
    f"aurrealdea.{extensions[0]}",
    f"atzealdea.{extensions[0]}",
    f"lan-bizitza_2023-10-20.{extensions[1]}",
    f"meteorologia-ikastaroa.{extensions[1]}",
    f"Aula_Carpe_Diem-MySQL_PHP.{extensions[1]}",
    f"EGA.{extensions[1]}",
    f"titulu_ofiziala.{extensions[1]}",
    f"HEO-ingelesa_C1.{extensions[1]}",
    f"titulo_oficial.{extensions[1]}"
]

# Corresponding names for renaming #
#----------------------------------#

file_list_rename = [
    f"argazkia.{extensions[0]}",
    f"CV_betea.{extensions[1]}",
    f"NAN_aurrealdea.{extensions[0]}",
    f"NAN_atzealdea.{extensions[0]}",
    f"gida-baimena_aurrealdea.{extensions[1]}",
    f"gida-baimena_atzealdea.{extensions[1]}",
    f"lan-bizitza_2023-10-20.{extensions[1]}",
    f"meteorologia-ikastaroa_ziurtagiria.{extensions[1]}",
    f"MySQL-PHP_ziurtagiria.{extensions[0]}",
    f"EGA-titulu_ofiziala.{extensions[1]}",
    f"fisikako_gradua-titulu_ofiziala.{extensions[1]}",
    f"ingelesa_C1-titulu_ofiziala.{extensions[1]}",
    f"master_meteorologia_titulo_oficial.{extensions[1]}"
]

# Files to exclude from compression #
#-----------------------------------#

files_excluded_from_zipping = [file_list_rename[1:3]]  

#--------------------------------------#
# Step 1: Delete already present files #
#--------------------------------------#

remove_files(patterns=file_list_rename,
             input_directories=".",
             match_type="glob_both")

#---------------------------------------------------------#
# Step 2: Search mechanism to find directories with files #
#---------------------------------------------------------#

found_dirs = find_dirs_with_files(file_list_orig,
                                  search_path=high_level_path,
                                  match_type="glob_both", 
                                  dirs_to_exclude=dirs_to_exclude)

#--------------------#
# Step 3: Copy files #
#--------------------#

copy_files(file_list_orig, found_dirs, dirs_to_exclude=dirs_to_exclude)

#--------------------------------------------#
# Step 4: Rename the copied files (optional) #
#--------------------------------------------#

if file_list_rename:
    rename_objects(file_list_orig, file_list_rename)

#----------------------------------------------#
# Step 5: Compress files if 'compress' is True #
#----------------------------------------------#

if compress:
    print("Berrizendatutako programak karpeta konprimatu batean gordetzen...")
    time.sleep(0.5)
    
    # Prepare command for zipping
    file_list_rename_str = flatten_to_string(file_list_rename)
    if files_excluded_from_zipping:
        files_excluded_str = f"-x {flatten_to_string(files_excluded_from_zipping)}"        
        zip_command = f"zip {output_zip_file} {file_list_rename_str} {files_excluded_str}"
    else:
        zip_command = f"zip {output_zip_file} {file_list_rename_str}"
    
    # Execute the zip command
    run_system_command(zip_command, shell=True)
