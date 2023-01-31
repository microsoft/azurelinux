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

TSS2_RC Tss2_Sys_GetTctiContext(
    TSS2_SYS_CONTEXT *sysContext,
    TSS2_TCTI_CONTEXT **tctiContext)
{
    _TSS2_SYS_CONTEXT_BLOB *ctx = syscontext_cast(sysContext);

    if (!ctx || !tctiContext)
        return TSS2_SYS_RC_BAD_REFERENCE;

    *tctiContext = ctx->tctiContext;

    return TSS2_RC_SUCCESS;
}
