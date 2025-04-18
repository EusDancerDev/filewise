#! /usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------#
# Import modules #
#----------------#

import os

#-----------------------#
# Import custom modules #
#-----------------------#

from filewise.file_operations.ops_handler import move_files
from filewise.file_operations.path_utils import find_dirs_with_files, find_files
from filewise.xarray_utils.file_utils import ncfile_integrity_status
from filewise.xarray_utils.patterns import (
    find_coordinate_variables,
    get_latlon_bounds,
    get_latlon_deltas,
    get_times
)
from paramlib.global_parameters import climate_file_extensions
from pygenutils.strings.text_formatters import format_string, string_underliner
from pygenutils.time_handling.time_utils import find_time_key

#-------------------------#
# Define custom functions #
#-------------------------#

# Data extractors #
#-----------------#

def extract_latlon_bounds(delta_roundoff, value_roundoff):
    """
    Extract latitude and longitude bounds from netCDF files.

    Parameters
    ----------
    delta_roundoff : int
        Number of decimal places to round off the delta between latitude and longitude points.
    value_roundoff : int
        Number of decimal places to round off the latitude and longitude values.

    Returns
    -------
    None

    Notes
    -----
    - The extracted latitude and longitude arrays, their dimensions,
      and deltas are saved in a report file.
    - If any files are faulty or cannot be processed, relevant error information 
      is recorded in the report.
    """
    nc_dirs = find_dirs_with_files(extensions[0], search_path=code_call_dir)
    
    for dir_num, dir_name in enumerate(nc_dirs, start=1):
        nc_files = find_files(extensions[0], dir_name, match_type="ext", top_path_only=True)
        
        with open(coord_info_fname, "w") as report:
            if nc_files:
                for file_num, nc_file in enumerate(nc_files, start=1):
                    print(f"Processing file {file_num} out of {len(nc_files)} "
                          f"in directory {dir_num} out of {len(nc_dirs)}...")
                    report.write(format_string(string_underliner(dir_info_template, dir_name), "+"))
                    
                    try:
                        ncfile_integrity_status(nc_file)
                    except Exception as ncf_err:
                        report.write(f"FAULTY FILE '{nc_file}': {ncf_err}\n")
                    else:
                        try:
                            coord_vars = find_coordinate_variables(nc_file)
                        except Exception as coord_err:
                            report.write(f"ERROR IN FILE '{nc_file}': {coord_err}\n")
                        else:
                            lats, lons = get_latlon_bounds(nc_file, coord_vars[0], coord_vars[1], value_roundoff)
                            lat_delta, lon_delta = get_latlon_deltas(lats, lons, delta_roundoff)
                            
                            format_args_latlon_bounds = (
                                nc_file, 
                                lats,
                                lons, 
                                len(lats), 
                                len(lons), 
                                lat_delta, 
                                lon_delta
                                )
                            
                            report.write(format_string(latlon_info_template, format_args_latlon_bounds))
                            move_files(coord_info_fname,
                                       input_directories=".", 
                                       destination_directories=dir_name, 
                                       match_type="glob")
            else:
                report.write(f"No netCDF files in directory {dir_name}\n")
                move_files(coord_info_fname,
                           input_directories=".", 
                           destination_directories=dir_name, 
                           match_type="glob")


def extract_time_bounds():
    """
    Extract the time bounds (start and end times) from netCDF files.

    Parameters
    ----------
    None

    Returns
    -------
    None

    Notes
    -----
    - The time range (start and end times) and the total number of time records 
      are saved in a report file.
    - If any files are faulty or cannot be processed, relevant error information 
      is recorded in the report.
    """
    nc_dirs = find_dirs_with_files(extensions[0], search_path=code_call_dir)
    
    for dir_num, dir_name in enumerate(nc_dirs, start=1):
        nc_files = find_files(extensions[0], dir_name, match_type="ext", top_path_only=True)
        
        with open(date_range_info_fname, "w") as report:
            if nc_files:
                for file_num, nc_file in enumerate(nc_files, start=1):
                    print(f"Processing file {file_num} out of {len(nc_files)} "
                          f"in directory {dir_num} out of {len(nc_dirs)}...")
                    report.write(format_string(string_underliner(dir_info_template, dir_name), "+"))
                    
                    try:
                        ncfile_integrity_status(nc_file)
                    except Exception as ncf_err:
                        report.write(f"FAULTY FILE '{nc_file}': {ncf_err}\n")
                    else:
                        try:
                            time_var = find_time_key(nc_file)
                        except Exception as time_err:
                            report.write(f"ERROR IN FILE '{nc_file}': {time_err}\n")
                        else:
                            times = get_times(nc_file, time_var)                            
                            format_args_time_periods = (
                                nc_file, 
                                times[0].values,
                                times[-1].values, 
                                len(times)
                                )
                            
                            report.write(format_string(period_info_template, format_args_time_periods))
                            move_files(date_range_info_fname,
                                       input_directories=".", 
                                       destination_directories=dir_name, 
                                       match_type="glob")
            else:
                report.write(f"No netCDF files in directory {dir_name}\n")
                move_files(date_range_info_fname,
                           input_directories=".", 
                           destination_directories=dir_name, 
                           match_type="glob")


def extract_time_formats():
    """
    Extract the time formats from netCDF files.

    Parameters
    ----------
    None

    Returns
    -------
    None

    Notes
    -----
    - The extracted time formats and the total number of time records are saved 
      in a report file.
    - If any files are faulty or cannot be processed, relevant error information 
      is recorded in the report.
    """

    nc_dirs = find_dirs_with_files(extensions[0], search_path=code_call_dir)
    
    for dir_num, dir_name in enumerate(nc_dirs, start=1):
        nc_files = find_files(extensions[0], dir_name, match_type="ext", top_path_only=True)
        
        with open(time_formats_file_name, "w") as report:
            if nc_files:
                for file_num, nc_file in enumerate(nc_files, start=1):
                    print(f"Processing file {file_num} out of {len(nc_files)} "
                          f"in directory {dir_num} out of {len(nc_dirs)}...")
                    report.write(format_string(string_underliner(dir_info_template, dir_name), "+"))
                    
                    try:
                        ncfile_integrity_status(nc_file)
                    except Exception as ncf_err:
                        report.write(f"FAULTY FILE '{nc_file}': {ncf_err}\n")
                    else:
                        try:
                            time_var = find_time_key(nc_file)
                        except Exception as time_err:
                            report.write(f"ERROR IN FILE '{nc_file}': {time_err}\n")
                        else:
                            times = get_times(nc_file, time_var)
                            format_args_time_formats = (
                                nc_file, 
                                times.values, 
                                len(times)
                                )
                            report.write(format_string(time_format_info_template, format_args_time_formats))
                            move_files(time_formats_file_name,
                                       input_directories=".", 
                                       destination_directories=dir_name, 
                                       match_type="glob")
            else:
                report.write(f"No netCDF files in directory {dir_name}\n")
                move_files(time_formats_file_name,
                           input_directories=".", 
                           destination_directories=dir_name, 
                           match_type="glob")
            
# File regridding #
#-----------------#

def netcdf_regridder(ds_in, ds_image, regrid_method="bilinear"):    
    
    """
    Function that regrids a xarray Dataset to that of the desired Dataset. 
    It is similar to CDO but more intuitive and
    easier to understand, supported by Python.
    
    Parameters
    ----------
    ds_in : xarray.Dataset
        Input xarray data set
    ds_image : xarray.Dataset
        Xarray data set with grid specifications to which apply on ds_in.
    regrid_method : {'bilinear', 'conservative', 'nearest_s2d', 'nearest_d2s', 'patch'}
        Regridding method. Defaults 'bilinear'.
    
    Returns
    -------
    ds_out : xarray.Dataset
        Output data set regridded according to the grid specs of ds_in.
    """
    import xesmf as xe
    if regrid_method not in regrid_method_list:
        raise ValueError("Invalid regridding method.\n"
                         f"Choose one from {regrid_method_list}.")        
    else:
        regridder = xe.Regridder(ds_in, ds_image, regrid_method)
        ds_out = regridder(ds_in)
        return ds_out    

#--------------------------#
# Parameters and constants #
#--------------------------#

# Directory from where this code is being called #
code_call_dir = os.getcwd()

# File extensions #
extensions = climate_file_extensions[::3]

# Main file names #
coord_info_fname = "latlon_bounds.txt"
date_range_info_fname = "period_bounds.txt"
time_formats_file_name = "time_formats.txt"

# Regridding method options #
regrid_method_list = [
    "bilinear",
    "conservative",
    "conservative_normed",
    "nearest_s2d",
    "nearest_d2s",
    "patch"
    ]

# Template strings #
#------------------#

# Main parameter scanning info strings #
latlon_info_template = \
"""=========================================================
·File: {}

·Latitudes:
 {}

·Longitudes:
 {}

-Latitude-longitude array dimensions = {} x {}
-Latitude-longitude array delta = ({}, {})
    
"""

period_info_template = \
"""=========================================================
·File: {}
·Time range: {} -- {}
-Range length = {}

"""
    
time_format_info_template = \
"""=========================================================
·File: {}
    
·Time array:
 {}

-Array length = {}
"""

# File scanning progress information strings #
dir_info_template = """\nDirectory: {}"""
