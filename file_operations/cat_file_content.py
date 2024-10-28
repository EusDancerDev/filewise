#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------#
# Import modules #
#----------------#

import os

#-------------------------#
# Define custom functions #
#-------------------------#

def cat(path, mode="r"):
    
    """
    Prints the content of a file specified in an absolute or relative path
    the same way as it does the 'cat' UNIX command.
    
    Parameters
    ----------
    path : str or PosixPath
        Absolute or relative path.
    mode : str, optional
        Specify the IO mode for output when supplying a path.
        Default value is 'r' (read-only).
          
    Returns
    -------
    The path is always case-sensitive.
    If the path exists, it returns the string of the whole content
    of the specified path, else throws a FileNotFoundError.
    """
    
    path_exists = os.path.exists(path)
    
    if path_exists:
        with open(path, mode=mode) as file_obj:
            for line in file_obj:
                line_stripped = line.strip()
                print(line_stripped)
        
    else:
        raise FileNotFoundError("No such file or directory. "
                                "Try fixing misspellings or check path's components.")        
        
#-------------------#
# Call the function #
#-------------------#
        
path = input('Enter the relative or absolute path to the file to be read: ')
cat(path)