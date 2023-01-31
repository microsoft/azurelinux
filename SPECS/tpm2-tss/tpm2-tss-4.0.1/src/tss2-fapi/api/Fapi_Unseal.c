/* SPDX-License-Identifier: BSD-2-Clause */
/*******************************************************************************
 * Copyright 2018-2019, Fraunhofer SIT sponsored by Infineon Technologies AG
 * All rights reserved.
 ******************************************************************************/

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <stdlib.h>
#include <errno.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>

#include "tss2_fapi.h"
#include "fapi_int.h"
#include "fapi_util.h"
#include "fapi_policy.h"
#include "tss2_esys.h"
#define LOGMODULE fapi
#include "util/log.h"
#include "util/aux_util.h"
#include "fapi_crypto.h"

/** One-Call function for Fapi_Unseal
 *
 * Unseals data from a seal in the FAPI metadata store.
 *
 * @param[in,out] context The FAPI_CONTEXT
 * @param[in] path The path to the sealed data
 * @param[out] data The decrypted data after unsealing. May be NULL
 * @param[out] size The size of data in bytes. May be NULL
 *
 * @retval TSS2_RC_SUCCESS: if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE: if context or path is NULL.
 * @retval TSS2_FAPI_RC_BAD_CONTEXT: if context corruption is detected.
 * @retval TSS2_FAPI_RC_BAD_PATH: if path does not point to a sealed data object.
 * @retval TSS2_FAPI_RC_BAD_VALUE: if the digestSize is zero.
 * @retval TSS2_FAPI_RC_BAD_SEQUENCE: if the context has an asynchronous
 *         operation already pending.
 * @retval TSS2_FAPI_RC_IO_ERROR: if the data cannot be saved.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory for
 *         internal operations or return parameters.
 * @retval TSS2_FAPI_RC_NO_TPM if FAPI was initialized in no-TPM-mode via its
 *         config file.
 * @retval TSS2_FAPI_RC_TRY_AGAIN if an I/O operation is not finished yet and
 *         this function needs to be called again.
 * @retval TSS2_FAPI_RC_PATH_NOT_FOUND if a FAPI object path was not found
 *         during authorization.
 * @retval TSS2_FAPI_RC_KEY_NOT_FOUND if a key was not found.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE if an internal error occurred.
 * @retval TSS2_FAPI_RC_SIGNATURE_VERIFICATION_FAILED if the signature could not
 *         be verified
 * @retval TSS2_ESYS_RC_* possible error codes of ESAPI.
 * @retval TSS2_FAPI_RC_NOT_PROVISIONED FAPI was not provisioned.
 * @retval TSS2_FAPI_RC_AUTHORIZATION_UNKNOWN if a required authorization callback
 *         is not set.
 * @retval TSS2_FAPI_RC_AUTHORIZATION_FAILED if the authorization attempt fails.
 * @retval TSS2_FAPI_RC_POLICY_UNKNOWN if policy search for a certain policy digest
 *         was not successful.
 */
TSS2_RC
Fapi_Unseal(
    FAPI_CONTEXT  *context,
    char    const *path,
    uint8_t      **data,
    size_t        *size)
{
    LOG_TRACE("called for context:%p", context);

    TSS2_RC r, r2;

    /* Check for NULL parameters */
    check_not_null(context);
    check_not_null(path);

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

    r = Fapi_Unseal_Async(context, path);
    return_if_error_reset_state(r, "Unseal");

    do {
        /* We wait for file I/O to be ready if the FAPI state automata
           are in a file I/O state. */
        r = ifapi_io_poll(&context->io);
        return_if_error(r, "Something went wrong with IO polling");

        /* Repeatedly call the finish function, until FAPI has transitioned
           through all execution stages / states of this invocation. */
        r = Fapi_Unseal_Finish(context, data, size);
    } while (base_rc(r) == TSS2_BASE_RC_TRY_AGAIN);

    /* Reset the ESYS timeout to non-blocking, immediate response. */
    r2 = Esys_SetTimeout(context->esys, 0);
    return_if_error(r2, "Set Timeout to non-blocking");

    return_if_error_reset_state(r, "Unseal");

    LOG_TRACE("finished");
    return TSS2_RC_SUCCESS;
}

/** Asynchronous function for Fapi_Unseal
 *
 * Unseals data from a seal in the FAPI metadata store.
 *
 * Call Fapi_Unseal_Finish to finish the execution of this command.
 *
 * @param[in,out] context The FAPI_CONTEXT
 * @param[in] path The path to the sealed data
 *
 * @retval TSS2_RC_SUCCESS: if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE: if context or path is NULL.
 * @retval TSS2_FAPI_RC_BAD_CONTEXT: if context corruption is detected.
 * @retval TSS2_FAPI_RC_BAD_PATH: if path does not point to a sealed data object.
 * @retval TSS2_FAPI_RC_BAD_VALUE: if the digestSize is zero.
 * @retval TSS2_FAPI_RC_BAD_SEQUENCE: if the context has an asynchronous
 *         operation already pending.
 * @retval TSS2_FAPI_RC_IO_ERROR: if the data cannot be saved.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory for
 *         internal operations or return parameters.
 * @retval TSS2_FAPI_RC_NO_TPM if FAPI was initialized in no-TPM-mode via its
 *         config file.
 */
TSS2_RC
Fapi_Unseal_Async(
    FAPI_CONTEXT  *context,
    char    const *path)
{
    LOG_TRACE("called for context:%p", context);
    LOG_TRACE("path: %s", path);

    TSS2_RC r;

    /* Check for NULL parameters */
    check_not_null(context);
    check_not_null(path);

    /* Helpful alias pointers */
    IFAPI_Unseal * command = &context->cmd.Unseal;
    memset(command, 0 ,sizeof(IFAPI_Unseal));

    /* Reset all context-internal session state information. */
    r = ifapi_session_init(context);
    return_if_error(r, "Initialize Unseal");

    /* Copy parameters to context for use during _Finish. */
    strdup_check(command->keyPath, path, r, error_cleanup);

    /* Initialize the context state for this operation. */
    context->state = UNSEAL_WAIT_FOR_KEY;
    LOG_TRACE("finished");
    return TSS2_RC_SUCCESS;

error_cleanup:
    /* Cleanup duplicated input parameters that were copied before. */
    SAFE_FREE(command->keyPath);
    return r;
}

/** Asynchronous finish function for Fapi_Unseal
 *
 * This function should be called after a previous Fapi_Unseal_Async.
 *
 * @param[in,out] context The FAPI_CONTEXT
 * @param[out] data The decrypted data after unsealing. May be NULL
 * @param[out] size The size of data in bytes. May be NULL
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
 * @retval TSS2_FAPI_RC_SIGNATURE_VERIFICATION_FAILED if the signature could not
 *         be verified
 * @retval TSS2_ESYS_RC_* possible error codes of ESAPI.
 * @retval TSS2_FAPI_RC_NOT_PROVISIONED FAPI was not provisioned.
 * @retval TSS2_FAPI_RC_BAD_PATH if the path is used in inappropriate context
 *         or contains illegal characters.
 * @retval TSS2_FAPI_RC_AUTHORIZATION_UNKNOWN if a required authorization callback
 *         is not set.
 * @retval TSS2_FAPI_RC_AUTHORIZATION_FAILED if the authorization attempt fails.
 * @retval TSS2_FAPI_RC_POLICY_UNKNOWN if policy search for a certain policy digest
 *         was not successful.
 */
TSS2_RC
Fapi_Unseal_Finish(
    FAPI_CONTEXT *context,
    uint8_t     **data,
    size_t       *size)
{
    LOG_TRACE("called for context:%p", context);

    TSS2_RC r;
    ESYS_TR auth_session;

    /* Check for NULL parameters */
    check_not_null(context);

    /* Helpful alias pointers */
    IFAPI_Unseal * command = &context->cmd.Unseal;

    switch (context->state) {
        statecase(context->state, UNSEAL_WAIT_FOR_KEY);
            /* Load the key to be used for unsealing from the keystore. */
            r = ifapi_load_key(context, command->keyPath,
                               &command->object);
            return_try_again(r);
            goto_if_error(r, "Fapi load key.", error_cleanup);

            fallthrough;

        statecase(context->state, UNSEAL_AUTHORIZE_OBJECT);
            /* Authorize the session for use with with key. */
            r = ifapi_authorize_object(context, command->object, &auth_session);
            return_try_again(r);
            goto_if_error(r, "Authorize sealed object.", error_cleanup);

            /* Perform the unseal operation with the TPM. */
            r = Esys_Unseal_Async(context->esys, command->object->public.handle,
                    auth_session,
                    ESYS_TR_NONE, ESYS_TR_NONE);
            goto_if_error(r, "Error esys Unseal ", error_cleanup);

            fallthrough;

        statecase(context->state, UNSEAL_WAIT_FOR_UNSEAL);
            r = Esys_Unseal_Finish(context->esys, &command->unseal_data);
            return_try_again(r);
            goto_if_error(r, "Unseal_Finish", error_cleanup);

            /* Flush the used key from the TPM. */
            if (!command->object->misc.key.persistent_handle) {
                r = Esys_FlushContext_Async(context->esys, command->object->public.handle);
                goto_if_error(r, "Error Esys Flush ", error_cleanup);
            }

            fallthrough;

        statecase(context->state, UNSEAL_WAIT_FOR_FLUSH);
            if (!command->object->misc.key.persistent_handle) {
                r = Esys_FlushContext_Finish(context->esys);
                return_try_again(r);
                goto_if_error(r, "Unseal_Flush", error_cleanup);
            }

            fallthrough;

        statecase(context->state, UNSEAL_CLEANUP)
            /* Cleanup the session used for authentication. */
            r = ifapi_cleanup_session(context);
            try_again_or_error_goto(r, "Cleanup", error_cleanup);

            /* Return the data as requested by the caller.
               Duplicate the unseal_data as necessary. */
            if (size)
                *size = command->unseal_data->size;
            if (data) {
                *data = malloc(command->unseal_data->size);
                goto_if_null2(*data, "Out of memory", r, TSS2_FAPI_RC_MEMORY, error_cleanup);

                memcpy(*data, &command->unseal_data->buffer[0],
                       command->unseal_data->size);
            }
            SAFE_FREE(command->unseal_data);

            context->state = _FAPI_STATE_INIT;
            break;

        statecasedefault(context->state);
    }

error_cleanup:
    /* Cleanup any intermediate results and state stored in the context. */
    if (r)
        SAFE_FREE(command->unseal_data);
    ifapi_cleanup_ifapi_object(command->object);
    ifapi_cleanup_ifapi_object(&context->loadKey.auth_object);
    ifapi_cleanup_ifapi_object(context->loadKey.key_object);
    ifapi_cleanup_ifapi_object(&context->createPrimary.pkey_object);
    ifapi_session_clean(context);
    SAFE_FREE(command->keyPath);
    LOG_TRACE("finished");
    return r;
}
