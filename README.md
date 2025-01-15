# OpenSCAD-DXF-Fixup

Fixes up DXF exported from OpenSCAD to create circle elements from line groups. This is to make it easier to use services like SendCutSend.

## Dependencies

* [ezdxf](https://github.com/mozman/ezdxf)
* python3

## Usage

`python3 fixup_dxf.py your_file_here.dxf`

A converted file will be saved with _fixed appended to the filename, e.g. `your_file_here_fixed.dxf`