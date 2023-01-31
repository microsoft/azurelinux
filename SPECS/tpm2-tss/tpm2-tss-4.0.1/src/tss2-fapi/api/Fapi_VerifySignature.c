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
#include "fapi_crypto.h"
#include "fapi_int.h"
#include "fapi_util.h"
#include "tss2_esys.h"
#define LOGMODULE fapi
#include "util/log.h"
#include "util/aux_util.h"

/** One-Call function for Fapi_VerifySignature
 *
 * Verifies a signature using a public key found in a keyPath.
 *
 * @param[in,out] context The FAPI_CONTEXT
 * @param[in] keyPath The path to the verification public key
 * @param[in] digest The that was signed. Must be already hashed
 * @param[in] digestSize the size of digest in bytes
 * @param[in] signature The signature to be verified
 * @param[in] signatureSize The size of signature in bytes
 *
 * @retval TSS2_RC_SUCCESS: if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE: if context, keyPath, signature, or
 *         digest is NULL.
 * @retval TSS2_FAPI_RC_BAD_CONTEXT: if context corruption is detected.
 * @retval TSS2_FAPI_RC_KEY_NOT_FOUND: if keyPath does not map to a FAPI object.
 * @retval TSS2_FAPI_RC_BAD_KEY: if the object at publicKeyPath is not a key, or
 *         is a key that is unsuitable for the requested operation.
 * @retval TSS2_FAPI_RC_BAD_VALUE: if signature is invalid (has the wrong format)
 *         or if digestSize is zero.
 * @retval TSS2_FAPI_RC_SIGNATURE_VERIFICATION_FAILED: if the signature fails to
 *         verify.
 * @retval TSS2_FAPI_RC_BAD_SEQUENCE: if the context has an asynchronous
 *         operation already pending.
 * @retval TSS2_FAPI_RC_IO_ERROR: if the data cannot be saved.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory for
 *         internal operations or return parameters.
 * @retval TSS2_FAPI_RC_PATH_NOT_FOUND if a FAPI object path was not found
 *         during authorization.
 * @retval TSS2_FAPI_RC_TRY_AGAIN if an I/O operation is not finished yet and
 *         this function needs to be called again.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE if an internal error occurred.
 * @retval TSS2_FAPI_RC_NOT_PROVISIONED FAPI was not provisioned.
 * @retval TSS2_FAPI_RC_BAD_PATH if the path is used in inappropriate context
 *         or contains illegal characters.
 */
TSS2_RC
Fapi_VerifySignature(
    FAPI_CONTEXT  *context,
    char    const *keyPath,
    uint8_t const *digest,
    size_t         digestSize,
    uint8_t const *signature,
    size_t         signatureSize)
{
    LOG_TRACE("called for context:%p", context);

    TSS2_RC r;

    /* Check for NULL parameters */
    check_not_null(context);
    check_not_null(keyPath);
    check_not_null(digest);
    check_not_null(signature);

    r = Fapi_VerifySignature_Async(context, keyPath, digest, digestSize,
                                   signature, signatureSize);
    return_if_error_reset_state(r, "Key_VerifySignature");

    do {
        /* We wait for file I/O to be ready if the FAPI state automata
           are in a file I/O state. */
        r = ifapi_io_poll(&context->io);
        return_if_error(r, "Something went wrong with IO polling");

        /* Repeatedly call the finish function, until FAPI has transitioned
           through all execution stages / states of this invocation. */
        r = Fapi_VerifySignature_Finish(context);
    } while (base_rc(r) == TSS2_BASE_RC_TRY_AGAIN);

    return_if_error_reset_state(r, "Key_VerifySignature");

    LOG_TRACE("finished");
    return TSS2_RC_SUCCESS;
}

/** Asynchronous function for Fapi_VerifySignature
 *
 * Verifies a signature using a public key found in a keyPath.
 *
 * Call Fapi_VerifySignature_Finish to finish the execution of this command.
 *
 * @param[in,out] context The FAPI_CONTEXT
 * @param[in] keyPath The path to the verification public key
 * @param[in] digest The that was signed. Must be already hashed
 * @param[in] digestSize the size of digest in bytes
 * @param[in] signature The signature to be verified
 * @param[in] signatureSize The size of signature in bytes
 *
 * @retval TSS2_RC_SUCCESS: if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE: if context, keyPath, signature, or
 *         digest is NULL.
 * @retval TSS2_FAPI_RC_BAD_CONTEXT: if context corruption is detected.
 * @retval TSS2_FAPI_RC_KEY_NOT_FOUND: if keyPath does not map to a FAPI object.
 * @retval TSS2_FAPI_RC_BAD_KEY: if the object at publicKeyPath is not a key, or
 *         is a key that is unsuitable for the requested operation.
 * @retval TSS2_FAPI_RC_BAD_VALUE: if signature is invalid (has the wrong format)
 *         or if digestSize is zero.
 * @retval TSS2_FAPI_RC_SIGNATURE_VERIFICATION_FAILED: if the signature fails to
 *         verify.
 * @retval TSS2_FAPI_RC_BAD_SEQUENCE: if the context has an asynchronous
 *         operation already pending.
 * @retval TSS2_FAPI_RC_IO_ERROR: if the data cannot be saved.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory for
 *         internal operations or return parameters.
 * @retval TSS2_FAPI_RC_PATH_NOT_FOUND if a FAPI object path was not found
 *         during authorization.
 * @retval TSS2_FAPI_RC_NOT_PROVISIONED FAPI was not provisioned.
 * @retval TSS2_FAPI_RC_BAD_PATH if the path is used in inappropriate context
 *         or contains illegal characters.
 */
TSS2_RC
Fapi_VerifySignature_Async(
    FAPI_CONTEXT  *context,
    char    const *keyPath,
    uint8_t const *digest,
    size_t         digestSize,
    uint8_t const *signature,
    size_t         signatureSize)
{
    LOG_TRACE("called for context:%p", context);
    LOG_TRACE("keyPath: %s", keyPath);
    if (digest) {
        LOGBLOB_TRACE(digest, digestSize, "digest");
    } else {
        LOG_TRACE("digset: (null) digestSize: %zi", digestSize);
    }
    if (signature) {
        LOGBLOB_TRACE(signature, signatureSize, "signature");
    } else {
        LOG_TRACE("signature: (null) sigantureSize: %zi", signatureSize);
    }

    TSS2_RC r;

    /* Check for NULL parameters */
    check_not_null(context);
    check_not_null(keyPath);
    check_not_null(digest);
    check_not_null(signature);

    /* Helpful alias pointers */
    IFAPI_Key_VerifySignature * command = &context->cmd.Key_VerifySignature;

    r = ifapi_non_tpm_mode_init(context);
    return_if_error(r, "Initialize VerifySignature");

    /* Copy parameters to context for use during _Finish. */
    uint8_t * signatureBuffer = malloc(signatureSize);
    uint8_t * digestBuffer = malloc(digestSize);
    goto_if_null2(signatureBuffer, "Out of memory", r, TSS2_FAPI_RC_MEMORY,
            error_cleanup);
    goto_if_null2(digestBuffer, "Out of memory", r, TSS2_FAPI_RC_MEMORY,
            error_cleanup);
    memcpy(signatureBuffer, signature, signatureSize);
    memcpy(digestBuffer, digest, digestSize);
    command->signature = signatureBuffer;
    command->digest = digestBuffer;
    command->signatureSize = signatureSize;
    command->digestSize = digestSize;
    memset(&command->key_object, 0, sizeof(IFAPI_OBJECT));

    /* Load the key for verification from the keystore. */
    r = ifapi_keystore_load_async(&context->keystore, &context->io, keyPath);
    goto_if_error2(r, "Could not open: %s", error_cleanup, keyPath);

    /* Initialize the context state for this operation. */
    LOG_TRACE("finished");
    return TSS2_RC_SUCCESS;

error_cleanup:
    /* Cleanup duplicated input parameters that were copied before. */
    SAFE_FREE(signatureBuffer);
    command->signature = NULL;
    SAFE_FREE(digestBuffer);
    command->digest = NULL;
    return r;
}

/** Asynchronous finish function for Fapi_VerifySignature
 *
 * This function should be called after a previous Fapi_VerifySignature_Async.
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
 * @retval TSS2_FAPI_RC_SIGNATURE_VERIFICATION_FAILED if the signature could not
 *         be verified
 */
TSS2_RC
Fapi_VerifySignature_Finish(
    FAPI_CONTEXT  *context)
{
    LOG_TRACE("called for context:%p", context);

    TSS2_RC r;

    /* Check for NULL parameters */
    check_not_null(context);

    /* Helpful alias pointers */
    IFAPI_Key_VerifySignature * command = &context->cmd.Key_VerifySignature;

    r = ifapi_keystore_load_finish(&context->keystore, &context->io,
                                   &command->key_object);
    return_try_again(r);
    return_if_error_reset_state(r, "read_finish failed");

    /* Verify the signature using a helper that tests all known signature schemes. */
    r = ifapi_verify_signature(&command->key_object, command->signature,
           command->signatureSize, command->digest, command->digestSize);
    goto_if_error(r, "Verify signature.", cleanup);

cleanup:
    /* Cleanup any intermediate results and state stored in the context. */
    if (command->key_object.objectType)
        ifapi_cleanup_ifapi_object(&command->key_object);
    ifapi_cleanup_ifapi_object(&context->loadKey.auth_object);
    ifapi_cleanup_ifapi_object(context->loadKey.key_object);
    ifapi_cleanup_ifapi_object(&context->createPrimary.pkey_object);
    SAFE_FREE(command->signature);
    SAFE_FREE(command->digest);
    LOG_TRACE("finished");
    return r;
}
