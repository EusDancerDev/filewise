#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
**Note**

This program is an application of the main module 'bulk_rename_auto',
and it uses some of its attributes and/or functions.
YOU MAY REDISTRIBUTE this program along any other directory,
but keep in mind that the module is designed to work with absolute paths.
"""

#------------------------#
# Import project modules #
#------------------------#

from filewise.file_operations.bulk_rename_auto import reorder_objs

#-------------------#
# Define parameters #
#-------------------#

PATH = "/home/jonander/Pictures/2023/Tenerife_test_rename_pygenutils"
OBJ_TYPE = "file"

ZERO_PADDING = 3
EXTENSIONS2SKIP = ""

STARTING_NUMBER = "default"
INDEX_RANGE = "all"

SPLIT_DELIM = None

#------------------#
# Perform the task #
#------------------#

reorder_objs(PATH,
             OBJ_TYPE,
             EXTENSIONS2SKIP,
             INDEX_RANGE,
             STARTING_NUMBER,
             ZERO_PADDING,
             splitdelim=SPLIT_DELIM)
