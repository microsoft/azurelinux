/* SPDX-License-Identifier: BSD-2-Clause */
/*******************************************************************************
 * Copyright 2021, Fraunhofer SIT
 * All rights reserved.
 *******************************************************************************/

/**
 * The purpose of this file is to copy it into your project and
 * include it during compilation if you don't want to link against
 * libtss2-mu at compile time.
 * It will attempt to load libtss2-mu.so during runtime.
 * It will either work similarly to directly linking to libtss2-mu.so
 * at compile-time or return a NOT_IMPLEMENTED error.
 *
 * For new versions of this file, please check:
 * http://github.com/tpm2-software/tpm2-tss/tss2-dlopen
*/

#include <dlfcn.h>
#include <stdio.h>
#include <tss2/tss2_mu.h>

#define str(s) xstr(s)
#define xstr(s) #s

#ifdef ENABLE_WARN
#define WARN(str, ...) do { fprintf(stderr, "WARNING: " str "\n", ## __VA_ARGS__); } while (0)
#else /* ENABLE_WARN */
#define WARN(...) do { } while (0)
#endif /* ENABLE_WARN */

#define LIB "libtss2-mu.so.0"
static void *dlhandle = NULL;

static TSS2_RC
init_dlhandle(void)
{
    if (dlhandle)
        return TSS2_RC_SUCCESS;
    dlhandle = dlopen(LIB, RTLD_NOW | RTLD_LOCAL);
    if (!dlhandle) {
        WARN("Library " LIB " not found: %s.", dlerror());
        return TSS2_BASE_RC_NOT_IMPLEMENTED;
    }
    return TSS2_RC_SUCCESS;
}

#define MAKE_MU_BASE(typ) \
TSS2_RC Tss2_MU_ ## typ ## _Marshal ( \
    typ             src, \
    uint8_t         buffer[], \
    size_t          buffer_size, \
    size_t         *offset) \
{ \
    if (init_dlhandle() != TSS2_RC_SUCCESS) \
        return TSS2_BASE_RC_NOT_IMPLEMENTED; \
    static TSS2_RC (*sym) (typ, uint8_t [], size_t, size_t *) = NULL; \
    if (!sym) \
        sym = dlsym(dlhandle, str(Tss2_MU_ ## typ ## _Marshal)); \
    if (!sym) { \
        WARN("Function " str(Tss2_MU_ ## typ ## _Marshal) " not found."); \
        return TSS2_BASE_RC_NOT_IMPLEMENTED; \
    } \
    return sym(src, buffer, buffer_size, offset); \
} \
TSS2_RC Tss2_MU_ ## typ ## _Unmarshal ( \
    uint8_t const   buffer[], \
    size_t          buffer_size, \
    size_t         *offset, \
    typ            *dest) \
{ \
    if (init_dlhandle() != TSS2_RC_SUCCESS) \
        return TSS2_BASE_RC_NOT_IMPLEMENTED; \
    static TSS2_RC (*sym) (const uint8_t [], size_t, size_t *, typ *) = NULL; \
    if (!sym) \
        sym = dlsym(dlhandle, str(Tss2_MU_ ## typ ## _Unmarshal)); \
    if (!sym) { \
        WARN("Function " str(Tss2_MU_ ## typ ## _Unmarshal) " not found."); \
        return TSS2_BASE_RC_NOT_IMPLEMENTED; \
    } \
    return sym(buffer, buffer_size, offset, dest); \
}

#define MAKE_MU_STRUCT(typ) \
TSS2_RC Tss2_MU_ ## typ ## _Marshal ( \
    typ const      *src, \
    uint8_t         buffer[], \
    size_t          buffer_size, \
    size_t         *offset) \
{ \
    if (init_dlhandle() != TSS2_RC_SUCCESS) \
        return TSS2_BASE_RC_NOT_IMPLEMENTED; \
    static TSS2_RC (*sym) (const typ *, uint8_t [], size_t, size_t *) = NULL; \
    if (!sym) \
        sym = dlsym(dlhandle, str(Tss2_MU_ ## typ ## _Marshal)); \
    if (!sym) { \
        WARN("Function " str(Tss2_MU_ ## typ ## _Marshal) " not found."); \
        return TSS2_BASE_RC_NOT_IMPLEMENTED; \
    } \
    return sym(src, buffer, buffer_size, offset); \
} \
TSS2_RC Tss2_MU_ ## typ ## _Unmarshal ( \
    uint8_t const   buffer[], \
    size_t          buffer_size, \
    size_t         *offset, \
    typ            *dest) \
{ \
    if (init_dlhandle() != TSS2_RC_SUCCESS) \
        return TSS2_BASE_RC_NOT_IMPLEMENTED; \
    static TSS2_RC (*sym) (const uint8_t [], size_t, size_t *, typ *) = NULL; \
    if (!sym) \
        sym = dlsym(dlhandle, str(Tss2_MU_ ## typ ## _Unmarshal)); \
    if (!sym) { \
        WARN("Function " str(Tss2_MU_ ## typ ## _Unmarshal) " not found."); \
        return TSS2_BASE_RC_NOT_IMPLEMENTED; \
    } \
    return sym(buffer, buffer_size, offset, dest); \
}

#define MAKE_MU_UNION(typ) \
TSS2_RC Tss2_MU_ ## typ ## _Marshal ( \
    typ const      *src, \
    uint32_t        selector_value, \
    uint8_t         buffer[], \
    size_t          buffer_size, \
    size_t         *offset) \
{ \
    if (init_dlhandle() != TSS2_RC_SUCCESS) \
        return TSS2_BASE_RC_NOT_IMPLEMENTED; \
    static TSS2_RC (*sym) (const typ *, uint32_t, uint8_t [], size_t, size_t *) = NULL; \
    if (!sym) \
        sym = dlsym(dlhandle, str(Tss2_MU_ ## typ ## _Marshal)); \
    if (!sym) { \
        WARN("Function " str(Tss2_MU_ ## typ ## _Marshal) " not found."); \
        return TSS2_BASE_RC_NOT_IMPLEMENTED; \
    } \
    return sym(src, selector_value, buffer, buffer_size, offset); \
} \
TSS2_RC Tss2_MU_ ## typ ## _Unmarshal ( \
    uint8_t const   buffer[], \
    size_t          buffer_size, \
    size_t         *offset, \
    uint32_t        selector_value, \
    typ            *dest) \
{ \
    if (init_dlhandle() != TSS2_RC_SUCCESS) \
        return TSS2_BASE_RC_NOT_IMPLEMENTED; \
    static TSS2_RC (*sym) (const uint8_t [], size_t, size_t *, uint32_t, typ *) = NULL; \
    if (!sym) \
        sym = dlsym(dlhandle, str(Tss2_MU_ ## typ ## _Unmarshal)); \
    if (!sym) { \
        WARN("Function " str(Tss2_MU_ ## typ ## _Unmarshal) " not found."); \
        return TSS2_BASE_RC_NOT_IMPLEMENTED; \
    } \
    return sym(buffer, buffer_size, offset, selector_value, dest); \
}

MAKE_MU_BASE(INT8);
MAKE_MU_BASE(INT16);
MAKE_MU_BASE(INT32);
MAKE_MU_BASE(INT64);
MAKE_MU_BASE(UINT8);
MAKE_MU_BASE(UINT16);
MAKE_MU_BASE(UINT32);
MAKE_MU_BASE(UINT64);
MAKE_MU_BASE(TPM2_CC);
MAKE_MU_BASE(TPM2_ST);
MAKE_MU_BASE(TPMA_ALGORITHM);
MAKE_MU_BASE(TPMA_CC);
MAKE_MU_BASE(TPMA_LOCALITY);
MAKE_MU_BASE(TPMA_NV);
MAKE_MU_BASE(TPMA_OBJECT);
MAKE_MU_BASE(TPMA_PERMANENT);
MAKE_MU_BASE(TPMA_SESSION);
MAKE_MU_BASE(TPMA_STARTUP_CLEAR);
MAKE_MU_STRUCT(TPM2B_DIGEST);
MAKE_MU_STRUCT(TPM2B_ATTEST);
MAKE_MU_STRUCT(TPM2B_NAME);
MAKE_MU_STRUCT(TPM2B_MAX_NV_BUFFER);
MAKE_MU_STRUCT(TPM2B_SENSITIVE_DATA);
MAKE_MU_STRUCT(TPM2B_ECC_PARAMETER);
MAKE_MU_STRUCT(TPM2B_PUBLIC_KEY_RSA);
MAKE_MU_STRUCT(TPM2B_PRIVATE_KEY_RSA);
MAKE_MU_STRUCT(TPM2B_PRIVATE);
MAKE_MU_STRUCT(TPM2B_CONTEXT_SENSITIVE);
MAKE_MU_STRUCT(TPM2B_CONTEXT_DATA);
MAKE_MU_STRUCT(TPM2B_DATA);
MAKE_MU_STRUCT(TPM2B_SYM_KEY);
MAKE_MU_STRUCT(TPM2B_ECC_POINT);
MAKE_MU_STRUCT(TPM2B_NV_PUBLIC);
MAKE_MU_STRUCT(TPM2B_SENSITIVE);
MAKE_MU_STRUCT(TPM2B_SENSITIVE_CREATE);
MAKE_MU_STRUCT(TPM2B_CREATION_DATA);
MAKE_MU_STRUCT(TPM2B_PUBLIC);
MAKE_MU_STRUCT(TPM2B_ENCRYPTED_SECRET);
MAKE_MU_STRUCT(TPM2B_ID_OBJECT);
MAKE_MU_STRUCT(TPM2B_IV);
MAKE_MU_STRUCT(TPM2B_AUTH);
MAKE_MU_STRUCT(TPM2B_EVENT);
MAKE_MU_STRUCT(TPM2B_MAX_BUFFER);
MAKE_MU_STRUCT(TPM2B_NONCE);
MAKE_MU_STRUCT(TPM2B_OPERAND);
MAKE_MU_STRUCT(TPM2B_TIMEOUT);
MAKE_MU_STRUCT(TPM2B_TEMPLATE);
MAKE_MU_STRUCT(TPMS_CONTEXT);
MAKE_MU_STRUCT(TPMS_TIME_INFO);
MAKE_MU_STRUCT(TPMS_ECC_POINT);
MAKE_MU_STRUCT(TPMS_NV_PUBLIC);
MAKE_MU_STRUCT(TPMS_ALG_PROPERTY);
MAKE_MU_STRUCT(TPMS_TAGGED_PROPERTY);
MAKE_MU_STRUCT(TPMS_TAGGED_POLICY);
MAKE_MU_STRUCT(TPMS_CLOCK_INFO);
MAKE_MU_STRUCT(TPMS_TIME_ATTEST_INFO);
MAKE_MU_STRUCT(TPMS_CERTIFY_INFO);
MAKE_MU_STRUCT(TPMS_COMMAND_AUDIT_INFO);
MAKE_MU_STRUCT(TPMS_SESSION_AUDIT_INFO);
MAKE_MU_STRUCT(TPMS_CREATION_INFO);
MAKE_MU_STRUCT(TPMS_NV_CERTIFY_INFO);
MAKE_MU_STRUCT(TPMS_AUTH_COMMAND);
MAKE_MU_STRUCT(TPMS_AUTH_RESPONSE);
MAKE_MU_STRUCT(TPMS_SENSITIVE_CREATE);
MAKE_MU_STRUCT(TPMS_SCHEME_HASH);
MAKE_MU_STRUCT(TPMS_SCHEME_ECDAA);
MAKE_MU_STRUCT(TPMS_SCHEME_XOR);
MAKE_MU_STRUCT(TPMS_SIGNATURE_RSA);
MAKE_MU_STRUCT(TPMS_SIGNATURE_ECC);
MAKE_MU_STRUCT(TPMS_NV_PIN_COUNTER_PARAMETERS);
MAKE_MU_STRUCT(TPMS_CONTEXT_DATA);
MAKE_MU_STRUCT(TPMS_PCR_SELECT);
MAKE_MU_STRUCT(TPMS_PCR_SELECTION);
MAKE_MU_STRUCT(TPMS_TAGGED_PCR_SELECT);
MAKE_MU_STRUCT(TPMS_QUOTE_INFO);
MAKE_MU_STRUCT(TPMS_CREATION_DATA);
MAKE_MU_STRUCT(TPMS_ECC_PARMS);
MAKE_MU_STRUCT(TPMS_ATTEST);
MAKE_MU_STRUCT(TPMS_ALGORITHM_DETAIL_ECC);
MAKE_MU_STRUCT(TPMS_CAPABILITY_DATA);
MAKE_MU_STRUCT(TPMS_KEYEDHASH_PARMS);
MAKE_MU_STRUCT(TPMS_RSA_PARMS);
MAKE_MU_STRUCT(TPMS_SYMCIPHER_PARMS);
MAKE_MU_STRUCT(TPMS_AC_OUTPUT);
MAKE_MU_STRUCT(TPMS_ID_OBJECT);
MAKE_MU_STRUCT(TPMS_ACT_DATA);
MAKE_MU_STRUCT(TPMS_NV_DIGEST_CERTIFY_INFO);
MAKE_MU_STRUCT(TPML_CC);
MAKE_MU_STRUCT(TPML_CCA);
MAKE_MU_STRUCT(TPML_ALG);
MAKE_MU_STRUCT(TPML_HANDLE);
MAKE_MU_STRUCT(TPML_DIGEST);
MAKE_MU_STRUCT(TPML_DIGEST_VALUES);
MAKE_MU_STRUCT(TPML_PCR_SELECTION);
MAKE_MU_STRUCT(TPML_ALG_PROPERTY);
MAKE_MU_STRUCT(TPML_ECC_CURVE);
MAKE_MU_STRUCT(TPML_TAGGED_PCR_PROPERTY);
MAKE_MU_STRUCT(TPML_TAGGED_TPM_PROPERTY);
MAKE_MU_STRUCT(TPML_INTEL_PTT_PROPERTY);
MAKE_MU_STRUCT(TPML_AC_CAPABILITIES);
MAKE_MU_STRUCT(TPML_TAGGED_POLICY);
MAKE_MU_STRUCT(TPML_ACT_DATA);
MAKE_MU_UNION(TPMU_HA);
MAKE_MU_UNION(TPMU_CAPABILITIES);
MAKE_MU_UNION(TPMU_ATTEST);
MAKE_MU_UNION(TPMU_SYM_KEY_BITS);
MAKE_MU_UNION(TPMU_SYM_MODE);
MAKE_MU_UNION(TPMU_SIG_SCHEME);
MAKE_MU_UNION(TPMU_KDF_SCHEME);
MAKE_MU_UNION(TPMU_ASYM_SCHEME);
MAKE_MU_UNION(TPMU_SCHEME_KEYEDHASH);
MAKE_MU_UNION(TPMU_SIGNATURE);
MAKE_MU_UNION(TPMU_SENSITIVE_COMPOSITE);
MAKE_MU_UNION(TPMU_ENCRYPTED_SECRET);
MAKE_MU_UNION(TPMU_PUBLIC_PARMS);
MAKE_MU_UNION(TPMU_PUBLIC_ID);
MAKE_MU_UNION(TPMU_NAME);
MAKE_MU_STRUCT(TPMT_HA);
MAKE_MU_STRUCT(TPMT_SYM_DEF);
MAKE_MU_STRUCT(TPMT_SYM_DEF_OBJECT);
MAKE_MU_STRUCT(TPMT_KEYEDHASH_SCHEME);
MAKE_MU_STRUCT(TPMT_SIG_SCHEME);
MAKE_MU_STRUCT(TPMT_KDF_SCHEME);
MAKE_MU_STRUCT(TPMT_ASYM_SCHEME);
MAKE_MU_STRUCT(TPMT_RSA_SCHEME);
MAKE_MU_STRUCT(TPMT_RSA_DECRYPT);
MAKE_MU_STRUCT(TPMT_ECC_SCHEME);
MAKE_MU_STRUCT(TPMT_SIGNATURE);
MAKE_MU_STRUCT(TPMT_SENSITIVE);
MAKE_MU_STRUCT(TPMT_PUBLIC);
MAKE_MU_STRUCT(TPMT_PUBLIC_PARMS);
MAKE_MU_STRUCT(TPMT_TK_CREATION);
MAKE_MU_STRUCT(TPMT_TK_VERIFIED);
MAKE_MU_STRUCT(TPMT_TK_AUTH);
MAKE_MU_STRUCT(TPMT_TK_HASHCHECK);
MAKE_MU_BASE(TPM2_HANDLE);
MAKE_MU_BASE(TPMI_ALG_HASH);
MAKE_MU_BASE(BYTE);
MAKE_MU_BASE(TPM2_SE);
MAKE_MU_BASE(TPM2_NT);
MAKE_MU_STRUCT(TPMS_EMPTY);
