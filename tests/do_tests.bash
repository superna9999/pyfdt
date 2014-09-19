#!/bin/bash

set -e

DTB_TESTS="
addresses.test.dtb                   dtc_references.test.both.dtb       label01.dts.fdtget.test.dtb                        search_paths.dtb
aliases.dtb                          dtc_references.test.dtb            label01.dts.fdtput.test.dtb                        search_paths_subdir.dtb
aliases.dts.test.dtb                 dtc_references.test.epapr.dtb      label_repeated.test.dtb                            sourceoutput.test.dtb
appendprop.test.dtb                  dtc_references.test.legacy.dtb     line_directives.test.dtb                           sourceoutput.test.dts.test.dtb
bad-empty-ranges.dts.test.dtb        dtc_sized_cells.test.dtb           minusone-phandle.dts.test.dtb                      stdin_dtc_tree1.test.dtb
bad-name-property.dts.test.dtb       dtc_tree1_delete.test.dtb          multilabel_merge.test.dtb                          subnode_iterate.dtb
bad-ncells.dts.test.dtb              dtc_tree1_merge_labelled.test.dtb  multilabel.test.dtb                                test_tree1.dts.test.dtb
bad-reg-ranges.dts.test.dtb          dtc_tree1_merge_path.test.dtb      obsolete-chosen-interrupt-controller.dts.test.dtb  test_tree1_wrong1.test.dtb
bad-string-props.dts.test.dtb        dtc_tree1_merge.test.dtb           odts_dtc_escapes.test.dtb.test.dtb                 test_tree1_wrong2.test.dtb
boot_cpuid_17.test.dtb               dtc_tree1.test.dtb                 odts_dtc_extra-terminating-null.test.dtb.test.dtb  test_tree1_wrong3.test.dtb
boot_cpuid.test.dtb                  dup-nodename.dts.test.dtb          odts_dtc_references.test.dtb.test.dtb              test_tree1_wrong4.test.dtb
comments.dts.test.dtb                dup-phandle.dts.test.dtb           odts_dtc_tree1.test.dtb.test.dtb                   test_tree1_wrong5.test.dtb
default-addr-size.dts.test.dtb       dup-propname.dts.test.dtb          override0_boot_cpuid_17.test.dtb                   test_tree1_wrong6.test.dtb
dependencies.test.dtb                embedded_nul_equiv.test.dtb        override17_boot_cpuid.test.dtb                     test_tree1_wrong7.test.dtb
dtc_char_literal.test.dtb            embedded_nul.test.dtb              path-references.dts.test.dtb                       test_tree1_wrong8.test.dtb
dtc_comments-cmp.test.dtb            escapes.dts.test.dtb               preserve_boot_cpuid_17.test.dtb                    test_tree1_wrong9.test.dtb
dtc_comments.test.dtb                incbin.dts.test.dtb                preserve_boot_cpuid.test.dtb                       value-labels.dts.test.dtb
dtc_escapes.test.dtb                 incbin.test.dtb                    references.dts.test.dtb                            zero-phandle.dts.test.dtb
dtc_extra-terminating-null.test.dtb  include0.dts.test.dtb              reg-ranges-root.dts.test.dtb
dtc_path-references.test.dtb         includes.test.dtb                  search_paths_b.dtb"

echo "Building DTC..."
make -C dtc
echo "Running DTC Tests..."
(cd dtc/tests/ && ./run_tests.sh)

PASS=0
FAIL=0

echo "Running pyfdt DTB Parser Tests..."
for dtb in $DTB_TESTS; do
    echo "TEST $dtb..."
    if ! ../dtbdump.py --format dtb dtc/tests/$dtb $dtb ; then
        echo "FAIL parsing $dtb"
        FAIL=`expr $FAIL + 1`
        continue
    fi
    hd < $dtb > $dtb.hex
    hd < dtc/tests/$dtb > $dtb.orig.hex
    if ! diff $dtb.hex $dtb.orig.hex > $dtb.result ; then
        echo "FAIL output : $dtb see $dtb.result"
        FAIL=`expr $FAIL + 1`
        continue
    fi
    rm $dtb*
    PASS=`expr $PASS + 1`
done

echo "Passed : $PASS"
echo "Failed : $FAIL"

if [ $FAIL -lt 0 ] ; then
    exit 1
fi

exit 0
