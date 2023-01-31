/* SPDX-License-Identifier: BSD-2-Clause */
/***********************************************************************
 * Copyright (c) 2018, Intel Corporation
 *
 * All rights reserved.
 ***********************************************************************/
#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <stdbool.h>
#include <stdlib.h>

#define LOGMODULE test
#include "tss2_sys.h"
#include "tss2_tcti.h"
#include "util/log.h"
#include "test.h"
#include "test-options.h"
#include "context-util.h"
#include "tss2-sys/sysapi_util.h"
#include "tcti/tcti-fuzzing.h"

int
LLVMFuzzerTestOneInput (
        const uint8_t *Data,
        size_t Size)
{
    int ret;
    TSS2_SYS_CONTEXT *sys_context;
    _TSS2_SYS_CONTEXT_BLOB *ctx = NULL;
    TSS2_TCTI_FUZZING_CONTEXT *tcti_fuzzing = NULL;

    /* Use the fuzzing tcti */
    test_opts_t opts = {
        .tcti_type      = FUZZING_TCTI,
        .device_file    = DEVICE_PATH_DEFAULT,
        .socket_address = HOSTNAME_DEFAULT,
        .socket_port    = PORT_DEFAULT,
    };

    get_test_opts_from_env (&opts);
    if (sanity_check_test_opts (&opts) != 0) {
        LOG_ERROR("Checking test options");
        exit(1); /* fatal error */
    }

    sys_context = sys_init_from_opts (&opts);
    if (sys_context == NULL) {
        LOG_ERROR("SYS context not initialized");
        exit(1); /* fatal error */
    }

    ctx = syscontext_cast (sys_context);
    tcti_fuzzing = tcti_fuzzing_context_cast (ctx->tctiContext);
    tcti_fuzzing->data = Data;
    tcti_fuzzing->size = Size;

    ret = test_invoke (sys_context);

    sys_teardown_full (sys_context);

    if (ret) {
        LOG_ERROR("Test failed");
        exit(1); /* fatal error */
    }

    return 0;  // Non-zero return values are reserved for future use.
}
