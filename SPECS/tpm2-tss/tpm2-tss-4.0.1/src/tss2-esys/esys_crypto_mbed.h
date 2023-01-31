/* SPDX-License-Identifier: BSD-2-Clause */
/*******************************************************************************
 * Copyright: 2020, Andreas Droescher
 * All rights reserved.
 ******************************************************************************/

#ifndef ESYS_CRYPTO_MBED_H
#define ESYS_CRYPTO_MBED_H

#include <stddef.h>
#include "tss2_tpm2_types.h"
#include "tss2-sys/sysapi_util.h"

#ifdef __cplusplus
extern "C" {
#endif

TSS2_RC iesys_cryptmbed_hash_start(
    ESYS_CRYPTO_CONTEXT_BLOB **context,
    TPM2_ALG_ID hashAlg,
    void *userdata);

TSS2_RC iesys_cryptmbed_hash_update(
    ESYS_CRYPTO_CONTEXT_BLOB *context,
    const uint8_t *buffer, size_t size,
    void *userdata);

TSS2_RC iesys_cryptmbed_hash_finish(
    ESYS_CRYPTO_CONTEXT_BLOB **context,
    uint8_t *buffer,
    size_t *size,
    void *userdata);

void iesys_cryptmbed_hash_abort(
    ESYS_CRYPTO_CONTEXT_BLOB **context,
    void *userdata);

#define _iesys_crypto_rsa_pk_encrypt iesys_cryptmbed_pk_encrypt
#define _iesys_crypto_hash_start iesys_cryptmbed_hash_start
#define _iesys_crypto_hash_update iesys_cryptmbed_hash_update
#define _iesys_crypto_hash_finish iesys_cryptmbed_hash_finish
#define _iesys_crypto_hash_abort iesys_cryptmbed_hash_abort

TSS2_RC iesys_cryptmbed_hmac_start(
    ESYS_CRYPTO_CONTEXT_BLOB **context,
    TPM2_ALG_ID hmacAlg,
    const uint8_t *key,
    size_t size,
    void *userdata);

TSS2_RC iesys_cryptmbed_hmac_update(
    ESYS_CRYPTO_CONTEXT_BLOB *context,
    const uint8_t *buffer,
    size_t size,
    void *userdata);

TSS2_RC iesys_cryptmbed_hmac_finish(
    ESYS_CRYPTO_CONTEXT_BLOB **context,
    uint8_t *buffer,
    size_t *size,
    void *userdata);

void iesys_cryptmbed_hmac_abort(
    ESYS_CRYPTO_CONTEXT_BLOB **context,
    void *userdata);

#define _iesys_crypto_hmac_start iesys_cryptmbed_hmac_start
#define _iesys_crypto_hmac_update iesys_cryptmbed_hmac_update
#define _iesys_crypto_hmac_finish iesys_cryptmbed_hmac_finish
#define _iesys_crypto_hmac_abort iesys_cryptmbed_hmac_abort

TSS2_RC iesys_cryptmbed_random2b(
    TPM2B_NONCE *nonce,
    size_t num_bytes,
    void *userdata);

TSS2_RC iesys_cryptmbed_pk_encrypt(
    TPM2B_PUBLIC *key,
    size_t in_size,
    BYTE *in_buffer,
    size_t max_out_size,
    BYTE *out_buffer,
    size_t *out_size,
    const char *label,
    void *userdata);


TSS2_RC iesys_cryptmbed_sym_aes_encrypt(
    uint8_t *key,
    TPM2_ALG_ID tpm_sym_alg,
    TPMI_AES_KEY_BITS key_bits,
    TPM2_ALG_ID tpm_mode,
    uint8_t *dst,
    size_t dst_size,
    uint8_t *iv,
    void *userdata);

TSS2_RC iesys_cryptmbed_sym_aes_decrypt(
    uint8_t *key,
    TPM2_ALG_ID tpm_sym_alg,
    TPMI_AES_KEY_BITS key_bits,
    TPM2_ALG_ID tpm_mode,
    uint8_t *dst,
    size_t dst_size,
    uint8_t *iv,
    void *userdata);

TSS2_RC iesys_cryptmbed_get_ecdh_point(
    TPM2B_PUBLIC *key,
    size_t max_out_size,
    TPM2B_ECC_PARAMETER *Z,
    TPMS_ECC_POINT *Q,
    BYTE * out_buffer,
    size_t * out_size,
    void *userdata);

TSS2_RC iesys_cryptmbed_init(void *userdata);

#define _iesys_crypto_get_random2b iesys_cryptmbed_random2b
#define _iesys_crypto_get_ecdh_point iesys_cryptmbed_get_ecdh_point
#define _iesys_crypto_aes_encrypt iesys_cryptmbed_sym_aes_encrypt
#define _iesys_crypto_aes_decrypt iesys_cryptmbed_sym_aes_decrypt

#define _iesys_crypto_init iesys_cryptmbed_init

#ifdef __cplusplus
} /* extern "C" */
#endif

#endif /* ESYS_CRYPTO_MBED_H */
