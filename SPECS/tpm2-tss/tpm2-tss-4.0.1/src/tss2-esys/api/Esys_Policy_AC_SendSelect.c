/* SPDX-License-Identifier: BSD-2-Clause */
/*******************************************************************************
 * Copyright (c) 2022, Intel Corporation
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

/**
 * One-Call function for TPM2_Policy_AC_SendSelect.
 *
 * This command allows qualification of the sending (copying) of an Object to
 * an Attached Component (AC). Qualification includes selection of the
 * receiving AC and the method of authentication for the AC, and, in certain
 * circumstances, the Object to be sent may be specified.
 *
 * @param[in,out] esysContext The ESYS_CONTEXT.
 * @param[in] policySession1 handle for the policy session being extended
 * @param[in] optionalSession2 Second session handle.
 * @param[in] optionalSession3 Third session handle.
 * @param[in] objectName Name of the Object to be sent
 * @param[in] authHandleName Name associated with authHandle used in the
 *                           TPM2_AC_Send() command
 * @param[in] acName Name of the Attached Component to which the Object will
 *                   be sent
 * @param[in] includeObject if SET, objectName will be included in the value in
 *                          policySession→policyDigest
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
 * @retval TSS2_ESYS_RC_NO_DECRYPT_PARAM: if one of the sessions has the
 *         'decrypt' attribute set and the command does not support encryption
 *         of the first command parameter.
 * @retval TSS2_ESYS_RC_NO_ENCRYPT_PARAM: if one of the sessions has the
 *         'encrypt' attribute set and the command does not support encryption
 *          of the first response parameter.
 */
TSS2_RC Esys_Policy_AC_SendSelect(
    ESYS_CONTEXT *esysContext,
    ESYS_TR policySession1,
    ESYS_TR optionalSession2,
    ESYS_TR optionalSession3,
    TPM2B_NAME *objectName,
    TPM2B_NAME *authHandleName,
    TPM2B_NAME *acName,
    TPMI_YES_NO includeObject)
{
    TSS2_RC r;
    r = Esys_Policy_AC_SendSelect_Async(esysContext, policySession1,
                                        optionalSession2, optionalSession3,
                                        objectName, authHandleName, acName,
                                        includeObject);
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
    do
    {
        r = Esys_Policy_AC_SendSelect_Finish(esysContext);
        /* This is just debug information about the reattempt to finish the
           command */
        if (base_rc(r) == TSS2_BASE_RC_TRY_AGAIN)
            LOG_DEBUG("A layer below returned TRY_AGAIN: %" PRIx32
                      " => resubmitting command", r);
    } while (base_rc(r) == TSS2_BASE_RC_TRY_AGAIN);

    /* Restore the timeout value to the original value */
    esysContext->timeout = timeouttmp;
    return_if_error(r, "Esys Finish");

    return r;
}

/**
 * Asynchronous function for TPM2_Policy_AC_SendSelect
 *
 * This function invokes the TPM2_Policy_AC_SendSelect command in a
 * asynchronous variant. This means the function will return as soon as the
 * command has been sent downwards the stack to the TPM.
 *
 * @param[in,out] esysContext The ESYS_CONTEXT.
 * @param[in] policySession1 handle for the policy session being extended
 * @param[in] optionalSession2 Second session handle.
 * @param[in] optionalSession3 Third session handle.
 * @param[in] objectName Name of the Object to be sent
 * @param[in] authHandleName Name associated with authHandle used in the
 *                           TPM2_AC_Send() command
 * @param[in] acName Name of the Attached Component to which the Object will
 *                   be sent
 * @param[in] includeObject if SET, objectName will be included in the value in
 *                          policySession→policyDigest
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
 * @retval TSS2_ESYS_RC_NO_DECRYPT_PARAM: if one of the sessions has the
 *         'decrypt' attribute set and the command does not support encryption
 *         of the first command parameter.
 * @retval TSS2_ESYS_RC_NO_ENCRYPT_PARAM: if one of the sessions has the
 *         'encrypt' attribute set and the command does not support encryption
 *          of the first response parameter.
 */
TSS2_RC Esys_Policy_AC_SendSelect_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR policySession1,
    ESYS_TR optionalSession2,
    ESYS_TR optionalSession3,
    TPM2B_NAME *objectName,
    TPM2B_NAME *authHandleName,
    TPM2B_NAME *acName,
    TPMI_YES_NO includeObject)
{
    TSS2_RC r;
    LOG_TRACE("context=%p, policySession1=%"PRIx32 ", objectName=%p,"
              "authHandleName=%p, acName=%p",
              esysContext, policySession1, objectName, authHandleName, acName);
    TSS2L_SYS_AUTH_COMMAND auths;
    RSRC_NODE_T *policySessionNode;

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
    r = check_session_feasibility(policySession1, optionalSession2,
                                  optionalSession3, 0);
    return_state_if_error(r, _ESYS_STATE_INIT, "Check session usage");

    /* Retrieve the metadata objects for provided handles */
    r = esys_GetResourceObject(esysContext, policySession1, &policySessionNode);
    return_state_if_error(r, _ESYS_STATE_INIT, "policySession unknown.");

    r = Tss2_Sys_Policy_AC_SendSelect_Prepare(esysContext->sys,
                                              (policySessionNode == NULL)
                                              ? TPM2_RH_NULL
                                              : policySessionNode->rsrc.handle,
                                              objectName, authHandleName,
                                              acName, includeObject);
    return_state_if_error(r, _ESYS_STATE_INIT, "SAPI Prepare returned error.");

    /* Calculate the cpHash Values */
    r = init_session_tab(esysContext, policySession1, optionalSession2,
                         optionalSession3);
    return_state_if_error(r, _ESYS_STATE_INIT, "Initialize session resources");\
    iesys_compute_session_value(esysContext->session_tab[0], NULL, NULL);
    iesys_compute_session_value(esysContext->session_tab[1], NULL, NULL);
    iesys_compute_session_value(esysContext->session_tab[2], NULL, NULL);

    /* Generate the auth values and set them in the SAPI command buffer */
    r = iesys_gen_auths(esysContext, policySessionNode, NULL, NULL, &auths);
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

/**
 * Asynchronous finish function for TPM2_Policy_AC_SendSelect
 *
 * This function returns the results of a TPM2_Policy_AC_SendSelect command
 * invoked via Esys_Policy_AC_SendSelect_Finish. All non-simple output
 * parameters are allocated by the function's implementation.
 *
 * @param[in] esysContext The ESYS_CONTEXT.
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
 * @retval TSS2_ESYS_RC_NO_DECRYPT_PARAM: if one of the sessions has the
 *         'decrypt' attribute set and the command does not support encryption
 *         of the first command parameter.
 * @retval TSS2_ESYS_RC_NO_ENCRYPT_PARAM: if one of the sessions has the
 *         'encrypt' attribute set and the command does not support encryption
 *          of the first response parameter.
 */
TSS2_RC Esys_Policy_AC_SendSelect_Finish(
    ESYS_CONTEXT *esysContext)
{
    TSS2_RC r;
    LOG_TRACE("context=%p",
              esysContext);

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

    /*Receive the TPM response and handle resubmissions if necessary. */
    r = Tss2_Sys_ExecuteFinish(esysContext->sys, esysContext->timeout);
    if (base_rc(r) == TSS2_BASE_RC_TRY_AGAIN) {
        LOG_DEBUG("A layer below returned TRY_AGAIN: %" PRIx32, r);
        esysContext->state = _ESYS_STATE_SENT;
        return r;
    }
    /* This block handle the resubmission of TPM commands given a certain set of
     * TPM response codes. */
    if (r == TPM2_RC_RETRY || r == TPM2_RC_TESTING || r == TPM2_RC_YIELDED) {
        LOG_DEBUG("TPM returned RETRY, TESTING or YIELDED, which triggers a "
            "resubmission: %" PRIx32, r);
        if (esysContext->submissionCount++ >= _ESYS_MAX_SUBMISSIONS) {
            LOG_WARNING("Maximum number of (re)submissions has been reached.");
            esysContext->state = _ESYS_STATE_INIT;
            return r;
        }
        esysContext->state = _ESYS_STATE_RESUBMISSION;
        r = Tss2_Sys_ExecuteAsync(esysContext->sys);
        if (r != TSS2_RC_SUCCESS) {
            LOG_WARNING("Error attempting to resubmit");
            /* We do not set esysContext->state here but inherit the most recent
             * state of the _async function. */
            return r;
        }
        r = TSS2_ESYS_RC_TRY_AGAIN;
        LOG_DEBUG("Resubmission initiated and returning RC_TRY_AGAIN.");
        return r;
    }
    /* The following is the "regular error" handling. */
    if (iesys_tpm_error(r)) {
        LOG_WARNING("Received TPM Error");
        esysContext->state = _ESYS_STATE_INIT;
        return r;
    } else if (r != TSS2_RC_SUCCESS) {
        LOG_ERROR("Received a non-TPM Error");
        esysContext->state = _ESYS_STATE_INTERNALERROR;
        return r;
    }

    /*
     * Now the verification of the response (hmac check) and if necessary the
     * parameter decryption have to be done.
     */
    r = iesys_check_response(esysContext);
    return_state_if_error(r, _ESYS_STATE_INTERNALERROR,
                          "Error: check response");

    /*
     * After the verification of the response we call the complete function
     * to deliver the result.
     */
    r = Tss2_Sys_Policy_AC_SendSelect_Complete(esysContext->sys);
    return_state_if_error(r, _ESYS_STATE_INTERNALERROR,
                          "Received error from SAPI unmarshaling" );

    esysContext->state = _ESYS_STATE_INIT;

    return TSS2_RC_SUCCESS;
}
