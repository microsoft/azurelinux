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

/** Test the ESYS function Esys_ChangeEPS.
 *
 *\b Note: platform authorization needed.
 *
 * Tested ESYS commands:
 *  - Esys_ChangeEPS() (O)
 *
 * @param[in,out] esys_context The ESYS_CONTEXT.
 * @retval EXIT_FAILURE
 * @retval EXIT_SKIP
 * @retval EXIT_SUCCESS
 */
int
test_esys_change_eps(ESYS_CONTEXT * esys_context)
{
    TSS2_RC r;

    ESYS_TR authHandle = ESYS_TR_RH_PLATFORM;

    r = Esys_ChangeEPS(
        esys_context,
        authHandle,
        ESYS_TR_PASSWORD,
        ESYS_TR_NONE,
        ESYS_TR_NONE);

    if ((r == TPM2_RC_COMMAND_CODE) ||
        (r == (TPM2_RC_COMMAND_CODE | TSS2_RESMGR_RC_LAYER)) ||
        (r == (TPM2_RC_COMMAND_CODE | TSS2_RESMGR_TPM_RC_LAYER))) {
        LOG_WARNING("Command TPM2_ChangeEPS not supported by TPM.");
        return  EXIT_SKIP;
        goto error;
    }

    if (number_rc(r) == TPM2_RC_BAD_AUTH) {
        /* Platform authorization not possible test will be skipped */
        LOG_WARNING("Platform authorization not possible.");
        return EXIT_SKIP;
    }

    goto_if_error(r, "Error: ChangeEPS", error);

    return EXIT_SUCCESS;

 error:
    return EXIT_FAILURE;
}

int
test_invoke_esys(ESYS_CONTEXT * esys_context) {
    return test_esys_change_eps(esys_context);
}
