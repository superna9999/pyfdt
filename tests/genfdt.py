#!/usr/bin/env python
from pyfdt import *
import argparse

def gen_v1():
    phandle = 0

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
    phandle = 0

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
    phandle = 0

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
    intc_phandle = phandle
    phandle += 1
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

tests = {'basic' : gen_basic, "gen_v1" : gen_v1, "gen_v2" : gen_v2, "gen_v3" : gen_v3}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Device Tree Generator')
    parser.add_argument('name', help="test name")
    args = parser.parse_args()

    fdt = tests.get(args.name, error)()

    with open("out.dts", "wb") as outfile:
        outfile.write(fdt.to_dts())
    with open("out.dtb", "wb") as outfile:
        outfile.write(fdt.to_dtb())
