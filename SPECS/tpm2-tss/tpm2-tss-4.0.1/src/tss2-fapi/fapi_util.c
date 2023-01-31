/* SPDX-License-Identifier: BSD-2-Clause */
/*******************************************************************************
 * Copyright 2018-2019, Fraunhofer SIT sponsored by Infineon Technologies AG
 * All rights reserved.
 *******************************************************************************/

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <stdio.h>
#include <string.h>
#include <stdarg.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <ctype.h>
#include <dirent.h>

#include "tss2_mu.h"
#include "fapi_util.h"
#include "fapi_crypto.h"
#include "ifapi_helpers.h"
#include "ifapi_json_serialize.h"
#include "ifapi_json_deserialize.h"
#include "tpm_json_deserialize.h"
#include "fapi_policy.h"
#include "ifapi_policyutil_execute.h"
#define LOGMODULE fapi
#include "util/log.h"
#include "util/aux_util.h"

/** State machine for flushing objects.
 *
 * @param[in] context The FAPI_CONTEXT.
 * @param[in] handle of the object to be flushed.
 *
 * @retval TSS2_RC_SUCCESS on success.
 * @retval TSS2_ESYS_RC_* possible error codes of ESAPI.
 * @retval TSS2_FAPI_RC_TRY_AGAIN if an I/O operation is not finished yet and
 *         this function needs to be called again.
 * @retval TSS2_FAPI_RC_BAD_SEQUENCE if the context has an asynchronous
 *         operation already pending.
 */
TSS2_RC
ifapi_flush_object(FAPI_CONTEXT *context, ESYS_TR handle)
{
    TSS2_RC r = TSS2_RC_SUCCESS;

    if (handle == ESYS_TR_NONE)
        return r;

    switch (context->flush_object_state) {
    statecase(context->flush_object_state, FLUSH_INIT);
        r = Esys_FlushContext_Async(context->esys, handle);
        return_if_error(r, "Flush Object");
        fallthrough;

    statecase(context->flush_object_state, WAIT_FOR_FLUSH);
        r = Esys_FlushContext_Finish(context->esys);
        if (base_rc(r) == TSS2_BASE_RC_TRY_AGAIN)
            return TSS2_FAPI_RC_TRY_AGAIN;

        return_if_error(r, "FlushContext");

        context->flush_object_state = FLUSH_INIT;
        return TSS2_RC_SUCCESS;

    statecasedefault(context->flush_object_state);
    }
}

/** Preparation for getting a session handle.
 *
 * The corresponding async call be executed and a session secret for encryption
 * TPM2B parameters will be created.
 *
 * @param[in] esys The ESYS_CONTEXT.
 * @param[in] saltkey The key which will be used for the encryption of the session
 *            secret.
 * @param[in] profile The FAPI profile will be used to adjust the sessions symmetric
 *            parameters.
 * @param[in] hashAlg The hash algorithm used for the session.
 *
 * @retval TSS2_RC_SUCCESS on success.
 * @retval TSS2_ESYS_RC_* possible error codes of ESAPI.
 */
TSS2_RC
ifapi_get_session_async(ESYS_CONTEXT *esys, ESYS_TR saltkey, const IFAPI_PROFILE *profile,
                        TPMI_ALG_HASH hashAlg)
{
    TSS2_RC r;

    r = Esys_StartAuthSession_Async(esys, saltkey,
                                    ESYS_TR_NONE,
                                    ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE,
                                    NULL,
                                    TPM2_SE_HMAC, &profile->session_symmetric,
                                    hashAlg);
    return_if_error(r, "Creating session.");

    return TSS2_RC_SUCCESS;
}

/**  Call for getting a session handle and adjust session parameters.
 *
 * @param[in] esys The ESYS_CONTEXT.
 * @param[out] session The session handle.
 * @param[in] flags The flags to adjust the session attributes.
 *
 * @retval TSS2_RC_SUCCESS on success.
 * @retval TSS2_ESYS_RC_* possible error codes of ESAPI.
 */
TSS2_RC
ifapi_get_session_finish(ESYS_CONTEXT *esys, ESYS_TR *session,
                         TPMA_SESSION flags)
{
    TSS2_RC r;
    TPMA_SESSION sessionAttributes = 0;

    /* Check whether authorization callback is defined */

    r = Esys_StartAuthSession_Finish(esys, session);
    if (r != TSS2_RC_SUCCESS)
        return r;

    sessionAttributes |= flags;
    sessionAttributes |= TPMA_SESSION_CONTINUESESSION;

    r = Esys_TRSess_SetAttributes(esys, *session, sessionAttributes,
                                  0xff);
    return_if_error(r, "Set session attributes.");

    return TSS2_RC_SUCCESS;
}

/** Get the digest size of the policy of a FAPI object.
 *
 * @param[in] object The object with the correspodning policy.
 *
 * @retval The size of policy digest.
 * @retval 0 if The object does not have a policy.
 */
static size_t
policy_digest_size(IFAPI_OBJECT *object)
{
    switch (object->objectType) {
    case IFAPI_KEY_OBJ:
        return object->misc.key.public.publicArea.authPolicy.size;
    case IFAPI_NV_OBJ:
        return object->misc.nv.public.nvPublic.authPolicy.size;
    case IFAPI_HIERARCHY_OBJ:
        return object->misc.hierarchy.authPolicy.size;
    default:
        return 0;
    }
}

/** Add a object together with size as first element to a linked list.
 *
 * This function can e.g. used to add byte arrays together with their size
 * to a linked list.
 *
 * @param[in] object The object to be added.
 * @param[in] size The size of the object to be added.
 * @param[in,out] object_list The linked list to be extended.
 *
 * @retval TSS2_RC_SUCCESS if the object was added.
 * @retval TSS2_FAPI_RC_MEMORY If memory for the list extension cannot
 *         be allocated.
 */
static TSS2_RC
push_object_with_size_to_list(void *object, size_t size, NODE_OBJECT_T **object_list)
{
    TSS2_RC r;
    r = push_object_to_list(object, object_list);
    return_if_error(r, "Push object with size.");

    (*object_list)->size = size;

    return TSS2_RC_SUCCESS;
}

/** Initialize and expand the linked list representing a FAPI key path.
 *
 * From a passed key path the explicit key path will be determined. The
 * profile and the hierarchy will be added if necessary and the extension
 * is possible.
 *
 * @param[in]  context_profile The profile used for extension of no profile is
 *             part of the path.
 * @param[in]  ipath The implicit pathname which has to be extended.
 * @param[out] list_node1 The linked list for the passed key path without
 *             extensions.
 * @param[out] current_list_node The current node in the list list_node1,
 *             which represent the tail not processed.
 * @param[out] result The part of the new list which had been extended
 *             without the tail not processed.
 *
 * @retval TSS2_RC_SUCCESS: If the initialization was successful.
 * @retval TSS2_FAPI_RC_BAD_VALUE If an invalid path was passed.
 * @retval TSS2_FAPI_RC_MEMORY: if not enough memory can be allocated.
 * @retval TSS2_FAPI_RC_BAD_PATH if the path is used in inappropriate context
 *         or contains illegal characters.
 */
static TSS2_RC
init_explicit_key_path(
    const char *context_profile,
    const char *ipath,
    NODE_STR_T **list_node1,
    NODE_STR_T **current_list_node,
    NODE_STR_T **result)
{
    *list_node1 = split_string(ipath, IFAPI_FILE_DELIM);
    NODE_STR_T *list_node = *list_node1;
    char const *profile;
    char *hierarchy;
    TSS2_RC r = TSS2_RC_SUCCESS;

    *result = NULL;
    if (list_node == NULL) {
        LOG_ERROR("Invalid path");
        free_string_list(*list_node1);
        return TSS2_FAPI_RC_BAD_VALUE;
    }

    /* Processing of the profile. */
    if (strncmp("P_", list_node->str, 2) == 0) {
        profile = list_node->str;
        list_node = list_node->next;
    } else {
        profile = context_profile;
    }
    /* Create the initial node of the linked list. */
    *result = init_string_list(profile);
    if (*result == NULL) {
        free_string_list(*list_node1);
        LOG_ERROR("Out of memory");
        return TSS2_FAPI_RC_MEMORY;
    }
    if (list_node == NULL) {
        /* Storage hierarchy will be used as default. */
        hierarchy = "HS";
    } else {
        if (strcmp(list_node->str, "HN") == 0) {
            hierarchy = list_node->str;
            list_node = list_node->next;
        } else if (strcmp(list_node->str, "HS") == 0 ||
                   strcmp(list_node->str, "HE") == 0 ||
                   strcmp(list_node->str, "HN") == 0) {
            hierarchy = list_node->str;
            list_node = list_node->next;
        } else if (strcmp(list_node->str, "EK") == 0) {
            /* The hierarchy for an endorsement key will be added. */
            hierarchy = "HE";
        } else if (list_node->str != NULL &&
                   strcmp(list_node->str, "SRK") == 0) {
            /* The storage hierachy will be added. */
            hierarchy = "HS";
        } else {
            LOG_ERROR("Hierarchy cannot be determined.");
            r = TSS2_FAPI_RC_BAD_PATH;
            goto error;
        }
    }
    /* Add the used hierarchy to the linked list. */
    if (!add_string_to_list(*result, hierarchy)) {
        LOG_ERROR("Out of memory");
        r = TSS2_FAPI_RC_MEMORY;
        goto error;
    }
    if (list_node == NULL) {
        goto_error(r, TSS2_FAPI_RC_BAD_PATH, "Explicit path can't be determined.",
                   error);
    }

    /* Add the primary directory to the linked list. */
    if (!add_string_to_list(*result, list_node->str)) {
        LOG_ERROR("Out of memory");
        r = TSS2_FAPI_RC_MEMORY;
        goto error;
    }

    if (strcmp(hierarchy, "HS") == 0 && strcmp(list_node->str, "EK") == 0) {
        LOG_ERROR("Key EK cannot be create in the storage hierarchy.");
        r = TSS2_FAPI_RC_BAD_PATH;
        goto error;
    }

    if (strcmp(hierarchy, "HE") == 0 && strcmp(list_node->str, "SRK") == 0) {
        LOG_ERROR("Key EK cannot be create in the endorsement hierarchy.");
        r = TSS2_FAPI_RC_BAD_PATH;
        goto error;
    }

    if (strcmp(hierarchy, "HN") == 0 &&
        (strcmp(list_node->str, "SRK") == 0 || strcmp(list_node->str, "EK") == 0)) {
        LOG_ERROR("Key EK and SRK cannot be created in NULL hierarchy.");
        r = TSS2_FAPI_RC_BAD_PATH;
        goto error;
    }

    /* Return the rest of the path. */
    *current_list_node = list_node->next;
    return TSS2_RC_SUCCESS;

error:
    free_string_list(*result);
    *result = NULL;
    free_string_list(*list_node1);
    *list_node1 = NULL;
    return r;
}

/** Free first object of a linked list.
 *
 * Note: Referenced objects of the list have to be freed before.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
static TSS2_RC
pop_object_from_list(FAPI_CONTEXT *context, NODE_OBJECT_T **object_list)
{
    return_if_null(*object_list, "Pop from list.", TSS2_FAPI_RC_BAD_REFERENCE);

    NODE_OBJECT_T *head = *object_list;
    NODE_OBJECT_T *next = head->next;
    *object_list = next;
    ifapi_free_object(context, (void *)&head->object);
    free(head);
    return TSS2_RC_SUCCESS;
}

/** Get relative path of a FAPI object.
 *
 * @param[in] object The internal FAPI object.
 *
 * @retval The relative path of the object.
 * @retval NULL if no path is available.
 */
const char *
ifapi_get_object_path(IFAPI_OBJECT *object)
{
    if (object->rel_path)
        return object->rel_path;

    /* For hierarchies the path might not be set during reading
       from keystore. */
    if (object->objectType == IFAPI_HIERARCHY_OBJ) {
        switch (object->public.handle) {
        case ESYS_TR_RH_NULL:
            return "/HN";
        case ESYS_TR_RH_OWNER:
            return "/HS";
        case ESYS_TR_RH_ENDORSEMENT:
            return "/HE";
        case ESYS_TR_RH_LOCKOUT:
            return  "/LOCKOUT";
        }
    }
    return NULL;
}

/** Set authorization value for a primary key to be created.
 *
 * The callback which provides the auth value must be defined.
 *
 * @param[in,out] context The FAPI_CONTEXT.
 * @param[in]     object The auth value will be assigned to this object.
 * @param[in,out] inSensitive The sensitive data to store the auth value.
 *
 * @retval TSS2_RC_SUCCESS on success.
 * @retval TSS2_FAPI_RC_AUTHORIZATION_UNKNOWN If the callback for getting
 *         the auth value is not defined.
 */
TSS2_RC
ifapi_set_auth_primary(
    FAPI_CONTEXT *context,
    IFAPI_OBJECT *object,
    TPMS_SENSITIVE_CREATE *inSensitive)
{
    TSS2_RC r;
    const char *auth = NULL;
    const char *obj_path;

    memset(inSensitive, 0, sizeof(TPMS_SENSITIVE_CREATE));

    if (!object->misc.key.with_auth) {
        return TSS2_RC_SUCCESS;
    }

    obj_path = ifapi_get_object_path(object);

    /* Check whether callback is defined. */
    if (context->callbacks.auth) {
        r = context->callbacks.auth(obj_path, object->misc.key.description,
                                    &auth, context->callbacks.authData);
        return_if_error(r, "AuthCallback");
        if (auth != NULL) {
            inSensitive->userAuth.size = strlen(auth);
            memcpy(&inSensitive->userAuth.buffer[0], auth,
                   inSensitive->userAuth.size);
        }
        return TSS2_RC_SUCCESS;
    }
    SAFE_FREE(auth);
    return_error( TSS2_FAPI_RC_AUTHORIZATION_UNKNOWN, "Authorization callback not defined.");
}

/** Set authorization value for a FAPI object.
 *
 * The callback which provides the auth value must be defined.
 *
 * @param[in,out] context The FAPI_CONTEXT.
 * @param[in]     auth_object The auth value will be assigned to this object.
 * @param[in]     description The description will be passed to the callback
 *                which delivers the auth value.
 *
 * @retval TSS2_RC_SUCCESS on success.
 * @retval TSS2_FAPI_RC_AUTHORIZATION_UNKNOWN If the callback for getting
 *         the auth value is not defined.
 */
TSS2_RC
ifapi_set_auth(
    FAPI_CONTEXT *context,
    IFAPI_OBJECT *auth_object,
    const char *description)
{
    TSS2_RC r;
    const char *auth = NULL;
    TPM2B_AUTH authValue = {.size = 0,.buffer = {0} };
    const char *obj_path;

    obj_path = ifapi_get_object_path(auth_object);

    /* Check whether callback is defined. */
    if (context->callbacks.auth) {
        r = context->callbacks.auth(obj_path, description, &auth,
                                    context->callbacks.authData);
        return_if_error(r, "policyAuthCallback");
        if (auth != NULL) {
            authValue.size = strlen(auth);
            memcpy(&authValue.buffer[0], auth, authValue.size);
        }

        /* Store auth value in the ESYS object. */
        r = Esys_TR_SetAuth(context->esys, auth_object->public.handle, &authValue);
        return_if_error(r, "Set auth value.");

        if (auth_object->objectType == IFAPI_HIERARCHY_OBJ)
            auth_object->misc.hierarchy.authorized = true;

        return TSS2_RC_SUCCESS;
    }
    SAFE_FREE(auth);
    return_error( TSS2_FAPI_RC_AUTHORIZATION_UNKNOWN, "Authorization callback not defined.");
}

/** Preparation for getting a free handle after a start handle number.
 *
 * @param[in] fctx The FAPI_CONTEXT.
 * @param[in] handle The start value for handle search.
 *
 * @retval TSS2_RC_SUCCESS on success.
 * @retval TSS2_ESYS_RC_* possible error codes of ESAPI.
 */
TSS2_RC
ifapi_get_free_handle_async(FAPI_CONTEXT *fctx, TPM2_HANDLE *handle)
{
    TSS2_RC r = Esys_GetCapability_Async(fctx->esys,
                                         ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE,
                                         TPM2_CAP_HANDLES, *handle, 1);
    return_if_error(r, "GetCapability");
    return r;
}

/** Execution of get capability until a free handle is found.
 *
 * The get capability method is called until a free handle is found
 * or the max number of trials passe to the function is exeeded.
 *
 * @param[in] fctx The FAPI_CONTEXT.
 * @param[out] handle The free handle.
 * @param[in] max The maximal number of trials.
 *
 * @retval TSS2_RC_SUCCESS on success.
 * @retval TSS2_FAPI_RC_NV_TOO_SMALL if too many NV handles are defined.
 * @retval TSS2_ESYS_RC_* possible error codes of ESAPI.
 * @retval TSS2_FAPI_RC_TRY_AGAIN if an I/O operation is not finished yet and
 *         this function needs to be called again.
 */
TSS2_RC
ifapi_get_free_handle_finish(FAPI_CONTEXT *fctx, TPM2_HANDLE *handle,
                             TPM2_HANDLE max)
{
    TPMI_YES_NO moreData;
    TPMS_CAPABILITY_DATA *capabilityData = NULL;
    TSS2_RC r = Esys_GetCapability_Finish(fctx->esys,
                                          &moreData, &capabilityData);

    if (base_rc(r) == TSS2_BASE_RC_TRY_AGAIN)
        return TSS2_FAPI_RC_TRY_AGAIN;

    return_if_error(r, "GetCapability");

    if (capabilityData->data.handles.count == 0 ||
            capabilityData->data.handles.handle[0] != *handle) {
        SAFE_FREE(capabilityData);
        return TSS2_RC_SUCCESS;
    }
    SAFE_FREE(capabilityData);
    *handle += 1;
    if (*handle > max) {
        return_error(TSS2_FAPI_RC_NV_TOO_SMALL, "No NV index free.");
    }

    r = ifapi_get_free_handle_async(fctx, handle);
    return_if_error(r, "GetCapability");

    return TSS2_FAPI_RC_TRY_AGAIN;
}

/** Create a linked list of directories in the key store.
 *
 * If the absolute path in key store is not defined the list will
 * be extended if possible.
 *
 * @param[out] keystore The used keystore.
 * @param[in] ipath The implicit pathname, which might be extended.
 * @param[out] The linked list of directories in the explicit pathname.
 *
 * @retval TSS2_RC_SUCCESS If the keystore can be initialized.
 * @retval TSS2_FAPI_RC_IO_ERROR If the user part of the keystore can't be
 *         initialized.
 * @retval TSS2_FAPI_RC_MEMORY if memory could not be allocated.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_BAD_PATH if the path is used in inappropriate context
 *         or contains illegal characters.
 * @retval TSS2_FAPI_RC_PATH_NOT_FOUND if a FAPI object path was not found
 *         during authorization.
 */
static TSS2_RC
get_explicit_key_path(
    IFAPI_KEYSTORE *keystore,
    const char *ipath,
    NODE_STR_T **result)
{
    NODE_STR_T *list_node1 = NULL;
    NODE_STR_T *list_node = NULL;

    /* Extend the first part of the list if necessary. */
    TSS2_RC r = init_explicit_key_path(keystore->defaultprofile, ipath,
                                       &list_node1, &list_node, result);
    goto_if_error(r, "init_explicit_key_path", error);

    /* Extend the list with the tail of the initial unmodified list. */
    while (list_node != NULL) {
        if (!add_string_to_list(*result, list_node->str)) {
            LOG_ERROR("Out of memory");
            r = TSS2_FAPI_RC_MEMORY;
            goto error;
        }
        list_node = list_node->next;
    }
    free_string_list(list_node1);
    return TSS2_RC_SUCCESS;

error:
    if (*result)
        free_string_list(*result);
    if (list_node1)
        free_string_list(list_node1);
    return r;
}

/** Prepare the creation of a primary key.
 *
 * Depending on the parameters the creation of an endorsement or storage root key
 * will be prepared.
 *
 * @param[in] context The FAPI_CONTEXT.
 * @param[in] ktype The type of key TSS2_EK or TSS2_SRK.
 * @retval TSS2_RC_SUCCESS on success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if a wrong type was passed.
 * @retval TSS2_ESYS_RC_* possible error codes of ESAPI.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_TRY_AGAIN if an I/O operation is not finished yet and
 *         this function needs to be called again.
 * @retval TSS2_FAPI_RC_BAD_SEQUENCE if the context has an asynchronous
 *         operation already pending.
 * @retval TSS2_FAPI_RC_IO_ERROR if an error occurred while accessing the
 *         object store.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE if an internal error occurred.
 * @retval TSS2_FAPI_RC_PATH_NOT_FOUND if a FAPI object path was not found
 *         during authorization.
 * @retval TSS2_FAPI_RC_KEY_NOT_FOUND if a key was not found.
 * @retval TSS2_FAPI_RC_NOT_PROVISIONED FAPI was not provisioned.
 * @retval TSS2_FAPI_RC_BAD_PATH if the path is used in inappropriate context
 *         or contains illegal characters.
 */
TSS2_RC
ifapi_init_primary_async(FAPI_CONTEXT *context, TSS2_KEY_TYPE ktype)
{
    TSS2_RC r;
    TPMS_POLICY *policy;
    IFAPI_KEY *pkey = &context->createPrimary.pkey_object.misc.key;

    r = TSS2_RC_SUCCESS;

    if (ktype == TSS2_EK) {
        pkey->ek_profile = TPM2_YES;
        /* Values set according to EK credential profile. */
        if (context->cmd.Provision.public_templ.public.publicArea.type == TPM2_ALG_RSA) {
            if (pkey->nonce.size) {
                memcpy(context->cmd.Provision.public_templ.public.publicArea.unique.rsa.buffer,
                       &pkey->nonce.buffer[0], pkey->nonce.size);
            }
            if ((context->cmd.Provision.public_templ.public.publicArea.objectAttributes & TPMA_OBJECT_USERWITHAUTH))
                context->cmd.Provision.public_templ.public.publicArea.unique.rsa.size = 0;
            else
                context->cmd.Provision.public_templ.public.publicArea.unique.rsa.size = 256;
        } else if (context->cmd.Provision.public_templ.public.publicArea.type == TPM2_ALG_ECC) {
            if (pkey->nonce.size) {
                memcpy(context->cmd.Provision.public_templ.public.publicArea.unique.ecc.x.buffer,
                       &pkey->nonce.buffer[0], pkey->nonce.size);
            }
            if ((context->cmd.Provision.public_templ.public.publicArea.objectAttributes & TPMA_OBJECT_USERWITHAUTH)) {
                context->cmd.Provision.public_templ.public.publicArea.unique.ecc.x.size = 0;
                context->cmd.Provision.public_templ.public.publicArea.unique.ecc.y.size = 0;
            } else {
                context->cmd.Provision.public_templ.public.publicArea.unique.ecc.x.size = 32;
                context->cmd.Provision.public_templ.public.publicArea.unique.ecc.y.size = 32;
            }
        }
        policy = context->profiles.default_profile.ek_policy;
    } else if (ktype == TSS2_SRK) {
        policy = context->profiles.default_profile.srk_policy;
    } else {
        return_error(TSS2_FAPI_RC_BAD_VALUE,
                     "Invalid key type. Only EK or SRK allowed");
    }

    if (policy) {
        /* Duplicate policy to prevent profile policy from cleanup. */
        policy = ifapi_copy_policy(policy);
        return_if_null(policy, "Out of memory.", TSS2_FAPI_RC_MEMORY);

        r = ifapi_calculate_tree(context, NULL, /**< no path needed */
                                 policy,
                                 context->profiles.default_profile.nameAlg,
                                 &context->cmd.Provision.digest_idx,
                                 &context->cmd.Provision.hash_size);
        if (r) {
            LOG_ERROR("Policy calculation");
            SAFE_FREE(policy);
            return r;
        }
        /* Check whether policy digest defined for key matches the computed policy. */
        if (context->cmd.Provision.public_templ.public.publicArea.authPolicy.size) {
            if (context->cmd.Provision.public_templ.public.publicArea.authPolicy.size
                != context->cmd.Provision.hash_size ||
                memcmp(&policy->policyDigests.digests[context->policy.digest_idx].digest,
                       &context->cmd.Provision.public_templ.public.publicArea.authPolicy.buffer[0],
                       context->cmd.Provision.hash_size) != 0) {
                SAFE_FREE(policy);
                return_error(TSS2_FAPI_RC_BAD_VALUE, "EK Policy does not match policy defined in profile.");
            }
        }
        context->cmd.Provision.public_templ.public.publicArea.authPolicy.size =
            context->cmd.Provision.hash_size;
        memcpy(&context->cmd.Provision.public_templ.public.publicArea.authPolicy.buffer[0],
               &policy->policyDigests.digests[context->policy.digest_idx].digest,
               context->cmd.Provision.hash_size);
    }
    context->createPrimary.pkey_object.policy = policy;
    context->createPrimary.pkey_object.objectType = IFAPI_KEY_OBJ;

    memset(&context->cmd.Provision.inSensitive, 0, sizeof(TPM2B_SENSITIVE_CREATE));
    memset(&context->cmd.Provision.outsideInfo, 0, sizeof(TPM2B_DATA));
    memset(&context->cmd.Provision.creationPCR, 0, sizeof(TPML_PCR_SELECTION));

    context->primary_state = PRIMARY_AUTHORIZE_HIERARCHY;
    return r;
}

/** Finalize the creation of a primary key.
 *
 * Depending on the parameters the creation of an endorsement key or a storage root key
 * will be finalized. The created object with the all information needed by FAPI will
 * be stored in the FAPI context.
 *
 * @param[in] context The FAPI_CONTEXT.
 * @param[in] ktype The type of key TSS2_EK or TSS2_SRK.
 * @param[in,out] hierarchy The hiearchy used for primary creation.
 *
 * @retval TSS2_RC_SUCCESS on success.
 * @retval TSS2_FAPI_RC_TRY_AGAIN if the execution cannot be completed.
 * @retval TSS2_FAPI_RC_BAD_VALUE if a wrong type was passed.
 * @retval TSS2_ESYS_RC_* possible error codes of ESAPI.
 * @retval TSS2_FAPI_RC_AUTHORIZATION_UNKNOWN if a required authorization callback
 *         is not set.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE if an internal error occurred.
 * @retval TSS2_FAPI_RC_BAD_SEQUENCE if the context has an asynchronous
 *         operation already pending.
 * @retval TSS2_FAPI_RC_AUTHORIZATION_FAILED if the authorization attempt fails.
 * @retval TSS2_FAPI_RC_PATH_NOT_FOUND if a FAPI object path was not found
 *         during authorization.
 * @retval TSS2_FAPI_RC_KEY_NOT_FOUND if a key was not found.
 * @retval TSS2_FAPI_RC_IO_ERROR if an error occured while accessing the
 *         object store.
 * @retval TSS2_FAPI_RC_POLICY_UNKNOWN if policy search for a certain policy digest
 *         was not successful.
 */
TSS2_RC
ifapi_init_primary_finish(FAPI_CONTEXT *context, TSS2_KEY_TYPE ktype, IFAPI_OBJECT *hierarchy)
{
    TSS2_RC r;
    ESYS_TR primaryHandle;
    TPM2B_PUBLIC *outPublic = NULL;
    TPM2B_CREATION_DATA *creationData = NULL;
    TPM2B_DIGEST *creationHash = NULL;
    TPMT_TK_CREATION *creationTicket = NULL;
    IFAPI_KEY *pkey = &context->createPrimary.pkey_object.misc.key;
    NODE_STR_T *k_sub_path = NULL;
    ESYS_TR auth_session;

    switch (context->primary_state) {
    statecase(context->primary_state, PRIMARY_AUTHORIZE_HIERARCHY);
        if (hierarchy->misc.hierarchy.with_auth == TPM2_YES || policy_digest_size(hierarchy)) {
            r = ifapi_authorize_object(context, hierarchy, &auth_session);
            FAPI_SYNC(r, "Authorize hierarchy.", error_cleanup);
        } else {
            auth_session = context->session1;
        }
        r = Esys_CreatePrimary_Async(context->esys, hierarchy->public.handle,
                                     (auth_session == ESYS_TR_NONE) ?
                                     ESYS_TR_PASSWORD : auth_session,
                                     ESYS_TR_NONE, ESYS_TR_NONE,
                                     &context->cmd.Provision.inSensitive,
                                     &context->cmd.Provision.public_templ.public,
                                     &context->cmd.Provision.outsideInfo,
                                     &context->cmd.Provision.creationPCR);
        goto_if_error_reset_state(r, "CreatePrimary", error_cleanup);

        fallthrough;

    statecase(context->primary_state, PRIMARY_WAIT_FOR_PRIMARY);
        r = Esys_CreatePrimary_Finish(context->esys,
                                      &primaryHandle, &outPublic, &creationData, &creationHash,
                                      &creationTicket);
        if (base_rc(r) == TSS2_BASE_RC_TRY_AGAIN)
            return TSS2_FAPI_RC_TRY_AGAIN;

        /* Retry with authorization callback after trial with null auth */
        if (number_rc(r) == TPM2_RC_BAD_AUTH
            && hierarchy->misc.hierarchy.with_auth == TPM2_NO) {
            char *description;
            r = ifapi_get_description(hierarchy, &description);
            return_if_error(r, "Get description");

            r = ifapi_set_auth(context, hierarchy, description);
            SAFE_FREE(description);
            goto_if_error_reset_state(r, "CreatePrimary", error_cleanup);

            r = Esys_CreatePrimary_Async(context->esys, hierarchy->public.handle,
                                         (context->session1 == ESYS_TR_NONE) ?
                                         ESYS_TR_PASSWORD : context->session1,
                                         ESYS_TR_NONE, ESYS_TR_NONE,
                                         &context->cmd.Provision.inSensitive,
                                         &context->cmd.Provision.public_templ.public,
                                         &context->cmd.Provision.outsideInfo,
                                         &context->cmd.Provision.creationPCR);
            goto_if_error_reset_state(r, "CreatePrimary", error_cleanup);

            if (ktype == TSS2_EK) {
                context->state = PROVISION_AUTH_EK_AUTH_SENT;
            } else {
                context->state = PROVISION_AUTH_SRK_AUTH_SENT;
            }
            hierarchy->misc.hierarchy.with_auth = TPM2_YES;
            return TSS2_FAPI_RC_TRY_AGAIN;

        } else {
            goto_if_error_reset_state(r, "FAPI Provision", error_cleanup);
        }
        /* Set EK or SRK handle in context. */
        if (ktype == TSS2_EK) {
            context->ek_handle = primaryHandle;
        } else if (ktype == TSS2_SRK) {
            context->srk_handle = primaryHandle;
        } else {
            return_error(TSS2_FAPI_RC_BAD_VALUE,
                         "Invalid key type. Only EK or SRK allowed");
        }

        /* Prepare serialization of pkey to key store. */

        SAFE_FREE(pkey->serialization.buffer);
        r = Esys_TR_Serialize(context->esys, primaryHandle, &pkey->serialization.buffer,
                          &pkey->serialization.size);
        goto_if_error(r, "Error serialize esys object", error_cleanup);

        r = ifapi_get_name(&outPublic->publicArea, &pkey->name);
        goto_if_error(r, "Get primary name", error_cleanup);

        pkey->public = *outPublic;
        pkey->policyInstance = NULL;
        pkey->creationData = *creationData;
        pkey->creationHash = *creationHash;
        pkey->creationTicket = *creationTicket;
        pkey->description = NULL;
        pkey->certificate = NULL;

        /* Cleanup unused information */
        SAFE_FREE(outPublic);
        SAFE_FREE(creationData);
        SAFE_FREE(creationHash);
        SAFE_FREE(creationTicket);

        if (pkey->public.publicArea.type == TPM2_ALG_RSA)
            pkey->signing_scheme = context->profiles.default_profile.rsa_signing_scheme;
        else
            pkey->signing_scheme = context->profiles.default_profile.ecc_signing_scheme;
        context->createPrimary.pkey_object.public.handle = primaryHandle;
        SAFE_FREE(pkey->serialization.buffer);
        return TSS2_RC_SUCCESS;

    statecasedefault(context->primary_state);
    }

error_cleanup:
    SAFE_FREE(outPublic);
    SAFE_FREE(creationData);
    SAFE_FREE(creationHash);
    SAFE_FREE(creationTicket);
    ifapi_cleanup_ifapi_object(&context->createPrimary.pkey_object);
    free_string_list(k_sub_path);
    SAFE_FREE(pkey->serialization.buffer);
    ifapi_cleanup_ifapi_object(&context->createPrimary.pkey_object);
    return r;
}

/** Prepare the loading of a primary key from key store.
 *
 * The asynchronous loading or the key from keystore will be prepared and
 * the path will be stored in the FAPI context.
 *
 * @param[in] context The FAPI_CONTEXT.
 * @param[in] path The FAPI path of the primary key.
 *
 * @retval TSS2_RC_SUCCESS on success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if a wrong type was passed.
 * @retval TSS2_FAPI_RC_IO_ERROR if an I/O error was encountered.
 * @retval TSS2_FAPI_RC_PATH_NOT_FOUND if the file does not exist.
 * @retval TSS2_FAPI_RC_MEMORY if memory could not be allocated for path names.
 * @retval TSS2_FAPI_RC_KEY_NOT_FOUND if a key was not found.
 * @retval TSS2_FAPI_RC_NOT_PROVISIONED FAPI was not provisioned.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_BAD_PATH if the path is used in inappropriate context
 *         or contains illegal characters.
 */
TSS2_RC
ifapi_load_primary_async(FAPI_CONTEXT *context, char *path)
{

    TSS2_RC r;

    memset(&context->createPrimary.pkey_object, 0, sizeof(IFAPI_OBJECT));
    context->createPrimary.path = path;
    r = ifapi_keystore_load_async(&context->keystore, &context->io, path);
    return_if_error2(r, "Could not open: %s", path);
    context->primary_state = PRIMARY_READ_KEY;
    return TSS2_RC_SUCCESS;

}

/** State machine to finalize the loading of a primary key from key store.
 *
 * The asynchronous loading or the key from keystore will be finalized.
 * Afterwards the hierarchy object, which will be used for authorization will
 * be loaded and the ESAPI functions for primary generation will be called
 * if the primary is not persistent.
 *
 * @param[in] context The FAPI_CONTEXT.
 * @param[out] handle The object handle of the primary key.
 *
 * @retval TSS2_RC_SUCCESS on success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if a wrong type was passed.
 * @retval TSS2_FAPI_RC_PATH_NOT_FOUND if the hierarchy file does not exist.
 * @retval TSS2_FAPI_RC_IO_ERROR if an I/O error was encountered.
 * @retval TSS2_FAPI_RC_MEMORY if memory could not be allocated for path names.
 * @retval TSS2_ESYS_RC_* possible error codes of ESAPI.
 * @retval TSS2_FAPI_RC_TRY_AGAIN if an I/O operation is not finished yet and
 *         this function needs to be called again.
 * @retval TSS2_FAPI_RC_BAD_SEQUENCE if the context has an asynchronous
 *         operation already pending.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE if an internal error occurred.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_KEY_NOT_FOUND if a key was not found.
 * @retval TSS2_FAPI_RC_AUTHORIZATION_UNKNOWN if a required authorization callback
 *         is not set.
 * @retval TSS2_FAPI_RC_AUTHORIZATION_FAILED if the authorization attempt fails.
 * @retval TSS2_FAPI_RC_POLICY_UNKNOWN if policy search for a certain policy digest
 *         was not successful.
 * @retval TSS2_FAPI_RC_NOT_PROVISIONED FAPI was not provisioned.
 * @retval TSS2_FAPI_RC_BAD_PATH if the path is used in inappropriate context
 *         or contains illegal characters.
 */
TSS2_RC
ifapi_load_primary_finish(FAPI_CONTEXT *context, ESYS_TR *handle)
{
    TSS2_RC r;
    IFAPI_OBJECT *hierarchy = &context->createPrimary.hierarchy;

    TPM2B_PUBLIC *outPublic = NULL;
    TPM2B_CREATION_DATA *creationData = NULL;
    TPM2B_DIGEST *creationHash = NULL;
    TPMT_TK_CREATION *creationTicket = NULL;
    IFAPI_OBJECT *pkey_object = &context->createPrimary.pkey_object;
    IFAPI_KEY *pkey = &context->createPrimary.pkey_object.misc.key;
    TPMS_CAPABILITY_DATA **capabilityData = &context->createPrimary.capabilityData;
    TPMI_YES_NO moreData;
    ESYS_TR auth_session = ESYS_TR_NONE; /* Initialized due to scanbuild */

    LOG_TRACE("call");

    switch (context->primary_state) {
    statecase(context->primary_state, PRIMARY_READ_KEY);
        /* Read the primary key from keystore. */
        r = ifapi_keystore_load_finish(&context->keystore, &context->io,
                                       pkey_object);
        return_try_again(r);
        return_if_error(r, "read_finish failed");

        r = ifapi_initialize_object(context->esys, pkey_object);
        goto_if_error_reset_state(r, "Initialize key object", error_cleanup);

        /* Check whether a persistent key was loaded.
           In this case the handle has already been set. */
        if (pkey_object->public.handle != ESYS_TR_NONE) {
            if (pkey->creationTicket.hierarchy == TPM2_RH_EK) {
                context->ek_persistent = true;
            } else {
                context->srk_persistent = true;
            }
            /* It has to be checked whether the persistent handle exists. */
            context->primary_state = PRIMARY_VERIFY_PERSISTENT;
            return TSS2_FAPI_RC_TRY_AGAIN;
        }
        else {
            if (pkey->creationTicket.hierarchy == TPM2_RH_EK) {
                context->ek_persistent = false;
            } else {
                context->srk_persistent = false;
            }
        }
        fallthrough;

    statecase(context->primary_state, PRIMARY_READ_HIERARCHY);
        /* The hierarchy object used for auth_session will be loaded from key store. */
        if (pkey->creationTicket.hierarchy == TPM2_RH_EK ||
            (pkey->ek_profile && pkey->creationTicket.hierarchy == TPM2_RH_ENDORSEMENT)) {
            r = ifapi_keystore_load_async(&context->keystore, &context->io, "/HE");
            return_if_error2(r, "Could not open hierarchy /HE");
        } else if (pkey->creationTicket.hierarchy == TPM2_RH_NULL) {
            r = ifapi_keystore_load_async(&context->keystore, &context->io, "/HN");
            return_if_error2(r, "Could not open hierarchy /HN");
        } else {
            r = ifapi_keystore_load_async(&context->keystore, &context->io, "/HS");
            return_if_error2(r, "Could not open hierarchy /HS");
        }
        fallthrough;

    statecase(context->primary_state, PRIMARY_READ_HIERARCHY_FINISH);
        r = ifapi_keystore_load_finish(&context->keystore, &context->io, hierarchy);
        return_try_again(r);
        return_if_error(r, "read_finish failed");

        r = ifapi_initialize_object(context->esys, hierarchy);
        goto_if_error_reset_state(r, "Initialize hierarchy object", error_cleanup);

        if (pkey->creationTicket.hierarchy == TPM2_RH_EK) {
            hierarchy->public.handle = ESYS_TR_RH_ENDORSEMENT;
        } else if (pkey->creationTicket.hierarchy == TPM2_RH_ENDORSEMENT &&
                   pkey->ek_profile) {
            hierarchy->public.handle = ESYS_TR_RH_ENDORSEMENT;
        } else if (pkey->creationTicket.hierarchy == TPM2_RH_NULL) {
            hierarchy->public.handle = ESYS_TR_RH_NULL;
        } else {
            hierarchy->public.handle = ESYS_TR_RH_OWNER;
        }
        fallthrough;

    statecase(context->primary_state, PRIMARY_AUTHORIZE_HIERARCHY);
        /* The asynchronous authorization of the hierarchy needed for primary. */
        r = ifapi_authorize_object(context, hierarchy, &auth_session);
        FAPI_SYNC(r, "Authorize hierarchy.", error_cleanup);

        memset(&context->createPrimary.inSensitive, 0, sizeof(TPM2B_SENSITIVE_CREATE));
        memset(&context->createPrimary.outsideInfo, 0, sizeof(TPM2B_DATA));
        memset(&context->createPrimary.creationPCR, 0, sizeof(TPML_PCR_SELECTION));
        fallthrough;

    statecase(context->primary_state, PRIMARY_GET_AUTH_VALUE);
        /* Get the auth value to be stored in inSensitive */
        r = ifapi_set_auth_primary(context, pkey_object,
                                   &context->createPrimary.inSensitive.sensitive);
        return_try_again(r);
        goto_if_error_reset_state(r, "Get auth value for primary", error_cleanup);

        /* Prepare primary creation. */
        TPM2B_PUBLIC public = pkey->public;

        memset(&public.publicArea.unique, 0, sizeof(TPMU_PUBLIC_ID));

        if (hierarchy->public.handle == ESYS_TR_RH_ENDORSEMENT &&
            pkey->ek_profile) {
            /* Values set according to EK credential profile. */
            if (public.publicArea.type == TPM2_ALG_RSA) {
                if (pkey->nonce.size) {
                    memcpy(public.publicArea.unique.rsa.buffer,
                           &pkey->nonce.buffer[0], pkey->nonce.size);
                }
                if ((public.publicArea.objectAttributes & TPMA_OBJECT_USERWITHAUTH))
                    public.publicArea.unique.rsa.size = 0;
                else
                    public.publicArea.unique.rsa.size = 256;
            } else if (public.publicArea.type == TPM2_ALG_ECC) {
                if (pkey->nonce.size) {
                    memcpy(public.publicArea.unique.ecc.x.buffer,
                           &pkey->nonce.buffer[0], pkey->nonce.size);
                }
                if ((public.publicArea.objectAttributes & TPMA_OBJECT_USERWITHAUTH)) {
                    public.publicArea.unique.ecc.x.size = 0;
                    public.publicArea.unique.ecc.y.size = 0;
                } else {
                    public.publicArea.unique.ecc.x.size = 32;
                    public.publicArea.unique.ecc.y.size = 32;
                }
            }
        }

        r = Esys_CreatePrimary_Async(context->esys, hierarchy->public.handle,
                                     auth_session, ESYS_TR_NONE, ESYS_TR_NONE,
                                     &context->createPrimary.inSensitive,
                                     &public,
                                     &context->createPrimary.outsideInfo,
                                     &context->createPrimary.creationPCR);
        return_if_error(r, "CreatePrimary");
        fallthrough;

    statecase(context->primary_state, PRIMARY_HAUTH_SENT);
        if (context->createPrimary.handle) {
            *handle = context->createPrimary.handle;
            context->primary_state = PRIMARY_CREATED;
            return TSS2_FAPI_RC_TRY_AGAIN;
        } else {
            r = Esys_CreatePrimary_Finish(context->esys,
                                          &pkey_object->public.handle, &outPublic,
                                          &creationData, &creationHash,
                                          &creationTicket);
            return_try_again(r);
            goto_if_error_reset_state(r, "FAPI regenerate primary", error_cleanup);
        }
        *handle = pkey_object->public.handle;
        context->primary_state = PRIMARY_INIT;
        break;

    statecase(context->primary_state, PRIMARY_VERIFY_PERSISTENT);
        /* Check the TPM capabilities for the persistent handle. */
        r = Esys_GetCapability_Async(context->esys,
                                     ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE,
                                     TPM2_CAP_HANDLES,
                                     pkey_object->misc.key.persistent_handle, 1);
        goto_if_error(r, "Esys_GetCapability_Async", error_cleanup);
        fallthrough;

    statecase(context->primary_state, PRIMARY_GET_CAP);
        r = Esys_GetCapability_Finish(context->esys, &moreData, capabilityData);
        return_try_again(r);
        goto_if_error_reset_state(r, "GetCapablity_Finish", error_cleanup);

        /* Check whether the persistent handle exists. */
        if ((*capabilityData)->data.handles.count != 0 &&
            (*capabilityData)->data.handles.handle[0] ==
            pkey_object->misc.key.persistent_handle) {
            /* Persistent handle found. */
            SAFE_FREE(*capabilityData);
            *handle = pkey_object->public.handle;
            break;
        }
        goto_error(r, TSS2_FAPI_RC_KEY_NOT_FOUND ,
                   "The persistent handle 0x%x does not exist. "
                   "The TPM state and the keystore state do not match."
,                   error_cleanup, pkey_object->misc.key.persistent_handle);
        fallthrough;

    statecasedefault(context->primary_state);
    }
    SAFE_FREE(outPublic);
    SAFE_FREE(creationData);
    SAFE_FREE(creationHash);
    SAFE_FREE(creationTicket);
    ifapi_cleanup_ifapi_object(&context->createPrimary.hierarchy);
    return TSS2_RC_SUCCESS;

error_cleanup:
    SAFE_FREE(*capabilityData);
    SAFE_FREE(outPublic);
    SAFE_FREE(creationData);
    SAFE_FREE(creationHash);
    SAFE_FREE(creationTicket);
    ifapi_cleanup_ifapi_object(&context->createPrimary.hierarchy);
    ifapi_cleanup_ifapi_object(&context->createPrimary.pkey_object);
    return r;
}

/** Prepare session for FAPI command execution.
 *
 * It will be checked whether the context of FAPI and ESAPI is initialized
 * and whether no other FAPI command session is running.
 * Also some handle variables in the context are initialized.
 *
 * @param[in] context The FAPI_CONTEXT.
 *
 * @retval TSS2_RC_SUCCESS on success.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE if the context is not initialized.
 * @retval TSS2_FAPI_RC_BAD_SEQUENCE If a FAPI command session is active.
 * @retval TSS2_FAPI_RC_NO_TPM if the ESAPI context is not initialized.
 */
TSS2_RC
ifapi_session_init(FAPI_CONTEXT *context)
{
    LOG_TRACE("call");
    return_if_null(context, "No context", TSS2_FAPI_RC_BAD_REFERENCE);

    return_if_null(context->esys, "No context", TSS2_FAPI_RC_NO_TPM);

    if (context->state != _FAPI_STATE_INIT) {
        return_error(TSS2_FAPI_RC_BAD_SEQUENCE, "Invalid State");
    }

    context->session1 = ESYS_TR_NONE;
    context->session2 = ESYS_TR_NONE;
    context->policy.session = ESYS_TR_NONE;
    context->srk_handle = ESYS_TR_NONE;
    return TSS2_RC_SUCCESS;
}

/** Prepare session for FAPI command execution without TPM.
 *
 * It will be checked whether the context of FAPI is initialized
 * and whether no other FAPI command session is running.
 * Also some handle variables in the context are initialized.
 *
 * @param[in] context The FAPI_CONTEXT.
 *
 * @retval TSS2_RC_SUCCESS on success.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE if the context is not initialized.
 * @retval TSS2_FAPI_RC_BAD_SEQUENCE If a FAPI command session is active.
 */
TSS2_RC
ifapi_non_tpm_mode_init(FAPI_CONTEXT *context)
{
    LOG_TRACE("call");
    return_if_null(context, "No context", TSS2_FAPI_RC_BAD_REFERENCE);

    if (context->state != _FAPI_STATE_INIT) {
        return_error(TSS2_FAPI_RC_BAD_SEQUENCE, "Invalid State");
    }

    context->session1 = ESYS_TR_NONE;
    context->session2 = ESYS_TR_NONE;
    context->policy.session = ESYS_TR_NONE;
    context->srk_handle = ESYS_TR_NONE;
    return TSS2_RC_SUCCESS;
}

/** Cleanup FAPI sessions in error cases.
 *
 * The uses sessions and the SRK (if not persistent) will be flushed
 * non asynchronous in error cases.
 *
 * @param[in,out] context The FAPI_CONTEXT.
 */
void
ifapi_session_clean(FAPI_CONTEXT *context)
{
    if (context->policy_session && context->policy_session != ESYS_TR_NONE) {
        Esys_FlushContext(context->esys, context->policy_session);
    }
    if (context->session1 != ESYS_TR_NONE) {
        if (Esys_FlushContext(context->esys, context->session1) != TSS2_RC_SUCCESS) {
            LOG_ERROR("Cleanup session failed.");
        }
        context->session1 = ESYS_TR_NONE;
    }
    if (context->session2 != ESYS_TR_NONE) {
        if (Esys_FlushContext(context->esys, context->session2) != TSS2_RC_SUCCESS) {
            LOG_ERROR("Cleanup session failed.");
            context->session2 = ESYS_TR_NONE;
        }
    }
    if (!context->srk_persistent && context->srk_handle != ESYS_TR_NONE) {
        if (Esys_FlushContext(context->esys, context->srk_handle) != TSS2_RC_SUCCESS) {
            LOG_ERROR("Cleanup Policy Session  failed.");
        }
        context->srk_handle = ESYS_TR_NONE;
    }
    context->srk_persistent = false;
}

/** State machine for asynchronous cleanup of a FAPI session.
 *
 * Used sessions and the SRK will be flushed.
 *
 * @param[in] context The FAPI_CONTEXT storing the used handles.
 *
 * @retval TSS2_RC_SUCCESS on success.
 * @retval TSS2_ESYS_RC_* possible error codes of ESAPI.
 * @retval TSS2_FAPI_RC_TRY_AGAIN if an I/O operation is not finished yet and
 *         this function needs to be called again.
 * @retval TSS2_FAPI_RC_BAD_SEQUENCE if the context has an asynchronous
 *         operation already pending.
 */
TSS2_RC
ifapi_cleanup_session(FAPI_CONTEXT *context)
{
    TSS2_RC r;

    /* Policy sessions were closed after successful execution. */
    context->policy_session = ESYS_TR_NONE;

    switch (context->cleanup_state) {
        statecase(context->cleanup_state, CLEANUP_INIT);
            if (context->session1 != ESYS_TR_NONE) {
                r = Esys_FlushContext_Async(context->esys, context->session1);
                try_again_or_error(r, "Flush session.");
            }
            fallthrough;

        statecase(context->cleanup_state, CLEANUP_SESSION1);
            if (context->session1 != ESYS_TR_NONE) {
                r = Esys_FlushContext_Finish(context->esys);
                try_again_or_error(r, "Flush session.");
            }
            context->session1 = ESYS_TR_NONE;

            if (context->session2 != ESYS_TR_NONE) {
                r = Esys_FlushContext_Async(context->esys, context->session2);
                try_again_or_error(r, "Flush session.");
            }
            fallthrough;

        statecase(context->cleanup_state, CLEANUP_SESSION2);
            if (context->session2 != ESYS_TR_NONE) {
                r = Esys_FlushContext_Finish(context->esys);
                try_again_or_error(r, "Flush session.");
            }
            context->session2 = ESYS_TR_NONE;

            if (!context->srk_persistent && context->srk_handle != ESYS_TR_NONE) {
                r = Esys_FlushContext_Async(context->esys, context->srk_handle);
                try_again_or_error(r, "Flush SRK.");
            }
            fallthrough;

        statecase(context->cleanup_state, CLEANUP_SRK);
            if (!context->srk_persistent && context->srk_handle != ESYS_TR_NONE) {
                r = Esys_FlushContext_Finish(context->esys);
                try_again_or_error(r, "Flush SRK.");

                context->srk_handle = ESYS_TR_NONE;
                context->srk_persistent = false;
            }
            context->cleanup_state = CLEANUP_INIT;
            return TSS2_RC_SUCCESS;

        statecasedefault(context->state);
    }
}

/** Cleanup primary keys in error cases (non asynchronous).
 *
 * @param[in] context The FAPI_CONTEXT storing the used handles.
 *
 * @retval TSS2_RC_SUCCESS on success.
 * @retval TSS2_ESYS_RC_* possible error codes of ESAPI.
 */
void
ifapi_primary_clean(FAPI_CONTEXT *context)
{
    if (!context->srk_persistent && context->srk_handle != ESYS_TR_NONE) {
        if (Esys_FlushContext(context->esys, context->srk_handle) != TSS2_RC_SUCCESS) {
            LOG_ERROR("Cleanup session failed.");
        }
        context->srk_handle = ESYS_TR_NONE;
    }
    if (!context->ek_persistent && context->ek_handle != ESYS_TR_NONE) {
        if (Esys_FlushContext(context->esys, context->ek_handle) != TSS2_RC_SUCCESS) {
            LOG_ERROR("Cleanup EK failed.");
        }
        context->ek_handle = ESYS_TR_NONE;
    }
    context->srk_persistent = false;
}

/** Prepare the session creation of a FAPI command.
 *
 * The initial state of the state machine for session creation will be determined.
 * Depending of the session_flags creation of a primary for the encryption of
 * the session secret can be adjusted.
 * The session passed session attributes will be used for the ESAPI command
 * Esys_TRSess_SetAttributes.
 *
 * @param[in] context The FAPI_CONTEXT storing the used handles.
 * @param[in] session_flags The flags to adjust used session and encryption
 *            key. With IFAPI_SESSION1 and IFAPI_SESSION2 the session creation
 *            for sesion1 and session2 can be activated, IFAPI_SESSION_GENEK
 *            triggers the creation of the primary for session secret encryption.
 * @param[in] attribute_flags1 The attributes used for session1.
 * @param[in] attribute_flags2 The attributes used for session2.
 *
 * @retval TSS2_RC_SUCCESS on success.
 * @retval TSS2_FAPI_RC_PATH_NOT_FOUND if the hierarchy file or the primary key file
 *         does not exist.
 * @retval TSS2_FAPI_RC_MEMORY if memory could not be allocated for path names.
 *         of the primary.
 * @retval TSS2_FAPI_RC_KEY_NOT_FOUND if a key was not found.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_IO_ERROR if an error occurred while accessing the
 *         object store.
 * @retval TSS2_FAPI_RC_NOT_PROVISIONED FAPI was not provisioned.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_BAD_PATH if the path is used in inappropriate context
 *         or contains illegal characters.
 */
TSS2_RC
ifapi_get_sessions_async(FAPI_CONTEXT *context,
                         IFAPI_SESSION_TYPE session_flags,
                         TPMA_SESSION attribute_flags1,
                         TPMA_SESSION attribute_flags2)
{
    TSS2_RC r;

    LOG_TRACE("call");
    context->session_flags = session_flags;
    context->session1_attribute_flags = attribute_flags1;
    context->session2_attribute_flags = attribute_flags2;
    char *file = NULL;

    if (!(session_flags & IFAPI_SESSION_GENEK)) {
        context->srk_handle = ESYS_TR_NONE;
        context->session_state = SESSION_CREATE_SESSION;
        return TSS2_RC_SUCCESS;
    }

    context->primary_state = PRIMARY_INIT;
    r = ifapi_asprintf(&file, "%s%s", context->config.profile_name,
                       IFAPI_SRK_KEY_PATH);
    goto_if_error(r, "Error ifapi_asprintf", error_cleanup);

    r = ifapi_load_primary_async(context, file);
    return_if_error_reset_state(r, "Load EK");
    free(file);

    context->session_state = SESSION_WAIT_FOR_PRIMARY;
    return TSS2_RC_SUCCESS;

error_cleanup:
    SAFE_FREE(file);
    return r;
}

/** State machine for the session creation of a FAPI command.
 *
 * The sessions needed for a FAPI command will be created. If needed also the
 * primary key for session encryption will be created.
 *
 * @param[in] context The FAPI_CONTEXT storing the used handles.
 * @param[in] profile The FAPI profile will be used to adjust session parameters.
 * @param[in] hash_alg The hash algorithm used for the session.
 *
 * @retval TSS2_RC_SUCCESS on success.
 * @retval TSS2_FAPI_RC_IO_ERROR if an I/O error was encountered.
 * @retval TSS2_FAPI_RC_MEMORY if memory could not be allocated for path names.
 * @retval TSS2_ESYS_RC_* possible error codes of ESAPI.
 * @retval TSS2_FAPI_RC_TRY_AGAIN if an I/O operation is not finished yet and
 *         this function needs to be called again.
 * @retval TSS2_FAPI_RC_BAD_SEQUENCE if the context has an asynchronous
 *         operation already pending.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE if an internal error occurred.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_PATH_NOT_FOUND if a FAPI object path was not found
 *         during authorization.
 * @retval TSS2_FAPI_RC_KEY_NOT_FOUND if a key was not found.
 * @retval TSS2_FAPI_RC_AUTHORIZATION_UNKNOWN if a required authorization callback
 *         is not set.
 * @retval TSS2_FAPI_RC_AUTHORIZATION_FAILED if the authorization attempt fails.
 * @retval TSS2_FAPI_RC_POLICY_UNKNOWN if policy search for a certain policy digest
 *         was not successful.
 * @retval TSS2_FAPI_RC_NOT_PROVISIONED FAPI was not provisioned.
 * @retval TSS2_FAPI_RC_BAD_PATH if the path is used in inappropriate context
 *         or contains illegal characters.
 */
TSS2_RC
ifapi_get_sessions_finish(
    FAPI_CONTEXT *context,
    const IFAPI_PROFILE *profile,
    TPMI_ALG_HASH hash_alg)
{
    TSS2_RC r;

    switch (context->session_state) {
    statecase(context->session_state, SESSION_WAIT_FOR_PRIMARY);
        LOG_TRACE("**STATE** SESSION_WAIT_FOR_PRIMARY");
        r = ifapi_load_primary_finish(context, &context->srk_handle);
        return_try_again(r);

        ifapi_cleanup_ifapi_object(&context->createPrimary.pkey_object);
        return_if_error(r, "Load primary.");
        fallthrough;

    statecase(context->session_state, SESSION_CREATE_SESSION);
        LOG_TRACE("**STATE** SESSION_CREATE_SESSION");
        if (!(context->session_flags & IFAPI_SESSION1)) {
            LOG_TRACE("finished");
            return TSS2_RC_SUCCESS;
        }

        /* Initializing the first session for the caller */

        r = ifapi_get_session_async(context->esys, context->srk_handle, profile,
                                    hash_alg);
        return_if_error_reset_state(r, "Create FAPI session async");
        fallthrough;

    statecase(context->session_state, SESSION_WAIT_FOR_SESSION1);
        LOG_TRACE("**STATE** SESSION_WAIT_FOR_SESSION1");
        r = ifapi_get_session_finish(context->esys, &context->session1,
                                     context->session1_attribute_flags);
        return_try_again(r);
        return_if_error_reset_state(r, "Create FAPI session finish");

        if (!(context->session_flags & IFAPI_SESSION2)) {
            LOG_TRACE("finished");
            return TSS2_RC_SUCCESS;
        }

        /* Initializing the second session for the caller */

        r = ifapi_get_session_async(context->esys, context->srk_handle, profile,
                                    profile->nameAlg);
        return_if_error_reset_state(r, "Create FAPI session async");
        fallthrough;

    statecase(context->session_state, SESSION_WAIT_FOR_SESSION2);
        LOG_TRACE("**STATE** SESSION_WAIT_FOR_SESSION2");
        r = ifapi_get_session_finish(context->esys, &context->session2,
                                     context->session2_attribute_flags);
        return_try_again(r);

        return_if_error_reset_state(r, "Create FAPI session finish");
        break;

    statecasedefault(context->session_state);
    }

    return TSS2_RC_SUCCESS;
}

/** Merge profile already stored in FAPI context into a NV object template.
 *
 * The defaults for NV creation which are stored in the FAPI default profile
 * will be merged in the passed templates default values.
 *
 * @param[in] context The FAPI_CONTEXT with the default profile.
 * @param[in] template The template with the default values for the NV object.
 *
 * @retval TSS2_RC_SUCCESS on success.
 */
TSS2_RC
ifapi_merge_profile_into_nv_template(
    FAPI_CONTEXT *context,
    IFAPI_NV_TEMPLATE *template)
{
    const TPMA_NV extend_mask = TPM2_NT_EXTEND << TPMA_NV_TPM2_NT_SHIFT;
    const TPMA_NV counter_mask = TPM2_NT_COUNTER << TPMA_NV_TPM2_NT_SHIFT;
    const TPMA_NV bitfield_mask = TPM2_NT_BITS << TPMA_NV_TPM2_NT_SHIFT;
    const IFAPI_PROFILE *profile = &context->profiles.default_profile;
    size_t hash_size;

    template->public.nameAlg = profile->nameAlg;
    if ((template->public.attributes & extend_mask) == extend_mask) {
        /* The size of the NV ram to be extended must be read from the
           profile */
        hash_size = ifapi_hash_get_digest_size(profile->nameAlg);
        template->public.dataSize = hash_size;
    } else if ((template->public.attributes & counter_mask) == counter_mask ||
               (template->public.attributes & bitfield_mask) == bitfield_mask) {
        /* For bit fields and counters only size 8 is possible */
        template->public.dataSize = 8;
    } else {
        /* For normal NV ram the passed size will be used. */
        template->public.dataSize = context->nv_cmd.numBytes;
    }

    return TSS2_RC_SUCCESS;
}

/** Merge profile already stored in FAPI context into a key template.
 *
 * The defaults for key creation which are stored in the FAPI default profile
 * will be merged in the passed templates default values.
 *
 * @param[in] profile The profile which will be used to adjust the template.
 * @param[in] template The template with the default values for the key object.
 *
 * @retval TSS2_RC_SUCCESS on success.
 */
TSS2_RC
ifapi_merge_profile_into_template(
    const IFAPI_PROFILE *profile,
    IFAPI_KEY_TEMPLATE *template)
{
    /* Merge profile parameters */
    template->public.publicArea.type = profile->type;
    template->public.publicArea.nameAlg = profile->nameAlg;
    if (profile->type == TPM2_ALG_RSA) {
        template->public.publicArea.parameters.rsaDetail.keyBits = profile->keyBits;
        template->public.publicArea.parameters.rsaDetail.exponent = profile->exponent;
    } else if (profile->type == TPM2_ALG_ECC) {
        template->public.publicArea.parameters.eccDetail.curveID = profile->curveID;
        template->public.publicArea.parameters.eccDetail.kdf.scheme = TPM2_ALG_NULL;
    }

    /* Set remaining parameters depending on key type */
    if (template->public.publicArea.objectAttributes & TPMA_OBJECT_RESTRICTED) {
        if (template->public.publicArea.objectAttributes & TPMA_OBJECT_DECRYPT) {
            template->public.publicArea.parameters.asymDetail.symmetric =
            profile->sym_parameters;
        } else {
            template->public.publicArea.parameters.asymDetail.symmetric.algorithm =
            TPM2_ALG_NULL;
        }
        if (profile->type == TPM2_ALG_RSA) {
            if (template->public.publicArea.objectAttributes & TPMA_OBJECT_SIGN_ENCRYPT) {
                template->public.publicArea.parameters.rsaDetail.scheme.scheme =
                profile->rsa_signing_scheme.scheme;
                memcpy(&template->public.publicArea.parameters.rsaDetail.scheme.details,
                       &profile->rsa_signing_scheme.details, sizeof(TPMU_ASYM_SCHEME));
            } else {
                template->public.publicArea.parameters.rsaDetail.scheme.scheme = TPM2_ALG_NULL;
            }
        } else if (profile->type == TPM2_ALG_ECC) {
            if (template->public.publicArea.objectAttributes & TPMA_OBJECT_SIGN_ENCRYPT) {
                template->public.publicArea.parameters.eccDetail.scheme.scheme =
                profile->ecc_signing_scheme.scheme;
                memcpy(&template->public.publicArea.parameters.eccDetail.scheme.details,
                       &profile->ecc_signing_scheme.details, sizeof(TPMU_ASYM_SCHEME));
            } else {
                template->public.publicArea.parameters.eccDetail.scheme.scheme = TPM2_ALG_NULL;
            }
        } else {
            template->public.publicArea.parameters.asymDetail.scheme.scheme = TPM2_ALG_NULL;
        }
    } else {
        /* Non restricted key */
        template->public.publicArea.parameters.asymDetail.symmetric.algorithm =
        TPM2_ALG_NULL;
        template->public.publicArea.parameters.asymDetail.scheme.scheme = TPM2_ALG_NULL;
    }
    return TSS2_RC_SUCCESS;
}

/** Convert absolute path to FAPI path which can be used as parameter for FAPI commands.
 *
 * Function converts the absolute path to a FAPI path.
 *
 * @param[in] keystore The used keystore.
 * @param[out] path FAPI key path.
 */
static void
full_path_to_fapi_path(IFAPI_KEYSTORE *keystore, char *path)
{
    unsigned int start_pos, end_pos, i;
    const unsigned int path_length = strlen(path);
    size_t keystore_length = strlen(keystore->userdir);
    char fapi_path_delim;

    start_pos = 0;

    /* Check key store part of the path */
    if (strncmp(&path[0], keystore->userdir, keystore_length) == 0) {
        start_pos = strlen(keystore->userdir);
    } else {
        keystore_length = strlen(keystore->systemdir);
        if (strncmp(&path[0], keystore->systemdir, keystore_length) == 0)
            start_pos = strlen(keystore->systemdir);
    }
    if (!start_pos)
        return;

    /* Shift FAPI path to the beginning. */
    end_pos = path_length - start_pos;
    memmove(&path[0], &path[start_pos], end_pos);
    size_t ip = 0;
    size_t lp = strlen(path);

    /* Special handling for // */
    while (ip < lp) {
        if (strncmp(&path[ip], "//", 2) == 0) {
            memmove(&path[ip], &path[ip + 1], lp - ip);
            lp -= 1;
        } else {
            ip += 1;
        }
    }

    /* Special handling for policy path were the name of the object file
       is part of the path. */
    if (ifapi_path_type_p(path, IFAPI_POLICY_PATH))
        fapi_path_delim = '.';
    else
        fapi_path_delim = IFAPI_FILE_DELIM_CHAR;

    for (i = end_pos - 1; i > 0; i--) {
        if (path[i] == fapi_path_delim) {
            path[i] = '\0';
            break;
        }
    }
}

/** Asynchronous preparation for loading a key and parent keys.
 *
 * The key loading is prepared. The pathname will be extended if possible and
 * a linked list with the directories will be created.
 *
 * @param[in,out] context The FAPI_CONTEXT.
 * @param[in]     keyPath the key path without the parent directories
 *                of the key store. (e.g. HE/EK, HS/SRK/mykey)
 *
 * @retval TSS2_RC_SUCCESS If the preparation is successful.
 * @retval TSS2_FAPI_RC_MEMORY if memory could not be allocated for path names.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_BAD_PATH if the path is used in inappropriate context
 *         or contains illegal characters.
 * @retval TSS2_FAPI_RC_PATH_NOT_FOUND if a FAPI object path was not found
 *         during authorization.
 */
TSS2_RC
ifapi_load_keys_async(FAPI_CONTEXT *context, char const *keyPath)
{
    TSS2_RC r;
    NODE_STR_T *path_list;
    size_t path_length;
    char *fapi_key_path = NULL;

    LOG_TRACE("Load key: %s", keyPath);
    fapi_key_path = strdup(keyPath);
    check_oom(fapi_key_path);
    full_path_to_fapi_path(&context->keystore, fapi_key_path);
    r = get_explicit_key_path(&context->keystore, fapi_key_path, &path_list);
    SAFE_FREE(fapi_key_path);
    return_if_error(r, "Compute explicit path.");

    context->loadKey.path_list = path_list;
    path_length = ifapi_path_length(path_list);
    r = ifapi_load_key_async(context, path_length);
    goto_if_error(r, "Load key async.", error);

    return TSS2_RC_SUCCESS;

 error:
    free_string_list( context->loadKey.path_list);
    return r;
}

/** Asynchronous preparation for loading of the parent keys.
 *
 * The key loading is prepared. The pathname will be extended if possible and
 * a linked list with the directories will be created.
 *
 * @param[in,out] context The FAPI_CONTEXT.
 * @param[in]     keyPath the key path without the parent directories
 *                of the key store. (e.g. HE/EK, HS/SRK/mykey)
 *
 * @retval TSS2_RC_SUCCESS If the preparation is successful.
 * @retval TSS2_FAPI_RC_MEMORY if memory could not be allocated for path names.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_BAD_PATH if the path is used in inappropriate context
 *         or contains illegal characters.
 * @retval TSS2_FAPI_RC_PATH_NOT_FOUND if a FAPI object path was not found
 *         during authorization.
 */
TSS2_RC
ifapi_load_parent_keys_async(FAPI_CONTEXT *context, char const *keyPath)
{
    TSS2_RC r;
    NODE_STR_T *path_list;
    size_t path_length;
    char *fapi_key_path = NULL;

    LOG_TRACE("Load key: %s", keyPath);
    fapi_key_path = strdup(keyPath);
    check_oom(fapi_key_path);
    full_path_to_fapi_path(&context->keystore, fapi_key_path);
    r = get_explicit_key_path(&context->keystore, fapi_key_path, &path_list);
    SAFE_FREE(fapi_key_path);
    goto_if_error(r, "Compute explicit path.", error);

    context->loadKey.path_list = path_list;
    path_length = ifapi_path_length(path_list);
    r = ifapi_load_key_async(context, path_length - 1);
    return_if_error(r, "Load key async.");

    return TSS2_RC_SUCCESS;

 error:
    free_string_list(context->loadKey.path_list);
    return r;
}

/** Asynchronous finish function for loading a key.
  *
 * @param[in,out] context The FAPI_CONTEXT.
 * @param[in]     flush_parent If false the parent of the key to be loaded
 *                will not be flushed.
 * @param[out]    handle The ESYS handle of the key.
 * @param[out]    key_object The object which will be used for the
 *                authorization of the loaded key.
 * @retval TSS2_FAPI_RC_TRY_AGAIN if an I/O operation is not finished yet and
 *         this function needs to be called again.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE if an internal error occurred.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_BAD_SEQUENCE if the context has an asynchronous
 *         operation already pending.
 * @retval TSS2_FAPI_RC_PATH_NOT_FOUND if a FAPI object path was not found
 *         during authorization.
 * @retval TSS2_FAPI_RC_KEY_NOT_FOUND if a key was not found.
 * @retval TSS2_FAPI_RC_IO_ERROR if an error occurred while accessing the
 *         object store.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
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
ifapi_load_keys_finish(
    FAPI_CONTEXT *context,
    bool flush_parent,
    ESYS_TR *handle,
    IFAPI_OBJECT **key_object)
{
    TSS2_RC r;

    r = ifapi_load_key_finish(context, flush_parent);
    if (r == TSS2_FAPI_RC_TRY_AGAIN)
        return r;

    goto_if_error(r, "Load keys", error);

    *handle = context->loadKey.auth_object.public.handle;
    /* The current authorization object is the last key loaded and
       will be used. */
    *key_object = &context->loadKey.auth_object;
    free_string_list(context->loadKey.path_list);
    return TSS2_RC_SUCCESS;

 error:
    free_string_list(context->loadKey.path_list);
    return r;

}

/** Initialize state machine for loading a key.
 *
 * @param[in,out] context for storing all state information.
 * @param[in] position the position of the key in path list stored in
 *            context->loadKey.path_list.
 *
 * @retval TSS2_RC_SUCCESS on success.
 * @retval TSS2_FAPI_RC_MEMORY if memory could not be allocated for path names.
 */
TSS2_RC
ifapi_load_key_async(FAPI_CONTEXT *context, size_t position)
{
    context->loadKey.state = LOAD_KEY_GET_PATH;
    context->loadKey.position = position;
    context->loadKey.key_list = NULL;
    context->loadKey.parent_handle = ESYS_TR_NONE;

    return TSS2_RC_SUCCESS;
}

/** State machine for loading a key.
 *
 * A stack with all sup keys will be created and decremented during
 * the loading auf all keys.
 * The object of the loaded key will be stored in:
 * context->loadKey.auth_object
 *
 * @param[in,out] context for storing all state information.
 * @param[in]     flush_parent If flush_parent is false parent is
                  only flushed if a new parent is available.
 *
 * @retval TSS2_RC_SUCCESS If the loading of the key was successful.
 * @retval TSS2_ESYS_RC_* possible error codes of ESAPI.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE If an internal error occurs, which is
 *         not covered by other return codes.
 * @retval TSS2_FAPI_RC_BAD_VALUE If wrong values are detected during execution.
 * @retval TSS2_FAPI_RC_IO_ERROR If an error occurs during access to the policy
 *         store.
 * @retval TSS2_FAPI_RC_PATH_NOT_FOUND If an object needed for loading or
 *         authentication was not found.
 * @retval TSS2_FAPI_RC_POLICY_UNKNOWN If policy search for a certain policy digest was
 *         not successful.
 * @retval TPM2_RC_BAD_AUTH If the authentication for an object needed for loading
 *         fails.
 * @retval TSS2_FAPI_RC_AUTHORIZATION_UNKNOWN if a needed authorization callback
 *         is not defined.
 * @retval TSS2_FAPI_RC_TRY_AGAIN if an I/O operation is not finished yet and
 *         this function needs to be called again.
 * @retval TSS2_FAPI_RC_BAD_SEQUENCE if the context has an asynchronous
 *         operation already pending.
 * @retval TSS2_FAPI_RC_KEY_NOT_FOUND if a key was not found.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_AUTHORIZATION_FAILED if the authorization attempt fails.
 * @retval TSS2_FAPI_RC_BAD_PATH if the path is used in inappropriate context
 *         or contains illegal characters.
 * @retval TSS2_FAPI_RC_NOT_PROVISIONED FAPI was not provisioned.
 */
TSS2_RC
ifapi_load_key_finish(FAPI_CONTEXT *context, bool flush_parent)
{
    TSS2_RC r;
    NODE_STR_T *path_list = context->loadKey.path_list;
    size_t *position = &context->loadKey.position;
    IFAPI_OBJECT *key_object = NULL;
    IFAPI_KEY *key = NULL;
    ESYS_TR auth_session;

    switch (context->loadKey.state) {
    statecase(context->loadKey.state, LOAD_KEY_GET_PATH);
        context->loadKey.key_path = NULL;
        /* Compute path name of key to be loaded. */
        r = ifapi_path_string_n(&context->loadKey.key_path, NULL, path_list, NULL,
                                *position);
        LOG_TRACE("Load path %s", context->loadKey.key_path);
        return_if_error(r, "Compute key path.");

        context->loadKey.key_object = ifapi_allocate_object(context);
        goto_if_null2(context->loadKey.key_object, "Allocating key", r,
                      TSS2_FAPI_RC_MEMORY, error_cleanup);

        goto_if_null2(context->loadKey.key_path, "Invalid path", r,
                      TSS2_FAPI_RC_GENERAL_FAILURE,
                      error_cleanup); /**< to avoid scan-build errors. */

        /* Prepare key loading. */
        r = ifapi_keystore_load_async(&context->keystore, &context->io,
                                      context->loadKey.key_path);
        return_if_error2(r, "Could not open: %s", context->loadKey.key_path);
        fallthrough;

    statecase(context->loadKey.state, LOAD_KEY_READ_KEY);
        goto_if_null2(context->loadKey.key_path, "Invalid path", r,
                      TSS2_FAPI_RC_GENERAL_FAILURE,
                      error_cleanup); /**< to avoid scan-build errors. */

        key = &context->loadKey.key_object->misc.key;

        r = ifapi_keystore_load_finish(&context->keystore, &context->io,
                                       context->loadKey.key_object);
        if (r != TSS2_RC_SUCCESS) {
            ifapi_cleanup_ifapi_object(context->loadKey.key_object);
        }
        return_try_again(r);
        return_if_error(r, "read_finish failed");

        if (context->loadKey.key_object->objectType != IFAPI_KEY_OBJ)
            goto_error(r, TSS2_FAPI_RC_BAD_PATH, "%s is no key", error_cleanup,
                       context->loadKey.key_path);

        r = ifapi_initialize_object(context->esys, context->loadKey.key_object);
        goto_if_error_reset_state(r, "Initialize key object", error_cleanup);

        SAFE_FREE(context->loadKey.key_path);
        context->loadKey.handle = context->loadKey.key_object->public.handle;
        if (context->loadKey.handle != ESYS_TR_NONE) {
            /* Persistent key could be desearialized keys can be loaded */
            r = ifapi_copy_ifapi_key_object(&context->loadKey.auth_object,
                context->loadKey.key_object);
            goto_if_error(r, "Could not copy key object", error_cleanup);
            ifapi_cleanup_ifapi_object(context->loadKey.key_object);
            context->loadKey.state = LOAD_KEY_LOAD_KEY;

            return TSS2_FAPI_RC_TRY_AGAIN;
        }

        if (key->private.size == 0) {
            /* Create a deep copy of the primary key */
            r = ifapi_copy_ifapi_key_object(&context->createPrimary.pkey_object,
                                            context->loadKey.key_object);
            goto_if_error(r, "Could not copy primary key", error_cleanup);

            ifapi_cleanup_ifapi_key(key);
            context->primary_state = PRIMARY_READ_HIERARCHY;
            context->loadKey.state = LOAD_KEY_WAIT_FOR_PRIMARY;
            return TSS2_FAPI_RC_TRY_AGAIN;
        }
        IFAPI_OBJECT * copyToPush = malloc(sizeof(IFAPI_OBJECT));
        goto_if_null(copyToPush, "Out of memory", TSS2_FAPI_RC_MEMORY, error_cleanup);
        r = ifapi_copy_ifapi_key_object(copyToPush, context->loadKey.key_object);
        if (r) {
            free(copyToPush);
            LOG_ERROR("Could not create a copy to push");
            goto error_cleanup;
        }
        /* Add object to the list of keys to be loaded. */
        r = push_object_to_list(copyToPush, &context->loadKey.key_list);
        if (r) {
            free(copyToPush);
            LOG_ERROR("Out of memory");
            goto error_cleanup;
        }

        ifapi_cleanup_ifapi_object(context->loadKey.key_object);

        *position -= 1;
        context->loadKey.state = LOAD_KEY_GET_PATH;
        return TSS2_FAPI_RC_TRY_AGAIN;

    statecase(context->loadKey.state, LOAD_KEY_LOAD_KEY);
        if (!(context->loadKey.key_list)) {
            LOG_TRACE("All keys loaded.");
            return TSS2_RC_SUCCESS;
        }

        /* if flush_parent is false parent is only flushed if a new parent
           is available */
        if (!flush_parent && context->loadKey.parent_handle != ESYS_TR_NONE) {
            r = Esys_FlushContext(context->esys, context->loadKey.parent_handle);
            goto_if_error_reset_state(r, "Flush object", error_cleanup);
        }
        fallthrough;

    statecase(context->loadKey.state, LOAD_KEY_AUTHORIZE);
        key_object = context->loadKey.key_list->object;
        key = &key_object->misc.key;
        r = ifapi_authorize_object(context, &context->loadKey.auth_object, &auth_session);
        FAPI_SYNC(r, "Authorize key.", error_cleanup);

        /* Store parent handle in context for usage in ChangeAuth if not persistent */
        context->loadKey.parent_handle = context->loadKey.handle;
        if (context->loadKey.auth_object.misc.key.persistent_handle)
            context->loadKey.parent_handle_persistent = true;
        else
            context->loadKey.parent_handle_persistent = false;

        TPM2B_PRIVATE private;

        private.size = key->private.size;
        memcpy(&private.buffer[0], key->private.buffer, key->private.size);

        r = Esys_Load_Async(context->esys, context->loadKey.handle,
                            auth_session,
                            ESYS_TR_NONE, ESYS_TR_NONE,
                            &private, &key->public);
        goto_if_error(r, "Load async", error_cleanup);
        fallthrough;

    statecase(context->loadKey.state, LOAD_KEY_AUTH);
        r = Esys_Load_Finish(context->esys, &context->loadKey.handle);
        return_try_again(r);
        goto_if_error_reset_state(r, "Load", error_cleanup);

        /* The current parent is flushed if not prohibited by flush parent */
        if (flush_parent && context->loadKey.auth_object.objectType == IFAPI_KEY_OBJ &&
            ! context->loadKey.auth_object.misc.key.persistent_handle) {
            r = Esys_FlushContext(context->esys, context->loadKey.auth_object.public.handle);
            goto_if_error_reset_state(r, "Flush object", error_cleanup);

        }
        LOG_TRACE("New key used as auth object.");
        ifapi_cleanup_ifapi_object(&context->loadKey.auth_object);
        r = ifapi_copy_ifapi_key_object(&context->loadKey.auth_object,
                context->loadKey.key_list->object);
        goto_if_error(r, "Could not copy loaded key", error_cleanup);
        context->loadKey.auth_object.public.handle = context->loadKey.handle;
        IFAPI_OBJECT *top_obj = context->loadKey.key_list->object;
        ifapi_cleanup_ifapi_object(top_obj);
        SAFE_FREE(context->loadKey.key_list->object);
        r = pop_object_from_list(context, &context->loadKey.key_list);
        goto_if_error_reset_state(r, "Pop key failed.", error_cleanup);

        if (context->loadKey.key_list) {
            /* Object can be cleaned if it's not the last */
            ifapi_free_object(context, &top_obj);
        }

        context->loadKey.state = LOAD_KEY_LOAD_KEY;
        return TSS2_FAPI_RC_TRY_AGAIN;

    statecase(context->loadKey.state, LOAD_KEY_WAIT_FOR_PRIMARY);
        r = ifapi_load_primary_finish(context, &context->loadKey.handle);
        return_try_again(r);
        goto_if_error(r, "CreatePrimary", error_cleanup);

        /* Save the primary object for authorization */
        r = ifapi_copy_ifapi_key_object(&context->loadKey.auth_object,
                &context->createPrimary.pkey_object);
        goto_if_error(r, "Could not copy primary key", error_cleanup);

        if (context->loadKey.key_list) {
            context->loadKey.state = LOAD_KEY_LOAD_KEY;
            return TSS2_FAPI_RC_TRY_AGAIN;
        } else {
            LOG_TRACE("success");
            ifapi_cleanup_ifapi_object(context->loadKey.key_object);
            return TSS2_RC_SUCCESS;
        }
        break;

    statecasedefault(context->loadKey.state);
    }

error_cleanup:
    if (context->loadKey.handle && context->loadKey.handle != ESYS_TR_NONE &&
        context->loadKey.key_object->misc.key.persistent_handle) {
        Esys_FlushContext(context->esys, context->loadKey.handle);
    }
    ifapi_free_object_list(context->loadKey.key_list);
    ifapi_cleanup_ifapi_object(context->loadKey.key_object);
    SAFE_FREE(context->loadKey.key_path);
    return r;
}

/** Get the name alg corresponding to a FAPI object.
 *
 * @param[in] context The context with the default profile.
 * @param[in] object The object to be checked.
 * @retval TPMI_ALG_HASH The hash algorithm.
 * @retval 0 If no name alg can be assigned to the object.
 */
static size_t
get_name_alg(FAPI_CONTEXT *context, IFAPI_OBJECT *object)
{
    switch (object->objectType) {
    case IFAPI_KEY_OBJ:
        return object->misc.key.public.publicArea.nameAlg;
    case IFAPI_NV_OBJ:
        return object->misc.nv.public.nvPublic.nameAlg;
    case IFAPI_HIERARCHY_OBJ:
        return context->profiles.default_profile.nameAlg;
    default:
        return 0;
    }
}

/** Check whether policy session has to be flushed.
 *
 * Policy sessions with cleared continue session flag are not flushed in error
 * cases. Therefore the return code will be checked and if a policy session was
 * used the session will be flushed if the command was not executed successfully.
 *
 * @param[in,out] context for storing all state information.
 * @param[in] session the session to be checked whether flush is needed.
 * @param[in] r The return code of the command using the session.
 */
void
ifapi_flush_policy_session(FAPI_CONTEXT *context, ESYS_TR session, TSS2_RC r)
{
    if (session != context->session1) {
        /* A policy session was used instead auf the default session. */
        if (r != TSS2_RC_SUCCESS) {
            Esys_FlushContext(context->esys, session);
        }
    }
}

/** State machine to authorize a key, a NV object of a hierarchy.
 *
 * @param[in,out] context for storing all state information.
 * @param[in] object The FAPI object.
 * @param[out] session The session which can be used for object authorization.
 *
 * @retval TSS2_RC_SUCCESS If the authorization is successful
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 * @retval TSS2_FAPI_RC_BAD_VALUE If wrong values are detected during execution.
 * @retval TSS2_FAPI_RC_IO_ERROR If an error occurs during access to the policy
 *         store.
 * @retval TSS2_FAPI_RC_PATH_NOT_FOUND If a policy for a certain path was not found.
 * @retval TSS2_FAPI_RC_POLICY_UNKNOWN If policy search for a certain policy digest was
 *         not successful.
 * @retval TPM2_RC_BAD_AUTH If the authentication for an object needed for the policy
 *         execution fails.
 * @retval TSS2_FAPI_RC_AUTHORIZATION_UNKNOWN if a needed authorization callback
           is not defined.
 * @retval TSS2_FAPI_RC_TRY_AGAIN if an I/O operation is not finished yet and
 *         this function needs to be called again.
 * @retval TSS2_FAPI_RC_AUTHORIZATION_FAILED if the authorization attempt fails.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE if an internal error occurred.
 * @retval TSS2_ESYS_RC_* possible error codes of ESAPI.
 * @retval TSS2_FAPI_RC_KEY_NOT_FOUND if a key was not found.
 */
TSS2_RC
ifapi_authorize_object(FAPI_CONTEXT *context, IFAPI_OBJECT *object, ESYS_TR *session)
{
    TSS2_RC r;
    TPMI_YES_NO auth_required;

    LOG_DEBUG("Authorize object: %x", object->public.handle);
    switch (object->authorization_state) {
        statecase(object->authorization_state, AUTH_INIT)
            LOG_TRACE("**STATE** AUTH_INIT");

            if (!policy_digest_size(object)) {
                /* No policy used authorization callbacks have to be called if necessary. */
                if (object_with_auth(object)) {
                    /* Check whether hierarchy was already authorized. */
                    if (object->objectType != IFAPI_HIERARCHY_OBJ ||
                        !object->misc.hierarchy.authorized) {
                        char *description = NULL;
                        r = ifapi_get_description(object, &description);
                        return_if_error(r, "Get description");

                        r = ifapi_set_auth(context, object, description);
                        SAFE_FREE(description);
                        return_if_error(r, "Set auth value");
                    }
                }
                /* No policy session needed current fapi session can be used */
                if (context->session1 && context->session1 != ESYS_TR_NONE)
                    *session = context->session1;
                else
                    /* Use password session if session1 had not been created */
                    *session = ESYS_TR_PASSWORD;
                break;
            }
            /* Save current object to be authorized in context. */
            context->current_auth_object = object;
            r = ifapi_policyutil_execute_prepare(context, get_name_alg(context, object),
                                                 object->policy);
            return_if_error(r, "Prepare policy execution.");

            /* Next state will switch from prev context to next context. */
            context->policy.util_current_policy = context->policy.util_current_policy->prev;
            object->authorization_state = AUTH_EXEC_POLICY;
            fallthrough;

        statecase(object->authorization_state, AUTH_EXEC_POLICY)
            *session = ESYS_TR_NONE;
            r = ifapi_policyutil_execute(context, session);
            if (r == TSS2_FAPI_RC_TRY_AGAIN)
                return r;

            return_if_error(r, "Execute policy.");

            r = Esys_TRSess_GetAuthRequired(context->esys, *session,
                                            &auth_required);
            return_if_error(r, "GetAuthRequired");

            /* Check whether PolicyCommand requiring authorization was executed */
            if (auth_required == TPM2_YES) {
                char* description;
                r = ifapi_get_description(object, &description);
                return_if_error(r, "Get description");
                r = ifapi_set_auth(context, object, description);
                SAFE_FREE(description);
                goto_if_error(r, "Set auth value", error);
            }
            /* Clear continue session flag, so policy session will be flushed after authorization */
            r = Esys_TRSess_SetAttributes(context->esys, *session, 0, TPMA_SESSION_CONTINUESESSION);
            goto_if_error(r, "Esys_TRSess_SetAttributes", error);
            break;

        general_failure(object->authorization_state)
    }

    object->authorization_state = AUTH_INIT;
    return TSS2_RC_SUCCESS;

error:
    /* No policy call was executed session can be flushed */
    Esys_FlushContext(context->esys, *session);
    return r;
}

/** State machine to write data to the NV ram of the TPM.
 *
 * The NV object will be read from object store and the data will be
 * written by one, or more than one if necessary, ESAPI calls to the NV ram of
 * the TPM.
 * The sub context nv_cmd will be prepared:
 * - data The buffer for the data which has to be written
 * - offset The current offset for writing
 * - numBytes The number of bytes which have to be written.
 *
 * @param[in,out] context for storing all state information.
 * @param[in] nvPath The fapi path of the NV object.
 * @param[in] param_offset The offset in the NV memory (will be stored in context).
 * @param[in] data The pointer to the data to be written.
 * @param[in] size The number of bytes to be written.
 *
 * @retval TSS2_RC_SUCCESS If data can be written.
 * @retval TSS2_ESYS_RC_* possible error codes of ESAPI.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 * @retval TSS2_FAPI_RC_BAD_VALUE If wrong values are detected during execution.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE If an internal error occurs, which is
 +         not covered by other return codes.
 * @retval TSS2_FAPI_RC_IO_ERROR If an error occurs during access to the object
 *         store.
 * @retval TSS2_FAPI_RC_PATH_NOT_FOUND The nv object or an object needed for
 *         authentication was not found.
 * @retval TSS2_FAPI_RC_POLICY_UNKNOWN If policy search for a certain policy digest was
 *          not successful.
 * @retval TPM2_RC_BAD_AUTH If the authentication for an object needed for the
 *         command execution fails.
 * @retval TSS2_FAPI_RC_AUTHORIZATION_UNKNOWN if a needed authorization callback
 *         is not defined.
 * @retval TSS2_FAPI_RC_BAD_PATH if a path is used in inappropriate context
 *         or contains illegal characters.
 * @retval TSS2_FAPI_RC_TRY_AGAIN if an I/O operation is not finished yet and
 *         this function needs to be called again.
 * @retval TSS2_FAPI_RC_BAD_SEQUENCE if the context has an asynchronous
 *         operation already pending.
 * @retval TSS2_FAPI_RC_KEY_NOT_FOUND if a key was not found.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_AUTHORIZATION_FAILED if the authorization attempt fails.
 * @retval TSS2_FAPI_RC_NOT_PROVISIONED FAPI was not provisioned.
 */
TSS2_RC
ifapi_nv_write(
    FAPI_CONTEXT *context,
    char         *nvPath,
    size_t         param_offset,
    uint8_t const *data,
    size_t         size)
{
    TSS2_RC r = TSS2_RC_SUCCESS;
    ESYS_TR auth_index;
    ESYS_TR nv_index = context->nv_cmd.esys_handle;
    IFAPI_OBJECT *object = &context->nv_cmd.nv_object;
    IFAPI_OBJECT *auth_object = &context->nv_cmd.auth_object;
    TPM2B_MAX_NV_BUFFER *aux_data = (TPM2B_MAX_NV_BUFFER *)&context->aux_data;
    char *nv_file_name = NULL;
    ESYS_TR auth_session;

    switch (context->nv_cmd.nv_write_state) {
    statecase(context->nv_cmd.nv_write_state, NV2_WRITE_INIT);
        memset(&context->nv_cmd.nv_object, 0, sizeof(IFAPI_OBJECT));
        context->nv_cmd.nvPath = nvPath;
        context->nv_cmd.offset = param_offset;
        context->nv_cmd.numBytes = size;
        context->nv_cmd.data = data;
        if (context->nv_cmd.numBytes > context->nv_buffer_max)
            aux_data->size = context->nv_buffer_max;
        else
            aux_data->size = context->nv_cmd.numBytes;
        context->nv_cmd.data_idx = 0;

        /* Use calloc to ensure zero padding for write buffer. */
        context->nv_cmd.write_data = calloc(size, 1);
        goto_if_null2(context->nv_cmd.write_data, "Out of memory.", r,
                      TSS2_FAPI_RC_MEMORY,
                      error_cleanup);
        memcpy(context->nv_cmd.write_data, data, size);
        memcpy(&aux_data->buffer[0], &context->nv_cmd.data[0], aux_data->size);

        /* Prepare reading of the key from keystore. */
        r = ifapi_keystore_load_async(&context->keystore, &context->io,
                                      context->nv_cmd.nvPath);
        return_if_error2(r, "Could not open: %s", context->nv_cmd.nvPath);
        fallthrough;

    statecase(context->nv_cmd.nv_write_state, NV2_WRITE_READ);
        r = ifapi_keystore_load_finish(&context->keystore, &context->io, object);
        return_try_again(r);
        return_if_error(r, "read_finish failed");

        if (object->objectType != IFAPI_NV_OBJ)
            goto_error(r, TSS2_FAPI_RC_BAD_PATH, "%s is no NV object.", error_cleanup,
                       context->nv_cmd.nvPath);

        r = ifapi_initialize_object(context->esys, object);
        goto_if_error_reset_state(r, "Initialize NV object", error_cleanup);

        /* Store object info in context */
        nv_index = context->nv_cmd.nv_object.public.handle;
        context->nv_cmd.esys_handle = nv_index;
        context->nv_cmd.nv_obj = object->misc.nv;

        /* Determine the object which will be uses for authorization. */
        if (object->misc.nv.public.nvPublic.attributes & TPMA_NV_PPWRITE) {
            ifapi_init_hierarchy_object(auth_object, ESYS_TR_RH_PLATFORM);
            auth_index = ESYS_TR_RH_PLATFORM;
        } else {
            if (object->misc.nv.public.nvPublic.attributes & TPMA_NV_OWNERWRITE) {
                ifapi_init_hierarchy_object(auth_object, ESYS_TR_RH_OWNER);
                auth_index = ESYS_TR_RH_OWNER;
            } else {
                auth_index = nv_index;
            }
            *auth_object = *object;
        }
        context->nv_cmd.auth_index = auth_index;

        /* Get A session for authorizing the NV write operation. */
        r = ifapi_get_sessions_async(context, IFAPI_SESSION_GENEK | IFAPI_SESSION1,
                                         TPMA_SESSION_DECRYPT, 0);
        goto_if_error(r, "Create sessions", error_cleanup);

        fallthrough;

    statecase(context->nv_cmd.nv_write_state, NV2_WRITE_WAIT_FOR_SESSSION);
        r = ifapi_get_sessions_finish(context, &context->profiles.default_profile,
                                      object->misc.nv.public.nvPublic.nameAlg);
        return_try_again(r);
        goto_if_error_reset_state(r, " FAPI create session", error_cleanup);

        fallthrough;

    statecase(context->nv_cmd.nv_write_state, NV2_WRITE_AUTHORIZE);
        r = ifapi_authorize_object(context, auth_object, &auth_session);
        FAPI_SYNC(r, "Authorize NV object.", error_cleanup);

        /* Prepare the writing to NV ram. */
        r = Esys_NV_Write_Async(context->esys,
                                context->nv_cmd.auth_index,
                                nv_index,
                                auth_session,
                                context->session2,
                                ESYS_TR_NONE,
                                aux_data,
                                context->nv_cmd.data_idx);
        goto_if_error_reset_state(r, " Fapi_NvWrite_Async", error_cleanup);

        if (!(object->misc.nv.public.nvPublic.attributes & TPMA_NV_NO_DA))
            context->nv_cmd.nv_write_state = NV2_WRITE_AUTH_SENT;
        else
            context->nv_cmd.nv_write_state = NV2_WRITE_NULL_AUTH_SENT;

        context->nv_cmd.bytesRequested = aux_data->size;

        fallthrough;

    case NV2_WRITE_AUTH_SENT:
    case NV2_WRITE_NULL_AUTH_SENT:
        r = Esys_NV_Write_Finish(context->esys);
        return_try_again(r);

        if (number_rc(r) == TPM2_RC_BAD_AUTH) {
            if (context->nv_cmd.nv_write_state == NV2_WRITE_NULL_AUTH_SENT) {
                IFAPI_OBJECT *auth_object = &context->nv_cmd.auth_object;
                char *description;
                r = ifapi_get_description(auth_object, &description);
                return_if_error(r, "Get description");
                r = ifapi_set_auth(context, auth_object, description);
                SAFE_FREE(description);
                goto_if_error_reset_state(r, " Fapi_NvWrite_Finish", error_cleanup);

                /* Prepare the writing to NV ram. */
                r = Esys_NV_Write_Async(context->esys,
                                        context->nv_cmd.auth_index,
                                        nv_index,
                                        (!context->policy.session
                                         || context->policy.session == ESYS_TR_NONE) ? context->session1 :
                                        context->policy.session,
                                        context->session2,
                                        ESYS_TR_NONE,
                                        aux_data,
                                        context->nv_cmd.data_idx);
                goto_if_error_reset_state(r, "FAPI NV_Write_Async", error_cleanup);

                context->nv_cmd.nv_write_state = NV2_WRITE_AUTH_SENT;
                return TSS2_FAPI_RC_TRY_AGAIN;
            }
        }
        goto_if_error_reset_state(r, "FAPI NV_Write_Finish", error_cleanup);

        context->nv_cmd.numBytes -= context->nv_cmd.bytesRequested;

        if (context->nv_cmd.numBytes > 0) {
            /* Increment data idx with number of transmitted bytes. */
            context->nv_cmd.data_idx += aux_data->size;
            if (context->nv_cmd.numBytes > context->nv_buffer_max)
                aux_data->size = context->nv_buffer_max;
            else
                aux_data->size = context->nv_cmd.numBytes;
            memcpy(&aux_data->buffer[0],
                   &context->nv_cmd.write_data[context->nv_cmd.data_idx],
                   aux_data->size);

            statecase(context->nv_cmd.nv_write_state, NV2_WRITE_AUTHORIZE2);
                r = ifapi_authorize_object(context, auth_object, &auth_session);
                FAPI_SYNC(r, "Authorize NV object.", error_cleanup);

            /* Prepare the writing to NV ram */
            r = Esys_NV_Write_Async(context->esys,
                                    context->nv_cmd.auth_index,
                                    nv_index,
                                    auth_session,
                                    context->session2,
                                    ESYS_TR_NONE,
                                    aux_data,
                                    context->nv_cmd.data_idx);
            goto_if_error_reset_state(r, "FAPI NV_Write", error_cleanup);

            context->nv_cmd.bytesRequested = aux_data->size;
            context->nv_cmd.nv_write_state = NV2_WRITE_AUTH_SENT;
            return TSS2_FAPI_RC_TRY_AGAIN;

        }
        fallthrough;

    statecase(context->nv_cmd.nv_write_state, NV2_WRITE_WRITE_PREPARE);
        /* Set written bit in keystore */
        context->nv_cmd.nv_object.misc.nv.public.nvPublic.attributes |= TPMA_NV_WRITTEN;
        /* Perform esys serialization if necessary */
        r = ifapi_esys_serialize_object(context->esys, &context->nv_cmd.nv_object);
        goto_if_error(r, "Prepare serialization", error_cleanup);

        /* Start writing the NV object to the key store */
        r = ifapi_keystore_store_async(&context->keystore, &context->io,
                                       context->nv_cmd.nvPath,
                                       &context->nv_cmd.nv_object);
        goto_if_error_reset_state(r, "Could not open: %s", error_cleanup,
                                  context->nv_cmd.nvPath);
        context->nv_cmd.nv_write_state = NV2_WRITE_WRITE;
        fallthrough;

    statecase(context->nv_cmd.nv_write_state, NV2_WRITE_WRITE);
        /* Finish writing the NV object to the key store */
        r = ifapi_keystore_store_finish(&context->io);
        return_try_again(r);
        return_if_error_reset_state(r, "write_finish failed");

        LOG_DEBUG("success");
        r = TSS2_RC_SUCCESS;

        context->nv_cmd.nv_write_state = NV2_WRITE_INIT;
        break;

    statecasedefault(context->nv_cmd.nv_write_state);
    }

error_cleanup:
    SAFE_FREE(nv_file_name);
    SAFE_FREE(context->nv_cmd.write_data);
    return r;
}

/** State machine to read data from the NV ram of the TPM.
 *
 * The state machine can bes used to read NV data for a given ESAPI
 * object or for a TPM NV index. If TPM NV index is used a ESAPI object
 * will be created if the NV index exists. If not the size 0 will be
 * returned.
 * If a TPM handle is used the initial stat NV_READ_CHECK_HANDLE has
 * to be set: context->nv_cmd.nv_read_state.
 * Context nv_cmd has to be prepared before the call of this function:
 * With an TPM handle:
 * - tpm_handle The ESAPI handle of the authorization object.
 * With an ESYS handle:
 * - auth_index The ESAPI handle of the authorization object.
 * - numBytes The number of bytes which should be read.
 * - esys_handle The ESAPI handle of the NV object.
 *
 * @param[in,out] context for storing all state information.
 * @param[out] data the data fetched from TPM.
 * @param[in,out] size The number of bytes requested and fetched.
 *                will be 0 if a TPM handle is used but the NV index
 *                does not exist.
 *
 * @retval TSS2_RC_SUCCESS If the data was read successfully.
 * @retval TSS2_ESYS_RC_* possible error codes of ESAPI.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 * @retval TSS2_FAPI_RC_BAD_VALUE If wrong values are detected during execution.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE If an internal error occurs, which is
 +         not covered by other return codes.
 * @retval TSS2_FAPI_RC_IO_ERROR If an error occurs during access to the object
 *         store.
 * @retval TSS2_FAPI_RC_PATH_NOT_FOUND If a policy for a certain path was not found.
 * @retval TSS2_FAPI_RC_POLICY_UNKNOWN If policy search for a certain policy digest was
 *         not successful.
 * @retval TPM2_RC_BAD_AUTH If the authentication for an object needed for the
 *         execution fails.
 * @retval TSS2_FAPI_RC_AUTHORIZATION_UNKNOWN if a needed authorization callback
 *         is not defined.
 * @retval TSS2_FAPI_RC_TRY_AGAIN if an I/O operation is not finished yet and
 *         this function needs to be called again.
 * @retval TSS2_FAPI_RC_BAD_SEQUENCE if the context has an asynchronous
 *         operation already pending.
 * @retval TSS2_FAPI_RC_AUTHORIZATION_FAILED if the authorization attempt fails.
 * @retval TSS2_FAPI_RC_KEY_NOT_FOUND if a key was not found.
 */
TSS2_RC
ifapi_nv_read(
    FAPI_CONTEXT *context,
    uint8_t     **data,
    size_t       *size)
{
    TSS2_RC r;
    UINT16 aux_size;
    TPM2B_MAX_NV_BUFFER *aux_data;
    UINT16 bytesRequested = context->nv_cmd.bytesRequested;
    size_t *numBytes = &context->nv_cmd.numBytes;
    ESYS_TR nv_index = context->nv_cmd.esys_handle;
    IFAPI_OBJECT *auth_object = &context->nv_cmd.auth_object;
    ESYS_TR session;
    TPMS_CAPABILITY_DATA *capabilityData = NULL;
    TPM2B_NV_PUBLIC *nvPublic = NULL;
    TPMI_YES_NO moreData;

    switch (context->nv_cmd.nv_read_state) {
    statecase(context->nv_cmd.nv_read_state, NV_READ_INIT);
        LOG_TRACE("NV_READ_INIT");
        context->nv_cmd.rdata = NULL;
        fallthrough;

    statecase(context->nv_cmd.nv_read_state, NV_READ_AUTHORIZE);
        LOG_TRACE("NV_READ_AUTHORIZE");
        r = ifapi_authorize_object(context, auth_object, &session);
        FAPI_SYNC(r, "Authorize NV object.", error_cleanup);

        if (*numBytes > context->nv_buffer_max)
            aux_size = context->nv_buffer_max;
        else
            aux_size = *numBytes;

        /* Prepare the reading from NV ram. */
        r = Esys_NV_Read_Async(context->esys,
                               context->nv_cmd.auth_index,
                               nv_index,
                               session,
                               ESYS_TR_NONE,
                               ESYS_TR_NONE,
                               aux_size,
                               0);
        goto_if_error_reset_state(r, " Fapi_NvRead_Async", error_cleanup);

        context->nv_cmd.nv_read_state = NV_READ_AUTH_SENT;
        context->nv_cmd.bytesRequested = aux_size;

        return TSS2_FAPI_RC_TRY_AGAIN;

    statecase(context->nv_cmd.nv_read_state, NV_READ_AUTH_SENT);
        LOG_TRACE("NV_READ_NULL_AUTH_SENT");
        if (context->nv_cmd.rdata == NULL) {
            /* Allocate the data buffer if not already initialized. */
            LOG_TRACE("Allocate %zu bytes", *numBytes);
            context->nv_cmd.rdata = malloc(*numBytes);
        }
        *data = context->nv_cmd.rdata;
        goto_if_null(*data, "Malloc failed", TSS2_FAPI_RC_MEMORY, error_cleanup);

        r = Esys_NV_Read_Finish(context->esys, &aux_data);

        if (base_rc(r) == TSS2_BASE_RC_TRY_AGAIN)
            return TSS2_FAPI_RC_TRY_AGAIN;

        if (context->nv_cmd.auth_index == ESYS_TR_RH_OWNER  &&
            number_rc(r) == TPM2_RC_BAD_AUTH &&
            auth_object->misc.hierarchy.with_auth == TPM2_NO) {
            /* NULL auth failed, password was used for owner hierarchy, try again. */
            auth_object->misc.hierarchy.with_auth = TPM2_YES;
            context->nv_cmd.nv_read_state =  NV_READ_AUTHORIZE;

            return TSS2_FAPI_RC_TRY_AGAIN;
        }

        goto_if_error_reset_state(r, "FAPI NV_Read_Finish", error_cleanup);

        if (aux_data->size < bytesRequested)
            *numBytes = 0;
        else
            *numBytes -= aux_data->size;
        memcpy(*data + context->nv_cmd.data_idx, &aux_data->buffer[0],
               aux_data->size);
        context->nv_cmd.data_idx += aux_data->size;
        free(aux_data);
        if (*numBytes > 0) {
            statecase(context->nv_cmd.nv_read_state, NV_READ_AUTHORIZE2);
                r = ifapi_authorize_object(context, auth_object, &session);
                FAPI_SYNC(r, "Authorize NV object.", error_cleanup);

            /* The reading of the NV data is not completed. The next
            reading will be prepared. */
            if (*numBytes > context->nv_buffer_max)
                aux_size = context->nv_buffer_max;
            else
                aux_size = *numBytes;

            r = Esys_NV_Read_Async(context->esys,
                                   context->nv_cmd.auth_index,
                                   nv_index,
                                   session,
                                   ESYS_TR_NONE,
                                   ESYS_TR_NONE,
                                   aux_size,
                                   context->nv_cmd.data_idx);
            goto_if_error_reset_state(r, "FAPI NV_Read", error_cleanup);
            context->nv_cmd.bytesRequested = aux_size;
            context->nv_cmd.nv_read_state = NV_READ_AUTH_SENT;
            return TSS2_FAPI_RC_TRY_AGAIN;
        } else {
            *size = context->nv_cmd.data_idx;
            context->nv_cmd.nv_read_state = NV_READ_INIT;
            LOG_DEBUG("success");
            r = TSS2_RC_SUCCESS;
            break;
        }
    statecase(context->nv_cmd.nv_read_state, NV_READ_CHECK_HANDLE);
        context->nv_cmd.data_idx = 0;
        context->nv_cmd.auth_index = ESYS_TR_RH_OWNER;
        context->nv_cmd.offset = 0;
        r = Esys_GetCapability_Async(context->esys,
                                     ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE,
                                     TPM2_CAP_HANDLES,
                                     context->nv_cmd.tpm_handle, 1);
        goto_if_error(r, "Esys_GetCapability_Async", error_cleanup);

        fallthrough;

    statecase(context->nv_cmd.nv_read_state, NV_READ_GET_CAPABILITY);
        r = Esys_GetCapability_Finish(context->esys, &moreData, &capabilityData);
        return_try_again(r);
        goto_if_error_reset_state(r, "GetCapablity_Finish", error_cleanup);

        if (capabilityData->data.handles.count == 0 ||
            capabilityData->data.handles.handle[0] != context->nv_cmd.tpm_handle) {
            context->nv_cmd.nv_read_state = NV_READ_INIT;
            *size = 0;
            break;
        }
        SAFE_FREE(capabilityData);
        r = Esys_TR_FromTPMPublic_Async(context->esys, context->nv_cmd.tpm_handle,
                                        ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE);
        goto_if_error(r, "Esys_TR_FromTPMPublic_Async", error_cleanup);

        fallthrough;

    statecase(context->nv_cmd.nv_read_state, NV_READ_GET_ESYS_HANDLE);
        r = Esys_TR_FromTPMPublic_Finish(context->esys, &context->nv_cmd.esys_handle);
        return_try_again(r);

        goto_if_error(r, "Esys_TR_FromTPMPublic_Finish", error_cleanup);

        r = Esys_NV_ReadPublic_Async(context->esys, context->nv_cmd.esys_handle,
                                     ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE);
        goto_if_error(r, "Esys_NV_ReadPublic_Async", error_cleanup);

        fallthrough;

    statecase(context->nv_cmd.nv_read_state, NV_READ_GET_NV_PUBLIC);
        r = Esys_NV_ReadPublic_Finish(context->esys, &nvPublic, NULL);
        return_try_again(r);
        goto_if_error(r, "Error: nv read public", error_cleanup);

        context->nv_cmd.numBytes = nvPublic->nvPublic.dataSize;
        SAFE_FREE(nvPublic);
        context->nv_cmd.nv_read_state = NV_READ_INIT;
        return TSS2_FAPI_RC_TRY_AGAIN;

    statecasedefault(context->nv_cmd.nv_read_state);
    }

error_cleanup:
    SAFE_FREE(capabilityData);
    return r;
}

#define min(X,Y) (X>Y)?Y:X

/** State machine to retrieve random data from TPM.
 *
 * If the buffer size exceeds the maximum size, several ESAPI calls are made.
 *
 * @param[in,out] context for storing all state information.
 * @param[in] numBytes Number of random bytes to be computed.
 * @param[out] data The random data.
 *
 * @retval TSS2_RC_SUCCESS If random data can be computed.
 * @retval TSS2_ESYS_RC_* possible error codes of ESAPI.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_TRY_AGAIN if an I/O operation is not finished yet and
 *         this function needs to be called again.
 * @retval TSS2_FAPI_RC_BAD_SEQUENCE if the context has an asynchronous
 *         operation already pending.
 */
TSS2_RC
ifapi_get_random(FAPI_CONTEXT *context, size_t numBytes, uint8_t **data)
{
    TSS2_RC r;
    TPM2B_DIGEST *aux_data = NULL;

    switch (context->get_random_state) {
    statecase(context->get_random_state, GET_RANDOM_INIT);
        context->get_random.numBytes = numBytes;
        context->get_random.data = calloc(context->get_random.numBytes, 1);
        context->get_random.idx = 0;
        return_if_null(context->get_random.data, "FAPI out of memory.",
                       TSS2_FAPI_RC_MEMORY);

        /* Prepare the creation of random data. */
        r = Esys_GetRandom_Async(context->esys,
                                 context->session1,
                                 ESYS_TR_NONE, ESYS_TR_NONE,
                                 min(context->get_random.numBytes, sizeof(TPMU_HA)));
        goto_if_error_reset_state(r, "FAPI GetRandom", error_cleanup);
        fallthrough;

    statecase(context->get_random_state, GET_RANDOM_SENT);
        r = Esys_GetRandom_Finish(context->esys, &aux_data);
        return_try_again(r);
        goto_if_error_reset_state(r, "FAPI GetRandom_Finish", error_cleanup);

        if (aux_data -> size > context->get_random.numBytes) {
            goto_error(r, TSS2_FAPI_RC_BAD_VALUE, "TPM returned too many bytes",
                       error_cleanup);
        }

        /* Save created random data. */
        memcpy(context->get_random.data + context->get_random.idx, &aux_data->buffer[0],
               aux_data->size);
        context->get_random.numBytes -= aux_data->size;
        context->get_random.idx += aux_data->size;
        Esys_Free(aux_data);
        aux_data = NULL;
        if (context->get_random.numBytes > 0) {

            /* Continue creaion of random data if needed. */
            r = Esys_GetRandom_Async(context->esys, context->session1, ESYS_TR_NONE,
                                     ESYS_TR_NONE, min(context->get_random.numBytes, sizeof(TPMU_HA)));
            goto_if_error_reset_state(r, "FAPI GetRandom", error_cleanup);

            return TSS2_FAPI_RC_TRY_AGAIN;
        }
        break;

    statecasedefault(context->get_random_state);
    }

    *data = context->get_random.data;

    LOG_DEBUG("success");
    context->get_random_state = GET_RANDOM_INIT;
    return TSS2_RC_SUCCESS;

error_cleanup:
    if (aux_data)
        Esys_Free(aux_data);
    context->get_random_state = GET_RANDOM_INIT;
    if (context->get_random.data != NULL)
        SAFE_FREE(context->get_random.data);
    return r;
}

/** Load a key and initialize profile and session for ESAPI execution.
 *
 * This state machine prepares the session for key loading. Some
 * session related parameters will be taken from profile.
 *
 * @param[in,out] context The FAPI_CONTEXT.
 * @param[in]     keyPath the key path without the parent directories
 *                of the key store. (e.g. HE/EK, HS/SRK/mykey)
 * @param[out]    key_object The callee allocated internal representation
 *                of a key object.
 *
 * @retval TSS2_RC_SUCCESS If the key was loaded successfully.
 * @retval TSS2_ESYS_RC_* possible error codes of ESAPI.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE If an internal error occurs, which is
 *         not covered by other return codes.
 * @retval TSS2_FAPI_RC_BAD_VALUE If wrong values are detected during execution.
 * @retval TSS2_FAPI_RC_IO_ERROR If an error occurs during access to the object
 *         store.
 * @retval TSS2_FAPI_RC_PATH_NOT_FOUND If a policy or key was not found.
 * @retval TSS2_FAPI_RC_POLICY_UNKNOWN If policy search for a certain policy digest was
 *         not successful.
 * @retval TPM2_RC_BAD_AUTH If the authentication for an object needed for policy
 *         execution fails.
 * @retval TSS2_FAPI_RC_AUTHORIZATION_UNKNOWN if a needed authorization callback
           is not defined.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_TRY_AGAIN if an I/O operation is not finished yet and
 *         this function needs to be called again.
 * @retval TSS2_FAPI_RC_BAD_SEQUENCE if the context has an asynchronous
 *         operation already pending.
 * @retval TSS2_FAPI_RC_KEY_NOT_FOUND if a key was not found.
 * @retval TSS2_FAPI_RC_AUTHORIZATION_FAILED if the authorization attempt fails.
 * @retval TSS2_FAPI_RC_NOT_PROVISIONED FAPI was not provisioned.
 * @retval TSS2_FAPI_RC_BAD_PATH if the path is used in inappropriate context
 *         or contains illegal characters.
 */
TSS2_RC
ifapi_load_key(
    FAPI_CONTEXT  *context,
    char    const *keyPath,
    IFAPI_OBJECT **key_object)
{
    TSS2_RC r;
    const IFAPI_PROFILE *profile;

    return_if_null(keyPath, "Bad reference for key path.",
                   TSS2_FAPI_RC_BAD_REFERENCE);

    switch (context->loadKey.prepare_state) {
    statecase(context->loadKey.prepare_state, PREPARE_LOAD_KEY_INIT);
        context->loadKey.path = keyPath;

        /* Prepare the session creation. */
        r = ifapi_get_sessions_async(context,
                                     IFAPI_SESSION_GENEK | IFAPI_SESSION1,
                                     TPMA_SESSION_DECRYPT, 0);
        goto_if_error_reset_state(r, "Create sessions", error_cleanup);
        fallthrough;

    statecase(context->loadKey.prepare_state, PREPARE_LOAD_KEY_WAIT_FOR_SESSION);
        r = ifapi_profiles_get(&context->profiles, context->loadKey.path, &profile);
        goto_if_error_reset_state(r, "Reading profile data", error_cleanup);

        r = ifapi_get_sessions_finish(context, profile, profile->nameAlg);
        return_try_again(r);
        goto_if_error_reset_state(r, " FAPI create session", error_cleanup);

        /* Prepare the key loading. */
        r = ifapi_load_keys_async(context, context->loadKey.path);
        goto_if_error(r, "Load keys.", error_cleanup);
        fallthrough;

    statecase(context->loadKey.prepare_state, PREPARE_LOAD_KEY_WAIT_FOR_KEY);
        r = ifapi_load_keys_finish(context, IFAPI_FLUSH_PARENT,
                                   &context->loadKey.handle,
                                   key_object);
        return_try_again(r);
        goto_if_error_reset_state(r, " Load key.", error_cleanup);

        context->loadKey.prepare_state = PREPARE_LOAD_KEY_INIT;
        break;

    statecase(context->loadKey.prepare_state, PREPARE_LOAD_KEY_INIT_KEY);
        context->loadKey.path = keyPath;
        r = ifapi_load_keys_async(context, context->loadKey.path);
        goto_if_error(r, "Load keys.", error_cleanup);

        context->loadKey.prepare_state =  PREPARE_LOAD_KEY_WAIT_FOR_KEY;

        return TSS2_FAPI_RC_TRY_AGAIN;

    statecasedefault(context->loadKey.prepare_state);
    }

error_cleanup:
    return r;
}

/** State machine for signing operation.
 *
 * The key used for signing will be authorized and the signing of the passed data
 * will be executed.
 *
 * @param[in,out] context The FAPI_CONTEXT.
 * @param[in]     sig_key_object The Fapi key object which will be used to
 *                sign the passed digest.
 * @param[in]     padding is the padding algorithm used. Possible values are RSA_SSA,
 *                RSA_PPSS (case insensitive). padding MAY be NULL.
 * @param[in]     digest is the data to be signed, already hashed.
 *                digest MUST NOT be NULL.
 * @param[out]    tpm_signature returns the signature in binary form (DER format).
 *                tpm_signature MUST NOT be NULL (callee-allocated).
 * @param[out]    publicKey is the public key of the signing key in PEM format.
 *                publicKey is callee allocated and MAY be NULL.
 * @param[out]    certificate is the certificate associated with the signing key
 *                in PEM format. certificate MAY be NULL.
 *
 * @retval TSS2_RC_SUCCESS If the signing was successful.
 * @retval TSS2_ESYS_RC_* possible error codes of ESAPI.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE If an internal error occurs, which is
 *         not covered by other return codes.
 * @retval TSS2_FAPI_RC_BAD_VALUE If wrong values are detected during execution.
 * @retval TSS2_FAPI_RC_IO_ERROR If an error occurs during access to the policy
 *         store.
 * @retval TSS2_FAPI_RC_PATH_NOT_FOUND If a policy for a certain path was not found.
 * @retval TSS2_FAPI_RC_POLICY_UNKNOWN If policy search for a certain policy digest was
 *         not successful.
 * @retval TSS2_FAPI_RC_BAD_TEMPLATE In a invalid policy is loaded during execution.
 * @retval TPM2_RC_BAD_AUTH If the authentication for an object needed for policy
 *         execution fails.
 * @retval TSS2_FAPI_RC_AUTHORIZATION_UNKNOWN if a needed authorization callback
 *         is not defined.
 * @retval TSS2_FAPI_RC_TRY_AGAIN if an I/O operation is not finished yet and
 *         this function needs to be called again.
 * @retval TSS2_FAPI_RC_BAD_SEQUENCE if the context has an asynchronous
 *         operation already pending.
 * @retval TSS2_FAPI_RC_AUTHORIZATION_FAILED if the authorization attempt fails.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_KEY_NOT_FOUND if a key was not found.
 */
TSS2_RC
ifapi_key_sign(
    FAPI_CONTEXT     *context,
    IFAPI_OBJECT     *sig_key_object,
    char const       *padding,
    TPM2B_DIGEST     *digest,
    TPMT_SIGNATURE  **tpm_signature,
    char            **publicKey,
    char            **certificate)
{
    TSS2_RC r;
    TPMT_SIG_SCHEME sig_scheme;
    ESYS_TR session;

    TPMT_TK_HASHCHECK hash_validation = {
        .tag = TPM2_ST_HASHCHECK,
        .hierarchy = TPM2_RH_OWNER,
    };
    memset(&hash_validation.digest, 0, sizeof(TPM2B_DIGEST));

    switch (context->Key_Sign.state) {
    statecase(context->Key_Sign.state, SIGN_INIT);
        sig_key_object = context->Key_Sign.key_object;
        context->Key_Sign.handle = sig_key_object->public.handle;

        r = ifapi_authorize_object(context, sig_key_object, &session);
        FAPI_SYNC(r, "Authorize signature key.", cleanup);

        context->policy.session = session;

        r = ifapi_get_sig_scheme(context, sig_key_object, padding, digest, &sig_scheme);
        goto_if_error(r, "Get signature scheme", cleanup);

        /* Prepare the signing operation. */
        r = Esys_Sign_Async(context->esys,
                            context->Key_Sign.handle,
                            session,
                            ESYS_TR_NONE, ESYS_TR_NONE,
                            digest,
                            &sig_scheme,
                            &hash_validation);
        goto_if_error(r, "Error: Sign", cleanup);
        fallthrough;

    statecase(context->Key_Sign.state, SIGN_AUTH_SENT);
        context->Key_Sign.signature = NULL;
        r = Esys_Sign_Finish(context->esys,
                             &context->Key_Sign.signature);
        return_try_again(r);
        ifapi_flush_policy_session(context, context->policy.session, r);
        goto_if_error(r, "Error: Sign", cleanup);

        /* Prepare the flushing of the signing key. */
        if (!sig_key_object->misc.key.persistent_handle) {
            r = Esys_FlushContext_Async(context->esys, context->Key_Sign.handle);
            goto_if_error(r, "Error: FlushContext", cleanup);
        }
        fallthrough;

    statecase(context->Key_Sign.state, SIGN_WAIT_FOR_FLUSH);
        if (!sig_key_object->misc.key.persistent_handle) {
            r = Esys_FlushContext_Finish(context->esys);
            return_try_again(r);
            goto_if_error(r, "Error: Sign", cleanup);
        }

        int pem_size;
        if (publicKey) {
            /* Convert internal key object to PEM format. */
            r = ifapi_pub_pem_key_from_tpm(&sig_key_object->misc.key.public,
                                                publicKey,
                                                &pem_size);
            goto_if_error(r, "Conversion pub key to PEM failed", cleanup);
        }
        context->Key_Sign.handle = ESYS_TR_NONE;
        *tpm_signature = context->Key_Sign.signature;
        if (certificate) {
            if (context->Key_Sign.key_object->misc.key.certificate) {
                *certificate = strdup(context->Key_Sign.key_object->misc.key.certificate);
                goto_if_null(*certificate, "Out of memory.",
                             TSS2_FAPI_RC_MEMORY, cleanup);
            } else {
                strdup_check(*certificate, "", r, cleanup);
            }
        }
        context->Key_Sign.state = SIGN_INIT;
        LOG_TRACE("success");
        r = TSS2_RC_SUCCESS;
        break;

    statecasedefault(context->Key_Sign.state);
    }

cleanup:
    if (context->Key_Sign.handle != ESYS_TR_NONE)
        Esys_FlushContext(context->esys, context->Key_Sign.handle);
    ifapi_cleanup_ifapi_object(context->Key_Sign.key_object);
    return r;
}

/** Get json encoding for FAPI object.
 *
 * A json representation which can be used for exporting of a FAPI object will
 * be created.
 *
 * @param[in]   context The FAPI_CONTEXT.
 * @param[in]   object The object to be serialized.
 * @param[out]  json_string The json string created by the deserialzation
 *              function (callee-allocated).
 *
 * @retval TSS2_RC_SUCCESS If the serialization was successful.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 * @retval TSS2_FAPI_RC_BAD_VALUE If wrong values are detected during
 *         serialization.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE If a NULL pointer was passed for
 *         the object.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE if an internal error occurred.
 * @retval TSS2_ESYS_RC_* possible error codes of ESAPI.
 */
TSS2_RC
ifapi_get_json(FAPI_CONTEXT *context, IFAPI_OBJECT *object, char **json_string)
{
    TSS2_RC r = TSS2_RC_SUCCESS;
    json_object *jso = NULL;

    /* Perform esys serialization if necessary */
    r = ifapi_esys_serialize_object(context->esys, object);
    goto_if_error(r, "Prepare serialization", cleanup);

    r = ifapi_json_IFAPI_OBJECT_serialize(object, &jso);
    return_if_error(r, "Serialize duplication object");

    *json_string = strdup(json_object_to_json_string_ext(jso,
                          JSON_C_TO_STRING_PRETTY));
    goto_if_null2(*json_string, "Converting json to string", r, TSS2_FAPI_RC_MEMORY,
                  cleanup);

cleanup:
    if (jso)
        json_object_put(jso);
    return r;
}

/** Serialize persistent objects into buffer of keystore object.
 *
 * NV objects and persistent keys will serialized via the ESYS API to
 * enable reconstruction durinng loading from keystore.
 *
 * @param[in]     ectx The ESAPI context.
 * @param[in,out] object  The nv object or the key.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE if an internal error occured.
 */
TSS2_RC
ifapi_esys_serialize_object(ESYS_CONTEXT *ectx, IFAPI_OBJECT *object)
{
    TSS2_RC r = TSS2_RC_SUCCESS;
    IFAPI_KEY *key_object = NULL;
    IFAPI_NV *nv_object;

    switch (object->objectType) {
    case IFAPI_NV_OBJ:
        nv_object = &object->misc.nv;
        if (nv_object->serialization.buffer != NULL) {
            /* Cleanup old buffer */
            Fapi_Free(nv_object->serialization.buffer);
            nv_object->serialization.buffer = NULL;
        }
        r = Esys_TR_Serialize(ectx, object->public.handle,
                              &nv_object->serialization.buffer,
                              &nv_object->serialization.size);
        return_if_error(r, "Error serialize esys object");
        break;

    case IFAPI_KEY_OBJ:
        key_object = &object->misc.key;
        key_object->serialization.size = 0;
        if (key_object->serialization.buffer != NULL) {
            /* Cleanup old buffer */
            Fapi_Free(key_object->serialization.buffer);
            key_object->serialization.buffer = NULL;
        }
        if (object->public.handle != ESYS_TR_NONE && key_object->persistent_handle) {
            key_object->serialization.buffer = NULL;
            r = Esys_TR_Serialize(ectx, object->public.handle,
                                  &key_object->serialization.buffer,
                                  &key_object->serialization.size);
            return_if_error(r, "Error serialize esys object");
        }
        break;

    default:
        /* Nothing to be done */
        break;
    }
    return TSS2_RC_SUCCESS;
}

 /** Initialize the part of an IFAPI_OBJECT  which is not serialized.
  *
  * For persistent objects the correspodning ESYS object will be created.
  *
  * @param[in,out] ectx The ESYS context.
  * @param[out] object the deserialzed binary object.
  * @retval TSS2_RC_SUCCESS if the function call was a success.
  * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
  */
TSS2_RC
ifapi_initialize_object(
    ESYS_CONTEXT *ectx,
    IFAPI_OBJECT *object)
{
    TSS2_RC r = TSS2_RC_SUCCESS;
    ESYS_TR handle;

    switch (object->objectType) {
    case IFAPI_NV_OBJ:
        if (object->misc.nv.serialization.size > 0) {
            r = Esys_TR_Deserialize(ectx, &object->misc.nv.serialization.buffer[0],
                                    object->misc.nv.serialization.size, &handle);
            goto_if_error(r, "Error dserialize esys object", cleanup);
        } else {
            handle = ESYS_TR_NONE;
        }
        object->authorization_state = AUTH_INIT;
        object->public.handle = handle;
        break;

    case IFAPI_KEY_OBJ:
        if (object->misc.key.serialization.size > 0) {
            r = Esys_TR_Deserialize(ectx, &object->misc.key.serialization.buffer[0],
                                    object->misc.key.serialization.size, &handle);
            goto_if_error(r, "Error deserialize esys object", cleanup);
        } else {
            handle = ESYS_TR_NONE;
        }
        object->authorization_state = AUTH_INIT;
        object->public.handle = handle;
        break;

    default:
        object->authorization_state = AUTH_INIT;
        break;
    }

    return r;

cleanup:
    SAFE_FREE(object->policy);
    return r;
}

/** Prepare key creation with an auth value.
 *
 * The auth value will be copied int the FAPI context for later use in key creation.
 *
 * @param[in,out] context The FAPI_CONTEXT.
 * @param[in]     keyPath the key path without the parent directories
 *                of the key store. (e.g. HE/EK, HS/SRK/mykey)
 * @param[in]     policyPath identifies the policy to be associated with the new key.
 *                policyPath MAY be NULL. If policyPath is NULL then no policy will
 *                be associated with the key.
 * @param[in]     authValue The authentication value of the key.
 *
 * @retval TSS2_RC_SUCCESS If the preparation was successful.
 * @retval TSS2_FAPI_RC_PATH_ALREADY_EXISTS If the object with does already exist in
 *         keystore.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_NO_TPM if FAPI was initialized in no-TPM-mode via its
 *         config file.
 * @retval TSS2_FAPI_RC_BAD_SEQUENCE if the context has an asynchronous
 *         operation already pending.
 * @retval TSS2_FAPI_RC_BAD_PATH if the path is used in inappropriate context
 *         or contains illegal characters.
 * @retval TSS2_FAPI_RC_PATH_NOT_FOUND if a FAPI object path was not found
 *         during authorization.
 */
TSS2_RC
ifapi_key_create_prepare_auth(
    FAPI_CONTEXT  *context,
    char   const *keyPath,
    char   const *policyPath,
    char   const *authValue)
{
    TSS2_RC r;

    memset(&context->cmd.Key_Create.inSensitive, 0, sizeof(TPM2B_SENSITIVE_CREATE));
    if (authValue) {
        /* Copy the auth value */
        if (strlen(authValue) > sizeof(TPMU_HA)) {
            return_error(TSS2_FAPI_RC_BAD_VALUE, "Password too long.");
        }
        memcpy(&context->cmd.Key_Create.inSensitive.sensitive.userAuth.buffer,
               authValue, strlen(authValue));
        context->cmd.Key_Create.inSensitive.sensitive.userAuth.size = strlen(authValue);
    }
    context->cmd.Key_Create.gen_sensitive_random = false;
    context->cmd.Key_Create.inSensitive.sensitive.data.size = 0;
    r = ifapi_key_create_prepare(context, keyPath, policyPath);
    return r;
}

/** Prepare key creation with an auth value and sensitive data.
 *
 * The auth value and the sensitive data will be copied int the FAPI context
 * for later use in key creation.
 *
 * @param[in,out] context The FAPI_CONTEXT.
 * @param[in]     keyPath the key path without the parent directories
 *                of the key store. (e.g. HE/EK, HS/SRK/mykey)
 * @param[in]     policyPath identifies the policy to be associated with the new key.
 *                policyPath MAY be NULL. If policyPath is NULL then no policy will
 *                be associated with the key.
 * @param[in]     dataSize The size of the sensitive data.
 * @param[in]     authValue The authentication value of the key.
 * @param[in]     data The sensitive data.
 *
 * @retval TSS2_RC_SUCCESS If the preparation was successful.
 * @retval TSS2_FAPI_RC_PATH_ALREADY_EXISTS If the object with does already exist in
 *         keystore.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_NO_TPM if FAPI was initialized in no-TPM-mode via its
 *         config file.
 * @retval TSS2_FAPI_RC_BAD_SEQUENCE if the context has an asynchronous
 *         operation already pending.
 * @retval TSS2_FAPI_RC_BAD_PATH if the path is used in inappropriate context
 *         or contains illegal characters.
 * @retval TSS2_FAPI_RC_PATH_NOT_FOUND if a FAPI object path was not found
 *         during authorization.
 */
TSS2_RC
ifapi_key_create_prepare_sensitive(
    FAPI_CONTEXT  *context,
    char    const *keyPath,
    char    const *policyPath,
    size_t         dataSize,
    char    const *authValue,
    uint8_t const *data)
{
    TSS2_RC r;

    memset(&context->cmd.Key_Create.inSensitive, 0, sizeof(TPM2B_SENSITIVE_CREATE));
    if (dataSize > sizeof(context->cmd.Key_Create.inSensitive.sensitive.data.buffer)
        || dataSize == 0) {
        return_error(TSS2_FAPI_RC_BAD_VALUE, "Data too big or equal zero.");
    }
    if (data) {
        /* Copy the sensitive data */
        context->cmd.Key_Create.gen_sensitive_random = false;
        memcpy(&context->cmd.Key_Create.inSensitive.sensitive.data.buffer,
               data, dataSize);
    } else {
        context->cmd.Key_Create.gen_sensitive_random = true;
    }
    context->cmd.Key_Create.inSensitive.sensitive.data.size = dataSize;
    if (authValue) {
        /* Copy the auth value. */
        if (strlen(authValue) > sizeof(TPMU_HA)) {
            return_error(TSS2_FAPI_RC_BAD_VALUE, "Password too long.");
        }
        memcpy(&context->cmd.Key_Create.inSensitive.sensitive.userAuth.buffer,
               authValue, strlen(authValue));
        context->cmd.Key_Create.inSensitive.sensitive.userAuth.size = strlen(authValue);
    }
    r = ifapi_key_create_prepare(context, keyPath, policyPath);
    return r;
}

/** Prepare key creation if possible.
 *
 * It will be checked whether the object already exists in key store and the FAPI context
 * will be initialized appropriate for key creation.
 *
 * @param[in,out] context The FAPI_CONTEXT.
 * @param[in]     keyPath the key path without the parent directories
 *                of the key store. (e.g. HE/EK, HS/SRK/mykey)
 * @param[in]     policyPath identifies the policy to be associated with the new key.
 *                policyPath MAY be NULL. If policyPath is NULL then no policy will
 *                be associated with the key.
 *
 * @retval TSS2_RC_SUCCESS If the preparation was successful.
 * @retval TSS2_FAPI_RC_PATH_ALREADY_EXISTS If the object with does already exist in
 *         keystore.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_NO_TPM if FAPI was initialized in no-TPM-mode via its
 *         config file.
 * @retval TSS2_FAPI_RC_BAD_SEQUENCE if the context has an asynchronous
 *         operation already pending.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_BAD_PATH if the path is used in inappropriate context
 *         or contains illegal characters.
 * @retval TSS2_FAPI_RC_PATH_NOT_FOUND if a FAPI object path was not found
 *         during authorization.
 */
TSS2_RC
ifapi_key_create_prepare(
    FAPI_CONTEXT  *context,
    char   const *keyPath,
    char   const *policyPath)
{
    TSS2_RC r;
    IFAPI_OBJECT *object = &context->cmd.Key_Create.object;
    NODE_STR_T *path_list = NULL;

    LOG_TRACE("call");
    r = ifapi_session_init(context);
    return_if_error(r, "Initialize Key_Create");

    /* First check whether an existing object would be overwritten */
    r = ifapi_keystore_check_overwrite(&context->keystore, keyPath);
    return_if_error2(r, "Check overwrite %s", keyPath);

    context->srk_handle = 0;

    /* Clear the memory used for the the new key object */
    memset(&context->cmd.Key_Create.outsideInfo, 0, sizeof(TPM2B_DATA));
    memset(&context->cmd.Key_Create.creationPCR, 0, sizeof(TPML_PCR_SELECTION));
    memset(object, 0, sizeof(IFAPI_OBJECT));

    strdup_check(context->cmd.Key_Create.policyPath, policyPath, r, error);
    strdup_check(context->cmd.Key_Create.keyPath, keyPath, r, error);
    r = get_explicit_key_path(&context->keystore, keyPath, &path_list);
    return_if_error(r, "Compute explicit path.");

    context->loadKey.path_list = path_list;
    char *file;
    r = ifapi_path_string(&file, NULL, path_list, NULL);
    goto_if_error(r, "Compute explicit path.", error);

    LOG_DEBUG("Explicit key path: %s", file);

    free(file);

    context->cmd.Key_Create.state = KEY_CREATE_INIT;

    return TSS2_RC_SUCCESS;

error:
    free_string_list(path_list);
    return r;
}

/** State machine for key creation.
 *
 * The function for the preparation of the key have to called before the state machine can
 * be activated. The linked list for the used directories must be available in the
 * FAPI context.
 * It will be checked whether the object already exists in key store and the FAPI context
 * will be initialized appropriate for key creation.
 *
 * @param[in,out] context The FAPI_CONTEXT.
 * @param[in] template The template which defines the key attributes and whether the
 *            key will be persistent.
 *
 * @retval TSS2_RC_SUCCESS If the key could be generated.
 * @retval TSS2_ESYS_RC_* possible error codes of ESAPI.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE If an internal error occurs, which is
 *         not covered by other return codes.
 * @retval TSS2_FAPI_RC_BAD_VALUE If wrong values are detected during execution.
 * @retval TSS2_FAPI_RC_IO_ERROR If an error occurs during access to the policy
 *         store.
 * @retval TSS2_FAPI_RC_PATH_NOT_FOUND If an object needed for creation or
           authentication was not found.
 * @retval TSS2_FAPI_RC_POLICY_UNKNOWN If policy search for a certain policy digest was
 *         not successful.
 * @retval TPM2_RC_BAD_AUTH If the authentication for an object needed for creation
 *         fails.
 * @retval TSS2_FAPI_RC_AUTHORIZATION_UNKNOWN if a needed authorization callback
 *         is not defined.
 * @retval TSS2_FAPI_RC_TRY_AGAIN if an I/O operation is not finished yet and
 *         this function needs to be called again.
 * @retval TSS2_FAPI_RC_BAD_SEQUENCE if the context has an asynchronous
 *         operation already pending.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_NOT_PROVISIONED FAPI was not provisioned.
 * @retval TSS2_FAPI_RC_KEY_NOT_FOUND if a key was not found.
 * @retval TSS2_FAPI_RC_BAD_PATH if the path is used in inappropriate context
 *         or contains illegal characters.
 * @retval TSS2_FAPI_RC_AUTHORIZATION_FAILED if the authorization attempt fails.
 * @retval TSS2_FAPI_RC_PATH_ALREADY_EXISTS if the object already exists in object store.
 */
TSS2_RC
ifapi_key_create(
    FAPI_CONTEXT *context,
    IFAPI_KEY_TEMPLATE *template)
{
    TSS2_RC r;
    size_t path_length;
    NODE_STR_T *path_list = context->loadKey.path_list;
    TPM2B_PUBLIC *outPublic = NULL;
    TPM2B_PRIVATE *outPrivate = NULL;
    TPM2B_CREATION_DATA *creationData = NULL;
    TPM2B_DIGEST *creationHash = NULL;
    TPMT_TK_CREATION *creationTicket = NULL;
    IFAPI_OBJECT *object = &context->cmd.Key_Create.object;
    IFAPI_OBJECT *hierarchy = &context->cmd.Key_Create.hierarchy;
    ESYS_TR auth_session;
    uint8_t *random_data = NULL;

    LOG_TRACE("call");

    switch (context->cmd.Key_Create.state) {
    statecase(context->cmd.Key_Create.state, KEY_CREATE_INIT);
        context->cmd.Key_Create.public_templ = *template;
        context->loadKey.auth_object.public.handle = ESYS_TR_NONE;

        /* Profile name is first element of the explicit path list */
        char *profile_name = context->loadKey.path_list->str;
        r = ifapi_profiles_get(&context->profiles, profile_name, &context->cmd.Key_Create.profile);
        goto_if_error_reset_state(r, "Retrieving profile data", error_cleanup);

        if (context->cmd.Key_Create.inSensitive.sensitive.data.size > 0) {
            /* A keyed hash object sealing sensitive data will be created */
            context->cmd.Key_Create.public_templ.public.publicArea.type = TPM2_ALG_KEYEDHASH;
            context->cmd.Key_Create.public_templ.public.publicArea.nameAlg =
                    context->cmd.Key_Create.profile->nameAlg;
            if (context->cmd.Key_Create.public_templ.public.publicArea.objectAttributes &
                TPMA_OBJECT_SIGN_ENCRYPT) {
                TPMS_KEYEDHASH_PARMS *details;
                details = &context->cmd.Key_Create.public_templ.public.publicArea.parameters.keyedHashDetail;
                details->scheme.scheme = TPM2_ALG_HMAC;
                details->scheme.details.hmac.hashAlg =  context->cmd.Key_Create.profile->nameAlg;
            } else {
                context->cmd.Key_Create.public_templ.public.publicArea.parameters.keyedHashDetail.scheme.scheme =
                    TPM2_ALG_NULL;
            }
        } else {
            r = ifapi_merge_profile_into_template(context->cmd.Key_Create.profile,
                                                  &context->cmd.Key_Create.public_templ);
            goto_if_error_reset_state(r, "Merge profile", error_cleanup);
        }

        if (context->cmd.Key_Create.policyPath
                && strcmp(context->cmd.Key_Create.policyPath, "") != 0)
            context->cmd.Key_Create.state = KEY_CREATE_CALCULATE_POLICY;
        /* else jump over to KEY_CREATE_WAIT_FOR_SESSION below */
    /* FALLTHRU */

    case KEY_CREATE_CALCULATE_POLICY:
        if (context->cmd.Key_Create.state == KEY_CREATE_CALCULATE_POLICY) {
            r = ifapi_calculate_tree(context, context->cmd.Key_Create.policyPath,
                                     &context->policy.policy,
                                     context->cmd.Key_Create.public_templ.public.publicArea.nameAlg,
                                     &context->policy.digest_idx,
                                     &context->policy.hash_size);
            return_try_again(r);
            goto_if_error2(r, "Calculate policy tree %s", error_cleanup,
                           context->cmd.Key_Create.policyPath);

            /* Store the calculated policy in the key object */
            object->policy = calloc(1, sizeof(TPMS_POLICY));
            return_if_null(object->policy, "Out of memory",
                    TSS2_FAPI_RC_MEMORY);
            *(object->policy) = context->policy.policy;

            context->cmd.Key_Create.public_templ.public.publicArea.authPolicy.size =
                context->policy.hash_size;
            memcpy(&context->cmd.Key_Create.public_templ.public.publicArea.authPolicy.buffer[0],
                   &context->policy.policy.policyDigests.digests[context->policy.digest_idx].digest,
                   context->policy.hash_size);
        }
        r = ifapi_get_sessions_async(context,
                                     IFAPI_SESSION_GENEK | IFAPI_SESSION1,
                                     TPMA_SESSION_ENCRYPT | TPMA_SESSION_DECRYPT, 0);
        goto_if_error_reset_state(r, "Create sessions", error_cleanup);
        fallthrough;

    statecase(context->cmd.Key_Create.state, KEY_CREATE_WAIT_FOR_SESSION);
        LOG_TRACE("KEY_CREATE_WAIT_FOR_SESSION");
        r = ifapi_get_sessions_finish(context, context->cmd.Key_Create.profile,
                                      context->cmd.Key_Create.profile->nameAlg);
        return_try_again(r);
        goto_if_error_reset_state(r, " FAPI create session", error_cleanup);
        fallthrough;

    statecase(context->cmd.Key_Create.state, KEY_CREATE_WAIT_FOR_RANDOM);
        if (context->cmd.Key_Create.gen_sensitive_random) {
            r = ifapi_get_random(context,
                                 context->cmd.Key_Create.inSensitive.sensitive.data.size,
                                 &random_data);
            return_try_again(r);
            goto_if_error_reset_state(r, "FAPI GetRandom", error_cleanup);

            /* Copy the sensitive data */
            memcpy(&context->cmd.Key_Create.inSensitive.sensitive.data.buffer,
                   random_data,
                   context->cmd.Key_Create.inSensitive.sensitive.data.size);
            SAFE_FREE(random_data);
        }
        path_length = ifapi_path_length(path_list);
        r = ifapi_load_key_async(context, path_length - 1);
        goto_if_error(r, "LoadKey async", error_cleanup);
        fallthrough;

    statecase(context->cmd.Key_Create.state, KEY_CREATE_WAIT_FOR_PARENT);
        LOG_TRACE("KEY_CREATE_WAIT_FOR_PARENT");
        r = ifapi_load_key_finish(context, IFAPI_FLUSH_PARENT);
        return_try_again(r);
        goto_if_error(r, "LoadKey finish", error_cleanup);
        fallthrough;

    statecase(context->cmd.Key_Create.state, KEY_CREATE_WAIT_FOR_AUTHORIZATION);
        r = ifapi_authorize_object(context, &context->loadKey.auth_object, &auth_session);
        FAPI_SYNC(r, "Authorize key.", error_cleanup);

        r = Esys_Create_Async(context->esys, context->loadKey.auth_object.public.handle,
                              auth_session,
                              ESYS_TR_NONE, ESYS_TR_NONE,
                              &context->cmd.Key_Create.inSensitive,
                              &context->cmd.Key_Create.public_templ.public,
                              &context->cmd.Key_Create.outsideInfo,
                              &context->cmd.Key_Create.creationPCR);
        goto_if_error(r, "Create_Async", error_cleanup);
        fallthrough;

    statecase(context->cmd.Key_Create.state, KEY_CREATE_AUTH_SENT);
        r = Esys_Create_Finish(context->esys, &outPrivate, &outPublic, &creationData,
                               &creationHash, &creationTicket);
        try_again_or_error_goto(r, "Key create finish", error_cleanup);

        /* Prepare object for serialization */
        object->system = context->cmd.Key_Create.public_templ.system;
        object->objectType = IFAPI_KEY_OBJ;
        object->misc.key.public = *outPublic;
        object->misc.key.private.size = outPrivate->size;
        object->misc.key.private.buffer = calloc(1, outPrivate->size);
        goto_if_null2( object->misc.key.private.buffer, "Out of memory.", r,
                       TSS2_FAPI_RC_MEMORY, error_cleanup);

        object->misc.key.private.buffer = memcpy(&object->misc.key.private.buffer[0],
                                                 &outPrivate->buffer[0], outPrivate->size);
        object->misc.key.policyInstance = NULL;
        object->misc.key.creationData = *creationData;
        object->misc.key.creationHash = *creationHash;
        object->misc.key.creationTicket = *creationTicket;
        object->misc.key.description = NULL;
        object->misc.key.certificate = NULL;
        SAFE_FREE(creationData);
        SAFE_FREE(creationTicket);
        SAFE_FREE(creationHash);
        if (context->cmd.Key_Create.inSensitive.sensitive.userAuth.size > 0)
            object->misc.key.with_auth = TPM2_YES;
        else
            object->misc.key.with_auth = TPM2_NO;;
        r = ifapi_get_name(&outPublic->publicArea, &object->misc.key.name);
        goto_if_error(r, "Get key name", error_cleanup);

        SAFE_FREE(outPrivate);
        SAFE_FREE(outPublic);

        if (object->misc.key.public.publicArea.type == TPM2_ALG_RSA)
            object->misc.key.signing_scheme = context->cmd.Key_Create.profile->rsa_signing_scheme;
        else
            object->misc.key.signing_scheme = context->cmd.Key_Create.profile->ecc_signing_scheme;

        fallthrough;

    statecase(context->cmd.Key_Create.state, KEY_CREATE_WAIT_FOR_LOAD_AUTHORIZATION);
        if (template->persistent_handle) {
            r = ifapi_authorize_object(context, &context->loadKey.auth_object, &auth_session);
            FAPI_SYNC(r, "Authorize key.", error_cleanup);

            TPM2B_PRIVATE private;
            private.size = object->misc.key.private.size;
            memcpy(&private.buffer[0], &object->misc.key.private.buffer[0],
                   private.size);

            r = Esys_Load_Async(context->esys, context->loadKey.handle,
                                auth_session,
                                ESYS_TR_NONE, ESYS_TR_NONE,
                                &private,
                                &object->misc.key.public);
            goto_if_error(r, "Load key.", error_cleanup);

        }
        fallthrough;

    statecase(context->cmd.Key_Create.state, KEY_CREATE_WAIT_FOR_KEY);
        if (template->persistent_handle) {
            r = Esys_Load_Finish(context->esys, &context->loadKey.handle);
            return_try_again(r);
            goto_if_error_reset_state(r, "Load", error_cleanup);
        }
        /* Prepare Flushing of key used for authorization */
        if (!context->loadKey.auth_object.misc.key.persistent_handle) {
            r = Esys_FlushContext_Async(context->esys, context->loadKey.auth_object.public.handle);
            goto_if_error(r, "Flush parent", error_cleanup);
        }
        fallthrough;

    statecase(context->cmd.Key_Create.state, KEY_CREATE_FLUSH1);
        if (!context->loadKey.auth_object.misc.key.persistent_handle) {
            r = Esys_FlushContext_Finish(context->esys);
            try_again_or_error_goto(r, "Flush context", error_cleanup);

            ifapi_cleanup_ifapi_object(&context->loadKey.auth_object);
        }
        if (template->persistent_handle) {
            r = ifapi_keystore_load_async(&context->keystore, &context->io, "/HS");
            return_if_error2(r, "Could not open hierarchy /HS");
        }
        fallthrough;

    statecase(context->cmd.Key_Create.state, KEY_CREATE_WAIT_FOR_HIERARCHY);
        if (template->persistent_handle) {
            r = ifapi_keystore_load_finish(&context->keystore, &context->io, hierarchy);
            return_try_again(r);
            return_if_error(r, "read_finish failed");
            r = ifapi_initialize_object(context->esys, hierarchy);
            goto_if_error_reset_state(r, "Initialize hierarchy object", error_cleanup);

            hierarchy->public.handle = ESYS_TR_RH_OWNER;
        }
        fallthrough;

    statecase(context->cmd.Key_Create.state, KEY_CREATE_AUTHORIZE_HIERARCHY);
        if (template->persistent_handle) {
            r = ifapi_authorize_object(context, hierarchy, &auth_session);
            FAPI_SYNC(r, "Authorize hierarchy.", error_cleanup);

            object->misc.key.persistent_handle = template->persistent_handle;

            /* Prepare making the loaded key permanent. */
            r = Esys_EvictControl_Async(context->esys, hierarchy->public.handle,
                                        context->loadKey.handle,
                                        auth_session, ESYS_TR_NONE,
                                        ESYS_TR_NONE,
                                        object->misc.key.persistent_handle);
            goto_if_error(r, "Error Esys EvictControl", error_cleanup);

            ifapi_cleanup_ifapi_object(hierarchy);
        }
        fallthrough;

    statecase(context->cmd.Key_Create.state, KEY_CREATE_WAIT_FOR_EVICT_CONTROL);
        if (template->persistent_handle) {
            /* Prepare making the loaded key permanent. */
            r = Esys_EvictControl_Finish(context->esys, &object->public.handle);
            return_try_again(r);
            goto_if_error(r, "Evict control failed", error_cleanup);
        }

        fallthrough;

    statecase(context->cmd.Key_Create.state, KEY_CREATE_FLUSH2);
        /* Flush the key which was evicted. */
        if (template->persistent_handle) {
            r = ifapi_flush_object(context, context->loadKey.handle);
            return_try_again(r);
            goto_if_error(r, "Flush key", error_cleanup);
        }

        fallthrough;

    statecase(context->cmd.Key_Create.state, KEY_CREATE_WRITE_PREPARE);
        if (template->persistent_handle) {
            /* Compute the serialization, which will be used for the
               reconstruction of the key object. */
            SAFE_FREE(object->misc.key.serialization.buffer);
            r = Esys_TR_Serialize(context->esys, object->public.handle,
                                  &object->misc.key.serialization.buffer,
                                  &object->misc.key.serialization.size);
            goto_if_error(r, "Serialize object", error_cleanup);
        }

        /* Perform esys serialization if necessary */
        r = ifapi_esys_serialize_object(context->esys, object);
        goto_if_error(r, "Prepare serialization", error_cleanup);

        /* Check whether object already exists in key store.*/
        r = ifapi_keystore_object_does_not_exist(&context->keystore,
                                                 context->cmd.Key_Create.keyPath,
                                                 object);
        goto_if_error_reset_state(r, "Could not write: %s", error_cleanup,
                                  context->cmd.Key_Create.keyPath);

        /* Start writing the object to the key store */
        r = ifapi_keystore_store_async(&context->keystore, &context->io,
                                       context->cmd.Key_Create.keyPath, object);
        goto_if_error_reset_state(r, "Could not open: %s", error_cleanup,
                                  context->cmd.Key_Create.keyPath);
        ifapi_cleanup_ifapi_object(object);
        fallthrough;

    statecase(context->cmd.Key_Create.state, KEY_CREATE_WRITE);
        /* Finish writing the key to the key store */
        r = ifapi_keystore_store_finish(&context->io);
        return_try_again(r);
        return_if_error_reset_state(r, "write_finish failed");

        fallthrough;

    statecase(context->cmd.Key_Create.state, KEY_CREATE_CLEANUP);
        r = ifapi_cleanup_session(context);
        try_again_or_error_goto(r, "Cleanup", error_cleanup);

        context->cmd.Key_Create.state = KEY_CREATE_INIT;
        r = TSS2_RC_SUCCESS;
        break;

    statecasedefault(context->cmd.Key_Create.state);
    }

 cleanup:
    free_string_list(context->loadKey.path_list);
    SAFE_FREE(outPublic);
    SAFE_FREE(outPrivate);
    SAFE_FREE(creationData);
    SAFE_FREE(creationHash);
    SAFE_FREE(creationTicket);
    SAFE_FREE(context->cmd.Key_Create.policyPath);
    SAFE_FREE(context->cmd.Key_Create.keyPath);
    SAFE_FREE(random_data);
    ifapi_cleanup_ifapi_object(object);
    ifapi_session_clean(context);
    if  (template->persistent_handle)
        ifapi_cleanup_ifapi_object(hierarchy);
    return r;

 error_cleanup:
    if  (template->persistent_handle)
        ifapi_cleanup_ifapi_object(hierarchy);
    if (context->loadKey.auth_object.public.handle != ESYS_TR_NONE &&
        !context->loadKey.auth_object.misc.key.persistent_handle) {
        Esys_FlushContext(context->esys, context->loadKey.auth_object.public.handle);
    }
    goto cleanup;
}

/** Get signature scheme for key.
 *
 * If padding is passed the scheme will be derived from paddint otherwise
 * the scheme form object will be used.
 *
 * @param[in] context The FAPI_CONTEXT.
 * @param[in] object The internal FAPI object of the key.
 * @param[in] padding The strings RSA_SSA or RSA_PSS will be converted
 *            into the TSS constants used for the signing scheme.
 * @param[in] digest The digest size will be used to determine the hashalg
 *            for the signature scheme.
 * @param[out] sig_scheme The computed signature scheme.
 *
 * @retval TSS2_FAPI_RC_BAD_VALUE If the digest size is not appropriate.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_get_sig_scheme(
    FAPI_CONTEXT *context,
    IFAPI_OBJECT *object,
    char const *padding,
    TPM2B_DIGEST *digest,
    TPMT_SIG_SCHEME *sig_scheme)
{
    TPMI_ALG_HASH hash_alg;
    TSS2_RC r;

    /* Get hash algorithm from digest size */
    r = ifapi_get_hash_alg_for_size(digest->size, &hash_alg);
    return_if_error2(r, "Invalid digest size");

    if (digest->size == TPM2_SM3_256_DIGEST_SIZE &&
        object->misc.key.signing_scheme.details.any.hashAlg == TPM2_ALG_SM3_256) {
        hash_alg = TPM2_ALG_SM3_256;
    }

    if (padding) {
        /* Use scheme object from context */
        if (strcasecmp("RSA_SSA", padding) == 0) {
            context->Key_Sign.scheme.scheme = TPM2_ALG_RSASSA;
            context->Key_Sign.scheme.details.rsassa.hashAlg = hash_alg;
        }
        if (strcasecmp("RSA_PSS", padding) == 0) {
            context->Key_Sign.scheme.scheme = TPM2_ALG_RSAPSS;
            context->Key_Sign.scheme.details.rsapss.hashAlg = hash_alg;
        }
        *sig_scheme = context->Key_Sign.scheme;
        return TSS2_RC_SUCCESS;
    } else {
        /* Use scheme defined for object */
        *sig_scheme = object->misc.key.signing_scheme;
        sig_scheme->details.any.hashAlg = hash_alg;
        return TSS2_RC_SUCCESS;
    }
}

/** State machine for changing the hierarchy authorization.
 *
 * First it will be tried to set the auth value of the hierarchy with a
 * "null" authorization. If this trial is not successful it will be tried to
 * authorize the hierarchy via a callback.
 * If an not null auth value is passed with_auth is set to yes for the
 * object otherwise to no. So for later authorizations it will be clear
 * whether null authorization is possible or not.
 *
 * @param[in] context The FAPI_CONTEXT.
 * @param[in] handle The ESAPI handle of the hierarchy.
 * @param[in,out] hierarchy_object The internal FAPI representation of a
 *                hierarchy.
 * @param[in] newAuthValue The new authorization for the hierarchy.
 *
 * @retval TSS2_RC_SUCCESS on success.
 * @retval TSS2_ESYS_RC_* possible error codes of ESAPI.
 * @retval TSS2_FAPI_RC_TRY_AGAIN if an I/O operation is not finished yet and
 *         this function needs to be called again.
 * @retval TSS2_FAPI_RC_BAD_SEQUENCE if the context has an asynchronous
 *         operation already pending.
 * @retval TSS2_FAPI_RC_AUTHORIZATION_UNKNOWN if a required authorization callback
 *         is not set.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 * @retval TSS2_FAPI_RC_AUTHORIZATION_FAILED if the authorization attempt fails.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE if an internal error occured.
 * @retval TSS2_FAPI_RC_PATH_NOT_FOUND if a FAPI object path was not found
 *         during authorization.
 * @retval TSS2_FAPI_RC_KEY_NOT_FOUND if a key was not found.
 * @retval TSS2_FAPI_RC_IO_ERROR if an error occured while accessing the
 *         object store.
 * @retval TSS2_FAPI_RC_POLICY_UNKNOWN if policy search for a certain policy digest
 *         was not successful.
 */
TSS2_RC
ifapi_change_auth_hierarchy(
    FAPI_CONTEXT *context,
    ESYS_TR handle,
    IFAPI_OBJECT *hierarchy_object,
    TPM2B_AUTH *newAuthValue)
{
    TSS2_RC r;
    ESYS_TR auth_session;

    switch (context->hierarchy_state) {
    statecase(context->hierarchy_state, HIERARCHY_CHANGE_AUTH_INIT);
        if (hierarchy_object->misc.hierarchy.with_auth == TPM2_YES ||
            policy_digest_size(hierarchy_object)) {
            r = ifapi_authorize_object(context, hierarchy_object, &auth_session);
            FAPI_SYNC(r, "Authorize hierarchy.", error);
        } else {
            auth_session = context->session1;
        }

        r = Esys_HierarchyChangeAuth_Async(context->esys,
                                           handle,
                                           (auth_session
                                            && auth_session != ESYS_TR_NONE) ?
                                           auth_session : ESYS_TR_PASSWORD,
                                           ESYS_TR_NONE, ESYS_TR_NONE,
                                           newAuthValue);
        return_if_error(r, "HierarchyChangeAuth");
        fallthrough;

    statecase(context->hierarchy_state, HIERARCHY_CHANGE_AUTH_NULL_AUTH_SENT);
        r = Esys_HierarchyChangeAuth_Finish(context->esys);
        return_try_again(r);

        if  (number_rc(r) == TPM2_RC_BAD_AUTH &&
             hierarchy_object->misc.hierarchy.with_auth == TPM2_NO) {

            /* Retry after NULL authorization was not successful */
            char *description;
            r = ifapi_get_description(hierarchy_object, &description);
            return_if_error(r, "Get description");

            r = ifapi_set_auth(context, hierarchy_object, description);
            SAFE_FREE(description);
            return_if_error(r, "HierarchyChangeAuth");

            r = Esys_HierarchyChangeAuth_Async(context->esys,
                                               handle,
                                               (context->session1
                                                && context->session1 != ESYS_TR_NONE) ?
                                               context->session1 : ESYS_TR_PASSWORD,
                                               ESYS_TR_NONE, ESYS_TR_NONE,
                                               newAuthValue);
            return_if_error(r, "HierarchyChangeAuth");
            return TSS2_FAPI_RC_TRY_AGAIN;
        }
        return_if_error(r, "HierarchyChangeAuth");

        if (newAuthValue->size > 0)
            hierarchy_object->misc.hierarchy.with_auth = TPM2_YES;
        else
            hierarchy_object->misc.hierarchy.with_auth = TPM2_NO;

        context->hierarchy_state = HIERARCHY_CHANGE_AUTH_INIT;
        return r;

    statecasedefault(context->hierarchy_state);
    }
error:
    return r;
}

/** State machine for changing the policy of a hierarchy.
 *
 * Based on a passed policy the policy digest will be computed.
 * First it will be tried to set the policy of the hierarchy with a
 * "null" authorization. If this trial is not successful it will be tried to
 * authorize the hierarchy via a callback.
 * If an not null auth value is passed with_auth is set to yes for the
 * object otherwise to no. So for later authorizations it will be clear
 * whether null authorization is possible or not.
 *
 * @param[in] context The FAPI_CONTEXT.
 * @param[in] handle The ESAPI handle of the hierarchy.
 * @param[in,out] hierarchy_object The internal FAPI representation of a
 *                hierarchy.
 * @param[in] policy The new policy assigned to the hierarchy.
 *
 * @retval TSS2_RC_SUCCESS on success.
 * @retval TSS2_ESYS_RC_* possible error codes of ESAPI.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE If an internal error occurs, which is
 *         not covered by other return codes.
 * @retval TSS2_FAPI_RC_BAD_VALUE If wrong values are detected during policy calculation.
 * @retval TSS2_FAPI_RC_IO_ERROR If an error occurs during access to the policy
 *         store.
 * @retval TSS2_FAPI_RC_PATH_NOT_FOUND If an object needed for policy calculation was
 *         not found.
 * @retval TSS2_FAPI_RC_POLICY_UNKNOWN If policy search for a certain policy digest was
 *         not successful.
 * @retval TSS2_FAPI_RC_TRY_AGAIN if an I/O operation is not finished yet and
 *         this function needs to be called again.
 * @retval TSS2_FAPI_RC_BAD_SEQUENCE if the context has an asynchronous
 *         operation already pending.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_KEY_NOT_FOUND if a key was not found.
 * @retval TSS2_FAPI_RC_AUTHORIZATION_UNKNOWN if a required authorization callback
 *         is not set.
 * @retval TSS2_FAPI_RC_AUTHORIZATION_FAILED if the authorization attempt fails.
 * @retval TSS2_FAPI_RC_NOT_PROVISIONED FAPI was not provisioned.
 * @retval TSS2_FAPI_RC_BAD_PATH if the path is used in inappropriate context
 *         or contains illegal characters.
 */
TSS2_RC
ifapi_change_policy_hierarchy(
    FAPI_CONTEXT *context,
    ESYS_TR handle,
    IFAPI_OBJECT *hierarchy_object,
    TPMS_POLICY *policy)
{
    TSS2_RC r;
    ESYS_TR auth_session;

    switch (context->hierarchy_policy_state) {
    statecase(context->hierarchy_policy_state, HIERARCHY_CHANGE_POLICY_INIT);
        if ((! policy || ! policy->policy) && !hierarchy_object->policy) {
            /* No policy will be used for hierarchy */
            return TSS2_RC_SUCCESS;
        }
        fallthrough;

    statecase(context->hierarchy_policy_state, HIERARCHY_CHANGE_POLICY_AUTHORIZE);
        if (hierarchy_object->misc.hierarchy.with_auth == TPM2_YES ||
            policy_digest_size(hierarchy_object)) {
            r = ifapi_authorize_object(context, hierarchy_object, &auth_session);
            FAPI_SYNC(r, "Authorize hierarchy.", error);
        } else {
            auth_session = context->session1;
        }

        if (policy) {
            context->policy.state = POLICY_INIT;

            /* Calculate the policy digest which will be used as hierarchy policy. */
            r = ifapi_calculate_tree(context, NULL, /**< no path needed */
                                     policy,
                                     context->profiles.default_profile.nameAlg,
                                     &context->cmd.Provision.digest_idx,
                                     &context->cmd.Provision.hash_size);
            goto_if_error(r, "Policy calculation", error);

            /* Policy data will be stored in the provisioning context. */
            context->cmd.Provision.policy_digest.size = context->cmd.Provision.hash_size;
            memcpy(&context->cmd.Provision.policy_digest.buffer[0],
                   &policy
                   ->policyDigests.digests[context->cmd.Provision.digest_idx].digest,
                   context->cmd.Provision.hash_size);

            hierarchy_object->policy = policy;
            hierarchy_object->misc.hierarchy.authPolicy = context->cmd.Provision.policy_digest;
        } else {
            /* No policy will be used for this hierarchy. */
            context->cmd.Provision.policy_digest.size = 0;
            ifapi_cleanup_policy(hierarchy_object->policy);
            SAFE_FREE(hierarchy_object->policy);
            hierarchy_object->policy = NULL;
            hierarchy_object->misc.hierarchy.with_auth = TPM2_NO;
            hierarchy_object->misc.hierarchy.authPolicy.size = 0;
        }

        /* Prepare the setting of the policy. */
        r = Esys_SetPrimaryPolicy_Async(context->esys, handle,
                                        (auth_session
                                         && auth_session != ESYS_TR_NONE) ?
                                        auth_session : ESYS_TR_PASSWORD,
                                        ESYS_TR_NONE, ESYS_TR_NONE,
                                        &context->cmd.Provision.policy_digest,
                                        context->cmd.Provision.policy_digest.size ?
                                        context->profiles.default_profile.nameAlg :
                                        TPM2_ALG_NULL);
        return_if_error(r, "Esys_SetPrimaryPolicy_Async");
        fallthrough;

    statecase(context->hierarchy_policy_state, HIERARCHY_CHANGE_POLICY_NULL_AUTH_SENT);
        r = Esys_SetPrimaryPolicy_Finish(context->esys);
        return_try_again(r);
        if (number_rc(r) == TPM2_RC_BAD_AUTH  &&
             hierarchy_object->misc.hierarchy.with_auth == TPM2_NO) {
            /* Retry after NULL authorization was not successful */
            char *description;
            r = ifapi_get_description(hierarchy_object, &description);
            return_if_error(r, "Get description");

            r = ifapi_set_auth(context, hierarchy_object, description);
            SAFE_FREE(description);
            return_if_error(r, "HierarchyChangePolicy");

            r = Esys_SetPrimaryPolicy_Async(context->esys, handle,
                                            (context->session1
                                             && context->session1 != ESYS_TR_NONE) ?
                                            context->session1 : ESYS_TR_PASSWORD,
                                            ESYS_TR_NONE, ESYS_TR_NONE,
                                            &context->cmd.Provision.policy_digest,
                                            context->profiles.default_profile.nameAlg);
            return_if_error(r, "Esys_SetPrimaryPolicy_Async");
            return TSS2_FAPI_RC_TRY_AGAIN;
        }
        return_if_error(r, "Set primary policy");
        break;

    statecasedefault(context->hierarchy_policy_state);
    }

error:
    return r;
}

/** Allocate ifapi object and store the result in a linked list.
 *
 * Allocated ifapi objects will be recorded in the context.
 *
 * @param[in,out] context The FAPI_CONTEXT.
 *
 * @retval The allocated ifapi object.
 * @retval NULL if the object cannot be allocated.
 */
IFAPI_OBJECT
*ifapi_allocate_object(FAPI_CONTEXT *context)
{
    NODE_OBJECT_T *node = calloc(1, sizeof(NODE_OBJECT_T));
    if (!node)
        return NULL;

    node->object = calloc(1, sizeof(IFAPI_OBJECT));
    if (!node->object) {
        free(node);
        return NULL;
    }
    node->next = context->object_list;
    context->object_list = node;
    return (IFAPI_OBJECT *) node->object;
}

/** Free all ifapi objects stored in the context.
 *
 * @param[in,out] context The FAPI_CONTEXT.
 */
void
ifapi_free_objects(FAPI_CONTEXT *context)
{
    NODE_OBJECT_T *free_node;
    NODE_OBJECT_T *node = context->object_list;
    while (node) {
        free(node->object);
        free_node = node;
        node = node->next;
        free(free_node);
    }
}

/** Free ifapi a object stored in the context.
 *
 * @param[in,out] context The FAPI_CONTEXT.
 * @param[in,out] object The object which should be removed from the
 *                the linked list stored in context.
 */
void
ifapi_free_object(FAPI_CONTEXT *context, IFAPI_OBJECT **object)
{
    NODE_OBJECT_T *node;
    NODE_OBJECT_T **update_ptr;

    for (node = context->object_list,
             update_ptr = &context->object_list;
             node != NULL;
         update_ptr = &node->next, node = node->next) {
        if (node->object == object) {
            *update_ptr = node->next;
            SAFE_FREE(node->object);
            SAFE_FREE(node);
            *object = NULL;
            return;
        }
    }
}

#define ADD_CAPABILITY_INFO(capability, field, subfield, max_count, property_count) \
    if (context->cmd.GetInfo.fetched_data->data.capability.count > max_count - property_count) { \
        context->cmd.GetInfo.fetched_data->data.capability.count = max_count - property_count; \
    } \
\
    memmove(&context->cmd.GetInfo.capability_data->data.capability.field[property_count], \
            context->cmd.GetInfo.fetched_data->data.capability.field, \
            context->cmd.GetInfo.fetched_data->data.capability.count \
            * sizeof(context->cmd.GetInfo.fetched_data->data.capability.field[0]));       \
    property_count += context->cmd.GetInfo.fetched_data->data.capability.count; \
\
    context->cmd.GetInfo.capability_data->data.capability.count = property_count; \
\
    if (more_data && property_count < count \
        && context->cmd.GetInfo.fetched_data->data.capability.count) {  \
        context->cmd.GetInfo.property \
            = context->cmd.GetInfo.capability_data->data. \
            capability.field[property_count - 1]subfield + 1;   \
    } else { \
        more_data = false; \
    }


/** Prepare the receiving of capability data.
 *
 * @param[in,out] context The FAPI_CONTEXT.
 *
 * @retval TSS2_RC_SUCCESS.
 */
TPM2_RC
ifapi_capability_init(FAPI_CONTEXT *context)
{
    context->cmd.GetInfo.capability_data = NULL;
    context->cmd.GetInfo.fetched_data = NULL;

    return TSS2_RC_SUCCESS;


}

/** State machine for receiving TPM capability information.
 *
 * The state machine shares the state with the FAPI function Fapi_GetInfo.
 * context->state == GET_INFO_GET_CAP_MORE signals that more capability data can
 * be retrieved.
 *
 * @param[in,out] context The FAPI_CONTEXT.
 * @param[in]     capability The capability to be retrieved.
 * @param[in]     count The maximal number of items that should be retrieved.
 * @param[out]    capability_data The retrieved capability information.
 *
 * @retval TSS2_RC_SUCCESS If all capability data is retrieved.
 * @retval TSS2_FAPI_RC_TRY_AGAIN if more capability data is available.
 * @retval TSS2_ESYS_RC_* possible error codes of ESAPI.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE if an internal error occurred.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_BAD_SEQUENCE if the context has an asynchronous
 *         operation already pending.
 */
TPM2_RC
ifapi_capability_get(FAPI_CONTEXT *context, TPM2_CAP capability,
                     UINT32 count, TPMS_CAPABILITY_DATA **capability_data) {

    TPMI_YES_NO more_data;
    TSS2_RC r = TSS2_RC_SUCCESS;
    ESYS_CONTEXT *ectx = context->esys;

    switch (context->state) {
    statecase(context->state, GET_INFO_GET_CAP);
        /* fetch capability info */
        context->cmd.GetInfo.fetched_data = NULL;
        context->cmd.GetInfo.capability_data = NULL;
        fallthrough;

    statecase(context->state, GET_INFO_GET_CAP_MORE);
        r = Esys_GetCapability_Async(ectx, ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE,
                                     capability, context->cmd.GetInfo.property,
                                     count - context->cmd.GetInfo.property_count);
        goto_if_error(r, "Error GetCapability", error_cleanup);
        fallthrough;

    statecase(context->state, GET_INFO_WAIT_FOR_CAP);
        r = Esys_GetCapability_Finish(ectx, &more_data, &context->cmd.GetInfo.fetched_data);
        return_try_again(r);
        goto_if_error(r, "Error GetCapability", error_cleanup);

        LOG_TRACE("GetCapability: capability: 0x%x, property: 0x%x", capability,
                  context->cmd.GetInfo.property);

        if (context->cmd.GetInfo.fetched_data->capability != capability) {
            goto_error(r, TSS2_FAPI_RC_GENERAL_FAILURE,
                       "TPM returned different capability than requested: 0x%x != 0x%x",
                       error_cleanup,
                       context->cmd.GetInfo.fetched_data->capability, capability);
        }

        if (context->cmd.GetInfo.capability_data == NULL) {
            /* reuse the TPM's result structure */
            context->cmd.GetInfo.capability_data = context->cmd.GetInfo.fetched_data;

            if (!more_data) {
                /* there won't be another iteration of the loop, just return the result unmodified */
                *capability_data = context->cmd.GetInfo.capability_data;
                return TPM2_RC_SUCCESS;
            }
        }

        /* append the TPM's results to the initial structure, as long as there is still space left */
        switch (capability) {
        case TPM2_CAP_ALGS:
            ADD_CAPABILITY_INFO(algorithms, algProperties, .alg,
                                TPM2_MAX_CAP_ALGS,
                                context->cmd.GetInfo.property_count);
            break;
        case TPM2_CAP_HANDLES:
            ADD_CAPABILITY_INFO(handles, handle,,
                                TPM2_MAX_CAP_HANDLES,
                                context->cmd.GetInfo.property_count);
            break;
        case TPM2_CAP_COMMANDS:
            ADD_CAPABILITY_INFO(command, commandAttributes,,
                                TPM2_MAX_CAP_CC,
                                context->cmd.GetInfo.property_count);
            /* workaround because tpm2-tss does not implement attribute commandIndex for TPMA_CC */
            context->cmd.GetInfo.property &= TPMA_CC_COMMANDINDEX_MASK;
            break;
        case TPM2_CAP_PP_COMMANDS:
            ADD_CAPABILITY_INFO(ppCommands, commandCodes,,
                                TPM2_MAX_CAP_CC,
                                context->cmd.GetInfo.property_count);
            break;
        case TPM2_CAP_AUDIT_COMMANDS:
            ADD_CAPABILITY_INFO(auditCommands, commandCodes,,
                                TPM2_MAX_CAP_CC,
                                context->cmd.GetInfo.property_count);
            break;
        case TPM2_CAP_PCRS:
            ADD_CAPABILITY_INFO(assignedPCR, pcrSelections, .hash,
                                TPM2_NUM_PCR_BANKS,
                                context->cmd.GetInfo.property_count);
            break;
        case TPM2_CAP_TPM_PROPERTIES:
            ADD_CAPABILITY_INFO(tpmProperties, tpmProperty, .property,
                                TPM2_MAX_TPM_PROPERTIES,
                                context->cmd.GetInfo.property_count);
            break;
        case TPM2_CAP_PCR_PROPERTIES:
            ADD_CAPABILITY_INFO(pcrProperties, pcrProperty, .tag,
                                TPM2_MAX_PCR_PROPERTIES,
                                context->cmd.GetInfo.property_count);
            break;
        case TPM2_CAP_ECC_CURVES:
            ADD_CAPABILITY_INFO(eccCurves, eccCurves,,
                                TPM2_MAX_ECC_CURVES,
                                context->cmd.GetInfo.property_count);
            break;
        case TPM2_CAP_VENDOR_PROPERTY:
            /* We will skip over VENDOR_PROPERTY capabilities on FAPI level */
            break;
        default:
            LOG_ERROR("Unsupported capability: 0x%x\n", capability);
            if (context->cmd.GetInfo.fetched_data != context->cmd.GetInfo.capability_data) {
                free(context->cmd.GetInfo.fetched_data);
            }
            free(context->cmd.GetInfo.capability_data);
            *capability_data = NULL;
            return TSS2_FAPI_RC_BAD_VALUE;
        }

        if (context->cmd.GetInfo.fetched_data != context->cmd.GetInfo.capability_data) {
            free(context->cmd.GetInfo.fetched_data);
        }
        *capability_data = context->cmd.GetInfo.capability_data;
        break;

    statecasedefault(context->state);
    }
    if (more_data) {
        context->state = GET_INFO_GET_CAP_MORE;
        return TSS2_FAPI_RC_TRY_AGAIN;
    } else {
        context->state = _FAPI_STATE_INIT;
        return TSS2_RC_SUCCESS;
    }

error_cleanup:
    context->state = _FAPI_STATE_INIT;
    SAFE_FREE(context->cmd.GetInfo.capability_data);
    SAFE_FREE(context->cmd.GetInfo.fetched_data);
    return r;
}

/** Get certificates stored in NV ram.
 *
 * The NV handles in the certificate range are determined. The corresponding
 * certificates are read out and stored in a linked list.
 *
 * @param[in,out] context The FAPI_CONTEXT. The sub context for NV reading
 *                will be used.
 * @param[in] min_handle The first possible handle in the handle range.
 * @param[in] max_handle Maximal handle to filter out the handles not in the
 *            handle range for certificates.
 * @param[out] cert_list The callee allocates linked list of certificates.
 *
 * @retval TSS2_RC_SUCCESS on success.
 * @retval TSS2_ESYS_RC_* possible error codes of ESAPI.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 *
 * @retval TSS2_FAPI_RC_TRY_AGAIN if an I/O operation is not finished yet and
 *         this function needs to be called again.
 * @retval TSS2_FAPI_RC_BAD_SEQUENCE if the context has an asynchronous
 *         operation already pending.
 * @retval TSS2_FAPI_RC_AUTHORIZATION_UNKNOWN if a required authorization callback
 *         is not set.
 * @retval TSS2_FAPI_RC_AUTHORIZATION_FAILED if the authorization attempt fails.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE if an internal error occurred.
 * @retval TSS2_FAPI_RC_IO_ERROR if an error occurred while accessing the
 *         object store.
 * @retval TSS2_FAPI_RC_POLICY_UNKNOWN if policy search for a certain policy digest
 *         was not successful.
 * @retval TSS2_FAPI_RC_NOT_PROVISIONED FAPI was not provisioned.
 * @retval TSS2_FAPI_RC_KEY_NOT_FOUND if a key was not found.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_BAD_PATH if the path is used in inappropriate context
 *         or contains illegal characters.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_PATH_NOT_FOUND if a FAPI object path was not found
 *         during authorization.
 */
TSS2_RC
ifapi_get_certificates(
    FAPI_CONTEXT *context,
    UINT32 min_handle,
    UINT32 max_handle,
    NODE_OBJECT_T **cert_list)
{
    TSS2_RC r;
    TPMI_YES_NO moreData;
    uint8_t *cert_data = NULL;
    size_t cert_size;

    context->cmd.Provision.cert_nv_idx = MIN_EK_CERT_HANDLE;

    switch (context->get_cert_state) {
    statecase(context->get_cert_state, GET_CERT_INIT);
        *cert_list = NULL;
        context->cmd.Provision.capabilityData = NULL;
        context->cmd.Provision.cert_idx = 0;
        /* Prepare the reading of the capability handles in the certificate range */
        r = Esys_GetCapability_Async(context->esys,
                                     ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE,
                                     TPM2_CAP_HANDLES, min_handle,
                                     TPM2_MAX_CAP_HANDLES);
        goto_if_error(r, "Esys_GetCapability_Async", error);
        fallthrough;

    statecase(context->get_cert_state, GET_CERT_WAIT_FOR_GET_CAP);
        r = Esys_GetCapability_Finish(context->esys, &moreData,
                                      &context->cmd.Provision.capabilityData);
        try_again_or_error(r, "GetCapablity_Finish");

        if (!context->cmd.Provision.capabilityData ||
            context->cmd.Provision.capabilityData->data.handles.count == 0) {
            *cert_list = NULL;
            SAFE_FREE(context->cmd.Provision.capabilityData);
            return TSS2_RC_SUCCESS;
        }
        context->cmd.Provision.cert_count =
            context->cmd.Provision.capabilityData->data.handles.count;

        /* Filter out NV handles beyond the EK cert range */
        for (size_t i = 0; i < context->cmd.Provision.cert_count; i++) {
            if (context->cmd.Provision.capabilityData->data.handles.handle[i] > max_handle) {
                context->cmd.Provision.cert_count = i;
                break;
            }
        }
        fallthrough;

    statecase(context->get_cert_state, GET_CERT_GET_CERT_NV);
        goto_if_null(context->cmd.Provision.capabilityData,
            "capabilityData is null", TSS2_FAPI_RC_MEMORY, error);
        context->cmd.Provision.cert_nv_idx
            = context->cmd.Provision.capabilityData
            ->data.handles.handle[context->cmd.Provision.cert_idx];

        ifapi_init_hierarchy_object(&context->nv_cmd.auth_object,
                                    TPM2_RH_OWNER);

        r = Esys_TR_FromTPMPublic_Async(context->esys,
                                        context->cmd.Provision.cert_nv_idx,
                                        ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE);
        goto_if_error_reset_state(r, "Esys_TR_FromTPMPublic_Async", error);
        fallthrough;

    statecase(context->get_cert_state, GET_CERT_GET_CERT_NV_FINISH);
        r = Esys_TR_FromTPMPublic_Finish(context->esys,
                                         &context->cmd.Provision.esys_nv_cert_handle);
        try_again_or_error_goto(r, "TR_FromTPMPublic_Finish", error);

        /* Read public to get size of certificate */
        r = Esys_NV_ReadPublic_Async(context->esys,
                                     context->cmd.Provision.esys_nv_cert_handle,
                                     ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE);
        goto_if_error_reset_state(r, "Esys_NV_ReadPublic_Async", error);
        fallthrough;

    statecase(context->get_cert_state, GET_CERT_GET_CERT_READ_PUBLIC);
        r = Esys_NV_ReadPublic_Finish(context->esys,
                                      &context->cmd.Provision.nvPublic,
                                      NULL);
        try_again_or_error_goto(r, "Error: nv read public", error);

        /* TPMA_NV_NO_DA is set for NV certificate */
        context->nv_cmd.nv_object.misc.nv.public.nvPublic.attributes = TPMA_NV_NO_DA;

        r = ifapi_keystore_load_async(&context->keystore, &context->io, "/HS");
        goto_if_error_reset_state(r, "Could not open hierarchy /HS", error);

        fallthrough;

    statecase(context->get_cert_state, GET_CERT_GET_CERT_READ_HIERARCHY);
        r = ifapi_keystore_load_finish(&context->keystore, &context->io,
                                       &context->nv_cmd.auth_object);
        try_again_or_error_goto(r, "read_finish failed", error);

        /* Prepare context for nv read */
        r = ifapi_initialize_object(context->esys, &context->nv_cmd.auth_object);
        goto_if_error_reset_state(r, "Initialize hierarchy object", error);

        context->nv_cmd.auth_object.public.handle = ESYS_TR_RH_OWNER;
        context->nv_cmd.data_idx = 0;
        context->nv_cmd.auth_index = ESYS_TR_RH_OWNER;
        context->nv_cmd.numBytes = context->cmd.Provision.nvPublic->nvPublic.dataSize;
        context->nv_cmd.esys_handle = context->cmd.Provision.esys_nv_cert_handle;
        context->nv_cmd.offset = 0;
        context->cmd.Provision.pem_cert = NULL;
        context->session1 = ESYS_TR_PASSWORD;
        context->session2 = ESYS_TR_NONE;
        context->nv_cmd.nv_read_state = NV_READ_INIT;
        memset(&context->nv_cmd.nv_object, 0, sizeof(IFAPI_OBJECT));
        SAFE_FREE(context->cmd.Provision.nvPublic);
        fallthrough;

    statecase(context->get_cert_state, GET_CERT_READ_CERT);
        r = ifapi_nv_read(context, &cert_data, &cert_size);
        try_again_or_error_goto(r, " FAPI NV_Read", error);

        context->cmd.Provision.cert_idx += 1;

        /* Add cert to list */
        if (context->cmd.Provision.cert_idx == context->cmd.Provision.cert_count) {
            context->get_cert_state = GET_CERT_GET_CERT_NV;

            r = push_object_with_size_to_list(cert_data, cert_size, cert_list);
            goto_if_error(r, "Store certificate in list.", error);

            ifapi_cleanup_ifapi_object(&context->nv_cmd.auth_object);

            SAFE_FREE(context->cmd.Provision.capabilityData);
            return TSS2_RC_SUCCESS;
        } else {
            context->get_cert_state = GET_CERT_GET_CERT_NV;
            return TSS2_FAPI_RC_TRY_AGAIN;
        }
        break;

    statecasedefault(context->get_cert_state);
    }

error:
    SAFE_FREE(context->cmd.Provision.nvPublic);
    SAFE_FREE(context->cmd.Provision.capabilityData);
    ifapi_cleanup_ifapi_object(&context->nv_cmd.auth_object);
    ifapi_free_object_list(*cert_list);
    return r;
}


/** Get description of an internal FAPI object.
 *
 * @param[in] object The object with the description.
 * @param[out] description The callee allocated description.
 *
 * @retval TSS2_RC_SUCCESS If a copy of the description can be returned
 *         or if no description exists.
 * @retval TSS2_FAPI_RC_MEMORY in the copy cannot be allocated.
 */
TSS2_RC
ifapi_get_description(IFAPI_OBJECT *object, char **description)
{
    char *obj_description = NULL;

    switch (object->objectType) {
    case IFAPI_KEY_OBJ:
        obj_description = object->misc.key.description;
        break;
    case IFAPI_NV_OBJ:
        obj_description = object->misc.nv.description;
        break;
    case IFAPI_HIERARCHY_OBJ:
        if (object->misc.hierarchy.description)
            obj_description = object->misc.hierarchy.description;
        else if (object->public.handle == ESYS_TR_RH_OWNER)
            obj_description = "Owner Hierarchy";
        else if (object->public.handle == ESYS_TR_RH_ENDORSEMENT)
            obj_description = "Endorsement Hierarchy";
        else if (object->public.handle == ESYS_TR_RH_LOCKOUT)
            obj_description = "Lockout Hierarchy";
        else if (object->public.handle == ESYS_TR_RH_NULL)
            obj_description = "Null Hierarchy";
        else
            obj_description = "Hierarchy";
        break;
    default:
        *description = strdup("");
        check_oom(*description);
        return TSS2_RC_SUCCESS;
    }
    if (obj_description) {
        *description = strdup(obj_description);
        check_oom(*description);
    } else {
        *description = strdup("");
        check_oom(*description);
    }
    return TSS2_RC_SUCCESS;
}

/** Set description of an internal FAPI object.
 *
 * @param[in,out] object The object with the description.
 * @param[in] description The description char strint or NULL.
 */
void
ifapi_set_description(IFAPI_OBJECT *object, char *description)
{
    switch (object->objectType) {
    case IFAPI_KEY_OBJ:
        SAFE_FREE(object->misc.key.description);
        object->misc.key.description = description;
        break;
    case IFAPI_NV_OBJ:
        SAFE_FREE(object->misc.nv.description);
        object->misc.nv.description = description;
        break;
    case IFAPI_HIERARCHY_OBJ:
        SAFE_FREE(object->misc.hierarchy.description);
        object->misc.hierarchy.description = description;
        break;
    default:
        LOG_WARNING("Description can't be set");
        break;
    }
}

/** Determine key properties (primary, null hierarchy).
 *
 * It will be checked whether a path is the path of a primary key,
 * and whether it's a key in null hiearchy
 *
 * @param[in,out] context The FAPI_CONTEXT.
 * @param[in]     key_path the key path.
 * @param[out]    is_primary if key path is the path of a primary.
 * @param[out]    in_null_hierarchy if key is a null hierarchy key.
 *
 * @retval TSS2_RC_SUCCESS If the preparation is successful.
 * @retval TSS2_FAPI_RC_MEMORY if memory could not be allocated for path names.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_BAD_PATH if the path is used in inappropriate context
 *         or contains illegal characters.
 * @retval TSS2_FAPI_RC_PATH_NOT_FOUND if a FAPI object path was not found
 *         during authorization.
 */
TSS2_RC
ifapi_get_key_properties(
    FAPI_CONTEXT *context,
    char const *key_path,
    bool *is_primary,
    bool *in_null_hierarchy)
{
    TSS2_RC r;
    NODE_STR_T *path_list = NULL;
    size_t path_length;
    const char *hierarchy;

    LOG_TRACE("Check primary: %s", key_path);

    *is_primary = false;
    *in_null_hierarchy = false;

    r = get_explicit_key_path(&context->keystore, key_path, &path_list);
    return_if_error(r, "Compute explicit path.");

    path_length = ifapi_path_length(path_list);

    if (path_length == 3) {
        if (strncmp("P_", path_list->str, 2) == 0) {
            hierarchy = path_list->next->str;
            if (strcmp(hierarchy,"HS") == 0 ||
                strcmp(hierarchy,"HE") == 0 ||
                strcmp(hierarchy,"HN") == 0) {
                *is_primary = true;
            }
        }
    }
    if (path_length >= 3) {
        hierarchy = path_list->next->str;
        if (strcmp(hierarchy,"HN") == 0)
            *in_null_hierarchy = true;
    }
    free_string_list(path_list);
    return TSS2_RC_SUCCESS;
}

/** Creation of a primary key.
 *
 * Depending on the flags stored in the context the creation of a primary
 * key will be prepared.
 *
 * @param[in] context The FAPI_CONTEXT.
 * @param[in] template The template which defines the key attributes and whether the
 *            key will be persistent.
 * @retval TSS2_RC_SUCCESS on success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if a wrong type was passed.
 * @retval TSS2_ESYS_RC_* possible error codes of ESAPI.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_TRY_AGAIN if an I/O operation is not finished yet and
 *         this function needs to be called again.
 * @retval TSS2_FAPI_RC_BAD_SEQUENCE if the context has an asynchronous
 *         operation already pending.
 * @retval TSS2_FAPI_RC_IO_ERROR if an error occurred while accessing the
 *         object store.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE if an internal error occurred.
 * @retval TSS2_FAPI_RC_PATH_NOT_FOUND if a FAPI object path was not found
 *         during authorization.
 * @retval TSS2_FAPI_RC_KEY_NOT_FOUND if a key was not found.
 * @retval TSS2_FAPI_RC_NOT_PROVISIONED FAPI was not provisioned.
 * @retval TSS2_FAPI_RC_BAD_PATH if the path is used in inappropriate context
 *         or contains illegal characters.
 * @retval TSS2_FAPI_RC_AUTHORIZATION_UNKNOWN if a required authorization callback
 *         is not set.
 * @retval TSS2_FAPI_RC_AUTHORIZATION_FAILED if the authorization attempt fails.
 * @retval TSS2_FAPI_RC_POLICY_UNKNOWN if policy search for a certain policy digest
 *         was not successful.
 * @retval TSS2_FAPI_RC_PATH_ALREADY_EXISTS if the object already exists in object store.
 */
TSS2_RC
ifapi_create_primary(
    FAPI_CONTEXT *context,
    IFAPI_KEY_TEMPLATE *template)
{
    TSS2_RC r;
    ESYS_TR auth_session;
    TPM2B_PUBLIC *outPublic = NULL;
    TPM2B_CREATION_DATA *creationData = NULL;
    TPM2B_DIGEST *creationHash = NULL;
    TPMT_TK_CREATION *creationTicket = NULL;
    IFAPI_OBJECT *object = &context->cmd.Key_Create.object;
    IFAPI_OBJECT *hierarchy = &context->cmd.Key_Create.hierarchy;
    IFAPI_KEY *pkey = &context->cmd.Key_Create.object.misc.key;
    const char *hierarchy_path;
    const char *profile_name;

    /* Compute policy */

    switch (context->cmd.Key_Create.state) {
    statecase(context->cmd.Key_Create.state, KEY_CREATE_PRIMARY_INIT);
        profile_name = context->loadKey.path_list->str;
        r = ifapi_profiles_get(&context->profiles, profile_name,
                               &context->cmd.Key_Create.profile);
        goto_if_error_reset_state(r, "Retrieving profile data", error_cleanup);

        context->cmd.Key_Create.public_templ = *template;
        r = ifapi_merge_profile_into_template(context->cmd.Key_Create.profile,
                                              &context->cmd.Key_Create.public_templ);
        goto_if_error_reset_state(r, "Merge profile", error_cleanup);

        /* Persistent keys are not allowd in the NULL hierarchy. */

        if (template->persistent_handle) {
            hierarchy_path = context->loadKey.path_list->next->str;
            if (strcmp(hierarchy_path, "HN") == 0)
                goto_error_reset_state(r, TSS2_FAPI_RC_BAD_VALUE,
                                       "Persistent keys are not possible in the NULL "
                                       "hierarchy.", error_cleanup);
        }

        if (context->cmd.Key_Create.policyPath
            && strcmp(context->cmd.Key_Create.policyPath, "") != 0)
            context->cmd.Key_Create.state = KEY_CREATE_PRIMARY_CALCULATE_POLICY;
        /* else jump over to KEY_CREATE_PRIMARY_WAIT_FOR_SESSION below */
    /* FALLTHRU */
    case KEY_CREATE_PRIMARY_CALCULATE_POLICY:
        if (context->cmd.Key_Create.state == KEY_CREATE_PRIMARY_CALCULATE_POLICY) {
            r = ifapi_calculate_tree(context, context->cmd.Key_Create.policyPath,
                                     &context->policy.policy,
                                     context->cmd.Key_Create.public_templ.public.publicArea.nameAlg,
                                     &context->policy.digest_idx,
                                     &context->policy.hash_size);
            return_try_again(r);
            goto_if_error2(r, "Calculate policy tree %s", error_cleanup,
                           context->cmd.Key_Create.policyPath);

            /* Store the calculated policy in the key object */
            object->policy = calloc(1, sizeof(TPMS_POLICY));
            return_if_null(object->policy, "Out of memory",
                    TSS2_FAPI_RC_MEMORY);
            *(object->policy) = context->policy.policy;

            context->cmd.Key_Create.public_templ.public.publicArea.authPolicy.size =
                context->policy.hash_size;
            memcpy(&context->cmd.Key_Create.public_templ.public.publicArea.authPolicy.buffer[0],
                   &context->policy.policy.policyDigests.digests[context->policy.digest_idx].digest,
                   context->policy.hash_size);
        }

        r = ifapi_get_sessions_async(context,
                                     IFAPI_SESSION_GENEK | IFAPI_SESSION1,
                                     TPMA_SESSION_ENCRYPT | TPMA_SESSION_DECRYPT, 0);
        goto_if_error_reset_state(r, "Create sessions", error_cleanup);

        fallthrough;

    statecase(context->cmd.Key_Create.state, KEY_CREATE_PRIMARY_WAIT_FOR_SESSION);
        r = ifapi_get_sessions_finish(context, &context->profiles.default_profile,
                                      context->profiles.default_profile.nameAlg);
        return_try_again(r);
        goto_if_error(r, "Create FAPI session.", error_cleanup);

        hierarchy_path = context->loadKey.path_list->next->str;

        r = ifapi_keystore_load_async(&context->keystore, &context->io, hierarchy_path);
        free_string_list(context->loadKey.path_list);
        context->loadKey.path_list = NULL;
        return_if_error2(r, "Could not open hierarchy /%s", hierarchy_path);

        fallthrough;

    statecase(context->cmd.Key_Create.state, KEY_CREATE_PRIMARY_WAIT_FOR_HIERARCHY);
        r = ifapi_keystore_load_finish(&context->keystore, &context->io, hierarchy);
        return_try_again(r);
        return_if_error(r, "read_finish failed");

        r = ifapi_initialize_object(context->esys, hierarchy);
        goto_if_error_reset_state(r, "Initialize hierarchy object", error_cleanup);

        fallthrough;

    statecase(context->cmd.Key_Create.state, KEY_CREATE_PRIMARY_WAIT_FOR_AUTHORIZE1);
        r = ifapi_authorize_object(context, hierarchy, &auth_session);
        FAPI_SYNC(r, "Authorize hierarchy.", error_cleanup);

        r = Esys_CreatePrimary_Async(context->esys, hierarchy->public.handle,
                                     auth_session,
                                     ESYS_TR_NONE, ESYS_TR_NONE,
                                     &context->cmd.Key_Create.inSensitive,
                                     &context->cmd.Key_Create.public_templ.public,
                                     &context->cmd.Key_Create.outsideInfo,
                                     &context->cmd.Key_Create.creationPCR);
        goto_if_error_reset_state(r, "Prepare create primary", error_cleanup);

        fallthrough;

    statecase(context->cmd.Key_Create.state, KEY_CREATE_PRIMARY_WAIT_FOR_PRIMARY);
        r = Esys_CreatePrimary_Finish(context->esys,
                                      &context->cmd.Key_Create.handle,
                                      &outPublic, &creationData, &creationHash,
                                      &creationTicket);
        try_again_or_error_goto(r, "Create primary.", error_cleanup);

        /* Prepare object for serialization */
        object->system = context->cmd.Key_Create.public_templ.system;
        object->objectType = IFAPI_KEY_OBJ;
        object->misc.key.public = *outPublic;
        object->misc.key.private.size = 0;
        object->misc.key.private.buffer = NULL;
        object->misc.key.policyInstance = NULL;
        object->misc.key.creationData = *creationData;
        object->misc.key.creationHash = *creationHash;
        object->misc.key.creationTicket = *creationTicket;
        object->misc.key.description = NULL;
        object->misc.key.certificate = NULL;
        object->misc.key.reset_count = context->init_time.clockInfo.resetCount;
        SAFE_FREE(pkey->serialization.buffer);
        r = Esys_TR_Serialize(context->esys, context->cmd.Key_Create.handle,
                              &pkey->serialization.buffer, &pkey->serialization.size);
        goto_if_error(r, "Error serialize esys object", error_cleanup);
        SAFE_FREE(creationData);
        SAFE_FREE(creationTicket);
        SAFE_FREE(creationHash);
        if (context->cmd.Key_Create.inSensitive.sensitive.userAuth.size > 0)
            object->misc.key.with_auth = TPM2_YES;
        else
            object->misc.key.with_auth = TPM2_NO;;
        r = ifapi_get_name(&outPublic->publicArea, &object->misc.key.name);
        goto_if_error(r, "Get key name", error_cleanup);

        if (object->misc.key.public.publicArea.type == TPM2_ALG_RSA)
            object->misc.key.signing_scheme = context->cmd.Key_Create.profile->rsa_signing_scheme;
        else
            object->misc.key.signing_scheme = context->cmd.Key_Create.profile->ecc_signing_scheme;
        fallthrough;

    statecase(context->cmd.Key_Create.state, KEY_CREATE_PRIMARY_WAIT_FOR_AUTHORIZE2);
        if (template->persistent_handle) {
            r = ifapi_authorize_object(context, hierarchy, &auth_session);
            FAPI_SYNC(r, "Authorize hierarchy.", error_cleanup);

            /* Prepare making the created primary permanent. */
            r = Esys_EvictControl_Async(context->esys, hierarchy->public.handle,
                                        context->cmd.Key_Create.handle,
                                        auth_session, ESYS_TR_NONE,
                                        ESYS_TR_NONE,
                                        object->misc.key.persistent_handle);
            goto_if_error(r, "Error Esys EvictControl", error_cleanup);
        }
        fallthrough;

    statecase(context->cmd.Key_Create.state, KEY_CREATE_PRIMARY_WAIT_FOR_EVICT_CONTROL);
        if (template->persistent_handle) {
            /* Prepare making the loaded key permanent. */
            r = Esys_EvictControl_Finish(context->esys, &object->public.handle);
            return_try_again(r);
            goto_if_error(r, "Evict control failed", error_cleanup);
        }

        fallthrough;

    statecase(context->cmd.Key_Create.state, KEY_CREATE_PRIMARY_FLUSH);
        /* Flush the primary key. */
        r = ifapi_flush_object(context, context->cmd.Key_Create.handle);
        return_try_again(r);
        goto_if_error(r, "Flush key", error_cleanup);

        fallthrough;

    statecase(context->cmd.Key_Create.state, KEY_CREATE_PRIMARY_WRITE_PREPARE);
        SAFE_FREE(outPublic);

        /* Perform esys serialization */
        r = ifapi_esys_serialize_object(context->esys, object);
        goto_if_error(r, "Prepare serialization", error_cleanup);

        /* Check whether object already exists in key store.*/
        r = ifapi_keystore_object_does_not_exist(&context->keystore,
                                                 context->cmd.Key_Create.keyPath,
                                                 object);
        goto_if_error_reset_state(r, "Could not write: %s", error_cleanup,
                                  context->cmd.Key_Create.keyPath);

        /* Start writing the object to the key store */
        r = ifapi_keystore_store_async(&context->keystore, &context->io,
                                       context->cmd.Key_Create.keyPath, object);
        goto_if_error_reset_state(r, "Could not open: %s", error_cleanup,
                                  context->cmd.Key_Create.keyPath);
        ifapi_cleanup_ifapi_object(object);
        fallthrough;

    statecase(context->cmd.Key_Create.state, KEY_CREATE_PRIMARY_WRITE);
        /* Finish writing the key to the key store */
        r = ifapi_keystore_store_finish(&context->io);
        return_try_again(r);
        return_if_error_reset_state(r, "write_finish failed");

        fallthrough;

    statecase(context->cmd.Key_Create.state, KEY_CREATE_PRIMARY_CLEANUP);
        r = ifapi_cleanup_session(context);
        try_again_or_error_goto(r, "Cleanup", error_cleanup);

        context->cmd.Key_Create.state = KEY_CREATE_INIT;
        break;

    statecasedefault(context->cmd.Key_Create.state);
    }
    free_string_list(context->loadKey.path_list);
    ifapi_cleanup_ifapi_object(hierarchy);
    SAFE_FREE(outPublic);
    SAFE_FREE(creationData);
    SAFE_FREE(creationHash);
    SAFE_FREE(creationTicket);
    SAFE_FREE(context->cmd.Key_Create.policyPath);
    SAFE_FREE(context->cmd.Key_Create.keyPath);
    ifapi_cleanup_ifapi_object(object);
    ifapi_session_clean(context);
    return TSS2_RC_SUCCESS;

 error_cleanup:
    SAFE_FREE(outPublic);
    SAFE_FREE(creationData);
    SAFE_FREE(creationHash);
    SAFE_FREE(creationTicket);
    SAFE_FREE(context->cmd.Key_Create.policyPath);
    SAFE_FREE(context->cmd.Key_Create.keyPath);
    free_string_list(context->loadKey.path_list);
    ifapi_cleanup_ifapi_object(hierarchy);
    return r;

}
