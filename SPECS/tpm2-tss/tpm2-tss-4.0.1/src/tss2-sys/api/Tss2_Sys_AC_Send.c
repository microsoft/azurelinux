/* SPDX-License-Identifier: BSD-2-Clause */
/***********************************************************************;
 * Copyright (c) 2017, Intel Corporation
 * All rights reserved.
 ***********************************************************************/

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include "tss2_tpm2_types.h"
#include "tss2_mu.h"
#include "sysapi_util.h"

TSS2_RC Tss2_Sys_AC_Send_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_DH_OBJECT sendObject,
    TPMI_RH_NV_AUTH authHandle,
    TPMI_RH_AC ac,
    TPM2B_MAX_BUFFER *acDataIn)
{
    _TSS2_SYS_CONTEXT_BLOB *ctx = syscontext_cast(sysContext);
    TSS2_RC rval;

    if (!ctx)
        return TSS2_SYS_RC_BAD_REFERENCE;

    rval = CommonPreparePrologue(ctx, TPM2_CC_AC_Send);
    if (rval)
        return rval;

    rval = Tss2_MU_TPM2_HANDLE_Marshal(sendObject, ctx->cmdBuffer,
                                       ctx->maxCmdSize,
                                       &ctx->nextData);
    if (rval)
        return rval;

    rval = Tss2_MU_TPM2_HANDLE_Marshal(authHandle, ctx->cmdBuffer,
                                       ctx->maxCmdSize,
                                       &ctx->nextData);
    if (rval)
        return rval;

    rval = Tss2_MU_TPM2_HANDLE_Marshal(ac, ctx->cmdBuffer,
                                       ctx->maxCmdSize,
                                       &ctx->nextData);
    if (rval)
        return rval;

    if (!acDataIn) {
        ctx->decryptNull = 1;

        rval = Tss2_MU_UINT16_Marshal(0, ctx->cmdBuffer,
                                      ctx->maxCmdSize,
                                      &ctx->nextData);
    } else {

        rval = Tss2_MU_TPM2B_MAX_BUFFER_Marshal(acDataIn, ctx->cmdBuffer,
                                                ctx->maxCmdSize,
                                                &ctx->nextData);
    }
    if (rval)
        return rval;

    ctx->decryptAllowed = 1;
    ctx->encryptAllowed = 0;
    ctx->authAllowed = 1;

    return CommonPrepareEpilogue(ctx);
}

TSS2_RC Tss2_Sys_AC_Send_Complete(
    TSS2_SYS_CONTEXT *sysContext,
    TPMS_AC_OUTPUT *acDataOut)
{
    _TSS2_SYS_CONTEXT_BLOB *ctx = syscontext_cast(sysContext);
    TSS2_RC rval;

    if (!ctx)
        return TSS2_SYS_RC_BAD_REFERENCE;

    rval = CommonComplete(ctx);
    if (rval)
        return rval;

    return Tss2_MU_TPMS_AC_OUTPUT_Unmarshal(ctx->cmdBuffer,
                                            ctx->maxCmdSize,
                                            &ctx->nextData,
                                            acDataOut);
}

TSS2_RC Tss2_Sys_AC_Send(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_DH_OBJECT sendObject,
    TPMI_RH_NV_AUTH authHandle,
    TPMI_RH_AC ac,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    TPM2B_MAX_BUFFER *acDataIn,
    TPMS_AC_OUTPUT *acDataOut,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray)
{
    _TSS2_SYS_CONTEXT_BLOB *ctx = syscontext_cast(sysContext);
    TSS2_RC rval;

    rval = Tss2_Sys_AC_Send_Prepare(sysContext, sendObject, authHandle, ac,
                                    acDataIn);
    if (rval)
        return rval;

    rval = CommonOneCall(ctx, cmdAuthsArray, rspAuthsArray);
    if (rval)
        return rval;

    return Tss2_Sys_AC_Send_Complete(sysContext, acDataOut);
}
