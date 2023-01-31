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

#include "tss2_fapi.h"

#define LOGMODULE test
#include "util/log.h"
#include "util/aux_util.h"
#include "test-fapi.h"

#define NV_SIZE 32

#define PASSWORD "abc"

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

    *auth = password;
    return TSS2_RC_SUCCESS;
}


/** Test the FAPI function FAPI_NvExtend.
 *
 * Tested FAPI commands:
 *  - Fapi_Provision()
 *  - Fapi_CreateNv()
 *  - Fapi_NvExtend()
 *  - Fapi_Delete()
 *  - Fapi_SetAuthCB()
 *
 * @param[in,out] context The FAPI_CONTEXT.
 * @retval EXIT_FAILURE
 * @retval EXIT_SUCCESS
 */
int
test_fapi_nv_extend(FAPI_CONTEXT *context)
{
    TSS2_RC r;
    char *nvPathExtend = "/nv/Owner/myNVextend";
    uint8_t *data_dest = NULL;
    char *log = NULL;
    size_t dest_size;

    r = Fapi_Provision(context, NULL, NULL, NULL);
    goto_if_error(r, "Error Fapi_Provision", error);

    /* Test no password, noda set */
    r = Fapi_CreateNv(context, nvPathExtend, "pcr, noda", 0, "", "");
    goto_if_error(r, "Error Fapi_CreateNv", error);

    uint8_t data_src[NV_SIZE] = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9,
                                 0, 1, 2, 3, 4, 5, 6, 7, 8, 9,
                                 0, 1, 2, 3, 4, 5, 6, 7, 8, 9,
                                 0, 1
                                };


    r = Fapi_NvExtend(context, nvPathExtend, &data_src[0], NV_SIZE, "{ \"test\": \"myfile\" }");
    goto_if_error(r, "Error Fapi_NV_EXTEND", error);

    r = Fapi_NvRead(context, nvPathExtend, &data_dest, &dest_size, &log);
    goto_if_error(r, "Error Fapi_NvRead", error);
    ASSERT(data_dest != NULL);
    ASSERT(log != NULL);
    LOG_INFO("\nTEST_JSON\nLog:\n%s\nEND_JSON", log);
    char *fields_log1[] =  { "0", "digests", "0", "digest" };

    if (strcmp(FAPI_PROFILE, "P_ECC384") == 0) {
        CHECK_JSON_FIELDS(log, fields_log1,
                          "c8ffec7d7d70c61b16adaab88925a1759b94cf6b50669b04aef1a8427fabb131eafbf9a21e3b8bddd9c5d5e7",
                          error);
    } else {
        CHECK_JSON_FIELDS(log, fields_log1,
                          "dcb1ac4a5de370cad091c13f13aee2f936c278fa05d264653c0c1321852a35e8",
                          error);
    }

    ASSERT(strlen(log) > ASSERT_SIZE);

    fprintf(stderr, "\nLog:\n%s\n", log);
    SAFE_FREE(data_dest);

    r = Fapi_NvExtend(context, nvPathExtend, &data_src[0], NV_SIZE, "{ \"test\": \"myfile\" }");
    goto_if_error(r, "Error Fapi_NV_EXTEND", error);

    SAFE_FREE(log);
    data_dest = NULL;
    log = NULL;
    r = Fapi_NvRead(context, nvPathExtend, &data_dest, &dest_size, &log);
    goto_if_error(r, "Error Fapi_NvRead", error);
    ASSERT(data_dest != NULL);
    ASSERT(log != NULL);
    ASSERT(strlen(log) > ASSERT_SIZE);
    LOG_INFO("\nTEST_JSON\nLog:\n%s\nEND_JSON", log);
    char *fields_log2[] =  { "1", "digests", "0", "digest" };

    if (strcmp(FAPI_PROFILE, "P_ECC384") == 0) {
        CHECK_JSON_FIELDS(log, fields_log2,
                          "c8ffec7d7d70c61b16adaab88925a1759b94cf6b50669b04aef1a8427fabb131eafbf9a21e3b8bddd9c5d5e7",
                          error);
    } else {
        CHECK_JSON_FIELDS(log, fields_log2,
                          "dcb1ac4a5de370cad091c13f13aee2f936c278fa05d264653c0c1321852a35e8",
                          error);
    }

    fprintf(stderr, "\nLog:\n%s\n", log);

    r = Fapi_Delete(context, nvPathExtend);
    goto_if_error(r, "Error Fapi_NV_Undefine", error);

    r = Fapi_SetAuthCB(context, auth_callback, "");
    goto_if_error(r, "Error SetPolicyAuthCallback", error);

    /* Test with password noda  set */
    password = PASSWORD;
    r = Fapi_CreateNv(context, nvPathExtend, "pcr, noda", 0, "", PASSWORD);
    goto_if_error(r, "Error Fapi_CreateNv", error);

    r = Fapi_SetAuthCB(context, auth_callback, "");
    goto_if_error(r, "Error SetPolicyAuthCallback", error);

    r = Fapi_NvExtend(context, nvPathExtend, &data_src[0], NV_SIZE, "{ \"test\": \"myfile\" }");
    goto_if_error(r, "Error Fapi_NV_EXTEN", error);

    r = Fapi_Delete(context, nvPathExtend);
    goto_if_error(r, "Error Fapi_NV_Undefine", error);

    /* Test no password, noda clear */
    password = "";
    r = Fapi_CreateNv(context, nvPathExtend, "pcr", 0, "", "");
    goto_if_error(r, "Error Fapi_CreateNv", error);

    r = Fapi_NvExtend(context, nvPathExtend, &data_src[0], NV_SIZE, "{ \"test\": \"myfile\" }");
    goto_if_error(r, "Error Fapi_NV_EXTEN", error);

    r = Fapi_Delete(context, nvPathExtend);
    goto_if_error(r, "Error Fapi_NV_Undefine", error);

    /* Test with password noda clear */
    password = PASSWORD;
    r = Fapi_CreateNv(context, nvPathExtend, "pcr", 0, "", PASSWORD);
    goto_if_error(r, "Error Fapi_CreateNv", error);

    r = Fapi_SetAuthCB(context, auth_callback, "");
    goto_if_error(r, "Error SetPolicyAuthCallback", error);

    r = Fapi_NvExtend(context, nvPathExtend, &data_src[0], NV_SIZE, "{ \"test\": \"myfile\" }");
    goto_if_error(r, "Error Fapi_NV_EXTEN", error);

    r = Fapi_Delete(context, nvPathExtend);
    goto_if_error(r, "Error Fapi_NV_Undefine", error);

    r = Fapi_Delete(context, "/");
    goto_if_error(r, "Error Fapi_Delete", error);

    SAFE_FREE(log);
    SAFE_FREE(data_dest);
    return EXIT_SUCCESS;

error:
    Fapi_Delete(context, "/");
    SAFE_FREE(log);
    SAFE_FREE(data_dest);
    return EXIT_FAILURE;
}

int
test_invoke_fapi(FAPI_CONTEXT *context)
{
    return test_fapi_nv_extend(context);
}
