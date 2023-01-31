/* SPDX-License-Identifier: BSD-2-Clause */
/*******************************************************************************
 * Copyright: 2020, Andreas Droescher
 * All rights reserved.
 ******************************************************************************/

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <stdlib.h>
#include <string.h>

#include <mbedtls/md.h>
#include <mbedtls/rsa.h>
#include <mbedtls/ecdh.h>
#include <mbedtls/aes.h>
#include <mbedtls/entropy.h>
#include <mbedtls/ctr_drbg.h>

#include "esys_iutil.h"
#include "esys_mu.h"
#define LOGMODULE esys_crypto
#include "util/log.h"
#include "util/aux_util.h"

#if MBEDTLS_VERSION_MAJOR > 2
#define MBEDTLS_ACCESS(member) MBEDTLS_PRIVATE(member)
#else
#define MBEDTLS_ACCESS(member) member
#endif

/** Context to hold temporary values for iesys_crypto */
typedef struct ESYS_CRYPTO_CONTEXT_BLOB {
    enum {
        IESYS_CRYPTMBED_TYPE_HASH = 1,
        IESYS_CRYPTMBED_TYPE_HMAC,
    } type; /**< The type of context to hold; hash or hmac */
    union {
        struct {
            mbedtls_md_context_t mbed_context;
            size_t hash_len;
        } hash; /**< the state variables for a hash context */
        struct {
            mbedtls_md_context_t mbed_context;
            size_t hmac_len;
        } hmac; /**< the state variables for an hmac context */
    };
} IESYS_CRYPTMBED_CONTEXT;

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
iesys_cryptmbed_hash_start(ESYS_CRYPTO_CONTEXT_BLOB ** context,
                           TPM2_ALG_ID hashAlg,
                           void *userdata)
{
    UNUSED(userdata);

    TSS2_RC r = TSS2_RC_SUCCESS;
    const mbedtls_md_info_t* md_info = NULL;

    if (context == NULL) {
        return_error(TSS2_ESYS_RC_BAD_REFERENCE,
                     "Null-Pointer passed in for context");
    }
    IESYS_CRYPTMBED_CONTEXT *mycontext = calloc(1, sizeof(IESYS_CRYPTMBED_CONTEXT));
    return_if_null(mycontext, "Out of Memory", TSS2_ESYS_RC_MEMORY);

    mbedtls_md_init(&mycontext->hash.mbed_context);

    switch(hashAlg) {
      case TPM2_ALG_SHA1:
          md_info = mbedtls_md_info_from_type(MBEDTLS_MD_SHA1);
          break;
      case TPM2_ALG_SHA256:
          md_info = mbedtls_md_info_from_type(MBEDTLS_MD_SHA256);
          break;
      case TPM2_ALG_SHA384:
          md_info = mbedtls_md_info_from_type(MBEDTLS_MD_SHA384);
          break;
    case TPM2_ALG_SHA512:
          md_info = mbedtls_md_info_from_type(MBEDTLS_MD_SHA384);
          break;
    }

    if (md_info == NULL) {
        goto_error(r, TSS2_ESYS_RC_NOT_IMPLEMENTED,
                   "Unsupported hash algorithm (%"PRIu16")", cleanup, hashAlg);
    }

    mycontext->hash.hash_len = mbedtls_md_get_size(md_info);

    if (mbedtls_md_setup(&mycontext->hash.mbed_context, md_info, true) != 0) {
        goto_error(r, TSS2_ESYS_RC_GENERAL_FAILURE,
                   "MBED HASH setup", cleanup);
    }

    if (mbedtls_md_starts(&mycontext->hash.mbed_context) != 0) {
        goto_error(r, TSS2_ESYS_RC_GENERAL_FAILURE,
                   "MBED HASH start", cleanup);
    }

    mycontext->type = IESYS_CRYPTMBED_TYPE_HASH;

    *context = (ESYS_CRYPTO_CONTEXT_BLOB *) mycontext;

    return TSS2_RC_SUCCESS;

 cleanup:
    mbedtls_md_free(&mycontext->hash.mbed_context);
    SAFE_FREE(mycontext);
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
iesys_cryptmbed_hash_update(ESYS_CRYPTO_CONTEXT_BLOB * context,
                            const uint8_t * buffer, size_t size,
                            void *userdata)
{
    UNUSED(userdata);

    if (context == NULL || buffer == NULL) {
        return_error(TSS2_ESYS_RC_BAD_REFERENCE, "Null-Pointer passed");
    }
    IESYS_CRYPTMBED_CONTEXT *mycontext = (IESYS_CRYPTMBED_CONTEXT *) context;
    if (mycontext->type != IESYS_CRYPTMBED_TYPE_HASH) {
        return_error(TSS2_ESYS_RC_BAD_REFERENCE, "bad context");
    }

    if (mbedtls_md_update(&mycontext->hash.mbed_context, buffer, size) != 0) {
        return_error(TSS2_ESYS_RC_GENERAL_FAILURE, "MBED HASH update");
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
iesys_cryptmbed_hash_finish(ESYS_CRYPTO_CONTEXT_BLOB ** context,
                            uint8_t * buffer, size_t * size,
                            void *userdata)
{
    UNUSED(userdata);

    TSS2_RC r = TSS2_RC_SUCCESS;

    if (context == NULL || *context == NULL || buffer == NULL || size == NULL) {
        return_error(TSS2_ESYS_RC_BAD_REFERENCE, "Null-Pointer passed");
    }
    IESYS_CRYPTMBED_CONTEXT *mycontext =
        (IESYS_CRYPTMBED_CONTEXT *) * context;
    if (mycontext->type != IESYS_CRYPTMBED_TYPE_HASH) {
        return_error(TSS2_ESYS_RC_BAD_REFERENCE, "bad context");
    }

    if (*size < mycontext->hash.hash_len) {
        return_error(TSS2_ESYS_RC_BAD_SIZE, "Buffer too small");
    }

    if (mbedtls_md_finish(&mycontext->hmac.mbed_context, buffer) != 0) {
        goto_error(r, TSS2_ESYS_RC_GENERAL_FAILURE, "MBED HASH finish", cleanup);
    }

    *size = mycontext->hash.hash_len;

 cleanup:
    mbedtls_md_free(&mycontext->hash.mbed_context);
    SAFE_FREE(mycontext);
    *context = NULL;

    return r;
}

/** Release the resources of a digest object.
 *
 * The assigned resources will be released and the context will be set to NULL.
 * @param[in,out] context The context of the digest object.
 */
void
iesys_cryptmbed_hash_abort(ESYS_CRYPTO_CONTEXT_BLOB ** context, void *userdata)
{
    UNUSED(userdata);

    if (context == NULL || *context == NULL) {
        return;
    }

    IESYS_CRYPTMBED_CONTEXT *mycontext =
        (IESYS_CRYPTMBED_CONTEXT *) * context;
    if (mycontext->type != IESYS_CRYPTMBED_TYPE_HASH) {
        return;
    }

    mbedtls_md_free(&mycontext->hash.mbed_context);
    free(mycontext);
    *context = NULL;
}

/* HMAC */

/** Provide the context an HMAC digest object from a byte buffer key.
 *
 * The context will be created and initialized according to the hash function
 * and the used HMAC key.
 * @param[out] context The created context (callee-allocated).
 * @param[in] hmacAlg The hash algorithm for the HMAC computation.
 * @param[in] key The byte buffer of the HMAC key.
 * @param[in] size The size of the HMAC key.
 * @retval TSS2_RC_SUCCESS on success.
 * @retval TSS2_ESYS_RC_BAD_REFERENCE for invalid parameters.
 * @retval TSS2_ESYS_RC_MEMORY Memory cannot be allocated.
 * @retval TSS2_ESYS_RC_GENERAL_FAILURE for errors of the crypto library.
 */
TSS2_RC
iesys_cryptmbed_hmac_start(ESYS_CRYPTO_CONTEXT_BLOB ** context,
                           TPM2_ALG_ID hashAlg,
                           const uint8_t * key, size_t size,
                           void *userdata)
{
    UNUSED(userdata);

    TSS2_RC r = TSS2_RC_SUCCESS;
    const mbedtls_md_info_t* md_info = NULL;

    if (context == NULL || key == NULL) {
        return_error(TSS2_ESYS_RC_BAD_REFERENCE,
                     "Null-Pointer passed in for context");
    }
    IESYS_CRYPTMBED_CONTEXT *mycontext = calloc(1, sizeof(IESYS_CRYPTMBED_CONTEXT));
    return_if_null(mycontext, "Out of Memory", TSS2_ESYS_RC_MEMORY);

    mbedtls_md_init(&mycontext->hash.mbed_context);

    switch(hashAlg) {
      case TPM2_ALG_SHA1:
          md_info = mbedtls_md_info_from_type(MBEDTLS_MD_SHA1);
          break;
      case TPM2_ALG_SHA256:
          md_info = mbedtls_md_info_from_type(MBEDTLS_MD_SHA256);
          break;
      case TPM2_ALG_SHA384:
          md_info = mbedtls_md_info_from_type(MBEDTLS_MD_SHA384);
          break;
    }

    if (md_info == NULL) {
        goto_error(r, TSS2_ESYS_RC_NOT_IMPLEMENTED,
                   "Unsupported hash algorithm (%"PRIu16")", cleanup, hashAlg);
    }

    mycontext->hmac.hmac_len = mbedtls_md_get_size(md_info);

    if (mbedtls_md_setup(&mycontext->hash.mbed_context, md_info, true) != 0) {
        goto_error(r, TSS2_ESYS_RC_GENERAL_FAILURE,
                   "MBED HMAC setup", cleanup);
    }

    if (mbedtls_md_hmac_starts(&mycontext->hash.mbed_context, key, size) != 0) {
        goto_error(r, TSS2_ESYS_RC_GENERAL_FAILURE,
                   "MBED HMAC start", cleanup);
    }

    mycontext->type = IESYS_CRYPTMBED_TYPE_HMAC;

    *context = (ESYS_CRYPTO_CONTEXT_BLOB *) mycontext;

    return TSS2_RC_SUCCESS;

 cleanup:
    mbedtls_md_free(&mycontext->hmac.mbed_context);
    SAFE_FREE(mycontext);
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
iesys_cryptmbed_hmac_update(ESYS_CRYPTO_CONTEXT_BLOB * context,
                            const uint8_t * buffer, size_t size,
                            void *userdata)
{
    UNUSED(userdata);

    if (context == NULL || buffer == NULL) {
        return_error(TSS2_ESYS_RC_BAD_REFERENCE, "Null-Pointer passed");
    }
    IESYS_CRYPTMBED_CONTEXT *mycontext = (IESYS_CRYPTMBED_CONTEXT *) context;
    if (mycontext->type != IESYS_CRYPTMBED_TYPE_HMAC) {
        return_error(TSS2_ESYS_RC_BAD_REFERENCE, "bad context");
    }

    if (mbedtls_md_hmac_update(&mycontext->hmac.mbed_context, buffer, size) != 0) {
        return_error(TSS2_ESYS_RC_GENERAL_FAILURE, "MBED HMAC update");
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
iesys_cryptmbed_hmac_finish(ESYS_CRYPTO_CONTEXT_BLOB ** context,
                            uint8_t * buffer, size_t * size,
                            void *userdata)
{
    UNUSED(userdata);

    TSS2_RC r = TSS2_RC_SUCCESS;

    if (context == NULL || *context == NULL || buffer == NULL || size == NULL) {
        return_error(TSS2_ESYS_RC_BAD_REFERENCE, "Null-Pointer passed");
    }
    IESYS_CRYPTMBED_CONTEXT *mycontext =
        (IESYS_CRYPTMBED_CONTEXT *) * context;
    if (mycontext->type != IESYS_CRYPTMBED_TYPE_HMAC) {
        return_error(TSS2_ESYS_RC_BAD_REFERENCE, "bad context");
    }

    if (*size < mycontext->hmac.hmac_len) {
        return_error(TSS2_ESYS_RC_BAD_SIZE, "Buffer too small");
    }

    if (mbedtls_md_hmac_finish(&mycontext->hmac.mbed_context, buffer) != 0) {
        goto_error(r, TSS2_ESYS_RC_GENERAL_FAILURE, "MBED HMAC finish", cleanup);
    }

    *size = mycontext->hmac.hmac_len;

 cleanup:
    mbedtls_md_free(&mycontext->hmac.mbed_context);
    SAFE_FREE(mycontext);
    *context = NULL;
    return r;
}

/** Release the resources of an HAMC object.
 *
 * The assigned resources will be released and the context will be set to NULL.
 * @param[in,out] context The context of the HMAC object.
 */
void
iesys_cryptmbed_hmac_abort(ESYS_CRYPTO_CONTEXT_BLOB ** context, void *userdata)
{
    UNUSED(userdata);

    if (context == NULL || *context == NULL) {
        return;
    }

    IESYS_CRYPTMBED_CONTEXT *mycontext =
        (IESYS_CRYPTMBED_CONTEXT *) * context;
    if (mycontext->type != IESYS_CRYPTMBED_TYPE_HMAC) {
        return;
    }

    mbedtls_md_free(&mycontext->hmac.mbed_context);
    free(mycontext);
    *context = NULL;
}

/** Wrapper for mbedtls random number generator
 *
 * @param[in] context Optional unused parameter.
 * @param[out] buffer Buffer to write randomness to.
 * @param[om] buf_size Number of bytes to write to buffer.
 */
static int get_random(void* context, unsigned char * buffer, size_t buf_size) {
    UNUSED(context);

    int r = 0; //success in terms of mbedtls

    mbedtls_entropy_context entropy_context;
    mbedtls_entropy_init(&entropy_context);

    mbedtls_ctr_drbg_context drbg_context;
    mbedtls_ctr_drbg_init(&drbg_context);

    if (mbedtls_ctr_drbg_seed(&drbg_context,
                              mbedtls_entropy_func,
                              &entropy_context,
                              NULL,
                              0) != 0) {
        goto_error(r, MBEDTLS_ERR_CTR_DRBG_ENTROPY_SOURCE_FAILED,
                   "Could not seed random number generator.", cleanup);
    }

    if (mbedtls_ctr_drbg_random(&drbg_context,
                                &buffer[0],
                                buf_size) != 0) {
        goto_error(r, MBEDTLS_ERR_CTR_DRBG_REQUEST_TOO_BIG,
                   "Failure in random number generator.", cleanup);
    }

cleanup:
    mbedtls_ctr_drbg_free(&drbg_context);
    mbedtls_entropy_free(&entropy_context);
    return r;
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
iesys_cryptmbed_random2b(TPM2B_NONCE * nonce, size_t num_bytes, void *userdata)
{
    UNUSED(userdata);

    if (num_bytes == 0) {
        nonce->size = sizeof(nonce->buffer);
    } else {
        nonce->size = num_bytes;
    }

    if (get_random(NULL, &nonce->buffer[0], nonce->size) != 0) {
        return_error(TSS2_ESYS_RC_GENERAL_FAILURE,
                     "Hash algorithm not supported");
    }

    return TSS2_RC_SUCCESS;
}

/** Encryption of a buffer using a public (RSA) key.
 *
 * Encrypting a buffer using a public key is used for example during
 * Esys_StartAuthSession in order to encrypt the salt value.
 * @param[in] key The key to be used for encryption.
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
iesys_cryptmbed_pk_encrypt(TPM2B_PUBLIC * pub_tpm_key,
                           size_t in_size,
                           BYTE * in_buffer,
                           size_t max_out_size,
                           BYTE * out_buffer,
                           size_t * out_size,
                           const char *label,
                           void *userdata)
{
    UNUSED(userdata);

    TSS2_RC r = TSS2_RC_SUCCESS;
    int hash_id = 0;
    mbedtls_rsa_context rsa_context;

    switch(pub_tpm_key->publicArea.nameAlg) {
        case TPM2_ALG_SHA1:
            hash_id = MBEDTLS_MD_SHA1;
            break;
        case TPM2_ALG_SHA256:
            hash_id = MBEDTLS_MD_SHA256;
            break;
        case TPM2_ALG_SHA384:
            hash_id = MBEDTLS_MD_SHA384;
            break;
        case TPM2_ALG_SHA512:
            hash_id = MBEDTLS_MD_SHA512;
            break;
        default:
            return_error(TSS2_ESYS_RC_NOT_IMPLEMENTED,
                         "Hash algorithm not supported");
    }

#if MBEDTLS_VERSION_MAJOR > 2
    mbedtls_rsa_init(&rsa_context);
    mbedtls_rsa_set_padding(&rsa_context, MBEDTLS_RSA_PKCS_V21, hash_id);
#else
    mbedtls_rsa_init(&rsa_context, MBEDTLS_RSA_PKCS_V21, hash_id);
#endif

    if (pub_tpm_key->publicArea.unique.rsa.size == 0) {
        goto_error(r, TSS2_ESYS_RC_BAD_VALUE,
                   "Public key size may not be 0", cleanup);
    }

    UINT8 exp[sizeof(UINT32)] = { 0x00, 0x01, 0x00, 0x01 }; //big-endian 65537
    UINT32 exp_as_int = pub_tpm_key->publicArea.parameters.rsaDetail.exponent;
    if (exp_as_int != 0) {
        exp[0] = (exp_as_int >> 24) & 0xff;
        exp[1] = (exp_as_int >> 16) & 0xff;
        exp[2] = (exp_as_int >>  8) & 0xff;
        exp[3] = (exp_as_int >>  0) & 0xff;
    }

    if (mbedtls_rsa_import_raw(&rsa_context,
                              pub_tpm_key->publicArea.unique.rsa.buffer,
                              pub_tpm_key->publicArea.unique.rsa.size,
                              NULL /* p */,
                              0,
                              NULL /* q */,
                              0,
                              NULL /* d */,
                              0,
                              &exp[0],
                              sizeof(UINT32)) != 0) {
        goto_error(r, TSS2_ESYS_RC_GENERAL_FAILURE,
                   "Could not import public key", cleanup);
    }

    if (mbedtls_rsa_complete(&rsa_context) != 0) {
        goto_error(r, TSS2_ESYS_RC_GENERAL_FAILURE,
                   "Could not complete key import", cleanup);
    }

    if (mbedtls_rsa_get_len(&rsa_context) > max_out_size) {
        goto_error(r, TSS2_ESYS_RC_GENERAL_FAILURE,
                   "Encrypted data too big", cleanup);
    }

    switch (pub_tpm_key->publicArea.parameters.rsaDetail.scheme.scheme) {
        case TPM2_ALG_RSAES:
            if (mbedtls_rsa_pkcs1_encrypt(&rsa_context,
                                          get_random,
                                          NULL,
#if MBEDTLS_VERSION_MAJOR <= 2
                                          MBEDTLS_RSA_PUBLIC,
#endif
                                          in_size,
                                          in_buffer,
                                          out_buffer) != 0) {
                goto_error(r, TSS2_ESYS_RC_GENERAL_FAILURE,
                           "Could not encrypt data.", cleanup);
            }
            break;
        case TPM2_ALG_OAEP:
            if (mbedtls_rsa_rsaes_oaep_encrypt(&rsa_context,
                                               get_random,
                                               NULL,
#if MBEDTLS_VERSION_MAJOR <= 2
                                               MBEDTLS_RSA_PUBLIC,
#endif
                                               (const UINT8*)label,
                                               strlen(label) + 1,
                                               in_size,
                                               in_buffer,
                                               out_buffer) != 0) {
                goto_error(r, TSS2_ESYS_RC_GENERAL_FAILURE,
                           "Could not encrypt data.", cleanup);
            }
            break;
        default:
            goto_error(r, TSS2_ESYS_RC_BAD_VALUE,
                       "Illegal RSA scheme", cleanup);
            break;
    }
    *out_size = mbedtls_rsa_get_len(&rsa_context);

    r = TSS2_RC_SUCCESS;

cleanup:
    mbedtls_rsa_free(&rsa_context);
    return r;
}

/** Computation of ephemeral ECC key and shared secret Z.
 *
 * According to the description in TPM spec part 1 C 6.1 a shared secret
 * between application and TPM is computed (ECDH). An ephemeral ECC key and a
 * TPM key are used for the ECDH key exchange.
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
iesys_cryptmbed_get_ecdh_point(TPM2B_PUBLIC *key,
                               size_t max_out_size,
                               TPM2B_ECC_PARAMETER *Z,
                               TPMS_ECC_POINT *Q,
                               BYTE * out_buffer,
                               size_t * out_size,
                               void *userdata)
{
    UNUSED(userdata);

    TSS2_RC r = TSS2_RC_SUCCESS;
    mbedtls_ecp_group ecp_group;
    mbedtls_mpi ecp_d;
    mbedtls_ecp_point ecp_Q;
    mbedtls_ecp_point ecp_Qp;
    mbedtls_mpi ecp_z;

    mbedtls_ecp_group_init(&ecp_group);
    mbedtls_mpi_init(&ecp_d);
    mbedtls_ecp_point_init(&ecp_Q);
    mbedtls_ecp_point_init(&ecp_Qp);
    mbedtls_mpi_init(&ecp_z);

    /* Load named curve */
    switch (key->publicArea.parameters.eccDetail.curveID) {
    case TPM2_ECC_NIST_P192:
        if(mbedtls_ecp_group_load(&ecp_group, MBEDTLS_ECP_DP_SECP192R1) != 0) {
            goto_error(r, TSS2_ESYS_RC_GENERAL_FAILURE,
                       "ECP group load failed", cleanup);
        }
        break;
    case TPM2_ECC_NIST_P224:
        if(mbedtls_ecp_group_load(&ecp_group, MBEDTLS_ECP_DP_SECP224R1) != 0) {
            goto_error(r, TSS2_ESYS_RC_GENERAL_FAILURE,
                       "ECP group load failed", cleanup);
        }
        break;
    case TPM2_ECC_NIST_P256:
        if(mbedtls_ecp_group_load(&ecp_group, MBEDTLS_ECP_DP_SECP256R1) != 0) {
            goto_error(r, TSS2_ESYS_RC_GENERAL_FAILURE,
                       "ECP group load failed", cleanup);
        }
        break;
    case TPM2_ECC_NIST_P384:
        if(mbedtls_ecp_group_load(&ecp_group, MBEDTLS_ECP_DP_SECP384R1) != 0) {
             goto_error(r, TSS2_ESYS_RC_GENERAL_FAILURE,
                        "ECP group load failed", cleanup);
        }
        break;
    case TPM2_ECC_NIST_P521:
        if(mbedtls_ecp_group_load(&ecp_group, MBEDTLS_ECP_DP_SECP521R1) != 0) {
            goto_error(r, TSS2_ESYS_RC_GENERAL_FAILURE,
                       "ECP group load failed", cleanup);
        }
        break;
    default:
        return_error(TSS2_ESYS_RC_NOT_IMPLEMENTED,
                     "ECC curve not implemented.");
    }

    /* Generate ephemeral key */
    if (mbedtls_ecdh_gen_public(&ecp_group,
                                &ecp_d,
                                &ecp_Q,
                                get_random,
                                NULL) != 0) {
        goto_error(r, TSS2_ESYS_RC_GENERAL_FAILURE,
                   "ECDH gen failed", cleanup);
    }

    /* Write affine coordinates of ephemeral pub key to TPM point Q
     *
     * Note
     * mpi_write_bin prepends numbers with 0 if they are smaller as
     * TPM2_MAX_ECC_KEY_BYTES. This is for big-endian mathematicaly
     * correct but breaks the interface if we want to set bignum.size
     * to anything but TPM2_MAX_ECC_KEY_BYTES. The easiest fix is
     * to shrink out_size to mpi_size.
     */

    Q->x.size = mbedtls_mpi_size(&ecp_Q.MBEDTLS_ACCESS(X));
    if (Q->x.size > TPM2_MAX_ECC_KEY_BYTES) {
        goto_error(r, TSS2_ESYS_RC_GENERAL_FAILURE,
                   "Write Q.x does not fit into byte buffer", cleanup);
    }
    if (mbedtls_mpi_write_binary(&ecp_Q.MBEDTLS_ACCESS(X),
                                 &Q->x.buffer[0],
                                 Q->x.size) != 0) {
        goto_error(r, TSS2_ESYS_RC_GENERAL_FAILURE,
                   "Write Q.x to byte buffer failed", cleanup);
    }

    Q->y.size = mbedtls_mpi_size(&ecp_Q.MBEDTLS_ACCESS(Y));
    if (Q->y.size > TPM2_MAX_ECC_KEY_BYTES) {
        goto_error(r, TSS2_ESYS_RC_GENERAL_FAILURE,
                   "Write Q.y does not fit into byte buffer", cleanup);
    }
    if (mbedtls_mpi_write_binary(&ecp_Q.MBEDTLS_ACCESS(Y),
                                 &Q->y.buffer[0],
                                 Q->y.size) != 0) {
        goto_error(r, TSS2_ESYS_RC_GENERAL_FAILURE,
                   "Write Q.y to byte buffer failed", cleanup);
    }

    /* Initialise Qp.Z (Qp would be zero, or "at infinity", if Z == 0) */
    if (mbedtls_mpi_lset(&ecp_Qp.MBEDTLS_ACCESS(Z), 1) != 0)
    {
        goto_error(r, TSS2_ESYS_RC_GENERAL_FAILURE,
                   "Init of Qp.z to 1 failed", cleanup);
    }

    /* Read ephemeral pub key from TPM to Qp */
    if (mbedtls_mpi_read_binary(&ecp_Qp.MBEDTLS_ACCESS(X),
                                &key->publicArea.unique.ecc.x.buffer[0],
                                key->publicArea.unique.ecc.x.size) != 0) {
        goto_error(r, TSS2_ESYS_RC_GENERAL_FAILURE,
                   "Read of Qp.x from byte buffer failed", cleanup);
    }
    if (mbedtls_mpi_read_binary(&ecp_Qp.MBEDTLS_ACCESS(Y),
                                &key->publicArea.unique.ecc.y.buffer[0],
                                key->publicArea.unique.ecc.y.size) != 0) {
        goto_error(r, TSS2_ESYS_RC_GENERAL_FAILURE,
                   "Read of Qp.y from byte buffer failed", cleanup);
    }

    /* Validate TPM's pub key */
    if (mbedtls_ecp_check_pubkey(&ecp_group,
                                 &ecp_Qp) != 0) {
        goto_error(r, TSS2_ESYS_RC_GENERAL_FAILURE,
                   "Point Qp is invalid", cleanup);
    }

    /* Calculate shared secret */
    if (mbedtls_ecdh_compute_shared(&ecp_group,
                                    &ecp_z,
                                    &ecp_Qp,
                                    &ecp_d,
                                    get_random,
                                    NULL) != 0) {
        goto_error(r, TSS2_ESYS_RC_GENERAL_FAILURE,
                   "ECDH compute shared failed", cleanup);
    }

    /* Write shared secret to TPM ECC param Z */
    Z->size = mbedtls_mpi_size(&ecp_z);
    if (Z->size > TPM2_MAX_ECC_KEY_BYTES) {
        goto_error(r, TSS2_ESYS_RC_GENERAL_FAILURE,
                   "Write Q.y does not fit into byte buffer", cleanup);
    }
    if (mbedtls_mpi_write_binary(&ecp_z,
                                 &Z->buffer[0],
                                 Z->size) != 0) {
        goto_error(r, TSS2_ESYS_RC_GENERAL_FAILURE,
                   "Write Z to byte buffer failed", cleanup);
    }

    /* Write the public ephemeral key in TPM format to out buffer */
    size_t offset = 0;
    r = Tss2_MU_TPMS_ECC_POINT_Marshal(Q, &out_buffer[0], max_out_size, &offset);
    goto_if_error(r, "Error marshaling Q", cleanup);
    *out_size = offset;

cleanup:
    mbedtls_mpi_free(&ecp_z);
    mbedtls_ecp_point_free(&ecp_Qp);
    mbedtls_ecp_point_free(&ecp_Q);
    mbedtls_mpi_free(&ecp_d);
    mbedtls_ecp_group_free(&ecp_group);
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
iesys_cryptmbed_sym_aes_encrypt(uint8_t * key,
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
    mbedtls_aes_context aes_ctx;

    if (key == NULL || buffer == NULL) {
        return_error(TSS2_ESYS_RC_BAD_REFERENCE, "Bad reference");
    }

    mbedtls_aes_init(&aes_ctx);

    if (tpm_sym_alg != TPM2_ALG_AES || tpm_mode != TPM2_ALG_CFB) {
        goto_error(r, TSS2_ESYS_RC_BAD_VALUE,
                   "AES encrypt called with wrong algorithm.", cleanup);
    }

    if (mbedtls_aes_setkey_enc(&aes_ctx, key, key_bits) != 0) {
        goto_error(r, TSS2_ESYS_RC_BAD_VALUE,
                   "Key size not not implemented.", cleanup);
    }

    size_t iv_off = 0;
    if (mbedtls_aes_crypt_cfb128(&aes_ctx, MBEDTLS_AES_ENCRYPT, buffer_size,
                                 &iv_off, iv, buffer, buffer) != 0) {
        goto_error(r, TSS2_ESYS_RC_GENERAL_FAILURE,
                   "Enncrypt", cleanup);
    }

cleanup:
    mbedtls_aes_free(&aes_ctx);
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
iesys_cryptmbed_sym_aes_decrypt(uint8_t * key,
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
    mbedtls_aes_context aes_ctx;

    if (key == NULL || buffer == NULL) {
        return_error(TSS2_ESYS_RC_BAD_REFERENCE, "Bad reference");
    }

    mbedtls_aes_init(&aes_ctx);

    if (tpm_sym_alg != TPM2_ALG_AES || tpm_mode != TPM2_ALG_CFB) {
        goto_error(r, TSS2_ESYS_RC_BAD_VALUE,
                   "AES encrypt called with wrong algorithm.", cleanup);
    }

    /* Note in mbedTLS Documentation:
     * For CFB, you must set up the context with mbedtls_aes_setkey_enc(),
     * regardless of whether you are performing an encryption or decryption
     * operation, that is, regardless of the mode parameter. This is because
     * CFB mode uses the same key schedule for encryption and decryption.
     */
    if (mbedtls_aes_setkey_enc(&aes_ctx, key, key_bits) != 0) {
        goto_error(r, TSS2_ESYS_RC_GENERAL_FAILURE,
                   "Key size not not implemented.", cleanup);
    }

    size_t iv_off = 0;
    if (mbedtls_aes_crypt_cfb128(&aes_ctx, MBEDTLS_AES_DECRYPT, buffer_size,
                                 &iv_off, iv, buffer, buffer) != 0) {
        goto_error(r, TSS2_ESYS_RC_GENERAL_FAILURE,
                   "Dencrypt", cleanup);
    }

cleanup:
    mbedtls_aes_free(&aes_ctx);
    return r;
}

TSS2_RC
iesys_cryptmbed_init(void *userdata) {
    UNUSED(userdata);

    return TSS2_RC_SUCCESS;
}
