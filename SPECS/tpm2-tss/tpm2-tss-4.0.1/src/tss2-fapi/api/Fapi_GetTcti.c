/* SPDX-License-Identifier: BSD-2-Clause */
/*******************************************************************************
 * Copyright 2018-2019, Fraunhofer SIT sponsored by Infineon Technologies AG
 * All rights reserved.
 ******************************************************************************/

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include "tss2_fapi.h"
#include "tss2_esys.h"
#include "tss2_tcti.h"

#include "fapi_int.h"
#define LOGMODULE fapi
#include "util/log.h"
#include "util/aux_util.h"

/** One-Call function for Fapi_GetTcti
 *
 * Fapi_GetTcti returns the TSS2_TCTI_CONTEXT currently used by the provided FAPI_CONTEXT.
 * The purpose is to enable advanced access to the TPM that is currently being talked to.
 * It is especially useful in combination with Fapi_GetTpmBlobs().
 *
 * Note: The application must ensure that this TSS2_TCTI_CONTEXT is not being used in parallel to
 *       the processing of a FAPI command.
 *
 * @param[in,out] context The FAPI_CONTEXT
 * @param[out] tcti The TSS2_TCTI_CONTEXT used to talk to the current TPM.
 *
 * @retval TSS2_RC_SUCCESS: if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE: if context, tcti is NULL.
 * @retval TSS2_FAPI_RC_BAD_CONTEXT: if context corruption is detected.
 * @retval TSS2_FAPI_RC_NO_TPM: if FAPI was started in non-TPM mode.
 */
TSS2_RC
Fapi_GetTcti(
    FAPI_CONTEXT       *context,
    TSS2_TCTI_CONTEXT **tcti)
{
    LOG_TRACE("called for context:%p", context);

    TSS2_RC r;

    /* Check for NULL parameters */
    check_not_null(context);
    check_not_null(tcti);

    /* Check if FAPI was started in a non-TPM mode. */
    if (!context->esys)
        return_error(TSS2_FAPI_RC_NO_TPM, "Fapi is running in non-TPM mode");

    /* Retrieve the TCTI from ESYS. */
    r = Esys_GetTcti(context->esys, tcti);
    return_if_error(r, "Esys_GetTcti");

    LOG_DEBUG("finished");
    return r;
}
