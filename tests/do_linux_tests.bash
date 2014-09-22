#!/bin/bash

DTB_TESTS=$1/arch/arm/boot/dts/*.dtb

TESTS=0
PASS=0
FAIL=0

FAILED=""

echo "Running linux DTB Parser Tests..."
for dtb in $DTB_TESTS; do
    FILENAME=`basename $dtb`
    TESTS=`expr $TESTS + 1`
    echo "TEST $dtb..."
    if ! ../dtbdump.py --format dtb $dtb $FILENAME ; then
        echo "FAIL parsing $FILENAME"
        FAIL=`expr $FAIL + 1`
        FAILED="$FAILED $FILENAME"
        continue
    fi
    if ! dtc/fdtdump $FILENAME > $FILENAME.dts ; then
        echo "FAIL dump : $FILENAME see $FILENAME.hex"
        hd < $FILENAME > $FILENAME.hex
        hd < $dtb > $FILENAME.orig.hex
        FAIL=`expr $FAIL + 1`
        FAILED="$FAILED $FILENAME"
        continue
    fi
    dtc/fdtdump $dtb > $FILENAME.orig.dts
    if ! diff -u $FILENAME.dts $FILENAME.orig.dts > $FILENAME.result ; then
        echo "FAIL diff : $FILENAME see $FILENAME.result"
        hd < $FILENAME > $FILENAME.hex
        hd < $dtb > $FILENAME.orig.hex
        FAIL=`expr $FAIL + 1`
        FAILED="$FAILED $FILENAME"
        continue
    fi
    rm $FILENAME*
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

