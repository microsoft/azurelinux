/* SPDX-License-Identifier: BSD-2-Clause */
/*
 * Copyright (c) 2018 Intel Corporation
 * All rights reserved.
 */
 /* Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved. */

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <inttypes.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <windows.h>
#include <Tbs.h>

#include "tss2_tcti.h"
#include "tss2_tcti_tbs.h"

#include "tcti-common.h"
#include "tcti-tbs.h"

#define LOGMODULE tcti
#include "util/log.h"

/*
 * This function wraps the "up-cast" of the opaque TCTI context type to the
 * type for the mssim TCTI context. If passed a NULL context the function
 * returns a NULL ptr. The function doesn't check magic number anymore
 * It should checked by the appropriate tcti_common_checks.
 */
TSS2_TCTI_TBS_CONTEXT*
tcti_tbs_context_cast (TSS2_TCTI_CONTEXT *tcti_ctx)
{
    if (tcti_ctx == NULL) {
        return NULL;
    }

    return (TSS2_TCTI_TBS_CONTEXT*)tcti_ctx;
}

/*
 * This function down-casts the TBS TCTI context to the common context
 * defined in the tcti-common module.
 */
TSS2_TCTI_COMMON_CONTEXT*
tcti_tbs_down_cast (TSS2_TCTI_TBS_CONTEXT *tcti_tbs)
{
    if (tcti_tbs == NULL) {
        return NULL;
    }
    return &tcti_tbs->common;
}

TSS2_RC
tcti_tbs_transmit (
    TSS2_TCTI_CONTEXT *tctiContext,
    size_t command_size,
    const uint8_t *command_buffer)
{
    TSS2_TCTI_TBS_CONTEXT *tcti_tbs = tcti_tbs_context_cast (tctiContext);
    TSS2_TCTI_COMMON_CONTEXT *tcti_common = tcti_tbs_down_cast (tcti_tbs);
    TSS2_RC rc = TSS2_RC_SUCCESS;

    rc = tcti_common_transmit_checks(tcti_common, command_buffer, TCTI_TBS_MAGIC);
    if (rc != TSS2_RC_SUCCESS) {
        return rc;
    }

    LOGBLOB_DEBUG (command_buffer,
                   command_size,
                   "sending %zu byte command buffer:",
                   command_size);

    memcpy (tcti_tbs->commandBuffer, command_buffer, command_size);
    tcti_tbs->commandSize = command_size;

    tcti_common->state = TCTI_STATE_RECEIVE;
    return TSS2_RC_SUCCESS;
}

/*
 * This receive function deviates from the spec a bit. Calling this function
 * with a NULL 'response_buffer' parameter *should* result in the required size
 * for the response buffer being returned to the caller. The required size for
 * the response buffer is normally stored in the pcbResult parameter of
 * the 'TBSip_Submit_Command' function by TBS. To avoid having to maintain
 * a response buffer, we are passing the 'response_buffer' parameter directly to
 * 'Tbsip_Submit_Command'; this means that in the case when 'response_buffer'
 * is NULL, we would not be able to retreive the size without losing the response.
 *
 * Instead, if the caller queries the size, we return 4k just to be on the
 * safe side. We do *not* however verify that the provided buffer is large
 * enough to hold the full response (we can't). If the caller provides us with
 * a buffer less than 4k we'll read as much of the response as we can given
 * the size of the buffer. If the response size is larger than the provided
 * buffer we print a warning. This allows "expert applications" to
 * precalculate the required response buffer size for whatever commands they
 * may send.
 */
TSS2_RC
tcti_tbs_receive (
    TSS2_TCTI_CONTEXT *tctiContext,
    size_t *response_size,
    uint8_t *response_buffer,
    int32_t timeout)
{
    TSS2_TCTI_TBS_CONTEXT *tcti_tbs = tcti_tbs_context_cast (tctiContext);
    TSS2_TCTI_COMMON_CONTEXT *tcti_common = tcti_tbs_down_cast (tcti_tbs);
    TSS2_RC rc = TSS2_RC_SUCCESS;
    TBS_RESULT tbs_rc;
    int original_size;

    rc = tcti_common_receive_checks(tcti_common, response_size, TCTI_TBS_MAGIC);
    if (rc != TSS2_RC_SUCCESS) {
        return rc;
    }
    if (timeout != TSS2_TCTI_TIMEOUT_BLOCK) {
        LOG_WARNING ("The underlying IPC mechanism does not support "
                     "asynchronous I/O. The 'timeout' parameter must be "
                     "TSS2_TCTI_TIMEOUT_BLOCK");
        return TSS2_TCTI_RC_BAD_VALUE;
    }
    if (response_buffer == NULL) {
        LOG_DEBUG("Caller queried for size but our TCTI TBS implementation doesn't "
                  "support this, Returning %d which is the max size for "
                  "a response buffer.",
                   TPM2_MAX_RESPONSE_SIZE);
        *response_size = TPM2_MAX_RESPONSE_SIZE;
        return TSS2_RC_SUCCESS;
    }
    if (*response_size < TPM2_MAX_RESPONSE_SIZE) {
        LOG_INFO("Caller provided buffer that *may* not be large enough to "
            "hold the response buffer.");
    }

    original_size = *response_size;

    tbs_rc = Tbsip_Submit_Command (tcti_tbs->hContext,
                                   TBS_COMMAND_LOCALITY_ZERO,
                                   TBS_COMMAND_PRIORITY_NORMAL,
                                   tcti_tbs->commandBuffer,
                                   tcti_tbs->commandSize,
                                   response_buffer,
                                   (PUINT32) response_size);
    if (tbs_rc != TBS_SUCCESS) {
        LOG_ERROR ("Failed to submit command to TBS with error: 0x%x", tbs_rc);
        rc = TSS2_TCTI_RC_IO_ERROR;
        goto out;
    }

    LOGBLOB_DEBUG (response_buffer, *response_size, "Response Received");

    if (original_size < *response_size) {
        LOG_WARNING("TPM2 response size is larger than the provided "
            "buffer: future use of this TCTI will likely fail.");
        rc = TSS2_TCTI_RC_INSUFFICIENT_BUFFER;
        goto out;
    }

    rc = header_unmarshal (response_buffer, &tcti_common->header);
    if (rc != TSS2_RC_SUCCESS) {
        goto out;
    }

    /*
     * Executing code beyond this point transitions the state machine to
     * TRANSMIT. Another call to this function will not be possible until
     * another command is sent to the TPM.
     */
out:
    tcti_common->state = TCTI_STATE_TRANSMIT;
    return rc;
}

void
tcti_tbs_finalize (
    TSS2_TCTI_CONTEXT *tctiContext)
{
    TSS2_TCTI_TBS_CONTEXT *tcti_tbs = tcti_tbs_context_cast (tctiContext);
    TSS2_TCTI_COMMON_CONTEXT *tcti_common = tcti_tbs_down_cast (tcti_tbs);
    TBS_RESULT tbs_rc;

    if (tcti_tbs == NULL) {
        return;
    }

    if (tcti_tbs->commandBuffer!= NULL) {
        free (tcti_tbs->commandBuffer);
        tcti_tbs->commandBuffer = NULL;
    }

    tbs_rc = Tbsip_Context_Close (tcti_tbs->hContext);
    if (tbs_rc != TBS_SUCCESS) {
        LOG_WARNING ("Failed to close context with TBS error: 0x%x", tbs_rc);
    }

    tcti_common->state = TCTI_STATE_FINAL;
}

TSS2_RC
tcti_tbs_cancel (
    TSS2_TCTI_CONTEXT *tctiContext)
{
    TBS_RESULT tbs_rc;
    TSS2_RC rc = TSS2_RC_SUCCESS;
    TSS2_TCTI_TBS_CONTEXT *tcti_tbs = tcti_tbs_context_cast (tctiContext);

    if (tcti_tbs == NULL) {
        return TSS2_TCTI_RC_BAD_REFERENCE;
    }
    tbs_rc = Tbsip_Cancel_Commands (tcti_tbs->hContext);
    if (tbs_rc != TBS_SUCCESS) {
        LOG_WARNING ("Failed to cancel commands with TBS error: 0x%x", tbs_rc);
        rc = TSS2_TCTI_RC_GENERAL_FAILURE;
    }

    return rc;
}

TSS2_RC
tcti_tbs_get_poll_handles (
    TSS2_TCTI_CONTEXT *tctiContext,
    TSS2_TCTI_POLL_HANDLE *handles,
    size_t *num_handles)
{
    /* TBS doesn't support polling. */
    UNUSED(tctiContext);
    UNUSED(handles);
    UNUSED(num_handles);
    return TSS2_TCTI_RC_NOT_IMPLEMENTED;
}

TSS2_RC
tcti_tbs_set_locality (
    TSS2_TCTI_CONTEXT *tctiContext,
    uint8_t locality)
{
    /*
     * TBS currently only supports locality 0
     */
    UNUSED(tctiContext);
    UNUSED(locality);
    return TSS2_TCTI_RC_NOT_IMPLEMENTED;
}

TSS2_RC
Tss2_Tcti_Tbs_Init (
    TSS2_TCTI_CONTEXT *tctiContext,
    size_t *size,
    const char *conf)
{
    TSS2_TCTI_TBS_CONTEXT *tcti_tbs;
    TSS2_TCTI_COMMON_CONTEXT *tcti_common;
    TBS_RESULT tbs_rc;
    TBS_CONTEXT_PARAMS2 params;
    TPM_DEVICE_INFO info;

    if (tctiContext == NULL) {
        if (size == NULL) {
            return TSS2_TCTI_RC_BAD_VALUE;
        }
        *size = sizeof (TSS2_TCTI_TBS_CONTEXT);
        return TSS2_RC_SUCCESS;
    }

    /* Init TCTI context */
    TSS2_TCTI_MAGIC (tctiContext) = TCTI_TBS_MAGIC;
    TSS2_TCTI_VERSION (tctiContext) = TCTI_VERSION;
    TSS2_TCTI_TRANSMIT (tctiContext) = tcti_tbs_transmit;
    TSS2_TCTI_RECEIVE (tctiContext) = tcti_tbs_receive;
    TSS2_TCTI_FINALIZE (tctiContext) = tcti_tbs_finalize;
    TSS2_TCTI_CANCEL (tctiContext) = tcti_tbs_cancel;
    TSS2_TCTI_GET_POLL_HANDLES (tctiContext) = tcti_tbs_get_poll_handles;
    TSS2_TCTI_SET_LOCALITY (tctiContext) = tcti_tbs_set_locality;
    TSS2_TCTI_MAKE_STICKY (tctiContext) = tcti_make_sticky_not_implemented;
    tcti_tbs = tcti_tbs_context_cast (tctiContext);
    tcti_common = tcti_tbs_down_cast (tcti_tbs);
    tcti_common->state = TCTI_STATE_TRANSMIT;

    memset (&tcti_common->header, 0, sizeof (tcti_common->header));
    tcti_common->locality = 0;

    params.includeTpm20 = 1;
    params.includeTpm12 = 0;
    params.version = TBS_CONTEXT_VERSION_TWO;
    tbs_rc = Tbsi_Context_Create ((PCTBS_CONTEXT_PARAMS)&params, &(tcti_tbs->hContext));
    if (tbs_rc != TBS_SUCCESS) {
        LOG_WARNING ("Failed to create context with TBS error: 0x%x", tbs_rc);
        return TSS2_TCTI_RC_IO_ERROR;
    }

    tbs_rc = Tbsi_GetDeviceInfo (sizeof (info), &info);
    if (tbs_rc != TBS_SUCCESS) {
        LOG_WARNING ("Failed to get device information with TBS error: 0x%x", tbs_rc);
        Tbsip_Context_Close (tcti_tbs->hContext);
        return TSS2_TCTI_RC_IO_ERROR;
    }
    if (info.tpmVersion != TPM_VERSION_20) {
        LOG_WARNING ("Failed to create context, TPM version is incorrect");
        Tbsip_Context_Close (tcti_tbs->hContext);
        return TSS2_TCTI_RC_IO_ERROR;
    }

    tcti_tbs->commandBuffer = malloc (sizeof (BYTE) * TPM2_MAX_COMMAND_SIZE);
    if (tcti_tbs->commandBuffer == NULL) {
        LOG_WARNING ("Failed to allocate memory for the result buffer when creating context");
        Tbsip_Context_Close (tcti_tbs->hContext);
        return TSS2_TCTI_RC_IO_ERROR;
    }

    return TSS2_RC_SUCCESS;
}

const TSS2_TCTI_INFO tss2_tcti_info = {
    .version = TCTI_VERSION,
    .name = "tcti-tbs",
    .description = "TCTI module for communication with Windows TPM Base Services",
    .config_help = "Configuration is not used",
    .init = Tss2_Tcti_Tbs_Init,
};

const TSS2_TCTI_INFO*
Tss2_Tcti_Info (void)
{
    return &tss2_tcti_info;
}
