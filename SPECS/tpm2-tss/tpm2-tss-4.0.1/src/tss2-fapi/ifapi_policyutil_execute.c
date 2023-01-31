/* SPDX-License-Identifier: BSD-2-Clause */
/*******************************************************************************
 * Copyright 2018-2019, Fraunhofer SIT sponsored by Infineon Technologies AG
 * All rights reserved.
 *******************************************************************************/

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <string.h>
#include <stdlib.h>

#include "tss2_mu.h"
#include "fapi_util.h"
#include "fapi_crypto.h"
//#include "fapi_policy.h"
#include "ifapi_policy_execute.h"
#include "ifapi_policyutil_execute.h"
#include "ifapi_helpers.h"
#include "ifapi_json_deserialize.h"
#include "tpm_json_deserialize.h"
#include "ifapi_policy_callbacks.h"
#include "ifapi_policyutil_execute.h"
#define LOGMODULE fapi
#include "util/log.h"
#include "util/aux_util.h"

/** Create a new policy on policy stack.
 *
 * The structures for policy and callback execution are allocated
 * and the callbacks are assigned.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 */
static TSS2_RC
new_policy(
    FAPI_CONTEXT *context,
    TPMS_POLICY *policy,
    IFAPI_POLICYUTIL_STACK **current_policy)
{
    LOG_DEBUG("ADD POLICY");
    IFAPI_POLICY_EXEC_CTX *pol_exec_ctx;
    IFAPI_POLICY_EXEC_CB_CTX *pol_exec_cb_ctx;

    *current_policy = calloc(sizeof(IFAPI_POLICYUTIL_STACK), 1);
    if (!*current_policy) {
        return_error(TSS2_FAPI_RC_MEMORY, "Out of memory");
    }

    pol_exec_ctx = calloc(sizeof(IFAPI_POLICY_EXEC_CTX), 1);
    if (!pol_exec_ctx) {
        SAFE_FREE(*current_policy);
        return_error(TSS2_FAPI_RC_MEMORY, "Out of memory");
    }
    (*current_policy)->pol_exec_ctx = pol_exec_ctx;
    pol_exec_ctx->callbacks.cbauth = ifapi_policyeval_cbauth;
    pol_exec_ctx->callbacks.cbauth_userdata = context;
    pol_exec_ctx->callbacks.cbload = ifapi_policyeval_cbload_key;
    pol_exec_ctx->callbacks.cbload_userdata = context;
    pol_exec_ctx->callbacks.cbpolsel = ifapi_branch_selection;
    pol_exec_ctx->callbacks.cbpolsel_userdata = context;
    pol_exec_ctx->callbacks.cbsign = ifapi_sign_buffer;
    pol_exec_ctx->callbacks.cbsign_userdata = context;
    pol_exec_ctx->callbacks.cbauthpol = ifapi_exec_auth_policy;
    pol_exec_ctx->callbacks.cbauthpol_userdata = context;
    pol_exec_ctx->callbacks.cbauthnv = ifapi_exec_auth_nv_policy;
    pol_exec_ctx->callbacks.cbauthnv_userdata = context;
    pol_exec_ctx->callbacks.cbdup = ifapi_get_duplicate_name;
    pol_exec_ctx->callbacks.cbdup_userdata = context;
    pol_exec_ctx->callbacks.cbaction = ifapi_policy_action;
    pol_exec_ctx->callbacks.cbaction_userdata = context;

    pol_exec_cb_ctx = calloc(sizeof(IFAPI_POLICY_EXEC_CB_CTX), 1);
    if (!pol_exec_cb_ctx) {
        SAFE_FREE(*current_policy);
        return_error(TSS2_FAPI_RC_MEMORY, "Out of memory");
    }
    pol_exec_ctx->app_data = pol_exec_cb_ctx;
    pol_exec_ctx->policy = policy;
    if (!context->policy.policyutil_stack) {
        context->policy.policyutil_stack = *current_policy;
        context->policy.util_current_policy = *current_policy;
    } else {
        context->policy.util_current_policy->next = *current_policy;
        (*current_policy)->prev = context->policy.util_current_policy;
    }
    return TSS2_RC_SUCCESS;
}

/** Compute a new session which will be uses as policy session.
 * @retval TSS2_FAPI_RC_TRY_AGAIN if an I/O operation is not finished yet and
 *         this function needs to be called again.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE if an internal error occurred.
 * @retval TSS2_ESYS_RC_* possible error codes of ESAPI.
 */
static TSS2_RC
create_session(
    FAPI_CONTEXT *context,
    ESYS_TR *session,
    TPMI_ALG_HASH hash_alg)
{
    TSS2_RC r = TSS2_RC_SUCCESS;

    switch (context->policy.create_session_state) {
    case CREATE_SESSION_INIT:
        r = Esys_StartAuthSession_Async(context->esys,
                                        context->srk_handle ? context->srk_handle : ESYS_TR_NONE,
                                        ESYS_TR_NONE,
                                        ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE,
                                        NULL,
                                        TPM2_SE_POLICY,
                                        &context->profiles.default_profile.session_symmetric,
                                        hash_alg);

        return_if_error(r, "Creating session.");

        context->policy.create_session_state = WAIT_FOR_CREATE_SESSION;
        return TSS2_FAPI_RC_TRY_AGAIN;

    case WAIT_FOR_CREATE_SESSION:
        r = Esys_StartAuthSession_Finish(context->esys, session);
        if (r != TSS2_RC_SUCCESS)
            return r;
        context->policy.create_session_state = CREATE_SESSION_INIT;
        break;

    default:
        context->state = _FAPI_STATE_INTERNALERROR;
        goto_error(r, TSS2_FAPI_RC_GENERAL_FAILURE, "Invalid state for create session.",
                   cleanup);
    }

cleanup:
    return r;
}

/** Cleanup the current policy and adapt the policy stack.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE if an internal error occurred.
 */
static TSS2_RC
clear_current_policy(FAPI_CONTEXT *context)
{
    LOG_DEBUG("CLEAR POLICY");
    IFAPI_POLICYUTIL_STACK *prev_pol;
    if (!context->policy.util_current_policy) {
        return_error(TSS2_FAPI_RC_GENERAL_FAILURE, "No current policy.");
    }
    prev_pol = context->policy.util_current_policy->prev;

    SAFE_FREE(context->policy.util_current_policy->pol_exec_ctx->app_data);
    SAFE_FREE(context->policy.util_current_policy->pol_exec_ctx);
    SAFE_FREE(context->policy.util_current_policy);

    if (!prev_pol) {
        context->policy.policyutil_stack = NULL;
    } else {
        prev_pol->next = NULL;
    }
    return TSS2_RC_SUCCESS;
}

/** Prepare the execution of a new policy on policy stack.
 *
 * The context for the  policy utility, the policy execution and the needed
 * callbacks is initialized.
 * The policy execution will be prepared. In this step the list of policies
 * to be executed will be computed.
 * @param[in,out] context The fapi context with the pointer to the policy stack.
 * @param[in] hash_alg The hash algorithm used for the policy computation.
 * @param[in,out] policy The policy to be executed. Some policy elements will
 *                be used to store computed parameters needed for policy
 *                execution.
 * @retval TSS2_RC_SUCCESS on success.
 * @retval TSS2_FAPI_RC_AUTHORIZATION_UNKNOWN If the callback for branch selection is
 *         not defined. This callback will be needed of or policies have to be
 *         executed.
 * @retval TSS2_FAPI_RC_BAD_VALUE If the computed branch index delivered by the
 *         callback does not identify a branch.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE If no context is passed.
 *
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 * @retval TSS2_FAPI_RC_AUTHORIZATION_FAILED if the authorization attempt fails.
 * @retval TSS2_ESYS_RC_* possible error codes of ESAPI.
 */
TSS2_RC
ifapi_policyutil_execute_prepare(
    FAPI_CONTEXT *context,
    TPMI_ALG_HASH hash_alg,
    TPMS_POLICY *policy)
{
    TSS2_RC r;
    IFAPI_POLICYUTIL_STACK *current_policy, *prev_policy;

    return_if_null(context, "Bad context.", TSS2_FAPI_RC_BAD_REFERENCE);

    r = new_policy(context, policy, &current_policy);
    return_if_error(r, "Create new policy.");

    current_policy->pol_exec_ctx->auth_object = context->current_auth_object;

    r = ifapi_policyeval_execute_prepare(current_policy->pol_exec_ctx, hash_alg, policy);
    goto_if_error(r, "Prepare policy execution.", error);

    return r;

error:
    prev_policy = current_policy;
    if (context->policy.util_current_policy)
        clear_current_policy(context);
    context->policy.util_current_policy = prev_policy;
    return r;
}
/** State machine to Execute the TPM policy commands needed for the current policy.
 *
 * In the first step a session will be created if no session is passed.
 * In the second step the policy engine will execute the policy.
 *
 * @param[in,out] context The fapi context with the pointer to the policy stack.
 * @param[in,out] session The policy session to be extended or if the value is
 *                equal zero or ESYS_TR_NONE a new created session will been
 *                be stored in this parameter.
 * @retval TSS2_RC_SUCCESS on success.
 * @retval TSS2_FAPI_RC_MEMORY: if not enough memory can be allocated.
 * @retval TSS2_FAPI_RC_BAD_VALUE If wrong values are detected during execution.
 * @retval TSS2_FAPI_RC_IO_ERROR If an error occurs during access to the policy
 *         store.
 * @retval TSS2_FAPI_RC_POLICY_UNKNOWN If policy search for a certain policy digest was
 *         not successful.
 * @retval TSS2_FAPI_RC_BAD_TEMPLATE In a invalid policy is loaded during execution.
 * @retval TPM2_RC_BAD_AUTH If the authentication for an object needed for policy
 *         execution fails.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE if an internal error occurred.
 * @retval TSS2_FAPI_RC_TRY_AGAIN if an I/O operation is not finished yet and
 *         this function needs to be called again.
 * @retval TSS2_FAPI_RC_BAD_SEQUENCE if the context has an asynchronous
 *         operation already pending.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_PATH_NOT_FOUND if a FAPI object path was not found
 *         during authorization.
 * @retval TSS2_FAPI_RC_KEY_NOT_FOUND if a key was not found.
 * @retval TSS2_FAPI_RC_AUTHORIZATION_UNKNOWN if a required authorization callback
 *         is not set.
 * @retval TSS2_FAPI_RC_AUTHORIZATION_FAILED if the authorization attempt fails.
 * @retval TSS2_ESYS_RC_* possible error codes of ESAPI.
 * @retval TSS2_FAPI_RC_BAD_PATH if the path is used in inappropriate context
 *         or contains illegal characters.
 * @retval TSS2_FAPI_RC_NOT_PROVISIONED FAPI was not provisioned.
 */
TSS2_RC
ifapi_policyutil_execute(FAPI_CONTEXT *context, ESYS_TR *session)
{
    TSS2_RC r;
    IFAPI_POLICYUTIL_STACK *pol_util_ctx;
    TPMI_ALG_HASH hash_alg;

    if (context->policy.util_current_policy) {
        pol_util_ctx = context->policy.util_current_policy->next;
        context->policy.util_current_policy = context->policy.util_current_policy->next;
    } else {
        pol_util_ctx = context->policy.policyutil_stack;
        context->policy.util_current_policy = pol_util_ctx;
    }
    LOG_TRACE("Util context: %p", pol_util_ctx);
    if (!pol_util_ctx) {
        return_error(TSS2_FAPI_RC_GENERAL_FAILURE, "No policy util stack.");
    }

    switch (pol_util_ctx->state) {
        statecase(pol_util_ctx->state, POLICY_UTIL_INIT);
            LOG_DEBUG("Util session: %x", pol_util_ctx->policy_session);
            if (*session == ESYS_TR_NONE  || *session == 0) {
                /* Create a new  policy session for the current policy execution */
                hash_alg = pol_util_ctx->pol_exec_ctx->hash_alg;
                r = create_session(context, &pol_util_ctx->policy_session,
                                  hash_alg);
                if (base_rc(r) == TSS2_BASE_RC_TRY_AGAIN) {
                    context->policy.util_current_policy = pol_util_ctx->prev;
                    return TSS2_FAPI_RC_TRY_AGAIN;
                }
                goto_if_error(r, "Create policy session", error);

                pol_util_ctx->pol_exec_ctx->session = pol_util_ctx->policy_session;
                /* Save policy session for cleanup in error case. */
                context->policy_session = pol_util_ctx->policy_session;
            } else {
                pol_util_ctx->pol_exec_ctx->session = *session;
            }
            fallthrough;

        statecase(pol_util_ctx->state, POLICY_UTIL_EXEC_POLICY);
            r = ifapi_policyeval_execute(context->esys,
                                         pol_util_ctx->pol_exec_ctx,
                                         true);
            if (base_rc(r) == TSS2_BASE_RC_TRY_AGAIN) {
                context->policy.util_current_policy = pol_util_ctx->prev;
                return TSS2_FAPI_RC_TRY_AGAIN;
            }
            goto_if_error(r, "Execute policy.", error);

            break;

        statecasedefault(pol_util_ctx->state);
    }
    *session = pol_util_ctx->policy_session;

    pol_util_ctx = pol_util_ctx->prev;

    r = clear_current_policy(context);
    goto_if_error(r, "Clear policy.", error);

    context->policy.util_current_policy = pol_util_ctx;

    LOG_TRACE("success");
    return r;

error:
    pol_util_ctx = pol_util_ctx->prev;
    if (context->policy.util_current_policy)
        clear_current_policy(context);
    context->policy.util_current_policy = pol_util_ctx;
    return r;
}
