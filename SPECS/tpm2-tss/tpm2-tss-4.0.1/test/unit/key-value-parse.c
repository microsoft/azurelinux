/* SPDX-License-Identifier: BSD-2-Clause */
/***********************************************************************
 * Copyright (c) 2017-2018, Intel Corporation
 *
 * All rights reserved.
 ***********************************************************************/

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <setjmp.h>
#include <cmocka.h>

#include "util/key-value-parse.h"

/*
 * Ensure that a simple key / value string is parsed into its component parts.
 */
static void
parse_key_value_simple_test (void **state)
{
    bool ret;
    char test_str[] = "key=value";
    key_value_t key_value = KEY_VALUE_INIT;

    ret = parse_key_value (test_str, &key_value);
    assert_true (ret);
    assert_string_equal (key_value.key, "key");
    assert_string_equal (key_value.value, "value");
}
/*
 * Ensure that a NULL key/value string causes parse_key_value to return false.
 */
static void
parse_key_value_NULL_string_test (void **state)
{
    bool ret;
    key_value_t key_value = KEY_VALUE_INIT;

    ret = parse_key_value (NULL, &key_value);
    assert_false (ret);
}
/*
 * Ensure that a NULL key_value_t parameter causes parse_key_value to return
 * false.
 */
static void
parse_key_value_NULL_key_value_test (void **state)
{
    bool ret;
    char test_str[] = "key=value";

    ret = parse_key_value (test_str, NULL);
    assert_false (ret);
}
/*
 * Ensure that an incomplete key/value string with only the "key=" returns
 * false.
 */
static void
parse_key_value_no_value_test (void **state)
{
    bool ret;
    char test_str[] = "key=";
    key_value_t key_value = KEY_VALUE_INIT;

    ret = parse_key_value (test_str, &key_value);
    assert_false (ret);
}
/*
 * Ensure that a key/value string with only the "=value" part returns false.
 */
static void
parse_key_value_no_key_test (void **state)
{
    bool ret;
    char test_str[] = "=value";
    key_value_t key_value = KEY_VALUE_INIT;

    ret = parse_key_value (test_str, &key_value);
    assert_false (ret);
}
/*
 * Ensure that a key/value string with the separators in the wrong place
 * returns false.
 */
static void
parse_key_value_two_seps_test (void **state)
{
    bool ret;
    char test_str[] = "=foo=";
    key_value_t key_value = KEY_VALUE_INIT;

    ret = parse_key_value (test_str, &key_value);
    assert_false (ret);
}
/*
 * Ensure that a key/value string with all separators returns false.
 */
static void
parse_key_value_all_seps_test (void **state)
{
    bool ret;
    char test_str[] = "====";
    key_value_t key_value = KEY_VALUE_INIT;

    ret = parse_key_value (test_str, &key_value);
    assert_false (ret);
}
/*
 * Ensure that a key/value string that alternates strings and separators
 * will parse the first two and ignore the rest.
 */
static void
parse_key_value_alt_seps_test (void **state)
{
    bool ret;
    char test_str[] = "key=value=key=value";
    key_value_t key_value = KEY_VALUE_INIT;

    ret = parse_key_value (test_str, &key_value);
    assert_true (ret);
    assert_string_equal (key_value.key, "key");
    assert_string_equal (key_value.value, "value");
}
/*
 * This is a simple data structure used to hold values parsed from a string
 * of key/value pairs.
 */
#define TEST_DATA_INIT { \
    .value0 = NULL, \
    .value1 = NULL, \
}
typedef struct {
    char *value0;
    char *value1;
} test_data_t;
/*
 * This is a callback function used to handle extracted key / value pairs.
 */
TSS2_RC
key_value_callback (const key_value_t *key_value,
                    void *user_data)
{
    test_data_t *test_data = (test_data_t*)user_data;

    if (strcmp ("key0", key_value->key) == 0) {
        test_data->value0 = key_value->value;
        return TSS2_RC_SUCCESS;
    } else if (strcmp ("key1", key_value->key) == 0) {
        test_data->value1 = key_value->value;
        return TSS2_RC_SUCCESS;
    } else {
        return 1;
    }
}
/*
 * This tests the typical case for the parsing of a string of key / value
 * pairs.
 */
static void
parse_key_value_string_good_test (void **state)
{
    TSS2_RC rc;
    char test_str[] = "key0=value0,key1=value1";
    test_data_t test_data = TEST_DATA_INIT;

    rc = parse_key_value_string (test_str, key_value_callback, &test_data);
    assert_int_equal (rc, TSS2_RC_SUCCESS);
    assert_string_equal (test_data.value0, "value0");
    assert_string_equal (test_data.value1, "value1");
}
/*
 * This test ensures that he parse_key_value_string function handles a failed
 * call to parse a key/value pair properly.
 */
static void
parse_key_value_string_no_value_test (void **state)
{
    TSS2_RC rc;
    char test_str[] = "key0=,key1=value1";
    test_data_t test_data = TEST_DATA_INIT;

    rc = parse_key_value_string (test_str, key_value_callback, &test_data);
    assert_int_equal (rc, TSS2_TCTI_RC_BAD_VALUE);
}
/*
 * This test ensures that the parse_key_value_string function handles a failed
 * call to the user provided callback properly. The return value we get from
 * the parse_key_value_string function is the same value returned by our
 * callback.
 */
static void
parse_key_value_string_unknown_key_test (void **state)
{
    TSS2_RC rc;
    char test_str[] = "key0=foo=bar,baz=qux";
    test_data_t test_data = TEST_DATA_INIT;

    rc = parse_key_value_string (test_str, key_value_callback, &test_data);
    assert_int_equal (rc, 1);
}
/*
 * The following 3 tests ensures that NULL parameters produce an error.
 */
static void
parse_key_value_string_NULL_kv_string_test (void **state)
{
    TSS2_RC rc;
    test_data_t test_data = TEST_DATA_INIT;

    rc = parse_key_value_string (NULL, key_value_callback, &test_data);
    assert_int_equal (rc, TSS2_TCTI_RC_BAD_VALUE);
}
static void
parse_key_value_string_NULL_callback_test (void **state)
{
    TSS2_RC rc;
    char test_str[] = "key0=foo=bar,baz=qux";
    test_data_t test_data = TEST_DATA_INIT;

    rc = parse_key_value_string (test_str, NULL, &test_data);
    assert_int_equal (rc, TSS2_TCTI_RC_BAD_VALUE);
}
static void
parse_key_value_string_NULL_user_data_test (void **state)
{
    TSS2_RC rc;
    char test_str[] = "key0=foo=bar,baz=qux";

    rc = parse_key_value_string (test_str, key_value_callback, NULL);
    assert_int_equal (rc, TSS2_TCTI_RC_BAD_VALUE);
}

int
main(int argc, char* argv[])
{
    const struct CMUnitTest tests[] = {
        cmocka_unit_test (parse_key_value_simple_test),
        cmocka_unit_test (parse_key_value_NULL_string_test),
        cmocka_unit_test (parse_key_value_NULL_key_value_test),
        cmocka_unit_test (parse_key_value_no_value_test),
        cmocka_unit_test (parse_key_value_no_key_test),
        cmocka_unit_test (parse_key_value_two_seps_test),
        cmocka_unit_test (parse_key_value_all_seps_test),
        cmocka_unit_test (parse_key_value_alt_seps_test),
        cmocka_unit_test (parse_key_value_string_good_test),
        cmocka_unit_test (parse_key_value_string_no_value_test),
        cmocka_unit_test (parse_key_value_string_unknown_key_test),
        cmocka_unit_test (parse_key_value_string_NULL_kv_string_test),
        cmocka_unit_test (parse_key_value_string_NULL_callback_test),
        cmocka_unit_test (parse_key_value_string_NULL_user_data_test),
    };
    return cmocka_run_group_tests (tests, NULL, NULL);
}
