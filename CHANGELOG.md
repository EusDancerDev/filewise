# filewise changelog

All notable changes to this project will be documented in this file.

---

## [v3.5.4] - 2025-02-18

### Changed

**General**

- In all relevant modules, replace `method` with `function` to accurately refer to the code block that contains the function definition, where no object is instantiated.
- In module `introspection_utils`, rename constant `func_name_libs` to `NAME_RESOLUTION_LIBRARIES` to improve clarity and reflect its purpose of listing supported libraries for function name retrieval.

---

## [v3.5.0] - 2024-11-18

### Changed

**JSON utils**

- Module `json_obj_handler`: enhanced JSON serialization functions to support dictionaries and lists of dictionaries; improved naming and documentation for clarity.
- The following method renamings have been made:
<table>
	<thead>
		<tr>
			<th>Old function name</span></th>
			<th>New function name</span></th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>serialise_dict_to_json</td>
			<td>serialise_to_json</td>
		</tr>
		<tr>
			<td>serialise_json_to_dict</td>
			<td>deserialise_json</td>
		</tr>
		<tr>
			<td>serialise_json_to_df</td>
			<td>deserialise_json_to_df</td>
		</tr>
	</tbody>
</table>

---

## [v3.4.2] - 2024-11-12 

### Changed

**File Operations**
- Module `bulk_rename_auto`: in the import of the module `introspection_utils`, substitute the `get_caller_method_all_args` method name with the actual `get_all_caller_args`.

---

## [v3.4.0] - 2024-11-03

### Added

- Added `__init__.py` files to all first-level and deeper sub-packages for enhanced import access

### Changed

**File Operations**
- Module `path_utils`: enhanced path retrieval logic with an updated internal helper and improved directory and file search methods.

---

## [v3.3.5] - 2024-11-02 

### Changed

**File Operations**
- Module `path_utils`:
	- Enhanced `find_files` and `find_dirs_with_files` with new `match_type` options for flexible pattern matching.
	- Removed redundant methods and improved modularity with internal helper functions.
	- Added `dirs_to_exclude` argument to `find_files`, `find_dirs_with_files`, and `find_items` functions for selective directory exclusion during searches.

**scripts**
- Add `copy_compress` script for efficient file copying and optional compression.

---

## [v3.0.0] - 2024-11-01

### Changed
- For all files contained in this package, package names in the absolute imports have been relocated

---

## [2.1.0] - Initial Release - 2024-10-28

### Added
- **File Operations** tools for bulk renaming, copying, moving, and managing file permissions
- **format_converters**: conversion tools for PDF and NetCDF file formats
- **data utilities**:
	- JSON utilities for encoding and handling JSON objects
	- pandas utilities for data manipulation and conversions
	- xarray utilities for handling NetCDF data and patterns
- **scripts**: automation scripts for various file-related tasks
