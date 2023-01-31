/* SPDX-License-Identifier: BSD-2-Clause */
/*******************************************************************************
 * Copyright 2017-2018, Fraunhofer SIT sponsored by Infineon Technologies AG
 * All rights reserved.
 *******************************************************************************/
#ifndef TSS2_ESYS_H
#define TSS2_ESYS_H

#include "tss2_tcti.h"
#include "tss2_sys.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef uint32_t ESYS_TR;

#define ESYS_TR_NONE     0xfffU
#define ESYS_TR_PASSWORD 0x0ffU
#define ESYS_TR_PCR0      0U
#define ESYS_TR_PCR1      1U
#define ESYS_TR_PCR2      2U
#define ESYS_TR_PCR3      3U
#define ESYS_TR_PCR4      4U
#define ESYS_TR_PCR5      5U
#define ESYS_TR_PCR6      6U
#define ESYS_TR_PCR7      7U
#define ESYS_TR_PCR8      8U
#define ESYS_TR_PCR9      9U
#define ESYS_TR_PCR10    10U
#define ESYS_TR_PCR11    11U
#define ESYS_TR_PCR12    12U
#define ESYS_TR_PCR13    13U
#define ESYS_TR_PCR14    14U
#define ESYS_TR_PCR15    15U
#define ESYS_TR_PCR16    16U
#define ESYS_TR_PCR17    17U
#define ESYS_TR_PCR18    18U
#define ESYS_TR_PCR19    19U
#define ESYS_TR_PCR20    20U
#define ESYS_TR_PCR21    21U
#define ESYS_TR_PCR22    22U
#define ESYS_TR_PCR23    23U
#define ESYS_TR_PCR24    24U
#define ESYS_TR_PCR25    25U
#define ESYS_TR_PCR26    26U
#define ESYS_TR_PCR27    27U
#define ESYS_TR_PCR28    28U
#define ESYS_TR_PCR29    29U
#define ESYS_TR_PCR30    30U
#define ESYS_TR_PCR31    31U

/* From TPM_RH_CONSTANTS */
#define ESYS_TR_RH_OWNER       0x101U
#define ESYS_TR_RH_NULL        0x107U
#define ESYS_TR_RH_LOCKOUT     0x10AU
#define ESYS_TR_RH_ENDORSEMENT 0x10BU
#define ESYS_TR_RH_PLATFORM    0x10CU
#define ESYS_TR_RH_PLATFORM_NV 0x10DU

#define ESYS_TR_RH_AUTH_FIRST  0x110U
#define ESYS_TR_RH_AUTH(x) (ESYS_TR_RH_AUTH_FIRST + (ESYS_TR)(x))
#define ESYS_TR_RH_ACT_FIRST  0x120U
#define ESYS_TR_RH_ACT(x) (ESYS_TR_RH_ACT_FIRST + (ESYS_TR)(x))
#define ESYS_TR_RH_ACT_0       ESYS_TR_RH_ACT_FIRST
#define ESYS_TR_RH_ACT_1       0x121U
#define ESYS_TR_RH_ACT_2       0x122U
#define ESYS_TR_RH_ACT_3       0x123U
#define ESYS_TR_RH_ACT_4       0x124U
#define ESYS_TR_RH_ACT_5       0x125U
#define ESYS_TR_RH_ACT_6       0x126U
#define ESYS_TR_RH_ACT_7       0x127U
#define ESYS_TR_RH_ACT_8       0x128U
#define ESYS_TR_RH_ACT_9       0x129U
#define ESYS_TR_RH_ACT_A       0x12AU
#define ESYS_TR_RH_ACT_B       0x12BU
#define ESYS_TR_RH_ACT_C       0x12CU
#define ESYS_TR_RH_ACT_D       0x12DU
#define ESYS_TR_RH_ACT_E       0x12EU
#define ESYS_TR_RH_ACT_F       0x12FU
#define ESYS_TR_RH_ACT_LAST    ESYS_TR_RH_ACT_F
#define ESYS_TR_RH_AC_FIRST    0x140U
#define ESYS_TR_RH_AC(x)       (ESYS_TR_RH_AC_FIRST + (ESYS_TR)(x))
#define ESYS_TR_RH_AC_LAST     (ESYS_TR_RH_AC_FIRST  + 0xFFFFU)

typedef struct ESYS_CONTEXT ESYS_CONTEXT;

typedef struct ESYS_CRYPTO_CONTEXT_BLOB ESYS_CRYPTO_CONTEXT_BLOB;

/*
 * Crypto Backend Support
 */

/** Provide the context for the computation of a hash digest.
 *
 * The context will be created and initialized according to the hash function.
 * @param[out] context The created context (callee-allocated).
 * @param[in] hashAlg The hash algorithm for the creation of the context.
 * @param[in/out] userdata information.
 * @retval TSS2_RC_SUCCESS on success.
 * @retval USER_DEFINED user defined errors on failure.
 */
typedef TSS2_RC
    (*ESYS_CRYPTO_HASH_START_FNP)(
        ESYS_CRYPTO_CONTEXT_BLOB ** context,
        TPM2_ALG_ID hashAlg,
        void *userdata);

/** Update the digest value of a digest object from a byte buffer.
 *
 * The context of a digest object will be updated according to the hash
 * algorithm of the context. <
 * @param[in,out] context The context of the digest object which will be updated.
 * @param[in] buffer The data for the update.
 * @param[in] size The size of the data buffer.
 * @param[in/out] userdata information.
 * @retval TSS2_RC_SUCCESS on success.
 * @retval USER_DEFINED user defined errors on failure.
 */
typedef TSS2_RC
    (*ESYS_CRYPTO_HASH_UPDATE_FNP)(
        ESYS_CRYPTO_CONTEXT_BLOB * context,
        const uint8_t *buffer,
        size_t size,
        void *userdata);

/** Get the digest value of a digest object and close the context.
 *
 * The digest value will written to a passed buffer and the resources of the
 * digest object are released.
 * @param[in,out] context The context of the digest object to be released
 * @param[out] buffer The buffer for the digest value (caller-allocated).
 * @param[out] size The size of the digest.
 * @param[in/out] userdata information.
 * @retval TSS2_RC_SUCCESS on success.
 * @retval USER_DEFINED user defined errors on failure.
 */
typedef TSS2_RC
    (*ESYS_CRYPTO_HASH_FINISH_FNP)(
        ESYS_CRYPTO_CONTEXT_BLOB **context,
        uint8_t *buffer,
        size_t *size,
        void *userdata);

/** Release the resources of a digest object.
 *
 * The assigned resources will be released and the context will be set to NULL.
 * @param[in,out] context The context of the digest object.
 * @param[in/out] userdata information.
 */
typedef void
    (*ESYS_CRYPTO_HASH_ABORT_FNP)(
        ESYS_CRYPTO_CONTEXT_BLOB **context,
        void *userdata);

/** Provide the context an HMAC digest object from a byte buffer key.
 *
 * The context will be created and initialized according to the hash function
 * and the used HMAC key.
 * @param[out] context The created context (callee-allocated).
 * @param[in] hashAlg The hash algorithm for the HMAC computation.
 * @param[in] key The byte buffer of the HMAC key.
 * @param[in] size The size of the HMAC key.
 * @param[in/out] userdata information.
 * @retval TSS2_RC_SUCCESS on success.
 * @retval USER_DEFINED user defined errors on failure.
 */
typedef TSS2_RC
    (*ESYS_CRYPTO_HMAC_START_FNP)(
        ESYS_CRYPTO_CONTEXT_BLOB **context,
        TPM2_ALG_ID hashAlg,
        const uint8_t *key,
        size_t size,
        void *userdata);

/** Update and HMAC digest value from a byte buffer.
 *
 * The context of a digest object will be updated according to the hash
 * algorithm and the key of the context.
 * @param[in,out] context The context of the digest object which will be updated.
 * @param[in] buffer The data for the update.
 * @param[in] size The size of the data buffer.
 * @param[in/out] userdata information.
 * @retval TSS2_RC_SUCCESS on success.
 * @retval USER_DEFINED user defined errors on failure.
 */
typedef TSS2_RC
    (*ESYS_CRYPTO_HMAC_UPDATE_FNP)(
        ESYS_CRYPTO_CONTEXT_BLOB *context,
        const uint8_t *buffer,
        size_t size,
        void *userdata);

/** Write the HMAC digest value to a byte buffer and close the context.
 *
 * The digest value will written to a passed buffer and the resources of the
 * HMAC object are released.
 * @param[in,out] context The context of the HMAC object.
 * @param[out] buffer The buffer for the digest value (caller-allocated).
 * @param[out] size The size of the digest.
 * @param[in/out] userdata information.
 * @retval TSS2_RC_SUCCESS on success.
 * @retval USER_DEFINED user defined errors on failure.
 */
typedef TSS2_RC
    (*ESYS_CRYPTO_HMAC_FINISH_FNP)(
        ESYS_CRYPTO_CONTEXT_BLOB **context,
        uint8_t *buffer,
        size_t *size,
        void *userdata);

/** Release the resources of an HMAC object.
 *
 * The assigned resources will be released and the context will be set to NULL.
 * @param[in,out] context The context of the HMAC object.
 * @param[in/out] userdata information.
 */
typedef void
    (*ESYS_CRYPTO_HMAC_ABORT_FNP)(
        ESYS_CRYPTO_CONTEXT_BLOB **context,
        void *userdata);

/** Compute random TPM2B data.
 *
 * The random data will be generated and written to a passed TPM2B structure.
 * @param[out] nonce The TPM2B structure for the random data (caller-allocated).
 * @param[in] num_bytes The number of bytes to be generated.
 * @param[in/out] userdata information.
 * @retval TSS2_RC_SUCCESS on success.
 * @retval USER_DEFINED user defined errors on failure.
 * @note: the TPM should not be used to obtain the random data
 */
typedef TSS2_RC
    (*ESYS_CRYPTO_GET_RANDOM2B_FNP)(
        TPM2B_NONCE *nonce,
        size_t num_bytes,
        void *userdata);

/** Computation of an ephemeral ECC key and shared secret Z.
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
 * @param[in/out] userdata information.
 * @retval TSS2_RC_SUCCESS on success
 * @retval USER_DEFINED user defined errors on failure.
 */
typedef TSS2_RC
    (*ESYS_CRYPTO_GET_ECDH_POINT_FNP)(
        TPM2B_PUBLIC *key,
        size_t max_out_size,
        TPM2B_ECC_PARAMETER *Z,
        TPMS_ECC_POINT *Q,
        BYTE *out_buffer,
        size_t *out_size,
        void *userdata);

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
 * @param[in/out] userdata information.
 * @retval TSS2_RC_SUCCESS on success
 * @retval USER_DEFINED user defined errors on failure.
 */
typedef TSS2_RC
    (*ESYS_CRYPTO_AES_ENCRYPT_FNP)(
        uint8_t *key,
        TPM2_ALG_ID tpm_sym_alg,
        TPMI_AES_KEY_BITS key_bits,
        TPM2_ALG_ID tpm_mode,
        uint8_t *buffer,
        size_t buffer_size,
        uint8_t *iv,
        void *userdata);

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
 * @param[in/out] userdata information.
 * @retval TSS2_RC_SUCCESS on success
 * @retval USER_DEFINED user defined errors on failure.
 */
typedef TSS2_RC
    (*ESYS_CRYPTO_AES_DECRYPT_FNP)(
        uint8_t *key,
        TPM2_ALG_ID tpm_sym_alg,
        TPMI_AES_KEY_BITS key_bits,
        TPM2_ALG_ID tpm_mode,
        uint8_t *buffer,
        size_t buffer_size,
        uint8_t *iv,
        void *userdata);

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
 * @param[in/out] userdata information.
 * @retval TSS2_RC_SUCCESS on success
 * @retval USER_DEFINED user defined errors on failure.
 */
typedef TSS2_RC
    (*ESYS_CRYPTO_PK_RSA_ENCRYPT_FNP)(
        TPM2B_PUBLIC * pub_tpm_key,
        size_t in_size,
        BYTE *in_buffer,
        size_t max_out_size,
        BYTE *out_buffer,
        size_t *out_size,
        const char *label,
        void *userdata);

/** Initialize crypto backend.
 *
 * Initialize internal tables of crypto backend.
 *
 * @param[in/out] userdata Optional userdata pointer.
 *
 * @retval TSS2_RC_SUCCESS ong success.
 * @retval USER_DEFINED user defined errors on failure.
 */
typedef TSS2_RC (*ESYS_CRYPTO_INIT_FNP)(void *userdata);

typedef struct ESYS_CRYPTO_CALLBACKS ESYS_CRYPTO_CALLBACKS;
struct ESYS_CRYPTO_CALLBACKS {
    ESYS_CRYPTO_PK_RSA_ENCRYPT_FNP rsa_pk_encrypt;
    ESYS_CRYPTO_HASH_START_FNP hash_start;
    ESYS_CRYPTO_HASH_UPDATE_FNP hash_update;
    ESYS_CRYPTO_HASH_FINISH_FNP hash_finish;
    ESYS_CRYPTO_HASH_ABORT_FNP hash_abort;
    ESYS_CRYPTO_HMAC_START_FNP hmac_start;
    ESYS_CRYPTO_HMAC_UPDATE_FNP hmac_update;
    ESYS_CRYPTO_HMAC_FINISH_FNP hmac_finish;
    ESYS_CRYPTO_HMAC_ABORT_FNP hmac_abort;
    ESYS_CRYPTO_GET_RANDOM2B_FNP get_random2b;
    ESYS_CRYPTO_GET_ECDH_POINT_FNP get_ecdh_point;
    ESYS_CRYPTO_AES_ENCRYPT_FNP aes_encrypt;
    ESYS_CRYPTO_AES_DECRYPT_FNP aes_decrypt;
    ESYS_CRYPTO_INIT_FNP init;
    void *userdata;
};

/*
 * TPM 2.0 ESAPI Functions
 */

TSS2_RC
Esys_Initialize(
    ESYS_CONTEXT **esys_context,
    TSS2_TCTI_CONTEXT *tcti,
    TSS2_ABI_VERSION *abiVersion);

void
Esys_Finalize(
    ESYS_CONTEXT **context);

TSS2_RC
Esys_GetTcti(
    ESYS_CONTEXT *esys_context,
    TSS2_TCTI_CONTEXT **tcti);

TSS2_RC
Esys_GetPollHandles(
    ESYS_CONTEXT *esys_context,
    TSS2_TCTI_POLL_HANDLE **handles,
    size_t *count);

TSS2_RC
Esys_SetTimeout(
    ESYS_CONTEXT *esys_context,
    int32_t timeout);

TSS2_RC
Esys_TR_Serialize(
    ESYS_CONTEXT *esys_context,
    ESYS_TR object,
    uint8_t **buffer,
    size_t *buffer_size);

TSS2_RC
Esys_TR_Deserialize(
    ESYS_CONTEXT *esys_context,
    uint8_t const *buffer,
    size_t buffer_size,
    ESYS_TR *esys_handle);

TSS2_RC
Esys_TR_FromTPMPublic_Async(
    ESYS_CONTEXT *esysContext,
    TPM2_HANDLE tpm_handle,
    ESYS_TR optionalSession1,
    ESYS_TR optionalSession2,
    ESYS_TR optionalSession3);

TSS2_RC
Esys_TR_FromTPMPublic_Finish(
    ESYS_CONTEXT *esysContext,
    ESYS_TR *object);

TSS2_RC
Esys_TR_FromTPMPublic(
    ESYS_CONTEXT *esysContext,
    TPM2_HANDLE tpm_handle,
    ESYS_TR optionalSession1,
    ESYS_TR optionalSession2,
    ESYS_TR optionalSession3,
    ESYS_TR *object);

TSS2_RC
Esys_TR_Close(
    ESYS_CONTEXT *esys_context,
    ESYS_TR *rsrc_handle);

TSS2_RC
Esys_TR_SetAuth(
    ESYS_CONTEXT *esysContext,
    ESYS_TR handle,
    TPM2B_AUTH const *authValue);

TSS2_RC
Esys_TR_GetName(
    ESYS_CONTEXT *esysContext,
    ESYS_TR handle,
    TPM2B_NAME **name);

TSS2_RC
Esys_TRSess_GetAttributes(
    ESYS_CONTEXT *esysContext,
    ESYS_TR session,
    TPMA_SESSION *flags);

TSS2_RC
Esys_TRSess_SetAttributes(
    ESYS_CONTEXT *esysContext,
    ESYS_TR session,
    TPMA_SESSION flags,
    TPMA_SESSION mask);

TSS2_RC
Esys_TRSess_GetNonceTPM(
    ESYS_CONTEXT *esysContext,
    ESYS_TR session,
    TPM2B_NONCE **nonceTPM);

TSS2_RC
Esys_TR_GetTpmHandle(
    ESYS_CONTEXT *esys_context,
    ESYS_TR esys_handle,
    TPM2_HANDLE *tpm_handle);

TSS2_RC
Esys_TRSess_GetAuthRequired(
    ESYS_CONTEXT *esys_context,
    ESYS_TR esys_handle,
    TPMI_YES_NO *auth_needed);

/* Table 5 - TPM2_Startup Command */

TSS2_RC
Esys_Startup(
    ESYS_CONTEXT *esysContext,
    TPM2_SU startupType);

TSS2_RC
Esys_Startup_Async(
    ESYS_CONTEXT *esysContext,
    TPM2_SU startupType);

TSS2_RC
Esys_Startup_Finish(
    ESYS_CONTEXT *esysContext);

/* Table 7 - TPM2_Shutdown Command */

TSS2_RC
Esys_Shutdown(
    ESYS_CONTEXT *esysContext,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    TPM2_SU shutdownType);

TSS2_RC
Esys_Shutdown_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    TPM2_SU shutdownType);

TSS2_RC
Esys_Shutdown_Finish(
    ESYS_CONTEXT *esysContext);

/* Table 9 - TPM2_SelfTest Command */

TSS2_RC
Esys_SelfTest(
    ESYS_CONTEXT *esysContext,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    TPMI_YES_NO fullTest);

TSS2_RC
Esys_SelfTest_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    TPMI_YES_NO fullTest);

TSS2_RC
Esys_SelfTest_Finish(
    ESYS_CONTEXT *esysContext);

/* Table 11 - TPM2_IncrementalSelfTest Command */

TSS2_RC
Esys_IncrementalSelfTest(
    ESYS_CONTEXT *esysContext,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPML_ALG *toTest,
    TPML_ALG **toDoList);

TSS2_RC
Esys_IncrementalSelfTest_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPML_ALG *toTest);

TSS2_RC
Esys_IncrementalSelfTest_Finish(
    ESYS_CONTEXT *esysContext,
    TPML_ALG **toDoList);

/* Table 13 - TPM2_GetTestResult Command */

TSS2_RC
Esys_GetTestResult(
    ESYS_CONTEXT *esysContext,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    TPM2B_MAX_BUFFER **outData,
    TPM2_RC *testResult);

TSS2_RC
Esys_GetTestResult_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3);

TSS2_RC
Esys_GetTestResult_Finish(
    ESYS_CONTEXT *esysContext,
    TPM2B_MAX_BUFFER **outData,
    TPM2_RC *testResult);

/* Table 15 - TPM2_StartAuthSession Command */

TSS2_RC
Esys_StartAuthSession(
    ESYS_CONTEXT *esysContext,
    ESYS_TR tpmKey,
    ESYS_TR bind,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_NONCE *nonceCaller,
    TPM2_SE sessionType,
    const TPMT_SYM_DEF *symmetric,
    TPMI_ALG_HASH authHash,
    ESYS_TR *sessionHandle);

TSS2_RC
Esys_StartAuthSession_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR tpmKey,
    ESYS_TR bind,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_NONCE *nonceCaller,
    TPM2_SE sessionType,
    const TPMT_SYM_DEF *symmetric,
    TPMI_ALG_HASH authHash);

TSS2_RC
Esys_StartAuthSession_Finish(
    ESYS_CONTEXT *esysContext,
    ESYS_TR *sessionHandle);

/* Table 17 - TPM2_PolicyRestart Command */

TSS2_RC
Esys_PolicyRestart(
    ESYS_CONTEXT *esysContext,
    ESYS_TR sessionHandle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3);

TSS2_RC
Esys_PolicyRestart_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR sessionHandle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3);

TSS2_RC
Esys_PolicyRestart_Finish(
    ESYS_CONTEXT *esysContext);

/* Table 19 - TPM2_Create Command */

TSS2_RC
Esys_Create(
    ESYS_CONTEXT *esysContext,
    ESYS_TR parentHandle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_SENSITIVE_CREATE *inSensitive,
    const TPM2B_PUBLIC *inPublic,
    const TPM2B_DATA *outsideInfo,
    const TPML_PCR_SELECTION *creationPCR,
    TPM2B_PRIVATE **outPrivate,
    TPM2B_PUBLIC **outPublic,
    TPM2B_CREATION_DATA **creationData,
    TPM2B_DIGEST **creationHash,
    TPMT_TK_CREATION **creationTicket);

TSS2_RC
Esys_Create_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR parentHandle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_SENSITIVE_CREATE *inSensitive,
    const TPM2B_PUBLIC *inPublic,
    const TPM2B_DATA *outsideInfo,
    const TPML_PCR_SELECTION *creationPCR);

TSS2_RC
Esys_Create_Finish(
    ESYS_CONTEXT *esysContext,
    TPM2B_PRIVATE **outPrivate,
    TPM2B_PUBLIC **outPublic,
    TPM2B_CREATION_DATA **creationData,
    TPM2B_DIGEST **creationHash,
    TPMT_TK_CREATION **creationTicket);

/* Table 21 - TPM2_Load Command */

TSS2_RC
Esys_Load(
    ESYS_CONTEXT *esysContext,
    ESYS_TR parentHandle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_PRIVATE *inPrivate,
    const TPM2B_PUBLIC *inPublic,
    ESYS_TR *objectHandle);

TSS2_RC
Esys_Load_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR parentHandle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_PRIVATE *inPrivate,
    const TPM2B_PUBLIC *inPublic);

TSS2_RC
Esys_Load_Finish(
    ESYS_CONTEXT *esysContext,
    ESYS_TR *objectHandle);

/* Table 23 - TPM2_LoadExternal Command */

TSS2_RC
Esys_LoadExternal(
    ESYS_CONTEXT *esysContext,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_SENSITIVE *inPrivate,
    const TPM2B_PUBLIC *inPublic,
    ESYS_TR hierarchy,
    ESYS_TR *objectHandle);

TSS2_RC
Esys_LoadExternal_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_SENSITIVE *inPrivate,
    const TPM2B_PUBLIC *inPublic,
    ESYS_TR hierarchy);

TSS2_RC
Esys_LoadExternal_Finish(
    ESYS_CONTEXT *esysContext,
    ESYS_TR *objectHandle);

/* Table 25 - TPM2_ReadPublic Command */

TSS2_RC
Esys_ReadPublic(
    ESYS_CONTEXT *esysContext,
    ESYS_TR objectHandle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    TPM2B_PUBLIC **outPublic,
    TPM2B_NAME **name,
    TPM2B_NAME **qualifiedName);

TSS2_RC
Esys_ReadPublic_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR objectHandle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3);

TSS2_RC
Esys_ReadPublic_Finish(
    ESYS_CONTEXT *esysContext,
    TPM2B_PUBLIC **outPublic,
    TPM2B_NAME **name,
    TPM2B_NAME **qualifiedName);

/* Table 27 - TPM2_ActivateCredential Command */

TSS2_RC
Esys_ActivateCredential(
    ESYS_CONTEXT *esysContext,
    ESYS_TR activateHandle,
    ESYS_TR keyHandle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_ID_OBJECT *credentialBlob,
    const TPM2B_ENCRYPTED_SECRET *secret,
    TPM2B_DIGEST **certInfo);

TSS2_RC
Esys_ActivateCredential_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR activateHandle,
    ESYS_TR keyHandle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_ID_OBJECT *credentialBlob,
    const TPM2B_ENCRYPTED_SECRET *secret);

TSS2_RC
Esys_ActivateCredential_Finish(
    ESYS_CONTEXT *esysContext,
    TPM2B_DIGEST **certInfo);

TSS2_RC
Esys_ACT_SetTimeout(
    ESYS_CONTEXT *esysContext,
    ESYS_TR actHandle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    UINT32 startTimeout);

TSS2_RC
Esys_ACT_SetTimeout_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR actHandle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    UINT32 startTimeout);

TSS2_RC
Esys_ACT_SetTimeout_Finish(
    ESYS_CONTEXT *esysContext);

TSS2_RC
Esys_AC_GetCapability_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR optionalSession1,
    ESYS_TR optionalSession2,
    ESYS_TR optionalSession3,
    ESYS_TR ac,
    TPM_AT capability,
    UINT32 count);

TSS2_RC
Esys_AC_GetCapability_Finish(
    ESYS_CONTEXT *esysContext,
    TPMI_YES_NO *moreData,
    TPML_AC_CAPABILITIES **capabilityData);

TSS2_RC
Esys_AC_GetCapability(
    ESYS_CONTEXT *esysContext,
    ESYS_TR optionalSession1,
    ESYS_TR optionalSession2,
    ESYS_TR optionalSession3,
    ESYS_TR ac,
    TPM_AT capability,
    UINT32 count,
    TPMI_YES_NO *moreData,
    TPML_AC_CAPABILITIES **capabilityData);

TSS2_RC
Esys_AC_Send_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR sendObject,
    ESYS_TR nvAuthHandle,
    ESYS_TR optionalSession1,
    ESYS_TR optionalSession2,
    ESYS_TR optionalSession3,
    ESYS_TR ac,
    TPM2B_MAX_BUFFER *acDataIn);

TSS2_RC
Esys_AC_Send_Finish(
    ESYS_CONTEXT *esysContext,
    TPMS_AC_OUTPUT **acDataOut);

TSS2_RC
Esys_AC_Send(
    ESYS_CONTEXT *esysContext,
    ESYS_TR sendObject,
    ESYS_TR nvAuthHandle,
    ESYS_TR optionalSession1,
    ESYS_TR optionalSession2,
    ESYS_TR optionalSession3,
    ESYS_TR ac,
    TPM2B_MAX_BUFFER *acDataIn,
    TPMS_AC_OUTPUT **acDataOut);

TSS2_RC
Esys_Policy_AC_SendSelect_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR policySession1,
    ESYS_TR optionalSession2,
    ESYS_TR optionalSession3,
    TPM2B_NAME *objectName,
    TPM2B_NAME *authHandleName,
    TPM2B_NAME *acName,
    const TPMI_YES_NO includeObject);

TSS2_RC
Esys_Policy_AC_SendSelect_Finish(
    ESYS_CONTEXT *esysContext);

TSS2_RC
Esys_Policy_AC_SendSelect(
    ESYS_CONTEXT *esysContext,
    ESYS_TR policySession1,
    ESYS_TR optionalSession2,
    ESYS_TR optionalSession3,
    TPM2B_NAME *objectName,
    TPM2B_NAME *authHandleName,
    TPM2B_NAME *acName,
    TPMI_YES_NO includeObject);

/* Table 29 - TPM2_MakeCredential Command */

TSS2_RC
Esys_MakeCredential(
    ESYS_CONTEXT *esysContext,
    ESYS_TR handle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_DIGEST *credential,
    const TPM2B_NAME *objectName,
    TPM2B_ID_OBJECT **credentialBlob,
    TPM2B_ENCRYPTED_SECRET **secret);

TSS2_RC
Esys_MakeCredential_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR handle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_DIGEST *credential,
    const TPM2B_NAME *objectName);

TSS2_RC
Esys_MakeCredential_Finish(
    ESYS_CONTEXT *esysContext,
    TPM2B_ID_OBJECT **credentialBlob,
    TPM2B_ENCRYPTED_SECRET **secret);

/* Table 31 - TPM2_Unseal Command */

TSS2_RC
Esys_Unseal(
    ESYS_CONTEXT *esysContext,
    ESYS_TR itemHandle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    TPM2B_SENSITIVE_DATA **outData);

TSS2_RC
Esys_Unseal_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR itemHandle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3);

TSS2_RC
Esys_Unseal_Finish(
    ESYS_CONTEXT *esysContext,
    TPM2B_SENSITIVE_DATA **outData);

/* Table 33 - TPM2_ObjectChangeAuth Command */

TSS2_RC
Esys_ObjectChangeAuth(
    ESYS_CONTEXT *esysContext,
    ESYS_TR objectHandle,
    ESYS_TR parentHandle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_AUTH *newAuth,
    TPM2B_PRIVATE **outPrivate);

TSS2_RC
Esys_ObjectChangeAuth_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR objectHandle,
    ESYS_TR parentHandle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_AUTH *newAuth);

TSS2_RC
Esys_ObjectChangeAuth_Finish(
    ESYS_CONTEXT *esysContext,
    TPM2B_PRIVATE **outPrivate);

/* Table 35 - TPM2_CreateLoaded Command */

TSS2_RC
Esys_CreateLoaded(
    ESYS_CONTEXT *esysContext,
    ESYS_TR parentHandle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_SENSITIVE_CREATE *inSensitive,
    const TPM2B_TEMPLATE *inPublic,
    ESYS_TR *objectHandle,
    TPM2B_PRIVATE **outPrivate,
    TPM2B_PUBLIC **outPublic);

TSS2_RC
Esys_CreateLoaded_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR parentHandle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_SENSITIVE_CREATE *inSensitive,
    const TPM2B_TEMPLATE *inPublic);

TSS2_RC
Esys_CreateLoaded_Finish(
    ESYS_CONTEXT *esysContext,
    ESYS_TR *objectHandle,
    TPM2B_PRIVATE **outPrivate,
    TPM2B_PUBLIC **outPublic);

/* Table 37 - TPM2_Duplicate Command */

TSS2_RC
Esys_Duplicate(
    ESYS_CONTEXT *esysContext,
    ESYS_TR objectHandle,
    ESYS_TR newParentHandle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_DATA *encryptionKeyIn,
    const TPMT_SYM_DEF_OBJECT *symmetricAlg,
    TPM2B_DATA **encryptionKeyOut,
    TPM2B_PRIVATE **duplicate,
    TPM2B_ENCRYPTED_SECRET **outSymSeed);

TSS2_RC
Esys_Duplicate_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR objectHandle,
    ESYS_TR newParentHandle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_DATA *encryptionKeyIn,
    const TPMT_SYM_DEF_OBJECT *symmetricAlg);

TSS2_RC
Esys_Duplicate_Finish(
    ESYS_CONTEXT *esysContext,
    TPM2B_DATA **encryptionKeyOut,
    TPM2B_PRIVATE **duplicate,
    TPM2B_ENCRYPTED_SECRET **outSymSeed);

/* Table 39 - TPM2_Rewrap Command */

TSS2_RC
Esys_Rewrap(
    ESYS_CONTEXT *esysContext,
    ESYS_TR oldParent,
    ESYS_TR newParent,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_PRIVATE *inDuplicate,
    const TPM2B_NAME *name,
    const TPM2B_ENCRYPTED_SECRET *inSymSeed,
    TPM2B_PRIVATE **outDuplicate,
    TPM2B_ENCRYPTED_SECRET **outSymSeed);

TSS2_RC
Esys_Rewrap_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR oldParent,
    ESYS_TR newParent,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_PRIVATE *inDuplicate,
    const TPM2B_NAME *name,
    const TPM2B_ENCRYPTED_SECRET *inSymSeed);

TSS2_RC
Esys_Rewrap_Finish(
    ESYS_CONTEXT *esysContext,
    TPM2B_PRIVATE **outDuplicate,
    TPM2B_ENCRYPTED_SECRET **outSymSeed);

/* Table 41 - TPM2_Import Command */

TSS2_RC
Esys_Import(
    ESYS_CONTEXT *esysContext,
    ESYS_TR parentHandle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_DATA *encryptionKey,
    const TPM2B_PUBLIC *objectPublic,
    const TPM2B_PRIVATE *duplicate,
    const TPM2B_ENCRYPTED_SECRET *inSymSeed,
    const TPMT_SYM_DEF_OBJECT *symmetricAlg,
    TPM2B_PRIVATE **outPrivate);

TSS2_RC
Esys_Import_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR parentHandle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_DATA *encryptionKey,
    const TPM2B_PUBLIC *objectPublic,
    const TPM2B_PRIVATE *duplicate,
    const TPM2B_ENCRYPTED_SECRET *inSymSeed,
    const TPMT_SYM_DEF_OBJECT *symmetricAlg);

TSS2_RC
Esys_Import_Finish(
    ESYS_CONTEXT *esysContext,
    TPM2B_PRIVATE **outPrivate);

/* Table 45 - TPM2_RSA_Encrypt Command */

TSS2_RC
Esys_RSA_Encrypt(
    ESYS_CONTEXT *esysContext,
    ESYS_TR keyHandle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_PUBLIC_KEY_RSA *message,
    const TPMT_RSA_DECRYPT *inScheme,
    const TPM2B_DATA *label,
    TPM2B_PUBLIC_KEY_RSA **outData);

TSS2_RC
Esys_RSA_Encrypt_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR keyHandle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_PUBLIC_KEY_RSA *message,
    const TPMT_RSA_DECRYPT *inScheme,
    const TPM2B_DATA *label);

TSS2_RC
Esys_RSA_Encrypt_Finish(
    ESYS_CONTEXT *esysContext,
    TPM2B_PUBLIC_KEY_RSA **outData);

/* Table 47 - TPM2_RSA_Decrypt Command */

TSS2_RC
Esys_RSA_Decrypt(
    ESYS_CONTEXT *esysContext,
    ESYS_TR keyHandle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_PUBLIC_KEY_RSA *cipherText,
    const TPMT_RSA_DECRYPT *inScheme,
    const TPM2B_DATA *label,
    TPM2B_PUBLIC_KEY_RSA **message);

TSS2_RC
Esys_RSA_Decrypt_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR keyHandle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_PUBLIC_KEY_RSA *cipherText,
    const TPMT_RSA_DECRYPT *inScheme,
    const TPM2B_DATA *label);

TSS2_RC
Esys_RSA_Decrypt_Finish(
    ESYS_CONTEXT *esysContext,
    TPM2B_PUBLIC_KEY_RSA **message);

/* Table 49 - TPM2_ECDH_KeyGen Command */

TSS2_RC
Esys_ECDH_KeyGen(
    ESYS_CONTEXT *esysContext,
    ESYS_TR keyHandle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    TPM2B_ECC_POINT **zPoint,
    TPM2B_ECC_POINT **pubPoint);

TSS2_RC
Esys_ECDH_KeyGen_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR keyHandle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3);

TSS2_RC
Esys_ECDH_KeyGen_Finish(
    ESYS_CONTEXT *esysContext,
    TPM2B_ECC_POINT **zPoint,
    TPM2B_ECC_POINT **pubPoint);

/* Table 51 - TPM2_ECDH_ZGen Command */

TSS2_RC
Esys_ECDH_ZGen(
    ESYS_CONTEXT *esysContext,
    ESYS_TR keyHandle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_ECC_POINT *inPoint,
    TPM2B_ECC_POINT **outPoint);

TSS2_RC
Esys_ECDH_ZGen_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR keyHandle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_ECC_POINT *inPoint);

TSS2_RC
Esys_ECDH_ZGen_Finish(
    ESYS_CONTEXT *esysContext,
    TPM2B_ECC_POINT **outPoint);

/* Table 53 - TPM2_ECC_Parameters Command */

TSS2_RC
Esys_ECC_Parameters(
    ESYS_CONTEXT *esysContext,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    TPMI_ECC_CURVE curveID,
    TPMS_ALGORITHM_DETAIL_ECC **parameters);

TSS2_RC
Esys_ECC_Parameters_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    TPMI_ECC_CURVE curveID);

TSS2_RC
Esys_ECC_Parameters_Finish(
    ESYS_CONTEXT *esysContext,
    TPMS_ALGORITHM_DETAIL_ECC **parameters);

/* Table 55 - TPM2_ZGen_2Phase Command */

TSS2_RC
Esys_ZGen_2Phase(
    ESYS_CONTEXT *esysContext,
    ESYS_TR keyA,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_ECC_POINT *inQsB,
    const TPM2B_ECC_POINT *inQeB,
    TPMI_ECC_KEY_EXCHANGE inScheme,
    UINT16 counter,
    TPM2B_ECC_POINT **outZ1,
    TPM2B_ECC_POINT **outZ2);

TSS2_RC
Esys_ZGen_2Phase_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR keyA,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_ECC_POINT *inQsB,
    const TPM2B_ECC_POINT *inQeB,
    TPMI_ECC_KEY_EXCHANGE inScheme,
    UINT16 counter);

TSS2_RC
Esys_ZGen_2Phase_Finish(
    ESYS_CONTEXT *esysContext,
    TPM2B_ECC_POINT **outZ1,
    TPM2B_ECC_POINT **outZ2);

/* Table 58 - TPM2_EncryptDecrypt Command */

TSS2_RC
Esys_EncryptDecrypt(
    ESYS_CONTEXT *esysContext,
    ESYS_TR keyHandle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    TPMI_YES_NO decrypt,
    TPMI_ALG_CIPHER_MODE mode,
    const TPM2B_IV *ivIn,
    const TPM2B_MAX_BUFFER *inData,
    TPM2B_MAX_BUFFER **outData,
    TPM2B_IV **ivOut);

TSS2_RC
Esys_EncryptDecrypt_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR keyHandle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    TPMI_YES_NO decrypt,
    TPMI_ALG_CIPHER_MODE mode,
    const TPM2B_IV *ivIn,
    const TPM2B_MAX_BUFFER *inData);

TSS2_RC
Esys_EncryptDecrypt_Finish(
    ESYS_CONTEXT *esysContext,
    TPM2B_MAX_BUFFER **outData,
    TPM2B_IV **ivOut);

/* Table 60 - TPM2_EncryptDecrypt2 Command */

TSS2_RC
Esys_EncryptDecrypt2(
    ESYS_CONTEXT *esysContext,
    ESYS_TR keyHandle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_MAX_BUFFER *inData,
    TPMI_YES_NO decrypt,
    TPMI_ALG_CIPHER_MODE mode,
    const TPM2B_IV *ivIn,
    TPM2B_MAX_BUFFER **outData,
    TPM2B_IV **ivOut);

TSS2_RC
Esys_EncryptDecrypt2_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR keyHandle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_MAX_BUFFER *inData,
    TPMI_YES_NO decrypt,
    TPMI_ALG_CIPHER_MODE mode,
    const TPM2B_IV *ivIn);

TSS2_RC
Esys_EncryptDecrypt2_Finish(
    ESYS_CONTEXT *esysContext,
    TPM2B_MAX_BUFFER **outData,
    TPM2B_IV **ivOut);

/* Table 62 - TPM2_Hash Command */

TSS2_RC
Esys_Hash(
    ESYS_CONTEXT *esysContext,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_MAX_BUFFER *data,
    TPMI_ALG_HASH hashAlg,
    ESYS_TR hierarchy,
    TPM2B_DIGEST **outHash,
    TPMT_TK_HASHCHECK **validation);

TSS2_RC
Esys_Hash_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_MAX_BUFFER *data,
    TPMI_ALG_HASH hashAlg,
    ESYS_TR hierarchy);

TSS2_RC
Esys_Hash_Finish(
    ESYS_CONTEXT *esysContext,
    TPM2B_DIGEST **outHash,
    TPMT_TK_HASHCHECK **validation);

/* Table 64 - TPM2_HMAC Command */

TSS2_RC
Esys_HMAC(
    ESYS_CONTEXT *esysContext,
    ESYS_TR handle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_MAX_BUFFER *buffer,
    TPMI_ALG_HASH hashAlg,
    TPM2B_DIGEST **outHMAC);

TSS2_RC
Esys_HMAC_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR handle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_MAX_BUFFER *buffer,
    TPMI_ALG_HASH hashAlg);

TSS2_RC
Esys_HMAC_Finish(
    ESYS_CONTEXT *esysContext,
    TPM2B_DIGEST **outHMAC);

TSS2_RC
Esys_MAC_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR handle,
    ESYS_TR handleSession1,
    ESYS_TR optionalSession2,
    ESYS_TR optionalSession3,
    const TPM2B_MAX_BUFFER *buffer,
    TPMI_ALG_MAC_SCHEME inScheme);

TSS2_RC
Esys_MAC_Finish(
    ESYS_CONTEXT *esysContext,
    TPM2B_DIGEST **outMAC);

TSS2_RC
Esys_MAC(
    ESYS_CONTEXT *esysContext,
    ESYS_TR handle,
    ESYS_TR handleSession1,
    ESYS_TR optionalSession2,
    ESYS_TR optionalSession3,
    const TPM2B_MAX_BUFFER *buffer,
    TPMI_ALG_MAC_SCHEME inScheme,
    TPM2B_DIGEST **outMAC);

/* Table 66 - TPM2_GetRandom Command */

TSS2_RC
Esys_GetRandom(
    ESYS_CONTEXT *esysContext,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    UINT16 bytesRequested,
    TPM2B_DIGEST **randomBytes);

TSS2_RC
Esys_GetRandom_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    UINT16 bytesRequested);

TSS2_RC
Esys_GetRandom_Finish(
    ESYS_CONTEXT *esysContext,
    TPM2B_DIGEST **randomBytes);

/* Table 68 - TPM2_StirRandom Command */

TSS2_RC
Esys_StirRandom(
    ESYS_CONTEXT *esysContext,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_SENSITIVE_DATA *inData);

TSS2_RC
Esys_StirRandom_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_SENSITIVE_DATA *inData);

TSS2_RC
Esys_StirRandom_Finish(
    ESYS_CONTEXT *esysContext);

/* Table 71 - TPM2_HMAC_Start Command */

TSS2_RC
Esys_HMAC_Start(
    ESYS_CONTEXT *esysContext,
    ESYS_TR handle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_AUTH *auth,
    TPMI_ALG_HASH hashAlg,
    ESYS_TR *sequenceHandle);

TSS2_RC
Esys_HMAC_Start_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR handle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_AUTH *auth,
    TPMI_ALG_HASH hashAlg);

TSS2_RC
Esys_HMAC_Start_Finish(
    ESYS_CONTEXT *esysContext,
    ESYS_TR *sequenceHandle);

TSS2_RC
Esys_MAC_Start(
    ESYS_CONTEXT *esysContext,
    ESYS_TR handle,
    ESYS_TR handleSession1,
    ESYS_TR optionalSession2,
    ESYS_TR optionalSession3,
    const TPM2B_AUTH *auth,
    TPMI_ALG_MAC_SCHEME inScheme,
    ESYS_TR *sequenceHandle);

TSS2_RC
Esys_MAC_Start_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR handle,
    ESYS_TR handleSession1,
    ESYS_TR optionalSession2,
    ESYS_TR optionalSession3,
    const TPM2B_AUTH *auth,
    TPMI_ALG_MAC_SCHEME inScheme);

TSS2_RC
Esys_MAC_Start_Finish(
    ESYS_CONTEXT *esysContext,
    ESYS_TR *sequenceHandle);

/* Table 73 - TPM2_HashSequenceStart Command */

TSS2_RC
Esys_HashSequenceStart(
    ESYS_CONTEXT *esysContext,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_AUTH *auth,
    TPMI_ALG_HASH hashAlg,
    ESYS_TR *sequenceHandle);

TSS2_RC
Esys_HashSequenceStart_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_AUTH *auth,
    TPMI_ALG_HASH hashAlg);

TSS2_RC
Esys_HashSequenceStart_Finish(
    ESYS_CONTEXT *esysContext,
    ESYS_TR *sequenceHandle);

/* Table 75 - TPM2_SequenceUpdate Command */

TSS2_RC
Esys_SequenceUpdate(
    ESYS_CONTEXT *esysContext,
    ESYS_TR sequenceHandle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_MAX_BUFFER *buffer);

TSS2_RC
Esys_SequenceUpdate_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR sequenceHandle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_MAX_BUFFER *buffer);

TSS2_RC
Esys_SequenceUpdate_Finish(
    ESYS_CONTEXT *esysContext);

/* Table 77 - TPM2_SequenceComplete Command */

TSS2_RC
Esys_SequenceComplete(
    ESYS_CONTEXT *esysContext,
    ESYS_TR sequenceHandle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_MAX_BUFFER *buffer,
    ESYS_TR hierarchy,
    TPM2B_DIGEST **result,
    TPMT_TK_HASHCHECK **validation);

TSS2_RC
Esys_SequenceComplete_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR sequenceHandle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_MAX_BUFFER *buffer,
    ESYS_TR hierarchy);

TSS2_RC
Esys_SequenceComplete_Finish(
    ESYS_CONTEXT *esysContext,
    TPM2B_DIGEST **result,
    TPMT_TK_HASHCHECK **validation);

/* Table 79 - TPM2_EventSequenceComplete Command */

TSS2_RC
Esys_EventSequenceComplete(
    ESYS_CONTEXT *esysContext,
    ESYS_TR pcrHandle,
    ESYS_TR sequenceHandle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_MAX_BUFFER *buffer,
    TPML_DIGEST_VALUES **results);

TSS2_RC
Esys_EventSequenceComplete_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR pcrHandle,
    ESYS_TR sequenceHandle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_MAX_BUFFER *buffer);

TSS2_RC
Esys_EventSequenceComplete_Finish(
    ESYS_CONTEXT *esysContext,
    TPML_DIGEST_VALUES **results);

/* Table 81 - TPM2_Certify Command */

TSS2_RC
Esys_Certify(
    ESYS_CONTEXT *esysContext,
    ESYS_TR objectHandle,
    ESYS_TR signHandle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_DATA *qualifyingData,
    const TPMT_SIG_SCHEME *inScheme,
    TPM2B_ATTEST **certifyInfo,
    TPMT_SIGNATURE **signature);

TSS2_RC
Esys_Certify_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR objectHandle,
    ESYS_TR signHandle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_DATA *qualifyingData,
    const TPMT_SIG_SCHEME *inScheme);

TSS2_RC
Esys_Certify_Finish(
    ESYS_CONTEXT *esysContext,
    TPM2B_ATTEST **certifyInfo,
    TPMT_SIGNATURE **signature);

/* Table 83 - TPM2_CertifyCreation Command */

TSS2_RC
Esys_CertifyCreation(
    ESYS_CONTEXT *esysContext,
    ESYS_TR signHandle,
    ESYS_TR objectHandle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_DATA *qualifyingData,
    const TPM2B_DIGEST *creationHash,
    const TPMT_SIG_SCHEME *inScheme,
    const TPMT_TK_CREATION *creationTicket,
    TPM2B_ATTEST **certifyInfo,
    TPMT_SIGNATURE **signature);

TSS2_RC
Esys_CertifyCreation_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR signHandle,
    ESYS_TR objectHandle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_DATA *qualifyingData,
    const TPM2B_DIGEST *creationHash,
    const TPMT_SIG_SCHEME *inScheme,
    const TPMT_TK_CREATION *creationTicket);

TSS2_RC
Esys_CertifyCreation_Finish(
    ESYS_CONTEXT *esysContext,
    TPM2B_ATTEST **certifyInfo,
    TPMT_SIGNATURE **signature);

TSS2_RC
Esys_CertifyX509(
    ESYS_CONTEXT *esysContext,
    ESYS_TR objectHandle,
    ESYS_TR signHandle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_DATA *reserved,
    const TPMT_SIG_SCHEME *inScheme,
    const TPM2B_MAX_BUFFER *partialCertificate,
    TPM2B_MAX_BUFFER **addedToCertificate,
    TPM2B_DIGEST **tbsDigest,
    TPMT_SIGNATURE **signature);

TSS2_RC
Esys_CertifyX509_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR objectHandle,
    ESYS_TR signHandle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_DATA *reserved,
    const TPMT_SIG_SCHEME *inScheme,
    const TPM2B_MAX_BUFFER *partialCertificate);

TSS2_RC
Esys_CertifyX509_Finish(
    ESYS_CONTEXT *esysContext,
    TPM2B_MAX_BUFFER **addedToCertificate,
    TPM2B_DIGEST **tbsDigest,
    TPMT_SIGNATURE **signature);

/* Table 85 - TPM2_Quote Command */

TSS2_RC
Esys_Quote(
    ESYS_CONTEXT *esysContext,
    ESYS_TR signHandle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_DATA *qualifyingData,
    const TPMT_SIG_SCHEME *inScheme,
    const TPML_PCR_SELECTION *PCRselect,
    TPM2B_ATTEST **quoted,
    TPMT_SIGNATURE **signature);

TSS2_RC
Esys_Quote_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR signHandle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_DATA *qualifyingData,
    const TPMT_SIG_SCHEME *inScheme,
    const TPML_PCR_SELECTION *PCRselect);

TSS2_RC
Esys_Quote_Finish(
    ESYS_CONTEXT *esysContext,
    TPM2B_ATTEST **quoted,
    TPMT_SIGNATURE **signature);

/* Table 87 - TPM2_GetSessionAuditDigest Command */

TSS2_RC
Esys_GetSessionAuditDigest(
    ESYS_CONTEXT *esysContext,
    ESYS_TR privacyAdminHandle,
    ESYS_TR signHandle,
    ESYS_TR sessionHandle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_DATA *qualifyingData,
    const TPMT_SIG_SCHEME *inScheme,
    TPM2B_ATTEST **auditInfo,
    TPMT_SIGNATURE **signature);

TSS2_RC
Esys_GetSessionAuditDigest_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR privacyAdminHandle,
    ESYS_TR signHandle,
    ESYS_TR sessionHandle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_DATA *qualifyingData,
    const TPMT_SIG_SCHEME *inScheme);

TSS2_RC
Esys_GetSessionAuditDigest_Finish(
    ESYS_CONTEXT *esysContext,
    TPM2B_ATTEST **auditInfo,
    TPMT_SIGNATURE **signature);

/* Table 89 - TPM2_GetCommandAuditDigest Command */

TSS2_RC
Esys_GetCommandAuditDigest(
    ESYS_CONTEXT *esysContext,
    ESYS_TR privacyHandle,
    ESYS_TR signHandle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_DATA *qualifyingData,
    const TPMT_SIG_SCHEME *inScheme,
    TPM2B_ATTEST **auditInfo,
    TPMT_SIGNATURE **signature);

TSS2_RC
Esys_GetCommandAuditDigest_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR privacyHandle,
    ESYS_TR signHandle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_DATA *qualifyingData,
    const TPMT_SIG_SCHEME *inScheme);

TSS2_RC
Esys_GetCommandAuditDigest_Finish(
    ESYS_CONTEXT *esysContext,
    TPM2B_ATTEST **auditInfo,
    TPMT_SIGNATURE **signature);

/* Table 91 - TPM2_GetTime Command */

TSS2_RC
Esys_GetTime(
    ESYS_CONTEXT *esysContext,
    ESYS_TR privacyAdminHandle,
    ESYS_TR signHandle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_DATA *qualifyingData,
    const TPMT_SIG_SCHEME *inScheme,
    TPM2B_ATTEST **timeInfo,
    TPMT_SIGNATURE **signature);

TSS2_RC
Esys_GetTime_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR privacyAdminHandle,
    ESYS_TR signHandle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_DATA *qualifyingData,
    const TPMT_SIG_SCHEME *inScheme);

TSS2_RC
Esys_GetTime_Finish(
    ESYS_CONTEXT *esysContext,
    TPM2B_ATTEST **timeInfo,
    TPMT_SIGNATURE **signature);

/* Table 93 - TPM2_Commit Command */

TSS2_RC
Esys_Commit(
    ESYS_CONTEXT *esysContext,
    ESYS_TR signHandle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_ECC_POINT *P1,
    const TPM2B_SENSITIVE_DATA *s2,
    const TPM2B_ECC_PARAMETER *y2,
    TPM2B_ECC_POINT **K,
    TPM2B_ECC_POINT **L,
    TPM2B_ECC_POINT **E,
    UINT16 *counter);

TSS2_RC
Esys_Commit_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR signHandle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_ECC_POINT *P1,
    const TPM2B_SENSITIVE_DATA *s2,
    const TPM2B_ECC_PARAMETER *y2);

TSS2_RC
Esys_Commit_Finish(
    ESYS_CONTEXT *esysContext,
    TPM2B_ECC_POINT **K,
    TPM2B_ECC_POINT **L,
    TPM2B_ECC_POINT **E,
    UINT16 *counter);

/* Table 95 - TPM2_EC_Ephemeral Command */

TSS2_RC
Esys_EC_Ephemeral(
    ESYS_CONTEXT *esysContext,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    TPMI_ECC_CURVE curveID,
    TPM2B_ECC_POINT **Q,
    UINT16 *counter);

TSS2_RC
Esys_EC_Ephemeral_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    TPMI_ECC_CURVE curveID);

TSS2_RC
Esys_EC_Ephemeral_Finish(
    ESYS_CONTEXT *esysContext,
    TPM2B_ECC_POINT **Q,
    UINT16 *counter);

/* Table 97 - TPM2_VerifySignature Command */

TSS2_RC
Esys_VerifySignature(
    ESYS_CONTEXT *esysContext,
    ESYS_TR keyHandle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_DIGEST *digest,
    const TPMT_SIGNATURE *signature,
    TPMT_TK_VERIFIED **validation);

TSS2_RC
Esys_VerifySignature_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR keyHandle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_DIGEST *digest,
    const TPMT_SIGNATURE *signature);

TSS2_RC
Esys_VerifySignature_Finish(
    ESYS_CONTEXT *esysContext,
    TPMT_TK_VERIFIED **validation);

/* Table 99 - TPM2_Sign Command */

TSS2_RC
Esys_Sign(
    ESYS_CONTEXT *esysContext,
    ESYS_TR keyHandle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_DIGEST *digest,
    const TPMT_SIG_SCHEME *inScheme,
    const TPMT_TK_HASHCHECK *validation,
    TPMT_SIGNATURE **signature);

TSS2_RC
Esys_Sign_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR keyHandle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_DIGEST *digest,
    const TPMT_SIG_SCHEME *inScheme,
    const TPMT_TK_HASHCHECK *validation);

TSS2_RC
Esys_Sign_Finish(
    ESYS_CONTEXT *esysContext,
    TPMT_SIGNATURE **signature);

/* Table 101 - TPM2_SetCommandCodeAuditStatus Command */

TSS2_RC
Esys_SetCommandCodeAuditStatus(
    ESYS_CONTEXT *esysContext,
    ESYS_TR auth,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    TPMI_ALG_HASH auditAlg,
    const TPML_CC *setList,
    const TPML_CC *clearList);

TSS2_RC
Esys_SetCommandCodeAuditStatus_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR auth,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    TPMI_ALG_HASH auditAlg,
    const TPML_CC *setList,
    const TPML_CC *clearList);

TSS2_RC
Esys_SetCommandCodeAuditStatus_Finish(
    ESYS_CONTEXT *esysContext);

/* Table 103 - TPM2_PCR_Extend Command */

TSS2_RC
Esys_PCR_Extend(
    ESYS_CONTEXT *esysContext,
    ESYS_TR pcrHandle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPML_DIGEST_VALUES *digests);

TSS2_RC
Esys_PCR_Extend_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR pcrHandle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPML_DIGEST_VALUES *digests);

TSS2_RC
Esys_PCR_Extend_Finish(
    ESYS_CONTEXT *esysContext);

/* Table 105 - TPM2_PCR_Event Command */

TSS2_RC
Esys_PCR_Event(
    ESYS_CONTEXT *esysContext,
    ESYS_TR pcrHandle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_EVENT *eventData,
    TPML_DIGEST_VALUES **digests);

TSS2_RC
Esys_PCR_Event_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR pcrHandle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_EVENT *eventData);

TSS2_RC
Esys_PCR_Event_Finish(
    ESYS_CONTEXT *esysContext,
    TPML_DIGEST_VALUES **digests);

/* Table 107 - TPM2_PCR_Read Command */

TSS2_RC
Esys_PCR_Read(
    ESYS_CONTEXT *esysContext,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPML_PCR_SELECTION *pcrSelectionIn,
    UINT32 *pcrUpdateCounter,
    TPML_PCR_SELECTION **pcrSelectionOut,
    TPML_DIGEST **pcrValues);

TSS2_RC
Esys_PCR_Read_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPML_PCR_SELECTION *pcrSelectionIn);

TSS2_RC
Esys_PCR_Read_Finish(
    ESYS_CONTEXT *esysContext,
    UINT32 *pcrUpdateCounter,
    TPML_PCR_SELECTION **pcrSelectionOut,
    TPML_DIGEST **pcrValues);

/* Table 109 - TPM2_PCR_Allocate Command */

TSS2_RC
Esys_PCR_Allocate(
    ESYS_CONTEXT *esysContext,
    ESYS_TR authHandle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPML_PCR_SELECTION *pcrAllocation,
    TPMI_YES_NO *allocationSuccess,
    UINT32 *maxPCR,
    UINT32 *sizeNeeded,
    UINT32 *sizeAvailable);

TSS2_RC
Esys_PCR_Allocate_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR authHandle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPML_PCR_SELECTION *pcrAllocation);

TSS2_RC
Esys_PCR_Allocate_Finish(
    ESYS_CONTEXT *esysContext,
    TPMI_YES_NO *allocationSuccess,
    UINT32 *maxPCR,
    UINT32 *sizeNeeded,
    UINT32 *sizeAvailable);

/* Table 111 - TPM2_PCR_SetAuthPolicy Command */

TSS2_RC
Esys_PCR_SetAuthPolicy(
    ESYS_CONTEXT *esysContext,
    ESYS_TR authHandle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_DIGEST *authPolicy,
    TPMI_ALG_HASH hashAlg,
    TPMI_DH_PCR pcrNum);

TSS2_RC
Esys_PCR_SetAuthPolicy_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR authHandle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_DIGEST *authPolicy,
    TPMI_ALG_HASH hashAlg,
    TPMI_DH_PCR pcrNum);

TSS2_RC
Esys_PCR_SetAuthPolicy_Finish(
    ESYS_CONTEXT *esysContext);

/* Table 113 - TPM2_PCR_SetAuthValue Command */

TSS2_RC
Esys_PCR_SetAuthValue(
    ESYS_CONTEXT *esysContext,
    ESYS_TR pcrHandle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_DIGEST *auth);

TSS2_RC
Esys_PCR_SetAuthValue_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR pcrHandle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_DIGEST *auth);

TSS2_RC
Esys_PCR_SetAuthValue_Finish(
    ESYS_CONTEXT *esysContext);

/* Table 115 - TPM2_PCR_Reset Command */

TSS2_RC
Esys_PCR_Reset(
    ESYS_CONTEXT *esysContext,
    ESYS_TR pcrHandle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3);

TSS2_RC
Esys_PCR_Reset_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR pcrHandle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3);

TSS2_RC
Esys_PCR_Reset_Finish(
    ESYS_CONTEXT *esysContext);

/* Table 117 - TPM2_PolicySigned Command */

TSS2_RC
Esys_PolicySigned(
    ESYS_CONTEXT *esysContext,
    ESYS_TR authObject,
    ESYS_TR policySession,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_NONCE *nonceTPM,
    const TPM2B_DIGEST *cpHashA,
    const TPM2B_NONCE *policyRef,
    INT32 expiration,
    const TPMT_SIGNATURE *auth,
    TPM2B_TIMEOUT **timeout,
    TPMT_TK_AUTH **policyTicket);

TSS2_RC
Esys_PolicySigned_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR authObject,
    ESYS_TR policySession,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_NONCE *nonceTPM,
    const TPM2B_DIGEST *cpHashA,
    const TPM2B_NONCE *policyRef,
    INT32 expiration,
    const TPMT_SIGNATURE *auth);

TSS2_RC
Esys_PolicySigned_Finish(
    ESYS_CONTEXT *esysContext,
    TPM2B_TIMEOUT **timeout,
    TPMT_TK_AUTH **policyTicket);

/* Table 119 - TPM2_PolicySecret Command */

TSS2_RC
Esys_PolicySecret(
    ESYS_CONTEXT *esysContext,
    ESYS_TR authHandle,
    ESYS_TR policySession,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_NONCE *nonceTPM,
    const TPM2B_DIGEST *cpHashA,
    const TPM2B_NONCE *policyRef,
    INT32 expiration,
    TPM2B_TIMEOUT **timeout,
    TPMT_TK_AUTH **policyTicket);

TSS2_RC
Esys_PolicySecret_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR authHandle,
    ESYS_TR policySession,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_NONCE *nonceTPM,
    const TPM2B_DIGEST *cpHashA,
    const TPM2B_NONCE *policyRef,
    INT32 expiration);

TSS2_RC
Esys_PolicySecret_Finish(
    ESYS_CONTEXT *esysContext,
    TPM2B_TIMEOUT **timeout,
    TPMT_TK_AUTH **policyTicket);

/* Table 121 - TPM2_PolicyTicket Command */

TSS2_RC
Esys_PolicyTicket(
    ESYS_CONTEXT *esysContext,
    ESYS_TR policySession,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_TIMEOUT *timeout,
    const TPM2B_DIGEST *cpHashA,
    const TPM2B_NONCE *policyRef,
    const TPM2B_NAME *authName,
    const TPMT_TK_AUTH *ticket);

TSS2_RC
Esys_PolicyTicket_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR policySession,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_TIMEOUT *timeout,
    const TPM2B_DIGEST *cpHashA,
    const TPM2B_NONCE *policyRef,
    const TPM2B_NAME *authName,
    const TPMT_TK_AUTH *ticket);

TSS2_RC
Esys_PolicyTicket_Finish(
    ESYS_CONTEXT *esysContext);

/* Table 123 - TPM2_PolicyOR Command */

TSS2_RC
Esys_PolicyOR(
    ESYS_CONTEXT *esysContext,
    ESYS_TR policySession,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPML_DIGEST *pHashList);

TSS2_RC
Esys_PolicyOR_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR policySession,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPML_DIGEST *pHashList);

TSS2_RC
Esys_PolicyOR_Finish(
    ESYS_CONTEXT *esysContext);

/* Table 125 - TPM2_PolicyPCR Command */

TSS2_RC
Esys_PolicyPCR(
    ESYS_CONTEXT *esysContext,
    ESYS_TR policySession,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_DIGEST *pcrDigest,
    const TPML_PCR_SELECTION *pcrs);

TSS2_RC
Esys_PolicyPCR_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR policySession,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_DIGEST *pcrDigest,
    const TPML_PCR_SELECTION *pcrs);

TSS2_RC
Esys_PolicyPCR_Finish(
    ESYS_CONTEXT *esysContext);

/* Table 127 - TPM2_PolicyLocality Command */

TSS2_RC
Esys_PolicyLocality(
    ESYS_CONTEXT *esysContext,
    ESYS_TR policySession,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    TPMA_LOCALITY locality);

TSS2_RC
Esys_PolicyLocality_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR policySession,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    TPMA_LOCALITY locality);

TSS2_RC
Esys_PolicyLocality_Finish(
    ESYS_CONTEXT *esysContext);

/* Table 129 - TPM2_PolicyNV Command */

TSS2_RC
Esys_PolicyNV(
    ESYS_CONTEXT *esysContext,
    ESYS_TR authHandle,
    ESYS_TR nvIndex,
    ESYS_TR policySession,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_OPERAND *operandB,
    UINT16 offset,
    TPM2_EO operation);

TSS2_RC
Esys_PolicyNV_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR authHandle,
    ESYS_TR nvIndex,
    ESYS_TR policySession,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_OPERAND *operandB,
    UINT16 offset,
    TPM2_EO operation);

TSS2_RC
Esys_PolicyNV_Finish(
    ESYS_CONTEXT *esysContext);

/* Table 131 - TPM2_PolicyCounterTimer Command */

TSS2_RC
Esys_PolicyCounterTimer(
    ESYS_CONTEXT *esysContext,
    ESYS_TR policySession,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_OPERAND *operandB,
    UINT16 offset,
    TPM2_EO operation);

TSS2_RC
Esys_PolicyCounterTimer_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR policySession,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_OPERAND *operandB,
    UINT16 offset,
    TPM2_EO operation);

TSS2_RC
Esys_PolicyCounterTimer_Finish(
    ESYS_CONTEXT *esysContext);

/* Table 133 - TPM2_PolicyCommandCode Command */

TSS2_RC
Esys_PolicyCommandCode(
    ESYS_CONTEXT *esysContext,
    ESYS_TR policySession,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    TPM2_CC code);

TSS2_RC
Esys_PolicyCommandCode_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR policySession,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    TPM2_CC code);

TSS2_RC
Esys_PolicyCommandCode_Finish(
    ESYS_CONTEXT *esysContext);

/* Table 135 - TPM2_PolicyPhysicalPresence Command */

TSS2_RC
Esys_PolicyPhysicalPresence(
    ESYS_CONTEXT *esysContext,
    ESYS_TR policySession,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3);

TSS2_RC
Esys_PolicyPhysicalPresence_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR policySession,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3);

TSS2_RC
Esys_PolicyPhysicalPresence_Finish(
    ESYS_CONTEXT *esysContext);

/* Table 137 - TPM2_PolicyCpHash Command */

TSS2_RC
Esys_PolicyCpHash(
    ESYS_CONTEXT *esysContext,
    ESYS_TR policySession,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_DIGEST *cpHashA);

TSS2_RC
Esys_PolicyCpHash_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR policySession,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_DIGEST *cpHashA);

TSS2_RC
Esys_PolicyCpHash_Finish(
    ESYS_CONTEXT *esysContext);

/* Table 139 - TPM2_PolicyNameHash Command */

TSS2_RC
Esys_PolicyNameHash(
    ESYS_CONTEXT *esysContext,
    ESYS_TR policySession,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_DIGEST *nameHash);

TSS2_RC
Esys_PolicyNameHash_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR policySession,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_DIGEST *nameHash);

TSS2_RC
Esys_PolicyNameHash_Finish(
    ESYS_CONTEXT *esysContext);

/* Table 141 - TPM2_PolicyDuplicationSelect Command */

TSS2_RC
Esys_PolicyDuplicationSelect(
    ESYS_CONTEXT *esysContext,
    ESYS_TR policySession,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_NAME *objectName,
    const TPM2B_NAME *newParentName,
    TPMI_YES_NO includeObject);

TSS2_RC
Esys_PolicyDuplicationSelect_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR policySession,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_NAME *objectName,
    const TPM2B_NAME *newParentName,
    TPMI_YES_NO includeObject);

TSS2_RC
Esys_PolicyDuplicationSelect_Finish(
    ESYS_CONTEXT *esysContext);

/* Table 143 - TPM2_PolicyAuthorize Command */

TSS2_RC
Esys_PolicyAuthorize(
    ESYS_CONTEXT *esysContext,
    ESYS_TR policySession,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_DIGEST *approvedPolicy,
    const TPM2B_NONCE *policyRef,
    const TPM2B_NAME *keySign,
    const TPMT_TK_VERIFIED *checkTicket);

TSS2_RC
Esys_PolicyAuthorize_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR policySession,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_DIGEST *approvedPolicy,
    const TPM2B_NONCE *policyRef,
    const TPM2B_NAME *keySign,
    const TPMT_TK_VERIFIED *checkTicket);

TSS2_RC
Esys_PolicyAuthorize_Finish(
    ESYS_CONTEXT *esysContext);

/* Table 145 - TPM2_PolicyAuthValue Command */

TSS2_RC
Esys_PolicyAuthValue(
    ESYS_CONTEXT *esysContext,
    ESYS_TR policySession,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3);

TSS2_RC
Esys_PolicyAuthValue_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR policySession,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3);

TSS2_RC
Esys_PolicyAuthValue_Finish(
    ESYS_CONTEXT *esysContext);

/* Table 147 - TPM2_PolicyPassword Command */

TSS2_RC
Esys_PolicyPassword(
    ESYS_CONTEXT *esysContext,
    ESYS_TR policySession,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3);

TSS2_RC
Esys_PolicyPassword_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR policySession,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3);

TSS2_RC
Esys_PolicyPassword_Finish(
    ESYS_CONTEXT *esysContext);

/* Table 149 - TPM2_PolicyGetDigest Command */

TSS2_RC
Esys_PolicyGetDigest(
    ESYS_CONTEXT *esysContext,
    ESYS_TR policySession,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    TPM2B_DIGEST **policyDigest);

TSS2_RC
Esys_PolicyGetDigest_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR policySession,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3);

TSS2_RC
Esys_PolicyGetDigest_Finish(
    ESYS_CONTEXT *esysContext,
    TPM2B_DIGEST **policyDigest);

/* Table 151 - TPM2_PolicyNvWritten Command */

TSS2_RC
Esys_PolicyNvWritten(
    ESYS_CONTEXT *esysContext,
    ESYS_TR policySession,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    TPMI_YES_NO writtenSet);

TSS2_RC
Esys_PolicyNvWritten_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR policySession,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    TPMI_YES_NO writtenSet);

TSS2_RC
Esys_PolicyNvWritten_Finish(
    ESYS_CONTEXT *esysContext);

/* Table 153 - TPM2_PolicyTemplate Command */

TSS2_RC
Esys_PolicyTemplate(
    ESYS_CONTEXT *esysContext,
    ESYS_TR policySession,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_DIGEST *templateHash);

TSS2_RC
Esys_PolicyTemplate_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR policySession,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_DIGEST *templateHash);

TSS2_RC
Esys_PolicyTemplate_Finish(
    ESYS_CONTEXT *esysContext);

/* Table 155 - TPM2_PolicyAuthorizeNV Command */

TSS2_RC
Esys_PolicyAuthorizeNV(
    ESYS_CONTEXT *esysContext,
    ESYS_TR authHandle,
    ESYS_TR nvIndex,
    ESYS_TR policySession,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3);

TSS2_RC
Esys_PolicyAuthorizeNV_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR authHandle,
    ESYS_TR nvIndex,
    ESYS_TR policySession,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3);

TSS2_RC
Esys_PolicyAuthorizeNV_Finish(
    ESYS_CONTEXT *esysContext);

/* Table 157 - TPM2_CreatePrimary Command */

TSS2_RC
Esys_CreatePrimary(
    ESYS_CONTEXT *esysContext,
    ESYS_TR primaryHandle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_SENSITIVE_CREATE *inSensitive,
    const TPM2B_PUBLIC *inPublic,
    const TPM2B_DATA *outsideInfo,
    const TPML_PCR_SELECTION *creationPCR,
    ESYS_TR *objectHandle,
    TPM2B_PUBLIC **outPublic,
    TPM2B_CREATION_DATA **creationData,
    TPM2B_DIGEST **creationHash,
    TPMT_TK_CREATION **creationTicket);

TSS2_RC
Esys_CreatePrimary_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR primaryHandle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_SENSITIVE_CREATE *inSensitive,
    const TPM2B_PUBLIC *inPublic,
    const TPM2B_DATA *outsideInfo,
    const TPML_PCR_SELECTION *creationPCR);

TSS2_RC
Esys_CreatePrimary_Finish(
    ESYS_CONTEXT *esysContext,
    ESYS_TR *objectHandle,
    TPM2B_PUBLIC **outPublic,
    TPM2B_CREATION_DATA **creationData,
    TPM2B_DIGEST **creationHash,
    TPMT_TK_CREATION **creationTicket);

/* Table 159 - TPM2_HierarchyControl Command */

TSS2_RC
Esys_HierarchyControl(
    ESYS_CONTEXT *esysContext,
    ESYS_TR authHandle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    ESYS_TR enable,
    TPMI_YES_NO state);

TSS2_RC
Esys_HierarchyControl_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR authHandle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    ESYS_TR enable,
    TPMI_YES_NO state);

TSS2_RC
Esys_HierarchyControl_Finish(
    ESYS_CONTEXT *esysContext);

/* Table 161 - TPM2_SetPrimaryPolicy Command */

TSS2_RC
Esys_SetPrimaryPolicy(
    ESYS_CONTEXT *esysContext,
    ESYS_TR authHandle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_DIGEST *authPolicy,
    TPMI_ALG_HASH hashAlg);

TSS2_RC
Esys_SetPrimaryPolicy_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR authHandle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_DIGEST *authPolicy,
    TPMI_ALG_HASH hashAlg);

TSS2_RC
Esys_SetPrimaryPolicy_Finish(
    ESYS_CONTEXT *esysContext);

/* Table 163 - TPM2_ChangePPS Command */

TSS2_RC
Esys_ChangePPS(
    ESYS_CONTEXT *esysContext,
    ESYS_TR authHandle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3);

TSS2_RC
Esys_ChangePPS_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR authHandle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3);

TSS2_RC
Esys_ChangePPS_Finish(
    ESYS_CONTEXT *esysContext);

/* Table 165 - TPM2_ChangeEPS Command */

TSS2_RC
Esys_ChangeEPS(
    ESYS_CONTEXT *esysContext,
    ESYS_TR authHandle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3);

TSS2_RC
Esys_ChangeEPS_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR authHandle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3);

TSS2_RC
Esys_ChangeEPS_Finish(
    ESYS_CONTEXT *esysContext);

/* Table 167 - TPM2_Clear Command */

TSS2_RC
Esys_Clear(
    ESYS_CONTEXT *esysContext,
    ESYS_TR authHandle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3);

TSS2_RC
Esys_Clear_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR authHandle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3);

TSS2_RC
Esys_Clear_Finish(
    ESYS_CONTEXT *esysContext);

/* Table 169 - TPM2_ClearControl Command */

TSS2_RC
Esys_ClearControl(
    ESYS_CONTEXT *esysContext,
    ESYS_TR auth,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    TPMI_YES_NO disable);

TSS2_RC
Esys_ClearControl_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR auth,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    TPMI_YES_NO disable);

TSS2_RC
Esys_ClearControl_Finish(
    ESYS_CONTEXT *esysContext);

/* Table 171 - TPM2_HierarchyChangeAuth Command */

TSS2_RC
Esys_HierarchyChangeAuth(
    ESYS_CONTEXT *esysContext,
    ESYS_TR authHandle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_AUTH *newAuth);

TSS2_RC
Esys_HierarchyChangeAuth_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR authHandle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_AUTH *newAuth);

TSS2_RC
Esys_HierarchyChangeAuth_Finish(
    ESYS_CONTEXT *esysContext);

/* Table 173 - TPM2_DictionaryAttackLockReset Command */

TSS2_RC
Esys_DictionaryAttackLockReset(
    ESYS_CONTEXT *esysContext,
    ESYS_TR lockHandle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3);

TSS2_RC
Esys_DictionaryAttackLockReset_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR lockHandle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3);

TSS2_RC
Esys_DictionaryAttackLockReset_Finish(
    ESYS_CONTEXT *esysContext);

/* Table 175 - TPM2_DictionaryAttackParameters Command */

TSS2_RC
Esys_DictionaryAttackParameters(
    ESYS_CONTEXT *esysContext,
    ESYS_TR lockHandle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    UINT32 newMaxTries,
    UINT32 newRecoveryTime,
    UINT32 lockoutRecovery);

TSS2_RC
Esys_DictionaryAttackParameters_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR lockHandle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    UINT32 newMaxTries,
    UINT32 newRecoveryTime,
    UINT32 lockoutRecovery);

TSS2_RC
Esys_DictionaryAttackParameters_Finish(
    ESYS_CONTEXT *esysContext);

/* Table 177 - TPM2_PP_Commands Command */

TSS2_RC
Esys_PP_Commands(
    ESYS_CONTEXT *esysContext,
    ESYS_TR auth,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPML_CC *setList,
    const TPML_CC *clearList);

TSS2_RC
Esys_PP_Commands_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR auth,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPML_CC *setList,
    const TPML_CC *clearList);

TSS2_RC
Esys_PP_Commands_Finish(
    ESYS_CONTEXT *esysContext);

/* Table 179 - TPM2_SetAlgorithmSet Command */

TSS2_RC
Esys_SetAlgorithmSet(
    ESYS_CONTEXT *esysContext,
    ESYS_TR authHandle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    UINT32 algorithmSet);

TSS2_RC
Esys_SetAlgorithmSet_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR authHandle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    UINT32 algorithmSet);

TSS2_RC
Esys_SetAlgorithmSet_Finish(
    ESYS_CONTEXT *esysContext);

/* Table 181 - TPM2_FieldUpgradeStart Command */

TSS2_RC
Esys_FieldUpgradeStart(
    ESYS_CONTEXT *esysContext,
    ESYS_TR authorization,
    ESYS_TR keyHandle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_DIGEST *fuDigest,
    const TPMT_SIGNATURE *manifestSignature);

TSS2_RC
Esys_FieldUpgradeStart_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR authorization,
    ESYS_TR keyHandle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_DIGEST *fuDigest,
    const TPMT_SIGNATURE *manifestSignature);

TSS2_RC
Esys_FieldUpgradeStart_Finish(
    ESYS_CONTEXT *esysContext);

/* Table 183 - TPM2_FieldUpgradeData Command */

TSS2_RC
Esys_FieldUpgradeData(
    ESYS_CONTEXT *esysContext,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_MAX_BUFFER *fuData,
    TPMT_HA **nextDigest,
    TPMT_HA **firstDigest);

TSS2_RC
Esys_FieldUpgradeData_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_MAX_BUFFER *fuData);

TSS2_RC
Esys_FieldUpgradeData_Finish(
    ESYS_CONTEXT *esysContext,
    TPMT_HA **nextDigest,
    TPMT_HA **firstDigest);

/* Table 185 - TPM2_FirmwareRead Command */

TSS2_RC
Esys_FirmwareRead(
    ESYS_CONTEXT *esysContext,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    UINT32 sequenceNumber,
    TPM2B_MAX_BUFFER **fuData);

TSS2_RC
Esys_FirmwareRead_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    UINT32 sequenceNumber);

TSS2_RC
Esys_FirmwareRead_Finish(
    ESYS_CONTEXT *esysContext,
    TPM2B_MAX_BUFFER **fuData);

/* Table 187 - TPM2_ContextSave Command */

TSS2_RC
Esys_ContextSave(
    ESYS_CONTEXT *esysContext,
    ESYS_TR saveHandle,
    TPMS_CONTEXT **context);

TSS2_RC
Esys_ContextSave_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR saveHandle);

TSS2_RC
Esys_ContextSave_Finish(
    ESYS_CONTEXT *esysContext,
    TPMS_CONTEXT **context);

/* Table 189 - TPM2_ContextLoad Command */

TSS2_RC
Esys_ContextLoad(
    ESYS_CONTEXT *esysContext,
    const TPMS_CONTEXT *context,
    ESYS_TR *loadedHandle);

TSS2_RC
Esys_ContextLoad_Async(
    ESYS_CONTEXT *esysContext,
    const TPMS_CONTEXT *context);

TSS2_RC
Esys_ContextLoad_Finish(
    ESYS_CONTEXT *esysContext,
    ESYS_TR *loadedHandle);

/* Table 191 - TPM2_FlushContext Command */

TSS2_RC
Esys_FlushContext(
    ESYS_CONTEXT *esysContext,
    ESYS_TR flushHandle);

TSS2_RC
Esys_FlushContext_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR flushHandle);

TSS2_RC
Esys_FlushContext_Finish(
    ESYS_CONTEXT *esysContext);

/* Table 193 - TPM2_EvictControl Command */

TSS2_RC
Esys_EvictControl(
    ESYS_CONTEXT *esysContext,
    ESYS_TR auth,
    ESYS_TR objectHandle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    TPMI_DH_PERSISTENT persistentHandle,
    ESYS_TR *newObjectHandle);

TSS2_RC
Esys_EvictControl_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR auth,
    ESYS_TR objectHandle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    TPMI_DH_PERSISTENT persistentHandle);

TSS2_RC
Esys_EvictControl_Finish(
    ESYS_CONTEXT *esysContext,
    ESYS_TR *newObjectHandle);

/* Table 195 - TPM2_ReadClock Command */

TSS2_RC
Esys_ReadClock(
    ESYS_CONTEXT *esysContext,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    TPMS_TIME_INFO **currentTime);

TSS2_RC
Esys_ReadClock_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3);

TSS2_RC
Esys_ReadClock_Finish(
    ESYS_CONTEXT *esysContext,
    TPMS_TIME_INFO **currentTime);

/* Table 197 - TPM2_ClockSet Command */

TSS2_RC
Esys_ClockSet(
    ESYS_CONTEXT *esysContext,
    ESYS_TR auth,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    UINT64 newTime);

TSS2_RC
Esys_ClockSet_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR auth,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    UINT64 newTime);

TSS2_RC
Esys_ClockSet_Finish(
    ESYS_CONTEXT *esysContext);

/* Table 199 - TPM2_ClockRateAdjust Command */

TSS2_RC
Esys_ClockRateAdjust(
    ESYS_CONTEXT *esysContext,
    ESYS_TR auth,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    TPM2_CLOCK_ADJUST rateAdjust);

TSS2_RC
Esys_ClockRateAdjust_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR auth,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    TPM2_CLOCK_ADJUST rateAdjust);

TSS2_RC
Esys_ClockRateAdjust_Finish(
    ESYS_CONTEXT *esysContext);

/* Table 201 - TPM2_GetCapability Command */

TSS2_RC
Esys_GetCapability(
    ESYS_CONTEXT *esysContext,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    TPM2_CAP capability,
    UINT32 property,
    UINT32 propertyCount,
    TPMI_YES_NO *moreData,
    TPMS_CAPABILITY_DATA **capabilityData);

TSS2_RC
Esys_GetCapability_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    TPM2_CAP capability,
    UINT32 property,
    UINT32 propertyCount);

TSS2_RC
Esys_GetCapability_Finish(
    ESYS_CONTEXT *esysContext,
    TPMI_YES_NO *moreData,
    TPMS_CAPABILITY_DATA **capabilityData);

/* Table 203 - TPM2_TestParms Command */

TSS2_RC
Esys_TestParms(
    ESYS_CONTEXT *esysContext,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPMT_PUBLIC_PARMS *parameters);

TSS2_RC
Esys_TestParms_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPMT_PUBLIC_PARMS *parameters);

TSS2_RC
Esys_TestParms_Finish(
    ESYS_CONTEXT *esysContext);

/* Table 205 - TPM2_NV_DefineSpace Command */

TSS2_RC
Esys_NV_DefineSpace(
    ESYS_CONTEXT *esysContext,
    ESYS_TR authHandle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_AUTH *auth,
    const TPM2B_NV_PUBLIC *publicInfo,
    ESYS_TR *nvHandle);

TSS2_RC
Esys_NV_DefineSpace_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR authHandle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_AUTH *auth,
    const TPM2B_NV_PUBLIC *publicInfo);

TSS2_RC
Esys_NV_DefineSpace_Finish(
    ESYS_CONTEXT *esysContext,
    ESYS_TR *nvHandle);

/* Table 207 - TPM2_NV_UndefineSpace Command */

TSS2_RC
Esys_NV_UndefineSpace(
    ESYS_CONTEXT *esysContext,
    ESYS_TR authHandle,
    ESYS_TR nvIndex,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3);

TSS2_RC
Esys_NV_UndefineSpace_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR authHandle,
    ESYS_TR nvIndex,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3);

TSS2_RC
Esys_NV_UndefineSpace_Finish(
    ESYS_CONTEXT *esysContext);

/* Table 209 - TPM2_NV_UndefineSpaceSpecial Command */

TSS2_RC
Esys_NV_UndefineSpaceSpecial(
    ESYS_CONTEXT *esysContext,
    ESYS_TR nvIndex,
    ESYS_TR platform,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3);

TSS2_RC
Esys_NV_UndefineSpaceSpecial_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR nvIndex,
    ESYS_TR platform,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3);

TSS2_RC
Esys_NV_UndefineSpaceSpecial_Finish(
    ESYS_CONTEXT *esysContext);

/* Table 211 - TPM2_NV_ReadPublic Command */

TSS2_RC
Esys_NV_ReadPublic(
    ESYS_CONTEXT *esysContext,
    ESYS_TR nvIndex,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    TPM2B_NV_PUBLIC **nvPublic,
    TPM2B_NAME **nvName);

TSS2_RC
Esys_NV_ReadPublic_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR nvIndex,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3);

TSS2_RC
Esys_NV_ReadPublic_Finish(
    ESYS_CONTEXT *esysContext,
    TPM2B_NV_PUBLIC **nvPublic,
    TPM2B_NAME **nvName);

/* Table 213 - TPM2_NV_Write Command */

TSS2_RC
Esys_NV_Write(
    ESYS_CONTEXT *esysContext,
    ESYS_TR authHandle,
    ESYS_TR nvIndex,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_MAX_NV_BUFFER *data,
    UINT16 offset);

TSS2_RC
Esys_NV_Write_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR authHandle,
    ESYS_TR nvIndex,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_MAX_NV_BUFFER *data,
    UINT16 offset);

TSS2_RC
Esys_NV_Write_Finish(
    ESYS_CONTEXT *esysContext);

/* Table 215 - TPM2_NV_Increment Command */

TSS2_RC
Esys_NV_Increment(
    ESYS_CONTEXT *esysContext,
    ESYS_TR authHandle,
    ESYS_TR nvIndex,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3);

TSS2_RC
Esys_NV_Increment_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR authHandle,
    ESYS_TR nvIndex,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3);

TSS2_RC
Esys_NV_Increment_Finish(
    ESYS_CONTEXT *esysContext);

/* Table 217 - TPM2_NV_Extend Command */

TSS2_RC
Esys_NV_Extend(
    ESYS_CONTEXT *esysContext,
    ESYS_TR authHandle,
    ESYS_TR nvIndex,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_MAX_NV_BUFFER *data);

TSS2_RC
Esys_NV_Extend_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR authHandle,
    ESYS_TR nvIndex,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_MAX_NV_BUFFER *data);

TSS2_RC
Esys_NV_Extend_Finish(
    ESYS_CONTEXT *esysContext);

/* Table 219 - TPM2_NV_SetBits Command */

TSS2_RC
Esys_NV_SetBits(
    ESYS_CONTEXT *esysContext,
    ESYS_TR authHandle,
    ESYS_TR nvIndex,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    UINT64 bits);

TSS2_RC
Esys_NV_SetBits_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR authHandle,
    ESYS_TR nvIndex,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    UINT64 bits);

TSS2_RC
Esys_NV_SetBits_Finish(
    ESYS_CONTEXT *esysContext);

/* Table 221 - TPM2_NV_WriteLock Command */

TSS2_RC
Esys_NV_WriteLock(
    ESYS_CONTEXT *esysContext,
    ESYS_TR authHandle,
    ESYS_TR nvIndex,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3);

TSS2_RC
Esys_NV_WriteLock_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR authHandle,
    ESYS_TR nvIndex,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3);

TSS2_RC
Esys_NV_WriteLock_Finish(
    ESYS_CONTEXT *esysContext);

/* Table 223 - TPM2_NV_GlobalWriteLock Command */

TSS2_RC
Esys_NV_GlobalWriteLock(
    ESYS_CONTEXT *esysContext,
    ESYS_TR authHandle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3);

TSS2_RC
Esys_NV_GlobalWriteLock_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR authHandle,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3);

TSS2_RC
Esys_NV_GlobalWriteLock_Finish(
    ESYS_CONTEXT *esysContext);

/* Table 225 - TPM2_NV_Read Command */

TSS2_RC
Esys_NV_Read(
    ESYS_CONTEXT *esysContext,
    ESYS_TR authHandle,
    ESYS_TR nvIndex,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    UINT16 size,
    UINT16 offset,
    TPM2B_MAX_NV_BUFFER **data);

TSS2_RC
Esys_NV_Read_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR authHandle,
    ESYS_TR nvIndex,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    UINT16 size,
    UINT16 offset);

TSS2_RC
Esys_NV_Read_Finish(
    ESYS_CONTEXT *esysContext,
    TPM2B_MAX_NV_BUFFER **data);

/* Table 227 - TPM2_NV_ReadLock Command */

TSS2_RC
Esys_NV_ReadLock(
    ESYS_CONTEXT *esysContext,
    ESYS_TR authHandle,
    ESYS_TR nvIndex,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3);

TSS2_RC
Esys_NV_ReadLock_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR authHandle,
    ESYS_TR nvIndex,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3);

TSS2_RC
Esys_NV_ReadLock_Finish(
    ESYS_CONTEXT *esysContext);

/* Table 229 - TPM2_NV_ChangeAuth Command */

TSS2_RC
Esys_NV_ChangeAuth(
    ESYS_CONTEXT *esysContext,
    ESYS_TR nvIndex,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_AUTH *newAuth);

TSS2_RC
Esys_NV_ChangeAuth_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR nvIndex,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_AUTH *newAuth);

TSS2_RC
Esys_NV_ChangeAuth_Finish(
    ESYS_CONTEXT *esysContext);

/* Table 231 - TPM2_NV_Certify Command */

TSS2_RC
Esys_NV_Certify(
    ESYS_CONTEXT *esysContext,
    ESYS_TR signHandle,
    ESYS_TR authHandle,
    ESYS_TR nvIndex,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_DATA *qualifyingData,
    const TPMT_SIG_SCHEME *inScheme,
    UINT16 size,
    UINT16 offset,
    TPM2B_ATTEST **certifyInfo,
    TPMT_SIGNATURE **signature);

TSS2_RC
Esys_NV_Certify_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR signHandle,
    ESYS_TR authHandle,
    ESYS_TR nvIndex,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_DATA *qualifyingData,
    const TPMT_SIG_SCHEME *inScheme,
    UINT16 size,
    UINT16 offset);

TSS2_RC
Esys_NV_Certify_Finish(
    ESYS_CONTEXT *esysContext,
    TPM2B_ATTEST **certifyInfo,
    TPMT_SIGNATURE **signature);

/* Table 233 - TPM2_Vendor_TCG_Test Command */

TSS2_RC
Esys_Vendor_TCG_Test(
    ESYS_CONTEXT *esysContext,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_DATA *inputData,
    TPM2B_DATA **outputData);

TSS2_RC
Esys_Vendor_TCG_Test_Async(
    ESYS_CONTEXT *esysContext,
    ESYS_TR shandle1,
    ESYS_TR shandle2,
    ESYS_TR shandle3,
    const TPM2B_DATA *inputData);

TSS2_RC
Esys_Vendor_TCG_Test_Finish(
    ESYS_CONTEXT *esysContext,
    TPM2B_DATA **outputData);

/*
 * TPM 2.0 ESAPI Helper Functions
 */
void
Esys_Free(
    void *__ptr);

TSS2_RC
Esys_GetSysContext(
    ESYS_CONTEXT *esys_context,
    TSS2_SYS_CONTEXT **sys_context);

TSS2_RC
Esys_SetCryptoCallbacks(
    ESYS_CONTEXT *esysContext,
    ESYS_CRYPTO_CALLBACKS *callbacks);

#ifdef __cplusplus
}
#endif

#endif /* TSS2_ESYS_H */
