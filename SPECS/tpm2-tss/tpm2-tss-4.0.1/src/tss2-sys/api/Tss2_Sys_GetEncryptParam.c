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

TSS2_RC Tss2_Sys_GetEncryptParam(
    TSS2_SYS_CONTEXT *sysContext,
    size_t *encryptParamSize,
    const uint8_t **encryptParamBuffer)
{
    _TSS2_SYS_CONTEXT_BLOB *ctx = syscontext_cast(sysContext);
    uint8_t *offset;

    if (!encryptParamSize || !encryptParamBuffer || !ctx)
        return TSS2_SYS_RC_BAD_REFERENCE;

    if (ctx->encryptAllowed == 0)
        return TSS2_SYS_RC_NO_ENCRYPT_PARAM;

    if (ctx->previousStage != CMD_STAGE_RECEIVE_RESPONSE)
        return TSS2_SYS_RC_BAD_SEQUENCE;

    if (BE_TO_HOST_16(resp_header_from_cxt(ctx)->tag) == TPM2_ST_NO_SESSIONS)
        return TSS2_SYS_RC_NO_ENCRYPT_PARAM;

    /* Get first parameter, interpret it as a TPM2B and return its size field
     * and a pointer to its buffer area. */
    offset = ctx->cmdBuffer
            + sizeof(TPM20_Header_Out)
            + ctx->numResponseHandles * sizeof(TPM2_HANDLE)
            + sizeof(TPM2_PARAMETER_SIZE);

    *encryptParamSize = BE_TO_HOST_16(*((UINT16 *)offset));
    *encryptParamBuffer = offset + sizeof(UINT16);

    return TSS2_RC_SUCCESS;
}
