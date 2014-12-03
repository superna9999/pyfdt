## pyfdt : Installation ##
----------

pyfdt support python 2.6, 27, 3.2, 3.3 and 3.4.

Installation can be done by 
 - using pip ou pypu with the pyfdt package
 - using a git tarball or checkout running setup.py

Examples are provided in the examples directory.

Special 2.6 notes :
 - python-argparse should be installed at least on debian systems

Tests notes :
 - git submodule is needed to checkout dtc into tests directory, on old git version you should run git submodule update
 - dtc needs at least gcc, bison and flex
