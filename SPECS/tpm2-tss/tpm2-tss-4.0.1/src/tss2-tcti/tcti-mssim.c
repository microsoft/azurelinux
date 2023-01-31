/* SPDX-License-Identifier: BSD-2-Clause */
/*
 * Copyright (c) 2015 - 2018 Intel Corporation
 * All rights reserved.
 */

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
#include "tss2_tcti_mssim.h"

#include "tcti-mssim.h"
#include "tcti-common.h"
#include "util/key-value-parse.h"
#define LOGMODULE tcti
#include "util/log.h"

/*
 * This function wraps the "up-cast" of the opaque TCTI context type to the
 * type for the mssim TCTI context. If passed a NULL context the function
 * returns a NULL ptr. The function doesn't check magic number anymore
 * It should checked by the appropriate tcti_common_checks.
 */
TSS2_TCTI_MSSIM_CONTEXT*
tcti_mssim_context_cast (TSS2_TCTI_CONTEXT *tcti_ctx)
{
    if (tcti_ctx == NULL)
        return NULL;

    return (TSS2_TCTI_MSSIM_CONTEXT*)tcti_ctx;
}
/*
 * This function down-casts the mssim TCTI context to the common context
 * defined in the tcti-common module.
 */
TSS2_TCTI_COMMON_CONTEXT*
tcti_mssim_down_cast (TSS2_TCTI_MSSIM_CONTEXT *tcti_mssim)
{
    if (tcti_mssim == NULL) {
        return NULL;
    }
    return &tcti_mssim->common;
}
/*
 * This function is for sending one of the MS_SIM_* platform commands to the
 * Microsoft TPM2 simulator. These are sent over the platform socket.
 */
TSS2_RC tcti_platform_command (
    TSS2_TCTI_CONTEXT *tctiContext,
    UINT32 cmd)
{
    TSS2_TCTI_MSSIM_CONTEXT *tcti_mssim = tcti_mssim_context_cast (tctiContext);
    uint8_t buf [sizeof (cmd)] = { 0 };
    UINT32 rsp = 0;
    TSS2_RC rc = TSS2_RC_SUCCESS;
    int ret;
    ssize_t read_ret;

    if (tcti_mssim == NULL) {
        return TSS2_TCTI_RC_BAD_REFERENCE;
    }

    if (TSS2_TCTI_MAGIC (tcti_mssim) != TCTI_MSSIM_MAGIC) {
        return TSS2_TCTI_RC_BAD_CONTEXT;
    }

    rc = Tss2_MU_UINT32_Marshal (cmd, buf, sizeof (cmd), NULL);
    if (rc != TSS2_RC_SUCCESS) {
        LOG_ERROR ("Failed to marshal platform command %" PRIu32 ", rc: 0x%"
                   PRIx32, cmd, rc);
        return rc;
    }

    LOGBLOB_DEBUG(buf, sizeof (cmd), "Sending %zu bytes to socket %" PRIu32
                  ":", sizeof (cmd), tcti_mssim->platform_sock);
    ret = write_all (tcti_mssim->platform_sock, buf, sizeof (cmd));
    if (ret < (ssize_t) sizeof (cmd)) {
        LOG_ERROR("Failed to send platform command %d with error: %d",
                  cmd, ret);
        return TSS2_TCTI_RC_IO_ERROR;
    }

#ifdef _WIN32
    read_ret = recv (tcti_mssim->platform_sock, (char *) buf, sizeof (buf), 0);
    if (read_ret < (ssize_t) sizeof (buf)) {
        LOG_ERROR ("Failed to get response to platform command, errno %d: %s",
                   WSAGetLastError(), strerror (WSAGetLastError()));
        return TSS2_TCTI_RC_IO_ERROR;
    }
#else
    read_ret = read(tcti_mssim->platform_sock, buf, sizeof (buf));
    if (read_ret < (ssize_t) sizeof (buf)) {
        LOG_ERROR ("Failed to get response to platform command, errno %d: %s",
                   errno, strerror (errno));
        return TSS2_TCTI_RC_IO_ERROR;
    }
#endif
    LOGBLOB_DEBUG (buf, sizeof (buf), "Received %zu bytes from socket 0x%"
                   PRIx32 ":", read_ret, tcti_mssim->platform_sock);
    rc = Tss2_MU_UINT32_Unmarshal (buf, sizeof (rsp), NULL, &rsp);
    if (rc != TSS2_RC_SUCCESS) {
        LOG_ERROR ("Failed to unmarshal response to platform command. rc: 0x%"
                   PRIx32, rc);
        return rc;
    }
    if (rsp != 0) {
        LOG_INFO ("Platform command failed with error: %" PRIu32, rsp);
        return TSS2_TCTI_RC_IO_ERROR;
    }
    return rc;
}
/*
 * This function sends the special TPM_SESSION_END message over the provided
 * socket.
 */
TSS2_RC
send_sim_session_end (
    SOCKET sock)
{
    uint8_t buf [4] = { 0, };
    TSS2_RC rc;

    rc = Tss2_MU_UINT32_Marshal (TPM_SESSION_END, buf, sizeof (buf), NULL);
    if (rc == TSS2_RC_SUCCESS) {
        return rc;
    }
    return socket_xmit_buf (sock, buf, sizeof (buf));
}

/*
 * This function is used to send the simulator a sort of command message
 * that tells it we're about to send it a TPM command. This requires that
 * we first send it a 4 byte code that's defined by the simulator. Then
 * another byte identifying the locality and finally the size of the TPM
 * command buffer that we're about to send. After these 9 bytes are sent
 * the simulator will accept a TPM command buffer.
 */
#define SIM_CMD_SIZE (sizeof (UINT32) + sizeof (UINT8) + sizeof (UINT32))
TSS2_RC
send_sim_cmd_setup (
    TSS2_TCTI_MSSIM_CONTEXT *tcti_mssim,
    UINT32 size)
{
    TSS2_TCTI_COMMON_CONTEXT *tcti_common = tcti_mssim_down_cast (tcti_mssim);
    uint8_t buf [SIM_CMD_SIZE] = { 0 };
    size_t offset = 0;
    TSS2_RC rc;

    rc = Tss2_MU_UINT32_Marshal (MS_SIM_TPM_SEND_COMMAND,
                                 buf,
                                 sizeof (buf),
                                 &offset);
    if (rc != TSS2_RC_SUCCESS) {
        return rc;
    }

    rc = Tss2_MU_UINT8_Marshal (tcti_common->locality,
                                buf,
                                sizeof (buf),
                                &offset);
    if (rc != TSS2_RC_SUCCESS) {
        return rc;
    }

    rc = Tss2_MU_UINT32_Marshal (size, buf, sizeof (buf), &offset);
    if (rc != TSS2_RC_SUCCESS) {
        return rc;
    }

    return socket_xmit_buf (tcti_mssim->tpm_sock, buf, sizeof (buf));
}

TSS2_RC
tcti_mssim_transmit (
    TSS2_TCTI_CONTEXT *tcti_ctx,
    size_t size,
    const uint8_t *cmd_buf)
{
    TSS2_TCTI_MSSIM_CONTEXT *tcti_mssim = tcti_mssim_context_cast (tcti_ctx);
    TSS2_TCTI_COMMON_CONTEXT *tcti_common = tcti_mssim_down_cast (tcti_mssim);
    tpm_header_t header;
    TSS2_RC rc;

    rc = tcti_common_transmit_checks (tcti_common, cmd_buf, TCTI_MSSIM_MAGIC);
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
    rc = send_sim_cmd_setup (tcti_mssim, header.size);
    if (rc != TSS2_RC_SUCCESS) {
        return rc;
    }
    rc = socket_xmit_buf (tcti_mssim->tpm_sock, cmd_buf, size);
    if (rc != TSS2_RC_SUCCESS) {
        return rc;
    }

    tcti_common->state = TCTI_STATE_RECEIVE;

    return rc;
}

TSS2_RC
tcti_mssim_cancel (
    TSS2_TCTI_CONTEXT *tctiContext)
{
    TSS2_TCTI_MSSIM_CONTEXT *tcti_mssim = tcti_mssim_context_cast (tctiContext);
    TSS2_TCTI_COMMON_CONTEXT *tcti_common = tcti_mssim_down_cast (tcti_mssim);
    TSS2_RC rc;

    rc = tcti_common_cancel_checks (tcti_common, TCTI_MSSIM_MAGIC);
    if (rc != TSS2_RC_SUCCESS) {
        return rc;
    }
    rc = tcti_platform_command (tctiContext, MS_SIM_CANCEL_ON);
    if (rc != TSS2_RC_SUCCESS) {
        return rc;
    }

    tcti_common->state = TCTI_STATE_TRANSMIT;
    tcti_mssim->cancel = 1;

    return rc;
}

TSS2_RC
tcti_mssim_set_locality (
    TSS2_TCTI_CONTEXT *tctiContext,
    uint8_t locality)
{
    TSS2_TCTI_MSSIM_CONTEXT *tcti_mssim = tcti_mssim_context_cast (tctiContext);
    TSS2_TCTI_COMMON_CONTEXT *tcti_common = tcti_mssim_down_cast (tcti_mssim);
    TSS2_RC rc;

    rc = tcti_common_set_locality_checks (tcti_common, TCTI_MSSIM_MAGIC);
    if (rc != TSS2_RC_SUCCESS) {
        return rc;
    }

    tcti_common->locality = locality;
    return TSS2_RC_SUCCESS;
}

TSS2_RC
tcti_mssim_get_poll_handles (
    TSS2_TCTI_CONTEXT *tctiContext,
    TSS2_TCTI_POLL_HANDLE *handles,
    size_t *num_handles)
{
    TSS2_TCTI_MSSIM_CONTEXT *tcti_mssim = tcti_mssim_context_cast (tctiContext);

    if (num_handles == NULL || tcti_mssim == NULL) {
        return TSS2_TCTI_RC_BAD_REFERENCE;
    }

    if (handles != NULL && *num_handles < 1) {
        return TSS2_TCTI_RC_BAD_VALUE;
    }

    *num_handles = 1;
    if (handles != NULL) {
#ifdef _WIN32
        *handles = tcti_mssim->tpm_sock;
#else
        handles->fd = tcti_mssim->tpm_sock;
        handles->events = POLLIN | POLLOUT;
#endif
    }

    return TSS2_RC_SUCCESS;
}

void
tcti_mssim_finalize(
    TSS2_TCTI_CONTEXT *tctiContext)
{
    TSS2_TCTI_MSSIM_CONTEXT *tcti_mssim = tcti_mssim_context_cast (tctiContext);

    if (tcti_mssim == NULL) {
        return;
    }
    send_sim_session_end (tcti_mssim->platform_sock);
    send_sim_session_end (tcti_mssim->tpm_sock);
    socket_close (&tcti_mssim->platform_sock);
    socket_close (&tcti_mssim->tpm_sock);
}

TSS2_RC
tcti_mssim_receive (
    TSS2_TCTI_CONTEXT *tctiContext,
    size_t *response_size,
    unsigned char *response_buffer,
    int32_t timeout)
{
#ifdef TEST_FAPI_ASYNC
    /* Used for simulating a timeout. */
    static int wait = 0;
#endif
    TSS2_TCTI_MSSIM_CONTEXT *tcti_mssim = tcti_mssim_context_cast (tctiContext);
    TSS2_TCTI_COMMON_CONTEXT *tcti_common = tcti_mssim_down_cast (tcti_mssim);
    TSS2_RC rc;
    UINT32 trash;
    int ret;

    rc = tcti_common_receive_checks (tcti_common,
                                     response_size,
                                     TCTI_MSSIM_MAGIC);
    if (rc != TSS2_RC_SUCCESS) {
        return rc;
    }

    if (timeout != TSS2_TCTI_TIMEOUT_BLOCK) {
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
        /* Receive the size of the response. */
        uint8_t size_buf [sizeof (UINT32)];

        ret = socket_poll(tcti_mssim->tpm_sock, timeout);
        if (ret != TSS2_RC_SUCCESS) {
            if (ret == TSS2_TCTI_RC_TRY_AGAIN) {
                return ret;
            }
            rc = ret;
            goto out;
        }
        ret = socket_recv_buf (tcti_mssim->tpm_sock, size_buf, sizeof(UINT32));
        if (ret != sizeof (UINT32)) {
            rc = TSS2_TCTI_RC_IO_ERROR;
            goto out;
        }

        rc = Tss2_MU_UINT32_Unmarshal (size_buf,
                                       sizeof (size_buf), 0,
                                       &tcti_common->header.size);
        if (rc != TSS2_RC_SUCCESS) {
            LOG_WARNING ("Failed to unmarshal size from tpm2 simulator "
                         "protocol: 0x%" PRIu32, rc);
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
        LOG_ERROR("Response size to big: %zu > %u", *response_size, tcti_common->header.size);
        return TSS2_TCTI_RC_INSUFFICIENT_BUFFER;
    }
    *response_size = tcti_common->header.size;

    /* Receive the TPM response. */
    LOG_DEBUG ("Reading response of size %" PRIu32, tcti_common->header.size);
    ret = socket_poll(tcti_mssim->tpm_sock, timeout);
    if (ret != TSS2_RC_SUCCESS) {
        if (ret == TSS2_TCTI_RC_TRY_AGAIN) {
            return ret;
        }
        rc = ret;
        goto out;
    }
    ret = socket_recv_buf (tcti_mssim->tpm_sock,
                           (unsigned char *)response_buffer,
                           tcti_common->header.size);
    if (ret < (ssize_t)tcti_common->header.size) {
        rc = TSS2_TCTI_RC_IO_ERROR;
        goto out;
    }
    LOGBLOB_DEBUG(response_buffer, tcti_common->header.size,
                  "Response buffer received:");

    ret = socket_poll (tcti_mssim->tpm_sock, timeout);
    if (ret != TSS2_RC_SUCCESS) {
        if (ret == TSS2_TCTI_RC_TRY_AGAIN) {
            return ret;
        }
        rc = ret;
        goto out;
    }

    /* Receive the appended four bytes of 0's */
    ret = socket_recv_buf (tcti_mssim->tpm_sock,
                           (unsigned char *)&trash, 4);
    if (ret != 4) {
        LOG_DEBUG ("Error reading last 4 bytes %" PRIu32, ret);
        rc = TSS2_TCTI_RC_IO_ERROR;
        goto out;
    }

    if (tcti_mssim->cancel) {
        rc = tcti_platform_command (tctiContext, MS_SIM_CANCEL_OFF);
        tcti_mssim->cancel = 0;
    }
    /*
     * Executing code beyond this point transitions the state machine to
     * TRANSMIT. Another call to this function will not be possible until
     * another command is sent to the TPM.
     */
out:
    tcti_common->header.size = 0;
    tcti_common->state = TCTI_STATE_TRANSMIT;

    return rc;
}

/**
 * This function sends the Microsoft simulator the MS_SIM_POWER_ON and
 * MS_SIM_NV_ON commands using the platform command mechanism. Without
 * these the simulator will respond with zero sized buffer which causes
 * the TSS to freak out. Sending this command more than once is harmless,
 * so it's advisable to call this function as part of the TCTI context
 * initialization just to be sure.
 *
 * NOTE: The caller will still need to call Tss2_Sys_Startup. If they
 * don't, an error will be returned from each call till they do but
 * the error will at least be meaningful (TPM2_RC_INITIALIZE).
 */
static TSS2_RC
simulator_setup (
    TSS2_TCTI_CONTEXT *tctiContext)
{
    TSS2_RC rc;

    LOG_TRACE ("Initializing TCTI context 0x%" PRIxPTR,
               (uintptr_t)tctiContext);
    rc = tcti_platform_command (tctiContext, MS_SIM_POWER_ON);
    if (rc != TSS2_RC_SUCCESS) {
        LOG_WARNING ("Failed to send MS_SIM_POWER_ON platform command.");
        return rc;
    }

    rc = tcti_platform_command (tctiContext, MS_SIM_NV_ON);
    if (rc != TSS2_RC_SUCCESS) {
        LOG_WARNING ("Failed to send MS_SIM_NV_ON platform command.");
    }

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
 * mssim_conf_t structure which is passed through the 'user_data' parameter.
 */
TSS2_RC
mssim_kv_callback (const key_value_t *key_value,
                   void *user_data)
{
    mssim_conf_t *mssim_conf = (mssim_conf_t*)user_data;

    LOG_TRACE ("key_value: 0x%" PRIxPTR " and user_data: 0x%" PRIxPTR,
               (uintptr_t)key_value, (uintptr_t)user_data);
    if (key_value == NULL || user_data == NULL) {
        LOG_WARNING ("%s passed NULL parameter", __func__);
        return TSS2_TCTI_RC_GENERAL_FAILURE;
    }
    LOG_DEBUG ("key: %s / value: %s\n", key_value->key, key_value->value);
    if (strcmp (key_value->key, "host") == 0) {
        mssim_conf->host = key_value->value;
        mssim_conf->path = NULL;
        return TSS2_RC_SUCCESS;
    } else if (strcmp (key_value->key, "port") == 0) {
        mssim_conf->port = string_to_port (key_value->value);
        if (mssim_conf->port == 0) {
            return TSS2_TCTI_RC_BAD_VALUE;
        }
        return TSS2_RC_SUCCESS;
    } else if (strcmp (key_value->key, "path") == 0) {
        mssim_conf->path = key_value->value;
        mssim_conf->host = NULL;
        return TSS2_RC_SUCCESS;
    } else {
        return TSS2_TCTI_RC_BAD_VALUE;
    }
}
void
tcti_mssim_init_context_data (
    TSS2_TCTI_COMMON_CONTEXT *tcti_common)
{
    TSS2_TCTI_MAGIC (tcti_common) = TCTI_MSSIM_MAGIC;
    TSS2_TCTI_VERSION (tcti_common) = TCTI_VERSION;
    TSS2_TCTI_TRANSMIT (tcti_common) = tcti_mssim_transmit;
    TSS2_TCTI_RECEIVE (tcti_common) = tcti_mssim_receive;
    TSS2_TCTI_FINALIZE (tcti_common) = tcti_mssim_finalize;
    TSS2_TCTI_CANCEL (tcti_common) = tcti_mssim_cancel;
    TSS2_TCTI_GET_POLL_HANDLES (tcti_common) = tcti_mssim_get_poll_handles;
    TSS2_TCTI_SET_LOCALITY (tcti_common) = tcti_mssim_set_locality;
    TSS2_TCTI_MAKE_STICKY (tcti_common) = tcti_make_sticky_not_implemented;
    tcti_common->state = TCTI_STATE_TRANSMIT;
    tcti_common->locality = 0;
    memset (&tcti_common->header, 0, sizeof (tcti_common->header));
}
/*
 * This is an implementation of the standard TCTI initialization function for
 * this module.
 */
TSS2_RC
Tss2_Tcti_Mssim_Init (
    TSS2_TCTI_CONTEXT *tctiContext,
    size_t *size,
    const char *conf)
{
    TSS2_TCTI_MSSIM_CONTEXT *tcti_mssim = (TSS2_TCTI_MSSIM_CONTEXT*)tctiContext;
    TSS2_TCTI_COMMON_CONTEXT *tcti_common = tcti_mssim_down_cast (tcti_mssim);
    TSS2_RC rc;
    char *conf_copy = NULL;
    mssim_conf_t mssim_conf = MSSIM_CONF_DEFAULT_INIT;

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
        *size = sizeof (TSS2_TCTI_MSSIM_CONTEXT);
        return TSS2_RC_SUCCESS;
    }

    if (conf != NULL) {
        LOG_TRACE ("conf is not NULL");
        if (strlen (conf) > TCTI_MSSIM_CONF_MAX) {
            LOG_WARNING ("Provided conf string exceeds maximum of %u",
                         TCTI_MSSIM_CONF_MAX);
            return TSS2_TCTI_RC_BAD_VALUE;
        }
        conf_copy = strdup (conf);
        if (conf_copy == NULL) {
            LOG_ERROR ("Failed to allocate buffer: %s", strerror (errno));
            rc = TSS2_TCTI_RC_GENERAL_FAILURE;
            goto fail_out;
        }
        LOG_DEBUG ("Dup'd conf string to: 0x%" PRIxPTR,
                   (uintptr_t)conf_copy);
        rc = parse_key_value_string (conf_copy,
                                     mssim_kv_callback,
                                     &mssim_conf);
        if (rc != TSS2_RC_SUCCESS) {
            goto fail_out;
        }
    }
    LOG_DEBUG ("Initializing mssim TCTI with host: %s, port: %" PRIu16,
               mssim_conf.host, mssim_conf.port);

    tcti_mssim->tpm_sock = -1;
    tcti_mssim->platform_sock = -1;

    if (mssim_conf.path)
        rc = socket_connect_unix (mssim_conf.path,
                                  0,
                                  &tcti_mssim->tpm_sock);
    else
        rc = socket_connect (mssim_conf.host,
                             mssim_conf.port,
                             0,
                             &tcti_mssim->tpm_sock);
    if (rc != TSS2_RC_SUCCESS) {
        goto fail_out;
    }

    rc = socket_set_nonblock (tcti_mssim->tpm_sock);
    if (rc != TSS2_RC_SUCCESS) {
        goto fail_out;
    }

    if (mssim_conf.path)
        rc = socket_connect_unix (mssim_conf.path,
                                  1,
                                  &tcti_mssim->platform_sock);
    else
        rc = socket_connect (mssim_conf.host,
                             mssim_conf.port,
                             1,
                             &tcti_mssim->platform_sock);
    if (rc != TSS2_RC_SUCCESS) {
        goto fail_out;
    }

    tcti_mssim_init_context_data (tcti_common);
    rc = simulator_setup (tctiContext);
    if (rc != TSS2_RC_SUCCESS) {
        goto fail_out;
    }

    if (conf_copy != NULL) {
        free (conf_copy);
    }
    return TSS2_RC_SUCCESS;

fail_out:
    if (conf_copy != NULL) {
        free (conf_copy);
    }
    socket_close (&tcti_mssim->tpm_sock);
    socket_close (&tcti_mssim->platform_sock);

    return rc;
}

/* public info structure */
const TSS2_TCTI_INFO tss2_tcti_info = {
    .version = TCTI_VERSION,
    .name = "tcti-socket",
    .description = "TCTI module for communication with the Microsoft TPM2 Simulator.",
    .config_help = "Key / value string in the form \"host=localhost,port=2321\".",
    .init = Tss2_Tcti_Mssim_Init,
};

const TSS2_TCTI_INFO*
Tss2_Tcti_Info (void)
{
    return &tss2_tcti_info;
}
