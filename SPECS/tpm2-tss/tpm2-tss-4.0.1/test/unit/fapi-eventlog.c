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
#include "tpm_json_serialize.h"
#include "ifapi_json_eventlog_serialize.h"
#include "ifapi_json_eventlog_deserialize.h"
#include "ifapi_eventlog.h"
#include "tpm_json_deserialize.h"
#include "ifapi_json_serialize.h"
#include "ifapi_json_deserialize.h"
#include "fapi_policy.h"

#include "util/aux_util.h"

#define LOGMODULE tests
#include "util/log.h"

static uint8_t *file_to_buffer(const char *filename, size_t *size)
{
    uint8_t *eventlog = NULL;
    size_t alloc_size = UINT16_MAX;
    size_t alloc_buf_size;
    size_t n_alloc = 1;
    size_t file_size = 0;
    size_t read_size = 0;

    FILE *fp = fopen(filename, "rb");
    if (!fp) {
        return NULL;
    }
    *size = 0;
    eventlog = calloc(1, alloc_size);
    if (!eventlog)
        return NULL;
    read_size = fread(eventlog, 1, alloc_size, fp);
    file_size += read_size;
    alloc_buf_size = alloc_size;

    while (file_size == alloc_buf_size) {
        n_alloc += 1;
        uint8_t* tmp_buff = calloc(1, alloc_size * n_alloc);
        if (!tmp_buff) {
            free(eventlog);
            return NULL;
        }
        alloc_buf_size = alloc_size * n_alloc;
        memcpy(&tmp_buff[0], &eventlog[0], file_size);
        free(eventlog);
        eventlog = tmp_buff;
        read_size = fread(&eventlog[file_size], 1, alloc_size, fp);
        file_size += read_size;
    }
    *size = file_size;
    if (*size) {
        return eventlog;
    } else {
        return NULL;
    }
}

uint32_t pcr_list[9] = { 0, 1, 2, 3, 4, 5, 6, 7, 8 };
uint32_t pcr_list2[1] = { 2  };

static void
check_eventlog(const char *file, uint32_t *pcr_list, size_t pcr_list_size, int n_events)
{
    TSS2_RC r;
    uint8_t *eventlog;
    size_t size;
    int i, n;
    char *json_string = NULL;
    json_object *json_event_list = NULL, *jso;
    IFAPI_EVENT event;

    /* Read file to get file size for comparison. */
    eventlog = file_to_buffer(file, &size);
    assert_non_null(eventlog);

    r = ifapi_get_tcg_firmware_event_list(file, pcr_list, pcr_list_size, &json_event_list);
    assert_int_equal (r, TSS2_RC_SUCCESS);

    json_string = strdup(json_object_to_json_string_ext(json_event_list, JSON_C_TO_STRING_PRETTY));
    assert_non_null(json_string);

    fprintf(stderr,"\n%s\n", json_string);

    n = json_object_array_length(json_event_list);

    for (i = 0; i < n; i++) {
        jso = json_object_array_get_idx(json_event_list, i);
        r = ifapi_json_IFAPI_EVENT_deserialize(jso, &event, DIGEST_CHECK_ERROR);
        assert_int_equal(r, TSS2_RC_SUCCESS);

        ifapi_cleanup_event(&event);
    }
    json_object_put(json_event_list);
    SAFE_FREE(json_string);
    SAFE_FREE(eventlog);
}

static void
check_bios_nuc(void **state)
{
    check_eventlog("test/data/fapi/eventlog/binary_measurements_nuc.bin", &pcr_list[0], 1, 2);
    check_eventlog("test/data/fapi/eventlog/binary_measurements_nuc.bin", &pcr_list[0], 3, 4);
    check_eventlog("test/data/fapi/eventlog/binary_measurements_nuc.bin", NULL, 0, 0);
}

static void
check_bios_pc_client(void **state)
{
    check_eventlog("test/data/fapi/eventlog/binary_measurements_pc_client.bin", &pcr_list[0], 1, 5);
    check_eventlog("test/data/fapi/eventlog/binary_measurements_pc_client.bin", &pcr_list[0], 3, 17);
    check_eventlog("test/data/fapi/eventlog/binary_measurements_pc_client.bin", NULL, 0, 0);
}

static void
check_event_uefiservices(void **state)
{
    check_eventlog("test/data/fapi/eventlog/binary_measurements_nuc.bin", &pcr_list2[0], 1, 1);
    check_eventlog("test/data/fapi/eventlog/event-uefiservices.bin", NULL, 0, 0);
}

static void
check_event_uefiaction(void **state)
{
    check_eventlog("test/data/fapi/eventlog/event-uefiaction.bin", NULL, 0, 0);
}

static void
check_event_uefivar(void **state)
{
    check_eventlog("test/data/fapi/eventlog/event-uefivar.bin", NULL, 0, 0);
}

static void
check_event(void **state)
{
    check_eventlog("test/data/fapi/eventlog/event.bin", NULL, 0, 0);
}

static void
check_specid_vendordata(void **state)
{
    check_eventlog("test/data/fapi/eventlog/specid-vendordata.bin", NULL, 0, 0);
}

int
main(int argc, char *argv[])
{
    const struct CMUnitTest tests[] = {
        cmocka_unit_test(check_bios_nuc),
        cmocka_unit_test(check_bios_pc_client),
        cmocka_unit_test(check_event_uefiservices),
        cmocka_unit_test(check_event_uefiaction),
        cmocka_unit_test(check_event_uefivar),
        cmocka_unit_test(check_event),
        cmocka_unit_test(check_specid_vendordata),
    };
    return cmocka_run_group_tests(tests, NULL, NULL);
}
