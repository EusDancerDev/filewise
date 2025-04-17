#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------#
# Import modules #
#----------------#

import pandas as pd

#-----------------------#
# Import custom modules #
#-----------------------#

from filewise.pandas_utils.pandas_obj_handler import csv2df

#------------------#
# Define functions #
#------------------#

# Data frame value handling #
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

def sort_df_values(df,
                   by,
                   ignore_index_bool=False,
                   axis=0,
                   ascending_bool=True,
                   na_position="last",
                   key=None):
    
    """
    Sort by the values along either axis
    
    Parameters
    ----------
    df : pandas.DataFrame or pandas.Series.
    by : str or list of str
        Name or list of names to sort by.
    ignore_index : bool
        Boolean to determine whether to relabel indices
        at ascending order: 0, 1, ..., n-1 or remain them unchanged.
        Defaults False.
    axis : {0, 'index', 1, 'columns'}
        Axis to be sorted; default value is 0.
    ascending : bool or list of bool
        Sort ascending vs. descending. Specify list for multiple sort
        orders. Default is True boolean.
    na_position : {'first', 'last'}
        Puts NaNs at the beginning if 'first'; 'last' puts NaNs at the end.
        Defaults to "last".
    key : callable, optional
        Apply the key function to the values
        before sorting. This is similar to the 'key' argument in the
        builtin :meth:'sorted' function, with the notable difference that
        this 'key' function should be *vectorised*.
    """
    
    df = df.sort_values(by=by,
                        axis=axis, 
                        ascending=ascending_bool,
                        na_position=na_position,
                        ignore_index=ignore_index_bool,
                        key=key)

    return df

    
def insert_column_in_df(df, index_col, column_name, values):
    
    """
    Function that inserts a column on a simple, non multi-index
    Pandas DataFrame, specified by an index column.
    Note that this function acts in-place.
    
    Parameters
    ----------
    df : pandas.DataFrame
        Data frame containing data.
    index_col : int
        Denotes the column position to insert new data.
        It is considered that data is desired to introduced
        at the LEFT of that index, so that once inserted data on that position, 
        the rest of the data will be displaced rightwards.
    column_name : str
        Name of the column to be inserted.
    values : list, numpy.array or pandas.Series
    """
    
    ncols = len(df.iloc[0])
    
    if index_col < 0:
        index_col += ncols + 1

    df.insert(index_col, column_name, values)
    
    
def insert_row_in_df(df, row_data, index=None):
    """
    Insert a row into a pandas DataFrame at a specified index.
    
    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame to insert the row into
    row_data : dict or list
        The data for the new row. If dict, keys should match DataFrame columns.
        If list, values should be in the same order as DataFrame columns.
    index : int, optional
        The index at which to insert the row. If None, appends to the end.
        
    Returns
    -------
    pandas.DataFrame
        The DataFrame with the new row inserted
    """
    
    if isinstance(row_data, dict):
        new_row = pd.DataFrame([row_data])
    elif isinstance(row_data, list):
        new_row = pd.DataFrame([row_data], columns=df.columns)
    else:
        raise ValueError("row_data must be a dict or list")
        
    if index is None:
        return pd.concat([df, new_row], ignore_index=True)
    else:
        return pd.concat([df.iloc[:index], new_row, df.iloc[index:]], ignore_index=True)

    
# Data frame index handling #
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

def sort_df_indices(df,
                    axis=0,
                    ignore_index_bool=False,
                    level=None,
                    ascending_bool=True,
                    na_position="last",
                    sort_remaining_bool=True,
                    key=None):
    
    """
    Returns a new data frame sorted 
    
    Parameters
    ----------
    df : pandas.DataFrame or pandas.Series.
    level : int or level name or list of ints or list of level names
        If not None, sort on values in specified index level(s)
    axis : {0, 'index', 1, 'columns'}
        Axis to be sorted; default value is 0.
    ignore_index : bool
        Boolean to determine whether to relabel indices
        at ascending order: 0, 1, ..., n-1 or remain them unchanged.
        Defaults False.
    ascending : bool or list of bool
        Sort ascending vs. descending. Specify list for multiple sort
        orders. Default is True boolean.
    na_position : {'first', 'last'}.
        Puts NaNs at the beginning if 'first'; 'last' puts NaNs at the end.
        Defaults to "last".
    sort_remaining : bool
        If True and sorting by level and index is multilevel, sort by other
        levels too (in order) after sorting by specified level.
        Default value is True.
    key : callable, optional
        Apply the key function to the values
        before sorting. This is similar to the 'key' argument in the
        builtin :meth:'sorted' function, with the notable difference that
        this 'key' function should be *vectorised*.
    """
            
    df.sort_index(axis=axis, 
                  level=level,
                  ascending=ascending_bool,
                  na_position=na_position,
                  sort_remaining=sort_remaining_bool,
                  ignore_index=ignore_index_bool,
                  key=key)
    
    return df


def reindex_df(df, col_to_replace=None, vals_to_replace=None):
    
    """
    Further function than df.reset_index attribute,
    for resetting the index of the given Pandas DataFrame,
    using any specified column and then resetting the latter.
    This function applies only for one-leveled objects
    (i.e, cannot have a MultiIndex) and can contain any tipe of index.
    It can also be applied for simple reindexing.
    
    Parameters
    ----------
    df : pandas.DataFrame or pandas.Series.
    vals_to_replace : list, np.ndarray or pandas.Series
        New labels / index to conform to.
    col_to_replace : str or int
        If further reindexing is required,
        an it is a string, then it selects the columns to put as index.
        Otherwise it selects the number column.
        Defaults to None, that is, to simple reindexing.
    """
    
    if col_to_replace is None and vals_to_replace is None:
        raise ValueError("You must provide an object containing values to"
                         "put as index.")
        
    elif col_to_replace is None and vals_to_replace is not None:
        df = df.reindex(vals_to_replace)
        
    else:
        
        if isinstance(col_to_replace, str):

            # Substitute the index as desired #  
            df_reidx_drop_col\
            = df.reindex(df[col_to_replace]).drop(columns=col_to_replace)
            
            # Assign the remaining values to the new data frame #
            df_reidx_drop_col.loc[:,:]\
            = df.drop(columns=col_to_replace).values
            
        elif isinstance(col_to_replace, int):
            
            columns = df.columns
            colname_to_drop = columns[col_to_replace]
            
            # Substitute the index as desired #              
            df_reidx_drop_col\
            = df.reindex(df.iloc[:, col_to_replace]).drop(columns=colname_to_drop)
        
            # Assign the remaining values to the new data frame #
            df_reidx_drop_col.loc[:,:]\
            = df.drop(columns=colname_to_drop).values
        
    return df_reidx_drop_col


def count_data_by_concept(df, df_cols):
    data_count = df.groupby(df_cols).count()
    return data_count    



def concat_dfs_aux(input_file_list,
                   separator_in,
                   engine,
                   encoding, 
                   header, 
                   parse_dates, 
                   index_col, 
                   decimal):
    
    all_file_data_df = pd.DataFrame()
    for file in input_file_list:
        file_df = csv2df(separator=separator_in,
                         engine=engine,
                         encoding=encoding,
                         header=header,
                         parse_dates=parse_dates,
                         index_col=index_col,
                         decimal=decimal)
        
        all_file_data_df = pd.concat([all_file_data_df, file_df], axis=1)
    return all_file_data_df


def create_pivot_table(df, df_values, df_index, func_apply_on_values):    
    """
    Create a pivot table from the given DataFrame.

    Parameters
    ----------
    df : pandas.DataFrame
        The input DataFrame from which to create the pivot table.
    df_values : str or list
        Column(s) in the DataFrame to aggregate.
    df_index : str or list
        Column(s) to set as index for the pivot table.
    func_apply_on_values : str or callable
        The aggregation function to apply on the values.

    Returns
    -------
    pandas.DataFrame
        A pivot table as a DataFrame.

    Raises
    ------
    ValueError
        If df is empty or if df_values or df_index are not found in the DataFrame.
    
    Notes
    -----
    Common aggregation functions include 'mean', 'sum', 'count', etc.
    """
    
    if df.empty:
        raise ValueError("Input DataFrame is empty.")
    
    if df_values not in df.columns:
        raise ValueError(f"Column '{df_values}' not found in DataFrame.")
    
    if df_index not in df.columns:
        raise ValueError(f"Column '{df_index}' not found in DataFrame.")
    
    pivot_table = pd.pivot_table(df, 
                                 values=df_values, 
                                 index=df_index,
                                 aggfunc=func_apply_on_values)
    return pivot_table

    
