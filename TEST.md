## pyfdt : Test Suite ##
----------

pyfdt has a test suite against dtc testsuite.

To run the testsuite :
 - if the tests/dtc git submodule has not been downloaded, run :

    git submodule init
    git submodule update

 - Install the hexdump, bash, make, flex and bison packages
 - Run the proper testsuite :

    tests/do_tests.bash


The testsuite consist of :
 - Building dtc binaries and tests
 - Run the dtc testsuite
 - Run pyfdt against dtc generated .dtb
 - Generate trees in pure python
 - Manipulates trees in pure python

You whould have 0 failed tests.
