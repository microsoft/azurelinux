/* SPDX-License-Identifier: BSD-2-Clause */
/*******************************************************************************
 * Copyright 2018-2019, Fraunhofer SIT sponsored by Infineon Technologies AG
 * All rights reserved.
 ******************************************************************************/
#ifndef FAPI_TPM_JSON_DESERIALIZE_H
#define FAPI_TPM_JSON_DESERIALIZE_H

#include <stdbool.h>
#include <json-c/json.h>
#include <json-c/json_util.h>

#include "tss2_tpm2_types.h"
#include "fapi_int.h"
#define YES 1
#define NO 0

/* Deserialize according to the rules of parenttype and then filter against values
   provided in the ... list. */
#define SUBTYPE_FILTER(type, parenttype, ...) \
    TSS2_RC r; \
    type tab[] = { __VA_ARGS__ }; \
    type v; \
    r = ifapi_json_ ## parenttype ## _deserialize(jso, &v); \
    return_if_error(r, "Bad value"); \
    for (size_t i = 0; i < sizeof(tab) / sizeof(tab[0]); i++) { \
        if (v == tab[i]) { \
            *out = v; \
            return TSS2_RC_SUCCESS; \
        } \
    } \
    LOG_ERROR("Bad sub-value"); \
    return TSS2_FAPI_RC_BAD_VALUE;

json_object*
ifapi_parse_json(const char *jstring) ;

TSS2_RC
ifapi_hex_to_byte_ary(const char hex[], UINT32 vlen, BYTE val[]);

TSS2_RC
ifapi_json_BYTE_array_deserialize(size_t max, json_object *jso, BYTE *out);

TSS2_RC
ifapi_json_UINT8_ARY_deserialize(json_object *jso, UINT8_ARY *out);

bool
ifapi_get_sub_object(json_object *jso, char *name, json_object **sub_jso);

TSS2_RC
ifapi_json_BYTE_deserialize(json_object *jso, BYTE *out);

TSS2_RC
ifapi_json_UINT16_deserialize(json_object *jso, UINT16 *out);

TSS2_RC
ifapi_json_UINT32_deserialize(json_object *jso, UINT32 *out);

TSS2_RC
ifapi_json_UINT64_deserialize(json_object *jso, UINT64 *out);

TSS2_RC
ifapi_json_TPM2_GENERATED_deserialize(json_object *jso, TPM2_GENERATED *out);

TSS2_RC
ifapi_json_TPM2_ALG_ID_deserialize(json_object *jso, TPM2_ALG_ID *out);

TSS2_RC
ifapi_json_TPM2_ECC_CURVE_deserialize(json_object *jso, TPM2_ECC_CURVE *out);

TSS2_RC
ifapi_json_TPM2_CC_deserialize(json_object *jso, TPM2_CC *out);

TSS2_RC
ifapi_json_TPM2_EO_deserialize(json_object *jso, TPM2_EO *out);

TSS2_RC
ifapi_json_TPM2_ST_deserialize(json_object *jso, TPM2_ST *out);

TSS2_RC
ifapi_json_TPM2_PT_PCR_deserialize(json_object *jso, TPM2_PT_PCR *out);

TSS2_RC
ifapi_json_TPM2_HANDLE_deserialize(json_object *jso, TPM2_HANDLE *out);

TSS2_RC
ifapi_json_TPMA_OBJECT_deserialize(json_object *jso, TPMA_OBJECT *out);

TSS2_RC
ifapi_json_TPMA_LOCALITY_deserialize(json_object *jso, TPMA_LOCALITY *out);

TSS2_RC
ifapi_json_TPMA_ACT_deserialize(json_object *jso, TPMA_ACT *out);

TSS2_RC
ifapi_json_TPMI_YES_NO_deserialize(json_object *jso, TPMI_YES_NO *out);

TSS2_RC
ifapi_json_TPMI_RH_HIERARCHY_deserialize(json_object *jso,
        TPMI_RH_HIERARCHY *out);

TSS2_RC
ifapi_json_TPMI_RH_NV_INDEX_deserialize(json_object *jso,
                                        TPMI_RH_NV_INDEX *out);

TSS2_RC
ifapi_json_TPMI_ALG_HASH_deserialize(json_object *jso, TPMI_ALG_HASH *out);

TSS2_RC
ifapi_json_TPMI_ALG_SYM_deserialize(json_object *jso, TPMI_ALG_SYM *out);

TSS2_RC
ifapi_json_TPMI_ALG_SYM_OBJECT_deserialize(json_object *jso,
        TPMI_ALG_SYM_OBJECT *out);

TSS2_RC
ifapi_json_TPMI_ALG_CIPHER_MODE_deserialize(json_object *jso,
        TPMI_ALG_CIPHER_MODE *out);

TSS2_RC
ifapi_json_TPMI_ALG_SYM_MODE_deserialize(json_object *jso,
        TPMI_ALG_SYM_MODE *out);

TSS2_RC
ifapi_json_TPMI_ALG_KDF_deserialize(json_object *jso, TPMI_ALG_KDF *out);

TSS2_RC
ifapi_json_TPMI_ALG_SIG_SCHEME_deserialize(json_object *jso,
        TPMI_ALG_SIG_SCHEME *out);

TSS2_RC
ifapi_json_TPMS_EMPTY_deserialize(json_object *jso, TPMS_EMPTY *out);

TSS2_RC
ifapi_json_TPMU_HA_deserialize(UINT32 selector, json_object *jso, TPMU_HA *out);

TSS2_RC
ifapi_json_TPMT_HA_deserialize(json_object *jso, TPMT_HA *out);

TSS2_RC
ifapi_json_TPM2B_DIGEST_deserialize(json_object *jso, TPM2B_DIGEST *out);

TSS2_RC
ifapi_json_TPM2B_DATA_deserialize(json_object *jso, TPM2B_DATA *out);

TSS2_RC
ifapi_json_TPM2B_NONCE_deserialize(json_object *jso, TPM2B_NONCE *out);

TSS2_RC
ifapi_json_TPM2B_OPERAND_deserialize(json_object *jso, TPM2B_OPERAND *out);

TSS2_RC
ifapi_json_TPM2B_EVENT_deserialize(json_object *jso, TPM2B_EVENT *out);

TSS2_RC
ifapi_json_TPM2B_MAX_NV_BUFFER_deserialize(json_object *jso,
        TPM2B_MAX_NV_BUFFER *out);

TSS2_RC
ifapi_json_TPM2B_NAME_deserialize(json_object *jso, TPM2B_NAME *out);

TSS2_RC
ifapi_json_TPMS_PCR_SELECT_deserialize(json_object *jso, TPMS_PCR_SELECT *out);

TSS2_RC
ifapi_json_TPMS_PCR_SELECTION_deserialize(json_object *jso,
        TPMS_PCR_SELECTION *out);

TSS2_RC
ifapi_json_TPMS_TAGGED_POLICY_deserialize(json_object *jso,
        TPMS_TAGGED_POLICY *out);

TSS2_RC
ifapi_json_TPMS_ACT_DATA_deserialize(json_object *jso,
        TPMS_ACT_DATA *out);

TSS2_RC
ifapi_json_TPMT_TK_CREATION_deserialize(json_object *jso,
                                        TPMT_TK_CREATION *out);

TSS2_RC
ifapi_json_TPML_DIGEST_VALUES_deserialize(json_object *jso,
        TPML_DIGEST_VALUES *out);

TSS2_RC
ifapi_json_TPML_PCR_SELECTION_deserialize(json_object *jso,
        TPML_PCR_SELECTION *out);

TSS2_RC
ifapi_json_TPMS_CLOCK_INFO_deserialize(json_object *jso, TPMS_CLOCK_INFO *out);

TSS2_RC
ifapi_json_TPMS_TIME_INFO_deserialize(json_object *jso, TPMS_TIME_INFO *out);

TSS2_RC
ifapi_json_TPMS_TIME_ATTEST_INFO_deserialize(json_object *jso,
        TPMS_TIME_ATTEST_INFO *out);

TSS2_RC
ifapi_json_TPMS_CERTIFY_INFO_deserialize(json_object *jso,
        TPMS_CERTIFY_INFO *out);

TSS2_RC
ifapi_json_TPMS_QUOTE_INFO_deserialize(json_object *jso, TPMS_QUOTE_INFO *out);

TSS2_RC
ifapi_json_TPMS_COMMAND_AUDIT_INFO_deserialize(json_object *jso,
        TPMS_COMMAND_AUDIT_INFO *out);

TSS2_RC
ifapi_json_TPMS_SESSION_AUDIT_INFO_deserialize(json_object *jso,
        TPMS_SESSION_AUDIT_INFO *out);

TSS2_RC
ifapi_json_TPMS_CREATION_INFO_deserialize(json_object *jso,
        TPMS_CREATION_INFO *out);

TSS2_RC
ifapi_json_TPMS_NV_CERTIFY_INFO_deserialize(json_object *jso,
        TPMS_NV_CERTIFY_INFO *out);

TSS2_RC
ifapi_json_TPMI_ST_ATTEST_deserialize(json_object *jso, TPMI_ST_ATTEST *out);

TSS2_RC
ifapi_json_TPMU_ATTEST_deserialize(UINT32 selector, json_object *jso,
                                   TPMU_ATTEST *out);

TSS2_RC
ifapi_json_TPMS_ATTEST_deserialize(json_object *jso, TPMS_ATTEST *out);

TSS2_RC
ifapi_json_TPMI_AES_KEY_BITS_deserialize(json_object *jso,
        TPMI_AES_KEY_BITS *out);

TSS2_RC
ifapi_json_TPMU_SYM_KEY_BITS_deserialize(UINT32 selector, json_object *jso,
        TPMU_SYM_KEY_BITS *out);

TSS2_RC
ifapi_json_TPMU_SYM_MODE_deserialize(UINT32 selector, json_object *jso,
                                     TPMU_SYM_MODE *out);

TSS2_RC
ifapi_json_TPMT_SYM_DEF_deserialize(json_object *jso, TPMT_SYM_DEF *out);

TSS2_RC
ifapi_json_TPMT_SYM_DEF_OBJECT_deserialize(json_object *jso,
        TPMT_SYM_DEF_OBJECT *out);

TSS2_RC
ifapi_json_TPMS_SYMCIPHER_PARMS_deserialize(json_object *jso,
        TPMS_SYMCIPHER_PARMS *out);

TSS2_RC
ifapi_json_TPMS_SCHEME_HASH_deserialize(json_object *jso,
                                        TPMS_SCHEME_HASH *out);

TSS2_RC
ifapi_json_TPMS_SCHEME_ECDAA_deserialize(json_object *jso,
        TPMS_SCHEME_ECDAA *out);

TSS2_RC
ifapi_json_TPMI_ALG_KEYEDHASH_SCHEME_deserialize(json_object *jso,
        TPMI_ALG_KEYEDHASH_SCHEME *out);

TSS2_RC
ifapi_json_TPMS_SCHEME_HMAC_deserialize(json_object *jso,
                                        TPMS_SCHEME_HMAC *out);

TSS2_RC
ifapi_json_TPMS_SCHEME_XOR_deserialize(json_object *jso, TPMS_SCHEME_XOR *out);

TSS2_RC
ifapi_json_TPMU_SCHEME_KEYEDHASH_deserialize(UINT32 selector, json_object *jso,
        TPMU_SCHEME_KEYEDHASH *out);

TSS2_RC
ifapi_json_TPMT_KEYEDHASH_SCHEME_deserialize(json_object *jso,
        TPMT_KEYEDHASH_SCHEME *out);

TSS2_RC
ifapi_json_TPMS_SIG_SCHEME_RSASSA_deserialize(json_object *jso,
        TPMS_SIG_SCHEME_RSASSA *out);

TSS2_RC
ifapi_json_TPMS_SIG_SCHEME_RSAPSS_deserialize(json_object *jso,
        TPMS_SIG_SCHEME_RSAPSS *out);

TSS2_RC
ifapi_json_TPMS_SIG_SCHEME_ECDSA_deserialize(json_object *jso,
        TPMS_SIG_SCHEME_ECDSA *out);

TSS2_RC
ifapi_json_TPMS_SIG_SCHEME_SM2_deserialize(json_object *jso,
        TPMS_SIG_SCHEME_SM2 *out);

TSS2_RC
ifapi_json_TPMS_SIG_SCHEME_ECSCHNORR_deserialize(json_object *jso,
        TPMS_SIG_SCHEME_ECSCHNORR *out);

TSS2_RC
ifapi_json_TPMS_SIG_SCHEME_ECDAA_deserialize(json_object *jso,
        TPMS_SIG_SCHEME_ECDAA *out);

TSS2_RC
ifapi_json_TPMU_SIG_SCHEME_deserialize(UINT32 selector, json_object *jso,
                                       TPMU_SIG_SCHEME *out);

TSS2_RC
ifapi_json_TPMT_SIG_SCHEME_deserialize(json_object *jso, TPMT_SIG_SCHEME *out);

TSS2_RC
ifapi_json_TPMS_ENC_SCHEME_OAEP_deserialize(json_object *jso,
        TPMS_ENC_SCHEME_OAEP *out);

TSS2_RC
ifapi_json_TPMS_ENC_SCHEME_RSAES_deserialize(json_object *jso,
        TPMS_ENC_SCHEME_RSAES *out);

TSS2_RC
ifapi_json_TPMS_KEY_SCHEME_ECDH_deserialize(json_object *jso,
        TPMS_KEY_SCHEME_ECDH *out);

TSS2_RC
ifapi_json_TPMS_SCHEME_MGF1_deserialize(json_object *jso,
                                        TPMS_SCHEME_MGF1 *out);

TSS2_RC
ifapi_json_TPMS_SCHEME_KDF1_SP800_56A_deserialize(json_object *jso,
        TPMS_SCHEME_KDF1_SP800_56A *out);

TSS2_RC
ifapi_json_TPMS_SCHEME_KDF1_SP800_108_deserialize(json_object *jso,
        TPMS_SCHEME_KDF1_SP800_108 *out);

TSS2_RC
ifapi_json_TPMU_KDF_SCHEME_deserialize(UINT32 selector, json_object *jso,
                                       TPMU_KDF_SCHEME *out);

TSS2_RC
ifapi_json_TPMT_KDF_SCHEME_deserialize(json_object *jso, TPMT_KDF_SCHEME *out);

TSS2_RC
ifapi_json_TPMU_ASYM_SCHEME_deserialize(UINT32 selector, json_object *jso,
                                        TPMU_ASYM_SCHEME *out);

TSS2_RC
ifapi_json_TPMI_ALG_RSA_SCHEME_deserialize(json_object *jso,
        TPMI_ALG_RSA_SCHEME *out);

TSS2_RC
ifapi_json_TPMT_RSA_SCHEME_deserialize(json_object *jso, TPMT_RSA_SCHEME *out);

TSS2_RC
ifapi_json_TPMI_ALG_RSA_DECRYPT_deserialize(json_object *jso,
        TPMI_ALG_RSA_DECRYPT *out);

TSS2_RC
ifapi_json_TPMT_RSA_DECRYPT_deserialize(json_object *jso,
                                        TPMT_RSA_DECRYPT *out);

TSS2_RC
ifapi_json_TPM2B_PUBLIC_KEY_RSA_deserialize(json_object *jso,
        TPM2B_PUBLIC_KEY_RSA *out);

TSS2_RC
ifapi_json_TPMI_RSA_KEY_BITS_deserialize(json_object *jso,
        TPMI_RSA_KEY_BITS *out);

TSS2_RC
ifapi_json_TPM2B_ECC_PARAMETER_deserialize(json_object *jso,
        TPM2B_ECC_PARAMETER *out);

TSS2_RC
ifapi_json_TPMS_ECC_POINT_deserialize(json_object *jso, TPMS_ECC_POINT *out);

TSS2_RC
ifapi_json_TPMI_ALG_ECC_SCHEME_deserialize(json_object *jso,
        TPMI_ALG_ECC_SCHEME *out);

TSS2_RC
ifapi_json_TPMI_ECC_CURVE_deserialize(json_object *jso, TPMI_ECC_CURVE *out);

TSS2_RC
ifapi_json_TPMT_ECC_SCHEME_deserialize(json_object *jso, TPMT_ECC_SCHEME *out);

TSS2_RC
ifapi_json_TPMS_SIGNATURE_RSA_deserialize(json_object *jso,
        TPMS_SIGNATURE_RSA *out);

TSS2_RC
ifapi_json_TPMS_SIGNATURE_RSASSA_deserialize(json_object *jso,
        TPMS_SIGNATURE_RSASSA *out);

TSS2_RC
ifapi_json_TPMS_SIGNATURE_RSAPSS_deserialize(json_object *jso,
        TPMS_SIGNATURE_RSAPSS *out);

TSS2_RC
ifapi_json_TPMS_SIGNATURE_ECC_deserialize(json_object *jso,
        TPMS_SIGNATURE_ECC *out);

TSS2_RC
ifapi_json_TPMS_SIGNATURE_ECDSA_deserialize(json_object *jso,
        TPMS_SIGNATURE_ECDSA *out);

TSS2_RC
ifapi_json_TPMS_SIGNATURE_ECDAA_deserialize(json_object *jso,
        TPMS_SIGNATURE_ECDAA *out);

TSS2_RC
ifapi_json_TPMS_SIGNATURE_SM2_deserialize(json_object *jso,
        TPMS_SIGNATURE_SM2 *out);

TSS2_RC
ifapi_json_TPMS_SIGNATURE_ECSCHNORR_deserialize(json_object *jso,
        TPMS_SIGNATURE_ECSCHNORR *out);

TSS2_RC
ifapi_json_TPMU_SIGNATURE_deserialize(UINT32 selector, json_object *jso,
                                      TPMU_SIGNATURE *out);

TSS2_RC
ifapi_json_TPMT_SIGNATURE_deserialize(json_object *jso, TPMT_SIGNATURE *out);

TSS2_RC
ifapi_json_TPM2B_ENCRYPTED_SECRET_deserialize(json_object *jso,
        TPM2B_ENCRYPTED_SECRET *out);

TSS2_RC
ifapi_json_TPMI_ALG_PUBLIC_deserialize(json_object *jso, TPMI_ALG_PUBLIC *out);

TSS2_RC
ifapi_json_TPMU_PUBLIC_ID_deserialize(UINT32 selector, json_object *jso,
                                      TPMU_PUBLIC_ID *out);

TSS2_RC
ifapi_json_TPMS_KEYEDHASH_PARMS_deserialize(json_object *jso,
        TPMS_KEYEDHASH_PARMS *out);

TSS2_RC
ifapi_json_TPMS_RSA_PARMS_deserialize(json_object *jso, TPMS_RSA_PARMS *out);

TSS2_RC
ifapi_json_TPMS_ECC_PARMS_deserialize(json_object *jso, TPMS_ECC_PARMS *out);

TSS2_RC
ifapi_json_TPMU_PUBLIC_PARMS_deserialize(UINT32 selector, json_object *jso,
        TPMU_PUBLIC_PARMS *out);

TSS2_RC
ifapi_json_TPMT_PUBLIC_deserialize(json_object *jso, TPMT_PUBLIC *out);

TSS2_RC
ifapi_json_TPM2B_PUBLIC_deserialize(json_object *jso, TPM2B_PUBLIC *out);

TSS2_RC
ifapi_json_TPM2B_PRIVATE_deserialize(json_object *jso, TPM2B_PRIVATE *out);

TSS2_RC
ifapi_json_TPM2_NT_deserialize(json_object *jso, TPM2_NT *out);

TSS2_RC
ifapi_json_TPMA_NV_deserialize(json_object *jso, TPMA_NV *out);

TSS2_RC
ifapi_json_TPMS_NV_PUBLIC_deserialize(json_object *jso, TPMS_NV_PUBLIC *out);

TSS2_RC
ifapi_json_TPM2B_NV_PUBLIC_deserialize(json_object *jso, TPM2B_NV_PUBLIC *out);

TSS2_RC
ifapi_json_TPMS_CREATION_DATA_deserialize(json_object *jso,
        TPMS_CREATION_DATA *out);

TSS2_RC
ifapi_json_TPM2B_CREATION_DATA_deserialize(json_object *jso,
        TPM2B_CREATION_DATA *out);

#endif /* FAPI_TPM_JSON_DESERIALIZE_H */
