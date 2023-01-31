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
    TPM20TEST_SOCKET_PORT="${SIM_PORT_DATA}"
    TPM20TEST_TCTI="${INTEGRATION_TCTI}:host=${TPM20TEST_SOCKET_ADDRESS},port=${TPM20TEST_SOCKET_PORT}"
else
    # Device will be used.
    TPM20TEST_TCTI="${INTEGRATION_TCTI}:${TPM20TEST_DEVICE_FILE}"
fi

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

# Certificate generation for simulator tests
if [ "${TPM20TEST_TCTI_NAME}" != "device" ]; then
    EKPUB_FILE=${TEST_BIN}_ekpub.pem
    EKCERT_FILE=${TEST_BIN}_ekcert.crt
    EKCERT_PEM_FILE=${TEST_BIN}_ekcert.pem

    env TPM20TEST_TCTI_NAME="${TPM20TEST_TCTI_NAME}" \
        TPM20TEST_SOCKET_ADDRESS="${TPM20TEST_SOCKET_ADDRESS}" \
        TPM20TEST_SOCKET_PORT="${TPM20TEST_SOCKET_PORT}" \
        TPM20TEST_TCTI="${TPM20TEST_TCTI}" \
        TPM20TEST_DEVICE_FILE="${TPM20TEST_DEVICE_FILE}" \
        G_MESSAGES_DEBUG=all ./test/helper/tpm_getek ${EKPUB_FILE}
    if [ $? -ne 0 ]; then
        echo "TPM_getek failed"
        ret=99
        break
    fi

    EKECCPUB_FILE=${TEST_BIN}_ekeccpub.pem
    EKECCCERT_FILE=${TEST_BIN}_ekecccert.crt
    EKECCCERT_PEM_FILE=${TEST_BIN}_ekecccert.pem

    env TPM20TEST_TCTI_NAME="${TPM20TEST_TCTI_NAME}" \
        TPM20TEST_SOCKET_ADDRESS="${TPM20TEST_SOCKET_ADDRESS}" \
        TPM20TEST_SOCKET_PORT="${TPM20TEST_SOCKET_PORT}" \
        TPM20TEST_TCTI="${TPM20TEST_TCTI}" \
        TPM20TEST_DEVICE_FILE="${TPM20TEST_DEVICE_FILE}" \
        G_MESSAGES_DEBUG=all ./test/helper/tpm_getek_ecc ${EKECCPUB_FILE}
    if [ $? -ne 0 ]; then
        echo "TPM_getek_ecc failed"
        ret=99
        break
    fi

    INTERMEDCA_FILE=${TEST_BIN}_intermedecc-ca
    ROOTCA_FILE=${TEST_BIN}_root-ca

    SCRIPTDIR="$(dirname $(realpath $0))/"
    ${SCRIPTDIR}/ekca/create_ca.sh "${EKPUB_FILE}" "${EKECCPUB_FILE}" "${EKCERT_FILE}" \
                "${EKECCCERT_FILE}" "${INTERMEDCA_FILE}" "${ROOTCA_FILE}" >${TEST_BIN}_ca.log 2>&1
    if [ $? -ne 0 ]; then
        echo "ek-cert ca failed"
        ret=99
        break
    fi

    # Determine the fingerprint of the RSA EK public.
    FINGERPRINT=$(openssl pkey -pubin -inform PEM -in ${EKPUB_FILE} -outform DER | shasum -a 256  | cut -f 1 -d ' ')
    export FAPI_TEST_FINGERPRINT=" { \"hashAlg\" : \"sha256\", \"digest\" : \"${FINGERPRINT}\" }"
    openssl x509 -inform DER -in ${EKCERT_FILE} -outform PEM -out ${EKCERT_PEM_FILE}
    export FAPI_TEST_CERTIFICATE="file:${EKCERT_PEM_FILE}"

    # Determine the fingerprint of the RSA EK public.
    FINGERPRINT_ECC=$(openssl pkey -pubin -inform PEM -in ${EKECCPUB_FILE} -outform DER | shasum -a 256  | cut -f 1 -d ' ')
    export FAPI_TEST_FINGERPRINT_ECC=" { \"hashAlg\" : \"sha256\", \"digest\" : \"${FINGERPRINT_ECC}\" }"
    openssl x509 -inform DER -in ${EKECCCERT_FILE} -outform PEM -out ${EKECCCERT_PEM_FILE}
    export FAPI_TEST_CERTIFICATE_ECC="file:${EKECCCERT_PEM_FILE}"

    cat $EKCERT_FILE | \
        env TPM20TEST_TCTI_NAME="${TPM20TEST_TCTI_NAME}" \
            TPM20TEST_SOCKET_ADDRESS="${TPM20TEST_SOCKET_ADDRESS}" \
            TPM20TEST_SOCKET_PORT="${TPM20TEST_SOCKET_PORT}" \
            TPM20TEST_TCTI="${TPM20TEST_TCTI}" \
            TPM20TEST_DEVICE_FILE="${TPM20TEST_DEVICE_FILE}" \
            G_MESSAGES_DEBUG=all ./test/helper/tpm_writeekcert 1C00002
    if [ $? -ne 0 ]; then
        echo "TPM_writeekcert failed"
        ret=99
        break
    fi

    cat $EKECCCERT_FILE | \
        env TPM20TEST_TCTI_NAME="${TPM20TEST_TCTI_NAME}" \
            TPM20TEST_SOCKET_ADDRESS="${TPM20TEST_SOCKET_ADDRESS}" \
            TPM20TEST_SOCKET_PORT="${TPM20TEST_SOCKET_PORT}" \
            TPM20TEST_TCTI="${TPM20TEST_TCTI}" \
            TPM20TEST_DEVICE_FILE="${TPM20TEST_DEVICE_FILE}" \
            G_MESSAGES_DEBUG=all ./test/helper/tpm_writeekcert 1C0000A
    if [ $? -ne 0 ]; then
        echo "TPM_writeekcert failed"
        ret=99
    fi
fi # certificate generation

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
if [ "${TPM20TEST_TCTI_NAME}" == "device" ]; then
    # No root certificate needed
    env TPM20TEST_TCTI_NAME="${TPM20TEST_TCTI_NAME}" \
        TPM20TEST_SOCKET_ADDRESS="${TPM20TEST_SOCKET_ADDRESS}" \
        TPM20TEST_SOCKET_PORT="${TPM20TEST_SOCKET_PORT}" \
        TPM20TEST_TCTI="${TPM20TEST_TCTI}" \
        TPM20TEST_DEVICE_FILE="${TPM20TEST_DEVICE_FILE}" \
        G_MESSAGES_DEBUG=all ${@: -1}
else
    # Run test with generated certificate.
    env TPM20TEST_TCTI_NAME="${TPM20TEST_TCTI_NAME}" \
        TPM20TEST_SOCKET_ADDRESS="${TPM20TEST_SOCKET_ADDRESS}" \
        TPM20TEST_SOCKET_PORT="${TPM20TEST_SOCKET_PORT}" \
        TPM20TEST_TCTI="${TPM20TEST_TCTI}" \
        FAPI_TEST_ROOT_CERT=${ROOTCA_FILE}.pem \
        TPM20TEST_DEVICE_FILE="${TPM20TEST_DEVICE_FILE}" \
        G_MESSAGES_DEBUG=all ${@: -1}
fi
ret=$?
echo "Script returned $ret"

#We check the state before a reboot to see if transients and NV were chagned.
env TPM20TEST_TCTI_NAME="${TPM20TEST_TCTI_NAME}" \
    TPM20TEST_SOCKET_ADDRESS="${TPM20TEST_SOCKET_ADDRESS}" \
    TPM20TEST_SOCKET_PORT="${TPM20TEST_SOCKET_PORT}" \
    TPM20TEST_TCTI="${TPM20TEST_TCTI}" \
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

#TODO: Add a tpm-restart/reboot here

break
done

if [ "${TPM20TEST_TCTI_NAME}" != "device" ]; then
    # This sleep is sadly necessary: If we kill the tabrmd w/o sleeping for a
    # second after the test finishes the simulator will die too. Bug in the
    # simulator?
    sleep 1
    # teardown
    daemon_stop ${SIM_PID_FILE}
    rm -rf ${SIM_TMP_DIR} ${SIM_PID_FILE}
fi

exit $ret
