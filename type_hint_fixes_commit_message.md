Standardise type hints for Python 3.10+ "|" operator compliance

- Fix inconsistent docstring capitalisation (`List/Tuple` → `list/tuple`)
- Replace lowercase `any` with `Any` from typing module (4 files)
- Replace lowercase `callable` with `Callable` from typing module (3 files)  
- Remove syntax errors from extra parentheses in `flatten_list` function calls
- Add missing typing imports (`Any`, `Callable`) where needed
- Ensure built-in types use lowercase, typing imports use uppercase

Files modified:

- `pandas_utils/pandas_obj_handler.py`
- `general/introspection_utils.py`  
- `json_utils/json_encoding_operations.py`
- `json_utils/json_obj_handler.py`
- `xarray_utils/xarray_obj_handler.py`
- `pandas_utils/data_manipulation.py`
- `file_operations/path_utils.py`

Resolves type hinting inconsistencies and improves IDE support.