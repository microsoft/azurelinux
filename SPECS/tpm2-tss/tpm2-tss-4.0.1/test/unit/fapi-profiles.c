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
#include "ifapi_profiles.h"
#include "util/aux_util.h"

#define LOGMODULE tests
#include "util/log.h"

/*
 * The unit tests will test deserialization of FAPI profiles. It will be
 * checked whether the correct return codes are returned if optional and
 * mandatory fields are removed from the profile.
 */

/* Profile file which will be used for the test. */
char *wrap_profile_file;
/* JSON field which will be removed for the test. */
char *wrap_remove_field;

json_object *
read_json(char *file_name)
{
    FILE *stream = NULL;
    long file_size;
    char *json_string = NULL;
    json_object *jso = NULL;
    char file[1024];

    if (snprintf(&file[0], 1023, TOP_SOURCEDIR "/%s", file_name) < 0)
        return NULL;

    stream = fopen(file, "r");
    if (!stream) {
        LOG_ERROR("File %s does not exist", file);
        return NULL;
    }
    fseek(stream, 0L, SEEK_END);
    file_size = ftell(stream);
    fclose(stream);
    json_string = malloc(file_size + 1);
    stream = fopen(file, "r");
    ssize_t ret = read(fileno(stream), json_string, file_size);
    if (ret != file_size) {
        LOG_ERROR("IO error %s.",file);
        return NULL;
    }
    json_string[file_size] = '\0';
    jso = json_tokener_parse(json_string);
    SAFE_FREE(json_string);
    return jso;
}

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

    jso = read_json(wrap_profile_file);
    assert_ptr_not_equal(jso, NULL);
    json_object_object_del(jso, wrap_remove_field);
    jso_string = json_object_to_json_string_ext(jso, JSON_C_TO_STRING_PRETTY);
    assert_ptr_not_equal(jso_string, NULL);
    *buffer = (uint8_t *)strdup(jso_string);
    json_object_put(jso);
    assert_ptr_not_equal(*buffer, NULL);
    return TSS2_RC_SUCCESS;
}

/* Function to remove the field and check the profile initialization. */
void check_remove_field(char *file, char* fname, TSS2_RC rc)
    {
        IFAPI_IO io;
        IFAPI_PROFILES profiles;
        TSS2_RC r;

        profiles.num_profiles = 1;
        profiles.profiles_idx = 0;
        profiles.default_name = strdup("dmy_name");
        profiles.filenames = calloc(1 ,sizeof(profiles.filenames[0]));
        assert_ptr_not_equal(profiles.filenames, NULL);
        profiles.profiles = calloc(profiles.num_profiles, sizeof(profiles.profiles[0]));
        profiles.profiles[0].name = strdup("dmy_name");
        assert_ptr_not_equal(profiles.profiles[0].name, NULL);
        profiles.filenames[0] = strdup("dmy_name");
        assert_ptr_not_equal( profiles.filenames[0], NULL);
        wrap_profile_file = file;
        wrap_remove_field = fname;
        r = ifapi_profiles_initialize_finish(&profiles, &io);
        assert_int_equal(r, rc);
        ifapi_profiles_finalize(&profiles);
    }

/* Check removing the optional fields. */
static void
check_profile_json_remove_field_allowed(void **state) {
    check_remove_field("test/data/fapi/P_RSA.json", "srk_description", TSS2_RC_SUCCESS);
    check_remove_field("test/data/fapi/P_RSA.json", "ekk_description", TSS2_RC_SUCCESS);
}

/* Check removing of the mandatory fields. */
static void
check_profile_json_remove_field_not_allowed(void **state) {
    check_remove_field("test/data/fapi/P_ECC.json", "type", TSS2_FAPI_RC_BAD_VALUE);
    check_remove_field("test/data/fapi/P_ECC.json", "curveID", TSS2_FAPI_RC_BAD_VALUE);
    check_remove_field("test/data/fapi/P_RSA.json", "keyBits", TSS2_FAPI_RC_BAD_VALUE);
    check_remove_field("test/data/fapi/P_RSA.json", "exponent", TSS2_FAPI_RC_BAD_VALUE);
    check_remove_field("test/data/fapi/P_RSA.json", "nameAlg", TSS2_FAPI_RC_BAD_VALUE);
    check_remove_field("test/data/fapi/P_RSA.json", "pcr_selection", TSS2_FAPI_RC_BAD_VALUE);
    check_remove_field("test/data/fapi/P_RSA.json", "pcr_selection", TSS2_FAPI_RC_BAD_VALUE);
    check_remove_field("test/data/fapi/P_RSA.json", "sym_block_size", TSS2_FAPI_RC_BAD_VALUE);
    check_remove_field("test/data/fapi/P_RSA.json", "sym_parameters", TSS2_FAPI_RC_BAD_VALUE);
    check_remove_field("test/data/fapi/P_RSA.json", "sym_mode", TSS2_FAPI_RC_BAD_VALUE);
    check_remove_field("test/data/fapi/P_RSA.json", "ek_template", TSS2_FAPI_RC_BAD_VALUE);
    check_remove_field("test/data/fapi/P_RSA.json", "srk_template", TSS2_FAPI_RC_BAD_VALUE);
}


int
main(int argc, char *argv[])
{
    const struct CMUnitTest tests[] = {
        cmocka_unit_test(check_profile_json_remove_field_allowed),
        cmocka_unit_test(check_profile_json_remove_field_not_allowed),
    };
    return cmocka_run_group_tests(tests, NULL, NULL);
}
