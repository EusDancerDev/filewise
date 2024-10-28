#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------#
# Import modules #
#----------------#

from numpy import array

#-----------------------#
# Import custom modules #
#-----------------------#

from pyutils.string_handler import string_handler

# Create aliases #
#----------------#

find_substring_index = string_handler.find_substring_index
get_obj_specs = string_handler.get_obj_specs
modify_obj_specs = string_handler.modify_obj_specs

#------------------#
# Define functions #
#------------------#

# Pandas objects #
#----------------#

# Structured array conversion #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

def df_to_structured_array(df):
    """
    Converts a pandas DataFrame into a structured NumPy array, 
    where each row is represented as a tuple, and each column 
    has its own data type.

    This type of array categorizes each column of the DataFrame 
    by its data type and converts the rows into tuples.

    Parameters
    ----------
    df : pandas.DataFrame
        A pandas DataFrame with the data to convert into a structured array.
        
    Returns
    -------
    numpy.ndarray
        A structured NumPy array where each row is a tuple and each column 
        has its corresponding data type. 

    Notes
    -----
    - The structured array allows more efficient storage and retrieval 
      by enforcing data types at the column level.
    - Structured arrays are useful when working with heterogeneous data 
      types in a NumPy array format.

    Examples
    --------
    >>> dtype = [('name', 'S10'), ('height', float), ('age', int)]
    >>> values = [('Arthur', 1.8, 41), ('Lancelot', 1.9, 38),
                  ('Galahad', 1.7, 38)]
    >>> a = np.array(values, dtype=dtype)
    array([(b'Arthur', 1.8, 41), (b'Lancelot', 1.9, 38),
           (b'Galahad', 1.7, 38)],
          dtype=[('name', 'S10'), ('height', '<f8'), ('age', '<i8')])

    The structured array displays each row as a tuple with the column data types:
    - 'name': string (max 10 characters)
    - 'height': float (less than 8 bits)
    - 'age': integer (less than 8 bits)
    
    You can easily convert it back to a pandas DataFrame for readability:
    
          name    height  age
    0  b'Arthur'   1.8     41
    1  b'Lancelot' 1.9     38
    2  b'Galahad'  1.7     38
    """
    
    # Convert DataFrame to a NumPy record array (row tuples)
    records = df.to_records(index=False)
    
    # Convert the record array to a structured NumPy array with column-specific types
    structured_array = array(records, dtype=records.dtype.descr)
    
    return structured_array
