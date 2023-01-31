/*
 * SPDX-License-Identifier: BSD-2-Clause
 * Copyright 2018-2019, Intel Corporation
 */

#include <inttypes.h>
#include <limits.h>
#include <stdarg.h>
#include <stdbool.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#include <setjmp.h>
#include <cmocka.h>

#include "tss2_tcti.h"
#include "tss2_tctildr.h"

#include "tss2-tcti/tctildr.h"
#include "tss2-tcti/tcti-common.h"
#include "util/aux_util.h"

#define TEST_MAGIC 0x1234321
#define TEST_VERSION 2

TSS2_RC
__wrap_tctildr_get_info (const char *name,
                         const TSS2_TCTI_INFO **info,
                         void **data)
{
    TSS2_RC rc = mock_type (TSS2_RC);
    if (rc == TSS2_RC_SUCCESS) {
        *info = mock_type (TSS2_TCTI_INFO*);
        *data = mock_type (void*);
    }
    return rc;
}
TSS2_RC
__wrap_tctildr_get_tcti (const char *name,
                  const char* conf,
                  TSS2_TCTI_CONTEXT **tcti,
                  void **data)
{
    TSS2_RC rc = mock_type (TSS2_RC);
    if (rc == TSS2_RC_SUCCESS) {
        *tcti= mock_type (TSS2_TCTI_CONTEXT*);
        *data = mock_type (void*);
    }
    return rc;
}
void __wrap_tctildr_finalize_data (void **data) {}

static TSS2_RC
tctildr_mock_transmit (TSS2_TCTI_CONTEXT *context,
                       size_t size,
                       uint8_t const *command)
{
    return mock_type (TSS2_RC);
}
TSS2_RC
tctildr_mock_receive (TSS2_TCTI_CONTEXT *context,
                      size_t *size,
                      uint8_t *response,
                      int32_t timeout)
{
    return mock_type (TSS2_RC);
}
TSS2_RC
tctildr_mock_cancel (TSS2_TCTI_CONTEXT *context)
{
    return mock_type (TSS2_RC);
}
TSS2_RC
tctildr_mock_get_poll_handles (TSS2_TCTI_CONTEXT *context,
                               TSS2_TCTI_POLL_HANDLE *handles,
                               size_t *num_handles)
{
    return mock_type (TSS2_RC);
}
TSS2_RC
tctildr_mock_set_locality (TSS2_TCTI_CONTEXT *context,
                           uint8_t locality)
{
    return mock_type (TSS2_RC);
}
TSS2_RC
tctildr_mock_make_sticky (TSS2_TCTI_CONTEXT *context,
                          TPM2_HANDLE *handle,
                          uint8_t sticky)
{
    return mock_type (TSS2_RC);
}
#define TSS2_TCTI_MOCK_CONTEXT TSS2_TCTI_CONTEXT_COMMON_V2
#define TEST_TCTI_HANDLE (TSS2_TCTI_LIBRARY_HANDLE)0x9827635
static int
tctildr_setup (void **state)
{
    TSS2_TCTILDR_CONTEXT *ldr_ctx;
    TSS2_TCTI_MOCK_CONTEXT *tmp;

    ldr_ctx  = calloc (1, sizeof (TSS2_TCTILDR_CONTEXT));
    TSS2_TCTI_MAGIC (ldr_ctx) = TCTILDR_MAGIC;
    TSS2_TCTI_VERSION (ldr_ctx) = TCTI_VERSION;
    TSS2_TCTI_TRANSMIT (ldr_ctx) = tctildr_transmit;
    TSS2_TCTI_RECEIVE (ldr_ctx) = tctildr_receive;
    TSS2_TCTI_CANCEL (ldr_ctx) = tctildr_cancel;
    TSS2_TCTI_GET_POLL_HANDLES (ldr_ctx) = tctildr_get_poll_handles;
    TSS2_TCTI_SET_LOCALITY (ldr_ctx) = tctildr_set_locality;
    TSS2_TCTI_MAKE_STICKY (ldr_ctx) = tctildr_make_sticky;
    ldr_ctx->library_handle = TEST_TCTI_HANDLE;

    tmp = calloc (1, sizeof (TSS2_TCTI_MOCK_CONTEXT));
    ldr_ctx->tcti = (TSS2_TCTI_CONTEXT*)tmp;
    TSS2_TCTI_MAGIC (ldr_ctx->tcti) = TEST_MAGIC;
    TSS2_TCTI_VERSION (ldr_ctx->tcti) = TEST_VERSION;
    TSS2_TCTI_TRANSMIT (ldr_ctx->tcti) = tctildr_mock_transmit;
    TSS2_TCTI_RECEIVE (ldr_ctx->tcti) = tctildr_mock_receive;
    TSS2_TCTI_CANCEL (ldr_ctx->tcti) = tctildr_mock_cancel;
    TSS2_TCTI_GET_POLL_HANDLES (ldr_ctx->tcti) = tctildr_mock_get_poll_handles;
    TSS2_TCTI_SET_LOCALITY (ldr_ctx->tcti) = tctildr_mock_set_locality;
    TSS2_TCTI_MAKE_STICKY (ldr_ctx->tcti) = tctildr_mock_make_sticky;

    *state = ldr_ctx;

    return 0;
}
static int
tctildr_teardown (void **state)
{
    TSS2_TCTI_CONTEXT *context = (TSS2_TCTI_CONTEXT*)*state;

    tctildr_finalize (context);

    free (context);

    return 0;
}
static void
tctildr_transmit_test (void **state)
{
    TSS2_RC rc;
    TSS2_TCTI_CONTEXT *context = (TSS2_TCTI_CONTEXT*)*state;
    uint8_t buffer [64] = { 0 };
    size_t size = sizeof (buffer);

    will_return (tctildr_mock_transmit, TSS2_RC_SUCCESS);
    rc = Tss2_Tcti_Transmit (context, size, buffer);
    assert_int_equal (rc, TSS2_RC_SUCCESS);
}
static void
tctildr_transmit_null_test (void **state)
{
    TSS2_RC rc;
    uint8_t buffer [64] = { 0 };
    size_t size = sizeof (buffer);

    rc = tctildr_transmit (NULL, size, buffer);
    assert_int_equal (rc, TSS2_TCTI_RC_BAD_REFERENCE);
}
static void
tctildr_receive_test (void **state)
{
    TSS2_RC rc;
    TSS2_TCTI_CONTEXT *context = (TSS2_TCTI_CONTEXT*)*state;
    uint8_t buffer [64] = { 0 };
    size_t size = sizeof (buffer);
    int32_t timeout = TSS2_TCTI_TIMEOUT_BLOCK;

    will_return (tctildr_mock_receive, TSS2_RC_SUCCESS);
    rc = Tss2_Tcti_Receive (context, &size, buffer, timeout);
    assert_int_equal (rc, TSS2_RC_SUCCESS);
}
static void
tctildr_receive_null_test (void **state)
{
    TSS2_RC rc;
    uint8_t buffer [64] = { 0 };
    size_t size = sizeof (buffer);
    int32_t timeout = TSS2_TCTI_TIMEOUT_BLOCK;

    rc = tctildr_receive (NULL, &size, buffer, timeout);
    assert_int_equal (rc, TSS2_TCTI_RC_BAD_REFERENCE);
}
static void
tctildr_cancel_test (void **state)
{
    TSS2_RC rc;
    TSS2_TCTI_CONTEXT *context = (TSS2_TCTI_CONTEXT*)*state;

    will_return (tctildr_mock_cancel, TSS2_RC_SUCCESS);
    rc = Tss2_Tcti_Cancel (context);
    assert_int_equal (rc, TSS2_RC_SUCCESS);
}
static void
tctildr_cancel_null_test (void **state)
{
    TSS2_RC rc;
    UNUSED (state);

    rc = tctildr_cancel (NULL);
    assert_int_equal (rc, TSS2_TCTI_RC_BAD_REFERENCE);
}
#define TEST_NUM_HANDLES 3
static void
tctildr_get_poll_handles_test (void **state)
{
    TSS2_RC rc;
    TSS2_TCTI_CONTEXT *context = (TSS2_TCTI_CONTEXT*)*state;
    TSS2_TCTI_POLL_HANDLE handles [TEST_NUM_HANDLES] = { 0 };
    size_t num_handles = sizeof (handles);

    will_return (tctildr_mock_get_poll_handles, TSS2_RC_SUCCESS);
    rc = Tss2_Tcti_GetPollHandles (context, handles, &num_handles);
    assert_int_equal (rc, TSS2_RC_SUCCESS);
}
static void
tctildr_get_poll_handles_null_test (void **state)
{
    TSS2_RC rc;
    TSS2_TCTI_POLL_HANDLE handles [TEST_NUM_HANDLES] = { 0 };
    size_t num_handles = sizeof (handles);

    rc = tctildr_get_poll_handles (NULL, handles, &num_handles);
    assert_int_equal (rc, TSS2_TCTI_RC_BAD_REFERENCE);
}
static void
tctildr_set_locality_test (void **state)
{
    TSS2_RC rc;
    TSS2_TCTI_CONTEXT *context = (TSS2_TCTI_CONTEXT*)*state;

    will_return (tctildr_mock_set_locality, TSS2_RC_SUCCESS);
    rc = Tss2_Tcti_SetLocality (context, 1);
    assert_int_equal (rc, TSS2_RC_SUCCESS);
}
static void
tctildr_set_locality_null_test (void **state)
{
    TSS2_RC rc;
    UNUSED (state);

    rc = tctildr_set_locality (NULL, 1);
    assert_int_equal (rc, TSS2_TCTI_RC_BAD_REFERENCE);
}
#define TEST_HANDLE 0x1
static void
tctildr_make_sticky_test (void **state)
{
    TSS2_RC rc;
    TSS2_TCTI_CONTEXT *context = (TSS2_TCTI_CONTEXT*)*state;
    TPM2_HANDLE handle = TEST_HANDLE;

    will_return (tctildr_mock_make_sticky, TSS2_RC_SUCCESS);
    rc = Tss2_Tcti_MakeSticky (context, &handle, TPM2_YES);
    assert_int_equal (rc, TSS2_RC_SUCCESS);
}
static void
tctildr_make_sticky_null_test (void **state)
{
    TSS2_RC rc;
    TPM2_HANDLE handle = TEST_HANDLE;
    UNUSED (state);

    rc = tctildr_make_sticky (NULL, &handle, TPM2_YES);
    assert_int_equal (rc, TSS2_TCTI_RC_BAD_REFERENCE);
}
/*
 * This test covers the 'sanity test' path in the tctildr finalize
 * function. There's not really a way to check whether or not this test
 * passes / does what's intended beyond checking the report from the code
 * coverage tool.
 */
static void
tctildr_finalize_null_ctx_test (void **state)
{
    TSS2_TCTI_CONTEXT *context = NULL;
    tctildr_finalize (context);
    assert_true (true);
}
int
main (int argc, char* arvg[])
{
    const struct CMUnitTest tests[] = {
        cmocka_unit_test_setup_teardown (tctildr_transmit_test,
                                         tctildr_setup,
                                         tctildr_teardown),
        cmocka_unit_test_setup_teardown (tctildr_transmit_null_test,
                                         tctildr_setup,
                                         tctildr_teardown),
        cmocka_unit_test_setup_teardown (tctildr_receive_test,
                                         tctildr_setup,
                                         tctildr_teardown),
        cmocka_unit_test_setup_teardown (tctildr_receive_null_test,
                                         tctildr_setup,
                                         tctildr_teardown),
        cmocka_unit_test_setup_teardown (tctildr_cancel_test,
                                         tctildr_setup,
                                         tctildr_teardown),
        cmocka_unit_test_setup_teardown (tctildr_cancel_null_test,
                                         tctildr_setup,
                                         tctildr_teardown),
        cmocka_unit_test_setup_teardown (tctildr_get_poll_handles_test,
                                         tctildr_setup,
                                         tctildr_teardown),
        cmocka_unit_test_setup_teardown (tctildr_get_poll_handles_null_test,
                                         tctildr_setup,
                                         tctildr_teardown),
        cmocka_unit_test_setup_teardown (tctildr_set_locality_test,
                                         tctildr_setup,
                                         tctildr_teardown),
        cmocka_unit_test_setup_teardown (tctildr_set_locality_null_test,
                                         tctildr_setup,
                                         tctildr_teardown),
        cmocka_unit_test_setup_teardown (tctildr_make_sticky_test,
                                         tctildr_setup,
                                         tctildr_teardown),
        cmocka_unit_test_setup_teardown (tctildr_make_sticky_null_test,
                                         tctildr_setup,
                                         tctildr_teardown),
        cmocka_unit_test (tctildr_finalize_null_ctx_test),
    };
    return cmocka_run_group_tests (tests, NULL, NULL);
}
