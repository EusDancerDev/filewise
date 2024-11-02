# filewise changelog

All notable changes to this project will be documented in this file.

## [v3.3.2] - 2024-11-02 

### Changed

**file_operations**
- Module `path_utils`:
	- Enhanced `find_files` and `find_dirs_with_files` with new `match_type` options for flexible pattern matching.
	- Removed redundant methods and improved modularity with internal helper functions.
	- Added `dirs_to_exclude` argument to `find_files`, `find_dirs_with_files`, and `find_items` functions for selective directory exclusion during searches.

---

## [v3.0.0] - 2024-11-01

### Changed
- For all files contained in this package, package names in the absolute imports have been relocated

---

## [2.1.0] - Initial Release - 2024-10-28

### Added
- **file_operations** tools for bulk renaming, copying, moving, and managing file permissions
- **format_converters**: conversion tools for PDF and NetCDF file formats
- **data utilities**:
	- JSON utilities for encoding and handling JSON objects
	- pandas utilities for data manipulation and conversions
	- xarray utilities for handling NetCDF data and patterns
- **scripts**: automation scripts for various file-related tasks
