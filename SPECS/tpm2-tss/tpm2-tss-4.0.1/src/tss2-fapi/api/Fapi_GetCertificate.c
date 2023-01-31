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
#include "fapi_crypto.h"

/** One-Call function for Fapi_GetCertificate
 *
 * Gets an x.509 certificate for the key at a given path.
 *
 * @param[in,out] context The FAPI_CONTEXT
 * @param[in] path The path to the key whose certificate is created
 * @param[out] x509certData The PEM-encoded certificate
 *
 * @retval TSS2_RC_SUCCESS: if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE: if context, path or x509CertData is
 *         NULL.
 * @retval TSS2_FAPI_RC_BAD_CONTEXT: if context corruption is detected.
 * @retval TSS2_FAPI_RC_PATH_NOT_FOUND: if path does not map to a FAPI entity.
 * @retval TSS2_FAPI_RC_BAD_KEY: if the key is unsuitable for the requested
 *         operation.
 * @retval TSS2_FAPI_RC_NO_CERTIFICATE: if there is not a x.509 cert associated
 *         with the path of the key.
 * @retval TSS2_FAPI_RC_BAD_SEQUENCE: if the context has an asynchronous
 *         operation already pending.
 * @retval TSS2_FAPI_RC_IO_ERROR: if the data cannot be saved.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory for
 *         internal operations or return parameters.
 * @retval TSS2_FAPI_RC_KEY_NOT_FOUND if a key was not found.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_TRY_AGAIN if an I/O operation is not finished yet and
 *         this function needs to be called again.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE if an internal error occurred.
 * @retval TSS2_FAPI_RC_NOT_PROVISIONED FAPI was not provisioned.
 * @retval TSS2_FAPI_RC_BAD_PATH if the path is used in inappropriate context
 *         or contains illegal characters.
 */
TSS2_RC
Fapi_GetCertificate(
    FAPI_CONTEXT *context,
    char const   *path,
    char        **x509certData)
{
    LOG_TRACE("called for context:%p", context);

    TSS2_RC r;

    /* Check for NULL parameters */
    check_not_null(context);
    check_not_null(path);
    check_not_null(x509certData);

    r = Fapi_GetCertificate_Async(context, path);
    return_if_error_reset_state(r, "Key_GetCertificate");

    do {
        /* We wait for file I/O to be ready if the FAPI state automata
           are in a file I/O state. */
        r = ifapi_io_poll(&context->io);
        return_if_error(r, "Something went wrong with IO polling");

        /* Repeatedly call the finish function, until FAPI has transitioned
           through all execution stages / states of this invocation. */
        r = Fapi_GetCertificate_Finish(context, x509certData);
    } while (base_rc(r) == TSS2_BASE_RC_TRY_AGAIN);

    return_if_error_reset_state(r, "Key_GetCertificate");

    LOG_TRACE("finished");
    return TSS2_RC_SUCCESS;
}

/** Asynchronous function for Fapi_GetCertificate
 *
 * Gets an x.509 certificate for the key at a given path.
 *
 * Call Fapi_GetCertificate_Finish to finish the execution of this command.
 *
 * @param[in,out] context The FAPI_CONTEXT
 * @param[in] path The path to the key whose certificate is created
 *
 * @retval TSS2_RC_SUCCESS: if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE: if context or path is NULL.
 * @retval TSS2_FAPI_RC_BAD_CONTEXT: if context corruption is detected.
 * @retval TSS2_FAPI_RC_PATH_NOT_FOUND: if path does not map to a FAPI entity.
 * @retval TSS2_FAPI_RC_BAD_KEY: if the key is unsuitable for the requested
 *         operation.
 * @retval TSS2_FAPI_RC_NO_CERTIFICATE: if there is not a x.509 cert associated
 *         with the path of the key.
 * @retval TSS2_FAPI_RC_BAD_SEQUENCE: if the context has an asynchronous
 *         operation already pending.
 * @retval TSS2_FAPI_RC_IO_ERROR: if the data cannot be saved.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory for
 *         internal operations or return parameters.
 * @retval TSS2_FAPI_RC_KEY_NOT_FOUND if a key was not found.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_NOT_PROVISIONED FAPI was not provisioned.
 * @retval TSS2_FAPI_RC_BAD_PATH if the path is used in inappropriate context
 *         or contains illegal characters.
 */
TSS2_RC
Fapi_GetCertificate_Async(
    FAPI_CONTEXT   *context,
    char    const  *path)

{
    LOG_TRACE("called for context:%p", context);
    LOG_TRACE("path: %s", path);

    TSS2_RC r;

    /* Check for NULL parameters */
    check_not_null(context);
    check_not_null(path);

    r = ifapi_non_tpm_mode_init(context);
    return_if_error(r, "Initialize GetCertificate");

    /* Load the object metadata from keystore. */
    r = ifapi_keystore_load_async(&context->keystore, &context->io, path);
    return_if_error2(r, "Could not open: %s", path);

    /* Initialize the context state for this operation. */
    context->state = KEY_GET_CERTIFICATE_READ;

    LOG_TRACE("finished");
    return TSS2_RC_SUCCESS;
}

/** Asynchronous finish function for Fapi_GetCertificate
 *
 * This function should be called after a previous Fapi_GetCertificate_Async.
 *
 * @param[in,out] context The FAPI_CONTEXT
 * @param[out] x509certData The PEM-encoded certificate
 *
 * @retval TSS2_RC_SUCCESS: if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE: if context or x509certData is NULL.
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
Fapi_GetCertificate_Finish(
    FAPI_CONTEXT  *context,
    char         **x509certData)
{
    LOG_TRACE("called for context:%p", context);

    TSS2_RC r;

    /* Check for NULL parameters */
    check_not_null(context);
    check_not_null(x509certData);

    /* Helpful alias pointers */
    IFAPI_Key_SetCertificate *command = &context->cmd.Key_SetCertificate;
    IFAPI_OBJECT *keyObject = &command->key_object;

    switch (context->state) {
        statecase(context->state, KEY_GET_CERTIFICATE_READ)
            r = ifapi_keystore_load_finish(&context->keystore, &context->io, keyObject);
            return_try_again(r);
            return_if_error_reset_state(r, "read_finish failed");

            /* Retrieve the appropriate field from the objects and duplicate its
               content to be returned to the user. */
            if (keyObject->objectType == IFAPI_EXT_PUB_KEY_OBJ) {
                strdup_check(*x509certData, keyObject->misc.ext_pub_key.certificate,
                        r, error_cleanup);
            } else if (keyObject->objectType == IFAPI_KEY_OBJ)  {
                strdup_check(*x509certData, keyObject->misc.key.certificate,
                        r, error_cleanup);
            } else {
                strdup_check(*x509certData, "",
                             r, error_cleanup);
            }

            context->state = _FAPI_STATE_INIT;
            r = TSS2_RC_SUCCESS;
            break;

        statecasedefault(context->state);
    }

error_cleanup:
    /* Cleanup any intermediate results and state stored in the context. */
    if (keyObject->objectType) {
        ifapi_cleanup_ifapi_object(keyObject);
    }
    ifapi_cleanup_ifapi_object(&context->loadKey.auth_object);
    ifapi_cleanup_ifapi_object(context->loadKey.key_object);
    ifapi_cleanup_ifapi_object(&context->createPrimary.pkey_object);

    LOG_TRACE("finished");
    return r;
}
