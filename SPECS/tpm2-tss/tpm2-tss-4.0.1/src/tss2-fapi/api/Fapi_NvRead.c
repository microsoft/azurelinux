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
#include <unistd.h>
#include <errno.h>

#include "tss2_fapi.h"
#include "fapi_int.h"
#include "fapi_util.h"
#include "tss2_esys.h"
#define LOGMODULE fapi
#include "util/log.h"
#include "util/aux_util.h"

/** One-Call function for Fapi_NvRead
 *
 * Reads data from an NV index within the TPM.
 * The FAPI will automatically do the multiple reads if the NV index is larger
 * than the TPM's TPM2_MAX_NV_BUFFER_SIZE.
 *
 * @param[in,out] context The FAPI_CONTEXT
 * @param[in] nvPath The path of the NV index to read
 * @param[out] data The data that was read from the NV index
 * @param[out] size The size of data in bytes. May be NULL
 * @param[out] logData The log data of the NV index if the index is of type
 *             "extend". May be NULL
 *
 * @retval TSS2_RC_SUCCESS: if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE: if context, nvPath or data is NULL.
 * @retval TSS2_FAPI_RC_BAD_CONTEXT: if context corruption is detected.
 * @retval TSS2_FAPI_RC_BAD_PATH: if nvPath is not found.
 * @retval TSS2_FAPI_RC_AUTHORIZATION_FAILED: if authorization fails.
 * @retval TSS2_FAPI_RC_AUTHORIZATION_UNKNOWN: if don't know how to authenticate.
 * @retval TSS2_FAPI_RC_NV_NOT_READABLE: if the NV is not a readable index.
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
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_TRY_AGAIN if an I/O operation is not finished yet and
 *         this function needs to be called again.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE if an internal error occurred.
 * @retval TSS2_FAPI_RC_POLICY_UNKNOWN if policy search for a certain policy digest
 *         was not successful.
 * @retval TSS2_ESYS_RC_* possible error codes of ESAPI.
 * @retval TSS2_FAPI_RC_NOT_PROVISIONED FAPI was not provisioned.
 */
TSS2_RC
Fapi_NvRead(
    FAPI_CONTEXT   *context,
    char     const *nvPath,
    uint8_t       **data,
    size_t         *size,
    char          **logData)
{
    LOG_TRACE("called for context:%p", context);

    TSS2_RC r, r2;

    /* Check for NULL parameters */
    check_not_null(context);
    check_not_null(nvPath);
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

    r = Fapi_NvRead_Async(context, nvPath);
    return_if_error_reset_state(r, "NV_Read");

    do {
        /* We wait for file I/O to be ready if the FAPI state automata
           are in a file I/O state. */
        r = ifapi_io_poll(&context->io);
        return_if_error(r, "Something went wrong with IO polling");

        /* Repeatedly call the finish function, until FAPI has transitioned
           through all execution stages / states of this invocation. */
        r = Fapi_NvRead_Finish(context, data, size, logData);
    } while (base_rc(r) == TSS2_BASE_RC_TRY_AGAIN);

    /* Reset the ESYS timeout to non-blocking, immediate response. */
    r2 = Esys_SetTimeout(context->esys, 0);
    return_if_error(r2, "Set Timeout to non-blocking");

    return_if_error_reset_state(r, "NV_Read");

    LOG_TRACE("finished");
    return TSS2_RC_SUCCESS;
}

/** Asynchronous function for Fapi_NvRead
 *
 * Reads data from an NV index within the TPM.
 * The FAPI will automatically do the multiple reads if the NV index is larger
 * than the TPM's TPM2_MAX_NV_BUFFER_SIZE.
 *
 * Call Fapi_NvRead_Finish to finish the execution of this command.
 *
 * @param[in,out] context The FAPI_CONTEXT
 * @param[in] nvPath The path of the NV index to read
 *
 * @retval TSS2_RC_SUCCESS: if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE: if context or nvPath is NULL. *
 * @retval TSS2_FAPI_RC_BAD_CONTEXT: if context corruption is detected.
 * @retval TSS2_FAPI_RC_BAD_PATH: if nvPath is not found.
 * @retval TSS2_FAPI_RC_AUTHORIZATION_FAILED: if authorization fails.
 * @retval TSS2_FAPI_RC_AUTHORIZATION_UNKNOWN: if don't know how to authenticate.
 * @retval TSS2_FAPI_RC_NV_NOT_READABLE: if the NV is not a readable index.
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
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_NOT_PROVISIONED FAPI was not provisioned.
 */
TSS2_RC
Fapi_NvRead_Async(
    FAPI_CONTEXT   *context,
    char     const *nvPath)
{
    LOG_TRACE("called for context:%p", context);
    LOG_TRACE("nvPath: %s", nvPath);

    TSS2_RC r;

    /* Check for NULL parameters */
    check_not_null(context);
    check_not_null(nvPath);

    /* Helpful alias pointers */
    IFAPI_NV_Cmds * command = &context->nv_cmd;

    /* Reset all context-internal session state information. */
    r = ifapi_session_init(context);
    return_if_error(r, "Initialize NvRead");

    memset(command, 0, sizeof(IFAPI_NV_Cmds));

    /* Copy parameters to context for use during _Finish. */
    strdup_check(command->nvPath, nvPath, r, error_cleanup);

    /* Load the NV index metadata from keystore. */
    r = ifapi_keystore_load_async(&context->keystore, &context->io, command->nvPath);
    goto_if_error_reset_state(r, "Could not open: %s", error_cleanup, command->nvPath);

    /* Initialize the context state for this operation. */
    context->state = NV_READ_READ;
    LOG_TRACE("finished");
    return TSS2_RC_SUCCESS;

error_cleanup:
    /* Cleanup duplicated input parameters that were copied before. */
    SAFE_FREE(command->nvPath);
    return r;
}

/** Asynchronous finish function for Fapi_NvRead
 *
 * This function should be called after a previous Fapi_NvRead_Async.
 *
 * @param[in,out] context The FAPI_CONTEXT
 * @param[out] data The data that was read from the NV index
 * @param[out] size The size of data in bytes. May be NULL
 * @param[out] logData The log data of the NV index if the index is of type
 *			   "extend". May be NULL
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
 * @retval TSS2_FAPI_RC_BAD_PATH if a path is used in inappropriate context
 *         or contains illegal characters.
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
 */
TSS2_RC
Fapi_NvRead_Finish(
    FAPI_CONTEXT   *context,
    uint8_t       **data,
    size_t         *size,
    char          **logData)
{
    LOG_TRACE("called for context:%p", context);

    TSS2_RC r;
    ESYS_TR authIndex;
    size_t readSize;

    /* Check for NULL parameters */
    check_not_null(context);
    check_not_null(data);

    /* Helpful alias pointers */
    IFAPI_NV_Cmds *command = &context->nv_cmd;
    IFAPI_OBJECT *object = &command->nv_object;
    IFAPI_OBJECT *authObject = &command->auth_object;

    switch (context->state) {
    statecase(context->state, NV_READ_READ)
        r = ifapi_keystore_load_finish(&context->keystore, &context->io, object);
        return_try_again(r);
        return_if_error_reset_state(r, "read_finish failed");

        if (object->objectType != IFAPI_NV_OBJ)
            goto_error(r, TSS2_FAPI_RC_BAD_PATH, "%s is no NV object.", error_cleanup,
                       command->nvPath);

        /* Initialize the NV index object for use with ESYS. */
        r = ifapi_initialize_object(context->esys, object);
        goto_if_error_reset_state(r, "Initialize NV object", error_cleanup);

        command->esys_handle = object->public.handle;
        command->nv_obj = object->misc.nv;
        command->size = object->misc.nv.public.nvPublic.dataSize;
        command->numBytes = object->misc.nv.public.nvPublic.dataSize;

        /* Determine auth object */
        if (object->misc.nv.public.nvPublic.attributes & TPMA_NV_PPREAD) {
            ifapi_init_hierarchy_object(authObject, ESYS_TR_RH_PLATFORM);
            authIndex = ESYS_TR_RH_PLATFORM;
        } else {
            if (object->misc.nv.public.nvPublic.attributes & TPMA_NV_OWNERREAD) {
                ifapi_init_hierarchy_object(authObject, ESYS_TR_RH_OWNER);
                authIndex = ESYS_TR_RH_OWNER;
            } else {
                authIndex = object->public.handle;
            }
            *authObject = *object;
        }
        command->auth_index = authIndex;
        context->primary_state = PRIMARY_INIT;

        /* Prepare session for authorization and data encryption. */
        r = ifapi_get_sessions_async(context,
                                     IFAPI_SESSION_GENEK | IFAPI_SESSION1,
                                     TPMA_SESSION_ENCRYPT, 0);
        goto_if_error_reset_state(r, "Create sessions", error_cleanup);

        fallthrough;

    statecase(context->state, NV_READ_WAIT_FOR_SESSION)
        r = ifapi_get_sessions_finish(context, &context->profiles.default_profile,
                                      object->misc.nv.public.nvPublic.nameAlg);
        return_try_again(r);
        goto_if_error_reset_state(r, " FAPI create session", error_cleanup);

        command->nv_read_state = NV_READ_INIT;

        fallthrough;

    statecase(context->state, NV_READ_WAIT)
        if (data) {
            /* Read the data from the TPM. */
            r = ifapi_nv_read(context, &command->rdata, &readSize);
            return_try_again(r);

            goto_if_error_reset_state(r, " FAPI NV_Read", error_cleanup);
        }

        if (logData) {
            /* Duplicate the logdata that may have been stored during a
               NvExtend command. */
            if (object->misc.nv.event_log) {
                strdup_check(command->logData, object->misc.nv.event_log, r, error_cleanup);
            } else {
               strdup_check(command->logData, "", r, error_cleanup);
            }
        }
        fallthrough;

    statecase(context->state, NV_READ_CLEANUP)
        /* Cleanup the session used for authorization. */
        r = ifapi_cleanup_session(context);
        try_again_or_error_goto(r, "Cleanup", error_cleanup);

        if (logData)
            *logData = command->logData;
        *data = command->rdata;
        if (size)
            *size = command->size;
        context->state = _FAPI_STATE_INIT;
        break;

    statecasedefault(context->state);
    }

error_cleanup:
    /* Cleanup any intermediate results and state stored in the context. */
    ifapi_cleanup_ifapi_object(&command->nv_object);
    ifapi_cleanup_ifapi_object(&context->loadKey.auth_object);
    ifapi_cleanup_ifapi_object(context->loadKey.key_object);
    ifapi_cleanup_ifapi_object(&context->createPrimary.pkey_object);
    SAFE_FREE(command->nvPath);
    //SAFE_FREE(context->nv_cmd.tes);
    ifapi_session_clean(context);
    LOG_TRACE("finished");
    return r;
}
