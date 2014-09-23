#!/usr/bin/env python

from pyfdt import *
import argparse

def fdtgetpath(fdt, path):
    if not path.startswith('/'):
        return None
    cur = fdt.get_rootnode()
    if path == "/":
        return cur
    subs = path[1:].split("/")
    for sub in subs:
        print "search %s in %s" % (sub, cur.get_name())
        found = False
        if not isinstance(cur, pyfdt.FdtNode):
            return None
        for node in cur:
            print "%s : %s" % (node.get_name(), node)
            if sub == node.get_name():
                cur = node
                found = True
                break
        if not found:
            return None
    return cur

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Device Tree Blob FUSE mount')
    parser.add_argument('filename', help="input dtb filename")
    parser.add_argument('path', help="fdt path")
    args = parser.parse_args()

    with open(args.filename) as infile:
        dtb = pyfdt.FdtBlobParse(infile)

    fdt = dtb.to_fdt()

    print fdtgetpath(fdt, args.path)
