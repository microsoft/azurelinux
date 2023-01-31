/* SPDX-License-Identifier: BSD-2-Clause */
/*******************************************************************************
 * Copyright 2017-2018, Fraunhofer SIT sponsored by Infineon Technologies AG
 * All rights reserved.
 ******************************************************************************/
#ifndef ESYS_CRYPTO_H
#define ESYS_CRYPTO_H

#include <stddef.h>
#include "tss2_tpm2_types.h"
#include "tss2-sys/sysapi_util.h"
#if defined(OSSL)
#include "esys_crypto_ossl.h"
#elif defined(MBED)
#include "esys_crypto_mbed.h"
#else
#define _iesys_crypto_aes_decrypt NULL;
#define _iesys_crypto_aes_encrypt NULL;
#define _iesys_crypto_get_ecdh_point NULL;
#define _iesys_crypto_hash_abort NULL;
#define _iesys_crypto_hash_finish NULL;
#define _iesys_crypto_hash_start NULL;
#define _iesys_crypto_hash_update NULL;
#define _iesys_crypto_hmac_abort NULL;
#define _iesys_crypto_hmac_finish NULL;
#define _iesys_crypto_hmac_start NULL;
#define _iesys_crypto_hmac_update NULL;
#define _iesys_crypto_init NULL;
#define _iesys_crypto_get_random2b NULL;
#define _iesys_crypto_rsa_pk_encrypt NULL;
#endif

#ifdef __cplusplus
extern "C" {
#endif

#define AES_BLOCK_SIZE_IN_BYTES 16

TSS2_RC iesys_crypto_hash_get_digest_size(TPM2_ALG_ID hashAlg, size_t *size);

TSS2_RC iesys_crypto_pHash(
    ESYS_CRYPTO_CALLBACKS *crypto_cb,
    TPM2_ALG_ID alg,
    const uint8_t rcBuffer[4],
    const uint8_t ccBuffer[4],
    const TPM2B_NAME *name1,
    const TPM2B_NAME *name2,
    const TPM2B_NAME *name3,
    const uint8_t *pBuffer,
    size_t pBuffer_size,
    uint8_t *pHash,
    size_t *pHash_size);

#define iesys_crypto_cpHash(ectx, alg, ccBuffer, name1, name2, name3, \
                            cpBuffer, cpBuffer_size, cpHash, cpHash_size) \
        iesys_crypto_pHash(ectx, alg, NULL, ccBuffer, name1, name2, name3, cpBuffer, \
                           cpBuffer_size, cpHash, cpHash_size)
#define iesys_crypto_rpHash(ectx, alg, rcBuffer, ccBuffer, rpBuffer, rpBuffer_size, \
                            rpHash, rpHash_size)                        \
        iesys_crypto_pHash(ectx, alg, rcBuffer, ccBuffer, NULL, NULL, NULL, rpBuffer, \
                           rpBuffer_size, rpHash, rpHash_size)

TSS2_RC iesys_crypto_hmac_finish2b(
    ESYS_CRYPTO_CALLBACKS *crypto_cb,
    ESYS_CRYPTO_CONTEXT_BLOB ** context,
    TPM2B *tpm2b);

TSS2_RC iesys_crypto_hmac_update2b(
    ESYS_CRYPTO_CALLBACKS *crypto_cb,
    ESYS_CRYPTO_CONTEXT_BLOB * context,
    TPM2B *tpm2b);

TSS2_RC iesys_crypto_hash_update2b(
    ESYS_CRYPTO_CALLBACKS *crypto_cb,
    ESYS_CRYPTO_CONTEXT_BLOB * context,
    TPM2B *tpm2b);

TSS2_RC iesys_crypto_rsa_pk_encrypt(
    ESYS_CRYPTO_CALLBACKS *crypto_cb,
    TPM2B_PUBLIC * pub_tpm_key,
    size_t in_size,
    BYTE * in_buffer,
    size_t max_out_size,
    BYTE * out_buffer,
    size_t * out_size,
    const char *label);

TSS2_RC iesys_crypto_hash_start(
    ESYS_CRYPTO_CALLBACKS *crypto_cb,
    ESYS_CRYPTO_CONTEXT_BLOB **context,
    TPM2_ALG_ID hashAlg);

TSS2_RC  iesys_crypto_hash_update(
    ESYS_CRYPTO_CALLBACKS *crypto_cb,
    ESYS_CRYPTO_CONTEXT_BLOB *context,
    const uint8_t *buffer,
    size_t size);

TSS2_RC iesys_crypto_hash_finish(
    ESYS_CRYPTO_CALLBACKS *crypto_cb,
    ESYS_CRYPTO_CONTEXT_BLOB ** context,
    uint8_t *buffer,
    size_t *size);

TSS2_RC iesys_crypto_hash_abort(
    ESYS_CRYPTO_CALLBACKS *crypto_cb,
    ESYS_CRYPTO_CONTEXT_BLOB **context);

TSS2_RC iesys_crypto_hmac_start(
    ESYS_CRYPTO_CALLBACKS *crypto_cb,
    ESYS_CRYPTO_CONTEXT_BLOB **context,
   TPM2_ALG_ID hashAlg,
   const uint8_t *key,
   size_t size);

TSS2_RC iesys_crypto_hmac_update(
    ESYS_CRYPTO_CALLBACKS *crypto_cb,
    ESYS_CRYPTO_CONTEXT_BLOB * context,
    const uint8_t *buffer,
    size_t size);

TSS2_RC iesys_crypto_hmac_finish(
    ESYS_CRYPTO_CALLBACKS *crypto_cb,
    ESYS_CRYPTO_CONTEXT_BLOB **context,
    uint8_t *buffer,
    size_t * size);

TSS2_RC iesys_crypto_hmac_abort(
    ESYS_CRYPTO_CALLBACKS *crypto_cb,
    ESYS_CRYPTO_CONTEXT_BLOB **context);

TSS2_RC iesys_crypto_get_random2b(
    ESYS_CRYPTO_CALLBACKS *crypto_cb,
    TPM2B_NONCE *nonce,
    size_t num_bytes);

TSS2_RC iesys_crypto_get_ecdh_point(
    ESYS_CRYPTO_CALLBACKS *crypto_cb,
    TPM2B_PUBLIC *key,
    size_t max_out_size,
    TPM2B_ECC_PARAMETER *Z,
    TPMS_ECC_POINT *Q,
    BYTE * out_buffer,
    size_t * out_size);

 TSS2_RC iesys_crypto_aes_encrypt(
    ESYS_CRYPTO_CALLBACKS *crypto_cb,
    uint8_t *key,
    TPM2_ALG_ID tpm_sym_alg,
    TPMI_AES_KEY_BITS key_bits,
    TPM2_ALG_ID tpm_mode,
    uint8_t *buffer,
    size_t buffer_size,
    uint8_t *iv);

TSS2_RC iesys_crypto_aes_decrypt(
    ESYS_CRYPTO_CALLBACKS *crypto_cb,
    uint8_t *key,
    TPM2_ALG_ID tpm_sym_alg,
    TPMI_AES_KEY_BITS key_bits,
    TPM2_ALG_ID tpm_mode,
    uint8_t *buffer,
    size_t buffer_size,
    uint8_t *iv);

TSS2_RC iesys_crypto_authHmac(
    ESYS_CRYPTO_CALLBACKS *crypto_cb,
    TPM2_ALG_ID alg,
    uint8_t *hmacKey,
    size_t hmacKeySize,
    const uint8_t *pHash,
    size_t pHash_size,
    const TPM2B_NONCE *nonceNewer,
    const TPM2B_NONCE *nonceOlder,
    const TPM2B_NONCE *nonceDecrypt,
    const TPM2B_NONCE *nonceEncrypt,
    TPMA_SESSION sessionAttributes,
    TPM2B_AUTH *hmac);

TSS2_RC iesys_crypto_KDFaHmac(
    ESYS_CRYPTO_CALLBACKS *crypto_cb,
    TPM2_ALG_ID alg,
    uint8_t *hmacKey,
    size_t hmacKeySize,
    uint32_t counter,
    const char *label,
    TPM2B_NONCE *contextU,
    TPM2B_NONCE *contextV,
    uint32_t bitlength,
    uint8_t *hmac,
    size_t *hmacSize);

TSS2_RC iesys_crypto_KDFa(
    ESYS_CRYPTO_CALLBACKS *crypto_cb,
    TPM2_ALG_ID hashAlg,
    uint8_t *hmacKey,
    size_t hmacKeySize,
    const char *label,
    TPM2B_NONCE *contextU,
    TPM2B_NONCE *contextV,
    uint32_t bitLength,
    uint32_t *counterInOut,
    BYTE *outKey,
    BOOL use_digest_size);

TSS2_RC iesys_xor_parameter_obfuscation(
    ESYS_CRYPTO_CALLBACKS *cryto_cb,
    TPM2_ALG_ID hash_alg,
    uint8_t *key,
    size_t key_size,
    TPM2B_NONCE * contextU,
    TPM2B_NONCE * contextV,
    BYTE *data,
    size_t data_size);

TSS2_RC iesys_crypto_KDFe(
    ESYS_CRYPTO_CALLBACKS *crypto_cb,
    TPM2_ALG_ID hashAlg,
    TPM2B_ECC_PARAMETER *Z,
    const char *label,
    TPM2B_ECC_PARAMETER *partyUInfo,
    TPM2B_ECC_PARAMETER *partyVInfo,
    UINT32 bit_size,
    BYTE *key);

TSS2_RC iesys_initialize_crypto_backend(
    ESYS_CRYPTO_CALLBACKS *crypto_cb,
    ESYS_CRYPTO_CALLBACKS *user_cb);

#ifdef __cplusplus
} /* extern "C" */
#endif

#endif /* ESYS_CRYPTO_H */
