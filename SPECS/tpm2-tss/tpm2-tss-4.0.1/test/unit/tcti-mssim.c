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
#include "tss2_tcti_mssim.h"

#include "tss2-tcti/tcti-common.h"
#include "tss2-tcti/tcti-mssim.h"
#include "util/key-value-parse.h"

/*
 * This function is defined in the tcti-mssim module but not exposed through
 * the header.
 */
TSS2_RC
mssim_kv_callback (const key_value_t *key_value,
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
    mssim_conf_t mssim_conf = {
        .path = unusedpath
    };

    rc = parse_key_value_string (conf, mssim_kv_callback, &mssim_conf);
    assert_int_equal (rc, TSS2_RC_SUCCESS);
    assert_int_equal (mssim_conf.port, 2321);
    assert_string_equal (mssim_conf.host, "127.0.0.1");
    assert_null (mssim_conf.path);
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
    mssim_conf_t mssim_conf = {
        .host = "foo",
        .port = NO_PORT_VALUE,
        .path = unusedpath
    };

    rc = parse_key_value_string (conf, mssim_kv_callback, &mssim_conf);
    assert_int_equal (rc, TSS2_RC_SUCCESS);
    assert_string_equal (mssim_conf.host, "127.0.0.1");
    assert_int_equal (mssim_conf.port, NO_PORT_VALUE);
    assert_null (mssim_conf.path);
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
    mssim_conf_t mssim_conf = {
        .path = unusedpath
    };

    rc = parse_key_value_string (conf, mssim_kv_callback, &mssim_conf);
    assert_int_equal (rc, TSS2_RC_SUCCESS);
    assert_int_equal (mssim_conf.port, 2321);
    assert_string_equal (mssim_conf.host, "::1");
    assert_null (mssim_conf.path);
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
    mssim_conf_t mssim_conf = {
        .port = NO_PORT_VALUE,
        .path = NO_PATH_VALUE
    };

    rc = parse_key_value_string (conf, mssim_kv_callback, &mssim_conf);
    assert_int_equal (rc, TSS2_RC_SUCCESS);
    assert_int_equal (mssim_conf.port, NO_PORT_VALUE);
    assert_string_equal (mssim_conf.host, "::1");
    assert_null (mssim_conf.path);
}

/*
 * The 'conf_str_to_host_port' function rejects ports over UINT16_MAX.
 */
static void
conf_str_to_host_port_invalid_port_large_test (void **state)
{
    TSS2_RC rc;
    char conf[] = "host=127.0.0.1,port=99999";
    mssim_conf_t mssim_conf = { 0 };

    rc = parse_key_value_string (conf, mssim_kv_callback, &mssim_conf);
    assert_int_equal (rc, TSS2_TCTI_RC_BAD_VALUE);
}
/* The 'conf_str_to_host_port' function rejects URIs with port == 0 */
static void
conf_str_to_host_port_invalid_port_0_test (void **state)
{
    TSS2_RC rc;
    char conf[] = "host=127.0.0.1,port=0";
    mssim_conf_t mssim_conf = { 0 };

    rc = parse_key_value_string (conf, mssim_kv_callback, &mssim_conf);
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
    mssim_conf_t mssim_conf = {
        .host = unusedhost
    };

    rc = parse_key_value_string (conf, mssim_kv_callback, &mssim_conf);
    assert_int_equal (rc, TSS2_RC_SUCCESS);
    assert_string_equal (mssim_conf.path, "/some/path");
    assert_null (mssim_conf.host);
}

/* When passed all NULL values ensure that we get back the expected RC. */
static void
tcti_socket_init_all_null_test (void **state)
{
    TSS2_RC rc;

    rc = Tss2_Tcti_Mssim_Init (NULL, NULL, NULL);
    assert_int_equal (rc, TSS2_TCTI_RC_BAD_VALUE);
}
/*
 * Determine the size of a TCTI context structure. Requires calling the
 * initialization function for the device TCTI with the first parameter
 * (the TCTI context) NULL.
 */
static void
tcti_socket_init_size_test (void **state)
{
    size_t tcti_size = 0;
    TSS2_RC ret = TSS2_RC_SUCCESS;

    ret = Tss2_Tcti_Mssim_Init (NULL, &tcti_size, NULL);
    assert_int_equal (ret, TSS2_RC_SUCCESS);
    assert_int_equal (tcti_size, sizeof (TSS2_TCTI_MSSIM_CONTEXT));
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
 * Wrap the 'poll' system call.
 */
int
__wrap_poll (struct pollfd *fds, nfds_t nfds, int timeout)
{
    int ret = mock_type (int);

    fds->revents = fds->events;
    return ret;
}
/*
 * This is a utility function used by other tests to setup a TCTI context. It
 * effectively wraps the init / allocate / init pattern as well as priming the
 * mock functions necessary for a the successful call to
 * 'Tss2_Tcti_Mssim_Init'.
 */
static TSS2_TCTI_CONTEXT*
tcti_socket_init_from_conf (const char *conf)
{
    size_t tcti_size = 0;
    uint8_t recv_buf[4] = { 0 };
    TSS2_RC ret = TSS2_RC_SUCCESS;
    TSS2_TCTI_CONTEXT *ctx = NULL;

    printf ("%s: before first init\n", __func__);
    ret = Tss2_Tcti_Mssim_Init (NULL, &tcti_size, NULL);
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
     * two 'platform commands are sent on initialization, 4 bytes sent for
     * each, 4 byte response received (all 0's) for each.
     */
    will_return (__wrap_write, 4);
    will_return (__wrap_read, 4);
    will_return (__wrap_read, recv_buf);
    will_return (__wrap_write, 4);
    will_return (__wrap_read, 4);
    will_return (__wrap_read, recv_buf);
    printf ("%s: before second_init\n", __func__);
    ret = Tss2_Tcti_Mssim_Init (ctx, &tcti_size, conf);
    printf ("%s: after second init\n", __func__);
    assert_int_equal (ret, TSS2_RC_SUCCESS);
    return ctx;
}

/*
 * This is a utility function to setup the "default" TCTI context.
 */
static int
tcti_socket_setup (void **state)
{
    printf ("%s: before tcti_socket_init_from_conf\n", __func__);
    *state = tcti_socket_init_from_conf ("host=127.0.0.1,port=666");
    printf ("%s: done\n", __func__);
    return 0;
}
#ifndef _WIN32
/* variant of tcti_socket_setup() for unix domain sockets. */
static int
tcti_socket_setup_unix (void **state)
{
    printf ("%s: before tcti_socket_init_from_conf\n", __func__);
    *state = tcti_socket_init_from_conf ("path=/notarealdirectory/notarealfile");
    printf ("%s: done\n", __func__);
    return 0;
}
#endif
static void
tcti_socket_init_null_conf_test (void **state)
{
    TSS2_TCTI_CONTEXT *ctx = tcti_socket_init_from_conf (NULL);
    assert_non_null (ctx);
    free (ctx);
}
/*
 * This is a utility function to teardown a TCTI context allocated by the
 * tcti_socket_setup function.
 */
static int
tcti_socket_teardown (void **state)
{
    TSS2_TCTI_CONTEXT *ctx = (TSS2_TCTI_CONTEXT*)*state;

    Tss2_Tcti_Finalize (ctx);
    free (ctx);
    return 0;
}
/*
 * This test ensures that the GetPollHandles function in the device TCTI
 * returns the expected value. Since this TCTI does not support async I/O
 * on account of limitations in the kernel it just returns the
 * NOT_IMPLEMENTED response code.
 */
static void
tcti_mssim_get_poll_handles_test (void **state)
{
    TSS2_TCTI_CONTEXT *ctx = (TSS2_TCTI_CONTEXT*)*state;
    size_t num_handles = 5;
    TSS2_TCTI_POLL_HANDLE handles [5] = { 0 };

    TSS2_RC rc = Tss2_Tcti_GetPollHandles (ctx, handles, &num_handles);
    TSS2_TCTI_MSSIM_CONTEXT *mssim_ctx = (TSS2_TCTI_MSSIM_CONTEXT*)ctx;
    assert_int_equal (rc, TSS2_RC_SUCCESS);
    assert_int_equal (num_handles, 1);
    assert_int_equal (handles[0].fd, mssim_ctx->tpm_sock);
}
/*
 */
static void
tcti_socket_receive_null_size_test (void **state)
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
tcti_socket_receive_success_test (void **state)
{
    TSS2_TCTI_CONTEXT *ctx = (TSS2_TCTI_CONTEXT*)*state;
    TSS2_TCTI_COMMON_CONTEXT *tcti_common = tcti_common_context_cast (ctx);
    TSS2_RC rc = TSS2_RC_SUCCESS;
    size_t response_size = 0xc;
    uint8_t response_in [] = { 0x80, 0x02,
                               0x00, 0x00, 0x00, 0x0c,
                               0x00, 0x00, 0x00, 0x00,
                               0x01, 0x02,
    /* simulator appends 4 bytes of 0's to every response */
                               0x00, 0x00, 0x00, 0x00 };
    uint8_t response_out [12] = { 0 };

    /* Keep state machine check in `receive` from returning error. */
    tcti_common->state = TCTI_STATE_RECEIVE;
    /* receive response size */
    will_return (__wrap_poll, 1);
    will_return (__wrap_read, 4);
    will_return (__wrap_read, &response_in [2]);
    /* receive tag */
    will_return (__wrap_poll, 1);
    will_return (__wrap_read, 2);
    will_return (__wrap_read, response_in);
    /* receive size (again)  */
    will_return (__wrap_poll, 1);
    will_return (__wrap_read, 4);
    will_return (__wrap_read, &response_in [2]);
    /* receive the rest of the command */
    will_return (__wrap_read, 0xc - sizeof (TPM2_ST) - sizeof (UINT32));
    will_return (__wrap_read, &response_in [6]);
    /* receive the 4 bytes of 0's appended by the simulator */
    will_return (__wrap_read, 4);
    will_return (__wrap_read, &response_in [12]);

    rc = Tss2_Tcti_Receive (ctx, &response_size, response_out, TSS2_TCTI_TIMEOUT_BLOCK);
    assert_int_equal (rc, TSS2_RC_SUCCESS);
    assert_memory_equal (response_in, response_out, response_size);
}
/*
 */
static void
tcti_socket_receive_size_success_test (void **state)
{
    TSS2_TCTI_CONTEXT *ctx = (TSS2_TCTI_CONTEXT*)*state;
    TSS2_TCTI_COMMON_CONTEXT *tcti_common = tcti_common_context_cast (ctx);
    TSS2_RC rc = TSS2_RC_SUCCESS;
    size_t response_size = 0;
    uint8_t response_in [] = { 0x80, 0x02,
                               0x00, 0x00, 0x00, 0x0c,
                               0x00, 0x00, 0x00, 0x00,
                               0x01, 0x02,
    /* simulator appends 4 bytes of 0's to every response */
                               0x00, 0x00, 0x00, 0x00 };
    uint8_t response_out [12] = { 0 };

    /* Keep state machine check in `receive` from returning error. */
    tcti_common->state = TCTI_STATE_RECEIVE;
    /* receive response size */
    will_return (__wrap_poll, 1);
    will_return (__wrap_read, 4);
    will_return (__wrap_read, &response_in [2]);
    rc = Tss2_Tcti_Receive (ctx, &response_size, NULL, TSS2_TCTI_TIMEOUT_BLOCK);

    assert_int_equal (rc, TSS2_RC_SUCCESS);
    assert_int_equal (response_size, 0xc);
    /* receive tag */
    will_return (__wrap_poll, 1);
    will_return (__wrap_read, 2);
    will_return (__wrap_read, response_in);
    /* receive size (again)  */
    will_return (__wrap_poll, 1);
    will_return (__wrap_read, 4);
    will_return (__wrap_read, &response_in [2]);
    /* receive the rest of the command */
    will_return (__wrap_read, 0xc - sizeof (TPM2_ST) - sizeof (UINT32));
    will_return (__wrap_read, &response_in [6]);
    /* receive the 4 bytes of 0's appended by the simulator */
    will_return (__wrap_read, 4);
    will_return (__wrap_read, &response_in [12]);

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
tcti_mssim_receive_eof_first_read_test (void **state)
{
    TSS2_TCTI_CONTEXT *ctx = (TSS2_TCTI_CONTEXT*)*state;
    TSS2_TCTI_COMMON_CONTEXT *tcti_common = tcti_common_context_cast (ctx);
    TSS2_RC rc;
    /* output buffer for response */
    uint8_t buf [TPM_HEADER_SIZE] = { 0 };
    size_t size = sizeof (buf);

    /* Keep state machine check in `receive` from returning error. */
    tcti_common->state = TCTI_STATE_RECEIVE;
    will_return (__wrap_poll, 1);
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
tcti_mssim_receive_eof_second_read_test (void **state)
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
    will_return (__wrap_poll, 1);
    will_return (__wrap_read, 4);
    will_return (__wrap_read, &response_in [2]);
    /* setup 0 for EOF on second read */
    will_return (__wrap_poll, 1);
    will_return (__wrap_read, 0);
    will_return (__wrap_read, response_in);
    rc = Tss2_Tcti_Receive (ctx,
                            &size,
                            response_out,
                            TSS2_TCTI_TIMEOUT_BLOCK);
    assert_true (rc == TSS2_TCTI_RC_IO_ERROR);
}
/*
 * This test exercises the successful code path through the transmit function.
 */
static void
tcti_socket_transmit_success_test (void **state)
{
    TSS2_TCTI_CONTEXT *ctx = (TSS2_TCTI_CONTEXT*)*state;
    TSS2_RC rc = TSS2_RC_SUCCESS;
    uint8_t command [] = { 0x80, 0x02,
                           0x00, 0x00, 0x00, 0x0c,
                           0x00, 0x00, 0x00, 0x00,
                           0x01, 0x02 };
    size_t  command_size = sizeof (command);

    /* send the TPM2_SEND_COMMAND code */
    will_return (__wrap_write, 4);
    /* send the locality for the command */
    will_return (__wrap_write, 1);
    /* send the number of bytes in command */
    will_return (__wrap_write, 4);
    /* send the command buffer */
    will_return (__wrap_write, 0xc);
    rc = Tss2_Tcti_Transmit (ctx, command_size, command);
    assert_int_equal (rc, TSS2_RC_SUCCESS);
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
        cmocka_unit_test (tcti_socket_init_all_null_test),
        cmocka_unit_test (tcti_socket_init_size_test),
        cmocka_unit_test (tcti_socket_init_null_conf_test),
        cmocka_unit_test_setup_teardown (tcti_mssim_get_poll_handles_test,
                                         tcti_socket_setup,
                                         tcti_socket_teardown),
        cmocka_unit_test_setup_teardown (tcti_socket_receive_null_size_test,
                                         tcti_socket_setup,
                                         tcti_socket_teardown),
        cmocka_unit_test_setup_teardown (tcti_socket_receive_success_test,
                                  tcti_socket_setup,
                                  tcti_socket_teardown),
        cmocka_unit_test_setup_teardown (tcti_socket_receive_size_success_test,
                                  tcti_socket_setup,
                                  tcti_socket_teardown),
        cmocka_unit_test_setup_teardown (tcti_mssim_receive_eof_first_read_test,
                                         tcti_socket_setup,
                                         tcti_socket_teardown),
        cmocka_unit_test_setup_teardown (tcti_mssim_receive_eof_second_read_test,
                                         tcti_socket_setup,
                                         tcti_socket_teardown),
        cmocka_unit_test_setup_teardown (tcti_socket_transmit_success_test,
                                  tcti_socket_setup,
                                  tcti_socket_teardown),
#ifndef _WIN32
        cmocka_unit_test_setup_teardown (tcti_socket_receive_success_test,
                                  tcti_socket_setup_unix,
                                  tcti_socket_teardown),
#endif
    };
    return cmocka_run_group_tests (tests, NULL, NULL);
}
