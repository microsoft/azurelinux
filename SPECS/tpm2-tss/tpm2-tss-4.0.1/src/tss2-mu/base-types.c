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

#include "util/tss2_endian.h"
#define LOGMODULE marshal
#include "util/log.h"

#define BASE_MARSHAL(type) \
TSS2_RC \
Tss2_MU_##type##_Marshal ( \
    type           src, \
    uint8_t        buffer [], \
    size_t         buffer_size, \
    size_t        *offset) \
{ \
    size_t  local_offset = 0; \
\
    if (offset != NULL) { \
        LOG_TRACE("offset non-NULL, initial value: %zu", *offset); \
        local_offset = *offset; \
    } \
\
    if (buffer == NULL && offset == NULL) { \
        LOG_ERROR("buffer and offset parameter are NULL"); \
        return TSS2_MU_RC_BAD_REFERENCE; \
    } else if (buffer == NULL && offset != NULL) { \
        *offset += sizeof (src); \
        LOG_TRACE("buffer NULL and offset non-NULL, updating offset to %zu", \
             *offset); \
        return TSS2_RC_SUCCESS; \
    } else if (buffer_size < local_offset || \
               buffer_size - local_offset < sizeof (src)) \
    { \
        LOG_DEBUG( \
             "buffer_size: %zu with offset: %zu are insufficient for object " \
             "of size %zu", \
             buffer_size, \
             local_offset, \
             sizeof (src)); \
        return TSS2_MU_RC_INSUFFICIENT_BUFFER; \
    } \
\
    LOG_DEBUG(\
         "Marshalling " #type " from 0x%" PRIxPTR " to buffer 0x%" PRIxPTR \
         " at index 0x%zx", \
         (uintptr_t)&src, \
         (uintptr_t)buffer, \
         local_offset); \
\
    switch (sizeof (type)) { \
        case 1: \
            break; \
        case 2: \
            src = (type)HOST_TO_BE_16((UINT16)src); \
            break; \
        case 4: \
            src = (type)HOST_TO_BE_32((UINT32)src); \
            break; \
        case 8: \
            src = (type)HOST_TO_BE_64((UINT64)src); \
            break; \
\
    } \
    memcpy (&buffer [local_offset], &src, sizeof (src)); \
    if (offset != NULL) { \
        *offset = local_offset + sizeof (src); \
        LOG_DEBUG("offset parameter non-NULL, updated to %zu", *offset); \
    } \
\
    return TSS2_RC_SUCCESS; \
}

#define BASE_UNMARSHAL(type) \
TSS2_RC \
Tss2_MU_##type##_Unmarshal ( \
    uint8_t const buffer[], \
    size_t        buffer_size, \
    size_t       *offset, \
    type         *dest) \
{ \
    size_t  local_offset = 0; \
    type tmp = 0; \
\
    if (offset != NULL) { \
        LOG_TRACE("offset non-NULL, initial value: %zu", *offset); \
        local_offset = *offset; \
    } \
\
    if (buffer == NULL || (dest == NULL && offset == NULL)) { \
        LOG_ERROR("buffer or dest and offset parameter are NULL"); \
        return TSS2_MU_RC_BAD_REFERENCE; \
    } \
    if (buffer_size < local_offset || \
        sizeof (*dest) > buffer_size - local_offset) \
    { \
        LOG_DEBUG( \
             "buffer_size: %zu with offset: %zu are insufficient for object " \
             "of size %zu", buffer_size, local_offset, sizeof (*dest)); \
        return TSS2_MU_RC_INSUFFICIENT_BUFFER; \
    } \
    if (dest == NULL && offset != NULL) { \
        *offset += sizeof (type); \
        LOG_TRACE(\
             "buffer NULL and offset non-NULL, updating offset to %zu", \
             *offset); \
        return TSS2_RC_SUCCESS; \
    } \
\
    LOG_DEBUG(\
         "Unmarshaling " #type " from 0x%" PRIxPTR " to buffer 0x%" PRIxPTR \
         " at index 0x%zx", \
         (uintptr_t)buffer, \
         (uintptr_t)dest, \
         local_offset); \
\
    memcpy (&tmp, &buffer [local_offset], sizeof (tmp)); \
\
    switch (sizeof (type)) { \
        case 1: \
            *dest = (type)tmp; \
            break; \
        case 2: \
            *dest = (type)BE_TO_HOST_16((UINT16)tmp); \
            break; \
        case 4: \
            *dest = (type)BE_TO_HOST_32((UINT32)tmp); \
            break; \
        case 8: \
            *dest = (type)BE_TO_HOST_64((UINT64)tmp); \
            break; \
\
    } \
\
    if (offset != NULL) { \
        *offset = local_offset + sizeof (*dest); \
        LOG_DEBUG("offset parameter non-NULL, updated to %zu", *offset); \
    } \
\
    return TSS2_RC_SUCCESS; \
}

/*
 * These macros expand to (un)marshal functions for each of the base types
 * the specification part 2, table 3: Definition of Base Types.
 */
BASE_MARSHAL  (BYTE)
BASE_UNMARSHAL(BYTE)
BASE_MARSHAL  (INT8)
BASE_UNMARSHAL(INT8)
BASE_MARSHAL  (INT16)
BASE_UNMARSHAL(INT16)
BASE_MARSHAL  (INT32)
BASE_UNMARSHAL(INT32)
BASE_MARSHAL  (INT64)
BASE_UNMARSHAL(INT64)
BASE_MARSHAL  (UINT8)
BASE_UNMARSHAL(UINT8)
BASE_MARSHAL  (UINT16)
BASE_UNMARSHAL(UINT16)
BASE_MARSHAL  (UINT32)
BASE_UNMARSHAL(UINT32)
BASE_MARSHAL  (UINT64)
BASE_UNMARSHAL(UINT64)
BASE_MARSHAL  (TPM2_CC)
BASE_UNMARSHAL(TPM2_CC)
BASE_MARSHAL  (TPM2_ST)
BASE_UNMARSHAL(TPM2_ST)
BASE_MARSHAL  (TPM2_SE)
BASE_UNMARSHAL(TPM2_SE)
BASE_MARSHAL  (TPM2_NT)
BASE_UNMARSHAL(TPM2_NT)
BASE_MARSHAL  (TPM2_HANDLE)
BASE_UNMARSHAL(TPM2_HANDLE)
BASE_MARSHAL  (TPMI_ALG_HASH)
BASE_UNMARSHAL(TPMI_ALG_HASH)
