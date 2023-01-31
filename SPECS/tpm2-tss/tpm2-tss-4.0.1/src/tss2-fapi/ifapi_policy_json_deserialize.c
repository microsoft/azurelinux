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

#include "ifapi_helpers.h"
#include "tpm_json_deserialize.h"
#include "ifapi_json_deserialize.h"
#include "fapi_policy.h"
#define LOGMODULE fapijson
#include "util/log.h"
#include "util/aux_util.h"

static char *tss_const_prefixes[] = { "TPM2_ALG_", "TPM2_", "TPM_", "TPMA_", "POLICY", NULL };

/** Get the index of a sub string after a certain prefix.
 *
 * The prefixes from table tss_const_prefixes will be used for case
 * insensitive comparison.
 *
 * param[in] token the token with a potential prefix.
 * @retval the position of the sub string after the prefix.
 * @retval 0 if no prefix is found.
 */
static int
get_token_start_idx(const char *token)
{
    int itoken = 0;
    char *entry;
    int i;

    for (i = 0, entry = tss_const_prefixes[0]; entry != NULL;
            i++, entry = tss_const_prefixes[i]) {
        if (strncasecmp(token, entry, strlen(entry)) == 0) {
            itoken += strlen(entry);
            break;
        }
    }
    return itoken;
}

/** Get number from a string.
 *
 * A string which represents a number or hex number (prefix 0x) is converted
 * to an int64 number.
 *
 * param[in] token the string representing the number.
 * param[out] num the converted number.
 * @retval true if token represents a number
 * @retval false if token does not represent a number.
 */
static bool
get_number(const char *token, int64_t *num)
{
    int itoken = 0;
    int pos = 0;
    if (strncmp(token, "0x", 2) == 0) {
        itoken = 2;
        sscanf(&token[itoken], "%"PRIx64"%n", num, &pos);
    } else {
        sscanf(&token[itoken], "%"PRId64"%n", num, &pos);
    }
    if ((size_t)pos == strlen(token) - itoken)
        return true;
    else
        return false;
}

/** Deserialize a TPMI_POLICYTYPE json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 */
TSS2_RC
ifapi_json_TPMI_POLICYTYPE_deserialize(json_object *jso, TPMI_POLICYTYPE *out)
{
    LOG_TRACE("call");
    return ifapi_json_TPMI_POLICYTYPE_deserialize_txt(jso, out);
}

typedef struct {
    TPMI_POLICYTYPE in;
    char *name;
} IFAPI_TPMI_POLICYTYPE_ASSIGN;

static IFAPI_TPMI_POLICYTYPE_ASSIGN deserialize_TPMI_POLICYTYPE_tab[] = {
    { POLICYOR, "Or" },
    { POLICYSIGNED, "Signed" },
    { POLICYSECRET, "Secret" },
    { POLICYPCR, "PCR" },
    { POLICYLOCALITY, "Locality" },
    { POLICYNV, "NV" },
    { POLICYCOUNTERTIMER, "CounterTimer" },
    { POLICYCOMMANDCODE, "CommandCode" },
    { POLICYPHYSICALPRESENCE, "PhysicalPresence" },
    { POLICYCPHASH, "CpHash" },
    { POLICYNAMEHASH, "NameHash" },
    { POLICYDUPLICATIONSELECT, "DuplicationSelect" },
    { POLICYAUTHORIZE, "Authorize" },
    { POLICYAUTHVALUE, "AuthValue" },
    { POLICYPASSWORD, "Password" },
    { POLICYNVWRITTEN, "NvWritten" },
    { POLICYTEMPLATE, "Template" },
    { POLICYAUTHORIZENV, "AuthorizeNv" },
    { POLICYACTION, "Action" },
};

/**  Deserialize a json object of type TPMI_POLICYTYPE.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 */
TSS2_RC
ifapi_json_TPMI_POLICYTYPE_deserialize_txt(json_object *jso,
        TPMI_POLICYTYPE *out)
{
    LOG_TRACE("call");
    const char *token = json_object_get_string(jso);
    int64_t i64;
    if (get_number(token, &i64)) {
        *out = (TPMI_POLICYTYPE) i64;
        if ((int64_t)*out != i64) {
            LOG_ERROR("Bad value");
            return TSS2_FAPI_RC_BAD_VALUE;
        }
        return TSS2_RC_SUCCESS;

    } else {
        int itoken = get_token_start_idx(token);
        size_t i;
        size_t n = sizeof(deserialize_TPMI_POLICYTYPE_tab) /
                   sizeof(deserialize_TPMI_POLICYTYPE_tab[0]);
        size_t size = strlen(token) - itoken;
        for (i = 0; i < n; i++) {
            if (strncasecmp(&token[itoken],
                            &deserialize_TPMI_POLICYTYPE_tab[i].name[0],
                            size) == 0) {
                *out = deserialize_TPMI_POLICYTYPE_tab[i].in;
                return TSS2_RC_SUCCESS;
            }
        }
        return_error(TSS2_FAPI_RC_BAD_VALUE, "Undefined constant.");
    }

}

static char *field_TPMS_POLICYSIGNED_tab[] = {
    "cpHashA",
    "cphasha",
    "policyRef",
    "policyref",
    "keyPath",
    "keypath",
    "keyPublic",
    "keypublic",
    "keyPEM",
    "keypem",
    "publicKeyHint",
    "publickeyhint",
    "publicKey",
    "publickey",
    "keyPEMhashAlg",
    "keypemhashalg",
    "$schema",
    "type",
    "policyDigests",
    "policydigests",
    "nonceTPM",
    "expiration",
    "rsaScheme",
    "rsascheme"
};

/** Deserialize a TPMS_POLICYSIGNED json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 */
TSS2_RC
ifapi_json_TPMS_POLICYSIGNED_deserialize(json_object *jso,
        TPMS_POLICYSIGNED *out)
{
    json_object *jso2;
    TSS2_RC r;
    LOG_TRACE("call");
    return_if_null(out, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);
    size_t cond_cnt = 0; /**< counter for conditional fields */

    ifapi_check_json_object_fields(jso, &field_TPMS_POLICYSIGNED_tab[0],
                                   SIZE_OF_ARY(field_TPMS_POLICYSIGNED_tab));
    if (!ifapi_get_sub_object(jso, "cpHashA", &jso2)) {
        memset(&out->cpHashA, 0, sizeof(TPM2B_DIGEST));
    } else {
        r = ifapi_json_TPM2B_DIGEST_deserialize(jso2, &out->cpHashA);
        return_if_error(r, "Bad value for field \"cpHashA\".");
    }

    if (!ifapi_get_sub_object(jso, "policyRef", &jso2)) {
        memset(&out->policyRef, 0, sizeof(TPM2B_NONCE));
    } else {
        r = ifapi_json_TPM2B_NONCE_deserialize(jso2, &out->policyRef);
        return_if_error(r, "Bad value for field \"policyRef\".");
    }

    out->expiration = 0;

    if (!ifapi_get_sub_object(jso, "keyPath", &jso2)) {
        out->keyPath = NULL;
    } else {
        cond_cnt++;
        r = ifapi_json_char_deserialize(jso2, &out->keyPath);
        return_if_error(r, "Bad value for field \"keyPath\".");
    }

    if (!ifapi_get_sub_object(jso, "keyPublic", &jso2)) {
        memset(&out->keyPublic, 0, sizeof(TPMT_PUBLIC));
    } else {
        cond_cnt++;
        r = ifapi_json_TPMT_PUBLIC_deserialize(jso2, &out->keyPublic);
        return_if_error(r, "Bad value for field \"keyPublic\".");
    }

    if (!ifapi_get_sub_object(jso, "keyPEM", &jso2)) {
        out->keyPEM = NULL;
    } else {
        cond_cnt++;
        r = ifapi_json_char_deserialize(jso2, &out->keyPEM);
        return_if_error(r, "Bad value for field \"keyPEM\".");
    }

    if (!ifapi_get_sub_object(jso, "publicKeyHint", &jso2)) {
        out->publicKeyHint = NULL;
    } else {
        r = ifapi_json_char_deserialize(jso2, &out->publicKeyHint);
        return_if_error(r, "Bad value for field \"publicKeyHint\".");
    }

    if (!ifapi_get_sub_object(jso, "publicKey", &jso2)) {
        memset(&out->publicKey, 0, sizeof(TPM2B_NAME));
    } else {
        r = ifapi_json_TPM2B_NAME_deserialize(jso2, &out->publicKey);
        return_if_error(r, "Bad value for field \"publicKey\".");
    }

    if (!ifapi_get_sub_object(jso, "keyPEMhashAlg", &jso2)) {
        out->keyPEMhashAlg = TPM2_ALG_SHA256;
    } else {
        r = ifapi_json_TPMI_ALG_HASH_deserialize(jso2, &out->keyPEMhashAlg);
        return_if_error(r, "Bad value for field \"keyPEMhashAlg\".");
    }

    if (ifapi_get_sub_object(jso, "rsaScheme", &jso2)) {
        r = ifapi_json_TPMT_RSA_SCHEME_deserialize(jso2, &out->rsaScheme);
        return_if_error(r, "Bad value for field \"rsaScheme\".");
    } else {
        out->rsaScheme.scheme = TPM2_ALG_RSAPSS;
        out->rsaScheme.details.rsapss.hashAlg = out->keyPEMhashAlg;
    }

        /* Check whether only one condition field found in policy. */
    if (cond_cnt != 1) {
        return_error(TSS2_FAPI_RC_BAD_VALUE,
                     "Exactly one conditional is allowed for policy signed.");
    }

    LOG_TRACE("true");
    return TSS2_RC_SUCCESS;
}

static char *field_TPMS_POLICYSECRET_tab[] = {
    "cpHashA",
    "cphasha",
    "policyRef",
    "policyref",
    "objectPath",
    "objectpath",
    "objectName",
    "objectname",
    "$schema",
    "type",
    "policyDigests",
    "nonceTPM",
    "expiration"
};

/** Deserialize a TPMS_POLICYSECRET json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 */
TSS2_RC
ifapi_json_TPMS_POLICYSECRET_deserialize(json_object *jso,
        TPMS_POLICYSECRET *out)
{
    json_object *jso2;
    TSS2_RC r;
    size_t cond_cnt = 0; /**< counter for conditional fields */

    LOG_TRACE("call");
    return_if_null(out, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    ifapi_check_json_object_fields(jso, &field_TPMS_POLICYSECRET_tab[0],
                                   SIZE_OF_ARY(field_TPMS_POLICYSECRET_tab));
    if (!ifapi_get_sub_object(jso, "cpHashA", &jso2)) {
        memset(&out->cpHashA, 0, sizeof(TPM2B_DIGEST));
    } else {
        r = ifapi_json_TPM2B_DIGEST_deserialize(jso2, &out->cpHashA);
        return_if_error(r, "Bad value for field \"cpHashA\".");
    }

    if (!ifapi_get_sub_object(jso, "policyRef", &jso2)) {
        memset(&out->policyRef, 0, sizeof(TPM2B_NONCE));
    } else {
        r = ifapi_json_TPM2B_NONCE_deserialize(jso2, &out->policyRef);
        return_if_error(r, "Bad value for field \"policyRef\".");
    }
    out->expiration = 0;

    if (!ifapi_get_sub_object(jso, "objectPath", &jso2)) {
        out->objectPath = NULL;
    } else {
        cond_cnt++;
        r = ifapi_json_char_deserialize(jso2, &out->objectPath);
        return_if_error(r, "Bad value for field \"objectPath\".");
    }

    if (!ifapi_get_sub_object(jso, "objectName", &jso2)) {
        memset(&out->objectName, 0, sizeof(TPM2B_DIGEST));
    } else {
        cond_cnt++;
        r = ifapi_json_TPM2B_NAME_deserialize(jso2, &out->objectName);
        return_if_error(r, "Bad value for field \"objectName\".");
    }
    if (cond_cnt != 1) {
        return_error(TSS2_FAPI_RC_BAD_VALUE,
                     "Exactly one conditional needed for policy secret .");
    }
    LOG_TRACE("true");
    return TSS2_RC_SUCCESS;
}

static char *field_TPMS_POLICYLOCALITY_tab[] = {
    "locality",
    "$schema",
    "type",
    "policyDigests",
    "nonceTPM"
};

/** Deserialize a TPMS_POLICYLOCALITY json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_POLICYLOCALITY_deserialize(json_object *jso,
        TPMS_POLICYLOCALITY *out)
{
    json_object *jso2;
    TSS2_RC r;
    LOG_TRACE("call");
    return_if_null(out, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    ifapi_check_json_object_fields(jso, &field_TPMS_POLICYLOCALITY_tab[0],
                                   SIZE_OF_ARY(field_TPMS_POLICYLOCALITY_tab));
    if (!ifapi_get_sub_object(jso, "locality", &jso2)) {
        LOG_ERROR("Field \"locality\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPMA_LOCALITY_deserialize(jso2, &out->locality);
    return_if_error(r, "Bad value for field \"locality\".");
    LOG_TRACE("true");
    return TSS2_RC_SUCCESS;
}

static char *field_TPMS_POLICYNV_tab[] = {
    "nvPath",
    "nvpath",
    "nvIndex",
    "nvindex",
    "nvPublic",
    "nvpublic",
    "operandB",
    "operandb",
    "offset",
    "operation",
    "$schema",
    "type",
    "policyDigests",
    "nonceTPM"
};

/** Deserialize a TPMS_POLICYNV json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 */
TSS2_RC
ifapi_json_TPMS_POLICYNV_deserialize(json_object *jso,  TPMS_POLICYNV *out)
{
    json_object *jso2;
    TSS2_RC r;
    size_t cond_cnt = 0; /**< counter for conditional fields */

    LOG_TRACE("call");
    return_if_null(out, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    ifapi_check_json_object_fields(jso, &field_TPMS_POLICYNV_tab[0],
                                   SIZE_OF_ARY(field_TPMS_POLICYNV_tab));
    if (!ifapi_get_sub_object(jso, "nvPath", &jso2)) {
        out->nvPath = NULL;
    } else {
        cond_cnt++;
        r = ifapi_json_char_deserialize(jso2, &out->nvPath);
        return_if_error(r, "Bad value for field \"nvPath\".");
    }

    if (!ifapi_get_sub_object(jso, "nvIndex", &jso2)) {
        out->nvIndex = 0;
    } else {
        cond_cnt++;
        r = ifapi_json_TPMI_RH_NV_INDEX_deserialize(jso2, &out->nvIndex);
        return_if_error(r, "Bad value for field \"nvIndex\".");
    }

    if (!ifapi_get_sub_object(jso, "nvPublic", &jso2)) {
        memset(&out->nvPublic, 0, sizeof(TPM2B_NV_PUBLIC));
    } else {
        TPM2B_NV_PUBLIC tmp = { 0 };
        r = ifapi_json_TPM2B_NV_PUBLIC_deserialize(jso2, &tmp);
        return_if_error(r, "Bad value for field \"nvPublic\".");
        out->nvPublic = tmp.nvPublic;
    }

    if (!ifapi_get_sub_object(jso, "operandB", &jso2)) {
        LOG_ERROR("Field \"operandB\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPM2B_OPERAND_deserialize(jso2, &out->operandB);
    return_if_error(r, "Bad value for field \"operandB\".");

    if (!ifapi_get_sub_object(jso, "offset", &jso2)) {
        out->offset = 0;
    } else {
        r = ifapi_json_UINT16_deserialize(jso2, &out->offset);
        return_if_error(r, "Bad value for field \"offset\".");
    }

    if (!ifapi_get_sub_object(jso, "operation", &jso2)) {
        out->operation = 0;
    } else {
        r = ifapi_json_TPM2_EO_deserialize(jso2, &out->operation);
        return_if_error(r, "Bad value for field \"operation\".");
    }
    /* Check whether only one conditional is used. */
    if (cond_cnt != 1) {
        return_error(TSS2_FAPI_RC_BAD_VALUE,
                     "Exactly one conditional is allowed for policy NV.");
    }

    LOG_TRACE("true");
    return TSS2_RC_SUCCESS;
}

static char *field_TPMS_POLICYCOUNTERTIMER_tab[] = {
    "operandB",
    "operandb",
    "offset",
    "operation",
    "$schema",
    "type",
    "policyDigests",
    "nonceTPM"
};

/** Deserialize a TPMS_POLICYCOUNTERTIMER json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_POLICYCOUNTERTIMER_deserialize(json_object *jso,
        TPMS_POLICYCOUNTERTIMER *out)
{
    json_object *jso2;
    TSS2_RC r;
    LOG_TRACE("call");
    return_if_null(out, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    ifapi_check_json_object_fields(jso, &field_TPMS_POLICYCOUNTERTIMER_tab[0],
                                   SIZE_OF_ARY(field_TPMS_POLICYCOUNTERTIMER_tab));
    if (!ifapi_get_sub_object(jso, "operandB", &jso2)) {
        LOG_ERROR("Field \"operandB\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPM2B_OPERAND_deserialize(jso2, &out->operandB);
    return_if_error(r, "Bad value for field \"operandB\".");

    if (!ifapi_get_sub_object(jso, "offset", &jso2)) {
        out->offset = 0;
    } else {
        r = ifapi_json_UINT16_deserialize(jso2, &out->offset);
        return_if_error(r, "Bad value for field \"offset\".");
    }

    if (!ifapi_get_sub_object(jso, "operation", &jso2)) {
        LOG_ERROR("Field \"operation\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPM2_EO_deserialize(jso2, &out->operation);
    return_if_error(r, "Bad value for field \"operation\".");
    LOG_TRACE("true");
    return TSS2_RC_SUCCESS;
}

static char *field_TPMS_POLICYCOMMANDCODE_tab[] = {
    "code",
    "$schema",
    "type",
    "policyDigests",
    "nonceTPM"
};

/** Deserialize a TPMS_POLICYCOMMANDCODE json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_POLICYCOMMANDCODE_deserialize(json_object *jso,
        TPMS_POLICYCOMMANDCODE *out)
{
    json_object *jso2;
    TSS2_RC r;
    LOG_TRACE("call");
    return_if_null(out, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    ifapi_check_json_object_fields(jso, &field_TPMS_POLICYCOMMANDCODE_tab[0],
                                   SIZE_OF_ARY(field_TPMS_POLICYCOMMANDCODE_tab));
    if (!ifapi_get_sub_object(jso, "code", &jso2)) {
        LOG_ERROR("Field \"code\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPM2_CC_deserialize(jso2, &out->code);
    return_if_error(r, "Bad value for field \"code\".");
    LOG_TRACE("true");
    return TSS2_RC_SUCCESS;
}

/** Deserialize a TPMS_POLICYPHYSICALPRESENCE json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 */
TSS2_RC
ifapi_json_TPMS_POLICYPHYSICALPRESENCE_deserialize(json_object *jso,
        TPMS_POLICYPHYSICALPRESENCE *out)
{
    LOG_TRACE("call");
    UNUSED(jso);
    UNUSED(out);

    LOG_TRACE("true");
    return TSS2_RC_SUCCESS;
}

static char *field_TPMS_POLICYCPHASH_tab[] = {
    "cpHash",
    "cphash",
    "$schema",
    "type",
    "policyDigests",
    "nonceTPM"
};

/** Deserialize a TPMS_POLICYCPHASH json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_POLICYCPHASH_deserialize(json_object *jso,
        TPMS_POLICYCPHASH *out)
{
    json_object *jso2;
    TSS2_RC r;
    LOG_TRACE("call");
    return_if_null(out, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    ifapi_check_json_object_fields(jso, &field_TPMS_POLICYCPHASH_tab[0],
                                   SIZE_OF_ARY(field_TPMS_POLICYCPHASH_tab));
    if (!ifapi_get_sub_object(jso, "cpHash", &jso2)) {
        LOG_ERROR("Field \"cpHash\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPM2B_DIGEST_deserialize(jso2, &out->cpHash);
    return_if_error(r, "Bad value for field \"cpHash\".");
    LOG_TRACE("true");
    return TSS2_RC_SUCCESS;
}

static char *field_TPMS_POLICYNAMEHASH_tab[] = {
    "nameHash",
    "namehash",
    "namePaths",
    "namepaths",
    "objectNames",
    "objectnames",
    "$schema",
    "type",
    "policyDigests",
    "nonceTPM"
};

/** Deserialize a TPMS_POLICYNAMEHASH json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 */
TSS2_RC
ifapi_json_TPMS_POLICYNAMEHASH_deserialize(json_object *jso,
        TPMS_POLICYNAMEHASH *out)
{
    json_object *jso2, *jso3;
    TSS2_RC r;
    size_t i, n_paths = 0, n_names = 0;
    size_t cond_cnt = 0; /**< counter for conditional fields */

    LOG_TRACE("call");
    memset(out, 0, sizeof(TPMS_POLICYNAMEHASH));
    return_if_null(out, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    ifapi_check_json_object_fields(jso, &field_TPMS_POLICYNAMEHASH_tab[0],
                                   SIZE_OF_ARY(field_TPMS_POLICYNAMEHASH_tab));
    if (ifapi_get_sub_object(jso, "nameHash", &jso2)) {
        cond_cnt++;
        r = ifapi_json_TPM2B_DIGEST_deserialize(jso2, &out->nameHash);
        return_if_error(r, "Bad value for field \"nameHash\".");

        /* No need to deserialize namePaths or objectNames from which nameHash would
           be derived. */
        return TSS2_RC_SUCCESS;
    }

    if (ifapi_get_sub_object(jso, "namePaths", &jso2)) {
        json_type jso_type = json_object_get_type(jso2);
        cond_cnt++;
        if (jso_type == json_type_array) {
            n_paths = json_object_array_length(jso2);
            if (n_paths > 3) {
                return_error(TSS2_FAPI_RC_BAD_VALUE,
                             "More than 3 path names in policy name hash.");
            }
            for (i = 0; i < n_paths; i++) {
                jso3 = json_object_array_get_idx(jso2, i);
                r = ifapi_json_char_deserialize(jso3, &out->namePaths[i]);
                return_if_error(r, "Bad value for field \"namePaths\".");
            }
            out->count = n_paths;
        } else {
            LOG_ERROR("No list of name paths");
            return TSS2_FAPI_RC_BAD_VALUE;
        }

    }
    if (ifapi_get_sub_object(jso, "objectNames", &jso2)) {
        json_type jso_type = json_object_get_type(jso);
        if (jso_type == json_type_array) {
            n_names = json_object_array_length(jso2);
            if (n_paths > 0 && n_names > 0) {
                return_error(TSS2_FAPI_RC_BAD_VALUE,
                             "Only pathname or only TPM names are allowed "
                             "for policy name hash.");
            }
            if (n_names > 3) {
                return_error(TSS2_FAPI_RC_BAD_VALUE,
                             "More than 3 names in policy name hash.");
            }
            for (i = 0; i < n_names; i++) {
                jso3 = json_object_array_get_idx(jso, i);
                r = ifapi_json_TPM2B_NAME_deserialize(jso3, &out->objectNames[i]);
                return_if_error(r, "BAD TEMPLATE");
            }
            out->count = n_names;
        } else {
            LOG_ERROR("No list of object names");
            return TSS2_FAPI_RC_BAD_VALUE;
        }
    }
    if (out->count == 0) {
        LOG_ERROR("No list of object names or path names");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    /* Check whether only one condition field found in policy. */
    if (cond_cnt != 1) {
        return_error(TSS2_FAPI_RC_BAD_VALUE,
                     "Exactly one conditional is allowed for policy name hash.");
    }
    return TSS2_RC_SUCCESS;
}

static char *field_TPMS_POLICYDUPLICATIONSELECT_tab[] = {
    "includeObject",
    "includeobject",
    "newParentPath",
    "newparentpath",
    "objectName",
    "objectname",
    "newParentName",
    "newparentname",
    "newParentPublic",
    "newparentpublic",
    "$schema",
    "type",
    "policyDigests",
    "nonceTPM"
};

/** Deserialize a TPMS_POLICYDUPLICATIONSELECT json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 */
TSS2_RC
ifapi_json_TPMS_POLICYDUPLICATIONSELECT_deserialize(json_object *jso,
        TPMS_POLICYDUPLICATIONSELECT *out)
{
    json_object *jso2;
    TSS2_RC r;
    size_t cond_cnt = 0; /**< counter for conditional fields */

    LOG_TRACE("call");
    return_if_null(out, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    GET_OPTIONAL(objectName, "objectName", TPM2B_NAME);
    GET_OPTIONAL(newParentName, "newParentName", TPM2B_NAME);
    ifapi_check_json_object_fields(jso, &field_TPMS_POLICYDUPLICATIONSELECT_tab[0],
                                   SIZE_OF_ARY(field_TPMS_POLICYDUPLICATIONSELECT_tab));
    if (out->newParentName.size)
        cond_cnt++;
    if (ifapi_get_sub_object(jso, "includeObject", &jso2)) {
        r = ifapi_json_TPMI_YES_NO_deserialize(jso2, &out->includeObject);
        return_if_error(r, "Yes or No expected.");
    } else {
        if (out->objectName.size > 0)
            out->includeObject = TPM2_YES;
        else
            out->includeObject = TPM2_NO;
    }
    GET_CONDITIONAL_TPM2B(newParentPublic, "newParentPublic", TPM2B_PUBLIC, TPMT_PUBLIC,
                          publicArea, cond_cnt);

    if (!ifapi_get_sub_object(jso, "newParentPath", &jso2)) {
        if (!out->newParentPublic.type) {
            if (!out->newParentName.size) {
                return_error(TSS2_FAPI_RC_BAD_VALUE,
                             "No path, new parent public, or new parent name ");
            }
        }
        out->newParentPath = NULL;
    } else {
        cond_cnt++;
        r = ifapi_json_char_deserialize(jso2, &out->newParentPath);
        return_if_error(r, "Bad value for field \"newParentPath\".");
    }
    /* Check whether only one condition field found in policy. */
    if (cond_cnt != 1) {
        return_error(TSS2_FAPI_RC_BAD_VALUE,
                     "Exactly one conditional is allowed for "
                     "policy duplication select.");
    }
    LOG_TRACE("true");
    return TSS2_RC_SUCCESS;
}

static char *field_TPMS_POLICYAUTHORIZE_tab[] = {
    "approvedPolicy",
    "approvedpolicy",
    "policyRef",
    "policyref",
    "keyName",
    "keyname",
    "keyPath",
    "keypath",
    "keyPublic",
    "keypublic",
    "keyPEM",
    "keypem",
    "keyPEMhashAlg",
    "keypemhashalg",
    "$schema",
    "type",
    "policyDigests",
    "nonceTPM",
    "rsaScheme",
    "rsascheme"
};

/** Deserialize a TPMS_POLICYAUTHORIZE json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 */
TSS2_RC
ifapi_json_TPMS_POLICYAUTHORIZE_deserialize(json_object *jso,
        TPMS_POLICYAUTHORIZE *out)
{
    json_object *jso2;
    TSS2_RC r;
    size_t cond_cnt = 0; /**< counter for conditional fields */

    LOG_TRACE("call");
    return_if_null(out, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    ifapi_check_json_object_fields(jso, &field_TPMS_POLICYAUTHORIZE_tab[0],
                                   SIZE_OF_ARY(field_TPMS_POLICYAUTHORIZE_tab));
    if (!ifapi_get_sub_object(jso, "approvedPolicy", &jso2)) {
        memset(&out->approvedPolicy, 0, sizeof(TPM2B_DIGEST));
    } else {
        r = ifapi_json_TPM2B_DIGEST_deserialize(jso2, &out->approvedPolicy);
        return_if_error(r, "Bad value for field \"approvedPolicy\".");
    }

    if (!ifapi_get_sub_object(jso, "policyRef", &jso2)) {
        memset(&out->policyRef, 0, sizeof(TPM2B_NONCE));
    } else {
        r = ifapi_json_TPM2B_NONCE_deserialize(jso2, &out->policyRef);
        return_if_error(r, "Bad value for field \"policyRef\".");
    }

    if (!ifapi_get_sub_object(jso, "keyName", &jso2)) {
        memset(&out->keyName, 0, sizeof(TPM2B_NAME));
    } else {
        r = ifapi_json_TPM2B_NAME_deserialize(jso2, &out->keyName);
        return_if_error(r, "Bad value for field \"keyName\".");
    }

    if (ifapi_get_sub_object(jso, "keyPath", &jso2)) {
        cond_cnt++;
        r = ifapi_json_char_deserialize(jso2, &out->keyPath);
        return_if_error(r, "Bad value for field \"keyPath\".");
    } else {
        out->keyPath = NULL;
    }

    if (!ifapi_get_sub_object(jso, "keyPublic", &jso2)) {
        memset(&out->keyPublic, 0, sizeof(TPMT_PUBLIC));
    } else {
        cond_cnt++;
        r = ifapi_json_TPMT_PUBLIC_deserialize(jso2, &out->keyPublic);
        return_if_error(r, "Bad value for field \"keyPublic\".");
    }

    if (!ifapi_get_sub_object(jso, "keyPEM", &jso2)) {
        out->keyPEM = NULL;
    } else {
        cond_cnt++;
        r = ifapi_json_char_deserialize(jso2, &out->keyPEM);
        return_if_error(r, "Bad value for field \"keyPEM\".");
    }

    if (!ifapi_get_sub_object(jso, "keyPEMhashAlg", &jso2)) {
        out->keyPEMhashAlg = TPM2_ALG_SHA256;
    } else {
        r = ifapi_json_TPMI_ALG_HASH_deserialize(jso2, &out->keyPEMhashAlg);
        return_if_error(r, "Bad value for field \"keyPEMhashAlg\".");
    }

    if (ifapi_get_sub_object(jso, "rsaScheme", &jso2)) {
        r = ifapi_json_TPMT_RSA_SCHEME_deserialize(jso2, &out->rsaScheme);
        return_if_error(r, "Bad value for field \"rsaScheme\".");
    } else {
        out->rsaScheme.scheme = TPM2_ALG_RSAPSS;
        out->rsaScheme.details.rsapss.hashAlg = out->keyPEMhashAlg;
    }
    /* Check whether only one condition field found in policy. */
    if (cond_cnt != 1) {
        return_error(TSS2_FAPI_RC_BAD_VALUE,
                     "Exactly one conditional is allowed for policy authorize.");
    }
    LOG_TRACE("true");
    return TSS2_RC_SUCCESS;
}

/** Deserialize a TPMS_POLICYAUTHVALUE json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 */
TSS2_RC
ifapi_json_TPMS_POLICYAUTHVALUE_deserialize(json_object *jso,
        TPMS_POLICYAUTHVALUE *out)
{
    LOG_TRACE("call");
    UNUSED(out);
    UNUSED(jso);

    LOG_TRACE("true");
    return TSS2_RC_SUCCESS;
}

/** Deserialize a TPMS_POLICYPASSWORD json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 */
TSS2_RC
ifapi_json_TPMS_POLICYPASSWORD_deserialize(json_object *jso,
        TPMS_POLICYPASSWORD *out)
{
    LOG_TRACE("call");
    UNUSED(jso);
    UNUSED(out);

    LOG_TRACE("true");
    return TSS2_RC_SUCCESS;
}

static char *field_TPMS_POLICYNVWRITTEN_tab[] = {
    "writtenSet",
    "writtenset",
    "$schema",
    "type",
    "policyDigests",
    "nonceTPM"
};

/** Deserialize a TPMS_POLICYNVWRITTEN json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_POLICYNVWRITTEN_deserialize(json_object *jso,
        TPMS_POLICYNVWRITTEN *out)
{
    json_object *jso2;
    TSS2_RC r;
    LOG_TRACE("call");
    return_if_null(out, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    ifapi_check_json_object_fields(jso, &field_TPMS_POLICYNVWRITTEN_tab[0],
                                   SIZE_OF_ARY(field_TPMS_POLICYNVWRITTEN_tab));
    if (!ifapi_get_sub_object(jso, "writtenSet", &jso2)) {
        out->writtenSet = TPM2_YES;
        return TSS2_RC_SUCCESS;
    }
    r = ifapi_json_TPMI_YES_NO_deserialize(jso2, &out->writtenSet);
    return_if_error(r, "Bad value for field \"writtenSet\".");
    LOG_TRACE("true");
    return TSS2_RC_SUCCESS;
}

static char *field_TPMS_POLICYTEMPLATE_tab[] = {
    "templateHash",
    "templatehash",
    "templatePublic",
    "templatepublic",
    "templateName",
    "templatename",
    "$schema",
    "type",
    "policyDigests",
    "nonceTPM"
};

/** Deserialize a TPMS_POLICYTEMPLATE json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 */
TSS2_RC
ifapi_json_TPMS_POLICYTEMPLATE_deserialize(json_object *jso,
        TPMS_POLICYTEMPLATE *out)
{
    json_object *jso2;
    TSS2_RC r;
    size_t cond_cnt = 0; /**< counter for conditional fields */

    LOG_TRACE("call");
    return_if_null(out, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    ifapi_check_json_object_fields(jso, &field_TPMS_POLICYTEMPLATE_tab[0],
                                   SIZE_OF_ARY(field_TPMS_POLICYTEMPLATE_tab));
    if (!ifapi_get_sub_object(jso, "templateHash", &jso2)) {
        memset(&out->templateHash, 0, sizeof(TPM2B_DIGEST));
    } else {
        cond_cnt++;
        r = ifapi_json_TPM2B_DIGEST_deserialize(jso2, &out->templateHash);
        return_if_error(r, "Bad value for field \"templateHash\".");
    }

    if (!ifapi_get_sub_object(jso, "templatePublic", &jso2)) {
        memset(&out->templatePublic, 0, sizeof(TPM2B_PUBLIC));
    } else {
        cond_cnt++;
        r = ifapi_json_TPMT_PUBLIC_deserialize(jso2, &out->templatePublic.publicArea);
        return_if_error(r, "Bad value for field \"templatePublic\".");

        out->templatePublic.size = 0;
    }

    /* Check whether only one condition field found in policy. */
    if (cond_cnt != 1) {
        return_error(TSS2_FAPI_RC_BAD_VALUE,
                     "Exactly one conditional is allowed for policy template.");
    }

    LOG_TRACE("true");
    return TSS2_RC_SUCCESS;
}

static char *field_TPMS_POLICYAUTHORIZENV_tab[] = {
    "nvPath",
    "nvpath",
    "nvPublic",
    "nvpublic",
    "$schema",
    "type",
    "policyDigests",
    "nonceTPM"
};

/** Deserialize a TPMS_POLICYAUTHORIZENV json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 */
TSS2_RC
ifapi_json_TPMS_POLICYAUTHORIZENV_deserialize(json_object *jso,
        TPMS_POLICYAUTHORIZENV *out)
{
    json_object *jso2;
    TSS2_RC r;
    size_t cond_cnt = 0; /**< counter for conditional fields */

    LOG_TRACE("call");
    return_if_null(out, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    memset(out, 0, sizeof(TPMS_POLICYAUTHORIZENV));

    ifapi_check_json_object_fields(jso, &field_TPMS_POLICYAUTHORIZENV_tab[0],
                                   SIZE_OF_ARY(field_TPMS_POLICYAUTHORIZENV_tab));
    if (ifapi_get_sub_object(jso, "nvPath", &jso2)) {
        cond_cnt++;
        r = ifapi_json_char_deserialize(jso2, &out->nvPath);
        return_if_error(r, "Bad value for field \"nvPath\".");
    } else {
        out->nvPath = NULL;
    }

    GET_CONDITIONAL_TPM2B(nvPublic, "nvPublic", TPM2B_NV_PUBLIC, TPMS_NV_PUBLIC,
                          nvPublic, cond_cnt);

    /* Check whether only one condition field found in policy. */
    if (cond_cnt != 1) {
        return_error(TSS2_FAPI_RC_BAD_VALUE,
                     "Exactly one conditional is allowed for policy signed.");
    }

    LOG_TRACE("true");
    return TSS2_RC_SUCCESS;
}

static char *field_TPMS_POLICYACTION_tab[] = {
    "action",
    "$schema",
    "type",
    "policyDigests",
    "nonceTPM"
};

/** Deserialize a TPMS_POLICYACTION json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 */
TSS2_RC
ifapi_json_TPMS_POLICYACTION_deserialize(json_object *jso,
        TPMS_POLICYACTION *out)
{
    json_object *jso2;
    TSS2_RC r;
    LOG_TRACE("call");
    return_if_null(out, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    memset(out, 0, sizeof(*out));

    ifapi_check_json_object_fields(jso, &field_TPMS_POLICYACTION_tab[0],
                                   SIZE_OF_ARY(field_TPMS_POLICYACTION_tab));
    if (!ifapi_get_sub_object(jso, "action", &jso2)) {
        LOG_ERROR("Field \"action\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_char_deserialize(jso2, &out->action);
    return_if_error(r, "Bad value for field \"action\".");
    LOG_TRACE("true");
    return TSS2_RC_SUCCESS;
}

static char *field_TPMS_PCRVALUE_tab[] = {
    "pcr",
    "hashAlg",
    "hashalg",
    "digest",
    "$schema"
};

/** Deserialize a TPMS_PCRVALUE json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_PCRVALUE_deserialize(json_object *jso,  TPMS_PCRVALUE *out)
{
    json_object *jso2;
    TSS2_RC r;

    LOG_TRACE("call");
    return_if_null(out, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    ifapi_check_json_object_fields(jso, &field_TPMS_PCRVALUE_tab[0],
                                   SIZE_OF_ARY(field_TPMS_PCRVALUE_tab));
    if (!ifapi_get_sub_object(jso, "pcr", &jso2)) {
        LOG_ERROR("Field \"pcr\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_UINT32_deserialize(jso2, &out->pcr);
    return_if_error(r, "Bad value for field \"pcr\".");

    if (!ifapi_get_sub_object(jso, "hashAlg", &jso2)) {
        LOG_ERROR("Field \"hashAlg\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPM2_ALG_ID_deserialize(jso2, &out->hashAlg);
    return_if_error(r, "Bad value for field \"hashAlg\".");
    if (!ifapi_get_sub_object(jso, "digest", &jso2)) {
        LOG_ERROR("Field \"digest\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPMU_HA_deserialize(out->hashAlg, jso2, &out->digest);
    return_if_error(r, "Bad value for field \"digest\".");

    LOG_TRACE("true");
    return TSS2_RC_SUCCESS;
}

/** Deserialize a TPML_PCRVALUES json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 */
TSS2_RC
ifapi_json_TPML_PCRVALUES_deserialize(json_object *jso,  TPML_PCRVALUES **out)
{
    json_object *jso2;
    TSS2_RC r;
    LOG_TRACE("call");
    return_if_null(out, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    json_type jso_type = json_object_get_type(jso);
    if (jso_type == json_type_array) {
        *out = calloc(1, sizeof(TPML_PCRVALUES) +
                      json_object_array_length(jso) * sizeof(TPMS_PCRVALUE));
        return_if_null(*out, "Out of memory.", TSS2_FAPI_RC_MEMORY);

        (*out)->count = json_object_array_length(jso);
        for (size_t i = 0; i < (*out)->count; i++) {
            jso2 = json_object_array_get_idx(jso, i);
            r = ifapi_json_TPMS_PCRVALUE_deserialize(jso2, &(*out)->pcrs[i]);
            return_if_error(r, "TPMS_PCRVALUE_deserialize");
        }
    } else {
        return_error(TSS2_FAPI_RC_BAD_VALUE, "BAD VALUE");
    }
    return TSS2_RC_SUCCESS;
}

static char *field_TPMS_POLICYPCR_tab[] = {
    "pcrs",
    "currentPCRs",
    "currentpcrs",
    "currentPCRandBanks",
    "currentpcrandbanks",
    "$schema",
    "type",
    "policyDigests",
    "nonceTPM"
};

/** Deserialize a TPMS_POLICYPCR json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 */
TSS2_RC
ifapi_json_TPMS_POLICYPCR_deserialize(json_object *jso,  TPMS_POLICYPCR *out)
{
    json_object *jso2;
    TSS2_RC r;
    size_t cond_cnt = 0; /**< counter for conditional fields */

    LOG_TRACE("call");
    return_if_null(out, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    ifapi_check_json_object_fields(jso, &field_TPMS_POLICYPCR_tab[0],
                                   SIZE_OF_ARY(field_TPMS_POLICYPCR_tab));
    if (ifapi_get_sub_object(jso, "pcrs", &jso2)) {
        cond_cnt++;
        r = ifapi_json_TPML_PCRVALUES_deserialize(jso2, &out->pcrs);
        return_if_error(r, "Bad value for field \"pcrs\".");
    } else {
        memset(&out->pcrs, 0, sizeof(TPML_PCRVALUES));
    }

    if (ifapi_get_sub_object(jso, "currentPCRs", &jso2)) {
        cond_cnt++;
        r = ifapi_json_TPMS_PCR_SELECT_deserialize(jso2, &out->currentPCRs);
        return_if_error(r, "Bad value for field \"currentPCRs\".");
    } else {
        memset(&out->currentPCRs, 0, sizeof(TPMS_PCR_SELECT));
    }

    if (ifapi_get_sub_object(jso, "currentPCRandBanks", &jso2)) {
        cond_cnt++;
        r = ifapi_json_TPML_PCR_SELECTION_deserialize(jso2, &out->currentPCRandBanks);
        return_if_error(r, "Bad value for field \"currentPCRandBanks\".");
    } else {
        memset(&out->currentPCRandBanks, 0, sizeof(TPML_PCR_SELECTION));
    }

    /* Check whether only one conditional is used. */
    if (cond_cnt != 1) {
        return_error(TSS2_FAPI_RC_BAD_VALUE,
                     "Exactly one conditional is allowed for policy PCR.");
    }

    LOG_TRACE("true");
    return TSS2_RC_SUCCESS;
}

static char *field_TPMS_POLICYAUTHORIZATION_tab[] = {
    "type",
    "key",
    "policyRef",
    "policyref",
    "signature",
    "$schema",
    "policyDigests",
    "nonceTPM",
    "hashAlg",
    "hashalg",
    "rsaScheme",
    "rsascheme",
    "keyPEMhashAlg",
    "keyPEM",
    "rsaScheme"
};

/** Deserialize a TPMS_POLICYAUTHORIZATION json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 */
TSS2_RC
ifapi_json_TPMS_POLICYAUTHORIZATION_deserialize(json_object *jso,
        TPMS_POLICYAUTHORIZATION *out)
{
    json_object *jso2;
    TSS2_RC r;
    LOG_TRACE("call");
    return_if_null(out, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    ifapi_check_json_object_fields(jso, &field_TPMS_POLICYAUTHORIZATION_tab[0],
                                   SIZE_OF_ARY(field_TPMS_POLICYAUTHORIZATION_tab));
    if (!ifapi_get_sub_object(jso, "type", &jso2)) {
        LOG_ERROR("Field \"type\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_char_deserialize(jso2, &out->type);
    return_if_error(r, "Bad value for field \"type\".");

    if (!ifapi_get_sub_object(jso, "key", &jso2)) {
        LOG_ERROR("Field \"key\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }

    if (strcmp(out->type,"tpm") == 0) {
        r = ifapi_json_TPMT_PUBLIC_deserialize(jso2, &out->key);
        return_if_error(r, "Bad value for field \"key\".");

        if (!ifapi_get_sub_object(jso, "signature", &jso2)) {
            LOG_ERROR("Field \"signature\" not found.");
            return TSS2_FAPI_RC_BAD_VALUE;
        }
        r = ifapi_json_TPMT_SIGNATURE_deserialize(jso2, &out->signature);
        return_if_error(r, "Bad value for field \"signature\".");
    } else if  (strcmp(out->type,"pem") == 0) {
        r = ifapi_json_char_deserialize(jso2, &out->keyPEM);
        return_if_error(r, "Bad value for field \"key\".");
        if (ifapi_get_sub_object(jso, "keyPEMhashAlg", &jso2)) {
            /* Allow value not defined in spec to achieve backward compatibility. */
            r = ifapi_json_TPMI_ALG_HASH_deserialize(jso2, &out->hashAlg);
            return_if_error(r, "Bad value for field \"keyPEMhashAlg\".");
        } else if (ifapi_get_sub_object(jso, "hashAlg", &jso2)) {
            r = ifapi_json_TPMI_ALG_HASH_deserialize(jso2, &out->hashAlg);
            return_if_error(r, "Bad value for field \"hashAlg\".");
        } else {
            out->hashAlg = TPM2_ALG_SHA256;
        }
        if (ifapi_get_sub_object(jso, "rsaScheme", &jso2)) {
            r = ifapi_json_TPMT_RSA_SCHEME_deserialize(jso2, &out->rsaScheme);
            return_if_error(r, "Bad value for field \"rsaScheme\".");
        } else {
            out->rsaScheme.scheme = TPM2_ALG_RSAPSS;
            out->rsaScheme.details.rsapss.hashAlg = out->hashAlg;
        }
        if (!ifapi_get_sub_object(jso, "signature", &jso2)) {
            LOG_ERROR("Field \"signature\" not found.");
            return TSS2_FAPI_RC_BAD_VALUE;
        }
        r = ifapi_json_UINT8_ARY_deserialize(jso2, &out->pemSignature);
        return_if_error(r, "Bad value for field \"signature\".");

    } else {
        LOG_ERROR("Bad value for field \"type\" (should be: tpm or pem).");
            return TSS2_FAPI_RC_BAD_VALUE;
    }

    if (ifapi_get_sub_object(jso, "policyRef", &jso2)) {
        r = ifapi_json_TPM2B_NONCE_deserialize(jso2, &out->policyRef);
        return_if_error(r, "Bad value for field \"policyRef\".");
    } else {
        memset(&out->policyRef, 0, sizeof(TPM2B_NONCE));
    }
    LOG_TRACE("true");
    return TSS2_RC_SUCCESS;
}

/** Deserialize a TPML_POLICYAUTHORIZATIONS json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 */
TSS2_RC
ifapi_json_TPML_POLICYAUTHORIZATIONS_deserialize(json_object *jso,
        TPML_POLICYAUTHORIZATIONS **out)
{
    json_object *jso2;
    TSS2_RC r = TSS2_RC_SUCCESS;
    LOG_TRACE("call");
    return_if_null(out, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    json_type jso_type = json_object_get_type(jso);
    if (jso_type == json_type_array) {
        *out = calloc(1, sizeof(TPML_POLICYAUTHORIZATIONS) +
                      json_object_array_length(jso) * sizeof(TPMS_POLICYAUTHORIZATION));
        return_if_null(*out, "Out of memory.", TSS2_FAPI_RC_MEMORY);

        (*out)->count = json_object_array_length(jso);
        for (size_t i = 0; i < (*out)->count; i++) {
            jso2 = json_object_array_get_idx(jso, i);
            r = ifapi_json_TPMS_POLICYAUTHORIZATION_deserialize(jso2,
                    &(*out)->authorizations[i]);
            return_if_error(r, "TPMS_POLICYAUTHORIZATION_deserialize");
        }
    } else {
        return_error(TSS2_FAPI_RC_BAD_VALUE, "BAD VALUE");
    }
    return TSS2_RC_SUCCESS;
}

static char *field_TPMS_POLICYBRANCH_tab[] = {
    "name",
    "description",
    "policy",
    "policyDigests",
    "policydigests",
    "$schema",
    "type",
    "nonceTPM"
};

/** Deserialize a TPMS_POLICYBRANCH json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 */
TSS2_RC
ifapi_json_TPMS_POLICYBRANCH_deserialize(json_object *jso,
        TPMS_POLICYBRANCH *out)
{
    json_object *jso2;
    TSS2_RC r;
    LOG_TRACE("call");
    return_if_null(out, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    ifapi_check_json_object_fields(jso, &field_TPMS_POLICYBRANCH_tab[0],
                                   SIZE_OF_ARY(field_TPMS_POLICYBRANCH_tab));
    if (!ifapi_get_sub_object(jso, "name", &jso2)) {
        LOG_ERROR("Field \"name\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_char_deserialize(jso2, &out->name);
    return_if_error(r, "Bad value for field \"name\".");

    if (!ifapi_get_sub_object(jso, "description", &jso2)) {
        LOG_ERROR("Field \"description\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_char_deserialize(jso2, &out->description);
    return_if_error(r, "Bad value for field \"description\".");

    if (!ifapi_get_sub_object(jso, "policy", &jso2)) {
        LOG_ERROR("Field \"policy\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPML_POLICYELEMENTS_deserialize(jso2, &out->policy);
    return_if_error(r, "Bad value for field \"policy\".");

    if (!ifapi_get_sub_object(jso, "policyDigests", &jso2)) {
        memset(&out->policyDigests, 0, sizeof(TPML_DIGEST_VALUES));
    } else {
        r = ifapi_json_TPML_DIGEST_VALUES_deserialize(jso2, &out->policyDigests);
        return_if_error(r, "Bad value for field \"policyDigests\".");

    }

    LOG_TRACE("true");
    return TSS2_RC_SUCCESS;
}

/** Deserialize a TPML_POLICYBRANCHES json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 */
TSS2_RC
ifapi_json_TPML_POLICYBRANCHES_deserialize(json_object *jso,
        TPML_POLICYBRANCHES **out)
{
    json_object *jso2;
    TSS2_RC r;
    LOG_TRACE("call");
    return_if_null(out, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    json_type jso_type = json_object_get_type(jso);
    if (jso_type == json_type_array) {
        *out = calloc(1, sizeof(TPML_POLICYBRANCHES) +
                      json_object_array_length(jso) * sizeof(TPMS_POLICYBRANCH));
        return_if_null(*out, "Out of memory.", TSS2_FAPI_RC_MEMORY);

        (*out)->count = json_object_array_length(jso);
        for (size_t i = 0; i < (*out)->count; i++) {
            jso2 = json_object_array_get_idx(jso, i);
            r = ifapi_json_TPMS_POLICYBRANCH_deserialize(jso2, &(*out)->authorizations[i]);
            return_if_error(r, "TPMS_POLICYBRANCH_deserialize");
        }
    } else {
        return_error(TSS2_FAPI_RC_BAD_VALUE, "BAD VALUE");
    }
    return TSS2_RC_SUCCESS;
}

static char *field_TPMS_POLICYOR_tab[] = {
    "branches",
    "$schema",
    "type",
    "policyDigests",
    "nonceTPM"
};

/** Deserialize a TPMS_POLICYOR json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 */
TSS2_RC
ifapi_json_TPMS_POLICYOR_deserialize(json_object *jso,  TPMS_POLICYOR *out)
{
    json_object *jso2;
    TSS2_RC r;
    LOG_TRACE("call");
    return_if_null(out, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    ifapi_check_json_object_fields(jso, &field_TPMS_POLICYOR_tab[0],
                                   SIZE_OF_ARY(field_TPMS_POLICYOR_tab));
    if (!ifapi_get_sub_object(jso, "branches", &jso2)) {
        LOG_ERROR("Field \"branches\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPML_POLICYBRANCHES_deserialize(jso2, &out->branches);
    return_if_error(r, "Bad value for field \"branches\".");
    LOG_TRACE("true");
    return TSS2_RC_SUCCESS;
}

/** Deserialize a TPMU_POLICYELEMENT json object.
 *
 * This functions expects the Bitfield to be encoded as unsigned int in host-endianess.
 * @param[in]  selector The type the policy element.
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 */
TSS2_RC
ifapi_json_TPMU_POLICYELEMENT_deserialize(
    UINT32 selector,
    json_object *jso,
    TPMU_POLICYELEMENT *out)
{
    LOG_TRACE("call");
    switch (selector) {
    case POLICYOR:
        return ifapi_json_TPMS_POLICYOR_deserialize(jso, &out->PolicyOr);
    case POLICYSIGNED:
        return ifapi_json_TPMS_POLICYSIGNED_deserialize(jso, &out->PolicySigned);
    case POLICYSECRET:
        return ifapi_json_TPMS_POLICYSECRET_deserialize(jso, &out->PolicySecret);
    case POLICYPCR:
        return ifapi_json_TPMS_POLICYPCR_deserialize(jso, &out->PolicyPCR);
    case POLICYLOCALITY:
        return ifapi_json_TPMS_POLICYLOCALITY_deserialize(jso, &out->PolicyLocality);
    case POLICYNV:
        return ifapi_json_TPMS_POLICYNV_deserialize(jso, &out->PolicyNV);
    case POLICYCOUNTERTIMER:
        return ifapi_json_TPMS_POLICYCOUNTERTIMER_deserialize(jso,
                &out->PolicyCounterTimer);
    case POLICYCOMMANDCODE:
        return ifapi_json_TPMS_POLICYCOMMANDCODE_deserialize(jso,
                &out->PolicyCommandCode);
    case POLICYPHYSICALPRESENCE:
        return ifapi_json_TPMS_POLICYPHYSICALPRESENCE_deserialize(jso,
                &out->PolicyPhysicalPresence);
    case POLICYCPHASH:
        return ifapi_json_TPMS_POLICYCPHASH_deserialize(jso, &out->PolicyCpHash);
    case POLICYNAMEHASH:
        return ifapi_json_TPMS_POLICYNAMEHASH_deserialize(jso, &out->PolicyNameHash);
    case POLICYDUPLICATIONSELECT:
        return ifapi_json_TPMS_POLICYDUPLICATIONSELECT_deserialize(jso,
                &out->PolicyDuplicationSelect);
    case POLICYAUTHORIZE:
        return ifapi_json_TPMS_POLICYAUTHORIZE_deserialize(jso, &out->PolicyAuthorize);
    case POLICYAUTHVALUE:
        return ifapi_json_TPMS_POLICYAUTHVALUE_deserialize(jso, &out->PolicyAuthValue);
    case POLICYPASSWORD:
        return ifapi_json_TPMS_POLICYPASSWORD_deserialize(jso, &out->PolicyPassword);
    case POLICYNVWRITTEN:
        return ifapi_json_TPMS_POLICYNVWRITTEN_deserialize(jso, &out->PolicyNvWritten);
    case POLICYTEMPLATE:
        return ifapi_json_TPMS_POLICYTEMPLATE_deserialize(jso, &out->PolicyTemplate);
    case POLICYAUTHORIZENV:
        return ifapi_json_TPMS_POLICYAUTHORIZENV_deserialize(jso,
                &out->PolicyAuthorizeNv);
    case POLICYACTION:
        return ifapi_json_TPMS_POLICYACTION_deserialize(jso, &out->PolicyAction);
    default:
        LOG_TRACE("false");
        return TSS2_FAPI_RC_BAD_VALUE;
    };
}

/** Deserialize a TPMT_POLICYELEMENT json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 */
TSS2_RC
ifapi_json_TPMT_POLICYELEMENT_deserialize(json_object *jso,
        TPMT_POLICYELEMENT *out)
{
    json_object *jso2;
    TSS2_RC r;
    LOG_TRACE("call");
    return_if_null(out, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    if (!ifapi_get_sub_object(jso, "type", &jso2)) {
        LOG_ERROR("Field \"type\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPMI_POLICYTYPE_deserialize(jso2, &out->type);
    return_if_error(r, "Bad value for field \"type\".");

    if (!ifapi_get_sub_object(jso, "policyDigests", &jso2)) {
        memset(&out->policyDigests, 0, sizeof(TPML_DIGEST_VALUES));
    } else {
        r = ifapi_json_TPML_DIGEST_VALUES_deserialize(jso2, &out->policyDigests);
        return_if_error(r, "Bad value for field \"policyDigests\".");

    }
    r = ifapi_json_TPMU_POLICYELEMENT_deserialize(out->type, jso, &out->element);
    return_if_error(r, "Bad value for field \"element\".");

    LOG_TRACE("true");
    return TSS2_RC_SUCCESS;
}

/** Deserialize a TPML_POLICYELEMENTS json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 */
TSS2_RC
ifapi_json_TPML_POLICYELEMENTS_deserialize(json_object *jso,
        TPML_POLICYELEMENTS **out)
{
    json_object *jso2;
    TSS2_RC r;
    LOG_TRACE("call");
    return_if_null(out, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    json_type jso_type = json_object_get_type(jso);
    if (jso_type == json_type_array) {
        *out = calloc(1, sizeof(TPML_POLICYELEMENTS) +
                      json_object_array_length(jso) * sizeof(TPMT_POLICYELEMENT));
        return_if_null(*out, "Out of memory.", TSS2_FAPI_RC_MEMORY);

        (*out)->count = json_object_array_length(jso);
        for (size_t i = 0; i < (*out)->count; i++) {
            jso2 = json_object_array_get_idx(jso, i);
            r = ifapi_json_TPMT_POLICYELEMENT_deserialize(jso2, &(*out)->elements[i]);
            return_if_error(r, "TPMT_POLICYELEMENT_deserialize");
        }
    } else {
        return_error(TSS2_FAPI_RC_BAD_VALUE, "BAD VALUE");
    }
    return TSS2_RC_SUCCESS;
}

static char *field_TPMS_POLICY_tab[] = {
    "description",
    "policyDigests",
    "policydigests",
    "policyAuthorizations",
    "policyauthorizations",
    "policy",
    "name",
    "$schema",
    "type",
    "nonceTPM"
};

/** Deserialize a TPMS_POLICY json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 */
TSS2_RC
ifapi_json_TPMS_POLICY_deserialize(json_object *jso,
        TPMS_POLICY *out)
{
    json_object *jso2;
    TSS2_RC r;
    LOG_TRACE("call");
    return_if_null(out, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    ifapi_check_json_object_fields(jso, &field_TPMS_POLICY_tab[0],
                                   SIZE_OF_ARY(field_TPMS_POLICY_tab));
    if (!ifapi_get_sub_object(jso, "description", &jso2)) {
        LOG_ERROR("No description for policy.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_char_deserialize(jso2, &out->description);
    return_if_error(r, "Bad value for field \"description\".");

    if (!ifapi_get_sub_object(jso, "policyDigests", &jso2)) {
        memset(&out->policyDigests, 0, sizeof(TPML_DIGEST_VALUES));
    } else {
        r = ifapi_json_TPML_DIGEST_VALUES_deserialize(jso2, &out->policyDigests);
        return_if_error(r, "Bad value for field \"policyDigests\".");

    }
    if (!ifapi_get_sub_object(jso, "policyAuthorizations", &jso2)) {
        memset(&out->policyAuthorizations, 0, sizeof(TPML_POLICYAUTHORIZATIONS));
    } else {
        r = ifapi_json_TPML_POLICYAUTHORIZATIONS_deserialize(jso2,
                &out->policyAuthorizations);
        return_if_error(r, "Bad value for field \"policyAuthorizations\".");

    }
    if (!ifapi_get_sub_object(jso, "policy", &jso2)) {
        LOG_ERROR("Field \"policy\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPML_POLICYELEMENTS_deserialize(jso2, &out->policy);
    return_if_error(r, "Bad value for field \"policy\".");
    LOG_TRACE("true");
    return TSS2_RC_SUCCESS;
}
