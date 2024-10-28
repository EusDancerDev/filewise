#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-----------------------#
# Import custom modules #
#-----------------------#

from pyutils.arrays_and_lists.data_manipulation import flatten_to_string
from pyutils.operative_systems.os_operations import exit_info, run_system_command
from pyutils.parameters_and_constants.global_parameters import common_delim_list
from pyutils.strings import string_handler, information_output_formatters
from pyutils.filewise.file_operations import ops_handler, path_utils
from pyutils.filewise import introspection_utils 

# Aliases for functions #
#-----------------------#

format_string = information_output_formatters.format_string
format_table_from_lists = information_output_formatters.format_table_from_lists

get_caller_args = introspection_utils.get_caller_args
get_type_str = introspection_utils.get_type_str

remove_files = ops_handler.remove_files
find_files = path_utils.find_files

ext_adder = string_handler.ext_adder
add_str_to_path = string_handler.add_str_to_aux_path

#------------------#
# Define functions #
#------------------#

def tweak_pages(file, cat_str, out_path=None):
    """
    Modify and select specific pages in a PDF file based on the provided page string.

    Parameters
    ----------
    file : str
        Path to the PDF file to be modified.
    cat_str : str
        Page selection string for the 'pdftk' command.
    out_path : str, optional
        Destination path for the modified PDF file. If None, generates a default name.
    """
    if out_path is None:
        out_path = add_str_to_path(file, f"_{cat_str}")
        if len(out_path) > 60:
            out_path = add_str_to_path(file, "_lotsOfPagesTweaked")

    command = f"{essential_command_list[1]} '{file}' cat {cat_str} output '{out_path}'"
    process_exit_info = run_system_command(command)
    exit_info(process_exit_info)


def file_tweaker(path, cat_obj):
    """
    Configure and modify pages in one or multiple PDF files based on specified configurations.

    Parameters
    ----------
    path : str or list of str
        Path(s) to the PDF file(s) for page manipulation.
    cat_obj : str, dict, or list of dict
        Object defining output filenames and page configurations.

    Raises
    ------
    SyntaxError
        If `cat_obj` is a str but does not contain the required delimiter.
    TypeError
        If `path` and `cat_obj` do not match one of the allowed type patterns:
        - str and str
        - str and dict
        - list and list
    """
    split_delim = common_delim_list[2]
    if isinstance(path, str) and isinstance(cat_obj, str):
        if split_delim not in cat_obj:
            raise SyntaxError(syntax_error_str)
        cat_str, out_path = cat_obj.split(split_delim)
        out_path = ext_adder(out_path, extensions[0])
        tweak_pages(path, cat_str, out_path)
    elif isinstance(path, str) and isinstance(cat_obj, dict):
        for out_path, cat_str in cat_obj.items():
            out_path = ext_adder(out_path, extensions[0])
            tweak_pages(path, cat_str, out_path)
    elif isinstance(path, list) and isinstance(cat_obj, list):
        for p, co_obj in zip(path, cat_obj):
            for out_path, cat_str in co_obj.items():
                out_path = ext_adder(out_path, extensions[0])
                tweak_pages(p, cat_str, out_path)
    else:
        param_keys = get_caller_args()
        type_param1, type_param2 = get_type_str(path), get_type_str(cat_obj)
        type_combo_list1 = [["str", "str"], ["str", "dict"], ["list", "list"]]
        
        raise TypeError(format_string(format_string(type_error_str, (type_param1, type_param2)), 
                                      format_table_from_lists(param_keys, type_combo_list1)))
   
    
def merge_files(in_path_list, out_path=None):
    """
    Merge multiple PDF files into a single PDF document.

    Parameters
    ----------
    in_paths : list of str
        List of input PDF file paths to merge.
    out_path : str, optional
        Path for the merged PDF file. Defaults to 'merged_doc.pdf' if None.
    """
    all_in_paths = flatten_to_string(in_path_list)
    out_path = out_path or ext_adder("merged_doc", extensions[0])
    command = format_string(pdfunite_command_prefmt, (all_in_paths, out_path))
    process_exit_info = run_system_command(command)
    exit_info(process_exit_info)


def file_compressor(in_path, out_path=None):
    """
    Compress one or multiple PDF files with minimal quality loss.

    Parameters
    ----------
    in_path : str or list of str
        Path(s) to the PDF file(s) for compression.
    out_path : str, list of str, or None, optional
        Output path(s) for the compressed file(s). Defaults to 'compressed_doc.pdf' if None.

    Raises
    ------
    TypeError
        If `in_path` and `out_path` do not match one of the allowed type patterns:
        - str and str
        - str and None
        - list and list
    """
    if isinstance(in_path, str) and (isinstance(out_path, str) or out_path is None):
        in_path = [in_path]
        out_path = [out_path or "compressed_doc"]
    elif isinstance(in_path, list) and isinstance(out_path, list):
        out_path = [op or "compressed_doc" for op in out_path]
    else:
        param_keys = get_caller_args()
        type_param1, type_param2 = get_type_str(in_path), get_type_str(out_path)
        type_combo_list2 = [["str", "str"], ["str", "None"], ["list", "list"]]
        
        raise TypeError(format_string(format_string(type_error_str, (type_param1, type_param2)), 
                                      format_table_from_lists(param_keys, type_combo_list2)))

    for ip, op_aux in zip(in_path, out_path):
        op = ext_adder(op_aux, extensions[0])
        command = f"{essential_command_list[0]} -dPDFSETTINGS=/ebook {ip} {op}"
        process_exit_info = run_system_command(command)
        exit_info(process_exit_info)
   

# Conversion Functions #
#----------------------#

def eml_to_pdf(search_path, delete_eml_files=False):
    """
    Convert .eml files to PDF, with an option to delete .eml files post-conversion.

    Parameters
    ----------
    src_path : str
        Path to search for '.eml' files.
    del_eml : bool, optional
        Whether to delete '.eml' files after conversion. Defaults to False.
    """
    eml_files = find_files(extensions[1], search_path, match_type="ext", top_path_only=True)
    converter_tool_path = find_files(f"*emailconverter*.{extensions[-1]}", alldoc_dirpath, match_type="glob")
    for emlf in eml_files:
        command = f"java -jar {converter_tool_path} '{emlf}'"
        process_exit_info = run_system_command(command)
        exit_info(process_exit_info)
    if delete_eml_files:
        remove_files(extensions[1], search_path)


def msg_to_pdf(search_path, delete_msg_files=False, delete_eml_files=False):
    """
    Convert .msg files to .pdf or .eml files to .pdf, with deletion options.

    Parameters
    ----------
    src_path : str
        Path to search for '.msg' files.
    del_msg : bool, optional
        If True, deletes '.msg' files after conversion.
    del_eml : bool, optional
        If True, deletes '.eml' files after conversion.
    """
    msg_files = find_files(extensions[2], search_path, match_type="ext", top_path_only=True)
    for msgf in msg_files:
        command = f"{essential_command_list[3]} '{msgf}'"
        process_exit_info = run_system_command(command)
        exit_info(process_exit_info)
    eml_to_pdf(search_path, delete_eml_files=delete_eml_files)
    if delete_msg_files:
        remove_files(extensions[2], search_path)

# Utility Functions #
#-------------------#

def _check_essential_progs():
    """
    Verify the installation of essential programs required for PDF and file manipulation.
    
    Raises
    ------
    ModuleNotFoundError
        If any required program is not installed, lists missing programs.
    """
    non_installed_prog_list = []
    for prog in essential_program_list:
        command = f"dpkg -l | grep -i {prog} | wc -l"
        process_exit_info = run_system_command(command, capture_output=True)
        exit_info(process_exit_info)
        if int(process_exit_info.get("stdout")) < 1:
            non_installed_prog_list.append(prog)
    if non_installed_prog_list:
        raise ModuleNotFoundError(format_string(essential_prog_not_found_error, non_installed_prog_list))


# Parameters and Constants #
#--------------------------#

alldoc_dirpath = "/home/jonander/Documents"
extensions = ["pdf", "eml", "msg", "jar"]

essential_program_list = [
    "ghostscript", 
    "pdftk", 
    "wkhtmltopdf", 
    "libemail-address-xs-perl", 
    "poppler-utils"
    ]

essential_command_list = [
    "ps2pdf",
    "pdftk",
    "wkhtmltopdf",
    "mgsconvert",
    "pdfunite"
    ]

syntax_error_str = """Please use a semicolon (';') to separate the page cat string\
from the output path. For example: '{cat_str}; {out_path}'"""
     
type_error_str = """Unsupported parameter type pair '{}' and '{}'. It must be\
one of the following table:
{}
"""

essential_prog_not_found_error = "Programs missing for module functionality:\n{}"

pdfunite_command_prefmt = "pdfunite {} {}"

# Initialize #
#------------#

# Check for essential program installation #
_check_essential_progs()
