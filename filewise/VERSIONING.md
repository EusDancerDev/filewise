# Versioning Policy

This document outlines the versioning policy for the **filewise** package, explaining how version numbers are assigned and what they signify.

## Version Number Format

The **filewise** package follows [Semantic Versioning](https://semver.org/) (SemVer) with a version number format of `MAJOR.MINOR.PATCH`:

- **MAJOR** version (e.g., 2.x.x to 3.x.x): Indicates incompatible API changes
- **MINOR** version (e.g., 3.3.x to 3.4.x): Indicates new functionality in a backward-compatible manner
- **PATCH** version (e.g., 3.5.0 to 3.5.4): Indicates backward-compatible bug fixes

## Version Number Guidelines

### MAJOR Version (X.0.0)

- Incremented when making incompatible API changes
- Examples of MAJOR version changes in filewise:
  - v2.1.0 to v3.0.0: Relocation of package names in absolute imports

### MINOR Version (0.X.0)

- Incremented when adding functionality in a backward-compatible manner
- Examples of MINOR version changes in filewise:
  - v3.3.5 to v3.4.0: Added `__init__.py` files to all sub-packages
  - v3.4.0 to v3.5.0: Enhanced JSON serialization functions
  - v3.5.0 to v3.6.0: Improved variable naming conventions

### PATCH Version (0.0.X)

- Incremented when making backward-compatible bug fixes
- Examples of PATCH version changes in filewise:
  - v3.5.0 to v3.5.4: Renamed `func_name_libs` to `NAME_RESOLUTION_LIBRARIES`
  - v3.4.0 to v3.4.2: Fixed import of `get_all_caller_args`

## Version History

The following table provides a summary of the version history for the **filewise** package:

| Version | Date | Description |
|---------|------|-------------|
| v3.6.0 | 2025-04-05 | Improved variable naming conventions across multiple modules |
| v3.5.4 | 2025-02-18 | Replaced `method` with `function` and renamed constants |
| v3.5.0 | 2024-11-18 | Enhanced JSON serialization functions |
| v3.4.2 | 2024-11-12 | Fixed import of `get_all_caller_args` |
| v3.4.0 | 2024-11-03 | Added `__init__.py` files to all sub-packages |
| v3.3.5 | 2024-11-02 | Enhanced path retrieval logic and added `copy_compress` script |
| v3.0.0 | 2024-11-01 | Relocated package names in absolute imports |
| v2.1.0 | 2024-10-28 | Initial release |

## Versioning Process

1. **Version Planning**: Before making significant changes, the version number is determined based on the nature of the changes.
2. **Development**: Changes are made in a development branch.
3. **Testing**: All changes are thoroughly tested to ensure they work as expected.
4. **Documentation**: The CHANGELOG.md file is updated with details about the changes.
5. **Release**: The new version is released and tagged in the repository.

## Version Compatibility

- **Backward Compatibility**: MINOR and PATCH version changes maintain backward compatibility with previous versions.
- **Breaking Changes**: MAJOR version changes may include breaking changes that require updates to existing code.

## Version Information in Code

The current version of the package can be accessed in code using:

```python
import filewise
print(filewise.__version__)
```

## References

- [Semantic Versioning 2.0.0](https://semver.org/)
- [Python Packaging User Guide](https://packaging.python.org/)
