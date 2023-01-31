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
#include "tss2_esys.h"

#include "test-fapi.h"
#include "fapi_util.h"
#include "fapi_int.h"
#include "tss2_esys.h"

#include "esys_iutil.h"
#define LOGMODULE test
#include "util/log.h"
#include "util/aux_util.h"
#include "tss2_mu.h"
#include "fapi_int.h"


/** Test the FAPI cleanup in an error case.
 *
 * Tested FAPI commands:
 *  - Fapi_Provision()
 *
 * @param[in,out] context The FAPI_CONTEXT.
 * @retval EXIT_FAILURE
 * @retval EXIT_SUCCESS
 */
int
test_fapi_test_provisioning_error(FAPI_CONTEXT *context)
{
    TSS2_RC r;

    r = Fapi_Provision(context, NULL, NULL, NULL);

    if ((r & ~TPM2_RC_N_MASK) == (TPM2_RC_NV_DEFINED & ~TPM2_RC_N_MASK))
        return EXIT_SUCCESS;
    goto_if_error(r, "Error Fapi_Provision", error);

    return EXIT_FAILURE;

error:
    Fapi_Delete(context, "/");
    return EXIT_FAILURE;
}

int
test_invoke_fapi(FAPI_CONTEXT *fapi_context)
{
    return test_fapi_test_provisioning_error(fapi_context);
}
