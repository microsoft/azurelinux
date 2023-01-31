/* SPDX-License-Identifier: BSD-2-Clause */
/***********************************************************************;
 * Copyright (c) 2015 - 2018, Intel Corporation
 * All rights reserved.
 ***********************************************************************/

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include "tss2_tpm2_types.h"
#include "tss2_mu.h"
#include "sysapi_util.h"
#include "util/tss2_endian.h"

TSS2_RC Tss2_Sys_GetDecryptParam(
    TSS2_SYS_CONTEXT *sysContext,
    size_t *decryptParamSize,
    const uint8_t **decryptParamBuffer)
{
    _TSS2_SYS_CONTEXT_BLOB *ctx = syscontext_cast(sysContext);
    TPM2B *decryptParam;

    if (!decryptParamSize || !decryptParamBuffer || !ctx)
        return TSS2_SYS_RC_BAD_REFERENCE;

    if (ctx->previousStage != CMD_STAGE_PREPARE)
        return TSS2_SYS_RC_BAD_SEQUENCE;

    if (ctx->decryptAllowed == 0)
        return TSS2_SYS_RC_NO_DECRYPT_PARAM;

    /* Get first parameter and return its size and a pointer to it. */
    decryptParam = (TPM2B *)(ctx->cpBuffer);
    *decryptParamSize = BE_TO_HOST_16(decryptParam->size);
    *decryptParamBuffer = decryptParam->buffer;

    return TSS2_RC_SUCCESS;
}
