/* SPDX-License-Identifier: BSD-2-Clause */
/*******************************************************************************
 * Copyright 2018-2019, Fraunhofer SIT sponsored by Infineon Technologies AG
 * All rights reserved.
 ******************************************************************************/

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <stdlib.h>
#include <errno.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>

#include "tss2_fapi.h"
#include "fapi_int.h"
#include "fapi_util.h"
#include "tss2_esys.h"
#include "fapi_crypto.h"
#include "fapi_policy.h"
#include "ifapi_json_serialize.h"
#include "ifapi_json_deserialize.h"
#include "tpm_json_deserialize.h"
#define LOGMODULE fapi
#include "util/log.h"
#include "util/aux_util.h"

/** One-Call function for Fapi_ExportKey
 *
 * Given a key it will (if the key is a storage key) duplicate the key and
 * package up the duplicated key and all keys below it into a file ready to move to
 * a new TPM.
 *
 * @param[in,out] context The FAPI_CONTEXT
 * @param[in] pathOfKeyToDuplicate The path to the root of the subtree to
 *            export.
 * @param[in] pathToPublicKeyOfNewParent The path to the public key of the new
 *            parent. May be NULL
 * @param[out] exportedData The exported subtree
 *
 * @retval TSS2_RC_SUCCESS: if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE: if context, pathOfKeyToDuplicate
 *         or exportedData is NULL.
 * @retval TSS2_FAPI_RC_BAD_CONTEXT: if context corruption is detected.
 * @retval TSS2_FAPI_RC_KEY_NOT_FOUND: if pathOfKeyToDuplicate or
 *         pathToPublicKeyOfNewParent does not map to a . FAPI object.
 * @retval TSS2_FAPI_RC_BAD_KEY: if the key at pathToPublicKeyOfNewParent is not
 *         suitable for the requeste operation.
 * @retval TSS2_FAPI_RC_KEY_NOT_DUPLICABLE: if the key is not a duplicable key.
 * @retval TSS2_FAPI_RC_BAD_SEQUENCE: if the context has an asynchronous
 *         operation already pending.
 * @retval TSS2_FAPI_RC_IO_ERROR: if the data cannot be saved.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory for
 *         internal operations or return parameters.
 * @retval TSS2_FAPI_RC_NO_TPM if FAPI was initialized in no-TPM-mode via its
 *         config file.
 * @retval TSS2_FAPI_RC_PATH_NOT_FOUND if a FAPI object path was not found
 *         during authorization.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_BAD_PATH if a path is used in inappropriate context
 *         or contains illegal characters.
 * @retval TSS2_FAPI_RC_TRY_AGAIN if an I/O operation is not finished yet and
 *         this function needs to be called again.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE if an internal error occurred.
 * @retval TSS2_FAPI_RC_AUTHORIZATION_UNKNOWN if a required authorization callback
 *         is not set.
 * @retval TSS2_FAPI_RC_AUTHORIZATION_FAILED if the authorization attempt fails.
 * @retval TSS2_FAPI_RC_POLICY_UNKNOWN if policy search for a certain policy digest
 *         was not successful.
 * @retval TSS2_ESYS_RC_* possible error codes of ESAPI.
 * @retval TSS2_FAPI_RC_NOT_PROVISIONED FAPI was not provisioned.
 */
TSS2_RC
Fapi_ExportKey(
    FAPI_CONTEXT *context,
    char   const *pathOfKeyToDuplicate,
    char   const *pathToPublicKeyOfNewParent,
    char        **exportedData)
{
    LOG_TRACE("called for context:%p", context);

    TSS2_RC r, r2;

    /* Check for NULL parameters */
    check_not_null(context);
    check_not_null(pathOfKeyToDuplicate);
    check_not_null(exportedData);

    /* Check whether TCTI and ESYS are initialized */
    return_if_null(context->esys, "Command can't be executed in none TPM mode.",
                   TSS2_FAPI_RC_NO_TPM);

    /* If the async state automata of FAPI shall be tested, then we must not set
       the timeouts of ESYS to blocking mode.
       During testing, the mssim tcti will ensure multiple re-invocations.
       Usually however the synchronous invocations of FAPI shall instruct ESYS
       to block until a result is available. */
#ifndef TEST_FAPI_ASYNC
    r = Esys_SetTimeout(context->esys, TSS2_TCTI_TIMEOUT_BLOCK);
    return_if_error_reset_state(r, "Set Timeout to blocking");
#endif /* TEST_FAPI_ASYNC */

    r = Fapi_ExportKey_Async(context, pathOfKeyToDuplicate,
                             pathToPublicKeyOfNewParent);
    return_if_error_reset_state(r, "ExportKey");

    do {
        /* We wait for file I/O to be ready if the FAPI state automata
           are in a file I/O state. */
        r = ifapi_io_poll(&context->io);
        return_if_error(r, "Something went wrong with IO polling");

        /* Repeatedly call the finish function, until FAPI has transitioned
           through all execution stages / states of this invocation. */
        r = Fapi_ExportKey_Finish(context, exportedData);
    } while (base_rc(r) == TSS2_BASE_RC_TRY_AGAIN);

    /* Reset the ESYS timeout to non-blocking, immediate response. */
    r2 = Esys_SetTimeout(context->esys, 0);
    return_if_error(r2, "Set Timeout to non-blocking");

    return_if_error_reset_state(r, "ExportKey");

    LOG_TRACE("finished");
    return TSS2_RC_SUCCESS;
}

/** Asynchronous function for Fapi_ExportKey
 *
 * Given a key it will (if the key is a storage key) duplicate the key and
 * package up the duplicated key and all keys below it into a file ready to move to
 * a new TPM.
 *
 * Call Fapi_ExportKey_Finish to finish the execution of this command.
 *
 * @param[in,out] context The FAPI_CONTEXT
 * @param[in] pathOfKeyToDuplicate The path to the root of the subtree to
 *            export.
 * @param[in] pathToPublicKeyOfNewParent The path to the public key of the new
 *            parent
 *
 * @retval TSS2_RC_SUCCESS: if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE: if context or pathOfKeyToDuplicate
 *         is NULL.
 * @retval TSS2_FAPI_RC_BAD_CONTEXT: if context corruption is detected.
 * @retval TSS2_FAPI_RC_KEY_NOT_FOUND: if pathOfKeyToDuplicate or
 *         pathToPublicKeyOfNewParent does not map to a . FAPI object.
 * @retval TSS2_FAPI_RC_BAD_KEY: if the key at pathToPublicKeyOfNewParent is not
 *         suitable for the requeste operation.
 * @retval TSS2_FAPI_RC_KEY_NOT_DUPLICABLE: if the key is not a duplicable key.
 * @retval TSS2_FAPI_RC_BAD_SEQUENCE: if the context has an asynchronous
 *         operation already pending.
 * @retval TSS2_FAPI_RC_IO_ERROR: if the data cannot be saved.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory for
 *         internal operations or return parameters.
 * @retval TSS2_FAPI_RC_NO_TPM if FAPI was initialized in no-TPM-mode via its
 *         config file.
 * @retval TSS2_FAPI_RC_PATH_NOT_FOUND if a FAPI object path was not found
 *         during authorization.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_NOT_PROVISIONED FAPI was not provisioned.
 * @retval TSS2_FAPI_RC_BAD_PATH if the path is used in inappropriate context
 *         or contains illegal characters.
 */
TSS2_RC
Fapi_ExportKey_Async(
    FAPI_CONTEXT *context,
    char   const *pathOfKeyToDuplicate,
    char   const *pathToPublicKeyOfNewParent)
{
    LOG_TRACE("called for context:%p", context);
    LOG_TRACE("pathOfKeyToDuplicate: %s", pathOfKeyToDuplicate);
    LOG_TRACE("pathToPublicKeyOfNewParent: %s", pathToPublicKeyOfNewParent);

    TSS2_RC r;

    /* Check for NULL parameters */
    check_not_null(context);
    check_not_null(pathOfKeyToDuplicate);

    /* Helpful alias pointers */
    IFAPI_ExportKey * command = &context->cmd.ExportKey;

    /* Reset all context-internal session state information. */
    r = ifapi_session_init(context);
    return_if_error(r, "Initialize ExportKey");

    /* Copy parameters to context for use during _Finish. */
    command->pathOfKeyToDuplicate = NULL;
    command->pathToPublicKeyOfNewParent = NULL;
    strdup_check(command->pathOfKeyToDuplicate, pathOfKeyToDuplicate,
                 r, error_cleanup);
    strdup_check(command->pathToPublicKeyOfNewParent,
                 pathToPublicKeyOfNewParent, r, error_cleanup);
    command->exportedData = NULL;

    if (!pathToPublicKeyOfNewParent) {
        /* Only public key of KeyToDuplocate will be exported */
        r = ifapi_keystore_load_async(&context->keystore, &context->io,
                                      pathOfKeyToDuplicate);
        return_if_error2(r, "Could not open: %s", pathOfKeyToDuplicate);

        /* Initialize the context state for this operation. */
        context->state = EXPORT_KEY_READ_PUB_KEY;
    } else {
        /* The public key of the new parent is needed for duplication */
        r = ifapi_keystore_load_async(&context->keystore, &context->io,
                                      pathToPublicKeyOfNewParent);
        return_if_error2(r, "Could not open: %s", pathToPublicKeyOfNewParent);

        /* Initialize the context state for this operation. */
        context->state = EXPORT_KEY_READ_PUB_KEY_PARENT;
    }
    LOG_TRACE("finished");
    return r;

error_cleanup:
    /* Cleanup duplicated input parameters that were copied before. */
    SAFE_FREE(command->pathOfKeyToDuplicate);
    SAFE_FREE(command->pathToPublicKeyOfNewParent);
    return r;
}

/** Asynchronous finish function for Fapi_ExportKey
 *
 * This function should be called after a previous Fapi_ExportKey_Async.
 *
 * @param[in,out] context The FAPI_CONTEXT
 * @param[out] exportedData The exported subtree
 *
 * @retval TSS2_RC_SUCCESS: if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE: if context or exportedData is NULL.
 * @retval TSS2_FAPI_RC_BAD_CONTEXT: if context corruption is detected.
 * @retval TSS2_FAPI_RC_BAD_SEQUENCE: if the context has an asynchronous
 *         operation already pending.
 * @retval TSS2_FAPI_RC_IO_ERROR: if the data cannot be saved.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory for
 *         internal operations or return parameters.
 * @retval TSS2_FAPI_RC_TRY_AGAIN: if the asynchronous operation is not yet
 *         complete. Call this function again later.
 * @retval TSS2_FAPI_RC_BAD_PATH if a path is used in inappropriate context
 *         or contains illegal characters.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE if an internal error occurred.
 * @retval TSS2_FAPI_RC_PATH_NOT_FOUND if a FAPI object path was not found
 *         during authorization.
 * @retval TSS2_FAPI_RC_KEY_NOT_FOUND if a key was not found.
 * @retval TSS2_FAPI_RC_AUTHORIZATION_UNKNOWN if a required authorization callback
 *         is not set.
 * @retval TSS2_FAPI_RC_AUTHORIZATION_FAILED if the authorization attempt fails.
 * @retval TSS2_FAPI_RC_POLICY_UNKNOWN if policy search for a certain policy digest
 *         was not successful.
 * @retval TSS2_FAPI_RC_NO_TPM if FAPI was initialized in no-TPM-mode via its
 *         config file.
 * @retval TSS2_ESYS_RC_* possible error codes of ESAPI.
 * @retval TSS2_FAPI_RC_NOT_PROVISIONED FAPI was not provisioned.
 */
TSS2_RC
Fapi_ExportKey_Finish(
    FAPI_CONTEXT *context,
    char        **exportedData)
{
    LOG_TRACE("called for context:%p", context);

    TSS2_RC r;
    json_object *jsoOut = NULL;
    int sizePem;
    TPM2B_ENCRYPTED_SECRET *encryptedSeed = NULL;
    TPM2B_PRIVATE *duplicate = NULL;
    IFAPI_OBJECT commandObject = {0};
    IFAPI_OBJECT parentKeyObject = {0};
    ESYS_TR auth_session;

    /* Check for NULL parameters */
    check_not_null(context);
    check_not_null(exportedData);

    /* Helpful alias pointers */
    IFAPI_ExportKey * command = &context->cmd.ExportKey;
    IFAPI_OBJECT *pubKey = &command->pub_key;
    IFAPI_OBJECT *exportTree = &command->export_tree;
    IFAPI_DUPLICATE * keyTree = &exportTree->misc.key_tree;
    pubKey->misc.ext_pub_key.certificate = NULL;

    switch (context->state) {
        statecase(context->state, EXPORT_KEY_READ_PUB_KEY);
            /* This is the entry point if only the public key shall be exported
               because no new parent key for encrypting the private portion was
               provided by the caller. */
            r = ifapi_keystore_load_finish(&context->keystore, &context->io,
                                           &commandObject);
            return_try_again(r);
            return_if_error_reset_state(r, "read_finish failed");

            if (commandObject.objectType != IFAPI_KEY_OBJ) {
                /* No key object was loaded */
                ifapi_cleanup_ifapi_object(&commandObject);
                goto_error(r, TSS2_FAPI_RC_BAD_PATH, "%s is not a key object.",
                           cleanup, command->pathOfKeyToDuplicate);
            }

            pubKey->objectType = IFAPI_EXT_PUB_KEY_OBJ;
            pubKey->misc.ext_pub_key.public = commandObject.misc.key.public;

            /* Convert the TPM key format to PEM. */
            r = ifapi_pub_pem_key_from_tpm(&pubKey->misc.ext_pub_key.public,
                                           &pubKey->misc.ext_pub_key.pem_ext_public,
                                           &sizePem);
            goto_if_error(r, "Convert public TPM key to pem.", cleanup);

            r = ifapi_json_IFAPI_OBJECT_serialize(pubKey, &jsoOut);
            goto_if_error(r, "Error serialize FAPI KEY object", cleanup);

            command->exportedData
                = strdup(json_object_to_json_string_ext(jsoOut,
                                                        JSON_C_TO_STRING_PRETTY));
            goto_if_null2(command->exportedData, "Converting json to string", r,
                          TSS2_FAPI_RC_MEMORY, cleanup);

            *exportedData = command->exportedData;
            break;

        statecase(context->state, EXPORT_KEY_READ_PUB_KEY_PARENT);
            /* This is the entry point if a new parent key was provided and
               the private portion shall be re-encrypted. */
            r = ifapi_keystore_load_finish(&context->keystore, &context->io,
                    &parentKeyObject);
            if (r != TSS2_RC_SUCCESS) {
                ifapi_cleanup_ifapi_object(&parentKeyObject);
            }
            return_try_again(r);
            return_if_error_reset_state(r, "read_finish failed");

            if (parentKeyObject.objectType != IFAPI_EXT_PUB_KEY_OBJ) {
                goto_error(r, TSS2_FAPI_RC_BAD_VALUE, "No public key in %s",
                           cleanup, command->pathToPublicKeyOfNewParent);
            }

            /* Store the public information of the new parent in the context
               and cleanup all other metadata for this key. */
            command->public_parent = parentKeyObject.misc.ext_pub_key.public;
            ifapi_cleanup_ifapi_object(&parentKeyObject);

            fallthrough;

        statecase(context->state, EXPORT_KEY_WAIT_FOR_KEY);
            /* Load the key to be duplicated. */
            r = ifapi_load_key(context, command->pathOfKeyToDuplicate,
                               &command->key_object);
            return_try_again(r);
            goto_if_error(r, "Fapi load key.", cleanup);

            context->duplicate_key = command->key_object;

            /* Load the new parent key. */
            r = Esys_LoadExternal_Async(context->esys,
                                        ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE,
                                        NULL,   &command->public_parent,
                                        ESYS_TR_RH_OWNER);
            goto_if_error(r, "LoadExternal_Async", cleanup);

            fallthrough;

        statecase(context->state, EXPORT_KEY_WAIT_FOR_EXT_KEY);
            r = Esys_LoadExternal_Finish(context->esys,
                                         &command->handle_ext_key);
            try_again_or_error_goto(r, "Load external key.", cleanup);

            fallthrough;

        statecase(context->state, EXPORT_KEY_WAIT_FOR_AUTHORIZATON);
            /* Authorize against the key to be exported. */
            r = ifapi_authorize_object(context, command->key_object, &auth_session);
            return_try_again(r);
            goto_if_error(r, "Authorize key.", cleanup);

            TPM2B_DATA encryptionKey;
            TPMT_SYM_DEF_OBJECT symmetric;

            symmetric.algorithm = TPM2_ALG_NULL;
            encryptionKey.size = 0;

            /* Duplicate the key; i.e. re-encrypt the private key with
               the public key of the new parent. */
            r = Esys_Duplicate_Async(context->esys,
                                     command->key_object->public.handle,
                                     command->handle_ext_key,
                                     auth_session,
                                     ESYS_TR_NONE, ESYS_TR_NONE,
                                     &encryptionKey, &symmetric);
            goto_if_error(r, "Duplicate", cleanup);

            fallthrough;

        statecase(context->state, EXPORT_KEY_WAIT_FOR_DUPLICATE);
            exportTree->objectType = IFAPI_DUPLICATE_OBJ;
            r = Esys_Duplicate_Finish(context->esys, NULL, &duplicate, &encryptedSeed);
            try_again_or_error_goto(r, "Duplicate", cleanup);

            /* Store and JSON encode the data to be returned. */
            /* Note: keyTree = &exportTree->misc.key_tree */
            keyTree->encrypted_seed = *encryptedSeed;
            SAFE_FREE(encryptedSeed);
            keyTree->duplicate = *duplicate;
            SAFE_FREE(duplicate);
            keyTree->public =
                command->key_object->misc.key.public;
            keyTree->public_parent = command->public_parent;

            /* For the policy added no cleanup is needed. The cleanup will
               be done with the object cleanup. */
            keyTree->policy = command->key_object->policy;
            r = ifapi_get_json(context, exportTree, &command->exportedData);
            goto_if_error2(r, "get JSON for exported data.", cleanup);

            fallthrough;

        statecase(context->state, EXPORT_KEY_WAIT_FOR_FLUSH1);
            /* Flush the key to be exported from the TPM. */
            r = ifapi_flush_object(context, command->key_object->public.handle);
            return_try_again(r);
            goto_if_error(r, "Flush key", cleanup);

            fallthrough;

        statecase(context->state, EXPORT_KEY_WAIT_FOR_FLUSH2);
            /* Flush the new parent key from the TPM. */
            r = ifapi_flush_object(context, command->handle_ext_key);
            return_try_again(r);
            goto_if_error(r, "Flush key", cleanup);

            fallthrough;

        statecase(context->state, EXPORT_KEY_CLEANUP)
            /* Cleanup the sessions used for authorization. */
            r = ifapi_cleanup_session(context);
            try_again_or_error_goto(r, "Cleanup", cleanup);

            *exportedData = command->exportedData;
            break;

        statecasedefault(context->state);
    }

cleanup:
    /* Cleanup any intermediate results and state stored in the context. */
    if (command->key_object) {
        ifapi_cleanup_ifapi_object(command->key_object);
    }
    if (jsoOut != NULL) {
        json_object_put(jsoOut);
    }
    if (r)
        SAFE_FREE(command->exportedData);
    context->duplicate_key = NULL;
    context->state = _FAPI_STATE_INIT;
    ifapi_cleanup_ifapi_object(&parentKeyObject);
    ifapi_cleanup_ifapi_object(&commandObject);
    ifapi_session_clean(context);
    ifapi_cleanup_ifapi_object(&context->loadKey.auth_object);
    ifapi_cleanup_ifapi_object(context->loadKey.key_object);
    ifapi_cleanup_ifapi_object(&context->createPrimary.pkey_object);
    SAFE_FREE(pubKey->misc.ext_pub_key.pem_ext_public);
    SAFE_FREE(pubKey->misc.ext_pub_key.certificate);
    SAFE_FREE(command->pathOfKeyToDuplicate);
    SAFE_FREE(command->pathToPublicKeyOfNewParent);
    LOG_TRACE("finished");
    return r;
}
