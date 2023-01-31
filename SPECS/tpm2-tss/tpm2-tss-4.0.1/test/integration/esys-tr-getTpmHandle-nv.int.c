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
#define LOGMODULE test
#include "util/log.h"
#include "util/aux_util.h"

/** This tests the Esys_TR_ToTPMPublic function by
 *  creating an NV index object and then attempting to retrieve
 *  the TPM2_HANDLE for it and validating that the handle is correct for the
 *  expected object type.
 *
 * Tested ESYS commands:
 *  - Esys_NV_DefineSpace() (M)
 *  - Esys_NV_UndefineSpace() (M)
 *  - Esys_TR_ToTPMPublic() (M)
 *
 * @param[in,out] ectx The ESYS_CONTEXT.
 * @retval EXIT_FAILURE
 * @retval EXIT_SUCCESS
 */

int
test_esys_tr_toTpmPublic_nv(ESYS_CONTEXT * ectx)
{
    int rc = EXIT_FAILURE;

    TSS2_RC r;
    ESYS_TR nvHandle = ESYS_TR_NONE;

    TPM2B_AUTH auth = {.size = 20,
                       .buffer={10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
                                20, 21, 22, 23, 24, 25, 26, 27, 28, 29}};

    TPM2B_NV_PUBLIC publicInfo = {
        .size = 0,
        .nvPublic = {
            .nvIndex =TPM2_NV_INDEX_FIRST,
            .nameAlg = TPM2_ALG_SHA256,
            .attributes = TPMA_NV_AUTHWRITE | TPMA_NV_AUTHREAD,
            .authPolicy = {
                 .size = 0,
                 .buffer = {},
             },
            .dataSize = 1,
        }
    };

    r = Esys_NV_DefineSpace(ectx, ESYS_TR_RH_OWNER,
                            ESYS_TR_PASSWORD, ESYS_TR_NONE, ESYS_TR_NONE,
                            &auth, &publicInfo, &nvHandle);
    goto_if_error(r, "NV define space", out);

    /* the handle should be NV */
    TPM2_HANDLE tpmHandle = ESYS_TR_NONE;
    r = Esys_TR_GetTpmHandle(ectx, nvHandle, &tpmHandle);
    goto_if_error(r, "Esys_TR_ToTPMPublic", error);

    if (!(tpmHandle & TPM2_HR_NV_INDEX)) {
        LOG_ERROR("Retrieved handle should be NV, got: 0x%x", tpmHandle);
        goto error;
    }

    rc = EXIT_SUCCESS;

error:
    r = Esys_NV_UndefineSpace(ectx, ESYS_TR_RH_OWNER, nvHandle,
                              ESYS_TR_PASSWORD, ESYS_TR_NONE, ESYS_TR_NONE);
    if (r != TSS2_RC_SUCCESS) {
        LOG_ERROR("NV UndefineSpace");
        rc = EXIT_FAILURE;
    }
out:
    return rc;
}

int
test_invoke_esys(ESYS_CONTEXT * esys_context) {
    return test_esys_tr_toTpmPublic_nv(esys_context);
}
