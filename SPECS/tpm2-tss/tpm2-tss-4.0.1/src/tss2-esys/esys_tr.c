/* SPDX-License-Identifier: BSD-2-Clause */
/*******************************************************************************
 * Copyright 2017-2018, Fraunhofer SIT sponsored by Infineon Technologies AG
 * All rights reserved.
 ******************************************************************************/

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include "tss2_esys.h"
#include "esys_mu.h"

#include "esys_iutil.h"
#define LOGMODULE esys
#include "util/log.h"
#include "util/aux_util.h"

/** Serialization of an ESYS_TR into a byte buffer.
 *
 * Serialize the metadata of an ESYS_TR object into a byte buffer such that it
 * can be stored on disk for later use by a different program or context.
 * The serialized object can be deserialized using Esys_TR_Deserialize.
 * @param esys_context [in,out] The ESYS_CONTEXT.
 * @param esys_handle [in] The ESYS_TR object to serialize.
 * @param buffer [out] The buffer containing the serialized metadata.
 *        (caller-callocated) Shall be freed using free().
 * @param buffer_size [out] The size of the buffer parameter.
 * @retval TSS2_RC_SUCCESS on Success.
 * @retval TSS2_ESYS_RC_BAD_TR if the ESYS_TR object is unknown to the
 *         ESYS_CONTEXT.
 * @retval TSS2_ESYS_RC_MEMORY if the buffer for marshaling the object can't
 *         be allocated.
 * @retval TSS2_ESYS_RC_BAD_VALUE For invalid ESYS data to be marshaled.
 * @retval TSS2_RCs produced by lower layers of the software stack.
 */
TSS2_RC
Esys_TR_Serialize(ESYS_CONTEXT * esys_context,
                  ESYS_TR esys_handle, uint8_t ** buffer, size_t * buffer_size)
{
    TSS2_RC r = TSS2_RC_SUCCESS;
    RSRC_NODE_T *esys_object;
    size_t offset = 0;
    *buffer_size = 0;

    r = esys_GetResourceObject(esys_context, esys_handle, &esys_object);
    return_if_error(r, "Get resource object");

    r = iesys_MU_IESYS_RESOURCE_Marshal(&esys_object->rsrc, NULL, SIZE_MAX,
                                        buffer_size);
    return_if_error(r, "Marshal resource object");

    *buffer = malloc(*buffer_size);
    return_if_null(*buffer, "Buffer could not be allocated",
                   TSS2_ESYS_RC_MEMORY);

    r = iesys_MU_IESYS_RESOURCE_Marshal(&esys_object->rsrc, *buffer,
                                        *buffer_size, &offset);
    return_if_error(r, "Marshal resource object");

    return TSS2_RC_SUCCESS;
};

/** Deserialization of an ESYS_TR from a byte buffer.
 *
 * Deserialize the metadata of an ESYS_TR object from a byte buffer that was
 * stored on disk for later use by a different program or context.
 * An object can be deserialized using Esys_TR_Deserialize.
 * @param esys_context [in,out] The ESYS_CONTEXT.
 * @param esys_handle [out] The ESYS_TR object to deserialize.
 * @param buffer [in] The buffer containing the metadata of the ESYS_TR object.
 * @param buffer_size [in] The size of the buffer parameter.
 * @retval TSS2_RC_SUCCESS on Success.
 * @retval TSS2_ESYS_RC_MEMORY if the object can not be allocated.
 * @retval TSS2_ESYS_RC_INSUFFICIENT_BUFFER if the buffer for unmarshalling.
 * @retval TSS2_ESYS_RC_BAD_REFERENCE if the esysContext is NULL.
 * @retval TSS2_RCs produced by lower layers of the software stack.
 */
TSS2_RC
Esys_TR_Deserialize(ESYS_CONTEXT * esys_context,
                    uint8_t const *buffer,
                    size_t buffer_size, ESYS_TR * esys_handle)
{
    TSS2_RC r;

    RSRC_NODE_T *esys_object;
    size_t offset = 0;

    _ESYS_ASSERT_NON_NULL(esys_context);
    *esys_handle = esys_context->esys_handle_cnt++;
    r = esys_CreateResourceObject(esys_context, *esys_handle, &esys_object);
    return_if_error(r, "Get resource object");

    r = iesys_MU_IESYS_RESOURCE_Unmarshal(buffer, buffer_size, &offset,
                                          &esys_object->rsrc);
    return_if_error(r, "Unmarshal resource object");

    return TSS2_RC_SUCCESS;
}

/** Start synchronous creation of an ESYS_TR object from TPM metadata.
 *
 * This function starts the asynchronous retrieval of metadata from the TPM in
 * order to create a new ESYS_TR object.
 * @param esys_context [in,out] The ESYS_CONTEXT
 * @param tpm_handle [in] The handle of the TPM object to represent as ESYS_TR.
 * @param shandle1 [in,out] A session for securing the TPM command (optional).
 * @param shandle2 [in,out] A session for securing the TPM command (optional).
 * @param shandle3 [in,out] A session for securing the TPM command (optional).
 * @retval TSS2_RC_SUCCESS on success
 * @retval ESYS_RC_SUCCESS if the function call was a success.
 * @retval TSS2_ESYS_RC_BAD_REFERENCE if the esysContext is NULL.
 * @retval TSS2_ESYS_RC_BAD_CONTEXT: if esysContext corruption is detected.
 * @retval TSS2_ESYS_RC_MEMORY: if the ESAPI cannot allocate enough memory for
 *         internal operations or return parameters.
 * @retval TSS2_ESYS_RC_MULTIPLE_DECRYPT_SESSIONS: if more than one session has
 *         the 'decrypt' attribute bit set.
 * @retval TSS2_ESYS_RC_MULTIPLE_ENCRYPT_SESSIONS: if more than one session has
 *         the 'encrypt' attribute bit set.
 * @retval TSS2_ESYS_RC_NO_DECRYPT_PARAM: if one of the sessions has the
 *         'decrypt' attribute set and the command does not support encryption
 *         of the first command parameter.
 * @retval TSS2_RCs produced by lower layers of the software stack may be
 *         returned to the caller unaltered unless handled internally.
 */
TSS2_RC
Esys_TR_FromTPMPublic_Async(ESYS_CONTEXT * esys_context,
                            TPM2_HANDLE tpm_handle,
                            ESYS_TR shandle1,
                            ESYS_TR shandle2, ESYS_TR shandle3)
{
    TSS2_RC r;
    _ESYS_ASSERT_NON_NULL(esys_context);
    ESYS_TR esys_handle = esys_context->esys_handle_cnt++;
    RSRC_NODE_T *esysHandleNode = NULL;
    RSRC_NODE_T *node_rsrc = NULL;
    RSRC_NODE_T *next_node_rsrc;

    for (node_rsrc = esys_context->rsrc_list; node_rsrc != NULL;
         node_rsrc = next_node_rsrc) {
         if (node_rsrc->rsrc.handle == tpm_handle) {
             esysHandleNode = node_rsrc;
             esys_context->esys_handle = node_rsrc->esys_handle;
             break;
         }
         next_node_rsrc = node_rsrc->next;
    }

    if (!esysHandleNode) {
        /* Object was already created */
        esys_handle = esys_context->esys_handle_cnt++;
        r = esys_CreateResourceObject(esys_context, esys_handle, &esysHandleNode);
        goto_if_error(r, "Error create resource", error_cleanup);

        /* In the first trial no session will be used to determine the object name. */
        esys_context->sav_session1 = shandle1;
        esys_context->sav_session2 = shandle2;
        esys_context->sav_session3 = shandle3;
        esys_context->session_tab[0] = NULL;
        esys_context->session_tab[1] = NULL;
        esys_context->session_tab[2] = NULL;
        esysHandleNode->rsrc.handle = tpm_handle;
        esys_context->esys_handle = esys_handle;
        shandle1 = ESYS_TR_NONE;
        shandle2 = ESYS_TR_NONE;
        shandle3 = ESYS_TR_NONE;
    } else {
        esys_handle = esysHandleNode->esys_handle;
        esys_context->esys_handle = esys_handle;
    }

    if (tpm_handle >= TPM2_NV_INDEX_FIRST && tpm_handle <= TPM2_NV_INDEX_LAST) {
        r = Esys_NV_ReadPublic_Async(esys_context, esys_handle, shandle1,
                                     shandle2, shandle3);
        goto_if_error(r, "Error NV_ReadPublic", error_cleanup);

    } else if(tpm_handle >> TPM2_HR_SHIFT == TPM2_HT_LOADED_SESSION
            || tpm_handle >> TPM2_HR_SHIFT == TPM2_HT_SAVED_SESSION) {
        // no readpublic call for loaded or saved sessions.
        r = TSS2_RC_SUCCESS;
    } else {
        r = Esys_ReadPublic_Async(esys_context, esys_handle, shandle1, shandle2,
                                  shandle3);
        goto_if_error(r, "Error ReadPublic", error_cleanup);
    }
    return r;
 error_cleanup:
    Esys_TR_Close(esys_context, &esys_handle);
    return r;
}

/** Finish asynchronous creation of an ESYS_TR object from TPM metadata.
 *
 * This function finishes the asynchronous retrieval of metadata from the TPM in
 * order to create a new ESYS_TR object.
 * @param esys_context [in,out] The ESYS_CONTEXT
 * @param object [out] The newly created ESYS_TR metadata object.
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
 *          at least contain the tag, response length, and response code.
 * @retval TSS2_ESYS_RC_MALFORMED_RESPONSE: if the TPM's response is corrupted.
 * @retval TSS2_RCs produced by lower layers of the software stack may be
 *         returned to the caller unaltered unless handled internally.
 */
TSS2_RC
Esys_TR_FromTPMPublic_Finish(ESYS_CONTEXT * esys_context, ESYS_TR * object)
{
    TSS2_RC r = TSS2_RC_SUCCESS;
    ESYS_TR objectHandle = ESYS_TR_NONE;
    RSRC_NODE_T *objectHandleNode;
    bool first_call;

    _ESYS_ASSERT_NON_NULL(esys_context);

    objectHandle = esys_context->esys_handle;

    r = esys_GetResourceObject(esys_context, objectHandle, &objectHandleNode);
    goto_if_error(r, "get resource", error_cleanup);

    /* Check whether the object was already initialized. */
    first_call = !objectHandleNode->rsrc.rsrcType;

    if (objectHandleNode->rsrc.handle >= TPM2_NV_INDEX_FIRST
        && objectHandleNode->rsrc.handle <= TPM2_NV_INDEX_LAST) {
        TPM2B_NV_PUBLIC *nvPublic;
        TPM2B_NAME *nvName;
        r = Esys_NV_ReadPublic_Finish(esys_context, &nvPublic, &nvName);
        if (base_rc(r) == TSS2_BASE_RC_TRY_AGAIN) {
            LOG_DEBUG("A layer below returned TRY_AGAIN: %" PRIx32
                      " => resubmitting command", r);
            return r;
        }
        goto_if_error(r, "Error NV_ReadPublic", error_cleanup);

        bool is_nvname_mismatch = false;
        if (first_call) {
            objectHandleNode->rsrc.rsrcType = IESYSC_NV_RSRC;
            objectHandleNode->rsrc.name = *nvName;
            objectHandleNode->rsrc.misc.rsrc_nv_pub = *nvPublic;
        } else {
            if (objectHandleNode->rsrc.name.size != nvName->size ||
                memcmp(&objectHandleNode->rsrc.name.name[0], &nvName->name[0], nvName->size) != 0) {
                is_nvname_mismatch = true;
            }
        }
        SAFE_FREE(nvPublic);
        SAFE_FREE(nvName);
        if (is_nvname_mismatch) {
            goto_error(r, TSS2_ESYS_RC_GENERAL_FAILURE,
                "Name mismatch between two calls of Esys_TR_FromTPMPublic",
                error_cleanup);
        }
    }
    else if(objectHandleNode->rsrc.handle >> TPM2_HR_SHIFT == TPM2_HT_LOADED_SESSION
       || objectHandleNode->rsrc.handle >> TPM2_HR_SHIFT == TPM2_HT_SAVED_SESSION) {
        objectHandleNode->rsrc.rsrcType = IESYSC_DEGRADED_SESSION_RSRC;
    } else {
        TPM2B_PUBLIC *public;
        TPM2B_NAME *name = NULL;
        TPM2B_NAME *qualifiedName = NULL;
        r = Esys_ReadPublic_Finish(esys_context, &public, &name,
                                   &qualifiedName);
        if (base_rc(r) == TSS2_BASE_RC_TRY_AGAIN) {
            LOG_DEBUG("A layer below returned TRY_AGAIN: %" PRIx32
                      " => resubmitting command", r);
            return r;
        }
        goto_if_error(r, "Error ReadPublic", error_cleanup);

        if (first_call) {
            objectHandleNode->rsrc.rsrcType = IESYSC_KEY_RSRC;
            objectHandleNode->rsrc.name = *name;
            objectHandleNode->rsrc.misc.rsrc_key_pub = *public;
        } else {
            if (objectHandleNode->rsrc.name.size != name->size ||
                memcmp(&objectHandleNode->rsrc.name.name[0], &name->name[0], name->size) != 0) {
                goto_error(r, TSS2_ESYS_RC_GENERAL_FAILURE,
                           "Name mismatch between two calls of Esys_TR_FromTPMPublic",
                           error_cleanup);
            }
        }
        SAFE_FREE(public);
        SAFE_FREE(name);
        SAFE_FREE(qualifiedName);
    }

    if (esys_context->sav_session1 != ESYS_TR_NONE && first_call) {
        /* Initialize second call if session is used */
        r = init_session_tab(esys_context, esys_context->sav_session1,
                            esys_context->sav_session2, esys_context->sav_session3);
        return_if_error(r, "Initialize session resources");

        iesys_compute_session_value(esys_context->session_tab[0],
                                    &objectHandleNode->rsrc.name, NULL);
        iesys_compute_session_value(esys_context->session_tab[1], NULL, NULL);
        iesys_compute_session_value(esys_context->session_tab[2], NULL, NULL);
        r = Esys_TR_FromTPMPublic_Async(esys_context, objectHandleNode->rsrc.handle,
                                        esys_context->session_tab[0]->esys_handle,
                                        esys_context->session_tab[1] ?
                                        esys_context->session_tab[1]->esys_handle : ESYS_TR_NONE,
                                        esys_context->session_tab[2] ?
                                        esys_context->session_tab[2]->esys_handle : ESYS_TR_NONE);
        return_if_error(r, "Error TR FromTPMPublic");
        return TSS2_ESYS_RC_TRY_AGAIN;
    } else {
        *object = objectHandle;
        return TSS2_RC_SUCCESS;
    }

 error_cleanup:
    Esys_TR_Close(esys_context, &objectHandle);
    return r;
}

/** Creation of an ESYS_TR object from TPM metadata.
 *
 * This function can be used to create ESYS_TR object for Tpm Resources that are
 * not created or loaded (e.g. using ESys_CreatePrimary or ESys_Load) but
 * pre-exist inside the TPM. Examples are NV-Indices or persistent object.
 *
 * Note: For PCRs and hierarchies, please use the global ESYS_TR identifiers.
 * Note: If a session is provided the TPM is queried for the metadata twice.
 * First without a session to retrieve some metadata then with the session where
 * this metadata is used in the session HMAC calculation and thereby verified.
 *
 * Since man in the middle attacks should be prevented as much as possible it is
 * recommended to pass a session.
 * @param esys_context [in,out] The ESYS_CONTEXT
 * @param tpm_handle [in] The handle of the TPM object to represent as ESYS_TR.
 * @param shandle1 [in,out] A session for securing the TPM command (optional).
 * @param shandle2 [in,out] A session for securing the TPM command (optional).
 * @param shandle3 [in,out] A session for securing the TPM command (optional).
 * @param object [out] The newly created ESYS_TR metadata object.
 * @retval TSS2_RC_SUCCESS on success
 * @retval ESYS_RC_SUCCESS if the function call was a success.
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
 * @retval TSS2_ESYS_RC_MULTIPLE_DECRYPT_SESSIONS: if more than one session has
 *         the 'decrypt' attribute bit set.
 * @retval TSS2_ESYS_RC_MULTIPLE_ENCRYPT_SESSIONS: if more than one session has
 *         the 'encrypt' attribute bit set.
 * @retval TSS2_ESYS_RC_NO_DECRYPT_PARAM: if one of the sessions has the
 *         'decrypt' attribute set and the command does not support encryption
 *         of the first command parameter.
 * @retval TSS2_RCs produced by lower layers of the software stack may be
 *         returned to the caller unaltered unless handled internally.
 */
TSS2_RC
Esys_TR_FromTPMPublic(ESYS_CONTEXT * esys_context,
                      TPM2_HANDLE tpm_handle,
                      ESYS_TR shandle1,
                      ESYS_TR shandle2, ESYS_TR shandle3, ESYS_TR * object)
{
    TSS2_RC r;

    _ESYS_ASSERT_NON_NULL(esys_context);
    r = Esys_TR_FromTPMPublic_Async(esys_context, tpm_handle,
                                    shandle1, shandle2, shandle3);
    return_if_error(r, "Error TR FromTPMPublic");

    /* Set the timeout to indefinite for now, since we want _Finish to block */
    int32_t timeouttmp = esys_context->timeout;
    esys_context->timeout = -1;
    /*
     * Now we call the finish function, until return code is not equal to
     * from TSS2_BASE_RC_TRY_AGAIN.
     * Note that the finish function may return TSS2_RC_TRY_AGAIN, even if we
     * have set the timeout to -1. This occurs for example if the TPM requests
     * a retransmission of the command via TPM2_RC_YIELDED.
     */
    do {
        r = Esys_TR_FromTPMPublic_Finish(esys_context, object);
        if (base_rc(r) == TSS2_BASE_RC_TRY_AGAIN)
            LOG_DEBUG("A layer below returned TRY_AGAIN: %" PRIx32
                      " => resubmitting command", r);
    } while (base_rc(r) == TSS2_BASE_RC_TRY_AGAIN);

    /* Restore the timeout value to the original value */
    esys_context->timeout = timeouttmp;
    return_if_error(r, "Error TR FromTPMPublic");

    return r;
}

/** Close an ESYS_TR without removing it from the TPM.
 *
 * This function deletes an ESYS_TR object from an ESYS_CONTEXT without deleting
 * it from the TPM. This is useful for NV-Indices or persistent keys, after
 * Esys_TR_Serialize has been called. Transient objects should be deleted using
 * Esys_FlushContext.
 * @param esys_context [in,out] The ESYS_CONTEXT
 * @param object [out] ESYS_TR metadata object to be deleted from ESYS_CONTEXT.
 * @retval TSS2_RC_SUCCESS on Success.
 * @retval TSS2_ESYS_RC_BAD_REFERENCE if the esysContext is NULL.
 * @retval TSS2_ESYS_RC_BAD_TR if the ESYS_TR object is unknown to the
 *         ESYS_CONTEXT.
 */
TSS2_RC
Esys_TR_Close(ESYS_CONTEXT * esys_context, ESYS_TR * object)
{
    RSRC_NODE_T *node;
    RSRC_NODE_T **update_ptr;

    _ESYS_ASSERT_NON_NULL(esys_context);
    for (node = esys_context->rsrc_list,
         update_ptr = &esys_context->rsrc_list;
         node != NULL;
         update_ptr = &node->next, node = node->next) {
        if (node->esys_handle == *object) {
            *update_ptr = node->next;
            SAFE_FREE(node);
            *object = ESYS_TR_NONE;
            return TSS2_RC_SUCCESS;
        }
    }
    LOG_ERROR("Error: Esys handle does not exist (%x).", TSS2_ESYS_RC_BAD_TR);
    return TSS2_ESYS_RC_BAD_TR;
}

/** Set the authorization value of an ESYS_TR.
 *
 * Authorization values are associated with ESYS_TR Tpm Resource object. They
 * are then picked up whenever an authorization is needed.
 *
 * Note: The authorization value is not stored in the metadata during
 * Esys_TR_Serialize. Therefor Esys_TR_SetAuth needs to be called again after
 * every Esys_TR_Deserialize.
 * @param esys_context [in,out] The ESYS_CONTEXT.
 * @param esys_handle [in,out] The ESYS_TR for which to set the auth value.
 * @param authValue [in] The auth value to set for the ESYS_TR or NULL to zero
 *        the auth.
 * @retval TSS2_RC_SUCCESS on Success.
 * @retval TSS2_ESYS_RC_BAD_REFERENCE if the esysContext is NULL.
 * @retval TSS2_ESYS_RC_BAD_TR if the ESYS_TR object is unknown to the
 *         ESYS_CONTEXT or it equals ESYS_TR_NONE.
 */
TSS2_RC
Esys_TR_SetAuth(ESYS_CONTEXT * esys_context, ESYS_TR esys_handle,
                TPM2B_AUTH const *authValue)
{
    RSRC_NODE_T *esys_object;
    TSS2_RC r;
    TPMI_ALG_HASH name_alg = TPM2_ALG_NULL;

    _ESYS_ASSERT_NON_NULL(esys_context);
    if (esys_handle == ESYS_TR_NONE) {
      return_error(TSS2_ESYS_RC_BAD_TR, "esys_handle can't be ESYS_TR_NONE.");
    }
    r = esys_GetResourceObject(esys_context, esys_handle, &esys_object);
    if (r != TPM2_RC_SUCCESS)
        return r;

    if (authValue == NULL) {
        esys_object->auth.size = 0;
    } else {
        if (authValue->size > sizeof(TPMU_HA)) {
            return_error(TSS2_ESYS_RC_BAD_SIZE, "Bad size for auth value.");
        }
        /* Determine name alg of resource */
        if (esys_object->rsrc.rsrcType == IESYSC_KEY_RSRC) {
            name_alg = esys_object->rsrc.misc.rsrc_key_pub.publicArea.nameAlg;
        } else if (esys_object->rsrc.rsrcType == IESYSC_NV_RSRC) {
            name_alg = esys_object->rsrc.misc.rsrc_nv_pub.nvPublic.nameAlg;
        }
        esys_object->auth = *authValue;
        /* Adapt auth value to hash for large auth values. */
        if (name_alg != TPM2_ALG_NULL) {
            r = iesys_hash_long_auth_values(&esys_context->crypto_backend,
                    &esys_object->auth, name_alg);
            return_if_error(r, "Hashing overlength authValue failed.");
        }
    }
    return TSS2_RC_SUCCESS;
}

/** Retrieve the TPM public name of an Esys_TR object.
 *
 * Some operations (i.e. Esys_PolicyNameHash) require the name of a TPM object
 * to be passed. Esys_TR_GetName provides this name to the caller.
 * @param esys_context [in,out] The ESYS_CONTEXT.
 * @param esys_handle [in,out] The ESYS_TR for which to retrieve the name.
 * @param name [out] The name of the object (caller-allocated; use free()).
 * @retval TSS2_RC_SUCCESS on Success.
 * @retval TSS2_ESYS_RC_MEMORY if needed memory can't be allocated.
 * @retval TSS2_ESYS_RC_GENERAL_FAILURE for errors of the crypto library.
 * @retval TSS2_ESYS_RC_BAD_REFERENCE if the esysContext is NULL.
 * @retval TSS2_ESYS_RC_BAD_TR if the handle is invalid.
 * @retval TSS2_SYS_RC_* for SAPI errors.
 */
TSS2_RC
Esys_TR_GetName(ESYS_CONTEXT * esys_context, ESYS_TR esys_handle,
                TPM2B_NAME ** name)
{
    RSRC_NODE_T *esys_object;
    TSS2_RC r;
    _ESYS_ASSERT_NON_NULL(esys_context);

    if (esys_handle == ESYS_TR_NONE) {
        return_error(TSS2_ESYS_RC_BAD_TR, "Name for ESYS_TR_NONE can't be determined.");
    }

    r = esys_GetResourceObject(esys_context, esys_handle, &esys_object);
    return_if_error(r, "Object not found");

    *name = malloc(sizeof(TPM2B_NAME));
    if (*name == NULL) {
        LOG_ERROR("Error: out of memory");
        return TSS2_ESYS_RC_MEMORY;
    }
    if (esys_object->rsrc.rsrcType == IESYSC_KEY_RSRC) {
        r = iesys_get_name(&esys_context->crypto_backend,
                &esys_object->rsrc.misc.rsrc_key_pub, *name);
        goto_if_error(r, "Error get name", error_cleanup);

    } else {
        if (esys_object->rsrc.rsrcType == IESYSC_NV_RSRC) {
            r = iesys_nv_get_name(&esys_context->crypto_backend,
                    &esys_object->rsrc.misc.rsrc_nv_pub, *name);
            goto_if_error(r, "Error get name", error_cleanup);

        } else {
            size_t offset = 0;
            r = Tss2_MU_TPM2_HANDLE_Marshal(esys_object->rsrc.handle,
                                            &(*name)->name[0], sizeof(TPM2_HANDLE),
                                            &offset);
            goto_if_error(r, "Error get name", error_cleanup);
            (*name)->size = offset;
        }
    }
    return r;
 error_cleanup:
    SAFE_FREE(*name);
    return r;
}


/** Retrieve the Session Attributes of the ESYS_TR session.
 *
 * Sessions possess attributes, such as whether they shall continue of be
 * flushed after the next command, or whether they are used to encrypt
 * parameters.
 * Note: this function only applies to ESYS_TR objects that represent sessions.
 * @param esys_context [in,out] The ESYS_CONTEXT.
 * @param esys_handle [in,out] The ESYS_TR of the session.
 * @param flags [out] The attributes of the session.
 * @retval TSS2_ESYS_RC_BAD_REFERENCE if the esysContext is NULL.
 * @retval TSS2_ESYS_RC_BAD_TR if the ESYS_TR object is unknown to the
 *         ESYS_CONTEXT or ESYS_TR object is not a session object.
 */
TSS2_RC
Esys_TRSess_GetAttributes(ESYS_CONTEXT * esys_context, ESYS_TR esys_handle,
                          TPMA_SESSION * flags)
{
    RSRC_NODE_T *esys_object;

    _ESYS_ASSERT_NON_NULL(esys_context);
    TSS2_RC r = esys_GetResourceObject(esys_context, esys_handle, &esys_object);
    return_if_error(r, "Object not found");

    if (esys_object->rsrc.rsrcType != IESYSC_SESSION_RSRC)
        return_error(TSS2_ESYS_RC_BAD_TR, "Object is not a session object");
    *flags = esys_object->rsrc.misc.rsrc_session.sessionAttributes;
    return TSS2_RC_SUCCESS;
}

/** Set session attributes
 *
 * Set or unset a session's attributes according to the provided flags and mask.
 * @verbatim new_attributes = old_attributes & ~mask | flags & mask @endverbatim
 * Note: this function only applies to ESYS_TR objects that represent sessions.
 * @param esys_context [in,out] The ESYS_CONTEXT.
 * @param esys_handle [in,out] The ESYS_TR of the session.
 * @param flags [in] The flags to be set or unset for the session.
 * @param mask [in] The mask for the flags to be set or unset.
 * @retval TSS2_RC_SUCCESS on Success.
 * @retval TSS2_ESYS_RC_BAD_REFERENCE if the esysContext is NULL.
 * @retval TSS2_ESYS_RC_BAD_TR if the ESYS_TR object is unknown to the
 *         ESYS_CONTEXT or ESYS_TR object is not a session object.
 */
TSS2_RC
Esys_TRSess_SetAttributes(ESYS_CONTEXT * esys_context, ESYS_TR esys_handle,
                          TPMA_SESSION flags, TPMA_SESSION mask)
{
    RSRC_NODE_T *esys_object;

    _ESYS_ASSERT_NON_NULL(esys_context);
    TSS2_RC r = esys_GetResourceObject(esys_context, esys_handle, &esys_object);
    return_if_error(r, "Object not found");

    return_if_null(esys_object, "Object not found", TSS2_ESYS_RC_BAD_VALUE);

    if (esys_object->rsrc.rsrcType != IESYSC_SESSION_RSRC)
        return_error(TSS2_ESYS_RC_BAD_TR, "Object is not a session object");
    esys_object->rsrc.misc.rsrc_session.sessionAttributes =
        (esys_object->rsrc.misc.rsrc_session.
         sessionAttributes & ~mask) | (flags & mask);
    if (esys_object->rsrc.misc.rsrc_session.sessionAttributes & TPMA_SESSION_AUDIT)
        esys_object->rsrc.misc.rsrc_session.bound_entity.size = 0;
    return TSS2_RC_SUCCESS;
}

/** Retrieve the TPM nonce of an Esys_TR session object.
 *
 * Some operations (i.e. Esys_PolicySigned) require the nonce returned by the
 * TPM during Esys_StartauthSession. This function provides this nonce to the
 * caller.
 * @param esys_context [in,out] The ESYS_CONTEXT.
 * @param esys_handle [in,out] The ESYS_TRsess for which to retrieve the nonce.
 * @param nonceTPM [out] The nonce of the object (callee-allocated; use free()).
 * @retval TSS2_RC_SUCCESS on Success.
 * @retval TSS2_ESYS_RC_MEMORY if needed memory can't be allocated.
 * @retval TSS2_ESYS_RC_GENERAL_FAILURE for errors of the crypto library.
 * @retval TSS2_ESYS_RC_BAD_REFERENCE if the esysContext is NULL.
 * @retval TSS2_SYS_RC_* for SAPI errors.
 */
TSS2_RC
Esys_TRSess_GetNonceTPM(ESYS_CONTEXT * esys_context, ESYS_TR esys_handle,
                TPM2B_NONCE **nonceTPM)
{
    RSRC_NODE_T *esys_object;
    TSS2_RC r;
    _ESYS_ASSERT_NON_NULL(esys_context);
    _ESYS_ASSERT_NON_NULL(nonceTPM);

    r = esys_GetResourceObject(esys_context, esys_handle, &esys_object);
    return_if_error(r, "Object not found");

    *nonceTPM = calloc(1, sizeof(**nonceTPM));
    if (*nonceTPM == NULL) {
        LOG_ERROR("Error: out of memory");
        return TSS2_ESYS_RC_MEMORY;
    }
    if (esys_object->rsrc.rsrcType != IESYSC_SESSION_RSRC) {
        goto_error(r, TSS2_ESYS_RC_BAD_TR,
                   "NonceTPM for non-session object requested.",
                   error_cleanup);

    }
    **nonceTPM = esys_object->rsrc.misc.rsrc_session.nonceTPM;

    return r;
 error_cleanup:
    SAFE_FREE(*nonceTPM);
    return r;
}

/** Retrieves the associated TPM2_HANDLE from an ESYS_TR object.
 *
 * Retrieves the TPM2_HANDLE for an associated ESYS_TR object for use with the
 * SAPI API or comparisons against raw TPM2_HANDLES from commands like
 * TPM2_GetCapability or use of various handle bitwise comparisons. For example
 * the mask TPM2_HR_NV_INDEX.
 *
 * @param esys_context [in,out] The ESYS_CONTEXT.
 * @param esys_handle [in] The ESYS_TR object to retrieve the TPM2_HANDLE from.
 * @param tpm_handle [out] The TPM2_HANDLE retrieved from the ESYS_TR object.
 * @retval TSS2_RC_SUCCESS on Success.
 * @retval TSS2_ESYS_RC_BAD_TR if the ESYS_TR object is unknown to the
 *         ESYS_CONTEXT or is ESYS_TR_NONE.
 * @retval TSS2_ESYS_RC_BAD_VALUE if an unknown handle < ESYS_TR_MIN_OBJECT is
 *         passed.
 * @retval TSS2_ESYS_RC_BAD_REFERENCE For invalid ESYS_CONTEXT.
 */
TSS2_RC
Esys_TR_GetTpmHandle(ESYS_CONTEXT * esys_context, ESYS_TR esys_handle,
                  TPM2_HANDLE * tpm_handle)
{
    TSS2_RC r = TSS2_RC_SUCCESS;
    RSRC_NODE_T *esys_object;

    _ESYS_ASSERT_NON_NULL(esys_context);
    _ESYS_ASSERT_NON_NULL(tpm_handle);

    if (esys_handle == ESYS_TR_NONE) {
        return TSS2_ESYS_RC_BAD_TR;
    }

    r = esys_GetResourceObject(esys_context, esys_handle, &esys_object);
    return_if_error(r, "Get resource object");

    *tpm_handle = esys_object->rsrc.handle;

    return TSS2_RC_SUCCESS;
};

/** Retrieve whether auth value is required from a Esys_TR session object.
 *
 * This function can be used to determin whether PoliyPassword or
 * PlolicyAuthValue are used for a session.
 * @param esys_context [in,out] The ESYS_CONTEXT.
 * @param esys_handle [in,out] The ESYS_TRsess for which to retrieve the nonce.
 * @param neeed [out] The boolean indicating whether auth value will be
 *                    needed.
 * @retval TSS2_RC_SUCCESS on Success.
 * @retval TSS2_ESYS_RC_GENERAL_FAILURE for errors of the crypto library.
 * @retval TSS2_ESYS_RC_BAD_REFERENCE if the esysContext is NULL.
 * @retval TSS2_SYS_RC_* for SAPI errors.
 */
TSS2_RC
Esys_TRSess_GetAuthRequired(ESYS_CONTEXT * esys_context, ESYS_TR esys_handle,
                            TPMI_YES_NO *auth_needed)
{
    RSRC_NODE_T *esys_object;
    TSS2_RC r;
    _ESYS_ASSERT_NON_NULL(esys_context);

    r = esys_GetResourceObject(esys_context, esys_handle, &esys_object);
    return_if_error(r, "Object not found");

    if (esys_object->rsrc.rsrcType != IESYSC_SESSION_RSRC) {
        return_if_error(TSS2_ESYS_RC_BAD_TR,
                        "Auth value needed for non-session object requested.");
    }

    if (esys_object->rsrc.misc.rsrc_session.type_policy_session == POLICY_AUTH ||
        esys_object->rsrc.misc.rsrc_session.type_policy_session == POLICY_PASSWORD)
        *auth_needed = TPM2_YES;
    else
        *auth_needed = TPM2_NO;
    return TSS2_RC_SUCCESS;

}
