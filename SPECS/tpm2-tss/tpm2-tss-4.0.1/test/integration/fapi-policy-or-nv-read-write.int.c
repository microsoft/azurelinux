/* SPDX-License-Identifier: BSD-2-Clause */
/*******************************************************************************
 * Copyright 2017-2018, Fraunhofer SIT sponsored by Infineon Technologies AG
 * All rights reserved.
 *******************************************************************************/

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <stdbool.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <errno.h>
#include <fcntl.h>
#include <unistd.h>
#include <assert.h>

#include "tss2_fapi.h"

#include "test-fapi.h"

#define LOGMODULE test
#include "util/log.h"
#include "util/aux_util.h"

#define PASSWORD1 "abc"
#define PASSWORD2 "def"
#define SIGN_TEMPLATE  "sign,noDa"
#define NV_SIZE 10

static bool cb_branch_called = false;
static bool cb_auth_called = false;
static bool written = false;

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

    if (strcmp(objectPath, "/nv/Owner/foo1") == 0)
        *auth = PASSWORD1;
    else
        *auth = PASSWORD2;
    cb_auth_called = true;
    return TSS2_RC_SUCCESS;
}

static TSS2_RC
branch_callback(
    char   const *objectPath,
    char   const *description,
    char  const **branchNames,
    size_t        numBranches,
    size_t       *selectedBranch,
    void         *userData)
{
    UNUSED(description);
    UNUSED(userData);
    UNUSED(branchNames);

    if (strcmp(objectPath, "/nv/Owner/useful") != 0) {
        return_error(TSS2_FAPI_RC_BAD_VALUE, "Unexpected path");
    }

    if (numBranches != 2) {
        LOG_ERROR("Wrong number of branches");
        return TSS2_FAPI_RC_GENERAL_FAILURE;
    }

    if (written) {
        *selectedBranch = 1;
    } else {
        written = true;
        *selectedBranch = 0;
    }
    cb_branch_called = true;
    return TSS2_RC_SUCCESS;
}


/** Test the FAPI for PolicyOr with a different policy for read and write.
 *
 * The write to NV ram will be authorized by two secrets.
 *
 * Tested FAPI commands:
 *  - Fapi_Provision()
 *  - Fapi_Import()
 *  - Fapi_CreateNv()
 *  - Fapi_NvWrite()
 *  - Fapi_Nvread()
 *  - Fapi_SetBranchCB()
 *  - Fapi_SetAuthCB()
 *  - Fapi_Delete()
 *
 * Tested Policies:
 *  - PolicyOr
 *  - PolicySecret
 *  - PolicyCommandCode
 *
 * @param[in,out] context The FAPI_CONTEXT.
 * @retval EXIT_FAILURE
 * @retval EXIT_SUCCESS
 */
int
test_fapi_policy_or_nv_read_write(FAPI_CONTEXT *context)
{
    TSS2_RC r;
    char *policy_name = "/policy/pol_or_read_write_secret";
    char *policy_file = TOP_SOURCEDIR "/test/data/fapi/policy/pol_or_read_write_secret.json";
    FILE *stream = NULL;
    char *json_policy = NULL;
    long policy_size;
    uint8_t data_src[NV_SIZE];
    size_t dest_size = NV_SIZE;
    uint8_t *data_dest = NULL;

    for (int i = 0; i < NV_SIZE; i++) {
        data_src[i] = (i % 10) + 1;
    }

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

    r = Fapi_SetBranchCB(context, branch_callback, NULL);
    goto_if_error(r, "Error SetPolicybranchselectioncallback", error);

    r = Fapi_SetAuthCB(context, auth_callback, "");
    goto_if_error(r, "Error Fapi_SetAuthCB", error);

    r = Fapi_CreateNv(context, "/nv/Owner/foo1", "noda", NV_SIZE, "", PASSWORD1);
    goto_if_error(r, "Error Fapi_CreateNv", error);

    r = Fapi_CreateNv(context, "/nv/Owner/foo2", "noda", NV_SIZE, "", PASSWORD2);
    goto_if_error(r, "Error Fapi_CreateNv", error);

    r = Fapi_CreateNv(context, "/nv/Owner/useful", "noda", NV_SIZE, policy_name, "");
    goto_if_error(r, "Error Fapi_CreateNv", error);

    r = Fapi_NvWrite(context, "/nv/Owner/useful", &data_src[0], NV_SIZE);
    goto_if_error(r, "Error Fapi_NvWrite", error);

    r = Fapi_NvRead(context, "/nv/Owner/useful", &data_dest, &dest_size, NULL);
    goto_if_error(r, "Error Fapi_NvRead", error);
    assert(data_dest != NULL);

    if (dest_size != NV_SIZE ||
        memcmp(data_src, data_dest, dest_size) != 0) {
        LOG_ERROR("Error: result of nv read is wrong.");
        goto error;
    }
    SAFE_FREE(data_dest);

    r = Fapi_Delete(context, "/");
    goto_if_error(r, "Error Fapi_Delete", error);

    SAFE_FREE(json_policy);

    if (!cb_branch_called) {
        LOG_ERROR("Branch selection callback was not called.");
        return EXIT_FAILURE;
    }
    if (!cb_auth_called) {
        LOG_ERROR("Auth value callback was not called.");
        return EXIT_FAILURE;
    }

    return EXIT_SUCCESS;

error:
    SAFE_FREE(data_dest);
    Fapi_Delete(context, "/");
    SAFE_FREE(json_policy);
    return EXIT_FAILURE;
}

int
test_invoke_fapi(FAPI_CONTEXT *fapi_context)
{
    return test_fapi_policy_or_nv_read_write(fapi_context);
}
