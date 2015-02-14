#!/usr/bin/env python
from pyfdt.pyfdt import *
import argparse

def manip_simple_cmp_tree():
    root = FdtNode("/")
    root.add_subnode(FdtPropertyWords("pwet", [2]))
    root.add_subnode(FdtPropertyWords("#address-cells", [1]))

    root1 = FdtNode("/")
    root1.add_subnode(FdtPropertyWords("#address-cells", [1]))
    root1.add_subnode(FdtPropertyWords("pwet", [2]))

    if root1 != root:
        raise Exception("Tree cmp Failed")

    fdt = Fdt(version=1, last_comp_version=1)
    fdt.add_rootnode(root)
    return fdt

def manip_subtree_cmp_tree():
    root = FdtNode("/")
    root.add_subnode(FdtPropertyStrings("pwet", ["yo"]))
    subnode = FdtNode("abc")
    subnode.add_subnode(FdtProperty("ranges"))
    subnode.add_subnode(FdtPropertyBytes("#address-cells", [0x12, 0x23]))
    subnode.set_parent_node(root)
    root.append(subnode)
    root.add_subnode(FdtPropertyWords("#address-cells", [3]))

    root1 = FdtNode("/")
    root1.add_subnode(FdtPropertyWords("#address-cells", [3]))
    subnode1 = FdtNode("abc")
    subnode1.add_subnode(FdtPropertyBytes("#address-cells", [0x12, 0x23]))
    subnode1.add_subnode(FdtProperty("ranges"))
    subnode1.set_parent_node(root1)
    root1.append(subnode1)
    root1.add_subnode(FdtPropertyStrings("pwet", ["yo"]))

    if root1 != root:
        raise Exception("Tree cmp Failed")

    fdt = Fdt(version=17, last_comp_version=16)
    fdt.add_rootnode(root)
    return fdt

def manip_simple_merge():
    root = FdtNode("/")
    root.add_subnode(FdtPropertyWords("#address-cells", [1]))

    root1 = FdtNode("/")
    root1.add_subnode(FdtPropertyWords("#address-cells", [2]))
    root1.add_subnode(FdtPropertyWords("pwet", [2]))

    root.merge(root1)
    if root[0][0] != 2 or len(root) < 2:
        raise Exception("Merge Failed")

    fdt = Fdt(version=1, last_comp_version=1)
    fdt.add_rootnode(root)
    return fdt

def manip_subtree_merge():
    root = FdtNode("/")
    root.add_subnode(FdtPropertyWords("#address-cells", [1]))
    subnode = FdtNode("abc")
    subnode.add_subnode(FdtPropertyWords("#address-cells", [1]))
    root.append(subnode)

    root1 = FdtNode("/")
    subnode1 = FdtNode("abc")
    subnode1.add_subnode(FdtPropertyWords("#address-cells", [2]))
    subnode1.set_parent_node(root1)
    root1.append(subnode1)
    subnode2 = FdtNode("def")
    subnode2.add_subnode(FdtPropertyWords("#address-cells", [3]))
    subsubnode1 = FdtNode("pwet")
    subsubnode1.add_subnode(FdtPropertyWords("#address-cells", [4]))
    subsubnode1.set_parent_node(subnode2)
    subnode2.append(subsubnode1)
    subnode2.set_parent_node(root1)
    root1.append(subnode2)

    root.merge(root1)

    if root[0][0] != 1 \
       or root[1][0][0] != 2  \
       or len(root) != 3 \
       or id(subnode2.get_parent_node()) != id(root1) \
       or root[2][1].get_name() != "pwet":
        raise Exception("Merge Failed")

    fdt = Fdt(version=1, last_comp_version=1)
    fdt.add_rootnode(root)
    return fdt

def manip_badobj_merge():
    root = FdtNode("/")
    root.add_subnode(FdtPropertyWords("#address-cells", [1]))

    root.merge("str")

    fdt = Fdt(version=1, last_comp_version=1)
    fdt.add_rootnode(root)
    return fdt

def manip_setitem():
    root = FdtNode("/")
    root.add_subnode(FdtPropertyWords("#address-cells", [1]))
    root[0] = FdtPropertyWords("#address-cells", [1])

    fdt = Fdt(version=1, last_comp_version=1)
    fdt.add_rootnode(root)
    return fdt

def manip_badobj_setitem():
    root = FdtNode("/")
    root.add_subnode(FdtPropertyWords("#address-cells", [1]))

    root[0] = "str"

    fdt = Fdt(version=1, last_comp_version=1)
    fdt.add_rootnode(root)
    return fdt

def manip_replace_setitem():
    root = FdtNode("/")
    root.add_subnode(FdtPropertyWords("#address-cells", [1]))
    root.add_subnode(FdtPropertyWords("test", [2]))
    root[1] = FdtPropertyWords("test", [3])

    fdt = Fdt(version=1, last_comp_version=1)
    fdt.add_rootnode(root)
    return fdt

def manip_bad_setitem():
    root = FdtNode("/")
    root.add_subnode(FdtPropertyWords("#address-cells", [1]))
    root.add_subnode(FdtPropertyWords("test", [2]))
    root[1] = FdtPropertyWords("#address-cells", [1])

    fdt = Fdt(version=1, last_comp_version=1)
    fdt.add_rootnode(root)
    return fdt

def manip_append():
    root = FdtNode("/")
    root.add_subnode(FdtPropertyWords("#address-cells", [1]))
    root.append(FdtPropertyWords("#test", [2]))

    fdt = Fdt(version=1, last_comp_version=1)
    fdt.add_rootnode(root)
    return fdt

def manip_dup_append():
    root = FdtNode("/")
    root.add_subnode(FdtPropertyWords("#address-cells", [1]))
    root.append(FdtPropertyWords("#address-cells", [1]))

    fdt = Fdt(version=1, last_comp_version=1)
    fdt.add_rootnode(root)
    return fdt

def manip_badobj_append():
    root = FdtNode("/")
    root.add_subnode(FdtPropertyWords("#address-cells", [1]))

    root.append("str")

    fdt = Fdt(version=1, last_comp_version=1)
    fdt.add_rootnode(root)
    return fdt

def manip_pop():
    root = FdtNode("/")
    root.add_subnode(FdtPropertyWords("#address-cells", [1]))
    root.add_subnode(FdtPropertyWords("#yop", [2]))
    if root.pop().get_name() != "#yop":
        raise Exception("Bad poped subnode")

    fdt = Fdt(version=1, last_comp_version=1)
    fdt.add_rootnode(root)
    return fdt

def manip_empty_pop():
    root = FdtNode("/")
    root.add_subnode(FdtPropertyWords("#address-cells", [1]))
    root.pop()
    root.pop()

    fdt = Fdt(version=1, last_comp_version=1)
    fdt.add_rootnode(root)
    return fdt

def manip_insert():
    root = FdtNode("/")
    root.add_subnode(FdtPropertyWords("#address-cells", [1]))
    root.add_subnode(FdtPropertyWords("abc", [2]))
    root.insert(1, FdtPropertyWords("def", [2]))
    if root[1].get_name() != "def":
        raise Exception("Bad inserted subnode")

    fdt = Fdt(version=1, last_comp_version=1)
    fdt.add_rootnode(root)
    return fdt

def manip_dup_insert():
    root = FdtNode("/")
    root.add_subnode(FdtPropertyWords("#address-cells", [1]))
    root.add_subnode(FdtPropertyWords("abc", [1]))
    root.insert(1, FdtPropertyWords("abc", [1]))

    fdt = Fdt(version=1, last_comp_version=1)
    fdt.add_rootnode(root)
    return fdt

def manip_badobj_insert():
    root = FdtNode("/")
    root.add_subnode(FdtPropertyWords("#address-cells", [1]))

    root.insert(1, "str")

    fdt = Fdt(version=1, last_comp_version=1)
    fdt.add_rootnode(root)
    return fdt

def manip_remove():
    root = FdtNode("/")
    root.add_subnode(FdtPropertyWords("#address-cells", [1]))
    root.add_subnode(FdtPropertyWords("abc", [1]))
    root.remove("abc")
    if len(root) == 2 or root[0].get_name() != "#address-cells":
        raise Exception("subnode bad removed")

    fdt = Fdt(version=1, last_comp_version=1)
    fdt.add_rootnode(root)
    return fdt

def manip_noexist_remove():
    root = FdtNode("/")
    root.add_subnode(FdtPropertyWords("#address-cells", [1]))
    root.remove("abc")

    fdt = Fdt(version=1, last_comp_version=1)
    fdt.add_rootnode(root)
    return fdt

def manip_index():
    root = FdtNode("/")
    root.add_subnode(FdtPropertyWords("#address-cells", [1]))
    root.add_subnode(FdtPropertyWords("abc", [1]))
    if root.index("abc") != 1:
        raise Exception("subnode bad index")

    fdt = Fdt(version=1, last_comp_version=1)
    fdt.add_rootnode(root)
    return fdt

def manip_noexist_index():
    root = FdtNode("/")
    root.add_subnode(FdtPropertyWords("#address-cells", [1]))
    root.index("abc")

    fdt = Fdt(version=1, last_comp_version=1)
    fdt.add_rootnode(root)
    return fdt

def gen_dup():
    root = FdtNode("/")
    root.add_subnode(FdtPropertyWords("#address-cells", [1]))
    root.add_subnode(FdtPropertyWords("#address-cells", [1]))

    fdt = Fdt(version=1, last_comp_version=1)
    fdt.add_rootnode(root)
    return fdt

def gen_nobyte():
    root = FdtNode("/")
    root.add_subnode(FdtPropertyBytes("test", []))

    fdt = Fdt(version=1, last_comp_version=1)
    fdt.add_rootnode(root)
    return fdt

def gen_badbyte():
    root = FdtNode("/")
    root.add_subnode(FdtPropertyBytes("test", [0x1FF]))

    fdt = Fdt(version=1, last_comp_version=1)
    fdt.add_rootnode(root)
    return fdt

def gen_noword():
    root = FdtNode("/")
    root.add_subnode(FdtPropertyWords("#address-cells", []))

    fdt = Fdt(version=1, last_comp_version=1)
    fdt.add_rootnode(root)
    return fdt

def gen_badword():
    root = FdtNode("/")
    root.add_subnode(FdtPropertyWords("#address-cells", [0xFFFFFFFFFFFF]))

    fdt = Fdt(version=1, last_comp_version=1)
    fdt.add_rootnode(root)
    return fdt

def gen_emptystr():
    root = FdtNode("/")
    root.add_subnode(FdtPropertyStrings("model", ["ok", '']))

    fdt = Fdt(version=1, last_comp_version=1)
    fdt.add_rootnode(root)
    return fdt

def gen_badstr():
    root = FdtNode("/")
    root.add_subnode(FdtPropertyStrings("model", ['\xc3\xa9']))

    fdt = Fdt(version=1, last_comp_version=1)
    fdt.add_rootnode(root)
    return fdt

def gen_norootnode():
    fdt = Fdt(version=1, last_comp_version=1)
    return fdt

def gen_v1():
    root = FdtNode("/")

    root.add_subnode(FdtPropertyWords("#address-cells", [1]))
    root.add_subnode(FdtPropertyWords("#size-cells", [1]))
    root.add_subnode(FdtNop())
    root.add_subnode(FdtPropertyStrings("model", ["My Model"]))
    root.add_subnode(FdtNop())
    root.add_subnode(FdtPropertyStrings("compatible", ["my,model"]))

    fdt = Fdt(version=1, last_comp_version=1)
    fdt.add_rootnode(root)
    return fdt

def gen_v2():
    root = FdtNode("/")

    root.add_subnode(FdtPropertyWords("#address-cells", [1]))
    root.add_subnode(FdtPropertyWords("#size-cells", [1]))
    root.add_subnode(FdtNop())
    root.add_subnode(FdtPropertyStrings("model", ["My Model"]))
    root.add_subnode(FdtNop())
    root.add_subnode(FdtPropertyStrings("compatible", ["my,model"]))

    fdt = Fdt(version=2, last_comp_version=2)
    fdt.add_rootnode(root)
    return fdt

def gen_v3():
    root = FdtNode("/")

    root.add_subnode(FdtPropertyWords("#address-cells", [1]))
    root.add_subnode(FdtPropertyWords("#size-cells", [1]))
    root.add_subnode(FdtNop())
    root.add_subnode(FdtPropertyStrings("model", ["My Model"]))
    root.add_subnode(FdtNop())
    root.add_subnode(FdtPropertyStrings("compatible", ["my,model"]))

    fdt = Fdt(version=3, last_comp_version=2)
    fdt.add_rootnode(root)
    return fdt

def gen_basic():
    phandle = 0

    root = FdtNode("/")
    chosen = FdtNode("chosen")
    aliases = FdtNode("aliases")
    memory = FdtNode("memory")
    cpus = FdtNode("cpus")
    clocks = FdtNode("clocks")
    soc = FdtNode("soc")
    soc_intc = FdtNode("interrupt-controller")
    soc_uart = FdtNode("uart@0xF000E000")

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
    fdt = Fdt()
    fdt.add_rootnode(root)
    return fdt

def error():
    raise Exception("Test Name Error")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Device Tree Generator')
    parser.add_argument('name', help="test name")
    args = parser.parse_args()

    fdt = globals().get(args.name, error)()

    with open("out.dts", "w") as outfile:
        outfile.write(fdt.to_dts())
    with open("out.dtb", "wb") as outfile:
        outfile.write(fdt.to_dtb())
