/* SPDX-License-Identifier: BSD-2-Clause */
/*******************************************************************************
 * Copyright 2017-2018, Fraunhofer SIT sponsored by Infineon Technologies AG All
 * rights reserved.
 ******************************************************************************/

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <stdarg.h>
#include <inttypes.h>
#include <string.h>
#include <stdlib.h>

#include <setjmp.h>
#include <cmocka.h>

#include "tss2_esys.h"

#include "tss2-esys/esys_iutil.h"
#define LOGMODULE tests
#include "util/log.h"
#include "util/aux_util.h"
#include "esys-dummy-defs.h"

/**
 * This unit test looks into a set of Esys_<cmd>() functions and tests the
 * resubmission behaviour. The ESAPI is expected to resubmit a command for a
 * certain number of times if the TPM return RC_YIELDED. After this number of
 * times, the ESAPI shall not try it any further but return the TPM's error.
 * For all these resubmissions the command must be the same as before.
 * This shall be extended to cover all functions at some point.
 */

#define TCTI_TRYAGAINERROR_MAGIC 0x5441455252000000ULL        /* 'TAERR\0' */
#define TCTI_TRYAGAINERROR_VERSION 0x1

typedef struct {
    uint64_t magic;
    uint32_t version;
    TSS2_TCTI_TRANSMIT_FCN transmit;
    TSS2_TCTI_RECEIVE_FCN receive;
    TSS2_RC(*finalize) (TSS2_TCTI_CONTEXT * tctiContext);
    TSS2_RC(*cancel) (TSS2_TCTI_CONTEXT * tctiContext);
    TSS2_RC(*getPollHandles) (TSS2_TCTI_CONTEXT * tctiContext,
                           TSS2_TCTI_POLL_HANDLE * handles,
                           size_t * num_handles);
    TSS2_RC(*setLocality) (TSS2_TCTI_CONTEXT * tctiContext, uint8_t locality);
    uint32_t count;
} TSS2_TCTI_CONTEXT_TRYAGAINERROR;

static TSS2_TCTI_CONTEXT_TRYAGAINERROR *
tcti_tryagainerror_cast(TSS2_TCTI_CONTEXT * ctx)
{
    TSS2_TCTI_CONTEXT_TRYAGAINERROR *ctxi = (TSS2_TCTI_CONTEXT_TRYAGAINERROR *) ctx;
    if (ctxi == NULL || ctxi->magic != TCTI_TRYAGAINERROR_MAGIC) {
        LOG_ERROR("Bad tcti passed.");
        exit(1);
    }
    return ctxi;
}

static TSS2_RC
tcti_tryagainerror_transmit(TSS2_TCTI_CONTEXT * tctiContext,
                      size_t size, const uint8_t * buffer)
{
    TSS2_TCTI_CONTEXT_TRYAGAINERROR *tcti = tcti_tryagainerror_cast(tctiContext);

    /* First call to transmit on this context */
    if (tcti->count == 0)
        return TSS2_RC_SUCCESS;

    if (tcti->count == 2)
        return TSS2_RC_SUCCESS;

    LOG_ERROR("Expected 2 receives before the next transmit, but %" PRIu32
              "receives occurred.", tcti->count);
    return TSS2_TCTI_RC_GENERAL_FAILURE;
}

static TSS2_RC
tcti_tryagainerror_receive(TSS2_TCTI_CONTEXT * tctiContext,
                     size_t * response_size,
                     uint8_t * response_buffer, int32_t timeout)
{
    TSS2_TCTI_CONTEXT_TRYAGAINERROR *tcti = tcti_tryagainerror_cast(tctiContext);
    UNUSED(response_size);
    UNUSED(response_buffer);
    UNUSED(timeout);
    tcti->count++;
    if (tcti->count == 1)
        return TSS2_TCTI_RC_TRY_AGAIN;
    else
        return TSS2_TCTI_RC_NO_CONNECTION;
}

static void
tcti_tryagainerror_finalize(TSS2_TCTI_CONTEXT * tctiContext)
{
    TSS2_TCTI_CONTEXT_TRYAGAINERROR *tcti = tcti_tryagainerror_cast(tctiContext);
    if (tcti->count != 2) {
        LOG_ERROR("Expected 2 receives before the next transmit, but %" PRIu32
                  "receives occurred.", tcti->count);
        exit(1);
    }
}

static TSS2_RC
tcti_tryagainerror_initialize(TSS2_TCTI_CONTEXT * tctiContext, size_t * contextSize)
{
    TSS2_TCTI_CONTEXT_TRYAGAINERROR *tcti_tryagainerror =
        (TSS2_TCTI_CONTEXT_TRYAGAINERROR *) tctiContext;

    if (tctiContext == NULL && contextSize == NULL) {
        return TSS2_TCTI_RC_BAD_VALUE;
    } else if (tctiContext == NULL) {
        *contextSize = sizeof(*tcti_tryagainerror);
        return TSS2_RC_SUCCESS;
    }

    /* Init TCTI context */
    memset(tcti_tryagainerror, 0, sizeof(*tcti_tryagainerror));
    TSS2_TCTI_MAGIC(tctiContext) = TCTI_TRYAGAINERROR_MAGIC;
    TSS2_TCTI_VERSION(tctiContext) = TCTI_TRYAGAINERROR_VERSION;
    TSS2_TCTI_TRANSMIT(tctiContext) = tcti_tryagainerror_transmit;
    TSS2_TCTI_RECEIVE(tctiContext) = tcti_tryagainerror_receive;
    TSS2_TCTI_FINALIZE(tctiContext) = tcti_tryagainerror_finalize;
    TSS2_TCTI_CANCEL(tctiContext) = NULL;
    TSS2_TCTI_GET_POLL_HANDLES(tctiContext) = NULL;
    TSS2_TCTI_SET_LOCALITY(tctiContext) = NULL;
    tcti_tryagainerror->count = 0;

    return TSS2_RC_SUCCESS;
}

static int
setup(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *ectx;
    size_t size = sizeof(TSS2_TCTI_CONTEXT_TRYAGAINERROR);
    TSS2_TCTI_CONTEXT *tcti = malloc(size);
    ESYS_TR objectHandle;
    RSRC_NODE_T *objectHandleNode = NULL;

    r = tcti_tryagainerror_initialize(tcti, &size);
    if (r)
        return (int)r;
    r = Esys_Initialize(&ectx, tcti, NULL);
    if (r)
        return (int)r;

    /* Create dummy object to enable usage of SAPI prepare functions in the tests */
    objectHandle = DUMMY_TR_HANDLE_POLICY_SESSION;
    r = esys_CreateResourceObject(ectx, objectHandle, &objectHandleNode);
    if (r)
        return (int)r;
    objectHandleNode->rsrc.rsrcType = IESYSC_SESSION_RSRC;
    objectHandleNode->rsrc.handle = TPM2_POLICY_SESSION_FIRST;

    objectHandle = DUMMY_TR_HANDLE_HMAC_SESSION;
    r = esys_CreateResourceObject(ectx, objectHandle, &objectHandleNode);
    if (r)
        return (int)r;
    objectHandleNode->rsrc.rsrcType = IESYSC_SESSION_RSRC;
    objectHandleNode->rsrc.handle = TPM2_HMAC_SESSION_FIRST;

    objectHandle = DUMMY_TR_HANDLE_KEY;
    r = esys_CreateResourceObject(ectx, objectHandle, &objectHandleNode);
    if (r)
        return (int)r;
    objectHandleNode->rsrc.rsrcType = IESYSC_KEY_RSRC;
    objectHandleNode->rsrc.handle = TPM2_TRANSIENT_FIRST;

    objectHandle = DUMMY_TR_HANDLE_HIERARCHY_OWNER;
    r = esys_CreateResourceObject(ectx, objectHandle, &objectHandleNode);
    if (r)
        return (int)r;
    objectHandleNode->rsrc.rsrcType = IESYSC_WITHOUT_MISC_RSRC;
    objectHandleNode->rsrc.handle = TPM2_RH_OWNER;

    objectHandle = DUMMY_TR_HANDLE_HIERARCHY_PLATFORM;
    r = esys_CreateResourceObject(ectx, objectHandle, &objectHandleNode);
    if (r)
        return (int)r;
    objectHandleNode->rsrc.rsrcType = IESYSC_WITHOUT_MISC_RSRC;
    objectHandleNode->rsrc.handle = TPM2_RH_PLATFORM;

    objectHandle = DUMMY_TR_HANDLE_LOCKOUT;
    r = esys_CreateResourceObject(ectx, objectHandle, &objectHandleNode);
    if (r)
        return (int)r;
    objectHandleNode->rsrc.rsrcType = IESYSC_WITHOUT_MISC_RSRC;
    objectHandleNode->rsrc.handle = TPM2_RH_LOCKOUT;

    objectHandle = DUMMY_TR_HANDLE_NV_INDEX;
    r = esys_CreateResourceObject(ectx, objectHandle, &objectHandleNode);
    if (r)
        return (int)r;
    objectHandleNode->rsrc.rsrcType = IESYSC_WITHOUT_MISC_RSRC;
    objectHandleNode->rsrc.handle = TPM2_NV_INDEX_FIRST;

    objectHandle = DUMMY_TR_HANDLE_PRIVACY_ADMIN;
    r = esys_CreateResourceObject(ectx, objectHandle, &objectHandleNode);
    if (r)
        return (int)r;
    objectHandleNode->rsrc.rsrcType = IESYSC_WITHOUT_MISC_RSRC;
    objectHandleNode->rsrc.handle = TPM2_RH_ENDORSEMENT;
    *state = (void *)ectx;
    return 0;
}

static int
teardown(void **state)
{
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *ectx = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(ectx, &tcti);
    Esys_Finalize(&ectx);
    free(tcti);
    return 0;
}

static void
test_Startup(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    TPM2_SU startupType = TPM2_SU_CLEAR;
    r = Esys_Startup(esys_context, startupType);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_Shutdown(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    TPM2_SU shutdownType = TPM2_SU_CLEAR;
    r = Esys_Shutdown(esys_context,
                      ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE, shutdownType);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_SelfTest(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    r = Esys_SelfTest(esys_context,
                      ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE, 0);
    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_IncrementalSelfTest(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    TPML_ALG toTest = {0};
    TPML_ALG *toDoList = {0} ;
    r = Esys_IncrementalSelfTest(esys_context,
                                 ESYS_TR_NONE,
                                 ESYS_TR_NONE,
                                 ESYS_TR_NONE, &toTest, &toDoList);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_GetTestResult(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    TPM2B_MAX_BUFFER *outData;
    TPM2_RC testResult;
    r = Esys_GetTestResult(esys_context,
                           ESYS_TR_NONE,
                           ESYS_TR_NONE, ESYS_TR_NONE, &outData, &testResult);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_StartAuthSession(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    ESYS_TR tpmKey_handle = ESYS_TR_NONE;
    ESYS_TR bind_handle = ESYS_TR_NONE;
    TPM2B_NONCE nonceCaller = DUMMY_2B_DATA(.buffer);
    TPM2_SE sessionType = TPM2_SE_HMAC;
    TPMT_SYM_DEF symmetric = {.algorithm = TPM2_ALG_AES,
        .keyBits = {.aes = 128},
        .mode = {.aes = TPM2_ALG_CFB}
    };
    TPMI_ALG_HASH authHash = TPM2_ALG_SHA1;
    ESYS_TR sessionHandle_handle;

    r = Esys_StartAuthSession(esys_context,
                              tpmKey_handle,
                              bind_handle,
                              ESYS_TR_NONE,
                              ESYS_TR_NONE,
                              ESYS_TR_NONE,
                              &nonceCaller,
                              sessionType,
                              &symmetric,
                              authHash, &sessionHandle_handle);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_PolicyRestart(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    r = Esys_PolicyRestart(esys_context,
                           DUMMY_TR_HANDLE_POLICY_SESSION,
                           ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_Create(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);
    TPM2B_SENSITIVE_CREATE inSensitive = { 0 };
    TPM2B_PUBLIC inPublic = DUMMY_IN_PUBLIC_DATA;
    TPM2B_DATA outsideInfo = DUMMY_2B_DATA0;
    TPML_PCR_SELECTION creationPCR = {
        .count = 0,
    };
    TPM2B_PRIVATE *outPrivate;
    TPM2B_PUBLIC *outPublic;
    TPM2B_CREATION_DATA *creationData;
    TPM2B_DIGEST *creationHash;
    TPMT_TK_CREATION *creationTicket;

    r = Esys_Create(esys_context,
                    DUMMY_TR_HANDLE_KEY,
                    ESYS_TR_PASSWORD,
                    ESYS_TR_NONE,
                    ESYS_TR_NONE,
                    &inSensitive,
                    &inPublic,
                    &outsideInfo,
                    &creationPCR,
                    &outPrivate,
                    &outPublic, &creationData, &creationHash, &creationTicket);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_Load(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    TPM2B_PRIVATE inPrivate = DUMMY_2B_DATA(.buffer);
    TPM2B_PUBLIC inPublic = DUMMY_IN_PUBLIC_DATA;
    ESYS_TR objectHandle_handle;
    r = Esys_Load(esys_context,
                  DUMMY_TR_HANDLE_KEY,
                  ESYS_TR_PASSWORD,
                  ESYS_TR_NONE,
                  ESYS_TR_NONE, &inPrivate, &inPublic, &objectHandle_handle);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_LoadExternal(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    TPM2B_PUBLIC inPublic = DUMMY_IN_PUBLIC_DATA;
    ESYS_TR objectHandle_handle;
    r = Esys_LoadExternal(esys_context,
                          ESYS_TR_NONE,
                          ESYS_TR_NONE,
                          ESYS_TR_NONE,
                          NULL, &inPublic, ESYS_TR_RH_OWNER, &objectHandle_handle);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_ReadPublic(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    ESYS_TR objectHandle_handle = DUMMY_TR_HANDLE_KEY;
    TPM2B_PUBLIC *outPublic;
    TPM2B_NAME *name;
    TPM2B_NAME *qualifiedName;
    r = Esys_ReadPublic(esys_context,
                        objectHandle_handle,
                        ESYS_TR_NONE,
                        ESYS_TR_NONE,
                        ESYS_TR_NONE, &outPublic, &name, &qualifiedName);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_ActivateCredential(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    ESYS_TR activateHandle_handle = DUMMY_TR_HANDLE_KEY;
    ESYS_TR keyHandle_handle = DUMMY_TR_HANDLE_KEY;
    TPM2B_ID_OBJECT credentialBlob = DUMMY_2B_DATA(.credential);
    TPM2B_ENCRYPTED_SECRET secret = DUMMY_2B_DATA(.secret);;
    TPM2B_DIGEST *certInfo;
    r = Esys_ActivateCredential(esys_context,
                                activateHandle_handle,
                                keyHandle_handle,
                                ESYS_TR_PASSWORD,
                                ESYS_TR_PASSWORD,
                                ESYS_TR_NONE,
                                &credentialBlob, &secret, &certInfo);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_MakeCredential(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    ESYS_TR handle_handle = ESYS_TR_NONE;
    TPM2B_DIGEST credential = DUMMY_2B_DATA(.buffer);
    TPM2B_NAME objectName = DUMMY_2B_DATA(.name);;
    TPM2B_ID_OBJECT *credentialBlob;
    TPM2B_ENCRYPTED_SECRET *secret;
    r = Esys_MakeCredential(esys_context,
                            handle_handle,
                            ESYS_TR_NONE,
                            ESYS_TR_NONE,
                            ESYS_TR_NONE,
                            &credential, &objectName, &credentialBlob, &secret);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_Unseal(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    ESYS_TR itemHandle_handle = DUMMY_TR_HANDLE_KEY;
    TPM2B_SENSITIVE_DATA *outData;
    r = Esys_Unseal(esys_context,
                    itemHandle_handle,
                    ESYS_TR_PASSWORD, ESYS_TR_NONE, ESYS_TR_NONE, &outData);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_ObjectChangeAuth(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    ESYS_TR objectHandle_handle = DUMMY_TR_HANDLE_KEY;
    ESYS_TR parentHandle_handle = DUMMY_TR_HANDLE_KEY;
    TPM2B_AUTH newAuth = DUMMY_2B_DATA(.buffer);
    TPM2B_PRIVATE *outPrivate;
    r = Esys_ObjectChangeAuth(esys_context,
                              objectHandle_handle,
                              parentHandle_handle,
                              ESYS_TR_PASSWORD,
                              ESYS_TR_NONE,
                              ESYS_TR_NONE, &newAuth, &outPrivate);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_Duplicate(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    ESYS_TR objectHandle_handle = DUMMY_TR_HANDLE_KEY;
    ESYS_TR newParentHandle_handle = DUMMY_TR_HANDLE_KEY;
    TPM2B_DATA encryptionKeyIn = DUMMY_2B_DATA(.buffer);
    TPMT_SYM_DEF_OBJECT symmetricAlg = DUMMY_SYMMETRIC;
    TPM2B_DATA *encryptionKeyOut;
    TPM2B_PRIVATE *duplicate;
    TPM2B_ENCRYPTED_SECRET *outSymSeed;
    r = Esys_Duplicate(esys_context,
                       objectHandle_handle,
                       newParentHandle_handle,
                       ESYS_TR_PASSWORD,
                       ESYS_TR_NONE,
                       ESYS_TR_NONE,
                       &encryptionKeyIn,
                       &symmetricAlg,
                       &encryptionKeyOut, &duplicate, &outSymSeed);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_Rewrap(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    ESYS_TR oldParent_handle = DUMMY_TR_HANDLE_KEY;
    ESYS_TR newParent_handle = DUMMY_TR_HANDLE_KEY;
    TPM2B_PRIVATE inDuplicate = DUMMY_2B_DATA(.buffer);
    TPM2B_NAME name = DUMMY_2B_DATA(.name);
    TPM2B_ENCRYPTED_SECRET inSymSeed = DUMMY_2B_DATA(.secret);
    TPM2B_PRIVATE *outDuplicate;
    TPM2B_ENCRYPTED_SECRET *outSymSeed;
    r = Esys_Rewrap(esys_context,
                    oldParent_handle,
                    newParent_handle,
                    ESYS_TR_PASSWORD,
                    ESYS_TR_NONE,
                    ESYS_TR_NONE,
                    &inDuplicate,
                    &name, &inSymSeed, &outDuplicate, &outSymSeed);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_Import(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    ESYS_TR parentHandle_handle = DUMMY_TR_HANDLE_KEY;
    TPM2B_DATA encryptionKey = DUMMY_2B_DATA(.buffer);
    TPM2B_PUBLIC objectPublic = DUMMY_IN_PUBLIC_DATA;
    TPM2B_PRIVATE duplicate = DUMMY_2B_DATA(.buffer);
    TPM2B_ENCRYPTED_SECRET inSymSeed = DUMMY_2B_DATA(.secret);
    TPMT_SYM_DEF_OBJECT symmetricAlg = DUMMY_SYMMETRIC;
    TPM2B_PRIVATE *outPrivate;
    r = Esys_Import(esys_context,
                    parentHandle_handle,
                    ESYS_TR_PASSWORD,
                    ESYS_TR_NONE,
                    ESYS_TR_NONE,
                    &encryptionKey,
                    &objectPublic,
                    &duplicate, &inSymSeed, &symmetricAlg, &outPrivate);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_RSA_Encrypt(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    ESYS_TR keyHandle_handle = DUMMY_TR_HANDLE_KEY;
    TPM2B_PUBLIC_KEY_RSA message = DUMMY_2B_DATA(.buffer);
    TPMT_RSA_DECRYPT inScheme = DUMMY_RSA_DECRYPT;
    TPM2B_DATA label = DUMMY_2B_DATA(.buffer);
    TPM2B_PUBLIC_KEY_RSA *outData;
    r = Esys_RSA_Encrypt(esys_context,
                         keyHandle_handle,
                         ESYS_TR_NONE,
                         ESYS_TR_NONE,
                         ESYS_TR_NONE, &message, &inScheme, &label, &outData);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_RSA_Decrypt(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    ESYS_TR keyHandle_handle = DUMMY_TR_HANDLE_KEY;
    TPM2B_PUBLIC_KEY_RSA cipherText = DUMMY_2B_DATA(.buffer);
    TPMT_RSA_DECRYPT inScheme = DUMMY_RSA_DECRYPT;
    TPM2B_DATA label = DUMMY_2B_DATA(.buffer);
    TPM2B_PUBLIC_KEY_RSA *message;
    r = Esys_RSA_Decrypt(esys_context,
                         keyHandle_handle,
                         ESYS_TR_PASSWORD,
                         ESYS_TR_NONE,
                         ESYS_TR_NONE,
                         &cipherText, &inScheme, &label, &message);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_ECDH_KeyGen(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    ESYS_TR keyHandle_handle = DUMMY_TR_HANDLE_KEY;
    TPM2B_ECC_POINT *zPoint;
    TPM2B_ECC_POINT *pubPoint;
    r = Esys_ECDH_KeyGen(esys_context,
                         keyHandle_handle,
                         ESYS_TR_NONE,
                         ESYS_TR_NONE, ESYS_TR_NONE, &zPoint, &pubPoint);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_ECDH_ZGen(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    ESYS_TR keyHandle_handle = DUMMY_TR_HANDLE_KEY;
    TPM2B_ECC_POINT inPoint = { 0 };
    TPM2B_ECC_POINT *outPoint;
    r = Esys_ECDH_ZGen(esys_context,
                       keyHandle_handle,
                       ESYS_TR_PASSWORD,
                       ESYS_TR_NONE, ESYS_TR_NONE, &inPoint, &outPoint);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_ECC_Parameters(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    TPMI_ECC_CURVE curveID = TPM2_ECC_BN_P256;
    TPMS_ALGORITHM_DETAIL_ECC *parameters;
    r = Esys_ECC_Parameters(esys_context,
                            ESYS_TR_NONE,
                            ESYS_TR_NONE, ESYS_TR_NONE, curveID, &parameters);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_ZGen_2Phase(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    ESYS_TR keyA_handle = DUMMY_TR_HANDLE_KEY;
    TPM2B_ECC_POINT inQsB = { 0 };
    TPM2B_ECC_POINT inQeB = { 0 };
    TPMI_ECC_KEY_EXCHANGE inScheme = TPM2_ALG_NULL;
    UINT16 counter = 0;
    TPM2B_ECC_POINT *outZ1;
    TPM2B_ECC_POINT *outZ2;
    r = Esys_ZGen_2Phase(esys_context,
                         keyA_handle,
                         ESYS_TR_PASSWORD,
                         ESYS_TR_NONE,
                         ESYS_TR_NONE,
                         &inQsB, &inQeB, inScheme, counter, &outZ1, &outZ2);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_EncryptDecrypt(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    ESYS_TR keyHandle_handle = DUMMY_TR_HANDLE_KEY;
    TPMI_YES_NO decrypt = 0;
    TPMI_ALG_CIPHER_MODE mode = TPM2_ALG_NULL;
    TPM2B_IV ivIn = DUMMY_2B_DATA16(.buffer);
    TPM2B_MAX_BUFFER inData = DUMMY_2B_DATA(.buffer);
    TPM2B_MAX_BUFFER *outData;
    TPM2B_IV *ivOut;
    r = Esys_EncryptDecrypt(esys_context,
                            keyHandle_handle,
                            ESYS_TR_PASSWORD,
                            ESYS_TR_NONE,
                            ESYS_TR_NONE,
                            decrypt, mode, &ivIn, &inData, &outData, &ivOut);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_EncryptDecrypt2(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    ESYS_TR keyHandle_handle = DUMMY_TR_HANDLE_KEY;
    TPM2B_MAX_BUFFER inData = DUMMY_2B_DATA(.buffer);
    TPMI_YES_NO decrypt = 0;
    TPMI_ALG_CIPHER_MODE mode = TPM2_ALG_NULL;
    TPM2B_IV ivIn = DUMMY_2B_DATA16(.buffer);
    TPM2B_MAX_BUFFER *outData;
    TPM2B_IV *ivOut;
    r = Esys_EncryptDecrypt2(esys_context,
                             keyHandle_handle,
                             ESYS_TR_PASSWORD,
                             ESYS_TR_NONE,
                             ESYS_TR_NONE,
                             &inData, decrypt, mode, &ivIn, &outData, &ivOut);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_Hash(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    TPM2B_MAX_BUFFER data = DUMMY_2B_DATA(.buffer);
    TPMI_ALG_HASH hashAlg = TPM2_ALG_SHA1;
    ESYS_TR hierarchy = ESYS_TR_RH_OWNER;
    TPM2B_DIGEST *outHash;
    TPMT_TK_HASHCHECK *validation;
    r = Esys_Hash(esys_context,
                  ESYS_TR_NONE,
                  ESYS_TR_NONE,
                  ESYS_TR_NONE,
                  &data, hashAlg, hierarchy, &outHash, &validation);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_HMAC(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    ESYS_TR handle_handle = DUMMY_TR_HANDLE_KEY;
    TPM2B_MAX_BUFFER buffer = DUMMY_2B_DATA(.buffer);
    TPMI_ALG_HASH hashAlg = TPM2_ALG_SHA1;
    TPM2B_DIGEST *outHMAC;
    r = Esys_HMAC(esys_context,
                  handle_handle,
                  ESYS_TR_PASSWORD,
                  ESYS_TR_NONE, ESYS_TR_NONE, &buffer, hashAlg, &outHMAC);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_MAC(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    ESYS_TR handle_handle = DUMMY_TR_HANDLE_KEY;
    TPM2B_MAX_BUFFER buffer = DUMMY_2B_DATA(.buffer);
    TPMI_ALG_MAC_SCHEME hashAlg = TPM2_ALG_SHA1;
    TPM2B_DIGEST *outMAC;
    r = Esys_MAC(esys_context,
                  handle_handle,
                  ESYS_TR_PASSWORD,
                  ESYS_TR_NONE, ESYS_TR_NONE, &buffer, hashAlg, &outMAC);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_GetRandom(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    UINT16 bytesRequested = 0;
    TPM2B_DIGEST *randomBytes;
    r = Esys_GetRandom(esys_context,
                       ESYS_TR_NONE,
                       ESYS_TR_NONE,
                       ESYS_TR_NONE, bytesRequested, &randomBytes);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_StirRandom(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    TPM2B_SENSITIVE_DATA inData = DUMMY_2B_DATA(.buffer);
    r = Esys_StirRandom(esys_context,
                        ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE, &inData);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_HMAC_Start(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    ESYS_TR handle_handle = DUMMY_TR_HANDLE_KEY;
    TPM2B_AUTH auth = DUMMY_2B_DATA(.buffer);
    TPMI_ALG_HASH hashAlg = TPM2_ALG_SHA1;
    ESYS_TR sequenceHandle_handle;
    r = Esys_HMAC_Start(esys_context,
                        handle_handle,
                        ESYS_TR_PASSWORD,
                        ESYS_TR_NONE,
                        ESYS_TR_NONE, &auth, hashAlg, &sequenceHandle_handle);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_MAC_Start(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    ESYS_TR handle_handle = DUMMY_TR_HANDLE_KEY;
    TPM2B_AUTH auth = DUMMY_2B_DATA(.buffer);
    TPMI_ALG_MAC_SCHEME hashAlg = TPM2_ALG_SHA1;
    ESYS_TR sequenceHandle_handle;
    r = Esys_MAC_Start(esys_context,
                        handle_handle,
                        ESYS_TR_PASSWORD,
                        ESYS_TR_NONE,
                        ESYS_TR_NONE, &auth, hashAlg, &sequenceHandle_handle);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_HashSequenceStart(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    TPM2B_AUTH auth = DUMMY_2B_DATA(.buffer);
    TPMI_ALG_HASH hashAlg = TPM2_ALG_SHA1;
    ESYS_TR sequenceHandle_handle;
    r = Esys_HashSequenceStart(esys_context,
                               ESYS_TR_NONE,
                               ESYS_TR_NONE,
                               ESYS_TR_NONE,
                               &auth, hashAlg, &sequenceHandle_handle);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_SequenceUpdate(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    ESYS_TR sequenceHandle_handle = DUMMY_TR_HANDLE_KEY;
    TPM2B_MAX_BUFFER buffer = DUMMY_2B_DATA(.buffer);
    r = Esys_SequenceUpdate(esys_context,
                            sequenceHandle_handle,
                            ESYS_TR_PASSWORD,
                            ESYS_TR_NONE, ESYS_TR_NONE, &buffer);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_SequenceComplete(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    ESYS_TR sequenceHandle_handle = DUMMY_TR_HANDLE_KEY;
    TPM2B_MAX_BUFFER buffer = DUMMY_2B_DATA(.buffer);
    ESYS_TR hierarchy = ESYS_TR_RH_OWNER;
    TPM2B_DIGEST *result;
    TPMT_TK_HASHCHECK *validation;
    r = Esys_SequenceComplete(esys_context,
                              sequenceHandle_handle,
                              ESYS_TR_PASSWORD,
                              ESYS_TR_NONE,
                              ESYS_TR_NONE,
                              &buffer, hierarchy, &result, &validation);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_EventSequenceComplete(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    ESYS_TR pcrHandle_handle = 16;
    ESYS_TR sequenceHandle_handle = DUMMY_TR_HANDLE_KEY;
    TPM2B_MAX_BUFFER buffer = DUMMY_2B_DATA(.buffer);
    TPML_DIGEST_VALUES *results;
    r = Esys_EventSequenceComplete(esys_context,
                                   pcrHandle_handle,
                                   sequenceHandle_handle,
                                   ESYS_TR_PASSWORD,
                                   ESYS_TR_PASSWORD,
                                   ESYS_TR_NONE, &buffer, &results);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_Certify(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    ESYS_TR objectHandle_handle = DUMMY_TR_HANDLE_KEY;
    ESYS_TR signHandle_handle = DUMMY_TR_HANDLE_KEY;
    TPM2B_DATA qualifyingData = DUMMY_2B_DATA(.buffer);
    TPMT_SIG_SCHEME inScheme = {.scheme = TPM2_ALG_NULL,.details = {} };
    TPM2B_ATTEST *certifyInfo;
    TPMT_SIGNATURE *signature;
    r = Esys_Certify(esys_context,
                     objectHandle_handle,
                     signHandle_handle,
                     ESYS_TR_PASSWORD,
                     ESYS_TR_PASSWORD,
                     ESYS_TR_NONE,
                     &qualifyingData, &inScheme, &certifyInfo, &signature);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_CertifyCreation(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    ESYS_TR signHandle_handle = DUMMY_TR_HANDLE_KEY;
    ESYS_TR objectHandle_handle = DUMMY_TR_HANDLE_KEY;
    TPM2B_DATA qualifyingData = DUMMY_2B_DATA(.buffer);
    TPM2B_DIGEST creationHash = DUMMY_2B_DATA(.buffer);
    TPMT_SIG_SCHEME inScheme = {.scheme = TPM2_ALG_NULL,.details = {} };
    TPMT_TK_CREATION creationTicket = DUMMY_TPMT_TK_CREATION;
    TPM2B_ATTEST *certifyInfo;
    TPMT_SIGNATURE *signature;
    r = Esys_CertifyCreation(esys_context,
                             signHandle_handle,
                             objectHandle_handle,
                             ESYS_TR_PASSWORD,
                             ESYS_TR_NONE,
                             ESYS_TR_NONE,
                             &qualifyingData,
                             &creationHash,
                             &inScheme,
                             &creationTicket, &certifyInfo, &signature);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_Quote(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    ESYS_TR signHandle_handle = DUMMY_TR_HANDLE_KEY;
    TPM2B_DATA qualifyingData = DUMMY_2B_DATA(.buffer);
    TPMT_SIG_SCHEME inScheme = {.scheme = TPM2_ALG_NULL,.details = {} };
    TPML_PCR_SELECTION PCRselect = { 0 };
    TPM2B_ATTEST *quoted;
    TPMT_SIGNATURE *signature;
    r = Esys_Quote(esys_context,
                   signHandle_handle,
                   ESYS_TR_PASSWORD,
                   ESYS_TR_NONE,
                   ESYS_TR_NONE,
                   &qualifyingData, &inScheme, &PCRselect, &quoted, &signature);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_GetSessionAuditDigest(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    ESYS_TR privacyAdminHandle_handle = DUMMY_TR_HANDLE_PRIVACY_ADMIN;
    ESYS_TR signHandle_handle = DUMMY_TR_HANDLE_KEY;
    ESYS_TR sessionHandle_handle = DUMMY_TR_HANDLE_HMAC_SESSION;
    TPM2B_DATA qualifyingData = DUMMY_2B_DATA(.buffer);
    TPMT_SIG_SCHEME inScheme = {.scheme = TPM2_ALG_NULL,.details = {} };
    TPM2B_ATTEST *auditInfo;
    TPMT_SIGNATURE *signature;
    r = Esys_GetSessionAuditDigest(esys_context,
                                   privacyAdminHandle_handle,
                                   signHandle_handle,
                                   sessionHandle_handle,
                                   ESYS_TR_PASSWORD,
                                   ESYS_TR_PASSWORD,
                                   ESYS_TR_NONE,
                                   &qualifyingData,
                                   &inScheme, &auditInfo, &signature);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_GetCommandAuditDigest(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    ESYS_TR privacyHandle_handle = DUMMY_TR_HANDLE_PRIVACY_ADMIN;
    ESYS_TR signHandle_handle = DUMMY_TR_HANDLE_KEY;
    TPM2B_DATA qualifyingData = DUMMY_2B_DATA(.buffer);
    TPMT_SIG_SCHEME inScheme = {.scheme = TPM2_ALG_NULL,.details = {} };
    TPM2B_ATTEST *auditInfo;
    TPMT_SIGNATURE *signature;
    r = Esys_GetCommandAuditDigest(esys_context,
                                   privacyHandle_handle,
                                   signHandle_handle,
                                   ESYS_TR_PASSWORD,
                                   ESYS_TR_PASSWORD,
                                   ESYS_TR_NONE,
                                   &qualifyingData,
                                   &inScheme, &auditInfo, &signature);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_GetTime(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    ESYS_TR privacyAdminHandle_handle = DUMMY_TR_HANDLE_PRIVACY_ADMIN;
    ESYS_TR signHandle_handle = DUMMY_TR_HANDLE_KEY;
    TPM2B_DATA qualifyingData = DUMMY_2B_DATA(.buffer);
    TPMT_SIG_SCHEME inScheme = {.scheme = TPM2_ALG_NULL,.details = {} };
    TPM2B_ATTEST *timeInfo;
    TPMT_SIGNATURE *signature;
    r = Esys_GetTime(esys_context,
                     privacyAdminHandle_handle,
                     signHandle_handle,
                     ESYS_TR_PASSWORD,
                     ESYS_TR_PASSWORD,
                     ESYS_TR_NONE,
                     &qualifyingData, &inScheme, &timeInfo, &signature);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_Commit(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    ESYS_TR signHandle_handle = DUMMY_TR_HANDLE_KEY;
    TPM2B_ECC_POINT P1 = { 0 };
    TPM2B_SENSITIVE_DATA s2 = DUMMY_2B_DATA(.buffer);
    TPM2B_ECC_PARAMETER y2 = { 0 };
    TPM2B_ECC_POINT *K;
    TPM2B_ECC_POINT *L;
    TPM2B_ECC_POINT *E;
    UINT16 counter;
    r = Esys_Commit(esys_context,
                    signHandle_handle,
                    ESYS_TR_PASSWORD,
                    ESYS_TR_NONE,
                    ESYS_TR_NONE, &P1, &s2, &y2, &K, &L, &E, &counter);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_EC_Ephemeral(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    TPMI_ECC_CURVE curveID = TPM2_ECC_BN_P256;
    TPM2B_ECC_POINT *Q;
    UINT16 counter;
    r = Esys_EC_Ephemeral(esys_context,
                          ESYS_TR_NONE,
                          ESYS_TR_NONE, ESYS_TR_NONE, curveID, &Q, &counter);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_VerifySignature(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    ESYS_TR keyHandle_handle = DUMMY_TR_HANDLE_KEY;
    TPM2B_DIGEST digest = DUMMY_2B_DATA(.buffer);
    TPMT_SIGNATURE signature = DUMMY_TPMT_SIGNATURE;
    TPMT_TK_VERIFIED *validation;
    r = Esys_VerifySignature(esys_context,
                             keyHandle_handle,
                             ESYS_TR_NONE,
                             ESYS_TR_NONE,
                             ESYS_TR_NONE, &digest, &signature, &validation);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_Sign(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    ESYS_TR keyHandle_handle = DUMMY_TR_HANDLE_KEY;
    TPM2B_DIGEST digest = DUMMY_2B_DATA(.buffer);
    TPMT_SIG_SCHEME inScheme = {.scheme = TPM2_ALG_NULL,.details = {} };
    TPMT_TK_HASHCHECK validation = DUMMY_TPMT_TK_HASHCHECK;
    TPMT_SIGNATURE *signature;
    r = Esys_Sign(esys_context,
                  keyHandle_handle,
                  ESYS_TR_PASSWORD,
                  ESYS_TR_NONE,
                  ESYS_TR_NONE, &digest, &inScheme, &validation, &signature);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_SetCommandCodeAuditStatus(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    ESYS_TR auth_handle = DUMMY_TR_HANDLE_HIERARCHY_PLATFORM;
    TPMI_ALG_HASH auditAlg = TPM2_ALG_SHA1;
    TPML_CC setList = { 0 };
    TPML_CC clearList = { 0 };
    r = Esys_SetCommandCodeAuditStatus(esys_context,
                                       auth_handle,
                                       ESYS_TR_PASSWORD,
                                       ESYS_TR_NONE,
                                       ESYS_TR_NONE,
                                       auditAlg, &setList, &clearList);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_PCR_Extend(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    ESYS_TR pcrHandle_handle = 16;
    TPML_DIGEST_VALUES digests = { 0 };
    r = Esys_PCR_Extend(esys_context,
                        pcrHandle_handle,
                        ESYS_TR_PASSWORD, ESYS_TR_NONE, ESYS_TR_NONE, &digests);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_PCR_Event(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    ESYS_TR pcrHandle_handle = 16;
    TPM2B_EVENT eventData = DUMMY_2B_DATA(.buffer);
    TPML_DIGEST_VALUES *digests;
    r = Esys_PCR_Event(esys_context,
                       pcrHandle_handle,
                       ESYS_TR_PASSWORD,
                       ESYS_TR_NONE, ESYS_TR_NONE, &eventData, &digests);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_PCR_Read(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    TPML_PCR_SELECTION pcrSelectionIn = { 0 };
    TPML_PCR_SELECTION *pcrSelectionOut;
    TPML_DIGEST *pcrValues;
    UINT32 pcrUpdateCounter;
    r = Esys_PCR_Read(esys_context,
                      ESYS_TR_NONE,
                      ESYS_TR_NONE,
                      ESYS_TR_NONE,
                      &pcrSelectionIn,
                      &pcrUpdateCounter, &pcrSelectionOut, &pcrValues);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_PCR_Allocate(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    ESYS_TR authHandle_handle = DUMMY_TR_HANDLE_HIERARCHY_PLATFORM;
    TPML_PCR_SELECTION pcrAllocation = { 0 };
    TPMI_YES_NO allocationSuccess;
    UINT32 maxPCR;
    UINT32 sizeNeeded;
    UINT32 sizeAvailable;
    r = Esys_PCR_Allocate(esys_context,
                          authHandle_handle,
                          ESYS_TR_PASSWORD,
                          ESYS_TR_NONE,
                          ESYS_TR_NONE,
                          &pcrAllocation,
                          &allocationSuccess,
                          &maxPCR, &sizeNeeded, &sizeAvailable);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_PCR_SetAuthPolicy(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    ESYS_TR authHandle_handle = DUMMY_TR_HANDLE_HIERARCHY_PLATFORM;
    TPM2B_DIGEST authPolicy = DUMMY_2B_DATA(.buffer);
    TPMI_ALG_HASH hashAlg = TPM2_ALG_SHA1;
    TPMI_DH_PCR pcrNum = 0;
    r = Esys_PCR_SetAuthPolicy(esys_context,
                               authHandle_handle,
                               ESYS_TR_PASSWORD,
                               ESYS_TR_NONE,
                               ESYS_TR_NONE, &authPolicy, hashAlg, pcrNum);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_PCR_SetAuthValue(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    ESYS_TR pcrHandle_handle = 16;
    TPM2B_DIGEST auth = DUMMY_2B_DATA(.buffer);
    r = Esys_PCR_SetAuthValue(esys_context,
                              pcrHandle_handle,
                              ESYS_TR_PASSWORD,
                              ESYS_TR_NONE, ESYS_TR_NONE, &auth);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_PCR_Reset(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    ESYS_TR pcrHandle_handle = 16;
    r = Esys_PCR_Reset(esys_context,
                       pcrHandle_handle,
                       ESYS_TR_PASSWORD, ESYS_TR_NONE, ESYS_TR_NONE);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_PolicySigned(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    ESYS_TR authObject_handle = DUMMY_TR_HANDLE_KEY;
    ESYS_TR policySession_handle = DUMMY_TR_HANDLE_POLICY_SESSION;
    TPM2B_NONCE nonceTPM = DUMMY_2B_DATA(.buffer);
    TPM2B_DIGEST cpHashA = DUMMY_2B_DATA(.buffer);
    TPM2B_NONCE policyRef = DUMMY_2B_DATA(.buffer);
    INT32 expiration = 0;
    TPMT_SIGNATURE auth = DUMMY_TPMT_SIGNATURE;
    TPM2B_TIMEOUT *timeout;
    TPMT_TK_AUTH *policyTicket;
    r = Esys_PolicySigned(esys_context,
                          authObject_handle,
                          policySession_handle,
                          ESYS_TR_NONE,
                          ESYS_TR_NONE,
                          ESYS_TR_NONE,
                          &nonceTPM,
                          &cpHashA,
                          &policyRef,
                          expiration, &auth, &timeout, &policyTicket);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_PolicySecret(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    ESYS_TR authHandle_handle = DUMMY_TR_HANDLE_HIERARCHY_PLATFORM;
    ESYS_TR policySession_handle = DUMMY_TR_HANDLE_POLICY_SESSION;
    TPM2B_NONCE nonceTPM = DUMMY_2B_DATA(.buffer);
    TPM2B_DIGEST cpHashA = DUMMY_2B_DATA(.buffer);
    TPM2B_NONCE policyRef = DUMMY_2B_DATA(.buffer);
    INT32 expiration = 0;
    TPM2B_TIMEOUT *timeout;
    TPMT_TK_AUTH *policyTicket;
    r = Esys_PolicySecret(esys_context,
                          authHandle_handle,
                          policySession_handle,
                          ESYS_TR_PASSWORD,
                          ESYS_TR_NONE,
                          ESYS_TR_NONE,
                          &nonceTPM,
                          &cpHashA,
                          &policyRef, expiration, &timeout, &policyTicket);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_PolicyTicket(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    ESYS_TR policySession_handle = DUMMY_TR_HANDLE_POLICY_SESSION;
    TPM2B_TIMEOUT timeout = DUMMY_2B_DATA(.buffer);
    TPM2B_DIGEST cpHashA = DUMMY_2B_DATA(.buffer);
    TPM2B_NONCE policyRef = DUMMY_2B_DATA(.buffer);
    TPM2B_NAME authName = DUMMY_2B_DATA(.name);
    TPMT_TK_AUTH ticket = DUMMY_TPMT_TK_AUTH;
    r = Esys_PolicyTicket(esys_context,
                          policySession_handle,
                          ESYS_TR_NONE,
                          ESYS_TR_NONE,
                          ESYS_TR_NONE,
                          &timeout, &cpHashA, &policyRef, &authName, &ticket);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_PolicyOR(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    ESYS_TR policySession_handle = DUMMY_TR_HANDLE_POLICY_SESSION;
    TPML_DIGEST pHashList = { 0 };
    r = Esys_PolicyOR(esys_context,
                      policySession_handle,
                      ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE, &pHashList);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_PolicyPCR(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    ESYS_TR policySession_handle = DUMMY_TR_HANDLE_POLICY_SESSION;
    TPM2B_DIGEST pcrDigest = DUMMY_2B_DATA(.buffer);
    TPML_PCR_SELECTION pcrs = { 0 };
    r = Esys_PolicyPCR(esys_context,
                       policySession_handle,
                       ESYS_TR_NONE,
                       ESYS_TR_NONE, ESYS_TR_NONE, &pcrDigest, &pcrs);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_PolicyLocality(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    ESYS_TR policySession = DUMMY_TR_HANDLE_POLICY_SESSION;
    TPMA_LOCALITY locality = TPMA_LOCALITY_TPM2_LOC_ZERO;
    r = Esys_PolicyLocality(esys_context, policySession,
                            ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE, locality);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_PolicyNV(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    ESYS_TR authHandle_handle = DUMMY_TR_HANDLE_HIERARCHY_PLATFORM;
    ESYS_TR nvIndex_handle = DUMMY_TR_HANDLE_NV_INDEX;
    ESYS_TR policySession_handle = DUMMY_TR_HANDLE_POLICY_SESSION;
    TPM2B_OPERAND operandB = DUMMY_2B_DATA(.buffer);
    UINT16 offset = 0;
    TPM2_EO operation = 0;
    r = Esys_PolicyNV(esys_context,
                      authHandle_handle,
                      nvIndex_handle,
                      policySession_handle,
                      ESYS_TR_PASSWORD,
                      ESYS_TR_NONE, ESYS_TR_NONE, &operandB, offset, operation);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_PolicyCounterTimer(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    ESYS_TR policySession_handle = DUMMY_TR_HANDLE_POLICY_SESSION;
    TPM2B_OPERAND operandB = DUMMY_2B_DATA(.buffer);
    UINT16 offset = 0;
    TPM2_EO operation = 0;
    r = Esys_PolicyCounterTimer(esys_context,
                                policySession_handle,
                                ESYS_TR_NONE,
                                ESYS_TR_NONE,
                                ESYS_TR_NONE, &operandB, offset, operation);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_PolicyCommandCode(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    ESYS_TR policySession_handle = DUMMY_TR_HANDLE_POLICY_SESSION;
    TPM2_CC code = TPM2_CC_FIRST;
    r = Esys_PolicyCommandCode(esys_context,
                               policySession_handle,
                               ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE, code);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_PolicyPhysicalPresence(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    ESYS_TR policySession_handle = DUMMY_TR_HANDLE_POLICY_SESSION;
    r = Esys_PolicyPhysicalPresence(esys_context,
                                    policySession_handle,
                                    ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_PolicyCpHash(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    ESYS_TR policySession = DUMMY_TR_HANDLE_POLICY_SESSION;
    TPM2B_DIGEST cpHashA = DUMMY_2B_DATA(.buffer);
    r = Esys_PolicyCpHash(esys_context,
                          policySession,
                          ESYS_TR_NONE,
                          ESYS_TR_NONE, ESYS_TR_NONE, &cpHashA);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_PolicyNameHash(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    ESYS_TR policySession = DUMMY_TR_HANDLE_POLICY_SESSION;
    TPM2B_DIGEST nameHash = DUMMY_2B_DATA(.buffer);
    r = Esys_PolicyNameHash(esys_context,
                            policySession,
                            ESYS_TR_NONE,
                            ESYS_TR_NONE,
                            ESYS_TR_NONE, &nameHash);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_PolicyDuplicationSelect(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    ESYS_TR policySession = DUMMY_TR_HANDLE_POLICY_SESSION;
    TPM2B_NAME objectName = DUMMY_2B_DATA(.name);
    TPM2B_NAME newParentName = DUMMY_2B_DATA(.name);
    TPMI_YES_NO includeObject = 0;
    r = Esys_PolicyDuplicationSelect(esys_context,
                                     policySession,
                                     ESYS_TR_NONE,
                                     ESYS_TR_NONE,
                                     ESYS_TR_NONE,
                                     &objectName,
                                     &newParentName, includeObject);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_PolicyAuthorize(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    ESYS_TR policySession_handle = DUMMY_TR_HANDLE_POLICY_SESSION;
    TPM2B_DIGEST approvedPolicy = DUMMY_2B_DATA(.buffer);
    TPM2B_NONCE policyRef = DUMMY_2B_DATA(.buffer);
    TPM2B_NAME keySign = DUMMY_2B_DATA(.name);
    TPMT_TK_VERIFIED checkTicket = DUMMY_TPMT_TK_VERIFIED;
    r = Esys_PolicyAuthorize(esys_context,
                             policySession_handle,
                             ESYS_TR_NONE,
                             ESYS_TR_NONE,
                             ESYS_TR_NONE,
                             &approvedPolicy,
                             &policyRef, &keySign, &checkTicket);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_PolicyAuthValue(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    ESYS_TR policySession_handle = DUMMY_TR_HANDLE_POLICY_SESSION;
    r = Esys_PolicyAuthValue(esys_context,
                             policySession_handle,
                             ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_PolicyPassword(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    ESYS_TR policySession_handle = DUMMY_TR_HANDLE_POLICY_SESSION;
    r = Esys_PolicyPassword(esys_context,
                            policySession_handle,
                            ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_PolicyGetDigest(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    ESYS_TR policySession_handle = DUMMY_TR_HANDLE_POLICY_SESSION;
    TPM2B_DIGEST *policyDigest;
    r = Esys_PolicyGetDigest(esys_context,
                             policySession_handle,
                             ESYS_TR_NONE,
                             ESYS_TR_NONE, ESYS_TR_NONE, &policyDigest);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_PolicyNvWritten(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    ESYS_TR policySession_handle = DUMMY_TR_HANDLE_POLICY_SESSION;
    TPMI_YES_NO writtenSet = 0;
    r = Esys_PolicyNvWritten(esys_context,
                             policySession_handle,
                             ESYS_TR_NONE,
                             ESYS_TR_NONE, ESYS_TR_NONE, writtenSet);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_PolicyTemplate(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    ESYS_TR policySession = DUMMY_TR_HANDLE_POLICY_SESSION;
    TPM2B_DIGEST templateHash = DUMMY_2B_DATA(.buffer);
    r = Esys_PolicyTemplate(esys_context,
                            policySession,
                            ESYS_TR_NONE,
                            ESYS_TR_NONE,
                            ESYS_TR_NONE, &templateHash);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_PolicyAuthorizeNV(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    ESYS_TR authHandle_handle = DUMMY_TR_HANDLE_HIERARCHY_PLATFORM;
    ESYS_TR nvIndex_handle = DUMMY_TR_HANDLE_NV_INDEX;
    ESYS_TR policySession_handle = DUMMY_TR_HANDLE_POLICY_SESSION;
    r = Esys_PolicyAuthorizeNV(esys_context,
                               authHandle_handle,
                               nvIndex_handle,
                               policySession_handle,
                               ESYS_TR_PASSWORD, ESYS_TR_NONE, ESYS_TR_NONE);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_CreatePrimary(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    ESYS_TR primaryHandle_handle = DUMMY_TR_HANDLE_HIERARCHY_PLATFORM;
    TPM2B_SENSITIVE_CREATE inSensitive = { 0 };
    TPM2B_PUBLIC inPublic = DUMMY_IN_PUBLIC_DATA;
    TPM2B_DATA outsideInfo = DUMMY_2B_DATA(.buffer);
    TPML_PCR_SELECTION creationPCR = { 0 };
    ESYS_TR objectHandle_handle;
    TPM2B_PUBLIC *outPublic;
    TPM2B_CREATION_DATA *creationData;
    TPM2B_DIGEST *creationHash;
    TPMT_TK_CREATION *creationTicket;
    r = Esys_CreatePrimary(esys_context,
                           primaryHandle_handle,
                           ESYS_TR_PASSWORD,
                           ESYS_TR_NONE,
                           ESYS_TR_NONE,
                           &inSensitive,
                           &inPublic,
                           &outsideInfo,
                           &creationPCR,
                           &objectHandle_handle,
                           &outPublic,
                           &creationData, &creationHash, &creationTicket);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_HierarchyControl(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    ESYS_TR authHandle_handle = DUMMY_TR_HANDLE_HIERARCHY_PLATFORM;
    ESYS_TR enable = ESYS_TR_RH_OWNER;
    TPMI_YES_NO state2 = 0;
    r = Esys_HierarchyControl(esys_context,
                              authHandle_handle,
                              ESYS_TR_PASSWORD,
                              ESYS_TR_NONE, ESYS_TR_NONE, enable, state2);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_SetPrimaryPolicy(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    ESYS_TR authHandle_handle = DUMMY_TR_HANDLE_HIERARCHY_PLATFORM;
    TPM2B_DIGEST authPolicy = DUMMY_2B_DATA(.buffer);
    TPMI_ALG_HASH hashAlg = TPM2_ALG_SHA1;
    r = Esys_SetPrimaryPolicy(esys_context,
                              authHandle_handle,
                              ESYS_TR_PASSWORD,
                              ESYS_TR_NONE, ESYS_TR_NONE, &authPolicy, hashAlg);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_ChangePPS(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    ESYS_TR authHandle_handle = DUMMY_TR_HANDLE_HIERARCHY_PLATFORM;
    r = Esys_ChangePPS(esys_context,
                       authHandle_handle,
                       ESYS_TR_PASSWORD, ESYS_TR_NONE, ESYS_TR_NONE);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_ChangeEPS(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    ESYS_TR authHandle_handle = DUMMY_TR_HANDLE_HIERARCHY_PLATFORM;
    r = Esys_ChangeEPS(esys_context,
                       authHandle_handle,
                       ESYS_TR_PASSWORD, ESYS_TR_NONE, ESYS_TR_NONE);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_Clear(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    ESYS_TR authHandle_handle = DUMMY_TR_HANDLE_HIERARCHY_PLATFORM;
    r = Esys_Clear(esys_context,
                   authHandle_handle,
                   ESYS_TR_PASSWORD, ESYS_TR_NONE, ESYS_TR_NONE);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_ClearControl(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    ESYS_TR auth_handle = DUMMY_TR_HANDLE_HIERARCHY_PLATFORM;
    TPMI_YES_NO disable = 0;
    r = Esys_ClearControl(esys_context,
                          auth_handle,
                          ESYS_TR_PASSWORD,
                          ESYS_TR_NONE, ESYS_TR_NONE, disable);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_HierarchyChangeAuth(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    ESYS_TR authHandle_handle = DUMMY_TR_HANDLE_HIERARCHY_PLATFORM;
    TPM2B_AUTH newAuth = DUMMY_2B_DATA(.buffer);
    r = Esys_HierarchyChangeAuth(esys_context,
                                 authHandle_handle,
                                 ESYS_TR_PASSWORD,
                                 ESYS_TR_NONE, ESYS_TR_NONE, &newAuth);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_DictionaryAttackLockReset(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    ESYS_TR lockHandle_handle = DUMMY_TR_HANDLE_LOCKOUT;;
    r = Esys_DictionaryAttackLockReset(esys_context,
                                       lockHandle_handle,
                                       ESYS_TR_PASSWORD,
                                       ESYS_TR_NONE, ESYS_TR_NONE);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_DictionaryAttackParameters(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    ESYS_TR lockHandle_handle = DUMMY_TR_HANDLE_LOCKOUT;
    UINT32 newMaxTries = 0;
    UINT32 newRecoveryTime = 0;
    UINT32 lockoutRecovery = 0;
    r = Esys_DictionaryAttackParameters(esys_context,
                                        lockHandle_handle,
                                        ESYS_TR_PASSWORD,
                                        ESYS_TR_NONE,
                                        ESYS_TR_NONE,
                                        newMaxTries,
                                        newRecoveryTime, lockoutRecovery);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_PP_Commands(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    ESYS_TR auth_handle = DUMMY_TR_HANDLE_HIERARCHY_PLATFORM;
    TPML_CC setList = { 0 };
    TPML_CC clearList = { 0 };
    r = Esys_PP_Commands(esys_context,
                         auth_handle,
                         ESYS_TR_PASSWORD,
                         ESYS_TR_NONE, ESYS_TR_NONE, &setList, &clearList);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_SetAlgorithmSet(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    ESYS_TR authHandle_handle = DUMMY_TR_HANDLE_HIERARCHY_PLATFORM;
    UINT32 algorithmSet = 0;
    r = Esys_SetAlgorithmSet(esys_context,
                             authHandle_handle,
                             ESYS_TR_PASSWORD,
                             ESYS_TR_NONE, ESYS_TR_NONE, algorithmSet);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_FieldUpgradeStart(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    ESYS_TR authorization_handle = DUMMY_TR_HANDLE_HIERARCHY_PLATFORM;;
    ESYS_TR keyHandle_handle = DUMMY_TR_HANDLE_KEY;
    TPM2B_DIGEST fuDigest = DUMMY_2B_DATA(.buffer);
    TPMT_SIGNATURE manifestSignature = DUMMY_TPMT_SIGNATURE;
    r = Esys_FieldUpgradeStart(esys_context,
                               authorization_handle,
                               keyHandle_handle,
                               ESYS_TR_PASSWORD,
                               ESYS_TR_NONE,
                               ESYS_TR_NONE, &fuDigest, &manifestSignature);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_FieldUpgradeData(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    TPM2B_MAX_BUFFER fuData = DUMMY_2B_DATA(.buffer);
    TPMT_HA *nextDigest;
    TPMT_HA *firstDigest;
    r = Esys_FieldUpgradeData(esys_context,
                              ESYS_TR_NONE,
                              ESYS_TR_NONE,
                              ESYS_TR_NONE, &fuData, &nextDigest, &firstDigest);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_FirmwareRead(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    UINT32 sequenceNumber = 0;
    TPM2B_MAX_BUFFER *fuData;
    r = Esys_FirmwareRead(esys_context,
                          ESYS_TR_NONE,
                          ESYS_TR_NONE, ESYS_TR_NONE, sequenceNumber, &fuData);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_ContextSave(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    ESYS_TR saveHandle_handle = DUMMY_TR_HANDLE_KEY;
    TPMS_CONTEXT *context;
    r = Esys_ContextSave(esys_context, saveHandle_handle, &context);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_ContextLoad(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    TPMS_CONTEXT context = { 0 };
    ESYS_TR loadedHandle_handle;

    context.contextBlob.size = 0x100;
    context.savedHandle = TPM2_TRANSIENT_FIRST;
    context.hierarchy = TPM2_RH_OWNER;
    r = Esys_ContextLoad(esys_context, &context, &loadedHandle_handle);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_FlushContext(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    ESYS_TR flushHandle_handle = DUMMY_TR_HANDLE_KEY;
    r = Esys_FlushContext(esys_context, flushHandle_handle);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_EvictControl(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    ESYS_TR auth_handle = DUMMY_TR_HANDLE_HIERARCHY_PLATFORM;
    ESYS_TR objectHandle_handle = DUMMY_TR_HANDLE_KEY;
    TPMI_DH_PERSISTENT persistentHandle = TPM2_PERSISTENT_FIRST;
    ESYS_TR newObjectHandle_handle;
    r = Esys_EvictControl(esys_context,
                          auth_handle,
                          objectHandle_handle,
                          ESYS_TR_PASSWORD,
                          ESYS_TR_NONE,
                          ESYS_TR_NONE,
                          persistentHandle, &newObjectHandle_handle);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_ReadClock(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    TPMS_TIME_INFO *currentTime;
    r = Esys_ReadClock(esys_context,
                       ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE, &currentTime);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_ClockSet(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    ESYS_TR auth_handle = DUMMY_TR_HANDLE_HIERARCHY_PLATFORM;
    UINT64 newTime = 0;
    r = Esys_ClockSet(esys_context,
                      auth_handle,
                      ESYS_TR_PASSWORD, ESYS_TR_NONE, ESYS_TR_NONE, newTime);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_ClockRateAdjust(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    ESYS_TR auth_handle = DUMMY_TR_HANDLE_HIERARCHY_PLATFORM;
    TPM2_CLOCK_ADJUST rateAdjust = 0;
    r = Esys_ClockRateAdjust(esys_context,
                             auth_handle,
                             ESYS_TR_PASSWORD,
                             ESYS_TR_NONE, ESYS_TR_NONE, rateAdjust);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_GetCapability(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    TPM2_CAP capability = 0;
    UINT32 property = 0;
    UINT32 propertyCount = 0;
    TPMS_CAPABILITY_DATA *capabilityData;
    TPMI_YES_NO moreData;
    r = Esys_GetCapability(esys_context,
                           ESYS_TR_NONE,
                           ESYS_TR_NONE,
                           ESYS_TR_NONE,
                           capability,
                           property, propertyCount, &moreData, &capabilityData);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_TestParms(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    TPMT_PUBLIC_PARMS parameters = DUMMY_TPMT_PUBLIC_PARAMS;
    r = Esys_TestParms(esys_context,
                       ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE, &parameters);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_NV_DefineSpace(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    ESYS_TR authHandle_handle = DUMMY_TR_HANDLE_HIERARCHY_PLATFORM;
    TPM2B_AUTH auth = DUMMY_2B_DATA(.buffer);
    TPM2B_NV_PUBLIC publicInfo = {
        .size = 0,
        .nvPublic = {
                     .nvIndex = TPM2_NV_INDEX_FIRST,
                     .nameAlg = TPM2_ALG_SHA1,
                     .attributes = (TPMA_NV_PPWRITE |
                                    TPMA_NV_AUTHWRITE |
                                    1 << TPMA_NV_TPM2_NT_SHIFT |
                                    TPMA_NV_WRITE_STCLEAR |
                                    TPMA_NV_PPREAD |
                                    TPMA_NV_AUTHREAD | TPMA_NV_PLATFORMCREATE),
                     .authPolicy = {
                                    .size = 0,
                                    .buffer = {},
                                    },
                     .dataSize = 32,
                     }
    };
    ESYS_TR nvHandle_handle;
    r = Esys_NV_DefineSpace(esys_context,
                            authHandle_handle,
                            ESYS_TR_PASSWORD,
                            ESYS_TR_NONE,
                            ESYS_TR_NONE, &auth, &publicInfo, &nvHandle_handle);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_NV_UndefineSpace(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    ESYS_TR authHandle_handle = DUMMY_TR_HANDLE_HIERARCHY_PLATFORM;
    ESYS_TR nvIndex_handle = DUMMY_TR_HANDLE_NV_INDEX;
    r = Esys_NV_UndefineSpace(esys_context,
                              authHandle_handle,
                              nvIndex_handle,
                              ESYS_TR_PASSWORD, ESYS_TR_NONE, ESYS_TR_NONE);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_NV_UndefineSpaceSpecial(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    ESYS_TR nvIndex_handle = DUMMY_TR_HANDLE_NV_INDEX;
    ESYS_TR platform_handle = DUMMY_TR_HANDLE_HIERARCHY_PLATFORM;
    r = Esys_NV_UndefineSpaceSpecial(esys_context,
                                     nvIndex_handle,
                                     platform_handle,
                                     ESYS_TR_PASSWORD,
                                     ESYS_TR_PASSWORD, ESYS_TR_NONE);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_NV_ReadPublic(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    ESYS_TR nvIndex_handle = DUMMY_TR_HANDLE_NV_INDEX;
    TPM2B_NV_PUBLIC *nvPublic;
    TPM2B_NAME *nvName;
    r = Esys_NV_ReadPublic(esys_context,
                           nvIndex_handle,
                           ESYS_TR_NONE,
                           ESYS_TR_NONE, ESYS_TR_NONE, &nvPublic, &nvName);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_NV_Write(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    ESYS_TR authHandle_handle = DUMMY_TR_HANDLE_HIERARCHY_PLATFORM;
    ESYS_TR nvIndex_handle = DUMMY_TR_HANDLE_NV_INDEX;
    TPM2B_MAX_NV_BUFFER data = DUMMY_2B_DATA(.buffer);
    UINT16 offset = 0;
    r = Esys_NV_Write(esys_context,
                      authHandle_handle,
                      nvIndex_handle,
                      ESYS_TR_PASSWORD,
                      ESYS_TR_NONE, ESYS_TR_NONE, &data, offset);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_NV_Increment(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    ESYS_TR authHandle_handle = DUMMY_TR_HANDLE_HIERARCHY_PLATFORM;
    ESYS_TR nvIndex_handle = DUMMY_TR_HANDLE_NV_INDEX;
    r = Esys_NV_Increment(esys_context,
                          authHandle_handle,
                          nvIndex_handle,
                          ESYS_TR_PASSWORD, ESYS_TR_NONE, ESYS_TR_NONE);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_NV_Extend(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    ESYS_TR authHandle_handle = DUMMY_TR_HANDLE_HIERARCHY_PLATFORM;
    ESYS_TR nvIndex_handle = DUMMY_TR_HANDLE_NV_INDEX;
    TPM2B_MAX_NV_BUFFER data = DUMMY_2B_DATA(.buffer);
    r = Esys_NV_Extend(esys_context,
                       authHandle_handle,
                       nvIndex_handle,
                       ESYS_TR_PASSWORD, ESYS_TR_NONE, ESYS_TR_NONE, &data);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_NV_SetBits(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    ESYS_TR authHandle_handle = DUMMY_TR_HANDLE_HIERARCHY_PLATFORM;
    ESYS_TR nvIndex_handle = DUMMY_TR_HANDLE_NV_INDEX;
    UINT64 bits = 0;
    r = Esys_NV_SetBits(esys_context,
                        authHandle_handle,
                        nvIndex_handle,
                        ESYS_TR_PASSWORD, ESYS_TR_NONE, ESYS_TR_NONE, bits);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_NV_WriteLock(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    ESYS_TR authHandle_handle = DUMMY_TR_HANDLE_HIERARCHY_PLATFORM;
    ESYS_TR nvIndex_handle = DUMMY_TR_HANDLE_NV_INDEX;
    r = Esys_NV_WriteLock(esys_context,
                          authHandle_handle,
                          nvIndex_handle,
                          ESYS_TR_PASSWORD, ESYS_TR_NONE, ESYS_TR_NONE);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_NV_GlobalWriteLock(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    ESYS_TR authHandle_handle = DUMMY_TR_HANDLE_HIERARCHY_PLATFORM;
    r = Esys_NV_GlobalWriteLock(esys_context,
                                authHandle_handle,
                                ESYS_TR_PASSWORD, ESYS_TR_NONE, ESYS_TR_NONE);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_NV_Read(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    ESYS_TR authHandle_handle = DUMMY_TR_HANDLE_HIERARCHY_PLATFORM;
    ESYS_TR nvIndex_handle = DUMMY_TR_HANDLE_NV_INDEX;
    UINT16 size = 0;
    UINT16 offset = 0;
    TPM2B_MAX_NV_BUFFER *data;
    r = Esys_NV_Read(esys_context,
                     authHandle_handle,
                     nvIndex_handle,
                     ESYS_TR_PASSWORD,
                     ESYS_TR_NONE, ESYS_TR_NONE, size, offset, &data);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_NV_ReadLock(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    ESYS_TR authHandle_handle = DUMMY_TR_HANDLE_HIERARCHY_PLATFORM;
    ESYS_TR nvIndex_handle = DUMMY_TR_HANDLE_NV_INDEX;
    r = Esys_NV_ReadLock(esys_context,
                         authHandle_handle,
                         nvIndex_handle,
                         ESYS_TR_PASSWORD, ESYS_TR_NONE, ESYS_TR_NONE);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_NV_ChangeAuth(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    ESYS_TR nvIndex_handle = DUMMY_TR_HANDLE_NV_INDEX;
    TPM2B_AUTH newAuth = DUMMY_2B_DATA(.buffer);
    r = Esys_NV_ChangeAuth(esys_context,
                           nvIndex_handle,
                           ESYS_TR_PASSWORD,
                           ESYS_TR_NONE, ESYS_TR_NONE, &newAuth);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_NV_Certify(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    ESYS_TR signHandle_handle = DUMMY_TR_HANDLE_KEY;
    ESYS_TR authHandle_handle = DUMMY_TR_HANDLE_HIERARCHY_PLATFORM;
    ESYS_TR nvIndex_handle = DUMMY_TR_HANDLE_NV_INDEX;
    TPM2B_DATA qualifyingData = DUMMY_2B_DATA(.buffer);
    TPMT_SIG_SCHEME inScheme = {.scheme = TPM2_ALG_NULL,.details = {} };
    UINT16 size = 0;
    UINT16 offset = 0;
    TPM2B_ATTEST *certifyInfo;
    TPMT_SIGNATURE *signature;
    r = Esys_NV_Certify(esys_context,
                        signHandle_handle,
                        authHandle_handle,
                        nvIndex_handle,
                        ESYS_TR_PASSWORD,
                        ESYS_TR_PASSWORD,
                        ESYS_TR_NONE,
                        &qualifyingData,
                        &inScheme, size, offset, &certifyInfo, &signature);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_Vendor_TCG_Test(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    TPM2B_DATA inputData = DUMMY_2B_DATA(.buffer);
    TPM2B_DATA *outputData;
    r = Esys_Vendor_TCG_Test(esys_context,
                             ESYS_TR_NONE,
                             ESYS_TR_NONE,
                             ESYS_TR_NONE, &inputData, &outputData);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_AC_GetCapability(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    TPM_AT capability = 0;
    ESYS_TR ac = 0;
    UINT32 count = 0;
    TPML_AC_CAPABILITIES *capabilityData;
    TPMI_YES_NO moreData;
    r = Esys_AC_GetCapability(esys_context, ESYS_TR_NONE, ESYS_TR_NONE,
                              ESYS_TR_NONE, ac, capability, count, &moreData,
                              &capabilityData);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_AC_Send(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    ESYS_TR ac = 0;
    TPMS_AC_OUTPUT *acDataOut;
    TPM2B_MAX_BUFFER inputData = DUMMY_2B_DATA(.buffer);
    r = Esys_AC_Send(esys_context, 0, 0, ESYS_TR_NONE, ESYS_TR_NONE,
                     ESYS_TR_NONE, ac, &inputData, &acDataOut);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

static void
test_Policy_AC_SendSelect(void **state)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(esys_context, &tcti);

    TPMI_YES_NO includeObject = 0;
    TPM2B_NAME objectName = DUMMY_2B_DATA(.name);
    TPM2B_NAME authHandleName = DUMMY_2B_DATA(.name);
    TPM2B_NAME acName = DUMMY_2B_DATA(.name);
    r = Esys_Policy_AC_SendSelect(esys_context, ESYS_TR_NONE, ESYS_TR_NONE,
                                  ESYS_TR_NONE, &objectName, &authHandleName,
                                  &acName, includeObject);

    assert_int_equal(r, TSS2_TCTI_RC_NO_CONNECTION);
}

int
main(int argc, char *argv[])
{
    const struct CMUnitTest tests[] = {
        cmocka_unit_test_setup_teardown(test_Startup, setup, teardown),
        cmocka_unit_test_setup_teardown(test_Shutdown, setup, teardown),
        cmocka_unit_test_setup_teardown(test_SelfTest, setup, teardown),
        cmocka_unit_test_setup_teardown(test_IncrementalSelfTest, setup,
                                        teardown),
        cmocka_unit_test_setup_teardown(test_GetTestResult, setup, teardown),
        cmocka_unit_test_setup_teardown(test_StartAuthSession, setup, teardown),
        cmocka_unit_test_setup_teardown(test_PolicyRestart, setup, teardown),
        cmocka_unit_test_setup_teardown(test_Create, setup, teardown),
        cmocka_unit_test_setup_teardown(test_Load, setup, teardown),
        cmocka_unit_test_setup_teardown(test_LoadExternal, setup, teardown),
        cmocka_unit_test_setup_teardown(test_ReadPublic, setup, teardown),
        cmocka_unit_test_setup_teardown(test_ActivateCredential, setup,
                                        teardown),
        cmocka_unit_test_setup_teardown(test_MakeCredential, setup, teardown),
        cmocka_unit_test_setup_teardown(test_Unseal, setup, teardown),
        cmocka_unit_test_setup_teardown(test_ObjectChangeAuth, setup, teardown),
        cmocka_unit_test_setup_teardown(test_Duplicate, setup, teardown),
        cmocka_unit_test_setup_teardown(test_Rewrap, setup, teardown),
        cmocka_unit_test_setup_teardown(test_Import, setup, teardown),
        cmocka_unit_test_setup_teardown(test_RSA_Encrypt, setup, teardown),
        cmocka_unit_test_setup_teardown(test_RSA_Decrypt, setup, teardown),
        cmocka_unit_test_setup_teardown(test_ECDH_KeyGen, setup, teardown),
        cmocka_unit_test_setup_teardown(test_ECDH_ZGen, setup, teardown),
        cmocka_unit_test_setup_teardown(test_ECC_Parameters, setup, teardown),
        cmocka_unit_test_setup_teardown(test_ZGen_2Phase, setup, teardown),
        cmocka_unit_test_setup_teardown(test_EncryptDecrypt, setup, teardown),
        cmocka_unit_test_setup_teardown(test_EncryptDecrypt2, setup, teardown),
        cmocka_unit_test_setup_teardown(test_Hash, setup, teardown),
        cmocka_unit_test_setup_teardown(test_HMAC, setup, teardown),
        cmocka_unit_test_setup_teardown(test_MAC, setup, teardown),
        cmocka_unit_test_setup_teardown(test_GetRandom, setup, teardown),
        cmocka_unit_test_setup_teardown(test_StirRandom, setup, teardown),
        cmocka_unit_test_setup_teardown(test_HMAC_Start, setup, teardown),
        cmocka_unit_test_setup_teardown(test_MAC_Start, setup, teardown),
        cmocka_unit_test_setup_teardown(test_HashSequenceStart, setup,
                                        teardown),
        cmocka_unit_test_setup_teardown(test_SequenceUpdate, setup, teardown),
        cmocka_unit_test_setup_teardown(test_SequenceComplete, setup, teardown),
        cmocka_unit_test_setup_teardown(test_EventSequenceComplete, setup,
                                        teardown),
        cmocka_unit_test_setup_teardown(test_Certify, setup, teardown),
        cmocka_unit_test_setup_teardown(test_CertifyCreation, setup, teardown),
        cmocka_unit_test_setup_teardown(test_Quote, setup, teardown),
        cmocka_unit_test_setup_teardown(test_GetSessionAuditDigest, setup,
                                        teardown),
        cmocka_unit_test_setup_teardown(test_GetCommandAuditDigest, setup,
                                        teardown),
        cmocka_unit_test_setup_teardown(test_GetTime, setup, teardown),
        cmocka_unit_test_setup_teardown(test_Commit, setup, teardown),
        cmocka_unit_test_setup_teardown(test_EC_Ephemeral, setup, teardown),
        cmocka_unit_test_setup_teardown(test_VerifySignature, setup, teardown),
        cmocka_unit_test_setup_teardown(test_Sign, setup, teardown),
        cmocka_unit_test_setup_teardown(test_SetCommandCodeAuditStatus, setup,
                                        teardown),
        cmocka_unit_test_setup_teardown(test_PCR_Extend, setup, teardown),
        cmocka_unit_test_setup_teardown(test_PCR_Event, setup, teardown),
        cmocka_unit_test_setup_teardown(test_PCR_Read, setup, teardown),
        cmocka_unit_test_setup_teardown(test_PCR_Allocate, setup, teardown),
        cmocka_unit_test_setup_teardown(test_PCR_SetAuthPolicy, setup,
                                        teardown),
        cmocka_unit_test_setup_teardown(test_PCR_SetAuthValue, setup, teardown),
        cmocka_unit_test_setup_teardown(test_PCR_Reset, setup, teardown),
        cmocka_unit_test_setup_teardown(test_PolicySigned, setup, teardown),
        cmocka_unit_test_setup_teardown(test_PolicySecret, setup, teardown),
        cmocka_unit_test_setup_teardown(test_PolicyTicket, setup, teardown),
        cmocka_unit_test_setup_teardown(test_PolicyOR, setup, teardown),
        cmocka_unit_test_setup_teardown(test_PolicyPCR, setup, teardown),
        cmocka_unit_test_setup_teardown(test_PolicyLocality, setup, teardown),
        cmocka_unit_test_setup_teardown(test_PolicyNV, setup, teardown),
        cmocka_unit_test_setup_teardown(test_PolicyCounterTimer, setup,
                                        teardown),
        cmocka_unit_test_setup_teardown(test_PolicyCommandCode, setup,
                                        teardown),
        cmocka_unit_test_setup_teardown(test_PolicyPhysicalPresence, setup,
                                        teardown),
        cmocka_unit_test_setup_teardown(test_PolicyCpHash, setup, teardown),
        cmocka_unit_test_setup_teardown(test_PolicyNameHash, setup, teardown),
        cmocka_unit_test_setup_teardown(test_PolicyDuplicationSelect, setup,
                                        teardown),
        cmocka_unit_test_setup_teardown(test_PolicyAuthorize, setup, teardown),
        cmocka_unit_test_setup_teardown(test_PolicyAuthValue, setup, teardown),
        cmocka_unit_test_setup_teardown(test_PolicyPassword, setup, teardown),
        cmocka_unit_test_setup_teardown(test_PolicyGetDigest, setup, teardown),
        cmocka_unit_test_setup_teardown(test_PolicyNvWritten, setup, teardown),
        cmocka_unit_test_setup_teardown(test_PolicyTemplate, setup, teardown),
        cmocka_unit_test_setup_teardown(test_PolicyAuthorizeNV, setup,
                                        teardown),
        cmocka_unit_test_setup_teardown(test_CreatePrimary, setup, teardown),
        cmocka_unit_test_setup_teardown(test_HierarchyControl, setup, teardown),
        cmocka_unit_test_setup_teardown(test_SetPrimaryPolicy, setup, teardown),
        cmocka_unit_test_setup_teardown(test_ChangePPS, setup, teardown),
        cmocka_unit_test_setup_teardown(test_ChangeEPS, setup, teardown),
        cmocka_unit_test_setup_teardown(test_Clear, setup, teardown),
        cmocka_unit_test_setup_teardown(test_ClearControl, setup, teardown),
        cmocka_unit_test_setup_teardown(test_HierarchyChangeAuth, setup,
                                        teardown),
        cmocka_unit_test_setup_teardown(test_DictionaryAttackLockReset, setup,
                                        teardown),
        cmocka_unit_test_setup_teardown(test_DictionaryAttackParameters, setup,
                                        teardown),
        cmocka_unit_test_setup_teardown(test_PP_Commands, setup, teardown),
        cmocka_unit_test_setup_teardown(test_SetAlgorithmSet, setup, teardown),
        cmocka_unit_test_setup_teardown(test_FieldUpgradeStart, setup,
                                        teardown),
        cmocka_unit_test_setup_teardown(test_FieldUpgradeData, setup, teardown),
        cmocka_unit_test_setup_teardown(test_FirmwareRead, setup, teardown),
        cmocka_unit_test_setup_teardown(test_ContextSave, setup, teardown),
        cmocka_unit_test_setup_teardown(test_ContextLoad, setup, teardown),
        cmocka_unit_test_setup_teardown(test_FlushContext, setup, teardown),
        cmocka_unit_test_setup_teardown(test_EvictControl, setup, teardown),
        cmocka_unit_test_setup_teardown(test_ReadClock, setup, teardown),
        cmocka_unit_test_setup_teardown(test_ClockSet, setup, teardown),
        cmocka_unit_test_setup_teardown(test_ClockRateAdjust, setup, teardown),
        cmocka_unit_test_setup_teardown(test_GetCapability, setup, teardown),
        cmocka_unit_test_setup_teardown(test_TestParms, setup, teardown),
        cmocka_unit_test_setup_teardown(test_NV_DefineSpace, setup, teardown),
        cmocka_unit_test_setup_teardown(test_NV_UndefineSpace, setup, teardown),
        cmocka_unit_test_setup_teardown(test_NV_UndefineSpaceSpecial, setup,
                                        teardown),
        cmocka_unit_test_setup_teardown(test_NV_ReadPublic, setup, teardown),
        cmocka_unit_test_setup_teardown(test_NV_Write, setup, teardown),
        cmocka_unit_test_setup_teardown(test_NV_Increment, setup, teardown),
        cmocka_unit_test_setup_teardown(test_NV_Extend, setup, teardown),
        cmocka_unit_test_setup_teardown(test_NV_SetBits, setup, teardown),
        cmocka_unit_test_setup_teardown(test_NV_WriteLock, setup, teardown),
        cmocka_unit_test_setup_teardown(test_NV_GlobalWriteLock, setup,
                                        teardown),
        cmocka_unit_test_setup_teardown(test_NV_Read, setup, teardown),
        cmocka_unit_test_setup_teardown(test_NV_ReadLock, setup, teardown),
        cmocka_unit_test_setup_teardown(test_NV_ChangeAuth, setup, teardown),
        cmocka_unit_test_setup_teardown(test_NV_Certify, setup, teardown),
        cmocka_unit_test_setup_teardown(test_Vendor_TCG_Test, setup, teardown),
        cmocka_unit_test_setup_teardown(test_AC_GetCapability, setup, teardown),
        cmocka_unit_test_setup_teardown(test_AC_Send, setup, teardown),
        cmocka_unit_test_setup_teardown(test_Policy_AC_SendSelect, setup, teardown)
    };
    return cmocka_run_group_tests(tests, NULL, NULL);
}
