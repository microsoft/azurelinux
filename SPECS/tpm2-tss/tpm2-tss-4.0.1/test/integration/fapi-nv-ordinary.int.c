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

#define NV_SIZE 1200

#define PASSWORD "abc"
#define USER_DATA "my user data"

static char *password;

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

static TSS2_RC
action_callback(
    const char *objectPath,
    const char *action,
    void *userData)
{
    UNUSED(userData);

    ASSERT(objectPath != NULL);
    ASSERT(action != NULL);

    ASSERT(strlen(userData) == strlen((char*)USER_DATA));

    if (strcmp(objectPath, "/nv/Owner/myNV") != 0) {
        return_error(TSS2_FAPI_RC_BAD_VALUE, "Unexpected path");
    }

    if (strcmp(action, "myaction")) {
        LOG_ERROR("Bad action: %s", action);
        return TSS2_FAPI_RC_GENERAL_FAILURE;
    }
    return TSS2_RC_SUCCESS;

 error:
    exit(EXIT_FAILURE);
}

static char *
read_policy(FAPI_CONTEXT *context, char *policy_name)
{
    FILE *stream = NULL;
    long policy_size;
    char *json_policy = NULL;
    char policy_file[1024];

    if (snprintf(&policy_file[0], 1023, TOP_SOURCEDIR "/test/data/fapi/%s.json", policy_name) < 0)
        return NULL;

    stream = fopen(policy_file, "r");
    if (!stream) {
        LOG_ERROR("File %s does not exist", policy_file);
        return NULL;
    }
    fseek(stream, 0L, SEEK_END);
    policy_size = ftell(stream);
    fclose(stream);
    json_policy = malloc(policy_size + 1);
    return_if_null(json_policy,
            "Could not allocate memory for the JSON policy",
            NULL);
    stream = fopen(policy_file, "r");
    ssize_t ret = read(fileno(stream), json_policy, policy_size);
    if (ret != policy_size) {
        LOG_ERROR("IO error %s.", policy_file);
        return NULL;
    }
    json_policy[policy_size] = '\0';
    return json_policy;
}

/** Test the FAPI NV functions.
 *
 * Tested FAPI commands:
 *  - Fapi_Provision()
 *  - Fapi_Import()
 *  - Fapi_SetPolicyActionCB()
 *  - Fapi_CreateNv()
 *  - Fapi_NvWrite()
 *  - Fapi_NvRead()
 *  - Fapi_Delete()
 *  - Fapi_SetDescription()
 *  - Fapi_GetDescription()
 *  - Fapi_SetAuthCB()
 *
 * Tested Policies:
 *  - PolicyAction
 *
 * @param[in,out] context The FAPI_CONTEXT.
 * @retval EXIT_FAILURE
 * @retval EXIT_SUCCESS
 */
int
test_fapi_nv_ordinary(FAPI_CONTEXT *context)
{
    TSS2_RC r;
    char *nvPathOrdinary = "/nv/Owner/myNV";
    uint8_t data_src[NV_SIZE];
    uint8_t *data_dest = NULL;
    char *logData = NULL;
    size_t dest_size = NV_SIZE;
    char *description1 = "nvDescription";
    char *description2 = NULL;
    char *policy_action = "/policy/pol_action";
    char *policy_pcr8_0 = "/policy/pol_pcr8_0";
    char *json_policy = NULL;

    for (int i = 0; i < NV_SIZE; i++) {
        data_src[i] = (i % 10) + 1;
    }

    r = Fapi_Provision(context, NULL, NULL, NULL);
    goto_if_error(r, "Error Fapi_Provision", error);

    r = pcr_reset(context, 16);
    goto_if_error(r, "Error pcr_reset", error);

    json_policy = read_policy(context, policy_action);

    r = Fapi_Import(context, policy_action, json_policy);
    goto_if_error(r, "Error Fapi_Import", error);

    SAFE_FREE(json_policy);

    r = Fapi_SetPolicyActionCB(context, action_callback, USER_DATA);
    goto_if_error(r, "Error Fapi_SetPolicyActionCB", error);

    /* Test with policy action */
    r = Fapi_CreateNv(context, nvPathOrdinary, "noda", NV_SIZE, policy_action, "");
    goto_if_error(r, "Error Fapi_CreateNv", error);

    r = Fapi_NvWrite(context, nvPathOrdinary, &data_src[0], NV_SIZE);
    goto_if_error(r, "Error Fapi_NvWrite", error);

    r = Fapi_NvRead(context, nvPathOrdinary, &data_dest, &dest_size, &logData);
    goto_if_error(r, "Error Fapi_NvRead", error);
    ASSERT(data_dest != NULL);
    ASSERT(logData != NULL);
    ASSERT(strlen(logData) == 0);

    if (dest_size != NV_SIZE ||
        memcmp(data_src, data_dest, dest_size) != 0) {
        LOG_ERROR("Error: result of nv read is wrong.");
        goto error;
    }

    r = Fapi_Delete(context, nvPathOrdinary);
    goto_if_error(r, "Error Fapi_NV_Undefine", error);
    SAFE_FREE(data_dest);
    SAFE_FREE(logData);

    /* Test with pcr policy with pcr 8. */

    uint8_t *pcr_digest = NULL;
    char *pcrLog = NULL;
    size_t pcr_digest_size = 0;
    uint8_t zero_digest[32];
    memset(&zero_digest[0], 0, 32);

    r = Fapi_PcrRead(context, 8, &pcr_digest,
                     &pcr_digest_size, &pcrLog);
    goto_if_error(r, "Error Fapi_PcrRead", error);
    ASSERT(pcr_digest != NULL);
    ASSERT(pcrLog != NULL);

    if (memcmp(&pcr_digest[0], &zero_digest, pcr_digest_size) != 0) {
        SAFE_FREE(pcr_digest);
        SAFE_FREE(pcrLog);
        LOG_WARNING("PCR 8 is not zero. Test with pcr policy not executed.");
    } else {
        SAFE_FREE(pcr_digest);
        SAFE_FREE(pcrLog);
        json_policy = read_policy(context, policy_pcr8_0);

        r = Fapi_Import(context, policy_pcr8_0, json_policy);
        goto_if_error(r, "Error Fapi_Import", error);

        SAFE_FREE(json_policy);

        /* Test with policy action */
        r = Fapi_CreateNv(context, nvPathOrdinary, "noda", NV_SIZE, policy_pcr8_0, "");
        goto_if_error(r, "Error Fapi_CreateNv", error);

        r = Fapi_NvWrite(context, nvPathOrdinary, &data_src[0], NV_SIZE);
        goto_if_error(r, "Error Fapi_NvWrite", error);

        data_dest = NULL;
        logData = NULL;
        r = Fapi_NvRead(context, nvPathOrdinary, &data_dest, &dest_size, &logData);
        goto_if_error(r, "Error Fapi_NvRead", error);
        ASSERT(data_dest != NULL);
        ASSERT(logData != NULL);
        ASSERT(strlen(logData) == 0);

        if (dest_size != NV_SIZE ||
            memcmp(data_src, data_dest, dest_size) != 0) {
            LOG_ERROR("Error: result of nv read is wrong.");
            goto error;
        }

        r = Fapi_Delete(context, nvPathOrdinary);
        goto_if_error(r, "Error Fapi_NV_Undefine", error);
        SAFE_FREE(data_dest);
        SAFE_FREE(logData);
    }

    /* Empty auth noda set */
    r = Fapi_CreateNv(context, nvPathOrdinary, "noda", NV_SIZE, "", "");
    goto_if_error(r, "Error Fapi_CreateNv", error);

    r = Fapi_NvWrite(context, nvPathOrdinary, &data_src[0], NV_SIZE);
    goto_if_error(r, "Error Fapi_NvWrite", error);

    data_dest = NULL;
    logData = NULL;
    r = Fapi_NvRead(context, nvPathOrdinary, &data_dest, &dest_size, &logData);
    goto_if_error(r, "Error Fapi_NvRead", error);
    ASSERT(data_dest != NULL);
    ASSERT(logData != NULL);
    ASSERT(strlen(logData) == 0);

    if (dest_size != NV_SIZE ||
        memcmp(data_src, data_dest, dest_size) != 0) {
        LOG_ERROR("Error: result of nv read is wrong.");
        goto error;
    }

    r = Fapi_Delete(context, nvPathOrdinary);
    goto_if_error(r, "Error Fapi_NV_Undefine", error);
    SAFE_FREE(data_dest);
    SAFE_FREE(logData);

    r = Fapi_SetAuthCB(context, auth_callback, "");
    goto_if_error(r, "Error Fapi_SetAuthCB", error);

    /* Password set and noda set */
    password = PASSWORD;
    r = Fapi_CreateNv(context, nvPathOrdinary, "", NV_SIZE, "", password);
    goto_if_error(r, "Error Fapi_CreateNv", error);

    r = Fapi_SetAuthCB(context, auth_callback, "");
    goto_if_error(r, "Error SetPolicyAuthCallback", error);

    r = Fapi_NvWrite(context, nvPathOrdinary, &data_src[0], NV_SIZE);
    goto_if_error(r, "Error Fapi_NvWrite", error);

    data_dest = NULL;
    logData = NULL;
    r = Fapi_NvRead(context, nvPathOrdinary, &data_dest, &dest_size, &logData);
    goto_if_error(r, "Error Fapi_NvRead", error);
    ASSERT(data_dest != NULL);
    ASSERT(logData != NULL);
    ASSERT(strlen(logData) == 0);

    if (dest_size != NV_SIZE ||
        memcmp(data_src, data_dest, dest_size) != 0) {
        LOG_ERROR("Error: result of nv read is wrong.");
        goto error;
    }

    r = Fapi_Delete(context, nvPathOrdinary);
    goto_if_error(r, "Error Fapi_NV_Undefine", error);
    SAFE_FREE(data_dest);
    SAFE_FREE(logData);

    /* Empty auth noda clear */
    password = "";
    r = Fapi_CreateNv(context, nvPathOrdinary, "", NV_SIZE, "", "");
    goto_if_error(r, "Error Fapi_CreateNv", error);

    r = Fapi_SetDescription(context, nvPathOrdinary, description1);
    goto_if_error(r, "Error Fapi_SetDescription", error);

    r = Fapi_GetDescription(context, nvPathOrdinary, &description2);
    goto_if_error(r, "Error Fapi_GetDescription", error);
    ASSERT(description2 != NULL);

    if (strcmp(description1, description2) != 0) {
        goto_if_error(r, "Different descriptions", error);
    }

    r = Fapi_NvWrite(context, nvPathOrdinary, &data_src[0], NV_SIZE);
    goto_if_error(r, "Error Fapi_NvWrite", error);

    data_dest = NULL;
    logData = NULL;
    r = Fapi_NvRead(context, nvPathOrdinary, &data_dest, &dest_size, &logData);
    goto_if_error(r, "Error Fapi_NvRead", error);
    ASSERT(data_dest != NULL);
    ASSERT(logData != NULL);
    ASSERT(strlen(logData) == 0);

    if (dest_size != NV_SIZE ||
        memcmp(data_src, data_dest, dest_size) != 0) {
        LOG_ERROR("Error: result of nv read is wrong.");
        goto error;
    }

    r = Fapi_Delete(context, nvPathOrdinary);
    goto_if_error(r, "Error Fapi_NV_Undefine", error);
    SAFE_FREE(data_dest);
    SAFE_FREE(logData);

    /* Password set and noda clear  */
    password = PASSWORD;
    r = Fapi_CreateNv(context, nvPathOrdinary, "", NV_SIZE, "", password);
    goto_if_error(r, "Error Fapi_CreateNv", error);

    r = Fapi_SetAuthCB(context, auth_callback, "");
    goto_if_error(r, "Error SetPolicyAuthCallback", error);

    r = Fapi_NvWrite(context, nvPathOrdinary, &data_src[0], NV_SIZE);
    goto_if_error(r, "Error Fapi_NvWrite", error);

    data_dest = NULL;
    logData = NULL;
    r = Fapi_NvRead(context, nvPathOrdinary, &data_dest, &dest_size, &logData);
    goto_if_error(r, "Error Fapi_NvRead", error);
    ASSERT(data_dest != NULL);
    ASSERT(logData != NULL);
    ASSERT(strlen(logData) == 0);

    if (dest_size != NV_SIZE ||
        memcmp(data_src, data_dest, dest_size) != 0) {
        LOG_ERROR("Error: result of nv read is wrong.");
        goto error;
    }
    r = Fapi_Delete(context, nvPathOrdinary);
    goto_if_error(r, "Error Fapi_NV_Undefine", error);

    r = Fapi_Delete(context, "/");
    goto_if_error(r, "Error Fapi_Delete", error);

    SAFE_FREE(data_dest);
    SAFE_FREE(logData);
    SAFE_FREE(description2);
    SAFE_FREE(json_policy);
    return EXIT_SUCCESS;

error:
    Fapi_Delete(context, "/");
    SAFE_FREE(data_dest);
    SAFE_FREE(logData);
    SAFE_FREE(description2);
    SAFE_FREE(json_policy);
    return EXIT_FAILURE;
}

int
test_invoke_fapi(FAPI_CONTEXT *context)
{
    return test_fapi_nv_ordinary(context);
}
