/*
 * SPDX-License-Identifier: BSD-2-Clause
 * Copyright 2019, Intel Corporation
 */

#include <errno.h>
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

static char* name_dup = "name_dup";
static char* description_dup = "description_dup";
static char* config_help_dup = "config_help_dup";

static TSS2_TCTI_INFO info_src = {
    .version = 1,
    .name = "name",
    .description = "description",
    .config_help = "config_help",
};
static TSS2_TCTI_INFO info_dst = { 0, };

char*
__real_strndup (const char *s, size_t n);
char*
__wrap_strndup (const char *s,
                size_t n)
{
    if (s == info_src.name || \
        s == info_src.description || \
        s == info_src.config_help)
    {
        printf("%s: got known string\n", __func__);
        errno = mock_type (int);
        return mock_type (char*);
    } else {
        return __real_strndup (s, n);
    }
}

void __real_free (void *ptr);
void
__wrap_free (void *ptr)
{
    printf("%s: %p\n", __func__, ptr);
    if (ptr == name_dup || \
        ptr == description_dup || \
        ptr == config_help_dup || \
        ptr == &info_dst)
    {
        printf("%s: got known memory\n", __func__);
        return;
    } else {
        printf("%s: real free\n", __func__);
        return __real_free (ptr);
    }
}
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

static void
copyinfo_null_params (void **state)
{
    TSS2_RC rc = copy_info (NULL, NULL);
    assert_int_equal (rc, TSS2_TCTI_RC_BAD_REFERENCE);
}
static void
copyinfo_strndup1_fail (void **state)
{
    TSS2_TCTI_INFO info_dst = { 0, };
    will_return (__wrap_strndup, ENOMEM);
    will_return (__wrap_strndup, NULL);
    TSS2_RC rc = copy_info (&info_src, &info_dst);
    assert_int_equal (rc, TSS2_TCTI_RC_GENERAL_FAILURE);
}
static void
copyinfo_strndup2_fail (void **state)
{
    TSS2_TCTI_INFO info_dst = { 0, };
    will_return (__wrap_strndup, 0);
    will_return (__wrap_strndup, name_dup);
    will_return (__wrap_strndup, ENOMEM);
    will_return (__wrap_strndup, NULL);
    TSS2_RC rc = copy_info (&info_src, &info_dst);
    assert_int_equal (rc, TSS2_TCTI_RC_GENERAL_FAILURE);
}
static void
copyinfo_strndup3_fail (void **state)
{
    TSS2_TCTI_INFO info_dst = { 0, };
    will_return (__wrap_strndup, 0);
    will_return (__wrap_strndup, name_dup);
    will_return (__wrap_strndup, 0);
    will_return (__wrap_strndup, description_dup);
    will_return (__wrap_strndup, ENOMEM);
    will_return (__wrap_strndup, NULL);
    TSS2_RC rc = copy_info (&info_src, &info_dst);
    assert_int_equal (rc, TSS2_TCTI_RC_GENERAL_FAILURE);
}
static void
copyinfo_success (void **state)
{
    TSS2_TCTI_INFO info_dst = { 0, };
    will_return (__wrap_strndup, 0);
    will_return (__wrap_strndup, name_dup);
    will_return (__wrap_strndup, 0);
    will_return (__wrap_strndup, description_dup);
    will_return (__wrap_strndup, 0);
    will_return (__wrap_strndup, config_help_dup);
    TSS2_RC rc = copy_info (&info_src, &info_dst);
    assert_int_equal (rc, TSS2_RC_SUCCESS);
    assert_string_equal (info_dst.name, name_dup);
    assert_string_equal (info_dst.description, description_dup);
    assert_string_equal (info_dst.config_help, config_help_dup);
}
static void
getinfo_null_info (void **state)
{
    TSS2_RC rc = Tss2_TctiLdr_GetInfo (NULL, NULL);
    assert_int_equal (rc, TSS2_TCTI_RC_BAD_REFERENCE);
}
TSS2_RC
__wrap_handle_from_name(const char *file,
                        void **handle)
{
    printf ("%s\n", __func__);
    *handle = mock_type (void*);
    return mock_type (TSS2_RC);
}
const TSS2_TCTI_INFO*
__wrap_info_from_handle (void *dlhandle)
{
    printf ("%s\n", __func__);
    return mock_type (const TSS2_TCTI_INFO*);
}
TSS2_RC
__wrap_get_tcti_default(TSS2_TCTI_CONTEXT ** tcticontext, void **dlhandle)
{
    printf ("%s\n", __func__);
    return TSS2_RC_SUCCESS;
}
TSS2_RC
__wrap_tcti_from_file(const char *file,
               const char* conf,
               TSS2_TCTI_CONTEXT **tcti,
               void **dlhandle)
{
    printf ("%s\n", __func__);
    return TSS2_RC_SUCCESS;
}
#define TEST_HANDLE (void*)666
#define HANDLE_FROM_NAME_FAIL_RC (TSS2_RC)574567392
void
__wrap_dlclose (void *handle)
{
    if (handle == TEST_HANDLE) {
        printf ("%s got TEST_HANDLE\n", __func__);
        return;
    } else {
        printf ("%s got unexpected handle\n", __func__);
        return;
    }
}
TSS2_RC
__wrap_get_info_default (TSS2_TCTI_INFO **info,
                         void **dlhandle)
{
    printf ("%s\n", __func__);
    if (*info == &info_src) {
        *dlhandle = mock_type (void*);
        return mock_type (TSS2_RC);
    } else {
        printf ("%s: this shouldn't happen", __func__);
        assert_true(1);
        return 1;
    }
}
#define TCTI_NAME "foo"
static void
getinfo_get_info_fail (void **state)
{
    TSS2_TCTI_INFO *info = NULL;
    will_return (__wrap_tctildr_get_info, HANDLE_FROM_NAME_FAIL_RC);
    TSS2_RC rc = Tss2_TctiLdr_GetInfo (TCTI_NAME, &info);
    assert_int_equal (rc, HANDLE_FROM_NAME_FAIL_RC);
}
void*
__wrap_calloc(size_t nmemb, size_t size)
{
    printf("%s\n", __func__);
    return mock_type (void*);
}
#define TEST_DATA (void*)0xabcdef999
static void
getinfo_calloc_fail (void **state)
{
    TSS2_TCTI_INFO *info = NULL;
    will_return (__wrap_tctildr_get_info, TSS2_RC_SUCCESS);
    will_return (__wrap_tctildr_get_info, &info_src);
    will_return (__wrap_tctildr_get_info, TEST_DATA);
    will_return (__wrap_calloc, NULL);
    TSS2_RC rc = Tss2_TctiLdr_GetInfo (TCTI_NAME, &info);
    assert_int_equal (rc, TSS2_TCTI_RC_GENERAL_FAILURE);
}
static void
getinfo_copy_info_fail (void **state)
{
    TSS2_TCTI_INFO *info = NULL;
    printf ("%s: pointer %p\n", __func__, &info_dst);
    will_return (__wrap_tctildr_get_info, TSS2_RC_SUCCESS);
    will_return (__wrap_tctildr_get_info, &info_src);
    will_return (__wrap_tctildr_get_info, TEST_DATA);
    will_return (__wrap_calloc, &info_dst);
    will_return (__wrap_strndup, ENOMEM);
    will_return (__wrap_strndup, NULL);
    TSS2_RC rc = Tss2_TctiLdr_GetInfo (TCTI_NAME, &info);
    assert_int_equal (rc, TSS2_TCTI_RC_GENERAL_FAILURE);
}
static void
getinfo_success (void **state)
{
    TSS2_TCTI_INFO *info = NULL;
    will_return (__wrap_tctildr_get_info, TSS2_RC_SUCCESS);
    will_return (__wrap_tctildr_get_info, &info_src);
    will_return (__wrap_tctildr_get_info, TEST_DATA);
    will_return (__wrap_calloc, &info_dst);
    will_return (__wrap_strndup, 0);
    will_return (__wrap_strndup, name_dup);
    will_return (__wrap_strndup, 0);
    will_return (__wrap_strndup, description_dup);
    will_return (__wrap_strndup, 0);
    will_return (__wrap_strndup, config_help_dup);
    TSS2_RC rc = Tss2_TctiLdr_GetInfo (TCTI_NAME, &info);
    assert_int_equal (rc, TSS2_RC_SUCCESS);
}
static void
freeinfo_null (void **state)
{
    TSS2_TCTI_INFO *info = NULL;
    Tss2_TctiLdr_FreeInfo (&info);
    assert_null (info);
}
static void
freeinfo_success (void **state)
{
    TSS2_TCTI_INFO *info = &info_dst;
    Tss2_TctiLdr_FreeInfo (&info);
    assert_null (info);
}
int
main (int argc, char* arvg[])
{
    const struct CMUnitTest tests[] = {
        cmocka_unit_test (copyinfo_null_params),
        cmocka_unit_test (copyinfo_strndup1_fail),
        cmocka_unit_test (copyinfo_strndup2_fail),
        cmocka_unit_test (copyinfo_strndup3_fail),
        cmocka_unit_test (copyinfo_success),
        cmocka_unit_test (getinfo_null_info),
        cmocka_unit_test (getinfo_get_info_fail),
        cmocka_unit_test (getinfo_calloc_fail),
        cmocka_unit_test (getinfo_copy_info_fail),
        cmocka_unit_test (getinfo_success),
        cmocka_unit_test (freeinfo_null),
        cmocka_unit_test (freeinfo_success),
    };
    return cmocka_run_group_tests (tests, NULL, NULL);
}
