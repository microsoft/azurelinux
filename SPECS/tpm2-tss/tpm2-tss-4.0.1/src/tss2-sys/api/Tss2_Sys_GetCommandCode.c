/* SPDX-License-Identifier: BSD-2-Clause */
/***********************************************************************;
 * Copyright (c) 2015 - 2018, Intel Corporation
 * All rights reserved.
 ***********************************************************************/
#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <string.h>

#include "tss2_tpm2_types.h"
#include "tss2_mu.h"
#include "sysapi_util.h"
#include "util/tss2_endian.h"

TSS2_RC Tss2_Sys_GetCommandCode(
    TSS2_SYS_CONTEXT *sysContext,
    UINT8 *commandCode)
{
    _TSS2_SYS_CONTEXT_BLOB *ctx = syscontext_cast(sysContext);

    if (!ctx || !commandCode)
        return TSS2_SYS_RC_BAD_REFERENCE;

    if (ctx->previousStage == CMD_STAGE_INITIALIZE)
        return TSS2_SYS_RC_BAD_SEQUENCE;

    TPM2_CC tmp = HOST_TO_BE_32(ctx->commandCode);
    memcpy(commandCode, (void *)&tmp, sizeof(tmp));

    return TSS2_RC_SUCCESS;
}
