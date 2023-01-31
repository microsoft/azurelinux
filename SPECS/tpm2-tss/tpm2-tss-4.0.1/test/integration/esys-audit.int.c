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

#include "esys_iutil.h"
#include "test-esys.h"
#define LOGMODULE test
#include "util/log.h"
#include "util/aux_util.h"

/** This test is intended to test the ESYS audit commands.
 *
 * First a key for signing the audit digest is computed.
 * A audit session is started, and for the command GetCapability the
 * command audit digest and the session audit digest is computed.
 * (Esys_GetCommandAuditDigest, Esys_GetSessionAuditDigest). In the
 * last test the audit hash alg is changed with Esys_SetCommandCodeAuditStatus.
 *
 *\b Note: platform authorization needed.
 *
 * Tested ESYS commands:
 *  - Esys_CreatePrimary() (M)
 *  - Esys_FlushContext() (M)
 *  - Esys_GetCapability() (M)
 *  - Esys_GetCommandAuditDigest() (O)
 *  - Esys_GetSessionAuditDigest() (M)
 *  - Esys_SetCommandCodeAuditStatus() (O)
 *  - Esys_StartAuthSession() (M)
 *  - Esys_StartAuthSession() (M)
 *
 * @param[in,out] esys_context The ESYS_CONTEXT.
 * @retval EXIT_FAILURE
 * @retval EXIT_SKIP
 * @retval EXIT_SUCCESS
 */

int
test_esys_audit(ESYS_CONTEXT * esys_context)
{
    TSS2_RC r;
    ESYS_TR signHandle = ESYS_TR_NONE;
    ESYS_TR session = ESYS_TR_NONE;
    int failure_return = EXIT_FAILURE;

    TPM2B_PUBLIC *outPublic = NULL;
    TPM2B_CREATION_DATA *creationData = NULL;
    TPM2B_DIGEST *creationHash = NULL;
    TPMT_TK_CREATION *creationTicket = NULL;
    TPMS_CAPABILITY_DATA *capabilityData = NULL;
    TPM2B_ATTEST *auditInfo = NULL;
    TPMT_SIGNATURE *signature = NULL;

    /* Compute a signing key */
    TPM2B_AUTH authValuePrimary = {
        .size = 5,
        .buffer = {1, 2, 3, 4, 5}
    };

    TPM2B_SENSITIVE_CREATE inSensitivePrimary = {
        .size = 0,
        .sensitive = {
            .userAuth = {
                 .size = 0,
                 .buffer = {0},
             },
            .data = {
                 .size = 0,
                 .buffer = {0},
             },
        },
    };

    inSensitivePrimary.sensitive.userAuth = authValuePrimary;

    TPM2B_PUBLIC inPublic = {
            .size = 0,
            .publicArea = {
                .type = TPM2_ALG_RSA,
                .nameAlg = TPM2_ALG_SHA256,
                .objectAttributes = (
                    TPMA_OBJECT_USERWITHAUTH |
                    TPMA_OBJECT_RESTRICTED |
                    TPMA_OBJECT_SIGN_ENCRYPT |
                    TPMA_OBJECT_FIXEDTPM |
                    TPMA_OBJECT_FIXEDPARENT |
                    TPMA_OBJECT_SENSITIVEDATAORIGIN
                    ),
                .authPolicy = {
                        .size = 0,
                    },
                .parameters.rsaDetail = {
                    .symmetric = {
                        .algorithm = TPM2_ALG_NULL,
                        .keyBits.aes = 128,
                        .mode.aes = TPM2_ALG_CFB,
                        },
                    .scheme = {
                         .scheme = TPM2_ALG_RSASSA,
                         .details = { .rsassa = { .hashAlg = TPM2_ALG_SHA256 }},

                    },
                    .keyBits = 2048,
                    .exponent = 0,
                },
                .unique.rsa = {
                        .size = 0,
                        .buffer = {},
                    },
            },
        };

    TPM2B_AUTH authValue = {
                .size = 0,
                .buffer = {}
    };

    TPM2B_DATA outsideInfo = {
            .size = 0,
            .buffer = {},
    };

    TPML_PCR_SELECTION creationPCR = {
        .count = 0,
    };

    r = Esys_TR_SetAuth(esys_context, ESYS_TR_RH_OWNER, &authValue);
    goto_if_error(r, "Error: TR_SetAuth", error);

    r = Esys_CreatePrimary(esys_context, ESYS_TR_RH_OWNER, ESYS_TR_PASSWORD,
                           ESYS_TR_NONE, ESYS_TR_NONE, &inSensitivePrimary,
                           &inPublic, &outsideInfo, &creationPCR,
                           &signHandle, &outPublic, &creationData,
                           &creationHash, &creationTicket);
    goto_if_error(r, "Error esys create primary", error);

    /* Start a audit session */
    TPMA_SESSION sessionAttributes = TPMA_SESSION_CONTINUESESSION |
                                     TPMA_SESSION_AUDIT;
    TPM2_SE sessionType = TPM2_SE_HMAC;
    TPMI_ALG_HASH authHash = TPM2_ALG_SHA256;
    TPMT_SYM_DEF symmetric = {.algorithm = TPM2_ALG_NULL };

    r = Esys_StartAuthSession(esys_context, ESYS_TR_NONE, ESYS_TR_NONE,
                              ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE,
                              NULL,
                              sessionType, &symmetric, authHash, &session);

    goto_if_error(r, "Error Esys_StartAuthSession", error);
    r = Esys_TRSess_SetAttributes(esys_context, session, sessionAttributes,
                                  0xff);
    goto_if_error(r, "Error Esys_TRSess_SetAttributes", error);

    /* Execute one command to be audited */
    TPM2_CAP capability = TPM2_CAP_TPM_PROPERTIES;
    UINT32 property = TPM2_PT_LOCKOUT_COUNTER;
    UINT32 propertyCount = 1;
    TPMI_YES_NO moreData;

    r = Esys_GetCapability(esys_context,
                           session, ESYS_TR_NONE, ESYS_TR_NONE,
                           capability, property, propertyCount,
                           &moreData, &capabilityData);

    goto_if_error(r, "Error esys get capability", error);

    ESYS_TR privacyHandle = ESYS_TR_RH_ENDORSEMENT;
    TPM2B_DATA qualifyingData = {0};
    TPMT_SIG_SCHEME inScheme = { .scheme = TPM2_ALG_NULL };

    /* Test the audit commands */
    r = Esys_GetCommandAuditDigest(
        esys_context,
        privacyHandle,
        signHandle,
        ESYS_TR_PASSWORD,
        ESYS_TR_PASSWORD,
        ESYS_TR_NONE,
        &qualifyingData,
        &inScheme,
        &auditInfo,
        &signature);

    if ((r == TPM2_RC_COMMAND_CODE) ||
        (r == (TPM2_RC_COMMAND_CODE | TSS2_RESMGR_RC_LAYER)) ||
        (r == (TPM2_RC_COMMAND_CODE | TSS2_RESMGR_TPM_RC_LAYER))) {
        LOG_WARNING("Command TPM2_GetCommandAuditDigest not supported by TPM.");
        failure_return = EXIT_SKIP;
        goto error;
    }

    Esys_Free(auditInfo);
    Esys_Free(signature);

    goto_if_error(r, "Error: GetCommandAuditDigest", error);

    r = Esys_GetSessionAuditDigest(
        esys_context,
        privacyHandle,
        signHandle,
        session,
        ESYS_TR_PASSWORD,
        ESYS_TR_PASSWORD,
        ESYS_TR_NONE,
        &qualifyingData,
        &inScheme,
        &auditInfo,
        &signature);
    goto_if_error(r, "Error: GetSessionAuditDigest", error);

    TPMI_ALG_HASH auditAlg = TPM2_ALG_SHA256;
    TPML_CC clearList = {0};
    TPML_CC setList = {0};

    r = Esys_SetCommandCodeAuditStatus(
        esys_context,
        ESYS_TR_RH_PLATFORM,
        ESYS_TR_PASSWORD,
        ESYS_TR_NONE,
        ESYS_TR_NONE,
        auditAlg,
        &setList,
        &clearList);

    if (number_rc(r) == TPM2_RC_BAD_AUTH) {
        /* Platform authorization not possible test will be skipped */
        LOG_WARNING("Platform authorization not possible.");
        failure_return =  EXIT_SKIP;
        goto error;
    }

    goto_if_error(r, "Error: SetCommandCodeAuditStatus", error);

    r = Esys_FlushContext(esys_context, signHandle);
    goto_if_error(r, "Error: FlushContext", error);

    signHandle = ESYS_TR_NONE;

    r = Esys_FlushContext(esys_context, session);
    goto_if_error(r, "Error during FlushContext", error);

    Esys_Free(outPublic);
    Esys_Free(creationData);
    Esys_Free(creationHash);
    Esys_Free(creationTicket);
    Esys_Free(capabilityData);
    Esys_Free(auditInfo);
    Esys_Free(signature);
    return EXIT_SUCCESS;

 error:

    if (session != ESYS_TR_NONE) {
        if (Esys_FlushContext(esys_context, session) != TSS2_RC_SUCCESS) {
            LOG_ERROR("Cleanup session failed.");
        }
    }

    if (signHandle != ESYS_TR_NONE) {
        if (Esys_FlushContext(esys_context, signHandle) != TSS2_RC_SUCCESS) {
            LOG_ERROR("Cleanup signHandle failed.");
        }
    }
    Esys_Free(outPublic);
    Esys_Free(creationData);
    Esys_Free(creationHash);
    Esys_Free(creationTicket);
    Esys_Free(capabilityData);
    Esys_Free(auditInfo);
    Esys_Free(signature);
    return failure_return;
}

int
test_invoke_esys(ESYS_CONTEXT * esys_context) {
    return test_esys_audit(esys_context);
}
