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

#define ADDR &
#define VAL
#define TAB_SIZE(tab) (sizeof(tab) / sizeof(tab[0]))

#define TPML_MARSHAL(type, marshal_func, buf_name, op) \
TSS2_RC Tss2_MU_##type##_Marshal(type const *src, uint8_t buffer[], \
                                 size_t buffer_size, size_t *offset) \
{ \
    size_t  local_offset = 0; \
    UINT32 i, count = 0; \
    TSS2_RC ret = TSS2_RC_SUCCESS; \
\
    if (offset != NULL) { \
        LOG_TRACE("offset non-NULL, initial value: %zu", *offset); \
        local_offset = *offset; \
    } \
\
    if (src == NULL) { \
        LOG_ERROR("src is NULL"); \
        return TSS2_MU_RC_BAD_REFERENCE; \
    } \
\
    if (buffer == NULL && offset == NULL) { \
        LOG_ERROR("buffer and offset parameter are NULL"); \
        return TSS2_MU_RC_BAD_REFERENCE; \
    } else if (buffer_size < local_offset || \
               buffer_size - local_offset < sizeof(count)) { \
        LOG_DEBUG( \
             "buffer_size: %zu with offset: %zu are insufficient for object " \
             "of size %zu", \
             buffer_size, \
             local_offset, \
             sizeof(count)); \
        return TSS2_MU_RC_INSUFFICIENT_BUFFER; \
    } \
\
    if (src->count > TAB_SIZE(src->buf_name)) { \
        LOG_WARNING("count too big"); \
        return TSS2_SYS_RC_BAD_VALUE; \
    } \
\
    LOG_DEBUG(\
         "Marshalling " #type " from 0x%" PRIxPTR " to buffer 0x%" PRIxPTR \
         " at index 0x%zx", \
         (uintptr_t)&src, \
         (uintptr_t)buffer, \
         local_offset); \
\
    ret = Tss2_MU_UINT32_Marshal(src->count, buffer, buffer_size, &local_offset); \
    if (ret) \
        return ret; \
\
    for (i = 0; i < src->count; i++) \
    { \
        ret = marshal_func(op src->buf_name[i], buffer, buffer_size, &local_offset); \
        if (ret) \
            return ret; \
    } \
    if (offset != NULL) { \
        *offset = local_offset; \
        LOG_DEBUG("offset parameter non-NULL updated to %zu", *offset); \
    } \
\
    return TSS2_RC_SUCCESS; \
}

#define TPML_UNMARSHAL(type, unmarshal_func, buf_name) \
TSS2_RC Tss2_MU_##type##_Unmarshal(uint8_t const buffer[], size_t buffer_size, \
                                   size_t *offset, type *dest) \
{ \
    size_t  local_offset = 0; \
    UINT32 i, count = 0; \
    TSS2_RC ret = TSS2_RC_SUCCESS; \
\
    if (offset != NULL) { \
        LOG_TRACE("offset non-NULL, initial value: %zu", *offset); \
        local_offset = *offset; \
    } \
\
    if (buffer == NULL || (dest == NULL && offset == NULL)) { \
        LOG_ERROR("buffer or dest and offset parameter are NULL"); \
        return TSS2_MU_RC_BAD_REFERENCE; \
    } else if (buffer_size < local_offset || \
               sizeof(count) > buffer_size - local_offset) \
    { \
        LOG_DEBUG( \
             "buffer_size: %zu with offset: %zu are insufficient for object " \
             "of size %zu", \
             buffer_size, \
             local_offset, \
             sizeof(count)); \
        return TSS2_MU_RC_INSUFFICIENT_BUFFER; \
    } \
\
    LOG_DEBUG(\
         "Unmarshaling " #type " from 0x%" PRIxPTR " to buffer 0x%" PRIxPTR \
         " at index 0x%zx", \
         (uintptr_t)buffer, \
         (uintptr_t)dest, \
         local_offset); \
\
    ret = Tss2_MU_UINT32_Unmarshal(buffer, buffer_size, &local_offset, &count); \
    if (ret) \
        return ret; \
\
    if (count > TAB_SIZE(dest->buf_name)) { \
        LOG_WARNING("count too big"); \
        return TSS2_SYS_RC_MALFORMED_RESPONSE; \
    } \
\
    if (dest != NULL) { \
        memset(dest, 0, sizeof(*dest)); \
        dest->count = count; \
    } \
\
    for (i = 0; i < count; i++) \
    { \
        ret = unmarshal_func(buffer, buffer_size, &local_offset, \
                             (dest == NULL)? NULL: &dest->buf_name[i]); \
        if (ret) \
            return ret; \
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
 * These macros expand to (un)marshal functions for each of the TPML types
 * the specification part 2.
 */
TPML_MARSHAL(TPML_CC, Tss2_MU_TPM2_CC_Marshal, commandCodes, VAL)
TPML_UNMARSHAL(TPML_CC, Tss2_MU_TPM2_CC_Unmarshal, commandCodes)
TPML_MARSHAL(TPML_CCA, Tss2_MU_TPMA_CC_Marshal, commandAttributes, VAL)
TPML_UNMARSHAL(TPML_CCA, Tss2_MU_TPMA_CC_Unmarshal, commandAttributes)
TPML_MARSHAL(TPML_ALG, Tss2_MU_UINT16_Marshal, algorithms, VAL)
TPML_UNMARSHAL(TPML_ALG, Tss2_MU_UINT16_Unmarshal, algorithms)
TPML_MARSHAL(TPML_HANDLE, Tss2_MU_UINT32_Marshal, handle, VAL)
TPML_UNMARSHAL(TPML_HANDLE, Tss2_MU_UINT32_Unmarshal, handle)
TPML_MARSHAL(TPML_DIGEST, Tss2_MU_TPM2B_DIGEST_Marshal, digests, ADDR)
TPML_UNMARSHAL(TPML_DIGEST, Tss2_MU_TPM2B_DIGEST_Unmarshal, digests)
TPML_MARSHAL(TPML_ALG_PROPERTY, Tss2_MU_TPMS_ALG_PROPERTY_Marshal, algProperties, ADDR)
TPML_UNMARSHAL(TPML_ALG_PROPERTY, Tss2_MU_TPMS_ALG_PROPERTY_Unmarshal, algProperties)
TPML_MARSHAL(TPML_ECC_CURVE, Tss2_MU_UINT16_Marshal, eccCurves, VAL)
TPML_UNMARSHAL(TPML_ECC_CURVE, Tss2_MU_UINT16_Unmarshal, eccCurves)
TPML_MARSHAL(TPML_TAGGED_TPM_PROPERTY, Tss2_MU_TPMS_TAGGED_PROPERTY_Marshal, tpmProperty, ADDR)
TPML_UNMARSHAL(TPML_TAGGED_TPM_PROPERTY, Tss2_MU_TPMS_TAGGED_PROPERTY_Unmarshal, tpmProperty)
TPML_MARSHAL(TPML_TAGGED_PCR_PROPERTY, Tss2_MU_TPMS_TAGGED_PCR_SELECT_Marshal, pcrProperty, ADDR)
TPML_UNMARSHAL(TPML_TAGGED_PCR_PROPERTY, Tss2_MU_TPMS_TAGGED_PCR_SELECT_Unmarshal, pcrProperty)
TPML_MARSHAL(TPML_PCR_SELECTION, Tss2_MU_TPMS_PCR_SELECTION_Marshal, pcrSelections, ADDR)
TPML_UNMARSHAL(TPML_PCR_SELECTION, Tss2_MU_TPMS_PCR_SELECTION_Unmarshal, pcrSelections)
TPML_MARSHAL(TPML_DIGEST_VALUES, Tss2_MU_TPMT_HA_Marshal, digests, ADDR)
TPML_UNMARSHAL(TPML_DIGEST_VALUES, Tss2_MU_TPMT_HA_Unmarshal, digests)
TPML_MARSHAL(TPML_INTEL_PTT_PROPERTY, Tss2_MU_UINT32_Marshal, property, VAL)
TPML_UNMARSHAL(TPML_INTEL_PTT_PROPERTY, Tss2_MU_UINT32_Unmarshal, property)
TPML_MARSHAL(TPML_AC_CAPABILITIES, Tss2_MU_TPMS_AC_OUTPUT_Marshal, acCapabilities, ADDR)
TPML_UNMARSHAL(TPML_AC_CAPABILITIES, Tss2_MU_TPMS_AC_OUTPUT_Unmarshal, acCapabilities)
TPML_MARSHAL(TPML_TAGGED_POLICY, Tss2_MU_TPMS_TAGGED_POLICY_Marshal, policies, ADDR)
TPML_UNMARSHAL(TPML_TAGGED_POLICY, Tss2_MU_TPMS_TAGGED_POLICY_Unmarshal, policies)
TPML_MARSHAL(TPML_ACT_DATA, Tss2_MU_TPMS_ACT_DATA_Marshal, actData, ADDR)
TPML_UNMARSHAL(TPML_ACT_DATA, Tss2_MU_TPMS_ACT_DATA_Unmarshal, actData)
