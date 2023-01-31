/* SPDX-License-Identifier: BSD-2-Clause */
/*******************************************************************************
 * Copyright 2017-2018, Fraunhofer SIT sponsored by Infineon Technologies AG
 * All rights reserved.
 *******************************************************************************/

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <signal.h>
#include <stdint.h>
#define LOGMODULE test
#include "util/log.h"
#include "util/aux_util.h"
#include "tss2-sys/sysapi_util.h"
#include <tss2_esys.h>
#include "esys_types.h"
#include "esys_iutil.h"

#include <setjmp.h>
#include <cmocka.h>

/**
 * This unit test checks whether all  Esys_<cmd>() functions (one call, async,
 * and finish check the NULL pointer ESYS context.
 */

void
check_Startup(void **state)
{
    TSS2_RC r;

    r = Esys_Startup(NULL, 0);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_Startup_Async(NULL, 0);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_Startup_Finish(NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_Shutdown(void **state)
{
    TSS2_RC r;

    r = Esys_Shutdown(NULL, ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE, 0);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_Shutdown_Async(NULL, ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE, 0);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_Shutdown_Finish(NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_SelfTest(void **state)
{
    TSS2_RC r;

    r = Esys_SelfTest(NULL, ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE, 0);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_SelfTest_Async(NULL, ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE, 0);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_SelfTest_Finish(NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_IncrementalSelfTest(void **state)
{
    TSS2_RC r;

    r = Esys_IncrementalSelfTest(NULL,
                                 ESYS_TR_NONE,
                                 ESYS_TR_NONE, ESYS_TR_NONE, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_IncrementalSelfTest_Async(NULL,
                                       ESYS_TR_NONE,
                                       ESYS_TR_NONE, ESYS_TR_NONE, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_IncrementalSelfTest_Finish(NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_GetTestResult(void **state)
{
    TSS2_RC r;

    r = Esys_GetTestResult(NULL,
                           ESYS_TR_NONE,
                           ESYS_TR_NONE, ESYS_TR_NONE, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_GetTestResult_Async(NULL,
                                 ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_GetTestResult_Finish(NULL, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_StartAuthSession(void **state)
{
    TSS2_RC r;

    r = Esys_StartAuthSession(NULL,
                              0,
                              0,
                              ESYS_TR_NONE,
                              ESYS_TR_NONE,
                              ESYS_TR_NONE, NULL, 0, NULL, 0, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_StartAuthSession_Async(NULL,
                                    0,
                                    0,
                                    ESYS_TR_NONE,
                                    ESYS_TR_NONE,
                                    ESYS_TR_NONE, NULL, 0, NULL, 0);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_StartAuthSession_Finish(NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_PolicyRestart(void **state)
{
    TSS2_RC r;

    r = Esys_PolicyRestart(NULL, 0, ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_PolicyRestart_Async(NULL,
                                 0, ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_PolicyRestart_Finish(NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_Create(void **state)
{
    TSS2_RC r;

    r = Esys_Create(NULL,
                    0,
                    ESYS_TR_PASSWORD,
                    ESYS_TR_NONE,
                    ESYS_TR_NONE,
                    NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_Create_Async(NULL,
                          0,
                          ESYS_TR_PASSWORD,
                          ESYS_TR_NONE, ESYS_TR_NONE, NULL, NULL, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_Create_Finish(NULL, NULL, NULL, NULL, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_Load(void **state)
{
    TSS2_RC r;

    r = Esys_Load(NULL,
                  0,
                  ESYS_TR_PASSWORD,
                  ESYS_TR_NONE, ESYS_TR_NONE, NULL, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_Load_Async(NULL,
                        0,
                        ESYS_TR_PASSWORD,
                        ESYS_TR_NONE, ESYS_TR_NONE, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_Load_Finish(NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_LoadExternal(void **state)
{
    TSS2_RC r;

    r = Esys_LoadExternal(NULL,
                          ESYS_TR_NONE,
                          ESYS_TR_NONE, ESYS_TR_NONE, NULL, NULL, 0, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_LoadExternal_Async(NULL,
                                ESYS_TR_NONE,
                                ESYS_TR_NONE, ESYS_TR_NONE, NULL, NULL, 0);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_LoadExternal_Finish(NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_ReadPublic(void **state)
{
    TSS2_RC r;

    r = Esys_ReadPublic(NULL,
                        0,
                        ESYS_TR_NONE,
                        ESYS_TR_NONE, ESYS_TR_NONE, NULL, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_ReadPublic_Async(NULL,
                              0, ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_ReadPublic_Finish(NULL, NULL, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_ActivateCredential(void **state)
{
    TSS2_RC r;

    r = Esys_ActivateCredential(NULL,
                                0,
                                0,
                                ESYS_TR_PASSWORD,
                                ESYS_TR_PASSWORD,
                                ESYS_TR_NONE, NULL, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_ActivateCredential_Async(NULL,
                                      0,
                                      0,
                                      ESYS_TR_PASSWORD,
                                      ESYS_TR_PASSWORD,
                                      ESYS_TR_NONE, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_ActivateCredential_Finish(NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_MakeCredential(void **state)
{
    TSS2_RC r;

    r = Esys_MakeCredential(NULL,
                            0,
                            ESYS_TR_NONE,
                            ESYS_TR_NONE, ESYS_TR_NONE, NULL, NULL, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_MakeCredential_Async(NULL,
                                  0,
                                  ESYS_TR_NONE,
                                  ESYS_TR_NONE, ESYS_TR_NONE, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_MakeCredential_Finish(NULL, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_Unseal(void **state)
{
    TSS2_RC r;

    r = Esys_Unseal(NULL,
                    0, ESYS_TR_PASSWORD, ESYS_TR_NONE, ESYS_TR_NONE, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_Unseal_Async(NULL,
                          0, ESYS_TR_PASSWORD, ESYS_TR_NONE, ESYS_TR_NONE);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_Unseal_Finish(NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_ObjectChangeAuth(void **state)
{
    TSS2_RC r;

    r = Esys_ObjectChangeAuth(NULL,
                              0,
                              0,
                              ESYS_TR_PASSWORD,
                              ESYS_TR_NONE, ESYS_TR_NONE, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_ObjectChangeAuth_Async(NULL,
                                    0,
                                    0,
                                    ESYS_TR_PASSWORD,
                                    ESYS_TR_NONE, ESYS_TR_NONE, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_ObjectChangeAuth_Finish(NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_CreateLoaded(void **state)
{
    TSS2_RC r;

    r = Esys_CreateLoaded(NULL,
                          0,
                          ESYS_TR_PASSWORD,
                          ESYS_TR_NONE,
                          ESYS_TR_NONE, NULL, NULL, NULL, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_CreateLoaded_Async(NULL,
                                0,
                                ESYS_TR_PASSWORD,
                                ESYS_TR_NONE, ESYS_TR_NONE, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_CreateLoaded_Finish(NULL, NULL, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_Duplicate(void **state)
{
    TSS2_RC r;

    r = Esys_Duplicate(NULL,
                       0,
                       0,
                       ESYS_TR_PASSWORD,
                       ESYS_TR_NONE,
                       ESYS_TR_NONE, NULL, NULL, NULL, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_Duplicate_Async(NULL,
                             0,
                             0,
                             ESYS_TR_PASSWORD,
                             ESYS_TR_NONE, ESYS_TR_NONE, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_Duplicate_Finish(NULL, NULL, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_Rewrap(void **state)
{
    TSS2_RC r;

    r = Esys_Rewrap(NULL,
                    0,
                    0,
                    ESYS_TR_PASSWORD,
                    ESYS_TR_NONE, ESYS_TR_NONE, NULL, NULL, NULL, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_Rewrap_Async(NULL,
                          0,
                          0,
                          ESYS_TR_PASSWORD,
                          ESYS_TR_NONE, ESYS_TR_NONE, NULL, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_Rewrap_Finish(NULL, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_Import(void **state)
{
    TSS2_RC r;

    r = Esys_Import(NULL,
                    0,
                    ESYS_TR_PASSWORD,
                    ESYS_TR_NONE,
                    ESYS_TR_NONE, NULL, NULL, NULL, NULL, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_Import_Async(NULL,
                          0,
                          ESYS_TR_PASSWORD,
                          ESYS_TR_NONE,
                          ESYS_TR_NONE, NULL, NULL, NULL, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_Import_Finish(NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_RSA_Encrypt(void **state)
{
    TSS2_RC r;

    r = Esys_RSA_Encrypt(NULL,
                         0,
                         ESYS_TR_NONE,
                         ESYS_TR_NONE, ESYS_TR_NONE, NULL, NULL, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_RSA_Encrypt_Async(NULL,
                               0,
                               ESYS_TR_NONE,
                               ESYS_TR_NONE, ESYS_TR_NONE, NULL, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_RSA_Encrypt_Finish(NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_RSA_Decrypt(void **state)
{
    TSS2_RC r;

    r = Esys_RSA_Decrypt(NULL,
                         0,
                         ESYS_TR_PASSWORD,
                         ESYS_TR_NONE, ESYS_TR_NONE, NULL, NULL, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_RSA_Decrypt_Async(NULL,
                               0,
                               ESYS_TR_PASSWORD,
                               ESYS_TR_NONE, ESYS_TR_NONE, NULL, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_RSA_Decrypt_Finish(NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_ECDH_KeyGen(void **state)
{
    TSS2_RC r;

    r = Esys_ECDH_KeyGen(NULL,
                         0,
                         ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_ECDH_KeyGen_Async(NULL,
                               0, ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_ECDH_KeyGen_Finish(NULL, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_ECDH_ZGen(void **state)
{
    TSS2_RC r;

    r = Esys_ECDH_ZGen(NULL,
                       0,
                       ESYS_TR_PASSWORD,
                       ESYS_TR_NONE, ESYS_TR_NONE, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_ECDH_ZGen_Async(NULL,
                             0,
                             ESYS_TR_PASSWORD,
                             ESYS_TR_NONE, ESYS_TR_NONE, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_ECDH_ZGen_Finish(NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_ECC_Parameters(void **state)
{
    TSS2_RC r;

    r = Esys_ECC_Parameters(NULL,
                            ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE, 0, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_ECC_Parameters_Async(NULL,
                                  ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE, 0);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_ECC_Parameters_Finish(NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_ZGen_2Phase(void **state)
{
    TSS2_RC r;

    r = Esys_ZGen_2Phase(NULL,
                         0,
                         ESYS_TR_PASSWORD,
                         ESYS_TR_NONE,
                         ESYS_TR_NONE, NULL, NULL, 0, 0, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_ZGen_2Phase_Async(NULL,
                               0,
                               ESYS_TR_PASSWORD,
                               ESYS_TR_NONE, ESYS_TR_NONE, NULL, NULL, 0, 0);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_ZGen_2Phase_Finish(NULL, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_EncryptDecrypt(void **state)
{
    TSS2_RC r;

    r = Esys_EncryptDecrypt(NULL,
                            0,
                            ESYS_TR_PASSWORD,
                            ESYS_TR_NONE,
                            ESYS_TR_NONE, 0, 0, NULL, NULL, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_EncryptDecrypt_Async(NULL,
                                  0,
                                  ESYS_TR_PASSWORD,
                                  ESYS_TR_NONE, ESYS_TR_NONE, 0, 0, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_EncryptDecrypt_Finish(NULL, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_EncryptDecrypt2(void **state)
{
    TSS2_RC r;

    r = Esys_EncryptDecrypt2(NULL,
                             0,
                             ESYS_TR_PASSWORD,
                             ESYS_TR_NONE,
                             ESYS_TR_NONE, NULL, 0, 0, NULL, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_EncryptDecrypt2_Async(NULL,
                                   0,
                                   ESYS_TR_PASSWORD,
                                   ESYS_TR_NONE,
                                   ESYS_TR_NONE, NULL, 0, 0, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_EncryptDecrypt2_Finish(NULL, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_Hash(void **state)
{
    TSS2_RC r;

    r = Esys_Hash(NULL,
                  ESYS_TR_NONE,
                  ESYS_TR_NONE, ESYS_TR_NONE, NULL, 0, 0, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_Hash_Async(NULL,
                        ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE, NULL, 0, 0);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_Hash_Finish(NULL, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_HMAC(void **state)
{
    TSS2_RC r;

    r = Esys_HMAC(NULL,
                  0,
                  ESYS_TR_PASSWORD, ESYS_TR_NONE, ESYS_TR_NONE, NULL, 0, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_HMAC_Async(NULL,
                        0,
                        ESYS_TR_PASSWORD, ESYS_TR_NONE, ESYS_TR_NONE, NULL, 0);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_HMAC_Finish(NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_MAC(void **state)
{
    TSS2_RC r;

    r = Esys_MAC(NULL,
                  0,
                  ESYS_TR_PASSWORD, ESYS_TR_NONE, ESYS_TR_NONE, NULL, 0, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_MAC_Async(NULL,
                        0,
                        ESYS_TR_PASSWORD, ESYS_TR_NONE, ESYS_TR_NONE, NULL, 0);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_MAC_Finish(NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_GetRandom(void **state)
{
    TSS2_RC r;

    r = Esys_GetRandom(NULL, ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE, 0, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_GetRandom_Async(NULL, ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE, 0);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_GetRandom_Finish(NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_StirRandom(void **state)
{
    TSS2_RC r;

    r = Esys_StirRandom(NULL, ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_StirRandom_Async(NULL,
                              ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_StirRandom_Finish(NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_HMAC_Start(void **state)
{
    TSS2_RC r;

    r = Esys_HMAC_Start(NULL,
                        0,
                        ESYS_TR_PASSWORD,
                        ESYS_TR_NONE, ESYS_TR_NONE, NULL, 0, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_HMAC_Start_Async(NULL,
                              0,
                              ESYS_TR_PASSWORD,
                              ESYS_TR_NONE, ESYS_TR_NONE, NULL, 0);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_HMAC_Start_Finish(NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_MAC_Start(void **state)
{
    TSS2_RC r;

    r = Esys_MAC_Start(NULL,
                        0,
                        ESYS_TR_PASSWORD,
                        ESYS_TR_NONE, ESYS_TR_NONE, NULL, 0, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_MAC_Start_Async(NULL,
                              0,
                              ESYS_TR_PASSWORD,
                              ESYS_TR_NONE, ESYS_TR_NONE, NULL, 0);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_MAC_Start_Finish(NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_HashSequenceStart(void **state)
{
    TSS2_RC r;

    r = Esys_HashSequenceStart(NULL,
                               ESYS_TR_NONE,
                               ESYS_TR_NONE, ESYS_TR_NONE, NULL, 0, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_HashSequenceStart_Async(NULL,
                                     ESYS_TR_NONE,
                                     ESYS_TR_NONE, ESYS_TR_NONE, NULL, 0);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_HashSequenceStart_Finish(NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_SequenceUpdate(void **state)
{
    TSS2_RC r;

    r = Esys_SequenceUpdate(NULL,
                            0,
                            ESYS_TR_PASSWORD, ESYS_TR_NONE, ESYS_TR_NONE, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_SequenceUpdate_Async(NULL,
                                  0,
                                  ESYS_TR_PASSWORD,
                                  ESYS_TR_NONE, ESYS_TR_NONE, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_SequenceUpdate_Finish(NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_SequenceComplete(void **state)
{
    TSS2_RC r;

    r = Esys_SequenceComplete(NULL,
                              0,
                              ESYS_TR_PASSWORD,
                              ESYS_TR_NONE, ESYS_TR_NONE, NULL, 0, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_SequenceComplete_Async(NULL,
                                    0,
                                    ESYS_TR_PASSWORD,
                                    ESYS_TR_NONE, ESYS_TR_NONE, NULL, 0);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_SequenceComplete_Finish(NULL, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_EventSequenceComplete(void **state)
{
    TSS2_RC r;

    r = Esys_EventSequenceComplete(NULL,
                                   0,
                                   0,
                                   ESYS_TR_PASSWORD,
                                   ESYS_TR_PASSWORD, ESYS_TR_NONE, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_EventSequenceComplete_Async(NULL,
                                         0,
                                         0,
                                         ESYS_TR_PASSWORD,
                                         ESYS_TR_PASSWORD, ESYS_TR_NONE, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_EventSequenceComplete_Finish(NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_Certify(void **state)
{
    TSS2_RC r;

    r = Esys_Certify(NULL,
                     0,
                     0,
                     ESYS_TR_PASSWORD,
                     ESYS_TR_PASSWORD, ESYS_TR_NONE, NULL, NULL, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_Certify_Async(NULL,
                           0,
                           0,
                           ESYS_TR_PASSWORD,
                           ESYS_TR_PASSWORD, ESYS_TR_NONE, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_Certify_Finish(NULL, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_CertifyCreation(void **state)
{
    TSS2_RC r;

    r = Esys_CertifyCreation(NULL,
                             0,
                             0,
                             ESYS_TR_PASSWORD,
                             ESYS_TR_NONE,
                             ESYS_TR_NONE, NULL, NULL, NULL, NULL, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_CertifyCreation_Async(NULL,
                                   0,
                                   0,
                                   ESYS_TR_PASSWORD,
                                   ESYS_TR_NONE,
                                   ESYS_TR_NONE, NULL, NULL, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_CertifyCreation_Finish(NULL, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_Quote(void **state)
{
    TSS2_RC r;

    r = Esys_Quote(NULL,
                   0,
                   ESYS_TR_PASSWORD,
                   ESYS_TR_NONE, ESYS_TR_NONE, NULL, NULL, NULL, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_Quote_Async(NULL,
                         0,
                         ESYS_TR_PASSWORD,
                         ESYS_TR_NONE, ESYS_TR_NONE, NULL, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_Quote_Finish(NULL, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_GetSessionAuditDigest(void **state)
{
    TSS2_RC r;

    r = Esys_GetSessionAuditDigest(NULL,
                                   0,
                                   0,
                                   0,
                                   ESYS_TR_PASSWORD,
                                   ESYS_TR_PASSWORD,
                                   ESYS_TR_NONE, NULL, NULL, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_GetSessionAuditDigest_Async(NULL,
                                         0,
                                         0,
                                         0,
                                         ESYS_TR_PASSWORD,
                                         ESYS_TR_PASSWORD,
                                         ESYS_TR_NONE, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_GetSessionAuditDigest_Finish(NULL, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_GetCommandAuditDigest(void **state)
{
    TSS2_RC r;

    r = Esys_GetCommandAuditDigest(NULL,
                                   0,
                                   0,
                                   ESYS_TR_PASSWORD,
                                   ESYS_TR_PASSWORD,
                                   ESYS_TR_NONE, NULL, NULL, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_GetCommandAuditDigest_Async(NULL,
                                         0,
                                         0,
                                         ESYS_TR_PASSWORD,
                                         ESYS_TR_PASSWORD,
                                         ESYS_TR_NONE, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_GetCommandAuditDigest_Finish(NULL, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_GetTime(void **state)
{
    TSS2_RC r;

    r = Esys_GetTime(NULL,
                     0,
                     0,
                     ESYS_TR_PASSWORD,
                     ESYS_TR_PASSWORD, ESYS_TR_NONE, NULL, NULL, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_GetTime_Async(NULL,
                           0,
                           0,
                           ESYS_TR_PASSWORD,
                           ESYS_TR_PASSWORD, ESYS_TR_NONE, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_GetTime_Finish(NULL, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_Commit(void **state)
{
    TSS2_RC r;

    r = Esys_Commit(NULL,
                    0,
                    ESYS_TR_PASSWORD,
                    ESYS_TR_NONE,
                    ESYS_TR_NONE, NULL, NULL, NULL, NULL, NULL, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_Commit_Async(NULL,
                          0,
                          ESYS_TR_PASSWORD,
                          ESYS_TR_NONE, ESYS_TR_NONE, NULL, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_Commit_Finish(NULL, NULL, NULL, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_EC_Ephemeral(void **state)
{
    TSS2_RC r;

    r = Esys_EC_Ephemeral(NULL,
                          ESYS_TR_NONE,
                          ESYS_TR_NONE, ESYS_TR_NONE, 0, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_EC_Ephemeral_Async(NULL,
                                ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE, 0);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_EC_Ephemeral_Finish(NULL, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_VerifySignature(void **state)
{
    TSS2_RC r;

    r = Esys_VerifySignature(NULL,
                             0,
                             ESYS_TR_NONE,
                             ESYS_TR_NONE, ESYS_TR_NONE, NULL, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_VerifySignature_Async(NULL,
                                   0,
                                   ESYS_TR_NONE,
                                   ESYS_TR_NONE, ESYS_TR_NONE, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_VerifySignature_Finish(NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_Sign(void **state)
{
    TSS2_RC r;

    r = Esys_Sign(NULL,
                  0,
                  ESYS_TR_PASSWORD,
                  ESYS_TR_NONE, ESYS_TR_NONE, NULL, NULL, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_Sign_Async(NULL,
                        0,
                        ESYS_TR_PASSWORD,
                        ESYS_TR_NONE, ESYS_TR_NONE, NULL, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_Sign_Finish(NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_SetCommandCodeAuditStatus(void **state)
{
    TSS2_RC r;

    r = Esys_SetCommandCodeAuditStatus(NULL,
                                       0,
                                       ESYS_TR_PASSWORD,
                                       ESYS_TR_NONE,
                                       ESYS_TR_NONE, 0, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_SetCommandCodeAuditStatus_Async(NULL,
                                             0,
                                             ESYS_TR_PASSWORD,
                                             ESYS_TR_NONE,
                                             ESYS_TR_NONE, 0, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_SetCommandCodeAuditStatus_Finish(NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_PCR_Extend(void **state)
{
    TSS2_RC r;

    r = Esys_PCR_Extend(NULL,
                        0, ESYS_TR_PASSWORD, ESYS_TR_NONE, ESYS_TR_NONE, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_PCR_Extend_Async(NULL,
                              0,
                              ESYS_TR_PASSWORD,
                              ESYS_TR_NONE, ESYS_TR_NONE, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_PCR_Extend_Finish(NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_PCR_Event(void **state)
{
    TSS2_RC r;

    r = Esys_PCR_Event(NULL,
                       0,
                       ESYS_TR_PASSWORD,
                       ESYS_TR_NONE, ESYS_TR_NONE, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_PCR_Event_Async(NULL,
                             0,
                             ESYS_TR_PASSWORD,
                             ESYS_TR_NONE, ESYS_TR_NONE, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_PCR_Event_Finish(NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_PCR_Read(void **state)
{
    TSS2_RC r;

    r = Esys_PCR_Read(NULL,
                      ESYS_TR_NONE,
                      ESYS_TR_NONE, ESYS_TR_NONE, NULL, NULL, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_PCR_Read_Async(NULL,
                            ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_PCR_Read_Finish(NULL, NULL, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_PCR_Allocate(void **state)
{
    TSS2_RC r;

    r = Esys_PCR_Allocate(NULL,
                          0,
                          ESYS_TR_PASSWORD,
                          ESYS_TR_NONE,
                          ESYS_TR_NONE, NULL, NULL, NULL, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_PCR_Allocate_Async(NULL,
                                0,
                                ESYS_TR_PASSWORD,
                                ESYS_TR_NONE, ESYS_TR_NONE, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_PCR_Allocate_Finish(NULL, NULL, NULL, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_PCR_SetAuthPolicy(void **state)
{
    TSS2_RC r;

    r = Esys_PCR_SetAuthPolicy(NULL,
                               0,
                               ESYS_TR_PASSWORD,
                               ESYS_TR_NONE, ESYS_TR_NONE, NULL, 0, 0);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_PCR_SetAuthPolicy_Async(NULL,
                                     0,
                                     ESYS_TR_PASSWORD,
                                     ESYS_TR_NONE, ESYS_TR_NONE, NULL, 0, 0);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_PCR_SetAuthPolicy_Finish(NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_PCR_SetAuthValue(void **state)
{
    TSS2_RC r;

    r = Esys_PCR_SetAuthValue(NULL,
                              0,
                              ESYS_TR_PASSWORD,
                              ESYS_TR_NONE, ESYS_TR_NONE, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_PCR_SetAuthValue_Async(NULL,
                                    0,
                                    ESYS_TR_PASSWORD,
                                    ESYS_TR_NONE, ESYS_TR_NONE, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_PCR_SetAuthValue_Finish(NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_PCR_Reset(void **state)
{
    TSS2_RC r;

    r = Esys_PCR_Reset(NULL, 0, ESYS_TR_PASSWORD, ESYS_TR_NONE, ESYS_TR_NONE);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_PCR_Reset_Async(NULL,
                             0, ESYS_TR_PASSWORD, ESYS_TR_NONE, ESYS_TR_NONE);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_PCR_Reset_Finish(NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_PolicySigned(void **state)
{
    TSS2_RC r;

    r = Esys_PolicySigned(NULL,
                          0,
                          0,
                          ESYS_TR_NONE,
                          ESYS_TR_NONE,
                          ESYS_TR_NONE, NULL, NULL, NULL, 0, NULL, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_PolicySigned_Async(NULL,
                                0,
                                0,
                                ESYS_TR_NONE,
                                ESYS_TR_NONE,
                                ESYS_TR_NONE, NULL, NULL, NULL, 0, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_PolicySigned_Finish(NULL, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_PolicySecret(void **state)
{
    TSS2_RC r;

    r = Esys_PolicySecret(NULL,
                          0,
                          0,
                          ESYS_TR_PASSWORD,
                          ESYS_TR_NONE,
                          ESYS_TR_NONE, NULL, NULL, NULL, 0, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_PolicySecret_Async(NULL,
                                0,
                                0,
                                ESYS_TR_PASSWORD,
                                ESYS_TR_NONE,
                                ESYS_TR_NONE, NULL, NULL, NULL, 0);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_PolicySecret_Finish(NULL, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_PolicyTicket(void **state)
{
    TSS2_RC r;

    r = Esys_PolicyTicket(NULL,
                          0,
                          ESYS_TR_NONE,
                          ESYS_TR_NONE,
                          ESYS_TR_NONE, NULL, NULL, NULL, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_PolicyTicket_Async(NULL,
                                0,
                                ESYS_TR_NONE,
                                ESYS_TR_NONE,
                                ESYS_TR_NONE, NULL, NULL, NULL, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_PolicyTicket_Finish(NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_PolicyOR(void **state)
{
    TSS2_RC r;

    r = Esys_PolicyOR(NULL, 0, ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_PolicyOR_Async(NULL,
                            0, ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_PolicyOR_Finish(NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_PolicyPCR(void **state)
{
    TSS2_RC r;

    r = Esys_PolicyPCR(NULL,
                       0, ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_PolicyPCR_Async(NULL,
                             0,
                             ESYS_TR_NONE,
                             ESYS_TR_NONE, ESYS_TR_NONE, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_PolicyPCR_Finish(NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_PolicyLocality(void **state)
{
    TSS2_RC r;

    r = Esys_PolicyLocality(NULL,
                            ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE, 0, 0);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_PolicyLocality_Async(NULL,
                                  ESYS_TR_NONE,
                                  ESYS_TR_NONE, ESYS_TR_NONE, 0, 0);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_PolicyLocality_Finish(NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_PolicyNV(void **state)
{
    TSS2_RC r;

    r = Esys_PolicyNV(NULL,
                      0,
                      0,
                      0,
                      ESYS_TR_PASSWORD, ESYS_TR_NONE, ESYS_TR_NONE, NULL, 0, 0);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_PolicyNV_Async(NULL,
                            0,
                            0,
                            0,
                            ESYS_TR_PASSWORD,
                            ESYS_TR_NONE, ESYS_TR_NONE, NULL, 0, 0);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_PolicyNV_Finish(NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_PolicyCounterTimer(void **state)
{
    TSS2_RC r;

    r = Esys_PolicyCounterTimer(NULL,
                                0,
                                ESYS_TR_NONE,
                                ESYS_TR_NONE, ESYS_TR_NONE, NULL, 0, 0);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_PolicyCounterTimer_Async(NULL,
                                      0,
                                      ESYS_TR_NONE,
                                      ESYS_TR_NONE, ESYS_TR_NONE, NULL, 0, 0);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_PolicyCounterTimer_Finish(NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_PolicyCommandCode(void **state)
{
    TSS2_RC r;

    r = Esys_PolicyCommandCode(NULL,
                               0, ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE, 0);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_PolicyCommandCode_Async(NULL,
                                     0,
                                     ESYS_TR_NONE,
                                     ESYS_TR_NONE, ESYS_TR_NONE, 0);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_PolicyCommandCode_Finish(NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_PolicyPhysicalPresence(void **state)
{
    TSS2_RC r;

    r = Esys_PolicyPhysicalPresence(NULL,
                                    0,
                                    ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_PolicyPhysicalPresence_Async(NULL,
                                          0,
                                          ESYS_TR_NONE,
                                          ESYS_TR_NONE, ESYS_TR_NONE);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_PolicyPhysicalPresence_Finish(NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_PolicyCpHash(void **state)
{
    TSS2_RC r;

    r = Esys_PolicyCpHash(NULL,
                          ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE, 0, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_PolicyCpHash_Async(NULL,
                                ESYS_TR_NONE,
                                ESYS_TR_NONE, ESYS_TR_NONE, 0, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_PolicyCpHash_Finish(NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_PolicyNameHash(void **state)
{
    TSS2_RC r;

    r = Esys_PolicyNameHash(NULL,
                            ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE, 0, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_PolicyNameHash_Async(NULL,
                                  ESYS_TR_NONE,
                                  ESYS_TR_NONE, ESYS_TR_NONE, 0, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_PolicyNameHash_Finish(NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_PolicyDuplicationSelect(void **state)
{
    TSS2_RC r;

    r = Esys_PolicyDuplicationSelect(NULL,
                                     ESYS_TR_NONE,
                                     ESYS_TR_NONE,
                                     ESYS_TR_NONE, 0, NULL, NULL, 0);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_PolicyDuplicationSelect_Async(NULL,
                                           ESYS_TR_NONE,
                                           ESYS_TR_NONE,
                                           ESYS_TR_NONE, 0, NULL, NULL, 0);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_PolicyDuplicationSelect_Finish(NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_PolicyAuthorize(void **state)
{
    TSS2_RC r;

    r = Esys_PolicyAuthorize(NULL,
                             0,
                             ESYS_TR_NONE,
                             ESYS_TR_NONE,
                             ESYS_TR_NONE, NULL, NULL, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_PolicyAuthorize_Async(NULL,
                                   0,
                                   ESYS_TR_NONE,
                                   ESYS_TR_NONE,
                                   ESYS_TR_NONE, NULL, NULL, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_PolicyAuthorize_Finish(NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_PolicyAuthValue(void **state)
{
    TSS2_RC r;

    r = Esys_PolicyAuthValue(NULL, 0, ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_PolicyAuthValue_Async(NULL,
                                   0, ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_PolicyAuthValue_Finish(NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_PolicyPassword(void **state)
{
    TSS2_RC r;

    r = Esys_PolicyPassword(NULL, 0, ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_PolicyPassword_Async(NULL,
                                  0, ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_PolicyPassword_Finish(NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_PolicyGetDigest(void **state)
{
    TSS2_RC r;

    r = Esys_PolicyGetDigest(NULL,
                             0, ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_PolicyGetDigest_Async(NULL,
                                   0, ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_PolicyGetDigest_Finish(NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_PolicyNvWritten(void **state)
{
    TSS2_RC r;

    r = Esys_PolicyNvWritten(NULL,
                             0, ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE, 0);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_PolicyNvWritten_Async(NULL,
                                   0,
                                   ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE, 0);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_PolicyNvWritten_Finish(NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_PolicyTemplate(void **state)
{
    TSS2_RC r;

    r = Esys_PolicyTemplate(NULL,
                            ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE, 0, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_PolicyTemplate_Async(NULL,
                                  ESYS_TR_NONE,
                                  ESYS_TR_NONE, ESYS_TR_NONE, 0, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_PolicyTemplate_Finish(NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_PolicyAuthorizeNV(void **state)
{
    TSS2_RC r;

    r = Esys_PolicyAuthorizeNV(NULL,
                               0,
                               0,
                               0, ESYS_TR_PASSWORD, ESYS_TR_NONE, ESYS_TR_NONE);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_PolicyAuthorizeNV_Async(NULL,
                                     0,
                                     0,
                                     0,
                                     ESYS_TR_PASSWORD,
                                     ESYS_TR_NONE, ESYS_TR_NONE);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_PolicyAuthorizeNV_Finish(NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_CreatePrimary(void **state)
{
    TSS2_RC r;

    r = Esys_CreatePrimary(NULL,
                           0,
                           ESYS_TR_PASSWORD,
                           ESYS_TR_NONE,
                           ESYS_TR_NONE,
                           NULL,
                           NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_CreatePrimary_Async(NULL,
                                 0,
                                 ESYS_TR_PASSWORD,
                                 ESYS_TR_NONE,
                                 ESYS_TR_NONE, NULL, NULL, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_CreatePrimary_Finish(NULL, NULL, NULL, NULL, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_HierarchyControl(void **state)
{
    TSS2_RC r;

    r = Esys_HierarchyControl(NULL,
                              0,
                              ESYS_TR_PASSWORD,
                              ESYS_TR_NONE, ESYS_TR_NONE, 0, 0);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_HierarchyControl_Async(NULL,
                                    0,
                                    ESYS_TR_PASSWORD,
                                    ESYS_TR_NONE, ESYS_TR_NONE, 0, 0);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_HierarchyControl_Finish(NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_SetPrimaryPolicy(void **state)
{
    TSS2_RC r;

    r = Esys_SetPrimaryPolicy(NULL,
                              0,
                              ESYS_TR_PASSWORD,
                              ESYS_TR_NONE, ESYS_TR_NONE, NULL, 0);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_SetPrimaryPolicy_Async(NULL,
                                    0,
                                    ESYS_TR_PASSWORD,
                                    ESYS_TR_NONE, ESYS_TR_NONE, NULL, 0);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_SetPrimaryPolicy_Finish(NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_ChangePPS(void **state)
{
    TSS2_RC r;

    r = Esys_ChangePPS(NULL, 0, ESYS_TR_PASSWORD, ESYS_TR_NONE, ESYS_TR_NONE);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_ChangePPS_Async(NULL,
                             0, ESYS_TR_PASSWORD, ESYS_TR_NONE, ESYS_TR_NONE);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_ChangePPS_Finish(NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_ChangeEPS(void **state)
{
    TSS2_RC r;

    r = Esys_ChangeEPS(NULL, 0, ESYS_TR_PASSWORD, ESYS_TR_NONE, ESYS_TR_NONE);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_ChangeEPS_Async(NULL,
                             0, ESYS_TR_PASSWORD, ESYS_TR_NONE, ESYS_TR_NONE);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_ChangeEPS_Finish(NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_Clear(void **state)
{
    TSS2_RC r;

    r = Esys_Clear(NULL, 0, ESYS_TR_PASSWORD, ESYS_TR_NONE, ESYS_TR_NONE);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_Clear_Async(NULL, 0, ESYS_TR_PASSWORD, ESYS_TR_NONE, ESYS_TR_NONE);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_Clear_Finish(NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_ClearControl(void **state)
{
    TSS2_RC r;

    r = Esys_ClearControl(NULL,
                          0, ESYS_TR_PASSWORD, ESYS_TR_NONE, ESYS_TR_NONE, 0);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_ClearControl_Async(NULL,
                                0,
                                ESYS_TR_PASSWORD,
                                ESYS_TR_NONE, ESYS_TR_NONE, 0);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_ClearControl_Finish(NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_HierarchyChangeAuth(void **state)
{
    TSS2_RC r;

    r = Esys_HierarchyChangeAuth(NULL,
                                 0,
                                 ESYS_TR_PASSWORD,
                                 ESYS_TR_NONE, ESYS_TR_NONE, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_HierarchyChangeAuth_Async(NULL,
                                       0,
                                       ESYS_TR_PASSWORD,
                                       ESYS_TR_NONE, ESYS_TR_NONE, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_HierarchyChangeAuth_Finish(NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_DictionaryAttackLockReset(void **state)
{
    TSS2_RC r;

    r = Esys_DictionaryAttackLockReset(NULL,
                                       0,
                                       ESYS_TR_PASSWORD,
                                       ESYS_TR_NONE, ESYS_TR_NONE);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_DictionaryAttackLockReset_Async(NULL,
                                             0,
                                             ESYS_TR_PASSWORD,
                                             ESYS_TR_NONE, ESYS_TR_NONE);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_DictionaryAttackLockReset_Finish(NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_DictionaryAttackParameters(void **state)
{
    TSS2_RC r;

    r = Esys_DictionaryAttackParameters(NULL,
                                        0,
                                        ESYS_TR_PASSWORD,
                                        ESYS_TR_NONE, ESYS_TR_NONE, 0, 0, 0);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_DictionaryAttackParameters_Async(NULL,
                                              0,
                                              ESYS_TR_PASSWORD,
                                              ESYS_TR_NONE,
                                              ESYS_TR_NONE, 0, 0, 0);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_DictionaryAttackParameters_Finish(NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_PP_Commands(void **state)
{
    TSS2_RC r;

    r = Esys_PP_Commands(NULL,
                         0,
                         ESYS_TR_PASSWORD,
                         ESYS_TR_NONE, ESYS_TR_NONE, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_PP_Commands_Async(NULL,
                               0,
                               ESYS_TR_PASSWORD,
                               ESYS_TR_NONE, ESYS_TR_NONE, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_PP_Commands_Finish(NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_SetAlgorithmSet(void **state)
{
    TSS2_RC r;

    r = Esys_SetAlgorithmSet(NULL,
                             0,
                             ESYS_TR_PASSWORD, ESYS_TR_NONE, ESYS_TR_NONE, 0);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_SetAlgorithmSet_Async(NULL,
                                   0,
                                   ESYS_TR_PASSWORD,
                                   ESYS_TR_NONE, ESYS_TR_NONE, 0);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_SetAlgorithmSet_Finish(NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_FieldUpgradeStart(void **state)
{
    TSS2_RC r;

    r = Esys_FieldUpgradeStart(NULL,
                               0,
                               0,
                               ESYS_TR_PASSWORD,
                               ESYS_TR_NONE, ESYS_TR_NONE, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_FieldUpgradeStart_Async(NULL,
                                     0,
                                     0,
                                     ESYS_TR_PASSWORD,
                                     ESYS_TR_NONE, ESYS_TR_NONE, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_FieldUpgradeStart_Finish(NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_FieldUpgradeData(void **state)
{
    TSS2_RC r;

    r = Esys_FieldUpgradeData(NULL,
                              ESYS_TR_NONE,
                              ESYS_TR_NONE, ESYS_TR_NONE, NULL, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_FieldUpgradeData_Async(NULL,
                                    ESYS_TR_NONE,
                                    ESYS_TR_NONE, ESYS_TR_NONE, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_FieldUpgradeData_Finish(NULL, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_FirmwareRead(void **state)
{
    TSS2_RC r;

    r = Esys_FirmwareRead(NULL,
                          ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE, 0, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_FirmwareRead_Async(NULL,
                                ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE, 0);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_FirmwareRead_Finish(NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_ContextSave(void **state)
{
    TSS2_RC r;

    r = Esys_ContextSave(NULL, 0, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_ContextSave_Async(NULL, 0);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_ContextSave_Finish(NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_ContextLoad(void **state)
{
    TSS2_RC r;

    r = Esys_ContextLoad(NULL, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_ContextLoad_Async(NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_ContextLoad_Finish(NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_FlushContext(void **state)
{
    TSS2_RC r;

    r = Esys_FlushContext(NULL, 0);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_FlushContext_Async(NULL, 0);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_FlushContext_Finish(NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_EvictControl(void **state)
{
    TSS2_RC r;

    r = Esys_EvictControl(NULL,
                          0,
                          0,
                          ESYS_TR_PASSWORD,
                          ESYS_TR_NONE, ESYS_TR_NONE, 0, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_EvictControl_Async(NULL,
                                0,
                                0,
                                ESYS_TR_PASSWORD,
                                ESYS_TR_NONE, ESYS_TR_NONE, 0);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_EvictControl_Finish(NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_ReadClock(void **state)
{
    TSS2_RC r;

    r = Esys_ReadClock(NULL, ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_ReadClock_Async(NULL, ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_ReadClock_Finish(NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_ClockSet(void **state)
{
    TSS2_RC r;

    r = Esys_ClockSet(NULL, 0, ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE, 0);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_ClockSet_Async(NULL,
                            0, ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE, 0);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_ClockSet_Finish(NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_ClockRateAdjust(void **state)
{
    TSS2_RC r;

    r = Esys_ClockRateAdjust(NULL,
                             0,
                             ESYS_TR_PASSWORD, ESYS_TR_NONE, ESYS_TR_NONE, 0);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_ClockRateAdjust_Async(NULL,
                                   0,
                                   ESYS_TR_PASSWORD,
                                   ESYS_TR_NONE, ESYS_TR_NONE, 0);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_ClockRateAdjust_Finish(NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_GetCapability(void **state)
{
    TSS2_RC r;

    r = Esys_GetCapability(NULL,
                           ESYS_TR_NONE,
                           ESYS_TR_NONE, ESYS_TR_NONE, 0, 0, 0, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_GetCapability_Async(NULL,
                                 ESYS_TR_NONE,
                                 ESYS_TR_NONE, ESYS_TR_NONE, 0, 0, 0);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_GetCapability_Finish(NULL, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_TestParms(void **state)
{
    TSS2_RC r;

    r = Esys_TestParms(NULL, ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_TestParms_Async(NULL,
                             ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_TestParms_Finish(NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_NV_DefineSpace(void **state)
{
    TSS2_RC r;

    r = Esys_NV_DefineSpace(NULL,
                            0,
                            ESYS_TR_PASSWORD,
                            ESYS_TR_NONE, ESYS_TR_NONE, NULL, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_NV_DefineSpace_Async(NULL,
                                  0,
                                  ESYS_TR_PASSWORD,
                                  ESYS_TR_NONE, ESYS_TR_NONE, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_NV_DefineSpace_Finish(NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_NV_UndefineSpace(void **state)
{
    TSS2_RC r;

    r = Esys_NV_UndefineSpace(NULL,
                              0,
                              0, ESYS_TR_PASSWORD, ESYS_TR_NONE, ESYS_TR_NONE);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_NV_UndefineSpace_Async(NULL,
                                    0,
                                    0,
                                    ESYS_TR_PASSWORD,
                                    ESYS_TR_NONE, ESYS_TR_NONE);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_NV_UndefineSpace_Finish(NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_NV_UndefineSpaceSpecial(void **state)
{
    TSS2_RC r;

    r = Esys_NV_UndefineSpaceSpecial(NULL,
                                     0,
                                     0,
                                     ESYS_TR_PASSWORD,
                                     ESYS_TR_PASSWORD, ESYS_TR_NONE);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_NV_UndefineSpaceSpecial_Async(NULL,
                                           0,
                                           0,
                                           ESYS_TR_PASSWORD,
                                           ESYS_TR_PASSWORD, ESYS_TR_NONE);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_NV_UndefineSpaceSpecial_Finish(NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_NV_ReadPublic(void **state)
{
    TSS2_RC r;

    r = Esys_NV_ReadPublic(NULL,
                           0,
                           ESYS_TR_NONE,
                           ESYS_TR_NONE, ESYS_TR_NONE, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_NV_ReadPublic_Async(NULL,
                                 0, ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_NV_ReadPublic_Finish(NULL, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_NV_Write(void **state)
{
    TSS2_RC r;

    r = Esys_NV_Write(NULL,
                      0,
                      0, ESYS_TR_PASSWORD, ESYS_TR_NONE, ESYS_TR_NONE, NULL, 0);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_NV_Write_Async(NULL,
                            0,
                            0,
                            ESYS_TR_PASSWORD,
                            ESYS_TR_NONE, ESYS_TR_NONE, NULL, 0);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_NV_Write_Finish(NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_NV_Increment(void **state)
{
    TSS2_RC r;

    r = Esys_NV_Increment(NULL,
                          0, 0, ESYS_TR_PASSWORD, ESYS_TR_NONE, ESYS_TR_NONE);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_NV_Increment_Async(NULL,
                                0,
                                0,
                                ESYS_TR_PASSWORD, ESYS_TR_NONE, ESYS_TR_NONE);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_NV_Increment_Finish(NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_NV_Extend(void **state)
{
    TSS2_RC r;

    r = Esys_NV_Extend(NULL,
                       0,
                       0, ESYS_TR_PASSWORD, ESYS_TR_NONE, ESYS_TR_NONE, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_NV_Extend_Async(NULL,
                             0,
                             0,
                             ESYS_TR_PASSWORD,
                             ESYS_TR_NONE, ESYS_TR_NONE, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_NV_Extend_Finish(NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_NV_SetBits(void **state)
{
    TSS2_RC r;

    r = Esys_NV_SetBits(NULL,
                        0, 0, ESYS_TR_PASSWORD, ESYS_TR_NONE, ESYS_TR_NONE, 0);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_NV_SetBits_Async(NULL,
                              0,
                              0,
                              ESYS_TR_PASSWORD, ESYS_TR_NONE, ESYS_TR_NONE, 0);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_NV_SetBits_Finish(NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_NV_WriteLock(void **state)
{
    TSS2_RC r;

    r = Esys_NV_WriteLock(NULL,
                          0, 0, ESYS_TR_PASSWORD, ESYS_TR_NONE, ESYS_TR_NONE);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_NV_WriteLock_Async(NULL,
                                0,
                                0,
                                ESYS_TR_PASSWORD, ESYS_TR_NONE, ESYS_TR_NONE);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_NV_WriteLock_Finish(NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_NV_GlobalWriteLock(void **state)
{
    TSS2_RC r;

    r = Esys_NV_GlobalWriteLock(NULL,
                                0,
                                ESYS_TR_PASSWORD, ESYS_TR_NONE, ESYS_TR_NONE);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_NV_GlobalWriteLock_Async(NULL,
                                      0,
                                      ESYS_TR_PASSWORD,
                                      ESYS_TR_NONE, ESYS_TR_NONE);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_NV_GlobalWriteLock_Finish(NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_NV_Read(void **state)
{
    TSS2_RC r;

    r = Esys_NV_Read(NULL,
                     0,
                     0,
                     ESYS_TR_PASSWORD, ESYS_TR_NONE, ESYS_TR_NONE, 0, 0, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_NV_Read_Async(NULL,
                           0,
                           0,
                           ESYS_TR_PASSWORD, ESYS_TR_NONE, ESYS_TR_NONE, 0, 0);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_NV_Read_Finish(NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_NV_ReadLock(void **state)
{
    TSS2_RC r;

    r = Esys_NV_ReadLock(NULL,
                         0, 0, ESYS_TR_PASSWORD, ESYS_TR_NONE, ESYS_TR_NONE);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_NV_ReadLock_Async(NULL,
                               0,
                               0, ESYS_TR_PASSWORD, ESYS_TR_NONE, ESYS_TR_NONE);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_NV_ReadLock_Finish(NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_NV_ChangeAuth(void **state)
{
    TSS2_RC r;

    r = Esys_NV_ChangeAuth(NULL,
                           0,
                           ESYS_TR_PASSWORD, ESYS_TR_NONE, ESYS_TR_NONE, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_NV_ChangeAuth_Async(NULL,
                                 0,
                                 ESYS_TR_PASSWORD,
                                 ESYS_TR_NONE, ESYS_TR_NONE, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_NV_ChangeAuth_Finish(NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_NV_Certify(void **state)
{
    TSS2_RC r;

    r = Esys_NV_Certify(NULL,
                        0,
                        0,
                        0,
                        ESYS_TR_PASSWORD,
                        ESYS_TR_PASSWORD,
                        ESYS_TR_NONE, NULL, NULL, 0, 0, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_NV_Certify_Async(NULL,
                              0,
                              0,
                              0,
                              ESYS_TR_PASSWORD,
                              ESYS_TR_PASSWORD, ESYS_TR_NONE, NULL, NULL, 0, 0);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_NV_Certify_Finish(NULL, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_Vendor_TCG_Test(void **state)
{
    TSS2_RC r;

    r = Esys_Vendor_TCG_Test(NULL,
                             ESYS_TR_NONE,
                             ESYS_TR_NONE, ESYS_TR_NONE, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_Vendor_TCG_Test_Async(NULL,
                                   ESYS_TR_NONE,
                                   ESYS_TR_NONE, ESYS_TR_NONE, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_Vendor_TCG_Test_Finish(NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_AC_GetCapability(void **state)
{
    TSS2_RC r;

    r = Esys_AC_GetCapability(NULL, ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE,
                              0, 0, 0, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_AC_GetCapability_Async(NULL, ESYS_TR_NONE, ESYS_TR_NONE,
                                    ESYS_TR_NONE, 0, 0, 0);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_AC_GetCapability_Finish(NULL, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_AC_Send(void **state)
{
    TSS2_RC r;

    r = Esys_AC_Send(NULL, ESYS_TR_NONE, ESYS_TR_NONE,  ESYS_TR_NONE,
                     ESYS_TR_NONE, ESYS_TR_NONE, 0, NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_AC_Send_Async(NULL, ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE,
                           ESYS_TR_NONE, ESYS_TR_NONE, 0, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_AC_Send_Finish(NULL, NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

void
check_Policy_AC_SendSelect(void **state)
{
    TSS2_RC r;

    r = Esys_Policy_AC_SendSelect(NULL, ESYS_TR_NONE, ESYS_TR_NONE,
                                  ESYS_TR_NONE, NULL, NULL, NULL, 0);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_Policy_AC_SendSelect_Async(NULL, ESYS_TR_NONE, ESYS_TR_NONE,
                                        ESYS_TR_NONE, NULL, NULL, NULL, 0);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);

    r = Esys_Policy_AC_SendSelect_Finish(NULL);
    assert_int_equal(r, TSS2_ESYS_RC_BAD_REFERENCE);
}

int
main(void)
{
    const struct CMUnitTest tests[] = {
        cmocka_unit_test(check_Startup),
        cmocka_unit_test(check_Shutdown),
        cmocka_unit_test(check_SelfTest),
        cmocka_unit_test(check_IncrementalSelfTest),
        cmocka_unit_test(check_GetTestResult),
        cmocka_unit_test(check_StartAuthSession),
        cmocka_unit_test(check_PolicyRestart),
        cmocka_unit_test(check_Create),
        cmocka_unit_test(check_Load),
        cmocka_unit_test(check_LoadExternal),
        cmocka_unit_test(check_ReadPublic),
        cmocka_unit_test(check_ActivateCredential),
        cmocka_unit_test(check_MakeCredential),
        cmocka_unit_test(check_Unseal),
        cmocka_unit_test(check_ObjectChangeAuth),
        cmocka_unit_test(check_CreateLoaded),
        cmocka_unit_test(check_Duplicate),
        cmocka_unit_test(check_Rewrap),
        cmocka_unit_test(check_Import),
        cmocka_unit_test(check_RSA_Encrypt),
        cmocka_unit_test(check_RSA_Decrypt),
        cmocka_unit_test(check_ECDH_KeyGen),
        cmocka_unit_test(check_ECDH_ZGen),
        cmocka_unit_test(check_ECC_Parameters),
        cmocka_unit_test(check_ZGen_2Phase),
        cmocka_unit_test(check_EncryptDecrypt),
        cmocka_unit_test(check_EncryptDecrypt2),
        cmocka_unit_test(check_Hash),
        cmocka_unit_test(check_HMAC),
        cmocka_unit_test(check_GetRandom),
        cmocka_unit_test(check_StirRandom),
        cmocka_unit_test(check_HMAC_Start),
        cmocka_unit_test(check_HashSequenceStart),
        cmocka_unit_test(check_SequenceUpdate),
        cmocka_unit_test(check_SequenceComplete),
        cmocka_unit_test(check_EventSequenceComplete),
        cmocka_unit_test(check_Certify),
        cmocka_unit_test(check_CertifyCreation),
        cmocka_unit_test(check_Quote),
        cmocka_unit_test(check_GetSessionAuditDigest),
        cmocka_unit_test(check_GetCommandAuditDigest),
        cmocka_unit_test(check_GetTime),
        cmocka_unit_test(check_Commit),
        cmocka_unit_test(check_EC_Ephemeral),
        cmocka_unit_test(check_VerifySignature),
        cmocka_unit_test(check_Sign),
        cmocka_unit_test(check_SetCommandCodeAuditStatus),
        cmocka_unit_test(check_PCR_Extend),
        cmocka_unit_test(check_PCR_Event),
        cmocka_unit_test(check_PCR_Read),
        cmocka_unit_test(check_PCR_Allocate),
        cmocka_unit_test(check_PCR_SetAuthPolicy),
        cmocka_unit_test(check_PCR_SetAuthValue),
        cmocka_unit_test(check_PCR_Reset),
        cmocka_unit_test(check_PolicySigned),
        cmocka_unit_test(check_PolicySecret),
        cmocka_unit_test(check_PolicyTicket),
        cmocka_unit_test(check_PolicyOR),
        cmocka_unit_test(check_PolicyPCR),
        cmocka_unit_test(check_PolicyLocality),
        cmocka_unit_test(check_PolicyNV),
        cmocka_unit_test(check_PolicyCounterTimer),
        cmocka_unit_test(check_PolicyCommandCode),
        cmocka_unit_test(check_PolicyPhysicalPresence),
        cmocka_unit_test(check_PolicyCpHash),
        cmocka_unit_test(check_PolicyNameHash),
        cmocka_unit_test(check_PolicyDuplicationSelect),
        cmocka_unit_test(check_PolicyAuthorize),
        cmocka_unit_test(check_PolicyAuthValue),
        cmocka_unit_test(check_PolicyPassword),
        cmocka_unit_test(check_PolicyGetDigest),
        cmocka_unit_test(check_PolicyNvWritten),
        cmocka_unit_test(check_PolicyTemplate),
        cmocka_unit_test(check_PolicyAuthorizeNV),
        cmocka_unit_test(check_CreatePrimary),
        cmocka_unit_test(check_HierarchyControl),
        cmocka_unit_test(check_SetPrimaryPolicy),
        cmocka_unit_test(check_ChangePPS),
        cmocka_unit_test(check_ChangeEPS),
        cmocka_unit_test(check_Clear),
        cmocka_unit_test(check_ClearControl),
        cmocka_unit_test(check_HierarchyChangeAuth),
        cmocka_unit_test(check_DictionaryAttackLockReset),
        cmocka_unit_test(check_DictionaryAttackParameters),
        cmocka_unit_test(check_PP_Commands),
        cmocka_unit_test(check_SetAlgorithmSet),
        cmocka_unit_test(check_FieldUpgradeStart),
        cmocka_unit_test(check_FieldUpgradeData),
        cmocka_unit_test(check_FirmwareRead),
        cmocka_unit_test(check_ContextSave),
        cmocka_unit_test(check_ContextLoad),
        cmocka_unit_test(check_FlushContext),
        cmocka_unit_test(check_EvictControl),
        cmocka_unit_test(check_ReadClock),
        cmocka_unit_test(check_ClockSet),
        cmocka_unit_test(check_ClockRateAdjust),
        cmocka_unit_test(check_GetCapability),
        cmocka_unit_test(check_TestParms),
        cmocka_unit_test(check_NV_DefineSpace),
        cmocka_unit_test(check_NV_UndefineSpace),
        cmocka_unit_test(check_NV_UndefineSpaceSpecial),
        cmocka_unit_test(check_NV_ReadPublic),
        cmocka_unit_test(check_NV_Write),
        cmocka_unit_test(check_NV_Increment),
        cmocka_unit_test(check_NV_Extend),
        cmocka_unit_test(check_NV_SetBits),
        cmocka_unit_test(check_NV_WriteLock),
        cmocka_unit_test(check_NV_GlobalWriteLock),
        cmocka_unit_test(check_NV_Read),
        cmocka_unit_test(check_NV_ReadLock),
        cmocka_unit_test(check_NV_ChangeAuth),
        cmocka_unit_test(check_NV_Certify),
        cmocka_unit_test(check_Vendor_TCG_Test),
        cmocka_unit_test(check_AC_GetCapability),
        cmocka_unit_test(check_AC_Send),
        cmocka_unit_test(check_Policy_AC_SendSelect)
    };
    return cmocka_run_group_tests(tests, NULL, NULL);
}
