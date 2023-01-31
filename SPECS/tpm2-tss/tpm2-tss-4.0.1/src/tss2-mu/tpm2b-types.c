/* SPDX-License-Identifier: BSD-2-Clause */
/***********************************************************************
 * Copyright (c) 2015 - 2017, Intel Corporation
 *
 * All rights reserved.
 ***********************************************************************/

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <inttypes.h>
#include <string.h>

#include "tss2_mu.h"

#include "util/tpm2b.h"
#include "util/tss2_endian.h"
#define LOGMODULE marshal
#include "util/log.h"

#define TPM2B_MARSHAL(type) \
TSS2_RC Tss2_MU_##type##_Marshal(type const *src, uint8_t buffer[], \
                                 size_t buffer_size, size_t *offset) \
{ \
    size_t local_offset = 0; \
    TSS2_RC rc; \
\
    if (src == NULL) { \
        LOG_WARNING("src param is NULL"); \
        return TSS2_MU_RC_BAD_REFERENCE; \
    } \
    if (offset != NULL) { \
        LOG_DEBUG("offset non-NULL, initial value: %zu", *offset); \
        local_offset = *offset; \
    } \
    if (buffer == NULL && offset == NULL) { \
        LOG_WARNING("buffer and offset parameter are NULL"); \
        return TSS2_MU_RC_BAD_REFERENCE; \
    } else if (buffer == NULL && offset != NULL) { \
        *offset += sizeof(src->size) + src->size; \
        LOG_TRACE("buffer NULL and offset non-NULL, updating offset to %zu", \
             *offset); \
        return TSS2_RC_SUCCESS; \
    } else if (buffer_size < local_offset || \
               buffer_size - local_offset < (sizeof(src->size) + src->size)) { \
        LOG_DEBUG( \
             "buffer_size: %zu with offset: %zu are insufficient for object " \
             "of size %zu", \
             buffer_size, \
             local_offset, \
             sizeof(src->size) + src->size); \
        return TSS2_MU_RC_INSUFFICIENT_BUFFER; \
    } else if ((sizeof(type) - sizeof(src->size)) < src->size) { \
        LOG_WARNING(\
             "size: %u for buffer of " #type " is larger than max length" \
             " of buffer: %zu", \
             src->size, \
             (sizeof(type) - sizeof(src->size))); \
        return TSS2_MU_RC_BAD_SIZE; \
    } \
\
    LOG_DEBUG(\
         "Marshalling " #type " from 0x%" PRIxPTR " to buffer 0x%" PRIxPTR \
         " at index 0x%zx, buffer size %zu, object size %u", \
         (uintptr_t)&src, \
         (uintptr_t)buffer, \
         local_offset, \
         buffer_size, \
         src->size); \
\
    rc = Tss2_MU_UINT16_Marshal(src->size, buffer, buffer_size, &local_offset); \
    if (rc) \
        return rc; \
\
    if (src->size) { \
        memcpy(&buffer[local_offset], ((TPM2B *)src)->buffer, src->size); \
        local_offset += src->size; \
    } \
\
    if (offset != NULL) { \
        *offset = local_offset; \
        LOG_DEBUG("offset parameter non-NULL, updated to %zu", *offset); \
    } \
\
    return TSS2_RC_SUCCESS; \
}

#define TPM2B_UNMARSHAL(type, buf_name) \
TSS2_RC Tss2_MU_##type##_Unmarshal(uint8_t const buffer[], size_t buffer_size, \
                                   size_t *offset, type *dest) \
{ \
    size_t  local_offset = 0; \
    UINT16 size = 0; \
    TSS2_RC rc; \
\
    if (offset != NULL) { \
        LOG_DEBUG("offset non-NULL, initial value: %zu", *offset); \
        local_offset = *offset; \
    } \
\
    if (buffer == NULL || (dest == NULL && offset == NULL)) { \
        LOG_WARNING("buffer or dest and offset parameter are NULL"); \
        return TSS2_MU_RC_BAD_REFERENCE; \
    } else if (buffer_size < local_offset || \
               sizeof(size) > buffer_size - local_offset) \
    { \
        LOG_DEBUG( \
             "buffer_size: %zu with offset: %zu are insufficient for object " \
             "of size %zu", \
             buffer_size, \
             local_offset, \
             sizeof(size)); \
        return TSS2_MU_RC_INSUFFICIENT_BUFFER; \
    } \
\
    rc = Tss2_MU_UINT16_Unmarshal(buffer, buffer_size, &local_offset, &size); \
    if (rc) \
        return rc; \
\
    LOG_DEBUG(\
         "Unmarshaling " #type " from 0x%" PRIxPTR " to buffer 0x%" PRIxPTR \
         " at index 0x%zx, buffer size %zu, object size %u", \
         (uintptr_t)buffer, \
         (uintptr_t)dest, \
         local_offset, \
         buffer_size, \
         size); \
\
    if (size > buffer_size - local_offset) { \
        LOG_DEBUG( \
             "buffer_size: %zu with offset: %zu are insufficient for object " \
             "of size %zu", \
             buffer_size, \
             local_offset, \
             (size_t)size); \
        return TSS2_MU_RC_INSUFFICIENT_BUFFER; \
    } \
    if (sizeof(dest->buf_name) < size) { \
        LOG_DEBUG("The dest field size of %zu is too small to unmarshal %d bytes", \
                  sizeof(dest->buf_name), size); \
        return TSS2_MU_RC_INSUFFICIENT_BUFFER; \
    } \
\
    if (dest != NULL) { \
        dest->size = size; \
        memcpy(((TPM2B *)dest)->buffer, &buffer[local_offset], size); \
    } \
    local_offset += size; \
    if (offset != NULL) { \
        *offset = local_offset; \
        LOG_DEBUG("offset parameter non-NULL, updated to %zu", *offset); \
    } \
\
    return TSS2_RC_SUCCESS; \
}

#define TPM2B_MARSHAL_SUBTYPE(type, subtype, member) \
TSS2_RC Tss2_MU_##type##_Marshal(type const *src, uint8_t buffer[], \
                                 size_t buffer_size, size_t *offset) \
{ \
    size_t local_offset = 0; \
    UINT8 *ptr = NULL; \
    TSS2_RC rc; \
\
    if (src == NULL) { \
        LOG_WARNING("src param is NULL"); \
        return TSS2_MU_RC_BAD_REFERENCE; \
    } \
\
    if (offset != NULL) { \
        LOG_DEBUG("offset non-NULL, initial value: %zu", *offset); \
        local_offset = *offset; \
    } \
\
    if (buffer == NULL && offset == NULL) { \
        LOG_WARNING("buffer and offset parameter are NULL"); \
        return TSS2_MU_RC_BAD_REFERENCE; \
    } else if (buffer_size < local_offset || \
               buffer_size - local_offset < sizeof(src->size)) { \
        LOG_DEBUG( \
             "buffer_size: %zu with offset: %zu are insufficient for object " \
             "of size %zu", \
             buffer_size, \
             local_offset, \
             sizeof(src->size)); \
        return TSS2_MU_RC_INSUFFICIENT_BUFFER; \
    } \
\
    if (buffer) \
        ptr = &buffer[local_offset];            \
\
    LOG_DEBUG(\
         "Marshalling " #type " from 0x%" PRIxPTR " to buffer 0x%" PRIxPTR \
         " at index 0x%zx, buffer size %zu, object size %u", \
         (uintptr_t)&src, \
         (uintptr_t)buffer, \
         local_offset, \
         buffer_size, \
         src->size); \
\
    rc = Tss2_MU_UINT16_Marshal(src->size, buffer, buffer_size, &local_offset); \
    if (rc) \
        return rc; \
\
    rc = Tss2_MU_##subtype##_Marshal(&src->member, buffer, buffer_size, &local_offset); \
    if (rc) \
        return rc; \
\
    /* Update the size to the real value */ \
    if (buffer) { \
        UINT16 t = HOST_TO_BE_16((UINT16)(buffer + local_offset - ptr - 2)); \
        memcpy(ptr, &t, sizeof(t)); \
    } \
\
    if (offset != NULL) { \
        *offset = local_offset; \
        LOG_DEBUG("offset parameter non-NULL, updated to %zu", *offset); \
    } \
\
    return TSS2_RC_SUCCESS; \
}

#define TPM2B_UNMARSHAL_SUBTYPE(type, subtype, member) \
TSS2_RC Tss2_MU_##type##_Unmarshal(uint8_t const buffer[], size_t buffer_size, \
                                   size_t *offset, type *dest) \
{ \
    size_t  local_offset = 0; \
    UINT16 size = 0; \
    TSS2_RC rc; \
\
    if (offset != NULL) { \
        LOG_DEBUG("offset non-NULL, initial value: %zu", *offset); \
        local_offset = *offset; \
    } \
\
    if (buffer == NULL || (dest == NULL && offset == NULL)) { \
        LOG_WARNING("buffer or dest and offset parameter are NULL"); \
        return TSS2_MU_RC_BAD_REFERENCE; \
    } else if (buffer_size < local_offset || \
               sizeof(size) > buffer_size - local_offset) \
    { \
        LOG_DEBUG( \
             "buffer_size: %zu with offset: %zu are insufficient for object " \
             "of size %zu", \
             buffer_size, \
             local_offset, \
             sizeof(size)); \
        return TSS2_MU_RC_INSUFFICIENT_BUFFER; \
    } \
    if (dest && dest->size != 0) { \
        LOG_WARNING("Size not zero"); \
        return TSS2_SYS_RC_BAD_VALUE; \
    } \
\
    rc = Tss2_MU_UINT16_Unmarshal(buffer, buffer_size, &local_offset, &size); \
    if (rc) \
        return rc; \
    LOG_DEBUG(\
         "Unmarshaling " #type " from 0x%" PRIxPTR " to buffer 0x%" PRIxPTR \
         " at index 0x%zx, buffer size %zu, object size %u", \
         (uintptr_t)buffer, \
         (uintptr_t)dest, \
         local_offset, \
         buffer_size, \
         size); \
\
    if (size > buffer_size - local_offset) { \
        LOG_DEBUG( \
             "buffer_size: %zu with offset: %zu are insufficient for object " \
             "of size %zu", \
             buffer_size, \
             local_offset, \
             (size_t)size); \
        return TSS2_MU_RC_INSUFFICIENT_BUFFER; \
    } \
    if (sizeof(dest->member) < size) { \
        LOG_DEBUG("The dest field size of %zu is too small to unmarshal %d bytes", \
                  sizeof(dest->member), size); \
        return TSS2_MU_RC_INSUFFICIENT_BUFFER; \
    } \
\
    if (dest != NULL) { \
        dest->size = size; \
        Tss2_MU_##subtype##_Unmarshal(buffer, buffer_size, &local_offset, &dest->member); \
        if (rc) \
            return rc; \
    } else { \
        local_offset += size; \
    } \
\
    if (offset != NULL) { \
        *offset = local_offset; \
        LOG_DEBUG("offset parameter non-NULL, updated to %zu", *offset); \
    } \
\
    return TSS2_RC_SUCCESS; \
}

/*
 * These macros expand to (un)marshal functions for each of the TPM2B types
 * the specification part 2.
 */
TPM2B_MARSHAL  (TPM2B_DIGEST);
TPM2B_UNMARSHAL(TPM2B_DIGEST, buffer);
TPM2B_MARSHAL  (TPM2B_DATA);
TPM2B_UNMARSHAL(TPM2B_DATA, buffer);
TPM2B_MARSHAL  (TPM2B_EVENT);
TPM2B_UNMARSHAL(TPM2B_EVENT, buffer);
TPM2B_MARSHAL  (TPM2B_MAX_BUFFER);
TPM2B_UNMARSHAL(TPM2B_MAX_BUFFER, buffer);
TPM2B_MARSHAL  (TPM2B_MAX_NV_BUFFER);
TPM2B_UNMARSHAL(TPM2B_MAX_NV_BUFFER, buffer);
TPM2B_MARSHAL  (TPM2B_IV);
TPM2B_UNMARSHAL(TPM2B_IV, buffer);
TPM2B_MARSHAL  (TPM2B_NAME);
TPM2B_UNMARSHAL(TPM2B_NAME, name);
TPM2B_MARSHAL  (TPM2B_ATTEST);
TPM2B_UNMARSHAL(TPM2B_ATTEST, attestationData);
TPM2B_MARSHAL  (TPM2B_SYM_KEY);
TPM2B_UNMARSHAL(TPM2B_SYM_KEY, buffer);
TPM2B_MARSHAL  (TPM2B_SENSITIVE_DATA);
TPM2B_UNMARSHAL(TPM2B_SENSITIVE_DATA, buffer);
TPM2B_MARSHAL  (TPM2B_PUBLIC_KEY_RSA);
TPM2B_UNMARSHAL(TPM2B_PUBLIC_KEY_RSA, buffer);
TPM2B_MARSHAL  (TPM2B_PRIVATE_KEY_RSA);
TPM2B_UNMARSHAL(TPM2B_PRIVATE_KEY_RSA, buffer);
TPM2B_MARSHAL  (TPM2B_ECC_PARAMETER);
TPM2B_UNMARSHAL(TPM2B_ECC_PARAMETER, buffer);
TPM2B_MARSHAL  (TPM2B_ENCRYPTED_SECRET);
TPM2B_UNMARSHAL(TPM2B_ENCRYPTED_SECRET, secret);
TPM2B_MARSHAL  (TPM2B_PRIVATE_VENDOR_SPECIFIC);
TPM2B_UNMARSHAL(TPM2B_PRIVATE_VENDOR_SPECIFIC, buffer);
TPM2B_MARSHAL  (TPM2B_PRIVATE);
TPM2B_UNMARSHAL(TPM2B_PRIVATE, buffer);
TPM2B_MARSHAL  (TPM2B_ID_OBJECT);
TPM2B_UNMARSHAL(TPM2B_ID_OBJECT, credential);
TPM2B_MARSHAL  (TPM2B_CONTEXT_SENSITIVE);
TPM2B_UNMARSHAL(TPM2B_CONTEXT_SENSITIVE, buffer);
TPM2B_MARSHAL  (TPM2B_CONTEXT_DATA);
TPM2B_UNMARSHAL(TPM2B_CONTEXT_DATA, buffer);
TPM2B_MARSHAL  (TPM2B_NONCE);
TPM2B_UNMARSHAL(TPM2B_NONCE, buffer);
TPM2B_MARSHAL  (TPM2B_TIMEOUT);
TPM2B_UNMARSHAL(TPM2B_TIMEOUT, buffer);
TPM2B_MARSHAL  (TPM2B_AUTH);
TPM2B_UNMARSHAL(TPM2B_AUTH, buffer);
TPM2B_MARSHAL  (TPM2B_OPERAND);
TPM2B_UNMARSHAL(TPM2B_OPERAND, buffer);
TPM2B_MARSHAL  (TPM2B_TEMPLATE);
TPM2B_UNMARSHAL(TPM2B_TEMPLATE, buffer);
TPM2B_MARSHAL(TPM2B_MAX_CAP_BUFFER);
TPM2B_UNMARSHAL(TPM2B_MAX_CAP_BUFFER, buffer);
TPM2B_MARSHAL_SUBTYPE(TPM2B_ECC_POINT, TPMS_ECC_POINT, point);
TPM2B_UNMARSHAL_SUBTYPE(TPM2B_ECC_POINT, TPMS_ECC_POINT, point);
TPM2B_MARSHAL_SUBTYPE(TPM2B_NV_PUBLIC, TPMS_NV_PUBLIC, nvPublic);
TPM2B_UNMARSHAL_SUBTYPE(TPM2B_NV_PUBLIC, TPMS_NV_PUBLIC, nvPublic);
TPM2B_MARSHAL_SUBTYPE(TPM2B_SENSITIVE, TPMT_SENSITIVE, sensitiveArea);
TPM2B_UNMARSHAL_SUBTYPE(TPM2B_SENSITIVE, TPMT_SENSITIVE, sensitiveArea);
TPM2B_MARSHAL_SUBTYPE(TPM2B_SENSITIVE_CREATE, TPMS_SENSITIVE_CREATE, sensitive);
TPM2B_UNMARSHAL_SUBTYPE(TPM2B_SENSITIVE_CREATE, TPMS_SENSITIVE_CREATE, sensitive);
TPM2B_MARSHAL_SUBTYPE(TPM2B_CREATION_DATA, TPMS_CREATION_DATA, creationData);
TPM2B_UNMARSHAL_SUBTYPE(TPM2B_CREATION_DATA, TPMS_CREATION_DATA, creationData);
TPM2B_MARSHAL_SUBTYPE(TPM2B_PUBLIC, TPMT_PUBLIC, publicArea);
TPM2B_UNMARSHAL_SUBTYPE(TPM2B_PUBLIC, TPMT_PUBLIC, publicArea);
