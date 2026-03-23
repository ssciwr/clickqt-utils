# PathWithExtensions Example

This example shows how to use `clickqt_utils.PathWithExtensions` in a `click` CLI and render it as a GUI with `clickqt`.

## Prerequisites

From the `clickqt-utils` repository root, install this package and `clickqt`:

```bash
python -m pip install .
python -m pip install clickqt
```

## Run

From the `example/pathwithextensions` directory:

CLI:

```bash
python app.py --help
```

GUI:

```bash
clickqtfy app.py cli
```

CLI example invocation:

```bash
python app.py --input ./sample.txt
```

The GUI file browser will show extension-aware filters based on the grouped `file_extensions` configuration.
