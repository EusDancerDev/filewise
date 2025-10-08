#! /usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------#
# Import modules #
#----------------#

import numpy as np
import xarray as xr
from pathlib import Path

#------------------------#
# Import project modules #
#------------------------#

from filewise.xarray_utils.file_utils import ncfile_integrity_status
from paramlib.global_parameters import COMMON_DELIMITER_LIST
from pygenutils.arrays_and_lists.data_manipulation import flatten_list

#-------------------------#
# Define custom functions #
#-------------------------#            

# Dimension handlers #
#--------------------#

# Main functions #
#-#-#-#-#-#-#-#-#-

def get_file_dimensions(nc_file: str | xr.Dataset | Path) -> list[str] | str:
    """
    Extracts dimension names from a netCDF file or xarray.Dataset. In some cases,
    dimensions can also appear as variables, so this function ensures only
    dimensions are returned.

    Parameters
    ----------
    nc_file : str | Path | xarray.Dataset
        Either the path to the netCDF file or an already opened xarray.Dataset object.

    Returns
    -------
    dimension_names : str | list[str]
        A list of dimension names, or a single dimension name if only one is found.

    Raises
    ------
    TypeError
        If the input is not a string, Path, or xarray.Dataset object.
    ValueError
        If the file path is empty or invalid.
    FileNotFoundError
        If the file doesn't exist.
    """
    if isinstance(nc_file, (str, Path)):
        if not str(nc_file).strip():
            raise ValueError("File path cannot be empty")
        
        nc_path = Path(nc_file)
        if not nc_path.exists():
            raise FileNotFoundError(f"NetCDF file not found: {nc_path}")
        
        ncfile_integrity_status(nc_file)
        ds = xr.open_dataset(nc_file)
        close_dataset = True
    elif isinstance(nc_file, xr.Dataset):
        ds = nc_file
        close_dataset = False
    else:
        raise TypeError("Unsupported data file type. Expected str, Path, or xarray.Dataset.")

    try:
        dimlist = list(ds.dims)
        varlist = list(ds.variables)
        
        # Retain only those dimensions that are present among variables
        dimlist_nodim = [dim for dim in dimlist if dim in varlist]

        return dimlist_nodim[0] if len(dimlist_nodim) == 1 else dimlist_nodim
    finally:
        if close_dataset:
            ds.close()


def get_file_variables(nc_file: str | xr.Dataset | Path) -> list[str] | str:
    """
    Extracts variable names from a netCDF file or xarray.Dataset, excluding
    dimensions, as dimensions may also be present in the variable list.

    Parameters
    ----------
    nc_file : str | xarray.Dataset | Path
        Either the path to the netCDF file or an already opened xarray.Dataset object.

    Returns
    -------
    variable_names : str | list[str]
        A list of variable names, or a single variable name if only one is found.

    Raises
    ------
    TypeError
        If the input is not a string, Path, or xarray.Dataset object.
    ValueError
        If the file path is empty or invalid.
    FileNotFoundError
        If the file doesn't exist.
    """
    if isinstance(nc_file, (str, Path)):
        if not str(nc_file).strip():
            raise ValueError("File path cannot be empty")
        
        nc_path = Path(nc_file)
        if not nc_path.exists():
            raise FileNotFoundError(f"NetCDF file not found: {nc_path}")
        
        ncfile_integrity_status(nc_file)
        ds = xr.open_dataset(nc_file)
        close_dataset = True
    elif isinstance(nc_file, xr.Dataset):
        ds = nc_file
        close_dataset = False
    else:
        raise TypeError("Unsupported data file type. Expected str, Path, or xarray.Dataset.")

    try:
        varlist = list(ds.variables)
        dimlist = list(ds.dims)
        
        # Remove dimensions from the variable list
        varlist_nodim = [var for var in varlist if var not in dimlist]

        return varlist_nodim[0] if len(varlist_nodim) == 1 else varlist_nodim
    finally:
        if close_dataset:
            ds.close()


def get_model_list(path_list: list[str], split_pos: int, SPLIT_DELIM: str = "_") -> list[str]:
    """
    Extracts model names from a list of file paths or file names by splitting the file
    name at a specified position. The function can handle both absolute/relative paths 
    and file names, assuming they contain low bars ('_') as separators.

    Parameters
    ----------
    path_list : list[str]
        List of file paths (absolute or relative) or file names.
    split_pos : int
        Position in the split file name (after splitting by the delimiter) that contains
        the model name.
    SPLIT_DELIM : str, optional
        Delimiter used to split the file name. Default is "_".

    Returns
    -------
    unique_model_list : list[str]
        A list of unique model names extracted from the file paths.
        
    Raises
    ------
    TypeError
        If path_list is not a list or contains non-string elements.
    ValueError
        If path_list is empty, split_pos is negative, or SPLIT_DELIM is empty.
    IndexError
        If split_pos is beyond the available splits for any file.
    """
    # Parameter validation
    if not isinstance(path_list, list):
        raise TypeError("path_list must be a list")
    
    # Flatten nested lists for defensive programming
    path_list_flat = flatten_list(path_list)
    
    if not path_list_flat:
        raise ValueError("path_list cannot be empty")
    
    if not all(isinstance(path, str) for path in path_list_flat):
        raise TypeError("All items in path_list must be strings")
    
    if not all(path.strip() for path in path_list_flat):
        raise ValueError("All file paths must be non-empty strings")
    
    if not isinstance(split_pos, int) or split_pos < 0:
        raise ValueError("split_pos must be a non-negative integer")
    
    if not isinstance(SPLIT_DELIM, str) or not SPLIT_DELIM:
        raise ValueError("SPLIT_DELIM must be a non-empty string")

    # Handle paths with forward slashes to extract file names
    grib_file_list = [path.split("/")[-1] for path in path_list_flat]

    # Split file names by the delimiter and extract model names from the specified position
    model_list = []
    for f in grib_file_list:
        parts = f.split(SPLIT_DELIM)
        if split_pos >= len(parts):
            raise IndexError(f"split_pos {split_pos} is beyond available splits for file {f}")
        model_list.append(parts[split_pos])

    # Return unique model names
    unique_model_list = np.unique(model_list).tolist()
    return unique_model_list


def get_latlon_bounds(nc_file: str | xr.Dataset | Path, 
                      lat_dimension_name: str, 
                      lon_dimension_name: str, 
                      decimal_places: int = 3) -> tuple[np.ndarray, np.ndarray]:
    """
    Retrieves the latitude and longitude values from a netCDF file and rounds them 
    to the specified decimal precision.

    Parameters
    ----------
    nc_file : str | xarray.Dataset | Path
        Path to the netCDF file or an already opened xarray.Dataset object.
    lat_dimension_name : str
        Name of the latitude dimension in the dataset.
    lon_dimension_name : str
        Name of the longitude dimension in the dataset.
    decimal_places : int, optional
        Number of decimal places to round the latitude and longitude values. Default is 3.

    Returns
    -------
    tuple of numpy.ndarray
        Rounded latitude and longitude values from the netCDF file.
        
    Raises
    ------
    TypeError
        If nc_file is not str, Path, or xarray.Dataset, or if dimension names are not strings.
    ValueError
        If file path, dimension names are empty, or decimal_places is negative.
    FileNotFoundError
        If the file doesn't exist.
    KeyError
        If the specified dimensions don't exist in the dataset.
    """
    # Parameter validation
    if not isinstance(nc_file, (str, xr.Dataset, Path)):
        raise TypeError("nc_file must be a string, Path, or xarray.Dataset object")
    
    if not isinstance(lat_dimension_name, str) or not lat_dimension_name.strip():
        raise ValueError("lat_dimension_name must be a non-empty string")
    
    if not isinstance(lon_dimension_name, str) or not lon_dimension_name.strip():
        raise ValueError("lon_dimension_name must be a non-empty string")
    
    if not isinstance(decimal_places, int) or decimal_places < 0:
        raise ValueError("decimal_places must be a non-negative integer")

    # Open the netCDF file if it's a file path
    if isinstance(nc_file, (str, Path)):
        if not str(nc_file).strip():
            raise ValueError("File path cannot be empty")
        
        nc_path = Path(nc_file)
        if not nc_path.exists():
            raise FileNotFoundError(f"NetCDF file not found: {nc_path}")
        
        ncfile_integrity_status(nc_file)
        ds = xr.open_dataset(nc_file)
        close_dataset = True
    else:
        ds = nc_file
        close_dataset = False
    
    try:
        # Check if dimensions exist
        if lat_dimension_name not in ds.variables:
            raise KeyError(f"Latitude dimension '{lat_dimension_name}' not found in dataset")
        
        if lon_dimension_name not in ds.variables:
            raise KeyError(f"Longitude dimension '{lon_dimension_name}' not found in dataset")
        
        # Retrieve and round latitude and longitude values
        lat_values = ds[lat_dimension_name].values.round(decimal_places)
        lon_values = ds[lon_dimension_name].values.round(decimal_places)
        
        return lat_values, lon_values
    finally:
        if close_dataset:
            ds.close()


def get_latlon_deltas(lat_values: np.ndarray, 
                      lon_values: np.ndarray, 
                      decimal_places: int = 3) -> tuple[str, str]:
    """
    Computes the delta (difference) between the first two latitude and longitude values 
    and returns the deltas as rounded strings.

    Parameters
    ----------
    lat_values : numpy.ndarray
        Array of latitude values.
    lon_values : numpy.ndarray
        Array of longitude values.
    decimal_places : int, optional
        Number of decimal places to round the computed deltas. Default is 3.

    Returns
    -------
    tuple of str
        Rounded latitude and longitude deltas as strings.
        
    Raises
    ------
    TypeError
        If lat_values or lon_values are not numpy arrays.
    ValueError
        If arrays are empty, have less than 2 elements, or decimal_places is negative.
    """
    # Parameter validation
    if not isinstance(lat_values, np.ndarray):
        raise TypeError("lat_values must be a numpy array")
    
    if not isinstance(lon_values, np.ndarray):
        raise TypeError("lon_values must be a numpy array")
    
    if lat_values.size < 2:
        raise ValueError("lat_values must contain at least 2 elements")
    
    if lon_values.size < 2:
        raise ValueError("lon_values must contain at least 2 elements")
    
    if not isinstance(decimal_places, int) or decimal_places < 0:
        raise ValueError("decimal_places must be a non-negative integer")

    lat_delta = f"{abs(lat_values[1] - lat_values[0]):.{decimal_places}f}"
    lon_delta = f"{abs(lon_values[1] - lon_values[0]):.{decimal_places}f}"
    return lat_delta, lon_delta
        
    
def get_times(nc_file: str | xr.Dataset | Path, time_dimension_name: str) -> xr.DataArray:
    """
    Retrieves the time values from a specified time dimension in a netCDF file.

    Parameters
    ----------
    nc_file : str | xarray.Dataset | Path
        Path to the netCDF file or an already opened xarray.Dataset object.
    time_dimension_name : str
        Name of the time dimension in the dataset.

    Returns
    -------
    xarray.DataArray
        Time values as an xarray.DataArray.
        
    Raises
    ------
    TypeError
        If nc_file is not str, Path, or xarray.Dataset, or time_dimension_name is not string.
    ValueError
        If file path or time_dimension_name is empty.
    FileNotFoundError
        If the file doesn't exist.
    KeyError
        If the specified time dimension doesn't exist in the dataset.
    """
    # Parameter validation
    if not isinstance(nc_file, (str, xr.Dataset, Path)):
        raise TypeError("nc_file must be a string, Path, or xarray.Dataset object")
    
    if not isinstance(time_dimension_name, str) or not time_dimension_name.strip():
        raise ValueError("time_dimension_name must be a non-empty string")

    # Open the netCDF file if it's a file path
    if isinstance(nc_file, (str, Path)):
        if not str(nc_file).strip():
            raise ValueError("File path cannot be empty")
        
        nc_path = Path(nc_file)
        if not nc_path.exists():
            raise FileNotFoundError(f"NetCDF file not found: {nc_path}")
        
        ncfile_integrity_status(nc_file)
        ds = xr.open_dataset(nc_file)
        close_dataset = True
    else:
        ds = nc_file
        close_dataset = False
    
    try:
        # Check if time dimension exists
        if time_dimension_name not in ds.variables:
            raise KeyError(f"Time dimension '{time_dimension_name}' not found in dataset")
        
        # Extract time values from the specified time dimension
        time_values = ds[time_dimension_name]
        
        return time_values
    finally:
        if close_dataset:
            ds.close()


# Particular functions #
#-#-#-#-#-#-#-#-#-#-#-#-

def find_coordinate_variables(nc_file: str | xr.Dataset | Path) -> list[str]:
    """
    Function that searches for coordinate dimensions or variables 
    ('latitude', 'longitude', 'x', 'y') in an xarray Dataset.
    The coordinates should ideally be located among dimensions,
    but they might also appear among variables. This function attempts both cases using 
    'get_file_dimensions' and 'get_file_variables'.

    Parameters
    ----------
    nc_file : str | xarray.Dataset | Path
        String of the data file path, Path object, or the dataset itself.

    Returns
    -------
    list[str]
        A list of strings identifying the coordinate dimensions or variables.
        If duplicates are found, only unique keys are returned.

    Raises
    ------
    TypeError
        If nc_file is not str, Path, or xarray.Dataset.
    ValueError
        If no coordinate dimensions or variables are found, or file path is empty.
    FileNotFoundError
        If the file doesn't exist.
    """
    # Parameter validation
    if not isinstance(nc_file, (str, xr.Dataset, Path)):
        raise TypeError("nc_file must be a string, Path, or xarray.Dataset object")
    
    if isinstance(nc_file, (str, Path)) and not str(nc_file).strip():
        raise ValueError("File path cannot be empty")
    
    # Retrieve the dimension and variable lists
    dims = get_file_dimensions(nc_file)
    vars_ = get_file_variables(nc_file)

    # Ensure dims and vars_ are lists
    if isinstance(dims, str):
        dims = [dims]
    if isinstance(vars_, str):
        vars_ = [vars_]

    # Search for coordinate-related elements in dimensions and variables
    coord_keys = [key for key in dims + vars_ 
                  if key.lower().startswith(('lat', 'y', 'lon', 'x'))]

    if not coord_keys:
        raise ValueError("No 'latitude' or 'longitude' coordinates found "
                         f"in file '{nc_file}'.")

    unique_coord_keys = list(set(coord_keys))  # Remove duplicates and return a list of unique keys
    return unique_coord_keys
    

def find_nearest_coordinates(nc_file: str | xr.Dataset | Path, 
                           lats_obs: list[float] | np.ndarray, 
                           lons_obs: list[float] | np.ndarray, 
                           decimal_places: int = 3) -> tuple[np.ndarray, np.ndarray]:
    """
    Compares a set of observed latitude and longitude values with those from a netCDF file
    or xarray.Dataset object, and finds the nearest coordinates in the dataset that match
    the observed values.

    Parameters
    ----------
    nc_file : str | xarray.Dataset | Path
        Path to the netCDF file, Path object, or an already opened xarray.Dataset object containing 
        latitude and longitude coordinates.
    lats_obs : list[float] | numpy.ndarray
        List or array of observed latitude values to compare.
    lons_obs : list[float] | numpy.ndarray
        List or array of observed longitude values to compare.
    decimal_places : int, optional
         Number of decimal places to round the latitude and longitude values. 
         Default is 3.

    Returns
    -------
    tuple of numpy.ndarray
        Two arrays containing the nearest latitude and longitude values from the dataset
        for each observed coordinate. The values are rounded to specified decimal places.

    Raises
    ------
    TypeError
        If parameters have incorrect types.
    ValueError
        If coordinate arrays are empty or have mismatched lengths, or if no coordinate variables are found.
    FileNotFoundError
        If the file doesn't exist.
    """
    # Parameter validation
    if not isinstance(nc_file, (str, xr.Dataset, Path)):
        raise TypeError("nc_file must be a string, Path, or xarray.Dataset object")
    
    if not isinstance(lats_obs, (list, np.ndarray)):
        raise TypeError("lats_obs must be a list or numpy array")
    
    if not isinstance(lons_obs, (list, np.ndarray)):
        raise TypeError("lons_obs must be a list or numpy array")
    
    if not isinstance(decimal_places, int) or decimal_places < 0:
        raise ValueError("decimal_places must be a non-negative integer")
    
    # Convert to numpy arrays and validate
    lats_obs = np.array(lats_obs, dtype='d')
    lons_obs = np.array(lons_obs, dtype='d')
    
    if lats_obs.size == 0:
        raise ValueError("lats_obs cannot be empty")
    
    if lons_obs.size == 0:
        raise ValueError("lons_obs cannot be empty")
    
    if lats_obs.size != lons_obs.size:
        raise ValueError("lats_obs and lons_obs must have the same length")

    # Retrieve coordinate variable names (latitude and longitude)
    coord_varlist = find_coordinate_variables(nc_file)

    # Handle file opening: accept both file paths and already opened xarray.Dataset objects
    if isinstance(nc_file, (str, Path)):
        if not str(nc_file).strip():
            raise ValueError("File path cannot be empty")
        
        nc_path = Path(nc_file)
        if not nc_path.exists():
            raise FileNotFoundError(f"NetCDF file not found: {nc_path}")
        
        ncfile_integrity_status(nc_file)
        ds = xr.open_dataset(nc_file)
        close_ds = True
    elif isinstance(nc_file, xr.Dataset):
        ds = nc_file
        close_ds = False
    else:
        raise TypeError("Input must be a file path (str/Path) or an xarray.Dataset object.")

    try:
        # Retrieve latitude and longitude data from the dataset
        lats_ds = np.array(ds[coord_varlist[0]], dtype='d')
        lons_ds = np.array(ds[coord_varlist[1]], dtype='d')

        nearest_lats = []
        nearest_lons = []

        # Find the nearest latitude and longitude for each observed coordinate
        for lat_obs, lon_obs in zip(lats_obs, lons_obs):
            nearest_lat_idx = np.abs(lat_obs - lats_ds).argmin()
            nearest_lon_idx = np.abs(lon_obs - lons_ds).argmin()

            nearest_lats.append(lats_ds[nearest_lat_idx])
            nearest_lons.append(lons_ds[nearest_lon_idx])

        # Return nearest latitudes and longitudes, rounded to specified decimal places
        nearest_lats = np.round(nearest_lats, decimal_places)
        nearest_lons = np.round(nearest_lons, decimal_places)

        return nearest_lats, nearest_lons
    
    finally:
        # Close the dataset if it was opened within this function
        if close_ds:
            ds.close()


#--------------------------#
# Parameters and constants #
#--------------------------#

# String splitting character #
SPLIT_DELIM = COMMON_DELIMITER_LIST[0]
