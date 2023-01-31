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

#include "tss2_mu.h"
#include "tss2_fapi.h"
#include "fapi_int.h"
#include "fapi_util.h"
#include "tss2_esys.h"
#include "ifapi_policy_json_serialize.h"
#define LOGMODULE fapi
#include "util/log.h"
#include "util/aux_util.h"


/** One-Call function for Fapi_GetTpmBlobs
 *
 * Get the public and private blobs of a TPM object. They can be loaded with a
 * lower-level API such as the SAPI or the ESAPI.
 *
 * @param[in,out] context The FAPI_CONTEXT
 * @param[in] path The path to the key for which the blobs will be returned
 * @param[out] tpm2bPublic The returned public area of the object. May be NULL
 * @param[out] tpm2bPublicSize The size of tpm2bPublic in bytes. May be NULL
 * @param[out] tpm2bPrivate The returned private area of the object. May be
 *             NULL
 * @param[out] tpm2bPrivateSize The size of tpm2bPrivate in bytes. May be NULL
 * @param[out] policy The policy that is associated with the object encoded in
 *             JSON. May be NULL
 *
 * @retval TSS2_RC_SUCCESS: if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE: if context or path is NULL.
 * @retval TSS2_FAPI_RC_BAD_CONTEXT: if context corruption is detected.
 * @retval TSS2_FAPI_RC_BAD_PATH: if path does not map to a FAPI entity.
 * @retval TSS2_FAPI_RC_BAD_SEQUENCE: if the context has an asynchronous
 *         operation already pending.
 * @retval TSS2_FAPI_RC_IO_ERROR: if the data cannot be saved.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory for
 *         internal operations or return parameters.
 * @retval TSS2_FAPI_RC_PATH_NOT_FOUND if a FAPI object path was not found
 *         during authorization.
 * @retval TSS2_FAPI_RC_KEY_NOT_FOUND if a key was not found.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_TRY_AGAIN if an I/O operation is not finished yet and
 *         this function needs to be called again.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE if an internal error occurred.
 * @retval TSS2_FAPI_RC_NOT_PROVISIONED FAPI was not provisioned.
 */
TSS2_RC
Fapi_GetTpmBlobs(
    FAPI_CONTEXT   *context,
    char     const *path,
    uint8_t       **tpm2bPublic,
    size_t         *tpm2bPublicSize,
    uint8_t       **tpm2bPrivate,
    size_t         *tpm2bPrivateSize,
    char          **policy)
{
    LOG_TRACE("called for context:%p", context);

    TSS2_RC r;

    /* Check for NULL parameters */
    check_not_null(context);
    check_not_null(path);

    r = Fapi_GetTpmBlobs_Async(context, path);
    return_if_error_reset_state(r, "Entity_GetTPMBlobs");

    do {
        /* We wait for file I/O to be ready if the FAPI state automata
           are in a file I/O state. */
        r = ifapi_io_poll(&context->io);
        return_if_error(r, "Something went wrong with IO polling");

        /* Repeatedly call the finish function, until FAPI has transitioned
           through all execution stages / states of this invocation. */
        r = Fapi_GetTpmBlobs_Finish(context, tpm2bPublic, tpm2bPublicSize, tpm2bPrivate,
                                    tpm2bPrivateSize, policy);
    } while (base_rc(r) == TSS2_BASE_RC_TRY_AGAIN);

    return_if_error_reset_state(r, "Entity_GetTPMBlobs");

    LOG_TRACE("finished");
    return TSS2_RC_SUCCESS;
}

/** Asynchronous function for Fapi_GetTpmBlobs
 *
 * Get the public and private blobs of a TPM object. They can be loaded with a
 * lower-level API such as the SAPI or the ESAPI.
 *
 * Call Fapi_GetTpmBlobs_Finish to finish the execution of this command.
 *
 * @param[in,out] context The FAPI_CONTEXT
 * @param[in] path The path to the key for which the blobs will be returned
 *
 * @retval TSS2_RC_SUCCESS: if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE: if context or path is NULL.
 * @retval TSS2_FAPI_RC_BAD_CONTEXT: if context corruption is detected.
 * @retval TSS2_FAPI_RC_BAD_PATH: if path does not map to a FAPI entity.
 * @retval TSS2_FAPI_RC_BAD_SEQUENCE: if the context has an asynchronous
 *         operation already pending.
 * @retval TSS2_FAPI_RC_IO_ERROR: if the data cannot be saved.
 * @retval TSS2_FAPI_RC_MEMORY: if the FAPI cannot allocate enough memory for
 *         internal operations or return parameters.
 * @retval TSS2_FAPI_RC_PATH_NOT_FOUND if a FAPI object path was not found
 *         during authorization.
 * @retval TSS2_FAPI_RC_KEY_NOT_FOUND if a key was not found.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_NOT_PROVISIONED FAPI was not provisioned.
 */
TSS2_RC
Fapi_GetTpmBlobs_Async(
    FAPI_CONTEXT   *context,
    char     const *path)
{
    LOG_TRACE("called for context:%p", context);
    LOG_TRACE("path: %s", path);

    TSS2_RC r;

    /* Check for NULL parameters */
    check_not_null(context);
    check_not_null(path);

    /* Load the object from the key store. */
    r = ifapi_keystore_load_async(&context->keystore, &context->io, path);
    return_if_error2(r, "Could not open: %s", path);

    /* Initialize the context state for this operation. */
    context->state = ENTITY_GET_TPM_BLOBS_READ;
    LOG_TRACE("finished");
    return TSS2_RC_SUCCESS;
}

/** Asynchronous finish function for Fapi_GetTpmBlobs
 *
 * This function should be called after a previous Fapi_GetTpmBlobs_Async.
 *
 * @param[in,out] context The FAPI_CONTEXT
 * @param[out] tpm2bPublic The returned public area of the object. May be NULL
 * @param[out] tpm2bPublicSize The size of tpm2bPublic in bytes. May be NULL
 * @param[out] tpm2bPrivate The returned private area of the object. May be
 *             NULL
 * @param[out] tpm2bPrivateSize The size of tpm2bPrivate in bytes. May be NULL
 * @param[out] policy The policy that is associated with the object encoded in
 *             JSON. May be NULL
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
 * @retval TSS2_FAPI_RC_BAD_PATH if a path is used in inappropriate context
 *         or contains illegal characters.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE if an internal error occurred.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 */
TSS2_RC
Fapi_GetTpmBlobs_Finish(
    FAPI_CONTEXT   *context,
    uint8_t       **tpm2bPublic,
    size_t         *tpm2bPublicSize,
    uint8_t       **tpm2bPrivate,
    size_t         *tpm2bPrivateSize,
    char          **policy)
{
    LOG_TRACE("called for context:%p", context);

    TSS2_RC r;
    IFAPI_OBJECT object;
    UINT16 private_size;
    size_t offset;
    json_object *jso = NULL;

    /* Check for NULL parameters */
    check_not_null(context);

    switch (context->state) {
        statecase(context->state, ENTITY_GET_TPM_BLOBS_READ);
            /* Finish readon the metadata from key store. */
            r = ifapi_keystore_load_finish(&context->keystore, &context->io, &object);
            return_try_again(r);
            return_if_error_reset_state(r, "read_finish failed");

            if (object.objectType != IFAPI_KEY_OBJ) {
                goto_error(r, TSS2_FAPI_RC_BAD_PATH, "No key object.", error_cleanup);
            }

            /* Marshal the public data to the output parameter. */
            if (tpm2bPublic && tpm2bPublicSize) {
                *tpm2bPublic = malloc(sizeof(uint8_t) * sizeof(TPM2B_PUBLIC));
                goto_if_null(*tpm2bPublic, "Out of memory.",
                        TSS2_FAPI_RC_MEMORY, error_cleanup);
                offset = 0;
                r = Tss2_MU_TPM2B_PUBLIC_Marshal(&object.misc.key.public,
                        *tpm2bPublic, sizeof(TPM2B_PUBLIC), &offset);
                goto_if_error_reset_state(r, "FAPI marshal TPM2B_PUBLIC",
                        error_cleanup);

                *tpm2bPublicSize = offset;
                goto_if_error(r, "Marshaling TPM2B_PUBLIC", error_cleanup);
            }

            /* Marshal the private data to the output parameter. */
            if (tpm2bPrivate && tpm2bPrivateSize) {
                private_size = object.misc.key.private.size;
                *tpm2bPrivateSize = private_size + sizeof(UINT16);
                *tpm2bPrivate = malloc(*tpm2bPrivateSize);
                goto_if_null(*tpm2bPrivate, "Out of memory.",
                        TSS2_FAPI_RC_MEMORY, error_cleanup);
                offset = 0;
                r = Tss2_MU_UINT16_Marshal(private_size,
                                           *tpm2bPrivate, sizeof(TPM2B_PRIVATE), &offset);
                goto_if_error_reset_state(r, "FAPI marshal UINT16", error_cleanup);

                memcpy(*tpm2bPrivate + offset, &object.misc.key.private.buffer[0], private_size);
            }

            /* Duplicate the policy to the output parameter. */
            if (object.policy && policy) {
                r = ifapi_json_TPMS_POLICY_serialize(
                        object.policy, &jso);
                goto_if_error(r, "Serialize policy", error_cleanup);

                strdup_check(*policy,
                        json_object_to_json_string_ext(jso, JSON_C_TO_STRING_PRETTY),
                        r, error_cleanup);
                json_object_put(jso);
            } else {
                if (policy) {
                    strdup_check(*policy, "", r, error_cleanup);
                }
            }

            /* Cleanup any intermediate results and state stored in the context. */
            ifapi_cleanup_ifapi_object(&object);
            context->state = _FAPI_STATE_INIT;
            LOG_TRACE("finished");
            return TSS2_RC_SUCCESS;

        statecasedefault(context->state);
    }
error_cleanup:
    /* Cleanup any intermediate results and state stored in the context. */
    if (jso)
        json_object_put(jso);
    ifapi_cleanup_ifapi_object(&object);
    ifapi_cleanup_ifapi_object(&context->loadKey.auth_object);
    ifapi_cleanup_ifapi_object(context->loadKey.key_object);
    ifapi_cleanup_ifapi_object(&context->createPrimary.pkey_object);
    LOG_TRACE("finished");
    return r;
}
