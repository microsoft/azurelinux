/* SPDX-License-Identifier: BSD-2-Clause */
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

int
main(int argc, char *argv[])
{
    uint32_t pcr_list[9] = { 0, 1, 2, 3, 4, 5, 6, 7, 8 };
    size_t pcr_list_size = 9;

    json_object *json_event_list = NULL;
    TSS2_RC r;

    r = ifapi_get_tcg_firmware_event_list(argv[1], pcr_list, pcr_list_size, &json_event_list);
    UNUSED(r);
}
