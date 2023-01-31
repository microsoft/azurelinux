/* SPDX-License-Identifier: BSD-2-Clause */
/*******************************************************************************
 * Copyright 2017-2018, Fraunhofer SIT sponsored by Infineon Technologies AG
 * All rights reserved.
 ******************************************************************************/

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <openssl/rand.h>
#include <openssl/evp.h>
#include <openssl/rsa.h>
#include <openssl/ec.h>
#if OPENSSL_VERSION_NUMBER < 0x30000000L
#include <openssl/aes.h>
#else
#include <openssl/core_names.h>
#include <openssl/params.h>
#include <openssl/param_build.h>
#endif
#include <openssl/engine.h>
#include <stdio.h>

#include "tss2_esys.h"

#include "esys_crypto.h"
#include "esys_crypto_ossl.h"

#include "esys_iutil.h"
#include "esys_mu.h"
#define LOGMODULE esys_crypto
#include "util/log.h"
#include "util/aux_util.h"

#if OPENSSL_VERSION_NUMBER >= 0x10101000L
#define EC_POINT_set_affine_coordinates_tss(group, tpm_pub_key, bn_x, bn_y, dmy) \
        EC_POINT_set_affine_coordinates(group, tpm_pub_key, bn_x, bn_y, dmy)

#define EC_POINT_get_affine_coordinates_tss(group, tpm_pub_key, bn_x, bn_y, dmy) \
        EC_POINT_get_affine_coordinates(group, tpm_pub_key, bn_x, bn_y, dmy)

#else
#define EC_POINT_set_affine_coordinates_tss(group, tpm_pub_key, bn_x, bn_y, dmy) \
        EC_POINT_set_affine_coordinates_GFp(group, tpm_pub_key, bn_x, bn_y, dmy)

#define EC_POINT_get_affine_coordinates_tss(group, tpm_pub_key, bn_x, bn_y, dmy) \
        EC_POINT_get_affine_coordinates_GFp(group, tpm_pub_key, bn_x, bn_y, dmy)
#endif /* OPENSSL_VERSION_NUMBER >= 0x10101000L */

static int
iesys_bn2binpad(const BIGNUM *bn, unsigned char *bin, int bin_length)
{
    int len_bn = BN_num_bytes(bn);
    int offset = bin_length - len_bn;
    memset(bin,0,offset);
    BN_bn2bin(bn, bin + offset);
    return 1;
}

/** Context to hold temporary values for iesys_crypto */
typedef struct ESYS_CRYPTO_CONTEXT_BLOB {
    enum {
        IESYS_CRYPTOSSL_TYPE_HASH = 1,
        IESYS_CRYPTOSSL_TYPE_HMAC,
    } type; /**< The type of context to hold; hash or hmac */
    union {
        struct {
#if OPENSSL_VERSION_NUMBER < 0x30000000L
            const EVP_MD *ossl_hash_alg;
#else
            OSSL_LIB_CTX *ossl_libctx;
            EVP_MD *ossl_hash_alg;
#endif
            EVP_MD_CTX  *ossl_context;
            size_t hash_len;
        } hash; /**< the state variables for a HASH or HMAC context */
    };
} IESYS_CRYPTOSSL_CONTEXT;

static IESYS_CRYPTOSSL_CONTEXT *
iesys_cryptossl_context_new() {
    IESYS_CRYPTOSSL_CONTEXT *ctx;

    if (!(ctx = calloc(1, sizeof(IESYS_CRYPTOSSL_CONTEXT))))
        return NULL;

#if OPENSSL_VERSION_NUMBER >= 0x30000000L
    /* The TPM2 provider may be loaded in the global library context.
     * As we don't want the TPM to be called for these operations, we have
     * to initialize own library context with the default provider. */
    if (!(ctx->hash.ossl_libctx = OSSL_LIB_CTX_new())) {
        SAFE_FREE(ctx);
        return NULL;
    }
#endif
    return ctx;
}

static void
iesys_cryptossl_context_free(IESYS_CRYPTOSSL_CONTEXT *ctx) {
    if (!ctx)
        return;

    EVP_MD_CTX_free(ctx->hash.ossl_context);
#if OPENSSL_VERSION_NUMBER >= 0x30000000L
    EVP_MD_free(ctx->hash.ossl_hash_alg);
    OSSL_LIB_CTX_free(ctx->hash.ossl_libctx);
#endif
    SAFE_FREE(ctx);
}

#if OPENSSL_VERSION_NUMBER < 0x30000000L
static const EVP_MD *
get_ossl_hash_md(TPM2_ALG_ID hashAlg)
{
    switch (hashAlg) {
    case TPM2_ALG_SHA1:
        return EVP_sha1();
    case TPM2_ALG_SHA256:
        return EVP_sha256();
    case TPM2_ALG_SHA384:
        return EVP_sha384();
    case TPM2_ALG_SHA512:
        return EVP_sha512();
#if HAVE_EVP_SM3 && !defined(OPENSSL_NO_SM3)
    case TPM2_ALG_SM3_256:
        return EVP_sm3();
#endif
    default:
        return NULL;
    }
}
#else
static const char *
get_ossl_hash_md(TPM2_ALG_ID hashAlg)
{
    switch (hashAlg) {
    case TPM2_ALG_SHA1:
        return "SHA1";
    case TPM2_ALG_SHA256:
        return "SHA256";
    case TPM2_ALG_SHA384:
        return "SHA384";
    case TPM2_ALG_SHA512:
        return "SHA512";
    case TPM2_ALG_SM3_256:
        return "SM3";
    default:
        return NULL;
    }
}
#endif

static int
iesys_cryptossl_context_set_hash_md(IESYS_CRYPTOSSL_CONTEXT *ctx, TPM2_ALG_ID hashAlg) {
#if OPENSSL_VERSION_NUMBER < 0x30000000L
    ctx->hash.ossl_hash_alg = get_ossl_hash_md(hashAlg);
#else
    const char *alg_name =  get_ossl_hash_md(hashAlg);
    if (!alg_name)
        return 0;
    ctx->hash.ossl_hash_alg = EVP_MD_fetch(ctx->hash.ossl_libctx, alg_name, NULL);
#endif
    if (!ctx->hash.ossl_hash_alg)
        return 0;

    return 1;
}

/** Provide the context for the computation of a hash digest.
 *
 * The context will be created and initialized according to the hash function.
 * @param[out] context The created context (callee-allocated).
 * @param[in] hashAlg The hash algorithm for the creation of the context.
 * @retval TSS2_RC_SUCCESS on success.
 * @retval TSS2_ESYS_RC_BAD_VALUE or TSS2_ESYS_RC_BAD_REFERENCE for invalid parameters.
 * @retval TSS2_ESYS_RC_MEMORY Memory cannot be allocated.
 * @retval TSS2_ESYS_RC_GENERAL_FAILURE for errors of the crypto library.
 */
TSS2_RC
iesys_cryptossl_hash_start(ESYS_CRYPTO_CONTEXT_BLOB ** context,
                           TPM2_ALG_ID hashAlg,
                           void *userdata)
{
    UNUSED(userdata);

    TSS2_RC r = TSS2_RC_SUCCESS;
    LOG_TRACE("call: context=%p hashAlg=%"PRIu16, context, hashAlg);
    return_if_null(context, "Context is NULL", TSS2_ESYS_RC_BAD_REFERENCE);
    return_if_null(context, "Null-Pointer passed for context", TSS2_ESYS_RC_BAD_REFERENCE);

    IESYS_CRYPTOSSL_CONTEXT *mycontext = iesys_cryptossl_context_new();
    return_if_null(mycontext, "Out of Memory", TSS2_ESYS_RC_MEMORY);
    mycontext->type = IESYS_CRYPTOSSL_TYPE_HASH;

    if (!iesys_cryptossl_context_set_hash_md(mycontext, hashAlg)) {
        goto_error(r, TSS2_ESYS_RC_NOT_IMPLEMENTED,
                   "Unsupported hash algorithm (%"PRIu16")", cleanup, hashAlg);
    }

    if (iesys_crypto_hash_get_digest_size(hashAlg, &mycontext->hash.hash_len)) {
        goto_error(r, TSS2_ESYS_RC_NOT_IMPLEMENTED,
                   "Unsupported hash algorithm (%"PRIu16")", cleanup, hashAlg);
    }

    if (!(mycontext->hash.ossl_context = EVP_MD_CTX_create())) {
        goto_error(r, TSS2_ESYS_RC_GENERAL_FAILURE, "Error EVP_MD_CTX_create", cleanup);
    }

    if (1 != EVP_DigestInit(mycontext->hash.ossl_context,
                            mycontext->hash.ossl_hash_alg)) {
        goto_error(r, TSS2_ESYS_RC_GENERAL_FAILURE, "Errror EVP_DigestInit", cleanup);
    }

    *context = (ESYS_CRYPTO_CONTEXT_BLOB *) mycontext;

    return TSS2_RC_SUCCESS;

 cleanup:
    iesys_cryptossl_context_free(mycontext);

    return r;
}

/** Update the digest value of a digest object from a byte buffer.
 *
 * The context of a digest object will be updated according to the hash
 * algorithm of the context. <
 * @param[in,out] context The context of the digest object which will be updated.
 * @param[in] buffer The data for the update.
 * @param[in] size The size of the data buffer.
 * @retval TSS2_RC_SUCCESS on success.
 * @retval TSS2_ESYS_RC_BAD_REFERENCE for invalid parameters.
 */
TSS2_RC
iesys_cryptossl_hash_update(ESYS_CRYPTO_CONTEXT_BLOB * context,
                            const uint8_t * buffer, size_t size,
                            void *userdata)
{
    UNUSED(userdata);

    LOG_TRACE("called for context %p, buffer %p and size %zd", context, buffer,
              size);
    if (context == NULL || buffer == NULL) {
        LOG_ERROR("Null-Pointer passed");
        return TSS2_ESYS_RC_BAD_REFERENCE;
    }
    IESYS_CRYPTOSSL_CONTEXT *mycontext = (IESYS_CRYPTOSSL_CONTEXT *) context;
    if (mycontext->type != IESYS_CRYPTOSSL_TYPE_HASH) {
        LOG_ERROR("bad context");
        return TSS2_ESYS_RC_BAD_REFERENCE;
    }

    LOGBLOB_TRACE(buffer, size, "Updating hash with");

    if (1 != EVP_DigestUpdate(mycontext->hash.ossl_context, buffer, size)) {
        return_error(TSS2_ESYS_RC_GENERAL_FAILURE, "OSSL hash update");
    }

    return TSS2_RC_SUCCESS;
}

/** Get the digest value of a digest object and close the context.
 *
 * The digest value will written to a passed buffer and the resources of the
 * digest object are released.
 * @param[in,out] context The context of the digest object to be released
 * @param[out] buffer The buffer for the digest value (caller-allocated).
 * @param[out] size The size of the digest.
 * @retval TSS2_RC_SUCCESS on success.
 * @retval TSS2_ESYS_RC_BAD_REFERENCE for invalid parameters.
 * @retval TSS2_ESYS_RC_GENERAL_FAILURE for errors of the crypto library.
 */
TSS2_RC
iesys_cryptossl_hash_finish(ESYS_CRYPTO_CONTEXT_BLOB ** context,
                            uint8_t * buffer, size_t * size,
                            void *userdata)
{
    UNUSED(userdata);

    unsigned int digest_size = 0;

    LOG_TRACE("called for context-pointer %p, buffer %p and size-pointer %p",
              context, buffer, size);
    if (context == NULL || *context == NULL || buffer == NULL || size == NULL) {
        return_error(TSS2_ESYS_RC_BAD_REFERENCE, "Null-Pointer passed");
    }
    IESYS_CRYPTOSSL_CONTEXT *mycontext = * context;
    if (mycontext->type != IESYS_CRYPTOSSL_TYPE_HASH) {
        return_error(TSS2_ESYS_RC_BAD_REFERENCE, "bad context");
    }

    if (*size < mycontext->hash.hash_len) {
        return_error(TSS2_ESYS_RC_BAD_SIZE, "Buffer too small");
    }

    if (1 != EVP_DigestFinal(mycontext->hash.ossl_context, buffer, &digest_size)) {
        return_error(TSS2_ESYS_RC_GENERAL_FAILURE, "Ossl error.");
    }

    if (digest_size != mycontext->hash.hash_len) {
        return_error(TSS2_ESYS_RC_GENERAL_FAILURE,
                     "Invalid size computed by EVP_DigestFinal");
    }

    LOGBLOB_TRACE(buffer, mycontext->hash.hash_len, "read hash result");

    *size = mycontext->hash.hash_len;

    iesys_cryptossl_context_free(mycontext);
    *context = NULL;

    return TSS2_RC_SUCCESS;
}

/** Release the resources of a digest object.
 *
 * The assigned resources will be released and the context will be set to NULL.
 * @param[in,out] context The context of the digest object.
 */
void
iesys_cryptossl_hash_abort(
    ESYS_CRYPTO_CONTEXT_BLOB **context,
    void *userdata)
{
    UNUSED(userdata);

    LOG_TRACE("called for context-pointer %p", context);
    if (context == NULL || *context == NULL) {
        LOG_DEBUG("Null-Pointer passed");
        return;
    }
    IESYS_CRYPTOSSL_CONTEXT *mycontext =
        (IESYS_CRYPTOSSL_CONTEXT *) * context;
    if (mycontext->type != IESYS_CRYPTOSSL_TYPE_HASH) {
        LOG_DEBUG("bad context");
        return;
    }

    iesys_cryptossl_context_free(mycontext);
    *context = NULL;
}

/* HMAC */

/** Provide the context an HMAC digest object from a byte buffer key.
 *
 * The context will be created and initialized according to the hash function
 * and the used HMAC key.
 * @param[out] context The created context (callee-allocated).
 * @param[in] hashAlg The hash algorithm for the HMAC computation.
 * @param[in] key The byte buffer of the HMAC key.
 * @param[in] size The size of the HMAC key.
 * @retval TSS2_RC_SUCCESS on success.
 * @retval TSS2_ESYS_RC_BAD_REFERENCE for invalid parameters.
 * @retval TSS2_ESYS_RC_MEMORY Memory cannot be allocated.
 * @retval TSS2_ESYS_RC_GENERAL_FAILURE for errors of the crypto library.
 */
TSS2_RC
iesys_cryptossl_hmac_start(ESYS_CRYPTO_CONTEXT_BLOB ** context,
                           TPM2_ALG_ID hashAlg,
                           const uint8_t * key, size_t size,
                           void *userdata)
{
    UNUSED(userdata);

    TSS2_RC r = TSS2_RC_SUCCESS;
    EVP_PKEY *hkey = NULL;

    LOG_TRACE("called for context-pointer %p and hmacAlg %d", context, hashAlg);
    LOGBLOB_TRACE(key, size, "Starting  hmac with");
    if (context == NULL || key == NULL) {
        return_error(TSS2_ESYS_RC_BAD_REFERENCE,
                     "Null-Pointer passed in for context");
    }
    IESYS_CRYPTOSSL_CONTEXT *mycontext = iesys_cryptossl_context_new();
    return_if_null(mycontext, "Out of Memory", TSS2_ESYS_RC_MEMORY);

    if (!iesys_cryptossl_context_set_hash_md(mycontext, hashAlg)) {
        goto_error(r, TSS2_ESYS_RC_NOT_IMPLEMENTED,
                   "Unsupported hash algorithm (%"PRIu16")", cleanup, hashAlg);
    }

    if (iesys_crypto_hash_get_digest_size(hashAlg, &mycontext->hash.hash_len)) {
        goto_error(r, TSS2_ESYS_RC_GENERAL_FAILURE,
                   "Unsupported hash algorithm (%"PRIu16")", cleanup, hashAlg);
    }

    if (!(mycontext->hash.ossl_context = EVP_MD_CTX_create())) {
        goto_error(r, TSS2_ESYS_RC_GENERAL_FAILURE,
                   "Error EVP_MD_CTX_create", cleanup);
    }

#if OPENSSL_VERSION_NUMBER < 0x10101000L
    if (!(hkey = EVP_PKEY_new_mac_key(EVP_PKEY_HMAC, NULL, key, size))) {
#else
    /* this is preferred, but available since OpenSSL 1.1.1 only */
    if (!(hkey = EVP_PKEY_new_raw_private_key(EVP_PKEY_HMAC, NULL, key, size))) {
#endif
        goto_error(r, TSS2_ESYS_RC_GENERAL_FAILURE,
                   "Failed to create HMAC key", cleanup);
    }

    if(1 != EVP_DigestSignInit(mycontext->hash.ossl_context, NULL,
                               mycontext->hash.ossl_hash_alg, NULL, hkey)) {
        goto_error(r, TSS2_ESYS_RC_GENERAL_FAILURE,
                   "DigestSignInit", cleanup);
    }

    mycontext->type = IESYS_CRYPTOSSL_TYPE_HMAC;

    *context = (ESYS_CRYPTO_CONTEXT_BLOB *) mycontext;

    EVP_PKEY_free(hkey);

    return TSS2_RC_SUCCESS;

 cleanup:
    if(hkey)
        EVP_PKEY_free(hkey);
    iesys_cryptossl_context_free(mycontext);
    return r;
}

/** Update and HMAC digest value from a byte buffer.
 *
 * The context of a digest object will be updated according to the hash
 * algorithm and the key of the context.
 * @param[in,out] context The context of the digest object which will be updated.
 * @param[in] buffer The data for the update.
 * @param[in] size The size of the data buffer.
 * @retval TSS2_RC_SUCCESS on success.
 * @retval TSS2_ESYS_RC_BAD_REFERENCE for invalid parameters.
 */
TSS2_RC
iesys_cryptossl_hmac_update(ESYS_CRYPTO_CONTEXT_BLOB * context,
                            const uint8_t * buffer, size_t size,
                            void *userdata)
{
    UNUSED(userdata);

    LOG_TRACE("called for context %p, buffer %p and size %zd",
              context, buffer, size);
    if (context == NULL || buffer == NULL) {
        return_error(TSS2_ESYS_RC_BAD_REFERENCE, "Null-Pointer passed");
    }
    IESYS_CRYPTOSSL_CONTEXT *mycontext = (IESYS_CRYPTOSSL_CONTEXT *) context;
    if (mycontext->type != IESYS_CRYPTOSSL_TYPE_HMAC) {
        return_error(TSS2_ESYS_RC_BAD_REFERENCE, "bad context");
    }

    LOGBLOB_TRACE(buffer, size, "Updating hmac with");

    /* Call update with the message */
    if(1 != EVP_DigestSignUpdate(mycontext->hash.ossl_context, buffer, size)) {
        return_error(TSS2_ESYS_RC_GENERAL_FAILURE, "OSSL HMAC update");
    }

    return TSS2_RC_SUCCESS;
}

/** Write the HMAC digest value to a byte buffer and close the context.
 *
 * The digest value will written to a passed buffer and the resources of the
 * HMAC object are released.
 * @param[in,out] context The context of the HMAC object.
 * @param[out] buffer The buffer for the digest value (caller-allocated).
 * @param[out] size The size of the digest.
 * @retval TSS2_RC_SUCCESS on success.
 * @retval TSS2_ESYS_RC_BAD_REFERENCE for invalid parameters.
 * @retval TSS2_ESYS_RC_BAD_SIZE If the size passed is lower than the HMAC length.
 * @retval TSS2_ESYS_RC_GENERAL_FAILURE for errors of the crypto library.
 */
TSS2_RC
iesys_cryptossl_hmac_finish(ESYS_CRYPTO_CONTEXT_BLOB ** context,
                            uint8_t * buffer, size_t * size,
                            void *userdata)
{
    UNUSED(userdata);

    TSS2_RC r = TSS2_RC_SUCCESS;

    LOG_TRACE("called for context-pointer %p, buffer %p and size-pointer %p",
              context, buffer, size);
    if (context == NULL || *context == NULL || buffer == NULL || size == NULL) {
        return_error(TSS2_ESYS_RC_BAD_REFERENCE, "Null-Pointer passed");
    }
    IESYS_CRYPTOSSL_CONTEXT *mycontext =
        (IESYS_CRYPTOSSL_CONTEXT *) * context;
    if (mycontext->type != IESYS_CRYPTOSSL_TYPE_HMAC) {
        return_error(TSS2_ESYS_RC_BAD_REFERENCE, "bad context");
    }

    if (*size < mycontext->hash.hash_len) {
        return_error(TSS2_ESYS_RC_BAD_SIZE, "Buffer too small");
    }

    if (1 != EVP_DigestSignFinal(mycontext->hash.ossl_context, buffer, size)) {
        goto_error(r, TSS2_ESYS_RC_GENERAL_FAILURE, "DigestSignFinal", cleanup);
    }

    LOGBLOB_TRACE(buffer, *size, "read hmac result");

 cleanup:
    iesys_cryptossl_context_free(mycontext);
    *context = NULL;
    return r;
}

/** Release the resources of an HAMC object.
 *
 * The assigned resources will be released and the context will be set to NULL.
 * @param[in,out] context The context of the HMAC object.
 */
void
iesys_cryptossl_hmac_abort(
    ESYS_CRYPTO_CONTEXT_BLOB **context,
    void *userdata)
{
    UNUSED(userdata);

    LOG_TRACE("called for context-pointer %p", context);
    if (context == NULL || *context == NULL) {
        LOG_DEBUG("Null-Pointer passed");
        return;
    }
    if (*context != NULL) {
        IESYS_CRYPTOSSL_CONTEXT *mycontext =
            (IESYS_CRYPTOSSL_CONTEXT *) * context;
        if (mycontext->type != IESYS_CRYPTOSSL_TYPE_HMAC) {
            LOG_DEBUG("bad context");
            return;
        }

        iesys_cryptossl_context_free(mycontext);
        *context = NULL;
    }
}

/** Compute random TPM2B data.
 *
 * The random data will be generated and written to a passed TPM2B structure.
 * @param[out] nonce The TPM2B structure for the random data (caller-allocated).
 * @param[in] num_bytes The number of bytes to be generated.
 * @retval TSS2_RC_SUCCESS on success.
 *
 * NOTE: the TPM should not be used to obtain the random data
 */
TSS2_RC
iesys_cryptossl_random2b(
    TPM2B_NONCE *nonce,
    size_t num_bytes,
    void *userdata)
{
    UNUSED(userdata);

    int rc;
#if OPENSSL_VERSION_NUMBER < 0x30000000L
    const RAND_METHOD *rand_save = RAND_get_rand_method();
    RAND_set_rand_method(RAND_OpenSSL());
#else
    OSSL_LIB_CTX *libctx = OSSL_LIB_CTX_new();
    if (!libctx)
        return TSS2_ESYS_RC_MEMORY;
#endif

    if (num_bytes == 0) {
        nonce->size = sizeof(nonce->buffer);
    } else {
        nonce->size = num_bytes;
    }

#if OPENSSL_VERSION_NUMBER < 0x30000000L
    rc = RAND_bytes(&nonce->buffer[0], nonce->size);
    RAND_set_rand_method(rand_save);
#else
    rc = RAND_bytes_ex(libctx, &nonce->buffer[0], nonce->size, 0);
    OSSL_LIB_CTX_free(libctx);
#endif
    if (rc != 1)
        return_error(TSS2_ESYS_RC_GENERAL_FAILURE,
                     "Failure in random number generator.");
    return TSS2_RC_SUCCESS;
}

/** Encryption of a buffer using a public (RSA) key.
 *
 * Encrypting a buffer using a public key is used for example during
 * Esys_StartAuthSession in order to encrypt the salt value.
 * @param[in] pub_tpm_key The key to be used for encryption.
 * @param[in] in_size The size of the buffer to be encrypted.
 * @param[in] in_buffer The data buffer to be encrypted.
 * @param[in] max_out_size The maximum size for the output encrypted buffer.
 * @param[out] out_buffer The encrypted buffer.
 * @param[out] out_size The size of the encrypted output.
 * @param[in] label The label used in the encryption scheme.
 * @retval TSS2_RC_SUCCESS on success
 * @retval TSS2_ESYS_RC_BAD_VALUE The algorithm of key is not implemented.
 * @retval TSS2_ESYS_RC_GENERAL_FAILURE The internal crypto engine failed.
 */
TSS2_RC
iesys_cryptossl_pk_encrypt(TPM2B_PUBLIC * pub_tpm_key,
                           size_t in_size,
                           BYTE * in_buffer,
                           size_t max_out_size,
                           BYTE * out_buffer,
                           size_t * out_size,
                           const char *label,
                           void *userdata)
{
    UNUSED(userdata);

#if OPENSSL_VERSION_NUMBER < 0x30000000L
    RSA *rsa_key = NULL;
    const EVP_MD * hashAlg = NULL;
    const RAND_METHOD *rand_save = RAND_get_rand_method();

    RAND_set_rand_method(RAND_OpenSSL());
#else
    OSSL_LIB_CTX *libctx = NULL;
    EVP_MD * hashAlg = NULL;
    OSSL_PARAM *params = NULL;
    OSSL_PARAM_BLD *build = NULL;
#endif

    TSS2_RC r = TSS2_RC_SUCCESS;
    EVP_PKEY *evp_rsa_key = NULL;
    EVP_PKEY_CTX *genctx = NULL, *ctx = NULL;
    BIGNUM *bne = NULL, *n = NULL;
    int padding;
    char *label_copy = NULL;

#if OPENSSL_VERSION_NUMBER < 0x30000000L
    if (!(hashAlg = get_ossl_hash_md(pub_tpm_key->publicArea.nameAlg))) {
        RAND_set_rand_method(rand_save);
#else
    if (!(libctx = OSSL_LIB_CTX_new()))
        return TSS2_ESYS_RC_MEMORY;

    if (!(hashAlg = EVP_MD_fetch(libctx,
            get_ossl_hash_md(pub_tpm_key->publicArea.nameAlg), NULL))) {
        OSSL_LIB_CTX_free(libctx);
#endif
        LOG_ERROR("Unsupported hash algorithm (%"PRIu16")",
                  pub_tpm_key->publicArea.nameAlg);
        return TSS2_ESYS_RC_NOT_IMPLEMENTED;
    }

    switch (pub_tpm_key->publicArea.parameters.rsaDetail.scheme.scheme) {
    case TPM2_ALG_NULL:
        padding = RSA_NO_PADDING;
        break;
    case TPM2_ALG_RSAES:
        padding = RSA_PKCS1_PADDING;
        break;
    case TPM2_ALG_OAEP:
        padding = RSA_PKCS1_OAEP_PADDING;
        break;
    default:
        goto_error(r, TSS2_ESYS_RC_BAD_VALUE, "Illegal RSA scheme", cleanup);
    }

    UINT32 exp;
    if (pub_tpm_key->publicArea.parameters.rsaDetail.exponent == 0)
        exp = 65537;
    else
        exp = pub_tpm_key->publicArea.parameters.rsaDetail.exponent;

    if (!(n = BN_bin2bn(pub_tpm_key->publicArea.unique.rsa.buffer,
                        pub_tpm_key->publicArea.unique.rsa.size,
                        NULL))) {
        goto_error(r, TSS2_ESYS_RC_GENERAL_FAILURE,
                   "Could not create rsa n.", cleanup);
    }

#if OPENSSL_VERSION_NUMBER < 0x30000000L
    if (!(rsa_key = RSA_new())) {
        goto_error(r, TSS2_ESYS_RC_MEMORY,
                   "Could not allocate RSA key", cleanup);
    }

    if (!(bne = BN_new())) {
        goto_error(r, TSS2_ESYS_RC_MEMORY,
                   "Could not allocate Big Number", cleanup);
    }
    if (1 != BN_set_word(bne, exp)) {
        goto_error(r, TSS2_ESYS_RC_GENERAL_FAILURE,
                   "Could not set exponent.", cleanup);
    }

    if (1 != RSA_set0_key(rsa_key, n, bne, NULL)) {
        goto_error(r, TSS2_ESYS_RC_GENERAL_FAILURE,
                   "Could not set rsa n.", cleanup);
    }
    /* ownership got transferred */
    n = NULL;
    bne = NULL;

    if (!(evp_rsa_key = EVP_PKEY_new())) {
        goto_error(r, TSS2_ESYS_RC_GENERAL_FAILURE,
                   "Could not create evp key.", cleanup);
    }

    if (1 != EVP_PKEY_assign_RSA(evp_rsa_key, rsa_key)) {
        goto_error(r, TSS2_ESYS_RC_GENERAL_FAILURE,
                   "Could not set rsa key.", cleanup);
    }
    /* ownership got transferred */
    rsa_key = NULL;
#else /* OPENSSL_VERSION_NUMBER < 0x30000000L */
    if ((build = OSSL_PARAM_BLD_new()) == NULL
            || !OSSL_PARAM_BLD_push_BN(build, OSSL_PKEY_PARAM_RSA_N, n)
            || !OSSL_PARAM_BLD_push_uint32(build, OSSL_PKEY_PARAM_RSA_E, exp)
            || (params = OSSL_PARAM_BLD_to_param(build)) == NULL) {
        goto_error(r, TSS2_ESYS_RC_GENERAL_FAILURE, "Could not create rsa parameters.",
                   cleanup);
    }

    if ((genctx = EVP_PKEY_CTX_new_from_name(libctx, "RSA", NULL)) == NULL
            || EVP_PKEY_fromdata_init(genctx) <= 0
            || EVP_PKEY_fromdata(genctx, &evp_rsa_key, EVP_PKEY_PUBLIC_KEY, params) <= 0) {
        goto_error(r, TSS2_ESYS_RC_GENERAL_FAILURE, "Could not create rsa key.",
                   cleanup);
    }
#endif /* OPENSSL_VERSION_NUMBER < 0x30000000L */

    if (!(ctx = EVP_PKEY_CTX_new(evp_rsa_key, NULL))) {
        goto_error(r, TSS2_ESYS_RC_GENERAL_FAILURE,
                   "Could not create evp context.", cleanup);
    }

    if (1 != EVP_PKEY_encrypt_init(ctx)) {
        goto_error(r, TSS2_ESYS_RC_GENERAL_FAILURE,
                   "Could not init encrypt context.", cleanup);
    }

    if (1 != EVP_PKEY_CTX_set_rsa_padding(ctx, padding)) {
        goto_error(r, TSS2_ESYS_RC_GENERAL_FAILURE,
                   "Could not set RSA passing.", cleanup);
    }

    label_copy = OPENSSL_strdup(label);
    if (!label_copy) {
        goto_error(r, TSS2_ESYS_RC_MEMORY,
                   "Could not duplicate OAEP label", cleanup);
    }

    if (1 != EVP_PKEY_CTX_set0_rsa_oaep_label(ctx, label_copy, strlen(label_copy)+1)) {
        OPENSSL_free(label_copy);
        goto_error(r, TSS2_ESYS_RC_GENERAL_FAILURE,
                   "Could not set RSA label.", cleanup);
    }

    if (1 != EVP_PKEY_CTX_set_rsa_oaep_md(ctx, hashAlg)) {
        goto_error(r, TSS2_ESYS_RC_GENERAL_FAILURE,
                   "Could not set hash algorithm.", cleanup);
    }

    /* Determine out size */
    if (1 != EVP_PKEY_encrypt(ctx, NULL, out_size, in_buffer, in_size)) {
        goto_error(r, TSS2_ESYS_RC_GENERAL_FAILURE,
                   "Could not determine ciper size.", cleanup);
    }

    if ((size_t)*out_size > max_out_size) {
        goto_error(r, TSS2_ESYS_RC_GENERAL_FAILURE,
                   "Encrypted data too big", cleanup);
    }

    /* Encrypt data */
    if (1 != EVP_PKEY_encrypt(ctx, out_buffer, out_size, in_buffer, in_size)) {
        goto_error(r, TSS2_ESYS_RC_GENERAL_FAILURE,
                   "Could not encrypt data.", cleanup);
    }

    r = TSS2_RC_SUCCESS;

 cleanup:
    OSSL_FREE(genctx, EVP_PKEY_CTX);
    OSSL_FREE(ctx, EVP_PKEY_CTX);
    OSSL_FREE(evp_rsa_key, EVP_PKEY);
    OSSL_FREE(bne, BN);
    OSSL_FREE(n, BN);
#if OPENSSL_VERSION_NUMBER < 0x30000000L
    OSSL_FREE(rsa_key, RSA);
    RAND_set_rand_method(rand_save);
#else
    OSSL_FREE(params, OSSL_PARAM);
    OSSL_FREE(build, OSSL_PARAM_BLD);
    OSSL_FREE(hashAlg, EVP_MD);
    OSSL_FREE(libctx, OSSL_LIB_CTX);
#endif
    return r;
}

/** Computation of OSSL ec public point from TPM public point.
 *
 * @param[in] group The definition of the used ec curve.
 * @param[in] key The TPM public key.
 * @param[out] The TPM's public point in OSSL format.
 * @retval TSS2_RC_SUCCESS on success.
 * @retval TSS2_ESYS_RC_GENERAL_FAILURE The internal crypto engine failed.
 */
static TSS2_RC
tpm_pub_to_ossl_pub(EC_GROUP *group, TPM2B_PUBLIC *key, EC_POINT **tpm_pub_key)
{

    TSS2_RC r = TSS2_RC_SUCCESS;
    BIGNUM *bn_x = NULL;
    BIGNUM *bn_y = NULL;

    /* Create the big numbers for the coordinates of the point */
    if (!(bn_x = BN_bin2bn(&key->publicArea.unique.ecc.x.buffer[0],
                           key->publicArea.unique.ecc.x.size,
                           NULL))) {
        goto_error(r, TSS2_ESYS_RC_GENERAL_FAILURE,
                   "Create big num from byte buffer.", cleanup);
    }

    if (!(bn_y = BN_bin2bn(&key->publicArea.unique.ecc.y.buffer[0],
                           key->publicArea.unique.ecc.y.size,
                           NULL))) {
        goto_error(r, TSS2_ESYS_RC_GENERAL_FAILURE,
                   "Create big num from byte buffer.", cleanup);
    }

    /* Create the ec point with the affine coordinates of the TPM point */
    if (!(*tpm_pub_key = EC_POINT_new(group))) {
        goto_error(r, TSS2_ESYS_RC_GENERAL_FAILURE,
                   "Create point.", cleanup);
    }

    if (1 != EC_POINT_set_affine_coordinates_tss(group,
                                                 *tpm_pub_key, bn_x,
                                                 bn_y, NULL)) {
        OSSL_FREE(*tpm_pub_key, EC_POINT);
        goto_error(r, TSS2_ESYS_RC_GENERAL_FAILURE,
                   "Set affine coordinates", cleanup);
    }

    if (1 != EC_POINT_is_on_curve(group, *tpm_pub_key, NULL)) {
        goto_error(r, TSS2_ESYS_RC_GENERAL_FAILURE,
                   "The TPM point is not on the curve", cleanup);
    }

 cleanup:
    OSSL_FREE(bn_x, BN);
    OSSL_FREE(bn_y, BN);

    return r;
}

/** Computation of ephemeral ECC key and shared secret Z.
 *
 * According to the description in  TPM spec part 1 C 6.1 a shared secret
 * between application and TPM is computed (ECDH). An ephemeral ECC key and a
 * TPM keyare used for the ECDH key exchange.
 * @param[in] key The key to be used for ECDH key exchange.
 * @param[in] max_out_size the max size for the output of the public key of the
 *            computed ephemeral key.
 * @param[out] Z The computed shared secret.
 * @param[out] Q The public part of the ephemeral key in TPM format.
 * @param[out] out_buffer The public part of the ephemeral key will be marshaled
 *             to this buffer.
 * @param[out] out_size The size of the marshaled output.
 * @retval TSS2_RC_SUCCESS on success
 * @retval TSS2_ESYS_RC_BAD_VALUE The algorithm of key is not implemented.
 * @retval TSS2_ESYS_RC_GENERAL_FAILURE The internal crypto engine failed.
 */
TSS2_RC
iesys_cryptossl_get_ecdh_point(TPM2B_PUBLIC *key,
                               size_t max_out_size,
                               TPM2B_ECC_PARAMETER *Z,
                               TPMS_ECC_POINT *Q,
                               BYTE * out_buffer,
                               size_t * out_size,
                               void *userdata)
{
    UNUSED(userdata);

    TSS2_RC r = TSS2_RC_SUCCESS;
    EC_GROUP *group = NULL;               /* Group defines the used curve */
    EVP_PKEY_CTX *ctx = NULL;
    EVP_PKEY *eph_pkey = NULL;
#if OPENSSL_VERSION_NUMBER < 0x30000000L
    const EC_POINT *eph_pub_key = NULL;   /* Public part of ephemeral key */
    const BIGNUM *eph_priv_key = NULL;
#else
    BIGNUM *eph_priv_key = NULL;
#endif
    EC_POINT *tpm_pub_key = NULL;         /* Public part of TPM key */
    EC_POINT *mul_eph_tpm = NULL;
    BIGNUM *bn_x = NULL;
    BIGNUM *bn_y = NULL;
    size_t key_size;
    int curveId;
    size_t offset;

    /* Set ossl constant for curve type and create group for curve */
    switch (key->publicArea.parameters.eccDetail.curveID) {
    case TPM2_ECC_NIST_P192:
        curveId = NID_X9_62_prime192v1;
        key_size = 24;
        break;
    case TPM2_ECC_NIST_P224:
        curveId = NID_secp224r1;
        key_size = 28;
        break;
    case TPM2_ECC_NIST_P256:
        curveId = NID_X9_62_prime256v1;
        key_size = 32;
        break;
    case TPM2_ECC_NIST_P384:
        curveId = NID_secp384r1;
        key_size = 48;
        break;
    case TPM2_ECC_NIST_P521:
        curveId = NID_secp521r1;
        key_size = 66;
        break;
#if OPENSSL_VERSION_NUMBER >= 0x10101000L
    case TPM2_ECC_SM2_P256:
        curveId = NID_sm2;
        key_size = 32;
        break;
#endif
    default:
        return_error(TSS2_ESYS_RC_NOT_IMPLEMENTED,
                     "ECC curve not implemented.");
    }

    if (!(group = EC_GROUP_new_by_curve_name(curveId))) {
        goto_error(r, TSS2_ESYS_RC_GENERAL_FAILURE,
                   "Create group for curve", cleanup);
    }

    /* Create ephemeral key */
    if ((ctx = EVP_PKEY_CTX_new_id(EVP_PKEY_EC, NULL)) == NULL
            || EVP_PKEY_keygen_init(ctx) <= 0) {
        goto_error(r, TSS2_ESYS_RC_GENERAL_FAILURE,
                   "Initialize ec key generation", cleanup);
    }

    if (EVP_PKEY_CTX_set_ec_paramgen_curve_nid(ctx, curveId) <= 0
            || EVP_PKEY_keygen(ctx, &eph_pkey) <= 0) {
        goto_error(r, TSS2_ESYS_RC_GENERAL_FAILURE, "Generate ec key", cleanup);
    }

#if OPENSSL_VERSION_NUMBER < 0x30000000L
    EC_KEY *eph_ec_key = EVP_PKEY_get0_EC_KEY(eph_pkey);

    if (!(eph_pub_key =  EC_KEY_get0_public_key(eph_ec_key))) {
        goto_error(r, TSS2_ESYS_RC_GENERAL_FAILURE, "Get public key", cleanup);
    }

    eph_priv_key = EC_KEY_get0_private_key(eph_ec_key);
    if (1 != EC_POINT_is_on_curve(group, eph_pub_key, NULL)) {
        goto_error(r, TSS2_ESYS_RC_GENERAL_FAILURE,
                   "Ephemeral public key is on curve",cleanup);
    }

    /* Write affine coordinates of ephemeral pub key to TPM point Q */
    if (!(bn_x = BN_new())) {
        goto_error(r, TSS2_ESYS_RC_GENERAL_FAILURE, "Create bignum", cleanup);
    }

    if (!(bn_y = BN_new())) {
        goto_error(r, TSS2_ESYS_RC_GENERAL_FAILURE, "Create bignum", cleanup);
    }

    if (1 != EC_POINT_get_affine_coordinates_tss(group, eph_pub_key, bn_x,
                                                 bn_y, NULL)) {
        goto_error(r, TSS2_ESYS_RC_GENERAL_FAILURE,
                   "Get affine coordinates", cleanup);
    }
#else
    if (!EVP_PKEY_get_bn_param(eph_pkey, OSSL_PKEY_PARAM_PRIV_KEY, &eph_priv_key)
            || !EVP_PKEY_get_bn_param(eph_pkey, OSSL_PKEY_PARAM_EC_PUB_X, &bn_x)
            || !EVP_PKEY_get_bn_param(eph_pkey, OSSL_PKEY_PARAM_EC_PUB_Y, &bn_y)) {
        goto_error(r, TSS2_ESYS_RC_GENERAL_FAILURE,
                   "Get ephemeral key", cleanup);
    }
#endif

    if (1 != iesys_bn2binpad(bn_x, &Q->x.buffer[0], key_size)) {
        goto_error(r, TSS2_ESYS_RC_GENERAL_FAILURE,
                   "Write big num byte buffer", cleanup);
    }

    if (1 != iesys_bn2binpad(bn_y, &Q->y.buffer[0], key_size)) {
        goto_error(r, TSS2_ESYS_RC_GENERAL_FAILURE,
                   "Write big num byte buffer", cleanup);
    }

    Q->x.size = key_size;
    Q->y.size = key_size;

    /* Create an OSSL EC point from the TPM public point */
    r = tpm_pub_to_ossl_pub(group, key, &tpm_pub_key);
    goto_if_error(r, "Convert TPM pub point to ossl pub point", cleanup);

    if (!(mul_eph_tpm = EC_POINT_new(group))) {
        goto_error(r, TSS2_ESYS_RC_GENERAL_FAILURE, "Create point.", cleanup);
    }

    /* Multiply the ephemeral private key with TPM public key */
    if (1 != EC_POINT_mul(group, mul_eph_tpm, NULL,
                          tpm_pub_key, eph_priv_key, NULL)) {
        goto_error(r, TSS2_ESYS_RC_GENERAL_FAILURE,
                   "ec point multiplication", cleanup);
    }

    /* Write the x-part of the affine coordinate to Z */
    if (1 != EC_POINT_get_affine_coordinates_tss(group, mul_eph_tpm, bn_x,
                                                 bn_y, NULL)) {
        goto_error(r, TSS2_ESYS_RC_GENERAL_FAILURE,
                   "Get affine x coordinate", cleanup);
    }

    if (1 != iesys_bn2binpad(bn_x, &Z->buffer[0], key_size)) {
        goto_error(r, TSS2_ESYS_RC_GENERAL_FAILURE,
                   "Write big num byte buffer", cleanup);
    }

    Z->size = key_size;

    /* Write the public ephemeral key in TPM format to out buffer */
    offset = 0;
    r = Tss2_MU_TPMS_ECC_POINT_Marshal(Q,  &out_buffer[0], max_out_size, &offset);
    goto_if_error(r, "Error marshaling", cleanup);
    *out_size = offset;

 cleanup:
    OSSL_FREE(mul_eph_tpm, EC_POINT);
    OSSL_FREE(tpm_pub_key, EC_POINT);
    OSSL_FREE(group,EC_GROUP);
    OSSL_FREE(ctx, EVP_PKEY_CTX);
    OSSL_FREE(eph_pkey, EVP_PKEY);
#if OPENSSL_VERSION_NUMBER < 0x30000000L
    /* Note: free of eph_pub_key already done by free of eph_ec_key */
#else
    OSSL_FREE(eph_priv_key, BN);
#endif
    OSSL_FREE(bn_x, BN);
    OSSL_FREE(bn_y, BN);
    return r;
}

/** Encrypt data with AES.
 *
 * @param[in] key key used for AES.
 * @param[in] tpm_sym_alg AES type in TSS2 notation (must be TPM2_ALG_AES).
 * @param[in] key_bits Key size in bits.
 * @param[in] tpm_mode Block cipher mode of opertion in TSS2 notation (CFB).
 *            For parameter encryption only CFB can be used.
 * @param[in,out] buffer Data to be encrypted. The encrypted date will be stored
 *                in this buffer.
 * @param[in] buffer_size size of data to be encrypted.
 * @param[in] iv The initialization vector.
 * @retval TSS2_RC_SUCCESS on success, or TSS2_ESYS_RC_BAD_VALUE and
 * @retval TSS2_ESYS_RC_BAD_REFERENCE for invalid parameters,
 * @retval TSS2_ESYS_RC_GENERAL_FAILURE for errors of the crypto library.
 */
TSS2_RC
iesys_cryptossl_sym_aes_encrypt(uint8_t * key,
                                TPM2_ALG_ID tpm_sym_alg,
                                TPMI_AES_KEY_BITS key_bits,
                                TPM2_ALG_ID tpm_mode,
                                uint8_t * buffer,
                                size_t buffer_size,
                                uint8_t * iv,
                                void *userdata)
{
    UNUSED(userdata);

    TSS2_RC r = TSS2_RC_SUCCESS;
    const EVP_CIPHER  *cipher_alg = NULL;
    EVP_CIPHER_CTX *ctx = NULL;
    int cipher_len;

    if (key == NULL || buffer == NULL) {
        return_error(TSS2_ESYS_RC_BAD_REFERENCE, "Bad reference");
    }

    LOGBLOB_TRACE(buffer, buffer_size, "IESYS AES input");

    if (key_bits == 128 && tpm_mode == TPM2_ALG_CFB)
        cipher_alg = EVP_aes_128_cfb();
    else if (key_bits == 192 && tpm_mode == TPM2_ALG_CFB)
        cipher_alg = EVP_aes_192_cfb();
    else if (key_bits == 256 && tpm_mode == TPM2_ALG_CFB)
        cipher_alg = EVP_aes_256_cfb();
    else {
        goto_error(r, TSS2_ESYS_RC_BAD_VALUE,
                   "AES algorithm not implemented or illegal mode (CFB expected).",
                   cleanup);
    }

    if (tpm_sym_alg != TPM2_ALG_AES) {
        goto_error(r, TSS2_ESYS_RC_BAD_VALUE,
                   "AES encrypt called with wrong algorithm.", cleanup);
    }

    /* Create and initialize the context */
    if(!(ctx = EVP_CIPHER_CTX_new())) {
        goto_error(r, TSS2_ESYS_RC_GENERAL_FAILURE,
                   "Initialize cipher context", cleanup);
    }

    if (1 != EVP_EncryptInit(ctx, cipher_alg,key, iv)) {
        goto_error(r, TSS2_ESYS_RC_GENERAL_FAILURE,
                   "Initialize cipher operation", cleanup);
    }

    /* Perform the encryption */
    if (1 != EVP_EncryptUpdate(ctx, buffer, &cipher_len, buffer, buffer_size)) {
        goto_error(r, TSS2_ESYS_RC_GENERAL_FAILURE, "Encrypt update", cleanup);
    }

    if (1 != EVP_EncryptFinal(ctx, buffer, &cipher_len)) {
        goto_error(r, TSS2_ESYS_RC_GENERAL_FAILURE, "Encrypt final", cleanup);
    }
    LOGBLOB_TRACE(buffer, buffer_size, "IESYS AES output");

 cleanup:

    OSSL_FREE(ctx,EVP_CIPHER_CTX);

    return r;
}

/** Decrypt data with AES.
 *
 * @param[in] key key used for AES.
 * @param[in] tpm_sym_alg AES type in TSS2 notation (must be TPM2_ALG_AES).
 * @param[in] key_bits Key size in bits.
 * @param[in] tpm_mode Block cipher mode of opertion in TSS2 notation (CFB).
 *            For parameter encryption only CFB can be used.
 * @param[in,out] buffer Data to be decrypted. The decrypted date will be stored
 *                in this buffer.
 * @param[in] buffer_size size of data to be encrypted.
 * @param[in] iv The initialization vector.
 * @retval TSS2_RC_SUCCESS on success, or TSS2_ESYS_RC_BAD_VALUE and
 * @retval TSS2_ESYS_RC_BAD_REFERENCE for invalid parameters,
 * @retval TSS2_ESYS_RC_GENERAL_FAILURE for errors of the crypto library.
 */
TSS2_RC
iesys_cryptossl_sym_aes_decrypt(uint8_t * key,
                                TPM2_ALG_ID tpm_sym_alg,
                                TPMI_AES_KEY_BITS key_bits,
                                TPM2_ALG_ID tpm_mode,
                                uint8_t * buffer,
                                size_t buffer_size,
                                uint8_t * iv,
                                void *userdata)
{
    UNUSED(userdata);

    TSS2_RC r = TSS2_RC_SUCCESS;
    const EVP_CIPHER *cipher_alg = NULL;
    EVP_CIPHER_CTX *ctx = NULL;
    int cipher_len = 0;

    if (key == NULL || buffer == NULL) {
        return_error(TSS2_ESYS_RC_BAD_REFERENCE, "Bad reference");
    }

    if (tpm_sym_alg != TPM2_ALG_AES) {
        goto_error(r, TSS2_ESYS_RC_BAD_VALUE,
                   "AES encrypt called with wrong algorithm.", cleanup);
    }

    if (key_bits == 128 && tpm_mode == TPM2_ALG_CFB)
        cipher_alg = EVP_aes_128_cfb();
    else if (key_bits == 192 && tpm_mode == TPM2_ALG_CFB)
        cipher_alg = EVP_aes_192_cfb();
    else if (key_bits == 256 && tpm_mode == TPM2_ALG_CFB)
        cipher_alg = EVP_aes_256_cfb();
    else {

        goto_error(r, TSS2_ESYS_RC_NOT_IMPLEMENTED,
                   "AES algorithm not implemented.", cleanup);
    }

    /* Create and initialize the context */
    if(!(ctx = EVP_CIPHER_CTX_new())) {
        goto_error(r, TSS2_ESYS_RC_GENERAL_FAILURE,
                   "Initialize cipher context", cleanup);
    }

    LOGBLOB_TRACE(buffer, buffer_size, "IESYS AES input");

    if (1 != EVP_DecryptInit(ctx, cipher_alg, key, iv)) {
        goto_error(r, TSS2_ESYS_RC_GENERAL_FAILURE,
                   "Initialize cipher operation", cleanup);
    }

    /* Perform the decryption */
    if (1 != EVP_DecryptUpdate(ctx, buffer, &cipher_len, buffer, buffer_size)) {
        goto_error(r, TSS2_ESYS_RC_GENERAL_FAILURE, "Encrypt update", cleanup);
    }

    if (1 != EVP_DecryptFinal(ctx, buffer, &cipher_len)) {
        goto_error(r, TSS2_ESYS_RC_GENERAL_FAILURE, "Encrypt final", cleanup);
    }
    LOGBLOB_TRACE(buffer, buffer_size, "IESYS AES output");

 cleanup:

    OSSL_FREE(ctx,EVP_CIPHER_CTX);
    return r;
}


/** Initialize OpenSSL crypto backend.
 *
 * Initialize OpenSSL internal tables.
 *
 * @retval TSS2_RC_SUCCESS always returned
 * does not deliver
 * a return code.
 */
TSS2_RC
iesys_cryptossl_init(void *userdata)
{
    UNUSED(userdata);

    return TSS2_RC_SUCCESS;
}
