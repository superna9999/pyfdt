#!/usr/bin/env python
"""
Mount DTB as FUSE mount point
"""
import os
import sys
import errno

from fuse import FUSE, FuseOSError, Operations
from pyfdt import *
from errno import ENOENT
from stat import S_IFDIR, S_IFLNK, S_IFREG
from time import time
import argparse

def fdtgetpath(fdt, path):
    if not path.startswith('/'):
        return None
    cur = fdt.get_rootnode()
    if path == "/":
        return cur
    subs = path[1:].split("/")
    for sub in subs:
        found = False
        if not isinstance(cur, pyfdt.FdtNode):
            return None
        for node in cur:
            if sub == node.get_name():
                cur = node
                found = True
                break
        if not found:
            return None
    return cur

class DtbMount(Operations):

    def __init__(self, fdt):
        self.fdt = fdt
        self.fd = 0

    def getattr(self, path, fh=None):
        node = fdtgetpath(self.fdt, path)
        if isinstance(node, pyfdt.FdtNode):
            return dict(st_mode=(S_IFDIR | 0755), st_ctime=time(), 
                        st_mtime=time(), st_atime=time(), st_nlink=2)
        elif node:
            return dict(st_mode=(S_IFREG | 0755), st_ctime=time(), 
                        st_mtime=time(), st_atime=time(), st_nlink=1, 
                        st_size=len(node.to_raw()))
        return -1

    def readdir(self, path, fh):
        node = fdtgetpath(self.fdt, path)
        if isinstance(node, pyfdt.FdtNode):
            return ['.', '..'] + [subnode.get_name() for subnode in node]
        return -1

    def open(self, path, flags):
        node = fdtgetpath(self.fdt, path)
        if not isinstance(node, pyfdt.FdtNode):
            self.fd += 1
            return self.fd
        return -1

    def read(self, path, length, offset, fh):
        node = fdtgetpath(self.fdt, path)
        if not isinstance(node, pyfdt.FdtNode):
            return node.to_raw()[offset:(length-offset)]
        return -1

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Device Tree Blob FUSE mount')
    parser.add_argument('filename', help="input dtb filename")
    parser.add_argument('mountpoint', help="mount point")
    args = parser.parse_args()

    with open(args.filename) as infile:
        dtb = pyfdt.FdtBlobParse(infile)

    fdt = dtb.to_fdt()

    FUSE(DtbMount(fdt), args.mountpoint, foreground=True)
