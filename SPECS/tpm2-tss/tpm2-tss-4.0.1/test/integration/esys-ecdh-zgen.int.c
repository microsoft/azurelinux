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

/** This test is intended to test Esys_ECDH_ZGen.
 *   based on an ECC key
 * created with Esys_CreatePrimary and a dummy ECC point.
 *
 * Tested ESYS commands:
 *  - Esys_CreatePrimary() (M)
 *  - Esys_ECDH_ZGen() (M)
 *  - Esys_FlushContext() (M)
 *  - Esys_StartAuthSession() (M)
 *
 * @param[in,out] esys_context The ESYS_CONTEXT.
 * @retval EXIT_FAILURE
 * @retval EXIT_SUCCESS
 */

int
test_esys_ecdh_zgen(ESYS_CONTEXT * esys_context)
{
    TSS2_RC r;
    ESYS_TR eccHandle = ESYS_TR_NONE;
    ESYS_TR session = ESYS_TR_NONE;
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

    TPM2B_PUBLIC *outPublic = NULL;
    TPM2B_CREATION_DATA *creationData = NULL;
    TPM2B_DIGEST *creationHash = NULL;
    TPMT_TK_CREATION *creationTicket = NULL;
    TPM2B_ECC_POINT *outPoint = NULL;

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
                                 TPMA_OBJECT_DECRYPT |
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
                      .scheme = TPM2_ALG_ECDH,
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
    goto_if_error(r, "Error esys create primary", error);

    TPM2B_ECC_POINT inPoint= {
        .size = 0,
        .point = {
            .x = {
                 .size =  32,
                 .buffer = {
                     0x25, 0xdb, 0x1f, 0x8b, 0xbc, 0xfa, 0xbc, 0x31,
                     0xf8, 0x17, 0x6a, 0xcb, 0xb2, 0xf8, 0x40, 0xa3,
                     0xb6, 0xa5, 0xd3, 0x40, 0x65, 0x9d, 0x37, 0xee,
                     0xd9, 0xfd, 0x52, 0x47, 0xf5, 0x14, 0xd5, 0x98
                 },
             },
            .y = {
                 .size = 32,
                 .buffer = {
                     0xed, 0x62, 0x3e, 0x3d, 0xd2, 0x09, 0x08, 0xcf,
                     0x58, 0x3c, 0x81, 0x4b, 0xbf, 0x65, 0x7e, 0x08,
                     0xab, 0x9f, 0x40, 0xff, 0xea, 0x51, 0xda, 0x21,
                     0x29, 0x8c, 0xe2, 0x4d, 0xeb, 0x34, 0x4c, 0xcc
                 }
             }
        }
    };

    r = Esys_ECDH_ZGen(
        esys_context,
        eccHandle,
        ESYS_TR_PASSWORD,
        ESYS_TR_NONE,
        ESYS_TR_NONE,
        &inPoint,
        &outPoint);
    goto_if_error(r, "Error: ECDH_ZGen", error);

    r = Esys_FlushContext(esys_context, eccHandle);
    goto_if_error(r, "Error during FlushContext", error);

    r = Esys_FlushContext(esys_context, session);
    goto_if_error(r, "Flushing context", error);

    Esys_Free(outPublic);
    Esys_Free(creationData);
    Esys_Free(creationHash);
    Esys_Free(creationTicket);
    Esys_Free(outPoint);
    return EXIT_SUCCESS;

 error:
    LOG_ERROR("\nError Code: %x\n", r);

    if (session != ESYS_TR_NONE) {
        if (Esys_FlushContext(esys_context, session) != TSS2_RC_SUCCESS) {
            LOG_ERROR("Cleanup session failed.");
        }
    }

    if (eccHandle != ESYS_TR_NONE) {
        if (Esys_FlushContext(esys_context, eccHandle) != TSS2_RC_SUCCESS) {
            LOG_ERROR("Cleanup eccHandle failed.");
        }
    }

    Esys_Free(outPublic);
    Esys_Free(creationData);
    Esys_Free(creationHash);
    Esys_Free(creationTicket);
    Esys_Free(outPoint);
    return EXIT_FAILURE;
}

int
test_invoke_esys(ESYS_CONTEXT * esys_context) {
    return test_esys_ecdh_zgen(esys_context);
}
