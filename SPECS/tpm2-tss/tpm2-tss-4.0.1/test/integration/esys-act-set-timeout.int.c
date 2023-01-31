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
#define LOGMODULE test
#include "util/log.h"
#include "util/aux_util.h"

/** Test of the ESAPI function Esys_ACT_SetTimeout.
 *
 * Tested ESAPI commands:
 *  - Esys_ACT_SetTimeout() (M)
 *  - Esys_StartAuthSession()
 *  - Esys_FlushContext()
 *
 * Used compiler defines: TEST_SESSION
 *
 * @param[in,out] esys_context The ESYS_CONTEXT.
 * @retval EXIT_FAILURE
 * @retval EXIT_SUCCESS
 */
int
test_esys_act_set_timeout(ESYS_CONTEXT * esys_context)
{
    TSS2_RC r;
    ESYS_TR session = ESYS_TR_NONE;
    TPMT_SYM_DEF symmetric = {.algorithm = TPM2_ALG_AES,
                              .keyBits = {.aes = 128},
                              .mode = {.aes = TPM2_ALG_CFB}
    };
    TPMA_SESSION sessionAttributes = TPMA_SESSION_CONTINUESESSION |
                                     TPMA_SESSION_AUDIT;
    TPM2B_NONCE nonceCaller = {
        .size = 20,
        .buffer = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                   11, 12, 13, 14, 15, 16, 17, 18, 19, 20}
	};

    r = Esys_StartAuthSession(esys_context, ESYS_TR_NONE, ESYS_TR_NONE,
                              ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE,
                              &nonceCaller,
                              TPM2_SE_HMAC, &symmetric, TPM2_ALG_SHA256,
                              &session);
    goto_if_error(r, "Error: During initialization of session", error);

    r = Esys_TRSess_SetAttributes(esys_context, session, sessionAttributes, 0xFF);
    goto_if_error(r, "Error: TRSess_SetAttributes", error);

	ESYS_TR ACT_handle = ESYS_TR_RH_ACT(0); /* pick first Auth timer */

    r = Esys_ACT_SetTimeout(esys_context, ACT_handle,
                            session, ESYS_TR_NONE, ESYS_TR_NONE, 32);
    goto_if_error(r, "Error: Clear", error);

	r = Esys_FlushContext(esys_context, session);
    goto_if_error(r, "Error: FlushContext", error);
    return EXIT_SUCCESS;

 error:
    if (session != ESYS_TR_NONE) {
        if (Esys_FlushContext(esys_context, session) != TSS2_RC_SUCCESS) {
            LOG_ERROR("Cleanup session failed.");
        }
    }
    /* If the TPM doesn't support it return skip */
    if (r == TPM2_RC_COMMAND_CODE)
        return EXIT_SKIP;
    else
        return EXIT_FAILURE;
}

int
test_invoke_esys(ESYS_CONTEXT * esys_context) {
    return test_esys_act_set_timeout(esys_context);
}
