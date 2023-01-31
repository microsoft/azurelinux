/* SPDX-License-Identifier: BSD-2-Clause */
/*******************************************************************************
 * Copyright 2018-2019, Fraunhofer SIT sponsored by Infineon Technologies AG
 * All rights reserved.
 ******************************************************************************/

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <stdio.h>

#include "tpm_json_serialize.h"
#define LOGMODULE fapijson
#include "util/log.h"
#include "util/aux_util.h"

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

/** Serialize a TPMS_EMPTY.
 *
 * @param[in] in not used.
 * @param[in] jso not used.
 * @retval TSS2_RC_SUCCESS is always returnde.
 */
TSS2_RC
ifapi_json_TPMS_EMPTY_serialize(const TPMS_EMPTY *in, json_object **jso)
{
    UNUSED(in);
    UNUSED(jso);
    return TSS2_RC_SUCCESS;
}

/** Serialize a pcr selection to json
 *
 * @param[in]  sizeofSelect size of selection byte array.
 * @param[in]  pcrSelect selection array.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if sizeofSelect is too big.
 */
TSS2_RC
ifapi_json_pcr_select_serialize(
    const UINT8 sizeofSelect,
    const BYTE pcrSelect[],
    json_object **jso)
{
    if (*jso == NULL) {
        *jso = json_object_new_array();
        return_if_null(*jso, "Out of memory.", TSS2_FAPI_RC_MEMORY);
    }
    if (sizeofSelect > TPM2_PCR_SELECT_MAX) {
        LOG_ERROR("Too many bytes for array (%"PRIuPTR" > %"PRIuPTR" = TPM2_PCR_SELECT_MAX)",
                  (size_t)sizeofSelect, (size_t)TPM2_PCR_SELECT_MAX);
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    UINT32 i1, i2;
    json_object *jso2;
    for (i1 = 0; i1 < TPM2_PCR_LAST - TPM2_PCR_FIRST; i1++) {
        i2 = i1 + TPM2_PCR_FIRST;
        if (pcrSelect[i2 / 8] & (BYTE)(1 << (i2 % 8))) {
            jso2 = json_object_new_int(i2);
            return_if_null(jso2, "Out of memory.", TSS2_FAPI_RC_MEMORY);
            json_object_array_add(*jso, jso2);
        }
    }
    return TSS2_RC_SUCCESS;
}

/** Serialize a TPMS_PCR_SELECT structure to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMS_PCR_SELECTION.
 */
TSS2_RC
ifapi_json_TPMS_PCR_SELECT_serialize(const TPMS_PCR_SELECT *in,
                                        json_object **jso)
{
    TSS2_RC r;

    r = ifapi_json_pcr_select_serialize(in->sizeofSelect, &in->pcrSelect[0], jso);
    return_if_error(r, "Serialize pcr selection");

    return TSS2_RC_SUCCESS;
}


/** Serialize a TPMS_PCR_SELECTION structure to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMS_PCR_SELECTION.
 */
TSS2_RC
ifapi_json_TPMS_PCR_SELECTION_serialize(const TPMS_PCR_SELECTION *in,
                                        json_object **jso)
{
    if (*jso == NULL) {
        *jso = json_object_new_object();
        return_if_null(*jso, "Out of memory.", TSS2_FAPI_RC_MEMORY);
    }
    TSS2_RC r;
    json_object *jso2 = NULL;
    r = ifapi_json_TPMI_ALG_HASH_serialize(in->hash, &jso2);
    return_if_error(r, "Serialize pcr selection");

    json_object_object_add(*jso, "hash", jso2);
    jso2 = NULL;
    r = ifapi_json_pcr_select_serialize(in->sizeofSelect, &in->pcrSelect[0], &jso2);
    return_if_error(r, "Serialize pcr selection");

    json_object_object_add(*jso, "pcrSelect", jso2);
    return TSS2_RC_SUCCESS;
}

/** Serialize a TPMS_TAGGED_PCR_SELECT structure to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMS_TAGGED_PCR_SELECT.
 */
TSS2_RC
ifapi_json_TPMS_TAGGED_PCR_SELECT_serialize(const TPMS_TAGGED_PCR_SELECT *in,
        json_object **jso)
{
    TSS2_RC r;
    if (*jso == NULL)
        *jso = json_object_new_object();
    json_object *jso2 = NULL;
    r = ifapi_json_TPM2_PT_PCR_serialize(in->tag, &jso2);
    return_if_error(r, "Serialize pcr selection");

    json_object_object_add(*jso, "tag", jso2);
    jso2 = NULL;
    r = ifapi_json_pcr_select_serialize(in->sizeofSelect, &in->pcrSelect[0], &jso2);
    return_if_error(r, "Serialize pcr selection");

    json_object_object_add(*jso, "pcrSelect", jso2);
    return TSS2_RC_SUCCESS;
}

/** Serialize a TPMS_TAGGED_POLICY structure to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMS_TAGGED_POLICY.
 */
TSS2_RC
ifapi_json_TPMS_TAGGED_POLICY_serialize(const TPMS_TAGGED_POLICY *in, json_object **jso)
{
    TSS2_RC r;
    if (*jso == NULL)
        *jso = json_object_new_object();
    json_object *jso2 = NULL;
    r = ifapi_json_TPM2_HANDLE_serialize(in->handle, &jso2);
    return_if_error(r, "Serialize tagged policy");

    json_object_object_add(*jso, "handle", jso2);
    jso2 = NULL;
    r = ifapi_json_TPMT_HA_serialize(&in->policyHash, &jso2);
    return_if_error(r, "Serialize tagged policy");

    json_object_object_add(*jso, "policyHash", jso2);
    return TSS2_RC_SUCCESS;
}

/** Serialize a TPMS_ACT_DATA structure to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMS_ACT_DATA.
 */
TSS2_RC
ifapi_json_TPMS_ACT_DATA_serialize(const TPMS_ACT_DATA *in, json_object **jso)
{
    TSS2_RC r;
    if (*jso == NULL)
        *jso = json_object_new_object();
    json_object *jso2 = NULL;
    r = ifapi_json_TPM2_HANDLE_serialize(in->handle, &jso2);
    return_if_error(r, "Serialize act data");

    json_object_object_add(*jso, "handle", jso2);
    jso2 = NULL;
    r = ifapi_json_UINT32_serialize(in->timeout, &jso2);
    return_if_error(r, "Serialize act data");

    json_object_object_add(*jso, "timeout", jso2);
    jso2 = NULL;
    r = ifapi_json_TPMA_ACT_serialize(in->attributes, &jso2);
    return_if_error(r, "Serialize act data");

    json_object_object_add(*jso, "attributes", jso2);
    return TSS2_RC_SUCCESS;
}

/** Serialize a base_type UINT16 to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type UINT16.
 */
TSS2_RC
ifapi_json_UINT16_serialize(const UINT16 in, json_object **jso)
{
    *jso = json_object_new_int64(in);
    if (*jso == NULL) {
        LOG_ERROR("Bad value %04"PRIx16"", in);
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    return TSS2_RC_SUCCESS;
}

/** Serialize a base_type UINT32 to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type UINT32.
 */
TSS2_RC
ifapi_json_UINT32_serialize(const UINT32 in, json_object **jso)
{
    *jso = json_object_new_int64(in);
    if (*jso == NULL) {
        LOG_ERROR("Bad value %"PRIx32 "", in);
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    return TSS2_RC_SUCCESS;
}

/** Serialize a base_type INT32 to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type INT32.
 */
TSS2_RC
ifapi_json_INT32_serialize(const INT32 in, json_object **jso)
{
    *jso = json_object_new_int64(in);
    if (*jso == NULL) {
        LOG_ERROR("Bad value %"PRIi32 "", in);
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    return TSS2_RC_SUCCESS;
}

/** Serialize a base_type  UINT64 to json.
 *
 * @param[in] in variable to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type UINT64.
 */
TSS2_RC
ifapi_json_UINT64_serialize(UINT64 in, json_object **jso)
{
    json_object *jso1 = NULL, *jso2 = NULL;
    if (in < 0x1000000000000) {
        *jso = json_object_new_int64(in);
        if (*jso == NULL) {
            LOG_ERROR("Bad value %"PRIu32 "", (uint32_t)in);
            return TSS2_FAPI_RC_BAD_VALUE;
        }
        return TSS2_RC_SUCCESS;
    }

    jso1 = json_object_new_int64(in / 0x100000000);
    return_if_null(jso1, "Out of memory.", TSS2_FAPI_RC_MEMORY);

    in %= 0x100000000;

    jso2 = json_object_new_int64(in);
    if (!jso2) json_object_put(jso1);
    return_if_null(jso2, "Out of memory.", TSS2_FAPI_RC_MEMORY);

    *jso = json_object_new_array();
    if (!*jso) json_object_put(jso1);
    if (!*jso) json_object_put(jso2);
    return_if_null(*jso, "Out of memory.", TSS2_FAPI_RC_MEMORY);

    json_object_array_add(*jso, jso1);
    json_object_array_add(*jso, jso2);

    return TSS2_RC_SUCCESS;
}

/** Serialize TPM2_GENERATED to json.
 *
 * @param[in] in constant to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the constant is not of type TPM2_GENERATED.
 */
TSS2_RC
ifapi_json_TPM2_GENERATED_serialize(const TPM2_GENERATED in, json_object **jso)
{
    if (in != TPM2_GENERATED_VALUE) {
        return_error(TSS2_FAPI_RC_BAD_VALUE, "Undefined constant.");
    }

    *jso = json_object_new_string("VALUE");
    check_oom(*jso);

    return TSS2_RC_SUCCESS;
}

/** Serialize TPM2_ALG_ID to json.
 *
 * For hash algs lowercase is used because it's required for
 * JSON events in Canonical Event Log specification.
 *
 * @param[in] in constant to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the constant is not of type TPM2_ALG_ID.
 */
TSS2_RC
ifapi_json_TPM2_ALG_ID_serialize(const TPM2_ALG_ID in, json_object **jso)
{
    static const struct { TPM2_ALG_ID in; const char *name; } tab[] = {
        { TPM2_ALG_ERROR, "ERROR" },
        { TPM2_ALG_RSA, "RSA" },
        { TPM2_ALG_TDES, "TDES" },
/* We prefer SHA1 as output over SHA */
/*      { TPM2_ALG_SHA, "sha" },*/
        { TPM2_ALG_SHA1, "sha1" },
        { TPM2_ALG_CMAC, "CMAC" },
        { TPM2_ALG_HMAC, "HMAC" },
        { TPM2_ALG_AES, "AES" },
        { TPM2_ALG_MGF1, "MGF1" },
        { TPM2_ALG_KEYEDHASH, "KEYEDHASH" },
        { TPM2_ALG_XOR, "XOR" },
        { TPM2_ALG_SHA256, "sha256" },
        { TPM2_ALG_SHA384, "sha384" },
        { TPM2_ALG_SHA512, "sha512" },
        { TPM2_ALG_NULL, "NULL" },
        { TPM2_ALG_SM3_256, "sm3_256" },
        { TPM2_ALG_SM4, "SM4" },
        { TPM2_ALG_RSASSA, "RSASSA" },
        { TPM2_ALG_RSAES, "RSAES" },
        { TPM2_ALG_RSAPSS, "RSAPSS" },
        { TPM2_ALG_OAEP, "OAEP" },
        { TPM2_ALG_ECDSA, "ECDSA" },
        { TPM2_ALG_ECDH, "ECDH" },
        { TPM2_ALG_ECDAA, "ECDAA" },
        { TPM2_ALG_SM2, "SM2" },
        { TPM2_ALG_ECSCHNORR, "ECSCHNORR" },
        { TPM2_ALG_ECMQV, "ECMQV" },
        { TPM2_ALG_KDF1_SP800_56A, "KDF1_SP800_56A" },
        { TPM2_ALG_KDF2, "KDF2" },
        { TPM2_ALG_KDF1_SP800_108, "KDF1_SP800_108" },
        { TPM2_ALG_ECC, "ECC" },
        { TPM2_ALG_SYMCIPHER, "SYMCIPHER" },
        { TPM2_ALG_CAMELLIA, "CAMELLIA" },
        { TPM2_ALG_CTR, "CTR" },
        { TPM2_ALG_OFB, "OFB" },
        { TPM2_ALG_CBC, "CBC" },
        { TPM2_ALG_CFB, "CFB" },
        { TPM2_ALG_ECB, "ECB" },
    };

    for (size_t i = 0; i < sizeof(tab) / sizeof(tab[0]); i++) {
        if (tab[i].in == in) {
            *jso = json_object_new_string(tab[i].name);
            check_oom(*jso);
            return TSS2_RC_SUCCESS;
        }
    }
    return_error(TSS2_FAPI_RC_BAD_VALUE, "Undefined constant.");
}

/** Serialize TPM2_ECC_CURVE to json.
 *
 * @param[in] in constant to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the constant is not of type TPM2_ECC_CURVE.
 */
TSS2_RC
ifapi_json_TPM2_ECC_CURVE_serialize(const TPM2_ECC_CURVE in, json_object **jso)
{
    static const struct { TPM2_ECC_CURVE in; char *name; } tab[] = {
        { TPM2_ECC_NONE, "NONE" },
        { TPM2_ECC_NIST_P192, "NIST_P192" },
        { TPM2_ECC_NIST_P224, "NIST_P224" },
        { TPM2_ECC_NIST_P256, "NIST_P256" },
        { TPM2_ECC_NIST_P384, "NIST_P384" },
        { TPM2_ECC_NIST_P521, "NIST_P521" },
        { TPM2_ECC_BN_P256, "BN_P256" },
        { TPM2_ECC_BN_P638, "BN_P638" },
        { TPM2_ECC_SM2_P256, "SM2_P256" },
    };

    for (size_t i = 0; i < sizeof(tab) / sizeof(tab[0]); i++) {
        if (tab[i].in == in) {
            *jso = json_object_new_string(tab[i].name);
            check_oom(*jso);
            return TSS2_RC_SUCCESS;
        }
    }
    return_error(TSS2_FAPI_RC_BAD_VALUE, "Undefined constant.");
}

/** Serialize TPM2_CC to json.
 *
 * @param[in] in constant to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the constant is not of type TPM2_CC.
 */
TSS2_RC
ifapi_json_TPM2_CC_serialize(const TPM2_CC in, json_object **jso)
{
    static const struct { TPM2_CC in; char *name; } tab[] = {
        /* We don't want to return FIRST but the actual value */
        /* { TPM2_CC_FIRST, "FIRST" }, */
        { TPM2_CC_NV_UndefineSpaceSpecial, "NV_UndefineSpaceSpecial" },
        { TPM2_CC_EvictControl, "EvictControl" },
        { TPM2_CC_HierarchyControl, "HierarchyControl" },
        { TPM2_CC_NV_UndefineSpace, "NV_UndefineSpace" },
        { TPM2_CC_ChangeEPS, "ChangeEPS" },
        { TPM2_CC_ChangePPS, "ChangePPS" },
        { TPM2_CC_Clear, "Clear" },
        { TPM2_CC_ClearControl, "ClearControl" },
        { TPM2_CC_ClockSet, "ClockSet" },
        { TPM2_CC_HierarchyChangeAuth, "HierarchyChangeAuth" },
        { TPM2_CC_NV_DefineSpace, "NV_DefineSpace" },
        { TPM2_CC_PCR_Allocate, "PCR_Allocate" },
        { TPM2_CC_PCR_SetAuthPolicy, "PCR_SetAuthPolicy" },
        { TPM2_CC_PP_Commands, "PP_Commands" },
        { TPM2_CC_SetPrimaryPolicy, "SetPrimaryPolicy" },
        { TPM2_CC_FieldUpgradeStart, "FieldUpgradeStart" },
        { TPM2_CC_ClockRateAdjust, "ClockRateAdjust" },
        { TPM2_CC_CreatePrimary, "CreatePrimary" },
        { TPM2_CC_NV_GlobalWriteLock, "NV_GlobalWriteLock" },
        { TPM2_CC_GetCommandAuditDigest, "GetCommandAuditDigest" },
        { TPM2_CC_NV_Increment, "NV_Increment" },
        { TPM2_CC_NV_SetBits, "NV_SetBits" },
        { TPM2_CC_NV_Extend, "NV_Extend" },
        { TPM2_CC_NV_Write, "NV_Write" },
        { TPM2_CC_NV_WriteLock, "NV_WriteLock" },
        { TPM2_CC_DictionaryAttackLockReset, "DictionaryAttackLockReset" },
        { TPM2_CC_DictionaryAttackParameters, "DictionaryAttackParameters" },
        { TPM2_CC_NV_ChangeAuth, "NV_ChangeAuth" },
        { TPM2_CC_PCR_Event, "PCR_Event" },
        { TPM2_CC_PCR_Reset, "PCR_Reset" },
        { TPM2_CC_SequenceComplete, "SequenceComplete" },
        { TPM2_CC_SetAlgorithmSet, "SetAlgorithmSet" },
        { TPM2_CC_SetCommandCodeAuditStatus, "SetCommandCodeAuditStatus" },
        { TPM2_CC_FieldUpgradeData, "FieldUpgradeData" },
        { TPM2_CC_IncrementalSelfTest, "IncrementalSelfTest" },
        { TPM2_CC_SelfTest, "SelfTest" },
        { TPM2_CC_Startup, "Startup" },
        { TPM2_CC_Shutdown, "Shutdown" },
        { TPM2_CC_StirRandom, "StirRandom" },
        { TPM2_CC_ActivateCredential, "ActivateCredential" },
        { TPM2_CC_Certify, "Certify" },
        { TPM2_CC_PolicyNV, "PolicyNV" },
        { TPM2_CC_CertifyCreation, "CertifyCreation" },
        { TPM2_CC_Duplicate, "Duplicate" },
        { TPM2_CC_GetTime, "GetTime" },
        { TPM2_CC_GetSessionAuditDigest, "GetSessionAuditDigest" },
        { TPM2_CC_NV_Read, "NV_Read" },
        { TPM2_CC_NV_ReadLock, "NV_ReadLock" },
        { TPM2_CC_ObjectChangeAuth, "ObjectChangeAuth" },
        { TPM2_CC_PolicySecret, "PolicySecret" },
        { TPM2_CC_Rewrap, "Rewrap" },
        { TPM2_CC_Create, "Create" },
        { TPM2_CC_ECDH_ZGen, "ECDH_ZGen" },
        { TPM2_CC_HMAC, "HMAC" },
        { TPM2_CC_Import, "Import" },
        { TPM2_CC_Load, "Load" },
        { TPM2_CC_Quote, "Quote" },
        { TPM2_CC_RSA_Decrypt, "RSA_Decrypt" },
        { TPM2_CC_HMAC_Start, "HMAC_Start" },
        { TPM2_CC_SequenceUpdate, "SequenceUpdate" },
        { TPM2_CC_Sign, "Sign" },
        { TPM2_CC_Unseal, "Unseal" },
        { TPM2_CC_PolicySigned, "PolicySigned" },
        { TPM2_CC_ContextLoad, "ContextLoad" },
        { TPM2_CC_ContextSave, "ContextSave" },
        { TPM2_CC_ECDH_KeyGen, "ECDH_KeyGen" },
        { TPM2_CC_EncryptDecrypt, "EncryptDecrypt" },
        { TPM2_CC_FlushContext, "FlushContext" },
        { TPM2_CC_LoadExternal, "LoadExternal" },
        { TPM2_CC_MakeCredential, "MakeCredential" },
        { TPM2_CC_NV_ReadPublic, "NV_ReadPublic" },
        { TPM2_CC_PolicyAuthorize, "PolicyAuthorize" },
        { TPM2_CC_PolicyAuthValue, "PolicyAuthValue" },
        { TPM2_CC_PolicyCommandCode, "PolicyCommandCode" },
        { TPM2_CC_PolicyCounterTimer, "PolicyCounterTimer" },
        { TPM2_CC_PolicyCpHash, "PolicyCpHash" },
        { TPM2_CC_PolicyLocality, "PolicyLocality" },
        { TPM2_CC_PolicyNameHash, "PolicyNameHash" },
        { TPM2_CC_PolicyOR, "PolicyOR" },
        { TPM2_CC_PolicyTicket, "PolicyTicket" },
        { TPM2_CC_ReadPublic, "ReadPublic" },
        { TPM2_CC_RSA_Encrypt, "RSA_Encrypt" },
        { TPM2_CC_StartAuthSession, "StartAuthSession" },
        { TPM2_CC_VerifySignature, "VerifySignature" },
        { TPM2_CC_ECC_Parameters, "ECC_Parameters" },
        { TPM2_CC_FirmwareRead, "FirmwareRead" },
        { TPM2_CC_GetCapability, "GetCapability" },
        { TPM2_CC_GetRandom, "GetRandom" },
        { TPM2_CC_GetTestResult, "GetTestResult" },
        { TPM2_CC_Hash, "Hash" },
        { TPM2_CC_PCR_Read, "PCR_Read" },
        { TPM2_CC_PolicyPCR, "PolicyPCR" },
        { TPM2_CC_PolicyRestart, "PolicyRestart" },
        { TPM2_CC_ReadClock, "ReadClock" },
        { TPM2_CC_PCR_Extend, "PCR_Extend" },
        { TPM2_CC_PCR_SetAuthValue, "PCR_SetAuthValue" },
        { TPM2_CC_NV_Certify, "NV_Certify" },
        { TPM2_CC_EventSequenceComplete, "EventSequenceComplete" },
        { TPM2_CC_HashSequenceStart, "HashSequenceStart" },
        { TPM2_CC_PolicyPhysicalPresence, "PolicyPhysicalPresence" },
        { TPM2_CC_PolicyDuplicationSelect, "PolicyDuplicationSelect" },
        { TPM2_CC_PolicyGetDigest, "PolicyGetDigest" },
        { TPM2_CC_TestParms, "TestParms" },
        { TPM2_CC_Commit, "Commit" },
        { TPM2_CC_PolicyPassword, "PolicyPassword" },
        { TPM2_CC_ZGen_2Phase, "ZGen_2Phase" },
        { TPM2_CC_EC_Ephemeral, "EC_Ephemeral" },
        { TPM2_CC_PolicyNvWritten, "PolicyNvWritten" },
        { TPM2_CC_PolicyTemplate, "PolicyTemplate" },
        { TPM2_CC_CreateLoaded, "CreateLoaded" },
        { TPM2_CC_PolicyAuthorizeNV, "PolicyAuthorizeNV" },
        { TPM2_CC_EncryptDecrypt2, "EncryptDecrypt2" },
        /* We don't want to return LAST but the actual value */
        /* { TPM2_CC_LAST, "LAST" }, */
        { TPM2_CC_Vendor_TCG_Test, "Vendor_TCG_Test" },
    };

    for (size_t i = 0; i < sizeof(tab) / sizeof(tab[0]); i++) {
        if (tab[i].in == in) {
            *jso = json_object_new_string(tab[i].name);
            check_oom(*jso);
            return TSS2_RC_SUCCESS;
        }
    }
    return_error(TSS2_FAPI_RC_BAD_VALUE, "Undefined constant.");
}

/** Serialize TPM2_EO to json.
 *
 * @param[in] in constant to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the constant is not of type TPM2_EO.
 */
TSS2_RC
ifapi_json_TPM2_EO_serialize(const TPM2_EO in, json_object **jso)
{
    static const struct { TPM2_EO in; char *name; } tab[] = {
        { TPM2_EO_EQ,          "EQ" },
        { TPM2_EO_NEQ,         "TPM2_EO_NEQ" },
        { TPM2_EO_SIGNED_GT,   "SIGNED_GT" },
        { TPM2_EO_UNSIGNED_GT, "UNSIGNED_GT" },
        { TPM2_EO_SIGNED_LT,   "SIGNED_LT" },
        { TPM2_EO_UNSIGNED_LT, "UNSIGNED_LT" },
        { TPM2_EO_SIGNED_GE,   "SIGNED_GE" },
        { TPM2_EO_UNSIGNED_GE, "UNSIGNED_GE" },
        { TPM2_EO_SIGNED_LE,   "SIGNED_LE" },
        { TPM2_EO_UNSIGNED_LE, "UNSIGNED_LE" },
        { TPM2_EO_BITSET,      "BITSET" },
        { TPM2_EO_BITCLEAR,    "BITCLEAR" },
    };

    for (size_t i = 0; i < sizeof(tab) / sizeof(tab[0]); i++) {
        if (tab[i].in == in) {
            *jso = json_object_new_string(tab[i].name);
            check_oom(*jso);
            return TSS2_RC_SUCCESS;
        }
    }
    return_error(TSS2_FAPI_RC_BAD_VALUE, "Undefined constant.");
}

/** Serialize TPM2_ST to json.
 *
 * @param[in] in constant to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the constant is not of type TPM2_ST.
 */
TSS2_RC
ifapi_json_TPM2_ST_serialize(const TPM2_ST in, json_object **jso)
{
    static const struct { TPM2_ST in; char *name; } tab[] = {
        { TPM2_ST_RSP_COMMAND, "RSP_COMMAND" },
        { TPM2_ST_NULL, "NULL" },
        { TPM2_ST_NO_SESSIONS, "NO_SESSIONS" },
        { TPM2_ST_SESSIONS, "SESSIONS" },
        { TPM2_ST_ATTEST_NV, "ATTEST_NV" },
        { TPM2_ST_ATTEST_COMMAND_AUDIT, "ATTEST_COMMAND_AUDIT" },
        { TPM2_ST_ATTEST_SESSION_AUDIT, "ATTEST_SESSION_AUDIT" },
        { TPM2_ST_ATTEST_CERTIFY, "ATTEST_CERTIFY" },
        { TPM2_ST_ATTEST_QUOTE, "ATTEST_QUOTE" },
        { TPM2_ST_ATTEST_TIME, "ATTEST_TIME" },
        { TPM2_ST_ATTEST_CREATION, "ATTEST_CREATION" },
        { TPM2_ST_CREATION, "CREATION" },
        { TPM2_ST_VERIFIED, "VERIFIED" },
        { TPM2_ST_AUTH_SECRET, "AUTH_SECRET" },
        { TPM2_ST_HASHCHECK, "HASHCHECK" },
        { TPM2_ST_AUTH_SIGNED, "AUTH_SIGNED" },
        { TPM2_ST_FU_MANIFEST, "FU_MANIFEST" },
    };

    for (size_t i = 0; i < sizeof(tab) / sizeof(tab[0]); i++) {
        if (tab[i].in == in) {
            *jso = json_object_new_string(tab[i].name);
            check_oom(*jso);
            return TSS2_RC_SUCCESS;
        }
    }
    return_error(TSS2_FAPI_RC_BAD_VALUE, "Undefined constant.");
}

/** Serialize TPM2_CAP to json.
 *
 * @param[in] in constant to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the constant is not of type TPM2_CAP.
 */
TSS2_RC
ifapi_json_TPM2_CAP_serialize(const TPM2_CAP in, json_object **jso)
{
    static const struct { TPM2_CAP in; char *name; } tab[] = {
        { TPM2_CAP_ALGS, "ALGS" },
        { TPM2_CAP_HANDLES, "HANDLES" },
        { TPM2_CAP_COMMANDS, "COMMANDS" },
        { TPM2_CAP_PP_COMMANDS, "PP_COMMANDS" },
        { TPM2_CAP_AUDIT_COMMANDS, "AUDIT_COMMANDS" },
        { TPM2_CAP_PCRS, "PCRS" },
        { TPM2_CAP_TPM_PROPERTIES, "TPM_PROPERTIES" },
        { TPM2_CAP_PCR_PROPERTIES, "PCR_PROPERTIES" },
        { TPM2_CAP_ECC_CURVES, "ECC_CURVES" },
        { TPM2_CAP_AUTH_POLICIES, "AUTH_POLICIES" },
        { TPM2_CAP_ACT, "ACT"},
        { TPM2_CAP_LAST, "LAST" },
        { TPM2_CAP_VENDOR_PROPERTY, "VENDOR_PROPERTY" },
    };

    for (size_t i = 0; i < sizeof(tab) / sizeof(tab[0]); i++) {
        if (tab[i].in == in) {
            *jso = json_object_new_string(tab[i].name);
            check_oom(*jso);
            return TSS2_RC_SUCCESS;
        }
    }
    return_error(TSS2_FAPI_RC_BAD_VALUE, "Undefined constant.");
}

/** Serialize TPM2_PT to json.
 *
 * @param[in] in constant to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the constant is not of type TPM2_PT.
 */
TSS2_RC
ifapi_json_TPM2_PT_serialize(const TPM2_PT in, json_object **jso)
{
    static const struct { TPM2_PT in; char *name; } tab[] = {
        { TPM2_PT_NONE, "NONE" },
        { TPM2_PT_GROUP, "GROUP" },
        //{ TPM2_PT_FIXED, "FIXED" },
        { TPM2_PT_FAMILY_INDICATOR, "FAMILY_INDICATOR" },
        { TPM2_PT_LEVEL, "LEVEL" },
        { TPM2_PT_REVISION, "REVISION" },
        { TPM2_PT_DAY_OF_YEAR, "DAY_OF_YEAR" },
        { TPM2_PT_YEAR, "YEAR" },
        { TPM2_PT_MANUFACTURER, "MANUFACTURER" },
        { TPM2_PT_VENDOR_STRING_1, "VENDOR_STRING_1" },
        { TPM2_PT_VENDOR_STRING_2, "VENDOR_STRING_2" },
        { TPM2_PT_VENDOR_STRING_3, "VENDOR_STRING_3" },
        { TPM2_PT_VENDOR_STRING_4, "VENDOR_STRING_4" },
        { TPM2_PT_VENDOR_TPM_TYPE, "VENDOR_TPM_TYPE" },
        { TPM2_PT_FIRMWARE_VERSION_1, "FIRMWARE_VERSION_1" },
        { TPM2_PT_FIRMWARE_VERSION_2, "FIRMWARE_VERSION_2" },
        { TPM2_PT_INPUT_BUFFER, "INPUT_BUFFER" },
        { TPM2_PT_HR_TRANSIENT_MIN, "HR_TRANSIENT_MIN" },
        { TPM2_PT_HR_PERSISTENT_MIN, "HR_PERSISTENT_MIN" },
        { TPM2_PT_HR_LOADED_MIN, "HR_LOADED_MIN" },
        { TPM2_PT_ACTIVE_SESSIONS_MAX, "ACTIVE_SESSIONS_MAX" },
        { TPM2_PT_PCR_COUNT, "PCR_COUNT" },
        { TPM2_PT_PCR_SELECT_MIN, "PCR_SELECT_MIN" },
        { TPM2_PT_CONTEXT_GAP_MAX, "CONTEXT_GAP_MAX" },
        { TPM2_PT_NV_COUNTERS_MAX, "NV_COUNTERS_MAX" },
        { TPM2_PT_NV_INDEX_MAX, "NV_INDEX_MAX" },
        { TPM2_PT_MEMORY, "MEMORY" },
        { TPM2_PT_CLOCK_UPDATE, "CLOCK_UPDATE" },
        { TPM2_PT_CONTEXT_HASH, "CONTEXT_HASH" },
        { TPM2_PT_CONTEXT_SYM, "CONTEXT_SYM" },
        { TPM2_PT_CONTEXT_SYM_SIZE, "CONTEXT_SYM_SIZE" },
        { TPM2_PT_ORDERLY_COUNT, "ORDERLY_COUNT" },
        { TPM2_PT_MAX_COMMAND_SIZE, "MAX_COMMAND_SIZE" },
        { TPM2_PT_MAX_RESPONSE_SIZE, "MAX_RESPONSE_SIZE" },
        { TPM2_PT_MAX_DIGEST, "MAX_DIGEST" },
        { TPM2_PT_MAX_OBJECT_CONTEXT, "MAX_OBJECT_CONTEXT" },
        { TPM2_PT_MAX_SESSION_CONTEXT, "MAX_SESSION_CONTEXT" },
        { TPM2_PT_PS_FAMILY_INDICATOR, "PS_FAMILY_INDICATOR" },
        { TPM2_PT_PS_LEVEL, "PS_LEVEL" },
        { TPM2_PT_PS_REVISION, "PS_REVISION" },
        { TPM2_PT_PS_DAY_OF_YEAR, "PS_DAY_OF_YEAR" },
        { TPM2_PT_PS_YEAR, "PS_YEAR" },
        { TPM2_PT_SPLIT_MAX, "SPLIT_MAX" },
        { TPM2_PT_TOTAL_COMMANDS, "TOTAL_COMMANDS" },
        { TPM2_PT_LIBRARY_COMMANDS, "LIBRARY_COMMANDS" },
        { TPM2_PT_VENDOR_COMMANDS, "VENDOR_COMMANDS" },
        { TPM2_PT_NV_BUFFER_MAX, "NV_BUFFER_MAX" },
        { TPM2_PT_MODES, "MODES" },
        { TPM2_PT_MAX_CAP_BUFFER, "MAX_CAP_BUFFER" },
        //{ TPM2_PT_VAR, "VAR" },
        { TPM2_PT_PERMANENT, "PERMANENT" },
        { TPM2_PT_STARTUP_CLEAR, "STARTUP_CLEAR" },
        { TPM2_PT_HR_NV_INDEX, "HR_NV_INDEX" },
        { TPM2_PT_HR_LOADED, "HR_LOADED" },
        { TPM2_PT_HR_LOADED_AVAIL, "HR_LOADED_AVAIL" },
        { TPM2_PT_HR_ACTIVE, "HR_ACTIVE" },
        { TPM2_PT_HR_ACTIVE_AVAIL, "HR_ACTIVE_AVAIL" },
        { TPM2_PT_HR_TRANSIENT_AVAIL, "HR_TRANSIENT_AVAIL" },
        { TPM2_PT_HR_PERSISTENT, "HR_PERSISTENT" },
        { TPM2_PT_HR_PERSISTENT_AVAIL, "HR_PERSISTENT_AVAIL" },
        { TPM2_PT_NV_COUNTERS, "NV_COUNTERS" },
        { TPM2_PT_NV_COUNTERS_AVAIL, "NV_COUNTERS_AVAIL" },
        { TPM2_PT_ALGORITHM_SET, "ALGORITHM_SET" },
        { TPM2_PT_LOADED_CURVES, "LOADED_CURVES" },
        { TPM2_PT_LOCKOUT_COUNTER, "LOCKOUT_COUNTER" },
        { TPM2_PT_MAX_AUTH_FAIL, "MAX_AUTH_FAIL" },
        { TPM2_PT_LOCKOUT_INTERVAL, "LOCKOUT_INTERVAL" },
        { TPM2_PT_LOCKOUT_RECOVERY, "LOCKOUT_RECOVERY" },
        { TPM2_PT_NV_WRITE_RECOVERY, "NV_WRITE_RECOVERY" },
        { TPM2_PT_AUDIT_COUNTER_0, "AUDIT_COUNTER_0" },
        { TPM2_PT_AUDIT_COUNTER_1, "AUDIT_COUNTER_1" },
    };

    for (size_t i = 0; i < sizeof(tab) / sizeof(tab[0]); i++) {
        if (tab[i].in == in) {
            *jso = json_object_new_string(tab[i].name);
            check_oom(*jso);
            return TSS2_RC_SUCCESS;
        }
    }
    return_error2(TSS2_FAPI_RC_BAD_VALUE, "Undefined constant: %"PRIx32, in);
}

/** Serialize TPM2_PT_PCR to json.
 *
 * @param[in] in constant to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the constant is not of type TPM2_PT_PCR.
 */
TSS2_RC
ifapi_json_TPM2_PT_PCR_serialize(const TPM2_PT_PCR in, json_object **jso)
{
    static const struct { TPM2_PT_PCR in; char *name; } tab[] = {
        { TPM2_PT_PCR_SAVE, "SAVE" },
        { TPM2_PT_PCR_EXTEND_L0, "EXTEND_L0" },
        { TPM2_PT_PCR_RESET_L0, "RESET_L0" },
        { TPM2_PT_PCR_EXTEND_L1, "EXTEND_L1" },
        { TPM2_PT_PCR_RESET_L1, "RESET_L1" },
        { TPM2_PT_PCR_EXTEND_L2, "EXTEND_L2" },
        { TPM2_PT_PCR_RESET_L2, "RESET_L2" },
        { TPM2_PT_PCR_EXTEND_L3, "EXTEND_L3" },
        { TPM2_PT_PCR_RESET_L3, "RESET_L3" },
        { TPM2_PT_PCR_EXTEND_L4, "EXTEND_L4" },
        { TPM2_PT_PCR_RESET_L4, "RESET_L4" },
        { TPM2_PT_PCR_NO_INCREMENT, "NO_INCREMENT" },
        { TPM2_PT_PCR_DRTM_RESET, "DRTM_RESET" },
        { TPM2_PT_PCR_POLICY, "POLICY" },
        { TPM2_PT_PCR_AUTH, "AUTH" },
    };

    for (size_t i = 0; i < sizeof(tab) / sizeof(tab[0]); i++) {
        if (tab[i].in == in) {
            *jso = json_object_new_string(tab[i].name);
            check_oom(*jso);
            return TSS2_RC_SUCCESS;
        }
    }
    return_error2(TSS2_FAPI_RC_BAD_VALUE, "Undefined constant: %"PRIx32, in);
}

/** Serialize value of type TPM2_HANDLE to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPM2_HANDLE.
 */
TSS2_RC
ifapi_json_TPM2_HANDLE_serialize(const TPM2_HANDLE in, json_object **jso)
{
    *jso = json_object_new_int(in);
    if (*jso == NULL) {
        LOG_ERROR("Bad value %"PRIx32 "", in);
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    return TSS2_RC_SUCCESS;
}
/** Serialize a TPMA_ALGORITHM to json.
 *
 * This function expects the Bitfield to be encoded as unsigned int in host-endianess.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the constant is not of type TPMA_ALGORITHM.
 */
TSS2_RC
ifapi_json_TPMA_ALGORITHM_serialize(const TPMA_ALGORITHM in, json_object **jso)
{
    static const struct { TPMA_ALGORITHM in; char *name; } tab[] = {
        { TPMA_ALGORITHM_ASYMMETRIC, "asymmetric" },
        { TPMA_ALGORITHM_SYMMETRIC, "symmetric" },
        { TPMA_ALGORITHM_HASH, "hash" },
        { TPMA_ALGORITHM_OBJECT, "object" },
        { TPMA_ALGORITHM_SIGNING, "signing" },
        { TPMA_ALGORITHM_ENCRYPTING, "encrypting" },
        { TPMA_ALGORITHM_METHOD, "method" },
    };

    UINT32 input;
    input = (UINT32) in;
    json_object *jso_bit;
    if (*jso == NULL) {
        *jso = json_object_new_object();
        return_if_null(*jso, "Out of memory.", TSS2_FAPI_RC_MEMORY);
    }
    for (size_t i = 0; i < sizeof(tab) / sizeof(tab[0]); i++) {
        if (tab[i].in & input)
            jso_bit = json_object_new_int(1);
        else
            jso_bit = json_object_new_int(0);
        return_if_null(jso_bit, "Out of memory.", TSS2_FAPI_RC_MEMORY);

        json_object_object_add(*jso, tab[i].name, jso_bit);
    }
    return TSS2_RC_SUCCESS;
}

/** Serialize a TPMA_OBJECT to json.
 *
 * This function expects the Bitfield to be encoded as unsigned int in host-endianess.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the constant is not of type TPMA_OBJECT.
 */
TSS2_RC
ifapi_json_TPMA_OBJECT_serialize(const TPMA_OBJECT in, json_object **jso)
{
    static const struct { TPMA_OBJECT in; char *name; } tab[] = {
        { TPMA_OBJECT_FIXEDTPM, "fixedTPM" },
        { TPMA_OBJECT_STCLEAR, "stClear" },
        { TPMA_OBJECT_FIXEDPARENT, "fixedParent" },
        { TPMA_OBJECT_SENSITIVEDATAORIGIN, "sensitiveDataOrigin" },
        { TPMA_OBJECT_USERWITHAUTH, "userWithAuth" },
        { TPMA_OBJECT_ADMINWITHPOLICY, "adminWithPolicy" },
        { TPMA_OBJECT_NODA, "noDA" },
        { TPMA_OBJECT_ENCRYPTEDDUPLICATION, "encryptedDuplication" },
        { TPMA_OBJECT_RESTRICTED, "restricted" },
        { TPMA_OBJECT_DECRYPT, "decrypt" },
        { TPMA_OBJECT_SIGN_ENCRYPT, "sign" },
    };
    UINT32 input;
    input = (UINT32) in;
    json_object *jso_bit;
    if (*jso == NULL) {
        *jso = json_object_new_object();
        return_if_null(*jso, "Out of memory.", TSS2_FAPI_RC_MEMORY);
    }
    for (size_t i = 0; i < sizeof(tab) / sizeof(tab[0]); i++) {
        if (tab[i].in & input)
            jso_bit = json_object_new_int(1);
        else
            jso_bit = json_object_new_int(0);
        return_if_null(jso_bit, "Out of memory.", TSS2_FAPI_RC_MEMORY);

        json_object_object_add(*jso, tab[i].name, jso_bit);
    }
    return TSS2_RC_SUCCESS;
}

/** Serialize a TPMA_LOCALITY to json.
 *
 * This function expects the Bitfield to be encoded as unsigned int in host-endianess.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the constant is not of type TPMA_LOCALITY.
 */
TSS2_RC
ifapi_json_TPMA_LOCALITY_serialize(const TPMA_LOCALITY in, json_object **jso)
{
    static const struct { TPMA_LOCALITY in; char *name; } tab[] = {
        { TPMA_LOCALITY_TPM2_LOC_ZERO, "ZERO" },
        { TPMA_LOCALITY_TPM2_LOC_ONE, "ONE" },
        { TPMA_LOCALITY_TPM2_LOC_TWO, "TWO" },
        { TPMA_LOCALITY_TPM2_LOC_THREE, "THREE" },
        { TPMA_LOCALITY_TPM2_LOC_FOUR, "FOUR" },
    };

    UINT8 input;
    input = (UINT8) in;
    json_object *jso_bit;
    json_object *jso_bit_idx;
    if (*jso == NULL) {
        *jso = json_object_new_object();
        return_if_null(*jso, "Out of memory.", TSS2_FAPI_RC_MEMORY);
    }
    for (size_t i = 0; i < sizeof(tab) / sizeof(tab[0]); i++) {
        if (tab[i].in & input)
            jso_bit = json_object_new_int(1);
        else
            jso_bit = json_object_new_int(0);
        return_if_null(jso_bit, "Out of memory.", TSS2_FAPI_RC_MEMORY);

        json_object_object_add(*jso, tab[i].name, jso_bit);
    }
    jso_bit_idx = json_object_new_int64((TPMA_LOCALITY_EXTENDED_MASK & input) >>
                                         5);
    return_if_null(jso_bit_idx, "Out of memory.", TSS2_FAPI_RC_MEMORY);

    json_object_object_add(*jso, "Extended", jso_bit_idx);

    return TSS2_RC_SUCCESS;
}

/** Serialize a TPMA_CC to json.
 *
 * This function expects the Bitfield to be encoded as unsigned int in host-endianess.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the constant is not of type TPMA_CC.
 */
TSS2_RC
ifapi_json_TPMA_CC_serialize(const TPMA_CC in, json_object **jso)
{
    static const struct { TPMA_CC in; char *name; } tab[] = {
        { TPMA_CC_NV, "nv" },
        { TPMA_CC_EXTENSIVE, "extensive" },
        { TPMA_CC_FLUSHED, "flushed" },
        { TPMA_CC_RHANDLE, "rHandle" },
        { TPMA_CC_V, "V" },
    };
    TPM2_CC input;
    input = (TPM2_CC) in;
    json_object *jso_bit;
    json_object *jso_bit_idx;
    if (*jso == NULL) {
        *jso = json_object_new_object();
        return_if_null(*jso, "Out of memory.", TSS2_FAPI_RC_MEMORY);
    }
    for (size_t i = 0; i < sizeof(tab) / sizeof(tab[0]); i++) {
        if (tab[i].in & input)
            jso_bit = json_object_new_int(1);
        else
            jso_bit = json_object_new_int(0);
        return_if_null(jso_bit, "Out of memory.", TSS2_FAPI_RC_MEMORY);

        json_object_object_add(*jso, tab[i].name, jso_bit);
    }
    jso_bit_idx = json_object_new_int64((TPMA_CC_COMMANDINDEX_MASK & input) >> 0);
    return_if_null(jso_bit_idx, "Out of memory.", TSS2_FAPI_RC_MEMORY);

    json_object_object_add(*jso, "commandIndex", jso_bit_idx);

    jso_bit_idx = json_object_new_int64((TPMA_CC_CHANDLES_MASK & input) >> 25);
    return_if_null(jso_bit_idx, "Out of memory.", TSS2_FAPI_RC_MEMORY);

    json_object_object_add(*jso, "cHandles", jso_bit_idx);

    jso_bit_idx = json_object_new_int64((TPMA_CC_RES_MASK & input) >> 30);
    return_if_null(jso_bit_idx, "Out of memory.", TSS2_FAPI_RC_MEMORY);

    json_object_object_add(*jso, "Res", jso_bit_idx);

    return TSS2_RC_SUCCESS;
}

/** Serialize a TPMA_ACT to json.
 *
 * This function expects the Bitfield to be encoded as unsigned int in host-endianess.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the constant is not of type TPMA_ACT.
 */
TSS2_RC
ifapi_json_TPMA_ACT_serialize(const TPMA_ACT in, json_object **jso)
{
    static const struct {TPMA_ACT in; char *name; } tab[] = {
        {TPMA_ACT_SIGNALED, "signaled"},
        {TPMA_ACT_PRESERVESIGNALED, "preserveSignaled"},
    };
    UINT32 input;
    input = (UINT32) in;
    json_object *jso_bit;

    if (*jso == NULL) {
        *jso = json_object_new_object();
        return_if_null(*jso, "Out of memory.", TSS2_FAPI_RC_MEMORY);
    }

    for (size_t i = 0; i < sizeof(tab) / sizeof(tab[0]); i++) {
        if (tab[i].in & input)
            jso_bit = json_object_new_int(1);
        else
            jso_bit = json_object_new_int(0);
        return_if_null(jso_bit, "Out of memory.", TSS2_FAPI_RC_MEMORY);

        json_object_object_add(*jso, tab[i].name, jso_bit);
    }
    return TSS2_RC_SUCCESS;
}

/** Serialize TPMI_YES_NO to json.
 *
 * @param[in] in variable to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 */
TSS2_RC
ifapi_json_TPMI_YES_NO_serialize(const TPMI_YES_NO in, json_object **jso)
{
    if (in == YES) {
        *jso = json_object_new_string("YES");
    } else if (in == NO) {
        *jso = json_object_new_string("NO");
    } else {
        return_error(TSS2_FAPI_RC_BAD_VALUE, "Undefined constant.");
    }
    check_oom(*jso);
    return TSS2_RC_SUCCESS;
}

/** Serialize TPMI_RH_HIERARCHY to json.
 *
 * @param[in] in variable to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 */
TSS2_RC
ifapi_json_TPMI_RH_HIERARCHY_serialize(const TPMI_RH_HIERARCHY in,
                                       json_object **jso)
{
    static const struct { TPMI_RH_HIERARCHY in; char *name; } tab[] = {
        { TPM2_RH_OWNER, "OWNER" },
        { TPM2_RH_PLATFORM, "PLATFORM" },
        { TPM2_RH_ENDORSEMENT, "ENDORSEMENT" },
        { TPM2_RH_NULL, "NULL" },
    };

    for (size_t i = 0; i < sizeof(tab) / sizeof(tab[0]); i++) {
        if (tab[i].in == in) {
            *jso = json_object_new_string(tab[i].name);
            check_oom(*jso);
            return TSS2_RC_SUCCESS;
        }
    }
    return_error(TSS2_FAPI_RC_BAD_VALUE, "Undefined constant.");
}

/** Serialize value of type TPMI_RH_NV_INDEX to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMI_RH_NV_INDEX.
 *
 */
TSS2_RC
ifapi_json_TPMI_RH_NV_INDEX_serialize(const TPMI_RH_NV_INDEX in,
                                      json_object **jso)
{
    if (in >= TPM2_NV_INDEX_FIRST && in <= TPM2_NV_INDEX_LAST) {
        *jso = json_object_new_int64(in);
    } else {
        return_error(TSS2_FAPI_RC_BAD_VALUE, "Undefined constant.");
    }
    return_if_null(*jso, "Out of memory.", TSS2_FAPI_RC_MEMORY);

    return TSS2_RC_SUCCESS;
}

/** Serialize TPMI_ALG_HASH to json.
 *
 * @param[in] in variable to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 */
TSS2_RC
ifapi_json_TPMI_ALG_HASH_serialize(const TPMI_ALG_HASH in, json_object **jso)
{
    CHECK_IN_LIST(TPMI_ALG_HASH, in, TPM2_ALG_SHA1, TPM2_ALG_SHA256, TPM2_ALG_SHA384,
                      TPM2_ALG_SHA512, TPM2_ALG_SM3_256, TPM2_ALG_NULL);
    return ifapi_json_TPM2_ALG_ID_serialize(in, jso);
}

/** Serialize TPMI_ALG_SYM_OBJECT to json.
 *
 * @param[in] in variable to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 */
TSS2_RC
ifapi_json_TPMI_ALG_SYM_OBJECT_serialize(const TPMI_ALG_SYM_OBJECT in,
        json_object **jso)
{
    CHECK_IN_LIST(TPMI_ALG_SYM_OBJECT, in, TPM2_ALG_AES, TPM2_ALG_CAMELLIA, TPM2_ALG_SM4, TPM2_ALG_NULL);
    return ifapi_json_TPM2_ALG_ID_serialize(in, jso);
}

/** Serialize TPMI_ALG_SYM_MODE to json.
 *
 * @param[in] in variable to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 */
TSS2_RC
ifapi_json_TPMI_ALG_SYM_MODE_serialize(const TPMI_ALG_SYM_MODE in,
                                       json_object **jso)
{
    CHECK_IN_LIST(TPMI_ALG_SYM_MODE, in, TPM2_ALG_CTR, TPM2_ALG_OFB,
        TPM2_ALG_CBC, TPM2_ALG_CFB, TPM2_ALG_ECB, TPM2_ALG_NULL);
    return ifapi_json_TPM2_ALG_ID_serialize(in, jso);
}

/** Serialize TPMI_ALG_CIPHER_MODE to json.
 *
 * @param[in] in variable to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 */
TSS2_RC
ifapi_json_TPMI_ALG_CIPHER_MODE_serialize(const TPMI_ALG_CIPHER_MODE in,
                                          json_object **jso)
{
    CHECK_IN_LIST(TPMI_ALG_CIPHER_MODE, in, TPM2_ALG_CTR, TPM2_ALG_OFB,
        TPM2_ALG_CBC, TPM2_ALG_CFB, TPM2_ALG_ECB, TPM2_ALG_NULL);
    return ifapi_json_TPM2_ALG_ID_serialize(in, jso);
}

/** Serialize TPMI_ALG_KDF to json.
 *
 * @param[in] in variable to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 */
TSS2_RC
ifapi_json_TPMI_ALG_KDF_serialize(const TPMI_ALG_KDF in, json_object **jso)
{
    CHECK_IN_LIST(TPMI_ALG_KDF, in, TPM2_ALG_MGF1, TPM2_ALG_KDF1_SP800_56A,
        TPM2_ALG_KDF1_SP800_108, TPM2_ALG_NULL);
    return ifapi_json_TPM2_ALG_ID_serialize(in, jso);
}

/** Serialize TPMI_ALG_SIG_SCHEME to json.
 *
 * @param[in] in variable to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 */
TSS2_RC
ifapi_json_TPMI_ALG_SIG_SCHEME_serialize(const TPMI_ALG_SIG_SCHEME in,
        json_object **jso)
{
    CHECK_IN_LIST(TPMI_ALG_SIG_SCHEME, in, TPM2_ALG_RSASSA, TPM2_ALG_RSAPSS,
        TPM2_ALG_ECDSA, TPM2_ALG_ECDAA, TPM2_ALG_SM2, TPM2_ALG_ECSCHNORR,
        TPM2_ALG_HMAC, TPM2_ALG_NULL);
    return ifapi_json_TPM2_ALG_ID_serialize(in, jso);
}

/**  Serialize a TPMU_HA to json.
 *
 * This function expects the Bitfield to be encoded as unsigned int in host-endianess.
 * @param[in] in the value to be serialized.
 * @param[in] selector the type of the HA object.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMU_HA.
 */
TSS2_RC
ifapi_json_TPMU_HA_serialize(const TPMU_HA *in, UINT32 selector,
                             json_object **jso)
{
    size_t size;
    const uint8_t *buffer;

    switch (selector) {
    case TPM2_ALG_SHA1:
        size = TPM2_SHA1_DIGEST_SIZE;
        buffer = &in->sha1[0];
        break;
    case TPM2_ALG_SHA256:
        size = TPM2_SHA256_DIGEST_SIZE;
        buffer = &in->sha256[0];
        break;
    case TPM2_ALG_SHA384:
        size = TPM2_SHA384_DIGEST_SIZE;
        buffer = &in->sha384[0];
        break;
    case TPM2_ALG_SHA512:
        size = TPM2_SHA512_DIGEST_SIZE;
        buffer = &in->sha512[0];
        break;
    case TPM2_ALG_SM3_256:
        size = TPM2_SM3_256_DIGEST_SIZE;
        buffer = &in->sm3_256[0];
        break;
    default:
        LOG_ERROR("\nSelector %"PRIx32 " did not match", selector);
        return TSS2_FAPI_RC_BAD_VALUE;
    };
    char hex_string[(size) * 2 + 1];
    for (size_t i = 0, off = 0; i < size; i++, off += 2)
        sprintf(&hex_string[off], "%02x", buffer[i]);
    hex_string[(size) * 2] = '\0';
    *jso = json_object_new_string(hex_string);
    return_if_null(*jso, "Out of memory.", TSS2_FAPI_RC_MEMORY);

    return TSS2_RC_SUCCESS;
}

/** Serialize value of type TPMT_HA to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMT_HA.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMT_HA_serialize(const TPMT_HA *in, json_object **jso)
{
    return_if_null(in, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    TSS2_RC r;
    json_object *jso2;
    if (*jso == NULL)
        *jso = json_object_new_object();
    jso2 = NULL;
    r = ifapi_json_TPMI_ALG_HASH_serialize(in->hashAlg, &jso2);
    return_if_error(r, "Serialize TPMI_ALG_HASH");

    json_object_object_add(*jso, "hashAlg", jso2);
    if (in->hashAlg != TPM2_ALG_NULL) {
        json_object *jso2 = NULL;
        r = ifapi_json_TPMU_HA_serialize(&in->digest, in->hashAlg, &jso2);
        return_if_error(r, "Serialize TPMU_HA");

        json_object_object_add(*jso, "digest", jso2);
    }
    return TSS2_RC_SUCCESS;
}

/** Serialize value of type TPM2B_DIGEST to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPM2B_DIGEST.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPM2B_DIGEST_serialize(const TPM2B_DIGEST *in, json_object **jso)
{
    return_if_null(in, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    if (in->size > sizeof(TPMU_HA)) {
        LOG_ERROR("Too many bytes for array (%"PRIuPTR" > %"PRIuPTR" = sizeof(TPMU_HA))",
                  (size_t)in->size, (size_t)sizeof(TPMU_HA));
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    char hex_string[((size_t)in->size)*2+1];

    for (size_t i = 0, off = 0; i < in->size; i++, off+=2)
        sprintf(&hex_string[off], "%02x", in->buffer[i]);
    hex_string[(in->size)*2] = '\0';
    *jso = json_object_new_string (hex_string);
    return_if_null(*jso, "Out of memory.", TSS2_FAPI_RC_MEMORY);

    return TSS2_RC_SUCCESS;
}

/** Serialize value of type TPM2B_DATA to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPM2B_DATA.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPM2B_DATA_serialize(const TPM2B_DATA *in, json_object **jso)
{
    return_if_null(in, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    if (in->size > sizeof(TPMU_HA)) {
        LOG_ERROR("Too many bytes for array (%"PRIuPTR" > %"PRIuPTR" = sizeof(TPMT_HA))",
                  (size_t)in->size, (size_t)sizeof(TPMT_HA));
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    char hex_string[sizeof(TPMT_HA)*2+1];

    for (size_t i = 0, off = 0; i < in->size; i++, off+=2)
        sprintf(&hex_string[off], "%02x", in->buffer[i]);
    hex_string[(in->size)*2] = '\0';
    *jso = json_object_new_string (hex_string);
    return_if_null(*jso, "Out of memory.", TSS2_FAPI_RC_MEMORY);

    return TSS2_RC_SUCCESS;
}

/** Serialize a TPM2B_NONCE to json.
 *
 * @param[in] in value of type TPM2B_NONCE to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPM2B_NONCE.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPM2B_NONCE_serialize(const TPM2B_NONCE *in, json_object **jso)
{
    return ifapi_json_TPM2B_DIGEST_serialize(in, jso);
}

/** Serialize a TPM2B_OPERAND to json.
 *
 * @param[in] in value of type TPM2B_OPERAND to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPM2B_OPERAND.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPM2B_OPERAND_serialize(const TPM2B_OPERAND *in, json_object **jso)
{
    return ifapi_json_TPM2B_DIGEST_serialize(in, jso);
}

/** Serialize value of type TPM2B_EVENT to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPM2B_EVENT.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPM2B_EVENT_serialize(const TPM2B_EVENT *in, json_object **jso)
{
    return_if_null(in, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    if (in->size > 1024) {
        LOG_ERROR("Too many bytes for array (%"PRIuPTR" > %"PRIuPTR" = 1024)",
                  (size_t)in->size, (size_t)1024);
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    char hex_string[((size_t)in->size)*2+1];

    for (size_t i = 0, off = 0; i < in->size; i++, off+=2)
        sprintf(&hex_string[off], "%02x", in->buffer[i]);
    hex_string[(in->size)*2] = '\0';
    *jso = json_object_new_string (hex_string);
    return_if_null(*jso, "Out of memory.", TSS2_FAPI_RC_MEMORY);

    return TSS2_RC_SUCCESS;
}

/** Serialize value of type TPM2B_MAX_NV_BUFFER to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPM2B_MAX_NV_BUFFER.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPM2B_MAX_NV_BUFFER_serialize(const TPM2B_MAX_NV_BUFFER *in, json_object **jso)
{
    return_if_null(in, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    if (in->size > TPM2_MAX_NV_BUFFER_SIZE) {
        LOG_ERROR("Too many bytes for array (%"PRIuPTR" > %"PRIuPTR" = TPM2_MAX_NV_BUFFER_SIZE)",
                  (size_t)in->size, (size_t)TPM2_MAX_NV_BUFFER_SIZE);
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    char hex_string[((size_t)in->size)*2+1];

    for (size_t i = 0, off = 0; i < in->size; i++, off+=2)
        sprintf(&hex_string[off], "%02x", in->buffer[i]);
    hex_string[(in->size)*2] = '\0';
    *jso = json_object_new_string (hex_string);
    return_if_null(*jso, "Out of memory.", TSS2_FAPI_RC_MEMORY);

    return TSS2_RC_SUCCESS;
}

/** Serialize value of type TPM2B_NAME to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPM2B_NAME.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPM2B_NAME_serialize(const TPM2B_NAME *in, json_object **jso)
{
    return_if_null(in, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    if (in->size > sizeof(TPMU_NAME)) {
        LOG_ERROR("Too many bytes for array (%"PRIuPTR" > %"PRIuPTR" = sizeof(TPMU_NAME))",
                  (size_t)in->size, (size_t)sizeof(TPMU_NAME));
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    char hex_string[((size_t)in->size)*2+1];

    for (size_t i = 0, off = 0; i < in->size; i++, off+=2)
        sprintf(&hex_string[off], "%02x", in->name[i]);
    hex_string[(in->size)*2] = '\0';
    *jso = json_object_new_string (hex_string);
    return_if_null(*jso, "Out of memory.", TSS2_FAPI_RC_MEMORY);

    return TSS2_RC_SUCCESS;
}

/** Serialize value of type TPMT_TK_CREATION to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMT_TK_CREATION.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMT_TK_CREATION_serialize(const TPMT_TK_CREATION *in, json_object **jso)
{
    return_if_null(in, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    TSS2_RC r;
    json_object *jso2;
    if (*jso == NULL)
        *jso = json_object_new_object ();
    if (in != NULL && in->tag != TPM2_ST_CREATION) {
        LOG_ERROR("BAD VALUE %"PRIuPTR" != %"PRIuPTR,(size_t)in->tag,(size_t)TPM2_ST_CREATION);
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    jso2 = NULL;
    r = ifapi_json_TPM2_ST_serialize(in->tag, &jso2);
    return_if_error(r, "Serialize TPM2_ST");

    json_object_object_add(*jso, "tag", jso2);
    jso2 = NULL;
    r = ifapi_json_TPMI_RH_HIERARCHY_serialize(in->hierarchy, &jso2);
    return_if_error(r, "Serialize TPMI_RH_HIERARCHY");

    json_object_object_add(*jso, "hierarchy", jso2);
    jso2 = NULL;
    r = ifapi_json_TPM2B_DIGEST_serialize(&in->digest, &jso2);
    return_if_error(r, "Serialize TPM2B_DIGEST");

    json_object_object_add(*jso, "digest", jso2);
    return TSS2_RC_SUCCESS;
}

/** Serialize value of type TPMS_ALG_PROPERTY to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMS_ALG_PROPERTY.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_ALG_PROPERTY_serialize(const TPMS_ALG_PROPERTY *in, json_object **jso)
{
    return_if_null(in, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    TSS2_RC r;
    json_object *jso2;
    if (*jso == NULL)
        *jso = json_object_new_object ();
    jso2 = NULL;
    r = ifapi_json_TPM2_ALG_ID_serialize(in->alg, &jso2);
    return_if_error(r, "Serialize TPM2_ALG_ID");

    json_object_object_add(*jso, "alg", jso2);
    jso2 = NULL;
    r = ifapi_json_TPMA_ALGORITHM_serialize(in->algProperties, &jso2);
    return_if_error(r, "Serialize TPMA_ALGORITHM");

    json_object_object_add(*jso, "algProperties", jso2);
    return TSS2_RC_SUCCESS;
}

/** Serialize value of type TPMS_TAGGED_PROPERTY to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMS_TAGGED_PROPERTY.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_TAGGED_PROPERTY_serialize(const TPMS_TAGGED_PROPERTY *in, json_object **jso)
{
    return_if_null(in, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    TSS2_RC r;
    json_object *jso2;
    if (*jso == NULL)
        *jso = json_object_new_object ();
    jso2 = NULL;
    r = ifapi_json_TPM2_PT_serialize(in->property, &jso2);
    return_if_error(r, "Serialize TPM2_PT");

    json_object_object_add(*jso, "property", jso2);
    jso2 = NULL;
    r = ifapi_json_UINT32_serialize(in->value, &jso2);
    return_if_error(r, "Serialize UINT32");

    json_object_object_add(*jso, "value", jso2);
    return TSS2_RC_SUCCESS;
}

/** Serialize value of type TPML_CC to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPML_CC.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPML_CC_serialize(const TPML_CC *in, json_object **jso)
{
    return_if_null(in, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    TSS2_RC r;
    if (in->count > TPM2_MAX_CAP_CC) {
        LOG_ERROR("Too many bytes for array (%"PRIuPTR" > %"PRIuPTR" = TPM2_MAX_CAP_CC)",
                  (size_t)in->count, (size_t)TPM2_MAX_CAP_CC);
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    *jso = json_object_new_array();
    return_if_null(*jso, "Out of memory.", TSS2_FAPI_RC_MEMORY);

    for (size_t i=0; i < in->count; i++) {
        json_object *jso2 = NULL;
        r = ifapi_json_TPM2_CC_serialize (in->commandCodes[i], &jso2);
        return_if_error(r, "Serialize TPM2_CC");

        json_object_array_add(*jso, jso2);
    }
    return TSS2_RC_SUCCESS;
}

/** Serialize value of type TPML_CCA to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPML_CCA.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPML_CCA_serialize(const TPML_CCA *in, json_object **jso)
{
    return_if_null(in, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    TSS2_RC r;
    if (in->count > TPM2_MAX_CAP_CC) {
        LOG_ERROR("Too many bytes for array (%"PRIuPTR" > %"PRIuPTR" = TPM2_MAX_CAP_CC)",
                  (size_t)in->count, (size_t)TPM2_MAX_CAP_CC);
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    *jso = json_object_new_array();
    return_if_null(*jso, "Out of memory.", TSS2_FAPI_RC_MEMORY);

    for (size_t i=0; i < in->count; i++) {
        json_object *jso2 = NULL;
        r = ifapi_json_TPMA_CC_serialize (in->commandAttributes[i], &jso2);
        return_if_error(r, "Serialize TPMA_CC");

        json_object_array_add(*jso, jso2);
    }
    return TSS2_RC_SUCCESS;
}

/** Serialize value of type TPML_HANDLE to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPML_HANDLE.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPML_HANDLE_serialize(const TPML_HANDLE *in, json_object **jso)
{
    return_if_null(in, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    TSS2_RC r;
    if (in->count > TPM2_MAX_CAP_HANDLES) {
        LOG_ERROR("Too many bytes for array (%"PRIuPTR" > %"PRIuPTR" = TPM2_MAX_CAP_HANDLES)",
                  (size_t)in->count, (size_t)TPM2_MAX_CAP_HANDLES);
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    *jso = json_object_new_array();
    return_if_null(*jso, "Out of memory.", TSS2_FAPI_RC_MEMORY);

    for (size_t i=0; i < in->count; i++) {
        json_object *jso2 = NULL;
        r = ifapi_json_TPM2_HANDLE_serialize (in->handle[i], &jso2);
        return_if_error(r, "Serialize TPM2_HANDLE");

        json_object_array_add(*jso, jso2);
    }
    return TSS2_RC_SUCCESS;
}

/** Serialize value of type TPML_DIGEST_VALUES to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPML_DIGEST_VALUES.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPML_DIGEST_VALUES_serialize(const TPML_DIGEST_VALUES *in, json_object **jso)
{
    return_if_null(in, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    TSS2_RC r;
    if (in->count > TPM2_NUM_PCR_BANKS) {
        LOG_ERROR("Too many bytes for array (%"PRIuPTR" > %"PRIuPTR" = TPM2_NUM_PCR_BANKS)",
                  (size_t)in->count, (size_t)TPM2_NUM_PCR_BANKS);
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    *jso = json_object_new_array();
    return_if_null(*jso, "Out of memory.", TSS2_FAPI_RC_MEMORY);

    for (size_t i=0; i < in->count; i++) {
        json_object *jso2 = NULL;
        r = ifapi_json_TPMT_HA_serialize (&in->digests[i], &jso2);
        return_if_error(r, "Serialize TPMT_HA");

        json_object_array_add(*jso, jso2);
    }
    return TSS2_RC_SUCCESS;
}

/** Serialize value of type TPML_PCR_SELECTION to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPML_PCR_SELECTION.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPML_PCR_SELECTION_serialize(const TPML_PCR_SELECTION *in, json_object **jso)
{
    return_if_null(in, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    TSS2_RC r;
    if (in->count > TPM2_NUM_PCR_BANKS) {
        LOG_ERROR("Too many bytes for array (%"PRIuPTR" > %"PRIuPTR" = TPM2_NUM_PCR_BANKS)",
                  (size_t)in->count, (size_t)TPM2_NUM_PCR_BANKS);
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    *jso = json_object_new_array();
    return_if_null(*jso, "Out of memory.", TSS2_FAPI_RC_MEMORY);

    for (size_t i=0; i < in->count; i++) {
        json_object *jso2 = NULL;
        r = ifapi_json_TPMS_PCR_SELECTION_serialize (&in->pcrSelections[i], &jso2);
        return_if_error(r, "Serialize TPMS_PCR_SELECTION");

        json_object_array_add(*jso, jso2);
    }
    return TSS2_RC_SUCCESS;
}

/** Serialize value of type TPML_ALG_PROPERTY to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPML_ALG_PROPERTY.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPML_ALG_PROPERTY_serialize(const TPML_ALG_PROPERTY *in, json_object **jso)
{
    return_if_null(in, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    TSS2_RC r;
    if (in->count > TPM2_MAX_CAP_ALGS) {
        LOG_ERROR("Too many bytes for array (%"PRIuPTR" > %"PRIuPTR" = TPM2_MAX_CAP_ALGS)",
                  (size_t)in->count, (size_t)TPM2_MAX_CAP_ALGS);
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    *jso = json_object_new_array();
    return_if_null(*jso, "Out of memory.", TSS2_FAPI_RC_MEMORY);

    for (size_t i=0; i < in->count; i++) {
        json_object *jso2 = NULL;
        r = ifapi_json_TPMS_ALG_PROPERTY_serialize (&in->algProperties[i], &jso2);
        return_if_error(r, "Serialize TPMS_ALG_PROPERTY");

        json_object_array_add(*jso, jso2);
    }
    return TSS2_RC_SUCCESS;
}

/** Serialize value of type TPML_TAGGED_TPM_PROPERTY to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPML_TAGGED_TPM_PROPERTY.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPML_TAGGED_TPM_PROPERTY_serialize(const TPML_TAGGED_TPM_PROPERTY *in, json_object **jso)
{
    return_if_null(in, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    TSS2_RC r;
    if (in->count > TPM2_MAX_TPM_PROPERTIES) {
        LOG_ERROR("Too many bytes for array (%"PRIuPTR" > %"PRIuPTR" = TPM2_MAX_TPM_PROPERTIES)",
                  (size_t)in->count, (size_t)TPM2_MAX_TPM_PROPERTIES);
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    *jso = json_object_new_array();
    return_if_null(*jso, "Out of memory.", TSS2_FAPI_RC_MEMORY);

    for (size_t i=0; i < in->count; i++) {
        json_object *jso2 = NULL;
        r = ifapi_json_TPMS_TAGGED_PROPERTY_serialize (&in->tpmProperty[i], &jso2);
        return_if_error(r, "Serialize TPMS_TAGGED_PROPERTY");

        json_object_array_add(*jso, jso2);
    }
    return TSS2_RC_SUCCESS;
}

/** Serialize value of type TPML_TAGGED_PCR_PROPERTY to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPML_TAGGED_PCR_PROPERTY.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPML_TAGGED_PCR_PROPERTY_serialize(const TPML_TAGGED_PCR_PROPERTY *in, json_object **jso)
{
    return_if_null(in, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    TSS2_RC r;
    if (in->count > TPM2_MAX_PCR_PROPERTIES) {
        LOG_ERROR("Too many bytes for array (%"PRIuPTR" > %"PRIuPTR" = TPM2_MAX_PCR_PROPERTIES)",
                  (size_t)in->count, (size_t)TPM2_MAX_PCR_PROPERTIES);
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    *jso = json_object_new_array();
    return_if_null(*jso, "Out of memory.", TSS2_FAPI_RC_MEMORY);

    for (size_t i=0; i < in->count; i++) {
        json_object *jso2 = NULL;
        r = ifapi_json_TPMS_TAGGED_PCR_SELECT_serialize (&in->pcrProperty[i], &jso2);
        return_if_error(r, "Serialize TPMS_TAGGED_PCR_SELECT");

        json_object_array_add(*jso, jso2);
    }
    return TSS2_RC_SUCCESS;
}

/** Serialize value of type TPML_ECC_CURVE to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPML_ECC_CURVE.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPML_ECC_CURVE_serialize(const TPML_ECC_CURVE *in, json_object **jso)
{
    return_if_null(in, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    TSS2_RC r;
    if (in->count > TPM2_MAX_ECC_CURVES) {
        LOG_ERROR("Too many bytes for array (%"PRIuPTR" > %"PRIuPTR" = TPM2_MAX_ECC_CURVES)",
                  (size_t)in->count, (size_t)TPM2_MAX_ECC_CURVES);
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    *jso = json_object_new_array();
    return_if_null(*jso, "Out of memory.", TSS2_FAPI_RC_MEMORY);

    for (size_t i=0; i < in->count; i++) {
        json_object *jso2 = NULL;
        r = ifapi_json_TPM2_ECC_CURVE_serialize (in->eccCurves[i], &jso2);
        return_if_error(r, "Serialize TPM2_ECC_CURVE");

        json_object_array_add(*jso, jso2);
    }
    return TSS2_RC_SUCCESS;
}

/** Serialize value of type TPML_TAGGED_POLICY to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPML_TAGGED_POLICY.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPML_TAGGED_POLICY_serialize(const TPML_TAGGED_POLICY *in, json_object **jso)
{
    return_if_null(in, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    TSS2_RC r;
    if (in->count > TPM2_MAX_TAGGED_POLICIES) {
        LOG_ERROR("Too many bytes for array (%"PRIuPTR" > %"PRIuPTR" = TPM2_MAX_TAGGED_POLICIES)",
            (size_t)in->count, (size_t)TPM2_MAX_TAGGED_POLICIES);
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    *jso = json_object_new_array();
    return_if_null(*jso, "Out of memory.", TSS2_FAPI_RC_MEMORY);

    for (size_t i=0; i < in->count; i++) {
        json_object *jso2 = NULL;
        r = ifapi_json_TPMS_TAGGED_POLICY_serialize (&in->policies[i], &jso2);
        return_if_error(r, "Serialize TPMS_TAGGED_POLICY");

        json_object_array_add(*jso, jso2);
    }
    return TSS2_RC_SUCCESS;
}

/** Serialize value of type TPML_ACT_DATA to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPML_ACT_DATA.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPML_ACT_DATA_serialize(const TPML_ACT_DATA *in, json_object **jso)
{
    return_if_null(in, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    TSS2_RC r;
    if (in->count > TPM2_MAX_ACT_DATA) {
        LOG_ERROR("Too many bytes for array (%"PRIuPTR" > %"PRIuPTR" = TPM2_MAX_ACT_DATA)",
            (size_t)in->count, (size_t)TPM2_MAX_ACT_DATA);
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    *jso = json_object_new_array();
    return_if_null(*jso, "Out of memory.", TSS2_FAPI_RC_MEMORY);

    for (size_t i=0; i < in->count; i++) {
        json_object *jso2 = NULL;
        r = ifapi_json_TPMS_ACT_DATA_serialize(&in->actData[i], &jso2);
        return_if_error(r, "Serialize TPMS_ACT_DATA");

        json_object_array_add(*jso, jso2);
    }
    return TSS2_RC_SUCCESS;
}

/**  Serialize a TPMU_CAPABILITIES to json.
 *
 * This function expects the Bitfield to be encoded as unsigned int in host-endianess.
 * @param[in] in the value to be serialized.
 * @param[in] selector the type of the capabilities.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMU_CAPABILITIES.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMU_CAPABILITIES_serialize(const TPMU_CAPABILITIES *in, UINT32 selector, json_object **jso)
{
    switch (selector) {
        case TPM2_CAP_ALGS:
            return ifapi_json_TPML_ALG_PROPERTY_serialize(&in->algorithms, jso);
        case TPM2_CAP_HANDLES:
            return ifapi_json_TPML_HANDLE_serialize(&in->handles, jso);
        case TPM2_CAP_COMMANDS:
            return ifapi_json_TPML_CCA_serialize(&in->command, jso);
        case TPM2_CAP_PP_COMMANDS:
            return ifapi_json_TPML_CC_serialize(&in->ppCommands, jso);
        case TPM2_CAP_AUDIT_COMMANDS:
            return ifapi_json_TPML_CC_serialize(&in->auditCommands, jso);
        case TPM2_CAP_PCRS:
            return ifapi_json_TPML_PCR_SELECTION_serialize(&in->assignedPCR, jso);
        case TPM2_CAP_TPM_PROPERTIES:
            return ifapi_json_TPML_TAGGED_TPM_PROPERTY_serialize(&in->tpmProperties, jso);
        case TPM2_CAP_PCR_PROPERTIES:
            return ifapi_json_TPML_TAGGED_PCR_PROPERTY_serialize(&in->pcrProperties, jso);
        case TPM2_CAP_ECC_CURVES:
            return ifapi_json_TPML_ECC_CURVE_serialize(&in->eccCurves, jso);
        case TPM2_CAP_AUTH_POLICIES:
            return ifapi_json_TPML_TAGGED_POLICY_serialize(&in->authPolicies, jso);
        case TPM2_CAP_ACT:
            return ifapi_json_TPML_ACT_DATA_serialize(&in->actData, jso);
        default:
            LOG_ERROR("\nSelector %"PRIx32 " did not match", selector);
            return TSS2_FAPI_RC_BAD_VALUE;
    };
    return TSS2_RC_SUCCESS;
}

/** Serialize value of type TPMS_CAPABILITY_DATA to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMS_CAPABILITY_DATA.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_CAPABILITY_DATA_serialize(const TPMS_CAPABILITY_DATA *in, json_object **jso)
{
    return_if_null(in, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    TSS2_RC r;
    json_object *jso2;
    if (*jso == NULL)
        *jso = json_object_new_object ();
    jso2 = NULL;
    r = ifapi_json_TPM2_CAP_serialize(in->capability, &jso2);
    return_if_error(r, "Serialize TPM2_CAP");

    json_object_object_add(*jso, "capability", jso2);
    jso2 = NULL;
    r = ifapi_json_TPMU_CAPABILITIES_serialize(&in->data, in->capability, &jso2);
    return_if_error(r,"Serialize TPMU_CAPABILITIES");

    json_object_object_add(*jso, "data", jso2);
    return TSS2_RC_SUCCESS;
}

/** Serialize value of type TPMS_CLOCK_INFO to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMS_CLOCK_INFO.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_CLOCK_INFO_serialize(const TPMS_CLOCK_INFO *in, json_object **jso)
{
    return_if_null(in, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    TSS2_RC r;
    json_object *jso2;
    if (*jso == NULL)
        *jso = json_object_new_object ();
    jso2 = NULL;
    r = ifapi_json_UINT64_serialize(in->clock, &jso2);
    return_if_error(r, "Serialize UINT64");

    json_object_object_add(*jso, "clock", jso2);
    jso2 = NULL;
    r = ifapi_json_UINT32_serialize(in->resetCount, &jso2);
    return_if_error(r, "Serialize UINT32");

    json_object_object_add(*jso, "resetCount", jso2);
    jso2 = NULL;
    r = ifapi_json_UINT32_serialize(in->restartCount, &jso2);
    return_if_error(r, "Serialize UINT32");

    json_object_object_add(*jso, "restartCount", jso2);
    jso2 = NULL;
    r = ifapi_json_TPMI_YES_NO_serialize(in->safe, &jso2);
    return_if_error(r, "Serialize TPMI_YES_NO");

    json_object_object_add(*jso, "safe", jso2);
    return TSS2_RC_SUCCESS;
}

/** Serialize value of type TPMS_TIME_INFO to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMS_TIME_INFO.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_TIME_INFO_serialize(const TPMS_TIME_INFO *in, json_object **jso)
{
    return_if_null(in, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    TSS2_RC r;
    json_object *jso2;
    if (*jso == NULL)
        *jso = json_object_new_object ();
    jso2 = NULL;
    r = ifapi_json_UINT64_serialize(in->time, &jso2);
    return_if_error(r, "Serialize UINT64");

    json_object_object_add(*jso, "time", jso2);
    jso2 = NULL;
    r = ifapi_json_TPMS_CLOCK_INFO_serialize(&in->clockInfo, &jso2);
    return_if_error(r, "Serialize TPMS_CLOCK_INFO");

    json_object_object_add(*jso, "clockInfo", jso2);
    return TSS2_RC_SUCCESS;
}

/** Serialize value of type TPMS_TIME_ATTEST_INFO to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMS_TIME_ATTEST_INFO.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_TIME_ATTEST_INFO_serialize(const TPMS_TIME_ATTEST_INFO *in, json_object **jso)
{
    return_if_null(in, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    TSS2_RC r;
    json_object *jso2;
    if (*jso == NULL)
        *jso = json_object_new_object ();
    jso2 = NULL;
    r = ifapi_json_TPMS_TIME_INFO_serialize(&in->time, &jso2);
    return_if_error(r, "Serialize TPMS_TIME_INFO");

    json_object_object_add(*jso, "time", jso2);
    jso2 = NULL;
    r = ifapi_json_UINT64_serialize(in->firmwareVersion, &jso2);
    return_if_error(r, "Serialize UINT64");

    json_object_object_add(*jso, "firmwareVersion", jso2);
    return TSS2_RC_SUCCESS;
}

/** Serialize value of type TPMS_CERTIFY_INFO to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMS_CERTIFY_INFO.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_CERTIFY_INFO_serialize(const TPMS_CERTIFY_INFO *in, json_object **jso)
{
    return_if_null(in, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    TSS2_RC r;
    json_object *jso2;
    if (*jso == NULL)
        *jso = json_object_new_object ();
    jso2 = NULL;
    r = ifapi_json_TPM2B_NAME_serialize(&in->name, &jso2);
    return_if_error(r, "Serialize TPM2B_NAME");

    json_object_object_add(*jso, "name", jso2);
    jso2 = NULL;
    r = ifapi_json_TPM2B_NAME_serialize(&in->qualifiedName, &jso2);
    return_if_error(r, "Serialize TPM2B_NAME");

    json_object_object_add(*jso, "qualifiedName", jso2);
    return TSS2_RC_SUCCESS;
}

/** Serialize value of type TPMS_QUOTE_INFO to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMS_QUOTE_INFO.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_QUOTE_INFO_serialize(const TPMS_QUOTE_INFO *in, json_object **jso)
{
    return_if_null(in, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    TSS2_RC r;
    json_object *jso2;
    if (*jso == NULL)
        *jso = json_object_new_object ();
    jso2 = NULL;
    r = ifapi_json_TPML_PCR_SELECTION_serialize(&in->pcrSelect, &jso2);
    return_if_error(r, "Serialize TPML_PCR_SELECTION");

    json_object_object_add(*jso, "pcrSelect", jso2);
    jso2 = NULL;
    r = ifapi_json_TPM2B_DIGEST_serialize(&in->pcrDigest, &jso2);
    return_if_error(r, "Serialize TPM2B_DIGEST");

    json_object_object_add(*jso, "pcrDigest", jso2);
    return TSS2_RC_SUCCESS;
}

/** Serialize value of type TPMS_COMMAND_AUDIT_INFO to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMS_COMMAND_AUDIT_INFO.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_COMMAND_AUDIT_INFO_serialize(const TPMS_COMMAND_AUDIT_INFO *in, json_object **jso)
{
    return_if_null(in, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    TSS2_RC r;
    json_object *jso2;
    if (*jso == NULL)
        *jso = json_object_new_object ();
    jso2 = NULL;
    r = ifapi_json_UINT64_serialize(in->auditCounter, &jso2);
    return_if_error(r, "Serialize UINT64");

    json_object_object_add(*jso, "auditCounter", jso2);
    jso2 = NULL;
    r = ifapi_json_TPM2_ALG_ID_serialize(in->digestAlg, &jso2);
    return_if_error(r, "Serialize TPM2_ALG_ID");

    json_object_object_add(*jso, "digestAlg", jso2);
    jso2 = NULL;
    r = ifapi_json_TPM2B_DIGEST_serialize(&in->auditDigest, &jso2);
    return_if_error(r, "Serialize TPM2B_DIGEST");

    json_object_object_add(*jso, "auditDigest", jso2);
    jso2 = NULL;
    r = ifapi_json_TPM2B_DIGEST_serialize(&in->commandDigest, &jso2);
    return_if_error(r, "Serialize TPM2B_DIGEST");

    json_object_object_add(*jso, "commandDigest", jso2);
    return TSS2_RC_SUCCESS;
}

/** Serialize value of type TPMS_SESSION_AUDIT_INFO to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMS_SESSION_AUDIT_INFO.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_SESSION_AUDIT_INFO_serialize(const TPMS_SESSION_AUDIT_INFO *in, json_object **jso)
{
    return_if_null(in, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    TSS2_RC r;
    json_object *jso2;
    if (*jso == NULL)
        *jso = json_object_new_object ();
    jso2 = NULL;
    r = ifapi_json_TPMI_YES_NO_serialize(in->exclusiveSession, &jso2);
    return_if_error(r, "Serialize TPMI_YES_NO");

    json_object_object_add(*jso, "exclusiveSession", jso2);
    jso2 = NULL;
    r = ifapi_json_TPM2B_DIGEST_serialize(&in->sessionDigest, &jso2);
    return_if_error(r, "Serialize TPM2B_DIGEST");

    json_object_object_add(*jso, "sessionDigest", jso2);
    return TSS2_RC_SUCCESS;
}

/** Serialize value of type TPMS_CREATION_INFO to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMS_CREATION_INFO.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_CREATION_INFO_serialize(const TPMS_CREATION_INFO *in, json_object **jso)
{
    return_if_null(in, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    TSS2_RC r;
    json_object *jso2;
    if (*jso == NULL)
        *jso = json_object_new_object ();
    jso2 = NULL;
    r = ifapi_json_TPM2B_NAME_serialize(&in->objectName, &jso2);
    return_if_error(r, "Serialize TPM2B_NAME");

    json_object_object_add(*jso, "objectName", jso2);
    jso2 = NULL;
    r = ifapi_json_TPM2B_DIGEST_serialize(&in->creationHash, &jso2);
    return_if_error(r, "Serialize TPM2B_DIGEST");

    json_object_object_add(*jso, "creationHash", jso2);
    return TSS2_RC_SUCCESS;
}

/** Serialize value of type TPMS_NV_CERTIFY_INFO to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMS_NV_CERTIFY_INFO.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_NV_CERTIFY_INFO_serialize(const TPMS_NV_CERTIFY_INFO *in, json_object **jso)
{
    return_if_null(in, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    TSS2_RC r;
    json_object *jso2;
    if (*jso == NULL)
        *jso = json_object_new_object ();
    jso2 = NULL;
    r = ifapi_json_TPM2B_NAME_serialize(&in->indexName, &jso2);
    return_if_error(r, "Serialize TPM2B_NAME");

    json_object_object_add(*jso, "indexName", jso2);
    jso2 = NULL;
    r = ifapi_json_UINT16_serialize(in->offset, &jso2);
    return_if_error(r, "Serialize UINT16");

    json_object_object_add(*jso, "offset", jso2);
    jso2 = NULL;
    r = ifapi_json_TPM2B_MAX_NV_BUFFER_serialize(&in->nvContents, &jso2);
    return_if_error(r, "Serialize TPM2B_MAX_NV_BUFFER");

    json_object_object_add(*jso, "nvContents", jso2);
    return TSS2_RC_SUCCESS;
}

/** Serialize TPMI_ST_ATTEST to json.
 *
 * @param[in] in variable to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 */
TSS2_RC
ifapi_json_TPMI_ST_ATTEST_serialize(const TPMI_ST_ATTEST in, json_object **jso)
{
    CHECK_IN_LIST(TPMI_ALG_HASH, in, TPM2_ST_ATTEST_CERTIFY, TPM2_ST_ATTEST_QUOTE,
                  TPM2_ST_ATTEST_SESSION_AUDIT, TPM2_ST_ATTEST_COMMAND_AUDIT,
                  TPM2_ST_ATTEST_TIME, TPM2_ST_ATTEST_CREATION, TPM2_ST_ATTEST_NV);
    return ifapi_json_TPM2_ST_serialize(in, jso);
}

/**  Serialize a TPMU_ATTEST to json.
 *
 * This function expects the Bitfield to be encoded as unsigned int in host-endianess.
 * @param[in] in the value to be serialized.
 * @param[in] selector the type of the attest.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMU_ATTEST.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMU_ATTEST_serialize(const TPMU_ATTEST *in, UINT32 selector, json_object **jso)
{
    switch (selector) {
        case TPM2_ST_ATTEST_CERTIFY:
            return ifapi_json_TPMS_CERTIFY_INFO_serialize(&in->certify, jso);
        case TPM2_ST_ATTEST_CREATION:
            return ifapi_json_TPMS_CREATION_INFO_serialize(&in->creation, jso);
        case TPM2_ST_ATTEST_QUOTE:
            return ifapi_json_TPMS_QUOTE_INFO_serialize(&in->quote, jso);
        case TPM2_ST_ATTEST_COMMAND_AUDIT:
            return ifapi_json_TPMS_COMMAND_AUDIT_INFO_serialize(&in->commandAudit, jso);
        case TPM2_ST_ATTEST_SESSION_AUDIT:
            return ifapi_json_TPMS_SESSION_AUDIT_INFO_serialize(&in->sessionAudit, jso);
        case TPM2_ST_ATTEST_TIME:
            return ifapi_json_TPMS_TIME_ATTEST_INFO_serialize(&in->time, jso);
        case TPM2_ST_ATTEST_NV:
            return ifapi_json_TPMS_NV_CERTIFY_INFO_serialize(&in->nv, jso);
        default:
            LOG_ERROR("\nSelector %"PRIx32 " did not match", selector);
            return TSS2_FAPI_RC_BAD_VALUE;
    };
    return TSS2_RC_SUCCESS;
}

/** Serialize value of type TPMS_ATTEST to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMS_ATTEST.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_ATTEST_serialize(const TPMS_ATTEST *in, json_object **jso)
{
    return_if_null(in, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    TSS2_RC r;
    json_object *jso2;
    if (*jso == NULL)
        *jso = json_object_new_object ();
    jso2 = NULL;
    r = ifapi_json_TPM2_GENERATED_serialize(in->magic, &jso2);
    return_if_error(r, "Serialize TPM2_GENERATED");

    json_object_object_add(*jso, "magic", jso2);
    jso2 = NULL;
    r = ifapi_json_TPMI_ST_ATTEST_serialize(in->type, &jso2);
    return_if_error(r, "Serialize TPMI_ST_ATTEST");

    json_object_object_add(*jso, "type", jso2);
    jso2 = NULL;
    r = ifapi_json_TPM2B_NAME_serialize(&in->qualifiedSigner, &jso2);
    return_if_error(r, "Serialize TPM2B_NAME");

    json_object_object_add(*jso, "qualifiedSigner", jso2);
    jso2 = NULL;
    r = ifapi_json_TPM2B_DATA_serialize(&in->extraData, &jso2);
    return_if_error(r, "Serialize TPM2B_DATA");

    json_object_object_add(*jso, "extraData", jso2);
    jso2 = NULL;
    r = ifapi_json_TPMS_CLOCK_INFO_serialize(&in->clockInfo, &jso2);
    return_if_error(r, "Serialize TPMS_CLOCK_INFO");

    json_object_object_add(*jso, "clockInfo", jso2);
    jso2 = NULL;
    r = ifapi_json_UINT64_serialize(in->firmwareVersion, &jso2);
    return_if_error(r, "Serialize UINT64");

    json_object_object_add(*jso, "firmwareVersion", jso2);
    jso2 = NULL;
    r = ifapi_json_TPMU_ATTEST_serialize(&in->attested, in->type, &jso2);
    return_if_error(r,"Serialize TPMU_ATTEST");

    json_object_object_add(*jso, "attested", jso2);
    return TSS2_RC_SUCCESS;
}

/** Serialize value of type TPMI_SM4_KEY_BITS to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMI_SM4_KEY_BITS.
 *
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMI_SM4_KEY_BITS_serialize(const TPMI_SM4_KEY_BITS in, json_object **jso)
{
    CHECK_IN_LIST(UINT16, in, 128);
    return ifapi_json_UINT16_serialize(in, jso);
}

/** Serialize value of type TPMI_CAMELLIA_KEY_BITS to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMI_CAMELLIA_KEY_BITS.
 *
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMI_CAMELLIA_KEY_BITS_serialize(const TPMI_CAMELLIA_KEY_BITS in, json_object **jso)
{
    CHECK_IN_LIST(UINT16, in, 128, 192, 256);
    return ifapi_json_UINT16_serialize(in, jso);
}

/** Serialize value of type TPMI_AES_KEY_BITS to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMI_AES_KEY_BITS.
 *
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMI_AES_KEY_BITS_serialize(const TPMI_AES_KEY_BITS in, json_object **jso)
{
    CHECK_IN_LIST(UINT16, in, 128, 192, 256);
    return ifapi_json_UINT16_serialize(in, jso);
}
/**  Serialize a TPMU_SYM_KEY_BITS to json.
 *
 * This function expects the Bitfield to be encoded as unsigned int in host-endianess.
 * @param[in] in the value to be serialized.
 * @param[in] selector the type of the symmetric algorithm.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMU_SYM_KEY_BITS.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMU_SYM_KEY_BITS_serialize(const TPMU_SYM_KEY_BITS *in, UINT32 selector, json_object **jso)
{
    switch (selector) {
        case TPM2_ALG_AES:
            return ifapi_json_TPMI_AES_KEY_BITS_serialize(in->aes, jso);
        case TPM2_ALG_SM4:
            return ifapi_json_TPMI_SM4_KEY_BITS_serialize(in->sm4, jso);
        case TPM2_ALG_CAMELLIA:
            return ifapi_json_TPMI_CAMELLIA_KEY_BITS_serialize(in->camellia, jso);
        case TPM2_ALG_XOR:
            return ifapi_json_TPMI_ALG_HASH_serialize(in->exclusiveOr, jso);
        default:
            LOG_ERROR("\nSelector %"PRIx32 " did not match", selector);
            return TSS2_FAPI_RC_BAD_VALUE;
    };
    return TSS2_RC_SUCCESS;
}

/**  Serialize a TPMU_SYM_MODE to json.
 *
 * This function expects the Bitfield to be encoded as unsigned int in host-endianess.
 * @param[in] in the value to be serialized.
 * @param[in] selector the type of the symmetric mode.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMU_SYM_MODE.
 */
TSS2_RC
ifapi_json_TPMU_SYM_MODE_serialize(const TPMU_SYM_MODE *in, UINT32 selector, json_object **jso)
{
    switch (selector) {
        case TPM2_ALG_CAMELLIA:
        case TPM2_ALG_SM4:
        case TPM2_ALG_AES:
            return ifapi_json_TPMI_ALG_SYM_MODE_serialize(in->aes, jso);
        default:
            LOG_ERROR("\nSelector %"PRIx32 " did not match", selector);
            return TSS2_FAPI_RC_BAD_VALUE;
    };
    return TSS2_RC_SUCCESS;
}

/** Serialize value of type TPMT_SYM_DEF_OBJECT to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMT_SYM_DEF_OBJECT.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMT_SYM_DEF_OBJECT_serialize(const TPMT_SYM_DEF_OBJECT *in, json_object **jso)
{
    return_if_null(in, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    TSS2_RC r;
    json_object *jso2;
    if (*jso == NULL)
        *jso = json_object_new_object ();
    jso2 = NULL;
    r = ifapi_json_TPMI_ALG_SYM_OBJECT_serialize(in->algorithm, &jso2);
    return_if_error(r, "Serialize TPMI_ALG_SYM_OBJECT");

    json_object_object_add(*jso, "algorithm", jso2);
    if (in->algorithm != TPM2_ALG_NULL) {
        json_object *jso2 = NULL;
        r = ifapi_json_TPMU_SYM_KEY_BITS_serialize(&in->keyBits, in->algorithm, &jso2);
        return_if_error(r,"Serialize TPMU_SYM_KEY_BITS");

        json_object_object_add(*jso, "keyBits", jso2);
    }
    if (in->algorithm != TPM2_ALG_NULL) {
        json_object *jso2 = NULL;
        r = ifapi_json_TPMU_SYM_MODE_serialize(&in->mode, in->algorithm, &jso2);
        return_if_error(r,"Serialize TPMU_SYM_MODE");

        json_object_object_add(*jso, "mode", jso2);
    }
    return TSS2_RC_SUCCESS;
}

/** Serialize value of type TPMS_SYMCIPHER_PARMS to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMS_SYMCIPHER_PARMS.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_SYMCIPHER_PARMS_serialize(const TPMS_SYMCIPHER_PARMS *in, json_object **jso)
{
    return_if_null(in, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    TSS2_RC r;
    json_object *jso2;
    if (*jso == NULL)
        *jso = json_object_new_object ();
    jso2 = NULL;
    r = ifapi_json_TPMT_SYM_DEF_OBJECT_serialize(&in->sym, &jso2);
    return_if_error(r, "Serialize TPMT_SYM_DEF_OBJECT");

    json_object_object_add(*jso, "sym", jso2);
    return TSS2_RC_SUCCESS;
}

/** Serialize value of type TPMS_SCHEME_HASH to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMS_SCHEME_HASH.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_SCHEME_HASH_serialize(const TPMS_SCHEME_HASH *in, json_object **jso)
{
    return_if_null(in, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    TSS2_RC r;
    json_object *jso2;
    if (*jso == NULL)
        *jso = json_object_new_object ();
    jso2 = NULL;
    r = ifapi_json_TPMI_ALG_HASH_serialize(in->hashAlg, &jso2);
    return_if_error(r, "Serialize TPMI_ALG_HASH");

    json_object_object_add(*jso, "hashAlg", jso2);
    return TSS2_RC_SUCCESS;
}

/** Serialize value of type TPMS_SCHEME_ECDAA to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMS_SCHEME_ECDAA.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_SCHEME_ECDAA_serialize(const TPMS_SCHEME_ECDAA *in, json_object **jso)
{
    return_if_null(in, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    TSS2_RC r;
    json_object *jso2;
    if (*jso == NULL)
        *jso = json_object_new_object ();
    jso2 = NULL;
    r = ifapi_json_TPMI_ALG_HASH_serialize(in->hashAlg, &jso2);
    return_if_error(r, "Serialize TPMI_ALG_HASH");

    json_object_object_add(*jso, "hashAlg", jso2);
    jso2 = NULL;
    r = ifapi_json_UINT16_serialize(in->count, &jso2);
    return_if_error(r, "Serialize UINT16");

    json_object_object_add(*jso, "count", jso2);
    return TSS2_RC_SUCCESS;
}

/** Serialize TPMI_ALG_KEYEDHASH_SCHEME to json.
 *
 * @param[in] in variable to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 */
TSS2_RC
ifapi_json_TPMI_ALG_KEYEDHASH_SCHEME_serialize(const TPMI_ALG_KEYEDHASH_SCHEME in, json_object **jso)
{
    CHECK_IN_LIST(TPMI_ALG_HASH, in, TPM2_ALG_HMAC, TPM2_ALG_XOR, TPM2_ALG_NULL);
    return ifapi_json_TPM2_ALG_ID_serialize(in, jso);
}

/** Serialize a TPMS_SCHEME_HMAC to json.
 *
 * @param[in] in value of type TPMS_SCHEME_HMAC to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMS_SCHEME_HMAC.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_SCHEME_HMAC_serialize(const TPMS_SCHEME_HMAC *in, json_object **jso)
{
    return ifapi_json_TPMS_SCHEME_HASH_serialize(in, jso);
}

/** Serialize value of type TPMS_SCHEME_XOR to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMS_SCHEME_XOR.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_SCHEME_XOR_serialize(const TPMS_SCHEME_XOR *in, json_object **jso)
{
    return_if_null(in, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    TSS2_RC r;
    json_object *jso2;
    if (*jso == NULL)
        *jso = json_object_new_object ();
    jso2 = NULL;
    r = ifapi_json_TPMI_ALG_HASH_serialize(in->hashAlg, &jso2);
    return_if_error(r, "Serialize TPMI_ALG_HASH");

    json_object_object_add(*jso, "hashAlg", jso2);
    jso2 = NULL;
    r = ifapi_json_TPMI_ALG_KDF_serialize(in->kdf, &jso2);
    return_if_error(r, "Serialize TPMI_ALG_KDF");

    json_object_object_add(*jso, "kdf", jso2);
    return TSS2_RC_SUCCESS;
}

/**  Serialize a TPMU_SCHEME_KEYEDHASH to json.
 *
 * This function expects the Bitfield to be encoded as unsigned int in host-endianess.
 * @param[in] in the value to be serialized.
 * @param[in] selector the type of the keyedhash scheme.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMU_SCHEME_KEYEDHASH.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMU_SCHEME_KEYEDHASH_serialize(const TPMU_SCHEME_KEYEDHASH *in, UINT32 selector, json_object **jso)
{
    switch (selector) {
        case TPM2_ALG_HMAC:
            return ifapi_json_TPMS_SCHEME_HMAC_serialize(&in->hmac, jso);
        case TPM2_ALG_XOR:
            return ifapi_json_TPMS_SCHEME_XOR_serialize(&in->exclusiveOr, jso);
        default:
            LOG_ERROR("\nSelector %"PRIx32 " did not match", selector);
            return TSS2_FAPI_RC_BAD_VALUE;
    };
    return TSS2_RC_SUCCESS;
}

/** Serialize value of type TPMT_KEYEDHASH_SCHEME to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMT_KEYEDHASH_SCHEME.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMT_KEYEDHASH_SCHEME_serialize(const TPMT_KEYEDHASH_SCHEME *in, json_object **jso)
{
    return_if_null(in, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    TSS2_RC r;
    json_object *jso2;
    if (*jso == NULL)
        *jso = json_object_new_object ();
    jso2 = NULL;
    r = ifapi_json_TPMI_ALG_KEYEDHASH_SCHEME_serialize(in->scheme, &jso2);
    return_if_error(r, "Serialize TPMI_ALG_KEYEDHASH_SCHEME");

    json_object_object_add(*jso, "scheme", jso2);
    if (in->scheme != TPM2_ALG_NULL) {
        json_object *jso2 = NULL;
        r = ifapi_json_TPMU_SCHEME_KEYEDHASH_serialize(&in->details, in->scheme, &jso2);
        return_if_error(r,"Serialize TPMU_SCHEME_KEYEDHASH");

        json_object_object_add(*jso, "details", jso2);
    }
    return TSS2_RC_SUCCESS;
}

/** Serialize a TPMS_SIG_SCHEME_RSASSA to json.
 *
 * @param[in] in value of type TPMS_SIG_SCHEME_RSASSA to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMS_SIG_SCHEME_RSASSA.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_SIG_SCHEME_RSASSA_serialize(const TPMS_SIG_SCHEME_RSASSA *in, json_object **jso)
{
    return ifapi_json_TPMS_SCHEME_HASH_serialize(in, jso);
}

/** Serialize a TPMS_SIG_SCHEME_RSAPSS to json.
 *
 * @param[in] in value of type TPMS_SIG_SCHEME_RSAPSS to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMS_SIG_SCHEME_RSAPSS.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_SIG_SCHEME_RSAPSS_serialize(const TPMS_SIG_SCHEME_RSAPSS *in, json_object **jso)
{
    return ifapi_json_TPMS_SCHEME_HASH_serialize(in, jso);
}

/** Serialize a TPMS_SIG_SCHEME_ECDSA to json.
 *
 * @param[in] in value of type TPMS_SIG_SCHEME_ECDSA to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMS_SIG_SCHEME_ECDSA.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_SIG_SCHEME_ECDSA_serialize(const TPMS_SIG_SCHEME_ECDSA *in, json_object **jso)
{
    return ifapi_json_TPMS_SCHEME_HASH_serialize(in, jso);
}

/** Serialize a TPMS_SIG_SCHEME_SM2 to json.
 *
 * @param[in] in value of type TPMS_SIG_SCHEME_SM2 to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMS_SIG_SCHEME_SM2.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_SIG_SCHEME_SM2_serialize(const TPMS_SIG_SCHEME_SM2 *in, json_object **jso)
{
    return ifapi_json_TPMS_SCHEME_HASH_serialize(in, jso);
}

/** Serialize a TPMS_SIG_SCHEME_ECSCHNORR to json.
 *
 * @param[in] in value of type TPMS_SIG_SCHEME_ECSCHNORR to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMS_SIG_SCHEME_ECSCHNORR.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_SIG_SCHEME_ECSCHNORR_serialize(const TPMS_SIG_SCHEME_ECSCHNORR *in, json_object **jso)
{
    return ifapi_json_TPMS_SCHEME_HASH_serialize(in, jso);
}

/** Serialize a TPMS_SIG_SCHEME_ECDAA to json.
 *
 * @param[in] in value of type TPMS_SIG_SCHEME_ECDAA to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMS_SIG_SCHEME_ECDAA.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_SIG_SCHEME_ECDAA_serialize(const TPMS_SIG_SCHEME_ECDAA *in, json_object **jso)
{
    return ifapi_json_TPMS_SCHEME_ECDAA_serialize(in, jso);
}

/**  Serialize a TPMU_SIG_SCHEME to json.
 *
 * This function expects the Bitfield to be encoded as unsigned int in host-endianess.
 * @param[in] in the value to be serialized.
 * @param[in] selector the type of the signature scheme.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMU_SIG_SCHEME.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMU_SIG_SCHEME_serialize(const TPMU_SIG_SCHEME *in, UINT32 selector, json_object **jso)
{
    switch (selector) {
        case TPM2_ALG_RSASSA:
            return ifapi_json_TPMS_SIG_SCHEME_RSASSA_serialize(&in->rsassa, jso);
        case TPM2_ALG_RSAPSS:
            return ifapi_json_TPMS_SIG_SCHEME_RSAPSS_serialize(&in->rsapss, jso);
        case TPM2_ALG_ECDSA:
            return ifapi_json_TPMS_SIG_SCHEME_ECDSA_serialize(&in->ecdsa, jso);
        case TPM2_ALG_ECDAA:
            return ifapi_json_TPMS_SIG_SCHEME_ECDAA_serialize(&in->ecdaa, jso);
        case TPM2_ALG_SM2:
            return ifapi_json_TPMS_SIG_SCHEME_SM2_serialize(&in->sm2, jso);
        case TPM2_ALG_ECSCHNORR:
            return ifapi_json_TPMS_SIG_SCHEME_ECSCHNORR_serialize(&in->ecschnorr, jso);
        case TPM2_ALG_HMAC:
            return ifapi_json_TPMS_SCHEME_HMAC_serialize(&in->hmac, jso);
        default:
            LOG_ERROR("\nSelector %"PRIx32 " did not match", selector);
            return TSS2_FAPI_RC_BAD_VALUE;
    };
    return TSS2_RC_SUCCESS;
}

/** Serialize value of type TPMT_SIG_SCHEME to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMT_SIG_SCHEME.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMT_SIG_SCHEME_serialize(const TPMT_SIG_SCHEME *in, json_object **jso)
{
    return_if_null(in, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    TSS2_RC r;
    json_object *jso2;
    if (*jso == NULL)
        *jso = json_object_new_object ();
    jso2 = NULL;
    r = ifapi_json_TPMI_ALG_SIG_SCHEME_serialize(in->scheme, &jso2);
    return_if_error(r, "Serialize TPMI_ALG_SIG_SCHEME");

    json_object_object_add(*jso, "scheme", jso2);
    if (in->scheme != TPM2_ALG_NULL) {
        json_object *jso2 = NULL;
        r = ifapi_json_TPMU_SIG_SCHEME_serialize(&in->details, in->scheme, &jso2);
        return_if_error(r,"Serialize TPMU_SIG_SCHEME");

        json_object_object_add(*jso, "details", jso2);
    }
    return TSS2_RC_SUCCESS;
}

/** Serialize a TPMS_ENC_SCHEME_OAEP to json.
 *
 * @param[in] in value of type TPMS_ENC_SCHEME_OAEP to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMS_ENC_SCHEME_OAEP.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_ENC_SCHEME_OAEP_serialize(const TPMS_ENC_SCHEME_OAEP *in, json_object **jso)
{
    return ifapi_json_TPMS_SCHEME_HASH_serialize(in, jso);
}

/** Serialize a TPMS_ENC_SCHEME_RSAES to json.
 *
 * @param[in] in value of type TPMS_ENC_SCHEME_RSAES to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMS_ENC_SCHEME_RSAES.
 */
TSS2_RC
ifapi_json_TPMS_ENC_SCHEME_RSAES_serialize(const TPMS_ENC_SCHEME_RSAES *in, json_object **jso)
{
    return ifapi_json_TPMS_EMPTY_serialize(in, jso);
}

/** Serialize a TPMS_KEY_SCHEME_ECDH to json.
 *
 * @param[in] in value of type TPMS_KEY_SCHEME_ECDH to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMS_KEY_SCHEME_ECDH.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_KEY_SCHEME_ECDH_serialize(const TPMS_KEY_SCHEME_ECDH *in, json_object **jso)
{
    return ifapi_json_TPMS_SCHEME_HASH_serialize(in, jso);
}

/** Serialize a TPMS_SCHEME_MGF1 to json.
 *
 * @param[in] in value of type TPMS_SCHEME_MGF1 to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMS_SCHEME_MGF1.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_SCHEME_MGF1_serialize(const TPMS_SCHEME_MGF1 *in, json_object **jso)
{
    return ifapi_json_TPMS_SCHEME_HASH_serialize(in, jso);
}

/** Serialize a TPMS_SCHEME_KDF1_SP800_56A to json.
 *
 * @param[in] in value of type TPMS_SCHEME_KDF1_SP800_56A to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMS_SCHEME_KDF1_SP800_56A.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_SCHEME_KDF1_SP800_56A_serialize(const TPMS_SCHEME_KDF1_SP800_56A *in, json_object **jso)
{
    return ifapi_json_TPMS_SCHEME_HASH_serialize(in, jso);
}

/** Serialize a TPMS_SCHEME_KDF1_SP800_108 to json.
 *
 * @param[in] in value of type TPMS_SCHEME_KDF1_SP800_108 to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMS_SCHEME_KDF1_SP800_108.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_SCHEME_KDF1_SP800_108_serialize(const TPMS_SCHEME_KDF1_SP800_108 *in, json_object **jso)
{
    return ifapi_json_TPMS_SCHEME_HASH_serialize(in, jso);
}

/**  Serialize a TPMU_KDF_SCHEME to json.
 *
 * This function expects the Bitfield to be encoded as unsigned int in host-endianess.
 * @param[in] in the value to be serialized.
 * @param[in] selector the type of the KDF scheme.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMU_KDF_SCHEME.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMU_KDF_SCHEME_serialize(const TPMU_KDF_SCHEME *in, UINT32 selector, json_object **jso)
{
    switch (selector) {
        case TPM2_ALG_MGF1:
            return ifapi_json_TPMS_SCHEME_MGF1_serialize(&in->mgf1, jso);
        case TPM2_ALG_KDF1_SP800_56A:
            return ifapi_json_TPMS_SCHEME_KDF1_SP800_56A_serialize(&in->kdf1_sp800_56a, jso);
        case TPM2_ALG_KDF1_SP800_108:
            return ifapi_json_TPMS_SCHEME_KDF1_SP800_108_serialize(&in->kdf1_sp800_108, jso);
        default:
            LOG_ERROR("\nSelector %"PRIx32 " did not match", selector);
            return TSS2_FAPI_RC_BAD_VALUE;
    };
    return TSS2_RC_SUCCESS;
}

/** Serialize value of type TPMT_KDF_SCHEME to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMT_KDF_SCHEME.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMT_KDF_SCHEME_serialize(const TPMT_KDF_SCHEME *in, json_object **jso)
{
    return_if_null(in, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    TSS2_RC r;
    json_object *jso2;
    if (*jso == NULL)
        *jso = json_object_new_object ();
    jso2 = NULL;
    r = ifapi_json_TPMI_ALG_KDF_serialize(in->scheme, &jso2);
    return_if_error(r, "Serialize TPMI_ALG_KDF");

    json_object_object_add(*jso, "scheme", jso2);
    if (in->scheme != TPM2_ALG_NULL) {
        json_object *jso2 = NULL;
        r = ifapi_json_TPMU_KDF_SCHEME_serialize(&in->details, in->scheme, &jso2);
        return_if_error(r,"Serialize TPMU_KDF_SCHEME");

        json_object_object_add(*jso, "details", jso2);
    }
    return TSS2_RC_SUCCESS;
}

/** Serialize TPMI_ALG_ASYM_SCHEME to json.
 *
 * @param[in] in variable to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 */
TSS2_RC
ifapi_json_TPMI_ALG_ASYM_SCHEME_serialize(const TPMI_ALG_ASYM_SCHEME in, json_object **jso)
{
    CHECK_IN_LIST(TPMI_ALG_ASYM_SCHEME, in, TPM2_ALG_ECDH, TPM2_ALG_RSASSA, TPM2_ALG_RSAPSS,
                  TPM2_ALG_ECDSA, TPM2_ALG_ECDAA, TPM2_ALG_SM2, TPM2_ALG_ECSCHNORR,
                  TPM2_ALG_RSAES, TPM2_ALG_OAEP, TPM2_ALG_NULL);
    return ifapi_json_TPM2_ALG_ID_serialize(in, jso);
}

/**  Serialize a TPMU_ASYM_SCHEME to json.
 *
 * This function expects the Bitfield to be encoded as unsigned int in host-endianess.
 * @param[in] in the value to be serialized.
 * @param[in] selector the type of the scheme.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMU_ASYM_SCHEME.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMU_ASYM_SCHEME_serialize(const TPMU_ASYM_SCHEME *in, UINT32 selector, json_object **jso)
{
    switch (selector) {
        case TPM2_ALG_ECDH:
            return ifapi_json_TPMS_KEY_SCHEME_ECDH_serialize(&in->ecdh, jso);
        case TPM2_ALG_RSASSA:
            return ifapi_json_TPMS_SIG_SCHEME_RSASSA_serialize(&in->rsassa, jso);
        case TPM2_ALG_RSAPSS:
            return ifapi_json_TPMS_SIG_SCHEME_RSAPSS_serialize(&in->rsapss, jso);
        case TPM2_ALG_ECDSA:
            return ifapi_json_TPMS_SIG_SCHEME_ECDSA_serialize(&in->ecdsa, jso);
        case TPM2_ALG_ECDAA:
            return ifapi_json_TPMS_SIG_SCHEME_ECDAA_serialize(&in->ecdaa, jso);
        case TPM2_ALG_SM2:
            return ifapi_json_TPMS_SIG_SCHEME_SM2_serialize(&in->sm2, jso);
        case TPM2_ALG_ECSCHNORR:
            return ifapi_json_TPMS_SIG_SCHEME_ECSCHNORR_serialize(&in->ecschnorr, jso);
        case TPM2_ALG_RSAES:
            return ifapi_json_TPMS_ENC_SCHEME_RSAES_serialize(&in->rsaes, jso);
        case TPM2_ALG_OAEP:
            return ifapi_json_TPMS_ENC_SCHEME_OAEP_serialize(&in->oaep, jso);
        default:
            LOG_ERROR("\nSelector %"PRIx32 " did not match", selector);
            return TSS2_FAPI_RC_BAD_VALUE;
    };
    return TSS2_RC_SUCCESS;
}

/** Serialize TPMI_ALG_RSA_SCHEME to json.
 *
 * @param[in] in variable to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 */
TSS2_RC
ifapi_json_TPMI_ALG_RSA_SCHEME_serialize(const TPMI_ALG_RSA_SCHEME in, json_object **jso)
{
    CHECK_IN_LIST(TPMI_ALG_RSA_SCHEME, in, TPM2_ALG_RSAES, TPM2_ALG_OAEP, TPM2_ALG_RSASSA,
                  TPM2_ALG_RSAPSS, TPM2_ALG_NULL);
    return ifapi_json_TPM2_ALG_ID_serialize(in, jso);
}

/** Serialize value of type TPMT_RSA_SCHEME to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMT_RSA_SCHEME.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMT_RSA_SCHEME_serialize(const TPMT_RSA_SCHEME *in, json_object **jso)
{
    return_if_null(in, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    TSS2_RC r;
    json_object *jso2;
    if (*jso == NULL)
        *jso = json_object_new_object ();
    jso2 = NULL;
    r = ifapi_json_TPMI_ALG_RSA_SCHEME_serialize(in->scheme, &jso2);
    return_if_error(r, "Serialize TPMI_ALG_RSA_SCHEME");

    json_object_object_add(*jso, "scheme", jso2);
    if (in->scheme != TPM2_ALG_NULL) {
        json_object *jso2 = NULL;
        r = ifapi_json_TPMU_ASYM_SCHEME_serialize(&in->details, in->scheme, &jso2);
        return_if_error(r,"Serialize TPMU_ASYM_SCHEME");

        json_object_object_add(*jso, "details", jso2);
    }
    return TSS2_RC_SUCCESS;
}

/** Serialize value of type TPM2B_PUBLIC_KEY_RSA to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPM2B_PUBLIC_KEY_RSA.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPM2B_PUBLIC_KEY_RSA_serialize(const TPM2B_PUBLIC_KEY_RSA *in, json_object **jso)
{
    return_if_null(in, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    if (in->size > TPM2_MAX_RSA_KEY_BYTES) {
        LOG_ERROR("Too many bytes for array (%"PRIuPTR" > %"PRIuPTR" = TPM2_MAX_RSA_KEY_BYTES)",
                  (size_t)in->size, (size_t)TPM2_MAX_RSA_KEY_BYTES);
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    char hex_string[((size_t)in->size)*2+1];

    for (size_t i = 0, off = 0; i < in->size; i++, off+=2)
        sprintf(&hex_string[off], "%02x", in->buffer[i]);
    hex_string[(in->size)*2] = '\0';
    *jso = json_object_new_string (hex_string);
    return_if_null(*jso, "Out of memory.", TSS2_FAPI_RC_MEMORY);

    return TSS2_RC_SUCCESS;
}

/** Serialize value of type TPMI_RSA_KEY_BITS to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMI_RSA_KEY_BITS.
 *
 */
TSS2_RC
ifapi_json_TPMI_RSA_KEY_BITS_serialize(const TPMI_RSA_KEY_BITS in, json_object **jso)
{
    CHECK_IN_LIST(TPMI_RSA_KEY_BITS, in, 1024, 2048);
    return ifapi_json_UINT16_serialize(in, jso);
}

/** Serialize value of type TPM2B_ECC_PARAMETER to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPM2B_ECC_PARAMETER.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPM2B_ECC_PARAMETER_serialize(const TPM2B_ECC_PARAMETER *in, json_object **jso)
{
    return_if_null(in, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    if (in->size > TPM2_MAX_ECC_KEY_BYTES) {
        LOG_ERROR("Too many bytes for array (%"PRIuPTR" > %"PRIuPTR" = TPM2_MAX_ECC_KEY_BYTES)",
                  (size_t)in->size, (size_t)TPM2_MAX_ECC_KEY_BYTES);
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    char hex_string[((size_t)in->size)*2+1];

    for (size_t i = 0, off = 0; i < in->size; i++, off+=2)
        sprintf(&hex_string[off], "%02x", in->buffer[i]);
    hex_string[(in->size)*2] = '\0';
    *jso = json_object_new_string (hex_string);
    return_if_null(*jso, "Out of memory.", TSS2_FAPI_RC_MEMORY);

    return TSS2_RC_SUCCESS;
}

/** Serialize value of type TPMS_ECC_POINT to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMS_ECC_POINT.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_ECC_POINT_serialize(const TPMS_ECC_POINT *in, json_object **jso)
{
    return_if_null(in, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    TSS2_RC r;
    json_object *jso2;
    if (*jso == NULL)
        *jso = json_object_new_object ();
    jso2 = NULL;
    r = ifapi_json_TPM2B_ECC_PARAMETER_serialize(&in->x, &jso2);
    return_if_error(r, "Serialize TPM2B_ECC_PARAMETER");

    json_object_object_add(*jso, "x", jso2);
    jso2 = NULL;
    r = ifapi_json_TPM2B_ECC_PARAMETER_serialize(&in->y, &jso2);
    return_if_error(r, "Serialize TPM2B_ECC_PARAMETER");

    json_object_object_add(*jso, "y", jso2);
    return TSS2_RC_SUCCESS;
}

/** Serialize TPMI_ALG_ECC_SCHEME to json.
 *
 * @param[in] in variable to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 */
TSS2_RC
ifapi_json_TPMI_ALG_ECC_SCHEME_serialize(const TPMI_ALG_ECC_SCHEME in, json_object **jso)
{
    CHECK_IN_LIST(TPMI_ALG_ECC_SCHEME, in, TPM2_ALG_ECDSA, TPM2_ALG_ECDAA,
                  TPM2_ALG_SM2, TPM2_ALG_ECSCHNORR, TPM2_ALG_ECDH, TPM2_ALG_NULL);
    return ifapi_json_TPM2_ALG_ID_serialize(in, jso);
}

/** Serialize value of type TPMI_ECC_CURVE to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMI_ECC_CURVE.
 *
 */
TSS2_RC
ifapi_json_TPMI_ECC_CURVE_serialize(const TPMI_ECC_CURVE in, json_object **jso)
{
    return ifapi_json_TPM2_ECC_CURVE_serialize(in, jso);
}

/** Serialize value of type TPMT_ECC_SCHEME to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMT_ECC_SCHEME.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMT_ECC_SCHEME_serialize(const TPMT_ECC_SCHEME *in, json_object **jso)
{
    return_if_null(in, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    TSS2_RC r;
    json_object *jso2;
    if (*jso == NULL)
        *jso = json_object_new_object ();
    jso2 = NULL;
    r = ifapi_json_TPMI_ALG_ECC_SCHEME_serialize(in->scheme, &jso2);
    return_if_error(r, "Serialize TPMI_ALG_ECC_SCHEME");

    json_object_object_add(*jso, "scheme", jso2);
    if (in->scheme != TPM2_ALG_NULL) {
        json_object *jso2 = NULL;
        r = ifapi_json_TPMU_ASYM_SCHEME_serialize(&in->details, in->scheme, &jso2);
        return_if_error(r,"Serialize TPMU_ASYM_SCHEME");

        json_object_object_add(*jso, "details", jso2);
    }
    return TSS2_RC_SUCCESS;
}

/** Serialize value of type TPMS_SIGNATURE_RSA to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMS_SIGNATURE_RSA.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_SIGNATURE_RSA_serialize(const TPMS_SIGNATURE_RSA *in, json_object **jso)
{
    return_if_null(in, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    TSS2_RC r;
    json_object *jso2;
    if (*jso == NULL)
        *jso = json_object_new_object ();
    jso2 = NULL;
    r = ifapi_json_TPMI_ALG_HASH_serialize(in->hash, &jso2);
    return_if_error(r, "Serialize TPMI_ALG_HASH");

    json_object_object_add(*jso, "hash", jso2);
    jso2 = NULL;
    r = ifapi_json_TPM2B_PUBLIC_KEY_RSA_serialize(&in->sig, &jso2);
    return_if_error(r, "Serialize TPM2B_PUBLIC_KEY_RSA");

    json_object_object_add(*jso, "sig", jso2);
    return TSS2_RC_SUCCESS;
}

/** Serialize a TPMS_SIGNATURE_RSASSA to json.
 *
 * @param[in] in value of type TPMS_SIGNATURE_RSASSA to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMS_SIGNATURE_RSASSA.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_SIGNATURE_RSASSA_serialize(const TPMS_SIGNATURE_RSASSA *in, json_object **jso)
{
    return ifapi_json_TPMS_SIGNATURE_RSA_serialize(in, jso);
}

/** Serialize a TPMS_SIGNATURE_RSAPSS to json.
 *
 * @param[in] in value of type TPMS_SIGNATURE_RSAPSS to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMS_SIGNATURE_RSAPSS.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_SIGNATURE_RSAPSS_serialize(const TPMS_SIGNATURE_RSAPSS *in, json_object **jso)
{
    return ifapi_json_TPMS_SIGNATURE_RSA_serialize(in, jso);
}

/** Serialize value of type TPMS_SIGNATURE_ECC to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMS_SIGNATURE_ECC.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_SIGNATURE_ECC_serialize(const TPMS_SIGNATURE_ECC *in, json_object **jso)
{
    return_if_null(in, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    TSS2_RC r;
    json_object *jso2;
    if (*jso == NULL)
        *jso = json_object_new_object ();
    jso2 = NULL;
    r = ifapi_json_TPMI_ALG_HASH_serialize(in->hash, &jso2);
    return_if_error(r, "Serialize TPMI_ALG_HASH");

    json_object_object_add(*jso, "hash", jso2);
    jso2 = NULL;
    r = ifapi_json_TPM2B_ECC_PARAMETER_serialize(&in->signatureR, &jso2);
    return_if_error(r, "Serialize TPM2B_ECC_PARAMETER");

    json_object_object_add(*jso, "signatureR", jso2);
    jso2 = NULL;
    r = ifapi_json_TPM2B_ECC_PARAMETER_serialize(&in->signatureS, &jso2);
    return_if_error(r, "Serialize TPM2B_ECC_PARAMETER");

    json_object_object_add(*jso, "signatureS", jso2);
    return TSS2_RC_SUCCESS;
}

/** Serialize a TPMS_SIGNATURE_ECDSA to json.
 *
 * @param[in] in value of type TPMS_SIGNATURE_ECDSA to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMS_SIGNATURE_ECDSA.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_SIGNATURE_ECDSA_serialize(const TPMS_SIGNATURE_ECDSA *in, json_object **jso)
{
    return ifapi_json_TPMS_SIGNATURE_ECC_serialize(in, jso);
}

/** Serialize a TPMS_SIGNATURE_ECDAA to json.
 *
 * @param[in] in value of type TPMS_SIGNATURE_ECDAA to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMS_SIGNATURE_ECDAA.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_SIGNATURE_ECDAA_serialize(const TPMS_SIGNATURE_ECDAA *in, json_object **jso)
{
    return ifapi_json_TPMS_SIGNATURE_ECC_serialize(in, jso);
}

/** Serialize a TPMS_SIGNATURE_SM2 to json.
 *
 * @param[in] in value of type TPMS_SIGNATURE_SM2 to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMS_SIGNATURE_SM2.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_SIGNATURE_SM2_serialize(const TPMS_SIGNATURE_SM2 *in, json_object **jso)
{
    return ifapi_json_TPMS_SIGNATURE_ECC_serialize(in, jso);
}

/** Serialize a TPMS_SIGNATURE_ECSCHNORR to json.
 *
 * @param[in] in value of type TPMS_SIGNATURE_ECSCHNORR to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMS_SIGNATURE_ECSCHNORR.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_SIGNATURE_ECSCHNORR_serialize(const TPMS_SIGNATURE_ECSCHNORR *in, json_object **jso)
{
    return ifapi_json_TPMS_SIGNATURE_ECC_serialize(in, jso);
}

/**  Serialize a TPMU_SIGNATURE to json.
 *
 * This function expects the Bitfield to be encoded as unsigned int in host-endianess.
 * @param[in] in the value to be serialized.
 * @param[in] selector the type of the signature.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMU_SIGNATURE.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMU_SIGNATURE_serialize(const TPMU_SIGNATURE *in, UINT32 selector, json_object **jso)
{
    switch (selector) {
        case TPM2_ALG_RSASSA:
            return ifapi_json_TPMS_SIGNATURE_RSASSA_serialize(&in->rsassa, jso);
        case TPM2_ALG_RSAPSS:
            return ifapi_json_TPMS_SIGNATURE_RSAPSS_serialize(&in->rsapss, jso);
        case TPM2_ALG_ECDSA:
            return ifapi_json_TPMS_SIGNATURE_ECDSA_serialize(&in->ecdsa, jso);
        case TPM2_ALG_ECDAA:
            return ifapi_json_TPMS_SIGNATURE_ECDAA_serialize(&in->ecdaa, jso);
        case TPM2_ALG_SM2:
            return ifapi_json_TPMS_SIGNATURE_SM2_serialize(&in->sm2, jso);
        case TPM2_ALG_ECSCHNORR:
            return ifapi_json_TPMS_SIGNATURE_ECSCHNORR_serialize(&in->ecschnorr, jso);
        case TPM2_ALG_HMAC:
            return ifapi_json_TPMT_HA_serialize(&in->hmac, jso);
        default:
            LOG_ERROR("\nSelector %"PRIx32 " did not match", selector);
            return TSS2_FAPI_RC_BAD_VALUE;
    };
    return TSS2_RC_SUCCESS;
}

/** Serialize value of type TPMT_SIGNATURE to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMT_SIGNATURE.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMT_SIGNATURE_serialize(const TPMT_SIGNATURE *in, json_object **jso)
{
    return_if_null(in, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    TSS2_RC r;
    json_object *jso2;
    if (*jso == NULL)
        *jso = json_object_new_object ();
    jso2 = NULL;
    r = ifapi_json_TPMI_ALG_SIG_SCHEME_serialize(in->sigAlg, &jso2);
    return_if_error(r, "Serialize TPMI_ALG_SIG_SCHEME");

    json_object_object_add(*jso, "sigAlg", jso2);
    if (in->sigAlg != TPM2_ALG_NULL) {
        json_object *jso2 = NULL;
        r = ifapi_json_TPMU_SIGNATURE_serialize(&in->signature, in->sigAlg, &jso2);
        return_if_error(r,"Serialize TPMU_SIGNATURE");

        json_object_object_add(*jso, "signature", jso2);
    }
    return TSS2_RC_SUCCESS;
}

/** Serialize value of type TPM2B_ENCRYPTED_SECRET to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPM2B_ENCRYPTED_SECRET.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPM2B_ENCRYPTED_SECRET_serialize(const TPM2B_ENCRYPTED_SECRET *in, json_object **jso)
{
    return_if_null(in, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    if (in->size > sizeof(TPMU_ENCRYPTED_SECRET)) {
        LOG_ERROR("Too many bytes for array (%"PRIuPTR" > %"PRIuPTR" = sizeof(TPMU_ENCRYPTED_SECRET))",
                  (size_t)in->size, (size_t)sizeof(TPMU_ENCRYPTED_SECRET));
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    char hex_string[((size_t)in->size)*2+1];

    for (size_t i = 0, off = 0; i < in->size; i++, off+=2)
        sprintf(&hex_string[off], "%02x", in->secret[i]);
    hex_string[(in->size)*2] = '\0';
    *jso = json_object_new_string (hex_string);
    return_if_null(*jso, "Out of memory.", TSS2_FAPI_RC_MEMORY);

    return TSS2_RC_SUCCESS;
}

/** Serialize TPMI_ALG_PUBLIC to json.
 *
 * @param[in] in variable to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 */
TSS2_RC
ifapi_json_TPMI_ALG_PUBLIC_serialize(const TPMI_ALG_PUBLIC in, json_object **jso)
{
    CHECK_IN_LIST(TPMI_ALG_PUBLIC, in, TPM2_ALG_RSA, TPM2_ALG_KEYEDHASH,
                  TPM2_ALG_ECC, TPM2_ALG_SYMCIPHER, TPM2_ALG_NULL);
    return ifapi_json_TPM2_ALG_ID_serialize(in, jso);
}

/**  Serialize a TPMU_PUBLIC_ID to json.
 *
 * This function expects the Bitfield to be encoded as unsigned int in host-endianess.
 * @param[in] in the value to be serialized.
 * @param[in] selector the type of the public ID.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMU_PUBLIC_ID.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMU_PUBLIC_ID_serialize(const TPMU_PUBLIC_ID *in, UINT32 selector, json_object **jso)
{
    switch (selector) {
        case TPM2_ALG_KEYEDHASH:
            return ifapi_json_TPM2B_DIGEST_serialize(&in->keyedHash, jso);
        case TPM2_ALG_SYMCIPHER:
            return ifapi_json_TPM2B_DIGEST_serialize(&in->sym, jso);
        case TPM2_ALG_RSA:
            return ifapi_json_TPM2B_PUBLIC_KEY_RSA_serialize(&in->rsa, jso);
        case TPM2_ALG_ECC:
            return ifapi_json_TPMS_ECC_POINT_serialize(&in->ecc, jso);
        default:
            LOG_ERROR("\nSelector %"PRIx32 " did not match", selector);
            return TSS2_FAPI_RC_BAD_VALUE;
    };
    return TSS2_RC_SUCCESS;
}

/** Serialize value of type TPMS_KEYEDHASH_PARMS to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMS_KEYEDHASH_PARMS.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_KEYEDHASH_PARMS_serialize(const TPMS_KEYEDHASH_PARMS *in, json_object **jso)
{
    return_if_null(in, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    TSS2_RC r;
    json_object *jso2;
    if (*jso == NULL)
        *jso = json_object_new_object ();
    jso2 = NULL;
    r = ifapi_json_TPMT_KEYEDHASH_SCHEME_serialize(&in->scheme, &jso2);
    return_if_error(r, "Serialize TPMT_KEYEDHASH_SCHEME");

    json_object_object_add(*jso, "scheme", jso2);
    return TSS2_RC_SUCCESS;
}

/** Serialize value of type TPMS_RSA_PARMS to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMS_RSA_PARMS.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_RSA_PARMS_serialize(const TPMS_RSA_PARMS *in, json_object **jso)
{
    return_if_null(in, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    TSS2_RC r;
    json_object *jso2;
    if (*jso == NULL)
        *jso = json_object_new_object ();
    jso2 = NULL;
    r = ifapi_json_TPMT_SYM_DEF_OBJECT_serialize(&in->symmetric, &jso2);
    return_if_error(r, "Serialize TPMT_SYM_DEF_OBJECT");

    json_object_object_add(*jso, "symmetric", jso2);
    jso2 = NULL;
    r = ifapi_json_TPMT_RSA_SCHEME_serialize(&in->scheme, &jso2);
    return_if_error(r, "Serialize TPMT_RSA_SCHEME");

    json_object_object_add(*jso, "scheme", jso2);
    jso2 = NULL;
    r = ifapi_json_TPMI_RSA_KEY_BITS_serialize(in->keyBits, &jso2);
    return_if_error(r, "Serialize TPMI_RSA_KEY_BITS");

    json_object_object_add(*jso, "keyBits", jso2);
    jso2 = NULL;
    r = ifapi_json_UINT32_serialize(in->exponent, &jso2);
    return_if_error(r, "Serialize UINT32");

    json_object_object_add(*jso, "exponent", jso2);
    return TSS2_RC_SUCCESS;
}

/** Serialize value of type TPMS_ECC_PARMS to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMS_ECC_PARMS.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_ECC_PARMS_serialize(const TPMS_ECC_PARMS *in, json_object **jso)
{
    return_if_null(in, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    TSS2_RC r;
    json_object *jso2;
    if (*jso == NULL)
        *jso = json_object_new_object ();
    jso2 = NULL;
    r = ifapi_json_TPMT_SYM_DEF_OBJECT_serialize(&in->symmetric, &jso2);
    return_if_error(r, "Serialize TPMT_SYM_DEF_OBJECT");

    json_object_object_add(*jso, "symmetric", jso2);
    jso2 = NULL;
    r = ifapi_json_TPMT_ECC_SCHEME_serialize(&in->scheme, &jso2);
    return_if_error(r, "Serialize TPMT_ECC_SCHEME");

    json_object_object_add(*jso, "scheme", jso2);
    jso2 = NULL;
    r = ifapi_json_TPMI_ECC_CURVE_serialize(in->curveID, &jso2);
    return_if_error(r, "Serialize TPMI_ECC_CURVE");

    json_object_object_add(*jso, "curveID", jso2);
    jso2 = NULL;
    r = ifapi_json_TPMT_KDF_SCHEME_serialize(&in->kdf, &jso2);
    return_if_error(r, "Serialize TPMT_KDF_SCHEME");

    json_object_object_add(*jso, "kdf", jso2);
    return TSS2_RC_SUCCESS;
}

/**  Serialize a TPMU_PUBLIC_PARMS to json.
 *
 * This function expects the Bitfield to be encoded as unsigned int in host-endianess.
 * @param[in] in the value to be serialized.
 * @param[in] selector the type of the public parameters.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMU_PUBLIC_PARMS.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMU_PUBLIC_PARMS_serialize(const TPMU_PUBLIC_PARMS *in, UINT32 selector, json_object **jso)
{
    switch (selector) {
        case TPM2_ALG_KEYEDHASH:
            return ifapi_json_TPMS_KEYEDHASH_PARMS_serialize(&in->keyedHashDetail, jso);
        case TPM2_ALG_SYMCIPHER:
            return ifapi_json_TPMS_SYMCIPHER_PARMS_serialize(&in->symDetail, jso);
        case TPM2_ALG_RSA:
            return ifapi_json_TPMS_RSA_PARMS_serialize(&in->rsaDetail, jso);
        case TPM2_ALG_ECC:
            return ifapi_json_TPMS_ECC_PARMS_serialize(&in->eccDetail, jso);
        default:
            LOG_ERROR("\nSelector %"PRIx32 " did not match", selector);
            return TSS2_FAPI_RC_BAD_VALUE;
    };
    return TSS2_RC_SUCCESS;
}

/** Serialize value of type TPMT_PUBLIC to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMT_PUBLIC.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMT_PUBLIC_serialize(const TPMT_PUBLIC *in, json_object **jso)
{
    return_if_null(in, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    TSS2_RC r;
    json_object *jso2;
    if (*jso == NULL)
        *jso = json_object_new_object ();
    jso2 = NULL;
    r = ifapi_json_TPMI_ALG_PUBLIC_serialize(in->type, &jso2);
    return_if_error(r, "Serialize TPMI_ALG_PUBLIC");

    json_object_object_add(*jso, "type", jso2);
    jso2 = NULL;
    r = ifapi_json_TPMI_ALG_HASH_serialize(in->nameAlg, &jso2);
    return_if_error(r, "Serialize TPMI_ALG_HASH");

    json_object_object_add(*jso, "nameAlg", jso2);
    jso2 = NULL;
    r = ifapi_json_TPMA_OBJECT_serialize(in->objectAttributes, &jso2);
    return_if_error(r, "Serialize TPMA_OBJECT");

    json_object_object_add(*jso, "objectAttributes", jso2);
    jso2 = NULL;
    r = ifapi_json_TPM2B_DIGEST_serialize(&in->authPolicy, &jso2);
    return_if_error(r, "Serialize TPM2B_DIGEST");

    json_object_object_add(*jso, "authPolicy", jso2);
    jso2 = NULL;
    r = ifapi_json_TPMU_PUBLIC_PARMS_serialize(&in->parameters, in->type, &jso2);
    return_if_error(r,"Serialize TPMU_PUBLIC_PARMS");

    json_object_object_add(*jso, "parameters", jso2);
    jso2 = NULL;
    r = ifapi_json_TPMU_PUBLIC_ID_serialize(&in->unique, in->type, &jso2);
    return_if_error(r,"Serialize TPMU_PUBLIC_ID");

    json_object_object_add(*jso, "unique", jso2);
    return TSS2_RC_SUCCESS;
}

/** Serialize a TPM2B_PUBLIC to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPM2B_PUBLIC.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPM2B_PUBLIC_serialize(const TPM2B_PUBLIC *in, json_object **jso)
{
    if (*jso == NULL)
        *jso = json_object_new_object ();
    return_if_null(*jso, "Out of memory.", TSS2_FAPI_RC_MEMORY);

    json_object *jso2;

    jso2 = NULL;
    if (ifapi_json_UINT16_serialize(in->size, &jso2))
        return TSS2_FAPI_RC_BAD_VALUE;

    json_object_object_add(*jso, "size", jso2);

    jso2 = NULL;
    if (ifapi_json_TPMT_PUBLIC_serialize(&in->publicArea, &jso2))
        return TSS2_FAPI_RC_BAD_VALUE;

    json_object_object_add(*jso, "publicArea", jso2);

    return TSS2_RC_SUCCESS;
}

/** Serialize value of type TPM2B_PRIVATE to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPM2B_PRIVATE.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPM2B_PRIVATE_serialize(const TPM2B_PRIVATE *in, json_object **jso)
{
    return_if_null(in, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    if (in->size > sizeof(_PRIVATE)) {
        LOG_ERROR("Too many bytes for array (%"PRIuPTR" > %"PRIuPTR" = sizeof(_PRIVATE))",
                  (size_t)in->size, (size_t)sizeof(_PRIVATE));
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    char hex_string[((size_t)in->size)*2+1];

    for (size_t i = 0, off = 0; i < in->size; i++, off+=2)
        sprintf(&hex_string[off], "%02x", in->buffer[i]);
    hex_string[(in->size)*2] = '\0';
    *jso = json_object_new_string (hex_string);
    return_if_null(*jso, "Out of memory.", TSS2_FAPI_RC_MEMORY);

    return TSS2_RC_SUCCESS;
}

/** Serialize TPM2_NT to json.
 *
 * @param[in] in constant to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the constant is not of type TPM2_NT.
 */
TSS2_RC
ifapi_json_TPM2_NT_serialize(const TPM2_NT in, json_object **jso)
{
    static const struct { TPM2_NT in; char *name; } tab[] = {
        { TPM2_NT_ORDINARY, "ORDINARY" },
        { TPM2_NT_COUNTER, "COUNTER" },
        { TPM2_NT_BITS, "BITS" },
        { TPM2_NT_EXTEND, "EXTEND" },
        { TPM2_NT_PIN_FAIL, "PIN_FAIL" },
        { TPM2_NT_PIN_PASS, "PIN_PASS" },
    };

    for (size_t i = 0; i < sizeof(tab) / sizeof(tab[0]); i++) {
        if (tab[i].in == in) {
            *jso = json_object_new_string(tab[i].name);
            check_oom(*jso);
            return TSS2_RC_SUCCESS;
        }
    }
    return_error(TSS2_FAPI_RC_BAD_VALUE, "Undefined constant.");
}

/** Serialize a TPMA_NV to json.
 *
 * This function expects the Bitfield to be encoded as unsigned int in host-endianess.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the constant is not of type TPMA_NV.
 */
TSS2_RC
ifapi_json_TPMA_NV_serialize(const TPMA_NV in, json_object **jso)
{
    struct { TPMA_NV in; char *name; } tab[] = {
        { TPMA_NV_PPWRITE, "PPWRITE" },
        { TPMA_NV_OWNERWRITE, "OWNERWRITE" },
        { TPMA_NV_AUTHWRITE, "AUTHWRITE" },
        { TPMA_NV_POLICYWRITE, "POLICYWRITE" },
        { TPMA_NV_POLICY_DELETE, "POLICY_DELETE" },
        { TPMA_NV_WRITELOCKED, "WRITELOCKED" },
        { TPMA_NV_WRITEALL, "WRITEALL" },
        { TPMA_NV_WRITEDEFINE, "WRITEDEFINE" },
        { TPMA_NV_WRITE_STCLEAR, "WRITE_STCLEAR" },
        { TPMA_NV_GLOBALLOCK, "GLOBALLOCK" },
        { TPMA_NV_PPREAD, "PPREAD" },
        { TPMA_NV_OWNERREAD, "OWNERREAD" },
        { TPMA_NV_AUTHREAD, "AUTHREAD" },
        { TPMA_NV_POLICYREAD, "POLICYREAD" },
        { TPMA_NV_NO_DA, "NO_DA" },
        { TPMA_NV_ORDERLY, "ORDERLY" },
        { TPMA_NV_CLEAR_STCLEAR, "CLEAR_STCLEAR" },
        { TPMA_NV_READLOCKED, "READLOCKED" },
        { TPMA_NV_WRITTEN, "WRITTEN" },
        { TPMA_NV_PLATFORMCREATE, "PLATFORMCREATE" },
        { TPMA_NV_READ_STCLEAR, "READ_STCLEAR" },
    };

    UINT32 input;
    input = (UINT32) in;
    json_object *jso_bit;
    if (*jso == NULL) {
        *jso = json_object_new_object();
        return_if_null(*jso, "Out of memory.", TSS2_FAPI_RC_MEMORY);
    }
    size_t n = sizeof(tab) / sizeof(tab[0]);
    size_t i;
    for (i = 0; i < n; i++) {
        if (tab[i].in & input)
            jso_bit = json_object_new_int(1);
        else
            jso_bit = json_object_new_int(0);
        return_if_null(jso_bit, "Out of memory.", TSS2_FAPI_RC_MEMORY);

        json_object_object_add(*jso, tab[i].name, jso_bit);
    }
    TPM2_NT input2 = (TPMA_NV_TPM2_NT_MASK & input)>>4;
    json_object *jso2 = NULL;
    TSS2_RC r = ifapi_json_TPM2_NT_serialize(input2, &jso2);
    return_if_error(r, "Bad value");

    json_object_object_add(*jso, "TPM2_NT", jso2);

    return TSS2_RC_SUCCESS;
}

/** Serialize value of type TPMS_NV_PUBLIC to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMS_NV_PUBLIC.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_NV_PUBLIC_serialize(const TPMS_NV_PUBLIC *in, json_object **jso)
{
    return_if_null(in, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    TSS2_RC r;
    json_object *jso2;
    if (*jso == NULL)
        *jso = json_object_new_object ();
    jso2 = NULL;
    r = ifapi_json_TPMI_RH_NV_INDEX_serialize(in->nvIndex, &jso2);
    return_if_error(r, "Serialize TPMI_RH_NV_INDEX");

    json_object_object_add(*jso, "nvIndex", jso2);
    jso2 = NULL;
    r = ifapi_json_TPMI_ALG_HASH_serialize(in->nameAlg, &jso2);
    return_if_error(r, "Serialize TPMI_ALG_HASH");

    json_object_object_add(*jso, "nameAlg", jso2);
    jso2 = NULL;
    r = ifapi_json_TPMA_NV_serialize(in->attributes, &jso2);
    return_if_error(r, "Serialize TPMA_NV");

    json_object_object_add(*jso, "attributes", jso2);
    jso2 = NULL;
    r = ifapi_json_TPM2B_DIGEST_serialize(&in->authPolicy, &jso2);
    return_if_error(r, "Serialize TPM2B_DIGEST");

    json_object_object_add(*jso, "authPolicy", jso2);
    jso2 = NULL;
    r = ifapi_json_UINT16_serialize(in->dataSize, &jso2);
    return_if_error(r, "Serialize UINT16");

    json_object_object_add(*jso, "dataSize", jso2);
    return TSS2_RC_SUCCESS;
}

/** Serialize a TPM2B_NV_PUBLIC to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPM2B_NV_PUBLIC.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPM2B_NV_PUBLIC_serialize(const TPM2B_NV_PUBLIC *in, json_object **jso)
{
    if (*jso == NULL)
        *jso = json_object_new_object ();
    return_if_null(*jso, "Out of memory.", TSS2_FAPI_RC_MEMORY);

    json_object *jso2;

    jso2 = NULL;
    if (ifapi_json_UINT16_serialize(in->size, &jso2))
        return TSS2_FAPI_RC_BAD_VALUE;

    json_object_object_add(*jso, "size", jso2);

    jso2 = NULL;
    if (ifapi_json_TPMS_NV_PUBLIC_serialize(&in->nvPublic, &jso2))
        return TSS2_FAPI_RC_BAD_VALUE;

    json_object_object_add(*jso, "nvPublic", jso2);

    return TSS2_RC_SUCCESS;
}

/** Serialize value of type TPMS_CREATION_DATA to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMS_CREATION_DATA.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_CREATION_DATA_serialize(const TPMS_CREATION_DATA *in, json_object **jso)
{
    return_if_null(in, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    TSS2_RC r;
    json_object *jso2;
    if (*jso == NULL)
        *jso = json_object_new_object ();
    jso2 = NULL;
    r = ifapi_json_TPML_PCR_SELECTION_serialize(&in->pcrSelect, &jso2);
    return_if_error(r, "Serialize TPML_PCR_SELECTION");

    json_object_object_add(*jso, "pcrSelect", jso2);
    jso2 = NULL;
    r = ifapi_json_TPM2B_DIGEST_serialize(&in->pcrDigest, &jso2);
    return_if_error(r, "Serialize TPM2B_DIGEST");

    json_object_object_add(*jso, "pcrDigest", jso2);
    jso2 = NULL;
    r = ifapi_json_TPMA_LOCALITY_serialize(in->locality, &jso2);
    return_if_error(r, "Serialize TPMA_LOCALITY");

    json_object_object_add(*jso, "locality", jso2);
    jso2 = NULL;
    r = ifapi_json_TPM2_ALG_ID_serialize(in->parentNameAlg, &jso2);
    return_if_error(r, "Serialize TPM2_ALG_ID");

    json_object_object_add(*jso, "parentNameAlg", jso2);
    jso2 = NULL;
    r = ifapi_json_TPM2B_NAME_serialize(&in->parentName, &jso2);
    return_if_error(r, "Serialize TPM2B_NAME");

    json_object_object_add(*jso, "parentName", jso2);
    jso2 = NULL;
    r = ifapi_json_TPM2B_NAME_serialize(&in->parentQualifiedName, &jso2);
    return_if_error(r, "Serialize TPM2B_NAME");

    json_object_object_add(*jso, "parentQualifiedName", jso2);
    jso2 = NULL;
    r = ifapi_json_TPM2B_DATA_serialize(&in->outsideInfo, &jso2);
    return_if_error(r, "Serialize TPM2B_DATA");

    json_object_object_add(*jso, "outsideInfo", jso2);
    return TSS2_RC_SUCCESS;
}

/** Serialize a TPM2B_CREATION_DATA to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPM2B_CREATION_DATA.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPM2B_CREATION_DATA_serialize(const TPM2B_CREATION_DATA *in, json_object **jso)
{
    if (*jso == NULL)
        *jso = json_object_new_object ();
    return_if_null(*jso, "Out of memory.", TSS2_FAPI_RC_MEMORY);

    json_object *jso2;

    jso2 = NULL;
    if (ifapi_json_UINT16_serialize(in->size, &jso2))
        return TSS2_FAPI_RC_BAD_VALUE;

    json_object_object_add(*jso, "size", jso2);

    jso2 = NULL;
    if (ifapi_json_TPMS_CREATION_DATA_serialize(&in->creationData, &jso2))
        return TSS2_FAPI_RC_BAD_VALUE;

    json_object_object_add(*jso, "creationData", jso2);

    return TSS2_RC_SUCCESS;
}
