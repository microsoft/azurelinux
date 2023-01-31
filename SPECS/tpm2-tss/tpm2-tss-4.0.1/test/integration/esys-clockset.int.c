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

/** Test the ESYS function Esys_ClockSet and Esys_ReadClock.
 *
 *\b Note: platform authorization needed.
 *
 * Tested ESYS commands:
 *  - Esys_ClockRateAdjust() (M)
 *  - Esys_ClockSet() (M)
 *  - Esys_ReadClock() (M)
 *
 * Used compiler defines: TEST_SESSION
 *
 * @param[in,out] esys_context The ESYS_CONTEXT.
 * @retval EXIT_FAILURE
 * @retval EXIT_SKIP
 * @retval EXIT_SUCCESS
 */
int
test_esys_clockset(ESYS_CONTEXT * esys_context)
{

    TSS2_RC r;
    int failure_return = EXIT_FAILURE;

    ESYS_TR auth_handle = ESYS_TR_RH_OWNER;
    TPMS_TIME_INFO *currentTime = NULL;

#ifdef TEST_SESSION
    ESYS_TR session = ESYS_TR_NONE;
    TPMT_SYM_DEF symmetric = { .algorithm = TPM2_ALG_NULL };
    TPM2B_NONCE nonceCaller = {
        .size = 20,
        .buffer = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                   11, 12, 13, 14, 15, 16, 17, 18, 19, 20}
    };

    /* Audit session */
    r = Esys_StartAuthSession(esys_context, ESYS_TR_NONE, ESYS_TR_NONE,
                              ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE,
                              &nonceCaller,
                              TPM2_SE_HMAC, &symmetric, TPM2_ALG_SHA256,
                              &session);
    goto_if_error(r, "Error: During initialization of session", error);

    TPMA_SESSION sessionAttributes = TPMA_SESSION_AUDIT |
                                     TPMA_SESSION_CONTINUESESSION;

    r = Esys_TRSess_SetAttributes(esys_context, session, sessionAttributes, 0xFF);
    goto_if_error(r, "Error: During SetAttributes", error);

    r = Esys_ReadClock(esys_context,
                       session,
                       ESYS_TR_NONE,
                       ESYS_TR_NONE,
                       &currentTime);

    /* TPMs before Revision 1.38 might not support session usage*/
    if ((r == TPM2_RC_AUTH_CONTEXT ) ||
        (r == (TPM2_RC_AUTH_CONTEXT  | TSS2_RESMGR_RC_LAYER)) ||
        (r == (TPM2_RC_AUTH_CONTEXT  | TSS2_RESMGR_TPM_RC_LAYER))) {
        LOG_WARNING("Session usage not supported by TPM.");
        failure_return = EXIT_SKIP;
        goto error;
    }

#else
    r = Esys_ReadClock(esys_context,
                       ESYS_TR_NONE,
                       ESYS_TR_NONE,
                       ESYS_TR_NONE,
                       &currentTime);
#endif
    goto_if_error(r, "Error: ReadClock", error);

    UINT64 newTime = currentTime->clockInfo.clock + 010000;

    r = Esys_ClockSet(esys_context,
                      auth_handle,
                      ESYS_TR_PASSWORD,
                      ESYS_TR_NONE,
                      ESYS_TR_NONE,
                      newTime);

    if (number_rc(r) == TPM2_RC_BAD_AUTH) {
        /* Platform authorization not possible test will be skipped */
        LOG_WARNING("Platform authorization not possible.");
        failure_return = EXIT_SKIP;
        goto error;
    }

    goto_if_error(r, "Error: ClockSet", error);

    r = Esys_ClockRateAdjust(esys_context,
                             auth_handle,
                             ESYS_TR_PASSWORD,
                             ESYS_TR_NONE,
                             ESYS_TR_NONE,
                             TPM2_CLOCK_MEDIUM_FASTER);
    goto_if_error(r, "Error: ClockRateAdjust", error);

    r = Esys_ClockRateAdjust(esys_context,
                             auth_handle,
                             ESYS_TR_PASSWORD,
                             ESYS_TR_NONE,
                             ESYS_TR_NONE,
                             TPM2_CLOCK_MEDIUM_SLOWER);
    goto_if_error(r, "Error: ClockRateAdjust", error);
    Esys_Free(currentTime);
#ifdef TEST_SESSION
    if (session != ESYS_TR_NONE) {
        if (Esys_FlushContext(esys_context, session) != TSS2_RC_SUCCESS) {
            LOG_ERROR("Cleanup session_enc failed.");
        }
    }
#endif
    return EXIT_SUCCESS;

 error:
    Esys_Free(currentTime);
#ifdef TEST_SESSION
    if (session != ESYS_TR_NONE) {
        if (Esys_FlushContext(esys_context, session) != TSS2_RC_SUCCESS) {
            LOG_ERROR("Cleanup session_enc failed.");
        }
    }
#endif
    return failure_return;
}

int
test_invoke_esys(ESYS_CONTEXT * esys_context) {
    return test_esys_clockset(esys_context);
}
