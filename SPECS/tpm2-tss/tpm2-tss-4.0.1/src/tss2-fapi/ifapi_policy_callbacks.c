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

#include "fapi_util.h"
#include "fapi_policy.h"
#include "ifapi_helpers.h"
#include "fapi_crypto.h"
#include "ifapi_policy_instantiate.h"
#include "ifapi_policyutil_execute.h"
#include "ifapi_policy_execute.h"
#include "ifapi_policy_callbacks.h"
#include "tss2_mu.h"

#define LOGMODULE fapi
#include "util/log.h"
#include "util/aux_util.h"

/** Determine the auth object of a NV index.
 *
 * The auth object is determined depending on the object flags.
 *
 * @param[in]  nv_object The internal FAPI object representing the NV index.
 * @param[out] nv_index The ESYS handle of the NV index.
 * @param[out] auth_object The internal FAPI auth object.
 * @param[out] auth_index The ESYS handle of the auth object.
 * @retval TSS2_RC_SUCCESS on success.
 */
static void
get_nv_auth_object(
    IFAPI_OBJECT *nv_object,
    ESYS_TR nv_index,
    IFAPI_OBJECT *auth_object,
    ESYS_TR *auth_index)
{
    if (nv_object->misc.nv.public.nvPublic.attributes & TPMA_NV_PPREAD) {
        ifapi_init_hierarchy_object(auth_object, ESYS_TR_RH_PLATFORM);
        *auth_index = ESYS_TR_RH_PLATFORM;
    } else {
        if (nv_object->misc.nv.public.nvPublic.attributes & TPMA_NV_OWNERREAD) {
            ifapi_init_hierarchy_object(auth_object, ESYS_TR_RH_OWNER);
            *auth_index = ESYS_TR_RH_OWNER;
        } else {
            *auth_index = nv_index;
            *auth_object = *nv_object;
        }
    }
}

/** Get public data of a key from keystore.
 *
 * @param[in] path The relative path of the key.
 * @param[out] public The caller allocated public structure.
 * @param[in,out] ctx The context to access io and keystore module and to store
 *                      the io state.
 * @retval TSS2_RC_SUCCESS on success.
 * @retval TSS2_FAPI_RC_IO_ERROR: if the data cannot be loaded.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory for
 *         internal operations or return parameters.
 * @retval TSS2_FAPI_RC_BAD_TEMPLATE If the loaded template is not
 *         appropriate for this operation.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_TRY_AGAIN if an I/O operation is not finished yet and
 *         this function needs to be called again.
 * @retval TSS2_FAPI_RC_BAD_SEQUENCE if the context has an asynchronous
 *         operation already pending.
 * @retval TSS2_FAPI_RC_PATH_NOT_FOUND if a FAPI object path was not found
 *         during authorization.
 * @retval TSS2_FAPI_RC_KEY_NOT_FOUND if a key was not found.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE if an internal error occurred.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_NOT_PROVISIONED FAPI was not provisioned.
 * @retval TSS2_FAPI_RC_BAD_PATH if the path is used in inappropriate context
 *         or contains illegal characters.
 */
TSS2_RC
ifapi_get_key_public(
    const char *path,
    TPMT_PUBLIC *public,
    void *ctx)
{
    TSS2_RC r = TSS2_RC_SUCCESS;
    IFAPI_OBJECT object;
    FAPI_CONTEXT *context = ctx;

    switch (context->io_state) {
    statecase(context->io_state, IO_INIT)
        /* Prepare the loading of the object. */
        r = ifapi_keystore_load_async(&context->keystore, &context->io, path);
        return_if_error2(r, "Could not open: %s", path);
        fallthrough;

    statecase(context->io_state, IO_ACTIVE)
        /* Finalize or retry the reading and check the object type */
        r = ifapi_keystore_load_finish(&context->keystore, &context->io,
                                       &object);
        return_try_again(r);
        return_if_error(r, "read_finish failed");

        switch (object.objectType) {
        case IFAPI_KEY_OBJ:
            *public = object.misc.key.public.publicArea;
            break;
        case IFAPI_EXT_PUB_KEY_OBJ:
            *public = object.misc.ext_pub_key.public.publicArea;
            break;
        default:
            goto_error(r, TSS2_FAPI_RC_BAD_VALUE, "Object %s is not a key.",
                       cleanup, path);
        }
        break;

    statecasedefault_error(context->state, r, cleanup);
    }

cleanup:
    context->io_state = IO_INIT;
    ifapi_cleanup_ifapi_object(&object);
    return r;
}

/** Get TPM name of an object from  key keystore.
 *
 * @param[in] path The relative path of the object.
 * @param[out] name The caller allocate public structure.
 * @param[in,out] ctx The context to access io and keystore module and to store
 *                the io state.
 * @retval TSS2_RC_SUCCESS on success.
 * @retval TSS2_FAPI_RC_IO_ERROR: if the data cannot be loaded.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory for
 *         internal operations or return parameters.
 * @retval TSS2_FAPI_RC_BAD_TEMPLATE If the loaded template is not
 *         appropriate for this operation.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_TRY_AGAIN if an I/O operation is not finished yet and
 *         this function needs to be called again.
 * @retval TSS2_FAPI_RC_BAD_SEQUENCE if the context has an asynchronous
 *         operation already pending.
 * @retval TSS2_FAPI_RC_PATH_NOT_FOUND if a FAPI object path was not found
 *         during authorization.
 * @retval TSS2_FAPI_RC_KEY_NOT_FOUND if a key was not found.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE if an internal error occurred.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_NOT_PROVISIONED FAPI was not provisioned.
 * @retval TSS2_FAPI_RC_BAD_PATH if the path is used in inappropriate context
 *         or contains illegal characters.
 */
TSS2_RC
ifapi_get_object_name(
    const char *path,
    TPM2B_NAME *name,
    void *ctx)
{
    TSS2_RC r = TSS2_RC_SUCCESS;
    IFAPI_OBJECT object;
    FAPI_CONTEXT *context = ctx;

    switch (context->io_state) {
    statecase(context->io_state, IO_INIT)
        /* Prepare the loading of the object. */
        r = ifapi_keystore_load_async(&context->keystore, &context->io, path);
        return_if_error2(r, "Could not open: %s", path);
        fallthrough;

    statecase(context->io_state, IO_ACTIVE)
        /* Finalize or retry the reading and check the object type */
        r = ifapi_keystore_load_finish(&context->keystore, &context->io,
                                       &object);
        return_try_again(r);
        return_if_error(r, "read_finish failed");

        switch (object.objectType) {
        case IFAPI_KEY_OBJ:
            r = ifapi_get_name(&object.misc.key.public.publicArea,
                               (TPM2B_NAME *)name);
            break;
        case IFAPI_EXT_PUB_KEY_OBJ:
            r = ifapi_get_name(&object.misc.ext_pub_key.public.publicArea,
                               (TPM2B_NAME *)name);
            break;
        case IFAPI_NV_OBJ:
            r = ifapi_nv_get_name(&object.misc.nv.public.nvPublic, name);
            break;
        default:
            goto_error(r, TSS2_FAPI_RC_BAD_VALUE, "Invalid object %s.",
                       cleanup, path);
        }
        goto_if_error(r, "Get object name.", cleanup);
        break;

    statecasedefault(context->state);
    }

cleanup:
    context->io_state = IO_INIT;
    ifapi_cleanup_ifapi_object(&object);
    return r;
}

/** Get public data of a NV object from keystore.
 *
 * @param[in] path The relative path of the NV object. The path will
              be used to get the public from the keystore if no nv_index is
              passed.
 * @param[in] nv_index The index of the NV object. The index will be used to
 *            get the public data if nv_index > 0.
 * @param[out] nv_public The caller allocated public structure.
 * @param[in,out] ctx The context to access io and keystore module and to store
 *                the io state.
 * @retval TSS2_RC_SUCCESS on success.
 * @retval TSS2_FAPI_RC_IO_ERROR: if the data cannot be loaded.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory for
 *         internal operations or return parameters.
 * @retval TSS2_FAPI_RC_BAD_TEMPLATE If the loaded template is not
 *         appropriate for this operation.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_TRY_AGAIN if an I/O operation is not finished yet and
 *         this function needs to be called again.
 * @retval TSS2_FAPI_RC_BAD_SEQUENCE if the context has an asynchronous
 *         operation already pending.
 * @retval TSS2_FAPI_RC_PATH_NOT_FOUND if a FAPI object path was not found
 *         during authorization.
 * @retval TSS2_FAPI_RC_KEY_NOT_FOUND if a key was not found.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE if an internal error occurred.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_NOT_PROVISIONED FAPI was not provisioned.
 * @retval TSS2_FAPI_RC_BAD_PATH if the path is used in inappropriate context
 *         or contains illegal characters.
 */
TSS2_RC
ifapi_get_nv_public(
    const char *path,
    TPMI_RH_NV_INDEX nv_index,
    TPMS_NV_PUBLIC *nv_public,
    void *ctx)
{
    TSS2_RC r = TSS2_RC_SUCCESS;
    IFAPI_OBJECT object;
    FAPI_CONTEXT *context = ctx;
    TPM2B_NV_PUBLIC *nv_public_esys;
    ESYS_TR esys_tr;

    if (nv_index) {
        switch (context->read_nv_public_state) {
            statecase(context->read_nv_public_state, READ_NV_PUBLIC_INIT)
                r = Esys_TR_FromTPMPublic_Async(context->esys, nv_index, ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE);
                goto_if_error(r, "Error: tr from public", cleanup);
                fallthrough;

            statecase(context->read_nv_public_state, READ_NV_PUBLIC_GET_ESYS_TR)
                r = Esys_TR_FromTPMPublic_Finish(context->esys, &esys_tr);
                try_again_or_error_goto(r, "Error: tr from public finish", cleanup);

                r = Esys_NV_ReadPublic_Async(context->esys, esys_tr,
                                             ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE);
                goto_if_error(r, "Error: nv read public async", cleanup);
                fallthrough;

            statecase(context->read_nv_public_state, READ_NV_PUBLIC_GET_PUBLIC)
                r = Esys_NV_ReadPublic_Finish(context->esys,
                                              &nv_public_esys,
                                              NULL);
                try_again_or_error_goto(r, "Error: nv read public finish", cleanup);

                *nv_public = nv_public_esys->nvPublic;
                SAFE_FREE(nv_public_esys);
                context->io_state = IO_INIT;
                break;

            statecasedefault(context->state);
        }

    } else {
        switch (context->io_state) {
            statecase(context->io_state, IO_INIT)
                /* Prepare the loading of the NV object. */
                r = ifapi_keystore_load_async(&context->keystore, &context->io, path);
                return_if_error2(r, "Could not open: %s", path);
                fallthrough;

            statecase(context->io_state, IO_ACTIVE)
                /* Finalize or retry the reading and check the object type */
                r = ifapi_keystore_load_finish(&context->keystore, &context->io,
                                               &object);
                return_try_again(r);
                return_if_error(r, "read_finish failed");

                if (object.objectType != IFAPI_NV_OBJ) {
                    goto_error(r, TSS2_FAPI_RC_BAD_VALUE, "Object %s is not a key.",
                               cleanup, path);
                }

                *nv_public = object.misc.nv.public.nvPublic;
                context->io_state = IO_INIT;
                break;

            statecasedefault(context->state);
        }
    }

cleanup:
    context->io_state = IO_INIT;
    if (!nv_index) {
        ifapi_cleanup_ifapi_object(&object);
    }
    return r;
}

/** Read values of PCR registers and clear selection.
 *
 * @param[in] pcr_selection The registers to be read (with bank selection).
 * @param[out] out_pcr_selection The registers that were read (with bank selection).
 * @param[out] out_pcr_values The PCR values.
 * @param[in] ctx The FAPI_CONTEXT to access io and keystore module and to store
 *                the io state.
 * @retval TSS2_RC_SUCCESS on success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the input parameters had inappropriate values.
 * @retval TSS2_FAPI_RC_TRY_AGAIN: if the asynchronous operation is not yet
 *         complete. Call this function again later.
 * @retval TSS2_FAPI_RC_MEMORY if memory allocation failed.
 * @retval TSS2_FAPI_RC_BAD_SEQUENCE: if the context has an asynchronous
 *         operation already pending.
 */
TSS2_RC ifapi_read_pcr(
    TSS2_POLICY_PCR_SELECTION *pcr_selection,
    TPML_PCR_SELECTION *out_pcr_selection,
    TPML_DIGEST *out_pcr_digests,
    void *ctx) {

    TSS2_RC r = TSS2_RC_SUCCESS;
    FAPI_CONTEXT *context = ctx;
    UINT32 update_counter;
    TPML_PCR_SELECTION *out_selection = NULL;
    TPML_PCR_SELECTION *profile_selection;
    TPML_DIGEST *pcr_digests = NULL;
    size_t i, pcr;

    TPML_PCR_SELECTION in_pcr_selection = { 0 };

    switch (context->io_state) {
    statecase(context->io_state, IO_INIT)

        /* Raw selector without bank specifier, figure out bank and copy
         * the raw selector over to the input selector */
        if (pcr_selection->type == TSS2_POLICY_PCR_SELECTOR_PCR_SELECT) {

            /* Determine hash alg */
            profile_selection = &context->profiles.default_profile.pcr_selection;
            for (i = 0; i < profile_selection->count; i++) {
                for (pcr = 0; pcr < TPM2_MAX_PCRS; pcr++) {
                    uint8_t byte_idx = pcr / 8;
                    uint8_t flag = 1 << (pcr % 8);
                    /* Check whether PCR is used. */
                    if ((flag & profile_selection->pcrSelections[i].pcrSelect[byte_idx]) &&
                        (flag & pcr_selection->selections.pcr_select.pcrSelect[byte_idx])) {
                        in_pcr_selection.pcrSelections[0].hash = profile_selection->pcrSelections[i].hash;
                    }
                }
            }
            if (!in_pcr_selection.pcrSelections[0].hash) {
                /* hash for current pcr_select can't be determined */
                return_error(TSS2_FAPI_RC_BAD_VALUE,
                             "Policy PCR: pcr_select does not match profile.");
            }
            /* Only one bank will be used. The hash alg from profile will be used */
            in_pcr_selection.count = 1;
            in_pcr_selection.pcrSelections[0].sizeofSelect = pcr_selection->selections.pcr_select.sizeofSelect;
            for (i = 0; i < pcr_selection->selections.pcr_select.sizeofSelect; i++)
                in_pcr_selection.pcrSelections[0].pcrSelect[i] = pcr_selection->selections.pcr_select.pcrSelect[i];
        } else {
            /* we have specified selection with bank, so just copy it. */
            in_pcr_selection = pcr_selection->selections.pcr_selection;
        }

        /* Prepare the PCR Reading. */
        r = Esys_PCR_Read_Async(context->esys,
                                ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE,
                                &in_pcr_selection);
        return_if_error(r, "PCR Read");
        fallthrough;

    statecase(context->io_state, IO_ACTIVE)
        /* Finalize or retry the reading and check the object type */
        r = Esys_PCR_Read_Finish(context->esys,
                                 &update_counter,
                                 &out_selection,
                                 &pcr_digests);

        if (base_rc(r) == TSS2_BASE_RC_TRY_AGAIN)
            return TSS2_FAPI_RC_TRY_AGAIN;
        goto_if_error2(r, "PCR_Read_Finish", cleanup);

        /* copy to caller */
        *out_pcr_selection = *out_selection;
        *out_pcr_digests = *pcr_digests;

        context->io_state = IO_INIT;
        break;

    statecasedefault(context->state);
    }

cleanup:
    SAFE_FREE(out_selection);
    SAFE_FREE(pcr_digests);
    return r;
}

/** Callback for authorization of objects used by policy.
 *
 * @param[in] name The name of the object to be authorized.
 * @param[in] object_handle The ESYS handle of the used object.
 * @param[in] auth_handle will be used for object authorization. For
              keys it will we equal to the object handle.
 * @param[out] authSession The session used for object authorization.
 * @param[in,out] userdata The Fapi context which will be used for keystore
 *                access, and storing the policy execution state.
 *                the io state.
 * @retval TSS2_RC_SUCCESS on success.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE: if context or policy is NULL.
 * @retval TSS2_FAPI_RC_MEMORY if memory allocation failed.
 * @retval TSS2_FAPI_RC_TRY_AGAIN: if the asynchronous operation is not yet
 *         complete. Call this function again later.
 * @retval TSS2_FAPI_RC_BAD_SEQUENCE: if the context has an asynchronous
 *         operation already pending.
 * @retval TSS2_FAPI_RC_PATH_NOT_FOUND If a policy was not found.
 * @retval TSS2_FAPI_RC_KEY_NOT_FOUND If a key was not found.
 * @retval TSS2_FAPI_RC_IO_ERROR If an IO error occurred during reading
 *         a policy or a key.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE If an error in an used library
 *         occurred.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_AUTHORIZATION_UNKNOWN if a required authorization callback
 *         is not set.
 * @retval TSS2_FAPI_RC_AUTHORIZATION_FAILED if the authorization attempt fails.
 * @retval TSS2_FAPI_RC_POLICY_UNKNOWN if policy search for a certain policy digest
 *         was not successful.
 * @retval TSS2_ESYS_RC_* possible error codes of ESAPI.
 * @retval TSS2_FAPI_RC_BAD_PATH if the path is used in inappropriate context
 *         or contains illegal characters.
 * @retval TSS2_FAPI_RC_NOT_PROVISIONED FAPI was not provisioned.
 */
TSS2_RC
ifapi_policyeval_cbauth(
    TPM2B_NAME *name,
    ESYS_TR *object_handle,
    ESYS_TR *auth_handle,
    ESYS_TR *authSession,
    void *userdata)
{
    TSS2_RC r;
    FAPI_CONTEXT *fapi_ctx = userdata;
    IFAPI_POLICY_EXEC_CTX *current_policy;
    IFAPI_POLICY_EXEC_CB_CTX *cb_ctx;

    return_if_null(fapi_ctx, "Bad user data.", TSS2_FAPI_RC_BAD_REFERENCE);
    return_if_null(fapi_ctx->policy.policyutil_stack, "Policy not initialized.",
                   TSS2_FAPI_RC_BAD_REFERENCE);

    if (fapi_ctx->policy.util_current_policy) {
        /* Use the current policy in the policy stack. */
        current_policy = fapi_ctx->policy.util_current_policy->pol_exec_ctx;
    } else {
        /* Start with the bottom of the policy stack */
        current_policy = fapi_ctx->policy.policyutil_stack->pol_exec_ctx;
    }
    cb_ctx = current_policy->app_data;

    switch (cb_ctx->cb_state) {
        statecase(cb_ctx->cb_state, POL_CB_EXECUTE_INIT);
            cb_ctx->flush_handle = false;
            cb_ctx->auth_index = ESYS_TR_NONE;
            /* Search object with name in keystore. */
            r = ifapi_keystore_search_obj(&fapi_ctx->keystore, &fapi_ctx->io,
                                          name,
                                          &cb_ctx->object_path);
            FAPI_SYNC(r, "Search Object", cleanup);

            r = ifapi_keystore_load_async(&fapi_ctx->keystore, &fapi_ctx->io,
                                          cb_ctx->object_path);
            return_if_error2(r, "Could not open: %s", cb_ctx->object_path);
            SAFE_FREE(cb_ctx->object_path);
            fallthrough;

        statecase(cb_ctx->cb_state, POL_CB_READ_OBJECT);
            /* Get object from file */
            r = ifapi_keystore_load_finish(&fapi_ctx->keystore, &fapi_ctx->io,
                                           &cb_ctx->object);
            return_try_again(r);
            return_if_error(r, "read_finish failed");

            r = ifapi_initialize_object(fapi_ctx->esys, &cb_ctx->object);
            goto_if_error(r, "Initialize NV object", cleanup);

            if (cb_ctx->object.objectType == IFAPI_NV_OBJ) {
                /* NV Authorization */

                cb_ctx->nv_index = cb_ctx->object.public.handle;

                /* Determine the object used for authorization. */
                get_nv_auth_object(&cb_ctx->object,
                                   cb_ctx->object.public.handle,
                                   &cb_ctx->auth_object,
                                   &cb_ctx->auth_index);

                goto_if_error(r, "PolicySecret set authorization", cleanup);
                cb_ctx->cb_state = POL_CB_AUTHORIZE_OBJECT;

                cb_ctx->auth_object_ptr = &cb_ctx->auth_object;
                return TSS2_FAPI_RC_TRY_AGAIN;
            } else if (cb_ctx->object.objectType == IFAPI_HIERARCHY_OBJ) {
                cb_ctx->cb_state = POL_CB_AUTHORIZE_OBJECT;
                cb_ctx->auth_object_ptr = &cb_ctx->object;
                return TSS2_FAPI_RC_TRY_AGAIN;
            } else {
                cb_ctx->key_handle = cb_ctx->object.public.handle;
                if (cb_ctx->key_handle == ESYS_TR_NONE) {
                    cb_ctx->cb_state = POL_CB_LOAD_KEY;
                    return TSS2_FAPI_RC_TRY_AGAIN;
                }
            }
            fallthrough;

        statecase(cb_ctx->cb_state, POL_CB_AUTHORIZE_OBJECT);
            r = ifapi_authorize_object(fapi_ctx, cb_ctx->auth_object_ptr, authSession);
            return_try_again(r);
            goto_if_error(r, "Authorize  object.", cleanup);

            cb_ctx->cb_state = POL_CB_EXECUTE_INIT;
            break;
            /* FALLTHRU */

        statecase(cb_ctx->cb_state, POL_CB_LOAD_KEY);
            /* Prepare new context for loadkey in policy and skip session creation. */
            memset(&cb_ctx->load_ctx, 0, sizeof(IFAPI_LoadKey));
            cb_ctx->load_ctx.prepare_state = PREPARE_LOAD_KEY_INIT_KEY;
            memset(&cb_ctx->create_primary_ctx, 0, sizeof(IFAPI_CreatePrimary));
            fallthrough;

        statecase(cb_ctx->cb_state, POL_CB_LOAD_KEY_FINISH);
            cb_ctx->load_ctx_sav = fapi_ctx->loadKey;
            cb_ctx->create_primary_ctx_sav = fapi_ctx->createPrimary;
            fapi_ctx->loadKey = cb_ctx->load_ctx;
            fapi_ctx->createPrimary = cb_ctx->create_primary_ctx;
            cb_ctx->auth_object_ptr = &cb_ctx->load_ctx.auth_object;
            r = ifapi_load_key(fapi_ctx, ifapi_get_object_path(&cb_ctx->object),
                               &cb_ctx->auth_object_ptr);
            if (r == TSS2_RC_SUCCESS &&
                !cb_ctx->load_ctx.auth_object.misc.key.persistent_handle) {
                current_policy->flush_handle = true;
            }
            cb_ctx->load_ctx = fapi_ctx->loadKey;
            cb_ctx->create_primary_ctx = fapi_ctx->createPrimary;
            fapi_ctx->loadKey = cb_ctx->load_ctx_sav;
            fapi_ctx->createPrimary = cb_ctx->create_primary_ctx_sav;
            FAPI_SYNC(r, "Fapi load key.", cleanup);

            ifapi_cleanup_ifapi_object(&cb_ctx->object);
            cb_ctx->object = *cb_ctx->auth_object_ptr;
            fallthrough;

        statecase(cb_ctx->cb_state, POL_CB_AUTHORIZE_KEY);
            cb_ctx->load_ctx_sav = fapi_ctx->loadKey;
            cb_ctx->create_primary_ctx_sav = fapi_ctx->createPrimary;
            fapi_ctx->loadKey = cb_ctx->load_ctx;
            fapi_ctx->createPrimary = cb_ctx->create_primary_ctx;
            cb_ctx->object = *cb_ctx->auth_object_ptr;
            *auth_handle = cb_ctx->auth_object_ptr->public.handle;

            r = ifapi_authorize_object(fapi_ctx, cb_ctx->auth_object_ptr, authSession);
            return_try_again(r);
            fapi_ctx->loadKey = cb_ctx->load_ctx_sav;
            fapi_ctx->createPrimary = cb_ctx->create_primary_ctx;

            goto_if_error(r, "Authorize  object.", cleanup);

            cb_ctx->cb_state = POL_CB_EXECUTE_INIT;
            break;
            /* FALLTHRU */

        statecasedefault(cb_ctx->cb_state);
    }

    *object_handle = cb_ctx->object.public.handle;
    if (cb_ctx->object.objectType == IFAPI_NV_OBJ)
        *auth_handle = cb_ctx->auth_index;
    else
        *auth_handle = cb_ctx->object.public.handle;

    if (current_policy->policySessionSav != ESYS_TR_NONE)
        fapi_ctx->policy.session = current_policy->policySessionSav;

cleanup:
    ifapi_cleanup_ifapi_object(&cb_ctx->object);
    if (current_policy->policySessionSav
        && current_policy->policySessionSav != ESYS_TR_NONE)
        fapi_ctx->policy.session = current_policy->policySessionSav;
    return r;
}

/** Callback for loading a key object used by policy.
 *
 * @param[in] name The name of the object to be loaded.
 * @param[out] object_handle The ESYS handle of the used object.
 * @param[in,out] userdata The Fapi context which will be used for keystore
 *                access, and storing the policy execution state.
 *                the io state.
 * @retval TSS2_RC_SUCCESS on success.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE: if context or policy is NULL.
 * @retval TSS2_FAPI_RC_MEMORY if memory allocation failed.
 * @retval TSS2_FAPI_RC_TRY_AGAIN: if the asynchronous operation is not yet
 *         complete. Call this function again later.
 * @retval TSS2_FAPI_RC_BAD_SEQUENCE: if the context has an asynchronous
 *         operation already pending.
 * @retval TSS2_FAPI_RC_PATH_NOT_FOUND If a policy was not found.
 * @retval TSS2_FAPI_RC_KEY_NOT_FOUND If a key was not found.
 * @retval TSS2_FAPI_RC_IO_ERROR If an IO error occurred during reading
 *         a policy or a key.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE If an error in an used library
 *         occurred.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_AUTHORIZATION_UNKNOWN if a required authorization callback
 *         is not set.
 * @retval TSS2_FAPI_RC_AUTHORIZATION_FAILED if the authorization attempt fails.
 * @retval TSS2_FAPI_RC_POLICY_UNKNOWN if policy search for a certain policy digest
 *         was not successful.
 * @retval TSS2_ESYS_RC_* possible error codes of ESAPI.
 * @retval TSS2_FAPI_RC_BAD_PATH if the path is used in inappropriate context
 *         or contains illegal characters.
 * @retval TSS2_FAPI_RC_NOT_PROVISIONED FAPI was not provisioned.
 */
TSS2_RC
ifapi_policyeval_cbload_key(
    TPM2B_NAME *name,
    ESYS_TR *object_handle,
    void *userdata)
{
    TSS2_RC r;
    FAPI_CONTEXT *fapi_ctx = userdata;
    IFAPI_POLICY_EXEC_CTX *current_policy;
    IFAPI_POLICY_EXEC_CB_CTX *cb_ctx;

    return_if_null(fapi_ctx, "Bad user data.", TSS2_FAPI_RC_BAD_REFERENCE);
    return_if_null(fapi_ctx->policy.policyutil_stack, "Policy not initialized.",
                   TSS2_FAPI_RC_BAD_REFERENCE);

    if (fapi_ctx->policy.util_current_policy) {
        /* Use the current policy in the policy stack. */
        current_policy = fapi_ctx->policy.util_current_policy->pol_exec_ctx;
    } else {
        /* Start with the bottom of the policy stack */
        current_policy = fapi_ctx->policy.policyutil_stack->pol_exec_ctx;
    }
    cb_ctx = current_policy->app_data;

    switch (cb_ctx->cb_state) {
        statecase(cb_ctx->cb_state, POL_CB_EXECUTE_INIT);
            cb_ctx->flush_handle = false;
            cb_ctx->auth_index = ESYS_TR_NONE;
            /* Search object with name in keystore. */
            r = ifapi_keystore_search_obj(&fapi_ctx->keystore, &fapi_ctx->io,
                                          name,
                                          &cb_ctx->object_path);
            FAPI_SYNC(r, "Search Object", cleanup);

            r = ifapi_keystore_load_async(&fapi_ctx->keystore, &fapi_ctx->io,
                                          cb_ctx->object_path);
            return_if_error2(r, "Could not open: %s", cb_ctx->object_path);
            SAFE_FREE(cb_ctx->object_path);
            fallthrough;

        statecase(cb_ctx->cb_state, POL_CB_READ_OBJECT);
            /* Get object from file */
            r = ifapi_keystore_load_finish(&fapi_ctx->keystore, &fapi_ctx->io,
                                           &cb_ctx->object);
            return_try_again(r);
            return_if_error(r, "read_finish failed");

            r = ifapi_initialize_object(fapi_ctx->esys, &cb_ctx->object);
            goto_if_error(r, "Initialize key", cleanup);

            if (cb_ctx->object.objectType != IFAPI_KEY_OBJ) {
                goto_error(r, TSS2_FAPI_RC_BAD_VALUE,
                           "Key object expected", cleanup);
            }
            cb_ctx->key_handle = cb_ctx->object.public.handle;
            if (cb_ctx->key_handle != ESYS_TR_NONE) {
                break;
            }
            fallthrough;

        statecase(cb_ctx->cb_state, POL_CB_LOAD_KEY);
            /* Prepare new context for loadkey in policy and skip session creation. */
            memset(&cb_ctx->load_ctx, 0, sizeof(IFAPI_LoadKey));
            cb_ctx->load_ctx.prepare_state = PREPARE_LOAD_KEY_INIT_KEY;
            memset(&cb_ctx->create_primary_ctx, 0, sizeof(IFAPI_CreatePrimary));
            fallthrough;

        statecase(cb_ctx->cb_state, POL_CB_LOAD_KEY_FINISH);
            cb_ctx->load_ctx_sav = fapi_ctx->loadKey;
            cb_ctx->create_primary_ctx_sav = fapi_ctx->createPrimary;
            fapi_ctx->loadKey = cb_ctx->load_ctx;
            fapi_ctx->createPrimary = cb_ctx->create_primary_ctx;
            cb_ctx->auth_object_ptr = &cb_ctx->load_ctx.auth_object;
            r = ifapi_load_key(fapi_ctx, ifapi_get_object_path(&cb_ctx->object),
                               &cb_ctx->auth_object_ptr);
            if (r == TSS2_RC_SUCCESS &&
                !cb_ctx->load_ctx.auth_object.misc.key.persistent_handle) {
                current_policy->flush_handle = true;
            }
            cb_ctx->load_ctx = fapi_ctx->loadKey;
            cb_ctx->create_primary_ctx = fapi_ctx->createPrimary;
            fapi_ctx->loadKey = cb_ctx->load_ctx_sav;
            fapi_ctx->createPrimary = cb_ctx->create_primary_ctx_sav;
            FAPI_SYNC(r, "Fapi load key.", cleanup);

            ifapi_cleanup_ifapi_object(&cb_ctx->object);
            cb_ctx->object = *cb_ctx->auth_object_ptr;

            *object_handle = cb_ctx->auth_object_ptr->public.handle;

            cb_ctx->cb_state = POL_CB_EXECUTE_INIT;
            break;

       statecasedefault(cb_ctx->cb_state);
    }

    if (current_policy->policySessionSav != ESYS_TR_NONE)
        fapi_ctx->policy.session = current_policy->policySessionSav;

cleanup:
     ifapi_cleanup_ifapi_object(&cb_ctx->object);
    if (current_policy->policySessionSav
        && current_policy->policySessionSav != ESYS_TR_NONE)
        fapi_ctx->policy.session = current_policy->policySessionSav;
    return r;
}

/** Callback for branch selection of policy or.
 *
 * @param[in]  branches The list of policy branches.
 * @param[out] branch_idx The index of the selcted branch.
 * @param[in,out] userdata The Fapi context which will be used for keystore
 *                access, and storing the policy execution state.
 *                the io state.
 * @retval TSS2_RC_SUCCESS on success.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE: if context is NULL.
 * @retval TSS2_FAPI_RC_AUTHORIZATION_UNKNOWN if no branch selection callback is
 *         defined. This callback will be needed of or policies which have to be
 *         executed.
 * @retval TSS2_FAPI_RC_AUTHORIZATION_FAILED if the computed branch index
 *         delivered by the callback does not identify a branch.
 */
TSS2_RC
ifapi_branch_selection(
    TSS2_OBJECT *auth_object,
    const char *branch_names[8],
    size_t branch_count,
    size_t *branch_idx,
    void *userdata)
{
    TSS2_RC r;
    FAPI_CONTEXT *fapi_ctx = userdata;
    const char* object_path;

    return_if_null(fapi_ctx, "Bad user data.", TSS2_FAPI_RC_BAD_REFERENCE);

    /* Determine path of object to be authenticated. */
    return_if_null(auth_object, "No object passed.", TSS2_FAPI_RC_BAD_REFERENCE);

    return_if_null(fapi_ctx->callbacks.branch, "No branch selection callback", TSS2_FAPI_RC_AUTHORIZATION_UNKNOWN);

    object_path = ifapi_get_object_path(TSS2_OBJECT_TO_IFAPI_OBJECT(auth_object));

    r = fapi_ctx->callbacks.branch(object_path, "PolicyOR",
                                   &branch_names[0],
                                   branch_count,
                                   branch_idx,
                                   fapi_ctx->callbacks.branchData);
    return_if_error(r, "policyBranchSelectionCallback");

    return TSS2_RC_SUCCESS;
}

/** Callback for policy action.
 *
 * @param[in] action The name of the policy action.
 * @param[in,out] userdata The Fapi context which will be used for keystore
 *                access, and storing the policy execution state.
 *                the io state.
 * @retval TSS2_RC_SUCCESS on success.
 * @retval TSS2_FAPI_RC_AUTHORIZATION_UNKNOWN If the callback for branch selection is
 *         not defined. This callback will be needed of or policies have to be
 *         executed.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE If no user data is passed.
 */
TSS2_RC
ifapi_policy_action(
    const char *action,
    void *userdata)
{
    TSS2_RC r;
    FAPI_CONTEXT *fapi_ctx = userdata;
    IFAPI_OBJECT *auth_object;
    const char* object_path;

    return_if_null(fapi_ctx, "Bad user data.", TSS2_FAPI_RC_BAD_REFERENCE);

    if (!fapi_ctx->callbacks.action) {
        return_error(TSS2_FAPI_RC_AUTHORIZATION_UNKNOWN,
                     "No action callback");
    }

    /* Determine path of object to be authenticated. */
    auth_object = fapi_ctx->policy.util_current_policy->pol_exec_ctx->auth_object;
    return_if_null(auth_object, "No object passed.", TSS2_FAPI_RC_BAD_REFERENCE);

    object_path = ifapi_get_object_path(auth_object);
    r = fapi_ctx->callbacks.action(object_path, action,
                                   fapi_ctx->callbacks.actionData);
    return_if_error(r, "ifapi_policy_action callback");

    return TSS2_RC_SUCCESS;
}

/** Callback for signing a byte buffer.
 *
 * @param[in] key_pem The pem key used for signing operation.
 * @param[in] public_key_hint A human readable hint to denote which public
 *            key to use.
 * @param[in] key_pem_hash_alg The hash alg used for digest computation.
 * @param[in] buffer the byte array to be signed.
 * @param[in] buffer_size The size of the buffer to be signed.
 * @param[out] signature The signature in DER format.
 * @param[out] signature_size The size of the signature.
 * @param[in] userdata The user context to retrieve the signing function.
 * @retval TSS2_RC_SUCCESS on success.
 * @retval TSS2_FAPI_RC_AUTHORIZATION_UNKNOWN If the callback for signing is
 *         not defined.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE If no user data is passed.
 * @retval TSS2_FAPI_RC_TRY_AGAIN: if the callback operation is not yet
 *         complete. Call this function again later.
 */
TSS2_RC
ifapi_sign_buffer(
    char *key_pem,
    char *public_key_hint,
    TPMI_ALG_HASH key_pem_hash_alg,
    uint8_t *buffer,
    size_t buffer_size,
    const uint8_t **signature,
    size_t *signature_size,
    void *userdata)
{
    TSS2_RC r;
    FAPI_CONTEXT *fapi_ctx = userdata;
    IFAPI_OBJECT *auth_object;
    const char* object_path;

    return_if_null(fapi_ctx, "Bad user data.", TSS2_FAPI_RC_BAD_REFERENCE);

    /* Determine path of object to be authenticated. */
    auth_object = fapi_ctx->policy.util_current_policy->pol_exec_ctx->auth_object;
    return_if_null(auth_object, "No object passed.", TSS2_FAPI_RC_BAD_REFERENCE);

    object_path = ifapi_get_object_path(auth_object);

    if (!fapi_ctx->callbacks.sign) {
        return_error2(TSS2_FAPI_RC_AUTHORIZATION_UNKNOWN,
                      "No signature callback.");
    }
    r = fapi_ctx->callbacks.sign(object_path, "PolicySigned", key_pem,
                                 public_key_hint ? public_key_hint : "",
                                 key_pem_hash_alg,
                                 buffer, buffer_size,
                                 signature, signature_size,
                                 fapi_ctx->callbacks.signData);
    try_again_or_error(r, "Execute policy signature callback.");

    return TSS2_RC_SUCCESS;
}

static bool
cmp_policy_ref(TPM2B_NONCE *ref1, TPM2B_NONCE *ref2)
{
    if ((!ref1 || !ref1->size) && (!ref2 || !ref2->size)) {
        return true;
    }
    if (!ref1 || !ref1->size || !ref2 || !ref2->size)  {
        return false;
    }

    if (ref1->size != ref2->size) {
        return false;
    }

    if (memcmp(&ref1->buffer[0], &ref2->buffer[0], ref1->size) != 0) {
        return false;
    }

    return true;
}

/**  Check whether public data of key is assigned to policy.
 *
 * It will be checked whether policy was authorized by abort key with public
 * data of type TPMT_PUBLIC.
 *
 * @param[in] policy The policy to be checked.
 * @param[in] publicVoid The public information of the key.
 * @param[in] policyReferenceVoid The policy reverence to be compared.
 * @param[out] equal Switch whether check was successful.
 */
static TSS2_RC
equal_policy_authorization(
    TPMS_POLICY *policy,
    void *publicVoid,
    void *policyRefVoid,
    bool *equal)
{
    TPMT_PUBLIC *public = publicVoid;
    TPM2B_NONCE *policyRef = policyRefVoid;
    size_t i;
    TPML_POLICYAUTHORIZATIONS *authorizations = policy->policyAuthorizations;
    TSS2_RC r;
    TPM2B_PUBLIC pem_public;

    *equal = false;
    if (authorizations) {
        for (i = 0; i < authorizations->count; i++) {
            if (strcmp(authorizations->authorizations[i].type, "pem") == 0) {
                /* The public info has to be computed from the PEM key */
                r = ifapi_get_tpm2b_public_from_pem(
                         authorizations->authorizations[i].keyPEM, &pem_public);
                return_if_error(r, "Invalid PEM key.");

                if (pem_public.publicArea.type == TPM2_ALG_RSA) {
                    pem_public.publicArea.parameters.rsaDetail.scheme
                        = authorizations->authorizations[i].rsaScheme;
                }
                pem_public.publicArea.nameAlg = authorizations->authorizations[i].hashAlg;

                /* Check public information if key and policyRef */
                if (ifapi_TPMT_PUBLIC_cmp(public, &pem_public.publicArea) &&
                    cmp_policy_ref(policyRef,
                                   &authorizations->authorizations[i].policyRef)) {
                    *equal = true;
                    return TSS2_RC_SUCCESS;
                }
            } else
                /* Check public information if key and policyRef */
                if (ifapi_TPMT_PUBLIC_cmp(public, &authorizations->authorizations[i].key) &&
                    cmp_policy_ref(policyRef,
                                   &authorizations->authorizations[i].policyRef)) {
                    *equal = true;
                    return TSS2_RC_SUCCESS;
                }
        }
    }
    return TSS2_RC_SUCCESS;
}

/** Check whether policy digest can be found in policy.
 *
 * It will be tested whether the policy has been instatiated with the
 * passed digest.
 *
 * @param[in] policy The policy to be checked.
 * @param[in] authPolicyVoid The digest to be searched.
 * @param[in] nameAlgVoid The hash algorithm used for the digest computation.
 * @param[out] equal Switch whether check was successful.
 */
static TSS2_RC
compare_policy_digest(
    TPMS_POLICY *policy,
    void *authPolicyVoid,
    void *nameAlgVoid,
    bool *equal)
{
    TPM2B_DIGEST *authPolicy = authPolicyVoid;
    TPMI_ALG_HASH *hash_alg_ptr = nameAlgVoid;
    TPMI_ALG_HASH hash_alg = *hash_alg_ptr;
    size_t i;
    TPML_DIGEST_VALUES *digest_values;

    *equal = false;

    digest_values = &policy->policyDigests;

    if (digest_values) {
        for (i = 0; i < digest_values->count; i++) {
            if (digest_values->digests[i].hashAlg == hash_alg) {
                if (memcmp(&digest_values->digests[i].digest,
                           &authPolicy->buffer[0],
                           authPolicy->size))
                    continue;
                *equal = true;
                return TSS2_RC_SUCCESS;
            }
        }
    }
    return TSS2_RC_SUCCESS;
}

/** Search a policy file which fulfills a certain predicate.
 *
 * @param[in] context The context for storing the state information of the search
              process and the keystore paths.
 * @param[in] compare The function which will be used for comparison.
 * @param[in] all_objects Switch which determines wheter all policies fulfilling the
 *            the condition will be returned or only the first policy.
 * @param[in] object1 The first object used for comparison.
 * @param[in] object2 The second object used for comparison.
 * @param[out] policy_found The linked list with the policies fulfilling the condition.
 *
 * @retval TSS2_RC_SUCCESS on success.
 * @retval TSS2_FAPI_RC_POLICY_UNKNOWN if policy search for a certain policy digest
 *         was not successful.
 * @retval TSS2_FAPI_RC_TRY_AGAIN if an I/O operation is not finished yet and
 *         this function needs to be called again.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_IO_ERROR if an error occurred while accessing the
 *         object store.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE if an internal error occurred.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_BAD_PATH if the path is used in inappropriate context
 *         or contains illegal characters.
 * @retval TSS2_FAPI_RC_PATH_NOT_FOUND if a FAPI object path was not found
 *         during authorization.
 */
static TSS2_RC
search_policy(
    FAPI_CONTEXT *context,
    Policy_Compare_Object compare,
    bool all_objects,
    void *object1,
    void *object2,
    struct POLICY_LIST **policy_found)
{
    TSS2_RC r = TSS2_RC_SUCCESS;
    char *path;
    TPMS_POLICY policy = { 0 };
    bool found;
    struct POLICY_LIST *policy_object = NULL;
    struct POLICY_LIST *second;

    switch (context->fsearch.state) {
    case FSEARCH_INIT:
        LOG_DEBUG("** STATE ** FSEARCH_INIT");
        memset(&context->fsearch, 0, sizeof(IFAPI_FILE_SEARCH_CTX));
        /* Get the list of all files. */
        r = ifapi_keystore_list_all(&context->keystore, IFAPI_POLICY_DIR, &context->fsearch.pathlist,
                                    &context->fsearch.numPaths);
        return_if_error(r, "get entities.");
        context->fsearch.path_idx = context->fsearch.numPaths;

        context->fsearch.state = FSEARCH_OBJECT;
    /* FALLTHRU */

    case FSEARCH_OBJECT:
        LOG_DEBUG("** STATE ** FSEARCH_OBJECT");

        /* Test whether all files have been checked. */
        if (context->fsearch.path_idx == 0) {
            if (*policy_found) {
                context->fsearch.state = FSEARCH_INIT;
                for (size_t i = 0; i < context->fsearch.numPaths; i++) {
                    SAFE_FREE(context->fsearch.pathlist[i]);
                }
                SAFE_FREE(context->fsearch.pathlist);
                return TSS2_RC_SUCCESS;
            }
            goto_error(r, TSS2_FAPI_RC_POLICY_UNKNOWN, "Policy not found.", cleanup);
        }
        context->fsearch.path_idx -= 1;
        path = context->fsearch.pathlist[context->fsearch.path_idx];
        context->fsearch.current_path = path;
        LOG_DEBUG("Check file: %s %zu", path, context->fsearch.path_idx);

        /* Prepare policy loading. */
        r = ifapi_policy_store_load_async(&context->pstore, &context->io, path);
        goto_if_error2(r, "Can't open: %s", cleanup, path);

        context->fsearch.state = FSEARCH_READ;
    /* FALLTHRU */

    case FSEARCH_READ:
        LOG_DEBUG("** STATE ** FSEARCH_READ");
        /* Finalize policy loading if possible. */
        r = ifapi_policy_store_load_finish(&context->pstore, &context->io, &policy);
        return_try_again(r);
        goto_if_error(r, "read_finish failed", cleanup);

        /* Call the passed compare function. */
        r = compare(&policy, object1, object2, &found);
        if (found) {
            LOG_DEBUG("compare true  %s",
                      context->fsearch.pathlist[context->fsearch.path_idx]);
        } else {
            LOG_DEBUG("compare false  %s",
                      context->fsearch.pathlist[context->fsearch.path_idx]);
        }
        goto_if_error(r, "Invalid cipher object.", cleanup);

        if (!found) {
            if (!all_objects && context->fsearch.path_idx == 0) {
                /* All files checked, but no policy found. */
                context->fsearch.state = FSEARCH_INIT;
                ifapi_cleanup_policy(&policy);
                return TSS2_BASE_RC_POLICY_UNKNOWN;
            } else {
                /* Continue search. */
                context->fsearch.state = FSEARCH_OBJECT;
                ifapi_cleanup_policy(&policy);
                return TSS2_FAPI_RC_TRY_AGAIN;
            }
        }
        /* Extend linked list.*/
        policy_object = calloc(sizeof(struct POLICY_LIST), 1);
        return_if_null(policy_object, "Out of memory.", TSS2_FAPI_RC_MEMORY);

        strdup_check(policy_object->path, context->fsearch.current_path, r, cleanup);
        policy_object->policy = policy;
        if (*policy_found != NULL) {
            second = *policy_found;
            policy_object->next = second;
        }
        *policy_found = policy_object;

        if (context->fsearch.path_idx == 0) {
            context->fsearch.state = FSEARCH_INIT;
            /* Cleanup list of all paths. */
            for (size_t i = 0; i < context->fsearch.numPaths; i++) {
                SAFE_FREE(context->fsearch.pathlist[i]);
            }
            SAFE_FREE(context->fsearch.pathlist);
            return TSS2_RC_SUCCESS;
        }

        if (all_objects) {
            context->fsearch.state = FSEARCH_OBJECT;
            return TSS2_FAPI_RC_TRY_AGAIN;
        }

        break;

    default:
        context->state = _FAPI_STATE_INTERNALERROR;
        goto_error(r, TSS2_FAPI_RC_BAD_VALUE, "Invalid state for load key.", cleanup);
    }
    context->fsearch.state = FSEARCH_INIT;
    for (size_t i = 0; i < context->fsearch.numPaths; i++) {
        SAFE_FREE(context->fsearch.pathlist[i]);
    }
    SAFE_FREE(context->fsearch.pathlist);
    return TSS2_RC_SUCCESS;
cleanup:
    SAFE_FREE(policy_object);
    ifapi_cleanup_policy(&policy);
    for (size_t i = 0; i < context->fsearch.numPaths; i++) {
        SAFE_FREE(context->fsearch.pathlist[i]);
    }
    SAFE_FREE(context->fsearch.pathlist);
    context->fsearch.state = FSEARCH_INIT;
    return r;
}

/** Get policy digest for a certain hash alg.
 *
 * @param[in]  policy The policy with the digest list.
 * @param[in]  hashAlg The hash algorithm used for the digest computation.
 * @param[out] digest The digest matching hashAlg.
 * @retval TSS2_RC_SUCCESS on success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE if an internal error occurred.
 */
static TSS2_RC
get_policy_digest(TPMS_POLICY *policy,
                  TPMI_ALG_HASH hashAlg,
                  TPM2B_DIGEST *digest)
{
    size_t i;

    if (!(digest->size = ifapi_hash_get_digest_size(hashAlg))) {
        return_error2(TSS2_FAPI_RC_BAD_VALUE,
                      "Unsupported hash algorithm (%" PRIu16 ")", hashAlg);
    }

    for (i = 0; i < policy->policyDigests.count; i++) {
        if (policy->policyDigests.digests[i].hashAlg == hashAlg) {
            memcpy(&digest->buffer[0],
                   &policy->policyDigests.digests[i].digest, digest->size);
            return TSS2_RC_SUCCESS;
        }
    }
    return TSS2_FAPI_RC_GENERAL_FAILURE;
}

/** Get policy authorization for a certain public key
 *
 * @param[in]  policy The policy with the authorization.
 * @param[in]  public The public data of the key.
 * @param[out] signature The signature found in the authorization list.
 * @retval TSS2_RC_SUCCESS on success.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE if an internal error occurred.
 */
static TSS2_RC
get_policy_signature(
    TPMS_POLICY *policy,
    TPMT_PUBLIC *public,
    TPMT_SIGNATURE *signature)
{
    TSS2_RC r;
    size_t i;
    TPM2B_PUBLIC pem_public;
    TPML_POLICYAUTHORIZATIONS *authorizations = policy->policyAuthorizations;

    for (i = 0; i < policy->policyAuthorizations->count; i++) {
        if (strcmp(authorizations->authorizations[i].type, "pem") == 0) {
            /* The public info has to be computed from the PEM key */
            r = ifapi_get_tpm2b_public_from_pem(
                    authorizations->authorizations[i].keyPEM, &pem_public);
            return_if_error(r, "Invalid PEM key.");

            if (pem_public.publicArea.type == TPM2_ALG_RSA) {
                pem_public.publicArea.parameters.rsaDetail.scheme
                    = authorizations->authorizations[i].rsaScheme;
            }
            pem_public.publicArea.nameAlg = authorizations->authorizations[i].hashAlg;

            if (ifapi_TPMT_PUBLIC_cmp(public, &pem_public.publicArea)) {
                r = ifapi_der_sig_to_tpm(&pem_public.publicArea,
                                         authorizations->authorizations[i].pemSignature.buffer,
                                         authorizations->authorizations[i].pemSignature.size,
                                         authorizations->authorizations[i].hashAlg,
                                         signature);

                return_if_error(r, "Invalid signature.");

                return TSS2_RC_SUCCESS;
            }
        } else if (ifapi_TPMT_PUBLIC_cmp(public,
                                  &policy->policyAuthorizations->authorizations[i].key)) {
            /* The public info was already stored in the policy. */
            *signature = policy->policyAuthorizations->authorizations[i].signature;
            return TSS2_RC_SUCCESS;
        }
    }
    /* Appropriate authorization should always exist */
    return TSS2_FAPI_RC_GENERAL_FAILURE;
}

/** Cleanup a linked list of policies.
 *
 * @param[in] The linked list.
 */
static void
cleanup_policy_list(struct POLICY_LIST * list) {
    if (list) {
        struct POLICY_LIST * branch = list;
        while (branch) {
            struct POLICY_LIST *next = branch->next;
            /* Cleanup the policy stored in the list. */
            ifapi_cleanup_policy(&branch->policy);
            SAFE_FREE(branch->path);
            SAFE_FREE(branch);
            branch = next;
        }
    }
}

/** Callback for retrieving, selecting and execute a authorized policy.
 *
 * All policies authorized by a certain key will be retrieved and one policy
 * will be selected via a branch selection callback.
 *
 * @param[in] key_public the public data of the key which was used for policy
 *            authorization.
 * @param[in] hash_alg The hash algorithm used for policy computation.
 * @param[out] digest The policy digest of the authorized policy.
 * @param[out] signature The signature produced during policy authorization.
 * @param[in] userdata The user context to retrieve the policy.
 * @retval TSS2_RC_SUCCESS on success.
 * @retval TSS2_FAPI_RC_MEMORY: if it's not possible to allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE If no user data id passed or context stack
 *         is not initialized.
 * @retval TSS2_FAPI_RC_IO_ERROR If an error occurs during access to the policy
 *         store.
 * @retval TSS2_FAPI_RC_PATH_NOT_FOUND If a policy for a certain path was not found.
 * @retval TSS2_FAPI_RC_POLICY_UNKNOWN If policy search for a certain policy digest
 *         was not successful.
 * @retval TPM2_RC_BAD_AUTH If the authentication for an object needed for policy
 *         execution fails.
 * @retval TSS2_FAPI_RC_AUTHORIZATION_UNKNOWN if a required authorization callback
 *         is not set.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE if an internal error occurred.
 * @retval TSS2_FAPI_RC_TRY_AGAIN if an I/O operation is not finished yet and
 *         this function needs to be called again.
 * @retval TSS2_FAPI_RC_BAD_SEQUENCE if the context has an asynchronous
 *         operation already pending.
 * @retval TSS2_FAPI_RC_AUTHORIZATION_FAILED if the authorization attempt fails.
 * @retval TSS2_FAPI_RC_KEY_NOT_FOUND if a key was not found.
 * @retval TSS2_ESYS_RC_* possible error codes of ESAPI.
 * @retval TSS2_FAPI_RC_BAD_PATH if the path is used in inappropriate context
 *         or contains illegal characters.
 * @retval TSS2_FAPI_RC_NOT_PROVISIONED FAPI was not provisioned.
 */
TSS2_RC
ifapi_exec_auth_policy(
    TPMT_PUBLIC *key_public,
    TPMI_ALG_HASH hash_alg,
    TPM2B_DIGEST *digest,
    TPM2B_NONCE *policyRef,
    TPMT_SIGNATURE *signature,
    void *userdata)
{
    TSS2_RC r;
    FAPI_CONTEXT *fapi_ctx = userdata;
    IFAPI_POLICY_EXEC_CTX *current_policy;
    IFAPI_POLICY_EXEC_CB_CTX *cb_ctx;
    size_t n, i;
    struct POLICY_LIST *branch;
    const char **names = NULL;
    size_t branch_idx;
    bool policy_set = false;
    IFAPI_OBJECT *auth_object;
    const char* object_path;


    return_if_null(fapi_ctx, "Bad user data.", TSS2_FAPI_RC_BAD_REFERENCE);
    return_if_null(fapi_ctx->policy.policyutil_stack, "Policy not initialized.",
                   TSS2_FAPI_RC_BAD_REFERENCE);

    if (fapi_ctx->policy.util_current_policy) {
        /* Use the current policy in the policy stack. */
        current_policy = fapi_ctx->policy.util_current_policy->pol_exec_ctx;
    } else {
        /* Start with the bottom of the policy stack */
        current_policy = fapi_ctx->policy.policyutil_stack->pol_exec_ctx;
    }
    cb_ctx = current_policy->app_data;

    switch (cb_ctx->cb_state) {
        statecase(cb_ctx->cb_state, POL_CB_EXECUTE_INIT)
            current_policy->object_handle = ESYS_TR_NONE;
            current_policy->policy_list = NULL;
            fallthrough;

        statecase(cb_ctx->cb_state, POL_CB_SEARCH_POLICY)
            r = search_policy(fapi_ctx,
                              equal_policy_authorization, true,
                              key_public, policyRef,
                              &current_policy->policy_list);
            FAPI_SYNC(r, "Search policy", cleanup);

            if (current_policy->policy_list->next) {
                /* More than one policy has to be selected via
                   callback */
                if (!fapi_ctx->callbacks.branch) {
                    return_error(TSS2_FAPI_RC_AUTHORIZATION_UNKNOWN,
                                 "No branch selection callback");
                }
                n = 1;

                /* Count policies */
                for (branch = current_policy->policy_list; branch->next;
                     branch = branch->next)
                    n += 1;
                names = malloc(sizeof(char *) * n);
                return_if_null(names, "Out of memory.", TSS2_FAPI_RC_MEMORY);
                i = 0;
                branch = current_policy->policy_list;
                /* Compute name list for slectiion callback. */
                do {
                    names[i] = branch->path;
                    i += 1;
                    branch = branch->next;
                } while (branch);

                /* Determine path of object to be authenticated. */
                auth_object = fapi_ctx->policy.util_current_policy->pol_exec_ctx->auth_object;
                goto_if_null2(auth_object, "No object passed.", r, TSS2_FAPI_RC_BAD_REFERENCE,
                              cleanup);

                object_path = ifapi_get_object_path(auth_object);

                /* Policy selection */
                r = fapi_ctx->callbacks.branch(object_path, "PolicyAuthorize",
                                               &names[0], n, &branch_idx,
                                               fapi_ctx->callbacks.branchData);
                goto_if_error(r, "policyBranchSelectionCallback", cleanup);

                if (branch_idx >= n) {
                    goto_error(r, TSS2_FAPI_RC_BAD_VALUE, "Invalid branch number.",
                               cleanup);
                }
                /* Get policy from policy list */
                n = 0;
                branch = current_policy->policy_list;
                do {
                    if (n == branch_idx) {
                        cb_ctx->policy = &branch->policy;
                        policy_set = true;
                        break;
                    }
                    n += 1;
                    branch = branch->next;
                }  while (branch);

            } else {
                /* Only one policy found. */
                cb_ctx->policy = &current_policy->policy_list->policy;
                policy_set = true;
            }
            if (!policy_set) {
                goto_error(r, TSS2_FAPI_RC_GENERAL_FAILURE, "Policy could not be set.",
                           cleanup);
            }
            /* Prepare policy execution */
            r = ifapi_policyutil_execute_prepare(fapi_ctx, current_policy->hash_alg,
                                                 cb_ctx->policy);
            /* Next state will switch from prev context to next context. */
            goto_if_error(r, "Prepare policy execution.", cleanup);
            fallthrough;

        statecase(cb_ctx->cb_state, POL_CB_EXECUTE_SUB_POLICY)
            ESYS_TR session = current_policy->session;
            r = ifapi_policyutil_execute(fapi_ctx, &session);
            if (r == TSS2_FAPI_RC_TRY_AGAIN){
                SAFE_FREE(names);
                return r;
            }

            goto_if_error(r, "Execute policy.", cleanup);

            r = get_policy_signature(cb_ctx->policy, key_public,
                                     signature);
            goto_if_error(r, "Get authorization", cleanup);

            r = get_policy_digest(cb_ctx->policy, hash_alg, digest);
            goto_if_error(r, "Get authorization", cleanup);
            cb_ctx->cb_state = POL_CB_EXECUTE_INIT;
            break;

        statecasedefault_error(cb_ctx->state, r, cleanup);
    }
cleanup:
    SAFE_FREE(names);
    /* Check whether cleanup was executed. */
    if (fapi_ctx->policy.policyutil_stack)
        cleanup_policy_list(current_policy->policy_list);
    return r;
}

/** Callback for executing a policy identified by a digest stored in a nv object.
 *
 * @param[in] nv_public the public data of the nv object which stores the digest
 *            of the authorized policy.
 * @param[in] hash_alg The hash algorithm used for policy computation.
 * @param[in] userdata The user context to retrieve the policy.
 * @retval TSS2_RC_SUCCESS on success.
 * @retval TSS2_FAPI_RC_MEMORY: if it's not possible to allocate enough memory.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE If no user data id passed or context stack
 *         is not initialized.
 * @retval TSS2_FAPI_RC_IO_ERROR If an error occurs during access to the policy
 *         store.
 * @retval TSS2_FAPI_RC_PATH_NOT_FOUND If a policy for a certain path was not found.
 * @retval TSS2_FAPI_RC_POLICY_UNKNOWN If policy search for a certain policy digest was
 *         not successful.
 * @retval TPM2_RC_BAD_AUTH If the authentication for an object needed for policy
 *         execution fails.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_TRY_AGAIN if an I/O operation is not finished yet and
 *         this function needs to be called again.
 * @retval TSS2_FAPI_RC_BAD_SEQUENCE if the context has an asynchronous
 *         operation already pending.
 * @retval TSS2_FAPI_RC_KEY_NOT_FOUND if a key was not found.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE if an internal error occurred.
 * @retval TSS2_FAPI_RC_AUTHORIZATION_UNKNOWN if a required authorization callback
 *         is not set.
 * @retval TSS2_FAPI_RC_AUTHORIZATION_FAILED if the authorization attempt fails.
 * @retval TSS2_ESYS_RC_* possible error codes of ESAPI.
 * @retval TSS2_FAPI_RC_BAD_PATH if the path is used in inappropriate context
 *         or contains illegal characters.
 * @retval TSS2_FAPI_RC_NOT_PROVISIONED FAPI was not provisioned.
 */
TSS2_RC
ifapi_exec_auth_nv_policy(
    TPMS_NV_PUBLIC *nv_public,
    TPMI_ALG_HASH hash_alg,
    void *userdata)
{
    TSS2_RC r;
    TPM2B_MAX_NV_BUFFER *aux_data;
    FAPI_CONTEXT *fapi_ctx = userdata;
    IFAPI_POLICY_EXEC_CTX *current_policy;
    IFAPI_POLICY_EXEC_CB_CTX *cb_ctx;
    char *nv_path = NULL;
    ESYS_CONTEXT *esys_ctx;
    size_t digest_size, offset;
    TPMT_HA nv_policy;

    return_if_null(fapi_ctx, "Bad user data.", TSS2_FAPI_RC_BAD_REFERENCE);
    return_if_null(fapi_ctx->policy.policyutil_stack, "Policy not initialized.",
                   TSS2_FAPI_RC_BAD_REFERENCE);

    if (fapi_ctx->policy.util_current_policy) {
        /* Use the current policy in the policy stack. */
        current_policy = fapi_ctx->policy.util_current_policy->pol_exec_ctx;
    } else {
        /* Start with the bottom of the policy stack */
        current_policy = fapi_ctx->policy.policyutil_stack->pol_exec_ctx;
    }
    cb_ctx = current_policy->app_data;
    esys_ctx = fapi_ctx->esys;

    if (!(digest_size = ifapi_hash_get_digest_size(hash_alg))) {
        return_error2(TSS2_FAPI_RC_BAD_VALUE,
                      "Unsupported hash algorithm (%" PRIu16 ")", hash_alg);
    }

    switch (cb_ctx->cb_state) {
        statecase(cb_ctx->cb_state, POL_CB_EXECUTE_INIT)
            /*
             * Search a NV object with a certain NV indext stored in nv_public.
             * TODO Consider modifying internal APIs to use TPMS_NV_INDEX over TPM2B variant.
             */
            TPM2B_NV_PUBLIC tmp = { 0 };
            tmp.nvPublic = *nv_public;
            r = ifapi_keystore_search_nv_obj(&fapi_ctx->keystore, &fapi_ctx->io,
                                             &tmp, &nv_path);
            FAPI_SYNC(r, "Search Object", cleanup);

            r = ifapi_keystore_load_async(&fapi_ctx->keystore, &fapi_ctx->io, nv_path);
            SAFE_FREE(nv_path);
            return_if_error2(r, "Could not open: %s", nv_path);

            fallthrough;

        statecase(cb_ctx->cb_state, POL_CB_NV_READ)
            /* Get object from file */
            r = ifapi_keystore_load_finish(&fapi_ctx->keystore, &fapi_ctx->io,
                                           &cb_ctx->object);
            return_try_again(r);
            return_if_error(r, "read_finish failed");

            r = ifapi_initialize_object(esys_ctx, &cb_ctx->object);
            goto_if_error(r, "Initialize NV object", cleanup);

            current_policy->nv_index = cb_ctx->object.public.handle;
            ifapi_cleanup_ifapi_object(&cb_ctx->object);
            get_nv_auth_object(&cb_ctx->object,
                               current_policy->nv_index,
                               &current_policy->auth_objectNV,
                               &current_policy->auth_handle);
            fallthrough;

        statecase(cb_ctx->cb_state, POL_CB_AUTHORIZE_OBJECT)
            /* Authorize the NV object with the corresponding auth object. */
            r = ifapi_authorize_object(fapi_ctx, &cb_ctx->auth_object, &cb_ctx->session);
            return_try_again(r);
            goto_if_error(r, "Authorize  object.", cleanup);

            /* Prepare the reading of the NV index from TPM. */
            r = Esys_NV_Read_Async(esys_ctx,
                            current_policy->auth_handle, current_policy->nv_index,
                            cb_ctx->session, ESYS_TR_NONE, ESYS_TR_NONE,
                            sizeof(TPMI_ALG_HASH) + digest_size, 0);
            goto_if_error(r, "Unmarshal policy", cleanup);
            fallthrough;

        statecase(cb_ctx->cb_state, POL_CB_READ_NV_POLICY)
            /* Finalize the reading. */
            r = Esys_NV_Read_Finish(esys_ctx, &aux_data);
            try_again_or_error_goto(r, "NV read", cleanup);

            offset = 0;
            r = Tss2_MU_TPMT_HA_Unmarshal(&aux_data->buffer[0], aux_data->size,
                                          &offset, &nv_policy);
            Esys_Free(aux_data);
            goto_if_error(r, "Unmarshal policy", cleanup);

            cb_ctx->policy_digest.size = digest_size;
            memcpy(&cb_ctx->policy_digest.buffer[0], &nv_policy.digest, digest_size);
            fallthrough;

        statecase(cb_ctx->cb_state, POL_CB_SEARCH_POLICY)
            /* Search policy appropriate in object store */
            r = search_policy(fapi_ctx, compare_policy_digest, false,
                              &cb_ctx->policy_digest, &hash_alg,
                              &current_policy->policy_list);
            FAPI_SYNC(r, "Search policy", cleanup);

            if (!current_policy->policy_list) {
                goto_error(r, TSS2_FAPI_RC_POLICY_UNKNOWN, "Policy not found", cleanup);
            }
            /* Prepare policy execution */
            r = ifapi_policyutil_execute_prepare(fapi_ctx, current_policy->hash_alg,
                                                 &current_policy->policy_list->policy);
            return_if_error(r, "Prepare policy execution.");
            fallthrough;

        statecase(cb_ctx->cb_state, POL_CB_EXECUTE_SUB_POLICY)
            ESYS_TR session = current_policy->session;
            r = ifapi_policyutil_execute(fapi_ctx, &session);
            if (r == TSS2_FAPI_RC_TRY_AGAIN)
                return r;

            goto_if_error(r, "Execute policy.", cleanup);
            cb_ctx->cb_state = POL_CB_EXECUTE_INIT;
            break;

        statecasedefault_error(cb_ctx->state, r, cleanup);
    }
cleanup:
    cleanup_policy_list(current_policy->policy_list);
    SAFE_FREE(nv_path);
    return r;

}

/** Callback for getting the name of a key to be duplicated.
 *
 * @param[out] name the name of the object to be duplicated.
 * @param[in] userdata The user context to retrieve the key.
 * @retval TSS2_RC_SUCCESS on success.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE: if the context is not passed or the
 *         object to be duplicated is not set.
 */
TSS2_RC
ifapi_get_duplicate_name(
    TPM2B_NAME *name,
    void *userdata)
{
    FAPI_CONTEXT *fapi_ctx = userdata;

    return_if_null(fapi_ctx, "Bad user data.", TSS2_FAPI_RC_BAD_REFERENCE);
    return_if_null(fapi_ctx->duplicate_key, "Object for duplication no set.",
                   TSS2_FAPI_RC_BAD_REFERENCE);
    *name = fapi_ctx->duplicate_key->misc.key.name;
    return TSS2_RC_SUCCESS;
}
