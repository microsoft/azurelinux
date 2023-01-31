/* SPDX-License-Identifier: BSD-2-Clause */
/*******************************************************************************
 * Copyright 2018-2019, Fraunhofer SIT sponsored by Infineon Technologies AG
 * All rights reserved.
 ******************************************************************************/

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <stdio.h>
#include <string.h>

#include "tss2_fapi.h"
#include "fapi_int.h"
#include "fapi_util.h"
#include "tss2_esys.h"
#define LOGMODULE fapi
#include "util/log.h"
#include "util/aux_util.h"

/** One-Call function for Fapi_Quote
 *
 * Given a set of PCRs and a restricted signing key, it will sign those PCRs and
 * return the quote.
 *
 * @param[in,out] context The FAPI_CONTEXT
 * @param[in] pcrList The list of PCRs that are to be quoted
 * @param[in] pcrListSize The size of pcrList in bytes
 * @param[in] keyPath The path to the signing key
 * @param[in] quoteType The type of quote. May be NULL
 * @param[in] qualifyingData A nonce provided by the caller. May be NULL
 * @param[in] qualifyingDataSize The size of qualifyingData in bytes. Must be 0
 *            if qualifyingData is NULL
 * @param[out] quoteInfo A JSON-encoded structure holding the inputs to the
 *             quote operation
 * @param[out] signature The signature of the PCRs
 * @param[out] signatureSize The size of the signature in bytes. May be NULL
 * @param[out] pcrLog The log of the PCR. May be NULL
 * @param[out] certificate The certificate associated with the signing key. May
 *             be NULL
 *
 * @retval TSS2_RC_SUCCESS: if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE: if context, pcrList, keyPath,
 *         quoteInfo or signature is NULL.
 * @retval TSS2_FAPI_RC_BAD_CONTEXT: if context corruption is detected.
 * @retval TSS2_FAPI_RC_KEY_NOT_FOUND: if path does not map to a FAPI entity.
 * @retval TSS2_FAPI_RC_BAD_KEY: if the entity at path is not a key, or is a key
 *         that is unsuitable for the requested operation.
 * @retval TSS2_FAPI_RC_BAD_VALUE: if qualifyingData is invalid or if
 *         qualifyingDataSize is zero.
 * @retval TSS2_FAPI_RC_IO_ERROR: if the data cannot be saved.
 * @retval TSS2_FAPI_RC_BAD_SEQUENCE: if the context has an asynchronous
 *         operation already pending.
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
Fapi_Quote(
    FAPI_CONTEXT   *context,
    uint32_t       *pcrList,
    size_t          pcrListSize,
    char     const *keyPath,
    char     const *quoteType,
    uint8_t  const *qualifyingData,
    size_t          qualifyingDataSize,
    char          **quoteInfo,
    uint8_t       **signature,
    size_t         *signatureSize,
    char          **pcrLog,
    char          **certificate)
{
    LOG_TRACE("called for context:%p", context);

    TSS2_RC r, r2;

    /* Check for NULL parameters */
    check_not_null(context);
    check_not_null(pcrList);
    check_not_null(keyPath);
    check_not_null(quoteInfo);
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

    r = Fapi_Quote_Async(context, pcrList, pcrListSize, keyPath, quoteType,
                         qualifyingData, qualifyingDataSize);
    return_if_error_reset_state(r, "PCR_Quote");

    do {
        /* We wait for file I/O to be ready if the FAPI state automata
           are in a file I/O state. */
        r = ifapi_io_poll(&context->io);
        return_if_error(r, "Something went wrong with IO polling");

        /* Repeatedly call the finish function, until FAPI has transitioned
           through all execution stages / states of this invocation. */
        r = Fapi_Quote_Finish(context, quoteInfo, signature, signatureSize,
                               pcrLog, certificate);
    } while (base_rc(r) == TSS2_BASE_RC_TRY_AGAIN);

    /* Reset the ESYS timeout to non-blocking, immediate response. */
    r2 = Esys_SetTimeout(context->esys, 0);
    return_if_error(r2, "Set Timeout to non-blocking");

    return_if_error_reset_state(r, "PCR_Quote");

    LOG_TRACE("finished");
    return TSS2_RC_SUCCESS;
}

/** Asynchronous function for Fapi_Quote
 *
 * Given a set of PCRs and a restricted signing key, it will sign those PCRs and
 * return the quote.
 *
 * Call Fapi_Quote_Finish to finish the execution of this command.
 *
 * @param[in,out] context The FAPI_CONTEXT
 * @param[in] pcrList The list of PCRs that are to be quoted
 * @param[in] pcrListSize The size of pcrList in bytes
 * @param[in] keyPath The path to the signing key
 * @param[in] quoteType The type of quote. May be NULL
 * @param[in] qualifyingData A nonce provided by the caller. May be NULL
 * @param[in] qualifyingDataSize The size of qualifyingData in bytes. Must be 0
 *            if qualifyingData is NULL
 *
 * @retval TSS2_RC_SUCCESS: if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE: if context, pcrList or keyPath
 *         is NULL.
 * @retval TSS2_FAPI_RC_BAD_CONTEXT: if context corruption is detected.
 * @retval TSS2_FAPI_RC_KEY_NOT_FOUND: if path does not map to a FAPI entity.
 * @retval TSS2_FAPI_RC_BAD_KEY: if the entity at path is not a key, or is a key
 *         that is unsuitable for the requested operation.
 * @retval TSS2_FAPI_RC_BAD_VALUE: if pcrListSize is 0, qualifyingData is
 *         invalid or if qualifyingDataSize is zero.
 * @retval TSS2_FAPI_RC_IO_ERROR: if the data cannot be saved.
 * @retval TSS2_FAPI_RC_BAD_SEQUENCE: if the context has an asynchronous
 *         operation already pending.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory for
 *         internal operations or return parameters.
 * @retval TSS2_FAPI_RC_NO_TPM if FAPI was initialized in no-TPM-mode via its
 *         config file.
 */
TSS2_RC
Fapi_Quote_Async(
    FAPI_CONTEXT   *context,
    uint32_t       *pcrList,
    size_t          pcrListSize,
    char     const *keyPath,
    char     const *quoteType,
    uint8_t  const *qualifyingData,
    size_t          qualifyingDataSize)
{
    LOG_TRACE("called for context:%p", context);
    LOG_TRACE("pcrListSize: %zi", pcrListSize);
    for (size_t i = 0; i < pcrListSize; i++) {
        LOG_TRACE("PCR list entry %zu: %ul", i, pcrList[i]);
    }
    LOG_TRACE("keyPath: %s", keyPath);
    LOG_TRACE("quoteType: %s", quoteType);
    if (qualifyingData) {
        LOGBLOB_TRACE(qualifyingData, qualifyingDataSize, "qualifyingData");
    } else {
        LOG_TRACE("qualifyingData: (null) qualifyingDataSize: %zi", qualifyingDataSize);
    }

    TSS2_RC r;

    /* Check for NULL parameters */
    check_not_null(context);
    check_not_null(pcrList);
    check_not_null(keyPath);

    /* Check for invalid parameters */
    if (pcrListSize == 0) {
        LOG_ERROR("pcrListSize must not be NULL");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    if (qualifyingData == NULL && qualifyingDataSize) {
        LOG_ERROR("QualifyingData is NULL but qualifyingDataSize is not 0");
        return TSS2_FAPI_RC_BAD_VALUE;
    }

    /* Helpful alias pointers */
    IFAPI_PCR * command = &context->cmd.pcr;

    if (qualifyingDataSize > sizeof(command->qualifyingData.buffer)) {
        return_error(TSS2_FAPI_RC_BAD_VALUE, "qualifyingDataSize too large.");
    }

    /* Reset all context-internal session state information. */
    r = ifapi_session_init(context);
    return_if_error(r, "Initialize Quote");
    memset(&context->cmd.pcr, 0, sizeof(IFAPI_PCR));

    if (quoteType && strcmp(quoteType, "TPM-Quote") != 0) {
        return_error(TSS2_FAPI_RC_BAD_VALUE,
                     "Only quote type TPM-Quote is allowed");
    }

    /* Store parameters in context */
    strdup_check(command->keyPath, keyPath, r, error_cleanup);

    command->pcrList = malloc(pcrListSize * sizeof(TPM2_HANDLE));
    goto_if_null2(command->pcrList, "Out of memory", r, TSS2_FAPI_RC_MEMORY,
            error_cleanup);
    memcpy(command->pcrList, pcrList, pcrListSize * sizeof(TPM2_HANDLE));

    command->pcrListSize = pcrListSize;
    command->tpm_quoted = NULL;
    if (qualifyingData != NULL) {
        FAPI_COPY_DIGEST(&command->qualifyingData.buffer[0],
                command->qualifyingData.size, qualifyingData, qualifyingDataSize);
    } else {
        command->qualifyingData.size = 0;
    }

    /* Initialize the context state for this operation. */
    context->state = PCR_QUOTE_WAIT_FOR_GET_CAP;
    command->handle = ESYS_TR_NONE;
    LOG_TRACE("finished");
    return TSS2_RC_SUCCESS;

error_cleanup:
    /* Cleanup duplicated input parameters that were copied before. */
    SAFE_FREE(command->keyPath);
    SAFE_FREE(command->pcrList);
    return r;
}

/** Asynchronous finish function for Fapi_Quote
 *
 * This function should be called after a previous Fapi_Quote_Async.
 *
 * @param[in,out] context The FAPI_CONTEXT
 * @param[out] quoteInfo A JSON-encoded structure holding the inputs to the
 *             quote operation
 * @param[out] signature The signature of the PCRs
 * @param[out] signatureSize The size of the signature in bytes. May be NULL
 * @param[out] pcrLog The log of the PCR. May be NULL
 * @param[out] certificate The certificate associated with the signing key. May
 *             be NULL
 *
 * @retval TSS2_RC_SUCCESS: if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE: if context, quoteInfor or signature
 *         is NULL.
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
Fapi_Quote_Finish(
    FAPI_CONTEXT  *context,
    char         **quoteInfo,
    uint8_t      **signature,
    size_t        *signatureSize,
    char          **pcrLog,
    char          **certificate)
{
    LOG_TRACE("called for context:%p", context);

    TSS2_RC r;
    IFAPI_OBJECT *sig_key_object;
    const IFAPI_PROFILE *profile;
    ESYS_TR auth_session;

    /* Check for NULL parameters */
    check_not_null(context);
    check_not_null(quoteInfo);
    check_not_null(signature);

    /* Helpful alias pointers */
    IFAPI_PCR * command = &context->cmd.pcr;

    switch (context->state) {
        statecase(context->state, PCR_QUOTE_WAIT_FOR_GET_CAP);
            command->pcr_selection = context->profiles.default_profile.pcr_selection;

            r = ifapi_filter_pcr_selection_by_index(&command->pcr_selection,
                                                    command->pcrList,
                                                    command->pcrListSize);
            goto_if_error_reset_state(r, "A selected PCR has no bank associated in the"
                                      "current cryptographic profile.", error_cleanup);

            /* Get a session for authorization of the quote operation. */
            r = ifapi_get_sessions_async(context,
                                         IFAPI_SESSION_GENEK | IFAPI_SESSION1,
                                         TPMA_SESSION_DECRYPT, 0);
            goto_if_error_reset_state(r, "Create sessions", error_cleanup);

            fallthrough;

        statecase(context->state, PCR_QUOTE_WAIT_FOR_SESSION);
            /* Retrieve the profile information. */
            r = ifapi_profiles_get(&context->profiles, command->keyPath, &profile);
            goto_if_error_reset_state(r, " FAPI create session", error_cleanup);

            r = ifapi_get_sessions_finish(context, profile, profile->nameAlg);
            return_try_again(r);
            goto_if_error_reset_state(r, " FAPI create session", error_cleanup);

            /* Load the key into the TPM. */
            r = ifapi_load_keys_async(context, command->keyPath);
            goto_if_error(r, "Load keys.", error_cleanup);

            fallthrough;

        statecase(context->state, PCR_QUOTE_WAIT_FOR_KEY);
            r = ifapi_load_keys_finish(context, IFAPI_FLUSH_PARENT,
                                       &command->handle,
                                       &command->key_object);
            return_try_again(r);
            goto_if_error_reset_state(r, " Load key.", error_cleanup);

            fallthrough;

        statecase(context->state, PCR_QUOTE_AUTHORIZE);
            /* Authorize the session for use with the key. */
            r = ifapi_authorize_object(context, command->key_object, &auth_session);
            return_try_again(r);
            goto_if_error(r, "Authorize key.", error_cleanup);

            /* Perform the Quote operation. */
            r = Esys_Quote_Async(context->esys, command->handle,
                                 auth_session, ESYS_TR_NONE, ESYS_TR_NONE,
                                 &command->qualifyingData,
                                 &command->key_object->misc.key.signing_scheme,
                                 &command->pcr_selection);
            goto_if_error(r, "Error: PCR_Quote", error_cleanup);

            fallthrough;

        statecase(context->state, PCR_QUOTE_AUTH_SENT);
            command->tpm_signature = NULL;
            SAFE_FREE(command->tpm_signature);
            r = Esys_Quote_Finish(context->esys, &command->tpm_quoted,
                                  &command->tpm_signature);
            return_try_again(r);
            if (r == 0x1D5) {
                LOG_ERROR("qualifyingData is of wrong size; probably larger than"
                          "the TPM's max hash size (32 for SHA256, 64 for SHA512).");
            }
            goto_if_error(r, "Error: PCR_Quote", error_cleanup);

            /* Flush the key used for the quote. */
            r = Esys_FlushContext_Async(context->esys, command->handle);
            goto_if_error(r, "Error: FlushContext", error_cleanup);
            command->handle = ESYS_TR_NONE;

            fallthrough;

        statecase(context->state, PCR_QUOTE_WAIT_FOR_FLUSH);
            r = Esys_FlushContext_Finish(context->esys);
            return_try_again(r);
            goto_if_error(r, "Error: Sign", error_cleanup);

            sig_key_object = command->key_object;
            /* Convert the TPM-encoded signature into something useful for the caller. */
            r = ifapi_tpm_to_fapi_signature(sig_key_object,
                                            command->tpm_signature,
                                            &command->signature, &command->signatureSize);
            SAFE_FREE(command->tpm_signature);
            goto_if_error(r, "Create FAPI signature.", error_cleanup);

            /* Compute the quote info; i.e. the data that was actually
               signed by the TPM. */
            r = ifapi_compute_quote_info(sig_key_object,
                                         command->tpm_quoted,
                                         quoteInfo);
            goto_if_error(r, "Create compute quote info.", error_cleanup);

            /* Return the key's certificate if requested. */
            if (certificate) {
                strdup_check(*certificate, sig_key_object->misc.key.certificate, r, error_cleanup);
            }

            /* If the pcrLog was not requested, the operation is done. */
            if (!pcrLog) {
                context->state = PCR_QUOTE_CLEANUP;
                return TSS2_FAPI_RC_TRY_AGAIN;
            }

            /* Retrieve the eventlog for the PCRs for the quote. */
            r = ifapi_eventlog_get_async(&context->eventlog, &context->io,
                                         command->pcrList,
                                         command->pcrListSize);
            goto_if_error(r, "Error getting event log", error_cleanup);

            fallthrough;

        statecase(context->state, PCR_QUOTE_READ_EVENT_LIST);
            r = ifapi_eventlog_get_finish(&context->eventlog, &context->io,
                                          &command->pcrLog);
            return_try_again(r);
            goto_if_error(r, "Error getting event log", error_cleanup);
            fallthrough;

        statecase(context->state, PCR_QUOTE_CLEANUP)
            /* Cleanup the session used for authorization. */
            r = ifapi_cleanup_session(context);
            try_again_or_error_goto(r, "Cleanup", error_cleanup);

            if (pcrLog)
                *pcrLog = command->pcrLog;
            *signature = command->signature;
            *signatureSize = command->signatureSize;
            context->state = _FAPI_STATE_INIT;
            break;

        statecasedefault(context->state);
    }

error_cleanup:
    /* Cleanup any intermediate results and state stored in the context. */
    SAFE_FREE(command->tpm_signature);
    SAFE_FREE(command->tpm_quoted);
    SAFE_FREE(command->keyPath);
    SAFE_FREE(command->pcrList);
    if (r) {
        SAFE_FREE(command->pcrLog);
        SAFE_FREE(command->signature);
    }
    ifapi_cleanup_ifapi_object(&context->loadKey.auth_object);
    ifapi_cleanup_ifapi_object(context->loadKey.key_object);
    ifapi_cleanup_ifapi_object(&context->createPrimary.pkey_object);
    ifapi_cleanup_ifapi_object(command->key_object);
    ifapi_session_clean(context);
    if (command->handle != ESYS_TR_NONE) {
        Esys_FlushContext(context->esys, command->handle);
    }
    LOG_TRACE("finished");
    return r;
}
