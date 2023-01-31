/* SPDX-License-Identifier: BSD-2-Clause */
/*******************************************************************************
 * Copyright 2017-2018, Fraunhofer SIT sponsored by Infineon Technologies AG
 * All rights reserved.
 *******************************************************************************/

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif
#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>
#include <json-c/json.h>
#include <json-c/json_util.h>
#include <json-c/json_tokener.h>

#include "tss2_fapi.h"

#include "test-fapi.h"
#define LOGMODULE test
#include "util/log.h"
#include "util/aux_util.h"

#define EVENT_SIZE 10

/** Test the wrong paths for object creation functions.
 *
 * Tested FAPI commands:
 *  - Fapi_Provision()
 *  - Fapi_CreateKey()
 *  - Fapi_Delete()
 *
 * @param[in,out] context The FAPI_CONTEXT.
 * @retval EXIT_FAILURE
 * @retval EXIT_SUCCESS
 */
int
test_fapi_wrong_path(FAPI_CONTEXT *context)
{
    TSS2_RC r;

    r = Fapi_Provision(context, NULL, NULL, NULL);

    goto_if_error(r, "Error Fapi_Provision", error);

    r = Fapi_CreateKey(context, "myKey", "sign,noDa", "", NULL);

    if (r == TSS2_RC_SUCCESS) {
        LOG_ERROR( "Wrong key path not detected");
        goto error;
    }

    if (r !=  TSS2_FAPI_RC_BAD_PATH) {
        goto_if_error(r, "Wrong return code", error);
    }

    r = Fapi_CreateKey(context, "/HE/SRK/myKey", "sign,noDa", "", NULL);

    if (r == TSS2_RC_SUCCESS) {
        LOG_ERROR( "Wrong key path not detected");
        goto error;
    }

    if (r !=  TSS2_FAPI_RC_BAD_PATH) {
        goto_if_error(r, "Wrong return code", error);
    }

    r = Fapi_CreateKey(context, "/HS/EK/Key", "sign,noDa", "", NULL);

    if (r == TSS2_RC_SUCCESS) {
        LOG_ERROR( "Wrong key path not detected");
        goto error;
    }

    if (r !=  TSS2_FAPI_RC_BAD_PATH) {
        goto_if_error(r, "Error Fapi_CreateKey", error);
    }

    r = Fapi_CreateNv(context, "myNv", "noda", 10, "", "");

    if (r == TSS2_RC_SUCCESS) {
        LOG_ERROR( "Wrong key path not detected");
        goto error;
    }

    if (r !=  TSS2_FAPI_RC_BAD_PATH) {
        goto_if_error(r, "Error Fapi_CreateNv", error);
    }

    r = Fapi_CreateNv(context, "/nv/../Owner/myNv", "noda,0xff", 10, "", "");
    if (r == TSS2_RC_SUCCESS) {
        goto_if_error(r, "Bad character in path was not detected.", error);
    }
    if (r != TSS2_FAPI_RC_BAD_PATH) {
        goto_if_error(r, "Wrong return code for bad characters in path.", error);
    }

    r = Fapi_CreateKey(context, "/HS/../EK/Key", "sign,noDa", "", NULL);
    if (r == TSS2_RC_SUCCESS) {
        goto_if_error(r, "Bad character in path was not detected.", error);
    }
    if (r != TSS2_FAPI_RC_BAD_PATH) {
        goto_if_error(r, "Wrong return code for bad characters in path.", error);
    }

    r = Fapi_Delete(context, "/HS/../EK/Key");
    if (r == TSS2_RC_SUCCESS) {
        goto_if_error(r, "Bad character in path was not detected.", error);
    }
    if (r != TSS2_FAPI_RC_BAD_PATH) {
        goto_if_error(r, "Wrong return code for bad characters in path.", error);
    }

    Fapi_Delete(context, "/");

    return EXIT_SUCCESS;

 error:
    Fapi_Delete(context, "/");
    return EXIT_FAILURE;
}

int
test_invoke_fapi(FAPI_CONTEXT *fapi_context)
{
    return test_fapi_wrong_path(fapi_context);
}
