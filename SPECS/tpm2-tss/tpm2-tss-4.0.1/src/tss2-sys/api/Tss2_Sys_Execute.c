/* SPDX-License-Identifier: BSD-2-Clause */
/***********************************************************************;
 * Copyright (c) 2015 - 2018, Intel Corporation
 * All rights reserved.
 ***********************************************************************/

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <inttypes.h>
#include <string.h>

#include "tss2_tpm2_types.h"
#include "tss2_mu.h"
#include "sysapi_util.h"
#include "util/tss2_endian.h"
#define LOGMODULE sys
#include "util/log.h"

TSS2_RC Tss2_Sys_ExecuteAsync(TSS2_SYS_CONTEXT *sysContext)
{
    _TSS2_SYS_CONTEXT_BLOB *ctx = syscontext_cast(sysContext);
    TSS2_RC rval;

    if (!ctx)
        return TSS2_SYS_RC_BAD_REFERENCE;

    if (ctx->previousStage != CMD_STAGE_PREPARE)
        return TSS2_SYS_RC_BAD_SEQUENCE;

    rval = Tss2_Tcti_Transmit(ctx->tctiContext,
                              HOST_TO_BE_32(req_header_from_cxt(ctx)->commandSize),
                              ctx->cmdBuffer);
    if (rval)
        return rval;

    /* Keep a copy of the cmd header to be able reissue the command
     * after receiving a TPM error
     */
    memcpy(ctx->cmd_header, ctx->cmdBuffer, sizeof(ctx->cmd_header));

    ctx->previousStage = CMD_STAGE_SEND_COMMAND;

    return rval;
}

TSS2_RC Tss2_Sys_ExecuteFinish(TSS2_SYS_CONTEXT *sysContext, int32_t timeout)
{
    _TSS2_SYS_CONTEXT_BLOB *ctx = syscontext_cast(sysContext);
    TSS2_RC rval;
    size_t response_size = 0;

    if (!ctx)
        return TSS2_SYS_RC_BAD_REFERENCE;

    if (ctx->previousStage != CMD_STAGE_SEND_COMMAND)
        return TSS2_SYS_RC_BAD_SEQUENCE;

    /*
	 * Call tcti_receive with NULL response buffer to get the actual size
	 * of the response. If we can read the response in multiple chunks
	 * then the tcti should read the response header first and give us
	 * the acctual size. If not it should set the response size to the
	 * maximum possible size.
     */
    rval = Tss2_Tcti_Receive(ctx->tctiContext, &response_size,
                             NULL, timeout);
    if (rval)
        return rval;

    if (response_size < sizeof(TPM20_Header_Out)) {
        ctx->previousStage = CMD_STAGE_PREPARE;
        return TSS2_SYS_RC_INSUFFICIENT_RESPONSE;
    }
    if (response_size > ctx->maxCmdSize) {
        ctx->previousStage = CMD_STAGE_PREPARE;
        LOG_ERROR("Response size to big: %zu > %u", response_size, ctx->maxCmdSize);
        return TSS2_SYS_RC_INSUFFICIENT_CONTEXT;
    }

    /* Then call receive again with the response buffer to read the response */
    rval = Tss2_Tcti_Receive(ctx->tctiContext, &response_size,
                             ctx->cmdBuffer, timeout);
    if (rval == TSS2_TCTI_RC_INSUFFICIENT_BUFFER) {
        LOG_ERROR("TCTI: Insufficient Buffer.");
        return TSS2_SYS_RC_INSUFFICIENT_CONTEXT;
    }

    if (rval)
        return rval;

    /*
     * Unmarshal the tag, response size, and response code as soon
     * as possible. Later processing code should get this data from
     * the TPM20_Header_Out in the context structure. No need to
     * unmarshal this stuff again.
     */
    ctx->nextData = 0;

    rval = Tss2_MU_TPM2_ST_Unmarshal(ctx->cmdBuffer,
                                     ctx->maxCmdSize,
                                     &ctx->nextData,
                                     &ctx->rsp_header.tag);
    if (rval) {
        LOG_ERROR("Unmarshaling response tag. RC=%" PRIx32, rval);
        return rval;
    }

    if (ctx->rsp_header.tag != TPM2_ST_SESSIONS &&
        ctx->rsp_header.tag != TPM2_ST_NO_SESSIONS) {
        if (ctx->rsp_header.tag == TPM2_ST_RSP_COMMAND) {
            LOG_ERROR("Unsupported device. The device is a TPM 1.2");
            return TSS2_SYS_RC_GENERAL_FAILURE;
        } else {
            LOG_ERROR("Malformed reponse: Invalid tag in response header: %" PRIx16,
                      ctx->rsp_header.tag);
            return TSS2_SYS_RC_MALFORMED_RESPONSE;
        }
    }

    rval = Tss2_MU_UINT32_Unmarshal(ctx->cmdBuffer,
                                     ctx->maxCmdSize,
                                     &ctx->nextData,
                                     &ctx->rsp_header.responseSize);
    if (rval)
        return rval;

    if (ctx->rsp_header.responseSize > ctx->maxCmdSize) {
        return TSS2_SYS_RC_MALFORMED_RESPONSE;
    }

    rval = Tss2_MU_UINT32_Unmarshal(ctx->cmdBuffer,
                                    ctx->maxCmdSize,
                                    &ctx->nextData,
                                    &ctx->rsp_header.responseCode);
    if (rval)
        return rval;

    rval = ctx->rsp_header.responseCode;

    /* If didn't receive enough response bytes, reset SAPI state machine to
     * CMD_STAGE_PREPARE. There's nothing else we can do for current command.
     */
    if (ctx->rsp_header.responseSize < sizeof(TPM20_Header_Out)) {
        ctx->previousStage = CMD_STAGE_PREPARE;
        return TSS2_SYS_RC_INSUFFICIENT_RESPONSE;
    }

    /* If we received a TPM error then reset SAPI state machine to
     * CMD_STAGE_PREPARE, and restore the command header so the command
     * can be reissued without going through the usual *_prepare stage.
     */
    if (rval && rval != TPM2_RC_INITIALIZE) {
        ctx->previousStage = CMD_STAGE_PREPARE;
        memcpy(ctx->cmdBuffer, ctx->cmd_header, sizeof(ctx->cmd_header));
        return rval;
    }

    ctx->previousStage = CMD_STAGE_RECEIVE_RESPONSE;
    return rval;
}

TSS2_RC Tss2_Sys_Execute(TSS2_SYS_CONTEXT *sysContext)
{
    TSS2_RC rval;

    if (!sysContext)
        return TSS2_SYS_RC_BAD_REFERENCE;

    rval = Tss2_Sys_ExecuteAsync(sysContext);
    if (rval)
        return rval;

    return Tss2_Sys_ExecuteFinish(sysContext, TSS2_TCTI_TIMEOUT_BLOCK);
}
