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

/** This test is intended to test Esys_Commit.
 *   based on an ECC key
 * created with Esys_CreatePrimary Esys_Commit is called with a point
 * from the primary key.
 *
 * Tested ESYS commands:
 *  - Esys_Commit() (M)
 *  - Esys_CreatePrimary() (M)
 *  - Esys_FlushContext() (M)
 *  - Esys_StartAuthSession() (M)
 *
 * @param[in,out] esys_context The ESYS_CONTEXT.
 * @retval EXIT_FAILURE
 * @retval EXIT_SKIP
 * @retval EXIT_SUCCESS
 */

int
test_esys_commit(ESYS_CONTEXT * esys_context)
{
    TSS2_RC r;
    ESYS_TR eccHandle = ESYS_TR_NONE;
    ESYS_TR session = ESYS_TR_NONE;
    int failure_return = EXIT_FAILURE;

    TPM2B_PUBLIC *outPublic = NULL;
    TPM2B_CREATION_DATA *creationData = NULL;
    TPM2B_DIGEST *creationHash = NULL;
    TPMT_TK_CREATION *creationTicket = NULL;

    TPM2B_ECC_POINT *K = NULL;
    TPM2B_ECC_POINT *L = NULL;
    TPM2B_ECC_POINT *E = NULL;

    TPMT_SYM_DEF symmetric = {
        .algorithm = TPM2_ALG_AES,
        .keyBits = { .aes = 128 },
        .mode = {.aes = TPM2_ALG_CFB}
    };
    TPMA_SESSION sessionAttributes;
    TPM2B_NONCE nonceCaller = {
        .size = 20,
        .buffer = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20}
    };

    memset(&sessionAttributes, 0, sizeof sessionAttributes);

    r = Esys_StartAuthSession(esys_context, ESYS_TR_NONE, ESYS_TR_NONE,
                              ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE,
                              &nonceCaller,
                              TPM2_SE_HMAC, &symmetric, TPM2_ALG_SHA256,
                              &session);

    goto_if_error(r, "Error: During initialization of session", error);

    TPM2B_SENSITIVE_CREATE inSensitive = {
        .size = 0,
        .sensitive = {
            .userAuth = {
                 .size = 0,
                 .buffer = {0}
             },
            .data = {
                 .size = 0,
                 .buffer = {0}
             }
        }
    };
    TPM2B_PUBLIC inPublicECC = {
        .size = 0,
        .publicArea = {
            .type = TPM2_ALG_ECC,
            .nameAlg = TPM2_ALG_SHA256,
            .objectAttributes = (TPMA_OBJECT_USERWITHAUTH |
                                 TPMA_OBJECT_SIGN_ENCRYPT |
                                 TPMA_OBJECT_FIXEDTPM |
                                 TPMA_OBJECT_FIXEDPARENT |
                                 TPMA_OBJECT_SENSITIVEDATAORIGIN),
            .authPolicy = {
                 .size = 0,
             },
            .parameters.eccDetail = {
                 .symmetric = {
                     .algorithm = TPM2_ALG_NULL,
                     .keyBits.aes = 128,
                     .mode.aes = TPM2_ALG_CFB,
                 },
                 .scheme = {
                      .scheme = TPM2_ALG_ECDAA,
                      .details = {.ecdh = {.hashAlg = TPM2_ALG_SHA256}
                      }
                  },
                 .curveID = TPM2_ECC_NIST_P256,
                 .kdf = {.scheme = TPM2_ALG_NULL }
             },
            .unique.ecc = {
                 .x = {.size = 0,.buffer = {}},
                 .y = {.size = 0,.buffer = {}}
             }
            ,
        }
    };
    LOG_INFO("\nECC key will be created.");
    TPM2B_PUBLIC inPublic = inPublicECC;

    TPM2B_DATA outsideInfo = {
        .size = 0,
        .buffer = {}
        ,
    };

    TPML_PCR_SELECTION creationPCR = {
        .count = 0,
    };

    TPM2B_AUTH authValue = {
        .size = 0,
        .buffer = {}
    };

    r = Esys_TR_SetAuth(esys_context, ESYS_TR_RH_OWNER, &authValue);
    goto_if_error(r, "Error: TR_SetAuth", error);

    r = Esys_CreatePrimary(esys_context, ESYS_TR_RH_OWNER, session,
                           ESYS_TR_NONE, ESYS_TR_NONE, &inSensitive, &inPublic,
                           &outsideInfo, &creationPCR, &eccHandle,
                           &outPublic, &creationData, &creationHash,
                           &creationTicket);

    if (base_rc(r) == (TPM2_RC_SCHEME | TPM2_RC_P | TPM2_RC_2)) {
        LOG_WARNING("Scheme ECDAA not supported by TPM.");
        failure_return = EXIT_SKIP;
        goto error;
    }

    goto_if_error(r, "Error esys create primary", error);

    TPM2B_ECC_POINT P1 = {0};
    TPM2B_SENSITIVE_DATA s2 = {0};
    TPM2B_ECC_PARAMETER y2 = {0};
    UINT16 counter;
    r = Esys_Commit(esys_context, eccHandle,
                    session, ESYS_TR_NONE, ESYS_TR_NONE,
                    &P1, &s2, &y2,
                    &K, &L, &E, &counter);
    goto_if_error(r, "Error: Commit", error);

    r = Esys_FlushContext(esys_context, eccHandle);
    goto_if_error(r, "Flushing context", error);

    eccHandle = ESYS_TR_NONE;

    r = Esys_FlushContext(esys_context, session);
    goto_if_error(r, "Error: FlushContext", error);

    session = ESYS_TR_NONE;

    Esys_Free(outPublic);
    Esys_Free(creationData);
    Esys_Free(creationHash);
    Esys_Free(creationTicket);
    Esys_Free(K);
    Esys_Free(L);
    Esys_Free(E);
    return EXIT_SUCCESS;

 error:
    LOG_ERROR("\nError Code: %x\n", r);

    if (eccHandle != ESYS_TR_NONE) {
        if (Esys_FlushContext(esys_context, eccHandle) != TSS2_RC_SUCCESS) {
            LOG_ERROR("Cleanup eccHandle failed.");
        }
    }

    if (session != ESYS_TR_NONE) {
        if (Esys_FlushContext(esys_context, session) != TSS2_RC_SUCCESS) {
            LOG_ERROR("Cleanup session failed.");
        }
    }

    Esys_Free(outPublic);
    Esys_Free(creationData);
    Esys_Free(creationHash);
    Esys_Free(creationTicket);
    Esys_Free(K);
    Esys_Free(L);
    Esys_Free(E);
    return failure_return;
}

int
test_invoke_esys(ESYS_CONTEXT * esys_context) {
    return test_esys_commit(esys_context);
}
