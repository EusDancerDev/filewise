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

#-----------------------#
# Import custom modules #
#-----------------------#

from pyutils.parameters_and_constants.global_parameters import climate_file_extensions
from pyutils.string_handler import information_output_formatters, string_handler
from pyutils.filewise.file_operations import path_utils

# Create aliases #
#----------------#

find_files = path_utils.find_files

format_string = information_output_formatters.format_string
print_format_string = information_output_formatters.print_format_string
string_underliner = information_output_formatters.string_underliner

get_obj_specs = string_handler.get_obj_specs

#-------------------------#
# Define custom functions #
#-------------------------#

# netCDF file searching #
#-----------------------#

# Main method #
#-#-#-#-#-#-#-#
    
def scan_ncfiles(search_path):
    """
    Scans directories for netCDF (.nc) files, optionally checks file integrity, 
    and can generate a report for faulty files. Returns netCDF file paths, 
    directories containing netCDF files, or both, depending on user configuration.

    Parameters
    ----------
    search_path : str or list
        The directory or list of directories to scan for .nc files.
    
    return_files : bool, optional (default=True)
        If True, returns a list of netCDF file paths found within the specified directories.
    
    return_dirs : bool, optional (default=False)
        If True, returns a list of directories containing netCDF files.
    
    check_integrity : bool, optional (default=False)
        If True, checks the integrity of each .nc file using xarray.
        Faulty files are flagged and can be reported.
        This report included detailed progress information (file name, number, and directory).
    
    create_report : bool, optional (default=False)
        If True, generates a report listing all faulty netCDF files (requires `check_integrity=True`).
    
    verbose : bool, optional (default=False)
        If True, prints detailed progress information (file name, number, and directory) during the scan.
        Note: `verbose` and `extra_verbose` cannot be True at the same time.
 
    Returns
    -------
    result : dict
        A dictionary containing the requested data based on the input parameters:
        - 'files': List of netCDF file paths (if `return_files=True`).
        - 'dirs': List of directories containing netCDF files (if `return_dirs=True`).
        - 'faulty_files': List of faulty netCDF file paths (if `check_integrity=True`).
        - 'faulty_count': Total number of faulty netCDF files (if `check_integrity=True`).

    Example
    -------
    # Example 1: Return a list of netCDF files found in the directory
    result = scan_netCDF_files("/path/to/scan", return_files=True)
    print(result['files'])

    # Example 2: Scan and check file integrity, generate a report for faulty files
    result = scan_netCDF_files("/path/to/scan", check_integrity=True, create_report=True)
    print(f"Faulty files: {result['faulty_files']}, Count: {result['faulty_count']}")

    # Example 3: Return both file paths and directories containing netCDF files
    result = scan_netCDF_files("/path/to/scan", return_files=True, return_dirs=True)
    print(result['files'], result['dirs'])
    """
        
    # Step 1: Search for all netCDF files #
    #######################################
    all_files = find_files(extensions[0], search_path)
    
    # Step 2: Check each file's integrity and collect faulty files  #
    #################################################################
    file_vs_err_list = []
    for idx, file in enumerate(all_files, start=1):
        arg_tuple_scanf = (idx, len(all_files), file)
        print_format_string(scan_progress_str, arg_tuple_scanf)
        try:
            ncfile_integrity_status(file)
        except Exception as ncf_err:
            err_tuple = (file, str(ncf_err))
            file_vs_err_list.append(err_tuple)
                
    # Step 3: Find directories containing faulty files #
    ####################################################
    dir_list = np.unique([get_obj_specs(err_tuple[0], "parent") for err_tuple in file_vs_err_list])
    
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
    with open(report_file_path, "w") as report:
        report.write(report_info_str.format(*(total_dirs, total_files, total_faulties)))
        
        for dirc in file_vs_errs_dict.keys():
            scandir_arg_tuple = (dirc, len(file_vs_errs_dict[dirc]))
            report.write(format_string(string_underliner(dir_info_str, scandir_arg_tuple), "="))
            for values in file_vs_errs_dict[dirc]:
                report.write(format_string(file_info_writing_str, values))


# Helpers #
#-#-#-#-#-#

def ncfile_integrity_status(ncfile_name):
    """
    Checks the integrity of a given netCDF file by attempting to open it with xarray.

    This method tries to open the specified netCDF file using `xarray.open_dataset`.
    If the file is successfully opened, it is closed and the function completes without
    returning anything. If an error occurs during this process, it delegates the exception
    raise to the output of xarray.dataset class.
    
    Parameters
    ----------
    ncfile_name : str
        Path to the netCDF file to be checked.

    Returns
    -------
    str
        A string representation of the error message if an exception occurs.
        If the file is successfully opened and closed, no value is returned (i.e., None).

    Raises
    ------
    Common exceptions are:
        
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
    ds = xr.open_dataset(ncfile_name)
    ds.close()

#--------------------------#
# Parameters and constants #
#--------------------------#

# Directory from where this code is being called #
code_call_dir = os.getcwd()

# File extensions #
extensions = climate_file_extensions[::3]

# Preformatted strings #
#----------------------#

# File scanning progress information strings #
scan_progress_str =\
"""
File number: {} out of {}
File name: {}
"""

dir_info_str = """\nDirectory: {} | Faulty files in this directory: {}"""
file_info_writing_str = """\nFile: {} -> {}\n"""

# Report results
report_fn_noext = "faulty_netcdf_file_report"
report_file_path = f"{code_call_dir}/{report_fn_noext}.txt"
report_info_str =\
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
