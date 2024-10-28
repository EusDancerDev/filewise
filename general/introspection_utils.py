#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------#
# Import modules # 
#----------------#

from collections.abc import Iterable
import inspect
import sys

#------------------#
# Define functions #
#------------------#

# Methods #
#---------#

# Function names #
def get_func_name(lib="inspect"):
    """
    Retrieves the name of the caller function using the specified library.

    Parameters
    ----------
    lib : str, optional
        Library to use for function name retrieval. Must be one of 'inspect' or 'sys'.
        Defaults to 'inspect'.

    Returns
    -------
    str
        Name of the caller function.

    Raises
    ------
    ValueError
        If `lib` is not a supported library.
    """
    if lib not in func_name_libs:
        raise ValueError("Unsupported library. Choose from {func_name_libs}.")
    if lib == "inspect":
        return inspect.getframeinfo(inspect.currentframe().f_back).function
    return sys._getframe(1).f_code.co_name
    

# Function arguments #
#--------------------#

# General frame #
#-#-#-#-#-#-#-#-#

def get_func_args(func):
    """
    Retrieves the required argument names of the provided function.

    Parameters
    ----------
    func : callable
        Function whose required argument names are retrieved.

    Returns
    -------
    list of str
        List of required argument names.

    Example
    -------
    >>> def example_func(arg1, arg2, kwarg1=None): pass
    >>> get_func_args(example_func)
    ['arg1', 'arg2']
    """
    sig = inspect.signature(func)
    return [p.name for p in sig.parameters.values() if p.default == inspect.Parameter.empty
            and p.kind in (inspect.Parameter.POSITIONAL_OR_KEYWORD, 
                           inspect.Parameter.KEYWORD_ONLY)]


def get_all_func_args(func):
    """
    Retrieves all argument names of the provided function.

    Parameters
    ----------
    func : callable
        Function whose argument names are retrieved.

    Returns
    -------
    list of str
        List of all argument names, including those with default values.

    Example
    -------
    >>> def example_func(arg1, arg2, kwarg1=None): pass
    >>> get_all_func_args(example_func)
    ['arg1', 'arg2', 'kwarg1']
    """
    return [p.name for p in inspect.signature(func).parameters.values()]


def get_func_signature(func):
    """
    Retrieves the full signature of the provided function.

    Parameters
    ----------
    func : callable
        Function whose signature is retrieved.

    Returns
    -------
    inspect.Signature
        The full function signature, including argument names and default values.

    Example
    -------
    >>> def example_func(arg1, arg2, kwarg1=None): pass
    >>> get_func_signature(example_func)
    (arg1, arg2, kwarg1=None)
    """
    return inspect.signature(func)


# Caller's frame #
#-#-#-#-#-#-#-#-#-

def get_caller_args():
    """
    Retrieves the required argument names of the caller function.

    Returns
    -------
    list of str
        List of argument names used in the caller function.

    Example
    -------
    >>> def example_func(arg1, arg2): get_caller_args()
    ['arg1', 'arg2']
    """
    caller_frame = inspect.currentframe().f_back
    caller_args, _, _, _ = inspect.getargvalues(caller_frame)
    return list(caller_args)
    

def get_all_caller_args():
    """
    Retrieves all argument names and their values in the caller function.

    Returns
    -------
    dict
        Dictionary of argument names and values used in the caller function.

    Example
    -------
    >>> def example_func(arg1, kwarg1=None): get_all_caller_args()
    {'arg1': value1, 'kwarg1': None}
    """
    caller_frame = inspect.currentframe().f_back
    caller_args, _, _, caller_values = inspect.getargvalues(caller_frame)
    return {arg: caller_values[arg] for arg in caller_args}


def get_caller_signature():
    """
    Retrieves the full signature of the caller function.

    Returns
    -------
    inspect.Signature
        Full signature of the caller function, including argument names and default values.

    Example
    -------
    >>> def example_func(arg1, kwarg1=None): get_caller_signature()
    (arg1, kwarg1=None)
    """
    caller_frame = inspect.currentframe().f_back
    caller_func = caller_frame.f_globals[caller_frame.f_code.co_name]
    return inspect.signature(caller_func)


# Attributes #
#------------#

def get_attr_names(obj):
    """
    Retrieves all non-callable attribute names of the given object.

    Parameters
    ----------
    obj : any
        The object whose attribute names are retrieved.

    Returns
    -------
    list of str
        List of all non-callable attribute names.
    """
    return [attr for attr in dir(obj) if not callable(getattr(obj, attr))]


# Object types #
#--------------#

def get_type_str(obj, lowercase=False):
    """
    Returns the type of an object as a string.

    Parameters
    ----------
    obj : any
        Object whose type is returned as a string.
    lowercase : bool, optional
        If True, returns the type string in lowercase. Defaults to False.

    Returns
    -------
    str
        String representation of the object's type.
    """
    return type(obj).__name__.lower() if lowercase else type(obj).__name__


# More functions related to introspection or utility as needed #
#--------------------------------------------------------------#

def inspect_memory_usage(obj, seen=None):
    """
    Recursively calculates the memory usage of an object and its contents.

    Parameters
    ----------
    obj : any
        The object whose memory usage is to be calculated.
    seen : set, optional
        A set of object IDs already inspected to avoid double-counting 
        in case of cyclic references. Defaults to None.

    Returns
    -------
    int
        Total memory usage of the object and its contents in bytes.

    Raises
    ------
    TypeError
        If the object type cannot be processed by `sys.getsizeof`.

    Example
    -------
    >>> data = [1, 2, [3, 4], {'a': 5, 'b': 6}]
    >>> inspect_memory_usage(data)
    408  # output will vary depending on Python version and system
    """
    if seen is None:
        seen = set()  # Initialize a set to track processed object IDs

    obj_id = id(obj)
    if obj_id in seen:
        return 0  # Avoid double-counting objects

    seen.add(obj_id)  # Mark the object ID as seen
    size = sys.getsizeof(obj)  # Initial size of the object

    # Recursively calculate size for container types
    if isinstance(obj, dict):
        size += sum(inspect_memory_usage(k, seen) + inspect_memory_usage(v, seen) for k, v in obj.items())
    elif isinstance(obj, (list, tuple, set)):
        size += sum(inspect_memory_usage(i, seen) for i in obj)
    elif hasattr(obj, '__dict__'):
        size += inspect_memory_usage(vars(obj), seen)
    elif isinstance(obj, Iterable) and not isinstance(obj, (str, bytes)):
        size += sum(inspect_memory_usage(i, seen) for i in obj)

    return size

    
#--------------------------#
# Parameters and constants #
#--------------------------#

# Supported library list for method name retrievals #
func_name_libs = ["inspect", "sys"]