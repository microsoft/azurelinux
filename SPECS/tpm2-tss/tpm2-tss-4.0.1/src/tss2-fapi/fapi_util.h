/* SPDX-License-Identifier: BSD-2-Clause */
/*******************************************************************************
 * Copyright 2018-2019, Fraunhofer SIT sponsored by Infineon Technologies AG
 * All rights reserved.
 *******************************************************************************/
#ifndef FAPI_UTIL_H
#define FAPI_UTIL_H

#include <stdint.h>
#include <stdarg.h>
#include <stdbool.h>
#include <sys/stat.h>
#include <json-c/json.h>
#include <json-c/json_util.h>

#include "util/aux_util.h"
#include "tss2_esys.h"
#include "tss2_fapi.h"
#include "fapi_int.h"
#include "ifapi_helpers.h"

TSS2_RC
ifapi_flush_object(FAPI_CONTEXT *context, ESYS_TR session);

TSS2_RC
ifapi_get_session_async(
    ESYS_CONTEXT *esys,
    ESYS_TR saltkey,
    const IFAPI_PROFILE*profile,
    TPMI_ALG_HASH hashAlg);

TSS2_RC
ifapi_get_session_finish(ESYS_CONTEXT *esys, ESYS_TR *session,
                         TPMA_SESSION flags);

const char *
ifapi_get_object_path(IFAPI_OBJECT *object);

TSS2_RC
ifapi_set_auth(
    FAPI_CONTEXT *context,
    IFAPI_OBJECT *auth_object,
    const char *description);

TSS2_RC
ifapi_get_free_handle_async(FAPI_CONTEXT *fctx, TPM2_HANDLE *handle);

TSS2_RC
ifapi_get_free_handle_finish(FAPI_CONTEXT *fctx, TPM2_HANDLE *handle,
                             TPM2_HANDLE max);

TSS2_RC
ifapi_init_primary_async(
    FAPI_CONTEXT *context,
    TSS2_KEY_TYPE ktype);

TSS2_RC
ifapi_init_primary_finish(
    FAPI_CONTEXT *context,
    TSS2_KEY_TYPE ktype,
    IFAPI_OBJECT *hierarchy);

TSS2_RC
ifapi_session_init(FAPI_CONTEXT *context);

TSS2_RC
ifapi_non_tpm_mode_init(FAPI_CONTEXT *context);

void
ifapi_session_clean(FAPI_CONTEXT *context);

TSS2_RC
ifapi_cleanup_session(FAPI_CONTEXT *context);

void
ifapi_primary_clean(FAPI_CONTEXT *context);

TSS2_RC
ifapi_get_sessions_async(
    FAPI_CONTEXT *context,
    IFAPI_SESSION_TYPE session_flags,
    TPMA_SESSION attribute_flags1,
    TPMA_SESSION attribute_flags2);

TSS2_RC
ifapi_get_sessions_finish(
    FAPI_CONTEXT *context,
    const IFAPI_PROFILE *profile,
    TPMI_ALG_HASH hash_alg);

TSS2_RC
ifapi_merge_profile_into_nv_template(
    FAPI_CONTEXT *context,
    IFAPI_NV_TEMPLATE *template);

TSS2_RC
ifapi_merge_profile_into_template(
    const IFAPI_PROFILE *profile,
    IFAPI_KEY_TEMPLATE *template);

TSS2_RC
ifapi_load_key_async(FAPI_CONTEXT *context, size_t position);

TSS2_RC
ifapi_load_parent_keys_async(FAPI_CONTEXT *context, char const *keyPath);

TSS2_RC
ifapi_load_key_finish(FAPI_CONTEXT *context, bool flush_parent);

TSS2_RC
ifapi_load_keys_async(
    FAPI_CONTEXT *context,
    char const *keyPath);

TSS2_RC
ifapi_load_keys_finish(
    FAPI_CONTEXT *context,
    bool flush_parent,
    ESYS_TR *handle,
    IFAPI_OBJECT **key_object);

TSS2_RC
ifapi_nv_read(
    FAPI_CONTEXT *context,
    uint8_t     **data,
    size_t       *size);

void
ifapi_flush_policy_session(
    FAPI_CONTEXT *context,
    ESYS_TR session,
    TSS2_RC r);

TSS2_RC
ifapi_nv_write(
    FAPI_CONTEXT *context,
    char         *nvPath,
    size_t         param_offset,
    uint8_t const *data,
    size_t         size);

TSS2_RC
ifapi_get_random(
    FAPI_CONTEXT *context,
    size_t numBytes,
    uint8_t **data);

TSS2_RC
ifapi_load_key(
    FAPI_CONTEXT  *context,
    char    const *keyPath,
    IFAPI_OBJECT **key_object);

TSS2_RC
ifapi_key_sign(
    FAPI_CONTEXT    *context,
    IFAPI_OBJECT    *sig_key_object,
    char const      *padding,
    TPM2B_DIGEST    *digest,
    TPMT_SIGNATURE **tpm_signature,
    char           **publicKey,
    char           **certificate);

TSS2_RC
ifapi_authorize_object(
    FAPI_CONTEXT *context,
    IFAPI_OBJECT *object,
    ESYS_TR      *session);

TSS2_RC
ifapi_get_json(
    FAPI_CONTEXT *context,
    IFAPI_OBJECT *object,
    char **json_string);

TSS2_RC
ifapi_key_create_prepare(
    FAPI_CONTEXT  *context,
    char   const *keyPath,
    char   const *policyPath);

TSS2_RC
ifapi_key_create_prepare_auth(
    FAPI_CONTEXT  *context,
    char   const *keyPath,
    char   const *policyPath,
    char   const *authValue);

TSS2_RC
ifapi_key_create_prepare_sensitive(
    FAPI_CONTEXT  *context,
    char    const *keyPath,
    char    const *policyPath,
    size_t         dataSize,
    char    const *authValue,
    uint8_t const *data);

TSS2_RC
ifapi_key_create(
    FAPI_CONTEXT *context,
    IFAPI_KEY_TEMPLATE *template);

TSS2_RC
ifapi_get_sig_scheme(
    FAPI_CONTEXT *context,
    IFAPI_OBJECT *object,
    char const *padding,
    TPM2B_DIGEST *digest,
    TPMT_SIG_SCHEME *sig_scheme);

TSS2_RC
ifapi_change_auth_hierarchy(
    FAPI_CONTEXT *context,
    ESYS_TR handle,
    IFAPI_OBJECT *hierarchy_object,
    TPM2B_AUTH *newAuthValue);

TSS2_RC
ifapi_change_policy_hierarchy(
    FAPI_CONTEXT *context,
    ESYS_TR handle,
    IFAPI_OBJECT *hierarchy_object,
    TPMS_POLICY *policy);

IFAPI_OBJECT
*ifapi_allocate_object(FAPI_CONTEXT *context);

void
ifapi_free_objects(FAPI_CONTEXT *context);

void
ifapi_free_object(FAPI_CONTEXT *context, IFAPI_OBJECT **object);

TPM2_RC
ifapi_capability_init(FAPI_CONTEXT *context);

TPM2_RC
ifapi_capability_get(FAPI_CONTEXT *context, TPM2_CAP capability,
                     UINT32 count, TPMS_CAPABILITY_DATA **capability_data);

TSS2_RC
ifapi_get_certificates(
    FAPI_CONTEXT *context,
    UINT32 min_handle,
    UINT32 max_handle,
    NODE_OBJECT_T **cert_list);

TSS2_RC
ifapi_initialize_object(
    ESYS_CONTEXT *ectx,
    IFAPI_OBJECT *object);

TSS2_RC
ifapi_esys_serialize_object(
    ESYS_CONTEXT *ectx,
    IFAPI_OBJECT *object);

TSS2_RC
ifapi_get_description(IFAPI_OBJECT *object, char **description);

void
ifapi_set_description(IFAPI_OBJECT *object, char *description);

TSS2_RC
ifapi_get_key_properties(
    FAPI_CONTEXT *context,
    char const *key_path,
    bool *is_primary,
    bool *in_null_hierarchy);

TSS2_RC
ifapi_create_primary(FAPI_CONTEXT *context, IFAPI_KEY_TEMPLATE *template);

#endif /* FAPI_UTIL_H */
