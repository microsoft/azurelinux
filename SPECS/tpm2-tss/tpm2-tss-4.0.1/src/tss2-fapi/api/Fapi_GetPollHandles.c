/* SPDX-License-Identifier: BSD-2-Clause */
/*******************************************************************************
 * Copyright 2018-2019, Fraunhofer SIT sponsored by Infineon Technologies AG
 * All rights reserved.
 ******************************************************************************/

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <stdlib.h>
#include <string.h>

#include "tss2_fapi.h"
#include "fapi_int.h"
#include "fapi_util.h"
#include "tss2_esys.h"
#define LOGMODULE fapi
#include "util/log.h"
#include "util/aux_util.h"

/** Retrieve handles for polling
 *
 * Returns an array of handles that can be polled on to get notified when
 * data from the TPM or from a disk operation is available.
 *
 * The corresponding code should look similar to follows:
 * do { r = Fapi_GetPollHandles(fc, &ph, &nph);
        if (r == TSS2_RC_SUCCESS) { poll(ph, nph, -1); Fapi_Free(ph); }
 *      r = Fapi_*_Finish(fc, ...); } while (r == TSS2_FAPI_RC_TRY_AGAIN);
 *
 * @param[in,out] context The FAPI_CONTEXT
 * @param[out] handles An array of poll handle entries
 * @param[out] num_handles The size of the array in handles
 *
 * @retval TSS2_RC_SUCCESS: if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE: if context or data is NULL.
 * @retval TSS2_FAPI_RC_BAD_CONTEXT: if context corruption is detected.
 * @retval TSS2_FAPI_RC_BAD_SEQUENCE: if the context has no asynchronous
 *         operation pending.
 * @retval TSS2_FAPI_RC_NO_HANDLE: if there are no handles to poll on
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory for
 *         internal operations or return parameters.
 */
TSS2_RC
Fapi_GetPollHandles(
    FAPI_CONTEXT *context,
    FAPI_POLL_HANDLE **handles,
    size_t            *num_handles)
{
    LOG_TRACE("called for context:%p", context);

    TSS2_RC r;

    /* Check for NULL parameters */
    check_not_null(context);
    check_not_null(handles);
    check_not_null(num_handles);

    /* Check the correct state for poll handle retrieval. */
    if (context->state == _FAPI_STATE_INIT) {
        LOG_ERROR("PollHandles can only be returned while an operation is running");
        return TSS2_FAPI_RC_BAD_SEQUENCE;
    }

    /* First we check for poll handles from IO operations. */
    r = ifapi_io_poll_handles(&context->io, handles, num_handles);
    if (r == TSS2_RC_SUCCESS) {
        LOG_DEBUG("Returning %zi IO poll handles.", *num_handles);
        return r;
    }
    if (r != TSS2_FAPI_RC_NO_HANDLE)
        return_if_error(r, "Retrieving poll handles failed");

    /* Then we check for poll handles from ESYS operations. */
    /* If we are running in none-TPM mode then we are already done trying. */
    return_if_null(context->esys, "No non-TPM based poll handles found.",
                   TSS2_FAPI_RC_NO_HANDLE);

    /* Retrieve the actual poll handles from ESYS. */
    r = Esys_GetPollHandles(context->esys, handles, num_handles);
    if (r) {
        LOG_DEBUG("Returning TSS2_FAPI_RC_NO_HANDLE");
        return TSS2_FAPI_RC_NO_HANDLE;
    }

    LOG_DEBUG("Returning %zi ESYS poll handles.", *num_handles);
    LOG_TRACE("finished");
    return r;
}
