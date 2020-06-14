ColX
===========================

A tiny tool for extracting specific columns in an Excel file with tremendous sheets.

## How to run

Install dependencies with
```
pipenv install
```

Run with [fbs](https://build-system.fman.io/)
```
fbs run
```

To build a executable binary file, run
```
fbs freeze
```
and the target file lies at `target` directory.

## Generate .py from .ui

The UI of `ColX` is designed by `Qt Creator`.
You can modify `mainwindow.ui` and generate the relative .py file by
```
pyuic5 mainwindow.ui -o mainwindow.py
```
