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

TSS2_RC Tss2_Sys_EncryptDecrypt2_Prepare (
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_DH_OBJECT keyHandle,
    const TPM2B_MAX_BUFFER *inData,
    TPMI_YES_NO decrypt,
    TPMI_ALG_CIPHER_MODE mode,
    const TPM2B_IV *ivIn)
{
    _TSS2_SYS_CONTEXT_BLOB *ctx = syscontext_cast(sysContext);
    TSS2_RC rval;

    if (!ctx)
        return TSS2_SYS_RC_BAD_REFERENCE;

    rval = CommonPreparePrologue (ctx, TPM2_CC_EncryptDecrypt2);
    if (rval)
        return rval;

    rval = Tss2_MU_UINT32_Marshal (keyHandle,
                                   ctx->cmdBuffer,
                                   ctx->maxCmdSize,
                                   &ctx->nextData);
    if (rval)
        return rval;

    if (!inData) {
        rval = Tss2_MU_UINT16_Marshal(0, ctx->cmdBuffer,
                                      ctx->maxCmdSize,
                                      &ctx->nextData);

    } else {

        rval = Tss2_MU_TPM2B_MAX_BUFFER_Marshal (inData,
                                                 ctx->cmdBuffer,
                                                 ctx->maxCmdSize,
                                                 &ctx->nextData);
    }

    if (rval)
        return rval;

    rval = Tss2_MU_UINT8_Marshal (decrypt,
                                  ctx->cmdBuffer,
                                  ctx->maxCmdSize,
                                  &ctx->nextData);
    if (rval)
        return rval;

    rval = Tss2_MU_UINT16_Marshal (mode,
                                   ctx->cmdBuffer,
                                   ctx->maxCmdSize,
                                   &ctx->nextData);
    if (rval)
        return rval;

    if (!ivIn) {
        rval = Tss2_MU_UINT16_Marshal(0, ctx->cmdBuffer,
                                      ctx->maxCmdSize,
                                      &ctx->nextData);

    } else {

        rval = Tss2_MU_TPM2B_IV_Marshal (ivIn,
                                         ctx->cmdBuffer,
                                         ctx->maxCmdSize,
                                         &ctx->nextData);
    }

    if (rval)
        return rval;

    ctx->decryptAllowed = 1;
    ctx->encryptAllowed = 1;
    ctx->authAllowed = 1;

    return CommonPrepareEpilogue (ctx);
}

TSS2_RC Tss2_Sys_EncryptDecrypt2_Complete (
    TSS2_SYS_CONTEXT *sysContext,
    TPM2B_MAX_BUFFER *outData,
    TPM2B_IV *ivOut)
{
    _TSS2_SYS_CONTEXT_BLOB *ctx = syscontext_cast(sysContext);
    TSS2_RC rval;

    if (!ctx)
        return TSS2_SYS_RC_BAD_REFERENCE;

    rval = CommonComplete (ctx);
    if (rval)
        return rval;

    rval = Tss2_MU_TPM2B_MAX_BUFFER_Unmarshal (ctx->cmdBuffer,
                                               ctx->maxCmdSize,
                                               &ctx->nextData,
                                               outData);
    if (rval)
        return rval;

    return Tss2_MU_TPM2B_IV_Unmarshal (ctx->cmdBuffer,
                                       ctx->maxCmdSize,
                                       &ctx->nextData,
                                       ivOut);
}

TSS2_RC Tss2_Sys_EncryptDecrypt2 (
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_DH_OBJECT keyHandle,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    const TPM2B_MAX_BUFFER *inData,
    TPMI_YES_NO decrypt,
    TPMI_ALG_CIPHER_MODE mode,
    const TPM2B_IV *ivIn,
    TPM2B_MAX_BUFFER *outData,
    TPM2B_IV *ivOut,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray)
{
    _TSS2_SYS_CONTEXT_BLOB *ctx = syscontext_cast(sysContext);
    TSS2_RC rval;

    rval = Tss2_Sys_EncryptDecrypt2_Prepare (sysContext,
                                             keyHandle,
                                             inData,
                                             decrypt,
                                             mode,
                                             ivIn);
    if (rval)
        return rval;

    rval = CommonOneCall (ctx, cmdAuthsArray, rspAuthsArray);
    if (rval)
        return rval;

    return Tss2_Sys_EncryptDecrypt2_Complete (sysContext, outData, ivOut);
}
