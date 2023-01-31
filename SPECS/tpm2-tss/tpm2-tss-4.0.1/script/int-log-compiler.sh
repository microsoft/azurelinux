#!/usr/bin/env bash
#;**********************************************************************;
# SPDX-License-Identifier: BSD-2-Clause
#
# Copyright (c) 2017 - 2020, Intel Corporation
# Copyright (c) 2018 - 2020, Fraunhofer SIT sponsored by Infineon Technologies AG
#
# All rights reserved.
#;**********************************************************************;

# source the int-log-compiler-common sript
. ${srcdir}/script/int-log-compiler-common.sh

sanity_test

# start simulator if needed
if [[ ${INTEGRATION_TCTI} == "mssim" || ${INTEGRATION_TCTI} == "swtpm" ]]; then
    echo "Trying to start simulator ${INTEGRATION_TCTI}"
    try_simulator_start
fi

TPM20TEST_SOCKET_PORT="${SIM_PORT_DATA}"
TPM20TEST_TCTI="${INTEGRATION_TCTI}:host=${TPM20TEST_SOCKET_ADDRESS},port=${TPM20TEST_SOCKET_PORT}"

while true; do

# Some debug prints
echo "TPM20TEST_TCTI_NAME=${TPM20TEST_TCTI_NAME}"
echo "TPM20TEST_DEVICE_FILE=${TPM20TEST_DEVICE_FILE}"
echo "TPM20TEST_SOCKET_ADDRESS=${TPM20TEST_SOCKET_ADDRESS}"
echo "TPM20TEST_SOCKET_PORT=${TPM20TEST_SOCKET_PORT}"
echo "TPM20TEST_TCTI=${TPM20TEST_TCTI}"

if [ "${TPM20TEST_TCTI_NAME}" != "device" ]; then
    env TPM20TEST_TCTI_NAME="${TPM20TEST_TCTI_NAME}" \
        TPM20TEST_SOCKET_ADDRESS="${TPM20TEST_SOCKET_ADDRESS}" \
        TPM20TEST_SOCKET_PORT="${TPM20TEST_SOCKET_PORT}" \
        TPM20TEST_TCTI="${TPM20TEST_TCTI}" \
        G_MESSAGES_DEBUG=all ./test/helper/tpm_startup
    if [ $? -ne 0 ]; then
        echo "TPM_StartUp failed"
        ret=99
        break
    fi
else
    env TPM20TEST_TCTI_NAME=${TPM20TEST_TCTI_NAME} \
        TPM20TEST_DEVICE_FILE=${TPM20TEST_DEVICE_FILE} \
        G_MESSAGES_DEBUG=all ./test/helper/tpm_transientempty
    if [ $? -ne 0 ]; then
        echo "TPM transient area not empty => skipping"
        ret=99
        break
    fi
fi

TPMSTATE_FILE1=${TEST_BIN}_state1
TPMSTATE_FILE2=${TEST_BIN}_state2

env TPM20TEST_TCTI_NAME="${TPM20TEST_TCTI_NAME}" \
    TPM20TEST_SOCKET_ADDRESS="${TPM20TEST_SOCKET_ADDRESS}" \
    TPM20TEST_SOCKET_PORT="${TPM20TEST_SOCKET_PORT}" \
    TPM20TEST_TCTI="${TPM20TEST_TCTI}" \
    TPM20TEST_DEVICE_FILE="${TPM20TEST_DEVICE_FILE}" \
    G_MESSAGES_DEBUG=all ./test/helper/tpm_dumpstate>${TPMSTATE_FILE1}
if [ $? -ne 0 ]; then
    echo "Error during dumpstate"
    ret=99
    break
fi

echo "Execute the test script"
env TPM20TEST_TCTI_NAME="${TPM20TEST_TCTI_NAME}" \
    TPM20TEST_SOCKET_ADDRESS="${TPM20TEST_SOCKET_ADDRESS}" \
    TPM20TEST_SOCKET_PORT="${TPM20TEST_SOCKET_PORT}" \
    TPM20TEST_TCTI="${TPM20TEST_TCTI}" \
    TPM20TEST_DEVICE_FILE="${TPM20TEST_DEVICE_FILE}" \
    G_MESSAGES_DEBUG=all ${@: -1}
ret=$?
echo "Script returned $ret"

#We check the state before a reboot to see if transients and NV were chagned.
env TPM20TEST_TCTI_NAME="${TPM20TEST_TCTI_NAME}" \
    TPM20TEST_SOCKET_ADDRESS="${TPM20TEST_SOCKET_ADDRESS}" \
    TPM20TEST_SOCKET_PORT="${TPM20TEST_SOCKET_PORT}" \
    TPM20TEST_TCTI="${TPM20TEST_TCTI}" \
    TPM20TEST_DEVICE_FILE="${TPM20TEST_DEVICE_FILE}" \
    G_MESSAGES_DEBUG=all ./test/helper/tpm_dumpstate>${TPMSTATE_FILE2}
if [ $? -ne 0 ]; then
    echo "Error during dumpstate"
    ret=99
    break
fi

if [ "$(cat ${TPMSTATE_FILE1})" != "$(cat ${TPMSTATE_FILE2})" ]; then
    echo "TPM changed state during test"
    echo "State before ($TPMSTATE_FILE1):"
    cat ${TPMSTATE_FILE1}
    echo "State after ($TPMSTATE_FILE2):"
    cat ${TPMSTATE_FILE2}
    ret=1
    break
fi

break
done

# This sleep is sadly necessary: If we kill the tabrmd w/o sleeping for a
# second after the test finishes the simulator will die too. Bug in the
# simulator?
sleep 1
# teardown
daemon_stop ${SIM_PID_FILE}
rm -rf ${SIM_TMP_DIR} ${SIM_PID_FILE}
exit $ret
