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

#define FAPI_MAX_APP_DATA_SIZE 10*1024*1024

/** One-Call function for Fapi_SetAppData
 *
 * Associates an arbitrary data blob with a given object.
 *
 * @param[in,out] context The FAPI_CONTEXT
 * @param[in] path The path to the object the blob is associated with
 * @param[in] appData The blob to associate with the object. May be NULL
 * @param[in] appDataSize The size of appData in bytes. Must be 0 if appData is
 *            NULL
 *
 * @retval TSS2_RC_SUCCESS: if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE: if context or path is NULL or if appData
 *         is NULL and appDataSize is not 0.
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
Fapi_SetAppData(
    FAPI_CONTEXT  *context,
    char    const *path,
    uint8_t const *appData,
    size_t         appDataSize)
{
    LOG_TRACE("called for context:%p", context);

    TSS2_RC r;

    /* Check for NULL parameters */
    check_not_null(context);
    check_not_null(path);

    r = Fapi_SetAppData_Async(context, path, appData, appDataSize);
    return_if_error_reset_state(r, "SetAppData");

    do {
        /* We wait for file I/O to be ready if the FAPI state automata
           are in a file I/O state. */
        r = ifapi_io_poll(&context->io);
        return_if_error(r, "Something went wrong with IO polling");

        /* Repeatedly call the finish function, until FAPI has transitioned
           through all execution stages / states of this invocation. */
        r = Fapi_SetAppData_Finish(context);
    } while (base_rc(r) == TSS2_BASE_RC_TRY_AGAIN);

    return_if_error_reset_state(r, "SetAppData");

    LOG_TRACE("finished");
    return TSS2_RC_SUCCESS;
}

/** One-Call function for Fapi_SetAppData
 *
 * Associates an arbitrary data blob with a given object.
 *
 * Call Fapi_SetAppData_Finish to finish the execution of this command.
 *
 * @param[in,out] context The FAPI_CONTEXT
 * @param[in] path The path to the object the blob is associated with
 * @param[in] appData The blob to associate with the object. May be NULL
 * @param[in] appDataSize The size of appData in bytes. Must be 0 if appData is
 *            NULL
 *
 * @retval TSS2_RC_SUCCESS: if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE: if context or path is NULL or if appData
 *         is NULL and appDataSize is not 0.
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
Fapi_SetAppData_Async(
    FAPI_CONTEXT  *context,
    char    const *path,
    uint8_t const *appData,
    size_t         appDataSize)
{
    LOG_TRACE("called for context:%p", context);
    LOG_TRACE("path: %s", path);
    if (appData) {
        LOGBLOB_TRACE(appData, appDataSize, "appData");
    } else {
        LOG_TRACE("appData: (null) appDataSize: %zi", appDataSize);
    }

    TSS2_RC r;

    /* Check for NULL parameters */
    check_not_null(context);
    check_not_null(path);

    /* App data is restricted to 10MB. */
    if (appDataSize > FAPI_MAX_APP_DATA_SIZE) {
        LOG_ERROR("Only 10MB are allowd for app data.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }

    /* Check for invalid parameters */
    if (!appData && appDataSize != 0) {
        return_error(TSS2_FAPI_RC_BAD_VALUE,
                     "NULL-pointer passed for appData, though appDataSize != 0.");
    }

    /* Helpful alias pointers */
    IFAPI_Path_SetDescription * command = &context->cmd.path_set_info;

    /* Copy parameters to context for use during _Finish. */
    strdup_check(command->object_path, path, r, error_cleanup);

    if (appDataSize > 0) {
        command->appData.buffer = malloc(appDataSize);
        goto_if_null2(command->appData.buffer, "Out of memory.",
                      r, TSS2_FAPI_RC_MEMORY, error_cleanup);

        memcpy(&command->appData.buffer[0], appData, appDataSize);
    } else {
        command->appData.buffer = NULL;
    }
    command->appData.size = appDataSize;

    /* Load the current metadata for the object from keystore. */
    r = ifapi_keystore_load_async(&context->keystore, &context->io, path);
    return_if_error2(r, "Could not open: %s", path);

    /* Initialize the context state for this operation. */
    context->state = APP_DATA_SET_READ;
    LOG_TRACE("finished");
    return TSS2_RC_SUCCESS;

error_cleanup:
    /* Cleanup duplicated input parameters that were copied before. */
    SAFE_FREE(command->object_path);
    SAFE_FREE(command->appData.buffer);
    return r;
}

/** Asynchronous finish function for Fapi_SetAppData
 *
 * This function should be called after a previous Fapi_SetAppData_Async.
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
 * @retval TSS2_FAPI_RC_BAD_PATH if a path is used in inappropriate context
 *         or contains illegal characters.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE if an internal error occurred.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_PATH_NOT_FOUND if a FAPI object path was not found
 *         during authorization.
 */
TSS2_RC
Fapi_SetAppData_Finish(
    FAPI_CONTEXT *context)
{
    LOG_TRACE("called for context:%p", context);

    TSS2_RC r;

    /* Check for NULL parameters */
    check_not_null(context);

    /* Helpful alias pointers */
    IFAPI_Path_SetDescription * command = &context->cmd.path_set_info;
    IFAPI_OBJECT *object = &command->object;
    UINT8_ARY *objAppData;

    switch (context->state) {
        statecase(context->state, APP_DATA_SET_READ);
            r = ifapi_keystore_load_finish(&context->keystore, &context->io, object);
            return_try_again(r);
            return_if_error_reset_state(r, "read_finish failed");

            r = ifapi_initialize_object(context->esys, object);
            goto_if_error_reset_state(r, "Initialize key object", error_cleanup);

            /* Depending on the object type get the correct appData pointer. */
            switch (object->objectType) {
            case IFAPI_KEY_OBJ:
                objAppData = &object->misc.key.appData;
                break;
            case IFAPI_NV_OBJ:
                objAppData = &object->misc.nv.appData;
                break;
            default:
                goto_error(r, TSS2_FAPI_RC_BAD_PATH, "Object has no app data.", error_cleanup);
            }

            /* If exists delete old appData */
            SAFE_FREE(objAppData->buffer);

            /* Set new appData for object */
            objAppData->size = command->appData.size;
            objAppData->buffer = command->appData.buffer;

            /* Prepare (over-)writing of object */
            r = ifapi_keystore_store_async(&context->keystore, &context->io,
                                           command->object_path, object);
            goto_if_error_reset_state(r, "Could not open: %sh", error_cleanup,
                                      command->object_path);

            fallthrough;

        statecase(context->state, APP_DATA_SET_WRITE);
            /* Finish writing of object */
            r = ifapi_keystore_store_finish(&context->io);
            return_try_again(r);
            return_if_error_reset_state(r, "write_finish failed");
            ifapi_cleanup_ifapi_object(object);

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
