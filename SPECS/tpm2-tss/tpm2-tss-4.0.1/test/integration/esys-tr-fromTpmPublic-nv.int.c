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

/** This tests the Esys_TR_FromTPMPublic and Esys_TR_GetName functions by
 *  creating an NV Index and then attempting to retrieve an ESYS_TR object for
 *  it.
 *  Then we call Esys_TR_GetName to see if the correct public name has been
 * retrieved.
 *
 * Tested ESYS commands:
 *  - Esys_NV_DefineSpace() (M)
 *  - Esys_NV_ReadPublic() (M)
 *  - Esys_NV_UndefineSpace() (M)
 *  - Esys_TR_FromTPMPublic() (M)
 *
 * @param[in,out] ectx The ESYS_CONTEXT.
 * @retval EXIT_FAILURE
 * @retval EXIT_SUCCESS
 */

int
test_esys_tr_fromTpmPublic_nv(ESYS_CONTEXT * ectx)
{
    TSS2_RC r;
    ESYS_TR nvHandle = ESYS_TR_NONE;

    TPM2B_NAME *name1, *name2;
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

    ESYS_TR session = ESYS_TR_NONE;
    ESYS_TR session2 = ESYS_TR_NONE;
    TPMT_SYM_DEF symmetric = {.algorithm = TPM2_ALG_AES,
        .keyBits = {.aes = 128},
        .mode = {.aes = TPM2_ALG_CFB}
    };

    r = Esys_NV_DefineSpace(ectx, ESYS_TR_RH_OWNER,
                            ESYS_TR_PASSWORD, ESYS_TR_NONE, ESYS_TR_NONE,
                            &auth, &publicInfo, &nvHandle);
    goto_if_error(r, "NV define space", error);

    r = Esys_NV_ReadPublic(ectx, nvHandle,
                           ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE,
                           NULL, &name1);
    goto_if_error(r, "NV read public", error);

    r = Esys_TR_Close(ectx, &nvHandle);
    goto_if_error(r, "TR close on nv object", error_name1);

    /* Reading public data for a TPM handle  without session */
    r = Esys_TR_FromTPMPublic(ectx, TPM2_NV_INDEX_FIRST,
                              ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE,
                              &nvHandle);
    goto_if_error(r, "TR from TPM public", error_name1);

    /* Reading public data for a TPM handle  without session for an existing
       esys object. */
    r = Esys_TR_FromTPMPublic(ectx, TPM2_NV_INDEX_FIRST,
                              ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE,
                              &nvHandle);
    goto_if_error(r, "TR from TPM public", error_name1);

    r = Esys_TR_Close(ectx, &nvHandle);
    goto_if_error(r, "TR close on nv object", error_name1);

    /* Reading public data for a TPM handle with a HMAC session. */
    r = Esys_StartAuthSession(ectx, ESYS_TR_NONE, ESYS_TR_NONE,
                              ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE,
                              NULL,
                              TPM2_SE_HMAC, &symmetric, TPM2_ALG_SHA1,
                              &session);

    goto_if_error(r, "Error: During initialization of session", error);

    r = Esys_TRSess_SetAttributes(ectx, session, TPMA_SESSION_ENCRYPT,
                                  TPMA_SESSION_CONTINUESESSION | TPMA_SESSION_ENCRYPT);
    goto_if_error(r, "TR_Sess_SetAttributes", error);

    r = Esys_StartAuthSession(ectx, ESYS_TR_NONE, ESYS_TR_NONE,
                              ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE,
                              NULL,
                              TPM2_SE_HMAC, &symmetric, TPM2_ALG_SHA1,
                              &session2);
    goto_if_error(r, "Error: During initialization of session", error);

    /* Create also a second session for reading the public data. */

    r = Esys_TRSess_SetAttributes(ectx, session2, TPMA_SESSION_AUDIT,
                                  TPMA_SESSION_CONTINUESESSION | TPMA_SESSION_AUDIT);

    goto_if_error(r, "TR_Sess_SetAttributes", error);

    r = Esys_TR_FromTPMPublic(ectx, TPM2_NV_INDEX_FIRST,
                              session, session2, ESYS_TR_NONE,
                              &nvHandle);
    goto_if_error(r, "TR from TPM public", error_name1);

    /* Reading public data for a TPM handle with a HMAC session for an existing
       esys object.  */
    r = Esys_StartAuthSession(ectx, ESYS_TR_NONE, ESYS_TR_NONE,
                              ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE,
                              NULL,
                              TPM2_SE_HMAC, &symmetric, TPM2_ALG_SHA1,
                              &session);

    goto_if_error(r, "Error: During initialization of session", error);

    r = Esys_TRSess_SetAttributes(ectx, session, TPMA_SESSION_ENCRYPT,
                                  TPMA_SESSION_CONTINUESESSION | TPMA_SESSION_ENCRYPT);
    goto_if_error(r, "TR_Sess_SetAttributes", error);

    r = Esys_TR_FromTPMPublic(ectx, TPM2_NV_INDEX_FIRST,
                              session, ESYS_TR_NONE, ESYS_TR_NONE,
                              &nvHandle);
    goto_if_error(r, "TR from TPM public", error_name1);

    r = Esys_TR_GetName(ectx, nvHandle, &name2);
    goto_if_error(r, "TR get name", error_name1);

    r = Esys_NV_UndefineSpace(ectx, ESYS_TR_RH_OWNER, nvHandle,
                              ESYS_TR_PASSWORD, ESYS_TR_NONE, ESYS_TR_NONE);
    goto_if_error(r, "NV UndefineSpace", error_name2);

    if (name1->size != name2->size ||
        memcmp(&name1->name[0], &name2->name[0], name1->size) != 0)
    {
        LOG_ERROR("Names mismatch between NV_GetPublic and TR_GetName");
        goto error_name2;
    }

    free(name1);
    free(name2);

    return EXIT_SUCCESS;

error_name2:
    free(name2);
error_name1:
    free(name1);
error:

    if (nvHandle != ESYS_TR_NONE) {
        if (Esys_NV_UndefineSpace(ectx,
                                  ESYS_TR_RH_OWNER,
                                  nvHandle,
                                  ESYS_TR_PASSWORD,
                                  ESYS_TR_NONE,
                                  ESYS_TR_NONE) != TSS2_RC_SUCCESS) {
             LOG_ERROR("Cleanup nvHandle failed.");
        }
    }


    return EXIT_FAILURE;
}

int
test_invoke_esys(ESYS_CONTEXT * esys_context) {
    return test_esys_tr_fromTpmPublic_nv(esys_context);
}
