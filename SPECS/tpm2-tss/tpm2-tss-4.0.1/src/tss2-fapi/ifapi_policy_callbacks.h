/* SPDX-License-Identifier: BSD-2-Clause */
/*******************************************************************************
 * Copyright 2018-2019, Fraunhofer SIT sponsored by Infineon Technologies AG
 * All rights reserved.
 *******************************************************************************/
#ifndef FAPI_POLICY_CALLBACKS_H
#define FAPI_POLICY_CALLBACKS_H


/** The states for policy execution callbacks */
enum IFAPI_STATE_POL_CB_EXCECUTE {
    POL_CB_EXECUTE_INIT = 0,
    POL_CB_LOAD_KEY,
    POL_CB_LOAD_KEY_FINISH,
    POL_CB_SEARCH_POLICY,
    POL_CB_EXECUTE_SUB_POLICY,
    POL_CB_NV_READ,
    POL_CB_READ_NV_POLICY,
    POL_CB_READ_OBJECT,
    POL_CB_AUTHORIZE_OBJECT,
    POL_CB_AUTHORIZE_KEY
};

/** The context of the policy execution */
typedef struct {
    enum  IFAPI_STATE_POL_CB_EXCECUTE cb_state;
                                    /**< The execution state of the current policy callback */
    char*object_path;               /**< The pathname determined by object search */
    IFAPI_OBJECT object;            /**< Object to be authorized */
    ESYS_TR key_handle;             /**< Handle of a used key */
    ESYS_TR nv_index;               /**< Index of nv object storing a policy */
    ESYS_TR auth_index;             /**< Index of authorization object */
    ESYS_TR flush_handle;           /**< Handle which has to be flushed after policy execution */
    IFAPI_OBJECT auth_object;       /**< FAPI auth object needed for authorization */
    IFAPI_LoadKey load_ctx_sav;
    IFAPI_LoadKey load_ctx;
    IFAPI_CreatePrimary create_primary_ctx_sav;
    IFAPI_CreatePrimary create_primary_ctx;
    IFAPI_OBJECT *key_object_ptr;
    IFAPI_OBJECT *auth_object_ptr;
    IFAPI_NV_Cmds nv_cmd_state;
    IFAPI_NV_Cmds nv_cmd_state_sav; /**< backup for state of fapi nv commands */
    TPM2B_DIGEST policy_digest;
    ESYS_TR session;
    TPMS_POLICY *policy;
} IFAPI_POLICY_EXEC_CB_CTX;

TSS2_RC
ifapi_get_key_public(
    const char *path,
    TPMT_PUBLIC *public,
    void *context);

TSS2_RC
ifapi_get_object_name(
    const char *path,
    TPM2B_NAME *name,
    void *context);

TSS2_RC
ifapi_get_nv_public(
    const char *path,
    TPMI_RH_NV_INDEX nv_index,
    TPMS_NV_PUBLIC *nv_public,
    void *context);

TSS2_RC
ifapi_read_pcr(
    TSS2_POLICY_PCR_SELECTION *pcr_selection,
    TPML_PCR_SELECTION *out_pcr_selection,
    TPML_DIGEST *out_pcr_digests,
    void *ctx);

TSS2_RC
ifapi_policyeval_cbauth(
    TPM2B_NAME *name,
    ESYS_TR *object_handle,
    ESYS_TR *auth_handle,
    ESYS_TR *authSession,
    void *userdata);

TSS2_RC
ifapi_policyeval_cbload_key(
    TPM2B_NAME *name,
    ESYS_TR *object_handle,
    void *userdata);

TSS2_RC
ifapi_branch_selection(
    TSS2_OBJECT *auth_object,
    const char *branch_names[8],
    size_t branch_count,
    size_t *branch_idx,
    void *userdata);

TSS2_RC
ifapi_sign_buffer(
    char *key_pem,
    char *public_key_hint,
    TPMI_ALG_HASH key_pem_hash_alg,
    uint8_t *buffer,
    size_t buffer_size,
    const uint8_t **signature,
    size_t *signature_size,
    void *userdata);

TSS2_RC
ifapi_exec_auth_policy(
    TPMT_PUBLIC *key_public,
    TPMI_ALG_HASH hash_alg,
    TPM2B_DIGEST *digest,
    TPM2B_NONCE *policyRef,
    TPMT_SIGNATURE *signature,
    void *userdata);

TSS2_RC
ifapi_exec_auth_nv_policy(
    TPMS_NV_PUBLIC *nv_public,
    TPMI_ALG_HASH hash_alg,
    void *userdata);

TSS2_RC
ifapi_get_duplicate_name(
    TPM2B_NAME *name,
    void *userdata);

TSS2_RC
ifapi_policy_action(
    const char *action,
    void *userdata);

#endif /* FAPI_POLICY_CALLBACKS_H */
