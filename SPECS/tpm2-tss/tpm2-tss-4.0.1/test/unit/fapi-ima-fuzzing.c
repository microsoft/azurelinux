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

int
main(int argc, char *argv[])
{
    uint32_t pcr_list[1] = { 10 };
    json_object *json_event_list = NULL;
    TSS2_RC r;

    r = ifapi_read_ima_event_log(argv[1], &pcr_list[0], 1, &json_event_list);
    UNUSED(r);
}
