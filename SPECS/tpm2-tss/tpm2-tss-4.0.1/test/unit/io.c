/* SPDX-License-Identifier: BSD-2-Clause */
/***********************************************************************
 * Copyright (c) 2017-2018, Intel Corporation
 *
 * All rights reserved.
 ***********************************************************************/
#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <inttypes.h>
#include <stdio.h>
#include <stdbool.h>
#include <string.h>

#include <setjmp.h>
#include <cmocka.h>

#include "tss2_tpm2_types.h"

#include "util/io.h"
#define LOGMODULE test
#include "util/log.h"

int
__wrap_socket (
    int domain,
    int type,
    int protocol)
{
    errno = mock_type (int);
    return mock_type (int);
}
int
__wrap_connect (
    int sockfd,
    const struct sockaddr *addr,
    socklen_t addrlen)
{
    errno = mock_type (int);
    return mock_type (int);
}

/*
 * Wrap the 'recv' system call. The mock queue for this function must have an
 * integer return value (the number of byts recv'd), as well as a pointer to
 * a buffer to copy data from to return to the caller.
 */
ssize_t
__wrap_read (int fd, void *buffer, size_t count)
{
    LOG_DEBUG ("%s: reading %zu bytes from fd: %d to buffer at 0x%" PRIxPTR,
               __func__, count, fd, (uintptr_t)buffer);
    int r = mock_type (ssize_t);
    if (r > 0)
        memset(buffer, 0x66, r);
    return r;
}

ssize_t
__wrap_write (int fd, const void *buffer, size_t buffer_size)
{
    LOG_DEBUG ("writing %zd bytes from 0x%" PRIxPTR " to fd: %d",
               buffer_size, (uintptr_t)buffer, fd);
    return mock_type (ssize_t);
}

/*
 * A test case for a successful call to the receive function. This requires
 * that the context and the command buffer be valid (including the size
 * field being set appropriately). The result should be an RC indicating
 * success and the size parameter be updated to reflect the size of the
 * data received.
 */
static void
write_all_simple_success_test (void **state)
{
    ssize_t ret;
    uint8_t buf [10];

    will_return (__wrap_write, sizeof (buf));
    ret = write_all (99, buf, sizeof (buf));
    assert_int_equal(ret, sizeof (buf));
}
/*
 * This test causes the underlying 'read' operation to return '0' bytes
 * indicating EOF.
 */
static void
read_all_eof_test (void **state)
{
    ssize_t ret;
    uint8_t buf [10];

    will_return (__wrap_read, 0);
    ret = read_all (10, buf, sizeof (buf));
    assert_int_equal (ret, 0);
}
/*
 * This test is a minor variation on the 'read_all_eof_test'. We still get
 * an EOF from the underlying read but only after we get a good read, but one
 * that's less than what was requested.
 */
static void
read_all_twice_eof (void **state)
{
    ssize_t ret;
    uint8_t buf [10];

    will_return (__wrap_read, 5);
    will_return (__wrap_read, 0);
    ret = read_all (10, buf, 10);
    assert_int_equal (ret, 5);
}
/* When passed all NULL values ensure that we get back the expected RC. */
static void
socket_connect_test (void **state)
{
    TSS2_RC rc;
    SOCKET sock;
    int ctrl;

    for (ctrl = 0; ctrl < 2; ctrl++) {
        will_return (__wrap_socket, 0);
        will_return (__wrap_socket, 1);
        will_return (__wrap_connect, 0);
        will_return (__wrap_connect, 1);
        rc = socket_connect ("127.0.0.1", 666, ctrl, &sock);
        assert_int_equal (rc, TSS2_RC_SUCCESS);
    }
}
static void
socket_connect_socket_fail_test (void **state)
{
    TSS2_RC rc;
    SOCKET sock;

    will_return (__wrap_socket, EINVAL);
    will_return (__wrap_socket, -1);
    rc = socket_connect ("127.0.0.1", 555, 0, &sock);
    assert_int_equal (rc, TSS2_TCTI_RC_IO_ERROR);
}
static void
socket_connect_connect_fail_test (void **state)
{
    TSS2_RC rc;
    SOCKET sock;

    will_return (__wrap_socket, 0);
    will_return (__wrap_socket, 1);
    will_return (__wrap_connect, ENOTSOCK);
    will_return (__wrap_connect, -1);
    rc = socket_connect ("127.0.0.1", 444, 0, &sock);
    assert_int_equal (rc, TSS2_TCTI_RC_IO_ERROR);
}

/* When passed all NULL values ensure that we get back the expected RC. */
static void
socket_ipv6_connect_test (void **state)
{
    TSS2_RC rc;
    SOCKET sock;
    int ctrl;

    for (ctrl = 0; ctrl < 2; ctrl++) {
        will_return (__wrap_socket, 0);
        will_return (__wrap_socket, 1);
        will_return (__wrap_connect, 0);
        will_return (__wrap_connect, 1);
        rc = socket_connect ("::1", 666, ctrl, &sock);
        assert_int_equal (rc, TSS2_RC_SUCCESS);
    }
}
static void
socket_ipv6_connect_socket_fail_test (void **state)
{
    TSS2_RC rc;
    SOCKET sock;

    will_return (__wrap_socket, EINVAL);
    will_return (__wrap_socket, -1);
    rc = socket_connect ("::1", 555, 0, &sock);
    assert_int_equal (rc, TSS2_TCTI_RC_IO_ERROR);
}
static void
socket_ipv6_connect_connect_fail_test (void **state)
{
    TSS2_RC rc;
    SOCKET sock;

    will_return (__wrap_socket, 0);
    will_return (__wrap_socket, 1);
    will_return (__wrap_connect, ENOTSOCK);
    will_return (__wrap_connect, -1);
    rc = socket_connect ("::1", 444, 0, &sock);
    assert_int_equal (rc, TSS2_TCTI_RC_IO_ERROR);
}

#ifdef _WIN32
static void
socket_connect_unix_win32_fail_test (void **state)
{
    TSS2_RC rc;
    SOCKET sock;

    rc = socket_connect_unix ("/some/path", 0, &sock);
    assert_int_equal (rc, TSS2_RC_BAD_REFERENCE);
}
#else
static void
socket_connect_unix_test (void **state)
{
    TSS2_RC rc;
    SOCKET sock;
    int ctrl;

    for (ctrl = 0; ctrl < 2; ctrl++) {
        will_return (__wrap_socket, 0);
        will_return (__wrap_socket, 1);
        will_return (__wrap_connect, 0);
        will_return (__wrap_connect, 1);
        rc = socket_connect_unix ("/some/path", ctrl, &sock);
        assert_int_equal (rc, TSS2_RC_SUCCESS);
    }
}
static void
socket_connect_unix_socket_fail_test (void **state)
{
    TSS2_RC rc;
    SOCKET sock;

    will_return (__wrap_socket, EINVAL);
    will_return (__wrap_socket, -1);
    rc = socket_connect_unix ("/some/path", 0, &sock);
    assert_int_equal (rc, TSS2_TCTI_RC_IO_ERROR);
}
static void
socket_connect_unix_connect_fail_test (void **state)
{
    TSS2_RC rc;
    SOCKET sock;

    will_return (__wrap_socket, 0);
    will_return (__wrap_socket, 1);
    will_return (__wrap_connect, ENOTSOCK);
    will_return (__wrap_connect, -1);
    rc = socket_connect_unix ("/some/path", 0, &sock);
    assert_int_equal (rc, TSS2_TCTI_RC_IO_ERROR);
}
#endif

static void
socket_connect_null_test (void **state)
{
    TSS2_RC rc;
    SOCKET sock;

    rc = socket_connect (NULL, 444, 0, &sock);
    assert_int_equal (rc, TSS2_TCTI_RC_BAD_REFERENCE);
}

int
main (int   argc,
      char *argv[])
{
    const struct CMUnitTest tests[] = {
        cmocka_unit_test (write_all_simple_success_test),
        cmocka_unit_test (read_all_eof_test),
        cmocka_unit_test (read_all_twice_eof),
        cmocka_unit_test (socket_connect_test),
        cmocka_unit_test (socket_connect_null_test),
        cmocka_unit_test (socket_connect_socket_fail_test),
        cmocka_unit_test (socket_connect_connect_fail_test),
        cmocka_unit_test (socket_ipv6_connect_test),
        cmocka_unit_test (socket_ipv6_connect_socket_fail_test),
        cmocka_unit_test (socket_ipv6_connect_connect_fail_test),
        cmocka_unit_test (socket_connect_unix_test),
        cmocka_unit_test (socket_connect_unix_socket_fail_test),
        cmocka_unit_test (socket_connect_unix_connect_fail_test),
    };
    return cmocka_run_group_tests (tests, NULL, NULL);
}
