/* SPDX-License-Identifier: BSD-2-Clause */
/*******************************************************************************
 * Copyright 2018-2019, Fraunhofer SIT sponsored by Infineon Technologies AG
 * All rights reserved.
 *******************************************************************************/

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <string.h>
#include <stdlib.h>

#include "tss2_mu.h"
#include "fapi_util.h"
#include "fapi_crypto.h"
#include "fapi_policy.h"
#include "ifapi_helpers.h"
#include "ifapi_json_deserialize.h"
#include "tpm_json_deserialize.h"
#define LOGMODULE fapi
#include "util/log.h"
#include "util/aux_util.h"

/** Copy policy digest.
 *
 * One digest is copied from certain position in a policy list to the
 * same position in a second list.
 *
 * @param[out] dest The digest list to which the new value is added.
 * @param[in]  src The digest list with the value to be copied.
 * @param[in]  digest_idx The index of the digest to be copied.
 * @param[in]  hash_size The number of bytes to be copied.
 * @param[in]  txt Text which will be used for additional logging information..
 * @retval TSS2_RC_SUCCESS on success.
 */
static void
copy_policy_digest(TPML_DIGEST_VALUES *dest, TPML_DIGEST_VALUES *src,
                   size_t digest_idx, size_t hash_size, char *txt MAYBE_UNUSED)
{
    memcpy(&dest->digests[digest_idx].digest, &src->digests[digest_idx].digest,
           hash_size);
    dest->digests[digest_idx].hashAlg = src->digests[digest_idx].hashAlg;
    LOGBLOB_DEBUG((uint8_t *)&dest->digests[digest_idx].digest, hash_size,
                  "%s : Copy digest size: %zu", txt, hash_size);
    dest->count = src->count;
}

/** Logdefault policy digest.
 *
 * @param[in] dest The digest to be logged.
 * @param[in] digest_idx The index of the digest to be logged
 * @param[in] hash_size The number of bytes to be logged
 * @param[in] txt Text which will be used for additional logging information.
 */
static void
log_policy_digest(TPML_DIGEST_VALUES *dest MAYBE_UNUSED,
                  size_t digest_idx MAYBE_UNUSED,
                  size_t hash_size MAYBE_UNUSED,
                  char *txt MAYBE_UNUSED)
{
    LOGBLOB_DEBUG((uint8_t *)&dest->digests[digest_idx].digest, hash_size,
                  "Digest %s", txt);
}

/** Calculate a policy digest for a certain PCR selection.
 *
 * From a PCR list the list of PCR values and the corresponding PCR digest
 * is computed. The passed policy digest will be extended with this data
 * and also with the policy command code.
 *
 * @param[in] policy The policy with the list of selected PCRs.
 * @param[in,out] current_digest The digest list which has to be updated.
 * @param[in] current_hash_alg The hash algorithm used for the policy computation.
 *
 * @retval TSS2_RC_SUCCESS on success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE if an internal error occurred.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 */
TSS2_RC
ifapi_compute_policy_pcr(
    TPMS_POLICYPCR *policy,
    TPML_DIGEST_VALUES *current_digest,
    TPMI_ALG_HASH current_hash_alg)
{
    TSS2_RC r = TSS2_RC_SUCCESS;
    IFAPI_CRYPTO_CONTEXT_BLOB *cryptoContext = NULL;
    TPML_PCR_SELECTION pcr_selection;
    size_t digest_idx;
    TPM2B_DIGEST pcr_digest;
    size_t hash_size;

    LOG_TRACE("call");

    if (!(hash_size = ifapi_hash_get_digest_size(current_hash_alg))) {
        goto_error(r, TSS2_FAPI_RC_BAD_VALUE,
                   "Unsupported hash algorithm (%" PRIu16 ")", cleanup,
                   current_hash_alg);
    }

    /* Compute of the index of the current policy in the passed digest list */
    r = get_policy_digest_idx(current_digest, current_hash_alg, &digest_idx);
    return_if_error(r, "Get hash alg for digest.");

    /* Compute PCR selection and pcr digest */
    r = ifapi_compute_policy_digest(policy->pcrs, &pcr_selection,
                                    current_hash_alg, &pcr_digest);
    return_if_error(r, "Compute policy digest and selection.");

    LOG_TRACE("Compute policy pcr");
    r = ifapi_crypto_hash_start(&cryptoContext, current_hash_alg);
    return_if_error(r, "crypto hash start");

    /* Update the passed policy. */
    HASH_UPDATE_BUFFER(cryptoContext,
                       &current_digest->digests[digest_idx].digest, hash_size,
                       r, cleanup);
    HASH_UPDATE(cryptoContext, TPM2_CC, TPM2_CC_PolicyPCR, r, cleanup);
    /* The marshaled version of the digest list will be added. */
    HASH_UPDATE(cryptoContext, TPML_PCR_SELECTION, &pcr_selection, r, cleanup);
    HASH_UPDATE_BUFFER(cryptoContext, &pcr_digest.buffer[0], hash_size, r,
                       cleanup);

    r = ifapi_crypto_hash_finish(&cryptoContext,
                                 (uint8_t *) & current_digest->
                                 digests[digest_idx].digest, &hash_size);
    return_if_error(r, "crypto hash finish");

cleanup:
    if (cryptoContext)
        ifapi_crypto_hash_abort(&cryptoContext);
    return r;
}

/** Calculate a policy digest for a TPM2B object name, and a policy reference.
 *
 * A policy hash based on a passed policy digest, the policy command code,
 * optionally the name, and the policy reference will be computed.
 * The calculation is carried out in two steps. First a hash with the
 * command code and the passed digest, and optionaly the name is computed.
 * This digest, together with the other parameters is used to compute
 * the final policy digest.
 *
 * @param[in] command_code The TPM command code of the policy command.
 * @param[in] name The name of a key or a NV object.
 * @param[in] policyRef The policy reference value.
 * @param[in] hash_size The digest size of the used hash algorithm.
 * @param[in] current_hash_alg The used has algorithm.
 * @param[in,out] digest The policy digest which will be extended.
 *
 * @retval TSS2_RC_SUCCESS on success.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE if an internal error occurred.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 */
static TSS2_RC
calculate_policy_key_param(
    TPM2_CC command_code,
    TPM2B_NAME *name,
    TPM2B_NONCE *policyRef,
    size_t hash_size,
    TPMI_ALG_HASH current_hash_alg,
    TPMU_HA *digest)
{
    TSS2_RC r = TSS2_RC_SUCCESS;
    IFAPI_CRYPTO_CONTEXT_BLOB *cryptoContext = NULL;

    r = ifapi_crypto_hash_start(&cryptoContext, current_hash_alg);
    return_if_error(r, "crypto hash start");

    LOGBLOB_DEBUG((uint8_t *) digest, hash_size, "Digest Start");

    /* First compute hash from passed policy digest and command code
       and optionally the object name */
    HASH_UPDATE_BUFFER(cryptoContext, digest, hash_size, r, cleanup);
    HASH_UPDATE(cryptoContext, TPM2_CC, command_code, r, cleanup);
    if (name && name->size > 0) {
        LOGBLOB_DEBUG(&name->name[0], name->size, "Key name");
        HASH_UPDATE_BUFFER(cryptoContext, &name->name[0],
                           name->size, r, cleanup);
    }
    r = ifapi_crypto_hash_finish(&cryptoContext,
                                 (uint8_t *) digest, &hash_size);
    LOGBLOB_DEBUG((uint8_t *) digest, hash_size, "Digest Finish");
    return_if_error(r, "crypto hash finish");

    /* Use policyRef for second hash computation */
    if (policyRef) {
        r = ifapi_crypto_hash_start(&cryptoContext, current_hash_alg);
        return_if_error(r, "crypto hash start");

        HASH_UPDATE_BUFFER(cryptoContext, digest, hash_size, r, cleanup);
        HASH_UPDATE_BUFFER(cryptoContext, &policyRef->buffer[0],
                           policyRef->size, r, cleanup);
        r = ifapi_crypto_hash_finish(&cryptoContext,
                                     (uint8_t *) digest, &hash_size);
        return_if_error(r, "crypto hash finish");
    }

cleanup:
    if (cryptoContext)
        ifapi_crypto_hash_abort(&cryptoContext);
    return r;
}

/** Calculate a policy digest for a signed policy.
 *
 * Based on the command code, the public key, and the policy reference
 * stored in the policy the new policy digest is computed by the function
 * calculate_policy_key_param().
 *
 * @param[in] policy The policy with the public key and the policy reference.
 * @param[in,out] current_digest The digest list which has to be updated.
 * @param[in] current_hash_alg The hash algorithm used for the policy computation.
 *
 * @retval TSS2_RC_SUCCESS on success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE if an internal error occurred.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 */
TSS2_RC
ifapi_calculate_policy_signed(
    TPMS_POLICYSIGNED *policy,
    TPML_DIGEST_VALUES *current_digest,
    TPMI_ALG_HASH current_hash_alg)
{
    TSS2_RC r = TSS2_RC_SUCCESS;
    size_t digest_idx;
    size_t hash_size;

    LOG_DEBUG("call");

    if (!(hash_size = ifapi_hash_get_digest_size(current_hash_alg))) {
        goto_error(r, TSS2_FAPI_RC_BAD_VALUE,
                   "Unsupported hash algorithm (%" PRIu16 ")", cleanup,
                   current_hash_alg);
    }

    /* Compute of the index of the current policy in the passed digest list */
    r = get_policy_digest_idx(current_digest, current_hash_alg, &digest_idx);
    return_if_error(r, "Get hash alg for digest.");

    r = calculate_policy_key_param(TPM2_CC_PolicySigned,
                                   &policy->publicKey,
                                   &policy->policyRef, hash_size,
                                   current_hash_alg,
                                   &current_digest->digests[digest_idx].digest);
    goto_if_error(r, "crypto hash start", cleanup);

cleanup:
    return r;
}

/** Calculate a policy digest for a policy stored in an approved NV index.
 *
 * Based on the command code, and the computed NV name the new policy digest
 * is computed by the function calculate_policy_key_param().
 *
 * @param[in] policy The policy with the public information of the NV index.
 * @param[in,out] current_digest The digest list which has to be updated.
 * @param[in] current_hash_alg The hash algorithm used for the policy computation.
 *
 * @retval TSS2_RC_SUCCESS on success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE if an internal error occurred.
 */
TSS2_RC
ifapi_calculate_policy_authorize_nv(
    TPMS_POLICYAUTHORIZENV *policy,
    TPML_DIGEST_VALUES *current_digest,
    TPMI_ALG_HASH current_hash_alg)
{
    TSS2_RC r = TSS2_RC_SUCCESS;
    size_t digest_idx;
    size_t hash_size;
    TPM2B_NAME nv_name;

    LOG_DEBUG("call");

    /* Written flag has to be set for policy calculation, because during
       policy execution it will be set. */
    policy->nvPublic.attributes |= TPMA_NV_WRITTEN;

    r = ifapi_nv_get_name(&policy->nvPublic, &nv_name);
    return_if_error(r, "Compute NV name");

    if (!(hash_size = ifapi_hash_get_digest_size(current_hash_alg))) {
        goto_error(r, TSS2_FAPI_RC_BAD_VALUE,
                   "Unsupported hash algorithm (%" PRIu16 ")", cleanup,
                   current_hash_alg);
    }

    /* Compute of the index of the current policy in the passed digest list */
    r = get_policy_digest_idx(current_digest, current_hash_alg, &digest_idx);
    return_if_error(r, "Get hash alg for digest.");

    r = calculate_policy_key_param(TPM2_CC_PolicyAuthorizeNV,
                                   &nv_name,
                                   NULL, hash_size, current_hash_alg,
                                   &current_digest->digests[digest_idx].digest);
    goto_if_error(r, "crypto hash start", cleanup);

cleanup:
    return r;
}

/** Calculate a policy digest to allow duplication force a selected new parent.
 *
 * Based on the command code, the name of the new parent, and the include object
 * switch the new policy digest is computed.
 *
 * @param[in] policy The policy with the new parent information.
 * @param[in,out] current_digest The digest list which has to be updated.
 * @param[in] current_hash_alg The hash algorithm used for the policy computation.
 *
 * @retval TSS2_RC_SUCCESS on success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE if an internal error occurred.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 */
TSS2_RC
ifapi_calculate_policy_duplicate(
    TPMS_POLICYDUPLICATIONSELECT *policy,
    TPML_DIGEST_VALUES *current_digest,
    TPMI_ALG_HASH current_hash_alg)
{
    TSS2_RC r = TSS2_RC_SUCCESS;
    IFAPI_CRYPTO_CONTEXT_BLOB *cryptoContext = NULL;
    size_t digest_idx;
    size_t hash_size;

    LOG_DEBUG("call");

    if (!(hash_size = ifapi_hash_get_digest_size(current_hash_alg))) {
        goto_error(r, TSS2_FAPI_RC_BAD_VALUE,
                   "Unsupported hash algorithm (%" PRIu16 ")", cleanup,
                   current_hash_alg);
    }

    /* Compute of the index of the current policy in the passed digest list */
    r = get_policy_digest_idx(current_digest, current_hash_alg, &digest_idx);
    return_if_error(r, "Get hash alg for digest.");

    LOG_TRACE("Compute policy");
    r = ifapi_crypto_hash_start(&cryptoContext, current_hash_alg);
    return_if_error(r, "crypto hash start");

    /* Update the policy digest */
    HASH_UPDATE_BUFFER(cryptoContext,
                       &current_digest->digests[digest_idx].digest, hash_size,
                       r, cleanup);
    HASH_UPDATE(cryptoContext, TPM2_CC, TPM2_CC_PolicyDuplicationSelect, r,
                cleanup);
    LOGBLOB_DEBUG(&policy->newParentName.name[0], policy->newParentName.size,
                  "Policy Duplicate Parent Name");
    HASH_UPDATE_BUFFER(cryptoContext, &policy->newParentName.name[0],
                       policy->newParentName.size, r, cleanup);
    HASH_UPDATE(cryptoContext, BYTE, policy->includeObject, r, cleanup);

    r = ifapi_crypto_hash_finish(&cryptoContext,
                                 (uint8_t *) & current_digest->
                                 digests[digest_idx].digest, &hash_size);
    return_if_error(r, "crypto hash finish");

    LOGBLOB_DEBUG((uint8_t *) & current_digest->digests[digest_idx].digest,
                  hash_size, "Policy Duplicate digest");

cleanup:
    if (cryptoContext)
        ifapi_crypto_hash_abort(&cryptoContext);
    return r;
}

/** Calculate a policy digest for a placeholder policy.
 *
 * The placeholder policy can be extended during execution by a
 * signed policy, which can be verified by using the parameters of
 * this placeholder policy.
 * Based on the command code, the key name of the signing key and
 * a policy reference the new policy digest is computed by the
 * function calculate_policy_key_param().
 *
 * @param[in] policy The policy with the name of the public key and the
 *                   policy reference.
 * @param[in,out] current_digest The digest list which has to be updated.
 * @param[in] current_hash_alg The hash algorithm used for the policy computation.
 *
 * @retval TSS2_RC_SUCCESS on success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE if an internal error occurred.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 */
TSS2_RC
ifapi_calculate_policy_authorize(
    TPMS_POLICYAUTHORIZE *policy,
    TPML_DIGEST_VALUES *current_digest,
    TPMI_ALG_HASH current_hash_alg)
{
    TSS2_RC r = TSS2_RC_SUCCESS;
    size_t digest_idx;
    size_t hash_size;

    LOG_DEBUG("call");

    if (!(hash_size = ifapi_hash_get_digest_size(current_hash_alg))) {
        goto_error(r, TSS2_FAPI_RC_BAD_VALUE,
                   "Unsupported hash algorithm (%" PRIu16 ")", cleanup,
                   current_hash_alg);
    }

    /* Compute of the index of the current policy in the passed digest list */
    r = get_policy_digest_idx(current_digest, current_hash_alg, &digest_idx);
    return_if_error(r, "Get hash alg for digest.");

    r = calculate_policy_key_param(TPM2_CC_PolicyAuthorize,
                                   &policy->keyName,
                                   &policy->policyRef, hash_size,
                                   current_hash_alg,
                                   &current_digest->digests[digest_idx].digest);
    goto_if_error(r, "crypto hash start", cleanup);

cleanup:
    return r;
}

/** Calculate a policy for adding secret-based authorization.
 *
 * During execution proving the knowledge of the secrect auth value of a certain
 * object is required. The name of this object and a policy reference is used
 * for policy calculation.
 * Based on the command code, the object name and a policy reference the new
 * policy digest is computed by the function calculate_policy_key_param().
 *
 * @param[in] policy The policy with the object name of the object to be
 *            authorized  and the policy reference.
 * @param[in,out] current_digest The digest list which has to be updated.
 * @param[in] current_hash_alg The hash algorithm used for the policy computation.
 *
 * @retval TSS2_RC_SUCCESS on success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE if an internal error occurred.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 */
TSS2_RC
ifapi_calculate_policy_secret(
    TPMS_POLICYSECRET *policy,
    TPML_DIGEST_VALUES *current_digest,
    TPMI_ALG_HASH current_hash_alg)
{
    TSS2_RC r = TSS2_RC_SUCCESS;
    size_t digest_idx;
    size_t hash_size;

    LOG_DEBUG("call");

    if (!(hash_size = ifapi_hash_get_digest_size(current_hash_alg))) {
        goto_error(r, TSS2_FAPI_RC_BAD_VALUE,
                   "Unsupported hash algorithm (%" PRIu16 ")", cleanup,
                   current_hash_alg);
    }

    /* Compute of the index of the current policy in the passed digest list */
    r = get_policy_digest_idx(current_digest, current_hash_alg, &digest_idx);
    return_if_error(r, "Get hash alg for digest.");

    /* Update the policy */
    r = calculate_policy_key_param(TPM2_CC_PolicySecret,
                                   (TPM2B_NAME *)&policy->objectName,
                                   &policy->policyRef, hash_size,
                                   current_hash_alg,
                                   &current_digest->digests[digest_idx].digest);
    goto_if_error(r, "crypto hash start", cleanup);

cleanup:
    return r;
}

/** Calculate a policy for for comparing current TPM timers with the policy.
 *
 * The timer value and the operation for comparison defined in the policy will
 * bu used to update the policy digest.
 * The offset which is supported by the TPM policy for FAPI will be 0.
 *
 * @param[in] policy The policy with the timer value and the operation for
 *            comparison.
 * @param[in,out] current_digest The digest list which has to be updated.
 * @param[in] current_hash_alg The hash algorithm used for the policy computation.
 *
 * @retval TSS2_RC_SUCCESS on success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE if an internal error occurred.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 */
TSS2_RC
ifapi_calculate_policy_counter_timer(
    TPMS_POLICYCOUNTERTIMER *policy,
    TPML_DIGEST_VALUES *current_digest,
    TPMI_ALG_HASH current_hash_alg)
{
    TSS2_RC r = TSS2_RC_SUCCESS;
    IFAPI_CRYPTO_CONTEXT_BLOB *cryptoContext = NULL;
    size_t digest_idx;
    size_t hash_size;
    TPM2B_DIGEST counter_timer_hash;

    LOG_DEBUG("call");

    if (!(hash_size = ifapi_hash_get_digest_size(current_hash_alg))) {
        goto_error(r, TSS2_FAPI_RC_BAD_VALUE,
                   "Unsupported hash algorithm (%" PRIu16 ")", cleanup,
                   current_hash_alg);
    }

    /* Compute of the index of the current policy in the passed digest list */
    r = get_policy_digest_idx(current_digest, current_hash_alg, &digest_idx);
    return_if_error(r, "Get hash alg for digest.");

    r = ifapi_crypto_hash_start(&cryptoContext, current_hash_alg);
    return_if_error(r, "crypto hash start");

    /* Compute a has value from the offset, the timer value and the operation. */
    HASH_UPDATE_BUFFER(cryptoContext, &policy->operandB.buffer[0],
                       policy->operandB.size, r, cleanup);
    HASH_UPDATE(cryptoContext, UINT16, policy->offset, r, cleanup);
    HASH_UPDATE(cryptoContext, UINT16, policy->operation, r, cleanup);

    r = ifapi_crypto_hash_finish(&cryptoContext,
                                 (uint8_t *) &counter_timer_hash.buffer[0], &hash_size);
    return_if_error(r, "crypto hash finish");

    /* Extend the policy digest from the hash value computed above and the
       command code. */
    r = ifapi_crypto_hash_start(&cryptoContext, current_hash_alg);
    return_if_error(r, "crypto hash start");

    HASH_UPDATE_BUFFER(cryptoContext,
                       &current_digest->digests[digest_idx].digest, hash_size,
                       r, cleanup);
    HASH_UPDATE(cryptoContext, TPM2_CC, TPM2_CC_PolicyCounterTimer, r, cleanup);
    HASH_UPDATE_BUFFER(cryptoContext, &counter_timer_hash.buffer[0],
                       hash_size, r, cleanup);
    r = ifapi_crypto_hash_finish(&cryptoContext,
                                 (uint8_t *) &current_digest->digests[digest_idx].digest,
                                 &hash_size);
cleanup:
    if (cryptoContext)
        ifapi_crypto_hash_abort(&cryptoContext);
    return r;
}

/** Update policy if only the command codes are used.
 *
 * Some simple policies use onle one or two command codes for policy calculation.
 *
 * @param[in] command_code1 The first command code for policy extension.
 *            Can be NULL.
 * @param[in] command_code2 The second command code for policy extension.
 *            Can be NULL.
 * @param[in,out] current_digest The digest list which has to be updated.
 * @param[in] current_hash_alg The hash algorithm used for the policy computation.
 *
 * @retval TSS2_RC_SUCCESS on success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE if an internal error occurred.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 */
TSS2_RC
ifapi_calculate_simple_policy(
    TPM2_CC command_code1,
    TPM2_CC command_code2,
    TPML_DIGEST_VALUES *current_digest,
    TPMI_ALG_HASH current_hash_alg)
{
    TSS2_RC r = TSS2_RC_SUCCESS;
    IFAPI_CRYPTO_CONTEXT_BLOB *cryptoContext = NULL;
    size_t digest_idx;
    size_t hash_size;

    LOG_DEBUG("call");

    if (!(hash_size = ifapi_hash_get_digest_size(current_hash_alg))) {
        goto_error(r, TSS2_FAPI_RC_BAD_VALUE,
                   "Unsupported hash algorithm (%" PRIu16 ")", cleanup,
                   current_hash_alg);
    }

    /* Compute of the index of the current policy in the passed digest list */
    r = get_policy_digest_idx(current_digest, current_hash_alg, &digest_idx);
    return_if_error(r, "Get hash alg for digest.");

    /* Update the policy */
    r = ifapi_crypto_hash_start(&cryptoContext, current_hash_alg);
    return_if_error(r, "crypto hash start");

    HASH_UPDATE_BUFFER(cryptoContext,
                       &current_digest->digests[digest_idx].digest, hash_size,
                       r, cleanup);
    if (command_code1) {
        HASH_UPDATE(cryptoContext, TPM2_CC, command_code1, r, cleanup);
    }
    if (command_code2) {
        HASH_UPDATE(cryptoContext, TPM2_CC, command_code2, r, cleanup);
    }
    r = ifapi_crypto_hash_finish(&cryptoContext,
                                 (uint8_t *) &current_digest->digests[digest_idx].digest,
                                 &hash_size);

cleanup:
    if (cryptoContext)
        ifapi_crypto_hash_abort(&cryptoContext);
    return r;
}

/** Update policy with command code policy physical presence.
 *
 * The policy will be updated with the function ifapi_calculate_simple_policy()
 *
 * @param[in] policy The policy physical presence.
 * @param[in,out] current_digest The digest list which has to be updated.
 * @param[in] current_hash_alg The hash algorithm used for the policy computation.
 *
 * @retval TSS2_RC_SUCCESS on success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE if an internal error occurred.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 */
TSS2_RC
ifapi_calculate_policy_physical_presence(
    TPML_DIGEST_VALUES *current_digest,
    TPMI_ALG_HASH current_hash_alg)
{
    TSS2_RC r = TSS2_RC_SUCCESS;

    LOG_DEBUG("call");

    r = ifapi_calculate_simple_policy(TPM2_CC_PolicyPhysicalPresence, 0,
            current_digest, current_hash_alg);
    return_if_error(r, "Calculate policy for command code.");

    return r;
}

/** Update policy with command code of policy auth value.
 *
 * The policy will be updated with the function ifapi_calculate_simple_policy()
 *
 * @param[in,out] current_digest The digest list which has to be updated.
 * @param[in] current_hash_alg The hash algorithm used for the policy computation.
 *
 * @retval TSS2_RC_SUCCESS on success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE if an internal error occurred.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 */
TSS2_RC
ifapi_calculate_policy_auth_value(
    TPML_DIGEST_VALUES *current_digest,
    TPMI_ALG_HASH current_hash_alg)
{
    TSS2_RC r = TSS2_RC_SUCCESS;

    LOG_DEBUG("call");

    r = ifapi_calculate_simple_policy(TPM2_CC_PolicyAuthValue, 0,
            current_digest, current_hash_alg);
    return_if_error(r, "Calculate policy auth value.");

    return r;
}

/** Update policy with the command code of policy password.
 *
 * The policy will be updated with the function ifapi_calculate_simple_policy()
 *
 * @param[in,out] current_digest The digest list which has to be updated.
 * @param[in] current_hash_alg The hash algorithm used for the policy computation.
 *
 * @retval TSS2_RC_SUCCESS on success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE if an internal error occurred.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 */
TSS2_RC
ifapi_calculate_policy_password(
    TPML_DIGEST_VALUES *current_digest,
    TPMI_ALG_HASH current_hash_alg)
{
    TSS2_RC r = TSS2_RC_SUCCESS;

    LOG_DEBUG("call");

    r = ifapi_calculate_simple_policy(TPM2_CC_PolicyAuthValue, 0,
            current_digest, current_hash_alg);
    return_if_error(r, "Calculate policy password.");

    return r;
}

/** Update policy command code with a command code defined in the policy.
 *
 * For the update two command codes will be used. The command code of
 * policy command code and the passed command code.
 * The policy will be updated with the function ifapi_calculate_simple_policy()
 *
 * @param[in] policy The policy command code with the second command code.
 * @param[in,out] current_digest The digest list which has to be updated.
 * @param[in] current_hash_alg The hash algorithm used for the policy computation.
 *
 * @retval TSS2_RC_SUCCESS on success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE if an internal error occurred.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 */
TSS2_RC
ifapi_calculate_policy_command_code(
    TPMS_POLICYCOMMANDCODE *policy,
    TPML_DIGEST_VALUES *current_digest,
    TPMI_ALG_HASH current_hash_alg)
{
    TSS2_RC r = TSS2_RC_SUCCESS;

    LOG_DEBUG("call");

    r = ifapi_calculate_simple_policy(TPM2_CC_PolicyCommandCode, policy->code,
            current_digest, current_hash_alg);
    return_if_error(r, "Calculate policy for command code.");

    return r;
}

/** Compute policy if only a digest and a command code are needed for extension.
 *
 * @param[in] digest the digest which will be used for policy extension.
 * @param[in,out] current_digest The digest list which has to be updated.
 * @param[in] current_hash_alg The hash algorithm used for the policy computation.
 * @param[in] command_code The compute of the command which did compute the digest.
 *
 * @retval TSS2_RC_SUCCESS on success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE if an internal error occurred.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 */
TSS2_RC
ifapi_calculate_policy_digest_hash(
    TPM2B_DIGEST *digest,
    TPML_DIGEST_VALUES *current_digest,
    TPMI_ALG_HASH current_hash_alg,
    TPM2_CC command_code)
{
    TSS2_RC r = TSS2_RC_SUCCESS;
    IFAPI_CRYPTO_CONTEXT_BLOB *cryptoContext = NULL;
    size_t digest_idx;
    size_t hash_size;

    LOG_DEBUG("call");

    if (!(hash_size = ifapi_hash_get_digest_size(current_hash_alg))) {
        goto_error(r, TSS2_FAPI_RC_BAD_VALUE,
                   "Unsupported hash algorithm (%" PRIu16 ")", cleanup,
                   current_hash_alg);
    }

    /* Compute of the index of the current policy in the passed digest list */
    r = get_policy_digest_idx(current_digest, current_hash_alg, &digest_idx);
    return_if_error(r, "Get hash alg for digest.");

    /* Update the policy. */
    r = ifapi_crypto_hash_start(&cryptoContext, current_hash_alg);
    return_if_error(r, "crypto hash start");

    HASH_UPDATE_BUFFER(cryptoContext,
                       &current_digest->digests[digest_idx].digest, hash_size,
                       r, cleanup);
    HASH_UPDATE(cryptoContext, TPM2_CC, command_code, r, cleanup);
    HASH_UPDATE_BUFFER(cryptoContext, &digest->buffer[0],
                       digest->size, r, cleanup);
    r = ifapi_crypto_hash_finish(&cryptoContext,
                                 (uint8_t *) &current_digest->digests[digest_idx].digest,
                                 &hash_size);
cleanup:
    if (cryptoContext)
        ifapi_crypto_hash_abort(&cryptoContext);
    return r;
}

/** Compute policy bound to a specific set of TPM entities.
 *
 * The policy digest will be updated with the function
 * ifapi_calculate_policy_digest_hash() which will add the hash of the
 * entity name list.
 *
 * @param[in] policy The policy with the list of entity names.
 * @param[in,out] current_digest The digest list which has to be updated.
 * @param[in] current_hash_alg The hash algorithm used for the policy computation.
 *
 * @retval TSS2_RC_SUCCESS on success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE if an internal error occurred.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 */
TSS2_RC
ifapi_calculate_policy_name_hash(
    TPMS_POLICYNAMEHASH *policy,
    TPML_DIGEST_VALUES *current_digest,
    TPMI_ALG_HASH current_hash_alg)
{
    TSS2_RC r = TSS2_RC_SUCCESS;
    IFAPI_CRYPTO_CONTEXT_BLOB *cryptoContext = NULL;
    size_t hash_size;
    size_t i;

    LOG_DEBUG("call");

    if (!(hash_size = ifapi_hash_get_digest_size(current_hash_alg))) {
        goto_error(r, TSS2_FAPI_RC_BAD_VALUE,
                   "Unsupported hash algorithm (%" PRIu16 ")", cleanup,
                   current_hash_alg);
    }

    /* Compute of the index of the current policy in the passed digest list */
    r = ifapi_crypto_hash_start(&cryptoContext, current_hash_alg);
    return_if_error(r, "crypto hash start");

    /* Compute name hash from the list of object names */
    for (i = 0; i <= policy->count; i++) {
        HASH_UPDATE_BUFFER(cryptoContext, &policy->objectNames[i].name[0],
                           policy->objectNames[i].size, r,
                           cleanup);
    }
    r = ifapi_crypto_hash_finish(&cryptoContext,
                                 (uint8_t *) &policy->nameHash.buffer[0],
                                 &hash_size);
    return_if_error(r, "crypto hash finish");

    policy->nameHash.size = hash_size;

    /* Update the policy with the computed hash value of the name list and
       the command code. */
    r = ifapi_calculate_policy_digest_hash(&policy->nameHash,
                                           current_digest,
                                           current_hash_alg, TPM2_CC_PolicyNameHash);
    return_if_error(r, "Calculate digest hash for policy");

cleanup:
    if (cryptoContext)
        ifapi_crypto_hash_abort(&cryptoContext);
    return r;
}

/** Compute policy bound to a specific command and command parameters.
 *
 * The cp hash value and the command code will be updated by the
 * function ifapi_calculate_policy_digest_hash().
 *
 * @param[in] policy The policy with the cp hash value.
 * @param[in,out] current_digest The digest list which has to be updated.
 * @param[in] current_hash_alg The hash algorithm used for the policy computation.
 *
 * @retval TSS2_RC_SUCCESS on success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE if an internal error occurred.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 */
TSS2_RC
ifapi_calculate_policy_cp_hash(
    TPMS_POLICYCPHASH *policy,
    TPML_DIGEST_VALUES *current_digest,
    TPMI_ALG_HASH current_hash_alg)
{
    TSS2_RC r = TSS2_RC_SUCCESS;

    LOG_DEBUG("call");

    r = ifapi_calculate_policy_digest_hash(&policy->cpHash,
                                           current_digest, current_hash_alg,
                                           TPM2_CC_PolicyCpHash);
    return_if_error(r, "Calculate digest hash for policy");

    return r;
}

/** Compute policy which limits authorization to a specific locality.
 *
 * @param[in] policy The policy with the locality.
 * @param[in,out] current_digest The digest list which has to be updated.
 * @param[in] current_hash_alg The hash algorithm used for the policy computation.
 *
 * @retval TSS2_RC_SUCCESS on success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE if an internal error occurred.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 */
TSS2_RC
ifapi_calculate_policy_locality(
    TPMS_POLICYLOCALITY *policy,
    TPML_DIGEST_VALUES *current_digest,
    TPMI_ALG_HASH current_hash_alg)
{
    TSS2_RC r = TSS2_RC_SUCCESS;
    IFAPI_CRYPTO_CONTEXT_BLOB *cryptoContext = NULL;
    size_t digest_idx;
    size_t hash_size;

    LOG_DEBUG("call");

    if (!(hash_size = ifapi_hash_get_digest_size(current_hash_alg))) {
        goto_error(r, TSS2_FAPI_RC_BAD_VALUE,
                   "Unsupported hash algorithm (%" PRIu16 ")", cleanup,
                   current_hash_alg);
    }

    /* Compute of the index of the current policy in the passed digest list */
    r = get_policy_digest_idx(current_digest, current_hash_alg, &digest_idx);
    return_if_error(r, "Get hash alg for digest.");

    /* Update the policy */
    r = ifapi_crypto_hash_start(&cryptoContext, current_hash_alg);
    return_if_error(r, "crypto hash start");

    HASH_UPDATE_BUFFER(cryptoContext,
                       &current_digest->digests[digest_idx].digest, hash_size,
                       r, cleanup);
    HASH_UPDATE(cryptoContext, TPM2_CC, TPM2_CC_PolicyLocality, r, cleanup);
    HASH_UPDATE(cryptoContext, BYTE, policy->locality, r, cleanup);
    r = ifapi_crypto_hash_finish(&cryptoContext,
                                 (uint8_t *) & current_digest->
                                 digests[digest_idx].digest, &hash_size);

cleanup:
    if (cryptoContext)
        ifapi_crypto_hash_abort(&cryptoContext);
    return r;
}

/** Compute policy bound to bound to the TPMA_NV_WRITTEN attributes.
 *
 * The expected value of the NV written attribute is part of the policy.
 *
 * @param[in] policy The policy with the expected attribute value.
 * @param[in,out] current_digest The digest list which has to be updated.
 * @param[in] current_hash_alg The hash algorithm used for the policy computation.
 *
 * @retval TSS2_RC_SUCCESS on success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE if an internal error occurred.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 */
TSS2_RC
ifapi_calculate_policy_nv_written(
    TPMS_POLICYNVWRITTEN *policy,
    TPML_DIGEST_VALUES *current_digest,
    TPMI_ALG_HASH current_hash_alg)
{
    TSS2_RC r = TSS2_RC_SUCCESS;
    IFAPI_CRYPTO_CONTEXT_BLOB *cryptoContext = NULL;
    size_t digest_idx;
    size_t hash_size;

    LOG_DEBUG("call");

    if (!(hash_size = ifapi_hash_get_digest_size(current_hash_alg))) {
        goto_error(r, TSS2_FAPI_RC_BAD_VALUE,
                   "Unsupported hash algorithm (%" PRIu16 ")", cleanup,
                   current_hash_alg);
    }

    /* Compute of the index of the current policy in the passed digest list */
    r = get_policy_digest_idx(current_digest, current_hash_alg, &digest_idx);
    return_if_error(r, "Get hash alg for digest.");

    /* Update the policy */
    r = ifapi_crypto_hash_start(&cryptoContext, current_hash_alg);
    return_if_error(r, "crypto hash start");

    HASH_UPDATE_BUFFER(cryptoContext,
                       &current_digest->digests[digest_idx].digest, hash_size,
                       r, cleanup);
    HASH_UPDATE(cryptoContext, TPM2_CC, TPM2_CC_PolicyNvWritten, r, cleanup);
    /* Update the expected attribute value. */
    HASH_UPDATE(cryptoContext, BYTE, policy->writtenSet, r, cleanup);
    r = ifapi_crypto_hash_finish(&cryptoContext,
                                 (uint8_t *) & current_digest->
                                 digests[digest_idx].digest, &hash_size);

cleanup:
    if (cryptoContext)
        ifapi_crypto_hash_abort(&cryptoContext);
    return r;
}

/** Compute policy bound to the content of an NV index.
 *
 * The value used for comparison, the compare operation and an
 * offset for the NV index are part of the policy.
 *
 * @param[in] policy The policy with the expected values used for comparison.
 * @param[in,out] current_digest The digest list which has to be updated.
 * @param[in] current_hash_alg The hash algorithm used for the policy computation.
 *
 * @retval TSS2_RC_SUCCESS on success.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE if an internal error occurred.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 */
TSS2_RC
ifapi_calculate_policy_nv(
    TPMS_POLICYNV *policy,
    TPML_DIGEST_VALUES *current_digest,
    TPMI_ALG_HASH current_hash_alg)
{
    TSS2_RC r = TSS2_RC_SUCCESS;
    IFAPI_CRYPTO_CONTEXT_BLOB *cryptoContext = NULL;
    TPM2B_NAME nv_name;
    size_t hash_size;
    TPM2B_DIGEST nv_hash;
    size_t digest_idx;

    LOG_DEBUG("call");

    memset(&nv_name, 0, sizeof(TPM2B_NAME));

    /* Written flag has to be set for policy calculation, because during
       policy execution it will be set. */
    policy->nvPublic.attributes |= TPMA_NV_WRITTEN;

    /* Compute NV name from public info */

    r = ifapi_nv_get_name(&policy->nvPublic, &nv_name);
    return_if_error(r, "Compute NV name");

    /* Compute of the index of the current policy in the passed digest list */
    r = get_policy_digest_idx(current_digest, current_hash_alg, &digest_idx);
    return_if_error(r, "Get hash alg for digest.");

    r = ifapi_crypto_hash_start(&cryptoContext, current_hash_alg);
    return_if_error(r, "crypto hash start");

    /* Compute the hash for the compare operation. */
    HASH_UPDATE_BUFFER(cryptoContext, &policy->operandB.buffer[0],
                       policy->operandB.size, r, cleanup);
    HASH_UPDATE(cryptoContext, UINT16, policy->offset, r, cleanup);
    HASH_UPDATE(cryptoContext, UINT16, policy->operation, r, cleanup);
    r = ifapi_crypto_hash_finish(&cryptoContext,
                                 (uint8_t *) &nv_hash.buffer[0], &hash_size);
    return_if_error(r, "crypto hash finish");

    nv_hash.size = hash_size;

    /* Update the policy with the hash of the compare operation and the NV name. */
    r = ifapi_crypto_hash_start(&cryptoContext, current_hash_alg);
    return_if_error(r, "crypto hash start");

    HASH_UPDATE_BUFFER(cryptoContext,
                       &current_digest->digests[digest_idx].digest, hash_size,
                       r, cleanup);
    HASH_UPDATE(cryptoContext, TPM2_CC, TPM2_CC_PolicyNV, r, cleanup);
    HASH_UPDATE_BUFFER(cryptoContext, &nv_hash.buffer[0], nv_hash.size, r, cleanup)
    HASH_UPDATE_BUFFER(cryptoContext, &nv_name.name[0], nv_name.size, r, cleanup);
    r = ifapi_crypto_hash_finish(&cryptoContext,
                                 (uint8_t *) &current_digest->digests[digest_idx].digest,
                                 &hash_size);
    return_if_error(r, "crypto hash finish");

cleanup:
    if (cryptoContext)
        ifapi_crypto_hash_abort(&cryptoContext);
    return r;
}

/** Compute a list of policies to enable authorization options.
 *
 * First the policy digest will be computed for every branch.
 * After that the policy digest will be reset to zero and extended by the
 * list of computed policy digests of the branches.
 *
 * @param[in] policyOr The policy with the possible policy branches.
 * @param[in,out] current_digest The digest list which has to be updated.
 * @param[in] hash_alg The hash algorithm used for the policy computation.
 * @param[in] hash_size The size of the policy digest.
 * @param[in] digest_idx The index of the current policy in the passed digest list.
 *
 * @retval TSS2_RC_SUCCESS on success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE if an internal error occurred.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 */
TSS2_RC
ifapi_calculate_policy_or(
    TPMS_POLICYOR *policyOr,
    TPML_DIGEST_VALUES *current_digest,
    TPMI_ALG_HASH hash_alg,
    size_t hash_size,
    size_t digest_idx)
{
    size_t i;
    TSS2_RC r = TSS2_RC_SUCCESS;
    IFAPI_CRYPTO_CONTEXT_BLOB *cryptoContext = NULL;

    for (i = 0; i < policyOr->branches->count; i++) {
        /* Compute the policy digest for every branch. */
        copy_policy_digest(&policyOr->branches->authorizations[i].policyDigests,
                           current_digest, digest_idx, hash_size,
                           "Copy or digest");

        r = ifapi_calculate_policy(policyOr->branches->authorizations[i].policy,
                                   &policyOr->branches->authorizations[i].
                                   policyDigests, hash_alg, hash_size,
                                   digest_idx);
        log_policy_digest(&policyOr->branches->authorizations[i].policyDigests,
                          digest_idx, hash_size, "Branch digest");

        return_if_error(r, "Compute policy.");
    }
    /* Reset the or policy digest because the digest is included in all sub policies */
    memset(&current_digest->digests[digest_idx], 0, hash_size);
    r = ifapi_crypto_hash_start(&cryptoContext, hash_alg);
    return_if_error(r, "crypto hash start");
    r = ifapi_crypto_hash_update(cryptoContext, (const uint8_t *)
                                 &current_digest->digests[digest_idx].digest,
                                 hash_size);
    goto_if_error(r, "crypto hash update", cleanup);

    /* Start with the update of the reset digest. */
    uint8_t buffer[sizeof(TPM2_CC)];
    size_t offset = 0;
    r = Tss2_MU_TPM2_CC_Marshal(TPM2_CC_PolicyOR,
                                &buffer[0], sizeof(TPM2_CC), &offset);
    goto_if_error(r, "Marshal cc", cleanup);

    r = ifapi_crypto_hash_update(cryptoContext,
                                 (const uint8_t *)&buffer[0], sizeof(TPM2_CC));
    goto_if_error(r, "crypto hash update", cleanup);

    /* Update the digest with the complete list of computed digests of the branches. */
    for (i = 0; i < policyOr->branches->count; i++) {
        r = ifapi_crypto_hash_update(cryptoContext, (const uint8_t *)
                                     &policyOr->branches->authorizations[i]
                                     .policyDigests.digests[digest_idx].digest,
                                     hash_size);
        log_policy_digest(&policyOr->branches->authorizations[i].policyDigests,
                          digest_idx, hash_size, "Or branch");
        current_digest->count =
            policyOr->branches->authorizations[i].policyDigests.count;
        goto_if_error(r, "crypto hash update", cleanup);
    }
    current_digest->digests[digest_idx].hashAlg = hash_alg;
    r = ifapi_crypto_hash_finish(&cryptoContext,
                                 (uint8_t *) & current_digest->
                                 digests[digest_idx].digest, &hash_size);
    log_policy_digest(current_digest, digest_idx, hash_size, "Final or digest");
    goto_if_error(r, "crypto hash finish", cleanup);

cleanup:
    if (cryptoContext)
        ifapi_crypto_hash_abort(&cryptoContext);
    return r;
}

/** Calculate a policy digest for policy template.
 *
 * The template hash will be derived from template_public if no template hash
 * is provided.
 *
 * @param[in] policy The policy with the template hash or the public data used to
 *            compute the template hash.
 * @param[in,out] current_digest The digest list which has to be updated.
 * @param[in] current_hash_alg The hash algorithm used for the policy computation.
 *
 * @retval TSS2_RC_SUCCESS on success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE if an internal error occurred.
 */
TSS2_RC
ifapi_calculate_policy_template(
    TPMS_POLICYTEMPLATE *policy,
    TPML_DIGEST_VALUES *current_digest,
    TPMI_ALG_HASH current_hash_alg)

{
    TSS2_RC r = TSS2_RC_SUCCESS;
    size_t digest_idx;
    size_t hash_size;
    TPM2B_DIGEST computed_template_hash;
    TPM2B_DIGEST *used_template_hash;
    IFAPI_CRYPTO_CONTEXT_BLOB *cryptoContext = NULL;
    uint8_t buffer[sizeof(TPM2B_PUBLIC)];
    size_t offset = 0;
    size_t digest_size;

    LOG_DEBUG("call");

    if (!(hash_size = ifapi_hash_get_digest_size(current_hash_alg))) {
        goto_error(r, TSS2_FAPI_RC_BAD_VALUE,
                   "Unsupported hash algorithm (%" PRIu16 ")", cleanup,
                   current_hash_alg);
    }

    /* Compute of the index of the current policy in the passed digest list */
    r = get_policy_digest_idx(current_digest, current_hash_alg, &digest_idx);
    return_if_error(r, "Get hash alg for digest.");

    if (policy->templateHash.size == 0) {
        used_template_hash = &computed_template_hash;
        r = Tss2_MU_TPMT_PUBLIC_Marshal(&policy->templatePublic.publicArea,
                                        &buffer[0], sizeof(TPMT_PUBLIC), &offset);
        return_if_error(r, "Marshaling TPMT_PUBLIC");

        r = ifapi_crypto_hash_start(&cryptoContext, current_hash_alg);
        return_if_error(r, "crypto hash start");

        HASH_UPDATE_BUFFER(cryptoContext,
                           &buffer[0], offset,
                           r, cleanup);
        r = ifapi_crypto_hash_finish(&cryptoContext,
                                     &used_template_hash->buffer[0],
                                     &digest_size);
        goto_if_error(r, "crypto hash finish", cleanup);
        used_template_hash->size = digest_size;
    } else {
        used_template_hash = &policy->templateHash;
    }

    LOG_TRACE("Compute policy template");
    r = ifapi_crypto_hash_start(&cryptoContext, current_hash_alg);
    return_if_error(r, "crypto hash start");

    HASH_UPDATE(cryptoContext, TPM2_CC, TPM2_CC_PolicyTemplate, r,
                cleanup);
    HASH_UPDATE_BUFFER(cryptoContext, &used_template_hash->buffer[0],
                       used_template_hash->size, r, cleanup);
    r = ifapi_crypto_hash_finish(&cryptoContext,
                                 (uint8_t *) & current_digest->
                                 digests[digest_idx].digest, &hash_size);
    return_if_error(r, "crypto hash finish");

    LOGBLOB_DEBUG((uint8_t *) & current_digest->digests[digest_idx].digest,
                  hash_size, "Policy Duplicate digest");

cleanup:
    if (cryptoContext)
        ifapi_crypto_hash_abort(&cryptoContext);
    return r;
}

/** Compute policy digest for a list of policies.
 *
 * Every policy in the list will update the previous policy. Thus the final
 * policy digest will describe the sequential execution of the policy list.
 *
 * @param[in] policy The policy with the policy list.
 * @param[in,out] policyDigests The digest list which has to be updated.
 * @param[in] hash_alg The hash algorithm used for the policy computation.
 * @param[in] hash_size The size of the policy digest.
 * @param[in] digest_idx The index of the current policy in the passed digest list.
 *
 * @retval TSS2_RC_SUCCESS on success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE if an internal error occurred.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 */
TSS2_RC
ifapi_calculate_policy(
    TPML_POLICYELEMENTS *policy,
    TPML_DIGEST_VALUES *policyDigests,
    TPMI_ALG_HASH hash_alg,
    size_t hash_size,
    size_t digest_idx)
{
    size_t i;
    TSS2_RC r = TSS2_RC_SUCCESS;

    for (i = 0; i < policy->count; i++) {

        copy_policy_digest(&policy->elements[i].policyDigests,
                           policyDigests, digest_idx, hash_size,
                           "Copy policy digest (to)");

        switch (policy->elements[i].type) {

        case POLICYPCR:
            r = ifapi_compute_policy_pcr(&policy->elements[i].element.PolicyPCR,
                                         &policy->elements[i].policyDigests,
                                         hash_alg);
            return_if_error(r, "Compute policy pcr");
            break;

        case POLICYSIGNED:
            r = ifapi_calculate_policy_signed(&policy->elements[i].element.
                                              PolicySigned,
                                              &policy->elements[i].
                                              policyDigests, hash_alg);
            return_if_error(r, "Compute policy nv");

            break;

        case POLICYDUPLICATIONSELECT:
            r = ifapi_calculate_policy_duplicate(&policy->elements[i].element.
                                                 PolicyDuplicationSelect,
                                                 &policy->elements[i].
                                                 policyDigests, hash_alg);
            return_if_error(r, "Compute policy duplication select");

            break;

        case POLICYAUTHORIZENV:
            r = ifapi_calculate_policy_authorize_nv(&policy->elements[i].
                                                    element.PolicyAuthorizeNv,
                                                    &policy->elements[i].
                                                    policyDigests, hash_alg);
            return_if_error(r, "Compute policy authorizeg");

            break;

        case POLICYAUTHORIZE:
            r = ifapi_calculate_policy_authorize(&policy->elements[i].element.
                                                 PolicyAuthorize,
                                                 &policy->elements[i].
                                                 policyDigests, hash_alg);
            return_if_error(r, "Compute policy authorizeg");

            break;

        case POLICYSECRET:
            r = ifapi_calculate_policy_secret(&policy->elements[i].element.
                                              PolicySecret,
                                              &policy->elements[i].
                                              policyDigests, hash_alg);
            return_if_error(r, "Compute policy nv");

            break;

        case POLICYOR:
            r = ifapi_calculate_policy_or(&policy->elements[i].element.PolicyOr,
                                          &policy->elements[i].policyDigests,
                                          hash_alg, hash_size, digest_idx);
            return_if_error(r, "Compute policy or");

            break;

        case POLICYNV:
            r = ifapi_calculate_policy_nv(&policy->elements[i].element.PolicyNV,
                                          &policy->elements[i].policyDigests,
                                          hash_alg);
            return_if_error(r, "Compute policy nv");

            break;

        case POLICYNVWRITTEN:
            r = ifapi_calculate_policy_nv_written(&policy->elements[i].element.
                                                  PolicyNvWritten,
                                                  &policy->elements[i].
                                                  policyDigests, hash_alg);
            return_if_error(r, "Compute policy nv written");
            break;

        case POLICYCOUNTERTIMER:
            r = ifapi_calculate_policy_counter_timer(
                    &policy->elements[i].element.PolicyCounterTimer,
                    &policy->elements[i].policyDigests, hash_alg);
            return_if_error(r, "Compute policy counter timer");
            break;

        case POLICYPHYSICALPRESENCE:
            r = ifapi_calculate_policy_physical_presence(
                    &policy->elements[i].policyDigests, hash_alg);
            return_if_error(r, "Compute policy physical presence");
            break;

        case POLICYAUTHVALUE:
            r = ifapi_calculate_policy_auth_value(&policy->elements[i].policyDigests, hash_alg);
            return_if_error(r, "Compute policy auth value");
            break;

        case POLICYPASSWORD:
            r = ifapi_calculate_policy_password(&policy->elements[i].policyDigests, hash_alg);
            return_if_error(r, "Compute policy password");
            break;

        case POLICYCOMMANDCODE:
            r = ifapi_calculate_policy_command_code(&policy->elements[i].element.PolicyCommandCode,
                                                    &policy->elements[i].policyDigests, hash_alg);
            return_if_error(r, "Compute policy physical presence");
            break;

        case POLICYNAMEHASH:
            r = ifapi_calculate_policy_name_hash(&policy->elements[i].element.PolicyNameHash,
                                                 &policy->elements[i].policyDigests, hash_alg);
            return_if_error(r, "Compute policy  name hash");
            break;

        case POLICYCPHASH:
            r = ifapi_calculate_policy_cp_hash(&policy->elements[i].element.PolicyCpHash,
                                               &policy->elements[i].policyDigests, hash_alg);
            return_if_error(r, "Compute policy cp hash");
            break;

        case POLICYLOCALITY:
            r = ifapi_calculate_policy_locality(&policy->elements[i].element.PolicyLocality,
                                                &policy->elements[i].policyDigests, hash_alg);
            return_if_error(r, "Compute policy locality");
            break;

        case POLICYACTION:
            /* This does not alter the policyDigest */
            break;

        case POLICYTEMPLATE:
            r = ifapi_calculate_policy_template(&policy->elements[i].element.
                                                 PolicyTemplate,
                                                 &policy->elements[i].
                                                 policyDigests, hash_alg);
            return_if_error(r, "Compute policy template");

            break;

        default:
            return_error(TSS2_FAPI_RC_BAD_VALUE,
                         "Policy not implemented");
        }

        copy_policy_digest(policyDigests, &policy->elements[i].policyDigests,
                           digest_idx, hash_size, "Copy policy digest (from)");
    }
    return r;
}
