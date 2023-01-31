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
#include "ifapi_json_eventlog_deserialize.h"
#include "efi_event.h"
#include "tpm_json_deserialize.h"
#include "ifapi_json_deserialize.h"
#include "fapi_policy.h"
#include "ifapi_config.h"
#include "fapi_crypto.h"
#include "ifapi_ima_eventlog.h"
#include "ifapi_eventlog_system.h"
#include "ifapi_helpers.h"
#define LOGMODULE fapijson
#include "util/log.h"
#include "util/aux_util.h"
#include "tss2_mu.h"

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

/** Deserialize a character string.
 *
 * @param[in] jso json string object.
 * @param[out] out the pointer to the created string.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 */
TSS2_RC
ifapi_json_char_deserialize(
    json_object *jso,
    char **out)
{
    *out = strdup(json_object_get_string(jso));
    return_if_null(*out, "Out of memory.", TSS2_FAPI_RC_MEMORY);
    return TSS2_RC_SUCCESS;
}

/** Deserialize a IFAPI_KEY json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 */
TSS2_RC
ifapi_json_IFAPI_KEY_deserialize(json_object *jso,  IFAPI_KEY *out)
{
    json_object *jso2;
    TSS2_RC r;
    LOG_TRACE("call");
    return_if_null(out, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);


    if (!ifapi_get_sub_object(jso, "persistent_handle", &jso2)) {
        LOG_ERROR("Field \"persistent_handle\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_UINT32_deserialize(jso2, &out->persistent_handle);
    return_if_error(r, "Bad value for field \"persistent_handle\".");

    if (ifapi_get_sub_object(jso, "with_auth", &jso2)) {
        r = ifapi_json_TPMI_YES_NO_deserialize(jso2, &out->with_auth);
        return_if_error(r, "Bad value for field \"with_auth\".");

    } else {
        out->with_auth = TPM2_NO;
    }

    if (!ifapi_get_sub_object(jso, "public", &jso2)) {
        LOG_ERROR("Field \"public\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPM2B_PUBLIC_deserialize(jso2, &out->public);
    return_if_error(r, "Bad value for field \"public\".");

    if (!ifapi_get_sub_object(jso, "serialization", &jso2)) {
        LOG_ERROR("Field \"serialization\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_UINT8_ARY_deserialize(jso2, &out->serialization);
    return_if_error(r, "Bad value for field \"serialization\".");

    if (!ifapi_get_sub_object(jso, "private", &jso2)) {
        memset(&out->private, 0, sizeof(UINT8_ARY));
    } else {
        r = ifapi_json_UINT8_ARY_deserialize(jso2, &out->private);
        return_if_error(r, "Bad value for field \"private\".");
    }

    if (!ifapi_get_sub_object(jso, "appData", &jso2)) {
        memset(&out->appData, 0, sizeof(UINT8_ARY));
    } else {
        r = ifapi_json_UINT8_ARY_deserialize(jso2, &out->appData);
        return_if_error(r, "Bad value for field \"appData\".");
    }

    if (!ifapi_get_sub_object(jso, "policyInstance", &jso2)) {
        LOG_ERROR("Field \"policyInstance\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_char_deserialize(jso2, &out->policyInstance);
    return_if_error(r, "Bad value for field \"policyInstance\".");

    if (ifapi_get_sub_object(jso, "creationData", &jso2)) {
        r = ifapi_json_TPM2B_CREATION_DATA_deserialize(jso2, &out->creationData);
        return_if_error(r, "Bad value for field \"creationData\".");

    } else {
        memset(&out->creationData, 0, sizeof(TPM2B_CREATION_DATA));
    }

    if (ifapi_get_sub_object(jso, "creationHash", &jso2)) {
        r = ifapi_json_TPM2B_DIGEST_deserialize(jso2, &out->creationHash);
        return_if_error(r, "Bad value for field \"creationHash\".");

    } else {
        memset(&out->creationHash, 0, sizeof(TPM2B_DIGEST));
    }

    if (ifapi_get_sub_object(jso, "creationTicket", &jso2)) {
        r = ifapi_json_TPMT_TK_CREATION_deserialize(jso2, &out->creationTicket);
        return_if_error(r, "Bad value for field \"creationTicket\".");

    } else {
        memset(&out->creationTicket, 0, sizeof(TPMT_TK_CREATION));
    }
    if (!ifapi_get_sub_object(jso, "description", &jso2)) {
        LOG_ERROR("Field \"description\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_char_deserialize(jso2, &out->description);
    return_if_error(r, "Bad value for field \"description\".");

    if (!ifapi_get_sub_object(jso, "certificate", &jso2)) {
        LOG_ERROR("Field \"certificate\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_char_deserialize(jso2, &out->certificate);
    return_if_error(r, "Bad value for field \"certificate\".");

    if (out->public.publicArea.type != TPM2_ALG_KEYEDHASH) {
         /* Keyed hash objects to not need a signing scheme. */
        if (!ifapi_get_sub_object(jso, "signing_scheme", &jso2)) {
            LOG_ERROR("Field \"signing_scheme\" not found.");
            return TSS2_FAPI_RC_BAD_VALUE;
        }
        r = ifapi_json_TPMT_SIG_SCHEME_deserialize(jso2, &out->signing_scheme);
        return_if_error(r, "Bad value for field \"signing_scheme\".");
    }

    if (!ifapi_get_sub_object(jso, "name", &jso2)) {
        LOG_ERROR("Field \"name\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPM2B_NAME_deserialize(jso2, &out->name);
    return_if_error(r, "Bad value for field \"name\".");

    if (ifapi_get_sub_object(jso, "reset_count", &jso2)) {
        r = ifapi_json_UINT32_deserialize(jso2, &out->reset_count);
        return_if_error(r, "Bad value for field \"reset_count\".");
    } else {
        out->reset_count = 0;
    }

    if (ifapi_get_sub_object(jso, "delete_prohibited", &jso2)) {
        r = ifapi_json_TPMI_YES_NO_deserialize(jso2, &out->delete_prohibited);
        return_if_error(r, "Bad value for field \"delete_prohibited\".");

    } else {
        out->delete_prohibited = TPM2_NO;
    }

    if (ifapi_get_sub_object(jso, "ek_profile", &jso2)) {
        r = ifapi_json_TPMI_YES_NO_deserialize(jso2, &out->ek_profile);
        return_if_error(r, "Bad value for field \"ek_profile\".");

    } else {
        out->ek_profile = TPM2_NO;
    }

    if (ifapi_get_sub_object(jso, "nonce", &jso2)) {
        r = ifapi_json_TPM2B_DIGEST_deserialize(jso2, &out->nonce);
        return_if_error(r, "Bad value for field \"nonce\".");

    } else {
        memset(&out->nonce, 0, sizeof(TPM2B_DIGEST));
    }



    LOG_TRACE("true");
    return TSS2_RC_SUCCESS;
}

static char *field_import_IFAPI_KEY_tab[] = {
    "noauth",
    "public",
    "private",
    "$schema"
};

/** Deserialize a import data to create a IFAPI_KEY json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 */
TSS2_RC
ifapi_json_import_IFAPI_KEY_deserialize(json_object *jso,  IFAPI_KEY *out)
{
    json_object *jso2;
    TSS2_RC r;
    UINT8_ARY public_blob = { .size = 0, .buffer = NULL };
    UINT8_ARY private_blob = { .size = 0, .buffer = NULL };
    TPM2B_PRIVATE private;
    size_t offset = 0;
    TPMI_YES_NO noauth;

    LOG_TRACE("call");
    return_if_null(out, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    memset(out, 0, sizeof(IFAPI_KEY));

    ifapi_check_json_object_fields(jso, &field_import_IFAPI_KEY_tab[0],
                                   SIZE_OF_ARY(field_import_IFAPI_KEY_tab));
    if (ifapi_get_sub_object(jso, "noauth", &jso2)) {
        r = ifapi_json_TPMI_YES_NO_deserialize(jso2, &noauth);
        return_if_error(r, "BAD VALUE");

        if (noauth == TPM2_YES)
            out->with_auth = TPM2_NO;
        else
            out->with_auth = TPM2_YES;

    } else {
        out->with_auth = TPM2_YES;
    }

    if (!ifapi_get_sub_object(jso, "public", &jso2)) {
        LOG_ERROR("Field \"public\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_UINT8_ARY_deserialize(jso2, &public_blob);
    return_if_error(r, "BAD VALUE");

    /* Get structure with public data from binary blob. */
    r = Tss2_MU_TPM2B_PUBLIC_Unmarshal(public_blob.buffer, public_blob.size,
                                       &offset, &out->public);
    return_if_error(r, "Invalid public data.");

    SAFE_FREE(public_blob.buffer);

    if (!ifapi_get_sub_object(jso, "private", &jso2)) {
        memset(&out->private, 0, sizeof(UINT8_ARY));
    } else {
        /* Deserialize complete binary blob. */
        r = ifapi_json_UINT8_ARY_deserialize(jso2, &private_blob);
        return_if_error(r, "BAD VALUE");
        offset = 0;

        /* Extract private data from blob with size. */
        r = Tss2_MU_TPM2B_PRIVATE_Unmarshal(private_blob.buffer, private_blob.size,
                                            &offset, &private);
        goto_if_error(r, "BAD VALUE", error_cleanup);

        SAFE_FREE(private_blob.buffer);

        /* Copy private data into object structure. */
        out->private.size = private.size;
        out->private.buffer = malloc(private.size);
        goto_if_null2(out->private.buffer, "Out of memory", r, TSS2_FAPI_RC_MEMORY,
                      error_cleanup);

        memcpy(out->private.buffer, &private.buffer[0], private.size);
    }

    strdup_check(out->policyInstance, "", r, error_cleanup);
    strdup_check(out->description, "", r, error_cleanup);
    strdup_check(out->certificate, "", r, error_cleanup);

    LOG_TRACE("true");
    return TSS2_RC_SUCCESS;

 error_cleanup:
    SAFE_FREE(public_blob.buffer);
    SAFE_FREE(private_blob.buffer);
    return r;
}


/** Deserialize a IFAPI_EXT_PUB_KEY json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 */
TSS2_RC
ifapi_json_IFAPI_EXT_PUB_KEY_deserialize(json_object *jso,
        IFAPI_EXT_PUB_KEY *out)
{
    json_object *jso2;
    TSS2_RC r;
    LOG_TRACE("call");
    return_if_null(out, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);


    if (!ifapi_get_sub_object(jso, "pem_ext_public", &jso2)) {
        LOG_ERROR("Field \"pem_ext_public\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_char_deserialize(jso2, &out->pem_ext_public);
    return_if_error(r, "Bad value for field \"pem_ext_public\".");

    if (ifapi_get_sub_object(jso, "certificate", &jso2)) {
        r = ifapi_json_char_deserialize(jso2, &out->certificate);
        return_if_error(r, "Bad value for field \"certificate\".");
    } else {
        out->certificate = NULL;
    }

    if (ifapi_get_sub_object(jso, "public", &jso2)) {
        r = ifapi_json_TPM2B_PUBLIC_deserialize(jso2, &out->public);
        return_if_error(r, "Bad value for field \"public\".");

    } else {
        memset(&out->public, 0, sizeof(TPM2B_PUBLIC));
    }
    LOG_TRACE("true");
    return TSS2_RC_SUCCESS;
}

/** Deserialize a IFAPI_NV json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 */
TSS2_RC
ifapi_json_IFAPI_NV_deserialize(json_object *jso,  IFAPI_NV *out)
{
    json_object *jso2;
    TSS2_RC r;
    LOG_TRACE("call");
    return_if_null(out, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    if (!ifapi_get_sub_object(jso, "appData", &jso2)) {
        memset(&out->appData, 0, sizeof(UINT8_ARY));
    } else {
        r = ifapi_json_UINT8_ARY_deserialize(jso2, &out->appData);
        return_if_error(r, "Bad value for field \"appData\".");
    }

    if (ifapi_get_sub_object(jso, "with_auth", &jso2)) {
        r = ifapi_json_TPMI_YES_NO_deserialize(jso2, &out->with_auth);
        return_if_error(r, "Bad value for field \"with_auth\".");

    } else {
        out->with_auth = TPM2_NO;
    }

    if (!ifapi_get_sub_object(jso, "public", &jso2)) {
        LOG_ERROR("Field \"public\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPM2B_NV_PUBLIC_deserialize(jso2, &out->public);
    return_if_error(r, "Bad value for field \"public\".");

    if (!ifapi_get_sub_object(jso, "serialization", &jso2)) {
        LOG_ERROR("Field \"serialization\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_UINT8_ARY_deserialize(jso2, &out->serialization);
    return_if_error(r, "Bad value for field \"serialization\".");

    if (!ifapi_get_sub_object(jso, "hierarchy", &jso2)) {
        LOG_ERROR("Field \"hierarchy\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_UINT32_deserialize(jso2, &out->hierarchy);
    return_if_error(r, "Bad value for field \"hierarchy\".");

    if (!ifapi_get_sub_object(jso, "policyInstance", &jso2)) {
        LOG_ERROR("Field \"policyInstance\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_char_deserialize(jso2, &out->policyInstance);
    return_if_error(r, "Bad value for field \"policyInstance\".");

    if (!ifapi_get_sub_object(jso, "description", &jso2)) {
        LOG_ERROR("Field \"description\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_char_deserialize(jso2, &out->description);
    return_if_error(r, "Bad value for field \"description\".");

    return_if_error(r, "BAD VALUE");
    if (ifapi_get_sub_object(jso, "event_log", &jso2)) {
        r = ifapi_json_char_deserialize(jso2, &out->event_log);
        return_if_error(r, "Bad value for field \"event_log\".");

    } else {
        out->event_log = NULL;
    }
    LOG_TRACE("true");
    return TSS2_RC_SUCCESS;
}

/** Deserialize a IFAPI_NV json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 */
TSS2_RC
ifapi_json_IFAPI_HIERARCHY_deserialize(json_object *jso,  IFAPI_HIERARCHY *out)
{
    json_object *jso2;
    TSS2_RC r;
    LOG_TRACE("call");
    return_if_null(out, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    if (ifapi_get_sub_object(jso, "with_auth", &jso2)) {
        r = ifapi_json_TPMI_YES_NO_deserialize(jso2, &out->with_auth);
        return_if_error(r, "Bad value for field \"with_auth\".");

    } else {
        out->with_auth = TPM2_NO;
    }

    if (!ifapi_get_sub_object(jso, "authPolicy", &jso2)) {
        LOG_ERROR("Field \"authPolicy\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPM2B_DIGEST_deserialize(jso2, &out->authPolicy);
    return_if_error(r, "Bad value for field \"authPolicy\".");

    if (!ifapi_get_sub_object(jso, "description", &jso2)) {
        LOG_ERROR("Field \"description\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_char_deserialize(jso2, &out->description);
    return_if_error(r, "Bad value for field \"description\".");

    if (ifapi_get_sub_object(jso, "esysHandle", &jso2)) {
        r = ifapi_json_UINT32_deserialize(jso2, &out->esysHandle);
        return_if_error(r, "Bad value for field \"esysHandle\".");
    } else {
        out->esysHandle = ESYS_TR_RH_OWNER;
    }

    LOG_TRACE("true");
    return TSS2_RC_SUCCESS;
}

static char *field_FAPI_QUOTE_INFO_tab[] = {
    "sig_scheme",
    "attest",
    "$schema"
};

/** Deserialize a FAPI_QUOTE_INFO json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_FAPI_QUOTE_INFO_deserialize(json_object *jso,  FAPI_QUOTE_INFO *out)
{
    json_object *jso2;
    TSS2_RC r;
    LOG_TRACE("call");
    return_if_null(out, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);


    ifapi_check_json_object_fields(jso, &field_FAPI_QUOTE_INFO_tab[0],
                                   SIZE_OF_ARY(field_FAPI_QUOTE_INFO_tab));
    if (!ifapi_get_sub_object(jso, "sig_scheme", &jso2)) {
        LOG_ERROR("Field \"sig_scheme\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPMT_SIG_SCHEME_deserialize(jso2, &out->sig_scheme);
    return_if_error(r, "Bad value for field \"sig_scheme\".");

    if (!ifapi_get_sub_object(jso, "attest", &jso2)) {
        LOG_ERROR("Field \"attest\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPMS_ATTEST_deserialize(jso2, &out->attest);
    return_if_error(r, "Bad value for field \"attest\".");
    LOG_TRACE("true");
    return TSS2_RC_SUCCESS;
}

/** Deserialize a IFAPI_DUPLICATE json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 */
TSS2_RC
ifapi_json_IFAPI_DUPLICATE_deserialize(json_object *jso, IFAPI_DUPLICATE *out)
{
    json_object *jso2;
    TSS2_RC r;
    LOG_TRACE("call");
    return_if_null(out, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    if (!ifapi_get_sub_object(jso, "duplicate", &jso2)) {
        LOG_ERROR("Field \"duplicate\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }

    r = ifapi_json_TPM2B_PRIVATE_deserialize(jso2, &out->duplicate);
    return_if_error(r, "Bad value for field \"duplicate\".");

    if (!ifapi_get_sub_object(jso, "encrypted_seed", &jso2)) {
        LOG_ERROR("Field \"encrypted_seed\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPM2B_ENCRYPTED_SECRET_deserialize(jso2, &out->encrypted_seed);
    return_if_error(r, "Bad value for field \"encrypted_seed\".");

    if (ifapi_get_sub_object(jso, "certificate", &jso2)) {
        r = ifapi_json_char_deserialize(jso2, &out->certificate);
        return_if_error(r, "Bad value for field \"certificate\".");

    } else {
        out->certificate = NULL;
    }

    if (!ifapi_get_sub_object(jso, "public", &jso2)) {
        LOG_ERROR("Field \"public\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }

    r = ifapi_json_TPM2B_PUBLIC_deserialize(jso2, &out->public);
    return_if_error(r, "Bad value for field \"public\".");
    if (!ifapi_get_sub_object(jso, "public_parent", &jso2)) {
        LOG_ERROR("Field \"public_parent\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }

    r = ifapi_json_TPM2B_PUBLIC_deserialize(jso2, &out->public_parent);
    return_if_error(r, "Bad value for field \"public_parent\".");

    if (ifapi_get_sub_object(jso, "policy", &jso2)) {
        out->policy = calloc(1, sizeof(TPMS_POLICY));
        goto_if_null2(out->policy, "Out of memory.", r, TSS2_FAPI_RC_MEMORY,
                      error_cleanup);

        r = ifapi_json_TPMS_POLICY_deserialize(jso2, out->policy);
        goto_if_error(r, "Deserialize policy.", error_cleanup);
    } else {
        out->policy = NULL;
    }

    return TSS2_RC_SUCCESS;

error_cleanup:
    SAFE_FREE(out->policy);
    return r;
}

/**  Deserialize a IFAPI_OBJECT_TYPE_CONSTANT json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 */
TSS2_RC
ifapi_json_IFAPI_OBJECT_TYPE_CONSTANT_deserialize(json_object *jso,
        IFAPI_OBJECT_TYPE_CONSTANT *out)
{
    LOG_TRACE("call");
    const char *token = json_object_get_string(jso);
    int64_t i64;
    if (get_number(token, &i64)) {
        *out = (IFAPI_OBJECT_TYPE_CONSTANT) i64;
        if ((int64_t)*out != i64) {
            LOG_ERROR("Bad value");
            return TSS2_FAPI_RC_BAD_VALUE;
        }
        return TSS2_RC_SUCCESS;
    } else {
        LOG_ERROR("Bad value");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
}

/** Deserialize a IFAPI_OBJECT json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE if an internal error occurred.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 */
TSS2_RC
ifapi_json_IFAPI_OBJECT_deserialize(json_object *jso, IFAPI_OBJECT *out)
{
    json_object *jso2;
    TSS2_RC r;
    LOG_TRACE("call");
    return_if_null(out, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    if (!ifapi_get_sub_object(jso, "objectType", &jso2)) {
        LOG_ERROR("Field \"objectType\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }

    r = ifapi_json_IFAPI_OBJECT_TYPE_CONSTANT_deserialize(jso2, &out->objectType);
    return_if_error(r, "Bad value for field \"objectType\".");

    switch (out->objectType) {
    case IFAPI_NV_OBJ:
        r = ifapi_json_IFAPI_NV_deserialize(jso, &out->misc.nv);
        return_if_error(r, "Bad value for NV object.");
        break;

    case IFAPI_DUPLICATE_OBJ:
        r = ifapi_json_IFAPI_DUPLICATE_deserialize(jso, &out->misc.key_tree);
        return_if_error(r, "Bad value for key tree");

        break;

    case IFAPI_EXT_PUB_KEY_OBJ:
        r = ifapi_json_IFAPI_EXT_PUB_KEY_deserialize(jso, &out->misc.ext_pub_key);
        return_if_error(r, "Bad value for external public key.");

        break;

    case IFAPI_HIERARCHY_OBJ:
        r = ifapi_json_IFAPI_HIERARCHY_deserialize(jso, &out->misc.hierarchy);
        return_if_error(r, "Bad value for hierarchy.");

        r = ifapi_set_name_hierarchy_object(out);
        return_if_error(r, "Bad hierarchy.");

        break;
    case IFAPI_KEY_OBJ:
        r = ifapi_json_IFAPI_KEY_deserialize(jso, &out->misc.key);
        return_if_error(r, "Bad value for key.");

        break;
    default:
        goto_error(r, TSS2_FAPI_RC_GENERAL_FAILURE, "Invalid call deserialize",
                   cleanup);
    }

    if (ifapi_get_sub_object(jso, "system", &jso2)) {
        r = ifapi_json_TPMI_YES_NO_deserialize(jso2, &out->system);
        return_if_error(r, "Bad value for field \"system\".");

    } else {
        out->system = TPM2_NO;
    }

    if (ifapi_get_sub_object(jso, "policy", &jso2)) {
        out->policy = calloc(1, sizeof(TPMS_POLICY));
        goto_if_null2(out->policy, "Out of memory.", r, TSS2_FAPI_RC_MEMORY,
                      cleanup);

        r = ifapi_json_TPMS_POLICY_deserialize(jso2, out->policy);
        goto_if_error(r, "Deserialize policy.", cleanup);
    } else {
        out->policy = NULL;
    }

    return TSS2_RC_SUCCESS;

cleanup:
    SAFE_FREE(out->policy);
    return r;
}

/** Deserialize a IFAPI_EVENT_TYPE json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 */
TSS2_RC
ifapi_json_IFAPI_EVENT_TYPE_deserialize(json_object *jso, IFAPI_EVENT_TYPE *out)
{
    LOG_TRACE("call");
    return ifapi_json_IFAPI_EVENT_TYPE_deserialize_txt(jso, out);
}

typedef struct {
    IFAPI_EVENT_TYPE in;
    char *name;
} IFAPI_IFAPI_EVENT_TYPE_ASSIGN;

static IFAPI_IFAPI_EVENT_TYPE_ASSIGN deserialize_IFAPI_EVENT_TYPE_tab[] = {
    { IFAPI_IMA_EVENT_TAG, "ima_template" },
    { IFAPI_TSS_EVENT_TAG, "tss2" },
    { IFAPI_PC_CLIENT, "pcclient_std" },
    { IFAPI_CEL_TAG, "cel" }
};

/**  Deserialize a json object of type IFAPI_EVENT_TYPE.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 */
TSS2_RC
ifapi_json_IFAPI_EVENT_TYPE_deserialize_txt(json_object *jso,
        IFAPI_EVENT_TYPE *out)
{
    LOG_TRACE("call");
    const char *token = json_object_get_string(jso);
    int64_t i64;
    if (get_number(token, &i64)) {
        *out = (IFAPI_EVENT_TYPE) i64;
        if ((int64_t)*out != i64) {
            LOG_ERROR("Bad value");
            return TSS2_FAPI_RC_BAD_VALUE;
        }
        return TSS2_RC_SUCCESS;

    } else {
        int itoken = get_token_start_idx(token);
        size_t i;
        size_t n = sizeof(deserialize_IFAPI_EVENT_TYPE_tab) /
                   sizeof(deserialize_IFAPI_EVENT_TYPE_tab[0]);
        size_t size = strlen(token) - itoken;
        for (i = 0; i < n; i++) {
            if (strncasecmp(&token[itoken],
                            &deserialize_IFAPI_EVENT_TYPE_tab[i].name[0],
                            size) == 0) {
                *out = deserialize_IFAPI_EVENT_TYPE_tab[i].in;
                return TSS2_RC_SUCCESS;
            }
        }
        return_error(TSS2_FAPI_RC_BAD_VALUE, "Undefined constant.");
    }

}

static char *field_IFAPI_TSS_EVENT_tab[] = {
    "data",
    "event",
    "$schema"
};

/** Deserialize a IFAPI_TSS_EVENT json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 */
TSS2_RC
ifapi_json_IFAPI_TSS_EVENT_deserialize(json_object *jso,
                                       IFAPI_TSS_EVENT *out)
{
    json_object *jso2;
    TSS2_RC r;
    LOG_TRACE("call");
    return_if_null(out, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    ifapi_check_json_object_fields(jso, &field_IFAPI_TSS_EVENT_tab[0],
                                   SIZE_OF_ARY(field_IFAPI_TSS_EVENT_tab));
    if (!ifapi_get_sub_object(jso, "data", &jso2)) {
        LOG_ERROR("Field \"data\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPM2B_EVENT_deserialize(jso2, &out->data);
    return_if_error(r, "Bad value for field \"data\".");

    if (!ifapi_get_sub_object(jso, "event", &jso2)) {
        out->event = NULL;
    } else {
        /* out->event is a special case. It can be an arbitrary
           JSON object. Since FAPI does not access its internals
           we just store its string represenation here. */
        out->event = strdup(json_object_to_json_string_ext(jso2,
                                JSON_C_TO_STRING_PRETTY));
        return_if_null(out->event, "OOM", TSS2_FAPI_RC_MEMORY);
    }
    LOG_TRACE("true");
    return TSS2_RC_SUCCESS;
}

/** Deserialize a IFAPI_EVENT_UNION json object.
 *
 * This functions expects the Bitfield to be encoded as unsigned int in host-endianess.
 * @param[in] jso the json object to be deserialized.
 * @param[in] selector the event type.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 */
TSS2_RC
ifapi_json_IFAPI_EVENT_UNION_deserialize(
    UINT32 selector,
    json_object *jso,
    IFAPI_EVENT_UNION *out,
    bool *verify)
{
    TSS2_RC r;

    LOG_TRACE("call");
    /* The default is to verify the digest with the event data. */
    *verify = true;
    switch (selector) {
    case IFAPI_TSS_EVENT_TAG:
        return ifapi_json_IFAPI_TSS_EVENT_deserialize(jso, &out->tss_event);
    case IFAPI_IMA_EVENT_TAG:
        return ifapi_json_IFAPI_IMA_EVENT_deserialize(jso, &out->ima_event);
    case IFAPI_PC_CLIENT:
        r  = ifapi_json_IFAPI_FIRMWARE_EVENT_deserialize(jso, &out->firmware_event, verify);
        return_if_error(r, "Deserialize firmware event");
        return TSS2_RC_SUCCESS;
    case IFAPI_CEL_TAG:
        r  = ifapi_json_TPMS_EVENT_CELMGT_deserialize(jso, &out->cel_event);
        return_if_error(r, "Deserialize CEL event");
        return TSS2_RC_SUCCESS;
     default:
        LOG_TRACE("false");
        return TSS2_FAPI_RC_BAD_VALUE;
    };
}


/** Compute the event hash from event content.
 *
 * The event digest for a certain hash alg determined by the passed
 * crypto context is computed.
 *
 * @param[in] cryptoContext The event with the content to be hashed.
 * @param[in] event The event with the content to be hased.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the event is not valid,
 */
static TSS2_RC
get_event_hash(
    IFAPI_CRYPTO_CONTEXT_BLOB *cryptoContext,
    IFAPI_EVENT *event)
{
    TSS2_RC r;

    LOG_TRACE("call");
    switch (event->content_type) {
    case IFAPI_TSS_EVENT_TAG:
        HASH_UPDATE_BUFFER(cryptoContext, &event->content.tss_event.data.buffer[0],
                           event->content.tss_event.data.size, r, error_cleanup);
        return TSS2_RC_SUCCESS;
    case IFAPI_IMA_EVENT_TAG:
        HASH_UPDATE_BUFFER(cryptoContext, &event->content.ima_event.template_value.buffer[0],
                           event->content.ima_event.template_value.size, r, error_cleanup);
        return TSS2_RC_SUCCESS;
    case IFAPI_PC_CLIENT:
        HASH_UPDATE_BUFFER(cryptoContext, &event->content.firmware_event.data.buffer[0],
                           event->content.firmware_event.data.size, r, error_cleanup);
        return TSS2_RC_SUCCESS;
     default:
        LOG_TRACE("false");
        return TSS2_FAPI_RC_BAD_VALUE;
    };
 error_cleanup:
    return r;
}

/** Check whether the digest of an event matches the event content.
 *
 * If an IMA event was invalidated (Both the event digest and the file digest
 * consist of zeros) the event digest will be set to 0xff in the size of
 * the event digest.
 *
 * This functions expects the Bitfield to be encoded as unsigned int in host-endianess.
 * @param[in] event  The event with the digest list and the event content.
 * @param[in] error_handling an enum to determine the action if the digest
 *            is not appropriate for the event content.
 *            (DIGEST_CHECK_ERROR, DIGEST_CHECK_WARNING, DO_NOT_CHECK_DIGEST).
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the event is not valid or the digest is
 *         not valid.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 */
static TSS2_RC
check_event_digest(
    IFAPI_EVENT *event,
    enum IFAPI_EVENT_ERROR_HANDLING error_handling)
{
    TSS2_RC r;
    IFAPI_CRYPTO_CONTEXT_BLOB *cryptoContext = NULL;
    size_t i, hash_size;
    uint8_t data_hash[sizeof(TPMU_HA)];
    bool ff_digest;

    LOG_TRACE("Verify event for PCR %u", event->pcr);

    if (event->content_type == IFAPI_IMA_EVENT_TAG) {
        /* Check whether IMA digest was invalidated. */
        ff_digest = true;
        for (i = 0; i < TPM2_SHA1_DIGEST_SIZE; i++) {
            if (event->digests.digests[0].digest.sha512[i] < 0xff) {
                ff_digest = false;
                break;
            }
        }
        if (ff_digest) {
            char *name;
            r = ifapi_get_ima_eventname(&event->content.ima_event, &name);
            goto_if_error(r, "Get eventname.", error_cleanup);

            LOG_WARNING("IMA event was invalidated: %s", name);
            return TSS2_RC_SUCCESS;
        }
    }

    for (i = 0; i < event->digests.count; i++) {
        if (!(hash_size = ifapi_hash_get_digest_size(event->digests.digests[i].hashAlg))) {
            goto_error(r, TSS2_FAPI_RC_BAD_VALUE,
                       "Unsupported hash algorithm (%" PRIu16 ")", error_cleanup,
                       event->digests.digests[i].hashAlg);
        }
        r = ifapi_crypto_hash_start(&cryptoContext, event->digests.digests[i].hashAlg);
        return_if_error(r, "crypto hash start");

        r = get_event_hash(cryptoContext, event);
        goto_if_error(r, "Get digest event hash.",  error_cleanup);

        r = ifapi_crypto_hash_finish(&cryptoContext,
                                     &data_hash[0], &hash_size);
        return_if_error(r, "crypto hash finish");

        if (memcmp(&event->digests.digests[i].digest.sha512[0], &data_hash[0], hash_size) != 0) {
            if (error_handling == DIGEST_CHECK_ERROR) {
                goto_error(r, TSS2_FAPI_RC_BAD_VALUE,
                           "Digest verification",  error_cleanup);
            } else {
                LOG_WARNING("Failure in digest verification.");
            }
        }
    }
    return TSS2_RC_SUCCESS;

error_cleanup:
    return r;
}

static char *field_IFAPI_EVENT_tab[] = {
    "recnum",
    "pcr",
    "digests",
    CONTENT_TYPE,
    CONTENT,
    "$schema"
};

/** Deserialize a IFAPI_EVENT json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[in]  error switch whether an error will be generated if the digest
 *             verification fails. If set to false only a warning will be
 *             generated.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 */
TSS2_RC
ifapi_json_IFAPI_EVENT_deserialize(
    json_object *jso,
    IFAPI_EVENT *out,
    enum IFAPI_EVENT_ERROR_HANDLING error_handling)
{
    json_object *jso2;
    TSS2_RC r = TSS2_RC_SUCCESS;;
    bool verify;

    LOG_TRACE("call");
    memset(out, 0, sizeof(IFAPI_EVENT));
    return_if_null(out, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    ifapi_check_json_object_fields(jso, &field_IFAPI_EVENT_tab[0],
                                   SIZE_OF_ARY(field_IFAPI_EVENT_tab));
    if (ifapi_get_sub_object(jso, "recnum", &jso2)) {
        r = ifapi_json_UINT32_deserialize(jso2, &out->recnum);
        return_if_error(r, "BAD VALUE");
    } else {
        out->recnum = 0;
    }

    if (!ifapi_get_sub_object(jso, "pcr", &jso2)) {
        LOG_ERROR("Field \"pcr\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPM2_HANDLE_deserialize(jso2, &out->pcr);
    return_if_error(r, "Bad value for field \"pcr\".");

    if (!ifapi_get_sub_object(jso, "digests", &jso2)) {
        LOG_ERROR("Field \"digests\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPML_DIGEST_VALUES_deserialize(jso2, &out->digests);
    return_if_error(r, "Bad value for field \"digests\".");

    if (!ifapi_get_sub_object(jso, CONTENT_TYPE, &jso2)) {
        LOG_ERROR("Field \"content_type\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_IFAPI_EVENT_TYPE_deserialize(jso2, &out->content_type);
    return_if_error(r, "Bad value for field \"content_type\".");

    if (!ifapi_get_sub_object(jso, CONTENT, &jso2)) {
        LOG_ERROR("Field \"content\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_IFAPI_EVENT_UNION_deserialize(out->content_type, jso2,
                                                 &out->content,
                                                 &verify);
    goto_if_error(r,"Bad value for field \"content\"." , cleanup);

    if (verify && error_handling != DO_NOT_CHECK_DIGEST) {
        r = check_event_digest(out, error_handling);
        goto_if_error(r, "Check event digest", cleanup);
    }
    return TSS2_RC_SUCCESS;

 cleanup:
    if (out->content_type == IFAPI_IMA_EVENT_TAG) {
        SAFE_FREE(out->content.ima_event.template_value.buffer);
    } else if (out->content_type == IFAPI_PC_CLIENT) {
         SAFE_FREE(out->content.firmware_event.data.buffer);
    }
    return r;
}

static char *field_TPMS_CEL_VERSION_tab[] = {
    "major",
    "minor",
    "$schema"
};

/** Deserialize a TPMS_CEL_VERSION variable.
 *
 * @param[in]  jso json object to be deserialized.
 * @param[out] out the deserialized object.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 */
TSS2_RC
ifapi_json_TPMS_CEL_VERSION_deserialize(json_object *jso,
        TPMS_CEL_VERSION *out)
{
    LOG_TRACE("call");
    json_object *jso2;
    TSS2_RC r;

    memset(out, 0, sizeof(TPMS_CEL_VERSION));
    ifapi_check_json_object_fields(jso, &field_TPMS_CEL_VERSION_tab[0],
                                   SIZE_OF_ARY(field_TPMS_CEL_VERSION_tab));
    if (!ifapi_get_sub_object(jso, "major", &jso2)) {
        LOG_ERROR("Field \"major\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_UINT16_deserialize(jso2, &out->major);
    return_if_error(r, "Bad value for field \"major\".");

    if (!ifapi_get_sub_object(jso, "minor", &jso2)) {
        LOG_ERROR("Field \"minor\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    return ifapi_json_UINT16_deserialize(jso2, &out->minor);
}

/** Deserialize a TPMU_CELMGT json object.
 *
 * Desearialize a canonical eventlog management event.
 * @param[in]  selector The CEL type.
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMU_CELMGT_deserialize(
    UINT32 selector,
    json_object *jso,
    TPMU_CELMGT *out)
{
    json_object *jso2 = NULL;
    LOG_TRACE("call");
    switch (selector) {
    case CEL_VERSION:
        return ifapi_json_TPMS_CEL_VERSION_deserialize(jso, &out->cel_version);
    case FIRMWARE_END:
        return ifapi_json_TPMS_EMPTY_deserialize(jso, &out->firmware_end);
    case CEL_TIMESTAMP:
        if (!ifapi_get_sub_object(jso, "cel_timestamp", &jso2)) {
            LOG_ERROR("Field \"cel_timestamp\" not found.");
            return TSS2_FAPI_RC_BAD_VALUE;
        }
        return ifapi_json_UINT64_deserialize(jso2, &out->cel_timestamp);

    default:
        LOG_TRACE("false");
        return TSS2_FAPI_RC_BAD_VALUE;
    };
}

static char *field_TPMS_EVENT_CELMGT_tab[] = {
    "type",
    "data",
    "$schema"
};

/** Deserialize a TPMI_CELMGTTYPE json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 */
TSS2_RC
ifapi_json_TPMI_CELMGTTYPE_deserialize(json_object *jso, TPMI_CELMGTTYPE *out)
{
    static const struct { TPMI_CELMGTTYPE in; const char *name; } jso_tab[] = {
        { CEL_VERSION, "cel_version" },
        { FIRMWARE_END, "firmware_end" },
    };
    const char *str = json_object_get_string(jso);
    if (str) {
        for (size_t i = 0; i < sizeof(jso_tab) / sizeof(jso_tab[0]); i++) {
            if (strcasecmp(str, &jso_tab[i].name[0]) == 0) {
                *out = jso_tab[i].in;
                return TSS2_RC_SUCCESS;
            }
        }
    }
    SUBTYPE_FILTER(TPMI_CELMGTTYPE, UINT32,
                   CEL_VERSION, FIRMWARE_END);
}

/** Deserialize a TPMS_EVENT_CELMGT json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_EVENT_CELMGT_deserialize(json_object *jso,  TPMS_EVENT_CELMGT *out)
{
    json_object *jso2;
    TSS2_RC r;
    LOG_TRACE("call");
    return_if_null(out, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    ifapi_check_json_object_fields(jso, &field_TPMS_EVENT_CELMGT_tab[0],
                                   SIZE_OF_ARY(field_TPMS_EVENT_CELMGT_tab));
    if (!ifapi_get_sub_object(jso, "type", &jso2)) {
        LOG_ERROR("Field \"type\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }

    r = ifapi_json_TPMI_CELMGTTYPE_deserialize(jso2, &out->type);
    return_if_error(r, "Bad value for field \"type\".");

    if (out->type != FIRMWARE_END) {
        if(!ifapi_get_sub_object(jso, "data", &jso2)) {
            LOG_ERROR("Field \"data\" not found.");
            return TSS2_FAPI_RC_BAD_VALUE;
        }
        r = ifapi_json_TPMU_CELMGT_deserialize(out->type, jso2, &out->data);
        return_if_error(r, "Bad value for field \"data\".");
    }

    LOG_TRACE("true");
    return TSS2_RC_SUCCESS;
}
