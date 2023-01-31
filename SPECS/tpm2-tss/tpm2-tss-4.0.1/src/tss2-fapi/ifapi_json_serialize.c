/* SPDX-License-Identifier: BSD-2-Clause */
/*******************************************************************************
 * Copyright 2018-2019, Fraunhofer SIT sponsored by Infineon Technologies AG
 * All rights reserved.
 ******************************************************************************/

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <stdio.h>
#include <string.h>

#include "ifapi_json_serialize.h"
#include "tpm_json_serialize.h"
#include "fapi_policy.h"
#include "tpm_json_deserialize.h"
#include "ifapi_policy_json_serialize.h"
#include "ifapi_config.h"
#include "ifapi_helpers.h"

#define LOGMODULE fapijson
#include "util/log.h"
#include "util/aux_util.h"


/** Serialize a character string to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 */
TSS2_RC
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

/** Serialize value of type UINT8_ARY to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPM2B_DIGEST.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_UINT8_ARY_serialize(const UINT8_ARY *in, json_object **jso)
{
    TSS2_RC r;

    return_if_null(in, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    char *hex_string = malloc((in->size) * 2 + 1);
    return_if_null(hex_string, "Out of memory.", TSS2_FAPI_RC_MEMORY);

    if (in->size > 0) {
        uint8_t *buffer = in->buffer;

        for (size_t i = 0, off = 0; i < in->size; i++, off += 2)
            sprintf(&hex_string[off], "%02x", buffer[i]);
    }
    hex_string[(in->size) * 2] = '\0';
    *jso = json_object_new_string(hex_string);
    goto_if_null2(jso, "Out of memory", r, TSS2_FAPI_RC_MEMORY, error);

    SAFE_FREE(hex_string);
    return TSS2_RC_SUCCESS;

 error:
    SAFE_FREE(hex_string);
    return r;
}

/** Serialize value of type IFAPI_KEY to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type IFAPI_KEY.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_IFAPI_KEY_serialize(const IFAPI_KEY *in, json_object **jso)
{
    return_if_null(in, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    TSS2_RC r;
    json_object *jso2;

    if (*jso == NULL)
        *jso = json_object_new_object();
    jso2 = NULL;
    r = ifapi_json_TPMI_YES_NO_serialize(in->with_auth, &jso2);
    return_if_error(r, "Serialize TPMI_YES_NO");

    json_object_object_add(*jso, "with_auth", jso2);
    jso2 = NULL;
    r = ifapi_json_UINT32_serialize(in->persistent_handle, &jso2);
    return_if_error(r, "Serialize UINT32");

    json_object_object_add(*jso, "persistent_handle", jso2);
    jso2 = NULL;
    r = ifapi_json_TPM2B_PUBLIC_serialize(&in->public, &jso2);
    return_if_error(r, "Serialize TPM2B_PUBLIC");

    json_object_object_add(*jso, "public", jso2);
    jso2 = NULL;
    r = ifapi_json_UINT8_ARY_serialize(&in->serialization, &jso2);
    return_if_error(r, "Serialize UINT8_ARY");

    json_object_object_add(*jso, "serialization", jso2);
    if (in->private.buffer != NULL) {
        jso2 = NULL;
        r = ifapi_json_UINT8_ARY_serialize(&in->private, &jso2);
        return_if_error(r, "Serialize UINT8_ARY");

        json_object_object_add(*jso, "private", jso2);
    }
    if (in->appData.buffer != NULL) {
        jso2 = NULL;
        r = ifapi_json_UINT8_ARY_serialize(&in->appData, &jso2);
        return_if_error(r, "Serialize UINT8_ARY");

        json_object_object_add(*jso, "appData", jso2);
    }
    jso2 = NULL;
    r = ifapi_json_char_serialize(in->policyInstance, &jso2);
    return_if_error(r, "Serialize char");

    json_object_object_add(*jso, "policyInstance", jso2);

    /* Creation Data is not available for imported keys */
    if (in->creationData.size) {
        jso2 = NULL;
        r = ifapi_json_TPM2B_CREATION_DATA_serialize(&in->creationData, &jso2);
        return_if_error(r, "Serialize TPM2B_CREATION_DATA");

        json_object_object_add(*jso, "creationData", jso2);
    }
    /* Creation Hash is not available for imported keys */
    if (in->creationHash.size) {
        jso2 = NULL;
        r = ifapi_json_TPM2B_DIGEST_serialize(&in->creationHash, &jso2);
        return_if_error(r, "Serialize TPM2B_DIGEST");

        json_object_object_add(*jso, "creationHash", jso2);
    }
    /* Creation Ticket is not available for imported keys */
    if (in->creationTicket.tag) {
        jso2 = NULL;
        r = ifapi_json_TPMT_TK_CREATION_serialize(&in->creationTicket, &jso2);
        return_if_error(r, "Serialize TPMT_TK_CREATION");

        json_object_object_add(*jso, "creationTicket", jso2);
    }
    jso2 = NULL;
    r = ifapi_json_char_serialize(in->description, &jso2);
    return_if_error(r, "Serialize char");

    json_object_object_add(*jso, "description", jso2);
    jso2 = NULL;
    r = ifapi_json_char_serialize(in->certificate, &jso2);
    return_if_error(r, "Serialize char");

    json_object_object_add(*jso, "certificate", jso2);

    if (in->public.publicArea.type != TPM2_ALG_KEYEDHASH) {
        /* Keyed hash objects to not need a signing scheme. */
        jso2 = NULL;
        r = ifapi_json_TPMT_SIG_SCHEME_serialize(&in->signing_scheme, &jso2);
        return_if_error(r, "Serialize TPMT_SIG_SCHEME");

        json_object_object_add(*jso, "signing_scheme", jso2);
    }
    jso2 = NULL;
    r = ifapi_json_TPM2B_NAME_serialize(&in->name, &jso2);
    return_if_error(r, "Serialize TPM2B_NAME");

    json_object_object_add(*jso, "name", jso2);
    jso2 = NULL;
    if (in->reset_count) {
        r = ifapi_json_UINT32_serialize(in->reset_count, &jso2);
        return_if_error(r, "Serialize UINT32");

        json_object_object_add(*jso, "reset_count", jso2);
    }
    jso2 = NULL;
    r = ifapi_json_TPMI_YES_NO_serialize(in->delete_prohibited, &jso2);
    return_if_error(r, "Serialize TPMI_YES_NO");

    json_object_object_add(*jso, "delete_prohibited", jso2);

    jso2 = NULL;
    r = ifapi_json_TPMI_YES_NO_serialize(in->ek_profile, &jso2);
    return_if_error(r, "Serialize TPMI_YES_NO");

    json_object_object_add(*jso, "ek_profile", jso2);

    if (in->nonce.size) {
        jso2 = NULL;
        r = ifapi_json_TPM2B_DIGEST_serialize(&in->nonce, &jso2);
        return_if_error(r, "Serialize TPM2B_DIGEST");

        json_object_object_add(*jso, "nonce", jso2);
    }



    return TSS2_RC_SUCCESS;
}

/** Serialize value of type IFAPI_EXT_PUB_KEY to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type IFAPI_EXT_PUB_KEY.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_IFAPI_EXT_PUB_KEY_serialize(const IFAPI_EXT_PUB_KEY *in,
                                       json_object **jso)
{
    return_if_null(in, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    TSS2_RC r;
    json_object *jso2;

    if (*jso == NULL)
        *jso = json_object_new_object();
    jso2 = NULL;
    r = ifapi_json_char_serialize(in->pem_ext_public, &jso2);
    return_if_error(r, "Serialize char");

    json_object_object_add(*jso, "pem_ext_public", jso2);
    jso2 = NULL;
    if (in->certificate) {
        r = ifapi_json_char_serialize(in->certificate, &jso2);
        return_if_error(r, "Serialize char");

        json_object_object_add(*jso, "certificate", jso2);
    }
    if (in->public.publicArea.type) {
        /* Public area was initialized */
        jso2 = NULL;
        r = ifapi_json_TPM2B_PUBLIC_serialize(&in->public, &jso2);
        return_if_error(r, "Serialize TPM2B_PUBLIC");

        json_object_object_add(*jso, "public", jso2);
    }
    return TSS2_RC_SUCCESS;
}

/** Serialize value of type IFAPI_NV to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type IFAPI_NV.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_IFAPI_NV_serialize(const IFAPI_NV *in, json_object **jso)
{
    return_if_null(in, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    TSS2_RC r;
    json_object *jso2;

    if (*jso == NULL)
        *jso = json_object_new_object();
    jso2 = NULL;
    r = ifapi_json_TPMI_YES_NO_serialize(in->with_auth, &jso2);
    return_if_error(r, "Serialize TPMI_YES_NO");

    json_object_object_add(*jso, "with_auth", jso2);

    /* Add tag to classify json NV objects without deserialization */
    jso2 = json_object_new_boolean(true);
    json_object_object_add(*jso, "nv_object", jso2);

    jso2 = NULL;
    r = ifapi_json_TPM2B_NV_PUBLIC_serialize(&in->public, &jso2);
    return_if_error(r, "Serialize TPM2B_NV_PUBLIC");

    json_object_object_add(*jso, "public", jso2);
    jso2 = NULL;
    r = ifapi_json_UINT8_ARY_serialize(&in->serialization, &jso2);
    return_if_error(r, "Serialize UINT8_ARY");

    json_object_object_add(*jso, "serialization", jso2);
    jso2 = NULL;
    r = ifapi_json_UINT32_serialize(in->hierarchy, &jso2);
    return_if_error(r, "Serialize UINT32");

    json_object_object_add(*jso, "hierarchy", jso2);
    jso2 = NULL;
    r = ifapi_json_char_serialize(in->policyInstance, &jso2);
    return_if_error(r, "Serialize char");

    json_object_object_add(*jso, "policyInstance", jso2);
    jso2 = NULL;
    r = ifapi_json_char_serialize(in->description, &jso2);
    return_if_error(r, "Serialize char");

    json_object_object_add(*jso, "description", jso2);

    if (in->appData.buffer != NULL) {
        jso2 = NULL;
        r = ifapi_json_UINT8_ARY_serialize(&in->appData, &jso2);
        return_if_error(r, "Serialize UINT8_ARY");

        json_object_object_add(*jso, "appData", jso2);
    }
    jso2 = NULL;
    if (in->event_log) {
        r = ifapi_json_char_serialize(in->event_log, &jso2);
        return_if_error(r, "Serialize event log");

        json_object_object_add(*jso, "event_log", jso2);
    }
    return TSS2_RC_SUCCESS;
}

/** Serialize value of type IFAPI_NV to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type IFAPI_NV.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_IFAPI_HIERARCHY_serialize(const IFAPI_HIERARCHY *in, json_object **jso)
{
    return_if_null(in, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    TSS2_RC r;
    json_object *jso2;

    if (*jso == NULL)
        *jso = json_object_new_object();
    jso2 = NULL;
    r = ifapi_json_TPMI_YES_NO_serialize(in->with_auth, &jso2);
    return_if_error(r, "Serialize TPMI_YES_NO");

    json_object_object_add(*jso, "with_auth", jso2);

    jso2 = NULL;
    r = ifapi_json_TPM2B_DIGEST_serialize(&in->authPolicy, &jso2);
    return_if_error(r, "Serialize TPM2B_DIGEST");

    json_object_object_add(*jso, "authPolicy", jso2);

    jso2 = NULL;
    r = ifapi_json_char_serialize(in->description, &jso2);
    return_if_error(r, "Serialize char");

    json_object_object_add(*jso, "description", jso2);

    jso2 = NULL;
    r = ifapi_json_UINT32_serialize(in->esysHandle, &jso2);
    return_if_error(r, "Serialize esys handle");

    json_object_object_add(*jso, "esysHandle", jso2);

    return TSS2_RC_SUCCESS;
}

/** Serialize value of type FAPI_QUOTE_INFO to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type FAPI_QUOTE_INFO.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_FAPI_QUOTE_INFO_serialize(const FAPI_QUOTE_INFO *in,
                                     json_object **jso)
{
    return_if_null(in, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    TSS2_RC r;
    json_object *jso2;

    if (*jso == NULL)
        *jso = json_object_new_object();
    jso2 = NULL;
    r = ifapi_json_TPMT_SIG_SCHEME_serialize(&in->sig_scheme, &jso2);
    return_if_error(r, "Serialize TPMT_SIG_SCHEME");

    json_object_object_add(*jso, "sig_scheme", jso2);
    jso2 = NULL;
    r = ifapi_json_TPMS_ATTEST_serialize(&in->attest, &jso2);
    return_if_error(r, "Serialize TPMS_ATTEST");

    json_object_object_add(*jso, "attest", jso2);
    return TSS2_RC_SUCCESS;
}


/** Serialize value of type IFAPI_DUPLICATE to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type IFAPI_DUPLICATE.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_IFAPI_DUPLICATE_serialize(const IFAPI_DUPLICATE *in,
                                     json_object **jso)
{
    return_if_null(in, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    TSS2_RC r;
    json_object *jso2;

    if (*jso == NULL)
        *jso = json_object_new_object();
    jso2 = NULL;
    r = ifapi_json_TPM2B_PRIVATE_serialize(&in->duplicate, &jso2);
    return_if_error(r, "Serialize TPM2B_PRIVATE");

    json_object_object_add(*jso, "duplicate", jso2);
    jso2 = NULL;
    r = ifapi_json_TPM2B_ENCRYPTED_SECRET_serialize(&in->encrypted_seed, &jso2);
    return_if_error(r, "Serialize TPM2B_ENCRYPTED_SECRET");

    json_object_object_add(*jso, "encrypted_seed", jso2);
    jso2 = NULL;
    if (in->certificate) {
        r = ifapi_json_char_serialize(in->certificate, &jso2);
        return_if_error(r, "Serialize certificate");

        json_object_object_add(*jso, "certificate", jso2);
    }
    jso2 = NULL;
    r = ifapi_json_TPM2B_PUBLIC_serialize(&in->public, &jso2);
    return_if_error(r, "Serialize TPM2B_PUBLIC");

    json_object_object_add(*jso, "public", jso2);

    jso2 = NULL;
    r = ifapi_json_TPM2B_PUBLIC_serialize(&in->public_parent, &jso2);
    return_if_error(r, "Serialize TPM2B_PUBLIC");

    json_object_object_add(*jso, "public_parent", jso2);
    if (in->policy) {
        jso2 = NULL;
        r = ifapi_json_TPMS_POLICY_serialize(in->policy, &jso2);
        return_if_error(r, "Serialize policy");

        json_object_object_add(*jso, "policy", jso2);
    }

    return TSS2_RC_SUCCESS;
}

/** Serialize value of type IFAPI_OBJECT_TYPE_CONSTANT to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPM2_HANDLE.
 */
TSS2_RC
ifapi_json_IFAPI_OBJECT_TYPE_CONSTANT_serialize(const IFAPI_OBJECT_TYPE_CONSTANT
        in, json_object **jso)
{
    *jso = json_object_new_int(in);
    if (*jso == NULL) {
        LOG_ERROR("Bad value %"PRIx32 "", in);
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    return TSS2_RC_SUCCESS;
}

/** Serialize a IFAPI_OBJECT to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type IFAPI_OBJECT.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE if an internal error occurred.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_IFAPI_OBJECT_serialize(const IFAPI_OBJECT *in,
                                  json_object **jso)
{
    TSS2_RC r;

    if (*jso == NULL)
        *jso = json_object_new_object();
    return_if_null(*jso, "Out of memory.", TSS2_FAPI_RC_MEMORY);
    json_object *jso2;

    jso2 = NULL;
    r = ifapi_json_IFAPI_OBJECT_TYPE_CONSTANT_serialize(in->objectType, &jso2);
    return_if_error(r, "Serialize IFAPI_OBJECT");

    json_object_object_add(*jso, "objectType", jso2);
    jso2 = NULL;
    r = ifapi_json_TPMI_YES_NO_serialize(in->system, &jso2);
    return_if_error(r, "Serialize TPMI_YES_NO");

    json_object_object_add(*jso, "system", jso2);

    switch (in->objectType) {
    case IFAPI_HIERARCHY_OBJ:
        r = ifapi_json_IFAPI_HIERARCHY_serialize(&in->misc.hierarchy, jso);
        return_if_error(r, "Error serialize FAPI hierarchy object");

        break;
    case IFAPI_NV_OBJ:
        r = ifapi_json_IFAPI_NV_serialize(&in->misc.nv, jso);
        return_if_error(r, "Error serialize FAPI NV object");

        break;

    case IFAPI_DUPLICATE_OBJ:
        r = ifapi_json_IFAPI_DUPLICATE_serialize(&in->misc.key_tree, jso);
        return_if_error(r, "Serialize IFAPI_OBJECT");

        break;

    case IFAPI_KEY_OBJ:
        r = ifapi_json_IFAPI_KEY_serialize(&in->misc.key, jso);
        return_if_error(r, "Error serialize FAPI KEY object");
        break;

    case IFAPI_EXT_PUB_KEY_OBJ:
        r = ifapi_json_IFAPI_EXT_PUB_KEY_serialize(&in->misc.ext_pub_key, jso);
        return_if_error(r, "Serialize IFAPI_OBJECT");

        break;

    default:
        return_error(TSS2_FAPI_RC_GENERAL_FAILURE, "Invalid call get_json");
    }

    if (in->policy) {
        jso2 = NULL;
        r = ifapi_json_TPMS_POLICY_serialize(in->policy, &jso2);
        return_if_error(r, "Serialize policy");

        json_object_object_add(*jso, "policy", jso2);
    }

    if (in->policy) {
        jso2 = NULL;
        r = ifapi_json_TPMS_POLICY_serialize(in->policy, &jso2);
        return_if_error(r, "Serialize policy");

        json_object_object_add(*jso, "policy", jso2);
    }
    return TSS2_RC_SUCCESS;
}

/** Serialize value of type IFAPI_CAP_INFO to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type IFAPI_INFO.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_IFAPI_CAP_INFO_serialize(const IFAPI_CAP_INFO *in, json_object **jso)
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
    r = ifapi_json_TPMS_CAPABILITY_DATA_serialize(in->capability, &jso2);
    return_if_error(r, "Serialize TPMS_CAPABILITY_DATA");

    json_object_object_add(*jso, "info", jso2);

    return TSS2_RC_SUCCESS;
}

/** Serialize value of type IFAPI_INFO to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type IFAPI_INFO.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_IFAPI_INFO_serialize(const IFAPI_INFO *in, json_object **jso)
{
    return_if_null(in, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    TSS2_RC r;
    json_object *jso2;
    json_object *jso_cap_list;
    size_t i;

    if (*jso == NULL)
        *jso = json_object_new_object();
    jso2 = NULL;
    r = ifapi_json_char_serialize(in->fapi_version, &jso2);
    return_if_error(r, "Serialize char");

    json_object_object_add(*jso, "version", jso2);
    jso2 = NULL;
    r = ifapi_json_IFAPI_CONFIG_serialize(&in->fapi_config, &jso2);
    return_if_error(r, "Serialize char");

    json_object_object_add(*jso, "fapi_config", jso2);
    jso_cap_list = json_object_new_array();

    for (i = 0; i < IFAPI_MAX_CAP_INFO; i++) {
        jso2 = NULL;
        r = ifapi_json_IFAPI_CAP_INFO_serialize(&in->cap[i], &jso2);
        return_if_error(r, "Serialize TPMS_CAPABILITY_DATA");

        json_object_array_add(jso_cap_list, jso2);

    }
    json_object_object_add(*jso, "capabilities", jso_cap_list);

    return TSS2_RC_SUCCESS;
}

/** Serialize IFAPI_EVENT_TYPE to json.
 *
 * @param[in] in constant to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the constant is not of type IFAPI_EVENT_TYPE.
 */
TSS2_RC
ifapi_json_IFAPI_EVENT_TYPE_serialize(const IFAPI_EVENT_TYPE in,
                                      json_object **jso)
{
    return ifapi_json_IFAPI_EVENT_TYPE_serialize_txt(in, jso);
}

typedef struct {
    IFAPI_EVENT_TYPE in;
    char *name;
} IFAPI_EVENT_TYPE_ASSIGN;

static IFAPI_EVENT_TYPE_ASSIGN serialize_IFAPI_EVENT_TYPE_tab[] = {
    { IFAPI_IMA_EVENT_TAG,         "ima_template" },
    { IFAPI_PC_CLIENT,             "pcclient_std" },
    { IFAPI_TSS_EVENT_TAG,         "tss2" },
    { IFAPI_CEL_TAG,               "cel"  },
};

/** Get json object for a constant, if a variable is actually of type IFAPI_EVENT_TYPE.
 *
 * @param[in] in binary value of constant.
 * @param[out] str_jso object with text representing the constant.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the constant is not of type IFAPI_EVENT_TYPE.
 */
TSS2_RC
ifapi_json_IFAPI_EVENT_TYPE_serialize_txt(
    const IFAPI_EVENT_TYPE in,
    json_object **str_jso)
{
    size_t n = sizeof(serialize_IFAPI_EVENT_TYPE_tab) / sizeof(
                   serialize_IFAPI_EVENT_TYPE_tab[0]);
    size_t i;
    for (i = 0; i < n; i++) {
        if (serialize_IFAPI_EVENT_TYPE_tab[i].in == in) {
            *str_jso = json_object_new_string(serialize_IFAPI_EVENT_TYPE_tab[i].name);
            return_if_null(str_jso, "Out of memory.", TSS2_FAPI_RC_MEMORY);

            return TSS2_RC_SUCCESS;
        }
    }
    return_error(TSS2_FAPI_RC_BAD_VALUE, "Undefined constant.");
}

/** Serialize value of type IFAPI_TSS_EVENT to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type IFAPI_TSS_EVENT.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_IFAPI_TSS_EVENT_serialize(const IFAPI_TSS_EVENT *in,
                                     json_object **jso)
{
    return_if_null(in, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    TSS2_RC r;
    json_object *jso2;

    if (*jso == NULL)
        *jso = json_object_new_object();
    jso2 = NULL;
    r = ifapi_json_TPM2B_EVENT_serialize(&in->data, &jso2);
    return_if_error(r, "Serialize TPM2B_EVENT");

    json_object_object_add(*jso, "data", jso2);

    if (in->event) {
        /* The in->event field is somewhat special. Its an arbitrary json
           object that shall be serialized under the event field. Thus we
           first have to deserialize the string before we can add it to
           the data structure. */
        jso2 = ifapi_parse_json(in->event);
        return_if_null(jso2, "Event is not valid JSON.", TSS2_FAPI_RC_BAD_VALUE);

        json_object_object_add(*jso, "event", jso2);
    }
    return TSS2_RC_SUCCESS;
}

/** Serialize value of type IFAPI_IMA_EVENT to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type IFAPI_IMA_EVENT.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_IFAPI_IMA_EVENT_serialize(const IFAPI_IMA_EVENT *in,
                                     json_object **jso)
{
    return_if_null(in, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    TSS2_RC r;
    json_object *jso2;

    if (*jso == NULL)
        *jso = json_object_new_object();
    jso2 = NULL;
    r = ifapi_json_UINT8_ARY_serialize(&in->template_value, &jso2);
    return_if_error(r, "Serialize UINT8_ARY");

    json_object_object_add(*jso, "template_value", jso2);
    return TSS2_RC_SUCCESS;
}

/**  Serialize a IFAPI_EVENT_UNION to json.
 *
 * This function expects the Bitfield to be encoded as unsigned int in host-endianess.
 * @param[in] in the value to be serialized.
 * @param[in] selector the type of the event.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type IFAPI_EVENT_UNION.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_IFAPI_EVENT_UNION_serialize(const IFAPI_EVENT_UNION *in,
                                       UINT32 selector, json_object **jso)
{
    if (*jso == NULL)
        *jso = json_object_new_object();
    return_if_null(*jso, "Out of memory.", TSS2_FAPI_RC_MEMORY);

    switch (selector) {
    case IFAPI_TSS_EVENT_TAG:
        return ifapi_json_IFAPI_TSS_EVENT_serialize(&in->tss_event, jso);
    case IFAPI_IMA_EVENT_TAG:
        return ifapi_json_IFAPI_IMA_EVENT_serialize(&in->ima_event, jso);
    case IFAPI_CEL_TAG:
        return ifapi_json_TPMS_EVENT_CELMGT_serialize(&in->cel_event, jso);
    default:
        LOG_ERROR("\nSelector %"PRIx32 " did not match", selector);
        return TSS2_SYS_RC_BAD_VALUE;
    };
    return TSS2_RC_SUCCESS;
}

/** Serialize value of type IFAPI_EVENT to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type IFAPI_EVENT.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_IFAPI_EVENT_serialize(const IFAPI_EVENT *in, json_object **jso)
{
    return_if_null(in, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    TSS2_RC r;
    json_object *recnum = NULL;
    json_object *pcr = NULL;
    json_object *digests = NULL;
    json_object *type = NULL;
    json_object *content = NULL;

    r = ifapi_json_UINT32_serialize(in->recnum, &recnum);
    goto_if_error(r, "Serialize UINT32", error_cleanup);

    r = ifapi_json_TPM2_HANDLE_serialize(in->pcr, &pcr);
    goto_if_error(r, "Serialize TPM2_HANDLE", error_cleanup);

    r = ifapi_json_TPML_DIGEST_VALUES_serialize(&in->digests, &digests);
    goto_if_error(r, "Serialize TPML_DIGEST", error_cleanup);

    r = ifapi_json_IFAPI_EVENT_TYPE_serialize(in->content_type, &type);
    goto_if_error(r, "Serialize IFAPI_EVENT_TYPE", error_cleanup);

    r = ifapi_json_IFAPI_EVENT_UNION_serialize(&in->content, in->content_type, &content);
    goto_if_error(r, "Serialize IFAPI_EVENT_UNION", error_cleanup);

    if (*jso == NULL) {
        *jso = json_object_new_object();
        if (!*jso) {
            goto_error(r, TSS2_FAPI_RC_MEMORY, "OOM", error_cleanup);
        }
    }

    json_object_object_add(*jso, "recnum", recnum);
    json_object_object_add(*jso, "pcr", pcr);
    json_object_object_add(*jso, "digests", digests);
    json_object_object_add(*jso, CONTENT_TYPE, type);
    json_object_object_add(*jso, CONTENT, content);

    return TSS2_RC_SUCCESS;

error_cleanup:
    if (recnum)
        json_object_put(recnum);
    if (pcr)
        json_object_put(pcr);
    if (digests)
        json_object_put(digests);
    if (type)
        json_object_put(type);
    if (content)
        json_object_put(content);
    return r;
}

/** Serializes a configuration JSON object.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type IFAPI_KEY.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_IFAPI_CONFIG_serialize(const IFAPI_CONFIG *in, json_object **jso)
 {
     TSS2_RC r;
     json_object *jso2;

     return_if_null(in, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

     if (*jso == NULL)
         *jso = json_object_new_object();

     jso2 = NULL;
     r = ifapi_json_char_serialize(in->profile_dir, &jso2);
     return_if_error(r, "Serialize char");

     json_object_object_add(*jso, "profile_dir", jso2);

     jso2 = NULL;
     r = ifapi_json_char_serialize(in->user_dir, &jso2);
     return_if_error(r, "Serialize char");

     json_object_object_add(*jso, "user_dir", jso2);

     jso2 = NULL;
     r = ifapi_json_char_serialize(in->keystore_dir, &jso2);
     return_if_error(r, "Serialize char");

     json_object_object_add(*jso, "system_dir", jso2);

     jso2 = NULL;
     r = ifapi_json_char_serialize(in->log_dir, &jso2);
     return_if_error(r, "Serialize char");

     json_object_object_add(*jso, "log_dir", jso2);

     jso2 = NULL;
     r = ifapi_json_char_serialize(in->profile_name, &jso2);
     return_if_error(r, "Serialize char");

     json_object_object_add(*jso, "profile_name", jso2);

     jso2 = NULL;
     r = ifapi_json_char_serialize(in->tcti, &jso2);
     return_if_error(r, "Serialize char");

     json_object_object_add(*jso, "tcti", jso2);

     jso2 = NULL;
     r = ifapi_json_TPML_PCR_SELECTION_serialize(&in->system_pcrs, &jso2);
     return_if_error(r, "Serialize char");

     json_object_object_add(*jso, "system_pcrs", jso2);

     jso2 = NULL;
     r = ifapi_json_char_serialize(in->ek_cert_file, &jso2);
     return_if_error(r, "Serialize char");

     json_object_object_add(*jso, "ek_cert_file", jso2);

     jso2 = NULL;
     r = ifapi_json_TPMI_YES_NO_serialize(in->ek_cert_less, &jso2);
     return_if_error(r, "Serialize yes no");

     json_object_object_add(*jso, "ek_cert_less", jso2);

     if (in->ek_fingerprint.hashAlg) {
         jso2 = NULL;
         ifapi_json_TPMT_HA_serialize(&in->ek_fingerprint, &jso2);
         return_if_error(r, "Serialize char");

         json_object_object_add(*jso, "ek_fingerprint", jso2);
     }

     jso2 = NULL;
     r = ifapi_json_char_serialize(in->intel_cert_service, &jso2);
     return_if_error(r, "Serialize char");

     json_object_object_add(*jso, "intel_cert_service", jso2);

     if (in->firmware_log_file) {
         jso2 = NULL;
         r = ifapi_json_char_serialize(in->firmware_log_file, &jso2);
         return_if_error(r, "Serialize char");

         json_object_object_add(*jso, "firmware_log_file", jso2);
     }

     if (in->ima_log_file) {
         jso2 = NULL;
         r = ifapi_json_char_serialize(in->ima_log_file, &jso2);
         return_if_error(r, "Serialize char");

         json_object_object_add(*jso, "ima_log_file", jso2);
     }

     return TSS2_RC_SUCCESS;
 }

/** Serialize a TPMS_CEL_VERSION structure to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMS_PCR_SELECTION.
 */
TSS2_RC
ifapi_json_TPMS_CEL_VERSION_serialize(
    const TPMS_CEL_VERSION *in,
    json_object **jso)
{
    if (*jso == NULL) {
        *jso = json_object_new_object();
        return_if_null(*jso, "Out of memory.", TSS2_FAPI_RC_MEMORY);
    }
    TSS2_RC r;
    json_object *jso2 = NULL;
    r = ifapi_json_UINT16_serialize(in->major, &jso2);
    return_if_error(r, "Serialize major version");

    json_object_object_add(*jso, "major", jso2);
    jso2 = NULL;
    r = ifapi_json_UINT16_serialize(in->minor, &jso2);
    return_if_error(r, "Serialize minor version");

    json_object_object_add(*jso, "minor", jso2);
    return TSS2_RC_SUCCESS;
}


/**  Serialize a IFAPI_CELU to json.
 *
 * Serialize canonical eventlog management events.
 * @param[in] in the value to be serialized.
 * @param[in] selector the type of the capabilities.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMU_CELMGT.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMU_CELMGT_serialize(const TPMU_CELMGT *in, UINT32 selector, json_object **jso)
{
    json_object *jso2;
    switch (selector) {
        case CEL_VERSION:
            return ifapi_json_TPMS_CEL_VERSION_serialize(&in->cel_version, jso);
        case FIRMWARE_END:
            return ifapi_json_TPMS_EMPTY_serialize(&in->firmware_end, jso);
        case CEL_TIMESTAMP:
            jso2 = NULL;
            if (ifapi_json_UINT64_serialize(in->cel_timestamp, &jso2))
                 return TSS2_FAPI_RC_BAD_VALUE;
            json_object_object_add(*jso, "cel_timestamp", jso2);
            break;
        default:
            LOG_ERROR("\nSelector %"PRIx32 " did not match", selector);
            return TSS2_FAPI_RC_BAD_VALUE;
    };
    return TSS2_RC_SUCCESS;
}

/** Serialize TPMI_CELMGTTYPE to json.
 *
 * @param[in] in variable to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 */
TSS2_RC
ifapi_json_TPMI_CELMGTTYPE_serialize(const TPMI_CELMGTTYPE in, json_object **jso)
{
    static const struct { TPMI_CELMGTTYPE in; const char *name; } jso_tab[] = {
        { CEL_VERSION, "cel_version" },
        { FIRMWARE_END, "firmware_end" }
    };
    CHECK_IN_LIST(TPMI_CELMGTTYPE, in, CEL_VERSION, FIRMWARE_END);
    for (size_t i = 0; i < sizeof(jso_tab) / sizeof(jso_tab[0]); i++) {
        if (jso_tab[i].in == in) {
            *jso = json_object_new_string(jso_tab[i].name);
            check_oom(*jso);
            return TSS2_RC_SUCCESS;
        }
    }
    return_error(TSS2_FAPI_RC_BAD_VALUE, "Undefined constant.");
}

/** Serialize value of type TPMS_EVENT_CELMGT to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPMS_ATTEST.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_EVENT_CELMGT_serialize(const TPMS_EVENT_CELMGT *in, json_object **jso)
{
    return_if_null(in, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    TSS2_RC r;
    json_object *jso2;
    if (*jso == NULL)
        *jso = json_object_new_object ();
    jso2 = NULL;
    jso2 = NULL;
    r = ifapi_json_TPMI_CELMGTTYPE_serialize(in->type, &jso2);
    return_if_jso_error(r, "Serialize TPMI_CELMGTTYPE", jso2);

    json_object_object_add(*jso, "type", jso2);
    jso2 = NULL;
    r = ifapi_json_TPMU_CELMGT_serialize(&in->data, in->type, &jso2);
    return_if_jso_error(r,"Serialize TPMU_CELMGT", jso2);

    if (jso2) {
        json_object_object_add(*jso, "data", jso2);
    }
    return TSS2_RC_SUCCESS;
}
