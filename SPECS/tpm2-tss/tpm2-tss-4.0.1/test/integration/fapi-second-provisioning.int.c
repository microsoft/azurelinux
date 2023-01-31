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

/** Test the FAPI provisioning with passwords already set for endorsement and
 *  owner hierarchy.
 *
 * Tested FAPI commands:
 *  - Fapi_Provision()
 *  - Fapi_SetAuthCB()
 *  - Fapi_ChangeAuth()
 *  - Fapi_Delete()
 *
 * @param[in,out] context The FAPI_CONTEXT.
 * @retval EXIT_FAILURE
 * @retval EXIT_SUCCESS
 */
int
test_fapi_test_second_provisioning(FAPI_CONTEXT *context)
{
    TSS2_RC r;

    /* We need to reset the passwords again, in order to not brick physical TPMs */
    r = Fapi_Provision(context, PASSWORD, PASSWORD, NULL);
    goto_if_error(r, "Error Fapi_Provision", error);

    r = pcr_reset(context, 16);
    goto_if_error(r, "Error pcr_reset", error);

    r = Fapi_SetAuthCB(context, auth_callback, NULL);
    goto_if_error(r, "Error SetPolicyAuthCallback", error);

    goto_if_error(r, "Error Fapi_NV_Undefine", error);

    Fapi_Finalize(&context);

    int rc = init_fapi("P_RSA2", &context);
    if (rc)
        goto error;

    /* Authentication should not work due to auth for hierarchy was set. */
    r = Fapi_Provision(context, NULL, NULL, NULL);

    if (r == TSS2_RC_SUCCESS) {
        goto_if_error(r, "Wrong authentication.", error);
    }
    if (r != TSS2_FAPI_RC_AUTHORIZATION_UNKNOWN) {
        goto_if_error(r, "Wrong check auth value.", error);
    }

    /* Correct Provisioning with auth value for hierarchy from previous
       provisioning. The information whether a auth value is needed
       will be taken from hierarchy object of first provisioning. */
    r = Fapi_SetAuthCB(context, auth_callback, NULL);
    goto_if_error(r, "Error SetPolicyAuthCallback", error);

    r = Fapi_Provision(context, NULL, NULL, NULL);
    goto_if_error(r, "Error Fapi_Provision", error);

    r = Fapi_Delete(context, "/");
    goto_if_error(r, "Error Fapi_Delete", error);

    Fapi_Finalize(&context);
    rc = init_fapi("P_RSA2", &context);
    if (rc)
        goto error;

     /* Correct Provisioning with auth value for hierarchy from previous
       provisioning. Non information whether auth value is needed is
       available. */

    r = Fapi_SetAuthCB(context, auth_callback, NULL);
    goto_if_error(r, "Error SetPolicyAuthCallback", error);

    r = Fapi_Provision(context, NULL, NULL, NULL);
    goto_if_error(r, "Error Fapi_Provision", error);

    /* We need to reset the passwords again, in order to not brick physical TPMs */
    r = Fapi_ChangeAuth(context, "/HS", NULL);
    goto_if_error(r, "Error Fapi_ChangeAuth", error);

    r = Fapi_ChangeAuth(context, "/HE", NULL);
    goto_if_error(r, "Error Fapi_ChangeAuth", error);

    r = Fapi_Delete(context, "/");
    goto_if_error(r, "Error Fapi_Delete", error);

    Fapi_Finalize(&context);

    if (strcmp(FAPI_PROFILE, "P_ECC384") == 0) {
        rc = init_fapi("P_ECC_sh_eh_policy_sha384", &context);
    } else {
         rc = init_fapi("P_ECC_sh_eh_policy", &context);
    }

    if (rc)
        goto error;

    /* A policy will be assigned to owner and endorsement hierarchy. */

    r = Fapi_Provision(context, NULL, NULL, NULL);
    goto_if_error(r, "Error Fapi_Provision", error);

    Fapi_Finalize(&context);
    if (strcmp(FAPI_PROFILE, "P_ECC") == 0) {
        rc = init_fapi("P_ECC", &context);
    } else if (strcmp(FAPI_PROFILE, "P_ECC384") == 0) {
        rc = init_fapi("P_ECC384", &context);
    } else {
        LOG_ERROR("Profile %s not supported for this test!", FAPI_PROFILE);
    }

    if (rc)
        goto error;

    /* Owner and endorsement hierarchy will be authorized via policy and
       policy will be reset. */
    r = Fapi_Provision(context, NULL, NULL, NULL);

    goto_if_error(r, "Error Fapi_Provision", error);

    Fapi_Delete(context, "/");

    return EXIT_SUCCESS;

error:
    Fapi_Delete(context, "/");
    return EXIT_FAILURE;
}

int
test_invoke_fapi(FAPI_CONTEXT *fapi_context)
{
    return test_fapi_test_second_provisioning(fapi_context);
}
