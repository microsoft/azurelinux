/* SPDX-License-Identifier: BSD-2-Clause */
/*******************************************************************************
 * Copyright 2017, Fraunhofer SIT sponsored by Infineon Technologies AG
 * All rights reserved.
 *******************************************************************************/

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif
#include <stdlib.h>

#include "tss2_esys.h"
#include "tss2_tctildr.h"

#include "esys_crypto.h"
#include "esys_iutil.h"
#include "tss2-tcti/tctildr-interface.h"
#define LOGMODULE esys
#include "util/log.h"
#include "util/aux_util.h"

/** Initialize an ESYS_CONTEXT for further use.
 *
 * Initialize an ESYS_CONTEXT that holds all the state and metadata information
 * during an interaction with the TPM.
 * If not specified, load a TCTI in this order:
 *       Library libtss2-tcti-default.so (link to the preferred TCTI)
 *       Library libtss2-tcti-tabrmd.so (tabrmd)
 *       Device /dev/tpmrm0 (kernel resident resource manager)
 *       Device /dev/tpm0 (hardware TPM)
 *       TCP socket localhost:2321 (TPM simulator)
 * @param esys_context [out] The ESYS_CONTEXT.
 * @param tcti [in] The TCTI context used to connect to the TPM (may be NULL).
 * @param abiVersion [in,out] The abi version to check and the abi version
 *        supported by this implementation (may be NULL).
 * @retval TSS2_ESYS_RC_SUCCESS if the function call was a success.
 * @retval TSS2_ESYS_RC_BAD_REFERENCE if esysContext is NULL.
 * @retval TSS2_ESYS_RC_MEMORY if the ESAPI cannot allocate enough memory to
 *         create the context.
 * @retval TSS2_RCs produced by lower layers of the software stack may be
 *         returned to the caller unaltered unless handled internally.
 */
TSS2_RC
Esys_Initialize(ESYS_CONTEXT ** esys_context, TSS2_TCTI_CONTEXT * tcti,
                TSS2_ABI_VERSION * abiVersion)
{
    TSS2_RC r;
    size_t syssize;

    _ESYS_ASSERT_NON_NULL(esys_context);
    *esys_context = NULL;

    /* Allocate memory for the ESYS context
     * After this errors must jump to cleanup_return instead of returning. */
    *esys_context = calloc(1, sizeof(ESYS_CONTEXT));
    return_if_null(*esys_context, "Out of memory.", TSS2_ESYS_RC_MEMORY);

    /* Store the application provided tcti to be return on Esys_GetTcti(). */
    (*esys_context)->tcti_app_param = tcti;

    /* Allocate memory for the SYS context */
    syssize = Tss2_Sys_GetContextSize(0);
    (*esys_context)->sys = calloc(1, syssize);
    goto_if_null((*esys_context)->sys, "Error: During malloc.",
                 TSS2_ESYS_RC_MEMORY, cleanup_return);

    /* If no tcti was provided, initialize the default one. */
    if (tcti == NULL) {
        r = Tss2_TctiLdr_Initialize (NULL, &tcti);
        goto_if_error(r, "Initialize default tcti.", cleanup_return);
    }

    /* Initialize the ESAPI */
    r = Tss2_Sys_Initialize((*esys_context)->sys, syssize, tcti, abiVersion);
    goto_if_error(r, "During syscontext initialization", cleanup_return);

    /* Use random number for initial esys handle value to provide pseudo
       namespace for handles */
    (*esys_context)->esys_handle_cnt = ESYS_TR_MIN_OBJECT + (rand() % 6000000);

    /*
     * setup crypto backend and initialize. Note: their is no userdata or callbacks
     * here, so NULL NULL
     */
    r = iesys_initialize_crypto_backend(&(*esys_context)->crypto_backend, NULL);
    goto_if_error(r, "Initialize crypto backend.", cleanup_return);

    return TSS2_RC_SUCCESS;

cleanup_return:
    /* If we created the tcti ourselves, we must clean it up */
    if ((*esys_context)->tcti_app_param == NULL && tcti != NULL) {
        Tss2_TctiLdr_Finalize(&tcti);
    }

    /* No need to finalize (*esys_context)->sys only free since
       it is the last goto in this function. */
    free((*esys_context)->sys);
    free(*esys_context);
    *esys_context = NULL;
    return r;
}

/** Finalize an ESYS_CONTEXT
 *
 * After interactions with the TPM the context holding the metadata needs to be
 * freed. Since additional internal memory allocations may have happened during
 * use of the context, it needs to be finalized correctly.
 * @param esys_context [in,out] The ESYS_CONTEXT. (will be freed and set to NULL)
 */
void
Esys_Finalize(ESYS_CONTEXT ** esys_context)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tctcontext = NULL;

    if (esys_context == NULL || *esys_context == NULL) {
        LOG_DEBUG("Finalizing NULL context.");
        return;
    }

    /* Flush from TPM and free all resource objects first */
    iesys_DeleteAllResourceObjects(*esys_context);

    /* If no tcti context was provided during initialization, then we need to
       finalize the tcti context. So we retrieve here before finalizing the
       SAPI context. */
    if ((*esys_context)->tcti_app_param == NULL) {
        r = Tss2_Sys_GetTctiContext((*esys_context)->sys, &tctcontext);
        if (r != TSS2_RC_SUCCESS) {
            LOG_ERROR("Internal error in Tss2_Sys_GetTctiContext.");
            tctcontext = NULL;
        }
    }

    /* Finalize the syscontext */
    Tss2_Sys_Finalize((*esys_context)->sys);
    free((*esys_context)->sys);

    /* If no tcti context was provided during initialization, then we need to
       finalize the tcti context here. */
    if (tctcontext != NULL) {
        Tss2_TctiLdr_Finalize(&tctcontext);
    }

    /* Free esys_context */
    free(*esys_context);
    *esys_context = NULL;
}

/** Return the used TCTI context.
 *
 * If a tcti context was passed into Esys_Initialize then this tcti context is
 * return. If NULL was passed in, then NULL will be returned.
 * This function is useful before Esys_Finalize to retrieve the tcti context and
 * perform a clean Tss2_Tcti_Finalize.
 * @param esys_context [in] The ESYS_CONTEXT.
 * @param tcti [out] The TCTI context used to connect to the TPM (may be NULL).
 * @retval TSS2_RC_SUCCESS on Success.
 * @retval TSS2_ESYS_RC_BAD_REFERENCE if esysContext or tcti is NULL.
 */
TSS2_RC
Esys_GetTcti(ESYS_CONTEXT * esys_context, TSS2_TCTI_CONTEXT ** tcti)
{
    _ESYS_ASSERT_NON_NULL(esys_context);
    _ESYS_ASSERT_NON_NULL(tcti);
    *tcti = esys_context->tcti_app_param;
    return TSS2_RC_SUCCESS;
}

/** Return the poll handles of the used TCTI.
 *
 * The connection to the TPM is held using a TCTI. These may optionally provide
 * handles that can be used to poll for incoming data. This is useful when
 * using the asynchronous function of ESAPI in an event-loop model.
 * @param esys_context [in] The ESYS_CONTEXT.
 * @param handles [out] The poll handles (callee-allocated, use free())
 * @param count [out] The number of poll handles.
 * @retval TSS2_RC_SUCCESS on Success.
 * @retval TSS2_ESYS_RC_BAD_REFERENCE if esysContext, handles or count is NULL.
 * @retval TSS2_RCs produced by lower layers of the software stack.
 */
TSS2_RC
Esys_GetPollHandles(ESYS_CONTEXT * esys_context,
                    TSS2_TCTI_POLL_HANDLE ** handles, size_t * count)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti_context;

    _ESYS_ASSERT_NON_NULL(esys_context);
    _ESYS_ASSERT_NON_NULL(handles);
    _ESYS_ASSERT_NON_NULL(count);

    /* Get the tcti-context to use */
    r = Tss2_Sys_GetTctiContext(esys_context->sys, &tcti_context);
    return_if_error(r, "Invalid SAPI or TCTI context.");

    /* Allocate the memory to hold the poll handles */
    r = Tss2_Tcti_GetPollHandles(tcti_context, NULL, count);
    return_if_error(r, "Error getting poll handle count.");
    *handles = calloc(*count, sizeof(TSS2_TCTI_POLL_HANDLE));
    return_if_null(*handles, "Out of memory.", TSS2_ESYS_RC_MEMORY);

    /* Retrieve the poll handles */
    r = Tss2_Tcti_GetPollHandles(tcti_context, *handles, count);
    return_if_error(r, "Error getting poll handles.");
    return r;
}

/** Set the timeout of Esys asynchronous functions.
 *
 * Sets the timeout for the _finish() functions in the asynchronous versions of
 * the Esys commands.
 * @param esys_context [in] The ESYS_CONTEXT.
 * @param timeout [in] The timeout in ms or -1 to block indefinately.
 * @retval TSS2_RC_SUCCESS on Success.
 * @retval TSS2_ESYS_RC_BAD_REFERENCE if esysContext is NULL.
 */
TSS2_RC
Esys_SetTimeout(ESYS_CONTEXT * esys_context, int32_t timeout)
{
    _ESYS_ASSERT_NON_NULL(esys_context);
    esys_context->timeout = timeout;
    return TSS2_RC_SUCCESS;
}

/** Helper function that returns sys contest from the give esys context.
 *
 * Function returns sys contest from the give esys context.
 * @param esys_context [in] ESYS context.
 * @param sys_context [out] SYS context.
 * @retval TSS2_RC_SUCCESS on Success.
 * @retval TSS2_ESYS_RC_BAD_REFERENCE if esys_context of sys_context are NULL.
 */
TSS2_RC
Esys_GetSysContext(ESYS_CONTEXT *esys_context, TSS2_SYS_CONTEXT **sys_context)
{
    if (esys_context == NULL || sys_context == NULL)
        return TSS2_ESYS_RC_BAD_REFERENCE;

    *sys_context = esys_context->sys;

    return TSS2_RC_SUCCESS;
}

/** Set Crypto Callbacks
 *
 * This is an advanced functionality that should be used with caution and by those
 * who know exactly what they are doing. This function provides the ability to set
 * and restore to the original state, the cryptographic callbacks that ESAPI
 * uses internally. This is useful for custom builds where runtime configurable
 * cryptography is beneficial over a configure time, --with-crypto=<ossl|mbed>
 * backend.
 *
 * @param[in] esysContext The ESYS_CONTEXT.
 * @param[in] callbacks The user define crypto callbacks or NULL for a reset to the
 *   ./configure time state.
 * @retval TSS2_ESYS_RC_BAD_REFERENCE is esysContext is NULL.
 * @retval TSS2_TSS2_ESYS_RC_CALLBACK_NULL if a required callback pointer is NULL.
 * @retval USER_DEFINED user defined errors if the user callback fails.
 * @note If ./configure --with-crypto=none, ESAPI functions that need crypto will
 * fail with TSS2_TSS2_ESYS_RC_CALLBACK_NULL until the application registers
 * callbacks. Under the same scenario, It will also fail if the application resets
 * the state back to the original state.
 */
TSS2_RC
Esys_SetCryptoCallbacks(
    ESYS_CONTEXT *esysContext,
    ESYS_CRYPTO_CALLBACKS *callbacks)
{
    LOG_TRACE("context=%p, callbacks=%p",
              esysContext, callbacks);

    /* Check context, sequence correctness and set state to error for now */
    if (esysContext == NULL) {
        LOG_ERROR("esyscontext is NULL.");
        return TSS2_ESYS_RC_BAD_REFERENCE;
    }

    return iesys_initialize_crypto_backend(&esysContext->crypto_backend, callbacks);
}

ESYS_TR
Esys_GetCryptoCallbacks(
    ESYS_CONTEXT *esysContext,
    ESYS_CRYPTO_CALLBACKS *callbacks)
{
    LOG_TRACE("context=%p, callbacks=%p",
              esysContext, callbacks);

    if (esysContext == NULL || callbacks == NULL) {
        LOG_ERROR("esyscontext or callbacks is NULL.");
        return TSS2_ESYS_RC_BAD_REFERENCE;
    }

    *callbacks = esysContext->crypto_backend;

    return TSS2_RC_SUCCESS;
}
