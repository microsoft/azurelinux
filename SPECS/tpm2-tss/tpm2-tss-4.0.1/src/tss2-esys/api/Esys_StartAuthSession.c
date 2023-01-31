/* SPDX-License-Identifier: BSD-2-Clause */
/*******************************************************************************
 * Copyright 2017-2018, Fraunhofer SIT sponsored by Infineon Technologies AG
 * All rights reserved.
 ******************************************************************************/

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include "tss2_mu.h"
#include "tss2_sys.h"
#include "tss2_esys.h"

#include "esys_types.h"
#include "esys_iutil.h"
#include "esys_mu.h"
#define LOGMODULE esys
#include "util/log.h"
#include "util/aux_util.h"

/** Store command parameters inside the ESYS_CONTEXT for use during _Finish */
static void store_input_parameters (
    ESYS_CONTEXT *esysContext,
    ESYS_TR tpmKey,
    ESYS_TR bind,
    const TPM2B_NONCE *nonceCaller,
    TPM2_SE sessionType,
    const TPMT_SYM_DEF *symmetric,
    TPMI_ALG_HASH authHash)
{
    esysContext->in.StartAuthSession.tpmKey = tpmKey;
    esysContext->in.StartAuthSession.bind = bind;
    esysContext->in.StartAuthSession.sessionType = sessionType;
    esysContext->in.StartAuthSession.authHash = authHash;
    if (nonceCaller == NULL) {
        esysContext->in.StartAuthSession.nonceCaller = NULL;
    } else {
        esysContext->in.StartAuthSession.nonceCallerData = *nonceCaller;
        esysContext->in.StartAuthSession.nonceCaller =
            &esysContext->in.StartAuthSession.nonceCallerData;
    }
    if (symmetric == NULL) {
        esysContext->in.StartAuthSession.symmetric = NULL;
    } else {
        esysContext->in.StartAuthSession.symmetricData = *symmetric;
        esysContext->in.StartAuthSession.symmetric =
            &esysContext->in.StartAuthSession.symmetricData;
    }
}

/** One-Call function for TPM2_StartAuthSession
 *
 * This function invokes the TPM2_StartAuthSession command in a one-call
 * variant. This means the function will block until the TPM response is
 * available. All input parameters are const. The memory for non-simple output
 * parameters is allocated by the function implementation.
 *
 * @param[in,out] esysContext The ESYS_CONTEXT.
 * @param[in]  tpmKey Handle of a loaded decrypt key used to encrypt salt.
 * @param[in]  bind Entity providing the authValue.
 * @param[in]  shandle1 First session handle.
 * @param[in]  shandle2 Second session handle.
 * @param[in]  shandle3 Third session handle.
 * @param[in]  nonceCaller Initial nonceCaller, sets nonceTPM size for the
 *             session.
 * @param[in]  sessionType Indicates the type of the session; simple HMAC or
 *             policy (including a trial policy).
 * @param[in]  symmetric The algorithm and key size for parameter encryption.
 * @param[in]  authHash Hash algorithm to use for the session.
 * @param[out] sessionHandle  ESYS_TR handle of ESYS resource for TPMI_SH_AUTH_SESSION.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_ESYS_RC_BAD_REFERENCE if the esysContext or required input
 *         pointers or required output handle references are NULL.
 * @retval TSS2_ESYS_RC_BAD_CONTEXT: if esysContext corruption is detected.
 * @retval TSS2_ESYS_RC_MEMORY: if the ESAPI cannot allocate enough memory for
 *         internal operations or return parameters.
 * @retval TSS2_ESYS_RC_BAD_SEQUENCE: if the context has an asynchronous
 *         operation already pending.
 * @retval TSS2_ESYS_RC_INSUFFICIENT_RESPONSE: if the TPM's response does not
 *          at least contain the tag, response length, and response code.
 * @retval TSS2_ESYS_RC_MALFORMED_RESPONSE: if the TPM's response is corrupted.
 * @retval TSS2_ESYS_RC_RSP_AUTH_FAILED: if the response HMAC from the TPM
           did not verify.
 * @retval TSS2_ESYS_RC_MULTIPLE_DECRYPT_SESSIONS: if more than one session has
 *         the 'decrypt' attribute bit set.
 * @retval TSS2_ESYS_RC_MULTIPLE_ENCRYPT_SESSIONS: if more than one session has
 *         the 'encrypt' attribute bit set.
 * @retval TSS2_ESYS_RC_BAD_TR: if any of the ESYS_TR objects are unknown
 *         to the ESYS_CONTEXT or are of the wrong type or if required
 *         ESYS_TR objects are ESYS_TR_NONE.
 * @retval TSS2_RCs produced by lower layers of the software stack may be
 *         returned to the caller unaltered unless handled internally.
 */
TSS2_RC
Esys_StartAuthSession(
    ESYS_CONTEXT *esysContext,
    ESYS_TR tpmKey,
    ESYS_TR bind,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_NONCE *nonceCaller,
    TPM2_SE sessionType,
    const TPMT_SYM_DEF *symmetric,
    TPMI_ALG_HASH authHash, ESYS_TR *sessionHandle)
{
    TSS2_RC r;

    r = Esys_StartAuthSession_Async(esysContext, tpmKey, bind, shandle1,
                                    shandle2, shandle3, nonceCaller, sessionType,
                                    symmetric, authHash);
    return_if_error(r, "Error in async function");

    /* Set the timeout to indefinite for now, since we want _Finish to block */
    int32_t timeouttmp = esysContext->timeout;
    esysContext->timeout = -1;
    /*
     * Now we call the finish function, until return code is not equal to
     * from TSS2_BASE_RC_TRY_AGAIN.
     * Note that the finish function may return TSS2_RC_TRY_AGAIN, even if we
     * have set the timeout to -1. This occurs for example if the TPM requests
     * a retransmission of the command via TPM2_RC_YIELDED.
     */
    do {
        r = Esys_StartAuthSession_Finish(esysContext, sessionHandle);
        /* This is just debug information about the reattempt to finish the
           command */
        if (base_rc(r) == TSS2_BASE_RC_TRY_AGAIN)
            LOG_DEBUG("A layer below returned TRY_AGAIN: %" PRIx32
                      " => resubmitting command", r);
    } while (base_rc(r) == TSS2_BASE_RC_TRY_AGAIN);

    /* Restore the timeout value to the original value */
    esysContext->timeout = timeouttmp;
    return_if_error(r, "Esys Finish");

    return TSS2_RC_SUCCESS;
}

/** Asynchronous function for TPM2_StartAuthSession
 *
 * This function invokes the TPM2_StartAuthSession command in a asynchronous
 * variant. This means the function will return as soon as the command has been
 * sent downwards the stack to the TPM. All input parameters are const.
 * In order to retrieve the TPM's response call Esys_StartAuthSession_Finish.
 *
 * @param[in,out] esysContext The ESYS_CONTEXT.
 * @param[in]  tpmKey Handle of a loaded decrypt key used to encrypt salt.
 * @param[in]  bind Entity providing the authValue.
 * @param[in]  shandle1 First session handle.
 * @param[in]  shandle2 Second session handle.
 * @param[in]  shandle3 Third session handle.
 * @param[in]  nonceCaller Initial nonceCaller, sets nonceTPM size for the
 *             session.
 * @param[in]  sessionType Indicates the type of the session; simple HMAC or
 *             policy (including a trial policy).
 * @param[in]  symmetric The algorithm and key size for parameter encryption.
 * @param[in]  authHash Hash algorithm to use for the session.
 * @retval ESYS_RC_SUCCESS if the function call was a success.
 * @retval TSS2_ESYS_RC_BAD_REFERENCE if the esysContext or required input
 *         pointers or required output handle references are NULL.
 * @retval TSS2_ESYS_RC_BAD_CONTEXT: if esysContext corruption is detected.
 * @retval TSS2_ESYS_RC_MEMORY: if the ESAPI cannot allocate enough memory for
 *         internal operations or return parameters.
 * @retval TSS2_RCs produced by lower layers of the software stack may be
           returned to the caller unaltered unless handled internally.
 * @retval TSS2_ESYS_RC_MULTIPLE_DECRYPT_SESSIONS: if more than one session has
 *         the 'decrypt' attribute bit set.
 * @retval TSS2_ESYS_RC_MULTIPLE_ENCRYPT_SESSIONS: if more than one session has
 *         the 'encrypt' attribute bit set.
 * @retval TSS2_ESYS_RC_BAD_TR: if any of the ESYS_TR objects are unknown
 *         to the ESYS_CONTEXT or are of the wrong type or if required
 *         ESYS_TR objects are ESYS_TR_NONE.
 */
TSS2_RC
Esys_StartAuthSession_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR tpmKey,
    ESYS_TR bind,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_NONCE *nonceCaller,
    TPM2_SE sessionType,
    const TPMT_SYM_DEF *symmetric,
    TPMI_ALG_HASH authHash)
{
    TSS2_RC r;
    LOG_TRACE("context=%p, tpmKey=%"PRIx32 ", bind=%"PRIx32 ","
              "nonceCaller=%p, sessionType=%02"PRIx8", symmetric=%p,"
              "authHash=%04"PRIx16"",
              esysContext, tpmKey, bind, nonceCaller, sessionType,
              symmetric, authHash);
    TPM2B_ENCRYPTED_SECRET encryptedSaltAux;
    const TPM2B_ENCRYPTED_SECRET *encryptedSalt = &encryptedSaltAux;
    TSS2L_SYS_AUTH_COMMAND auths;
    RSRC_NODE_T *tpmKeyNode;
    RSRC_NODE_T *bindNode;

    /* Check context, sequence correctness and set state to error for now */
    if (esysContext == NULL) {
        LOG_ERROR("esyscontext is NULL.");
        return TSS2_ESYS_RC_BAD_REFERENCE;
    }
    r = iesys_check_sequence_async(esysContext);
    if (r != TSS2_RC_SUCCESS)
        return r;
    esysContext->state = _ESYS_STATE_INTERNALERROR;

    /* Check input parameters */
    r = check_session_feasibility(shandle1, shandle2, shandle3, 0);
    return_state_if_error(r, _ESYS_STATE_INIT, "Check session usage");
    store_input_parameters(esysContext, tpmKey, bind, nonceCaller, sessionType,
                           symmetric, authHash);

    /* Retrieve the metadata objects for provided handles */
    r = esys_GetResourceObject(esysContext, tpmKey, &tpmKeyNode);
    return_state_if_error(r, _ESYS_STATE_INIT, "tpmKey unknown.");
    r = esys_GetResourceObject(esysContext, bind, &bindNode);
    return_state_if_error(r, _ESYS_STATE_INIT, "bind unknown.");
    size_t authHash_size = 0;
    TSS2_RC r2;
    r2 = iesys_compute_encrypted_salt(esysContext, tpmKeyNode,
                                      &encryptedSaltAux);
    return_state_if_error(r2, _ESYS_STATE_INIT, "Error in parameter encryption.");

    if (nonceCaller == NULL) {
        r2 = iesys_crypto_hash_get_digest_size(authHash,&authHash_size);
        return_state_if_error(r2, _ESYS_STATE_INIT, "Error in hash_get_digest_size.");

        r2 = iesys_crypto_get_random2b(&esysContext->crypto_backend,
                &esysContext->in.StartAuthSession.nonceCallerData,
                                   authHash_size);
        return_state_if_error(r2, _ESYS_STATE_INIT, "Error in crypto_random2b.");
        esysContext->in.StartAuthSession.nonceCaller
           = &esysContext->in.StartAuthSession.nonceCallerData;
        nonceCaller = esysContext->in.StartAuthSession.nonceCaller;
    }

    /* Initial invocation of SAPI to prepare the command buffer with parameters */
    r = Tss2_Sys_StartAuthSession_Prepare(esysContext->sys,
                                          (tpmKeyNode == NULL) ? TPM2_RH_NULL
                                           : tpmKeyNode->rsrc.handle,
                                          (bindNode == NULL) ? TPM2_RH_NULL
                                           : bindNode->rsrc.handle, nonceCaller,
                                          encryptedSalt, sessionType, symmetric,
                                          authHash);
    return_state_if_error(r, _ESYS_STATE_INIT, "SAPI Prepare returned error.");

    /* Calculate the cpHash Values */
    r = init_session_tab(esysContext, shandle1, shandle2, shandle3);
    return_state_if_error(r, _ESYS_STATE_INIT, "Initialize session resources");
    iesys_compute_session_value(esysContext->session_tab[0], NULL, NULL);
    iesys_compute_session_value(esysContext->session_tab[1], NULL, NULL);
    iesys_compute_session_value(esysContext->session_tab[2], NULL, NULL);

    /* Generate the auth values and set them in the SAPI command buffer */

    RSRC_NODE_T none;
    size_t offset = 0;
    none.rsrc.handle = TPM2_RH_NULL;
    none.rsrc.rsrcType = IESYSC_WITHOUT_MISC_RSRC;
    r = Tss2_MU_TPM2_HANDLE_Marshal(TPM2_RH_NULL,
                                none.rsrc.name.name,
                                sizeof(none.rsrc.name.name),
                                &offset);
    return_state_if_error(r, _ESYS_STATE_INIT, "Marshaling TPM handle.");
    none.rsrc.name.size = offset;
    r = iesys_gen_auths(esysContext, tpmKeyNode ? tpmKeyNode : &none,
                                     bindNode ? bindNode : &none, NULL, &auths);
    return_state_if_error(r, _ESYS_STATE_INIT,
                          "Error in computation of auth values");

    esysContext->authsCount = auths.count;
    if (auths.count > 0) {
        r = Tss2_Sys_SetCmdAuths(esysContext->sys, &auths);
        return_state_if_error(r, _ESYS_STATE_INIT, "SAPI error on SetCmdAuths");
    }

    /* Trigger execution and finish the async invocation */
    r = Tss2_Sys_ExecuteAsync(esysContext->sys);
    return_state_if_error(r, _ESYS_STATE_INTERNALERROR,
                          "Finish (Execute Async)");

    esysContext->state = _ESYS_STATE_SENT;

    return r;
}

/** Asynchronous finish function for TPM2_StartAuthSession
 *
 * This function returns the results of a TPM2_StartAuthSession command
 * invoked via Esys_StartAuthSession_Finish. All non-simple output parameters
 * are allocated by the function's implementation. NULL can be passed for every
 * output parameter if the value is not required.
 *
 * @param[in,out] esysContext The ESYS_CONTEXT.
 * @param[out] sessionHandle  ESYS_TR handle of ESYS resource for TPMI_SH_AUTH_SESSION.
 * @retval TSS2_RC_SUCCESS on success
 * @retval ESYS_RC_SUCCESS if the function call was a success.
 * @retval TSS2_ESYS_RC_BAD_REFERENCE if the esysContext or required input
 *         pointers or required output handle references are NULL.
 * @retval TSS2_ESYS_RC_BAD_CONTEXT: if esysContext corruption is detected.
 * @retval TSS2_ESYS_RC_MEMORY: if the ESAPI cannot allocate enough memory for
 *         internal operations or return parameters.
 * @retval TSS2_ESYS_RC_BAD_SEQUENCE: if the context has an asynchronous
 *         operation already pending.
 * @retval TSS2_ESYS_RC_TRY_AGAIN: if the timeout counter expires before the
 *         TPM response is received.
 * @retval TSS2_ESYS_RC_INSUFFICIENT_RESPONSE: if the TPM's response does not
 *         at least contain the tag, response length, and response code.
 * @retval TSS2_ESYS_RC_RSP_AUTH_FAILED: if the response HMAC from the TPM did
 *         not verify.
 * @retval TSS2_ESYS_RC_MALFORMED_RESPONSE: if the TPM's response is corrupted.
 * @retval TSS2_RCs produced by lower layers of the software stack may be
 *         returned to the caller unaltered unless handled internally.
 */
TSS2_RC
Esys_StartAuthSession_Finish(
    ESYS_CONTEXT *esysContext, ESYS_TR *sessionHandle)
{
    TPM2B_NONCE lnonceTPM;
    TSS2_RC r;
    LOG_TRACE("context=%p, sessionHandle=%p",
              esysContext, sessionHandle);

    if (esysContext == NULL) {
        LOG_ERROR("esyscontext is NULL.");
        return TSS2_ESYS_RC_BAD_REFERENCE;
    }

    /* Check for correct sequence and set sequence to irregular for now */
    if (esysContext->state != _ESYS_STATE_SENT &&
        esysContext->state != _ESYS_STATE_RESUBMISSION) {
        LOG_ERROR("Esys called in bad sequence.");
        return TSS2_ESYS_RC_BAD_SEQUENCE;
    }
    esysContext->state = _ESYS_STATE_INTERNALERROR;
    RSRC_NODE_T *sessionHandleNode = NULL;

    /* Allocate memory for response parameters */
    if (sessionHandle == NULL) {
        LOG_ERROR("Handle sessionHandle may not be NULL");
        return TSS2_ESYS_RC_BAD_REFERENCE;
    }
    *sessionHandle = esysContext->esys_handle_cnt++;
    r = esys_CreateResourceObject(esysContext, *sessionHandle, &sessionHandleNode);
    if (r != TSS2_RC_SUCCESS)
        return r;

    IESYS_RESOURCE *rsrc = &sessionHandleNode->rsrc;
    rsrc->handle = ESYS_TR_NONE;
    rsrc->misc.rsrc_session.sessionAttributes = TPMA_SESSION_CONTINUESESSION;
    rsrc->misc.rsrc_session.sessionType = esysContext->in.StartAuthSession.sessionType;
    rsrc->misc.rsrc_session.authHash = esysContext->in.StartAuthSession.authHash;
    rsrc->misc.rsrc_session.symmetric = *esysContext->in.StartAuthSession.symmetric;
    rsrc->misc.rsrc_session.nonceCaller = esysContext->in.StartAuthSession.nonceCallerData;

    /* Receive the TPM response and handle resubmissions if necessary. */
    r = Tss2_Sys_ExecuteFinish(esysContext->sys, esysContext->timeout);
    if (base_rc(r) == TSS2_BASE_RC_TRY_AGAIN) {
        LOG_DEBUG("A layer below returned TRY_AGAIN: %" PRIx32, r);
        esysContext->state = _ESYS_STATE_SENT;
        goto error_cleanup;
    }
    /* This block handle the resubmission of TPM commands given a certain set of
     * TPM response codes. */
    if (r == TPM2_RC_RETRY || r == TPM2_RC_TESTING || r == TPM2_RC_YIELDED) {
        LOG_DEBUG("TPM returned RETRY, TESTING or YIELDED, which triggers a "
            "resubmission: %" PRIx32, r);
        if (esysContext->submissionCount++ >= _ESYS_MAX_SUBMISSIONS) {
            LOG_WARNING("Maximum number of (re)submissions has been reached.");
            esysContext->state = _ESYS_STATE_INIT;
            goto error_cleanup;
        }
        esysContext->state = _ESYS_STATE_RESUBMISSION;
        r = Tss2_Sys_ExecuteAsync(esysContext->sys);
        if (r != TSS2_RC_SUCCESS) {
            LOG_WARNING("Error attempting to resubmit");
            /* We do not set esysContext->state here but inherit the most recent
             * state of the _async function. */
            goto error_cleanup;
        }
        r = TSS2_ESYS_RC_TRY_AGAIN;
        LOG_DEBUG("Resubmission initiated and returning RC_TRY_AGAIN.");
        goto error_cleanup;
    }
    /* The following is the "regular error" handling. */
    if (iesys_tpm_error(r)) {
        LOG_WARNING("Received TPM Error");
        esysContext->state = _ESYS_STATE_INIT;
        goto error_cleanup;
    } else if (r != TSS2_RC_SUCCESS) {
        LOG_ERROR("Received a non-TPM Error");
        esysContext->state = _ESYS_STATE_INTERNALERROR;
        goto error_cleanup;
    }

    /*
     * Now the verification of the response (hmac check) and if necessary the
     * parameter decryption have to be done.
     */
    r = iesys_check_response(esysContext);
    goto_state_if_error(r, _ESYS_STATE_INTERNALERROR, "Error: check response",
                        error_cleanup);

    /*
     * After the verification of the response we call the complete function
     * to deliver the result.
     */
    r = Tss2_Sys_StartAuthSession_Complete(esysContext->sys,
                                           &sessionHandleNode->rsrc.handle,
                                           &lnonceTPM);
    goto_state_if_error(r, _ESYS_STATE_INTERNALERROR,
                        "Received error from SAPI unmarshaling" ,
                        error_cleanup);

    sessionHandleNode->rsrc.misc.rsrc_session.nonceTPM = lnonceTPM;
    sessionHandleNode->rsrc.rsrcType = IESYSC_SESSION_RSRC;
    if (esysContext->in.StartAuthSession.bind != ESYS_TR_NONE || esysContext->salt.size > 0) {
        ESYS_TR bind = esysContext->in.StartAuthSession.bind;
        ESYS_TR tpmKey = esysContext->in.StartAuthSession.tpmKey;
        RSRC_NODE_T *bindNode;
        r = esys_GetResourceObject(esysContext, bind, &bindNode);
        goto_if_error(r, "get resource", error_cleanup);

        RSRC_NODE_T *tpmKeyNode;
        r = esys_GetResourceObject(esysContext, tpmKey, &tpmKeyNode);
        goto_if_error(r, "get resource", error_cleanup);

        size_t keyHash_size = 0;
        size_t authHash_size = 0;
        if (tpmKeyNode != NULL) {
            r = iesys_crypto_hash_get_digest_size(
                     tpmKeyNode->rsrc.misc.rsrc_key_pub.publicArea.nameAlg, &
                     keyHash_size);
            if (r != TSS2_RC_SUCCESS) {
                LOG_ERROR("Error: initialize auth session (%x).", r);
                return r;
            }
        }
        r = iesys_crypto_hash_get_digest_size(esysContext->in.StartAuthSession.
                                              authHash,&authHash_size);
        if (r != TSS2_RC_SUCCESS) {
            LOG_ERROR("Error: initialize auth session (%x).", r);
            return r;
        }
        /* compute session key except for an unbound session */
        if (!(bind == ESYS_TR_RH_NULL && tpmKey == ESYS_TR_NONE)) {
            size_t secret_size = 0;
            if (tpmKey != ESYS_TR_NONE)
                secret_size += keyHash_size;
            if (bind != ESYS_TR_NONE && bindNode != NULL)
                secret_size += bindNode->auth.size;
            /*
             * A non null pointer for secret is required by the subsequent functions,
             * hence a malloc is called with size 1 if secret_size is zero.
             */
            uint8_t *secret = malloc(secret_size ? secret_size : 1);
            if (secret == NULL) {
                LOG_ERROR("Out of memory.");
                return TSS2_ESYS_RC_MEMORY;
            }
            if  (bind != ESYS_TR_NONE && bindNode != NULL
                 && bindNode->auth.size > 0)
                memcpy(&secret[0], &bindNode->auth.buffer[0], bindNode->auth.size);
            if (tpmKey != ESYS_TR_NONE)
                memcpy(&secret[(bind == ESYS_TR_NONE || bindNode == NULL) ? 0
                               : bindNode->auth.size],
                       &esysContext->salt.buffer[0], keyHash_size);
            if (bind != ESYS_TR_NONE &&  bindNode != NULL)
                iesys_compute_bound_entity(&bindNode->rsrc.name,
                                           &bindNode->auth,
                                           &sessionHandleNode->rsrc.misc.rsrc_session.bound_entity);
            LOGBLOB_DEBUG(secret, secret_size, "ESYS Session Secret");
            r = iesys_crypto_KDFa(&esysContext->crypto_backend, esysContext->in.StartAuthSession.authHash, secret,
                                  secret_size, "ATH",
                                  &lnonceTPM, esysContext->in.StartAuthSession.nonceCaller,
                                  authHash_size*8, NULL,
                                  &sessionHandleNode->rsrc.misc.rsrc_session.sessionKey.buffer[0], FALSE);
            free(secret);
            return_if_error(r, "Error in KDFa computation.");

            sessionHandleNode->rsrc.misc.rsrc_session.sessionKey.size = authHash_size;
            LOGBLOB_DEBUG(&sessionHandleNode->rsrc.misc.rsrc_session.sessionKey
                      .buffer[0], authHash_size, "Session Key");
            return_if_error(r,"Error KDFa");
        }
    }
    size_t offset = 0;
    r = Tss2_MU_TPM2_HANDLE_Marshal(sessionHandleNode->rsrc.handle,
                                    &sessionHandleNode->rsrc.name.name[0],
                                    sizeof(sessionHandleNode->rsrc.name.name),
                                    &offset);
    goto_if_error(r, "Marshal session name", error_cleanup);

    sessionHandleNode->rsrc.name.size = offset;
    memset(&esysContext->salt, '\0', sizeof(esysContext->salt));
    esysContext->state = _ESYS_STATE_INIT;

    return TSS2_RC_SUCCESS;

error_cleanup:
    if (sessionHandleNode->rsrc.handle != ESYS_TR_NONE) {
        r = Esys_FlushContext(esysContext, sessionHandleNode->rsrc.handle);
        if (r != TSS2_RC_SUCCESS)
            LOG_ERROR("FlushContext failed.");
    }
    Esys_TR_Close(esysContext, sessionHandle);

    return r;
}
