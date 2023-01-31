/* SPDX-License-Identifier: BSD-2-Clause */
/*******************************************************************************
 * Copyright 2018-2019, Fraunhofer SIT sponsored by Infineon Technologies AG
 * All rights reserved.
 *******************************************************************************/
#ifndef IFAPI_IMA_EVENTLOG_H
#define IFAPI_IMA_EVENTLOG_H

#include <json-c/json.h>

#include "fapi_types.h"

/* Defines from kernel ima.h" */
#define TCG_EVENT_NAME_LEN_MAX 255
#define IMA_TEMPLATE_FIELD_ID_MAX_LEN 16
#define IMA_TEMPLATE_NUM_FIELDS_MAX	15

/* Define from kernel crypt.h */
#define CRYPTO_MAX_ALG_NAME 128

typedef UINT32 IFAPI_IMA_EVENT_TYPE;
#define IFAPI_IMA_EVENT_TAG_IMA        1   /**< Tag for IMA type "ima" */
#define IFAPI_IMA_EVENT_TAG_NG         2   /**< Tag for IMA type "ima-ng" */
#define IFAPI_IMA_EVENT_TAG_SIG        3   /**< Tag for IMT type "sig"*/

/* Structure to store event header and data of IMA template */
typedef struct {
    /* header is the First part of the template which will be read
       beforte the rest of the event will be read and parsed. */
    struct {
        UINT32 pcr;
        UINT8  digest[TPM2_SHA512_DIGEST_SIZE + sizeof(UINT32) + 3];
    } header;
    UINT32 ima_type_size;
    size_t hash_size;
    TPMI_ALG_HASH hash_alg;
    char ima_type[TCG_EVENT_NAME_LEN_MAX + 1];
    char *name;
    UINT32 event_size;
    UINT8 *event_buffer; /**< The data after header and name */
} IFAPI_IMA_TEMPLATE;

/** IMA event information
 */
typedef struct {
    IFAPI_IMA_EVENT_TYPE template_name;
    UINT8_ARY template_value;    /**< The value to be hashed. */
} IFAPI_IMA_EVENT;

TSS2_RC
ifapi_json_IFAPI_IMA_EVENT_deserialize(json_object *jso,  IFAPI_IMA_EVENT *out);

TSS2_RC
ifapi_json_IFAPI_IMA_EVENT_TYPE_deserialize_txt(json_object *jso,
                                                IFAPI_IMA_EVENT_TYPE *out);

TSS2_RC ifapi_read_ima_event_log(
    const char   *filename,
    const uint32_t *pcrList,
    const size_t  pcrListSize,
    json_object **jso_list);

TSS2_RC
ifapi_get_ima_eventname(IFAPI_IMA_EVENT *event, char **name);

#endif /* IFAPI_IMA_EVENTLOG_H */
