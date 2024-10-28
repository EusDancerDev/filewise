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
of the module `permission_manager` (subpackage `file_operations` in `filewise`).
"""

#-----------------------#
# Import custom modules #
#-----------------------#

from pyutils.filewise.file_operations.permission_manager import modify_obj_owner, modify_obj_permissions

#-------------------#
# Define parameters #
#-------------------#

# File objects #
#--------------#

# Path to search for directories and files
path = "/home/jonander/Documents"

# Extensions excluded from searching #
extensions2skip = ""

# File object properties #
#------------------------#
    
# Permission ID #
attr_id = -1
    
# Owner and group names or IDs 
new_owner = -1
new_group = -1

# Owner modification method params #
#----------------------------------#

# Module to use for #
module = "shutil"

#------------#
# Operations #
#------------#

modify_obj_permissions(path, extensions2skip, attr_id)
modify_obj_owner(path, module, extensions2skip, new_owner, new_group)
