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

/** One-Call function for Fapi_GetDescription
 *
 * Returns the description of a previously stored object.
 *
 * @param[in,out] context The FAPI_CONTEXT
 * @param[in] path The path of the object for which the description is loaded
 * @param[out] description The description of the object
 *
 * @retval TSS2_RC_SUCCESS: if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE: if context, path or description is NULL.
 * @retval TSS2_FAPI_RC_BAD_CONTEXT: if context corruption is detected.
 * @retval TSS2_FAPI_RC_BAD_PATH: if path does not map to a FAPI entity.
 * @retval TSS2_FAPI_RC_BAD_SEQUENCE: if the context has an asynchronous
 *         operation already pending.
 * @retval TSS2_FAPI_RC_IO_ERROR: if the data cannot be saved.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory for
 *         internal operations or return parameters.
 * @retval TSS2_FAPI_RC_PATH_NOT_FOUND if a FAPI object path was not found
 *         during authorization.
 * @retval TSS2_FAPI_RC_KEY_NOT_FOUND if a key was not found.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_TRY_AGAIN if an I/O operation is not finished yet and
 *         this function needs to be called again.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE if an internal error occurred.
 * @retval TSS2_FAPI_RC_NOT_PROVISIONED FAPI was not provisioned.
 */
TSS2_RC
Fapi_GetDescription(
    FAPI_CONTEXT *context,
    char   const *path,
    char        **description)
{
    LOG_TRACE("called for context:%p", context);

    TSS2_RC r;

    /* Check for NULL parameters */
    check_not_null(context);
    check_not_null(path);
    check_not_null(description);

    r = Fapi_GetDescription_Async(context, path);
    return_if_error_reset_state(r, "Path_SetDescription");

    do {
        /* We wait for file I/O to be ready if the FAPI state automata
           are in a file I/O state. */
        r = ifapi_io_poll(&context->io);
        return_if_error(r, "Something went wrong with IO polling");

        /* Repeatedly call the finish function, until FAPI has transitioned
           through all execution stages / states of this invocation. */
        r = Fapi_GetDescription_Finish(context, description);
    } while (base_rc(r) == TSS2_BASE_RC_TRY_AGAIN);

    return_if_error_reset_state(r, "Path_SetDescription");

    LOG_TRACE("finished");
    return TSS2_RC_SUCCESS;
}

/** Asynchronous function for Fapi_GetDescription
 *
 * Returns the description of a previously stored object.
 *
 * Call Fapi_GetDescription_Finish to finish the execution of this command.
 *
 * @param[in,out] context The FAPI_CONTEXT
 * @param[in] path The path of the object for which the description is loaded
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
 * @retval TSS2_FAPI_RC_PATH_NOT_FOUND if a FAPI object path was not found
 *         during authorization.
 * @retval TSS2_FAPI_RC_KEY_NOT_FOUND if a key was not found.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_NOT_PROVISIONED FAPI was not provisioned.
 */
TSS2_RC
Fapi_GetDescription_Async(
    FAPI_CONTEXT *context,
    char   const *path)
{
    LOG_TRACE("called for context:%p", context);
    LOG_TRACE("path: %s", path);

    TSS2_RC r;

    /* Check for NULL parameters */
    check_not_null(context);
    check_not_null(path);

    /* Load the object metadata from keystore. */
    r = ifapi_keystore_load_async(&context->keystore, &context->io, path);
    return_if_error2(r, "Could not open: %s", path);

    /* Initialize the context state for this operation. */
    context->state = PATH_GET_DESCRIPTION_READ;

    LOG_TRACE("finished");
    return TSS2_RC_SUCCESS;
}

/** Asynchronous finish function for Fapi_GetDescription
 *
 * This function should be called after a previous Fapi_GetDescription_Async.
 *
 * @param[in,out] context The FAPI_CONTEXT
 * @param[out] description The description of the object
 *
 * @retval TSS2_RC_SUCCESS: if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE: if context or description is NULL.
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
 */
TSS2_RC
Fapi_GetDescription_Finish(
    FAPI_CONTEXT *context,
    char        **description)
{
    LOG_TRACE("called for context:%p", context);

    TSS2_RC r;
    IFAPI_OBJECT object;

    /* Check for NULL parameters */
    check_not_null(context);
    check_not_null(description);

    switch (context->state) {
        statecase(context->state, PATH_GET_DESCRIPTION_READ);
            r = ifapi_keystore_load_finish(&context->keystore, &context->io, &object);
            return_try_again(r);
            return_if_error_reset_state(r, "read_finish failed");

            /* Retrieve the description from the metadata object. */
            r = ifapi_get_description(&object, description);
            ifapi_cleanup_ifapi_object(&object);
            return_if_error_reset_state(r, "Get description");

            context->state = _FAPI_STATE_INIT;
            r = TSS2_RC_SUCCESS;
            break;

        statecasedefault(context->state);
    }
    LOG_TRACE("finished");
    /* Cleanup any intermediate results and state stored in the context. */
    ifapi_cleanup_ifapi_object(&object);
    ifapi_cleanup_ifapi_object(&context->loadKey.auth_object);
    ifapi_cleanup_ifapi_object(context->loadKey.key_object);
    ifapi_cleanup_ifapi_object(&context->createPrimary.pkey_object);
    return r;
}
