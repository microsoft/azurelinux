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
#include "esys_int.h"

#include "esys_iutil.h"
#define LOGMODULE test
#include "util/log.h"
#include "util/aux_util.h"

#define TEST_FN_PTR ((void *)0xBADC0DE)

#define CHECK_BACKEND_FN_NOT_TEST(backend, fn) \
    if (backend.fn == TEST_FN_PTR) { \
        LOG_ERROR("Expected function \"%s\" not to be test ptr", xstr(fn)); \
        return EXIT_FAILURE; \
    }

/** This test is intended to test the ESYS command  Esys_SetCryptoCallbacks.
 *
 * The test checks whether callbacks are set as expected.
 *
 * Tested ESYS commands:
 *  - Esys_Hash() (M)
 *
 * @retval EXIT_FAILURE
 * @retval EXIT_SUCCESS
 */

static int init_called = 0;
static TSS2_RC
    init(void *userdata)
{
    init_called = 1;
    return (void *)0xDEADBEEF ? TSS2_RC_SUCCESS : TSS2_ESYS_RC_BAD_VALUE;
}

int
test_invoke_esys(ESYS_CONTEXT *esys_context)
{
    /*peer into the internals, state should be as expected in esys context */
    CHECK_BACKEND_FN_NOT_TEST(esys_context->crypto_backend, hash_start);
    CHECK_BACKEND_FN_NOT_TEST(esys_context->crypto_backend, hash_update);
    CHECK_BACKEND_FN_NOT_TEST(esys_context->crypto_backend, hash_finish);
    CHECK_BACKEND_FN_NOT_TEST(esys_context->crypto_backend, hash_abort);

    CHECK_BACKEND_FN_NOT_TEST(esys_context->crypto_backend, hmac_start);
    CHECK_BACKEND_FN_NOT_TEST(esys_context->crypto_backend, hmac_update);
    CHECK_BACKEND_FN_NOT_TEST(esys_context->crypto_backend, hmac_finish);
    CHECK_BACKEND_FN_NOT_TEST(esys_context->crypto_backend, hmac_abort);

    CHECK_BACKEND_FN_NOT_TEST(esys_context->crypto_backend, aes_decrypt);
    CHECK_BACKEND_FN_NOT_TEST(esys_context->crypto_backend, aes_encrypt);
    CHECK_BACKEND_FN_NOT_TEST(esys_context->crypto_backend, get_ecdh_point);
    CHECK_BACKEND_FN_NOT_TEST(esys_context->crypto_backend, get_random2b);
    CHECK_BACKEND_FN_NOT_TEST(esys_context->crypto_backend, rsa_pk_encrypt);

    ESYS_CRYPTO_CALLBACKS callbacks = {
        .aes_decrypt = TEST_FN_PTR,
        .aes_encrypt = TEST_FN_PTR,
        .get_ecdh_point = TEST_FN_PTR,
        .get_random2b = TEST_FN_PTR,
        .rsa_pk_encrypt = TEST_FN_PTR,
        .hash_abort = TEST_FN_PTR,
        .hash_finish = TEST_FN_PTR,
        .hash_start = TEST_FN_PTR,
        .hash_update = TEST_FN_PTR,
        .hmac_abort = TEST_FN_PTR,
        .hmac_finish = TEST_FN_PTR,
        .hmac_start = TEST_FN_PTR,
        .hmac_update = TEST_FN_PTR,
        .init = init,
        .userdata = (void *)0xDEADBEEF
    };

    TSS2_RC r = Esys_SetCryptoCallbacks(
            esys_context,
            &callbacks);
    if (r != TSS2_RC_SUCCESS) {
        LOG_ERROR("Esys_SetCryptoCallbacks failed: 0x%x", r);
        return EXIT_FAILURE;
    }

    if (!init_called) {
        LOG_ERROR("user callback for init not invoked");
        return EXIT_FAILURE;
    }

    /* peer back into internals and ensure state is correct */
    if (memcmp(&esys_context->crypto_backend, &callbacks, sizeof(callbacks))) {
        LOG_ERROR("ESYS_CONTEXT state for user callbacks not as expected");
        return EXIT_FAILURE;
    }

    /* reset state */
    r = Esys_SetCryptoCallbacks(
            esys_context,
            NULL);
    if (r != TSS2_RC_SUCCESS) {
        LOG_ERROR("Esys_SetCryptoCallbacks failed: 0x%x", r);
        return EXIT_FAILURE;
    }

    CHECK_BACKEND_FN_NOT_TEST(esys_context->crypto_backend, hash_start);
    CHECK_BACKEND_FN_NOT_TEST(esys_context->crypto_backend, hash_update);
    CHECK_BACKEND_FN_NOT_TEST(esys_context->crypto_backend, hash_finish);
    CHECK_BACKEND_FN_NOT_TEST(esys_context->crypto_backend, hash_abort);

    CHECK_BACKEND_FN_NOT_TEST(esys_context->crypto_backend, hmac_start);
    CHECK_BACKEND_FN_NOT_TEST(esys_context->crypto_backend, hmac_update);
    CHECK_BACKEND_FN_NOT_TEST(esys_context->crypto_backend, hmac_finish);
    CHECK_BACKEND_FN_NOT_TEST(esys_context->crypto_backend, hmac_abort);

    CHECK_BACKEND_FN_NOT_TEST(esys_context->crypto_backend, aes_decrypt);
    CHECK_BACKEND_FN_NOT_TEST(esys_context->crypto_backend, aes_encrypt);
    CHECK_BACKEND_FN_NOT_TEST(esys_context->crypto_backend, get_ecdh_point);
    CHECK_BACKEND_FN_NOT_TEST(esys_context->crypto_backend, get_random2b);
    CHECK_BACKEND_FN_NOT_TEST(esys_context->crypto_backend, rsa_pk_encrypt);

    return EXIT_SUCCESS;
}
