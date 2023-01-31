/* SPDX-License-Identifier: BSD-2-Clause */
/*******************************************************************************
 * Copyright 2019, Fraunhofer SIT, Infineon Technologies AG, Intel Corporation
 * All rights reserved.
 ******************************************************************************/

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <inttypes.h>
#include <limits.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#ifndef _WIN32
#include <sys/time.h>
#include <unistd.h>
#endif

#include "tss2_mu.h"
#include "tss2_tcti_swtpm.h"

#include "tcti-swtpm.h"
#include "tcti-common.h"
#include "util/key-value-parse.h"
#include "util/tss2_endian.h"
#define LOGMODULE tcti
#include "util/log.h"

/*
 * swtpm control channel command codes
 * see the <swtpm/tpm_ioctl.h
 */
#define PTM_INIT_FLAG_DELETE_VOLATILE 1

#define CMD_GET_CAPABILITY        0x01
#define CMD_INIT                  0x02
#define CMD_SHUTDOWN              0x03
#define CMD_GET_TPMESTABLISHED    0x04
#define CMD_SET_LOCALITY          0x05
#define CMD_HASH_START            0x06
#define CMD_HASH_DATA             0x07
#define CMD_HASH_END              0x08
#define CMD_CANCEL_TPM_CMD        0x09
#define CMD_STORE_VOLATILE        0x0a
#define CMD_RESET_TPMESTABLISHED  0x0b
#define CMD_GET_STATEBLOB         0x0c
#define CMD_SET_STATEBLOB         0x0d
#define CMD_STOP                  0x0e
#define CMD_GET_CONFIG            0x0f
#define CMD_SET_DATAFD            0x10
#define CMD_SET_BUFFERSIZE        0x11
#define CMD_GET_INFO              0x12

/*
 * This function wraps the "up-cast" of the opaque TCTI context type to the
 * type for the mssim TCTI context. If passed a NULL context the function
 * returns a NULL ptr. The function doesn't check magic number anymore
 * It should checked by the appropriate tcti_common_checks.
 */
TSS2_TCTI_SWTPM_CONTEXT*
tcti_swtpm_context_cast (TSS2_TCTI_CONTEXT *tcti_ctx)
{
    if (tcti_ctx == NULL)
        return NULL;

    return (TSS2_TCTI_SWTPM_CONTEXT*)tcti_ctx;
}
/*
 * This function down-casts the swtpm TCTI context to the common context
 * defined in the tcti-common module.
 */
TSS2_TCTI_COMMON_CONTEXT*
tcti_swtpm_down_cast (TSS2_TCTI_SWTPM_CONTEXT *tcti_swtpm)
{
    if (tcti_swtpm == NULL) {
        return NULL;
    }
    return &tcti_swtpm->common;
}

/*
 * This function is for sending one of the SWTPM_* control commands to the swtpm
 * simulator. These are sent over the out-of-band control socket.
 *
 * For the control channel spec, see:
 * https://github.com/stefanberger/swtpm/wiki/Control-Channel-Specification
 *
 * For data types, see swtpm/tpm_ioctl.h
 *
 * Basically, we send a command (4 bytes) followed by the parameters (if there
 * are any). The response will be a response code (4 bytes, 0 is success)
 * followed by other values (if there are any)
 *
 *
 * @param[in,out] tctiContext The tcti context.
 * @param[in]  cmd_code Control command code to send
 * @param[in]  cmd_sdu Control command payload to send (can be NULL)
 * @param[in]  cmd_sdu_len Length of the control command payload
 * @param[out] resp_code Response code received (can be NULL)
 * @param[out] resp_sdu Payload of the response (can be NULL)
 * @param[out] resp_sdu_len Length of the response's payload (can be NULL)
 * @retval TSS2_RC_SUCCESS if the received response code is zero, a TCTI error
 *         code otherwise
 */
TSS2_RC tcti_control_command (
    TSS2_TCTI_CONTEXT *tctiContext,
    uint32_t cmd_code, const void *cmd_sdu, size_t cmd_sdu_len,
    uint32_t *resp_code, void *resp_sdu, size_t *resp_sdu_len)
{
    TSS2_TCTI_SWTPM_CONTEXT *tcti_swtpm = tcti_swtpm_context_cast(tctiContext);
    TSS2_RC rc = TSS2_RC_SUCCESS;
    int ret;
    uint32_t response_code;

    if (tcti_swtpm == NULL) {
        return TSS2_TCTI_RC_BAD_REFERENCE;
    }

    if (TSS2_TCTI_MAGIC (tcti_swtpm) != TCTI_SWTPM_MAGIC) {
        return TSS2_TCTI_RC_BAD_CONTEXT;
    }

    if (cmd_sdu == NULL && cmd_sdu_len != 0) {
        return TSS2_TCTI_RC_BAD_VALUE;
    }

    LOG_DEBUG ("Issue control command: 0x%" PRIx32, cmd_code);

    uint8_t req_buf[SWTPM_CTRL_REQ_MAX_LEN] = { 0 };
    size_t req_buf_len = 0;
    uint8_t resp_buf[SWTPM_CTRL_RESP_MAX_LEN] = { 0 };
    size_t resp_buf_len = sizeof(uint32_t);

    if (tcti_swtpm->swtpm_conf.path)
        rc = socket_connect_unix (tcti_swtpm->swtpm_conf.path,
                                  1,
                                  &tcti_swtpm->ctrl_sock);
    else
        rc = socket_connect (tcti_swtpm->swtpm_conf.host,
                             tcti_swtpm->swtpm_conf.port,
                             1,
                             &tcti_swtpm->ctrl_sock);
    if (rc != TSS2_RC_SUCCESS) {
        LOG_ERROR ("Failed to connect to control socket.");
        rc = TSS2_TCTI_RC_IO_ERROR;
        goto out;
    }

    /* marshal control command code (4 bytes) */
    rc = Tss2_MU_UINT32_Marshal (cmd_code, req_buf, sizeof(req_buf),
                                 &req_buf_len);
    if (rc != TSS2_RC_SUCCESS) {
        LOG_ERROR("Failed to marshal control command code %" PRIu32 ", rc: 0x%"
                  PRIx32, cmd_code, rc);
        goto out;
    }

    /* copy command payload */
    if (cmd_sdu) {
        memcpy(req_buf + req_buf_len, cmd_sdu, cmd_sdu_len);
        req_buf_len += cmd_sdu_len;
    }

    /* transmit */
    LOGBLOB_DEBUG(req_buf, req_buf_len, "Sending %zu bytes to socket %" PRIu32
                  ":", req_buf_len, tcti_swtpm->ctrl_sock);
    ret = write_all (tcti_swtpm->ctrl_sock, req_buf, req_buf_len);
    if (ret < (ssize_t) req_buf_len) {
        LOG_ERROR("Failed to send control command %d with error: %d",
                  cmd_code, ret);
        rc = TSS2_TCTI_RC_IO_ERROR;
        goto out;
    }

    /* receive */
#ifdef _WIN32
    resp_buf_len = recv(tcti_swtpm->ctrl_sock, (char *) resp_buf,
                    sizeof(resp_buf), 0);
    if (resp_buf_len < (ssize_t) sizeof(uint32_t)) {
        LOG_ERROR("Failed to get response to control command, errno %d: %s",
                  WSAGetLastError(), strerror (WSAGetLastError()));
        rc = TSS2_TCTI_RC_IO_ERROR;
        goto out;
    }
#else
    resp_buf_len = read(tcti_swtpm->ctrl_sock, resp_buf, sizeof(resp_buf));
    if (resp_buf_len < (ssize_t) sizeof(uint32_t)) {
        LOG_ERROR ("Failed to get response to control command, errno %d: %s",
                   errno, strerror (errno));
        rc = TSS2_TCTI_RC_IO_ERROR;
        goto out;
    }
#endif
    LOGBLOB_DEBUG (resp_buf, resp_buf_len,
                   "Received %zu bytes from socket 0x%" PRIx32 ":",
                   resp_buf_len, tcti_swtpm->ctrl_sock);

    /* unmarshal response code */
    rc = Tss2_MU_UINT32_Unmarshal(resp_buf, sizeof(resp_buf), NULL,
                                  &response_code);
    if (rc != TSS2_RC_SUCCESS) {
        LOG_ERROR ("Failed to unmarshal response code of control command. rc: 0x%"
                   PRIx32, rc);
        goto out;
    }

    /* return response payload length */
    if (resp_sdu_len != NULL) {
        *resp_sdu_len = resp_buf_len - sizeof(uint32_t);
    }

    /* copy response payload */
    if (resp_sdu != NULL) {
        memcpy(resp_sdu, resp_buf +  sizeof(uint32_t),
               resp_buf_len - sizeof(uint32_t));
    }

    /* copy response code */
    if (resp_code != NULL) {
        *resp_code = response_code;
    }

    if (response_code != 0) {
        LOG_ERROR ("Control command failed with error: %" PRIu32, response_code);
        rc = TSS2_TCTI_RC_IO_ERROR;
        goto out;
    }

    rc = TSS2_RC_SUCCESS;

out:
    socket_close(&tcti_swtpm->ctrl_sock);
    return rc;
}

TSS2_RC Tss2_Tcti_Swtpm_Reset(TSS2_TCTI_CONTEXT *tctiContext)
{
    TSS2_RC rc;
    uint32_t init_flags = BE_TO_HOST_32(PTM_INIT_FLAG_DELETE_VOLATILE);

    rc = tcti_control_command(tctiContext, CMD_INIT,
                              &init_flags, sizeof(init_flags),
                              NULL, NULL, 0);
    if (rc != TSS2_RC_SUCCESS) {
        LOG_ERROR("Failed to reset TPM: 0x%" PRIx32, rc);
    }

    return rc;
}

TSS2_RC
tcti_swtpm_transmit (
    TSS2_TCTI_CONTEXT *tcti_ctx,
    size_t size,
    const uint8_t *cmd_buf)
{
    TSS2_TCTI_SWTPM_CONTEXT *tcti_swtpm = tcti_swtpm_context_cast (tcti_ctx);
    TSS2_TCTI_COMMON_CONTEXT *tcti_common = tcti_swtpm_down_cast (tcti_swtpm);
    tpm_header_t header;
    TSS2_RC rc;

    rc = tcti_common_transmit_checks (tcti_common, cmd_buf, TCTI_SWTPM_MAGIC);
    if (rc != TSS2_RC_SUCCESS) {
        return rc;
    }
    rc = header_unmarshal (cmd_buf, &header);
    if (rc != TSS2_RC_SUCCESS) {
        return rc;
    }
    if (header.size != size) {
        LOG_ERROR ("Buffer size parameter: %zu, and TPM2 command header size "
                   "field: %" PRIu32 " disagree.", size, header.size);
        return TSS2_TCTI_RC_BAD_VALUE;
    }

    LOG_DEBUG ("Sending command with TPM_CC 0x%" PRIx32 " and size %" PRIu32,
               header.code, header.size);

    if (tcti_swtpm->swtpm_conf.path)
        rc = socket_connect_unix (tcti_swtpm->swtpm_conf.path,
                                  0,
                                  &tcti_swtpm->tpm_sock);
    else
        rc = socket_connect (tcti_swtpm->swtpm_conf.host,
                             tcti_swtpm->swtpm_conf.port,
                             0,
                             &tcti_swtpm->tpm_sock);
    if (rc != TSS2_RC_SUCCESS) {
        return rc;
    }

    rc = socket_xmit_buf (tcti_swtpm->tpm_sock, cmd_buf, size);
    if (rc != TSS2_RC_SUCCESS) {
        return rc;
    }

    tcti_common->state = TCTI_STATE_RECEIVE;

    return rc;
}

/*
 * In theory, we could send a cancel command to the swtpm:
 *    tcti_control_command (tctiContext, CMD_CANCEL_TPM_CMD,
 *                          NULL, 0, NULL, NULL, 0);
 *
 * However, it seems to be not implemented. A comment states:
 *  > for cancellation to work, the TPM would have to
 *  > execute in another thread that polls on a cancel
 *  > flag
 */
TSS2_RC
tcti_swtpm_cancel (
    TSS2_TCTI_CONTEXT *tctiContext)
{
    UNUSED(tctiContext);
    return TSS2_TCTI_RC_NOT_IMPLEMENTED;
}

TSS2_RC
tcti_swtpm_set_locality (
    TSS2_TCTI_CONTEXT *tctiContext,
    uint8_t locality)
{
    TSS2_TCTI_SWTPM_CONTEXT *tcti_swtpm = tcti_swtpm_context_cast (tctiContext);
    TSS2_TCTI_COMMON_CONTEXT *tcti_common = tcti_swtpm_down_cast (tcti_swtpm);
    TSS2_RC rc;

    rc = tcti_common_set_locality_checks (tcti_common, TCTI_SWTPM_MAGIC);
    if (rc != TSS2_RC_SUCCESS) {
        return rc;
    }

    rc = tcti_control_command (tctiContext, CMD_SET_LOCALITY,
                               &locality, sizeof(locality),
                               NULL, NULL, 0);
    if (rc != TSS2_RC_SUCCESS) {
        LOG_ERROR("Failed to set locality: 0x%" PRIx32, rc);
        return rc;
    }

    tcti_common->locality = locality;
    return TSS2_RC_SUCCESS;
}

TSS2_RC
tcti_swtpm_get_poll_handles (
    TSS2_TCTI_CONTEXT *tctiContext,
    TSS2_TCTI_POLL_HANDLE *handles,
    size_t *num_handles)
{
    UNUSED(tctiContext);
    UNUSED(handles);
    UNUSED(num_handles);
    return TSS2_TCTI_RC_NOT_IMPLEMENTED;
}

void
tcti_swtpm_finalize(
    TSS2_TCTI_CONTEXT *tctiContext)
{
    TSS2_TCTI_SWTPM_CONTEXT *tcti_swtpm = tcti_swtpm_context_cast (tctiContext);

    if (tcti_swtpm == NULL) {
        return;
    }

    socket_close (&tcti_swtpm->tpm_sock);
    free (tcti_swtpm->conf_copy);
}

TSS2_RC
tcti_swtpm_receive (
    TSS2_TCTI_CONTEXT *tctiContext,
    size_t *response_size,
    unsigned char *response_buffer,
    int32_t timeout)
{
#ifdef TEST_FAPI_ASYNC
    /* Used for simulating a timeout. */
    static int wait = 0;
#endif

    TSS2_TCTI_SWTPM_CONTEXT *tcti_swtpm = tcti_swtpm_context_cast (tctiContext);
    TSS2_TCTI_COMMON_CONTEXT *tcti_common = tcti_swtpm_down_cast (tcti_swtpm);
    TSS2_RC rc;
    int ret;

    rc = tcti_common_receive_checks (tcti_common, response_size, TCTI_SWTPM_MAGIC);
    if (rc != TSS2_RC_SUCCESS) {
        return rc;
    }

    if (timeout != TSS2_TCTI_TIMEOUT_BLOCK) {
        LOG_TRACE("Asynchronous I/O not actually implemented.");
#ifdef TEST_FAPI_ASYNC
        if (wait < 1) {
            LOG_TRACE("Simulating Async by requesting another invocation.");
            wait += 1;
            return TSS2_TCTI_RC_TRY_AGAIN;
        } else {
            LOG_TRACE("Sending the actual result.");
            wait = 0;
        }
#endif /* TEST_FAPI_ASYNC */
    }

    if (tcti_common->header.size == 0) {
        LOG_DEBUG("Receiving header to determine the size of the response.");
        uint8_t res_header[10];
        ret = socket_recv_buf (tcti_swtpm->tpm_sock, &res_header[0], 10);
        if (ret != 10) {
            rc = TSS2_TCTI_RC_IO_ERROR;
            goto out;
        }

        rc = header_unmarshal (&res_header[0], &tcti_common->header);
        if (rc != TSS2_RC_SUCCESS) {
            LOG_ERROR ("Failed to unmarshal tpm2 header: 0x%" PRIx32, rc);
            goto out;
        }

        LOG_DEBUG ("response size: %" PRIu32, tcti_common->header.size);
    }

    if (response_buffer == NULL) {
        *response_size = tcti_common->header.size;
        return TSS2_RC_SUCCESS;
    }

    if (*response_size < tcti_common->header.size) {
        *response_size = tcti_common->header.size;
        return TSS2_TCTI_RC_INSUFFICIENT_BUFFER;
    }
    *response_size = tcti_common->header.size;

    if (tcti_common->header.size > 10) {
        LOG_DEBUG ("Reading response of size %" PRIu32, tcti_common->header.size);
        ret = socket_recv_buf (tcti_swtpm->tpm_sock,
                               (unsigned char *)&response_buffer[10],
                               tcti_common->header.size - 10);
        if (ret < (ssize_t)tcti_common->header.size - 10) {
            rc = TSS2_TCTI_RC_IO_ERROR;
            goto out;
        }
    }

    rc = header_marshal (&tcti_common->header, &response_buffer[0]);
    if (rc != TSS2_RC_SUCCESS) {
        LOG_WARNING ("Failed to remarshal tpm2 header: 0x%"PRIu32, rc);
        goto out;
    }

    LOGBLOB_DEBUG(response_buffer, tcti_common->header.size,
                  "Response received:");
    /*
     * Executing code beyond this point transitions the state machine to
     * TRANSMIT. Another call to this function will not be possible until
     * another command is sent to the TPM.
     */
out:
    socket_close (&tcti_swtpm->tpm_sock);

    tcti_common->header.size = 0;
    tcti_common->state = TCTI_STATE_TRANSMIT;

    return rc;
}

/*
 * This is a utility function to extract a TCP port number from a string.
 * The string must be 6 characters long. If the supplied string contains an
 * invalid port number then 0 is returned.
 */
static uint16_t
string_to_port (char port_str[6])
{
    uint32_t port = 0;

    if (sscanf (port_str, "%" SCNu32, &port) == EOF || port > UINT16_MAX) {
        return 0;
    }
    return port;
}
/*
 * This function is a callback conforming to the KeyValueFunc prototype. It
 * is called by the key-value-parse module for each key / value pair extracted
 * from the configuration string. Its sole purpose is to identify valid keys
 * from the conf string and to store their corresponding values in the
 * swtpm_conf_t structure which is passed through the 'user_data' parameter.
 */
TSS2_RC
swtpm_kv_callback (const key_value_t *key_value,
                   void *user_data)
{
    swtpm_conf_t *swtpm_conf = (swtpm_conf_t*)user_data;

    LOG_TRACE ("key_value: 0x%" PRIxPTR " and user_data: 0x%" PRIxPTR,
               (uintptr_t)key_value, (uintptr_t)user_data);
    if (key_value == NULL || user_data == NULL) {
        LOG_WARNING ("%s passed NULL parameter", __func__);
        return TSS2_TCTI_RC_GENERAL_FAILURE;
    }
    LOG_DEBUG ("key: %s / value: %s\n", key_value->key, key_value->value);
    if (strcmp (key_value->key, "host") == 0) {
        swtpm_conf->host = key_value->value;
        swtpm_conf->path = NULL;
        return TSS2_RC_SUCCESS;
    } else if (strcmp (key_value->key, "port") == 0) {
        swtpm_conf->port = string_to_port (key_value->value);
        if (swtpm_conf->port == 0) {
            return TSS2_TCTI_RC_BAD_VALUE;
        }
        return TSS2_RC_SUCCESS;
    } else if (strcmp (key_value->key, "path") == 0) {
        swtpm_conf->path = key_value->value;
        swtpm_conf->host = NULL;
        return TSS2_RC_SUCCESS;
    } else {
        return TSS2_TCTI_RC_BAD_VALUE;
    }
}
void
tcti_swtpm_init_context_data (
    TSS2_TCTI_COMMON_CONTEXT *tcti_common)
{
    TSS2_TCTI_MAGIC (tcti_common) = TCTI_SWTPM_MAGIC;
    TSS2_TCTI_VERSION (tcti_common) = TCTI_VERSION;
    TSS2_TCTI_TRANSMIT (tcti_common) = tcti_swtpm_transmit;
    TSS2_TCTI_RECEIVE (tcti_common) = tcti_swtpm_receive;
    TSS2_TCTI_FINALIZE (tcti_common) = tcti_swtpm_finalize;
    TSS2_TCTI_CANCEL (tcti_common) = tcti_swtpm_cancel;
    TSS2_TCTI_GET_POLL_HANDLES (tcti_common) = tcti_swtpm_get_poll_handles;
    TSS2_TCTI_SET_LOCALITY (tcti_common) = tcti_swtpm_set_locality;
    TSS2_TCTI_MAKE_STICKY (tcti_common) = tcti_make_sticky_not_implemented;
    tcti_common->state = TCTI_STATE_TRANSMIT;
    memset (&tcti_common->header, 0, sizeof (tcti_common->header));
}
/*
 * This is an implementation of the standard TCTI initialization function for
 * this module.
 */
TSS2_RC
Tss2_Tcti_Swtpm_Init (
    TSS2_TCTI_CONTEXT *tctiContext,
    size_t *size,
    const char *conf)
{
    TSS2_TCTI_SWTPM_CONTEXT *tcti_swtpm = (TSS2_TCTI_SWTPM_CONTEXT*)tctiContext;
    TSS2_TCTI_COMMON_CONTEXT *tcti_common = tcti_swtpm_down_cast (tcti_swtpm);
    TSS2_RC rc;
    if (conf == NULL) {
        LOG_TRACE ("tctiContext: 0x%" PRIxPTR ", size: 0x%" PRIxPTR ""
                   " default configuration will be used.",
                   (uintptr_t)tctiContext, (uintptr_t)size);
    } else {
        LOG_TRACE ("tctiContext: 0x%" PRIxPTR ", size: 0x%" PRIxPTR ", conf: %s",
                   (uintptr_t)tctiContext, (uintptr_t)size, conf);
    }
    if (size == NULL) {
        return TSS2_TCTI_RC_BAD_VALUE;
    }
    if (tctiContext == NULL) {
        *size = sizeof (TSS2_TCTI_SWTPM_CONTEXT);
        return TSS2_RC_SUCCESS;
    }

    tcti_swtpm->swtpm_conf.host = TCTI_SWTPM_DEFAULT_HOST;
    tcti_swtpm->swtpm_conf.port = TCTI_SWTPM_DEFAULT_PORT;

    if (conf != NULL) {
        LOG_TRACE ("conf is not NULL");
        if (strlen (conf) > TCTI_SWTPM_CONF_MAX) {
            LOG_WARNING ("Provided conf string exceeds maximum of %u",
                         TCTI_SWTPM_CONF_MAX);
            return TSS2_TCTI_RC_BAD_VALUE;
        }
        tcti_swtpm->conf_copy = strdup (conf);
        if (tcti_swtpm->conf_copy == NULL) {
            LOG_ERROR ("Failed to allocate buffer: %s", strerror (errno));
            return TSS2_TCTI_RC_GENERAL_FAILURE;
        }
        LOG_DEBUG ("Dup'd conf string to: 0x%" PRIxPTR,
                   (uintptr_t)tcti_swtpm->conf_copy);
        rc = parse_key_value_string (tcti_swtpm->conf_copy,
                                     swtpm_kv_callback,
                                     &tcti_swtpm->swtpm_conf);
        if (rc != TSS2_RC_SUCCESS) {
            goto fail_out;
        }
    }
    LOG_DEBUG ("Initializing swtpm TCTI with host: %s, port: %" PRIu16,
               tcti_swtpm->swtpm_conf.host, tcti_swtpm->swtpm_conf.port);

    tcti_swtpm->tpm_sock = -1;
    tcti_swtpm->ctrl_sock = -1;

    /* sanity check */
    if (tcti_swtpm->swtpm_conf.path)
        rc = socket_connect_unix (tcti_swtpm->swtpm_conf.path,
                                  0,
                                  &tcti_swtpm->tpm_sock);
    else
        rc = socket_connect (tcti_swtpm->swtpm_conf.host,
                             tcti_swtpm->swtpm_conf.port,
                             0,
                             &tcti_swtpm->tpm_sock);
    socket_close (&tcti_swtpm->tpm_sock);
    if (rc != TSS2_RC_SUCCESS) {
        LOG_ERROR ("Cannot connect to swtpm TPM socket");
        goto fail_out;
    }

    tcti_swtpm_init_context_data (tcti_common);

    rc = tcti_swtpm_set_locality(tctiContext, 0);
    if (rc != TSS2_RC_SUCCESS) {
        LOG_WARNING ("Could not set locality via control channel: 0x%" PRIx32,
                     rc);
        return rc;
    }


    return TSS2_RC_SUCCESS;

fail_out:
    free (tcti_swtpm->conf_copy);

    return rc;
}

/* public info structure */
const TSS2_TCTI_INFO tss2_tcti_info = {
    .version = TCTI_VERSION,
    .name = "tcti-swtpm",
    .description = "TCTI module for communication with the swtpm.",
    .config_help = "Key / value string in the form \"host=localhost,port=2321\".",
    .init = Tss2_Tcti_Swtpm_Init,
};

const TSS2_TCTI_INFO*
Tss2_Tcti_Info (void)
{
    return &tss2_tcti_info;
}
