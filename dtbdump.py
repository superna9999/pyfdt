#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Python DTB dumper

@author: Neil 'superna' Armstrong <superna9999@gmail.com>
"""

import argparse
from pyfdt.pyfdt import FdtBlobParse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Device Tree Blob dump')
    parser.add_argument('--format', dest = 'format' ,help="output format (dts, json or dtb), default to dts", default = "dts")
    parser.add_argument('in_filename', help="input filename")
    parser.add_argument('out_filename', help="output filename")
    args = parser.parse_args()

    if args.format not in ('dts', 'json', 'dtb'):
        raise Exception('Invalid Output Format')
    
    with open(args.in_filename, 'rb') as infile:
        dtb = FdtBlobParse(infile)
    
    fdt = dtb.to_fdt()
    
    if args.format == "dts":
        with open(args.out_filename, 'wb') as outfile:
            outfile.write(fdt.to_dts().encode('ascii'))
    elif args.format == "dtb":
        with open(args.out_filename, 'wb') as outfile:
            outfile.write(fdt.to_dtb())
    elif args.format == "json":
        with open(args.out_filename, 'wb') as outfile:
            outfile.write(fdt.to_json().encode('ascii'))
