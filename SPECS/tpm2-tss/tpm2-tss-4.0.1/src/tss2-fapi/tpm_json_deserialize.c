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
#include <ctype.h>

#include "ifapi_helpers.h"
#include "tpm_json_deserialize.h"
#define LOGMODULE fapijson
#include "util/log.h"
#include "util/aux_util.h"


/** Parse JSON data and create JSON object.
 *
 * The JSON character string will be parsed and a JSON object will
 * be created vor valid JSON.  For invalid JSON data
 * an error message which indicates the error position will be
 * displayed.
 *
 * @param[in] jstring The JSON data.
 * @retval The JSON object vor valid JSON.
 * @retval NULL for invalid JSON.
 */
json_object*
ifapi_parse_json(const char *jstring) {
    json_object *jso = NULL;
    enum json_tokener_error jerr;
    int line = 1;
    int line_offset = 0;
    int char_pos;
    struct json_tokener* tok = json_tokener_new();
    if (!tok) {
        LOG_ERROR("Could not allocate json tokener");
        return NULL;
    }
    jso = json_tokener_parse_ex(tok, jstring, -1);
    jerr = json_tokener_get_error(tok);
    if (jerr != json_tokener_success) {
        for (char_pos = 0; char_pos <= tok->char_offset; char_pos++) {
            if (jstring[char_pos] == '\n') {
                line++;
                line_offset = 0;
            } else {
                line_offset++;
            }
        }
        LOG_ERROR("Invalid JSON at line %i column %i: %s.", line, line_offset,
                  json_tokener_error_desc(jerr));
        json_tokener_free(tok);
        return NULL;
    }
    json_tokener_free(tok);
    return jso;
}

/** Strip a prefix from the input
 *
 * Strip the provided prefixes from the provided
 * input string and return the substring.
 *
 * @param[in] in The input string to strip the prefix from
 * @param[in] ... A list of prefixes to string from the input string
 * @return The prefix cleared substring
 */
static const char *
strip_prefix(const char *in, ...)
{
    va_list ap;
    const char *prefix;

    if (!in)
        return NULL;

    va_start(ap, in);
    while ((prefix = va_arg(ap, const char *)) != NULL) {
        if (strncasecmp(in, prefix, strlen(prefix)) == 0) {
            in = &in[strlen(prefix)];
        }
    }
    va_end(ap);

    return in;
}

/** Deserialize a TPMS_EMPTY .
 *
 * @param[out] out not used.
 * @param[in]  jso not used.
 */
TSS2_RC
ifapi_json_TPMS_EMPTY_deserialize(json_object *jso, TPMS_EMPTY *out)
{
    UNUSED(out);
    UNUSED(jso);
    LOG_TRACE("call");
    return TSS2_RC_SUCCESS;
}

/** Convert a byte array in character representation to binary.
 *
 * @param[in]  hex the character representation of the byte array
 * @param[in]  vlen the maximal length of the binary byte array.
 * @param[out] val the byte array.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the character representation is too long.
 */
TSS2_RC
ifapi_hex_to_byte_ary(const char hex[], UINT32 vlen, BYTE val[])
{
    UINT32 j;
    UINT32 hexlen;

    hexlen = strlen(hex);

    if (vlen < hexlen / 2) {
        LOG_ERROR("Hex string too long. (%zu > %"PRIu32")", strlen(hex) / 2, vlen);
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    for (j = 0; j < vlen
            && 2 * j < hexlen; j++) { //convert hex-Argv to byte array
        if (!isxdigit(hex[2 * j]) || (!(hex[2 * j + 1] == 0)
                                      && !isxdigit(hex[2 * j + 1]))) {
            LOG_ERROR("Error in value (%i)", j);
            return TSS2_FAPI_RC_BAD_VALUE;
        }
        val[j] = hex[2 * j] < 65 ? hex[2 * j] - 48 :
                 hex[2 * j] < 97 ? hex[2 * j] - 65 + 10 : hex[2 * j] - 97 + 10;
        val[j] *= 16;
        if (hex[2 * j + 1] != 0)
            val[j] += hex[2 * j + 1] < 65 ? hex[2 * j + 1] - 48 :
                      hex[2 * j + 1] < 97 ? hex[2 * j + 1] - 65 + 10 : hex[2 * j + 1] - 97 + 10;
    }
    for (; j < vlen; j++) {    //Padd with 0
        val[j] = 0;
    }
    return TSS2_RC_SUCCESS;
}

/** Deserialize a json array of bytes.
 *
 * @param[in] jso the parent object of the json byte array.
 * @param[in] max maximal size of the deserialized object.
 * @param[out] out* Pointer to the deserialized byte array.
 * @param[out] out_size the length of the deserialized byte array.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 */
TSS2_RC
ifapi_json_byte_deserialize(
    json_object *jso,
    UINT32 max,
    BYTE *out,
    UINT16 *out_size)
{
    TSS2_RC r;

    json_type jso_type = json_object_get_type(jso);
    if (jso_type == json_type_array) {
        r = ifapi_json_BYTE_array_deserialize(max, jso, out);
        return_if_error(r, "BAD VALUE");
        *out_size = json_object_array_length(jso);
    } else if (jso_type == json_type_string) {
        const char *token = json_object_get_string(jso);
        int itoken = 0;
        if (strncmp(token, "0x", 2) == 0)
            itoken = 2;
        r = ifapi_hex_to_byte_ary(&token[itoken], max, out);
        return_if_error(r, "Error convert hex digest to binary.");
        *out_size = (strlen(token) - itoken) / 2;
    } else {
        LOG_ERROR("Byte array is neither of type array nor string.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    return TSS2_RC_SUCCESS;
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

/** Get sub object from a json object.
 *
 * A sub object with a certain name stored in the passed object is returned.
 * If the sub object is not found e second trial with the lower case version
 * of the name will be performed.
 *
 * param[in] jso the object with the sub object.
 * param[in] name  the name of the stored sub object.
 * param[out] sub_jso the pointer to the sub object.
 * @retval true if object was found.
 * @retval false if the object was not found.
 */
bool
ifapi_get_sub_object(json_object *jso, char *name, json_object **sub_jso)
{
    int i;
    if (json_object_object_get_ex(jso, name, sub_jso)) {
        return true;
    } else {
        char name2[strlen(name) + 1];
        for (i = 0; name[i]; i++)
            name2[i] = tolower(name[i]);
        name2[strlen(name)] = '\0';
        return json_object_object_get_ex(jso, name2, sub_jso);
    }
}

/** Get number from a json object.
 *
 * A int64 number is retrieved from a json object which should represent a number.
 *
 * param[in] jso the json object.
 * param[out] num the int64 number.
 * @retval TSS2_RC_SUCCESS if json object represents a number.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object does not represent a number.
 */
static TSS2_RC
get_number_from_json(json_object *jso, int64_t *num)
{
    const char *token = json_object_get_string(jso);
    if (!get_number(token, num)) {
        LOG_ERROR("Bad value");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    return TSS2_RC_SUCCESS;
}

/** Get boolean from a json object.
 *
 * A boolean value is retrieved from a json object.
 * The value can be 1, 0, yes, or no.
 *
 * param[in] jso the json object.
 * param[out] value the boolean value.
 * @retval TSS2_RC_SUCCESS if json object represents a boolean.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object does not represent a boolean.
 */
static TSS2_RC
get_boolean_from_json(json_object *jso, TPMI_YES_NO *value)
{
    TSS2_RC r = ifapi_json_TPMI_YES_NO_deserialize(jso, value);
    if (r != TSS2_RC_SUCCESS) {
        const char *token = json_object_get_string(jso);
        if (strcasecmp(token, "set") || strcasecmp(token, "on")) {
            *value = 1;
        } else if (strcasecmp(token, "off")) {
            *value = 0;
        } else {
            return_error(TSS2_FAPI_RC_BAD_VALUE, "No boolean value");
        }
    }
    if (*value != 0 && *value != 1) {
        return_error(TSS2_FAPI_RC_BAD_VALUE, "No boolean value.");
    };
    return TSS2_RC_SUCCESS;
}

/** Deserialize json object which represents a pcr selection.
 *
 * @param[in]  jso json array of pcr registers.
 * @param[out] sizeofSelect size of bit mask for used pcr registers.
 * @param[out] pcrSelect byte array with bit mask.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 */
TSS2_RC
ifapi_json_pcr_selection_deserialize(
    json_object *jso,
    UINT8 *sizeofSelect,
    BYTE pcrSelect[])
{
    LOG_TRACE("call");
    TSS2_RC r;
    size_t i;
    int64_t n;
    int n_byte = 0;
    json_type jso_type = json_object_get_type(jso);

    if (jso_type != json_type_array) {
        return_error(TSS2_FAPI_RC_BAD_VALUE, "Bad value (array of numbers expected).");
    }
    /* Cast (size_t) is necessary to support older version of libjson-c */
    for (i = 0; i < (size_t)json_object_array_length(jso); i++) {
        r = get_number_from_json(json_object_array_get_idx(jso, i), &n);
        return_if_error(r, "Bad PCR value");
        n_byte = n / 8;
        pcrSelect[n_byte] |= (BYTE)(1 << (n % 8));
        if (n_byte > *sizeofSelect)
            *sizeofSelect = n_byte;
    }
    *sizeofSelect = 3;
    return TSS2_RC_SUCCESS;
}

/** Deserialize an array of UINT8.
 *
 * @param[in]  jso object to be deserialized.
 * @param[out] out the deserialized object.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 */
TSS2_RC
ifapi_json_UINT8_ARY_deserialize(
    json_object *jso,
    UINT8_ARY *out)
{
    TSS2_RC r;

    const char *hex_string = json_object_get_string(jso);
    out->size = strlen(hex_string) / 2;
    out->buffer = malloc(out->size);
    return_if_null(out->buffer, "Out of memory.", TSS2_FAPI_RC_MEMORY);

    r = ifapi_hex_to_byte_ary(hex_string, out->size, &out->buffer[0]);
    return_if_error(r, "Can't convert hex values.");

    return TSS2_RC_SUCCESS;
}

/** Deserialize a TPMS_PCR_SELECT variable.
 *
 * @param[in]  jso  json object to be deserialized.
 * @param[out] out the deserialized object.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 */
TSS2_RC
ifapi_json_TPMS_PCR_SELECT_deserialize(json_object *jso,  TPMS_PCR_SELECT *out)
{
    LOG_TRACE("call");

    memset(out, 0, sizeof(TPMS_PCR_SELECT));
    return ifapi_json_pcr_selection_deserialize(jso, &out->sizeofSelect,
            &out->pcrSelect[0]);
}

static char *field_TPMS_PCR_SELECTION_tab[] = {
    "hash",
    "pcrSelect",
    "pcrselect",
    "$schema"
};

/** Deserialize a TPMS_PCR_SELECTION variable.
 *
 * @param[in]  jso json object to be deserialized.
 * @param[out] out the deserialized object.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 */
TSS2_RC
ifapi_json_TPMS_PCR_SELECTION_deserialize(json_object *jso,
        TPMS_PCR_SELECTION *out)
{
    LOG_TRACE("call");
    json_object *jso2;
    TSS2_RC r;

    memset(out, 0, sizeof(TPMS_PCR_SELECTION));
    ifapi_check_json_object_fields(jso, &field_TPMS_PCR_SELECTION_tab[0],
                                   SIZE_OF_ARY(field_TPMS_PCR_SELECTION_tab));
    if (!ifapi_get_sub_object(jso, "hash", &jso2)) {
        LOG_ERROR("Field \"hash\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPMI_ALG_HASH_deserialize(jso2, &out->hash);
    return_if_error(r, "Bad value for field \"hash\".");

    if (!ifapi_get_sub_object(jso, "pcrSelect", &jso2)) {
        LOG_ERROR("Field \"pcrSelect\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    return ifapi_json_pcr_selection_deserialize(jso2, &out->sizeofSelect,
            &out->pcrSelect[0]);
}

static char *field_TPMS_TAGGED_POLICY_tab[] = {
    "handle",
    "policyHash"
};

/** Deserialize a TPMS_TAGGED_POLICY variable.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 *
 */
TSS2_RC
ifapi_json_TPMS_TAGGED_POLICY_deserialize(json_object *jso,
        TPMS_TAGGED_POLICY *out)
{
    json_object *jso2;
    TSS2_RC r;
    LOG_TRACE("call");
    return_if_null(out, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    memset(out, 0, sizeof(TPMS_TAGGED_POLICY));
    ifapi_check_json_object_fields(jso, &field_TPMS_TAGGED_POLICY_tab[0],
                                   SIZE_OF_ARY(field_TPMS_TAGGED_POLICY_tab));
    if (!ifapi_get_sub_object(jso, "handle", &jso2)) {
        LOG_ERROR("Field \"handle\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPM2_HANDLE_deserialize(jso2, &out->handle);
    return_if_error(r, "Bad value for field \"handle\".");

    if (!ifapi_get_sub_object(jso, "policyHash", &jso2)) {
        LOG_ERROR("Field \"policyHash\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPMT_HA_deserialize(jso2, &out->policyHash);
    return_if_error(r, "Bad value for field \"policyHash\".");

    LOG_TRACE("true");
    return TSS2_RC_SUCCESS;
}

static char *field_TPMS_ACT_DATA_tab[] = {
    "handle",
    "timeout",
    "attributes"
};

/** Deserialize a TPMS_ACT_DATA variable.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 *
 */
TSS2_RC
ifapi_json_TPMS_ACT_DATA_deserialize(json_object *jso,
        TPMS_ACT_DATA *out)
{
    json_object *jso2;
    TSS2_RC r;
    LOG_TRACE("call");
    return_if_null(out, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    memset(out, 0, sizeof(TPMS_ACT_DATA));
    ifapi_check_json_object_fields(jso, &field_TPMS_ACT_DATA_tab[0],
                                   SIZE_OF_ARY(field_TPMS_ACT_DATA_tab));
    if (!ifapi_get_sub_object(jso, "handle", &jso2)) {
        LOG_ERROR("Field \"handle\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPM2_HANDLE_deserialize(jso2, &out->handle);
    return_if_error(r, "Bad value for field \"handle\".");

    if (!ifapi_get_sub_object(jso, "timeout", &jso2)) {
        LOG_ERROR("Field \"timeout\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_UINT32_deserialize(jso2, &out->timeout);
    return_if_error(r, "Bad value for field \"timeout\".");

    if (!ifapi_get_sub_object(jso, "attributes", &jso2)) {
        LOG_ERROR("Field \"attributes\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPMA_ACT_deserialize(jso2, &out->attributes);
    return_if_error(r, "Bad value for field \"attributes\".");

    LOG_TRACE("true");
    return TSS2_RC_SUCCESS;
}

/** Deserialize an array of BYTE structures.
 *
 * @param[in] max the maximal number of bytess to be deserialized.
 * @param[in] jso the JSON object with the byte array.
 * @param[in] out the byte array for deserialization.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 */
TSS2_RC
ifapi_json_BYTE_array_deserialize(size_t max, json_object *jso, BYTE *out)
{
    LOG_TRACE("call");
    json_type jso_type = json_object_get_type(jso);
    if (jso_type == json_type_array) {
        int size = json_object_array_length(jso);
        if (size > (int)max) {
            LOG_ERROR("Array of BYTE too large (%i > %zu)", size, max);
        }
        for (int i = 0; i < size; i++) {
            json_object *jso2 = json_object_array_get_idx(jso, i);
            TSS2_RC r = ifapi_json_BYTE_deserialize(jso2, &out[i]);
            return_if_error(r, "BAD VALUE");
        }
        return TSS2_RC_SUCCESS;
    } else {
        LOG_ERROR("BAD VALUE");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
}

/** Deserialize a BYTE json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 */
TSS2_RC
ifapi_json_BYTE_deserialize(json_object *jso, BYTE *out)
{
    LOG_TRACE("call");
    const char *token = json_object_get_string(jso);
    int64_t i64;
    if (!get_number(token, &i64)) {
        LOG_ERROR("Bad value");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    *out = (BYTE) i64;
    if ((int64_t)*out != i64) {
        LOG_ERROR("Bad value");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    return TSS2_RC_SUCCESS;
}

/** Deserialize a UINT8 json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 */
TSS2_RC
ifapi_json_UINT8_deserialize(json_object *jso, UINT8 *out)
{
    LOG_TRACE("call");
    const char *token = json_object_get_string(jso);
    int64_t i64;
    if (!get_number(token, &i64)) {
        LOG_ERROR("Bad value");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    *out = (UINT8) i64;
    if ((int64_t)*out != i64) {
        LOG_ERROR("Bad value");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    return TSS2_RC_SUCCESS;
}

/** Deserialize a UINT16 json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 */
TSS2_RC
ifapi_json_UINT16_deserialize(json_object *jso, UINT16 *out)
{
    LOG_TRACE("call");
    const char *token = json_object_get_string(jso);
    int64_t i64;
    if (!get_number(token, &i64)) {
        LOG_ERROR("Bad value %s", json_object_get_string(jso));
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    *out = (UINT16) i64;
    if ((int64_t)*out != i64) {
        LOG_ERROR("Bad value %s", json_object_get_string(jso));
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    return TSS2_RC_SUCCESS;
}

/** Deserialize a UINT32 json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 */
TSS2_RC
ifapi_json_UINT32_deserialize(json_object *jso, UINT32 *out)
{
    LOG_TRACE("call");
    const char *token = json_object_get_string(jso);
    int64_t i64;
    if (!get_number(token, &i64)) {
        LOG_ERROR("Bad value");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    *out = (UINT32) i64;
    if ((int64_t)*out != i64) {
        LOG_ERROR("Bad value");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    return TSS2_RC_SUCCESS;
}

/** Deserialize a UINT64 json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 */
TSS2_RC
ifapi_json_UINT64_deserialize(json_object *jso, UINT64 *out)
{
    UINT32 tmp;
    LOG_TRACE("call");
    /* json-c allows only 53 bit numbers, therefore 64 bit numbers are split */
    if (json_object_get_type(jso) == json_type_array) {
        if (json_object_array_length(jso) != 2) {
            LOG_ERROR("Bad value");
            return TSS2_FAPI_RC_BAD_VALUE;
        }
        TSS2_RC r = ifapi_json_UINT32_deserialize(json_object_array_get_idx(jso, 0),
                        &tmp);
        return_if_error(r, "BAD VALUE");
        *out = tmp * 0x100000000;

        r = ifapi_json_UINT32_deserialize(json_object_array_get_idx(jso, 1),
                                          &tmp);
        return_if_error(r, "BAD VALUE");
        *out += tmp;
        return TSS2_RC_SUCCESS;
    }

    const char *token = json_object_get_string(jso);
    int64_t i64;
    if (!get_number(token, &i64)) {
        LOG_ERROR("Bad value");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    *out = (UINT64) i64;
    if ((int64_t)*out != i64) {
        LOG_ERROR("Bad value");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    return TSS2_RC_SUCCESS;
}

/** Deserialize a TPM2_GENERATED json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 */
TSS2_RC
ifapi_json_TPM2_GENERATED_deserialize(json_object *jso, TPM2_GENERATED *out)
{
    static const struct { TPM2_GENERATED in; const char *name; } tab[] = {
        { TPM2_GENERATED_VALUE, "VALUE" },
    };

    const char *s = json_object_get_string(jso);
    const char *str = strip_prefix(s, "TPM_", "TPM2_", "GENERATED_", NULL);
    LOG_TRACE("called for %s parsing %s", s, str);

    if (str) {
        for (size_t i = 0; i < sizeof(tab) / sizeof(tab[0]); i++) {
            if (strcasecmp(str, &tab[i].name[0]) == 0) {
                *out = tab[i].in;
                return TSS2_RC_SUCCESS;
            }
        }
    }

    return ifapi_json_UINT32_deserialize(jso, out);
}

/** Deserialize a TPM2_ALG_ID json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 */
TSS2_RC
ifapi_json_TPM2_ALG_ID_deserialize(json_object *jso, TPM2_ALG_ID *out)
{
    static const struct { TPM2_ALG_ID in; const char *name; } tab[] = {
        { TPM2_ALG_ERROR, "ERROR" },
        { TPM2_ALG_RSA, "RSA" },
        { TPM2_ALG_SHA, "SHA" },
        { TPM2_ALG_SHA1, "SHA1" },
        { TPM2_ALG_HMAC, "HMAC" },
        { TPM2_ALG_AES, "AES" },
        { TPM2_ALG_MGF1, "MGF1" },
        { TPM2_ALG_KEYEDHASH, "KEYEDHASH" },
        { TPM2_ALG_XOR, "XOR" },
        { TPM2_ALG_SHA256, "SHA256" },
        { TPM2_ALG_SHA384, "SHA384" },
        { TPM2_ALG_SHA512, "SHA512" },
        { TPM2_ALG_NULL, "NULL" },
        { TPM2_ALG_SM3_256, "SM3_256" },
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

    const char *s = json_object_get_string(jso);
    const char *str = strip_prefix(s, "TPM_", "TPM2_", "ALG_", "ID_", NULL);
    LOG_TRACE("called for %s parsing %s", s, str);

    if (str) {
        for (size_t i = 0; i < sizeof(tab) / sizeof(tab[0]); i++) {
            if (strcasecmp(str, &tab[i].name[0]) == 0) {
                *out = tab[i].in;
                return TSS2_RC_SUCCESS;
            }
        }
    }

    return ifapi_json_UINT16_deserialize(jso, out);
}

/** Deserialize a TPM2_ECC_CURVE json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 */
TSS2_RC
ifapi_json_TPM2_ECC_CURVE_deserialize(json_object *jso, TPM2_ECC_CURVE *out)
{
    static const struct { TPM2_ECC_CURVE in; const char *name; } tab[] = {
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

    const char *s = json_object_get_string(jso);
    const char *str = strip_prefix(s, "TPM_", "TPM2_", "ECC_", "CURVE_", NULL);
    LOG_TRACE("called for %s parsing %s", s, str);

    if (str) {
        for (size_t i = 0; i < sizeof(tab) / sizeof(tab[0]); i++) {
            if (strcasecmp(str, &tab[i].name[0]) == 0) {
                *out = tab[i].in;
                return TSS2_RC_SUCCESS;
            }
        }
    }

    return ifapi_json_UINT16_deserialize(jso, out);
}

/** Deserialize a TPM2_CC json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 */
TSS2_RC
ifapi_json_TPM2_CC_deserialize(json_object *jso, TPM2_CC *out)
{
    static const struct { TPM2_CC in; const char *name; } tab[] = {
        { TPM2_CC_FIRST, "FIRST" },
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
        { TPM2_CC_LAST, "LAST" },
        { TPM2_CC_Vendor_TCG_Test, "Vendor_TCG_Test" },
    };

    const char *s = json_object_get_string(jso);
    const char *str = strip_prefix(s, "TPM_", "TPM2_", "CC_", NULL);
    LOG_TRACE("called for %s parsing %s", s, str);

    if (str) {
        for (size_t i = 0; i < sizeof(tab) / sizeof(tab[0]); i++) {
            if (strcasecmp(str, &tab[i].name[0]) == 0) {
                *out = tab[i].in;
                return TSS2_RC_SUCCESS;
            }
        }
    }

    return ifapi_json_UINT32_deserialize(jso, out);
}

/** Deserialize a TPM2_EO json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 */
TSS2_RC
ifapi_json_TPM2_EO_deserialize(json_object *jso, TPM2_EO *out)
{
    static const struct { TPM2_EO in; const char *name; } tab[] = {
        { TPM2_EO_EQ,          "EQ" },
        { TPM2_EO_NEQ,         "NEQ" },
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

    const char *s = json_object_get_string(jso);
    const char *str = strip_prefix(s, "TPM_", "TPM2_", "EO_", NULL);
    LOG_TRACE("called for %s parsing %s", s, str);

    if (str) {
        for (size_t i = 0; i < sizeof(tab) / sizeof(tab[0]); i++) {
            if (strcasecmp(str, &tab[i].name[0]) == 0) {
                *out = tab[i].in;
                return TSS2_RC_SUCCESS;
            }
        }
    }

    return ifapi_json_UINT16_deserialize(jso, out);
}

/** Deserialize a TPM2_ST json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 */
TSS2_RC
ifapi_json_TPM2_ST_deserialize(json_object *jso, TPM2_ST *out)
{
    static const struct { TPM2_ST in; const char *name; } tab[] = {
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

    const char *s = json_object_get_string(jso);
    const char *str = strip_prefix(s, "TPM_", "TPM2_", "ST_", NULL);
    LOG_TRACE("called for %s parsing %s", s, str);

    if (str) {
        for (size_t i = 0; i < sizeof(tab) / sizeof(tab[0]); i++) {
            if (strcasecmp(str, &tab[i].name[0]) == 0) {
                *out = tab[i].in;
                return TSS2_RC_SUCCESS;
            }
        }
    }

    return ifapi_json_UINT16_deserialize(jso, out);
}

/** Deserialize a TPM2_PT_PCR json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 */
TSS2_RC
ifapi_json_TPM2_PT_PCR_deserialize(json_object *jso, TPM2_PT_PCR *out)
{
    static const struct { TPM2_PT_PCR in; const char *name; } tab[] = {
        { TPM2_PT_TPM2_PCR_FIRST, "FIRST" },
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
        { TPM2_PT_TPM2_PCR_LAST, "LAST" }
    };

    const char *s = json_object_get_string(jso);
    const char *str = strip_prefix(s, "TPM_", "TPM2_", "PT_", "PCR_", NULL);
    LOG_TRACE("called for %s parsing %s", s, str);

    if (str) {
        for (size_t i = 0; i < sizeof(tab) / sizeof(tab[0]); i++) {
            if (strcasecmp(str, &tab[i].name[0]) == 0) {
                *out = tab[i].in;
                return TSS2_RC_SUCCESS;
            }
        }
    }

    return ifapi_json_UINT32_deserialize(jso, out);
}

/*** Table 26 .Definition of Types for HandlesTable ***/

/**  Deserialize a TPM2_HANDLE json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 */
TSS2_RC
ifapi_json_TPM2_HANDLE_deserialize(json_object *jso, TPM2_HANDLE *out)
{
    LOG_TRACE("call");
    const char *token = json_object_get_string(jso);
    int64_t i64;
    if (get_number(token, &i64)) {
        *out = (TPM2_HANDLE) i64;
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

/** Deserialize a TPMA_OBJECT json object.
 *
 * @param[in] jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 */
TSS2_RC
ifapi_json_TPMA_OBJECT_deserialize(json_object *jso, TPMA_OBJECT *out)
{
    struct { TPMA_OBJECT in; char *name; } tab[] = {
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
    size_t n = sizeof(tab) / sizeof(tab[0]);
    size_t i, j;

    TPMI_YES_NO flag;
    TSS2_RC r;

    LOG_TRACE("call");
    memset(out, 0, sizeof(TPMA_OBJECT));
    json_type jso_type = json_object_get_type(jso);
    if (jso_type == json_type_array) {
        /* Cast (size_t) is necessary to support older version of libjson-c */
        for (i = 0; i < (size_t)json_object_array_length(jso); i++) {
            json_object *jso2 = json_object_array_get_idx(jso, i);
            const char *token = strip_prefix(json_object_get_string(jso2),
                                    "TPM_", "TPM2_", "TPMA_", "OBJECT_", NULL);
            if (!token) {
                LOG_ERROR("Bad object; expected array of strings.");
                return TSS2_FAPI_RC_BAD_VALUE;
            }
            for (j = 0; j < n; j++) {
                if (strcasecmp(tab[j].name, token) == 0) {
                    *out |= tab[j].in;
                    break;
                }
            }
            if (j == n) {
                LOG_ERROR("Unknown value: %s", json_object_get_string(jso2));
                return TSS2_FAPI_RC_BAD_VALUE;
            }
        }
    } else if (jso_type == json_type_object) {
        json_object_object_foreach(jso, key, val) {
            const char *token = strip_prefix(key,
                                    "TPM_", "TPM2_", "TPMA_", "OBJECT_", NULL);
            r = get_boolean_from_json(val, &flag);
            return_if_error2(r, "Boolean value expected at key: %s", key);
            for (j = 0; j < n; j++) {
                if (strcasecmp(tab[j].name, token) == 0) {
                    if (flag)
                        *out |= tab[j].in;
                    break;
                }
            }
            if (j == n) {
                LOG_ERROR("Unknown key: %s", key);
                return TSS2_FAPI_RC_BAD_VALUE;
            }
        }
    } else {
        const char *token;
        token = json_object_get_string(jso);
        int64_t i64;
        if (!get_number(token, &i64)) {
            LOG_ERROR("Bad value");
            return TSS2_FAPI_RC_BAD_VALUE;
        }
        *out = (TPMA_OBJECT) i64;
        if ((int64_t)*out != i64) {
            LOG_ERROR("Bad value");
            return TSS2_FAPI_RC_BAD_VALUE;
        }
        return TSS2_RC_SUCCESS;
    }
    LOG_TRACE("true");
    return TSS2_RC_SUCCESS;
}

/** Deserialize a TPMA_LOCALITY json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 */
TSS2_RC
ifapi_json_TPMA_LOCALITY_deserialize(json_object *jso, TPMA_LOCALITY *out)
{
    struct { TPMA_LOCALITY in; char *name; } tab[] = {
        { TPMA_LOCALITY_TPM2_LOC_ZERO, "ZERO" },
        { TPMA_LOCALITY_TPM2_LOC_ONE, "ONE" },
        { TPMA_LOCALITY_TPM2_LOC_TWO, "TWO" },
        { TPMA_LOCALITY_TPM2_LOC_THREE, "THREE" },
        { TPMA_LOCALITY_TPM2_LOC_FOUR, "FOUR" },
    };
    size_t n = sizeof(tab) / sizeof(tab[0]);
    size_t i, j;

    TPMI_YES_NO flag;
    TSS2_RC r;

    LOG_TRACE("call");
    memset(out, 0, sizeof(TPMA_LOCALITY));
    json_type jso_type = json_object_get_type(jso);
    if (jso_type == json_type_array) {
        /* Cast (size_t) is necessary to support older version of libjson-c */
        for (i = 0; i < (size_t)json_object_array_length(jso); i++) {
            json_object *jso2 = json_object_array_get_idx(jso, i);
            const char *token = strip_prefix(json_object_get_string(jso2),
                                    "TPM_", "TPM2_", "TPMA_", "LOCALITY_",
                                    "TPM2_", "LOC_", NULL);
            if (!token) {
                LOG_ERROR("Bad object; expected array of strings.");
                return TSS2_FAPI_RC_BAD_VALUE;
            }
            for (j = 0; j < n; j++) {
                if (strcasecmp(tab[j].name, token) == 0) {
                    *out |= tab[j].in;
                    break;
                }
            }
            if (j == n) {
                LOG_ERROR("Unknown value: %s", json_object_get_string(jso2));
                return TSS2_FAPI_RC_BAD_VALUE;
            }
        }
    } else if (jso_type == json_type_object) {
        json_object_object_foreach(jso, key, val) {
            const char *token = strip_prefix(key,
                                    "TPM_", "TPM2_", "TPMA_", "LOCALITY_",
                                    "TPM2_", "LOC_", NULL);
            if (strcasecmp(token, "extended") == 0) {
                int64_t i64;
                if (!get_number(json_object_get_string(val), &i64)) {
                    LOG_ERROR("Bad value");
                    return TSS2_FAPI_RC_BAD_VALUE;
                }
                if (((i64<<5) & ~TPMA_LOCALITY_EXTENDED_MASK) != 0) {
                    LOG_ERROR("Bad value for extended");
                    return TSS2_FAPI_RC_BAD_VALUE;
                }
                *out |= (TPMA_LOCALITY)(i64<<5);
                continue;
            }
            r = get_boolean_from_json(val, &flag);
            return_if_error2(r, "Boolean value expected at key: %s", key);
            for (j = 0; j < n; j++) {
                if (strcasecmp(tab[j].name, token) == 0) {
                    if (flag)
                        *out |= tab[j].in;
                    break;
                }
            }
            if (j == n) {
                LOG_ERROR("Unknown key: %s", key);
                return TSS2_FAPI_RC_BAD_VALUE;
            }
        }
    } else {
        const char *token;
        token = json_object_get_string(jso);
        int64_t i64;
        if (!get_number(token, &i64)) {
            LOG_ERROR("Bad value");
            return TSS2_FAPI_RC_BAD_VALUE;
        }
        *out = (TPMA_LOCALITY) i64;
        if ((int64_t)*out != i64) {
            LOG_ERROR("Bad value");
            return TSS2_FAPI_RC_BAD_VALUE;
        }
        return TSS2_RC_SUCCESS;
    }
    LOG_TRACE("true");
    return TSS2_RC_SUCCESS;
}

/** Deserialize a TPMA_ACT json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 */
TSS2_RC
ifapi_json_TPMA_ACT_deserialize(json_object *jso, TPMA_ACT *out) {
    static const struct {TPMA_ACT in; char *name; } tab[] = {
        {TPMA_ACT_SIGNALED, "signaled"},
        {TPMA_ACT_PRESERVESIGNALED, "preserveSignaled"},
    };

    size_t n = sizeof(tab) / sizeof(tab[0]);
    size_t i, j;

    TPMI_YES_NO flag;
    TSS2_RC r;

    LOG_TRACE("call");
    memset(out, 0, sizeof(TPMA_ACT));
    json_type jso_type = json_object_get_type(jso);
    if (jso_type == json_type_array) {
        /* Cast (size_t) is necessary to support older version of libjson-c */
        for (i = 0; i < (size_t)json_object_array_length(jso); i++) {
            json_object *jso2 = json_object_array_get_idx(jso, i);
            const char *token = strip_prefix(json_object_get_string(jso2),
                                    "TPM_", "TPM2_", "TPMA_", "ACT_", NULL);
            if (!token) {
                LOG_ERROR("Bad object; expected array of strings.");
                return TSS2_FAPI_RC_BAD_VALUE;
            }
            for (j = 0; j < n; j++) {
                if (strcasecmp(tab[j].name, token) == 0) {
                    *out |= tab[j].in;
                    break;
                }
            }
            if (j == n) {
                LOG_ERROR("Unknown value: %s", json_object_get_string(jso2));
                return TSS2_FAPI_RC_BAD_VALUE;
            }
        }
    } else if (jso_type == json_type_object) {
        json_object_object_foreach(jso, key, val) {
            const char *token = strip_prefix(key,
                                    "TPM_", "TPM2_", "TPMA_", "ACT_", NULL);
            r = get_boolean_from_json(val, &flag);
            return_if_error2(r, "Boolean value expected at key: %s", key);
            for (j = 0; j < n; j++) {
                if (strcasecmp(tab[j].name, token) == 0) {
                    if (flag)
                        *out |= tab[j].in;
                    break;
                }
            }
            if (j == n) {
                LOG_ERROR("Unknown key: %s", key);
                return TSS2_FAPI_RC_BAD_VALUE;
            }
        }
    } else {
        const char *token;
        token = json_object_get_string(jso);
        int64_t i64;
        if (!get_number(token, &i64)) {
            LOG_ERROR("Bad value");
            return TSS2_FAPI_RC_BAD_VALUE;
        }
        *out = (TPMA_ACT) i64;
        if ((int64_t)*out != i64) {
            LOG_ERROR("Bad value");
            return TSS2_FAPI_RC_BAD_VALUE;
        }
        return TSS2_RC_SUCCESS;
    }
    LOG_TRACE("true");
    return TSS2_RC_SUCCESS;

}

/** Deserialize a TPMI_YES_NO json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 */
TSS2_RC
ifapi_json_TPMI_YES_NO_deserialize(json_object *jso, TPMI_YES_NO *out)
{
    static const struct { TPMI_YES_NO in; const char *name; } tab[] = {
        { NO, "NO" },
        { YES, "YES" },
    };

    const char *s = json_object_get_string(jso);
    const char *str = strip_prefix(s, "TPM_", "TPM2_", "TPMI_", NULL);
    LOG_TRACE("called for %s parsing %s", s, str);

    if (str) {
        for (size_t i = 0; i < sizeof(tab) / sizeof(tab[0]); i++) {
            if (strcasecmp(str, &tab[i].name[0]) == 0) {
                *out = tab[i].in;
                return TSS2_RC_SUCCESS;
            }
        }
    }

    return ifapi_json_BYTE_deserialize(jso, out);
}

/** Deserialize a TPMI_RH_HIERARCHY json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 */
TSS2_RC
ifapi_json_TPMI_RH_HIERARCHY_deserialize(json_object *jso,
        TPMI_RH_HIERARCHY *out)
{
    static const struct { TPMI_RH_HIERARCHY in; const char *name; } tab[] = {
        { TPM2_RH_OWNER, "OWNER" },
        { TPM2_RH_PLATFORM, "PLATFORM" },
        { TPM2_RH_ENDORSEMENT, "ENDORSEMENT" },
        { TPM2_RH_NULL, "NULL" },
    };

    const char *s = json_object_get_string(jso);
    const char *str = strip_prefix(s, "TPM_", "TPM2_", "TPMI_", "RH_", "HIERARCHY_", NULL);
    LOG_TRACE("called for %s parsing %s", s, str);

    if (str) {
        for (size_t i = 0; i < sizeof(tab) / sizeof(tab[0]); i++) {
            if (strcasecmp(str, &tab[i].name[0]) == 0) {
                *out = tab[i].in;
                return TSS2_RC_SUCCESS;
            }
        }
    }

    return ifapi_json_UINT32_deserialize(jso, out);
}

/** Deserialize a TPMI_RH_NV_INDEX json object.
 *
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 */
TSS2_RC
ifapi_json_TPMI_RH_NV_INDEX_deserialize(json_object *jso, TPMI_RH_NV_INDEX *out)
{
    return ifapi_json_TPM2_HANDLE_deserialize(jso, out);
}

/** Deserialize a TPMI_ALG_HASH json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 */
TSS2_RC
ifapi_json_TPMI_ALG_HASH_deserialize(json_object *jso, TPMI_ALG_HASH *out)
{
    SUBTYPE_FILTER(TPMI_ALG_HASH, TPM2_ALG_ID,
        TPM2_ALG_SHA1, TPM2_ALG_SHA256, TPM2_ALG_SHA384, TPM2_ALG_SHA512, TPM2_ALG_SM3_256, TPM2_ALG_NULL);
}

/** Deserialize a  TPMI_ALG_SYM json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 */
TSS2_RC
ifapi_json_TPMI_ALG_SYM_deserialize(json_object *jso, TPMI_ALG_SYM *out)
{
    SUBTYPE_FILTER(TPMI_ALG_SYM, TPM2_ALG_ID,
        TPM2_ALG_AES, TPM2_ALG_CAMELLIA, TPM2_ALG_SM4, TPM2_ALG_XOR, TPM2_ALG_NULL);
}

/** Deserialize a TPMI_ALG_SYM_OBJECT json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 */
TSS2_RC
ifapi_json_TPMI_ALG_SYM_OBJECT_deserialize(json_object *jso,
        TPMI_ALG_SYM_OBJECT *out)
{
    SUBTYPE_FILTER(TPMI_ALG_SYM_OBJECT, TPM2_ALG_ID,
        TPM2_ALG_AES, TPM2_ALG_CAMELLIA, TPM2_ALG_SM4, TPM2_ALG_NULL);
}

/** Deserialize a TPMI_ALG_SYM_MODE json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 */
TSS2_RC
ifapi_json_TPMI_ALG_SYM_MODE_deserialize(json_object *jso,
        TPMI_ALG_SYM_MODE *out)
{
    SUBTYPE_FILTER(TPMI_ALG_SYM_MODE, TPM2_ALG_ID,
        TPM2_ALG_CTR, TPM2_ALG_OFB, TPM2_ALG_CBC, TPM2_ALG_CFB, TPM2_ALG_ECB, TPM2_ALG_NULL);
}

/** Deserialize a TPMI_ALG_CIPHER_MODE json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 */
TSS2_RC
ifapi_json_TPMI_ALG_CIPHER_MODE_deserialize(json_object *jso,
        TPMI_ALG_CIPHER_MODE *out)
{
    SUBTYPE_FILTER(TPMI_ALG_CIPHER_MODE, TPM2_ALG_ID,
        TPM2_ALG_CTR, TPM2_ALG_OFB, TPM2_ALG_CBC, TPM2_ALG_CFB, TPM2_ALG_ECB, TPM2_ALG_NULL);
}

/** Deserialize a TPMI_ALG_KDF json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 */
TSS2_RC
ifapi_json_TPMI_ALG_KDF_deserialize(json_object *jso, TPMI_ALG_KDF *out)
{
    SUBTYPE_FILTER(TPMI_ALG_KDF, TPM2_ALG_ID,
        TPM2_ALG_MGF1, TPM2_ALG_KDF1_SP800_56A, TPM2_ALG_KDF1_SP800_108, TPM2_ALG_NULL);
}

/** Deserialize a TPMI_ALG_SIG_SCHEME json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 */
TSS2_RC
ifapi_json_TPMI_ALG_SIG_SCHEME_deserialize(json_object *jso,
        TPMI_ALG_SIG_SCHEME *out)
{
    SUBTYPE_FILTER(TPMI_ALG_SIG_SCHEME, TPM2_ALG_ID,
        TPM2_ALG_RSASSA, TPM2_ALG_RSAPSS, TPM2_ALG_ECDSA, TPM2_ALG_ECDAA, TPM2_ALG_SM2,
        TPM2_ALG_ECSCHNORR, TPM2_ALG_HMAC, TPM2_ALG_NULL);
}

/** Deserialize a TPMU_HA json object.
 *
 * This functions expects the Bitfield to be encoded as unsigned int in host-endianess.
 * @param[in]  selector The type of the HA object.
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMU_HA_deserialize(
    UINT32 selector,
    json_object *jso,
    TPMU_HA *out)
{
    UINT16 size;
    UINT16 hash_size;
    uint8_t *buffer;
    TSS2_RC r;

    LOG_TRACE("call");
    switch (selector) {
    case TPM2_ALG_SHA1:
        hash_size = TPM2_SHA1_DIGEST_SIZE;
        buffer = &out->sha1[0];
        break;
    case TPM2_ALG_SHA256:
        hash_size = TPM2_SHA256_DIGEST_SIZE;
        buffer = &out->sha256[0];
        break;
    case TPM2_ALG_SHA384:
        hash_size = TPM2_SHA384_DIGEST_SIZE;
        buffer = &out->sha384[0];
        break;
    case TPM2_ALG_SHA512:
        hash_size = TPM2_SHA512_DIGEST_SIZE;
        buffer = &out->sha512[0];
        break;
    case TPM2_ALG_SM3_256:
        hash_size = TPM2_SM3_256_DIGEST_SIZE;
        buffer = &out->sm3_256[0];
        break;
    case TPM2_ALG_NULL: {
            return TSS2_RC_SUCCESS;
        }
    default:
        LOG_TRACE("false");
        return TSS2_FAPI_RC_BAD_VALUE;
    };

    r = ifapi_json_byte_deserialize(jso, hash_size, buffer, &size);
    return_if_error(r, "byte serialize");

    if (hash_size != size) {
        return_error(TSS2_FAPI_RC_BAD_VALUE, "Wrong size of digest.");
    }

    return TSS2_RC_SUCCESS;
}

static char *field_TPMT_HA_tab[] = {
    "hashAlg",
    "hashalg",
    "digest",
    "$schema"
};

/** Deserialize a TPMT_HA json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMT_HA_deserialize(json_object *jso,  TPMT_HA *out)
{
    json_object *jso2;
    TSS2_RC r;
    LOG_TRACE("call");
    return_if_null(out, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    ifapi_check_json_object_fields(jso, &field_TPMT_HA_tab[0],
                                   SIZE_OF_ARY(field_TPMT_HA_tab));
    if (!ifapi_get_sub_object(jso, "hashAlg", &jso2)) {
        LOG_ERROR("Field \"hashAlg\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPMI_ALG_HASH_deserialize(jso2, &out->hashAlg);
    return_if_error(r, "Bad value for field \"hashAlg\".");
    if (out->hashAlg != TPM2_ALG_NULL) {
        if (!ifapi_get_sub_object(jso, "digest", &jso2)) {
            LOG_ERROR("Field \"digest\" not found.");
            return TSS2_FAPI_RC_BAD_VALUE;
        }
        r = ifapi_json_TPMU_HA_deserialize(out->hashAlg, jso2, &out->digest);
        return_if_error(r, "Bad value for field \"digest\".");
    }

    LOG_TRACE("true");
    return TSS2_RC_SUCCESS;
}

/** Deserialize a TPM2B_DIGEST json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPM2B_DIGEST_deserialize(json_object *jso,  TPM2B_DIGEST *out)
{
    TSS2_RC r;
    LOG_TRACE("call");
    return_if_null(out, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    UINT16 size = 0;
    r = ifapi_json_byte_deserialize(jso, sizeof(TPMU_HA), (BYTE *)&out->buffer,
                                     &size);
    return_if_error(r, "byte serialize");

    out->size = size;
    return r;
    LOG_TRACE("true");
    return TSS2_RC_SUCCESS;
}

/** Deserialize a TPM2B_DATA json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPM2B_DATA_deserialize(json_object *jso,  TPM2B_DATA *out)
{
    TSS2_RC r;
    LOG_TRACE("call");
    return_if_null(out, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    UINT16 size = 0;
    r = ifapi_json_byte_deserialize(jso, sizeof(TPMT_HA), (BYTE *)&out->buffer,
                                     &size);
    return_if_error(r, "byte serialize");

    out->size = size;
    return r;
    LOG_TRACE("true");
    return TSS2_RC_SUCCESS;
}

/*** Table 75 - Definition of Types for TPM2B_NONCE ***/

/** Deserialize a TPM2B_NONCE json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPM2B_NONCE_deserialize(json_object *jso, TPM2B_NONCE *out)
{
    LOG_TRACE("call");
    return ifapi_json_TPM2B_DIGEST_deserialize(jso, out);
}

/*** Table 77 - Definition of Types for TPM2B_OPERAND ***/

/** Deserialize a TPM2B_OPERAND json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPM2B_OPERAND_deserialize(json_object *jso, TPM2B_OPERAND *out)
{
    LOG_TRACE("call");
    return ifapi_json_TPM2B_DIGEST_deserialize(jso, out);
}

/** Deserialize a TPM2B_EVENT json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPM2B_EVENT_deserialize(json_object *jso,  TPM2B_EVENT *out)
{
    TSS2_RC r;
    LOG_TRACE("call");
    return_if_null(out, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    UINT16 size = 0;
    r = ifapi_json_byte_deserialize(jso, 1024, (BYTE *)&out->buffer, &size);
    return_if_error(r, "byte serialize");

    out->size = size;
    return r;
    LOG_TRACE("true");
    return TSS2_RC_SUCCESS;
}

/** Deserialize a TPM2B_MAX_NV_BUFFER json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPM2B_MAX_NV_BUFFER_deserialize(json_object *jso,
        TPM2B_MAX_NV_BUFFER *out)
{
    TSS2_RC r;
    LOG_TRACE("call");
    return_if_null(out, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    UINT16 size = 0;
    r = ifapi_json_byte_deserialize(jso, TPM2_MAX_NV_BUFFER_SIZE,
                                     (BYTE *)&out->buffer, &size);
    return_if_error(r, "byte serialize");

    out->size = size;
    return r;
    LOG_TRACE("true");
    return TSS2_RC_SUCCESS;
}

/** Deserialize a TPM2B_NAME json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPM2B_NAME_deserialize(json_object *jso,  TPM2B_NAME *out)
{
    TSS2_RC r;
    LOG_TRACE("call");
    return_if_null(out, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    UINT16 size = 0;
    r = ifapi_json_byte_deserialize(jso, sizeof(TPMU_NAME), (BYTE *)&out->name,
                                     &size);
    return_if_error(r, "byte serialize");

    out->size = size;
    return r;
    LOG_TRACE("true");
    return TSS2_RC_SUCCESS;
}

static char *field_TPMT_TK_CREATION_tab[] = {
    "tag",
    "hierarchy",
    "digest",
    "$schema"
};

/** Deserialize a TPMT_TK_CREATION json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMT_TK_CREATION_deserialize(json_object *jso,
                                        TPMT_TK_CREATION *out)
{
    json_object *jso2;
    TSS2_RC r;
    LOG_TRACE("call");
    return_if_null(out, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    ifapi_check_json_object_fields(jso, &field_TPMT_TK_CREATION_tab[0],
                                   SIZE_OF_ARY(field_TPMT_TK_CREATION_tab));
    if (!ifapi_get_sub_object(jso, "tag", &jso2)) {
        LOG_ERROR("Field \"tag\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPM2_ST_deserialize(jso2, &out->tag);
    return_if_error(r, "Bad value for field \"tag\".");
    if (out != NULL && out->tag != TPM2_ST_CREATION) {
        LOG_ERROR("BAD VALUE %zu != %zu", (size_t)out->tag, (size_t)TPM2_ST_CREATION);
    }

    if (!ifapi_get_sub_object(jso, "hierarchy", &jso2)) {
        LOG_ERROR("Field \"hierarchy\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPMI_RH_HIERARCHY_deserialize(jso2, &out->hierarchy);
    return_if_error(r, "Bad value for field \"hierarchy\".");

    if (!ifapi_get_sub_object(jso, "digest", &jso2)) {
        LOG_ERROR("Field \"digest\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPM2B_DIGEST_deserialize(jso2, &out->digest);
    return_if_error(r, "Bad value for field \"digest\".");
    LOG_TRACE("true");
    return TSS2_RC_SUCCESS;
}

/** Deserialize a TPML_DIGEST_VALUES json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPML_DIGEST_VALUES_deserialize(json_object *jso,
        TPML_DIGEST_VALUES *out)
{
    TSS2_RC r;
    LOG_TRACE("call");
    return_if_null(out, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    json_type jso_type = json_object_get_type(jso);
    if (jso_type == json_type_array) {
        if (json_object_array_length(jso) > (int)TPM2_NUM_PCR_BANKS) {
            /* Cast (size_t) is necessary to support older version of libjson-c */
            LOG_ERROR("Too many bytes for array (%zu > %zu)",
                      (size_t)json_object_array_length(jso), (size_t)TPM2_NUM_PCR_BANKS);
            return TSS2_FAPI_RC_BAD_VALUE;
        }
        out->count = json_object_array_length(jso);
        size_t i;
        /* Cast (size_t) is necessary to support older version of libjson-c */
        for (i = 0; i < (size_t)json_object_array_length(jso); i++) {
            json_object *jso3 = json_object_array_get_idx(jso, i);
            r = ifapi_json_TPMT_HA_deserialize(jso3, &out->digests[i]);
            return_if_error(r, "Bad value for field \"digests\".");
        }
        return TSS2_RC_SUCCESS;
    } else {
        LOG_ERROR("BAD VALUE");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    LOG_TRACE("true");
    return TSS2_RC_SUCCESS;
}

/** Deserialize a TPML_PCR_SELECTION json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPML_PCR_SELECTION_deserialize(json_object *jso,
        TPML_PCR_SELECTION *out)
{
    TSS2_RC r;
    LOG_TRACE("call");
    return_if_null(out, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    json_type jso_type = json_object_get_type(jso);
    if (jso_type == json_type_array) {
        if (json_object_array_length(jso) > (int)TPM2_NUM_PCR_BANKS) {
            /* Cast (size_t) is necessary to support older version of libjson-c */
            LOG_ERROR("Too many bytes for array (%zu > %zu)",
                      (size_t)json_object_array_length(jso), (size_t)TPM2_NUM_PCR_BANKS);
            return TSS2_FAPI_RC_BAD_VALUE;
        }
        out->count = json_object_array_length(jso);
        size_t i;
        /* Cast (size_t) is necessary to support older version of libjson-c */
        for (i = 0; i < (size_t)json_object_array_length(jso); i++) {
            json_object *jso3 = json_object_array_get_idx(jso, i);
            r = ifapi_json_TPMS_PCR_SELECTION_deserialize(jso3, &out->pcrSelections[i]);
            return_if_error(r, "Bad value for field \"pcrSelections\".");
        }
        return TSS2_RC_SUCCESS;
    } else {
        LOG_ERROR("BAD VALUE");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    LOG_TRACE("true");
    return TSS2_RC_SUCCESS;
}

static char *field_TPMS_CLOCK_INFO_tab[] = {
    "clock",
    "resetCount",
    "resetcount",
    "restartCount",
    "restartcount",
    "safe",
    "$schema"
};

/** Deserialize a TPMS_CLOCK_INFO json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_CLOCK_INFO_deserialize(json_object *jso,  TPMS_CLOCK_INFO *out)
{
    json_object *jso2;
    TSS2_RC r;
    LOG_TRACE("call");
    return_if_null(out, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    ifapi_check_json_object_fields(jso, &field_TPMS_CLOCK_INFO_tab[0],
                                   SIZE_OF_ARY(field_TPMS_CLOCK_INFO_tab));
    if (!ifapi_get_sub_object(jso, "clock", &jso2)) {
        LOG_ERROR("Field \"clock\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_UINT64_deserialize(jso2, &out->clock);
    return_if_error(r, "Bad value for field \"clock\".");

    if (!ifapi_get_sub_object(jso, "resetCount", &jso2)) {
        LOG_ERROR("Field \"resetCount\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_UINT32_deserialize(jso2, &out->resetCount);
    return_if_error(r, "Bad value for field \"resetCount\".");

    if (!ifapi_get_sub_object(jso, "restartCount", &jso2)) {
        LOG_ERROR("Field \"restartCount\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_UINT32_deserialize(jso2, &out->restartCount);
    return_if_error(r, "Bad value for field \"restartCount\".");

    if (!ifapi_get_sub_object(jso, "safe", &jso2)) {
        LOG_ERROR("Field \"safe\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPMI_YES_NO_deserialize(jso2, &out->safe);
    return_if_error(r, "Bad value for field \"safe\".");
    LOG_TRACE("true");
    return TSS2_RC_SUCCESS;
}

static char *field_TPMS_TIME_INFO_tab[] = {
    "time",
    "clockInfo",
    "clockinfo",
    "$schema"
};

/** Deserialize a TPMS_TIME_INFO json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_TIME_INFO_deserialize(json_object *jso,  TPMS_TIME_INFO *out)
{
    json_object *jso2;
    TSS2_RC r;
    LOG_TRACE("call");
    return_if_null(out, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    ifapi_check_json_object_fields(jso, &field_TPMS_TIME_INFO_tab[0],
                                   SIZE_OF_ARY(field_TPMS_TIME_INFO_tab));
    if (!ifapi_get_sub_object(jso, "time", &jso2)) {
        LOG_ERROR("Field \"time\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_UINT64_deserialize(jso2, &out->time);
    return_if_error(r, "Bad value for field \"time\".");

    if (!ifapi_get_sub_object(jso, "clockInfo", &jso2)) {
        LOG_ERROR("Field \"clockInfo\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPMS_CLOCK_INFO_deserialize(jso2, &out->clockInfo);
    return_if_error(r, "Bad value for field \"clockInfo\".");
    LOG_TRACE("true");
    return TSS2_RC_SUCCESS;
}

static char *field_TPMS_TIME_ATTEST_INFO_tab[] = {
    "time",
    "firmwareVersion",
    "firmwareversion",
    "$schema"
};

/** Deserialize a TPMS_TIME_ATTEST_INFO json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_TIME_ATTEST_INFO_deserialize(json_object *jso,
        TPMS_TIME_ATTEST_INFO *out)
{
    json_object *jso2;
    TSS2_RC r;
    LOG_TRACE("call");
    return_if_null(out, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    ifapi_check_json_object_fields(jso, &field_TPMS_TIME_ATTEST_INFO_tab[0],
                                   SIZE_OF_ARY(field_TPMS_TIME_ATTEST_INFO_tab));
    if (!ifapi_get_sub_object(jso, "time", &jso2)) {
        LOG_ERROR("Field \"time\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPMS_TIME_INFO_deserialize(jso2, &out->time);
    return_if_error(r, "Bad value for field \"time\".");

    if (!ifapi_get_sub_object(jso, "firmwareVersion", &jso2)) {
        LOG_ERROR("Field \"firmwareVersion\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_UINT64_deserialize(jso2, &out->firmwareVersion);
    return_if_error(r, "Bad value for field \"firmwareVersion\".");
    LOG_TRACE("true");
    return TSS2_RC_SUCCESS;
}

static char *field_TPMS_CERTIFY_INFO_tab[] = {
    "name",
    "qualifiedName",
    "qualifiedname",
    "$schema"
};

/** Deserialize a TPMS_CERTIFY_INFO json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_CERTIFY_INFO_deserialize(json_object *jso,
        TPMS_CERTIFY_INFO *out)
{
    json_object *jso2;
    TSS2_RC r;
    LOG_TRACE("call");
    return_if_null(out, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    ifapi_check_json_object_fields(jso, &field_TPMS_CERTIFY_INFO_tab[0],
                                   SIZE_OF_ARY(field_TPMS_CERTIFY_INFO_tab));
    if (!ifapi_get_sub_object(jso, "name", &jso2)) {
        LOG_ERROR("Field \"name\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPM2B_NAME_deserialize(jso2, &out->name);
    return_if_error(r, "Bad value for field \"name\".");

    if (!ifapi_get_sub_object(jso, "qualifiedName", &jso2)) {
        LOG_ERROR("Field \"qualifiedName\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPM2B_NAME_deserialize(jso2, &out->qualifiedName);
    return_if_error(r, "Bad value for field \"qualifiedName\".");
    LOG_TRACE("true");
    return TSS2_RC_SUCCESS;
}

static char *field_TPMS_QUOTE_INFO_tab[] = {
    "pcrSelect",
    "pcrselect",
    "pcrDigest",
    "pcrdigest",
    "$schema"
};

/** Deserialize a TPMS_QUOTE_INFO json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_QUOTE_INFO_deserialize(json_object *jso,  TPMS_QUOTE_INFO *out)
{
    json_object *jso2;
    TSS2_RC r;
    LOG_TRACE("call");
    return_if_null(out, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    ifapi_check_json_object_fields(jso, &field_TPMS_QUOTE_INFO_tab[0],
                                   SIZE_OF_ARY(field_TPMS_QUOTE_INFO_tab));
    if (!ifapi_get_sub_object(jso, "pcrSelect", &jso2)) {
        LOG_ERROR("Field \"pcrSelect\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPML_PCR_SELECTION_deserialize(jso2, &out->pcrSelect);
    return_if_error(r, "Bad value for field \"pcrSelect\".");

    if (!ifapi_get_sub_object(jso, "pcrDigest", &jso2)) {
        LOG_ERROR("Field \"pcrDigest\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPM2B_DIGEST_deserialize(jso2, &out->pcrDigest);
    return_if_error(r, "Bad value for field \"pcrDigest\".");
    LOG_TRACE("true");
    return TSS2_RC_SUCCESS;
}

static char *field_TPMS_COMMAND_AUDIT_INFO_tab[] = {
    "auditCounter",
    "auditcounter",
    "digestAlg",
    "digestalg",
    "auditDigest",
    "auditdigest",
    "commandDigest",
    "commanddigest",
    "$schema"
};

/** Deserialize a TPMS_COMMAND_AUDIT_INFO json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_COMMAND_AUDIT_INFO_deserialize(json_object *jso,
        TPMS_COMMAND_AUDIT_INFO *out)
{
    json_object *jso2;
    TSS2_RC r;
    LOG_TRACE("call");
    return_if_null(out, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    ifapi_check_json_object_fields(jso, &field_TPMS_COMMAND_AUDIT_INFO_tab[0],
                                   SIZE_OF_ARY(field_TPMS_COMMAND_AUDIT_INFO_tab));
    if (!ifapi_get_sub_object(jso, "auditCounter", &jso2)) {
        LOG_ERROR("Field \"auditCounter\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_UINT64_deserialize(jso2, &out->auditCounter);
    return_if_error(r, "Bad value for field \"auditCounter\".");

    if (!ifapi_get_sub_object(jso, "digestAlg", &jso2)) {
        LOG_ERROR("Field \"digestAlg\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPM2_ALG_ID_deserialize(jso2, &out->digestAlg);
    return_if_error(r, "Bad value for field \"digestAlg\".");

    if (!ifapi_get_sub_object(jso, "auditDigest", &jso2)) {
        LOG_ERROR("Field \"auditDigest\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPM2B_DIGEST_deserialize(jso2, &out->auditDigest);
    return_if_error(r, "Bad value for field \"auditDigest\".");

    if (!ifapi_get_sub_object(jso, "commandDigest", &jso2)) {
        LOG_ERROR("Field \"commandDigest\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPM2B_DIGEST_deserialize(jso2, &out->commandDigest);
    return_if_error(r, "Bad value for field \"commandDigest\".");
    LOG_TRACE("true");
    return TSS2_RC_SUCCESS;
}

static char *field_TPMS_SESSION_AUDIT_INFO_tab[] = {
    "exclusiveSession",
    "exclusivesession",
    "sessionDigest",
    "sessiondigest",
    "$schema"
};

/** Deserialize a TPMS_SESSION_AUDIT_INFO json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_SESSION_AUDIT_INFO_deserialize(json_object *jso,
        TPMS_SESSION_AUDIT_INFO *out)
{
    json_object *jso2;
    TSS2_RC r;
    LOG_TRACE("call");
    return_if_null(out, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    ifapi_check_json_object_fields(jso, &field_TPMS_SESSION_AUDIT_INFO_tab[0],
                                   SIZE_OF_ARY(field_TPMS_SESSION_AUDIT_INFO_tab));
    if (!ifapi_get_sub_object(jso, "exclusiveSession", &jso2)) {
        LOG_ERROR("Field \"exclusiveSession\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPMI_YES_NO_deserialize(jso2, &out->exclusiveSession);
    return_if_error(r, "Bad value for field \"exclusiveSession\".");

    if (!ifapi_get_sub_object(jso, "sessionDigest", &jso2)) {
        LOG_ERROR("Field \"sessionDigest\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPM2B_DIGEST_deserialize(jso2, &out->sessionDigest);
    return_if_error(r, "Bad value for field \"sessionDigest\".");
    LOG_TRACE("true");
    return TSS2_RC_SUCCESS;
}

static char *field_TPMS_CREATION_INFO_tab[] = {
    "objectName",
    "objectname",
    "creationHash",
    "creationhash",
    "$schema"
};

/** Deserialize a TPMS_CREATION_INFO json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_CREATION_INFO_deserialize(json_object *jso,
        TPMS_CREATION_INFO *out)
{
    json_object *jso2;
    TSS2_RC r;
    LOG_TRACE("call");
    return_if_null(out, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    ifapi_check_json_object_fields(jso, &field_TPMS_CREATION_INFO_tab[0],
                                   SIZE_OF_ARY(field_TPMS_CREATION_INFO_tab));
    if (!ifapi_get_sub_object(jso, "objectName", &jso2)) {
        LOG_ERROR("Field \"objectName\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPM2B_NAME_deserialize(jso2, &out->objectName);
    return_if_error(r, "Bad value for field \"objectName\".");

    if (!ifapi_get_sub_object(jso, "creationHash", &jso2)) {
        LOG_ERROR("Field \"creationHash\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPM2B_DIGEST_deserialize(jso2, &out->creationHash);
    return_if_error(r, "Bad value for field \"creationHash\".");
    LOG_TRACE("true");
    return TSS2_RC_SUCCESS;
}

static char *field_TPMS_NV_CERTIFY_INFO_tab[] = {
    "indexName",
    "indexname",
    "offset",
    "nvContents",
    "nvcontents",
    "$schema"
};

/** Deserialize a TPMS_NV_CERTIFY_INFO json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_NV_CERTIFY_INFO_deserialize(json_object *jso,
        TPMS_NV_CERTIFY_INFO *out)
{
    json_object *jso2;
    TSS2_RC r;
    LOG_TRACE("call");
    return_if_null(out, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    ifapi_check_json_object_fields(jso, &field_TPMS_NV_CERTIFY_INFO_tab[0],
                                   SIZE_OF_ARY(field_TPMS_NV_CERTIFY_INFO_tab));
    if (!ifapi_get_sub_object(jso, "indexName", &jso2)) {
        LOG_ERROR("Field \"indexName\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPM2B_NAME_deserialize(jso2, &out->indexName);
    return_if_error(r, "Bad value for field \"indexName\".");

    if (!ifapi_get_sub_object(jso, "offset", &jso2)) {
        LOG_ERROR("Field \"offset\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_UINT16_deserialize(jso2, &out->offset);
    return_if_error(r, "Bad value for field \"offset\".");

    if (!ifapi_get_sub_object(jso, "nvContents", &jso2)) {
        LOG_ERROR("Field \"nvContents\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPM2B_MAX_NV_BUFFER_deserialize(jso2, &out->nvContents);
    return_if_error(r, "Bad value for field \"nvContents\".");
    LOG_TRACE("true");
    return TSS2_RC_SUCCESS;
}

/** Deserialize a TPMI_ST_ATTEST json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 */
TSS2_RC
ifapi_json_TPMI_ST_ATTEST_deserialize(json_object *jso, TPMI_ST_ATTEST *out)
{
    SUBTYPE_FILTER(TPMI_ST_ATTEST, TPM2_ST,
        TPM2_ST_ATTEST_CERTIFY, TPM2_ST_ATTEST_QUOTE, TPM2_ST_ATTEST_SESSION_AUDIT,
        TPM2_ST_ATTEST_COMMAND_AUDIT, TPM2_ST_ATTEST_TIME, TPM2_ST_ATTEST_CREATION,
        TPM2_ST_ATTEST_NV);
}

/** Deserialize a TPMU_ATTEST json object.
 *
 * This functions expects the Bitfield to be encoded as unsigned int in host-endianess.
 * @param[in]  selector The type the attest.
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMU_ATTEST_deserialize(
    UINT32 selector,
    json_object *jso,
    TPMU_ATTEST *out)
{
    LOG_TRACE("call");
    switch (selector) {
    case TPM2_ST_ATTEST_CERTIFY:
        return ifapi_json_TPMS_CERTIFY_INFO_deserialize(jso, &out->certify);
    case TPM2_ST_ATTEST_CREATION:
        return ifapi_json_TPMS_CREATION_INFO_deserialize(jso, &out->creation);
    case TPM2_ST_ATTEST_QUOTE:
        return ifapi_json_TPMS_QUOTE_INFO_deserialize(jso, &out->quote);
    case TPM2_ST_ATTEST_COMMAND_AUDIT:
        return ifapi_json_TPMS_COMMAND_AUDIT_INFO_deserialize(jso, &out->commandAudit);
    case TPM2_ST_ATTEST_SESSION_AUDIT:
        return ifapi_json_TPMS_SESSION_AUDIT_INFO_deserialize(jso, &out->sessionAudit);
    case TPM2_ST_ATTEST_TIME:
        return ifapi_json_TPMS_TIME_ATTEST_INFO_deserialize(jso, &out->time);
    case TPM2_ST_ATTEST_NV:
        return ifapi_json_TPMS_NV_CERTIFY_INFO_deserialize(jso, &out->nv);
    default:
        LOG_TRACE("false");
        return TSS2_FAPI_RC_BAD_VALUE;
    };
}

static char *field_TPMS_ATTEST_tab[] = {
    "magic",
    "type",
    "qualifiedSigner",
    "qualifiedsigner",
    "extraData",
    "extradata",
    "clockInfo",
    "clockinfo",
    "firmwareVersion",
    "firmwareversion",
    "attested",
    "$schema"
};

/** Deserialize a TPMS_ATTEST json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_ATTEST_deserialize(json_object *jso,  TPMS_ATTEST *out)
{
    json_object *jso2;
    TSS2_RC r;
    LOG_TRACE("call");
    return_if_null(out, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    ifapi_check_json_object_fields(jso, &field_TPMS_ATTEST_tab[0],
                                   SIZE_OF_ARY(field_TPMS_ATTEST_tab));
    if (!ifapi_get_sub_object(jso, "magic", &jso2)) {
        LOG_ERROR("Field \"magic\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPM2_GENERATED_deserialize(jso2, &out->magic);
    return_if_error(r, "Bad value for field \"magic\".");

    if (!ifapi_get_sub_object(jso, "type", &jso2)) {
        LOG_ERROR("Field \"type\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPMI_ST_ATTEST_deserialize(jso2, &out->type);
    return_if_error(r, "Bad value for field \"type\".");

    if (!ifapi_get_sub_object(jso, "qualifiedSigner", &jso2)) {
        LOG_ERROR("Field \"qualifiedSigner\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPM2B_NAME_deserialize(jso2, &out->qualifiedSigner);
    return_if_error(r, "Bad value for field \"qualifiedSigner\".");

    if (!ifapi_get_sub_object(jso, "extraData", &jso2)) {
        LOG_ERROR("Field \"extraData\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPM2B_DATA_deserialize(jso2, &out->extraData);
    return_if_error(r, "Bad value for field \"extraData\".");

    if (!ifapi_get_sub_object(jso, "clockInfo", &jso2)) {
        LOG_ERROR("Field \"clockInfo\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPMS_CLOCK_INFO_deserialize(jso2, &out->clockInfo);
    return_if_error(r, "Bad value for field \"clockInfo\".");

    if (!ifapi_get_sub_object(jso, "firmwareVersion", &jso2)) {
        LOG_ERROR("Field \"firmwareVersion\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_UINT64_deserialize(jso2, &out->firmwareVersion);
    return_if_error(r, "Bad value for field \"firmwareVersion\".");
    if (!ifapi_get_sub_object(jso, "attested", &jso2)) {
        LOG_ERROR("Field \"attested\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPMU_ATTEST_deserialize(out->type, jso2, &out->attested);
    return_if_error(r, "Bad value for field \"attested\".");

    LOG_TRACE("true");
    return TSS2_RC_SUCCESS;
}

/** Deserialize a TPMI_AES_KEY_BITS json object.
 *
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 */
TSS2_RC
ifapi_json_TPMI_AES_KEY_BITS_deserialize(json_object *jso, TPMI_AES_KEY_BITS *out)
{
    SUBTYPE_FILTER(TPMI_AES_KEY_BITS, UINT16,
        128, 192, 256);
}

/** Deserialize a TPMI_CAMELLIA_KEY_BITS json object.
 *
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 */
TSS2_RC
ifapi_json_TPMI_CAMELLIA_KEY_BITS_deserialize(json_object *jso, TPMI_CAMELLIA_KEY_BITS *out)
{
    SUBTYPE_FILTER(TPMI_CAMELLIA_KEY_BITS, UINT16,
        128, 192, 256);
}

/** Deserialize a TPMI_SM4_KEY_BITS json object.
 *
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 */
TSS2_RC
ifapi_json_TPMI_SM4_KEY_BITS_deserialize(json_object *jso, TPMI_SM4_KEY_BITS *out)
{
    SUBTYPE_FILTER(TPMI_SM4_KEY_BITS, UINT16, 128);
}

/** Deserialize a TPMU_SYM_KEY_BITS json object.
 *
 * This functions expects the Bitfield to be encoded as unsigned int in host-endianess.
 * @param[in]  selector The type the symmetric algorithm.
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 */
TSS2_RC
ifapi_json_TPMU_SYM_KEY_BITS_deserialize(
    UINT32 selector,
    json_object *jso,
    TPMU_SYM_KEY_BITS *out)
{
    LOG_TRACE("call");
    switch (selector) {
    case TPM2_ALG_AES:
        return ifapi_json_TPMI_AES_KEY_BITS_deserialize(jso, &out->aes);
    case TPM2_ALG_XOR:
        return ifapi_json_TPMI_ALG_HASH_deserialize(jso, &out->exclusiveOr);
    case TPM2_ALG_SM4:
        return ifapi_json_TPMI_SM4_KEY_BITS_deserialize(jso, &out->sm4);
    case TPM2_ALG_CAMELLIA:
        return ifapi_json_TPMI_CAMELLIA_KEY_BITS_deserialize(jso, &out->camellia);
    case TPM2_ALG_NULL: {
            return TSS2_RC_SUCCESS;
        }
    default:
        LOG_TRACE("false");
        return TSS2_FAPI_RC_BAD_VALUE;
    };
}

/** Deserialize a TPMU_SYM_MODE json object.
 *
 * This functions expects the Bitfield to be encoded as unsigned int in host-endianess.
 * @param[in]  selector The type the symmetric algorithm.
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 */
TSS2_RC
ifapi_json_TPMU_SYM_MODE_deserialize(
    UINT32 selector,
    json_object *jso,
    TPMU_SYM_MODE *out)
{
    LOG_TRACE("call");
    switch (selector) {
    case TPM2_ALG_SM4:
    case TPM2_ALG_AES:
    case TPM2_ALG_CAMELLIA:
        return ifapi_json_TPMI_ALG_SYM_MODE_deserialize(jso, &out->aes);

    case TPM2_ALG_NULL: {
            return TSS2_RC_SUCCESS;
        }
    default:
        LOG_TRACE("false");
        return TSS2_FAPI_RC_BAD_VALUE;
    };
}

static char *field_TPMT_SYM_DEF_tab[] = {
    "algorithm",
    "keyBits",
    "keybits",
    "mode",
    "$schema"
};

/** Deserialize a TPMT_SYM_DEF json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMT_SYM_DEF_deserialize(json_object *jso,  TPMT_SYM_DEF *out)
{
    json_object *jso2;
    TSS2_RC r;
    LOG_TRACE("call");
    return_if_null(out, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    ifapi_check_json_object_fields(jso, &field_TPMT_SYM_DEF_tab[0],
                                   SIZE_OF_ARY(field_TPMT_SYM_DEF_tab));
    if (!ifapi_get_sub_object(jso, "algorithm", &jso2)) {
        LOG_ERROR("Field \"algorithm\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPMI_ALG_SYM_deserialize(jso2, &out->algorithm);
    return_if_error(r, "Bad value for field \"algorithm\".");
    if (out->algorithm != TPM2_ALG_NULL) {
        if (!ifapi_get_sub_object(jso, "keyBits", &jso2)) {
            LOG_ERROR("Field \"keyBits\" not found.");
            return TSS2_FAPI_RC_BAD_VALUE;
        }
        r = ifapi_json_TPMU_SYM_KEY_BITS_deserialize(out->algorithm, jso2,
                &out->keyBits);
        return_if_error(r, "Bad value for field \"keyBits\".");
    }

    if (out->algorithm != TPM2_ALG_NULL) {
        if (!ifapi_get_sub_object(jso, "mode", &jso2)) {
            LOG_ERROR("Field \"mode\" not found.");
            return TSS2_FAPI_RC_BAD_VALUE;
        }
        r = ifapi_json_TPMU_SYM_MODE_deserialize(out->algorithm, jso2, &out->mode);
        return_if_error(r, "Bad value for field \"mode\".");
    }

    LOG_TRACE("true");
    return TSS2_RC_SUCCESS;
}

static char *field_TPMT_SYM_DEF_OBJECT_tab[] = {
    "algorithm",
    "keyBits",
    "keybits",
    "mode",
    "$schema"
};

/** Deserialize a TPMT_SYM_DEF_OBJECT json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMT_SYM_DEF_OBJECT_deserialize(json_object *jso,
        TPMT_SYM_DEF_OBJECT *out)
{
    json_object *jso2;
    TSS2_RC r;
    LOG_TRACE("call");
    return_if_null(out, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    ifapi_check_json_object_fields(jso, &field_TPMT_SYM_DEF_OBJECT_tab[0],
                                   SIZE_OF_ARY(field_TPMT_SYM_DEF_OBJECT_tab));
    if (!ifapi_get_sub_object(jso, "algorithm", &jso2)) {
        LOG_ERROR("Field \"algorithm\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPMI_ALG_SYM_OBJECT_deserialize(jso2, &out->algorithm);
    return_if_error(r, "Bad value for field \"algorithm\".");
    if (out->algorithm != TPM2_ALG_NULL) {
        if (!ifapi_get_sub_object(jso, "keyBits", &jso2)) {
            LOG_ERROR("Field \"keyBits\" not found.");
            return TSS2_FAPI_RC_BAD_VALUE;
        }
        r = ifapi_json_TPMU_SYM_KEY_BITS_deserialize(out->algorithm, jso2,
                &out->keyBits);
        return_if_error(r, "Bad value for field \"keyBits\".");
    }

    if (out->algorithm != TPM2_ALG_NULL) {
        if (!ifapi_get_sub_object(jso, "mode", &jso2)) {
            LOG_ERROR("Field \"mode\" not found.");
            return TSS2_FAPI_RC_BAD_VALUE;
        }
        r = ifapi_json_TPMU_SYM_MODE_deserialize(out->algorithm, jso2, &out->mode);
        return_if_error(r, "Bad value for field \"mode\".");
    }

    LOG_TRACE("true");
    return TSS2_RC_SUCCESS;
}

static char *field_TPMS_SYMCIPHER_PARMS_tab[] = {
    "sym",
    "$schema"
};

/** Deserialize a TPMS_SYMCIPHER_PARMS json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_SYMCIPHER_PARMS_deserialize(json_object *jso,
        TPMS_SYMCIPHER_PARMS *out)
{
    json_object *jso2;
    TSS2_RC r;
    LOG_TRACE("call");
    return_if_null(out, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    ifapi_check_json_object_fields(jso, &field_TPMS_SYMCIPHER_PARMS_tab[0],
                                   SIZE_OF_ARY(field_TPMS_SYMCIPHER_PARMS_tab));
    if (!ifapi_get_sub_object(jso, "sym", &jso2)) {
        LOG_ERROR("Field \"sym\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPMT_SYM_DEF_OBJECT_deserialize(jso2, &out->sym);
    return_if_error(r, "Bad value for field \"sym\".");
    LOG_TRACE("true");
    return TSS2_RC_SUCCESS;
}

static char *field_TPMS_SCHEME_HASH_tab[] = {
    "hashAlg",
    "hashalg",
    "$schema"
};

/** Deserialize a TPMS_SCHEME_HASH json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_SCHEME_HASH_deserialize(json_object *jso,
                                        TPMS_SCHEME_HASH *out)
{
    json_object *jso2;
    TSS2_RC r;
    LOG_TRACE("call");
    return_if_null(out, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    ifapi_check_json_object_fields(jso, &field_TPMS_SCHEME_HASH_tab[0],
                                   SIZE_OF_ARY(field_TPMS_SCHEME_HASH_tab));
    if (!ifapi_get_sub_object(jso, "hashAlg", &jso2)) {
        LOG_ERROR("Field \"hashAlg\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPMI_ALG_HASH_deserialize(jso2, &out->hashAlg);
    return_if_error(r, "Bad value for field \"hashAlg\".");
    LOG_TRACE("true");
    return TSS2_RC_SUCCESS;
}

static char *field_TPMS_SCHEME_ECDAA_tab[] = {
    "hashAlg",
    "hashalg",
    "count",
    "$schema"
};

/** Deserialize a TPMS_SCHEME_ECDAA json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_SCHEME_ECDAA_deserialize(json_object *jso,
        TPMS_SCHEME_ECDAA *out)
{
    json_object *jso2;
    TSS2_RC r;
    LOG_TRACE("call");
    return_if_null(out, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    ifapi_check_json_object_fields(jso, &field_TPMS_SCHEME_ECDAA_tab[0],
                                   SIZE_OF_ARY(field_TPMS_SCHEME_ECDAA_tab));
    if (!ifapi_get_sub_object(jso, "hashAlg", &jso2)) {
        LOG_ERROR("Field \"hashAlg\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPMI_ALG_HASH_deserialize(jso2, &out->hashAlg);
    return_if_error(r, "Bad value for field \"hashAlg\".");

    if (!ifapi_get_sub_object(jso, "count", &jso2)) {
        LOG_ERROR("Field \"count\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_UINT16_deserialize(jso2, &out->count);
    return_if_error(r, "Bad value for field \"count\".");
    LOG_TRACE("true");
    return TSS2_RC_SUCCESS;
}

/** Deserialize a TPMI_ALG_KEYEDHASH_SCHEME json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 */
TSS2_RC
ifapi_json_TPMI_ALG_KEYEDHASH_SCHEME_deserialize(json_object *jso,
        TPMI_ALG_KEYEDHASH_SCHEME *out)
{
    SUBTYPE_FILTER(TPMI_ALG_KEYEDHASH_SCHEME, TPM2_ALG_ID,
        TPM2_ALG_HMAC, TPM2_ALG_XOR, TPM2_ALG_NULL);
}

/*** Table 144 - Definition of Types for HMAC_SIG_SCHEME ***/

/** Deserialize a TPMS_SCHEME_HMAC json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_SCHEME_HMAC_deserialize(json_object *jso, TPMS_SCHEME_HMAC *out)
{
    LOG_TRACE("call");
    return ifapi_json_TPMS_SCHEME_HASH_deserialize(jso, out);
}

static char *field_TPMS_SCHEME_XOR_tab[] = {
    "hashAlg",
    "hashalg",
    "kdf",
    "$schema"
};

/** Deserialize a TPMS_SCHEME_XOR json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_SCHEME_XOR_deserialize(json_object *jso,  TPMS_SCHEME_XOR *out)
{
    json_object *jso2;
    TSS2_RC r;
    LOG_TRACE("call");
    return_if_null(out, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    ifapi_check_json_object_fields(jso, &field_TPMS_SCHEME_XOR_tab[0],
                                   SIZE_OF_ARY(field_TPMS_SCHEME_XOR_tab));
    if (!ifapi_get_sub_object(jso, "hashAlg", &jso2)) {
        LOG_ERROR("Field \"hashAlg\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPMI_ALG_HASH_deserialize(jso2, &out->hashAlg);
    return_if_error(r, "Bad value for field \"hashAlg\".");

    if (!ifapi_get_sub_object(jso, "kdf", &jso2)) {
        LOG_ERROR("Field \"kdf\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPMI_ALG_KDF_deserialize(jso2, &out->kdf);
    return_if_error(r, "Bad value for field \"kdf\".");
    LOG_TRACE("true");
    return TSS2_RC_SUCCESS;
}

/** Deserialize a TPMU_SCHEME_KEYEDHASH json object.
 *
 * This functions expects the Bitfield to be encoded as unsigned int in host-endianess.
 * @param[in]  selector The type the keyedhash scheme.
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMU_SCHEME_KEYEDHASH_deserialize(
    UINT32 selector,
    json_object *jso,
    TPMU_SCHEME_KEYEDHASH *out)
{
    LOG_TRACE("call");
    switch (selector) {
    case TPM2_ALG_HMAC:
        return ifapi_json_TPMS_SCHEME_HMAC_deserialize(jso, &out->hmac);
    case TPM2_ALG_XOR:
        return ifapi_json_TPMS_SCHEME_XOR_deserialize(jso, &out->exclusiveOr);

    case TPM2_ALG_NULL: {
            return TSS2_RC_SUCCESS;
        }
    default:
        LOG_TRACE("false");
        return TSS2_FAPI_RC_BAD_VALUE;
    };
}

static char *field_TPMT_KEYEDHASH_SCHEME_tab[] = {
    "scheme",
    "details",
    "$schema"
};

/** Deserialize a TPMT_KEYEDHASH_SCHEME json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMT_KEYEDHASH_SCHEME_deserialize(json_object *jso,
        TPMT_KEYEDHASH_SCHEME *out)
{
    json_object *jso2;
    TSS2_RC r;
    LOG_TRACE("call");
    return_if_null(out, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    ifapi_check_json_object_fields(jso, &field_TPMT_KEYEDHASH_SCHEME_tab[0],
                                   SIZE_OF_ARY(field_TPMT_KEYEDHASH_SCHEME_tab));
    if (!ifapi_get_sub_object(jso, "scheme", &jso2)) {
        LOG_ERROR("Field \"scheme\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPMI_ALG_KEYEDHASH_SCHEME_deserialize(jso2, &out->scheme);
    return_if_error(r, "Bad value for field \"scheme\".");
    if (out->scheme != TPM2_ALG_NULL) {
        if (!ifapi_get_sub_object(jso, "details", &jso2)) {
            LOG_ERROR("Field \"details\" not found.");
            return TSS2_FAPI_RC_BAD_VALUE;
        }
        r = ifapi_json_TPMU_SCHEME_KEYEDHASH_deserialize(out->scheme, jso2,
                &out->details);
        return_if_error(r, "Bad value for field \"details\".");
    }

    LOG_TRACE("true");
    return TSS2_RC_SUCCESS;
}

/*** Table 148 - Definition of  Types for RSA Signature Schemes ***/

/** Deserialize a TPMS_SIG_SCHEME_RSASSA json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_SIG_SCHEME_RSASSA_deserialize(json_object *jso,
        TPMS_SIG_SCHEME_RSASSA *out)
{
    LOG_TRACE("call");
    return ifapi_json_TPMS_SCHEME_HASH_deserialize(jso, out);
}

/** Deserialize a TPMS_SIG_SCHEME_RSAPSS json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_SIG_SCHEME_RSAPSS_deserialize(json_object *jso,
        TPMS_SIG_SCHEME_RSAPSS *out)
{
    LOG_TRACE("call");
    return ifapi_json_TPMS_SCHEME_HASH_deserialize(jso, out);
}

/*** Table 149 - Definition of  Types for ECC Signature Schemes ***/

/** Deserialize a TPMS_SIG_SCHEME_ECDSA json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_SIG_SCHEME_ECDSA_deserialize(json_object *jso,
        TPMS_SIG_SCHEME_ECDSA *out)
{
    LOG_TRACE("call");
    return ifapi_json_TPMS_SCHEME_HASH_deserialize(jso, out);
}

/** Deserialize a TPMS_SIG_SCHEME_SM2 json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_SIG_SCHEME_SM2_deserialize(json_object *jso,
        TPMS_SIG_SCHEME_SM2 *out)
{
    LOG_TRACE("call");
    return ifapi_json_TPMS_SCHEME_HASH_deserialize(jso, out);
}

/** Deserialize a TPMS_SIG_SCHEME_ECSCHNORR json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_SIG_SCHEME_ECSCHNORR_deserialize(json_object *jso,
        TPMS_SIG_SCHEME_ECSCHNORR *out)
{
    LOG_TRACE("call");
    return ifapi_json_TPMS_SCHEME_HASH_deserialize(jso, out);
}

/** Deserialize a TPMS_SIG_SCHEME_ECDAA json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_SIG_SCHEME_ECDAA_deserialize(json_object *jso,
        TPMS_SIG_SCHEME_ECDAA *out)
{
    LOG_TRACE("call");
    return ifapi_json_TPMS_SCHEME_ECDAA_deserialize(jso, out);
}

/** Deserialize a TPMU_SIG_SCHEME json object.
 *
 * This functions expects the Bitfield to be encoded as unsigned int in host-endianess.
 * @param[in]  selector The type the signature scheme.
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMU_SIG_SCHEME_deserialize(
    UINT32 selector,
    json_object *jso,
    TPMU_SIG_SCHEME *out)
{
    LOG_TRACE("call");
    switch (selector) {
    case TPM2_ALG_RSASSA:
        return ifapi_json_TPMS_SIG_SCHEME_RSASSA_deserialize(jso, &out->rsassa);
    case TPM2_ALG_RSAPSS:
        return ifapi_json_TPMS_SIG_SCHEME_RSAPSS_deserialize(jso, &out->rsapss);
    case TPM2_ALG_ECDSA:
        return ifapi_json_TPMS_SIG_SCHEME_ECDSA_deserialize(jso, &out->ecdsa);
    case TPM2_ALG_ECDAA:
        return ifapi_json_TPMS_SIG_SCHEME_ECDAA_deserialize(jso, &out->ecdaa);
    case TPM2_ALG_SM2:
        return ifapi_json_TPMS_SIG_SCHEME_SM2_deserialize(jso, &out->sm2);
    case TPM2_ALG_ECSCHNORR:
        return ifapi_json_TPMS_SIG_SCHEME_ECSCHNORR_deserialize(jso, &out->ecschnorr);
    case TPM2_ALG_HMAC:
        return ifapi_json_TPMS_SCHEME_HMAC_deserialize(jso, &out->hmac);

    case TPM2_ALG_NULL: {
            return TSS2_RC_SUCCESS;
        }
    default:
        LOG_TRACE("false");
        return TSS2_FAPI_RC_BAD_VALUE;
    };
}

static char *field_TPMT_SIG_SCHEME_tab[] = {
    "scheme",
    "details",
    "$schema"
};

/** Deserialize a TPMT_SIG_SCHEME json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMT_SIG_SCHEME_deserialize(json_object *jso,  TPMT_SIG_SCHEME *out)
{
    json_object *jso2;
    TSS2_RC r;
    LOG_TRACE("call");
    return_if_null(out, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    ifapi_check_json_object_fields(jso, &field_TPMT_SIG_SCHEME_tab[0],
                                   SIZE_OF_ARY(field_TPMT_SIG_SCHEME_tab));
    if (!ifapi_get_sub_object(jso, "scheme", &jso2)) {
        LOG_ERROR("Field \"scheme\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPMI_ALG_SIG_SCHEME_deserialize(jso2, &out->scheme);
    return_if_error(r, "Bad value for field \"scheme\".");
    if (out->scheme != TPM2_ALG_NULL) {
        if (!ifapi_get_sub_object(jso, "details", &jso2)) {
            LOG_ERROR("Field \"details\" not found.");
            return TSS2_FAPI_RC_BAD_VALUE;
        }
        r = ifapi_json_TPMU_SIG_SCHEME_deserialize(out->scheme, jso2, &out->details);
        return_if_error(r, "Bad value for field \"details\".");
    }

    LOG_TRACE("true");
    return TSS2_RC_SUCCESS;
}

/*** Table 152 - Definition of Types for  Encryption Schemes ***/

/** Deserialize a TPMS_ENC_SCHEME_OAEP json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_ENC_SCHEME_OAEP_deserialize(json_object *jso,
        TPMS_ENC_SCHEME_OAEP *out)
{
    LOG_TRACE("call");
    return ifapi_json_TPMS_SCHEME_HASH_deserialize(jso, out);
}

/** Deserialize a TPMS_ENC_SCHEME_RSAES json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 */
TSS2_RC
ifapi_json_TPMS_ENC_SCHEME_RSAES_deserialize(json_object *jso,
        TPMS_ENC_SCHEME_RSAES *out)
{
    LOG_TRACE("call");
    return ifapi_json_TPMS_EMPTY_deserialize(jso, out);
}

/*** Table 153 - Definition of Types for  ECC Key Exchange ***/

/** Deserialize a TPMS_KEY_SCHEME_ECDH json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_KEY_SCHEME_ECDH_deserialize(json_object *jso,
        TPMS_KEY_SCHEME_ECDH *out)
{
    LOG_TRACE("call");
    return ifapi_json_TPMS_SCHEME_HASH_deserialize(jso, out);
}

/*** Table 154 - Definition of Types for KDF Schemes ***/

/** Deserialize a TPMS_SCHEME_MGF1 json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_SCHEME_MGF1_deserialize(json_object *jso, TPMS_SCHEME_MGF1 *out)
{
    LOG_TRACE("call");
    return ifapi_json_TPMS_SCHEME_HASH_deserialize(jso, out);
}

/** Deserialize a TPMS_SCHEME_KDF1_SP800_56A json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_SCHEME_KDF1_SP800_56A_deserialize(json_object *jso,
        TPMS_SCHEME_KDF1_SP800_56A *out)
{
    LOG_TRACE("call");
    return ifapi_json_TPMS_SCHEME_HASH_deserialize(jso, out);
}

/** Deserialize a TPMS_SCHEME_KDF1_SP800_108 json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_SCHEME_KDF1_SP800_108_deserialize(json_object *jso,
        TPMS_SCHEME_KDF1_SP800_108 *out)
{
    LOG_TRACE("call");
    return ifapi_json_TPMS_SCHEME_HASH_deserialize(jso, out);
}

/** Deserialize a TPMU_KDF_SCHEME json object.
 *
 * This functions expects the Bitfield to be encoded as unsigned int in host-endianess.
 * @param[in]  selector The type the KDF scheme.
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMU_KDF_SCHEME_deserialize(
    UINT32 selector,
    json_object *jso,
    TPMU_KDF_SCHEME *out)
{
    LOG_TRACE("call");
    switch (selector) {
    case TPM2_ALG_MGF1:
        return ifapi_json_TPMS_SCHEME_MGF1_deserialize(jso, &out->mgf1);
    case TPM2_ALG_KDF1_SP800_56A:
        return ifapi_json_TPMS_SCHEME_KDF1_SP800_56A_deserialize(jso,
                &out->kdf1_sp800_56a);
    case TPM2_ALG_KDF1_SP800_108:
        return ifapi_json_TPMS_SCHEME_KDF1_SP800_108_deserialize(jso,
                &out->kdf1_sp800_108);

    case TPM2_ALG_NULL: {
            return TSS2_RC_SUCCESS;
        }
    default:
        LOG_TRACE("false");
        return TSS2_FAPI_RC_BAD_VALUE;
    };
}

static char *field_TPMT_KDF_SCHEME_tab[] = {
    "scheme",
    "details",
    "$schema"
};

/** Deserialize a TPMT_KDF_SCHEME json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMT_KDF_SCHEME_deserialize(json_object *jso,  TPMT_KDF_SCHEME *out)
{
    json_object *jso2;
    TSS2_RC r;
    LOG_TRACE("call");
    return_if_null(out, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    ifapi_check_json_object_fields(jso, &field_TPMT_KDF_SCHEME_tab[0],
                                   SIZE_OF_ARY(field_TPMT_KDF_SCHEME_tab));
    if (!ifapi_get_sub_object(jso, "scheme", &jso2)) {
        LOG_ERROR("Field \"scheme\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPMI_ALG_KDF_deserialize(jso2, &out->scheme);
    return_if_error(r, "Bad value for field \"scheme\".");
    if (out->scheme != TPM2_ALG_NULL) {
        if (!ifapi_get_sub_object(jso, "details", &jso2)) {
            LOG_ERROR("Field \"details\" not found.");
            return TSS2_FAPI_RC_BAD_VALUE;
        }
        r = ifapi_json_TPMU_KDF_SCHEME_deserialize(out->scheme, jso2, &out->details);
        return_if_error(r, "Bad value for field \"details\".");
    }

    LOG_TRACE("true");
    return TSS2_RC_SUCCESS;
}

/** Deserialize a TPMU_ASYM_SCHEME json object.
 *
 * This functions expects the Bitfield to be encoded as unsigned int in host-endianess.
 * @param[in]  jso the json object to be deserialized.
 * @param[in]  selector The type the scheme.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMU_ASYM_SCHEME_deserialize(
    UINT32 selector,
    json_object *jso,
    TPMU_ASYM_SCHEME *out)
{
    LOG_TRACE("call");
    switch (selector) {
    case TPM2_ALG_ECDH:
        return ifapi_json_TPMS_KEY_SCHEME_ECDH_deserialize(jso, &out->ecdh);
    case TPM2_ALG_RSASSA:
        return ifapi_json_TPMS_SIG_SCHEME_RSASSA_deserialize(jso, &out->rsassa);
    case TPM2_ALG_RSAPSS:
        return ifapi_json_TPMS_SIG_SCHEME_RSAPSS_deserialize(jso, &out->rsapss);
    case TPM2_ALG_ECDSA:
        return ifapi_json_TPMS_SIG_SCHEME_ECDSA_deserialize(jso, &out->ecdsa);
    case TPM2_ALG_ECDAA:
        return ifapi_json_TPMS_SIG_SCHEME_ECDAA_deserialize(jso, &out->ecdaa);
    case TPM2_ALG_SM2:
        return ifapi_json_TPMS_SIG_SCHEME_SM2_deserialize(jso, &out->sm2);
    case TPM2_ALG_ECSCHNORR:
        return ifapi_json_TPMS_SIG_SCHEME_ECSCHNORR_deserialize(jso, &out->ecschnorr);
    case TPM2_ALG_RSAES:
        return ifapi_json_TPMS_ENC_SCHEME_RSAES_deserialize(jso, &out->rsaes);
    case TPM2_ALG_OAEP:
        return ifapi_json_TPMS_ENC_SCHEME_OAEP_deserialize(jso, &out->oaep);

    case TPM2_ALG_NULL: {
            return TSS2_RC_SUCCESS;
        }
    default:
        LOG_TRACE("false");
        return TSS2_FAPI_RC_BAD_VALUE;
    };
}

/** Deserialize a TPMI_ALG_RSA_SCHEME json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 */
TSS2_RC
ifapi_json_TPMI_ALG_RSA_SCHEME_deserialize(json_object *jso,
        TPMI_ALG_RSA_SCHEME *out)
{
    SUBTYPE_FILTER(TPMI_ALG_RSA_SCHEME, TPM2_ALG_ID,
        TPM2_ALG_RSAES, TPM2_ALG_OAEP, TPM2_ALG_RSASSA, TPM2_ALG_RSAPSS, TPM2_ALG_NULL);
}

static char *field_TPMT_RSA_SCHEME_tab[] = {
    "scheme",
    "details",
    "$schema"
};

/** Deserialize a TPMT_RSA_SCHEME json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMT_RSA_SCHEME_deserialize(json_object *jso,  TPMT_RSA_SCHEME *out)
{
    json_object *jso2;
    TSS2_RC r;
    LOG_TRACE("call");
    return_if_null(out, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    ifapi_check_json_object_fields(jso, &field_TPMT_RSA_SCHEME_tab[0],
                                   SIZE_OF_ARY(field_TPMT_RSA_SCHEME_tab));
    if (!ifapi_get_sub_object(jso, "scheme", &jso2)) {
        LOG_ERROR("Field \"scheme\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPMI_ALG_RSA_SCHEME_deserialize(jso2, &out->scheme);
    return_if_error(r, "Bad value for field \"scheme\".");
    if (out->scheme != TPM2_ALG_NULL) {
        if (!ifapi_get_sub_object(jso, "details", &jso2)) {
            LOG_ERROR("Field \"details\" not found.");
            return TSS2_FAPI_RC_BAD_VALUE;
        }
        r = ifapi_json_TPMU_ASYM_SCHEME_deserialize(out->scheme, jso2, &out->details);
        return_if_error(r, "Bad value for field \"details\".");
    }

    LOG_TRACE("true");
    return TSS2_RC_SUCCESS;
}

/** Deserialize a TPMI_ALG_RSA_DECRYPT json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 */
TSS2_RC
ifapi_json_TPMI_ALG_RSA_DECRYPT_deserialize(json_object *jso,
        TPMI_ALG_RSA_DECRYPT *out)
{
    SUBTYPE_FILTER(TPMI_ALG_RSA_DECRYPT, TPM2_ALG_ID,
        TPM2_ALG_RSAES, TPM2_ALG_OAEP, TPM2_ALG_NULL);
}

static char *field_TPMT_RSA_DECRYPT_tab[] = {
    "scheme",
    "details",
    "$schema"
};

/** Deserialize a TPMT_RSA_DECRYPT json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMT_RSA_DECRYPT_deserialize(json_object *jso,
                                        TPMT_RSA_DECRYPT *out)
{
    json_object *jso2;
    TSS2_RC r;
    LOG_TRACE("call");
    return_if_null(out, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    ifapi_check_json_object_fields(jso, &field_TPMT_RSA_DECRYPT_tab[0],
                                   SIZE_OF_ARY(field_TPMT_RSA_DECRYPT_tab));
    if (!ifapi_get_sub_object(jso, "scheme", &jso2)) {
        LOG_ERROR("Field \"scheme\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPMI_ALG_RSA_DECRYPT_deserialize(jso2, &out->scheme);
    return_if_error(r, "Bad value for field \"scheme\".");
    if (out->scheme != TPM2_ALG_NULL) {
        if (!ifapi_get_sub_object(jso, "details", &jso2)) {
            LOG_ERROR("Field \"details\" not found.");
            return TSS2_FAPI_RC_BAD_VALUE;
        }
        r = ifapi_json_TPMU_ASYM_SCHEME_deserialize(out->scheme, jso2, &out->details);
        return_if_error(r, "Bad value for field \"details\".");
    }

    LOG_TRACE("true");
    return TSS2_RC_SUCCESS;
}

/** Deserialize a TPM2B_PUBLIC_KEY_RSA json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPM2B_PUBLIC_KEY_RSA_deserialize(json_object *jso,
        TPM2B_PUBLIC_KEY_RSA *out)
{
    TSS2_RC r;
    LOG_TRACE("call");
    return_if_null(out, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    UINT16 size = 0;
    r = ifapi_json_byte_deserialize(jso, TPM2_MAX_RSA_KEY_BYTES,
                                     (BYTE *)&out->buffer, &size);
    return_if_error(r, "byte serialize");

    out->size = size;
    return r;
    LOG_TRACE("true");
    return TSS2_RC_SUCCESS;
}

/** Deserialize a TPMI_RSA_KEY_BITS json object.
 *
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 */
TSS2_RC
ifapi_json_TPMI_RSA_KEY_BITS_deserialize(json_object *jso,
        TPMI_RSA_KEY_BITS *out)
{
    SUBTYPE_FILTER(TPMI_RSA_KEY_BITS, UINT16,
        1024, 2048);
}

/** Deserialize a TPM2B_ECC_PARAMETER json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPM2B_ECC_PARAMETER_deserialize(json_object *jso,
        TPM2B_ECC_PARAMETER *out)
{
    TSS2_RC r;
    LOG_TRACE("call");
    return_if_null(out, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    UINT16 size = 0;
    r = ifapi_json_byte_deserialize(jso, TPM2_MAX_ECC_KEY_BYTES,
                                     (BYTE *)&out->buffer, &size);
    return_if_error(r, "byte serialize");

    out->size = size;
    return r;
    LOG_TRACE("true");
    return TSS2_RC_SUCCESS;
}

static char *field_TPMS_ECC_POINT_tab[] = {
    "x",
    "y",
    "$schema"
};

/** Deserialize a TPMS_ECC_POINT json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_ECC_POINT_deserialize(json_object *jso,  TPMS_ECC_POINT *out)
{
    json_object *jso2;
    TSS2_RC r;
    LOG_TRACE("call");
    return_if_null(out, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    ifapi_check_json_object_fields(jso, &field_TPMS_ECC_POINT_tab[0],
                                   SIZE_OF_ARY(field_TPMS_ECC_POINT_tab));
    if (!ifapi_get_sub_object(jso, "x", &jso2)) {
        LOG_ERROR("Field \"x\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPM2B_ECC_PARAMETER_deserialize(jso2, &out->x);
    return_if_error(r, "Bad value for field \"x\".");

    if (!ifapi_get_sub_object(jso, "y", &jso2)) {
        LOG_ERROR("Field \"y\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPM2B_ECC_PARAMETER_deserialize(jso2, &out->y);
    return_if_error(r, "Bad value for field \"y\".");
    LOG_TRACE("true");
    return TSS2_RC_SUCCESS;
}

/** Deserialize a TPMI_ALG_ECC_SCHEME json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 */
TSS2_RC
ifapi_json_TPMI_ALG_ECC_SCHEME_deserialize(json_object *jso,
        TPMI_ALG_ECC_SCHEME *out)
{
    SUBTYPE_FILTER(TPMI_ALG_ECC_SCHEME, TPM2_ALG_ID,
        TPM2_ALG_ECDSA, TPM2_ALG_ECDAA, TPM2_ALG_SM2, TPM2_ALG_ECSCHNORR,
        TPM2_ALG_ECDH, TPM2_ALG_NULL);
}

/** Deserialize a TPMI_ECC_CURVE json object.
 *
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 */
TSS2_RC
ifapi_json_TPMI_ECC_CURVE_deserialize(json_object *jso, TPMI_ECC_CURVE *out)
{
    SUBTYPE_FILTER(TPMI_ECC_CURVE, TPM2_ECC_CURVE,
        TPM2_ECC_NONE, TPM2_ECC_NIST_P192, TPM2_ECC_NIST_P224, TPM2_ECC_NIST_P256,
        TPM2_ECC_NIST_P384, TPM2_ECC_NIST_P521, TPM2_ECC_BN_P256, TPM2_ECC_BN_P638,
        TPM2_ECC_SM2_P256);
}

static char *field_TPMT_ECC_SCHEME_tab[] = {
    "scheme",
    "details",
    "$schema"
};

/** Deserialize a TPMT_ECC_SCHEME json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMT_ECC_SCHEME_deserialize(json_object *jso,  TPMT_ECC_SCHEME *out)
{
    json_object *jso2;
    TSS2_RC r;
    LOG_TRACE("call");
    return_if_null(out, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    ifapi_check_json_object_fields(jso, &field_TPMT_ECC_SCHEME_tab[0],
                                   SIZE_OF_ARY(field_TPMT_ECC_SCHEME_tab));
    if (!ifapi_get_sub_object(jso, "scheme", &jso2)) {
        LOG_ERROR("Field \"scheme\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPMI_ALG_ECC_SCHEME_deserialize(jso2, &out->scheme);
    return_if_error(r, "Bad value for field \"scheme\".");
    if (out->scheme != TPM2_ALG_NULL) {
        if (!ifapi_get_sub_object(jso, "details", &jso2)) {
            LOG_ERROR("Field \"details\" not found.");
            return TSS2_FAPI_RC_BAD_VALUE;
        }
        r = ifapi_json_TPMU_ASYM_SCHEME_deserialize(out->scheme, jso2, &out->details);
        return_if_error(r, "Bad value for field \"details\".");
    }

    LOG_TRACE("true");
    return TSS2_RC_SUCCESS;
}

static char *field_TPMS_SIGNATURE_RSA_tab[] = {
    "hash",
    "sig",
    "$schema"
};

/** Deserialize a TPMS_SIGNATURE_RSA json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_SIGNATURE_RSA_deserialize(json_object *jso,
        TPMS_SIGNATURE_RSA *out)
{
    json_object *jso2;
    TSS2_RC r;
    LOG_TRACE("call");
    return_if_null(out, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    ifapi_check_json_object_fields(jso, &field_TPMS_SIGNATURE_RSA_tab[0],
                                   SIZE_OF_ARY(field_TPMS_SIGNATURE_RSA_tab));
    if (!ifapi_get_sub_object(jso, "hash", &jso2)) {
        LOG_ERROR("Field \"hash\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPMI_ALG_HASH_deserialize(jso2, &out->hash);
    return_if_error(r, "Bad value for field \"hash\".");

    if (!ifapi_get_sub_object(jso, "sig", &jso2)) {
        LOG_ERROR("Field \"sig\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPM2B_PUBLIC_KEY_RSA_deserialize(jso2, &out->sig);
    return_if_error(r, "Bad value for field \"sig\".");
    LOG_TRACE("true");
    return TSS2_RC_SUCCESS;
}

/*** Table 175 - Definition of Types for  Signature ***/

/** Deserialize a TPMS_SIGNATURE_RSASSA json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_SIGNATURE_RSASSA_deserialize(json_object *jso,
        TPMS_SIGNATURE_RSASSA *out)
{
    LOG_TRACE("call");
    return ifapi_json_TPMS_SIGNATURE_RSA_deserialize(jso, out);
}

/** Deserialize a TPMS_SIGNATURE_RSAPSS json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_SIGNATURE_RSAPSS_deserialize(json_object *jso,
        TPMS_SIGNATURE_RSAPSS *out)
{
    LOG_TRACE("call");
    return ifapi_json_TPMS_SIGNATURE_RSA_deserialize(jso, out);
}

static char *field_TPMS_SIGNATURE_ECC_tab[] = {
    "hash",
    "signatureR",
    "signaturer",
    "signatureS",
    "signatures",
    "$schema"
};

/** Deserialize a TPMS_SIGNATURE_ECC json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_SIGNATURE_ECC_deserialize(json_object *jso,
        TPMS_SIGNATURE_ECC *out)
{
    json_object *jso2;
    TSS2_RC r;
    LOG_TRACE("call");
    return_if_null(out, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    ifapi_check_json_object_fields(jso, &field_TPMS_SIGNATURE_ECC_tab[0],
                                   SIZE_OF_ARY(field_TPMS_SIGNATURE_ECC_tab));
    if (!ifapi_get_sub_object(jso, "hash", &jso2)) {
        LOG_ERROR("Field \"hash\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPMI_ALG_HASH_deserialize(jso2, &out->hash);
    return_if_error(r, "Bad value for field \"hash\".");

    if (!ifapi_get_sub_object(jso, "signatureR", &jso2)) {
        LOG_ERROR("Field \"signatureR\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPM2B_ECC_PARAMETER_deserialize(jso2, &out->signatureR);
    return_if_error(r, "Bad value for field \"signatureR\".");

    if (!ifapi_get_sub_object(jso, "signatureS", &jso2)) {
        LOG_ERROR("Field \"signatureS\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPM2B_ECC_PARAMETER_deserialize(jso2, &out->signatureS);
    return_if_error(r, "Bad value for field \"signatureS\".");
    LOG_TRACE("true");
    return TSS2_RC_SUCCESS;
}

/*** Table 177 - Definition of Types for  TPMS_SIGNATURE_ECC ***/

/** Deserialize a TPMS_SIGNATURE_ECDSA json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_SIGNATURE_ECDSA_deserialize(json_object *jso,
        TPMS_SIGNATURE_ECDSA *out)
{
    LOG_TRACE("call");
    return ifapi_json_TPMS_SIGNATURE_ECC_deserialize(jso, out);
}

/** Deserialize a TPMS_SIGNATURE_ECDAA json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_SIGNATURE_ECDAA_deserialize(json_object *jso,
        TPMS_SIGNATURE_ECDAA *out)
{
    LOG_TRACE("call");
    return ifapi_json_TPMS_SIGNATURE_ECC_deserialize(jso, out);
}

/** Deserialize a TPMS_SIGNATURE_SM2 json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_SIGNATURE_SM2_deserialize(json_object *jso,
        TPMS_SIGNATURE_SM2 *out)
{
    LOG_TRACE("call");
    return ifapi_json_TPMS_SIGNATURE_ECC_deserialize(jso, out);
}

/** Deserialize a TPMS_SIGNATURE_ECSCHNORR json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_SIGNATURE_ECSCHNORR_deserialize(json_object *jso,
        TPMS_SIGNATURE_ECSCHNORR *out)
{
    LOG_TRACE("call");
    return ifapi_json_TPMS_SIGNATURE_ECC_deserialize(jso, out);
}

/** Deserialize a TPMU_SIGNATURE json object.
 *
 * This functions expects the Bitfield to be encoded as unsigned int in host-endianess.
 * @param[in]  selector The type the signature.
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMU_SIGNATURE_deserialize(
    UINT32 selector,
    json_object *jso,
    TPMU_SIGNATURE *out)
{
    LOG_TRACE("call");
    switch (selector) {
    case TPM2_ALG_RSASSA:
        return ifapi_json_TPMS_SIGNATURE_RSASSA_deserialize(jso, &out->rsassa);
    case TPM2_ALG_RSAPSS:
        return ifapi_json_TPMS_SIGNATURE_RSAPSS_deserialize(jso, &out->rsapss);
    case TPM2_ALG_ECDSA:
        return ifapi_json_TPMS_SIGNATURE_ECDSA_deserialize(jso, &out->ecdsa);
    case TPM2_ALG_ECDAA:
        return ifapi_json_TPMS_SIGNATURE_ECDAA_deserialize(jso, &out->ecdaa);
    case TPM2_ALG_SM2:
        return ifapi_json_TPMS_SIGNATURE_SM2_deserialize(jso, &out->sm2);
    case TPM2_ALG_ECSCHNORR:
        return ifapi_json_TPMS_SIGNATURE_ECSCHNORR_deserialize(jso, &out->ecschnorr);
    case TPM2_ALG_HMAC:
        return ifapi_json_TPMT_HA_deserialize(jso, &out->hmac);

    case TPM2_ALG_NULL: {
            return TSS2_RC_SUCCESS;
        }
    default:
        LOG_TRACE("false");
        return TSS2_FAPI_RC_BAD_VALUE;
    };
}

static char *field_TPMT_SIGNATURE_tab[] = {
    "sigAlg",
    "sigalg",
    "signature",
    "$schema"
};

/** Deserialize a TPMT_SIGNATURE json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMT_SIGNATURE_deserialize(json_object *jso,  TPMT_SIGNATURE *out)
{
    json_object *jso2;
    TSS2_RC r;
    LOG_TRACE("call");
    return_if_null(out, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    ifapi_check_json_object_fields(jso, &field_TPMT_SIGNATURE_tab[0],
                                   SIZE_OF_ARY(field_TPMT_SIGNATURE_tab));
    if (!ifapi_get_sub_object(jso, "sigAlg", &jso2)) {
        LOG_ERROR("Field \"sigAlg\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPMI_ALG_SIG_SCHEME_deserialize(jso2, &out->sigAlg);
    return_if_error(r, "Bad value for field \"sigAlg\".");
    if (out->sigAlg != TPM2_ALG_NULL) {
        if (!ifapi_get_sub_object(jso, "signature", &jso2)) {
            LOG_ERROR("Field \"signature\" not found.");
            return TSS2_FAPI_RC_BAD_VALUE;
        }
        r = ifapi_json_TPMU_SIGNATURE_deserialize(out->sigAlg, jso2, &out->signature);
        return_if_error(r, "Bad value for field \"signature\".");
    }

    LOG_TRACE("true");
    return TSS2_RC_SUCCESS;
}

/** Deserialize a TPM2B_ENCRYPTED_SECRET json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPM2B_ENCRYPTED_SECRET_deserialize(json_object *jso,
        TPM2B_ENCRYPTED_SECRET *out)
{
    TSS2_RC r;
    LOG_TRACE("call");
    return_if_null(out, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    UINT16 size = 0;
    r = ifapi_json_byte_deserialize(jso, sizeof(TPMU_ENCRYPTED_SECRET),
                                     (BYTE *)&out->secret, &size);
    return_if_error(r, "byte serialize");

    out->size = size;
    return r;
    LOG_TRACE("true");
    return TSS2_RC_SUCCESS;
}

/** Deserialize a TPMI_ALG_PUBLIC json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 */
TSS2_RC
ifapi_json_TPMI_ALG_PUBLIC_deserialize(json_object *jso, TPMI_ALG_PUBLIC *out)
{
    SUBTYPE_FILTER(TPMI_ALG_PUBLIC, TPM2_ALG_ID,
        TPM2_ALG_RSA, TPM2_ALG_KEYEDHASH, TPM2_ALG_ECC, TPM2_ALG_SYMCIPHER, TPM2_ALG_NULL);
}

/** Deserialize a TPMU_PUBLIC_ID json object.
 *
 * This functions expects the Bitfield to be encoded as unsigned int in host-endianess.
 * @param[in]  selector The type the public ID.
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMU_PUBLIC_ID_deserialize(
    UINT32 selector,
    json_object *jso,
    TPMU_PUBLIC_ID *out)
{
    LOG_TRACE("call");
    switch (selector) {
    case TPM2_ALG_KEYEDHASH:
        return ifapi_json_TPM2B_DIGEST_deserialize(jso, &out->keyedHash);
    case TPM2_ALG_SYMCIPHER:
        return ifapi_json_TPM2B_DIGEST_deserialize(jso, &out->sym);
    case TPM2_ALG_RSA:
        return ifapi_json_TPM2B_PUBLIC_KEY_RSA_deserialize(jso, &out->rsa);
    case TPM2_ALG_ECC:
        return ifapi_json_TPMS_ECC_POINT_deserialize(jso, &out->ecc);
    default:
        LOG_TRACE("false");
        return TSS2_FAPI_RC_BAD_VALUE;
    };
}

static char *field_TPMS_KEYEDHASH_PARMS_tab[] = {
    "scheme",
    "$schema"
};

/** Deserialize a TPMS_KEYEDHASH_PARMS json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_KEYEDHASH_PARMS_deserialize(json_object *jso,
        TPMS_KEYEDHASH_PARMS *out)
{
    json_object *jso2;
    TSS2_RC r;
    LOG_TRACE("call");
    return_if_null(out, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    ifapi_check_json_object_fields(jso, &field_TPMS_KEYEDHASH_PARMS_tab[0],
                                   SIZE_OF_ARY(field_TPMS_KEYEDHASH_PARMS_tab));
    if (!ifapi_get_sub_object(jso, "scheme", &jso2)) {
        LOG_ERROR("Field \"scheme\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPMT_KEYEDHASH_SCHEME_deserialize(jso2, &out->scheme);
    return_if_error(r, "Bad value for field \"scheme\".");
    LOG_TRACE("true");
    return TSS2_RC_SUCCESS;
}

static char *field_TPMS_RSA_PARMS_tab[] = {
    "symmetric",
    "scheme",
    "keyBits",
    "keybits",
    "exponent",
    "$schema"
};

/** Deserialize a TPMS_RSA_PARMS json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_RSA_PARMS_deserialize(json_object *jso,  TPMS_RSA_PARMS *out)
{
    json_object *jso2;
    TSS2_RC r;
    LOG_TRACE("call");
    return_if_null(out, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    ifapi_check_json_object_fields(jso, &field_TPMS_RSA_PARMS_tab[0],
                                   SIZE_OF_ARY(field_TPMS_RSA_PARMS_tab));
    if (!ifapi_get_sub_object(jso, "symmetric", &jso2)) {
        LOG_ERROR("Field \"symmetric\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPMT_SYM_DEF_OBJECT_deserialize(jso2, &out->symmetric);
    return_if_error(r, "Bad value for field \"symmetric\".");

    if (!ifapi_get_sub_object(jso, "scheme", &jso2)) {
        LOG_ERROR("Field \"scheme\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPMT_RSA_SCHEME_deserialize(jso2, &out->scheme);
    return_if_error(r, "Bad value for field \"scheme\".");

    if (!ifapi_get_sub_object(jso, "keyBits", &jso2)) {
        LOG_ERROR("Field \"keyBits\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPMI_RSA_KEY_BITS_deserialize(jso2, &out->keyBits);
    return_if_error(r, "Bad value for field \"keyBits\".");

    if (!ifapi_get_sub_object(jso, "exponent", &jso2)) {
        LOG_ERROR("Field \"exponent\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_UINT32_deserialize(jso2, &out->exponent);
    return_if_error(r, "Bad value for field \"exponent\".");
    LOG_TRACE("true");
    return TSS2_RC_SUCCESS;
}

static char *field_TPMS_ECC_PARMS_tab[] = {
    "symmetric",
    "scheme",
    "curveID",
    "curveid",
    "kdf",
    "$schema"
};

/** Deserialize a TPMS_ECC_PARMS json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_ECC_PARMS_deserialize(json_object *jso,  TPMS_ECC_PARMS *out)
{
    json_object *jso2;
    TSS2_RC r;
    LOG_TRACE("call");
    return_if_null(out, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    ifapi_check_json_object_fields(jso, &field_TPMS_ECC_PARMS_tab[0],
                                   SIZE_OF_ARY(field_TPMS_ECC_PARMS_tab));
    if (!ifapi_get_sub_object(jso, "symmetric", &jso2)) {
        LOG_ERROR("Field \"symmetric\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPMT_SYM_DEF_OBJECT_deserialize(jso2, &out->symmetric);
    return_if_error(r, "Bad value for field \"symmetric\".");

    if (!ifapi_get_sub_object(jso, "scheme", &jso2)) {
        LOG_ERROR("Field \"scheme\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPMT_ECC_SCHEME_deserialize(jso2, &out->scheme);
    return_if_error(r, "Bad value for field \"scheme\".");

    if (!ifapi_get_sub_object(jso, "curveID", &jso2)) {
        LOG_ERROR("Field \"curveID\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPMI_ECC_CURVE_deserialize(jso2, &out->curveID);
    return_if_error(r, "Bad value for field \"curveID\".");

    if (!ifapi_get_sub_object(jso, "kdf", &jso2)) {
        LOG_ERROR("Field \"kdf\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPMT_KDF_SCHEME_deserialize(jso2, &out->kdf);
    return_if_error(r, "Bad value for field \"kdf\".");
    LOG_TRACE("true");
    return TSS2_RC_SUCCESS;
}

/** Deserialize a TPMU_PUBLIC_PARMS json object.
 *
 * This functions expects the Bitfield to be encoded as unsigned int in host-endianess.
 * @param[in]  selector The type the public params.
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMU_PUBLIC_PARMS_deserialize(
    UINT32 selector,
    json_object *jso,
    TPMU_PUBLIC_PARMS *out)
{
    LOG_TRACE("call");
    switch (selector) {
    case TPM2_ALG_KEYEDHASH:
        return ifapi_json_TPMS_KEYEDHASH_PARMS_deserialize(jso, &out->keyedHashDetail);
    case TPM2_ALG_SYMCIPHER:
        return ifapi_json_TPMS_SYMCIPHER_PARMS_deserialize(jso, &out->symDetail);
    case TPM2_ALG_RSA:
        return ifapi_json_TPMS_RSA_PARMS_deserialize(jso, &out->rsaDetail);
    case TPM2_ALG_ECC:
        return ifapi_json_TPMS_ECC_PARMS_deserialize(jso, &out->eccDetail);
    default:
        LOG_TRACE("false");
        return TSS2_FAPI_RC_BAD_VALUE;
    };
}

static char *field_TPMT_PUBLIC_tab[] = {
    "type",
    "nameAlg",
    "namealg",
    "objectAttributes",
    "objectattributes",
    "authPolicy",
    "authpolicy",
    "parameters",
    "unique",
    "$schema"
};

/** Deserialize a TPMT_PUBLIC json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMT_PUBLIC_deserialize(json_object *jso,  TPMT_PUBLIC *out)
{
    json_object *jso2;
    TSS2_RC r;
    LOG_TRACE("call");
    return_if_null(out, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    ifapi_check_json_object_fields(jso, &field_TPMT_PUBLIC_tab[0],
                                   SIZE_OF_ARY(field_TPMT_PUBLIC_tab));
    if (!ifapi_get_sub_object(jso, "type", &jso2)) {
        LOG_ERROR("Field \"type\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPMI_ALG_PUBLIC_deserialize(jso2, &out->type);
    return_if_error(r, "Bad value for field \"type\".");

    if (!ifapi_get_sub_object(jso, "nameAlg", &jso2)) {
        LOG_ERROR("Field \"nameAlg\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPMI_ALG_HASH_deserialize(jso2, &out->nameAlg);
    return_if_error(r, "Bad value for field \"nameAlg\".");

    if (!ifapi_get_sub_object(jso, "objectAttributes", &jso2)) {
        LOG_ERROR("Field \"objectAttributes\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPMA_OBJECT_deserialize(jso2, &out->objectAttributes);
    return_if_error(r, "Bad value for field \"objectAttributes\".");

    if (!ifapi_get_sub_object(jso, "authPolicy", &jso2)) {
        LOG_ERROR("Field \"authPolicy\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPM2B_DIGEST_deserialize(jso2, &out->authPolicy);
    return_if_error(r, "Bad value for field \"authPolicy\".");
    if (!ifapi_get_sub_object(jso, "parameters", &jso2)) {
        LOG_ERROR("Field \"parameters\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPMU_PUBLIC_PARMS_deserialize(out->type, jso2, &out->parameters);
    return_if_error(r, "Bad value for field \"parameters\".");

    if (!ifapi_get_sub_object(jso, "unique", &jso2)) {
        memset(&out->unique, 0, sizeof(TPMU_PUBLIC_ID));
    } else {
        r = ifapi_json_TPMU_PUBLIC_ID_deserialize(out->type, jso2, &out->unique);
        return_if_error(r, "Bad value for field \"unique\".");
    }

    LOG_TRACE("true");
    return TSS2_RC_SUCCESS;
}

static char *field_TPM2B_PUBLIC_tab[] = {
    "size",
    "publicArea",
    "publicarea",
    "$schema"
};

/** Deserialize a TPM2B_PUBLIC json object.
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPM2B_PUBLIC_deserialize(json_object *jso, TPM2B_PUBLIC *out)
{
    json_object *jso2;
    TSS2_RC res;
    LOG_TRACE("call");
    ifapi_check_json_object_fields(jso, &field_TPM2B_PUBLIC_tab[0],
                                   SIZE_OF_ARY(field_TPM2B_PUBLIC_tab));
    if (!ifapi_get_sub_object(jso, "size", &jso2)) {
        LOG_ERROR("Field \"size\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    res = ifapi_json_UINT16_deserialize(jso2, &out->size);
    return_if_error(res, "Bad value for field \"size\".");
    if (!ifapi_get_sub_object(jso, "publicArea", &jso2)) {
        LOG_ERROR("Field \"publicArea\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    res = ifapi_json_TPMT_PUBLIC_deserialize(jso2, &out->publicArea);
    return_if_error(res, "Bad value for field \"publicArea\".");
    return TSS2_RC_SUCCESS;
}

/** Deserialize a TPM2B_PRIVATE json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPM2B_PRIVATE_deserialize(json_object *jso,  TPM2B_PRIVATE *out)
{
    TSS2_RC r;
    LOG_TRACE("call");
    return_if_null(out, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    UINT16 size = 0;
    r = ifapi_json_byte_deserialize(jso, sizeof(_PRIVATE), (BYTE *)&out->buffer,
                                     &size);
    return_if_error(r, "byte serialize");

    out->size = size;
    return r;
    LOG_TRACE("true");
    return TSS2_RC_SUCCESS;
}

/** Deserialize a TPM2_NT json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPM2_NT_deserialize(json_object *jso, TPM2_NT *out)
{
    static const struct { TPM2_NT in; const char *name; } tab[] = {
        { TPM2_NT_ORDINARY, "ORDINARY" },
        { TPM2_NT_COUNTER, "COUNTER" },
        { TPM2_NT_BITS, "BITS" },
        { TPM2_NT_EXTEND, "EXTEND" },
        { TPM2_NT_PIN_FAIL, "PIN_FAIL" },
        { TPM2_NT_PIN_PASS, "PIN_PASS" },
    };

    const char *s = json_object_get_string(jso);
    const char *str = strip_prefix(s, "TPM_", "TPM2_", "NT_", NULL);
    LOG_TRACE("called for %s parsing %s", s, str);

    if (str) {
        for (size_t i = 0; i < sizeof(tab) / sizeof(tab[0]); i++) {
            if (strcasecmp(str, &tab[i].name[0]) == 0) {
                *out = tab[i].in;
                return TSS2_RC_SUCCESS;
            }
        }
    }

    return ifapi_json_UINT8_deserialize(jso, out);
}

/** Deserialize a TPMA_NV json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMA_NV_deserialize(json_object *jso, TPMA_NV *out)
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
        { TPM2_NT_ORDINARY << 4, "ORDINARY" },
        { TPM2_NT_COUNTER << 4, "COUNTER" },
        { TPM2_NT_BITS << 4, "BITS" },
        { TPM2_NT_EXTEND << 4, "EXTEND" },
        { TPM2_NT_PIN_FAIL << 4, "PIN_FAIL" },
        { TPM2_NT_PIN_PASS << 4, "PIN_PASS" },
    };
    size_t n = sizeof(tab) / sizeof(tab[0]);
    size_t i, j;

    TPMI_YES_NO flag;
    TSS2_RC r;

    LOG_TRACE("call");
    memset(out, 0, sizeof(TPMA_NV));
    json_type jso_type = json_object_get_type(jso);
    if (jso_type == json_type_array) {
        /* Cast (size_t) is necessary to support older version of libjson-c */
        for (i = 0; i < (size_t)json_object_array_length(jso); i++) {
            json_object *jso2 = json_object_array_get_idx(jso, i);
            if (json_object_get_type(jso2) == json_type_object) {
                if (!json_object_object_get_ex(jso2, "TPM2_NT", &jso2)) {
                    LOG_ERROR("Found object in array without TPM2_NT");
                    return TSS2_FAPI_RC_BAD_VALUE;
                }
                TPM2_NT out2;
                TSS2_RC r = ifapi_json_TPM2_NT_deserialize(jso2, &out2);
                return_if_error(r, "Bad value");
                *out |= out2 << 4;
                continue;
            }
            const char *token = strip_prefix(json_object_get_string(jso2),
                                    "TPM_", "TPM2_", "TPMA_", "NV_",
                                    "TPM2_", "NT_", NULL);
            if (!token) {
                LOG_ERROR("Bad object; expected array of strings.");
                return TSS2_FAPI_RC_BAD_VALUE;
            }
            for (j = 0; j < n; j++) {
                if (strcasecmp(tab[j].name, token) == 0) {
                    *out |= tab[j].in;
                    break;
                }
            }
            if (j == n) {
                LOG_ERROR("Unknown value: %s", json_object_get_string(jso2));
                return TSS2_FAPI_RC_BAD_VALUE;
            }
        }
    } else if (jso_type == json_type_object) {
        json_object_object_foreach(jso, key, val) {
            const char *token = strip_prefix(key, "TPM_", "TPM2_", "TPMA_", "NV_", "TPM2_", NULL);
            if (strcasecmp(token, "NT") == 0) {
                TPM2_NT out2;
                TSS2_RC r = ifapi_json_TPM2_NT_deserialize(val, &out2);
                return_if_error(r, "Bad value");
                *out |= out2 << 4;
                continue;
            }
            token = strip_prefix(token, "NT_", NULL);
            r = get_boolean_from_json(val, &flag);
            return_if_error2(r, "Boolean value expected at key: %s", key);
            for (j = 0; j < n; j++) {
                if (strcasecmp(tab[j].name, token) == 0) {
                    if (flag)
                        *out |= tab[j].in;
                    break;
                }
            }
            if (j == n) {
                LOG_ERROR("Unknown key: %s", key);
                return TSS2_FAPI_RC_BAD_VALUE;
            }
        }
    } else {
        const char *token;
        token = json_object_get_string(jso);
        int64_t i64;
        if (!get_number(token, &i64)) {
            LOG_ERROR("Bad value");
            return TSS2_FAPI_RC_BAD_VALUE;
        }
        *out = (TPMA_NV) i64;
        if ((int64_t)*out != i64) {
            LOG_ERROR("Bad value");
            return TSS2_FAPI_RC_BAD_VALUE;
        }
        return TSS2_RC_SUCCESS;
    }
    LOG_TRACE("true");
    return TSS2_RC_SUCCESS;
}

static char *field_TPMS_NV_PUBLIC_tab[] = {
    "nvIndex",
    "nvindex",
    "nameAlg",
    "namealg",
    "attributes",
    "authPolicy",
    "authpolicy",
    "dataSize",
    "datasize",
    "$schema"
};

/** Deserialize a TPMS_NV_PUBLIC json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_NV_PUBLIC_deserialize(json_object *jso,  TPMS_NV_PUBLIC *out)
{
    json_object *jso2;
    TSS2_RC r;
    LOG_TRACE("call");
    return_if_null(out, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    ifapi_check_json_object_fields(jso, &field_TPMS_NV_PUBLIC_tab[0],
                                   SIZE_OF_ARY(field_TPMS_NV_PUBLIC_tab));
    if (!ifapi_get_sub_object(jso, "nvIndex", &jso2)) {
        LOG_ERROR("Field \"nvIndex\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPMI_RH_NV_INDEX_deserialize(jso2, &out->nvIndex);
    return_if_error(r, "Bad value for field \"nvIndex\".");

    if (!ifapi_get_sub_object(jso, "nameAlg", &jso2)) {
        LOG_ERROR("Field \"nameAlg\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPMI_ALG_HASH_deserialize(jso2, &out->nameAlg);
    return_if_error(r, "Bad value for field \"nameAlg\".");

    if (!ifapi_get_sub_object(jso, "attributes", &jso2)) {
        LOG_ERROR("Field \"attributes\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPMA_NV_deserialize(jso2, &out->attributes);
    return_if_error(r, "Bad value for field \"attributes\".");

    if (!ifapi_get_sub_object(jso, "authPolicy", &jso2)) {
        LOG_ERROR("Field \"authPolicy\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPM2B_DIGEST_deserialize(jso2, &out->authPolicy);
    return_if_error(r, "Bad value for field \"authPolicy\".");

    if (!ifapi_get_sub_object(jso, "dataSize", &jso2)) {
        LOG_ERROR("Field \"dataSize\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_UINT16_deserialize(jso2, &out->dataSize);
    return_if_error(r, "Bad value for field \"dataSize\".");

    LOG_TRACE("true");
    return TSS2_RC_SUCCESS;
}

static char *field_TPM2B_NV_PUBLIC_tab[] = {
    "size",
    "nvPublic",
    "nvpublic",
    "$schema"
};

/** Deserialize a TPM2B_NV_PUBLIC json object.
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPM2B_NV_PUBLIC_deserialize(json_object *jso, TPM2B_NV_PUBLIC *out)
{
    json_object *jso2;
    TSS2_RC res;
    LOG_TRACE("call");
    ifapi_check_json_object_fields(jso, &field_TPM2B_NV_PUBLIC_tab[0],
                                   SIZE_OF_ARY(field_TPM2B_NV_PUBLIC_tab));
    if (!ifapi_get_sub_object(jso, "size", &jso2)) {
        LOG_ERROR("Field \"size\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    res = ifapi_json_UINT16_deserialize(jso2, &out->size);
    return_if_error(res, "Bad value for field \"size\".");
    if (!ifapi_get_sub_object(jso, "nvPublic", &jso2)) {
        LOG_ERROR("Field \"nvPublic\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    res = ifapi_json_TPMS_NV_PUBLIC_deserialize(jso2, &out->nvPublic);
    return_if_error(res, "Bad value for field \"nvPublic\".");
    return TSS2_RC_SUCCESS;
}

static char *field_TPMS_CREATION_DATA_tab[] = {
    "pcrSelect",
    "pcrselect",
    "pcrDigest",
    "pcrdigest",
    "locality",
    "parentNameAlg",
    "parentnamealg",
    "parentName",
    "parentname",
    "parentQualifiedName",
    "parentqualifiedname",
    "outsideInfo",
    "outsideinfo",
    "$schema"
};

/** Deserialize a TPMS_CREATION_DATA json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPMS_CREATION_DATA_deserialize(json_object *jso,
        TPMS_CREATION_DATA *out)
{
    json_object *jso2;
    TSS2_RC r;
    LOG_TRACE("call");
    return_if_null(out, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    ifapi_check_json_object_fields(jso, &field_TPMS_CREATION_DATA_tab[0],
                                   SIZE_OF_ARY(field_TPMS_CREATION_DATA_tab));
    if (!ifapi_get_sub_object(jso, "pcrSelect", &jso2)) {
        LOG_ERROR("Field \"pcrSelect\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPML_PCR_SELECTION_deserialize(jso2, &out->pcrSelect);
    return_if_error(r, "Bad value for field \"pcrSelect\".");

    if (!ifapi_get_sub_object(jso, "pcrDigest", &jso2)) {
        LOG_ERROR("Field \"pcrDigest\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPM2B_DIGEST_deserialize(jso2, &out->pcrDigest);
    return_if_error(r, "Bad value for field \"pcrDigest\".");

    if (!ifapi_get_sub_object(jso, "locality", &jso2)) {
        LOG_ERROR("Field \"locality\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPMA_LOCALITY_deserialize(jso2, &out->locality);
    return_if_error(r, "Bad value for field \"locality\".");

    if (!ifapi_get_sub_object(jso, "parentNameAlg", &jso2)) {
        LOG_ERROR("Field \"parentNameAlg\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPM2_ALG_ID_deserialize(jso2, &out->parentNameAlg);
    return_if_error(r, "Bad value for field \"parentNameAlg\".");

    if (!ifapi_get_sub_object(jso, "parentName", &jso2)) {
        LOG_ERROR("Field \"parentName\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPM2B_NAME_deserialize(jso2, &out->parentName);
    return_if_error(r, "Bad value for field \"parentName\".");

    if (!ifapi_get_sub_object(jso, "parentQualifiedName", &jso2)) {
        LOG_ERROR("Field \"parentQualifiedName\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPM2B_NAME_deserialize(jso2, &out->parentQualifiedName);
    return_if_error(r, "Bad value for field \"parentQualifiedName\".");

    if (!ifapi_get_sub_object(jso, "outsideInfo", &jso2)) {
        LOG_ERROR("Field \"outsideInfo\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPM2B_DATA_deserialize(jso2, &out->outsideInfo);
    return_if_error(r, "Bad value for field \"outsideInfo\".");
    LOG_TRACE("true");
    return TSS2_RC_SUCCESS;
}

static char *field_TPM2B_CREATION_DATA_tab[] = {
    "size",
    "creationData",
    "creationdata",
    "$schema"
};

/** Deserialize a TPM2B_CREATION_DATA json object.
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_json_TPM2B_CREATION_DATA_deserialize(json_object *jso,
        TPM2B_CREATION_DATA *out)
{
    json_object *jso2;
    TSS2_RC res;
    LOG_TRACE("call");
    ifapi_check_json_object_fields(jso, &field_TPM2B_CREATION_DATA_tab[0],
                                   SIZE_OF_ARY(field_TPM2B_CREATION_DATA_tab));
    if (!ifapi_get_sub_object(jso, "size", &jso2)) {
        LOG_ERROR("Field \"size\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    res = ifapi_json_UINT16_deserialize(jso2, &out->size);
    return_if_error(res, "Bad value for field \"size\".");
    if (!ifapi_get_sub_object(jso, "creationData", &jso2)) {
        LOG_ERROR("Field \"creationData\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    res = ifapi_json_TPMS_CREATION_DATA_deserialize(jso2, &out->creationData);
    return_if_error(res, "Bad value for field \"creationData\".");
    return TSS2_RC_SUCCESS;
}
