#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 13:54:11 2024

@author: jonander
"""

#! /usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------#
# Import modules #
#----------------#

import numpy as np
import xarray as xr
import os
from pathlib import Path

#------------------------#
# Import project modules #
#------------------------#

from filewise.file_operations.path_utils import find_files
from pygenutils.arrays_and_lists.data_manipulation import flatten_list
from pygenutils.strings.string_handler import get_obj_specs
from pygenutils.strings.text_formatters import (
    format_string,
    print_format_string,
    string_underliner
)

#-------------------------#
# Define custom functions #
#-------------------------#

# Internal #
#----------#

def _unique_sorted(items: list) -> list:
    """
    Returns a sorted list of unique items.
    
    Parameters
    ----------
    items : list
        List of items to deduplicate and sort.
        
    Returns
    -------
    list
        Sorted list of unique items.
        
    Raises
    ------
    TypeError
        If items is not a list.
    """
    if not isinstance(items, list):
        raise TypeError("Input must be a list")
    
    return sorted(set(items))

# Public #
#--------#

# netCDF file searching #
#~~~~~~~~~~~~~~~~~~~~~~~#

# Main function #
#-#-#-#-#-#-#-#-#
    
def scan_ncfiles(search_path: str | list[str] | Path) -> dict[str, int | list[str]]:
    """
    Scans directories for netCDF (.nc) files, checks file integrity, 
    and generates a report for faulty files. Returns comprehensive information
    about netCDF files and their status.

    Parameters
    ----------
    search_path : str | list[str] | Path
        The directory or list of directories to scan for .nc files.
    
    Returns
    -------
    dict
        A dictionary containing:
        - 'total_dirs': Number of directories containing faulty files
        - 'total_files': Total number of netCDF files scanned
        - 'faulty_files': List of faulty netCDF file paths
        - 'faulty_count': Total number of faulty netCDF files
        - 'faulty_by_dir': Dictionary mapping directories to their faulty files

    Raises
    ------
    TypeError
        If search_path is not str, list, or Path.
    ValueError
        If search_path is empty or contains invalid paths.
    FileNotFoundError
        If any specified search path doesn't exist.

    Example
    -------
    # Example: Scan and check file integrity, generate a report for faulty files
    result = scan_ncfiles("/path/to/scan")
    print(f"Faulty files: {result['faulty_files']}, Count: {result['faulty_count']}")
    """
    # Parameter validation
    if not isinstance(search_path, (str, list, Path)):
        raise TypeError("search_path must be a string, list of strings, or Path object")
    
    # Convert to list and flatten if necessary
    if isinstance(search_path, (str, Path)):
        search_paths = [str(search_path)]
    else:
        search_paths = flatten_list([str(p) for p in search_path])
    
    # Validate paths
    if not search_paths:
        raise ValueError("search_path cannot be empty")
    
    for path in search_paths:
        if not isinstance(path, str) or not path.strip():
            raise ValueError("All search paths must be non-empty strings")
        
        if not Path(path).exists():
            raise FileNotFoundError(f"Search path does not exist: {path}")
        
        if not Path(path).is_dir():
            raise ValueError(f"Search path must be a directory: {path}")
    
    # Import here to avoid circular imports
    from paramlib.global_parameters import CLIMATE_FILE_EXTENSIONS
        
    # Step 1: Search for all netCDF files #
    #######################################
    all_files = []
    for path in search_paths:
        files_in_path = find_files(CLIMATE_FILE_EXTENSIONS[0], path)
        all_files.extend(files_in_path)
    
    if not all_files:
        print("No netCDF files found in the specified directories")
        return {
            'total_dirs': 0,
            'total_files': 0,
            'faulty_files': [],
            'faulty_count': 0,
            'faulty_by_dir': {}
        }
    
    # Step 2: Check each file's integrity and collect faulty files  #
    #################################################################
    file_vs_err_list = []
    for idx, file in enumerate(all_files, start=1):
        format_args_scan_progress = (idx, len(all_files), file)
        print_format_string(SCAN_PROGRESS_TEMPLATE, format_args_scan_progress)
        try:
            ncfile_integrity_status(file)
        except Exception as ncf_err:
            err_tuple = (file, str(ncf_err))
            file_vs_err_list.append(err_tuple)
                
    # Step 3: Find directories containing faulty files #
    ####################################################
    dir_list = _unique_sorted([get_obj_specs(err_tuple[0], "parent") for err_tuple in file_vs_err_list])
    
    # Step 4: Group faulty files by directory
    file_vs_errs_dict = {dirc: [err_tuple for err_tuple in file_vs_err_list 
                                if get_obj_specs(err_tuple[0], "parent")==dirc]
                         for dirc in dir_list}
        
    # Step 5: Generate report #
    ###########################
    
    # Statistics #
    total_dirs = len(dir_list)
    total_files = len(all_files)
    total_faulties = sum(len(lst) for lst in file_vs_errs_dict.values())
    
    # Report generation #
    with open(REPORT_FILE_PATH, "w") as report:
        report.write(REPORT_INFO_TEMPLATE.format(*(total_dirs, total_files, total_faulties)))
        
        for dirc in file_vs_errs_dict.keys():
            format_args_dir_info = (dirc, len(file_vs_errs_dict[dirc]))
            report.write(format_string(string_underliner(DIR_INFO_TEMPLATE, format_args_dir_info), "="))
            for values in file_vs_errs_dict[dirc]:
                report.write(format_string(FILE_INFO_WRITING_TEMPLATE, values))
    
    # Return comprehensive results
    return {
        'total_dirs': total_dirs,
        'total_files': total_files,
        'faulty_files': [err_tuple[0] for err_tuple in file_vs_err_list],
        'faulty_count': total_faulties,
        'faulty_by_dir': file_vs_errs_dict
    }

# Auxiliary functions #
#-#-#-#-#-#-#-#-#-#-#-#

def ncfile_integrity_status(ncfile_name: str | Path) -> xr.Dataset:
    """
    Checks the integrity of a given netCDF file by attempting to open it with xarray.

    This function tries to open the specified netCDF file using `xarray.open_dataset`.
    If the file is successfully opened, it returns the dataset before closing it.
    If an error occurs during this process, it delegates the exception
    raise to the output of xarray.dataset class.
    
    Parameters
    ----------
    ncfile_name : str | Path
        Path to the netCDF file to be checked.

    Returns
    -------
    xarray.Dataset
        The opened dataset if successful.

    Raises
    ------
    TypeError
        If ncfile_name is not str or Path.
    ValueError
        If the file path is empty or invalid.
    FileNotFoundError
        If the file doesn't exist.
    OSError
        Raised if the file cannot be found, opened, or there are issues with file permissions.
    ValueError
        Raised if the file is successfully opened but is not a valid netCDF file or has 
        an unsupported format.
    RuntimeError
        Raised for internal errors within the netCDF4 or h5py libraries, such as when 
        reading compressed data fails.
    IOError
        Raised for input/output errors at the system level, such as file corruption 
        or disk read failures.
    KeyError
        Raised in rare cases when essential variables or attributes required for reading 
        the file are missing or invalid.
    """
    # Parameter validation
    if not isinstance(ncfile_name, (str, Path)):
        raise TypeError("ncfile_name must be a string or Path object")
    
    ncfile_path = Path(ncfile_name)
    
    if not str(ncfile_path).strip():
        raise ValueError("File path cannot be empty")
    
    if not ncfile_path.exists():
        raise FileNotFoundError(f"NetCDF file not found: {ncfile_path}")
    
    if not ncfile_path.is_file():
        raise ValueError(f"Path must be a file, not a directory: {ncfile_path}")
    
    # Check file extension
    if not str(ncfile_path).lower().endswith(('.nc', '.netcdf')):
        print(f"Warning: File {ncfile_path} may not be a netCDF file based on extension")
    
    try:
        ds = xr.open_dataset(ncfile_path)
        return ds
    except Exception as e:
        raise type(e)(f"Failed to open netCDF file {ncfile_path}: {str(e)}")
    finally:
        if 'ds' in locals():
            ds.close()

#--------------------------#
# Parameters and constants #
#--------------------------#

# Directory from where this code is being called #
CODE_CALL_DIR = os.getcwd()

# Template strings #
#------------------#

# File scanning progress information strings #
SCAN_PROGRESS_TEMPLATE =\
"""
File number: {} out of {}
File name: {}
"""

DIR_INFO_TEMPLATE = """\nDirectory: {} | Faulty files in this directory: {}"""
FILE_INFO_WRITING_TEMPLATE = """\nFile: {} -> {}\n"""

# Report results
REPORT_FN_NOEXT = "faulty_netcdf_file_report"
REPORT_FILE_PATH = f"{CODE_CALL_DIR}/{REPORT_FN_NOEXT}.txt"
REPORT_INFO_TEMPLATE =\
"""
+--------------------------------+
|Faulty NETCDF format file report|
+--------------------------------+
·Total directories scanned : {}
·Total files scanned: {}    
·Total faulty files: {}

Faulty files
+----------+
"""
