#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
DTB merge : merge dtb2 into db1, replace properties of dtb1 with properties of dtb2

@author: Neil 'superna' Armstrong <superna9999@gmail.com>
"""

import argparse
from pyfdt.pyfdt import FdtBlobParse, FdtJsonParse, FdtFsParse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Device Tree Blob merge')
    parser.add_argument('--format1', dest = 'format1' ,help="input format1 (dtb, fs or json), default to dtb", default = "dtb")
    parser.add_argument('--format2', dest = 'format2' ,help="input format2 (dtb, fs or json), default to dtb", default = "dtb")
    parser.add_argument('--outformat', dest = 'outformat' ,help="output format (dtb, dts or json), default to dtb", default = "dtb")
    parser.add_argument('in_dtb1', help="input filename 1")
    parser.add_argument('in_dtb2', help="input filename 2")
    parser.add_argument('out_filename', help="output filename")
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
    
    fdt1.get_rootnode().merge(fdt2.get_rootnode())

    if args.outformat == "dts":
        with open(args.out_filename, 'wb') as outfile:
            outfile.write(fdt1.to_dts())
    elif args.outformat == "dtb":
        with open(args.out_filename, 'wb') as outfile:
            outfile.write(fdt1.to_dtb())
    elif args.outformat == "json":
        with open(args.out_filename, 'wb') as outfile:
            outfile.write(fdt1.to_json())
