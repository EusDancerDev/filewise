# filewise

**filewise*- is a comprehensive Python package designed to simplify file and directory operations, providing a robust set of tools for file management, format conversion, and data handling. It streamlines common file-related tasks with a focus on efficiency, clarity, and maintainability.

## Features

- **File Operations**:
  - Bulk renaming with pattern matching and automatic conflict resolution
  - Efficient file copying, moving, and permission management
  - Advanced directory traversal and file searching capabilities
  - File synchronization with rsync integration

- **Format Converters**:
  - PDF manipulation (merging, splitting, compression)
  - Email format conversion (EML, MSG to PDF)
  - NetCDF and GRIB file handling
  - JSON data serialization and deserialization

- **Data Utilities**:
  - Pandas DataFrame operations and Excel file handling
  - Xarray utilities for scientific data processing
  - JSON object manipulation and conversion
  - Structured data validation and transformation

- **Automation Scripts**:
  - Ready-to-use scripts for common file tasks
  - Batch processing capabilities
  - Customizable workflows for repetitive operations

## Versioning

This package follows [Semantic Versioning](https://semver.org/) (MAJOR.MINOR.PATCH):

- **MAJOR*- version (e.g., 2.x.x to 3.x.x): Incompatible API changes
- **MINOR*- version (e.g., 3.3.x to 3.4.x): New functionality in a backward-compatible manner
- **PATCH*- version (e.g., 3.5.0 to 3.5.4): Backward-compatible bug fixes

For detailed information about changes in each version, please refer to the [CHANGELOG.md](CHANGELOG.md) file.

---

## Installation Guide

### Dependency Notice

Before installing, please ensure the following dependencies are available on your system:

- **Required Third-Party Libraries**: common dependencies include the latest versions of NumPy, Pandas, and others as specified.
  - numpy
  - pandas
  - xarray

  - You can install them via pip:

    ```bash
    pip3 install numpy pandas xarray
    ```

  - Alternatively, you can install them via Anaconda. Currently, the recommended channel from where to install for best practices is `conda-forge`:

    ```bash
    conda install -c conda-forge numpy pandas xarray
    ```

- **Other Internal Packages**: these are other packages created by the same author. To install them as well as the required third-party packages, refer to the README.md document of the corresponding package:
  - filewise
  - paramlib
  - pygenutils

**Note**: In the future, this package will be available via PyPI and Anaconda, where dependencies will be handled automatically.

### Unconventional Installation Instructions

Until this package is available on PyPI or Anaconda, please follow these steps:

1. **Clone the Repository**: Download the repository to your local machine by running:

   ```bash
   git clone https://github.com/EusDancerDev/filewise.git
   ```

2. **Check the Latest Version**: Open the `CHANGELOG.md` file in the repository to see the latest version information.

3. **Build the Package**: Navigate to the repository directory and run:

   ```bash
   python setup.py sdist
   ```

   This will create a `dist/` directory containing the package tarball.

4. **Install the Package**:
   - Navigate to the `dist/` directory.
   - Run the following command to install the package:

     ```bash
     pip3 install filewise-<latest_version>.tar.gz
     ```

     Replace `<latest_version>` with the version number from `CHANGELOG.md`.

**Note**: Once available on PyPI and Anaconda, installation will be simpler and more conventional.

---

### Package Updates

To stay up-to-date with the latest version of this package, follow these steps:

1. **Check the Latest Version**: Open the `CHANGELOG.md` file in this repository to see if a new version has been released.

2. **Pull the Latest Version**:
   - Navigate to the directory where you initially cloned the repository.
   - Run the following command to update your local copy:

     ```bash
     git pull origin main
     ```

3. **Rebuild and Reinstall**: After updating, rebuild and reinstall the package as described in the [Installation Guide](#installation-guide) above.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
