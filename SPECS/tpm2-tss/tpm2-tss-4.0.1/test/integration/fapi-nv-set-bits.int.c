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

/** Test the FAPI function Fapi_NvSetBits.
 *
 * Tested FAPI commands:
 *  - Fapi_Provision()
 *  - Fapi_CreateNv()
 *  - Fapi_NvSetBits()
 *  - Fapi_Delete()
 *  - Fapi_SetAuthCB()
 *
 * @param[in,out] context The FAPI_CONTEXT.
 * @retval EXIT_FAILURE
 * @retval EXIT_SUCCESS
 */
int
test_fapi_nv_set_bits(FAPI_CONTEXT *context)
{
    TSS2_RC r;
    char *nvPathBitMap = "/nv/Owner/myNV_BitMap";

    r = Fapi_Provision(context, NULL, NULL, NULL);
    goto_if_error(r, "Error Fapi_Provision", error);

    r = Fapi_Provision(context, NULL, NULL, NULL);
    if (r != TSS2_FAPI_RC_ALREADY_PROVISIONED) {
        /* File exists or persistent key exists. */
        LOG_ERROR("Check whether provisioning directory exists failed.");
        goto error;
    }

    /* Test no password, noda set */
    r = Fapi_CreateNv(context, nvPathBitMap, "bitfield, noda", 0, "", "");
    goto_if_error(r, "Error Fapi_CreateNv", error);

    uint64_t bitmap = 0x0102030405060608;

    r = Fapi_NvSetBits(context, nvPathBitMap, bitmap);
    goto_if_error(r, "Error Fapi_SetBits", error);

    r = Fapi_Delete(context, nvPathBitMap);
    goto_if_error(r, "Error Fapi_Delete", error);

    /* Test with password noda set */
    r = Fapi_CreateNv(context, nvPathBitMap, "bitfield, noda", 0, "", PASSWORD);
    goto_if_error(r, "Error Fapi_CreateNv", error);

    r = Fapi_SetAuthCB(context, auth_callback, "");
    goto_if_error(r, "Error SetPolicyAuthCallback", error);

    r = Fapi_NvSetBits(context, nvPathBitMap, bitmap);
    goto_if_error(r, "Error Fapi_CreateNv", error);

    r = Fapi_Delete(context, nvPathBitMap);
    goto_if_error(r, "Error Fapi_Delete", error);

    /* Test no password, noda set */
    r = Fapi_CreateNv(context, nvPathBitMap, "bitfield, noda", 0, "", "");
    goto_if_error(r, "Error Fapi_CreateNv", error);

    r = Fapi_NvSetBits(context, nvPathBitMap, bitmap);
    goto_if_error(r, "Error Fapi_NvSetbits", error);

    r = Fapi_Delete(context, nvPathBitMap);
    goto_if_error(r, "Error Fapi_Delete", error);

    /* Test with password noda set */
    r = Fapi_CreateNv(context, nvPathBitMap, "bitfield, noda", 0, "", PASSWORD);
    goto_if_error(r, "Error Fapi_CreateNv", error);

    r = Fapi_SetAuthCB(context, auth_callback, "");
    goto_if_error(r, "Error SetPolicyAuthCallback", error);

    r = Fapi_NvSetBits(context, nvPathBitMap, bitmap);
    goto_if_error(r, "Error Fapi_SetBits", error);

    r = Fapi_Delete(context, nvPathBitMap);
    goto_if_error(r, "Error Fapi_Delete", error);


    r = Fapi_Delete(context, "/");

    goto_if_error(r, "Error Fapi_Delete", error);

    return EXIT_SUCCESS;

error:
    Fapi_Delete(context, "/");
    return EXIT_FAILURE;
}

int
test_invoke_fapi(FAPI_CONTEXT *context)
{
    return test_fapi_nv_set_bits(context);
}
