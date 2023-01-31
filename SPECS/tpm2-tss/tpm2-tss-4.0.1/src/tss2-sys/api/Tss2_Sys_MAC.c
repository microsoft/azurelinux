/* SPDX-License-Identifier: BSD-2-Clause */
/***********************************************************************;
 * Copyright (c) 2015 - 2017, Intel Corporation
 * All rights reserved.
 ***********************************************************************/

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include "tss2_tpm2_types.h"
#include "tss2_mu.h"
#include "sysapi_util.h"

TSS2_RC Tss2_Sys_MAC_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_DH_OBJECT handle,
    const TPM2B_MAX_BUFFER *buffer,
    TPMI_ALG_MAC_SCHEME inScheme)
{
    _TSS2_SYS_CONTEXT_BLOB *ctx = syscontext_cast(sysContext);
    TSS2_RC rval;

    if (!ctx)
        return TSS2_SYS_RC_BAD_REFERENCE;

    if (IsAlgorithmWeak(hashAlg, 0))
        return TSS2_SYS_RC_BAD_VALUE;

    rval = CommonPreparePrologue(ctx, TPM2_CC_MAC);
    if (rval)
        return rval;

    rval = Tss2_MU_UINT32_Marshal(handle, ctx->cmdBuffer,
                                  ctx->maxCmdSize,
                                  &ctx->nextData);
    if (rval)
        return rval;

    if (!buffer) {
        ctx->decryptNull = 1;

        rval = Tss2_MU_UINT16_Marshal(0, ctx->cmdBuffer,
                                      ctx->maxCmdSize,
                                      &ctx->nextData);
    } else {

        rval = Tss2_MU_TPM2B_MAX_BUFFER_Marshal(buffer, ctx->cmdBuffer,
                                                ctx->maxCmdSize,
                                                &ctx->nextData);
    }

    if (rval)
        return rval;

    rval = Tss2_MU_UINT16_Marshal(inScheme, ctx->cmdBuffer,
                                  ctx->maxCmdSize,
                                  &ctx->nextData);
    if (rval)
        return rval;

    ctx->decryptAllowed = 1;
    ctx->encryptAllowed = 1;
    ctx->authAllowed = 1;

    return CommonPrepareEpilogue(ctx);
}

TSS2_RC Tss2_Sys_MAC_Complete(
    TSS2_SYS_CONTEXT *sysContext,
    TPM2B_DIGEST *outMAC)
{
    _TSS2_SYS_CONTEXT_BLOB *ctx = syscontext_cast(sysContext);
    TSS2_RC rval;

    if (!ctx)
        return TSS2_SYS_RC_BAD_REFERENCE;

    rval = CommonComplete(ctx);
    if (rval)
        return rval;

    return Tss2_MU_TPM2B_DIGEST_Unmarshal(ctx->cmdBuffer,
                                          ctx->maxCmdSize,
                                          &ctx->nextData,
                                          outMAC);
}

TSS2_RC Tss2_Sys_MAC(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_DH_OBJECT handle,
    const TSS2L_SYS_AUTH_COMMAND *cmdAuths,
    const TPM2B_MAX_BUFFER *buffer,
    TPMI_ALG_MAC_SCHEME inScheme,
    TPM2B_DIGEST *outMAC,
    TSS2L_SYS_AUTH_RESPONSE *rspAuths)
{
    _TSS2_SYS_CONTEXT_BLOB *ctx = syscontext_cast(sysContext);
    TSS2_RC rval;

    rval = Tss2_Sys_MAC_Prepare(sysContext, handle, buffer, inScheme);
    if (rval)
        return rval;

    rval = CommonOneCall(ctx, cmdAuths, rspAuths);
    if (rval)
        return rval;

    return Tss2_Sys_MAC_Complete(sysContext, outMAC);
}
