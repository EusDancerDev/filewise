#! /usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------#
# Import modules #
#----------------#

import os
from pathlib import Path

#------------------------#
# Import project modules #
#------------------------#

from filewise.file_operations.ops_handler import move_files
from filewise.file_operations.path_utils import find_dirs_with_files, find_files
from filewise.xarray_utils.file_utils import ncfile_integrity_status
from filewise.xarray_utils.patterns import (
    find_coordinate_variables,
    get_latlon_bounds,
    get_latlon_deltas,
    get_times
)
from paramlib.global_parameters import CLIMATE_FILE_EXTENSIONS
from pygenutils.strings.text_formatters import format_string, string_underliner
from pygenutils.time_handling.date_and_time_utils import find_dt_key

#-------------------------#
# Define custom functions #
#-------------------------#

# Data extractors #
#-----------------#

def extract_latlon_bounds(delta_roundoff: int, value_roundoff: int) -> None:
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

    Raises
    ------
    TypeError
        If roundoff parameters are not integers.
    ValueError
        If roundoff parameters are negative.

    Notes
    -----
    - The extracted latitude and longitude arrays, their dimensions,
      and deltas are saved in a report file.
    - If any files are faulty or cannot be processed, relevant error information 
      is recorded in the report.
    """
    # Parameter validation
    if not isinstance(delta_roundoff, int):
        raise TypeError("delta_roundoff must be an integer")
    
    if not isinstance(value_roundoff, int):
        raise TypeError("value_roundoff must be an integer")
    
    if delta_roundoff < 0:
        raise ValueError("delta_roundoff must be non-negative")
    
    if value_roundoff < 0:
        raise ValueError("value_roundoff must be non-negative")
    
    nc_dirs = find_dirs_with_files(EXTENSIONS[0], search_path=CODE_CALL_DIR)
    
    for dir_num, dir_name in enumerate(nc_dirs, start=1):
        nc_files = find_files(EXTENSIONS[0], dir_name, match_type="ext", top_path_only=True)
        
        with open(COORD_INFO_FNAME, "w") as report:
            if nc_files:
                for file_num, nc_file in enumerate(nc_files, start=1):
                    print(f"Processing file {file_num} out of {len(nc_files)} "
                          f"in directory {dir_num} out of {len(nc_dirs)}...")
                    report.write(format_string(string_underliner(DIR_INFO_TEMPLATE, dir_name), "+"))
                    
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
                            try:
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
                                
                                report.write(format_string(LATLON_INFO_TEMPLATE, format_args_latlon_bounds))
                            except Exception as e:
                                report.write(f"ERROR PROCESSING COORDINATES IN FILE '{nc_file}': {e}\n")
                            
                move_files(COORD_INFO_FNAME,
                           input_directories=".", 
                           destination_directories=dir_name, 
                           match_type="glob")
            else:
                report.write(f"No netCDF files in directory {dir_name}\n")
                move_files(COORD_INFO_FNAME,
                           input_directories=".", 
                           destination_directories=dir_name, 
                           match_type="glob")


def extract_time_bounds() -> None:
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
    nc_dirs = find_dirs_with_files(EXTENSIONS[0], search_path=CODE_CALL_DIR)
    
    for dir_num, dir_name in enumerate(nc_dirs, start=1):
        nc_files = find_files(EXTENSIONS[0], dir_name, match_type="ext", top_path_only=True)
        
        with open(DATE_RANGE_INFO_FNAME, "w") as report:
            if nc_files:
                for file_num, nc_file in enumerate(nc_files, start=1):
                    print(f"Processing file {file_num} out of {len(nc_files)} "
                          f"in directory {dir_num} out of {len(nc_dirs)}...")
                    report.write(format_string(string_underliner(DIR_INFO_TEMPLATE, dir_name), "+"))
                    
                    try:
                        ncfile_integrity_status(nc_file)
                    except Exception as ncf_err:
                        report.write(f"FAULTY FILE '{nc_file}': {ncf_err}\n")
                    else:
                        try:
                            time_var = find_dt_key(nc_file)
                        except Exception as time_err:
                            report.write(f"ERROR IN FILE '{nc_file}': {time_err}\n")
                        else:
                            try:
                                times = get_times(nc_file, time_var)                            
                                format_args_time_periods = (
                                    nc_file, 
                                    times[0].values,
                                    times[-1].values, 
                                    len(times)
                                    )
                                
                                report.write(format_string(PERIOD_INFO_TEMPLATE, format_args_time_periods))
                            except Exception as e:
                                report.write(f"ERROR PROCESSING TIME DATA IN FILE '{nc_file}': {e}\n")
                            
                move_files(DATE_RANGE_INFO_FNAME,
                           input_directories=".", 
                           destination_directories=dir_name, 
                           match_type="glob")
            else:
                report.write(f"No netCDF files in directory {dir_name}\n")
                move_files(DATE_RANGE_INFO_FNAME,
                           input_directories=".", 
                           destination_directories=dir_name, 
                           match_type="glob")


def extract_time_formats() -> None:
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

    nc_dirs = find_dirs_with_files(EXTENSIONS[0], search_path=CODE_CALL_DIR)
    
    for dir_num, dir_name in enumerate(nc_dirs, start=1):
        nc_files = find_files(EXTENSIONS[0], dir_name, match_type="ext", top_path_only=True)
        
        with open(TIME_FORMATS_FILE_NAME, "w") as report:
            if nc_files:
                for file_num, nc_file in enumerate(nc_files, start=1):
                    print(f"Processing file {file_num} out of {len(nc_files)} "
                          f"in directory {dir_num} out of {len(nc_dirs)}...")
                    report.write(format_string(string_underliner(DIR_INFO_TEMPLATE, dir_name), "+"))
                    
                    try:
                        ncfile_integrity_status(nc_file)
                    except Exception as ncf_err:
                        report.write(f"FAULTY FILE '{nc_file}': {ncf_err}\n")
                    else:
                        try:
                            time_var = find_dt_key(nc_file)
                        except Exception as time_err:
                            report.write(f"ERROR IN FILE '{nc_file}': {time_err}\n")
                        else:
                            try:
                                times = get_times(nc_file, time_var)
                                format_args_time_formats = (
                                    nc_file, 
                                    times.values, 
                                    len(times)
                                    )
                                report.write(format_string(TIME_FORMAT_INFO_TEMPLATE, format_args_time_formats))
                            except Exception as e:
                                report.write(f"ERROR PROCESSING TIME FORMATS IN FILE '{nc_file}': {e}\n")
                                
                move_files(TIME_FORMATS_FILE_NAME,
                           input_directories=".", 
                           destination_directories=dir_name, 
                           match_type="glob")
            else:
                report.write(f"No netCDF files in directory {dir_name}\n")
                move_files(TIME_FORMATS_FILE_NAME,
                           input_directories=".", 
                           destination_directories=dir_name, 
                           match_type="glob")
            
# File regridding #
#-----------------#

def netcdf_regridder(ds_in: 'xr.Dataset', ds_image: 'xr.Dataset', regrid_method: str = "bilinear") -> 'xr.Dataset':    
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
        
    Raises
    ------
    TypeError
        If input datasets are not xarray.Dataset objects.
    ValueError
        If regrid_method is not valid.
    ImportError
        If xesmf package is not available.
    RuntimeError
        If regridding operation fails.
    """
    # Parameter validation
    try:
        import xarray as xr
        if not isinstance(ds_in, xr.Dataset):
            raise TypeError("ds_in must be an xarray.Dataset")
        
        if not isinstance(ds_image, xr.Dataset):
            raise TypeError("ds_image must be an xarray.Dataset")
    except ImportError:
        raise ImportError("xarray package is required but not available")
    
    if not isinstance(regrid_method, str):
        raise TypeError("regrid_method must be a string")
    
    if regrid_method not in REGRID_METHOD_LIST:
        raise ValueError("Invalid regridding method.\n"
                         f"Choose one from {REGRID_METHOD_LIST}.")        
    
    try:
        import xesmf as xe
    except ImportError:
        raise ImportError("xesmf package is required for regridding but not available")
    
    try:
        regridder = xe.Regridder(ds_in, ds_image, regrid_method)
        ds_out = regridder(ds_in)
        return ds_out    
    except Exception as e:
        raise RuntimeError(f"Regridding operation failed: {e}")

#--------------------------#
# Parameters and constants #
#--------------------------#

# Directory from where this code is being called #
CODE_CALL_DIR = os.getcwd()

# File extensions #
EXTENSIONS = CLIMATE_FILE_EXTENSIONS[::3]

# Main file names #
COORD_INFO_FNAME = "latlon_bounds.txt"
DATE_RANGE_INFO_FNAME = "period_bounds.txt"
TIME_FORMATS_FILE_NAME = "time_formats.txt"

# Regridding method options #
REGRID_METHOD_LIST = [
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
LATLON_INFO_TEMPLATE = \
"""=========================================================
·File: {}

·Latitudes:
 {}

·Longitudes:
 {}

-Latitude-longitude array dimensions = {} x {}
-Latitude-longitude array delta = ({}, {})
    
"""

PERIOD_INFO_TEMPLATE = \
"""=========================================================
·File: {}
·Time range: {} -- {}
-Range length = {}

"""
    
TIME_FORMAT_INFO_TEMPLATE = \
"""=========================================================
·File: {}
    
·Time array:
 {}

-Array length = {}
"""

# File scanning progress information strings #
DIR_INFO_TEMPLATE = """\nDirectory: {}"""
