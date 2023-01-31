/* SPDX-License-Identifier: BSD-2-Clause */
/*******************************************************************************
 * Copyright 2017-2018, Fraunhofer SIT sponsored by Infineon Technologies AG
 * All rights reserved.
 *******************************************************************************/

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <stdlib.h>
#include <stdio.h>
#include <inttypes.h>
#include <string.h>
#include <unistd.h>

#include "tss2_fapi.h"

#include "test-fapi.h"
#define LOGMODULE test
#include "util/log.h"
#include "util/aux_util.h"

#define PASSWORD "abc"

static TSS2_RC
auth_callback(
    char const *objectPath,
    char const *description,
    const char **auth,
    void *userData)
{
    UNUSED(description);
    UNUSED(userData);

    if (!objectPath) {
        return_error(TSS2_FAPI_RC_BAD_VALUE, "No path.");
    }

    *auth = PASSWORD;
    return TSS2_RC_SUCCESS;
}

/** Test the FAPI function FAPI_NvIncrement.
 *
 * Tested FAPI commands:
 *  - Fapi_Provision()
 *  - Fapi_Import()
 *  - Fapi_CreateNv()
 *  - Fapi_SetAuthCB()
 *  - Fapi_ChangeAuth()
 *  - Fapi_Delete()
 *  - Fapi_NvIncrement()
 *
 * Tested Policies:
 *  - PolicyAuthValue
 *  - PolicyCommandCode
 *
 * @param[in,out] context The FAPI_CONTEXT.
 * @retval EXIT_FAILURE
 * @retval EXIT_SUCCESS
 */
int
test_fapi_nv_increment(FAPI_CONTEXT *context)
{
    TSS2_RC r;
    char *nvPathCounter = "nv/Owner/myNV_Counter";
    char *policy_name = "/policy/pol_nv_change_auth";
    char *policy_file = TOP_SOURCEDIR "/test/data/fapi/policy/pol_nv_change_auth.json";
    FILE *stream = NULL;
    char *json_policy = NULL;
    long policy_size;

    r = Fapi_Provision(context, NULL, NULL, NULL);
    goto_if_error(r, "Error Fapi_Provision", error);

    r = pcr_reset(context, 16);
    goto_if_error(r, "Error pcr_reset", error);

    stream = fopen(policy_file, "r");
    if (!stream) {
        LOG_ERROR("File %s does not exist", policy_file);
        goto error;
    }
    fseek(stream, 0L, SEEK_END);
    policy_size = ftell(stream);
    fclose(stream);
    json_policy = malloc(policy_size + 1);
    goto_if_null(json_policy,
            "Could not allocate memory for the JSON policy",
            TSS2_FAPI_RC_MEMORY, error);
    stream = fopen(policy_file, "r");
    ssize_t ret = read(fileno(stream), json_policy, policy_size);
    if (ret != policy_size) {
        LOG_ERROR("IO error %s.", policy_file);
        goto error;
    }
    json_policy[policy_size] = '\0';

    r = Fapi_Import(context, policy_name, json_policy);
    goto_if_error(r, "Error Fapi_Import", error);

    /* Test no password, noda set */
    r = Fapi_CreateNv(context, nvPathCounter, "counter, noda", 0, policy_name, "abc");
    goto_if_error(r, "Error Fapi_CreateNv", error);

    r = Fapi_SetAuthCB(context, auth_callback, "");
    goto_if_error(r, "Error SetPolicyAuthCallback", error);

    r = Fapi_ChangeAuth(context, nvPathCounter, "abc");
    goto_if_error(r, "Error Fapi_CreateNv", error);

    r = Fapi_Delete(context, nvPathCounter);
    goto_if_error(r, "Error Fapi_NV_Undefine", error);

    /* Test no password, noda set */
    r = Fapi_CreateNv(context, nvPathCounter, "counter, noda", 0, "", "");
    goto_if_error(r, "Error Fapi_CreateNv", error);

    r = Fapi_NvIncrement(context, nvPathCounter);
    goto_if_error(r, "Error Fapi_CreateNv", error);

       r = Fapi_Delete(context, nvPathCounter);
    goto_if_error(r, "Error Fapi_NV_Undefine", error);

    /* Test with password noda set */
    r = Fapi_CreateNv(context, nvPathCounter, "counter, noda", 0, "", PASSWORD);
    goto_if_error(r, "Error Fapi_CreateNv", error);

    r = Fapi_SetAuthCB(context, auth_callback, "");
    goto_if_error(r, "Error SetPolicyAuthCallback", error);

    r = Fapi_NvIncrement(context, nvPathCounter);
    goto_if_error(r, "Error Fapi_CreateNv", error);

    r = Fapi_Delete(context, nvPathCounter);
    goto_if_error(r, "Error Fapi_NV_Undefine", error);

    /* Test no password, noda clear */
    r = Fapi_CreateNv(context, nvPathCounter, "counter", 0, "", "");
    goto_if_error(r, "Error Fapi_CreateNv", error);

    r = Fapi_NvIncrement(context, nvPathCounter);
    goto_if_error(r, "Error Fapi_CreateNv", error);

    r = Fapi_Delete(context, nvPathCounter);
    goto_if_error(r, "Error Fapi_NV_Undefine", error);

    /* Test with password noda clear */
    r = Fapi_CreateNv(context, nvPathCounter, "counter", 0, "", PASSWORD);
    goto_if_error(r, "Error Fapi_CreateNv", error);

    r = Fapi_SetAuthCB(context, auth_callback, "");
    goto_if_error(r, "Error SetPolicyAuthCallback", error);

    r = Fapi_NvIncrement(context, nvPathCounter);
    goto_if_error(r, "Error Fapi_CreateNv", error);

    r = Fapi_Delete(context, nvPathCounter);
    goto_if_error(r, "Error Fapi_NV_Undefine", error);


    r = Fapi_Delete(context, "/");
    goto_if_error(r, "Error Fapi_Delete", error);

    SAFE_FREE(json_policy);
    return EXIT_SUCCESS;

error:
    Fapi_Delete(context, "/");
    SAFE_FREE(json_policy);
    return EXIT_FAILURE;
}

int
test_invoke_fapi(FAPI_CONTEXT *context)
{
    return test_fapi_nv_increment(context);
}
