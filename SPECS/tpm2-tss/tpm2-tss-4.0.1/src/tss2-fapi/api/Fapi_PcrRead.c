/* SPDX-License-Identifier: BSD-2-Clause */
/*******************************************************************************
 * Copyright 2018-2019, Fraunhofer SIT sponsored by Infineon Technologies AG
 * All rights reserved.
 ******************************************************************************/

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <stdio.h>
#include <string.h>

#include "tss2_fapi.h"
#include "fapi_int.h"
#include "fapi_util.h"
#include "tss2_esys.h"
#define LOGMODULE fapi
#include "util/log.h"
#include "util/aux_util.h"

/** One-Call function for Fapi_PcrRead
 *
 * Reads from a given PCR and returns the value and the event log.
 *
 * @param[in,out] context The FAPI_CONTEXT
 * @param[in] pcrIndex The index of the PCR to read
 * @param[out] pcrValue The value of the PCR. May be NULL
 * @param[out] pcrValueSize The size of value in bytes. May be NULL
 * @param[out] pcrLog The PCR log. May be NULL
 *
 * @retval TSS2_RC_SUCCESS: if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE: if context, pcrValue or pcrValueSize
 *              is NULL.
 * @retval TSS2_FAPI_RC_BAD_CONTEXT: if context corruption is detected.
 * @retval TSS2_FAPI_RC_BAD_VALUE: if pcrIndex is invalid.
 * @retval TSS2_FAPI_RC_BAD_SEQUENCE: if the context has an asynchronous
 *         operation already pending.
 * @retval TSS2_FAPI_RC_IO_ERROR: if the data cannot be saved.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory for
 *         internal operations or return parameters.
 * @retval TSS2_FAPI_RC_NO_TPM if FAPI was initialized in no-TPM-mode via its
 *         config file.
 * @retval TSS2_FAPI_RC_TRY_AGAIN if an I/O operation is not finished yet and
 *         this function needs to be called again.
 * @retval TSS2_FAPI_RC_AUTHORIZATION_UNKNOWN if a required authorization callback
 *         is not set.
 * @retval TSS2_FAPI_RC_AUTHORIZATION_FAILED if the authorization attempt fails.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE if an internal error occurred.
 * @retval TSS2_FAPI_RC_POLICY_UNKNOWN if policy search for a certain policy digest
 *         was not successful.
 * @retval TSS2_FAPI_RC_NO_CERT if an error did occur during certificate downloading.
 * @retval TSS2_FAPI_RC_PATH_NOT_FOUND if a FAPI object path was not found
 *         during authorization.
 * @retval TSS2_FAPI_RC_KEY_NOT_FOUND if a key was not found.
 * @retval TSS2_ESYS_RC_* possible error codes of ESAPI.
 */
TSS2_RC
Fapi_PcrRead(
    FAPI_CONTEXT *context,
    uint32_t      pcrIndex,
    uint8_t     **pcrValue,
    size_t       *pcrValueSize,
    char        **pcrLog)
{
    LOG_TRACE("called for context:%p", context);

    TSS2_RC r, r2;

    /* Check for NULL parameters */
    check_not_null(context);

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

    r = Fapi_PcrRead_Async(context, pcrIndex);
    return_if_error_reset_state(r, "PCR_ReadWithLog");

    do {
        /* We wait for file I/O to be ready if the FAPI state automata
           are in a file I/O state. */
        r = ifapi_io_poll(&context->io);
        return_if_error(r, "Something went wrong with IO polling");

        /* Repeatedly call the finish function, until FAPI has transitioned
           through all execution stages / states of this invocation. */
        r = Fapi_PcrRead_Finish(context, pcrValue, pcrValueSize, pcrLog);
    } while (base_rc(r) == TSS2_BASE_RC_TRY_AGAIN);

    /* Reset the ESYS timeout to non-blocking, immediate response. */
    r2 = Esys_SetTimeout(context->esys, 0);
    return_if_error(r2, "Set Timeout to non-blocking");

    return_if_error_reset_state(r, "NV_ReadWithLog");

    LOG_TRACE("finished");
    return TSS2_RC_SUCCESS;
}

/** Asynchronous function for Fapi_PcrRead
 *
 * Reads from a given PCR and returns the value and the event log.
 *
 * Call Fapi_PcrRead_Finish to finish the execution of this command.
 *
 * @param[in,out] context The FAPI_CONTEXT
 * @param[in] pcrIndex The index of the PCR to read
 *
 * @retval TSS2_RC_SUCCESS: if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE: if context is NULL.
 * @retval TSS2_FAPI_RC_BAD_CONTEXT: if context corruption is detected.
 * @retval TSS2_FAPI_RC_BAD_VALUE: if pcrIndex is invalid.
 * @retval TSS2_FAPI_RC_BAD_SEQUENCE: if the context has an asynchronous
 *         operation already pending.
 * @retval TSS2_FAPI_RC_IO_ERROR: if the data cannot be saved.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory for
 *         internal operations or return parameters.
 * @retval TSS2_FAPI_RC_NO_TPM if FAPI was initialized in no-TPM-mode via its
 *         config file.
 * @retval TSS2_ESYS_RC_* possible error codes of ESAPI.
 */
TSS2_RC
Fapi_PcrRead_Async(
    FAPI_CONTEXT *context,
    uint32_t      pcrIndex)
{
    LOG_TRACE("called for context:%p", context);
    LOG_TRACE("pcrIndex: %" PRIu32, pcrIndex);

    TSS2_RC r;
    TPML_PCR_SELECTION pcr_selection;

    /* Check for NULL parameters */
    check_not_null(context);

    /* Helpful alias pointers */
    IFAPI_PCR * command = &context->cmd.pcr;

    /* Reset all context-internal session state information. */
    r = ifapi_session_init(context);
    return_if_error(r, "Initialize PcrRead");

    /* Determine the banks to be used for the requested PCR based on
       the default cryptographic profile. */
    pcr_selection = context->profiles.default_profile.pcr_selection;

    r = ifapi_filter_pcr_selection_by_index(&pcr_selection, &pcrIndex, 1);
    return_if_error(r, "PCR selection");

    /* Perform the PCR read operation. */
    r = Esys_PCR_Read_Async(context->esys,
                            ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE,
                            &pcr_selection);
    return_if_error(r, "PCR Read");

    /* Used for retrieving the eventlog during finish*/
    command->pcrIndex = pcrIndex;

    /* Initialize the context state for this operation. */
    context->state = PCR_READ_READ_PCR;

    LOG_TRACE("finished");
    return TSS2_RC_SUCCESS;
}

/** Asynchronous finish function for Fapi_PcrRead
 *
 * This function should be called after a previous Fapi_PcrRead_Async.
 *
 * @param[in,out] context The FAPI_CONTEXT
 * @param[out] pcrValue The value of the PCR. May be NULL
 * @param[out] pcrValueSize The size of value in bytes. May be NULL
 * @param[out] pcrLog The PCR log. May be NULL
 *
 * @retval TSS2_RC_SUCCESS: if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE: if context, pcrValue or pcrValueSize
 *         is NULL.
 * @retval TSS2_FAPI_RC_BAD_CONTEXT: if context corruption is detected.
 * @retval TSS2_FAPI_RC_BAD_SEQUENCE: if the context has an asynchronous
 *         operation already pending.
 * @retval TSS2_FAPI_RC_IO_ERROR: if the data cannot be saved.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory for
 *         internal operations or return parameters.
 * @retval TSS2_FAPI_RC_TRY_AGAIN: if the asynchronous operation is not yet
 *         complete. Call this function again later.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_ESYS_RC_* possible error codes of ESAPI.
 */
TSS2_RC
Fapi_PcrRead_Finish(
    FAPI_CONTEXT *context,
    uint8_t     **pcrValue,
    size_t       *pcrValueSize,
    char        **pcrLog)
{
    LOG_TRACE("called for context:%p", context);

    TSS2_RC r;

    /* Check for NULL parameters */
    check_not_null(context);

    /* Helpful alias pointers */
    IFAPI_PCR * command = &context->cmd.pcr;

    command->pcrValues = NULL;

    switch (context->state) {
        statecase(context->state, PCR_READ_READ_PCR);
            SAFE_FREE(command->pcrValues);
            r = Esys_PCR_Read_Finish(context->esys,
                                     &command->update_count,
                                     NULL,
                                     &command->pcrValues);
            return_try_again(r);
            goto_if_error_reset_state(r, "PCR_ReadWithLog_Finish", cleanup);

            /* Copy the return values to the output parameters. */
            if (pcrValueSize)
                command->pcrValueSize = command->pcrValues->digests[0].size;
            if (pcrValue) {
                command->pcrValue = malloc(command->pcrValues->digests[0].size);
                goto_if_null2(command->pcrValue, "Out of memory.",
                        r, TSS2_FAPI_RC_MEMORY, cleanup);

                memcpy(command->pcrValue, &command->pcrValues->digests[0].buffer[0],
                       command->pcrValues->digests[0].size);
            }
            SAFE_FREE(command->pcrValues);

            /* If no event log was requested the operation is now complete. */
            if (!pcrLog) {
                if (pcrValue)
                    *pcrValue = command->pcrValue;
                if (pcrValueSize)
                    *pcrValueSize = command->pcrValueSize;
                context->state = _FAPI_STATE_INIT;
                break;
            }

            /* Retrieve the eventlog for the requestion PCR. */
            r = ifapi_eventlog_get_async(&context->eventlog, &context->io,
                                         &command->pcrIndex, 1);
            goto_if_error(r, "Error getting event log", cleanup);

            fallthrough;

        statecase(context->state, PCR_READ_READ_EVENT_LIST);
            r = ifapi_eventlog_get_finish(&context->eventlog, &context->io, pcrLog);
            return_try_again(r);
            goto_if_error(r, "Error getting event log", cleanup);

            if (pcrValue)
                *pcrValue = command->pcrValue;
            if (pcrValueSize)
                *pcrValueSize = command->pcrValueSize;
            context->state = _FAPI_STATE_INIT;
            break;

        statecasedefault(context->state);
    }

cleanup:
    /* Cleanup any intermediate results and state stored in the context. */
    if (r) {
        /* The result will be deleted in error cases. */
        SAFE_FREE(command->pcrValue);
    }
    SAFE_FREE(command->pcrValues);
    LOG_TRACE("finished");
    return r;
}
