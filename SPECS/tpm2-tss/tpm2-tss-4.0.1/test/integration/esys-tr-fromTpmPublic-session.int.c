/* SPDX-License-Identifier: BSD-2-Clause */
#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <stdlib.h>

#include "tss2_esys.h"

#include "esys_iutil.h"
#define LOGMODULE test
#include "util/log.h"
#include "util/aux_util.h"

/** This tests the ability to create an ESYS_TR object via Esys_TR_FromTPMPublic
 *  given a TPM2_HANDLE representing a session handle.
 *
 * Tested ESYS commands:
 *  - Esys_StartAuthSession() (M)
 *  - Esys_GetCapability() (M)
 *  - Esys_FlushContext() (M)
 *
 * @param[in,out] ectx The ESYS_CONTEXT.
 * @retval EXIT_FAILURE
 * @retval EXIT_SUCCESS
 */

int
test_esys_tr_fromTpmPublic_session(ESYS_CONTEXT * ectx)
{
    int rc = EXIT_FAILURE;

    ESYS_TR session = ESYS_TR_NONE;
    TPMT_SYM_DEF symmetric = {
        .algorithm = TPM2_ALG_XOR,
        .keyBits = { .exclusiveOr = TPM2_ALG_SHA256 }
    };

    TPMS_CAPABILITY_DATA *cap_data = NULL;

    TSS2_RC r = Esys_StartAuthSession(ectx, ESYS_TR_NONE, ESYS_TR_NONE,
                              ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE,
                              NULL,
                              TPM2_SE_HMAC, &symmetric, TPM2_ALG_SHA256,
                              &session);
    goto_if_error(r, "Error: During initialization of session", out);

    TPMI_YES_NO more_data;
    r = Esys_GetCapability(ectx, ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE,
                                 TPM2_CAP_HANDLES,
                                 TPM2_LOADED_SESSION_FIRST,
                                 TPM2_MAX_CAP_HANDLES,
                                 &more_data,
                                 &cap_data);
    goto_if_error(r, "Error: getting capability for loaded sessions", out);

    if (cap_data->data.handles.count != 1) {
        LOG_ERROR("Expected 1 loaded session handle, got: %"PRIu32,
                  cap_data->data.handles.count);
        goto out;
    }

    TPM2_HANDLE tpm2_handle = cap_data->data.handles.handle[0];

    ESYS_TR new_handle = ESYS_TR_NONE;
    r = Esys_TR_FromTPMPublic(
            ectx,
            tpm2_handle,
            ESYS_TR_NONE,
            ESYS_TR_NONE,
            ESYS_TR_NONE,
            &new_handle);
    goto_if_error(r, "Error: converting TPM2_HANDLE to ESYS_TR object", out);

    r = Esys_TRSess_SetAttributes(ectx, new_handle,
          TPMA_SESSION_DECRYPT|TPMA_SESSION_ENCRYPT,
          0xFF);
    if (r != TSS2_ESYS_RC_BAD_TR) {
        LOG_ERROR("Error: Expected GetCapability call to fail with "
                "TSS2_ESYS_RC_BAD_TR, got: "TPM2_ERROR_FORMAT,
                TPM2_ERROR_TEXT(r));
        goto out;
    }

    free(cap_data);
    cap_data = NULL;

    r = Esys_GetCapability(ectx, new_handle, ESYS_TR_NONE, ESYS_TR_NONE,
                           TPM2_CAP_HANDLES,
                           TPM2_LOADED_SESSION_FIRST,
                           TPM2_MAX_CAP_HANDLES,
                           &more_data,
                           &cap_data);
    if (r != TSS2_ESYS_RC_BAD_TR) {
        LOG_ERROR("Error: Expected GetCapability call to fail with "
                "TSS2_ESYS_RC_BAD_TR, got: "TPM2_ERROR_FORMAT,
                TPM2_ERROR_TEXT(r));
        goto out;
    }

    /* ensure you can flush the frompublic session handle */
    session = new_handle;

    rc = EXIT_SUCCESS;
out:
    free(cap_data);

    if (session != ESYS_TR_NONE) {
        r = Esys_FlushContext(ectx, session);
        if (r != TSS2_RC_SUCCESS) {
            LOG_ERROR("Error: FlushContext " TPM2_ERROR_FORMAT, TPM2_ERROR_TEXT(r));
            rc = EXIT_FAILURE;
        }
    }

    return rc;
}

int
test_invoke_esys(ESYS_CONTEXT * esys_context) {
    return test_esys_tr_fromTpmPublic_session(esys_context);
}
