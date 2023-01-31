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
#include "tpm_json_deserialize.h"
#include "ifapi_json_serialize.h"
#include "ifapi_json_deserialize.h"
#include "fapi_policy.h"
#include "ifapi_helpers.h"

#include "util/aux_util.h"

#define LOGMODULE tests
#include "util/log.h"

/* 6 copies of cleanup functions from ifapi_keystore.c */

void
cleanup_ifapi_duplicate(IFAPI_DUPLICATE * duplicate) {
    if (duplicate != NULL) {
        SAFE_FREE(duplicate->certificate);
    }
}

void
cleanup_ifapi_hierarchy(IFAPI_HIERARCHY * hierarchy) {
    if (hierarchy != NULL) {
        SAFE_FREE(hierarchy->description);
    }
}

void
cleanup_ifapi_ext_pub_key(IFAPI_EXT_PUB_KEY * key) {
    if (key != NULL) {
        SAFE_FREE(key->pem_ext_public);
        SAFE_FREE(key->certificate);
    }
}

void
cleanup_ifapi_key(IFAPI_KEY * key) {
    if (key != NULL) {
        SAFE_FREE(key->policyInstance);
        SAFE_FREE(key->serialization.buffer);
        SAFE_FREE(key->private.buffer);
        SAFE_FREE(key->description);
        SAFE_FREE(key->certificate);
        SAFE_FREE(key->appData.buffer);
    }
}

void
cleanup_ifapi_nv(IFAPI_NV * nv) {
    if (nv != NULL) {
        SAFE_FREE(nv->serialization.buffer);
        SAFE_FREE(nv->appData.buffer);
        SAFE_FREE(nv->policyInstance);
        SAFE_FREE(nv->description);
        SAFE_FREE(nv->event_log);
    }
}

void
cleanup_ifapi_object(
    IFAPI_OBJECT * object)
{
    if (object != NULL) {
        if (object->objectType != IFAPI_OBJ_NONE) {
            if (object->objectType == IFAPI_KEY_OBJ) {
                cleanup_ifapi_key(&object->misc.key);
            } else if (object->objectType == IFAPI_NV_OBJ) {
                cleanup_ifapi_nv(&object->misc.nv);
            } else if (object->objectType == IFAPI_DUPLICATE_OBJ) {
                cleanup_ifapi_duplicate(&object->misc.key_tree);
            } else if (object->objectType == IFAPI_EXT_PUB_KEY_OBJ) {
                cleanup_ifapi_ext_pub_key(&object->misc.ext_pub_key);
            } else if (object->objectType == IFAPI_HIERARCHY_OBJ) {
                cleanup_ifapi_hierarchy(&object->misc.hierarchy);
            }

            ifapi_cleanup_policy(object->policy);
            SAFE_FREE(object->rel_path);
            SAFE_FREE(object->policy);
            object->objectType = IFAPI_OBJ_NONE;
        }
    }
}

char * normalize(const char *string) {
    char *string2 = malloc(strlen(string)+1);
    int i;
    int j = 0;
    for(i = 0; string[i] != '\0'; i++) {
        if ((string[i] != '\n' && string[i] != ' ')) {
            string2[j] = string[i];
            j += 1;
        }
    }
    string2[j] = '\0';
	return string2;
}

#define CHECK_ERROR(TYPE, SRC, RC) \
        { \
            TYPE out; \
            TSS2_RC rc; \
            json_object *jso = json_tokener_parse((SRC)); \
            assert_non_null(jso); \
            rc = ifapi_json_ ## TYPE ## _deserialize (jso, &out); \
            assert_int_equal (rc, RC); \
            json_object_put(jso); \
        }

#define CHECK_ERROR_CLEANUP(TYPE, SRC, RC)     \
        { \
            TYPE out; \
            TSS2_RC rc; \
            json_object *jso = json_tokener_parse((SRC)); \
            memset(&out, 0, sizeof(TYPE));                \
            assert_non_null(jso); \
            rc = ifapi_json_ ## TYPE ## _deserialize (jso, &out); \
            assert_int_equal (rc, RC); \
            json_object_put(jso); \
            cleanup_ifapi_object(&out); \
        }



#define CHECK_JSON2(TYPE, SRC, DST, PSERIALIZE)  \
        { \
            TYPE out; \
            TSS2_RC rc; \
            json_object *jso = json_tokener_parse((SRC)); \
            if (!jso) fprintf(stderr, "JSON parsing failed\n"); \
            assert_non_null(jso); \
            rc = ifapi_json_ ## TYPE ## _deserialize (jso, &out); \
            if (rc) fprintf(stderr, "Deserialization failed\n"); \
            assert_int_equal (rc, TSS2_RC_SUCCESS); \
            json_object_put(jso); \
            jso = NULL; \
            rc = ifapi_json_ ## TYPE ## _serialize (PSERIALIZE, &jso); \
            assert_int_equal (rc, TSS2_RC_SUCCESS); \
            assert_non_null(jso); \
            const char *jso_string = json_object_to_json_string_ext(jso, JSON_C_TO_STRING_PRETTY); \
            assert_non_null(jso_string); \
            char *string1 = normalize(jso_string); \
            char *string2 =  normalize(DST); \
            assert_string_equal(string1, string2); \
            json_object_put(jso); \
            free(string1); \
            free(string2); \
        }

#define CHECK_JSON(TYPE, SRC, DST)  \
    CHECK_JSON2(TYPE, SRC, DST, &out)

#define CHECK_POLICY2(SRC, DST, PSERIALIZE)                   \
        { \
            TPMS_POLICY out; \
            TSS2_RC rc; \
            json_object *jso = json_tokener_parse((SRC)); \
            if (!jso) fprintf(stderr, "JSON parsing failed\n"); \
            assert_non_null(jso); \
            rc = ifapi_json_TPMS_POLICY_deserialize (jso, &out); \
            if (rc) fprintf(stderr, "Deserialization failed\n"); \
            assert_int_equal (rc, TSS2_RC_SUCCESS); \
            json_object_put(jso); \
            jso = NULL; \
            rc = ifapi_json_TPMS_POLICY_serialize (PSERIALIZE, &jso); \
            assert_int_equal (rc, TSS2_RC_SUCCESS); \
            assert_non_null(jso); \
            const char *jso_string = json_object_to_json_string_ext(jso, JSON_C_TO_STRING_PRETTY); \
            assert_non_null(jso_string); \
            char *string1 = normalize(jso_string); \
            char *string2 =  normalize(DST); \
            assert_string_equal(string1, string2); \
            json_object_put(jso); \
            ifapi_cleanup_policy(&out); \
            free(string1); \
            free(string2); \
        }

#define CHECK_POLICY(SRC, DST)  \
    CHECK_POLICY2(SRC, DST, &out)

#define CHECK_JSON_SIMPLE(TYPE, SRC, DST)  \
    CHECK_JSON2(TYPE, SRC, DST, out)

#define CHECK_JSON_TO_BIN(TYPE, SRC, DST) \
        { \
            TYPE out; \
            TSS2_RC rc; \
            TYPE expected = DST; \
            json_object *jso = json_tokener_parse((SRC)); \
            assert_non_null(jso); \
            rc = ifapi_json_ ## TYPE ## _deserialize (jso, &out); \
            assert_int_equal (rc, TSS2_RC_SUCCESS); \
            json_object_put(jso); \
            assert_true(out == expected);       \
        }

#define CHECK_BIN2(TYPE, BIN, PSERIALIZE)                  \
    TYPE BIN ## 2; \
    { \
        char *jso_string1, *jso_string2; \
        json_object *jso = NULL; \
        TSS2_RC rc = ifapi_json_ ## TYPE ## _serialize (PSERIALIZE, &jso); \
        jso_string1 = strdup(json_object_to_json_string_ext(jso, JSON_C_TO_STRING_PRETTY)); \
        assert_int_equal (rc, TSS2_RC_SUCCESS); \
        rc = ifapi_json_ ## TYPE ## _deserialize (jso, &BIN ## 2); \
        assert_int_equal (rc, TSS2_RC_SUCCESS); \
        json_object_put(jso); \
        jso = NULL; \
        rc = ifapi_json_ ## TYPE ## _serialize (PSERIALIZE ## 2, &jso); \
        jso_string2 = strdup(json_object_to_json_string_ext(jso, JSON_C_TO_STRING_PRETTY)); \
        assert_int_equal (rc, TSS2_RC_SUCCESS); \
        if (strcmp(jso_string1, jso_string2)) { \
            fprintf(stderr,"\n jso: %s\n", jso_string1); \
            fprintf(stderr,"\n jso: %s\n", jso_string2); \
        } \
        assert_string_equal(jso_string1, jso_string2); \
        json_object_put(jso); \
        free(jso_string1); \
        free(jso_string2); \
    }

#define CHECK_BIN(TYPE, BIN) \
    CHECK_BIN2(TYPE, BIN, &BIN)

#define CHECK_BIN_SIMPLE(TYPE, BIN) \
    CHECK_BIN2(TYPE, BIN, BIN)

static void
check_bin(void **state)
{
    TPM2B_PUBLIC inPublicAES = {
        .size = 0,
        .publicArea = {
            .type = TPM2_ALG_SYMCIPHER,
            .nameAlg = TPM2_ALG_SHA256,
            .objectAttributes = (TPMA_OBJECT_USERWITHAUTH |
                                 TPMA_OBJECT_SIGN_ENCRYPT |
                                 TPMA_OBJECT_DECRYPT),

            .authPolicy = {
                 .size = 0,
             },
            .parameters.symDetail = {
                 .sym = {
                     .algorithm = TPM2_ALG_AES,
                     .keyBits = {.aes = 128},
                     .mode = {.aes = TPM2_ALG_CFB}}
             },
            .unique.sym = {
                 .size = 0,
                 .buffer = {}
             }
        }
    };

    CHECK_BIN(TPM2B_PUBLIC, inPublicAES);

    TPM2B_PUBLIC inPublicECC = {
            .size = 0,
            .publicArea = {
                .type = TPM2_ALG_ECC,
                .nameAlg = TPM2_ALG_SHA1,
                .objectAttributes = (
                             TPMA_OBJECT_USERWITHAUTH |
                             TPMA_OBJECT_RESTRICTED |
                             TPMA_OBJECT_SIGN_ENCRYPT |
                             TPMA_OBJECT_FIXEDTPM |
                             TPMA_OBJECT_FIXEDPARENT |
                             TPMA_OBJECT_SENSITIVEDATAORIGIN
                             ),
                .authPolicy = {
                         .size = 0,
                     },

                .parameters.eccDetail = {
                     .symmetric = {
                         .algorithm = TPM2_ALG_NULL,
                         .keyBits.aes = 128,
                         .mode.aes = TPM2_ALG_ECB,
                     },
                     .scheme = {
                          .scheme = TPM2_ALG_ECDAA,
                          .details = { .ecdaa = { .hashAlg = TPM2_ALG_SHA256 }},
                      },
                     .curveID = TPM2_ECC_BN_P256,
                     .kdf = { .scheme = TPM2_ALG_NULL, .details = {} }
                 },
                /*
                  .parameters.asymDetail.symmetric.algorithm = TPM2_ALG_NULL,
                */
                .unique.ecc = {
                     .x = { .size = 0, .buffer = {} } ,
                     .y = { .size = 0, .buffer = {} } ,
                 },
            },
        };

    CHECK_BIN(TPM2B_PUBLIC, inPublicECC);

    TPM2B_PUBLIC inPublicECC_MGF1 = inPublicECC;

    inPublicECC_MGF1.publicArea.parameters.eccDetail.kdf.scheme = TPM2_ALG_MGF1;
    inPublicECC_MGF1.publicArea.parameters.eccDetail.kdf.details.mgf1.hashAlg = TPM2_ALG_SHA256;
    CHECK_BIN(TPM2B_PUBLIC, inPublicECC_MGF1);

    TPM2B_PUBLIC inPublicECC_KDF12 = inPublicECC;

    inPublicECC_KDF12.publicArea.parameters.eccDetail.kdf.scheme = TPM2_ALG_KDF1_SP800_56A;
    inPublicECC_KDF12.publicArea.parameters.eccDetail.kdf.details.kdf1_sp800_56a.hashAlg = TPM2_ALG_SHA256;
    CHECK_BIN(TPM2B_PUBLIC, inPublicECC_KDF12);

    TPM2B_PUBLIC inPublicECC_KDF13 = inPublicECC;

    inPublicECC_KDF13.publicArea.parameters.eccDetail.kdf.scheme = TPM2_ALG_KDF1_SP800_108;
    inPublicECC_KDF13.publicArea.parameters.eccDetail.kdf.details.kdf1_sp800_108.hashAlg = TPM2_ALG_SHA256;
    CHECK_BIN(TPM2B_PUBLIC, inPublicECC_KDF13);

    TPM2B_PUBLIC inPublicRSA2 = {
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
                 .size = 0,
                 .buffer = {},
             },
        },
    };

    TPMS_SIGNATURE_ECC ecc_signature = {
        .hash = TPM2_ALG_SHA1,
        .signatureR = {
            .size =  32,
            .buffer = {
                0x25, 0xdb, 0x1f, 0x8b, 0xbc, 0xfa, 0xbc, 0x31,
                0xf8, 0x17, 0x6a, 0xcb, 0xb2, 0xf8, 0x40, 0xa3,
                0xb6, 0xa5, 0xd3, 0x40, 0x65, 0x9d, 0x37, 0xee,
                0xd9, 0xfd, 0x52, 0x47, 0xf5, 0x14, 0xd5, 0x98
            },
        },
        .signatureS = {
            .size = 32,
            .buffer = {
                0xed, 0x62, 0x3e, 0x3d, 0xd2, 0x09, 0x08, 0xcf,
                0x58, 0x3c, 0x81, 0x4b, 0xbf, 0x65, 0x7e, 0x08,
                0xab, 0x9f, 0x40, 0xff, 0xea, 0x51, 0xda, 0x21,
                0x29, 0x8c, 0xe2, 0x4d, 0xeb, 0x34, 0x4c, 0xcc
            }
        }
    };

    CHECK_BIN(TPMS_SIGNATURE_ECC, ecc_signature);

    CHECK_BIN(TPM2B_PUBLIC, inPublicRSA2);

    TPMT_SIG_SCHEME ecc_scheme_ecdsa = { .scheme = TPM2_ALG_ECDSA, .details.ecdsa = TPM2_ALG_SHA1 };

    CHECK_BIN(TPMT_SIG_SCHEME, ecc_scheme_ecdsa);

    TPMT_SIG_SCHEME ecc_scheme_ecdaa = { .scheme = TPM2_ALG_ECDAA, .details.ecdaa = TPM2_ALG_SHA1 };

    CHECK_BIN(TPMT_SIG_SCHEME, ecc_scheme_ecdaa);

    TPMT_SIG_SCHEME rsa_scheme_rsapss = { .scheme = TPM2_ALG_RSAPSS, .details.rsapss = TPM2_ALG_SHA1 };

    CHECK_BIN(TPMT_SIG_SCHEME, rsa_scheme_rsapss);

    TPMT_SIG_SCHEME rsa_scheme_rsassa = { .scheme = TPM2_ALG_RSASSA, .details.rsassa = TPM2_ALG_SHA1 };

    CHECK_BIN(TPMT_SIG_SCHEME, rsa_scheme_rsassa);

    TPMT_SIG_SCHEME sm2_scheme = { .scheme = TPM2_ALG_SM2, .details.sm2 = TPM2_ALG_SHA1 };

    CHECK_BIN(TPMT_SIG_SCHEME, sm2_scheme);

    TPMT_SIG_SCHEME hmac_scheme = { .scheme = TPM2_ALG_HMAC, .details.hmac = TPM2_ALG_SHA1 };

    CHECK_BIN(TPMT_SIG_SCHEME, hmac_scheme);

    TPMT_SIG_SCHEME ecschnorr_scheme = { .scheme = TPM2_ALG_ECSCHNORR, .details.ecschnorr = TPM2_ALG_SHA1 };

    CHECK_BIN(TPMT_SIG_SCHEME, ecschnorr_scheme);

    TPMT_SIG_SCHEME rsa_scheme = { .scheme = TPM2_ALG_NULL };

    CHECK_BIN(TPMT_SIG_SCHEME, rsa_scheme);

    TPMA_NV testNV = 0xffffff0f ;

    CHECK_BIN_SIMPLE(TPMA_NV, testNV);

    TPML_PCR_SELECTION pcr_selection = {
        .count = 3,
        .pcrSelections = {
         {
            .hash = TPM2_ALG_SHA1,
            .sizeofSelect = 3,
            .pcrSelect = { 01, 00, 03 }},
        {
            .hash = TPM2_ALG_SHA256,
            .sizeofSelect = 3,
            .pcrSelect = { 01 ,00 ,03 }},
        {
            .hash = TPM2_ALG_SHA384,
            .sizeofSelect = 3,
            .pcrSelect = { 02, 00, 02 }}
        }
    };

    CHECK_BIN(TPML_PCR_SELECTION, pcr_selection);
}

static void
check_policy_bin(void **state)
{
    TPMS_PCRVALUE pcr_value;
    TPML_PCRVALUES *pcr_value_list;
    TPML_POLICYBRANCHES *or_branch_list;
    TPMS_POLICYPCR pcr_policy;
    TPMT_POLICYELEMENT policy_element0;
    TPMT_POLICYELEMENT policy_element1;
    TPMT_POLICYELEMENT policy_element_or;
    TPML_POLICYELEMENTS *policy_elements_or;
    TPML_POLICYELEMENTS *policy_elements0;
    TPML_POLICYELEMENTS *policy_elements1;
    TPMS_POLICY policy;
    TPMS_POLICYBRANCH branch0;
    TPMS_POLICYBRANCH branch1;

    pcr_value.pcr = 16;
    pcr_value.hashAlg = TPM2_ALG_SHA1;
    memset(&pcr_value.digest, 0, sizeof(TPMU_HA));
    memset(&pcr_policy, 0, sizeof(TPMS_POLICYPCR));
    pcr_value_list = calloc(1, sizeof(TPML_PCRVALUES) + sizeof(TPMS_PCRVALUE));
    if (pcr_value_list == NULL) {
        LOG_ERROR("%s", "Out of memory.");
        return;
    }
    pcr_value_list->count = 1;
    pcr_value_list->pcrs[0] = pcr_value;
    pcr_policy.pcrs = pcr_value_list;
    memset(&policy_element0, 0, sizeof(TPMT_POLICYELEMENT));
    policy_element0.element.PolicyPCR = pcr_policy;
    policy_element0.type = POLICYPCR;
    memset(&policy_element1, 0, sizeof(TPMT_POLICYELEMENT));
    policy_element1.element.PolicyPCR = pcr_policy;
    policy_element1.type = POLICYPCR;
    policy_elements0 = calloc(1, sizeof(TPML_POLICYELEMENTS) + sizeof(TPMT_POLICYELEMENT));
    if (policy_elements0 == NULL) {
        LOG_ERROR("%s", "Out of memory.");
        if (pcr_policy.pcrs){
            free(pcr_policy.pcrs);
        }
        return;
    }
    policy_elements0->count = 1;
    policy_elements0->elements[0] = policy_element0;
    policy.policy = policy_elements0;
    policy.description = "hareness description";
    policy.policyAuthorizations = NULL;
    memset(&policy.policyDigests, 0, sizeof(TPML_DIGEST_VALUES));

    //CHECK_BIN(TPMS_POLICY, policy);
    {
        char *jso_string1, *jso_string2;
        json_object *jso = NULL;
        TSS2_RC rc = ifapi_json_TPMS_POLICY_serialize (&policy, &jso);
        jso_string1 = strdup(json_object_to_json_string_ext(jso, JSON_C_TO_STRING_PRETTY));
        assert_int_equal (rc, TSS2_RC_SUCCESS);
        rc = ifapi_json_TPMS_POLICY_deserialize (jso, &policy);
        assert_int_equal (rc, TSS2_RC_SUCCESS);
        json_object_put(jso);
        jso = NULL;
        rc = ifapi_json_TPMS_POLICY_serialize (&policy, &jso);
        jso_string2 = strdup(json_object_to_json_string_ext(jso, JSON_C_TO_STRING_PRETTY));
        assert_int_equal (rc, TSS2_RC_SUCCESS);
        if (strcmp(jso_string1, jso_string2)) {
            fprintf(stderr,"\n jso: %s\n", jso_string1);
            fprintf(stderr,"\n jso: %s\n", jso_string2);
        }
        assert_string_equal(jso_string1, jso_string2);
        json_object_put(jso);
        free(jso_string1);
        free(jso_string2);
    }
    ifapi_cleanup_policy(&policy);

    or_branch_list = calloc(2, sizeof(TPML_POLICYBRANCHES) + (2 * sizeof(TPMS_POLICYBRANCH)));
    if (or_branch_list == NULL) {
        LOG_ERROR("%s", "Out of memory.");
        return;
    }
    or_branch_list->count = 2;

    policy_elements1 = calloc(1, sizeof(TPML_POLICYELEMENTS) + sizeof(TPMT_POLICYELEMENT));
    if (policy_elements1 == NULL) {
        LOG_ERROR("%s", "Out of memory.");
        if (or_branch_list){
            free(or_branch_list);
        }
        return;
    }
    policy_elements1->count = 1;
    policy_elements1->elements[0] = policy_element1;

    memset(&branch0, 0, sizeof(TPMS_POLICYBRANCH));
    memset(&branch1, 0, sizeof(TPMS_POLICYBRANCH));
    branch0.policy = policy_elements0;
    branch0.name = "branch0";
    branch0.description = "description branch 0";
    branch1.policy = policy_elements1;
    branch1.name = "branch1";
    branch1.description = "description branch 1";
    memcpy(&or_branch_list->authorizations[0], &branch0, sizeof(TPMS_POLICYBRANCH));
    memcpy(&or_branch_list->authorizations[1], &branch1, sizeof(TPMS_POLICYBRANCH));
    //or_policy.pcrs = pcr_branch_list;

    policy_elements_or = calloc(1, sizeof(TPML_POLICYELEMENTS) + sizeof(TPMT_POLICYELEMENT));
    if (policy_elements_or == NULL) {
        LOG_ERROR("%s", "Out of memory.");
        if (or_branch_list) {
            free(or_branch_list);
        }
        return;
    }
    policy_elements_or->count = 1;

    memset(&policy_element_or, 0, sizeof(TPMT_POLICYELEMENT));
    policy_element_or.element.PolicyOr.branches = or_branch_list;
    policy_element_or.type = POLICYOR;
    policy_elements_or->elements[0] = policy_element_or;
    policy.policy =  policy_elements_or;

    //CHECK_BIN(TPMS_POLICY, policy);
    {
        char *jso_string1, *jso_string2;
        json_object *jso = NULL;
        TSS2_RC rc = ifapi_json_TPMS_POLICY_serialize (&policy, &jso);
        jso_string1 = strdup(json_object_to_json_string_ext(jso, JSON_C_TO_STRING_PRETTY));
        assert_int_equal (rc, TSS2_RC_SUCCESS);
        rc = ifapi_json_TPMS_POLICY_deserialize (jso, &policy);
        assert_int_equal (rc, TSS2_RC_SUCCESS);
        json_object_put(jso);
        jso = NULL;
        rc = ifapi_json_TPMS_POLICY_serialize (&policy, &jso);
        jso_string2 = strdup(json_object_to_json_string_ext(jso, JSON_C_TO_STRING_PRETTY));
        assert_int_equal (rc, TSS2_RC_SUCCESS);
        if (strcmp(jso_string1, jso_string2)) {
            fprintf(stderr,"\n jso: %s\n", jso_string1);
            fprintf(stderr,"\n jso: %s\n", jso_string2);
        }
        assert_string_equal(jso_string1, jso_string2);
        json_object_put(jso);
        free(jso_string1);
        free(jso_string2);
    }
    ifapi_cleanup_policy(&policy);

    free(policy_elements_or);
    free(policy_elements0);
    free(policy_elements1);
    free(or_branch_list);
    free(pcr_value_list);
}

static void
check_json_to_bin(void **state)
{
    CHECK_JSON_TO_BIN(UINT64, "22147483647", 22147483647);
    CHECK_JSON_TO_BIN(UINT64, "\"0xffffffff\"", 0xffffffff);
    CHECK_JSON_TO_BIN(UINT64, "\"0xfffffffff\"", 0xfffffffff);
    CHECK_JSON_TO_BIN(UINT32,  "\"0xFfffffff\"", 0xffffffff);
    CHECK_JSON_TO_BIN(UINT16, "\"0xffff\"", 0xffff);
}

static void
check_json_structs(void **state)
{
    const char *test_json_TPMS_POLICYTEMPLATE =
        "{\n"
        "  \"templateHash\": \"0011223344556677889900112233445566778899\"\n"
        "}";
    CHECK_JSON(TPMS_POLICYTEMPLATE, test_json_TPMS_POLICYTEMPLATE, test_json_TPMS_POLICYTEMPLATE);

    const char *test_json_TPM2B_PUBLIC_expected =
        "{\n"
        "  \"size\":0,\n"
        "  \"publicArea\":{\n"
        "    \"type\":\"ECC\",\n"
        "    \"nameAlg\":\"sha1\",\n"
        "\"objectAttributes\":{"
        "      \"fixedTPM\":1,"
        "      \"stClear\":0,"
        "      \"fixedParent\":1,"
        "      \"sensitiveDataOrigin\":1,"
        "      \"userWithAuth\":1,"
        "      \"adminWithPolicy\":0,"
        "      \"noDA\":0,"
        "      \"encryptedDuplication\":0,"
        "      \"restricted\":1,"
        "      \"decrypt\":0,"
        "      \"sign\":1"
        "    },"
        "    \"authPolicy\":\"\",\n"
        "    \"parameters\":{\n"
        "      \"symmetric\":{\n"
        "        \"algorithm\":\"NULL\"\n"
        "      },\n"
        "      \"scheme\":{\n"
        "        \"scheme\":\"ECDAA\",\n"
        "        \"details\":{\n"
        "          \"hashAlg\":\"sha256\",\n"
        "          \"count\":0\n"
        "        }\n"
        "      },\n"
        "      \"curveID\":\"BN_P256\",\n"
        "      \"kdf\":{\n"
        "        \"scheme\":\"NULL\"\n"
        "      }\n"
        "    },\n"
        "    \"unique\":{\n"
        "      \"x\": \"\",\n"
        "      \"y\": \"\"\n"
        "    }\n"
        "  }\n"
        "}";

    const char *test_json_TPM2B_PUBLIC_src=
        "{"
        "  \"size\":0,"
        "  \"publicArea\":{"
        "    \"type\":\"ECC\","
        "    \"nameAlg\":\"sha1\","
        "    \"objectAttributes\":["
        "      \"fixedTPM\","
        "      \"fixedParent\","
        "      \"sensitiveDataOrigin\","
        "      \"userWithAuth\","
        "      \"restricted\","
        "      \"sign\""
        "    ],"
        "    \"authPolicy\":\"\","
        "    \"parameters\":{"
        "      \"symmetric\":{"
        "        \"algorithm\":\"NULL\""
        "      },"
        "      \"scheme\":{"
        "        \"scheme\":\"ECDAA\","
        "        \"details\":{"
        "          \"hashAlg\":\"sha256\","
        "          \"count\":0"
        "        }"
        "      },"
        "      \"curveID\":\"ECC_BN_P256\","
        "      \"kdf\":{"
        "        \"scheme\":\"NULL\""
        "      }"
        "    },"
        "    \"unique\":{"
        "      \"x\": \"\",\n"
        "      \"y\": \"\"\n"
        "    }"
        "  }"
        "}"
        "";
    const char *test_json_TPM2B_PUBLIC_dwnc_src =
        "{"
        "  \"size\":0,"
        "  \"publicArea\":{"
        "    \"type\":\"ecc\","
        "    \"nameAlg\":\"sha1\","
        "    \"objectAttributes\":["
        "      \"fixedTPM\","
        "      \"fixedParent\","
        "      \"sensitiveDataOrigin\","
        "      \"userWithAuth\","
        "      \"restricted\","
        "      \"sign\""
        "    ],"
        "    \"authPolicy\":\"\","
        "    \"parameters\":{"
        "      \"symmetric\":{"
        "        \"algorithm\":\"null\""
        "      },"
        "      \"scheme\":{"
        "        \"scheme\":\"ecdaa\","
        "        \"details\":{"
        "          \"hashAlg\":\"sha256\","
        "          \"count\":0"
        "        }"
        "      },"
        "      \"curveID\":\"ecc_BN_P256\","
        "      \"kdf\":{"
        "        \"scheme\":\"null\""
        "      }"
        "    },"
        "    \"unique\":{"
        "      \"x\": \"\",\n"
        "      \"y\": \"\"\n"
        "      }"
        "    }"
        "  }"
        "}"
        "";

    CHECK_JSON(TPM2B_PUBLIC, test_json_TPM2B_PUBLIC_src, test_json_TPM2B_PUBLIC_expected);
    CHECK_JSON(TPM2B_PUBLIC, test_json_TPM2B_PUBLIC_dwnc_src, test_json_TPM2B_PUBLIC_expected);

    const char *test_json_TPMS_ATTEST_certify_src =
        "{\n"
        "    \"magic\": \"0xff544347\",\n"
        "    \"type\": \"ST_ATTEST_CERTIFY\",\n"
        "    \"qualifiedSigner\": \"0x00010203040506070809a0a1a2a3a4a5a6a7a8a9\",\n"
        "    \"extraData\": \"0x00010203040506070809b0b1b2b3b4b5b6b7b8b9\",\n"
        "    \"clockInfo\": {\n"
        "        \"clock\": 123,\n"
        "        \"resetCount\": 23,\n"
        "        \"restartCount\": 1,\n"
        "        \"safe\": \"yes\"\n"
        "    },\n"
        "    \"firmwareVersion\": 783,\n"
        "    \"attested\": {\n"
        "        \"name\": \"0x00010203040506070809c0c1c2c3c4c5c6c7c8c9\",\n"
        "        \"qualifiedName\": \"0x00010203040506070809d0d1d2d3d4d5d6d7d8d9\"\n"
        "    }\n"
        "}";
    const char *test_json_TPMS_ATTEST_certify_expt =
        "{\n"
        "    \"magic\": \"VALUE\",\n"
        "    \"type\": \"ATTEST_CERTIFY\",\n"
        "    \"qualifiedSigner\": \"00010203040506070809a0a1a2a3a4a5a6a7a8a9\",\n"
        "    \"extraData\": \"00010203040506070809b0b1b2b3b4b5b6b7b8b9\",\n"
        "    \"clockInfo\": {\n"
        "        \"clock\": 123,\n"
        "        \"resetCount\": 23,\n"
        "        \"restartCount\": 1,\n"
        "        \"safe\": \"YES\"\n"
        "    },\n"
        "    \"firmwareVersion\": 783,\n"
        "    \"attested\": {\n"
        "        \"name\": \"00010203040506070809c0c1c2c3c4c5c6c7c8c9\",\n"
        "        \"qualifiedName\": \"00010203040506070809d0d1d2d3d4d5d6d7d8d9\"\n"
        "    }\n"
        "}";
    CHECK_JSON(TPMS_ATTEST, test_json_TPMS_ATTEST_certify_src, test_json_TPMS_ATTEST_certify_expt);

    const char *test_json_TPMS_ATTEST_sessionaudit_src =
        "{\n"
        "    \"magic\": \"0xff544347\",\n"
        "    \"type\": \"ST_ATTEST_SESSION_AUDIT\",\n"
        "    \"qualifiedSigner\": \"0x00010203040506070809a0a1a2a3a4a5a6a7a8a9\",\n"
        "    \"extraData\": \"0x00010203040506070809b0b1b2b3b4b5b6b7b8b9\",\n"
        "    \"clockInfo\": {\n"
        "        \"clock\": [12345,0],\n"
        "        \"resetCount\": 23,\n"
        "        \"restartCount\": 1,\n"
        "        \"safe\": \"yes\"\n"
        "    },\n"
        "    \"firmwareVersion\": [783783,0],\n"
        "    \"attested\": {\n"
        "        \"exclusiveSession\": \"yes\",\n"
        "        \"sessionDigest\": \"0x00010203040506070809d0d1d2d3d4d5d6d7d8d9\"\n"
        "    }\n"
        "}";
    const char *test_json_TPMS_ATTEST_sessionaudit_expt =
        "{\n"
        "    \"magic\": \"VALUE\",\n"
        "    \"type\": \"ATTEST_SESSION_AUDIT\",\n"
        "    \"qualifiedSigner\": \"00010203040506070809a0a1a2a3a4a5a6a7a8a9\",\n"
        "    \"extraData\": \"00010203040506070809b0b1b2b3b4b5b6b7b8b9\",\n"
        "    \"clockInfo\": {\n"
        "        \"clock\": 53021371269120,\n"
        "        \"resetCount\": 23,\n"
        "        \"restartCount\": 1,\n"
        "        \"safe\": \"YES\"\n"
        "    },\n"
        "    \"firmwareVersion\": [783783,0],\n"
        "    \"attested\": {\n"
        "        \"exclusiveSession\": \"YES\",\n"
        "        \"sessionDigest\": \"00010203040506070809d0d1d2d3d4d5d6d7d8d9\"\n"
        "    }\n"
        "}";
    CHECK_JSON(TPMS_ATTEST, test_json_TPMS_ATTEST_sessionaudit_src, test_json_TPMS_ATTEST_sessionaudit_expt);

    const char *test_json_TPMS_ATTEST_certifycreation_src =
        "{\n"
        "    \"magic\": \"0xff544347\",\n"
        "    \"type\": \"ST_ATTEST_CREATION\",\n"
        "    \"qualifiedSigner\": \"0x00010203040506070809a0a1a2a3a4a5a6a7a8a9\",\n"
        "    \"extraData\": \"0x00010203040506070809b0b1b2b3b4b5b6b7b8b9\",\n"
        "    \"clockInfo\": {\n"
        "        \"clock\": 123,\n"
        "        \"resetCount\": 23,\n"
        "        \"restartCount\": 1,\n"
        "        \"safe\": \"yes\"\n"
        "    },\n"
        "    \"firmwareVersion\": [0,783],\n"
        "    \"attested\": {\n"
        "        \"objectName\": \"0x00010203040506070809c0c1c2c3c4c5c6c7c8c9\",\n"
        "        \"creationHash\": \"0x00010203040506070809d0d1d2d3d4d5d6d7d8d9\"\n"
        "    }\n"
        "}";
    const char *test_json_TPMS_ATTEST_certifycreation_expt =
        "{\n"
        "    \"magic\": \"VALUE\",\n"
        "    \"type\": \"ATTEST_CREATION\",\n"
        "    \"qualifiedSigner\": \"00010203040506070809a0a1a2a3a4a5a6a7a8a9\",\n"
        "    \"extraData\": \"00010203040506070809b0b1b2b3b4b5b6b7b8b9\",\n"
        "    \"clockInfo\": {\n"
        "        \"clock\": 123,\n"
        "        \"resetCount\": 23,\n"
        "        \"restartCount\": 1,\n"
        "        \"safe\": \"YES\"\n"
        "    },\n"
        "    \"firmwareVersion\": 783,\n"
        "    \"attested\": {\n"
        "        \"objectName\": \"00010203040506070809c0c1c2c3c4c5c6c7c8c9\",\n"
        "        \"creationHash\": \"00010203040506070809d0d1d2d3d4d5d6d7d8d9\"\n"
        "    }\n"
        "}";
    CHECK_JSON(TPMS_ATTEST, test_json_TPMS_ATTEST_certifycreation_src, test_json_TPMS_ATTEST_certifycreation_expt);

    const char *test_json_TPMS_ATTEST_commandaudit_src =
        "{\n"
        "    \"magic\": \"0xff544347\",\n"
        "    \"type\": \"ST_ATTEST_COMMAND_AUDIT\",\n"
        "    \"qualifiedSigner\": \"0x00010203040506070809a0a1a2a3a4a5a6a7a8a9\",\n"
        "    \"extraData\": \"0x00010203040506070809b0b1b2b3b4b5b6b7b8b9\",\n"
        "    \"clockInfo\": {\n"
        "        \"clock\": 123,\n"
        "        \"resetCount\": 23,\n"
        "        \"restartCount\": 1,\n"
        "        \"safe\": \"yes\"\n"
        "    },\n"
        "    \"firmwareVersion\": 783,\n"
        "    \"attested\": {\n"
        "        \"auditCounter\": 456,\n"
        "        \"digestAlg\": \"sha1\",\n"
        "        \"auditDigest\": \"0x00010203040506070809c0c1c2c3c4c5c6c7c8c9\",\n"
        "        \"commandDigest\": \"0x00010203040506070809d0d1d2d3d4d5d6d7d8d9\"\n"
        "    }\n"
        "}";
    const char *test_json_TPMS_ATTEST_commandaudit_expt =
        "{\n"
        "    \"magic\": \"VALUE\",\n"
        "    \"type\": \"ATTEST_COMMAND_AUDIT\",\n"
        "    \"qualifiedSigner\": \"00010203040506070809a0a1a2a3a4a5a6a7a8a9\",\n"
        "    \"extraData\": \"00010203040506070809b0b1b2b3b4b5b6b7b8b9\",\n"
        "    \"clockInfo\": {\n"
        "        \"clock\": 123,\n"
        "        \"resetCount\": 23,\n"
        "        \"restartCount\": 1,\n"
        "        \"safe\": \"YES\"\n"
        "    },\n"
        "    \"firmwareVersion\": 783,\n"
        "    \"attested\": {\n"
        "        \"auditCounter\": 456,\n"
        "        \"digestAlg\": \"sha1\",\n"
        "        \"auditDigest\": \"00010203040506070809c0c1c2c3c4c5c6c7c8c9\",\n"
        "        \"commandDigest\": \"00010203040506070809d0d1d2d3d4d5d6d7d8d9\"\n"
        "    }\n"
        "}";
    CHECK_JSON(TPMS_ATTEST, test_json_TPMS_ATTEST_commandaudit_src, test_json_TPMS_ATTEST_commandaudit_expt);

    const char *test_json_TPMS_ATTEST_time_src =
        "{\n"
        "    \"magic\": \"0xff544347\",\n"
        "    \"type\": \"ST_ATTEST_TIME\",\n"
        "    \"qualifiedSigner\": \"0x00010203040506070809a0a1a2a3a4a5a6a7a8a9\",\n"
        "    \"extraData\": \"0x00010203040506070809b0b1b2b3b4b5b6b7b8b9\",\n"
        "    \"clockInfo\": {\n"
        "        \"clock\": 123,\n"
        "        \"resetCount\": 23,\n"
        "        \"restartCount\": 1,\n"
        "        \"safe\": \"yes\"\n"
        "    },\n"
        "    \"firmwareVersion\": 783,\n"
        "    \"attested\": {\n"
        "        \"time\": {\n"
        "            \"time\": 234,\n"
        "            \"clockInfo\": {\n"
        "                \"clock\": 123,\n"
        "                \"resetCount\": 23,\n"
        "                \"restartCount\": 1,\n"
        "                \"safe\": \"yes\"\n"
        "            }\n"
        "        },\n"
        "        \"firmwareVersion\": 783\n"
        "    }\n"
        "}";
    const char *test_json_TPMS_ATTEST_time_expt =
        "{\n"
        "    \"magic\": \"VALUE\",\n"
        "    \"type\": \"ATTEST_TIME\",\n"
        "    \"qualifiedSigner\": \"00010203040506070809a0a1a2a3a4a5a6a7a8a9\",\n"
        "    \"extraData\": \"00010203040506070809b0b1b2b3b4b5b6b7b8b9\",\n"
        "    \"clockInfo\": {\n"
        "        \"clock\": 123,\n"
        "        \"resetCount\": 23,\n"
        "        \"restartCount\": 1,\n"
        "        \"safe\": \"YES\"\n"
        "    },\n"
        "    \"firmwareVersion\": 783,\n"
        "    \"attested\": {\n"
        "        \"time\": {\n"
        "            \"time\": 234,\n"
        "            \"clockInfo\": {\n"
        "                \"clock\": 123,\n"
        "                \"resetCount\": 23,\n"
        "                \"restartCount\": 1,\n"
        "                \"safe\": \"YES\"\n"
        "            }\n"
        "        },\n"
        "        \"firmwareVersion\": 783\n"
        "    }\n"
        "}";
    CHECK_JSON(TPMS_ATTEST, test_json_TPMS_ATTEST_time_src, test_json_TPMS_ATTEST_time_expt);

    const char *test_json_TPMS_ATTEST_certifynv_src =
        "{\n"
        "    \"magic\": \"0xff544347\",\n"
        "    \"type\": \"ST_ATTEST_NV\",\n"
        "    \"qualifiedSigner\": \"0x00010203040506070809a0a1a2a3a4a5a6a7a8a9\",\n"
        "    \"extraData\": \"0x00010203040506070809b0b1b2b3b4b5b6b7b8b9\",\n"
        "    \"clockInfo\": {\n"
        "        \"clock\": 123,\n"
        "        \"resetCount\": 23,\n"
        "        \"restartCount\": 1,\n"
        "        \"safe\": \"yes\"\n"
        "    },\n"
        "    \"firmwareVersion\": 783,\n"
        "    \"attested\": {\n"
        "        \"indexName\": \"0x00010203040506070809c0c1c2c3c4c5c6c7c8c9\",\n"
        "        \"offset\": 10,\n"
        "        \"nvContents\": \"0x00010203040506070809d0d1d2d3d4d5d6d7d8d9\"\n"
        "    }\n"
        "}";
    const char *test_json_TPMS_ATTEST_certifynv_expt =
        "{\n"
        "    \"magic\": \"VALUE\",\n"
        "    \"type\": \"ATTEST_NV\",\n"
        "    \"qualifiedSigner\": \"00010203040506070809a0a1a2a3a4a5a6a7a8a9\",\n"
        "    \"extraData\": \"00010203040506070809b0b1b2b3b4b5b6b7b8b9\",\n"
        "    \"clockInfo\": {\n"
        "        \"clock\": 123,\n"
        "        \"resetCount\": 23,\n"
        "        \"restartCount\": 1,\n"
        "        \"safe\": \"YES\"\n"
        "    },\n"
        "    \"firmwareVersion\": 783,\n"
        "    \"attested\": {\n"
        "        \"indexName\": \"00010203040506070809c0c1c2c3c4c5c6c7c8c9\",\n"
        "        \"offset\": 10,\n"
        "        \"nvContents\": \"00010203040506070809d0d1d2d3d4d5d6d7d8d9\"\n"
        "    }\n"
        "}";
    CHECK_JSON(TPMS_ATTEST, test_json_TPMS_ATTEST_certifynv_src, test_json_TPMS_ATTEST_certifynv_expt);

    const char *test_json_TPMT_KEYEDHASH_SCHEME_hmac_src =
        "{\n"
        "    \"scheme\": \"HMAC\",\n"
        "    \"details\": {\n"
        "        \"hashAlg\": \"sha256\"\n"
        "    }\n"
        "}";
    const char *test_json_TPMT_KEYEDHASH_SCHEME_hmac_expt =
        "{\n"
        "    \"scheme\": \"HMAC\",\n"
        "    \"details\": {\n"
        "        \"hashAlg\": \"sha256\"\n"
        "    }\n"
        "}";
    CHECK_JSON(TPMT_KEYEDHASH_SCHEME, test_json_TPMT_KEYEDHASH_SCHEME_hmac_src, test_json_TPMT_KEYEDHASH_SCHEME_hmac_expt);

    const char *test_json_TPMT_KEYEDHASH_SCHEME_xor_src =
        "{\n"
        "    \"scheme\": \"XOR\",\n"
        "    \"details\": {\n"
        "        \"hashAlg\": \"sha256\",\n"
        "        \"kdf\": \"MGF1\"\n"
        "    }\n"
        "}";
    const char *test_json_TPMT_KEYEDHASH_SCHEME_xor_expt =
        "{\n"
        "    \"scheme\": \"XOR\",\n"
        "    \"details\": {\n"
        "        \"hashAlg\": \"sha256\",\n"
        "        \"kdf\": \"MGF1\"\n"
        "    }\n"
        "}";
    CHECK_JSON(TPMT_KEYEDHASH_SCHEME, test_json_TPMT_KEYEDHASH_SCHEME_xor_src, test_json_TPMT_KEYEDHASH_SCHEME_xor_expt);

    const char *test_json_TPMS_TAGGED_POLICY_sha256_src =
        "{\n"
        "    \"handle\":0,"
        "    \"policyHash\": {\n"
        "        \"hashAlg\":\"sha256\",\n"
        "        \"digest\":\"59215cb6c21a60e26b2cc479334a021113611903795507c1227659e2aef23d16\"\n"
        "    }\n"
        "}";

    const char *test_json_TPMS_TAGGED_POLICY_sha256_expt =
        "{\n"
        "    \"handle\":0,"
        "    \"policyHash\": {\n"
        "        \"hashAlg\":\"sha256\",\n"
        "        \"digest\":\"59215cb6c21a60e26b2cc479334a021113611903795507c1227659e2aef23d16\"\n"
        "    }\n"
        "}";
    CHECK_JSON(TPMS_TAGGED_POLICY, test_json_TPMS_TAGGED_POLICY_sha256_src, test_json_TPMS_TAGGED_POLICY_sha256_expt);

    const char *test_json_TPMS_ACT_DATA_src =
        "{"
        "    \"handle\":0,"
        "    \"timeout\":23,"
        "    \"attributes\":["
        "      \"signaled\""
        "    ],"
        "}";

    const char *test_json_TPMS_ACT_DATA_expt =
        "{\n"
        "    \"handle\":0,\n"
        "    \"timeout\":23,\n"
        "    \"attributes\":{"
        "      \"signaled\":1,"
        "      \"preserveSignaled\":0"
        "    }"
        "}";
    CHECK_JSON(TPMS_ACT_DATA, test_json_TPMS_ACT_DATA_src, test_json_TPMS_ACT_DATA_expt);

    /*
     * Check whether policy version with complex TPM2B for newParentPublic in policy
     * POLICYDUPLICATIONSELECT is deserialized to TPMT_PUBLIC.
     */

    const char *test_json_TPMS_POLICY_src =
        "{\n"
        "    \"description\":\"Description pol_duplicate\",\n"
        "    \"policy\":[\n"
        "        {\n"
        "            \"type\": \"POLICYDUPLICATIONSELECT\",\n"
        "            \"newParentPublic\":\n"
        "            {\n"
        "                \"size\":90,\n"
        "                \"publicArea\":{\n"
        "                    \"type\":\"ECC\",\n"
        "                    \"nameAlg\":\"sha256\",\n"
        "                    \"objectAttributes\":{\n"
        "                        \"fixedTPM\":1,\n"
        "                        \"stClear\":0,\n"
        "                        \"fixedParent\":1,\n"
        "                        \"sensitiveDataOrigin\":1,\n"
        "                        \"userWithAuth\":1,\n"
        "                        \"adminWithPolicy\":0,\n"
        "                        \"noDA\":1,\n"
        "                        \"encryptedDuplication\":0,\n"
        "                        \"restricted\":1,\n"
        "                        \"decrypt\":1,\n"
        "                        \"sign\":0\n"
        "                    },\n"
        "                    \"authPolicy\":\"\",\n"
        "                    \"parameters\":{\n"
        "                        \"symmetric\":{\n"
        "                            \"algorithm\":\"AES\",\n"
        "                            \"keyBits\":128,\n"
        "                            \"mode\":\"CFB\"\n"
        "                        },\n"
        "                        \"scheme\":{\n"
        "                            \"scheme\":\"NULL\"\n"
        "                        },\n"
        "                        \"curveID\":\"NIST_P256\",\n"
        "                        \"kdf\":{\n"
        "                            \"scheme\":\"NULL\"\n"
        "                        }\n"
        "                    },\n"
        "                    \"unique\":{\n"
        "                        \"x\":\"a12497c5ba7473779d02fd7a9df5b7afc7bc6db6d9f5eccb0b74a265259cacce\",\n"
        "                        \"y\":\"b92b44809e190e721524696e2eab1da8dea0f7bd9cd6c38d5d9804c5c64faa95\"\n"
        "                    }\n"
        "                }\n"
        "            }\n"
        "        }\n"
        "    ]\n"
        "}\n";

       const char *test_json_TPMS_POLICY_expt =
        "{\n"
        "    \"description\":\"Description pol_duplicate\",\n"
        "    \"policyDigests\":[],\n"
        "    \"policy\":[\n"
        "        {\n"
        "            \"type\": \"POLICYDUPLICATIONSELECT\",\n"
        "            \"objectName\":\"\",\"includeObject\":\"NO\","
        "            \"newParentPublic\":\n"
        "            {\n"
        "                \"type\":\"ECC\",\n"
        "                \"nameAlg\":\"sha256\",\n"
        "                \"objectAttributes\":{\n"
        "                    \"fixedTPM\":1,\n"
        "                    \"stClear\":0,\n"
        "                    \"fixedParent\":1,\n"
        "                    \"sensitiveDataOrigin\":1,\n"
        "                    \"userWithAuth\":1,\n"
        "                    \"adminWithPolicy\":0,\n"
        "                    \"noDA\":1,\n"
        "                    \"encryptedDuplication\":0,\n"
        "                    \"restricted\":1,\n"
        "                    \"decrypt\":1,\n"
        "                    \"sign\":0\n"
        "                },\n"
        "                \"authPolicy\":\"\",\n"
        "                \"parameters\":{\n"
        "                    \"symmetric\":{\n"
        "                        \"algorithm\":\"AES\",\n"
        "                        \"keyBits\":128,\n"
        "                        \"mode\":\"CFB\"\n"
        "                    },\n"
        "                    \"scheme\":{\n"
        "                        \"scheme\":\"NULL\"\n"
        "                    },\n"
        "                    \"curveID\":\"NIST_P256\",\n"
        "                    \"kdf\":{\n"
        "                        \"scheme\":\"NULL\"\n"
        "                    }\n"
        "                },\n"
        "                \"unique\":{\n"
        "                    \"x\":\"a12497c5ba7473779d02fd7a9df5b7afc7bc6db6d9f5eccb0b74a265259cacce\",\n"
        "                    \"y\":\"b92b44809e190e721524696e2eab1da8dea0f7bd9cd6c38d5d9804c5c64faa95\"\n"
        "                }\n"
        "            }\n"
        "        }\n"
        "    ]\n"
        "}\n";

      CHECK_POLICY(test_json_TPMS_POLICY_src, test_json_TPMS_POLICY_expt);
}

static void
check_json_constants(void **state)
{
    CHECK_JSON_SIMPLE(TPMI_ALG_HASH, "\"sha1\"", "\"sha1\"");
    CHECK_JSON_SIMPLE(TPMI_ALG_HASH, "\"0x04\"", "\"sha1\"");
    CHECK_JSON_SIMPLE(TPMI_ALG_HASH, "4", "\"sha1\"");
}

static void
check_json_numbers(void **state)
{
    CHECK_JSON_SIMPLE(UINT16, "10", "10");
    CHECK_JSON_SIMPLE(UINT16, "\"0x0a\"", "10");
    CHECK_JSON_SIMPLE(UINT64, "10000000000000000","[2328306,1874919424]");
}

static void
check_json_bits(void **state)
{
    CHECK_JSON_SIMPLE(TPMA_NV, "{\"PPWRITE\":1,\"OWNERWRITE\":1}",
                      "{\"PPWRITE\":1,\"OWNERWRITE\":1,\"AUTHWRITE\":0,\"POLICYWRITE\":0,\"POLICY_DELETE\":0,"
                      "\"WRITELOCKED\":0,\"WRITEALL\":0,\"WRITEDEFINE\":0,\"WRITE_STCLEAR\":0,\"GLOBALLOCK\":0,\"PPREAD\":0,"
                      "\"OWNERREAD\":0,\"AUTHREAD\":0,\"POLICYREAD\":0,\"NO_DA\":0,\"ORDERLY\":0,\"CLEAR_STCLEAR\":0,"
                      "\"READLOCKED\":0,\"WRITTEN\":0,\"PLATFORMCREATE\":0,\"READ_STCLEAR\":0,\"TPM2_NT\":\"ORDINARY\"}");
    CHECK_JSON_SIMPLE(TPMA_LOCALITY, "3", "{\"ZERO\":1,\"ONE\":1,\"TWO\":0,\"THREE\":0,\"FOUR\":0,\"Extended\":0}");
    CHECK_JSON_SIMPLE(TPMA_LOCALITY,
                      "[ \"ZERO\", \"ONE\" ]",
                      "{\"ZERO\":1,\"ONE\":1,\"TWO\":0,\"THREE\":0,\"FOUR\":0,\"Extended\":0}");
    CHECK_JSON_SIMPLE(TPMA_NV, "\"0xffffff0f\"",
                      "{\"PPWRITE\":1,\"OWNERWRITE\":1,\"AUTHWRITE\":1,\"POLICYWRITE\":1,\"POLICY_DELETE\":1,"
                      "\"WRITELOCKED\":1,\"WRITEALL\":1,\"WRITEDEFINE\":1,\"WRITE_STCLEAR\":1,\"GLOBALLOCK\":1,\"PPREAD\":1,"
                      "\"OWNERREAD\":1,\"AUTHREAD\":1,\"POLICYREAD\":1,\"NO_DA\":1,\"ORDERLY\":1,\"CLEAR_STCLEAR\":1,"
                      "\"READLOCKED\":1,\"WRITTEN\":1,\"PLATFORMCREATE\":1,\"READ_STCLEAR\":1,\"TPM2_NT\":\"ORDINARY\"}");
    CHECK_JSON_SIMPLE(TPMA_LOCALITY, "3", "{\"ZERO\":1,\"ONE\":1,\"TWO\":0,\"THREE\":0,\"FOUR\":0,\"Extended\":0}");
    CHECK_JSON_SIMPLE(TPMA_LOCALITY,
                      "{\"ZERO\":1,\"ONE\":1,\"TWO\":0,\"THREE\":0,\"FOUR\":0,\"Extended\":0}",
                      "{\"ZERO\":1,\"ONE\":1,\"TWO\":0,\"THREE\":0,\"FOUR\":0,\"Extended\":0}");
    CHECK_JSON_SIMPLE(TPMA_OBJECT,
                      "{\"fixedTPM\":1,\"stClear\":1,\"fixedParent\":0,\"sensitiveDataOrigin\":0,\"userWithAuth\":0,"
                      "\"adminWithPolicy\":0,\"noDA\":0,\"encryptedDuplication\":0,\"restricted\":0,\"decrypt\":0,\"sign\":0}",
                      "{\"fixedTPM\":1,\"stClear\":1,\"fixedParent\":0,\"sensitiveDataOrigin\":0,\"userWithAuth\":0,"
                      "\"adminWithPolicy\":0,\"noDA\":0,\"encryptedDuplication\":0,\"restricted\":0,\"decrypt\":0,\"sign\":0}");
    CHECK_JSON_SIMPLE(TPMA_OBJECT,
                      "\"0\"",
                      "{\"fixedTPM\":0,\"stClear\":0,\"fixedParent\":0,\"sensitiveDataOrigin\":0,\"userWithAuth\":0,"
                      "\"adminWithPolicy\":0,\"noDA\":0,\"encryptedDuplication\":0,\"restricted\":0,\"decrypt\":0,\"sign\":0}");
    CHECK_JSON_SIMPLE(TPMA_ACT,
                      "\"0\"",
                      "{\"signaled\":0,\"preserveSignaled\":0}");
    CHECK_JSON_SIMPLE(TPMA_ACT,
                      "0",
                      "{\"signaled\":0,\"preserveSignaled\":0}");
    CHECK_JSON_SIMPLE(TPMA_ACT,
                      "\"1\"",
                      "{\"signaled\":1,\"preserveSignaled\":0}");
    CHECK_JSON_SIMPLE(TPMA_ACT,
                      "1",
                      "{\"signaled\":1,\"preserveSignaled\":0}");
    CHECK_JSON_SIMPLE(TPMA_ACT,
                      "\"2\"",
                      "{\"signaled\":0,\"preserveSignaled\":1}");
    CHECK_JSON_SIMPLE(TPMA_ACT,
                      "2",
                      "{\"signaled\":0,\"preserveSignaled\":1}");
    CHECK_JSON_SIMPLE(TPMA_ACT,
                      "\"3\"",
                      "{\"signaled\":1,\"preserveSignaled\":1}");
    CHECK_JSON_SIMPLE(TPMA_ACT,
                      "3",
                      "{\"signaled\":1,\"preserveSignaled\":1}");
    CHECK_JSON_SIMPLE(TPMA_ACT,
                    "{\"signaled\":1,\"preserveSignaled\":0}",
                    "{\"signaled\":1,\"preserveSignaled\":0}");
    CHECK_JSON_SIMPLE(TPMA_ACT,
                    "{\"signaled\":0,\"preserveSignaled\":1}",
                    "{\"signaled\":0,\"preserveSignaled\":1}");

    const char *test_json_TPMA_NV_expected =\
                    "{"
                    "  \"PPWRITE\":0,"
                    "  \"OWNERWRITE\":1,"
                    "  \"AUTHWRITE\":1,"
                    "  \"POLICYWRITE\":1,"
                    "  \"POLICY_DELETE\":1,"
                    "  \"WRITELOCKED\":0,"
                    "  \"WRITEALL\":0,"
                    "  \"WRITEDEFINE\":0,"
                    "  \"WRITE_STCLEAR\":0,"
                    "  \"GLOBALLOCK\":0,"
                    "  \"PPREAD\":0,"
                    "  \"OWNERREAD\":1,"
                    "  \"AUTHREAD\":1,"
                    "  \"POLICYREAD\":1,"
                    "  \"NO_DA\":0,"
                    "  \"ORDERLY\":1,"
                    "  \"CLEAR_STCLEAR\":1,"
                    "  \"READLOCKED\":1,"
                    "  \"WRITTEN\":1,"
                    "  \"PLATFORMCREATE\":0,"
                    "  \"READ_STCLEAR\":0,"
                    "  \"TPM2_NT\":\"COUNTER\""
                    "}";

    const char *test_json_TPMA_NV_src_array =\
                    "["
                    "  \"nv_ownerwrite\","
                    "  \"nv_authwrite\","
                    "  \"nv_policywrite\","
                    "  \"nv_policy_delete\","
                    "  \"nv_ownerread\","
                    "  \"nv_authread\","
                    "  \"nv_policyread\","
                    "  \"nv_orderly\","
                    "  \"nv_clear_stclear\","
                    "  \"nv_readlocked\","
                    "  \"nv_written\","
                    "  {"
                    "    \"TPM2_NT\": \"NT_COUNTER\""
                    "  }"
                    "]";

    const char *test_json_TPMA_NV_src_struct =  \
                    "{"
                    "  \"TPMA_NV_OWNERWRITE\":\"YES\","
                    "  \"TPMA_NV_AUTHWRITE\":\"yes\","
                    "  \"TPMA_NV_POLICYWRITE\":\"TPM2_YES\","
                    "  \"TPMA_NV_POLICY_DELETE\":\"tpm2_yes\","
                    "  \"TPMA_NV_OWNERREAD\":\"SET\","
                    "  \"TPMA_NV_AUTHREAD\":\"set\","
                    "  \"TPMA_NV_POLICYREAD\":1,"
                    "  \"TPMA_NV_ORDERLY\":1,"
                    "  \"TPMA_NV_CLEAR_STCLEAR\":1,"
                    "  \"TPMA_NV_READLOCKED\":1,"
                    "  \"TPMA_NV_WRITTEN\":1,"
                    "  \"TPM2_NT\":1"
                    "  }";

    const char *test_json_TPMA_NV_expected2 =    \
                    "{"
                    "  \"PPWRITE\":1,"
                    "  \"OWNERWRITE\":0,"
                    "  \"AUTHWRITE\":0,"
                    "  \"POLICYWRITE\":0,"
                    "  \"POLICY_DELETE\":0,"
                    "  \"WRITELOCKED\":0,"
                    "  \"WRITEALL\":0,"
                    "  \"WRITEDEFINE\":0,"
                    "  \"WRITE_STCLEAR\":0,"
                    "  \"GLOBALLOCK\":0,"
                    "  \"PPREAD\":0,"
                    "  \"OWNERREAD\":0,"
                    "  \"AUTHREAD\":0,"
                    "  \"POLICYREAD\":0,"
                    "  \"NO_DA\":0,"
                    "  \"ORDERLY\":0,"
                    "  \"CLEAR_STCLEAR\":0,"
                    "  \"READLOCKED\":0,"
                    "  \"WRITTEN\":0,"
                    "  \"PLATFORMCREATE\":0,"
                    "  \"READ_STCLEAR\":0,"
                    "  \"TPM2_NT\":\"ORDINARY\""
                    "}";

    CHECK_JSON_SIMPLE(TPMA_NV, test_json_TPMA_NV_src_array, test_json_TPMA_NV_expected);
    CHECK_JSON_SIMPLE(TPMA_NV, test_json_TPMA_NV_src_struct, test_json_TPMA_NV_expected);
    CHECK_JSON_SIMPLE(TPMA_NV, "1", test_json_TPMA_NV_expected2);
}

static void
check_json_policy(void **state)
{
     const char *test_json_policy_nv_src =       \
        "{"
        "  \"description\":\"Description pol_nv\","
        "  \"policyDigests\":["
        "  ],"
        "  \"policyAuthorizations\":["
        "  ],"
        "    \"policy\":["
        "        {"
        "            \"type\": \"POLICYNV\","
        "                   \"nvPath\": \"myNV\","
        "                   \"operandB\": \"01030304\""
        "      }"
        "  ]"
        "}";

       const char *test_json_policy_nv_expected =       \
        "{"
        "  \"description\":\"Description pol_nv\","
        "  \"policyDigests\":["
        "  ],"
        "  \"policyAuthorizations\":["
        "  ],"
        "    \"policy\":["
        "        {"
        "            \"type\": \"POLICYNV\","
        "                   \"nvPath\": \"myNV\","
        "                   \"operandB\": \"01030304\""
        "     }"
        "  ]"
        "}";


//    CHECK_JSON(TPMS_POLICY, test_json_policy_nv_src, test_json_policy_nv_expected);
        {
            TPMS_POLICY out;
            TSS2_RC rc;
            json_object *jso = json_tokener_parse(test_json_policy_nv_src);
            if (!jso) fprintf(stderr, "JSON parsing failed\n");
            assert_non_null(jso);
            rc = ifapi_json_TPMS_POLICY_deserialize (jso, &out);
            if (rc) fprintf(stderr, "Deserialization failed\n");
            assert_int_equal (rc, TSS2_RC_SUCCESS);
            json_object_put(jso);
            jso = NULL;
            rc = ifapi_json_TPMS_POLICY_serialize (&out, &jso);
            assert_int_equal (rc, TSS2_RC_SUCCESS);
            assert_non_null(jso);
            const char *jso_string = json_object_to_json_string_ext(jso, JSON_C_TO_STRING_PRETTY);
            assert_non_null(jso_string);
            char *string1 = normalize(jso_string);
            char *string2 =  normalize(test_json_policy_nv_expected);
            assert_string_equal(string1, string2);
            json_object_put(jso);
            ifapi_cleanup_policy(&out);
            free(string1);
            free(string2);
        }

    const char *test_json_policy_or_src =       \
        "{"
        "  \"description\":\"hareness description\","
        "  \"policyDigests\":["
        "    {"
        "      \"hashAlg\":\"sha256\","
        "      \"digest\":\"59215cb6c21a60e26b2cc479334a021113611903795507c1227659e2aef23d16\""
        "    }"
        "  ],"
        "  \"policy\":["
        "    {"
        "      \"type\":\"POLICYOR\","
        "      \"policyDigests\":["
        "        {"
        "          \"hashAlg\":\"sha256\","
        "          \"digest\":\"59215cb6c21a60e26b2cc479334a021113611903795507c1227659e2aef23d16\""
        "        }"
        "      ],"
        "        \"branches\":["
        "          {"
        "            \"name\":\"branch1\","
        "            \"description\":\"description branch 1\","
        "            \"policy\":["
        "              {"
        "                \"type\":\"POLICYPCR\","
        "                \"policyDigests\":["
        "                  {"
        "                    \"hashAlg\":\"sha256\","
        "                    \"digest\":\"17d552f8e39ad882f6b3c09ae139af59616bf6a63f4093d6d20e9e1b9f7cdb6e\""
        "                  }"
        "                ],"
        "                  \"pcrs\":["
        "                    {"
        "                      \"pcr\":16,"
        "                      \"hashAlg\":\"sha1\","
        "                      \"digest\":\"0000000000000000000000000000000000000000\""
        "                    }"
        "                  ]"
        "              }"
        "            ],"
        "            \"policyDigests\":["
        "              {"
        "                \"hashAlg\":\"sha256\","
        "                \"digest\":\"17d552f8e39ad882f6b3c09ae139af59616bf6a63f4093d6d20e9e1b9f7cdb6e\""
        "              }"
        "            ]"
        "          },"
        "          {"
        "            \"name\":\"branch1\","
        "            \"description\":\"description branch 1\","
        "            \"policy\":["
        "              {"
        "                \"type\":\"POLICYPCR\","
        "                \"policyDigests\":["
        "                  {"
        "                    \"hashAlg\":\"sha256\","
        "                    \"digest\":\"17d552f8e39ad882f6b3c09ae139af59616bf6a63f4093d6d20e9e1b9f7cdb6e\""
        "                  }"
        "                ],"
        "                  \"pcrs\":["
        "                    {"
        "                      \"pcr\":16,"
        "                      \"hashAlg\":\"sha1\","
        "                      \"digest\":\"0000000000000000000000000000000000000000\""
        "                    }"
        "                  ]"
        "              }"
        "            ],"
        "            \"policyDigests\":["
        "              {"
        "                \"hashAlg\":\"sha256\","
        "                \"digest\":\"17d552f8e39ad882f6b3c09ae139af59616bf6a63f4093d6d20e9e1b9f7cdb6e\""
        "              }"
        "            ]"
        "          }"
        "        ]"
        "    }"
        "  ]"
        "}";

    char *test_json_policy_or_expected = strdup(test_json_policy_or_src);
    if (test_json_policy_or_expected == NULL){
        LOG_ERROR("%s", "Out of memory.");
        return;
    }
//    CHECK_JSON(TPMS_POLICY, test_json_policy_or_src, test_json_policy_or_expected);
        {
            TPMS_POLICY out;
            TSS2_RC rc;
            json_object *jso = json_tokener_parse(test_json_policy_or_src);
            if (!jso) fprintf(stderr, "JSON parsing failed\n");
            assert_non_null(jso);
            rc = ifapi_json_TPMS_POLICY_deserialize (jso, &out);
            if (rc) fprintf(stderr, "Deserialization failed\n");
            assert_int_equal (rc, TSS2_RC_SUCCESS);
            json_object_put(jso);
            jso = NULL;
            rc = ifapi_json_TPMS_POLICY_serialize (&out, &jso);
            assert_int_equal (rc, TSS2_RC_SUCCESS);
            assert_non_null(jso);
            const char *jso_string = json_object_to_json_string_ext(jso, JSON_C_TO_STRING_PRETTY);
            assert_non_null(jso_string);
            char *string1 = normalize(jso_string);
            char *string2 =  normalize(test_json_policy_or_expected);
            assert_string_equal(string1, string2);
            json_object_put(jso);
            ifapi_cleanup_policy(&out);
            free(string1);
            free(string2);
        }
    free(test_json_policy_or_expected);
}


static void
check_json_tpm2bs(void **state)
{
    CHECK_JSON(TPM2B_DIGEST, "\"0x0102\"", "\"0102\"");
    CHECK_JSON(TPM2B_DIGEST, "\"0102\"", "\"0102\"");
    CHECK_JSON(TPM2B_DIGEST, "\"caffee\"", "\"caffee\"");
}

static void
check_error(void **state)
{
   /* Value is > then max value for UINT */
    CHECK_ERROR(UINT16, "\"0x10000\"", TSS2_FAPI_RC_BAD_VALUE);
    CHECK_ERROR(UINT32, "\"0x100000000\"", TSS2_FAPI_RC_BAD_VALUE);

    /* Digest/list is too large*/
    CHECK_ERROR(TPM2B_DIGEST, "\"0x0102222222222222222222222222222222222222222222222222222"
                "22222222222222222222222222222222222222222222222222222222222222222222222222222\"",
                TSS2_FAPI_RC_BAD_VALUE);

    /* Illegal values */
    CHECK_ERROR(TPMI_ALG_HASH, "\"sha9999\"", TSS2_FAPI_RC_BAD_VALUE);
    CHECK_ERROR(TPM2B_DIGEST, "\"xxxx\"", TSS2_FAPI_RC_BAD_VALUE);
    CHECK_ERROR(TPM2B_DIGEST, "\"0x010x\"", TSS2_FAPI_RC_BAD_VALUE);

    /*
     * Illegal keys
     */
    const char *test_json_key_err1 =
        /* Without persistent handle */
        "{"
        "  \"objectType\":1,"
        "  \"system\":\"YES\","
        "}";
    CHECK_ERROR_CLEANUP(IFAPI_OBJECT, test_json_key_err1, TSS2_FAPI_RC_BAD_VALUE);

    const char *test_json_key_err2 =
        /* Without public */
        "{"
        "  \"objectType\":1,"
        "  \"system\":\"YES\","
        "  \"persistent_handle\":0,"
        "}";
    CHECK_ERROR_CLEANUP(IFAPI_OBJECT, test_json_key_err2, TSS2_FAPI_RC_BAD_VALUE);

    const char *test_json_key_err3 =
        /* Without serialization */
        "{"
        "  \"objectType\":1,"
        "  \"system\":\"YES\","
        "  \"with_auth\":\"NO\","
        "  \"persistent_handle\":0,"
        "  \"public\":{"
        "    \"size\":122,"
        "    \"publicArea\":{"
        "      \"type\":\"ECC\","
        "      \"nameAlg\":\"sha256\","
        "      \"objectAttributes\":1,"
        "      \"authPolicy\":\"837197674484b3f81a90cc8d46a5d724fd52d76e06520b64f2a1da1b331469aa\","
        "      \"parameters\":{"
        "        \"symmetric\":{"
        "          \"algorithm\":\"AES\","
        "          \"keyBits\":128,"
        "          \"mode\":\"CFB\""
        "        },"
        "        \"scheme\":{"
        "          \"scheme\":\"NULL\""
        "        },"
        "        \"curveID\":\"NIST_P256\","
        "        \"kdf\":{"
        "          \"scheme\":\"NULL\""
        "        }"
        "      },"
        "      \"unique\":{"
        "        \"x\":\"78d926c582566a70eedffcda4fe147e1b24fe624305441167fac483a3079b2e7\","
        "        \"y\":\"8bdc62992c3382e29687114ea0a9e1ac69f91283ae1d018b6d37859731617c3a\""
        "      }"
        "    }"
        "  },"
        "}";
    CHECK_ERROR_CLEANUP(IFAPI_OBJECT, test_json_key_err3, TSS2_FAPI_RC_BAD_VALUE);

    const char *test_json_key_err4 =
        /* Without PolicyInstance */
        "{"
        "  \"objectType\":1,"
        "  \"system\":\"YES\","
        "  \"with_auth\":\"NO\","
        "  \"persistent_handle\":0,"
        "  \"public\":{"
        "    \"size\":122,"
        "    \"publicArea\":{"
        "      \"type\":\"ECC\","
        "      \"nameAlg\":\"sha256\","
        "      \"objectAttributes\":{"
        "        \"fixedTPM\":1,"
        "        \"stClear\":0,"
        "        \"fixedParent\":1,"
        "        \"sensitiveDataOrigin\":1,"
        "        \"userWithAuth\":0,"
        "        \"adminWithPolicy\":1,"
        "        \"noDA\":0,"
        "        \"encryptedDuplication\":0,"
        "        \"restricted\":1,"
        "        \"decrypt\":1,"
        "        \"sign\":0"
        "      },"
        "      \"authPolicy\":\"837197674484b3f81a90cc8d46a5d724fd52d76e06520b64f2a1da1b331469aa\","
        "      \"parameters\":{"
        "        \"symmetric\":{"
        "          \"algorithm\":\"AES\","
        "          \"keyBits\":128,"
        "          \"mode\":\"CFB\""
        "        },"
        "        \"scheme\":{"
        "          \"scheme\":\"NULL\""
        "        },"
        "        \"curveID\":\"NIST_P256\","
        "        \"kdf\":{"
        "          \"scheme\":\"NULL\""
        "        }"
        "      },"
        "      \"unique\":{"
        "        \"x\":\"78d926c582566a70eedffcda4fe147e1b24fe624305441167fac483a3079b2e7\","
        "        \"y\":\"8bdc62992c3382e29687114ea0a9e1ac69f91283ae1d018b6d37859731617c3a\""
        "      }"
        "    }"
        "  },"
        "  \"serialization\":\"\","
        "}";
    CHECK_ERROR_CLEANUP(IFAPI_OBJECT, test_json_key_err4, TSS2_FAPI_RC_BAD_VALUE);

    const char *test_json_key_err5 =
        /* Without certificate */
        "{"
        "  \"objectType\":1,"
        "  \"system\":\"YES\","
        "  \"with_auth\":\"NO\","
        "  \"persistent_handle\":0,"
        "  \"public\":{"
        "    \"size\":122,"
        "    \"publicArea\":{"
        "      \"type\":\"ECC\","
        "      \"nameAlg\":\"sha256\","
        "      \"objectAttributes\":{"
        "        \"fixedTPM\":1,"
        "        \"stClear\":0,"
        "        \"fixedParent\":1,"
        "        \"sensitiveDataOrigin\":1,"
        "        \"userWithAuth\":0,"
        "        \"adminWithPolicy\":1,"
        "        \"noDA\":0,"
        "        \"encryptedDuplication\":0,"
        "        \"restricted\":1,"
        "        \"decrypt\":1,"
        "        \"sign\":0"
        "      },"
        "      \"authPolicy\":\"837197674484b3f81a90cc8d46a5d724fd52d76e06520b64f2a1da1b331469aa\","
        "      \"parameters\":{"
        "        \"symmetric\":{"
        "          \"algorithm\":\"AES\","
        "          \"keyBits\":128,"
        "          \"mode\":\"CFB\""
        "        },"
        "        \"scheme\":{"
        "          \"scheme\":\"NULL\""
        "        },"
        "        \"curveID\":\"NIST_P256\","
        "        \"kdf\":{"
        "          \"scheme\":\"NULL\""
        "        }"
        "      },"
        "      \"unique\":{"
        "        \"x\":\"78d926c582566a70eedffcda4fe147e1b24fe624305441167fac483a3079b2e7\","
        "        \"y\":\"8bdc62992c3382e29687114ea0a9e1ac69f91283ae1d018b6d37859731617c3a\""
        "      }"
        "    }"
        "  },"
        "  \"serialization\":\"\","
        "  \"policyInstance\":\"\","
        "  \"description\":\"\","
        "}";
    CHECK_ERROR_CLEANUP(IFAPI_OBJECT, test_json_key_err5, TSS2_FAPI_RC_BAD_VALUE);

    const char *test_json_key_err6 =
        /* Without description */
        "{"
        "  \"objectType\":1,"
        "  \"system\":\"YES\","
        "  \"with_auth\":\"NO\","
        "  \"persistent_handle\":0,"
        "  \"public\":{"
        "    \"size\":122,"
        "    \"publicArea\":{"
        "      \"type\":\"ECC\","
        "      \"nameAlg\":\"sha256\","
        "      \"objectAttributes\":{"
        "        \"fixedTPM\":1,"
        "        \"stClear\":0,"
        "        \"fixedParent\":1,"
        "        \"sensitiveDataOrigin\":1,"
        "        \"userWithAuth\":0,"
        "        \"adminWithPolicy\":1,"
        "        \"noDA\":0,"
        "        \"encryptedDuplication\":0,"
        "        \"restricted\":1,"
        "        \"decrypt\":1,"
        "        \"sign\":0"
        "      },"
        "      \"authPolicy\":\"837197674484b3f81a90cc8d46a5d724fd52d76e06520b64f2a1da1b331469aa\","
        "      \"parameters\":{"
        "        \"symmetric\":{"
        "          \"algorithm\":\"AES\","
        "          \"keyBits\":128,"
        "          \"mode\":\"CFB\""
        "        },"
        "        \"scheme\":{"
        "          \"scheme\":\"NULL\""
        "        },"
        "        \"curveID\":\"NIST_P256\","
        "        \"kdf\":{"
        "          \"scheme\":\"NULL\""
        "        }"
        "      },"
        "      \"unique\":{"
        "        \"x\":\"78d926c582566a70eedffcda4fe147e1b24fe624305441167fac483a3079b2e7\","
        "        \"y\":\"8bdc62992c3382e29687114ea0a9e1ac69f91283ae1d018b6d37859731617c3a\""
        "      }"
        "    }"
        "  },"
        "  \"serialization\":\"\","
        "  \"policyInstance\":\"\","
        "  \"certificate\":\"\","
        "}";
    CHECK_ERROR_CLEANUP(IFAPI_OBJECT, test_json_key_err6, TSS2_FAPI_RC_BAD_VALUE);

    const char *test_json_key_err7 =
        /* Without signing scheme */
         "{"
         "  \"objectType\":1,"
         "  \"system\":\"YES\","
         "  \"public\":{"
        "    \"size\":122,"
        "    \"publicArea\":{"
        "      \"type\":\"ECC\","
        "      \"nameAlg\":\"sha256\","
        "      \"objectAttributes\":{"
        "        \"fixedTPM\":1,"
        "        \"stClear\":0,"
        "        \"fixedParent\":1,"
        "        \"sensitiveDataOrigin\":1,"
        "        \"userWithAuth\":0,"
        "        \"adminWithPolicy\":1,"
        "        \"noDA\":0,"
        "        \"encryptedDuplication\":0,"
        "        \"restricted\":1,"
        "        \"decrypt\":1,"
        "        \"sign\":0"
        "      },"
        "      \"authPolicy\":\"837197674484b3f81a90cc8d46a5d724fd52d76e06520b64f2a1da1b331469aa\","
        "      \"parameters\":{"
        "        \"symmetric\":{"
        "          \"algorithm\":\"AES\","
        "          \"keyBits\":128,"
        "          \"mode\":\"CFB\""
        "        },"
        "        \"scheme\":{"
        "          \"scheme\":\"NULL\""
        "        },"
        "        \"curveID\":\"NIST_P256\","
        "        \"kdf\":{"
        "          \"scheme\":\"NULL\""
        "        }"
        "      },"
        "      \"unique\":{"
        "        \"x\":\"78d926c582566a70eedffcda4fe147e1b24fe624305441167fac483a3079b2e7\","
        "        \"y\":\"8bdc62992c3382e29687114ea0a9e1ac69f91283ae1d018b6d37859731617c3a\""
        "      }"
        "    }"
        "  },"
         "  \"with_auth\":\"NO\","
         "  \"persistent_handle\":0,"
          "  \"serialization\":\"\","
         "  \"policyInstance\":\"\","
         "  \"certificate\":\"\","
         "  \"description\":\"\","
         "}";
    CHECK_ERROR_CLEANUP(IFAPI_OBJECT, test_json_key_err7, TSS2_FAPI_RC_BAD_VALUE);

      const char *test_json_key_err8 =
        /* Without name */
         "{"
         "  \"objectType\":1,"
         "  \"system\":\"YES\","
         "  \"public\":{"
        "    \"size\":122,"
        "    \"publicArea\":{"
        "      \"type\":\"ECC\","
        "      \"nameAlg\":\"sha256\","
        "      \"objectAttributes\":{"
        "        \"fixedTPM\":1,"
        "        \"stClear\":0,"
        "        \"fixedParent\":1,"
        "        \"sensitiveDataOrigin\":1,"
        "        \"userWithAuth\":0,"
        "        \"adminWithPolicy\":1,"
        "        \"noDA\":0,"
        "        \"encryptedDuplication\":0,"
        "        \"restricted\":1,"
        "        \"decrypt\":1,"
        "        \"sign\":0"
        "      },"
        "      \"authPolicy\":\"837197674484b3f81a90cc8d46a5d724fd52d76e06520b64f2a1da1b331469aa\","
        "      \"parameters\":{"
        "        \"symmetric\":{"
        "          \"algorithm\":\"AES\","
        "          \"keyBits\":128,"
        "          \"mode\":\"CFB\""
        "        },"
        "        \"scheme\":{"
        "          \"scheme\":\"NULL\""
        "        },"
        "        \"curveID\":\"NIST_P256\","
        "        \"kdf\":{"
        "          \"scheme\":\"NULL\""
        "        }"
        "      },"
        "      \"unique\":{"
        "        \"x\":\"78d926c582566a70eedffcda4fe147e1b24fe624305441167fac483a3079b2e7\","
        "        \"y\":\"8bdc62992c3382e29687114ea0a9e1ac69f91283ae1d018b6d37859731617c3a\""
        "      }"
        "    }"
        "  },"
         "  \"with_auth\":\"NO\","
         "  \"persistent_handle\":0,"
          "  \"serialization\":\"\","
         "  \"policyInstance\":\"\","
         "  \"certificate\":\"\","
         "  \"description\":\"\","
          "  \"signing_scheme\":{"
          "    \"scheme\":\"ECDSA\","
          "    \"details\":{"
          "      \"hashAlg\":\"sha256\""
          "    }"
          "  },"
         "}";
    CHECK_ERROR_CLEANUP(IFAPI_OBJECT, test_json_key_err8, TSS2_FAPI_RC_BAD_VALUE);


    const char *test_json_nv_err1 =
        "{"
        "  \"objectType\":2,"
        "  \"system\":\"NO\","
        "  \"with_auth\":\"NO\","
        "  \"nv_object\":true,"
        "  \"hierarchy\":257,"
        "  \"policyInstance\":\"\","
        "  \"description\":\"\","
        "}";

    CHECK_ERROR_CLEANUP(IFAPI_OBJECT, test_json_nv_err1, TSS2_FAPI_RC_BAD_VALUE);

    const char *test_json_nv_err2 =
        "{"
        "  \"objectType\":2,"
        "  \"system\":\"NO\","
        "  \"with_auth\":\"NO\","
        "  \"nv_object\":true,"
        "  \"public\":{"
        "    \"size\":0,"
        "    \"nvPublic\":{"
        "      \"nvIndex\":25165824,"
        "      \"nameAlg\":\"sha256\","
        "      \"attributes\":{"
        "        \"PPWRITE\":0,"
        "        \"OWNERWRITE\":0,"
        "        \"AUTHWRITE\":0,"
        "        \"POLICYWRITE\":1,"
        "        \"POLICY_DELETE\":0,"
        "        \"WRITELOCKED\":0,"
        "        \"WRITEALL\":0,"
        "        \"WRITEDEFINE\":0,"
        "        \"WRITE_STCLEAR\":1,"
        "        \"GLOBALLOCK\":0,"
        "        \"PPREAD\":0,"
        "        \"OWNERREAD\":0,"
        "        \"AUTHREAD\":0,"
        "        \"POLICYREAD\":1,"
        "        \"NO_DA\":1,"
        "        \"ORDERLY\":0,"
        "        \"CLEAR_STCLEAR\":0,"
        "        \"READLOCKED\":0,"
        "        \"WRITTEN\":0,"
        "        \"PLATFORMCREATE\":0,"
        "        \"READ_STCLEAR\":1,"
        "        \"TPM2_NT\":\"ORDINARY\""
        "      },"
        "      \"authPolicy\":\"0000000000000000000000000000000000000000000000000000000000000000\","
        "      \"dataSize\":1200"
        "    }"
        "  },"
        "  \"serialization\":\"018000000022000b59323f518181d5e607ade494f3ecaf7ba552ddc57fde379b3cf8ca82c009257c00000002002e01800000000b820840080020000000000000000000000000000000000000000000000000000000000000000004b0\","
        "  \"policyInstance\":\"\","
        "  \"description\":\"\","
        "}";

    CHECK_ERROR_CLEANUP(IFAPI_OBJECT, test_json_nv_err2, TSS2_FAPI_RC_BAD_VALUE);

    const char *test_json_nv_err3 =
        "{"
        "  \"objectType\":2,"
        "  \"system\":\"NO\","
        "  \"with_auth\":\"NO\","
        "  \"nv_object\":true,"
        "  \"public\":{"
        "    \"size\":0,"
        "    \"nvPublic\":{"
        "      \"nvIndex\":25165824,"
        "      \"nameAlg\":\"sha256\","
        "      \"attributes\":{"
        "        \"PPWRITE\":0,"
        "        \"OWNERWRITE\":0,"
        "        \"AUTHWRITE\":0,"
        "        \"POLICYWRITE\":1,"
        "        \"POLICY_DELETE\":0,"
        "        \"WRITELOCKED\":0,"
        "        \"WRITEALL\":0,"
        "        \"WRITEDEFINE\":0,"
        "        \"WRITE_STCLEAR\":1,"
        "        \"GLOBALLOCK\":0,"
        "        \"PPREAD\":0,"
        "        \"OWNERREAD\":0,"
        "        \"AUTHREAD\":0,"
        "        \"POLICYREAD\":1,"
        "        \"NO_DA\":1,"
        "        \"ORDERLY\":0,"
        "        \"CLEAR_STCLEAR\":0,"
        "        \"READLOCKED\":0,"
        "        \"WRITTEN\":0,"
        "        \"PLATFORMCREATE\":0,"
        "        \"READ_STCLEAR\":1,"
        "        \"TPM2_NT\":\"ORDINARY\""
        "      },"
        "      \"authPolicy\":\"0000000000000000000000000000000000000000000000000000000000000000\","
        "      \"dataSize\":1200"
        "    }"
        "  },"
        "  \"serialization\":\"018000000022000b59323f518181d5e607ade494f3ecaf7ba552ddc57fde379b3cf8ca82c009257c00000002002e01800000000b820840080020000000000000000000000000000000000000000000000000000000000000000004b0\","
        "  \"hierarchy\":257,"
        "  \"description\":\"\","
        "}";
    CHECK_ERROR_CLEANUP(IFAPI_OBJECT, test_json_nv_err3, TSS2_FAPI_RC_BAD_VALUE);
    const char *test_json_nv_err4 =
        "{"
        "  \"objectType\":2,"
        "  \"system\":\"NO\","
        "  \"nv_object\":true,"
        "  \"public\":{"
        "    \"size\":0,"
        "    \"nvPublic\":{"
        "      \"nvIndex\":25165824,"
        "      \"nameAlg\":\"sha256\","
        "      \"attributes\":{"
        "        \"PPWRITE\":0,"
        "        \"OWNERWRITE\":0,"
        "        \"AUTHWRITE\":0,"
        "        \"POLICYWRITE\":1,"
        "        \"POLICY_DELETE\":0,"
        "        \"WRITELOCKED\":0,"
        "        \"WRITEALL\":0,"
        "        \"WRITEDEFINE\":0,"
        "        \"WRITE_STCLEAR\":1,"
        "        \"GLOBALLOCK\":0,"
        "        \"PPREAD\":0,"
        "        \"OWNERREAD\":0,"
        "        \"AUTHREAD\":0,"
        "        \"POLICYREAD\":1,"
        "        \"NO_DA\":1,"
        "        \"ORDERLY\":0,"
        "        \"CLEAR_STCLEAR\":0,"
        "        \"READLOCKED\":0,"
        "        \"WRITTEN\":0,"
        "        \"PLATFORMCREATE\":0,"
        "        \"READ_STCLEAR\":1,"
        "        \"TPM2_NT\":\"ORDINARY\""
        "      },"
        "      \"authPolicy\":\"0000000000000000000000000000000000000000000000000000000000000000\","
        "      \"dataSize\":1200"
        "    }"
        "  },"
        "  \"serialization\":\"018000000022000b59323f518181d5e607ade494f3ecaf7ba552ddc57fde379b3cf8ca82c009257c00000002002e01800000000b820840080020000000000000000000000000000000000000000000000000000000000000000004b0\","
        "  \"hierarchy\":257,"
        "  \"policyInstance\":\"\","
        "}";
    CHECK_ERROR_CLEANUP(IFAPI_OBJECT, test_json_nv_err4, TSS2_FAPI_RC_BAD_VALUE);

    const char *test_json_nv_err5 =
        "{"
        "  \"objectType\":2,"
        "  \"system\":\"NO\","
        "  \"with_auth\":\"NO\","
        "  \"nv_object\":true,"
        "  \"public\":{"
        "    \"size\":0,"
        "    \"nvPublic\":{"
        "      \"nvIndex\":25165824,"
        "      \"nameAlg\":\"sha256\","
        "      \"attributes\":{"
        "        \"PPWRITE\":0,"
        "        \"OWNERWRITE\":0,"
        "        \"AUTHWRITE\":0,"
        "        \"POLICYWRITE\":1,"
        "        \"POLICY_DELETE\":0,"
        "        \"WRITELOCKED\":0,"
        "        \"WRITEALL\":0,"
        "        \"WRITEDEFINE\":0,"
        "        \"WRITE_STCLEAR\":1,"
        "        \"GLOBALLOCK\":0,"
        "        \"PPREAD\":0,"
        "        \"OWNERREAD\":0,"
        "        \"AUTHREAD\":0,"
        "        \"POLICYREAD\":1,"
        "        \"NO_DA\":1,"
        "        \"ORDERLY\":0,"
        "        \"CLEAR_STCLEAR\":0,"
        "        \"READLOCKED\":0,"
        "        \"WRITTEN\":0,"
        "        \"PLATFORMCREATE\":0,"
        "        \"READ_STCLEAR\":1,"
        "        \"TPM2_NT\":\"ORDINARY\""
        "      },"
        "      \"authPolicy\":\"0000000000000000000000000000000000000000000000000000000000000000\","
        "      \"dataSize\":1200"
        "    }"
        "  },"
        "  \"serialization\":\"018000000022000b59323f518181d5e607ade494f3ecaf7ba552ddc57fde379b3cf8ca82c009257c00000002002e01800000000b820840080020000000000000000000000000000000000000000000000000000000000000000004b0\","
        "  \"hierarchy\":257,"
        "  \"description\":\"\","
        "}";
    CHECK_ERROR_CLEANUP(IFAPI_OBJECT, test_json_nv_err5, TSS2_FAPI_RC_BAD_VALUE);

        const char *test_json_attest_err1 =
        "{"
        "    \"magic\":\"VALUE\","
        "    \"type\":\"ATTEST_QUOTE\","
        "    \"qualifiedSigner\":\"000b5adea4e8b49b3f76db36b9442a29e515263e28bbd9e9263843675bb3cf750202\","
        "    \"extraData\":\"6768033e216468247bd031a0a2d9876d79818f8f\","
        "    \"clockInfo\":{"
        "    \"clock\":8048,"
        "    \"resetCount\":639972755,"
        "    \"restartCount\":158941495,"
        "    \"safe\":\"YES\" }"
        "}";
    CHECK_ERROR(TPMS_ATTEST, test_json_attest_err1, TSS2_FAPI_RC_BAD_VALUE);

    const char *test_json_attest_err2 =
        "{"
        "    \"magic\":\"VALUE\","
        "    \"type\":\"ATTEST_QUOTE\","
        "    \"qualifiedSigner\":\"000b5adea4e8b49b3f76db36b9442a29e515263e28bbd9e9263843675bb3cf750202\","
        "    \"extraData\":\"6768033e216468247bd031a0a2d9876d79818f8f\""
        "}";
    CHECK_ERROR(TPMS_ATTEST, test_json_attest_err2, TSS2_FAPI_RC_BAD_VALUE);

    const char *test_json_attest_err3 =
        "{"
        "    \"magic\":\"VALUE\","
        "    \"type\":\"ATTEST_QUOTE\","
        "    \"qualifiedSigner\":\"000b5adea4e8b49b3f76db36b9442a29e515263e28bbd9e9263843675bb3cf750202\","
        "}";
    CHECK_ERROR(TPMS_ATTEST, test_json_attest_err3, TSS2_FAPI_RC_BAD_VALUE);

    const char *test_json_attest_err4 =
        "{"
        "    \"magic\":\"VALUE\","
        "    \"type\":\"ATTEST_QUOTE\","
        "}";
    CHECK_ERROR(TPMS_ATTEST, test_json_attest_err4, TSS2_FAPI_RC_BAD_VALUE);

    const char *test_json_attest_err5 =
        "{"
        "    \"magic\":\"VALUE\","
        "}";
    CHECK_ERROR(TPMS_ATTEST, test_json_attest_err5, TSS2_FAPI_RC_BAD_VALUE);

    const char *test_json_attest_err6 =
        "{"
        "}";
    CHECK_ERROR(TPMS_ATTEST, test_json_attest_err6, TSS2_FAPI_RC_BAD_VALUE);

    const char *test_json_clock_err1 =
        "{"
        "      \"clock\":8048,"
        "      \"resetCount\":639972755,"
        "      \"restartCount\":158941495,"
        "}";

    CHECK_ERROR(TPMS_CLOCK_INFO, test_json_clock_err1, TSS2_FAPI_RC_BAD_VALUE);

    const char *test_json_clock_err2 =
        "{"
        "      \"clock\":8048,"
        "      \"resetCount\":639972755,"
        "}";

    CHECK_ERROR(TPMS_CLOCK_INFO, test_json_clock_err2, TSS2_FAPI_RC_BAD_VALUE);

    const char *test_json_clock_err3 =
        "{"
        "      \"clock\":8048,"
        "}";

    CHECK_ERROR(TPMS_CLOCK_INFO, test_json_clock_err3, TSS2_FAPI_RC_BAD_VALUE);

    const char *test_json_clock_err4 =
        "{"
        "}";

    CHECK_ERROR(TPMS_CLOCK_INFO, test_json_clock_err4, TSS2_FAPI_RC_BAD_VALUE);

    const char *test_json_command_audit_err1 =
        "{"
        "      \"auditCounter\":8048,"
        "      \"digestAlg\":\"sha1\","
        "      \"auditDigest\":\"0102\","
        "}";

    CHECK_ERROR(TPMS_COMMAND_AUDIT_INFO, test_json_command_audit_err1, TSS2_FAPI_RC_BAD_VALUE);

    const char *test_json_command_audit_err2 =
        "{"
        "      \"auditCounter\":8048,"
        "      \"digestAlg\":\"sha1\","
        "}";

    CHECK_ERROR(TPMS_COMMAND_AUDIT_INFO, test_json_command_audit_err2, TSS2_FAPI_RC_BAD_VALUE);

    const char *test_json_command_audit_err3 =
        "{"
        "      \"auditCounter\":8048,"
        "}";

    CHECK_ERROR(TPMS_COMMAND_AUDIT_INFO, test_json_command_audit_err3, TSS2_FAPI_RC_BAD_VALUE);
      const char *test_json_command_audit_err4 =
        "{"
        "}";

    CHECK_ERROR(TPMS_COMMAND_AUDIT_INFO, test_json_command_audit_err4, TSS2_FAPI_RC_BAD_VALUE);

    const char *test_json_tk_creation_err1 =
        "{"
        "      \"tag\":\"NULL\","
        "      \"hierarchy\":\"OWNER\","
        "}";

    CHECK_ERROR(TPMT_TK_CREATION, test_json_tk_creation_err1, TSS2_FAPI_RC_BAD_VALUE);

    const char *test_json_tk_creation_err2 =
        "{"
        "      \"tag\":\"NULL\","
        "}";

    CHECK_ERROR(TPMT_TK_CREATION, test_json_tk_creation_err2, TSS2_FAPI_RC_BAD_VALUE);

    const char *test_json_tk_creation_err3 =
        "{"
        "}";

    CHECK_ERROR(TPMT_TK_CREATION, test_json_tk_creation_err3, TSS2_FAPI_RC_BAD_VALUE);

    const char *test_json_nv_certify_info_err1 =
        "{"
        "      \"indexName\":\"0102\","
        "      \"offset\":0,"
        "}";

    CHECK_ERROR(TPMS_NV_CERTIFY_INFO, test_json_nv_certify_info_err1, TSS2_FAPI_RC_BAD_VALUE);

    const char *test_json_nv_certify_info_err2 =
        "{"
        "      \"indexName\":\"0102\","
        "}";

    CHECK_ERROR(TPMS_NV_CERTIFY_INFO, test_json_nv_certify_info_err2, TSS2_FAPI_RC_BAD_VALUE);
    const char *test_json_nv_certify_info_err3 =
        "{"
        "}";

    CHECK_ERROR(TPMS_NV_CERTIFY_INFO, test_json_nv_certify_info_err3, TSS2_FAPI_RC_BAD_VALUE);


    const char *test_json_signature_ecc_err1 =
        "{"
        "      \"hash\":\"sha1\","
        "      \"signatureR\":\"0102\","
        "}";

    CHECK_ERROR(TPMS_SIGNATURE_ECC, test_json_signature_ecc_err1, TSS2_FAPI_RC_BAD_VALUE);

    const char *test_json_signature_ecc_err2 =
        "{"
        "      \"hash\":\"sha1\","
        "}";

    CHECK_ERROR(TPMS_SIGNATURE_ECC, test_json_signature_ecc_err2, TSS2_FAPI_RC_BAD_VALUE);

    const char *test_json_signature_ecc_err4 =
        "{"
        "}";

    CHECK_ERROR(TPMS_SIGNATURE_ECC, test_json_signature_ecc_err4, TSS2_FAPI_RC_BAD_VALUE);

    const char *test_json_signature_err1 =
        "{"
        "      \"sigAlg\":\"HMAC\","
        "      \"signature\":\"0102\","
        "}";

    CHECK_ERROR(TPMT_SIGNATURE, test_json_signature_err1, TSS2_FAPI_RC_BAD_VALUE);

    const char *test_json_signature_err2 =
        "{"
        "      \"sigAlg\":\"ECDSA\","
        "      \"signature\":\"0102\","
        "}";

    CHECK_ERROR(TPMT_SIGNATURE, test_json_signature_err2, TSS2_FAPI_RC_BAD_VALUE);

    const char *test_json_signature_err3 =
        "{"
        "      \"sigAlg\":\"ECDAA\","
        "      \"signature\":\"0102\","
        "}";

    CHECK_ERROR(TPMT_SIGNATURE, test_json_signature_err3, TSS2_FAPI_RC_BAD_VALUE);

    const char *test_json_signature_err4 =
        "{"
        "      \"sigAlg\":\"SM2\","
        "      \"signature\":\"0102\","
        "}";

    CHECK_ERROR(TPMT_SIGNATURE, test_json_signature_err4, TSS2_FAPI_RC_BAD_VALUE);

    const char *test_json_signature_err5 =
        "{"
        "      \"sigAlg\":\"ECSCHNORR\","
        "      \"signature\":\"0102\","
        "}";

    CHECK_ERROR(TPMT_SIGNATURE, test_json_signature_err5, TSS2_FAPI_RC_BAD_VALUE);

    const char *test_json_signature_err6 =
        "{"
        "      \"sigAlg\":\"RSASSA\","
        "      \"signature\":\"0102\","
        "}";

    CHECK_ERROR(TPMT_SIGNATURE, test_json_signature_err6, TSS2_FAPI_RC_BAD_VALUE);

    const char *test_json_signature_err7 =
        "{"
        "}";

    CHECK_ERROR(TPMT_SIGNATURE, test_json_signature_err7, TSS2_FAPI_RC_BAD_VALUE);

    const char *test_json_signature_err8 =
        "{"
        "      \"sigAlg\":\"RSASSA\","
        "}";

    CHECK_ERROR(TPMT_SIGNATURE, test_json_signature_err8, TSS2_FAPI_RC_BAD_VALUE);
}

static void
check_tpmjson_tofromtxt(void **state)
{
    const char *testcase_alg_id[] = { "\"TPM_ALG_ID_SHA1\"", "\"TPM2_ALG_ID_SHA1\"",
                                      "\"ALG_ID_SHA1\"", "\"sha1\"", "\"ALG_SHA1\"",
                                      "\"tpm2_alg_id_sha1\"", "\"sha1\"", "\"0x0004\"" };
    const char *expected_ald_id = { "\"sha1\"" };
    for (size_t i = 0; i < sizeof(testcase_alg_id) / sizeof(testcase_alg_id[0]); i++) {
        CHECK_JSON_SIMPLE(TPM2_ALG_ID, testcase_alg_id[i], expected_ald_id);
    }

    const char *testcase_ecc_curve[] = { "\"TPM2_ECC_NIST_P256\"", "\"ECC_NIST_P256\"",
                                         "\"NIST_P256\"", "\"0x0003\"", "\"nist_p256\"" };
    const char *expected_ecc_curve = { "\"NIST_P256\"" };
    for (size_t i = 0; i < sizeof(testcase_ecc_curve) / sizeof(testcase_ecc_curve[0]); i++) {
        CHECK_JSON_SIMPLE(TPM2_ECC_CURVE, testcase_ecc_curve[i], expected_ecc_curve);
    }

    const char *testcase_cc[] = { "\"TPM2_CC_Startup\"", "\"CC_Startup\"",
                                  "\"Startup\"", "\"0x00000144\"" };
    const char *expected_cc = { "\"Startup\"" };
    for (size_t i = 0; i < sizeof(testcase_cc) / sizeof(testcase_cc[0]); i++) {
        CHECK_JSON_SIMPLE(TPM2_CC, testcase_cc[i], expected_cc);
    }

    const char *testcase_eo[] = { "\"TPM2_EO_EQ\"", "\"EO_EQ\"",
                                  "\"EQ\"", "\"0x0000\"" };
    const char *expected_eo = { "\"EQ\"" };
    for (size_t i = 0; i < sizeof(testcase_eo) / sizeof(testcase_eo[0]); i++) {
        CHECK_JSON_SIMPLE(TPM2_EO, testcase_eo[i], expected_eo);
    }

    const char *testcase_st[] = { "\"TPM2_ST_NO_SESSIONS\"", "\"ST_NO_SESSIONS\"",
                                  "\"no_SESSIONS\"", "\"0x8001\"" };
    const char *expected_st = { "\"NO_SESSIONS\"" };
    for (size_t i = 0; i < sizeof(testcase_st) / sizeof(testcase_st[0]); i++) {
        CHECK_JSON_SIMPLE(TPM2_ST, testcase_st[i], expected_st);
    }

    const char *testcase_pt_pcr[] = { "\"TPM2_PT_PCR_EXTEND_L0\"", "\"PT_PCR_EXTEND_L0\"",
                                  "\"PCR_EXTEND_L0\"", "\"EXTEND_L0\"" };
    const char *expected_pt_pcr = { "\"EXTEND_L0\"" };
    for (size_t i = 0; i < sizeof(testcase_pt_pcr) / sizeof(testcase_pt_pcr[0]); i++) {
        CHECK_JSON_SIMPLE(TPM2_PT_PCR, testcase_pt_pcr[i], expected_pt_pcr);
    }

    const char *testcase_alg_public[] = { "\"TPM2_ALG_RSA\"", "\"ALG_RSA\"",
                                          "\"RSA\"", "\"0x0001\"" };
    const char *expected_alg_public = { "\"RSA\"" };
    for (size_t i = 0; i < sizeof(testcase_alg_public) / sizeof(testcase_alg_public[0]); i++) {
        CHECK_JSON_SIMPLE(TPMI_ALG_PUBLIC, testcase_alg_public[i], expected_alg_public);
    }
}

static void
check_invalid_json(void **state) {
      json_object *jso = ifapi_parse_json("{\n \"field\", \"value\"");
      assert_null(jso);
}

int
main(int argc, char *argv[])
{
    const struct CMUnitTest tests[] = {
        cmocka_unit_test(check_tpmjson_tofromtxt),
        cmocka_unit_test(check_json_structs),
        cmocka_unit_test(check_json_constants),
        cmocka_unit_test(check_json_numbers),
        cmocka_unit_test(check_json_bits),
        cmocka_unit_test(check_json_tpm2bs),
        cmocka_unit_test(check_json_to_bin),
        cmocka_unit_test(check_bin),
        cmocka_unit_test(check_policy_bin),
        cmocka_unit_test(check_error),
        cmocka_unit_test(check_json_policy),
        cmocka_unit_test(check_invalid_json),
    };
    return cmocka_run_group_tests(tests, NULL, NULL);
}
