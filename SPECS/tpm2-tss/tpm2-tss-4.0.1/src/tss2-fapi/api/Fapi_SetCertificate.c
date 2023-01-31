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

/** One-Call function for Fapi_SetCertificate
 *
 * Sets an x509 cert into the path of a key.
 *
 * @param[in,out] context The FAPI_CONTEXT
 * @param[in] path The path of the entity to be associated with the
 *            certificate
 * @param[in] x509certData The certificate that is associated with the entity.
 *            If this is NULL an existing certificate will be removed from
 *            the entity
 *
 * @retval TSS2_RC_SUCCESS: if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE: if context or path is NULL.
 * @retval TSS2_FAPI_RC_BAD_CONTEXT: if context corruption is detected.
 * @retval TSS2_FAPI_RC_KEY_NOT_FOUND: if path does not map to a FAPI entity.
 * @retval TSS2_FAPI_RC_BAD_KEY: if x509certData is invalid.
 * @retval TSS2_FAPI_RC_BAD_SEQUENCE: if the context has an asynchronous
 *         operation already pending.
 * @retval TSS2_FAPI_RC_IO_ERROR: if the data cannot be saved.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory for
 *         internal operations or return parameters.
 * @retval TSS2_FAPI_RC_PATH_NOT_FOUND if a FAPI object path was not found
 *         during authorization.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_TRY_AGAIN if an I/O operation is not finished yet and
 *         this function needs to be called again.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE if an internal error occurred.
 * @retval TSS2_ESYS_RC_* possible error codes of ESAPI.
 * @retval TSS2_FAPI_RC_NOT_PROVISIONED FAPI was not provisioned.
 * @retval TSS2_FAPI_RC_BAD_PATH if the path is used in inappropriate context
 *         or contains illegal characters.
 */
TSS2_RC
Fapi_SetCertificate(
    FAPI_CONTEXT  *context,
    char    const *path,
    char    const *x509certData)
{
    LOG_TRACE("called for context:%p", context);

    TSS2_RC r;

    /* Check for NULL parameters */
    check_not_null(context);
    check_not_null(path);

    r = Fapi_SetCertificate_Async(context, path, x509certData);
    return_if_error_reset_state(r, "Key_SetCertificate");

    do {
        /* We wait for file I/O to be ready if the FAPI state automata
           are in a file I/O state. */
        r = ifapi_io_poll(&context->io);
        return_if_error(r, "Something went wrong with IO polling");

        /* Repeatedly call the finish function, until FAPI has transitioned
           through all execution stages / states of this invocation. */
        r = Fapi_SetCertificate_Finish(context);
    } while (base_rc(r) == TSS2_BASE_RC_TRY_AGAIN);

    return_if_error_reset_state(r, "Key_SetCertificate");

    LOG_TRACE("finished");
    return TSS2_RC_SUCCESS;
}

/** Asynchronous function for Fapi_SetCertificate
 *
 * Sets an x509 cert into the path of a key.
 *
 * Call Fapi_SetCertificate_Finish to finish the execution of this command.
 *
 * @param[in,out] context The FAPI_CONTEXT
 * @param[in] path The path of the entity to be associated with the
 *            certificate
 * @param[in] x509certData The certificate that is associated with the entity.
 *            If this is NULL an existing certificate will be removed from
 *            the entity
 *
 * @retval TSS2_RC_SUCCESS: if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE: if context or path is NULL.
 * @retval TSS2_FAPI_RC_BAD_CONTEXT: if context corruption is detected.
 * @retval TSS2_FAPI_RC_KEY_NOT_FOUND: if path does not map to a FAPI entity.
 * @retval TSS2_FAPI_RC_BAD_KEY: if x509certData is invalid.
 * @retval TSS2_FAPI_RC_BAD_SEQUENCE: if the context has an asynchronous
 *         operation already pending.
 * @retval TSS2_FAPI_RC_IO_ERROR: if the data cannot be saved.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory for
 *         internal operations or return parameters.
 * @retval TSS2_FAPI_RC_PATH_NOT_FOUND if a FAPI object path was not found
 *         during authorization.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_NOT_PROVISIONED FAPI was not provisioned.
 * @retval TSS2_FAPI_RC_BAD_PATH if the path is used in inappropriate context
 *         or contains illegal characters.
 */
TSS2_RC
Fapi_SetCertificate_Async(
    FAPI_CONTEXT  *context,
    char    const *path,
    char    const *x509certData)
{
    LOG_TRACE("called for context:%p", context);
    LOG_TRACE("path: %s", path);
    LOG_TRACE("x509certData: %s", x509certData);

    TSS2_RC r;

    /* Check for NULL parameters */
    check_not_null(context);
    check_not_null(path);

    /* Helpful alias pointers */
    IFAPI_Key_SetCertificate * command = &context->cmd.Key_SetCertificate;

    r = ifapi_non_tpm_mode_init(context);
    goto_if_error(r, "Initialize SetCertificate", error_cleanup);

    /* Copy parameters to context for use during _Finish. */
    if (x509certData) {
        strdup_check(command->pem_cert, x509certData, r, error_cleanup);
    } else {
        command->pem_cert = NULL;
    }
    strdup_check(command->key_path, path, r, error_cleanup);
    context->state = KEY_SET_CERTIFICATE_READ;
    memset(&command->key_object, 0, sizeof(IFAPI_OBJECT));

    /* Load the object's current metadata from the keystore. */
    r = ifapi_keystore_load_async(&context->keystore, &context->io, path);
    goto_if_error2(r, "Could not open: %s", error_cleanup, path);

    LOG_TRACE("finished");
    return TSS2_RC_SUCCESS;

error_cleanup:
    /* Initialize the context state for this operation. */
    SAFE_FREE(command->pem_cert);
    SAFE_FREE(command->key_path);
    return r;
}

/** Asynchronous finish function for Fapi_SetCertificate
 *
 * This function should be called after a previous Fapi_SetCertificate_Async.
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
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE if an internal error occurred.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_ESYS_RC_* possible error codes of ESAPI.
 * @retval TSS2_FAPI_RC_BAD_PATH if the path is used in inappropriate context
 *         or contains illegal characters.
 * @retval TSS2_FAPI_RC_PATH_NOT_FOUND if a FAPI object path was not found
 *         during authorization.
 */
TSS2_RC
Fapi_SetCertificate_Finish(
    FAPI_CONTEXT  *context)
{
    LOG_TRACE("called for context:%p", context);

    TSS2_RC r;

    /* Check for NULL parameters */
    check_not_null(context);

    /* Helpful alias pointers */
    IFAPI_Key_SetCertificate * command = &context->cmd.Key_SetCertificate;
    IFAPI_OBJECT *key_object = &command->key_object;
    const char ** pem_cert = &command->pem_cert;
    char ** pem_cert_dup = &command->pem_cert_dup;

    switch (context->state) {
        statecase(context->state, KEY_SET_CERTIFICATE_READ)
            r = ifapi_keystore_load_finish(&context->keystore, &context->io, key_object);
            return_try_again(r);
            return_if_error_reset_state(r, "read_finish failed");

            /* Duplicate and store the certificate in the key object. */
            if (!*pem_cert) {
                strdup_check(*pem_cert_dup, "", r, error_cleanup);
            } else {
                strdup_check(*pem_cert_dup, *pem_cert, r, error_cleanup);
            }
            if (key_object->objectType == IFAPI_EXT_PUB_KEY_OBJ) {
                SAFE_FREE(key_object->misc.ext_pub_key.certificate);
                key_object->misc.ext_pub_key.certificate = *pem_cert_dup;
            } else {
                SAFE_FREE(key_object->misc.key.certificate);
                key_object->misc.key.certificate = *pem_cert_dup;
            }

            r = ifapi_initialize_object(context->esys, key_object);
            goto_if_error_reset_state(r, "Initialize key object", error_cleanup);

            /* Perform esys serialization if necessary */
            r = ifapi_esys_serialize_object(context->esys, key_object);
            goto_if_error(r, "Prepare serialization", error_cleanup);

            /* Start writing the NV object to the key store */
            r = ifapi_keystore_store_async(&context->keystore, &context->io,
                    command->key_path, key_object);
            goto_if_error_reset_state(r, "Could not open: %sh", error_cleanup,
                    command->key_path);

            context->state = KEY_SET_CERTIFICATE_WRITE;
            fallthrough;

        statecase(context->state, KEY_SET_CERTIFICATE_WRITE)
            /* Finish writing the object to the key store */
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
    SAFE_FREE(command->pem_cert);
    SAFE_FREE(command->key_path);
    if (key_object->objectType) {
        ifapi_cleanup_ifapi_object(key_object);
    }
    ifapi_cleanup_ifapi_object(&context->loadKey.auth_object);
    ifapi_cleanup_ifapi_object(context->loadKey.key_object);
    ifapi_cleanup_ifapi_object(&context->createPrimary.pkey_object);
    LOG_TRACE("finished");
    return r;
}
