#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
FS to DTB

@author: Neil 'superna' Armstrong <superna9999@gmail.com>
"""

import argparse
from pyfdt.pyfdt import *

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='FS to Device Tree Blob')
    parser.add_argument('path', help="filesystem path")
    parser.add_argument('out_filename', help="output filename")
    args = parser.parse_args()

    with open(args.out_filename, "wb") as outfile:
        fdt = FdtFsParse(args.path)
        outfile.write(fdt.to_dtb())
