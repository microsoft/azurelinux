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

#define TPMT_MARSHAL_2(type, m1, op1, fn1, m2, op2, sel, fn2) \
TSS2_RC Tss2_MU_##type##_Marshal(type const *src, uint8_t buffer[], \
                                 size_t buffer_size, size_t *offset) \
{ \
    TSS2_RC ret = TSS2_RC_SUCCESS; \
    size_t local_offset = 0; \
\
    if (!src) \
        return TSS2_SYS_RC_BAD_REFERENCE; \
\
    if (offset) \
        local_offset = *offset; \
    else if (!buffer) \
        return TSS2_MU_RC_BAD_REFERENCE; \
\
    LOG_DEBUG(\
         "Marshalling " #type " from 0x%" PRIxPTR " to buffer 0x%" PRIxPTR \
         " at index 0x%zx", (uintptr_t)src,  (uintptr_t)buffer, local_offset); \
\
    ret = fn1(op1 src->m1, buffer, buffer_size, &local_offset); \
    if (ret != TSS2_RC_SUCCESS) \
        return ret; \
\
    ret = fn2(op2 src->m2, src->sel, buffer, buffer_size, &local_offset); \
\
    if (offset && ret == TSS2_RC_SUCCESS) { \
        *offset = local_offset; \
    } \
\
    return ret; \
}

#define TPMT_UNMARSHAL_2(type, m1, fn1, m2, sel, fn2) \
TSS2_RC Tss2_MU_##type##_Unmarshal(uint8_t const buffer[], size_t buffer_size, \
                                   size_t *offset, type *dest) \
{ \
    TSS2_RC ret = TSS2_RC_SUCCESS; \
    size_t local_offset = 0; \
    type tmp; \
\
    if (offset) \
        local_offset = *offset; \
    else if (!dest) \
        return TSS2_MU_RC_BAD_REFERENCE; \
\
    LOG_DEBUG(\
         "Unmarshaling " #type " from 0x%" PRIxPTR " to buffer 0x%" PRIxPTR \
         " at index 0x%zx", (uintptr_t)dest,  (uintptr_t)buffer, local_offset); \
\
    memset(&tmp, '\0', sizeof(tmp)); \
\
    ret = fn1(buffer, buffer_size, &local_offset, dest ? &dest->m1 : &tmp.m1); \
    if (ret != TSS2_RC_SUCCESS) \
        return ret; \
\
    ret = fn2(buffer, buffer_size, &local_offset, dest ? dest->sel : tmp.sel, dest ? &dest->m2 : NULL); \
\
    if (offset && ret == TSS2_RC_SUCCESS) { \
        *offset = local_offset; \
    } \
\
    return ret; \
}

#define TPMT_MARSHAL_3(type, m1, op1, fn1, m2, op2, sel2, fn2, m3, op3, sel3, fn3) \
TSS2_RC Tss2_MU_##type##_Marshal(type const *src, uint8_t buffer[], \
                                 size_t buffer_size, size_t *offset) \
{ \
    TSS2_RC ret = TSS2_RC_SUCCESS; \
    size_t local_offset = 0; \
\
    if (!src) \
        return TSS2_SYS_RC_BAD_REFERENCE; \
\
    if (offset) \
        local_offset = *offset; \
    else if (!buffer) \
        return TSS2_MU_RC_BAD_REFERENCE; \
\
    LOG_DEBUG(\
         "Marshalling " #type " from 0x%" PRIxPTR " to buffer 0x%" PRIxPTR \
         " at index 0x%zx", (uintptr_t)src,  (uintptr_t)buffer, local_offset); \
\
    ret = fn1(op1 src->m1, buffer, buffer_size, &local_offset); \
    if (ret != TSS2_RC_SUCCESS) \
        return ret; \
\
    ret = fn2(op2 src->m2, src->sel2, buffer, buffer_size, &local_offset); \
    if (ret != TSS2_RC_SUCCESS) \
        return ret; \
\
    ret = fn3(op3 src->m3, src->sel3, buffer, buffer_size, &local_offset); \
\
    if (offset && ret == TSS2_RC_SUCCESS) { \
        *offset = local_offset; \
    } \
\
    return ret; \
}

#define TPMT_UNMARSHAL_3(type, m1, fn1, m2, sel2, fn2, m3, sel3, fn3) \
TSS2_RC Tss2_MU_##type##_Unmarshal(uint8_t const buffer[], size_t buffer_size, \
                                   size_t *offset, type *dest) \
{ \
    TSS2_RC ret = TSS2_RC_SUCCESS; \
    size_t local_offset = 0; \
    type tmp; \
\
    if (offset) \
        local_offset = *offset; \
    else if (!dest) \
        return TSS2_MU_RC_BAD_REFERENCE; \
\
    memset(&tmp, '\0', sizeof(tmp)); \
\
    LOG_DEBUG(\
         "Unmarshaling " #type " from 0x%" PRIxPTR " to buffer 0x%" PRIxPTR \
         " at index 0x%zx", (uintptr_t)dest,  (uintptr_t)buffer, local_offset); \
\
    ret = fn1(buffer, buffer_size, &local_offset, dest ? &dest->m1 : &tmp.m1); \
    if (ret != TSS2_RC_SUCCESS) \
        return ret; \
\
    ret = fn2(buffer, buffer_size, &local_offset, dest ? dest->sel2 : tmp.sel2, dest ? &dest->m2 : NULL); \
    if (ret != TSS2_RC_SUCCESS) \
        return ret; \
\
    ret = fn3(buffer, buffer_size, &local_offset, dest ? dest->sel3 : tmp.sel3, dest ? &dest->m3 : NULL); \
\
    if (offset && ret == TSS2_RC_SUCCESS) { \
        *offset = local_offset; \
    } \
\
    return ret; \
}

#define TPMT_MARSHAL_TK(type, m1, fn1, m2, fn2, m3, fn3) \
TSS2_RC Tss2_MU_##type##_Marshal(type const *src, uint8_t buffer[], \
                                 size_t buffer_size, size_t *offset) \
{ \
    TSS2_RC ret = TSS2_RC_SUCCESS; \
    size_t local_offset = 0; \
\
    if (!src) \
        return TSS2_SYS_RC_BAD_REFERENCE; \
\
    if (offset) \
        local_offset = *offset; \
    else if (!buffer) \
        return TSS2_MU_RC_BAD_REFERENCE; \
\
    LOG_DEBUG(\
         "Marshalling " #type " from 0x%" PRIxPTR " to buffer 0x%" PRIxPTR \
         " at index 0x%zx", (uintptr_t)src,  (uintptr_t)buffer, local_offset); \
\
    ret = fn1(src->m1, buffer, buffer_size, &local_offset); \
    if (ret != TSS2_RC_SUCCESS) \
        return ret; \
\
    ret = fn2(src->m2, buffer, buffer_size, &local_offset); \
    if (ret != TSS2_RC_SUCCESS) \
        return ret; \
\
    ret = fn3(&src->m3, buffer, buffer_size, &local_offset); \
\
    if (offset && ret == TSS2_RC_SUCCESS) { \
        *offset = local_offset; \
    } \
\
    return ret; \
}

#define TPMT_UNMARSHAL_TK(type, m1, fn1, m2, fn2, m3, fn3) \
TSS2_RC Tss2_MU_##type##_Unmarshal(uint8_t const buffer[], size_t buffer_size, \
                                   size_t *offset, type *dest) \
{ \
    TSS2_RC ret = TSS2_RC_SUCCESS; \
    size_t local_offset = 0; \
\
    if (offset) \
        local_offset = *offset; \
    else if (!dest) \
        return TSS2_MU_RC_BAD_REFERENCE; \
\
    LOG_DEBUG(\
         "Unmarshaling " #type " from 0x%" PRIxPTR " to buffer 0x%" PRIxPTR \
         " at index 0x%zx", (uintptr_t)dest,  (uintptr_t)buffer, local_offset); \
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
\
    return ret; \
}

#define TPMT_MARSHAL_4(type, m1, op1, fn1, m2, op2, fn2, m3, op3, fn3, \
                       m4, sel4, op4, fn4) \
TSS2_RC Tss2_MU_##type##_Marshal(type const *src, uint8_t buffer[], \
                                 size_t buffer_size, size_t *offset) \
{ \
    TSS2_RC ret = TSS2_RC_SUCCESS; \
    size_t local_offset = 0; \
\
    if (!src) \
        return TSS2_SYS_RC_BAD_REFERENCE; \
\
    if (offset) \
        local_offset = *offset; \
    else if (!buffer) \
        return TSS2_MU_RC_BAD_REFERENCE; \
\
    LOG_DEBUG(\
         "Marshalling " #type " from 0x%" PRIxPTR " to buffer 0x%" PRIxPTR \
         " at index 0x%zx", (uintptr_t)src,  (uintptr_t)buffer, local_offset); \
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
    ret = fn4(op4 src->m4, src->sel4, buffer, buffer_size, &local_offset); \
\
    if (offset && ret == TSS2_RC_SUCCESS) { \
        *offset = local_offset; \
    } \
\
    return ret; \
}

#define TPMT_UNMARSHAL_4(type, m1, fn1, m2, fn2, m3, fn3, m4, sel4, fn4) \
TSS2_RC Tss2_MU_##type##_Unmarshal(uint8_t const buffer[], size_t buffer_size, \
                                   size_t *offset, type *dest) \
{ \
    TSS2_RC ret = TSS2_RC_SUCCESS; \
    size_t local_offset = 0; \
    type tmp; \
\
    if (offset) \
        local_offset = *offset; \
    else if (!dest) \
        return TSS2_MU_RC_BAD_REFERENCE; \
\
    memset(&tmp, '\0', sizeof(tmp)); \
\
    LOG_DEBUG(\
         "Unmarshaling " #type " from 0x%" PRIxPTR " to buffer 0x%" PRIxPTR \
         " at index 0x%zx", (uintptr_t)dest,  (uintptr_t)buffer, local_offset); \
\
    ret = fn1(buffer, buffer_size, &local_offset, dest ? &dest->m1 : &tmp.m1); \
    if (ret != TSS2_RC_SUCCESS) \
        return ret; \
\
    ret = fn2(buffer, buffer_size, &local_offset, dest ? &dest->m2 : &tmp.m2); \
    if (ret != TSS2_RC_SUCCESS) \
        return ret; \
\
    ret = fn3(buffer, buffer_size, &local_offset, dest ? &dest->m3 : &tmp.m3); \
    if (ret != TSS2_RC_SUCCESS) \
        return ret; \
\
    ret = fn4(buffer, buffer_size, &local_offset, dest ? dest->sel4 : tmp.sel4, dest ? &dest->m4 : NULL); \
\
    if (offset && ret == TSS2_RC_SUCCESS) { \
        *offset = local_offset; \
    } \
\
    return ret; \
}

#define TPMT_MARSHAL_5(type, m1, op1, fn1, m2, op2, fn2, m3, op3, fn3, \
                       m4, op4, fn4, m5, op5, fn5) \
TSS2_RC Tss2_MU_##type##_Marshal(type const *src, uint8_t buffer[], \
                                 size_t buffer_size, size_t *offset) \
{ \
    TSS2_RC ret = TSS2_RC_SUCCESS; \
    size_t local_offset = 0; \
\
    if (!src) \
        return TSS2_SYS_RC_BAD_REFERENCE; \
\
    if (offset) \
        local_offset = *offset; \
    else if (!buffer) \
        return TSS2_MU_RC_BAD_REFERENCE; \
\
    LOG_DEBUG(\
         "Marshalling " #type " from 0x%" PRIxPTR " to buffer 0x%" PRIxPTR \
         " at index 0x%zx", (uintptr_t)src,  (uintptr_t)buffer, local_offset); \
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
\
    return ret; \
}

#define TPMT_UNMARSHAL_5(type, m1, fn1, m2, fn2, m3, fn3, m4, fn4, m5, fn5) \
TSS2_RC Tss2_MU_##type##_Unmarshal(uint8_t const buffer[], size_t buffer_size, \
                                   size_t *offset, type *dest) \
{ \
    TSS2_RC ret = TSS2_RC_SUCCESS; \
    size_t local_offset = 0; \
\
    if (offset) \
        local_offset = *offset; \
    else if (!dest) \
        return TSS2_MU_RC_BAD_REFERENCE; \
\
    LOG_DEBUG(\
         "Unmarshaling " #type " from 0x%" PRIxPTR " to buffer 0x%" PRIxPTR \
         " at index 0x%zx", (uintptr_t)dest,  (uintptr_t)buffer, local_offset); \
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
\
    return ret; \
}

#define TPMT_MARSHAL_6(type, m1, op1, fn1, m2, op2, fn2, m3, op3, fn3, \
                       m4, op4, fn4, m5, op5, sel5, fn5, m6, op6, sel6, fn6) \
TSS2_RC Tss2_MU_##type##_Marshal(type const *src, uint8_t buffer[], \
                                 size_t buffer_size, size_t *offset) \
{ \
    TSS2_RC ret = TSS2_RC_SUCCESS; \
    size_t local_offset = 0; \
\
    if (!src) \
        return TSS2_SYS_RC_BAD_REFERENCE; \
\
    if (offset) \
        local_offset = *offset; \
    else if (!buffer) \
        return TSS2_MU_RC_BAD_REFERENCE; \
\
    LOG_DEBUG(\
         "Marshalling " #type " from 0x%" PRIxPTR " to buffer 0x%" PRIxPTR \
         " at index 0x%zx", (uintptr_t)src,  (uintptr_t)buffer, local_offset); \
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
    ret = fn5(op5 src->m5, src->sel5, buffer, buffer_size, &local_offset); \
    if (ret != TSS2_RC_SUCCESS) \
        return ret; \
\
    ret = fn6(op6 src->m6, src->sel6, buffer, buffer_size, &local_offset); \
\
    if (offset && ret == TSS2_RC_SUCCESS) { \
        *offset = local_offset; \
    } \
\
    return ret; \
}

#define TPMT_UNMARSHAL_6(type, m1, fn1, m2, fn2, m3, fn3, m4, fn4, m5, sel5, fn5, m6, sel6, fn6) \
TSS2_RC Tss2_MU_##type##_Unmarshal(uint8_t const buffer[], size_t buffer_size, \
                                   size_t *offset, type *dest) \
{ \
    TSS2_RC ret = TSS2_RC_SUCCESS; \
    size_t local_offset = 0; \
    type tmp; \
\
    if (offset) \
        local_offset = *offset; \
    else if (!dest) \
        return TSS2_MU_RC_BAD_REFERENCE; \
\
    memset(&tmp, '\0', sizeof(tmp)); \
\
    LOG_DEBUG(\
         "Unmarshaling " #type " from 0x%" PRIxPTR " to buffer 0x%" PRIxPTR \
         " at index 0x%zx", (uintptr_t)dest,  (uintptr_t)buffer, local_offset); \
\
    ret = fn1(buffer, buffer_size, &local_offset, dest ? &dest->m1 : &tmp.m1); \
    if (ret != TSS2_RC_SUCCESS) \
        return ret; \
\
    ret = fn2(buffer, buffer_size, &local_offset, dest ? &dest->m2 : &tmp.m2); \
    if (ret != TSS2_RC_SUCCESS) \
        return ret; \
\
    ret = fn3(buffer, buffer_size, &local_offset, dest ? &dest->m3 : &tmp.m3); \
    if (ret != TSS2_RC_SUCCESS) \
        return ret; \
\
    ret = fn4(buffer, buffer_size, &local_offset, dest ? &dest->m4 : &tmp.m4); \
    if (ret != TSS2_RC_SUCCESS) \
        return ret; \
\
    ret = fn5(buffer, buffer_size, &local_offset, dest ? dest->sel5 : tmp.sel5, dest ? &dest->m5 : NULL); \
    if (ret != TSS2_RC_SUCCESS) \
        return ret; \
\
    ret = fn6(buffer, buffer_size, &local_offset, dest ? dest->sel6 : tmp.sel6, dest ? &dest->m6 : NULL); \
\
    if (offset && ret == TSS2_RC_SUCCESS) { \
        *offset = local_offset; \
    } \
\
    return ret; \
}

/*
 * These macros expand to (un)marshal functions for each of the TPMT types
 * the specification part 2.
 */
TPMT_MARSHAL_2(TPMT_HA, hashAlg, VAL, Tss2_MU_UINT16_Marshal,
               digest, ADDR, hashAlg, Tss2_MU_TPMU_HA_Marshal)

TPMT_UNMARSHAL_2(TPMT_HA, hashAlg, Tss2_MU_UINT16_Unmarshal,
                 digest, hashAlg, Tss2_MU_TPMU_HA_Unmarshal)

TPMT_MARSHAL_3(TPMT_SYM_DEF, algorithm, VAL, Tss2_MU_UINT16_Marshal,
               keyBits, ADDR, algorithm, Tss2_MU_TPMU_SYM_KEY_BITS_Marshal,
               mode, ADDR, algorithm, Tss2_MU_TPMU_SYM_MODE_Marshal)

TPMT_UNMARSHAL_3(TPMT_SYM_DEF, algorithm, Tss2_MU_UINT16_Unmarshal,
                 keyBits, algorithm, Tss2_MU_TPMU_SYM_KEY_BITS_Unmarshal,
                 mode, algorithm, Tss2_MU_TPMU_SYM_MODE_Unmarshal)

TPMT_MARSHAL_3(TPMT_SYM_DEF_OBJECT, algorithm, VAL, Tss2_MU_UINT16_Marshal,
               keyBits, ADDR, algorithm, Tss2_MU_TPMU_SYM_KEY_BITS_Marshal,
               mode, ADDR, algorithm, Tss2_MU_TPMU_SYM_MODE_Marshal)

TPMT_UNMARSHAL_3(TPMT_SYM_DEF_OBJECT, algorithm, Tss2_MU_UINT16_Unmarshal,
                 keyBits, algorithm, Tss2_MU_TPMU_SYM_KEY_BITS_Unmarshal,
                 mode, algorithm, Tss2_MU_TPMU_SYM_MODE_Unmarshal)

TPMT_MARSHAL_2(TPMT_KEYEDHASH_SCHEME, scheme, VAL, Tss2_MU_UINT16_Marshal,
               details, ADDR, scheme, Tss2_MU_TPMU_SCHEME_KEYEDHASH_Marshal)

TPMT_UNMARSHAL_2(TPMT_KEYEDHASH_SCHEME, scheme, Tss2_MU_UINT16_Unmarshal,
                 details, scheme, Tss2_MU_TPMU_SCHEME_KEYEDHASH_Unmarshal)

TPMT_MARSHAL_2(TPMT_SIG_SCHEME, scheme, VAL, Tss2_MU_UINT16_Marshal,
               details, ADDR, scheme, Tss2_MU_TPMU_SIG_SCHEME_Marshal)

TPMT_UNMARSHAL_2(TPMT_SIG_SCHEME, scheme, Tss2_MU_UINT16_Unmarshal,
                 details, scheme, Tss2_MU_TPMU_SIG_SCHEME_Unmarshal)

TPMT_MARSHAL_2(TPMT_KDF_SCHEME, scheme, VAL, Tss2_MU_UINT16_Marshal,
               details, ADDR, scheme, Tss2_MU_TPMU_KDF_SCHEME_Marshal)

TPMT_UNMARSHAL_2(TPMT_KDF_SCHEME, scheme, Tss2_MU_UINT16_Unmarshal,
                 details, scheme, Tss2_MU_TPMU_KDF_SCHEME_Unmarshal)

TPMT_MARSHAL_2(TPMT_ASYM_SCHEME, scheme, VAL, Tss2_MU_UINT16_Marshal,
               details, ADDR, scheme, Tss2_MU_TPMU_ASYM_SCHEME_Marshal)

TPMT_UNMARSHAL_2(TPMT_ASYM_SCHEME, scheme, Tss2_MU_UINT16_Unmarshal,
                 details, scheme, Tss2_MU_TPMU_ASYM_SCHEME_Unmarshal)

TPMT_MARSHAL_2(TPMT_RSA_SCHEME, scheme, VAL, Tss2_MU_UINT16_Marshal,
               details, ADDR, scheme, Tss2_MU_TPMU_ASYM_SCHEME_Marshal)

TPMT_UNMARSHAL_2(TPMT_RSA_SCHEME, scheme, Tss2_MU_UINT16_Unmarshal,
                 details, scheme, Tss2_MU_TPMU_ASYM_SCHEME_Unmarshal)

TPMT_MARSHAL_2(TPMT_RSA_DECRYPT, scheme, VAL, Tss2_MU_UINT16_Marshal,
               details, ADDR, scheme, Tss2_MU_TPMU_ASYM_SCHEME_Marshal)

TPMT_UNMARSHAL_2(TPMT_RSA_DECRYPT, scheme, Tss2_MU_UINT16_Unmarshal,
                 details, scheme, Tss2_MU_TPMU_ASYM_SCHEME_Unmarshal)

TPMT_MARSHAL_2(TPMT_ECC_SCHEME, scheme, VAL, Tss2_MU_UINT16_Marshal,
               details, ADDR, scheme, Tss2_MU_TPMU_ASYM_SCHEME_Marshal)

TPMT_UNMARSHAL_2(TPMT_ECC_SCHEME, scheme, Tss2_MU_UINT16_Unmarshal,
                 details, scheme, Tss2_MU_TPMU_ASYM_SCHEME_Unmarshal)

TPMT_MARSHAL_2(TPMT_SIGNATURE, sigAlg, VAL, Tss2_MU_UINT16_Marshal,
               signature, ADDR, sigAlg, Tss2_MU_TPMU_SIGNATURE_Marshal)

TPMT_UNMARSHAL_2(TPMT_SIGNATURE, sigAlg, Tss2_MU_UINT16_Unmarshal,
                 signature, sigAlg, Tss2_MU_TPMU_SIGNATURE_Unmarshal)

TPMT_MARSHAL_4(TPMT_SENSITIVE, sensitiveType, VAL, Tss2_MU_UINT16_Marshal,
               authValue, ADDR, Tss2_MU_TPM2B_DIGEST_Marshal,
               seedValue, ADDR, Tss2_MU_TPM2B_DIGEST_Marshal,
               sensitive, sensitiveType, ADDR, Tss2_MU_TPMU_SENSITIVE_COMPOSITE_Marshal)

TPMT_UNMARSHAL_4(TPMT_SENSITIVE, sensitiveType, Tss2_MU_UINT16_Unmarshal,
                 authValue, Tss2_MU_TPM2B_DIGEST_Unmarshal,
                 seedValue, Tss2_MU_TPM2B_DIGEST_Unmarshal,
                 sensitive, sensitiveType, Tss2_MU_TPMU_SENSITIVE_COMPOSITE_Unmarshal)

TPMT_MARSHAL_6(TPMT_PUBLIC, type, VAL, Tss2_MU_UINT16_Marshal,
               nameAlg, VAL, Tss2_MU_UINT16_Marshal,
               objectAttributes, VAL, Tss2_MU_TPMA_OBJECT_Marshal,
               authPolicy, ADDR, Tss2_MU_TPM2B_DIGEST_Marshal,
               parameters, ADDR, type, Tss2_MU_TPMU_PUBLIC_PARMS_Marshal,
               unique, ADDR, type, Tss2_MU_TPMU_PUBLIC_ID_Marshal)

TPMT_UNMARSHAL_6(TPMT_PUBLIC, type, Tss2_MU_UINT16_Unmarshal,
                 nameAlg, Tss2_MU_UINT16_Unmarshal,
                 objectAttributes, Tss2_MU_TPMA_OBJECT_Unmarshal,
                 authPolicy, Tss2_MU_TPM2B_DIGEST_Unmarshal,
                 parameters, type, Tss2_MU_TPMU_PUBLIC_PARMS_Unmarshal,
                 unique, type, Tss2_MU_TPMU_PUBLIC_ID_Unmarshal)

TPMT_MARSHAL_2(TPMT_PUBLIC_PARMS, type, VAL, Tss2_MU_UINT16_Marshal,
               parameters, ADDR, type, Tss2_MU_TPMU_PUBLIC_PARMS_Marshal)

TPMT_UNMARSHAL_2(TPMT_PUBLIC_PARMS, type, Tss2_MU_UINT16_Unmarshal,
                 parameters, type, Tss2_MU_TPMU_PUBLIC_PARMS_Unmarshal)

TPMT_MARSHAL_TK(TPMT_TK_CREATION, tag, Tss2_MU_UINT16_Marshal,
                hierarchy, Tss2_MU_UINT32_Marshal, digest, Tss2_MU_TPM2B_DIGEST_Marshal)

TPMT_UNMARSHAL_TK(TPMT_TK_CREATION, tag, Tss2_MU_UINT16_Unmarshal,
                  hierarchy, Tss2_MU_UINT32_Unmarshal, digest, Tss2_MU_TPM2B_DIGEST_Unmarshal)

TPMT_MARSHAL_TK(TPMT_TK_VERIFIED, tag, Tss2_MU_UINT16_Marshal,
                hierarchy, Tss2_MU_UINT32_Marshal, digest, Tss2_MU_TPM2B_DIGEST_Marshal)

TPMT_UNMARSHAL_TK(TPMT_TK_VERIFIED, tag, Tss2_MU_UINT16_Unmarshal,
                  hierarchy, Tss2_MU_UINT32_Unmarshal, digest, Tss2_MU_TPM2B_DIGEST_Unmarshal)

TPMT_MARSHAL_TK(TPMT_TK_AUTH, tag, Tss2_MU_UINT16_Marshal,
                hierarchy, Tss2_MU_UINT32_Marshal, digest, Tss2_MU_TPM2B_DIGEST_Marshal)

TPMT_UNMARSHAL_TK(TPMT_TK_AUTH, tag, Tss2_MU_UINT16_Unmarshal,
                  hierarchy, Tss2_MU_UINT32_Unmarshal, digest, Tss2_MU_TPM2B_DIGEST_Unmarshal)

TPMT_MARSHAL_TK(TPMT_TK_HASHCHECK, tag, Tss2_MU_UINT16_Marshal,
                hierarchy, Tss2_MU_UINT32_Marshal, digest, Tss2_MU_TPM2B_DIGEST_Marshal)

TPMT_UNMARSHAL_TK(TPMT_TK_HASHCHECK, tag, Tss2_MU_UINT16_Unmarshal,
                  hierarchy, Tss2_MU_UINT32_Unmarshal, digest, Tss2_MU_TPM2B_DIGEST_Unmarshal)
