# filewise changelog

All notable changes to this project will be documented in this file.

---

## [v3.6.1] - 2025-04-06

### Fixed

#### **Pandas Utils**

- Module `pandas_obj_handler`:
  - Corrected import paths for the `filewise` package
  - Updated import statements to use correct package paths
  - Maintained consistent import structure across the module

---

## [v3.6.0] - 2025-04-05

### Changed

#### **General**

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

#### **File Operations**

- Modules `bulk_rename_auto` and `bulk_rename_manual`: renamed all `arg_tuple_*` variables to `format_args_*` for clarity and consistency
- Module `file_utils`: renamed `arg_tuple_scanf` to `format_args_scan_progress` and `scandir_arg_tuple` to `format_args_dir_info`

#### **Format Converters**

- Module `pdf_tools`:
  - Renamed `pdfunite_command_prefmt` to `pdfunite_template`
  - Renamed generic `command` variables to specific templates:
    - `pdftk_template` for PDF page manipulation
    - `ps2pdf_template` for PDF compression
    - `email_converter_template` for email conversion
    - `msg_converter_template` for MSG file conversion
    - `dpkg_check_template` for program installation checks

#### **Xarray Utils**

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

#### **JSON utils**

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
