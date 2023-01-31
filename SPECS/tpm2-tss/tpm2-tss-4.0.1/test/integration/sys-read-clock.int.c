/* SPDX-License-Identifier: BSD-2-Clause */
/***********************************************************************
 * Copyright (c) 2020, Intel Corporation
 *
 * All rights reserved.
 ***********************************************************************/
#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <inttypes.h>
#include <stdio.h>
#include <stdlib.h>

#include "tss2_sys.h"

#define LOGMODULE test
#include "util/log.h"
#include "test.h"

#define EXIT_SKIP 77
/*
 * This is an incredibly simple test to create the most simple session
 * (which ends up being a trial policy) and then just tear it down.
 */
int
test_invoke (TSS2_SYS_CONTEXT *sys_context)
{
    TSS2_RC rc, rc2;
    TPM2B_NONCE nonce_caller = {
        .size   = TPM2_SHA1_DIGEST_SIZE,
        .buffer = {
                0xde, 0xad, 0xbe, 0xef, 0xde, 0xad, 0xbe, 0xef,
                0xde, 0xad, 0xbe, 0xef, 0xde, 0xad, 0xbe, 0xef,
                0xde, 0xad, 0xbe, 0xef,
            }
    };
    TPM2B_NONCE nonce_tpm = {
        .size   = TPM2_SHA1_DIGEST_SIZE,
        .buffer = { 0 }
    };
    TPM2B_ENCRYPTED_SECRET encrypted_salt = { 0 };
    TPMI_SH_AUTH_SESSION   session = 0;
    TPMT_SYM_DEF symmetric = { .algorithm = TPM2_ALG_NULL  };

    LOG_INFO("StartAuthSession for TPM2_SE_POLICY (policy session)");
    rc = Tss2_Sys_StartAuthSession (sys_context,
                                    TPM2_RH_NULL,
                                    TPM2_RH_NULL,
                                    NULL,
                                    &nonce_caller,
                                    &encrypted_salt,
                                    TPM2_SE_HMAC,
                                    &symmetric,
                                    TPM2_ALG_SHA1,
                                    &session,
                                    &nonce_tpm,
                                    NULL);
    if (rc != TSS2_RC_SUCCESS) {
        LOG_ERROR("Tss2_Sys_StartAuthSession failed: 0x%" PRIx32, rc);
        exit(1);
    }
    LOG_INFO("StartAuthSession for TPM2_SE_POLICY success! Session handle: "
               "0x%" PRIx32, session);

    rc = Tss2_Sys_ReadClock_Prepare(sys_context);
    if (rc != TSS2_RC_SUCCESS) {
        LOG_ERROR("Tss2_Sys_ReadClock_Prepare failed: 0x%" PRIx32, rc);
	goto error;
    }

    TSS2L_SYS_AUTH_COMMAND auths = {0};
    auths.auths[0].sessionHandle = session;
    auths.auths[0].sessionAttributes = TPMA_SESSION_AUDIT |
                                       TPMA_SESSION_CONTINUESESSION;
    auths.count = 1;

    rc = Tss2_Sys_SetCmdAuths(sys_context, &auths);
    if (rc != TSS2_RC_SUCCESS) {
        LOG_ERROR("Tss2_Sys_SetCmdAuths failed: 0x%" PRIx32, rc);
	goto error;
    }

    rc = Tss2_Sys_Execute(sys_context);
    /* TPMs before Revision 1.38 might not support session usage*/
    if ((rc == TPM2_RC_AUTH_CONTEXT ) ||
        (rc == (TPM2_RC_AUTH_CONTEXT  | TSS2_RESMGR_RC_LAYER)) ||
        (rc == (TPM2_RC_AUTH_CONTEXT  | TSS2_RESMGR_TPM_RC_LAYER))) {
        LOG_WARNING("Session usage not supported by TPM.");
        rc = EXIT_SKIP;
        goto error;
    }

    if (rc != TSS2_RC_SUCCESS) {
        LOG_ERROR("Tss2_Sys_ExecuteAsync failed: 0x%" PRIx32, rc);
	goto error;
    }

    TPMS_TIME_INFO time;

    rc = Tss2_Sys_ReadClock_Complete(sys_context, &time);
    if (rc != TSS2_RC_SUCCESS) {
        LOG_ERROR("Tss2_Sys_ReadClock_Complete failed: 0x%" PRIx32, rc);
	goto error;
    }

error:
    rc2 = Tss2_Sys_FlushContext (sys_context, session);
    if (rc2 != TSS2_RC_SUCCESS) {
        LOG_ERROR("Tss2_Sys_FlushContext failed: 0x%" PRIx32, rc);
	return rc2;
    }
    return rc;
}
