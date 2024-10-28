#! /usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------#
# Import modules #
#----------------#

import numpy as np
import xarray as xr

#-----------------------#
# Import custom modules #
#-----------------------#

from pyutils.parameters_and_constants.global_parameters import common_delim_list
from pyutils.filewise.xarray_utils.file_utils import check_ncfile_integrity

#-------------------------#
# Define custom functions #
#-------------------------#            

# Dimension handlers #
#--------------------#

# Main methods #
#-#-#-#-#-#-#-#-

def get_file_dimensions(nc_file):
    """
    Extracts dimension names from a netCDF file or xarray.Dataset. In some cases,
    dimensions can also appear as variables, so this function ensures only
    dimensions are returned.

    Parameters
    ----------
    nc_file : str or xarray.Dataset
        Either the path to the netCDF file or an already opened xarray.Dataset object.

    Returns
    -------
    dimension_names : list or str
        A list of dimension names, or a single dimension name if only one is found.

    Raises
    ------
    TypeError
        If the input is neither a string nor an xarray.Dataset object.
    """
    if isinstance(nc_file, str):
        ds = check_ncfile_integrity(nc_file)
        close_dataset = True
    elif isinstance(nc_file, xr.Dataset):
        ds = nc_file
        close_dataset = False
    else:
        raise TypeError("Unsupported data file type. Expected str or xarray.Dataset.")

    dimlist = list(ds.dims)
    varlist = list(ds.variables)
    
    # Retain only those dimensions that are present among variables
    dimlist_nodim = [dim for dim in dimlist if dim in varlist]

    if close_dataset:
        ds.close()
        
    return dimlist_nodim[0] if len(dimlist_nodim) == 1 else dimlist_nodim


def get_file_variables(nc_file):
    """
    Extracts variable names from a netCDF file or xarray.Dataset, excluding
    dimensions, as dimensions may also be present in the variable list.

    Parameters
    ----------
    nc_file : str or xarray.Dataset
        Either the path to the netCDF file or an already opened xarray.Dataset object.

    Returns
    -------
    variable_names : list or str
        A list of variable names, or a single variable name if only one is found.

    Raises
    ------
    TypeError
        If the input is neither a string nor an xarray.Dataset object.
    """
    if isinstance(nc_file, str):
        ds = check_ncfile_integrity(nc_file)
        close_dataset = True
    elif isinstance(nc_file, xr.Dataset):
        ds = nc_file
        close_dataset = False
    else:
        raise TypeError("Unsupported data file type. Expected str or xarray.Dataset.")

    varlist = list(ds.variables)
    dimlist = list(ds.dims)
    
    # Remove dimensions from the variable list
    varlist_nodim = [var for var in varlist if var not in dimlist]

    if close_dataset:
        ds.close()
        
    return varlist_nodim[0] if len(varlist_nodim) == 1 else varlist_nodim


def get_model_list(path_list, split_pos, splitdelim="_"):
    """
    Extracts model names from a list of file paths or file names by splitting the file
    name at a specified position. The function can handle both absolute/relative paths 
    and file names, assuming they contain low bars ('_') as separators.

    Parameters
    ----------
    path_list : list of str
        List of file paths (absolute or relative) or file names.
    split_pos : int
        Position in the split file name (after splitting by the delimiter) that contains
        the model name.
    splitdelim : str, optional
        Delimiter used to split the file name. Default is "_".

    Returns
    -------
    unique_model_list : list of str
        A list of unique model names extracted from the file paths.
    """
    # Handle paths with forward slashes to extract file names
    grib_file_list = [path.split("/")[-1] for path in path_list]

    # Split file names by the delimiter and extract model names from the specified position
    model_list = [f.split(splitdelim)[split_pos] for f in grib_file_list]

    # Return unique model names
    unique_model_list = np.unique(model_list).tolist()
    return unique_model_list


def get_latlon_bounds(nc_file, lat_dimension_name, lon_dimension_name, value_roundoff=3):
    """
    Retrieves the latitude and longitude values from a netCDF file and rounds them 
    to the specified decimal precision.

    Parameters
    ----------
    nc_file : str or xarray.Dataset
        Path to the netCDF file or an already opened xarray.Dataset object.
    lat_dimension_name : str
        Name of the latitude dimension in the dataset.
    lon_dimension_name : str
        Name of the longitude dimension in the dataset.
    value_roundoff : int, optional
        Number of decimal places to round the latitude and longitude values. Default is 3.

    Returns
    -------
    tuple of numpy.ndarray
        Rounded latitude and longitude values from the netCDF file.
    """
    # Open the netCDF file
    ds = check_ncfile_integrity(nc_file)
    
    # Retrieve and round latitude and longitude values
    lat_values = ds[lat_dimension_name].values.round(value_roundoff)
    lon_values = ds[lon_dimension_name].values.round(value_roundoff)
    
    ds.close()
    return lat_values, lon_values


def get_latlon_deltas(lat_values, lon_values, delta_roundoff=3):
    """
    Computes the delta (difference) between the first two latitude and longitude values 
    and returns the deltas as rounded strings.

    Parameters
    ----------
    lat_values : numpy.ndarray
        Array of latitude values.
    lon_values : numpy.ndarray
        Array of longitude values.
    delta_roundoff : int, optional
        Number of decimal places to round the computed deltas. Default is 3.

    Returns
    -------
    tuple of str
        Rounded latitude and longitude deltas as strings.
    """
    lat_delta = f"{abs(lat_values[1] - lat_values[0]):.{delta_roundoff}f}"
    lon_delta = f"{abs(lon_values[1] - lon_values[0]):.{delta_roundoff}f}"
    return lat_delta, lon_delta
        
    
def get_times(nc_file, time_dimension_name):
    """
    Retrieves the time values from a specified time dimension in a netCDF file.

    Parameters
    ----------
    nc_file : str or xarray.Dataset
        Path to the netCDF file or an already opened xarray.Dataset object.
    time_dimension_name : str
        Name of the time dimension in the dataset.

    Returns
    -------
    xarray.DataArray
        Time values as an xarray.DataArray.
    """
    ds = check_ncfile_integrity(nc_file)
    
    # Extract time values from the specified time dimension
    time_values = ds[time_dimension_name]
    
    ds.close()
    return time_values


# Particular methods #
#-#-#-#-#-#-#-#-#-#-#-

def find_coordinate_variables(nc_file):
    """
    Function that searches for coordinate dimensions or variables 
    ('latitude', 'longitude', 'x', 'y') in an xarray Dataset.
    The coordinates should ideally be located among dimensions,
    but they might also appear among variables. This function attempts both cases using 
    'get_file_dimensions' and 'get_file_variables'.

    Parameters
    ----------
    nc_file : str or xarray.Dataset
        String of the data file or the dataset itself.

    Returns
    -------
    list or None
        A list of strings identifying the coordinate dimensions or variables.
        If duplicates are found, only unique keys are returned.

    Raises
    ------
    ValueError
        If no coordinate dimensions or variables are found.
    """
    
    # Retrieve the dimension and variable lists
    dims = get_file_dimensions(nc_file)
    vars_ = get_file_variables(nc_file)

    # Search for coordinate-related elements in dimensions and variables
    coord_keys = [key for key in dims + vars_ 
                  if key.lower().startswith(('lat', 'y', 'lon', 'x'))]

    if not coord_keys:
        raise ValueError("No 'latitude' or 'longitude' coordinates found "
                         f"in file '{nc_file}'.")

    unique_coord_keys = list(set(coord_keys))  # Remove duplicates and return a list of unique keys
    return unique_coord_keys
    

def find_nearest_coordinates(nc_file, lats_obs, lons_obs, roundoff=3):
    """
    Compares a set of observed latitude and longitude values with those from a netCDF file
    or xarray.Dataset object, and finds the nearest coordinates in the dataset that match
    the observed values.

    Parameters
    ----------
    nc_file : str or xarray.Dataset
        Path to the netCDF file or an already opened xarray.Dataset object containing 
        latitude and longitude coordinates.
    lats_obs : list or numpy.ndarray
        List or array of observed latitude values to compare.
    lons_obs : list or numpy.ndarray
        List or array of observed longitude values to compare.
    roundoff : int, optional
         Number of decimal places to round the latitude and longitude values. 
         Default is 3.

    Returns
    -------
    tuple of numpy.ndarray
        Two arrays containing the nearest latitude and longitude values from the dataset
        for each observed coordinate. The values are rounded to 3 decimal places.

    Raises
    ------
    ValueError
        If no coordinate variables ('latitude' or 'longitude') are found in the dataset.
    """
    # Retrieve coordinate variable names (latitude and longitude)
    coord_varlist = find_coordinate_variables(nc_file)

    # Handle file opening: accept both file paths and already opened xarray.Dataset objects
    if isinstance(nc_file, str):
        ds = check_ncfile_integrity(nc_file)
        close_ds = True
    elif isinstance(nc_file, xr.Dataset):
        ds = nc_file
        close_ds = False
    else:
        raise TypeError("Input must be a file path (str) or an xarray.Dataset object.")

    # Retrieve latitude and longitude data from the dataset
    lats_ds = np.array(ds[coord_varlist[0]], dtype='d')
    lons_ds = np.array(ds[coord_varlist[1]], dtype='d')

    # Ensure observed lats and lons are in numpy array format
    lats_obs = np.array(lats_obs, dtype='d')
    lons_obs = np.array(lons_obs, dtype='d')

    nearest_lats = []
    nearest_lons = []

    # Find the nearest latitude and longitude for each observed coordinate
    for lat_obs, lon_obs in zip(lats_obs, lons_obs):
        nearest_lat_idx = np.abs(lat_obs - lats_ds).argmin()
        nearest_lon_idx = np.abs(lon_obs - lons_ds).argmin()

        nearest_lats.append(lats_ds[nearest_lat_idx])
        nearest_lons.append(lons_ds[nearest_lon_idx])

    # Close the dataset if it was opened within this function
    if close_ds:
        ds.close()

    # Return nearest latitudes and longitudes, rounded to 3 decimal places
    nearest_lats = np.round(nearest_lats, roundoff)
    nearest_lons = np.round(nearest_lons, roundoff)

    return nearest_lats, nearest_lons


#--------------------------#
# Parameters and constants #
#--------------------------#

# String splitting character #
splitdelim = common_delim_list[0]
