/* SPDX-License-Identifier: BSD-2-Clause */
#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <stdbool.h>
#include <stdlib.h>
#include <stdio.h>
#include <inttypes.h>
#include <openssl/evp.h>
#include <openssl/pem.h>
#include <openssl/err.h>
#if OPENSSL_VERSION_NUMBER < 0x30000000
#include <openssl/ec.h>
#else
#include <openssl/core_names.h>
#include <openssl/params.h>
#include <openssl/param_build.h>
#endif
#include <string.h>

#include "tss2_sys.h"
#include "tss2_mu.h"

#define LOGMODULE test
#include "util/log.h"
#include "test-options.h"
#include "context-util.h"

void handleErrors(void)
{
    unsigned long errCode;

    printf("An error occurred\n");
    while((errCode = ERR_get_error()))
    {
        char *err = ERR_error_string(errCode, NULL);
        printf("%s\n", err);
    }
    abort();
}

int
main (int argc, char *argv[])
{
    TSS2_RC rc;
    TSS2_SYS_CONTEXT *sys_context;
    TSS2L_SYS_AUTH_COMMAND auth_cmd = {
        .auths = {{ .sessionHandle = TPM2_RH_PW }},
        .count = 1
    };
    TPM2B_SENSITIVE_CREATE in_sensitive = { 0 };
    TPM2B_PUBLIC in_public = {
        .publicArea = {
            .type = TPM2_ALG_ECC,
            .nameAlg = TPM2_ALG_SHA256,
            .objectAttributes = (
                                 TPMA_OBJECT_FIXEDTPM |
                                 TPMA_OBJECT_FIXEDPARENT |
                                 TPMA_OBJECT_SENSITIVEDATAORIGIN |
                                 TPMA_OBJECT_ADMINWITHPOLICY |
                                 TPMA_OBJECT_RESTRICTED |
                                 TPMA_OBJECT_DECRYPT
                                 ),
            .authPolicy = {
                .size = 32,
                .buffer = 0x83, 0x71, 0x97, 0x67, 0x44, 0x84,
                0xB3, 0xF8, 0x1A, 0x90, 0xCC, 0x8D,
                0x46, 0xA5, 0xD7, 0x24, 0xFD, 0x52,
                0xD7, 0x6E, 0x06, 0x52, 0x0B, 0x64,
                0xF2, 0xA1, 0xDA, 0x1B, 0x33, 0x14,
                0x69, 0xAA,
            },
            .parameters.eccDetail = {
                .symmetric = {
                    .algorithm = TPM2_ALG_AES,
                    .keyBits.aes = 128,
                    .mode.aes = TPM2_ALG_CFB,
                },
                .scheme = {
                    .scheme = TPM2_ALG_NULL,
                    .details = { 0 }
                },
                .curveID = TPM2_ECC_NIST_P256,
                .kdf = {.scheme = TPM2_ALG_NULL,
                        .details = { 0 }
                }
            },
            .unique.ecc = {
                .x = {.size = 32,.buffer = { 0 }},
                .y = {.size = 32,.buffer = { 0 }}
            }
        }
    };
    TPML_PCR_SELECTION creation_pcr = { 0 };
    TPM2_HANDLE handle;
    TPM2B_PUBLIC out_public = { 0 };
    TSS2L_SYS_AUTH_RESPONSE auth_rsp = {
        .count = 0
    };

    test_opts_t opts = {
        .tcti_type      = TCTI_DEFAULT,
        .device_file    = DEVICE_PATH_DEFAULT,
        .socket_address = HOSTNAME_DEFAULT,
        .socket_port    = PORT_DEFAULT,
    };

    get_test_opts_from_env (&opts);
    if (sanity_check_test_opts (&opts) != 0)
        exit (1);

    sys_context = sys_init_from_opts (&opts);
    if (sys_context == NULL)
        exit (1);

    /* Generate the EK key */

    rc = Tss2_Sys_CreatePrimary(sys_context, TPM2_RH_ENDORSEMENT, &auth_cmd,
                                &in_sensitive, &in_public, NULL, &creation_pcr,
                                &handle, &out_public, NULL, NULL, NULL, NULL, &auth_rsp);
    if (rc != TSS2_RC_SUCCESS) {
        LOG_ERROR("TPM CreatePrimary FAILED: 0x%"PRIx32, rc);
        exit(1);
    }

    rc = Tss2_Sys_FlushContext(sys_context, handle);
    if (rc != TSS2_RC_SUCCESS) {
        LOG_ERROR("TPM FlushContext FAILED: 0x%"PRIx32, rc);
        exit(1);
    }

    sys_teardown_full (sys_context);

    /* Convert the key from out_public to PEM */

    EVP_PKEY *evp = NULL;
    BIGNUM *x = NULL, *y = NULL;
    BIO *bio;
    FILE *out = NULL;
    int nid;

    if (argc == 2) {
        out = fopen(argv[1], "w");
        if (!out) {
            LOG_ERROR("Can not open file %s", argv[1]);
            exit(1);
        }
        bio = BIO_new_fp(out, BIO_NOCLOSE);
    }
    else
        bio = BIO_new_fp(stdout, BIO_NOCLOSE);

    nid = EC_curve_nist2nid("P-256");
    EC_GROUP *ecgroup = EC_GROUP_new_by_curve_name(nid);

    /* Set the ECC parameters in the OpenSSL key */
    x = BN_bin2bn(out_public.publicArea.unique.ecc.x.buffer,
                  out_public.publicArea.unique.ecc.x.size, NULL);

    y = BN_bin2bn(out_public.publicArea.unique.ecc.y.buffer,
                  out_public.publicArea.unique.ecc.y.size, NULL);

    if (!x || !y) {
        exit(1);
    }

    EC_POINT *point = EC_POINT_new(ecgroup);
#if OPENSSL_VERSION_NUMBER < 0x10101000L
    EC_POINT_set_affine_coordinates_GFp(ecgroup, point, x, y, NULL);
#else
    EC_POINT_set_affine_coordinates(ecgroup, point, x, y, NULL);
#endif

#if OPENSSL_VERSION_NUMBER < 0x30000000
    EC_KEY *ecc_key = EC_KEY_new();
    if (!EC_KEY_set_group(ecc_key, ecgroup))
        exit(1);

    if (!EC_KEY_set_public_key(ecc_key, point)) {
        exit(1);
    }

    evp = EVP_PKEY_new();
    if (!EVP_PKEY_assign_EC_KEY(evp, ecc_key)) {
        handleErrors();
        LOG_ERROR("PEM_write failed");
        exit(1);
    }
#else /* OPENSSL_VERSION_NUMBER < 0x30000000 */
    unsigned char *puboct = NULL;
    size_t bsize;

    bsize = EC_POINT_point2buf(ecgroup, point, POINT_CONVERSION_UNCOMPRESSED,
                               &puboct, NULL);

    OSSL_PARAM_BLD *build = OSSL_PARAM_BLD_new();
    OSSL_PARAM_BLD_push_utf8_string(build, OSSL_PKEY_PARAM_GROUP_NAME,
                                    (char *)OBJ_nid2sn(nid), 0);
    OSSL_PARAM_BLD_push_octet_string(build, OSSL_PKEY_PARAM_PUB_KEY,
                                     puboct, bsize);
    OSSL_PARAM *params = OSSL_PARAM_BLD_to_param(build);

    EVP_PKEY_CTX *ctx = EVP_PKEY_CTX_new_from_name(NULL, "EC", NULL);
    EVP_PKEY_fromdata_init(ctx);
    EVP_PKEY_fromdata(ctx, &evp, EVP_PKEY_PUBLIC_KEY, params);
#endif /* OPENSSL_VERSION_NUMBER < 0x30000000 */

    if (!PEM_write_bio_PUBKEY(bio, evp)) {
        handleErrors();
        LOG_ERROR("PEM_write failed");
        exit(1);
    }

    EVP_PKEY_free(evp);
#if OPENSSL_VERSION_NUMBER < 0x30000000
    /* ownership was taken by the EVP_PKEY */
#else
    EVP_PKEY_CTX_free(ctx);
    OSSL_PARAM_free(params);
    OSSL_PARAM_BLD_free(build);
    OPENSSL_free(puboct);
#endif
    EC_POINT_free(point);
    EC_GROUP_free(ecgroup);
    BN_free(y);
    BN_free(x);
    BIO_free(bio);
    fclose(out);

    return 0;
}
