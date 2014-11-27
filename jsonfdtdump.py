#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
JSON to Fdt dumper

See JSONDeviceTree.md for format

@author: Neil 'superna' Armstrong <superna9999@gmail.com>
"""

import argparse
from pyfdt.pyfdt import FdtJsonParse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Device Tree Blob JSON to DTB')
    parser.add_argument('--format', dest = 'format' ,help="output format (dts, dtb or json), default to dts", default = "dts")    
    parser.add_argument('in_filename', help="input filename")
    parser.add_argument('out_filename', help="output filename")
    args = parser.parse_args()

    if args.format not in ('dts', 'dtb', 'json'):
        raise Exception('Invalid Output Format')

    with open(args.in_filename) as infile:
        fdt = FdtJsonParse(infile.read())
    
    if args.format == "dts":
        with open(args.out_filename, 'wb') as outfile:
            outfile.write(fdt.to_dts())
    elif args.format == "dtb":
        with open(args.out_filename, 'wb') as outfile:
            outfile.write(fdt.to_dtb())
    elif args.format == "json":
        with open(args.out_filename, 'wb') as outfile:
            outfile.write(fdt.to_json())
