/* SPDX-License-Identifier: BSD-2-Clause */
/*******************************************************************************
 * Copyright 2021, Fraunhofer SIT
 * All rights reserved.
 *******************************************************************************/

/**
 * The purpose of this file is to copy it into your project and
 * include it during compilation if you don't want to link against
 * libtss2-fapi at compile time.
 * It will attempt to load libtss2-fapi.so during runtime.
 * It will either work similarly to directly linking to libtss2-fapi.so
 * at compile-time or return a NOT_IMPLEMENTED error.
 *
 * For new versions of this file, please check:
 * http://github.com/tpm2-software/tpm2-tss/tss2-dlopen
*/

#include <dlfcn.h>
#include <stdio.h>
#include <tss2/tss2_fapi.h>

#define str(s) xstr(s)
#define xstr(s) #s

#ifdef ENABLE_WARN
#define WARN(str, ...) do { fprintf(stderr, "WARNING: " str "\n", ## __VA_ARGS__); } while (0)
#else /* ENABLE_WARN */
#define WARN(...) do { } while (0)
#endif /* ENABLE_WARN */

#define LIB "libtss2-fapi.so.1"
static void *dlhandle = NULL;

static TSS2_RC
init_dlhandle(void)
{
    if (dlhandle)
        return TSS2_RC_SUCCESS;
    dlhandle = dlopen(LIB, RTLD_NOW | RTLD_LOCAL);
    if (!dlhandle) {
        WARN("Library " LIB " not found: %s.", dlerror());
        return TSS2_FAPI_RC_NOT_IMPLEMENTED;
    }
    return TSS2_RC_SUCCESS;
}

TSS2_RC
Fapi_Initialize(
    FAPI_CONTEXT  **context,
    char     const *uri)
{
    if (init_dlhandle() != TSS2_RC_SUCCESS)
        return TSS2_FAPI_RC_NOT_IMPLEMENTED;

    static TSS2_RC (*sym) (FAPI_CONTEXT **context, char const *uri) = NULL;
    if (!sym)
        sym = dlsym(dlhandle, "Fapi_Initialize");
    if (!sym) {
        WARN("Function Fapi_Initialize not found.");
        return TSS2_FAPI_RC_NOT_IMPLEMENTED;
    }

    return sym(context, uri);
}

TSS2_RC
Fapi_Initialize_Async(
    FAPI_CONTEXT  **context,
    char     const *uri)
{
    if (init_dlhandle() != TSS2_RC_SUCCESS)
        return TSS2_FAPI_RC_NOT_IMPLEMENTED;

    static TSS2_RC (*sym) (FAPI_CONTEXT **context, char const *uri) = NULL;
    if (!sym)
        sym = dlsym(dlhandle, "Fapi_Initialize_Async");
    if (!sym) {
        WARN("Function Fapi_Initialize_Async not found.");
        return TSS2_FAPI_RC_NOT_IMPLEMENTED;
    }

    return sym(context, uri);
}

TSS2_RC Fapi_Initialize_Finish(
    FAPI_CONTEXT  **context)
{
    static TSS2_RC (*sym) (FAPI_CONTEXT **context) = NULL;
    if (!sym)
        sym = dlsym(dlhandle, "Fapi_Initialize_Finish");
    if (!sym) {
        WARN("Function Fapi_Initialize_Finish not found.");
        return TSS2_FAPI_RC_NOT_IMPLEMENTED;
    }

    return sym(context);
}

void
Fapi_Finalize(FAPI_CONTEXT **ctx)
{
    if (!ctx || !*ctx)
        return;
    static TSS2_RC (*sym) (FAPI_CONTEXT **ctx) = NULL;
    if (!sym)
        sym = dlsym(dlhandle, "Fapi_Finalize");
    if (!sym) {
        WARN("Function Fapi_Finalize not found.");
        return;
    }
    sym(ctx);
}

void
Fapi_Free(void *__ptr)
{
    if (!__ptr)
        return;
    static TSS2_RC (*sym) (void *__ptr) = NULL;
    if (!sym)
        sym = dlsym(dlhandle, "Fapi_Free");
    if (!sym) {
        WARN("Function Fapi_Free not found.");
        return;
    }
    sym(__ptr);
}

#define MAKE_FAPI_0(fun) \
TSS2_RC fun (FAPI_CONTEXT *ctx) { \
    static TSS2_RC (*sym) (FAPI_CONTEXT *ctx) = NULL; \
    if (!sym) \
        sym = dlsym(dlhandle, str(fun)); \
    if (!sym) { \
        WARN("Function " str(fun) " not found."); \
        return TSS2_FAPI_RC_NOT_IMPLEMENTED; \
    } \
    return sym(ctx); \
}

#define MAKE_FAPI_1(fun, type1,parm1) \
TSS2_RC fun (FAPI_CONTEXT *ctx, type1 parm1) { \
    static TSS2_RC (*sym) (FAPI_CONTEXT *ctx, type1) = NULL; \
    if (!sym) \
        sym = dlsym(dlhandle, str(fun)); \
    if (!sym) { \
        WARN("Function " str(fun) " not found."); \
        return TSS2_FAPI_RC_NOT_IMPLEMENTED; \
    } \
    return sym(ctx, parm1); \
}

#define MAKE_FAPI_2(fun, type1,parm1, type2,parm2) \
TSS2_RC fun (FAPI_CONTEXT *ctx, type1 parm1, type2 parm2) { \
    static TSS2_RC (*sym) (FAPI_CONTEXT *ctx, type1, type2) = NULL; \
    if (!sym) \
        sym = dlsym(dlhandle, str(fun)); \
    if (!sym) { \
        WARN("Function " str(fun) " not found."); \
        return TSS2_FAPI_RC_NOT_IMPLEMENTED; \
    } \
    return sym(ctx, parm1, parm2); \
}

#define MAKE_FAPI_3(fun, type1,parm1, type2,parm2, type3,parm3) \
TSS2_RC fun (FAPI_CONTEXT *ctx, type1 parm1, type2 parm2, type3 parm3) { \
    static TSS2_RC (*sym) (FAPI_CONTEXT *ctx, type1, type2, type3) = NULL; \
    if (!sym) \
        sym = dlsym(dlhandle, str(fun)); \
    if (!sym) { \
        WARN("Function " str(fun) " not found."); \
        return TSS2_FAPI_RC_NOT_IMPLEMENTED; \
    } \
    return sym(ctx, parm1, parm2, parm3); \
}

#define MAKE_FAPI_4(fun, type1,parm1, type2,parm2, type3,parm3, type4,parm4) \
TSS2_RC fun (FAPI_CONTEXT *ctx, type1 parm1, type2 parm2, type3 parm3, type4 parm4) { \
    static TSS2_RC (*sym) (FAPI_CONTEXT *ctx, type1, type2, type3, type4) = NULL; \
    if (!sym) \
        sym = dlsym(dlhandle, str(fun)); \
    if (!sym) { \
        WARN("Function " str(fun) " not found."); \
        return TSS2_FAPI_RC_NOT_IMPLEMENTED; \
    } \
    return sym(ctx, parm1, parm2, parm3, parm4); \
}

#define MAKE_FAPI_5(fun, type1,parm1, type2,parm2, type3,parm3, type4,parm4, \
                         type5,parm5) \
TSS2_RC fun (FAPI_CONTEXT *ctx, type1 parm1, type2 parm2, type3 parm3, type4 parm4, \
                                type5 parm5) { \
    static TSS2_RC (*sym) (FAPI_CONTEXT *ctx, type1, type2, type3, type4, type5) = NULL; \
    if (!sym) \
        sym = dlsym(dlhandle, str(fun)); \
    if (!sym) { \
        WARN("Function " str(fun) " not found."); \
        return TSS2_FAPI_RC_NOT_IMPLEMENTED; \
    } \
    return sym(ctx, parm1, parm2, parm3, parm4, parm5); \
}

#define MAKE_FAPI_6(fun, type1,parm1, type2,parm2, type3,parm3, type4,parm4, \
                         type5,parm5, type6,parm6) \
TSS2_RC fun (FAPI_CONTEXT *ctx, type1 parm1, type2 parm2, type3 parm3, type4 parm4, \
                                type5 parm5, type6 parm6) { \
    static TSS2_RC (*sym) (FAPI_CONTEXT *ctx, type1, type2, type3, type4, type5, type6) = NULL; \
    if (!sym) \
        sym = dlsym(dlhandle, str(fun)); \
    if (!sym) { \
        WARN("Function " str(fun) " not found."); \
        return TSS2_FAPI_RC_NOT_IMPLEMENTED; \
    } \
    return sym(ctx, parm1, parm2, parm3, parm4, parm5, parm6); \
}

#define MAKE_FAPI_7(fun, type1,parm1, type2,parm2, type3,parm3, type4,parm4, \
                         type5,parm5, type6,parm6, type7,parm7) \
TSS2_RC fun (FAPI_CONTEXT *ctx, type1 parm1, type2 parm2, type3 parm3, type4 parm4, \
                                type5 parm5, type6 parm6, type7 parm7) { \
    static TSS2_RC (*sym) (FAPI_CONTEXT *ctx, type1, type2, type3, type4, type5, type6, type7) = NULL; \
    if (!sym) \
        sym = dlsym(dlhandle, str(fun)); \
    if (!sym) { \
        WARN("Function " str(fun) " not found."); \
        return TSS2_FAPI_RC_NOT_IMPLEMENTED; \
    } \
    return sym(ctx, parm1, parm2, parm3, parm4, parm5, parm6, parm7); \
}

#define MAKE_FAPI_8(fun, type1,parm1, type2,parm2, type3,parm3, type4,parm4, \
                         type5,parm5, type6,parm6, type7,parm7, type8,parm8) \
TSS2_RC fun (FAPI_CONTEXT *ctx, type1 parm1, type2 parm2, type3 parm3, type4 parm4, \
                                type5 parm5, type6 parm6, type7 parm7, type8 parm8) { \
    static TSS2_RC (*sym) (FAPI_CONTEXT *ctx, type1, type2, type3, type4, type5, type6, type7, type8) = NULL; \
    if (!sym) \
        sym = dlsym(dlhandle, str(fun)); \
    if (!sym) { \
        WARN("Function " str(fun) " not found."); \
        return TSS2_FAPI_RC_NOT_IMPLEMENTED; \
    } \
    return sym(ctx, parm1, parm2, parm3, parm4, parm5, parm6, parm7, parm8); \
}

#define MAKE_FAPI_9(fun, type1,parm1, type2,parm2, type3,parm3, type4,parm4, \
                         type5,parm5, type6,parm6, type7,parm7, type8,parm8, \
                         type9,parm9) \
TSS2_RC fun (FAPI_CONTEXT *ctx, type1 parm1, type2 parm2, type3 parm3, type4 parm4, \
                                type5 parm5, type6 parm6, type7 parm7, type8 parm8, \
                                type9 parm9) { \
    TSS2_RC (*sym)(FAPI_CONTEXT *ctx, type1, type2, type3, type4, type5, type6, type7, type8, \
                                      type9) = NULL; \
    if (!sym) \
        sym = dlsym(dlhandle, str(fun)); \
    if (!sym) { \
        WARN("Function " str(fun) " not found."); \
        return TSS2_FAPI_RC_NOT_IMPLEMENTED; \
    } \
    return sym(ctx, parm1, parm2, parm3, parm4, parm5, parm6, parm7, parm8, \
                    parm9); \
}

#define MAKE_FAPI_10(fun, type1,parm1, type2,parm2, type3,parm3, type4,parm4, \
                          type5,parm5, type6,parm6, type7,parm7, type8,parm8, \
                          type9,parm9, type10,parm10) \
TSS2_RC fun (FAPI_CONTEXT *ctx, type1 parm1, type2 parm2, type3 parm3, type4 parm4, \
                                type5 parm5, type6 parm6, type7 parm7, type8 parm8, \
                                type9 parm9, type10 parm10) { \
    TSS2_RC (*sym)(FAPI_CONTEXT *ctx, type1, type2, type3, type4, type5, type6, type7, type8, \
                                      type9, type10) = NULL; \
    if (!sym) \
        sym = dlsym(dlhandle, str(fun)); \
    if (!sym) { \
        WARN("Function " str(fun) " not found."); \
        return TSS2_FAPI_RC_NOT_IMPLEMENTED; \
    } \
    return sym(ctx, parm1, parm2, parm3, parm4, parm5, parm6, parm7, parm8, \
                    parm9, parm10); \
}

#define MAKE_FAPI_11(fun, type1,parm1, type2,parm2, type3,parm3, type4,parm4, \
                          type5,parm5, type6,parm6, type7,parm7, type8,parm8, \
                          type9,parm9, type10,parm10, type11,parm11) \
TSS2_RC fun (FAPI_CONTEXT *ctx, type1 parm1, type2 parm2, type3 parm3, type4 parm4, \
                                type5 parm5, type6 parm6, type7 parm7, type8 parm8, \
                                type9 parm9, type10 parm10, type11 parm11) { \
    TSS2_RC (*sym)(FAPI_CONTEXT *ctx, type1, type2, type3, type4, type5, type6, type7, type8, \
                                      type9, type10, type11) = NULL; \
    if (!sym) \
        sym = dlsym(dlhandle, str(fun)); \
    if (!sym) { \
        WARN("Function " str(fun) " not found."); \
        return TSS2_FAPI_RC_NOT_IMPLEMENTED; \
    } \
    return sym(ctx, parm1, parm2, parm3, parm4, parm5, parm6, parm7, parm8, \
                    parm9, parm10, parm11); \
}

#define MAKE_FAPI_12(fun, type1,parm1, type2,parm2, type3,parm3, type4,parm4, \
                          type5,parm5, type6,parm6, type7,parm7, type8,parm8, \
                          type9,parm9, type10,parm10, type11,parm11, type12,parm12) \
TSS2_RC fun (FAPI_CONTEXT *ctx, type1 parm1, type2 parm2, type3 parm3, type4 parm4, \
                                type5 parm5, type6 parm6, type7 parm7, type8 parm8, \
                                type9 parm9, type10 parm10, type11 parm11, type12 parm12) { \
    TSS2_RC (*sym)(FAPI_CONTEXT *ctx, type1, type2, type3, type4, type5, type6, type7, type8, \
                                      type9, type10, type11, type12) = NULL; \
    if (!sym) \
        sym = dlsym(dlhandle, str(fun)); \
    if (!sym) { \
        WARN("Function " str(fun) " not found."); \
        return TSS2_FAPI_RC_NOT_IMPLEMENTED; \
    } \
    return sym(ctx, parm1, parm2, parm3, parm4, parm5, parm6, parm7, parm8, \
                    parm9, parm10, parm11, parm12); \
}

#define MAKE_FAPI_13(fun, type1,parm1, type2,parm2, type3,parm3, type4,parm4, \
                          type5,parm5, type6,parm6, type7,parm7, type8,parm8, \
                          type9,parm9, type10,parm10, type11,parm11, type12,parm12, \
                          type13,parm13) \
TSS2_RC fun (FAPI_CONTEXT *ctx, type1 parm1, type2 parm2, type3 parm3, type4 parm4, \
                                type5 parm5, type6 parm6, type7 parm7, type8 parm8, \
                                type9 parm9, type10 parm10, type11 parm11, type12 parm12, \
                                type13 parm13) { \
    TSS2_RC (*sym)(FAPI_CONTEXT *ctx, type1, type2, type3, type4, type5, type6, type7, type8, \
                                      type9, type10, type11, type12, type13) = NULL; \
    if (!sym) \
        sym = dlsym(dlhandle, str(fun)); \
    if (!sym) { \
        WARN("Function " str(fun) " not found."); \
        return TSS2_FAPI_RC_NOT_IMPLEMENTED; \
    } \
    return sym(ctx, parm1, parm2, parm3, parm4, parm5, parm6, parm7, parm8, \
                    parm9, parm10, parm11, parm12, parm13); \
}

MAKE_FAPI_1(Fapi_GetTcti,
    TSS2_TCTI_CONTEXT **, tcti);
MAKE_FAPI_2(Fapi_GetPollHandles,
    FAPI_POLL_HANDLE **, handles,
    size_t *, num_handles);
MAKE_FAPI_1(Fapi_GetInfo,
    char **, info);
MAKE_FAPI_0(Fapi_GetInfo_Async);
MAKE_FAPI_1(Fapi_GetInfo_Finish,
    char **, info);
MAKE_FAPI_3(Fapi_Provision,
    char const *, authValueEh,
    char const *, authValueSh,
    char const *, authValueLockout);
MAKE_FAPI_3(Fapi_Provision_Async,
    char const *, authValueEh,
    char const *, authValueSh,
    char const *, authValueLockout);
MAKE_FAPI_0(Fapi_Provision_Finish);
MAKE_FAPI_2(Fapi_GetPlatformCertificates,
    uint8_t **, certificates,
    size_t *, certificatesSize);
MAKE_FAPI_0(Fapi_GetPlatformCertificates_Async);
MAKE_FAPI_2(Fapi_GetPlatformCertificates_Finish,
    uint8_t **, certificates,
    size_t *, certificatesSize);
MAKE_FAPI_2(Fapi_GetRandom,
    size_t, numBytes,
    uint8_t **, data);
MAKE_FAPI_1(Fapi_GetRandom_Async,
    size_t, numBytes);
MAKE_FAPI_1(Fapi_GetRandom_Finish,
    uint8_t **, data);
MAKE_FAPI_2(Fapi_Import,
    char const *, path,
    char const *, importData);
MAKE_FAPI_2(Fapi_Import_Async,
    char const *, path,
    char const *, importData);
MAKE_FAPI_0(Fapi_Import_Finish);
MAKE_FAPI_2(Fapi_List,
    char const *, searchPath,
    char **, pathList);
MAKE_FAPI_1(Fapi_List_Async,
    char const *, searchPath);
MAKE_FAPI_1(Fapi_List_Finish,
    char **, pathList);
MAKE_FAPI_1(Fapi_Delete,
    char const *, path);
MAKE_FAPI_1(Fapi_Delete_Async,
    char const *, path);
MAKE_FAPI_0(Fapi_Delete_Finish);
MAKE_FAPI_4(Fapi_GetEsysBlob,
    char const *, path,
    uint8_t *, type,
    uint8_t **, data,
    size_t *, length);
MAKE_FAPI_1(Fapi_GetEsysBlob_Async,
    char const *, path);
MAKE_FAPI_3(Fapi_GetEsysBlob_Finish,
    uint8_t *, type,
    uint8_t **, data,
    size_t *, length);
MAKE_FAPI_2(Fapi_ChangeAuth,
    char const *, entityPath,
    char const *, authValue);
MAKE_FAPI_2(Fapi_ChangeAuth_Async,
    char const *, entityPath,
    char const *, authValue);
MAKE_FAPI_0(Fapi_ChangeAuth_Finish);
MAKE_FAPI_2(Fapi_SetDescription,
    char const *, path,
    char const *, description);
MAKE_FAPI_2(Fapi_SetDescription_Async,
    char const *, path,
    char const *, description);
MAKE_FAPI_0(Fapi_SetDescription_Finish);
MAKE_FAPI_2(Fapi_GetDescription,
    char const *, path,
    char **, description);
MAKE_FAPI_1(Fapi_GetDescription_Async,
    char const *, path);
MAKE_FAPI_1(Fapi_GetDescription_Finish,
    char **, description);
MAKE_FAPI_3(Fapi_SetAppData,
    char const *, path,
    uint8_t const *, appData,
    size_t, appDataSize);
MAKE_FAPI_3(Fapi_SetAppData_Async,
    char const *, path,
    uint8_t const *, appData,
    size_t, appDataSize);
MAKE_FAPI_0(Fapi_SetAppData_Finish);
MAKE_FAPI_3(Fapi_GetAppData,
    char const *, path,
    uint8_t **, appData,
    size_t *, appDataSize);
MAKE_FAPI_1(Fapi_GetAppData_Async,
    char const *, path);
MAKE_FAPI_2(Fapi_GetAppData_Finish,
    uint8_t **, appData,
    size_t *, appDataSize);
MAKE_FAPI_6(Fapi_GetTpmBlobs,
    char const *, path,
    uint8_t **, tpm2bPublic,
    size_t *, tpm2bPublicSize,
    uint8_t **, tpm2bPrivate,
    size_t *, tpm2bPrivateSize,
    char **, policy);
MAKE_FAPI_1(Fapi_GetTpmBlobs_Async,
    char const *, path);
MAKE_FAPI_5(Fapi_GetTpmBlobs_Finish,
    uint8_t **, tpm2bPublic,
    size_t *, tpm2bPublicSize,
    uint8_t **, tpm2bPrivate,
    size_t *, tpm2bPrivateSize,
    char **, policy);
MAKE_FAPI_4(Fapi_CreateKey,
    char const *, path,
    char const *, type,
    char const *, policyPath,
    char const *, authValue);
MAKE_FAPI_4(Fapi_CreateKey_Async,
    char const *, path,
    char const *, type,
    char const *, policyPath,
    char const *, authValue);
MAKE_FAPI_0(Fapi_CreateKey_Finish);
MAKE_FAPI_8(Fapi_Sign,
    char const *, keyPath,
    char const *, padding,
    uint8_t const *, digest,
    size_t, digestSize,
    uint8_t **, signature,
    size_t *, signatureSize,
    char **, publicKey,
    char **, certificate);
MAKE_FAPI_4(Fapi_Sign_Async,
    char const *, keyPath,
    char const *, padding,
    uint8_t const *, digest,
    size_t, digestSize);
MAKE_FAPI_4(Fapi_Sign_Finish,
    uint8_t **, signature,
    size_t *, signatureSize,
    char **, publicKey,
    char **, certificate);
MAKE_FAPI_5(Fapi_VerifySignature,
    char const *, keyPath,
    uint8_t const *, digest,
    size_t, digestSize,
    uint8_t const *, signature,
    size_t, signatureSize);
MAKE_FAPI_5(Fapi_VerifySignature_Async,
    char const *, keyPath,
    uint8_t const *, digest,
    size_t, digestSize,
    uint8_t const *, signature,
    size_t, signatureSize);
MAKE_FAPI_0(Fapi_VerifySignature_Finish);
MAKE_FAPI_5(Fapi_Encrypt,
    char const *, keyPath,
    uint8_t const *, plainText,
    size_t, plainTextSize,
    uint8_t **, cipherText,
    size_t *, cipherTextSize);
MAKE_FAPI_3(Fapi_Encrypt_Async,
    char const *, keyPath,
    uint8_t const *, plainText,
    size_t, plainTextSize);
MAKE_FAPI_2(Fapi_Encrypt_Finish,
    uint8_t **, cipherText,
    size_t *, cipherTextSize );
MAKE_FAPI_5(Fapi_Decrypt,
    char const *, keyPath,
    uint8_t const *, cipherText,
    size_t, cipherTextSize,
    uint8_t **, plainText,
    size_t *, plainTextSize);
MAKE_FAPI_3(Fapi_Decrypt_Async,
    char const *, keyPath,
    uint8_t const *, cipherText,
    size_t, cipherTextSize);
MAKE_FAPI_2(Fapi_Decrypt_Finish,
    uint8_t **, plainText,
    size_t *, plainTextSize);
MAKE_FAPI_2(Fapi_SetCertificate,
    char const *, path,
    char const *, x509certData);
MAKE_FAPI_2(Fapi_SetCertificate_Async,
    char const *, path,
    char const *, x509certData);
MAKE_FAPI_0(Fapi_SetCertificate_Finish);
MAKE_FAPI_2(Fapi_GetCertificate,
    char const *, path,
    char **, x509certData);
MAKE_FAPI_1(Fapi_GetCertificate_Async,
    char const *, path);
MAKE_FAPI_1(Fapi_GetCertificate_Finish,
    char **, x509certData);
MAKE_FAPI_3(Fapi_ExportKey,
    char const *, pathOfKeyToDuplicate,
    char const *, pathToPublicKeyOfNewParent,
    char **, exportedData);
MAKE_FAPI_2(Fapi_ExportKey_Async,
    char const *, pathOfKeyToDuplicate,
    char const *, pathToPublicKeyOfNewParent);
MAKE_FAPI_1(Fapi_ExportKey_Finish,
    char **, exportedData);
MAKE_FAPI_6(Fapi_CreateSeal,
    char const *, path,
    char const *, type,
    size_t, size,
    char const *, policyPath,
    char const *, authValue,
    uint8_t const *, data);
MAKE_FAPI_6(Fapi_CreateSeal_Async,
    char const *, path,
    char const *, type,
    size_t, size,
    char const *, policyPath,
    char const *, authValue,
    uint8_t const *, data);
MAKE_FAPI_0(Fapi_CreateSeal_Finish);
MAKE_FAPI_3(Fapi_Unseal,
    char const *, path,
    uint8_t **, data,
    size_t *, size);
MAKE_FAPI_1(Fapi_Unseal_Async,
    char const *, path);
MAKE_FAPI_2(Fapi_Unseal_Finish,
    uint8_t **, data,
    size_t *, size);
MAKE_FAPI_2(Fapi_ExportPolicy,
    char const *, path,
    char **, jsonPolicy);
MAKE_FAPI_1(Fapi_ExportPolicy_Async,
    char const *, path);
MAKE_FAPI_1(Fapi_ExportPolicy_Finish,
    char **, jsonPolicy);
MAKE_FAPI_4(Fapi_AuthorizePolicy,
    char const *, policyPath,
    char const *, keyPath,
    uint8_t const *, policyRef,
    size_t, policyRefSize);
MAKE_FAPI_4(Fapi_AuthorizePolicy_Async,
    char const *, policyPath,
    char const *, keyPath,
    uint8_t const *, policyRef,
    size_t, policyRefSize);
MAKE_FAPI_0(Fapi_AuthorizePolicy_Finish);
MAKE_FAPI_2(Fapi_WriteAuthorizeNv,
    char const *, nvPath,
    char const *, policyPath);
MAKE_FAPI_2(Fapi_WriteAuthorizeNv_Async,
    char const *, nvPath,
    char const *, policyPath);
MAKE_FAPI_0(Fapi_WriteAuthorizeNv_Finish);
MAKE_FAPI_4(Fapi_PcrRead,
    uint32_t, pcrIndex,
    uint8_t **, pcrValue,
    size_t *, pcrValueSize,
    char **, pcrLog);
MAKE_FAPI_1(Fapi_PcrRead_Async,
    uint32_t, pcrIndex);
MAKE_FAPI_3(Fapi_PcrRead_Finish,
    uint8_t **, pcrValue,
    size_t *, pcrValueSize,
    char **, pcrLog);
MAKE_FAPI_4(Fapi_PcrExtend,
    uint32_t, pcr,
    uint8_t const *, data,
    size_t, dataSize,
    char const *, logData);
MAKE_FAPI_4(Fapi_PcrExtend_Async,
    uint32_t, pcr,
    uint8_t const *, data,
    size_t, dataSize,
    char const *, logData);
MAKE_FAPI_0(Fapi_PcrExtend_Finish);
MAKE_FAPI_11(Fapi_Quote,
    uint32_t *, pcrList,
    size_t, pcrListSize,
    char const *, keyPath,
    char const *, quoteType,
    uint8_t const *, qualifyingData,
    size_t, qualifyingDataSize,
    char **, quoteInfo,
    uint8_t **, signature,
    size_t *, signatureSize,
    char **, pcrLog,
    char **, certificate);
MAKE_FAPI_6(Fapi_Quote_Async,
    uint32_t *, pcrList,
    size_t, pcrListSize,
    char const *, keyPath,
    char const *, quoteType,
    uint8_t const *, qualifyingData,
    size_t, qualifyingDataSize);
MAKE_FAPI_5(Fapi_Quote_Finish,
    char **, quoteInfo,
    uint8_t **, signature,
    size_t *, signatureSize,
    char **, pcrLog,
    char **, certificate);
MAKE_FAPI_7(Fapi_VerifyQuote,
    char const *, publicKeyPath,
    uint8_t const *, qualifyingData,
    size_t, qualifyingDataSize,
    char const *, quoteInfo,
    uint8_t const *, signature,
    size_t, signatureSize,
    char const *, pcrLog);
MAKE_FAPI_7(Fapi_VerifyQuote_Async,
    char const *, publicKeyPath,
    uint8_t const *, qualifyingData,
    size_t, qualifyingDataSize,
    char const *, quoteInfo,
    uint8_t const *, signature,
    size_t, signatureSize,
    char const *, pcrLog);
MAKE_FAPI_0(Fapi_VerifyQuote_Finish);
MAKE_FAPI_5(Fapi_CreateNv,
    char const *, path,
    char const *, type,
    size_t, size,
    char const *, policyPath,
    char const *, authValue);
MAKE_FAPI_5(Fapi_CreateNv_Async,
    char const *, path,
    char const *, type,
    size_t, size,
    char const *, policyPath,
    char const *, authValue);
MAKE_FAPI_0(Fapi_CreateNv_Finish);
MAKE_FAPI_4(Fapi_NvRead,
    char const *, path,
    uint8_t **, data,
    size_t *, size,
    char **, logData);
MAKE_FAPI_1(Fapi_NvRead_Async,
    char const *, path);
MAKE_FAPI_3(Fapi_NvRead_Finish,
    uint8_t **, data,
    size_t *, size,
    char **, logData);
MAKE_FAPI_3(Fapi_NvWrite,
    char const *, path,
    uint8_t const *, data,
    size_t, size);
MAKE_FAPI_3(Fapi_NvWrite_Async,
    char const *, path,
    uint8_t const *, data,
    size_t, size);
MAKE_FAPI_0(Fapi_NvWrite_Finish);
MAKE_FAPI_4(Fapi_NvExtend,
    char const *, path,
    uint8_t const *, data,
    size_t, size,
    char const *, logData);
MAKE_FAPI_4(Fapi_NvExtend_Async,
    char const *, path,
    uint8_t const *, data,
    size_t, size,
    char const *, logData);
MAKE_FAPI_0(Fapi_NvExtend_Finish);
MAKE_FAPI_1(Fapi_NvIncrement,
    char const *, path);
MAKE_FAPI_1(Fapi_NvIncrement_Async,
    char const *, path);
MAKE_FAPI_0(Fapi_NvIncrement_Finish);
MAKE_FAPI_2(Fapi_NvSetBits,
    char const *, path,
    uint64_t, bitmap);
MAKE_FAPI_2(Fapi_NvSetBits_Async,
    char const *, path,
    uint64_t, bitmap);
MAKE_FAPI_0(Fapi_NvSetBits_Finish);
MAKE_FAPI_2(Fapi_SetAuthCB,
    Fapi_CB_Auth, callback,
    void *, userData);
MAKE_FAPI_2(Fapi_SetBranchCB,
    Fapi_CB_Branch, callback,
    void *, userData);
MAKE_FAPI_2(Fapi_SetSignCB,
    Fapi_CB_Sign, callback,
    void *, userData);
MAKE_FAPI_2(Fapi_SetPolicyActionCB,
    Fapi_CB_PolicyAction, callback,
    void *, userData);
