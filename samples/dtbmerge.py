#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
DTB merge : merge dtb2 into db1, replace properties of dtb1 with properties of dtb2

@author: Neil 'superna' Armstrong <superna9999@gmail.com>
"""

import argparse
from pyfdt.pyfdt import FdtBlobParse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Device Tree Blob merge')
    parser.add_argument('in_dtb1', help="input filename 1")
    parser.add_argument('in_dtb2', help="input filename 2")
    parser.add_argument('out_filename', help="input filename")
    args = parser.parse_args()

    with open(args.in_dtb1) as infile:
        dtb1 = FdtBlobParse(infile)
    with open(args.in_dtb2) as infile:
        dtb2 = FdtBlobParse(infile)
    
    fdt1 = dtb1.to_fdt()
    fdt2 = dtb2.to_fdt()
    
    fdt1.get_rootnode().merge(fdt2.get_rootnode())

    with open(args.out_filename, "wb") as outfile:
        outfile.write(fdt1.to_dtb())
