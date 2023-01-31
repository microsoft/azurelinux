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

#define TPMS_PCR_MARSHAL(type, firstFieldMarshal) \
TSS2_RC \
Tss2_MU_##type##_Marshal(const type *src, uint8_t buffer[], \
                           size_t buffer_size, size_t *offset) \
{ \
    TSS2_RC ret = TSS2_RC_SUCCESS; \
    size_t local_offset = 0; \
    UINT8 i; \
\
    if (!src) { \
        LOG_WARNING("src param is NULL"); \
        return TSS2_MU_RC_BAD_REFERENCE; \
    } \
\
    if (offset) { \
        local_offset = *offset; \
    } else if (!buffer) { \
        return TSS2_MU_RC_BAD_REFERENCE; \
    } \
\
    LOG_DEBUG( \
         "Marshalling " #type " from 0x%" PRIxPTR " to buffer 0x%" PRIxPTR \
         " at index 0x%zx", (uintptr_t)&src, (uintptr_t)buffer, \
         offset?*offset:0xffff); \
\
    if (src->sizeofSelect > TAB_SIZE(src->pcrSelect)) { \
        LOG_ERROR("sizeofSelect value %"PRIu8"/%zi too big", src->sizeofSelect, \
                  TAB_SIZE(src->pcrSelect)); \
        return TSS2_SYS_RC_BAD_VALUE; \
    } \
\
    ret = firstFieldMarshal; \
    if (ret != TSS2_RC_SUCCESS) \
        return ret; \
\
    ret = Tss2_MU_UINT8_Marshal(src->sizeofSelect, buffer, buffer_size, &local_offset); \
    if (ret != TSS2_RC_SUCCESS) \
        return ret; \
\
    for (i = 0; i < src->sizeofSelect; i++) { \
        ret = Tss2_MU_BYTE_Marshal(src->pcrSelect[i], buffer, buffer_size, \
                                    &local_offset); \
        if (ret != TSS2_RC_SUCCESS) \
            return ret; \
    } \
\
    if (offset) { \
        *offset = local_offset; \
    } \
\
    return TSS2_RC_SUCCESS; \
}

TPMS_PCR_MARSHAL(TPMS_PCR_SELECT, TSS2_RC_SUCCESS)

TPMS_PCR_MARSHAL(TPMS_PCR_SELECTION, \
    Tss2_MU_TPMI_ALG_HASH_Marshal(src->hash, buffer, buffer_size, &local_offset))

TPMS_PCR_MARSHAL(TPMS_TAGGED_PCR_SELECT, \
    Tss2_MU_UINT32_Marshal(src->tag, buffer, buffer_size, &local_offset))

#define TPMS_PCR_UNMARSHAL(type, firstFieldUnmarshal) \
TSS2_RC \
Tss2_MU_##type##_Unmarshal(uint8_t const buffer[], size_t buffer_size, \
                                    size_t *offset, type *dest) \
{ \
    TSS2_RC ret = TSS2_RC_SUCCESS; \
    size_t local_offset = 0; \
    UINT8 i, tmp; \
\
    LOG_DEBUG( \
         "Unmarshaling " #type " from 0x%" PRIxPTR " to buffer 0x%" PRIxPTR \
         " at index 0x%zx", (uintptr_t)dest, (uintptr_t)buffer, \
         offset?*offset:0xffff); \
\
    if (offset) { \
        local_offset = *offset; \
    } else if (!dest) { \
        return TSS2_MU_RC_BAD_REFERENCE; \
    } \
\
    if (dest) \
        memset(dest, 0, sizeof(*dest)); \
\
    ret = firstFieldUnmarshal; \
    if (ret != TSS2_RC_SUCCESS) \
        return ret; \
\
    ret = Tss2_MU_UINT8_Unmarshal(buffer, buffer_size, &local_offset, \
                                  dest? &dest->sizeofSelect : &tmp); \
    if (ret) \
        return ret; \
\
    if ((dest? dest->sizeofSelect : tmp) > TAB_SIZE(dest->pcrSelect)) { \
        LOG_ERROR("sizeofSelect value %"PRIu8" / %zi too big", \
                  dest? dest->sizeofSelect : tmp, TAB_SIZE(dest->pcrSelect)); \
        return TSS2_SYS_RC_MALFORMED_RESPONSE; \
    } \
\
    for (i = 0; i < (dest? dest->sizeofSelect : tmp); i++) \
    { \
        ret = Tss2_MU_UINT8_Unmarshal(buffer, buffer_size, &local_offset, \
                                      dest? &dest->pcrSelect[i] : NULL); \
        if (ret != TSS2_RC_SUCCESS) \
            return ret; \
    } \
\
    if (offset) { \
        *offset = local_offset; \
    } \
\
    return TSS2_RC_SUCCESS; \
}

TPMS_PCR_UNMARSHAL(TPMS_PCR_SELECT, TSS2_RC_SUCCESS)

TPMS_PCR_UNMARSHAL(TPMS_PCR_SELECTION, \
    Tss2_MU_TPMI_ALG_HASH_Unmarshal(buffer, buffer_size, &local_offset, \
                                    dest? &dest->hash : NULL))

TPMS_PCR_UNMARSHAL(TPMS_TAGGED_PCR_SELECT, \
    Tss2_MU_UINT32_Unmarshal(buffer, buffer_size, &local_offset, \
                             dest? &dest->tag : NULL))

#define TPMS_MARSHAL_0(type) \
TSS2_RC Tss2_MU_##type##_Marshal(type const *src, \
                                 uint8_t buffer[], \
                                 size_t buffer_size, \
                                 size_t *offset) \
{ \
    UNUSED(buffer); \
    UNUSED(buffer_size); \
    UNUSED(offset); \
    if (!src) { \
        LOG_WARNING("src param is NULL"); \
        return TSS2_MU_RC_BAD_REFERENCE; \
    } \
\
    LOG_DEBUG( \
         "Marshalling " #type " from 0x%" PRIxPTR " to buffer 0x%" PRIxPTR \
         " at index 0x%zx", (uintptr_t)&src,  (uintptr_t)buffer, *offset); \
\
    return TSS2_RC_SUCCESS; \
}

#define TPMS_UNMARSHAL_0(type) \
TSS2_RC Tss2_MU_##type##_Unmarshal(uint8_t const buffer[], size_t buffer_size, \
                                   size_t *offset, type *dest) \
{ \
    UNUSED(buffer); \
    UNUSED(buffer_size); \
    UNUSED(offset); \
\
    if (!dest) { \
        LOG_WARNING("src param is NULL"); \
        return TSS2_MU_RC_BAD_REFERENCE; \
    } \
\
    LOG_DEBUG( \
         "Unmarshaling " #type " from 0x%" PRIxPTR " to buffer 0x%" PRIxPTR \
         " at index 0x%zx", (uintptr_t)dest,  (uintptr_t)buffer, *offset); \
\
    return TSS2_RC_SUCCESS; \
}

#define TPMS_MARSHAL_1(type, m, op, fn) \
TSS2_RC Tss2_MU_##type##_Marshal(type const *src, uint8_t buffer[], \
                                 size_t buffer_size, size_t *offset) \
{ \
    if (!src) { \
        LOG_WARNING("src param is NULL"); \
        return TSS2_MU_RC_BAD_REFERENCE; \
    } \
\
    LOG_DEBUG(\
         "Marshalling " #type " from 0x%" PRIxPTR " to buffer 0x%" PRIxPTR \
         " at index 0x%zx", (uintptr_t)&src,  (uintptr_t)buffer, offset?*offset:0xffff); \
\
    return fn(op src->m, buffer, buffer_size, offset); \
}

#define TPMS_UNMARSHAL_1(type, m, fn) \
TSS2_RC Tss2_MU_##type##_Unmarshal(uint8_t const buffer[], size_t buffer_size, \
                                   size_t *offset, type *dest) \
{ \
    LOG_DEBUG(\
         "Unmarshaling " #type " from 0x%" PRIxPTR " to buffer 0x%" PRIxPTR \
         " at index 0x%zx", (uintptr_t)dest,  (uintptr_t)buffer, offset?*offset:0xffff); \
\
    return fn(buffer, buffer_size, offset, dest ? &dest->m : NULL); \
}

#define TPMS_MARSHAL_2_U(type, m1, op1, fn1, m2, op2, fn2) \
TSS2_RC Tss2_MU_##type##_Marshal(type const *src, uint8_t buffer[], \
                                 size_t buffer_size, size_t *offset) \
{ \
    TSS2_RC ret = TSS2_RC_SUCCESS; \
    size_t local_offset = 0; \
\
    if (!src) { \
        LOG_WARNING("src param is NULL"); \
        return TSS2_MU_RC_BAD_REFERENCE; \
    } \
\
    if (offset) {\
        local_offset = *offset; \
    } else if (!buffer) { \
        return TSS2_MU_RC_BAD_REFERENCE; \
    } \
\
    LOG_DEBUG(\
         "Marshalling " #type " from 0x%" PRIxPTR " to buffer 0x%" PRIxPTR \
         " at index 0x%zx", (uintptr_t)&src,  (uintptr_t)buffer, offset?*offset:0xffff); \
\
    ret = fn1(op1 src->m1, buffer, buffer_size, &local_offset); \
    if (ret != TSS2_RC_SUCCESS) \
        return ret; \
\
    ret = fn2(op2 src->m2, src->m1, buffer, buffer_size, &local_offset); \
\
    if (offset && ret == TSS2_RC_SUCCESS) { \
        *offset = local_offset; \
    } \
    return ret; \
}

#define TPMS_UNMARSHAL_2_U(type, m1, fn1, m2, fn2) \
TSS2_RC Tss2_MU_##type##_Unmarshal(uint8_t const buffer[], size_t buffer_size, \
                                   size_t *offset, type *dest) \
{ \
    TSS2_RC ret = TSS2_RC_SUCCESS; \
    size_t local_offset = 0; \
    type tmp_dest; \
\
    LOG_DEBUG(\
         "Unmarshaling " #type " from 0x%" PRIxPTR " to buffer 0x%" PRIxPTR \
         " at index 0x%zx", (uintptr_t)dest,  (uintptr_t)buffer, offset?*offset:0xffff); \
\
    if (offset) { \
        local_offset = *offset; \
    } else if (!dest) { \
        return TSS2_MU_RC_BAD_REFERENCE; \
    } \
\
    if (dest) \
        memset(dest, 0, sizeof(*dest)); \
\
    ret = fn1(buffer, buffer_size, &local_offset, dest ? &dest->m1 : &tmp_dest.m1); \
    if (ret != TSS2_RC_SUCCESS) \
        return ret; \
\
    ret = fn2(buffer, buffer_size, &local_offset, dest ? dest->m1 : tmp_dest.m1, dest ? &dest->m2 : NULL); \
\
    if (offset && ret == TSS2_RC_SUCCESS) { \
        *offset = local_offset; \
    } \
    return ret; \
}

#define TPMS_MARSHAL_2(type, m1, op1, fn1, m2, op2, fn2) \
TSS2_RC Tss2_MU_##type##_Marshal(type const *src, uint8_t buffer[], \
                                 size_t buffer_size, size_t *offset) \
{ \
    TSS2_RC ret = TSS2_RC_SUCCESS; \
    size_t local_offset = 0; \
\
    if (!src) { \
        LOG_WARNING("src param is NULL"); \
        return TSS2_MU_RC_BAD_REFERENCE; \
    } \
\
    if (offset) { \
        local_offset = *offset; \
    } else if (!buffer) { \
        return TSS2_MU_RC_BAD_REFERENCE; \
    } \
\
    LOG_DEBUG(\
         "Marshalling " #type " from 0x%" PRIxPTR " to buffer 0x%" PRIxPTR \
         " at index 0x%zx", (uintptr_t)&src,  (uintptr_t)buffer, offset?*offset:0xffff); \
\
    ret = fn1(op1 src->m1, buffer, buffer_size, &local_offset); \
    if (ret != TSS2_RC_SUCCESS) \
        return ret; \
\
    ret = fn2(op2 src->m2, buffer, buffer_size, &local_offset); \
\
    if (offset && ret == TSS2_RC_SUCCESS) { \
        *offset = local_offset; \
    } \
    return ret; \
}

#define TPMS_UNMARSHAL_2(type, m1, fn1, m2, fn2) \
TSS2_RC Tss2_MU_##type##_Unmarshal(uint8_t const buffer[], size_t buffer_size, \
                                   size_t *offset, type *dest) \
{ \
    TSS2_RC ret = TSS2_RC_SUCCESS; \
    size_t local_offset = 0; \
\
    LOG_DEBUG(\
         "Unmarshaling " #type " from 0x%" PRIxPTR " to buffer 0x%" PRIxPTR \
         " at index 0x%zx", (uintptr_t)dest,  (uintptr_t)buffer, offset?*offset:0xffff); \
\
    if (offset) { \
        local_offset = *offset; \
    } else if (!dest) { \
        return TSS2_MU_RC_BAD_REFERENCE; \
    } \
\
    if (dest) \
        memset(dest, 0, sizeof(*dest)); \
\
    ret = fn1(buffer, buffer_size, &local_offset, dest ? &dest->m1 : NULL); \
    if (ret != TSS2_RC_SUCCESS) \
        return ret; \
\
    ret = fn2(buffer, buffer_size, &local_offset, dest ? &dest->m2 : NULL); \
\
    if (offset && ret == TSS2_RC_SUCCESS) { \
        *offset = local_offset; \
    } \
    return ret; \
}

#define TPMS_MARSHAL_3(type, m1, op1, fn1, m2, op2, fn2, m3, op3, fn3) \
TSS2_RC Tss2_MU_##type##_Marshal(type const *src, uint8_t buffer[], \
                                 size_t buffer_size, size_t *offset) \
{ \
    TSS2_RC ret = TSS2_RC_SUCCESS; \
    size_t local_offset = 0; \
\
    if (!src) { \
        LOG_WARNING("src param is NULL"); \
        return TSS2_MU_RC_BAD_REFERENCE; \
    } \
\
    if (offset) { \
        local_offset = *offset; \
    } else if (!buffer) { \
        return TSS2_MU_RC_BAD_REFERENCE; \
    } \
\
    LOG_DEBUG(\
         "Marshalling " #type " from 0x%" PRIxPTR " to buffer 0x%" PRIxPTR \
         " at index 0x%zx", (uintptr_t)&src,  (uintptr_t)buffer, offset?*offset:0xffff); \
\
    ret = fn1(op1 src->m1, buffer, buffer_size, &local_offset); \
    if (ret != TSS2_RC_SUCCESS) \
        return ret; \
\
    ret = fn2(op2 src->m2, buffer, buffer_size, &local_offset); \
    if (ret != TSS2_RC_SUCCESS) \
        return ret; \
\
    ret = fn3(op3 src->m3, buffer, buffer_size, &local_offset); \
\
    if (offset && ret == TSS2_RC_SUCCESS) { \
        *offset = local_offset; \
    } \
    return ret; \
}

#define TPMS_UNMARSHAL_3(type, m1, fn1, m2, fn2, m3, fn3) \
TSS2_RC Tss2_MU_##type##_Unmarshal(uint8_t const buffer[], size_t buffer_size, \
                                   size_t *offset, type *dest) \
{ \
    TSS2_RC ret = TSS2_RC_SUCCESS; \
    size_t local_offset = 0; \
\
    LOG_DEBUG(\
         "Unmarshaling " #type " from 0x%" PRIxPTR " to buffer 0x%" PRIxPTR \
         " at index 0x%zx", (uintptr_t)dest,  (uintptr_t)buffer, offset?*offset:0xffff); \
\
    if (offset) { \
        local_offset = *offset; \
    } else if (!dest) { \
        return TSS2_MU_RC_BAD_REFERENCE; \
    } \
\
    if (dest) \
        memset(dest, 0, sizeof(*dest)); \
\
    ret = fn1(buffer, buffer_size, &local_offset, dest ? &dest->m1 : NULL); \
    if (ret != TSS2_RC_SUCCESS) \
        return ret; \
\
    ret = fn2(buffer, buffer_size, &local_offset, dest ? &dest->m2 : NULL); \
    if (ret != TSS2_RC_SUCCESS) \
        return ret; \
\
    ret = fn3(buffer, buffer_size, &local_offset, dest ? &dest->m3 : NULL); \
\
    if (offset && ret == TSS2_RC_SUCCESS) { \
        *offset = local_offset; \
    } \
    return ret; \
}

#define TPMS_MARSHAL_4(type, m1, op1, fn1, m2, op2, fn2, m3, op3, fn3, m4, op4, fn4) \
TSS2_RC Tss2_MU_##type##_Marshal(type const *src, uint8_t buffer[], \
                                 size_t buffer_size, size_t *offset) \
{ \
    TSS2_RC ret = TSS2_RC_SUCCESS; \
    size_t local_offset = 0; \
\
    if (!src) { \
        LOG_WARNING("src param is NULL"); \
        return TSS2_MU_RC_BAD_REFERENCE; \
    } \
\
    if (offset) { \
        local_offset = *offset; \
    } else if (!buffer) { \
        return TSS2_MU_RC_BAD_REFERENCE; \
    } \
\
    LOG_DEBUG(\
         "Marshalling " #type " from 0x%" PRIxPTR " to buffer 0x%" PRIxPTR \
         " at index 0x%zx", (uintptr_t)&src,  (uintptr_t)buffer, offset?*offset:0xffff); \
\
    ret = fn1(op1 src->m1, buffer, buffer_size, &local_offset); \
    if (ret != TSS2_RC_SUCCESS) \
        return ret; \
\
    ret = fn2(op2 src->m2, buffer, buffer_size, &local_offset); \
    if (ret != TSS2_RC_SUCCESS) \
        return ret; \
\
    ret = fn3(op3 src->m3, buffer, buffer_size, &local_offset); \
    if (ret != TSS2_RC_SUCCESS) \
        return ret; \
\
    ret = fn4(op4 src->m4, buffer, buffer_size, &local_offset); \
\
    if (offset && ret == TSS2_RC_SUCCESS) { \
        *offset = local_offset; \
    } \
    return ret; \
}

#define TPMS_UNMARSHAL_4(type, m1, fn1, m2, fn2, m3, fn3, m4, fn4) \
TSS2_RC Tss2_MU_##type##_Unmarshal(uint8_t const buffer[], size_t buffer_size, \
                                   size_t *offset, type *dest) \
{ \
    TSS2_RC ret = TSS2_RC_SUCCESS; \
    size_t local_offset = 0; \
\
    if (offset) { \
        local_offset = *offset; \
    } else if (!dest) { \
        return TSS2_MU_RC_BAD_REFERENCE; \
    } \
\
    if (dest) \
        memset(dest, 0, sizeof(*dest)); \
\
    LOG_DEBUG(\
         "Unmarshaling " #type " from 0x%" PRIxPTR " to buffer 0x%" PRIxPTR \
         " at index 0x%zx", (uintptr_t)dest,  (uintptr_t)buffer, offset?*offset:0xffff); \
\
    ret = fn1(buffer, buffer_size, &local_offset, dest ? &dest->m1 : NULL); \
    if (ret != TSS2_RC_SUCCESS) \
        return ret; \
\
    ret = fn2(buffer, buffer_size, &local_offset, dest ? &dest->m2 : NULL); \
    if (ret != TSS2_RC_SUCCESS) \
        return ret; \
\
    ret = fn3(buffer, buffer_size, &local_offset, dest ? &dest->m3 : NULL); \
    if (ret != TSS2_RC_SUCCESS) \
        return ret; \
\
    ret = fn4(buffer, buffer_size, &local_offset, dest ? &dest->m4 : NULL); \
\
    if (offset && ret == TSS2_RC_SUCCESS) { \
        *offset = local_offset; \
    } \
    return ret; \
}

#define TPMS_MARSHAL_5(type, m1, op1, fn1, m2, op2, fn2, m3, op3, fn3, \
                       m4, op4, fn4, m5, op5, fn5) \
TSS2_RC Tss2_MU_##type##_Marshal(type const *src, uint8_t buffer[], \
                                 size_t buffer_size, size_t *offset) \
{ \
    TSS2_RC ret = TSS2_RC_SUCCESS; \
    size_t local_offset = 0; \
\
    if (!src) { \
        LOG_WARNING("src param is NULL"); \
        return TSS2_MU_RC_BAD_REFERENCE; \
    } \
\
    if (offset) { \
        local_offset = *offset; \
    } else if (!buffer) { \
        return TSS2_MU_RC_BAD_REFERENCE; \
    } \
\
    LOG_DEBUG(\
         "Marshalling " #type " from 0x%" PRIxPTR " to buffer 0x%" PRIxPTR \
         " at index 0x%zx", (uintptr_t)&src,  (uintptr_t)buffer, offset?*offset:0xffff); \
\
    ret = fn1(op1 src->m1, buffer, buffer_size, &local_offset); \
    if (ret != TSS2_RC_SUCCESS) \
        return ret; \
\
    ret = fn2(op2 src->m2, buffer, buffer_size, &local_offset); \
    if (ret != TSS2_RC_SUCCESS) \
        return ret; \
\
    ret = fn3(op3 src->m3, buffer, buffer_size, &local_offset); \
    if (ret != TSS2_RC_SUCCESS) \
        return ret; \
\
    ret = fn4(op4 src->m4, buffer, buffer_size, &local_offset); \
    if (ret != TSS2_RC_SUCCESS) \
        return ret; \
\
    ret = fn5(op5 src->m5, buffer, buffer_size, &local_offset); \
\
    if (offset && ret == TSS2_RC_SUCCESS) { \
        *offset = local_offset; \
    } \
    return ret; \
}

#define TPMS_UNMARSHAL_5(type, m1, fn1, m2, fn2, m3, fn3, m4, fn4, m5, fn5) \
TSS2_RC Tss2_MU_##type##_Unmarshal(uint8_t const buffer[], size_t buffer_size, \
                                   size_t *offset, type *dest) \
{ \
    TSS2_RC ret = TSS2_RC_SUCCESS; \
    size_t local_offset = 0; \
\
    LOG_DEBUG(\
         "Unmarshaling " #type " from 0x%" PRIxPTR " to buffer 0x%" PRIxPTR \
         " at index 0x%zx", (uintptr_t)dest,  (uintptr_t)buffer, offset?*offset:0xffff); \
\
    if (offset) { \
        local_offset = *offset; \
    } else if (!dest) { \
        return TSS2_MU_RC_BAD_REFERENCE; \
    } \
\
    if (dest) \
        memset(dest, 0, sizeof(*dest)); \
\
    ret = fn1(buffer, buffer_size, &local_offset, dest ? &dest->m1 : NULL); \
    if (ret != TSS2_RC_SUCCESS) \
        return ret; \
\
    ret = fn2(buffer, buffer_size, &local_offset, dest ? &dest->m2 : NULL); \
    if (ret != TSS2_RC_SUCCESS) \
        return ret; \
\
    ret = fn3(buffer, buffer_size, &local_offset, dest ? &dest->m3 : NULL); \
    if (ret != TSS2_RC_SUCCESS) \
        return ret; \
\
    ret = fn4(buffer, buffer_size, &local_offset, dest ? &dest->m4 : NULL); \
    if (ret != TSS2_RC_SUCCESS) \
        return ret; \
\
    ret = fn5(buffer, buffer_size, &local_offset, dest ? &dest->m5 : NULL); \
\
    if (offset && ret == TSS2_RC_SUCCESS) { \
        *offset = local_offset; \
    } \
    return ret; \
}

#define TPMS_MARSHAL_7(type, m1, op1, fn1, m2, op2, fn2, m3, op3, fn3, \
                       m4, op4, fn4, m5, op5, fn5, m6, op6, fn6, m7, op7, fn7) \
TSS2_RC Tss2_MU_##type##_Marshal(type const *src, uint8_t buffer[], \
                                 size_t buffer_size, size_t *offset) \
{ \
    TSS2_RC ret = TSS2_RC_SUCCESS; \
    size_t local_offset = 0; \
\
    if (!src) { \
        LOG_WARNING("src param is NULL"); \
        return TSS2_MU_RC_BAD_REFERENCE; \
    } \
\
    if (offset) { \
        local_offset = *offset; \
    } else if (!buffer) { \
        return TSS2_MU_RC_BAD_REFERENCE; \
    } \
\
    LOG_DEBUG(\
         "Marshalling " #type " from 0x%" PRIxPTR " to buffer 0x%" PRIxPTR \
         " at index 0x%zx", (uintptr_t)&src,  (uintptr_t)buffer, offset?*offset:0xffff); \
\
    ret = fn1(op1 src->m1, buffer, buffer_size, &local_offset); \
    if (ret != TSS2_RC_SUCCESS) \
        return ret; \
\
    ret = fn2(op2 src->m2, buffer, buffer_size, &local_offset); \
    if (ret != TSS2_RC_SUCCESS) \
        return ret; \
\
    ret = fn3(op3 src->m3, buffer, buffer_size, &local_offset); \
    if (ret != TSS2_RC_SUCCESS) \
        return ret; \
\
    ret = fn4(op4 src->m4, buffer, buffer_size, &local_offset); \
    if (ret != TSS2_RC_SUCCESS) \
        return ret; \
\
    ret = fn5(op5 src->m5, buffer, buffer_size, &local_offset); \
    if (ret != TSS2_RC_SUCCESS) \
        return ret; \
\
    ret = fn6(op6 src->m6, buffer, buffer_size, &local_offset); \
    if (ret != TSS2_RC_SUCCESS) \
        return ret; \
\
    ret = fn7(op7 src->m7, buffer, buffer_size, &local_offset); \
\
    if (offset && ret == TSS2_RC_SUCCESS) { \
        *offset = local_offset; \
    } \
    return ret; \
}

#define TPMS_UNMARSHAL_7(type, m1, fn1, m2, fn2, m3, fn3, m4, fn4, m5, fn5, m6, fn6, m7, fn7) \
TSS2_RC Tss2_MU_##type##_Unmarshal(uint8_t const buffer[], size_t buffer_size, \
                                   size_t *offset, type *dest) \
{ \
    TSS2_RC ret = TSS2_RC_SUCCESS; \
    size_t local_offset = 0; \
\
    LOG_DEBUG(\
         "Unmarshaling " #type " from 0x%" PRIxPTR " to buffer 0x%" PRIxPTR \
         " at index 0x%zx", (uintptr_t)dest,  (uintptr_t)buffer, offset?*offset:0xffff); \
\
    if (offset) { \
        local_offset = *offset; \
    } else if (!dest) { \
        return TSS2_MU_RC_BAD_REFERENCE; \
    } \
\
    if (dest) \
        memset(dest, 0, sizeof(*dest)); \
\
    ret = fn1(buffer, buffer_size, &local_offset, dest ? &dest->m1 : NULL); \
    if (ret != TSS2_RC_SUCCESS) \
        return ret; \
\
    ret = fn2(buffer, buffer_size, &local_offset, dest ? &dest->m2 : NULL); \
    if (ret != TSS2_RC_SUCCESS) \
        return ret; \
\
    ret = fn3(buffer, buffer_size, &local_offset, dest ? &dest->m3 : NULL); \
    if (ret != TSS2_RC_SUCCESS) \
        return ret; \
\
    ret = fn4(buffer, buffer_size, &local_offset, dest ? &dest->m4 : NULL); \
    if (ret != TSS2_RC_SUCCESS) \
        return ret; \
\
    ret = fn5(buffer, buffer_size, &local_offset, dest ? &dest->m5 : NULL); \
    if (ret != TSS2_RC_SUCCESS) \
        return ret; \
\
    ret = fn6(buffer, buffer_size, &local_offset, dest ? &dest->m6 : NULL); \
    if (ret != TSS2_RC_SUCCESS) \
        return ret; \
\
    ret = fn7(buffer, buffer_size, &local_offset, dest ? &dest->m7 : NULL); \
\
    if (offset && ret == TSS2_RC_SUCCESS) { \
        *offset = local_offset; \
    } \
    return ret; \
}

#define TPMS_MARSHAL_7_U(type, m1, op1, fn1, m2, op2, fn2, m3, op3, fn3, \
                       m4, op4, fn4, m5, op5, fn5, m6, op6, fn6, m7, op7, fn7) \
TSS2_RC Tss2_MU_##type##_Marshal(type const *src, uint8_t buffer[], \
                                 size_t buffer_size, size_t *offset) \
{ \
    TSS2_RC ret = TSS2_RC_SUCCESS; \
    size_t local_offset = 0; \
\
    if (!src) { \
        LOG_WARNING("src param is NULL"); \
        return TSS2_MU_RC_BAD_REFERENCE; \
    } \
\
    if (offset) { \
        local_offset = *offset; \
    } else if (!buffer) { \
        return TSS2_MU_RC_BAD_REFERENCE; \
    } \
\
    LOG_DEBUG(\
         "Marshalling " #type " from 0x%" PRIxPTR " to buffer 0x%" PRIxPTR \
         " at index 0x%zx", (uintptr_t)&src,  (uintptr_t)buffer, offset?*offset:0xffff); \
\
    ret = fn1(op1 src->m1, buffer, buffer_size, &local_offset); \
    if (ret != TSS2_RC_SUCCESS) \
        return ret; \
\
    ret = fn2(op2 src->m2, buffer, buffer_size, &local_offset); \
    if (ret != TSS2_RC_SUCCESS) \
        return ret; \
\
    ret = fn3(op3 src->m3, buffer, buffer_size, &local_offset); \
    if (ret != TSS2_RC_SUCCESS) \
        return ret; \
\
    ret = fn4(op4 src->m4, buffer, buffer_size, &local_offset); \
    if (ret != TSS2_RC_SUCCESS) \
        return ret; \
\
    ret = fn5(op5 src->m5, buffer, buffer_size, &local_offset); \
    if (ret != TSS2_RC_SUCCESS) \
        return ret; \
\
    ret = fn6(op6 src->m6, buffer, buffer_size, &local_offset); \
    if (ret != TSS2_RC_SUCCESS) \
        return ret; \
\
    ret = fn7(op7 src->m7, src->m2, buffer, buffer_size, &local_offset); \
\
    if (offset && ret == TSS2_RC_SUCCESS) { \
        *offset = local_offset; \
    } \
    return ret; \
}

#define TPMS_UNMARSHAL_7_U(type, m1, fn1, m2, fn2, m3, fn3, m4, fn4, m5, fn5, m6, fn6, m7, fn7) \
TSS2_RC Tss2_MU_##type##_Unmarshal(uint8_t const buffer[], size_t buffer_size, \
                                   size_t *offset, type *dest) \
{ \
    TSS2_RC ret = TSS2_RC_SUCCESS; \
    size_t local_offset = 0; \
\
    LOG_DEBUG(\
         "Unmarshaling " #type " from 0x%" PRIxPTR " to buffer 0x%" PRIxPTR \
         " at index 0x%zx", (uintptr_t)dest,  (uintptr_t)buffer, offset?*offset:0xffff); \
\
    if (offset) { \
        local_offset = *offset; \
    } else if (!dest) { \
        return TSS2_MU_RC_BAD_REFERENCE; \
    } \
\
    if (dest) \
        memset(dest, 0, sizeof(*dest)); \
\
    ret = fn1(buffer, buffer_size, &local_offset, dest ? &dest->m1 : NULL); \
    if (ret != TSS2_RC_SUCCESS) \
        return ret; \
\
    ret = fn2(buffer, buffer_size, &local_offset, dest ? &dest->m2 : NULL); \
    if (ret != TSS2_RC_SUCCESS) \
        return ret; \
\
    ret = fn3(buffer, buffer_size, &local_offset, dest ? &dest->m3 : NULL); \
    if (ret != TSS2_RC_SUCCESS) \
        return ret; \
\
    ret = fn4(buffer, buffer_size, &local_offset, dest ? &dest->m4 : NULL); \
    if (ret != TSS2_RC_SUCCESS) \
        return ret; \
\
    ret = fn5(buffer, buffer_size, &local_offset, dest ? &dest->m5 : NULL); \
    if (ret != TSS2_RC_SUCCESS) \
        return ret; \
\
    ret = fn6(buffer, buffer_size, &local_offset, dest ? &dest->m6 : NULL); \
    if (ret != TSS2_RC_SUCCESS) \
        return ret; \
\
    ret = fn7(buffer, buffer_size, &local_offset, dest ? dest->m2 : 0, dest ? &dest->m7 : NULL); \
\
    if (offset && ret == TSS2_RC_SUCCESS) { \
        *offset = local_offset; \
    } \
    return ret; \
}

#define TPMS_MARSHAL_11(type, m1, op1, fn1, m2, op2, fn2, m3, op3, fn3, \
                       m4, op4, fn4, m5, op5, fn5, m6, op6, fn6, m7, op7, fn7, \
                       m8, op8, fn8, m9, op9, fn9, m10, op10, fn10, m11, op11, fn11) \
TSS2_RC Tss2_MU_##type##_Marshal(type const *src, uint8_t buffer[], \
                                 size_t buffer_size, size_t *offset) \
{ \
    TSS2_RC ret = TSS2_RC_SUCCESS; \
    size_t local_offset = 0; \
\
    if (!src) { \
        LOG_WARNING("src param is NULL"); \
        return TSS2_MU_RC_BAD_REFERENCE; \
    } \
\
    if (offset) { \
        local_offset = *offset; \
    } else if (!buffer) { \
        return TSS2_MU_RC_BAD_REFERENCE; \
    } \
\
    LOG_DEBUG(\
         "Marshalling " #type " from 0x%" PRIxPTR " to buffer 0x%" PRIxPTR \
         " at index 0x%zx", (uintptr_t)&src,  (uintptr_t)buffer, offset?*offset:0xffff); \
\
    ret = fn1(op1 src->m1, buffer, buffer_size, &local_offset); \
    if (ret != TSS2_RC_SUCCESS) \
        return ret; \
\
    ret = fn2(op2 src->m2, buffer, buffer_size, &local_offset); \
    if (ret != TSS2_RC_SUCCESS) \
        return ret; \
\
    ret = fn3(op3 src->m3, buffer, buffer_size, &local_offset); \
    if (ret != TSS2_RC_SUCCESS) \
        return ret; \
\
    ret = fn4(op4 src->m4, buffer, buffer_size, &local_offset); \
    if (ret != TSS2_RC_SUCCESS) \
        return ret; \
\
    ret = fn5(op5 src->m5, buffer, buffer_size, &local_offset); \
    if (ret != TSS2_RC_SUCCESS) \
        return ret; \
\
    ret = fn6(op6 src->m6, buffer, buffer_size, &local_offset); \
    if (ret != TSS2_RC_SUCCESS) \
        return ret; \
\
    ret = fn7(op7 src->m7, buffer, buffer_size, &local_offset); \
    if (ret != TSS2_RC_SUCCESS) \
        return ret; \
\
    ret = fn8(op8 src->m8, buffer, buffer_size, &local_offset); \
    if (ret != TSS2_RC_SUCCESS) \
        return ret; \
\
    ret = fn9(op9 src->m9, buffer, buffer_size, &local_offset); \
    if (ret != TSS2_RC_SUCCESS) \
        return ret; \
\
    ret = fn10(op10 src->m10, buffer, buffer_size, &local_offset); \
    if (ret != TSS2_RC_SUCCESS) \
        return ret; \
\
    ret = fn11(op11 src->m11, buffer, buffer_size, &local_offset); \
\
    if (offset && ret == TSS2_RC_SUCCESS) { \
        *offset = local_offset; \
    } \
    return ret; \
}

#define TPMS_UNMARSHAL_11(type, m1, fn1, m2, fn2, m3, fn3, m4, fn4, m5, fn5, m6, fn6, m7, fn7, \
                          m8, fn8, m9, fn9, m10, fn10, m11, fn11) \
TSS2_RC Tss2_MU_##type##_Unmarshal(uint8_t const buffer[], size_t buffer_size, \
                                   size_t *offset, type *dest) \
{ \
    TSS2_RC ret = TSS2_RC_SUCCESS; \
    size_t local_offset = 0; \
\
    LOG_DEBUG(\
         "Unmarshaling " #type " from 0x%" PRIxPTR " to buffer 0x%" PRIxPTR \
         " at index 0x%zx", (uintptr_t)dest,  (uintptr_t)buffer, offset?*offset:0xffff); \
\
    if (offset) { \
        local_offset = *offset; \
    } else if (!dest) { \
        return TSS2_MU_RC_BAD_REFERENCE; \
    } \
\
    if (dest) \
        memset(dest, 0, sizeof(*dest)); \
\
    ret = fn1(buffer, buffer_size, &local_offset, dest ? &dest->m1 : NULL); \
    if (ret != TSS2_RC_SUCCESS) \
        return ret; \
\
    ret = fn2(buffer, buffer_size, &local_offset, dest ? &dest->m2 : NULL); \
    if (ret != TSS2_RC_SUCCESS) \
        return ret; \
\
    ret = fn3(buffer, buffer_size, &local_offset, dest ? &dest->m3 : NULL); \
    if (ret != TSS2_RC_SUCCESS) \
        return ret; \
\
    ret = fn4(buffer, buffer_size, &local_offset, dest ? &dest->m4 : NULL); \
    if (ret != TSS2_RC_SUCCESS) \
        return ret; \
\
    ret = fn5(buffer, buffer_size, &local_offset, dest ? &dest->m5 : NULL); \
    if (ret != TSS2_RC_SUCCESS) \
        return ret; \
\
    ret = fn6(buffer, buffer_size, &local_offset, dest ? &dest->m6 : NULL); \
    if (ret != TSS2_RC_SUCCESS) \
        return ret; \
\
    ret = fn7(buffer, buffer_size, &local_offset, dest ? &dest->m7 : NULL); \
    if (ret != TSS2_RC_SUCCESS) \
        return ret; \
\
    ret = fn8(buffer, buffer_size, &local_offset, dest ? &dest->m8 : NULL); \
    if (ret != TSS2_RC_SUCCESS) \
        return ret; \
\
    ret = fn9(buffer, buffer_size, &local_offset, dest ? &dest->m9 : NULL); \
    if (ret != TSS2_RC_SUCCESS) \
        return ret; \
\
    ret = fn10(buffer, buffer_size, &local_offset, dest ? &dest->m10 : NULL); \
    if (ret != TSS2_RC_SUCCESS) \
        return ret; \
\
    ret = fn11(buffer, buffer_size, &local_offset, dest ? &dest->m11 : NULL); \
\
    if (offset && ret == TSS2_RC_SUCCESS) { \
        *offset = local_offset; \
    } \
    return ret; \
}

/*
 * These macros expand to (un)marshal functions for each of the TPMS types
 * the specification part 2.
 */
TPMS_MARSHAL_2(TPMS_ALG_PROPERTY,
               alg, VAL, Tss2_MU_UINT16_Marshal,
               algProperties, VAL, Tss2_MU_TPMA_ALGORITHM_Marshal)

TPMS_UNMARSHAL_2(TPMS_ALG_PROPERTY,
                 alg, Tss2_MU_UINT16_Unmarshal,
                 algProperties, Tss2_MU_TPMA_ALGORITHM_Unmarshal)

TPMS_MARSHAL_2(TPMS_TAGGED_PROPERTY,
               property, VAL, Tss2_MU_UINT32_Marshal,
               value, VAL, Tss2_MU_UINT32_Marshal)

TPMS_UNMARSHAL_2(TPMS_TAGGED_PROPERTY,
                 property, Tss2_MU_UINT32_Unmarshal,
                 value, Tss2_MU_UINT32_Unmarshal)

TPMS_MARSHAL_2(TPMS_TAGGED_POLICY,
               handle, VAL, Tss2_MU_UINT32_Marshal,
               policyHash, ADDR, Tss2_MU_TPMT_HA_Marshal)

TPMS_UNMARSHAL_2(TPMS_TAGGED_POLICY,
                 handle, Tss2_MU_UINT32_Unmarshal,
                 policyHash, Tss2_MU_TPMT_HA_Unmarshal)

TPMS_MARSHAL_4(TPMS_CLOCK_INFO,
               clock, VAL, Tss2_MU_UINT64_Marshal,
               resetCount, VAL, Tss2_MU_UINT32_Marshal,
               restartCount, VAL, Tss2_MU_UINT32_Marshal,
               safe, VAL, Tss2_MU_UINT8_Marshal)

TPMS_UNMARSHAL_4(TPMS_CLOCK_INFO,
                 clock, Tss2_MU_UINT64_Unmarshal,
                 resetCount, Tss2_MU_UINT32_Unmarshal,
                 restartCount, Tss2_MU_UINT32_Unmarshal,
                 safe, Tss2_MU_UINT8_Unmarshal)

TPMS_MARSHAL_2(TPMS_TIME_INFO,
               time, VAL, Tss2_MU_UINT64_Marshal,
               clockInfo, ADDR, Tss2_MU_TPMS_CLOCK_INFO_Marshal)

TPMS_UNMARSHAL_2(TPMS_TIME_INFO,
                 time, Tss2_MU_UINT64_Unmarshal,
                 clockInfo, Tss2_MU_TPMS_CLOCK_INFO_Unmarshal)

TPMS_MARSHAL_2(TPMS_TIME_ATTEST_INFO,
               time, ADDR, Tss2_MU_TPMS_TIME_INFO_Marshal,
               firmwareVersion, VAL, Tss2_MU_UINT64_Marshal)

TPMS_UNMARSHAL_2(TPMS_TIME_ATTEST_INFO,
                 time, Tss2_MU_TPMS_TIME_INFO_Unmarshal,
                 firmwareVersion, Tss2_MU_UINT64_Unmarshal)

TPMS_MARSHAL_2(TPMS_CERTIFY_INFO,
               name, ADDR, Tss2_MU_TPM2B_NAME_Marshal,
               qualifiedName, ADDR, Tss2_MU_TPM2B_NAME_Marshal)

TPMS_UNMARSHAL_2(TPMS_CERTIFY_INFO,
                 name, Tss2_MU_TPM2B_NAME_Unmarshal,
                 qualifiedName, Tss2_MU_TPM2B_NAME_Unmarshal)

TPMS_MARSHAL_4(TPMS_COMMAND_AUDIT_INFO,
               auditCounter, VAL, Tss2_MU_UINT64_Marshal,
               digestAlg, VAL, Tss2_MU_UINT16_Marshal,
               auditDigest, ADDR, Tss2_MU_TPM2B_DIGEST_Marshal,
               commandDigest, ADDR, Tss2_MU_TPM2B_DIGEST_Marshal)

TPMS_UNMARSHAL_4(TPMS_COMMAND_AUDIT_INFO,
                 auditCounter, Tss2_MU_UINT64_Unmarshal,
                 digestAlg, Tss2_MU_UINT16_Unmarshal,
                 auditDigest, Tss2_MU_TPM2B_DIGEST_Unmarshal,
                 commandDigest, Tss2_MU_TPM2B_DIGEST_Unmarshal)

TPMS_MARSHAL_2(TPMS_SESSION_AUDIT_INFO,
               exclusiveSession, VAL, Tss2_MU_UINT8_Marshal,
               sessionDigest, ADDR, Tss2_MU_TPM2B_DIGEST_Marshal)

TPMS_UNMARSHAL_2(TPMS_SESSION_AUDIT_INFO,
                 exclusiveSession, Tss2_MU_UINT8_Unmarshal,
                 sessionDigest, Tss2_MU_TPM2B_DIGEST_Unmarshal)

TPMS_MARSHAL_2(TPMS_CREATION_INFO,
               objectName, ADDR, Tss2_MU_TPM2B_NAME_Marshal,
               creationHash, ADDR, Tss2_MU_TPM2B_DIGEST_Marshal)

TPMS_UNMARSHAL_2(TPMS_CREATION_INFO,
                 objectName, Tss2_MU_TPM2B_NAME_Unmarshal,
                 creationHash, Tss2_MU_TPM2B_DIGEST_Unmarshal)

TPMS_MARSHAL_3(TPMS_NV_CERTIFY_INFO,
               indexName, ADDR, Tss2_MU_TPM2B_NAME_Marshal,
               offset, VAL, Tss2_MU_UINT16_Marshal,
               nvContents, ADDR, Tss2_MU_TPM2B_MAX_NV_BUFFER_Marshal)

TPMS_UNMARSHAL_3(TPMS_NV_CERTIFY_INFO,
                 indexName, Tss2_MU_TPM2B_NAME_Unmarshal,
                 offset, Tss2_MU_UINT16_Unmarshal,
                 nvContents, Tss2_MU_TPM2B_MAX_NV_BUFFER_Unmarshal)

TPMS_MARSHAL_4(TPMS_AUTH_COMMAND,
               sessionHandle, VAL, Tss2_MU_UINT32_Marshal,
               nonce, ADDR, Tss2_MU_TPM2B_DIGEST_Marshal,
               sessionAttributes, VAL, Tss2_MU_TPMA_SESSION_Marshal,
               hmac, ADDR, Tss2_MU_TPM2B_DIGEST_Marshal)

TPMS_UNMARSHAL_4(TPMS_AUTH_COMMAND,
                 sessionHandle, Tss2_MU_UINT32_Unmarshal,
                 nonce, Tss2_MU_TPM2B_DIGEST_Unmarshal,
                 sessionAttributes, Tss2_MU_TPMA_SESSION_Unmarshal,
                 hmac, Tss2_MU_TPM2B_DIGEST_Unmarshal)

TPMS_MARSHAL_3(TPMS_AUTH_RESPONSE,
               nonce, ADDR, Tss2_MU_TPM2B_DIGEST_Marshal,
               sessionAttributes, VAL, Tss2_MU_TPMA_SESSION_Marshal,
               hmac, ADDR, Tss2_MU_TPM2B_DIGEST_Marshal)

TPMS_UNMARSHAL_3(TPMS_AUTH_RESPONSE,
                 nonce, Tss2_MU_TPM2B_DIGEST_Unmarshal,
                 sessionAttributes, Tss2_MU_TPMA_SESSION_Unmarshal,
                 hmac, Tss2_MU_TPM2B_DIGEST_Unmarshal)

TPMS_MARSHAL_2(TPMS_SENSITIVE_CREATE,
               userAuth, ADDR, Tss2_MU_TPM2B_DIGEST_Marshal,
               data, ADDR, Tss2_MU_TPM2B_SENSITIVE_DATA_Marshal)

TPMS_UNMARSHAL_2(TPMS_SENSITIVE_CREATE,
                 userAuth, Tss2_MU_TPM2B_DIGEST_Unmarshal,
                 data, Tss2_MU_TPM2B_SENSITIVE_DATA_Unmarshal)

TPMS_MARSHAL_1(TPMS_SCHEME_HASH,
               hashAlg, VAL, Tss2_MU_UINT16_Marshal)

TPMS_UNMARSHAL_1(TPMS_SCHEME_HASH,
                 hashAlg, Tss2_MU_UINT16_Unmarshal)

TPMS_MARSHAL_2(TPMS_SCHEME_ECDAA,
               hashAlg, VAL, Tss2_MU_UINT16_Marshal,
               count, VAL, Tss2_MU_UINT16_Marshal)

TPMS_UNMARSHAL_2(TPMS_SCHEME_ECDAA,
                 hashAlg, Tss2_MU_UINT16_Unmarshal,
                 count, Tss2_MU_UINT16_Unmarshal)

TPMS_MARSHAL_2(TPMS_SCHEME_XOR,
               hashAlg, VAL, Tss2_MU_UINT16_Marshal,
               kdf, VAL, Tss2_MU_UINT16_Marshal)

TPMS_UNMARSHAL_2(TPMS_SCHEME_XOR,
                 hashAlg, Tss2_MU_UINT16_Unmarshal,
                 kdf, Tss2_MU_UINT16_Unmarshal)

TPMS_MARSHAL_2(TPMS_ECC_POINT,
               x, ADDR, Tss2_MU_TPM2B_ECC_PARAMETER_Marshal,
               y, ADDR, Tss2_MU_TPM2B_ECC_PARAMETER_Marshal)

TPMS_UNMARSHAL_2(TPMS_ECC_POINT,
                 x, Tss2_MU_TPM2B_ECC_PARAMETER_Unmarshal,
                 y, Tss2_MU_TPM2B_ECC_PARAMETER_Unmarshal)

TPMS_MARSHAL_2(TPMS_SIGNATURE_RSA,
               hash, VAL, Tss2_MU_UINT16_Marshal,
               sig, ADDR, Tss2_MU_TPM2B_PUBLIC_KEY_RSA_Marshal)

TPMS_UNMARSHAL_2(TPMS_SIGNATURE_RSA,
                 hash, Tss2_MU_UINT16_Unmarshal,
                 sig, Tss2_MU_TPM2B_PUBLIC_KEY_RSA_Unmarshal)

TPMS_MARSHAL_3(TPMS_SIGNATURE_ECC,
               hash, VAL, Tss2_MU_UINT16_Marshal,
               signatureR, ADDR, Tss2_MU_TPM2B_ECC_PARAMETER_Marshal,
               signatureS, ADDR, Tss2_MU_TPM2B_ECC_PARAMETER_Marshal)

TPMS_UNMARSHAL_3(TPMS_SIGNATURE_ECC,
                 hash, Tss2_MU_UINT16_Unmarshal,
                 signatureR, Tss2_MU_TPM2B_ECC_PARAMETER_Unmarshal,
                 signatureS, Tss2_MU_TPM2B_ECC_PARAMETER_Unmarshal)

TPMS_MARSHAL_2(TPMS_NV_PIN_COUNTER_PARAMETERS,
               pinCount, VAL, Tss2_MU_UINT32_Marshal,
               pinLimit, VAL, Tss2_MU_UINT32_Marshal)

TPMS_UNMARSHAL_2(TPMS_NV_PIN_COUNTER_PARAMETERS,
                 pinCount, Tss2_MU_UINT32_Unmarshal,
                 pinLimit, Tss2_MU_UINT32_Unmarshal)

TPMS_MARSHAL_5(TPMS_NV_PUBLIC,
               nvIndex, VAL, Tss2_MU_UINT32_Marshal,
               nameAlg, VAL, Tss2_MU_UINT16_Marshal,
               attributes, VAL, Tss2_MU_TPMA_NV_Marshal,
               authPolicy, ADDR, Tss2_MU_TPM2B_DIGEST_Marshal,
               dataSize, VAL, Tss2_MU_UINT16_Marshal)

TPMS_UNMARSHAL_5(TPMS_NV_PUBLIC,
                 nvIndex, Tss2_MU_UINT32_Unmarshal,
                 nameAlg, Tss2_MU_UINT16_Unmarshal,
                 attributes, Tss2_MU_TPMA_NV_Unmarshal,
                 authPolicy, Tss2_MU_TPM2B_DIGEST_Unmarshal,
                 dataSize, Tss2_MU_UINT16_Unmarshal)

TPMS_MARSHAL_2(TPMS_CONTEXT_DATA,
               integrity, ADDR, Tss2_MU_TPM2B_DIGEST_Marshal,
               encrypted, ADDR, Tss2_MU_TPM2B_CONTEXT_SENSITIVE_Marshal)

TPMS_UNMARSHAL_2(TPMS_CONTEXT_DATA,
                 integrity, Tss2_MU_TPM2B_DIGEST_Unmarshal,
                 encrypted, Tss2_MU_TPM2B_CONTEXT_SENSITIVE_Unmarshal)

TPMS_MARSHAL_4(TPMS_CONTEXT,
               sequence, VAL, Tss2_MU_UINT64_Marshal,
               savedHandle, VAL, Tss2_MU_UINT32_Marshal,
               hierarchy, VAL, Tss2_MU_UINT32_Marshal,
               contextBlob, ADDR, Tss2_MU_TPM2B_CONTEXT_DATA_Marshal)

TPMS_UNMARSHAL_4(TPMS_CONTEXT,
                 sequence, Tss2_MU_UINT64_Unmarshal,
                 savedHandle, Tss2_MU_UINT32_Unmarshal,
                 hierarchy, Tss2_MU_UINT32_Unmarshal,
                 contextBlob, Tss2_MU_TPM2B_CONTEXT_DATA_Unmarshal)

TPMS_MARSHAL_2(TPMS_QUOTE_INFO,
               pcrSelect, ADDR, Tss2_MU_TPML_PCR_SELECTION_Marshal,
               pcrDigest, ADDR, Tss2_MU_TPM2B_DIGEST_Marshal)

TPMS_UNMARSHAL_2(TPMS_QUOTE_INFO,
                 pcrSelect, Tss2_MU_TPML_PCR_SELECTION_Unmarshal,
                 pcrDigest, Tss2_MU_TPM2B_DIGEST_Unmarshal)

TPMS_MARSHAL_7(TPMS_CREATION_DATA,
               pcrSelect, ADDR, Tss2_MU_TPML_PCR_SELECTION_Marshal,
               pcrDigest, ADDR, Tss2_MU_TPM2B_DIGEST_Marshal,
               locality, VAL, Tss2_MU_TPMA_LOCALITY_Marshal,
               parentNameAlg, VAL, Tss2_MU_UINT16_Marshal,
               parentName, ADDR, Tss2_MU_TPM2B_NAME_Marshal,
               parentQualifiedName, ADDR, Tss2_MU_TPM2B_NAME_Marshal,
               outsideInfo, ADDR, Tss2_MU_TPM2B_DATA_Marshal)

TPMS_UNMARSHAL_7(TPMS_CREATION_DATA,
                 pcrSelect, Tss2_MU_TPML_PCR_SELECTION_Unmarshal,
                 pcrDigest, Tss2_MU_TPM2B_DIGEST_Unmarshal,
                 locality, Tss2_MU_TPMA_LOCALITY_Unmarshal,
                 parentNameAlg, Tss2_MU_UINT16_Unmarshal,
                 parentName, Tss2_MU_TPM2B_NAME_Unmarshal,
                 parentQualifiedName, Tss2_MU_TPM2B_NAME_Unmarshal,
                 outsideInfo, Tss2_MU_TPM2B_DATA_Unmarshal)

TPMS_MARSHAL_4(TPMS_ECC_PARMS,
               symmetric, ADDR, Tss2_MU_TPMT_SYM_DEF_OBJECT_Marshal,
               scheme, ADDR, Tss2_MU_TPMT_ECC_SCHEME_Marshal,
               curveID, VAL, Tss2_MU_UINT16_Marshal,
               kdf, ADDR, Tss2_MU_TPMT_KDF_SCHEME_Marshal)

TPMS_UNMARSHAL_4(TPMS_ECC_PARMS,
                 symmetric, Tss2_MU_TPMT_SYM_DEF_OBJECT_Unmarshal,
                 scheme, Tss2_MU_TPMT_ECC_SCHEME_Unmarshal,
                 curveID, Tss2_MU_UINT16_Unmarshal,
                 kdf, Tss2_MU_TPMT_KDF_SCHEME_Unmarshal)

TPMS_MARSHAL_7_U(TPMS_ATTEST,
                 magic, VAL, Tss2_MU_UINT32_Marshal,
                 type, VAL, Tss2_MU_TPM2_ST_Marshal,
                 qualifiedSigner, ADDR, Tss2_MU_TPM2B_NAME_Marshal,
                 extraData, ADDR, Tss2_MU_TPM2B_DATA_Marshal,
                 clockInfo, ADDR, Tss2_MU_TPMS_CLOCK_INFO_Marshal,
                 firmwareVersion, VAL, Tss2_MU_UINT64_Marshal,
                 attested, ADDR, Tss2_MU_TPMU_ATTEST_Marshal)

TPMS_UNMARSHAL_7_U(TPMS_ATTEST,
                   magic, Tss2_MU_UINT32_Unmarshal,
                   type, Tss2_MU_TPM2_ST_Unmarshal,
                   qualifiedSigner, Tss2_MU_TPM2B_NAME_Unmarshal,
                   extraData, Tss2_MU_TPM2B_DATA_Unmarshal,
                   clockInfo, Tss2_MU_TPMS_CLOCK_INFO_Unmarshal,
                   firmwareVersion, Tss2_MU_UINT64_Unmarshal,
                   attested, Tss2_MU_TPMU_ATTEST_Unmarshal)

TPMS_MARSHAL_11(TPMS_ALGORITHM_DETAIL_ECC,
                curveID, VAL, Tss2_MU_UINT16_Marshal,
                keySize, VAL, Tss2_MU_UINT16_Marshal,
                kdf, ADDR, Tss2_MU_TPMT_KDF_SCHEME_Marshal,
                sign, ADDR, Tss2_MU_TPMT_ECC_SCHEME_Marshal,
                p, ADDR, Tss2_MU_TPM2B_ECC_PARAMETER_Marshal,
                a, ADDR, Tss2_MU_TPM2B_ECC_PARAMETER_Marshal,
                b, ADDR, Tss2_MU_TPM2B_ECC_PARAMETER_Marshal,
                gX, ADDR, Tss2_MU_TPM2B_ECC_PARAMETER_Marshal,
                gY, ADDR, Tss2_MU_TPM2B_ECC_PARAMETER_Marshal,
                n, ADDR, Tss2_MU_TPM2B_ECC_PARAMETER_Marshal,
                h, ADDR, Tss2_MU_TPM2B_ECC_PARAMETER_Marshal)

TPMS_UNMARSHAL_11(TPMS_ALGORITHM_DETAIL_ECC,
                  curveID, Tss2_MU_UINT16_Unmarshal,
                  keySize, Tss2_MU_UINT16_Unmarshal,
                  kdf, Tss2_MU_TPMT_KDF_SCHEME_Unmarshal,
                  sign, Tss2_MU_TPMT_ECC_SCHEME_Unmarshal,
                  p, Tss2_MU_TPM2B_ECC_PARAMETER_Unmarshal,
                  a, Tss2_MU_TPM2B_ECC_PARAMETER_Unmarshal,
                  b, Tss2_MU_TPM2B_ECC_PARAMETER_Unmarshal,
                  gX, Tss2_MU_TPM2B_ECC_PARAMETER_Unmarshal,
                  gY, Tss2_MU_TPM2B_ECC_PARAMETER_Unmarshal,
                  n, Tss2_MU_TPM2B_ECC_PARAMETER_Unmarshal,
                  h, Tss2_MU_TPM2B_ECC_PARAMETER_Unmarshal)

TPMS_MARSHAL_2_U(TPMS_CAPABILITY_DATA,
                 capability, VAL, Tss2_MU_UINT32_Marshal,
                 data, ADDR, Tss2_MU_TPMU_CAPABILITIES_Marshal)

TPMS_UNMARSHAL_2_U(TPMS_CAPABILITY_DATA,
                   capability, Tss2_MU_UINT32_Unmarshal,
                   data, Tss2_MU_TPMU_CAPABILITIES_Unmarshal)

TPMS_MARSHAL_1(TPMS_KEYEDHASH_PARMS,
               scheme, ADDR, Tss2_MU_TPMT_KEYEDHASH_SCHEME_Marshal)

TPMS_UNMARSHAL_1(TPMS_KEYEDHASH_PARMS,
                 scheme, Tss2_MU_TPMT_KEYEDHASH_SCHEME_Unmarshal)

TPMS_MARSHAL_4(TPMS_RSA_PARMS,
               symmetric, ADDR, Tss2_MU_TPMT_SYM_DEF_OBJECT_Marshal,
               scheme, ADDR, Tss2_MU_TPMT_RSA_SCHEME_Marshal,
               keyBits, VAL, Tss2_MU_UINT16_Marshal,
               exponent, VAL, Tss2_MU_UINT32_Marshal)

TPMS_UNMARSHAL_4(TPMS_RSA_PARMS,
                 symmetric, Tss2_MU_TPMT_SYM_DEF_OBJECT_Unmarshal,
                 scheme, Tss2_MU_TPMT_RSA_SCHEME_Unmarshal,
                 keyBits, Tss2_MU_UINT16_Unmarshal,
                 exponent, Tss2_MU_UINT32_Unmarshal)

TPMS_MARSHAL_1(TPMS_SYMCIPHER_PARMS,
               sym, ADDR, Tss2_MU_TPMT_SYM_DEF_OBJECT_Marshal)

TPMS_UNMARSHAL_1(TPMS_SYMCIPHER_PARMS,
                 sym, Tss2_MU_TPMT_SYM_DEF_OBJECT_Unmarshal)

TPMS_MARSHAL_0(TPMS_EMPTY);

TPMS_UNMARSHAL_0(TPMS_EMPTY);

TPMS_MARSHAL_2(TPMS_AC_OUTPUT,
               tag, VAL, Tss2_MU_UINT32_Marshal,
               data, VAL, Tss2_MU_UINT32_Marshal)

TPMS_UNMARSHAL_2(TPMS_AC_OUTPUT,
                 tag, Tss2_MU_UINT32_Unmarshal,
                 data, Tss2_MU_UINT32_Unmarshal)

TPMS_MARSHAL_2(TPMS_ID_OBJECT,
               integrityHMAC, ADDR, Tss2_MU_TPM2B_DIGEST_Marshal,
               encIdentity, ADDR, Tss2_MU_TPM2B_DIGEST_Marshal)

TPMS_UNMARSHAL_2(TPMS_ID_OBJECT,
                 integrityHMAC, Tss2_MU_TPM2B_DIGEST_Unmarshal,
                 encIdentity, Tss2_MU_TPM2B_DIGEST_Unmarshal)

TPMS_MARSHAL_2(TPMS_NV_DIGEST_CERTIFY_INFO,
               indexName, ADDR, Tss2_MU_TPM2B_NAME_Marshal,
               nvDigest, ADDR, Tss2_MU_TPM2B_DIGEST_Marshal)

TPMS_UNMARSHAL_2(TPMS_NV_DIGEST_CERTIFY_INFO,
                 indexName, Tss2_MU_TPM2B_NAME_Unmarshal,
                 nvDigest, Tss2_MU_TPM2B_DIGEST_Unmarshal)

TPMS_MARSHAL_3(TPMS_ACT_DATA,
               handle, VAL, Tss2_MU_TPM2_HANDLE_Marshal,
               timeout, VAL, Tss2_MU_UINT32_Marshal,
               attributes, VAL, Tss2_MU_UINT32_Marshal)

TPMS_UNMARSHAL_3(TPMS_ACT_DATA,
                 handle, Tss2_MU_TPM2_HANDLE_Unmarshal,
                 timeout, Tss2_MU_UINT32_Unmarshal,
                 attributes, Tss2_MU_UINT32_Unmarshal)
