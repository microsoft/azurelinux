/* SPDX-License-Identifier: BSD-2-Clause */
/***********************************************************************
 * Copyright (c) 2017-2018, Intel Corporation
 *
 * All rights reserved.
 ***********************************************************************/
#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <stdlib.h>

#include "tss2_tpm2_types.h"

#include "inttypes.h"
#define LOGMODULE test
#include "util/log.h"
#include "sys-util.h"
#include "test.h"

int
test_invoke (TSS2_SYS_CONTEXT *sys_context)
{
    TSS2_RC                  rc                = TPM2_RC_SUCCESS;
    TPM2_HANDLE              parent_handle     = 0;
    TPM2B_SENSITIVE_CREATE  inSensitive       = { 0 };
    TPM2B_DATA              outsideInfo       = { 0 };
    TPML_PCR_SELECTION      creationPCR       = { 0 };

    TPM2B_PRIVATE       outPrivate             = TPM2B_PRIVATE_INIT;
    TPM2B_PUBLIC        inPublic               = { 0 };
    TPM2B_PUBLIC        outPublic              = { 0 };
    TPM2B_CREATION_DATA creationData           = { 0 };
    TPM2B_DIGEST        creationHash           = TPM2B_DIGEST_INIT;
    TPMT_TK_CREATION    creationTicket         = { 0 };

    /* session parameters */
    /* command session info */
    TSS2L_SYS_AUTH_COMMAND  sessions_cmd         = {
        .auths = {{ .sessionHandle = TPM2_RH_PW }},
        .count = 1
    };
    /* response session info */
    TSS2L_SYS_AUTH_RESPONSE  sessions_rsp         = {
        .auths = { 0 },
        .count = 0
    };

    rc = create_primary_rsa_2048_aes_128_cfb (sys_context, &parent_handle);
    if (rc == TSS2_RC_SUCCESS) {
        LOG_INFO("primary created successfully: 0x%" PRIx32, parent_handle);
    } else {
        LOG_ERROR("CreatePrimary failed with 0x%" PRIx32, rc);
        return 99; /* fatal error */
    }

    inPublic.publicArea.nameAlg = TPM2_ALG_SHA1;
    inPublic.publicArea.type = TPM2_ALG_KEYEDHASH;
    inPublic.publicArea.objectAttributes |= TPMA_OBJECT_SIGN_ENCRYPT;
    inPublic.publicArea.objectAttributes |= TPMA_OBJECT_SENSITIVEDATAORIGIN;
    inPublic.publicArea.parameters.keyedHashDetail.scheme.scheme = TPM2_ALG_HMAC;
    inPublic.publicArea.parameters.keyedHashDetail.scheme.details.hmac.hashAlg = TPM2_ALG_SHA1;

    LOG_INFO("Create keyedhash SHA1 HMAC");
    rc = TSS2_RETRY_EXP (Tss2_Sys_Create (sys_context,
                                          parent_handle,
                                          &sessions_cmd,
                                          &inSensitive,
                                          &inPublic,
                                          &outsideInfo,
                                          &creationPCR,
                                          &outPrivate,
                                          &outPublic,
                                          &creationData,
                                          &creationHash,
                                          &creationTicket,
                                          &sessions_rsp));
    if (rc == TPM2_RC_SUCCESS) {
        LOG_INFO("success");
    } else {
        LOG_ERROR("Create FAILED! Response Code : 0x%x", rc);
        return 1;
    }

    rc = Tss2_Sys_FlushContext(sys_context, parent_handle);
    if (rc != TSS2_RC_SUCCESS) {
        LOG_ERROR("Tss2_Sys_FlushContext failed with 0x%"PRIx32, rc);
        return 99; /* fatal error */
    }

    return 0;
}
