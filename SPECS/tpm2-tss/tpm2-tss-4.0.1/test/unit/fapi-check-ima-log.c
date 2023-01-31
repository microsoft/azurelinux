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
#include <json-c/json_util.h>
#include <json-c/json_tokener.h>

#include <setjmp.h>
#include <cmocka.h>

#include "tss2_fapi.h"
#include "ifapi_eventlog.h"
#include "ifapi_ima_eventlog.h"
#include "fapi_policy.h"

#include "util/aux_util.h"

#define LOGMODULE tests
#include "util/log.h"


static void
check_eventlog(const char *file)
{
    TSS2_RC r;
    char *json_string;
    int n_bin, i;
    uint32_t pcr_list[1] = { 10 };
    json_object
        *json_event_list = NULL, *json_bin = NULL,
        *json_ascii_list = NULL;
    r = ifapi_read_ima_event_log(file, &pcr_list[0], 1, &json_event_list);
    assert_int_equal (r, TSS2_RC_SUCCESS);

    json_string = strdup(json_object_to_json_string_ext(json_event_list,
                                                        JSON_C_TO_STRING_PRETTY));
    assert_non_null(json_string);

    fprintf(stderr, "\n%s\n", json_string);

    n_bin= json_object_array_length(json_event_list);

    for (i = 0; i < n_bin; i++) {
        IFAPI_EVENT event;

        json_bin =  json_object_array_get_idx(json_event_list, i);
        assert_non_null(json_bin);

        r = ifapi_json_IFAPI_EVENT_deserialize(json_bin,  &event,
                                               DIGEST_CHECK_ERROR);
        assert_int_equal(r, TSS2_RC_SUCCESS);

        ifapi_cleanup_event(&event);
    }
    json_object_put(json_event_list);
    json_object_put(json_ascii_list);
    SAFE_FREE(json_string);
}

/*
 * Ensure that an IMA ima-ng  event list can be read deserialized with digest
 * verification.
 */
static void
check_sml_ima_ng_sha1(void **state)
{
    check_eventlog("test/data/fapi/eventlog/sml-ima-ng-sha1.bin");
}

/*
 * Ensure that an IMA legacy event list can be read deserialized with digest
 * verification.
 */
static void
check_sml_ima_sha1(void **state)
{
    check_eventlog("test/data/fapi/eventlog/sml-ima-sha1.bin");
}

/*
 * Ensure that an IMA ima-ng event list with invalidated events can be read
 * deserialized with digest verification.
 */
static void
check_sml_ima_ng_sha1_invalidated(void **state)
{
    // TOODO check ivalidated file
    // check_eventlog("test/data/fapi/eventlog/sml-ima-ng-sha1-invalidated.bin");
}

/*
 * Ensure that an IMA legacy event list with invalidated events can be read
 * deserialized with digest verification.
 */
static void
check_sml_ima_sha1_invalidated(void **state)
{
    check_eventlog("test/data/fapi/eventlog/sml-ima-sha1-invalidated.bin");
}


/*
 * Ensure that an IMA ima-sig event list with invalidated events can be read
 * deserialized with digest verification.
 */
static void
check_sml_ima_sig_sha256(void **state)
{
    check_eventlog("test/data/fapi/eventlog/sml-ima-sig-sha256.bin");
}

/*
 * Ensure that an IMA ima-sig event list with invalidated events can be read
 * deserialized with digest verification.
 */
static void
check_sml_ima_sig_sha256_invalidated(void **state)
{
    check_eventlog("test/data/fapi/eventlog/sml-ima-sig-sha256-invalidated.bin");
}


int
main(int argc, char *argv[])
{
    const struct CMUnitTest tests[] = {
        cmocka_unit_test(check_sml_ima_ng_sha1),
        cmocka_unit_test(check_sml_ima_sha1),
        cmocka_unit_test(check_sml_ima_sig_sha256),
        cmocka_unit_test(check_sml_ima_ng_sha1_invalidated),
        cmocka_unit_test(check_sml_ima_sha1_invalidated),
        cmocka_unit_test(check_sml_ima_sig_sha256_invalidated),
    };
    return cmocka_run_group_tests(tests, NULL, NULL);
}
