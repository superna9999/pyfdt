#!/bin/bash

set -e

cd `dirname $0`

DTB_TESTS="
addresses.test.dtb                   moved.test_tree1.dtb                               reg-ranges-root.dts.test.dtb
aliases.dtb                          moved.unfinished_tree1.test.dtb                    repacked.v16.mst.test_tree1.dtb
aliases.dts.test.dtb                 multilabel_merge.test.dtb                          repacked.v16.mts.test_tree1.dtb
appendprop1.test.dtb                 multilabel.test.dtb                                repacked.v16.smt.test_tree1.dtb
appendprop2.test.dtb                 noppy.rw_tree1.test.dtb                            repacked.v16.stm.test_tree1.dtb
appendprop.test.dtb                  noppy.sw_tree1.test.dtb                            repacked.v16.tms.test_tree1.dtb
bad-empty-ranges.dts.test.dtb        noppy.test_tree1.dtb                               repacked.v16.tsm.test_tree1.dtb
bad-name-property.dts.test.dtb       oasm_aliases.dts.test.dtb                          repacked.v17.mst.test_tree1.dtb
bad-ncells.dts.test.dtb              oasm_comments.dts.test.dtb                         repacked.v17.mts.test_tree1.dtb
bad_node_char.dtb                    oasm_escapes.dts.test.dtb                          repacked.v17.smt.test_tree1.dtb
bad_node_format.dtb                  oasm_incbin.dts.test.dtb                           repacked.v17.stm.test_tree1.dtb
bad_prop_char.dtb                    oasm_include0.dts.test.dtb                         repacked.v17.tms.test_tree1.dtb
bad-reg-ranges.dts.test.dtb          oasm_path-references.dts.test.dtb                  repacked.v17.tsm.test_tree1.dtb
bad-string-props.dts.test.dtb        oasm_references.dts.test.dtb                       rw_tree1.test.dtb
boot_cpuid_17.test.dtb               oasm_test_tree1.dts.test.dtb                       search_paths_b.dtb
boot_cpuid.test.dtb                  oasm_value-labels.dts.test.dtb                     search_paths.dtb
comments.dts.test.dtb                obsolete-chosen-interrupt-controller.dts.test.dtb  search_paths_subdir.dtb
default-addr-size.dts.test.dtb       odts_dtc_escapes.test.dtb.test.dtb                 shunted.sw_tree1.test.dtb
dependencies.test.dtb                odts_dtc_extra-terminating-null.test.dtb.test.dtb  shunted.test_tree1.dtb
deshunted.sw_tree1.test.dtb          odts_dtc_references.test.dtb.test.dtb              shunted.unfinished_tree1.test.dtb 
deshunted.test_tree1.dtb             odts_dtc_tree1.test.dtb.test.dtb                   sourceoutput.test.dtb
deshunted.unfinished_tree1.test.dtb  odts_test_tree1.dtb.test.dtb                       sourceoutput.test.dts.test.dtb
dtc_char_literal.test.dtb            opened.v16.mst.test_tree1.dtb                      stdin_dtc_tree1.test.dtb
dtc_comments-cmp.test.dtb            opened.v16.mts.test_tree1.dtb                      subnode_iterate.dtb
dtc_comments.test.dtb                opened.v16.smt.test_tree1.dtb                      sw_tree1.test.dtb
dtc_escapes.test.dtb                 opened.v16.stm.test_tree1.dtb                      test_tree1.dtb
dtc_extra-terminating-null.test.dtb  opened.v16.tms.test_tree1.dtb                      test_tree1.dtb.reversed.sorted.test.dtb
dtc_path-references.test.dtb         opened.v16.tsm.test_tree1.dtb                      test_tree1.dtb.reversed.test.dtb
dtc_references.test.both.dtb         opened.v17.mst.test_tree1.dtb                      test_tree1.dtb.sorted.test.dtb
dtc_references.test.dtb              opened.v17.mts.test_tree1.dtb                      test_tree1.dts.test.dtb
dtc_references.test.epapr.dtb        opened.v17.smt.test_tree1.dtb                      test_tree1_wrong1.test.dtb
dtc_references.test.legacy.dtb       opened.v17.stm.test_tree1.dtb                      test_tree1_wrong2.test.dtb
dtc_sized_cells.test.dtb             opened.v17.tms.test_tree1.dtb                      test_tree1_wrong3.test.dtb
dtc_tree1_delete.test.dtb            opened.v17.tsm.test_tree1.dtb                      test_tree1_wrong4.test.dtb
dtc_tree1_merge_labelled.test.dtb    ov16_ov16_test_tree1.dtb.test.dtb                  test_tree1_wrong5.test.dtb
dtc_tree1_merge_path.test.dtb        ov16_ov17_test_tree1.dtb.test.dtb                  test_tree1_wrong6.test.dtb
dtc_tree1_merge.test.dtb             ov16_ov1_test_tree1.dtb.test.dtb                   test_tree1_wrong7.test.dtb
dtc_tree1.test.dtb                   ov16_ov2_test_tree1.dtb.test.dtb                   test_tree1_wrong8.test.dtb
dup-nodename.dts.test.dtb            ov16_ov3_test_tree1.dtb.test.dtb                   test_tree1_wrong9.test.dtb
dup-phandle.dts.test.dtb             ov16_test_tree1.dtb.test.dtb                       unfinished_tree1.test.dtb
dup-propname.dts.test.dtb            ov17_ov16_test_tree1.dtb.test.dtb                  v16.mst.test_tree1.dtb
embedded_nul_equiv.test.dtb          ov17_ov17_test_tree1.dtb.test.dtb                  v16.mts.test_tree1.dtb
embedded_nul.test.dtb                ov17_ov1_test_tree1.dtb.test.dtb                   v16.smt.test_tree1.dtb
escapes.dts.test.dtb                 ov17_ov2_test_tree1.dtb.test.dtb                   v16.stm.test_tree1.dtb
incbin.dts.test.dtb                  ov17_ov3_test_tree1.dtb.test.dtb                   v16.tms.test_tree1.dtb
incbin.test.dtb                      ov17_test_tree1.dtb.test.dtb                       v16.tsm.test_tree1.dtb
include0.dts.test.dtb                ov1_test_tree1.dtb.test.dtb                        v17.mst.test_tree1.dtb
includes.test.dtb                    ov2_test_tree1.dtb.test.dtb                        v17.mts.test_tree1.dtb
integer-expressions.test.dtb         ov3_test_tree1.dtb.test.dtb                        v17.smt.test_tree1.dtb
label01.dts.fdtget.test.dtb          override0_boot_cpuid_17.test.dtb                   v17.stm.test_tree1.dtb
label01.dts.fdtput.test.dtb          override17_boot_cpuid.test.dtb                     v17.tms.test_tree1.dtb
label_repeated.test.dtb              path-references.dts.test.dtb                       v17.tsm.test_tree1.dtb
line_directives.test.dtb             preserve_boot_cpuid_17.test.dtb                    value-labels.dts.test.dtb
minusone-phandle.dts.test.dtb        preserve_boot_cpuid.test.dtb                       zero-phandle.dts.test.dtb
moved.sw_tree1.test.dtb              references.dts.test.dtb"

MUST_FAIL_PARSE="
moved.unfinished_tree1.test.dtb
shunted.unfinished_tree1.test.dtb
deshunted.unfinished_tree1.test.dtb
unfinished_tree1.test.dtb
dup-nodename.dts.test.dtb
dup-propname.dts.test.dtb"

CAN_FAIL_HEAD_DTS_DIFF="
moved.test_tree1.dtb
repacked.v16.mst.test_tree1.dtb
repacked.v16.mts.test_tree1.dtb
repacked.v16.smt.test_tree1.dtb
noppy.rw_tree1.test.dtb
repacked.v16.stm.test_tree1.dtb
noppy.sw_tree1.test.dtb
repacked.v16.tms.test_tree1.dtb
noppy.test_tree1.dtb
repacked.v16.tsm.test_tree1.dtb
repacked.v17.mst.test_tree1.dtb
repacked.v17.mts.test_tree1.dtb
repacked.v17.smt.test_tree1.dtb
repacked.v17.stm.test_tree1.dtb
repacked.v17.tms.test_tree1.dtb
repacked.v17.tsm.test_tree1.dtb
shunted.sw_tree1.test.dtb
shunted.test_tree1.dtb
deshunted.sw_tree1.test.dtb
deshunted.test_tree1.dtb
opened.v16.mst.test_tree1.dtb
opened.v16.mts.test_tree1.dtb
opened.v16.smt.test_tree1.dtb
sw_tree1.test.dtb
opened.v16.stm.test_tree1.dtb
test_tree1.dtb
opened.v16.tms.test_tree1.dtb
opened.v16.tsm.test_tree1.dtb
test_tree1.dtb.reversed.test.dtb
opened.v17.mst.test_tree1.dtb
opened.v17.mts.test_tree1.dtb
opened.v17.smt.test_tree1.dtb
opened.v17.stm.test_tree1.dtb
opened.v17.tms.test_tree1.dtb
opened.v17.tsm.test_tree1.dtb
v16.mst.test_tree1.dtb
v16.mts.test_tree1.dtb
v16.smt.test_tree1.dtb
v16.stm.test_tree1.dtb
v16.tms.test_tree1.dtb
v16.tsm.test_tree1.dtb
v17.mst.test_tree1.dtb
v17.mts.test_tree1.dtb
v17.smt.test_tree1.dtb
v17.stm.test_tree1.dtb
v17.tms.test_tree1.dtb
v17.tsm.test_tree1.dtb
moved.sw_tree1.test.dtb
"

echo "Building DTC..."
make -C dtc all tests
echo "Running DTC Tests..."
(cd dtc/tests/ && ./run_tests.sh)

TESTS=0
PASS=0
FAIL=0

FAILED=""

echo "Running pyfdt DTB Parser Tests..."
for dtb in $DTB_TESTS; do
    TESTS=`expr $TESTS + 1`
    echo "TEST $dtb..."
    SKIP=0
    if ! ../dtbdump.py --format dtb dtc/tests/$dtb $dtb ; then
        if echo $MUST_FAIL_PARSE  | grep -q $dtb; then
            echo "PASS $dtb failure expected"
            SKIP=1
        else
            echo "FAIL parsing $dtb"
            FAIL=`expr $FAIL + 1`
            FAILED="$FAILED $dtb"
            continue
        fi
    fi
    if [ $SKIP -lt 1 ] ; then
        if ! dtc/fdtdump $dtb > $dtb.dts ; then
            echo "FAIL dump : $dtb see $dtb.hex"
            hd < $dtb > $dtb.hex
            hd < dtc/tests/$dtb > $dtb.orig.hex
            FAIL=`expr $FAIL + 1`
            FAILED="$FAILED $dtb"
            continue
        fi
        dtc/fdtdump dtc/tests/$dtb > $dtb.orig.dts
        ../dtbdump.py --format dts dtc/tests/$dtb $dtb.pydts
        grep -v "// " $dtb.orig.dts > $dtb.orig.dts_
        grep -v "// " $dtb.dts > $dtb.dts_
        grep -v "// " $dtb.pydts > $dtb.pydts_
        if ! diff -u $dtb.dts $dtb.orig.dts > $dtb.result ; then
            if echo $CAN_FAIL_HEAD_DTS_DIFF  | grep -q $dtb; then
                echo "PASS $dtb header diff failure expected"
            else
                echo "FAIL diff : $dtb see $dtb.result"
                hd < $dtb > $dtb.hex
                hd < dtc/tests/$dtb > $dtb.orig.hex
                FAIL=`expr $FAIL + 1`
                FAILED="$FAILED $dtb"
                continue
            fi
        fi
        if ! diff -u $dtb.dts_ $dtb.orig.dts_ > $dtb.result ; then
            echo "FAIL diff : $dtb see $dtb.result"
            hd < $dtb > $dtb.hex
            hd < dtc/tests/$dtb > $dtb.orig.hex
            FAIL=`expr $FAIL + 1`
            FAILED="$FAILED $dtb"
            continue
        fi
        if ! diff -u $dtb.pydts_ $dtb.orig.dts_ > $dtb.result_ ; then
            echo "FAIL pydump diff : $dtb see $dtb.result_"
            hd < $dtb > $dtb.hex
            hd < dtc/tests/$dtb > $dtb.orig.hex
            FAIL=`expr $FAIL + 1`
            FAILED="$FAILED $dtb"
            continue
        fi
        if echo $MUST_FAIL  | grep -q $dtb; then
            echo "ERROR $dtb should have failed"
            FAIL=`expr $FAIL + 1`
            FAILED="$FAILED $dtb"
            continue
        fi
        rm $dtb*
    fi
    PASS=`expr $PASS + 1`
done

PYFDT_TESTS="
bad_testname_test
basic
gen_v1
gen_v2 
gen_v3
gen_dup
gen_nobyte
gen_badbyte
gen_noword
gen_badword
gen_emptystr
gen_badstr
gen_norootnode
manip_setitem
manip_append
manip_pop
manip_insert
manip_remove
manip_index
manip_bad_setitem
manip_dup_append
manip_empty_pop
manip_dup_insert
manip_noexist_remove
manip_noexist_index
"

PYFDT_TESTS_FAILS="
bad_testname_test
gen_dup
gen_nobyte
gen_badbyte
gen_noword
gen_badword
gen_emptystr
gen_badstr
gen_norootnode
manip_bad_setitem
manip_dup_append
manip_empty_pop
manip_dup_insert
manip_noexist_remove
manip_noexist_index
"

echo "Running pyfdt generation Tests..."
for dtb in $PYFDT_TESTS; do
    TESTS=`expr $TESTS + 1`
    echo "TEST $dtb..."
    SKIP=0
    if ! PYTHONPATH=$PWD/../ ./genfdt.py $dtb ; then
        if echo $PYFDT_TESTS_FAILS  | grep -q $dtb; then
            echo "PASS $dtb failure expected"
            SKIP=1
        else
            echo "FAIL generating $dtb"
            FAIL=`expr $FAIL + 1`
            FAILED="$FAILED $dtb"
            continue
        fi
    fi
    if [ $SKIP -lt 1 ] ; then
        if ! dtc/fdtdump out.dtb > $dtb.dts ; then
            echo "FAIL dump : $dtb see $dtb.hex"
            hd < out.dtb > $dtb.hex
            FAIL=`expr $FAIL + 1`
            FAILED="$FAILED $dtb"
            continue
        fi
        ../dtbdump.py --format dts out.dtb $dtb.pydts
        if ! diff -u out.dts $dtb.pydts > $dtb.pyresult ; then
            echo "FAIL diff : $dtb see $dtb.pyresult"
            hd < out.dtb > $dtb.hex
            cp out.dts $dtb.orig.pydts
            FAIL=`expr $FAIL + 1`
            FAILED="$FAILED $dtb"
            continue
        fi
        grep -v "// " $dtb.dts > $dtb.dts_
        grep -v "// " $dtb.pydts > $dtb.pydts_
        if ! diff -u $dtb.dts_ $dtb.pydts_ > $dtb.result ; then
            echo "FAIL diff : $dtb see $dtb.result"
            hd < out.dtb > $dtb.hex
            FAIL=`expr $FAIL + 1`
            FAILED="$FAILED $dtb"
            continue
        fi
        rm out.dts out.dtb $dtb*
        if echo $PYFDT_TESTS_FAILS  | grep -q $dtb; then
            echo "FAIL $dtb failure was expected"
            FAIL=`expr $FAIL + 1`
            FAILED="$FAILED $dtb"
            continue
        fi
    fi
    PASS=`expr $PASS + 1`
done

echo "Passed : $PASS/$TESTS"
echo "Failed : $FAIL/$TESTS"

echo "List Failed :"
for failed in $FAILED ; do
    echo $failed
done

if [ $FAIL -lt 0 ] ; then
    exit 1
fi

exit 0
