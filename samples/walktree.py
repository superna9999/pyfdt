#!/usr/bin/env python

from pyfdt.pyfdt import *
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Device Tree Blob Dump PATHS')
    parser.add_argument('filename', help="input dtb filename")
    args = parser.parse_args()

    with open(args.filename) as infile:
        dtb = FdtBlobParse(infile)

    fdt = dtb.to_fdt()

    for (path, node) in fdt.resolve_path('/').walk():
        print path
