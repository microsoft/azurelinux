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

#include <setjmp.h>
#include <cmocka.h>

#include "tss2_fapi.h"
#include "tpm_json_serialize.h"
#include "ifapi_eventlog.h"
#include "tpm_json_deserialize.h"
#include "ifapi_json_serialize.h"
#include "ifapi_json_deserialize.h"
#include "ifapi_helpers.h"
#include "fapi_crypto.h"

#include "util/aux_util.h"

#define LOGMODULE tests
#include "util/log.h"

/*
 * The unit tests will be used to test cases of the FAPI helper
 * functions which were not covered by the integration tests.
 */

/* Global variables to trigger wrapper functions. If set to false the
 * real function will be called. */
bool wrap_activate_crypto_hash_update = false;
bool wrap_activate_crypto_hash_finish = false;


/*
 * Wrappers for crypto functions.
 */
TSS2_RC
__real_ifapi_crypto_hash_update(IFAPI_CRYPTO_CONTEXT_BLOB *context,
                                const uint8_t *buffer, size_t size, ...);

TSS2_RC
__wrap_ifapi_crypto_hash_update(IFAPI_CRYPTO_CONTEXT_BLOB *context,
                                const uint8_t *buffer, size_t size, ...)
{
    if (wrap_activate_crypto_hash_update)
        return mock_type(int);
    else
        return __real_ifapi_crypto_hash_update(context, buffer, size);
}

TSS2_RC
__real_ifapi_crypto_hash_finish(IFAPI_CRYPTO_CONTEXT_BLOB **context,
                                const uint8_t *digest, size_t size, ...);

TSS2_RC
__wrap_ifapi_crypto_hash_finish(IFAPI_CRYPTO_CONTEXT_BLOB **context,
                                const uint8_t *digest, size_t size, ...)
{
    if (wrap_activate_crypto_hash_finish)
        return mock_type(int);
    else
        return __real_ifapi_crypto_hash_finish(context, digest, size);
}

/*
 * Check all cases to determine the first index of an NV path.
 */
static void
check_get_nv_start_index2(char *path, TPM2_HANDLE exp_start_idx, TSS2_RC exp_r)
{
    TSS2_RC r;
    TPM2_HANDLE nv_index;

    r = ifapi_get_nv_start_index(path, &nv_index);
    assert_int_equal(r, exp_r);
    if (r == TPM2_RC_SUCCESS) {
        assert_int_equal(nv_index, exp_start_idx);
    }
}

static void
check_get_nv_start_index(void **state)
{
    check_get_nv_start_index2("/nv/wrong_path", 0, TSS2_FAPI_RC_BAD_PATH);
    check_get_nv_start_index2("/nv/TPM", 0x01000000, TSS2_RC_SUCCESS);
    check_get_nv_start_index2("/nv/Owner", 0x01800000, TSS2_RC_SUCCESS);
    check_get_nv_start_index2("/nv/Endorsement_Certificate", 0x01c00000, TSS2_RC_SUCCESS);
    check_get_nv_start_index2("/nv/Platform_Certificate", 0x01c08000, TSS2_RC_SUCCESS);
    check_get_nv_start_index2("/nv/Component_OEM", 0x01c10000, TSS2_RC_SUCCESS);
    check_get_nv_start_index2("/nv/TPM_OEM", 0x01c20000, TSS2_RC_SUCCESS);
    check_get_nv_start_index2("/nv/Platform_OEM", 0x01c30000, TSS2_RC_SUCCESS);
    check_get_nv_start_index2("/nv/PC-Client", 0x01c40000, TSS2_RC_SUCCESS);
    check_get_nv_start_index2("/nv/Server", 0x01c50000, TSS2_RC_SUCCESS);
    check_get_nv_start_index2("/nv/Virtualized_Platform", 0x01c60000, TSS2_RC_SUCCESS);
    check_get_nv_start_index2("/nv/MPWG", 0x01c70000, TSS2_RC_SUCCESS);
    check_get_nv_start_index2("/nv/Embedded", 0x01c80000, TSS2_RC_SUCCESS);
}

/*
 * Test all cases which check whether a given NV index is valid for a certain path.
 */
static void
check_check_nv_index2(char *path, TPM2_HANDLE nv_index, TSS2_RC exp_r)
{
    TSS2_RC r;

    r = ifapi_check_nv_index(path, nv_index);
    assert_int_equal(r, exp_r);
}

static void
check_check_nv_index(void **state)
{
    check_check_nv_index2("/nv/TPM", 0x01000000, TSS2_RC_SUCCESS);
    check_check_nv_index2("/nv/TPM", 0x013fffff, TSS2_RC_SUCCESS);
    check_check_nv_index2("/nv/TPM", 0xffffff, TSS2_FAPI_RC_BAD_VALUE);
    check_check_nv_index2("/nv/TPM", 0x1400000, TSS2_FAPI_RC_BAD_VALUE);
    check_check_nv_index2("/nv/Platform", 0x01400000, TSS2_RC_SUCCESS);
    check_check_nv_index2("/nv/Platform", 0x017fffff, TSS2_RC_SUCCESS);
    check_check_nv_index2("/nv/Platform", 0x13fffff, TSS2_FAPI_RC_BAD_VALUE);
    check_check_nv_index2("/nv/Platform", 0x1800000, TSS2_FAPI_RC_BAD_VALUE);
    check_check_nv_index2("/nv/Owner", 0x01800000, TSS2_RC_SUCCESS);
    check_check_nv_index2("/nv/Owner", 0x01bfffff, TSS2_RC_SUCCESS);
    check_check_nv_index2("/nv/Owner", 0x17fffff, TSS2_FAPI_RC_BAD_VALUE);
    check_check_nv_index2("/nv/Owner", 0x1c00000, TSS2_FAPI_RC_BAD_VALUE);
    check_check_nv_index2("/nv/Endorsement_Certificate", 0x01c00000, TSS2_RC_SUCCESS);
    check_check_nv_index2("/nv/Endorsement_Certificate", 0x01c07fff, TSS2_RC_SUCCESS);
    check_check_nv_index2("/nv/Endorsement_Certificate", 0x1bfffff, TSS2_FAPI_RC_BAD_VALUE);
    check_check_nv_index2("/nv/Endorsement_Certificate", 0x1c08000, TSS2_FAPI_RC_BAD_VALUE);
    check_check_nv_index2("/nv/Platform_Certificate", 0x01c08000, TSS2_RC_SUCCESS);
    check_check_nv_index2("/nv/Platform_Certificate", 0x01c0ffff, TSS2_RC_SUCCESS);
    check_check_nv_index2("/nv/Platform_Certificate", 0x1c07fff, TSS2_FAPI_RC_BAD_VALUE);
    check_check_nv_index2("/nv/Platform_Certificate", 0x1c10000, TSS2_FAPI_RC_BAD_VALUE);
    check_check_nv_index2("/nv/Component_OEM", 0x01c10000, TSS2_RC_SUCCESS);
    check_check_nv_index2("/nv/Component_OEM", 0x01c1ffff, TSS2_RC_SUCCESS);
    check_check_nv_index2("/nv/Component_OEM", 0x1c0ffff, TSS2_FAPI_RC_BAD_VALUE);
    check_check_nv_index2("/nv/Component_OEM", 0x1c20000, TSS2_FAPI_RC_BAD_VALUE);
    check_check_nv_index2("/nv/TPM_OEM", 0x01c20000, TSS2_RC_SUCCESS);
    check_check_nv_index2("/nv/TPM_OEM", 0x01c2ffff, TSS2_RC_SUCCESS);
    check_check_nv_index2("/nv/TPM_OEM", 0x1c1ffff, TSS2_FAPI_RC_BAD_VALUE);
    check_check_nv_index2("/nv/TPM_OEM", 0x1c30000, TSS2_FAPI_RC_BAD_VALUE);
    check_check_nv_index2("/nv/Platform_OEM", 0x01c30000, TSS2_RC_SUCCESS);
    check_check_nv_index2("/nv/Platform_OEM", 0x01c3ffff, TSS2_RC_SUCCESS);
    check_check_nv_index2("/nv/Platform_OEM", 0x1c2ffff, TSS2_FAPI_RC_BAD_VALUE);
    check_check_nv_index2("/nv/Platform_OEM", 0x1c40000, TSS2_FAPI_RC_BAD_VALUE);
    check_check_nv_index2("/nv/PC-Client", 0x01c40000, TSS2_RC_SUCCESS);
    check_check_nv_index2("/nv/PC-Client", 0x01c4ffff, TSS2_RC_SUCCESS);
    check_check_nv_index2("/nv/PC-Client", 0x1c3ffff, TSS2_FAPI_RC_BAD_VALUE);
    check_check_nv_index2("/nv/PC-Client", 0x1c50000, TSS2_FAPI_RC_BAD_VALUE);
    check_check_nv_index2("/nv/Server", 0x01c50000, TSS2_RC_SUCCESS);
    check_check_nv_index2("/nv/Server", 0x01c5ffff, TSS2_RC_SUCCESS);
    check_check_nv_index2("/nv/Server", 0x1c4ffff, TSS2_FAPI_RC_BAD_VALUE);
    check_check_nv_index2("/nv/Server", 0x1c60000, TSS2_FAPI_RC_BAD_VALUE);
    check_check_nv_index2("/nv/Virtualized_Platform", 0x01c60000, TSS2_RC_SUCCESS);
    check_check_nv_index2("/nv/Virtualized_Platform", 0x01c6ffff, TSS2_RC_SUCCESS);
    check_check_nv_index2("/nv/Virtualized_Platform", 0x1c5ffff, TSS2_FAPI_RC_BAD_VALUE);
    check_check_nv_index2("/nv/Virtualized_Platform", 0x1c70000, TSS2_FAPI_RC_BAD_VALUE);
    check_check_nv_index2("/nv/MPWG", 0x01c70000, TSS2_RC_SUCCESS);
    check_check_nv_index2("/nv/MPWG", 0x01c7ffff, TSS2_RC_SUCCESS);
    check_check_nv_index2("/nv/MPWG", 0x1c6ffff, TSS2_FAPI_RC_BAD_VALUE);
    check_check_nv_index2("/nv/MPWG", 0x1c80000, TSS2_FAPI_RC_BAD_VALUE);
    check_check_nv_index2("/nv/Embedded", 0x01c80000, TSS2_RC_SUCCESS);
    check_check_nv_index2("/nv/Embedded", 0x01c8ffff, TSS2_RC_SUCCESS);
    check_check_nv_index2("/nv/Embedded", 0x1c7ffff, TSS2_FAPI_RC_BAD_VALUE);
    check_check_nv_index2("/nv/Embedded", 0x1c90000, TSS2_FAPI_RC_BAD_VALUE);
}

/*
 * Check comparison of TPMU_PUBLIC_ID structures with the selectors
 * TPM2_ALG_KEYEDHASH and TPM2_ALG_SYMCIPHER.
 */
static void
check_cmp_TPMU_PUBLIC_ID2(
    TPMT_PUBLIC *pid1,
    TPMT_PUBLIC *pid2,
    bool exp_r)
{
    bool r;
    r = ifapi_TPMT_PUBLIC_cmp(pid1, pid2);
    if (exp_r)
        assert_true(r);
    else
        assert_false(r);
}

static void
check_cmp_TPMU_PUBLIC_ID(void **state) {
    TPM2B_DIGEST digest1 = {
        .size = 10,
        .buffer = { 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 }
    };
    TPM2B_DIGEST digest2 = {
        .size = 10,
        .buffer = { 10, 11, 12, 13, 14, 15, 16, 17, 18, 19 }
    };
    TPMT_PUBLIC keyed_hash1;
    TPMT_PUBLIC sym1;
    TPMT_PUBLIC keyed_hash2;
    TPMT_PUBLIC sym2;

    keyed_hash1.type = TPM2_ALG_KEYEDHASH;
    keyed_hash1.unique.keyedHash = digest1;
    sym1.type = TPM2_ALG_SYMCIPHER;
    sym1.unique.sym = digest1;
    keyed_hash2.type = TPM2_ALG_KEYEDHASH;
    keyed_hash2.unique.keyedHash = digest2;
    sym2.type = TPM2_ALG_SYMCIPHER;
    sym2.unique.sym = digest2;

    check_cmp_TPMU_PUBLIC_ID2(&keyed_hash1, &sym1, false);
    check_cmp_TPMU_PUBLIC_ID2(&keyed_hash1, &keyed_hash1, true);
    check_cmp_TPMU_PUBLIC_ID2(&keyed_hash1, &keyed_hash2, false);
    check_cmp_TPMU_PUBLIC_ID2(&sym1, &sym1, true);
    check_cmp_TPMU_PUBLIC_ID2(&sym1, &sym2, false);
}

TPMT_PUBLIC in_public = {
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
            .details = {.ecdsa =
                        {.hashAlg = TPM2_ALG_SHA1}
            }
        },
        .curveID = TPM2_ECC_NIST_P256,
        .kdf = {.scheme =
                TPM2_ALG_NULL,.details = {}
        }
    },
    .unique.ecc = {
        .x = {.size = 0,.buffer = {}},
        .y = {.size = 0,.buffer = {}}
    },
};

/*
 * Check error cases of the function ifapi_get_name.
 */
static void
check_get_name(void **state) {
    TPMT_PUBLIC public = { 0 };
    TPM2B_NAME name;
    TSS2_RC r;

    public.nameAlg = TPM2_ALG_SHA256;
    public.authPolicy.size = 0xFFFF;
    r = ifapi_get_name(&public, &name);
    assert_int_equal(r, TSS2_MU_RC_INSUFFICIENT_BUFFER);

    wrap_activate_crypto_hash_update = true;
    will_return(__wrap_ifapi_crypto_hash_update, TSS2_FAPI_RC_GENERAL_FAILURE);

     r = ifapi_get_name(&in_public, &name);
    assert_int_equal(r, TSS2_FAPI_RC_GENERAL_FAILURE);
    wrap_activate_crypto_hash_update = false;

    wrap_activate_crypto_hash_finish = true;
    will_return(__wrap_ifapi_crypto_hash_finish, TSS2_FAPI_RC_GENERAL_FAILURE);

    r = ifapi_get_name(&in_public, &name);
    assert_int_equal(r, TSS2_FAPI_RC_GENERAL_FAILURE);
    wrap_activate_crypto_hash_finish = false;
}

/*
 * Check valid return and out parameters of the function
 * ifapi_get_profile_sig_scheme.
 */
static void
check_get_profile_sig_scheme(void **stat) {
    IFAPI_PROFILE profile;
    TPMT_SIG_SCHEME sig_scheme;
    TPMT_PUBLIC tpm_public;
    TSS2_RC r;
    TPMT_SIG_SCHEME ecc_scheme = { .scheme = TPM2_ALG_ECDSA,
                                   .details.ecdsa = TPM2_ALG_SHA1 };
    TPMT_SIG_SCHEME rsa_scheme = { .scheme = TPM2_ALG_RSAPSS,
                                   .details.rsapss = TPM2_ALG_SHA1 };
    TPMI_ALG_HASH hash_alg;

    profile.rsa_signing_scheme = rsa_scheme;
    profile.ecc_signing_scheme = ecc_scheme;

    tpm_public.type = TPM2_ALG_RSA;
    r = ifapi_get_profile_sig_scheme(&profile, &tpm_public, &sig_scheme);
    assert_int_equal(r, TSS2_RC_SUCCESS);
    assert_true(sig_scheme.scheme == TPM2_ALG_RSAPSS);
    hash_alg = sig_scheme.details.rsapss.hashAlg;
    assert_true(hash_alg== TPM2_ALG_SHA1);

    tpm_public.type = TPM2_ALG_ECC;
    r = ifapi_get_profile_sig_scheme(&profile, &tpm_public, &sig_scheme);
    assert_int_equal(r, TSS2_RC_SUCCESS);
    assert_true(sig_scheme.scheme == TPM2_ALG_ECDSA);
    hash_alg = sig_scheme.details.ecdsa.hashAlg;
    assert_true(hash_alg== TPM2_ALG_SHA1);

    tpm_public.type = TPM2_ALG_NULL;
    r = ifapi_get_profile_sig_scheme(&profile, &tpm_public, &sig_scheme);
    assert_int_equal(r, TSS2_FAPI_RC_BAD_VALUE);
}

int
main(int argc, char *argv[])
{
    const struct CMUnitTest tests[] = {
        cmocka_unit_test(check_get_nv_start_index),
        cmocka_unit_test(check_check_nv_index),
        cmocka_unit_test(check_cmp_TPMU_PUBLIC_ID),
        cmocka_unit_test(check_get_name),
        cmocka_unit_test(check_get_profile_sig_scheme),
    };
    return cmocka_run_group_tests(tests, NULL, NULL);
}
