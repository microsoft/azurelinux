/* SPDX-License-Identifier: BSD-2-Clause */
/*******************************************************************************
 * Copyright 2017-2019, Intel Corporation
 * All rights reserved.
 *******************************************************************************/

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <stdlib.h>
#include "tss2_esys.h"
#include "esys_iutil.h"
#define LOGMODULE test
#include "util/log.h"
#include "util/aux_util.h"

/** This test is intended to test auto adjust and restore session flags in ESYS
 *
 * Tested ESYS commands:
 *  - Esys_FlushContext() (M)
 *  - Esys_NV_DefineSpace() (M)
 *  - Esys_NV_Read() (M)
 *  - Esys_NV_Write() (M)
 *  - Esys_NV_UndefineSpace() (M)
 *  - Esys_StartAuthSession() (M)
 *
 * @param[in,out] esys_context The ESYS_CONTEXT.
 * @retval EXIT_FAILURE
 * @retval EXIT_SUCCESS
 */

int
test_esys_auto_flags(ESYS_CONTEXT * esys_context)
{

    TSS2_RC r;
    int test_ret = EXIT_SUCCESS ;
    ESYS_TR nvHandle = ESYS_TR_NONE;
    ESYS_TR session_auth = ESYS_TR_NONE;
    ESYS_TR session_enc = ESYS_TR_NONE;
    TPMT_SYM_DEF symmetric = {.algorithm = TPM2_ALG_AES,
                              .keyBits = {.aes = 128},
                              .mode = {.aes = TPM2_ALG_CFB}
    };

    TPM2B_NONCE nonceCaller = {
        .size = 20,
        .buffer = { 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,11, 12, 13, 14, 15, 16, 17,
                    18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32}
    };

    /* Auth session */
    r = Esys_StartAuthSession(esys_context, ESYS_TR_NONE, ESYS_TR_NONE,
                              ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE,
                              &nonceCaller,
                              TPM2_SE_HMAC, &symmetric, TPM2_ALG_SHA256,
                              &session_auth);
    goto_if_error(r, "Error: During initialization of session_auth", error);

    /* Enc param session */
    r = Esys_StartAuthSession(esys_context, ESYS_TR_NONE, ESYS_TR_NONE,
                              ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE,
                              &nonceCaller,
                              TPM2_SE_HMAC, &symmetric, TPM2_ALG_SHA256,
                              &session_enc);
    goto_if_error(r, "Error: During initialization of session_enc", error);

    /* Set both ENC and DEC flags for the enc session */
    TPMA_SESSION sessionAttributes = TPMA_SESSION_DECRYPT |
                                     TPMA_SESSION_ENCRYPT |
                                     TPMA_SESSION_CONTINUESESSION;

    r = Esys_TRSess_SetAttributes(esys_context, session_enc, sessionAttributes, 0xFF);
    goto_if_error(r, "Error: During SetAttributes", error);

    TPM2B_AUTH auth = {.size = 20,
                       .buffer={10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
                                20, 21, 22, 23, 24, 25, 26, 27, 28, 29}};

    TPM2B_NV_PUBLIC publicInfo = {
        .size = 0,
        .nvPublic = {
            .nvIndex =TPM2_NV_INDEX_FIRST,
            .nameAlg = TPM2_ALG_SHA256,
            .attributes = (
                TPMA_NV_OWNERWRITE |
                TPMA_NV_AUTHWRITE |
                TPMA_NV_WRITE_STCLEAR |
                TPMA_NV_READ_STCLEAR |
                TPMA_NV_AUTHREAD |
                TPMA_NV_OWNERREAD
                ),
            .authPolicy = {
                 .size = 0,
                 .buffer = {},
             },
            .dataSize = 20,
        }
    };

    r = Esys_NV_DefineSpace (
        esys_context,
        ESYS_TR_RH_OWNER,
        session_auth,
        ESYS_TR_NONE,
        ESYS_TR_NONE,
        &auth,
        &publicInfo,
        &nvHandle);
    goto_if_error(r, "Error esys define nv space", error);

    TPM2B_MAX_NV_BUFFER nv_test_data = { .size = 20,
                                         .buffer={0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0,
                                                  1, 2, 3, 4, 5, 6, 7, 8, 9}};
    const TPM2B_MAX_NV_BUFFER *nv_test_data_ptr = &nv_test_data;

    /* NV_Write cmd does not support TPMA_SESSION_ENCRYPT - the flag should
     * be auto cleared by ESYS */
    r = Esys_NV_Write(
        esys_context,
        nvHandle,
        nvHandle,
        session_enc,
        ESYS_TR_NONE,
        ESYS_TR_NONE,
        nv_test_data_ptr,
        0);
    goto_if_error(r, "Error esys nv write", error);

    /* Verify that the same session flags are still set after the test */
    TPMA_SESSION sessionAttributesVerify;
    r = Esys_TRSess_GetAttributes(esys_context, session_enc,
                                  &sessionAttributesVerify);
    goto_if_error(r, "Error: During GetAttributes", error);

    if (sessionAttributes != sessionAttributesVerify) {
        LOG_ERROR("Session flags not equal after write %x, %x",
                  sessionAttributes, sessionAttributesVerify);
        r = TSS2_ESYS_RC_GENERAL_FAILURE;
        goto_if_error(r, "Error esys nv write", error);
    }

    TPM2B_MAX_NV_BUFFER *data;

    /* NV_Read cmd does not support TPMA_SESSION_DECRYPT - the flags should
     * be auto cleared by ESYS */
    r = Esys_NV_Read(
        esys_context,
        nvHandle,
        nvHandle,
        session_enc,
        ESYS_TR_NONE,
        ESYS_TR_NONE,
        20, 0, &data);
    goto_if_error(r, "Error: nv read", error);
    free(data);

    /* Verify that the same session flags are still set after the test */
    r = Esys_TRSess_GetAttributes(esys_context, session_enc,
                                  &sessionAttributesVerify);
    goto_if_error(r, "Error: During GetAttributes", error);

    if (sessionAttributes != sessionAttributesVerify) {
        LOG_ERROR("Session flags not equal after read %x, %x",
                  sessionAttributes, sessionAttributesVerify);
       r = TSS2_ESYS_RC_GENERAL_FAILURE;
    }

 error:
    if (r)
        test_ret = EXIT_FAILURE;

    if (nvHandle != ESYS_TR_NONE) {
        if (Esys_NV_UndefineSpace(esys_context,
                                  ESYS_TR_RH_OWNER,
                                  nvHandle,
                                  session_auth,
                                  ESYS_TR_NONE,
                                  ESYS_TR_NONE) != TSS2_RC_SUCCESS) {
            LOG_ERROR("Cleanup nvHandle failed.");
        }
    }

    if (session_auth != ESYS_TR_NONE) {
        if (Esys_FlushContext(esys_context, session_auth) != TSS2_RC_SUCCESS) {
            LOG_ERROR("Cleanup session_auth failed.");
        }
    }
    if (session_enc != ESYS_TR_NONE) {
        if (Esys_FlushContext(esys_context, session_enc) != TSS2_RC_SUCCESS) {
            LOG_ERROR("Cleanup session_enc failed.");
        }
    }

    return test_ret;
}

int
test_invoke_esys(ESYS_CONTEXT * esys_context) {
    return test_esys_auto_flags(esys_context);
}
