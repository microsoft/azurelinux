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
#include <stdarg.h>
#include <stdbool.h>
#include <stdio.h>
#include <string.h>
#include <poll.h>

#include <setjmp.h>
#include <cmocka.h>

#include "tss2_mu.h"
#include "tss2_tcti_device.h"

#include "tss2-tcti/tcti-common.h"
#include "tss2-tcti/tcti-device.h"

/*
 * Size of the TPM2 buffer used in these tests. In some cases this will be
 * the command sent (transmit tests) and in others it's used as the response
 * buffer returned by the TCTI. The only field used by the TCTI is the size
 * field.
 */
#define BUF_SIZE 20
static uint8_t tpm2_buf [BUF_SIZE] = {
    0x80, 0x02, /* TAG */
    0x00, 0x00, 0x00, 0x14, /* size (BUF_SIZE) */
    0x00, 0x00, 0x00, 0x00, /* rc (success) */
    0xde, 0xad, 0xbe, 0xef, /* junk data */
    0xca, 0xfe, 0xba, 0xbe,
    0xfe, 0xef
};
int
__real_open(const char *pathname, int flags, ...);
/* wrap function for open required to test init */
int
__wrap_open(const char *pathname, int flags, ...)
{
    const char* pathname_prefix_dev = "/dev";
    if (strncmp(pathname, pathname_prefix_dev, strlen(pathname_prefix_dev)) == 0) {
        return mock_type (int);
    } else {
        /* only mock opening of device files as the open() syscall is needed
           for code coverage reports as well */
        return __real_open(pathname, flags);
    }
}
/**
 * When passed all NULL values ensure that we get back the expected RC
 * indicating bad values.
 */
static void
tcti_device_init_all_null_test (void **state)
{
    TSS2_RC rc;

    rc = Tss2_Tcti_Device_Init (NULL, NULL, NULL);
    assert_int_equal (rc, TSS2_TCTI_RC_BAD_VALUE);
}
/* Determine the size of a TCTI context structure. Requires calling the
 * initialization function for the device TCTI with the first parameter
 * (the TCTI context) NULL.
 */
static void
tcti_device_init_size_test (void **state)
{
    size_t tcti_size = 0;
    TSS2_RC ret = TSS2_RC_SUCCESS;

    ret = Tss2_Tcti_Device_Init (NULL, &tcti_size, NULL);
    assert_int_equal (ret, TSS2_RC_SUCCESS);
}
/* Test the failure of opening a specified device file */
static void
tcti_device_init_conf_fail (void **state)
{
    size_t tcti_size = 0;
    TSS2_RC ret = TSS2_RC_SUCCESS;
    TSS2_TCTI_CONTEXT *ctx = NULL;

    ret = Tss2_Tcti_Device_Init (NULL, &tcti_size, NULL);
    assert_true (ret == TSS2_RC_SUCCESS);
    ctx = calloc (1, tcti_size);
    assert_non_null (ctx);
    errno = ENOENT; /* No such file or directory */
    will_return (__wrap_open, -1);
    ret = Tss2_Tcti_Device_Init (ctx, &tcti_size, "/dev/nonexistent");
    assert_true (ret == TSS2_TCTI_RC_IO_ERROR);

    free(ctx);
}
/* Test the device file recognition if no config string was specified */
static void
tcti_device_init_conf_default_fail (void **state)
{
    size_t tcti_size = 0;
    TSS2_RC ret = TSS2_RC_SUCCESS;
    TSS2_TCTI_CONTEXT *ctx = NULL;

    ret = Tss2_Tcti_Device_Init (NULL, &tcti_size, NULL);
    assert_true (ret == TSS2_RC_SUCCESS);
    ctx = calloc (1, tcti_size);
    assert_non_null (ctx);
    errno = EACCES; /* Permission denied */
    will_return (__wrap_open, -1);
    will_return (__wrap_open, -1);
    ret = Tss2_Tcti_Device_Init (ctx, &tcti_size, NULL);
    assert_true (ret == TSS2_TCTI_RC_IO_ERROR);

    free(ctx);
}

/* Test the device file recognition if no config string was specified */
static void
tcti_device_init_conf_default_success (void **state)
{
    size_t tcti_size = 0;
    TSS2_RC ret = TSS2_RC_SUCCESS;
    TSS2_TCTI_CONTEXT *ctx = NULL;

    ret = Tss2_Tcti_Device_Init (NULL, &tcti_size, NULL);
    assert_true (ret == TSS2_RC_SUCCESS);
    ctx = calloc (1, tcti_size);
    assert_non_null (ctx);
    will_return (__wrap_open, 3);
    will_return (__wrap_write, 12);
    will_return (__wrap_write, tpm2_buf);
    will_return (__wrap_poll, 1);
    will_return (__wrap_read, 10);
    will_return (__wrap_read, tpm2_buf);
    will_return (__wrap_poll, 1);
    will_return (__wrap_read, 8);
    will_return (__wrap_read, tpm2_buf);
    ret = Tss2_Tcti_Device_Init (ctx, &tcti_size, NULL);
    assert_true (ret == TSS2_RC_SUCCESS);

    free(ctx);
}

/* wrap functions for read & write required to test receive / transmit */
ssize_t
__wrap_read (int fd, void *buf, size_t count)
{
    ssize_t ret = mock_type (ssize_t);
    uint8_t *buf_in = mock_type (uint8_t*);

    memcpy (buf, buf_in, ret);
    return ret;
}
ssize_t
__wrap_write (int fd, const void *buffer, size_t buffer_size)
{
    ssize_t ret = mock_type (ssize_t);
    uint8_t *buf_out = mock_type (uint8_t*);

    memcpy (buf_out, buffer, ret);
    return ret;
}

int
__wrap_poll (struct pollfd *fds, nfds_t nfds, int timeout)
{
    int ret = mock_type (int);

    fds->revents = fds->events;
    return ret;
}

/* Setup functions to create the context for the device TCTI */
static int
tcti_device_setup (void **state)
{
    size_t tcti_size = 0;
    TSS2_RC ret = TSS2_RC_SUCCESS;
    TSS2_TCTI_CONTEXT *ctx = NULL;

    ret = Tss2_Tcti_Device_Init (NULL, &tcti_size, NULL);
    assert_true (ret == TSS2_RC_SUCCESS);
    ctx = calloc (1, tcti_size);
    assert_non_null (ctx);
    will_return (__wrap_open, 3);
    will_return (__wrap_write, 12);
    will_return (__wrap_write, tpm2_buf);
    will_return (__wrap_poll, 1);
    will_return (__wrap_read, 10);
    will_return (__wrap_read, tpm2_buf);
    will_return (__wrap_poll, 1);
    will_return (__wrap_read, 0);
    will_return (__wrap_read, tpm2_buf);
    will_return (__wrap_open, 3);
    ret = Tss2_Tcti_Device_Init (ctx, &tcti_size, "/dev/null");
    assert_true (ret == TSS2_RC_SUCCESS);

    *state = ctx;
    return 0;
}

static int
tcti_device_teardown (void **state)
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
tcti_device_get_poll_handles_test (void **state)
{
    TSS2_TCTI_CONTEXT *ctx = (TSS2_TCTI_CONTEXT*)*state;
    size_t num_handles = 5;
    TSS2_TCTI_POLL_HANDLE handles [5] = { 0 };
    TSS2_RC rc;

    rc = Tss2_Tcti_GetPollHandles (ctx, handles, &num_handles);
    assert_int_equal (rc, TSS2_RC_SUCCESS);
    assert_int_equal (num_handles, 1);
}
/*
 */
static void
tcti_device_receive_null_size_test (void **state)
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
 * A test case for a successful call to the receive function. This requires
 * that the context and the command buffer be valid (including the size
 * field being set appropriately). The result should be an RC indicating
 * success and the size parameter be updated to reflect the size of the
 * data received.
 */
static void
tcti_device_receive_success (void **state)
{
    TSS2_TCTI_CONTEXT *ctx = (TSS2_TCTI_CONTEXT*)*state;
    TSS2_TCTI_COMMON_CONTEXT *tcti_common = tcti_common_context_cast (ctx);
    TSS2_RC rc;
    /* output buffer for response */
    uint8_t buf_out [BUF_SIZE + 5] = { 0 };
    size_t size = BUF_SIZE + 5;

    /* Keep state machine check in `receive` from returning error. */
    tcti_common->state = TCTI_STATE_RECEIVE;
    will_return (__wrap_poll, 1);
    will_return (__wrap_read, BUF_SIZE);
    will_return (__wrap_read, tpm2_buf);
    rc = Tss2_Tcti_Receive (ctx,
                            &size,
                            buf_out,
                            TSS2_TCTI_TIMEOUT_BLOCK);
    assert_true (rc == TSS2_RC_SUCCESS);
    assert_int_equal (BUF_SIZE, size);
    assert_memory_equal (tpm2_buf, buf_out, size);
}
/*
 * Ensure that when the 'read' results in an EOF, we get a response code
 * indicating as much. EOF happens if / when the device driver kills our
 * connection.
 */
static void
tcti_device_receive_eof_test (void **state)
{
    TSS2_TCTI_CONTEXT *ctx = (TSS2_TCTI_CONTEXT*)*state;
    TSS2_TCTI_COMMON_CONTEXT *tcti_common = tcti_common_context_cast (ctx);
    TSS2_RC rc;
    /* output buffer for response */
    uint8_t buf_out [BUF_SIZE + 5] = { 0 };
    size_t size = BUF_SIZE + 5;

    /* Keep state machine check in `receive` from returning error. */
    tcti_common->state = TCTI_STATE_RECEIVE;
    will_return (__wrap_poll, 1);
    will_return (__wrap_read, 0);
    will_return (__wrap_read, tpm2_buf);
    rc = Tss2_Tcti_Receive (ctx,
                            &size,
                            buf_out,
                            TSS2_TCTI_TIMEOUT_BLOCK);
    assert_int_equal (rc, TSS2_TCTI_RC_NO_CONNECTION);
}
/*
 * This is a weird test: The device TCTI can't read the header for the
 * response buffer separately from the body. This means it can't know the size
 * of the response before reading the whole thing. In the event that the caller
 * provides a buffer that isn't large enough to hold the full response the TCTI
 * will just read as much data as the buffer will hold. Subsequent interactions
 * with the kernel driver will likely result in an error.
 */
static void
tcti_device_receive_buffer_lt_response (void **state)
{
    TSS2_TCTI_CONTEXT *ctx = (TSS2_TCTI_CONTEXT*)*state;
    TSS2_TCTI_COMMON_CONTEXT *tcti_common = tcti_common_context_cast (ctx);
    TSS2_RC rc;
    uint8_t buf_out [BUF_SIZE] = { 0 };
    /* set size to lt the size in the header of the TPM2 response buffer */
    size_t size = BUF_SIZE - 1;
    size_t small_size = TPM_HEADER_SIZE + 1;

    /* Keep state machine check in `receive` from returning error. */
    tcti_common->state = TCTI_STATE_RECEIVE;
    will_return (__wrap_poll, 1);
    will_return (__wrap_read, size);
    will_return (__wrap_read, tpm2_buf);
    rc = Tss2_Tcti_Receive (ctx,
                            &small_size,
                            buf_out,
                            TSS2_TCTI_TIMEOUT_BLOCK);
    assert_int_equal (rc, TSS2_TCTI_RC_GENERAL_FAILURE);
}
/*
 * A test case for a successful call to the transmit function. This requires
 * that the context and the cmmand buffer be valid. The only indication of
 * success is the RC.
 */
static void
tcti_device_transmit_success (void **state)
{
    TSS2_TCTI_CONTEXT *ctx = (TSS2_TCTI_CONTEXT*)*state;
    TSS2_RC rc;
    /* output buffer for response */
    uint8_t buf_out [BUF_SIZE] = { 0 };

    will_return (__wrap_write, BUF_SIZE);
    will_return (__wrap_write, buf_out);
    rc = Tss2_Tcti_Transmit (ctx,
                             BUF_SIZE,
                             tpm2_buf);
    assert_true (rc == TSS2_RC_SUCCESS);
    assert_memory_equal (tpm2_buf, buf_out, BUF_SIZE);
}
/*
 * A test case for a successful poll
 */
static void
tcti_device_poll_success (void **state)
{
    TSS2_TCTI_CONTEXT *ctx = (TSS2_TCTI_CONTEXT*)*state;
    TSS2_TCTI_COMMON_CONTEXT *tcti_common = tcti_common_context_cast (ctx);
    TSS2_RC rc;
    /* output buffer for response */
    uint8_t buf_out [BUF_SIZE] = { 0 };
    size_t size = BUF_SIZE;

    /* Keep state machine check in `receive` from returning error. */
    tcti_common->state = TCTI_STATE_RECEIVE;
    will_return (__wrap_poll, 1);
    will_return (__wrap_read, BUF_SIZE);
    will_return (__wrap_read, tpm2_buf);

    rc = Tss2_Tcti_Receive (ctx,
                            &size,
                            buf_out,
                            TSS2_TCTI_TIMEOUT_BLOCK);

    assert_true (rc == TSS2_RC_SUCCESS);
    assert_int_equal (BUF_SIZE, size);
    assert_memory_equal (tpm2_buf, buf_out, size);
}
/*
 * A test case for poll timeout
 */
static void
tcti_device_poll_timeout (void **state)
{
    TSS2_TCTI_CONTEXT *ctx = (TSS2_TCTI_CONTEXT*)*state;
    TSS2_TCTI_COMMON_CONTEXT *tcti_common = tcti_common_context_cast (ctx);
    TSS2_RC rc;
    /* output buffer for response */
    uint8_t buf_out [BUF_SIZE] = { 0 };
    size_t size = BUF_SIZE;

    /* Keep state machine check in `receive` from returning error. */
    tcti_common->state = TCTI_STATE_RECEIVE;
    will_return (__wrap_poll, 0);

    rc = Tss2_Tcti_Receive (ctx,
                            &size,
                            buf_out,
                            TSS2_TCTI_TIMEOUT_BLOCK);

    assert_true (rc == TSS2_TCTI_RC_TRY_AGAIN);
}
/*
 * A test case for poll io-error
 */
static void
tcti_device_poll_io_error (void **state)
{
    TSS2_TCTI_CONTEXT *ctx = (TSS2_TCTI_CONTEXT*)*state;
    TSS2_TCTI_COMMON_CONTEXT *tcti_common = tcti_common_context_cast (ctx);
    TSS2_RC rc;
    /* output buffer for response */
    uint8_t buf_out [BUF_SIZE] = { 0 };
    size_t size = BUF_SIZE;

    /* Keep state machine check in `receive` from returning error. */
    tcti_common->state = TCTI_STATE_RECEIVE;
    will_return (__wrap_poll, -1);

    rc = Tss2_Tcti_Receive (ctx,
                            &size,
                            buf_out,
                            TSS2_TCTI_TIMEOUT_BLOCK);

    assert_true (rc == TSS2_TCTI_RC_IO_ERROR);
}

int
main(int argc, char* argv[])
{
    const struct CMUnitTest tests[] = {
        cmocka_unit_test (tcti_device_init_all_null_test),
        cmocka_unit_test(tcti_device_init_size_test),
        cmocka_unit_test(tcti_device_init_conf_fail),
        cmocka_unit_test(tcti_device_init_conf_default_fail),
        cmocka_unit_test(tcti_device_init_conf_default_success),
        cmocka_unit_test_setup_teardown (tcti_device_get_poll_handles_test,
                                         tcti_device_setup,
                                         tcti_device_teardown),
        cmocka_unit_test_setup_teardown (tcti_device_receive_null_size_test,
                                         tcti_device_setup,
                                         tcti_device_teardown),
        cmocka_unit_test_setup_teardown (tcti_device_receive_success,
                                         tcti_device_setup,
                                         tcti_device_teardown),
        cmocka_unit_test_setup_teardown (tcti_device_receive_eof_test,
                                         tcti_device_setup,
                                         tcti_device_teardown),
        cmocka_unit_test_setup_teardown (tcti_device_receive_buffer_lt_response,
                                         tcti_device_setup,
                                         tcti_device_teardown),
        cmocka_unit_test_setup_teardown (tcti_device_transmit_success,
                                         tcti_device_setup,
                                         tcti_device_teardown),
        cmocka_unit_test_setup_teardown (tcti_device_poll_success,
                                         tcti_device_setup,
                                         tcti_device_teardown),
        cmocka_unit_test_setup_teardown (tcti_device_poll_timeout,
                                         tcti_device_setup,
                                         tcti_device_teardown),
        cmocka_unit_test_setup_teardown (tcti_device_poll_io_error,
                                         tcti_device_setup,
                                         tcti_device_teardown),
    };
    return cmocka_run_group_tests (tests, NULL, NULL);
}
