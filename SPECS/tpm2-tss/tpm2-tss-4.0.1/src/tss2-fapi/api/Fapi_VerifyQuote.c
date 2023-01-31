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
#include "fapi_crypto.h"
#define LOGMODULE fapi
#include "util/log.h"
#include "util/aux_util.h"

/** One-Call function for Fapi_VerifyQuote
 *
 * Verifies that the data returned by a quote is valid.
 *
 * @param[in,out] context The FAPI_CONTEXT
 * @param[in] publicKeyPath The path to the signing key
 * @param[in] qualifyingData The qualifying data nonce. May be NULL
 * @param[in] qualifyingDataSize The size of qualifyingData in bytes. Must be 0
 *            if qualifyingData is NULL
 * @param[in] quoteInfo The quote information
 * @param[in] signature The quote's signature
 * @param[in] signatureSize The size of signature in bytes
 * @param[in] pcrLog The PCR's log. May be NULL
 *
 * @retval TSS2_RC_SUCCESS: if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE: if context, publicKeyPath, quoteInfo,
 *         or signature is NULL.
 * @retval TSS2_FAPI_RC_BAD_CONTEXT: if context corruption is detected.
 * @retval TSS2_FAPI_RC_KEY_NOT_FOUND: if path does not map to a FAPI entity.
 * @retval TSS2_FAPI_RC_BAD_KEY: if the entity at path is not a key, or is a key
 *         that is unsuitable for the requested operation.
 * @retval TSS2_FAPI_RC_BAD_VALUE: if quoteInfo, pcrEventLog, qualifyingData, or
 *         signature is invalid.
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
 * @retval TSS2_FAPI_RC_SIGNATURE_VERIFICATION_FAILED if the signature could not
 *         be verified
 * @retval TSS2_FAPI_RC_NOT_PROVISIONED FAPI was not provisioned.
 * @retval TSS2_FAPI_RC_BAD_PATH if the path is used in inappropriate context
 *         or contains illegal characters.
 */
TSS2_RC
Fapi_VerifyQuote(
    FAPI_CONTEXT  *context,
    char    const *publicKeyPath,
    uint8_t const *qualifyingData,
    size_t         qualifyingDataSize,
    char    const *quoteInfo,
    uint8_t const *signature,
    size_t         signatureSize,
    char           const *pcrLog)
{
    LOG_TRACE("called for context:%p", context);

    TSS2_RC r;

    /* Check for NULL parameters */
    check_not_null(context);
    check_not_null(publicKeyPath);
    check_not_null(quoteInfo);
    check_not_null(signature);

    r = Fapi_VerifyQuote_Async(context, publicKeyPath,
                               qualifyingData, qualifyingDataSize,
                               quoteInfo, signature,
                               signatureSize, pcrLog);
    return_if_error_reset_state(r, "Key_VerifyQuote");

    do {
        /* We wait for file I/O to be ready if the FAPI state automata
           are in a file I/O state. */
        r = ifapi_io_poll(&context->io);
        return_if_error(r, "Something went wrong with IO polling");

        /* Repeatedly call the finish function, until FAPI has transitioned
           through all execution stages / states of this invocation. */
        r = Fapi_VerifyQuote_Finish(context);
    } while (base_rc(r) == TSS2_BASE_RC_TRY_AGAIN);

    return_if_error_reset_state(r, "Key_VerifyQuote");

    LOG_TRACE("finished");
    return TSS2_RC_SUCCESS;
}

/** Asynchronous function for Fapi_VerifyQuote
 *
 * Verifies that the data returned by a quote is valid.
 * Call Fapi_VerifyQuote_Finish to finish the execution of this command.
 *
 * @param[in,out] context The FAPI_CONTEXT
 * @param[in] publicKeyPath The path to the signing key
 * @param[in] qualifyingData The qualifying data nonce. May be NULL
 * @param[in] qualifyingDataSize The size of qualifyingData in bytes. Must be 0
 *            if qualifyingData is NULL
 * @param[in] quoteInfo The quote information
 * @param[in] signature The quote's signature
 * @param[in] signatureSize The size of signature in bytes
 * @param[in] pcrLog The PCR's log. May be NULL
 *
 * @retval TSS2_RC_SUCCESS: if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE: if context, publicKeyPath, quoteInfo,
 *         or signature is NULL.
 * @retval TSS2_FAPI_RC_BAD_CONTEXT: if context corruption is detected.
 * @retval TSS2_FAPI_RC_KEY_NOT_FOUND: if path does not map to a FAPI entity.
 * @retval TSS2_FAPI_RC_BAD_KEY: if the entity at path is not a key, or is a key
 *         that is unsuitable for the requested operation.
 * @retval TSS2_FAPI_RC_BAD_VALUE: if quoteInfo, pcrEventLog, qualifyingData, or
 *         signature is invalid.
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
Fapi_VerifyQuote_Async(
    FAPI_CONTEXT  *context,
    char    const *publicKeyPath,
    uint8_t const *qualifyingData,
    size_t         qualifyingDataSize,
    char    const *quoteInfo,
    uint8_t const *signature,
    size_t         signatureSize,
    char    const *pcrLog)
{
    LOG_TRACE("called for context:%p", context);
    LOG_TRACE("publicKeyPath: %s", publicKeyPath);
    if (qualifyingData) {
        LOGBLOB_TRACE(qualifyingData, qualifyingDataSize, "qualifyingData");
    } else {
        LOG_TRACE("qualifyingData: (null) qualifyingDataSize: %zi", qualifyingDataSize);
    }
    LOG_TRACE("quoteInfo: %s", quoteInfo);
    if (signature) {
        LOGBLOB_TRACE(signature, signatureSize, "signature");
    } else {
        LOG_TRACE("signature: (null) signatureSize: %zi", signatureSize);
    }
    LOG_TRACE("pcrLog: %s", pcrLog);

    TSS2_RC r;

    /* Check for NULL parameters */
    check_not_null(context);
    check_not_null(publicKeyPath);
    check_not_null(quoteInfo);
    check_not_null(signature);

    /* Check for invalid parameters */
    if (qualifyingData == NULL && qualifyingDataSize != 0) {
        LOG_ERROR("qualifyingData is NULL but qualifyingDataSize is not 0");
        return TSS2_FAPI_RC_BAD_VALUE;
    }

    /* Helpful alias pointers */
    IFAPI_PCR * command = &context->cmd.pcr;

    if (qualifyingDataSize > sizeof(command->qualifyingData.buffer)) {
        return_error(TSS2_FAPI_RC_BAD_VALUE, "qualifyingDataSize too large.");
    }

    r = ifapi_non_tpm_mode_init(context);
    return_if_error(r, "Initialize VerifyQuote");

    /* Copy parameters to context for use during _Finish. */
    uint8_t * signatureBuffer = malloc(signatureSize);
    goto_if_null2(signatureBuffer, "Out of memory",
            r, TSS2_FAPI_RC_MEMORY, error_cleanup);
    memcpy(signatureBuffer, signature, signatureSize);
    command->signature = signatureBuffer;
    command->signatureSize = signatureSize;

    strdup_check(command->keyPath, publicKeyPath, r, error_cleanup);
    strdup_check(command->quoteInfo, quoteInfo, r, error_cleanup);
    strdup_check(command->logData, pcrLog, r, error_cleanup);
    command->event_list = NULL;

    if (qualifyingData != NULL) {
        FAPI_COPY_DIGEST(&command->qualifyingData.buffer[0],
                command->qualifyingData.size,
                qualifyingData, qualifyingDataSize);
    } else {
        command->qualifyingData.size = 0;
    }

    /* Load the key for verification from the keystore. */
    r = ifapi_keystore_load_async(&context->keystore, &context->io, publicKeyPath);
    goto_if_error(r, "Could not open publicKeyPath", error_cleanup);

    /* Initialize the context state for this operation. */
    context->state = VERIFY_QUOTE_READ;
    LOG_TRACE("finished");
    return TSS2_RC_SUCCESS;

error_cleanup:
    /* Cleanup duplicated input parameters that were copied before. */
    SAFE_FREE(command->keyPath);
    SAFE_FREE(signatureBuffer);
    command->signature = NULL;
    SAFE_FREE(command->quoteInfo);
    SAFE_FREE(command->logData);
    return r;
}

/** Asynchronous finish function for Fapi_VerifyQuote
 *
 * This function should be called after a previous Fapi_VerifyQuote_Async.
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
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE if an internal error occurred.
 * @retval TSS2_FAPI_RC_SIGNATURE_VERIFICATION_FAILED if the signature could not
 *         be verified
 */
TSS2_RC
Fapi_VerifyQuote_Finish(
    FAPI_CONTEXT  *context)
{
    LOG_TRACE("called for context:%p", context);

    TSS2_RC r;
    IFAPI_OBJECT key_object;
    TPM2B_ATTEST attest2b;
    TPM2B_DIGEST pcr_digest;

    /* Check for NULL parameters */
    check_not_null(context);

    /* Helpful alias pointers */
    IFAPI_PCR * command = &context->cmd.pcr;

    memset(&key_object, 0, sizeof(IFAPI_OBJECT));

    switch (context->state) {
        statecase(context->state, VERIFY_QUOTE_READ);
            r = ifapi_keystore_load_finish(&context->keystore, &context->io, &key_object);
            return_try_again(r);
            goto_if_error_reset_state(r, "read_finish failed", error_cleanup);

            /* Recalculate the quote-info and attest2b buffer. */
            r = ifapi_get_quote_info(command->quoteInfo, &attest2b,
                                     &command->fapi_quote_info);
            goto_if_error(r, "Get quote info.", error_cleanup);

            /* Verify the signature over the attest2b structure. */
            r = ifapi_verify_signature_quote(&key_object,
                                             command->signature,
                                             command->signatureSize,
                                             &attest2b.attestationData[0],
                                             attest2b.size,
                                             &command->fapi_quote_info.sig_scheme);
            goto_if_error(r, "Verify signature.", error_cleanup);

            /* Check qualifying data */
            if (command->qualifyingData.size != command->fapi_quote_info.attest.extraData.size ||
                memcmp(&command->qualifyingData.buffer[0],
                       &command->fapi_quote_info.attest.extraData.buffer[0],
                       command->qualifyingData.size) != 0) {
                context->state = _FAPI_STATE_INIT;
                goto_error(r, TSS2_FAPI_RC_SIGNATURE_VERIFICATION_FAILED,
                           "Invalid qualifying data for quote", error_cleanup);
            }

            /* If no logData was provided then the operation is done. */
            if (!command->logData) {
                context->state = _FAPI_STATE_INIT;
                break;
            }

            /* If logData was provided then the pcr_digests need to be recalculated
               and verified against the quote_info. */

            /* Parse the logData JSON. */
            command->event_list = json_tokener_parse(context->cmd.pcr.logData);
            if (!command->event_list) {
                goto_error(r, TSS2_FAPI_RC_BAD_VALUE, "Bad value for logData", error_cleanup);
            }

            /* Recalculate and verify the PCR digests. */
            r = ifapi_calculate_pcr_digest(command->event_list,
                                           &command->fapi_quote_info, &pcr_digest);

            goto_if_error(r, "Verify event list.", error_cleanup);

            context->state = _FAPI_STATE_INIT;
            break;

        statecasedefault(context->state);
    }

error_cleanup:
    /* Cleanup any intermediate results and state stored in the context. */
    if (key_object.objectType)
        ifapi_cleanup_ifapi_object(&key_object);
    if (command->event_list)
        json_object_put(command->event_list);
    ifapi_cleanup_ifapi_object(&context->loadKey.auth_object);
    ifapi_cleanup_ifapi_object(context->loadKey.key_object);
    ifapi_cleanup_ifapi_object(&context->createPrimary.pkey_object);
    SAFE_FREE(command->keyPath);
    SAFE_FREE(command->signature);
    SAFE_FREE(command->quoteInfo);
    SAFE_FREE(command->logData);
    LOG_TRACE("finished");
    return r;
}
