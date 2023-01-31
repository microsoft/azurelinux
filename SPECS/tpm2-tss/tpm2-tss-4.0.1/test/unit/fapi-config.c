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
#include <unistd.h>
#include <stdio.h>
#include <json-c/json_object.h>
#include <json-c/json_util.h>
#include <json-c/json_tokener.h>

#include <setjmp.h>
#include <cmocka.h>
#include <errno.h>

#include "ifapi_io.h"
#include "ifapi_config.h"
#include "util/aux_util.h"

#define LOGMODULE tests
#include "util/log.h"

/*
 * The unit tests will test deserialization of FAPI config files. It will be
 * checked whether the correct return codes are returned if optional and
 * mandatory fields are removed from the configuration.
 * Also the expansion of abbreviations for the home directory will be
 * tested.
 */

/* Config file which will be used for the test. */
char *wrap_config_file_content;
/* JSON field which will be removed for the test. */
char *wrap_remove_field;

static char* config_tilde =
    "{" \
    "     \"profile_name\": \"P_ECCP256SHA256\"," \
    "     \"profile_dir\": \"~/profile\"," \
    "     \"user_dir\": \"~/user_dir\"," \
    "     \"system_dir\": \"~/system_dir\"," \
    "     \"log_dir\": \"~/log_dir\"," \
    "     \"tcti\": \"\"," \
    "     \"system_pcrs\" : []" \
    "}";

static char* config_home =
    "{" \
    "     \"profile_name\": \"P_ECCP256SHA256\"," \
    "     \"profile_dir\": \"$HOME/profile\"," \
    "     \"user_dir\": \"$HOME/user_dir\"," \
    "     \"system_dir\": \"$HOME/system_dir\"," \
    "     \"log_dir\": \"$HOME/log_dir\"," \
    "     \"tcti\": \"\"," \
    "     \"system_pcrs\" : []" \
    "}";

/*
 * Wrappers for reading the JSON profile.
 */
TSS2_RC
__wrap_ifapi_io_read_finish(
    struct IFAPI_IO *io,
    uint8_t **buffer,
    size_t *length, ...);

TSS2_RC
__wrap_ifapi_io_read_finish(
    struct IFAPI_IO *io,
    uint8_t **buffer,
    size_t *length, ...)
{
    json_object *jso = NULL;
    const char *jso_string = NULL;

    jso = json_tokener_parse(wrap_config_file_content);
    assert_ptr_not_equal(jso, NULL);
    json_object_object_del(jso, wrap_remove_field);
    jso_string = json_object_to_json_string_ext(jso, JSON_C_TO_STRING_PRETTY);
    assert_ptr_not_equal(jso_string, NULL);
    *buffer = (uint8_t *)strdup(jso_string);
    *length = strlen(jso_string);
    json_object_put(jso);
    assert_ptr_not_equal(*buffer, NULL);
    return TSS2_RC_SUCCESS;
}

/* Function to remove the field and check the initialization of the configuration. */
void check_remove_field(char *file_content, char* fname, TSS2_RC rc)
{
    IFAPI_IO io;
    IFAPI_CONFIG config;
    TSS2_RC r;
    char *home_dir = getenv("HOME");

    assert_ptr_not_equal(home_dir, NULL);
    wrap_config_file_content = file_content;
    wrap_remove_field = fname;
    r = ifapi_config_initialize_finish(&io, &config);
    assert_int_equal(r, rc);
    if (r == TSS2_RC_SUCCESS) {
        LOG_WARNING("TEST OUTPUT: %s", config.profile_dir);
        assert_true(strncmp(config.profile_dir, home_dir, strlen(home_dir)) == 0);
        SAFE_FREE(config.profile_dir);
        assert_true(strncmp(config.user_dir, home_dir, strlen(home_dir)) == 0);
        SAFE_FREE(config.user_dir);
        assert_true(strncmp(config.keystore_dir, home_dir, strlen(home_dir)) == 0);
        SAFE_FREE(config.keystore_dir);
        SAFE_FREE(config.log_dir);
        SAFE_FREE(config.profile_name);
        SAFE_FREE(config.tcti);
        SAFE_FREE(config.ek_cert_file);
        SAFE_FREE(config.intel_cert_service)
            }
}

/* Function to remove the field and check the initialization of the configuration. */
static void
check_config_json_remove_field_allowed(void **state) {
    check_remove_field(config_home, "log_dir", TSS2_RC_SUCCESS);
    check_remove_field(config_tilde, "log_dir", TSS2_RC_SUCCESS);
}

/* Check removing of the mandatory fields. */
static void
check_config_json_remove_field_not_allowed(void **state) {
    check_remove_field(config_tilde, "profile_dir", TSS2_FAPI_RC_BAD_VALUE);
    check_remove_field(config_tilde, "system_dir", TSS2_FAPI_RC_BAD_VALUE);
    check_remove_field(config_tilde, "user_dir", TSS2_FAPI_RC_BAD_VALUE);
    check_remove_field(config_tilde, "profile_name", TSS2_FAPI_RC_BAD_VALUE);
    check_remove_field(config_tilde, "tcti", TSS2_FAPI_RC_BAD_VALUE);
    check_remove_field(config_tilde, "system_pcrs", TSS2_FAPI_RC_BAD_VALUE);
}

int
main(int argc, char *argv[])
{
    const struct CMUnitTest tests[] = {
        cmocka_unit_test(check_config_json_remove_field_allowed),
        cmocka_unit_test(check_config_json_remove_field_not_allowed),
    };
    return cmocka_run_group_tests(tests, NULL, NULL);
}
