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

/** Test the basic commands for PCR processing.
 *
 *\b Note: platform authorization needed.
 *
 * Tested ESYS commands:
 *  - Esys_PCR_Allocate() (M)
 *  - Esys_PCR_Event() (M)
 *  - Esys_PCR_Extend() (M)
 *  - Esys_PCR_Read() (M)
 *  - Esys_PCR_Reset() (M)
 *
 * @param[in,out] esys_context The ESYS_CONTEXT.
 * @retval EXIT_FAILURE
 * @retval EXIT_SKIP
 * @retval EXIT_SUCCESS
 */

int
test_esys_pcr_basic(ESYS_CONTEXT * esys_context)
{
    TSS2_RC r;
    int failure_return = EXIT_FAILURE;

    TPMS_CAPABILITY_DATA *savedPCRs = NULL;
    TPML_PCR_SELECTION *pcrSelectionOut = NULL;
    TPML_DIGEST *pcrValues = NULL;
    TPML_DIGEST_VALUES *digestsEvent = NULL;

    ESYS_TR  pcrHandle_handle = 16;
    TPML_DIGEST_VALUES digests
        = {
        .count = 1,
        .digests = {
            {
                .hashAlg = TPM2_ALG_SHA256,
                .digest = {
                    .sha1 = { 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                              11, 12, 13, 14, 15, 16, 17, 18, 19}
                }
            },
        }};

    r = Esys_PCR_Extend(
        esys_context,
        pcrHandle_handle,
        ESYS_TR_PASSWORD,
        ESYS_TR_NONE,
        ESYS_TR_NONE,
        &digests
        );
    goto_if_error(r, "Error: PCR_Extend", error);

    TPML_PCR_SELECTION pcrSelectionIn = {
        .count = 1,
        .pcrSelections = {
            { .hash = TPM2_ALG_SHA256,
              .sizeofSelect = 3,
              .pcrSelect = { 01, 00, 03}
            },
        }
    };
    UINT32 pcrUpdateCounter;

    r = Esys_PCR_Read(
        esys_context,
        ESYS_TR_NONE,
        ESYS_TR_NONE,
        ESYS_TR_NONE,
        &pcrSelectionIn,
        &pcrUpdateCounter,
        &pcrSelectionOut,
        &pcrValues);
    goto_if_error(r, "Error: PCR_Read", error);

    r = Esys_PCR_Reset(
        esys_context,
        pcrHandle_handle,
        ESYS_TR_PASSWORD,
        ESYS_TR_NONE,
        ESYS_TR_NONE);

    goto_if_error(r, "Error: PCR_Reset", error);

    TPM2B_EVENT eventData = { .size = 20,
                              .buffer={0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0,
                                       1, 2, 3, 4, 5, 6, 7, 8, 9}};
    r = Esys_PCR_Event(
        esys_context,
        pcrHandle_handle,
        ESYS_TR_PASSWORD,
        ESYS_TR_NONE,
        ESYS_TR_NONE,
        &eventData,
        &digestsEvent);

    goto_if_error(r, "Error: PCR_Reset", error);

    TPMI_YES_NO allocationSuccess;
    UINT32 maxPCR;
    UINT32 sizeNeeded;
    UINT32 sizeAvailable;

    r = Esys_GetCapability(esys_context,
                           ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE,
                           TPM2_CAP_PCRS, 0, 10, NULL, &savedPCRs);
    goto_if_error(r, "Error: GetCapabilities", error);


    r = Esys_PCR_Allocate(
        esys_context,
        ESYS_TR_RH_PLATFORM,
        ESYS_TR_PASSWORD,
        ESYS_TR_NONE,
        ESYS_TR_NONE,
        &pcrSelectionIn,
        &allocationSuccess,
        &maxPCR,
        &sizeNeeded,
        &sizeAvailable);

    if (number_rc(r) == TPM2_RC_BAD_AUTH) {
        /* Platform authorization not possible test will be skipped */
        LOG_WARNING("Platform authorization not possible.");
        failure_return =  EXIT_SKIP;
    }

    goto_if_error(r, "Error: PCR_Allocate", error);

    r = Esys_PCR_Allocate(
        esys_context,
        ESYS_TR_RH_PLATFORM,
        ESYS_TR_PASSWORD,
        ESYS_TR_NONE,
        ESYS_TR_NONE,
        &savedPCRs->data.assignedPCR,
        &allocationSuccess,
        &maxPCR,
        &sizeNeeded,
        &sizeAvailable);

    goto_if_error(r, "Error: PCR_Allocate", error);

    Esys_Free(savedPCRs);
    Esys_Free(pcrSelectionOut);
    Esys_Free(pcrValues);
    Esys_Free(digestsEvent);
    return EXIT_SUCCESS;

 error:
    Esys_Free(savedPCRs);
    Esys_Free(pcrSelectionOut);
    Esys_Free(pcrValues);
    Esys_Free(digestsEvent);
    return failure_return;

}

int
test_invoke_esys(ESYS_CONTEXT * esys_context) {
    return test_esys_pcr_basic(esys_context);
}
