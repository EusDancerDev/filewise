#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#------------------------#
# Import project modules #
#------------------------#

from filewise.file_operations.ops_handler import remove_files
from filewise.file_operations.path_utils import find_files
from filewise.general.introspection_utils import get_caller_args, get_type_str
from paramlib.global_parameters import COMMON_DELIMITER_LIST
from pygenutils.arrays_and_lists.data_manipulation import flatten_list, flatten_to_string
from pygenutils.operative_systems.os_operations import exit_info, run_system_command
from pygenutils.strings.string_handler import ext_adder, add_str_to_path
from pygenutils.strings.text_formatters import format_string, format_table_from_lists

#------------------#
# Define functions #
#------------------#

def tweak_pages(
        file: str, 
        cat_str: str, 
        out_path: str | None = None,
        capture_output: bool = False,
        return_output_name: bool = False,
        encoding: str = "utf-8",
        shell: bool = True) -> None:
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
    capture_output : bool, optional
        Whether to capture the command output. Default is False.
    return_output_name : bool, optional
        Whether to return file descriptor names. Default is False.
    encoding : str, optional
        Encoding to use when decoding command output. Default is "utf-8".
    shell : bool, optional
        Whether to execute the command through the shell. Default is True.
    """
    if out_path is None:
        out_path = add_str_to_path(file, f"_{cat_str}")
        if len(out_path) > 60:
            out_path = add_str_to_path(file, "_lotsOfPagesTweaked")

    # Define the command based on the given options
    pdftk_template_formatted = f"{ESSENTIAL_COMMAND_LIST[1]} '{file}' cat {cat_str} output '{out_path}'"
    
    # Run the command
    process_exit_info = run_system_command(
        pdftk_template_formatted,
        capture_output=capture_output,
        return_output_name=return_output_name,
        encoding=encoding,
        shell=shell
    )
    # Call exit_info with parameters based on capture_output
    exit_info(
        process_exit_info,
        check_stdout=capture_output,
        check_stderr=capture_output,
        check_return_code=True
    )


def file_tweaker(path: str | list, cat_obj: str | dict | list) -> None:
    """
    Configure and modify pages in one or multiple PDF files based on specified configurations.

    Parameters
    ----------
    path : str | list
        Path(s) to the PDF file(s) for page manipulation. Supports nested lists.
    cat_obj : str | dict | list
        Object defining output filenames and page configurations. Supports nested structures.

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
    # Apply defensive programming for nested lists
    path = flatten_list(path) if isinstance(path, list) else path
    cat_obj = flatten_list(cat_obj) if isinstance(cat_obj, list) else cat_obj
    
    split_delim = COMMON_DELIMITER_LIST[2]
    if isinstance(path, str) and isinstance(cat_obj, str):
        if split_delim not in cat_obj:
            raise SyntaxError(SYNTAX_ERROR_STR)
        cat_str, out_path = cat_obj.split(split_delim)
        out_path = ext_adder(out_path, EXTENSIONS[0])
        tweak_pages(path, cat_str, out_path)
    elif isinstance(path, str) and isinstance(cat_obj, dict):
        for out_path, cat_str in cat_obj.items():
            out_path = ext_adder(out_path, EXTENSIONS[0])
            tweak_pages(path, cat_str, out_path)
    elif isinstance(path, list) and isinstance(cat_obj, list):
        for p, co_obj in zip(path, cat_obj):
            for out_path, cat_str in co_obj.items():
                out_path = ext_adder(out_path, EXTENSIONS[0])
                tweak_pages(p, cat_str, out_path)
    else:
        param_keys = get_caller_args()
        type_param1, type_param2 = get_type_str(path), get_type_str(cat_obj)
        type_combo_list1 = [["str", "str"], ["str", "dict"], ["list", "list"]]
        
        raise TypeError(format_string(format_string(TYPE_ERROR_STR, (type_param1, type_param2)), 
                                      format_table_from_lists(param_keys, type_combo_list1)))
   
    
def merge_files(
        in_path_list: list, 
        out_path: str | None = None,
        capture_output: bool = False,
        return_output_name: bool = False,
        encoding: str = "utf-8",
        shell: bool = True) -> None:
    """
    Merge multiple PDF files into a single PDF document.

    Parameters
    ----------
    in_path_list : list
        List of input PDF file paths to merge. Supports nested lists.
    out_path : str, optional
        Path for the merged PDF file. Defaults to 'merged_doc.pdf' if None.
    capture_output : bool, optional
        Whether to capture the command output. Default is False.
    return_output_name : bool, optional
        Whether to return file descriptor names. Default is False.
    encoding : str, optional
        Encoding to use when decoding command output. Default is "utf-8".
    shell : bool, optional
        Whether to execute the command through the shell. Default is True.
    """
    # Apply defensive programming for nested lists
    in_path_list = flatten_list(in_path_list)
    
    all_in_paths = flatten_to_string(in_path_list)
    out_path = out_path or ext_adder("merged_doc", EXTENSIONS[0])
    # Define the command for merging files
    pdfunite_cmd = format_string(PDFUNITE_TEMPLATE, (all_in_paths, out_path))

    # Run the command
    process_exit_info = run_system_command(
        pdfunite_cmd,
        capture_output=capture_output,
        return_output_name=return_output_name,
        encoding=encoding,
        shell=shell
    )

    # Call exit_info with parameters based on capture_output
    exit_info(
        process_exit_info,
        check_stdout=capture_output,
        check_stderr=capture_output,
        check_return_code=True
    )


def file_compressor(
        in_path: str | list, 
        out_path: str | list | None = None,
        capture_output: bool = False,
        return_output_name: bool = False,
        encoding: str = "utf-8",
        shell: bool = True) -> None:
    """
    Compress one or multiple PDF files with minimal quality loss.

    Parameters
    ----------
    in_path : str | list
        Path(s) to the PDF file(s) for compression. Supports nested lists.
    out_path : str | list | None, optional
        Output path(s) for the compressed file(s). Defaults to 'compressed_doc.pdf' if None.
        Supports nested lists when in_path is also a list.
    capture_output : bool, optional
        Whether to capture the command output. Default is False.
    return_output_name : bool, optional
        Whether to return file descriptor names. Default is False.
    encoding : str, optional
        Encoding to use when decoding command output. Default is "utf-8".
    shell : bool, optional
        Whether to execute the command through the shell. Default is True.
        
    Raises
    ------
    TypeError
        If `in_path` and `out_path` do not match one of the allowed type patterns:
        - str and str
        - str and None
        - list and list
    """
    # Apply defensive programming for nested lists
    if isinstance(in_path, list):
        in_path = flatten_list(in_path)
    if isinstance(out_path, list):
        out_path = flatten_list(out_path)
    
    if isinstance(in_path, str) and (isinstance(out_path, str) or out_path is None):
        in_path = [in_path]
        out_path = [out_path or "compressed_doc"]
    elif isinstance(in_path, list) and isinstance(out_path, list):
        out_path = [op or "compressed_doc" for op in out_path]
    else:
        param_keys = get_caller_args()
        type_param1, type_param2 = get_type_str(in_path), get_type_str(out_path)
        type_combo_list2 = [["str", "str"], ["str", "None"], ["list", "list"]]
        
        raise TypeError(format_string(format_string(TYPE_ERROR_STR, (type_param1, type_param2)), 
                                      format_table_from_lists(param_keys, type_combo_list2)))

    for ip, op_aux in zip(in_path, out_path):
        op = ext_adder(op_aux, EXTENSIONS[0])
        # Define the command for compression
        ps2pdf_template_formatted = f"{ESSENTIAL_COMMAND_LIST[0]} -dPDFSETTINGS=/ebook {ip} {op}"

        # Run the command
        process_exit_info = run_system_command(
            ps2pdf_template_formatted,
            capture_output=capture_output,
            return_output_name=return_output_name,
            encoding=encoding,
            shell=shell
        )

        # Call exit_info with parameters based on capture_output
        exit_info(
            process_exit_info,
            check_stdout=capture_output,
            check_stderr=capture_output,
            check_return_code=True
        )
   

# Conversion Functions #
#----------------------#

def eml_to_pdf(
        search_path: str, 
        delete_eml_files: bool = False,
        capture_output: bool = False,
        return_output_name: bool = False,
        encoding: str = "utf-8",
        shell: bool = True) -> None:
    """
    Convert .eml files to PDF, with an option to delete .eml files post-conversion.

    Parameters
    ----------
    src_path : str
        Path to search for '.eml' files.
    del_eml : bool, optional
        Whether to delete '.eml' files after conversion. Defaults to False.
    """
    eml_files = find_files(EXTENSIONS[1], search_path, match_type="ext", top_path_only=True)
    converter_tool_path = find_files(f"*emailconverter*.{EXTENSIONS[-1]}", ALLDOC_DIRPATH, match_type="glob")
    for emlf in eml_files:
        converter_template_formatted = f"java -jar {converter_tool_path} '{emlf}'"

        # Run the command
        process_exit_info = run_system_command(
            converter_template_formatted,
            capture_output=capture_output,
            return_output_name=return_output_name,
            encoding=encoding,
            shell=shell
        )
        # Call exit_info with parameters based on capture_output
        exit_info(
            process_exit_info,
            check_stdout=capture_output,
            check_stderr=capture_output,
            check_return_code=True
        )
    if delete_eml_files:
        remove_files(EXTENSIONS[1], search_path)


def msg_to_pdf(
        search_path: str, 
        delete_msg_files: bool = False, 
        delete_eml_files: bool = False,
        capture_output: bool = False,
        return_output_name: bool = False,
        encoding: str = "utf-8",
        shell: bool = True) -> None:
    """
    Convert .msg files to .pdf or .eml files to .pdf, with deletion options.

    Parameters
    ----------
    search_path : str
        Path to search for '.msg' files.
    delete_msg_files : bool, optional
        If True, deletes '.msg' files after conversion.
    delete_eml_files : bool, optional
        If True, deletes '.eml' files after conversion.
    capture_output : bool, optional
        Whether to capture the command output. Default is False.
    return_output_name : bool, optional
        Whether to return file descriptor names. Default is False.
    encoding : str, optional
        Encoding to use when decoding command output. Default is "utf-8".
    shell : bool, optional
        Whether to execute the command through the shell. Default is True.
    """
    msg_files = find_files(EXTENSIONS[2], search_path, match_type="ext", top_path_only=True)
    for msgf in msg_files:
        msg_to_pdf_template_formatted = f"{ESSENTIAL_COMMAND_LIST[3]} '{msgf}'"

        # Run the command
        process_exit_info = run_system_command(
            msg_to_pdf_template_formatted,
            capture_output=capture_output,
            return_output_name=return_output_name,
            encoding=encoding,
            shell=shell
        )
        # Call exit_info with parameters based on capture_output
        exit_info(
            process_exit_info,
            check_stdout=capture_output,
            check_stderr=capture_output,
            check_return_code=True
        )
    eml_to_pdf(search_path, delete_eml_files=delete_eml_files)
    if delete_msg_files:
        remove_files(EXTENSIONS[2], search_path)

# Utility Functions #
#-------------------#

def _check_essential_progs(
        capture_output: bool = False,
        return_output_name: bool = False,
        encoding: str = "utf-8",
        shell: bool = True) -> None:
    """
    Verify the installation of essential programs required for PDF and file manipulation.
    
    Parameters
    ----------
    capture_output : bool, optional
        Whether to capture the command output. Default is False.
    return_output_name : bool, optional
        Whether to return file descriptor names. Default is False.
    encoding : str, optional
        Encoding to use when decoding command output. Default is "utf-8".
    shell : bool, optional
        Whether to execute the command through the shell. Default is True.
    
    Raises
    ------
    ModuleNotFoundError
        If any required program is not installed, lists missing programs.
    """
    non_installed_prog_list = []
    for prog in ESSENTIAL_PROGRAM_LIST:
        dpkg_template_formatted = f"dpkg -l | grep -i {prog} | wc -l"

        # Run the command
        process_exit_info = run_system_command(
            dpkg_template_formatted,
            capture_output=capture_output,
            return_output_name=return_output_name,
            encoding=encoding,
            shell=shell
        )
        # Call exit_info with parameters based on capture_output
        exit_info(
            process_exit_info,
            check_stdout=capture_output,
            check_stderr=capture_output,
            check_return_code=True
        )
        if int(process_exit_info.get("stdout")) < 1:
            non_installed_prog_list.append(prog)
    if non_installed_prog_list:
        raise ModuleNotFoundError(format_string(ESSENTIAL_PROG_NOT_FOUND_ERROR, non_installed_prog_list))


# Parameters and Constants #
#--------------------------#

ALLDOC_DIRPATH = "/home/jonander/Documents"
EXTENSIONS = ["pdf", "eml", "msg", "jar"]

ESSENTIAL_PROGRAM_LIST = [
    "ghostscript", 
    "pdftk", 
    "wkhtmltopdf", 
    "libemail-address-xs-perl", 
    "poppler-utils"
    ]

ESSENTIAL_COMMAND_LIST = [
    "ps2pdf",
    "pdftk",
    "wkhtmltopdf",
    "mgsconvert",
    "pdfunite"
    ]

SYNTAX_ERROR_STR = """Please use a semicolon (';') to separate the page cat string\
from the output path. For example: '{cat_str}; {out_path}'"""
     
TYPE_ERROR_STR = """Unsupported parameter type pair '{}' and '{}'. It must be\
one of the following table:
{}
"""

ESSENTIAL_PROG_NOT_FOUND_ERROR = "Programs missing for module functionality:\n{}"

PDFUNITE_TEMPLATE = "pdfunite {} {}"

# Initialize #
#------------#

# Check for essential program installation #
_check_essential_progs()
