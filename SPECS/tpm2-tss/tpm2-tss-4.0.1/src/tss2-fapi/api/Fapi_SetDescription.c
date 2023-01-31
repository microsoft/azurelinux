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
#include "tss2_esys.h"
#define LOGMODULE fapi
#include "util/log.h"
#include "util/aux_util.h"

/** One-Call function for Fapi_SetDescription
 *
 * Associates a human readable description with an object in the metadata store.
 *
 * @param[in,out] context The FAPI_CONTEXT
 * @param[in] path The path of the object in the metadata store
 * @param[in] description The description that is associated with the object.
 *            May be NULL
 *
 * @retval TSS2_RC_SUCCESS: if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE: if context or path is NULL.
 * @retval TSS2_FAPI_RC_BAD_CONTEXT: if context corruption is detected.
 * @retval TSS2_FAPI_RC_BAD_PATH: if path does not map to a FAPI entity.
 * @retval TSS2_FAPI_RC_BAD_SEQUENCE: if the context has an asynchronous
 *         operation already pending.
 * @retval TSS2_FAPI_RC_IO_ERROR: if the data cannot be saved.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory for
 *         internal operations or return parameters.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_PATH_NOT_FOUND if a FAPI object path was not found
 *         during authorization.
 * @retval TSS2_FAPI_RC_KEY_NOT_FOUND if a key was not found.
 * @retval TSS2_FAPI_RC_TRY_AGAIN if an I/O operation is not finished yet and
 *         this function needs to be called again.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE if an internal error occurred.
 * @retval TSS2_FAPI_RC_NOT_PROVISIONED FAPI was not provisioned.
 */
TSS2_RC
Fapi_SetDescription(
    FAPI_CONTEXT *context,
    char   const *path,
    char   const *description)
{
    LOG_TRACE("called for context:%p", context);

    TSS2_RC r;

    /* Check for NULL parameters */
    check_not_null(context);
    check_not_null(path);

    r = Fapi_SetDescription_Async(context, path, description);
    return_if_error_reset_state(r, "Path_SetDescription");

    do {
        /* We wait for file I/O to be ready if the FAPI state automata
           are in a file I/O state. */
        r = ifapi_io_poll(&context->io);
        return_if_error(r, "Something went wrong with IO polling");

        /* Repeatedly call the finish function, until FAPI has transitioned
           through all execution stages / states of this invocation. */
        r = Fapi_SetDescription_Finish(context);
    } while (base_rc(r) == TSS2_BASE_RC_TRY_AGAIN);

    return_if_error_reset_state(r, "Path_SetDescription");

    LOG_TRACE("finished");
    return TSS2_RC_SUCCESS;
}

/** Asynchronous function for Fapi_SetDescription
 *
 * Associates a human readable description with an object in the metadata store.
 *
 * Call Fapi_SetDescription_Finish to finish the execution of this command.
 *
 * @param[in,out] context The FAPI_CONTEXT
 * @param[in] path The path of the object in the metadata store
 * @param[in] description The description that is associated with the object.
 *            May be NULL
 *
 * @retval TSS2_RC_SUCCESS: if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE: if context or path is NULL.
 * @retval TSS2_FAPI_RC_BAD_CONTEXT: if context corruption is detected.
 * @retval TSS2_FAPI_RC_BAD_PATH: if path does not map to a FAPI entity.
 * @retval TSS2_FAPI_RC_BAD_SEQUENCE: if the context has an asynchronous
 *         operation already pending.
 * @retval TSS2_FAPI_RC_IO_ERROR: if the data cannot be saved.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory for
 *         internal operations or return parameters.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_PATH_NOT_FOUND if a FAPI object path was not found
 *         during authorization.
 * @retval TSS2_FAPI_RC_KEY_NOT_FOUND if a key was not found.
 * @retval TSS2_FAPI_RC_NOT_PROVISIONED FAPI was not provisioned.
 */
TSS2_RC
Fapi_SetDescription_Async(
    FAPI_CONTEXT *context,
    char   const *path,
    char   const *description)
{
    LOG_TRACE("called for context:%p", context);
    LOG_TRACE("path: %s", path);
    LOG_TRACE("description: %s", description);

    TSS2_RC r;

    /* Check for NULL parameters */
    check_not_null(context);
    check_not_null(path);

    /* Check for invalid parameters */
    if (description && strlen(description) + 1 > 1024) {
        return_error(TSS2_FAPI_RC_BAD_VALUE,
                     "Length of description > 1024");
    }

    /* Helpful alias pointers */
    IFAPI_Path_SetDescription * command = &context->cmd.path_set_info;

    /* Copy parameters to context for use during _Finish. */
    strdup_check(command->object_path, path, r, error_cleanup);

    /* Load the object's current metadata from the keystore. */
    r = ifapi_keystore_load_async(&context->keystore, &context->io, path);
    goto_if_error2(r, "Could not open: %s", error_cleanup, path);

    if (description == NULL) {
        command->description = NULL;
    } else {
        strdup_check(command->description, description, r, error_cleanup);
    }


    /* Initialize the context state for this operation. */
    context->state = PATH_SET_DESCRIPTION_READ;
    LOG_TRACE("finished");
    return TSS2_RC_SUCCESS;

error_cleanup:
    /* Cleanup duplicated input parameters that were copied before. */
    SAFE_FREE(command->object_path);
    SAFE_FREE(command->description);
    return r;
}

/** Asynchronous finish function for Fapi_SetDescription
 *
 * This function should be called after a previous Fapi_SetDescription_Async.
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
 * @retval TSS2_FAPI_RC_PATH_NOT_FOUND If no file is found after pathname expansion.
 * @retval TSS2_FAPI_RC_TRY_AGAIN: if the asynchronous operation is not yet
 *         complete. Call this function again later.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE if an internal error occurred.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_BAD_PATH if the path is used in inappropriate context
 *         or contains illegal characters.
 */
TSS2_RC
Fapi_SetDescription_Finish(
    FAPI_CONTEXT *context)
{
    LOG_TRACE("called for context:%p", context);

    TSS2_RC r;

    /* Check for NULL parameters */
    check_not_null(context);

    /* Helpful alias pointers */
    IFAPI_Path_SetDescription * command = &context->cmd.path_set_info;
    IFAPI_OBJECT *object = &command->object;

    switch (context->state) {
        statecase(context->state, PATH_SET_DESCRIPTION_READ);
            r = ifapi_keystore_load_finish(&context->keystore, &context->io, object);
            return_try_again(r);
            goto_if_error_reset_state(r, "read_finish failed", error_cleanup);

            r = ifapi_initialize_object(context->esys, object);
            goto_if_error_reset_state(r, "Initialize key object", error_cleanup);

            /* Add new description to object and save object */
            ifapi_set_description(object, command->description);

            /* Store the updated metadata back to the keystore. */
            r = ifapi_keystore_store_async(&context->keystore, &context->io,
                                           command->object_path, object);
            goto_if_error_reset_state(r, "Could not open: %sh", error_cleanup,
                                      command->object_path);

            fallthrough;

        statecase(context->state, PATH_SET_DESCRIPTION_WRITE);
            r = ifapi_keystore_store_finish(&context->io);
            return_try_again(r);
            return_if_error_reset_state(r, "write_finish failed");

            context->state = _FAPI_STATE_INIT;
            r = TSS2_RC_SUCCESS;
            break;

        statecasedefault(context->state);
    }

error_cleanup:
    /* Cleanup any intermediate results and state stored in the context. */
    ifapi_cleanup_ifapi_object(object);
    ifapi_cleanup_ifapi_object(&context->loadKey.auth_object);
    ifapi_cleanup_ifapi_object(context->loadKey.key_object);
    ifapi_cleanup_ifapi_object(&context->createPrimary.pkey_object);
    SAFE_FREE(command->object_path);
    LOG_TRACE("finished");
    return r;
}
