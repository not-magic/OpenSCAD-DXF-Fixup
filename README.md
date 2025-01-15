# OpenSCAD-DXF-Fixup

Fixes up DXF exported from OpenSCAD to make it easier to use services like SendCutSend, to allow for hardware insertion and bending.

* Finds circular line groups and replaces them with DXF circles
* Can merge another dxf that contains skinny squares, and will turn them into bend lines. The center of the square on the longest axis is used to place the line.

## Dependencies

* [ezdxf](https://github.com/mozman/ezdxf)
* python3

## Usage

Circle detection:

`python3 fixup_dxf.py your_file_here.dxf`

Adding bend lines:

`python3 fixup_dxf.py your_file_here.dxf your_bend_file_here.dxf`

A converted file will be saved with _fixed appended to the filename, e.g. `your_file_here_fixed.dxf`