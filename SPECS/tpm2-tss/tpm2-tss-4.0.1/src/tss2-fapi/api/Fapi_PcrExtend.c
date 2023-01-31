/* SPDX-License-Identifier: BSD-2-Clause */
/*******************************************************************************
 * Copyright 2018-2019, Fraunhofer SIT sponsored by Infineon Technologies AG
 * All rights reserved.
 ******************************************************************************/

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include "tss2_fapi.h"
#include "fapi_int.h"
#include "fapi_util.h"
#include "tss2_esys.h"
#include "ifapi_json_serialize.h"
#include "fapi_crypto.h"
#define LOGMODULE fapi
#include "util/log.h"
#include "util/aux_util.h"

/** One-Call function for Fapi_PcrExtend
 *
 * Performs an extend operation on a given PCR.
 *
 * @param[in,out] context The FAPI_CONTEXT
 * @param[in] pcr The PCR to extend
 * @param[in] data The data that is to be extended on the PCR
 * @param[in] dataSize The size of data in bytes
 * @param[in] logData A JSON representation of data to be written to the PCR's
 *            event log. May be NULL
 *
 * @retval TSS2_RC_SUCCESS: if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE: if context or data is NULL.
 * @retval TSS2_FAPI_RC_BAD_CONTEXT: if context corruption is detected.
 * @retval TSS2_FAPI_RC_NO_PCR: if no such PCR exists on this TPM.
 * @retval TSS2_FAPI_RC_BAD_SEQUENCE: if the context has an asynchronous
 *         operation already pending.
 * @retval TSS2_FAPI_RC_IO_ERROR: if the data cannot be saved.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory for
 *         internal operations or return parameters.
 * @retval TSS2_FAPI_RC_NO_TPM if FAPI was initialized in no-TPM-mode via its
 *         config file.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_TRY_AGAIN if an I/O operation is not finished yet and
 *         this function needs to be called again.
 * @retval TSS2_FAPI_RC_PATH_NOT_FOUND if a FAPI object path was not found
 *         during authorization.
 * @retval TSS2_FAPI_RC_KEY_NOT_FOUND if a key was not found.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE if an internal error occurred.
 * @retval TSS2_FAPI_RC_AUTHORIZATION_UNKNOWN if a required authorization callback
 *         is not set.
 * @retval TSS2_FAPI_RC_AUTHORIZATION_FAILED if the authorization attempt fails.
 * @retval TSS2_FAPI_RC_POLICY_UNKNOWN if policy search for a certain policy digest
 *         was not successful.
 * @retval TSS2_ESYS_RC_* possible error codes of ESAPI.
 * @retval TSS2_FAPI_RC_NOT_PROVISIONED FAPI was not provisioned.
 * @retval TSS2_FAPI_RC_BAD_PATH if the path is used in inappropriate context
 *         or contains illegal characters.
 */
TSS2_RC
Fapi_PcrExtend(
    FAPI_CONTEXT   *context,
    uint32_t        pcr,
    uint8_t  const *data,
    size_t          dataSize,
    char     const *logData)
{
    LOG_TRACE("called for context:%p", context);

    TSS2_RC r, r2;

    /* Check for NULL parameters */
    check_not_null(context);
    check_not_null(data);

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

    r = Fapi_PcrExtend_Async(context, pcr, data, dataSize, logData);
    return_if_error_reset_state(r, "PcrExtend");

    do {
        /* We wait for file I/O to be ready if the FAPI state automata
           are in a file I/O state. */
        r = ifapi_io_poll(&context->io);
        return_if_error(r, "Something went wrong with IO polling");

        /* Repeatedly call the finish function, until FAPI has transitioned
           through all execution stages / states of this invocation. */
        r = Fapi_PcrExtend_Finish(context);
    } while (base_rc(r) == TSS2_BASE_RC_TRY_AGAIN);

    /* Reset the ESYS timeout to non-blocking, immediate response. */
    r2 = Esys_SetTimeout(context->esys, 0);
    return_if_error(r2, "Set Timeout to non-blocking");

    return_if_error_reset_state(r, "PcrExtend");

    LOG_TRACE("finished");
    return TSS2_RC_SUCCESS;
}

/** Asynchronous function for Fapi_PcrExtend
 *
 * Performs an extend operation on a given PCR.
 *
 * Call Fapi_PcrExtend_Finish to finish the execution of this command.
 *
 * @param[in,out] context The FAPI_CONTEXT
 * @param[in] pcr The PCR to extend
 * @param[in] data The data that is to be extended on the PCR
 * @param[in] dataSize The size of data in bytes
 * @param[in] logData A JSON representation of data to be written to the PCR's
 *            event log. May be NULL
 *
 * @retval TSS2_RC_SUCCESS: if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE: if context or data is NULL.
 * @retval TSS2_FAPI_RC_BAD_CONTEXT: if context corruption is detected.
 * @retval TSS2_FAPI_RC_NO_PCR: if no such PCR exists on this TPM.
 * @retval TSS2_FAPI_RC_BAD_SEQUENCE: if the context has an asynchronous
 *         operation already pending.
 * @retval TSS2_FAPI_RC_IO_ERROR: if the data cannot be saved.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory for
 *         internal operations or return parameters.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_NO_TPM if FAPI was initialized in no-TPM-mode via its
 *         config file.
 * @retval TSS2_ESYS_RC_* possible error codes of ESAPI.
 */
TSS2_RC
Fapi_PcrExtend_Async(
    FAPI_CONTEXT   *context,
    uint32_t        pcr,
    uint8_t  const *data,
    size_t          dataSize,
    char     const *logData)
{
    LOG_TRACE("called for context:%p", context);
    LOG_TRACE("pcr: %u", pcr);
    if (data) {
        LOGBLOB_TRACE(data, dataSize, "data");
    } else {
        LOG_TRACE("data: (null) dataSize: %zi", dataSize);
    }
    LOG_TRACE("logData: %s", logData);

    TSS2_RC r;

    /* Check for NULL parameters */
    check_not_null(context);
    check_not_null(data);

    /* Helpful alias pointers */
    IFAPI_PCR * command = &context->cmd.pcr;

    /* Reset all context-internal session state information. */
    r = ifapi_session_init(context);
    goto_if_error(r, "Initialize PcrExtend", error_cleanup);

    /* Perform some sanity checks on the input. */
    if (dataSize > 1024 || dataSize == 0) {
        goto_error(r, TSS2_FAPI_RC_BAD_VALUE,
                "Event size must be > 1024 and != 0", error_cleanup);
    }

    /* Copy parameters to context for use during _Finish. */
    strdup_check(command->logData, logData, r, error_cleanup);
    command->event.size = dataSize;
    memcpy(&command->event.buffer[0], data, dataSize);
    command->pcrIndex = pcr;

    r = Esys_GetCapability_Async(context->esys,
                                 ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE,
                                 TPM2_CAP_PCRS, 0, 1);
    goto_if_error(r, "Esys_GetCapability_Async", error_cleanup);

    /* Initialize the context state for this operation. */
    context->state = PCR_EXTEND_WAIT_FOR_GET_CAP;
    LOG_TRACE("finished");
    return TSS2_RC_SUCCESS;

error_cleanup:
    /* Cleanup duplicated input parameters that were copied before. */
    SAFE_FREE(command->logData);
    return r;
}

/** Asynchronous finish function for Fapi_PcrExtend
 *
 * This function should be called after a previous Fapi_PcrExtend_Async.
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
 * @retval TSS2_FAPI_RC_TRY_AGAIN: if the asynchronous operation is not yet
 *         complete. Call this function again later.
 * @retval TSS2_FAPI_RC_PATH_NOT_FOUND if a FAPI object path was not found
 *         during authorization.
 * @retval TSS2_FAPI_RC_KEY_NOT_FOUND if a key was not found.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE if an internal error occurred.
 * @retval TSS2_FAPI_RC_AUTHORIZATION_UNKNOWN if a required authorization callback
 *         is not set.
 * @retval TSS2_FAPI_RC_AUTHORIZATION_FAILED if the authorization attempt fails.
 * @retval TSS2_FAPI_RC_POLICY_UNKNOWN if policy search for a certain policy digest
 *         was not successful.
 * @retval TSS2_ESYS_RC_* possible error codes of ESAPI.
 * @retval TSS2_FAPI_RC_NOT_PROVISIONED FAPI was not provisioned.
 * @retval TSS2_FAPI_RC_BAD_PATH if the path is used in inappropriate context
 *         or contains illegal characters.
 */
TSS2_RC
Fapi_PcrExtend_Finish(
    FAPI_CONTEXT   *context)
{
    LOG_TRACE("called for context:%p", context);

    TSS2_RC r;
    TPMI_YES_NO moreData;

    /* Check for NULL parameters */
    check_not_null(context);

    /* Helpful alias pointers */
    IFAPI_PCR * command = &context->cmd.pcr;
    TPMS_CAPABILITY_DATA **capabilityData = &command->capabilityData;
    IFAPI_EVENT * pcrEvent = &command->pcr_event;
    IFAPI_TSS_EVENT * subEvent = &pcrEvent->content.tss_event;

    switch (context->state) {
        statecase(context->state, PCR_EXTEND_WAIT_FOR_GET_CAP);
            command->event_log_file = NULL;
            r = Esys_GetCapability_Finish(context->esys, &moreData, capabilityData);
            return_try_again(r);
            goto_if_error_reset_state(r, "GetCapablity_Finish", error_cleanup);

            /* Construct the filename for the eventlog file */
            r = ifapi_asprintf(&command->event_log_file, "%s/%s%i",
                               context->eventlog.log_dir, IFAPI_PCR_LOG_FILE, command->pcrIndex);
            return_if_error(r, "Out of memory.");

            /* Check wheter the event log has to be read. */
            if (ifapi_io_path_exists(command->event_log_file)) {
                r = ifapi_io_read_async(&context->io, command->event_log_file);
                goto_if_error_reset_state(r, "Read event log", error_cleanup);
                context->eventlog.state = IFAPI_EVENTLOG_STATE_READING;
            } else {
                context->eventlog.state = IFAPI_EVENTLOG_STATE_APPENDING;
                SAFE_FREE(command->event_log_file);
            }

            fallthrough;

        statecase(context->state,PCR_EXTEND_READ_EVENT_LOG);
            /* Check whether log file contains valid json. */
            r = ifapi_eventlog_append_check(&context->eventlog, &context->io);
            return_try_again(r);
            goto_if_error(r, "ifapi_eventlog_append_check", error_cleanup);

            /* Prepare session used for integrity protecting the PCR Event operation. */
            r = ifapi_get_sessions_async(context,
                                         IFAPI_SESSION_GENEK | IFAPI_SESSION1,
                                         0, 0);
            goto_if_error_reset_state(r, "Create sessions", error_cleanup);

            fallthrough;

        statecase(context->state, PCR_EXTEND_WAIT_FOR_SESSION);
            r = ifapi_get_sessions_finish(context, &context->profiles.default_profile,
                                          context->profiles.default_profile.nameAlg);
            return_try_again(r);
            goto_if_error_reset_state(r, " FAPI create session", error_cleanup);

            /* Call PCR Event on the TPM, which performs an extend to all banks. */
            r = Esys_PCR_Event_Async(context->esys, command->pcrIndex,
                                     context->session1, ESYS_TR_NONE, ESYS_TR_NONE,
                                     &command->event);
            return_if_error(r, "Esys_PCR_Event_Async");
            command->event_digests = NULL;

            fallthrough;

        statecase(context->state, PCR_EXTEND_FINISH);
            r = Esys_PCR_Event_Finish(context->esys, &command->event_digests);
            return_try_again(r);
            goto_if_error_reset_state(r, "PCR_Extend_Finish", error_cleanup);

            /* Construct the eventLog entry. */
            pcrEvent->digests = *command->event_digests;
            pcrEvent->pcr = command->pcrIndex;
            pcrEvent->content_type = IFAPI_TSS_EVENT_TAG;
            subEvent->data = command->event;
            if (command->logData) {
                strdup_check(subEvent->event,
                    command->logData, r, error_cleanup);
            } else {
                subEvent->event = NULL;
            }
            fallthrough;

        statecase(context->state, PCR_EXTEND_APPEND_EVENT_LOG);
            r = ifapi_eventlog_append_finish(&context->eventlog, &context->io,
                                             &command->pcr_event);
            return_try_again(r);
            goto_if_error(r, "ifapi_eventlog_append_finish", error_cleanup);

            SAFE_FREE(command->event_digests);
            fallthrough;

        statecase(context->state, PCR_EXTEND_CLEANUP)
            /* Cleanup the session used for integrity checking. */
            r = ifapi_cleanup_session(context);
            try_again_or_error_goto(r, "Cleanup", error_cleanup);

            context->state =  _FAPI_STATE_INIT;
            break;

        statecasedefault(context->state);
    }

error_cleanup:
    /* Cleanup any intermediate results and state stored in the context. */
    SAFE_FREE(command->event_log_file);
    SAFE_FREE(*capabilityData);
    SAFE_FREE(command->event_digests);
    SAFE_FREE(command->logData);
    ifapi_cleanup_ifapi_object(&context->loadKey.auth_object);
    ifapi_cleanup_ifapi_object(context->loadKey.key_object);
    ifapi_cleanup_ifapi_object(&context->createPrimary.pkey_object);
    ifapi_cleanup_event(pcrEvent);
    ifapi_session_clean(context);
    LOG_TRACE("finished");
    return r;
}
