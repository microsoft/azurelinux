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

TSS2_RC Tss2_Sys_ZGen_2Phase_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_DH_OBJECT keyA,
    const TPM2B_ECC_POINT *inQsB,
    const TPM2B_ECC_POINT *inQeB,
    TPMI_ECC_KEY_EXCHANGE inScheme,
    UINT16 counter)
{
    _TSS2_SYS_CONTEXT_BLOB *ctx = syscontext_cast(sysContext);
    TSS2_RC rval;

    if (!ctx)
        return TSS2_SYS_RC_BAD_REFERENCE;

    rval = CommonPreparePrologue(ctx, TPM2_CC_ZGen_2Phase);
    if (rval)
        return rval;

    rval = Tss2_MU_UINT32_Marshal(keyA, ctx->cmdBuffer,
                                  ctx->maxCmdSize,
                                  &ctx->nextData);
    if (rval)
        return rval;

    if (!inQsB) {
        ctx->decryptNull = 1;

        rval = Tss2_MU_UINT16_Marshal(0, ctx->cmdBuffer,
                                      ctx->maxCmdSize,
                                      &ctx->nextData);
    } else {

        rval = Tss2_MU_TPM2B_ECC_POINT_Marshal(inQsB, ctx->cmdBuffer,
                                               ctx->maxCmdSize,
                                               &ctx->nextData);
    }

    if (rval)
        return rval;

    if (!inQeB) {
        rval = Tss2_MU_UINT16_Marshal(0, ctx->cmdBuffer,
                                      ctx->maxCmdSize,
                                      &ctx->nextData);

    } else {

        rval = Tss2_MU_TPM2B_ECC_POINT_Marshal(inQeB, ctx->cmdBuffer,
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

    rval = Tss2_MU_UINT16_Marshal(counter, ctx->cmdBuffer,
                                  ctx->maxCmdSize,
                                  &ctx->nextData);
    if (rval)
        return rval;

    ctx->decryptAllowed = 1;
    ctx->encryptAllowed = 1;
    ctx->authAllowed = 1;

    return CommonPrepareEpilogue(ctx);
}

TSS2_RC Tss2_Sys_ZGen_2Phase_Complete(
    TSS2_SYS_CONTEXT *sysContext,
    TPM2B_ECC_POINT *outZ1,
    TPM2B_ECC_POINT *outZ2)
{
    _TSS2_SYS_CONTEXT_BLOB *ctx = syscontext_cast(sysContext);
    TSS2_RC rval;

    if (!ctx)
        return TSS2_SYS_RC_BAD_REFERENCE;

    rval = CommonComplete(ctx);
    if (rval)
        return rval;

    rval = Tss2_MU_TPM2B_ECC_POINT_Unmarshal(ctx->cmdBuffer,
                                             ctx->maxCmdSize,
                                             &ctx->nextData, outZ1);
    if (rval)
        return rval;

    return Tss2_MU_TPM2B_ECC_POINT_Unmarshal(ctx->cmdBuffer,
                                             ctx->maxCmdSize,
                                             &ctx->nextData, outZ2);
}

TSS2_RC Tss2_Sys_ZGen_2Phase(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_DH_OBJECT keyA,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    const TPM2B_ECC_POINT *inQsB,
    const TPM2B_ECC_POINT *inQeB,
    TPMI_ECC_KEY_EXCHANGE inScheme,
    UINT16 counter,
    TPM2B_ECC_POINT *outZ1,
    TPM2B_ECC_POINT *outZ2,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray)
{
    _TSS2_SYS_CONTEXT_BLOB *ctx = syscontext_cast(sysContext);
    TSS2_RC rval;

    rval = Tss2_Sys_ZGen_2Phase_Prepare(sysContext, keyA, inQsB, inQeB,
                                        inScheme, counter);
    if (rval)
        return rval;

    rval = CommonOneCall(ctx, cmdAuthsArray, rspAuthsArray);
    if (rval)
        return rval;

    return Tss2_Sys_ZGen_2Phase_Complete(sysContext, outZ1, outZ2);
}
