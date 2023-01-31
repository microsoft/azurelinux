/* SPDX-License-Identifier: BSD-2-Clause */
/***********************************************************************
 * Copyright (c) 2017-2018, Intel Corporation
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
#include "util/log.h"
#include "test.h"
#include "test-options.h"
#include "context-util.h"

/**
 * This program is a template for integration tests (ones that use the TCTI
 * and the SYS contexts / API directly). It does nothing more than parsing
 * command line options that allow the caller (likely a script) to specify
 * which TCTI to use for the test.
 */
int
main (int   argc,
      char *argv[])
{
    TSS2_SYS_CONTEXT *sys_context;
    int ret;
    test_opts_t opts = {
        .tcti_type      = TCTI_DEFAULT,
        .device_file    = DEVICE_PATH_DEFAULT,
        .socket_address = HOSTNAME_DEFAULT,
        .socket_port    = PORT_DEFAULT,
    };

    UNUSED(argc);
    UNUSED(argv);

    get_test_opts_from_env (&opts);
    if (sanity_check_test_opts (&opts) != 0) {
        LOG_ERROR("Checking test options");
        return 99; /* fatal error */
    }
    sys_context = sys_init_from_opts (&opts);
    if (sys_context == NULL) {
        LOG_ERROR("SYS context not initialized");
        return 99; /* fatal error */
    }

    ret = Tss2_Sys_Startup(sys_context, TPM2_SU_CLEAR);
    if (ret != TSS2_RC_SUCCESS && ret != TPM2_RC_INITIALIZE) {
        LOG_ERROR("TPM Startup FAILED! Response Code : 0x%x", ret);
        exit(1);
    }

    ret = test_invoke (sys_context);

    sys_teardown_full (sys_context);

    return ret;
}
