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

/** This test is intended to test the ESYS command  Esys_HASH.
 *
 * The test checks whether the TPM hash function can be used via the ESYS.
 *
 * Tested ESYS commands:
 *  - Esys_Hash() (M)
 *
 * @param[in,out] esys_context The ESYS_CONTEXT.
 * @param[in] hierarchy the hierarchy to perform the hash in.
 * @retval EXIT_FAILURE
 * @retval EXIT_SUCCESS
 */

int
test_esys_hash(ESYS_CONTEXT * esys_context, ESYS_TR hierarchy)
{
    TSS2_RC r;
    TPM2B_MAX_BUFFER data = { .size = 20,
                              .buffer={0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0,
                                       1, 2, 3, 4, 5, 6, 7, 8, 9}};
    TPMI_ALG_HASH hashAlg = TPM2_ALG_SHA256;
    TPM2B_DIGEST *outHash = NULL;
    TPMT_TK_HASHCHECK *validation = NULL;

    r = Esys_Hash(
        esys_context,
        ESYS_TR_NONE,
        ESYS_TR_NONE,
        ESYS_TR_NONE,
        &data,
        hashAlg,
        hierarchy,
        &outHash,
        &validation);
    goto_if_error(r, "Error: Hash", error);

    Esys_Free(outHash);
    Esys_Free(validation);
    return EXIT_SUCCESS;

 error:
    Esys_Free(outHash);
    Esys_Free(validation);
    return EXIT_FAILURE;
}

int
test_invoke_esys(ESYS_CONTEXT * esys_context) {
    int rc = test_esys_hash(esys_context, ESYS_TR_RH_OWNER);
    if (rc)
        return rc;

    /*
     * Test that backwards compat API change is still working, see:
     *   - https://github.com/tpm2-software/tpm2-tss/issues/1750
     */
    return test_esys_hash(esys_context, TPM2_RH_OWNER);
}
