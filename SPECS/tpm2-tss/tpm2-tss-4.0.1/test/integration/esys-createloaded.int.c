/* SPDX-License-Identifier: BSD-2-Clause */
/*******************************************************************************
 * Copyright 2017-2018, Fraunhofer SIT sponsored by Infineon Technologies AG
 * All rights reserved.
 *******************************************************************************/

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <stdbool.h>
#include <stdlib.h>

#include "tss2_esys.h"
#include "tss2_mu.h"

#include "esys_iutil.h"
#include "test-esys.h"
#define LOGMODULE test
#include "util/log.h"
#include "util/aux_util.h"

static bool check_name(ESYS_CONTEXT * esys_context, ESYS_TR object_handle)
{
    bool result = false;

    TPM2B_NAME *read_name = NULL;
    TPM2B_NAME *get_name = NULL;

    TSS2_RC r = Esys_ReadPublic(esys_context, object_handle,
                                ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE,
                                NULL, &read_name, NULL);
    goto_if_error(r, "Error esys readpublic", out);

    r = Esys_TR_GetName(esys_context, object_handle, &get_name);
    goto_if_error(r, "Error esys getname", out);

    if (read_name->size != get_name->size) {
        LOG_ERROR("name size mismatch %u != %u",
                  read_name->size, get_name->size);
        goto out;
    }

    result = memcmp(read_name->name, get_name->name, get_name->size) == 0;

out:
    Esys_Free(read_name);
    Esys_Free(get_name);

    return result;
}
/** This test is intended to test the ESYS command CreateLoaded.
 *
 * We start by creating a primary key (Esys_CreatePrimary).
 * This primary key will be used as parent key for CreateLoaded.
 *
 * Tested ESYS commands:
 *  - Esys_CreateLoaded() (F)
 *  - Esys_CreatePrimary() (M)
 *  - Esys_FlushContext() (M)
 *  - Esys_StartAuthSession() (M)
 *  - Esys_TR_GetName() (M)
 *  - Esys_TR_ReadPublic() (M)
 *
 * Used compiler defines: TEST_SESSION
 *
 * @param[in,out] esys_context The ESYS_CONTEXT.
 * @retval EXIT_FAILURE
 * @retval EXIT_SKIP
 * @retval EXIT_SUCCESS
 */

int
test_esys_createloaded(ESYS_CONTEXT * esys_context)
{

    TSS2_RC r;
    ESYS_TR primaryHandle = ESYS_TR_NONE;
    ESYS_TR objectHandle = ESYS_TR_NONE;
    int failure_return = EXIT_FAILURE;

    TPM2B_PUBLIC *outPublic = NULL;
    TPM2B_CREATION_DATA *creationData = NULL;
    TPM2B_DIGEST *creationHash = NULL;
    TPMT_TK_CREATION *creationTicket = NULL;
    TPM2B_PRIVATE *outPrivate2 = NULL;
    TPM2B_PUBLIC *outPublic2 = NULL;

#ifdef TEST_SESSION
    ESYS_TR session = ESYS_TR_NONE;
    TPMT_SYM_DEF symmetric = {.algorithm = TPM2_ALG_AES,
                              .keyBits = {.aes = 128},
                              .mode = {.aes = TPM2_ALG_CFB}
    };
    TPMA_SESSION sessionAttributes;
    TPM2B_NONCE nonceCaller = {
        .size = 20,
        .buffer = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                   11, 12, 13, 14, 15, 16, 17, 18, 19, 20}
    };

    memset(&sessionAttributes, 0, sizeof sessionAttributes);

    r = Esys_StartAuthSession(esys_context, ESYS_TR_NONE, ESYS_TR_NONE,
                              ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE,
                              &nonceCaller,
                              TPM2_SE_HMAC, &symmetric, TPM2_ALG_SHA256,
                              &session);

    goto_if_error(r, "Error: During initialization of session", error);
#endif /* TEST_SESSION */

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

    TPM2B_AUTH authValuePrimary = {
        .size = 5,
        .buffer = {1, 2, 3, 4, 5}
    };

    TPM2B_SENSITIVE_CREATE inSensitivePrimary = {
        .size = 0,
        .sensitive = {
            .userAuth = authValuePrimary,
            .data = {
                 .size = 0,
                 .buffer = {0},
             },
        },
    };

    TPM2B_DATA outsideInfo = {
        .size = 0,
        .buffer = {},
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

    r = Esys_CreatePrimary(esys_context, ESYS_TR_RH_OWNER, ESYS_TR_PASSWORD,
                           ESYS_TR_NONE, ESYS_TR_NONE, &inSensitivePrimary, &inPublic,
                           &outsideInfo, &creationPCR, &primaryHandle,
                           &outPublic, &creationData, &creationHash,
                           &creationTicket);
    goto_if_error(r, "Error esys create primary", error);

    r = Esys_TR_SetAuth(esys_context, primaryHandle, &authValuePrimary);
    goto_if_error(r, "Setting the Primary's AuthValue", error);

    TPM2B_AUTH authValueObject = {
        .size = 5,
        .buffer = {6, 7, 8, 9, 10}
    };

    TPM2B_SENSITIVE_CREATE inSensitiveObject = {
        .size = 0,
        .sensitive = {
            .userAuth = authValueObject,
            .data = {
                 .size = 0,
                 .buffer = {0},
             },
        },
    };

    TPM2B_TEMPLATE inPublic_template = {0};
    TPMT_PUBLIC  inPublic2 = {
        .type = TPM2_ALG_ECC,
        .nameAlg = TPM2_ALG_SHA256,
        .objectAttributes = (TPMA_OBJECT_USERWITHAUTH |
                             TPMA_OBJECT_RESTRICTED |
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
                  .scheme = TPM2_ALG_ECDSA,
                  .details = {.ecdsa =
                              {.hashAlg = TPM2_ALG_SHA256}
                  }
              },
             .curveID = TPM2_ECC_NIST_P256,
             .kdf = {.scheme =
                     TPM2_ALG_NULL,.details = {}
              }
         },
        .unique.ecc = {
             .x = {.size = 0,.buffer = {}},
             .y = {.size = 0,.buffer = {}}
         },
    };

    size_t offset = 0;

    r = Tss2_MU_TPMT_PUBLIC_Marshal(&inPublic2, &inPublic_template.buffer[0],
                                    sizeof(TPMT_PUBLIC), &offset);
    goto_if_error(r, "Error Tss2_MU_TPMT_PUBLIC_Marshal", error);

    inPublic_template.size = offset;

    r = Esys_CreateLoaded(
        esys_context,
        primaryHandle,
#ifdef TEST_SESSION
        session,
#else
        ESYS_TR_PASSWORD,
#endif
        ESYS_TR_NONE,
        ESYS_TR_NONE,
        &inSensitiveObject,
        &inPublic_template,
        &objectHandle,
        &outPrivate2,
        &outPublic2
        );
    if ((r == TPM2_RC_COMMAND_CODE) ||
        (r == (TPM2_RC_COMMAND_CODE | TSS2_RESMGR_RC_LAYER)) ||
        (r == (TPM2_RC_COMMAND_CODE | TSS2_RESMGR_TPM_RC_LAYER))) {
        LOG_WARNING("Command TPM2_CreateLoaded not supported by TPM.");
        failure_return = EXIT_SKIP;
        goto error;
    }

    goto_if_error(r, "Error During CreateLoaded", error);

    bool names_match = check_name(esys_context, objectHandle);
    if (!names_match) {
        goto error;
    }

    r = Esys_FlushContext(esys_context, primaryHandle);
    goto_if_error(r, "Flushing context", error);

    primaryHandle = ESYS_TR_NONE;

    r = Esys_FlushContext(esys_context, objectHandle);
    goto_if_error(r, "Flushing context", error);

    objectHandle = ESYS_TR_NONE;

#ifdef TEST_SESSION
    r = Esys_FlushContext(esys_context, session);
    goto_if_error(r, "Error: FlushContext", error);
#endif

    SAFE_FREE(outPublic);
    SAFE_FREE(creationData);
    SAFE_FREE(creationHash);
    SAFE_FREE(creationTicket);
    SAFE_FREE(outPrivate2);
    SAFE_FREE(outPublic2);
    return EXIT_SUCCESS;

 error:

#ifdef TEST_SESSION
    if (session != ESYS_TR_NONE) {
        if (Esys_FlushContext(esys_context, session) != TSS2_RC_SUCCESS) {
            LOG_ERROR("Cleanup session failed.");
        }
    }
#endif

    if (objectHandle != ESYS_TR_NONE) {
        if (Esys_FlushContext(esys_context, objectHandle) != TSS2_RC_SUCCESS) {
            LOG_ERROR("Cleanup objectHandle failed.");
        }
    }

    if (primaryHandle != ESYS_TR_NONE) {
        if (Esys_FlushContext(esys_context, primaryHandle) != TSS2_RC_SUCCESS) {
            LOG_ERROR("Cleanup primaryHandle failed.");
        }
    }

    SAFE_FREE(outPublic);
    SAFE_FREE(creationData);
    SAFE_FREE(creationHash);
    SAFE_FREE(creationTicket);
    SAFE_FREE(outPrivate2);
    SAFE_FREE(outPublic2);
    return failure_return;
}

int
test_invoke_esys(ESYS_CONTEXT * esys_context) {
    return test_esys_createloaded(esys_context);
}
