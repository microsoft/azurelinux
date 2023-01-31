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
#include <openssl/sha.h>
#include <openssl/evp.h>

#include <setjmp.h>
#include <cmocka.h>

#include "tss2_fapi.h"
#include "ifapi_eventlog.h"
#include "ifapi_ima_eventlog.h"
#include "fapi_policy.h"

#include "util/aux_util.h"

#define LOGMODULE tests
#include "util/log.h"

typedef struct {
	char *digest1;
    char *name;
} ascii_event;

ascii_event sml_ima_ng_sha1[6] = {
    { .digest1 = "1d8d532d463c9f8c205d0df7787669a85f93e260",
      .name = "boot_aggregate" },
    { .digest1 = "972d62ff5b3a74e89952e0980b2099eed49bf8f0",
      .name = "/init" },
    { .digest1 = "c76ee54d77352bee745ce43829247ff1706886df",
      .name = "/usr/bin/sh" },
    { .digest1 = "ef885dd41140c5fb993188f60a298c5a9b31d038",
      .name = "/usr/lib/x86_64-linux-gnu/ld-2.31.so" },
    { .digest1 = "a8fe19f5a9773edebf7b7df90bf9ce38b071e684",
      .name = "/etc/ld.so.cache" },
    { .digest1 = "0801daa94a2c43f41200143b319f19b28b43f745",
      .name = "/usr/lib/x86_64-linux-gnu/libc-2.31.so" }
};

ascii_event sml_ima_sha1[12] = {
    { .digest1 = "719de8e521439498e9b77f6ed41e230b9821111e",
      .name = "boot_aggregate" },
    { .digest1 = "a3ff2672a129ea092ec2d41b88daafe632a8b65a",
      .name = "/init" },
    { .digest1 = "11fdfd51127b2a3853c55136d0c76411f6246892",
      .name = "/usr/bin/sh" },
    { .digest1 = "7a89e5da2a7299c7b3d76fbbbd4727d13818cc9a",
      .name = "/usr/lib/x86_64-linux-gnu/ld-2.31.so" },
    { .digest1 = "6d644a6a36001decfbc93ae98734473adc807c98",
      .name = "/etc/ld.so.cache" },
    { .digest1 = "70ff9de3f9a80361cca4f13edc027150318116da",
      .name = "/usr/lib/x86_64-linux-gnu/libc-2.31.so" },
    { .digest1 = "082ab538004eb50f2c8cdcbc8467037b11436ed6",
      .name = "/conf/arch.conf" },
    { .digest1 = "0cf46ceded0ffc71df00612568f6679208bb43d1",
      .name = "/conf/initramfs.conf" },
    { .digest1 = "37d29d0dbcfcc9b90fcd1986e452ab27a017e61a",
      .name = "/scripts/functions" },
    { .digest1 = "b81750d408faeb879a02f14cd8f42253308686fa",
      .name = "/scripts/init-top/ORDER" },
    { .digest1 = "47a8d6956a06cecf639af074b264bd1338c0942e",
      .name = "/scripts/init-top/all_generic_ide" },
    { .digest1 = "21044c1265a4b298dfd97ead49c355817b1a2493",
      .name = "/scripts/init-top/blacklist" }
};

ascii_event sml_ima_sig_sha256[9] = {
    { .digest1 = "bcb0e518b79de0d7f2cd20b8a29a7092e65db7ef",
      .name = "boot_aggregate" },
    { .digest1 = "539fdb622d9bc29e698e8cb87ad654b318844987",
      .name = "/init" },
    { .digest1 = "2675452da05e86c25345bc22d71b53fb1de3aea6",
      .name = "/usr/bin/sh"  },
    { .digest1 = "9b98ed341fd71c6841eadda983f0bd067d7aae61",
      .name = "/usr/lib/x86_64-linux-gnu/ld-2.31.so" },
    { .digest1 = "4e1485e0515360012ae54a4e7775a09039da4cd6",
      .name = "/etc/ld.so.cache" },
    { .digest1 = "dbfdd0da61d79f6185b053e793c5e56a85c23eee",
      .name = "/usr/lib/x86_64-linux-gnu/libc-2.31.so" },
    { .digest1 = "4ca22ff0b5a3f5cec29d40b1a53c19b34b5e5d9a",
      .name = "/conf/arch.conf" },
    { .digest1 = "9f51391fdcb905d92ca5ca433dd1a9945c883164",
      .name = "/conf/initramfs.conf" },
    { .digest1 = "6b60a8edd48a777ac2e05fdcad20d2af09e8489c",
      .name = "/scripts/functions" }
};

static void
check_eventlog(const char *file, ascii_event *ima_ascii_list, int n_ascii)
{
    TSS2_RC r;
    char *json_string;
    json_object
        *json_event_list = NULL,
        *json_ascii_list = NULL,
        *json_digests, *json_digest, *json_digest_ary0, *json_bin,
        *json_content; // *json_name;
    int n_bin, i;
    int jso_result;
    const char *digest1; // *name;
    uint32_t pcr_list[1] = { 10 };

    r = ifapi_read_ima_event_log(file, &pcr_list[0], 1, &json_event_list);
    assert_int_equal (r, TSS2_RC_SUCCESS);

    json_string = strdup(json_object_to_json_string_ext(json_event_list,
                                                        JSON_C_TO_STRING_PRETTY));
    assert_non_null(json_string);

    n_bin= json_object_array_length(json_event_list);

    assert_int_equal(n_ascii, n_bin);

    fprintf(stderr,"\n%s\n", json_string);


    for (i = 0; i < n_bin; i++) {
        IFAPI_EVENT event;
        json_bin =  json_object_array_get_idx(json_event_list, i);
        assert_non_null(json_bin);

        r = ifapi_json_IFAPI_EVENT_deserialize(json_bin,  &event,
                                               DIGEST_CHECK_ERROR);
        assert_int_equal(r, TSS2_RC_SUCCESS);

        jso_result = json_object_object_get_ex(json_bin, "digests", &json_digests);
        assert_int_not_equal(jso_result, 0);

        json_digest_ary0 =  json_object_array_get_idx(json_digests, 0);
        assert_non_null(json_digest_ary0);

        jso_result = json_object_object_get_ex(json_digest_ary0, "digest", &json_digest);
        assert_int_not_equal(jso_result, 0);

        digest1  = json_object_get_string(json_digest);
        assert_non_null(digest1);

        assert_string_equal(digest1, ima_ascii_list[i].digest1);

        jso_result = json_object_object_get_ex(json_bin, CONTENT, &json_content);
        assert_int_not_equal(jso_result, 0);

        ifapi_cleanup_event(&event);
    }

    assert_int_equal (r, TSS2_RC_SUCCESS);

    json_object_put(json_event_list);
    json_object_put(json_ascii_list);
    SAFE_FREE(json_string);
}


static void check_get_name(void **state)
{
    IFAPI_EVENT event;
    TSS2_RC r;
    char *name;
    char *json_str =
        "{" \
        "    \"recnum\":0," \
        "    \"pcr\":10," \
        "    \"digests\":[" \
        "      {" \
        "        \"hashAlg\":\"sha1\"," \
        "        \"digest\":\"1d8d532d463c9f8c205d0df7787669a85f93e260\"" \
        "      }" \
        "    ]," \
        "    \"content_type\":\"ima_template\"," \
        "    \"content\":{" \
        "      \"template_name\":\"ima-ng\"," \
        "      \"template_value\":\"1a000000736861313a0000000000000000000000000000000000000000000f000000626f6f745f61676772656761746500\"" \
        "    }" \
        "}";

    json_object *jso = json_tokener_parse(json_str);   \
    assert_non_null(jso);
    OpenSSL_add_all_digests();
    r = ifapi_json_IFAPI_EVENT_deserialize(jso, &event, DIGEST_CHECK_ERROR);
    assert_int_equal(r, TSS2_RC_SUCCESS);

    r = ifapi_get_ima_eventname(&event.content.ima_event, &name);
    assert_int_equal(r, TSS2_RC_SUCCESS);
    assert_string_equal(name, "boot_aggregate");
    json_object_put(jso);
    ifapi_cleanup_event(&event);
}

static void check_invalidate_event(void **state)
{
    IFAPI_EVENT event;
    TSS2_RC r;
    char *name;
    char *json_str =
        "{" \
        "    \"recnum\":0," \
        "    \"pcr\":10," \
        "    \"digests\":[" \
        "      {" \
        "        \"hashAlg\":\"sha1\"," \
        "        \"digest\":\"ffffffffffffffffffffffffffffffffffffffff\"" \
        "      }" \
        "    ]," \
        "    \"content_type\":\"ima_template\"," \
        "    \"content\":{" \
        "      \"template_name\":\"ima-ng\"," \
        "      \"template_value\":\"1a000000736861313a0000000000000000000000000000000000000000000f000000626f6f745f61676772656761746500\"" \
        "    }" \
        "}";

    json_object *jso = json_tokener_parse(json_str);   \
    assert_non_null(jso);
    OpenSSL_add_all_digests();

    /* Verification is not possible, but event can be deserialized. */
    r = ifapi_json_IFAPI_EVENT_deserialize(jso, &event, DO_NOT_CHECK_DIGEST);
    assert_int_equal(r, TSS2_RC_SUCCESS);

    r = ifapi_get_ima_eventname(&event.content.ima_event, &name);
    assert_int_equal(r, TSS2_RC_SUCCESS);
    assert_string_equal(name, "boot_aggregate");
    json_object_put(jso);
    ifapi_cleanup_event(&event);
}

static void
check_sml_ima_ng_sha1(void **state)
{
    check_eventlog("test/data/fapi/eventlog/sml-ima-ng-sha1.bin", sml_ima_ng_sha1, 6);
}

static void
check_sml_ima_sha1(void **state)
{
    check_eventlog("test/data/fapi/eventlog/sml-ima-sha1.bin", sml_ima_sha1, 12);
}

static void
check_sml_ima_sig_sha256(void **state)
{
    check_eventlog("test/data/fapi/eventlog/sml-ima-sig-sha256.bin", sml_ima_sig_sha256, 9);
}

int
main(int argc, char *argv[])
{
    const struct CMUnitTest tests[] = {
        cmocka_unit_test(check_invalidate_event),
        cmocka_unit_test(check_get_name),
        cmocka_unit_test(check_sml_ima_sha1),
        cmocka_unit_test(check_sml_ima_ng_sha1),
        cmocka_unit_test(check_sml_ima_sig_sha256),
    };
    return cmocka_run_group_tests(tests, NULL, NULL);
}
