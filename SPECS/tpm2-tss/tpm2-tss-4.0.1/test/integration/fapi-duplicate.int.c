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
#include <unistd.h>
#include <string.h>

#include "tss2_fapi.h"

#include "test-fapi.h"
#define LOGMODULE test
#include "util/log.h"
#include "util/aux_util.h"

#define SIZE 2000

/** Test the FAPI functions for key duplication.
 *
 * Tested FAPI commands:
 *  - Fapi_Provision()
 *  - Fapi_Import()
 *  - Fapi_CreateKey()
 *  - Fapi_ExportKey()
 *  - Fapi_Delete()
 *
 * Tested Policies:
 *  - PolicyDuplicationSelect
 *
 * @param[in,out] context The FAPI_CONTEXT.
 * @retval EXIT_FAILURE
 * @retval EXIT_SUCCESS
 */
int
test_fapi_duplicate(FAPI_CONTEXT *context)
{
    TSS2_RC r;
    char *policy_name = "/policy/pol_duplicate";
    char *policy_file = TOP_SOURCEDIR "/test/data/fapi/policy/pol_duplicate.json";
    FILE *stream = NULL;
    char *json_policy = NULL;
    long policy_size;
    char *json_duplicate = NULL;
    char *json_string_pub_key = NULL;

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
    goto_if_error(r, "Error Fapi_List", error);

    r = Fapi_CreateKey(context, "HS/SRK/myCryptKey", "restricted,decrypt,noDa",
                       "", NULL);
    goto_if_error(r, "Error Fapi_CreateKey", error);

    r = Fapi_ExportKey(context, "HS/SRK/myCryptKey", NULL, &json_string_pub_key);
    goto_if_error(r, "Error Fapi_CreateKey", error);
    ASSERT(json_string_pub_key != NULL);
    ASSERT(strlen(json_string_pub_key) > ASSERT_SIZE);

    r = Fapi_Import(context, "ext/myNewParent", json_string_pub_key);
    goto_if_error(r, "Error Fapi_Import", error);

    r = Fapi_CreateKey(context, "HS/SRK/myCryptKey/myCryptKey2",
                       "exportable,decrypt,noDa", policy_name, NULL);
    goto_if_error(r, "Error Fapi_CreateKey", error);

    r = Fapi_ExportKey(context, "HS/SRK/myCryptKey/myCryptKey2",
                       "ext/myNewParent", &json_duplicate);
    goto_if_error(r, "Error Fapi_CreateKey", error);
    ASSERT(json_duplicate != NULL);
    ASSERT(strlen(json_duplicate) > ASSERT_SIZE);

    LOG_INFO("\nTEST_JSON\nExport Data:\n%s\nEND_JSON", json_duplicate);
    char *duplicate_check[] = { "duplicate" };

    CHECK_JSON_FIELDS(json_duplicate, duplicate_check, "", error);
    r = Fapi_Import(context, "importedKey", json_duplicate);
    goto_if_error(r, "Error Fapi_Import", error);

    fprintf(stderr, "Duplicate:\n%s\n", json_duplicate);

    r = Fapi_Delete(context, "/");
    goto_if_error(r, "Error Fapi_Delete", error);

    SAFE_FREE(json_string_pub_key);
    SAFE_FREE(json_duplicate);
    SAFE_FREE(json_policy);
    return EXIT_SUCCESS;

error:
    Fapi_Delete(context, "/");
    SAFE_FREE(json_string_pub_key);
    SAFE_FREE(json_duplicate);
    SAFE_FREE(json_policy);
    return EXIT_FAILURE;
}

int
test_invoke_fapi(FAPI_CONTEXT *fapi_context)
{
    return test_fapi_duplicate(fapi_context);
}
