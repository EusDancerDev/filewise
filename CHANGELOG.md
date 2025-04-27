# filewise changelog

All notable changes to this project will be documented in this file.

---

## [v3.8.1] - 2025-04-27

### Changed

#### **General**

- Modify the comment header `Import custom modules` to `Import project modules` in all modules having it.

---

## [v3.8.0] - 2025-04-25

### Changed (v3.8.0)

#### **File Operations**

- Modules `permission_manager.py`, `bulk_rename_auto.py`, `path_utils.py`, `ops_handler.py`:
  - Convert all configuration constants to uppercase
  - Update all references to these constants throughout the code
  - Reorganise imports to be more direct by removing unnecessary aliases
  - Sort standard library imports according to PEP 8 guidelines
  - For `bulk_rename_auto.py`, toggle uppercase all constants imported from `global_parameters.py` in `paramlib`

#### **Pandas Utils**

- Module `pandas_obj_handler.py`:
  - Convert all configuration constants to uppercase
  - Update all references to these constants throughout the code

#### **Format Converters**

- Module `pdf_tools.py`:
  - Convert all configuration constants to uppercase
  - Toggle uppercase all constants imported from `global_parameters.py` in `paramlib`
  - Update all references to these constants throughout the code
  - Reorganise imports to be more direct by removing unnecessary aliases

#### **JSON Utils**

- Module `json_obj_handler.py`:
  - Convert all configuration constants to uppercase
  - Toggle uppercase all constants imported from `global_parameters.py` in `paramlib`
  - Update all references to these constants throughout the code

#### **Xarray Utils**

- Modules `conversions.py`, `data_manipulation.py`, `file_utils.py`, `patterns.py`, `xarray_obj_handler.py`:
  - Convert all configuration constants to uppercase
  - Toggle uppercase all constants imported from `global_parameters.py` in `paramlib`
  - Update all references to these constants throughout the code
  - Sort and reorganise imports to be more direct by removing unnecessary aliases

---

## [v3.7.0] - 2025-04-23

### Changed (v3.7.0)

#### **General**

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

#### **Pandas utils**

- Module `bulk_rename_auto`:
  - Replace wrong package import for `select_elements` function.

- Module `data_manipulation.py`:
  - Remove the function `polish_df_column_names`
  - Function moved to `pandas_obj_handler.py` where it´s more logically placed
  - Cleaned up the function `insert_column_in_df`, eliminating unnecessarily lengthening code

- Module `pandas_obj_handler.py`:
  - Add the function `polish_df_column_names` originally from `data_manipulation` in the package
  - Remove the redundant import of that function

#### **Xarray utils** (v3.7.0)

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

## [v3.6.1] - 2025-04-15

### Fixed (v3.6.1)

#### **Pandas Utils** (v3.6.1)

- Module `pandas_obj_handler`:
  - Corrected import paths for the `filewise` package
  - Updated import statements to use correct package paths
  - Maintained consistent import structure across the module

---

## [v3.6.0] - 2025-04-05

### Changed (v3.6.0)

#### **General** (v3.6.0)

- Improved variable naming conventions across multiple modules for better clarity and consistency:
  - Renamed variables with "_command" suffix to use "template" suffix where they represent formatteable strings
  - Renamed generic "command" variables to more specific names that better describe their purpose

#### **Pandas Utils** (v3.6.0)

- Module `pandas_obj_handler`:
  - Improved variable naming conventions across multiple modules for better clarity and consistency
  - Replaced abbreviative variable names with more descriptive ones:
    - `lne` → `extension_length`
    - `lifn` → `input_file_count`
    - `ldsid` → `duplicate_sheet_count`
    - `lifdnu` → `unique_row_count`

#### **File Operations** (v3.6.0)

- Modules `bulk_rename_auto` and `bulk_rename_manual`: renamed all `arg_tuple_*` variables to `format_args_*` for clarity and consistency
- Module `file_utils`: renamed `arg_tuple_scanf` to `format_args_scan_progress` and `scandir_arg_tuple` to `format_args_dir_info`

#### **Format Converters** (v3.6.0)

- Module `pdf_tools`:
  - Renamed `pdfunite_command_prefmt` to `pdfunite_template`
  - Renamed generic `command` variables to specific templates:
    - `pdftk_template` for PDF page manipulation
    - `ps2pdf_template` for PDF compression
    - `email_converter_template` for email conversion
    - `msg_converter_template` for MSG file conversion
    - `dpkg_check_template` for program installation checks

#### **Xarray Utils** (v3.6.0)

- Module `conversions`: renamed `grib2nc_syntax` to `grib2nc_template`
- Module `file_utils`: renamed `arg_tuple_scanf` to `format_args_scan_progress` and `scandir_arg_tuple` to `format_args_dir_info`

---

## [v3.5.4] - 2025-02-18

### Changed (v3.5.4)

#### **General** (v3.5.4)

- In all relevant modules, replace `method` with `function` to accurately refer to the code block that contains the function definition, where no object is instantiated.
- In module `introspection_utils`, rename constant `func_name_libs` to `NAME_RESOLUTION_LIBRARIES` to improve clarity and reflect its purpose of listing supported libraries for function name retrieval.

---

## [v3.5.0] - 2024-11-18

### Changed (v3.5.0)

#### **JSON utils** (v3.5.0)

- Module `json_obj_handler`: enhanced JSON serialization functions to support dictionaries and lists of dictionaries; improved naming and documentation for clarity.

- The following method renamings have been made:

| Old function name | New function name |
|------------------|-------------------|
| serialise_dict_to_json | serialise_to_json |
| serialise_json_to_dict | deserialise_json |
| serialise_json_to_df | deserialise_json_to_df |

---

## [v3.4.2] - 2024-11-12

### Changed (v3.4.2)

#### **File Operations** (v3.4.2)

- Module `bulk_rename_auto`: in the import of the module `introspection_utils`, substitute the `get_caller_method_all_args` method name with the actual `get_all_caller_args`.

---

## [v3.4.0] - 2024-11-03

### Added (v3.4.0)

- Added `__init__.py` files to all first-level and deeper sub-packages for enhanced import access

### Changed (v3.4.0)

#### **File Operations** (v3.4.0)

- Module `path_utils`: enhanced path retrieval logic with an updated internal helper and improved directory and file search methods.

---

## [v3.3.5] - 2024-11-02

### Changed (v3.3.5)

#### **File Operations** (v3.3.5)

- Module `path_utils`:
  - Enhanced `find_files` and `find_dirs_with_files` with new `match_type` options for flexible pattern matching.
  - Removed redundant methods and improved modularity with internal helper functions.
  - Added `dirs_to_exclude` argument to `find_files`, `find_dirs_with_files`, and `find_items` functions for selective directory exclusion during searches.

#### **Scripts** (v3.3.5)

- Add `copy_compress` script for efficient file copying and optional compression.

---

## [v3.0.0] - 2024-11-01

### Changed (v3.0.0)

- For all files contained in this package, package names in the absolute imports have been relocated

---

## [2.1.0] - Initial Release - 2024-10-28

### Added (v2.1.0)

- **File Operations** tools for bulk renaming, copying, moving, and managing file permissions
- **format_converters**: conversion tools for PDF and NetCDF file formats
- **data utilities**:
  - JSON utilities for encoding and handling JSON objects
  - pandas utilities for data manipulation and conversions
  - xarray utilities for handling NetCDF data and patterns
- **scripts**: automation scripts for various file-related tasks
