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
#include "ifapi_json_serialize.h"
#include "fapi_policy.h"
#define LOGMODULE fapi
#include "util/log.h"
#include "util/aux_util.h"
#include "fapi_crypto.h"

#define IV_SIZE 16

/** One-Call function for Fapi_Encrypt
 *
 * Encrypt the provided data for the target key using the TPM encryption
 * schemes as specified in the crypto profile.
 * This function does not use the TPM; i.e. works in non-TPM mode.
 *
 * @param[in,out] context The FAPI_CONTEXT
 * @param[in] keyPath THe path to the encryption key
 * @param[in] plainText The plaintext data to encrypt
 * @param[in] plainTextSize The size of the plainText in bytes
 * @param[out] cipherText The encoded cipher text.
 * @param[out] cipherTextSize The size of the encoded cipher text.
 *
 * @retval TSS2_RC_SUCCESS: if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE: if context, keyPath, plainText, or
 *         cipherText is NULL.
 * @retval TSS2_FAPI_RC_BAD_CONTEXT: if context corruption is detected.
 * @retval TSS2_FAPI_RC_KEY_NOT_FOUND: if keyPath does not map to a FAPI key.
 * @retval TSS2_FAPI_RC_BAD_KEY: if the key at keyPath is unsuitable for
 *         encryption.
 * @retval TSS2_FAPI_RC_BAD_VALUE: if plainTextSize is 0.
 * @retval TSS2_FAPI_RC_BAD_SEQUENCE: if the context has an asynchronous
 *         operation already pending.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory for
 *         internal operations or return parameters.
 * @retval TSS2_FAPI_RC_NO_TPM if FAPI was initialized in no-TPM-mode via its
 *         config file.
 * @retval TSS2_FAPI_RC_IO_ERROR if an error occurred while accessing the
 *         object store.
 * @retval TSS2_FAPI_RC_NOT_IMPLEMENTED if the encryption algorithm is not available.
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
Fapi_Encrypt(
    FAPI_CONTEXT  *context,
    char    const *keyPath,
    uint8_t const *plainText,
    size_t         plainTextSize,
    uint8_t      **cipherText,
    size_t        *cipherTextSize)
{
    LOG_TRACE("called for context:%p", context);

    TSS2_RC r, r2;

    /* Check for NULL parameters */
    check_not_null(context);
    check_not_null(keyPath);
    check_not_null(plainText);
    check_not_null(cipherText);

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

    r = Fapi_Encrypt_Async(context, keyPath, plainText, plainTextSize);
    return_if_error_reset_state(r, "Data_Encrypt");

    do {
        /* We wait for file I/O to be ready if the FAPI state automata
           are in a file I/O state. */
        r = ifapi_io_poll(&context->io);
        return_if_error(r, "Something went wrong with IO polling");

        /* Repeatedly call the finish function, until FAPI has transitioned
           through all execution stages / states of this invocation. */
        r = Fapi_Encrypt_Finish(context, cipherText, cipherTextSize);
    } while (base_rc(r) == TSS2_BASE_RC_TRY_AGAIN);

    /* Reset the ESYS timeout to non-blocking, immediate response. */
    r2 = Esys_SetTimeout(context->esys, 0);
    return_if_error(r2, "Set Timeout to non-blocking");

    return_if_error_reset_state(r, "Data_Encrypt");

    LOG_TRACE("finished");
    return TSS2_RC_SUCCESS;
}

/** Asynchronous function for Fapi_Encrypt
 *
 * Encrypt the provided data for the target key using the TPM encryption
 * schemes as specified in the crypto profile.
 * This function does not use the TPM; i.e. works in non-TPM mode.
 *
 * Call Fapi_Encrypt_Finish to finish the execution of this command.
 *
 * @param[in,out] context The FAPI_CONTEXT
 * @param[in] keyPath The path to the encryption key
 * @param[in] plainText The plainText data to encrypt
 * @param[in] plainTextSize The size of the plainText in bytes
 *
 * @retval TSS2_RC_SUCCESS: if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE: if context, keyPath or plainText is
 *         NULL.
 * @retval TSS2_FAPI_RC_BAD_CONTEXT: if context corruption is detected.
 * @retval TSS2_FAPI_RC_KEY_NOT_FOUND: if keyPath does not map to a FAPI key.
 * @retval TSS2_FAPI_RC_BAD_KEY: if the key at keyPath is unsuitable for
 *         encryption.
 * @retval TSS2_FAPI_RC_BAD_VALUE: if plainTextSize is 0.
 * @retval TSS2_FAPI_RC_BAD_SEQUENCE: if the context has an asynchronous
 *         operation already pending.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory for
 *         internal operations or return parameters.
 * @retval TSS2_FAPI_RC_NO_TPM if FAPI was initialized in no-TPM-mode via its
 *         config file.
 */
TSS2_RC
Fapi_Encrypt_Async(
    FAPI_CONTEXT  *context,
    char    const *keyPath,
    uint8_t const *plainText,
    size_t         plainTextSize)
{
    LOG_TRACE("called for context:%p", context);
    LOG_TRACE("keyPath: %s", keyPath);
    if (plainText) {
        LOGBLOB_TRACE(plainText, plainTextSize, "plainText");
    } else {
        LOG_TRACE("plainText: (null) plainTextSize: %zi", plainTextSize);
    }

    TSS2_RC r;

    /* Check for NULL parameters */
    check_not_null(context);
    check_not_null(keyPath);
    check_not_null(plainText);

    /* Helpful alias pointers */
    IFAPI_Data_EncryptDecrypt * command = &(context->cmd.Data_EncryptDecrypt);

    r = ifapi_session_init(context);
    return_if_error(r, "Initialize Encrypt");

    /* Copy parameters to context for use during _Finish. */
    uint8_t *inData = malloc(plainTextSize);
    goto_if_null(inData, "Out of memory", r, error_cleanup);
    memcpy(inData, plainText, plainTextSize);
    command->in_data = inData;

    strdup_check(command->keyPath, keyPath, r, error_cleanup);

    command->in_dataSize = plainTextSize;
    command->key_handle = ESYS_TR_NONE;
    command->cipherText = NULL;

    /* Initialize the context state for this operation. */
    context->state = DATA_ENCRYPT_WAIT_FOR_PROFILE;
    LOG_TRACE("finished");
    return TSS2_RC_SUCCESS;

error_cleanup:
    SAFE_FREE(inData);
    SAFE_FREE(command->keyPath);
    return r;
}

/** Asynchronous finish function for Fapi_Encrypt
 *
 * This function should be called after a previous Fapi_Encrypt_Async.
 *
 * @param[in,out] context The FAPI_CONTEXT
 * @param[out] cipherText The encoded ciphertext
 * @param[out] cipherTextSize The size of the encoded cipher text.
 *
 * @retval TSS2_RC_SUCCESS: if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE: if context or ciphertext is NULL.
 * @retval TSS2_FAPI_RC_BAD_CONTEXT: if context corruption is detected.
 * @retval TSS2_FAPI_RC_BAD_SEQUENCE: if the context has an asynchronous
 *         operation already pending.
 * @retval TSS2_FAPI_RC_IO_ERROR: if the data cannot be saved.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory for
 *         internal operations or return parameters.
 * @retval TSS2_FAPI_RC_TRY_AGAIN: if the asynchronous operation is not yet
 *         complete. Call this function again later.
 * @retval TSS2_FAPI_RC_NOT_IMPLEMENTED if the encryption algorithm is not available.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_PATH_NOT_FOUND if a FAPI object path was not found
 *         during authorization.
 * @retval TSS2_FAPI_RC_KEY_NOT_FOUND if a key was not found.
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
Fapi_Encrypt_Finish(
    FAPI_CONTEXT  *context,
    uint8_t      **cipherText,
    size_t        *cipherTextSize)
{
    LOG_TRACE("called for context:%p", context);

    TSS2_RC r;

    /* Check for NULL parameters */
    check_not_null(context);
    check_not_null(cipherText);

    /* Helpful alias pointers */
    IFAPI_Data_EncryptDecrypt * command = &context->cmd.Data_EncryptDecrypt;
    IFAPI_OBJECT *encKeyObject;
    TPM2B_PUBLIC_KEY_RSA *tpmCipherText = NULL;

    switch (context->state) {
        statecase(context->state, DATA_ENCRYPT_WAIT_FOR_PROFILE);
            /* Retrieve the profile for the provided key in order to get the
               encryption scheme below. */
            r = ifapi_profiles_get(&context->profiles, command->keyPath,
                                   &command->profile);
            return_try_again(r);
            goto_if_error_reset_state(r, " FAPI create session", error_cleanup);

            /* Initialize a session used for authorization and parameter encryption. */
            r = ifapi_get_sessions_async(context,
                                         IFAPI_SESSION_GENEK | IFAPI_SESSION1,
                                         TPMA_SESSION_ENCRYPT | TPMA_SESSION_DECRYPT, 0);
            goto_if_error_reset_state(r, "Create sessions", error_cleanup);

            fallthrough;

        statecase(context->state, DATA_ENCRYPT_WAIT_FOR_SESSION);
        r = ifapi_get_sessions_finish(context, &context->profiles.default_profile,
                                      context->profiles.default_profile.nameAlg);
            return_try_again(r);
            goto_if_error(r, "Get session.", error_cleanup);

            /* Load the reference key by loading all of its parents starting from the SRK. */
            r = ifapi_load_keys_async(context, command->keyPath);
            goto_if_error(r, "Load keys.", error_cleanup);

            fallthrough;

        statecase(context->state, DATA_ENCRYPT_WAIT_FOR_KEY);
            r = ifapi_load_keys_finish(context, IFAPI_FLUSH_PARENT,
                                       &command->key_handle,
                                       &command->key_object);
            return_try_again(r);
            goto_if_error_reset_state(r, " Load key.", error_cleanup);

            encKeyObject = command->key_object;

            if (encKeyObject->misc.key.public.publicArea.type == TPM2_ALG_RSA) {
                TPM2B_DATA null_data = { .size = 0, .buffer = {} };
                TPM2B_PUBLIC_KEY_RSA *rsa_message = (TPM2B_PUBLIC_KEY_RSA *)&context->aux_data;
                size_t key_size =
                    encKeyObject->misc.key.public.publicArea.parameters.rsaDetail.keyBits / 8;
                if (context->cmd.Data_EncryptDecrypt.in_dataSize > key_size) {
                    goto_error_reset_state(r, TSS2_FAPI_RC_BAD_VALUE,
                                           "Size to big for RSA encryption.", error_cleanup);
                }
                rsa_message->size = context->cmd.Data_EncryptDecrypt.in_dataSize;
                memcpy(&rsa_message->buffer[0], context->cmd.Data_EncryptDecrypt.in_data,
                       context->cmd.Data_EncryptDecrypt.in_dataSize);

                /* Received plain text will be encrypted */
                r = Esys_TRSess_SetAttributes(context->esys, context->session1,
                                              TPMA_SESSION_CONTINUESESSION |  TPMA_SESSION_DECRYPT,
                                                  0xff);
                goto_if_error_reset_state(r, "Set session attributes.", error_cleanup);

                r = Esys_RSA_Encrypt_Async(context->esys,
                                           context->cmd.Data_EncryptDecrypt.key_handle,
                                           context->session1, ESYS_TR_NONE, ESYS_TR_NONE,
                                           rsa_message,
                                           &command->profile->rsa_decrypt_scheme,
                                           &null_data);
                goto_if_error(r, "Error esys rsa encrypt", error_cleanup);

                context-> state = DATA_ENCRYPT_WAIT_FOR_RSA_ENCRYPTION;
            } else if (encKeyObject->misc.key.public.publicArea.type == TPM2_ALG_ECC) {
                goto_error(r, TSS2_FAPI_RC_NOT_IMPLEMENTED,
                           "ECC Encryption not yet supported", error_cleanup);
            } else {
                goto_error(r, TSS2_FAPI_RC_NOT_IMPLEMENTED,
                           "Unsupported algorithm (%" PRIu16 ")",
                           error_cleanup, encKeyObject->misc.key.public.publicArea.type);
            }
            fallthrough;

        statecase(context->state, DATA_ENCRYPT_WAIT_FOR_RSA_ENCRYPTION);
            r = Esys_RSA_Encrypt_Finish(context->esys, &tpmCipherText);
            return_try_again(r);
            if (r == 0x00000084) {
                LOG_ERROR("The data to be encrypted might be too large. Common values are "
                          "256 bytes for no OAEP or 190 with OAEP.");
            }
            goto_if_error_reset_state(r, "RSA encryption.", error_cleanup);

            /* Return cipherTextSize if requested by the caller. */
            if (cipherTextSize)
                command->cipherTextSize = tpmCipherText->size;

            /* Duplicate the outputs for handling off to the caller. */
            command->cipherText = malloc(tpmCipherText->size);
            goto_if_null2(command->cipherText, "Out of memory", r, TSS2_FAPI_RC_MEMORY,
                          error_cleanup);

            memcpy(command->cipherText, &tpmCipherText->buffer[0], tpmCipherText->size);
            SAFE_FREE(tpmCipherText);

            /* Flush the key from the TPM. */
            if (!command->key_object->misc.key.persistent_handle) {
                r = Esys_FlushContext_Async(context->esys,
                                        command->key_handle);
                goto_if_error(r, "Error: FlushContext", error_cleanup);
            }
            fallthrough;

        statecase(context->state, DATA_ENCRYPT_WAIT_FOR_FLUSH);
            if (!command->key_object->misc.key.persistent_handle) {
                r = Esys_FlushContext_Finish(context->esys);
                return_try_again(r);

                goto_if_error(r, "Error: FlushContext", error_cleanup);
            }
            command->key_handle = ESYS_TR_NONE;
            fallthrough;

        statecase(context->state, DATA_ENCRYPT_CLEAN)
            /* Cleanup the sessions. */
            r = ifapi_cleanup_session(context);
            try_again_or_error_goto(r, "Cleanup", error_cleanup);

            *cipherText = command->cipherText;
            if (cipherTextSize)
                *cipherTextSize = command->cipherTextSize;
            break;

        statecasedefault(context->state);
    }

    context->state = _FAPI_STATE_INIT;

error_cleanup:
    /* Cleanup any intermediate results and state stored in the context. */
    if (command->key_handle != ESYS_TR_NONE)
        Esys_FlushContext(context->esys,  command->key_handle);
    if (r)
        SAFE_FREE(command->cipherText);
    ifapi_cleanup_ifapi_object(&context->loadKey.auth_object);
    ifapi_cleanup_ifapi_object(context->loadKey.key_object);
    ifapi_cleanup_ifapi_object(&context->createPrimary.pkey_object);
    ifapi_cleanup_ifapi_object(command->key_object);
    SAFE_FREE(tpmCipherText);
    SAFE_FREE(command->keyPath);
    SAFE_FREE(command->in_data);
    ifapi_session_clean(context);
    LOG_TRACE("finished");
    return r;
}
