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

/** Test the ESYS commands HashSequenceStart, SequenceUpdate,
 *  and EventSequenceComplete.
 *
 * Tested ESYS commands:
 *  - Esys_EventSequenceComplete() (M)
 *  - Esys_HashSequenceStart() (M)
 *  - Esys_SequenceUpdate() (M)
 *
 * @param[in,out] esys_context The ESYS_CONTEXT.
 * @retval EXIT_FAILURE
 * @retval EXIT_SUCCESS
 */

int
test_esys_event_sequence_complete(ESYS_CONTEXT * esys_context)
{
    TSS2_RC r;

    TPM2B_AUTH auth = {.size = 20,
                       .buffer={10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
                                20, 21, 22, 23, 24, 25, 26, 27, 28, 29}};

    TPMI_ALG_HASH hashAlg = TPM2_ALG_NULL;   /**< enforce event Sequence */
    ESYS_TR sequenceHandle_handle;
    TPML_DIGEST_VALUES *results = NULL;

    r = Esys_HashSequenceStart(esys_context,
                               ESYS_TR_NONE,
                               ESYS_TR_NONE,
                               ESYS_TR_NONE,
                               &auth,
                               hashAlg,
                               &sequenceHandle_handle
                               );
    goto_if_error(r, "Error: HashSequenceStart", error);

    TPM2B_MAX_BUFFER buffer = {.size = 20,
                              .buffer={10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
                                       20, 21, 22, 23, 24, 25, 26, 27, 28, 29}};

    r = Esys_TR_SetAuth(esys_context, sequenceHandle_handle, &auth);
    goto_if_error(r, "Error esys TR_SetAuth ", error);

    r = Esys_SequenceUpdate(esys_context,
                            sequenceHandle_handle,
                            ESYS_TR_PASSWORD,
                            ESYS_TR_NONE,
                            ESYS_TR_NONE,
                            &buffer
                            );
    goto_if_error(r, "Error: SequenceUpdate", error);

    ESYS_TR pcrHandle_handle = 16;

    r = Esys_EventSequenceComplete (
        esys_context,
        pcrHandle_handle,
        sequenceHandle_handle,
        ESYS_TR_PASSWORD,
        ESYS_TR_PASSWORD,
        ESYS_TR_NONE,
        &buffer,
        &results);
    goto_if_error(r, "Error: EventSequenceComplete", error);

    Esys_Free(results);
    return EXIT_SUCCESS;

 error:
    Esys_Free(results);
    return EXIT_FAILURE;
}

int
test_invoke_esys(ESYS_CONTEXT * esys_context) {
    return test_esys_event_sequence_complete(esys_context);
}
