#!/usr/bin/env python
from pyfdt import *
import argparse

def manip_setitem():
    root = pyfdt.FdtNode("/")
    root.add_subnode(FdtPropertyWords("#address-cells", [1]))
    root[0] = FdtPropertyWords("#address-cells", [1])

    fdt = pyfdt.Fdt(version=1, last_comp_version=1)
    fdt.add_rootnode(root)
    return fdt

def manip_bad_setitem():
    root = pyfdt.FdtNode("/")
    root.add_subnode(FdtPropertyWords("#address-cells", [1]))
    root.add_subnode(FdtPropertyWords("test", [2]))
    root[1] = FdtPropertyWords("#address-cells", [1])

    fdt = pyfdt.Fdt(version=1, last_comp_version=1)
    fdt.add_rootnode(root)
    return fdt

def manip_append():
    root = pyfdt.FdtNode("/")
    root.add_subnode(FdtPropertyWords("#address-cells", [1]))
    root.append(FdtPropertyWords("#test", [2]))

    fdt = pyfdt.Fdt(version=1, last_comp_version=1)
    fdt.add_rootnode(root)
    return fdt

def manip_dup_append():
    root = pyfdt.FdtNode("/")
    root.add_subnode(FdtPropertyWords("#address-cells", [1]))
    root.append(FdtPropertyWords("#address-cells", [1]))

    fdt = pyfdt.Fdt(version=1, last_comp_version=1)
    fdt.add_rootnode(root)
    return fdt

def manip_pop():
    root = pyfdt.FdtNode("/")
    root.add_subnode(FdtPropertyWords("#address-cells", [1]))
    root.add_subnode(FdtPropertyWords("#yop", [2]))
    if root.pop().get_name() != "#yop":
        raise Exception("Bad poped subnode")

    fdt = pyfdt.Fdt(version=1, last_comp_version=1)
    fdt.add_rootnode(root)
    return fdt

def manip_empty_pop():
    root = pyfdt.FdtNode("/")
    root.add_subnode(FdtPropertyWords("#address-cells", [1]))
    root.pop()
    root.pop()

    fdt = pyfdt.Fdt(version=1, last_comp_version=1)
    fdt.add_rootnode(root)
    return fdt

def manip_insert():
    root = pyfdt.FdtNode("/")
    root.add_subnode(FdtPropertyWords("#address-cells", [1]))
    root.add_subnode(FdtPropertyWords("abc", [2]))
    root.insert(1, FdtPropertyWords("def", [2]))
    if root[1].get_name() != "def":
        raise Exception("Bad inserted subnode")

    fdt = pyfdt.Fdt(version=1, last_comp_version=1)
    fdt.add_rootnode(root)
    return fdt

def manip_dup_insert():
    root = pyfdt.FdtNode("/")
    root.add_subnode(FdtPropertyWords("#address-cells", [1]))
    root.add_subnode(FdtPropertyWords("abc", [1]))
    root.insert(1, FdtPropertyWords("abc", [1]))

    fdt = pyfdt.Fdt(version=1, last_comp_version=1)
    fdt.add_rootnode(root)
    return fdt

def manip_remove():
    root = pyfdt.FdtNode("/")
    root.add_subnode(FdtPropertyWords("#address-cells", [1]))
    root.add_subnode(FdtPropertyWords("abc", [1]))
    root.remove("abc")
    if len(root) == 2 or root[0].get_name() != "#address-cells":
        raise Exception("subnode bad removed")

    fdt = pyfdt.Fdt(version=1, last_comp_version=1)
    fdt.add_rootnode(root)
    return fdt

def manip_noexist_remove():
    root = pyfdt.FdtNode("/")
    root.add_subnode(FdtPropertyWords("#address-cells", [1]))
    root.remove("abc")

    fdt = pyfdt.Fdt(version=1, last_comp_version=1)
    fdt.add_rootnode(root)
    return fdt

def manip_index():
    root = pyfdt.FdtNode("/")
    root.add_subnode(FdtPropertyWords("#address-cells", [1]))
    root.add_subnode(FdtPropertyWords("abc", [1]))
    if root.index("abc") != 1:
        raise Exception("subnode bad index")

    fdt = pyfdt.Fdt(version=1, last_comp_version=1)
    fdt.add_rootnode(root)
    return fdt

def manip_noexist_index():
    root = pyfdt.FdtNode("/")
    root.add_subnode(FdtPropertyWords("#address-cells", [1]))
    root.index("abc")

    fdt = pyfdt.Fdt(version=1, last_comp_version=1)
    fdt.add_rootnode(root)
    return fdt

def gen_dup():
    root = pyfdt.FdtNode("/")
    root.add_subnode(FdtPropertyWords("#address-cells", [1]))
    root.add_subnode(FdtPropertyWords("#address-cells", [1]))

    fdt = pyfdt.Fdt(version=1, last_comp_version=1)
    fdt.add_rootnode(root)
    return fdt

def gen_nobyte():
    root = pyfdt.FdtNode("/")
    root.add_subnode(FdtPropertyBytes("test", []))

    fdt = pyfdt.Fdt(version=1, last_comp_version=1)
    fdt.add_rootnode(root)
    return fdt

def gen_badbyte():
    root = pyfdt.FdtNode("/")
    root.add_subnode(FdtPropertyBytes("test", [0x1FF]))

    fdt = pyfdt.Fdt(version=1, last_comp_version=1)
    fdt.add_rootnode(root)
    return fdt

def gen_noword():
    root = pyfdt.FdtNode("/")
    root.add_subnode(FdtPropertyWords("#address-cells", []))

    fdt = pyfdt.Fdt(version=1, last_comp_version=1)
    fdt.add_rootnode(root)
    return fdt

def gen_badword():
    root = pyfdt.FdtNode("/")
    root.add_subnode(FdtPropertyWords("#address-cells", [0xFFFFFFFFFFFF]))

    fdt = pyfdt.Fdt(version=1, last_comp_version=1)
    fdt.add_rootnode(root)
    return fdt

def gen_emptystr():
    root = pyfdt.FdtNode("/")
    root.add_subnode(FdtPropertyStrings("model", ["ok", '']))

    fdt = pyfdt.Fdt(version=1, last_comp_version=1)
    fdt.add_rootnode(root)
    return fdt

def gen_badstr():
    root = pyfdt.FdtNode("/")
    root.add_subnode(FdtPropertyStrings("model", ['\xc3\xa9']))

    fdt = pyfdt.Fdt(version=1, last_comp_version=1)
    fdt.add_rootnode(root)
    return fdt

def gen_norootnode():
    fdt = pyfdt.Fdt(version=1, last_comp_version=1)
    return fdt

def gen_v1():
    root = pyfdt.FdtNode("/")

    root.add_subnode(FdtPropertyWords("#address-cells", [1]))
    root.add_subnode(FdtPropertyWords("#size-cells", [1]))
    root.add_subnode(FdtNop())
    root.add_subnode(FdtPropertyStrings("model", ["My Model"]))
    root.add_subnode(FdtNop())
    root.add_subnode(FdtPropertyStrings("compatible", ["my,model"]))

    fdt = pyfdt.Fdt(version=1, last_comp_version=1)
    fdt.add_rootnode(root)
    return fdt

def gen_v2():
    root = pyfdt.FdtNode("/")

    root.add_subnode(FdtPropertyWords("#address-cells", [1]))
    root.add_subnode(FdtPropertyWords("#size-cells", [1]))
    root.add_subnode(FdtNop())
    root.add_subnode(FdtPropertyStrings("model", ["My Model"]))
    root.add_subnode(FdtNop())
    root.add_subnode(FdtPropertyStrings("compatible", ["my,model"]))

    fdt = pyfdt.Fdt(version=2, last_comp_version=2)
    fdt.add_rootnode(root)
    return fdt

def gen_v3():
    root = pyfdt.FdtNode("/")

    root.add_subnode(FdtPropertyWords("#address-cells", [1]))
    root.add_subnode(FdtPropertyWords("#size-cells", [1]))
    root.add_subnode(FdtNop())
    root.add_subnode(FdtPropertyStrings("model", ["My Model"]))
    root.add_subnode(FdtNop())
    root.add_subnode(FdtPropertyStrings("compatible", ["my,model"]))

    fdt = pyfdt.Fdt(version=3, last_comp_version=2)
    fdt.add_rootnode(root)
    return fdt

def gen_basic():
    phandle = 0

    root = pyfdt.FdtNode("/")
    chosen = pyfdt.FdtNode("chosen")
    aliases = pyfdt.FdtNode("aliases")
    memory = pyfdt.FdtNode("memory")
    cpus = pyfdt.FdtNode("cpus")
    clocks = pyfdt.FdtNode("clocks")
    soc = pyfdt.FdtNode("soc")
    soc_intc = pyfdt.FdtNode("interrupt-controller")
    soc_uart = pyfdt.FdtNode("uart@0xF000E000")

    root.add_subnode(FdtPropertyWords("#address-cells", [1]))
    root.add_subnode(FdtPropertyWords("#size-cells", [1]))
    root.add_subnode(FdtPropertyStrings("model", ["My Model"]))
    root.add_subnode(FdtPropertyStrings("compatible", ["my,model"]))

    memory.add_subnode(FdtPropertyStrings("device_type", ["memory"]))
    memory.add_subnode(FdtPropertyWords("reg", [0x00000000, 0x00000000]))

    cpus.add_subnode(FdtPropertyWords("#address-cells", [1]))
    cpus.add_subnode(FdtPropertyWords("#size-cells", [1]))
    cpus.add_subnode(FdtPropertyStrings("device_type", ["cpu"]))
    cpus.add_subnode(FdtPropertyStrings("compatible", ["my,model"]))

    soc_intc.add_subnode(FdtPropertyStrings("compatible", ["my,intc"]))
    soc_intc.add_subnode(FdtPropertyWords("reg", [0xF0001000, 0x4000]))
    soc_intc.add_subnode(FdtPropertyWords("#address-cells", [1]))
    soc_intc.add_subnode(FdtPropertyWords("#size-cells", [1]))
    phandle += 1
    intc_phandle = phandle
    soc_intc.add_subnode(FdtPropertyWords("linux,phandle", [intc_phandle]))
    soc_intc.add_subnode(FdtPropertyWords("phandle", [intc_phandle]))

    soc_uart.add_subnode(FdtPropertyStrings("compatible", ["my,uart"]))
    soc_uart.add_subnode(FdtPropertyWords("reg", [0xF000E000, 0x4000]))
    soc_uart.add_subnode(FdtPropertyBytes("cfg", [0x12, 0x23, -0x64]))
    soc_uart.add_subnode(FdtProperty("no-rts-cts"))

    soc.add_subnode(FdtPropertyStrings("compatible", ["simple-bus"]))
    soc.add_subnode(FdtPropertyWords("#address-cells", [1]))
    soc.add_subnode(FdtPropertyWords("#size-cells", [1]))
    soc_uart.add_subnode(FdtProperty("ranges"))
    soc.add_subnode(FdtPropertyWords("interrupt-parent", [intc_phandle]))

    for subnode in (soc_intc, soc_uart):
        subnode.set_parent_node(subnode)
        soc.add_subnode(subnode)

    for subnode in (chosen, aliases, memory, cpus, clocks, soc):
        subnode.set_parent_node(root)
        root.add_subnode(subnode)
    fdt = pyfdt.Fdt()
    fdt.add_rootnode(root)
    return fdt

def error():
    raise Exception("Test Name Error")

tests = {'basic' : gen_basic, 
         "gen_v1" : gen_v1, 
         "gen_v2" : gen_v2, 
         "gen_v3" : gen_v3,
         "gen_dup" : gen_dup,
         "gen_nobyte" : gen_nobyte,
         "gen_badbyte" : gen_badbyte,
         "gen_noword" : gen_noword,
         "gen_badword" : gen_badword,
         "gen_emptystr" : gen_emptystr,
         "gen_badstr" : gen_badstr,
         "gen_norootnode" : gen_norootnode,
         "manip_setitem": manip_setitem,
         "manip_append": manip_append,
         "manip_pop": manip_pop,
         "manip_insert": manip_insert,
         "manip_remove": manip_remove,
         "manip_index": manip_index,
         "manip_bad_setitem": manip_bad_setitem,
         "manip_dup_append": manip_dup_append,
         "manip_empty_pop": manip_empty_pop,
         "manip_dup_insert": manip_dup_insert,
         "manip_noexist_remove": manip_noexist_remove,
         "manip_noexist_index": manip_noexist_index,
         }

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Device Tree Generator')
    parser.add_argument('name', help="test name")
    args = parser.parse_args()

    fdt = tests.get(args.name, error)()

    with open("out.dts", "wb") as outfile:
        outfile.write(fdt.to_dts())
    with open("out.dtb", "wb") as outfile:
        outfile.write(fdt.to_dtb())
