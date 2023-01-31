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
#include <dirent.h>

#include "tss2_fapi.h"
#include "fapi_int.h"
#include "fapi_util.h"
#include "tss2_esys.h"
#include "ifapi_keystore.h"
#define LOGMODULE fapi
#include "util/log.h"
#include "util/aux_util.h"

/** One-Call function for Fapi_List
 *
 * Enumerates all objects in the metadatastore in a fiven path and returns them
 * in a list of complete paths from the root with the values separated by
 * colons.
 *
 * @param[in,out] context The FAPI_CONTEXT
 * @param[in] searchPath The path that identifies the root of the search
 * @param[out] pathList A colon-separated list of all objects in the root path
 *
 * @retval TSS2_RC_SUCCESS: if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE: if context, searchPath, pathlist is
 *         NULL.
 * @retval TSS2_FAPI_RC_BAD_CONTEXT: if context corruption is detected.
 * @retval TSS2_FAPI_RC_BAD_PATH: if searchPath does not map to a FAPI entity.
 * @retval TSS2_FAPI_RC_BAD_SEQUENCE: if the context has an asynchronous
 *         operation already pending.
 * @retval TSS2_FAPI_RC_IO_ERROR: if the data cannot be saved.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory for
 *         internal operations or return parameters.
 * @retval TSS2_FAPI_RC_PATH_NOT_FOUND if a FAPI object path was not found
 *         during authorization.
 * @retval TSS2_FAPI_RC_NOT_PROVISIONED FAPI was not provisioned.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 */
TSS2_RC
Fapi_List(
    FAPI_CONTEXT *context,
    char   const *searchPath,
    char        **pathList)
{
    LOG_TRACE("called for context:%p", context);

    TSS2_RC r;

    /* Check for NULL parameters */
    check_not_null(context);
    check_not_null(searchPath);
    check_not_null(pathList);

    r = Fapi_List_Async(context, searchPath);
    return_if_error_reset_state(r, "Entities_List");

    do {
        /* We wait for file I/O to be ready if the FAPI state automata
           are in a file I/O state. */
        r = ifapi_io_poll(&context->io);
        return_if_error(r, "Something went wrong with IO polling");

        /* Repeatedly call the finish function, until FAPI has transitioned
           through all execution stages / states of this invocation. */
        r = Fapi_List_Finish(context, pathList);
    } while (base_rc(r) == TSS2_BASE_RC_TRY_AGAIN);

    return_if_error_reset_state(r, "Entities_List");

    LOG_TRACE("finished");
    return TSS2_RC_SUCCESS;
}

/** Asynchronous function for Fapi_List
 *
 * Enumerates all objects in the metadatastore in a fiven path and returns them
 * in a list of complete paths from the root with the values separated by
 * colons.
 *
 * Call Fapi_List_Finish to finish the execution of this command.
 *
 * @retval TSS2_RC_SUCCESS: if the function call was a success.
 * @param[in,out] context The FAPI_CONTEXT
 * @param[in] searchPath The path that identifies the root of the search
 *
 * @retval TSS2_FAPI_RC_BAD_REFERENCE: if context or searchPath is
 *         NULL.
 * @retval TSS2_FAPI_RC_BAD_CONTEXT: if context corruption is detected.
 * @retval TSS2_FAPI_RC_BAD_PATH: if searchPath does not map to a FAPI entity.
 * @retval TSS2_FAPI_RC_BAD_SEQUENCE: if the context has an asynchronous
 *         operation already pending.
 * @retval TSS2_FAPI_RC_IO_ERROR: if the data cannot be saved.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory for
 *         internal operations or return parameters.
 */
TSS2_RC
Fapi_List_Async(
    FAPI_CONTEXT *context,
    char   const *searchPath)
{
    LOG_TRACE("called for context:%p", context);
    LOG_TRACE("searchPath: %s", searchPath);

    TSS2_RC r;

    /* Check for NULL parameters */
    check_not_null(context);
    check_not_null(searchPath);

    /* Helpful alias pointers */
    IFAPI_Entities_List * command = &context->cmd.Entities_List;

    r = ifapi_non_tpm_mode_init(context);
    return_if_error(r, "Initialize List");

    /* Copy parameters to context for use during _Finish. */
    strdup_check(command->searchPath, searchPath, r, error_cleanup);

    LOG_TRACE("finished");
    return TSS2_RC_SUCCESS;

error_cleanup:
    /* Cleanup duplicated input parameters that were copied before. */
    SAFE_FREE(command->searchPath);
    return r;
}

/** Asynchronous finish function for Fapi_List
 *
 * This function should be called after a previous Fapi_List_Async.
 *
 * @param[in,out] context The FAPI_CONTEXT
 * @param[out] pathList A colon-separated list of all objects in the root path
 *
 * @retval TSS2_RC_SUCCESS: if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE: if context or pathList is NULL.
 * @retval TSS2_FAPI_RC_BAD_CONTEXT: if context corruption is detected.
 * @retval TSS2_FAPI_RC_BAD_SEQUENCE: if the context has an asynchronous
 *         operation already pending.
 * @retval TSS2_FAPI_RC_IO_ERROR: if the data cannot be saved.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory for
 *         internal operations or return parameters.
 * @retval TSS2_FAPI_RC_TRY_AGAIN: if the asynchronous operation is not yet
 *         complete. Call this function again later.
 * @retval TSS2_FAPI_RC_PATH_NOT_FOUND if a FAPI object path was not found
 *         during authorization.
 * @retval TSS2_FAPI_RC_NOT_PROVISIONED FAPI was not provisioned.
 * @retval TSS2_FAPI_RC_BAD_PATH if the path is used in inappropriate context
 *         or contains illegal characters.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 */
TSS2_RC
Fapi_List_Finish(
    FAPI_CONTEXT *context,
    char        **pathList)
{
    LOG_TRACE("called for context:%p", context);
    bool provision_check_ok;

    TSS2_RC r = TSS2_RC_SUCCESS;
    size_t sizePathList = 0;
    size_t numPaths = 0;
    char **pathArray = NULL;

    /* Check for NULL parameters */
    check_not_null(context);
    check_not_null(pathList);

    /* Helpful alias pointers */
    IFAPI_Entities_List * command = &context->cmd.Entities_List;

    /* Retrieve the objects along the search path. */
    r = ifapi_keystore_list_all(&context->keystore, command->searchPath,
                                &pathArray, &numPaths);
    goto_if_error(r, "get entities.", cleanup);

    if (numPaths == 0)
        goto check_provisioning;

    /* Determine size of char string to be returnded */
    for (size_t i = 0; i < numPaths; i++)
        sizePathList += strlen(pathArray[i]);

    /* Allocate path list plus colon separators plus \0-terminator */
    *pathList = malloc(sizePathList + (numPaths - 1) + 1);
    goto_if_null2(*pathList, "Out of memory", r, TSS2_FAPI_RC_MEMORY,  cleanup);

    (*pathList)[0] = '\0';
    (*pathList)[sizePathList + numPaths - 1] = '\0';

    /* Concatenate the path entries to the output string. */
    for (size_t i = 0; i < numPaths; i++) {
        strcat(*pathList, pathArray[i]);
        if (i < numPaths - 1)
            strcat(*pathList, IFAPI_LIST_DELIM);
    }

 check_provisioning:
    if (numPaths == 0 && (r == TSS2_RC_SUCCESS)) {
        if (command->searchPath && (strcmp(command->searchPath,"/") == 0
                                    || strcmp(command->searchPath,"") == 0)) {
            LOG_WARNING("Path not found: %s", command->searchPath);
            r = TSS2_FAPI_RC_NOT_PROVISIONED;
        } else {
            r = ifapi_check_provisioned(&context->keystore, command->searchPath, &provision_check_ok);
            goto_if_error(r, "Provisioning check.", cleanup);

            if (provision_check_ok) {
                LOG_WARNING("Path not found: %s", command->searchPath);
                r = TSS2_FAPI_RC_PATH_NOT_FOUND;
            } else {
                LOG_WARNING("Profile of path not provisioned: %s", command->searchPath);
                r = TSS2_FAPI_RC_NOT_PROVISIONED;
            }
        }
    }
    LOG_TRACE("finished");

cleanup:
    /* Cleanup any intermediate results and state stored in the context. */
    if (numPaths > 0) {
        for (size_t i = 0; i < numPaths; i++){
            SAFE_FREE(pathArray[i]);
        }
    }
    SAFE_FREE(command->searchPath);
    SAFE_FREE(pathArray);
    return r;
}
