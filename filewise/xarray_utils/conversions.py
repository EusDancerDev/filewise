#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------#
# Import modules #
#----------------#

import xarray as xr
from pathlib import Path

#------------------------#
# Import project modules #
#------------------------#

from filewise.xarray_utils.xarray_obj_handler import _save_ds_as_nc
from paramlib.global_parameters import CLIMATE_FILE_EXTENSIONS
from pygenutils.arrays_and_lists.conversions import flatten_to_string
from pygenutils.arrays_and_lists.data_manipulation import flatten_list
from pygenutils.operative_systems.os_operations import exit_info, run_system_command
from pygenutils.strings.string_handler import (
    find_substring_index,
    get_obj_specs,
    modify_obj_specs
)

#------------------#
# Define functions #
#------------------#

# Xarray objects #
#----------------#

def grib2nc(
        grib_file_list: str | list[str], 
        on_shell: bool = False, 
        option_str: str | None = None,
        capture_output: bool = False,
        return_output_name: bool = False,
        encoding: str = "utf-8",
        shell: bool = True) -> None:
    """
    Converts a GRIB file or list of GRIB files to netCDF format. The conversion
    can be executed either via shell commands or programmatically using xarray.
    
    Parameters
    ----------
    grib_file_list : str | list[str]
        The file path(s) of the GRIB file(s) to be converted.
    on_shell : bool, optional
        If True, the conversion will be handled through shell commands using 
        the 'grib_to_netcdf' tool. If False, the conversion will be done 
        programmatically using xarray.
    option_str : str, optional
        Additional options to pass to the shell command for 'grib_to_netcdf'. 
        This parameter is only used if 'on_shell' is set to True.
    capture_output : bool, optional
        Whether to capture the command output. Default is False.
    return_output_name : bool, optional
        Whether to return file descriptor names. Default is False.
    encoding : str, optional
        Encoding to use when decoding command output. Default is "utf-8".
    shell : bool, optional
        Whether to execute the command through the shell. Default is True.
        
    Returns
    -------
    None
        Converts the GRIB file(s) to netCDF format and saves the output 
        netCDF file(s) in the same directory as the GRIB files.

    Raises
    ------
    TypeError
        If grib_file_list is not str or list of str.
    ValueError
        If any GRIB file path is invalid or empty.
    FileNotFoundError
        If any GRIB file doesn't exist.

    Notes
    -----
    - When 'on_shell' is True, the function builds and runs a shell command 
      that calls the 'grib_to_netcdf' tool, with optional flags.
    - When 'on_shell' is False, xarray is used to directly open the GRIB file 
      and convert it to netCDF format.
    - The function will prompt for input in the case of multiple GRIB files if 
      'on_shell' is True.
    """
    
    # Parameter validation
    if not isinstance(grib_file_list, (str, list)):
        raise TypeError("grib_file_list must be a string or list of strings")
    
    # Flatten nested lists for defensive programming
    if isinstance(grib_file_list, list):
        grib_file_list = flatten_list(grib_file_list)
        
        # Validate all items are strings
        if not all(isinstance(item, str) for item in grib_file_list):
            raise TypeError("All items in grib_file_list must be strings")
        
        # Check for empty strings
        if not all(item.strip() for item in grib_file_list):
            raise ValueError("All GRIB file paths must be non-empty strings")
    else:
        # Single string validation
        if not isinstance(grib_file_list, str) or not grib_file_list.strip():
            raise ValueError("GRIB file path must be a non-empty string")
    
    # Check file existence
    files_to_check = [grib_file_list] if isinstance(grib_file_list, str) else grib_file_list
    for grib_file in files_to_check:
        if not Path(grib_file).exists():
            raise FileNotFoundError(f"GRIB file not found: {grib_file}")
        
        # Check if file has expected GRIB extension
        if not any(grib_file.lower().endswith(ext.lower()) for ext in ['.grib', '.grb', '.grib2', '.grb2']):
            print(f"Warning: File {grib_file} may not be a GRIB file based on extension")

    # Shell-based conversion #
    #-#-#-#-#-#-#-#-#-#-#-#-#-
    
    if on_shell:
        # Handle single GRIB file
        if isinstance(grib_file_list, str):
            nc_file_new = modify_obj_specs(grib_file_list, "ext", EXTENSIONS[0])
        
        # Handle list of GRIB files
        else:
            grib_allfile_info_str = flatten_to_string(grib_file_list)
            
            # Prompt user for the netCDF file name without extension
            nc_file_new_noext = input("Please introduce a name "
                                      "for the netCDF file, "
                                      "WITHOUT THE EXTENSION: ")
            
            # Validate the file name using RegEx
            allowed_minimum_char_idx = find_substring_index(nc_file_new_noext,
                                                            REGEX_GRIB2NC,
                                                            advanced_search=True)
            
            while allowed_minimum_char_idx == -1:
                print("Invalid file name.\nIt can contain alphanumeric characters, "
                      "as well as the following non-word characters: {. _ -}")
                nc_file_new_noext = input("Please introduce a valid name: ")
                allowed_minimum_char_idx = find_substring_index(nc_file_new_noext,
                                                                REGEX_GRIB2NC,
                                                                advanced_search=True)
            
            # Modify the file name to have the .nc extension
            nc_file_new = modify_obj_specs(nc_file_new_noext,
                                                 obj2modify="ext",
                                                 new_obj=EXTENSIONS[0])
        
        # Construct the shell command for conversion
        grib2nc_template = "grib_to_netcdf "
        if option_str:
            grib2nc_template += f"{option_str} "
        grib2nc_template += f"-o {nc_file_new} {grib_allfile_info_str}"
        
        # Execute the shell command
        try:
            process_exit_info = run_system_command(
                grib2nc_template,
                capture_output=capture_output,
                return_output_name=return_output_name,
                encoding=encoding,
                shell=shell
            )
            # Call exit_info with parameters based on capture_output
            exit_info(
                process_exit_info,
                check_stdout=True,
                check_stderr=True,
                check_return_code=True
            )
        except Exception as e:
            raise RuntimeError(f"Shell command execution failed: {e}")

    # Programmatic conversion #
    #-#-#-#-#-#-#-#-#-#-#-#-#-#
    
    else:
        # Ensure grib_file_list is a list
        if isinstance(grib_file_list, str):
            grib_file_list = [grib_file_list]

        # Convert each GRIB file in the list to netCDF
        for grib_file in grib_file_list:
            try:
                grib_file_noext = get_obj_specs(grib_file, "name_noext", EXTENSIONS[0])
                ds = xr.open_dataset(grib_file, engine="cfgrib")
                _save_ds_as_nc(ds, grib_file_noext)
                print(f"Successfully converted {grib_file} to netCDF format")
            except Exception as e:
                print(f"Error converting {grib_file}: {e}")
                raise

            
#--------------------------#
# Parameters and constants #
#--------------------------#

# Valid file extensions #
EXTENSIONS = CLIMATE_FILE_EXTENSIONS[::3]
  
# RegEx control for GRIB-to-netCDF single file name #
REGEX_GRIB2NC = r"^[a-zA-Z\d\._-]$"
