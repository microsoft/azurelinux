/* SPDX-License-Identifier: BSD-2-Clause */
/*******************************************************************************
 * Copyright 2018-2019, Fraunhofer SIT sponsored by Infineon Technologies AG
 * All rights reserved.
 ******************************************************************************/

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <errno.h>

#include "tss2_fapi.h"
#include "fapi_int.h"
#include "fapi_util.h"
#include "tss2_esys.h"
#include "ifapi_json_serialize.h"
#include "ifapi_json_deserialize.h"
#define LOGMODULE fapi
#include "util/log.h"
#include "util/aux_util.h"

/** Move a certain path to the beginning of a path array.
 *
 * A certain path starting with the profile passed will be moved.
 *
 * The pass will only be moved if current profile of the FAPI context
 * is the first element of the path in the file list.
 *
 * @param[in] path The part of the path without profile to be moved.
 * @param[in] profile_name The profile_name must be the first part of
 *            the path to be moved.
 * @param[in,out] file_ary The path array.
 * @param[in] n The size of the array.
 */
static void
move_path_to_top(
    const char* path,
    const char* profile_name,
    char **file_ary,
    size_t n)
{
    size_t i, pos, size_path, size_file;
    char* current_file;
    size_t shift_pos = 0;
    size_t prof_size = strlen(profile_name);

    for (i = 1; i < n; i++) {
        size_path = strlen(path);
        size_file = strlen(file_ary[i]);
        if (size_path < size_file) {
            /* Compare last part of the array item with path. */
            pos = size_file - size_path;
            current_file = file_ary[i];
            if (strncmp(profile_name, &current_file[1], prof_size) == 0 &&
                current_file[prof_size + 1] == IFAPI_FILE_DELIM_CHAR &&
                strncmp(&current_file[pos], path, size_path) == 0) {
                shift_pos = i;
                break;
            }
        }
    }
    /* Path was found behind the first item of the array. */
    if (shift_pos) {
        for (i = shift_pos; i > 0; i--)
            file_ary[i] = file_ary[i - 1];
        file_ary[0] = current_file;
    }
}

/** Search a path for a certain profile in the path list.
 *
 * @param[in] profile_name The profile_name must be the first part of
 *            the path to be moved.
 * @param[in] path The part of the path without profile to be moved.
 * @param[in,out] file_ary The path array.
 * @param[in] n The size of the array.
 * @retval true if the path was found.
 * @retval false if the path was not found.
 */
static bool
find_path_for_profile(
    char *profile_name,
    char *path,
    char **file_ary,
    size_t n)
{
    size_t size_profile = strlen(profile_name);
    size_t pos_path = size_profile + 1;
    size_t i;
    char *current_path;

    for (i = 0; i < n; i++) {
        current_path = file_ary[i];
        if (strncmp(profile_name, &current_path[1], size_profile) == 0 &&
            strcmp(path, &current_path[pos_path]) == 0)
            return true;
    }
    return false;
}

/** Check whether a hierarchy remains in keystore after deleting the SRK.
 *
 * @param[in] context The FAPI context.
 * @param[in] profile_name Profile of the SRK.
 * @param[in] hierarchy The hierarchy in the passed profile to be checked.
 * @param[in,out] file_ary The path array.
 * @param[in] n The size of the array.
 * @retval TSS2_RC_SUCCESS: if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_PATH: if path can't be used for deleting.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory for
 *         internal operations or return parameters.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_PATH_NOT_FOUND if a FAPI object path was not found
 *         during authorization.
 */
static TSS2_RC
check_hierarchy(
    FAPI_CONTEXT *context,
    char *profile_name,
    char *hierarchy,
    char **file_ary,
    size_t n)
{
    TSS2_RC r = TSS2_RC_SUCCESS;
    size_t i, n_all;
    char** file_all_ary;

    if (find_path_for_profile(profile_name, hierarchy,
                              file_ary, n)) {
        /* HE hierarchy will also be deleted. */
        return TSS2_RC_SUCCESS;
    }

    r = ifapi_keystore_list_all(&context->keystore, profile_name, &file_all_ary, &n_all);
    goto_if_error(r, "get entities.", cleanup);

    if (find_path_for_profile(profile_name, hierarchy, file_all_ary, n_all)) {
        /* Hierarchy would remain in keystore. */
        goto_error(r, TSS2_FAPI_RC_BAD_PATH,
                   "Cannot delete /HS/SRK because %s would remain in keystore",
                   cleanup, hierarchy);
    }

 cleanup:
    for (i = 0; i < n_all; i++)
        free(file_all_ary[i]);
    SAFE_FREE(file_all_ary);
    return r;
}

/** Check whether deletion is possible and normalize the file list.
 *
 * The file list will be reordered to assure that the SRK used as TPM key
 * for a session will be deleted last.
 * It will be checked whether there are remaining object for a certain profile
 * after deleting a  SRK of the list.
 *
 * @param[in,out] context The FAPI context.
 * @param[in,out] file_ary The path array.
 * @param[in] n The size of the array.
 * @retval TSS2_RC_SUCCESS: if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_PATH: if path can't be used for deleting.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory for
 *         internal operations or return parameters.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE if an internal error occurred.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_PATH_NOT_FOUND if a FAPI object path was not found
 *         during authorization.
 */
static TSS2_RC
normalize_and_check_path_list(
    FAPI_CONTEXT *context,
    char **file_ary,
    size_t n)
{
    TSS2_RC r;
    char *profile_name = NULL;
    char *current_file, *slash;

    /* Move SRK and HS to the top of list. The objects will be deleted in
       reverse order thus these objects are deleted last.
       The SRK can still be used as tpm key for session. */
    move_path_to_top(IFAPI_SRK_KEY_PATH, context->config.profile_name,
                     file_ary, n);
    move_path_to_top(IFAPI_HS_PATH, context->config.profile_name,
                     file_ary, n);
    if (find_path_for_profile(context->config.profile_name, IFAPI_SRK_KEY_PATH,
                             file_ary, n)) {
        /* The HS has to be delteed with SRK checked */
        if (!find_path_for_profile(context->config.profile_name, IFAPI_HS_PATH,
                                  file_ary, n))
            return_error(TSS2_FAPI_RC_BAD_PATH,
                         "SRK has to be deleted together with HS");

        r = check_hierarchy(context, context->config.profile_name, IFAPI_HE_PATH,
                            file_ary, n);
        return_if_error(r, "Check hierarchy" IFAPI_HE_PATH);

        r = check_hierarchy(context, context->config.profile_name, IFAPI_HN_PATH,
                            file_ary, n);
        return_if_error(r, "Check hierarchy" IFAPI_HN_PATH);

        r = check_hierarchy(context, context->config.profile_name, IFAPI_LOCKOUT_PATH,
                            file_ary, n);
        return_if_error(r, "Check hiearchy" IFAPI_LOCKOUT_PATH);

        return TSS2_RC_SUCCESS;
    } else {
        /* Check whether another SRK is in the list. */
        current_file = file_ary[0];
        if (strncmp(&current_file[1], "P_", 2) == 0) {
            size_t prof_size;
            slash = strchr(&current_file[1], IFAPI_FILE_DELIM_CHAR);

            /* Determine profile name. */
            if (slash)
                prof_size = (size_t)(slash - current_file) - 1;
            else
                /* This case should not occur. */
                return_error2(TSS2_FAPI_RC_GENERAL_FAILURE,
                              "Invalid object path to be deleted.");

            profile_name = malloc(prof_size + 1);
            return_if_null(profile_name, "FAPI out of memory.",
                           TSS2_FAPI_RC_MEMORY);
            memcpy(&profile_name[0], &current_file[1], prof_size);
            profile_name[prof_size] = '\0';

            /* Search SRK in the list. */
            if (!find_path_for_profile(profile_name, IFAPI_SRK_KEY_PATH, file_ary, n)) {
                /* No SRK found, no further check needed. */
                SAFE_FREE(profile_name);
                return TSS2_RC_SUCCESS;
            }
            r = check_hierarchy(context, profile_name, IFAPI_HE_PATH,
                                file_ary, n);
            goto_if_error2(r, "Check hierarchy: %s", error_cleanup, IFAPI_HE_PATH);

            r = check_hierarchy(context, profile_name, IFAPI_LOCKOUT_PATH,
                                file_ary, n);
            goto_if_error2(r, "Check hiearchy: %s", error_cleanup, IFAPI_HE_PATH);

            SAFE_FREE(profile_name);
            return TSS2_RC_SUCCESS;
        } else {
            /* No profile used in path. */
            return TSS2_RC_SUCCESS;
        }
    }
 error_cleanup:
    SAFE_FREE(profile_name);
    return r;
}

/** One-Call function for Fapi_Delete
 *
 * Deletes a given key, policy or NV index from the system.
 *
 * @param[in,out] context The ESAPI_CONTEXT
 * @param[in] path The path to the entity that is to be deleted
 *
 * @retval TSS2_RC_SUCCESS: if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE: if context or path is NULL.
 * @retval TSS2_FAPI_RC_BAD_CONTEXT: if context corruption is detected.
 * @retval TSS2_FAPI_RC_BAD_PATH: if path cannot be deleted.
 * @retval TSS2_FAPI_RC_NOT_DELETABLE: if the entity is not deletable or the
 *         path is read-only.
 * @retval TSS2_FAPI_RC_BAD_SEQUENCE: if the context has an asynchronous
 *         operation already pending.
 * @retval TSS2_FAPI_RC_IO_ERROR: if the data cannot be saved.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory for
 *         internal operations or return parameters.
 * @retval TSS2_FAPI_RC_NO_TPM if FAPI was initialized in no-TPM-mode via its
 *         config file.
 * @retval TSS2_FAPI_RC_PATH_NOT_FOUND if a FAPI object path was not found
 *         during authorization.
 * @retval TSS2_FAPI_RC_KEY_NOT_FOUND if a key was not found.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
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
Fapi_Delete(
    FAPI_CONTEXT   *context,
    char     const *path)
{
    LOG_TRACE("called for context:%p", context);

    TSS2_RC r;

    /* Check for NULL parameters */
    check_not_null(context);
    check_not_null(path);

    r = Fapi_Delete_Async(context, path);
    return_if_error_reset_state(r, "Entity_Delete");

    do {
        /* We wait for file I/O to be ready if the FAPI state automata
           are in a file I/O state. */
        r = ifapi_io_poll(&context->io);
        return_if_error(r, "Something went wrong with IO polling");

        /* Repeatedly call the finish function, until FAPI has transitioned
           through all execution stages / states of this invocation. */
        r = Fapi_Delete_Finish(context);
    } while (base_rc(r) == TSS2_BASE_RC_TRY_AGAIN);

    return_if_error_reset_state(r, "Entity_Delete");

    return TSS2_RC_SUCCESS;
}

/** Asynchronous function for Fapi_Delete
 *
 * Deletes a given key, policy or NV index from the system.

 * Call Fapi_Delete_Finish to finish the execution of this command.
 *
 * @param[in,out] context The ESAPI_CONTEXT
 * @param[in] path The path to the entity that is to be deleted
 *
 * @retval TSS2_RC_SUCCESS: if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE: if context or path is NULL.
 * @retval TSS2_FAPI_RC_BAD_CONTEXT: if context corruption is detected.
 * @retval TSS2_FAPI_RC_BAD_PATH: if path does not map to a FAPI entity.
 * @retval TSS2_FAPI_RC_NOT_DELETABLE: if the entity is not deletable or the
 *         path is read-only.
 * @retval TSS2_FAPI_RC_BAD_SEQUENCE: if the context has an asynchronous
 *         operation already pending.
 * @retval TSS2_FAPI_RC_IO_ERROR: if the data cannot be saved.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory for
 *         internal operations or return parameters.
 * @retval TSS2_FAPI_RC_NO_TPM if FAPI was initialized in no-TPM-mode via its
 *         config file.
 * @retval TSS2_FAPI_RC_PATH_NOT_FOUND if a FAPI object path was not found
 *         during authorization.
 * @retval TSS2_FAPI_RC_KEY_NOT_FOUND if a key was not found.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_ESYS_RC_* possible error codes of ESAPI.
 * @retval TSS2_FAPI_RC_NOT_PROVISIONED FAPI was not provisioned.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE if an internal error occurred.
 */
TSS2_RC
Fapi_Delete_Async(
    FAPI_CONTEXT   *context,
    char     const *path)
{
    LOG_TRACE("called for context:%p", context);
    LOG_TRACE("path: %s", path);

    TSS2_RC r;
    size_t i;

    /* Check for NULL parameters */
    check_not_null(context);
    check_not_null(path);

    /* Helpful alias pointers */
    IFAPI_Entity_Delete * command = &(context->cmd.Entity_Delete);
    IFAPI_OBJECT *object = &command->object;
    IFAPI_OBJECT *authObject = &command->auth_object;

    command->pathlist = NULL;
    context->session1 = ESYS_TR_NONE;

    /* Copy parameters to context for use during _Finish. */
    strdup_check(command->path, path, r, error_cleanup);

    /* List all keystore elements in the path hierarchy of the provided
       path. The last of these is the object to be deleted. */
    r = ifapi_keystore_list_all(&context->keystore, path, &command->pathlist,
                                &command->numPaths);
    goto_if_error(r, "get entities.", error_cleanup);

    /* Check whether a path for exactly one policy was passed. */
    if (command->numPaths == 0 && ifapi_path_type_p(path, IFAPI_POLICY_PATH)) {
        command->numPaths = 1;
        command->pathlist = calloc(1, sizeof(char *));
        strdup_check(command->pathlist[0], path, r, error_cleanup);
    }

    command->path_idx = command->numPaths;

    if (command->numPaths == 0) {
        if (strcmp(path, "") == 0 || strcmp(path, "/") == 0) {
            goto_error(r, TSS2_FAPI_RC_NOT_PROVISIONED, "FAPI not provisioned.", error_cleanup);
        } else {
            goto_error(r, TSS2_FAPI_RC_BAD_PATH, "No objects(s) found", error_cleanup);
        }
    }

    r = normalize_and_check_path_list(context,command->pathlist, command->numPaths);
    goto_if_error_reset_state(r, "Check whether delete is possible.", error_cleanup);

    object->objectType = IFAPI_OBJ_NONE;
    authObject->objectType = IFAPI_OBJ_NONE;

    if (ifapi_path_type_p(path, IFAPI_EXT_PATH) ||
        (ifapi_path_type_p(path, IFAPI_POLICY_PATH))) {
        /* No session will be needed these files can be deleted without
           interaction with the TPM */
        r = ifapi_non_tpm_mode_init(context);
        goto_if_error(r, "Initialize Entity_Delete", error_cleanup);
        context->session1 = ESYS_TR_NONE;

        context->state = ENTITY_DELETE_GET_FILE;
    } else {
        /* Check whether TCTI and ESYS are initialized */
        goto_if_null(context->esys, "Command can't be executed in none TPM mode.",
                       TSS2_FAPI_RC_NO_TPM, error_cleanup);

        /* If the async state automata of FAPI shall be tested, then we must not set
           the timeouts of ESYS to blocking mode.
           During testing, the mssim tcti will ensure multiple re-invocations.
           Usually however the synchronous invocations of FAPI shall instruct ESYS
           to block until a result is available. */
#ifndef TEST_FAPI_ASYNC
        r = Esys_SetTimeout(context->esys, TSS2_TCTI_TIMEOUT_BLOCK);
        goto_if_error_reset_state(r, "Set Timeout to blocking", error_cleanup);
#endif /* TEST_FAPI_ASYNC */

        /* A TPM session will be created to enable object authorization */
        r = ifapi_session_init(context);
        goto_if_error(r, "Initialize Entity_Delete", error_cleanup);

        r = ifapi_get_sessions_async(context,
                                 IFAPI_SESSION_GENEK | IFAPI_SESSION1,
                                 0, 0);
        goto_if_error_reset_state(r, "Create sessions", error_cleanup);

        context->state = ENTITY_DELETE_WAIT_FOR_SESSION;
    }

    LOG_TRACE("finished");
    return TSS2_RC_SUCCESS;

error_cleanup:
    /* Cleanup any intermediate results and state stored in the context. */
    if (command->pathlist)
        for (i = 0; i < command->numPaths; i++)
            SAFE_FREE(command->pathlist[i]);
    SAFE_FREE(command->pathlist);
    SAFE_FREE(command->path);
    if (context->session1 != ESYS_TR_NONE &&
        Esys_FlushContext(context->esys, context->session1) != TSS2_RC_SUCCESS) {
        LOG_ERROR("Cleanup session failed.");
    }
    return r;
}

/** Asynchronous finish function for Fapi_Delete
 *
 * This function should be called after a previous Fapi_Delete_Async.
 *
 * @param[in,out] context The FAPI_CONTEXT
 *
 * @retval TSS2_RC_SUCCESS: if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE: if context is NULL.
 * @retval TSS2_FAPI_RC_BAD_CONTEXT: if context corruption is detected.
 * @retval TSS2_FAPI_RC_BAD_SEQUENCE: if the context has an asynchronous
 *         operation already pending.
 * @retval TSS2_FAPI_RC_IO_ERROR: if the data cannot be saved.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory for
 *         internal operations or return parameters.
 * @retval TSS2_FAPI_RC_TRY_AGAIN: if the asynchronous operation is not yet
 *         complete. Call this function again later.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE if an internal error occurred.
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
 * @retval TSS2_ESYS_RC_* possible error codes of ESAPI.
 * @retval TSS2_FAPI_RC_NOT_PROVISIONED FAPI was not provisioned.
 * @retval TSS2_FAPI_RC_BAD_PATH if the path is used in inappropriate context
 *         or contains illegal characters.
 */
TSS2_RC
Fapi_Delete_Finish(
    FAPI_CONTEXT   *context)
{
    LOG_TRACE("called for context:%p", context);

    TSS2_RC r;
    ESYS_TR auth_session;
    char *path;

    /* Check for NULL parameters */
    check_not_null(context);

    /* Helpful alias pointers */
    IFAPI_Entity_Delete * command = &(context->cmd.Entity_Delete);
    IFAPI_OBJECT *object = &command->object;
    IFAPI_OBJECT *authObject = &command->auth_object;

    switch (context->state) {
        statecase(context->state, ENTITY_DELETE_WAIT_FOR_SESSION);
            /* If a TPM object (e.g. a persistent key) was referenced, then this
               is the entry point. */
            r = ifapi_get_sessions_finish(context, &context->profiles.default_profile,
                                      context->profiles.default_profile.nameAlg);
            return_try_again(r);
            goto_if_error(r, "Create FAPI session.", error_cleanup);

            fallthrough;

        statecase(context->state, ENTITY_DELETE_GET_FILE);
            /* If a non-TPM object (e.g. a policy) was referenced, then this is the
               entry point. */
            /* Use last path in the path list */
            command->path_idx -= 1;
            path = command->pathlist[command->path_idx];
            LOG_TRACE("Delete object: %s %zu", path, command->path_idx);

            if (ifapi_path_type_p(path, IFAPI_EXT_PATH)) {
                /* External keyfile can be deleted directly without TPM operations. */
                context->state = ENTITY_DELETE_FILE;
                return TSS2_FAPI_RC_TRY_AGAIN;
            }

            if (ifapi_path_type_p(path, IFAPI_POLICY_PATH)) {
                /* Policy file can be deleted directly without TPM operations. */
                context->state = ENTITY_DELETE_POLICY;
                return TSS2_FAPI_RC_TRY_AGAIN;
            }

            /* Load the object metadata from the keystore. */
            r = ifapi_keystore_load_async(&context->keystore, &context->io, path);
            return_if_error2(r, "Could not open: %s", path);

            fallthrough;

        statecase(context->state, ENTITY_DELETE_READ);
            /* We only end up in this path, if the referenced object requires
               TPM operations; e.g. persistent key or NV index. */
            r = ifapi_keystore_load_finish(&context->keystore, &context->io, object);
            return_try_again(r);
            return_if_error_reset_state(r, "read_finish failed");

            /* Initialize the ESYS object for the persistent key or NV Index. */
            r = ifapi_initialize_object(context->esys, object);
            goto_if_error_reset_state(r, "Initialize NV object", error_cleanup);

            if (object->objectType == IFAPI_KEY_OBJ) {
                /* If the object is a key, we jump over to ENTITY_DELETE_KEY. */
                command->is_key = true;
                context->state = ENTITY_DELETE_KEY;
                return TSS2_FAPI_RC_TRY_AGAIN;

            } else  if (object->objectType == IFAPI_NV_OBJ) {
                /* Prepare for the deletion of an NV index. */
                /* Prepare for the deletion of an NV index. */
                command->is_key = false;

                /* Check whether hierarchy file has been read. */
                if (authObject->objectType == IFAPI_OBJ_NONE) {
                    r = ifapi_keystore_load_async(&context->keystore, &context->io, "/HS");
                    return_if_error2(r, "Could not open hierarchy /HS");

                    command->auth_index = ESYS_TR_RH_OWNER;
                } else {
                    context->state = ENTITY_DELETE_AUTHORIZE_NV;
                    return TSS2_FAPI_RC_TRY_AGAIN;
                }
            } else {
                context->state = ENTITY_DELETE_FILE;
                return TSS2_FAPI_RC_TRY_AGAIN;
            }
            fallthrough;

        statecase(context->state, ENTITY_DELETE_READ_HIERARCHY);
            if (authObject->objectType == IFAPI_OBJ_NONE) {
                r = ifapi_keystore_load_finish(&context->keystore, &context->io, authObject);
                try_again_or_error(r, "read_finish failed");

                r = ifapi_initialize_object(context->esys, authObject);
                goto_if_error_reset_state(r, "Initialize hierarchy object", error_cleanup);
                authObject->public.handle = ESYS_TR_RH_OWNER;
            }
            fallthrough;

        statecase(context->state, ENTITY_DELETE_AUTHORIZE_NV);
            /* Authorize with the storage hierarchy / "owner" to delete the NV index. */
            r = ifapi_authorize_object(context, authObject, &auth_session);
            return_try_again(r);
            goto_if_error(r, "Authorize NV object.", error_cleanup);

            /* Delete the NV index. */
            r = Esys_NV_UndefineSpace_Async(context->esys,
                                            command->auth_index,
                                            object->public.handle,
                                            auth_session,
                                            ESYS_TR_NONE,
                                            ESYS_TR_NONE);
            goto_if_error_reset_state(r, " Fapi_NV_UndefineSpace_Async", error_cleanup);

            context->state = ENTITY_DELETE_NULL_AUTH_SENT_FOR_NV;
            return TSS2_FAPI_RC_TRY_AGAIN;

        statecase(context->state, ENTITY_DELETE_KEY);
            if (object->misc.key.persistent_handle) {
                r = ifapi_keystore_load_async(&context->keystore, &context->io, "/HS");
                return_if_error2(r, "Could not open hierarchy /HS");
            }
            fallthrough;

        statecase(context->state, ENTITY_DELETE_KEY_WAIT_FOR_HIERARCHY);
            if (object->misc.key.persistent_handle) {
                r = ifapi_keystore_load_finish(&context->keystore, &context->io, authObject);
                return_try_again(r);
                return_if_error(r, "read_finish failed");

                r = ifapi_initialize_object(context->esys, authObject);
                goto_if_error_reset_state(r, "Initialize hierarchy object", error_cleanup);

                authObject->public.handle = ESYS_TR_RH_OWNER;
            }
            fallthrough;

        statecase(context->state, ENTITY_DELETE_KEY_WAIT_FOR_AUTHORIZATION);
            /* Delete persistent object if not prohibited. */
            if (object->misc.key.persistent_handle) {
                if (object->misc.key.delete_prohibited) {
                    LOG_ERROR("Failed to delete TPM key (%s) because it was not "
                              "created by the tss Feature API",
                              command->pathlist[command->path_idx]);
                    context->state = ENTITY_DELETE_FILE;
                    return TSS2_FAPI_RC_TRY_AGAIN;
                } else {
                    r = ifapi_authorize_object(context, authObject, &auth_session);
                    FAPI_SYNC(r, "Authorize hierarchy.", error_cleanup);

                    /* Delete the persistent handle from the TPM. */
                    r = Esys_EvictControl_Async(context->esys, ESYS_TR_RH_OWNER,
                                                object->public.handle,
                                                auth_session,
                                                ESYS_TR_NONE, ESYS_TR_NONE,
                                            object->misc.key.persistent_handle);
                    goto_if_error(r, "Evict Control", error_cleanup);
                    context->state = ENTITY_DELETE_NULL_AUTH_SENT_FOR_KEY;
                }
            } else {
                context->state = ENTITY_DELETE_FILE;
                return TSS2_FAPI_RC_TRY_AGAIN;
            }
            fallthrough;

        statecase(context->state, ENTITY_DELETE_AUTH_SENT_FOR_KEY);
            fallthrough;
        statecase(context->state, ENTITY_DELETE_NULL_AUTH_SENT_FOR_KEY);
            r = Esys_EvictControl_Finish(context->esys,
                                         &command->new_object_handle);
            return_try_again(r);

            goto_if_error_reset_state(r, "FAPI Entity_Delete", error_cleanup);

            context->state = ENTITY_DELETE_FILE;
            return TSS2_FAPI_RC_TRY_AGAIN;
            break;

        statecase(context->state, ENTITY_DELETE_AUTH_SENT_FOR_NV);
            fallthrough;
        statecase(context->state, ENTITY_DELETE_NULL_AUTH_SENT_FOR_NV);
            r = Esys_NV_UndefineSpace_Finish(context->esys);
            return_try_again(r);

            goto_if_error_reset_state(r, "FAPI NV_UndefineSpace", error_cleanup);

            LOG_TRACE("NV Object undefined.");
            context->state = ENTITY_DELETE_FILE;
            return TSS2_FAPI_RC_TRY_AGAIN;
            break;

        statecase(context->state, ENTITY_DELETE_POLICY);
            /* This is the simple case of deleting a policy from the keystore. */
            path = command->pathlist[command->path_idx];
            LOG_TRACE("Delete: %s", path);

            r = ifapi_policy_delete(&context->pstore, path);
            goto_if_error_reset_state(r, "Could not delete: %s", error_cleanup, path);

            if (command->path_idx > 0)
                context->state = ENTITY_DELETE_GET_FILE;
            else
                context->state = ENTITY_DELETE_REMOVE_DIRS;
            return TSS2_FAPI_RC_TRY_AGAIN;

        statecase(context->state, ENTITY_DELETE_FILE);
            /* This is the simple case of deleting an external (pub)key from the keystore
               or we enter here after the TPM operation for the persistent key or NV index
               deletion have been performed. */
            path = command->pathlist[command->path_idx];
            ifapi_cleanup_ifapi_object(object);
            ifapi_cleanup_ifapi_object(authObject);

            /* Delete all the object's data from the keystore. */
            r = ifapi_keystore_delete(&context->keystore, path);
            goto_if_error_reset_state(r, "Could not delete: %s", error_cleanup, path);

            if (command->path_idx > 0) {
                context->state = ENTITY_DELETE_GET_FILE;
                return TSS2_FAPI_RC_TRY_AGAIN;
            }

            fallthrough;

        statecase(context->state, ENTITY_DELETE_REMOVE_DIRS);
            /* For some cases, we need to remove the directory that contained the
               meta data as well. */
            r = ifapi_keystore_remove_directories(&context->keystore, command->path);
            goto_if_error(r, "Error while removing directories", error_cleanup);

            fallthrough;

        statecase(context->state, ENTITY_DELETE_CLEANUP);
            /* Cleanup the session. */
            r = ifapi_cleanup_session(context);
            try_again_or_error_goto(r, "Cleanup", error_cleanup);

            context->state = _FAPI_STATE_INIT;

            LOG_DEBUG("success");
            r = TSS2_RC_SUCCESS;
            break;

        statecasedefault(context->state);
    }

    /* Reset the ESYS timeout to non-blocking, immediate response. */
    if (context->esys) {
        r = Esys_SetTimeout(context->esys, 0);
        goto_if_error(r, "Set Timeout to non-blocking", error_cleanup);
    }

    /* Cleanup intermediate state stored in the context. */
    SAFE_FREE(command->path);
    ifapi_cleanup_ifapi_object(authObject);
    ifapi_cleanup_ifapi_object(object);
    for (size_t i = 0; i < command->numPaths; i++) {
        SAFE_FREE(command->pathlist[i]);
    }
    SAFE_FREE(command->pathlist);
    ifapi_session_clean(context);
    ifapi_cleanup_ifapi_object(&context->loadKey.auth_object);
    ifapi_cleanup_ifapi_object(context->loadKey.key_object);
    ifapi_cleanup_ifapi_object(&context->createPrimary.pkey_object);

    LOG_TRACE("finished");
    return r;

error_cleanup:
    /* Cleanup any intermediate results and state stored in the context. */
    Esys_SetTimeout(context->esys, 0);
    ifapi_cleanup_ifapi_object(object);
    SAFE_FREE(command->path);
    if (command->pathlist) {
        for (size_t i = 0; i < command->numPaths; i++) {
            SAFE_FREE(command->pathlist[i]);
        }
    }
    SAFE_FREE(command->pathlist);
    ifapi_session_clean(context);
    ifapi_cleanup_ifapi_object(&context->createPrimary.pkey_object);
    return r;
}
