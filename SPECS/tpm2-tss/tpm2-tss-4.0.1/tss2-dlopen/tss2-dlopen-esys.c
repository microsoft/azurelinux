/* SPDX-License-Identifier: BSD-2-Clause */
/*******************************************************************************
 * Copyright 2021, Fraunhofer SIT
 * All rights reserved.
 *******************************************************************************/

/**
 * The purpose of this file is to copy it into your project and
 * include it during compilation if you don't want to link against
 * libtss2-esys at compile time.
 * It will attempt to load libtss2-esys.so during runtime.
 * It will either work similarly to directly linking to libtss2-esys.so
 * at compile-time or return a NOT_IMPLEMENTED error.
 *
 * For new versions of this file, please check:
 * http://github.com/tpm2-software/tpm2-tss/tss2-dlopen
*/

#include <dlfcn.h>
#include <stdio.h>
#include <tss2/tss2_esys.h>

#define str(s) xstr(s)
#define xstr(s) #s

#ifdef ENABLE_WARN
#define WARN(str, ...) do { fprintf(stderr, "WARNING: " str "\n", ## __VA_ARGS__); } while (0)
#else /* ENABLE_WARN */
#define WARN(...) do { } while (0)
#endif /* ENABLE_WARN */

#define LIB "libtss2-esys.so.0"
static void *dlhandle = NULL;

static TSS2_RC
init_dlhandle(void)
{
    if (dlhandle)
        return TSS2_RC_SUCCESS;
    dlhandle = dlopen(LIB, RTLD_NOW | RTLD_LOCAL);
    if (!dlhandle) {
        WARN("Library " LIB " not found: %s.", dlerror());
        return TSS2_ESYS_RC_NOT_IMPLEMENTED;
    }
    return TSS2_RC_SUCCESS;
}

TSS2_RC
Esys_Initialize(
    ESYS_CONTEXT **esys_context,
    TSS2_TCTI_CONTEXT *tcti,
    TSS2_ABI_VERSION *abiVersion)
{
    if (init_dlhandle() != TSS2_RC_SUCCESS)
        return TSS2_ESYS_RC_NOT_IMPLEMENTED;

    static TSS2_RC (*sym) (ESYS_CONTEXT **esys_context, TSS2_TCTI_CONTEXT *tcti, TSS2_ABI_VERSION *abiVersion) = NULL;
    if (!sym)
        sym = dlsym(dlhandle, "Esys_Initialize");
    if (!sym) {
        WARN("Function Esys_Initialize not found.");
        return TSS2_ESYS_RC_NOT_IMPLEMENTED;
    }

    return sym(esys_context, tcti, abiVersion);
}

void
Esys_Finalize(ESYS_CONTEXT **ctx)
{
    if (!ctx || !*ctx)
        return;
    static TSS2_RC (*sym) (ESYS_CONTEXT **ctx) = NULL;
    if (!sym)
        sym = dlsym(dlhandle, "Esys_Finalize");
    if (!sym) {
        WARN("Function Esys_Finalize not found.");
        return;
    }
    sym(ctx);
}

void
Esys_Free(void *__ptr)
{
    if (!__ptr)
        return;
    static TSS2_RC (*sym) (void *__ptr) = NULL;
    if (!sym)
        sym = dlsym(dlhandle, "Esys_Free");
    if (!sym) {
        WARN("Function Esys_Free not found.");
        return;
    }
    sym(__ptr);
}

#define MAKE_ESYS_0(fun) \
TSS2_RC fun (ESYS_CONTEXT *ctx) { \
    static TSS2_RC (*sym) (ESYS_CONTEXT *ctx) = NULL; \
    if (!sym) \
        sym = dlsym(dlhandle, str(fun)); \
    if (!sym) { \
        WARN("Function " str(fun) " not found."); \
        return TSS2_ESYS_RC_NOT_IMPLEMENTED; \
    } \
    return sym(ctx); \
}

#define MAKE_ESYS_1(fun, type1,parm1) \
TSS2_RC fun (ESYS_CONTEXT *ctx, type1 parm1) { \
    static TSS2_RC (*sym) (ESYS_CONTEXT *ctx, type1) = NULL; \
    if (!sym) \
        sym = dlsym(dlhandle, str(fun)); \
    if (!sym) { \
        WARN("Function " str(fun) " not found."); \
        return TSS2_ESYS_RC_NOT_IMPLEMENTED; \
    } \
    return sym(ctx, parm1); \
}

#define MAKE_ESYS_2(fun, type1,parm1, type2,parm2) \
TSS2_RC fun (ESYS_CONTEXT *ctx, type1 parm1, type2 parm2) { \
    static TSS2_RC (*sym) (ESYS_CONTEXT *ctx, type1, type2) = NULL; \
    if (!sym) \
        sym = dlsym(dlhandle, str(fun)); \
    if (!sym) { \
        WARN("Function " str(fun) " not found."); \
        return TSS2_ESYS_RC_NOT_IMPLEMENTED; \
    } \
    return sym(ctx, parm1, parm2); \
}

#define MAKE_ESYS_3(fun, type1,parm1, type2,parm2, type3,parm3) \
TSS2_RC fun (ESYS_CONTEXT *ctx, type1 parm1, type2 parm2, type3 parm3) { \
    static TSS2_RC (*sym) (ESYS_CONTEXT *ctx, type1, type2, type3) = NULL; \
    if (!sym) \
        sym = dlsym(dlhandle, str(fun)); \
    if (!sym) { \
        WARN("Function " str(fun) " not found."); \
        return TSS2_ESYS_RC_NOT_IMPLEMENTED; \
    } \
    return sym(ctx, parm1, parm2, parm3); \
}

#define MAKE_ESYS_4(fun, type1,parm1, type2,parm2, type3,parm3, type4,parm4) \
TSS2_RC fun (ESYS_CONTEXT *ctx, type1 parm1, type2 parm2, type3 parm3, type4 parm4) { \
    static TSS2_RC (*sym) (ESYS_CONTEXT *ctx, type1, type2, type3, type4) = NULL; \
    if (!sym) \
        sym = dlsym(dlhandle, str(fun)); \
    if (!sym) { \
        WARN("Function " str(fun) " not found."); \
        return TSS2_ESYS_RC_NOT_IMPLEMENTED; \
    } \
    return sym(ctx, parm1, parm2, parm3, parm4); \
}

#define MAKE_ESYS_5(fun, type1,parm1, type2,parm2, type3,parm3, type4,parm4, \
                         type5,parm5) \
TSS2_RC fun (ESYS_CONTEXT *ctx, type1 parm1, type2 parm2, type3 parm3, type4 parm4, \
                                type5 parm5) { \
    static TSS2_RC (*sym) (ESYS_CONTEXT *ctx, type1, type2, type3, type4, type5) = NULL; \
    if (!sym) \
        sym = dlsym(dlhandle, str(fun)); \
    if (!sym) { \
        WARN("Function " str(fun) " not found."); \
        return TSS2_ESYS_RC_NOT_IMPLEMENTED; \
    } \
    return sym(ctx, parm1, parm2, parm3, parm4, parm5); \
}

#define MAKE_ESYS_6(fun, type1,parm1, type2,parm2, type3,parm3, type4,parm4, \
                         type5,parm5, type6,parm6) \
TSS2_RC fun (ESYS_CONTEXT *ctx, type1 parm1, type2 parm2, type3 parm3, type4 parm4, \
                                type5 parm5, type6 parm6) { \
    static TSS2_RC (*sym) (ESYS_CONTEXT *ctx, type1, type2, type3, type4, type5, type6) = NULL; \
    if (!sym) \
        sym = dlsym(dlhandle, str(fun)); \
    if (!sym) { \
        WARN("Function " str(fun) " not found."); \
        return TSS2_ESYS_RC_NOT_IMPLEMENTED; \
    } \
    return sym(ctx, parm1, parm2, parm3, parm4, parm5, parm6); \
}

#define MAKE_ESYS_7(fun, type1,parm1, type2,parm2, type3,parm3, type4,parm4, \
                         type5,parm5, type6,parm6, type7,parm7) \
TSS2_RC fun (ESYS_CONTEXT *ctx, type1 parm1, type2 parm2, type3 parm3, type4 parm4, \
                                type5 parm5, type6 parm6, type7 parm7) { \
    static TSS2_RC (*sym) (ESYS_CONTEXT *ctx, type1, type2, type3, type4, type5, type6, type7) = NULL; \
    if (!sym) \
        sym = dlsym(dlhandle, str(fun)); \
    if (!sym) { \
        WARN("Function " str(fun) " not found."); \
        return TSS2_ESYS_RC_NOT_IMPLEMENTED; \
    } \
    return sym(ctx, parm1, parm2, parm3, parm4, parm5, parm6, parm7); \
}

#define MAKE_ESYS_8(fun, type1,parm1, type2,parm2, type3,parm3, type4,parm4, \
                         type5,parm5, type6,parm6, type7,parm7, type8,parm8) \
TSS2_RC fun (ESYS_CONTEXT *ctx, type1 parm1, type2 parm2, type3 parm3, type4 parm4, \
                                type5 parm5, type6 parm6, type7 parm7, type8 parm8) { \
    static TSS2_RC (*sym) (ESYS_CONTEXT *ctx, type1, type2, type3, type4, type5, type6, type7, type8) = NULL; \
    if (!sym) \
        sym = dlsym(dlhandle, str(fun)); \
    if (!sym) { \
        WARN("Function " str(fun) " not found."); \
        return TSS2_ESYS_RC_NOT_IMPLEMENTED; \
    } \
    return sym(ctx, parm1, parm2, parm3, parm4, parm5, parm6, parm7, parm8); \
}

#define MAKE_ESYS_9(fun, type1,parm1, type2,parm2, type3,parm3, type4,parm4, \
                         type5,parm5, type6,parm6, type7,parm7, type8,parm8, \
                         type9,parm9) \
TSS2_RC fun (ESYS_CONTEXT *ctx, type1 parm1, type2 parm2, type3 parm3, type4 parm4, \
                                type5 parm5, type6 parm6, type7 parm7, type8 parm8, \
                                type9 parm9) { \
    TSS2_RC (*sym)(ESYS_CONTEXT *ctx, type1, type2, type3, type4, type5, type6, type7, type8, \
                                      type9) = NULL; \
    if (!sym) \
        sym = dlsym(dlhandle, str(fun)); \
    if (!sym) { \
        WARN("Function " str(fun) " not found."); \
        return TSS2_ESYS_RC_NOT_IMPLEMENTED; \
    } \
    return sym(ctx, parm1, parm2, parm3, parm4, parm5, parm6, parm7, parm8, \
                    parm9); \
}

#define MAKE_ESYS_10(fun, type1,parm1, type2,parm2, type3,parm3, type4,parm4, \
                          type5,parm5, type6,parm6, type7,parm7, type8,parm8, \
                          type9,parm9, type10,parm10) \
TSS2_RC fun (ESYS_CONTEXT *ctx, type1 parm1, type2 parm2, type3 parm3, type4 parm4, \
                                type5 parm5, type6 parm6, type7 parm7, type8 parm8, \
                                type9 parm9, type10 parm10) { \
    TSS2_RC (*sym)(ESYS_CONTEXT *ctx, type1, type2, type3, type4, type5, type6, type7, type8, \
                                      type9, type10) = NULL; \
    if (!sym) \
        sym = dlsym(dlhandle, str(fun)); \
    if (!sym) { \
        WARN("Function " str(fun) " not found."); \
        return TSS2_ESYS_RC_NOT_IMPLEMENTED; \
    } \
    return sym(ctx, parm1, parm2, parm3, parm4, parm5, parm6, parm7, parm8, \
                    parm9, parm10); \
}

#define MAKE_ESYS_11(fun, type1,parm1, type2,parm2, type3,parm3, type4,parm4, \
                          type5,parm5, type6,parm6, type7,parm7, type8,parm8, \
                          type9,parm9, type10,parm10, type11,parm11) \
TSS2_RC fun (ESYS_CONTEXT *ctx, type1 parm1, type2 parm2, type3 parm3, type4 parm4, \
                                type5 parm5, type6 parm6, type7 parm7, type8 parm8, \
                                type9 parm9, type10 parm10, type11 parm11) { \
    TSS2_RC (*sym)(ESYS_CONTEXT *ctx, type1, type2, type3, type4, type5, type6, type7, type8, \
                                      type9, type10, type11) = NULL; \
    if (!sym) \
        sym = dlsym(dlhandle, str(fun)); \
    if (!sym) { \
        WARN("Function " str(fun) " not found."); \
        return TSS2_ESYS_RC_NOT_IMPLEMENTED; \
    } \
    return sym(ctx, parm1, parm2, parm3, parm4, parm5, parm6, parm7, parm8, \
                    parm9, parm10, parm11); \
}

#define MAKE_ESYS_12(fun, type1,parm1, type2,parm2, type3,parm3, type4,parm4, \
                          type5,parm5, type6,parm6, type7,parm7, type8,parm8, \
                          type9,parm9, type10,parm10, type11,parm11, type12,parm12) \
TSS2_RC fun (ESYS_CONTEXT *ctx, type1 parm1, type2 parm2, type3 parm3, type4 parm4, \
                                type5 parm5, type6 parm6, type7 parm7, type8 parm8, \
                                type9 parm9, type10 parm10, type11 parm11, type12 parm12) { \
    TSS2_RC (*sym)(ESYS_CONTEXT *ctx, type1, type2, type3, type4, type5, type6, type7, type8, \
                                      type9, type10, type11, type12) = NULL; \
    if (!sym) \
        sym = dlsym(dlhandle, str(fun)); \
    if (!sym) { \
        WARN("Function " str(fun) " not found."); \
        return TSS2_ESYS_RC_NOT_IMPLEMENTED; \
    } \
    return sym(ctx, parm1, parm2, parm3, parm4, parm5, parm6, parm7, parm8, \
                    parm9, parm10, parm11, parm12); \
}

#define MAKE_ESYS_13(fun, type1,parm1, type2,parm2, type3,parm3, type4,parm4, \
                          type5,parm5, type6,parm6, type7,parm7, type8,parm8, \
                          type9,parm9, type10,parm10, type11,parm11, type12,parm12, \
                          type13,parm13) \
TSS2_RC fun (ESYS_CONTEXT *ctx, type1 parm1, type2 parm2, type3 parm3, type4 parm4, \
                                type5 parm5, type6 parm6, type7 parm7, type8 parm8, \
                                type9 parm9, type10 parm10, type11 parm11, type12 parm12, \
                                type13 parm13) { \
    TSS2_RC (*sym)(ESYS_CONTEXT *ctx, type1, type2, type3, type4, type5, type6, type7, type8, \
                                      type9, type10, type11, type12, type13) = NULL; \
    if (!sym) \
        sym = dlsym(dlhandle, str(fun)); \
    if (!sym) { \
        WARN("Function " str(fun) " not found."); \
        return TSS2_ESYS_RC_NOT_IMPLEMENTED; \
    } \
    return sym(ctx, parm1, parm2, parm3, parm4, parm5, parm6, parm7, parm8, \
                    parm9, parm10, parm11, parm12, parm13); \
}

MAKE_ESYS_1(Esys_GetTcti,
    TSS2_TCTI_CONTEXT **, tcti);
MAKE_ESYS_2(Esys_GetPollHandles,
    TSS2_TCTI_POLL_HANDLE **, handles,
    size_t *, count);
MAKE_ESYS_1(Esys_SetTimeout,
    int32_t, timeout);
MAKE_ESYS_3(Esys_TR_Serialize,
    ESYS_TR, object,
    uint8_t **, buffer,
    size_t *, buffer_size);
MAKE_ESYS_3(Esys_TR_Deserialize,
    uint8_t const *, buffer,
    size_t, buffer_size,
    ESYS_TR *, esys_handle);
MAKE_ESYS_4(Esys_TR_FromTPMPublic_Async,
    TPM2_HANDLE, tpm_handle,
    ESYS_TR, optionalSession1,
    ESYS_TR, optionalSession2,
    ESYS_TR, optionalSession3);
MAKE_ESYS_1(Esys_TR_FromTPMPublic_Finish,
    ESYS_TR *, object);
MAKE_ESYS_5(Esys_TR_FromTPMPublic,
    TPM2_HANDLE, tpm_handle,
    ESYS_TR, optionalSession1,
    ESYS_TR, optionalSession2,
    ESYS_TR, optionalSession3,
    ESYS_TR *, object);
MAKE_ESYS_1(Esys_TR_Close,
    ESYS_TR *, rsrc_handle);
MAKE_ESYS_2(Esys_TR_SetAuth,
    ESYS_TR, handle,
    TPM2B_AUTH const *, authValue);
MAKE_ESYS_2(Esys_TR_GetName,
    ESYS_TR, handle,
    TPM2B_NAME **, name);
MAKE_ESYS_2(Esys_TRSess_GetAttributes,
    ESYS_TR, session,
    TPMA_SESSION *, flags);
MAKE_ESYS_3(Esys_TRSess_SetAttributes,
    ESYS_TR, session,
    TPMA_SESSION, flags,
    TPMA_SESSION, mask);
MAKE_ESYS_2(Esys_TRSess_GetNonceTPM,
    ESYS_TR, session,
    TPM2B_NONCE **, nonceTPM);
MAKE_ESYS_2(Esys_TR_GetTpmHandle,
    ESYS_TR, esys_handle,
    TPM2_HANDLE *, tpm_handle);
MAKE_ESYS_2(Esys_TRSess_GetAuthRequired,
    ESYS_TR, esys_handle,
    TPMI_YES_NO *, auth_needed);
MAKE_ESYS_1(Esys_Startup,
    TPM2_SU, startupType);
MAKE_ESYS_1(Esys_Startup_Async,
    TPM2_SU, startupType);
MAKE_ESYS_0(Esys_Startup_Finish);
MAKE_ESYS_4(Esys_Shutdown,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    TPM2_SU, shutdownType);
MAKE_ESYS_4(Esys_Shutdown_Async,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    TPM2_SU, shutdownType);
MAKE_ESYS_0(Esys_Shutdown_Finish);
MAKE_ESYS_4(Esys_SelfTest,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    TPMI_YES_NO, fullTest);
MAKE_ESYS_4(Esys_SelfTest_Async,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    TPMI_YES_NO, fullTest);
MAKE_ESYS_0(Esys_SelfTest_Finish);
MAKE_ESYS_5(Esys_IncrementalSelfTest,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPML_ALG *, toTest,
    TPML_ALG **, toDoList);
MAKE_ESYS_4(Esys_IncrementalSelfTest_Async,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPML_ALG *, toTest);
MAKE_ESYS_1(Esys_IncrementalSelfTest_Finish,
    TPML_ALG **, toDoList);
MAKE_ESYS_5(Esys_GetTestResult,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    TPM2B_MAX_BUFFER **, outData,
    TPM2_RC *, testResult);
MAKE_ESYS_3(Esys_GetTestResult_Async,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3);
MAKE_ESYS_2(Esys_GetTestResult_Finish,
    TPM2B_MAX_BUFFER **, outData,
    TPM2_RC *, testResult);
MAKE_ESYS_10(Esys_StartAuthSession,
    ESYS_TR, tpmKey,
    ESYS_TR, bind,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_NONCE *, nonceCaller,
    TPM2_SE, sessionType,
    const TPMT_SYM_DEF *, symmetric,
    TPMI_ALG_HASH, authHash,
    ESYS_TR *, sessionHandle);
MAKE_ESYS_9(Esys_StartAuthSession_Async,
    ESYS_TR, tpmKey,
    ESYS_TR, bind,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_NONCE *, nonceCaller,
    TPM2_SE, sessionType,
    const TPMT_SYM_DEF *, symmetric,
    TPMI_ALG_HASH, authHash);
MAKE_ESYS_1(Esys_StartAuthSession_Finish,
    ESYS_TR *, sessionHandle);
MAKE_ESYS_4(Esys_PolicyRestart,
    ESYS_TR, sessionHandle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3);
MAKE_ESYS_4(Esys_PolicyRestart_Async,
    ESYS_TR, sessionHandle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3);
MAKE_ESYS_0(Esys_PolicyRestart_Finish);
MAKE_ESYS_13(Esys_Create,
    ESYS_TR, parentHandle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_SENSITIVE_CREATE *, inSensitive,
    const TPM2B_PUBLIC *, inPublic,
    const TPM2B_DATA *, outsideInfo,
    const TPML_PCR_SELECTION *, creationPCR,
    TPM2B_PRIVATE **, outPrivate,
    TPM2B_PUBLIC **, outPublic,
    TPM2B_CREATION_DATA **, creationData,
    TPM2B_DIGEST **, creationHash,
    TPMT_TK_CREATION **, creationTicket);
MAKE_ESYS_8(Esys_Create_Async,
    ESYS_TR, parentHandle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_SENSITIVE_CREATE *, inSensitive,
    const TPM2B_PUBLIC *, inPublic,
    const TPM2B_DATA *, outsideInfo,
    const TPML_PCR_SELECTION *, creationPCR);
MAKE_ESYS_5(Esys_Create_Finish,
    TPM2B_PRIVATE **, outPrivate,
    TPM2B_PUBLIC **, outPublic,
    TPM2B_CREATION_DATA **, creationData,
    TPM2B_DIGEST **, creationHash,
    TPMT_TK_CREATION **, creationTicket);
MAKE_ESYS_7(Esys_Load,
    ESYS_TR, parentHandle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_PRIVATE *, inPrivate,
    const TPM2B_PUBLIC *, inPublic,
    ESYS_TR *, objectHandle);
MAKE_ESYS_6(Esys_Load_Async,
    ESYS_TR, parentHandle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_PRIVATE *, inPrivate,
    const TPM2B_PUBLIC *, inPublic);
MAKE_ESYS_1(Esys_Load_Finish,
    ESYS_TR *, objectHandle);
MAKE_ESYS_7(Esys_LoadExternal,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_SENSITIVE *, inPrivate,
    const TPM2B_PUBLIC *, inPublic,
    ESYS_TR, hierarchy,
    ESYS_TR *, objectHandle);
MAKE_ESYS_6(Esys_LoadExternal_Async,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_SENSITIVE *, inPrivate,
    const TPM2B_PUBLIC *, inPublic,
    ESYS_TR, hierarchy);
MAKE_ESYS_1(Esys_LoadExternal_Finish,
    ESYS_TR *, objectHandle);
MAKE_ESYS_7(Esys_ReadPublic,
    ESYS_TR, objectHandle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    TPM2B_PUBLIC **, outPublic,
    TPM2B_NAME **, name,
    TPM2B_NAME **, qualifiedName);
MAKE_ESYS_4(Esys_ReadPublic_Async,
    ESYS_TR, objectHandle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3);
MAKE_ESYS_3(Esys_ReadPublic_Finish,
    TPM2B_PUBLIC **, outPublic,
    TPM2B_NAME **, name,
    TPM2B_NAME **, qualifiedName);
MAKE_ESYS_8(Esys_ActivateCredential,
    ESYS_TR, activateHandle,
    ESYS_TR, keyHandle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_ID_OBJECT *, credentialBlob,
    const TPM2B_ENCRYPTED_SECRET *, secret,
    TPM2B_DIGEST **, certInfo);
MAKE_ESYS_7(Esys_ActivateCredential_Async,
    ESYS_TR, activateHandle,
    ESYS_TR, keyHandle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_ID_OBJECT *, credentialBlob,
    const TPM2B_ENCRYPTED_SECRET *, secret);
MAKE_ESYS_1(Esys_ActivateCredential_Finish,
    TPM2B_DIGEST **, certInfo);
MAKE_ESYS_5(Esys_ACT_SetTimeout,
    ESYS_TR, actHandle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    UINT32, startTimeout);
MAKE_ESYS_5(Esys_ACT_SetTimeout_Async,
    ESYS_TR, actHandle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    UINT32, startTimeout);
MAKE_ESYS_0(Esys_ACT_SetTimeout_Finish);
MAKE_ESYS_6(Esys_AC_GetCapability_Async,
    ESYS_TR, optionalSession1,
    ESYS_TR, optionalSession2,
    ESYS_TR, optionalSession3,
    ESYS_TR, ac,
    TPM_AT, capability,
    UINT32, count)
MAKE_ESYS_2(Esys_AC_GetCapability_Finish,
    TPMI_YES_NO *, moreData,
    TPML_AC_CAPABILITIES **, capabilityData);
MAKE_ESYS_8(Esys_AC_GetCapability,
    ESYS_TR, optionalSession1,
    ESYS_TR, optionalSession2,
    ESYS_TR, optionalSession3,
    ESYS_TR, ac,
    TPM_AT, capability,
    UINT32, count,
    TPMI_YES_NO *, moreData,
    TPML_AC_CAPABILITIES **, capabilityData);
MAKE_ESYS_7(Esys_AC_Send_Async,
    ESYS_TR, sendObject,
    ESYS_TR, nvAuthHandle,
    ESYS_TR, optionalSession1,
    ESYS_TR, optionalSession2,
    ESYS_TR, optionalSession3,
    ESYS_TR, ac,
    TPM2B_MAX_BUFFER *, acDataIn);
MAKE_ESYS_1(Esys_AC_Send_Finish,
    TPMS_AC_OUTPUT **, acDataOut);
MAKE_ESYS_8(Esys_AC_Send,
    ESYS_TR, sendObject,
    ESYS_TR, nvAuthHandle,
    ESYS_TR, optionalSession1,
    ESYS_TR, optionalSession2,
    ESYS_TR, optionalSession3,
    ESYS_TR, ac,
    TPM2B_MAX_BUFFER *, acDataIn,
    TPMS_AC_OUTPUT **, acDataOut);
MAKE_ESYS_7(Esys_Policy_AC_SendSelect_Async,
    ESYS_TR, policySession1,
    ESYS_TR, optionalSession2,
    ESYS_TR, optionalSession3,
    TPM2B_NAME *, objectName,
    TPM2B_NAME *, authHandleName,
    TPM2B_NAME *, acName,
    const TPMI_YES_NO, includeObject);
MAKE_ESYS_0(Esys_Policy_AC_SendSelect_Finish);
MAKE_ESYS_7(Esys_Policy_AC_SendSelect,
    ESYS_TR, policySession1,
    ESYS_TR, optionalSession2,
    ESYS_TR, optionalSession3,
    TPM2B_NAME *, objectName,
    TPM2B_NAME *, authHandleName,
    TPM2B_NAME *, acName,
    TPMI_YES_NO, includeObject);
MAKE_ESYS_8(Esys_MakeCredential,
    ESYS_TR, handle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_DIGEST *, credential,
    const TPM2B_NAME *, objectName,
    TPM2B_ID_OBJECT **, credentialBlob,
    TPM2B_ENCRYPTED_SECRET **, secret);
MAKE_ESYS_6(Esys_MakeCredential_Async,
    ESYS_TR, handle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_DIGEST *, credential,
    const TPM2B_NAME *, objectName);
MAKE_ESYS_2(Esys_MakeCredential_Finish,
    TPM2B_ID_OBJECT **, credentialBlob,
    TPM2B_ENCRYPTED_SECRET **, secret);
MAKE_ESYS_5(Esys_Unseal,
    ESYS_TR, itemHandle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    TPM2B_SENSITIVE_DATA **, outData);
MAKE_ESYS_4(Esys_Unseal_Async,
    ESYS_TR, itemHandle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3);
MAKE_ESYS_1(Esys_Unseal_Finish,
    TPM2B_SENSITIVE_DATA **, outData);
MAKE_ESYS_7(Esys_ObjectChangeAuth,
    ESYS_TR, objectHandle,
    ESYS_TR, parentHandle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_AUTH *, newAuth,
    TPM2B_PRIVATE **, outPrivate);
MAKE_ESYS_6(Esys_ObjectChangeAuth_Async,
    ESYS_TR, objectHandle,
    ESYS_TR, parentHandle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_AUTH *, newAuth);
MAKE_ESYS_1(Esys_ObjectChangeAuth_Finish,
    TPM2B_PRIVATE **, outPrivate);
MAKE_ESYS_9(Esys_CreateLoaded,
    ESYS_TR, parentHandle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_SENSITIVE_CREATE *, inSensitive,
    const TPM2B_TEMPLATE *, inPublic,
    ESYS_TR *, objectHandle,
    TPM2B_PRIVATE **, outPrivate,
    TPM2B_PUBLIC **, outPublic);
MAKE_ESYS_6(Esys_CreateLoaded_Async,
    ESYS_TR, parentHandle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_SENSITIVE_CREATE *, inSensitive,
    const TPM2B_TEMPLATE *, inPublic);
MAKE_ESYS_3(Esys_CreateLoaded_Finish,
    ESYS_TR *, objectHandle,
    TPM2B_PRIVATE **, outPrivate,
    TPM2B_PUBLIC **, outPublic);
MAKE_ESYS_10(Esys_Duplicate,
    ESYS_TR, objectHandle,
    ESYS_TR, newParentHandle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_DATA *, encryptionKeyIn,
    const TPMT_SYM_DEF_OBJECT *, symmetricAlg,
    TPM2B_DATA **, encryptionKeyOut,
    TPM2B_PRIVATE **, duplicate,
    TPM2B_ENCRYPTED_SECRET **, outSymSeed);
MAKE_ESYS_7(Esys_Duplicate_Async,
    ESYS_TR, objectHandle,
    ESYS_TR, newParentHandle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_DATA *, encryptionKeyIn,
    const TPMT_SYM_DEF_OBJECT *, symmetricAlg);
MAKE_ESYS_3(Esys_Duplicate_Finish,
    TPM2B_DATA **, encryptionKeyOut,
    TPM2B_PRIVATE **, duplicate,
    TPM2B_ENCRYPTED_SECRET **, outSymSeed);
MAKE_ESYS_10(Esys_Rewrap,
    ESYS_TR, oldParent,
    ESYS_TR, newParent,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_PRIVATE *, inDuplicate,
    const TPM2B_NAME *, name,
    const TPM2B_ENCRYPTED_SECRET *, inSymSeed,
    TPM2B_PRIVATE **, outDuplicate,
    TPM2B_ENCRYPTED_SECRET **, outSymSeed);
MAKE_ESYS_8(Esys_Rewrap_Async,
    ESYS_TR, oldParent,
    ESYS_TR, newParent,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_PRIVATE *, inDuplicate,
    const TPM2B_NAME *, name,
    const TPM2B_ENCRYPTED_SECRET *, inSymSeed);
MAKE_ESYS_2(Esys_Rewrap_Finish,
    TPM2B_PRIVATE **, outDuplicate,
    TPM2B_ENCRYPTED_SECRET **, outSymSeed);
MAKE_ESYS_10(Esys_Import,
    ESYS_TR, parentHandle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_DATA *, encryptionKey,
    const TPM2B_PUBLIC *, objectPublic,
    const TPM2B_PRIVATE *, duplicate,
    const TPM2B_ENCRYPTED_SECRET *, inSymSeed,
    const TPMT_SYM_DEF_OBJECT *, symmetricAlg,
    TPM2B_PRIVATE **, outPrivate);
MAKE_ESYS_9(Esys_Import_Async,
    ESYS_TR, parentHandle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_DATA *, encryptionKey,
    const TPM2B_PUBLIC *, objectPublic,
    const TPM2B_PRIVATE *, duplicate,
    const TPM2B_ENCRYPTED_SECRET *, inSymSeed,
    const TPMT_SYM_DEF_OBJECT *, symmetricAlg);
MAKE_ESYS_1(Esys_Import_Finish,
    TPM2B_PRIVATE **, outPrivate);
MAKE_ESYS_8(Esys_RSA_Encrypt,
    ESYS_TR, keyHandle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_PUBLIC_KEY_RSA *, message,
    const TPMT_RSA_DECRYPT *, inScheme,
    const TPM2B_DATA *, label,
    TPM2B_PUBLIC_KEY_RSA **, outData);
MAKE_ESYS_7(Esys_RSA_Encrypt_Async,
    ESYS_TR, keyHandle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_PUBLIC_KEY_RSA *, message,
    const TPMT_RSA_DECRYPT *, inScheme,
    const TPM2B_DATA *, label);
MAKE_ESYS_1(Esys_RSA_Encrypt_Finish,
    TPM2B_PUBLIC_KEY_RSA **, outData);
MAKE_ESYS_8(Esys_RSA_Decrypt,
    ESYS_TR, keyHandle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_PUBLIC_KEY_RSA *, cipherText,
    const TPMT_RSA_DECRYPT *, inScheme,
    const TPM2B_DATA *, label,
    TPM2B_PUBLIC_KEY_RSA **, message);
MAKE_ESYS_7(Esys_RSA_Decrypt_Async,
    ESYS_TR, keyHandle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_PUBLIC_KEY_RSA *, cipherText,
    const TPMT_RSA_DECRYPT *, inScheme,
    const TPM2B_DATA *, label);
MAKE_ESYS_1(Esys_RSA_Decrypt_Finish,
    TPM2B_PUBLIC_KEY_RSA **, message);
MAKE_ESYS_6(Esys_ECDH_KeyGen,
    ESYS_TR, keyHandle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    TPM2B_ECC_POINT **, zPoint,
    TPM2B_ECC_POINT **, pubPoint);
MAKE_ESYS_4(Esys_ECDH_KeyGen_Async,
    ESYS_TR, keyHandle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3);
MAKE_ESYS_2(Esys_ECDH_KeyGen_Finish,
    TPM2B_ECC_POINT **, zPoint,
    TPM2B_ECC_POINT **, pubPoint);
MAKE_ESYS_6(Esys_ECDH_ZGen,
    ESYS_TR, keyHandle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_ECC_POINT *, inPoint,
    TPM2B_ECC_POINT **, outPoint);
MAKE_ESYS_5(Esys_ECDH_ZGen_Async,
    ESYS_TR, keyHandle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_ECC_POINT *, inPoint);
MAKE_ESYS_1(Esys_ECDH_ZGen_Finish,
    TPM2B_ECC_POINT **, outPoint);
MAKE_ESYS_5(Esys_ECC_Parameters,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    TPMI_ECC_CURVE, curveID,
    TPMS_ALGORITHM_DETAIL_ECC **, parameters);
MAKE_ESYS_4(Esys_ECC_Parameters_Async,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    TPMI_ECC_CURVE, curveID);
MAKE_ESYS_1(Esys_ECC_Parameters_Finish,
    TPMS_ALGORITHM_DETAIL_ECC **, parameters);
MAKE_ESYS_10(Esys_ZGen_2Phase,
    ESYS_TR, keyA,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_ECC_POINT *, inQsB,
    const TPM2B_ECC_POINT *, inQeB,
    TPMI_ECC_KEY_EXCHANGE, inScheme,
    UINT16, counter,
    TPM2B_ECC_POINT **, outZ1,
    TPM2B_ECC_POINT **, outZ2);
MAKE_ESYS_8(Esys_ZGen_2Phase_Async,
    ESYS_TR, keyA,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_ECC_POINT *, inQsB,
    const TPM2B_ECC_POINT *, inQeB,
    TPMI_ECC_KEY_EXCHANGE, inScheme,
    UINT16, counter);
MAKE_ESYS_2(Esys_ZGen_2Phase_Finish,
    TPM2B_ECC_POINT **, outZ1,
    TPM2B_ECC_POINT **, outZ2);
MAKE_ESYS_10(Esys_EncryptDecrypt,
    ESYS_TR, keyHandle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    TPMI_YES_NO, decrypt,
    TPMI_ALG_CIPHER_MODE, mode,
    const TPM2B_IV *, ivIn,
    const TPM2B_MAX_BUFFER *, inData,
    TPM2B_MAX_BUFFER **, outData,
    TPM2B_IV **, ivOut);
MAKE_ESYS_8(Esys_EncryptDecrypt_Async,
    ESYS_TR, keyHandle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    TPMI_YES_NO, decrypt,
    TPMI_ALG_CIPHER_MODE, mode,
    const TPM2B_IV *, ivIn,
    const TPM2B_MAX_BUFFER *, inData);
MAKE_ESYS_2(Esys_EncryptDecrypt_Finish,
    TPM2B_MAX_BUFFER **, outData,
    TPM2B_IV **, ivOut);
MAKE_ESYS_10(Esys_EncryptDecrypt2,
    ESYS_TR, keyHandle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_MAX_BUFFER *, inData,
    TPMI_YES_NO, decrypt,
    TPMI_ALG_CIPHER_MODE, mode,
    const TPM2B_IV *, ivIn,
    TPM2B_MAX_BUFFER **, outData,
    TPM2B_IV **, ivOut);
MAKE_ESYS_8(Esys_EncryptDecrypt2_Async,
    ESYS_TR, keyHandle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_MAX_BUFFER *, inData,
    TPMI_YES_NO, decrypt,
    TPMI_ALG_CIPHER_MODE, mode,
    const TPM2B_IV *, ivIn);
MAKE_ESYS_2(Esys_EncryptDecrypt2_Finish,
    TPM2B_MAX_BUFFER **, outData,
    TPM2B_IV **, ivOut);
MAKE_ESYS_8(Esys_Hash,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_MAX_BUFFER *, data,
    TPMI_ALG_HASH, hashAlg,
    ESYS_TR, hierarchy,
    TPM2B_DIGEST **, outHash,
    TPMT_TK_HASHCHECK **, validation);
MAKE_ESYS_6(Esys_Hash_Async,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_MAX_BUFFER *, data,
    TPMI_ALG_HASH, hashAlg,
    ESYS_TR, hierarchy);
MAKE_ESYS_2(Esys_Hash_Finish,
    TPM2B_DIGEST **, outHash,
    TPMT_TK_HASHCHECK **, validation);
MAKE_ESYS_7(Esys_HMAC,
    ESYS_TR, handle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_MAX_BUFFER *, buffer,
    TPMI_ALG_HASH, hashAlg,
    TPM2B_DIGEST **, outHMAC);
MAKE_ESYS_6(Esys_HMAC_Async,
    ESYS_TR, handle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_MAX_BUFFER *, buffer,
    TPMI_ALG_HASH, hashAlg);
MAKE_ESYS_1(Esys_HMAC_Finish,
    TPM2B_DIGEST **, outHMAC);
MAKE_ESYS_6(Esys_MAC_Async,
    ESYS_TR, handle,
    ESYS_TR, handleSession1,
    ESYS_TR, optionalSession2,
    ESYS_TR, optionalSession3,
    const TPM2B_MAX_BUFFER *, buffer,
    TPMI_ALG_MAC_SCHEME, inScheme);
MAKE_ESYS_1(Esys_MAC_Finish,
    TPM2B_DIGEST **, outMAC);
MAKE_ESYS_7(Esys_MAC,
    ESYS_TR, handle,
    ESYS_TR, handleSession1,
    ESYS_TR, optionalSession2,
    ESYS_TR, optionalSession3,
    const TPM2B_MAX_BUFFER *, buffer,
    TPMI_ALG_MAC_SCHEME, inScheme,
    TPM2B_DIGEST **, outMAC);
MAKE_ESYS_5(Esys_GetRandom,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    UINT16, bytesRequested,
    TPM2B_DIGEST **, randomBytes);
MAKE_ESYS_4(Esys_GetRandom_Async,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    UINT16, bytesRequested);
MAKE_ESYS_1(Esys_GetRandom_Finish,
    TPM2B_DIGEST **, randomBytes);
MAKE_ESYS_4(Esys_StirRandom,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_SENSITIVE_DATA *, inData);
MAKE_ESYS_4(Esys_StirRandom_Async,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_SENSITIVE_DATA *, inData);
MAKE_ESYS_0(Esys_StirRandom_Finish);
MAKE_ESYS_7(Esys_HMAC_Start,
    ESYS_TR, handle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_AUTH *, auth,
    TPMI_ALG_HASH, hashAlg,
    ESYS_TR *, sequenceHandle);
MAKE_ESYS_6(Esys_HMAC_Start_Async,
    ESYS_TR, handle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_AUTH *, auth,
    TPMI_ALG_HASH, hashAlg);
MAKE_ESYS_1(Esys_HMAC_Start_Finish,
    ESYS_TR *, sequenceHandle);
MAKE_ESYS_7(Esys_MAC_Start,
    ESYS_TR, handle,
    ESYS_TR, handleSession1,
    ESYS_TR, optionalSession2,
    ESYS_TR, optionalSession3,
    const TPM2B_AUTH *, auth,
    TPMI_ALG_MAC_SCHEME, inScheme,
    ESYS_TR *, sequenceHandle);
MAKE_ESYS_6(Esys_MAC_Start_Async,
    ESYS_TR, handle,
    ESYS_TR, handleSession1,
    ESYS_TR, optionalSession2,
    ESYS_TR, optionalSession3,
    const TPM2B_AUTH *, auth,
    TPMI_ALG_MAC_SCHEME, inScheme);
MAKE_ESYS_1(Esys_MAC_Start_Finish,
    ESYS_TR *, sequenceHandle);
MAKE_ESYS_6(Esys_HashSequenceStart,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_AUTH *, auth,
    TPMI_ALG_HASH, hashAlg,
    ESYS_TR *, sequenceHandle);
MAKE_ESYS_5(Esys_HashSequenceStart_Async,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_AUTH *, auth,
    TPMI_ALG_HASH, hashAlg);
MAKE_ESYS_1(Esys_HashSequenceStart_Finish,
    ESYS_TR *, sequenceHandle);
MAKE_ESYS_5(Esys_SequenceUpdate,
    ESYS_TR, sequenceHandle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_MAX_BUFFER *, buffer);
MAKE_ESYS_5(Esys_SequenceUpdate_Async,
    ESYS_TR, sequenceHandle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_MAX_BUFFER *, buffer);
MAKE_ESYS_0(Esys_SequenceUpdate_Finish);
MAKE_ESYS_8(Esys_SequenceComplete,
    ESYS_TR, sequenceHandle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_MAX_BUFFER *, buffer,
    ESYS_TR, hierarchy,
    TPM2B_DIGEST **, result,
    TPMT_TK_HASHCHECK **, validation);
MAKE_ESYS_6(Esys_SequenceComplete_Async,
    ESYS_TR, sequenceHandle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_MAX_BUFFER *, buffer,
    ESYS_TR, hierarchy);
MAKE_ESYS_2(Esys_SequenceComplete_Finish,
    TPM2B_DIGEST **, result,
    TPMT_TK_HASHCHECK **, validation);
MAKE_ESYS_7(Esys_EventSequenceComplete,
    ESYS_TR, pcrHandle,
    ESYS_TR, sequenceHandle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_MAX_BUFFER *, buffer,
    TPML_DIGEST_VALUES **, results);
MAKE_ESYS_6(Esys_EventSequenceComplete_Async,
    ESYS_TR, pcrHandle,
    ESYS_TR, sequenceHandle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_MAX_BUFFER *, buffer);
MAKE_ESYS_1(Esys_EventSequenceComplete_Finish,
    TPML_DIGEST_VALUES **, results);
MAKE_ESYS_9(Esys_Certify,
    ESYS_TR, objectHandle,
    ESYS_TR, signHandle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_DATA *, qualifyingData,
    const TPMT_SIG_SCHEME *, inScheme,
    TPM2B_ATTEST **, certifyInfo,
    TPMT_SIGNATURE **, signature);
MAKE_ESYS_7(Esys_Certify_Async,
    ESYS_TR, objectHandle,
    ESYS_TR, signHandle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_DATA *, qualifyingData,
    const TPMT_SIG_SCHEME *, inScheme);
MAKE_ESYS_2(Esys_Certify_Finish,
    TPM2B_ATTEST **, certifyInfo,
    TPMT_SIGNATURE **, signature);
MAKE_ESYS_11(Esys_CertifyCreation,
    ESYS_TR, signHandle,
    ESYS_TR, objectHandle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_DATA *, qualifyingData,
    const TPM2B_DIGEST *, creationHash,
    const TPMT_SIG_SCHEME *, inScheme,
    const TPMT_TK_CREATION *, creationTicket,
    TPM2B_ATTEST **, certifyInfo,
    TPMT_SIGNATURE **, signature);
MAKE_ESYS_9(Esys_CertifyCreation_Async,
    ESYS_TR, signHandle,
    ESYS_TR, objectHandle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_DATA *, qualifyingData,
    const TPM2B_DIGEST *, creationHash,
    const TPMT_SIG_SCHEME *, inScheme,
    const TPMT_TK_CREATION *, creationTicket);
MAKE_ESYS_2(Esys_CertifyCreation_Finish,
    TPM2B_ATTEST **, certifyInfo,
    TPMT_SIGNATURE **, signature);
MAKE_ESYS_11(Esys_CertifyX509,
    ESYS_TR, objectHandle,
    ESYS_TR, signHandle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_DATA *, reserved,
    const TPMT_SIG_SCHEME *, inScheme,
    const TPM2B_MAX_BUFFER *, partialCertificate,
    TPM2B_MAX_BUFFER **, addedToCertificate,
    TPM2B_DIGEST **, tbsDigest,
    TPMT_SIGNATURE **, signature);
MAKE_ESYS_8(Esys_CertifyX509_Async,
    ESYS_TR, objectHandle,
    ESYS_TR, signHandle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_DATA *, reserved,
    const TPMT_SIG_SCHEME *, inScheme,
    const TPM2B_MAX_BUFFER *, partialCertificate);
MAKE_ESYS_3(Esys_CertifyX509_Finish,
    TPM2B_MAX_BUFFER **, addedToCertificate,
    TPM2B_DIGEST **, tbsDigest,
    TPMT_SIGNATURE **, signature);
MAKE_ESYS_9(Esys_Quote,
    ESYS_TR, signHandle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_DATA *, qualifyingData,
    const TPMT_SIG_SCHEME *, inScheme,
    const TPML_PCR_SELECTION *, PCRselect,
    TPM2B_ATTEST **, quoted,
    TPMT_SIGNATURE **, signature);
MAKE_ESYS_7(Esys_Quote_Async,
    ESYS_TR, signHandle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_DATA *, qualifyingData,
    const TPMT_SIG_SCHEME *, inScheme,
    const TPML_PCR_SELECTION *, PCRselect);
MAKE_ESYS_2(Esys_Quote_Finish,
    TPM2B_ATTEST **, quoted,
    TPMT_SIGNATURE **, signature);
MAKE_ESYS_10(Esys_GetSessionAuditDigest,
    ESYS_TR, privacyAdminHandle,
    ESYS_TR, signHandle,
    ESYS_TR, sessionHandle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_DATA *, qualifyingData,
    const TPMT_SIG_SCHEME *, inScheme,
    TPM2B_ATTEST **, auditInfo,
    TPMT_SIGNATURE **, signature);
MAKE_ESYS_8(Esys_GetSessionAuditDigest_Async,
    ESYS_TR, privacyAdminHandle,
    ESYS_TR, signHandle,
    ESYS_TR, sessionHandle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_DATA *, qualifyingData,
    const TPMT_SIG_SCHEME *, inScheme);
MAKE_ESYS_2(Esys_GetSessionAuditDigest_Finish,
    TPM2B_ATTEST **, auditInfo,
    TPMT_SIGNATURE **, signature);
MAKE_ESYS_9(Esys_GetCommandAuditDigest,
    ESYS_TR, privacyHandle,
    ESYS_TR, signHandle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_DATA *, qualifyingData,
    const TPMT_SIG_SCHEME *, inScheme,
    TPM2B_ATTEST **, auditInfo,
    TPMT_SIGNATURE **, signature);
MAKE_ESYS_7(Esys_GetCommandAuditDigest_Async,
    ESYS_TR, privacyHandle,
    ESYS_TR, signHandle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_DATA *, qualifyingData,
    const TPMT_SIG_SCHEME *, inScheme);
MAKE_ESYS_2(Esys_GetCommandAuditDigest_Finish,
    TPM2B_ATTEST **, auditInfo,
    TPMT_SIGNATURE **, signature);
MAKE_ESYS_9(Esys_GetTime,
    ESYS_TR, privacyAdminHandle,
    ESYS_TR, signHandle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_DATA *, qualifyingData,
    const TPMT_SIG_SCHEME *, inScheme,
    TPM2B_ATTEST **, timeInfo,
    TPMT_SIGNATURE **, signature);
MAKE_ESYS_7(Esys_GetTime_Async,
    ESYS_TR, privacyAdminHandle,
    ESYS_TR, signHandle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_DATA *, qualifyingData,
    const TPMT_SIG_SCHEME *, inScheme);
MAKE_ESYS_2(Esys_GetTime_Finish,
    TPM2B_ATTEST **, timeInfo,
    TPMT_SIGNATURE **, signature);
MAKE_ESYS_11(Esys_Commit,
    ESYS_TR, signHandle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_ECC_POINT *, P1,
    const TPM2B_SENSITIVE_DATA *, s2,
    const TPM2B_ECC_PARAMETER *, y2,
    TPM2B_ECC_POINT **, K,
    TPM2B_ECC_POINT **, L,
    TPM2B_ECC_POINT **, E,
    UINT16 *, counter);
MAKE_ESYS_7(Esys_Commit_Async,
    ESYS_TR, signHandle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_ECC_POINT *, P1,
    const TPM2B_SENSITIVE_DATA *, s2,
    const TPM2B_ECC_PARAMETER *, y2);
MAKE_ESYS_4(Esys_Commit_Finish,
    TPM2B_ECC_POINT **, K,
    TPM2B_ECC_POINT **, L,
    TPM2B_ECC_POINT **, E,
    UINT16 *, counter);
MAKE_ESYS_6(Esys_EC_Ephemeral,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    TPMI_ECC_CURVE, curveID,
    TPM2B_ECC_POINT **, Q,
    UINT16 *, counter);
MAKE_ESYS_4(Esys_EC_Ephemeral_Async,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    TPMI_ECC_CURVE, curveID);
MAKE_ESYS_2(Esys_EC_Ephemeral_Finish,
    TPM2B_ECC_POINT **, Q,
    UINT16 *, counter);
MAKE_ESYS_7(Esys_VerifySignature,
    ESYS_TR, keyHandle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_DIGEST *, digest,
    const TPMT_SIGNATURE *, signature,
    TPMT_TK_VERIFIED **, validation);
MAKE_ESYS_6(Esys_VerifySignature_Async,
    ESYS_TR, keyHandle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_DIGEST *, digest,
    const TPMT_SIGNATURE *, signature);
MAKE_ESYS_1(Esys_VerifySignature_Finish,
    TPMT_TK_VERIFIED **, validation);
MAKE_ESYS_8(Esys_Sign,
    ESYS_TR, keyHandle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_DIGEST *, digest,
    const TPMT_SIG_SCHEME *, inScheme,
    const TPMT_TK_HASHCHECK *, validation,
    TPMT_SIGNATURE **, signature);
MAKE_ESYS_7(Esys_Sign_Async,
    ESYS_TR, keyHandle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_DIGEST *, digest,
    const TPMT_SIG_SCHEME *, inScheme,
    const TPMT_TK_HASHCHECK *, validation);
MAKE_ESYS_1(Esys_Sign_Finish,
    TPMT_SIGNATURE **, signature);
MAKE_ESYS_7(Esys_SetCommandCodeAuditStatus,
    ESYS_TR, auth,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    TPMI_ALG_HASH, auditAlg,
    const TPML_CC *, setList,
    const TPML_CC *, clearList);
MAKE_ESYS_7(Esys_SetCommandCodeAuditStatus_Async,
    ESYS_TR, auth,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    TPMI_ALG_HASH, auditAlg,
    const TPML_CC *, setList,
    const TPML_CC *, clearList);
MAKE_ESYS_0(Esys_SetCommandCodeAuditStatus_Finish);
MAKE_ESYS_5(Esys_PCR_Extend,
    ESYS_TR, pcrHandle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPML_DIGEST_VALUES *, digests);
MAKE_ESYS_5(Esys_PCR_Extend_Async,
    ESYS_TR, pcrHandle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPML_DIGEST_VALUES *, digests);
MAKE_ESYS_0(Esys_PCR_Extend_Finish);
MAKE_ESYS_6(Esys_PCR_Event,
    ESYS_TR, pcrHandle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_EVENT *, eventData,
    TPML_DIGEST_VALUES **, digests);
MAKE_ESYS_5(Esys_PCR_Event_Async,
    ESYS_TR, pcrHandle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_EVENT *, eventData);
MAKE_ESYS_1(Esys_PCR_Event_Finish,
    TPML_DIGEST_VALUES **, digests);
MAKE_ESYS_7(Esys_PCR_Read,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPML_PCR_SELECTION *, pcrSelectionIn,
    UINT32 *, pcrUpdateCounter,
    TPML_PCR_SELECTION **, pcrSelectionOut,
    TPML_DIGEST **, pcrValues);
MAKE_ESYS_4(Esys_PCR_Read_Async,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPML_PCR_SELECTION *, pcrSelectionIn);
MAKE_ESYS_3(Esys_PCR_Read_Finish,
    UINT32 *, pcrUpdateCounter,
    TPML_PCR_SELECTION **, pcrSelectionOut,
    TPML_DIGEST **, pcrValues);
MAKE_ESYS_9(Esys_PCR_Allocate,
    ESYS_TR, authHandle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPML_PCR_SELECTION *, pcrAllocation,
    TPMI_YES_NO *, allocationSuccess,
    UINT32 *, maxPCR,
    UINT32 *, sizeNeeded,
    UINT32 *, sizeAvailable);
MAKE_ESYS_5(Esys_PCR_Allocate_Async,
    ESYS_TR, authHandle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPML_PCR_SELECTION *, pcrAllocation);
MAKE_ESYS_4(Esys_PCR_Allocate_Finish,
    TPMI_YES_NO *, allocationSuccess,
    UINT32 *, maxPCR,
    UINT32 *, sizeNeeded,
    UINT32 *, sizeAvailable);
MAKE_ESYS_7(Esys_PCR_SetAuthPolicy,
    ESYS_TR, authHandle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_DIGEST *, authPolicy,
    TPMI_ALG_HASH, hashAlg,
    TPMI_DH_PCR, pcrNum);
MAKE_ESYS_7(Esys_PCR_SetAuthPolicy_Async,
    ESYS_TR, authHandle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_DIGEST *, authPolicy,
    TPMI_ALG_HASH, hashAlg,
    TPMI_DH_PCR, pcrNum);
MAKE_ESYS_0(Esys_PCR_SetAuthPolicy_Finish);
MAKE_ESYS_5(Esys_PCR_SetAuthValue,
    ESYS_TR, pcrHandle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_DIGEST *, auth);
MAKE_ESYS_5(Esys_PCR_SetAuthValue_Async,
    ESYS_TR, pcrHandle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_DIGEST *, auth);
MAKE_ESYS_0(Esys_PCR_SetAuthValue_Finish);
MAKE_ESYS_4(Esys_PCR_Reset,
    ESYS_TR, pcrHandle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3);
MAKE_ESYS_4(Esys_PCR_Reset_Async,
    ESYS_TR, pcrHandle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3);
MAKE_ESYS_0(Esys_PCR_Reset_Finish);
MAKE_ESYS_12(Esys_PolicySigned,
    ESYS_TR, authObject,
    ESYS_TR, policySession,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_NONCE *, nonceTPM,
    const TPM2B_DIGEST *, cpHashA,
    const TPM2B_NONCE *, policyRef,
    INT32, expiration,
    const TPMT_SIGNATURE *, auth,
    TPM2B_TIMEOUT **, timeout,
    TPMT_TK_AUTH **, policyTicket);
MAKE_ESYS_10(Esys_PolicySigned_Async,
    ESYS_TR, authObject,
    ESYS_TR, policySession,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_NONCE *, nonceTPM,
    const TPM2B_DIGEST *, cpHashA,
    const TPM2B_NONCE *, policyRef,
    INT32, expiration,
    const TPMT_SIGNATURE *, auth);
MAKE_ESYS_2(Esys_PolicySigned_Finish,
    TPM2B_TIMEOUT **, timeout,
    TPMT_TK_AUTH **, policyTicket);
MAKE_ESYS_11(Esys_PolicySecret,
    ESYS_TR, authHandle,
    ESYS_TR, policySession,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_NONCE *, nonceTPM,
    const TPM2B_DIGEST *, cpHashA,
    const TPM2B_NONCE *, policyRef,
    INT32, expiration,
    TPM2B_TIMEOUT **, timeout,
    TPMT_TK_AUTH **, policyTicket);
MAKE_ESYS_9(Esys_PolicySecret_Async,
    ESYS_TR, authHandle,
    ESYS_TR, policySession,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_NONCE *, nonceTPM,
    const TPM2B_DIGEST *, cpHashA,
    const TPM2B_NONCE *, policyRef,
    INT32, expiration);
MAKE_ESYS_2(Esys_PolicySecret_Finish,
    TPM2B_TIMEOUT **, timeout,
    TPMT_TK_AUTH **, policyTicket);
MAKE_ESYS_9(Esys_PolicyTicket,
    ESYS_TR, policySession,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_TIMEOUT *, timeout,
    const TPM2B_DIGEST *, cpHashA,
    const TPM2B_NONCE *, policyRef,
    const TPM2B_NAME *, authName,
    const TPMT_TK_AUTH *, ticket);
MAKE_ESYS_9(Esys_PolicyTicket_Async,
    ESYS_TR, policySession,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_TIMEOUT *, timeout,
    const TPM2B_DIGEST *, cpHashA,
    const TPM2B_NONCE *, policyRef,
    const TPM2B_NAME *, authName,
    const TPMT_TK_AUTH *, ticket);
MAKE_ESYS_0(Esys_PolicyTicket_Finish);
MAKE_ESYS_5(Esys_PolicyOR,
    ESYS_TR, policySession,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPML_DIGEST *, pHashList);
MAKE_ESYS_5(Esys_PolicyOR_Async,
    ESYS_TR, policySession,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPML_DIGEST *, pHashList);
MAKE_ESYS_0(Esys_PolicyOR_Finish);
MAKE_ESYS_6(Esys_PolicyPCR,
    ESYS_TR, policySession,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_DIGEST *, pcrDigest,
    const TPML_PCR_SELECTION *, pcrs);
MAKE_ESYS_6(Esys_PolicyPCR_Async,
    ESYS_TR, policySession,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_DIGEST *, pcrDigest,
    const TPML_PCR_SELECTION *, pcrs);
MAKE_ESYS_0(Esys_PolicyPCR_Finish);
MAKE_ESYS_5(Esys_PolicyLocality,
    ESYS_TR, policySession,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    TPMA_LOCALITY, locality);
MAKE_ESYS_5(Esys_PolicyLocality_Async,
    ESYS_TR, policySession,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    TPMA_LOCALITY, locality);
MAKE_ESYS_0(Esys_PolicyLocality_Finish);
MAKE_ESYS_9(Esys_PolicyNV,
    ESYS_TR, authHandle,
    ESYS_TR, nvIndex,
    ESYS_TR, policySession,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_OPERAND *, operandB,
    UINT16, offset,
    TPM2_EO, operation);
MAKE_ESYS_9(Esys_PolicyNV_Async,
    ESYS_TR, authHandle,
    ESYS_TR, nvIndex,
    ESYS_TR, policySession,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_OPERAND *, operandB,
    UINT16, offset,
    TPM2_EO, operation);
MAKE_ESYS_0(Esys_PolicyNV_Finish);
MAKE_ESYS_7(Esys_PolicyCounterTimer,
    ESYS_TR, policySession,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_OPERAND *, operandB,
    UINT16, offset,
    TPM2_EO, operation);
MAKE_ESYS_7(Esys_PolicyCounterTimer_Async,
    ESYS_TR, policySession,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_OPERAND *, operandB,
    UINT16, offset,
    TPM2_EO, operation);
MAKE_ESYS_0(Esys_PolicyCounterTimer_Finish);
MAKE_ESYS_5(Esys_PolicyCommandCode,
    ESYS_TR, policySession,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    TPM2_CC, code);
MAKE_ESYS_5(Esys_PolicyCommandCode_Async,
    ESYS_TR, policySession,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    TPM2_CC, code);
MAKE_ESYS_0(Esys_PolicyCommandCode_Finish);
MAKE_ESYS_4(Esys_PolicyPhysicalPresence,
    ESYS_TR, policySession,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3);
MAKE_ESYS_4(Esys_PolicyPhysicalPresence_Async,
    ESYS_TR, policySession,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3);
MAKE_ESYS_0(Esys_PolicyPhysicalPresence_Finish);
MAKE_ESYS_5(Esys_PolicyCpHash,
    ESYS_TR, policySession,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_DIGEST *, cpHashA);
MAKE_ESYS_5(Esys_PolicyCpHash_Async,
    ESYS_TR, policySession,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_DIGEST *, cpHashA);
MAKE_ESYS_0(Esys_PolicyCpHash_Finish);
MAKE_ESYS_5(Esys_PolicyNameHash,
    ESYS_TR, policySession,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_DIGEST *, nameHash);
MAKE_ESYS_5(Esys_PolicyNameHash_Async,
    ESYS_TR, policySession,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_DIGEST *, nameHash);
MAKE_ESYS_0(Esys_PolicyNameHash_Finish);
MAKE_ESYS_7(Esys_PolicyDuplicationSelect,
    ESYS_TR, policySession,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_NAME *, objectName,
    const TPM2B_NAME *, newParentName,
    TPMI_YES_NO, includeObject);
MAKE_ESYS_7(Esys_PolicyDuplicationSelect_Async,
    ESYS_TR, policySession,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_NAME *, objectName,
    const TPM2B_NAME *, newParentName,
    TPMI_YES_NO, includeObject);
MAKE_ESYS_0(Esys_PolicyDuplicationSelect_Finish);
MAKE_ESYS_8(Esys_PolicyAuthorize,
    ESYS_TR, policySession,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_DIGEST *, approvedPolicy,
    const TPM2B_NONCE *, policyRef,
    const TPM2B_NAME *, keySign,
    const TPMT_TK_VERIFIED *, checkTicket);
MAKE_ESYS_8(Esys_PolicyAuthorize_Async,
    ESYS_TR, policySession,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_DIGEST *, approvedPolicy,
    const TPM2B_NONCE *, policyRef,
    const TPM2B_NAME *, keySign,
    const TPMT_TK_VERIFIED *, checkTicket);
MAKE_ESYS_0(Esys_PolicyAuthorize_Finish);
MAKE_ESYS_4(Esys_PolicyAuthValue,
    ESYS_TR, policySession,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3);
MAKE_ESYS_4(Esys_PolicyAuthValue_Async,
    ESYS_TR, policySession,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3);
MAKE_ESYS_0(Esys_PolicyAuthValue_Finish);
MAKE_ESYS_4(Esys_PolicyPassword,
    ESYS_TR, policySession,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3);
MAKE_ESYS_4(Esys_PolicyPassword_Async,
    ESYS_TR, policySession,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3);
MAKE_ESYS_0(Esys_PolicyPassword_Finish);
MAKE_ESYS_5(Esys_PolicyGetDigest,
    ESYS_TR, policySession,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    TPM2B_DIGEST **, policyDigest);
MAKE_ESYS_4(Esys_PolicyGetDigest_Async,
    ESYS_TR, policySession,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3);
MAKE_ESYS_1(Esys_PolicyGetDigest_Finish,
    TPM2B_DIGEST **, policyDigest);
MAKE_ESYS_5(Esys_PolicyNvWritten,
    ESYS_TR, policySession,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    TPMI_YES_NO, writtenSet);
MAKE_ESYS_5(Esys_PolicyNvWritten_Async,
    ESYS_TR, policySession,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    TPMI_YES_NO, writtenSet);
MAKE_ESYS_0(Esys_PolicyNvWritten_Finish);
MAKE_ESYS_5(Esys_PolicyTemplate,
    ESYS_TR, policySession,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_DIGEST *, templateHash);
MAKE_ESYS_5(Esys_PolicyTemplate_Async,
    ESYS_TR, policySession,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_DIGEST *, templateHash);
MAKE_ESYS_0(Esys_PolicyTemplate_Finish);
MAKE_ESYS_6(Esys_PolicyAuthorizeNV,
    ESYS_TR, authHandle,
    ESYS_TR, nvIndex,
    ESYS_TR, policySession,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3);
MAKE_ESYS_6(Esys_PolicyAuthorizeNV_Async,
    ESYS_TR, authHandle,
    ESYS_TR, nvIndex,
    ESYS_TR, policySession,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3);
MAKE_ESYS_0(Esys_PolicyAuthorizeNV_Finish);
MAKE_ESYS_13(Esys_CreatePrimary,
    ESYS_TR, primaryHandle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_SENSITIVE_CREATE *, inSensitive,
    const TPM2B_PUBLIC *, inPublic,
    const TPM2B_DATA *, outsideInfo,
    const TPML_PCR_SELECTION *, creationPCR,
    ESYS_TR *, objectHandle,
    TPM2B_PUBLIC **, outPublic,
    TPM2B_CREATION_DATA **, creationData,
    TPM2B_DIGEST **, creationHash,
    TPMT_TK_CREATION **, creationTicket);
MAKE_ESYS_8(Esys_CreatePrimary_Async,
    ESYS_TR, primaryHandle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_SENSITIVE_CREATE *, inSensitive,
    const TPM2B_PUBLIC *, inPublic,
    const TPM2B_DATA *, outsideInfo,
    const TPML_PCR_SELECTION *, creationPCR);
MAKE_ESYS_5(Esys_CreatePrimary_Finish,
    ESYS_TR *, objectHandle,
    TPM2B_PUBLIC **, outPublic,
    TPM2B_CREATION_DATA **, creationData,
    TPM2B_DIGEST **, creationHash,
    TPMT_TK_CREATION **, creationTicket);
MAKE_ESYS_6(Esys_HierarchyControl,
    ESYS_TR, authHandle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    ESYS_TR, enable,
    TPMI_YES_NO, state);
MAKE_ESYS_6(Esys_HierarchyControl_Async,
    ESYS_TR, authHandle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    ESYS_TR, enable,
    TPMI_YES_NO, state);
MAKE_ESYS_0(Esys_HierarchyControl_Finish);
MAKE_ESYS_6(Esys_SetPrimaryPolicy,
    ESYS_TR, authHandle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_DIGEST *, authPolicy,
    TPMI_ALG_HASH, hashAlg);
MAKE_ESYS_6(Esys_SetPrimaryPolicy_Async,
    ESYS_TR, authHandle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_DIGEST *, authPolicy,
    TPMI_ALG_HASH, hashAlg);
MAKE_ESYS_0(Esys_SetPrimaryPolicy_Finish);
MAKE_ESYS_4(Esys_ChangePPS,
    ESYS_TR, authHandle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3);
MAKE_ESYS_4(Esys_ChangePPS_Async,
    ESYS_TR, authHandle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3);
MAKE_ESYS_0(Esys_ChangePPS_Finish);
MAKE_ESYS_4(Esys_ChangeEPS,
    ESYS_TR, authHandle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3);
MAKE_ESYS_4(Esys_ChangeEPS_Async,
    ESYS_TR, authHandle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3);
MAKE_ESYS_0(Esys_ChangeEPS_Finish);
MAKE_ESYS_4(Esys_Clear,
    ESYS_TR, authHandle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3);
MAKE_ESYS_4(Esys_Clear_Async,
    ESYS_TR, authHandle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3);
MAKE_ESYS_0(Esys_Clear_Finish);
MAKE_ESYS_5(Esys_ClearControl,
    ESYS_TR, auth,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    TPMI_YES_NO, disable);
MAKE_ESYS_5(Esys_ClearControl_Async,
    ESYS_TR, auth,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    TPMI_YES_NO, disable);
MAKE_ESYS_0(Esys_ClearControl_Finish);
MAKE_ESYS_5(Esys_HierarchyChangeAuth,
    ESYS_TR, authHandle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_AUTH *, newAuth);
MAKE_ESYS_5(Esys_HierarchyChangeAuth_Async,
    ESYS_TR, authHandle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_AUTH *, newAuth);
MAKE_ESYS_0(Esys_HierarchyChangeAuth_Finish);
MAKE_ESYS_4(Esys_DictionaryAttackLockReset,
    ESYS_TR, lockHandle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3);
MAKE_ESYS_4(Esys_DictionaryAttackLockReset_Async,
    ESYS_TR, lockHandle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3);
MAKE_ESYS_0(Esys_DictionaryAttackLockReset_Finish);
MAKE_ESYS_7(Esys_DictionaryAttackParameters,
    ESYS_TR, lockHandle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    UINT32, newMaxTries,
    UINT32, newRecoveryTime,
    UINT32, lockoutRecovery);
MAKE_ESYS_7(Esys_DictionaryAttackParameters_Async,
    ESYS_TR, lockHandle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    UINT32, newMaxTries,
    UINT32, newRecoveryTime,
    UINT32, lockoutRecovery);
MAKE_ESYS_0(Esys_DictionaryAttackParameters_Finish);
MAKE_ESYS_6(Esys_PP_Commands,
    ESYS_TR, auth,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPML_CC *, setList,
    const TPML_CC *, clearList);
MAKE_ESYS_6(Esys_PP_Commands_Async,
    ESYS_TR, auth,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPML_CC *, setList,
    const TPML_CC *, clearList);
MAKE_ESYS_0(Esys_PP_Commands_Finish);
MAKE_ESYS_5(Esys_SetAlgorithmSet,
    ESYS_TR, authHandle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    UINT32, algorithmSet);
MAKE_ESYS_5(Esys_SetAlgorithmSet_Async,
    ESYS_TR, authHandle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    UINT32, algorithmSet);
MAKE_ESYS_0(Esys_SetAlgorithmSet_Finish);
MAKE_ESYS_7(Esys_FieldUpgradeStart,
    ESYS_TR, authorization,
    ESYS_TR, keyHandle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_DIGEST *, fuDigest,
    const TPMT_SIGNATURE *, manifestSignature);
MAKE_ESYS_7(Esys_FieldUpgradeStart_Async,
    ESYS_TR, authorization,
    ESYS_TR, keyHandle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_DIGEST *, fuDigest,
    const TPMT_SIGNATURE *, manifestSignature);
MAKE_ESYS_0(Esys_FieldUpgradeStart_Finish);
MAKE_ESYS_6(Esys_FieldUpgradeData,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_MAX_BUFFER *, fuData,
    TPMT_HA **, nextDigest,
    TPMT_HA **, firstDigest);
MAKE_ESYS_4(Esys_FieldUpgradeData_Async,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_MAX_BUFFER *, fuData);
MAKE_ESYS_2(Esys_FieldUpgradeData_Finish,
    TPMT_HA **, nextDigest,
    TPMT_HA **, firstDigest);
MAKE_ESYS_5(Esys_FirmwareRead,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    UINT32, sequenceNumber,
    TPM2B_MAX_BUFFER **, fuData);
MAKE_ESYS_4(Esys_FirmwareRead_Async,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    UINT32, sequenceNumber);
MAKE_ESYS_1(Esys_FirmwareRead_Finish,
    TPM2B_MAX_BUFFER **, fuData);
MAKE_ESYS_2(Esys_ContextSave,
    ESYS_TR, saveHandle,
    TPMS_CONTEXT **, context);
MAKE_ESYS_1(Esys_ContextSave_Async,
    ESYS_TR, saveHandle);
MAKE_ESYS_1(Esys_ContextSave_Finish,
    TPMS_CONTEXT **, context);
MAKE_ESYS_2(Esys_ContextLoad,
    const TPMS_CONTEXT *, context,
    ESYS_TR *, loadedHandle);
MAKE_ESYS_1(Esys_ContextLoad_Async,
    const TPMS_CONTEXT *, context);
MAKE_ESYS_1(Esys_ContextLoad_Finish,
    ESYS_TR *, loadedHandle);
MAKE_ESYS_1(Esys_FlushContext,
    ESYS_TR, flushHandle);
MAKE_ESYS_1(Esys_FlushContext_Async,
    ESYS_TR, flushHandle);
MAKE_ESYS_0(Esys_FlushContext_Finish);
MAKE_ESYS_7(Esys_EvictControl,
    ESYS_TR, auth,
    ESYS_TR, objectHandle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    TPMI_DH_PERSISTENT, persistentHandle,
    ESYS_TR *, newObjectHandle);
MAKE_ESYS_6(Esys_EvictControl_Async,
    ESYS_TR, auth,
    ESYS_TR, objectHandle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    TPMI_DH_PERSISTENT, persistentHandle);
MAKE_ESYS_1(Esys_EvictControl_Finish,
    ESYS_TR *, newObjectHandle);
MAKE_ESYS_4(Esys_ReadClock,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    TPMS_TIME_INFO **, currentTime);
MAKE_ESYS_3(Esys_ReadClock_Async,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3);
MAKE_ESYS_1(Esys_ReadClock_Finish,
    TPMS_TIME_INFO **, currentTime);
MAKE_ESYS_5(Esys_ClockSet,
    ESYS_TR, auth,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    UINT64, newTime);
MAKE_ESYS_5(Esys_ClockSet_Async,
    ESYS_TR, auth,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    UINT64, newTime);
MAKE_ESYS_0(Esys_ClockSet_Finish);
MAKE_ESYS_5(Esys_ClockRateAdjust,
    ESYS_TR, auth,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    TPM2_CLOCK_ADJUST, rateAdjust);
MAKE_ESYS_5(Esys_ClockRateAdjust_Async,
    ESYS_TR, auth,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    TPM2_CLOCK_ADJUST, rateAdjust);
MAKE_ESYS_0(Esys_ClockRateAdjust_Finish);
MAKE_ESYS_8(Esys_GetCapability,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    TPM2_CAP, capability,
    UINT32, property,
    UINT32, propertyCount,
    TPMI_YES_NO *, moreData,
    TPMS_CAPABILITY_DATA **, capabilityData);
MAKE_ESYS_6(Esys_GetCapability_Async,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    TPM2_CAP, capability,
    UINT32, property,
    UINT32, propertyCount);
MAKE_ESYS_2(Esys_GetCapability_Finish,
    TPMI_YES_NO *, moreData,
    TPMS_CAPABILITY_DATA **, capabilityData);
MAKE_ESYS_4(Esys_TestParms,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPMT_PUBLIC_PARMS *, parameters);
MAKE_ESYS_4(Esys_TestParms_Async,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPMT_PUBLIC_PARMS *, parameters);
MAKE_ESYS_0(Esys_TestParms_Finish);
MAKE_ESYS_7(Esys_NV_DefineSpace,
    ESYS_TR, authHandle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_AUTH *, auth,
    const TPM2B_NV_PUBLIC *, publicInfo,
    ESYS_TR *, nvHandle);
MAKE_ESYS_6(Esys_NV_DefineSpace_Async,
    ESYS_TR, authHandle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_AUTH *, auth,
    const TPM2B_NV_PUBLIC *, publicInfo);
MAKE_ESYS_1(Esys_NV_DefineSpace_Finish,
    ESYS_TR *, nvHandle);
MAKE_ESYS_5(Esys_NV_UndefineSpace,
    ESYS_TR, authHandle,
    ESYS_TR, nvIndex,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3);
MAKE_ESYS_5(Esys_NV_UndefineSpace_Async,
    ESYS_TR, authHandle,
    ESYS_TR, nvIndex,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3);
MAKE_ESYS_0(Esys_NV_UndefineSpace_Finish);
MAKE_ESYS_5(Esys_NV_UndefineSpaceSpecial,
    ESYS_TR, nvIndex,
    ESYS_TR, platform,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3);
MAKE_ESYS_5(Esys_NV_UndefineSpaceSpecial_Async,
    ESYS_TR, nvIndex,
    ESYS_TR, platform,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3);
MAKE_ESYS_0(Esys_NV_UndefineSpaceSpecial_Finish);
MAKE_ESYS_6(Esys_NV_ReadPublic,
    ESYS_TR, nvIndex,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    TPM2B_NV_PUBLIC **, nvPublic,
    TPM2B_NAME **, nvName);
MAKE_ESYS_4(Esys_NV_ReadPublic_Async,
    ESYS_TR, nvIndex,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3);
MAKE_ESYS_2(Esys_NV_ReadPublic_Finish,
    TPM2B_NV_PUBLIC **, nvPublic,
    TPM2B_NAME **, nvName);
MAKE_ESYS_7(Esys_NV_Write,
    ESYS_TR, authHandle,
    ESYS_TR, nvIndex,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_MAX_NV_BUFFER *, data,
    UINT16, offset);
MAKE_ESYS_7(Esys_NV_Write_Async,
    ESYS_TR, authHandle,
    ESYS_TR, nvIndex,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_MAX_NV_BUFFER *, data,
    UINT16, offset);
MAKE_ESYS_0(Esys_NV_Write_Finish);
MAKE_ESYS_5(Esys_NV_Increment,
    ESYS_TR, authHandle,
    ESYS_TR, nvIndex,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3);
MAKE_ESYS_5(Esys_NV_Increment_Async,
    ESYS_TR, authHandle,
    ESYS_TR, nvIndex,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3);
MAKE_ESYS_0(Esys_NV_Increment_Finish);
MAKE_ESYS_6(Esys_NV_Extend,
    ESYS_TR, authHandle,
    ESYS_TR, nvIndex,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_MAX_NV_BUFFER *, data);
MAKE_ESYS_6(Esys_NV_Extend_Async,
    ESYS_TR, authHandle,
    ESYS_TR, nvIndex,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_MAX_NV_BUFFER *, data);
MAKE_ESYS_0(Esys_NV_Extend_Finish);
MAKE_ESYS_6(Esys_NV_SetBits,
    ESYS_TR, authHandle,
    ESYS_TR, nvIndex,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    UINT64, bits);
MAKE_ESYS_6(Esys_NV_SetBits_Async,
    ESYS_TR, authHandle,
    ESYS_TR, nvIndex,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    UINT64, bits);
MAKE_ESYS_0(Esys_NV_SetBits_Finish);
MAKE_ESYS_5(Esys_NV_WriteLock,
    ESYS_TR, authHandle,
    ESYS_TR, nvIndex,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3);
MAKE_ESYS_5(Esys_NV_WriteLock_Async,
    ESYS_TR, authHandle,
    ESYS_TR, nvIndex,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3);
MAKE_ESYS_0(Esys_NV_WriteLock_Finish);
MAKE_ESYS_4(Esys_NV_GlobalWriteLock,
    ESYS_TR, authHandle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3);
MAKE_ESYS_4(Esys_NV_GlobalWriteLock_Async,
    ESYS_TR, authHandle,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3);
MAKE_ESYS_0(Esys_NV_GlobalWriteLock_Finish);
MAKE_ESYS_8(Esys_NV_Read,
    ESYS_TR, authHandle,
    ESYS_TR, nvIndex,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    UINT16, size,
    UINT16, offset,
    TPM2B_MAX_NV_BUFFER **, data);
MAKE_ESYS_7(Esys_NV_Read_Async,
    ESYS_TR, authHandle,
    ESYS_TR, nvIndex,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    UINT16, size,
    UINT16, offset);
MAKE_ESYS_1(Esys_NV_Read_Finish,
    TPM2B_MAX_NV_BUFFER **, data);
MAKE_ESYS_5(Esys_NV_ReadLock,
    ESYS_TR, authHandle,
    ESYS_TR, nvIndex,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3);
MAKE_ESYS_5(Esys_NV_ReadLock_Async,
    ESYS_TR, authHandle,
    ESYS_TR, nvIndex,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3);
MAKE_ESYS_0(Esys_NV_ReadLock_Finish);
MAKE_ESYS_5(Esys_NV_ChangeAuth,
    ESYS_TR, nvIndex,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_AUTH *, newAuth);
MAKE_ESYS_5(Esys_NV_ChangeAuth_Async,
    ESYS_TR, nvIndex,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_AUTH *, newAuth);
MAKE_ESYS_0(Esys_NV_ChangeAuth_Finish);
MAKE_ESYS_12(Esys_NV_Certify,
    ESYS_TR, signHandle,
    ESYS_TR, authHandle,
    ESYS_TR, nvIndex,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_DATA *, qualifyingData,
    const TPMT_SIG_SCHEME *, inScheme,
    UINT16, size,
    UINT16, offset,
    TPM2B_ATTEST **, certifyInfo,
    TPMT_SIGNATURE **, signature);
MAKE_ESYS_10(Esys_NV_Certify_Async,
    ESYS_TR, signHandle,
    ESYS_TR, authHandle,
    ESYS_TR, nvIndex,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_DATA *, qualifyingData,
    const TPMT_SIG_SCHEME *, inScheme,
    UINT16, size,
    UINT16, offset);
MAKE_ESYS_2(Esys_NV_Certify_Finish,
    TPM2B_ATTEST **, certifyInfo,
    TPMT_SIGNATURE **, signature);
MAKE_ESYS_5(Esys_Vendor_TCG_Test,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_DATA *, inputData,
    TPM2B_DATA **, outputData);
MAKE_ESYS_4(Esys_Vendor_TCG_Test_Async,
    ESYS_TR, shandle1,
    ESYS_TR, shandle2,
    ESYS_TR, shandle3,
    const TPM2B_DATA *, inputData);
MAKE_ESYS_1(Esys_Vendor_TCG_Test_Finish,
    TPM2B_DATA **, outputData);
MAKE_ESYS_1(Esys_GetSysContext,
    TSS2_SYS_CONTEXT **, sys_context);
MAKE_ESYS_1(Esys_SetCryptoCallbacks,
    ESYS_CRYPTO_CALLBACKS *, callbacks);
