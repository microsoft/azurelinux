/* SPDX-License-Identifier: BSD-2-Clause */
/*******************************************************************************
 * Copyright 2018-2019, Fraunhofer SIT sponsored by Infineon Technologies AG
 * All rights reserved.
 ******************************************************************************/
#ifndef FAPI_TPM_JSON_SERIALIZE_H
#define FAPI_TPM_JSON_SERIALIZE_H

#include <stdbool.h>
#include <json-c/json.h>
#include <json-c/json_util.h>

#include "tss2_tpm2_types.h"
#include "fapi_int.h"

#define YES 1
#define NO 0

#define CHECK_IN_LIST(type, needle, ...) \
    type tab[] = { __VA_ARGS__ }; \
    size_t i; \
    for(i = 0; i < sizeof(tab) / sizeof(tab[0]); i++) \
        if (needle == tab[i]) \
            break; \
    if (i == sizeof(tab) / sizeof(tab[0])) { \
        LOG_ERROR("Bad value"); \
        return TSS2_FAPI_RC_BAD_VALUE; \
    }

#define JSON_CLEAR(jso) \
    if (jso) {                   \
        json_object_put(jso); \
    }

#define return_if_jso_error(r,msg, jso)       \
    if (r != TSS2_RC_SUCCESS) { \
        LOG_ERROR("%s " TPM2_ERROR_FORMAT, msg, TPM2_ERROR_TEXT(r)); \
        if (jso) {                                                   \
            json_object_put(jso);                                    \
        } \
        return r;  \
    }

TSS2_RC
ifapi_json_TPM2_HANDLE_serialize(const TPM2_HANDLE in, json_object **jso);

TSS2_RC
ifapi_json_UINT16_serialize(const UINT16 in, json_object **jso);

TSS2_RC
ifapi_json_UINT32_serialize(const UINT32 in, json_object **jso);

TSS2_RC
ifapi_json_INT32_serialize(const INT32 in, json_object **jso);

TSS2_RC
ifapi_json_UINT64_serialize(const UINT64 in, json_object **jso);

TSS2_RC
ifapi_json_TPM2_GENERATED_serialize(const TPM2_GENERATED in, json_object **jso);

TSS2_RC
ifapi_json_TPM2_ALG_ID_serialize(const TPM2_ALG_ID in, json_object **jso);

TSS2_RC
ifapi_json_TPM2_ECC_CURVE_serialize(const TPM2_ECC_CURVE in, json_object **jso);

TSS2_RC
ifapi_json_TPM2_CC_serialize(const TPM2_CC in, json_object **jso);

TSS2_RC
ifapi_json_TPM2_EO_serialize(const TPM2_EO in, json_object **jso);

TSS2_RC
ifapi_json_TPM2_ST_serialize(const TPM2_ST in, json_object **jso);

TSS2_RC
ifapi_json_TPM2_CAP_serialize(const TPM2_CAP in, json_object **jso);

TSS2_RC
ifapi_json_TPM2_PT_serialize(const TPM2_PT in, json_object **jso);

TSS2_RC
ifapi_json_TPM2_PT_PCR_serialize(const TPM2_PT_PCR in, json_object **jso);

TSS2_RC
ifapi_json_TPMA_ALGORITHM_serialize(const TPMA_ALGORITHM in, json_object **jso);

TSS2_RC
ifapi_json_TPMA_OBJECT_serialize(const TPMA_OBJECT in, json_object **jso);

TSS2_RC
ifapi_json_TPMA_LOCALITY_serialize(const TPMA_LOCALITY in, json_object **jso);

TSS2_RC
ifapi_json_TPMA_CC_serialize(const TPMA_CC in, json_object **jso);

TSS2_RC
ifapi_json_TPMA_ACT_serialize(const TPMA_ACT in, json_object **jso);

TSS2_RC
ifapi_json_TPMI_YES_NO_serialize(const TPMI_YES_NO in, json_object **jso);

TSS2_RC
ifapi_json_TPMI_RH_HIERARCHY_serialize(const TPMI_RH_HIERARCHY in,
                                       json_object **jso);

TSS2_RC
ifapi_json_TPMI_RH_NV_INDEX_serialize(const TPMI_RH_NV_INDEX in,
                                      json_object **jso);

TSS2_RC
ifapi_json_TPMI_ALG_HASH_serialize(const TPMI_ALG_HASH in, json_object **jso);

TSS2_RC
ifapi_json_TPMI_ALG_SYM_OBJECT_serialize(const TPMI_ALG_SYM_OBJECT in,
        json_object **jso);

TSS2_RC
ifapi_json_TPMI_ALG_SYM_MODE_serialize(const TPMI_ALG_SYM_MODE in,
                                       json_object **jso);

TSS2_RC
ifapi_json_TPMI_ALG_CIPHER_MODE_serialize(const TPMI_ALG_CIPHER_MODE in,
                                          json_object **jso);

TSS2_RC
ifapi_json_TPMI_ALG_KDF_serialize(const TPMI_ALG_KDF in, json_object **jso);

TSS2_RC
ifapi_json_TPMI_ALG_SIG_SCHEME_serialize(const TPMI_ALG_SIG_SCHEME in,
        json_object **jso);

TSS2_RC
ifapi_json_TPMS_EMPTY_serialize(const TPMS_EMPTY *in, json_object **jso);

TSS2_RC
ifapi_json_TPMU_HA_serialize(const TPMU_HA *in, UINT32 selector,
                             json_object **jso);

TSS2_RC
ifapi_json_TPMT_HA_serialize(const TPMT_HA *in, json_object **jso);

TSS2_RC
ifapi_json_TPM2B_DIGEST_serialize(const TPM2B_DIGEST *in, json_object **jso);

TSS2_RC
ifapi_json_TPM2B_DATA_serialize(const TPM2B_DATA *in, json_object **jso);

TSS2_RC
ifapi_json_TPM2B_NONCE_serialize(const TPM2B_NONCE *in, json_object **jso);

TSS2_RC
ifapi_json_TPM2B_OPERAND_serialize(const TPM2B_OPERAND *in, json_object **jso);

TSS2_RC
ifapi_json_TPM2B_EVENT_serialize(const TPM2B_EVENT *in, json_object **jso);

TSS2_RC
ifapi_json_TPM2B_MAX_NV_BUFFER_serialize(const TPM2B_MAX_NV_BUFFER *in,
        json_object **jso);

TSS2_RC
ifapi_json_TPM2B_NAME_serialize(const TPM2B_NAME *in, json_object **jso);

TSS2_RC
ifapi_json_TPMS_PCR_SELECT_serialize(const TPMS_PCR_SELECT *in,
                                     json_object **jso);

TSS2_RC
ifapi_json_TPMS_PCR_SELECTION_serialize(const TPMS_PCR_SELECTION *in,
                                        json_object **jso);

TSS2_RC
ifapi_json_TPMT_TK_CREATION_serialize(const TPMT_TK_CREATION *in,
                                      json_object **jso);

TSS2_RC
ifapi_json_TPMS_ALG_PROPERTY_serialize(const TPMS_ALG_PROPERTY *in,
                                       json_object **jso);

TSS2_RC
ifapi_json_TPMS_TAGGED_PROPERTY_serialize(const TPMS_TAGGED_PROPERTY *in,
        json_object **jso);

TSS2_RC
ifapi_json_TPMS_TAGGED_PCR_SELECT_serialize(const TPMS_TAGGED_PCR_SELECT *in,
        json_object **jso);

TSS2_RC
ifapi_json_TPMS_TAGGED_POLICY_serialize(const TPMS_TAGGED_POLICY *in,
                                        json_object **jso);

TSS2_RC
ifapi_json_TPMS_ACT_DATA_serialize(const TPMS_ACT_DATA *in, json_object **jso);

TSS2_RC
ifapi_json_TPML_CC_serialize(const TPML_CC *in, json_object **jso);

TSS2_RC
ifapi_json_TPML_CCA_serialize(const TPML_CCA *in, json_object **jso);

TSS2_RC
ifapi_json_TPML_HANDLE_serialize(const TPML_HANDLE *in, json_object **jso);

TSS2_RC
ifapi_json_TPML_DIGEST_VALUES_serialize(const TPML_DIGEST_VALUES *in,
                                        json_object **jso);

TSS2_RC
ifapi_json_TPML_PCR_SELECTION_serialize(const TPML_PCR_SELECTION *in,
                                        json_object **jso);

TSS2_RC
ifapi_json_TPML_ALG_PROPERTY_serialize(const TPML_ALG_PROPERTY *in,
                                       json_object **jso);

TSS2_RC
ifapi_json_TPML_TAGGED_TPM_PROPERTY_serialize(const TPML_TAGGED_TPM_PROPERTY
        *in, json_object **jso);

TSS2_RC
ifapi_json_TPML_TAGGED_PCR_PROPERTY_serialize(const TPML_TAGGED_PCR_PROPERTY
        *in, json_object **jso);

TSS2_RC
ifapi_json_TPML_ECC_CURVE_serialize(const TPML_ECC_CURVE *in,
                                    json_object **jso);

TSS2_RC
ifapi_json_TPML_TAGGED_POLICY_serialize(const TPML_TAGGED_POLICY *in,
                                        json_object **jso);

TSS2_RC
ifapi_json_TPML_ACT_DATA_serialize(const TPML_ACT_DATA *in, json_object **jso);

TSS2_RC
ifapi_json_TPMU_CAPABILITIES_serialize(const TPMU_CAPABILITIES *in,
                                       UINT32 selector, json_object **jso);

TSS2_RC
ifapi_json_TPMS_CAPABILITY_DATA_serialize(const TPMS_CAPABILITY_DATA *in,
        json_object **jso);

TSS2_RC
ifapi_json_TPMS_CLOCK_INFO_serialize(const TPMS_CLOCK_INFO *in,
                                     json_object **jso);

TSS2_RC
ifapi_json_TPMS_TIME_INFO_serialize(const TPMS_TIME_INFO *in,
                                    json_object **jso);

TSS2_RC
ifapi_json_TPMS_TIME_ATTEST_INFO_serialize(const TPMS_TIME_ATTEST_INFO *in,
        json_object **jso);

TSS2_RC
ifapi_json_TPMS_CERTIFY_INFO_serialize(const TPMS_CERTIFY_INFO *in,
                                       json_object **jso);

TSS2_RC
ifapi_json_TPMS_QUOTE_INFO_serialize(const TPMS_QUOTE_INFO *in,
                                     json_object **jso);

TSS2_RC
ifapi_json_TPMS_COMMAND_AUDIT_INFO_serialize(const TPMS_COMMAND_AUDIT_INFO *in,
        json_object **jso);

TSS2_RC
ifapi_json_TPMS_SESSION_AUDIT_INFO_serialize(const TPMS_SESSION_AUDIT_INFO *in,
        json_object **jso);

TSS2_RC
ifapi_json_TPMS_CREATION_INFO_serialize(const TPMS_CREATION_INFO *in,
                                        json_object **jso);

TSS2_RC
ifapi_json_TPMS_NV_CERTIFY_INFO_serialize(const TPMS_NV_CERTIFY_INFO *in,
        json_object **jso);

TSS2_RC
ifapi_json_TPMI_ST_ATTEST_serialize(const TPMI_ST_ATTEST in, json_object **jso);

TSS2_RC
ifapi_json_TPMU_ATTEST_serialize(const TPMU_ATTEST *in, UINT32 selector,
                                 json_object **jso);

TSS2_RC
ifapi_json_TPMS_ATTEST_serialize(const TPMS_ATTEST *in, json_object **jso);

TSS2_RC
ifapi_json_TPMI_AES_KEY_BITS_serialize(const TPMI_AES_KEY_BITS in,
                                       json_object **jso);

TSS2_RC
ifapi_json_TPMU_SYM_KEY_BITS_serialize(const TPMU_SYM_KEY_BITS *in,
                                       UINT32 selector, json_object **jso);

TSS2_RC
ifapi_json_TPMU_SYM_MODE_serialize(const TPMU_SYM_MODE *in, UINT32 selector,
                                   json_object **jso);

TSS2_RC
ifapi_json_TPMT_SYM_DEF_OBJECT_serialize(const TPMT_SYM_DEF_OBJECT *in,
        json_object **jso);

TSS2_RC
ifapi_json_TPMS_SYMCIPHER_PARMS_serialize(const TPMS_SYMCIPHER_PARMS *in,
        json_object **jso);

TSS2_RC
ifapi_json_TPMS_SCHEME_HASH_serialize(const TPMS_SCHEME_HASH *in,
                                      json_object **jso);

TSS2_RC
ifapi_json_TPMS_SCHEME_ECDAA_serialize(const TPMS_SCHEME_ECDAA *in,
                                       json_object **jso);

TSS2_RC
ifapi_json_TPMI_ALG_KEYEDHASH_SCHEME_serialize(const TPMI_ALG_KEYEDHASH_SCHEME
        in, json_object **jso);

TSS2_RC
ifapi_json_TPMS_SCHEME_HMAC_serialize(const TPMS_SCHEME_HMAC *in,
                                      json_object **jso);

TSS2_RC
ifapi_json_TPMS_SCHEME_XOR_serialize(const TPMS_SCHEME_XOR *in,
                                     json_object **jso);

TSS2_RC
ifapi_json_TPMU_SCHEME_KEYEDHASH_serialize(const TPMU_SCHEME_KEYEDHASH *in,
        UINT32 selector, json_object **jso);

TSS2_RC
ifapi_json_TPMT_KEYEDHASH_SCHEME_serialize(const TPMT_KEYEDHASH_SCHEME *in,
        json_object **jso);

TSS2_RC
ifapi_json_TPMS_SIG_SCHEME_RSASSA_serialize(const TPMS_SIG_SCHEME_RSASSA *in,
        json_object **jso);

TSS2_RC
ifapi_json_TPMS_SIG_SCHEME_RSAPSS_serialize(const TPMS_SIG_SCHEME_RSAPSS *in,
        json_object **jso);

TSS2_RC
ifapi_json_TPMS_SIG_SCHEME_ECDSA_serialize(const TPMS_SIG_SCHEME_ECDSA *in,
        json_object **jso);

TSS2_RC
ifapi_json_TPMS_SIG_SCHEME_SM2_serialize(const TPMS_SIG_SCHEME_SM2 *in,
        json_object **jso);

TSS2_RC
ifapi_json_TPMS_SIG_SCHEME_ECSCHNORR_serialize(const TPMS_SIG_SCHEME_ECSCHNORR
        *in, json_object **jso);

TSS2_RC
ifapi_json_TPMS_SIG_SCHEME_ECDAA_serialize(const TPMS_SIG_SCHEME_ECDAA *in,
        json_object **jso);

TSS2_RC
ifapi_json_TPMU_SIG_SCHEME_serialize(const TPMU_SIG_SCHEME *in, UINT32 selector,
                                     json_object **jso);

TSS2_RC
ifapi_json_TPMT_SIG_SCHEME_serialize(const TPMT_SIG_SCHEME *in,
                                     json_object **jso);

TSS2_RC
ifapi_json_TPMS_ENC_SCHEME_OAEP_serialize(const TPMS_ENC_SCHEME_OAEP *in,
        json_object **jso);

TSS2_RC
ifapi_json_TPMS_ENC_SCHEME_RSAES_serialize(const TPMS_ENC_SCHEME_RSAES *in,
        json_object **jso);

TSS2_RC
ifapi_json_TPMS_KEY_SCHEME_ECDH_serialize(const TPMS_KEY_SCHEME_ECDH *in,
        json_object **jso);

TSS2_RC
ifapi_json_TPMS_SCHEME_MGF1_serialize(const TPMS_SCHEME_MGF1 *in,
                                      json_object **jso);

TSS2_RC
ifapi_json_TPMS_SCHEME_KDF1_SP800_56A_serialize(const TPMS_SCHEME_KDF1_SP800_56A
        *in, json_object **jso);

TSS2_RC
ifapi_json_TPMS_SCHEME_KDF1_SP800_108_serialize(const TPMS_SCHEME_KDF1_SP800_108
        *in, json_object **jso);

TSS2_RC
ifapi_json_TPMU_KDF_SCHEME_serialize(const TPMU_KDF_SCHEME *in, UINT32 selector,
                                     json_object **jso);

TSS2_RC
ifapi_json_TPMT_KDF_SCHEME_serialize(const TPMT_KDF_SCHEME *in,
                                     json_object **jso);

TSS2_RC
ifapi_json_TPMI_ALG_ASYM_SCHEME_serialize(const TPMI_ALG_ASYM_SCHEME in,
        json_object **jso);

TSS2_RC
ifapi_json_TPMU_ASYM_SCHEME_serialize(const TPMU_ASYM_SCHEME *in,
                                      UINT32 selector, json_object **jso);

TSS2_RC
ifapi_json_TPMT_ASYM_SCHEME_serialize(const TPMT_ASYM_SCHEME *in,
                                      json_object **jso);

TSS2_RC
ifapi_json_TPMI_ALG_RSA_SCHEME_serialize(const TPMI_ALG_RSA_SCHEME in,
        json_object **jso);

TSS2_RC
ifapi_json_TPMT_RSA_SCHEME_serialize(const TPMT_RSA_SCHEME *in,
                                     json_object **jso);

TSS2_RC
ifapi_json_TPM2B_PUBLIC_KEY_RSA_serialize(const TPM2B_PUBLIC_KEY_RSA *in,
        json_object **jso);

TSS2_RC
ifapi_json_TPMI_RSA_KEY_BITS_serialize(const TPMI_RSA_KEY_BITS in,
                                       json_object **jso);

TSS2_RC
ifapi_json_TPM2B_ECC_PARAMETER_serialize(const TPM2B_ECC_PARAMETER *in,
        json_object **jso);

TSS2_RC
ifapi_json_TPMS_ECC_POINT_serialize(const TPMS_ECC_POINT *in,
                                    json_object **jso);

TSS2_RC
ifapi_json_TPMI_ALG_ECC_SCHEME_serialize(const TPMI_ALG_ECC_SCHEME in,
        json_object **jso);

TSS2_RC
ifapi_json_TPMI_ECC_CURVE_serialize(const TPMI_ECC_CURVE in, json_object **jso);

TSS2_RC
ifapi_json_TPMT_ECC_SCHEME_serialize(const TPMT_ECC_SCHEME *in,
                                     json_object **jso);

TSS2_RC
ifapi_json_TPMS_SIGNATURE_RSA_serialize(const TPMS_SIGNATURE_RSA *in,
                                        json_object **jso);

TSS2_RC
ifapi_json_TPMS_SIGNATURE_RSASSA_serialize(const TPMS_SIGNATURE_RSASSA *in,
        json_object **jso);

TSS2_RC
ifapi_json_TPMS_SIGNATURE_RSAPSS_serialize(const TPMS_SIGNATURE_RSAPSS *in,
        json_object **jso);

TSS2_RC
ifapi_json_TPMS_SIGNATURE_ECC_serialize(const TPMS_SIGNATURE_ECC *in,
                                        json_object **jso);

TSS2_RC
ifapi_json_TPMS_SIGNATURE_ECDSA_serialize(const TPMS_SIGNATURE_ECDSA *in,
        json_object **jso);

TSS2_RC
ifapi_json_TPMS_SIGNATURE_ECDAA_serialize(const TPMS_SIGNATURE_ECDAA *in,
        json_object **jso);

TSS2_RC
ifapi_json_TPMS_SIGNATURE_SM2_serialize(const TPMS_SIGNATURE_SM2 *in,
                                        json_object **jso);

TSS2_RC
ifapi_json_TPMS_SIGNATURE_ECSCHNORR_serialize(const TPMS_SIGNATURE_ECSCHNORR
        *in, json_object **jso);

TSS2_RC
ifapi_json_TPMU_SIGNATURE_serialize(const TPMU_SIGNATURE *in, UINT32 selector,
                                    json_object **jso);

TSS2_RC
ifapi_json_TPMT_SIGNATURE_serialize(const TPMT_SIGNATURE *in,
                                    json_object **jso);

TSS2_RC
ifapi_json_TPM2B_ENCRYPTED_SECRET_serialize(const TPM2B_ENCRYPTED_SECRET *in,
        json_object **jso);

TSS2_RC
ifapi_json_TPMI_ALG_PUBLIC_serialize(const TPMI_ALG_PUBLIC in,
                                     json_object **jso);

TSS2_RC
ifapi_json_TPMU_PUBLIC_ID_serialize(const TPMU_PUBLIC_ID *in, UINT32 selector,
                                    json_object **jso);

TSS2_RC
ifapi_json_TPMS_KEYEDHASH_PARMS_serialize(const TPMS_KEYEDHASH_PARMS *in,
        json_object **jso);

TSS2_RC
ifapi_json_TPMS_RSA_PARMS_serialize(const TPMS_RSA_PARMS *in,
                                    json_object **jso);

TSS2_RC
ifapi_json_TPMS_ECC_PARMS_serialize(const TPMS_ECC_PARMS *in,
                                    json_object **jso);

TSS2_RC
ifapi_json_TPMU_PUBLIC_PARMS_serialize(const TPMU_PUBLIC_PARMS *in,
                                       UINT32 selector, json_object **jso);

TSS2_RC
ifapi_json_TPMT_PUBLIC_serialize(const TPMT_PUBLIC *in, json_object **jso);

TSS2_RC
ifapi_json_TPM2B_PUBLIC_serialize(const TPM2B_PUBLIC *in, json_object **jso);

TSS2_RC
ifapi_json_TPM2B_PRIVATE_serialize(const TPM2B_PRIVATE *in, json_object **jso);

TSS2_RC
ifapi_json_TPM2_NT_serialize(const TPM2_NT in, json_object **jso);

TSS2_RC
ifapi_json_TPMA_NV_serialize(const TPMA_NV in, json_object **jso);

TSS2_RC
ifapi_json_TPMS_NV_PUBLIC_serialize(const TPMS_NV_PUBLIC *in,
                                    json_object **jso);

TSS2_RC
ifapi_json_TPM2B_NV_PUBLIC_serialize(const TPM2B_NV_PUBLIC *in,
                                     json_object **jso);

TSS2_RC
ifapi_json_TPMS_CREATION_DATA_serialize(const TPMS_CREATION_DATA *in,
                                        json_object **jso);

TSS2_RC
ifapi_json_TPM2B_CREATION_DATA_serialize(const TPM2B_CREATION_DATA *in,
        json_object **jso);

#endif /* FAPI_TPM_JSON_SERIALIZE_H */
