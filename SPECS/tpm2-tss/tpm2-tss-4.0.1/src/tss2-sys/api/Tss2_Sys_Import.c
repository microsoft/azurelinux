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

TSS2_RC Tss2_Sys_Import_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_DH_OBJECT parentHandle,
    const TPM2B_DATA *encryptionKey,
    const TPM2B_PUBLIC *objectPublic,
    const TPM2B_PRIVATE *duplicate,
    const TPM2B_ENCRYPTED_SECRET *inSymSeed,
    const TPMT_SYM_DEF_OBJECT *symmetricAlg)
{
    _TSS2_SYS_CONTEXT_BLOB *ctx = syscontext_cast(sysContext);
    TSS2_RC rval;

    if (!ctx || !symmetricAlg)
        return TSS2_SYS_RC_BAD_REFERENCE;

    rval = CommonPreparePrologue(ctx, TPM2_CC_Import);
    if (rval)
        return rval;

    rval = Tss2_MU_UINT32_Marshal(parentHandle, ctx->cmdBuffer,
                                  ctx->maxCmdSize,
                                  &ctx->nextData);
    if (rval)
        return rval;

    if (!encryptionKey) {
        ctx->decryptNull = 1;

        rval = Tss2_MU_UINT16_Marshal(0, ctx->cmdBuffer,
                                      ctx->maxCmdSize,
                                      &ctx->nextData);
    } else {

        rval = Tss2_MU_TPM2B_DATA_Marshal(encryptionKey, ctx->cmdBuffer,
                                          ctx->maxCmdSize,
                                          &ctx->nextData);
    }

    if (rval)
        return rval;

    if (!objectPublic) {
        rval = Tss2_MU_UINT16_Marshal(0, ctx->cmdBuffer,
                                      ctx->maxCmdSize,
                                      &ctx->nextData);

    } else {
        rval = ValidatePublicTemplate(objectPublic);

        if (rval)
            return rval;
        rval = Tss2_MU_TPM2B_PUBLIC_Marshal(objectPublic, ctx->cmdBuffer,
                                            ctx->maxCmdSize,
                                            &ctx->nextData);
    }

    if (rval)
        return rval;

    if (!duplicate) {
        rval = Tss2_MU_UINT16_Marshal(0, ctx->cmdBuffer,
                                      ctx->maxCmdSize,
                                      &ctx->nextData);

    } else {

        rval = Tss2_MU_TPM2B_PRIVATE_Marshal(duplicate, ctx->cmdBuffer,
                                             ctx->maxCmdSize,
                                             &ctx->nextData);
    }

    if (rval)
        return rval;

    if (!inSymSeed) {
        rval = Tss2_MU_UINT16_Marshal(0, ctx->cmdBuffer,
                                      ctx->maxCmdSize,
                                      &ctx->nextData);

    } else {

        rval = Tss2_MU_TPM2B_ENCRYPTED_SECRET_Marshal(inSymSeed,
                                                      ctx->cmdBuffer,
                                                      ctx->maxCmdSize,
                                                      &ctx->nextData);
    }

    if (rval)
        return rval;

    rval = Tss2_MU_TPMT_SYM_DEF_OBJECT_Marshal(symmetricAlg,
                                               ctx->cmdBuffer,
                                               ctx->maxCmdSize,
                                               &ctx->nextData);
    if (rval)
        return rval;

    ctx->decryptAllowed = 1;
    ctx->encryptAllowed = 1;
    ctx->authAllowed = 1;

    return CommonPrepareEpilogue(ctx);
}

TSS2_RC Tss2_Sys_Import_Complete(
    TSS2_SYS_CONTEXT *sysContext,
    TPM2B_PRIVATE *outPrivate)
{
    _TSS2_SYS_CONTEXT_BLOB *ctx = syscontext_cast(sysContext);
    TSS2_RC rval;

    if (!ctx)
        return TSS2_SYS_RC_BAD_REFERENCE;

    rval = CommonComplete(ctx);
    if (rval)
        return rval;

    return Tss2_MU_TPM2B_PRIVATE_Unmarshal(ctx->cmdBuffer,
                                           ctx->maxCmdSize,
                                           &ctx->nextData,
                                           outPrivate);
}

TSS2_RC Tss2_Sys_Import(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_DH_OBJECT parentHandle,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    const TPM2B_DATA *encryptionKey,
    const TPM2B_PUBLIC *objectPublic,
    const TPM2B_PRIVATE *duplicate,
    const TPM2B_ENCRYPTED_SECRET *inSymSeed,
    const TPMT_SYM_DEF_OBJECT *symmetricAlg,
    TPM2B_PRIVATE *outPrivate,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray)
{
    _TSS2_SYS_CONTEXT_BLOB *ctx = syscontext_cast(sysContext);
    TSS2_RC rval;

    if (!symmetricAlg)
        return TSS2_SYS_RC_BAD_REFERENCE;

    rval = Tss2_Sys_Import_Prepare(sysContext, parentHandle, encryptionKey,
                                   objectPublic, duplicate, inSymSeed,
                                   symmetricAlg);
    if (rval)
        return rval;

    rval = CommonOneCall(ctx, cmdAuthsArray, rspAuthsArray);
    if (rval)
        return rval;

    return Tss2_Sys_Import_Complete(sysContext, outPrivate);
}
