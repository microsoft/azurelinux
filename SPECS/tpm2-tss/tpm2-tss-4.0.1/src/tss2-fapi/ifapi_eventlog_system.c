/* SPDX-License-Identifier: BSD-2-Clause */
/*******************************************************************************
 * Copyright 2018-2019, Fraunhofer SIT sponsored by Infineon Technologies AG
 * All rights reserved.
 *******************************************************************************/

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <string.h>

#include "ifapi_helpers.h"
#include "ifapi_eventlog_system.h"
#include "ifapi_json_serialize.h"
#include "tpm_json_deserialize.h"
#include "efi_event.h"

#define LOGMODULE fapi
#include "util/log.h"
#include "util/aux_util.h"
#include "ifapi_macros.h"
#include "fapi_crypto.h"

static char *tss_const_prefixes[] = { "TPM2_ALG_", "TPM2_", "TPM_", "TPMA_", "POLICY", NULL };

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
    uint itoken = 0;
    char *entry;
    uint i;

    for (i = 0, entry = tss_const_prefixes[0]; entry != NULL;
            i++, entry = tss_const_prefixes[i]) {
        if (strncasecmp(token, entry, strlen(entry)) == 0) {
            itoken += strlen(entry);
            break;
        }
    }
    return itoken;
}

bool digest2_accumulator_callback(TCG_DIGEST2 const *digest, size_t size,
                                  void *data){
    if (digest == NULL || data == NULL) {
        LOG_ERROR("neither parameter may be NULL");
        return false;
    }
    size_t *accumulator = (size_t*)data;

    *accumulator += sizeof(*digest) + size;

    return true;
}
/*
 * Invoke callback function for each TCG_DIGEST2 structure in the provided
 * TCG_EVENT_HEADER2. The callback function is only invoked if this function
 * is first able to determine that the provided buffer is large enough to
 * hold the digest. The size of the digest is passed to the callback in the
 * 'size' parameter.
 */
bool foreach_digest2(
    tpm2_eventlog_context *ctx,
    UINT32 event_type,
    unsigned pcr_index,
    TCG_DIGEST2 const *digest,
    size_t count,
    size_t size) {

    if (digest == NULL) {
        LOG_ERROR("digest cannot be NULL");
        return false;
    }

    bool ret = true;
    TSS2_RC r;

    size_t i, j;
    for (i = 0; i < count; i++) {
        if (size < sizeof(*digest)) {
            LOG_ERROR("insufficient size for digest header");
            return false;
        }

        const TPMI_ALG_HASH alg = digest->AlgorithmId;
        const size_t alg_size = ifapi_hash_get_digest_size(alg);
        if (size < sizeof(*digest) + alg_size) {
            LOG_ERROR("insufficient size for digest buffer");
            return false;
        }

        uint8_t *pcr = NULL;
        if (pcr_index > TPM2_MAX_PCRS) {
            LOG_ERROR("PCR%d > max %d", pcr_index, TPM2_MAX_PCRS);
            return false;
        } else if (alg == TPM2_ALG_SHA1) {
            pcr = ctx->sha1_pcrs[pcr_index];
            ctx->sha1_used |= (1 << pcr_index);
        } else if (alg == TPM2_ALG_SHA256) {
            pcr = ctx->sha256_pcrs[pcr_index];
            ctx->sha256_used |= (1 << pcr_index);
        } else if (alg == TPM2_ALG_SHA384) {
            pcr = ctx->sha384_pcrs[pcr_index];
            ctx->sha384_used |= (1 << pcr_index);
        } else if (alg == TPM2_ALG_SHA512) {
            pcr = ctx->sha512_pcrs[pcr_index];
            ctx->sha512_used |= (1 << pcr_index);
        } else if (alg == TPM2_ALG_SM3_256) {
            pcr = ctx->sm3_256_pcrs[pcr_index];
            ctx->sm3_256_used |= (1 << pcr_index);
        } else {
            LOG_WARNING("PCR%d algorithm %d unsupported", pcr_index, alg);
        }
        if (pcr) {
            r = ifapi_extend_pcr(alg, pcr, digest->Digest, alg_size);
            if (r) {
                LOG_ERROR("PCR%d extend failed", pcr_index);
                return false;
            }
        }

        if (event_type == EV_NO_ACTION) {
            /* Digest for EV_NO_ACTION must consist of 0 bytes. */
            for (j = 0; j < alg_size; j++) {
                if (digest->Digest[j]) {
                    LOG_ERROR("No zero digest for EV_NO_ACTION.");
                    return false;
                }
            }
        }

        if (ctx->digest2_cb != NULL) {
            ret = ctx->digest2_cb(digest, alg_size, ctx->data);
            if (!ret) {
                LOG_ERROR("callback failed for digest at %p with size %zu", digest, alg_size);
                break;
            }
        }

        size -= sizeof(*digest) + alg_size;
        digest = (TCG_DIGEST2*)((uintptr_t)digest->Digest + alg_size);
    }

    return ret;
}
/*
 * given the provided event type, parse event to ensure the structure / data
 * in the buffer doesn't exceed the buffer size
 */
bool parse_event2body(TCG_EVENT2 const *event, UINT32 type) {

    switch (type) {
    /* TCG PC Client FPF section 9.2.6 */
    case EV_EFI_VARIABLE_DRIVER_CONFIG:
    case EV_EFI_VARIABLE_BOOT:
    case EV_EFI_VARIABLE_AUTHORITY:
        {
            UEFI_VARIABLE_DATA *data = (UEFI_VARIABLE_DATA*)event->Event;
            if (event->EventSize < sizeof(*data)) {
                LOG_ERROR("size is insufficient for UEFI variable data");
                return false;
            }

            if (event->EventSize < sizeof(*data) + data->UnicodeNameLength *
                sizeof(char16_t) + data->VariableDataLength)
            {
                LOG_ERROR("size is insufficient for UEFI variable data");
                return false;
            }
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
                (UEFI_PLATFORM_FIRMWARE_BLOB*)event->Event;
            UNUSED(data);
            if (event->EventSize < sizeof(*data)) {
                LOG_ERROR("size is insufficient for UEFI FW blob data");
                return false;
            }
        }
        break;
    case EV_EFI_BOOT_SERVICES_APPLICATION:
    case EV_EFI_BOOT_SERVICES_DRIVER:
    case EV_EFI_RUNTIME_SERVICES_DRIVER:
        {
            UEFI_IMAGE_LOAD_EVENT *data = (UEFI_IMAGE_LOAD_EVENT*)event->Event;
            UNUSED(data);
            if (event->EventSize < sizeof(*data)) {
                LOG_ERROR("size is insufficient for UEFI image load event");
                return false;
            }
            /* what about the device path? */
        }
        break;
    }

    return true;
}
/*
 * parse event structure, including header, digests and event buffer ensuring
 * it all fits within the provided buffer (buf_size).
 */
bool parse_event2(TCG_EVENT_HEADER2 const *eventhdr, size_t buf_size,
                  size_t *event_size, size_t *digests_size) {

    bool ret;

    if (buf_size < sizeof(*eventhdr)) {
        LOG_ERROR("corrupted log, insufficient size for event header: %zu", buf_size);
        return false;
    }
    *event_size = sizeof(*eventhdr);

    tpm2_eventlog_context ctx = {
        .data = digests_size,
        .digest2_cb = digest2_accumulator_callback,
    };
    ret = foreach_digest2(&ctx, eventhdr->EventType, eventhdr->PCRIndex,
                          eventhdr->Digests, eventhdr->DigestCount,
                          buf_size - sizeof(*eventhdr));
    if (ret != true) {
        return false;
    }
    *event_size += *digests_size;

    TCG_EVENT2 *event = (TCG_EVENT2*)((uintptr_t)eventhdr + *event_size);
    if (buf_size < *event_size + sizeof(*event)) {
        LOG_ERROR("corrupted log: size insufficient for EventSize");
        return false;
    }
    *event_size += sizeof(*event);

    if (buf_size < *event_size + event->EventSize) {
        LOG_ERROR("size insufficient for event data");
        return false;
    }
    *event_size += event->EventSize;

    return true;
}

bool parse_sha1_log_event(tpm2_eventlog_context *ctx, TCG_EVENT const *event, size_t size,
                          size_t *event_size) {

    uint8_t *pcr = NULL;
    TSS2_RC r;

    /* enough size for the 1.2 event structure */
    if (size < sizeof(*event)) {
        LOG_ERROR("insufficient size for SpecID event header");
        return false;
    }
    if (event->pcrIndex > TPM2_MAX_PCRS) {
        LOG_ERROR("Invalid PCR index");
        return false;
    }
    *event_size = sizeof(*event);

    pcr = ctx->sha1_pcrs[ event->pcrIndex];
    if (pcr) {
        r = ifapi_extend_pcr(TPM2_ALG_SHA1, pcr, &event->digest[0], 20);
        if (r) {
            LOG_ERROR("PCR%d extend failed", event->pcrIndex);
            return false;
        }
        ctx->sha1_used |= (1 << event->pcrIndex);
    }

    /* buffer size must be sufficient to hold event and event data */
    if (size < sizeof(*event) + (sizeof(event->event[0]) *
                                 event->eventDataSize)) {
        LOG_ERROR("insufficient size for SpecID event data");
        return false;
    }
    *event_size += event->eventDataSize;
    return true;
}

bool foreach_sha1_log_event(tpm2_eventlog_context *ctx, TCG_EVENT const *eventhdr_start, size_t size) {

    if (eventhdr_start == NULL) {
        LOG_ERROR("invalid parameter");
        return false;
    }
    if (size == 0) {
        return true;
    }

    TCG_EVENT const *eventhdr;
    size_t event_size;
    bool ret;

    for (eventhdr = eventhdr_start, event_size = 0;
         size > 0;
         eventhdr = (TCG_EVENT*)((uintptr_t)eventhdr + event_size),
         size -= event_size) {

        ret = parse_sha1_log_event(ctx, eventhdr, size, &event_size);
        if (!ret) {
            return ret;
        }

        TCG_EVENT2 *event = (TCG_EVENT2*)((uintptr_t)&eventhdr->eventDataSize);

        /* event header callback */
        if (ctx->log_eventhdr_cb != NULL) {
            ret = ctx->log_eventhdr_cb(eventhdr, event_size, ctx->data);
            if (ret != true) {
                return false;
            }
        }

        ret = parse_event2body(event, eventhdr->eventType);
        if (ret != true) {
            return ret;
        }

        /* event data callback */
        if (ctx->event2_cb != NULL) {
            ret = ctx->event2_cb(event, eventhdr->eventType, ctx->data);
            if (ret != true) {
                return false;
            }
        }
    }

    return true;
}

bool foreach_event2(tpm2_eventlog_context *ctx, TCG_EVENT_HEADER2 const *eventhdr_start, size_t size) {

    if (eventhdr_start == NULL) {
        LOG_ERROR("invalid parameter");
        return false;
    }
    if (size == 0) {
        return true;
    }

    TCG_EVENT_HEADER2 const *eventhdr;
    size_t event_size;
    bool ret;

    for (eventhdr = eventhdr_start, event_size = 0;
         size > 0;
         eventhdr = (TCG_EVENT_HEADER2*)((uintptr_t)eventhdr + event_size),
         size -= event_size) {

        size_t digests_size = 0;

        ret = parse_event2(eventhdr, size, &event_size, &digests_size);
        if (!ret) {
            return ret;
        }

        TCG_EVENT2 *event = (TCG_EVENT2*)((uintptr_t)eventhdr->Digests + digests_size);

        /* event header callback */
        if (ctx->event2hdr_cb != NULL) {
            ret = ctx->event2hdr_cb(eventhdr, event_size, ctx->data);
            if (ret != true) {
                return false;
            }
        }

        /* digest callback foreach digest */
        ret = foreach_digest2(ctx, eventhdr->EventType, eventhdr->PCRIndex,
                              eventhdr->Digests, eventhdr->DigestCount, digests_size);
        if (ret != true) {
            return false;
        }

        ret = parse_event2body(event, eventhdr->EventType);
        if (ret != true) {
            return ret;
        }

        /* event data callback */
        if (ctx->event2_cb != NULL) {
            ret = ctx->event2_cb(event, eventhdr->EventType, ctx->data);
            if (ret != true) {
                return false;
            }
        }
    }

    return true;
}

bool specid_event(TCG_EVENT const *event, size_t size,
                  TCG_EVENT_HEADER2 **next) {

    /* enough size for the 1.2 event structure */
    if (size < sizeof(*event)) {
        LOG_ERROR("insufficient size for SpecID event header");
        return false;
    }

    if (event->eventType != EV_NO_ACTION) {
        LOG_ERROR("SpecID eventType must be EV_NO_ACTION");
        return false;
    }

    if (event->pcrIndex != 0) {
        LOG_ERROR("bad pcrIndex for EV_NO_ACTION event");
        return false;
    }

    size_t i;
    for (i = 0; i < sizeof(event->digest); ++i) {
        if (event->digest[i] != 0) {
            LOG_ERROR("SpecID digest data malformed");
            return false;
        }
    }

    /* eventDataSize must be sufficient to hold the specid event */
    if (event->eventDataSize < sizeof(TCG_SPECID_EVENT)) {
        LOG_ERROR("invalid eventDataSize in specid event");
        return false;
    }

    /* buffer size must be sufficient to hold event and event data */
    if (size < sizeof(*event) + (sizeof(event->event[0]) *
                                 event->eventDataSize)) {
        LOG_ERROR("insufficient size for SpecID event data");
        return false;
    }

    TCG_SPECID_EVENT *event_specid = (TCG_SPECID_EVENT*)event->event;

    /* Check the signature */
    if (strcmp((char *)&event_specid->Signature[0], "Spec ID Event03")) {
        LOG_ERROR("Check of signature \"Spec ID Event03\" failed.");
        return false;
    }

    /* specid event must have 1 or more algorithms */
    if (event_specid->numberOfAlgorithms == 0) {
        LOG_ERROR("numberOfAlgorithms is invalid, may not be 0");
        return false;
    }

    /* buffer size must be sufficient to hold event, specid event & algs */
    if (size < sizeof(*event) + sizeof(*event_specid) +
               sizeof(event_specid->digestSizes[0]) *
               event_specid->numberOfAlgorithms) {
        LOG_ERROR("insufficient size for SpecID algorithms");
        return false;
    }

    /* size must be sufficient for event, specid, algs & vendor stuff */
    if (size < sizeof(*event) + sizeof(*event_specid) +
               sizeof(event_specid->digestSizes[0]) *
               event_specid->numberOfAlgorithms + sizeof(TCG_VENDOR_INFO)) {
        LOG_ERROR("insufficient size for VendorStuff");
        return false;
    }

    TCG_VENDOR_INFO *vendor = (TCG_VENDOR_INFO*)((uintptr_t)event_specid->digestSizes +
                                                 sizeof(*event_specid->digestSizes) *
                                                 event_specid->numberOfAlgorithms);
    /* size must be sufficient for vendorInfo */
    if (size < sizeof(*event) + sizeof(*event_specid) +
               sizeof(event_specid->digestSizes[0]) *
               event_specid->numberOfAlgorithms + sizeof(*vendor) +
               vendor->vendorInfoSize) {
        LOG_ERROR("insufficient size for VendorStuff data");
        return false;
    }
    *next = (TCG_EVENT_HEADER2*)((uintptr_t)vendor->vendorInfo + vendor->vendorInfoSize);

    return true;
}

static TCG_EVENT_TYPE_ASSIGN deserialize_TCG_EVENT_TYPE_tab[] = {
    { EV_PREBOOT_CERT, "EV_PREBOOT_CERT" },
    { EV_POST_CODE, "EV_POST_CODE" },
    { EV_UNUSED, "EV_UNUSED" },
    { EV_NO_ACTION, "EV_NO_ACTION" },
    { EV_SEPARATOR, "EV_SEPARATOR" },
    { EV_ACTION, "EV_ACTION" },
    { EV_EVENT_TAG, "EV_EVENT_TAG" },
    { EV_S_CRTM_CONTENTS, "EV_S_CRTM_CONTENTS" },
    { EV_S_CRTM_VERSION, "EV_S_CRTM_VERSION" },
    { EV_CPU_MICROCODE, "EV_CPU_MICROCODE" },
    { EV_PLATFORM_CONFIG_FLAGS, "EV_PLATFORM_CONFIG_FLAGS" },
    { EV_TABLE_OF_DEVICES, "EV_TABLE_OF_DEVICES" },
    { EV_COMPACT_HASH, "EV_COMPACT_HASH" },
    { EV_IPL, "EV_IPL" },
    { EV_IPL_PARTITION_DATA, "EV_IPL_PARTITION_DATA" },
    { EV_NONHOST_CODE, "EV_NONHOST_CODE" },
    { EV_NONHOST_CONFIG, "EV_NONHOST_CONFIG" },
    { EV_NONHOST_INFO, "EV_NONHOST_INFO" },
    { EV_OMIT_BOOT_DEVICE_EVENTS, "EV_OMIT_BOOT_DEVICE_EVENTS" },
    { EV_EFI_VARIABLE_DRIVER_CONFIG, "EV_EFI_VARIABLE_DRIVER_CONFIG" },
    { EV_EFI_VARIABLE_BOOT, "EV_EFI_VARIABLE_BOOT" },
    { EV_EFI_BOOT_SERVICES_APPLICATION, "EV_EFI_BOOT_SERVICES_APPLICATION" },
    { EV_EFI_BOOT_SERVICES_DRIVER, "EV_EFI_BOOT_SERVICES_DRIVER" },
    { EV_EFI_RUNTIME_SERVICES_DRIVER, "EV_EFI_RUNTIME_SERVICES_DRIVER" },
    { EV_EFI_GPT_EVENT, "EV_EFI_GPT_EVENT" },
    { EV_EFI_ACTION, "EV_EFI_ACTION" },
    { EV_EFI_PLATFORM_FIRMWARE_BLOB, "EV_EFI_PLATFORM_FIRMWARE_BLOB" },
    { EV_EFI_HANDOFF_TABLES, "EV_EFI_HANDOFF_TABLES" },
    { EV_EFI_HCRTM_EVENT, "EV_EFI_HCRTM_EVENT" },
    { EV_EFI_VARIABLE_AUTHORITY, "EV_EFI_VARIABLE_AUTHORITY" },
};

/**  Deserialize a json object of type TCG_EVENT_TYPE.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 */
TSS2_RC
ifapi_json_TCG_EVENT_TYPE_deserialize_txt(json_object *jso,
        IFAPI_EVENT_TYPE *out)
{
    LOG_TRACE("call");
    int64_t i64;
    const char *token = json_object_get_string(jso);

    check_oom(token);

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
        size_t n = sizeof(deserialize_TCG_EVENT_TYPE_tab) /
                   sizeof(deserialize_TCG_EVENT_TYPE_tab[0]);
        size_t size = strlen(token) - itoken;
        for (i = 0; i < n; i++) {
            if (strncasecmp(&token[itoken],
                            &deserialize_TCG_EVENT_TYPE_tab[i].name[0],
                            size) == 0) {
                *out = deserialize_TCG_EVENT_TYPE_tab[i].in;
                return TSS2_RC_SUCCESS;
            }
        }
        return_error(TSS2_FAPI_RC_BAD_VALUE, "Undefined constant.");
    }

}

/** Deserialize a TCG_EVENT_TYPE json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 */
TSS2_RC
ifapi_json_TCG_EVENT_TYPE_deserialize(json_object *jso, IFAPI_EVENT_TYPE *out)
{
    LOG_TRACE("call");
    return ifapi_json_TCG_EVENT_TYPE_deserialize_txt(jso, out);
}

/** Check event field is string with or without NULL terminator.
 */
static TSS2_RC
check_out_string(const IFAPI_FIRMWARE_EVENT *in, const char *string) {
    if (strncmp((const char *)&in->data.buffer[0], string, strlen(string)) != 0) {
        return_error2(TSS2_FAPI_RC_BAD_VALUE, "Invalid event string. %s expected", string);
    }
    if (in->data.size == strlen(string)) {
        /* String without NULL terminator */
        return TSS2_RC_SUCCESS;
    }
    if  (in->data.size == strlen(string) + 1 &&
         in->data.buffer[strlen(string)] == '\0') {
        /* String with NULL terminator */
        return TSS2_RC_SUCCESS;
    }
    return_error2(TSS2_FAPI_RC_BAD_VALUE, "Invalid event string. %s expected", string);
}


/** Deserialize a IFAPI_FIRMWARE_EVENT json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @param[out] verify swithc whether the digest can be verified.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 */
TSS2_RC
ifapi_json_IFAPI_FIRMWARE_EVENT_deserialize(
    json_object *jso,
    IFAPI_FIRMWARE_EVENT *out,
    bool *verify)
{
    json_object *jso2;
    TSS2_RC r;
    UINT32  event_type;
    LOG_TRACE("call");

    return_if_null(out, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    out->data.buffer = NULL;

    if (!ifapi_get_sub_object(jso, "event_type", &jso2)) {
        LOG_ERROR("Bad value");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r =  ifapi_json_TCG_EVENT_TYPE_deserialize (jso2, &event_type);
    return_if_error(r,"BAD VALUE");

    if (!ifapi_get_sub_object(jso, "event_data", &jso2)) {
        LOG_ERROR("Bad value");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_UINT8_ARY_deserialize(jso2, &out->data);
    return_if_error(r, "BAD VALUE");

    if (event_type == EV_SEPARATOR) {
        /* The allowed event data for valid separator.
           Other events signal an error. The event data is not
           used to compute the digest. The hash of 0x00000001 will
           be used. */
        BYTE event_0[4] = { 0, 0, 0, 0 };
        BYTE event_ff[4] = { 0xff, 0xff, 0xff, 0xff };

        if (!(out->data.size == 4 &&
              (memcmp(&event_0[0], &out->data.buffer[0], 4) == 0 ||
               memcmp(&event_ff[0], &out->data.buffer[0], 4) == 0))) {
            /* An error is signaled the hash of event_err will be
               used as digest. */
            SAFE_FREE(out->data.buffer);
            out->data.buffer = calloc(1, 4);
            out->data.size = 4;
            /* hash of 0x00000001 will be used as digest. */
            out->data.buffer[3] = 1;
        }
    }

    if (event_type == EV_EFI_HCRTM_EVENT) {
        r = check_out_string(out, "HCRTM");
        goto_if_error(r, "Check HCRTM event.", error);
    } else if (event_type == EV_OMIT_BOOT_DEVICE_EVENTS) {
        r = check_out_string(out, "BOOT ATTEMPTS OMITTED");
        goto_if_error(r, "Check OMIT_BOOT_DEVICES event.", error);
    }

    /* Check whether digest computation for event is possible. */
    if (/* Verification is not possible */
        event_type == EV_EFI_BOOT_SERVICES_APPLICATION ||
        event_type == EV_NO_ACTION ||
        event_type == EV_S_CRTM_CONTENTS ||
        event_type == EV_POST_CODE ||
        event_type == EV_EFI_HANDOFF_TABLES ||
        event_type == EV_COMPACT_HASH ||
        event_type == EV_EFI_BOOT_SERVICES_DRIVER ||
        event_type == EV_EFI_PLATFORM_FIRMWARE_BLOB ||
        event_type == EV_PREBOOT_CERT ||
        event_type == EV_UNUSED ||
        event_type == EV_ACTION ||
        event_type == EV_CPU_MICROCODE ||
        event_type == EV_IPL ||
        event_type == EV_IPL_PARTITION_DATA ||
        event_type == EV_NONHOST_CODE ||
        event_type == EV_NONHOST_CONFIG ||
        event_type == EV_EFI_RUNTIME_SERVICES_DRIVER) {
        *verify = false;
    } else if (
        /* Verification is possible. (TODO check) */
        event_type == EV_EVENT_TAG ||
        event_type == EV_TABLE_OF_DEVICES ||
        event_type == EV_NONHOST_INFO ||
        event_type == EV_OMIT_BOOT_DEVICE_EVENTS ||
        event_type == EV_EFI_VARIABLE_AUTHORITY ||
        /* Verification is possible. */
        event_type == EV_S_CRTM_VERSION ||
        event_type == EV_EFI_HCRTM_EVENT ||
        event_type == EV_SEPARATOR ||
        event_type == EV_EFI_VARIABLE_DRIVER_CONFIG ||
        event_type == EV_EFI_GPT_EVENT ||
        event_type == EV_PLATFORM_CONFIG_FLAGS ||
        event_type == EV_EFI_VARIABLE_BOOT ||
        event_type == EV_EFI_ACTION) {
        *verify = true;
    } else {
        LOG_WARNING("Unknown Event: %x", event_type);
        *verify = false;
    }

    LOG_TRACE("true");
    return TSS2_RC_SUCCESS;

 error:
    SAFE_FREE(out->data.buffer);
    return r;
}

bool parse_eventlog(tpm2_eventlog_context *ctx, BYTE const *eventlog, size_t size) {

    TCG_EVENT_HEADER2 *next;
    TCG_EVENT *event = (TCG_EVENT*)eventlog;
    bool ret;

    if (event->eventType == EV_NO_ACTION) {
        ret = specid_event(event, size, &next);
        if (!ret) {
            return false;
        }

        size -= (uintptr_t)next - (uintptr_t)eventlog;

        if (ctx->specid_cb) {
            ret = ctx->specid_cb(event, ctx->data);
            if (!ret) {
                return false;
            }
        }
        return foreach_event2(ctx, next, size);
    } else {
        /* No spec id header found. */
        return foreach_sha1_log_event(ctx, event, size);
    }
}
