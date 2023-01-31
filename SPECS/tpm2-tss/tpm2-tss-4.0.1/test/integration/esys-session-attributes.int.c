/* SPDX-License-Identifier: BSD-2-Clause */
/*******************************************************************************
 * Copyright 2017-2018, Fraunhofer SIT sponsored by Infineon Technologies AG
 * All rights reserved.
 *******************************************************************************/

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <stdlib.h>

#include "tss2_esys.h"
#include "tss2_mu.h"

#include "esys_iutil.h"
#define LOGDEFAULT LOGLEVEL_INFO
#define LOGMODULE test
#include "util/log.h"
#include "util/aux_util.h"

extern TSS2_RC
(*transmit_hook) (const uint8_t *command_buffer, size_t command_size);

size_t handles;
TPMA_SESSION session1_attributes;
static TSS2_RC
hookcheck_session1 (const uint8_t *command_buffer, size_t command_size);

/** Test encrypt / decrypt session flags propagation
 *
 * Testing that the command decrypt and response encrypt session flags that are
 * set in Esys are actually propagated to the TPM command's session flags, if
 * the command allows this. Using TPM2_CreatePrimary as a candidate.
 *
 * @param[in,out] esys_context The ESYS_CONTEXT.
 * @retval EXIT_FAILURE
 * @retval EXIT_SUCCESS
 */
int
test_esys_session_attributes(ESYS_CONTEXT * esys_context)
{
    TSS2_RC r;
    ESYS_TR objectHandle = ESYS_TR_NONE;
    ESYS_TR session = ESYS_TR_NONE;
    TPM2B_DIGEST *rdata = NULL;

    TPMT_SYM_DEF symmetric = {.algorithm = TPM2_ALG_XOR,
                              .keyBits = { .exclusiveOr = TPM2_ALG_SHA256 },
                              .mode = {.aes = TPM2_ALG_CFB}};

    TPM2B_SENSITIVE_CREATE inSensitive = {
        .size = 0,
        .sensitive = {
            .userAuth = {
                 .size = 0,
                 .buffer = {0}
                 ,
             },
            .data = {
                 .size = 0,
                 .buffer = {0}
             }
        }
    };

    TPM2B_PUBLIC inPublic = {
        .size = 0,
        .publicArea = {
            .type = TPM2_ALG_RSA,
            .nameAlg = TPM2_ALG_SHA256,
            .objectAttributes = (TPMA_OBJECT_USERWITHAUTH |
                                 TPMA_OBJECT_RESTRICTED |
                                 TPMA_OBJECT_DECRYPT |
                                 TPMA_OBJECT_FIXEDTPM |
                                 TPMA_OBJECT_FIXEDPARENT |
                                 TPMA_OBJECT_SENSITIVEDATAORIGIN),
            .authPolicy = {
                 .size = 0,
             },
            .parameters.rsaDetail = {
                 .symmetric = {
                     .algorithm = TPM2_ALG_AES,
                     .keyBits.aes = 128,
                     .mode.aes = TPM2_ALG_CFB,
                 },
                 .scheme = {
                      .scheme =
                      TPM2_ALG_NULL,
                  },
                 .keyBits = 2048,
                 .exponent = 0,
             },
            .unique.rsa = {
                 .size = 0,
                 .buffer = {}
                 ,
             }
        }
    };

    TPM2B_DATA outsideInfo = {
        .size = 0,
        .buffer = {}
        ,
    };

    TPML_PCR_SELECTION creationPCR = {
        .count = 0,
    };

    r = Esys_StartAuthSession(esys_context, ESYS_TR_NONE, ESYS_TR_NONE,
                              ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE,
                              NULL,
                              TPM2_SE_HMAC, &symmetric, TPM2_ALG_SHA256,
                              &session);
    goto_if_error(r, "Error: During initialization of session", error);

    /* Testing Encrypt and Decrypt, both set */
    r = Esys_TRSess_SetAttributes(esys_context, session,
                                  TPMA_SESSION_DECRYPT | TPMA_SESSION_ENCRYPT,
                                  TPMA_SESSION_DECRYPT | TPMA_SESSION_ENCRYPT);
    goto_if_error(r, "Error: During initialization of attributes", error);

    handles = 1;
    session1_attributes = TPMA_SESSION_CONTINUESESSION | TPMA_SESSION_DECRYPT |
                          TPMA_SESSION_ENCRYPT;
    transmit_hook = hookcheck_session1;

    r = Esys_CreatePrimary(esys_context, ESYS_TR_RH_OWNER, session,
                           ESYS_TR_NONE, ESYS_TR_NONE, &inSensitive, &inPublic,
                           &outsideInfo, &creationPCR, &objectHandle,
                           NULL, NULL, NULL, NULL);
    transmit_hook = NULL;
    goto_if_error(r, "Error esys create primary", error);

    r = Esys_FlushContext(esys_context, objectHandle);
    goto_if_error(r, "Error during FlushContext", error);

    r = Esys_FlushContext(esys_context, session);
    goto_if_error(r, "Flushing context", error);

    /* Testing only Encrypt, i.e. responses, set */
    r = Esys_StartAuthSession(esys_context, ESYS_TR_NONE, ESYS_TR_NONE,
                              ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE,
                              NULL,
                              TPM2_SE_HMAC, &symmetric, TPM2_ALG_SHA256,
                              &session);
    goto_if_error(r, "Error: During initialization of session", error);

    r = Esys_TRSess_SetAttributes(esys_context, session,
                                  TPMA_SESSION_ENCRYPT,
                                  TPMA_SESSION_DECRYPT | TPMA_SESSION_ENCRYPT);
    goto_if_error(r, "Error: During initialization of attributes", error);

    handles = 0;
    session1_attributes = TPMA_SESSION_CONTINUESESSION | TPMA_SESSION_ENCRYPT;
    transmit_hook = hookcheck_session1;

    r = Esys_GetRandom(esys_context, session, ESYS_TR_NONE, ESYS_TR_NONE,
                       10, &rdata);
    Esys_Free(rdata);
    transmit_hook = NULL;
    goto_if_error(r, "Error esys create primary", error);

    transmit_hook = hookcheck_session1;

    r = Esys_GetRandom(esys_context, session, ESYS_TR_NONE, ESYS_TR_NONE,
                       10, &rdata);
    transmit_hook = NULL;
    goto_if_error(r, "Error esys create primary", error);

    LOGBLOB_INFO(&rdata->buffer[0], rdata->size, "rdata");

    /* Cleanup */
    r = Esys_FlushContext(esys_context, session);
    goto_if_error(r, "Flushing context", error);

    Esys_Free(rdata);
    return EXIT_SUCCESS;

 error:
    LOG_ERROR("\nError Code: %x\n", r);

    if (session != ESYS_TR_NONE) {
        if (Esys_FlushContext(esys_context, session) != TSS2_RC_SUCCESS) {
            LOG_ERROR("Cleanup session failed.");
        }
    }

    if (objectHandle != ESYS_TR_NONE) {
        if (Esys_FlushContext(esys_context, objectHandle) != TSS2_RC_SUCCESS) {
            LOG_ERROR("Cleanup objectHandle failed.");
        }
    }

    Esys_Free(rdata);
    return EXIT_FAILURE;
}

int
test_invoke_esys(ESYS_CONTEXT * esys_context) {
    return test_esys_session_attributes(esys_context);
}

static TSS2_RC
hookcheck_session1 (const uint8_t *command_buffer, size_t command_size)
{
    TSS2_RC r;
    size_t offset = 10; /* header */;
    TPM2_ST tag;
    TPMS_AUTH_COMMAND session1;

    LOGBLOB_INFO(command_buffer, command_size, "command");

    r = Tss2_MU_UINT16_Unmarshal(command_buffer, command_size, NULL, &tag);
    return_if_error(r, "Unmarshalling AuthSize failed");
    if (tag != TPM2_ST_SESSIONS) {
        LOG_ERROR("Bad Tag. Expected TPM2_ST_SESSION Got: 0x%04x", tag);
        return TSS2_TCTI_RC_BAD_VALUE;
    }

    offset += sizeof(TPM2_HANDLE) * handles;

    /* TPM2_AUTHORIZATION_SIZE authorizationSize */
    r = Tss2_MU_UINT32_Unmarshal(command_buffer, command_size, &offset, NULL);
    return_if_error(r, "Unmarshalling AuthSize failed");

    r = Tss2_MU_TPMS_AUTH_COMMAND_Unmarshal(command_buffer, command_size, &offset,
                                         &session1);
    return_if_error(r, "Unmarshalling first session failed");

    if (session1.sessionAttributes != session1_attributes) {
        LOG_ERROR("Session Attribute mismatch. Expected: 0x%08x Got: 0x%08x",
                  session1_attributes, session1.sessionAttributes);
        return TSS2_TCTI_RC_BAD_VALUE;
    }

    return TSS2_RC_SUCCESS;
}
