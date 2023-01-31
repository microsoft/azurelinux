/* SPDX-License-Identifier: BSD-2-Clause */
/***********************************************************************
 * Copyright (c) 2017-2018, Intel Corporation
 *
 * All rights reserved.
 ***********************************************************************/
#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <stdio.h>
#include <stdlib.h>

#include "tss2_sys.h"

#define LOGMODULE test
#include "util/log.h"
#include "test.h"
/**
 */
int
test_invoke (TSS2_SYS_CONTEXT *sys_context)
{
    TSS2_RC rc;

    /* NOTE: this should never be done in real applications.
     * It is only done here for test purposes.
     */
    TSS2_TCTI_CONTEXT_COMMON_V2 tctiContext;

    LOG_INFO("Sys_Initialize tests started.");

    rc = Tss2_Sys_Initialize( (TSS2_SYS_CONTEXT *)0, 10, (TSS2_TCTI_CONTEXT *)1, (TSS2_ABI_VERSION *)1 );
    if( rc != TSS2_SYS_RC_BAD_REFERENCE  ) {
        LOG_ERROR("Sys_Initialize context NULL test FAILED! Response Code : %x", rc);
        exit(1);
    }

    rc = Tss2_Sys_Initialize( (TSS2_SYS_CONTEXT *)1, 10, (TSS2_TCTI_CONTEXT *)0, (TSS2_ABI_VERSION *)1 );
    if( rc != TSS2_SYS_RC_BAD_REFERENCE  ) {
        LOG_ERROR("Sys_Initialize tcti  NULL test FAILED! Response Code : %x", rc);
        exit(1);
    }

    rc = Tss2_Sys_Initialize( (TSS2_SYS_CONTEXT *)1, 10, (TSS2_TCTI_CONTEXT *)1, (TSS2_ABI_VERSION *)1 );
    if( rc != TSS2_SYS_RC_INSUFFICIENT_CONTEXT ) {
        LOG_ERROR("Sys_Initialize insufficient context FAILED! Response Code : %x", rc);
        exit(1);
    }

    /* NOTE: don't do this in real applications. */
    TSS2_TCTI_RECEIVE (&tctiContext) = (TSS2_TCTI_RECEIVE_FCN)1;
    TSS2_TCTI_TRANSMIT (&tctiContext) = (TSS2_TCTI_TRANSMIT_FCN)0;

    rc = Tss2_Sys_Initialize( (TSS2_SYS_CONTEXT *)1, Tss2_Sys_GetContextSize (0), (TSS2_TCTI_CONTEXT *)&tctiContext, (TSS2_ABI_VERSION *)1 );
    if( rc != TSS2_SYS_RC_BAD_TCTI_STRUCTURE ) {
        LOG_ERROR("Sys_Initialize FAILED! Response Code : %x", rc);
        exit(1);
    }

    /* NOTE: don't do this in real applications. */
    TSS2_TCTI_RECEIVE (&tctiContext) = (TSS2_TCTI_RECEIVE_FCN)0;
    TSS2_TCTI_TRANSMIT (&tctiContext) = (TSS2_TCTI_TRANSMIT_FCN)1;

    rc = Tss2_Sys_Initialize( (TSS2_SYS_CONTEXT *)1, Tss2_Sys_GetContextSize (0), (TSS2_TCTI_CONTEXT *)&tctiContext, (TSS2_ABI_VERSION *)1 );
    if( rc != TSS2_SYS_RC_BAD_TCTI_STRUCTURE ) {
        LOG_ERROR("Sys_Initialize FAILED! Response Code : %x", rc);
        exit(1);
    }

    LOG_INFO("Sys_Initialize Test Passed!");
    return 0;
}
