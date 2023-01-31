/* SPDX-License-Identifier: BSD-2-Clause */
/*******************************************************************************
 * Copyright 2017-2018, Fraunhofer SIT sponsored by Infineon Technologies AG
 * All rights reserved.
 *******************************************************************************/

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <stdlib.h>

#include "tss2_esys.h"

#include "esys_iutil.h"
#include "test-esys.h"
#define LOGMODULE test
#include "util/log.h"
#include "util/aux_util.h"

/** Test the commands Esys_PCR_SetAuthValue and Esys_PCR_SetAuthPolicy.
 *
 *\b Note: platform authorization needed.
 *
 * Tested ESYS commands:
 *  - Esys_PCR_SetAuthPolicy() (O)
 *  - Esys_PCR_SetAuthValue() (O)
 *
 * @param[in,out] esys_context The ESYS_CONTEXT.
 * @retval EXIT_FAILURE
 * @retval EXIT_SKIP
 * @retval EXIT_SUCCESS
 */

int
test_esys_pcr_auth_value(ESYS_CONTEXT * esys_context)
{
    TSS2_RC r;
    int failure_return = EXIT_FAILURE;

    /*
     * PCR register 20 belongs to the policy group and the auth value group.
     * PCRs of these groups can be used for SetAuthValue and SetAuthPolicy.
     */
    ESYS_TR  pcrHandle_handle = 20;

    TPM2B_DIGEST auth = {
        .size = 20,
        .buffer = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                   11, 12, 13, 14, 15, 16, 17, 18, 19, 20}
    };

    r = Esys_PCR_SetAuthValue(
        esys_context,
        pcrHandle_handle,
        ESYS_TR_PASSWORD,
        ESYS_TR_NONE,
        ESYS_TR_NONE,
        &auth
        );


    if ((r == TPM2_RC_COMMAND_CODE) ||
        (r == (TPM2_RC_COMMAND_CODE | TSS2_RESMGR_RC_LAYER)) ||
        (r == (TPM2_RC_COMMAND_CODE | TSS2_RESMGR_TPM_RC_LAYER))) {
        LOG_WARNING("Command TPM2_PCR_SetAuthValue not supported by TPM.");
        failure_return = EXIT_SKIP;
        goto error;
    }

    goto_if_error(r, "Error: PCR_SetAuthValue", error);

    /* This should work as the authValue should be remembered, see
     *   - https://github.com/tpm2-software/tpm2-tss/issues/2099
     * for details.
     */
    r = Esys_PCR_SetAuthValue(
        esys_context,
        pcrHandle_handle,
        ESYS_TR_PASSWORD,
        ESYS_TR_NONE,
        ESYS_TR_NONE,
        &auth
        );
    goto_if_error(r, "Error: PCR_SetAuthValue2", error);

    TPM2B_DIGEST authPolicy = {
        .size = 32,
        .buffer = { 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,11, 12, 13, 14, 15, 16, 17,
                    18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32 }
    };

    r = Esys_PCR_SetAuthPolicy(
        esys_context,
        ESYS_TR_RH_PLATFORM,
        ESYS_TR_PASSWORD,
        ESYS_TR_NONE,
        ESYS_TR_NONE,
        &authPolicy,
        TPM2_ALG_SHA256,
        pcrHandle_handle);

    if (number_rc(r) == TPM2_RC_BAD_AUTH) {
        /* Platform authorization not possible test will be skipped */
        LOG_WARNING("Platform authorization not possible.");
        failure_return = EXIT_SKIP;
    }

    goto_if_error(r, "Error: PCR_SetAuthPolicy", error);

    return EXIT_SUCCESS;

 error:
    return failure_return;
}

int
test_invoke_esys(ESYS_CONTEXT * esys_context) {
    return test_esys_pcr_auth_value(esys_context);
}
