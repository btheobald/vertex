# Project: Vertex #
Computer Apps Group 21 - Electrostatics

## Important Project Notes ##

The structure of the application to follow is as such.

Core functionality and program startup is central to vtx_core.py.

Functions will be added in a modular fashion to files inside the module package, each relating to a specific area of the program to increase the readability and structure of code.

### Modules ###
- vtx_calc - Calculation and simulation.
- vtx_com - Common classes for all modules.
- vtx_draw - Drawing functions for the Tkinter canvas.
- vtx_file - JSON file loading/saving/selection.
- vtx_gui - Graphical User Interface definitions and init.

### Unit Testing ###
If you are writing code, you should be writing unit tests, create your test in a python file with a sensible name inside of tests, preferably with the name of the module being tested and some extra identifier. 

Example: *tests_file_simpleload.py* is used to check that a valid JSON file loads correctly, it imports the vtx_file module and is run as a program as itself in order to run the test. It performs basic checks as to what its result is and the expected result. (provided by the developer.) 

If the test passes it outputs PASS, if it FAILS then still commit your code (and the test.) but note in comments and the commit message that the test fails.

### Avoidance of Cyclic Imports ###
In order to maintain a good structure, the modules should not contain main programs themselves, but instead should pass back any objects likely to be needed to the calling function, which should be vtx_core.

Module files should not import modules other than vtx_com as this contains data structure definitons used throughout the program. This is to help prevent cyclic imports which are considered to be bad practice and lead to difficult to follow code.
