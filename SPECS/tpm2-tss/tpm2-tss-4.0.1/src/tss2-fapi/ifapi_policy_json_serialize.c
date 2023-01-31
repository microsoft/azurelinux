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
#include "fapi_policy.h"
#include "ifapi_policy_json_serialize.h"

#define LOGMODULE fapijson
#include "util/log.h"
#include "util/aux_util.h"


/** Serialize a character string to json.
 *
 * @param[in]in the character string.
 * @param[out] out the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 */
static TSS2_RC
ifapi_json_char_serialize(
    const char *in,
    json_object **jso)
{
    if (in == NULL) {
        *jso = json_object_new_string("");
    } else {
        *jso = json_object_new_string(in);
    }
    return_if_null(jso, "Out of memory.", TSS2_FAPI_RC_MEMORY);
    return TSS2_RC_SUCCESS;
}

typedef struct {
    TPMI_POLICYTYPE in;
    char *name;
} TPMI_POLICYTYPE_ASSIGN;

static TPMI_POLICYTYPE_ASSIGN serialize_TPMI_POLICYTYPE_tab[] = {
    { POLICYOR, "POLICYOR" },
    { POLICYSIGNED, "POLICYSIGNED" },
    { POLICYSECRET, "POLICYSECRET" },
    { POLICYPCR, "POLICYPCR" },
    { POLICYLOCALITY, "POLICYLOCALITY" },
    { POLICYNV, "POLICYNV" },
    { POLICYCOUNTERTIMER, "POLICYCOUNTERTIMER" },
    { POLICYCOMMANDCODE, "POLICYCOMMANDCODE" },
    { POLICYPHYSICALPRESENCE, "POLICYPHYSICALPRESENCE" },
    { POLICYCPHASH, "POLICYCPHASH" },
    { POLICYNAMEHASH, "POLICYNAMEHASH" },
    { POLICYDUPLICATIONSELECT, "POLICYDUPLICATIONSELECT" },
    { POLICYAUTHORIZE, "POLICYAUTHORIZE" },
    { POLICYAUTHVALUE, "POLICYAUTHVALUE" },
    { POLICYPASSWORD, "POLICYPASSWORD" },
    { POLICYNVWRITTEN, "POLICYNVWRITTEN" },
    { POLICYTEMPLATE, "POLICYTEMPLATE" },
    { POLICYAUTHORIZENV, "POLICYAUTHORIZENV" },
    { POLICYACTION, "POLICYACTION" },
};

/** Get json object for a constant, if a variable is actually of type TPMI_POLICYTYPE.
 *
 * @param[in] in binary value of constant.
 * @param[out] str_jso with text representing the constant.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the constant is not of type TPMI_POLICYTYPE.
 */
TSS2_RC
ifapi_json_TPMI_POLICYTYPE_serialize_txt(
    const TPMI_POLICYTYPE in,
    json_object **str_jso)
{
    size_t n = sizeof(serialize_TPMI_POLICYTYPE_tab) / sizeof(
                   serialize_TPMI_POLICYTYPE_tab[0]);
    size_t i;
    for (i = 0; i < n; i++) {
        if (serialize_TPMI_POLICYTYPE_tab[i].in == in) {
            *str_jso = json_object_new_string(serialize_TPMI_POLICYTYPE_tab[i].name);
            return_if_null(str_jso, "Out of memory.", TSS2_FAPI_RC_MEMORY);

            return TSS2_RC_SUCCESS;
        }
    }
    return_error(TSS2_FAPI_RC_BAD_VALUE, "Undefined constant.");
}

/** Serialize TPMI_POLICYTYPE to json.
 *
 * @param[in] in constant to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the constant is not of type TPMI_POLICYTYPE.
 */
TSS2_RC
ifapi_json_TPMI_POLICYTYPE_serialize(const TPMI_POLICYTYPE in,
                                     json_object **jso)
{
    return ifapi_json_TPMI_POLICYTYPE_serialize_txt(in, jso);
}

/** Serialize value of type TPMS_POLICYSIGNED to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMS_POLICYSIGNED.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_POLICYSIGNED_serialize(const TPMS_POLICYSIGNED *in,
                                       json_object **jso)
{
    return_if_null(in, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    TSS2_RC r;
    json_object *jso2;
    size_t cond_cnt = 0; /**< counter for conditional fields */

    if (*jso == NULL)
        *jso = json_object_new_object();

    if (in->cpHashA.size != 0) {
        jso2 = NULL;
        r = ifapi_json_TPM2B_DIGEST_serialize(&in->cpHashA, &jso2);
        return_if_error(r, "Serialize TPM2B_DIGEST");

        json_object_object_add(*jso, "cpHashA", jso2);
    }
    if (in->policyRef.size != 0) {
        jso2 = NULL;
        r = ifapi_json_TPM2B_NONCE_serialize(&in->policyRef, &jso2);
        return_if_error(r, "Serialize TPM2B_NONCE");

        json_object_object_add(*jso, "policyRef", jso2);
    }
    if (in->keyPath && strlen(in->keyPath) > 0) {
        jso2 = NULL;
        cond_cnt++;
        r = ifapi_json_char_serialize(in->keyPath, &jso2);
        return_if_error(r, "Serialize char");

        json_object_object_add(*jso, "keyPath", jso2);
    }
    if (in->keyPublic.type != 0) {
        jso2 = NULL;
        cond_cnt++;
        r = ifapi_json_TPMT_PUBLIC_serialize(&in->keyPublic, &jso2);
        return_if_error(r, "Serialize TPMT_PUBLIC");

        json_object_object_add(*jso, "keyPublic", jso2);
    }
    if ((in->keyPEM) && strcmp(in->keyPEM, "") != 0) {
        jso2 = NULL;
        cond_cnt++;
        r = ifapi_json_char_serialize(in->keyPEM, &jso2);
        return_if_error(r, "Serialize char");

        json_object_object_add(*jso, "keyPEM", jso2);
    }
    if ((in->publicKeyHint) && strcmp(in->publicKeyHint, "") != 0) {
        jso2 = NULL;
        r = ifapi_json_char_serialize(in->publicKeyHint, &jso2);
        return_if_error(r, "Serialize char");

        json_object_object_add(*jso, "publicKeyHint", jso2);
    }
    if (in->publicKey.size) {
        jso2 = NULL;
        r = ifapi_json_TPM2B_NAME_serialize(&in->publicKey, &jso2);
        return_if_error(r, "Serialize key name");

        json_object_object_add(*jso, "publicKey", jso2);
    }
    if (in->keyPEMhashAlg != 0) {
        jso2 = NULL;
        r = ifapi_json_TPMI_ALG_HASH_serialize(in->keyPEMhashAlg, &jso2);
        return_if_error(r, "Serialize TPMI_ALG_HASH");

        json_object_object_add(*jso, "keyPEMhashAlg", jso2);
    }
    /* Check whether only one conditional is used. */
    if (cond_cnt != 1) {
        return_error(TSS2_FAPI_RC_BAD_VALUE,
                     "Exactly one conditional is allowed for policy signed.");
    }
    jso2 = NULL;
    r = ifapi_json_TPMT_RSA_SCHEME_serialize(&in->rsaScheme, &jso2);
    return_if_error(r, "Serialize RSA scheme");

    json_object_object_add(*jso, "rsaScheme", jso2);

    return TSS2_RC_SUCCESS;
}

/** Serialize value of type TPMS_POLICYSECRET to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMS_POLICYSECRET.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_POLICYSECRET_serialize(const TPMS_POLICYSECRET *in,
                                       json_object **jso)
{
    return_if_null(in, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    TSS2_RC r;
    json_object *jso2;
    size_t cond_cnt = 0; /**< counter for conditional fields */

    if (*jso == NULL)
        *jso = json_object_new_object();
    jso2 = NULL;
    r = ifapi_json_TPM2B_NONCE_serialize(&in->nonceTPM, &jso2);
    return_if_error(r, "Serialize TPM2B_NONCE");

    json_object_object_add(*jso, "nonceTPM", jso2);
    jso2 = NULL;
    r = ifapi_json_TPM2B_DIGEST_serialize(&in->cpHashA, &jso2);
    return_if_error(r, "Serialize TPM2B_DIGEST");

    json_object_object_add(*jso, "cpHashA", jso2);
    if (in->policyRef.size != 0) {
        jso2 = NULL;
        r = ifapi_json_TPM2B_NONCE_serialize(&in->policyRef, &jso2);
        return_if_error(r, "Serialize TPM2B_NONCE");

        json_object_object_add(*jso, "policyRef", jso2);
    }
    jso2 = NULL;
    r = ifapi_json_INT32_serialize(in->expiration, &jso2);
    return_if_error(r, "Serialize INT32");

    json_object_object_add(*jso, "expiration", jso2);
    if ((in->objectPath) && strcmp(in->objectPath, "") != 0) {
        jso2 = NULL;
        cond_cnt++;
        r = ifapi_json_char_serialize(in->objectPath, &jso2);
        return_if_error(r, "Serialize char");

        json_object_object_add(*jso, "objectPath", jso2);
    }
    if (in->objectName.size != 0) {
        jso2 = NULL;
        cond_cnt++;
        r = ifapi_json_TPM2B_NAME_serialize(&in->objectName, &jso2);
        return_if_error(r, "Serialize TPM2B_DIGEST");

        json_object_object_add(*jso, "objectName", jso2);
    }
    if (cond_cnt != 1) {
        return_error(TSS2_FAPI_RC_BAD_VALUE,
                     "Exactly one conditional needed for policy secret .");
    }
    return TSS2_RC_SUCCESS;
}

/** Serialize value of type TPMS_POLICYLOCALITY to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMS_POLICYLOCALITY.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_POLICYLOCALITY_serialize(const TPMS_POLICYLOCALITY *in,
        json_object **jso)
{
    return_if_null(in, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    TSS2_RC r;
    json_object *jso2;

    if (*jso == NULL)
        *jso = json_object_new_object();
    jso2 = NULL;
    r = ifapi_json_TPMA_LOCALITY_serialize(in->locality, &jso2);
    return_if_error(r, "Serialize TPMA_LOCALITY");

    json_object_object_add(*jso, "locality", jso2);
    return TSS2_RC_SUCCESS;
}

/** Serialize value of type TPMS_POLICYNV to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMS_POLICYNV.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_POLICYNV_serialize(const TPMS_POLICYNV *in, json_object **jso)
{
    return_if_null(in, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    TSS2_RC r;
    json_object *jso2;
    size_t cond_cnt = 0; /**< counter for conditional fields */

    if (*jso == NULL)
        *jso = json_object_new_object();
    if ((in->nvPath) && strcmp(in->nvPath, "") != 0) {
        jso2 = NULL;
        cond_cnt++;
        r = ifapi_json_char_serialize(in->nvPath, &jso2);
        return_if_error(r, "Serialize char");

        json_object_object_add(*jso, "nvPath", jso2);
    }
    if (in->nvIndex != 0) {
        jso2 = NULL;
        cond_cnt++;
        r = ifapi_json_TPMI_RH_NV_INDEX_serialize(in->nvIndex, &jso2);
        return_if_error(r, "Serialize TPMI_RH_NV_INDEX");

        json_object_object_add(*jso, "nvIndex", jso2);
    }

    if (in->nvPublic.nvIndex) {
        jso2 = NULL;
        TPM2B_NV_PUBLIC tmp = { 0 };
        tmp.nvPublic = in->nvPublic;
        r = ifapi_json_TPM2B_NV_PUBLIC_serialize(&tmp, &jso2);
        return_if_error(r, "Serialize TPM2B_NV_PUBLIC");

        json_object_object_add(*jso, "nvPublic", jso2);
    }

    jso2 = NULL;
    r = ifapi_json_TPM2B_OPERAND_serialize(&in->operandB, &jso2);
    return_if_error(r, "Serialize TPM2B_OPERAND");

    json_object_object_add(*jso, "operandB", jso2);
    if (in->offset != 0) {
        jso2 = NULL;
        r = ifapi_json_UINT16_serialize(in->offset, &jso2);
        return_if_error(r, "Serialize UINT16");

        json_object_object_add(*jso, "offset", jso2);
    }
    if (in->operation != 0) {
        jso2 = NULL;
        r = ifapi_json_TPM2_EO_serialize(in->operation, &jso2);
        return_if_error(r, "Serialize TPM2_EO");

        json_object_object_add(*jso, "operation", jso2);
    }
    /* Check whether only one conditional is used. */
    if (cond_cnt != 1) {
        return_error(TSS2_FAPI_RC_BAD_VALUE,
                     "Exactly one conditional is allowed for policy NV.");
    }

    return TSS2_RC_SUCCESS;
}

/** Serialize value of type TPMS_POLICYCOUNTERTIMER to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMS_POLICYCOUNTERTIMER.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_POLICYCOUNTERTIMER_serialize(const TPMS_POLICYCOUNTERTIMER *in,
        json_object **jso)
{
    return_if_null(in, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    TSS2_RC r;
    json_object *jso2;

    if (*jso == NULL)
        *jso = json_object_new_object();
    jso2 = NULL;
    r = ifapi_json_TPM2B_OPERAND_serialize(&in->operandB, &jso2);
    return_if_error(r, "Serialize TPM2B_OPERAND");

    json_object_object_add(*jso, "operandB", jso2);
    if (in->offset != 0) {
        jso2 = NULL;
        r = ifapi_json_UINT16_serialize(in->offset, &jso2);
        return_if_error(r, "Serialize UINT16");

        json_object_object_add(*jso, "offset", jso2);
    }
    jso2 = NULL;
    r = ifapi_json_TPM2_EO_serialize(in->operation, &jso2);
    return_if_error(r, "Serialize TPM2_EO");

    json_object_object_add(*jso, "operation", jso2);
    return TSS2_RC_SUCCESS;
}

/** Serialize value of type TPMS_POLICYCOMMANDCODE to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMS_POLICYCOMMANDCODE.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_POLICYCOMMANDCODE_serialize(const TPMS_POLICYCOMMANDCODE *in,
        json_object **jso)
{
    return_if_null(in, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    TSS2_RC r;
    json_object *jso2;

    if (*jso == NULL)
        *jso = json_object_new_object();
    jso2 = NULL;
    r = ifapi_json_TPM2_CC_serialize(in->code, &jso2);
    return_if_error(r, "Serialize TPM2_CC");

    json_object_object_add(*jso, "code", jso2);
    return TSS2_RC_SUCCESS;
}

/** Serialize value of type TPMS_POLICYPHYSICALPRESENCE to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMS_POLICYPHYSICALPRESENCE.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_POLICYPHYSICALPRESENCE_serialize(const
        TPMS_POLICYPHYSICALPRESENCE *in, json_object **jso)
{
    return_if_null(in, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    if (*jso == NULL)
        *jso = json_object_new_object();
    return TSS2_RC_SUCCESS;
}

/** Serialize value of type TPMS_POLICYCPHASH to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMS_POLICYCPHASH.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_POLICYCPHASH_serialize(const TPMS_POLICYCPHASH *in,
                                       json_object **jso)
{
    return_if_null(in, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    TSS2_RC r;
    json_object *jso2;

    if (*jso == NULL)
        *jso = json_object_new_object();
    jso2 = NULL;
    r = ifapi_json_TPM2B_DIGEST_serialize(&in->cpHash, &jso2);
    return_if_error(r, "Serialize TPM2B_DIGEST");

    json_object_object_add(*jso, "cpHash", jso2);
    return TSS2_RC_SUCCESS;
}

/** Serialize value of type TPMS_POLICYNAMEHASH to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMS_POLICYNAMEHASH.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_POLICYNAMEHASH_serialize(const TPMS_POLICYNAMEHASH *in,
        json_object **jso)
{
    return_if_null(in, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    TSS2_RC r;
    json_object *jso2, *jso_ary;
    size_t i;
    size_t cond_cnt = 0; /**< counter for conditional fields */

    if (*jso == NULL) {
        *jso = json_object_new_object();
        return_if_null(jso, "Out of memory.", TSS2_FAPI_RC_MEMORY);
    }

    if (in->nameHash.size) {
        jso2 = NULL;
        cond_cnt++;
        r = ifapi_json_TPM2B_DIGEST_serialize(&in->nameHash, &jso2);
        return_if_error(r, "Serialize TPM2B_DIGEST");

        json_object_object_add(*jso, "nameHash", jso2);

        /* No need to serialize namePaths or objectNames from which would be
           needed to compute nameHash. */
        return TSS2_RC_SUCCESS;
    }

    jso_ary = json_object_new_array();
    return_if_null(jso, "Out of memory.", TSS2_FAPI_RC_MEMORY);

    if (in->namePaths[0]) {
        /* Pathnamees for objects are used */
        cond_cnt++;
        for (i = 0; i < in->count; i++) {
            jso2 = NULL;
            r = ifapi_json_char_serialize(in->namePaths[i], &jso2);
            return_if_error(r, "Serialize char");

            json_object_array_add(jso_ary, jso2);
        }
        json_object_object_add(*jso, "namePaths", jso_ary);
    } else {
        /* TPM object names are used */
        for (i = 0; i < in->count; i++) {
            jso2 = NULL;
            r = ifapi_json_TPM2B_NAME_serialize(&in->objectNames[i], &jso2);
            return_if_error(r, "Serialize TPM2B_NAME");
            json_object_array_add(jso_ary, jso2);
        }
        json_object_object_add(*jso, "objectNames", jso_ary);
    }
    /* Check whether only one condition field found in policy. */
    if (cond_cnt != 1) {
        return_error(TSS2_FAPI_RC_BAD_VALUE,
                     "Exactly one conditional is allowed for policy name hash.");
    }

    return TSS2_RC_SUCCESS;
}

/** Serialize value of type TPMS_POLICYDUPLICATIONSELECT to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMS_POLICYDUPLICATIONSELECT.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_POLICYDUPLICATIONSELECT_serialize(const
        TPMS_POLICYDUPLICATIONSELECT *in, json_object **jso)
{
    return_if_null(in, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    TSS2_RC r;
    json_object *jso2;
    size_t cond_cnt = 0; /**< counter for conditional fields */

    if (*jso == NULL)
        *jso = json_object_new_object();
    jso2 = NULL;
    r = ifapi_json_TPM2B_NAME_serialize(&in->objectName, &jso2);
    return_if_error(r, "Serialize TPM2B_NAME");

    json_object_object_add(*jso, "objectName", jso2);

    if (in->newParentName.size) {
        cond_cnt++;
        jso2 = NULL;
        r = ifapi_json_TPM2B_NAME_serialize(&in->newParentName, &jso2);
        return_if_error(r, "Serialize TPM2B_NAME");

        json_object_object_add(*jso, "newParentName", jso2);
    }
    jso2 = NULL;
    r = ifapi_json_TPMI_YES_NO_serialize(in->includeObject, &jso2);
    return_if_error(r, "Serialize TPMI_YES_NO");

    json_object_object_add(*jso, "includeObject", jso2);

    if (in->newParentPath) {
        jso2 = NULL;
        cond_cnt++;
        r = ifapi_json_char_serialize(in->newParentPath, &jso2);
        return_if_error(r, "Serialize char");

        json_object_object_add(*jso, "newParentPath", jso2);
    }

    if (in->newParentPublic.type) {
        jso2 = NULL;
        cond_cnt++;
        r = ifapi_json_TPMT_PUBLIC_serialize(&in->newParentPublic, &jso2);
        return_if_error(r, "Serialize TPM2B_PUBLIC");

        json_object_object_add(*jso, "newParentPublic", jso2);
    }

    /* Check whether only one condition field found in policy. */
    if (cond_cnt != 1) {
        return_error(TSS2_FAPI_RC_BAD_VALUE,
                     "Exactly one conditional is allowed for policy "
                     "duplication select.");
    }
    return TSS2_RC_SUCCESS;
}

/** Serialize value of type TPMS_POLICYAUTHORIZE to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMS_POLICYAUTHORIZE.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_POLICYAUTHORIZE_serialize(const TPMS_POLICYAUTHORIZE *in,
        json_object **jso)
{
    return_if_null(in, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    TSS2_RC r;
    json_object *jso2;
    size_t cond_cnt = 0; /**< counter for conditional fields */

    if (*jso == NULL)
        *jso = json_object_new_object();
    jso2 = NULL;
    r = ifapi_json_TPM2B_DIGEST_serialize(&in->approvedPolicy, &jso2);
    return_if_error(r, "Serialize TPM2B_DIGEST");

    json_object_object_add(*jso, "approvedPolicy", jso2);
    if (in->policyRef.size != 0) {
        jso2 = NULL;
        r = ifapi_json_TPM2B_NONCE_serialize(&in->policyRef, &jso2);
        return_if_error(r, "Serialize TPM2B_NONCE");

        json_object_object_add(*jso, "policyRef", jso2);
    }
    jso2 = NULL;
    r = ifapi_json_TPM2B_NAME_serialize(&in->keyName, &jso2);
    return_if_error(r, "Serialize TPM2B_NAME");

    json_object_object_add(*jso, "keyName", jso2);
    jso2 = NULL;

    if (in->keyPath) {
        cond_cnt++;
        r = ifapi_json_char_serialize(in->keyPath, &jso2);
        return_if_error(r, "Serialize char");

        json_object_object_add(*jso, "keyPath", jso2);
    }
    if (in->keyPublic.type != 0) {
        jso2 = NULL;
        cond_cnt++;
        r = ifapi_json_TPMT_PUBLIC_serialize(&in->keyPublic, &jso2);
        return_if_error(r, "Serialize TPMT_PUBLIC");

        json_object_object_add(*jso, "keyPublic", jso2);
    }
    if ((in->keyPEM) && strcmp(in->keyPEM, "") != 0) {
        jso2 = NULL;
        r = ifapi_json_char_serialize(in->keyPEM, &jso2);
        return_if_error(r, "Serialize char");

        json_object_object_add(*jso, "keyPEM", jso2);
    }
    if (in->keyPEMhashAlg != 0) {
        jso2 = NULL;
        r = ifapi_json_TPMI_ALG_HASH_serialize(in->keyPEMhashAlg, &jso2);
        return_if_error(r, "Serialize TPMI_ALG_HASH");

        json_object_object_add(*jso, "keyPEMhashAlg", jso2);
    }

    jso2 = NULL;
    r = ifapi_json_TPMT_RSA_SCHEME_serialize(&in->rsaScheme, &jso2);
    return_if_error(r, "Serialize RSA scheme");

    json_object_object_add(*jso, "rsaScheme", jso2);

    return TSS2_RC_SUCCESS;
}

/** Serialize value of type TPMS_POLICYAUTHVALUE to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMS_POLICYAUTHVALUE.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_POLICYAUTHVALUE_serialize(const TPMS_POLICYAUTHVALUE *in,
        json_object **jso)
{
    return_if_null(in, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    if (*jso == NULL)
        *jso = json_object_new_object();
    return TSS2_RC_SUCCESS;
}

/** Serialize value of type TPMS_POLICYPASSWORD to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMS_POLICYPASSWORD.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_POLICYPASSWORD_serialize(const TPMS_POLICYPASSWORD *in,
        json_object **jso)
{
    return_if_null(in, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    if (*jso == NULL)
        *jso = json_object_new_object();
    return TSS2_RC_SUCCESS;
}

/** Serialize value of type TPMS_POLICYNVWRITTEN to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMS_POLICYNVWRITTEN.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_POLICYNVWRITTEN_serialize(const TPMS_POLICYNVWRITTEN *in,
        json_object **jso)
{
    return_if_null(in, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    TSS2_RC r;
    json_object *jso2;

    if (*jso == NULL)
        *jso = json_object_new_object();
    jso2 = NULL;
    r = ifapi_json_TPMI_YES_NO_serialize(in->writtenSet, &jso2);
    return_if_error(r, "Serialize TPMI_YES_NO");

    json_object_object_add(*jso, "writtenSet", jso2);
    return TSS2_RC_SUCCESS;
}

/** Serialize value of type TPMS_POLICYTEMPLATE to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMS_POLICYTEMPLATE.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_POLICYTEMPLATE_serialize(const TPMS_POLICYTEMPLATE *in,
        json_object **jso)
{
    return_if_null(in, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    TSS2_RC r;
    json_object *jso2;
    size_t cond_cnt = 0; /**< counter for conditional fields */

    if (*jso == NULL)
        *jso = json_object_new_object();
    if (in->templateHash.size != 0) {
        jso2 = NULL;
        cond_cnt++;
        r = ifapi_json_TPM2B_DIGEST_serialize(&in->templateHash, &jso2);
        return_if_error(r, "Serialize TPM2B_DIGEST");

        json_object_object_add(*jso, "templateHash", jso2);
    }
    if (in->templatePublic.publicArea.type) {
        jso2 = NULL;
        cond_cnt++;
        r = ifapi_json_TPMT_PUBLIC_serialize(&in->templatePublic.publicArea, &jso2);
        return_if_error(r, "Serialize TPM2B_PUBLIC");

        json_object_object_add(*jso, "templatePublic", jso2);
    }

    /* Check whether only one condition field found in policy. */
    if (cond_cnt != 1) {
        return_error(TSS2_FAPI_RC_BAD_VALUE,
                     "Exactly one conditional is allowed for policy template.");
    }
    return TSS2_RC_SUCCESS;
}

/** Serialize value of type TPMS_POLICYAUTHORIZENV to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMS_POLICYAUTHORIZENV.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_POLICYAUTHORIZENV_serialize(const TPMS_POLICYAUTHORIZENV *in,
        json_object **jso)
{
    return_if_null(in, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    TSS2_RC r;
    json_object *jso2;
    size_t cond_cnt = 0; /**< counter for conditional fields */

    if (*jso == NULL)
        *jso = json_object_new_object();
    jso2 = NULL;
    if (in->nvPath) {
        cond_cnt++;
        r = ifapi_json_char_serialize(in->nvPath, &jso2);
        return_if_error(r, "Serialize char");

        json_object_object_add(*jso, "nvPath", jso2);
    }
    jso2 = NULL;
    if (in->nvPublic.nvIndex > 0) {
        cond_cnt++;
        /* Template already instantiated */
        r = ifapi_json_TPMS_NV_PUBLIC_serialize(&in->nvPublic, &jso2);
        return_if_error(r, "Serialize TPM2B_NV_PUBLIC");

        json_object_object_add(*jso, "nvPublic", jso2);
    }
    if (cond_cnt != 1) {
        return_error(TSS2_FAPI_RC_BAD_VALUE,
                     "Exactly one conditional needed for policy authorize nv .");
    }
    return TSS2_RC_SUCCESS;
}

/** Serialize value of type TPMS_POLICYACTION to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMS_POLICYACTION.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_POLICYACTION_serialize(const TPMS_POLICYACTION *in,
                                       json_object **jso)
{
    return_if_null(in, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    TSS2_RC r;
    json_object *jso2;

    if (*jso == NULL)
        *jso = json_object_new_object();
    jso2 = NULL;
    r = ifapi_json_char_serialize(in->action, &jso2);
    return_if_error(r, "Serialize char");

    json_object_object_add(*jso, "action", jso2);
    return TSS2_RC_SUCCESS;
}

/** Serialize value of type TPMS_PCRVALUE to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMS_PCRVALUE.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_PCRVALUE_serialize(const TPMS_PCRVALUE *in, json_object **jso)
{
    return_if_null(in, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    TSS2_RC r;
    json_object *jso2;

    if (*jso == NULL)
        *jso = json_object_new_object();
    jso2 = NULL;
    r = ifapi_json_UINT32_serialize(in->pcr, &jso2);
    return_if_error(r, "Serialize UINT32");

    json_object_object_add(*jso, "pcr", jso2);
    jso2 = NULL;
    r = ifapi_json_TPM2_ALG_ID_serialize(in->hashAlg, &jso2);
    return_if_error(r, "Serialize TPM2_ALG_ID");

    json_object_object_add(*jso, "hashAlg", jso2);
    jso2 = NULL;
    r = ifapi_json_TPMU_HA_serialize(&in->digest, in->hashAlg, &jso2);
    return_if_error(r, "Serialize TPMU_HA");

    json_object_object_add(*jso, "digest", jso2);
    return TSS2_RC_SUCCESS;
}

/** Serialize value of type TPML_PCRVALUES to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPML_PCRVALUES.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPML_PCRVALUES_serialize(const TPML_PCRVALUES *in, json_object **jso)
{
    TSS2_RC r;
    json_object *jso2;

    if (*jso == NULL)
        *jso = json_object_new_array();
    jso2 = NULL;
    return_if_null(jso, "Out of memory.", TSS2_FAPI_RC_MEMORY);

    for (size_t i = 0; i < in->count; i++) {
        jso2 = NULL;
        r = ifapi_json_TPMS_PCRVALUE_serialize(&in->pcrs[i], &jso2);
        return_if_error(r, "Serialize TPMS_PCRVALUE");

        json_object_array_add(*jso, jso2);
    }
    return TSS2_RC_SUCCESS;
}

/** Serialize value of type TPMS_POLICYPCR to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMS_POLICYPCR.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_POLICYPCR_serialize(const TPMS_POLICYPCR *in, json_object **jso)
{
    return_if_null(in, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    TSS2_RC r;
    json_object *jso2;
    size_t cond_cnt = 0; /**< counter for conditional fields */

    if (in->pcrs) {
        if (*jso == NULL)
            *jso = json_object_new_object();
        jso2 = NULL;
        cond_cnt++;
        r = ifapi_json_TPML_PCRVALUES_serialize(in->pcrs, &jso2);
        return_if_error(r, "Serialize TPML_PCRVALUES");

        json_object_object_add(*jso, "pcrs", jso2);
    }

    if (in->currentPCRandBanks.count) {
        jso2 = NULL;
        cond_cnt++;
        r = ifapi_json_TPML_PCR_SELECTION_serialize(&in->currentPCRandBanks, &jso2);
        return_if_error(r, "Serialize TPML_PCR_SELECTION");

        json_object_object_add(*jso, "currentPCRandBanks", jso2);
    }

    if (in->currentPCRs.sizeofSelect) {
        jso2 = NULL;
        cond_cnt++;
        r = ifapi_json_TPMS_PCR_SELECT_serialize(&in->currentPCRs, &jso2);
        return_if_error(r, "Serialize TPMS_PCR_SELECT");

        json_object_object_add(*jso, "currentPCRs", jso2);
    }
    /* Check whether only one conditional is used. */
    if (cond_cnt != 1) {
        return_error(TSS2_FAPI_RC_BAD_VALUE,
                     "Exactly one conditional is allowed for policy pcr.");
    }
    return TSS2_RC_SUCCESS;
}

/** Serialize value of type TPMS_POLICYAUTHORIZATION to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMS_POLICYAUTHORIZATION.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_POLICYAUTHORIZATION_serialize(
    const TPMS_POLICYAUTHORIZATION *in,
    json_object **jso)
{
    return_if_null(in, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    TSS2_RC r;
    json_object *jso2;

    if (*jso == NULL)
        *jso = json_object_new_object();
    jso2 = NULL;
    r = ifapi_json_char_serialize(in->type, &jso2);
    return_if_error(r, "Serialize char");

    json_object_object_add(*jso, "type", jso2);

    jso2 = NULL;
    r = ifapi_json_TPM2B_NONCE_serialize(&in->policyRef, &jso2);
    return_if_error(r, "Serialize TPM2B_NONCE");

    json_object_object_add(*jso, "policyRef", jso2);

    if (strcmp(in->type, "tpm") == 0) {
        jso2 = NULL;
        r = ifapi_json_TPMT_PUBLIC_serialize(&in->key, &jso2);
        return_if_error(r, "Serialize TPMT_PUBLIC");

        json_object_object_add(*jso, "key", jso2);
        jso2 = NULL;

        jso2 = NULL;
        r = ifapi_json_TPMT_SIGNATURE_serialize(&in->signature, &jso2);
        return_if_error(r, "Serialize TPMT_SIGNATURE");

        json_object_object_add(*jso, "signature", jso2);
    } else if (strcmp(in->type, "pem") == 0) {
        jso2 = NULL;
        r = ifapi_json_char_serialize(in->keyPEM, &jso2);
        return_if_error(r, "Serialize TPMT_PUBLIC");

        json_object_object_add(*jso, "key", jso2);
        jso2 = NULL;

        jso2 = NULL;
        r = ifapi_json_UINT8_ARY_serialize(&in->pemSignature, &jso2);
        return_if_error(r, "Serialize Signature");

        json_object_object_add(*jso, "signature", jso2);

        jso2 = NULL;
        r = ifapi_json_TPMT_RSA_SCHEME_serialize(&in->rsaScheme, &jso2);
        return_if_error(r, "Serialize RSA scheme");

        json_object_object_add(*jso, "rsaScheme", jso2);

        jso2 = NULL;
        r = ifapi_json_TPMI_ALG_HASH_serialize(in->hashAlg, &jso2);
        return_if_error(r, "Serialize hash alg.");

        json_object_object_add(*jso, "hashAlg", jso2);
    } else {
        return_error(TSS2_FAPI_RC_GENERAL_FAILURE, "Invalid key type.");
    }

    return TSS2_RC_SUCCESS;
}

/** Serialize value of type TPML_POLICYAUTHORIZATIONS to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPML_POLICYAUTHORIZATIONS.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPML_POLICYAUTHORIZATIONS_serialize(const TPML_POLICYAUTHORIZATIONS
        *in, json_object **jso)
{
    return_if_null(in, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    TSS2_RC r;
    json_object *jso2;

    if (*jso == NULL)
        *jso = json_object_new_array();
    jso2 = NULL;
    return_if_null(jso, "Out of memory.", TSS2_FAPI_RC_MEMORY);
    jso2 = NULL;
    for (size_t i = 0; i < in->count; i++) {
        jso2 = NULL;
        r = ifapi_json_TPMS_POLICYAUTHORIZATION_serialize(&in->authorizations[i],
                &jso2);
        return_if_error(r, "Serialize TPMS_POLICYAUTHORIZATION");

        json_object_array_add(*jso, jso2);
    }
    return TSS2_RC_SUCCESS;
}

/** Serialize value of type TPMS_POLICYBRANCH to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMS_POLICYBRANCH.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_POLICYBRANCH_serialize(const TPMS_POLICYBRANCH *in,
                                       json_object **jso)
{
    return_if_null(in, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    TSS2_RC r;
    json_object *jso2;

    if (*jso == NULL)
        *jso = json_object_new_object();
    jso2 = NULL;
    r = ifapi_json_char_serialize(in->name, &jso2);
    return_if_error(r, "Serialize char");

    json_object_object_add(*jso, "name", jso2);
    jso2 = NULL;
    r = ifapi_json_char_serialize(in->description, &jso2);
    return_if_error(r, "Serialize char");

    json_object_object_add(*jso, "description", jso2);
    jso2 = NULL;
    r = ifapi_json_TPML_POLICYELEMENTS_serialize(in->policy, &jso2);
    return_if_error(r, "Serialize TPML_POLICYELEMENTS");

    json_object_object_add(*jso, "policy", jso2);
    if (in->policyDigests.count > 0) {
        jso2 = NULL;
        r = ifapi_json_TPML_DIGEST_VALUES_serialize(&in->policyDigests, &jso2);
        return_if_error(r, "Serialize TPML_DIGEST_VALUES");

        json_object_object_add(*jso, "policyDigests", jso2);
    }
    return TSS2_RC_SUCCESS;
}

/** Serialize value of type TPML_POLICYBRANCHES to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPML_POLICYBRANCHES.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPML_POLICYBRANCHES_serialize(const TPML_POLICYBRANCHES *in,
        json_object **jso)
{
    return_if_null(in, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    TSS2_RC r;
    json_object *jso2;

    if (*jso == NULL)
        *jso = json_object_new_array();
    jso2 = NULL;
    return_if_null(jso, "Out of memory.", TSS2_FAPI_RC_MEMORY);
    jso2 = NULL;
    for (size_t i = 0; i < in->count; i++) {
        jso2 = NULL;
        r = ifapi_json_TPMS_POLICYBRANCH_serialize(&in->authorizations[i], &jso2);
        return_if_error(r, "Serialize TPMS_POLICYBRANCH");

        json_object_array_add(*jso, jso2);
    }
    return TSS2_RC_SUCCESS;
}

/** Serialize value of type TPMS_POLICYOR to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMS_POLICYOR.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_POLICYOR_serialize(const TPMS_POLICYOR *in, json_object **jso)
{
    return_if_null(in, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    TSS2_RC r;
    json_object *jso2;

    if (*jso == NULL)
        *jso = json_object_new_object();
    jso2 = NULL;
    r = ifapi_json_TPML_POLICYBRANCHES_serialize(in->branches, &jso2);
    return_if_error(r, "Serialize TPML_POLICYBRANCHES");

    json_object_object_add(*jso, "branches", jso2);
    return TSS2_RC_SUCCESS;
}

/**  Serialize a TPMU_POLICYELEMENT to json.
 *
 * This function expects the Bitfield to be encoded as unsigned int in host-endianess.
 * @param[in] in the value to be serialized.
 * @param[in] selector the type of the policy element.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMU_POLICYELEMENT.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMU_POLICYELEMENT_serialize(const TPMU_POLICYELEMENT *in,
                                        UINT32 selector, json_object **jso)
{
    if (*jso == NULL)
        *jso = json_object_new_object();
    return_if_null(*jso, "Out of memory.", TSS2_FAPI_RC_MEMORY);

    switch (selector) {
    case POLICYOR:
        return ifapi_json_TPMS_POLICYOR_serialize(&in->PolicyOr, jso);
    case POLICYSIGNED:
        return ifapi_json_TPMS_POLICYSIGNED_serialize(&in->PolicySigned, jso);
    case POLICYSECRET:
        return ifapi_json_TPMS_POLICYSECRET_serialize(&in->PolicySecret, jso);
    case POLICYPCR:
        return ifapi_json_TPMS_POLICYPCR_serialize(&in->PolicyPCR, jso);
    case POLICYLOCALITY:
        return ifapi_json_TPMS_POLICYLOCALITY_serialize(&in->PolicyLocality, jso);
    case POLICYNV:
        return ifapi_json_TPMS_POLICYNV_serialize(&in->PolicyNV, jso);
    case POLICYCOUNTERTIMER:
        return ifapi_json_TPMS_POLICYCOUNTERTIMER_serialize(&in->PolicyCounterTimer,
                jso);
    case POLICYCOMMANDCODE:
        return ifapi_json_TPMS_POLICYCOMMANDCODE_serialize(&in->PolicyCommandCode, jso);
    case POLICYPHYSICALPRESENCE:
        return ifapi_json_TPMS_POLICYPHYSICALPRESENCE_serialize(
                   &in->PolicyPhysicalPresence, jso);
    case POLICYCPHASH:
        return ifapi_json_TPMS_POLICYCPHASH_serialize(&in->PolicyCpHash, jso);
    case POLICYNAMEHASH:
        return ifapi_json_TPMS_POLICYNAMEHASH_serialize(&in->PolicyNameHash, jso);
    case POLICYDUPLICATIONSELECT:
        return ifapi_json_TPMS_POLICYDUPLICATIONSELECT_serialize(
                   &in->PolicyDuplicationSelect, jso);
    case POLICYAUTHORIZE:
        return ifapi_json_TPMS_POLICYAUTHORIZE_serialize(&in->PolicyAuthorize, jso);
    case POLICYAUTHVALUE:
        return ifapi_json_TPMS_POLICYAUTHVALUE_serialize(&in->PolicyAuthValue, jso);
    case POLICYPASSWORD:
        return ifapi_json_TPMS_POLICYPASSWORD_serialize(&in->PolicyPassword, jso);
    case POLICYNVWRITTEN:
        return ifapi_json_TPMS_POLICYNVWRITTEN_serialize(&in->PolicyNvWritten, jso);
    case POLICYTEMPLATE:
        return ifapi_json_TPMS_POLICYTEMPLATE_serialize(&in->PolicyTemplate, jso);
    case POLICYAUTHORIZENV:
        return ifapi_json_TPMS_POLICYAUTHORIZENV_serialize(&in->PolicyAuthorizeNv, jso);
    case POLICYACTION:
        return ifapi_json_TPMS_POLICYACTION_serialize(&in->PolicyAction, jso);
    default:
        LOG_ERROR("\nSelector %"PRIx32 " did not match", selector);
        return TSS2_SYS_RC_BAD_VALUE;
    };
    return TSS2_RC_SUCCESS;
}

/** Serialize value of type TPMT_POLICYELEMENT to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMT_POLICYELEMENT.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMT_POLICYELEMENT_serialize(const TPMT_POLICYELEMENT *in,
                                        json_object **jso)
{
    return_if_null(in, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    TSS2_RC r;
    json_object *jso2;

    if (*jso == NULL)
        *jso = json_object_new_object();
    jso2 = NULL;
    r = ifapi_json_TPMI_POLICYTYPE_serialize(in->type, &jso2);
    return_if_error(r, "Serialize TPMI_POLICYTYPE");

    json_object_object_add(*jso, "type", jso2);

    if (in->policyDigests.count > 0) {
        jso2 = NULL;
        r = ifapi_json_TPML_DIGEST_VALUES_serialize(&in->policyDigests, &jso2);
        return_if_error(r, "Serialize TPML_DIGEST_VALUES");

        json_object_object_add(*jso, "policyDigests", jso2);
    }
    r = ifapi_json_TPMU_POLICYELEMENT_serialize(&in->element, in->type, jso);
    return_if_error(r, "Serialize TPMU_POLICYELEMENT");

    return TSS2_RC_SUCCESS;
}

/** Serialize value of type TPML_POLICYELEMENTS to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPML_POLICYELEMENTS.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPML_POLICYELEMENTS_serialize(const TPML_POLICYELEMENTS *in,
        json_object **jso)
{
    return_if_null(in, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    TSS2_RC r;
    json_object *jso2;

    if (*jso == NULL)
        *jso = json_object_new_array();
    jso2 = NULL;
    return_if_null(jso, "Out of memory.", TSS2_FAPI_RC_MEMORY);

    for (size_t i = 0; i < in->count; i++) {
        jso2 = NULL;
        r = ifapi_json_TPMT_POLICYELEMENT_serialize(&in->elements[i], &jso2);
        return_if_error(r, "Serialize TPMT_POLICYELEMENT");

        json_object_array_add(*jso, jso2);
    }
    return TSS2_RC_SUCCESS;
}

/** Serialize value of type TPMS_POLICY to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMS_POLICY.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_POLICY_serialize(const TPMS_POLICY *in,
        json_object **jso)
{
    return_if_null(in, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    TSS2_RC r;
    json_object *jso2;

    if (*jso == NULL)
        *jso = json_object_new_object();
    jso2 = NULL;
    r = ifapi_json_char_serialize(in->description, &jso2);
    return_if_error(r, "Serialize char");

    json_object_object_add(*jso, "description", jso2);
    jso2 = NULL;
    r = ifapi_json_TPML_DIGEST_VALUES_serialize(&in->policyDigests, &jso2);
    return_if_error(r, "Serialize TPML_DIGEST_VALUES");

    json_object_object_add(*jso, "policyDigests", jso2);
    if (in->policyAuthorizations) {
        jso2 = NULL;
        r = ifapi_json_TPML_POLICYAUTHORIZATIONS_serialize(in->policyAuthorizations,
                &jso2);
        return_if_error(r, "Serialize TPML_POLICYAUTHORIZATIONS");

        json_object_object_add(*jso, "policyAuthorizations", jso2);
    }
    jso2 = NULL;
    r = ifapi_json_TPML_POLICYELEMENTS_serialize(in->policy, &jso2);
    return_if_error(r, "Serialize TPML_POLICYELEMENTS");

    json_object_object_add(*jso, "policy", jso2);
    return TSS2_RC_SUCCESS;
}
