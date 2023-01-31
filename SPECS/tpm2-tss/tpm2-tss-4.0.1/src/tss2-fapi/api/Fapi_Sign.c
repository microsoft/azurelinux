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

/** One-Call function for Fapi_Sign
 *
 * Uses a key, identified by its path, to sign a digest and puts the result in a
 * TPM2B bytestream.
 *
 * @param[in,out] context The FAPI_CONTEXT
 * @param[in] keyPath The path of the signature key
 * @param[in] padding A padding algorithm. Must be either "RSA_SSA" or
 *            "RSA_PSS" or NULL
 * @param[in] digest The digest to sign. Must be already hashed
 * @param[in] digestSize The size of the digest in bytes
 * @param[out] signature The signature
 * @param[out] signatureSize The size of signature in bytes. May be NULL
 * @param[out] publicKey The public key that can be used to verify signature
 *            in PEM format. May be NULL
 * @param[out] certificate The certificate associated with the signing key in PEM
 *            format. May be NULL
 *
 * @retval TSS2_RC_SUCCESS: if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE: if context, keyPath, digest or signature
 *         is NULL.
 * @retval TSS2_FAPI_RC_BAD_CONTEXT: if context corruption is detected.
 * @retval TSS2_FAPI_RC_KEY_NOT_FOUND: if keyPath does not map to a FAPI key.
 * @retval TSS2_FAPI_RC_BAD_KEY: if the object at keyPath is not a key, or is a
 *         key that is unsuitable for the requested operation.
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
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE if an internal error occurred.
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
Fapi_Sign(
    FAPI_CONTEXT  *context,
    char    const *keyPath,
    char    const *padding,
    uint8_t const *digest,
    size_t         digestSize,
    uint8_t      **signature,
    size_t        *signatureSize,
    char         **publicKey,
    char         **certificate)
{
    LOG_TRACE("called for context:%p", context);

    TSS2_RC r, r2;

    /* Check for NULL parameters */
    check_not_null(context);
    check_not_null(keyPath);
    check_not_null(digest);
    check_not_null(signature);

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

    r = Fapi_Sign_Async(context, keyPath, padding, digest, digestSize);
    return_if_error_reset_state(r, "Key_Sign");

    do {
        /* We wait for file I/O to be ready if the FAPI state automata
           are in a file I/O state. */
        r = ifapi_io_poll(&context->io);
        return_if_error(r, "Something went wrong with IO polling");

        /* Repeatedly call the finish function, until FAPI has transitioned
           through all execution stages / states of this invocation. */
        r = Fapi_Sign_Finish(context, signature, signatureSize, publicKey,
                              certificate);
    } while (base_rc(r) == TSS2_BASE_RC_TRY_AGAIN);

    /* Reset the ESYS timeout to non-blocking, immediate response. */
    r2 = Esys_SetTimeout(context->esys, 0);
    return_if_error(r2, "Set Timeout to non-blocking");

    return_if_error_reset_state(r, "Key_Sign");

    LOG_TRACE("finished");
    return TSS2_RC_SUCCESS;
}

/** Asynchronous function for Fapi_Sign
 *
 * Uses a key, identified by its path, to sign a digest and puts the result in a
 * TPM2B bytestream.
 *
 * Call Fapi_Sign_Finish to finish the execution of this command.
 *
 * @param[in,out] context The FAPI_CONTEXT
 * @param[in] keyPath The path of the signature key
 * @param[in] padding A padding algorithm. Must be either "RSA_SSA" or
 *            "RSA_PSS" or NULL
 * @param[in] digest The digest to sign. Must be already hashed
 * @param[in] digestSize The size of the digest in bytes
 *
 * @retval TSS2_RC_SUCCESS: if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE: if context, keyPath or digest
 *         is NULL.
 * @retval TSS2_FAPI_RC_BAD_CONTEXT: if context corruption is detected.
 * @retval TSS2_FAPI_RC_KEY_NOT_FOUND: if keyPath does not map to a FAPI key.
 * @retval TSS2_FAPI_RC_BAD_KEY: if the object at keyPath is not a key, or is a
 *         key that is unsuitable for the requested operation.
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
Fapi_Sign_Async(
    FAPI_CONTEXT  *context,
    char    const *keyPath,
    char    const *padding,
    uint8_t const *digest,
    size_t         digestSize)
{
    LOG_TRACE("called for context:%p", context);
    LOG_TRACE("keyPath: %s", keyPath);
    LOG_TRACE("padding: %s", padding);
    if (digest) {
        LOGBLOB_TRACE(digest, digestSize, "digest");
    } else {
        LOG_TRACE("digest: (null) digestSize: %zi", digestSize);
    }

    TSS2_RC r;

    /* Check for NULL parameters */
    check_not_null(context);
    check_not_null(keyPath);
    check_not_null(digest);

    /* Check for invalid parameters */
    if (padding) {
        if (strcasecmp("RSA_SSA", padding) != 0 &&
                strcasecmp("RSA_PSS", padding) != 0) {
            return_error(TSS2_FAPI_RC_BAD_VALUE,
                    "Only padding RSA_SSA or RSA_PSS allowed.");
        }
    }

    /* Helpful alias pointers */
    IFAPI_Key_Sign * command = &context->Key_Sign;

    /* Reset all context-internal session state information. */
    r = ifapi_session_init(context);
    return_if_error(r, "Initialize Sign");

    /* Copy parameters to context for use during _Finish. */
    FAPI_COPY_DIGEST(&command->digest.buffer[0],
                     command->digest.size, digest, digestSize);
    strdup_check(command->keyPath, keyPath, r, error_cleanup);
    strdup_check(command->padding, padding, r, error_cleanup);

    /* Initialize the context state for this operation. */
    context->state = KEY_SIGN_WAIT_FOR_KEY;
    LOG_TRACE("finished");
    return TSS2_RC_SUCCESS;

error_cleanup:
    /* Cleanup duplicated input parameters that were copied before. */
    SAFE_FREE(command->keyPath);
    SAFE_FREE(command->padding);
    return r;
}

/** Asynchronous finish function for Fapi_Sign
 *
 * This function should be called after a previous Fapi_Sign_Async.
 *
 * @param[in,out] context The FAPI_CONTEXT
 * @param[out] signature The signature
 * @param[out] signatureSize The size of signature in bytes. May be NULL
 * @param[out] publicKey The public key that can be used to verify signature
 *            in PEM format. May be NULL
 * @param[out] certificate The certificate associated with the signing key in PEM
 *            format. May be NULL
 *
 * @retval TSS2_RC_SUCCESS: if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE: if context or signature is NULL.
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
Fapi_Sign_Finish(
    FAPI_CONTEXT *context,
    uint8_t     **signature,
    size_t       *signatureSize,
    char        **publicKey,
    char        **certificate)
{
    LOG_TRACE("called for context:%p", context);

    TSS2_RC r;
    size_t resultSignatureSize;

    /* Check for NULL parameters */
    check_not_null(context);
    check_not_null(signature);

    /* Helpful alias pointers */
    IFAPI_Key_Sign * command = &context->Key_Sign;

    switch (context->state) {
        statecase(context->state, KEY_SIGN_WAIT_FOR_KEY);
            /* Load the key used for signing with a helper. */
            r = ifapi_load_key(context, command->keyPath,
                               &command->key_object);
            return_try_again(r);
            goto_if_error(r, "Fapi load key.", cleanup);

            fallthrough;

        statecase(context->state, KEY_SIGN_WAIT_FOR_SIGN);
            /* Perform the signing operation using a helper. */
            r = ifapi_key_sign(context, command->key_object,
                    command->padding, &command->digest, &command->tpm_signature,
                    &command->publicKey,
                    (certificate) ? &command->certificate : NULL);
            return_try_again(r);
            goto_if_error(r, "Fapi sign.", cleanup);

            /* Convert the TPM datatype signature to something useful for the caller. */
            r = ifapi_tpm_to_fapi_signature(command->key_object,
                     command->tpm_signature, &command->ret_signature, &resultSignatureSize);
            goto_if_error(r, "Create FAPI signature.", cleanup);

            if (signatureSize)
                command->signatureSize = resultSignatureSize;
            fallthrough;

        statecase(context->state, KEY_SIGN_CLEANUP)
            /* Cleanup the session used for authorization. */
            r = ifapi_cleanup_session(context);
            try_again_or_error_goto(r, "Cleanup", cleanup);

            if (certificate)
                *certificate = command->certificate;
            if (signatureSize)
                *signatureSize = command->signatureSize;
            if (publicKey)
                *publicKey = command->publicKey;
            *signature = command->ret_signature;
            context->state = _FAPI_STATE_INIT;
            break;

        statecasedefault(context->state);
    }

 cleanup:
    /* Cleanup any intermediate results and state stored in the context. */
    ifapi_cleanup_ifapi_object(command->key_object);
    ifapi_cleanup_ifapi_object(&context->loadKey.auth_object);
    ifapi_cleanup_ifapi_object(context->loadKey.key_object);
    SAFE_FREE(command->tpm_signature);
    SAFE_FREE(command->keyPath);
    SAFE_FREE(command->padding);
    ifapi_session_clean(context);
    ifapi_cleanup_ifapi_object(&context->createPrimary.pkey_object);
    LOG_TRACE("finished");
    return r;
}
