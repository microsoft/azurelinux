/* SPDX-License-Identifier: BSD-2-Clause */
/*******************************************************************************
 * Copyright 2018, Fraunhofer SIT sponsored by Infineon Technologies AG
 * All rights reserved.
 ******************************************************************************/

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <stdarg.h>
#include <inttypes.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <sys/stat.h>
#include <unistd.h>
#include <json-c/json_util.h>
#include <json-c/json_tokener.h>

#include <setjmp.h>
#include <cmocka.h>
#include <errno.h>

#include "ifapi_io.h"
#include "util/aux_util.h"

#define LOGMODULE tests
#include "util/log.h"

/*
 * The unit tests will simulate error codes which can be returned by the
 * system calls for file system IO.
 */

/* Global variables to trigger wrapper functions. If set to false the
 * real function will be called. */
bool wrap_fcntl_test = false;
bool wrap_malloc_test = false;
bool wrap_read_test = false;
char _mock_stream; /**< stream will be used to activate wrapper.*/

#define MOCK_STREAM ((FILE *)(&_mock_stream))

/*
 * Wrapper functions for file system io.
 */

int
 __real_stat(const char *pathname, struct stat *statbuf, ...);

int
 __wrap_stat(const char *pathname, struct stat *statbuf, ...)
{
    if (strcmp(pathname, "tss_unit_dummyf")) {
        return __real_stat(pathname, statbuf);
    }
    statbuf->st_mode = R_OK;
    return 0;
}

FILE *
__real_fopen(const char *pathname, const char* mode, ...);
FILE *
__wrap_fopen(const char *pathname, const char* mode, ...)
{
    if (strcmp(pathname, "tss_unit_dummyf")) {
        return __real_fopen(pathname, mode);
    }
    return mock_ptr_type(FILE*);
}

int
__real_fclose(FILE *stream, ...);

int
__wrap_fclose(FILE *stream, ...)
{
    if (stream != MOCK_STREAM) {
        return __real_fclose(stream);
    }
    return mock_type(int);
}

int
__real_fseek(FILE *stream, long offset, int whence, ...);

int
__wrap_fseek(FILE *stream, long offset, int whence, ...)
{
    if (stream != MOCK_STREAM) {
        return __real_fseek(stream, offset, whence);
    }
    return mock_type(int);
}

long
__real_ftell(FILE *stream, ...);

long
__wrap_ftell(FILE *stream, ...)
{
    if (stream != MOCK_STREAM) {
        return __real_ftell(stream);
    }
    return mock_type(int);
}

int
__real_fcntl(int fd, int cmd, ...);

int
__wrap_fcntl(int fd, int cmd, ...)
{
    if (wrap_fcntl_test)
        return mock_type(int);
    else
        return __real_fcntl(fd, cmd);
}

void *
__real_malloc(size_t size, ...);

void *
__wrap_malloc(size_t size, ...)
{
    if (wrap_malloc_test) {
        return mock_ptr_type (void*);
    } else {
        return __real_malloc(size);
    }
}

int
__real_fileno(FILE *stream, ...);

int
__wrap_fileno(FILE *stream, ...)
{
    if (stream != MOCK_STREAM) {
        return __real_fileno(stream);
    }
    return 1;
}

ssize_t
__real_read(int fd, void *buf, size_t count);

ssize_t
__wrap_read(int fd, void *buf, size_t count, ...) {
    if (!wrap_read_test) {
        return __real_read(fd, buf, count);
    }

    return mock_type(ssize_t);
}

/*
 * The return codes for error cases which can be occur in the
 * function: ifapi_io_read_async will be checked.
 */
static void
check_io_read_async(void **state) {
    IFAPI_IO io;
    TSS2_RC r;
    char *dmy_buf = "dummy";

    memset(&io, 0, sizeof(IFAPI_IO));
    io.char_rbuffer = &dmy_buf[0];
    r = ifapi_io_read_async(&io, "tss_unit_dummyf");
    assert_int_equal(r, TSS2_FAPI_RC_IO_ERROR);

    io.char_rbuffer = NULL;
    will_return(__wrap_fopen, NULL);
    r = ifapi_io_read_async(&io, "tss_unit_dummyf");
    assert_int_equal(r, TSS2_FAPI_RC_IO_ERROR);

    will_return(__wrap_fopen, NULL);
    io.char_buffer = "dummy";
    r = ifapi_io_read_async(&io, "tss_unit_dummyf");
    assert_int_equal(r, TSS2_FAPI_RC_IO_ERROR);

    wrap_fcntl_test = true;
    will_return(__wrap_fopen, MOCK_STREAM);
    will_return(__wrap_fcntl, -1);
    will_return_always(__wrap_fclose, 0);
    errno = EAGAIN;
    io.char_buffer = NULL;
    r = ifapi_io_read_async(&io, "tss_unit_dummyf");
    assert_int_equal(r, TSS2_FAPI_RC_IO_ERROR);

    will_return(__wrap_fopen, MOCK_STREAM);
    will_return(__wrap_fopen, MOCK_STREAM);
    will_return(__wrap_fcntl, 0);
    will_return(__wrap_fseek, 0);
    will_return(__wrap_ftell, 1);
    will_return(__wrap_malloc, NULL);
    errno = 0;
    io.char_buffer = NULL;
    wrap_malloc_test = true;

    r = ifapi_io_read_async(&io, "tss_unit_dummyf");
    assert_int_equal(r, TSS2_FAPI_RC_MEMORY);

    wrap_malloc_test = false;

    will_return(__wrap_fopen, MOCK_STREAM);
    will_return(__wrap_fopen, MOCK_STREAM);
    will_return(__wrap_fcntl, 0);
    will_return(__wrap_fseek, 0);
    will_return(__wrap_ftell, 1);
    will_return(__wrap_fcntl, 0);
    will_return(__wrap_fcntl, -1);

    errno = 0;
    io.char_buffer = NULL;
    r = ifapi_io_read_async(&io, "tss_unit_dummyf");
    assert_int_equal(r, TSS2_FAPI_RC_IO_ERROR);
    wrap_fcntl_test = false;
}

/*
 * The return codes for error cases which can be occur in the
 * function: ifapi_io_read_finish will be checked.
 */
static void
check_io_read_finish(void **state) {
    IFAPI_IO io;
    TSS2_RC r;
    uint8_t *buffer[10];
    char io_char_buffer[10];
    size_t count = 10;

    memset(&io, 0, sizeof(IFAPI_IO));
    wrap_read_test = true;
    will_return(__wrap_read, -1);
    // will_return_always(__wrap_fileno, 1);
    will_return_always(__wrap_fclose, 0);
    io.char_buffer = &io_char_buffer[0];
    io.buffer_length = 10;
    io.stream = MOCK_STREAM;
    errno = EAGAIN;
    r = ifapi_io_read_finish(&io, &buffer[0], &count);
    assert_int_equal(r, TSS2_FAPI_RC_TRY_AGAIN);

    will_return(__wrap_read, -1);
    errno = 0;
    r = ifapi_io_read_finish(&io, &buffer[0], &count);
    assert_int_equal(r, TSS2_FAPI_RC_IO_ERROR);

    will_return(__wrap_read, 8);
    errno = 0;
    r = ifapi_io_read_finish(&io, &buffer[0], &count);
    assert_int_equal(r, TSS2_FAPI_RC_TRY_AGAIN);

    will_return(__wrap_read, 10);
    errno = 0;
    r = ifapi_io_read_finish(&io, &buffer[0], &count);
    assert_int_equal(r, TSS2_RC_SUCCESS);

    will_return(__wrap_read, 10);
    errno = 0;
    r = ifapi_io_read_finish(&io, NULL, &count);
    assert_int_equal(r, TSS2_RC_SUCCESS);

    wrap_read_test = false;
}

/*
 * The return codes for error cases which can be occur in the
 * function: ifapi_io_write_async will be checked.
 */
static void
check_io_write_async(void **state) {
    IFAPI_IO io;
    TSS2_RC r;
    uint8_t buffer[5]  = { 1, 2, 3, 4, 5 };
    char *char_buffer = "dummy";

    will_return_always(__wrap_fclose, 0);
    // will_return_always(__wrap_fileno, 1);

    memset(&io, 0, sizeof(IFAPI_IO));

    io.char_rbuffer = &char_buffer[0];
    r = ifapi_io_write_async(&io, "tss_unit_dummyf", NULL, 0);
    assert_int_equal(r, TSS2_FAPI_RC_IO_ERROR);

    io.char_rbuffer = NULL;
    will_return(__wrap_malloc, NULL);
    wrap_malloc_test = true;

    r = ifapi_io_write_async(&io, "tss_unit_dummyf", NULL, 0);
    assert_int_equal(r, TSS2_FAPI_RC_MEMORY);

    wrap_malloc_test = false;

    will_return(__wrap_fopen, NULL);
    r = ifapi_io_write_async(&io, "tss_unit_dummyf", &buffer[0], 5);
    assert_int_equal(r, TSS2_FAPI_RC_IO_ERROR);

    wrap_fcntl_test = true;
    will_return(__wrap_fopen, MOCK_STREAM);
    will_return(__wrap_fcntl, -1);

    errno = EAGAIN;
    r = ifapi_io_write_async(&io, "tss_unit_dummyf", &buffer[0], 5);
    assert_int_equal(r, TSS2_FAPI_RC_IO_ERROR);

    io.char_rbuffer = NULL;
    will_return(__wrap_fopen, MOCK_STREAM);
    will_return(__wrap_fcntl, 0);
    will_return(__wrap_fcntl, 0);
    will_return(__wrap_fcntl, -1);
    errno = 0;
    r = ifapi_io_write_async(&io, "tss_unit_dummyf", &buffer[0], 5);
    assert_int_equal(r, TSS2_FAPI_RC_IO_ERROR);
    wrap_fcntl_test = false;
}

bool wrap_write_test = false;

ssize_t
__real_write(int fd, void *buf, size_t count);

ssize_t
__wrap_write(int fd, void *buf, size_t count, ...) {
    if (!wrap_write_test) {
        return __real_read(fd, buf, count);
    }

    return mock_type(ssize_t);
}

/*
 * The return codes for error cases which can be occur in the
 * function: ifapi_io_write_finish will be checked.
 */
static void
check_io_write_finish(void **state) {
    IFAPI_IO io;
    TSS2_RC r;
    //uint8_t buffer[5]  = { 1, 2, 3, 4, 5 };

    memset(&io, 0, sizeof(IFAPI_IO));
    // will_return_always(__wrap_fileno, 1);
    will_return_always(__wrap_fclose, 0);

    wrap_write_test = true;
    io.stream = MOCK_STREAM;
    will_return(__wrap_write, -1);
    errno = EAGAIN;
    r = ifapi_io_write_finish(&io);
    assert_int_equal(r, TSS2_FAPI_RC_TRY_AGAIN);

    errno = 0;
    will_return(__wrap_write, -1);
    r = ifapi_io_write_finish(&io);
    assert_int_equal(r, TSS2_FAPI_RC_IO_ERROR);

    wrap_write_test = false;
}

int
main(int argc, char *argv[])
{
    const struct CMUnitTest tests[] = {
        cmocka_unit_test(check_io_read_async),
        cmocka_unit_test(check_io_read_finish),
        cmocka_unit_test(check_io_write_async),
        cmocka_unit_test(check_io_write_finish),
    };
    return cmocka_run_group_tests(tests, NULL, NULL);
}
