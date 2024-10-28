#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
**Note**

This program is an application of the main module 'bulk_rename_auto',
and it uses some of its attributes and/or functions.
YOU MAY REDISTRIBUTE this program along any other directory,
but keep in mind that the module is designed to work with absolute paths.
"""

#-----------------------#
# Import custom modules #
#-----------------------#

from pyutils.filewise.file_operations.bulk_rename_auto import reorder_objs

#-------------------#
# Define parameters #
#-------------------#

path = "/home/jonander/Pictures/2023/Tenerife_test_rename_pyutils."
obj_type = "file"

zero_padding = 3
extensions2skip = ""

starting_number = "default"
index_range = "all"

splitdelim = None

#------------------#
# Perform the task #
#------------------#

reorder_objs(path,
             obj_type,
             extensions2skip,
             index_range,
             starting_number,
             zero_padding,
             splitdelim=splitdelim)
