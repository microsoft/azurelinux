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

/** This test is intended to test parameter encryption/decryption, session management,
 *  hmac computation, and session key generation.
 *
 * We start by creating a primary key (Esys_CreatePrimary).
 * The primary key will be used as tpmKey for Esys_StartAuthSession. Parameter
 * encryption and decryption will be activated for the session.
 * The session will be used to Create a second key by Eys_Create (with password)
 * This key will be Loaded to and a third key will be created with the second
 * key as parent key (Esys_Create).
 * The type of encryptin can be selected by the compiler variables (-D option):
 * TEST_XOR_OBFUSCATION or TEST_AES_ENCRYPTION.
 * Secret exchange with a ECC key can be activated with the compiler variable
 * -D TEST_ECC.
 *
 * Tested ESYS commands:
 *  - Esys_ContextLoad() (M)
 *  - Esys_ContextSave() (M)
 *  - Esys_Create() (M)
 *  - Esys_CreatePrimary() (M)
 *  - Esys_FlushContext() (M)
 *  - Esys_Load() (M)
 *  - Esys_StartAuthSession() (M)
 *
 * Used compiler defines: TEST_ECC, TEST_AES_ENCRYPTION, TEST_BOUND_SESSION
 *                        TEST_XOR_OBFUSCATION
 *
 * @param[in,out] esys_context The ESYS_CONTEXT.
 * @retval EXIT_FAILURE
 * @retval EXIT_SUCCESS
 */

int
test_esys_create_session_auth(ESYS_CONTEXT * esys_context)
{
    TSS2_RC r;
    ESYS_TR primaryHandle = ESYS_TR_NONE;
    ESYS_TR loadedKeyHandle = ESYS_TR_NONE;
#if defined(TEST_ECC) || !defined(TEST_NULL_BIND_NO_TPM_KEY)
    ESYS_TR primaryHandle_AuthSession = ESYS_TR_NONE;
#endif
    ESYS_TR session = ESYS_TR_NONE;
    ESYS_TR outerSession = ESYS_TR_NONE;

    TPM2B_PUBLIC *outPublic = NULL;
    TPM2B_CREATION_DATA *creationData = NULL;
    TPM2B_DIGEST *creationHash = NULL;
    TPMT_TK_CREATION *creationTicket = NULL;

#ifdef TEST_ECC
    TPM2B_PUBLIC *outPublicEcc = NULL;
    TPM2B_CREATION_DATA *creationDataEcc = NULL;
    TPM2B_DIGEST *creationHashEcc = NULL;
    TPMT_TK_CREATION *creationTicketEcc = NULL;
#endif

    TPM2B_PUBLIC *outPublic2 = NULL;
    TPM2B_PRIVATE *outPrivate2 = NULL;
    TPM2B_CREATION_DATA *creationData2 = NULL;
    TPM2B_DIGEST *creationHash2 = NULL;
    TPMT_TK_CREATION *creationTicket2 = NULL;

    TPM2B_AUTH authValuePrimary = {
        .size = 5,
        .buffer = {1, 2, 3, 4, 5}
    };

#ifdef TEST_LARGE_AUTH
    for (int i = 0; i < 33; i++)
        authValuePrimary.buffer[i] = i;
    authValuePrimary.size = 33;
#endif

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

#ifdef TEST_ECC
    TPM2B_PUBLIC inPublicEcc = {
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
                      .details = {
                          .ecdh = {.hashAlg  = TPM2_ALG_SHA256}},
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
#endif
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


#ifdef TEST_ECC
    r = Esys_CreatePrimary(esys_context, ESYS_TR_RH_OWNER, ESYS_TR_PASSWORD,
                           ESYS_TR_NONE, ESYS_TR_NONE, &inSensitivePrimary, &inPublicEcc,
                           &outsideInfo, &creationPCR, &primaryHandle_AuthSession,
                           &outPublicEcc, &creationDataEcc, &creationHashEcc,
                           &creationTicketEcc);
    goto_if_error(r, "Error esys create primary", error);

    r = Esys_TR_SetAuth(esys_context, primaryHandle_AuthSession, &authValuePrimary);
    goto_if_error(r, "Error: TR_SetAuth", error);
#elif defined(TEST_BOUND_SESSION) || !defined(TEST_NULL_BIND_NO_TPM_KEY)
    primaryHandle_AuthSession = primaryHandle;
#endif /* TEST_ECC */

#if TEST_XOR_OBFUSCATION
    TPMT_SYM_DEF symmetric = {.algorithm = TPM2_ALG_XOR,
                              .keyBits = { .exclusiveOr = TPM2_ALG_SHA256 },
                              .mode = {.aes = TPM2_ALG_CFB}};
#elif TEST_AES_ENCRYPTION
    TPMT_SYM_DEF symmetric = {.algorithm = TPM2_ALG_AES,
                              .keyBits = {.aes = 128},
                              .mode = {.aes = TPM2_ALG_CFB}};
#else
    #error "TEST_XOR_OBFUSCATION or TEST_PARAM_ENCRYPTION not set"
#endif

    TPMA_SESSION sessionAttributes;
    TPMA_SESSION sessionAttributes2;
    sessionAttributes = (TPMA_SESSION_DECRYPT |
                         TPMA_SESSION_ENCRYPT |
                         TPMA_SESSION_CONTINUESESSION);
    TPM2_SE sessionType = TPM2_SE_HMAC;
    TPMI_ALG_HASH authHash = TPM2_ALG_SHA256;

    r = Esys_StartAuthSession(esys_context,
                              ESYS_TR_NONE, ESYS_TR_NONE,
                              ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE,
                              NULL,
                              TPM2_SE_HMAC, &symmetric, TPM2_ALG_SHA256,
                              &outerSession);
    goto_if_error(r, "Error during Esys_StartAuthSession", error);

    r = Esys_TRSess_SetAttributes(esys_context, outerSession, TPMA_SESSION_AUDIT,
                                  TPMA_SESSION_AUDIT);
    goto_if_error(r, "Error Esys_TRSess_SetAttributes", error);

#if defined(TEST_BOUND_SESSION)
    r = Esys_StartAuthSession(esys_context,
                              primaryHandle_AuthSession,
                              primaryHandle_AuthSession,
                              outerSession, ESYS_TR_NONE, ESYS_TR_NONE,
                              NULL,
                              sessionType, &symmetric, authHash, &session);
#elif defined(TEST_NULL_BIND_TPMKEY)
     r = Esys_StartAuthSession(esys_context,
                              primaryHandle_AuthSession,
                              ESYS_TR_RH_NULL,
                              outerSession, ESYS_TR_NONE, ESYS_TR_NONE,
                              NULL,
                              sessionType, &symmetric, authHash, &session);
#elif defined(TEST_NULL_BIND_NO_TPM_KEY)
     r = Esys_StartAuthSession(esys_context,
                               ESYS_TR_NONE,
                               ESYS_TR_RH_NULL,
                               outerSession, ESYS_TR_NONE, ESYS_TR_NONE,
                               NULL,
                               sessionType, &symmetric, authHash, &session);
#else
     r = Esys_StartAuthSession(esys_context,
                               primaryHandle_AuthSession,
                               ESYS_TR_NONE,
                               outerSession, ESYS_TR_NONE, ESYS_TR_NONE,
                               NULL,
                               sessionType, &symmetric, authHash, &session);
#endif

     Esys_FlushContext(esys_context, outerSession);
    goto_if_error(r, "Error during Esys_StartAuthSession", error);

#ifdef TEST_ECC
    r = Esys_FlushContext(esys_context, primaryHandle_AuthSession);
    goto_if_error(r, "Error during FlushContext", error);
#endif

    goto_if_error(r, "Error Esys_StartAuthSessiony", error);
    r = Esys_TRSess_SetAttributes(esys_context, session, sessionAttributes,
                                  0xff);
    goto_if_error(r, "Error Esys_TRSess_SetAttributes", error);

    r = Esys_TRSess_GetAttributes(esys_context, session, &sessionAttributes2);
    goto_if_error(r, "Error Esys_TRSess_SetAttributes", error);

    if (sessionAttributes != sessionAttributes2) {
        LOG_ERROR("Session Attributes differ");
        goto error;
    }

    /* Save and load the session and test if the attributes are still OK. */
    TPMS_CONTEXT *contextBlob;
    r = Esys_ContextSave(esys_context, session, &contextBlob);
    goto_if_error(r, "Error during ContextSave", error);

    session = ESYS_TR_NONE;

    r = Esys_ContextLoad(esys_context, contextBlob, &session);
    goto_if_error(r, "Error during ContextLoad", error);

    free(contextBlob);

    r = Esys_TRSess_GetAttributes(esys_context, session, &sessionAttributes2);
    goto_if_error(r, "Error Esys_TRSess_SetAttributes", error);

    if (sessionAttributes != sessionAttributes2) {
        LOG_ERROR("Session Attributes differ");
        goto error;
    }

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

    TPM2B_SENSITIVE_CREATE inSensitive3 = {
        .size = 0,
        .sensitive = {
            .userAuth = {
                 .size = 0,
                 .buffer = {}
             },
            .data = {
                 .size = 0,
                 .buffer = {}
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

    r = Esys_Create(esys_context,
                    primaryHandle,
                    session, ESYS_TR_NONE, ESYS_TR_NONE,
                    &inSensitive2,
                    &inPublic2,
                    &outsideInfo2,
                    &creationPCR2,
                    &outPrivate2,
                    &outPublic2,
                    &creationData2, &creationHash2, &creationTicket2);
    goto_if_error(r, "Error esys create ", error);

    LOG_INFO("\nSecond key created.");

    r = Esys_Load(esys_context,
                  primaryHandle,
                  session,
                  ESYS_TR_NONE,
                  ESYS_TR_NONE, outPrivate2, outPublic2, &loadedKeyHandle);
    goto_if_error(r, "Error esys load ", error);

    LOG_INFO("\nSecond Key loaded.");

    r = Esys_TR_SetAuth(esys_context, loadedKeyHandle, &authKey2);
    goto_if_error(r, "Error esys TR_SetAuth ", error);

    Esys_Free(outPublic2);
    Esys_Free(outPrivate2);
    Esys_Free(creationData2);
    Esys_Free(creationHash2);
    Esys_Free(creationTicket2);

    r = Esys_Create(esys_context,
                    loadedKeyHandle,
                    session, ESYS_TR_NONE, ESYS_TR_NONE,
                    &inSensitive3,
                    &inPublic2,
                    &outsideInfo2,
                    &creationPCR2,
                    &outPrivate2,
                    &outPublic2,
                    &creationData2, &creationHash2, &creationTicket2);
    goto_if_error(r, "Error esys second create ", error);

    r = Esys_FlushContext(esys_context, primaryHandle);
    goto_if_error(r, "Error during FlushContext", error);

    r = Esys_FlushContext(esys_context, loadedKeyHandle);
    goto_if_error(r, "Error during FlushContext", error);

    r = Esys_FlushContext(esys_context, session);
    goto_if_error(r, "Flushing context", error);

    Esys_Free(outPublic);
    Esys_Free(creationData);
    Esys_Free(creationHash);
    Esys_Free(creationTicket);

#ifdef TEST_ECC
    Esys_Free(outPublicEcc);
    Esys_Free(creationDataEcc);
    Esys_Free(creationHashEcc);
    Esys_Free(creationTicketEcc);
#endif

    Esys_Free(outPublic2);
    Esys_Free(outPrivate2);
    Esys_Free(creationData2);
    Esys_Free(creationHash2);
    Esys_Free(creationTicket2);
    return EXIT_SUCCESS;

 error:

    if (session != ESYS_TR_NONE) {
        if (Esys_FlushContext(esys_context, session) != TSS2_RC_SUCCESS) {
            LOG_ERROR("Cleanup session failed.");
        }
    }

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

#ifdef TEST_ECC
    if (primaryHandle_AuthSession != ESYS_TR_NONE) {
        if (Esys_FlushContext(esys_context, primaryHandle_AuthSession) != TSS2_RC_SUCCESS) {
            LOG_ERROR("Cleanup primaryHandle_AuthSession failed.");
        }
    }
#endif

    Esys_Free(outPublic);
    Esys_Free(creationData);
    Esys_Free(creationHash);
    Esys_Free(creationTicket);

#ifdef TEST_ECC
    Esys_Free(outPublicEcc);
    Esys_Free(creationDataEcc);
    Esys_Free(creationHashEcc);
    Esys_Free(creationTicketEcc);
#endif

    Esys_Free(outPublic2);
    Esys_Free(outPrivate2);
    Esys_Free(creationData2);
    Esys_Free(creationHash2);
    Esys_Free(creationTicket2);
    return EXIT_FAILURE;
}

int
test_invoke_esys(ESYS_CONTEXT * esys_context) {
    return test_esys_create_session_auth(esys_context);
}
