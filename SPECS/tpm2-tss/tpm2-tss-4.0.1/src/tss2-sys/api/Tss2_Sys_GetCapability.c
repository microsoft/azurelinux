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

#include <string.h>

TSS2_RC Tss2_Sys_GetCapability_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPM2_CAP capability,
    UINT32 property,
    UINT32 propertyCount)
{
    _TSS2_SYS_CONTEXT_BLOB *ctx = syscontext_cast(sysContext);
    TSS2_RC rval;

    if (!ctx)
        return TSS2_SYS_RC_BAD_REFERENCE;

    rval = CommonPreparePrologue(ctx, TPM2_CC_GetCapability);
    if (rval)
        return rval;

    rval = Tss2_MU_UINT32_Marshal(capability, ctx->cmdBuffer,
                                  ctx->maxCmdSize,
                                  &ctx->nextData);
    if (rval)
        return rval;

    rval = Tss2_MU_UINT32_Marshal(property, ctx->cmdBuffer,
                                  ctx->maxCmdSize,
                                  &ctx->nextData);
    if (rval)
        return rval;

    rval = Tss2_MU_UINT32_Marshal(propertyCount, ctx->cmdBuffer,
                                  ctx->maxCmdSize,
                                  &ctx->nextData);
    if (rval)
        return rval;

    ctx->decryptAllowed = 0;
    ctx->encryptAllowed = 0;
    ctx->authAllowed = 1;

    return CommonPrepareEpilogue(ctx);
}

TSS2_RC Tss2_Sys_GetCapability_Complete(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_YES_NO *moreData,
    TPMS_CAPABILITY_DATA *capabilityData)
{
    _TSS2_SYS_CONTEXT_BLOB *ctx = syscontext_cast(sysContext);
    TSS2_RC rval;
    TPM2_CAP cap;

    if (!ctx)
        return TSS2_SYS_RC_BAD_REFERENCE;

    rval = CommonComplete(ctx);
    if (rval)
        return rval;

    rval = Tss2_MU_UINT8_Unmarshal(ctx->cmdBuffer,
                                   ctx->maxCmdSize,
                                   &ctx->nextData,
                                   moreData);
    if (rval)
        return rval;

    /* Peak at the capabilityData->capability field to decide what to do
       if this is a standard cap, just unmarshal it.
       if this is a vendor cap, we fill a tpm2b inside the struct buffer.*/
    size_t next_data_vendor = ctx->nextData;
    rval = Tss2_MU_UINT32_Unmarshal(ctx->cmdBuffer,
                                  ctx->maxCmdSize,
                                  &next_data_vendor,
                                  &cap);
    if (rval)
        return rval;

    if (cap != TPM2_CAP_VENDOR_PROPERTY)
        return Tss2_MU_TPMS_CAPABILITY_DATA_Unmarshal(ctx->cmdBuffer,
                                                      ctx->maxCmdSize,
                                                      &ctx->nextData,
                                                      capabilityData);

    /*
     * Size the capabilityData is the end of response we can copy the remainder
     * of the response in case of cap_vendor.
     *
     * Example for 23 byte response size:
     *
     * Header: 10 Bytes
     * MoreData: 1 byte
     * cap: 4 bytes
     * Vendor Data: 8 bytes
     */
    ctx->nextData = next_data_vendor;
    size_t left = ctx->rsp_header.responseSize - ctx->nextData;
    if (left > sizeof(capabilityData->data.vendor))
        return TSS2_MU_RC_BAD_SIZE;

    /* seems callers can use NULL */
    if (capabilityData) {
        capabilityData->capability = cap;

        capabilityData->data.vendor.size = left;
        memcpy(&capabilityData->data.vendor.buffer[0],
               &ctx->cmdBuffer[ctx->nextData],
               left);
    }
    ctx->nextData += left;

    return TSS2_RC_SUCCESS;
}

TSS2_RC Tss2_Sys_GetCapability(
    TSS2_SYS_CONTEXT *sysContext,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    TPM2_CAP capability,
    UINT32 property,
    UINT32 propertyCount,
    TPMI_YES_NO *moreData,
    TPMS_CAPABILITY_DATA *capabilityData,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray)
{
    _TSS2_SYS_CONTEXT_BLOB *ctx = syscontext_cast(sysContext);
    TSS2_RC rval;

    rval = Tss2_Sys_GetCapability_Prepare(sysContext, capability, property,
                                          propertyCount);
    if (rval)
        return rval;

    rval = CommonOneCall(ctx, cmdAuthsArray, rspAuthsArray);
    if (rval)
        return rval;

    return Tss2_Sys_GetCapability_Complete(sysContext, moreData, capabilityData);
}
