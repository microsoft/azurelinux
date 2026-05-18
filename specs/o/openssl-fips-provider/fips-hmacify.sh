#!/bin/bash

dd if=/dev/zero bs=1 count=32 of=tmp.mac >/dev/null 2>&1
objcopy --update-section .rodata1=tmp.mac $1 $1.zeromac
mv $1.zeromac $1
LD_LIBRARY_PATH=. apps/openssl dgst -binary -sha256 -mac HMAC -macopt hexkey:f4556650ac31d35461610bac4ed81b1a181b2d8a43ea2854cbae22ca74560813 < $1 > $1.hmac
objcopy --update-section .rodata1=$1.hmac $1 $1.mac
rm $1.hmac
mv $1.mac $1
