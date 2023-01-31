/* SPDX-License-Identifier: BSD-2-Clause */
/*******************************************************************************
 * Copyright 2018-2019, Fraunhofer SIT sponsored by Infineon Technologies AG
 * All rights reserved.
 *******************************************************************************/

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <errno.h>
#ifndef NO_DL
#include <dlfcn.h>
#endif /* NO_DL */

#include "tss2_tcti.h"
#include "tss2_tctildr.h"
#include "tss2_esys.h"
#include "tss2_fapi.h"
#include "fapi_int.h"
#include "fapi_util.h"
#include "ifapi_json_deserialize.h"
#include "ifapi_policy.h"
#define LOGMODULE fapi
#include "util/log.h"
#include "util/aux_util.h"

/** One-Call function for Fapi_Initialize
 *
 * Initializes a FAPI_CONTEXT that holds all the state and metadata information
 * during an interaction with the TPM.
 *
 * @param[out] context The FAPI_CONTEXT
 * @param[in] uri Unused in this version of the FAPI. Must be NULL
 *
 * @retval TSS2_RC_SUCCESS: if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE: if context is NULL.
 * @retval TSS2_FAPI_RC_BAD_VALUE: if uri is not NULL.
 * @retval TSS2_FAPI_RC_IO_ERROR: if the data cannot be saved.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory for
 *         internal operations or return parameters.
 * @retval TSS2_FAPI_RC_TRY_AGAIN if an I/O operation is not finished yet and
 *         this function needs to be called again.
 * @retval TSS2_FAPI_RC_BAD_SEQUENCE if the context has an asynchronous
 *         operation already pending.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE if an internal error occurred.
 * @retval TSS2_FAPI_RC_BAD_PATH if a path is used in inappropriate context
 *         or contains illegal characters.
 * @retval TSS2_ESYS_RC_* possible error codes of ESAPI.
 */
TSS2_RC
Fapi_Initialize(
    FAPI_CONTEXT **context,
    char const *uri)
{
    LOG_TRACE("called for context:%p", context);

    TSS2_RC r = TSS2_RC_SUCCESS;

    /* Check for NULL parameters */
    check_not_null(context);
    if (uri != NULL) {
        LOG_ERROR("uri is not NULL");
        return TSS2_FAPI_RC_BAD_VALUE;
    }

    r = Fapi_Initialize_Async(context, uri);
    return_if_error(r,  "FAPI Async call initialize");
    check_oom(*context);

    do {
        /* We wait for file I/O to be ready if the FAPI state automata
           are in a file I/O state. */
        r = ifapi_io_poll(&(*context)->io);
        return_if_error(r, "Something went wrong with IO polling");

        /* Repeatedly call the finish function, until FAPI has transitioned
           through all execution stages / states of this invocation. */
        r = Fapi_Initialize_Finish(context);
    } while (base_rc(r) == TSS2_BASE_RC_TRY_AGAIN);

    LOG_TRACE("finished");
    return r;
}

/** Asynchronous function for Fapi_Initialize
 *
 * Initializes a FAPI_CONTEXT that holds all the state and metadata information
 * during an interaction with the TPM.
 *
 * Call Fapi_Initialize to finish the execution of this command.
 *
 * @param[out] context The FAPI_CONTEXT
 * @param[in] uri Unused in this version of the FAPI. Must be NULL
 *
 * @retval TSS2_RC_SUCCESS: if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE: if context is NULL.
 * @retval TSS2_FAPI_RC_BAD_VALUE: if uri is not NULL.
 * @retval TSS2_FAPI_RC_IO_ERROR: if the data cannot be saved.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory for
 *         internal operations or return parameters.
 */
TSS2_RC
Fapi_Initialize_Async(
    FAPI_CONTEXT **context,
    char const *uri)
{
    LOG_TRACE("called for context:%p", context);
    LOG_TRACE("uri: %s", uri);

    TSS2_RC r = TSS2_RC_SUCCESS;

    /* Check for NULL parameters */
    check_not_null(context);
    if (uri != NULL) {
        LOG_ERROR("uri is not NULL");
        return TSS2_FAPI_RC_BAD_VALUE;
    }

    *context = NULL;

    /* Allocate memory for the FAPI context
     * After this errors must jump to cleanup_return instead of returning. */
    *context = calloc(1, sizeof(FAPI_CONTEXT));
    return_if_null(*context, "Out of memory.", TSS2_FAPI_RC_MEMORY);
    memset(*context, 0, sizeof(FAPI_CONTEXT));

    /* Initialize the context */
    r = ifapi_config_initialize_async(&(*context)->io);
    goto_if_error(r, "Could not initialize FAPI context", cleanup_return);

    memset(&(*context)->cmd.Initialize, 0, sizeof(IFAPI_INITIALIZE));

    ifapi_policy_ctx_init(*context);

    /* Initialize the context state for this operation. */
    (*context)->state = INITIALIZE_READ;

cleanup_return:
    if (r)
        SAFE_FREE(*context);
    LOG_TRACE("finished");
    return r;
}

/** Asynchronous finish function for Fapi_Initialize
 *
 * This function should be called after a previous Fapi_Initialize_Async.
 *
 * @param[out] context The FAPI_CONTEXT
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
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE if an internal error occurred.
 * @retval TSS2_FAPI_RC_BAD_PATH if a path is used in inappropriate context
 *         or contains illegal characters.
 * @retval TSS2_ESYS_RC_* possible error codes of ESAPI.
 */
TSS2_RC
Fapi_Initialize_Finish(
    FAPI_CONTEXT **context)
{
    LOG_TRACE("called for context:%p", context);

    TSS2_RC r;
    TPMI_YES_NO moreData;
    TSS2_TCTI_CONTEXT *fapi_tcti = NULL;
    TPMS_TIME_INFO *currentTime = NULL;
    IFAPI_OBJECT pkey_object;
    size_t i;

    /* Check for NULL parameters */
    check_not_null(context);
    check_not_null(*context);

    /* Helpful alias pointers */
    TPMS_CAPABILITY_DATA **capability = &(*context)->cmd.Initialize.capability;
    IFAPI_INITIALIZE * command = &(*context)->cmd.Initialize;

    switch ((*context)->state) {
    statecase((*context)->state, INITIALIZE_READ);
        /* This is the entry point; finishing the initialization of the config module. */
        r = ifapi_config_initialize_finish(&(*context)->io, &(*context)->config);
        return_try_again(r);
        goto_if_error(r, "Could not finish initialization", cleanup_return);

        /* Initialize the event log module. */
        r = ifapi_eventlog_initialize(&((*context)->eventlog),
                                      (*context)->config.log_dir,
                                      (*context)->config.firmware_log_file,
                                      (*context)->config.ima_log_file);
        goto_if_error(r, "Initializing eventlog module", cleanup_return);

        /* Initialize the keystore. */
        r = ifapi_keystore_initialize(&((*context)->keystore),
                                      (*context)->config.keystore_dir,
                                      (*context)->config.user_dir,
                                      (*context)->config.profile_name);
        goto_if_error2(r, "Keystore could not be initialized.", cleanup_return);

        /* Initialize the policy store. */
        /* Policy directory will be placed in keystore dir */
        r = ifapi_policy_store_initialize(&((*context)->pstore),
                                          (*context)->config.keystore_dir);
        goto_if_error2(r, "Keystore could not be initialized.", cleanup_return);

        fallthrough;

    statecase((*context)->state, INITIALIZE_INIT_TCTI);
        if (strcasecmp((*context)->config.tcti, "none") == 0) {
            /* FAPI will be used in none TPM mode */
            (*context)->esys = NULL;
            (*context)->state = INITIALIZE_READ_PROFILE_INIT;
            return TSS2_FAPI_RC_TRY_AGAIN;
        }

        /* Call for the TctiLdr to initialize a TCTI context given the config
           from the FAPI config module. */
        r = Tss2_TctiLdr_Initialize((*context)->config.tcti, &fapi_tcti);
        goto_if_error(r, "Initializing TCTI.", cleanup_return);

        /* Initialize an ESYS context using this Tcti. */
        r = Esys_Initialize(&((*context)->esys), fapi_tcti, NULL);
        goto_if_error(r, "Initialize esys context.", cleanup_return);

        /* Call Startup on the TPM. */
        r = Esys_Startup((*context)->esys, TPM2_SU_CLEAR);
        if (r != TSS2_RC_SUCCESS && r != TPM2_RC_INITIALIZE) {
            LOG_ERROR("Esys_Startup FAILED! Response Code : 0x%x", r);
            return r;
        }
        fallthrough;

    statecase((*context)->state, INITIALIZE_GET_CAP);
        /* Retrieve the maximal value for transfer of nv data from the TPM. */
        r = Esys_GetCapability_Async((*context)->esys, ESYS_TR_NONE, ESYS_TR_NONE,
                                     ESYS_TR_NONE,
                                     TPM2_CAP_TPM_PROPERTIES, TPM2_PT_NV_BUFFER_MAX, 1);
        goto_if_error(r, "Error json deserialize", cleanup_return);

        fallthrough;

    statecase((*context)->state, INITIALIZE_WAIT_FOR_CAP);
        r = Esys_GetCapability_Finish((*context)->esys, &moreData, capability);
        return_try_again(r);
        goto_if_error(r, "Get capability data.", cleanup_return);

        /* Check if the TPM returns the NV_BUFFER_MAX value. */
        if ((*capability)->data.tpmProperties.count == 1 &&
                (*capability)->data.tpmProperties.tpmProperty[0].property ==
                TPM2_PT_NV_BUFFER_MAX) {
            (*context)->nv_buffer_max = (*capability)->data.tpmProperties.tpmProperty[0].value;
            /* FAPI also contains an upper limit on the NV_MAX_BUFFER size. This is
               useful for vTPMs that could in theory allow for several Megabytes of
               max transfer buffer sizes. */
            if ((*context)->nv_buffer_max > IFAPI_MAX_BUFFER_SIZE)
                (*context)->nv_buffer_max = IFAPI_MAX_BUFFER_SIZE;
        } else {
            /* Note that for some time it was legal for a TPM to not return this value.
               in that case FAPI falls back to 64 bytes for NV_BUFFER_MAX that all TPMs
               must support. This slows down communication for NV read and write but
               ensures that data can be exchanged with the TPM. */
            (*context)->nv_buffer_max = 64;
        }
        fallthrough;

    statecase((*context)->state, INITIALIZE_READ_PROFILE_INIT);
        /* Initialize the proviles module that loads cryptographic profiles.
           The default profile is taken from config. */
        r = ifapi_profiles_initialize_async(&(*context)->profiles, &(*context)->io,
                                            (*context)->config.profile_dir,
                                            (*context)->config.profile_name);
        return_if_error(r, "Read profile");

        fallthrough;

    statecase((*context)->state, INITIALIZE_READ_PROFILE);
        r = ifapi_profiles_initialize_finish(&(*context)->profiles, &(*context)->io);
        FAPI_SYNC(r, "Read profile.", cleanup_return);

        if ((*context)->esys) {
            r = Esys_ReadClock_Async((*context)->esys,
                                     ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE);
            goto_if_error(r, "ReadClock_Async.", cleanup_return);
        } else {
            break;
        }
        fallthrough;

    statecase((*context)->state, INITIALIZE_READ_TIME);
        r = Esys_ReadClock_Finish((*context)->esys, &currentTime);
        return_try_again(r);
        goto_if_error(r, "ReadClock_Finish.", cleanup_return);

        (*context)->init_time = *currentTime;
        SAFE_FREE(currentTime);

        /* Compute the list of all NULL primary keys stored in keystore. */
        r = ifapi_keystore_list_all(&(*context)->keystore, "/HN", &command->pathlist,
                                    &command->numPaths);
        goto_if_error(r, "get entities.", cleanup_return);

        command->numNullPrimaries = 0;
        for (i = 0; i < command->numPaths; i++) {
            if (ifapi_null_primary_p(command->pathlist[i])) {
                if (i !=  command->numNullPrimaries) {
                    char *sav_path;
                    sav_path = command->pathlist[command->numNullPrimaries];
                    command->pathlist[command->numNullPrimaries] = command->pathlist[i];
                    command->pathlist[i] = sav_path;
                    command->numNullPrimaries += 1;
                } else {
                    command->numNullPrimaries += 1;
                }
            }
        }
        command->path_idx = 0;
        fallthrough;

    statecase((*context)->state, INITIALIZE_CHECK_NULL_PRIMARY);
        if (command->path_idx == command->numNullPrimaries)
            break;

        r = ifapi_keystore_load_async(&(*context)->keystore, &(*context)->io,
                                      command->pathlist[command->path_idx]);
        goto_if_error2(r, "Could not open %s", cleanup_return,
                           command->pathlist[command->path_idx]);
        fallthrough;

    statecase((*context)->state, INITIALIZE_READ_NULL_PRIMARY);
        r = ifapi_keystore_load_finish(&(*context)->keystore, &(*context)->io,
                                       &pkey_object);
        return_try_again(r);
        goto_if_error2(r, "Could not open %s", cleanup_return,
                       command->pathlist[command->path_idx]);

        if (pkey_object.misc.key.reset_count !=
            (*context)->init_time.clockInfo.resetCount) {
            ifapi_cleanup_ifapi_object(&pkey_object);
            /* The primary is not valid anymore. */
            r = ifapi_keystore_remove_directories(&(*context)->keystore,
                                                  command->pathlist[command->path_idx]);
            if (r) {
                LOG_WARNING("The keys %s in NULL hierarchy cannot be deleted.",
                            command->pathlist[command->path_idx]);
            }
        } else {
            ifapi_cleanup_ifapi_object(&pkey_object);
        }
        command->path_idx += 1;
        (*context)->state = INITIALIZE_CHECK_NULL_PRIMARY;
        return TSS2_FAPI_RC_TRY_AGAIN;

    statecasedefault((*context)->state);
    }

    (*context)->state = _FAPI_STATE_INIT;
    SAFE_FREE(*capability);
    for (size_t i = 0; i < command->numPaths; i++) {
        SAFE_FREE(command->pathlist[i]);
    }
    SAFE_FREE(command->pathlist);
    LOG_TRACE("finished");
    return TSS2_RC_SUCCESS;

cleanup_return:
    /* Cleanup any intermediate results and state stored in the context. */
    for (size_t i = 0; i < command->numPaths; i++) {
        SAFE_FREE(command->pathlist[i]);
    }
    SAFE_FREE(command->pathlist);
    if ((*context)->esys) {
        Esys_GetTcti((*context)->esys, &fapi_tcti);
        Esys_Finalize(&(*context)->esys);
    }
    if (fapi_tcti) {
        Tss2_TctiLdr_Finalize(&fapi_tcti);
    }

    /* Free the context memory in case of an error. */
    free(*context);
    *context = NULL;

    return r;
}
