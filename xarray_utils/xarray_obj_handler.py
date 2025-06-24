#! /usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------#
# Import modules #
#----------------#

import xarray as xr
from pathlib import Path

#------------------------#
# Import project modules #
#------------------------#

from filewise.pandas_utils.pandas_obj_handler import save2csv
from filewise.xarray_utils.patterns import find_coordinate_variables
from pygenutils.arrays_and_lists.data_manipulation import flatten_list
from pygenutils.strings.string_handler import append_ext, get_obj_specs
from pygenutils.time_handling.date_and_time_utils import find_dt_key

#-------------------------#
# Define custom functions #
#-------------------------#

# Main functions #
#----------------#

# xarray objects #
#~~~~~~~~~~~~~~~~#

def create_ds_component(var_name: str,
                        data_array: xr.DataArray | list | tuple,
                        dimlist: list[str],
                        dim_dict: dict[str, xr.DataArray | list | tuple],
                        attrs_dict: dict[str, str | int | float]) -> dict[str, xr.DataArray]:
    """
    Create an xarray.DataArray component to be added to an xarray.Dataset.

    Parameters:
    -----------
    var_name : str
        Name of the variable represented by the DataArray.
    data_array : xarray.DataArray or array-like
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

    Raises:
    -------
    TypeError
        If parameters have incorrect types.
    ValueError
        If var_name is empty, dimlist is empty, or dictionaries are empty.

    Notes:
    ------
    - The returned dictionary can be used to construct or extend an xarray.Dataset.
    """
    # Parameter validation
    if not isinstance(var_name, str) or not var_name.strip():
        raise ValueError("var_name must be a non-empty string")
    
    if not isinstance(dimlist, list) or not dimlist:
        raise ValueError("dimlist must be a non-empty list")
    
    if not all(isinstance(dim, str) and dim.strip() for dim in dimlist):
        raise ValueError("All dimension names must be non-empty strings")
    
    if not isinstance(dim_dict, dict) or not dim_dict:
        raise ValueError("dim_dict must be a non-empty dictionary")
    
    if not isinstance(attrs_dict, dict):
        raise ValueError("attrs_dict must be a dictionary")
    
    # Validate that all dimensions in dimlist are present in dim_dict
    missing_dims = set(dimlist) - set(dim_dict.keys())
    if missing_dims:
        raise ValueError(f"Missing dimensions in dim_dict: {missing_dims}")
    
    try:
        data_array_dict = {
            var_name: xr.DataArray(
                data=data_array,
                dims=dimlist,
                coords=dim_dict,
                attrs=attrs_dict,
            )
        }
        
        return data_array_dict
    except Exception as e:
        raise RuntimeError(f"Failed to create DataArray component: {e}")


# netCDF files #
#~~~~~~~~~~~~~~#

def save2nc(file_name: str | Path, 
            data: xr.Dataset | None = None, 
            file_format: str = "NETCDF4",
            vardim_list: str | list[str] | None = None, 
            data_arrays: xr.DataArray | list[xr.DataArray] | None = None, 
            dimlists: list[str] | list[list[str]] | None = None, 
            dim_dict_list: dict | list[dict] | None = None, 
            attrs_dict_list: dict | list[dict] | None = None, 
            global_attrs_dict: dict[str, str | int | float] | None = None) -> None:
    """
    Save data to a NetCDF file. Can handle either a fully constructed 
    xarray.Dataset or build a new dataset from components.

    Parameters
    ----------
    file_name : str or Path
        The name of the resulting NetCDF file.
        The '.nc' extension will be added automatically if not present.
    data : xarray.Dataset, optional
        An xarray Dataset, i.e. the pre-existing one, that will be directly saved.
    file_format : {"NETCDF4", "NETCDF4_CLASSIC", "NETCDF3_64BIT", "NETCDF3_CLASSIC"}, default "NETCDF4"
        File format for the resulting netCDF file.
    vardim_list : str or list of str, optional
        List of variable-dimension names for building the dataset.
    data_arrays : xarray.DataArray or list of xarray.DataArray, optional
        Data arrays for building the dataset if `data` is not provided.
    dimlists : list of str or list of list of str, optional
        List of dimension names for each variable in the dataset.
    dim_dict_list : dict or list of dict, optional
        List of dictionaries containing dimension information for each variable.
    attrs_dict_list : dict or list of dict, optional
        List of attribute dictionaries for each variable in the dataset.
    global_attrs_dict : dict, optional
        Dictionary for global attributes to assign to the dataset.

    Returns
    -------
    None
        Saves a NetCDF file and prints success confirmation.

    Raises
    ------
    TypeError
        If parameters have incorrect types.
    ValueError
        If file_name is empty, file_format is invalid, or parameter combinations are invalid.
    RuntimeError
        If dataset creation or file saving fails.

    Notes
    -----
    - If `data` is provided, the function directly saves it as a NetCDF file.
    - If `data` is not provided, the function will construct a dataset using the 
      `vardim_list`, `data_arrays`, `dimlists`, etc.
    """
    # Parameter validation
    if not isinstance(file_name, (str, Path)) or not str(file_name).strip():
        raise ValueError("file_name must be a non-empty string or Path")
    
    if not isinstance(file_format, str) or file_format not in NC_FILE_FORMATS:
        raise ValueError(f"Unsupported file format '{file_format}'. "
                         f"Choose one from {NC_FILE_FORMATS}.")
    
    if data is not None and not isinstance(data, xr.Dataset):
        raise TypeError("data must be an xarray.Dataset or None")
    
    if global_attrs_dict is not None and not isinstance(global_attrs_dict, dict):
        raise TypeError("global_attrs_dict must be a dictionary or None")
        
    # Convert arguments to lists if they are not already lists (defensive programming)
    if vardim_list is not None:
        vardim_list = _ensure_list(vardim_list)
        vardim_list = flatten_list(vardim_list)
    
    if data_arrays is not None:
        data_arrays = _ensure_list(data_arrays)
        data_arrays = flatten_list(data_arrays)
    
    if dimlists is not None:
        dimlists = _ensure_list(dimlists)
        dimlists = flatten_list(dimlists)
    
    if dim_dict_list is not None:
        dim_dict_list = _ensure_list(dim_dict_list)
        dim_dict_list = flatten_list(dim_dict_list)
    
    if attrs_dict_list is not None:
        attrs_dict_list = _ensure_list(attrs_dict_list)
        attrs_dict_list = flatten_list(attrs_dict_list)
    
    # Check if dataset exists
    if data is not None:
        # Call helper if dataset is already created
        _save_ds_as_nc(data, file_name, global_attrs_dict)
        
    else:
        # Validate required parameters for dataset construction
        if not all([vardim_list, data_arrays, dimlists, dim_dict_list, attrs_dict_list]):
            raise ValueError("When data is None, all of vardim_list, data_arrays, "
                           "dimlists, dim_dict_list, and attrs_dict_list must be provided")
        
        # Validate parameter lengths match
        param_lengths = [len(vardim_list), len(data_arrays), len(dimlists), 
                        len(dim_dict_list), len(attrs_dict_list)]
        if not all(length == param_lengths[0] for length in param_lengths):
            raise ValueError("All parameter lists must have the same length")
        
        # Build dataset from components
        try:
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
        except Exception as e:
            raise RuntimeError(f"Failed to build dataset from components: {e}")
    
        # Add netCDF file extension ('.nc') if not present
        if get_obj_specs(str(file_name), "ext") != f".{EXTENSIONS[0]}":
            file_name = append_ext(str(file_name), EXTENSIONS[0])
        
        # Save to file
        _save_ds_as_nc(ds, file_name, global_attrs_dict)
        print(f"{file_name} file successfully created")
 
# CSV files #
#~~~~~~~~~~~#

def save_nc_as_csv(nc_file: str | xr.Dataset | xr.DataArray | Path, 
                   columns_to_drop: str | list[str] | None = None,
                   separator: str = ",",
                   save_index: bool = False,
                   save_header: bool = True,
                   csv_file_name: str | Path | None = None,
                   date_format: str | None = None,
                   approximate_coords: bool = False,
                   latitude_point: float | None = None,
                   longitude_point: float | None = None) -> None:
    """
    Save netCDF data into a CSV file. The function handles 
    3D data variables (typically dependent on time, latitude, longitude)
    and speeds up further data processes.

    Parameters
    ----------
    nc_file : str or xarray.Dataset or xarray.DataArray or Path
        String of the xarray data set file path or the already opened dataset or data array.
    columns_to_drop : str or list of str, optional
        Names of columns to drop. Use "coords" to drop coordinate variables.
    separator : str, default ','
        Separator used in the CSV file.
    save_index : bool, default False
        Whether to include an index column in the CSV.
    save_header : bool, default True
        Whether to include a header row in the CSV.
    csv_file_name : str or Path, optional
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
        
    Raises
    ------
    TypeError
        If parameters have incorrect types.
    ValueError
        If required parameters are missing or invalid, or coordinate selection is invalid.
    FileNotFoundError
        If the input file doesn't exist.
    RuntimeError
        If coordinate approximation or file operations fail.
    """
    # Parameter validation
    if not isinstance(nc_file, (str, xr.Dataset, xr.DataArray, Path)):
        raise TypeError("nc_file must be a string, Path, xarray.Dataset, or xarray.DataArray")
    
    if isinstance(nc_file, (str, Path)) and not str(nc_file).strip():
        raise ValueError("File path cannot be empty")
    
    if columns_to_drop is not None:
        if isinstance(columns_to_drop, str):
            columns_to_drop = [columns_to_drop] if columns_to_drop != "coords" else columns_to_drop
        elif isinstance(columns_to_drop, list):
            columns_to_drop = flatten_list(columns_to_drop)
            if not all(isinstance(col, str) for col in columns_to_drop):
                raise TypeError("All items in columns_to_drop must be strings")
        else:
            raise TypeError("columns_to_drop must be a string, list of strings, or None")
    
    if not isinstance(separator, str) or not separator:
        raise ValueError("separator must be a non-empty string")
    
    if not isinstance(save_index, bool):
        raise TypeError("save_index must be a boolean")
    
    if not isinstance(save_header, bool):
        raise TypeError("save_header must be a boolean")
    
    if csv_file_name is not None and not isinstance(csv_file_name, (str, Path)):
        raise TypeError("csv_file_name must be a string, Path, or None")
    
    if csv_file_name is not None and not str(csv_file_name).strip():
        raise ValueError("csv_file_name cannot be empty")
    
    if not isinstance(approximate_coords, bool):
        raise TypeError("approximate_coords must be a boolean")
    
    if latitude_point is not None and not isinstance(latitude_point, (int, float)):
        raise TypeError("latitude_point must be a number or None")
    
    if longitude_point is not None and not isinstance(longitude_point, (int, float)):
        raise TypeError("longitude_point must be a number or None")
    
    # Open netCDF data file if passed a string or Path
    if isinstance(nc_file, (str, Path)):
        nc_path = Path(nc_file)
        if not nc_path.exists():
            raise FileNotFoundError(f"NetCDF file not found: {nc_path}")
        
        print(f"Opening {nc_file}...")
        try:
            ds = xr.open_dataset(nc_file)
        except Exception as e:
            raise RuntimeError(f"Failed to open netCDF file: {e}")
    else:
        ds = nc_file.copy()
        
    try:
        if latitude_point is not None or longitude_point is not None:
            if latitude_point is None or longitude_point is None:
                raise ValueError("Both latitude_point and longitude_point must be provided when using coordinate selection")
            
            coord_varlist = find_coordinate_variables(ds)
            lats = ds[coord_varlist[0]]
            lons = ds[coord_varlist[1]]
            
            if len(lats) == len(lons) == 1:
                raise ValueError("Object is already point data")
            
            # Approximate or select coordinates
            try:
                if approximate_coords:
                    lat_idx = abs(lats - latitude_point).argmin()
                    lon_idx = abs(lons - longitude_point).argmin()
                    coord_idx_kw = {coord_varlist[0]: lat_idx, coord_varlist[1]: lon_idx}
                    ds = ds.isel(**coord_idx_kw)
                else:
                    coord_idx_kw = {coord_varlist[0]: latitude_point, coord_varlist[1]: longitude_point}
                    ds = ds.sel(**coord_idx_kw)
            except Exception as e:
                raise RuntimeError(f"Failed to select coordinates: {e}")

        # Drop columns if needed
        try:
            if columns_to_drop is None:
                data_frame = ds.to_dataframe().reset_index(drop=False)
            elif columns_to_drop == "coords": 
                coord_varlist = find_coordinate_variables(ds)
                data_frame = ds.to_dataframe().reset_index(drop=False).drop(columns=coord_varlist)
            else:
                data_frame = ds.to_dataframe().reset_index(drop=False).drop(columns=columns_to_drop)
        except Exception as e:
            raise RuntimeError(f"Failed to process DataFrame: {e}")

        # Create CSV file name
        if isinstance(nc_file, (str, Path)) and not csv_file_name:
            csv_file_name = str(nc_file).split(".")[0] + ".csv"
        elif not isinstance(nc_file, (str, Path)) and not csv_file_name:
            raise ValueError("You must provide a CSV file name when input is not a file path.")
        
        # Save to CSV
        save2csv(str(csv_file_name), data_frame, separator, save_index, save_header, date_format)
        
    except Exception as e:
        if "Failed to" in str(e) or "You must provide" in str(e):
            raise  # Re-raise our custom errors
        else:
            raise RuntimeError(f"Unexpected error during CSV conversion: {e}")


def save_da_as_csv(data_array: xr.DataArray, 
                   separator: str = ",",
                   save_index: bool = False,
                   save_header: bool = True,
                   csv_file_name: str | Path | None = None,
                   new_columns: str | list[str] | None = None,
                   date_format: str | None = None) -> None:
    """
    Save a xarray.DataArray object to a CSV file. Data variables may 
    originally be 3D, typically depending on (time, latitude, longitude).

    Parameters
    ----------
    data_array : xarray.DataArray
        DataArray object to save.
    separator : str, default ','
        Separator for the CSV.
    save_index : bool, default False
        Whether to include an index column in the CSV.
    save_header : bool, default True
        Whether to include a header row in the CSV.
    csv_file_name : str or Path, optional
        Name for the CSV file.
    new_columns : str or list of str, optional
        Names for the new columns in the output CSV. Default uses 'time' and variable name.
    date_format : str, optional
        Date format for time data, if present.

    Returns
    -------
    None
        Saves a CSV file and prints success confirmation.
        
    Raises
    ------
    TypeError
        If parameters have incorrect types.
    ValueError
        If required parameters are missing or invalid.
    RuntimeError
        If DataFrame processing or file operations fail.
    """
    # Parameter validation
    if not isinstance(data_array, xr.DataArray):
        raise TypeError("data_array must be an xarray.DataArray")
    
    if not isinstance(separator, str) or not separator:
        raise ValueError("separator must be a non-empty string")
    
    if not isinstance(save_index, bool):
        raise TypeError("save_index must be a boolean")
    
    if not isinstance(save_header, bool):
        raise TypeError("save_header must be a boolean")
    
    if csv_file_name is None:
        raise ValueError("You must provide a CSV file name.")
    
    if not isinstance(csv_file_name, (str, Path)) or not str(csv_file_name).strip():
        raise ValueError("csv_file_name must be a non-empty string or Path")
    
    if new_columns is not None:
        if isinstance(new_columns, str):
            new_columns = [new_columns]
        elif isinstance(new_columns, list):
            new_columns = flatten_list(new_columns)
            if not all(isinstance(col, str) and col.strip() for col in new_columns):
                raise ValueError("All column names must be non-empty strings")
        else:
            raise TypeError("new_columns must be a string, list of strings, or None")
    
    try:
        # Convert to pandas DataFrame
        data_frame = data_array.to_dataframe().reset_index(drop=False)        
        
        # Rename the columns based on the provided new_columns
        if not new_columns:
            date_key = find_dt_key(data_array)
            new_columns = [date_key, data_array.name if data_array.name else "value"]
        
        if len(new_columns) != len(data_frame.columns):
            raise ValueError(f"Number of new column names ({len(new_columns)}) "
                           f"must match number of DataFrame columns ({len(data_frame.columns)})")
        
        data_frame.columns = new_columns
        
        # Save to CSV
        save2csv(str(csv_file_name), data_frame, separator, save_index, save_header, date_format)
        
    except Exception as e:
        if "must match" in str(e) or "You must provide" in str(e):
            raise  # Re-raise our custom errors
        else:
            raise RuntimeError(f"Failed to process DataArray or save to CSV: {e}")
    

# Helpers #
#---------#
        
# Helper function to save an existing dataset with optional attribute updates
def _save_ds_as_nc(xarray_ds: xr.Dataset, file_name: str | Path, attrs_dict: dict | None = None) -> None:
    """
    Helper function to save an xarray Dataset to netCDF format.
    
    Parameters
    ----------
    xarray_ds : xarray.Dataset
        Dataset to save.
    file_name : str or Path
        Output file name.
    attrs_dict : dict, optional
        Global attributes to add to the dataset.
        
    Raises
    ------
    TypeError
        If parameters have incorrect types.
    ValueError
        If file_name is empty.
    RuntimeError
        If file saving fails.
    """
    if not isinstance(xarray_ds, xr.Dataset):
        raise TypeError("xarray_ds must be an xarray.Dataset")
    
    if not isinstance(file_name, (str, Path)) or not str(file_name).strip():
        raise ValueError("file_name must be a non-empty string or Path")
    
    if attrs_dict is not None and not isinstance(attrs_dict, dict):
        raise TypeError("attrs_dict must be a dictionary or None")
    
    if attrs_dict:
        xarray_ds.attrs = attrs_dict
        
    # Add netCDF file extension ('.nc') if not present
    file_name_str = str(file_name)
    if get_obj_specs(file_name_str, "ext") != ".nc":
        file_name_str += ".nc" 
    
    # Save to file
    try:
        xarray_ds.to_netcdf(file_name_str, mode="w", format="NETCDF4")
        print(f"{file_name_str} has been successfully created")
    except Exception as e:
        raise RuntimeError(f"Failed to save netCDF file: {e}")

def _ensure_list(arg: any) -> list:
    """
    Helper function to ensure argument is a list.
    
    Parameters
    ----------
    arg : any
        Argument to convert to list if not already a list.
        
    Returns
    -------
    list
        The argument as a list.
    """
    return arg if isinstance(arg, list) else [arg]


#--------------------------#
# Parameters and constants #
#--------------------------#

# File extensions #
EXTENSIONS = ["nc", "csv"]

# Valid netCDF file formats #
NC_FILE_FORMATS = ["NETCDF4", "NETCDF4_CLASSIC", "NETCDF3_64BIT", "NETCDF3_CLASSIC"]
