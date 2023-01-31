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

/** One-Call function for TPM2_AC_Send. Used to send (copy) a loaded object
 * from the TPM to the Attached Component.
 *
 * @param[in,out] esysContext The ESYS_CONTEXT.
 * @param[in] sendObject handle of the object being sent to ac
 * @param[in] nvAuthHandle the handle indicating the source of the authorization
 *                         value
 * @param[in] optionalSession1 First session handle.
 * @param[in] optionalSession2 Second session handle.
 * @param[in] optionalSession3 Third session handle.
 * @param[in] ac handle indicating the attached component
 * @param[in] acDataIn Optional non sensitive information related to the object
 * @param[out] acDataOut May include AC specific data or information about an
 *                       error.
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
TSS2_RC Esys_AC_Send(
    ESYS_CONTEXT *esysContext,
    ESYS_TR sendObject,
    ESYS_TR nvAuthHandle,
    ESYS_TR optionalSession1,
    ESYS_TR optionalSession2,
    ESYS_TR optionalSession3,
    ESYS_TR ac,
    TPM2B_MAX_BUFFER *acDataIn,
    TPMS_AC_OUTPUT **acDataOut)
{
    TSS2_RC r;

    r = Esys_AC_Send_Async(esysContext, sendObject, nvAuthHandle,
                           optionalSession1, optionalSession2,
                           optionalSession3, ac, acDataIn);
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
        r = Esys_AC_Send_Finish(esysContext, acDataOut);
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

/** Asynchronous function for TPM2_AC_Send
 *
 * This function invokes the TPM2_AC_Send command in a asynchronous variant.
 * This means the function will return as soon as the command has been sent
 * downwards the stack to the TPM.
 *
 * @param[in] esysContext The ESYS_CONTEXT.
 * @param[in] sendObject handle of the object being sent to ac
 * @param[in] nvAuthHandle the handle indicating the source of the authorization
 *                     value
 * @param[in] optionalSession1 First session handle.
 * @param[in] optionalSession2 Second session handle.
 * @param[in] optionalSession3 Third session handle.
 * @param[in] ac handle indicating the attached component
 * @param[in] acDataIn Optional non sensitive information related to the object
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
TSS2_RC Esys_AC_Send_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR sendObject,
    ESYS_TR nvAuthHandle,
    ESYS_TR optionalSession1,
    ESYS_TR optionalSession2,
    ESYS_TR optionalSession3,
    ESYS_TR ac,
    TPM2B_MAX_BUFFER *acDataIn)
{
    TSS2_RC r;
    TSS2L_SYS_AUTH_COMMAND auths;
    LOG_TRACE("context=%p, sendObject=%"PRIx32 ", nvAuthHandle1=%"PRIx32 ","
              "ac=%"PRIx32 ", acDataIn=%p",
              esysContext, sendObject, nvAuthHandle, ac, acDataIn);

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
    r = check_session_feasibility(optionalSession1, optionalSession2,
                                  optionalSession3, 0);
    return_state_if_error(r, _ESYS_STATE_INIT, "Check session usage");

    /**
     * Convert inputs here
     *
     */
    TPMI_RH_AC tpmi_ac;
    TPMI_DH_OBJECT tpmi_sendObject;
    TPMI_RH_NV_AUTH tpmi_nvAuthHandle;
    r = iesys_handle_to_tpm_handle(ac, &tpmi_ac);
    if (r != TSS2_RC_SUCCESS)
        return r;
    r = iesys_handle_to_tpm_handle(sendObject, &tpmi_sendObject);
    if (r != TSS2_RC_SUCCESS)
        return r;
    r = iesys_handle_to_tpm_handle(nvAuthHandle, &tpmi_nvAuthHandle);
    if (r != TSS2_RC_SUCCESS)
        return r;
    /* Initial invocation of SAPI to prepare the command buffer with parameters */
    r = Tss2_Sys_AC_Send_Prepare(esysContext->sys, tpmi_sendObject,
                                 tpmi_nvAuthHandle, tpmi_ac, acDataIn);
    return_state_if_error(r, _ESYS_STATE_INIT, "SAPI Prepare returned error.");

    /* Calculate the cpHash Values */
    r = init_session_tab(esysContext, optionalSession1, optionalSession2,
                         optionalSession3);
    return_state_if_error(r, _ESYS_STATE_INIT, "Initialize session resources");\
    iesys_compute_session_value(esysContext->session_tab[0], NULL, NULL);
    iesys_compute_session_value(esysContext->session_tab[1], NULL, NULL);
    iesys_compute_session_value(esysContext->session_tab[2], NULL, NULL);

    /* Generate the auth values and set them in the SAPI command buffer */
    r = iesys_gen_auths(esysContext, NULL, NULL, NULL, &auths);
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

/** Asynchronous finish function for TPM2_AC_Send
 *
 * This function returns the results of a TPM2_AC_Send command invoked via
 * Esys_AC_Send_Finish. All non-simple output parameters are allocated by the
 * function's implementation.
 *
 * @param[in] esysContext The ESYS_CONTEXT.
 * @param[out] acDataOut May include AC specific data or information about an
 *                       error.
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
TSS2_RC Esys_AC_Send_Finish(
    ESYS_CONTEXT *esysContext, TPMS_AC_OUTPUT **acDataOut)
{
    TSS2_RC r;
    LOG_TRACE("context=%p, acDataOut=%p", esysContext, acDataOut);

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

    /* Allocate memory for response parameters */
    if (acDataOut != NULL) {
        *acDataOut = calloc(sizeof(TPMS_AC_OUTPUT), 1);
        if (*acDataOut == NULL) {
            return_error(TSS2_ESYS_RC_MEMORY, "Out of memory");
        }
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
    r = Tss2_Sys_AC_Send_Complete(esysContext->sys, (acDataOut != NULL)
                                  ? *acDataOut : NULL);
    goto_state_if_error(r, _ESYS_STATE_INTERNALERROR,
                        "Received error from SAPI unmarshaling" ,
                        error_cleanup);
    esysContext->state = _ESYS_STATE_INIT;

    return TSS2_RC_SUCCESS;

error_cleanup:
    if (acDataOut != NULL)
        SAFE_FREE(*acDataOut);

    return r;
}
