/* SPDX-License-Identifier: BSD-2-Clause */
/*******************************************************************************
 * Copyright 2017-2018, Fraunhofer SIT sponsored by Infineon Technologies AG
 * All rights reserved.
 ******************************************************************************/

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <stdio.h>

#include "tss2_esys.h"

#include "esys_crypto.h"
#include "esys_iutil.h"
#include "esys_mu.h"
#define LOGMODULE esys_crypto
#include "util/log.h"
#include "util/aux_util.h"

/** Provide the digest size for a given hash algorithm.
 *
 * This function provides the size of the digest for a given hash algorithm.
 *
 * @param[in] hashAlg The hash algorithm to get the size for.
 * @param[out] size The side of a digest of the hash algorithm.
 * @retval TSS2_RC_SUCCESS on success.
 * @retval TSS2_ESYS_RC_BAD_VALUE if hashAlg is unknown or unsupported.
 */
TSS2_RC
iesys_crypto_hash_get_digest_size(TPM2_ALG_ID hashAlg, size_t * size)
{
    LOG_TRACE("call: hashAlg=%"PRIu16" size=%p", hashAlg, size);
    if (size == NULL) {
        LOG_ERROR("Null-Pointer passed");
        return TSS2_ESYS_RC_BAD_REFERENCE;
    }
    switch (hashAlg) {
    case TPM2_ALG_SHA1:
        *size = TPM2_SHA1_DIGEST_SIZE;
        break;
    case TPM2_ALG_SHA256:
        *size = TPM2_SHA256_DIGEST_SIZE;
        break;
    case TPM2_ALG_SHA384:
        *size = TPM2_SHA384_DIGEST_SIZE;
        break;
    case TPM2_ALG_SHA512:
        *size = TPM2_SHA512_DIGEST_SIZE;
        break;
    case TPM2_ALG_SM3_256:
        *size = TPM2_SM3_256_DIGEST_SIZE;
        break;
    default:
        LOG_ERROR("Unsupported hash algorithm (%"PRIu16")", hashAlg);
        return TSS2_ESYS_RC_BAD_VALUE;
    }
    LOG_TRACE("return: *size=%zu", *size);
    return TSS2_RC_SUCCESS;
}

TSS2_RC iesys_crypto_hash_update2b(ESYS_CRYPTO_CALLBACKS *crypto_cb,
    ESYS_CRYPTO_CONTEXT_BLOB * context,
    TPM2B *tpm2b)
{
    return iesys_crypto_hash_update(crypto_cb, context, tpm2b->buffer, tpm2b->size);
}

TSS2_RC iesys_crypto_hmac_update2b(ESYS_CRYPTO_CALLBACKS *crypto_cb,
    ESYS_CRYPTO_CONTEXT_BLOB * context, TPM2B *tpm2b)
{
    return iesys_crypto_hmac_update(crypto_cb,
        context, tpm2b->buffer, tpm2b->size);
}

TSS2_RC iesys_crypto_hmac_finish2b(ESYS_CRYPTO_CALLBACKS *crypto_cb,
    ESYS_CRYPTO_CONTEXT_BLOB ** context, TPM2B *tpm2b)
{
    TSS2_RC r;
    size_t size = tpm2b->size;
    r = iesys_crypto_hmac_finish(crypto_cb,
        context, tpm2b->buffer, &size);
    tpm2b->size = size;
    return r;
}

#define DO_CALLBACK(callback, ...) \
    do { \
        if (!crypto_cb->callback) { \
            LOG_ERROR("Crypto callback \""str(callback)"\" not set"); \
            return TSS2_ESYS_RC_CALLBACK_NULL; \
        } \
        return crypto_cb->callback(__VA_ARGS__, crypto_cb->userdata); \
    } while (0)

TSS2_RC iesys_crypto_rsa_pk_encrypt(
    ESYS_CRYPTO_CALLBACKS *crypto_cb,
    TPM2B_PUBLIC * pub_tpm_key,
    size_t in_size,
    BYTE * in_buffer,
    size_t max_out_size,
    BYTE * out_buffer,
    size_t * out_size,
    const char *label)
{
    DO_CALLBACK(rsa_pk_encrypt,
            pub_tpm_key,
            in_size,
            in_buffer,
            max_out_size,
            out_buffer,
            out_size,
            label);
}

TSS2_RC iesys_crypto_hash_start(
    ESYS_CRYPTO_CALLBACKS *crypto_cb,
    ESYS_CRYPTO_CONTEXT_BLOB **context,
    TPM2_ALG_ID hashAlg)
{
    DO_CALLBACK(hash_start,
            context,
            hashAlg);
}

TSS2_RC  iesys_crypto_hash_update(
    ESYS_CRYPTO_CALLBACKS *crypto_cb,
    ESYS_CRYPTO_CONTEXT_BLOB *context,
    const uint8_t *buffer,
    size_t size)
{
    DO_CALLBACK(hash_update,
            context,
            buffer,
            size);
}

TSS2_RC iesys_crypto_hash_finish(
    ESYS_CRYPTO_CALLBACKS *crypto_cb,
    ESYS_CRYPTO_CONTEXT_BLOB ** context,
    uint8_t *buffer,
    size_t *size)
{
    DO_CALLBACK(hash_finish,
            context,
            buffer,
            size);
}

TSS2_RC iesys_crypto_hash_abort(
    ESYS_CRYPTO_CALLBACKS *crypto_cb,
    ESYS_CRYPTO_CONTEXT_BLOB **context)
{
    if (!crypto_cb->hash_abort) { \
        LOG_ERROR("Crypto callback \"hash_abort\" not set"); \
        return TSS2_ESYS_RC_CALLBACK_NULL;
    }

    crypto_cb->hash_abort(context, crypto_cb->userdata);
    return TSS2_RC_SUCCESS;
}

TSS2_RC iesys_crypto_hmac_start(
    ESYS_CRYPTO_CALLBACKS *crypto_cb,
    ESYS_CRYPTO_CONTEXT_BLOB **context,
   TPM2_ALG_ID hashAlg,
   const uint8_t *key,
   size_t size)
{
    DO_CALLBACK(hmac_start,
            context,
            hashAlg,
            key,
            size);
}

TSS2_RC iesys_crypto_hmac_update(
    ESYS_CRYPTO_CALLBACKS *crypto_cb,
    ESYS_CRYPTO_CONTEXT_BLOB * context,
    const uint8_t *buffer,
    size_t size)
{
    DO_CALLBACK(hmac_update,
            context,
            buffer,
            size);
}

TSS2_RC iesys_crypto_hmac_finish(
    ESYS_CRYPTO_CALLBACKS *crypto_cb,
    ESYS_CRYPTO_CONTEXT_BLOB **context,
    uint8_t *buffer,
    size_t * size)
{
    DO_CALLBACK(hmac_finish,
            context,
            buffer,
            size);
}

TSS2_RC iesys_crypto_hmac_abort(
    ESYS_CRYPTO_CALLBACKS *crypto_cb,
    ESYS_CRYPTO_CONTEXT_BLOB **context)
{
    if (!crypto_cb->hmac_abort) { \
        LOG_ERROR("Crypto callback \"hmac_abort\" not set"); \
        return TSS2_ESYS_RC_CALLBACK_NULL;
    }

    crypto_cb->hmac_abort(context, crypto_cb->userdata);
    return TSS2_RC_SUCCESS;
}

TSS2_RC iesys_crypto_get_random2b(
    ESYS_CRYPTO_CALLBACKS *crypto_cb,
    TPM2B_NONCE *nonce,
    size_t num_bytes)
{
    DO_CALLBACK(get_random2b,
            nonce,
            num_bytes);
}

TSS2_RC iesys_crypto_get_ecdh_point(
    ESYS_CRYPTO_CALLBACKS *crypto_cb,
    TPM2B_PUBLIC *key,
    size_t max_out_size,
    TPM2B_ECC_PARAMETER *Z,
    TPMS_ECC_POINT *Q,
    BYTE * out_buffer,
    size_t * out_size)
{
    DO_CALLBACK(get_ecdh_point,
            key,
            max_out_size,
            Z,
            Q,
            out_buffer,
            out_size);
}

 TSS2_RC iesys_crypto_aes_encrypt(
    ESYS_CRYPTO_CALLBACKS *crypto_cb,
    uint8_t *key,
    TPM2_ALG_ID tpm_sym_alg,
    TPMI_AES_KEY_BITS key_bits,
    TPM2_ALG_ID tpm_mode,
    uint8_t *buffer,
    size_t buffer_size,
    uint8_t *iv)
 {
     DO_CALLBACK(aes_encrypt,
             key,
             tpm_sym_alg,
             key_bits,
             tpm_mode,
             buffer,
             buffer_size,
             iv);
 }

TSS2_RC iesys_crypto_aes_decrypt(
    ESYS_CRYPTO_CALLBACKS *crypto_cb,
    uint8_t *key,
    TPM2_ALG_ID tpm_sym_alg,
    TPMI_AES_KEY_BITS key_bits,
    TPM2_ALG_ID tpm_mode,
    uint8_t *buffer,
    size_t buffer_size,
    uint8_t *iv)
{
    DO_CALLBACK(aes_decrypt,
            key,
            tpm_sym_alg,
            key_bits,
            tpm_mode,
            buffer,
            buffer_size,
            iv);
}

/** Compute the command or response parameter hash.
 *
 * These hashes are needed for the computation of the HMAC used for the
 * authorization of commands, or for the HMAC used for checking the responses.
 * The name parameters are only used for the command parameter hash (cp) and
 * must be NULL for the computation of the response parameter rp hash (rp).
 * @param[in] alg The hash algorithm.
 * @param[in] rcBuffer The response code in marshaled form.
 * @param[in] ccBuffer The command code in marshaled form.
 * @param[in] name1, name2, name3 The names associated with the corresponding
 *            handle. Must be NULL if no handle is passed.
 * @param[in] pBuffer The byte buffer or the command or the response.
 * @param[in] pBuffer_size The size of the command or response.
 * @param[out] pHash The result digest.
 * @param[out] pHash_size The size of the result digest.
 * @retval TSS2_RC_SUCCESS on success.
 * @retval TSS2_ESYS_RC_BAD_REFERENCE for invalid parameters.
 */
TSS2_RC
iesys_crypto_pHash(ESYS_CRYPTO_CALLBACKS *crypto_cb,
                   TPM2_ALG_ID alg,
                   const uint8_t rcBuffer[4],
                   const uint8_t ccBuffer[4],
                   const TPM2B_NAME * name1,
                   const TPM2B_NAME * name2,
                   const TPM2B_NAME * name3,
                   const uint8_t * pBuffer,
                   size_t pBuffer_size, uint8_t * pHash, size_t * pHash_size)
{
    LOG_TRACE("called");
    if (ccBuffer == NULL || pBuffer == NULL || pHash == NULL
        || pHash_size == NULL) {
        LOG_ERROR("Null-Pointer passed");
        return TSS2_ESYS_RC_BAD_REFERENCE;
    }

    ESYS_CRYPTO_CONTEXT_BLOB *cryptoContext;

    TSS2_RC r;
    r = iesys_crypto_hash_start(crypto_cb,
            &cryptoContext, alg);
    return_if_error(r, "Error");

    if (rcBuffer != NULL) {
        r = iesys_crypto_hash_update(crypto_cb,
                cryptoContext, &rcBuffer[0], 4);
        goto_if_error(r, "Error", error);
    }

    r = iesys_crypto_hash_update(crypto_cb,
        cryptoContext, &ccBuffer[0], 4);
    goto_if_error(r, "Error", error);

    if (name1 != NULL) {
        r = iesys_crypto_hash_update2b(crypto_cb, cryptoContext, (TPM2B *) name1);
        goto_if_error(r, "Error", error);
    }

    if (name2 != NULL) {
        r = iesys_crypto_hash_update2b(crypto_cb, cryptoContext, (TPM2B *) name2);
        goto_if_error(r, "Error", error);
    }

    if (name3 != NULL) {
        r = iesys_crypto_hash_update2b(crypto_cb, cryptoContext, (TPM2B *) name3);
        goto_if_error(r, "Error", error);
    }

    r = iesys_crypto_hash_update(crypto_cb,
        cryptoContext, pBuffer, pBuffer_size);
    goto_if_error(r, "Error", error);

    r = iesys_crypto_hash_finish(crypto_cb,
        &cryptoContext, pHash, pHash_size);
    goto_if_error(r, "Error", error);

    return r;

 error:
    iesys_crypto_hash_abort(crypto_cb, &cryptoContext);
    return r;
}

/** Compute the HMAC for authorization.
 *
 * Based on the session nonces, caller nonce, TPM nonce, if used encryption and
 * decryption nonce, the command parameter hash, and the session attributes the
 * HMAC used for authorization is computed.
 * @param[in] alg The hash algorithm used for HMAC computation.
 * @param[in] hmacKey The HMAC key byte buffer.
 * @param[in] hmacKeySize The size of the HMAC key byte buffer.
 * @param[in] pHash The command parameter hash byte buffer.
 * @param[in] pHash_size The size of the command parameter hash byte buffer.
 * @param[in] nonceNewer The TPM nonce.
 * @param[in] nonceOlder The caller nonce.
 * @param[in] nonceDecrypt The decrypt nonce (NULL if not used).
 * @param[in] nonceEncrypt The encrypt nonce (NULL if not used).
 * @param[in] sessionAttributes The attributes used for the current
 *            authentication.
 * @param[out] hmac The computed HMAC.
 * @retval TSS2_RC_SUCCESS on success
 * @retval TSS2_ESYS_RC_BAD_REFERENCE If a pointer is invalid.
 */
TSS2_RC
iesys_crypto_authHmac(ESYS_CRYPTO_CALLBACKS *crypto_cb,
                      TPM2_ALG_ID alg,
                      uint8_t * hmacKey, size_t hmacKeySize,
                      const uint8_t * pHash,
                      size_t pHash_size,
                      const TPM2B_NONCE * nonceNewer,
                      const TPM2B_NONCE * nonceOlder,
                      const TPM2B_NONCE * nonceDecrypt,
                      const TPM2B_NONCE * nonceEncrypt,
                      TPMA_SESSION sessionAttributes, TPM2B_AUTH * hmac)
{
    LOG_TRACE("called");
    if (hmacKey == NULL || pHash == NULL || nonceNewer == NULL ||
        nonceOlder == NULL || hmac == NULL) {
        LOG_ERROR("Null-Pointer passed");
        return TSS2_ESYS_RC_BAD_REFERENCE;
    }

    uint8_t sessionAttribs[sizeof(sessionAttributes)];
    size_t sessionAttribs_size = 0;

    ESYS_CRYPTO_CONTEXT_BLOB *cryptoContext;

    TSS2_RC r =
        iesys_crypto_hmac_start(crypto_cb, &cryptoContext, alg, hmacKey, hmacKeySize);
    return_if_error(r, "Error");

    r = iesys_crypto_hmac_update(crypto_cb, cryptoContext, pHash, pHash_size);
    goto_if_error(r, "Error", error);

    r = iesys_crypto_hmac_update2b(crypto_cb, cryptoContext, (TPM2B *) nonceNewer);
    goto_if_error(r, "Error", error);

    r = iesys_crypto_hmac_update2b(crypto_cb, cryptoContext, (TPM2B *) nonceOlder);
    goto_if_error(r, "Error", error);

    if (nonceDecrypt != NULL) {
        r = iesys_crypto_hmac_update2b(crypto_cb, cryptoContext, (TPM2B *) nonceDecrypt);
        goto_if_error(r, "Error", error);
    }

    if (nonceEncrypt != NULL) {
        iesys_crypto_hmac_update2b(crypto_cb, cryptoContext, (TPM2B *) nonceEncrypt);
        goto_if_error(r, "Error", error);
    }

    r = Tss2_MU_TPMA_SESSION_Marshal(sessionAttributes,
                                     &sessionAttribs[0],
                                     sizeof(sessionAttribs),
                                     &sessionAttribs_size);
    goto_if_error(r, "Error", error);

    r = iesys_crypto_hmac_update(crypto_cb, cryptoContext, &sessionAttribs[0],
                                 sessionAttribs_size);
    goto_if_error(r, "Error", error);

    r = iesys_crypto_hmac_finish2b(crypto_cb, &cryptoContext, (TPM2B *) hmac);
    goto_if_error(r, "Error", error);

    return r;

 error:
    iesys_crypto_hash_abort(crypto_cb, &cryptoContext);
    return r;

}

/**
 * HMAC computation for inner loop of KDFa key derivation.
 *
 * Except of ECDH this function is used for key derivation.
 * @param[in] alg The algorithm used for the HMAC.
 * @param[in] hmacKey The hmacKey used in KDFa.
 * @param[in] hmacKeySize The size of the HMAC key.
 * @param[in] counter The curren iteration step.
 * @param[in] label Indicates the use of the produced key.
 * @param[in] contextU, contextV are used for construction of a binary string
 *            containing information related to the derived key.
 * @param[in] bitlength The size of the generated key in bits.
 * @param[out] hmac Byte buffer for the generated HMAC key (caller-allocated).
 * @param[out] hmacSize  Size of the generated HMAC key.
 * @retval TSS2_RC_SUCCESS on success.
 * @retval TSS2_ESYS_RC_BAD_REFERENCE for invalid parameters.
 */
TSS2_RC
iesys_crypto_KDFaHmac(ESYS_CRYPTO_CALLBACKS *crypto_cb,
                      TPM2_ALG_ID alg,
                      uint8_t * hmacKey,
                      size_t hmacKeySize,
                      uint32_t counter,
                      const char *label,
                      TPM2B_NONCE * contextU,
                      TPM2B_NONCE * contextV,
                      uint32_t bitlength, uint8_t * hmac, size_t * hmacSize)
{
    LOG_TRACE("called");
    if (hmacKey == NULL || contextU == NULL || contextV == NULL) {
        LOG_ERROR("Null-Pointer passed");
        return TSS2_ESYS_RC_BAD_REFERENCE;
    }

    uint8_t buffer32[sizeof(uint32_t)];
    size_t buffer32_size = 0;

    ESYS_CRYPTO_CONTEXT_BLOB *cryptoContext;

    TSS2_RC r =
            iesys_crypto_hmac_start(crypto_cb, &cryptoContext, alg, hmacKey, hmacKeySize);
    return_if_error(r, "Error");

    r = Tss2_MU_UINT32_Marshal(counter, &buffer32[0], sizeof(UINT32),
                               &buffer32_size);
    goto_if_error(r, "Marsahling", error);
    r = iesys_crypto_hmac_update(crypto_cb, cryptoContext, &buffer32[0], buffer32_size);
    goto_if_error(r, "HMAC-Update", error);

    if (label != NULL) {
        size_t lsize = strlen(label) + 1;
        r = iesys_crypto_hmac_update(crypto_cb, cryptoContext, (uint8_t *) label, lsize);
        goto_if_error(r, "Error", error);
    }

    r = iesys_crypto_hmac_update2b(crypto_cb, cryptoContext, (TPM2B *) contextU);
    goto_if_error(r, "Error", error);

    r = iesys_crypto_hmac_update2b(crypto_cb, cryptoContext, (TPM2B *) contextV);
    goto_if_error(r, "Error", error);

    buffer32_size = 0;
    r = Tss2_MU_UINT32_Marshal(bitlength, &buffer32[0], sizeof(UINT32),
                               &buffer32_size);
    goto_if_error(r, "Marsahling", error);
    r = iesys_crypto_hmac_update(crypto_cb, cryptoContext, &buffer32[0], buffer32_size);
    goto_if_error(r, "Error", error);

    r = iesys_crypto_hmac_finish(crypto_cb, &cryptoContext, hmac, hmacSize);
    goto_if_error(r, "Error", error);

    return r;

 error:
    iesys_crypto_hmac_abort(crypto_cb, &cryptoContext);
    return r;
}

/**
 * KDFa Key derivation.
 *
 * Except of ECDH this function is used for key derivation.
 * @param[in] hashAlg The hash algorithm to use.
 * @param[in] hmacKey The hmacKey used in KDFa.
 * @param[in] hmacKeySize The size of the HMAC key.
 * @param[in] label Indicates the use of the produced key.
 * @param[in] contextU, contextV are used for construction of a binary string
 *            containing information related to the derived key.
 * @param[in] bitLength The size of generated key in bits.
 * @param[in,out] counterInOut Counter for the KDFa iterations. If set, the
 *                value will be used for the firt iteration step. The final
 *                counter value will be written to  counterInOut.
 * @param[out] outKey Byte buffer for the derived key (caller-allocated).
 * @param[in] use_digest_size Indicate whether the digest size of hashAlg is
 *            used as size of the generated key or the bitLength parameter is
 *            used.
 * @retval TSS2_RC_SUCCESS on success.
 * @retval TSS2_ESYS_RC_BAD_VALUE if hashAlg is unknown or unsupported.
 */
TSS2_RC
iesys_crypto_KDFa(ESYS_CRYPTO_CALLBACKS *crypto_cb,
                  TPM2_ALG_ID hashAlg,
                  uint8_t * hmacKey,
                  size_t hmacKeySize,
                  const char *label,
                  TPM2B_NONCE * contextU,
                  TPM2B_NONCE * contextV,
                  uint32_t bitLength,
                  uint32_t * counterInOut,
                  BYTE * outKey,
                  BOOL use_digest_size)
{
    LOG_DEBUG("IESYS KDFa hmac key hashAlg: %i label: %s bitLength: %i",
              hashAlg, label, bitLength);
    if (counterInOut != NULL)
        LOG_TRACE("IESYS KDFa hmac key counterInOut: %i", *counterInOut);
    LOGBLOB_DEBUG(hmacKey, hmacKeySize, "IESYS KDFa hmac key");

    LOGBLOB_DEBUG(&contextU->buffer[0], contextU->size,
                  "IESYS KDFa contextU key");
    LOGBLOB_DEBUG(&contextV->buffer[0], contextV->size,
                  "IESYS KDFa contextV key");
    BYTE *subKey = outKey;
    UINT32 counter = 0;
    INT32 bytes = 0;
    size_t hlen = 0;
    TSS2_RC r = iesys_crypto_hash_get_digest_size(hashAlg, &hlen);
    return_if_error(r, "Error");
    if (counterInOut != NULL)
        counter = *counterInOut;
    bytes = use_digest_size ? hlen : (bitLength + 7) / 8;
    LOG_DEBUG("IESYS KDFa hmac key bytes: %i", bytes);

     /* Fill outKey with results from KDFaHmac */
    for (; bytes > 0; subKey = &subKey[hlen], bytes = bytes - hlen) {
        LOG_TRACE("IESYS KDFa hmac key bytes: %i", bytes);
        //if(bytes < (INT32)hlen)
        //    hlen = bytes;
        counter++;
        r = iesys_crypto_KDFaHmac(crypto_cb, hashAlg, hmacKey,
                                  hmacKeySize, counter, label, contextU,
                                  contextV, bitLength, &subKey[0], &hlen);
        return_if_error(r, "Error");
    }
    if ((bitLength % 8) != 0)
        outKey[0] &= ((1 << (bitLength % 8)) - 1);
    if (counterInOut != NULL)
        *counterInOut = counter;
    LOGBLOB_DEBUG(outKey, (bitLength + 7) / 8, "IESYS KDFa key");
    return TPM2_RC_SUCCESS;
}

/** Compute KDFe as described in TPM spec part 1 C 6.1
 *
 * @param hashAlg [in] The nameAlg of the recipient key.
 * @param Z [in] the x coordinate (xP) of the product (P) of a public point and a
 *       private key.
 * @param label [in] KDF label.
 * @param partyUInfo [in] The x-coordinate of the secret exchange value (Qe,U).
 * @param partyVInfo [in] The x-coordinate of a public key (Qs,V).
 * @param bit_size [in] Bit size of generated key.
 * @param key [out] Key buffer.
 * @retval TSS2_RC_SUCCESS on success
 * @retval TSS2_ESYS_RC_BAD_REFERENCE for invalid parameters
 * @retval TSS2_ESYS_RC_MEMORY Memory cannot be allocated.
 */
TSS2_RC
iesys_crypto_KDFe(ESYS_CRYPTO_CALLBACKS *crypto_cb,
                  TPM2_ALG_ID hashAlg,
                  TPM2B_ECC_PARAMETER *Z,
                  const char *label,
                  TPM2B_ECC_PARAMETER *partyUInfo,
                  TPM2B_ECC_PARAMETER *partyVInfo,
                  UINT32 bit_size,
                  BYTE *key)
{
    TSS2_RC r = TSS2_RC_SUCCESS;
    size_t hash_len;
    INT16 byte_size = (INT16)((bit_size +7) / 8);
    BYTE *stream = key;
    ESYS_CRYPTO_CONTEXT_BLOB *cryptoContext;
    BYTE counter_buffer[4];
    UINT32 counter = 0;
    size_t offset;

    LOG_DEBUG("IESYS KDFe hashAlg: %i label: %s bitLength: %i",
              hashAlg, label, bit_size);
    if (partyUInfo != NULL)
        LOGBLOB_DEBUG(&partyUInfo->buffer[0], partyUInfo->size, "partyUInfo");
    if (partyVInfo != NULL)
        LOGBLOB_DEBUG(&partyVInfo->buffer[0], partyVInfo->size, "partyVInfo");
    r = iesys_crypto_hash_get_digest_size(hashAlg, &hash_len);
    return_if_error(r, "Hash algorithm not supported.");

    if(hashAlg == TPM2_ALG_NULL || byte_size == 0) {
        LOG_DEBUG("Bad parameters for KDFe");
        return TSS2_ESYS_RC_BAD_VALUE;
    }

    /* Fill seed key with hash of counter, Z, label, partyUInfo, and partyVInfo */
    for (; byte_size > 0; stream = &stream[hash_len], byte_size = byte_size - hash_len)
        {
            counter ++;
            r = iesys_crypto_hash_start(crypto_cb,
                &cryptoContext, hashAlg);
            return_if_error(r, "Error hash start");

            offset = 0;
            r = Tss2_MU_UINT32_Marshal(counter, &counter_buffer[0], 4, &offset);
            goto_if_error(r, "Error marshaling counter", error);

            r = iesys_crypto_hash_update(crypto_cb,
                    cryptoContext, &counter_buffer[0], 4);
            goto_if_error(r, "Error hash update", error);

            if (Z != NULL) {
                r = iesys_crypto_hash_update2b(crypto_cb, cryptoContext, (TPM2B *) Z);
                goto_if_error(r, "Error hash update2b", error);
            }

            if (label != NULL) {
                size_t lsize = strlen(label) + 1;
                r = iesys_crypto_hash_update(crypto_cb,
                    cryptoContext, (uint8_t *) label, lsize);
                goto_if_error(r, "Error hash update", error);
            }

            if (partyUInfo != NULL) {
                r = iesys_crypto_hash_update2b(crypto_cb, cryptoContext, (TPM2B *) partyUInfo);
                goto_if_error(r, "Error hash update2b", error);
            }

            if (partyVInfo != NULL) {
                r = iesys_crypto_hash_update2b(crypto_cb, cryptoContext,  (TPM2B *) partyVInfo);
               goto_if_error(r, "Error hash update2b", error);
            }
            r = iesys_crypto_hash_finish(crypto_cb,
                &cryptoContext, (uint8_t *) stream, &hash_len);
            goto_if_error(r, "Error", error);
        }
    LOGBLOB_DEBUG(key, bit_size/8, "Result KDFe");
    if((bit_size % 8) != 0)
        key[0] &= ((1 << (bit_size % 8)) - 1);
    return r;

 error:
    iesys_crypto_hmac_abort(crypto_cb, &cryptoContext);
    return r;
}

/** Encryption/Decryption using XOR obfuscation.
 *
 * The application of this function to data encrypted with this function will
 * produce the origin data. The key for XOR obfuscation will be derived with
 * KDFa form the passed key the session nonces, and the hash algorithm.
 * @param[in] hash_alg The algorithm used for key derivation.
 * @param[in] key key used for obfuscation
 * @param[in] key_size Key size in bits.
 * @param[in] contextU, contextV are used for construction of a binary string
 *            containing information related to the derived key.
 * @param[in,out] data Data to be encrypted/decrypted the result will be
 *                will be stored in this buffer.
 * @param[in] data_size size of data to be encrypted/decrypted.
 * @retval TSS2_RC_SUCCESS on success, or TSS2_ESYS_RC_BAD_VALUE and
 * @retval TSS2_ESYS_RC_BAD_REFERENCE for invalid parameters.
 */
TSS2_RC
iesys_xor_parameter_obfuscation(ESYS_CRYPTO_CALLBACKS *crypto_cb,
                                TPM2_ALG_ID hash_alg,
                                uint8_t *key,
                                size_t key_size,
                                TPM2B_NONCE * contextU,
                                TPM2B_NONCE * contextV,
                                BYTE *data,
                                size_t data_size)
{
    TSS2_RC r;
    uint32_t counter = 0;
    BYTE  kdfa_result[TPM2_MAX_DIGEST_BUFFER];
    size_t digest_size;
    size_t data_size_bits = data_size * 8;
    size_t rest_size = data_size;
    BYTE *kdfa_byte_ptr;
    BYTE *data_start MAYBE_UNUSED = data;

    if (key == NULL || data == NULL) {
        LOG_ERROR("Bad reference");
        return TSS2_ESYS_RC_BAD_REFERENCE;
    }

    r = iesys_crypto_hash_get_digest_size(hash_alg, &digest_size);
    return_if_error(r, "Hash alg not supported");
    while(rest_size > 0) {
        r = iesys_crypto_KDFa(crypto_cb, hash_alg, key, key_size, "XOR",
                              contextU, contextV, data_size_bits, &counter,
                              kdfa_result, TRUE);
        return_if_error(r, "iesys_crypto_KDFa failed");
        /* XOR next data sub block with KDFa result  */
        kdfa_byte_ptr = kdfa_result;
        LOGBLOB_TRACE(data_start, data_size, "Parameter data before XOR");
        for(size_t i = digest_size < rest_size ? digest_size : rest_size; i > 0;
            i--)
            *data++ ^= *kdfa_byte_ptr++;
        LOGBLOB_TRACE(data_start, data_size, "Parameter data after XOR");
        rest_size = rest_size < digest_size ? 0 : rest_size - digest_size;
    }
    return TSS2_RC_SUCCESS;
}

#define TEST_AND_SET_CALLBACK(crypto_cb, callbacks, fn) \
    if (callbacks->fn) { \
        crypto_cb->fn = callbacks->fn; \
    } else { \
        LOG_ERROR("Callback \"%s\" not set", xstr(fn)); \
        return TSS2_ESYS_RC_CALLBACK_NULL; \
    }

TSS2_RC
    ieys_set_crypto_callbacks(
                            ESYS_CRYPTO_CALLBACKS *crypto_cb,
                            ESYS_CRYPTO_CALLBACKS *user_cb)
{
    if (!user_cb) {
        /*
         * WARNING: Build time configured backends do not use the
         * userdata pointer, thus if they EVER need a backend
         * userdata pointer it must be saved and restored.
         */
        crypto_cb->userdata = NULL;
        crypto_cb->aes_decrypt = _iesys_crypto_aes_decrypt;
        crypto_cb->aes_encrypt = _iesys_crypto_aes_encrypt;
        crypto_cb->get_ecdh_point = _iesys_crypto_get_ecdh_point;
        crypto_cb->hash_abort = _iesys_crypto_hash_abort;
        crypto_cb->hash_finish = _iesys_crypto_hash_finish;
        crypto_cb->hash_start = _iesys_crypto_hash_start;
        crypto_cb->hash_update = _iesys_crypto_hash_update;
        crypto_cb->hmac_abort = _iesys_crypto_hmac_abort;
        crypto_cb->hmac_finish = _iesys_crypto_hmac_finish;
        crypto_cb->hmac_start = _iesys_crypto_hmac_start;
        crypto_cb->hmac_update = _iesys_crypto_hmac_update;
        crypto_cb->init = _iesys_crypto_init;
        crypto_cb->get_random2b = _iesys_crypto_get_random2b;
        crypto_cb->rsa_pk_encrypt = _iesys_crypto_rsa_pk_encrypt;

    } else {

        TEST_AND_SET_CALLBACK(crypto_cb, user_cb, aes_decrypt);
        TEST_AND_SET_CALLBACK(crypto_cb, user_cb, aes_encrypt);
        TEST_AND_SET_CALLBACK(crypto_cb, user_cb, get_ecdh_point);
        TEST_AND_SET_CALLBACK(crypto_cb, user_cb, get_random2b);
        TEST_AND_SET_CALLBACK(crypto_cb, user_cb, rsa_pk_encrypt);

        TEST_AND_SET_CALLBACK(crypto_cb, user_cb, hash_abort);
        TEST_AND_SET_CALLBACK(crypto_cb, user_cb, hash_finish);
        TEST_AND_SET_CALLBACK(crypto_cb, user_cb, hash_start);
        TEST_AND_SET_CALLBACK(crypto_cb, user_cb, hash_update);

        TEST_AND_SET_CALLBACK(crypto_cb, user_cb, hmac_abort);
        TEST_AND_SET_CALLBACK(crypto_cb, user_cb, hmac_finish);
        TEST_AND_SET_CALLBACK(crypto_cb, user_cb, hmac_start);
        TEST_AND_SET_CALLBACK(crypto_cb, user_cb, hmac_update);

        /* init is the only optional function */
        crypto_cb->init = user_cb->init;

        crypto_cb->userdata = user_cb->userdata;
    }

    return TSS2_RC_SUCCESS;
}

TSS2_RC
    iesys_initialize_crypto_backend(
                                    ESYS_CRYPTO_CALLBACKS *crypto_cb,
                                    ESYS_CRYPTO_CALLBACKS *user_cb)
{
    if (!crypto_cb) {
        return TSS2_ESYS_RC_BAD_REFERENCE;
    }

    TSS2_RC rc = ieys_set_crypto_callbacks(crypto_cb, user_cb);
    if (rc != TSS2_RC_SUCCESS) {
        return rc;
    }

    return crypto_cb->init ?
            crypto_cb->init(crypto_cb->userdata) : TSS2_RC_SUCCESS;
}
