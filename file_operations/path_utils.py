#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------#
# Import modules #
#----------------#

import os
import numpy as np

#-----------------------#
# Import custom modules #
#-----------------------#

from pyutils.strings.string_handler import get_obj_specs

#------------------#
# Define functions #
#------------------#

# Helpers #
#---------#

def path_converter(path, glob_bool=True):
    """
    Converts a path into an os-based path and handles globbing.

    Parameters
    ----------
    path : str
        The directory path to search within.
    glob_bool : bool, optional
        If True, finds all files and directories recursively. Defaults to True.
        
    Returns
    -------
    list
        A list of all files and directories found in the specified path.
    """
    if glob_bool:
        return [os.path.join(dirpath, file)
                for dirpath, _, files in os.walk(path)
                for file in files]
    else:
        return [os.path.join(path, item) for item in os.listdir(path)]

# Main functions #
#----------------#

# File Operations #
#~~~~~~~~~~~~~~~~~#

def find_files(patterns, search_path, match_type="ext", top_only=False):
    """
    Searches for files based on extensions or glob patterns.

    Parameters
    ----------
    patterns : str or list
        File extensions or glob patterns to search for.
    search_path : str
        The directory path to search within.
    match_type : str, optional
        Either "ext" for extensions or "glob" for glob patterns.
        Defaults to "ext".
    top_only : bool, optional
        If True, only searches in the top directory without subdirectories. 
        Defaults to False.
    
    Returns
    -------
    list of str
        A list of files matching the specified patterns.
    """
    if isinstance(patterns, str):
        patterns = [patterns]

    if top_only:
        files = path_converter(search_path, glob_bool=False)
    else:
        files = path_converter(search_path)

    match_func = match_type_dict.get(match_type)
    if not match_func:
        raise ValueError(f"Invalid match_type: {match_type}")

    return list(np.unique([file for file in files if match_func(file, patterns)]))


# Directory Operations #
#~~~~~~~~~~~~~~~~~~~~~~#

def find_dirs(search_path, top_only=False, include_root=True):
    """
    Finds all directories in the specified source directory.

    Parameters
    ----------
    search_path : str
        The directory path to search for directories.
    top_only : bool, optional
        If True, only searches the top directory without subdirectories.
        Defaults to False.
    include_root : bool, optional
        If False, only directory names are returned without full paths.
        Defaults to True.
    
    Returns
    -------
    list of str
        A list of directories found in the specified search path.
    """
    dirs = []
    if top_only:
        items = os.listdir(search_path)
        dirs = [os.path.join(search_path, item)
                if include_root else item 
                for item in items
                if os.path.isdir(os.path.join(search_path, item))]
    else:
        for dirpath, dirnames, _ in os.walk(search_path):
            dirs.extend([os.path.join(dirpath, dirname)
                         if include_root else dirname for dirname in dirnames])

    return list(np.unique(dirs))


def find_dirs_with_files(patterns, search_path, match_type="ext", top_only=False):
    """
    Finds directories containing files that match the given patterns.

    Parameters
    ----------
    patterns : str or list
        File extensions or glob patterns to search for.
    search_path : str
        The directory path to search within.
    match_type : str, optional
        Either "ext" for extensions or "glob" for glob patterns. Defaults to "ext".
    top_only : bool, optional
        If True, only searches in the top directory without subdirectories.
        Defaults to False.
    
    Returns
    -------
    list of str
        A list of directories containing files matching the specified patterns.
    """
    if isinstance(patterns, str):
        patterns = [patterns]

    if top_only:
        files = path_converter(search_path, glob_bool=False)
    else:
        files = path_converter(search_path)

    match_func = match_type_dict.get(match_type)
    if not match_func:
        raise ValueError(f"Invalid match_type: {match_type}")

    dirs = [os.path.dirname(file) for file in files if match_func(file, patterns)]
    return list(np.unique(dirs))


# Extensions and Directories Search #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

def find_items(search_path, skip_ext=None, top_only=False, task="extensions"):
    """
    Finds all unique file extensions or directories in the specified path.

    Parameters
    ----------
    search_path : str
        The directory path to search within.
    skip_ext : str or list, optional
        Extensions to skip while searching. Defaults to None.
    top_only : bool, optional
        If True, only searches in the top directory without subdirectories.
        Defaults to False.
    task : {"extensions", "directories"}, default "extensions"
        - "extensions": to find file extensions
        - "directories" to find directories
    
    Returns
    -------
    list of str
        A list of unique file extensions or directories.
    """
    if skip_ext is None:
        skip_ext = []
    if isinstance(skip_ext, str):
        skip_ext = [skip_ext]

    if top_only:
        items = path_converter(search_path, glob_bool=False)
    else:
        items = path_converter(search_path)

    if task == "extensions":
        extensions = [get_obj_specs(file, "ext") for file in items 
                      if os.path.isfile(file) and get_obj_specs(file, "ext") not in skip_ext]
        return list(np.unique(extensions))
    elif task == "directories":
        dirs = [item for item in items if os.path.isdir(item)]
        return list(np.unique(dirs))
    else:
        raise ValueError("Invalid task. Use 'extensions' or 'directories'.")


def find_by_pattern(patterns, search_path, match_type="ext", top_only=False, search_type="files"):
    """
    Finds files or directories based on extensions or glob patterns.

    Parameters
    ----------
    patterns : str or list
        File extensions or glob patterns to search for.
    search_path : str
        The directory path to search within.
    match_type : str, optional
        Either "ext" for extensions or "glob" for glob patterns. Defaults to "ext".
    top_only : bool, optional
        If True, only searches in the top directory without subdirectories. 
        Defaults to False.
    search_type : str, optional
        "files" to search for files or "directories" to search for directories. 
        Defaults to "files".
    
    Returns
    -------
    list of str
        A list of files or directories matching the specified patterns.
    """
    if isinstance(patterns, str):
        patterns = [patterns]

    if top_only:
        items = path_converter(search_path, glob_bool=False)
    else:
        items = path_converter(search_path)

    match_func = match_type_dict.get(match_type)
    if not match_func:
        raise ValueError(f"Invalid match_type: {match_type}")

    if search_type == "files":
        return list(np.unique([file for file in items 
                               if os.path.isfile(file) and match_func(file, patterns)]))
    elif search_type == "directories":
        dirs = [os.path.dirname(file) for file in items 
                if os.path.isfile(file) and match_func(file, patterns)]
        return list(np.unique(dirs))
    else:
        raise ValueError("Invalid search_type. Use 'files' or 'directories'.")


#--------------------------#
# Parameters and constants #
#--------------------------#

# Switch-case dictionaries #
#--------------------------#

# Define a switch-case dictionary to handle 'match_type' options
match_type_dict = {
    "ext": lambda file, patterns: any(file.endswith(f".{ext}") for ext in patterns),
    "glob": lambda file, patterns: any(pattern in file for pattern in patterns)
}