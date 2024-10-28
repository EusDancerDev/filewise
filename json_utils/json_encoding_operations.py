#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#------------------#
# Define functions #
#------------------#

# Unsupported object types #
#--------------------------#

def to_json(python_object):
    """
    Serialise a Python object to a JSON-compatible dictionary.

    Parameters
    ----------
    python_object : object
        The Python object to serialise. 
        Only bytes are supported; other types will raise a TypeError.

    Returns
    -------
    json_dict : dict
        A JSON-compatible dictionary representation of the input object. 
        For bytes, it includes a class identifier and the byte values as a list.

    Raises
    ------
    TypeError: If the input object is of an unsupported type.
    """
    if isinstance(python_object, bytes):
        json_dict = {'__class__': 'bytes', '__value__': list(python_object)}
        return json_dict
    raise TypeError(f"{repr(python_object)} non serialisable")
    

def from_json(json_object):
    """
    Deserialise a JSON-compatible dictionary back to a Python object.

    Parameters
    ----------
    json_object : dict
        The JSON-compatible dictionary to deserialise.
        Expected to have a class identifier for supported types.

    Returns
    -------
    bytes or object
        The corresponding Python object. 
        If the input dictionary has a class identifier for bytes,
        it is converted back to a bytes object; 
        otherwise, the original input object is returned unchanged.

    Raises
    ------
    KeyError
        If the input dictionary does not have a valid class identifier.
    """
    if '__class__' in json_object:
        if json_object['__class__'] == 'bytes':
            bytes_obj = bytes(json_object['__value__'])
            return bytes_obj
    return json_object
