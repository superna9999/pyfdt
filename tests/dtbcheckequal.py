#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
DTB compare : compare dtb2 and dtb1

@author: Neil 'superna' Armstrong <superna9999@gmail.com>
"""

import argparse
import sys
from pyfdt import FdtBlobParse, FdtJsonParse, FdtFsParse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Device Tree Blob merge')
    parser.add_argument('--format1', dest = 'format1' ,help="input format (dtb, fs or json), default to dtb", default = "dtb")
    parser.add_argument('--format2', dest = 'format2' ,help="input format (dtb, fs or json), default to dtb", default = "dtb")
    parser.add_argument('in_dtb1', help="input filename 1")
    parser.add_argument('in_dtb2', help="input filename 2")
    args = parser.parse_args()

    if args.format1 not in ('fs', 'dtb', 'json'):
        raise Exception('Invalid Format1')
    if args.format2 not in ('fs', 'dtb', 'json'):
        raise Exception('Invalid Format2')

    if args.format1 == 'dtb':
        with open(args.in_dtb1) as infile:
            dtb1 = FdtBlobParse(infile)
        fdt1 = dtb1.to_fdt()
    elif args.format1 == 'json':
        with open(args.in_dtb1) as infile:
            fdt1 = FdtJsonParse(infile.read())
    else:
        fdt1 = FdtFsParse(args.in_dtb1)

    if args.format2 == 'dtb':
        with open(args.in_dtb2) as infile:
            dtb2 = FdtBlobParse(infile)
        fdt2 = dtb2.to_fdt()
    elif args.format2 == 'json':
        with open(args.in_dtb2) as infile:
            fdt2 = FdtJsonParse(infile.read())
    else:
        fdt2 = FdtFsParse(args.in_dtb2)
    
    if fdt1.get_rootnode() == fdt2.get_rootnode():
        sys.exit(0)
    
    sys.exit(1)
