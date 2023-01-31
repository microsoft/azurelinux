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

/** This test is intended to test the ESYS commands  nv define space, nv write,
 *  nv read command, nv lock write and nv lock read, and nv undefine.
 *
 * The names stored in the ESYS resource are compared
 * with the names delivered from the TPM by the command ReadPublic.
 * only one of the tests NV_ReadLock and NV_WriteLock can be activated
 * by the defines TEST_READ_LOCK and TEST_WRITE_LOCK (-D option)
 *
 * Tested ESYS commands:
 *  - Esys_FlushContext() (M)
 *  - Esys_NV_DefineSpace() (M)
 *  - Esys_NV_Read() (M)
 *  - Esys_NV_ReadLock() (M)
 *  - Esys_NV_ReadPublic() (M)
 *  - Esys_NV_UndefineSpace() (M)
 *  - Esys_NV_Write() (M)
 *  - Esys_NV_WriteLock() (M)
 *  - Esys_StartAuthSession() (M)
 *
 * Used compiler defines: TEST_READ_LOCK TEST_SESSION TEST_WRITE_LOCK
 *
 * @param[in,out] esys_context The ESYS_CONTEXT.
 * @retval EXIT_FAILURE
 * @retval EXIT_SUCCESS
 */

int
test_esys_nv_ram_ordinary_index(ESYS_CONTEXT * esys_context)
{
    TSS2_RC r;
    ESYS_TR nvHandle = ESYS_TR_NONE;

    TPM2B_NV_PUBLIC *nvPublic = NULL;
    TPM2B_NAME *nvName = NULL;
    TPM2B_MAX_NV_BUFFER *nv_test_data2 = NULL;

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
            .dataSize = 32,
        }
    };

    r = Esys_NV_DefineSpace(esys_context,
                            ESYS_TR_RH_OWNER,
#ifdef TEST_SESSION
                            session,
#else
                            ESYS_TR_PASSWORD,
#endif
                            ESYS_TR_NONE,
                            ESYS_TR_NONE,
                            &auth,
                            &publicInfo,
                            &nvHandle);

    goto_if_error(r, "Error esys define nv space", error);

    UINT16 offset = 0;
    TPM2B_MAX_NV_BUFFER nv_test_data = { .size = 20,
                                         .buffer={0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0,
                                                  1, 2, 3, 4, 5, 6, 7, 8, 9}};

    r = Esys_NV_ReadPublic(esys_context,
                           nvHandle,
                           ESYS_TR_NONE,
                           ESYS_TR_NONE,
                           ESYS_TR_NONE,
                           &nvPublic,
                           &nvName);
    goto_if_error(r, "Error: nv read public", error);

    RSRC_NODE_T *nvHandleNode;

    r = esys_GetResourceObject(esys_context, nvHandle, &nvHandleNode);
    goto_if_error(r, "Error: nv get resource object", error);

    if (nvName->size != nvHandleNode->rsrc.name.size ||
        memcmp(&nvName->name, &nvHandleNode->rsrc.name.name, nvName->size) != 0) {
        LOG_ERROR("Error: define space name not equal");
        goto error;
    }
    r = Esys_NV_Write(esys_context,
                      nvHandle,
                      nvHandle,
#ifdef TEST_SESSION
                      session,
#else
                      ESYS_TR_PASSWORD,
#endif
                      ESYS_TR_NONE,
                      ESYS_TR_NONE,
                      &nv_test_data,
                      offset);

    goto_if_error(r, "Error esys nv write", error);

    Esys_Free(nvPublic);
    Esys_Free(nvName);

    r = Esys_NV_ReadPublic(esys_context,
                           nvHandle,
                           ESYS_TR_NONE,
                           ESYS_TR_NONE,
                           ESYS_TR_NONE,
                           &nvPublic,
                           &nvName);
    goto_if_error(r, "Error: nv read public", error);

    r = esys_GetResourceObject(esys_context, nvHandle, &nvHandleNode);
    goto_if_error(r, "Error: nv get resource object", error);

    if (nvName->size != nvHandleNode->rsrc.name.size ||
        memcmp(&nvName->name, &nvHandleNode->rsrc.name.name, nvName->size) != 0) {
        LOG_ERROR("Error: nv write name not equal");
        goto error;
    }

    r = Esys_NV_Read(esys_context,
                     nvHandle,
                     nvHandle,
#ifdef TEST_SESSION
                     session,
#else
                     ESYS_TR_PASSWORD,
#endif
                     ESYS_TR_NONE,
                     ESYS_TR_NONE,
                     20,
                     0,
                     &nv_test_data2);

    goto_if_error(r, "Error esys nv read", error);

    Esys_Free(nvPublic);
    Esys_Free(nvName);
    Esys_Free(nv_test_data2);

    r = Esys_NV_ReadPublic(esys_context,
                           nvHandle,
                           ESYS_TR_NONE,
                           ESYS_TR_NONE,
                           ESYS_TR_NONE,
                           &nvPublic,
                           &nvName);
    goto_if_error(r, "Error: nv read public", error);

    r = esys_GetResourceObject(esys_context, nvHandle, &nvHandleNode);
    goto_if_error(r, "Error: nv get resource object", error);

    if (nvName->size != nvHandleNode->rsrc.name.size ||
        memcmp(&nvName->name, &nvHandleNode->rsrc.name.name, nvName->size) != 0) {
        LOG_ERROR("Error: nv read name not equal");
        goto error;
    }

#ifdef TEST_READ_LOCK
    r = Esys_NV_ReadLock(esys_context,
                         nvHandle,
                         nvHandle,
#ifdef TEST_SESSION
                         session,
#else
                         ESYS_TR_PASSWORD,
#endif
                         ESYS_TR_NONE,
                         ESYS_TR_NONE
                         );
    goto_if_error(r, "Error: NV_ReadLock", error);

    Esys_Free(nvPublic);
    Esys_Free(nvName);

    r = Esys_NV_ReadPublic(esys_context,
                           nvHandle,
                           ESYS_TR_NONE,
                           ESYS_TR_NONE,
                           ESYS_TR_NONE,
                           &nvPublic,
                           &nvName);
    goto_if_error(r, "Error: nv read public", error);

    r = esys_GetResourceObject(esys_context, nvHandle, &nvHandleNode);
    goto_if_error(r, "Error: nv get resource object", error);

    if (nvName->size != nvHandleNode->rsrc.name.size ||
        memcmp(&nvName->name, &nvHandleNode->rsrc.name.name, nvName->size) != 0) {
        LOG_ERROR("Error: nv read name not equal");
        goto error;
    }

    r = Esys_NV_Read(esys_context,
                     nvHandle,
                     nvHandle,
#ifdef TEST_SESSION
                     session,
#else
                     ESYS_TR_PASSWORD,
#endif
                     ESYS_TR_NONE,
                     ESYS_TR_NONE,
                     20,
                     0,
                     &nv_test_data2);

    goto_error_if_not_failed(r, "Error esys nv write successful in write lock state", error);
#else /* TEST_READ_LOCK */
#ifdef TEST_WRITE_LOCK
    r = Esys_NV_WriteLock(esys_context,
                          nvHandle,
                          nvHandle,
#ifdef TEST_SESSION
                          session,
#else
                          ESYS_TR_PASSWORD,
#endif
                          ESYS_TR_NONE,
                          ESYS_TR_NONE
                          );
    goto_if_error(r, "Error: NV_WriteLock", error);

    Esys_Free(nvPublic);
    Esys_Free(nvName);

    r = Esys_NV_ReadPublic(esys_context,
                           nvHandle,
                           ESYS_TR_NONE,
                           ESYS_TR_NONE,
                           ESYS_TR_NONE,
                           &nvPublic,
                           &nvName);
    goto_if_error(r, "Error: NV_ReadPublic", error);

    r = esys_GetResourceObject(esys_context, nvHandle, &nvHandleNode);
    goto_if_error(r, "Error: nv get resource object", error);

    if (nvName->size != nvHandleNode->rsrc.name.size ||
        memcmp(&nvName->name, &nvHandleNode->rsrc.name.name, nvName->size) != 0) {
        LOG_ERROR("Error: nv read name not equal");
        goto error;
    }
    r = Esys_NV_Write(esys_context,
                      nvHandle,
                      nvHandle,
#ifdef TEST_SESSION
                      session,
#else
                      ESYS_TR_PASSWORD,
#endif
                      ESYS_TR_NONE,
                      ESYS_TR_NONE,
                      &nv_test_data,
                      offset);
    goto_error_if_not_failed(r, "Error esys nv write successful in write lock state", error);
#endif /* TEST_WRITE_LOCK */
#endif /* TEST_READ_LOCK */

    r = Esys_NV_UndefineSpace(esys_context,
                              ESYS_TR_RH_OWNER,
                              nvHandle,
#ifdef TEST_SESSION
                              session,
#else
                              ESYS_TR_PASSWORD,
#endif
                              ESYS_TR_NONE,
                              ESYS_TR_NONE
                              );
    goto_if_error(r, "Error: NV_UndefineSpace", error);

#ifdef TEST_SESSION
    r = Esys_FlushContext(esys_context, session);
    goto_if_error(r, "Error: FlushContext", error);
#endif

    Esys_Free(nvPublic);
    Esys_Free(nvName);
    return EXIT_SUCCESS;

 error:

    if (nvHandle != ESYS_TR_NONE) {
        if (Esys_NV_UndefineSpace(esys_context,
                                  ESYS_TR_RH_OWNER,
                                  nvHandle,
#ifdef TEST_SESSION
                                  session,
#else
                                  ESYS_TR_PASSWORD,
#endif
                                  ESYS_TR_NONE,
                                  ESYS_TR_NONE) != TSS2_RC_SUCCESS) {
             LOG_ERROR("Cleanup nvHandle failed.");
        }
    }

#ifdef TEST_SESSION
    if (session != ESYS_TR_NONE) {
        if (Esys_FlushContext(esys_context, session) != TSS2_RC_SUCCESS) {
            LOG_ERROR("Cleanup session failed.");
        }
    }
#endif
    Esys_Free(nvPublic);
    Esys_Free(nvName);
    Esys_Free(nv_test_data2);
    return EXIT_FAILURE;
}

int
test_invoke_esys(ESYS_CONTEXT * esys_context) {
    return test_esys_nv_ram_ordinary_index(esys_context);
}
