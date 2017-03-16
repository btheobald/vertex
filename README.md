# Project: Vertex #
Computer Apps Group 21 - Electrostatics

The structure of the application to follow is as such.

Core functionality and program startup is central to vtx_core.py.

Functions will be added in a modular fashion to files inside the module package, each relating to a specific area of the program to increase the readability and structure of code.

### Modules ###
- vtx_calc - Calculation and simulation.
- vtx_com - Common classes for all modules.
- vtx_draw - Drawing functions for the Tkinter canvas.
- vtx_file - JSON file loading/saving/selection.
- vtx_gui - Graphical User Interface definitions and init.

### Avoidance of Cyclic Imports ###
In order to maintain a good structure, the modules should not contain main programs themselves, but instead should pass back any objects likely to be needed to the calling function, which should be vtx_core.

Module files should not import modules other than vtx_com as this contains data structure definitons used throughout the program. This is to help prevent cyclic imports which are considered to be bad practice and lead to difficult to follow code.
