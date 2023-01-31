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
    const TPM2B_SENSITIVE_CREATE *inSensitive,
    const TPM2B_TEMPLATE *inPublic)
{
    if (inSensitive == NULL) {
        esysContext->in.CreateLoaded.inSensitive = NULL;
    } else {
        esysContext->in.CreateLoaded.inSensitiveData = *inSensitive;
        esysContext->in.CreateLoaded.inSensitive =
            &esysContext->in.CreateLoaded.inSensitiveData;
    }
    if (inPublic == NULL) {
        esysContext->in.CreateLoaded.inPublic = NULL;
    } else {
        esysContext->in.CreateLoaded.inPublicData = *inPublic;
        esysContext->in.CreateLoaded.inPublic =
            &esysContext->in.CreateLoaded.inPublicData;
    }
}

/** One-Call function for TPM2_CreateLoaded
 *
 * This function invokes the TPM2_CreateLoaded command in a one-call
 * variant. This means the function will block until the TPM response is
 * available. All input parameters are const. The memory for non-simple output
 * parameters is allocated by the function implementation.
 *
 * @param[in,out] esysContext The ESYS_CONTEXT.
 * @param[in]  parentHandle TPM2_Handle of a transient storage key, a persistent
 *             storage key, TPM2_RH_ENDORSEMENT, TPM2_RH_OWNER,
 *             TPM2_RH_PLATFORM+{PP}, or TPM2_RH_NULL.
 * @param[in]  shandle1 Session handle for authorization of parentHandle
 * @param[in]  shandle2 Second session handle.
 * @param[in]  shandle3 Third session handle.
 * @param[in]  inSensitive The sensitive data, see TPM 2.0 Part 1 Sensitive
 *             Values.
 * @param[in]  inPublic The public template.
 * @param[out] outPrivate The sensitive area of the object (optional).
 *             (callee-allocated)
 * @param[out] outPublic The public portion of the created object.
 *             (callee-allocated)
 * @param[out] objectHandle  ESYS_TR handle of ESYS resource for TPM2_HANDLE.
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
Esys_CreateLoaded(
    ESYS_CONTEXT *esysContext,
    ESYS_TR parentHandle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_SENSITIVE_CREATE *inSensitive,
    const TPM2B_TEMPLATE *inPublic, ESYS_TR *objectHandle,
    TPM2B_PRIVATE **outPrivate,
    TPM2B_PUBLIC **outPublic)
{
    TSS2_RC r;

    r = Esys_CreateLoaded_Async(esysContext, parentHandle, shandle1, shandle2,
                                shandle3, inSensitive, inPublic);
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
        r = Esys_CreateLoaded_Finish(esysContext, objectHandle, outPrivate,
                                     outPublic);
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

/** Asynchronous function for TPM2_CreateLoaded
 *
 * This function invokes the TPM2_CreateLoaded command in a asynchronous
 * variant. This means the function will return as soon as the command has been
 * sent downwards the stack to the TPM. All input parameters are const.
 * In order to retrieve the TPM's response call Esys_CreateLoaded_Finish.
 *
 * @param[in,out] esysContext The ESYS_CONTEXT.
 * @param[in]  parentHandle TPM2_Handle of a transient storage key, a persistent
 *             storage key, TPM2_RH_ENDORSEMENT, TPM2_RH_OWNER,
 *             TPM2_RH_PLATFORM+{PP}, or TPM2_RH_NULL.
 * @param[in]  shandle1 Session handle for authorization of parentHandle
 * @param[in]  shandle2 Second session handle.
 * @param[in]  shandle3 Third session handle.
 * @param[in]  inSensitive The sensitive data, see TPM 2.0 Part 1 Sensitive
 *             Values.
 * @param[in]  inPublic The public template.
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
Esys_CreateLoaded_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR parentHandle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_SENSITIVE_CREATE *inSensitive,
    const TPM2B_TEMPLATE *inPublic)
{
    TSS2_RC r;
    LOG_TRACE("context=%p, parentHandle=%"PRIx32 ", inSensitive=%p,"
              "inPublic=%p",
              esysContext, parentHandle, inSensitive, inPublic);
    TSS2L_SYS_AUTH_COMMAND auths;
    RSRC_NODE_T *parentHandleNode;
    size_t offset = 0;
    TPMT_PUBLIC publicArea;

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
    r = check_session_feasibility(shandle1, shandle2, shandle3, 1);
    return_state_if_error(r, _ESYS_STATE_INIT, "Check session usage");
    store_input_parameters(esysContext, inSensitive, inPublic);

    if (inPublic) {
        r = Tss2_MU_TPMT_PUBLIC_Unmarshal(&inPublic->buffer[0], inPublic->size, &offset,
                                          &publicArea);
        return_if_error(r, "Unmarshalling inPublic failed");

        r = iesys_hash_long_auth_values(
            &esysContext->crypto_backend,
            &esysContext->in.CreateLoaded.inSensitive->sensitive.userAuth,
             publicArea.nameAlg);
        return_state_if_error(r, _ESYS_STATE_INIT, "Adapt auth value.");
    }

    /* Retrieve the metadata objects for provided handles */
    r = esys_GetResourceObject(esysContext, parentHandle, &parentHandleNode);
    return_state_if_error(r, _ESYS_STATE_INIT, "parentHandle unknown.");

    /* Initial invocation of SAPI to prepare the command buffer with parameters */
    r = Tss2_Sys_CreateLoaded_Prepare(esysContext->sys,
                                      (parentHandleNode == NULL) ? TPM2_RH_NULL
                                       : parentHandleNode->rsrc.handle,
                                      esysContext->in.CreateLoaded.inSensitive, inPublic);
    return_state_if_error(r, _ESYS_STATE_INIT, "SAPI Prepare returned error.");

    /* Calculate the cpHash Values */
    r = init_session_tab(esysContext, shandle1, shandle2, shandle3);
    return_state_if_error(r, _ESYS_STATE_INIT, "Initialize session resources");
    if (parentHandleNode != NULL)
        iesys_compute_session_value(esysContext->session_tab[0],
                &parentHandleNode->rsrc.name, &parentHandleNode->auth);
    else
        iesys_compute_session_value(esysContext->session_tab[0], NULL, NULL);

    iesys_compute_session_value(esysContext->session_tab[1], NULL, NULL);
    iesys_compute_session_value(esysContext->session_tab[2], NULL, NULL);

    /* Generate the auth values and set them in the SAPI command buffer */
    r = iesys_gen_auths(esysContext, parentHandleNode, NULL, NULL, &auths);
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

/** Asynchronous finish function for TPM2_CreateLoaded
 *
 * This function returns the results of a TPM2_CreateLoaded command
 * invoked via Esys_CreateLoaded_Finish. All non-simple output parameters
 * are allocated by the function's implementation. NULL can be passed for every
 * output parameter if the value is not required.
 *
 * @param[in,out] esysContext The ESYS_CONTEXT.
 * @param[out] outPrivate The sensitive area of the object (optional).
 *             (callee-allocated)
 * @param[out] outPublic The public portion of the created object.
 *             (callee-allocated)
 * @param[out] objectHandle  ESYS_TR handle of ESYS resource for TPM2_HANDLE.
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
Esys_CreateLoaded_Finish(
    ESYS_CONTEXT *esysContext, ESYS_TR *objectHandle,
    TPM2B_PRIVATE **outPrivate,
    TPM2B_PUBLIC **outPublic)
{
    TPM2B_PUBLIC *loutPublic = NULL;
    TSS2_RC r;
    LOG_TRACE("context=%p, objectHandle=%p, outPrivate=%p,"
              "outPublic=%p",
              esysContext, objectHandle, outPrivate,
              outPublic);

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
    TPM2B_NAME name;
    RSRC_NODE_T *objectHandleNode = NULL;

    /* Allocate memory for response parameters */
    if (objectHandle == NULL) {
        LOG_ERROR("Handle objectHandle may not be NULL");
        return TSS2_ESYS_RC_BAD_REFERENCE;
    }
    *objectHandle = esysContext->esys_handle_cnt++;
    r = esys_CreateResourceObject(esysContext, *objectHandle, &objectHandleNode);
    if (r != TSS2_RC_SUCCESS)
        return r;

    if (outPrivate != NULL) {
        *outPrivate = calloc(sizeof(TPM2B_PRIVATE), 1);
        if (*outPrivate == NULL) {
            goto_error(r, TSS2_ESYS_RC_MEMORY, "Out of memory", error_cleanup);
        }
    }
    loutPublic = calloc(sizeof(TPM2B_PUBLIC), 1);
    if (loutPublic == NULL) {
        goto_error(r, TSS2_ESYS_RC_MEMORY, "Out of memory", error_cleanup);
    }

    /*Receive the TPM response and handle resubmissions if necessary. */
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
    r = Tss2_Sys_CreateLoaded_Complete(esysContext->sys,
                                       &objectHandleNode->rsrc.handle,
                                       (outPrivate != NULL) ? *outPrivate : NULL,
                                       loutPublic, &name);
    goto_state_if_error(r, _ESYS_STATE_INTERNALERROR,
                        "Received error from SAPI unmarshaling" ,
                        error_cleanup);


    /* Update the meta data of the ESYS_TR object */
    objectHandleNode->rsrc.rsrcType = IESYSC_KEY_RSRC;
    objectHandleNode->rsrc.misc.rsrc_key_pub = *loutPublic;

    /* Check name and outPublic for consistency */
    if (!iesys_compare_name(&esysContext->crypto_backend, &objectHandleNode->rsrc.misc.rsrc_key_pub, &name))
        goto_error(r, TSS2_ESYS_RC_MALFORMED_RESPONSE,
            "in Public name not equal name in response", error_cleanup);

    /* Update the meta data of the ESYS_TR object */
    objectHandleNode->rsrc.name = name;
    objectHandleNode->auth = esysContext->in.CreateLoaded.inSensitive->sensitive.userAuth;
    if (outPublic != NULL)
        *outPublic = loutPublic;
    else
        SAFE_FREE(loutPublic);

    esysContext->state = _ESYS_STATE_INIT;

    return TSS2_RC_SUCCESS;

error_cleanup:
    Esys_TR_Close(esysContext, objectHandle);
    if (outPrivate != NULL)
        SAFE_FREE(*outPrivate);
    SAFE_FREE(loutPublic);

    return r;
}
