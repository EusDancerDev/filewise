# filewise Changelog

All notable changes to this project will be documented in this file.

---

## [3.10.2] - 2025-06-27

### Fixed (3.10.2)

#### **General** (fixing; 3.10.2)

- **Documentation and Consistency**
  - Fix missing/incomplete docstrings across filewise package
  - Changes:
    - Modernised functions with complete documentation following Python 3.10+ standards and NumPy conventions.
    - Resolved parameter mismatches and added comprehensive error handling docs.
    - Achieves 100% docstring coverage.
  - Files affected:
    - `pandas_utils/data_manipulation.py`
    - `file_operations/ops_handler.py`
    - `file_operations/path_utils.py`
    - `file_operations/bulk_rename_auto.py`

### Changed (3.10.2)

#### **General** (changing; 3.10.2)

- **Type Hint Standardisation**
  - Comprehensive audit and standardisation of type hints across all modules when using the "|" operator
  - Ensured proper distinction between:
    - Built-in types (lowercase: `str`, `list`, `dict`, `tuple`)
    - Typing module imports (capitalised: `Any`, `Callable`)
  - Adopted Python 3.10+ union syntax (`|`) consistently across all modules
  - Added missing imports from typing module where needed

- Module `introspection_utils.py`:
  - **Fixed**: added `from typing import Any, Callable` imports
  - **Updated**:
    - Changed all instances of lowercase `any` to `Any` in type hints and docstrings
    - Changed all instances of lowercase `callable` to `Callable` in type hints and docstrings
  - Functions affected:
    - `get_all_caller_args`
    - `get_attr_names`
    - `get_type_str`
    - `inspect_memory_usage`
    - `get_func_args`
    - `get_all_func_args`
    - `get_func_signature`

#### **File Operations** (changing; 3.10.2)

- Module `path_utils.py`:
  - **Fixed**: Removed extra closing parentheses from `flatten_list` function calls on lines 190, 269, and 338 that were causing syntax errors

#### **JSON Utils** (changing; 3.10.2)

- Module `json_encoding_operations.py`:
  - **Fixed**: added `Any` import
  - **Updated**: changed lowercase `any` to `Any` in type hints for `to_json` and `from_json` functions

- Module `json_obj_handler.py`:
  - **Fixed**: added `Any, Callable` imports
  - **Updated**: changed lowercase `any` to `Any` and `callable` to `Callable` in type hints
  - Function affected: `serialise_to_json`

#### **Pandas Utils** (changing; 3.10.2)

- Module `pandas_obj_handler.py`:
  - **Fixed**: corrected docstring capitalisation inconsistencies to match function signatures:

  | Old | New |
  |:---:|:---:|
  | `List[pd.DataFrame]` | `list[pd.DataFrame]` |
  | `List[Tuple[str, str]]` | `list[tuple[str, str]]` |  
  
  - Function affected: `standardise_time_series`

- Module `data_manipulation.py`:
  - **Fixed**: added `Callable` import
  - **Updated**: changed all instances of lowercase `callable` to `Callable` in type hints and docstrings
  - Functions affected:
    - `sort_df_values`
    - `sort_df_indices`
    - `create_pivot_table`

#### **Xarray Utils** (changing; 3.10.2)

- Module `xarray_obj_handler.py`:
  - **Fixed**: added `Any` import
  - **Updated**: changed lowercase `any` to `Any` in type hints for `_ensure_list` function

---

## [3.10.1] - 2025-06-26

### Changed (3.10.1)

#### **File Operations** (changing; 3.10.1)

- Modules `path_utils.py`, `permission_manager.py`, and `ops_handler.py`:
  - Removed `list` call on function `flatten_list`, as by default it returns a list

---

## [3.10.0] - 2025-06-24

### Added (3.10.0)

#### **File Operations** (adding; 3.10.0)

- Goal:
  - Implement defensive programming to handle arbitrarily nested list structures in parameters that accept both strings and lists
  - Functions now safely process inputs like `["ext1", ["ext2", "ext3"], "ext4"]` by flattening them automatically
  - Prevent runtime crashes when nested lists are passed as input parameters

- Module `path_utils.py`:
  - Enhanced functions with nested list support:
    - `find_files`: `patterns` and `dirs_to_exclude` parameters
    - `find_dirs_with_files`: `patterns` and `dirs_to_exclude` parameters  
    - `find_items`: `skip_ext` and `dirs_to_exclude` parameters

  - Module `permission_manager.py`:
    - Enhanced functions with nested list support:
    - `modify_obj_permissions`: `extensions2skip` parameter
    - `modify_obj_owner`: `extensions2skip` parameter

#### **Format Converters** (adding; 3.10.0)

- Module `pdf_tools.py`:
  - Add nested list support by importing and using `flatten_list` from `pygenutils.arrays_and_lists.data_manipulation`
  - Implement defensive programming for `file_tweaker`, `merge_files`, and `file_compressor` functions
  - Functions now safely process nested list inputs like `[["file1.pdf", ["file2.pdf", "file3.pdf"]], "file4.pdf"]`
  - Prevent runtime crashes when complex nested structures are passed as input parameters

#### **Pandas Utils** (adding; 3.12.0)

- Modules `pandas_obj_handler.py` and `data_manipulation.py`:
  - Add nested list support for functions accepting list parameters
  - Implement defensive programming for `merge_excel_files`, `merge_csv_files`, `sort_df_values`, and `create_pivot_table`
  - Enhanced parameter validation with automatic flattening of arbitrarily nested list structures
  - Improved robustness for data processing workflows with complex input structures

#### **Scripts** (adding; 3.10.0)

- Module `copy_compress.py`:
  - Add comprehensive defensive programming with parameter validation and structured workflow management
  - Implement nested list support and enhanced error handling for file operations
  - Add PEP-604 type annotations and improved robustness for complex file management workflows

#### **Xarray Utils** (adding; 3.10.0)

- All modules (`conversions.py`, `file_utils.py`, `patterns.py`, `xarray_obj_handler.py`, `data_manipulation.py`):
  - Add comprehensive defensive programming with parameter validation and nested list support
  - Implement enhanced error handling and Path object compatibility throughout
  - Add PEP-604 type annotations (`str | list[str]`) replacing legacy union syntax
  - Enhanced file existence checks, extension validation, and integrity verification
  - Improved robustness for handling complex input structures and edge cases

### Changed (3.10.0)

#### **General** (changing; 3.10.0)

##### **Update variable names and key names** (changing; 3.10.0)

- Changes have been made in the original file `global_parameters.py` in the `paramlib` package.
- These include abbreviation addressing and variable/key name standardisation.

| Module | Old variable name | New variable name | Old key name | New key name |
|:------:|:-----------------:|:-----------------:|:------------:|:------------:|
| `file_operations/bulk_rename_auto.py` | `NON_STD_TIME_FORMAT_STRS` | `NON_STANDARD_TIME_FORMAT_STRS` | `CFT_H` | `CTIME_H` |
| `format_converters/pdf_tools.py` | `COMMON_DELIM_LIST` | `COMMON_DELIMITER_LIST` | `(N/A)` | `(N/A)` |
| `xarray_utils/patterns.py` | `COMMON_DELIM_LIST` | `COMMON_DELIMITER_LIST` | `(N/A)` | `(N/A)` |

##### **Type Annotation Modernisation** (changing; 3.10.0)

- **Format Converters (`pdf_tools.py`)**:
  - Replace missing type annotations with comprehensive PEP-604 syntax
  - Update `tweak_pages`, `eml_to_pdf`, `msg_to_pdf`, `_check_essential_progs` with modern union operators (`|`)
  - Enhanced parameter and return type specifications

- **General (`introspection_utils.py`)**:
  - Complete modernisation of all function signatures with PEP-604 type annotations
  - Replace legacy type hints with modern union syntax (`str | None` instead of `Optional[str]`)
  - Enhanced return type precision: `list[str]`, `dict[str, any]`, `inspect.Signature`
  - Improved IDE support and static analysis compatibility

- **JSON Utils (`json_encoding_operations.py`, `json_obj_handler.py`)**:
  - Update all function signatures with comprehensive type annotations
  - Modern parameter types: `dict | list | any`, `str | None`, `callable | None`
  - Enhanced return type specifications: `dict | list`, `str | None`, `bytes | any`

- **Pandas Utils**:
  - **`pandas_obj_handler.py`**: Replace old `Union[]` syntax with modern PEP-604 alternatives
    - `Union[str, List[str], None]` → `str | list[str] | None`
    - `Union[pd.DataFrame, Dict[str, pd.DataFrame], List[pd.DataFrame]]` → `pd.DataFrame | dict[str, pd.DataFrame] | list[pd.DataFrame]`
    - Update all function signatures with comprehensive type annotations
  - **`data_manipulation.py`**: Complete type annotation coverage for all functions
    - Enhanced parameter types: `pd.DataFrame`, `str | list`, `callable | None`
    - Precise return types: `pd.DataFrame`, `None` for in-place operations
  - **`conversions.py`**: Add missing type annotations with PEP-604 syntax

#### **File Operations** (changing; 3.10.0)

- Modules `path_utils.py`, `permission_manager.py`, `bulk_rename_auto.py`, `bulk_rename_manual.py`, and `cat_file_content.py`:
  - Modernise all function signatures to use PEP-604 union syntax (`|`) instead of legacy "or" notation
  - Replace docstring type annotations from `"str or list"` to `"str | list"` format
  - Update return type annotations from generic `"list"` to specific `"list[str]"`, `"list[Path]"`, etc.
  - Enhanced type precision for better IDE support, static analysis, and code clarity

- Module `path_utils.py`:
  - Updated all helper functions with comprehensive type annotations:
    - `_unique_sorted`, `_compile_pattern`, `_match_glob`, `_fetch_path_items`
    - `_add_glob_left`, `_add_glob_right`, `_add_glob_both`, `_whole_word`
  - Improved pattern modifier functions to return lists instead of generators for better consistency
  - Enhanced main functions: `find_files`, `find_dirs_with_files`, `find_items`

- Module `permission_manager.py`:
  - Updated functions with comprehensive type annotations: `modify_obj_permissions`, `modify_obj_owner`
  - Enhanced parameter validation and error handling with proper type specifications

- Module `bulk_rename_auto.py`:
  - Updated all functions with modern type annotations:
    - `shorten_conflicting_obj_list`, `loop_renamer`, `loop_direct_renamer`
    - `return_report_file_fixed_path`, `reorder_objs`
  - Added comprehensive parameter and return type specifications

- Module `bulk_rename_manual.py`:
  - Updated all functions with modern type annotations:
    - `change_to_path_and_store`, `get_current_path`, `get_obj_list`, `print_format_string`
  - Enhanced return type precision with union types where applicable
  - Fixed variable name references to match constants

- Module `cat_file_content.py`:
  - Updated `cat` function with modern type annotations supporting both `str` and `Path` inputs
  - Added `Path` import for proper type support
  - Improved documentation with accurate return type description

### Fixed (3.10.0)

#### **Documentation and Consistency** (fixing; 3.10.0)

- **Format Converters**: Corrected parameter name mismatches in docstrings (`src_path` → `search_path`)
- **General**: Enhanced docstring formatting and parameter descriptions across all modules
- **Pandas Utils**: Improved parameter documentation for complex type signatures
- **JSON Utils**: Standardised return type documentation and error handling descriptions

#### **File Operations** (fixing; 3.10.0)

- Module `permission_manager.py`:
  - Fixed `os.path.isdir` call that was missing the required path parameter
  - Corrected `print_format_string` usage to use proper string formatting with placeholders
  - Improved error handling and validation in permission modification functions

- Module `bulk_rename_manual.py`:
  - Fixed variable name references to use proper constant names (`OBJECT_LISTING_DICT`, `OBJ_TYPE_LIST`)
  - Corrected docstring formatting to use consistent parameter section headers

---

## [3.9.3] - 2025-05-20

### Added (3.9.3)

#### **Pandas Utils** (adding; 3.9.3)

- Module `pandas_obj_handler.py`:
  - Enhance `standardise_time_series` function with option to return separate DataFrames instead of a merged DataFrame
  - Add index handling options for separate DataFrames:
    - `reset_index` parameter to convert datetime index to column
    - `drop` parameter to remove index column completely
    - `names` parameter to customise index column names (single name or list of different names)
  - Add validation for parameter combinations with clear error messages
  - Refactor internal logic into `_standardise_time_series_core` helper function

---

## [3.9.2] - 2025-05-15

### Changed (3.9.2)

#### **Pandas Utils** (changing; 3.9.2)

- Module `pandas_obj_handler.py`:
  - Enhanced `read_table` function with two additional parameters:
    - Added `names` parameter to allow specifying custom column names
    - Added `parse_dates` parameter to enable automatic date parsing
  - Updated function documentation with detailed parameter descriptions
  - Updated function implementation to pass new parameters to pandas

---

## [3.9.1] - 2025-05-10

### Added (3.9.1)

#### **Pandas Utils** (adding; 3.9.1)

- Module `pandas_obj_handler.py`:
  - Add new `standardise_time_series` function to combine multiple time series DataFrames with different date columns into a single DataFrame with a common date index
  - Function automatically handles duplicate column names by adding numerical suffixes
  - Includes comprehensive type hints and documentation

### Changed (3.9.1)

#### **Pandas Utils** (changing; 3.9.1)

- Module `pandas_obj_handler.py`:
  - Give accessibility to undefined parameters and change visibility to the auxiliary function `_concat_dfs_aux`.

---

## [3.9.0] - 2025-05-09

### Fixed (3.9.0)

#### **File Operations** (fixing; 3.9.0)

- Modules `ops_handler.py`, `pdf_tools.py` and `conversions.py` (sub-package `xarray_utils`):
  - Improved system command execution to properly handle cases where command output isn't captured.

---

## [3.8.4] - 2025-05-07

### Changed (3.8.4)

#### **File Operations** (changing; 3.8.4)

- Module `path_utils.py`:
  - Added pattern compilation with LRU cache for faster glob matching
  - Consolidated glob pattern matching into a single optimised function
  - Added case sensitivity option to all matching functions
  - Implement array uniqueness calculation with with Python's built-in set, instead of `np.unique`.

- Module `file_utils.py`:
  - Implement array uniqueness calculation with with Python's built-in set, instead of `np.unique`.

---

## [3.8.3] - 2025-05-05

### Fixed (3.8.3)

#### **Xarray Utils** (fixing; 3.8.3)

- Module `file_utils.py`:
  - Resolved circular import issue by implementing lazy import of `CLIMATE_FILE_EXTENSIONS` from `paramlib.global_parameters`

---

## [3.8.2] - 2025-05-02

### Changed (3.8.2)

#### **General** (changing; 3.8.2)

- Replace the deprecated `find_time_key` function with the new `find_dt_key` function in the following modules:
  - `xarray_utils/data_manipulation.py`
  - `xarray_utils/xarray_obj_handler.py`

---

## [3.8.1] - 2025-04-27

### Changed (3.8.1)

#### **General** (changing; 3.8.1)

- Modify the comment header `Import custom modules` to `Import project modules` in all modules having it.
- Modify the constant `splitdelim` to `SPLIT_DELIM` in all modules having it.

#### **File Operations** (changing; 3.8.1)

- Modules `bulk_rename_auto.py` and `bulk_rename_manual.py`:
  - Convert all **constant names** under the header `Define parameters` to uppercase following Python naming conventions.

#### **Scripts** (changing; 3.8.1)

- Convert all **constant names** under the header `Define parameters` to uppercase in the following files:
  - `copy_compress.py`
  - `msg2pdf_exec.py`
  - `eml2pdf_exec.py`
  - `tweak_pdf.py`
  - `compress_pdf.py`
  - `modify_properties.py`
  - `bulk_rename.py`

- Module `copy_compress.py`: reorganise imports to be more direct, instead of using aliases.

---

## [3.8.0] - 2025-04-25

### Changed (3.8.0)

#### **File Operations** (changing; 3.8.0)

- Modules `permission_manager.py`, `bulk_rename_auto.py`, `path_utils.py`, `ops_handler.py`:
  - Convert all configuration constants to uppercase
  - Update all references to these constants throughout the code
  - Reorganise imports to be more direct by removing unnecessary aliases
  - Sort standard library imports according to PEP 8 guidelines
  - For `bulk_rename_auto.py`, toggle uppercase all constants imported from `global_parameters.py` in `paramlib`

#### **Pandas Utils** (changing; 3.8.0)

- Module `pandas_obj_handler.py`:
  - Convert all configuration constants to uppercase
  - Update all references to these constants throughout the code

#### **Format Converters** (changing; 3.8.0)

- Module `pdf_tools.py`:
  - Convert all configuration constants to uppercase
  - Toggle uppercase all constants imported from `global_parameters.py` in `paramlib`
  - Update all references to these constants throughout the code
  - Reorganise imports to be more direct by removing unnecessary aliases

#### **JSON Utils** (changing; 3.8.0)

- Module `json_obj_handler.py`:
  - Convert all configuration constants to uppercase
  - Toggle uppercase all constants imported from `global_parameters.py` in `paramlib`
  - Update all references to these constants throughout the code

#### **Xarray Utils** (changing; 3.8.0)

- Modules `conversions.py`, `data_manipulation.py`, `file_utils.py`, `patterns.py`, `xarray_obj_handler.py`:
  - Convert all configuration constants to uppercase
  - Toggle uppercase all constants imported from `global_parameters.py` in `paramlib`
  - Update all references to these constants throughout the code
  - Sort and reorganise imports to be more direct by removing unnecessary aliases

---

## [3.7.0] - 2025-04-23

### Changed (3.7.0)

#### **General** (changing; 3.7.0)

- Refactored package import structure:
  - Replace direct imports with `__all__` definitions in package initiator files:
    - `filewise/__init__.py`
    - `filewise/file_operations/__init__.py`
    - `filewise/format_converters/__init__.py`
    - `filewise/general/__init__.py`
    - `filewise/json_utils/__init__.py`
    - `filewise/pandas_utils/__init__.py`
    - `filewise/scripts/__init__.py`
    - `filewise/xarray_utils/__init__.py`
  - Improved control over exported symbols when using 'from package import *'
  - Maintained consistent public API while following Python best practices

### Fixed (3.7.0)

#### **Pandas Utils** (fixing; 3.7.0)

- Module `bulk_rename_auto`:
  - Replace wrong package import for `select_elements` function.

- Module `data_manipulation.py`:
  - Remove the function `polish_df_column_names`
  - Function moved to `pandas_obj_handler.py` where it´s more logically placed
  - Cleaned up the function `insert_column_in_df`, eliminating unnecessarily lengthening code

- Module `pandas_obj_handler.py`:
  - Add the function `polish_df_column_names` originally from `data_manipulation` in the package
  - Remove the redundant import of that function

#### **Xarray Utils** (fixing; 3.7.0)

- Module `file_utils.py`:
  - Correct the import paths of the modules `text_formatters` and `string_handler`
  - Allow the function `ncfile_integrity_status` to return the dataset if the file is successfully opened

- Module `patterns.py`:
  - Correct the function name `check_ncfile_integrity`to `ncfile_integrity_status` from the path `filewise.xarray_utils.file_utils`

- Module `conversions.py`:
  - Correct the path for the function `flatten_to_string`
  - Move the aliased functions into a single import
  - Remove the aliases themselves

- Module `xarray_obj_handler.py`:
  - Correct the path for the functions `append_ext` and `get_obj_specs`
  - Add the import of the function `find_time_key`, the newer and equivalent function to `find_time_dimension`
  - Remove the no longer existing function `find_time_dimension`, as `find_time_key` already supports all top-level xarray objects:
    - xarray.Dataset
    - xarray.DataArray

- Module `data_manipulation.py`:
  - Remove unused functions from the module `ops_handler.py`; conserve only `move_files`.
  - Refactor function aliasing.

---

## [3.6.1] - 2025-04-15

### Fixed (3.6.1)

#### **Pandas Utils** (fixing; 3.6.1)

- Module `pandas_obj_handler`:
  - Corrected import paths for the `filewise` package
  - Updated import statements to use correct package paths
  - Maintained consistent import structure across the module

---

## [3.6.0] - 2025-04-05

### Changed (3.6.0)

#### **General** (changing; 3.6.0)

- Improved variable naming conventions across multiple modules for better clarity and consistency:
  - Renamed variables with "_command" suffix to use "template" suffix where they represent formatteable strings
  - Renamed generic "command" variables to more specific names that better describe their purpose

#### **Pandas Utils** (changing; 3.6.0)

- Module `pandas_obj_handler`:
  - Improved variable naming conventions across multiple modules for better clarity and consistency
  - Replaced abbreviative variable names with more descriptive ones:
    - `lne` → `extension_length`
    - `lifn` → `input_file_count`
    - `ldsid` → `duplicate_sheet_count`
    - `lifdnu` → `unique_row_count`

#### **File Operations** (changing; 3.6.0)

- Modules `bulk_rename_auto` and `bulk_rename_manual`: renamed all `arg_tuple_*` variables to `format_args_*` for clarity and consistency
- Module `file_utils`: renamed `arg_tuple_scanf` to `format_args_scan_progress` and `scandir_arg_tuple` to `format_args_dir_info`

#### **Format Converters** (changing; 3.6.0)

- Module `pdf_tools`:
  - Renamed `pdfunite_command_prefmt` to `pdfunite_template`
  - Renamed generic `command` variables to specific templates:
    - `pdftk_template` for PDF page manipulation
    - `ps2pdf_template` for PDF compression
    - `email_converter_template` for email conversion
    - `msg_converter_template` for MSG file conversion
    - `dpkg_check_template` for program installation checks

#### **Xarray Utils** (changing; 3.6.0)

- Module `conversions`: renamed `grib2nc_syntax` to `grib2nc_template`
- Module `file_utils`: renamed `arg_tuple_scanf` to `format_args_scan_progress` and `scandir_arg_tuple` to `format_args_dir_info`

---

## [3.5.4] - 2025-02-18

### Changed (3.5.4)

#### **General** (changing; 3.5.4)

- In all relevant modules, replace `method` with `function` to accurately refer to the code block that contains the function definition, where no object is instantiated.
- In module `introspection_utils`, rename constant `func_name_libs` to `NAME_RESOLUTION_LIBRARIES` to improve clarity and reflect its purpose of listing supported libraries for function name retrieval.

---

## [3.5.0] - 2024-11-18

### Changed (3.5.0)

#### **JSON Utils** (changing; 3.5.0)

- Module `json_obj_handler`: enhanced JSON serialisation functions to support dictionaries and lists of dictionaries; improved naming and documentation for clarity.

- The following method renamings have been made:

| Old function name | New function name |
|:-----------------:|:-----------------:|
| `serialise_dict_to_json` | `serialise_to_json` |
| `serialise_json_to_dict` | `deserialise_json` |
| `serialise_json_to_df` | `deserialise_json_to_df` |

---

## [3.4.2] - 2024-11-12

### Fixed (3.4.2)

#### **File Operations** (fixing; 3.4.2)

- Module `bulk_rename_auto`: in the import of the module `introspection_utils`, substitute the `get_caller_method_all_args` method name with the actual `get_all_caller_args`.

---

## [3.4.0] - 2024-11-03

### Added (3.4.0)

#### **General** (adding; 3.4.0)

- Added `__init__.py` files to all first-level and deeper sub-packages for enhanced import access

### Changed (3.4.0)

#### **File Operations** (changing; 3.4.0)

- Module `path_utils`: enhanced path retrieval logic with an updated internal helper and improved directory and file search methods.

---

## [3.3.5] - 2024-11-02

### Added (3.3.5)

#### **Scripts** (adding; 3.3.5)

- Add `copy_compress` script for efficient file copying and optional compression.

### Changed (3.3.5)

#### **File Operations** (changing; 3.3.5)

- Module `path_utils`:
  - Enhanced `find_files` and `find_dirs_with_files` with new `match_type` options for flexible pattern matching.
  - Removed redundant methods and improved modularity with internal helper functions.
  - Added `dirs_to_exclude` argument to `find_files`, `find_dirs_with_files`, and `find_items` functions for selective directory exclusion during searches.

---

## [3.0.0] - 2024-11-01

### Changed (3.0.0)

#### **General** (changing; 3.0.0)

- For all files contained in this package, package names in the absolute imports have been relocated

---

## [2.1.0] - Initial Release - 2024-10-28

### Added (2.1.0)

#### **General** (adding; 2.1.0)

- **File Operations** tools for bulk renaming, copying, moving, and managing file permissions
- **format_converters**: conversion tools for PDF and NetCDF file formats
- **data utilities**:
  - JSON utilities for encoding and handling JSON objects
  - pandas utilities for data manipulation and conversions
  - xarray utilities for handling NetCDF data and patterns
- **scripts**: automation scripts for various file-related tasks
