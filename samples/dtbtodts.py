#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
DTB to DTS

@author: Neil 'superna' Armstrong <superna9999@gmail.com>
"""

import argparse
from pyfdt import FdtBlobParse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Device Tree Blob dump')
    parser.add_argument('in_filename', help="input filename")
    args = parser.parse_args()

    with open(args.in_filename) as infile:
        dtb = FdtBlobParse(infile)
    
    fdt = dtb.to_fdt()
    
    print fdt.to_dts()
