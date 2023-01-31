/* SPDX-License-Identifier: BSD-2-Clause */
/*
 * Copyright (c) 2020 Infineon Technologies AG
 * All rights reserved.
 */

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <stdint.h>
#include <string.h>
#include <inttypes.h>

#include "tss2_tpm2_types.h"
#include "tss2_common.h"
#include "tss2_tcti.h"
#include "tcti-common.h"
#define LOGMODULE tcti
#include "util/log.h"

#include "tcti-pcap.h"
#include "tcti-pcap-builder.h"
#include "tss2_tctildr.h"

/*
 * This function wraps the "up-cast" of the opaque TCTI context type to the
 * type for the pcap TCTI context. The only safeguard we have to ensure this
 * operation is possible is the magic number in the pcap TCTI context.
 * If passed a NULL context, or the magic number check fails, this function
 * will return NULL.
 */
TSS2_TCTI_PCAP_CONTEXT*
tcti_pcap_context_cast (TSS2_TCTI_CONTEXT *tcti_ctx)
{
    if (tcti_ctx != NULL && TSS2_TCTI_MAGIC (tcti_ctx) == TCTI_PCAP_MAGIC) {
        return (TSS2_TCTI_PCAP_CONTEXT*)tcti_ctx;
    }
    return NULL;
}

/*
 * This function down-casts the pcap TCTI context to the common context
 * defined in the tcti-common module.
 */
TSS2_TCTI_COMMON_CONTEXT*
tcti_pcap_down_cast (TSS2_TCTI_PCAP_CONTEXT *tcti_pcap)
{
    if (tcti_pcap == NULL) {
        return NULL;
    }
    return &tcti_pcap->common;
}

TSS2_RC
tcti_pcap_transmit (
    TSS2_TCTI_CONTEXT *tcti_ctx,
    size_t size,
    const uint8_t *cmd_buf)
{
    TSS2_TCTI_PCAP_CONTEXT *tcti_pcap = tcti_pcap_context_cast (tcti_ctx);
    TSS2_TCTI_COMMON_CONTEXT *tcti_common = tcti_pcap_down_cast (tcti_pcap);
    TSS2_RC rc;
    int ret;

    if (tcti_pcap == NULL) {
        return TSS2_TCTI_RC_BAD_CONTEXT;
    }
    rc = tcti_common_transmit_checks (tcti_common, cmd_buf, TCTI_PCAP_MAGIC);
    if (rc != TSS2_RC_SUCCESS) {
        return rc;
    }

    LOGBLOB_DEBUG (cmd_buf, size, "sending %zu byte command buffer:", size);

    /* handle errors of underlying TCTI later (always writes to PCAP file) */
    ret = pcap_print (&tcti_pcap->pcap_builder,
                      cmd_buf, size,
                      PCAP_DIR_HOST_TO_TPM);
    if (ret != 0) {
        LOG_WARNING ("Failed to save transmission to PCAP file.");
    }

    rc = Tss2_Tcti_Transmit (tcti_pcap->tcti_child, size, cmd_buf);
    if (rc != TSS2_RC_SUCCESS) {
        LOG_ERROR ("Failed calling TCTI transmit of child TCTI module");
        return rc;
    }

    tcti_common->state = TCTI_STATE_RECEIVE;
    return TSS2_RC_SUCCESS;
}

TSS2_RC
tcti_pcap_receive (
    TSS2_TCTI_CONTEXT *tctiContext,
    size_t *response_size,
    unsigned char *response_buffer,
    int32_t timeout)
{
    TSS2_TCTI_PCAP_CONTEXT *tcti_pcap = tcti_pcap_context_cast (tctiContext);
    TSS2_TCTI_COMMON_CONTEXT *tcti_common = tcti_pcap_down_cast (tcti_pcap);
    TSS2_RC rc;
    int ret;

    if (tcti_pcap == NULL) {
        return TSS2_TCTI_RC_BAD_CONTEXT;
    }
    rc = tcti_common_receive_checks (tcti_common, response_size, TCTI_PCAP_MAGIC);
    if (rc != TSS2_RC_SUCCESS) {
        return rc;
    }

    rc = Tss2_Tcti_Receive (tcti_pcap->tcti_child,
                            response_size, response_buffer,
                            timeout);
    /* handle errors of underlying TCTI directly (may not write to PCAP file) */
    if (rc != TPM2_RC_SUCCESS) {
        return rc;
    }

     /* partial read */
    if (response_buffer == NULL) {
        return rc;
    }

    LOGBLOB_DEBUG (response_buffer, *response_size, "Response Received");

    ret = pcap_print (&tcti_pcap->pcap_builder,
                      response_buffer, *response_size,
                      PCAP_DIR_TPM_TO_HOST);
    if (ret != 0) {
        LOG_WARNING ("Failed to save transmission to PCAP file.");
    }

    tcti_common->state = TCTI_STATE_TRANSMIT;
    return rc;
}

TSS2_RC
tcti_pcap_cancel (
    TSS2_TCTI_CONTEXT *tctiContext)
{
    TSS2_TCTI_PCAP_CONTEXT *tcti_pcap = tcti_pcap_context_cast (tctiContext);
    TSS2_TCTI_COMMON_CONTEXT *tcti_common = tcti_pcap_down_cast (tcti_pcap);
    TSS2_RC rc;

    if (tcti_pcap == NULL) {
        return TSS2_TCTI_RC_BAD_CONTEXT;
    }
    rc = tcti_common_cancel_checks (tcti_common, TCTI_PCAP_MAGIC);
    if (rc != TSS2_RC_SUCCESS) {
        return rc;
    }

    LOG_WARNING ("Logging Tcti_Cancel to a PCAP file is not implemented");

    rc = Tss2_Tcti_Cancel (tcti_pcap->tcti_child);
    if (rc != TSS2_RC_SUCCESS) {
        return rc;
    }

    tcti_common->state = TCTI_STATE_TRANSMIT;
    return rc;
}

TSS2_RC
tcti_pcap_set_locality (
    TSS2_TCTI_CONTEXT *tctiContext,
    uint8_t locality)
{
    TSS2_TCTI_PCAP_CONTEXT *tcti_pcap = tcti_pcap_context_cast (tctiContext);
    TSS2_TCTI_COMMON_CONTEXT *tcti_common = tcti_pcap_down_cast (tcti_pcap);
    TSS2_RC rc;

    if (tcti_pcap == NULL) {
        return TSS2_TCTI_RC_BAD_CONTEXT;
    }

    rc = tcti_common_set_locality_checks (tcti_common, TCTI_PCAP_MAGIC);
    if (rc != TSS2_RC_SUCCESS) {
        return rc;
    }

    LOG_WARNING ("Logging Tcti_SetLocality to a PCAP file is not implemented");

    rc = Tss2_Tcti_SetLocality (tcti_pcap->tcti_child, locality);
    if (rc != TSS2_RC_SUCCESS) {
        return rc;
    }

    tcti_common->locality = locality;
    return rc;
}

TSS2_RC
tcti_pcap_get_poll_handles (
    TSS2_TCTI_CONTEXT *tctiContext,
    TSS2_TCTI_POLL_HANDLE *handles,
    size_t *num_handles)
{
    TSS2_TCTI_PCAP_CONTEXT *tcti_pcap = tcti_pcap_context_cast (tctiContext);

    if (tcti_pcap == NULL) {
        return TSS2_TCTI_RC_BAD_CONTEXT;
    }

    return Tss2_Tcti_GetPollHandles (tcti_pcap->tcti_child, handles,
                                     num_handles);
}

void
tcti_pcap_finalize (
    TSS2_TCTI_CONTEXT *tctiContext)
{
    TSS2_TCTI_PCAP_CONTEXT *tcti_pcap = tcti_pcap_context_cast (tctiContext);
    TSS2_TCTI_COMMON_CONTEXT *tcti_common = tcti_pcap_down_cast (tcti_pcap);

    if (tcti_pcap == NULL) {
        return;
    }

    Tss2_TctiLdr_Finalize (&tcti_pcap->tcti_child);
    pcap_deinit (&tcti_pcap->pcap_builder);

    tcti_common->state = TCTI_STATE_FINAL;
}

/*
 * This is an implementation of the standard TCTI initialization function for
 * this module.
 */
TSS2_RC
Tss2_Tcti_Pcap_Init (
    TSS2_TCTI_CONTEXT *tctiContext,
    size_t *size,
    const char *conf)
{
    TSS2_TCTI_PCAP_CONTEXT *tcti_pcap = (TSS2_TCTI_PCAP_CONTEXT*) tctiContext;
    TSS2_TCTI_COMMON_CONTEXT *tcti_common = tcti_pcap_down_cast (tcti_pcap);
    TSS2_RC rc = TSS2_RC_SUCCESS;
    int ret;

    if (tctiContext == NULL && size == NULL) {
        return TSS2_TCTI_RC_BAD_VALUE;
    } else if (tctiContext == NULL) {
        *size = sizeof (TSS2_TCTI_PCAP_CONTEXT);
        return TSS2_RC_SUCCESS;
    }

    if (conf == NULL) {
        LOG_TRACE ("tctiContext: 0x%" PRIxPTR ", size: 0x%" PRIxPTR ""
                   " no configuration will be used.",
                   (uintptr_t)tctiContext, (uintptr_t)size);
    } else {
        LOG_TRACE ("tctiContext: 0x%" PRIxPTR ", size: 0x%" PRIxPTR ", conf: %s",
                   (uintptr_t)tctiContext, (uintptr_t)size, conf);
    }

    rc = Tss2_TctiLdr_Initialize (conf, &tcti_pcap->tcti_child);
    if (rc != TSS2_RC_SUCCESS) {
        LOG_ERROR ("Error loading TCTI: %s", conf);
        return rc;
    }

    TSS2_TCTI_MAGIC (tcti_common) = TCTI_PCAP_MAGIC;
    TSS2_TCTI_VERSION (tcti_common) = TCTI_VERSION;
    TSS2_TCTI_TRANSMIT (tcti_common) = tcti_pcap_transmit;
    TSS2_TCTI_RECEIVE (tcti_common) = tcti_pcap_receive;
    TSS2_TCTI_FINALIZE (tcti_common) = tcti_pcap_finalize;
    TSS2_TCTI_CANCEL (tcti_common) = tcti_pcap_cancel;
    TSS2_TCTI_GET_POLL_HANDLES (tcti_common) = tcti_pcap_get_poll_handles;
    TSS2_TCTI_SET_LOCALITY (tcti_common) = tcti_pcap_set_locality;
    TSS2_TCTI_MAKE_STICKY (tcti_common) = tcti_make_sticky_not_implemented;
    tcti_common->state = TCTI_STATE_TRANSMIT;
    tcti_common->locality = 3;
    memset (&tcti_common->header, 0, sizeof (tcti_common->header));

    ret = pcap_init (&tcti_pcap->pcap_builder);
    if (ret != 0) {
        LOG_ERROR ("Failed to initialize PCAP TCTI");
        Tss2_TctiLdr_Finalize (&tcti_pcap->tcti_child);
        return TSS2_TCTI_RC_IO_ERROR;
    }

    return TSS2_RC_SUCCESS;
}

/* public info structure */
const TSS2_TCTI_INFO tss2_tcti_info = {
    .version = TCTI_VERSION,
    .name = "tcti-pcap",
    .description = "TCTI module for logging TPM commands in pcapng format.",
    .config_help = "The child tcti module and its config string: <name>:<conf>",
    .init = Tss2_Tcti_Pcap_Init,
};

const TSS2_TCTI_INFO*
Tss2_Tcti_Info (void)
{
    return &tss2_tcti_info;
}
