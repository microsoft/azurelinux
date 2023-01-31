/* SPDX-License-Identifier: BSD-2-Clause */
/***********************************************************************
 * Copyright (c) 2015 - 2018, Intel Corporation
 *
 * All rights reserved.
 ***********************************************************************/

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include "util/tss2_endian.h"
#include "tss2_tpm2_types.h"
#include "tss2_mu.h"
#include "sysapi_util.h"
#include <string.h>

TSS2_RC Tss2_Sys_GetRspAuths(
    TSS2_SYS_CONTEXT *sysContext,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray)
{
    _TSS2_SYS_CONTEXT_BLOB *ctx = syscontext_cast(sysContext);
    TSS2_RC rval = TSS2_RC_SUCCESS;
    size_t offset = 0, offset_tmp;
    unsigned i = 0;
    UINT32 rspParamsSize;

    if (!ctx || !rspAuthsArray)
        return TSS2_SYS_RC_BAD_REFERENCE;

    if (ctx->previousStage != CMD_STAGE_RECEIVE_RESPONSE ||
        ctx->rsp_header.responseCode != TSS2_RC_SUCCESS ||
        ctx->authAllowed == 0)
        return TSS2_SYS_RC_BAD_SEQUENCE;

    if (TPM2_ST_SESSIONS != ctx->rsp_header.tag)
        return TSS2_SYS_RC_BAD_SEQUENCE;

    offset += sizeof(TPM20_Header_Out);
    offset += ctx->numResponseHandles * sizeof(TPM2_HANDLE);
    memcpy(&rspParamsSize, ctx->rspParamsSize, sizeof(rspParamsSize));
    offset += BE_TO_HOST_32(rspParamsSize);
    offset += sizeof(UINT32);
    offset_tmp = offset;

    /* Validate the auth area before copying it */
    for (i = 0; i < ctx->authsCount; i++) {

        if (offset_tmp > ctx->rsp_header.responseSize)
            return TSS2_SYS_RC_MALFORMED_RESPONSE;

        UINT16 tmp;
        memcpy(&tmp, ctx->cmdBuffer + offset_tmp, sizeof(UINT16));
        offset_tmp += sizeof(UINT16);
        offset_tmp += BE_TO_HOST_16(tmp);

        if (offset_tmp > ctx->rsp_header.responseSize)
            return TSS2_SYS_RC_MALFORMED_RESPONSE;

        offset_tmp += 1;

        if (offset_tmp > ctx->rsp_header.responseSize)
            return TSS2_SYS_RC_MALFORMED_RESPONSE;

        memcpy(&tmp, ctx->cmdBuffer + offset_tmp, sizeof(UINT16));
        offset_tmp += sizeof(UINT16);
        offset_tmp += BE_TO_HOST_16(tmp);

        if (offset_tmp > ctx->rsp_header.responseSize)
            return TSS2_SYS_RC_MALFORMED_RESPONSE;

        if (i + 1 > ctx->authsCount)
            return TSS2_SYS_RC_INVALID_SESSIONS;
    }

    /* Unmarshal the auth area */
    for (i = 0; i < ctx->authsCount; i++) {
        rval = Tss2_MU_TPMS_AUTH_RESPONSE_Unmarshal(ctx->cmdBuffer,
                                            ctx->maxCmdSize,
                                            &offset, &rspAuthsArray->auths[i]);
        if (rval)
            break;
    }

    rspAuthsArray->count = ctx->authsCount;

    return rval;
}
