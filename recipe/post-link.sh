#!/bin/bash
# Interdependent PyPI packages (aligned with pyproject.toml)
"${PREFIX}/bin/pip" install -v \
  "pygenutils>=17.1.0" \
  "paramlib>=3.5.0"
