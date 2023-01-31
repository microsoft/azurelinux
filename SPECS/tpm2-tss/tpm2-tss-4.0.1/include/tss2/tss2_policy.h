/* SPDX-License-Identifier: BSD-2-Clause */
#ifndef INCLUDE_TSS2_TSS2_POLICY_H_
#define INCLUDE_TSS2_TSS2_POLICY_H_

#include <stdint.h>

#include "tss2_esys.h"
#include "tss2_tpm2_types.h"

#define TSS2_POLICY_RC_LAYER TSS2_RC_LAYER(13)

#define TSS2_POLICY_RC_GENERAL_FAILURE             ((TSS2_RC)(TSS2_POLICY_RC_LAYER | \
                                                      TSS2_BASE_RC_GENERAL_FAILURE))
#define TSS2_POLICY_RC_IO_ERROR                    ((TSS2_RC)(TSS2_POLICY_RC_LAYER | \
                                                      TSS2_BASE_RC_IO_ERROR))
#define TSS2_POLICY_RC_AUTHORIZATION_UNKNOWN       ((TSS2_RC)(TSS2_POLICY_RC_LAYER | \
                                                        TSS2_BASE_RC_AUTHORIZATION_UNKNOWN))
#define TSS2_POLICY_RC_BAD_VALUE                   ((TSS2_RC)(TSS2_POLICY_RC_LAYER | \
                                                      TSS2_BASE_RC_BAD_VALUE))
#define TSS2_POLICY_RC_MEMORY                      ((TSS2_RC)(TSS2_POLICY_RC_LAYER | \
                                                      TSS2_BASE_RC_MEMORY))
#define TSS2_POLICY_RC_BAD_REFERENCE               ((TSS2_RC)(TSS2_POLICY_RC_LAYER | \
                                                      TSS2_BASE_RC_BAD_REFERENCE))
#define TSS2_POLICY_RC_BAD_TEMPLATE                ((TSS2_RC)(TSS2_POLICY_RC_LAYER | \
                                                        TSS2_BASE_RC_BAD_TEMPLATE))
#define TSS2_POLICY_RC_POLICY_NOT_CALCULATED       ((TSS2_RC)(TSS2_POLICY_RC_LAYER | \
                                                        TSS2_BASE_RC_NOT_PROVISIONED))
#define TSS2_POLICY_RC_BUFFER_TOO_SMALL            ((TSS2_RC)(TSS2_POLICY_RC_LAYER | \
                                                        TSS2_BASE_RC_BAD_SIZE))
#define TSS2_POLICY_RC_NULL_CALLBACK               ((TSS2_RC)(TSS2_POLICY_RC_LAYER | \
                                                        TSS2_BASE_RC_CALLBACK_NULL))

typedef struct TSS2_POLICY_CTX TSS2_POLICY_CTX;

typedef struct TSS2_OBJECT TSS2_OBJECT;
struct TSS2_OBJECT {
    ESYS_TR                                      handle;    /**< Handle used by ESAPI */
};

/** Policy type TPMS_PCRVALUE
 */
typedef struct TPMS_PCRVALUE TPMS_PCRVALUE;
struct TPMS_PCRVALUE {
    UINT32                                          pcr;    /**< None */
    TPM2_ALG_ID                                 hashAlg;    /**< None */
    TPMU_HA                                      digest;    /**< None */
};

/** Policy type TPML_PCRVALUES
 */
typedef struct TPML_PCRVALUES TPML_PCRVALUES;
struct TPML_PCRVALUES {
    UINT32                                        count;    /**< None */
    TPMS_PCRVALUE                                pcrs[];    /**< Array of pcr values */
};

typedef TSS2_RC (*TSS2_POLICY_CB_PUBLIC) (
    const char *path,
    TPMT_PUBLIC *public,
    void *userdata);   /* e.g. for ESAPI_CONTEXT */

typedef TSS2_RC (*TSS2_POLICY_CB_NAME) (
    const char *path,
    TPM2B_NAME *name,
    void *userdata);   /* e.g. for ESAPI_CONTEXT */

typedef enum TSS2_POLICY_PCR_SELECTOR TSS2_POLICY_PCR_SELECTOR;
enum TSS2_POLICY_PCR_SELECTOR {
    TSS2_POLICY_PCR_SELECTOR_PCR_SELECT = 0,
    TSS2_POLICY_PCR_SELECTOR_PCR_SELECTION
};

typedef union TSS2_POLICY_PCR_SELECTIONS TSS2_POLICY_PCR_SELECTIONS;
union TSS2_POLICY_PCR_SELECTIONS {
    TPMS_PCR_SELECT pcr_select;
    TPML_PCR_SELECTION pcr_selection;
};

typedef struct TSS2_POLICY_PCR_SELECTION TSS2_POLICY_PCR_SELECTION;
struct TSS2_POLICY_PCR_SELECTION {
    enum TSS2_POLICY_PCR_SELECTOR type;
    TSS2_POLICY_PCR_SELECTIONS selections;
};

typedef TSS2_RC (*TSS2_POLICY_CB_PCR) (
    TSS2_POLICY_PCR_SELECTION *selection,
    TPML_PCR_SELECTION *out_selection,
    TPML_DIGEST *out_digest,
    void *userdata);   /* e.g. for ESAPI_CONTEXT */

typedef TSS2_RC (*TSS2_POLICY_CB_NVPUBLIC) (
    const char *path,
    TPMI_RH_NV_INDEX nv_index,
    TPMS_NV_PUBLIC *nv_public,
    void *userdata);   /* e.g. for ESAPI_CONTEXT */

typedef struct TSS2_POLICY_CALC_CALLBACKS TSS2_POLICY_CALC_CALLBACKS;
struct TSS2_POLICY_CALC_CALLBACKS {
    TSS2_POLICY_CB_PCR                    cbpcr; /**< Callback to compute current PCR value */
    void                        *cbpcr_userdata;
    TSS2_POLICY_CB_NAME                  cbname; /**< Callback to compute name of an object from path */
    void                        *cbname_userdata;
    TSS2_POLICY_CB_PUBLIC               cbpublic; /**< Callback to compute public info of a key */
    void                        *cbpublic_userdata;
    TSS2_POLICY_CB_NVPUBLIC             cbnvpublic; /**< Callback to compute the NV public from path */
    void                        *cbnvpublic_userdata;
};

typedef TSS2_RC (*TSS2_POLICY_CB_EXEC_AUTH) (
    TPM2B_NAME *name,
    ESYS_TR *object_handle,
    ESYS_TR *auth_handle,
    ESYS_TR *authSession,
    void *userdata);

typedef TSS2_RC (*TSS2_POLICY_CB_EXEC_LOAD) (
    TPM2B_NAME *name,
    ESYS_TR *object_handle,
    void *userdata);

typedef TSS2_RC (*TSS2_POLICY_CB_EXEC_POLSEL) (
    TSS2_OBJECT *auth_object,
    const char **branch_names,
    size_t branch_count,
    size_t *branch_idx,
    void *userdata);

typedef TSS2_RC (*TSS2_POLICY_CB_EXEC_SIGN) (
    char *key_pem,
    char *public_key_hint,
    TPMI_ALG_HASH key_pem_hash_alg,
    uint8_t *buffer,
    size_t buffer_size,
    const uint8_t **signature,
    size_t *signature_size,
    void *userdata);

typedef TSS2_RC (*TSS2_POLICY_CB_EXEC_POLAUTH) (
    TPMT_PUBLIC *key_public,
    TPMI_ALG_HASH hash_alg,
    TPM2B_DIGEST *digest,
    TPM2B_NONCE *policyRef,
    TPMT_SIGNATURE *signature,
    void *userdata);

typedef TSS2_RC (*TSS2_POLICY_CB_EXEC_POLAUTHNV) (
    TPMS_NV_PUBLIC *nv_public,
    TPMI_ALG_HASH hash_alg,
    void *userdata);

typedef TSS2_RC (*TSS2_POLICY_CB_EXEC_POLDUP) (
    TPM2B_NAME *name,
    void *userdata);

typedef TSS2_RC (*TSS2_POLICY_CB_EXEC_POLACTION) (
    const char *action,
    void *userdata);

typedef struct TSS2_POLICY_EXEC_CALLBACKS TSS2_POLICY_EXEC_CALLBACKS;

struct TSS2_POLICY_EXEC_CALLBACKS {
    TSS2_POLICY_CB_EXEC_AUTH              cbauth; /**< Callback to authorize an object
                                                       retrieved by name in keystore */
    void                        *cbauth_userdata;
    TSS2_POLICY_CB_EXEC_LOAD              cbload; /**< Callback to load a key
                                                       retrieved by name in keystore */
    void                        *cbload_userdata;
    TSS2_POLICY_CB_EXEC_POLSEL          cbpolsel; /**< Callback for selection of policy
                                                       branch */
    void                      *cbpolsel_userdata;
    TSS2_POLICY_CB_EXEC_SIGN              cbsign; /**< Callback for policy sign */
    void                        *cbsign_userdata;
    TSS2_POLICY_CB_EXEC_POLAUTH        cbauthpol; /**< Callback for policy authorize */
    void                     *cbauthpol_userdata;
    TSS2_POLICY_CB_EXEC_POLAUTHNV       cbauthnv; /**< Callback for policy authorize nv */
    void                      *cbauthnv_userdata;
    TSS2_POLICY_CB_EXEC_POLDUP             cbdup; /**< Callback for policy duplication
                                                       select */
    void                         *cbdup_userdata;
    TSS2_POLICY_CB_EXEC_POLACTION       cbaction; /**< Callback for policy action */
    void                      *cbaction_userdata;
};

TSS2_RC
Tss2_PolicyInit(
    const char *json_policy,
    TPM2_ALG_ID hash_alg,
    TSS2_POLICY_CTX **policy_ctx);

void
Tss2_PolicyFinalize(
        TSS2_POLICY_CTX **policy);

TSS2_RC
Tss2_PolicySetCalcCallbacks(
    TSS2_POLICY_CTX *policy_ctx,
    TSS2_POLICY_CALC_CALLBACKS *calc_callbacks);

TSS2_RC
Tss2_PolicySetExecCallbacks(
    TSS2_POLICY_CTX *policy_ctx,
    TSS2_POLICY_EXEC_CALLBACKS *exec_callbacks);

TSS2_RC
Tss2_PolicyExecute(
    TSS2_POLICY_CTX *policy_ctx,
    ESYS_CONTEXT *esys_ctx,
    ESYS_TR session);

TSS2_RC
Tss2_PolicyCalculate(
        TSS2_POLICY_CTX *policy_ctx);

TSS2_RC
Tss2_PolicyGetCalculatedJSON(
        TSS2_POLICY_CTX *policy_ctx,
        char *buffer,
        size_t *size);

TSS2_RC
Tss2_PolicyGetDescription(
        TSS2_POLICY_CTX *policy_ctx,
        char *description,
        size_t *size);

TSS2_RC
Tss2_PolicyGetCalculatedDigest(
        TSS2_POLICY_CTX *policy_ctx,
        TPM2B_DIGEST *digest);

#endif /* INCLUDE_TSS2_TSS2_POLICY_H_ */
