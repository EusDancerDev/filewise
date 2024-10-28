#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
**Note**

This program is an application of the main module 'pdf_tools',
and it uses the 'file_compressor' attributes and/or functions.
YOU MAY REDISTRIBUTE this program along any other directory,
but keep in mind that the module is designed to work with absolute paths.

It is reccommended to firsly run this first cell, and then one of the 
following cells, instead of running the whole program.
"""

#-----------------------#
# Import custom modules #
#-----------------------#

from pyutils.filewise.format_converters.pdf_tools import file_compressor

#-------------------#
# Define parameters #
#-------------------#

#%%
# 1st case usage #
#----------------#

in_path_str  = "/home/jonander/Documents/apunteak.pdf"
out_path_str = "/home/jonander/Documents/tweaked.pdf"

# For readability purposes, place the method here,
# alongside with the case usage parameters 
file_compressor(in_path_str, out_path_str)

#%%
# 2nd case usage #
#----------------#

in_path_list = ["/home/jonander/Documents/sample_1.pdf",
                "/home/jonander/Documents/sample_2.pdf",
                "/home/jonander/Documents/sample_3.pdf",
                "/home/jonander/Documents/sample_4.pdf"]

out_path_list = ["/home/jonander/Documents/compressed_sample1.pdf",
                 "/home/jonander/Documents/compressed_sample2.pdf",
                 "/home/jonander/Documents/compressed_sample3.pdf",
                 "/home/jonander/Documents/compressed_sample4.pdf",]

# For readability purposes, place the method here,
# alongside with the case usage parameters 
file_compressor(in_path_list, out_path_list)
