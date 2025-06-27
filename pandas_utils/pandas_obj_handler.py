#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------#
# Import modules #
#----------------#

from numpy import unique
import pandas as pd
# Modern type annotations - no longer need typing imports for basic types

#------------------------#
# Import project modules #
#------------------------#

from filewise.file_operations.ops_handler import remove_files
from filewise.file_operations.path_utils import find_files
from filewise.general.introspection_utils import get_caller_args, get_type_str

from pygenutils.arrays_and_lists.data_manipulation import flatten_list
from pygenutils.arrays_and_lists.patterns import find_duplicated_elements
from pygenutils.strings.string_handler import append_ext, find_substring_index, get_obj_specs
from pygenutils.strings.text_formatters import format_string

#------------------#
# Define functions #
#------------------#

# Data file processing #
#----------------------#

# TXT files #
#-#-#-#-#-#-#

def read_table(file_path: str,
               separator: str = "\s+",
               dtype: dict | None = None,
               engine: str | None = None,
               encoding: str | None = None,
               header: int | list[int] | str | None = "infer",
               names: list | None = None,
               parse_dates: bool | list[int] | list[str] | list[list] | dict = False) -> pd.DataFrame:
 
    """
    Function that uses pandas module to read a text file
    and converts to a data frame.
    
    It assumes that the text file is well organised,
    with no irregular spaces, and that spaces mean 
    there should be different columns.
    
    It is still assumed that the whitespace is one character long
    throughout the whole data frame.
    
    Parameters
    ---------- 
    file_path : str
        Path of the file to be examined.
    separator : str, default '\\t' (tab-stop)
        Delimiter to use. If sep is None, the C engine cannot automatically detect
        the separator, but the Python parsing engine can, meaning the latter will
        be used and automatically detect the separator by Python's builtin sniffer
        tool, ''csv.Sniffer''. In addition, separators longer than 1 character and
        different from ''\s+'' will be interpreted as regular expressions and
        will also force the use of the Python parsing engine. Note that regex
        delimiters are prone to ignoring quoted data. Regex example: '\r\t'.
    dtype : Type name or dict of column -> type, optional
        Data type for data or columns. E.g. {'a': np.float64, 'b': np.int32,
        'c': 'Int64'}
        Use 'str' or 'object' together with suitable 'na_values' settings
        to preserve and not interpret dtype.
        If converters are specified, they will be applied INSTEAD
        of dtype conversion.
    engine : {'c', 'python', 'pyarrow'}, optional
        Parser engine to use. The C and pyarrow engines are faster, 
        while the python engine is currently more feature-complete. 
        Multithreading is currently only supported by the pyarrow engine.
        Defaults to None.
    encoding : str
        String that identifies the encoding to use for UTF
        when reading/writing.
        Default value is 'utf-8' but it can happen that
        the text file has internal strange characters that
        UTF-8 encoding is not able to read.
        In such cases "latin1" is reccommended to use.
   
    header : int | list[int] | None, default 'infer'
        Row number(s) to use as the column names, and the start of the data.
        Default behaviour is to infer the column names: if no names are passed
        the behaviour is identical to header=0 and column names are inferred
        from the first line of the file.
        
        If column names are passed explicitly then the behaviour
        is identical to header=None, where the text file's header
        are only column names.
        
        Explicitly pass header=0 to be able to replace existing names.
        The header can be a list of integers that specify row locations
        for a multi-index on the columns e.g. [0,1,3].
        
        This parameter ignores commented lines and empty lines if
        skip_blank_lines=True (not included in the arguments for simplicity),
        so header=0 denotes the first line of data
        rather than the first line of the file.
    names : array-like, optional
        List of column names to use. If the file contains a header row,
        then you should explicitly pass header=0 to override the column names.
        Duplicates in this list are not allowed.
    parse_dates : bool | list[int] | list[str] | list[list] | dict, default False
        The behaviour is as follows:
            * boolean. If True -> try parsing the index.
            * list of int or names. e.g. If [1, 2, 3] -> try parsing columns 1, 2, 3
              each as a separate date column.
            * list of lists. e.g.  If [[1, 3]] -> combine columns 1 and 3 and parse as
              a single date column.
            * dict, e.g. {'foo' : [1, 3]} -> parse columns 1, 3 as date and call
              result 'foo'
          
    Returns
    -------
    new_df : pandas.Dataset
        Text file converted to a data frame.
    """
     
    df = pd.read_table(file_path,
                       engine=engine,
                       encoding=encoding,
                       header=header,
                       sep=separator,
                       dtype=dtype,
                       names=names,
                       parse_dates=parse_dates)
    return df



# DataFrame column name handling #
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

def polish_df_column_names(df: pd.DataFrame, sep_to_polish: str = "\n") -> pd.DataFrame:
    """
    Function to polish a Pandas DataFrames' column names, by eliminating
    the specified separator that might appear when reading files such as
    Microsoft Excel or LibreOffice Calc document.
    
    It uses the 'rename' method to rename the columns by using a 'lambda';
    it simply takes the final entry of the list obtained by splitting 
    each column name any time there is a new line.
    If there is no new line, the column name is unchanged.
    
    Parameters
    ----------
    df : pandas.Dataframe
        Dataframe containing data
    sep_to_polish : str
        Separator to detect and eliminate from the string formed
        by all column names.
        
    Returns
    -------
    df_fixed : pandas.Dataframe
        Dataframe containing exactly the same data as the input one,
        with column names polished accordingly.    
    """
    
    df_fixed = df.rename(columns=lambda x: x.split(sep_to_polish)[-1])
    return df_fixed

# DataFrame time series handling #
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-

def _standardise_time_series_core(
    dfs: list[pd.DataFrame],
    date_value_pairs: list[tuple[str, str]]
) -> tuple[list[tuple], pd.Index]:
    """
    Core functionality for time series standardisation.
    
    Parameters
    ----------
    dfs : list[pd.DataFrame]
        List of input DataFrames to standardise.
    date_value_pairs : list[tuple[str, str]]
        List of (date_column, value_column) pairs for each DataFrame.
        
    Returns
    -------
    tuple[list[tuple], pd.Index]
        A tuple containing:
        - List of processed series with their value column names
        - Common date index for all series
    """
    from pygenutils.time_handling.time_formatters import parse_dt_string
    
    # Check if the number of DataFrames matches the number of date-value pairs
    if len(dfs) != len(date_value_pairs):
        raise ValueError("Number of DataFrames must match number of date-value pairs")
    
    # Extract and process each time series
    processed_series = []
    for df, (date_col, value_col) in zip(dfs, date_value_pairs):
        # Make a copy to avoid modifying the original
        df_copy = df.copy()
        
        # Convert date column to datetime
        df_copy[date_col] = parse_dt_string(df_copy[date_col], module="pandas")
        
        # Extract series and set date as index
        series = df_copy[[date_col, value_col]].dropna(subset=[date_col]).set_index(date_col)
        processed_series.append((series, value_col))
    
    # Find union of all dates
    all_dates = pd.Index([])
    for series, _ in processed_series:
        all_dates = all_dates.union(series.index)
    all_dates = all_dates.sort_values()
    
    return processed_series, all_dates

def standardise_time_series(
    dfs: list[pd.DataFrame],
    date_value_pairs: list[tuple[str, str]],
    handle_duplicates: bool = True,
    separate: bool = False,
    return_format: str = 'dict',
    reset_index: bool = False,
    drop: bool = False,
    names: str | list[str] | None = None
) -> pd.DataFrame | dict[str, pd.DataFrame] | list[pd.DataFrame]:
    """
    Standardise multiple time series DataFrames into a single DataFrame with a common date index,
    or as separate DataFrames sharing the same date index.
    
    Parameters
    ----------
    dfs : list[pd.DataFrame]
        List of input DataFrames to standardise.
    date_value_pairs : list[tuple[str, str]]
        List of (date_column, value_column) pairs for each DataFrame.
    handle_duplicates : bool, default True
        If True, adds numerical suffixes to duplicate column names.
        Only used when separate=False.
    separate : bool, default False
        If True, returns separate DataFrames instead of merging them.
        If False, returns a single merged DataFrame.
    return_format : str, default 'dict'
        Format to return the standardised DataFrames when separate=True. Options:
        - 'dict': Dictionary with value column names as keys
        - 'list': List of DataFrames in the same order as input
    reset_index : bool, default False
        Whether to reset the index for separate DataFrames (only applies when separate=True).
        If True, the datetime index becomes a regular column.
    drop : bool, default False
        Whether to drop the index column when resetting the index (only applies when reset_index=True).
    names : str | list[str] | None, default None
        Name(s) to use for the former index levels when resetting the index.
        Only applies when reset_index=True and drop=False.
        If a string, the same name is used for all DataFrames.
        If a list of strings, each string is applied to the corresponding DataFrame.
        The list length should match the number of DataFrames.
        
    Returns
    -------
    pd.DataFrame or dict or list
        If separate=False: A single DataFrame with all values aligned to a common date index.
        If separate=True and return_format='dict': Dictionary of DataFrames with value column names as keys.
        If separate=True and return_format='list': List of DataFrames in the original order.
        
    Raises
    ------
    ValueError
        If the lengths of dfs and date_value_pairs do not match,
        or if return_format is not one of the supported options,
        or if names is a list with length not matching the number of DataFrames,
        or if names is a list when separate=False (merged DataFrame output).
        
    Examples
    --------
    >>> df1 = pd.DataFrame({'Date1': ['2025-01-01', '2025-01-02'], 'Value1': [1.2, 3.4]})
    >>> df2 = pd.DataFrame({'Date2': ['2025-01-02', '2025-01-03'], 'Value2': [5.6, 7.8]})
    >>> # Merged result (default)
    >>> merged = standardise_time_series([df1, df2], [('Date1', 'Value1'), ('Date2', 'Value2')])
    >>> # Separate DataFrames as dict
    >>> separate_dict = standardise_time_series([df1, df2], [('Date1', 'Value1'), ('Date2', 'Value2')], separate=True)
    >>> # Separate DataFrames with same index name
    >>> separate_reset = standardise_time_series([df1, df2], [('Date1', 'Value1'), ('Date2', 'Value2')], 
    ...                                          separate=True, reset_index=True, names='timestamp')
    >>> # Separate DataFrames with different index names
    >>> separate_reset = standardise_time_series([df1, df2], [('Date1', 'Value1'), ('Date2', 'Value2')], 
    ...                                          separate=True, reset_index=True, names=['timestamp1', 'timestamp2'])
    """
    # Get common processed series and date index
    processed_series, all_dates = _standardise_time_series_core(dfs, date_value_pairs)
    
    # Check if names is a list but we're in merged mode
    if not separate and isinstance(names, list):
        raise ValueError("When separate=False (merged DataFrame output), names cannot be a list. "
                         "Use a single string for names or set separate=True.")
    
    # Return separate DataFrames if requested
    if separate:
        # Validate return format
        valid_return_formats = ['dict', 'list']
        if return_format not in valid_return_formats:
            raise ValueError(f"return_format must be one of {valid_return_formats}")
        
        # Validate names if it's a list
        if reset_index and isinstance(names, list):
            if len(names) != len(dfs):
                raise ValueError(f"If names is a list, its length ({len(names)}) must match "
                                f"the number of DataFrames ({len(dfs)})")
        
        # Create separate DataFrames
        result = {}
        for i, (series, value_col) in enumerate(processed_series):
            # Create a new DataFrame with the standardised index
            reindexed = series.reindex(all_dates)
            
            # Reset index if requested
            if reset_index:
                # Apply the appropriate name based on the type of names
                if isinstance(names, list):
                    index_name = names[i]
                else:
                    index_name = names
                
                reindexed = reindexed.reset_index(drop=drop, names=index_name)
                
            result[value_col] = reindexed
        
        # Return in the requested format
        if return_format == 'list':
            return [result[value_col] for _, value_col in date_value_pairs]
        else:  # return_format == 'dict'
            return result
    
    # Else return a single merged DataFrame (original behavior)
    else:
        result_dict = {}
        column_counts = {}
        
        for series, value_col in processed_series:
            reindexed = series.reindex(all_dates)
            
            # Handle duplicate column names if needed
            if handle_duplicates and value_col in result_dict:
                if value_col not in column_counts:
                    # First duplicate: rename the existing column
                    column_counts[value_col] = 1
                    old_key = value_col
                    new_key = f"{value_col}_{column_counts[value_col]}"
                    result_dict[new_key] = result_dict.pop(old_key)
                    column_counts[value_col] += 1
                
                # Add the new column with a suffix
                new_col_name = f"{value_col}_{column_counts[value_col]}"
                result_dict[new_col_name] = reindexed[value_col]
                column_counts[value_col] += 1
            else:
                result_dict[value_col] = reindexed[value_col]
        
        # Combine into a single DataFrame
        standardised_df = pd.DataFrame(result_dict, index=all_dates)
        return standardised_df


# Microsoft Excel spreadsheets #
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-

def excel_handler(file_path, 
                  sheet_name=None,
                  header=None,
                  engine=None,
                  decimal='.', 
                  return_obj_type='dict'):
    
    """
    Reads an Excel file and processes its sheets either into a 
    dictionary of DataFrames or a single merged DataFrame.

    Parameters
    ----------
    file_path : str
        Path to the Excel file.
    sheet_name : str | int | list[str] | list[int] | None, default 0
        Strings are used for sheet names. Integers are used in zero-indexed
        sheet positions (chart sheets do not count as a sheet position).
        Lists of strings/integers are used to request multiple sheets.
        Specify ``None`` to get all worksheets.
    header : int | list[int] | None, default None
        Row (0-indexed) to use for the column labels of the parsed DataFrame.
    engine : {'openpyxl', 'calamine', 'odf', 'pyxlsb', 'xlrd'}, default None
        Engine to use for reading Excel files. If None, defaults to the 
        appropriate engine for the file type.
    decimal : str, default '.'
        Character to recognise as decimal point (e.g., ',' in Europe).
    return_obj_type : str, default 'dict'
        Type of output to return. Must be either 'dict' to return a dictionary
        of DataFrames, or 'df' to return a single merged DataFrame.

    Returns 
    -------
    dict or pd.DataFrame
        If 'return_type' is 'dict', returns a dictionary where keys are
        sheet names and values are DataFrames.
        If 'return_type' is 'df', returns a single DataFrame
        with data from all sheets merged.

    Raises
    ------
    TypeError
        If 'return_type' is not 'dict' or 'df'.

    Examples
    --------
    result_dict = excel_handler('file_path.xlsx', return_type='dict')
    result_df = excel_handler('file_path.xlsx', return_type='df')
    """
    
    # Validate the return type argument #
    if return_obj_type not in EXCEL_HANDLING_RETURN_OPTIONS:
        raise TypeError("Invalid type of the object to return. "
                        f"Choose one from {EXCEL_HANDLING_RETURN_OPTIONS}.")

    else:
        sheetname_and_data_dict = pd.read_excel(file_path,
                                                sheet_name=sheet_name,
                                                header=header,
                                                engine=engine,
                                                decimal=decimal)
    
        if return_obj_type == 'dict':
            polished_sheetname_and_val_dict = {}
            for sheet_name, sheet_df in sheetname_and_data_dict.items():
                df_polished_colnames = polish_df_column_names(sheet_name, sheet_df)
                indiv_polished_dict = {sheet_name: df_polished_colnames}
                polished_sheetname_and_val_dict.update(indiv_polished_dict)
            return polished_sheetname_and_val_dict
    
        elif return_obj_type == 'df':
            all_value_df = pd.DataFrame()
            for sheet_name, sheet_df in sheetname_and_data_dict.items():
                df_polished_colnames = polish_df_column_names(sheet_name, sheet_df)
                all_value_df = pd.concat([all_value_df, df_polished_colnames])
                
            all_value_df.reset_index(inplace=True, drop=True)
            all_value_df = all_value_df.drop(columns=['sheet'])
            return all_value_df

def save2excel(file_path,
               frame_obj,
               indiv_sheet_name="Sheet1",
               save_index=False,
               save_header=False,
               engine="xlsxwriter"):
    
    """
    Save a DataFrame or a dictionary of DataFrames to an Excel file with separate sheets.

    Parameters
    ----------
    file_path : str
        Path to the Excel file where data will be saved.
    frame_obj : dict or pandas.DataFrame
        Data to be saved to the Excel file. If a dictionary is provided,
        keys are used as sheet names and values as DataFrames.
        If a single DataFrame is provided, it will be saved to one sheet.
    indiv_sheet_name : str, optional
        Name of the sheet to give when 'frame_obj' is a single DataFrame.
        Default is "Sheet1".
    save_index : bool, optional
        Whether to include the DataFrame index as a column in the Excel sheet. Default is False.
    save_header : bool, optional
        Whether to include the DataFrame column headers in the Excel sheet. Default is False.
    engine : {'openpyxl', 'xlsxwriter'}, optional
        The engine to use for writing to the Excel file. Default is "xlsxwriter".

    Returns
    -------
    int
        Always returns 0 to indicate successful execution.

    Examples
    --------
    Save a single DataFrame to an Excel file:
    
    >>> df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
    >>> save2excel("output.xlsx", df)

    Save multiple DataFrames to an Excel file with custom sheet names:
    
    >>> dfs = {"Sheet1": pd.DataFrame({"A": [1, 2]}), "Sheet2": pd.DataFrame({"B": [3, 4]})}
    >>> save2excel("output.xlsx", dfs)
    """
    
    # Get the file path's components #
    #--------------------------------#
    
    # Extension #
    """
    There can be some times in which the file does not have any extension,
    as a result of any other manipulation with any of the modules of this package.
    If so, Excel file extension is automatically added.
    """
    file_ext = get_obj_specs(file_path, obj_spec_key="ext")
    extension_length = len(file_ext)
    
    if extension_length == 0:
        file_path = append_ext(file_path, EXTENSIONS[1])
    
    # Name and parent #
    file_name = get_obj_specs(file_path, obj_spec_key="name")
    fn_parent = get_obj_specs(file_path, obj_spec_key="parent")
    
    # Check if the file already exists #
    #----------------------------------#
    
    file_already_exists\
    = bool(len(find_files(file_name, fn_parent, match_type="glob", top_only=True)))
    
    # Save the file according to the input data type #
    #------------------------------------------------#
    
    if isinstance(frame_obj, dict):
        writer = pd.ExcelWriter(file_path, engine=engine)
        
        for sheet, frame in frame_obj.items():
            frame.to_excel(writer,
                           sheet_name=sheet,
                           index=save_index,
                           header=save_header)
            
        # If the file to be created already exists, prompt to overwrite it #    
        if file_already_exists:
            format_args_file_exists = [file_name, fn_parent]
            overwrite_stdin\
            = input(format_string(ALREADY_EXISTING_FILE_WARNING_TEMPLATE, format_args_file_exists))
            
            while (overwrite_stdin != "y" and overwrite_stdin != "n"):
                overwrite_stdin = input(OVERWRITE_PROMPT_WARNING)
            else:  
                # In this case, save the file directly
                if overwrite_stdin == "y":
                    writer.close() 
                    return 0
                else:
                    pass
        
        # Else, save it directly #
        else:
            writer.close()
            return 0


    elif isinstance(frame_obj, pd.DataFrame):
        
        # If the file to be created already exists, prompt to overwrite it #    
        if file_already_exists:
            format_args_file_exists = [file_name, fn_parent]
            overwrite_stdin\
            = input(format_string(ALREADY_EXISTING_FILE_WARNING_TEMPLATE, format_args_file_exists))
            
            while (overwrite_stdin != "y" and overwrite_stdin != "n"):
                overwrite_stdin = input(OVERWRITE_PROMPT_WARNING)
            else:
                # If chosen to overwrite, data cannot be directly overriden.
                # Instead, delete the original file and create a new one
                # of the same name with the new data
                if overwrite_stdin == "y":
                    remove_files(file_path, fn_parent, match_type="glob")
                    frame_obj.to_excel(file_path, 
                                       sheet_name=indiv_sheet_name,
                                       index=save_index,
                                       header=save_header)
                    return 0
                else:
                    pass
          
        # Else, save it directly #
        else:
            frame_obj.to_excel(file_path, save_index, save_header)
            return 0
        
    else:
        raise TypeError("Unsupported type of frame. "
                        "It must either be of type 'dict' or 'pandas.DataFrame'.")
        

def merge_excel_files(input_file_list: str | list,
                      output_file_path: str,
                      header: int | list[int] | None = None,
                      engine: str | None = None,
                      decimal: str = ".",
                      save_index: bool = False,
                      save_header: bool = False,
                      save_merged_file: bool = False) -> int | dict:
    """
    Merge data from multiple Excel files into a single Excel file or dictionary.

    Parameters
    ----------
    input_file_list : str | list[str]
        Path or paths of the input Excel file(s) to be merged.
    output_file_path : str
        Path or name of the output Excel file. If 'save_merged_file' is False,
        this parameter is ignored.
    header : int | list[int] | None, default None
        Row (0-indexed) to use for the column labels of the parsed DataFrame.
        If a list of integers is passed, those row positions will be combined
        into a ``MultiIndex``. Use None if there is no header.
    engine : str | sqlalchemy.engine.base.Engine, optional
        SQLAlchemy engine or connection string for connecting to database files.
    decimal : str, default '.'
        Character recognised as decimal separator.
    save_index : bool, default False
        Whether to include a column in the output Excel file that identifies row numbers.
    save_header : bool, default False
        Whether to include a row in the output Excel file that identifies column numbers.
    save_merged_file : bool, default False
        Whether to save the merged data as an Excel file.

    Returns
    -------
    int or dict
        If 'save_merged_file' is True, returns 0 to indicate successful file saving.
        If 'save_merged_file' is False, returns a dictionary containing DataFrames
        with merged data, separated by file names.

    Raises
    ------
    ValueError
        If 'input_file_list' contains only one file.

    Notes
    -----
    If multiple files contain sheets with identical names, the function appends
    the original file name to the sheet names to avoid key conflicts
    in the output dictionary.
    """
    
    # Quality control section #
    if isinstance(input_file_list, str):
        input_file_list = [input_file_list]
    elif isinstance(input_file_list, list):
        input_file_list = flatten_list(input_file_list)
        
    input_file_count = len(input_file_list)    
    if input_file_count == 1:
        raise ValueError(BELOW_MINIMUM_FILE_WARNING)
        
    # For simplicity and convenience, even if any file has only one sheet, 
    # follow the natural behaviour, that is, conserving the key containing
    # object as a list, instead of indexing to an integer
    all_file_sheetname_list_of_lists = [list(excel_handler(file, 
                                                           engine=engine,
                                                           return_type='dict').keys())
                                        for file in input_file_list]
    
    
    """
    Handle duplicated sheet names, if any, by adding the corresponding
    file name after it. Otherwise, because in a dictionary cannot appear
    repeated keys, the information pertaining to the second key and beyond,
    among the duplicated ones, will be lost.
        
    For example, if the previous instruction gives a list of lists 
    like the following one:
        
    [['sheet1', 'test_sheet'], ['sheet1', 'savings']]
    
    To identify the duplicated names, as well as remembering which
    file do they correspond to:
    
    - Each individual list corresponds to the sheets contained in a file,
      which will be identified as a key.
    - A first index is necessary to idenfity which file does the potentially
      duplicated element correspond to, i.e. the position of the individual list.
    - Another index serves to locate the duplicated element within the
      mentioned individual list and modify its name.
      * The previous two indices will be contained in a tuple.
      * Because duplicated elements appear minimum twice,
        there will be more than one tuple, contained in a list,
        in order to preserve performance.
      
    The application of the function results in a dictionary as follows:
    res_dict = {'sheet1' : [(0,0), (1,0)]}
    
    In this case, the repeated key is 'sheet1', which appears in the sheets
    of the first and second file (first indices 0 and 1, respectively),
    and that sheet name is located in the first position for both files
    (second index 0 in both cases).
    """
    duplicated_sheetname_index_dict = find_duplicated_elements(all_file_sheetname_list_of_lists)
    duplicate_sheet_count = len(duplicated_sheetname_index_dict)
    if duplicate_sheet_count > 0:
        for sheet_name in list(duplicated_sheetname_index_dict.keys()):
            index_tuple_list = duplicated_sheetname_index_dict[sheet_name]
            for tupl in index_tuple_list:
                new_sheet_name = f"{sheet_name}_{input_file_list[tupl[0]]}"
                all_file_sheetname_list_of_lists[tupl[0]][tupl[1]] = new_sheet_name
        
    all_file_sheetname_list_of_lists = [lst[i] 
                                        for lst in all_file_sheetname_list_of_lists
                                        for i in range(len(lst))]
    

    # Gather data #     
    all_file_data_dict = {file_sheetname : excel_handler(file, 
                                                         header=header,
                                                         engine=engine, 
                                                         decimal=decimal,
                                                         return_type='dict')
                          for file_sheetname, file in zip(all_file_sheetname_list_of_lists, 
                                                          input_file_list)}

    # File saving 
    if save_merged_file:
        saving_result = save2excel(output_file_path,
                                   all_file_data_dict, 
                                   save_index=save_index, 
                                   save_header=save_header)
        return saving_result
     
    else:
        return all_file_data_dict
        

# CSV files #
#-#-#-#-#-#-#

def save2csv(file_path,
             data_frame,
             separator=',',
             save_index=False,
             save_header=False,
             decimal=".",
             date_format=None):
    """
    Save a DataFrame to a CSV file.

    Parameters
    ----------
    file_path : str
        Path of the output CSV file.
    data_frame : pandas.DataFrame
        DataFrame containing the data to be saved.
    separator : str, default ','
        String used to separate data columns.
    save_index : bool, default False
        Whether to include a column in the CSV file that identifies row numbers.
    save_header : bool, default False
        Whether to include a row in the CSV file that identifies column names.
    decimal : str, default '.'
        Character recognised as the decimal separator.
    date_format : str, optional
        Format string for datetime columns.

    Returns
    -------
    int
        Returns 0 to indicate successful execution.

    Raises
    ------
    TypeError
        If 'data_frame' is not of type 'pandas.DataFrame'.

    Notes
    -----
    - This function is designed to work with simple CSV files, typically with only one sheet.
    - If 'file_path' does not have a file extension, '.csv' is automatically appended to it.
    - If the specified file already exists, the function prompts to confirm overwrite before saving.
    """

    
    if isinstance(data_frame, pd.DataFrame):
        
        # Get the file path's components #
        #--------------------------------#
        
        # Extension #
        """
        There can be some times in which the file does not have any extension,
        as a result of any other manipulation with any of the modules of this package.
        If so, Excel file extension is automatically added.
        """
        
        file_ext = get_obj_specs(file_path, obj_spec_key="ext")
        extension_length = len(file_ext)
        
        if extension_length == 0:
            file_path = append_ext(file_path, EXTENSIONS[0])
        
        
        # Name and parent #
        file_name = get_obj_specs(file_path, obj_spec_key="name")
        fn_parent = get_obj_specs(file_path, obj_spec_key="parent")
        
        # Check if the file already exists #
        #----------------------------------#
        
        file_already_exists\
        = bool(len(find_files(file_name, fn_parent, match_type="glob", top_only=True)))
        
        # Save the file according to the input data type #
        #------------------------------------------------#
        
        if date_format is None:
            
            # If the file to be created already exists, prompt to overwrite it #  
            if file_already_exists:
                format_args_file_exists = [file_name, fn_parent]
                overwrite_stdin\
                = input(format_string(ALREADY_EXISTING_FILE_WARNING_TEMPLATE, format_args_file_exists))
                
                while (overwrite_stdin != "y" and overwrite_stdin != "n"):
                    overwrite_stdin = input(OVERWRITE_PROMPT_WARNING)
                else:
                    # If chosen to overwrite, data cannot be directly overriden.
                    # Instead, delete the original file and create a new one
                    # of the same name with the new data
                    if overwrite_stdin == "y":
                        remove_files(file_path, fn_parent, match_type="glob")
                        data_frame.to_csv(file_path,
                                          sep=separator,
                                          decimal=decimal,
                                          index=save_index,
                                          header=save_header)
                        return 0
                    else:
                        pass
                
            # Else, save it directly #
            else:
                data_frame.to_csv(file_path,
                                  sep=separator,
                                  decimal=decimal,
                                  index=save_index,
                                  header=save_header)
                return 0
                
            
        else:
            # If the file to be created already exists, prompt to overwrite it #  
            if file_already_exists:
                format_args_file_exists = [file_name, fn_parent]
                overwrite_stdin\
                = input(format_string(ALREADY_EXISTING_FILE_WARNING_TEMPLATE, format_args_file_exists))
                
                while (overwrite_stdin != "y" and overwrite_stdin != "n"):
                    overwrite_stdin = input(OVERWRITE_PROMPT_WARNING)
                else:
                    # If chosen to overwrite, data cannot be directly overriden.
                    # Instead, delete the original file and create a new one
                    # of the same name with the new data
                    if overwrite_stdin == "y":
                        remove_files(file_path, fn_parent, match_type="glob")
                        data_frame.to_csv(file_path,
                                          sep=separator,
                                          decimal=decimal,
                                          date_format=date_format,
                                          index=save_index,
                                          header=save_header)
                        return 0                        
                    else:
                        pass
                
            # Else, save it directly #
            else:
                data_frame.to_csv(file_path,
                                  sep=separator,
                                  decimal=decimal,
                                  date_format=date_format,
                                  index=save_index,
                                  header=save_header)
                return 0
            
    else:        
        input_obj_type = get_type_str(data_frame)
        raise TypeError(format_string(UNSUPPORTED_OBJ_TYPE_ERR_TEMPLATE, input_obj_type))
        
        
    
def csv2df(file_path,
           separator=None,
           engine="python",
           encoding=None,
           header='infer',
           parse_dates=False,
           index_col=None,
           decimal="."):
    
    
    """
    Function that loads a CSV file and loads the content
    into a Pandas DataFrame to a CSV file.
    
    Parameters
    ----------
    file_path : str
        Path of the file to evaluate.
    sep : str, default None
        Character or regex pattern to treat as the delimiter. If ``sep=None``, the
        C engine cannot automatically detect
        the separator, but the Python parsing engine can, meaning the latter will
        be used and automatically detect the separator from only the first valid
        row of the file by Python's builtin sniffer tool, ``csv.Sniffer``.
        In addition, separators longer than 1 character and different from
        ``'\s+'`` will be interpreted as regular expressions and will also force
        the use of the Python parsing engine. Note that regex delimiters are prone
        to ignoring quoted data. Regex example: ``'\r\t'``.
    engine : {'c', 'python', 'pyarrow'}, default 'python'
        Parser engine to use. The C and pyarrow engines are faster, 
        while the python engine is currently more feature-complete. 
        Multithreading is currently only supported by the pyarrow engine.
        Defaults to None.
    encoding : str
        Encoding to use for UTF when reading or writing.
        When this is 'None', 'errors="replace"' is passed to 'open()'; 
        technically no encoding is used.
        Otherwise, 'errors="strict"' is passed to 'open()'.
    header : int | list[int] | str | None
        Row number(s) to use as the column names, and the start of the
        data. Default behaviour is to infer the column names: if no names
        are passed the behaviour is identical to 'header=0' and column
        names are inferred from the first line of the file, if column
        names are passed explicitly then the behaviour is identical to
        'header=None'. Explicitly pass 'header=0' to be able to
        replace existing names.
    parse_dates : bool | list[int] | list[str] | list[list] | dict, default False
        The behaviour is as follows:
            * boolean. If True -> try parsing the index.
            * list of int or names. e.g. If [1, 2, 3] -> try parsing columns 1, 2, 3
              each as a separate date column.
            * list of lists. e.g.  If [[1, 3]] -> combine columns 1 and 3 and parse as
              a single date column.
            * dict, e.g. {'foo' : [1, 3]} -> parse columns 1, 3 as date and call
              result 'foo'
    
    index_col : int, str, sequence of int / str, False or NoneType
        Column(s) to use as the row labels of the 'DataFrame', either given as
        string name or column index. If a sequence of int / str is given, a
        MultiIndex is used.
    decimal : str, default '.'
        Character to recognise as decimal point for parsing string columns to numeric.
        Note that this parameter is only necessary for columns stored as TEXT in Excel,
        any numeric columns will automatically be parsed, regardless of display
        format (e.g. use ',' for European data).      
        
    Returns
    -------
    df : pandas.DataFrame
        Single DataFrame containing data of the CSV file, molded according to
        the reading parameters.
    """

    df = pd.read_csv(file_path, 
                     sep=separator,
                     decimal=decimal,
                     encoding=encoding,
                     header=header,
                     engine=engine,
                     parse_dates=parse_dates,
                     index_col=index_col)    
    return df


def merge_csv_files(input_file_list: str | list, 
                    output_file_path: str,
                    separator_in: str | None = None,
                    separator_out: str = ";",
                    engine: str = "python",
                    encoding: str | None = None,
                    header: int | list[int] | str | None = 'infer',
                    parse_dates: bool | list[int] | list[str] | list[list] | dict = False,
                    index_col: int | str | list | None = None,
                    decimal: str = ",",                                 
                    save_index: bool = False,
                    save_header: bool = False,
                    out_single_DataFrame: bool = True,
                    keep_data_in_sections: bool = False,
                    save_merged_file: bool = False) -> int | pd.DataFrame | dict:

    """
    Merges several CSV files' data into a single one.

    Two options are given:
        1. Merge data of each file into a single DataFrame.
        2. Do not concatenate all DataFrames, but store them separately
           with their corresponding file in a dictionary.
           
    Parameters
    ----------
    input_file_list : str | list[str]
        Path or paths of the files to be examined.   
        Each of them can be names or relative paths.
    output_file_path: str
        Name or path of the output file. It can either be a name or relative path.
    separator_in : str, default None
        Character or regex pattern to treat as the delimiter. If ``sep=None``, the
        C engine cannot automatically detect
        the separator, but the Python parsing engine can, meaning the latter will
        be used and automatically detect the separator from only the first valid
        row of the file by Python's builtin sniffer tool, ``csv.Sniffer``.
        In addition, separators longer than 1 character and different from
        ``'\s+'`` will be interpreted as regular expressions and will also force
        the use of the Python parsing engine. Note that regex delimiters are prone
        to ignoring quoted data. Regex example: ``'\r\t'``.        
    separator_out : str, default ';'
        Delimiter to use for the output file.    
    engine : {'c', 'python', 'pyarrow'}, default 'python'
        Parser engine to use. The C and pyarrow engines are faster, 
        while the python engine is currently more feature-complete. 
        Multithreading is currently only supported by the pyarrow engine.
        Defaults to None.
    encoding : str
        String that identifies the encoding to use for UTF
        when reading/writing.
        Default value is 'utf-8' but it can happen that
        the text file has internal strange characters that
        UTF-8 encoding is not able to read.
        In such cases "latin1" is reccommended to use.
   
    header : int | list[int] | None, default 'infer'
        Row number(s) to use as the column names, and the start of the data.
        Default behaviour is to infer the column names: if no names are passed
        the behaviour is identical to header=0 and column names are inferred
        from the first line of the file.
        
        If column names are passed explicitly then the behaviour
        is identical to header=None, where the text file's header
        are only column names.
        
        Explicitly pass header=0 to be able to replace existing names.
        The header can be a list of integers that specify row locations
        for a multi-index on the columns e.g. [0,1,3].
        
        This parameter ignores commented lines and empty lines if
        skip_blank_lines=True (not included in the arguments for simplicity),
        so header=0 denotes the first line of data
        rather than the first line of the file.
        
    parse_dates : bool | list[int] | list[str] | list[list] | list[dict], default False
        The behaviour is as follows:
            * boolean. If True -> try parsing the index.
            * list of int or names. e.g. If [1, 2, 3] -> try parsing columns 1, 2, 3
              each as a separate date column.
            * list of lists. e.g.  If [[1, 3]] -> combine columns 1 and 3 and parse as
              a single date column.
            * dict, e.g. {'foo' : [1, 3]} -> parse columns 1, 3 as date and call
              result 'foo'
    
    index_col : int, str, sequence of int / str, False or NoneType
        Column(s) to use as the row labels of the 'DataFrame', either given as
        string name or column index. If a sequence of int / str is given, a
        MultiIndex is used.
    decimal : str
        Character to recognise as decimal point (e.g. use ',' 
        for European data). Default value is ',' (comma).    
    save_index : bool, optional
        Whether to include the DataFrame index as a column in the Excel sheet. Default is False.
    save_header : bool, optional
        Whether to include the DataFrame column headers in the Excel sheet. Default is False.
    out_single_DataFrame : bool, default True
        Determines whether to save all DataFrames into a single one,
        concatenating all of them.
        The counterpart is that if not all of them have the same number
        of rows, the concatenation results in NaN filling.
    keep_data_in_sections : bool, default False
        If chosen, instead of concatenating all DataFrames, each one
        is stored in a dictionary, with the original file name 
        (without the relative path) being the key.
    save_merged_file : bool, default False
        Determines to save the object returned by the choice of the
        previous two arguments.
    
    Returns
    -------
    int
        Irrespective of 'out_single_DataFrame' and/or 'keep_data_in_sections'
        being True or False, if 'save_merged_file', 
        always returns 0 to indicate successful execution.
    all_file_data_df : pandas.DataFrame
        If 'out_single_DataFrame' is set to True, 
        (while 'keep_data_in_sections' to False)
        and 'save_merged_file' to False, the concatenated DataFrame is returned.
    all_file_data_dict : dict
        If 'keep_data_in_sections' is set to True 
        (while 'out_single_DataFrame' to False)
        and 'save_merged_file' to False, the dictionary with DataFrames
        separated by files as keys is returned.
        
    Notes
    -----   
    Usage of 'separator_in' applies for all files, which means
    that every file must have the same separator.
    In order to keep simplicity and practicality, 'out_single_DataFrame'
    and 'keep_data_in_sections' cannot be True at the same time.
    """
        
    # Proper argument selection control # 
    #-----------------------------------#
    
    # Data merging #
    param_keys = get_caller_args()
    kdis_arg_pos = find_substring_index(param_keys, "keep_data_in_sections")
    osd_arg_pos = find_substring_index(param_keys, "out_single_DataFrame")
    
    if out_single_DataFrame and keep_data_in_sections:
        raise ValueError(f"Arguments '{param_keys[kdis_arg_pos]}' and "
                         f"'{param_keys[osd_arg_pos]}' cannot be True at the same time. "
                         "Set one of them True and False the other one.")
    
    # Correct number of input files #
    if isinstance(input_file_list, str):
        input_file_list = [input_file_list]
    elif isinstance(input_file_list, list):
        input_file_list = flatten_list(input_file_list)
        
    input_file_count = len(input_file_list)
    
    if input_file_count == 1:
        raise ValueError(BELOW_MINIMUM_FILE_WARNING)
        
    # Option 1: merge data of all files into a single DataFrame #
    #-----------------------------------------------------------#
    
    if out_single_DataFrame and not keep_data_in_sections:
        
        # Check firstly if all data frames have the same number of columns 
        #-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-
        
        ind_file_df_nrow_list = []    
        for file in input_file_list:
            file_df = csv2df(file,
                             separator=separator_in,
                             engine=engine,
                             encoding=encoding,
                             header=header,
                             parse_dates=parse_dates,
                             index_col=index_col,
                             decimal=decimal)
            
            ind_file_df_nrow_list.append(file_df.shape[0])
            
        ind_file_df_nrow_unique = unique(ind_file_df_nrow_list)
        unique_row_count = len(ind_file_df_nrow_unique)
        
        # If not the case, warn respectively and prompt to merge anyway #
        if unique_row_count > 1:
            merge_anyway_stdin = input("Warning: number of rows of data in some files "
                                       "is not common to all data. "
                                       "Mergeing resulted in concatenation by "
                                       "filling the missing values with NaNs. "
                                       "Proceed anyway? (y/n) ")
            
            
            while (merge_anyway_stdin != "y" and merge_anyway_stdin != "n"):
                merge_anyway_stdin = input("\nPlease select 'y' for 'yes' "
                                           "or 'n' for 'no': ")
                
            else:  
                # Merge now all DataFrames into a single one #
                if merge_anyway_stdin == "y":
                    all_file_data_df = _concat_dfs_aux(input_file_list,
                                                       separator_in,
                                                       engine,
                                                       encoding,
                                                       header,
                                                       parse_dates,
                                                       index_col,
                                                       decimal)
                else:
                    pass
                
                
             
        # Otherwise merge all DataFrames into a single one directly #
        #-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
        
        else:
            all_file_data_df = _concat_dfs_aux(input_file_list,
                                               separator_in,
                                               engine,
                                               encoding,
                                               header,
                                               parse_dates,
                                               index_col,
                                               decimal)
            
        # Prompt to save the merged object #
        #-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-
        
        if save_merged_file:
           saving_result = save2csv(output_file_path, 
                                    all_file_data_df, 
                                    separator=separator_out,
                                    decimal=decimal,
                                    save_index=save_index, 
                                    save_header=save_header)
           return saving_result
            
        else:
            return all_file_data_df
        
        
    # Option 2: save each DataFrame with the corresponding file into a dictionary #
    #-----------------------------------------------------------------------------#
        
    elif not out_single_DataFrame and keep_data_in_sections:
        all_file_data_dict = \
            {get_obj_specs(file,"name_noext") : csv2df(file,
                                                       separator=separator_in,
                                                       engine=engine,
                                                       encoding=encoding,
                                                       header=header,
                                                       parse_dates=parse_dates,
                                                       index_col=index_col,
                                                       decimal=decimal)
             for file in input_file_list}
        
        # Prompt to save the merged object #
        #-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-
        
        # Because there is no 'sheet' concept, in case of saving the dictionary
        # it must be done so in an Excel file, not a CSV file
        
        if save_merged_file:
            saving_result = save2excel(output_file_path,
                                       all_file_data_dict, 
                                       save_index=save_index, 
                                       save_header=save_header)
            return saving_result
         
        else:
            return all_file_data_dict
        
        
    
def _concat_dfs_aux(input_file_list,
                    separator_in,
                    engine,
                    encoding, 
                    header, 
                    parse_dates, 
                    index_col, 
                    decimal):
    
    all_file_data_df = pd.DataFrame()
    for file in input_file_list:
        file_df = csv2df(file,
                         separator=separator_in,
                         engine=engine,
                         encoding=encoding,
                         header=header,
                         parse_dates=parse_dates,
                         index_col=index_col,
                         decimal=decimal)
        
        all_file_data_df = pd.concat([all_file_data_df, file_df], axis=1)
    return all_file_data_df
    

# ODS files #
#-#-#-#-#-#-#

def ods_handler(file_path, 
                sheet_name=None,
                header=None,
                decimal='.', 
                return_type='dict'):
    
    """
    Reads a LibreOffice Calc file and processes its sheets either into a 
    dictionary of DataFrames or a single merged DataFrame.
    
    In either case, it calls the 'excel_handler' function, because the only
    difference is the engine called, 'odf', from 'odfpy' library.
    Then this function inherits every functionalities from the mentioned one.

    Parameters
    ----------
    file_path : str
        Path to the Excel file.
    sheet_name : str, int, list, or None, default 0
        Strings are used for sheet names. Integers are used in zero-indexed
        sheet positions (chart sheets do not count as a sheet position).
        Lists of strings/integers are used to request multiple sheets.
        Specify ``None`` to get all worksheets.
    header : int | list[int] | None, default None
        Row (0-indexed) to use for the column labels of the parsed DataFrame.
    decimal : str, default '.'
        Character to recognise as decimal point (e.g., ',' in Europe).
    return_type : str, default 'dict'
        Type of output to return. Must be either 'dict' to return a dictionary
        of DataFrames, or 'df' to return a single merged DataFrame.

    Returns
    -------
    dict or pd.DataFrame
        If 'return_type' is 'dict', returns a dictionary where keys are
        sheet names and values are DataFrames.
        If 'return_type' is 'df', returns a single DataFrame
        with data from all sheets merged.

    Raises
    ------
    TypeError
        If 'return_type' is not 'dict' or 'df'.
    """
    
    # Common keyword argument dictionary #
    kwargs = dict(
        sheet_name=sheet_name,
        header=header, 
        engine="odf", 
        decimal=decimal
        )
    
    # Case studies #
    if return_type == 'dict':
        item_dict = excel_handler(file_path,
                                  **kwargs, 
                                  return_type='dict')        
        return item_dict
    
    elif return_type == 'df':
        all_data_df = excel_handler(file_path,
                                    **kwargs,
                                    return_type='df')
        return all_data_df   
    
    

def save2ods(file_path,
             frame_obj,
             indiv_sheet_name="Sheet1",
             save_index=False,
             save_header=False,
             engine="odf"):
    
    saving_result = save2excel(file_path,
                               frame_obj,
                               indiv_sheet_name=indiv_sheet_name,
                               save_index=save_index,
                               save_header=save_header,
                               engine=engine)    
    return saving_result
    

def merge_ods_files(input_file_list,
                    output_file_path,
                    save_index=False,
                    save_header=False,
                    save_merged_file=False):
    
    saving_result = merge_excel_files(input_file_list,
                                      output_file_path,
                                      save_index=save_index,
                                      save_header=save_header,
                                      save_merged_file=save_merged_file)
    return saving_result


#--------------------------#
# Parameters and constants #
#--------------------------#

# File extension list #
EXTENSIONS = ["csv", "xlsx"]

# Template strings #
#----------------------#

ALREADY_EXISTING_FILE_WARNING_TEMPLATE = """Warning: file '{}' at directory '{}' \
already exists.\nDo you want to overwrite it? (y/n) """

# Warning strings #
#-----------------#

OVERWRITE_PROMPT_WARNING = "\nPlease select 'y' for 'yes' or 'n' for 'no': "
BELOW_MINIMUM_FILE_WARNING = """At least 2 files must be given \
in order to perform the merge."""

# Error strings #
#---------------#

UNSUPPORTED_OBJ_TYPE_ERR_TEMPLATE = "Expected a pandas.DataFrame object, got {}"

# Argument choice options #
#-------------------------#

EXCEL_HANDLING_RETURN_OPTIONS = ["dict", "df"]
