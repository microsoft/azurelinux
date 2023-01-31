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

#define NV_SIZE 10
#define APP_DATA_SIZE 10*1024*1024

/** Test the FAPI policy PolicyNvWritten.
 *
 * Tested FAPI commands:
 *  - Fapi_Provision()
 *  - Fapi_CreateNv()
 *  - Fapi_SetAppData()
 *  - Fapi_GetAppData()
 *  - Fapi_NvWrite()
 *  - Fapi_Delete()
 *
 * Tested Policies:
 *  - PolicyNvWritten
 *
 * @param[in,out] context The FAPI_CONTEXT.
 * @retval EXIT_FAILURE
 * @retval EXIT_SUCCESS
 */
int
test_fapi_nv_written_policy(FAPI_CONTEXT *context)
{
    TSS2_RC r;
    char *nvPathOrdinary = "/nv/Owner/myNV";
    char *policy_name =  "/policy/pol_nv_written";
    char *policy_file = TOP_SOURCEDIR "/test/data/fapi/policy/pol_nv_written.json";
    FILE *stream = NULL;
    char *json_policy = NULL;
    long policy_size;
    uint8_t *appDataOut = NULL;
    size_t appDataOutSize, i;
    uint8_t *appDataIn = NULL;

    r = Fapi_Provision(context, NULL, NULL, NULL);
    goto_if_error(r, "Error Fapi_Provision", error);

    uint8_t data_src[NV_SIZE] = { 0, 1, 2, 3, 4, 5, 6, 7, 8, 9};

    appDataIn = calloc(1, APP_DATA_SIZE);
    if (!appDataIn) {
        LOG_ERROR("Out of memory.");
        goto error;
    }
    for (i = 0; i < APP_DATA_SIZE; i++)
        appDataIn[i] = i % 256;

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

    /* Empty auth noda set */
    r = Fapi_CreateNv(context, nvPathOrdinary, "noda", 10, policy_name, "");
    goto_if_error(r, "Error Fapi_CreateNv", error);

    r = Fapi_SetAppData(context, nvPathOrdinary, appDataIn, APP_DATA_SIZE);
    goto_if_error(r, "Error Fapi_SetAppData", error);

    r = Fapi_GetAppData(context, nvPathOrdinary, &appDataOut, &appDataOutSize);
    goto_if_error(r, "Error Fapi_GetAppData", error);
    ASSERT(appDataOut != NULL);

    if (APP_DATA_SIZE != appDataOutSize ||
            memcmp(appDataOut, &appDataIn[0], appDataOutSize) != 0) {
        LOG_ERROR("Error: AppData  equal to origin");
        goto error;
    }

    r = Fapi_NvWrite(context, nvPathOrdinary, &data_src[0], NV_SIZE);
    goto_if_error(r, "Error Fapi_NvWrite", error);

    r = Fapi_Delete(context, nvPathOrdinary);
    goto_if_error(r, "Error Fapi_NV_Undefine", error);

    r = Fapi_Delete(context, "/");
    goto_if_error(r, "Error Fapi_Delete", error);


    SAFE_FREE(json_policy);
    SAFE_FREE(appDataOut);
    SAFE_FREE(appDataIn);

    return EXIT_SUCCESS;

error:
    Fapi_Delete(context, "/");
    SAFE_FREE(json_policy);
    SAFE_FREE(appDataOut);
    SAFE_FREE(appDataIn);

    return EXIT_FAILURE;
}

int
test_invoke_fapi(FAPI_CONTEXT *context)
{
    return test_fapi_nv_written_policy(context);
}
