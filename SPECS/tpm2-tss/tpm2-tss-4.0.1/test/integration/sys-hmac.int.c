/* SPDX-License-Identifier: BSD-2-Clause */
/*******************************************************************************
 * Copyright 2017-2018, Fraunhofer SIT sponsored by Infineon Technologies AG
 * All rights reserved.
 *******************************************************************************/

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include "tss2_tpm2_types.h"
#include "tss2_sys.h"
#include "util/tpm2b.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <inttypes.h>

#include "tss2_tcti.h"
#include "tss2_sys.h"

#define LOGMODULE test
#include "util/log.h"
#include "test.h"
#include "sys-util.h"

int
test_sys_hmac(TSS2_SYS_CONTEXT * sys_context)
{

    TSS2_RC rc;
    TPM2B_PUBLIC out_public = { 0 };
    TPM2B_CREATION_DATA creation_data = {0,};
    creation_data.size = 0;
    TPM2B_DIGEST creation_hash = {
        .size = sizeof(creation_hash.buffer)
    };
    TPMT_TK_CREATION creation_ticket = { 0 };
    TPM2B_NAME name;
    TSS2L_SYS_AUTH_COMMAND sessions_cmd = {
        .auths = {{ .sessionHandle = TPM2_RH_PW }},
        .count = 1
    };
    TSS2L_SYS_AUTH_RESPONSE sessions_rsp = {
        .auths = { 0 },
        .count = 0
    };
    TPM2_HANDLE primaryHandle;

    if (sys_context == NULL) {
        return TSS2_RC_LAYER_MASK | TSS2_BASE_RC_BAD_REFERENCE;
    }

    TPM2B_DIGEST outHMAC = { 0 };

    TPM2B_SENSITIVE_CREATE in_sensitive = { 0 };
    TPM2B_PUBLIC inPublic = { 0 };

    TPM2B_DATA outsideInfo = {
        .size = 0,
        .buffer = {},
    };
    TPML_PCR_SELECTION creationPCR = {
        .count = 0,
    };

    inPublic.publicArea.nameAlg = TPM2_ALG_SHA256;
    inPublic.publicArea.type = TPM2_ALG_KEYEDHASH;
    inPublic.publicArea.objectAttributes |= TPMA_OBJECT_SIGN_ENCRYPT;
    inPublic.publicArea.objectAttributes |= TPMA_OBJECT_USERWITHAUTH;
    inPublic.publicArea.objectAttributes |= TPMA_OBJECT_SENSITIVEDATAORIGIN;
    inPublic.publicArea.parameters.keyedHashDetail.scheme.scheme = TPM2_ALG_HMAC;
    inPublic.publicArea.parameters.keyedHashDetail.scheme.details.hmac.hashAlg = TPM2_ALG_SHA256;

    rc = Tss2_Sys_CreatePrimary (sys_context, TPM2_RH_OWNER, &sessions_cmd,
                                 &in_sensitive, &inPublic, &outsideInfo,
                                 &creationPCR, &primaryHandle, &out_public,
                                 &creation_data, &creation_hash,
                                 &creation_ticket, &name, &sessions_rsp);
    if (rc != TPM2_RC_SUCCESS) {
        LOG_ERROR("CreatePrimary FAILED! Response Code : 0x%x", rc);
        exit(1);
    }

    TPM2B_MAX_BUFFER test_buffer = { .size = 20,
                                     .buffer={0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0,
                                              1, 2, 3, 4, 5, 6, 7, 8, 9}};

    rc = TSS2_RETRY_EXP(Tss2_Sys_HMAC(sys_context, primaryHandle,
                        &sessions_cmd, &test_buffer, TPM2_ALG_SHA256, &outHMAC,
                        &sessions_rsp));

    if (rc != TSS2_RC_SUCCESS) {
        LOG_ERROR("Tss2_Sys_MAC FAILED! Response Code : 0x%x", rc);
    }

    TPMT_SIGNATURE sig;
    sig.signature.hmac.hashAlg = TPM2_ALG_SHA256;
    sig.sigAlg = TPM2_ALG_HMAC;
    memcpy(sig.signature.hmac.digest.sha256, outHMAC.buffer, outHMAC.size);

    TPM2B_DIGEST dig = { .size = 20,
                         .buffer={0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0,
                                  1, 2, 3, 4, 5, 6, 7, 8, 9}} ;
    TPMT_TK_VERIFIED validation = { 0 };
    TSS2L_SYS_AUTH_RESPONSE sessions_rsp2 = {
        .auths = { 0 },
        .count = 0
    };

    rc = Tss2_Sys_VerifySignature(sys_context, primaryHandle, NULL, &dig, &sig,
                                  &validation, &sessions_rsp2);
    if (rc != TSS2_RC_SUCCESS) {
        LOG_ERROR("Tss2_Sys_VerifySignature FAILED! Response Code : 0x%x", rc);
        return 99;
    }

    rc = Tss2_Sys_FlushContext(sys_context, primaryHandle);
    if (rc != TSS2_RC_SUCCESS) {
        LOG_ERROR("Tss2_Sys_FlushContext failed with 0x%x", rc);
        return 99; /* fatal error */
    }

    return rc;
}

int
test_invoke (TSS2_SYS_CONTEXT *sys_ctx) {
    return test_sys_hmac(sys_ctx);
}
