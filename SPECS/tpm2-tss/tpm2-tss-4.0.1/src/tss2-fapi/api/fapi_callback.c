/* SPDX-License-Identifier: BSD-2-Clause */
/*******************************************************************************
 * Copyright 2018-2019, Fraunhofer SIT sponsored by Infineon Technologies AG
 * All rights reserved.
 *******************************************************************************/

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#ifndef NO_DL
#include <dlfcn.h>
#endif /* NO_DL */
#include <stdlib.h>

#include "tss2_esys.h"
#include "tss2_fapi.h"
#include "fapi_int.h"

#define LOGMODULE fapi
#include "util/log.h"
#include "util/aux_util.h"

/**
 * This function registers a callback that will be invoked whenever the FAPI has
 * to decide which branch of a Policy-OR policy to use to authorize a particular
 * FAPI operation.
 *
 * @param[in,out] context The FAPI_CONTEXT
 * @param[in] callback The callback function for branch selection
 * @param[in] userData A pointer that is provided to all callback invocations
 *
 * @retval TSS2_RC_SUCCESS: if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE: if the context is NULL.
 * @retval TSS2_FAPI_RC_BAD_CONTEXT: if context corruption is detected.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory for
 *         internal operations or return parameters.
 * @retval TSS2_FAPI_RC_BAD_SEQUENCE: if the synchronous or Async functions are
 *         called while the context has another asynchronous operation
 *         outstanding, or the Finish function is called while the context does
 *         not have an appropriate asynchronous operation outstanding.
 * @retval TSS2_FAPI_RC_IO_ERROR: if the data cannot be saved.
 */
TSS2_RC
Fapi_SetBranchCB(
    FAPI_CONTEXT                      *context,
    Fapi_CB_Branch                     callback,
    void                              *userData)
{
    LOG_TRACE("called for context:%p", context);
    LOG_TRACE("Callback %p Userdata %p", callback, userData);

    /* Check for NULL parameters */
    check_not_null(context);

    /* Store the callback and userdata pointer. */
    context->callbacks.branch = callback;
    context->callbacks.branchData = userData;

    LOG_TRACE("finished");
    return TSS2_RC_SUCCESS;
}

/**
 * This function registers an application-defined function as a callback to
 * allow the TSS to get authorization values from the application.
 *
 * @param[in,out] context The FAPI_CONTEXT
 * @param[in] callback The callback function for auth value retrieval
 * @param[in] userData A pointer that is provided to all callback invocations
 *
 * @retval TSS2_RC_SUCCESS: if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE: if the context is NULL.
 * @retval TSS2_FAPI_RC_BAD_CONTEXT: if context corruption is detected.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory for
 *         internal operations or return parameters.
 * @retval TSS2_FAPI_RC_BAD_SEQUENCE: if the synchronous or Async functions are
 *         called while the context has another asynchronous operation
 *         outstanding, or the Finish function is called while the context does
 *         not have an appropriate asynchronous operation outstanding.
 * @retval TSS2_FAPI_RC_IO_ERROR: if the data cannot be saved.
 */
TSS2_RC
Fapi_SetAuthCB(
    FAPI_CONTEXT           *context,
    Fapi_CB_Auth           callback,
    void                   *userData)
{
    LOG_TRACE("called for context:%p", context);
    LOG_TRACE("Callback %p Userdata %p", callback, userData);

    /* Check for NULL parameters */
    check_not_null(context);

    /* Store the callback and userdata pointer. */
    context->callbacks.auth = callback;
    context->callbacks.authData = userData;

    LOG_TRACE("finished");
    return TSS2_RC_SUCCESS;
}

/**
 * Fapi_SetSignCB() registers an application-defined function as a callback to
 * allow the FAPI to get signatures authorizing use of TPM objects.
 *
 * @param[in,out] context The FAPI_CONTEXT
 * @param[in] callback The callback function for signing selection
 * @param[in] userData A pointer that is provided to all callback invocations
 *
 * @retval TSS2_RC_SUCCESS: if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE: if the context is NULL.
 * @retval TSS2_FAPI_RC_BAD_CONTEXT: if context corruption is detected.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory for
 *         internal operations or return parameters.
 * @retval TSS2_FAPI_RC_BAD_SEQUENCE: if the synchronous or Async functions are
 *         called while the context has another asynchronous operation
 *         outstanding, or the Finish function is called while the context does
 *         not have an appropriate asynchronous operation outstanding.
 * @retval TSS2_FAPI_RC_IO_ERROR: if the data cannot be saved.
 */
TSS2_RC
Fapi_SetSignCB(
    FAPI_CONTEXT                *context,
    Fapi_CB_Sign                callback,
    void                        *userData)
{
    LOG_TRACE("called for context:%p", context);
    LOG_TRACE("Callback %p Userdata %p", callback, userData);

    /* Check for NULL parameters */
    check_not_null(context);

    /* Store the callback and userdata pointer. */
    context->callbacks.sign = callback;
    context->callbacks.signData = userData;

    LOG_TRACE("finished");
    return TSS2_RC_SUCCESS;
}


/**
 * Fapi_SetActionCB() registers an application-defined function as a callback
 * that shall be called back upon encountering a policy action element.
 *
 * @param[in,out] context The FAPI_CONTEXT
 * @param[in] callback The callback function for branch selection
 * @param[in] userData A pointer that is provided to all callback invocations
 *
 * @retval TSS2_RC_SUCCESS: if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE: if the context is NULL.
 * @retval TSS2_FAPI_RC_BAD_CONTEXT: if context corruption is detected.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory for
 *         internal operations or return parameters.
 * @retval TSS2_FAPI_RC_BAD_SEQUENCE: if the synchronous or Async functions are
 *         called while the context has another asynchronous operation
 *         outstanding, or the Finish function is called while the context does
 *         not have an appropriate asynchronous operation outstanding.
 * @retval TSS2_FAPI_RC_IO_ERROR: if the data cannot be saved.
 */
TSS2_RC
Fapi_SetPolicyActionCB(
    FAPI_CONTEXT                *context,
    Fapi_CB_PolicyAction         callback,
    void                        *userData)
{
    LOG_TRACE("called for context:%p", context);
    LOG_TRACE("Callback %p Userdata %p", callback, userData);

    /* Check for NULL parameters */
    check_not_null(context);

    /* Store the callback and userdata pointer. */
    context->callbacks.action = callback;
    context->callbacks.actionData = userData;

    LOG_TRACE("finished");
    return TSS2_RC_SUCCESS;
}
