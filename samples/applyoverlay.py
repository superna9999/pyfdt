#!/usr/bin/env python

import argparse
from pyfdt.pyfdt import FdtBlobParse, FdtPropertyWords, FdtPropertyStrings


def read_binary_file(fname):
    with open(fname, "rb") as f:
        dtb = FdtBlobParse(f)
        ftd = dtb.to_fdt()
    return ftd


def get_phandles(ftd):
    phandle_2_node_name = {}

    r = ftd.get_rootnode()
    for name, node in r.walk():
        path = name.split("/")
        pname = "/".join(path[:-1])
        if path[-1] == "phandle":
            phandle_2_node_name[node[0]] = pname

    return phandle_2_node_name


def fixup_overlay(overlay_ftd, main_ftd, main_phandle_2_node_name):
    """
    Follow the recipe in the following web page to prepare an overlay tree for merging
    with a main device tree.
    https://www.kernel.org/doc/html/latest/devicetree/dynamic-resolution-notes.html
    """

    min_phandle = max(main_phandle_2_node_name.keys()) + 1

    # Steps 1 and 2
    r = overlay_ftd.get_rootnode()
    for name, node in r.walk():
        if name.endswith("phandle"):
            assert type(node) is FdtPropertyWords
            node.words[0] += min_phandle

    # Step 3
    local_fixups = overlay_ftd.resolve_path("/__local_fixups__")
    for name, node in local_fixups.walk():
        if type(node) is FdtPropertyWords:
            tgt = overlay_ftd.resolve_path(name)
            assert type(tgt) is FdtPropertyWords
            assert len(node.words) >= 1 and len(tgt.words) >= 1
            phandle_fixup = min_phandle + node[0] + tgt.words[0]
            tgt.words[0] = phandle_fixup

    # Step 4, 5, 6
    fixups = overlay_ftd.resolve_path("/__fixups__")
    for n in fixups.subdata:
        name = n.get_name()
        orig = main_ftd.resolve_path("/__symbols__/{n}".format(n=name))
        assert type(orig) is FdtPropertyStrings
        ph_node = main_ftd.resolve_path(orig.strings[0] + "/phandle")
        ph_int = ph_node.words[0]
        for fix_spec in n.strings:
            path, prop, pos = fix_spec.split(":")
            prop_node = overlay_ftd.resolve_path(path + "/" + prop)
            assert type(prop_node) is FdtPropertyWords
            while len(prop_node.words) <= int(pos):
                prop_node.words.append(0)
            prop_node.words[int(pos)] = ph_int


def apply_fixed_up_overlay(overlay_ftd, main_ftd, main_phandle_2_node_name):
    """
    Merge an overlay tree with the targets in a main device tree.
    """
    ovr_r = overlay_ftd.get_rootnode()

    for frag in ovr_r.subdata:
        fname = frag.get_name()
        if not fname.startswith("fragment@"):
            continue
        target_node = overlay_ftd.resolve_path("/" + fname + "/target")
        assert type(target_node) is FdtPropertyWords
        tgt_path = main_phandle_2_node_name[target_node.words[0]]
        tgt_node = main_ftd.resolve_path(tgt_path)
        ovr_node = overlay_ftd.resolve_path("/{fn}/__overlay__".format(fn=fname))
        tgt_node.merge(ovr_node)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Merge an overlay into a main tree."
    )
    parser.add_argument('dtb_filename', help="input dtb filename")
    parser.add_argument('ovrl_filename', help="input dtbo filename")
    parser.add_argument(
        "--to_json",
        action="store_true",
        help="Create a json file.",
    )
    parser.add_argument(
        "--to_dts",
        action="store_true",
        help="Create a dtb file.",
    )
    args = parser.parse_args()
    main_ftd = read_binary_file(args.dtb_filename)
    main_phandle_2_node_name = get_phandles(main_ftd)

    overlay_ftd = read_binary_file(args.ovrl_filename)

    fixup_overlay(overlay_ftd, main_ftd, main_phandle_2_node_name)
    apply_fixed_up_overlay(overlay_ftd, main_ftd, main_phandle_2_node_name)

    if args.to_json:
        print(main_ftd.to_json())

    if args.to_dts:
        print(main_ftd.to_dts())
