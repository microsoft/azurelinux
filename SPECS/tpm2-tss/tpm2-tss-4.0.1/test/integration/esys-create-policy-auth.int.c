/* SPDX-License-Identifier: BSD-2-Clause */

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <stdlib.h>

#include "tss2_esys.h"

#include "esys_iutil.h"
#define LOGMODULE test
#include "util/log.h"
#include "util/aux_util.h"

/** This test is intended to test policy authentication for the ESYS command
 *  Create.
 *
 * We start by creating a primary key with a password and policy.
 * Based in the primary a second key will be created using the prinary key's
 * policy for authorization.
 *
 * Tested ESYS commands:
 *  - Esys_StartAuthSession() (M)
 *  - Esys_PolicyCommandCode() (M)
 *  - Esys_PolicyGetDigest() (M)
 *  - Esys_FlushContext() (M)
 *  - Esys_CreatePrimary() (M)
 *  - Esys_Create() (M)
 *
 * Used compiler defines: TEST_ECC
 *
 * @param[in,out] esys_context The ESYS_CONTEXT.
 * @retval EXIT_FAILURE
 * @retval EXIT_SUCCESS
 */

int
test_esys_create_policy_auth(ESYS_CONTEXT * esys_context)
{
    TSS2_RC r;
    ESYS_TR primaryHandle = ESYS_TR_NONE;
    ESYS_TR trialHandle = ESYS_TR_NONE;
    ESYS_TR policyHandle = ESYS_TR_NONE;

    TPM2B_DIGEST *trialDigest = NULL;
    TPM2B_PUBLIC *outPublic = NULL;
    TPM2B_PUBLIC *outPublic2 = NULL;
    TPM2B_PRIVATE *outPrivate2 = NULL;

    TPMT_SYM_DEF policyAlgo = {
        .algorithm = TPM2_ALG_AES,
        .keyBits.aes = 128,
        .mode.aes = TPM2_ALG_CFB,
    };

    r = Esys_StartAuthSession(esys_context, ESYS_TR_NONE, ESYS_TR_NONE,
                              ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE,
                              NULL, TPM2_SE_TRIAL, &policyAlgo,
                              TPM2_ALG_SHA256, &trialHandle);
    goto_if_error(r, "Error esys start trial session", error);

    r = Esys_PolicyCommandCode(esys_context, trialHandle, ESYS_TR_NONE,
                               ESYS_TR_NONE, ESYS_TR_NONE, TPM2_CC_Create);
    goto_if_error(r, "Error esys policy command code", error);

    r = Esys_PolicyGetDigest(esys_context, trialHandle, ESYS_TR_NONE,
                             ESYS_TR_NONE, ESYS_TR_NONE, &trialDigest);
    goto_if_error(r, "Error esys policy get digest", error);

    r = Esys_FlushContext(esys_context, trialHandle);
    goto_if_error(r, "Error esys flush context", error);

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

#ifdef TEST_ECC
    TPM2B_PUBLIC inPublic = {
        .size = 0,
        .publicArea = {
            .type = TPM2_ALG_ECC,
            .nameAlg = TPM2_ALG_SHA256,
            .objectAttributes = (TPMA_OBJECT_USERWITHAUTH |
                                 TPMA_OBJECT_RESTRICTED |
                                 TPMA_OBJECT_DECRYPT |
                                 TPMA_OBJECT_FIXEDTPM |
                                 TPMA_OBJECT_FIXEDPARENT |
                                 TPMA_OBJECT_SENSITIVEDATAORIGIN),
            .authPolicy = *trialDigest,
            .parameters.eccDetail = {
                 .symmetric = {
                     .algorithm = TPM2_ALG_NULL,
                     .keyBits.aes = 128,
                     .mode.aes = TPM2_ALG_CFB,
                 },
                 .scheme = {
                      .scheme = TPM2_ALG_ECDSA,
                      .details = {
                          .ecdsa = {.hashAlg  = TPM2_ALG_SHA256}},
                  },
                 .curveID = TPM2_ECC_NIST_P256,
                 .kdf = {
                      .scheme = TPM2_ALG_NULL,
                      .details = {}}
             },
            .unique.ecc = {
                 .x = {.size = 0,.buffer = {}},
                 .y = {.size = 0,.buffer = {}},
             },
        },
    };
    LOG_INFO("\nECC key will be created.");
#else
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
            .authPolicy = *trialDigest,
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
#endif /* TEST_ECC */

    TPM2B_DATA outsideInfo = {
        .size = 0,
        .buffer = {},
    };

    TPML_PCR_SELECTION creationPCR = {
        .count = 0,
    };

    r = Esys_CreatePrimary(esys_context, ESYS_TR_RH_OWNER, ESYS_TR_PASSWORD,
                           ESYS_TR_NONE, ESYS_TR_NONE,
                           &inSensitivePrimary, &inPublic,
                           &outsideInfo, &creationPCR, &primaryHandle,
                           &outPublic, NULL, NULL, NULL);
    goto_if_error(r, "Error esys create primary", error);

    LOG_INFO("Created Primary Key");

    r = Esys_TR_SetAuth(esys_context, primaryHandle, &authValuePrimary);
    goto_if_error(r, "Error: TR_SetAuth", error);

    r = Esys_StartAuthSession(esys_context, ESYS_TR_NONE, ESYS_TR_NONE,
                              ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE,
                              NULL, TPM2_SE_POLICY, &policyAlgo,
                              TPM2_ALG_SHA256, &policyHandle);
    goto_if_error(r, "Error esys start policy session", error);

    r = Esys_PolicyCommandCode(esys_context, policyHandle, ESYS_TR_NONE,
                               ESYS_TR_NONE, ESYS_TR_NONE, TPM2_CC_Create);
    goto_if_error(r, "Error esys policy command code", error);

    TPM2B_SENSITIVE_CREATE inSensitive2 = {
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

    TPM2B_PUBLIC inPublic2 = {
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
                     .mode.aes = TPM2_ALG_CFB
                 },
                 .scheme = {
                      .scheme =
                      TPM2_ALG_NULL,
                  },
                 .keyBits = 2048,
                 .exponent = 0
             },
            .unique.rsa = {
                 .size = 0,
                 .buffer = {}
                 ,
             }
        }
    };

    TPM2B_DATA outsideInfo2 = {
        .size = 0,
        .buffer = {}
        ,
    };

    TPML_PCR_SELECTION creationPCR2 = {
        .count = 0,
    };

    r = Esys_Create(esys_context, primaryHandle, policyHandle, ESYS_TR_NONE,
                    ESYS_TR_NONE, &inSensitive2, &inPublic2, &outsideInfo2,
                    &creationPCR2, &outPrivate2, &outPublic2, NULL, NULL, NULL);
    goto_if_error(r, "Error esys create ", error);

    LOG_INFO("\nSecond key created.");

    r = Esys_FlushContext(esys_context, policyHandle);
    policyHandle = ESYS_TR_NONE;
    goto_if_error(r, "Error during FlushContext", error);

    r = Esys_FlushContext(esys_context, primaryHandle);
    primaryHandle = ESYS_TR_NONE;
    goto_if_error(r, "Error during FlushContext", error);

    Esys_Free(trialDigest);
    Esys_Free(outPublic);
    Esys_Free(outPublic2);
    Esys_Free(outPrivate2);
    return EXIT_SUCCESS;

error:

    if (trialHandle != ESYS_TR_NONE) {
        if (Esys_FlushContext(esys_context, trialHandle) != TSS2_RC_SUCCESS) {
            LOG_ERROR("Cleanup trialHandle failed.");
        }
    }

    if (policyHandle != ESYS_TR_NONE) {
        if (Esys_FlushContext(esys_context, policyHandle) != TSS2_RC_SUCCESS) {
            LOG_ERROR("Cleanup policyHandle failed.");
        }
    }

    if (primaryHandle != ESYS_TR_NONE) {
         if (Esys_FlushContext(esys_context, primaryHandle) != TSS2_RC_SUCCESS) {
            LOG_ERROR("Cleanup primaryHandle failed.");
        }
    }

    Esys_Free(trialDigest);
    Esys_Free(outPublic);
    Esys_Free(outPublic2);
    Esys_Free(outPrivate2);
    return EXIT_FAILURE;
}

int
test_invoke_esys(ESYS_CONTEXT * esys_context) {
    return test_esys_create_policy_auth(esys_context);
}
