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

/** This tests the Esys_TR_ToTPMPublic function by
 *  creating a Primary Object Key and then attempting to retrieve
 *  the TPM2_HANDLE for it and validating that the handle is correct for the
 *  expected object type.
 *
 * Tested ESYS commands:
 *  - Esys_CreatePrimary() (M)
 *  - Esys_EvictControl() (M)
 *  - Esys_FlushContext() (M)
 *  - Esys_TR_ToTPMPublic() (M)
 *
 * @param[in,out] ectx The ESYS_CONTEXT.
 * @retval EXIT_FAILURE
 * @retval EXIT_SUCCESS
 */

int
test_esys_tr_toTpmPublic_key(ESYS_CONTEXT * ectx)
{
    int rc = EXIT_FAILURE;

    TSS2_RC r;
    ESYS_TR primaryHandle = ESYS_TR_NONE;
    ESYS_TR keyHandle = ESYS_TR_NONE;

    TPM2B_AUTH authValuePrimary = {
        .size = 5,
        .buffer = {1, 2, 3, 4, 5}
    };

    TPM2B_SENSITIVE_CREATE inSensitivePrimary = {
        .size = 0,
        .sensitive = {
            .userAuth = {
                 .size = 0,
                 .buffer = {0 },
             },
            .data = {
                 .size = 0,
                 .buffer = {0},
             },
        },
    };

    inSensitivePrimary.sensitive.userAuth = authValuePrimary;

    TPM2B_PUBLIC inPublic = {
        .size = 0,
        .publicArea = {
            .type = TPM2_ALG_RSA,
            .nameAlg = TPM2_ALG_SHA256,
            .objectAttributes = (TPMA_OBJECT_USERWITHAUTH |
                                 TPMA_OBJECT_RESTRICTED |
                                 TPMA_OBJECT_DECRYPT |
                                 TPMA_OBJECT_FIXEDTPM |
                                 TPMA_OBJECT_FIXEDPARENT |
                                 TPMA_OBJECT_SENSITIVEDATAORIGIN),
            .authPolicy = {
                 .size = 0,
             },
            .parameters.rsaDetail = {
                 .symmetric = {
                     .algorithm = TPM2_ALG_AES,
                     .keyBits.aes = 128,
                     .mode.aes = TPM2_ALG_CFB},
                 .scheme = {
                      .scheme = TPM2_ALG_NULL
                  },
                 .keyBits = 2048,
                 .exponent = 0,
             },
            .unique.rsa = {
                 .size = 0,
                 .buffer = {},
             },
        },
    };
    LOG_INFO("\nRSA key will be created.");

    TPM2B_DATA outsideInfo = {
        .size = 0,
        .buffer = {},
    };

    TPML_PCR_SELECTION creationPCR = {
        .count = 0,
    };

    /* create a key */
    r = Esys_CreatePrimary(ectx, ESYS_TR_RH_OWNER,
                           ESYS_TR_PASSWORD, ESYS_TR_NONE, ESYS_TR_NONE,
                           &inSensitivePrimary, &inPublic, &outsideInfo,
                           &creationPCR,
                           &primaryHandle, NULL, NULL, NULL, NULL);
    goto_if_error(r, "Create primary", out);

    /* the handle should be transient */
    TPM2_HANDLE tpmHandle = ESYS_TR_NONE;
    r = Esys_TR_GetTpmHandle(ectx, primaryHandle, &tpmHandle);
    goto_if_error(r, "Esys_TR_ToTPMPublic", error);

    if (!(tpmHandle & TPM2_HR_TRANSIENT)) {
        LOG_ERROR("Retrieved handle should be transient, got: 0x%x", tpmHandle);
        goto error;
    }

    /* make it persistent */
    r = Esys_EvictControl(ectx, ESYS_TR_RH_OWNER, primaryHandle,
                          ESYS_TR_PASSWORD, ESYS_TR_NONE, ESYS_TR_NONE,
                          TPM2_PERSISTENT_FIRST, &keyHandle);
    goto_if_error(r, "EvictControl make persistent", error);

    /* handle should be persistent */
    r = Esys_TR_GetTpmHandle(ectx, keyHandle, &tpmHandle);
    goto_if_error(r, "Esys_TR_ToTPMPublic", error);

    if (!(tpmHandle & TPM2_HR_PERSISTENT)) {
        LOG_ERROR("Retrieved handle should be transient, got: 0x%x", tpmHandle);
        goto error;
    }

    rc = EXIT_SUCCESS;

error:
    r = Esys_FlushContext(ectx, primaryHandle);
    if (r != TSS2_RC_SUCCESS) {
        rc = EXIT_FAILURE;
        LOG_ERROR("TR close on key object");
    }

    r = Esys_EvictControl(ectx, ESYS_TR_RH_OWNER, keyHandle,
                          ESYS_TR_PASSWORD, ESYS_TR_NONE, ESYS_TR_NONE,
                          TPM2_PERSISTENT_FIRST, &keyHandle);
    if (r != TSS2_RC_SUCCESS) {
        rc = EXIT_FAILURE;
        LOG_ERROR("Esys_EvictControl");
    }

out:
    return rc;
}

int
test_invoke_esys(ESYS_CONTEXT * esys_context) {
    return test_esys_tr_toTpmPublic_key(esys_context);
}
