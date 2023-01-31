/* SPDX-License-Identifier: BSD-2-Clause */
/*******************************************************************************
 * Copyright 2018-2019, Fraunhofer SIT sponsored by Infineon Technologies AG
 * All rights reserved.
 ******************************************************************************/

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <stdio.h>
#include <stdlib.h>
#include <inttypes.h>
#include <strings.h>
#include <string.h>
#include <uchar.h>
#include <uuid/uuid.h>
#include <uchar.h>

#include "tss2_common.h"
#include "tpm_json_deserialize.h"
#include "ifapi_json_serialize.h"
#include "ifapi_eventlog_system.h"
#include "ifapi_json_eventlog_serialize.h"
#include "fapi_crypto.h"
#include "tpm_json_serialize.h"
#include "tss2_tpm2_types.h"
#define LOGMODULE fapifirmware
#include "util/log.h"
#include "util/aux_util.h"

bool ifapi_pcr_used(uint32_t pcr, const uint32_t *pcr_list,  size_t pcr_list_size)
{
    size_t i;

    if (pcr_list_size) {
        for (i = 0; i < pcr_list_size; i++) {
            if (pcr_list[i] == pcr)
               return true;
        }
    } else {
        return true;
    }
    return false;
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

char const *eventtype_to_string (UINT32 event_type) {
    switch (event_type) {
    case EV_PREBOOT_CERT:
        return "EV_PREBOOT_CERT";
    case EV_POST_CODE:
        return "EV_POST_CODE";
    case EV_UNUSED:
        return "EV_UNUSED";
    case EV_NO_ACTION:
        return "EV_NO_ACTION";
    case EV_SEPARATOR:
        return "EV_SEPARATOR";
    case EV_ACTION:
        return "EV_ACTION";
    case EV_EVENT_TAG:
        return "EV_EVENT_TAG";
    case EV_S_CRTM_CONTENTS:
        return "EV_S_CRTM_CONTENTS";
    case EV_S_CRTM_VERSION:
        return "EV_S_CRTM_VERSION";
    case EV_CPU_MICROCODE:
        return "EV_CPU_MICROCODE";
    case EV_PLATFORM_CONFIG_FLAGS:
        return "EV_PLATFORM_CONFIG_FLAGS";
    case EV_TABLE_OF_DEVICES:
        return "EV_TABLE_OF_DEVICES";
    case EV_COMPACT_HASH:
        return "EV_COMPACT_HASH";
    case EV_IPL:
        return "EV_IPL";
    case EV_IPL_PARTITION_DATA:
        return "EV_IPL_PARTITION_DATA";
    case EV_NONHOST_CODE:
        return "EV_NONHOST_CODE";
    case EV_NONHOST_CONFIG:
        return "EV_NONHOST_CONFIG";
    case EV_NONHOST_INFO:
        return "EV_NONHOST_INFO";
    case EV_OMIT_BOOT_DEVICE_EVENTS:
        return "EV_OMIT_BOOT_DEVICE_EVENTS";
    case EV_EFI_VARIABLE_DRIVER_CONFIG:
        return "EV_EFI_VARIABLE_DRIVER_CONFIG";
    case EV_EFI_VARIABLE_BOOT:
        return "EV_EFI_VARIABLE_BOOT";
    case EV_EFI_BOOT_SERVICES_APPLICATION:
        return "EV_EFI_BOOT_SERVICES_APPLICATION";
    case EV_EFI_BOOT_SERVICES_DRIVER:
        return "EV_EFI_BOOT_SERVICES_DRIVER";
    case EV_EFI_RUNTIME_SERVICES_DRIVER:
        return "EV_EFI_RUNTIME_SERVICES_DRIVER";
    case EV_EFI_GPT_EVENT:
        return "EV_EFI_GPT_EVENT";
    case EV_EFI_ACTION:
        return "EV_EFI_ACTION";
    case EV_EFI_PLATFORM_FIRMWARE_BLOB:
        return "EV_EFI_PLATFORM_FIRMWARE_BLOB";
    case EV_EFI_HANDOFF_TABLES:
        return "EV_EFI_HANDOFF_TABLES";
    case EV_EFI_HCRTM_EVENT:
        return "EV_EFI_HCRTM_EVENT";
    case EV_EFI_VARIABLE_AUTHORITY:
        return "EV_EFI_VARIABLE_AUTHORITY";
    default:
        return "Unknown event type";
    }
}

/** Serialize value of type UINT8_ARY to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TPM2B_DIGEST.
 */
TSS2_RC ifapi_json_BYTE_ARY_serialize(const uint8_t *buffer, size_t size,json_object **jso)
{
    return_if_null(buffer, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    char hex_string[(size)*2+1];
    for (size_t i = 0, off = 0; i < size; i++, off+=2)
        sprintf(&hex_string[off], "%02x", buffer[i]);
    hex_string[size * 2] = '\0';
    *jso = json_object_new_string (hex_string);
    return_if_null(*jso, "Out of memory.", TSS2_FAPI_RC_MEMORY);

    return TSS2_RC_SUCCESS;
}

/** Serialize a base_type UINT8 to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type UINT16.
 */
TSS2_RC
ifapi_json_UINT8_serialize(const UINT8 in, json_object **jso)
{
    *jso = json_object_new_int64(in);
    if (*jso == NULL) {
        LOG_ERROR("Bad value %04"PRIx16"", in);
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    return TSS2_RC_SUCCESS;
}


/** Serialize value of type TCG_DIGEST2 to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TCG_DIGEST2.
 */
TSS2_RC ifapi_json_TCG_DIGEST2_serialize(const TCG_DIGEST2 *in, json_object **jso)
{
    return_if_null(in, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    TSS2_RC r;
    json_object *jso2;
    size_t size;

    if (*jso == NULL) {
        *jso = json_object_new_object();
         return_if_null(*jso, "Out of memory.", TSS2_FAPI_RC_MEMORY);
    }

    jso2 = NULL;
    r = ifapi_json_TPM2_ALG_ID_serialize(in->AlgorithmId, &jso2);
    return_if_jso_error(r, "Serialize hash algorithm", jso2);

    json_object_object_add(*jso, "hashAlg", jso2);
    jso2 = NULL;

    size = ifapi_hash_get_digest_size(in->AlgorithmId);
    r = ifapi_json_BYTE_ARY_serialize(&in->Digest[0], size, &jso2);
    return_if_jso_error(r, "Serialize UINT8", jso2);

    json_object_object_add(*jso, "digest", jso2);
    return TSS2_RC_SUCCESS;
}


bool ifapi_json_TCG_DIGEST2_cb(const TCG_DIGEST2 *in, size_t size, void *data)
{
    TSS2_RC r;
    json_object *jso = NULL;
    json_object *jso_digests, *jso_digest;
    callback_data *cb_data = data;
    json_object *jso_event_list = cb_data->jso_event_list;
    size_t number_of_events;
    (void)size;

    LOG_TRACE("call");

    if (cb_data->skip_event)
        return true;

    number_of_events = json_object_array_length(jso_event_list);

    jso = json_object_array_get_idx(jso_event_list, number_of_events - 1);

    if (!ifapi_get_sub_object(jso, "digests", &jso_digests)) {
        LOG_ERROR("Digest list expected.");
        return false;
    }

    jso_digest = NULL;
    r = ifapi_json_TCG_DIGEST2_serialize(in, &jso_digest);
    if (r) {
        JSON_CLEAR(jso_digest);
        return false;
    }

    json_object_array_add(jso_digests, jso_digest);
    return true;
}

/** Check event field is string with or without NULL terminator.
 */
static TSS2_RC
check_event_string(const TCG_EVENT2 *in, const char *string) {
    if (strncmp((const char *)&in->Event[0], string, strlen(string)) != 0) {
        return_error2(TSS2_FAPI_RC_BAD_VALUE, "Invalid event string. %s expected", string);
    }
    if (in->EventSize == strlen(string)) {
        /* String without NULL terminator */
        return TSS2_RC_SUCCESS;
    }
    if  (in->EventSize == strlen(string) + 1 &&
         in->Event[strlen(string)] == '\0') {
        /* String with NULL terminator */
        return TSS2_RC_SUCCESS;
    }
    return_error2(TSS2_FAPI_RC_BAD_VALUE, "Invalid event string. %s expected", string);
}

#if MAXLOGLEVEL >= LOGL_TRACE
/** Trace value of unicode name.
 *
 * @param[in] UnicodeName to be traced.
 * @param[in] UnicodeNameLength size of UnicodeName
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type UEFI_VARIABLE_DATA.
 */
TSS2_RC trace_unicodename(
    const char16_t *UnicodeName,
    UINT64 UnicodeNameLength)
{
    int ret = 0;
    char *mbstr = NULL, *tmp = NULL;
    mbstate_t st;

    memset(&st, '\0', sizeof(st));

    mbstr = tmp = calloc(UnicodeNameLength + 1, MB_CUR_MAX);
    if (mbstr == NULL) {
        LOG_ERROR("failed to allocate data: %s\n", strerror(errno));
        return TSS2_FAPI_RC_BAD_VALUE;
    }

    for(size_t i = 0; i < UnicodeNameLength; ++i, tmp += ret) {
        ret = c16rtomb(tmp, UnicodeName[i], &st);
        if (ret < 0) {
            LOG_ERROR("c16rtomb failed: %s", strerror(errno));
            free(mbstr);
            return TSS2_FAPI_RC_BAD_VALUE;
        }
    }
    LOG_TRACE("FIRMWARE UnicodeName %s", mbstr);
    free(mbstr);

    return TSS2_RC_SUCCESS;
}
#endif /* Loglevel trace */

/** Serialize value of type TCG_EVENT2 to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TCG_EVENT2.
 */
TSS2_RC ifapi_json_TCG_EVENT2_serialize(const TCG_EVENT2 *in, UINT32 event_type, json_object **jso)
{
    return_if_null(in, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    TSS2_RC r;
    json_object *jso2 = NULL;

    if (*jso == NULL) {
        *jso = json_object_new_object();
        return_if_null(*jso, "Out of memory.", TSS2_FAPI_RC_MEMORY);
    }
    jso2 = NULL;

    switch (event_type) {
    case EV_EFI_HCRTM_EVENT:
        r = check_event_string(in, "HCRTM");
        return_if_error(r, "Check event string.");
        break;
    case EV_OMIT_BOOT_DEVICE_EVENTS:
          r = check_event_string(in, "BOOT ATTEMPTS OMITTED");
          return_if_error(r, "Check event string.");
          break;
    /* TCG PC Client FPF section 9.2.6 */
    case EV_EFI_VARIABLE_DRIVER_CONFIG:
    case EV_EFI_VARIABLE_BOOT:
    case EV_EFI_VARIABLE_AUTHORITY:
        {
#if (MAXLOGLEVEL != LOGL_NONE)
            UEFI_VARIABLE_DATA *data = (UEFI_VARIABLE_DATA*)in->Event;
            BYTE *variableData;
            char uuidstr[37] = { 0 };

            if (in->EventSize < sizeof(*data)) {
                LOG_ERROR("size is insufficient for UEFI variable data");
                return false;
            }

            UINT64 size_name = (UINT64)data->UnicodeNameLength;
            UINT64 size_vdata = (UINT64)data->VariableDataLength;

            if  (size_name > UINT64_MAX / sizeof(UTF16_CHAR) ||
                 size_name * sizeof(UTF16_CHAR) > UINT64_MAX - size_vdata ||
                 size_name + size_vdata > UINT64_MAX - sizeof(*data) ||
                in->EventSize < (in->EventSize < sizeof(*data) + data->UnicodeNameLength *
                                 sizeof(UTF16_CHAR) + data->VariableDataLength))
            {
                LOG_ERROR("size is insufficient for UEFI variable data");
                return false;
            }

            uuid_unparse_lower(data->VariableName, uuidstr);
            LOG_TRACE("FIRMWARE VariableName: %s", uuidstr);
            char16_t *name = malloc(size_name * sizeof(char16_t));
            return_if_null(name, "Out of memory.", TSS2_FAPI_RC_MEMORY);
            memcpy(name, &data->UnicodeName[0], data->UnicodeNameLength  * sizeof(char16_t));
            return_if_null(name, "Out of memory", TSS2_FAPI_RC_MEMORY);

            r = trace_unicodename(name, size_name);
            SAFE_FREE(name);
            return_if_error(r, "Trace unicodename");

            variableData = (BYTE *)&data->UnicodeName + data->UnicodeNameLength * sizeof(char16_t);
            LOGBLOB_TRACE(variableData, data->VariableDataLength, "FIRMWARE VariableData:");
#endif
        }
        break;
    /* TCG PC Client FPF section 2.3.4.1 and 9.4.1 */
    case EV_POST_CODE:
        // the event is a string, so there are no length requirements.
        break;
    /* TCG PC Client FPF section 9.2.5 */
    case EV_S_CRTM_CONTENTS:
    case EV_EFI_PLATFORM_FIRMWARE_BLOB:
        {
            UEFI_PLATFORM_FIRMWARE_BLOB *data =
                (UEFI_PLATFORM_FIRMWARE_BLOB*)in->Event;
            return_if_null(data, "Invalid UEFI data.", TSS2_FAPI_RC_BAD_VALUE);

            if (in->EventSize < sizeof(*data)) {
                LOG_ERROR("size is insufficient for UEFI FW blob data");
                return false;
            }

            LOG_TRACE("FIRMWARE BlobBase: %"PRIu64, data->BlobBase);
            LOG_TRACE("FIRMWARE BlobLength: %"PRIu64, data->BlobLength);
        }
        break;
    case EV_EFI_BOOT_SERVICES_APPLICATION:
    case EV_EFI_BOOT_SERVICES_DRIVER:
    case EV_EFI_RUNTIME_SERVICES_DRIVER:
        {
            UEFI_IMAGE_LOAD_EVENT *data = (UEFI_IMAGE_LOAD_EVENT*)in->Event;
            return_if_null(data, "Invalid UEFI data.", TSS2_FAPI_RC_BAD_VALUE);

            if (in->EventSize < sizeof(*data) ||
                data->LengthOfDevicePath > UINT64_MAX - sizeof(*data) ||
                in->EventSize < sizeof(*data) + data->LengthOfDevicePath) {
                LOG_ERROR("size is insufficient for UEFI image load event");
                return false;
            }
            /* what about the device path? */
            LOG_TRACE("FIRMWARE ImageLocationInMemory: %"PRIu64, data->ImageLocationInMemory);
            LOG_TRACE("FIRMWARE ImageLengthInMemory: %"PRIu64, data->ImageLengthInMemory);
            LOG_TRACE("FIRMWARE ImageLinkTimeAddress: %"PRIu64, data->ImageLinkTimeAddress);
            LOGBLOB_TRACE(&data->DevicePath[0], data->LengthOfDevicePath, "DevicePath:");
        }
        break;
    }
    /* Check whether data has already been added (for legacy events). */
    if (!ifapi_get_sub_object(*jso, "event_data", &jso2)) {
        jso2 = NULL;
        r = ifapi_json_BYTE_ARY_serialize(&in->Event[0], in->EventSize, &jso2);
        return_if_jso_error(r, "Serialize UINT8", jso2);

        json_object_object_add(*jso, "event_data", jso2);
    }
        return TSS2_RC_SUCCESS;
}

bool ifapi_json_TCG_EVENT2_cb(const TCG_EVENT2 *in, UINT32 event_type, void *data)
{
    json_object *jso = NULL;
    callback_data *cb_data = data;
    json_object *jso_event_list = cb_data->jso_event_list;
    json_object *jso_sub = NULL;
    TSS2_RC r;
    size_t number_of_events;

    LOG_TRACE("call");

    if (cb_data->skip_event)
        return true;

    number_of_events = json_object_array_length(jso_event_list);

    jso = json_object_array_get_idx(jso_event_list, number_of_events - 1);

    if (!ifapi_get_sub_object(jso, CONTENT, &jso_sub)) {
        LOG_ERROR("content expected.");
        JSON_CLEAR(jso_sub);
        return  TSS2_FAPI_RC_BAD_VALUE;
    }
    r =  ifapi_json_TCG_EVENT2_serialize(in, event_type, &jso_sub);
    if (r) {
        return false;
    }

    return true;
}

/** Serialize value of type TCG_EVENT_HEADER2 to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TCG_EVENT_HEADER2.
 */
TSS2_RC ifapi_json_TCG_EVENT_HEADER2_serialize(
    const TCG_EVENT_HEADER2 *in,
    size_t size,
    size_t recnum,
    json_object **jso)
{
    (void)size;

    return_if_null(in, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    TSS2_RC r;
    json_object *jso2;
    json_object *jso_sub;
    json_object *jso_ary;

    if (*jso == NULL) {
        *jso = json_object_new_object();
        return_if_null(*jso, "Out of memory.", TSS2_FAPI_RC_MEMORY);
    }
    jso_sub = json_object_new_object();
    return_if_null(jso_sub, "Out of memory.", TSS2_FAPI_RC_MEMORY);
    json_object_object_add(*jso, CONTENT, jso_sub);

    r = add_string_to_json("pcclient_std", *jso, CONTENT_TYPE);
    return_if_error(r, "Add event type");

    r = ifapi_json_UINT32_serialize(in->PCRIndex, &jso2);
    return_if_error(r, "Serialize UINT32");

    json_object_object_add(*jso, "pcr", jso2);
    jso2 = NULL;

    jso2 = json_object_new_int64(recnum);
    return_if_null(jso2, "Out of memory.", TSS2_FAPI_RC_MEMORY);
    json_object_object_add(*jso, "recnum", jso2);

    jso2 = json_object_new_string(eventtype_to_string(in->EventType));

    json_object_object_add(jso_sub, "event_type", jso2);

    jso_ary = json_object_new_array();
    return_if_null(jso_ary, "Out of memory.", TSS2_FAPI_RC_MEMORY);
    json_object_object_add(*jso, "digests", jso_ary);

    return TSS2_RC_SUCCESS;
}

bool ifapi_json_TCG_EVENT_HEADER2_cb(
    const TCG_EVENT_HEADER2 *in,
    size_t size,
    void *data)
{
    TSS2_RC r;
    json_object *jso = NULL;
    callback_data *cb_data = data;
    json_object *jso_event_list = cb_data->jso_event_list;

    LOG_TRACE("call");

    cb_data->skip_event = true;

    cb_data->skip_event = !ifapi_pcr_used(in->PCRIndex, cb_data->pcr_list,
                                          cb_data->pcr_list_size);
    if (cb_data->skip_event)
        return true;

    r = ifapi_json_TCG_EVENT_HEADER2_serialize(in, size,
                                               cb_data->recnum_tab[in->PCRIndex],
                                               &jso);
    if (r) {
        JSON_CLEAR(jso);
        return false;
    }

    cb_data->recnum_tab[in->PCRIndex]++;

    json_object_array_add(jso_event_list, jso);
    return true;
}

/** Serialize value of type uuid_t to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type UEFI_VARIABLE_DATA.
 */
TSS2_RC ifapi_json_uuid_t_serialize(const uuid_t *in, json_object **jso) {
       char uuidstr[37] = { 0 };

       uuid_unparse_lower(*in, uuidstr);
       *jso = json_object_new_string (uuidstr);
       return_if_null(*jso, "Out of memory.", TSS2_FAPI_RC_MEMORY);

       return TSS2_RC_SUCCESS;
}

/** Serialize value of type TCG_EVENT to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TCG_EVENT.
 */
TSS2_RC ifapi_json_TCG_EVENT_serialize(const TCG_EVENT *in, size_t recnum, json_object **jso)
{
    return_if_null(in, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    TSS2_RC r;
    json_object *jso2, *jso_sub, *jso_digest, *jso_ary;

    if (*jso == NULL) {
        *jso = json_object_new_object();
        return_if_null(*jso, "Out of memory.", TSS2_FAPI_RC_MEMORY);
    }

    jso2 = NULL;
    r = add_string_to_json("pcclient_std", *jso, CONTENT_TYPE);
    return_if_error(r, "Add event type");

    r = ifapi_json_UINT32_serialize(in->pcrIndex, &jso2);
    return_if_error(r, "Serialize UINT32");

    json_object_object_add(*jso, "pcr", jso2);
    jso2 = json_object_new_int64(recnum);
    return_if_null(jso2, "Out of memory.", TSS2_FAPI_RC_MEMORY);

    json_object_object_add(*jso, "recnum", jso2);
    jso2 = json_object_new_string(eventtype_to_string(in->eventType));
    return_if_null(jso2, "Out of memory.", TSS2_FAPI_RC_MEMORY);

    jso_sub = json_object_new_object();
    return_if_null(jso_sub, "Out of memory.", TSS2_FAPI_RC_MEMORY);
    json_object_object_add(*jso, CONTENT, jso_sub);

    json_object_object_add(jso_sub, "event_type", jso2);

    jso_digest = json_object_new_object();
    return_if_null(*jso, "Out of memory.", TSS2_FAPI_RC_MEMORY);

    jso2 = NULL;
    r = ifapi_json_TPM2_ALG_ID_serialize(TPM2_ALG_SHA1, &jso2);
    return_if_error(r, "Serialize hash algorithm");

    json_object_object_add(jso_digest, "hashAlg", jso2);

    jso2 = NULL;
    r = ifapi_json_BYTE_ARY_serialize(&in->digest[0], 20, &jso2);
    return_if_error(r, "Serialize BYTE");

    json_object_object_add(jso_digest, "digest", jso2);

    jso_ary = json_object_new_array();
    return_if_null(jso_ary, "Out of memory.", TSS2_FAPI_RC_MEMORY);

    json_object_array_add(jso_ary, jso_digest);

    json_object_object_add(*jso, "digests", jso_ary);
    jso2 = NULL;
    r = ifapi_json_BYTE_ARY_serialize(&in->event[0], in->eventDataSize, &jso2);
    return_if_error(r, "Serialize BYTE");

    json_object_object_add(jso_sub, "event_data", jso2);
    return TSS2_RC_SUCCESS;
}

bool ifapi_json_TCG_EVENT_cb(const TCG_EVENT *in, size_t size, void *data)
{
    TSS2_RC r;
    json_object *jso = NULL;
    callback_data *cb_data = data;
    json_object *jso_event_list = cb_data->jso_event_list;
    (void)size;

    LOG_TRACE("call");

    cb_data->skip_event = !ifapi_pcr_used(in->pcrIndex, cb_data->pcr_list,
                                          cb_data->pcr_list_size);

    if (cb_data->skip_event)
        return true;

    r = ifapi_json_TCG_EVENT_serialize(in,
                                       cb_data->recnum_tab[in->pcrIndex],
                                       &jso);
    if (r) {
        JSON_CLEAR(jso);
        return false;
    }

     cb_data->recnum_tab[in->pcrIndex]++;

    json_object_array_add(jso_event_list, jso);
    return true;
}

/** Serialize value of type TCG_SPECID_ALG to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TCG_SPECID_ALG.
 */
TSS2_RC ifapi_json_TCG_SPECID_ALG_serialize(
    const TCG_SPECID_ALG *in,
    json_object **jso)
{
    return_if_null(in, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    TSS2_RC r;
    json_object *jso2;

    if (*jso == NULL) {
        *jso = json_object_new_object();
         return_if_null(*jso, "Out of memory.", TSS2_FAPI_RC_MEMORY);
    }

    jso2 = NULL;
    r = ifapi_json_TPM2_ALG_ID_serialize(in->algorithmId, &jso2);
    return_if_error(r, "Serialize UINT16");

    json_object_object_add(*jso, "algorithmId", jso2);
    jso2 = NULL;
    r = ifapi_json_UINT16_serialize(in->digestSize, &jso2);
    return_if_error(r, "Serialize UINT16");

    json_object_object_add(*jso, "digestSize", jso2);
    return TSS2_RC_SUCCESS;
}

/** Serialize value of type TCG_VENDOR_INFO to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TCG_VENDOR_INFO.
 */
TSS2_RC ifapi_json_TCG_VENDOR_INFO_serialize(const TCG_VENDOR_INFO *in, json_object **jso)
{
    return_if_null(in, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    TSS2_RC r;
    json_object *jso2;

    if (!in->vendorInfoSize)
        return TSS2_RC_SUCCESS;

    if (*jso == NULL) {
        *jso = json_object_new_object();
        return_if_null(*jso, "Out of memory.", TSS2_FAPI_RC_MEMORY);
    }

    jso2 = NULL;
    r = ifapi_json_BYTE_ARY_serialize(&in->vendorInfo[0], in->vendorInfoSize, &jso2);
    return_if_error(r, "Serialize BYTE");

    json_object_object_add(*jso, "vendorInfo", jso2);
    return TSS2_RC_SUCCESS;
}

/** Serialize value of type TCG_SPECID_EVENT to json.
 *
 * @param[in] in value to be serialized.
 * @param[out] jso pointer to the json object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the value is not of type TCG_SPECID_EVENT.
 */
TSS2_RC ifapi_json_TCG_SPECID_EVENT_serialize(const TCG_SPECID_EVENT *in, json_object **jso)
{
    return_if_null(in, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    size_t i;

    LOG_TRACE("call");

    if (*jso == NULL) {
        *jso = json_object_new_object();
         return_if_null(*jso, "Out of memory.", TSS2_FAPI_RC_MEMORY);
    }

    /* 'Signature' defined as byte buf, spec treats it like string w/o null. */
    char sig_str[sizeof(in->Signature) + 1] = { '\0', };
    memcpy(sig_str, in->Signature, sizeof(in->Signature));

    LOG_TRACE("Signature: %s", sig_str);
    LOG_TRACE("platformClass: %"PRIu32, in->platformClass);
    LOG_TRACE("specVersionMajor: %"PRIu8, in->specVersionMajor);
    LOG_TRACE("specVersionMinor: %"PRIu8, in->specVersionMinor);
    LOG_TRACE("specErrata: %"PRIu8, in->specErrata);
    LOG_TRACE("uintnSize: %"PRIu8, in->uintnSize);
    LOG_TRACE("specErrata: %"PRIu8, in->specErrata);
    LOG_TRACE("numberOfAlgorithms: %"PRIu32, in->numberOfAlgorithms);


    for (i = 0; i < in->numberOfAlgorithms; i++) {
        LOG_TRACE(" %zu AlgID: %"PRIu16, i, in->digestSizes[i].algorithmId);
        LOG_TRACE(" %zu DigestSize: %"PRIu16, i, in->digestSizes[i].digestSize);
    }
#if (MAXLOGLEVEL != LOGL_NONE)
    size_t offset = in->numberOfAlgorithms * sizeof(TCG_SPECID_ALG);
    TCG_VENDOR_INFO *vendor_info = (TCG_VENDOR_INFO *)&in->digestSizes[0] + offset;

    LOG_TRACE("vendorInfoSize: %"PRIu8, vendor_info->vendorInfoSize);
    LOGBLOB_TRACE(&vendor_info->vendorInfo[0], vendor_info->vendorInfoSize,
                  "vendorInfo");
#endif

    return TSS2_RC_SUCCESS;
}

bool ifapi_json_TCG_SPECID_EVENT_cb(
    const TCG_EVENT *tcg_event,
    void *data)
{
    TSS2_RC r;
    json_object *jso = NULL, *jso_sub;
    callback_data *cb_data = data;
    json_object *jso_event_list = cb_data->jso_event_list;
    TCG_SPECID_EVENT *event_specid = (TCG_SPECID_EVENT*)tcg_event->event;

    if (cb_data->skip_event)
        return true;

    if (!ifapi_pcr_used(0, cb_data->pcr_list,cb_data->pcr_list_size))
        /* PCR 0 not used */
        return true;

    r = ifapi_json_TCG_EVENT_serialize(tcg_event,
                                       cb_data->recnum_tab[0],
                                       &jso);
    if (r) {
        JSON_CLEAR(jso);
        return false;
    }

    cb_data->recnum_tab[0]++;

    if (!ifapi_get_sub_object(jso, CONTENT, &jso_sub)) {
        LOG_ERROR("content expected.");
        return  TSS2_FAPI_RC_BAD_VALUE;
    }

    r = ifapi_json_TCG_SPECID_EVENT_serialize(event_specid, &jso_sub);
    if (r) {
        JSON_CLEAR(jso_sub);
        return false;
    }

    json_object_array_add(jso_event_list, jso);
    return true;
}

typedef struct {
	json_object_iter *jso_event_list;
    const uint32_t *pcr_list;
    size_t size_of_pcr_list;
} cb_data;

TSS2_RC ifapi_tcg_eventlog_serialize(
    UINT8 const *eventlog,
    size_t size,
    const uint32_t *pcr_list,
    size_t  pcr_list_size,
    json_object **eventlog_json) {

    TSS2_RC r;
    size_t i;
    json_object *jso_ary = NULL;
    callback_data callback_data;

    tpm2_eventlog_context ctx = {
        .data = &callback_data,
        .specid_cb = ifapi_json_TCG_SPECID_EVENT_cb,
        .event2hdr_cb = ifapi_json_TCG_EVENT_HEADER2_cb,
        .log_eventhdr_cb = ifapi_json_TCG_EVENT_cb,
        .digest2_cb = ifapi_json_TCG_DIGEST2_cb,
        .event2_cb = ifapi_json_TCG_EVENT2_cb,
    };

    for (i = 1; i < TPM2_MAX_PCRS; i++)
        callback_data.recnum_tab[i] = 0;
    /* Set to one because the first element will be a cel_version. */
    callback_data.recnum_tab[0] = 1;

    callback_data.pcr_list = pcr_list;
    callback_data.pcr_list_size = pcr_list_size;
    callback_data.skip_event = false;

    /* Initialize JSON event list. */
    if (*eventlog_json) {
        jso_ary = *eventlog_json;
    } else {
        jso_ary =  json_object_new_array();
        return_if_null(jso_ary, "Out of memory.", TSS2_FAPI_RC_MEMORY);
    }
    callback_data.jso_event_list = jso_ary;

    ctx.data = &callback_data;

    bool rc = parse_eventlog(&ctx, eventlog, size);
    if (!rc) {
        goto_error(r, TSS2_FAPI_RC_BAD_VALUE, "Eventlog could not be parsed.", error);
    }

    *eventlog_json = jso_ary;
    return TSS2_RC_SUCCESS;

 error:
    if (jso_ary)
        json_object_put(jso_ary);
    return r;
}

static TSS2_RC
file_to_buffer(const char *filename, size_t *size, uint8_t **eventlog)
{
    return_if_null(eventlog, "Invalid buffer.", TSS2_FAPI_RC_BAD_VALUE);
    size_t alloc_size = UINT16_MAX;
    size_t alloc_buf_size;
    size_t n_alloc = 1;
    size_t file_size = 0;
    size_t read_size = 0;

    *eventlog = NULL;
    FILE *fp = fopen(filename, "rb");
    if (!fp) {
        return_error2(TSS2_FAPI_RC_IO_ERROR, "Could not read %s", filename);
    }
    *size = 0;
    *eventlog = calloc(1, alloc_size);
    if (!*eventlog) {
        return_error2(TSS2_FAPI_RC_IO_ERROR, "Could not read %s", filename);
    }
    read_size = fread(*eventlog, 1, alloc_size, fp);
    file_size += read_size;
    alloc_buf_size = alloc_size;

    while (file_size == alloc_buf_size) {
        n_alloc += 1;
        uint8_t* tmp_buff = calloc(1, alloc_size * n_alloc);
        if (!tmp_buff) {
            free(*eventlog);
            return_error2(TSS2_FAPI_RC_IO_ERROR, "Could not read %s", filename);
        }
        alloc_buf_size = alloc_size * n_alloc;
        memcpy(&tmp_buff[0], eventlog[0], file_size);
        free(*eventlog);
        *eventlog = tmp_buff;
        read_size = fread(eventlog[file_size], 1, alloc_size, fp);
        file_size += read_size;
    }
    *size = file_size;
    return TSS2_RC_SUCCESS;
}

TSS2_RC ifapi_get_tcg_firmware_event_list(
    char const *filename,
    const uint32_t *pcr_list,
    size_t  pcr_list_size,
    json_object **json_eventlog)
{
    TSS2_RC r;
    uint8_t *eventlog_buffer = NULL;
    size_t size;

    r = file_to_buffer(filename, &size, &eventlog_buffer);
    return_if_error(r, "Read eventlog.");

    r = ifapi_tcg_eventlog_serialize(eventlog_buffer, size, pcr_list,
                                     pcr_list_size, json_eventlog);
    goto_if_error(r, "Serialize eventlog.", error);

    SAFE_FREE(eventlog_buffer);
    return TSS2_RC_SUCCESS;

 error:
    SAFE_FREE(eventlog_buffer);
    return r;
}
