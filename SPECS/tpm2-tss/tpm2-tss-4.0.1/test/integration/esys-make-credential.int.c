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

/** This test is intended to test the function Esys_MakeCredential
 *  We start by creating a primary key (Esys_CreatePrimary).
 *
 * Based in the primary a second key will be created.
 * The public part of the key will be loaded by the function
 * Esys_LoadExternal. A credential will be encrypted with this
 * key with the command Esys_MakeCredential. The credential
 * will be activated with Esys_ActivateCredential.
 *
 * Tested ESYS commands:
 *  - Esys_ActivateCredential() (M)
 *  - Esys_Create() (M)
 *  - Esys_CreatePrimary() (M)
 *  - Esys_FlushContext() (M)
 *  - Esys_Load() (M)
 *  - Esys_LoadExternal() (M)
 *  - Esys_MakeCredential() (M)
 *  - Esys_ReadPublic() (M)
 *  - Esys_StartAuthSession() (M)
 *
 * Used compiler defines: TEST_SESSION
 *
 * @param[in,out] esys_context The ESYS_CONTEXT.
 * @retval EXIT_FAILURE
 * @retval EXIT_SUCCESS
 */

int
test_esys_make_credential(ESYS_CONTEXT * esys_context)
{
    TSS2_RC r;
    ESYS_TR primaryHandle = ESYS_TR_NONE;
    ESYS_TR loadedKeyHandle = ESYS_TR_NONE;

    TPM2B_PUBLIC *outPublic = NULL;
    TPM2B_CREATION_DATA *creationData = NULL;
    TPM2B_DIGEST *creationHash = NULL;
    TPMT_TK_CREATION *creationTicket = NULL;

    TPM2B_PUBLIC *outPublic2 = NULL;
    TPM2B_PRIVATE *outPrivate2 = NULL;
    TPM2B_CREATION_DATA *creationData2 = NULL;
    TPM2B_DIGEST *creationHash2 = NULL;
    TPMT_TK_CREATION *creationTicket2 = NULL;

    TPM2B_PUBLIC *primaryKeyPublic = NULL;
    TPM2B_NAME *primaryKeyName = NULL;
    TPM2B_NAME *primaryKeyQualifiedName = NULL;

    TPM2B_ID_OBJECT *credentialBlob = NULL;
    TPM2B_ENCRYPTED_SECRET *secret = NULL;

    TPM2B_DIGEST *certInfo = NULL;

#ifdef TEST_SESSION
    ESYS_TR session = ESYS_TR_NONE;
    ESYS_TR session2 = ESYS_TR_NONE;
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

    RSRC_NODE_T *session_node;

    r = Esys_StartAuthSession(esys_context, ESYS_TR_NONE, ESYS_TR_NONE,
                              ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE,
                              &nonceCaller,
                              TPM2_SE_HMAC, &symmetric, TPM2_ALG_SHA256,
                              &session);
    goto_if_error(r, "Error: During initialization of session", error);

    r = esys_GetResourceObject(esys_context, session,
                               &session_node);
    goto_if_error(r, "Error Esys GetResourceObject", error);

    LOG_INFO("Created session with handle 0x%08x...",
             session_node->rsrc.handle);

    RSRC_NODE_T *session2_node;

    r = Esys_StartAuthSession(esys_context, ESYS_TR_NONE, ESYS_TR_NONE,
                              ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE,
                              &nonceCaller,
                              TPM2_SE_HMAC, &symmetric, TPM2_ALG_SHA256,
                              &session2);
    goto_if_error(r, "Error: During initialization of session", error);

    r = esys_GetResourceObject(esys_context, session2,
                               &session2_node);
    goto_if_error(r, "Error Esys GetResourceObject", error);

    LOG_INFO("Created session2 with handle 0x%08x...",
             session2_node->rsrc.handle);

#endif /* TEST_SESSION */

    TPM2B_AUTH authValuePrimary = {
        .size = 5,
        .buffer = {1, 2, 3, 4, 5}
    };

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

    inSensitivePrimary.sensitive.userAuth = authValuePrimary;

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

    TPM2B_AUTH authValue = {
        .size = 0,
        .buffer = {}
    };

    r = Esys_TR_SetAuth(esys_context, ESYS_TR_RH_OWNER, &authValue);
    goto_if_error(r, "Error: TR_SetAuth", error);

    RSRC_NODE_T *primaryHandle_node;

    r = Esys_CreatePrimary(esys_context, ESYS_TR_RH_OWNER, ESYS_TR_PASSWORD,
                           ESYS_TR_NONE, ESYS_TR_NONE, &inSensitivePrimary, &inPublic,
                           &outsideInfo, &creationPCR, &primaryHandle,
                           &outPublic, &creationData, &creationHash,
                           &creationTicket);
    goto_if_error(r, "Error esys create primary", error);

    r = esys_GetResourceObject(esys_context, primaryHandle,
                               &primaryHandle_node);
    goto_if_error(r, "Error Esys GetResourceObject", error);

    LOG_INFO("Created Primary with handle 0x%08x...",
             primaryHandle_node->rsrc.handle);

    r = Esys_TR_SetAuth(esys_context, primaryHandle, &authValuePrimary);
    goto_if_error(r, "Error: TR_SetAuth", error);

    TPM2B_AUTH authKey2 = {
        .size = 6,
        .buffer = {6, 7, 8, 9, 10, 11}
    };

    TPM2B_SENSITIVE_CREATE inSensitive2 = {
        .size = 0,
        .sensitive = {
            .userAuth = {
                 .size = 0,
                 .buffer = {0}
             },
            .data = {
                 .size = 0,
                 .buffer = {}
             }
        }
    };

    inSensitive2.sensitive.userAuth = authKey2;

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

    r = Esys_Create(esys_context,
                    primaryHandle,
                    ESYS_TR_PASSWORD, ESYS_TR_NONE, ESYS_TR_NONE,
                    &inSensitive2,
                    &inPublic2,
                    &outsideInfo2,
                    &creationPCR2,
                    &outPrivate2,
                    &outPublic2,
                    &creationData2, &creationHash2, &creationTicket2);
    goto_if_error(r, "Error esys create ", error);

    LOG_INFO("\nSecond key created.");

    /*
     * Their is no individual stand-alone test for Esys_LoadExternal, so modify
     * a single Esys_LoadExternal call to test that the backwards compat change
     * from TPM2_RH to ESYS_TR works as expected. Their are other Esys_LoadExternal
     * calls that use the expected ESYS_TR type.
     *
     * For more details, see:
     *   - https://github.com/tpm2-software/tpm2-tss/issues/1750
     */
    r = Esys_LoadExternal(esys_context,
                          ESYS_TR_NONE,
                          ESYS_TR_NONE,
                          ESYS_TR_NONE,
                          NULL,
                          outPublic2,
                          TPM2_RH_OWNER,
                          &loadedKeyHandle);
    goto_if_error(r, "Error esys load external", error);

    r = Esys_ReadPublic(esys_context,
                        primaryHandle,
                        ESYS_TR_NONE,
                        ESYS_TR_NONE,
                        ESYS_TR_NONE,
                        &primaryKeyPublic,
                        &primaryKeyName,
                        &primaryKeyQualifiedName);

    goto_if_error(r, "Error esys read public", error);

    TPM2B_DIGEST credential = {
        .size = 20,
        .buffer = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                   11, 12, 13, 14, 15, 16, 17, 18, 19, 20}};

    r = Esys_MakeCredential(esys_context,
                            loadedKeyHandle,
                            ESYS_TR_NONE,
                            ESYS_TR_NONE,
                            ESYS_TR_NONE,
                            &credential,
                            primaryKeyName,
                            &credentialBlob,
                            &secret
                            );
    goto_if_error(r, "Error: MakeCredential", error);

    r = Esys_FlushContext(esys_context, loadedKeyHandle);
    goto_if_error(r, "Error esys flush context", error);

    r = Esys_Load(esys_context,
                  primaryHandle,
#ifdef TEST_SESSION
                  session,
#else
                  ESYS_TR_PASSWORD,
#endif
                  ESYS_TR_NONE,
                  ESYS_TR_NONE, outPrivate2, outPublic2, &loadedKeyHandle);
    goto_if_error(r, "Error esys load ", error);

    LOG_INFO("\nSecond Key loaded.");

    r = Esys_TR_SetAuth(esys_context, loadedKeyHandle, &authKey2);
    goto_if_error(r, "Error: TR_SetAuth", error);

    r = Esys_ActivateCredential(esys_context,
                                primaryHandle,
                                loadedKeyHandle,

#ifdef TEST_SESSION
                                session,
#else
                                ESYS_TR_PASSWORD,
#endif
#ifdef TEST_SESSION
                                session2,
#else
                                ESYS_TR_PASSWORD,
#endif
                                ESYS_TR_NONE,
                                credentialBlob,
                                secret,
                                &certInfo
                                );
    goto_if_error(r, "Error: ActivateCredential", error);

    r = Esys_FlushContext(esys_context, primaryHandle);
    goto_if_error(r, "Error during FlushContext", error);

    r = Esys_FlushContext(esys_context, loadedKeyHandle);
    goto_if_error(r, "Error esys flush context", error);

#ifdef TEST_SESSION
    r = Esys_FlushContext(esys_context, session);
    goto_if_error(r, "Flushing context", error);

    r = Esys_FlushContext(esys_context, session2);
    goto_if_error(r, "Flushing context", error);
#endif

    Esys_Free(outPublic);
    Esys_Free(creationData);
    Esys_Free(creationHash);
    Esys_Free(creationTicket);

    Esys_Free(outPublic2);
    Esys_Free(outPrivate2);
    Esys_Free(creationData2);
    Esys_Free(creationHash2);
    Esys_Free(creationTicket2);

    Esys_Free(primaryKeyPublic);
    Esys_Free(primaryKeyName);
    Esys_Free(primaryKeyQualifiedName);

    Esys_Free(credentialBlob);
    Esys_Free(secret);

    Esys_Free(certInfo);

    return EXIT_SUCCESS;

 error:

#ifdef TEST_SESSION
    if (session != ESYS_TR_NONE) {
        if (Esys_FlushContext(esys_context, session) != TSS2_RC_SUCCESS) {
            LOG_ERROR("Cleanup session failed.");
        }
    }

    if (session2 != ESYS_TR_NONE) {
        if (Esys_FlushContext(esys_context, session2) != TSS2_RC_SUCCESS) {
            LOG_ERROR("Cleanup session2 failed.");
        }
    }
#endif

    if (loadedKeyHandle != ESYS_TR_NONE) {
        if (Esys_FlushContext(esys_context, loadedKeyHandle) != TSS2_RC_SUCCESS) {
            LOG_ERROR("Cleanup loadedKeyHandle failed.");
        }
    }

    if (primaryHandle != ESYS_TR_NONE) {
        if (Esys_FlushContext(esys_context, primaryHandle) != TSS2_RC_SUCCESS) {
            LOG_ERROR("Cleanup primaryHandle failed.");
        }
    }

    Esys_Free(outPublic);
    Esys_Free(creationData);
    Esys_Free(creationHash);
    Esys_Free(creationTicket);

    Esys_Free(outPublic2);
    Esys_Free(outPrivate2);
    Esys_Free(creationData2);
    Esys_Free(creationHash2);
    Esys_Free(creationTicket2);

    Esys_Free(primaryKeyPublic);
    Esys_Free(primaryKeyName);
    Esys_Free(primaryKeyQualifiedName);

    Esys_Free(credentialBlob);
    Esys_Free(secret);

    Esys_Free(certInfo);
    return EXIT_FAILURE;
}

int
test_invoke_esys(ESYS_CONTEXT * esys_context) {
    return test_esys_make_credential(esys_context);
}
