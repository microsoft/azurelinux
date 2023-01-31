/* SPDX-License-Identifier: BSD-2-Clause */
/*******************************************************************************
 * Copyright 2018-2019, Fraunhofer SIT sponsored by Infineon Technologies AG
 * All rights reserved.
 *******************************************************************************/
#ifndef IFAPI_POLICY_H
#define IFAPI_POLICY_H

#include <stdint.h>
#include <stdarg.h>
#include <stdbool.h>
#include <sys/stat.h>
#include <json-c/json.h>
#include <json-c/json_util.h>

#include "tss2_esys.h"
#include "tss2_fapi.h"
#include "fapi_int.h"
#include "ifapi_policy_callbacks.h"

TSS2_RC
get_policy_digest_idx(
    TPML_DIGEST_VALUES *digest_values,
    TPMI_ALG_HASH hashAlg,
    size_t *idx);

TSS2_RC
ifapi_compute_policy_digest(
    TPML_PCRVALUES *pcrs,
    TPML_PCR_SELECTION *pcr_selection,
    TPMI_ALG_HASH hash_alg,
    TPM2B_DIGEST *pcr_digest);

static inline void ifapi_policy_ctx_init(FAPI_CONTEXT *context) {

    TSS2_POLICY_CALC_CALLBACKS *callbacks = &context->policy.eval_ctx.callbacks;
    callbacks->cbname = ifapi_get_object_name;
    callbacks->cbname_userdata = context;
    callbacks->cbpublic = ifapi_get_key_public;
    callbacks->cbpublic_userdata = context;
    callbacks->cbnvpublic = ifapi_get_nv_public;
    callbacks->cbnvpublic_userdata = context;
    callbacks->cbpcr = ifapi_read_pcr;
    callbacks->cbpcr_userdata = context;
}

TSS2_RC
ifapi_calculate_tree_ex(
    IFAPI_POLICY_CTX *policyContext,
    IFAPI_POLICY_STORE *pstore,
    IFAPI_IO *io,
    const char *policyPath,
    TPMS_POLICY *policy,
    TPMI_ALG_HASH hash_alg,
    size_t *digest_idx,
    size_t *hash_size);

TSS2_RC
ifapi_execute_tree_ex(
    enum IFAPI_STATE_POLICY *state,
    IFAPI_POLICY_EXEC_CTX *context,
    IFAPI_POLICY_EVAL_INST_CTX *eval_ctx,
    IFAPI_POLICY_STORE *pstore,
    IFAPI_IO *io,
    const char *policyPath,
    TPMS_POLICY *policy,
    ESYS_CONTEXT *esys_ctx,
    TPMI_ALG_HASH hash_alg,
    bool do_flush);

static inline TSS2_RC
ifapi_calculate_tree(
    FAPI_CONTEXT *context,
    const char *policyPath,
    TPMS_POLICY *policy,
    TPMI_ALG_HASH hash_alg,
    size_t *digest_idx,
    size_t *hash_size) {

    return ifapi_calculate_tree_ex(&context->policy,
            &context->pstore,
            &context->io,
            policyPath,
            policy,
            hash_alg,
            digest_idx,
            hash_size);
}

#endif /* IFAPI_POLICY_H */
