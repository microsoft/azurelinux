/* SPDX-License-Identifier: BSD-2-Clause */
/*******************************************************************************
 * Copyright 2018, Fraunhofer SIT sponsored by Infineon Technologies AG
 * Copyright 2019, Intel Corporation
 * All rights reserved.
 *******************************************************************************/

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <stdio.h>
#include <stddef.h>
#include <stdlib.h>

#include <dlfcn.h>

#include <setjmp.h>
#include <cmocka.h>

#include "tss2_tcti.h"

#include "tss2-tcti/tctildr-interface.h"
#include "tss2-tcti/tctildr-dl.h"
#include "tss2-tcti/tctildr.h"
#define LOGMODULE test
#include "util/log.h"

/* global TCTI object, use to return reference from */
static TSS2_TCTI_CONTEXT_COMMON_V2 tcti_instance = { 0, };

void *
__wrap_dlopen(const char *filename, int flags)
{
    LOG_TRACE("Called with filename %s and flags %x", filename, flags);
    check_expected_ptr(filename);
    check_expected(flags);
    return mock_type(void *);
}

int
__wrap_dlclose(void *handle)
{
    LOG_TRACE("Called with handle %p", handle);
    check_expected_ptr(handle);
    return mock_type(int);
}

void *
__wrap_dlsym(void *handle, const char *symbol)
{
    LOG_TRACE("Called with handle %p and symbol %s", handle, symbol);
    check_expected_ptr(handle);
    check_expected_ptr(symbol);
    return mock_type(void *);
}

void *
__wrap___dlsym_time64(void *handle, const char *symbol)
{
    return __wrap_dlsym(handle, symbol);
}

TSS2_TCTI_INFO *
__wrap_Tss2_Tcti_Fake_Info(void)
{
    LOG_TRACE("Called.");
    return mock_type(TSS2_TCTI_INFO *);
}

TSS2_RC
__wrap_tcti_from_init(TSS2_TCTI_INIT_FUNC init,
                      const char* conf,
                      TSS2_TCTI_CONTEXT **tcti)
{
    printf("%s", __func__);
    return mock_type (TSS2_RC);
}
TSS2_RC
__wrap_tcti_from_info(TSS2_TCTI_INFO_FUNC infof,
                      const char* conf,
                      TSS2_TCTI_CONTEXT **tcti)
{
    check_expected (infof);
    check_expected (conf);
    check_expected (tcti);
    if (tcti != NULL)
        *tcti = mock_type (TSS2_TCTI_CONTEXT*);
    return mock_type (TSS2_RC);
}

#define TEST_HANDLE (void*)0xade0
static void
test_info_from_handle_null (void **state)
{
    const TSS2_TCTI_INFO* info = info_from_handle (NULL);
    assert_null (info);
}
static void
test_info_from_handle_dlsym_fail (void **state)
{
    expect_value(__wrap_dlsym, handle, TEST_HANDLE);
    expect_string(__wrap_dlsym, symbol, TSS2_TCTI_INFO_SYMBOL);
    will_return(__wrap_dlsym, NULL);

    const TSS2_TCTI_INFO* info = info_from_handle (TEST_HANDLE);
    assert_null (info);
}
static void
test_info_from_handle_success (void **state)
{
    TSS2_TCTI_INFO info_instance = { 0, };
    const TSS2_TCTI_INFO *info = { 0, };

    expect_value(__wrap_dlsym, handle, TEST_HANDLE);
    expect_string(__wrap_dlsym, symbol, TSS2_TCTI_INFO_SYMBOL);
    will_return(__wrap_dlsym, &__wrap_Tss2_Tcti_Fake_Info);

    will_return(__wrap_Tss2_Tcti_Fake_Info, &info_instance);

    info = info_from_handle (TEST_HANDLE);
    assert_ptr_equal (info, &info_instance);
}

static void
test_fail_null(void **state)
{
    TSS2_RC r = tctildr_get_default(NULL, NULL);
    assert_int_equal(r, TSS2_TCTI_RC_BAD_REFERENCE);
}

static void
test_handle_from_name_null_handle (void **state)
{
    TSS2_RC rc = handle_from_name (NULL, NULL);
    assert_int_equal (rc, TSS2_TCTI_RC_BAD_REFERENCE);
}
#define TEST_TCTI_NAME "test-tcti"
#define TEST_TCTI_CONF "test-conf"
static void
test_handle_from_name_first_dlopen_success (void **state)
{
    TSS2_RC rc;
    void *handle = NULL;

    expect_string(__wrap_dlopen, filename, TEST_TCTI_NAME);
    expect_value(__wrap_dlopen, flags, RTLD_NOW);
    will_return(__wrap_dlopen, TEST_HANDLE);

    rc = handle_from_name (TEST_TCTI_NAME, &handle);
    assert_int_equal (rc, TSS2_RC_SUCCESS);
    assert_int_equal (handle, TEST_HANDLE);
}

#define TEST_TCTI_NAME_SO_0 TCTI_PREFIX"-"TEST_TCTI_NAME""TCTI_SUFFIX_0
static void
test_handle_from_name_second_dlopen_success (void **state)
{
    TSS2_RC rc;
    void *handle = NULL;

    expect_string(__wrap_dlopen, filename, TEST_TCTI_NAME);
    expect_value(__wrap_dlopen, flags, RTLD_NOW);
    will_return(__wrap_dlopen, NULL);

    expect_string(__wrap_dlopen, filename, TEST_TCTI_NAME_SO_0);
    expect_value(__wrap_dlopen, flags, RTLD_NOW);
    will_return(__wrap_dlopen, TEST_HANDLE);

    rc = handle_from_name (TEST_TCTI_NAME, &handle);
    assert_int_equal (rc, TSS2_RC_SUCCESS);
    assert_int_equal (handle, TEST_HANDLE);
}
#define TEST_TCTI_NAME_SO TCTI_PREFIX"-"TEST_TCTI_NAME""TCTI_SUFFIX
static void
test_handle_from_name_third_dlopen_success (void **state)
{
    TSS2_RC rc;
    void *handle = NULL;

    expect_string(__wrap_dlopen, filename, TEST_TCTI_NAME);
    expect_value(__wrap_dlopen, flags, RTLD_NOW);
    will_return(__wrap_dlopen, NULL);

    expect_string(__wrap_dlopen, filename, TEST_TCTI_NAME_SO_0);
    expect_value(__wrap_dlopen, flags, RTLD_NOW);
    will_return(__wrap_dlopen, NULL);

    expect_string(__wrap_dlopen, filename, TEST_TCTI_NAME_SO);
    expect_value(__wrap_dlopen, flags, RTLD_NOW);
    will_return(__wrap_dlopen, TEST_HANDLE);

    rc = handle_from_name (TEST_TCTI_NAME, &handle);
    assert_int_equal (rc, TSS2_RC_SUCCESS);
    assert_int_equal (handle, TEST_HANDLE);
}

static void
test_tcti_from_file_null_tcti (void **state)
{
    TSS2_RC rc = tcti_from_file (NULL, NULL, NULL, NULL);
    assert_int_equal (rc, TSS2_TCTI_RC_BAD_REFERENCE);
}

#define HANDLE (void *)123321
#ifndef ESYS_TCTI_DEFAULT_MODULE
static void
test_get_info_default_null (void **state)
{
    TSS2_RC rc = get_info_default (NULL, NULL);
    assert_int_equal (rc, TSS2_TCTI_RC_BAD_REFERENCE);
}
static void
test_get_info_default_success (void **state)
{
    const TSS2_TCTI_INFO info_instance = { 0, };
    TSS2_TCTI_INFO *info = { 0, };
    void *handle;

    expect_string(__wrap_dlopen, filename, "libtss2-tcti-default.so");
    expect_value(__wrap_dlopen, flags, RTLD_NOW);
    will_return(__wrap_dlopen, NULL);

    expect_string(__wrap_dlopen, filename, "libtss2-tcti-libtss2-tcti-default.so.so.0");
    expect_value(__wrap_dlopen, flags, RTLD_NOW);
    will_return(__wrap_dlopen, NULL);

    expect_string(__wrap_dlopen, filename, "libtss2-tcti-libtss2-tcti-default.so.so");
    expect_value(__wrap_dlopen, flags, RTLD_NOW);
    will_return(__wrap_dlopen, NULL);

    expect_string(__wrap_dlopen, filename, "libtss2-tcti-tabrmd.so.0");
    expect_value(__wrap_dlopen, flags, RTLD_NOW);
    will_return(__wrap_dlopen, HANDLE);

    expect_value(__wrap_dlsym, handle, HANDLE);
    expect_string(__wrap_dlsym, symbol, TSS2_TCTI_INFO_SYMBOL);
    will_return(__wrap_dlsym, &__wrap_Tss2_Tcti_Fake_Info);

    will_return(__wrap_Tss2_Tcti_Fake_Info, &info_instance);

    TSS2_RC rc = get_info_default (&info, &handle);
    assert_int_equal (rc, TSS2_RC_SUCCESS);
    assert_ptr_equal (info, &info_instance);
}
static void
test_get_info_default_info_fail (void **state)
{
    TSS2_TCTI_INFO *info = { 0, };
    void *handle;

    expect_string(__wrap_dlopen, filename, "libtss2-tcti-default.so");
    expect_value(__wrap_dlopen, flags, RTLD_NOW);
    will_return(__wrap_dlopen, NULL);

    expect_string(__wrap_dlopen, filename, "libtss2-tcti-libtss2-tcti-default.so.so.0");
    expect_value(__wrap_dlopen, flags, RTLD_NOW);
    will_return(__wrap_dlopen, NULL);

    expect_string(__wrap_dlopen, filename, "libtss2-tcti-libtss2-tcti-default.so.so");
    expect_value(__wrap_dlopen, flags, RTLD_NOW);
    will_return(__wrap_dlopen, NULL);

    expect_string(__wrap_dlopen, filename, "libtss2-tcti-tabrmd.so.0");
    expect_value(__wrap_dlopen, flags, RTLD_NOW);
    will_return(__wrap_dlopen, HANDLE);

    expect_value(__wrap_dlsym, handle, HANDLE);
    expect_string(__wrap_dlsym, symbol, TSS2_TCTI_INFO_SYMBOL);
    will_return(__wrap_dlsym, &__wrap_Tss2_Tcti_Fake_Info);

    will_return(__wrap_Tss2_Tcti_Fake_Info, NULL);

    expect_value(__wrap_dlclose, handle, HANDLE);
    will_return(__wrap_dlclose, 0);

    TSS2_RC rc = get_info_default (&info, &handle);
    assert_int_equal (rc, TSS2_TCTI_RC_GENERAL_FAILURE);
    assert_ptr_equal (info, NULL);
}
/** Test for tcti
 * { "libtss2-tcti-default.so", NULL, "", "Access libtss2-tcti-default.so" }
 */
static void
test_tcti_default(void **state)
{
    TSS2_TCTI_CONTEXT *tcti;

    expect_string(__wrap_dlopen, filename, "libtss2-tcti-default.so");
    expect_value(__wrap_dlopen, flags, RTLD_NOW);
    will_return(__wrap_dlopen, HANDLE);

    expect_value(__wrap_dlsym, handle, HANDLE);
    expect_string(__wrap_dlsym, symbol, TSS2_TCTI_INFO_SYMBOL);
    will_return(__wrap_dlsym, &__wrap_Tss2_Tcti_Fake_Info);

    expect_value(__wrap_tcti_from_info, infof, __wrap_Tss2_Tcti_Fake_Info);
    expect_value(__wrap_tcti_from_info, conf, NULL);
    expect_value(__wrap_tcti_from_info, tcti, &tcti);
    will_return(__wrap_tcti_from_info, &tcti_instance);
    will_return(__wrap_tcti_from_info, TSS2_RC_SUCCESS);

    TSS2_RC r;
    void *handle = NULL;
    r = tctildr_get_default(&tcti, &handle);
    assert_int_equal(r, TSS2_RC_SUCCESS);
}

/** Test for failure on tcti
 * { "libtss2-tcti-default.so", NULL, "", "Access libtss2-tcti-default.so" }
 */
static void
test_tcti_default_fail_sym(void **state)
{
    TSS2_TCTI_CONTEXT *tcti;
#define HANDLE (void *)123321

    expect_string(__wrap_dlopen, filename, "libtss2-tcti-default.so");
    expect_value(__wrap_dlopen, flags, RTLD_NOW);
    will_return(__wrap_dlopen, HANDLE);

    expect_value(__wrap_dlsym, handle, HANDLE);
    expect_string(__wrap_dlsym, symbol, TSS2_TCTI_INFO_SYMBOL);
    will_return(__wrap_dlsym, NULL);

    expect_value(__wrap_dlclose, handle, HANDLE);
    will_return(__wrap_dlclose, 0);

    /** Now test
     *{ "libtss2-tcti-tabrmd.so", NULL, "", "Access libtss2-tcti-tabrmd.so"},
     */
    expect_string(__wrap_dlopen, filename, "libtss2-tcti-tabrmd.so.0");
    expect_value(__wrap_dlopen, flags, RTLD_NOW);
    will_return(__wrap_dlopen, HANDLE);

    expect_value(__wrap_dlsym, handle, HANDLE);
    expect_string(__wrap_dlsym, symbol, TSS2_TCTI_INFO_SYMBOL);
    will_return(__wrap_dlsym, &__wrap_Tss2_Tcti_Fake_Info);

    expect_value(__wrap_tcti_from_info, infof, __wrap_Tss2_Tcti_Fake_Info);
    expect_value(__wrap_tcti_from_info, conf, NULL);
    expect_value(__wrap_tcti_from_info, tcti, &tcti);
    will_return(__wrap_tcti_from_info, &tcti_instance);
    will_return(__wrap_tcti_from_info, TSS2_RC_SUCCESS);

    TSS2_RC r;
    r = tctildr_get_default(&tcti, NULL);
    assert_int_equal(r, TSS2_RC_SUCCESS);
}

/** Test for failure on tcti
 * { "libtss2-tcti-default.so", NULL, "", "Access libtss2-tcti-default.so" }
 */
static void
test_tcti_default_fail_info(void **state)
{
    TSS2_TCTI_CONTEXT *tcti;
#define HANDLE (void *)123321
#define TEST_RC 0x55687

 /** Test for failure on tcti
 * { "libtss2-tcti-default.so", NULL, "", "Access libtss2-tcti-default.so" }
 */
    expect_string(__wrap_dlopen, filename, "libtss2-tcti-default.so");
    expect_value(__wrap_dlopen, flags, RTLD_NOW);
    will_return(__wrap_dlopen, HANDLE);

    expect_value(__wrap_dlsym, handle, HANDLE);
    expect_string(__wrap_dlsym, symbol, TSS2_TCTI_INFO_SYMBOL);
    will_return(__wrap_dlsym, &__wrap_Tss2_Tcti_Fake_Info);

    expect_value(__wrap_tcti_from_info, infof, __wrap_Tss2_Tcti_Fake_Info);
    expect_value(__wrap_tcti_from_info, conf, NULL);
    expect_value(__wrap_tcti_from_info, tcti, &tcti);
    will_return(__wrap_tcti_from_info, &tcti_instance);
    will_return(__wrap_tcti_from_info, TEST_RC);

    expect_value(__wrap_dlclose, handle, HANDLE);
    will_return(__wrap_dlclose, 0);

    /** Now test
     *{ "libtss2-tcti-tabrmd.so", NULL, "", "Access libtss2-tcti-tabrmd.so"},
     */
    expect_string(__wrap_dlopen, filename, "libtss2-tcti-tabrmd.so.0");
    expect_value(__wrap_dlopen, flags, RTLD_NOW);
    will_return(__wrap_dlopen, HANDLE);

    expect_value(__wrap_dlsym, handle, HANDLE);
    expect_string(__wrap_dlsym, symbol, TSS2_TCTI_INFO_SYMBOL);
    will_return(__wrap_dlsym, &__wrap_Tss2_Tcti_Fake_Info);

    expect_value(__wrap_tcti_from_info, infof, __wrap_Tss2_Tcti_Fake_Info);
    expect_value(__wrap_tcti_from_info, conf, NULL);
    expect_value(__wrap_tcti_from_info, tcti, &tcti);
    will_return(__wrap_tcti_from_info, &tcti_instance);
    will_return(__wrap_tcti_from_info, TSS2_RC_SUCCESS);

    TSS2_RC r;
    r = tctildr_get_default(&tcti, NULL);
    assert_int_equal(r, TSS2_RC_SUCCESS);
}

static void
test_tcti_fail_all (void **state)
{
    /* skip over libtss2-tcti-default.so */
    expect_string(__wrap_dlopen, filename, "libtss2-tcti-default.so");
    expect_value(__wrap_dlopen, flags, RTLD_NOW);
    will_return(__wrap_dlopen, NULL);
    expect_string(__wrap_dlopen, filename, "libtss2-tcti-libtss2-tcti-default.so.so.0");
    expect_value(__wrap_dlopen, flags, RTLD_NOW);
    will_return(__wrap_dlopen, NULL);
    expect_string(__wrap_dlopen, filename, "libtss2-tcti-libtss2-tcti-default.so.so");
    expect_value(__wrap_dlopen, flags, RTLD_NOW);
    will_return(__wrap_dlopen, NULL);

    /* Skip over libtss2-tcti-tabrmd.so */
    expect_string(__wrap_dlopen, filename, "libtss2-tcti-tabrmd.so.0");
    expect_value(__wrap_dlopen, flags, RTLD_NOW);
    will_return(__wrap_dlopen, NULL);
    expect_string(__wrap_dlopen, filename, "libtss2-tcti-libtss2-tcti-tabrmd.so.0.so.0");
    expect_value(__wrap_dlopen, flags, RTLD_NOW);
    will_return(__wrap_dlopen, NULL);
    expect_string(__wrap_dlopen, filename, "libtss2-tcti-libtss2-tcti-tabrmd.so.0.so");
    expect_value(__wrap_dlopen, flags, RTLD_NOW);
    will_return(__wrap_dlopen, NULL);

    /* Skip over libtss2-tcti-device.so, /dev/tpmrm0 */
    expect_string(__wrap_dlopen, filename, "libtss2-tcti-device.so.0");
    expect_value(__wrap_dlopen, flags, RTLD_NOW);
    will_return(__wrap_dlopen, NULL);
    expect_string(__wrap_dlopen, filename, "libtss2-tcti-libtss2-tcti-device.so.0.so.0");
    expect_value(__wrap_dlopen, flags, RTLD_NOW);
    will_return(__wrap_dlopen, NULL);
    expect_string(__wrap_dlopen, filename, "libtss2-tcti-libtss2-tcti-device.so.0.so");
    expect_value(__wrap_dlopen, flags, RTLD_NOW);
    will_return(__wrap_dlopen, NULL);

    /* Skip over libtss2-tcti-device.so, /dev/tpm0 */
    expect_string(__wrap_dlopen, filename, "libtss2-tcti-device.so.0");
    expect_value(__wrap_dlopen, flags, RTLD_NOW);
    will_return(__wrap_dlopen, NULL);
    expect_string(__wrap_dlopen, filename, "libtss2-tcti-libtss2-tcti-device.so.0.so.0");
    expect_value(__wrap_dlopen, flags, RTLD_NOW);
    will_return(__wrap_dlopen, NULL);
    expect_string(__wrap_dlopen, filename, "libtss2-tcti-libtss2-tcti-device.so.0.so");
    expect_value(__wrap_dlopen, flags, RTLD_NOW);
    will_return(__wrap_dlopen, NULL);

    /* Skip over libtss2-tcti-swtpm.so */
    expect_string(__wrap_dlopen, filename, "libtss2-tcti-swtpm.so.0");
    expect_value(__wrap_dlopen, flags, RTLD_NOW);
    will_return(__wrap_dlopen, NULL);
    expect_string(__wrap_dlopen, filename, "libtss2-tcti-libtss2-tcti-swtpm.so.0.so.0");
    expect_value(__wrap_dlopen, flags, RTLD_NOW);
    will_return(__wrap_dlopen, NULL);
    expect_string(__wrap_dlopen, filename, "libtss2-tcti-libtss2-tcti-swtpm.so.0.so");
    expect_value(__wrap_dlopen, flags, RTLD_NOW);
    will_return(__wrap_dlopen, NULL);

    /* Skip over libtss2-tcti-mssim.so */
    expect_string(__wrap_dlopen, filename, "libtss2-tcti-mssim.so.0");
    expect_value(__wrap_dlopen, flags, RTLD_NOW);
    will_return(__wrap_dlopen, NULL);
    expect_string(__wrap_dlopen, filename, "libtss2-tcti-libtss2-tcti-mssim.so.0.so.0");
    expect_value(__wrap_dlopen, flags, RTLD_NOW);
    will_return(__wrap_dlopen, NULL);
    expect_string(__wrap_dlopen, filename, "libtss2-tcti-libtss2-tcti-mssim.so.0.so");
    expect_value(__wrap_dlopen, flags, RTLD_NOW);
    will_return(__wrap_dlopen, NULL);

    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    r = tctildr_get_default(&tcti, NULL);
    assert_int_equal(r, TSS2_TCTI_RC_IO_ERROR);
}
#endif
void
test_info_from_name_null (void **state)
{
    TSS2_RC rc = info_from_name (NULL, NULL, NULL);
    assert_int_equal (rc, TSS2_TCTI_RC_BAD_REFERENCE);
}
void
test_info_from_name_handle_fail (void **state)
{
    const TSS2_TCTI_INFO *info;
    void *data;

    expect_string(__wrap_dlopen, filename, "foo");
    expect_value(__wrap_dlopen, flags, RTLD_NOW);
    will_return(__wrap_dlopen, NULL);
    expect_string(__wrap_dlopen, filename, "libtss2-tcti-foo.so.0");
    expect_value(__wrap_dlopen, flags, RTLD_NOW);
    will_return(__wrap_dlopen, NULL);
    expect_string(__wrap_dlopen, filename, "libtss2-tcti-foo.so");
    expect_value(__wrap_dlopen, flags, RTLD_NOW);
    will_return(__wrap_dlopen, NULL);

    TSS2_RC rc = info_from_name ("foo", &info, &data);
    assert_int_equal (rc, TSS2_TCTI_RC_NOT_SUPPORTED);
}
void
test_info_from_name_info_fail (void **state)
{
    const TSS2_TCTI_INFO *info = { 0, };
    void *data = HANDLE;

    expect_string(__wrap_dlopen, filename, "foo");
    expect_value(__wrap_dlopen, flags, RTLD_NOW);
    will_return(__wrap_dlopen, HANDLE);

    expect_value(__wrap_dlsym, handle, HANDLE);
    expect_string(__wrap_dlsym, symbol, TSS2_TCTI_INFO_SYMBOL);
    will_return(__wrap_dlsym, &__wrap_Tss2_Tcti_Fake_Info);

    will_return(__wrap_Tss2_Tcti_Fake_Info, NULL);

    expect_value(__wrap_dlclose, handle, HANDLE);
    will_return(__wrap_dlclose, 0);

    TSS2_RC rc = info_from_name ("foo", &info, &data);
    assert_int_equal (rc, TSS2_TCTI_RC_IO_ERROR);
}
void
test_info_from_name_success (void **state)
{
    const TSS2_TCTI_INFO *info = { 0, };
    TSS2_TCTI_INFO info_instance = { 0, };
    void *data;

    expect_string(__wrap_dlopen, filename, "foo");
    expect_value(__wrap_dlopen, flags, RTLD_NOW);
    will_return(__wrap_dlopen, HANDLE);

    expect_value(__wrap_dlsym, handle, HANDLE);
    expect_string(__wrap_dlsym, symbol, TSS2_TCTI_INFO_SYMBOL);
    will_return(__wrap_dlsym, &__wrap_Tss2_Tcti_Fake_Info);

    will_return(__wrap_Tss2_Tcti_Fake_Info, &info_instance);

    TSS2_RC rc = info_from_name ("foo", &info, &data);
    assert_int_equal (rc, TSS2_RC_SUCCESS);
    assert_ptr_equal (info, &info_instance);
    assert_ptr_equal (data, HANDLE);
}
void
test_get_tcti_null (void **state)
{
    TSS2_RC rc = tctildr_get_tcti (NULL, NULL, NULL, NULL);
    assert_int_equal(rc, TSS2_TCTI_RC_BAD_REFERENCE);
}
void
test_get_tcti_default (void **state)
{
    TSS2_TCTI_CONTEXT *tcti;

    expect_string(__wrap_dlopen, filename, "libtss2-tcti-default.so");
    expect_value(__wrap_dlopen, flags, RTLD_NOW);
    will_return(__wrap_dlopen, HANDLE);

    expect_value(__wrap_dlsym, handle, HANDLE);
    expect_string(__wrap_dlsym, symbol, TSS2_TCTI_INFO_SYMBOL);
    will_return(__wrap_dlsym, &__wrap_Tss2_Tcti_Fake_Info);

    expect_value(__wrap_tcti_from_info, infof, __wrap_Tss2_Tcti_Fake_Info);
    expect_value(__wrap_tcti_from_info, conf, NULL);
    expect_value(__wrap_tcti_from_info, tcti, &tcti);
    will_return(__wrap_tcti_from_info, &tcti_instance);
    will_return(__wrap_tcti_from_info, TSS2_RC_SUCCESS);

    void *data;
    TSS2_RC rc = tctildr_get_tcti (NULL, NULL, &tcti, &data);
    assert_int_equal(rc, TSS2_RC_SUCCESS);
}
void
test_get_tcti_from_name (void **state)
{
    TSS2_TCTI_CONTEXT *tcti;

    expect_string(__wrap_dlopen, filename, "libtss2-tcti-default.so");
    expect_value(__wrap_dlopen, flags, RTLD_NOW);
    will_return(__wrap_dlopen, HANDLE);

    expect_value(__wrap_dlsym, handle, HANDLE);
    expect_string(__wrap_dlsym, symbol, TSS2_TCTI_INFO_SYMBOL);
    will_return(__wrap_dlsym, &__wrap_Tss2_Tcti_Fake_Info);

    expect_value(__wrap_tcti_from_info, infof, __wrap_Tss2_Tcti_Fake_Info);
    expect_value(__wrap_tcti_from_info, conf, NULL);
    expect_value(__wrap_tcti_from_info, tcti, &tcti);
    will_return(__wrap_tcti_from_info, &tcti_instance);
    will_return(__wrap_tcti_from_info, TSS2_RC_SUCCESS);

    void *data;
    TSS2_RC rc = tctildr_get_tcti ("libtss2-tcti-default.so", NULL, &tcti, &data);
    assert_int_equal(rc, TSS2_RC_SUCCESS);
}

void
test_tctildr_get_info_from_name (void **state)
{
    const TSS2_TCTI_INFO *info;
    void *data;

    expect_string(__wrap_dlopen, filename, "foo");
    expect_value(__wrap_dlopen, flags, RTLD_NOW);
    will_return(__wrap_dlopen, NULL);
    expect_string(__wrap_dlopen, filename, "libtss2-tcti-foo.so.0");
    expect_value(__wrap_dlopen, flags, RTLD_NOW);
    will_return(__wrap_dlopen, NULL);
    expect_string(__wrap_dlopen, filename, "libtss2-tcti-foo.so");
    expect_value(__wrap_dlopen, flags, RTLD_NOW);
    will_return(__wrap_dlopen, NULL);

    TSS2_RC rc = tctildr_get_info ("foo", &info, &data);
    assert_int_equal (rc, TSS2_TCTI_RC_NOT_SUPPORTED);
}
void
test_tctildr_get_info_default (void **state)
{
    const TSS2_TCTI_INFO *info;
    void *data;

    expect_string(__wrap_dlopen, filename, "libtss2-tcti-default.so");
    expect_value(__wrap_dlopen, flags, RTLD_NOW);
    will_return(__wrap_dlopen, HANDLE);

    expect_value(__wrap_dlsym, handle, HANDLE);
    expect_string(__wrap_dlsym, symbol, TSS2_TCTI_INFO_SYMBOL);
    will_return(__wrap_dlsym, NULL);

    expect_value(__wrap_dlclose, handle, HANDLE);
    will_return(__wrap_dlclose, 0);

    TSS2_RC rc = tctildr_get_info (NULL, &info, &data);
    assert_int_equal (rc, TSS2_TCTI_RC_GENERAL_FAILURE);
}

void
test_finalize_data (void **state)
{
    void *data = HANDLE;

    expect_value(__wrap_dlclose, handle, data);
    will_return(__wrap_dlclose, 0);
    tctildr_finalize_data (&data);
    assert_null (data);
}

int
main(void)
{
    const struct CMUnitTest tests[] = {
        cmocka_unit_test(test_info_from_handle_null),
        cmocka_unit_test(test_info_from_handle_dlsym_fail),
        cmocka_unit_test(test_info_from_handle_success),
        cmocka_unit_test(test_handle_from_name_null_handle),
        cmocka_unit_test(test_handle_from_name_first_dlopen_success),
        cmocka_unit_test(test_handle_from_name_second_dlopen_success),
        cmocka_unit_test(test_handle_from_name_third_dlopen_success),
        cmocka_unit_test(test_fail_null),
        cmocka_unit_test(test_tcti_from_file_null_tcti),
#ifndef ESYS_TCTI_DEFAULT_MODULE
        cmocka_unit_test(test_get_info_default_null),
        cmocka_unit_test(test_get_info_default_success),
        cmocka_unit_test(test_get_info_default_info_fail),
        cmocka_unit_test(test_tcti_default),
        cmocka_unit_test(test_tcti_default_fail_sym),
        cmocka_unit_test(test_tcti_default_fail_info),
        cmocka_unit_test(test_tcti_fail_all),
        cmocka_unit_test(test_get_tcti_null),
        cmocka_unit_test(test_get_tcti_default),
        cmocka_unit_test(test_get_tcti_from_name),
        cmocka_unit_test(test_tctildr_get_info_from_name),
        cmocka_unit_test(test_tctildr_get_info_default),
#endif
        cmocka_unit_test(test_info_from_name_null),
        cmocka_unit_test(test_info_from_name_handle_fail),
        cmocka_unit_test(test_info_from_name_info_fail),
        cmocka_unit_test(test_info_from_name_success),
        cmocka_unit_test(test_finalize_data),
    };
    return cmocka_run_group_tests (tests, NULL, NULL);
}
