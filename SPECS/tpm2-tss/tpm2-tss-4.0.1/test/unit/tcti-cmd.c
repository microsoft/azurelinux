/* SPDX-License-Identifier: BSD-2-Clause */

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <inttypes.h>
#include <limits.h>
#include <setjmp.h>
#include <stdarg.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <cmocka.h>
#include <unistd.h>
#include <signal.h>

#if defined (__FreeBSD__)
#include <sys/procctl.h>
#else
#include <sys/prctl.h>
#endif
#include <sys/types.h>
#include <sys/wait.h>
#include <sys/time.h>

#include "tss2_tcti.h"
#include "tss2_tcti_cmd.h"
#include "tcti-cmd-test.h"

#include "tss2-tcti/tcti-common.h"
#include "tss2-tcti/tcti-cmd.h"

#define LOGMODULE tests
#include "util/log.h"

#define EXECLP_CMD "test/helper/tpm_cmd_tcti_dummy"

extern TSS2_TCTI_INFO *Tss2_Tcti_Info (void);

static inline
TSS2_TCTI_CONTEXT *state_cast (void **state)
{
    return (TSS2_TCTI_CONTEXT *)*state;
}

int tcti_cmd_pipe (int pipefd[2])
{
    int rc = mock_type (int);
    if (!rc) {
        return pipe (pipefd);
    }

    errno = rc;
    return -1;
}

int tcti_cmd_fork (void)
{
    int rc = mock_type (int);
    if (!rc) {
        return fork ();
    }

    errno = rc;
    return -1;
}

FILE *tcti_cmd_fdopen (int fd, const char *mode)
{
    int rc = mock_type (int);
    if (!rc) {
        return fdopen (fd, mode);
    }

    errno = rc;
    return NULL;
}

int tcti_cmd_sigprocmask (int how, const sigset_t *set, sigset_t *oldset)
{
    int rc = mock_type (int);
    if (!rc) {
        return sigprocmask (how, set, oldset);
    }

    errno = rc;
    return -1;
}

int tcti_cmd_ferror (FILE *stream)
{
    int rc = mock_type (int);
    if (!rc) {
        return ferror (stream);
    }

    errno = rc;
    return -1;
}

size_t tcti_cmd_fwrite (const void *ptr, size_t size, size_t nmemb,
        FILE *stream)
{
    int rc = mock_type (int);
    if (!rc) {
        return fwrite (ptr, size, nmemb, stream);
    }

    will_return (tcti_cmd_ferror, rc);
    errno = rc;
    return 0;
}

TSS2_TCTI_CONTEXT *
test_common_setup (const char *cmd)
{
    will_return_always (tcti_cmd_sigprocmask, 0);
    will_return_always (tcti_cmd_fdopen, 0);
    will_return_always (tcti_cmd_fork, 0);
    will_return_always (tcti_cmd_pipe, 0);

    size_t tcti_size = 0;
    TSS2_RC rval = Tss2_Tcti_Cmd_Init (NULL, &tcti_size, cmd);
    assert_int_equal (rval, TSS2_RC_SUCCESS);

    TSS2_TCTI_CONTEXT *tcti_context = calloc (1, tcti_size);
    assert_non_null (tcti_context);

    rval = Tss2_Tcti_Cmd_Init (tcti_context, &tcti_size, cmd);
    assert_int_equal (rval, TSS2_RC_SUCCESS);

    return tcti_context;
}

static int
test_teardown (void **state)
{
    will_return_always (tcti_cmd_sigprocmask, 0);

    TSS2_TCTI_CONTEXT *tcti_context = state_cast (state);
    if (tcti_context) {
        Tss2_Tcti_Finalize (tcti_context);
        free (tcti_context);
    }

    return 0;
}

/*
 * Unit Test Code Starts Here
 */

/* When passed all NULL values ensure that we get back the expected RC. */
static void
tcti_cmd_init_all_null_test (void **state)
{
    TSS2_RC rval = Tss2_Tcti_Cmd_Init (NULL, NULL, NULL);
    assert_int_equal (rval, TSS2_TCTI_RC_BAD_VALUE);
}

/*
 * Determine the size of a TCTI context structure. Requires calling the
 * initialization function for the cmd TCTI with the first parameter
 * (the TCTI context) NULL.
 */
static void
tcti_cmd_init_size_test (void **state)
{
    size_t tcti_size = 0;

    TSS2_RC rval = Tss2_Tcti_Cmd_Init (NULL, &tcti_size, __func__);
    assert_int_equal (rval, TSS2_RC_SUCCESS);
    assert_int_equal (tcti_size, sizeof (TSS2_TCTI_CMD_CONTEXT));
}

static void
tcti_cmd_test_pipe_1_fail (void **state)
{
    uint8_t buf[4096];
    size_t tcti_size = sizeof (buf);
    TSS2_TCTI_CONTEXT *tcti_context = (TSS2_TCTI_CONTEXT *)buf;

    will_return (tcti_cmd_pipe, EFAULT);

    TSS2_RC rval = Tss2_Tcti_Cmd_Init (tcti_context, &tcti_size, __func__);
    assert_int_equal (rval, TSS2_TCTI_RC_GENERAL_FAILURE);
}

static void
tcti_cmd_test_pipe_2_fail (void **state)
{
    uint8_t buf[4096];
    size_t tcti_size = sizeof (buf);
    TSS2_TCTI_CONTEXT *tcti_context = (TSS2_TCTI_CONTEXT *)buf;

    /* first pipe works, second pipe fails */
    will_return (tcti_cmd_pipe, 0);
    will_return (tcti_cmd_pipe, EFAULT);

    TSS2_RC rval = Tss2_Tcti_Cmd_Init (tcti_context, &tcti_size, __func__);
    assert_int_equal (rval, TSS2_TCTI_RC_GENERAL_FAILURE);
}

static void
tcti_cmd_test_fork_fail (void **state)
{
    uint8_t buf[4096];
    size_t tcti_size = sizeof (buf);
    TSS2_TCTI_CONTEXT *tcti_context = (TSS2_TCTI_CONTEXT *)buf;

    will_return_always (tcti_cmd_pipe, 0);
    will_return_always (tcti_cmd_sigprocmask, 0);

    will_return (tcti_cmd_fork, ENOMEM);

    TSS2_RC rval = Tss2_Tcti_Cmd_Init (tcti_context, &tcti_size, __func__);
    assert_int_equal (rval, TSS2_TCTI_RC_GENERAL_FAILURE);
}

static void
tcti_cmd_test_fdopen_1_fail (void **state)
{
    uint8_t buf[4096];
    size_t tcti_size = sizeof (buf);
    TSS2_TCTI_CONTEXT *tcti_context = (TSS2_TCTI_CONTEXT *)buf;

    will_return_always (tcti_cmd_pipe, 0);
    will_return_always (tcti_cmd_fork, 0);
    will_return_always (tcti_cmd_sigprocmask, 0);

    will_return (tcti_cmd_fdopen, EINVAL);

    TSS2_RC rval = Tss2_Tcti_Cmd_Init (tcti_context, &tcti_size, __func__);
    assert_int_equal (rval, TSS2_TCTI_RC_GENERAL_FAILURE);
}

static void
tcti_cmd_test_fdopen_2_fail (void **state)
{
    uint8_t buf[4096];
    size_t tcti_size = sizeof (buf);
    TSS2_TCTI_CONTEXT *tcti_context = (TSS2_TCTI_CONTEXT *)buf;

    will_return_always (tcti_cmd_pipe, 0);
    will_return_always (tcti_cmd_fork, 0);
    will_return_always (tcti_cmd_sigprocmask, 0);

    /* first fdopen works, second fails */
    will_return (tcti_cmd_fdopen, 0);
    will_return (tcti_cmd_fdopen, EINVAL);

    TSS2_RC rval = Tss2_Tcti_Cmd_Init (tcti_context, &tcti_size, __func__);
    assert_int_equal (rval, TSS2_TCTI_RC_GENERAL_FAILURE);
}

static void
tcti_cmd_test_sigprocmask_1_fail (void **state)
{
    uint8_t buf[4096];
    size_t tcti_size = sizeof (buf);
    TSS2_TCTI_CONTEXT *tcti_context = (TSS2_TCTI_CONTEXT *)buf;

    will_return_always (tcti_cmd_pipe, 0);

    will_return (tcti_cmd_sigprocmask, EINVAL);

    TSS2_RC rval = Tss2_Tcti_Cmd_Init (tcti_context, &tcti_size, __func__);
    assert_int_equal (rval, TSS2_TCTI_RC_GENERAL_FAILURE);
}

static void
tcti_cmd_test_good (void **state)
{
    will_return_always (tcti_cmd_fwrite, 0);
    will_return_always (tcti_cmd_ferror, 0);

    TSS2_TCTI_CONTEXT *tcti_context = *state =
            test_common_setup (EXECLP_CMD" good");
    assert_non_null (tcti_context);

    /* send the command buffer */
    TSS2_RC rval = Tss2_Tcti_Transmit (tcti_context,
            sizeof (getcap_command), getcap_command);
    assert_int_equal (rval, TSS2_RC_SUCCESS);

    uint8_t rbuf[sizeof (getcap_good_resp)];
    size_t rsize = sizeof (rbuf);

    /* get the valid response */
    rval = Tss2_Tcti_Receive (tcti_context, &rsize, rbuf,
            TSS2_TCTI_TIMEOUT_BLOCK);
    assert_int_equal (rval, TSS2_RC_SUCCESS);

    /* Should be the expected getcap good response */
    assert_int_equal (rsize, sizeof (getcap_good_resp));
    assert_memory_equal (rbuf, getcap_good_resp, rsize);
}

static void
tcti_cmd_test_malformed_size_smaller (void **state)
{
    will_return_always (tcti_cmd_fwrite, 0);
    will_return_always (tcti_cmd_ferror, 0);

    TSS2_TCTI_CONTEXT *tcti_context = *state =
            test_common_setup (EXECLP_CMD" smaller");
    assert_non_null (tcti_context);

    /* send the command buffer */
    TSS2_RC rval = Tss2_Tcti_Transmit (tcti_context,
            sizeof (getcap_command), getcap_command);
    assert_int_equal (rval, TSS2_RC_SUCCESS);

    uint8_t rbuf[sizeof (getcap_good_resp)];
    size_t rsize = sizeof (rbuf);

    /* Attempt to receive a malformed response */
    rval = Tss2_Tcti_Receive (tcti_context, &rsize, rbuf,
            TSS2_TCTI_TIMEOUT_BLOCK);
    assert_int_equal (rval, TSS2_TCTI_RC_MALFORMED_RESPONSE);
}

static void
tcti_cmd_test_malformed_size_bigger (void **state)
{
    will_return_always (tcti_cmd_fwrite, 0);
    will_return_always (tcti_cmd_ferror, 0);

    TSS2_TCTI_CONTEXT *tcti_context = *state =
            test_common_setup (EXECLP_CMD" bigger");
    assert_non_null (tcti_context);

    /* send the command buffer */
    TSS2_RC rval = Tss2_Tcti_Transmit (tcti_context,
            sizeof (getcap_command), getcap_command);
    assert_int_equal (rval, TSS2_RC_SUCCESS);

    uint8_t rbuf[sizeof (getcap_good_resp)];
    size_t rsize = sizeof (rbuf);

    /*
     * Attempt to receive a malformed response with command header size
     * larger than buffer size.
     */
    rval = Tss2_Tcti_Receive (tcti_context, &rsize, rbuf,
            TSS2_TCTI_TIMEOUT_BLOCK);
    assert_int_equal (rval, TSS2_TCTI_RC_MALFORMED_RESPONSE);
}

static void
tcti_cmd_test_transmit_fail (void **state)
{
    will_return_always (tcti_cmd_fwrite, EBADF);

    TSS2_TCTI_CONTEXT *tcti_context = *state =
            test_common_setup (EXECLP_CMD" good");
    assert_non_null (tcti_context);

    /* send the command buffer */
    TSS2_RC rval = Tss2_Tcti_Transmit (tcti_context,
            sizeof (getcap_command), getcap_command);
    assert_int_equal (rval, TSS2_TCTI_RC_IO_ERROR);

    uint8_t rbuf[sizeof (getcap_good_resp)];
    size_t rsize = sizeof (rbuf);

    /*
     * Attempt to receive a response in the wrong state
     */
    rval = Tss2_Tcti_Receive (tcti_context, &rsize, rbuf,
            TSS2_TCTI_TIMEOUT_BLOCK);
    assert_int_equal (rval, TSS2_TCTI_RC_BAD_SEQUENCE);
}

static void
tcti_cmd_test_set_locality (void **state)
{
    TSS2_TCTI_CONTEXT *tcti_context = *state =
            test_common_setup (EXECLP_CMD" good");
    assert_non_null (tcti_context);

    /* send the command buffer */
    TSS2_RC rval = Tss2_Tcti_SetLocality (tcti_context, 42);
    assert_int_equal (rval, TSS2_TCTI_RC_NOT_IMPLEMENTED);
}

static void
tcti_cmd_test_cancel (void **state)
{
    TSS2_TCTI_CONTEXT *tcti_context = *state =
            test_common_setup (EXECLP_CMD" good");
    assert_non_null (tcti_context);

    /* send the command buffer */
    TSS2_RC rval = Tss2_Tcti_Cancel (tcti_context);
    assert_int_equal (rval, TSS2_TCTI_RC_NOT_IMPLEMENTED);
}

static void
tcti_cmd_test_get_poll_handles_ok (void **state)
{
    TSS2_TCTI_CONTEXT *tcti_context = *state =
            test_common_setup (EXECLP_CMD" good");
    assert_non_null (tcti_context);

    size_t num_of_handles = 1;
    TSS2_TCTI_POLL_HANDLE poll_handle;

    /* send the command buffer */
    TSS2_RC rval = Tss2_Tcti_GetPollHandles (tcti_context, &poll_handle, &num_of_handles);
    assert_int_equal (rval, TSS2_RC_SUCCESS);
    assert_int_equal(num_of_handles, 1);
}

static void
tcti_cmd_test_get_info (void **state)
{
    TSS2_TCTI_CONTEXT *tcti_context = *state =
            test_common_setup (EXECLP_CMD" good");
    assert_non_null (tcti_context);

    const TSS2_TCTI_INFO *info = Tss2_Tcti_Info ();
    assert_non_null (info);
    assert_int_equal (info->version, TCTI_VERSION);
    assert_int_equal (info->init, Tss2_Tcti_Cmd_Init);

    assert_string_equal (info->name, TCTI_CMD_NAME);
    assert_string_equal (info->description, TCTI_CMD_DESCRIPTION);
    assert_string_equal (info->config_help, TCTI_CMD_HELP);
}

int
main (int   argc,
      char *argv[])
{
    const struct CMUnitTest tests[] = {
        /*
         * Tests that do not require the setup and teardown routine as they
         * don't fork successfully
         */
        cmocka_unit_test (tcti_cmd_init_all_null_test),
        cmocka_unit_test (tcti_cmd_init_size_test),
        cmocka_unit_test (tcti_cmd_test_pipe_1_fail),
        cmocka_unit_test (tcti_cmd_test_pipe_2_fail),
        cmocka_unit_test (tcti_cmd_test_fork_fail),
        cmocka_unit_test (tcti_cmd_test_fdopen_1_fail),
        cmocka_unit_test (tcti_cmd_test_fdopen_2_fail),
        cmocka_unit_test (tcti_cmd_test_sigprocmask_1_fail),
        /*
         * Tests that **do** require a teardown routine as they
         * **do** fork/exec successfully and thus get a TCTI_CONTEXT
         */
        cmocka_unit_test_teardown (
            tcti_cmd_test_good,
            test_teardown),
        cmocka_unit_test_teardown (
            tcti_cmd_test_malformed_size_smaller,
            test_teardown),
        cmocka_unit_test_teardown (
            tcti_cmd_test_malformed_size_bigger,
            test_teardown),
        cmocka_unit_test_teardown (
            tcti_cmd_test_transmit_fail,
            test_teardown),
        cmocka_unit_test_teardown (
            tcti_cmd_test_set_locality,
            test_teardown),
        cmocka_unit_test_teardown (
            tcti_cmd_test_cancel,
            test_teardown),
        cmocka_unit_test_teardown (
            tcti_cmd_test_get_poll_handles_ok,
            test_teardown),
        cmocka_unit_test_teardown (
            tcti_cmd_test_get_info,
            test_teardown),
    };

    return cmocka_run_group_tests (tests, NULL, NULL);
}
