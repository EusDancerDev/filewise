#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-----------------------#
# Import custom modules #
#-----------------------#

from pyutils.filewise.format_converters.pdf_tools import msg_to_pdf

#-------------------#
# Define parameters #
#-------------------#

path = "/home/jonander/Documents"

delete_msg_files = False
delete_eml_files = False

#------------------------------------------#
# Convert every Microsoft Outlook message  #
#------------------------------------------#

msg_to_pdf(path, delete_msg_files, delete_eml_files)
