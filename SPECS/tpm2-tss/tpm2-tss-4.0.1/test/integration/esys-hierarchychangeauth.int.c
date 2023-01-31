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
#define LOGMODULE test
#include "util/log.h"
#include "util/aux_util.h"

/** This test is intended to test the change of an authorization value of
 *  a hierarchy.
 *
 * To check whether the change was successful a primary key is created
 * with the handle of this hierarchy and the new authorization.
 * Also second primary is created after a call of Esys_TR_SetAuth with
 * the new auth value.
 *
 * Tested ESYS commands:
 *  - Esys_CreatePrimary() (M)
 *  - Esys_FlushContext() (M)
 *  - Esys_HierarchyChangeAuth() (M)
 *
 * @param[in,out] esys_context The ESYS_CONTEXT.
 * @retval EXIT_FAILURE
 * @retval EXIT_SUCCESS
 */

int
test_esys_hierarchychangeauth(ESYS_CONTEXT * esys_context)
{
    TSS2_RC r;
    ESYS_TR primaryHandle = ESYS_TR_NONE;
    bool auth_changed = false;
    ESYS_TR authHandle_handle = ESYS_TR_RH_OWNER;

    TPM2B_PUBLIC *outPublic = NULL;
    TPM2B_CREATION_DATA *creationData = NULL;
    TPM2B_DIGEST *creationHash = NULL;
    TPMT_TK_CREATION *creationTicket = NULL;

    TPM2B_AUTH newAuth = {
        .size = 5,
        .buffer = {1, 2, 3, 4, 5}
    };

    TPM2B_AUTH emptyAuth = {
        .size = 0,
        .buffer = {}
    };

    r = Esys_HierarchyChangeAuth(esys_context,
                                 authHandle_handle,
                                 ESYS_TR_PASSWORD,
                                 ESYS_TR_NONE,
                                 ESYS_TR_NONE,
                                 &newAuth);
    goto_if_error(r, "Error: HierarchyChangeAuth", error);

    auth_changed = true;

    TPM2B_SENSITIVE_CREATE inSensitivePrimary = {
        .size = 0,
        .sensitive = {
            .userAuth = {
                 .size = 0,
                .buffer = {0 },
             },
            .data = {
                 .size = 0,
                .buffer = {0},
             },
        },
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
                     .mode.aes = TPM2_ALG_CFB},
                 .scheme = {
                      .scheme = TPM2_ALG_NULL
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
    LOG_INFO("\nRSA key will be created.");

    TPM2B_DATA outsideInfo = {
        .size = 0,
        .buffer = {},
    };

    TPML_PCR_SELECTION creationPCR = {
        .count = 0,
    };

    goto_if_error(r, "Error: TR_SetAuth", error);

    r = Esys_CreatePrimary(esys_context, ESYS_TR_RH_OWNER, ESYS_TR_PASSWORD,
                           ESYS_TR_NONE, ESYS_TR_NONE, &inSensitivePrimary, &inPublic,
                           &outsideInfo, &creationPCR, &primaryHandle,
                           &outPublic, &creationData, &creationHash,
                           &creationTicket);
    goto_if_error(r, "Error esys create primary", error);

    r = Esys_FlushContext(esys_context, primaryHandle);
    goto_if_error(r, "Flushing context", error);

    primaryHandle = ESYS_TR_NONE;

    r = Esys_TR_SetAuth(esys_context, ESYS_TR_RH_OWNER, &newAuth);
    goto_if_error(r, "Error SetAuth", error);

    Esys_Free(outPublic);
    Esys_Free(creationData);
    Esys_Free(creationHash);
    Esys_Free(creationTicket);

    /* Check whether HierarchyChangeAuth with auth equal NULL works */

    r = Esys_CreatePrimary(esys_context, ESYS_TR_RH_OWNER, ESYS_TR_PASSWORD,
                           ESYS_TR_NONE, ESYS_TR_NONE, &inSensitivePrimary, &inPublic,
                           &outsideInfo, &creationPCR, &primaryHandle,
                           &outPublic, &creationData, &creationHash,
                           &creationTicket);
    goto_if_error(r, "Error esys create primary", error);

    r = Esys_FlushContext(esys_context, primaryHandle);
    goto_if_error(r, "Flushing context", error);

    r = Esys_HierarchyChangeAuth(esys_context,
                                 authHandle_handle,
                                 ESYS_TR_PASSWORD,
                                 ESYS_TR_NONE,
                                 ESYS_TR_NONE,
                                 NULL);
    goto_if_error(r, "Error: HierarchyChangeAuth", error);

    Esys_Free(outPublic);
    Esys_Free(creationData);
    Esys_Free(creationHash);
    Esys_Free(creationTicket);
    return EXIT_SUCCESS;

error:

    if (primaryHandle != ESYS_TR_NONE) {
        if (Esys_FlushContext(esys_context, primaryHandle) != TSS2_RC_SUCCESS) {
            LOG_ERROR("Cleanup primaryHandle failed.");
        }
    }

    if (auth_changed) {
        if (Esys_TR_SetAuth(esys_context, ESYS_TR_RH_OWNER, &newAuth) != TSS2_RC_SUCCESS) {
            LOG_ERROR("Error SetAuth");
        }
        if (Esys_HierarchyChangeAuth(esys_context,
                                     authHandle_handle,
                                     ESYS_TR_PASSWORD,
                                     ESYS_TR_NONE,
                                     ESYS_TR_NONE,
                                     &emptyAuth) != TSS2_RC_SUCCESS) {
            LOG_ERROR("Error: HierarchyChangeAuth");
        }
    }

    Esys_Free(outPublic);
    Esys_Free(creationData);
    Esys_Free(creationHash);
    Esys_Free(creationTicket);
    return EXIT_FAILURE;
}

int
test_invoke_esys(ESYS_CONTEXT * esys_context) {
    return test_esys_hierarchychangeauth(esys_context);
}
