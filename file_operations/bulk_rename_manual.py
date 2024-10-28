#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
**Purpose**

This program serves as a template for batch renaming files or directories 
within a specified path. It is designed to be simple, fast, and easily 
modifiable. No external modules are imported to keep the program self-contained. 
Users can restructure the file as needed, such as by recursing into a 
directory or modifying the renaming rules.
"""

#----------------#
# Import modules #
#----------------#

import os
from pathlib import Path

#------------------#
# Define functions #
#------------------#

def change_to_path_and_store(path_str):
    """
    Change the current working directory to the specified path.

    Parameters
    ----------
    path_str : str
        The path to which the working directory should be changed.
        
    Returns
    -------
    None
    """
    main_posix_path = Path(path_str)
    os.chdir(main_posix_path)
    
    
def get_current_path():
    """
    Get the current working directory.

    Returns
    -------
    cwd_path : PosixPath
        The current working directory as a Path object.
    """
    cwd_path = Path.cwd()
    return cwd_path


def get_obj_list(main_posix_path, obj_type, path_to_str=False):
    """
    Get a sorted list of files or directories in the specified path.

    Parameters
    ----------
    main_posix_path : Path
        The main path where files or directories are to be listed.
    obj_type : str
        The type of object to list. Must be either 'file' or 'directory'.
    path_to_str : bool, optional
        If True, converts Path objects to strings (default is False).

    Returns
    -------
    list
        A sorted list of file or directory names (as Path objects or strings).

    Raises
    ------
    ValueError
        If an unsupported object type is provided.
    RuntimeError
        If any other error occurs during listing.
    """
    try:
        obj_list = object_listing_dict[obj_type](main_posix_path)
        obj_list.sort()
        if path_to_str:
            obj_list = [obj.name for obj in obj_list]
        return obj_list
    except KeyError:
        raise ValueError(f"Unsupported object type '{obj_type}'. "
                         f"Choose one from {obj_type_list}.")
    except Exception as e:
        raise RuntimeError(f"An error occurred while listing {obj_type}s: "
                           f"{str(e)}")
     
    
def print_format_string(string2format, arg_list):
    """
    Print a formatted string with the provided arguments.

    Parameters
    ----------
    string2format : str
        The string to format.
    arg_list : list
        The list of arguments to format into the string.
    """
    print(string2format.format(*arg_list))

#-------------------#
# Define parameters #
#-------------------#

# Path objects #
#--------------#

# Define the main path #
main_path = "/home/jonander/Pictures/2024"

# Change to the desired directory and get that path #
change_to_path_and_store(main_path)
cwd_path = get_current_path()

# Progress information string #
rename_progress_info_str = """Current directory : {}
File or directory list : {}
Length of the list : {}
"""

# Supported object types #
obj_type_list = ["file" ,"directory"]

# Switch case dictionaries #
#--------------------------#

object_listing_dict = {
    obj_type_list[0] : lambda path : [file
                                      for file in path.iterdir() 
                                      if file.is_file()],
    obj_type_list[1] : lambda path : [dirc 
                                      for dirc in path.iterdir() 
                                      if dirc.is_dir()]
    }

#--------------------#
# Batch rename files #
#--------------------#

# List of files (or directories) in the previously given path #
obj_list = get_obj_list(cwd_path, "directory", return_path_obj=True)
len_obj_list = len(obj_list)

# Print basic information such as current path, list of files and its length #
arg_list = [cwd_path, obj_list, len_obj_list]
print_format_string(rename_progress_info_str, arg_list)

# Perform the file renaming #
for num, file in enumerate(obj_list, start=1):
    new_num = f"{num:02d}"
    ext = file.suffix
    new_file = f"{new_num}{ext}"
    print(file, new_file)
    # os.rename(f, new_file)