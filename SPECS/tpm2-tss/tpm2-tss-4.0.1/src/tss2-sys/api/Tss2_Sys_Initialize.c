/* SPDX-License-Identifier: BSD-2-Clause */
/***********************************************************************;
 * Copyright (c) 2015-2018, Intel Corporation
 *
 * Copyright 2015, Andreas Fuchs @ Fraunhofer SIT
 *
 * All rights reserved.
 ***********************************************************************/

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <inttypes.h>

#include "tss2_common.h"
#include "tss2_tpm2_types.h"
#include "tss2_mu.h"

#include "sysapi_util.h"
#define LOGMODULE sys
#include "util/log.h"

static const TSS2_ABI_VERSION CURRENT = TSS2_ABI_VERSION_CURRENT;
#define CURRENT_CREATOR (CURRENT.tssCreator)
#define CURRENT_FAMILY  (CURRENT.tssFamily)
#define CURRENT_LEVEL   (CURRENT.tssLevel)
#define CURRENT_VERSION (CURRENT.tssVersion)

TSS2_RC Tss2_Sys_Initialize(
    TSS2_SYS_CONTEXT *sysContext,
    size_t contextSize,
    TSS2_TCTI_CONTEXT *tctiContext,
    TSS2_ABI_VERSION *abiVersion)
{
    _TSS2_SYS_CONTEXT_BLOB *ctx = syscontext_cast(sysContext);

    if (!ctx || !tctiContext)
        return TSS2_SYS_RC_BAD_REFERENCE;

    if (contextSize < sizeof(_TSS2_SYS_CONTEXT_BLOB))
        return TSS2_SYS_RC_INSUFFICIENT_CONTEXT;

    if (!TSS2_TCTI_TRANSMIT (tctiContext) ||
        !TSS2_TCTI_RECEIVE (tctiContext))
        return TSS2_SYS_RC_BAD_TCTI_STRUCTURE;

    /* Checks for ABI negotiation. */
    if (abiVersion != NULL &&
        (abiVersion->tssCreator != CURRENT_CREATOR ||
         abiVersion->tssFamily != CURRENT_FAMILY ||
         abiVersion->tssLevel != CURRENT_LEVEL ||
         abiVersion->tssVersion != CURRENT_VERSION)) {
        LOG_ERROR("ABI-Version of application %" PRIx32 ".%" PRIu32 ".%"
                  PRIu32 ".%" PRIu32 " differs from ABI version of SAPI %"
                  PRIx32 ".%" PRIu32 ".%" PRIu32 ".%" PRIu32,
                  abiVersion->tssCreator, abiVersion->tssFamily,
                  abiVersion->tssLevel, abiVersion->tssVersion,
                  CURRENT_CREATOR, CURRENT_FAMILY,
                  CURRENT_LEVEL, CURRENT_VERSION);
        return TSS2_SYS_RC_ABI_MISMATCH;
    }

    ctx->tctiContext = tctiContext;
    InitSysContextPtrs(ctx, contextSize);
    InitSysContextFields(ctx);
    ctx->previousStage = CMD_STAGE_INITIALIZE;

    return TSS2_RC_SUCCESS;
}
