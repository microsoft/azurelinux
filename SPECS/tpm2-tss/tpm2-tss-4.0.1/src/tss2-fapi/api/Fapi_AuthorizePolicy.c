/* SPDX-License-Identifier: BSD-2-Clause */
/*******************************************************************************
 * Copyright 2018-2019, Fraunhofer SIT sponsored by Infineon Technologies AG
 * All rights reserved.
 ******************************************************************************/

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include "tss2_fapi.h"
#include "fapi_int.h"
#include "fapi_util.h"
#include "tss2_esys.h"
#include "fapi_policy.h"
#include "fapi_crypto.h"
#define LOGMODULE fapi
#include "util/log.h"
#include "util/aux_util.h"

/** One-Call function for Fapi_AuthorizePolicy
 *
 * If a current policy happens to be a PolicyAuthorize, then for it to be used,
 * the user must first satisfy a policy authorized by a having been signed (and
 * made into a ticket) by an authorized party.
 *
 * @param[in,out] context The FAPI context
 * @param[in] policyPath The path to the policy file
 * @param[in] keyPath The path to the signing key
 * @param[in] policyRef A byte buffer that is included in the signature. May be
 * 						NULL
 * @param[in] policyRefSize The size of policyRef. Must be 0 if policyRef is
 * 						NULL
 *
 * @retval TSS2_RC_SUCCESS: if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE: if context, policyPath or keyPath
 *         is NULL.
 * @retval TSS2_FAPI_RC_BAD_CONTEXT: if context corruption is detected.
 * @retval TSS2_FAPI_RC_BAD_PATH: if policyPath or keyPath does not
 *         map to a FAPI policy or key object.
 * @retval TSS2_FAPI_RC_BAD_SEQUENCE: if the context has an asynchronous
 *         operation already pending.
 * @retval TSS2_FAPI_RC_IO_ERROR: if the data cannot be saved.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory for
 *         internal operations or return parameters.
 * @retval TSS2_FAPI_RC_NO_TPM if FAPI was initialized in no-TPM-mode via its
 *         config file.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_TRY_AGAIN if an I/O operation is not finished yet and
 *         this function needs to be called again.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE if an internal error occurred.
 * @retval TSS2_FAPI_RC_PATH_NOT_FOUND if a FAPI object path was not found
 *         during authorization.
 * @retval TSS2_FAPI_RC_KEY_NOT_FOUND if a key was not found.
 * @retval TSS2_FAPI_RC_AUTHORIZATION_UNKNOWN if a required authorization callback
 *         is not set.
 * @retval TSS2_FAPI_RC_AUTHORIZATION_FAILED if the authorization attempt fails.
 * @retval TSS2_FAPI_RC_POLICY_UNKNOWN if policy search for a certain policy digest
 *         was not successful.
 * @retval TSS2_ESYS_RC_* possible error codes of ESAPI.
 * @retval TSS2_FAPI_RC_NOT_PROVISIONED FAPI was not provisioned.
 */
TSS2_RC
Fapi_AuthorizePolicy(
    FAPI_CONTEXT  *context,
    char    const *policyPath,
    char    const *keyPath,
    uint8_t const *policyRef,
    size_t         policyRefSize)
{
    TSS2_RC r, r2;

    LOG_TRACE("called for context:%p", context);

    /* Check for NULL parameters */
    check_not_null(context);
    check_not_null(policyPath);
    check_not_null(keyPath);

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

    r = Fapi_AuthorizePolicy_Async(context, policyPath, keyPath,
                                   policyRef, policyRefSize);
    return_if_error_reset_state(r, "Policy_AuthorizeNewpolicy");

    do {
        /* We wait for file I/O to be ready if the FAPI state automata
           are in a file I/O state. */
        r = ifapi_io_poll(&context->io);
        return_if_error(r, "Something went wrong with IO polling");

        /* Repeatedly call the finish function, until FAPI has transitioned
           through all execution stages / states of this invocation. */
        r = Fapi_AuthorizePolicy_Finish(context);
    } while (base_rc(r) == TSS2_BASE_RC_TRY_AGAIN);

    /* Reset the ESYS timeout to non-blocking, immediate response. */
    r2 = Esys_SetTimeout(context->esys, 0);
    return_if_error(r2, "Set Timeout to non-blocking");

    return_if_error_reset_state(r, "PolicyAuthorizeNewPolicy");

    return TSS2_RC_SUCCESS;
}

/** Asynchronous function for Fapi_AuthorizePolicy
 *
 * If a current policy happens to be a PolicyAuthorize, then for it to be used,
 * the user must first satisfy a policy authorized by a having been signed (and
 * made into a ticket) by an authorized party.
 *
 * Call Fapi_AuthorizePolicy_Finish to finish the execution of this command.
 *
 * @param[in,out] context The FAPI context
 * @param[in] policyPath The path to the policy file
 * @param[in] keyPath The path to the signing key
 * @param[in] policyRef A byte buffer that is included in the signature. May be
 * 						NULL
 * @param[in] policyRefSize The size of policyRef. Must be 0 if policyRef is
 * 						NULL
 *
 * @retval TSS2_RC_SUCCESS: if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE: if context, policyPath or keyPath
 *         is NULL.
 * @retval TSS2_FAPI_RC_BAD_CONTEXT: if context corruption is detected.
 * @retval TSS2_FAPI_RC_BAD_PATH: if policyPath or keyPath does not
 *         map to a FAPI policy or key object.
 * @retval TSS2_FAPI_RC_BAD_SEQUENCE: if the context has an asynchronous
 *         operation already pending.
 * @retval TSS2_FAPI_RC_IO_ERROR: if the data cannot be saved.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory for
 *         internal operations or return parameters.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_NO_TPM if FAPI was initialized in no-TPM-mode via its
 *         config file.
 */
TSS2_RC
Fapi_AuthorizePolicy_Async(
    FAPI_CONTEXT  *context,
    char    const *policyPath,
    char    const *keyPath,
    uint8_t const *policyRef,
    size_t         policyRefSize)
{
    LOG_TRACE("called for context:%p", context);
    LOG_TRACE("policyPath: %s", policyPath);
    LOG_TRACE("keyPath: %s", keyPath);
    if (policyRef) {
        LOGBLOB_TRACE(policyRef, policyRefSize, "policyRef");
    } else {
        LOG_TRACE("policyRef: (null) policyRefSize: %zi", policyRefSize);
    }

    TSS2_RC r;
    IFAPI_Fapi_AuthorizePolicy *policy;

    /* Check for NULL parameters */
    check_not_null(context);
    check_not_null(policyPath);
    check_not_null(keyPath);
    if (policyRefSize > 0) {
        check_not_null(policyRef);
    }

    if (policyRefSize > sizeof(policy->policyRef.buffer)) {
        return_error(TSS2_FAPI_RC_BAD_VALUE, "PolicyRef too large.");
    }

    /* Reset all context-internal session state information. */
    r = ifapi_session_init(context);
    return_if_error(r, "Initialize AuthorizePolicy");

    /* Copy parameters to context for use during _Finish. */
    policy = &context->cmd.Policy_AuthorizeNewPolicy;
    strdup_check(policy->policyPath, policyPath, r, error_cleanup);
    strdup_check(policy->signingKeyPath, keyPath, r, error_cleanup);
    if (policyRef) {
        FAPI_COPY_DIGEST(&policy->policyRef.buffer[0],
                         policy->policyRef.size, policyRef, policyRefSize);
    } else {
        policy->policyRef.size = 0;
    }

    /* Initialize the context state for this operation. */
    context->state = AUTHORIZE_NEW_LOAD_KEY;

    LOG_TRACE("finished");
    return TSS2_RC_SUCCESS;

error_cleanup:
    /* Cleanup duplicated input parameters that were copied before. */
    SAFE_FREE(policy->policyPath);
    SAFE_FREE(policy->signingKeyPath);
    return r;
}

/** Asynchronous finish function for Fapi_AuthorizePolicy
 *
 * This function should be called after a previous Fapi_AuthorizePolicy_Async.
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
 * @retval TSS2_FAPI_RC_PATH_NOT_FOUND if a FAPI object path was not found
 *         during authorization.
 * @retval TSS2_FAPI_RC_KEY_NOT_FOUND if a key was not found.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
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
Fapi_AuthorizePolicy_Finish(
    FAPI_CONTEXT *context)
{
    LOG_TRACE("called for context:%p", context);

    TSS2_RC r;
    TPMI_ALG_HASH hashAlg;
    IFAPI_CRYPTO_CONTEXT_BLOB *cryptoContext = NULL;
    size_t hashSize;
    size_t digestIdx;
    TPM2B_DIGEST aHash;
    char *publicKey = NULL;

    /* Check for NULL parameters */
    check_not_null(context);

    /* Helpful alias pointers */
    IFAPI_Fapi_AuthorizePolicy * command =
        &context->cmd.Policy_AuthorizeNewPolicy;
    TPMS_POLICYAUTHORIZATION *authorization = &command->authorization;
    TPMS_POLICY *policy = &context->policy.policy;
    TPMT_SIGNATURE *signature;
    IFAPI_OBJECT ** keyObject = &context->Key_Sign.key_object;

    switch (context->state) {
        statecase(context->state, AUTHORIZE_NEW_LOAD_KEY);
            /* Load the key used for signing the policy authorization. */
            r = ifapi_load_key(context, command->signingKeyPath,
                               keyObject);
            return_try_again(r);
            goto_if_error(r, "Fapi sign.", cleanup);

            fallthrough;

        statecase(context->state, AUTHORIZE_NEW_CALCULATE_POLICY);
            /*
             * NameAlg of signing key will be used to compute the aHash digest.
             * This NameAlg will also be used to compute the policy digest.
             * Thus the NameAlg must be equal to the NameAlg of the object to
             * be authorized.
             */
            hashAlg = (*keyObject)->misc.key.public.publicArea.nameAlg;

            if (!(hashSize = ifapi_hash_get_digest_size(hashAlg))) {
                goto_error(r, TSS2_ESYS_RC_NOT_IMPLEMENTED,
                           "Unsupported hash algorithm (%" PRIu16 ")",
                           cleanup, hashAlg);
            }

            /* Calculate the policy digest of the policy to be authorized. */
            r = ifapi_calculate_tree(context,
                                     command->policyPath, policy,
                                     hashAlg, &digestIdx, &hashSize);
            return_try_again(r);
            goto_if_error(r, "Fapi calculate tree.", cleanup);

            /* Compute the aHash from policy digest and policyRef */
            r = ifapi_crypto_hash_start(&cryptoContext, hashAlg);
            goto_if_error(r, "crypto hash start", cleanup);

            HASH_UPDATE_BUFFER(cryptoContext,
                               &policy->
                               policyDigests.digests[digestIdx].digest, hashSize,
                               r, cleanup);
            if (command->policyRef.size > 0) {
                HASH_UPDATE_BUFFER(cryptoContext,
                                   &command->policyRef.buffer[0],
                                   command->policyRef.size, r, cleanup);
            }
            r = ifapi_crypto_hash_finish(&cryptoContext,
                                         (uint8_t *) & aHash.buffer[0], &hashSize);
            goto_if_error(r, "crypto hash finish", cleanup);

            aHash.size = hashSize;
            LOGBLOB_TRACE(&command->policyRef.buffer[0], command->policyRef.size, "policyRef");
            LOGBLOB_TRACE(&aHash.buffer[0], aHash.size, "aHash");

            fallthrough;

        statecase(context->state, AUTHORIZE_NEW_KEY_SIGN_POLICY);
            /* Perform the singing operation on the policy's aHash. */
            r = ifapi_key_sign(context, *keyObject, NULL,
                               &aHash, &signature, &publicKey, NULL);
            return_try_again(r);
            goto_if_error(r, "Fapi sign.", cleanup);

            SAFE_FREE(publicKey);

            /* Store the signature results and cleanup remainters. */
            authorization->signature = *signature;
            authorization->policyRef = command->policyRef;
            strdup_check(authorization->type, "tpm", r, cleanup);
            authorization->key =
                (*keyObject)->misc.key.public.publicArea;
            SAFE_FREE(signature);
            ifapi_cleanup_ifapi_object(*keyObject);

            /* Extend the authorization to the policy stored. */
            ifapi_extend_authorization(policy, authorization);
            goto_if_null(policy->policyAuthorizations,
                         "Out of memory", TSS2_FAPI_RC_MEMORY, cleanup);

            fallthrough;

        statecase(context->state, AUTHORIZE_NEW_WRITE_POLICY_PREPARE);
            /* Store the newly authorized policy in the policy store. */
            r = ifapi_policy_store_store_async(&context->pstore, &context->io,
                                               command->policyPath, policy);
            goto_if_error_reset_state(r, "Could not open: %s", cleanup,
                    command->policyPath);

            fallthrough;

        statecase(context->state, AUTHORIZE_NEW_WRITE_POLICY);
            r = ifapi_policy_store_store_finish(&context->pstore, &context->io);
            return_try_again(r);
            goto_if_error_reset_state(r, "write_finish failed", cleanup);

            fallthrough;

        statecase(context->state, AUTHORIZE_NEW_CLEANUP)
            /* Cleanup and reset the context state. */
            r = ifapi_cleanup_session(context);
            try_again_or_error_goto(r, "Cleanup", cleanup);

            context->state = _FAPI_STATE_INIT;
            break;

       statecasedefault(context->state);
    }

cleanup:
    /* Cleanup any intermediate results and state stored in the context. */
    if (cryptoContext)
        ifapi_crypto_hash_abort(&cryptoContext);
    ifapi_session_clean(context);
    ifapi_cleanup_policy(policy);
    ifapi_cleanup_ifapi_object(&context->createPrimary.pkey_object);
    ifapi_cleanup_ifapi_object(context->loadKey.key_object);
    ifapi_cleanup_ifapi_object(&context->loadKey.auth_object);
    SAFE_FREE(command->policyPath);
    SAFE_FREE(command->signingKeyPath);
    LOG_TRACE("finished");
    return r;
}
