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

/** One-Call function for Fapi_CreateSeal
 *
 * Creates a sealed object and stores it in the FAPI metadata store. If no data
 * is provided, the TPM generates random data to fill the sealed object.
 *
 * @param[in,out] context The FAPI_CONTEXT
 * @param[in] path The path to the new sealed object
 * @param[in] type The type of the new sealed object. May be NULL
 * @param[in] size The size of the new sealed object. Must not be 0
 * @param[in] policyPath The path to the policy that is associated with the new
 *            sealed object. May be NULL
 * @param[in] authValue The authorization value for the new sealed object. May
 *            be NULL
 * @param[in] data The data that is to be sealed within the new object. May be
 *            NULL
 *
 * @retval TSS2_RC_SUCCESS: if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE: if context, or path is NULL.
 * @retval TSS2_FAPI_RC_BAD_CONTEXT: if context corruption is detected.
 * @retval TSS2_FAPI_RC_KEY_NOT_FOUND: if the parent key does not map to a
 *         FAPI key.
 * @retval TSS2_FAPI_RC_BAD_PATH: if policyPath is non-NULL and does not map to
 *         a FAPI key.
 * @retval TSS2_FAPI_RC_PATH_ALREADY_EXISTS: if a sealed object already exists
 *         at path.
 * @retval TSS2_FAPI_RC_BAD_VALUE: if the keyType is invalid.
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
 * @retval TSS2_ESYS_RC_* possible error codes of ESAPI.
 * @retval TSS2_FAPI_RC_PATH_NOT_FOUND if a FAPI object path was not found
 *         during authorization.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE if an internal error occured.
 * @retval TSS2_FAPI_RC_NOT_PROVISIONED FAPI was not provisioned.
 * @retval TSS2_FAPI_RC_AUTHORIZATION_FAILED if the authorization attempt fails.
 * @retval TSS2_FAPI_RC_POLICY_UNKNOWN if policy search for a certain policy digest
 *         was not successful.
 */
TSS2_RC
Fapi_CreateSeal(
    FAPI_CONTEXT *context,
    char    const *path,
    char    const *type,
    size_t         size,
    char    const *policyPath,
    char    const *authValue,
    uint8_t const *data)
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

    r = Fapi_CreateSeal_Async(context, path, type, size, policyPath,
                              authValue, data);
    return_if_error_reset_state(r, "CreateSeal");

    do {
        /* We wait for file I/O to be ready if the FAPI state automata
           are in a file I/O state. */
        r = ifapi_io_poll(&context->io);
        return_if_error(r, "Something went wrong with IO polling");

        /* Repeatedly call the finish function, until FAPI has transitioned
           through all execution stages / states of this invocation. */
        r = Fapi_CreateSeal_Finish(context);
    } while (base_rc(r) == TSS2_BASE_RC_TRY_AGAIN);

    /* Reset the ESYS timeout to non-blocking, immediate response. */
    r2 = Esys_SetTimeout(context->esys, 0);
    return_if_error(r2, "Set Timeout to non-blocking");

    return_if_error_reset_state(r, "CreateSeal");

    LOG_TRACE("finished");
    return TSS2_RC_SUCCESS;
}

/** Asynchronous function for Fapi_CreateSeal
 *
 * Creates a sealed object and stores it in the FAPI metadata store. If no data
 * is provided, the TPM generates random data to fill the sealed object.
 *
 * Call Fapi_CreateSeal_Finish to finish the execution of this command.
 *
 * @param[in,out] context The FAPI_CONTEXT
 * @param[in] path The path to the new sealed object
 * @param[in] type The type of the new sealed object. May be NULL
 * @param[in] size The size of the new sealed object. Must not be 0
 * @param[in] policyPath The path to the policy that is associated with the new
 *            sealed object. May be NULL
 * @param[in] authValue The authorization value for the new sealed object. May
 *            be NULL
 * @param[in] data The data that is to be sealed within the new object. May be
 *            NULL
 *
 * @retval TSS2_RC_SUCCESS: if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE: if context, or path is NULL.
 * @retval TSS2_FAPI_RC_BAD_CONTEXT: if context corruption is detected.
 * @retval TSS2_FAPI_RC_KEY_NOT_FOUND: if the parent key does not map to a
 *         FAPI key.
 * @retval TSS2_FAPI_RC_BAD_PATH: if policyPath is non-NULL and does not map to
 *         a FAPI key.
 * @retval TSS2_FAPI_RC_PATH_ALREADY_EXISTS: if a sealed object already exists
 *         at path.
 * @retval TSS2_FAPI_RC_BAD_VALUE: if the keyType is invalid.
 * @retval TSS2_FAPI_RC_BAD_SEQUENCE: if the context has an asynchronous
 *         operation already pending.
 * @retval TSS2_FAPI_RC_IO_ERROR: if the data cannot be saved.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory for
 *         internal operations or return parameters.
 * @retval TSS2_FAPI_RC_NO_TPM if FAPI was initialized in no-TPM-mode via its
 *         config file.
 * @retval TSS2_FAPI_RC_PATH_NOT_FOUND if a FAPI object path was not found
 *         during authorization.
 */
TSS2_RC
Fapi_CreateSeal_Async(
    FAPI_CONTEXT *context,
    char    const *path,
    char    const *type,
    size_t         size,
    char    const *policyPath,
    char    const *authValue,
    uint8_t const *data)
{
    LOG_TRACE("called for context:%p", context);
    LOG_TRACE("path: %s", path);
    LOG_TRACE("type: %s", type);
    LOG_TRACE("size: %zi", size);
    LOG_TRACE("policyPath: %s", policyPath);
    LOG_TRACE("authValue: %s", authValue);

    TSS2_RC r;

    /* Check for NULL parameters */
    check_not_null(context);
    check_not_null(path);

    /* Reset all context-internal session state information. */
    r = ifapi_session_init(context);
    return_if_error(r, "Initialize CreateSeal");

    /* Copy parameters to context for use during _Finish. */
    memset(&context->cmd.Key_Create.public_templ, 0, sizeof(IFAPI_KEY_TEMPLATE));
    r = ifapi_key_create_prepare_sensitive(context, path, policyPath, size,
                                           authValue, data);
    return_if_error(r, "Key create.");

    /* Set the flags of the NV index to be created. If no type is given the empty-string
       default type flags are set. */
    r = ifapi_set_key_flags(type ? type : "",
                            (policyPath && strcmp(policyPath, "") != 0) ? true : false,
                            &context->cmd.Key_Create.public_templ);
    return_if_error(r, "Set key flags for key");

    context->cmd.Key_Create.public_templ.public.publicArea.objectAttributes  &=
        ~TPMA_OBJECT_SENSITIVEDATAORIGIN;

    /* Initialize the context state for this operation. */
    context->state = CREATE_SEAL;

    LOG_TRACE("finished");
    return TSS2_RC_SUCCESS;
}

/** Asynchronous finish function for Fapi_CreateSeal
 *
 * This function should be called after a previous Fapi_CreateSeal.
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
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_AUTHORIZATION_UNKNOWN if a required authorization callback
 *         is not set.
 * @retval TSS2_ESYS_RC_* possible error codes of ESAPI.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE if an internal error occured.
 * @retval TSS2_FAPI_RC_NOT_PROVISIONED FAPI was not provisioned.
 * @retval TSS2_FAPI_RC_KEY_NOT_FOUND if a key was not found.
 * @retval TSS2_FAPI_RC_BAD_PATH if the path is used in inappropriate context
 *         or contains illegal characters.
 * @retval TSS2_FAPI_RC_PATH_NOT_FOUND if a FAPI object path was not found
 *         during authorization.
 * @retval TSS2_FAPI_RC_AUTHORIZATION_FAILED if the authorization attempt fails.
 * @retval TSS2_FAPI_RC_POLICY_UNKNOWN if policy search for a certain policy digest
 *         was not successful.
 * @retval TSS2_FAPI_RC_PATH_ALREADY_EXISTS if the object already exists in object store.
 */
TSS2_RC
Fapi_CreateSeal_Finish(
    FAPI_CONTEXT *context)
{
    LOG_TRACE("called for context:%p", context);

    TSS2_RC r;

    /* Check for NULL parameters */
    check_not_null(context);

    switch (context->state) {
        statecase(context->state, CREATE_SEAL);
            /* Create the seal object. A seal object internally is a so-called
               KEYED_HASH object and created in the same way as a regular key.
               Thus the function name ifapi_key_create(). */
            r = ifapi_key_create(context, &context->cmd.Key_Create.public_templ);
            return_try_again(r);
            goto_if_error(r, "Key create", error_cleanup);
            break;

        statecasedefault(context->state);
    }

error_cleanup:
   /* Cleanup any intermediate results and state stored in the context. */
    ifapi_cleanup_ifapi_object(&context->createPrimary.pkey_object);
    ifapi_cleanup_ifapi_object(context->loadKey.key_object);
    ifapi_cleanup_ifapi_object(&context->loadKey.auth_object);
    context->state = _FAPI_STATE_INIT;
    LOG_TRACE("finished");
    return r;
}
