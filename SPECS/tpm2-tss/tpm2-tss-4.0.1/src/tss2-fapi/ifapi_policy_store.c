/* SPDX-License-Identifier: BSD-2-Clause */
/*******************************************************************************
 * Copyright 2018-2019, Fraunhofer SIT sponsored by Infineon Technologies AG
 * All rights reserved.
 *******************************************************************************/

#ifdef HAVE_CONFIG_H
#include <config.h>
#include <dirent.h>
#endif

#include "ifapi_io.h"
#include "ifapi_helpers.h"
#include "ifapi_policy_types.h"
#include "ifapi_policy_store.h"
#include "ifapi_macros.h"
#define LOGMODULE fapi
#include "util/log.h"
#include "util/aux_util.h"
#include "tpm_json_deserialize.h"
#include "ifapi_policy_json_deserialize.h"
#include "ifapi_policy_json_serialize.h"

/** Compute absolute path of policy for IO.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 */
static TSS2_RC
policy_rel_path_to_abs_path(
    IFAPI_POLICY_STORE *pstore,
    const char *rel_path,
    char **abs_path)
{
    TSS2_RC r;

    if (ifapi_path_type_p(rel_path, IFAPI_POLICY_PATH)) {
        r = ifapi_asprintf(abs_path, "%s%s%s.json", pstore->policydir,
                           IFAPI_FILE_DELIM, rel_path);
    } else {
        r = ifapi_asprintf(abs_path, "%s%s%s%s%s.json", pstore->policydir,
                           IFAPI_FILE_DELIM, IFAPI_POLICY_PATH, IFAPI_FILE_DELIM, rel_path);

    }
    return_if_error(r, "Create policy file name.");
    return r;
}
/** Remove file storing a policy object.
 *
 * @param[in] pstore The policy directory.
 * @param[in] path The relative name of the object be removed.
 * @retval TSS2_RC_SUCCESS On success.
 * @retval TSS2_FAPI_RC_MEMORY: If memory could not be allocated.
 * @retval TSS2_FAPI_RC_PATH_NOT_FOUND If no file is found in policy store.
 * @retval TSS2_FAPI_RC_IO_ERROR If the file can't be removed.
 */
TSS2_RC
ifapi_policy_delete(
    IFAPI_POLICY_STORE * pstore,
    char *path)
{
    TSS2_RC r;
    char *abs_path = NULL;

    /* Convert relative path to absolute path in policy store */
    r = policy_rel_path_to_abs_path(pstore, path, &abs_path);
    goto_if_error2(r, "Path %s could not be created.", cleanup, path);

    if (!ifapi_io_path_exists(abs_path)) {
        goto_error(r, TSS2_FAPI_RC_PATH_NOT_FOUND,
                   "Policy %s not found.", cleanup, path);
    }

    if (remove(abs_path) != 0) {
        LOG_WARNING("File: %s can't be deleted.", abs_path);
    }

cleanup:
    SAFE_FREE(abs_path);
    return r;
}

/** Store policy store parameters in the policy store context.
 *
 * Also the user directory will be created if it does not exist.
 *
 * @param[out] pstore The keystore to be initialized.
 * @param[in] config_policydir The configured policy directory.
 * @retval TSS2_RC_SUCCESS If the keystore can be initialized.
 * @retval TSS2_FAPI_RC_IO_ERROR If the policy store can't be
 *         initialized.
 * @retval TSS2_FAPI_RC_MEMORY: if memory could not be allocated.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_policy_store_initialize(
    IFAPI_POLICY_STORE *pstore,
    const char *config_policydir)
{
    TSS2_RC r;
    char *policy_dir = NULL;

    memset(pstore, 0, sizeof(IFAPI_POLICY_STORE));
    check_not_null(config_policydir);

    strdup_check(pstore->policydir, config_policydir, r, error);

    r = ifapi_asprintf(&policy_dir, "%s%s%s", config_policydir,
                       (strcmp(&config_policydir[strlen(config_policydir) - 1],
                        IFAPI_FILE_DELIM) == 0) ? "" : IFAPI_FILE_DELIM,
					   IFAPI_POLICY_PATH);
    goto_if_error(r, "Out of memory.", error);

    r = ifapi_io_check_create_dir(policy_dir, FAPI_READ);
    goto_if_error2(r, "Policy directory %s can't be created.", error, policy_dir);

    SAFE_FREE(policy_dir);
    return TSS2_RC_SUCCESS;

error:
    SAFE_FREE(policy_dir);
    return r;
}

/** Start loading FAPI policy from policy store.
 *
 * Keys objects, NV objects, and hierarchies can be loaded.
 *
 * @param[in] pstore The policy directory.
 * @param[in] io  The input/output context being used for file I/O.
 * @param[in] path The relative path of the object. For keys the path will
 *           expanded if possible.
 * @retval TSS2_RC_SUCCESS If the object can be read.
 * @retval TSS2_FAPI_RC_IO_ERROR: if an I/O error was encountered.
 * @retval TSS2_FAPI_RC_PATH_NOT_FOUND if the file does not exist.
 * @retval TSS2_FAPI_RC_MEMORY: if memory could not be allocated to hold the read data.
 */
TSS2_RC
ifapi_policy_store_load_async(
    IFAPI_POLICY_STORE *pstore,
    IFAPI_IO *io,
    const char *path)
{
    TSS2_RC r;
    char *abs_path = NULL;

    LOG_TRACE("Load policy: %s", path);

    /* First it will be checked whether the only valid characters occur in the path. */
    if (pstore) {
        r = ifapi_check_valid_path(path);
        return_if_error(r, "Invalid path.");
    }

    /* Free old input buffer if buffer exists */
    SAFE_FREE(io->char_rbuffer);

    /* Convert relative path to absolute path in keystore */
    if (pstore) {
        r = policy_rel_path_to_abs_path(pstore, path, &abs_path);
        goto_if_error2(r, "Object %s not found.", cleanup, path);
    } else {
        abs_path = strdup(path);
        if (!abs_path) {
            return TSS2_FAPI_RC_MEMORY;
        }
    }

    if (!ifapi_io_path_exists(abs_path)) {
        goto_error(r, TSS2_FAPI_RC_BAD_PATH, "Policy %s does not exist.", cleanup, path);
    }

    /* Prepare read operation */
    r = ifapi_io_read_async(io, abs_path);

cleanup:
    SAFE_FREE(abs_path);
    return r;
}

/** Finish loading FAPI policy from policy store.
 *
 *
 * This function needs to be called repeatedly until it does not return TSS2_FAPI_RC_TRY_AGAIN.
 *
 * @param[in] pstore The policy context with the policy directory.
 * @param[in,out] io The input/output context being used for file I/O.
 * @param[in] policy The caller allocated policy which will loaded from policy store.
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
ifapi_policy_store_load_finish(
    IFAPI_POLICY_STORE *pstore,
    IFAPI_IO *io,
    TPMS_POLICY *policy)
{
    TSS2_RC r;
    json_object *jso = NULL;
    uint8_t *buffer = NULL;
    /* ptore parameter is used to be prepared if transmission of state information
       between async and finish will be necessary in future extensions. */
    UNUSED(pstore);

    r = ifapi_io_read_finish(io, &buffer, NULL);
    return_try_again(r);
    return_if_error(r, "keystore read_finish failed");

    /* If json objects can't be parse the object store is corrupted */
    jso = ifapi_parse_json((char *)buffer);
    SAFE_FREE(buffer);
    return_if_null(jso, "Policy store is corrupted (Json error).", TSS2_FAPI_RC_GENERAL_FAILURE);

    r = ifapi_json_TPMS_POLICY_deserialize(jso, policy);
    goto_if_error(r, "Deserialize policy", cleanup);

cleanup:
    SAFE_FREE(buffer);
    if (jso)
        json_object_put(jso);
    LOG_TRACE("Return %x", r);
    return r;

}

/**  Start writing FAPI object to the key store.
 *
 * The relative path will be expanded, if the default policy directory (/policy)
 * is not part of the path.
 *
 * @param[in] pstore The policy context with the policy directory.
 * @param[in] io  The input/output context being used for file I/O.
 * @param[in] path The relative path of the policy.
 * @param[in] policy The policy to be written to the policy store.
 * @retval TSS2_RC_SUCCESS If the policy is written successfully.
 * @retval TSS2_FAPI_RC_IO_ERROR: If an I/O error was encountered;
 * @retval TSS2_FAPI_RC_MEMORY: If memory could not be allocated to hold the output data.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 */
TSS2_RC
ifapi_policy_store_store_async(
    IFAPI_POLICY_STORE *pstore,
    IFAPI_IO *io,
    const char *path,
    const TPMS_POLICY *policy)
{
    TSS2_RC r;
    char *jso_string = NULL;
    json_object *jso = NULL;
    char *abs_path = NULL;

    LOG_TRACE("Store policy: %s", path);

    /* First it will be checked whether the only valid characters occur in the path. */
    r = ifapi_check_valid_path(path);
    return_if_error(r, "Invalid path.");

    /* Convert relative path to absolute path in the policy store */
    r = policy_rel_path_to_abs_path(pstore, path, &abs_path);
    goto_if_error2(r, "Path %s could not be created.", cleanup, path);

    /* Generate JSON string to be written to store */
    r = ifapi_json_TPMS_POLICY_serialize(policy, &jso);
    goto_if_error2(r, "Policy %s could not be serialized.", cleanup, path);

    jso_string = strdup(json_object_to_json_string_ext(jso,
                                                       JSON_C_TO_STRING_PRETTY));
    goto_if_null2(jso_string, "Converting json to string", r, TSS2_FAPI_RC_MEMORY,
                  cleanup);

    /* Start writing the json string to disk */
    r = ifapi_io_write_async(io, abs_path, (uint8_t *) jso_string, strlen(jso_string));
    free(jso_string);
    goto_if_error(r, "write_async failed", cleanup);

cleanup:
    if (jso)
        json_object_put(jso);
    SAFE_FREE(abs_path);
    return r;
}

/** Finish writing a FAPI policy object to the policy store.
 *
 * This function needs to be called repeatedly until it does not return TSS2_FAPI_RC_TRY_AGAIN.
 *
 * @param[in] pstore The policy context with the policy directory.
 * @param[in,out] io The input/output context being used for file I/O.
 * @retval TSS2_RC_SUCCESS: if the function call was a success.
 * @retval TSS2_FAPI_RC_IO_ERROR: if an I/O error was encountered; such as the file was not found.
 * @retval TSS2_FAPI_RC_TRY_AGAIN: if the asynchronous operation is not yet complete.
           Call this function again later.
 */
TSS2_RC
ifapi_policy_store_store_finish(
    IFAPI_POLICY_STORE *pstore,
    IFAPI_IO *io)
{
    TSS2_RC r;

    /* Pstore parameter is used to be prepared if transmission of state information
       between async and finish will be necessary in future extensions. */
    UNUSED(pstore);
    /* Finish writing the policy */
    r = ifapi_io_write_finish(io);
    return_try_again(r);

    LOG_TRACE("Return %x", r);
    return_if_error(r, "read_finish failed");

    return TSS2_RC_SUCCESS;
}

 /** Check whether policy already exists.
  *
  * @param[in] pstore The key directories and default profile.
  * @param[in] path The relative path of the policy.
  * @retval TSS2_RC_SUCCESS if the object does not exist.
  * @retval TSS2_FAPI_RC_PATH_ALREADY_EXISTS if the policy file exists.
  * @retval TSS2_FAPI_RC_MEMORY: if memory could not be allocated to hold the output data.
  */
TSS2_RC
ifapi_policystore_check_overwrite(
    IFAPI_POLICY_STORE *pstore,
    const char *path)
{
    TSS2_RC r;
    char *abs_path = NULL;

    /* Convert relative path to absolute path in keystore */
    r = policy_rel_path_to_abs_path(pstore, path, &abs_path);
    goto_if_error2(r, "Object %s not found.", cleanup, path);

    if (ifapi_io_path_exists(abs_path)) {
        goto_error(r, TSS2_FAPI_RC_PATH_ALREADY_EXISTS,
                   "Object %s already exists.", cleanup, path);
    }
    r = TSS2_RC_SUCCESS;

cleanup:
    SAFE_FREE(abs_path);
    return r;
}
