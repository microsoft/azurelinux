/* SPDX-License-Identifier: BSD-2-Clause */
/*******************************************************************************
 * Copyright 2017-2018, Fraunhofer SIT sponsored by Infineon Technologies AG
 * All rights reserved.
 *******************************************************************************/

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <inttypes.h>
#include <string.h>

#include "tss2_esys.h"

#include "esys_mu.h"
#include "esys_iutil.h"
#define LOGMODULE esys
#include "util/log.h"
#include "util/aux_util.h"

/** Marshal an array of BYTE structures into a byte buffer.
 *
 * @param[in] in Structures to be marshaled.
 * @param[in] count Number of structures to be marshaled.
 * @param[in,out] buffer Buffer to write result into.
 * @param[in] size Size of the buffer.
 * @param[in,out] offset Offset inside the buffer
 *                (being updated during marshaling).
 * @retval TSS2_RC_SUCCESS on success.
 * @retval TSS2_ESYS_RC_BAD_REFERENCE if src==NULL.
 * @retval TSS2_ESYS_RC_INSUFFICIENT_BUFFER if remaining buffer is insufficient.
 */
TSS2_RC
iesys_MU_BYTE_array_Marshal(
    const BYTE *src,
    size_t count,
    uint8_t *buffer,
    size_t size,
    size_t *offset)
{
    LOG_TRACE("called: src=%p count=%zu buffer=%p size=%zu offset=%p", src,
              count, buffer, size, offset);
    return_if_null(src, "src=NULL", TSS2_ESYS_RC_BAD_REFERENCE);

    size_t offset_loc = (offset != NULL)? *offset : 0;

    if (count > size || size - count < offset_loc) {
        LOG_ERROR("not enough space in target buffer");
        return TSS2_ESYS_RC_INSUFFICIENT_BUFFER;
    }

    if (buffer != NULL)
        memcpy(&buffer[offset_loc], src, count);
    offset_loc += count;

    if (offset != NULL)
        *offset = offset_loc;
    return TSS2_RC_SUCCESS;
}

/** Unmarshal an array of BYTE structures from a byte buffer.
 *
 * @param[in,out] buffer Buffer to read data from.
 * @param[in] size Size of the buffer.
 * @param[in,out] offset Offset inside the buffer
 *                (being updated during marshaling).
 * @param[in] count Number of structures to be unmarshaled.
 * @param[out] out Structures to store the result in.
 * @retval TSS2_RC_SUCCESS on success.
 * @retval TSS2_ESYS_RC_BAD_REFERENCE if buffer==NULL.
 * @retval TSS2_ESYS_RC_INSUFFICIENT_BUFFER if remaining buffer is insufficient.
 */
TSS2_RC
iesys_MU_BYTE_array_Unmarshal(
    const uint8_t *buffer,
    size_t size,
    size_t *offset,
    size_t count,
    BYTE *dst)
{
    LOG_TRACE("called: count=%zu buffer=%p size=%zu offset=%p dst=%p",
        count, buffer, size, offset, dst);
    return_if_null(buffer, "src=NULL", TSS2_ESYS_RC_BAD_REFERENCE);

    size_t offset_loc = (offset != NULL)? *offset : 0;
    if (dst != NULL)
        memset(dst, 0, sizeof(*dst));

    if (count > size || size - count < offset_loc) {
        LOG_ERROR("not enough space in target buffer");
        return TSS2_ESYS_RC_INSUFFICIENT_BUFFER;
    }

    if (dst != NULL)
        memcpy(dst, &buffer[offset_loc], count);
    offset_loc += count;

    if (offset != NULL)
        *offset = offset_loc;
    return TSS2_RC_SUCCESS;
}

/** Marshal a constant of type IESYSC_PARAM_ENCRYPT into a byte buffer.
 *
 * @param[in] src constant to be marshaled.
 * @param[in,out] buffer Buffer to write result into (may be NULL)
 * @param[in] size Size of the buffer.
 * @param[in,out] offset Offset inside the buffer (may be NULL.
 * @retval TSS2_RC_SUCCESS on success.
 * @retval TSS2_ESYS_RC_BAD_REFERENCE if src==NULL.
 * @retval TSS2_ESYS_RC_INSUFFICIENT_BUFFER if remaining buffer is insufficient.
 */
TSS2_RC
iesys_MU_IESYSC_PARAM_ENCRYPT_Marshal(
    const IESYSC_PARAM_ENCRYPT src,
    uint8_t *buffer,
    size_t size,
    size_t *offset)
{
    LOG_TRACE("called: src=%"PRIx32 " buffer=%p size=%zu offset=%p", src,
        buffer, size, offset);
    return Tss2_MU_UINT32_Marshal(src, buffer, size, offset);
}

/** Unmarshal a constant of type IESYSC_PARAM_ENCRYPT from a byte buffer.
 *
 * @param[in,out] buffer Buffer to read data from.
 * @param[in] size Size of the buffer.
 * @param[in,out] offset Offset inside the buffer
 *                (being updated during marshaling).
 * @param[out] dst variable to store the result in.
 * @retval TSS2_RC_SUCCESS on success.
 */
TSS2_RC
iesys_MU_IESYSC_PARAM_ENCRYPT_Unmarshal(
    const uint8_t *buffer,
    size_t size,
    size_t *offset,
    IESYSC_PARAM_ENCRYPT *dst)
{
    LOG_TRACE("called: buffer=%p size=%zu offset=%p dst=%p",
        buffer, size, offset, dst);
    size_t offset_loc = (offset != NULL)? *offset : 0;
    if (dst != NULL)
        memset(dst, 0, sizeof(*dst));
    IESYSC_PARAM_ENCRYPT dst_loc;
    TSS2_RC ret = Tss2_MU_UINT32_Unmarshal(buffer, size,
        &offset_loc, &dst_loc);
    return_if_error(ret, "Unmarshaling the base type");

    ret = iesys_MU_IESYSC_PARAM_ENCRYPT_check(&dst_loc);
    if (ret != TSS2_RC_SUCCESS) {
        LOG_ERROR("Bad value %"PRIx32 "", dst_loc);
        return ret;
    }
    if (offset != NULL)
        *offset = offset_loc;
    if (dst != NULL)
        *dst = dst_loc;
    LOG_TRACE("return: dst=%p value=%"PRIx32 "", dst, dst_loc);
    return TSS2_RC_SUCCESS;
}

/** Check, if a variable has a possible value of type IESYSC_PARAM_ENCRYPT.
 *
 * @param[in] in variable to check.
 * @retval TSS2_RC_SUCCESS on success.
 */
TSS2_RC
iesys_MU_IESYSC_PARAM_ENCRYPT_check(
    const IESYSC_PARAM_ENCRYPT *in)
{
    LOG_TRACE("called: in=%p", in);
    return_if_null(in, "in==NULL", TSS2_SYS_RC_BAD_REFERENCE);

    /* No Error-Messages, since this function may fail for a good reasons. */
    if (FALSE
        || (*in == ENCRYPT)
        || (*in == NO_ENCRYPT)) {
        return TSS2_RC_SUCCESS;
    }

    return TSS2_SYS_RC_BAD_VALUE;
}
/** Marshal a constant of type IESYSC_PARAM_DECRYPT into a byte buffer.
 *
 * @param[in] src constant to be marshaled.
 * @param[in,out] buffer Buffer to write result into (may be NULL)
 * @param[in] size Size of the buffer.
 * @param[in,out] offset Offset inside the buffer (may be NULL.
 * @retval TSS2_RC_SUCCESS on success.
 * @retval TSS2_ESYS_RC_BAD_REFERENCE if src==NULL.
 * @retval TSS2_ESYS_RC_INSUFFICIENT_BUFFER if remaining buffer is insufficient.
 */
TSS2_RC
iesys_MU_IESYSC_PARAM_DECRYPT_Marshal(
    const IESYSC_PARAM_DECRYPT src,
    uint8_t *buffer,
    size_t size,
    size_t *offset)
{
    LOG_TRACE("called: src=%"PRIx32 " buffer=%p size=%zu offset=%p", src,
        buffer, size, offset);
    return Tss2_MU_UINT32_Marshal(src, buffer, size, offset);
}

/** Unmarshal a constant of type IESYSC_PARAM_DECRYPT from a byte buffer.
 *
 * @param[in,out] buffer Buffer to read data from.
 * @param[in] size Size of the buffer.
 * @param[in,out] offset Offset inside the buffer
 *                (being updated during marshaling).
 * @param[out] dst variable to store the result in.
 * @retval TSS2_RC_SUCCESS on success.
 */
TSS2_RC
iesys_MU_IESYSC_PARAM_DECRYPT_Unmarshal(
    const uint8_t *buffer,
    size_t size,
    size_t *offset,
    IESYSC_PARAM_DECRYPT *dst)
{
    LOG_TRACE("called: buffer=%p size=%zu offset=%p dst=%p",
        buffer, size, offset, dst);
    size_t offset_loc = (offset != NULL)? *offset : 0;
    if (dst != NULL)
        memset(dst, 0, sizeof(*dst));
    IESYSC_PARAM_DECRYPT dst_loc;
    TSS2_RC ret = Tss2_MU_UINT32_Unmarshal(buffer, size,
        &offset_loc, &dst_loc);
    return_if_error(ret, "Unmarshaling the base type");

    ret = iesys_MU_IESYSC_PARAM_DECRYPT_check(&dst_loc);
    if (ret != TSS2_RC_SUCCESS) {
        LOG_ERROR("Bad value %"PRIx32 "", dst_loc);
        return ret;
    }
    if (offset != NULL)
        *offset = offset_loc;
    if (dst != NULL)
        *dst = dst_loc;
    LOG_TRACE("return: dst=%p value=%"PRIx32 "", dst, dst_loc);
    return TSS2_RC_SUCCESS;
}

/** Check, if a variable has a possible value of type IESYSC_PARAM_DECRYPT.
 *
 * @param[in] in variable to check.
 * @retval TSS2_RC_SUCCESS on success.
 */
TSS2_RC
iesys_MU_IESYSC_PARAM_DECRYPT_check(
    const IESYSC_PARAM_DECRYPT *in)
{
    LOG_TRACE("called: in=%p", in);
    return_if_null(in, "in==NULL", TSS2_SYS_RC_BAD_REFERENCE);

    /* No Error-Messages, since this function may fail for a good reasons. */
    if (FALSE
        || (*in == DECRYPT)
        || (*in == NO_DECRYPT)) {
        return TSS2_RC_SUCCESS;
    }

    return TSS2_SYS_RC_BAD_VALUE;
}
/** Marshal a constant of type IESYSC_TYPE_POLICY_AUTH into a byte buffer.
 *
 * @param[in] src constant to be marshaled.
 * @param[in,out] buffer Buffer to write result into (may be NULL)
 * @param[in] size Size of the buffer.
 * @param[in,out] offset Offset inside the buffer (may be NULL.
 * @retval TSS2_RC_SUCCESS on success.
 * @retval TSS2_ESYS_RC_BAD_REFERENCE if src==NULL.
 * @retval TSS2_ESYS_RC_INSUFFICIENT_BUFFER if remaining buffer is insufficient.
 */
TSS2_RC
iesys_MU_IESYSC_TYPE_POLICY_AUTH_Marshal(
    const IESYSC_TYPE_POLICY_AUTH src,
    uint8_t *buffer,
    size_t size,
    size_t *offset)
{
    LOG_TRACE("called: src=%"PRIx32 " buffer=%p size=%zu offset=%p", src,
        buffer, size, offset);
    return Tss2_MU_UINT32_Marshal(src, buffer, size, offset);
}

/** Unmarshal a constant of type IESYSC_TYPE_POLICY_AUTH from a byte buffer.
 *
 * @param[in,out] buffer Buffer to read data from.
 * @param[in] size Size of the buffer.
 * @param[in,out] offset Offset inside the buffer
 *                (being updated during marshaling).
 * @param[out] dst variable to store the result in.
 * @retval TSS2_RC_SUCCESS on success.
 */
TSS2_RC
iesys_MU_IESYSC_TYPE_POLICY_AUTH_Unmarshal(
    const uint8_t *buffer,
    size_t size,
    size_t *offset,
    IESYSC_TYPE_POLICY_AUTH *dst)
{
    LOG_TRACE("called: buffer=%p size=%zu offset=%p dst=%p",
        buffer, size, offset, dst);
    size_t offset_loc = (offset != NULL)? *offset : 0;
    if (dst != NULL)
        memset(dst, 0, sizeof(*dst));
    IESYSC_TYPE_POLICY_AUTH dst_loc;
    TSS2_RC ret = Tss2_MU_UINT32_Unmarshal(buffer, size,
        &offset_loc, &dst_loc);
    return_if_error(ret, "Unmarshaling the base type");

    ret = iesys_MU_IESYSC_TYPE_POLICY_AUTH_check(&dst_loc);
    if (ret != TSS2_RC_SUCCESS) {
        LOG_ERROR("Bad value %"PRIx32 "", dst_loc);
        return ret;
    }
    if (offset != NULL)
        *offset = offset_loc;
    if (dst != NULL)
        *dst = dst_loc;
    LOG_TRACE("return: dst=%p value=%"PRIx32 "", dst, dst_loc);
    return TSS2_RC_SUCCESS;
}

/** Check, if a variable has a possible value of type IESYSC_TYPE_POLICY_AUTH.
 *
 * @param[in] in variable to check.
 * @retval TSS2_RC_SUCCESS on success.
 */
TSS2_RC
iesys_MU_IESYSC_TYPE_POLICY_AUTH_check(
    const IESYSC_TYPE_POLICY_AUTH *in)
{
    LOG_TRACE("called: in=%p", in);
    return_if_null(in, "in==NULL", TSS2_SYS_RC_BAD_REFERENCE);

    /* No Error-Messages, since this function may fail for a good reasons. */
    if (FALSE
        || (*in == POLICY_PASSWORD)
        || (*in == POLICY_AUTH)
        || (*in == NO_POLICY_AUTH)) {
        return TSS2_RC_SUCCESS;
    }

    return TSS2_SYS_RC_BAD_VALUE;
}

/** Marshal a IESYS_SESSION structure into a byte buffer.
 *
 * @param[in] src variable to be marshaled.
 * @param[in,out] buffer Buffer to write result into.
 * @param[in] size Size of the buffer.
 * @param[in,out] offset Offset inside the buffer
 *                (being updated during marshaling).
 * @retval TSS2_RC_SUCCESS on success.
 * @retval TSS2_ESYS_RC_BAD_REFERENCE if src==NULL.
 * @retval TSS2_ESYS_RC_INSUFFICIENT_BUFFER if remaining buffer is insufficient.
 */
TSS2_RC
iesys_MU_IESYS_SESSION_Marshal(
    const IESYS_SESSION *src,
    uint8_t *buffer,
    size_t size,
    size_t *offset)
{
    LOG_TRACE("called: src=%p buffer=%p size=%zu offset=%p", src,
        buffer, size, offset);
    if (src == NULL) {
        LOG_ERROR("src=NULL");
        return TSS2_SYS_RC_BAD_REFERENCE;
    }
    TSS2_RC ret;
    size_t offset_loc = (offset != NULL)? *offset : 0;
    ret = Tss2_MU_TPM2B_NAME_Marshal(&src->bound_entity, buffer, size, &offset_loc);
    return_if_error(ret, "Error marshaling subfield bound_entity");

    ret = Tss2_MU_TPM2B_ENCRYPTED_SECRET_Marshal(&src->encryptedSalt, buffer, size, &offset_loc);
    return_if_error(ret, "Error marshaling subfield encryptedSalt");

    ret = Tss2_MU_TPM2B_DATA_Marshal(&src->salt, buffer, size, &offset_loc);
    return_if_error(ret, "Error marshaling subfield salt");

    ret = Tss2_MU_TPMT_SYM_DEF_Marshal(&src->symmetric, buffer, size, &offset_loc);
    return_if_error(ret, "Error marshaling subfield symmetric");

    ret = Tss2_MU_TPMI_ALG_HASH_Marshal(src->authHash, buffer, size, &offset_loc);
    return_if_error(ret, "Error marshaling subfield authHash");

    ret = Tss2_MU_TPM2B_DIGEST_Marshal(&src->sessionKey, buffer, size, &offset_loc);
    return_if_error(ret, "Error marshaling subfield sessionKey");

    ret = Tss2_MU_TPM2_SE_Marshal(src->sessionType, buffer, size, &offset_loc);
    return_if_error(ret, "Error marshaling subfield sessionType");

    ret = Tss2_MU_TPMA_SESSION_Marshal(src->sessionAttributes, buffer, size, &offset_loc);
    return_if_error(ret, "Error marshaling subfield sessionAttributes");

    ret = Tss2_MU_TPM2B_NONCE_Marshal(&src->nonceCaller, buffer, size, &offset_loc);
    return_if_error(ret, "Error marshaling subfield nonceCaller");

    ret = Tss2_MU_TPM2B_NONCE_Marshal(&src->nonceTPM, buffer, size, &offset_loc);
    return_if_error(ret, "Error marshaling subfield nonceTPM");

    ret = iesys_MU_IESYSC_PARAM_ENCRYPT_Marshal(src->encrypt, buffer, size, &offset_loc);
    return_if_error(ret, "Error marshaling subfield encrypt");

    ret = iesys_MU_IESYSC_PARAM_DECRYPT_Marshal(src->decrypt, buffer, size, &offset_loc);
    return_if_error(ret, "Error marshaling subfield decrypt");

    ret = iesys_MU_IESYSC_TYPE_POLICY_AUTH_Marshal(src->type_policy_session, buffer, size, &offset_loc);
    return_if_error(ret, "Error marshaling subfield type_policy_session");

    ret = Tss2_MU_UINT16_Marshal(src->sizeSessionValue, buffer, size, &offset_loc);
    return_if_error(ret, "Error marshaling subfield sizeSessionValue");

    ret = iesys_MU_BYTE_array_Marshal(&src->sessionValue[0], src->sizeSessionValue,
        buffer, size, &offset_loc);
    return_if_error(ret, "Error marshaling subfield sessionValue");

    ret = Tss2_MU_UINT16_Marshal(src->sizeHmacValue, buffer, size, &offset_loc);
    return_if_error(ret, "Error marshaling subfield sizeHmacValue");

    if (offset != NULL)
        *offset = offset_loc;
    return TSS2_RC_SUCCESS;
}

/** Unmarshal a IESYS_SESSION variable from a byte buffer.
 *
 * @param[in,out] buffer Buffer to read data from.
 * @param[in] size Size of the buffer.
 * @param[in,out] offset Offset inside the buffer
 *                (being updated during marshaling).
 * @param[out] out variable to store the result in.
 * @retval TSS2_RC_SUCCESS on success.
 * @retval TSS2_ESYS_RC_BAD_REFERENCE if buffer==NULL.
 * @retval TSS2_ESYS_RC_INSUFFICIENT_BUFFER if remaining buffer is insufficient.
 */
TSS2_RC
iesys_MU_IESYS_SESSION_Unmarshal(
    const uint8_t *buffer,
    size_t size,
    size_t *offset,
    IESYS_SESSION *dst)
{
    LOG_TRACE("called: buffer=%p size=%zu offset=%p dst=%p",
        buffer, size, offset, dst);
    if (buffer == NULL) {
        LOG_ERROR("buffer=NULL");
        return TSS2_ESYS_RC_BAD_REFERENCE;
    }
    TSS2_RC ret;
    size_t offset_loc = (offset != NULL)? *offset : 0;
    if (dst != NULL)
        memset(dst, 0, sizeof(*dst));
    ret = Tss2_MU_TPM2B_NAME_Unmarshal(buffer, size, &offset_loc,
            (dst == NULL)? NULL : &dst->bound_entity);
    return_if_error(ret, "Error unmarshaling subfield bound_entity");

    ret = Tss2_MU_TPM2B_ENCRYPTED_SECRET_Unmarshal(buffer, size, &offset_loc,
            (dst == NULL)? NULL : &dst->encryptedSalt);
    return_if_error(ret, "Error unmarshaling subfield encryptedSalt");

    ret = Tss2_MU_TPM2B_DATA_Unmarshal(buffer, size, &offset_loc,
            (dst == NULL)? NULL : &dst->salt);
    return_if_error(ret, "Error unmarshaling subfield salt");

    ret = Tss2_MU_TPMT_SYM_DEF_Unmarshal(buffer, size, &offset_loc,
            (dst == NULL)? NULL : &dst->symmetric);
    return_if_error(ret, "Error unmarshaling subfield symmetric");

    TPMI_ALG_HASH out_authHash;
    ret = Tss2_MU_TPMI_ALG_HASH_Unmarshal(buffer, size, &offset_loc,
            (dst == NULL)? &out_authHash : &dst->authHash);
    return_if_error(ret, "Error unmarshaling subfield authHash");

    ret = Tss2_MU_TPM2B_DIGEST_Unmarshal(buffer, size, &offset_loc,
            (dst == NULL)? NULL : &dst->sessionKey);
    return_if_error(ret, "Error unmarshaling subfield sessionKey");

    TPM2_SE out_sessionType;
    ret = Tss2_MU_TPM2_SE_Unmarshal(buffer, size, &offset_loc,
            (dst == NULL)? &out_sessionType : &dst->sessionType);
    return_if_error(ret, "Error unmarshaling subfield sessionType");

    TPMA_SESSION out_sessionAttributes;
    ret = Tss2_MU_TPMA_SESSION_Unmarshal(buffer, size, &offset_loc,
            (dst == NULL)? &out_sessionAttributes : &dst->sessionAttributes);
    return_if_error(ret, "Error unmarshaling subfield sessionAttributes");

    ret = Tss2_MU_TPM2B_NONCE_Unmarshal(buffer, size, &offset_loc,
            (dst == NULL)? NULL : &dst->nonceCaller);
    return_if_error(ret, "Error unmarshaling subfield nonceCaller");

    ret = Tss2_MU_TPM2B_NONCE_Unmarshal(buffer, size, &offset_loc,
            (dst == NULL)? NULL : &dst->nonceTPM);
    return_if_error(ret, "Error unmarshaling subfield nonceTPM");

    IESYSC_PARAM_ENCRYPT out_encrypt;
    ret = iesys_MU_IESYSC_PARAM_ENCRYPT_Unmarshal(buffer, size, &offset_loc,
            (dst == NULL)? &out_encrypt : &dst->encrypt);
    return_if_error(ret, "Error unmarshaling subfield encrypt");

    IESYSC_PARAM_DECRYPT out_decrypt;
    ret = iesys_MU_IESYSC_PARAM_DECRYPT_Unmarshal(buffer, size, &offset_loc,
            (dst == NULL)? &out_decrypt : &dst->decrypt);
    return_if_error(ret, "Error unmarshaling subfield decrypt");

    IESYSC_TYPE_POLICY_AUTH out_type_policy_session;
    ret = iesys_MU_IESYSC_TYPE_POLICY_AUTH_Unmarshal(buffer, size, &offset_loc,
            (dst == NULL)? &out_type_policy_session : &dst->type_policy_session);
    return_if_error(ret, "Error unmarshaling subfield type_policy_session");

    UINT16 out_sizeSessionValue;
    ret = Tss2_MU_UINT16_Unmarshal(buffer, size, &offset_loc,
            (dst == NULL)? &out_sizeSessionValue : &dst->sizeSessionValue);
    return_if_error(ret, "Error unmarshaling subfield sizeSessionValue");

    ret = iesys_MU_BYTE_array_Unmarshal(buffer, size, &offset_loc,
            (dst == NULL)? out_sizeSessionValue : dst->sizeSessionValue,
            (dst == NULL)? NULL : &dst->sessionValue[0]);
    return_if_error(ret, "Error unmarshaling subfield sessionValue");

    UINT16 out_sizeHmacValue;
    ret = Tss2_MU_UINT16_Unmarshal(buffer, size, &offset_loc,
            (dst == NULL)? &out_sizeHmacValue : &dst->sizeHmacValue);
    return_if_error(ret, "Error unmarshaling subfield sizeHmacValue");

    if (offset != NULL)
        *offset = offset_loc;
    return TSS2_RC_SUCCESS;
}

/** Marshal a IESYSC_RESOURCE_TYPE type into a byte buffer.
 *
 * @param[in] src constant to be marshaled.
 * @param[in,out] buffer Buffer to write result into (may be NULL)
 * @param[in] size Size of the buffer.
 * @param[in,out] offset Offset inside the buffer (may be NULL.
 * @retval TSS2_RC_SUCCESS on success.
 * @retval TSS2_ESYS_RC_BAD_REFERENCE if src==NULL.
 * @retval TSS2_ESYS_RC_INSUFFICIENT_BUFFER if remaining buffer is insufficient.
 */
TSS2_RC
iesys_MU_IESYSC_RESOURCE_TYPE_Marshal(
    const IESYSC_RESOURCE_TYPE src,
    uint8_t *buffer,
    size_t size,
    size_t *offset)
{
    LOG_TRACE("called: src=%"PRIx32 " buffer=%p size=%zu offset=%p", src,
        buffer, size, offset);
    return Tss2_MU_UINT32_Marshal(src, buffer, size, offset);
}

/** Unmarshal a IESYSC_RESOURCE_TYPE type from a byte buffer.
 *
 * @param[in,out] buffer Buffer to read data from.
 * @param[in] size Size of the buffer.
 * @param[in,out] offset Offset inside the buffer
 *                (being updated during marshaling).
 * @param[out] dst variable to store the result in.
 * @retval TSS2_RC_SUCCESS on success.
 */
TSS2_RC
iesys_MU_IESYSC_RESOURCE_TYPE_Unmarshal(
    const uint8_t *buffer,
    size_t size,
    size_t *offset,
    IESYSC_RESOURCE_TYPE *dst)
{
    LOG_TRACE("called: buffer=%p size=%zu offset=%p dst=%p",
        buffer, size, offset, dst);
    IESYSC_RESOURCE_TYPE dst_loc;
    TSS2_RC ret = Tss2_MU_UINT32_Unmarshal(buffer, size,
        offset, &dst_loc);
    return_if_error(ret, "Unmarshaling the base type");

    ret = iesys_MU_IESYSC_RESOURCE_TYPE_check(&dst_loc);
    if (ret != TSS2_RC_SUCCESS) {
        LOG_ERROR("Bad value %"PRIx32 "", dst_loc);
        return ret;
    }
    if (dst != NULL)
        *dst = dst_loc;
    LOG_TRACE("return: dst=%p value=%"PRIx32 "", dst, dst_loc);
    return TSS2_RC_SUCCESS;
}
/** Check, if a variable has a possible value of type IESYSC_RESOURCE_TYPE.
 *
 * @param[in] in variable to check.
 * @retval TSS2_RC_SUCCESS on success.
 */
TSS2_RC
iesys_MU_IESYSC_RESOURCE_TYPE_check(
    const IESYSC_RESOURCE_TYPE *in)
{
    LOG_TRACE("called: in=%p", in);
    return_if_null(in, "in==NULL", TSS2_SYS_RC_BAD_REFERENCE);

    /* No Error-Messages, since this function may fail for a good reasons. */
    if (FALSE
            || (*in == IESYSC_KEY_RSRC)
            || (*in == IESYSC_NV_RSRC)
            || (*in == IESYSC_SESSION_RSRC)
            || (*in == IESYSC_WITHOUT_MISC_RSRC)) {
        return TSS2_RC_SUCCESS;
    }

    return TSS2_SYS_RC_BAD_VALUE;
}

/** Marshal a IESYS_RSRC_UNION union into a byte buffer.
 *
 * @param[in] src variable to be marshaled.
 * @param[in] selector the selector value.
 * @param[in,out] buffer Buffer to write result into.
 * @param[in] size Size of the buffer.
 * @param[in,out] offset Offset inside the buffer
 *                (being updated during marshaling).
 * @retval TSS2_RC_SUCCESS on success.
 * @retval TSS2_ESYS_RC_BAD_REFERENCE if src==NULL.
 * @retval TSS2_ESYS_RC_INSUFFICIENT_BUFFER if remaining buffer is insufficient.
 */
TSS2_RC
iesys_MU_IESYS_RSRC_UNION_Marshal(
    const IESYS_RSRC_UNION *src,
    UINT32 selector,
    uint8_t *buffer,
    size_t size,
    size_t *offset)
{
    LOG_TRACE("called: src=%p buffer=%p size=%zu offset=%p", src,
        buffer, size, offset);
    if (src == NULL) {
        LOG_ERROR("src=NULL");
        return TSS2_ESYS_RC_BAD_REFERENCE;
    }

    switch (selector) {
    case IESYSC_KEY_RSRC:
        return Tss2_MU_TPM2B_PUBLIC_Marshal(&src->rsrc_key_pub, buffer, size, offset);
    case IESYSC_NV_RSRC:
        return Tss2_MU_TPM2B_NV_PUBLIC_Marshal(&src->rsrc_nv_pub, buffer, size, offset);
    case IESYSC_SESSION_RSRC:
        return iesys_MU_IESYS_SESSION_Marshal(&src->rsrc_session, buffer, size, offset);
    case IESYSC_WITHOUT_MISC_RSRC:
        return Tss2_MU_TPMS_EMPTY_Marshal(&src->rsrc_empty, buffer, size, offset);
    default:
        LOG_ERROR("Selector value %"PRIu32 " not found", selector);
        return TSS2_SYS_RC_BAD_VALUE;
    };
}

/** Unmarshal a IESYS_RSRC_UNION union from a byte buffer.
 *
 * @param[in,out] buffer Buffer to read data from.
 * @param[in] size Size of the buffer.
 * @param[in,out] offset Offset inside the buffer (may be NULL).
 * @param[in] selector The selector.
 * @param[out] out variable to store the result in (may be NULL).
 * @retval TSS2_RC_SUCCESS on success.
 * @retval TSS2_ESYS_RC_BAD_REFERENCE if src==NULL.
 * @retval TSS2_ESYS_RC_INSUFFICIENT_BUFFER if remaining buffer is insufficient.
 */
TSS2_RC
iesys_MU_IESYS_RSRC_UNION_Unmarshal(
    const uint8_t *buffer,
    size_t size,
    size_t *offset,
    UINT32 selector,
    IESYS_RSRC_UNION *dst)
{
    LOG_TRACE("called: buffer=%p size=%zu offset=%p dst=%p",
        buffer, size, offset, dst);
    if (buffer == NULL) {
        LOG_ERROR("buffer=NULL");
        return TSS2_ESYS_RC_BAD_REFERENCE;
    }
    switch (selector) {
    case IESYSC_KEY_RSRC:
        return Tss2_MU_TPM2B_PUBLIC_Unmarshal(buffer, size, offset,
                   (dst != NULL)? &dst->rsrc_key_pub : NULL);
    case IESYSC_NV_RSRC:
        return Tss2_MU_TPM2B_NV_PUBLIC_Unmarshal(buffer, size, offset,
                   (dst != NULL)? &dst->rsrc_nv_pub : NULL);
    case IESYSC_SESSION_RSRC:
        return iesys_MU_IESYS_SESSION_Unmarshal(buffer, size, offset,
                   (dst != NULL)? &dst->rsrc_session : NULL);
    case IESYSC_WITHOUT_MISC_RSRC:
        return Tss2_MU_TPMS_EMPTY_Unmarshal(buffer, size, offset,
                   (dst != NULL)? &dst->rsrc_empty : NULL);
    default:
        LOG_ERROR("Selector value %"PRIu32 " not found", selector);
        return TSS2_SYS_RC_BAD_VALUE;
    };
}

/** Marshal a IESYS_RESOURCE structure into a byte buffer.
 *
 * @param[in] src variable to be marshaled.
 * @param[in,out] buffer Buffer to write result into.
 * @param[in] size Size of the buffer.
 * @param[in,out] offset Offset inside the buffer
 *                (being updated during marshaling).
 * @retval TSS2_RC_SUCCESS on success.
 * @retval TSS2_ESYS_RC_BAD_REFERENCE if src==NULL.
 * @retval TSS2_ESYS_RC_INSUFFICIENT_BUFFER if remaining buffer is insufficient.
 */
TSS2_RC
iesys_MU_IESYS_RESOURCE_Marshal(
    const IESYS_RESOURCE *src,
    uint8_t *buffer,
    size_t size,
    size_t *offset)
{
    LOG_TRACE("called: src=%p buffer=%p size=%zu offset=%p", src,
        buffer, size, offset);
    if (src == NULL) {
        LOG_ERROR("src=NULL");
        return TSS2_SYS_RC_BAD_REFERENCE;
    }
    TSS2_RC ret;
    size_t offset_loc = (offset != NULL)? *offset : 0;
    ret = Tss2_MU_TPM2_HANDLE_Marshal(src->handle, buffer, size, &offset_loc);
    return_if_error(ret, "Error marshaling subfield handle");

    ret = Tss2_MU_TPM2B_NAME_Marshal(&src->name, buffer, size, &offset_loc);
    return_if_error(ret, "Error marshaling subfield name");

    ret = iesys_MU_IESYSC_RESOURCE_TYPE_Marshal(src->rsrcType, buffer, size, &offset_loc);
    return_if_error(ret, "Error marshaling subfield rsrcType");

    ret = iesys_MU_IESYS_RSRC_UNION_Marshal(&src->misc, src->rsrcType,
        buffer, size, &offset_loc);
    return_if_error(ret, "Error marshaling subfield misc");

    if (offset != NULL)
        *offset = offset_loc;
    return TSS2_RC_SUCCESS;
}

/** Unmarshal a IESYS_RESOURCE variable from a byte buffer.
 *
 * @param[in,out] buffer Buffer to read data from.
 * @param[in] size Size of the buffer.
 * @param[in,out] offset Offset inside the buffer
 *                (being updated during marshaling).
 * @param[out] out variable to store the result in.
 * @retval TSS2_RC_SUCCESS on success.
 * @retval TSS2_ESYS_RC_BAD_REFERENCE if buffer==NULL.
 * @retval TSS2_ESYS_RC_INSUFFICIENT_BUFFER if remaining buffer is insufficient.
 */
TSS2_RC
iesys_MU_IESYS_RESOURCE_Unmarshal(
    const uint8_t *buffer,
    size_t size,
    size_t *offset,
    IESYS_RESOURCE *dst)
{
    LOG_TRACE("called: buffer=%p size=%zu offset=%p dst=%p",
        buffer, size, offset, dst);
    if (buffer == NULL) {
        LOG_ERROR("buffer=NULL");
        return TSS2_ESYS_RC_BAD_REFERENCE;
    }
    TSS2_RC ret;
    size_t offset_loc = (offset != NULL)? *offset : 0;
    if (dst != NULL)
        memset(dst, 0, sizeof(*dst));
    TPM2_HANDLE out_handle;
    ret = Tss2_MU_TPM2_HANDLE_Unmarshal(buffer, size, &offset_loc,
            (dst == NULL)? &out_handle : &dst->handle);
    return_if_error(ret, "Error unmarshaling subfield handle");

    ret = Tss2_MU_TPM2B_NAME_Unmarshal(buffer, size, &offset_loc,
            (dst == NULL)? NULL : &dst->name);
    return_if_error(ret, "Error unmarshaling subfield name");

    IESYSC_RESOURCE_TYPE out_rsrcType;
    ret = iesys_MU_IESYSC_RESOURCE_TYPE_Unmarshal(buffer, size, &offset_loc,
            (dst == NULL)? &out_rsrcType : &dst->rsrcType);
    return_if_error(ret, "Error unmarshaling subfield rsrcType");

    ret = iesys_MU_IESYS_RSRC_UNION_Unmarshal(buffer, size, &offset_loc,
            (dst == NULL)? out_rsrcType : dst->rsrcType,
            (dst == NULL)? NULL : &dst->misc);
    return_if_error(ret, "Error unmarshaling subfield misc");

    if (offset != NULL)
        *offset = offset_loc;
    return TSS2_RC_SUCCESS;
}

/** Marshal a IESYS_METADATA structure into a byte buffer.
 *
 * @param[in] src variable to be marshaled.
 * @param[in,out] buffer Buffer to write result into.
 * @param[in] size Size of the buffer.
 * @param[in,out] offset Offset inside the buffer
 *                (being updated during marshaling).
 * @retval TSS2_RC_SUCCESS on success.
 * @retval TSS2_ESYS_RC_BAD_REFERENCE if src==NULL.
 * @retval TSS2_ESYS_RC_INSUFFICIENT_BUFFER if remaining buffer is insufficient.
 */
TSS2_RC
iesys_MU_IESYS_METADATA_Marshal(
    const IESYS_METADATA *src,
    uint8_t *buffer,
    size_t size,
    size_t *offset)
{
    LOG_TRACE("called: src=%p buffer=%p size=%zu offset=%p", src,
        buffer, size, offset);
    if (src == NULL) {
        LOG_ERROR("src=NULL");
        return TSS2_SYS_RC_BAD_REFERENCE;
    }
    TSS2_RC ret;
    size_t offset_loc = (offset != NULL)? *offset : 0;
    ret = Tss2_MU_UINT16_Marshal(src->size, buffer, size, &offset_loc);
    return_if_error(ret, "Error marshaling subfield size");

    ret = iesys_MU_IESYS_RESOURCE_Marshal(&src->data, buffer, size, &offset_loc);
    return_if_error(ret, "Error marshaling subfield data");

    if (offset != NULL)
        *offset = offset_loc;
    return TSS2_RC_SUCCESS;
}

/** Unmarshal a IESYS_METADATA variable from a byte buffer.
 *
 * @param[in,out] buffer Buffer to read data from.
 * @param[in] size Size of the buffer.
 * @param[in,out] offset Offset inside the buffer
 *                (being updated during marshaling).
 * @param[out] out variable to store the result in.
 * @retval TSS2_RC_SUCCESS on success.
 * @retval TSS2_ESYS_RC_BAD_REFERENCE if buffer==NULL.
 * @retval TSS2_ESYS_RC_INSUFFICIENT_BUFFER if remaining buffer is insufficient.
 */
TSS2_RC
iesys_MU_IESYS_METADATA_Unmarshal(
    const uint8_t *buffer,
    size_t size,
    size_t *offset,
    IESYS_METADATA *dst)
{
    LOG_TRACE("called: buffer=%p size=%zu offset=%p dst=%p",
        buffer, size, offset, dst);
    if (buffer == NULL) {
        LOG_ERROR("buffer=NULL");
        return TSS2_ESYS_RC_BAD_REFERENCE;
    }
    TSS2_RC ret;
    size_t offset_loc = (offset != NULL)? *offset : 0;
    if (dst != NULL)
        memset(dst, 0, sizeof(*dst));
    UINT16 out_size;
    ret = Tss2_MU_UINT16_Unmarshal(buffer, size, &offset_loc,
            (dst == NULL)? &out_size : &dst->size);
    return_if_error(ret, "Error unmarshaling subfield size");

    IESYS_RESOURCE out_data;
    ret = iesys_MU_IESYS_RESOURCE_Unmarshal(buffer, size, &offset_loc,
            (dst == NULL)? &out_data : &dst->data);
    return_if_error(ret, "Error unmarshaling subfield data");

    if (offset != NULL)
        *offset = offset_loc;
    return TSS2_RC_SUCCESS;
}

/** Marshal a IESYS_CONTEXT_DATA structure into a byte buffer.
 *
 * @param[in] src variable to be marshaled.
 * @param[in,out] buffer Buffer to write result into.
 * @param[in] size Size of the buffer.
 * @param[in,out] offset Offset inside the buffer
 *                (being updated during marshaling).
 * @retval TSS2_RC_SUCCESS on success.
 * @retval TSS2_ESYS_RC_BAD_REFERENCE if src==NULL.
 * @retval TSS2_ESYS_RC_INSUFFICIENT_BUFFER if remaining buffer is insufficient.
 */
TSS2_RC
iesys_MU_IESYS_CONTEXT_DATA_Marshal(
    const IESYS_CONTEXT_DATA *src,
    uint8_t *buffer,
    size_t size,
    size_t *offset)
{
    LOG_TRACE("called: src=%p buffer=%p size=%zu offset=%p", src,
        buffer, size, offset);
    if (src == NULL) {
        LOG_ERROR("src=NULL");
        return TSS2_SYS_RC_BAD_REFERENCE;
    }
    TSS2_RC ret;
    size_t offset_loc = (offset != NULL)? *offset : 0;
    ret = Tss2_MU_UINT32_Marshal(src->reserved, buffer, size, &offset_loc);
    return_if_error(ret, "Error marshaling subfield reserved");

    ret = Tss2_MU_TPM2B_CONTEXT_DATA_Marshal(&src->tpmContext, buffer, size, &offset_loc);
    return_if_error(ret, "Error marshaling subfield tpmContext");

    ret = iesys_MU_IESYS_METADATA_Marshal(&src->esysMetadata, buffer, size, &offset_loc);
    return_if_error(ret, "Error marshaling subfield esysMetadata");

    if (offset != NULL)
        *offset = offset_loc;
    return TSS2_RC_SUCCESS;
}

/** Unmarshal a IESYS_CONTEXT_DATA variable from a byte buffer.
 *
 * @param[in,out] buffer Buffer to read data from.
 * @param[in] size Size of the buffer.
 * @param[in,out] offset Offset inside the buffer
 *                (being updated during marshaling).
 * @param[out] out variable to store the result in.
 * @retval TSS2_RC_SUCCESS on success.
 * @retval TSS2_ESYS_RC_BAD_REFERENCE if buffer==NULL.
 * @retval TSS2_ESYS_RC_INSUFFICIENT_BUFFER if remaining buffer is insufficient.
 */
TSS2_RC
iesys_MU_IESYS_CONTEXT_DATA_Unmarshal(
    const uint8_t *buffer,
    size_t size,
    size_t *offset,
    IESYS_CONTEXT_DATA *dst)
{
    LOG_TRACE("called: buffer=%p size=%zu offset=%p dst=%p",
        buffer, size, offset, dst);
    if (buffer == NULL) {
        LOG_ERROR("buffer=NULL");
        return TSS2_ESYS_RC_BAD_REFERENCE;
    }
    TSS2_RC ret;
    size_t offset_loc = (offset != NULL)? *offset : 0;
    if (dst != NULL)
        memset(dst, 0, sizeof(*dst));
    UINT32 out_reserved;
    ret = Tss2_MU_UINT32_Unmarshal(buffer, size, &offset_loc,
            (dst == NULL)? &out_reserved : &dst->reserved);
    return_if_error(ret, "Error unmarshaling subfield reserved");

    ret = Tss2_MU_TPM2B_CONTEXT_DATA_Unmarshal(buffer, size, &offset_loc,
            (dst == NULL)? NULL : &dst->tpmContext);
    return_if_error(ret, "Error unmarshaling subfield tpmContext");

    IESYS_METADATA out_esysMetadata;
    ret = iesys_MU_IESYS_METADATA_Unmarshal(buffer, size, &offset_loc,
            (dst == NULL)? &out_esysMetadata : &dst->esysMetadata);
    return_if_error(ret, "Error unmarshaling subfield esysMetadata");

    if (offset != NULL)
        *offset = offset_loc;
    return TSS2_RC_SUCCESS;
}
