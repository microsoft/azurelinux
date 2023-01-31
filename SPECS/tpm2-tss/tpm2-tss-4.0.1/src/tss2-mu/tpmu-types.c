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

static TSS2_RC marshal_tab(BYTE const *src, uint8_t buffer[],
                           size_t buffer_size, size_t *offset, size_t size)
{
    size_t local_offset = 0;

    if (src == NULL) { \
        LOG_WARNING("src param is NULL"); \
        return TSS2_MU_RC_BAD_REFERENCE; \
    }

    if (offset != NULL) {
        LOG_DEBUG("offset non-NULL, initial value: %zu", *offset);
        local_offset = *offset;
    }

    if (buffer == NULL && offset == NULL) {
        LOG_WARNING("buffer and offset parameter are NULL");
        return TSS2_MU_RC_BAD_REFERENCE;
    } else if (buffer == NULL && offset != NULL) {
        *offset += size;
        LOG_TRACE("buffer NULL and offset non-NULL, updating offset to %zu",
             *offset);
        return TSS2_RC_SUCCESS;
    } else if (buffer_size < local_offset || buffer_size - local_offset < size) {
        LOG_DEBUG("buffer_size: %zu with offset: %zu are insufficient for "
             "object of size %zu", buffer_size, local_offset, size);
        return TSS2_MU_RC_INSUFFICIENT_BUFFER;
    }

    LOG_DEBUG("Marshalling TPMU tab of %d bytes from 0x%" PRIxPTR " to buffer 0x%"
         PRIxPTR " at index 0x%zx", (int)size, (uintptr_t)src, (uintptr_t)buffer,
         local_offset);

    memcpy(&buffer[local_offset], src, size);
    local_offset += size;

    if (offset) {
        *offset = local_offset;
        LOG_DEBUG("offset parameter non-NULL, updated to %zu", *offset);
    }
    return TSS2_RC_SUCCESS;
}

static TSS2_RC marshal_hash_sha(BYTE const *src, uint8_t buffer[],
                                size_t buffer_size, size_t *offset)
{
    return marshal_tab(src, buffer, buffer_size, offset, TPM2_SHA1_DIGEST_SIZE);
}

static TSS2_RC marshal_hash_sha256(BYTE const *src, uint8_t buffer[],
                                   size_t buffer_size, size_t *offset)
{
    return marshal_tab(src, buffer, buffer_size, offset, TPM2_SHA256_DIGEST_SIZE);
}

static TSS2_RC marshal_hash_sha384(BYTE const *src, uint8_t buffer[],
                                   size_t buffer_size, size_t *offset)
{
    return marshal_tab(src, buffer, buffer_size, offset, TPM2_SHA384_DIGEST_SIZE);
}

static TSS2_RC marshal_hash_sha512(BYTE const *src, uint8_t buffer[],
                                   size_t buffer_size, size_t *offset)
{
    return marshal_tab(src, buffer, buffer_size, offset, TPM2_SHA512_DIGEST_SIZE);
}

static TSS2_RC marshal_sm3_256(BYTE const *src, uint8_t buffer[],
                               size_t buffer_size, size_t *offset)
{
    return marshal_tab(src, buffer, buffer_size, offset, TPM2_SM3_256_DIGEST_SIZE);
}

static TSS2_RC marshal_ecc(BYTE const *src, uint8_t buffer[],
                           size_t buffer_size, size_t *offset)
{
    return marshal_tab(src, buffer, buffer_size, offset, sizeof(TPMS_ECC_POINT));
}

static TSS2_RC marshal_rsa(BYTE const *src, uint8_t buffer[],
                           size_t buffer_size, size_t *offset)
{
    return marshal_tab(src, buffer, buffer_size, offset, TPM2_MAX_RSA_KEY_BYTES);
}

static TSS2_RC marshal_symmetric(BYTE const *src, uint8_t buffer[],
                                 size_t buffer_size, size_t *offset)
{
    return marshal_tab(src, buffer, buffer_size, offset, sizeof(TPM2B_DIGEST));
}

static TSS2_RC marshal_keyedhash(BYTE const *src, uint8_t buffer[],
                                 size_t buffer_size, size_t *offset)
{
    return marshal_tab(src, buffer, buffer_size, offset, sizeof(TPM2B_DIGEST));
}


static TSS2_RC marshal_null(void const *src, uint8_t buffer[],
                            size_t buffer_size, size_t *offset)
{
    UNUSED(src);
    UNUSED(buffer);
    UNUSED(buffer_size);
    UNUSED(offset);
    return TSS2_RC_SUCCESS;
}

static TSS2_RC unmarshal_tab(uint8_t const buffer[], size_t buffer_size,
                             size_t *offset, BYTE *dest, size_t size)
{
    size_t  local_offset = 0;

    if (offset != NULL) {
        LOG_DEBUG("offset non-NULL, initial value: %zu", *offset);
        local_offset = *offset;
    }

    if (buffer == NULL || (dest == NULL && offset == NULL)) {
        LOG_WARNING("buffer or dest and offset parameter are NULL");
        return TSS2_MU_RC_BAD_REFERENCE;
    } else if (dest == NULL && offset != NULL) {
        *offset += size;
        LOG_TRACE("buffer NULL and offset non-NULL, updating offset to %zu",
             *offset);
        return TSS2_RC_SUCCESS;
    } else if (buffer_size < local_offset || size > buffer_size - local_offset) {
        LOG_DEBUG("buffer_size: %zu with offset: %zu are insufficient for "
             "object of size %zu", buffer_size, local_offset, size);
        return TSS2_MU_RC_INSUFFICIENT_BUFFER;
    }

    LOG_DEBUG("Marshalling TPMU tab of %d bytes from buffer 0x%" PRIxPTR
         " at index 0x%zx to dest 0x%" PRIxPTR, (int)size, (uintptr_t)buffer,
         local_offset, (uintptr_t)dest);

    memcpy(dest, &buffer[local_offset], size);
    local_offset += size;

    if (offset) {
        *offset = local_offset;
        LOG_DEBUG("offset parameter non-NULL, updated to %zu", *offset);
    }
    return TSS2_RC_SUCCESS;
}

static TSS2_RC unmarshal_hash_sha(uint8_t const buffer[], size_t buffer_size,
                                  size_t *offset, BYTE *dest)
{
    return unmarshal_tab(buffer, buffer_size, offset, dest, TPM2_SHA1_DIGEST_SIZE);
}

static TSS2_RC unmarshal_hash_sha256(uint8_t const buffer[], size_t buffer_size,
                                     size_t *offset, BYTE *dest)
{
    return unmarshal_tab(buffer, buffer_size, offset, dest, TPM2_SHA256_DIGEST_SIZE);
}

static TSS2_RC unmarshal_hash_sha384(uint8_t const buffer[], size_t buffer_size,
                                     size_t *offset, BYTE *dest)
{
    return unmarshal_tab(buffer, buffer_size, offset, dest, TPM2_SHA384_DIGEST_SIZE);
}

static TSS2_RC unmarshal_hash_sha512(uint8_t const buffer[], size_t buffer_size,
                                     size_t *offset, BYTE *dest)
{
    return unmarshal_tab(buffer, buffer_size, offset, dest, TPM2_SHA512_DIGEST_SIZE);
}

static TSS2_RC unmarshal_sm3_256(uint8_t const buffer[], size_t buffer_size,
                                 size_t *offset, BYTE *dest)
{
    return unmarshal_tab(buffer, buffer_size, offset, dest, TPM2_SM3_256_DIGEST_SIZE);
}

static TSS2_RC unmarshal_ecc(uint8_t const buffer[], size_t buffer_size,
                             size_t *offset, BYTE *dest)
{
    return unmarshal_tab(buffer, buffer_size, offset, dest, sizeof(TPMS_ECC_POINT));
}

static TSS2_RC unmarshal_rsa(uint8_t const buffer[], size_t buffer_size,
                             size_t *offset, BYTE *dest)
{
    return unmarshal_tab(buffer, buffer_size, offset, dest, TPM2_MAX_RSA_KEY_BYTES);
}

static TSS2_RC unmarshal_symmetric(uint8_t const buffer[], size_t buffer_size,
                                   size_t *offset, BYTE *dest)
{
    return unmarshal_tab(buffer, buffer_size, offset, dest, sizeof(TPM2B_DIGEST));
}

static TSS2_RC unmarshal_keyedhash(uint8_t const buffer[], size_t buffer_size,
                                   size_t *offset, BYTE *dest)
{
    return unmarshal_tab(buffer, buffer_size, offset, dest, sizeof(TPM2B_DIGEST));
}

static TSS2_RC unmarshal_null(uint8_t const buffer[], size_t buffer_size,
                              size_t *offset, void *dest)
{
    UNUSED(buffer);
    UNUSED(buffer_size);
    UNUSED(offset);
    UNUSED(dest);
    return TSS2_RC_SUCCESS;
}

/*
 * The TPMU_* types are unions with some number of members. The marshal
 * function for each union uses the provided selector value to identify the
 * member from the union that's written to the buffer. This is a pattern
 * that can be leveraged to generate the function bodies using macros.
 *
 * The TPMU_MARSHAL macro is used to generate these function bodies. It is
 * used below, once to define the marshaling function for each of the 15
 * unique TPMU_* types. The parameters are:
 *   type - The type of the TPMU_* being marshaled. This is used to
 *       generate the name of the function and the type of its first
 *       parameter.
 *   The remaining parameters are grouped as 4-tuples. There are 12 of them,
 *       each defined as <selector, operator, member, function> where:
 *       selector - The constant value, typically from a table in some TCG
 *           registry, that the generated function will use to select the
 *           member marshaled / written in network byte order to the buffer.
 *       operator - The member being marshaled may be passed by value or
 *           reference to its marshaling function. If it's by value this
 *           should be 'VAL', if by reference 'ADDR'.
 *       member - The name of the member data from the union passed to the
 *           marshaling function (the next parameter).
 *       function - A function capable of marshaling the 'member' from the
 *           TPMU_* being marshaled.
 *
 * This macro takes 12 such 4-tuples. This is the maximum number of members
 * in the TPMU_* types. All parameters after the first 49 parameters (12*4+1)
 * are taken as variadic arguments (...) but they are ignored. The reason for
 * this is documented with the TPMU_MARSHAL2 macro below.
 *
 * NOTE: this macro must be passed 12 4-tuples even when defining TPMU_* types
 * with fewer than 12 members. The extra tuples should be defined as:
 * <-X, ADDR, m, marshal_null> where:
 *     -X - A unique negative constant value.
 *     ADDR - The macro defined at the top of this file.
 *     m - Any valid member from the TPMU_* being marshaled.
 *     marshal_null - A function defined above that is effectively a
 *         marshaling no-op.
 */
#define TPMU_MARSHAL(type, sel, op, m, fn, sel2, op2, m2, fn2, sel3, op3, m3, fn3, \
                     sel4, op4, m4, fn4, sel5, op5, m5, fn5, sel6, op6, m6, fn6, \
                     sel7, op7, m7, fn7, sel8, op8, m8, fn8, sel9, op9, m9, fn9, \
                     sel10, op10, m10, fn10, sel11, op11, m11, fn11, sel12, op12, \
                     m12, fn12,  ...) \
TSS2_RC Tss2_MU_##type##_Marshal(type const *src, uint32_t selector, uint8_t buffer[], \
                                 size_t buffer_size, size_t *offset) \
{ \
    TSS2_RC ret = TSS2_MU_RC_BAD_VALUE; \
\
    if (src == NULL) { \
        LOG_WARNING("src param is NULL"); \
        return TSS2_MU_RC_BAD_REFERENCE; \
    } \
\
    LOG_DEBUG("Marshalling " #type ", selector %x", selector); \
    switch (selector) { \
    case sel: \
    ret = fn(op src->m, buffer, buffer_size, offset); \
    break; \
    case sel2: \
    ret = fn2(op2 src->m2, buffer, buffer_size, offset); \
    break; \
    case sel3: \
    ret = fn3(op3 src->m3, buffer, buffer_size, offset); \
    break; \
    case sel4: \
    ret = fn4(op4 src->m4, buffer, buffer_size, offset); \
    break; \
    case sel5: \
    ret = fn5(op5 src->m5, buffer, buffer_size, offset); \
    break; \
    case sel6: \
    ret = fn6(op6 src->m6, buffer, buffer_size, offset); \
    break; \
    case sel7: \
    ret = fn7(op7 src->m7, buffer, buffer_size, offset); \
    break; \
    case sel8: \
    ret = fn8(op8 src->m8, buffer, buffer_size, offset); \
    break; \
    case sel9: \
    ret = fn9(op9 src->m9, buffer, buffer_size, offset); \
    break; \
    case sel10: \
    ret = fn10(op10 src->m10, buffer, buffer_size, offset); \
    break; \
    case sel11: \
    ret = fn11(op11 src->m11, buffer, buffer_size, offset); \
    break; \
    case sel12: \
    ret = fn12(op12 src->m12, buffer, buffer_size, offset); \
    break; \
    case TPM2_ALG_NULL: \
    LOG_DEBUG("ALG_NULL selector skipping"); \
    ret = TSS2_RC_SUCCESS; \
    break; \
    default: \
    LOG_DEBUG("wrong selector %x return error", selector); \
    break; \
    } \
    return ret; \
}

/*
 * The TPMU_MARSHAL2 macro is a thin wrapper around the TPMU_MARSHAL macro.
 * This macro is designed to keep us from having to provide dummy 4-tuples
 * to satisfy the required 49 (12*4+1) parameters required by TPMU_MARSHAL.
 *
 * It does this by accepting the tuples describing the variable number of
 * members in a TPMU_* union (except for the first one) as variadic
 * arguments. It passes the supplied tuples to TPMU_MARSHAL while providing
 * additional no-op tuples to pad out the remaining required parameters to
 * the TPMU_MARSHAL macro.
 *
 * NOTE: Remember that all parameters to the TPMU_MARSHAL macro beyond the
 * first 49 are variadic parameters and are ignored by the macro. This
 * allows the TPMU_MARSHAL2 macro to provide the maximum required no-op
 * tuples.
 * e.g. The TPMU_* unions have between 2 and 12 members. A 2 member
 * TPMU_* will require 9 no-op tuples to provide 45 parameters to the
 * TPMU_MARSHAL macro (note the 10 no-op tuples used in the TPMU_MARSHAL2
 * macro). The largest TPMU_* with 11 members will need to provide 0 no-op
 * tuples. In this last case the 10 no-op tuples provided by the
 * TPMU_MARSHAL2 macro will fall into the variadic parameters accepted by
 * TPMU_MARSHAL and they will be ignored.
 */
#define TPMU_MARSHAL2(type, sel, op, m, fn, ...) \
    TPMU_MARSHAL(type, sel, op, m, fn, __VA_ARGS__, -1, ADDR, m, marshal_null, \
                 -2, ADDR, m, marshal_null, -3, ADDR, m, marshal_null, \
                 -4, ADDR, m, marshal_null, -5, ADDR, m, marshal_null, \
                 -6, ADDR, m, marshal_null, -7, ADDR, m, marshal_null, \
                 -8, ADDR, m, marshal_null, -9, ADDR, m, marshal_null, \
				 -10, ADDR, m, marshal_null)

/*
 * The TPMU_UNMARSHAL macro functions in the same way as the TPMU_MARSHAL
 * macro. The main difference is that instead of a 4-tuple of <selector,
 * operator, member, function> we remove the operator element and have
 * a 3-tuple of <selector, member, function>. The operator element isn't
 * needed because the first parameter to the function element is always a
 * reference (never a value).
 */
#define TPMU_UNMARSHAL(type, sel, m, fn, sel2, m2, fn2, sel3, m3, fn3, \
                       sel4, m4, fn4, sel5, m5, fn5, sel6, m6, fn6, sel7, m7, fn7, \
                       sel8, m8, fn8, sel9, m9, fn9, sel10, m10, fn10, sel11, m11, fn11, \
					   sel12, m12, fn12,...) \
TSS2_RC Tss2_MU_##type##_Unmarshal(uint8_t const buffer[], size_t buffer_size, \
                                   size_t *offset, uint32_t selector, type *dest) \
{ \
    TSS2_RC ret = TSS2_MU_RC_BAD_VALUE; \
\
    LOG_DEBUG("Unmarshalling " #type ", selector %x", selector); \
    switch (selector) { \
    case sel: \
    ret = fn(buffer, buffer_size, offset, dest ? &dest->m : NULL); \
    break; \
    case sel2: \
    ret = fn2(buffer, buffer_size, offset, dest ? &dest->m2 : NULL); \
    break; \
    case sel3: \
    ret = fn3(buffer, buffer_size, offset, dest ? &dest->m3 : NULL); \
    break; \
    case sel4: \
    ret = fn4(buffer, buffer_size, offset, dest ? &dest->m4 : NULL); \
    break; \
    case sel5: \
    ret = fn5(buffer, buffer_size, offset, dest ? &dest->m5 : NULL); \
    break; \
    case sel6: \
    ret = fn6(buffer, buffer_size, offset, dest ? &dest->m6 : NULL); \
    break; \
    case sel7: \
    ret = fn7(buffer, buffer_size, offset, dest ? &dest->m7 : NULL); \
    break; \
    case sel8: \
    ret = fn8(buffer, buffer_size, offset, dest ? &dest->m8 : NULL); \
    break; \
    case sel9: \
    ret = fn9(buffer, buffer_size, offset, dest ? &dest->m9 : NULL); \
    break; \
    case sel10: \
    ret = fn10(buffer, buffer_size, offset, dest ? &dest->m10 : NULL); \
    break; \
    case sel11: \
    ret = fn11(buffer, buffer_size, offset, dest ? &dest->m11 : NULL); \
    break; \
    case sel12: \
    ret = fn12(buffer, buffer_size, offset, dest ? &dest->m12 : NULL); \
    break; \
    case TPM2_ALG_NULL: \
    LOG_DEBUG("ALG_NULL selector skipping"); \
    ret = TSS2_RC_SUCCESS; \
    break; \
    default: \
    LOG_DEBUG("wrong selector %x return error", selector); \
    break; \
    } \
    return ret; \
}

/*
 * The TPMU_UNMARSHAL2 operates on the same principles as the TPMU_MARSHAL2
 * function. The difference again is that the <selector, member, function>
 * tuple is a 3-tuple (not the 4-tuple used by TPMU_MARSHAL2).
 */
#define TPMU_UNMARSHAL2(type, sel, m, fn, ...) \
    TPMU_UNMARSHAL(type, sel, m, fn, __VA_ARGS__, -1, m, unmarshal_null, \
            -2, m, unmarshal_null, -3, m, unmarshal_null, -4, m, unmarshal_null, \
            -5, m, unmarshal_null, -6, m, unmarshal_null, -7, m, unmarshal_null, \
            -8, m, unmarshal_null, -9, m, unmarshal_null, -10, m, unmarshal_null)

/*
 * Following are invocations of the TPMU_MARSHAL2 and TPMU_UNMARSHAL2 macros.
 * These generate the marshaling and unmarshaling functions for the TPMU_*
 * types. They are grouped by TPMU_* with the TPMU_* being the first parameter
 * to each and on the first line with the macro name. The remaining parameters
 * are grouped, one 4-tuple per line for the TPMU_MARSHAL2 macro and one
 * 3-tuple per line for the TPMU_UNMARSHAL2 macro.
 */
TPMU_MARSHAL2(TPMU_HA,
    TPM2_ALG_SHA1, ADDR, sha1[0], marshal_hash_sha,
    TPM2_ALG_SHA256, ADDR, sha256[0], marshal_hash_sha256,
    TPM2_ALG_SHA384, ADDR, sha384[0], marshal_hash_sha384,
    TPM2_ALG_SHA512, ADDR, sha512[0], marshal_hash_sha512,
    TPM2_ALG_SM3_256, ADDR, sm3_256[0], marshal_sm3_256)
TPMU_UNMARSHAL2(TPMU_HA,
    TPM2_ALG_SHA1, sha1[0], unmarshal_hash_sha,
    TPM2_ALG_SHA256, sha256[0], unmarshal_hash_sha256,
    TPM2_ALG_SHA384, sha384[0], unmarshal_hash_sha384,
    TPM2_ALG_SHA512, sha512[0], unmarshal_hash_sha512,
    TPM2_ALG_SM3_256, sm3_256[0], unmarshal_sm3_256)

TPMU_MARSHAL2(TPMU_CAPABILITIES,
    TPM2_CAP_ALGS, ADDR, algorithms, Tss2_MU_TPML_ALG_PROPERTY_Marshal,
    TPM2_CAP_HANDLES, ADDR, handles, Tss2_MU_TPML_HANDLE_Marshal,
    TPM2_CAP_COMMANDS, ADDR, command, Tss2_MU_TPML_CCA_Marshal,
    TPM2_CAP_PP_COMMANDS, ADDR, ppCommands, Tss2_MU_TPML_CC_Marshal,
    TPM2_CAP_AUDIT_COMMANDS, ADDR, auditCommands, Tss2_MU_TPML_CC_Marshal,
    TPM2_CAP_PCRS, ADDR, assignedPCR, Tss2_MU_TPML_PCR_SELECTION_Marshal,
    TPM2_CAP_TPM_PROPERTIES, ADDR, tpmProperties, Tss2_MU_TPML_TAGGED_TPM_PROPERTY_Marshal,
    TPM2_CAP_PCR_PROPERTIES, ADDR, pcrProperties, Tss2_MU_TPML_TAGGED_PCR_PROPERTY_Marshal,
    TPM2_CAP_ECC_CURVES, ADDR, eccCurves, Tss2_MU_TPML_ECC_CURVE_Marshal,
    TPM2_CAP_AUTH_POLICIES, ADDR, authPolicies, Tss2_MU_TPML_TAGGED_POLICY_Marshal,
    TPM2_CAP_ACT, ADDR, actData, Tss2_MU_TPML_ACT_DATA_Marshal,
    TPM2_CAP_VENDOR_PROPERTY, ADDR, vendor, Tss2_MU_TPM2B_MAX_CAP_BUFFER_Marshal)

TPMU_UNMARSHAL2(TPMU_CAPABILITIES,
    TPM2_CAP_ALGS, algorithms, Tss2_MU_TPML_ALG_PROPERTY_Unmarshal,
    TPM2_CAP_HANDLES, handles, Tss2_MU_TPML_HANDLE_Unmarshal,
    TPM2_CAP_COMMANDS, command, Tss2_MU_TPML_CCA_Unmarshal,
    TPM2_CAP_PP_COMMANDS, ppCommands, Tss2_MU_TPML_CC_Unmarshal,
    TPM2_CAP_AUDIT_COMMANDS, auditCommands, Tss2_MU_TPML_CC_Unmarshal,
    TPM2_CAP_PCRS, assignedPCR, Tss2_MU_TPML_PCR_SELECTION_Unmarshal,
    TPM2_CAP_TPM_PROPERTIES, tpmProperties, Tss2_MU_TPML_TAGGED_TPM_PROPERTY_Unmarshal,
    TPM2_CAP_PCR_PROPERTIES, pcrProperties, Tss2_MU_TPML_TAGGED_PCR_PROPERTY_Unmarshal,
    TPM2_CAP_ECC_CURVES, eccCurves, Tss2_MU_TPML_ECC_CURVE_Unmarshal,
    TPM2_CAP_AUTH_POLICIES, authPolicies, Tss2_MU_TPML_TAGGED_POLICY_Unmarshal,
    TPM2_CAP_ACT, actData, Tss2_MU_TPML_ACT_DATA_Unmarshal,
    TPM2_CAP_VENDOR_PROPERTY, vendor, Tss2_MU_TPM2B_MAX_CAP_BUFFER_Unmarshal)

TPMU_MARSHAL2(TPMU_ATTEST,
    TPM2_ST_ATTEST_CERTIFY, ADDR, certify, Tss2_MU_TPMS_CERTIFY_INFO_Marshal,
    TPM2_ST_ATTEST_CREATION, ADDR, creation, Tss2_MU_TPMS_CREATION_INFO_Marshal,
    TPM2_ST_ATTEST_QUOTE, ADDR, quote, Tss2_MU_TPMS_QUOTE_INFO_Marshal,
    TPM2_ST_ATTEST_COMMAND_AUDIT, ADDR, commandAudit, Tss2_MU_TPMS_COMMAND_AUDIT_INFO_Marshal,
    TPM2_ST_ATTEST_SESSION_AUDIT, ADDR, sessionAudit, Tss2_MU_TPMS_SESSION_AUDIT_INFO_Marshal,
    TPM2_ST_ATTEST_TIME, ADDR, time, Tss2_MU_TPMS_TIME_ATTEST_INFO_Marshal,
    TPM2_ST_ATTEST_NV, ADDR, nv, Tss2_MU_TPMS_NV_CERTIFY_INFO_Marshal)
TPMU_UNMARSHAL2(TPMU_ATTEST,
    TPM2_ST_ATTEST_CERTIFY, certify, Tss2_MU_TPMS_CERTIFY_INFO_Unmarshal,
    TPM2_ST_ATTEST_CREATION, creation, Tss2_MU_TPMS_CREATION_INFO_Unmarshal,
    TPM2_ST_ATTEST_QUOTE, quote, Tss2_MU_TPMS_QUOTE_INFO_Unmarshal,
    TPM2_ST_ATTEST_COMMAND_AUDIT, commandAudit, Tss2_MU_TPMS_COMMAND_AUDIT_INFO_Unmarshal,
    TPM2_ST_ATTEST_SESSION_AUDIT, sessionAudit, Tss2_MU_TPMS_SESSION_AUDIT_INFO_Unmarshal,
    TPM2_ST_ATTEST_TIME, time, Tss2_MU_TPMS_TIME_ATTEST_INFO_Unmarshal,
    TPM2_ST_ATTEST_NV, nv, Tss2_MU_TPMS_NV_CERTIFY_INFO_Unmarshal)

TPMU_MARSHAL2(TPMU_SYM_KEY_BITS,
    TPM2_ALG_AES, VAL, aes, Tss2_MU_UINT16_Marshal,
    TPM2_ALG_SM4, VAL, sm4, Tss2_MU_UINT16_Marshal,
    TPM2_ALG_CAMELLIA, VAL, camellia, Tss2_MU_UINT16_Marshal,
    TPM2_ALG_XOR, VAL, exclusiveOr, Tss2_MU_UINT16_Marshal,
    TPM2_ALG_SYMCIPHER, VAL, sym, Tss2_MU_UINT16_Marshal)
TPMU_UNMARSHAL2(TPMU_SYM_KEY_BITS,
    TPM2_ALG_AES, aes, Tss2_MU_UINT16_Unmarshal,
    TPM2_ALG_SM4, sm4, Tss2_MU_UINT16_Unmarshal,
    TPM2_ALG_CAMELLIA, camellia, Tss2_MU_UINT16_Unmarshal,
    TPM2_ALG_XOR, exclusiveOr, Tss2_MU_UINT16_Unmarshal,
    TPM2_ALG_SYMCIPHER, sym, Tss2_MU_UINT16_Unmarshal)

TPMU_MARSHAL2(TPMU_SYM_MODE,
    TPM2_ALG_AES, VAL, aes, Tss2_MU_UINT16_Marshal,
    TPM2_ALG_SM4, VAL, sm4, Tss2_MU_UINT16_Marshal,
    TPM2_ALG_CAMELLIA, VAL, camellia, Tss2_MU_UINT16_Marshal,
    TPM2_ALG_XOR, ADDR, sym, marshal_null,
    TPM2_ALG_SYMCIPHER, VAL, sym, Tss2_MU_UINT16_Marshal)
TPMU_UNMARSHAL2(TPMU_SYM_MODE,
    TPM2_ALG_AES, aes, Tss2_MU_UINT16_Unmarshal,
    TPM2_ALG_SM4, sm4, Tss2_MU_UINT16_Unmarshal,
    TPM2_ALG_CAMELLIA, camellia, Tss2_MU_UINT16_Unmarshal,
    TPM2_ALG_XOR, sym, unmarshal_null,
    TPM2_ALG_SYMCIPHER, sym, Tss2_MU_UINT16_Unmarshal)

TPMU_MARSHAL2(TPMU_SIG_SCHEME,
    TPM2_ALG_RSASSA, ADDR, rsassa, Tss2_MU_TPMS_SCHEME_HASH_Marshal,
    TPM2_ALG_RSAPSS, ADDR, rsapss, Tss2_MU_TPMS_SCHEME_HASH_Marshal,
    TPM2_ALG_ECDSA, ADDR, ecdsa, Tss2_MU_TPMS_SCHEME_HASH_Marshal,
    TPM2_ALG_ECDAA, ADDR, ecdaa, Tss2_MU_TPMS_SCHEME_ECDAA_Marshal,
    TPM2_ALG_SM2, ADDR, sm2, Tss2_MU_TPMS_SCHEME_HASH_Marshal,
    TPM2_ALG_ECSCHNORR, ADDR, ecschnorr, Tss2_MU_TPMS_SCHEME_HASH_Marshal,
    TPM2_ALG_HMAC, ADDR, hmac, Tss2_MU_TPMS_SCHEME_HASH_Marshal)
TPMU_UNMARSHAL2(TPMU_SIG_SCHEME,
    TPM2_ALG_RSASSA, rsassa, Tss2_MU_TPMS_SCHEME_HASH_Unmarshal,
    TPM2_ALG_RSAPSS, rsapss, Tss2_MU_TPMS_SCHEME_HASH_Unmarshal,
    TPM2_ALG_ECDSA, ecdsa, Tss2_MU_TPMS_SCHEME_HASH_Unmarshal,
    TPM2_ALG_ECDAA, ecdaa, Tss2_MU_TPMS_SCHEME_ECDAA_Unmarshal,
    TPM2_ALG_SM2, sm2, Tss2_MU_TPMS_SCHEME_HASH_Unmarshal,
    TPM2_ALG_ECSCHNORR, ecschnorr, Tss2_MU_TPMS_SCHEME_HASH_Unmarshal,
    TPM2_ALG_HMAC, hmac, Tss2_MU_TPMS_SCHEME_HASH_Unmarshal)

TPMU_MARSHAL2(TPMU_KDF_SCHEME,
    TPM2_ALG_MGF1, ADDR, mgf1, Tss2_MU_TPMS_SCHEME_HASH_Marshal,
    TPM2_ALG_KDF1_SP800_56A, ADDR, kdf1_sp800_56a, Tss2_MU_TPMS_SCHEME_HASH_Marshal,
    TPM2_ALG_KDF1_SP800_108, ADDR, kdf1_sp800_108, Tss2_MU_TPMS_SCHEME_HASH_Marshal)
TPMU_UNMARSHAL2(TPMU_KDF_SCHEME,
    TPM2_ALG_MGF1, mgf1, Tss2_MU_TPMS_SCHEME_HASH_Unmarshal,
    TPM2_ALG_KDF1_SP800_56A, kdf1_sp800_56a, Tss2_MU_TPMS_SCHEME_HASH_Unmarshal,
    TPM2_ALG_KDF1_SP800_108, kdf1_sp800_108, Tss2_MU_TPMS_SCHEME_HASH_Unmarshal)

TPMU_MARSHAL2(TPMU_ASYM_SCHEME,
    TPM2_ALG_ECDH, ADDR, ecdh, Tss2_MU_TPMS_SCHEME_HASH_Marshal,
    TPM2_ALG_ECMQV, ADDR, ecmqv, Tss2_MU_TPMS_SCHEME_HASH_Marshal,
    TPM2_ALG_RSASSA, ADDR, rsassa, Tss2_MU_TPMS_SCHEME_HASH_Marshal,
    TPM2_ALG_RSAPSS, ADDR, rsapss, Tss2_MU_TPMS_SCHEME_HASH_Marshal,
    TPM2_ALG_ECDSA, ADDR, ecdsa, Tss2_MU_TPMS_SCHEME_HASH_Marshal,
    TPM2_ALG_ECDAA, ADDR, ecdaa, Tss2_MU_TPMS_SCHEME_ECDAA_Marshal,
    TPM2_ALG_SM2, ADDR, sm2, Tss2_MU_TPMS_SCHEME_HASH_Marshal,
    TPM2_ALG_ECSCHNORR, ADDR, ecschnorr, Tss2_MU_TPMS_SCHEME_HASH_Marshal,
    TPM2_ALG_RSAES, ADDR, rsaes, marshal_null,
    TPM2_ALG_OAEP, ADDR, oaep, Tss2_MU_TPMS_SCHEME_HASH_Marshal)
TPMU_UNMARSHAL2(TPMU_ASYM_SCHEME,
    TPM2_ALG_ECDH, ecdh, Tss2_MU_TPMS_SCHEME_HASH_Unmarshal,
    TPM2_ALG_ECMQV, ecmqv, Tss2_MU_TPMS_SCHEME_HASH_Unmarshal,
    TPM2_ALG_RSASSA, rsassa, Tss2_MU_TPMS_SCHEME_HASH_Unmarshal,
    TPM2_ALG_RSAPSS, rsapss, Tss2_MU_TPMS_SCHEME_HASH_Unmarshal,
    TPM2_ALG_ECDSA, ecdsa, Tss2_MU_TPMS_SCHEME_HASH_Unmarshal,
    TPM2_ALG_ECDAA, ecdaa, Tss2_MU_TPMS_SCHEME_ECDAA_Unmarshal,
    TPM2_ALG_SM2, sm2, Tss2_MU_TPMS_SCHEME_HASH_Unmarshal,
    TPM2_ALG_ECSCHNORR, ecschnorr, Tss2_MU_TPMS_SCHEME_HASH_Unmarshal,
    TPM2_ALG_RSAES, rsaes, unmarshal_null,
    TPM2_ALG_OAEP, oaep, Tss2_MU_TPMS_SCHEME_HASH_Unmarshal)

TPMU_MARSHAL2(TPMU_SCHEME_KEYEDHASH,
    TPM2_ALG_HMAC, ADDR, hmac, Tss2_MU_TPMS_SCHEME_HASH_Marshal,
    TPM2_ALG_XOR, ADDR, exclusiveOr, Tss2_MU_TPMS_SCHEME_XOR_Marshal)
TPMU_UNMARSHAL2(TPMU_SCHEME_KEYEDHASH,
    TPM2_ALG_HMAC, hmac, Tss2_MU_TPMS_SCHEME_HASH_Unmarshal,
    TPM2_ALG_XOR, exclusiveOr, Tss2_MU_TPMS_SCHEME_XOR_Unmarshal)

TPMU_MARSHAL2(TPMU_SIGNATURE,
    TPM2_ALG_RSASSA, ADDR, rsassa, Tss2_MU_TPMS_SIGNATURE_RSA_Marshal,
    TPM2_ALG_RSAPSS, ADDR, rsapss, Tss2_MU_TPMS_SIGNATURE_RSA_Marshal,
    TPM2_ALG_ECDSA, ADDR, ecdsa, Tss2_MU_TPMS_SIGNATURE_ECC_Marshal,
    TPM2_ALG_ECDAA, ADDR, ecdaa, Tss2_MU_TPMS_SIGNATURE_ECC_Marshal,
    TPM2_ALG_SM2, ADDR, sm2, Tss2_MU_TPMS_SIGNATURE_ECC_Marshal,
    TPM2_ALG_ECSCHNORR, ADDR, ecschnorr, Tss2_MU_TPMS_SIGNATURE_ECC_Marshal,
    TPM2_ALG_HMAC, ADDR, hmac, Tss2_MU_TPMT_HA_Marshal)
TPMU_UNMARSHAL2(TPMU_SIGNATURE,
    TPM2_ALG_RSASSA, rsassa, Tss2_MU_TPMS_SIGNATURE_RSA_Unmarshal,
    TPM2_ALG_RSAPSS, rsapss, Tss2_MU_TPMS_SIGNATURE_RSA_Unmarshal,
    TPM2_ALG_ECDSA, ecdsa, Tss2_MU_TPMS_SIGNATURE_ECC_Unmarshal,
    TPM2_ALG_ECDAA, ecdaa, Tss2_MU_TPMS_SIGNATURE_ECC_Unmarshal,
    TPM2_ALG_SM2, sm2, Tss2_MU_TPMS_SIGNATURE_ECC_Unmarshal,
    TPM2_ALG_ECSCHNORR, ecschnorr, Tss2_MU_TPMS_SIGNATURE_ECC_Unmarshal,
    TPM2_ALG_HMAC, hmac, Tss2_MU_TPMT_HA_Unmarshal)

TPMU_MARSHAL2(TPMU_SENSITIVE_COMPOSITE,
    TPM2_ALG_RSA, ADDR, rsa, Tss2_MU_TPM2B_PRIVATE_KEY_RSA_Marshal,
    TPM2_ALG_ECC, ADDR, ecc, Tss2_MU_TPM2B_ECC_PARAMETER_Marshal,
    TPM2_ALG_KEYEDHASH, ADDR, bits, Tss2_MU_TPM2B_SENSITIVE_DATA_Marshal,
    TPM2_ALG_SYMCIPHER, ADDR, sym, Tss2_MU_TPM2B_SYM_KEY_Marshal)
TPMU_UNMARSHAL2(TPMU_SENSITIVE_COMPOSITE,
    TPM2_ALG_RSA, rsa, Tss2_MU_TPM2B_PRIVATE_KEY_RSA_Unmarshal,
    TPM2_ALG_ECC, ecc, Tss2_MU_TPM2B_ECC_PARAMETER_Unmarshal,
    TPM2_ALG_KEYEDHASH, bits, Tss2_MU_TPM2B_SENSITIVE_DATA_Unmarshal,
    TPM2_ALG_SYMCIPHER, sym, Tss2_MU_TPM2B_SYM_KEY_Unmarshal)

TPMU_MARSHAL2(TPMU_ENCRYPTED_SECRET,
    TPM2_ALG_ECC, ADDR, ecc[0], marshal_ecc,
    TPM2_ALG_RSA, ADDR, rsa[0], marshal_rsa,
    TPM2_ALG_SYMCIPHER, ADDR, symmetric[0], marshal_symmetric,
    TPM2_ALG_KEYEDHASH, ADDR, keyedHash[0], marshal_keyedhash)
TPMU_UNMARSHAL2(TPMU_ENCRYPTED_SECRET,
    TPM2_ALG_ECC, ecc[0], unmarshal_ecc,
    TPM2_ALG_RSA, rsa[0], unmarshal_rsa,
    TPM2_ALG_SYMCIPHER, symmetric[0], unmarshal_symmetric,
    TPM2_ALG_KEYEDHASH, keyedHash[0], unmarshal_keyedhash)

TPMU_MARSHAL2(TPMU_PUBLIC_ID,
    TPM2_ALG_KEYEDHASH, ADDR, keyedHash, Tss2_MU_TPM2B_DIGEST_Marshal,
    TPM2_ALG_SYMCIPHER, ADDR, sym, Tss2_MU_TPM2B_DIGEST_Marshal,
    TPM2_ALG_RSA, ADDR, rsa, Tss2_MU_TPM2B_PUBLIC_KEY_RSA_Marshal,
    TPM2_ALG_ECC, ADDR, ecc, Tss2_MU_TPMS_ECC_POINT_Marshal)
TPMU_UNMARSHAL2(TPMU_PUBLIC_ID,
    TPM2_ALG_KEYEDHASH, keyedHash, Tss2_MU_TPM2B_DIGEST_Unmarshal,
    TPM2_ALG_SYMCIPHER, sym, Tss2_MU_TPM2B_DIGEST_Unmarshal,
    TPM2_ALG_RSA, rsa, Tss2_MU_TPM2B_PUBLIC_KEY_RSA_Unmarshal,
    TPM2_ALG_ECC, ecc, Tss2_MU_TPMS_ECC_POINT_Unmarshal)

TPMU_MARSHAL2(TPMU_PUBLIC_PARMS,
    TPM2_ALG_KEYEDHASH, ADDR, keyedHashDetail, Tss2_MU_TPMS_KEYEDHASH_PARMS_Marshal,
    TPM2_ALG_SYMCIPHER, ADDR, symDetail, Tss2_MU_TPMS_SYMCIPHER_PARMS_Marshal,
    TPM2_ALG_RSA, ADDR, rsaDetail, Tss2_MU_TPMS_RSA_PARMS_Marshal,
    TPM2_ALG_ECC, ADDR, eccDetail, Tss2_MU_TPMS_ECC_PARMS_Marshal)
TPMU_UNMARSHAL2(TPMU_PUBLIC_PARMS,
    TPM2_ALG_KEYEDHASH, keyedHashDetail, Tss2_MU_TPMS_KEYEDHASH_PARMS_Unmarshal,
    TPM2_ALG_SYMCIPHER, symDetail, Tss2_MU_TPMS_SYMCIPHER_PARMS_Unmarshal,
    TPM2_ALG_RSA, rsaDetail, Tss2_MU_TPMS_RSA_PARMS_Unmarshal,
    TPM2_ALG_ECC, eccDetail, Tss2_MU_TPMS_ECC_PARMS_Unmarshal)

TPMU_MARSHAL2(TPMU_NAME,
    sizeof(TPM2_HANDLE), VAL, handle, Tss2_MU_UINT32_Marshal,
    sizeof(TPM2_ALG_ID) + TPM2_SHA1_DIGEST_SIZE, ADDR, digest, Tss2_MU_TPMT_HA_Marshal,
    sizeof(TPM2_ALG_ID) + TPM2_SHA256_DIGEST_SIZE, ADDR, digest, Tss2_MU_TPMT_HA_Marshal,
    sizeof(TPM2_ALG_ID) + TPM2_SHA384_DIGEST_SIZE, ADDR, digest, Tss2_MU_TPMT_HA_Marshal,
    sizeof(TPM2_ALG_ID) + TPM2_SHA512_DIGEST_SIZE, ADDR, digest, Tss2_MU_TPMT_HA_Marshal)
TPMU_UNMARSHAL2(TPMU_NAME,
    sizeof(TPM2_HANDLE), handle, Tss2_MU_UINT32_Unmarshal,
    sizeof(TPM2_ALG_ID) + TPM2_SHA1_DIGEST_SIZE, digest, Tss2_MU_TPMT_HA_Unmarshal,
    sizeof(TPM2_ALG_ID) + TPM2_SHA256_DIGEST_SIZE, digest, Tss2_MU_TPMT_HA_Unmarshal,
    sizeof(TPM2_ALG_ID) + TPM2_SHA384_DIGEST_SIZE, digest, Tss2_MU_TPMT_HA_Unmarshal,
    sizeof(TPM2_ALG_ID) + TPM2_SHA512_DIGEST_SIZE, digest, Tss2_MU_TPMT_HA_Unmarshal)
