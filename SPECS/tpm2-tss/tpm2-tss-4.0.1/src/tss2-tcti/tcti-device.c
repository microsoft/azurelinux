/* SPDX-License-Identifier: BSD-2-Clause */
/*
 * Copyright (c) 2015 - 2018 Intel Corporation
 * All rights reserved.
 * Copyright (c) 2019, Wind River Systems.
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *
 * 1. Redistributions of source code must retain the above copyright notice,
 * this list of conditions and the following disclaimer.
 *
 * 2. Redistributions in binary form must reproduce the above copyright notice,
 * this list of conditions and the following disclaimer in the documentation
 * and/or other materials provided with the distribution.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
 * LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
 * SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
 * INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
 * CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 * ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
 * THE POSSIBILITY OF SUCH DAMAGE.
 */

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <errno.h>
#include <fcntl.h>
#include <inttypes.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/types.h>
#ifdef __VXWORKS__
#include <sys/poll.h>
#else
#include <poll.h>
#endif
#include <unistd.h>

#include "tss2_tcti.h"
#include "tss2_tcti_device.h"
#include "tss2_mu.h"
#include "tcti-common.h"
#include "tcti-device.h"
#include "util/io.h"
#include "util/aux_util.h"
#define LOGMODULE tcti
#include "util/log.h"

static char *default_conf[] = {
#ifdef __VXWORKS__
    "/tpm0"
#else
    "/dev/tpmrm0",
    "/dev/tpm0",
#endif /* __VX_WORKS__ */
};

/*
 * This function wraps the "up-cast" of the opaque TCTI context type to the
 * type for the mssim TCTI context. If passed a NULL context the function
 * returns a NULL ptr. The function doesn't check magic number anymore
 * It should checked by the appropriate tcti_common_checks.
 */
TSS2_TCTI_DEVICE_CONTEXT*
tcti_device_context_cast (TSS2_TCTI_CONTEXT *tcti_ctx)
{
    if (tcti_ctx == NULL)
        return NULL;

    return (TSS2_TCTI_DEVICE_CONTEXT*)tcti_ctx;
}
/*
 * This function down-casts the device TCTI context to the common context
 * defined in the tcti-common module.
 */
TSS2_TCTI_COMMON_CONTEXT*
tcti_device_down_cast (TSS2_TCTI_DEVICE_CONTEXT *tcti_dev)
{
    if (tcti_dev == NULL) {
        return NULL;
    }
    return &tcti_dev->common;
}

TSS2_RC
tcti_device_transmit (
    TSS2_TCTI_CONTEXT *tctiContext,
    size_t command_size,
    const uint8_t *command_buffer)
{
    TSS2_TCTI_DEVICE_CONTEXT *tcti_dev = tcti_device_context_cast (tctiContext);
    TSS2_TCTI_COMMON_CONTEXT *tcti_common = tcti_device_down_cast (tcti_dev);
    TSS2_RC rc = TSS2_RC_SUCCESS;
    ssize_t size;

    rc = tcti_common_transmit_checks (tcti_common,
                                      command_buffer,
                                      TCTI_DEVICE_MAGIC);
    if (rc != TSS2_RC_SUCCESS) {
        return rc;
    }
    LOGBLOB_DEBUG (command_buffer,
                   command_size,
                   "sending %zu byte command buffer:",
                   command_size);
    size = write_all (tcti_dev->fd,
                      command_buffer,
                      command_size);
    if (size < 0) {
        return TSS2_TCTI_RC_IO_ERROR;
    } else if ((size_t)size != command_size) {
        LOG_ERROR ("wrong number of bytes written. Expected %zu, wrote %zd.",
                   command_size,
                   size);
        return TSS2_TCTI_RC_IO_ERROR;
    }

    tcti_common->state = TCTI_STATE_RECEIVE;
    return TSS2_RC_SUCCESS;
}
/*
 * This receive function deviates from the spec a bit. Calling this function
 * with a NULL 'tctiContext' parameter *should* result in the required size for
 * the response buffer being returned to the caller. We would typically do this
 * by reading the response's header and then returning the size to the caller.
 * We can't do that on account of the TPM2 kernel driver closing any connection
 * that doesn't read the whole response buffer in one 'read' call.
 *
 * Instead, if the caller queries the size, we return 4k just to be on the
 * safe side. We do *not* however verify that the provided buffer is large
 * enough to hold the full response (we can't). If the caller provides us with
 * a buffer less than 4k we'll read as much of the response as we can given
 * the size of the buffer. If we get enough of the response to read the size
 * field, we check to see if the buffer was large enough to get the full
 * response. If the response header claims it's larger than the provided
 * buffer we print a warning. This allows "expert applications" to
 * precalculate the required response buffer size for whatever commands they
 * may send.
 */
TSS2_RC
tcti_device_receive (
    TSS2_TCTI_CONTEXT *tctiContext,
    size_t *response_size,
    uint8_t *response_buffer,
    int32_t timeout)
{
    TSS2_TCTI_DEVICE_CONTEXT *tcti_dev = tcti_device_context_cast (tctiContext);
    TSS2_TCTI_COMMON_CONTEXT *tcti_common = tcti_device_down_cast (tcti_dev);
    TSS2_RC rc = TSS2_RC_SUCCESS;
    ssize_t size = 0;
    struct pollfd fds;
    int rc_poll, nfds = 1;
    uint8_t header[TPM_HEADER_SIZE];
    size_t offset = 2;
    UINT32 partial_size;

    rc = tcti_common_receive_checks (tcti_common,
                                     response_size,
                                     TCTI_DEVICE_MAGIC);
    if (rc != TSS2_RC_SUCCESS) {
        return rc;
    }

    if (!response_buffer) {
        if (!tcti_common->partial_read_supported) {
            LOG_DEBUG("Partial read not supported ");
            *response_size = 4096;
            return TSS2_RC_SUCCESS;
        } else {
            /* Read the header only and get the response size out of it */
            LOG_DEBUG("Partial read - reading response size");
            fds.fd = tcti_dev->fd;
            fds.events = POLLIN;

            rc_poll = poll(&fds, nfds, timeout);
            if (rc_poll < 0) {
                LOG_ERROR ("Failed to poll for response from fd %d, got errno %d: %s",
               tcti_dev->fd, errno, strerror(errno));
                return TSS2_TCTI_RC_IO_ERROR;
            } else if (rc_poll == 0) {
                LOG_INFO ("Poll timed out on fd %d.", tcti_dev->fd);
                return TSS2_TCTI_RC_TRY_AGAIN;
            } else if (fds.revents == POLLIN) {
                TEMP_RETRY (size, read (tcti_dev->fd, header, TPM_HEADER_SIZE));
                if (size < 0 || size != TPM_HEADER_SIZE) {
                    LOG_ERROR ("Failed to get response size fd %d, got errno %d: %s",
                           tcti_dev->fd, errno, strerror (errno));
                    return TSS2_TCTI_RC_IO_ERROR;
                }
            }
            LOG_DEBUG("Partial read - received header");
            rc = Tss2_MU_UINT32_Unmarshal(header, TPM_HEADER_SIZE,
                                          &offset, &partial_size);
            if (rc != TSS2_RC_SUCCESS) {
                LOG_ERROR ("Failed to unmarshal response size.");
                return rc;
            }
            if (partial_size < TPM_HEADER_SIZE) {
                LOG_ERROR ("Received %zu bytes, not enough to hold a TPM2"
               " response header.", size);
                return TSS2_TCTI_RC_GENERAL_FAILURE;
            }

            LOG_DEBUG("Partial read - received response size %d.", partial_size);
            tcti_common->partial = true;
            *response_size = partial_size;
            memcpy(&tcti_common->header, header, TPM_HEADER_SIZE);
            return rc;
        }
    }

    /* In case when the whole response is just the 10 bytes header
     * and we have read it already to get the size, we don't need
     * to call poll and read again. Just copy what we have read
     * and return.
     */
    if (tcti_common->partial == true && *response_size == TPM_HEADER_SIZE) {
        memcpy(response_buffer, &tcti_common->header, TPM_HEADER_SIZE);
        tcti_common->partial = false;
        goto out;
    }

    /*
     * The older kernel driver will only return a response buffer in a single
     * read operation. If we try to read again before sending another command
     * the kernel will close the file descriptor and we'll get an EOF.
     * Newer kernels should have partial reads enabled.
     */
    fds.fd = tcti_dev->fd;
    fds.events = POLLIN;

    rc_poll = poll(&fds, nfds, timeout);
    if (rc_poll < 0) {
        LOG_ERROR ("Failed to poll for response from fd %d, got errno %d: %s",
                   tcti_dev->fd, errno, strerror (errno));
        return TSS2_TCTI_RC_IO_ERROR;
    } else if (rc_poll == 0) {
        LOG_INFO ("Poll timed out on fd %d.", tcti_dev->fd);
        return TSS2_TCTI_RC_TRY_AGAIN;
    } else if (fds.revents == POLLIN) {
        if (tcti_common->partial == true) {
            memcpy(response_buffer, &tcti_common->header, TPM_HEADER_SIZE);
            TEMP_RETRY (size, read (tcti_dev->fd, response_buffer +
                        TPM_HEADER_SIZE, *response_size - TPM_HEADER_SIZE));
        } else {
            TEMP_RETRY (size, read (tcti_dev->fd, response_buffer,
                                    *response_size));
        }
        if (size < 0) {
            LOG_ERROR ("Failed to read response from fd %d, got errno %d: %s",
               tcti_dev->fd, errno, strerror (errno));
            return TSS2_TCTI_RC_IO_ERROR;
        }
    }
    if (size == 0) {
        LOG_WARNING ("Got EOF instead of response.");
        rc = TSS2_TCTI_RC_NO_CONNECTION;
        goto out;
    }

    size += tcti_common->partial ? TPM_HEADER_SIZE : 0;
    LOGBLOB_DEBUG(response_buffer, size, "Response Received");
    tcti_common->partial = false;

    if ((size_t)size < TPM_HEADER_SIZE) {
        LOG_ERROR ("Received %zu bytes, not enough to hold a TPM2 response "
                   "header.", size);
        rc = TSS2_TCTI_RC_GENERAL_FAILURE;
        goto out;
    }

    rc = header_unmarshal (response_buffer, &tcti_common->header);
    if (rc != TSS2_RC_SUCCESS)
        goto out;

    LOG_DEBUG("Size from header %u bytes read %zu", tcti_common->header.size, size);

    if ((size_t)size != tcti_common->header.size) {
        LOG_WARNING ("TPM2 response size disagrees with number of bytes read "
                     "from fd %d. Header says %u but we read %zu bytes.",
                     tcti_dev->fd, tcti_common->header.size, size);
    }
    if (*response_size < tcti_common->header.size) {
        LOG_WARNING ("TPM2 response size is larger than the provided "
                     "buffer: future use of this TCTI will likely fail.");
        rc = TSS2_TCTI_RC_GENERAL_FAILURE;
    }
    *response_size = size;
    /*
     * Executing code beyond this point transitions the state machine to
     * TRANSMIT. Another call to this function will not be possible until
     * another command is sent to the TPM.
     */
out:
    tcti_common->state = TCTI_STATE_TRANSMIT;

    return rc;
}

static void close_tpm(int *fd)
{
    if (fd == NULL || *fd < 0) {
        return;
    }

    close(*fd);
    *fd = -1;
}

void
tcti_device_finalize (
    TSS2_TCTI_CONTEXT *tctiContext)
{
    TSS2_TCTI_DEVICE_CONTEXT *tcti_dev = tcti_device_context_cast (tctiContext);
    TSS2_TCTI_COMMON_CONTEXT *tcti_common = tcti_device_down_cast (tcti_dev);

    if (tcti_dev == NULL) {
        return;
    }
    close_tpm (&tcti_dev->fd);
    tcti_common->state = TCTI_STATE_FINAL;
}

TSS2_RC
tcti_device_cancel (
    TSS2_TCTI_CONTEXT *tctiContext)
{
    /* Linux driver doesn't expose a mechanism to cancel commands. */
    UNUSED(tctiContext);
    return TSS2_TCTI_RC_NOT_IMPLEMENTED;
}

TSS2_RC
tcti_device_get_poll_handles (
    TSS2_TCTI_CONTEXT *tctiContext,
    TSS2_TCTI_POLL_HANDLE *handles,
    size_t *num_handles)
{
    TSS2_TCTI_DEVICE_CONTEXT *tcti_dev = tcti_device_context_cast (tctiContext);

    if (num_handles == NULL || tcti_dev == NULL) {
        return TSS2_TCTI_RC_BAD_REFERENCE;
    }

    if (handles != NULL && *num_handles < 1) {
        return TSS2_TCTI_RC_INSUFFICIENT_BUFFER;
    }

    *num_handles = 1;
    if (handles != NULL) {
        handles->fd = tcti_dev->fd;
        handles->events = POLLIN | POLLOUT;
    }

    return TSS2_RC_SUCCESS;
}

TSS2_RC
tcti_device_set_locality (
    TSS2_TCTI_CONTEXT *tctiContext,
    uint8_t locality)
{
    /*
     * Linux driver doesn't expose a mechanism for user space applications
     * to set locality.
     */
    UNUSED(tctiContext);
    UNUSED(locality);
    return TSS2_TCTI_RC_NOT_IMPLEMENTED;
}

static int open_tpm (
    const char* pathname) {
#ifdef __VXWORKS__
        return open (pathname, O_RDWR | O_NONBLOCK, (S_IRUSR | S_IWUSR | S_IRGRP | S_IWGRP));
#else
        return open (pathname, O_RDWR | O_NONBLOCK);
#endif
}

TSS2_RC
Tss2_Tcti_Device_Init (
    TSS2_TCTI_CONTEXT *tctiContext,
    size_t *size,
    const char *conf)
{
    TSS2_TCTI_DEVICE_CONTEXT *tcti_dev;
    TSS2_TCTI_COMMON_CONTEXT *tcti_common;
    char *used_conf = NULL;

    if (tctiContext == NULL && size == NULL) {
        return TSS2_TCTI_RC_BAD_VALUE;
    } else if (tctiContext == NULL) {
        *size = sizeof (TSS2_TCTI_DEVICE_CONTEXT);
        return TSS2_RC_SUCCESS;
    }

    /* Init TCTI context */
    TSS2_TCTI_MAGIC (tctiContext) = TCTI_DEVICE_MAGIC;
    TSS2_TCTI_VERSION (tctiContext) = TCTI_VERSION;
    TSS2_TCTI_TRANSMIT (tctiContext) = tcti_device_transmit;
    TSS2_TCTI_RECEIVE (tctiContext) = tcti_device_receive;
    TSS2_TCTI_FINALIZE (tctiContext) = tcti_device_finalize;
    TSS2_TCTI_CANCEL (tctiContext) = tcti_device_cancel;
    TSS2_TCTI_GET_POLL_HANDLES (tctiContext) = tcti_device_get_poll_handles;
    TSS2_TCTI_SET_LOCALITY (tctiContext) = tcti_device_set_locality;
    TSS2_TCTI_MAKE_STICKY (tctiContext) = tcti_make_sticky_not_implemented;
    tcti_dev = tcti_device_context_cast (tctiContext);
    tcti_common = tcti_device_down_cast (tcti_dev);
    tcti_common->state = TCTI_STATE_TRANSMIT;
    memset (&tcti_common->header, 0, sizeof (tcti_common->header));
    tcti_common->locality = 3;
    tcti_common->partial = false;

    if (conf == NULL) {
        LOG_TRACE ("No TCTI device file specified");

        for (size_t i = 0; i < ARRAY_LEN(default_conf); i++) {
            LOG_DEBUG ("Trying to open default TCTI device file %s",
                       default_conf[i]);
            tcti_dev->fd = open_tpm (default_conf[i]);
            if (tcti_dev->fd >= 0) {
                LOG_TRACE ("Successfully opened default TCTI device file %s",
                           default_conf[i]);
                    used_conf = default_conf[i];
                    break;
            } else {
                LOG_WARNING ("Failed to open default TCTI device file %s: %s",
                             default_conf[i], strerror (errno));
            }
        }
        if (tcti_dev->fd < 0) {
            LOG_ERROR ("Could not open any default TCTI device file");
            return TSS2_TCTI_RC_IO_ERROR;
        }
    } else {
        LOG_DEBUG ("Trying to open specified TCTI device file %s", conf);
        tcti_dev->fd = open_tpm (conf);
        if (tcti_dev->fd < 0) {
            LOG_ERROR ("Failed to open specified TCTI device file %s: %s",
                       conf, strerror (errno));
            return TSS2_TCTI_RC_IO_ERROR;
        } else {
            LOG_TRACE ("Successfully opened specified TCTI device file %s", conf);
        }
        used_conf = (char *)conf;
    }
    /* probe if the device support partial response read */
    LOG_DEBUG ("Probe device for partial response read support");
    uint8_t cmd[12] = { "\x80\x01\x00\x00\x00\x0c\x00\x00\x01\x7b\x00\x08" };
    uint8_t rsp[20] = {0};
    struct pollfd fds;
    int rc_poll, nfds = 1;

    ssize_t sz = write_all (tcti_dev->fd, cmd, sizeof(cmd));
    if (sz < 0 || sz != sizeof(cmd)) {
        LOG_ERROR ("Could not probe device for partial response read support");
        close_tpm (&tcti_dev->fd);
        return TSS2_TCTI_RC_IO_ERROR;
    }
    LOG_DEBUG ("Command sent, reading header");

    fds.fd = tcti_dev->fd;
    fds.events = POLLIN;
    rc_poll = poll(&fds, nfds, 1000); /* Wait 1 sec */
    if (rc_poll < 0 || rc_poll == 0) {
        LOG_ERROR ("Failed to poll for response from fd %d, rc %d, errno %d: %s",
                   tcti_dev->fd, rc_poll, errno, strerror(errno));
        close_tpm (&tcti_dev->fd);
        return TSS2_TCTI_RC_IO_ERROR;
    } else if (fds.revents == POLLIN) {
        TEMP_RETRY (sz, read (tcti_dev->fd, rsp, TPM_HEADER_SIZE));
        if (sz < 0 || sz != TPM_HEADER_SIZE) {
            LOG_ERROR ("Failed to read response header fd %d, got errno %d: %s",
                       tcti_dev->fd, errno, strerror (errno));
            close_tpm (&tcti_dev->fd);
            return TSS2_TCTI_RC_IO_ERROR;
        }
    }
    LOG_DEBUG ("Header read, reading rest of response");
    fds.fd = tcti_dev->fd;
    fds.events = POLLIN;
    sz = 0;
    rc_poll = poll(&fds, nfds, 1000); /* Wait 1 sec */
    if (rc_poll < 0) {
        LOG_DEBUG ("Failed to poll for response from fd %d, rc %d, errno %d: %s",
                   tcti_dev->fd, rc_poll, errno, strerror(errno));
        close_tpm (&tcti_dev->fd);
        return TSS2_TCTI_RC_IO_ERROR;
	} else if (rc_poll == 0) {
        LOG_ERROR ("timeout waiting for response from fd %d", tcti_dev->fd);
    } else if (fds.revents == POLLIN) {
        TEMP_RETRY (sz, read (tcti_dev->fd, rsp + TPM_HEADER_SIZE,
                    sizeof(rsp) - TPM_HEADER_SIZE));
    }

    if (sz <= 0) {
        /* partial read not supported. Reset the connection */
        LOG_DEBUG ("Failed to get response tail fd %d, got errno %d: %s",
                   tcti_dev->fd, errno, strerror (errno));
        tcti_common->partial_read_supported = 0;
        close_tpm (&tcti_dev->fd);
        tcti_dev->fd = open_tpm (used_conf);
        if (tcti_dev->fd < 0) {
            LOG_ERROR ("Failed to open specified TCTI device file %s: %s",
                       used_conf, strerror (errno));
            return TSS2_TCTI_RC_IO_ERROR;
        }
    } else {
        /* partial read supported. */
        LOG_DEBUG ("Read the rest - partial read supported");
        tcti_common->partial_read_supported = 1;
    }

    return TSS2_RC_SUCCESS;
}

const TSS2_TCTI_INFO tss2_tcti_info = {
    .version = TCTI_VERSION,
    .name = "tcti-device",
    .description = "TCTI module for communication with Linux kernel interface.",
    .config_help = "Path to TPM character device. Default value is: "
        "TCTI_DEVICE_DEFAULT",
    .init = Tss2_Tcti_Device_Init,
};

const TSS2_TCTI_INFO*
Tss2_Tcti_Info (void)
{
    return &tss2_tcti_info;
}
