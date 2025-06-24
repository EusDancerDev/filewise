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
from pathlib import Path

#------------------------#
# Import project modules #
#------------------------#

from filewise.file_operations.ops_handler import (
    copy_files,
    remove_files,
    rename_objects
)
from filewise.file_operations.path_utils import find_dirs_with_files
from pygenutils.arrays_and_lists.conversions import flatten_to_string
from pygenutils.arrays_and_lists.data_manipulation import flatten_list
from pygenutils.operative_systems.os_operations import run_system_command

#-------------------------#
# Define custom functions #
#-------------------------#

def _validate_parameters() -> None:
    """
    Validate the input parameters for the copy and compress workflow.
    
    Raises
    ------
    ValueError
        If any parameter validation fails.
    FileNotFoundError
        If the high-level path doesn't exist.
    """
    # Validate high-level path
    if not HIGH_LEVEL_PATH or not isinstance(HIGH_LEVEL_PATH, str):
        raise ValueError("HIGH_LEVEL_PATH must be a non-empty string")
    
    if not Path(HIGH_LEVEL_PATH).exists():
        raise FileNotFoundError(f"High-level path does not exist: {HIGH_LEVEL_PATH}")
    
    # Validate extensions
    if not EXTENSIONS or not isinstance(EXTENSIONS, list):
        raise ValueError("EXTENSIONS must be a non-empty list")
    
    if not all(isinstance(ext, str) and ext.strip() for ext in EXTENSIONS):
        raise ValueError("All extensions must be non-empty strings")
    
    # Validate file lists
    if len(file_list_orig) != len(file_list_rename):
        raise ValueError("Original and rename file lists must have the same length")
    
    if not all(isinstance(f, str) and f.strip() for f in file_list_orig + file_list_rename):
        raise ValueError("All file names must be non-empty strings")


def _execute_copy_compress_workflow() -> None:
    """
    Execute the complete copy and compress workflow with error handling.
    
    This function orchestrates the entire process including validation,
    file removal, searching, copying, renaming, and optional compression.
    """
    try:
        # Step 0: Validate parameters #
        #-----------------------------#
        
        _validate_parameters()
        
        # Step 1: Delete already present files #
        #--------------------------------------#
        
        print("Removing existing files...")
        remove_files(patterns=file_list_rename,
                     input_directories=".",
                     match_type="glob_both")

        # Step 2: Search mechanism to find directories with files #
        #---------------------------------------------------------#
        
        print("Searching for files in directories...")
        found_dirs = find_dirs_with_files(file_list_orig,
                                          search_path=HIGH_LEVEL_PATH,
                                          match_type="glob_both", 
                                          dirs_to_exclude=DIRS_TO_EXCLUDE)

        # Step 3: Copy files #
        #--------------------#
        
        print("Copying files...")
        copy_files(file_list_orig, found_dirs, dirs_to_exclude=DIRS_TO_EXCLUDE)

        # Step 4: Rename the copied files (optional) #
        #--------------------------------------------#
        
        if file_list_rename:
            print("Renaming files...")
            rename_objects(file_list_orig, file_list_rename)

        # Step 5: Compress files if 'compress' is True #
        #----------------------------------------------#
        
        if COMPRESS:
            print("Berrizendatutako programak karpeta konprimatu batean gordetzen...")
            time.sleep(0.5)
            
            # Prepare command for zipping with flattened lists #
            file_list_rename_flat = flatten_list(file_list_rename)
            file_list_rename_str = flatten_to_string(file_list_rename_flat)
            
            if files_excluded_from_zipping:
                files_excluded_flat = flatten_list(files_excluded_from_zipping)
                files_excluded_str = f"-x {flatten_to_string(files_excluded_flat)}"        
                zip_command = f"zip {OUTPUT_ZIP_FILE} {file_list_rename_str} {files_excluded_str}"
            else:
                zip_command = f"zip {OUTPUT_ZIP_FILE} {file_list_rename_str}"
            
            # Execute the zip command #
            run_system_command(zip_command, shell=True)
            print("Compression completed successfully!")

    except Exception as e:
        print(f"Error during copy-compress workflow: {e}")
        raise

#--------------------------#
# Parameters and constants #
#--------------------------#

# Config Parameters #
#-------------------#

HIGH_LEVEL_PATH: str = "/home/username/Documents"  # High-level directory to search
EXTENSIONS: list[str] = ["jpg", "pdf", "zip"]  # Extensions to work with

DIRS_TO_EXCLUDE: list[str] | None = None  # Optionally exclude directories

COMPRESS: bool = True  # Option to compress the files
OUTPUT_ZIP_FILE: str = f"compressed_file.{EXTENSIONS[-1]}"  # Default output zipped file

# List of file names to search #
#------------------------------#

file_list_orig: list[str] = [
    f"2023_garbiago.{EXTENSIONS[0]}",
    f"Jon_Ander_Gabantxo_betea.{EXTENSIONS[1]}",
    f"NAN_aurrealdea.{EXTENSIONS[0]}",
    f"NAN_atzealdea.{EXTENSIONS[0]}",
    f"aurrealdea.{EXTENSIONS[0]}",
    f"atzealdea.{EXTENSIONS[0]}",
    f"lan-bizitza_2023-10-20.{EXTENSIONS[1]}",
    f"meteorologia-ikastaroa.{EXTENSIONS[1]}",
    f"Aula_Carpe_Diem-MySQL_PHP.{EXTENSIONS[1]}",
    f"EGA.{EXTENSIONS[1]}",
    f"titulu_ofiziala.{EXTENSIONS[1]}",
    f"HEO-ingelesa_C1.{EXTENSIONS[1]}",
    f"titulo_oficial.{EXTENSIONS[1]}"
]

# Corresponding names for renaming #
#----------------------------------#

file_list_rename: list[str] = [
    f"argazkia.{EXTENSIONS[0]}",
    f"CV_betea.{EXTENSIONS[1]}",
    f"NAN_aurrealdea.{EXTENSIONS[0]}",
    f"NAN_atzealdea.{EXTENSIONS[0]}",
    f"gida-baimena_aurrealdea.{EXTENSIONS[1]}",
    f"gida-baimena_atzealdea.{EXTENSIONS[1]}",
    f"lan-bizitza_2023-10-20.{EXTENSIONS[1]}",
    f"meteorologia-ikastaroa_ziurtagiria.{EXTENSIONS[1]}",
    f"MySQL-PHP_ziurtagiria.{EXTENSIONS[0]}",
    f"EGA-titulu_ofiziala.{EXTENSIONS[1]}",
    f"fisikako_gradua-titulu_ofiziala.{EXTENSIONS[1]}",
    f"ingelesa_C1-titulu_ofiziala.{EXTENSIONS[1]}",
    f"master_meteorologia_titulo_oficial.{EXTENSIONS[1]}"
]

# Files to exclude from compression #
#-----------------------------------#

files_excluded_from_zipping: list[list[str]] = [file_list_rename[1:3]]  


# Execute the workflow
if __name__ == "__main__":
    _execute_copy_compress_workflow()
