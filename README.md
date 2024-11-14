# filewise

**filewise** is a Python package designed to simplify file and directory operations, providing tools for bulk renaming, copying, moving, permission management, and file format conversions. It includes utilities for handling various data formats, such as JSON, PDF, and NetCDF.

## Features

- **File Operations**:
  - Bulk renaming, copying, moving, and permission management.
- **Format Converters**:
  - Tools for converting file formats, such as PDF and NetCDF.
- **Data Utilities**:
  - Utilities for handling JSON, pandas, and xarray objects.
- **Automation Scripts**:
  - Ready-to-use scripts for common file tasks.

---

## Installation Guide

### Dependency Notice
Before installing, please ensure the following dependencies are available on your system:

- **Required Third-Party Libraries**: common dependencies include the latest versions of NumPy, Pandas, and others as specified.
  * numpy
  * pandas
  * xarray

  - You can install them via pip:
    ```bash
    pip3 install numpy pandas xarray
    ```
    
  - Alternatively, you can install them via Anaconda. Currenlty, the recommended channel from where to install for best practices is `conda-forge`:
    ```bash
    conda install -c conda-forge numpy pandas xarray
    ```

- **Other Internal Packages**: these are other packages created by the same author. To install them as well as the required third-party packages, refer to the README.md document of the corresponding package:
  * filewise
  * paramlib
  * pygenutils

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

This will download the latest changes from the main branch of the repository. After updating, you may need to rebuild and reinstall the package as described in the [Installation Guide](#installation-guide) above.
