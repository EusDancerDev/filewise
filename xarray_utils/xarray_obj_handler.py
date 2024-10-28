#! /usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------#
# Import modules #
#----------------#

import xarray as xr

#-----------------------#
# Import custom modules #
#-----------------------#

from pyutils.pandas_data_frames.data_frame_handler import save2csv
from pyutils.string_handler.string_handler import append_ext, get_obj_specs
from pyutils.filewise.xarray_utils.patterns import find_coordinate_variables, find_time_dimension

#-------------------------#
# Define custom functions #
#-------------------------#

# Main methods #
#--------------#

# xarray objects #
#~~~~~~~~~~~~~~~~#

def create_ds_component(var_name,
                        data_array,
                        dimlist,
                        dim_dict,
                        attrs_dict):
    """
    Create an xarray.DataArray component to be added to an xarray.Dataset.

    Parameters:
    -----------
    var_name : str
        Name of the variable represented by the DataArray.
    data_array : array-like
        The array containing data to be stored in the DataArray.
    dimlist : list of str
        List of dimension names corresponding to the dimensions of the data.
    dim_dict : dict
        Dictionary mapping dimension names to coordinate arrays.
    attrs_dict : dict
        Dictionary of attributes describing the DataArray (e.g., units, description).

    Returns:
    --------
    data_array_dict : dict
        A dictionary containing the DataArray with the variable name as the key.

    Notes:
    ------
    - The returned dictionary can be used to construct or extend an xarray.Dataset.
    """
    data_array_dict = {
        var_name: xr.DataArray(
            data=data_array,
            dims=dimlist,
            coords=dim_dict,
            attrs=attrs_dict,
        )
    }
    
    return data_array_dict


# netCDF files #
#~~~~~~~~~~~~~~#

def save2nc(file_name, data=None, file_format="NETCDF4",
            vardim_list=None, data_arrays=None, dimlists=None, dim_dict_list=None, 
            attrs_dict_list=None, global_attrs_dict=None):
    """
    Save data to a NetCDF file. Can handle either a fully constructed 
    xarray.Dataset or build a new dataset from components.

    Parameters
    ----------
    file_name : str
        The name of the resulting NetCDF file.
        The '.nc' extension will be added automatically if not present.
    data : xarray.Dataset
        An xarray Dataset, i.e. the pre-existing one, that will be directly saved.
    file_format : {"NETCDF4", "NETCDF4_CLASSIC", "NETCDF3_64BIT", "NETCDF3_CLASSIC"}, default "NETCDF4"
        File format for the resulting netCDF file:

        * NETCDF4: Data is stored in an HDF5 file, using netCDF4 API
          features.
        * NETCDF4_CLASSIC: Data is stored in an HDF5 file, using only
          netCDF 3 compatible API features.
        * NETCDF3_64BIT: 64-bit offset version of the netCDF 3 file format,
          which fully supports 2+ GB files, but is only compatible with
          clients linked against netCDF version 3.6.0 or later.
        * NETCDF3_CLASSIC: The classic netCDF 3 file format. It does not
          handle 2+ GB files very well.

        All formats are supported by the netCDF4-python library.
        scipy.io.netcdf only supports the last two formats.

        The default format is NETCDF4 if you are saving a file to disk and
        have the netCDF4-python library available. Otherwise, xarray falls
        back to using scipy to write netCDF files and defaults to the
        NETCDF3_64BIT format (scipy does not support netCDF4).    
    
    vardim_list : list of str, optional
        List of variable-dimension names for building the dataset.
    data_arrays : list of xarray.DataArray, optional
        Data arrays for building the dataset if `data` is not provided.
    dimlists : list of list, optional
        List of dimension names for each variable in the dataset.
    dim_dict_list : list of dict, optional
        List of dictionaries containing dimension information for each variable.
    attrs_dict_list : list of dict, optional
        List of attribute dictionaries for each variable in the dataset.
    global_attrs_dict : dict, optional
        Dictionary for global attributes to assign to the dataset.
        If no data is given, this argument will take effect instead of `attrs_dict_list`,
        because `data` is a pre-existing dataset.

    Returns
    -------
    None
        Saves a NetCDF file and prints success confirmation.

    Notes
    -----
    - If `data` is provided, the function directly saves it as a NetCDF file.
    - If `data` is not provided, the function will construct a dataset using the 
      `vardim_list`, `data_arrays`, `dimlists`, etc.
    """
    # File format validation
    if file_format not in nc_file_formats:
        raise ValueError(f"Unsupported file format '{file_format}'. "
                         f"Choose one from {nc_file_formats}.")
        
    # Convert arguments to lists if they are not already lists
    vardim_list = _ensure_list(vardim_list)
    data_arrays = _ensure_list(data_arrays)
    dimlists = _ensure_list(dimlists)
    dim_dict_list = _ensure_list(dim_dict_list)
    attrs_dict_list = _ensure_list(attrs_dict_list)    
    
    # Check if dataset exists
    if data is not None:
        # Call helper if dataset is already created
        _save_ds_as_nc(data, file_name, global_attrs_dict)
        
    else:
        # Build dataset from components
        ds = xr.Dataset()
        for vardim, data_array, dimlist, dim_dict, attrs_dict in zip(
                vardim_list, data_arrays, dimlists, dim_dict_list, attrs_dict_list
                ):
            
            data_array_dict = create_ds_component(vardim, 
                                                  data_array, 
                                                  dimlist, 
                                                  dim_dict, 
                                                  attrs_dict)
            ds = ds.merge(data_array_dict)
    
        # Add netCDF file extension ('.nc') if not present
        if get_obj_specs(file_name, "ext") != f".{extensions[0]}":
            file_name = append_ext(file_name, extensions[0])
        
        # Save to file
        _save_ds_as_nc(ds, file_name, global_attrs_dict)
        print(f"{file_name} file successfully created")
 
# CSV files #
#~~~~~~~~~~~#

def save_nc_as_csv(nc_file, 
                   columns_to_drop=None,
                   separator=",",
                   save_index=False,
                   save_header=True,
                   csv_file_name=None,
                   date_format=None,
                   approximate_coords=False,
                   latitude_point=None,
                   longitude_point=None):
    """
    Save netCDF data into a CSV file. The function handles 
    3D data variables (typically dependent on time, latitude, longitude)
    and speeds up further data processes.

    Parameters
    ----------
    nc_file : str or xarray.Dataset or xarray.DataArray
        String of the xarray data set file path or the already opened dataset or data array.
    columns_to_drop : str or list of str, optional
        Names of columns to drop. Use "coords" to drop coordinate variables.
    separator : str, default ','
        Separator used in the CSV file.
    save_index : bool, default False
        Whether to include an index column in the CSV.
    save_header : bool, default True
        Whether to include a header row in the CSV.
    csv_file_name : str, optional
        Name of the output CSV file. If None, extracts from nc_file name.
    date_format : str, optional
        Date format to apply if the dataset contains time data.
    approximate_coords : bool, default False
        If True, approximates the nearest latitude/longitude points.
    latitude_point : float, optional
        Latitude point for approximation.
    longitude_point : float, optional
        Longitude point for approximation.

    Returns
    -------
    None
        Saves a CSV file and prints success confirmation.
    """
    
    # Open netCDF data file if passed a string
    if isinstance(nc_file, str):
        print(f"Opening {nc_file}...")
        ds = xr.open_dataset(nc_file)
    else:
        ds = nc_file.copy()
        
    if latitude_point is not None or longitude_point is not None:
        coord_varlist = find_coordinate_variables(ds)
        lats = ds[coord_varlist[0]]
        lons = ds[coord_varlist[1]]
        
        if len(lats) == len(lons) == 1:
            raise ValueError("Object is already point data")
        
        # Approximate or select coordinates
        coord_idx_kw = {}
        if approximate_coords:
            lat_idx = abs(lats - latitude_point).argmin()
            lon_idx = abs(lons - longitude_point).argmin()
            coord_idx_kw = {coord_varlist[0]: lat_idx, coord_varlist[1]: lon_idx}
            ds = ds.isel(**coord_idx_kw)
        else:
            coord_idx_kw = {coord_varlist[0]: latitude_point, coord_varlist[1]: longitude_point}
            ds = ds.sel(**coord_idx_kw)

    # Drop columns if needed
    if columns_to_drop is None:
        data_frame = ds.to_dataframe().reset_index(drop=False)
    elif columns_to_drop == "coords": 
        coord_varlist = find_coordinate_variables(ds)
        data_frame = ds.to_dataframe().reset_index(drop=False).drop(columns=coord_varlist)
    else:
        data_frame = ds.to_dataframe().reset_index(drop=False).drop(columns=columns_to_drop)

    # Create CSV file name
    if isinstance(nc_file, str) and not csv_file_name:
        csv_file_name = nc_file.split(".")[0] + ".csv"
    elif not isinstance(nc_file, str) and not csv_file_name:
        raise ValueError("You must provide a CSV file name.")
    
    # Save to CSV
    save2csv(csv_file_name, data_frame, separator, save_index, save_header, date_format)


def save_da_as_csv(data_array, 
                   separator=",",
                   save_index=False,
                   save_header=True,
                   csv_file_name=None,
                   new_columns=None,
                   date_format=None):
    """
    Save a xarray.DataArray object to a CSV file. Data variables may 
    originally be 3D, typically depending on (time, latitude, longitude).

    Parameters
    ----------
    data_array : xarray.DataArray
        DataArray object to save.
    new_columns : str or list of str, optional
        Names for the new columns in the output CSV. Default uses 'time' and variable name.
    separator : str, default ','
        Separator for the CSV.
    save_index : bool, default False
        Whether to include an index column in the CSV.
    save_header : bool, default True
        Whether to include a header row in the CSV.
    csv_file_name : str, optional
        Name for the CSV file.
    date_format : str, optional
        Date format for time data, if present.

    Returns
    -------
    None
        Saves a CSV file and prints success confirmation.
    """
    
    # Convert to pandas DataFrame
    data_frame = data_array.to_dataframe().reset_index(drop=False)        
    
    # Rename the columns based on the provided new_columns
    if not new_columns:
        date_key = find_time_dimension(data_array)
        new_columns = [date_key, data_array.name]
    data_frame.columns = new_columns
    
    # Ensure CSV file name is provided
    if csv_file_name is None:
        raise ValueError("You must provide a CSV file name.")
    
    # Save to CSV
    save2csv(csv_file_name, data_frame, separator, save_index, save_header, date_format)
    

# Helpers #
#---------#
        
# Helper function to save an existing dataset with optional attribute updates
def _save_ds_as_nc(xarray_ds, file_name, attrs_dict=None):
    if attrs_dict:
        xarray_ds.attrs = attrs_dict
        
    # Add netCDF file extension ('.nc') if not present
    if get_obj_specs(file_name, "ext") != ".nc":
        file_name += ".nc" 
    
    # Save to file
    xarray_ds.to_netcdf(file_name, mode="w", format="NETCDF4")
    print(f"{file_name} has been successfully created")

def _ensure_list(arg):
    return arg if isinstance(arg, list) else [arg]


#--------------------------#
# Parameters and constants #
#--------------------------#

# File extensions #
extensions = ["nc", "csv"]

# Valid netCDF file formats #
nc_file_formats = ["NETCDF4", "NETCDF4_CLASSIC", "NETCDF3_64BIT", "NETCDF3_CLASSIC"]
