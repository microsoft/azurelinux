/* SPDX-License-Identifier: BSD-2-Clause */
/*******************************************************************************
 * Copyright 2018-2019, Fraunhofer SIT sponsored by Infineon Technologies AG
 * All rights reserved.
 ******************************************************************************/

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <stdlib.h>
#include <string.h>

#include "tss2_fapi.h"
#include "fapi_int.h"
#include "fapi_util.h"
#include "tss2_esys.h"
#define LOGMODULE fapi
#include "util/log.h"
#include "util/aux_util.h"

/** One-Call function for Fapi_GetRandom
 *
 * Creates an array with a specified number of bytes. May execute the underlying
 * TPM command multiple times if the requested number of bytes is too big.
 *
 * @param[in,out] context The FAPI_CONTEXT
 * @param[in] numBytes The number of bytes requested from the TPM
 * @param[out] data The array of random bytes returned from the TPM
 *
 * @retval TSS2_RC_SUCCESS: if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE: if context or data is NULL.
 * @retval TSS2_FAPI_RC_BAD_CONTEXT: if context corruption is detected.
 * @retval TSS2_FAPI_RC_BAD_VALUE: if numBytes is 0.
 * @retval TSS2_FAPI_RC_BAD_SEQUENCE: if the context has an asynchronous
 *         operation already pending.
 * @retval TSS2_FAPI_RC_IO_ERROR: if the data cannot be saved.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory for
 *         internal operations or return parameters.
 * @retval TSS2_FAPI_RC_NO_TPM if FAPI was initialized in no-TPM-mode via its
 *         config file.
 * @retval TSS2_FAPI_RC_PATH_NOT_FOUND if a FAPI object path was not found
 *         during authorization.
 * @retval TSS2_FAPI_RC_KEY_NOT_FOUND if a key was not found.
 * @retval TSS2_FAPI_RC_TRY_AGAIN if an I/O operation is not finished yet and
 *         this function needs to be called again.
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
Fapi_GetRandom(
    FAPI_CONTEXT *context,
    size_t        numBytes,
    uint8_t     **data)
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

    r = Fapi_GetRandom_Async(context, numBytes);
    return_if_error_reset_state(r, "GetRandom");

    do {
        /* We wait for file I/O to be ready if the FAPI state automata
           are in a file I/O state. */
        r = ifapi_io_poll(&context->io);
        return_if_error(r, "Something went wrong with IO polling");

        /* Repeatedly call the finish function, until FAPI has transitioned
           through all execution stages / states of this invocation. */
        r = Fapi_GetRandom_Finish(context, data);
    } while (base_rc(r) == TSS2_BASE_RC_TRY_AGAIN);

    /* Reset the ESYS timeout to non-blocking, immediate response. */
    r2 = Esys_SetTimeout(context->esys, 0);
    return_if_error(r2, "Set Timeout to non-blocking");

    return_if_error_reset_state(r, "GetRandom");

    LOG_TRACE("finished");
    return TSS2_RC_SUCCESS;
}

/** Asynchronous function for Fapi_GetRandom
 *
 * Creates an array with a specified number of bytes. May execute the underlying
 * TPM command multiple times if the requested number of bytes is too big.
 *
 * Call Fapi_GetRandom_Finish to finish the execution of this command.
 *
 * @param[in,out] context The FAPI_CONTEXT
 * @param[in] numBytes The number of bytes requested from the TPM
 *
 * @retval TSS2_RC_SUCCESS: if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE: if context is NULL.
 * @retval TSS2_FAPI_RC_BAD_CONTEXT: if context corruption is detected.
 * @retval TSS2_FAPI_RC_BAD_VALUE: if numBytes is 0.
 * @retval TSS2_FAPI_RC_BAD_SEQUENCE: if the context has an asynchronous
 *         operation already pending.
 * @retval TSS2_FAPI_RC_IO_ERROR: if the data cannot be saved.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory for
 *         internal operations or return parameters.
 * @retval TSS2_FAPI_RC_NO_TPM if FAPI was initialized in no-TPM-mode via its
 *         config file.
 * @retval TSS2_FAPI_RC_PATH_NOT_FOUND if a FAPI object path was not found
 *         during authorization.
 * @retval TSS2_FAPI_RC_KEY_NOT_FOUND if a key was not found.
 * @retval TSS2_FAPI_RC_NOT_PROVISIONED FAPI was not provisioned.
 * @retval TSS2_FAPI_RC_BAD_PATH if the path is used in inappropriate context
 *         or contains illegal characters.
 */
TSS2_RC
Fapi_GetRandom_Async(
    FAPI_CONTEXT *context,
    size_t        numBytes)
{
    LOG_TRACE("called for context:%p", context);
    LOG_TRACE("numBytes: %zu", numBytes);

    TSS2_RC r;

    /* Check for NULL parameters */
    check_not_null(context);

    /* Helpful alias pointers */
    IFAPI_GetRandom * command = &context->get_random;

    /* Reset all context-internal session state information. */
    r = ifapi_session_init(context);
    return_if_error(r, "Initialize GetRandom");

    /* Copy parameters to context for use during _Finish. */
    command->numBytes = numBytes;
    command->ret_data = NULL;
    command->data = NULL;

    /* Start a session for integrity protection and encryption of random data. */
    r = ifapi_get_sessions_async(context,
                                 IFAPI_SESSION_GENEK | IFAPI_SESSION1,
                                 TPMA_SESSION_ENCRYPT | TPMA_SESSION_DECRYPT, 0);
    return_if_error_reset_state(r, "Create FAPI session");

    /* Initialize the context state for this operation. */
    context->state = GET_RANDOM_WAIT_FOR_SESSION;
    LOG_TRACE("finished");
    return TSS2_RC_SUCCESS;
}

/** Asynchronous finish function for Fapi_GetRandom
 *
 * This function should be called after a previous Fapi_GetRandom_Async.
 *
 * @param[in,out] context The FAPI_CONTEXT
 * @param[out] data The array of random bytes returned from the TPM
 *
 * @retval TSS2_RC_SUCCESS: if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE: if context or data is NULL.
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
 * @retval TSS2_FAPI_RC_PATH_NOT_FOUND if a FAPI object path was not found
 *         during authorization.
 * @retval TSS2_FAPI_RC_KEY_NOT_FOUND if a key was not found.
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
Fapi_GetRandom_Finish(
    FAPI_CONTEXT *context,
    uint8_t     **data)
{
    LOG_TRACE("called for context:%p", context);

    TSS2_RC r;

    /* Check for NULL parameters */
    check_not_null(context);
    check_not_null(data);

    /* Helpful alias pointers */
    IFAPI_GetRandom * command = &context->get_random;

    switch (context->state) {
        statecase(context->state, GET_RANDOM_WAIT_FOR_SESSION);
        r = ifapi_get_sessions_finish(context, &context->profiles.default_profile,
                                      context->profiles.default_profile.nameAlg);
            return_try_again(r);
            goto_if_error_reset_state(r, " FAPI create session", error_cleanup);

            context->get_random_state = GET_RANDOM_INIT;

            fallthrough;

        statecase(context->state, GET_RANDOM_WAIT_FOR_RANDOM);
            /* Retrieve the random data from the TPM.
               This may involve several Esys_GetRandom calls. */
            r = ifapi_get_random(context, command->numBytes, &command->ret_data);
            return_try_again(r);
            goto_if_error_reset_state(r, "FAPI GetRandom", error_cleanup);
            fallthrough;

        statecase(context->state, GET_RANDOM_CLEANUP)
            /* Cleanup the session. */
            r = ifapi_cleanup_session(context);
            try_again_or_error_goto(r, "Cleanup", error_cleanup);

            *data = command->ret_data;
            break;

        statecasedefault(context->state);
    }

    /* Cleanup any intermediate results and state stored in the context. */
    context->state = _FAPI_STATE_INIT;
    ifapi_cleanup_ifapi_object(&context->createPrimary.pkey_object);
    ifapi_session_clean(context);
    LOG_TRACE("finished");
    return TSS2_RC_SUCCESS;

error_cleanup:
    /* Cleanup any intermediate results and state stored in the context. */
    ifapi_cleanup_ifapi_object(&context->createPrimary.pkey_object);
    ifapi_session_clean(context);
    SAFE_FREE(context->get_random.data);
    LOG_TRACE("finished");
    return r;
}
