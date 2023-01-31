/* SPDX-License-Identifier: BSD-2-Clause */
/***********************************************************************
 * Copyright (c) 2017-2018, Intel Corporation
 *
 * All rights reserved.
 ***********************************************************************/

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include "inttypes.h"
#define LOGMODULE test
#include "util/log.h"
#include "sys-util.h"
#include "test.h"

int
test_invoke (TSS2_SYS_CONTEXT *sys_context)
{
    TSS2_RC      rc             = TPM2_RC_SUCCESS;
    TPM2_HANDLE  primary_handle = 0;
    /* session parameters */
    /* command session info */
    TSS2L_SYS_AUTH_COMMAND  sessions_cmd         = {
        .auths = {{ .sessionHandle = TPM2_RH_PW }},
        .count = 1
    };
    /* response session info */
    TSS2L_SYS_AUTH_RESPONSE  sessions_rsp         = {
        .auths = { 0 },
        .count = 0
    };

    rc = create_primary_rsa_2048_aes_128_cfb (sys_context, &primary_handle);
    if (rc != TSS2_RC_SUCCESS) {
        LOG_INFO("failed to create primary: 0x%" PRIx32, rc);
        return 99; /* fatal error */
    }

    rc = Tss2_Sys_EvictControl (sys_context,
                                TPM2_RH_OWNER,
                                primary_handle,
                                &sessions_cmd,
                                0x81000000,
                                &sessions_rsp);
    if (rc != TSS2_RC_SUCCESS) {
        LOG_INFO("failed to make key 0x%" PRIx32 " persistent: 0x%" PRIx32,
                   primary_handle, rc);
        return 1;
    }

    rc = Tss2_Sys_EvictControl (sys_context,
                                TPM2_RH_OWNER,
                                0x81000000,
                                &sessions_cmd,
                                0x81000000,
                                &sessions_rsp);
    if (rc != TSS2_RC_SUCCESS) {
        LOG_INFO("failed to make key 0x%" PRIx32 " nonpersistent: 0x%" PRIx32,
                   primary_handle, rc);
        return 1;
    }

    rc = Tss2_Sys_FlushContext(sys_context, primary_handle);
    if (rc != TSS2_RC_SUCCESS) {
        LOG_ERROR("Tss2_Sys_FlushContext failed with 0x%"PRIx32, rc);
        return 99; /* fatal error */
    }

    return 0;
}
