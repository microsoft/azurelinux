/* SPDX-License-Identifier: BSD-2-Clause */
/*******************************************************************************
 * Copyright 2018, Fraunhofer SIT sponsored by Infineon Technologies AG
 * All rights reserved.
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
#include "esys_crypto.h"

#define LOGMODULE tests
#include "util/log.h"

/**
 * This unit tst checks several error cases of the crypto backends, which are not
 * covered by the integration tests.
 */

static void
check_hash_functions(void **state)
{
    TSS2_RC rc;
    ESYS_CRYPTO_CONTEXT_BLOB *context;
    uint8_t buffer[10] = { 0 };
    TPM2B tpm2b;
    size_t size = 0;

    ESYS_CRYPTO_CALLBACKS crypto_cb = { 0 };
    rc = iesys_initialize_crypto_backend(&crypto_cb, NULL);
    assert_int_equal (rc, TSS2_RC_SUCCESS);

    rc = iesys_crypto_hash_start(&crypto_cb, NULL, TPM2_ALG_SHA384);
    assert_int_equal (rc, TSS2_ESYS_RC_BAD_REFERENCE);

    rc = iesys_crypto_hash_start(&crypto_cb, &context, 0);
    assert_int_equal (rc, TSS2_ESYS_RC_NOT_IMPLEMENTED);

    rc = iesys_crypto_hash_start(&crypto_cb, &context, TPM2_ALG_SHA512);
    assert_int_equal (rc, TSS2_RC_SUCCESS);

    rc = iesys_crypto_hash_finish(&crypto_cb, NULL, &buffer[0], &size);
    assert_int_equal (rc, TSS2_ESYS_RC_BAD_REFERENCE);

    rc = iesys_crypto_hash_finish(&crypto_cb, &context, &buffer[0], &size);
    assert_int_equal (rc, TSS2_ESYS_RC_BAD_SIZE);

    iesys_crypto_hash_abort(&crypto_cb, NULL);
    iesys_crypto_hash_abort(&crypto_cb, &context);

    rc = iesys_crypto_hash_update(&crypto_cb, NULL, &buffer[0], 10);
    assert_int_equal (rc, TSS2_ESYS_RC_BAD_REFERENCE);

    rc = iesys_crypto_hash_update2b(&crypto_cb, NULL, &tpm2b);
    assert_int_equal (rc, TSS2_ESYS_RC_BAD_REFERENCE);

    /* Create invalid context */
    rc = iesys_crypto_hmac_start(&crypto_cb, &context, TPM2_ALG_SHA1, &buffer[0], 10);
    assert_int_equal (rc, TSS2_RC_SUCCESS);

    iesys_crypto_hash_abort(&crypto_cb, &context);

    rc = iesys_crypto_hash_update(&crypto_cb, context, &buffer[0], 10);
    assert_int_equal (rc, TSS2_ESYS_RC_BAD_REFERENCE);

    rc = iesys_crypto_hash_finish(&crypto_cb, &context, &buffer[0], &size);
    assert_int_equal (rc, TSS2_ESYS_RC_BAD_REFERENCE);

    /* cleanup */
    iesys_crypto_hmac_abort(&crypto_cb, &context);
}

static void
check_hmac_functions(void **state)
{
    TSS2_RC rc;
    ESYS_CRYPTO_CONTEXT_BLOB *context;
    uint8_t buffer[10] = { 0 };
    TPM2B tpm2b;
    size_t size = 0;

    ESYS_CRYPTO_CALLBACKS crypto_cb = { 0 };
    rc = iesys_initialize_crypto_backend(&crypto_cb, NULL);
    assert_int_equal (rc, TSS2_RC_SUCCESS);

    rc = iesys_crypto_hmac_start(&crypto_cb, NULL, TPM2_ALG_SHA384, &buffer[0], 10);
    assert_int_equal (rc, TSS2_ESYS_RC_BAD_REFERENCE);

#ifndef OSSL
    rc = iesys_crypto_hmac_start(&crypto_cb, &context, TPM2_ALG_SHA512, &buffer[0], 10);
    assert_int_equal (rc, TSS2_ESYS_RC_NOT_IMPLEMENTED);
#endif

    rc = iesys_crypto_hmac_start(&crypto_cb, &context, 0,  &buffer[0], 10);
    assert_int_equal (rc, TSS2_ESYS_RC_NOT_IMPLEMENTED);

    rc = iesys_crypto_hmac_start(&crypto_cb, &context, TPM2_ALG_SHA1,  &buffer[0], 10);
    assert_int_equal (rc, TSS2_RC_SUCCESS);

    rc = iesys_crypto_hmac_finish(&crypto_cb, NULL, &buffer[0], &size);
    assert_int_equal (rc, TSS2_ESYS_RC_BAD_REFERENCE);

    rc = iesys_crypto_hmac_finish2b(&crypto_cb, NULL, &tpm2b);
    assert_int_equal (rc, TSS2_ESYS_RC_BAD_REFERENCE);

    rc = iesys_crypto_hmac_finish(&crypto_cb, &context, &buffer[0], &size);
    assert_int_equal (rc, TSS2_ESYS_RC_BAD_SIZE);

    iesys_crypto_hmac_abort(&crypto_cb, NULL);
    iesys_crypto_hmac_abort(&crypto_cb, &context);

    rc = iesys_crypto_hmac_update(&crypto_cb, NULL, &buffer[0], 10);
    assert_int_equal (rc, TSS2_ESYS_RC_BAD_REFERENCE);

    rc = iesys_crypto_hmac_update2b(&crypto_cb, NULL, &tpm2b);
    assert_int_equal (rc, TSS2_ESYS_RC_BAD_REFERENCE);

    /* Create invalid context */
    rc = iesys_crypto_hash_start(&crypto_cb, &context, TPM2_ALG_SHA1);
    assert_int_equal (rc, TSS2_RC_SUCCESS);

    iesys_crypto_hmac_abort(&crypto_cb, &context);

    rc = iesys_crypto_hmac_update(&crypto_cb, context, &buffer[0], 10);
    assert_int_equal (rc, TSS2_ESYS_RC_BAD_REFERENCE);

    rc = iesys_crypto_hmac_finish(&crypto_cb, &context, &buffer[0], &size);
    assert_int_equal (rc, TSS2_ESYS_RC_BAD_REFERENCE);

    /* cleanup */
    iesys_crypto_hash_abort(&crypto_cb, &context);
}

static void
check_random(void **state)
{
    TSS2_RC rc;
    size_t num_bytes = 0;
    TPM2B_NONCE nonce;

    ESYS_CRYPTO_CALLBACKS crypto_cb = { 0 };
    rc = iesys_initialize_crypto_backend(&crypto_cb, NULL);
    assert_int_equal (rc, TSS2_RC_SUCCESS);

    rc = iesys_crypto_get_random2b(&crypto_cb, &nonce, num_bytes);
    assert_int_equal (rc, TSS2_RC_SUCCESS);
}

static void
check_pk_encrypt(void **state)
{
    TSS2_RC rc;
    uint8_t in_buffer[5] = { 1, 2, 3, 4, 5 };
    size_t size = 5;
    uint8_t out_buffer[5];
    TPM2B_PUBLIC inPublicRSA = {
        .size = 0,
        .publicArea = {
            .type = TPM2_ALG_RSA,
            .nameAlg = TPM2_ALG_SHA1,
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
                     .mode.aes = TPM2_ALG_CFB,
                 },
                 .scheme = {
                      .scheme =
                      TPM2_ALG_NULL,
                  },
                 .keyBits = 2048,
                 .exponent = 0,
             },
            .unique.rsa = {
                 .size = 0,
                 .buffer = {}
                 ,
             }
        }
    };

    inPublicRSA.publicArea.nameAlg = 0;

    ESYS_CRYPTO_CALLBACKS crypto_cb = { 0 };
    rc = iesys_initialize_crypto_backend(&crypto_cb, NULL);
    assert_int_equal (rc, TSS2_RC_SUCCESS);

    rc = iesys_crypto_rsa_pk_encrypt(&crypto_cb, &inPublicRSA, size, &in_buffer[0], size, &out_buffer[0], &size, "LABEL");
    assert_int_equal (rc, TSS2_ESYS_RC_NOT_IMPLEMENTED);

    inPublicRSA.publicArea.nameAlg = TPM2_ALG_SHA1;
    inPublicRSA.publicArea.parameters.rsaDetail.scheme.scheme = 0;
    rc = iesys_crypto_rsa_pk_encrypt(&crypto_cb, &inPublicRSA, size, &in_buffer[0], size, &out_buffer[0], &size, "LABEL");
    assert_int_equal (rc, TSS2_ESYS_RC_BAD_VALUE);
}

static void
check_aes_encrypt(void **state)
{
    TSS2_RC rc;
    uint8_t key[32] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16,
                       1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16  };
    uint8_t buffer[5] = { 1, 2, 3, 4, 5 };
    size_t size = 5;

    ESYS_CRYPTO_CALLBACKS crypto_cb = { 0 };
    rc = iesys_initialize_crypto_backend(&crypto_cb, NULL);
    assert_int_equal (rc, TSS2_RC_SUCCESS);

    rc = iesys_crypto_aes_encrypt(&crypto_cb, NULL, TPM2_ALG_AES, 192, TPM2_ALG_CFB,
                                      &buffer[0], size, &key[0]);
    assert_int_equal (rc, TSS2_ESYS_RC_BAD_REFERENCE);

    rc = iesys_crypto_aes_encrypt(&crypto_cb, &key[0], TPM2_ALG_AES, 192, TPM2_ALG_CFB,
                                      &buffer[0], size, &key[0]);
    assert_int_equal (rc, TSS2_RC_SUCCESS);
    rc = iesys_crypto_aes_encrypt(&crypto_cb, &key[0], TPM2_ALG_AES, 256, TPM2_ALG_CFB,
                                      &buffer[0], size, &key[0]);
    assert_int_equal (rc, TSS2_RC_SUCCESS);

    rc = iesys_crypto_aes_encrypt(&crypto_cb, &key[0], 0, 256, TPM2_ALG_CFB,
                                      &buffer[0], size, &key[0]);
    assert_int_equal (rc, TSS2_ESYS_RC_BAD_VALUE);

    rc = iesys_crypto_aes_encrypt(&crypto_cb, &key[0], TPM2_ALG_AES, 256, 0,
                                      &buffer[0], size, &key[0]);
    assert_int_equal (rc, TSS2_ESYS_RC_BAD_VALUE);

    rc = iesys_crypto_aes_encrypt(&crypto_cb, &key[0], TPM2_ALG_AES, 999, TPM2_ALG_CFB,
                                      &buffer[0], size, &key[0]);
    assert_int_equal (rc, TSS2_ESYS_RC_BAD_VALUE);

    rc = iesys_crypto_aes_decrypt(&crypto_cb, NULL, TPM2_ALG_AES, 192, TPM2_ALG_CFB,
                                      &buffer[0], size, &key[0]);
    assert_int_equal (rc, TSS2_ESYS_RC_BAD_REFERENCE);

    rc = iesys_crypto_aes_decrypt(&crypto_cb, &key[0], 0, 192, TPM2_ALG_CFB,
                                      &buffer[0], size, &key[0]);
    assert_int_equal (rc, TSS2_ESYS_RC_BAD_VALUE);
}

static void
check_free(void **state)
{
    uint8_t *buffer;

    buffer = malloc(10);
    Esys_Free(buffer);
}

static void
check_get_sys_context(void **state)
{
    ESYS_CONTEXT *ctx;
    TSS2_TCTI_CONTEXT_COMMON_V1 tcti = {0};
    TSS2_SYS_CONTEXT *sys_ctx = NULL;
    TSS2_RC rc;

    rc = Esys_GetSysContext(NULL, NULL);
    assert_int_equal(rc, TSS2_ESYS_RC_BAD_REFERENCE);

    tcti.version = 1;
    tcti.transmit = (void*) 0xdeadbeef;
    tcti.receive = (void*) 0xdeadbeef;

    rc = Esys_Initialize(&ctx, (TSS2_TCTI_CONTEXT *) &tcti, NULL);
    assert_int_equal(rc, TSS2_RC_SUCCESS);

    rc = Esys_GetSysContext(ctx, &sys_ctx);
    assert_ptr_not_equal(sys_ctx, NULL);
    assert_int_equal(rc, TSS2_RC_SUCCESS);

    Esys_Finalize(&ctx);
}

#define CHECK_BACKEND_FN(backend, fn) \
    assert_int_equal(backend.fn, _iesys_crypto_##fn)

static TSS2_RC
    crypto_init(void *userdata)
{
    assert_int_equal(userdata, (void *)0xDEADBEEF);
    return 0x42;
}

static void test_backend_set(void **state) {

    ESYS_CRYPTO_CALLBACKS crypto_cb = { 0 };
    TSS2_RC rc = iesys_initialize_crypto_backend(&crypto_cb, NULL);
    assert_int_equal (rc, TSS2_RC_SUCCESS);

    CHECK_BACKEND_FN(crypto_cb, hash_start);
    CHECK_BACKEND_FN(crypto_cb, hash_update);
    CHECK_BACKEND_FN(crypto_cb, hash_finish);
    CHECK_BACKEND_FN(crypto_cb, hash_abort);

    CHECK_BACKEND_FN(crypto_cb, hmac_start);
    CHECK_BACKEND_FN(crypto_cb, hmac_update);
    CHECK_BACKEND_FN(crypto_cb, hmac_finish);
    CHECK_BACKEND_FN(crypto_cb, hmac_abort);

    CHECK_BACKEND_FN(crypto_cb, aes_decrypt);
    CHECK_BACKEND_FN(crypto_cb, aes_encrypt);
    CHECK_BACKEND_FN(crypto_cb, get_ecdh_point);
    CHECK_BACKEND_FN(crypto_cb, get_random2b);
    CHECK_BACKEND_FN(crypto_cb, rsa_pk_encrypt);

    /* test a user change */
    ESYS_CRYPTO_CALLBACKS user_cb = {
        .aes_decrypt = (void *)0xBADCC0DE,
        .aes_encrypt = (void *)0xBADCC0DE,
        .get_ecdh_point = (void *)0xBADCC0DE,
        .get_random2b = (void *)0xBADCC0DE,
        .rsa_pk_encrypt = (void *)0xBADCC0DE,
        .hash_abort = (void *)0xBADCC0DE,
        .hash_finish = (void *)0xBADCC0DE,
        .hash_start = (void *)0xBADCC0DE,
        .hash_update = (void *)0xBADCC0DE,
        .hmac_abort = (void *)0xBADCC0DE,
        .hmac_finish = (void *)0xBADCC0DE,
        .hmac_start = (void *)0xBADCC0DE,
        .hmac_update = (void *)0xBADCC0DE,
        .init = crypto_init,
        .userdata = (void *)0xDEADBEEF
    };

    rc = iesys_initialize_crypto_backend(&crypto_cb, &user_cb);
    assert_int_equal (rc, 0x42);
    assert_memory_equal(&crypto_cb, &user_cb, sizeof(crypto_cb));

    /* reset state */
    rc = iesys_initialize_crypto_backend(&crypto_cb, NULL);
    assert_int_equal (rc, TSS2_RC_SUCCESS);

    CHECK_BACKEND_FN(crypto_cb, hash_start);
    CHECK_BACKEND_FN(crypto_cb, hash_update);
    CHECK_BACKEND_FN(crypto_cb, hash_finish);
    CHECK_BACKEND_FN(crypto_cb, hash_abort);

    CHECK_BACKEND_FN(crypto_cb, hmac_start);
    CHECK_BACKEND_FN(crypto_cb, hmac_update);
    CHECK_BACKEND_FN(crypto_cb, hmac_finish);
    CHECK_BACKEND_FN(crypto_cb, hmac_abort);

    CHECK_BACKEND_FN(crypto_cb, aes_decrypt);
    CHECK_BACKEND_FN(crypto_cb, aes_encrypt);
    CHECK_BACKEND_FN(crypto_cb, get_ecdh_point);
    CHECK_BACKEND_FN(crypto_cb, get_random2b);
    CHECK_BACKEND_FN(crypto_cb, rsa_pk_encrypt);
}

int
main(int argc, char *argv[])
{
    const struct CMUnitTest tests[] = {
        cmocka_unit_test(check_hash_functions),
        cmocka_unit_test(check_hmac_functions),
        cmocka_unit_test(check_random),
        cmocka_unit_test(check_pk_encrypt),
        cmocka_unit_test(check_aes_encrypt),
        cmocka_unit_test(check_free),
        cmocka_unit_test(check_get_sys_context),
        cmocka_unit_test(test_backend_set)
    };
    return cmocka_run_group_tests(tests, NULL, NULL);
}
