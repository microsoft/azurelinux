/* SPDX-License-Identifier: BSD-2-Clause */
/*******************************************************************************
 * Copyright 2018-2019, Fraunhofer SIT sponsored by Infineon Technologies AG
 * All rights reserved.
 ******************************************************************************/

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <json-c/json_util.h>
#include <json-c/json_tokener.h>
#include <string.h>

#include "ifapi_json_serialize.h"
#include "tss2_fapi.h"
#include "fapi_int.h"
#include "fapi_util.h"
#include "tss2_esys.h"
#define LOGMODULE fapi
#include "util/log.h"
#include "util/aux_util.h"

typedef struct {
    char *description;
    TPMI_POLICYTYPE capability;
    UINT32 property;
    UINT32 max;
} IFAPI_INFO_CAP;

#define CAP_IDX_PT_FIXED 9

static IFAPI_INFO_CAP info_cap_tab[] = {
    { "algorithms", TPM2_CAP_ALGS,  TPM2_ALG_FIRST, TPM2_MAX_CAP_ALGS},
    { "handles-transient", TPM2_CAP_HANDLES, TPM2_TRANSIENT_FIRST, TPM2_MAX_CAP_HANDLES},
    { "handles-persistent", TPM2_CAP_HANDLES, TPM2_PERSISTENT_FIRST, TPM2_MAX_CAP_HANDLES},
    { "handles-permanent", TPM2_CAP_HANDLES, TPM2_PERMANENT_FIRST, TPM2_MAX_CAP_HANDLES},
    { "handles-pcr", TPM2_CAP_HANDLES, TPM2_PCR_FIRST, TPM2_MAX_CAP_HANDLES},
    { "handles-nv-index", TPM2_CAP_HANDLES, TPM2_NV_INDEX_FIRST, TPM2_MAX_CAP_HANDLES},
    { "handles-loaded-session", TPM2_CAP_HANDLES, TPM2_LOADED_SESSION_FIRST, TPM2_MAX_CAP_HANDLES},
    { "handles-action-session", TPM2_CAP_HANDLES, TPM2_ACTIVE_SESSION_FIRST, TPM2_MAX_CAP_HANDLES},
    { "handles-saved-session", TPM2_CAP_HANDLES, TPM2_ACTIVE_SESSION_FIRST, TPM2_MAX_CAP_HANDLES},
    { "properties-fixed", TPM2_CAP_TPM_PROPERTIES, TPM2_PT_FIXED, TPM2_MAX_TPM_PROPERTIES },
    { "properties-variable", TPM2_CAP_TPM_PROPERTIES, TPM2_PT_VAR, TPM2_MAX_TPM_PROPERTIES },
    { "commands", TPM2_CAP_COMMANDS, TPM2_CC_FIRST, TPM2_MAX_CAP_CC },
    { "pp-commands", TPM2_CAP_PP_COMMANDS, TPM2_CC_FIRST, TPM2_MAX_CAP_CC },
    { "audit-commands", TPM2_CAP_AUDIT_COMMANDS, TPM2_CC_FIRST, TPM2_MAX_CAP_CC },
    { "pcrs", TPM2_CAP_PCRS, 0, TPM2_NUM_PCR_BANKS },
    { "pcr-properties", TPM2_CAP_PCR_PROPERTIES, TPM2_PCR_FIRST, TPM2_MAX_PCR_PROPERTIES },
    { "ecc-curves", TPM2_CAP_ECC_CURVES, 0, TPM2_MAX_ECC_CURVES },
};

/** One-Call function for Fapi_GetInfo
 *
 * Returns a UTF-8 encoded string that identifies the versions of FAPI, TPM,
 * configurations and other relevant information.
 *
 * @param[in,out] context The FAPI_CONTEXT
 * @param[out] info The byte buffer for the information string
 *
 * @retval TSS2_RC_SUCCESS: if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE: if context or info is NULL.
 * @retval TSS2_FAPI_RC_BAD_CONTEXT: if context corruption is detected.
 * @retval TSS2_FAPI_RC_BAD_SEQUENCE: if the context has an asynchronous
 *         operation already pending.
 * @retval TSS2_FAPI_RC_IO_ERROR: if the data cannot be saved.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory for
 *         internal operations or return parameters.
 * @retval TSS2_FAPI_RC_NO_TPM if FAPI was initialized in no-TPM-mode via its
 *         config file.
 * @retval TSS2_FAPI_RC_TRY_AGAIN if an I/O operation is not finished yet and
 *         this function needs to be called again.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE if an internal error occurred.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_ESYS_RC_* possible error codes of ESAPI.
 */
TSS2_RC
Fapi_GetInfo(
    FAPI_CONTEXT *context,
    char        **info)
{
    LOG_TRACE("called for context:%p", context);

    TSS2_RC r, r2;

    /* Check for NULL parameters */
    check_not_null(context);
    check_not_null(info);

    /* Check whether TCTI and ESYS are initialized */
    return_if_null(context->esys, "Command can't be executed in none TPM mode.",
                   TSS2_FAPI_RC_NO_TPM);

    /* If the async state automata of FAPI shall be tested, then we must not set
       the timeouts of ESYS to blocking mode.
       During testing, the mssim tcti will ensure multiple re-invocations.
       Usually however the synchronous invocations of FAPI shall instruct ESYS
       to block until a result is available. */
#ifndef TEST_FAPI_ASYNC
    r = Esys_SetTimeout(context->esys, TSS2_TCTI_TIMEOUT_BLOCK);
    return_if_error_reset_state(r, "Set Timeout to blocking");
#endif /* TEST_FAPI_ASYNC */

    r = Fapi_GetInfo_Async(context);
    return_if_error_reset_state(r, "GetTPMInfo");

    do {
        /* We wait for file I/O to be ready if the FAPI state automata
           are in a file I/O state. */
        r = ifapi_io_poll(&context->io);
        return_if_error(r, "Something went wrong with IO polling");

        /* Repeatedly call the finish function, until FAPI has transitioned
           through all execution stages / states of this invocation. */
        r = Fapi_GetInfo_Finish(context, info);
    } while (base_rc(r) == TSS2_BASE_RC_TRY_AGAIN);

    /* Reset the ESYS timeout to non-blocking, immediate response. */
    r2 = Esys_SetTimeout(context->esys, 0);
    return_if_error(r2, "Set Timeout to non-blocking");

    return_if_error_reset_state(r, "GetTPMInfo");

    LOG_TRACE("finished");
    return TSS2_RC_SUCCESS;
}

/** Asynchronous function for Fapi_GetInfo
 *
 * Returns a UTF-8 encoded string that identifies the versions of FAPI, TPM,
 * configurations and other relevant information.
 *
 * Call Fapi_GetInfo_Finish to finish the execution of this command.
 *
 * @param[in,out] context The FAPI_CONTEXT
 *
 * @retval TSS2_RC_SUCCESS: if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE: if context is NULL.
 * @retval TSS2_FAPI_RC_BAD_CONTEXT: if context corruption is detected.
 * @retval TSS2_FAPI_RC_BAD_SEQUENCE: if the context has an asynchronous
 *         operation already pending.
 * @retval TSS2_FAPI_RC_IO_ERROR: if the data cannot be saved.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory for
 *         internal operations or return parameters.
 * @retval TSS2_FAPI_RC_NO_TPM if FAPI was initialized in no-TPM-mode via its
 *         config file.
 */
TSS2_RC
Fapi_GetInfo_Async(
    FAPI_CONTEXT *context)
{
    LOG_TRACE("called for context:%p", context);

    TSS2_RC r;

    /* Check for NULL parameters */
    check_not_null(context);

    /* Helpful alias pointers */
    IFAPI_GetInfo * command = &context->cmd.GetInfo;

    /* Reset all context-internal session state information. */
    r = ifapi_session_init(context);
    return_if_error(r, "Initialize GetInfo");

    memset(command, 0, sizeof(IFAPI_GetInfo));
    r = ifapi_capability_init(context);
    return_if_error(r, "Capability init");

    /* Initialize the context state for this operation. */
    command->idx_info_cap = 0;
    context->state = GET_INFO_GET_CAP;

    LOG_TRACE("finished");
    return TSS2_RC_SUCCESS;
}

/** Asynchronous finish function for Fapi_GetInfo
 *
 * This function should be called after a previous Fapi_GetInfo_Async.
 *
 * @param[in,out] context The FAPI_CONTEXT
 * @param[out] info The byte buffer for the information string
 *
 * @retval TSS2_RC_SUCCESS: if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE: if context or info is NULL.
 * @retval TSS2_FAPI_RC_BAD_CONTEXT: if context corruption is detected.
 * @retval TSS2_FAPI_RC_BAD_SEQUENCE: if the context has an asynchronous
 *         operation already pending.
 * @retval TSS2_FAPI_RC_IO_ERROR: if the data cannot be saved.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory for
 *         internal operations or return parameters.
 * @retval TSS2_FAPI_RC_TRY_AGAIN: if the asynchronous operation is not yet
 *         complete. Call this function again later.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE if an internal error occurred.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_ESYS_RC_* possible error codes of ESAPI.
 */
TSS2_RC
Fapi_GetInfo_Finish(
    FAPI_CONTEXT *context,
    char        **info)
{
    LOG_TRACE("called for context:%p", context);

    TSS2_RC r;
    json_object *jso = NULL;
    size_t capIdx, i;

    /* Check for NULL parameters */
    check_not_null(context);
    check_not_null(info);

    /* Helpful alias pointers */
    IFAPI_GetInfo * command = &context->cmd.GetInfo;
    IFAPI_INFO *infoObj = &command->info_obj;
    TPMS_CAPABILITY_DATA *capabilityData = NULL;

    switch (context->state) {
    case GET_INFO_GET_CAP:
        /* Initialize the property for the first ESAPI call */
        command->property
            = info_cap_tab[command->idx_info_cap].property;
        fallthrough;

    case GET_INFO_GET_CAP_MORE:
        /* This state is a helper used from fapi_util.c */
        fallthrough;

    case GET_INFO_WAIT_FOR_CAP:
        /* State will be set by sub routine */
        capIdx = command->idx_info_cap;
        r = ifapi_capability_get(context,
                                 info_cap_tab[capIdx].capability,
                                 info_cap_tab[capIdx].max,
                                 &capabilityData);
        return_try_again(r);
        goto_if_error(r, "Get capability", cleanup);

        if (info_cap_tab[capIdx].capability == TPM2_CAP_TPM_PROPERTIES &&
            info_cap_tab[capIdx].property == TPM2_PT_FIXED) {
            /* Adapt count to number of fixed properties. */
            for (i = 0; i <  capabilityData->data.tpmProperties.count; i++) {
                /* TPM2_PT_MODES is the last fixed property. */
                if (capabilityData->data.tpmProperties.tpmProperty[i].property ==  TPM2_PT_MODES) {
                    capabilityData->data.tpmProperties.count = i + 1;
                    break;
                }
            }
        }

        infoObj->cap[capIdx].description = info_cap_tab[capIdx].description;
        infoObj->cap[capIdx].capability = capabilityData;
        command->property_count = 0;
        command->idx_info_cap += 1;
        if (command->idx_info_cap <  sizeof(info_cap_tab)
                / sizeof(info_cap_tab[0])) {
            /* Not all capabilities have been collected */
            context->state = GET_INFO_GET_CAP;
            return TSS2_FAPI_RC_TRY_AGAIN;
        }

        infoObj->fapi_version = PACKAGE_STRING;
        infoObj->fapi_config = context->config;

        /* Serialize the information. */
        r = ifapi_json_IFAPI_INFO_serialize(infoObj, &jso);
        goto_if_error(r, "Error serialize info object", cleanup);

        /* Duplicate the information to be returned to the caller. */
#ifdef JSON_C_TO_STRING_NOSLASHESCAPE
        *info = strdup(json_object_to_json_string_ext(jso, JSON_C_TO_STRING_PRETTY | JSON_C_TO_STRING_NOSLASHESCAPE));
#else
         *info = strdup(json_object_to_json_string_ext(jso, JSON_C_TO_STRING_PRETTY));
#endif
        goto_if_null2(*info, "Out of memory.", r, TSS2_FAPI_RC_MEMORY, cleanup);

        context->state = _FAPI_STATE_INIT;
        r = TSS2_RC_SUCCESS;
        break;

    statecasedefault(context->state);
    }

cleanup:
    /* Cleanup any intermediate results and state stored in the context. */
    json_object_put(jso);
    for (capIdx = 0; capIdx < IFAPI_MAX_CAP_INFO; capIdx++) {
        SAFE_FREE(infoObj->cap[capIdx].capability);
    }
    LOG_TRACE("finished");
    return r;
}
