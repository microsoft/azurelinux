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
#include <stdio.h>
#include <json-c/json_util.h>
#include <json-c/json_tokener.h>
#include <openssl/evp.h>

#include <setjmp.h>
#include <cmocka.h>

#include "tss2_fapi.h"
#include "fapi_int.h"
#include "ifapi_get_intl_cert.h"

#include "util/aux_util.h"

#define LOGMODULE tests
#include "util/log.h"

/*
 * The unit tests will simulate error codes which can be returned by the
 * functions which are used to retrieve the INTEL certificates.
 */

/* Mock data for the certificate buffer. and the public data of the EK  */

char* valid_json_cert = "{ \"certificate\": \"ZG15Cg==\" }"; /**< dmy base64 encoded */
char* invalid_json_cert1 = "{ \"certificate\": 1 }";
char* invalid_json_cert2 = "{ }";
char* mock_json_cert;

TPM2B_PUBLIC eccPublic = {
    .size = 0,
    .publicArea = {
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
                .details = {
                    .ecdsa = {.hashAlg  = TPM2_ALG_SHA256}},
            },
            .curveID = TPM2_ECC_NIST_P256,
            .kdf = {
                .scheme = TPM2_ALG_NULL,
                .details = {}}
        },
        .unique.ecc = {
            .x = {.size = 2, .buffer = { 1, 2 }},
            .y = {.size = 2, .buffer = { 3, 4 }},
        },
    },
};

TPM2B_PUBLIC rsaPublic = {
        .size = 0,
        .publicArea = {
            .type = TPM2_ALG_RSA,
            .nameAlg = TPM2_ALG_SHA1,
            .objectAttributes = (TPMA_OBJECT_USERWITHAUTH |
                                 TPMA_OBJECT_SIGN_ENCRYPT  |
                                 TPMA_OBJECT_FIXEDTPM |
                                 TPMA_OBJECT_FIXEDPARENT |
                                 TPMA_OBJECT_SENSITIVEDATAORIGIN),
            .authPolicy = {
                 .size = 0,
             },
            .parameters.rsaDetail = {
                 .symmetric = {
                     .algorithm = TPM2_ALG_NULL,
                     .keyBits.aes = 128,
                     .mode.aes = TPM2_ALG_CFB},
                 .scheme = {
                      .scheme = TPM2_ALG_RSAPSS,
                      .details = {
                          .rsapss = { .hashAlg = TPM2_ALG_SHA1 }
                      }
                  },
                 .keyBits = 2048,
                 .exponent = 0,
             },
            .unique.rsa = {
                 .size = 2,
                 .buffer = { 1, 2 },
             },
        },
    };

/*
 * Wrapper function for reading the certificate buffer.
 */
int
__real_ifapi_get_curl_buffer(unsigned char * url, unsigned char ** buffer,
                             size_t *buffer_size);

int
__wrap_ifapi_get_curl_buffer(unsigned char * url, unsigned char ** buffer,
                          size_t *buffer_size)
{
    UNUSED(url);
    *buffer = (unsigned char *)strdup(mock_json_cert);
    *buffer_size = strlen(mock_json_cert) + 1;
    return 0;
}

/*
 * Wrapper function for updating the hash of EK public data.
 */
size_t wrap_EVP_DigestUpdate_test = 0;

int
__real_EVP_DigestUpdate(EVP_MD_CTX *c, const void *data, size_t len);

int
__wrap_EVP_DigestUpdate(EVP_MD_CTX *c, const void *data, size_t len)
{
    if (!wrap_EVP_DigestUpdate_test) {
        return __real_EVP_DigestUpdate(c, data, len);
    } else if (wrap_EVP_DigestUpdate_test == 1) {
        wrap_EVP_DigestUpdate_test = 0;
        return mock_type(int);
    } else {
        wrap_EVP_DigestUpdate_test--;
        return __real_EVP_DigestUpdate(c, data, len);
    }
}

static int
setup (void **state)
{
    *state = calloc(1, sizeof(FAPI_CONTEXT));  //Fapi_Initialize
    return 0;
}

static int
teardown (void **state)
{
    SAFE_FREE(*state);
    return 0;

}

/*
 * Check receiving of valid JSON data for the certificate.
 */
static void
check_get_intl_cert_ok(void **state) {
    FAPI_CONTEXT *ctx = *state;
    unsigned char *cert_buf = NULL;
    size_t cert_size;
    TSS2_RC r;

    mock_json_cert = valid_json_cert;
    r = ifapi_get_intl_ek_certificate(ctx, &eccPublic, &cert_buf, &cert_size);
    assert_int_equal(r, TSS2_RC_SUCCESS);
    SAFE_FREE(cert_buf);

    r = ifapi_get_intl_ek_certificate(ctx, &rsaPublic, &cert_buf, &cert_size);
    SAFE_FREE(cert_buf);
    assert_int_equal(r, TSS2_RC_SUCCESS);
}

/*
 * Check receiving of invalid JSON data for the certificate.
 */
static void
check_get_intl_cert_invalid_json(void **state) {
    FAPI_CONTEXT *ctx = *state;
    unsigned char *cert_buf = NULL;
    size_t cert_size;
    TSS2_RC r;
    mock_json_cert = invalid_json_cert1;
    r = ifapi_get_intl_ek_certificate(ctx, &eccPublic, &cert_buf, &cert_size);
    assert_int_equal(r, TSS2_FAPI_RC_NO_CERT);

    mock_json_cert = invalid_json_cert2;
    r = ifapi_get_intl_ek_certificate(ctx, &rsaPublic, &cert_buf, &cert_size);
    assert_int_equal(r, TSS2_FAPI_RC_NO_CERT);
}

/*
 * Simulate error during hash update for the EK public data.
 */
static void
check_get_intl_cert_sha_error(void **state) {
    FAPI_CONTEXT *ctx = *state;
    unsigned char *cert_buf = NULL;
    size_t cert_size;
    TSS2_RC r;
    will_return_always(__wrap_EVP_DigestUpdate, 0);
    mock_json_cert = valid_json_cert;
    wrap_EVP_DigestUpdate_test = 1;
    r = ifapi_get_intl_ek_certificate(ctx, &eccPublic, &cert_buf, &cert_size);
    assert_int_equal(r,TSS2_FAPI_RC_NO_CERT);

    wrap_EVP_DigestUpdate_test = 1;
    r = ifapi_get_intl_ek_certificate(ctx, &rsaPublic, &cert_buf, &cert_size);
    assert_int_equal(r,TSS2_FAPI_RC_NO_CERT);

    wrap_EVP_DigestUpdate_test = 2;
    r = ifapi_get_intl_ek_certificate(ctx, &eccPublic, &cert_buf, &cert_size);
    assert_int_equal(r,TSS2_FAPI_RC_NO_CERT);

    wrap_EVP_DigestUpdate_test = 2;
    r = ifapi_get_intl_ek_certificate(ctx, &rsaPublic, &cert_buf, &cert_size);
    assert_int_equal(r,TSS2_FAPI_RC_NO_CERT);

}

int
main(int argc, char *argv[])
{
    const struct CMUnitTest tests[] = {
        cmocka_unit_test_setup_teardown(check_get_intl_cert_ok, setup, teardown),
        cmocka_unit_test_setup_teardown(check_get_intl_cert_invalid_json, setup, teardown),
        cmocka_unit_test_setup_teardown(check_get_intl_cert_sha_error, setup, teardown),
    };
    return cmocka_run_group_tests(tests, NULL, NULL);
}
