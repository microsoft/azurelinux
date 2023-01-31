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

TSS2_RC Tss2_Sys_ActivateCredential_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_DH_OBJECT activateHandle,
    TPMI_DH_OBJECT keyHandle,
    const TPM2B_ID_OBJECT *credentialBlob,
    const TPM2B_ENCRYPTED_SECRET *secret)
{
    _TSS2_SYS_CONTEXT_BLOB *ctx = syscontext_cast(sysContext);
    TSS2_RC rval;

    if (!ctx)
        return TSS2_SYS_RC_BAD_REFERENCE;

    rval = CommonPreparePrologue(ctx, TPM2_CC_ActivateCredential);
    if (rval)
        return rval;

    rval = Tss2_MU_UINT32_Marshal(activateHandle, ctx->cmdBuffer,
                                  ctx->maxCmdSize,
                                  &ctx->nextData);
    if (rval)
        return rval;

    rval = Tss2_MU_UINT32_Marshal(keyHandle, ctx->cmdBuffer,
                                  ctx->maxCmdSize,
                                  &ctx->nextData);
    if (rval)
        return rval;

    if (!credentialBlob) {
        ctx->decryptNull = 1;

        rval = Tss2_MU_UINT16_Marshal(0, ctx->cmdBuffer,
                                      ctx->maxCmdSize,
                                      &ctx->nextData);
    } else {

        rval = Tss2_MU_TPM2B_ID_OBJECT_Marshal(credentialBlob,
                                               ctx->cmdBuffer,
                                               ctx->maxCmdSize,
                                               &ctx->nextData);
    }

    if (rval)
        return rval;

    if (!secret) {
        rval = Tss2_MU_UINT16_Marshal(0, ctx->cmdBuffer,
                                      ctx->maxCmdSize,
                                      &ctx->nextData);

    } else {

        rval = Tss2_MU_TPM2B_ENCRYPTED_SECRET_Marshal(secret,
                                                      ctx->cmdBuffer,
                                                      ctx->maxCmdSize,
                                                      &ctx->nextData);
    }

    if (rval)
        return rval;

    ctx->decryptAllowed = 1;
    ctx->encryptAllowed = 1;
    ctx->authAllowed = 1;

    return CommonPrepareEpilogue(ctx);
}

TSS2_RC Tss2_Sys_ActivateCredential_Complete(
    TSS2_SYS_CONTEXT *sysContext,
    TPM2B_DIGEST *certInfo)
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
                                          certInfo);
}

TSS2_RC Tss2_Sys_ActivateCredential(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_DH_OBJECT activateHandle,
    TPMI_DH_OBJECT keyHandle,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    const TPM2B_ID_OBJECT *credentialBlob,
    const TPM2B_ENCRYPTED_SECRET *secret,
    TPM2B_DIGEST *certInfo,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray)
{
    TSS2_RC rval;
    _TSS2_SYS_CONTEXT_BLOB *ctx = syscontext_cast(sysContext);

    rval = Tss2_Sys_ActivateCredential_Prepare(sysContext, activateHandle,
                                               keyHandle, credentialBlob,
                                               secret);
    if (rval)
        return rval;

    rval = CommonOneCall(ctx, cmdAuthsArray, rspAuthsArray);
    if (rval)
        return rval;

    return Tss2_Sys_ActivateCredential_Complete(sysContext, certInfo);
}
