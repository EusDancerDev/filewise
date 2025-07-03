#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
**Note**

This program is an application of the main module 'change_permissions_main',
and it uses the 'modify_obj_permissions' and 'modify_obj_owner' 
attributes and/or functions.
YOU MAY REDISTRIBUTE this program along any other directory,
but keep in mind that the module is designed to work with absolute paths.

For more information about file object parameters, refer to the documentation
of the module `permission_manager` (sub-package `file_operations` in `filewise`).
"""

#-----------------------#
# Import project modules #
#------------------------#

from filewise.file_operations.permission_manager import modify_obj_owner, modify_obj_permissions

#-------------------#
# Define parameters #
#-------------------#

# File objects #
#--------------#

# Path to search for directories and files
PATH = "/home/jonander/Documents"

# Extensions excluded from searching #
EXTENSIONS2SKIP = ""

# File object properties #
#------------------------#
    
# Permission ID #
ATTR_ID = -1
    
# Owner and group names or IDs 
NEW_OWNER = -1
NEW_GROUP = -1

# Owner modification function params #
#-----------------------------------#

# Module to use for #
MODULE = "shutil"

#------------#
# Operations #
#------------#

modify_obj_permissions(PATH, EXTENSIONS2SKIP, ATTR_ID)
modify_obj_owner(PATH, MODULE, EXTENSIONS2SKIP, NEW_OWNER, NEW_GROUP)
