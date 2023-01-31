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
#include "ifapi_json_serialize.h"
#include "ifapi_json_deserialize.h"
#define LOGMODULE fapi
#include "util/log.h"
#include "util/aux_util.h"
#include "tss2_mu.h"

/** One-Call function for Fapi_GetEsysBlob
 *
 * Gets blobs of FAPI objects which can be used to create ESAPI objects.
 * The ESAPI objects can be created with the functions:
 * - Esys_TR_Deserialize for type == FAPI_ESYSBLOB_DESERIALIZE
 * - Tss2_MU_TPMS_CONTEXT_Unmarshal and Esys_ContextLoad for
 *   type == FAPI_ESYSBLOB_CONTEXTLOAD
 *
 * @param[in,out] context The FAPI_CONTEXT
 * @param[in] path The path of the FAPI object.
 * @param[out] type The type of the returned blob.
 *             FAPI_ESYSBLOB_CONTEXTLOAD if a context blob is returned.
 *             FAPI_ESYSBLOB_DESERIALIZE if a serialzed blob is returned.
 * @param[out] data The binary blob which can be used to create a ESAPI object.
 * @param[out] length The size of the binary blob.
 * @retval TSS2_RC_SUCCESS: if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE: if context or path is NULL.
 * @retval TSS2_FAPI_RC_BAD_CONTEXT: if context corruption is detected.
 * @retval TSS2_FAPI_RC_BAD_PATH: if path does not map to a FAPI entity.
 * @retval TSS2_FAPI_RC_NOT_DELETABLE: if the entity is not deletable or the
 *         path is read-only.
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
 * @retval TSS2_FAPI_RC_AUTHORIZATION_UNKNOWN if a required authorization callback
 *         is not set.
 * @retval TSS2_FAPI_RC_AUTHORIZATION_FAILED if the authorization attempt fails.
 * @retval TSS2_FAPI_RC_POLICY_UNKNOWN if policy search for a certain policy digest
 *         was not successful.
 * @retval TSS2_ESYS_RC_* possible error codes of ESAPI.
 * @retval TSS2_FAPI_RC_NOT_PROVISIONED FAPI was not provisioned.
 */
TSS2_RC
Fapi_GetEsysBlob(
    FAPI_CONTEXT   *context,
    char     const *path,
    uint8_t        *type,
    uint8_t       **data,
    size_t         *length)
{
    LOG_TRACE("called for context:%p", context);

    TSS2_RC r;

    /* Check for NULL parameters */
    check_not_null(context);
    check_not_null(path);

    r = Fapi_GetEsysBlob_Async(context, path);
    return_if_error_reset_state(r, "Entity_GetEsysBlob");

    do {
        /* We wait for file I/O to be ready if the FAPI state automata
           are in a file I/O state. */
        r = ifapi_io_poll(&context->io);
        return_if_error(r, "Something went wrong with IO polling");

        /* Repeatedly call the finish function, until FAPI has transitioned
           through all execution stages / states of this invocation. */
        r = Fapi_GetEsysBlob_Finish(context, type, data, length);
    } while (base_rc(r) == TSS2_BASE_RC_TRY_AGAIN);

    return_if_error_reset_state(r, "Entity_GetEsysBlob");

    return TSS2_RC_SUCCESS;
}

/** Asynchronous function for Fapi_GetEsysBlob
 *
 * Prepares the reading of the blobs from keystore or TPM.
 * Call Fapi_GetEsysBlob_Finish to finish the execution of this command.
 *
 * @param[in,out] context The ESAPI_CONTEXT
 * @param[in] path The path of the FAPI object.
 *
 * @retval TSS2_RC_SUCCESS: if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE: if context or path is NULL.
 * @retval TSS2_FAPI_RC_BAD_CONTEXT: if context corruption is detected.
 * @retval TSS2_FAPI_RC_BAD_PATH: if path does not map to a FAPI entity.
 * @retval TSS2_FAPI_RC_NOT_DELETABLE: if the entity is not deletable or the
 *         path is read-only.
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
 * @retval TSS2_ESYS_RC_* possible error codes of ESAPI.
 */
TSS2_RC
Fapi_GetEsysBlob_Async(
    FAPI_CONTEXT   *context,
    char     const *path)
{
    LOG_TRACE("called for context:%p", context);
    LOG_TRACE("path: %s", path);

    TSS2_RC r;

    /* Check for NULL parameters */
    check_not_null(context);
    check_not_null(path);

    /* Helpful alias pointers */
    IFAPI_GetEsysBlob * command = &(context->cmd.GetEsysBlob);
    IFAPI_OBJECT *object = &command->object;
    IFAPI_OBJECT *authObject = &command->auth_object;

    /* Copy parameters to context for use during _Finish. */
    strdup_check(command->path, path, r, error_cleanup);

    object->objectType = IFAPI_OBJ_NONE;
    authObject->objectType = IFAPI_OBJ_NONE;

    /* Check whether TCTI and ESYS are initialized */
    goto_if_null(context->esys, "Command can't be executed in none TPM mode.",
                   TSS2_FAPI_RC_NO_TPM, error_cleanup);

    /* If the async state automata of FAPI shall be tested, then we must not set
       the timeouts of ESYS to blocking mode.
       During testing, the mssim tcti will ensure multiple re-invocations.
       Usually however the synchronous invocations of FAPI shall instruct ESYS
       to block until a result is available. */
#ifndef TEST_FAPI_ASYNC
    r = Esys_SetTimeout(context->esys, TSS2_TCTI_TIMEOUT_BLOCK);
    goto_if_error_reset_state(r, "Set Timeout to blocking", error_cleanup);
#endif /* TEST_FAPI_ASYNC */

    /* A TPM session will be created to enable object authorization */
    r = ifapi_session_init(context);
    goto_if_error(r, "Initialize GetEsysBlob", error_cleanup);

    context->state = GET_ESYS_BLOB_GET_FILE;

    LOG_TRACE("finished");
    return TSS2_RC_SUCCESS;

error_cleanup:
    /* Cleanup any intermediate results and state stored in the context. */
    SAFE_FREE(command->path);
    if (Esys_FlushContext(context->esys, context->session1) != TSS2_RC_SUCCESS) {
        LOG_ERROR("Cleanup session failed.");
    }
    return r;
}

/** Asynchronous finish function for Fapi_GetEsysBlob
 *
 * This function should be called after a previous Fapi_GetEsysBlob_Async.
 *
 * @param[in,out] context The FAPI_CONTEXT
 * @param[out] type The type of the returned blob.

 * @param[out] data The binary blob which can be used to create a ESAPI object.
 * @param[out] length The size of the binary blob.
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
Fapi_GetEsysBlob_Finish(
    FAPI_CONTEXT   *context,
    uint8_t        *type,
    uint8_t       **data,
    size_t         *length)
{
    LOG_TRACE("called for context:%p", context);

    TSS2_RC r;
    char *path;
    TPMS_CONTEXT *key_context = NULL;
    size_t offset = 0;

    /* Check for NULL parameters */
    check_not_null(context);
    check_not_null(data);
    *data = NULL;

    /* Helpful alias pointers */
    IFAPI_GetEsysBlob * command = &(context->cmd.GetEsysBlob);
    IFAPI_OBJECT *object = &command->object;
    IFAPI_OBJECT *key_object = context->loadKey.key_object;
    IFAPI_OBJECT *authObject = &context->loadKey.auth_object;

    switch (context->state) {
        statecase(context->state, GET_ESYS_BLOB_GET_FILE);
            path = command->path;
            LOG_TRACE("GetEsysBlob object: %s", path);

            /* Prepare loading the object metadata from the keystore. */
            r = ifapi_keystore_load_async(&context->keystore, &context->io, path);
            return_if_error2(r, "Could not open: %s", path);

            fallthrough;

        statecase(context->state, GET_ESYS_BLOB_READ);
            /* Get object metadata from keystore. */
            r = ifapi_keystore_load_finish(&context->keystore, &context->io, object);
            return_try_again(r);
            return_if_error_reset_state(r, "read_finish failed");

            /* Initialize the ESYS object for the key or NV Index. */
            r = ifapi_initialize_object(context->esys, object);
            goto_if_error_reset_state(r, "Initialize NV object", error_cleanup);

            if (object->objectType == IFAPI_KEY_OBJ) {
                /* If the object is a key, we jump over to GET_ESYS_BLOB_KEY. */
                command->is_key = true;
                context->state = GET_ESYS_BLOB_KEY;
                return TSS2_FAPI_RC_TRY_AGAIN;

            } else  if (object->objectType != IFAPI_NV_OBJ) {
                goto_error(r, TSS2_FAPI_RC_BAD_VALUE, "Key or NV object expected.",
                           error_cleanup);
            }
            *type = FAPI_ESYSBLOB_DESERIALIZE;
            fallthrough;

        statecase(context->state, GET_ESYS_BLOB_SERIALIZE);
            r = Esys_TR_Serialize(context->esys, object->public.handle, data, length);
            goto_if_error(r, "Serialize object", error_cleanup);

            context->state = _FAPI_STATE_INIT;
            LOG_DEBUG("success");
            r = TSS2_RC_SUCCESS;
            break;

        statecase(context->state, GET_ESYS_BLOB_KEY);
            if (object->misc.key.persistent_handle) {
                *type = FAPI_ESYSBLOB_DESERIALIZE;
                context->state = GET_ESYS_BLOB_SERIALIZE;
                return TSS2_FAPI_RC_TRY_AGAIN;
            }
            fallthrough;

        statecase(context->state, GET_ESYS_BLOB_WAIT_FOR_KEY);
            /* Loading the key is needed for blob computation. */
            r = ifapi_load_key(context, command->path, &key_object);
            return_try_again(r);
            goto_if_error(r, "Fapi load key.", error_cleanup);

            command->type = FAPI_ESYSBLOB_CONTEXTLOAD;

            /* Prepare the saving of the context. */
            r = Esys_ContextSave_Async(context->esys, key_object->public.handle);
            goto_if_error(r, "Error esys context save", error_cleanup);

            fallthrough;

        statecase(context->state, GET_ESYS_BLOB_WAIT_FOR_CONTEXT_SAVE);
            /* Save and get the context. */
            r = Esys_ContextSave_Finish(context->esys, &key_context);
            return_try_again(r);
            goto_if_error(r, "Error esys context save", error_cleanup);

            command->length = 0;
            r = Tss2_MU_TPMS_CONTEXT_Marshal(key_context, NULL, SIZE_MAX,
                                             &command->length);
            goto_if_error(r, "Marshaling context", error_cleanup);

            command->data = malloc(command->length);
            goto_if_null2(command->data, "Out of memory", r, TSS2_FAPI_RC_MEMORY,
                          error_cleanup);

            r = Tss2_MU_TPMS_CONTEXT_Marshal(key_context, command->data, command->length,
                                             &offset);
            SAFE_FREE(key_context);
            goto_if_error(r, "Marshaling context", error_cleanup);

            /* Cleanup policy session if an error did occur. */
            ifapi_flush_policy_session(context, context->policy.session, r);
            goto_if_error(r, "Cleanup policy session", error_cleanup);

            /* Flush current object used for blob computation. */
            if (!key_object->misc.key.persistent_handle) {
                r = Esys_FlushContext_Async(context->esys, key_object->public.handle);
                goto_if_error(r, "Flush Context", error_cleanup);
            }

            fallthrough;

        statecase(context->state, GET_ESYS_BLOB_WAIT_FOR_FLUSH);
            if (!key_object->misc.key.persistent_handle) {
                r = Esys_FlushContext_Finish(context->esys);
                return_try_again(r);
                goto_if_error(r, "Flush Context", error_cleanup);
            }

            fallthrough;

        statecase(context->state, GET_ESYS_BLOB_CLEANUP)
            /* Cleanup the session used for authorization. */
            r = ifapi_cleanup_session(context);
            try_again_or_error_goto(r, "Cleanup", error_cleanup);
            *type = command->type;
            *data = command->data;
            *length = command->length;

            context->state = _FAPI_STATE_INIT;
            break;

        statecasedefault(context->state);
    }

    /* Reset the ESYS timeout to non-blocking, immediate response. */
    if (context->esys) {
        r = Esys_SetTimeout(context->esys, 0);
        goto_if_error(r, "Set Timeout to non-blocking", error_cleanup);
    }

    /* Cleanup intermediate state stored in the context. */
    SAFE_FREE(command->path);
    ifapi_cleanup_ifapi_object(authObject);
    ifapi_cleanup_ifapi_object(object);
    ifapi_cleanup_ifapi_object(key_object);
    ifapi_session_clean(context);
    ifapi_cleanup_ifapi_object(&context->loadKey.auth_object);
    ifapi_cleanup_ifapi_object(context->loadKey.key_object);
    ifapi_cleanup_ifapi_object(&context->createPrimary.pkey_object);

    LOG_TRACE("finished");
    return r;

error_cleanup:
    /* Cleanup any intermediate results and state stored in the context. */
    Esys_SetTimeout(context->esys, 0);
    ifapi_cleanup_ifapi_object(authObject);
    ifapi_cleanup_ifapi_object(object);
    ifapi_cleanup_ifapi_object(key_object);
    SAFE_FREE(command->path);
    SAFE_FREE(command->data);
    SAFE_FREE(key_context);
    ifapi_session_clean(context);
    ifapi_cleanup_ifapi_object(&context->loadKey.auth_object);
    ifapi_cleanup_ifapi_object(context->loadKey.key_object);
    ifapi_cleanup_ifapi_object(&context->createPrimary.pkey_object);
    return r;
}
