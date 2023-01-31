/* SPDX-License-Identifier: BSD-2-Clause */
/*******************************************************************************
 * Copyright 2017-2018, Fraunhofer SIT sponsored by Infineon Technologies AG
 * All rights reserved.
 ******************************************************************************/

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <stdio.h>
#include <stdlib.h>
#include <inttypes.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <string.h>
#include <unistd.h>
#include <errno.h>
#include <openssl/sha.h>
#include <ctype.h>
#include <stdbool.h>
#include <openssl/evp.h>
#include <json-c/json.h>
#include <json-c/json_util.h>
#include "tss2_common.h"
#include "tss2_tpm2_types.h"
#include "fapi_int.h"
#include "ifapi_json_deserialize.h"
#include "tpm_json_deserialize.h"
#include "ifapi_ima_eventlog.h"
#include "ifapi_helpers.h"

#define LOGMODULE fapijson
#include "util/log.h"
#include "util/aux_util.h"

/* Defines from kernel ima.h */
#define IMA_TEMPLATE_FIELD_ID_MAX_LEN 16
#define IMA_TEMPLATE_NUM_FIELDS_MAX 15
/* Define from kernel crypt.h */
#define CRYPTO_MAX_ALG_NAME 128

static TSS2_RC
get_json_content(json_object *jso, json_object **jso_sub) {
    if (!ifapi_get_sub_object(jso, CONTENT, jso_sub)) {
        *jso_sub = json_object_new_object();
        return_if_null(*jso_sub, "Out of memory.", TSS2_FAPI_RC_MEMORY);
        json_object_object_add(jso, CONTENT, *jso_sub);
    }
    return TSS2_RC_SUCCESS;
}

static TSS2_RC
add_uint8_ary_to_json(UINT8 *buffer, UINT32 size, json_object *jso, const char *jso_tag)
{
    json_object *jso_byte_string = NULL;

    return_if_null(buffer, "Bad reference.", TSS2_FAPI_RC_BAD_VALUE);
    return_if_null(jso, "Bad reference.", TSS2_FAPI_RC_BAD_VALUE);

    char *hex_string = malloc((size) * 2 + 1);
    return_if_null(hex_string, "Out of memory.", TSS2_FAPI_RC_MEMORY);

    if (size > 0) {
        for (size_t i = 0, off = 0; i < size; i++, off += 2)
            sprintf(&hex_string[off], "%02x", buffer[i]);
    }
    hex_string[(size) * 2] = '\0';
    jso_byte_string = json_object_new_string(hex_string);
    SAFE_FREE(hex_string)
    return_if_null(jso_byte_string, "Out of memory", TSS2_FAPI_RC_MEMORY);

    json_object_object_add(jso, jso_tag, jso_byte_string);
    return TSS2_RC_SUCCESS;
}

static TSS2_RC
add_string_to_json(const char *string, json_object *jso, const char *jso_tag)
{
    json_object *jso_string = NULL;

    return_if_null(string, "Bad reference.", TSS2_FAPI_RC_BAD_VALUE);
    return_if_null(jso, "Bad reference.", TSS2_FAPI_RC_BAD_VALUE);

    jso_string = json_object_new_string(string);
    return_if_null(jso_string, "Out of memory", TSS2_FAPI_RC_MEMORY);

    json_object_object_add(jso, jso_tag, jso_string);
    return TSS2_RC_SUCCESS;
}

static TSS2_RC
add_number_to_json(UINT32 number, json_object *jso, const char *jso_tag)
{
    json_object *jso_number = NULL;

    return_if_null(jso, "Bad reference.", TSS2_FAPI_RC_BAD_VALUE);

    jso_number = json_object_new_int64(number);
    return_if_null(jso_number, "Out of memory", TSS2_FAPI_RC_MEMORY);

    json_object_object_add(jso, jso_tag, jso_number);
    return TSS2_RC_SUCCESS;
}

static bool
zero_digest(UINT8 *buffer, size_t size)
{
    if (buffer[0] == 0 && memcmp(&buffer[0], &buffer[1], size - 1) == 0) {
        return true;
    } else {
        return false;
    }
}

static UINT8 digest_ff[TPM2_SHA512_DIGEST_SIZE] = {
    0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
    0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
    0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
    0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
    0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
    0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
    0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
    0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
};

/* Replace current sha1 digest with digest of 0xff values. */
static TSS2_RC
set_ff_digest(json_object *jso) {
    TSS2_RC r;
    json_object
        *jso_digest = NULL,
        *jso_ary = NULL,
        *jso_digest_type = NULL;

    jso_digest = json_object_new_object();
    return_if_null(jso_digest, "Out of memory.", TSS2_FAPI_RC_MEMORY);

    r = add_uint8_ary_to_json(digest_ff,TPM2_SHA1_DIGEST_SIZE, jso_digest, "digest");
    return_if_error(r, "Add digest to json");

    jso_digest_type = NULL;
    jso_digest_type = json_object_new_string ("sha1");
    goto_if_null(jso_digest_type, "Out of memory.", TSS2_FAPI_RC_MEMORY, error);

    json_object_object_add(jso_digest, "hashAlg", jso_digest_type);

    jso_ary = json_object_new_array();
    goto_if_null(jso_ary, "Out of memory.", TSS2_FAPI_RC_MEMORY, error);

    json_object_array_add(jso_ary, jso_digest);
    json_object_object_del(jso, "digests");
    json_object_object_add(jso, "digests", jso_ary);
    return TSS2_RC_SUCCESS;

 error:
    if (jso_digest)
        json_object_put(jso_digest);
    if (jso_digest_type)
        json_object_put(jso_digest_type);
    if (jso_ary)
        json_object_put(jso_ary);
    return r;
}

/** Callback for digest of old IMA format.
 */
static TSS2_RC
sha_digest_json_cb(UINT8 *digest, UINT8 * buffer, size_t *offset, json_object *jso,
                   IFAPI_IMA_TEMPLATE *template) {
    TSS2_RC r;
    UNUSED(template);

    LOGBLOB_TRACE(&buffer[*offset], TPM2_SHA1_DIGEST_SIZE, "IMA buffer");
    LOGBLOB_TRACE(digest, TPM2_SHA1_DIGEST_SIZE, "IMA digest");

    if (jso && zero_digest(digest, TPM2_SHA1_DIGEST_SIZE) &&
        zero_digest(&buffer[*offset], TPM2_SHA1_DIGEST_SIZE)) {
        r = set_ff_digest(jso);
        return_if_error(r, "Set 0xff in digest.");
    }

    *offset += TPM2_SHA1_DIGEST_SIZE;
    return TSS2_RC_SUCCESS;
}

/** Get UINT32 size value from buffer and increase offset.
 */
UINT32
get_size_from_buffer(UINT8 *buffer, size_t *offset) {
    UINT32 size;
    memcpy(&size, &buffer[*offset], sizeof(UINT32));
    *offset += sizeof(UINT32);
    return size;
}

/** Callback for digest with name of used hash algorithm,
 */
static TSS2_RC
digest_with_hash_name_cb(UINT8 *digest, UINT8 *buffer, size_t *offset, json_object *jso,
                        IFAPI_IMA_TEMPLATE *template) {
    TSS2_RC r;
    char hash_alg[CRYPTO_MAX_ALG_NAME + 1] = { 0 };
    size_t alg_name_size;
    const EVP_MD *md;
    int digest_size;
    UINT32 digest_buffer_size;

    digest_buffer_size = get_size_from_buffer(buffer, offset);
    alg_name_size = strlen((char *)&buffer[*offset]) - 1; /**< strip : */
    if (alg_name_size > CRYPTO_MAX_ALG_NAME) {
        return_error(TSS2_FAPI_RC_BAD_VALUE, "Invalid hash name.");
    }
    memcpy(hash_alg, &buffer[*offset], alg_name_size);
    md = EVP_get_digestbyname(hash_alg);
    if (md == NULL) {
        return_error(TSS2_FAPI_RC_BAD_VALUE, "Invalid hash name.");
    }
    *offset += alg_name_size + 2; /**< skip : and '\0' */
    digest_size = EVP_MD_size(md);
    if (alg_name_size + 2 + digest_size != digest_buffer_size) {
        return_error(TSS2_FAPI_RC_BAD_VALUE, "Invalid IMA binary format.");
    }

    LOGBLOB_TRACE(&buffer[*offset], digest_size, "IMA data_hash");

    if (jso && zero_digest(digest, template->hash_size) &&
        zero_digest(&buffer[*offset], digest_size)) {
        r = set_ff_digest(jso);
        return_if_error(r, "Set 0xff in digest.");
    }
    *offset += digest_size;
    return TSS2_RC_SUCCESS;
}

/** Callback to get digest with size field (UINT32).
 */
static TSS2_RC
signature_cb(UINT8 *digest, UINT8 *buffer, size_t *offset, json_object *jso,
             IFAPI_IMA_TEMPLATE *template) {
    UNUSED(digest);
    UNUSED(jso);
    UINT32 digest_size;
    UNUSED(template);

    digest_size =  get_size_from_buffer(buffer, offset);
    LOGBLOB_TRACE(&buffer[*offset], digest_size, "IMA Signature:");
    *offset += digest_size;
    return TSS2_RC_SUCCESS;
}

/** Callback to get null terminated name with size field (n-ng).
 */
static TSS2_RC eventname_ng_json_cb(UINT8 *digest, UINT8 *buffer, size_t *offset, json_object *jso,
                                    IFAPI_IMA_TEMPLATE *template) {
    size_t size;
    UINT32 size_from_buffer;
    UNUSED(digest);
    UNUSED(jso);

    /* Get size from buffer without 0 Terminator. */
    size_from_buffer = get_size_from_buffer(buffer, offset) - 1;
    size = strlen((const char *)&buffer[*offset]);
    if (size != size_from_buffer) {
        return_error2(TSS2_FAPI_RC_BAD_VALUE,
                      "Invalid digest size, string length: %zu size from buffer: %"
                      PRIu32, size, size_from_buffer);
    }
    LOG_TRACE("IMA name: %s", (const char *)&buffer[*offset]);
    template->name = (char *)&buffer[*offset];
    *offset += size + 1; /**< with 0 terminator */
    return TSS2_RC_SUCCESS;
}

/** Callback to get null terminated name (n).
 */
static TSS2_RC eventname_cb(UINT8 *digest, UINT8 *buffer, size_t *offset, json_object *jso,
                            IFAPI_IMA_TEMPLATE *template) {
    size_t size;
    UNUSED(digest);
    UNUSED(jso);

    size = strlen((const char *)&buffer[*offset]); // TODO check
    if (size > TCG_EVENT_NAME_LEN_MAX + 1) {
        return_error(TSS2_FAPI_RC_BAD_VALUE, "Too long event name.");
    }
    LOG_TRACE("IMA name: %s", (const char *)&buffer[*offset]);
    template->name =  (char *)&buffer[*offset];
    *offset += size + 1; /**< with 0 terminator */
    return TSS2_RC_SUCCESS;
}

/** Callback to initialize the json event list.
 */
TSS2_RC
init_event_list_json_cb(json_object **jso) {
    return_if_null(jso, "Bad reference.", TSS2_FAPI_RC_BAD_VALUE);
    if (!*jso) {
        *jso = json_object_new_array();
        return_if_null(*jso, "Out of memory", TSS2_FAPI_RC_MEMORY);
    }
    return TSS2_RC_SUCCESS;
}

/** Callback to convert header of IMA template to JSON.
 */
TSS2_RC
event_header_json_cb(
    size_t recnum,
    UINT32 pcr,
    const char* ima_type,
    UINT8 *digest,
    size_t digest_size,
    json_object *jso_list,
    json_object **jso)
{
    TSS2_RC r;
    json_object *jso_digest, *jso_digest_type, *jso_ary, *jso_content;
    char *hash_name;

    *jso = json_object_new_object();
    return_if_null(*jso, "Out of memory.", TSS2_FAPI_RC_MEMORY);

    r = add_number_to_json(recnum, *jso, "recnum");
    return_if_error(r, "Add number to json object.");

    r = add_number_to_json(pcr, *jso, "pcr");
    return_if_error(r, "Add number to json object.");

    jso_digest = json_object_new_object();
    return_if_null(*jso, "Out of memory.", TSS2_FAPI_RC_MEMORY);

    jso_digest_type = NULL;
    switch (digest_size) {
        case TPM2_SHA1_DIGEST_SIZE:
            hash_name = "sha1";
            break;
        case TPM2_SHA256_DIGEST_SIZE:
            hash_name = "sha256";
            break;
        case TPM2_SHA384_DIGEST_SIZE:
            hash_name = "sha384";
            break;
        case TPM2_SHA512_DIGEST_SIZE:
            hash_name = "sha512";
            break;
        default:
            return_error2(TSS2_FAPI_RC_BAD_VALUE, "Invalid hash size %zu",
                          digest_size);
    }

    jso_digest_type = json_object_new_string (hash_name);
    return_if_null(jso_digest_type, "Out of memory.", TSS2_FAPI_RC_MEMORY);

    json_object_object_add(jso_digest, "hashAlg", jso_digest_type);

    jso_ary = json_object_new_array();
    return_if_null(jso_ary, "Out of memory.", TSS2_FAPI_RC_MEMORY);

    json_object_array_add(jso_ary, jso_digest);
    json_object_object_add(*jso, "digests", jso_ary);

    r = add_uint8_ary_to_json(digest, digest_size, jso_digest, "digest");
    return_if_error(r, "Add digest to json");

    r = add_string_to_json("ima_template", *jso, CONTENT_TYPE);
    return_if_error(r, "Add number to json object.");

    r = get_json_content(*jso, &jso_content);
    return_if_error(r, "Get sub event");

    r = add_string_to_json(ima_type, jso_content, "template_name");
    return_if_error(r, "Add number to json object.");

    json_object_array_add(jso_list, *jso);
    return TSS2_RC_SUCCESS;
}

/* Type to store field data and the field callback */
struct template_field {
    const char *field_id;
    TSS2_RC (*field_cb) (UINT8 *digest, UINT8 *buffer, size_t *offset, json_object *jso,
                         IFAPI_IMA_TEMPLATE *template);
};

/* Type for storing the IMA template descriptor */
struct template_description {
    char *ima_type;
    char *format;
};

/* Callbacks to initialize result list and add events to the list */
struct event_callbacks {
    TSS2_RC (*init_list_cb) (json_object **jso);
    TSS2_RC (*add_header_cb) (size_t recnum,
                              UINT32 pcr,
                              const char* ima_type,
                              UINT8 *digest,
                              size_t digest_size,
                              json_object *jso_list,
                              json_object **jso_current_event);
};

static struct event_callbacks event_callbacks = {
    .init_list_cb = init_event_list_json_cb,
    .add_header_cb = event_header_json_cb
};

/*
 * Supported Descriptors and Template Fields.
 */
static struct template_description template_tab[] = {
    { .ima_type = "ima",
      .format = "d|n"},
    { .ima_type = "ima-ng",
      .format = "d-ng|n-ng"},
    { .ima_type = "ima-sig",
      .format = "d-ng|n-ng|sig"}
};

static struct template_field field_tab[] = {
    { .field_id = "d",
      .field_cb = sha_digest_json_cb },
    { .field_id = "n",
      .field_cb = eventname_cb },
    { .field_id = "d-ng",
      .field_cb = digest_with_hash_name_cb},
    { .field_id = "n-ng",
      .field_cb = eventname_ng_json_cb},
    { .field_id = "sig",
      .field_cb = signature_cb},
};

/**  Convert the IMA event to output format.
 *
 * Based on the event description in the ima template the appropriate callbacks are
 * determined and executed to generate the ouput.
 *
 * @param[in] template The IMA event.
 * @param[out] jso The output object.
 * @param[out] name The name of the event object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE If the current template foramt can't be processed.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 */
static TSS2_RC
convert_ima_event_buffer(
    IFAPI_IMA_TEMPLATE *template,
    json_object *jso,
    char **name)
{
    TSS2_RC r;
    size_t offset = 0;
    size_t i, j;
    char *copy_of_template_format = NULL;
    char *copy_of_template_format_orig = NULL;
    char *current_field;
    struct template_description *template_desc = NULL;
    size_t size_of_template_tab = sizeof(template_tab) / sizeof(template_tab[0]);
    size_t size_of_field_tab = sizeof(field_tab) / sizeof(field_tab[0]);
    json_object *jso_content;

    /* Search template decription corresponding to the template type. */
    for (i = 0; i < size_of_template_tab; i++) {
        if (strcmp(template->ima_type, template_tab[i].ima_type) == 0) {
            template_desc = template_tab + i;
            break;
        }
    }

    if (i == size_of_template_tab) {
        return_error(TSS2_FAPI_RC_BAD_VALUE, "Ima template type not supported.");
    }

    copy_of_template_format = strdup(template_desc->format);
    /* Save pointer for cleanup. */
    copy_of_template_format_orig = copy_of_template_format;
    goto_if_null(copy_of_template_format, "Out of memory.", TSS2_FAPI_RC_MEMORY, error);
    /* Loop over template fields separated by | */
    for (i = 0; (current_field = strsep(&copy_of_template_format, "|")) != NULL; i++) {
        struct template_field *field = NULL;

        for (j = 0; j < size_of_field_tab; j++) {
            if (!strcmp(current_field, field_tab[j].field_id)) {
                field = field_tab + j;
                break;
            }
        }

        goto_if_null2(field, "Unknown field %s", r, TSS2_FAPI_RC_BAD_VALUE, error, current_field);

        /* Convert the IMA data with the found callback. */
        r = field->field_cb(&template->header.digest[0],
                            template->event_buffer, &offset, jso, template);
        *name= template->name;
        goto_if_error(r, "Get field", error);
    }
    if (jso) {
        r = get_json_content(jso, &jso_content);
        goto_if_error(r, "Get sub event", error);

        r = add_uint8_ary_to_json(template->event_buffer, template->event_size, jso_content, "template_value");
        goto_if_error(r, "Create data to be hashed", error);
    }

    SAFE_FREE(copy_of_template_format_orig);
    return TSS2_RC_SUCCESS;
error:
    SAFE_FREE(copy_of_template_format_orig);
    return r;
}

/** Get one event from the event file.
 *
 * Retrieve the part of the event behind the fixed event header from the
 * event file.
 *
 * @param[in,out] template The IMA event with the already read event header.
 *                the storage for the rest of the event will be allocated
 *                and stored in the template.
 * @param[in] fp The event stream.
 *
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 */
static TSS2_RC
read_event_buffer(IFAPI_IMA_TEMPLATE *template, FILE *fp)
{
    bool old_ima_format;
    int size, rsize;

    /* Check IMA  legacy format. */
    if (strcmp(template->ima_type, "ima") == 0) {
        old_ima_format = true;
         /* Size is fixed for old IMA format. */
        template->event_size = TPM2_SHA1_DIGEST_SIZE + TCG_EVENT_NAME_LEN_MAX + 1;
        size = TPM2_SHA1_DIGEST_SIZE;
    } else {
        old_ima_format = false;
        /* For the new IMA format get size from event. */
        rsize = fread(&template->event_size, sizeof(UINT32), 1, fp);
        if (rsize != 1) {
            return_error(TSS2_FAPI_RC_BAD_VALUE, "Invalid ima data");
        }
        size = template->event_size;
    }

    template->event_buffer = calloc(template->event_size, sizeof(UINT8));
    return_if_null(template->event_buffer, "Out of memory", TSS2_FAPI_RC_MEMORY);

    rsize = fread(template->event_buffer, size, 1, fp);
    if (rsize != 1) {
        return_error(TSS2_FAPI_RC_BAD_VALUE, "Invalid ima data");
    }
    if (old_ima_format) {
        UINT32 field_len;

        rsize = fread(&field_len, sizeof(UINT32), 1, fp);
        if (rsize != 1) {
            return_error(TSS2_FAPI_RC_BAD_VALUE, "Invalid ima data");
        }
        if (field_len > template->event_size - TPM2_SHA1_DIGEST_SIZE) {
             return_error(TSS2_FAPI_RC_BAD_VALUE, "Invalid ima data");
        }
        rsize = fread(template->event_buffer +TPM2_SHA1_DIGEST_SIZE,
                      field_len, 1, fp);
        if (rsize != 1) {
            return_error(TSS2_FAPI_RC_BAD_VALUE, "Invalid ima data");
        }
    }
    return TSS2_RC_SUCCESS;
}

size_t read_ima_header(IFAPI_IMA_TEMPLATE *template, FILE *fp, TSS2_RC *rc)
{
    /* header: pcr register, sha1 digest, size field ima type string, start of ima type */
    size_t header_size = sizeof(UINT32) + TPM2_SHA1_DIGEST_SIZE + sizeof(UINT32) + 3;
    size_t size, rsize;
    size_t pos_ima_type = header_size - 3 - sizeof(UINT32);

    *rc = TSS2_RC_SUCCESS;

    size = fread(&template->header, header_size, 1, fp);
    if (size == 0) {
        return size;
    }
    if (memcmp(&template->header.digest[pos_ima_type], "ima", 3) == 0) {
        /* Start of IMA type string found. */
        memcpy(&template->ima_type_size,
               &template->header.digest[pos_ima_type - sizeof(UINT32)],
               sizeof(UINT32));
        memcpy(&template->ima_type[0], "ima", 3);
        /* Get the description of the IMA event. */
        size = template->ima_type_size - 3;
        if (size > 0) {
            if (size > TCG_EVENT_NAME_LEN_MAX) {
                LOG_ERROR("Invalid ima data");
                *rc = TSS2_FAPI_RC_BAD_VALUE;
                return 0;
            }
            rsize = fread(&template->ima_type[3], size, 1, fp);
            if (rsize != 1) {
                LOG_ERROR("Invalid ima data");
                *rc = TSS2_FAPI_RC_BAD_VALUE;
                return 0;
            }
        }
        template->ima_type[template->ima_type_size] = '\0';
        template->hash_alg =  TPM2_ALG_SHA1;
        template->hash_size = TPM2_SHA1_DIGEST_SIZE;
        return header_size;
    }
    return 0;
}

/** Read ima eventlog and create JSON list of events.
 *
 * @param[in] filename The filname of the IMA event file.
 * @param[in] pcrList The list of PCRs that are to be quoted
 * @param[in] pcrListSize The size of pcrList in bytes
 * @param[out] The event_list in JSON format.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_IO_ERROR If a event cannot be read.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory for
 *         internal operations or return parameters.
 */
TSS2_RC
ifapi_read_ima_event_log(
    const char *filename,
    const uint32_t *pcrList,
    size_t  pcrListSize,
    json_object **jso_list) {
    TSS2_RC r;
    FILE *fp = NULL;
    IFAPI_IMA_TEMPLATE template;
    size_t recnum = 0, i;
    json_object *jso_current_event = NULL;;
    bool add_event;

    return_if_null(jso_list, "Bad reference.", TSS2_FAPI_RC_BAD_VALUE);
    template.event_buffer = NULL;

    OpenSSL_add_all_digests();
    fp = fopen(filename, "r");
    goto_if_null2(fp, "Could not open: %s", r, TSS2_FAPI_RC_IO_ERROR, error, filename);
    LOG_INFO("IMA read file: %s", filename);

    r = event_callbacks.init_list_cb(jso_list);
    goto_if_error(r, "Initialize event list.", error);

    /* While the event header with fixed size can be read. */
    while (read_ima_header(&template, fp, &r)) {
        if (r) {
            return_error(r, "Invalid ima data.")
        }
        add_event = true;
        if (!template.ima_type_size ||
            template.ima_type_size > TCG_EVENT_NAME_LEN_MAX) {
            goto_error(r, TSS2_FAPI_RC_BAD_VALUE, "Invalid ima type size", error);
        }

        /* Check whether IMA PCR is member of pcrList. */
        for (i = 0; i < pcrListSize; i++) {
            if (pcrList[i] == template.header.pcr)
                break;
        }
        if (i == pcrListSize) {
            /* PCR  is not used. */
            add_event = false;
        }

        if (add_event) {
            r = event_callbacks.add_header_cb(recnum, template.header.pcr,
                                              template.ima_type, template.header.digest,
                                              template.hash_size,
                                              *jso_list, &jso_current_event);
            goto_if_error(r, "Add header to event list.", error);

            recnum += 1;
        }

        /* Read the rest of the event. */
        r = read_event_buffer(&template, fp);
        goto_if_error(r, "Read event buffer.", error);

        if (add_event) {
            char *name;
            r = convert_ima_event_buffer(&template, jso_current_event, &name);
            goto_if_error(r, "Create json event.", error);
        }
        SAFE_FREE(template.event_buffer);

    }
    fclose(fp);
    return TSS2_RC_SUCCESS;

 error:
    SAFE_FREE(template.event_buffer);
    if (fp)
        fclose(fp);
    if (*jso_list)
        json_object_put(*jso_list);
    return r;
}

static char *field_IFAPI_IMA_EVENT_tab[] = {
    "template_value",
    "template_name"
};

/** Deserialize a IFAPI_IMA_EVENT_TYPE json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 */
TSS2_RC
ifapi_json_IFAPI_IMA_EVENT_TYPE_deserialize(json_object *jso, IFAPI_IMA_EVENT_TYPE *out)
{
    LOG_TRACE("call");
    return ifapi_json_IFAPI_IMA_EVENT_TYPE_deserialize_txt(jso, out);
}

typedef struct {
    IFAPI_IMA_EVENT_TYPE in;
    char *name;
} IFAPI_IFAPI_IMA_EVENT_TYPE_ASSIGN;

static IFAPI_IFAPI_IMA_EVENT_TYPE_ASSIGN deserialize_IFAPI_IMA_EVENT_TYPE_tab[] = {
    { IFAPI_IMA_EVENT_TAG_IMA, "ima" },
    { IFAPI_IMA_EVENT_TAG_NG, "ima-ng" },
    { IFAPI_IMA_EVENT_TAG_SIG, "ima-sig" },
};

/**  Deserialize a json object of type IFAPI_IMA_EVENT_TYPE.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 */
TSS2_RC
ifapi_json_IFAPI_IMA_EVENT_TYPE_deserialize_txt(json_object *jso,
        IFAPI_IMA_EVENT_TYPE *out)
{
    LOG_TRACE("call");
    const char *token = json_object_get_string(jso);
    size_t i;
    size_t n = sizeof(deserialize_IFAPI_IMA_EVENT_TYPE_tab) /
        sizeof(deserialize_IFAPI_IMA_EVENT_TYPE_tab[0]);
    size_t size = strlen(token);
    for (i = 0; i < n; i++) {
        if (strncasecmp(&token[0],
                        &deserialize_IFAPI_IMA_EVENT_TYPE_tab[i].name[0],
                        size) == 0) {
            *out = deserialize_IFAPI_IMA_EVENT_TYPE_tab[i].in;
            return TSS2_RC_SUCCESS;
        }
    }
    return_error(TSS2_FAPI_RC_BAD_VALUE, "Undefined constant.");
}

/** Deserialize a IFAPI_IMA_EVENT json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 */
TSS2_RC
ifapi_json_IFAPI_IMA_EVENT_deserialize(json_object *jso,  IFAPI_IMA_EVENT *out)
{
    json_object *jso2;
    TSS2_RC r;

    LOG_TRACE("call");
    return_if_null(out, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    ifapi_check_json_object_fields(jso, &field_IFAPI_IMA_EVENT_tab[0],
                                   SIZE_OF_ARY(field_IFAPI_IMA_EVENT_tab));

    if (!ifapi_get_sub_object(jso, "template_name", &jso2)) {
        LOG_ERROR("Field \"template_value\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_IFAPI_IMA_EVENT_TYPE_deserialize(jso2, &out->template_name);
    return_if_error(r, "Bad value for field \"template_name\".");

    if (!ifapi_get_sub_object(jso, "template_value", &jso2)) {
        LOG_ERROR("Field \"template_value\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_UINT8_ARY_deserialize(jso2, &out->template_value);
    return_if_error(r, "Bad value for field \"template_valuse\".");

    LOG_TRACE("true");
    return TSS2_RC_SUCCESS;
}

TSS2_RC
ifapi_get_ima_eventname(IFAPI_IMA_EVENT *ima_event, char **name)
{
    TSS2_RC r;
    IFAPI_IMA_TEMPLATE template;
    size_t i;
    size_t n = SIZE_OF_ARY(deserialize_IFAPI_IMA_EVENT_TYPE_tab);

    memset(&template, 0, sizeof(template));
    for (i = 0; i < n; i++) {
        if (deserialize_IFAPI_IMA_EVENT_TYPE_tab[i].in ==
            ima_event->template_name) {
            char *tab_name = deserialize_IFAPI_IMA_EVENT_TYPE_tab[i].name;
            memcpy(&template.ima_type, tab_name, strlen(tab_name)+1);
            break;
        }
    }
    if (i >= n) {
        return_error(TSS2_FAPI_RC_BAD_VALUE, "Undefined constant.");
    }
    template.event_size = ima_event->template_value.size;
    template.event_buffer = &ima_event->template_value.buffer[0];
    r = convert_ima_event_buffer(&template, NULL, name);
    return_if_error(r, "Parsing of IMA template failed.");

    return TSS2_RC_SUCCESS;
}
