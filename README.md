## pyfdt : Python Flattened Device Tree Manipulation ##
----------
The pyfdt library is aimed to facilitate manipulation of the device tree in ordre to parse it and output in various formats.

Device Tree Blob (.dtb) input is actually the only input format accepted, but either DTB or Device Tree Structure (text .dts) is available.

The libraries is aimed to add the following features :

 - Node manipulation (list, delete attributes)
 - Attributes manipulation
 - Tree walkthrought
 - Device Tree path resolution

No DTS parser/compiler is event considered since "dtc" is the official compiler, but i'm open to any compiler implementation over pyftd...

Typical usage is :

    from pyfdt import FdtBlobParse
    with open("myfdt.dtb") as infile:
	    dtb = FdtBlobParse(infile)
	print dtb.to_fdt().to_dts()

Will open a binary DTB and output an human readable DTS structure.
