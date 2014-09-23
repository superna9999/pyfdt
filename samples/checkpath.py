#!/usr/bin/env python

from pyfdt import *
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Device Tree Blob FUSE mount')
    parser.add_argument('filename', help="input dtb filename")
    parser.add_argument('path', help="fdt path")
    args = parser.parse_args()

    with open(args.filename) as infile:
        dtb = pyfdt.FdtBlobParse(infile)

    fdt = dtb.to_fdt()

    node = fdt.resolve_path(args.path)
    if isinstance(node, pyfdt.FdtNode):
        print node
        for subnode in node:
            print '\t%s' % subnode
    else:
        print node
