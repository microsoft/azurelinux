/* SPDX-License-Identifier: BSD-2-Clause */
/*******************************************************************************
 * Copyright (c) 2020, Intel Corporation
 * All rights reserved.
 *******************************************************************************/

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <stdlib.h>

#include "tss2_esys.h"

#include "esys_iutil.h"
#include "test-esys.h"
#define LOGDEFAULT LOGLEVEL_INFO
#define LOGMODULE test
#include "util/log.h"
#include "util/aux_util.h"

/** Test auth verification in clear command
 *
 * After TPM2_Clear command is executed all auth values for
 * owner, platofrm and lockout are set to empty buffers and
 * the empty auth values should be used fot HMAC verification
 * in the response.
 *
 * @param[in,out] esys_context The ESYS_CONTEXT.
 * @retval EXIT_SUCCESS
 * @retval EXIT_SKIP
 * @retval EXIT_FAILURE
 */
int
test_esys_clear_auth(ESYS_CONTEXT * esys_context)
{
    TSS2_RC r;
    ESYS_TR session = ESYS_TR_NONE;
    int failure_return = EXIT_FAILURE;

    TPMT_SYM_DEF symmetric = {.algorithm = TPM2_ALG_XOR,
                              .keyBits = { .exclusiveOr = TPM2_ALG_SHA256 },
                              .mode = {.aes = TPM2_ALG_CFB}};

    /* Test lockout authorization */
    LOG_DEBUG("Test LOCKOUT authorization");
    LOG_DEBUG("Start Auth Session");
    r = Esys_StartAuthSession(esys_context, ESYS_TR_NONE, ESYS_TR_NONE,
                              ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE,
                              NULL,
                              TPM2_SE_HMAC, &symmetric, TPM2_ALG_SHA256,
                              &session);
    goto_if_error(r, "Error: During initialization of session", error);

    TPM2B_AUTH auth = {
            .size = 16,
            .buffer = "deadbeefdeadbeef",
    };

    LOG_DEBUG("Set Auth");
    r = Esys_HierarchyChangeAuth(esys_context, ESYS_TR_RH_LOCKOUT,
                                 ESYS_TR_PASSWORD, ESYS_TR_NONE, ESYS_TR_NONE,
                                 &auth);

    goto_if_error(r, "Error: During Esys_ObjectChangeAuth", error);
    Esys_TR_SetAuth(esys_context, ESYS_TR_RH_LOCKOUT, &auth);

    LOG_DEBUG("Clear");
    r = Esys_Clear(esys_context, ESYS_TR_RH_LOCKOUT, session,
                   ESYS_TR_NONE, ESYS_TR_NONE);
    goto_if_error(r, "Error: During Esys_Clear", error);

    r = Esys_FlushContext(esys_context, session);
    goto_if_error(r, "Error: During Esys_FlushContext", error);

    /* Test platform authorization */
    LOG_DEBUG("Test PLATFORM authorization");
    LOG_DEBUG("Start Auth Session");
    r = Esys_StartAuthSession(esys_context, ESYS_TR_NONE, ESYS_TR_NONE,
                              ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE,
                              NULL,
                              TPM2_SE_HMAC, &symmetric, TPM2_ALG_SHA256,
                              &session);
    goto_if_error(r, "Error: During initialization of session", error);

    LOG_DEBUG("Set Auth");
    r = Esys_HierarchyChangeAuth(esys_context, ESYS_TR_RH_PLATFORM,
                                 ESYS_TR_PASSWORD, ESYS_TR_NONE, ESYS_TR_NONE,
                                 &auth);

    if (number_rc(r) == TPM2_RC_BAD_AUTH ||
        number_rc(r) == TPM2_RC_HIERARCHY) {
        /* Platform authorization not possible test will be skipped */
        LOG_WARNING("Platform authorization not possible.");
        failure_return = EXIT_SKIP;
        goto error;
    }
    goto_if_error(r, "Error: During Esys_ObjectChangeAuth", error);

    Esys_TR_SetAuth(esys_context, ESYS_TR_RH_PLATFORM, &auth);

    LOG_DEBUG("Clear");
    r = Esys_Clear(esys_context, ESYS_TR_RH_PLATFORM, session,
                   ESYS_TR_NONE, ESYS_TR_NONE);
    goto_if_error(r, "Error: During Esys_Clear", error);

    r = Esys_FlushContext(esys_context, session);
    goto_if_error(r, "Error: During Esys_FlushContext", error);

    Esys_TR_SetAuth(esys_context, ESYS_TR_RH_PLATFORM, &auth);

    LOG_DEBUG("Set Auth");
    r = Esys_HierarchyChangeAuth(esys_context, ESYS_TR_RH_PLATFORM,
                                 ESYS_TR_PASSWORD, ESYS_TR_NONE, ESYS_TR_NONE,
                                 NULL);

    goto_if_error(r, "Error: During Esys_ObjectChangeAuth", error);

    return EXIT_SUCCESS;

 error:
    LOG_ERROR("\nError Code: %x\n", r);

    if (session != ESYS_TR_NONE) {
        if (Esys_FlushContext(esys_context, session) != TSS2_RC_SUCCESS) {
            LOG_ERROR("Cleanup session failed.");
        }
    }
    return failure_return;
}

int
test_invoke_esys(ESYS_CONTEXT * esys_context) {
    return test_esys_clear_auth(esys_context);
}
