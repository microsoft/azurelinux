/* SPDX-License-Identifier: BSD-2-Clause */
/***********************************************************************
 * Copyright (c) 2017-2018, Intel Corporation
 *
 * All rights reserved.
 ***********************************************************************/
#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <inttypes.h>

#define LOGMODULE test
#include "util/log.h"
#include "sys-util.h"
#include "test.h"

int
test_invoke (TSS2_SYS_CONTEXT *sys_context)
{
    TSS2_RC rc;
    TPM2_HANDLE handle;

    rc = create_primary_rsa_2048_aes_128_cfb (sys_context, &handle);
    if (rc != TSS2_RC_SUCCESS) {
        LOG_ERROR("CreatePrimary failed with 0x%"PRIx32, rc);
        return 1;
    }

    rc = Tss2_Sys_FlushContext(sys_context, handle);
    if (rc != TSS2_RC_SUCCESS) {
        LOG_ERROR("Tss2_Sys_FlushContext failed with 0x%"PRIx32, rc);
        return 99; /* fatal error */
    }

    return 0;
}
