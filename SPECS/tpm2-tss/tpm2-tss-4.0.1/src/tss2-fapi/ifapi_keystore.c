/* SPDX-License-Identifier: BSD-2-Clause */
/*******************************************************************************
 * Copyright 2018-2019, Fraunhofer SIT sponsored by Infineon Technologies AG
 * All rights reserved.
 *******************************************************************************/

#ifdef HAVE_CONFIG_H
#include <config.h>
#include <dirent.h>
#include <ctype.h>
#endif

#include "ifapi_io.h"
#include "ifapi_helpers.h"
#include "ifapi_keystore.h"
#define LOGMODULE fapi
#include "util/log.h"
#include "util/aux_util.h"
#include "tpm_json_deserialize.h"
#include "ifapi_json_deserialize.h"
#include "ifapi_json_serialize.h"


/** Check whether pathname is valid.
 *
 * Every key pathname will be checked whether the name contains only
 * valid character.
 * @param[in] path The pathname.
 * @retval TSS2_RC_SUCCESS If the pathname is ok.
 * @retval TSS2_FAPI_RC_BAD_PATH If not valid characters are detected.
 */
TSS2_RC
ifapi_check_valid_path(
    const char *path)
{
    for (size_t i = 0; i < strlen(path); i++) {
        if (!(isalnum(path[i]) ||
              path[i] == '_' ||
              path[i] == '-' ||
              path[i] == '/')) {
            LOG_ERROR("Invalid character %c in path %s", path[i], path);
            return TSS2_FAPI_RC_BAD_PATH;
        }
    }
    return TSS2_RC_SUCCESS;
}

/** Initialize the linked list for an explicit key path.
 *
 * An implicit key path will be expanded to a key path starting with the profile
 * directory. Missing parts will be added if possible.
 * A linked list of the directories of the explicit path will be returned.
 *
 * @param[in] context_profile  The profile name used for expansion of the
 *            implicit key path.
 * @param[in] ipath the implicit key path which has to be expanded.
 * @param[out] list_node1 The first directory of the implicit list.
 * @param[out] current_list_node The tail of the path list after the path
 *             which was expanded.
 * @param[out] result The list of directories as linked list.
 * @retval TSS2_RC_SUCCESS If the explicit path was created.
 * @retval TSS2_FAPI_RC_MEMORY: If memory for the path list could not be allocated.
 * @retval TSS2_FAPI_RC_BAD_VALUE If no explicit path can be derived from the
 *         implicit path.
 * @retval TSS2_FAPI_RC_BAD_PATH if no valid key path could be created.
 */
static TSS2_RC
initialize_explicit_key_path(
    const char *context_profile,
    const char *ipath,
    NODE_STR_T **list_node1,
    NODE_STR_T **current_list_node,
    NODE_STR_T **result)
{
    *list_node1 = split_string(ipath, IFAPI_FILE_DELIM);
    NODE_STR_T *list_node = *list_node1;
    char const *profile;
    char *hierarchy = NULL;
    TSS2_RC r = TSS2_RC_SUCCESS;

    *result = NULL;
    if (list_node == NULL) {
        LOG_ERROR("Invalid path");
        free_string_list(*list_node1);
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    /* Check whether profile is part of the implicit path. */
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
    if (strcmp(list_node->str, "HN") == 0 ||
        strcmp(list_node->str, "HS") == 0 ||
        strcmp(list_node->str, "HE") == 0 ||
        strcmp(list_node->str, "HN") == 0) {
        hierarchy = list_node->str;
        list_node = list_node->next;
    } else if (strcmp(list_node->str, "LOCKOUT") == 0) {
        if (list_node->next) {
            LOG_ERROR("No objects allowed in the lockout hierarchy.");
            r = TSS2_FAPI_RC_BAD_VALUE;
            goto error;
        }
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
    /* Add the used hierarchy to the linked list. */
    if (hierarchy && !add_string_to_list(*result, hierarchy)) {
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

    if (hierarchy && strcmp(hierarchy, "HS") == 0 && strcmp(list_node->str, "EK") == 0) {
        LOG_ERROR("Key EK cannot be created in the storage hierarchy.");
        r = TSS2_FAPI_RC_BAD_PATH;
        goto error;
    }

    if (hierarchy && strcmp(hierarchy, "HE") == 0 && strcmp(list_node->str, "SRK") == 0) {
        LOG_ERROR("Key EK cannot be create in the endorsement hierarchy.");
        r = TSS2_FAPI_RC_BAD_PATH;
        goto error;
    }

    if (hierarchy && strcmp(hierarchy, "HN") == 0 &&
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

/** Get explicit key path as linked list.
 *
 * An implicit key path will be expanded to a key path starting with the profile
 * directory. Missing parts will be added if possible.
 * A linked list of the directories of the explicit path will be returned.
 * @param[in] keystore The key directories and default profile.
 * @param[in] ipath the implicit key path which has to be expanded.
 * @param[out] result The list of directories as linked list.
 * @retval TSS2_RC_SUCCESS If the explicit path was created.
 * @retval TSS2_FAPI_RC_MEMORY: If memory for the path list could not be allocated.
 * @retval TSS2_FAPI_RC_BAD_VALUE If no explicit path can be derived from the
 *         implicit path.
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
    TSS2_RC r = initialize_explicit_key_path(keystore->defaultprofile, ipath,
                                             &list_node1, &list_node, result);
    goto_if_error(r, "init_explicit_key_path", error);

    while (list_node != NULL) {
        /* Add tail of path list to expanded head of the path list. */
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

/** Convert full FAPI path to relative path.
 *
 * The relative path will be copied directly into the passed object.
 *
 * @param[in] keystore The key directories and default profile.
 * @param[in,out] path The absolute path.
 */
void
full_path_to_fapi_path(IFAPI_KEYSTORE *keystore, char *path)
{
    unsigned int start_pos, end_pos, i;
    const unsigned int path_length = strlen(path);
    size_t keystore_length = strlen(keystore->userdir);
    char fapi_path_delim;

    start_pos = 0;

    /* Check type of path, user or system */
    if (strncmp(&path[0], keystore->userdir, keystore_length) == 0) {
        start_pos = strlen(keystore->userdir);
    } else {
        keystore_length = strlen(keystore->systemdir);
        if (strncmp(&path[0], keystore->systemdir, keystore_length) == 0)
            start_pos = strlen(keystore->systemdir);
    }

    if (!start_pos)
        /* relative path was passed */
        return;

    /* Move relative path */
    end_pos = path_length - start_pos;
    memmove(&path[0], &path[start_pos], end_pos);
    size_t ip = 0;
    size_t lp = strlen(path);

    /* Remove double / */
    while (ip < lp) {
        if (strncmp(&path[ip], "//", 2) == 0) {
            memmove(&path[ip], &path[ip+1], lp-ip);
            lp -= 1;
        } else {
            ip += 1;
        }
    }

    /* A relative policy path will end before the file extension.
       For other objects only the directory name will be uses as
       relative name. */
    if (ifapi_path_type_p(path, IFAPI_POLICY_PATH))
        fapi_path_delim = '.';
    else
        fapi_path_delim = IFAPI_FILE_DELIM_CHAR;

    for (i = end_pos - 2; i > 0; i--) {
        if (path[i] == fapi_path_delim) {
            path[i] = '\0';
            break;
        }
    }
}

/** Expand key store path.
 *
 * Depending on the type of the passed path the path will be expanded. For hierarchies
 * the profile directory  will be added. For keys the implicit path will
 * be expanded to an explicit path with all directories.
 * @param[in] keystore The key directories and default profile.
 * @param[in] path the implicit  path which has to be expanded if possible.
 * @param[out] file_name The explicit path (callee-allocated)
 * @retval TSS2_RC_SUCCESS If the explicit path was created.
 * @retval TSS2_FAPI_RC_MEMORY: If memory for the path list could not be allocated.
 * @retval TSS2_FAPI_RC_BAD_VALUE If no explicit path can be derived from the
 *         implicit path.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_BAD_PATH if the path is used in inappropriate context
 *         or contains illegal characters.
 * @retval TSS2_FAPI_RC_PATH_NOT_FOUND if a FAPI object path was not found
 *         during authorization.
 */
static TSS2_RC
expand_path(IFAPI_KEYSTORE *keystore, const char *path, char **file_name)
{
    TSS2_RC r;
    NODE_STR_T *node_list = NULL;
    size_t pos = 0;
    *file_name = NULL;

    check_not_null(path);

    /* First it will be checked whether the only valid characters occur in the path. */
    r = ifapi_check_valid_path(path);
    return_if_error(r, "Invalid path.");

    if (ifapi_hierarchy_path_p(path)) {
        if (strncmp(path, "P_", 2) == 0 || strncmp(path, "/P_", 3) == 0) {
            *file_name = strdup(path);
            return_if_null(*file_name, "Out of memory", TSS2_FAPI_RC_MEMORY);
        } else {
            if (strncmp("/", path, 1) == 0)
                pos = 1;
            r = ifapi_asprintf(file_name, "/%s%s%s", keystore->defaultprofile,
                               IFAPI_FILE_DELIM, &path[pos]);
            return_if_error(r, "Out of memory.");
        }
    } else if (ifapi_path_type_p(path, IFAPI_NV_PATH)
               || ifapi_path_type_p(path, IFAPI_POLICY_PATH)
               || ifapi_path_type_p(path, IFAPI_EXT_PATH)
               || strncmp(path, "/P_", 3) == 0 || strncmp(path, "P_", 2) == 0) {
        *file_name = strdup(path);
        return_if_null(*file_name, "Out of memory", TSS2_FAPI_RC_MEMORY);

    } else {
        r = get_explicit_key_path(keystore, path, &node_list);
        return_if_error(r, "Explicit key path cannot be determined.");

        r = ifapi_path_string(file_name, NULL, node_list, NULL);
        goto_if_error(r, "Out of memory", error);

        free_string_list(node_list);
    }

    /* Normalize the pathname. '/' at the beginning no '/' at the end. */
    if (strncmp(&(*file_name)[strlen(*file_name) - 1], "/", 1) == 0)
        (*file_name)[strlen(*file_name) - 1] = '\0';
    if (strncmp(&(*file_name)[0], "/", 1) != 0) {
        char *aux_str = NULL;
        aux_str = malloc(strlen(*file_name) + 2);
        goto_if_null(aux_str, "Out of memory", TSS2_FAPI_RC_MEMORY, error);

        aux_str[0] = '/';
        memcpy(&aux_str[1], &(*file_name)[0], strlen(*file_name)+1);
        SAFE_FREE(*file_name);
        *file_name = aux_str;
    }

    return TSS2_RC_SUCCESS;

error:
    SAFE_FREE(*file_name);
    free_string_list(node_list);
    return r;
}
/** Expand FAPI path to object path.
 *
 * The object file name will be appended and the implicit path will be expanded
 * if possible.
 * FAPI object path names correspond to directories of the key store. The
 * objects are stored in a certain file in this directory. This function
 * appends the name of the object file  to the FAPI directory to prepare file IO.
 * @retval TSS2_RC_SUCCESS If the object file path can be created.
 * @retval TSS2_FAPI_RC_MEMORY: If memory for the path name cannot allocated.
 * @retval TSS2_FAPI_RC_BAD_VALUE If no explicit path can be derived from the
 *         implicit path.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_BAD_PATH if the path is used in inappropriate context
 *         or contains illegal characters.
 * @retval TSS2_FAPI_RC_PATH_NOT_FOUND if a FAPI object path was not found
 *         during authorization.
 */
static TSS2_RC
expand_path_to_object(
    IFAPI_KEYSTORE *keystore,
    const char *path,
    const char *dir,
    char **file_name)
{

    TSS2_RC r;
    char *expanded_path = NULL;

    /* Expand implicit path to explicit path. */
    r = expand_path(keystore, path, &expanded_path);
    return_if_error(r, "Expand path");

    /* Append object file. */
    r = ifapi_asprintf(file_name, "%s/%s/%s", dir, expanded_path, IFAPI_OBJECT_FILE);
    SAFE_FREE(expanded_path);
    return r;
}

/** Store keystore parameters in the keystore context.
 *
 * Also the user directory will be created if it does not exist.
 *
 * @param[out] keystore The keystore to be initialized.
 * @param[in] config_systemdir The configured system directory.
 * @param[in] config_userdir The configured user directory.
 * @param[in] config_defaultprofile The configured profile.
 *
 * @retval TSS2_RC_SUCCESS If the keystore can be initialized.
 * @retval TSS2_FAPI_RC_IO_ERROR If the user part of the keystore can't be
 *         initialized.
 * @retval TSS2_FAPI_RC_MEMORY: if memory could not be allocated.
 * @retval TSS2_FAPI_RC_BAD_PATH if the home directory of the user
 *         cannot be determined.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 */
TSS2_RC
ifapi_keystore_initialize(
    IFAPI_KEYSTORE *keystore,
    const char *config_systemdir,
    const char *config_userdir,
    const char *config_defaultprofile)
{
    TSS2_RC r;

    memset(keystore, 0, sizeof(IFAPI_KEYSTORE));

    /* Create user directory if necessary */
    r = ifapi_io_check_create_dir(config_userdir, FAPI_WRITE);
    goto_if_error2(r, "User directory %s can't be created.", error, keystore->userdir);

    keystore->userdir = strdup(config_userdir);
    goto_if_null2(keystore->userdir, "Out of memory.", r, TSS2_FAPI_RC_MEMORY,
                  error);

    keystore->systemdir = strdup(config_systemdir);
    goto_if_null2(keystore->systemdir, "Out of memory.", r, TSS2_FAPI_RC_MEMORY,
                  error);

    keystore->defaultprofile = strdup(config_defaultprofile);
    goto_if_null2(keystore->defaultprofile, "Out of memory.", r, TSS2_FAPI_RC_MEMORY,
                  error);

    return TSS2_RC_SUCCESS;

error:
    SAFE_FREE(keystore->defaultprofile);
    SAFE_FREE(keystore->userdir);
    SAFE_FREE(keystore->systemdir);
    return r;
}

/** Get absolute object path for FAPI relative path and check whether file exists.
 *
 *  It will be checked whether object exists in user directory, if no
 *  the path in system directory will be returnde
 *
 * @param[in] keystore The key directories and default profile.
 * @param[in] rel_path The relative path of the object. For keys the path will
 *           expanded if possible.
 * @param[out] abs_path The absolute path of the object.
 * @retval TSS2_RC_SUCCESS If the object can be read.
 * @retval TSS2_FAPI_RC_KEY_NOT_FOUND if the file does not exist (for key objects).
 * @retval TSS2_FAPI_RC_PATH_NOT_FOUND if the file does not exist (for NV and hierarchy objects).
 * @retval TSS2_FAPI_RC_IO_ERROR: If the file could not be read by the IO module.
 * @retval TSS2_FAPI_RC_MEMORY: if memory could not be allocated to hold the read data.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_NOT_PROVISIONED FAPI was not provisioned.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_BAD_PATH if the path is used in inappropriate context
 *         or contains illegal characters.
 */
static TSS2_RC
rel_path_to_abs_path(
        IFAPI_KEYSTORE *keystore,
        const char *rel_path,
        char **abs_path)
{
    TSS2_RC r;
    char *directory = NULL;
    bool provision_check_ok;

    /* First expand path in user directory  */
    r = expand_path(keystore, rel_path, &directory);
    goto_if_error(r, "Expand path", cleanup);

    r = expand_path_to_object(keystore, directory,
            keystore->userdir, abs_path);
    goto_if_error2(r, "Object path %s could not be created.", cleanup, directory);


    if (!ifapi_io_path_exists(*abs_path)) {
        /* Second try system directory if object not found in user directory */
        SAFE_FREE(*abs_path);
        r = expand_path_to_object(keystore, directory,
                keystore->systemdir, abs_path);
        goto_if_error2(r, "Object path %s could not be created.", cleanup, directory);

        if (ifapi_io_path_exists(*abs_path)) {
            r = TSS2_RC_SUCCESS;
            goto cleanup;
        }

        /* Check whether provisioning was made for the path profile. */
        r = ifapi_check_provisioned(keystore, rel_path, &provision_check_ok);
        goto_if_error(r, "Provisioning check.", cleanup);

        if (!provision_check_ok) {
            goto_error(r, TSS2_FAPI_RC_NOT_PROVISIONED,
                       "FAPI not provisioned for path: %s.",
                       cleanup, rel_path);
        }

        /* Check type of object which does not exist. */
        if (ifapi_path_type_p(rel_path, IFAPI_NV_PATH)) {
            /* NV directory does not exist. */
            goto_error(r, TSS2_FAPI_RC_PATH_NOT_FOUND,
                    "File %s does not exist.",
                    cleanup, rel_path);
        } else if (ifapi_hierarchy_path_p(rel_path)) {
            /* Hierarchy which should be created during provisioning could not be loaded. */
            goto_error(r, TSS2_FAPI_RC_PATH_NOT_FOUND,
                    "Hierarchy file %s does not exist.",
                    cleanup, rel_path);
        } else {
            /* Object file for key does not exist in keystore */
            goto_error(r, TSS2_FAPI_RC_KEY_NOT_FOUND,
                    "Key %s not found.", cleanup, rel_path);
        }
    }

cleanup:
    SAFE_FREE(directory);
    return r;
}

/** Start loading FAPI object from key store.
 *
 * Keys objects, NV objects, and hierarchies can be loaded.
 *
 * @param[in] keystore The key directories and default profile.
 * @param[in] io  The input/output context being used for file I/O.
 * @param[in] path The relative path of the object. For keys the path will
 *           expanded if possible.
 * @retval TSS2_RC_SUCCESS If the object can be read.
 * @retval TSS2_FAPI_RC_IO_ERROR: if an I/O error was encountered.
 * @retval TSS2_FAPI_RC_PATH_NOT_FOUND if the file does not exist.
 * @retval TSS2_FAPI_RC_MEMORY: if memory could not be allocated to hold the read data.
 * @retval TSS2_FAPI_RC_KEY_NOT_FOUND if a key was not found.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_NOT_PROVISIONED FAPI was not provisioned.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_BAD_PATH if the path is used in inappropriate context
 *         or contains illegal characters.
 */
TSS2_RC
ifapi_keystore_load_async(
    IFAPI_KEYSTORE *keystore,
    IFAPI_IO *io,
    const char *path)
{
    TSS2_RC r;
    char *abs_path = NULL;

    LOG_TRACE("Load object: %s", path);

    /* Free old input buffer if buffer exists */
    SAFE_FREE(io->char_rbuffer);

    /* Save relative directory path for storing in the object. */
    strdup_check(keystore->rel_path, path, r, error_cleanup);

    /* Convert relative path to absolute path in keystore */
    r = rel_path_to_abs_path(keystore, path, &abs_path);
    goto_if_error2(r, "Object %s not found.", error_cleanup, path);

    /* Prepare read operation */
    r = ifapi_io_read_async(io, abs_path);
    goto_if_error2(r, "Read object %s", error_cleanup, path);
    SAFE_FREE(abs_path);
    return r;

 error_cleanup:
    SAFE_FREE(abs_path);
    SAFE_FREE(keystore->rel_path);
    return r;
}

/** Finish loading FAPI object from key store.
 *
 * This function needs to be called repeatedly until it does not return TSS2_FAPI_RC_TRY_AGAIN.
 *
 * @param[in] keystore The key directories and default profile.
 * @param[in,out] io The input/output context being used for file I/O.
 * @param[in] object The caller allocated object which will loaded from keystore.
 * @retval TSS2_RC_SUCCESS After successfully loading the object.
 * @retval TSS2_FAPI_RC_IO_ERROR: if an I/O error was encountered; such as the file was not found.
 * @retval TSS2_FAPI_RC_TRY_AGAIN: if the asynchronous operation is not yet complete.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE if an internal error occurred.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 */
TSS2_RC
ifapi_keystore_load_finish(
    IFAPI_KEYSTORE *keystore MAYBE_UNUSED,
    IFAPI_IO *io,
    IFAPI_OBJECT *object)
{
    TSS2_RC r;
    json_object *jso = NULL;
    uint8_t *buffer = NULL;

    r = ifapi_io_read_finish(io, &buffer, NULL);
    return_try_again(r);
    return_if_error(r, "keystore read_finish failed");

    /* If json objects can't be parse the object store is corrupted */
    jso = ifapi_parse_json((char *)buffer);
    SAFE_FREE(buffer);
    goto_if_null2(jso, "Keystore is corrupted (Json error).", r, TSS2_FAPI_RC_GENERAL_FAILURE,
                  error_cleanup);

    object->rel_path = keystore->rel_path;
    r = ifapi_json_IFAPI_OBJECT_deserialize(jso, object);
    goto_if_error(r, "Deserialize object.", error_cleanup);

    SAFE_FREE(buffer);
    if (jso)
        json_object_put(jso);
    LOG_TRACE("Return %x", r);
    return r;

 error_cleanup:
    SAFE_FREE(buffer);
    if (jso)
        json_object_put(jso);
    LOG_TRACE("Return %x", r);
    object->rel_path = NULL;
    SAFE_FREE(keystore->rel_path);
    return r;
}

/**  Start writing FAPI object to the key store.
 *
 *  Keys objects, NV objects, and hierarchies can be written.
 *
 * @param[in] keystore The key directories and default profile.
 * @param[in] io  The input/output context being used for file I/O.
 * @param[in] path The relative path of the object. For keys the path will
 *           expanded if possible.
 * @param[in] object The object to be written to the keystore.
 * @retval TSS2_RC_SUCCESS if the object is written successfully.
 * @retval TSS2_FAPI_RC_IO_ERROR: if an I/O error was encountered;
 * @retval TSS2_FAPI_RC_MEMORY: if memory could not be allocated to hold the output data.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE if an internal error occurred.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_BAD_PATH if the path is used in inappropriate context
 *         or contains illegal characters.
 * @retval TSS2_FAPI_RC_PATH_NOT_FOUND if a FAPI object path was not found
 *         during authorization.
 */
TSS2_RC
ifapi_keystore_store_async(
    IFAPI_KEYSTORE *keystore,
    IFAPI_IO *io,
    const char *path,
    const IFAPI_OBJECT *object)
{
    TSS2_RC r;
    char *directory = NULL;
    char *file = NULL;
    char *jso_string = NULL;
    json_object *jso = NULL;

    LOG_TRACE("Store object: %s", path);

    /* Prepare write operation: Create directories and valid object path */
    r = expand_path(keystore, path, &directory);
    goto_if_error(r, "Expand path", cleanup);

    if (object->system) {
        r = ifapi_create_dirs(keystore->systemdir, directory);
        goto_if_error2(r, "Directory %s could not be created.", cleanup, directory);

        r = expand_path_to_object(keystore, directory,
                                  keystore->systemdir, &file);
    } else {
        r = ifapi_create_dirs(keystore->userdir, directory);
        goto_if_error2(r, "Directory %s could not be created.", cleanup, directory);

        r = expand_path_to_object(keystore, directory,
                                  keystore->userdir, &file);
    }
    goto_if_error2(r, "Object path %s could not be created.", cleanup, directory);

    /* Generate JSON string to be written to store */
    r = ifapi_json_IFAPI_OBJECT_serialize(object, &jso);
    goto_if_error2(r, "Object for %s could not be serialized.", cleanup, file);

    jso_string = strdup(json_object_to_json_string_ext(jso,
                                                       JSON_C_TO_STRING_PRETTY));
    goto_if_null2(jso_string, "Converting json to string", r, TSS2_FAPI_RC_MEMORY,
                  cleanup);

    /* Start writing the json string to disk */
    r = ifapi_io_write_async(io, file, (uint8_t *) jso_string, strlen(jso_string));
    free(jso_string);
    goto_if_error(r, "write_async failed", cleanup);

cleanup:
    if (jso)
        json_object_put(jso);
    SAFE_FREE(directory);
    SAFE_FREE(file);
    return r;
}

/**  Check whether the key path for a new object does not exist in key store.
 *
 * To prevent overwriting of objects the functions returns an error
 * if the object is already stored in key store.
 * The FAPI path will be expanded to absolute path appropriate for
 * the object to be checked.
 *
 * @param[in] keystore The key directories and default profile.
 * @param[in] path The relative path of the object. For keys the path will
 *           expanded if possible.
 * @param[in] object The object to be checked.
 * @retval TSS2_RC_SUCCESS if the object does not exist and a new object
 *         can be written.
 * @retval TSS2_FAPI_RC_PATH_ALREADY_EXISTS: if the object exists in key store.
 * @retval TSS2_FAPI_RC_MEMORY: if memory could not be allocated to hold the output data.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_BAD_PATH if the path is used in inappropriate context
 *         or contains illegal characters.
 * @retval TSS2_FAPI_RC_PATH_NOT_FOUND if a FAPI object path was not found
 *         during authorization.
 */
TSS2_RC
ifapi_keystore_object_does_not_exist(
    IFAPI_KEYSTORE *keystore,
    const char *path,
    const IFAPI_OBJECT *object)
{
    TSS2_RC r;
    char *directory = NULL;
    char *file = NULL;

    LOG_TRACE("Store object: %s", path);

    /* Prepare write operation: Create directories and valid object path */
    r = expand_path(keystore, path, &directory);
    goto_if_error(r, "Expand path", cleanup);

    if (object->system) {
        r = expand_path_to_object(keystore, directory,
                                  keystore->systemdir, &file);
    } else {
        r = expand_path_to_object(keystore, directory,
                                  keystore->userdir, &file);
    }

    goto_if_error2(r, "Object path %s could not be created.", cleanup, directory);

    if (ifapi_io_path_exists(file)) {
        goto_error(r, TSS2_FAPI_RC_PATH_ALREADY_EXISTS, "File %s already exists.", cleanup, file);
    }

cleanup:
    SAFE_FREE(directory);
    SAFE_FREE(file);
    return r;
}

/** Finish writing a FAPI object to the keystore.
 *
 * This function needs to be called repeatedly until it does not return TSS2_FAPI_RC_TRY_AGAIN.
 *
 * @param[in,out] io The input/output context being used for file I/O.
 * @retval TSS2_RC_SUCCESS: if the function call was a success.
 * @retval TSS2_FAPI_RC_IO_ERROR: if an I/O error was encountered; such as the file was not found.
 * @retval TSS2_FAPI_RC_TRY_AGAIN: if the asynchronous operation is not yet complete.
 *         Call this function again later.
 */
TSS2_RC
ifapi_keystore_store_finish(
    IFAPI_IO *io)
{
    TSS2_RC r;

    /* Finish writing the object */
    r = ifapi_io_write_finish(io);
    return_try_again(r);

    LOG_TRACE("Return %x", r);
    return_if_error(r, "read_finish failed");

    return TSS2_RC_SUCCESS;
}

/** Create a list of all files in a certain directory.
 *
 * The list will be created in form of absolute pathnames.
 *
 * @param[in] keystore The key directories and default profile.
 * @param[in] searchpath The sub directory in key store used for the
 *            creation of the file list.
 * @param[out] results The array of all absolute pathnames.
 * @param[out] numresults The number of files.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_BAD_PATH if the path is used in inappropriate context
 *         or contains illegal characters.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_PATH_NOT_FOUND if a FAPI object path was not found
 *         during authorization.
 */
static TSS2_RC
keystore_list_all_abs(
    IFAPI_KEYSTORE *keystore,
    const char *searchpath,
    char ***results,
    size_t *numresults)
{
    TSS2_RC r;
    char *expanded_search_path = NULL, *full_search_path = NULL;
    size_t num_paths_system, num_paths_user, i, j;
    char **file_ary, **file_ary_system, **file_ary_user;

    *numresults = 0;
    file_ary_user = NULL;
    file_ary_system = NULL;

    if (!searchpath || strcmp(searchpath, "") == 0 || strcmp(searchpath, "/") == 0) {
        /* The complete keystore will be listed, no path expansion */
        expanded_search_path = NULL;
    } else {
        r = expand_path(keystore, searchpath, &expanded_search_path);
        return_if_error(r, "Expand path.");
    }

    /* Get the objects from system store */
    r = ifapi_asprintf(&full_search_path, "%s%s", keystore->systemdir,
                       expanded_search_path ? expanded_search_path : "");
    goto_if_error(r, "Out of memory.", cleanup);

    r = ifapi_io_dirfiles_all(full_search_path, &file_ary_system, &num_paths_system);
    goto_if_error(r, "Get all files in directory.", cleanup);
    SAFE_FREE(full_search_path);

    /* Get the objects from user store */
    r = ifapi_asprintf(&full_search_path, "%s%s", keystore->userdir,
                       expanded_search_path ? expanded_search_path : "");
    goto_if_error(r, "Out of memory.", cleanup);

    r = ifapi_io_dirfiles_all(full_search_path, &file_ary_user, &num_paths_user);

    *numresults = num_paths_system + num_paths_user;
    SAFE_FREE(full_search_path);

    if (*numresults > 0) {

        /* Move file names from list to combined array */
        file_ary = calloc(*numresults, sizeof(char *));
        goto_if_null(file_ary, "Out of memory.", TSS2_FAPI_RC_MEMORY,
                    cleanup);
        i = 0;
        for (j = 0; j < num_paths_system; j++)
            file_ary[i++] = file_ary_system[j];
        for (j = 0; j < num_paths_user; j++)
            file_ary[i++] = file_ary_user[j];

        SAFE_FREE(file_ary_system);
        SAFE_FREE(file_ary_user);
        SAFE_FREE(expanded_search_path);
        *results = file_ary;
    }

cleanup:
    SAFE_FREE(file_ary_system);
    SAFE_FREE(file_ary_user);
    SAFE_FREE(expanded_search_path);
    SAFE_FREE(full_search_path);
    return r;
}

/** Create a list of of objects in a certain search path.
 *
 * A vector of relative paths will be computed.
 *
 * @param[in] keystore The key directories, the default profile.
 * @param[in] searchpath The relative search path in key store.
 * @param[out] results The array with pointers to the relative object paths.
 * @param[out] numresults The number of found objects.
 * @retval TSS2_RC_SUCCESS on success.
 * @retval TSS2_FAPI_RC_MEMORY: if memory could not be allocated.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_BAD_PATH if the path is used in inappropriate context
 *         or contains illegal characters.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_PATH_NOT_FOUND if a FAPI object path was not found
 *         during authorization.
 */
TSS2_RC
ifapi_keystore_list_all(
    IFAPI_KEYSTORE *keystore,
    const char *searchpath,
    char ***results,
    size_t *numresults)
{
    TSS2_RC r;
    size_t i;

    r = keystore_list_all_abs(keystore, searchpath, results, numresults);
    return_if_error(r, "Get all keystore objects.");

    if (*numresults > 0) {
        /* Convert absolute path to relative path */
        for (i = 0; i < *numresults; i++) {
            full_path_to_fapi_path(keystore, (*results)[i]);
        }
    }
    return r;
}

/** Remove file storing a keystore object.
 *
 * @param[in] keystore The key directories, the default profile.
 * @param[in] path The relative name of the object be removed.
 * @retval TSS2_RC_SUCCESS On success.
 * @retval TSS2_FAPI_RC_MEMORY: If memory could not be allocated.
 * @retval TSS2_FAPI_RC_IO_ERROR If the file can't be removed.
 * @retval TSS2_FAPI_RC_PATH_NOT_FOUND if a FAPI object path was not found
 *         during authorization.
 * @retval TSS2_FAPI_RC_KEY_NOT_FOUND if a key was not found.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_NOT_PROVISIONED FAPI was not provisioned.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_BAD_PATH if the path is used in inappropriate context
 *         or contains illegal characters.
 */
TSS2_RC
ifapi_keystore_delete(
    IFAPI_KEYSTORE * keystore,
    char *path)
{
    TSS2_RC r;
    char *abs_path = NULL;

    /* Convert relative path to absolute path in keystore */
    r = rel_path_to_abs_path(keystore, path, &abs_path);
    goto_if_error2(r, "Object %s not found.", cleanup, path);

    r = ifapi_io_remove_file(abs_path);

cleanup:
    SAFE_FREE(abs_path);
    return r;
}

/** Expand directory name.
 *
 * Depending on the directory type the path will be expanded. For hierarchies
 * the profile directory  will be added. For keys the implicit path will
 * be expanded to an explicit path with all directories.
 * @param[in] keystore The key directories and default profile.
 * @param[in] path the implicit  path which has to be expanded if possible.
 * @param[out] directory_name The explicit path (callee-allocated)
 * @retval TSS2_RC_SUCCESS If the explicit path was created.
 * @retval TSS2_FAPI_RC_MEMORY: If memory for the path list could not be allocated.
 * @retval TSS2_FAPI_RC_BAD_VALUE If no explicit path can be derived from the
 *         implicit path.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_BAD_PATH if the path is used in inappropriate context
 *         or contains illegal characters.
 * @retval TSS2_FAPI_RC_PATH_NOT_FOUND if a FAPI object path was not found
 *         during authorization.
 */
static TSS2_RC
expand_directory(IFAPI_KEYSTORE *keystore, const char *path, char **directory_name)
{
    TSS2_RC r;

    if (path && strcmp(path, "") != 0 && strcmp(path, "/") != 0) {
        size_t start_pos = 0;
        if (path[0] == IFAPI_FILE_DELIM_CHAR)
            start_pos = 1;
        if ((strncmp(&path[start_pos], "HS", 2) == 0 ||
             strncmp(&path[start_pos], "HN", 2) == 0 ||
             strncmp(&path[start_pos], "HE", 2) == 0) &&
            strlen(&path[start_pos]) <= 3) {
            /* Root directory is hierarchy */
            r = ifapi_asprintf(directory_name, "/%s/%s/", keystore->defaultprofile,
                               &path[start_pos]);
            return_if_error(r, "Out of memory.");

        } else {
            /* Try to expand a key path */
            r = expand_path(keystore, path, directory_name);
            return_if_error(r, "Expand path.");
        }
    } else {
        *directory_name = NULL;
    }
    return TSS2_RC_SUCCESS;
}

/** Remove directories in keystore.
 *
 * If the expanded directory exists in userdir and systemdir both will be deleted.
 *
 * @param[in] keystore The key directories, the default profile.
 * @param[in] dir_name The relative name of the directory to be removed.
 * @retval TSS2_RC_SUCCESS on success.
 * @retval TSS2_FAPI_RC_MEMORY: If memory could not be allocated.
 * @retval TSS2_FAPI_RC_IO_ERROR If directory can't be deleted.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_BAD_PATH if the path is used in inappropriate context
 *         or contains illegal characters.
 * @retval TSS2_FAPI_RC_PATH_NOT_FOUND if a FAPI object path was not found
 *         during authorization.
 */
TSS2_RC
ifapi_keystore_remove_directories(IFAPI_KEYSTORE *keystore, const char *dir_name)
{
    TSS2_RC r = TSS2_RC_SUCCESS;
    char *absolute_dir_path = NULL;
    char *exp_dir_name = NULL;
    struct stat fbuffer;
    size_t pos;

    r = expand_directory(keystore, dir_name, &exp_dir_name);
    return_if_error(r, "Expand path string.");

    /* Cleanup user part of the store */
    if (keystore->userdir[strlen(keystore->userdir) - 1] == '/')
        pos = 1;
    else
        pos = 0;
    r = ifapi_asprintf(&absolute_dir_path, "%s%s", keystore->userdir,
                       exp_dir_name ? &exp_dir_name[pos] : "");
    goto_if_error(r, "Out of memory.", cleanup);

    if (stat(absolute_dir_path, &fbuffer) == 0) {
        r = ifapi_io_remove_directories(absolute_dir_path, keystore->userdir, NULL);
        goto_if_error2(r, "Could not remove: %s", cleanup, absolute_dir_path);
    }
    SAFE_FREE(absolute_dir_path);

    /* Cleanup system part of the store */
    if (keystore->systemdir[strlen(keystore->systemdir) - 1] == '/')
        /* For a final slash in system dir the startin slash of the
           expanded path will be ignored. */
        pos = 1;
    else
        pos = 0;
    r = ifapi_asprintf(&absolute_dir_path, "%s%s", keystore->systemdir,
                       exp_dir_name ? &exp_dir_name[pos] : "");
    goto_if_error(r, "Out of memory.", cleanup);

    if (stat(absolute_dir_path, &fbuffer) == 0) {
        r = ifapi_io_remove_directories(absolute_dir_path, keystore->systemdir,
                                        "/" IFAPI_POLICY_DIR);
        goto_if_error2(r, "%s cannot be deleted.", cleanup, absolute_dir_path);
    }

cleanup:
    SAFE_FREE(absolute_dir_path);
    SAFE_FREE(exp_dir_name);
    return r;
}

/** Predicate used as function parameter for object searching in keystore.
 *
 * @param[in] object The object from keystore which has to be compared.
 * @param[in] cmp_object The object which will used for the comparison,
 *            by the function with this signature.
 * @retval true if the comparison is successful.
 * @retval true if the comparison is not successful.
 */
typedef TSS2_RC (*ifapi_keystore_object_cmp) (
    IFAPI_OBJECT *object,
    void *cmp_object,
    bool *equal);

/** Search object with a certain propoerty in keystore.
 *
 * @param[in,out] keystore The key directories, the default profile, and the
 *               state information for the asynchronous search.
 * @param[in] io The input/output context being used for file I/O.
 * @param[in] name The name of the searched key.
 * @param[out] found_path The relative path of the found key.
 * @retval TSS2_RC_SUCCESS on success.
 * @retval TSS2_FAPI_RC_MEMORY: if memory could not be allocated.
 * @retval TSS2_FAPI_RC_KEY_NOT_FOUND If the key was not found in keystore.
 * @retval TSS2_FAPI_RC_PATH_NOT_FOUND if a FAPI object path was not found
 *         during authorization.
 * @retval TSS2_FAPI_RC_TRY_AGAIN if an I/O operation is not finished yet and
 *         this function needs to be called again.
 * @retval TSS2_FAPI_RC_BAD_SEQUENCE if the context has an asynchronous
 *         operation already pending.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_IO_ERROR if an error occurred while accessing the
 *         object store.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE if an internal error occurred.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_BAD_PATH if the path is used in inappropriate context
 *         or contains illegal characters.
 * @retval TSS2_FAPI_RC_NOT_PROVISIONED FAPI was not provisioned.
 */
static TSS2_RC
keystore_search_obj(
    IFAPI_KEYSTORE *keystore,
    IFAPI_IO *io,
    void *cmp_object,
    ifapi_keystore_object_cmp cmp_function,
    char **found_path)
{
    TSS2_RC r;
    UINT32 path_idx;
    char *path;
    IFAPI_OBJECT object;
    size_t i;

    /* Mark object "unread" */
    object.objectType = IFAPI_OBJ_NONE;

    switch (keystore->key_search.state) {
    statecase(keystore->key_search.state, KSEARCH_INIT)
        r = ifapi_keystore_list_all(keystore,
                                    "/", /**< search keys and NV objects in store */
                                    &keystore->key_search.pathlist,
                                    &keystore->key_search.numPaths);
        goto_if_error2(r, "Get entities.", cleanup);

        keystore->key_search.path_idx = keystore->key_search.numPaths;
        fallthrough;

    statecase(keystore->key_search.state, KSEARCH_SEARCH_OBJECT)
        /* Use the next object in the path list */
        if (keystore->key_search.path_idx == 0) {
            goto_error(r, TSS2_FAPI_RC_PATH_NOT_FOUND, "Key not found.", cleanup);
        }
        keystore->key_search.path_idx -= 1;
        path_idx = keystore->key_search.path_idx;
        path = keystore->key_search.pathlist[path_idx];
        LOG_TRACE("Check file: %s %zu", path, keystore->key_search.path_idx);

        /* Skip policy files. */
        if (ifapi_path_type_p(path, IFAPI_POLICY_PATH)) {
            return TSS2_FAPI_RC_TRY_AGAIN;
        }

        r = ifapi_keystore_load_async(keystore, io, path);
        return_if_error2(r, "Could not open: %s", path);

        fallthrough;

    statecase(keystore->key_search.state, KSEARCH_READ)
        r = ifapi_keystore_load_finish(keystore, io, &object);
        return_try_again(r);
        goto_if_error(r, "read_finish failed", cleanup);

        /* Check whether the key has the passed name */
        bool keys_equal;
        r = cmp_function(&object, cmp_object, &keys_equal);
        ifapi_cleanup_ifapi_object(&object);
        goto_if_error(r, "Invalid object.", cleanup);

        if (!keys_equal) {
            /* Try next key */
            keystore->key_search.state = KSEARCH_SEARCH_OBJECT;
            return TSS2_FAPI_RC_TRY_AGAIN;
        }
        /* Key found, the absolute path will be converted to relative path. */
        path_idx = keystore->key_search.path_idx;
        *found_path = strdup(keystore->key_search.pathlist[path_idx]);
        goto_if_null(*found_path, "Out of memory.",
                     TSS2_FAPI_RC_MEMORY, cleanup);
        full_path_to_fapi_path(keystore, *found_path);
        break;

    statecasedefault(keystore->key_search.state);
    }
cleanup:
    for (i = 0; i < keystore->key_search.numPaths; i++)
        free(keystore->key_search.pathlist[i]);
    free(keystore->key_search.pathlist);
    if (!*found_path) {
        LOG_ERROR("Object not found");
        r = TSS2_FAPI_RC_KEY_NOT_FOUND;
    }
    keystore->key_search.state = KSEARCH_INIT;
    ifapi_cleanup_ifapi_object(&object);
    return r;
}

/** Search object with a certain name in keystore.
 *
 * @param[in,out] keystore The key directories, the default profile, and the
 *               state information for the asynchronous search.
 * @param[in] io The input/output context being used for file I/O.
 * @param[in] name The name of the searched object.
 * @param[out] found_path The relative path of the found key.
 * @retval TSS2_RC_SUCCESS on success.
 * @retval TSS2_FAPI_RC_MEMORY: if memory could not be allocated.
 * @retval TSS2_FAPI_RC_KEY_NOT_FOUND If the key was not found in keystore.
 * @retval TSS2_FAPI_RC_PATH_NOT_FOUND if a FAPI object path was not found
 *         during authorization.
 * @retval TSS2_FAPI_RC_TRY_AGAIN if an I/O operation is not finished yet and
 *         this function needs to be called again.
 * @retval TSS2_FAPI_RC_BAD_SEQUENCE if the context has an asynchronous
 *         operation already pending.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_IO_ERROR if an error occurred while accessing the
 *         object store.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE if an internal error occurred.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_BAD_PATH if the path is used in inappropriate context
 *         or contains illegal characters.
 * @retval TSS2_FAPI_RC_NOT_PROVISIONED FAPI was not provisioned.
 */
TSS2_RC
ifapi_keystore_search_obj(
    IFAPI_KEYSTORE *keystore,
    IFAPI_IO *io,
    TPM2B_NAME *name,
    char **found_path)
{
    return keystore_search_obj(keystore, io, name,
                               ifapi_object_cmp_name, found_path);
}

/** Search nv object with a certain nv_index (from nv_public) in keystore.
 *
 * @param[in,out] keystore The key directories, the default profile, and the
 *               state information for the asynchronous search.
 * @param[in] io The input/output context being used for file I/O.
 * @param[in] nv_public The public data of the searched nv object.
 * @param[out] found_path The relative path of the found key.
 * @retval TSS2_RC_SUCCESS on success.
 * @retval TSS2_FAPI_RC_MEMORY: if memory could not be allocated.
 * @retval TSS2_FAPI_RC_KEY_NOT_FOUND If the key was not found in keystore.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_PATH_NOT_FOUND if a FAPI object path was not found
 *         during authorization.
 * @retval TSS2_FAPI_RC_TRY_AGAIN if an I/O operation is not finished yet and
 *         this function needs to be called again.
 * @retval TSS2_FAPI_RC_BAD_SEQUENCE if the context has an asynchronous
 *         operation already pending.
 * @retval TSS2_FAPI_RC_IO_ERROR if an error occurred while accessing the
 *         object store.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE if an internal error occurred.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_PATH_ALREADY_EXISTS if the object already exists in object store.
 * @retval TSS2_FAPI_RC_BAD_PATH if the path is used in inappropriate context
 *         or contains illegal characters.
 * @retval TSS2_FAPI_RC_NOT_PROVISIONED FAPI was not provisioned.
 */
TSS2_RC
ifapi_keystore_search_nv_obj(
    IFAPI_KEYSTORE *keystore,
    IFAPI_IO *io,
    TPM2B_NV_PUBLIC *nv_public,
    char **found_path)
{
    return keystore_search_obj(keystore, io, nv_public,
                               ifapi_object_cmp_nv_public, found_path);
}

 /** Check whether keystore object already exists.
  *
  * The passed relative path will be expanded for user store and system store.
  *
  * @param[in] keystore The key directories and default profile.
  * @param[in] path The relative path of the object. For keys the path will
  *            expanded if possible.
  * @retval TSS2_RC_SUCCESS if the object does not exist.
  * @retval TSS2_FAPI_RC_PATH_ALREADY_EXISTS if the file exists in the keystore.
  * @retval TSS2_FAPI_RC_MEMORY: if memory could not be allocated to hold the output data.
  */
TSS2_RC
ifapi_keystore_check_overwrite(
    IFAPI_KEYSTORE *keystore,
    const char *path)
{
    TSS2_RC r;
    char *directory = NULL;
    char *file = NULL;

    /* Expand relative path */
    r = expand_path(keystore, path, &directory);
    goto_if_error(r, "Expand path", cleanup);

    /* Expand absolute path for user and system directory */
    r = expand_path_to_object(keystore, directory,
                              keystore->systemdir, &file);
    goto_if_error(r, "Expand path to object", cleanup);

    if (ifapi_io_path_exists(file)) {
        goto_error(r, TSS2_FAPI_RC_PATH_ALREADY_EXISTS,
                   "Object %s already exists.", cleanup, path);
    }
    SAFE_FREE(file);
    r = expand_path_to_object(keystore, directory,
                              keystore->userdir, &file);
    goto_if_error(r, "Expand path to object", cleanup);

    if (ifapi_io_path_exists(file)) {
        goto_error(r, TSS2_FAPI_RC_PATH_ALREADY_EXISTS,
                   "Object %s already exists.", cleanup, path);
    }
    r = TSS2_RC_SUCCESS;

cleanup:
    SAFE_FREE(directory);
    SAFE_FREE(file);
    return r;
}

/** Check whether keystore object is writeable.
 *
 * The passed relative path will be expanded first for  user store, second for
 * system store if the file does not exist in system store.
 *
 *  Keys objects, NV objects, and hierarchies can be written.
 *
 * @param[in] keystore The key directories and default profile.
 * @param[in] path The relative path of the object. For keys the path will
 *           expanded if possible.
 * @retval TSS2_RC_SUCCESS if the object does not exist.
 * @retval TSS2_FAPI_RC_PATH_ALREADY_EXISTS if the file in objects exists.
 * @retval TSS2_FAPI_RC_MEMORY: if memory could not be allocated to hold the output data.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_IO_ERROR if an error occurred while accessing the
 *         object store.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_BAD_PATH if the path is used in inappropriate context
 *         or contains illegal characters.
 * @retval TSS2_FAPI_RC_PATH_NOT_FOUND if a FAPI object path was not found
 *         during authorization.
 */
TSS2_RC
ifapi_keystore_check_writeable(
    IFAPI_KEYSTORE *keystore,
    const char *path)
{
    TSS2_RC r;
    char *directory = NULL;
    char *file = NULL;

    /* Expand relative path */
    r = expand_path(keystore, path, &directory);
    goto_if_error(r, "Expand path", cleanup);

    /* Expand absolute path for user and system directory */
    r = expand_path_to_object(keystore, directory,
                              keystore->userdir, &file);
    goto_if_error(r, "Expand path to object", cleanup);

    if (ifapi_io_path_exists(file)) {
        r = ifapi_io_check_file_writeable(file);
        goto_if_error2(r, "Object %s is not writable.", cleanup, path);

        /* File can be written */
        goto cleanup;
    } else {
        SAFE_FREE(file);
        r = expand_path_to_object(keystore, directory,
                                  keystore->systemdir, &file);
        goto_if_error(r, "Expand path to object", cleanup);

        if (ifapi_io_path_exists(file)) {
             r = ifapi_io_check_file_writeable(file);
             goto_if_error2(r, "Object %s is not writable.", cleanup, path);

             /* File can be written */
             goto cleanup;
        }
    }

cleanup:
    SAFE_FREE(directory);
    SAFE_FREE(file);
    return r;
}

/** Create a copy of a an UINT8 array..
 *
 * @param[out] dest The caller allocated array which will be the
 *                  destination of the copy operation.
 * @param[in]  src  The source array.
 *
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
static TSS2_RC
copy_uint8_ary(UINT8_ARY *dest, const UINT8_ARY * src) {
    TSS2_RC r = TSS2_RC_SUCCESS;

    /* Check the parameters if they are valid */
    if (src == NULL || dest == NULL) {
        return TSS2_FAPI_RC_BAD_REFERENCE;
    }

    /* Initialize the object variables for a possible error cleanup */
    dest->buffer = NULL;

    /* Create the copy */
    dest->size = src->size;
    dest->buffer = malloc(dest->size);
    goto_if_null(dest->buffer, "Out of memory.", r, error_cleanup);
    memcpy(dest->buffer, src->buffer, dest->size);

    return r;

error_cleanup:
    SAFE_FREE(dest->buffer);
    return r;
}

/** Create a copy of a an ifapi key.
 *
 * @param[out] dest The caller allocated key object which will be the
 *                  destination of the copy operation.
 * @param[in]  src  The source key.
 *
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 */
TSS2_RC
ifapi_copy_ifapi_key(IFAPI_KEY * dest, const IFAPI_KEY * src) {
    TSS2_RC r = TSS2_RC_SUCCESS;

    /* Check the parameters if they are valid */
    if (src == NULL || dest == NULL) {
        return TSS2_FAPI_RC_BAD_REFERENCE;
    }

    /* Initialize the object variables for a possible error cleanup */
    dest->private.buffer = NULL;
    dest->serialization.buffer = NULL;
    dest->appData.buffer = NULL;
    dest->policyInstance = NULL;
    dest->description = NULL;

    /* Create the copy */

    r = copy_uint8_ary(&dest->private, &src->private);
    goto_if_error(r, "Could not copy private", error_cleanup);
    r = copy_uint8_ary(&dest->serialization, &src->serialization);
    goto_if_error(r, "Could not copy serialization", error_cleanup);
    r = copy_uint8_ary(&dest->appData, &src->appData);
    goto_if_error(r, "Could not copy appData", error_cleanup);

    strdup_check(dest->policyInstance, src->policyInstance, r, error_cleanup);
    strdup_check(dest->description, src->description, r, error_cleanup);
    strdup_check(dest->certificate, src->certificate, r, error_cleanup);

    dest->persistent_handle = src->persistent_handle;
    dest->public = src->public;
    dest->creationData = src->creationData;
    dest->creationTicket = src->creationTicket;
    dest->signing_scheme = src->signing_scheme;
    dest->name = src->name;
    dest->with_auth = src->with_auth;
    dest->delete_prohibited = src->delete_prohibited;
    dest->ek_profile = src->ek_profile;

    return r;

error_cleanup:
    ifapi_cleanup_ifapi_key(dest);
    return r;
}

/** Create a copy of a an ifapi hierarchy.
 *
 * @param[out] dest The caller allocated hierarchy object which will be the
 *                  destination of the copy operation.
 * @param[in]  src  The source hierarchy.
 *
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 */
TSS2_RC
ifapi_copy_ifapi_hierarchy(IFAPI_HIERARCHY * dest, const IFAPI_HIERARCHY * src) {
    TSS2_RC r = TSS2_RC_SUCCESS;

    /* Check the parameters if they are valid */
    if (src == NULL || dest == NULL) {
        return TSS2_FAPI_RC_BAD_REFERENCE;
    }

    /* Initialize the object variables for a possible error cleanup */
    dest->description = NULL;

    strdup_check(dest->description, src->description, r, error_cleanup);
    dest->with_auth = src->with_auth;
    dest->authPolicy = src->authPolicy;

    return r;

error_cleanup:
    ifapi_cleanup_ifapi_hierarchy(dest);
    return r;
}

/** Free memory allocated during deserialization of a key object.
 *
 * The key will not be freed (might be declared on the stack).
 *
 * @param[in] key The key object to be cleaned up.
 *
 */
void
ifapi_cleanup_ifapi_key(IFAPI_KEY * key) {
    if (key != NULL) {
        SAFE_FREE(key->policyInstance);
        SAFE_FREE(key->serialization.buffer);
        SAFE_FREE(key->private.buffer);
        SAFE_FREE(key->description);
        SAFE_FREE(key->certificate);
        SAFE_FREE(key->appData.buffer);
    }
}

/** Free memory allocated during deserialization of a pubkey object.
 *
 * The pubkey will not be freed (might be declared on the stack).
 *
 * @param[in] key The pubkey object to be cleaned up.
 */
void
ifapi_cleanup_ifapi_ext_pub_key(IFAPI_EXT_PUB_KEY * key) {
    if (key != NULL) {
        SAFE_FREE(key->pem_ext_public);
        SAFE_FREE(key->certificate);
    }
}

/** Free memory allocated during deserialization of a hierarchy object.
 *
 * The hierarchy object will not be freed (might be declared on the stack).
 *
 * @param[in] hierarchy The hierarchy object to be cleaned up.
 */
void
ifapi_cleanup_ifapi_hierarchy(IFAPI_HIERARCHY * hierarchy) {
    if (hierarchy != NULL) {
        SAFE_FREE(hierarchy->description);
    }
}

/** Free memory allocated during deserialization of a nv object.
 *
 * The nv object will not be freed (might be declared on the stack).
 *
 * @param[in] nv The nv object to be cleaned up.
 */
void
ifapi_cleanup_ifapi_nv(IFAPI_NV * nv) {
    if (nv != NULL) {
        SAFE_FREE(nv->serialization.buffer);
        SAFE_FREE(nv->appData.buffer);
        SAFE_FREE(nv->policyInstance);
        SAFE_FREE(nv->description);
        SAFE_FREE(nv->event_log);
    }
}

/** Free memory allocated during deserialization of a duplicate object.
 *
 * The duplicate object will not be freed (might be declared on the stack).
 *
 * @param[in] duplicate The duplicate object to be cleaned up.
 */
void
ifapi_cleanup_ifapi_duplicate(IFAPI_DUPLICATE * duplicate) {
    if (duplicate != NULL) {
        SAFE_FREE(duplicate->certificate);
    }
}

/** Free keystore related memory allocated during FAPI initialization.
 *
 * The keystore object will not be freed (might be declared on the stack).
 *
 * @param[in] keystore The kystore object to be cleaned up.
 */
void
ifapi_cleanup_ifapi_keystore(IFAPI_KEYSTORE * keystore) {
    if (keystore != NULL) {
        SAFE_FREE(keystore->systemdir);
        SAFE_FREE(keystore->userdir);
        SAFE_FREE(keystore->defaultprofile);
    }
}

/** Create a copy of a an ifapi object storing a key.
 *
 * The key together with the policy of the key will be copied.
 *
 * @param[out] dest The caller allocated key object which will be the
 *                  destination of the copy operation.
 * @param[in]  src  The source key.
 *
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE if the source is not of type key.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 */
TSS2_RC
ifapi_copy_ifapi_key_object(IFAPI_OBJECT * dest, const IFAPI_OBJECT * src) {
    TSS2_RC r = TSS2_RC_SUCCESS;

    /* Check the parameters if they are valid */
    if (src == NULL || dest == NULL) {
        return TSS2_FAPI_RC_BAD_REFERENCE;
    }

    if (src->objectType != IFAPI_KEY_OBJ) {
        LOG_ERROR("Bad object type");
        return TSS2_FAPI_RC_GENERAL_FAILURE;
    }

    /* Initialize the object variables for a possible error cleanup */

    /* Create the copy */
    dest->policy = ifapi_copy_policy(src->policy);
    strdup_check(dest->rel_path, src->rel_path, r, error_cleanup);

    r = ifapi_copy_ifapi_key(&dest->misc.key, &src->misc.key);
    goto_if_error(r, "Could not copy key", error_cleanup);

    dest->objectType = src->objectType;
    dest->system = src->system;
    dest->public.handle = src->public.handle;
    dest->authorization_state = src->authorization_state;

    return r;

error_cleanup:
    ifapi_cleanup_ifapi_object(dest);
    return r;
}

/** Create a copy of a an ifapi object storing a hierarchy.
 *
 * The hierarchy together with the policy of the hierarchy will be copied.
 *
 * @param[out] dest The caller allocated hierarchy object which will be the
 *                  destination of the copy operation.
 * @param[in]  src  The source hieararchy.
 *
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE if the source is not of type key.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 */
TSS2_RC
ifapi_copy_ifapi_hierarchy_object(IFAPI_OBJECT * dest, const IFAPI_OBJECT * src) {
    TSS2_RC r = TSS2_RC_SUCCESS;

    /* Check the parameters if they are valid */
    if (src == NULL || dest == NULL) {
        return TSS2_FAPI_RC_BAD_REFERENCE;
    }

    if (src->objectType != IFAPI_HIERARCHY_OBJ) {
        LOG_ERROR("Bad object type");
        return TSS2_FAPI_RC_GENERAL_FAILURE;
    }

    /* Create the copy */
    dest->policy = ifapi_copy_policy(src->policy);
    strdup_check(dest->rel_path, src->rel_path, r, error_cleanup);

    r = ifapi_copy_ifapi_hierarchy(&dest->misc.hierarchy, &src->misc.hierarchy);
    goto_if_error(r, "Could not copy key", error_cleanup);

    dest->objectType = src->objectType;
    dest->system = src->system;
    dest->public.handle = src->public.handle;
    dest->authorization_state = src->authorization_state;

    return r;

error_cleanup:
    ifapi_cleanup_ifapi_object(dest);
    return r;
}

/** Free memory allocated during deserialization of object.
 *
 * The object will not be freed (might be declared on the stack).
 *
 * @param[in]  object The object to be cleaned up.
 *
 */
void
ifapi_cleanup_ifapi_object(
    IFAPI_OBJECT * object)
{
    if (object != NULL) {
        if (object->objectType != IFAPI_OBJ_NONE) {
            if (object->objectType == IFAPI_KEY_OBJ) {
                ifapi_cleanup_ifapi_key(&object->misc.key);
            } else if (object->objectType == IFAPI_NV_OBJ) {
                ifapi_cleanup_ifapi_nv(&object->misc.nv);
            } else if (object->objectType == IFAPI_DUPLICATE_OBJ) {
                ifapi_cleanup_ifapi_duplicate(&object->misc.key_tree);
            } else if (object->objectType == IFAPI_EXT_PUB_KEY_OBJ) {
                ifapi_cleanup_ifapi_ext_pub_key(&object->misc.ext_pub_key);
            } else if (object->objectType == IFAPI_HIERARCHY_OBJ) {
                ifapi_cleanup_ifapi_hierarchy(&object->misc.hierarchy);
            }
            ifapi_cleanup_policy(object->policy);
            SAFE_FREE(object->rel_path);
            SAFE_FREE(object->policy);
            object->objectType = IFAPI_OBJ_NONE;
        }
    }
}

/** Check whether profile directory exists for a fapi path.
 *
 * It will be checked whether a profile directory exists for a path which starts
 * with a profile name after fapi pathname expansion.
 *
 * @param[in] keystore The key directories and default profile.
 * @param[in] rel_path The relative path to be checked.
 * @param[out] ok The boolean value whether the check ok.
 * @retval TSS2_RC_SUCCESS if the check could be made.
 * @retval TSS2_FAPI_RC_MEMORY: if memory could not be allocated to compute
 * the absolute paths.
 */
TSS2_RC
ifapi_check_provisioned(
    IFAPI_KEYSTORE *keystore,
    const char *rel_path,
    bool *ok)
{
    TSS2_RC r = TSS2_RC_SUCCESS;
    char *directory = NULL;
    char *profile_dir = NULL;
    char *end_profile;

    *ok = false;

    /* First expand path in user directory  */
    r = expand_path(keystore, rel_path, &directory);
    goto_if_error(r, "Expand path", cleanup);

    /* Check whether the path starts with a profile. */
    if (directory && (strncmp(directory, "P_", 2) != 0 || strncmp(directory, "/P_", 2) != 0)) {
        end_profile = strchr(&directory[1], '/');
        if (end_profile) {
            end_profile[0] = '\0';
        }
        /* Compute user path of the profile. */
        r = ifapi_asprintf(&profile_dir, "%s/%s", keystore->userdir, directory);
        goto_if_error2(r, "Profile path could not be created.", cleanup);

         if (ifapi_io_path_exists(profile_dir)) {
             *ok = true;
             goto cleanup;
         }
         /* Compute system path of the profile. */
         SAFE_FREE(profile_dir);
         r = ifapi_asprintf(&profile_dir, "%s/%s", keystore->systemdir, directory);
         goto_if_error2(r, "Profile path could not be created.", cleanup);

         if (ifapi_io_path_exists(profile_dir)) {
             *ok = true;
             goto cleanup;
         }
    } else {
        /* No check needed because no profile found in the path. */
        *ok = true;
    }
 cleanup:
    SAFE_FREE(profile_dir);
    SAFE_FREE(directory);
    return r;
}
