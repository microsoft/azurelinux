/* SPDX-License-Identifier: BSD-2-Clause */
/***********************************************************************;
 * Copyright (c) 2015 - 2018, Intel Corporation
 * All rights reserved.
 ***********************************************************************/

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <inttypes.h>
#include <limits.h>
#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include <setjmp.h>
#include <cmocka.h>

#include "tss2_tcti.h"
#include "tss2_tcti_swtpm.h"

#include "tss2-tcti/tcti-common.h"
#include "tss2-tcti/tcti-swtpm.h"
#include "util/key-value-parse.h"

/*
 * This function is defined in the tcti-swtpm module but not exposed through
 * the header.
 */
TSS2_RC
swtpm_kv_callback (const key_value_t *key_value,
                   void *user_data);

/*
 * In the tests below where 'host' is set (implying TCP and excluding unix domain
 * sockets), we ensure that 'path' comes back NULL. Similarly, when 'path' is
 * set (implying unix domain sockets), we ensure that 'host' is NULL.
 */
#define NO_HOST_VALUE "no.host.xyz"
#define NO_PORT_VALUE 646
#define NO_PATH_VALUE "/bad/path"

/*
 * This tests our ability to handle conf strings that have a port component. In
 * this case the 'conf_str_to_host_port' function should set the 'host' and
 * 'port' parameters and so we check to be sure they're set. (And that 'path'
 * is unset.)
 */
static void
conf_str_to_host_port_success_test (void **state)
{
    TSS2_RC rc;
    char conf[] = "host=127.0.0.1,port=2321";
    char unusedpath[] = NO_PATH_VALUE;
    swtpm_conf_t swtpm_conf = {
        .path = unusedpath
    };

    rc = parse_key_value_string (conf, swtpm_kv_callback, &swtpm_conf);
    assert_int_equal (rc, TSS2_RC_SUCCESS);
    assert_int_equal (swtpm_conf.port, 2321);
    assert_string_equal (swtpm_conf.host, "127.0.0.1");
    assert_null (swtpm_conf.path);
}

/*
 * This tests our ability to handle conf strings that don't have the port
 * component of the URI. In this case the 'conf_str_to_host_port' function
 * should not touch the 'port' parameter and so we check to be sure it's
 * unchanged. (And that 'path' is unset.)
 */
static void
conf_str_to_host_port_no_port_test (void **state)
{
    TSS2_RC rc;
    char conf[] = "host=127.0.0.1";
    char unusedpath[] = NO_PATH_VALUE;
    swtpm_conf_t swtpm_conf = {
        .host = "foo",
        .port = NO_PORT_VALUE,
        .path = unusedpath
    };

    rc = parse_key_value_string (conf, swtpm_kv_callback, &swtpm_conf);
    assert_int_equal (rc, TSS2_RC_SUCCESS);
    assert_string_equal (swtpm_conf.host, "127.0.0.1");
    assert_int_equal (swtpm_conf.port, NO_PORT_VALUE);
    assert_null (swtpm_conf.path);
}

/*
 * This tests our ability to handle conf strings that have an IPv6 address
 * and port component. In this case the 'conf_str_to_host_port' function
 * should set the 'hostname' parameter and so we check to be sure it's
 * set without the [] brackets. (And that 'path' is unset.)
 */
static void
conf_str_to_host_ipv6_port_success_test (void **state)
{
    TSS2_RC rc;
    char conf[] = "host=::1,port=2321";
    char unusedpath[] = NO_PATH_VALUE;
    swtpm_conf_t swtpm_conf = {
        .path = unusedpath
    };

    rc = parse_key_value_string (conf, swtpm_kv_callback, &swtpm_conf);
    assert_int_equal (rc, TSS2_RC_SUCCESS);
    assert_int_equal (swtpm_conf.port, 2321);
    assert_string_equal (swtpm_conf.host, "::1");
    assert_null (swtpm_conf.path);
}

/*
 * This tests our ability to handle conf strings that have an IPv6 address
 * but no port component. In this case the 'conf_str_to_host_port' function
 * should not touch the 'port' parameter and so we check to be sure it's
 * unchanged. (And that 'path' is unset.)
 */
static void
conf_str_to_host_ipv6_port_no_port_test (void **state)
{
    TSS2_RC rc;
    char conf[] = "host=::1";
    swtpm_conf_t swtpm_conf = {
        .port = NO_PORT_VALUE,
        .path = NO_PATH_VALUE
    };

    rc = parse_key_value_string (conf, swtpm_kv_callback, &swtpm_conf);
    assert_int_equal (rc, TSS2_RC_SUCCESS);
    assert_int_equal (swtpm_conf.port, NO_PORT_VALUE);
    assert_string_equal (swtpm_conf.host, "::1");
    assert_null (swtpm_conf.path);
}

/*
 * The 'conf_str_to_host_port' function rejects ports over UINT16_MAX.
 */
static void
conf_str_to_host_port_invalid_port_large_test (void **state)
{
    TSS2_RC rc;
    char conf[] = "host=127.0.0.1,port=99999";
    swtpm_conf_t swtpm_conf = { 0 };

    rc = parse_key_value_string (conf, swtpm_kv_callback, &swtpm_conf);
    assert_int_equal (rc, TSS2_TCTI_RC_BAD_VALUE);
}
/* The 'conf_str_to_host_port' function rejects URIs with port == 0 */
static void
conf_str_to_host_port_invalid_port_0_test (void **state)
{
    TSS2_RC rc;
    char conf[] = "host=127.0.0.1,port=0";
    swtpm_conf_t swtpm_conf = { 0 };

    rc = parse_key_value_string (conf, swtpm_kv_callback, &swtpm_conf);
    assert_int_equal (rc, TSS2_TCTI_RC_BAD_VALUE);
}

/*
 * This tests our ability to handle conf strings that have a path
 * component. In this case the 'conf_str_to_host_port' function
 * should set the 'path' parameter and so we check to be sure it's
 * set. (And that 'host' is unset.)
 */
static void
conf_str_to_path_success_test (void **state)
{
    TSS2_RC rc;
    char conf[] = "path=/some/path";
    char unusedhost[] = NO_HOST_VALUE;
    swtpm_conf_t swtpm_conf = {
        .host = unusedhost
    };

    rc = parse_key_value_string (conf, swtpm_kv_callback, &swtpm_conf);
    assert_int_equal (rc, TSS2_RC_SUCCESS);
    assert_string_equal (swtpm_conf.path, "/some/path");
    assert_null (swtpm_conf.host);
}

/* When passed all NULL values ensure that we get back the expected RC. */
static void
tcti_swtpm_init_all_null_test (void **state)
{
    TSS2_RC rc;

    rc = Tss2_Tcti_Swtpm_Init (NULL, NULL, NULL);
    assert_int_equal (rc, TSS2_TCTI_RC_BAD_VALUE);
}
/*
 * Determine the size of a TCTI context structure. Requires calling the
 * initialization function for the device TCTI with the first parameter
 * (the TCTI context) NULL.
 */
static void
tcti_swtpm_init_size_test (void **state)
{
    size_t tcti_size = 0;
    TSS2_RC ret = TSS2_RC_SUCCESS;

    ret = Tss2_Tcti_Swtpm_Init (NULL, &tcti_size, NULL);
    assert_int_equal (ret, TSS2_RC_SUCCESS);
    assert_int_equal (tcti_size, sizeof (TSS2_TCTI_SWTPM_CONTEXT));
}
/*
 * Wrap the 'connect' system call. The mock queue for this function must have
 * an integer to return as a response.
 */
int
__wrap_connect (int                    sockfd,
                const struct sockaddr *addr,
                socklen_t              addrlen)
{
    return mock_type (int);
}
/*
 * Wrap the 'recv' system call. The mock queue for this function must have an
 * integer return value (the number of byts recv'd), as well as a pointer to
 * a buffer to copy data from to return to the caller.
 */
ssize_t
__wrap_read (int sockfd,
             void *buf,
             size_t len)
{
    ssize_t  ret = mock_type (ssize_t);
    uint8_t *buf_in = mock_ptr_type (uint8_t*);

    memcpy (buf, buf_in, ret);
    return ret;
}
/*
 * Wrap the 'send' system call. The mock queue for this function must have an
 * integer to return as a response.
 */
ssize_t
__wrap_write (int sockfd,
              const void *buf,
              size_t len)

{
    return mock_type (TSS2_RC);
}
/*
 * This is a utility function used by other tests to setup a TCTI context. It
 * effectively wraps the init / allocate / init pattern as well as priming the
 * mock functions necessary for a the successful call to
 * 'Tss2_Tcti_Swtpm_Init'.
 */
static TSS2_TCTI_CONTEXT*
tcti_swtpm_init_from_conf (const char *conf)
{
    size_t tcti_size = 0;
    uint8_t recv_buf[4] = { 0 };
    TSS2_RC ret = TSS2_RC_SUCCESS;
    TSS2_TCTI_CONTEXT *ctx = NULL;

    printf ("%s: before first init\n", __func__);
    ret = Tss2_Tcti_Swtpm_Init (NULL, &tcti_size, NULL);
    assert_true (ret == TSS2_RC_SUCCESS);
    ctx = calloc (1, tcti_size);
    assert_non_null (ctx);
    /*
     * two calls to connect, one for the data socket, one for the command
     * socket
     */
    will_return (__wrap_connect, 0);
    will_return (__wrap_connect, 0);
    /*
     * one control command is sent on init (5 byte write, 4 byte read)
     */
    will_return (__wrap_write, 5);
    will_return (__wrap_read, 4);
    will_return (__wrap_read, recv_buf);
    printf ("%s: before second_init\n", __func__);
    ret = Tss2_Tcti_Swtpm_Init (ctx, &tcti_size, conf);
    printf ("%s: after second init\n", __func__);
    assert_int_equal (ret, TSS2_RC_SUCCESS);
    return ctx;
}

/*
 * This is a utility function to setup the "default" TCTI context.
 */
static int
tcti_swtpm_setup (void **state)
{
    printf ("%s: before tcti_swtpm_init_from_conf\n", __func__);
    *state = tcti_swtpm_init_from_conf ("host=127.0.0.1,port=666");
    printf ("%s: done\n", __func__);
    return 0;
}
#ifndef _WIN32
/* variant of tcti_swtpm_setup() for unix domain sockets. */
static int
tcti_swtpm_setup_unix (void **state)
{
    printf ("%s: before tcti_swtpm_init_from_conf\n", __func__);
    *state = tcti_swtpm_init_from_conf ("path=/notarealdirectory/notarealfile");
    printf ("%s: done\n", __func__);
    return 0;
}
#endif
static void
tcti_swtpm_init_null_conf_test (void **state)
{
    TSS2_TCTI_CONTEXT *ctx = tcti_swtpm_init_from_conf (NULL);
    assert_non_null (ctx);
    free (ctx);
}
/*
 * This test excersises the Tss2_Tcti_Info function
 */
const TSS2_TCTI_INFO *Tss2_Tcti_Info (void);
static void
tcti_swtpm_get_info_test (void **state)
{
    const TSS2_TCTI_INFO *info;

    info = Tss2_Tcti_Info ();
    assert_string_equal (info->name, "tcti-swtpm");
    assert_int_equal (info->init, &Tss2_Tcti_Swtpm_Init);
}
/*
 * This is a utility function to teardown a TCTI context allocated by the
 * tcti_swtpm_setup function.
 */
static int
tcti_swtpm_teardown (void **state)
{
    TSS2_TCTI_CONTEXT *ctx = (TSS2_TCTI_CONTEXT*)*state;

    Tss2_Tcti_Finalize (ctx);
    free (ctx);
    return 0;
}
/*
 * This test exercised a failed connect check in the Tss2_Tcti_Swtpm_Init function
 */
static void
tcti_swtpm_init_fail_connect_test (void **state)
{
    size_t tcti_size = 0;
    TSS2_RC ret = TSS2_RC_SUCCESS;
    TSS2_TCTI_CONTEXT *ctx = NULL;

    /* get tcti size */
    ret = Tss2_Tcti_Swtpm_Init (NULL, &tcti_size, NULL);
    assert_true (ret == TSS2_RC_SUCCESS);
    ctx = calloc (1, tcti_size);
    assert_non_null (ctx);

    /* first connect fails */
    will_return (__wrap_connect, -1);
    ret = Tss2_Tcti_Swtpm_Init (ctx, &tcti_size, "host=127.0.0.1,port=666");
    assert_int_equal (ret, TSS2_TCTI_RC_IO_ERROR);

    /* second connect fails */
    will_return (__wrap_connect, 0);
    will_return (__wrap_connect, -1);
    ret = Tss2_Tcti_Swtpm_Init (ctx, &tcti_size, "host=127.0.0.1,port=666");
    assert_int_equal (ret, TSS2_TCTI_RC_IO_ERROR);

    free(((TSS2_TCTI_SWTPM_CONTEXT*)ctx)->conf_copy);
    free(ctx);
}
/*
 * This test ensures that the GetPollHandles function in the device TCTI
 * returns the expected value. Since this TCTI does not support async I/O
 * on account of limitations in the kernel it just returns the
 * NOT_IMPLEMENTED response code.
 */
static void
tcti_swtpm_get_poll_handles_test (void **state)
{
    TSS2_TCTI_CONTEXT *ctx = (TSS2_TCTI_CONTEXT*)*state;
    size_t num_handles = 5;
    TSS2_TCTI_POLL_HANDLE handles [5] = { 0 };
    TSS2_RC rc;

    rc = Tss2_Tcti_GetPollHandles (ctx, handles, &num_handles);
    assert_int_equal (rc, TSS2_TCTI_RC_NOT_IMPLEMENTED);
}
/*
 * This test exercises the null check of tcti_swtpm_receive ()
 */
static void
tcti_swtpm_receive_null_test (void **state)
{
    TSS2_RC rc;

    rc = Tss2_Tcti_Receive (NULL, NULL, NULL, TSS2_TCTI_TIMEOUT_BLOCK);
    assert_int_equal (rc, TSS2_TCTI_RC_BAD_REFERENCE);
}
/*
 */
static void
tcti_swtpm_receive_null_size_test (void **state)
{
    TSS2_TCTI_CONTEXT *ctx = (TSS2_TCTI_CONTEXT*)*state;
    TSS2_TCTI_COMMON_CONTEXT *tcti_common = tcti_common_context_cast (ctx);
    TSS2_RC rc;

    /* Keep state machine check in `receive` from returning error. */
    tcti_common->state = TCTI_STATE_RECEIVE;
    rc = Tss2_Tcti_Receive (ctx,
                            NULL, /* NULL 'size' parameter */
                            NULL,
                            TSS2_TCTI_TIMEOUT_BLOCK);
    assert_int_equal (rc, TSS2_TCTI_RC_BAD_REFERENCE);
    rc = Tss2_Tcti_Receive (ctx,
                            NULL, /* NULL 'size' parameter */
                            (uint8_t*)1, /* non-NULL buffer */
                            TSS2_TCTI_TIMEOUT_BLOCK);
    assert_int_equal (rc, TSS2_TCTI_RC_BAD_REFERENCE);
}
/*
 * This test exercises the successful code path through the receive function.
 */
static void
tcti_swtpm_receive_success_test (void **state)
{
    TSS2_TCTI_CONTEXT *ctx = (TSS2_TCTI_CONTEXT*)*state;
    TSS2_TCTI_COMMON_CONTEXT *tcti_common = tcti_common_context_cast (ctx);
    TSS2_RC rc = TSS2_RC_SUCCESS;
    uint8_t response_in [] = { 0x80, 0x02,
                               0x00, 0x00, 0x00, 0x0c,
                               0x00, 0x00, 0x00, 0x00,
                               0x01, 0x02 };
    size_t response_size = sizeof(response_in);
    uint8_t response_out [12] = { 0 };

    /* Keep state machine check in `receive` from returning error. */
    tcti_common->state = TCTI_STATE_RECEIVE;
    /* receive response header */
    will_return (__wrap_read, 10);
    will_return (__wrap_read, response_in);
    /* receive remaining response */
    will_return (__wrap_read, response_size - 10);
    will_return (__wrap_read, &response_in [10]);

    rc = Tss2_Tcti_Receive (ctx, &response_size, response_out, TSS2_TCTI_TIMEOUT_BLOCK);
    assert_int_equal (rc, TSS2_RC_SUCCESS);
    assert_memory_equal (response_in, response_out, response_size);
}
/*
 */
static void
tcti_swtpm_receive_size_success_test (void **state)
{
    TSS2_TCTI_CONTEXT *ctx = (TSS2_TCTI_CONTEXT*)*state;
    TSS2_TCTI_COMMON_CONTEXT *tcti_common = tcti_common_context_cast (ctx);
    TSS2_RC rc = TSS2_RC_SUCCESS;
    size_t response_size = 0;
    uint8_t response_in [] = { 0x80, 0x02,
                               0x00, 0x00, 0x00, 0x0c,
                               0x00, 0x00, 0x00, 0x00,
                               0x01, 0x02 };
    uint8_t response_out [12] = { 0 };

    /* Keep state machine check in `receive` from returning error. */
    tcti_common->state = TCTI_STATE_RECEIVE;
    /* receive response header */
    will_return (__wrap_read, 10);
    will_return (__wrap_read, response_in);
    rc = Tss2_Tcti_Receive (ctx, &response_size, NULL, TSS2_TCTI_TIMEOUT_BLOCK);

    assert_int_equal (rc, TSS2_RC_SUCCESS);
    assert_int_equal (response_size, 0xc);

    /* receive remaining response */
    will_return (__wrap_read, response_size - 10);
    will_return (__wrap_read, &response_in [10]);

    rc = Tss2_Tcti_Receive (ctx, &response_size, response_out, TSS2_TCTI_TIMEOUT_BLOCK);
    assert_int_equal (rc, TSS2_RC_SUCCESS);
    assert_memory_equal (response_in, response_out, response_size);
}
/*
 * This test causes the underlying 'read' call to return 0 / EOF when we
 * call the TCTI 'receive' function. In this case the TCTI should return an
 * IO error.
 */
static void
tcti_swtpm_receive_eof_first_read_test (void **state)
{
    TSS2_TCTI_CONTEXT *ctx = (TSS2_TCTI_CONTEXT*)*state;
    TSS2_TCTI_COMMON_CONTEXT *tcti_common = tcti_common_context_cast (ctx);
    TSS2_RC rc;
    /* output buffer for response */
    uint8_t buf [TPM_HEADER_SIZE] = { 0 };
    size_t size = sizeof (buf);

    /* Keep state machine check in `receive` from returning error. */
    tcti_common->state = TCTI_STATE_RECEIVE;
    will_return (__wrap_read, 0);
    will_return (__wrap_read, buf);
    rc = Tss2_Tcti_Receive (ctx,
                            &size,
                            buf,
                            TSS2_TCTI_TIMEOUT_BLOCK);
    assert_true (rc == TSS2_TCTI_RC_IO_ERROR);
}
/*
 * This test causes the underlying 'read' call to return EOF but only after
 * a successful read that gets us the response size. This results in the
 * an IO_ERROR RC being returned.
 */
static void
tcti_swtpm_receive_eof_second_read_test (void **state)
{
    TSS2_TCTI_CONTEXT *ctx = (TSS2_TCTI_CONTEXT*)*state;
    TSS2_TCTI_COMMON_CONTEXT *tcti_common = tcti_common_context_cast (ctx);
    TSS2_RC rc;
    /* input response buffer */
    uint8_t response_in [] = { 0x80, 0x02,
                               0x00, 0x00, 0x00, 0x0c,
                               0x00, 0x00, 0x00, 0x00,
                               0x01, 0x02,
    /* simulator appends 4 bytes of 0's to every response */
                               0x00, 0x00, 0x00, 0x00 };
    /* output response buffer */
    uint8_t response_out [12] = { 0 };
    size_t size = sizeof (response_out);

    /* Keep state machine check in `receive` from returning error. */
    tcti_common->state = TCTI_STATE_RECEIVE;
    /* setup response size for first read */
    will_return (__wrap_read, 4);
    will_return (__wrap_read, &response_in [2]);
    /* setup 0 for EOF on second read */
    will_return (__wrap_read, 0);
    will_return (__wrap_read, response_in);
    rc = Tss2_Tcti_Receive (ctx,
                            &size,
                            response_out,
                            TSS2_TCTI_TIMEOUT_BLOCK);
    assert_true (rc == TSS2_TCTI_RC_IO_ERROR);
}
/*
 * This test exercises the (fake) timeout mechanism of the receive function.
 */
static void
tcti_swtpm_receive_timeout_try_again_test (void **state)
{
#ifdef TEST_FAPI_ASYNC
    TSS2_TCTI_CONTEXT *ctx = (TSS2_TCTI_CONTEXT*)*state;
    TSS2_TCTI_COMMON_CONTEXT *tcti_common = tcti_common_context_cast (ctx);
    TSS2_RC rc = TSS2_RC_SUCCESS;

    /* Keep state machine check in `receive` from returning error. */
    tcti_common->state = TCTI_STATE_RECEIVE;

    rc = Tss2_Tcti_Receive (ctx, (size_t*) 1, NULL, TSS2_TCTI_TIMEOUT_NONE);
    assert_int_equal (rc, TSS2_TCTI_RC_TRY_AGAIN);
#endif /* TEST_FAPI_ASYNC */
}
/*
 * This test exercises the successful code path through the transmit function.
 */
static void
tcti_swtpm_transmit_success_test (void **state)
{
    TSS2_TCTI_CONTEXT *ctx = (TSS2_TCTI_CONTEXT*)*state;
    TSS2_RC rc = TSS2_RC_SUCCESS;
    uint8_t command [] = { 0x80, 0x02,
                           0x00, 0x00, 0x00, 0x0c,
                           0x00, 0x00, 0x00, 0x00,
                           0x01, 0x02 };
    size_t  command_size = sizeof (command);

    /* connect to tpm_sock */
    will_return (__wrap_connect, 0);
    /* send the command buffer */
    will_return (__wrap_write, 0xc);
    rc = Tss2_Tcti_Transmit (ctx, command_size, command);
    assert_int_equal (rc, TSS2_RC_SUCCESS);
}
/*
 * This test exercises the NULL checks of the transmit function.
 */
static void
tcti_swtpm_transmit_null_test (void **state)
{
    TSS2_RC rc = TSS2_RC_SUCCESS;

    rc = Tss2_Tcti_Transmit (NULL, 0, NULL);
    assert_int_equal (rc, TSS2_TCTI_RC_BAD_REFERENCE);
}
/*
 * This test exercises the header check of the transmit function.
 * Also it exercises a marshaling failure check.
 */
static void
tcti_swtpm_transmit_fail_header_test (void **state)
{
    TSS2_TCTI_CONTEXT *ctx = (TSS2_TCTI_CONTEXT*)*state;
    TSS2_RC rc = TSS2_RC_SUCCESS;
    uint8_t command [] = { 0x80, 0x02,
                           0x00, 0x00, 0x00, 0xFF,
                           0x00, 0x00, 0x00, 0x00,
                           0x01, 0x02 };
    size_t  command_size = sizeof (command);

    rc = Tss2_Tcti_Transmit (ctx, command_size, command);
    assert_int_equal (rc, TSS2_TCTI_RC_BAD_VALUE);

    rc = Tss2_Tcti_Transmit (ctx, 0, command);
    assert_int_equal (rc, TSS2_TCTI_RC_BAD_VALUE);
}
/*
 * This test exercises the successful code path through the tcti_control_command
 * function
 */
TSS2_RC tcti_control_command (
    TSS2_TCTI_CONTEXT *tctiContext,
    uint32_t cmd_code, const void *cmd_sdu, size_t cmd_sdu_len,
    uint32_t *resp_code, void *resp_sdu, size_t *resp_sdu_len);
static void
tcti_swtpm_control_command_success_test (void **state)
{
    TSS2_TCTI_CONTEXT *ctx = (TSS2_TCTI_CONTEXT*)*state;
    TSS2_RC rc = TSS2_RC_SUCCESS;
    const uint32_t CMD_SET_BUFFERSIZE = 0x11;
    uint32_t buffersize_in = 0;
    uint8_t response[] = {0x00, 0x00, 0x00, 0x00,
                          0x00, 0x00, 0x10, 0x00,
                          0x00, 0x00, 0x0A, 0x2A,
                          0x00, 0x00, 0x10, 0x00};
    uint32_t respcode_out = 0;
    size_t payload_len_out_expected = sizeof(response) - sizeof(respcode_out);
    uint8_t payload_out[payload_len_out_expected];
    size_t payload_len_out;

    /*
     * Here we send the command CMD_SET_BUFFERSIZE.
     * Request
     *      00 00 00 11     (command code CMD_SET_BUFFERSIZE)
     *      00 00 00 00     (buffersize 0 -> do not set but query buffersize)
     * Response
     *      00 00 00 00     (response code success)
     *      00 00 10 00     (payload, buffersize)
     *      00 00 0A 2A     (payload, minsize)
     *      00 00 10 00     (payload, maxsize)
     */

    will_return (__wrap_connect, 0);
    will_return (__wrap_write, 8);
    will_return (__wrap_read, 16);
    will_return (__wrap_read, response);
    rc = tcti_control_command (ctx, CMD_SET_BUFFERSIZE, &buffersize_in,
                               sizeof(buffersize_in), &respcode_out,
                               payload_out, &payload_len_out);
    assert_int_equal (rc, TSS2_RC_SUCCESS);
    assert_int_equal (respcode_out, 0);
    assert_int_equal (payload_len_out, payload_len_out_expected);
    assert_int_equal (memcmp(payload_out,
                             response + sizeof(respcode_out),
                             payload_len_out),
                      0);
}
/*
 * This test exercises the NULL checks for tctiContext and resp_sdu_len
 */
static void
tcti_swtpm_control_command_null_test (void **state)
{
    TSS2_TCTI_CONTEXT *ctx = (TSS2_TCTI_CONTEXT*)*state;
    TSS2_RC rc;

    /* tcti context NULL */
    rc = tcti_control_command (NULL, 0, NULL, 0, NULL, NULL, NULL);
    assert_int_equal (rc, TSS2_TCTI_RC_BAD_REFERENCE);

    /* cmd_sdu NULL with cmd_sdu_len not 0 */
    rc = tcti_control_command (ctx, 0, NULL, 4, NULL, NULL, NULL);
    assert_int_equal (rc, TSS2_TCTI_RC_BAD_VALUE);
}
/*
 * This test exercises a failed receive for the two cases
 *  - too few bytes received
 *  - response code not success
 */
static void
tcti_swtpm_control_command_recv_fail_test (void **state)
{
    TSS2_TCTI_CONTEXT *ctx = (TSS2_TCTI_CONTEXT*)*state;
    TSS2_RC rc = TSS2_RC_SUCCESS;
    const uint32_t CMD_CANCEL_TPM_CMD = 0x09;
    uint32_t response = 0xFFFFFFFF;
    uint32_t respcode_out = 0;

    will_return (__wrap_connect, 0);
    will_return (__wrap_write, 8);
    will_return (__wrap_read, 0);
    will_return (__wrap_read, response);
    rc = tcti_control_command (ctx, CMD_CANCEL_TPM_CMD, NULL, 0, &respcode_out,
                               NULL, NULL);
    assert_int_equal (rc, TSS2_TCTI_RC_IO_ERROR);

    will_return (__wrap_connect, 0);
    will_return (__wrap_write, 8);
    will_return (__wrap_read, 4);
    will_return (__wrap_read, (uint8_t *) &response);
    rc = tcti_control_command (ctx, CMD_CANCEL_TPM_CMD, NULL, 0, &respcode_out,
                               NULL, NULL);
    assert_int_equal (rc, TSS2_TCTI_RC_IO_ERROR);
    assert_int_equal (respcode_out, response);
}
/*
 * This test checks the return code of tcti_swtpm_cancel
 */
static void
tcti_swtpm_cancel_test (void **state)
{
    TSS2_TCTI_CONTEXT *ctx = (TSS2_TCTI_CONTEXT*)*state;
    TSS2_RC rc = TSS2_RC_SUCCESS;

    rc = Tss2_Tcti_Cancel (ctx);
    assert_int_equal (rc, TSS2_TCTI_RC_NOT_IMPLEMENTED);
}
/*
 * This test excersises all paths through the set locality function
 */
static void
tcti_swtpm_locality_test (void **state)
{
    TSS2_TCTI_CONTEXT *ctx = (TSS2_TCTI_CONTEXT*)*state;
    TSS2_TCTI_COMMON_CONTEXT *tcti_common = tcti_common_context_cast (ctx);
    TSS2_RC rc = TSS2_RC_SUCCESS;
    uint32_t response;

    /* test NULL check */
    rc = Tss2_Tcti_SetLocality (NULL, 3);
    assert_int_equal (rc, TSS2_TCTI_RC_BAD_REFERENCE);

    /* fail due to non-success response code */
    response = 0xFFFFFFFF;
    will_return (__wrap_connect, 0);
    will_return (__wrap_write, 8);
    will_return (__wrap_read, 4);
    will_return (__wrap_read, (uint8_t *) &response);
    rc = Tss2_Tcti_SetLocality (ctx, 3);
    assert_int_equal (rc, TSS2_TCTI_RC_IO_ERROR);

    /* success */
    response = 0x00000000;
    will_return (__wrap_connect, 0);
    will_return (__wrap_write, 8);
    will_return (__wrap_read, 4);
    will_return (__wrap_read, (uint8_t *) &response);
    rc = Tss2_Tcti_SetLocality (ctx, 3);
    assert_int_equal (rc, TSS2_RC_SUCCESS);

    /* put state machine into `receive` to provoke an bad sequence error. */
    tcti_common->state = TCTI_STATE_RECEIVE;
    rc = Tss2_Tcti_SetLocality (ctx, 3);
    assert_int_equal (rc, TSS2_TCTI_RC_BAD_SEQUENCE);
}

int
main (int   argc,
      char *argv[])
{
    const struct CMUnitTest tests[] = {
        cmocka_unit_test (conf_str_to_host_port_success_test),
        cmocka_unit_test (conf_str_to_host_port_no_port_test),
        cmocka_unit_test (conf_str_to_host_ipv6_port_success_test),
        cmocka_unit_test (conf_str_to_host_ipv6_port_no_port_test),
        cmocka_unit_test (conf_str_to_host_port_invalid_port_large_test),
        cmocka_unit_test (conf_str_to_host_port_invalid_port_0_test),
        cmocka_unit_test (conf_str_to_path_success_test),
        cmocka_unit_test (tcti_swtpm_init_all_null_test),
        cmocka_unit_test (tcti_swtpm_init_size_test),
        cmocka_unit_test (tcti_swtpm_init_null_conf_test),
        cmocka_unit_test (tcti_swtpm_get_info_test),
        cmocka_unit_test_setup_teardown (tcti_swtpm_init_fail_connect_test,
                                         tcti_swtpm_setup,
                                         tcti_swtpm_teardown),
        cmocka_unit_test_setup_teardown (tcti_swtpm_get_poll_handles_test,
                                         tcti_swtpm_setup,
                                         tcti_swtpm_teardown),
        cmocka_unit_test_setup_teardown (tcti_swtpm_receive_null_test,
                                         tcti_swtpm_setup,
                                         tcti_swtpm_teardown),
        cmocka_unit_test_setup_teardown (tcti_swtpm_receive_null_size_test,
                                         tcti_swtpm_setup,
                                         tcti_swtpm_teardown),
        cmocka_unit_test_setup_teardown (tcti_swtpm_receive_success_test,
                                         tcti_swtpm_setup,
                                         tcti_swtpm_teardown),
        cmocka_unit_test_setup_teardown (tcti_swtpm_receive_size_success_test,
                                         tcti_swtpm_setup,
                                         tcti_swtpm_teardown),
        cmocka_unit_test_setup_teardown (tcti_swtpm_receive_eof_first_read_test,
                                         tcti_swtpm_setup,
                                         tcti_swtpm_teardown),
        cmocka_unit_test_setup_teardown (tcti_swtpm_receive_eof_second_read_test,
                                         tcti_swtpm_setup,
                                         tcti_swtpm_teardown),
        cmocka_unit_test_setup_teardown (tcti_swtpm_receive_timeout_try_again_test,
                                         tcti_swtpm_setup,
                                         tcti_swtpm_teardown),
        cmocka_unit_test_setup_teardown (tcti_swtpm_transmit_success_test,
                                         tcti_swtpm_setup,
                                         tcti_swtpm_teardown),
        cmocka_unit_test_setup_teardown (tcti_swtpm_transmit_null_test,
                                         tcti_swtpm_setup,
                                         tcti_swtpm_teardown),
        cmocka_unit_test_setup_teardown (tcti_swtpm_transmit_fail_header_test,
                                         tcti_swtpm_setup,
                                         tcti_swtpm_teardown),
        cmocka_unit_test_setup_teardown (tcti_swtpm_control_command_success_test,
                                         tcti_swtpm_setup,
                                         tcti_swtpm_teardown),
        cmocka_unit_test_setup_teardown (tcti_swtpm_control_command_null_test,
                                         tcti_swtpm_setup,
                                         tcti_swtpm_teardown),
        cmocka_unit_test_setup_teardown (tcti_swtpm_control_command_recv_fail_test,
                                         tcti_swtpm_setup,
                                         tcti_swtpm_teardown),
        cmocka_unit_test_setup_teardown (tcti_swtpm_cancel_test,
                                         tcti_swtpm_setup,
                                         tcti_swtpm_teardown),
        cmocka_unit_test_setup_teardown (tcti_swtpm_locality_test,
                                         tcti_swtpm_setup,
                                         tcti_swtpm_teardown),
#ifndef _WIN32
        cmocka_unit_test_setup_teardown (tcti_swtpm_receive_success_test,
                                         tcti_swtpm_setup_unix,
                                         tcti_swtpm_teardown),
#endif
    };
    return cmocka_run_group_tests (tests, NULL, NULL);
}
