# Welcome to clickqt-utils

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/ssciwr/clickqt-utils/ci.yml?branch=main)](https://github.com/ssciwr/clickqt-utils/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/ssciwr/clickqt-utils/branch/main/graph/badge.svg)](https://codecov.io/gh/ssciwr/clickqt-utils)

A collection of `click` utilities that is also understood by `clickqt`.

## Features

Currently, `clickqt-utils` contains the following utilities:

* `PathWithExtensions`: a `click.Path` type that only accepts files with configured extensions.

They are usable with any CLI written in `click`, but they have the advantage
of being directly understood by `clickqt`. Notably, this package does not
depend on `clickqt`, so depending on this will not make you depend on QT,
but your users can opt into using `clickqt` for GUI support of your tools.

## Installation

The Python package `clickqt-utils` can be installed from PyPI:

```
python -m pip install clickqt-utils
```

## Acknowledgments

This repository was set up using the [SSC Cookiecutter for Python Packages](https://github.com/ssciwr/cookiecutter-python-package).
