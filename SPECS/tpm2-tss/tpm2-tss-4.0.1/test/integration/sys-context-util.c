/* SPDX-License-Identifier: BSD-2-Clause */
/***********************************************************************
 * Copyright (c) 2017-2018, Intel Corporation
 *
 * All rights reserved.
 ***********************************************************************/
#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <errno.h>
#include <inttypes.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "tss2_tcti_device.h"
#include "tss2_tcti_mssim.h"
#include "tss2_tcti_swtpm.h"
#ifdef TCTI_FUZZING
#include "tss2_tcti_fuzzing.h"
#endif /* TCTI_FUZZING */

#include "context-util.h"
#include "tss2-tcti/tcti-mssim.h"
#include "tss2-tcti/tcti-swtpm.h"

#ifdef TCTI_DEVICE
/*
 * Initialize a TSS2_TCTI_CONTEXT for the device TCTI.
 */
TSS2_TCTI_CONTEXT *
tcti_device_init(char const *device_path)
{
    size_t size;
    TSS2_RC rc;
    TSS2_TCTI_CONTEXT *tcti_ctx;

    rc = Tss2_Tcti_Device_Init(NULL, &size, 0);
    if (rc != TSS2_RC_SUCCESS) {
        fprintf(stderr,
                "Failed to get allocation size for device tcti context: "
                "0x%x\n", rc);
        return NULL;
    }
    tcti_ctx = (TSS2_TCTI_CONTEXT *) calloc(1, size);
    if (tcti_ctx == NULL) {
        fprintf(stderr,
                "Allocation for device TCTI context failed: %s\n",
                strerror(errno));
        return NULL;
    }
    rc = Tss2_Tcti_Device_Init(tcti_ctx, &size, device_path);
    if (rc != TSS2_RC_SUCCESS) {
        fprintf(stderr, "Failed to initialize device TCTI context: 0x%x\n", rc);
        free(tcti_ctx);
        return NULL;
    }
    return tcti_ctx;
}
#endif /* TCTI_DEVICE */

#ifdef TCTI_MSSIM
/*
 * Initialize a socket TCTI instance using the provided options structure.
 * The hostname and port are the only configuration options used.
 * The caller is returned a TCTI context structure that is allocated by this
 * function. This structure must be freed by the caller.
 */
TSS2_TCTI_CONTEXT *
tcti_socket_init(char const *host, uint16_t port)
{
    size_t size;
    TSS2_RC rc;
    TSS2_TCTI_CONTEXT *tcti_ctx;
    char conf_str[TCTI_MSSIM_CONF_MAX] = { 0 };

    snprintf(conf_str, TCTI_MSSIM_CONF_MAX, "host=%s,port=%" PRIu16, host, port);
    rc = Tss2_Tcti_Mssim_Init(NULL, &size, conf_str);
    if (rc != TSS2_RC_SUCCESS) {
        fprintf(stderr, "Faled to get allocation size for tcti context: "
                "0x%x\n", rc);
        return NULL;
    }
    tcti_ctx = (TSS2_TCTI_CONTEXT *) calloc(1, size);
    if (tcti_ctx == NULL) {
        fprintf(stderr, "Allocation for tcti context failed: %s\n",
                strerror(errno));
        return NULL;
    }
    rc = Tss2_Tcti_Mssim_Init(tcti_ctx, &size, conf_str);
    if (rc != TSS2_RC_SUCCESS) {
        fprintf(stderr, "Failed to initialize tcti context: 0x%x\n", rc);
        free(tcti_ctx);
        return NULL;
    }
    return tcti_ctx;
}
#endif /* TCTI_MSSIM */

#ifdef TCTI_SWTPM
/*
 * Initialize a socket TCTI instance using the provided options structure.
 * The hostname and port are the only configuration options used.
 * The caller is returned a TCTI context structure that is allocated by this
 * function. This structure must be freed by the caller.
 */
TSS2_TCTI_CONTEXT *
tcti_swtpm_init(char const *host, uint16_t port)
{
    size_t size;
    TSS2_RC rc;
    TSS2_TCTI_CONTEXT *tcti_ctx;
    char conf_str[TCTI_SWTPM_CONF_MAX] = { 0 };

    snprintf(conf_str, TCTI_SWTPM_CONF_MAX, "host=%s,port=%" PRIu16, host, port);
    rc = Tss2_Tcti_Swtpm_Init(NULL, &size, conf_str);
    if (rc != TSS2_RC_SUCCESS) {
        fprintf(stderr, "Faled to get allocation size for tcti context: "
                "0x%x\n", rc);
        return NULL;
    }
    tcti_ctx = (TSS2_TCTI_CONTEXT *) calloc(1, size);
    if (tcti_ctx == NULL) {
        fprintf(stderr, "Allocation for tcti context failed: %s\n",
                strerror(errno));
        return NULL;
    }
    rc = Tss2_Tcti_Swtpm_Init(tcti_ctx, &size, conf_str);
    if (rc != TSS2_RC_SUCCESS) {
        fprintf(stderr, "Failed to initialize tcti context: 0x%x\n", rc);
        free(tcti_ctx);
        return NULL;
    }
    return tcti_ctx;
}
#endif /* TCTI_SWTPM */

#ifdef TCTI_FUZZING
/*
 * Initialize a fuzzing TCTI instance using the provided options structure.
 * The fuzzing_lengths.log file is the only configuration option used.
 * The caller is returned a TCTI context structure that is allocated by this
 * function. This structure must be freed by the caller.
 */
TSS2_TCTI_CONTEXT *
tcti_fuzzing_init()
{
    size_t size;
    TSS2_RC rc;
    TSS2_TCTI_CONTEXT *tcti_ctx;

    rc = Tss2_Tcti_Fuzzing_Init(NULL, &size, NULL);
    if (rc != TSS2_RC_SUCCESS) {
        fprintf(stderr, "Faled to get allocation size for tcti context: "
                "0x%x\n", rc);
        return NULL;
    }
    tcti_ctx = (TSS2_TCTI_CONTEXT *) calloc(1, size);
    if (tcti_ctx == NULL) {
        fprintf(stderr, "Allocation for tcti context failed: %s\n",
                strerror(errno));
        return NULL;
    }
    rc = Tss2_Tcti_Fuzzing_Init(tcti_ctx, &size, NULL);
    if (rc != TSS2_RC_SUCCESS) {
        fprintf(stderr, "Failed to initialize tcti context: 0x%x\n", rc);
        free(tcti_ctx);
        return NULL;
    }
    return tcti_ctx;
}
#endif /* TCTI_FUZZING */

/*
 * Initialize a SYS context using the TCTI context provided by the caller.
 * This function allocates memory for the SYS context and returns it to the
 * caller. This memory must be freed by the caller.
 */
TSS2_SYS_CONTEXT *
sys_init_from_tcti_ctx(TSS2_TCTI_CONTEXT * tcti_ctx)
{
    TSS2_SYS_CONTEXT *sys_ctx;
    TSS2_RC rc;
    size_t size;
    TSS2_ABI_VERSION abi_version = {
        .tssCreator = 1,
        .tssFamily = 2,
        .tssLevel = 1,
        .tssVersion = 108,
    };

    size = Tss2_Sys_GetContextSize(0);
    sys_ctx = (TSS2_SYS_CONTEXT *) calloc(1, size);
    if (sys_ctx == NULL) {
        fprintf(stderr,
                "Failed to allocate 0x%zx bytes for the SYS context\n", size);
        return NULL;
    }
    rc = Tss2_Sys_Initialize(sys_ctx, size, tcti_ctx, &abi_version);
    if (rc != TSS2_RC_SUCCESS) {
        fprintf(stderr, "Failed to initialize SYS context: 0x%x\n", rc);
        free(sys_ctx);
        return NULL;
    }
    return sys_ctx;
}

/*
 * Initialize a SYS context to use a socket TCTI. Get configuration data from
 * the provided structure.
 */
TSS2_SYS_CONTEXT *
sys_init_from_opts(test_opts_t * options)
{
    TSS2_TCTI_CONTEXT *tcti_ctx;
    TSS2_SYS_CONTEXT *sys_ctx;

    tcti_ctx = tcti_init_from_opts(options);
    if (tcti_ctx == NULL)
        return NULL;
    sys_ctx = sys_init_from_tcti_ctx(tcti_ctx);
    if (sys_ctx == NULL)
        return NULL;
    return sys_ctx;
}

/*
 * Initialize a TSS2_TCTI_CONTEXT using whatever TCTI data is in the options
 * structure. This is a mechanism that allows the calling application to be
 * mostly ignorant of which TCTI they're creating / initializing.
 */
TSS2_TCTI_CONTEXT *
tcti_init_from_opts(test_opts_t * options)
{
    switch (options->tcti_type) {
#ifdef TCTI_DEVICE
    case DEVICE_TCTI:
        return tcti_device_init(options->device_file);
#endif /* TCTI_DEVICE */
#ifdef TCTI_MSSIM
    case SOCKET_TCTI:
        return tcti_socket_init(options->socket_address, options->socket_port);
#endif /* TCTI_MSSIM */
#ifdef TCTI_SWTPM
    case SWTPM_TCTI:
       return tcti_swtpm_init(options->socket_address, options->socket_port);
#endif /* TCTI_SWTPM */
#ifdef TCTI_FUZZING
    case FUZZING_TCTI:
        return tcti_fuzzing_init();
#endif /* TCTI_FUZZING */
    default:
        return NULL;
    }
}

/*
 * Teardown / Finalize TCTI context and free memory.
 */
void
tcti_teardown(TSS2_TCTI_CONTEXT * tcti_context)
{
    if (tcti_context) {
        Tss2_Tcti_Finalize(tcti_context);
        free(tcti_context);
    }
}

/*
 * Teardown and free the resources associated with a SYS context structure.
 */
void
sys_teardown(TSS2_SYS_CONTEXT * sys_context)
{
    Tss2_Sys_Finalize(sys_context);
    free(sys_context);
}

/*
 * Teardown and free the resources associated with a SYS context structure.
 * This includes tearing down the TCTI as well.
 */
void
sys_teardown_full(TSS2_SYS_CONTEXT * sys_context)
{
    TSS2_TCTI_CONTEXT *tcti_context = NULL;
    TSS2_RC rc;

    rc = Tss2_Sys_GetTctiContext(sys_context, &tcti_context);
    if (rc != TSS2_RC_SUCCESS)
        return;

    sys_teardown(sys_context);
    tcti_teardown(tcti_context);
}
