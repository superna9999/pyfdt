## pyfdt : Python Flattened Device Tree Manipulation ##
----------
The pyfdt library is aimed to facilitate manipulation of the flattened device tree in order to parse it and generate output in various formats.

It is highly based on fdtdump for the dtc compiler package.

Device Tree Blob (.dtb) input is actually the only input format accepted, but either Device Tree Blob (DTB) or Device Tree Structure (text DTS) is available as output format.
Device Tree filesystem 'output' is available via the fusemount.py FUSE sample using [fusepy](https://github.com/terencehonles/fusepy) library.

The library future is to add the following features :

 - Node manipulation (list, delete attributes)
 - Attributes manipulation

No DTS parser/compiler is event considered since "dtc" is the official compiler, but i'm open to any compiler implementation over pyfdt...

Typical usage is :

    from pyfdt import FdtBlobParse
    with open("myfdt.dtb") as infile:
	    dtb = FdtBlobParse(infile)
	print dtb.to_fdt().to_dts()

Will open a binary DTB and output an human readable DTS structure.

The samples directory shows how to :
 - checkpath.py : resolve a FDT path to get a node object
 - dtbtodts.py : how to convert from DTB to DTS
 - fusemount.py : how to mount the DTB into a Device Tree filesystem you can recompile using dtc
 - python-generate.py : generate a FDT in 100% python and generate a DTS from it
 - walktree.py : List all paths of the device tree

[Device Tree Wiki](http://www.devicetree.org)
[Device Tree Compiler](http://www.devicetree.org/Device_Tree_Compiler)

[![Build Status](https://travis-ci.org/superna9999/pyfdt.svg?branch=master)](https://travis-ci.org/superna9999/pyfdt)
