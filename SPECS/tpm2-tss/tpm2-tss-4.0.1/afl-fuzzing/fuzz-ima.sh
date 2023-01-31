#!/bin/bash
# SPDX-License-Identifier: BSD-2-Clause
#set -x
export srcdir=$(pwd)

function stop() {
    killall afl-fuzz
    }


trap stop

mkdir -p afl-fuzzing/ima-sml
for x in sml-ima-ng-sha1.b64  sml-ima-sha1.b64  sml-ima-sha1-invalidated.b64  sml-ima-sig-sha256.b64  sml-ima-sig-sha256-invalidated.b64
do
    base64 -d test/data/fapi/eventlog/$x > afl-fuzzing/ima-sml/${x%.b64}.bin
done

afl-clang-fast -flto -o fapi-ima-fuzzing test/unit/fapi-ima-fuzzing.c \
               src/tss2-fapi/ifapi_ima_eventlog.c \
               src/tss2-fapi/ifapi_json_deserialize.c \
               src/tss2-fapi/ifapi_json_serialize.c \
               src/tss2-fapi/ifapi_policy_json_deserialize.c \
               src/tss2-fapi/ifapi_policy_json_serialize.c \
               src/tss2-fapi/tpm_json_deserialize.c \
               src/tss2-fapi/tpm_json_serialize.c \
               src/tss2-fapi/ifapi_json_eventlog_serialize.c \
               src/tss2-fapi/fapi_crypto.c \
               src/tss2-fapi/ifapi_eventlog.c \
               src/tss2-fapi/ifapi_helpers.c \
               src/tss2-fapi/ifapi_eventlog_system.c\
               src/tss2-fapi/ifapi_keystore.c  \
               src/tss2-fapi/ifapi_io.c \
               src/util/log.c \
               -DHAVE_CONFIG_H -I${srcdir} -I${srcdir}/include -I${srcdir}/src \
               -I${srcdir}/include -I${srcdir}/include/tss2 \
               -I${srcdir}/src/util -I${srcdir}/src/tss2-mu \
               -I${srcdir}/src/tss2-sys -I${srcdir}/src/tss2-esys \
               -I${srcdir}/src/tss2-fapi \
               -I${srcdir}/test/data \
               -Wno-unused-parameter -Wno-missing-field-initializers \
               -lcrypto -ljson-c

rm -r -f findings-ima
AFL_SKIP_CPUFREQ=1 afl-fuzz -M fuzz0 -iafl-fuzzing/ima-sml/ -ofindings-ima ./fapi-ima-fuzzing @@ &

if [ ! -z "$1" ]; then
    for i in $(seq $1)
    do
        AFL_SKIP_CPUFREQ=1 afl-fuzz -S fuzz${i} -iafl-fuzzing/ima-sml -ofindings-ima ./fapi-ima-fuzzing @@ > /dev/null &
    done
fi
wait
cat findings-ima/fuzz*/fuzzer_stats | grep uniq
