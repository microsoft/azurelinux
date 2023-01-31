/* SPDX-License-Identifier: BSD-2-Clause */
#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <stdlib.h>
#include <stdio.h>
#include "tss2_mu.h"
#include "tss2_esys.h"

#include "esys_iutil.h"
#define LOGMODULE test
#include "util/log.h"
#include "util/aux_util.h"

/** This tests the Esys_TR_GetTpmHandle and Esys_TR_GetName functions by
 *  using a dummy AC, ACT handle and validating it against the expected TPM
 *  handle and TPM name.
 *
 * Tested ESYS commands:
 * - Esys_TR_GetTpmHandle
 * - Esys_TR_GetName
 *
 * @param[in,out] ectx The ESYS_CONTEXT.
 * @retval EXIT_FAILURE
 * @retval EXIT_SUCCESS
 */

int
test_esys_tr_getName(ESYS_CONTEXT * ectx)
{
    TSS2_RC r;

    ESYS_TR ac = ESYS_TR_RH_AC(0);
    TPM2_HANDLE tpmHandle = ESYS_TR_NONE;

    r = Esys_TR_GetTpmHandle(ectx, ac, &tpmHandle);
    goto_if_error(r, "Error getting TPM Handle from Esys_TR_GetTpmHandle", error);

    if (tpmHandle != TPM2_NV_AC_FIRST) {
        LOG_ERROR("Handles mismatch");
        goto error;
    }

    TPM2B_NAME name1, *name2, act_name1, *act_name2;
    size_t offset = 0;

    r = Tss2_MU_TPM2_HANDLE_Marshal(TPM2_NV_AC_FIRST, &name1.name[0],
                                    sizeof(name1.name), &offset);
    goto_if_error(r, "Error Marshaling AC name", error);
    name1.size = offset;

    /**
     * Test AC handle
    */
    r = Esys_TR_GetName(ectx, ac, &name2);
    goto_if_error(r, "GetName for AC Handle failed", error);

    if (name1.size != name2->size ||
        memcmp(&name1.name[0], &name2->name[0], name1.size) != 0)
    {
        Esys_Free(name2);
        LOG_ERROR("Names mismatch between NV_GetPublic and TR_GetName");
        goto error;
    }

    /**
     * Test ACT handles
     */

    ESYS_TR act_handle = ESYS_TR_RH_ACT(5);
    size_t act_offset = 0;
    r = Tss2_MU_TPM2_HANDLE_Marshal(TPM2_RH_ACT_5, &act_name1.name[0],
                                    sizeof(act_name1.name), &act_offset);
    goto_if_error(r, "Error Marshaling ACT name", error);
    act_name1.size = act_offset;

    r = Esys_TR_GetName(ectx, act_handle, &act_name2);
    goto_if_error(r, "GetName for ACT Handle failed", error);

    if (act_name1.size != act_name2->size ||
        memcmp(&act_name1.name[0], &act_name2->name[0], act_name1.size) != 0)
    {
        Esys_Free(act_name2);
        LOG_ERROR("Names mismatch between NV_GetPublic and TR_GetName");
        goto error;
    }

    Esys_Free(name2);
    Esys_Free(act_name2);

    return EXIT_SUCCESS;

 error:
    return EXIT_FAILURE;
}

int
test_invoke_esys(ESYS_CONTEXT * esys_context) {
    return test_esys_tr_getName(esys_context);
}
