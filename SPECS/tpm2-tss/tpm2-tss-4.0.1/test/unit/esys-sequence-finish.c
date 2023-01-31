/* SPDX-License-Identifier: BSD-2-Clause */
/*******************************************************************************
 * Copyright 2017-2018, Fraunhofer SIT sponsored by Infineon Technologies AG
 * All rights reserved.
 *******************************************************************************/

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <stdarg.h>
#include <stdlib.h>
#include <inttypes.h>
#include <string.h>

#include <setjmp.h>
#include <cmocka.h>

#include "tss2_esys.h"

#include "tss2-esys/esys_iutil.h"
#define LOGMODULE tests
#include "util/log.h"
#include "util/aux_util.h"

/*
 * Tests whether all ESAPI finish calls handle wrong internal states with the correct
 * error response TSS2_ESYS_RC_BAD_SEQUENCE.
 */

static TSS2_RC
tcti_failure_transmit(TSS2_TCTI_CONTEXT * tctiContext,
                      size_t size, const uint8_t * buffer)
{
    UNUSED(tctiContext);
    UNUSED(size);
    UNUSED(buffer);

    return TSS2_RC_SUCCESS;
}

const uint8_t failure_response[] = {
    0x80, 0x01,                 /* TPM_ST_NO_SESSION */
    0x00, 0x00, 0x00, 0x0A,     /* Response Size 10 */
    0x00, 0x00, 0x01, 0x01      /* TPM_RC_FAILURE */
};

static TSS2_RC
tcti_failure_receive(TSS2_TCTI_CONTEXT * tctiContext,
                     size_t * response_size,
                     uint8_t * response_buffer, int32_t timeout)
{
    *response_size = sizeof(failure_response);
    if (response_buffer != NULL)
        memcpy(response_buffer, &failure_response[0], sizeof(failure_response));

    return TSS2_RC_SUCCESS;
}

/**
 * Prepare ESAPI context with a reference to SAPI and TCTI context.
 */
static int
esys_unit_setup(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context;

    /* This is a fake tcti context */
    TSS2_TCTI_CONTEXT_COMMON_V1 *tcti =
        calloc(1, sizeof(TSS2_TCTI_CONTEXT_COMMON_V1));
    tcti->version = 1;
    TSS2_TCTI_TRANSMIT (tcti) = tcti_failure_transmit;
    TSS2_TCTI_RECEIVE (tcti) = tcti_failure_receive;

    r = Esys_Initialize(&esys_context, (TSS2_TCTI_CONTEXT *) tcti, NULL);
    assert_int_equal(r, TSS2_RC_SUCCESS);
    *state = (void *)esys_context;
    return 0;
}

/**
 * Free  ESAPI, SAPI and TCTI context.
 */
static int
esys_unit_teardown(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    TSS2_TCTI_CONTEXT *tcti;
    r = Esys_GetTcti(esys_context, &tcti);
    assert_int_equal(r, TSS2_RC_SUCCESS);
    Esys_Finalize(&esys_context);
    free(tcti);
    return 0;
}

void
check_Startup(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_Startup_Finish(esys_context);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_Shutdown(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_Shutdown_Finish(esys_context);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_SelfTest(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_SelfTest_Finish(esys_context);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_IncrementalSelfTest(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    TPML_ALG *toDoList;
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_IncrementalSelfTest_Finish(esys_context, &toDoList);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_GetTestResult(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    TPM2B_MAX_BUFFER *outData;
    TPM2_RC testResult;
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_GetTestResult_Finish(esys_context, &outData, &testResult);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_StartAuthSession(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    ESYS_TR sessionHandle_handle;
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_StartAuthSession_Finish(esys_context,
                                         &sessionHandle_handle);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_PolicyRestart(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_PolicyRestart_Finish(esys_context);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_Create(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    TPM2B_PRIVATE *outPrivate;
    TPM2B_PUBLIC *outPublic;
    TPM2B_CREATION_DATA *creationData;
    TPM2B_DIGEST *creationHash;
    TPMT_TK_CREATION *creationTicket;
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_Create_Finish(esys_context,
                               &outPrivate,
                               &outPublic,
                               &creationData, &creationHash, &creationTicket);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_Load(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    ESYS_TR objectHandle_handle;
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_Load_Finish(esys_context, &objectHandle_handle);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_LoadExternal(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    ESYS_TR objectHandle_handle;
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_LoadExternal_Finish(esys_context, &objectHandle_handle);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_ReadPublic(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    TPM2B_PUBLIC *outPublic;
    TPM2B_NAME *name;
    TPM2B_NAME *qualifiedName;
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_ReadPublic_Finish(esys_context,
                                   &outPublic, &name, &qualifiedName);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_ActivateCredential(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    TPM2B_DIGEST *certInfo;
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_ActivateCredential_Finish(esys_context, &certInfo);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_MakeCredential(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    TPM2B_ID_OBJECT *credentialBlob;
    TPM2B_ENCRYPTED_SECRET *secret;
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_MakeCredential_Finish(esys_context, &credentialBlob, &secret);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_Unseal(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    TPM2B_SENSITIVE_DATA *outData;
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_Unseal_Finish(esys_context, &outData);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_ObjectChangeAuth(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    TPM2B_PRIVATE *outPrivate;
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_ObjectChangeAuth_Finish(esys_context, &outPrivate);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_CreateLoaded(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    ESYS_TR objectHandle_handle;
    TPM2B_PRIVATE *outPrivate;
    TPM2B_PUBLIC *outPublic;
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_CreateLoaded_Finish(esys_context,
                                     &objectHandle_handle,
                                     &outPrivate, &outPublic);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_Duplicate(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    TPM2B_DATA *encryptionKeyOut;
    TPM2B_PRIVATE *duplicate;
    TPM2B_ENCRYPTED_SECRET *outSymSeed;
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_Duplicate_Finish(esys_context,
                                  &encryptionKeyOut, &duplicate, &outSymSeed);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_Rewrap(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    TPM2B_PRIVATE *outDuplicate;
    TPM2B_ENCRYPTED_SECRET *outSymSeed;
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_Rewrap_Finish(esys_context, &outDuplicate, &outSymSeed);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_Import(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    TPM2B_PRIVATE *outPrivate;
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_Import_Finish(esys_context, &outPrivate);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_RSA_Encrypt(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    TPM2B_PUBLIC_KEY_RSA *outData;
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_RSA_Encrypt_Finish(esys_context, &outData);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_RSA_Decrypt(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    TPM2B_PUBLIC_KEY_RSA *message;
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_RSA_Decrypt_Finish(esys_context, &message);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_ECDH_KeyGen(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    TPM2B_ECC_POINT *zPoint;
    TPM2B_ECC_POINT *pubPoint;
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_ECDH_KeyGen_Finish(esys_context, &zPoint, &pubPoint);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_ECDH_ZGen(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    TPM2B_ECC_POINT *outPoint;
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_ECDH_ZGen_Finish(esys_context, &outPoint);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_ECC_Parameters(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    TPMS_ALGORITHM_DETAIL_ECC *parameters;
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_ECC_Parameters_Finish(esys_context, &parameters);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_ZGen_2Phase(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    TPM2B_ECC_POINT *outZ1;
    TPM2B_ECC_POINT *outZ2;
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_ZGen_2Phase_Finish(esys_context, &outZ1, &outZ2);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_EncryptDecrypt(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    TPM2B_MAX_BUFFER *outData;
    TPM2B_IV *ivOut;
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_EncryptDecrypt_Finish(esys_context, &outData, &ivOut);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_EncryptDecrypt2(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    TPM2B_MAX_BUFFER *outData;
    TPM2B_IV *ivOut;
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_EncryptDecrypt2_Finish(esys_context, &outData, &ivOut);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_Hash(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    TPM2B_DIGEST *outHash;
    TPMT_TK_HASHCHECK *validation;
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_Hash_Finish(esys_context, &outHash, &validation);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_HMAC(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    TPM2B_DIGEST *outHMAC;
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_HMAC_Finish(esys_context, &outHMAC);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_MAC(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    TPM2B_DIGEST *outMAC;
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_MAC_Finish(esys_context, &outMAC);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_GetRandom(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    TPM2B_DIGEST *randomBytes;
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_GetRandom_Finish(esys_context, &randomBytes);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_StirRandom(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_StirRandom_Finish(esys_context);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_HMAC_Start(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    ESYS_TR sequenceHandle_handle;
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_HMAC_Start_Finish(esys_context, &sequenceHandle_handle);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_MAC_Start(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    ESYS_TR sequenceHandle_handle;
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_MAC_Start_Finish(esys_context, &sequenceHandle_handle);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_HashSequenceStart(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    ESYS_TR sequenceHandle_handle;
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_HashSequenceStart_Finish(esys_context, &sequenceHandle_handle);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_SequenceUpdate(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_SequenceUpdate_Finish(esys_context);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_SequenceComplete(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    TPM2B_DIGEST *result;
    TPMT_TK_HASHCHECK *validation;
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_SequenceComplete_Finish(esys_context, &result, &validation);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_EventSequenceComplete(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    TPML_DIGEST_VALUES *results;
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_EventSequenceComplete_Finish(esys_context, &results);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_Certify(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    TPM2B_ATTEST *certifyInfo;
    TPMT_SIGNATURE *signature;
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_Certify_Finish(esys_context, &certifyInfo, &signature);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_CertifyCreation(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    TPM2B_ATTEST *certifyInfo;
    TPMT_SIGNATURE *signature;
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_CertifyCreation_Finish(esys_context, &certifyInfo, &signature);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_Quote(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    TPM2B_ATTEST *quoted;
    TPMT_SIGNATURE *signature;
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_Quote_Finish(esys_context, &quoted, &signature);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_GetSessionAuditDigest(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    TPM2B_ATTEST *auditInfo;
    TPMT_SIGNATURE *signature;
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_GetSessionAuditDigest_Finish(esys_context,
                                              &auditInfo, &signature);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_GetCommandAuditDigest(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    TPM2B_ATTEST *auditInfo;
    TPMT_SIGNATURE *signature;
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_GetCommandAuditDigest_Finish(esys_context,
                                              &auditInfo, &signature);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_GetTime(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    TPM2B_ATTEST *timeInfo;
    TPMT_SIGNATURE *signature;
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_GetTime_Finish(esys_context, &timeInfo, &signature);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_Commit(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    TPM2B_ECC_POINT *K;
    TPM2B_ECC_POINT *L;
    TPM2B_ECC_POINT *E;
    UINT16 counter;
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_Commit_Finish(esys_context, &K, &L, &E, &counter);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_EC_Ephemeral(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    TPM2B_ECC_POINT *Q;
    UINT16 counter;
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_EC_Ephemeral_Finish(esys_context, &Q, &counter);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_VerifySignature(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    TPMT_TK_VERIFIED *validation;
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_VerifySignature_Finish(esys_context, &validation);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_Sign(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    TPMT_SIGNATURE *signature;
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_Sign_Finish(esys_context, &signature);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_SetCommandCodeAuditStatus(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_SetCommandCodeAuditStatus_Finish(esys_context);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_PCR_Extend(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_PCR_Extend_Finish(esys_context);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_PCR_Event(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    TPML_DIGEST_VALUES *digests;
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_PCR_Event_Finish(esys_context, &digests);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_PCR_Read(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    TPML_PCR_SELECTION *pcrSelectionOut;
    TPML_DIGEST *pcrValues;
    UINT32 pcrUpdateCounter;
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_PCR_Read_Finish(esys_context,
                                 &pcrUpdateCounter,
                                 &pcrSelectionOut, &pcrValues);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_PCR_Allocate(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    TPMI_YES_NO allocationSuccess;
    UINT32 maxPCR;
    UINT32 sizeNeeded;
    UINT32 sizeAvailable;
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_PCR_Allocate_Finish(esys_context,
                                     &allocationSuccess,
                                     &maxPCR, &sizeNeeded, &sizeAvailable);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_PCR_SetAuthPolicy(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_PCR_SetAuthPolicy_Finish(esys_context);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_PCR_SetAuthValue(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_PCR_SetAuthValue_Finish(esys_context);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_PCR_Reset(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_PCR_Reset_Finish(esys_context);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_PolicySigned(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    TPM2B_TIMEOUT *timeout;
    TPMT_TK_AUTH *policyTicket;
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_PolicySigned_Finish(esys_context, &timeout, &policyTicket);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_PolicySecret(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    TPM2B_TIMEOUT *timeout;
    TPMT_TK_AUTH *policyTicket;
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_PolicySecret_Finish(esys_context, &timeout, &policyTicket);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_PolicyTicket(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_PolicyTicket_Finish(esys_context);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_PolicyOR(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_PolicyOR_Finish(esys_context);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_PolicyPCR(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_PolicyPCR_Finish(esys_context);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_PolicyLocality(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_PolicyLocality_Finish(esys_context);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_PolicyNV(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_PolicyNV_Finish(esys_context);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_PolicyCounterTimer(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_PolicyCounterTimer_Finish(esys_context);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_PolicyCommandCode(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_PolicyCommandCode_Finish(esys_context);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_PolicyPhysicalPresence(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_PolicyPhysicalPresence_Finish(esys_context);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_PolicyCpHash(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_PolicyCpHash_Finish(esys_context);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_PolicyNameHash(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_PolicyNameHash_Finish(esys_context);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_PolicyDuplicationSelect(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_PolicyDuplicationSelect_Finish(esys_context);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_PolicyAuthorize(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_PolicyAuthorize_Finish(esys_context);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_PolicyAuthValue(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_PolicyAuthValue_Finish(esys_context);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_PolicyPassword(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_PolicyPassword_Finish(esys_context);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_PolicyGetDigest(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    TPM2B_DIGEST *policyDigest;
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_PolicyGetDigest_Finish(esys_context, &policyDigest);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_PolicyNvWritten(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_PolicyNvWritten_Finish(esys_context);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_PolicyTemplate(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_PolicyTemplate_Finish(esys_context);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_PolicyAuthorizeNV(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_PolicyAuthorizeNV_Finish(esys_context);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_CreatePrimary(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    ESYS_TR objectHandle_handle;
    TPM2B_PUBLIC *outPublic;
    TPM2B_CREATION_DATA *creationData;
    TPM2B_DIGEST *creationHash;
    TPMT_TK_CREATION *creationTicket;
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_CreatePrimary_Finish(esys_context,
                                      &objectHandle_handle,
                                      &outPublic,
                                      &creationData,
                                      &creationHash, &creationTicket);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_HierarchyControl(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_HierarchyControl_Finish(esys_context);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_SetPrimaryPolicy(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_SetPrimaryPolicy_Finish(esys_context);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_ChangePPS(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_ChangePPS_Finish(esys_context);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_ChangeEPS(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_ChangeEPS_Finish(esys_context);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_Clear(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_Clear_Finish(esys_context);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_ClearControl(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_ClearControl_Finish(esys_context);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_HierarchyChangeAuth(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_HierarchyChangeAuth_Finish(esys_context);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_DictionaryAttackLockReset(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_DictionaryAttackLockReset_Finish(esys_context);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_DictionaryAttackParameters(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_DictionaryAttackParameters_Finish(esys_context);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_PP_Commands(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_PP_Commands_Finish(esys_context);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_SetAlgorithmSet(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_SetAlgorithmSet_Finish(esys_context);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_FieldUpgradeStart(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_FieldUpgradeStart_Finish(esys_context);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_FieldUpgradeData(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    TPMT_HA *nextDigest;
    TPMT_HA *firstDigest;
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_FieldUpgradeData_Finish(esys_context,
                                         &nextDigest, &firstDigest);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_FirmwareRead(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    TPM2B_MAX_BUFFER *fuData;
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_FirmwareRead_Finish(esys_context, &fuData);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_ContextSave(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    TPMS_CONTEXT *context;
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_ContextSave_Finish(esys_context, &context);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_ContextLoad(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    ESYS_TR loadedHandle_handle;
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_ContextLoad_Finish(esys_context, &loadedHandle_handle);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_FlushContext(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_FlushContext_Finish(esys_context);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_EvictControl(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    ESYS_TR newObjectHandle_handle;
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_EvictControl_Finish(esys_context, &newObjectHandle_handle);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_ReadClock(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    TPMS_TIME_INFO *currentTime;
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_ReadClock_Finish(esys_context, &currentTime);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_ClockSet(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_ClockSet_Finish(esys_context);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_ClockRateAdjust(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_ClockRateAdjust_Finish(esys_context);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_GetCapability(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    TPMS_CAPABILITY_DATA *capabilityData;
    TPMI_YES_NO moreData;
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_GetCapability_Finish(esys_context, &moreData, &capabilityData);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_TestParms(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_TestParms_Finish(esys_context);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_NV_DefineSpace(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    ESYS_TR nvHandle_handle;
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_NV_DefineSpace_Finish(esys_context, &nvHandle_handle);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_NV_UndefineSpace(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_NV_UndefineSpace_Finish(esys_context);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_NV_UndefineSpaceSpecial(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_NV_UndefineSpaceSpecial_Finish(esys_context);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_NV_ReadPublic(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    TPM2B_NV_PUBLIC *nvPublic;
    TPM2B_NAME *nvName;
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_NV_ReadPublic_Finish(esys_context, &nvPublic, &nvName);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_NV_Write(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_NV_Write_Finish(esys_context);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_NV_Increment(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_NV_Increment_Finish(esys_context);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_NV_Extend(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_NV_Extend_Finish(esys_context);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_NV_SetBits(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_NV_SetBits_Finish(esys_context);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_NV_WriteLock(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_NV_WriteLock_Finish(esys_context);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_NV_GlobalWriteLock(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_NV_GlobalWriteLock_Finish(esys_context);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_NV_Read(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    TPM2B_MAX_NV_BUFFER *data;
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_NV_Read_Finish(esys_context, &data);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_NV_ReadLock(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_NV_ReadLock_Finish(esys_context);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_NV_ChangeAuth(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_NV_ChangeAuth_Finish(esys_context);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_NV_Certify(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    TPM2B_ATTEST *certifyInfo;
    TPMT_SIGNATURE *signature;
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_NV_Certify_Finish(esys_context, &certifyInfo, &signature);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_Vendor_TCG_Test(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    TPM2B_DATA *outputData;
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_Vendor_TCG_Test_Finish(esys_context, &outputData);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_AC_GetCapability(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    TPML_AC_CAPABILITIES *capabilityData;
    TPMI_YES_NO moreData;
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_AC_GetCapability_Finish(esys_context, &moreData, &capabilityData);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_AC_Send(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    TPMS_AC_OUTPUT *acDataOut;
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_AC_Send_Finish(esys_context, &acDataOut);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

void
check_Policy_AC_SendSelect(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *esys_context = (ESYS_CONTEXT *) * state;
    enum _ESYS_STATE esys_states[3] = {
        _ESYS_STATE_INIT,
        _ESYS_STATE_INTERNALERROR
    };
    for (size_t i = 0; i < sizeof(esys_states) / sizeof(esys_states[0]); i++) {
        esys_context->state = esys_states[i];
        r = Esys_Policy_AC_SendSelect_Finish(esys_context);
        assert_int_equal(r, TSS2_ESYS_RC_BAD_SEQUENCE);
    }
}

int
main(void)
{
    const struct CMUnitTest tests[] = {
        cmocka_unit_test_setup_teardown(check_Startup, esys_unit_setup,
                                        esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_Shutdown, esys_unit_setup,
                                        esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_SelfTest, esys_unit_setup,
                                        esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_IncrementalSelfTest,
                                        esys_unit_setup, esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_GetTestResult, esys_unit_setup,
                                        esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_StartAuthSession, esys_unit_setup,
                                        esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_PolicyRestart, esys_unit_setup,
                                        esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_Create, esys_unit_setup,
                                        esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_Load, esys_unit_setup,
                                        esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_LoadExternal, esys_unit_setup,
                                        esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_ReadPublic, esys_unit_setup,
                                        esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_ActivateCredential,
                                        esys_unit_setup, esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_MakeCredential, esys_unit_setup,
                                        esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_Unseal, esys_unit_setup,
                                        esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_ObjectChangeAuth, esys_unit_setup,
                                        esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_CreateLoaded, esys_unit_setup,
                                        esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_Duplicate, esys_unit_setup,
                                        esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_Rewrap, esys_unit_setup,
                                        esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_Import, esys_unit_setup,
                                        esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_RSA_Encrypt, esys_unit_setup,
                                        esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_RSA_Decrypt, esys_unit_setup,
                                        esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_ECDH_KeyGen, esys_unit_setup,
                                        esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_ECDH_ZGen, esys_unit_setup,
                                        esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_ECC_Parameters, esys_unit_setup,
                                        esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_ZGen_2Phase, esys_unit_setup,
                                        esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_EncryptDecrypt, esys_unit_setup,
                                        esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_EncryptDecrypt2, esys_unit_setup,
                                        esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_Hash, esys_unit_setup,
                                        esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_HMAC, esys_unit_setup,
                                        esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_GetRandom, esys_unit_setup,
                                        esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_StirRandom, esys_unit_setup,
                                        esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_HMAC_Start, esys_unit_setup,
                                        esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_HashSequenceStart,
                                        esys_unit_setup, esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_SequenceUpdate, esys_unit_setup,
                                        esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_SequenceComplete, esys_unit_setup,
                                        esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_EventSequenceComplete,
                                        esys_unit_setup, esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_Certify, esys_unit_setup,
                                        esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_CertifyCreation, esys_unit_setup,
                                        esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_Quote, esys_unit_setup,
                                        esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_GetSessionAuditDigest,
                                        esys_unit_setup, esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_GetCommandAuditDigest,
                                        esys_unit_setup, esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_GetTime, esys_unit_setup,
                                        esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_Commit, esys_unit_setup,
                                        esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_EC_Ephemeral, esys_unit_setup,
                                        esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_VerifySignature, esys_unit_setup,
                                        esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_Sign, esys_unit_setup,
                                        esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_SetCommandCodeAuditStatus,
                                        esys_unit_setup, esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_PCR_Extend, esys_unit_setup,
                                        esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_PCR_Event, esys_unit_setup,
                                        esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_PCR_Read, esys_unit_setup,
                                        esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_PCR_Allocate, esys_unit_setup,
                                        esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_PCR_SetAuthPolicy,
                                        esys_unit_setup, esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_PCR_SetAuthValue, esys_unit_setup,
                                        esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_PCR_Reset, esys_unit_setup,
                                        esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_PolicySigned, esys_unit_setup,
                                        esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_PolicySecret, esys_unit_setup,
                                        esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_PolicyTicket, esys_unit_setup,
                                        esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_PolicyOR, esys_unit_setup,
                                        esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_PolicyPCR, esys_unit_setup,
                                        esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_PolicyLocality, esys_unit_setup,
                                        esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_PolicyNV, esys_unit_setup,
                                        esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_PolicyCounterTimer,
                                        esys_unit_setup, esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_PolicyCommandCode,
                                        esys_unit_setup, esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_PolicyPhysicalPresence,
                                        esys_unit_setup, esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_PolicyCpHash, esys_unit_setup,
                                        esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_PolicyNameHash, esys_unit_setup,
                                        esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_PolicyDuplicationSelect,
                                        esys_unit_setup, esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_PolicyAuthorize, esys_unit_setup,
                                        esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_PolicyAuthValue, esys_unit_setup,
                                        esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_PolicyPassword, esys_unit_setup,
                                        esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_PolicyGetDigest, esys_unit_setup,
                                        esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_PolicyNvWritten, esys_unit_setup,
                                        esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_PolicyTemplate, esys_unit_setup,
                                        esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_PolicyAuthorizeNV,
                                        esys_unit_setup, esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_CreatePrimary, esys_unit_setup,
                                        esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_HierarchyControl, esys_unit_setup,
                                        esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_SetPrimaryPolicy, esys_unit_setup,
                                        esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_ChangePPS, esys_unit_setup,
                                        esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_ChangeEPS, esys_unit_setup,
                                        esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_Clear, esys_unit_setup,
                                        esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_ClearControl, esys_unit_setup,
                                        esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_HierarchyChangeAuth,
                                        esys_unit_setup, esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_DictionaryAttackLockReset,
                                        esys_unit_setup, esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_DictionaryAttackParameters,
                                        esys_unit_setup, esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_PP_Commands, esys_unit_setup,
                                        esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_SetAlgorithmSet, esys_unit_setup,
                                        esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_FieldUpgradeStart,
                                        esys_unit_setup, esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_FieldUpgradeData, esys_unit_setup,
                                        esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_FirmwareRead, esys_unit_setup,
                                        esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_ContextSave, esys_unit_setup,
                                        esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_ContextLoad, esys_unit_setup,
                                        esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_FlushContext, esys_unit_setup,
                                        esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_EvictControl, esys_unit_setup,
                                        esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_ReadClock, esys_unit_setup,
                                        esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_ClockSet, esys_unit_setup,
                                        esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_ClockRateAdjust, esys_unit_setup,
                                        esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_GetCapability, esys_unit_setup,
                                        esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_TestParms, esys_unit_setup,
                                        esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_NV_DefineSpace, esys_unit_setup,
                                        esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_NV_UndefineSpace, esys_unit_setup,
                                        esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_NV_UndefineSpaceSpecial,
                                        esys_unit_setup, esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_NV_ReadPublic, esys_unit_setup,
                                        esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_NV_Write, esys_unit_setup,
                                        esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_NV_Increment, esys_unit_setup,
                                        esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_NV_Extend, esys_unit_setup,
                                        esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_NV_SetBits, esys_unit_setup,
                                        esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_NV_WriteLock, esys_unit_setup,
                                        esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_NV_GlobalWriteLock,
                                        esys_unit_setup, esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_NV_Read, esys_unit_setup,
                                        esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_NV_ReadLock, esys_unit_setup,
                                        esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_NV_ChangeAuth, esys_unit_setup,
                                        esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_NV_Certify, esys_unit_setup,
                                        esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_Vendor_TCG_Test, esys_unit_setup,
                                        esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_AC_GetCapability, esys_unit_setup,
                                        esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_AC_Send, esys_unit_setup,
                                        esys_unit_teardown),
        cmocka_unit_test_setup_teardown(check_Policy_AC_SendSelect, esys_unit_setup,
                                        esys_unit_teardown)
    };
    return cmocka_run_group_tests(tests, NULL, NULL);
}
