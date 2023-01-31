/*
 * SPDX-License-Identifier: BSD-2-Clause
 * Copyright 2019, Intel Corporation
 */

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <limits.h>
#include <stdio.h>
#include <stddef.h>
#include <stdlib.h>
#include <string.h>

#include <setjmp.h>
#include <cmocka.h>

#include "tss2_tctildr.h"
#include "tss2_tcti.h"
#include "tss2-tcti/tctildr.h"

static TSS2_TCTI_CONTEXT_COMMON_V2 tcti_ctx = { 0, };
static TSS2_TCTILDR_CONTEXT tctildr_ctx = { 0, };

TSS2_RC
local_init (
    TSS2_TCTI_CONTEXT *tctiContext,
    size_t *size,
    const char *config)
{
    *size = mock_type (size_t);
    return mock_type (TSS2_RC);
}

void
tcti_from_init_null_init (void **state)
{
    TSS2_RC rc = tcti_from_init (NULL, NULL, NULL);
    assert_int_equal (rc, TSS2_TCTI_RC_BAD_REFERENCE);
}

#define TEST_MAGIC_SIZE (size_t)5513444
#define TEST_INIT_RC_FAIL (TSS2_RC)0x6134
void
tcti_from_init_init_fail (void **state)
{
    will_return(local_init, TEST_MAGIC_SIZE);
    will_return(local_init, TEST_INIT_RC_FAIL);
    TSS2_TCTI_CONTEXT *tcti_ctx = NULL;
    TSS2_RC rc = tcti_from_init (local_init, NULL, &tcti_ctx);
    assert_int_equal (rc, TEST_INIT_RC_FAIL);
}

void* __real_calloc (size_t nmemb, size_t size);
void*
__wrap_calloc (size_t nmemb, size_t size)
{
    if (size == TEST_MAGIC_SIZE || size == sizeof (TSS2_TCTILDR_CONTEXT))
        return mock_type (void*);
    else
        return __real_calloc (nmemb, size);
}
void __real_free (void *ptr);
void
__wrap_free (void *ptr)
{
    if (ptr != &tcti_ctx && ptr != &tctildr_ctx)
        __real_free (ptr);
    return;
}
TSS2_RC
__wrap_tctildr_get_info (const char *name,
                         const TSS2_TCTI_INFO **info,
                         void **data)
{
    return TSS2_RC_SUCCESS;
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
void __wrap_tctildr_finalize_data (void **data){}

void
tcti_from_init_calloc_fail (void **state)
{
    will_return(local_init, TEST_MAGIC_SIZE);
    will_return(local_init, TSS2_RC_SUCCESS);
    TSS2_TCTI_CONTEXT *tcti_ctx = NULL;
    will_return(__wrap_calloc, NULL);
    TSS2_RC rc = tcti_from_init (local_init, NULL, &tcti_ctx);
    assert_int_equal (rc, TSS2_ESYS_RC_MEMORY);
}
void
tcti_from_init_second_init_fail (void **state)
{
    will_return(local_init, TEST_MAGIC_SIZE);
    will_return(local_init, TSS2_RC_SUCCESS);
    TSS2_TCTI_CONTEXT *tcti_ctx_ptr = NULL;
    will_return(__wrap_calloc, &tcti_ctx);
    will_return(local_init, TEST_MAGIC_SIZE);
    will_return(local_init, TEST_INIT_RC_FAIL);
    TSS2_RC rc = tcti_from_init (local_init, NULL, &tcti_ctx_ptr);
    assert_int_equal (rc, TEST_INIT_RC_FAIL);
}

void
tcti_from_init_success (void **state)
{
    will_return(local_init, TEST_MAGIC_SIZE);
    will_return(local_init, TSS2_RC_SUCCESS);
    TSS2_TCTI_CONTEXT *tcti_ctx_ptr = NULL;
    will_return(__wrap_calloc, &tcti_ctx);
    will_return(local_init, TEST_MAGIC_SIZE);
    will_return(local_init, TSS2_RC_SUCCESS);
    TSS2_RC rc = tcti_from_init (local_init, NULL, &tcti_ctx_ptr);
    assert_int_equal (rc, TSS2_RC_SUCCESS);
}
TSS2_TCTI_INFO info = { .init = local_init, };
const TSS2_TCTI_INFO*
local_info (void)
{
    return mock_type (const TSS2_TCTI_INFO*);
}
void
tcti_from_info_info_null (void **state)
{
    TSS2_TCTI_CONTEXT *tcti_ctx_ptr = NULL;

    will_return (local_info, NULL);
    TSS2_RC rc = tcti_from_info (local_info, NULL, &tcti_ctx_ptr);
    assert_int_equal (rc, TSS2_ESYS_RC_GENERAL_FAILURE);
}
void
tcti_from_info_info_fail (void **state)
{
    TSS2_TCTI_CONTEXT *tcti_ctx_ptr = NULL;

    will_return (local_info, &info);
    will_return(local_init, TEST_MAGIC_SIZE);
    will_return(local_init, TEST_INIT_RC_FAIL);
    TSS2_RC rc = tcti_from_info (local_info, NULL, &tcti_ctx_ptr);
    assert_int_equal (rc, TEST_INIT_RC_FAIL);
}
void
tcti_from_info_success (void **state)
{
    TSS2_TCTI_CONTEXT *tcti_ctx_ptr = NULL;

    will_return (local_info, &info);
    will_return(local_init, TEST_MAGIC_SIZE);
    will_return(local_init, TSS2_RC_SUCCESS);
    will_return(__wrap_calloc, &tcti_ctx);
    will_return(local_init, TEST_MAGIC_SIZE);
    will_return(local_init, TSS2_RC_SUCCESS);
    TSS2_RC rc = tcti_from_info (local_info, NULL, &tcti_ctx_ptr);
    assert_int_equal (rc, TSS2_RC_SUCCESS);
}
void
test_conf_parse_null (void **state)
{
    TSS2_RC rc = tctildr_conf_parse (NULL, NULL, NULL);
    assert_int_equal (rc, TSS2_TCTI_RC_BAD_REFERENCE);
}

void
test_conf_parse_bad_length (void **state)
{
    char name_buf[0], conf_buf[0];
    char name[PATH_MAX+1];
    memset(&name[0], 'a', sizeof(name));
    name[PATH_MAX] = '\0';
    TSS2_RC rc = tctildr_conf_parse (name, name_buf, conf_buf);
    assert_int_equal (rc, TSS2_TCTI_RC_BAD_VALUE);
}
void
test_conf_parse_empty_str (void **state)
{
    char name_buf[0], conf_buf[0];
    TSS2_RC rc = tctildr_conf_parse ("", name_buf, conf_buf);
    assert_int_equal (rc, TSS2_RC_SUCCESS);
}
void
test_conf_parse_no_colon (void **state)
{
    char name_buf[50] = { 0, }, conf_buf[50] = { 0, };
    TSS2_RC rc = tctildr_conf_parse ("foo", name_buf, conf_buf);
    assert_int_equal (rc, TSS2_RC_SUCCESS);
}
void
test_conf_parse_name_colon (void **state)
{
    char name_buf[50] = { 0, }, conf_buf[50] = { 0, };
    TSS2_RC rc = tctildr_conf_parse ("foo:", name_buf, conf_buf);
    assert_string_equal (name_buf, "foo");
    assert_int_equal (rc, TSS2_RC_SUCCESS);
}
void
test_conf_parse_name_colon_conf (void **state)
{
    char name_buf[50] = { 0, }, conf_buf[50] = { 0, };
    TSS2_RC rc = tctildr_conf_parse ("foo:bar", name_buf, conf_buf);
    assert_string_equal (name_buf, "foo");
    assert_string_equal (conf_buf, "bar");
    assert_int_equal (rc, TSS2_RC_SUCCESS);
}
/* tctildr init begin */
static void
tctildr_init_ex_null_test (void **state)
{
    TSS2_RC rc;

    rc = Tss2_TctiLdr_Initialize_Ex (NULL, NULL, NULL);
    assert_int_equal (rc, TSS2_TCTI_RC_BAD_VALUE);
}
static void
tctildr_init_null_test (void **state)
{
    TSS2_RC rc;

    rc = Tss2_TctiLdr_Initialize (NULL, NULL);
    assert_int_equal (rc, TSS2_TCTI_RC_BAD_VALUE);
}
static void
tctildr_init_conf_fail_test (void **state)
{
    TSS2_RC rc;
    char name[PATH_MAX+1];
    memset(&name[0], 'a', sizeof(name));
    name[PATH_MAX] = '\0';
    rc = Tss2_TctiLdr_Initialize (name, NULL);
    assert_int_equal (rc, TSS2_TCTI_RC_BAD_VALUE);
}
static void
tctildr_init_ex_default_fail (void **state)
{
    TSS2_RC rc;
    TSS2_TCTI_CONTEXT *context;

    will_return (__wrap_tctildr_get_tcti, TSS2_TCTI_RC_BAD_REFERENCE);
    rc = Tss2_TctiLdr_Initialize_Ex (NULL, NULL, &context);
    assert_int_equal (rc, TSS2_TCTI_RC_BAD_REFERENCE);
}
static void
tctildr_init_ex_from_file_fail (void **state)
{
    TSS2_RC rc;
    TSS2_TCTI_CONTEXT *context;

    will_return (__wrap_tctildr_get_tcti, TSS2_TCTI_RC_BAD_REFERENCE);
    rc = Tss2_TctiLdr_Initialize_Ex ("foo", NULL, &context);
    assert_int_equal (rc, TSS2_TCTI_RC_BAD_REFERENCE);
}
#define TEST_TCTI_HANDLE (TSS2_TCTI_LIBRARY_HANDLE)0x9827635
static void
tctildr_init_ex_calloc_fail_test (void **state)
{
    TSS2_RC rc;
    TSS2_TCTI_CONTEXT *ctx;

    will_return (__wrap_tctildr_get_tcti, TSS2_RC_SUCCESS);
    will_return (__wrap_tctildr_get_tcti, &tcti_ctx);
    will_return (__wrap_tctildr_get_tcti, TEST_TCTI_HANDLE);
    will_return (__wrap_calloc, NULL);

    rc = Tss2_TctiLdr_Initialize_Ex (NULL, NULL, &ctx);
    assert_int_equal (rc, TSS2_TCTI_RC_MEMORY);
}
static void
tctildr_init_ex_success_test (void **state)
{
    TSS2_RC rc;
    TSS2_TCTI_CONTEXT *ctx;

    will_return (__wrap_tctildr_get_tcti, TSS2_RC_SUCCESS);
    will_return (__wrap_tctildr_get_tcti, &tcti_ctx);
    will_return (__wrap_tctildr_get_tcti, TEST_TCTI_HANDLE);
    will_return (__wrap_calloc, &tctildr_ctx);

    rc = Tss2_TctiLdr_Initialize_Ex (NULL, NULL, &ctx);
    assert_int_equal (rc, TSS2_RC_SUCCESS);
}
static void
tctildr_finalize_null_ref_test (void **state)
{
    Tss2_TctiLdr_Finalize (NULL);
    assert_int_equal (1, 1);
}
static void
tctildr_finalize_null_ctx_test (void **state)
{
    TSS2_TCTI_CONTEXT *ctx = NULL;
    Tss2_TctiLdr_Finalize (&ctx);
    assert_int_equal (1, 1);
}
static void
tctildr_finalize_test (void **state)
{
    TSS2_TCTI_CONTEXT *ctx = (TSS2_TCTI_CONTEXT*)&tctildr_ctx;

    TSS2_TCTI_VERSION(&tctildr_ctx) = 3;
    tctildr_ctx.library_handle = TEST_TCTI_HANDLE;
    TSS2_TCTI_MAGIC(&tctildr_ctx) = TCTILDR_MAGIC;
    tctildr_ctx.tcti = (TSS2_TCTI_CONTEXT*)&tcti_ctx;
    Tss2_TctiLdr_Finalize (&ctx);
    assert_null (ctx);
}
/* tctildr init end */
int
main(void)
{
    const struct CMUnitTest tests[] = {
        cmocka_unit_test(tcti_from_init_null_init),
        cmocka_unit_test(tcti_from_init_init_fail),
        cmocka_unit_test(tcti_from_init_calloc_fail),
        cmocka_unit_test(tcti_from_init_second_init_fail),
        cmocka_unit_test(tcti_from_init_success),
        cmocka_unit_test(tcti_from_info_info_null),
        cmocka_unit_test(tcti_from_info_info_fail),
        cmocka_unit_test(tcti_from_info_success),
        cmocka_unit_test(test_conf_parse_null),
        cmocka_unit_test(test_conf_parse_bad_length),
        cmocka_unit_test(test_conf_parse_empty_str),
        cmocka_unit_test(test_conf_parse_no_colon),
        cmocka_unit_test(test_conf_parse_name_colon),
        cmocka_unit_test(test_conf_parse_name_colon_conf),
        cmocka_unit_test (tctildr_init_ex_null_test),
        cmocka_unit_test (tctildr_init_null_test),
        cmocka_unit_test (tctildr_init_conf_fail_test),
        cmocka_unit_test (tctildr_init_ex_default_fail),
        cmocka_unit_test (tctildr_init_ex_from_file_fail),
        cmocka_unit_test (tctildr_init_ex_calloc_fail_test),
        cmocka_unit_test (tctildr_init_ex_success_test),
        cmocka_unit_test (tctildr_finalize_null_ref_test),
        cmocka_unit_test (tctildr_finalize_null_ctx_test),
        cmocka_unit_test (tctildr_finalize_test),
    };
    return cmocka_run_group_tests (tests, NULL, NULL);
}
