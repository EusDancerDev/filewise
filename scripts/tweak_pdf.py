#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
**Note**

This program is an application of the main module 'pdf_tools',
and it uses the 'file_tweaker' attributes and/or functions.
YOU MAY REDISTRIBUTE this program along any other directory,
but keep in mind that the module is designed to work with absolute paths.
"""

#-----------------------#
# Import custom modules #
#-----------------------#

from pyutils.filewise.format_converters.pdf_tools import file_tweaker

#-------------------#
# Define parameters #
#-------------------#

"""
As described in the original module,
the main class distinguishes among these three cases:

1. Both the path and cat string are single strings
--------------------------------------------------

In this case, a sole output file is created from a single input file.
Then in order to distinguish
between the path (WITH or WITHOUT THE EXTENSION) and 
the string to assemble or catenate pages,
the following structure is used:
f"{output_path}; {cat_string}"

The semicolon is absolutely necessary, because the function
is designed to split the string is splitted
according to that character. 
The space aroun the semicolon is not necessary and
serves only as a description.

2. The path is a string, and the catenation object is a dictionary
------------------------------------------------------------------

Then it is understood that several files are going to be created
from a single input file.

The dictionary has to be structured like the following:

input_path --> type string --> it corresponds this object:
{output_path_1 : cat_str_1,
 output_path_2 : cat_str_2,
             (...)        ,
 output_path_n : cat_str_n}

3. Both the path and catenation object are lists
------------------------------------------------

This is the most complete case, in which each file
is splitted into several files.
There must be a catenation object per input path,
so the structure of the case is as follows:

input_path_1 --> type string --> it corresponds this object:
{output_path_1 : cat_str_1,
 output_path_2 : cat_str_2,
             (...)        ,
 output_path_n : cat_str_n}

[...]

input_path_n --> type string --> it corresponds this object:
{output_path_n+1 : cat_str_n+1,
 output_path_n+2 : cat_str_n+2,
               (...)        ,
 output_path_n+m : cat_str_n+m}


In order to maintain the required variable names to use the 'file_tweaker'
method, instead of centralizing under a generic name,
the program is splitted into three blocks, each for a case usage,
where at the end of it the method is implemented.

It is reccommended to firsly run this first cell, and then one of the 
following cells, instead of running the whole program.
"""

#%%
# 1st case usage #
#----------------#

path_str = "/home/jonander/Documents/apunteak.pdf"
output_path_str = "/home/jonander/Documents/tweaked.pdf"
cat_str = "1-2 8"

cat_out_str = f"{cat_str}; {output_path_str}"

# For readability purposes, place the method here,
# alongside with the case usage parameters 
file_tweaker(path_str, cat_out_str)

#%%
# 2nd case usage #
#----------------#

path_str = "/home/jonander/Documents/sample_1.pdf"

output_path_list = ["output_path_1",
                    "output_path_2",
                    "output_path_3",
                    "output_path_4"]

cat_str_list = ["1-25 34-end",
                "27-30 78 79 84 76-77west",
                "36 38 31 32 56up",
                "2-endnorth"]

cat_out_dict = {out_path : cat_str 
                for out_path, cat_str in zip(output_path_list, cat_str_list)}

# For readability purposes, place the method here,
# alongside with the case usage parameters 
file_tweaker(path_str, cat_out_dict)

#%%
# 3rd case usage #
#----------------#

path_list = ["/home/jonander/Documents/sample_1.pdf",
             "Hizkuntzak/sample_2.pdf"]

output_path_lists = [
    ["output_path_1",
     "output_path_2",
     "output_path_3",
     "output_path_4"],
    
    ["output_path_5",
     "output_path_6",
     "output_path_7",
     "output_path_8"],
    ]

cat_str_lists = [
    ["1-25 34-end",
     "27-30 78 79 84 76-77west",
     "36 38 31 32 56up",
     "2-endnorth"],
    
    ["4-end",
     "24east 45",
     "83 34north 48up",
     "4east-7",
     "1-2 8"],
    ]

cat_out_dict_list\
= [{out_path : cat_str 
    for out_path, cat_str in zip(output_path_list, cat_str_list)
    for output_path_list, cat_str_list in zip(output_path_lists, cat_str_list)}]

# For readability purposes, place the method here,
# alongside with the case usage parameters 
file_tweaker(path_list, cat_out_dict_list)
