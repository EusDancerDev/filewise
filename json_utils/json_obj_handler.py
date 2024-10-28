#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------#
# Import modules #
#----------------#

import json
import os

import pandas as pd

#-----------------------#
# Import custom modules #
#-----------------------#

from pyutils.strings.string_handler import append_ext, get_obj_specs

#------------------#
# Define functions #
#------------------#

# Read from and write to JSON files #
#-----------------------------------#

# Dictionaries #
#-#-#-#-#-#-#-#-

def serialise_dict_to_json(dictionary, 
                           out_file_path=None,
                           indent=4,
                           ensure_ascii=False,
                           sort_keys=False,
                           allow_nan=False,
                           default=None):
    """
    Convert a dictionary to a JSON string and optionally write it to a file.

    Parameters
    ----------
    dictionary : dict
        The dictionary to be converted to JSON format.
    out_file_path : str, optional
        The output file path. If None, the JSON data will only be returned as a string. 
        Default is None.
    indent : int, optional
        The number of spaces to use as indentation in the JSON file. Default is 4.
    ensure_ascii : bool, optional
        If True, all non-ASCII characters in the output are escaped with \\uXXXX sequences. 
        Default is False.
    sort_keys : bool, optional
        If True, the output JSON objects will be sorted by key. Default is False.
    allow_nan : bool, optional
        If True, NaN, Infinity, and -Infinity are allowed in the output. Default is False.
    default : callable, optional
        If specified, this function is called with an object that is not serializable. 
        Default is None.

    Returns
    -------
    str or None
        If out_file_path is None, returns the JSON-formatted string.
        Otherwise, writes the JSON to the specified path and returns None.

    Raises
    ------
    IOError
        If the file cannot be written to the specified path.
    """

    # Construct keyword arguments for json.dumps method
    kwargs = dict(
        indent=indent,
        ensure_ascii=ensure_ascii, 
        sort_keys=sort_keys,
        allow_nan=allow_nan,
        default=default
        )
    
    # Get file specs #
    out_file_parent = get_obj_specs(out_file_path, obj_spec_key="parent")
    out_file_no_rel_path = get_obj_specs(out_file_path, obj_spec_key="name")

    # Serialise dictionary to JSON formatted string
    json_str = json.dumps(dictionary, **kwargs)

    if out_file_path is not None:
        # Determine the output file path
        if not os.path.splitext(out_file_path)[1]:
            out_file_path = append_ext(out_file_path, extensions[0])

        try:
            # Check if file already exists
            if os.path.exists(out_file_path):
                overwrite_stdin = input(
                    f"Warning: file '{out_file_no_rel_path}' "
                    f"at directory '{out_file_parent}' already exists.\n"
                    "Overwrite it? (y/n) "
                    )
                while (overwrite_stdin not in ["y", "n"]):
                    overwrite_stdin = \
                    input("\nPlease enter 'y' for 'yes' or 'n' for 'no': ")
                
                if overwrite_stdin == "n":
                    print("File not overwritten.")
                    return None  # Do not overwrite file
                
            else:
                # Either if chosen not to overwrite or file initially inexistent,
                # write JSON string to new file
                with open(out_file_path, 'w') as f:
                    json.dump(dictionary, f, **kwargs)

            return out_file_path

        except IOError as e:
            raise IOError(f"Could not write to file '{out_file_path}': {e}")

    else:
        # If out_file_path is not provided, return JSON formatted string
        return json_str


def serialise_json_to_dict(in_file_path):
    """
    Convert a JSON file or a JSON-formatted string to a dictionary.

    Parameters 
    ----------
    in_file_path : str
        The input file path, which could be absolute or relative, or a JSON-formatted string.

    Returns
    -------
    dict
        The content of the JSON file or string as a dictionary.

    Raises
    ------
    FileNotFoundError
        If the input file is not found.
    ValueError
        If the content cannot be decoded as JSON.
    """

    # Check if the input is a file path and read from the file #
    if os.path.isfile(in_file_path):
        try:
            with open(in_file_path) as file:
                content_dict = json.load(file)
            return content_dict
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: '{in_file_path}'")
        except json.JSONDecodeError as e:
            raise ValueError(f"Could not decode content from file '{in_file_path}'.") from e
    else:
        # If it's not a file path, try to read it as a JSON-formatted string #
        try:
            content_dict = json.loads(in_file_path)
            return content_dict
        except json.JSONDecodeError as e:
            raise ValueError("Could not decode content from provided JSON string.") from e

       
# Pandas Dataframes #
#-#-#-#-#-#-#-#-#-#-#

def serialise_json_to_df(json_obj_list,
                         encoding="utf-8",
                         orient=None, 
                         typ='frame', 
                         dtype=True,
                         convert_dates=True,
                         keep_default_dates=True,
                         precise_float=False,
                         date_unit=None,
                         encoding_errors='strict'):

    """
    Converts a list of JSON-compatible strings or JSON file paths to a merged Pandas DataFrame.
    
    Parameters
    ----------
    json_obj_list : str or list of str
        A single JSON string or file path, or a list of JSON strings and/or file paths.
    encoding : str
        The encoding to use for reading JSON files, i.e decode py3 bytes.
        Default is 'utf-8'.    
    orient : str, optional
        Indication of expected JSON string format.
        Compatible JSON strings can be produced by ``to_json()`` with a
        corresponding orient value.
        The set of possible orients is:
    
        - ``'split'`` : dict like
          ``{index -> [index], columns -> [columns], data -> [values]}``
        - ``'records'`` : list like
          ``[{column -> value}, ... , {column -> value}]``
        - ``'index'`` : dict like ``{index -> {column -> value}}``
        - ``'columns'`` : dict like ``{column -> {index -> value}}``
        - ``'values'`` : just the values array
        - ``'table'`` : dict like ``{'schema': {schema}, 'data': {data}}``
    
        The allowed and default values depend on the value
        of the `typ` parameter.
    
        * when ``typ == 'series'``,
    
          - allowed orients are ``{'split','records','index'}``
          - default is ``'index'``
          - The Series index must be unique for orient ``'index'``.
    
        * when ``typ == 'frame'``,
    
          - allowed orients are ``{'split','records','index',
            'columns','values', 'table'}``
          - default is ``'columns'``
          - The DataFrame index must be unique for orients ``'index'`` and
            ``'columns'``.
          - The DataFrame columns must be unique for orients ``'index'``,
            ``'columns'``, and ``'records'``.
    
    typ : {'frame', 'series'}
        The type of object to recover (Series or DataFrame). Default is 'frame'.
                          
    dtype : bool or dict
        If True, infer dtypes; if a dict of column to dtype, then use those;
        if False, then don't infer dtypes at all, applies only to the data.
        Defaults to None.
                                         
    convert_dates : bool or list of str, default True
        If True then default datelike columns may be converted (depending on
        keep_default_dates).
        If False, leave dates unconverted.
        If a list of column names, then those columns will be converted and
        default datelike columns may also be converted (depending on
        keep_default_dates).
                               
    keep_default_dates : bool, default True
        Whether to keep the default date conversion.
        If parsing dates (convert_dates is not False), then try to parse the
        default datelike columns.
        A column label is datelike if
    
        * it ends with ``'_at'``,
    
        * it ends with ``'_time'``,
    
        * it begins with ``'timestamp'``,
    
        * it is ``'modified'``, or
    
        * it is ``'date'``.
    
    precise_float : bool
        Set to enable higher precision floating point conversion.
        Default (False) is to use fast but less precise builtin functionality.
        
    date_unit : {'s', 'ms', 'us' or 'ns'}, default None
        The timestamp unit to detect if converting dates.
        The default behaviour is to try and detect the correct precision, 
        but if this is not desired, then pass one of the mentioned options
        to force parsing only seconds, milliseconds, microseconds 
        or nanoseconds respectively.
        
    encoding_errors : str, optional
        How to handle encoding errors. Default is 'strict'.
        List of possible values available at
        https://docs.python.org/3/library/codecs.html#error-handlers_
        

    Returns
    -------
    df : pandas.DataFrame
        A Pandas DataFrame containing the merged data from the input JSON objects.

    Raises
    ------
    ValueError
        If the JSON content cannot be decoded.
    FileNotFoundError
        If a specified JSON file cannot be found.
    """
    
    # If the given path is a string, convert it to a list #
    #-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
    
    if isinstance(json_obj_list, str):
        json_obj_list = [json_obj_list]
    
    # Initialise an empty DataFrame #
    df = pd.DataFrame()
    
    # Iterate over the list of JSON objects or file paths #
    for json_obj in json_obj_list:
        if os.path.isfile(json_obj):
            # If it's a file path, read the JSON file
            try:
                next_df = pd.read_json(json_obj,
                                       encoding=encoding, 
                                       orient=orient, 
                                       typ=typ,
                                       dtype=dtype,
                                       convert_dates=convert_dates,
                                       keep_default_dates=keep_default_dates,
                                       date_unit=date_unit, 
                                       encoding_errors=encoding_errors)

            except FileNotFoundError:
                raise FileNotFoundError(f"File not found: '{json_obj}'")                    
            except ValueError:
                raise ValueError(f"Invalid JSON file content: {json_obj}")

                
        else:
            # If it's not a file path, try to read it as a JSON-formatted string #
            try:
                next_df = pd.read_json(json_obj,
                                       encoding=encoding, 
                                       orient="records", 
                                       typ=typ,
                                       dtype=dtype,
                                       convert_dates=convert_dates,
                                       keep_default_dates=keep_default_dates,
                                       date_unit=date_unit, 
                                       encoding_errors=encoding_errors)
                
            except ValueError:
                raise ValueError("Could not decode content from provided JSON string.")
                
        df = pd.concat([df, next_df], ignore_index=True)
    
    return df

def serialise_df_to_json(df, 
                         out_path=None,
                         orient=None,
                         force_ascii=True,
                         date_unit=None,
                         indent=4, 
                         mode="w"):
    
    """
    Convert a Pandas Dataframe to JSON object or file.
    
    Parameters
    ----------
    df : pandas.DataFrame
        The Dataframe to be converted to JSON.
    out_path : str, path object, file-like object, or None
        String, path object (implementing os.PathLike[str]), or file-like
        object implementing a write() function.
        If None, the result is returned as a string.
    orient : str
        Indication of expected JSON string format.
    
        * Series:
    
            - default is 'index'
            - allowed values are: {'split', 'records', 'index', 'table'}.
    
        * DataFrame:
    
            - default is 'columns'
            - allowed values are: {'split', 'records', 'index', 'columns',
              'values', 'table'}.
    
        * The format of the JSON string:
    
            - 'split' : dict like {'index' -> [index], 'columns' -> [columns],
              'data' -> [values]}
            - 'records' : list like [{column -> value}, ... , {column -> value}]
            - 'index' : dict like {index -> {column -> value}}
            - 'columns' : dict like {column -> {index -> value}}
            - 'values' : just the values array
            - 'table' : dict like {'schema': {schema}, 'data': {data}}
    
            Describing the data, where data component is like ``orient='records'``.
            
    indent : int, optional
        Length of whitespace used to indent each record.
    force_ascii : bool
        Force encoded string to be ASCII. Defaults to True.
    mode : str, default 'w' (writing)
        Specify the IO mode for output when supplying a path_or_buf.
        Accepted args are 'w' (writing) and 'a' (append) only.
        mode='a' is only supported when lines is True and orient is 'records'.
        
    date_unit : {'s', 'ms', 'us' or 'ns'}, default None
        The timestamp unit to detect if converting dates.
        The default behaviour is to try and detect the correct precision, 
        but if this is not desired, then pass one of the mentioned options
        to force parsing only seconds, milliseconds, microseconds 
        or nanoseconds respectively.
       
    Returns
    -------
    None or str
        If 'out_path' is None, returns the resulting JSON format as a string.
        Otherwise, writes the JSON to the specified path and returns None.
        
    Raises
    ------
    ValueError
        If the DataFrame is empty.
    FileNotFoundError
        If the specified file path is not found or is invalid.
    IOError
        If the file cannot be written.
    
    Notes
    -----
    The behaviour of ``indent=0`` varies from the stdlib, which does not
    indent the output but does insert newlines. Currently, ``indent=0``
    and the default ``indent=None`` are equivalent in pandas, though this
    may change in a future release.
    """
    
    # Check if the DataFrame is empty
    if df.empty:
        raise ValueError("The DataFrame is empty and cannot be converted to JSON.")
    
    # Attempt to convert the DataFrame to JSON and handle possible errors
    try:
        result = df.to_json(path_or_buf=out_path,
                            orient=orient,
                            force_ascii=force_ascii,
                            date_unit=date_unit,
                            indent=indent,
                            mode=mode)
        # Return the JSON string if no output path is provided
        return result
    
    except FileNotFoundError:
        raise FileNotFoundError(f"File path not found or invalid: '{out_path}'")
    
    except IOError as e:
        raise IOError(f"Cannot write to file '{out_path}': {e}") from e
    
    except ValueError as e:
        raise ValueError(f"An error occurred while converting DataFrame to JSON: {str(e)}") from e

#--------------------------#
# Parameters and constants #
#--------------------------#

# File extension list #
extensions = ["json"]
