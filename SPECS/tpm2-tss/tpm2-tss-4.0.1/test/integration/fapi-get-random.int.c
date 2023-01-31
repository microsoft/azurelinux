/* SPDX-License-Identifier: BSD-2-Clause */
/*******************************************************************************
 * Copyright 2017-2018, Fraunhofer SIT sponsored by Infineon Technologies AG
 * All rights reserved.
 *******************************************************************************/

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <stdlib.h>

#include "tss2_fapi.h"
#include "test-fapi.h"

#define LOGMODULE test
#include "util/log.h"
#include "util/aux_util.h"

/** Test the FAPI function FAPI_GetRandom and async invocations.
 *
 * Tested FAPI commands:
 *  - Fapi_Provision()
 *  - Fapi_GetRandom_Async()
 *  - Fapi_GetRandom_Finish()
 *  - Fapi_GetPollHandles()
 *  - Fapi_GetRandom()
 *  - Fapi_Delete()
 *
 * @param[in,out] context The FAPI_CONTEXT.
 * @retval EXIT_FAILURE
 * @retval EXIT_SUCCESS
 */
int
test_fapi_get_random(FAPI_CONTEXT *context)
{

    TSS2_RC r;
    FAPI_POLL_HANDLE *handles;
    size_t            num_handles;
    /* Ensure that more than one call of Esys_GetRandom is necessary */
    size_t  bytesRequested = sizeof(TPMU_HA) + 10;
    uint8_t *randomBytes = NULL;


    r = Fapi_Provision(context, NULL, NULL, NULL);
    goto_if_error(r, "Error Fapi_Provision", error);

    r = Fapi_GetRandom_Async(context, bytesRequested);
    goto_if_error(r, "GetRandom_Async", error);

    do {
        r = Fapi_GetPollHandles(context, &handles, &num_handles);
        if (r == TSS2_RC_SUCCESS) {
            poll(handles, num_handles, 99);
            Fapi_Free(handles);
        } else if (r != TSS2_FAPI_RC_NO_HANDLE) {
            LOG_ERROR("GetPollHandles failed");
            goto error;
        }

        r = Fapi_GetRandom_Finish(context, &randomBytes);
    } while (r == TSS2_FAPI_RC_TRY_AGAIN);
    goto_if_error(r, "Error Fapi_GetRandom_Finish", error);
    ASSERT(randomBytes != NULL);

    Fapi_Free(randomBytes);

    randomBytes = NULL;
    r = Fapi_GetRandom(context, bytesRequested, &randomBytes);
    goto_if_error(r, "Error Fapi_GetRandom", error);
    ASSERT(randomBytes != NULL);

    Fapi_Free(randomBytes);

    /* Cleanup */
    r = Fapi_Delete(context, "/");
    goto_if_error(r, "Error Fapi_Delete", error);

    return TSS2_RC_SUCCESS;

error:
    Fapi_Delete(context, "/");
    return EXIT_FAILURE;
}

int
test_invoke_fapi(FAPI_CONTEXT *fapi_context)
{
    return test_fapi_get_random(fapi_context);
}
