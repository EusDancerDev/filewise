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

#------------------------#
# Import project modules #
#------------------------#

from filewise.format_converters.pdf_tools import file_compressor

#-------------------#
# Define parameters #
#-------------------#

#%%
# 1st case usage #
#----------------#

IN_PATH_STR = "/home/jonander/Documents/apunteak.pdf"
OUT_PATH_STR = "/home/jonander/Documents/tweaked.pdf"

# For readability purposes, place the function here,
# alongside with the case usage parameters 
file_compressor(IN_PATH_STR, OUT_PATH_STR)

#%%
# 2nd case usage #
#----------------#

IN_PATH_LIST = ["/home/jonander/Documents/sample_1.pdf",
                "/home/jonander/Documents/sample_2.pdf",
                "/home/jonander/Documents/sample_3.pdf",
                "/home/jonander/Documents/sample_4.pdf"]

OUT_PATH_LIST = ["/home/jonander/Documents/compressed_sample1.pdf",
                 "/home/jonander/Documents/compressed_sample2.pdf",
                 "/home/jonander/Documents/compressed_sample3.pdf",
                 "/home/jonander/Documents/compressed_sample4.pdf",]

# For readability purposes, place the function here,
# alongside with the case usage parameters 
file_compressor(IN_PATH_LIST, OUT_PATH_LIST)
