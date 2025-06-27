#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------#
# Import modules #
#----------------#

import fnmatch
import os
import re
from functools import lru_cache

#------------------------#
# Import project modules #
#------------------------#

from pygenutils.arrays_and_lists.data_manipulation import flatten_list

#------------------#
# Define functions #
#------------------#

# Helpers #
#---------#

def _unique_sorted(items: list) -> list:
    """
    Returns a sorted list of unique items.
    
    Parameters
    ----------
    items : list
        List of items to deduplicate and sort.
        
    Returns
    -------
    list
        Sorted list of unique items.
    """
    return sorted(set(items))

@lru_cache(maxsize=128)
def _compile_pattern(pattern: str) -> re.Pattern:
    """
    Compiles a glob pattern into a regex pattern for faster matching.
    
    Parameters
    ----------
    pattern : str
        The glob pattern to compile.
        
    Returns
    -------
    re.Pattern
        Compiled regex pattern.
    """
    return re.compile(fnmatch.translate(pattern))

def _match_glob(file: str, patterns: list, case_sensitive: bool = True) -> bool:
    """
    Matches a file against a list of glob patterns.
    
    Parameters
    ----------
    file : str
        The file path to match.
    patterns : list
        List of glob patterns to match against.
    case_sensitive : bool, optional
        Whether to perform case-sensitive matching. Defaults to True.
        
    Returns
    -------
    bool
        True if the file matches any pattern, False otherwise.
    """
    if not os.path.isfile(file):
        return False
        
    basename = os.path.basename(file)
    if not case_sensitive:
        basename = basename.lower()
        patterns = [p.lower() for p in patterns]
    
    return any(_compile_pattern(pattern).match(basename) for pattern in patterns)

def _fetch_path_items(path: str, glob_bool: bool = True) -> list[str]:
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
    list[str]
        A list of all files and directories found in the specified path.
    """
    if glob_bool:
        items = []
        for dirpath, dirnames, filenames in os.walk(path):
            items.extend([os.path.join(dirpath, dirname) for dirname in dirnames])
            items.extend([os.path.join(dirpath, file) for file in filenames])
        return items
    else:
        return [os.path.join(path, item) for item in os.listdir(path)]
    
    
# Switch-case dictionary to modify patterns based on 'match_type' argument 
def _add_glob_left(patterns: list) -> list:
    """Add wildcard at the beginning of patterns (to match end of filename)"""
    return [f"*{pattern}" for pattern in patterns]

def _add_glob_right(patterns: list) -> list:
    """Add wildcard at the end of patterns (to match beginning of filename)"""
    return [f"{pattern}*" for pattern in patterns]

def _add_glob_both(patterns: list) -> list:
    """Add wildcards at both ends of patterns (to match anywhere in filename)"""
    return [f"*{pattern}*" for pattern in patterns]

def _whole_word(patterns: list) -> list:
    """No modification for whole word match"""
    return patterns


# Main functions #
#----------------#

# File Operations #
#~~~~~~~~~~~~~~~~~#

def find_files(patterns: str | list, 
               search_path: str, 
               match_type: str = "ext", 
               top_only: bool = False, 
               dirs_to_exclude: str | list | None = None, 
               case_sensitive: bool = True) -> list[str]:
    """
    Searches for files based on extensions or glob patterns with various matching types.

    Parameters
    ----------
    patterns : str | list
        File extensions or glob patterns to search for.
    search_path : str
        The directory path to search within.
    match_type : str, optional
        The type of matching to apply. Options include:
        - "ext": match based on file extensions.
        - "glob_left": match with a wildcard at the beginning of the pattern.
        - "glob_right": match with a wildcard at the end of the pattern.
        - "glob_both": match with wildcards at both the beginning and the end of the pattern.
        - "ww": match the exact whole word (no wildcards).
        Defaults to "ext".
    top_only : bool, optional
        If True, only searches in the top directory without subdirectories. 
        Defaults to False.
    dirs_to_exclude : str | list | None, optional
        Directory or list of directories to exclude from the search.
        Defaults to None.
    case_sensitive : bool, optional
        Whether to perform case-sensitive matching. Defaults to True.
    
    Returns
    -------
    list[str]
        A list of files matching the specified patterns.

    Raises
    ------
    ValueError
        If an invalid `match_type` is provided.
    """
    # Handle nested lists with defensive programming
    if isinstance(patterns, str):
        patterns = [patterns]
    elif isinstance(patterns, list):
        patterns = flatten_list(patterns)
    
    if dirs_to_exclude is None:
        dirs_to_exclude = []
    elif isinstance(dirs_to_exclude, str):
        dirs_to_exclude = [dirs_to_exclude]
    elif isinstance(dirs_to_exclude, list):
        dirs_to_exclude = flatten_list(dirs_to_exclude)

    modify_pattern_func = MATCH_PATTERN_MODIFIER.get(match_type)
    if not modify_pattern_func:
        raise ValueError(f"Invalid match_type '{match_type}'. Choose one from {MTD_KEYS}")
    
    patterns = modify_pattern_func(patterns)

    if top_only:
        files = _fetch_path_items(search_path, glob_bool=False)
    else:
        files = _fetch_path_items(search_path)

    if dirs_to_exclude:
        files = [file for file in files if not any(excluded in file for excluded in dirs_to_exclude)]

    match_func = MATCH_TYPE_DICT.get(match_type)
    if not match_func:
        raise ValueError(f"Invalid match_type '{match_type}'. Choose one from {MTD_KEYS}")

    return _unique_sorted([file for file in files if match_func(file, patterns, case_sensitive)])


# Directory Operations #
#~~~~~~~~~~~~~~~~~~~~~~#

def find_dirs_with_files(patterns: str | list, 
                         search_path: str, 
                         match_type: str = "ext", 
                         top_only: bool = False, 
                         dirs_to_exclude: str | list | None = None, 
                         case_sensitive: bool = True) -> list[str]:
    """
    Finds directories containing files that match the given patterns with various matching types.

    Parameters
    ----------
    patterns : str | list
        File extensions or glob patterns to search for.
    search_path : str
        The directory path to search within.
    match_type : str, optional
        The type of matching to apply. Options include:
        - "ext": match based on file extensions.
        - "glob_left": match with a wildcard at the beginning of the pattern.
        - "glob_right": match with a wildcard at the end of the pattern.
        - "glob_both": match with wildcards at both the beginning and the end of the pattern.
        - "ww": match the exact whole word (no wildcards).
        Defaults to "ext".
    top_only : bool, optional
        If True, only searches in the top directory without subdirectories.
        Defaults to False.
    dirs_to_exclude : str | list | None, optional
        Directory or list of directories to exclude from the search.
        Defaults to None.
    case_sensitive : bool, optional
        Whether to perform case-sensitive matching. Defaults to True.
    
    Returns
    -------
    list[str]
        A list of directories containing files matching the specified patterns.

    Raises
    ------
    ValueError
        If an invalid `match_type` is provided.
    """
    # Handle nested lists with defensive programming
    if isinstance(patterns, str):
        patterns = [patterns]
    elif isinstance(patterns, list):
        patterns = flatten_list(patterns)
    
    if dirs_to_exclude is None:
        dirs_to_exclude = []
    elif isinstance(dirs_to_exclude, str):
        dirs_to_exclude = [dirs_to_exclude]
    elif isinstance(dirs_to_exclude, list):
        dirs_to_exclude = flatten_list(dirs_to_exclude)

    modify_pattern_func = MATCH_PATTERN_MODIFIER.get(match_type)
    if not modify_pattern_func:
        raise ValueError(f"Invalid match_type '{match_type}'. Choose one from {MTD_KEYS}")
    
    patterns = modify_pattern_func(patterns)

    if top_only:
        files = _fetch_path_items(search_path, glob_bool=False)
    else:
        files = _fetch_path_items(search_path)

    if dirs_to_exclude:
        files = [file for file in files if not any(excluded in file for excluded in dirs_to_exclude)]

    match_func = MATCH_TYPE_DICT.get(match_type)
    if not match_func:
        raise ValueError(f"Invalid match_type '{match_type}'. Choose one from {MTD_KEYS}")

    dirs = [os.path.dirname(file) for file in files if match_func(file, patterns, case_sensitive)]
    return _unique_sorted(dirs)


# Extensions and Directories Search #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

def find_items(search_path: str, 
               skip_ext: str | list | None = None, 
               top_only: bool = False, 
               task: str = "extensions", 
               dirs_to_exclude: str | list | None = None) -> list[str]:
    """
    Finds all unique file extensions or directories in the specified path.

    Parameters
    ----------
    search_path : str
        The directory path to search within.
    skip_ext : str | list | None, optional
        Extensions to skip while searching. Defaults to None.
    top_only : bool, optional
        If True, only searches in the top directory without subdirectories.
        Defaults to False.
    task : str, default "extensions"
        - "extensions": to find file extensions
        - "directories" to find directories
    dirs_to_exclude : str | list | None, optional
        Directory or list of directories to exclude from the search.
        Defaults to None.
    
    Returns
    -------
    list[str]
        A list of unique file extensions or directories.
    """
    # Handle nested lists with defensive programming
    if skip_ext is None:
        skip_ext = []
    elif isinstance(skip_ext, str):
        skip_ext = [skip_ext]
    elif isinstance(skip_ext, list):
        skip_ext = flatten_list(skip_ext)
    
    if dirs_to_exclude is None:
        dirs_to_exclude = []
    elif isinstance(dirs_to_exclude, str):
        dirs_to_exclude = [dirs_to_exclude]
    elif isinstance(dirs_to_exclude, list):
        dirs_to_exclude = flatten_list(dirs_to_exclude)

    if top_only:
        items = _fetch_path_items(search_path, glob_bool=False)
    else:
        items = _fetch_path_items(search_path)

    if dirs_to_exclude:
        items = [item for item in items if not any(excluded in item for excluded in dirs_to_exclude)]

    if task == "extensions":
        extensions = [os.path.splitext(file)[1] for file in items 
                      if os.path.isfile(file) and os.path.splitext(file)[1] not in skip_ext]
        return _unique_sorted(extensions)
    elif task == "directories":
        dirs = [item for item in items if os.path.isdir(item)]
        return _unique_sorted(dirs)
    else:
        raise ValueError("Invalid task. Use 'extensions' or 'directories'.")
        
#--------------------------#
# Parameters and constants #
#--------------------------#

# Switch-case dictionaries #
#--------------------------#

# Define a switch-case dictionary to handle 'match_type' options
MATCH_TYPE_DICT = {
    # For extension matching, we check if the file ends with the extension
    "ext": lambda file, patterns, case_sensitive=True: (
        os.path.isfile(file) and 
        any(os.path.splitext(file)[1].lower() == f".{ext.lower()}" for ext in patterns)
    ),
    
    # For glob patterns, we use our optimised matching function
    "glob_left": _match_glob,
    "glob_right": _match_glob,
    "glob_both": _match_glob,
    
    # For whole word matching, we check if the pattern exactly matches the basename
    "ww": lambda file, patterns, case_sensitive=True: (
        os.path.isfile(file) and 
        any(pattern == os.path.basename(file) for pattern in patterns)
    )
}

MTD_KEYS = list(MATCH_TYPE_DICT.keys())

MATCH_PATTERN_MODIFIER = {
    "ext": lambda patterns: patterns,
    "glob_left": _add_glob_left,
    "glob_right": _add_glob_right,
    "glob_both": _add_glob_both,
    "ww": _whole_word
}