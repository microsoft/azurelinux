/* SPDX-License-Identifier: BSD-2-Clause */
/***********************************************************************;
 * Copyright (c) 2015-2018, Intel Corporation
 *
 * Copyright 2015, Andreas Fuchs @ Fraunhofer SIT
 *
 * All rights reserved.
 ***********************************************************************/

#ifndef TSS2_SYS_H
#define TSS2_SYS_H

#include "tss2_common.h"
#include "tss2_tcti.h"
#include "tss2_tpm2_types.h"

#ifndef TSS2_API_VERSION_1_2_1_108
#error Version mismatch among TSS2 header files.
#endif  /* TSS2_API_VERSION_1_2_1_108 */

#ifdef __cplusplus
extern "C" {
#endif

/* SAPI context blob */
typedef struct _TSS2_SYS_OPAQUE_CONTEXT_BLOB TSS2_SYS_CONTEXT;

#define TSS2_SYS_MAX_SESSIONS 3

/* Input structure for authorization area(s). */
typedef struct TSS2L_SYS_AUTH_COMMAND TSS2L_SYS_AUTH_COMMAND;
struct TSS2L_SYS_AUTH_COMMAND {
    uint16_t count;
    TPMS_AUTH_COMMAND auths[TSS2_SYS_MAX_SESSIONS];
};

typedef struct TSS2L_SYS_AUTH_RESPONSE TSS2L_SYS_AUTH_RESPONSE;
struct TSS2L_SYS_AUTH_RESPONSE {
    uint16_t count;
    TPMS_AUTH_RESPONSE auths[TSS2_SYS_MAX_SESSIONS];
};

size_t  Tss2_Sys_GetContextSize(
    size_t maxCommandResponseSize);

TSS2_RC Tss2_Sys_Initialize(
    TSS2_SYS_CONTEXT *sysContext,
    size_t contextSize,
    TSS2_TCTI_CONTEXT *tctiContext,
    TSS2_ABI_VERSION *abiVersion);

void Tss2_Sys_Finalize(
    TSS2_SYS_CONTEXT *sysContext);

TSS2_RC Tss2_Sys_GetTctiContext(
    TSS2_SYS_CONTEXT *sysContext,
    TSS2_TCTI_CONTEXT **tctiContext);

/* Command Preparation Functions */
TSS2_RC Tss2_Sys_GetDecryptParam(
    TSS2_SYS_CONTEXT *sysContext,
    size_t *decryptParamSize,
    const uint8_t **decryptParamBuffer);

TSS2_RC Tss2_Sys_SetDecryptParam(
    TSS2_SYS_CONTEXT *sysContext,
    size_t decryptParamSize,
    const uint8_t *decryptParamBuffer);

TSS2_RC Tss2_Sys_GetCpBuffer(
    TSS2_SYS_CONTEXT *sysContext,
    size_t *cpBufferUsedSize,
    const uint8_t **cpBuffer);

TSS2_RC Tss2_Sys_SetCmdAuths(
    TSS2_SYS_CONTEXT *sysContext,
    const TSS2L_SYS_AUTH_COMMAND *cmdAuthsArray);

/* Command Execution Functions */
TSS2_RC Tss2_Sys_ExecuteAsync(
    TSS2_SYS_CONTEXT *sysContext);

TSS2_RC Tss2_Sys_ExecuteFinish(
    TSS2_SYS_CONTEXT *sysContext,
    int32_t timeout);

TSS2_RC Tss2_Sys_Execute(
    TSS2_SYS_CONTEXT *sysContext);

/* Command Completion functions */
TSS2_RC Tss2_Sys_GetCommandCode(
    TSS2_SYS_CONTEXT *sysContext,
    UINT8 *commandCode);

TSS2_RC Tss2_Sys_GetRspAuths(
    TSS2_SYS_CONTEXT *sysContext,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_GetEncryptParam(
    TSS2_SYS_CONTEXT *sysContext,
    size_t *encryptParamSize,
    const uint8_t **encryptParamBuffer);

TSS2_RC Tss2_Sys_SetEncryptParam(
    TSS2_SYS_CONTEXT *sysContext,
    size_t encryptParamSize,
    const uint8_t *encryptParamBuffer);

TSS2_RC Tss2_Sys_GetRpBuffer(
    TSS2_SYS_CONTEXT *sysContext,
    size_t *rpBufferUsedSize,
    const uint8_t **rpBuffer);

TSS2_RC Tss2_Sys_Startup_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPM2_SU startupType);

TSS2_RC Tss2_Sys_Startup_Complete(
    TSS2_SYS_CONTEXT *sysContext);

TSS2_RC Tss2_Sys_Startup(
    TSS2_SYS_CONTEXT *sysContext,
    TPM2_SU startupType);

TSS2_RC Tss2_Sys_Shutdown_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPM2_SU shutdownType);

TSS2_RC Tss2_Sys_Shutdown_Complete(
    TSS2_SYS_CONTEXT *sysContext);

TSS2_RC Tss2_Sys_Shutdown(
    TSS2_SYS_CONTEXT *sysContext,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    TPM2_SU shutdownType,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_SelfTest_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_YES_NO fullTest);

TSS2_RC Tss2_Sys_SelfTest_Complete(
    TSS2_SYS_CONTEXT *sysContext);

TSS2_RC Tss2_Sys_SelfTest(
    TSS2_SYS_CONTEXT *sysContext,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    TPMI_YES_NO fullTest,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_IncrementalSelfTest_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    const TPML_ALG *toTest);

TSS2_RC Tss2_Sys_IncrementalSelfTest_Complete(
    TSS2_SYS_CONTEXT *sysContext,
    TPML_ALG *toDoList);

TSS2_RC Tss2_Sys_IncrementalSelfTest(
    TSS2_SYS_CONTEXT *sysContext,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    const TPML_ALG *toTest,
    TPML_ALG *toDoList,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_GetTestResult_Prepare(
    TSS2_SYS_CONTEXT *sysContext);

TSS2_RC Tss2_Sys_GetTestResult_Complete(
    TSS2_SYS_CONTEXT *sysContext,
    TPM2B_MAX_BUFFER *outData,
    TPM2_RC *testResult);

TSS2_RC Tss2_Sys_GetTestResult(
    TSS2_SYS_CONTEXT *sysContext,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    TPM2B_MAX_BUFFER *outData,
    TPM2_RC *testResult,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_StartAuthSession_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_DH_OBJECT tpmKey,
    TPMI_DH_ENTITY bind,
    const TPM2B_NONCE *nonceCaller,
    const TPM2B_ENCRYPTED_SECRET *encryptedSalt,
    TPM2_SE sessionType,
    const TPMT_SYM_DEF    *symmetric,
    TPMI_ALG_HASH authHash);

TSS2_RC Tss2_Sys_StartAuthSession_Complete(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_SH_AUTH_SESSION *sessionHandle,
    TPM2B_NONCE *nonceTPM);

TSS2_RC Tss2_Sys_StartAuthSession(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_DH_OBJECT tpmKey,
    TPMI_DH_ENTITY bind,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    const TPM2B_NONCE *nonceCaller,
    const TPM2B_ENCRYPTED_SECRET *encryptedSalt,
    TPM2_SE sessionType,
    const TPMT_SYM_DEF    *symmetric,
    TPMI_ALG_HASH authHash,
    TPMI_SH_AUTH_SESSION *sessionHandle,
    TPM2B_NONCE *nonceTPM,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_PolicyRestart_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_SH_POLICY sessionHandle);

TSS2_RC Tss2_Sys_PolicyRestart_Complete(
    TSS2_SYS_CONTEXT *sysContext);

TSS2_RC Tss2_Sys_PolicyRestart(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_SH_POLICY sessionHandle,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_Create_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_DH_OBJECT parentHandle,
    const TPM2B_SENSITIVE_CREATE *inSensitive,
    const TPM2B_PUBLIC *inPublic,
    const TPM2B_DATA *outsideInfo,
    const TPML_PCR_SELECTION *creationPCR);

TSS2_RC Tss2_Sys_Create_Complete(
    TSS2_SYS_CONTEXT *sysContext,
    TPM2B_PRIVATE *outPrivate,
    TPM2B_PUBLIC *outPublic,
    TPM2B_CREATION_DATA *creationData,
    TPM2B_DIGEST *creationHash,
    TPMT_TK_CREATION *creationTicket);

TSS2_RC Tss2_Sys_Create(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_DH_OBJECT parentHandle,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    const TPM2B_SENSITIVE_CREATE *inSensitive,
    const TPM2B_PUBLIC *inPublic,
    const TPM2B_DATA *outsideInfo,
    const TPML_PCR_SELECTION *creationPCR,
    TPM2B_PRIVATE *outPrivate,
    TPM2B_PUBLIC *outPublic,
    TPM2B_CREATION_DATA *creationData,
    TPM2B_DIGEST *creationHash,
    TPMT_TK_CREATION *creationTicket,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray
    );

TSS2_RC Tss2_Sys_Load_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_DH_OBJECT parentHandle,
    const TPM2B_PRIVATE *inPrivate,
    const TPM2B_PUBLIC *inPublic
    );

TSS2_RC Tss2_Sys_Load_Complete(
    TSS2_SYS_CONTEXT *sysContext,
    TPM2_HANDLE *objectHandle,
    TPM2B_NAME *name
    );

TSS2_RC Tss2_Sys_Load(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_DH_OBJECT parentHandle,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    const TPM2B_PRIVATE *inPrivate,
    const TPM2B_PUBLIC *inPublic,
    TPM2_HANDLE *objectHandle,
    TPM2B_NAME *name,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray
    );

TSS2_RC Tss2_Sys_LoadExternal_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    const TPM2B_SENSITIVE *inPrivate,
    const TPM2B_PUBLIC *inPublic,
    TPMI_RH_HIERARCHY hierarchy);

TSS2_RC Tss2_Sys_LoadExternal_Complete(
    TSS2_SYS_CONTEXT *sysContext,
    TPM2_HANDLE *objectHandle,
    TPM2B_NAME *name);

TSS2_RC Tss2_Sys_LoadExternal(
    TSS2_SYS_CONTEXT *sysContext,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    const TPM2B_SENSITIVE *inPrivate,
    const TPM2B_PUBLIC *inPublic,
    TPMI_RH_HIERARCHY hierarchy,
    TPM2_HANDLE *objectHandle,
    TPM2B_NAME *name,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_ReadPublic_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_DH_OBJECT objectHandle);

TSS2_RC Tss2_Sys_ReadPublic_Complete(
    TSS2_SYS_CONTEXT *sysContext,
    TPM2B_PUBLIC *outPublic,
    TPM2B_NAME *name,
    TPM2B_NAME *qualifiedName);

TSS2_RC Tss2_Sys_ReadPublic(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_DH_OBJECT objectHandle,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    TPM2B_PUBLIC *outPublic,
    TPM2B_NAME *name,
    TPM2B_NAME *qualifiedName,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_ActivateCredential_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_DH_OBJECT activateHandle,
    TPMI_DH_OBJECT keyHandle,
    const TPM2B_ID_OBJECT *credentialBlob,
    const TPM2B_ENCRYPTED_SECRET *secret);

TSS2_RC Tss2_Sys_ActivateCredential_Complete(
    TSS2_SYS_CONTEXT *sysContext,
    TPM2B_DIGEST *certInfo);

TSS2_RC Tss2_Sys_ActivateCredential(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_DH_OBJECT activateHandle,
    TPMI_DH_OBJECT keyHandle,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    const TPM2B_ID_OBJECT *credentialBlob,
    const TPM2B_ENCRYPTED_SECRET *secret,
    TPM2B_DIGEST *certInfo,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_MakeCredential_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_DH_OBJECT handle,
    const TPM2B_DIGEST *credential,
    const TPM2B_NAME *objectName);

TSS2_RC Tss2_Sys_MakeCredential_Complete(
    TSS2_SYS_CONTEXT *sysContext,
    TPM2B_ID_OBJECT *credentialBlob,
    TPM2B_ENCRYPTED_SECRET *secret);

TSS2_RC Tss2_Sys_MakeCredential(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_DH_OBJECT handle,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    const TPM2B_DIGEST *credential,
    const TPM2B_NAME *objectName,
    TPM2B_ID_OBJECT *credentialBlob,
    TPM2B_ENCRYPTED_SECRET *secret,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_Unseal_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_DH_OBJECT itemHandle);

TSS2_RC Tss2_Sys_Unseal_Complete(
    TSS2_SYS_CONTEXT *sysContext,
    TPM2B_SENSITIVE_DATA *outData);

TSS2_RC Tss2_Sys_Unseal(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_DH_OBJECT itemHandle,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    TPM2B_SENSITIVE_DATA *outData,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_ObjectChangeAuth_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_DH_OBJECT objectHandle,
    TPMI_DH_OBJECT parentHandle,
    const TPM2B_AUTH *newAuth);

TSS2_RC Tss2_Sys_ObjectChangeAuth_Complete(
    TSS2_SYS_CONTEXT *sysContext,
    TPM2B_PRIVATE *outPrivate);

TSS2_RC Tss2_Sys_ObjectChangeAuth(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_DH_OBJECT objectHandle,
    TPMI_DH_OBJECT parentHandle,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    const TPM2B_AUTH *newAuth,
    TPM2B_PRIVATE *outPrivate,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_Duplicate_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_DH_OBJECT objectHandle,
    TPMI_DH_OBJECT newParentHandle,
    const TPM2B_DATA *encryptionKeyIn,
    const TPMT_SYM_DEF_OBJECT *symmetricAlg);

TSS2_RC Tss2_Sys_Duplicate_Complete(
    TSS2_SYS_CONTEXT *sysContext,
    TPM2B_DATA *encryptionKeyOut,
    TPM2B_PRIVATE *duplicate,
    TPM2B_ENCRYPTED_SECRET *outSymSeed);

TSS2_RC Tss2_Sys_Duplicate(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_DH_OBJECT objectHandle,
    TPMI_DH_OBJECT newParentHandle,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    const TPM2B_DATA *encryptionKeyIn,
    const TPMT_SYM_DEF_OBJECT *symmetricAlg,
    TPM2B_DATA *encryptionKeyOut,
    TPM2B_PRIVATE *duplicate,
    TPM2B_ENCRYPTED_SECRET *outSymSeed,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_Rewrap_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_DH_OBJECT oldParent,
    TPMI_DH_OBJECT newParent,
    const TPM2B_PRIVATE *inDuplicate,
    const TPM2B_NAME *name,
    const TPM2B_ENCRYPTED_SECRET *inSymSeed);

TSS2_RC Tss2_Sys_Rewrap_Complete(
    TSS2_SYS_CONTEXT *sysContext,
    TPM2B_PRIVATE *outDuplicate,
    TPM2B_ENCRYPTED_SECRET *outSymSeed);

TSS2_RC Tss2_Sys_Rewrap(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_DH_OBJECT oldParent,
    TPMI_DH_OBJECT newParent,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    const TPM2B_PRIVATE *inDuplicate,
    const TPM2B_NAME *name,
    const TPM2B_ENCRYPTED_SECRET *inSymSeed,
    TPM2B_PRIVATE *outDuplicate,
    TPM2B_ENCRYPTED_SECRET *outSymSeed,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_Import_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_DH_OBJECT parentHandle,
    const TPM2B_DATA *encryptionKey,
    const TPM2B_PUBLIC *objectPublic,
    const TPM2B_PRIVATE *duplicate,
    const TPM2B_ENCRYPTED_SECRET *inSymSeed,
    const TPMT_SYM_DEF_OBJECT *symmetricAlg);

TSS2_RC Tss2_Sys_Import_Complete(
    TSS2_SYS_CONTEXT *sysContext,
    TPM2B_PRIVATE *outPrivate);

TSS2_RC Tss2_Sys_Import(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_DH_OBJECT parentHandle,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    const TPM2B_DATA *encryptionKey,
    const TPM2B_PUBLIC *objectPublic,
    const TPM2B_PRIVATE *duplicate,
    const TPM2B_ENCRYPTED_SECRET *inSymSeed,
    const TPMT_SYM_DEF_OBJECT *symmetricAlg,
    TPM2B_PRIVATE *outPrivate,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_RSA_Encrypt_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_DH_OBJECT keyHandle,
    const TPM2B_PUBLIC_KEY_RSA *message,
    const TPMT_RSA_DECRYPT *inScheme,
    const TPM2B_DATA *label);

TSS2_RC Tss2_Sys_RSA_Encrypt_Complete(
    TSS2_SYS_CONTEXT *sysContext,
    TPM2B_PUBLIC_KEY_RSA *outData);

TSS2_RC Tss2_Sys_RSA_Encrypt(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_DH_OBJECT keyHandle,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    const TPM2B_PUBLIC_KEY_RSA *message,
    const TPMT_RSA_DECRYPT *inScheme,
    const TPM2B_DATA *label,
    TPM2B_PUBLIC_KEY_RSA *outData,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_RSA_Decrypt_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_DH_OBJECT keyHandle,
    const TPM2B_PUBLIC_KEY_RSA *cipherText,
    const TPMT_RSA_DECRYPT *inScheme,
    const TPM2B_DATA *label);

TSS2_RC Tss2_Sys_RSA_Decrypt_Complete(
    TSS2_SYS_CONTEXT *sysContext,
    TPM2B_PUBLIC_KEY_RSA *message);

TSS2_RC Tss2_Sys_RSA_Decrypt(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_DH_OBJECT keyHandle,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    const TPM2B_PUBLIC_KEY_RSA *cipherText,
    const TPMT_RSA_DECRYPT *inScheme,
    const TPM2B_DATA *label,
    TPM2B_PUBLIC_KEY_RSA *message,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_ECDH_KeyGen_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_DH_OBJECT keyHandle);

TSS2_RC Tss2_Sys_ECDH_KeyGen_Complete(
    TSS2_SYS_CONTEXT *sysContext,
    TPM2B_ECC_POINT *zPoint,
    TPM2B_ECC_POINT *pubPoint);

TSS2_RC Tss2_Sys_ECDH_KeyGen(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_DH_OBJECT keyHandle,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    TPM2B_ECC_POINT *zPoint,
    TPM2B_ECC_POINT *pubPoint,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_ECDH_ZGen_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_DH_OBJECT keyHandle,
    const TPM2B_ECC_POINT *inPoint);

TSS2_RC Tss2_Sys_ECDH_ZGen_Complete(
    TSS2_SYS_CONTEXT *sysContext,
    TPM2B_ECC_POINT *outPoint);

TSS2_RC Tss2_Sys_ECDH_ZGen(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_DH_OBJECT keyHandle,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    const TPM2B_ECC_POINT *inPoint,
    TPM2B_ECC_POINT *outPoint,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_ECC_Parameters_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_ECC_CURVE curveID);

TSS2_RC Tss2_Sys_ECC_Parameters_Complete(
    TSS2_SYS_CONTEXT *sysContext,
    TPMS_ALGORITHM_DETAIL_ECC *parameters);

TSS2_RC Tss2_Sys_ECC_Parameters(
    TSS2_SYS_CONTEXT *sysContext,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    TPMI_ECC_CURVE curveID,
    TPMS_ALGORITHM_DETAIL_ECC *parameters,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_ZGen_2Phase_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_DH_OBJECT keyA,
    const TPM2B_ECC_POINT *inQsB,
    const TPM2B_ECC_POINT *inQeB,
    TPMI_ECC_KEY_EXCHANGE inScheme,
    UINT16 counter);

TSS2_RC Tss2_Sys_ZGen_2Phase_Complete(
    TSS2_SYS_CONTEXT *sysContext,
    TPM2B_ECC_POINT *outZ1,
    TPM2B_ECC_POINT *outZ2);

TSS2_RC Tss2_Sys_ZGen_2Phase(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_DH_OBJECT keyA,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    const TPM2B_ECC_POINT *inQsB,
    const TPM2B_ECC_POINT *inQeB,
    TPMI_ECC_KEY_EXCHANGE inScheme,
    UINT16 counter,
    TPM2B_ECC_POINT *outZ1,
    TPM2B_ECC_POINT *outZ2,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_EncryptDecrypt_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_DH_OBJECT keyHandle,
    TPMI_YES_NO decrypt,
    TPMI_ALG_CIPHER_MODE mode,
    const TPM2B_IV *ivIn,
    const TPM2B_MAX_BUFFER *inData);

TSS2_RC Tss2_Sys_EncryptDecrypt_Complete(
    TSS2_SYS_CONTEXT *sysContext,
    TPM2B_MAX_BUFFER *outData,
    TPM2B_IV *ivOut);

TSS2_RC Tss2_Sys_EncryptDecrypt(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_DH_OBJECT keyHandle,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    TPMI_YES_NO decrypt,
    TPMI_ALG_CIPHER_MODE mode,
    const TPM2B_IV *ivIn,
    const TPM2B_MAX_BUFFER *inData,
    TPM2B_MAX_BUFFER *outData,
    TPM2B_IV *ivOut,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_EncryptDecrypt2_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_DH_OBJECT keyHandle,
    const TPM2B_MAX_BUFFER *inData,
    TPMI_YES_NO decrypt,
    TPMI_ALG_CIPHER_MODE mode,
    const TPM2B_IV *ivIn);

TSS2_RC Tss2_Sys_EncryptDecrypt2_Complete(
    TSS2_SYS_CONTEXT *sysContext,
    TPM2B_MAX_BUFFER *outData,
    TPM2B_IV *ivOut);

TSS2_RC Tss2_Sys_EncryptDecrypt2(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_DH_OBJECT keyHandle,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    const TPM2B_MAX_BUFFER *inData,
    TPMI_YES_NO decrypt,
    TPMI_ALG_CIPHER_MODE mode,
    const TPM2B_IV *ivIn,
    TPM2B_MAX_BUFFER *outData,
    TPM2B_IV *ivOut,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_Hash_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    const TPM2B_MAX_BUFFER *data,
    TPMI_ALG_HASH hashAlg,
    TPMI_RH_HIERARCHY hierarchy);

TSS2_RC Tss2_Sys_Hash_Complete(
    TSS2_SYS_CONTEXT *sysContext,
    TPM2B_DIGEST *outHash,
    TPMT_TK_HASHCHECK *validation);

TSS2_RC Tss2_Sys_Hash(
    TSS2_SYS_CONTEXT *sysContext,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    const TPM2B_MAX_BUFFER *data,
    TPMI_ALG_HASH hashAlg,
    TPMI_RH_HIERARCHY hierarchy,
    TPM2B_DIGEST *outHash,
    TPMT_TK_HASHCHECK *validation,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_HMAC_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_DH_OBJECT handle,
    const TPM2B_MAX_BUFFER *buffer,
    TPMI_ALG_HASH hashAlg);

TSS2_RC Tss2_Sys_HMAC_Complete(
    TSS2_SYS_CONTEXT *sysContext,
    TPM2B_DIGEST *outHMAC);

TSS2_RC Tss2_Sys_HMAC(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_DH_OBJECT handle,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    const TPM2B_MAX_BUFFER *buffer,
    TPMI_ALG_HASH hashAlg,
    TPM2B_DIGEST *outHMAC,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_MAC_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_DH_OBJECT handle,
    const TPM2B_MAX_BUFFER *buffer,
    TPMI_ALG_MAC_SCHEME inScheme);

TSS2_RC Tss2_Sys_MAC_Complete(
    TSS2_SYS_CONTEXT *sysContext,
    TPM2B_DIGEST *outMAC);

TSS2_RC Tss2_Sys_MAC(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_DH_OBJECT handle,
    const TSS2L_SYS_AUTH_COMMAND *cmdAuths,
    const TPM2B_MAX_BUFFER *buffer,
    TPMI_ALG_MAC_SCHEME inScheme,
    TPM2B_DIGEST *outMAC,
    TSS2L_SYS_AUTH_RESPONSE *rspAuths);

TSS2_RC Tss2_Sys_GetRandom_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    UINT16 bytesRequested);

TSS2_RC Tss2_Sys_GetRandom_Complete(
    TSS2_SYS_CONTEXT *sysContext,
    TPM2B_DIGEST *randomBytes);

TSS2_RC Tss2_Sys_GetRandom(
    TSS2_SYS_CONTEXT *sysContext,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    UINT16 bytesRequested,
    TPM2B_DIGEST *randomBytes,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_StirRandom_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    const TPM2B_SENSITIVE_DATA *inData);

TSS2_RC Tss2_Sys_StirRandom_Complete(
    TSS2_SYS_CONTEXT *sysContext);

TSS2_RC Tss2_Sys_StirRandom(
    TSS2_SYS_CONTEXT *sysContext,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    const TPM2B_SENSITIVE_DATA *inData,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_HMAC_Start_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_DH_OBJECT handle,
    const TPM2B_AUTH *auth,
    TPMI_ALG_HASH hashAlg);

TSS2_RC Tss2_Sys_HMAC_Start_Complete(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_DH_OBJECT *sequenceHandle);

TSS2_RC Tss2_Sys_HMAC_Start(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_DH_OBJECT handle,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    const TPM2B_AUTH *auth,
    TPMI_ALG_HASH hashAlg,
    TPMI_DH_OBJECT *sequenceHandle,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_MAC_Start_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_DH_OBJECT handle,
    const TPM2B_AUTH *auth,
    TPMI_ALG_MAC_SCHEME inScheme);

TSS2_RC Tss2_Sys_MAC_Start_Complete(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_DH_OBJECT *sequenceHandle);

TSS2_RC Tss2_Sys_MAC_Start(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_DH_OBJECT handle,
    const TSS2L_SYS_AUTH_COMMAND *cmdAuths,
    const TPM2B_AUTH *auth,
    TPMI_ALG_MAC_SCHEME inScheme,
    TPMI_DH_OBJECT *sequenceHandle,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_HashSequenceStart_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    const TPM2B_AUTH *auth,
    TPMI_ALG_HASH hashAlg);

TSS2_RC Tss2_Sys_HashSequenceStart_Complete(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_DH_OBJECT *sequenceHandle);

TSS2_RC Tss2_Sys_HashSequenceStart(
    TSS2_SYS_CONTEXT *sysContext,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    const TPM2B_AUTH *auth,
    TPMI_ALG_HASH hashAlg,
    TPMI_DH_OBJECT *sequenceHandle,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_SequenceUpdate_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_DH_OBJECT sequenceHandle,
    const TPM2B_MAX_BUFFER *buffer);

TSS2_RC Tss2_Sys_SequenceUpdate_Complete(
    TSS2_SYS_CONTEXT *sysContext);

TSS2_RC Tss2_Sys_SequenceUpdate(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_DH_OBJECT sequenceHandle,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    const TPM2B_MAX_BUFFER *buffer,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_SequenceComplete_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_DH_OBJECT sequenceHandle,
    const TPM2B_MAX_BUFFER *buffer,
    TPMI_RH_HIERARCHY hierarchy);

TSS2_RC Tss2_Sys_SequenceComplete_Complete(
    TSS2_SYS_CONTEXT *sysContext,
    TPM2B_DIGEST *result,
    TPMT_TK_HASHCHECK *validation);

TSS2_RC Tss2_Sys_SequenceComplete(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_DH_OBJECT sequenceHandle,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    const TPM2B_MAX_BUFFER *buffer,
    TPMI_RH_HIERARCHY hierarchy,
    TPM2B_DIGEST *result,
    TPMT_TK_HASHCHECK *validation,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_EventSequenceComplete_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_DH_PCR pcrHandle,
    TPMI_DH_OBJECT sequenceHandle,
    const TPM2B_MAX_BUFFER *buffer);

TSS2_RC Tss2_Sys_EventSequenceComplete_Complete(
    TSS2_SYS_CONTEXT *sysContext,
    TPML_DIGEST_VALUES *results);

TSS2_RC Tss2_Sys_EventSequenceComplete(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_DH_PCR pcrHandle,
    TPMI_DH_OBJECT sequenceHandle,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    const TPM2B_MAX_BUFFER *buffer,
    TPML_DIGEST_VALUES *results,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_Certify_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_DH_OBJECT objectHandle,
    TPMI_DH_OBJECT signHandle,
    const TPM2B_DATA *qualifyingData,
    const TPMT_SIG_SCHEME *inScheme);

TSS2_RC Tss2_Sys_Certify_Complete(
    TSS2_SYS_CONTEXT *sysContext,
    TPM2B_ATTEST *certifyInfo,
    TPMT_SIGNATURE *signature);

TSS2_RC Tss2_Sys_Certify(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_DH_OBJECT objectHandle,
    TPMI_DH_OBJECT signHandle,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    const TPM2B_DATA *qualifyingData,
    const TPMT_SIG_SCHEME *inScheme,
    TPM2B_ATTEST *certifyInfo,
    TPMT_SIGNATURE *signature,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_CertifyX509_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_DH_OBJECT objectHandle,
    TPMI_DH_OBJECT signHandle,
    const TPM2B_DATA *reserved,
    const TPMT_SIG_SCHEME *inScheme,
    const TPM2B_MAX_BUFFER *partialCertificate);

TSS2_RC Tss2_Sys_CertifyX509_Complete(
    TSS2_SYS_CONTEXT *sysContext,
    TPM2B_MAX_BUFFER *addedToCertificate,
    TPM2B_DIGEST *tbsDigest,
    TPMT_SIGNATURE *signature);

TSS2_RC Tss2_Sys_CertifyX509(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_DH_OBJECT objectHandle,
    TPMI_DH_OBJECT signHandle,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    const TPM2B_DATA *reserved,
    const TPMT_SIG_SCHEME *inScheme,
    const TPM2B_MAX_BUFFER *partialCertificate,
    TPM2B_MAX_BUFFER *addedToCertificate,
    TPM2B_DIGEST *tbsDigest,
    TPMT_SIGNATURE *signature,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_CertifyCreation_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_DH_OBJECT signHandle,
    TPMI_DH_OBJECT objectHandle,
    const TPM2B_DATA *qualifyingData,
    const TPM2B_DIGEST *creationHash,
    const TPMT_SIG_SCHEME *inScheme,
    const TPMT_TK_CREATION *creationTicket);

TSS2_RC Tss2_Sys_CertifyCreation_Complete(
    TSS2_SYS_CONTEXT *sysContext,
    TPM2B_ATTEST *certifyInfo,
    TPMT_SIGNATURE *signature);

TSS2_RC Tss2_Sys_CertifyCreation(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_DH_OBJECT signHandle,
    TPMI_DH_OBJECT objectHandle,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    const TPM2B_DATA *qualifyingData,
    const TPM2B_DIGEST *creationHash,
    const TPMT_SIG_SCHEME *inScheme,
    const TPMT_TK_CREATION *creationTicket,
    TPM2B_ATTEST *certifyInfo,
    TPMT_SIGNATURE *signature,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_Quote_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_DH_OBJECT signHandle,
    const TPM2B_DATA *qualifyingData,
    const TPMT_SIG_SCHEME *inScheme,
    const TPML_PCR_SELECTION *PCRselect);

TSS2_RC Tss2_Sys_Quote_Complete(
    TSS2_SYS_CONTEXT *sysContext,
    TPM2B_ATTEST *quoted,
    TPMT_SIGNATURE *signature);

TSS2_RC Tss2_Sys_Quote(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_DH_OBJECT signHandle,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    const TPM2B_DATA *qualifyingData,
    const TPMT_SIG_SCHEME *inScheme,
    const TPML_PCR_SELECTION *PCRselect,
    TPM2B_ATTEST *quoted,
    TPMT_SIGNATURE *signature,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_GetSessionAuditDigest_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_RH_ENDORSEMENT privacyAdminHandle,
    TPMI_DH_OBJECT signHandle,
    TPMI_SH_HMAC sessionHandle,
    const TPM2B_DATA *qualifyingData,
    const TPMT_SIG_SCHEME *inScheme);

TSS2_RC Tss2_Sys_GetSessionAuditDigest_Complete(
    TSS2_SYS_CONTEXT *sysContext,
    TPM2B_ATTEST *auditInfo,
    TPMT_SIGNATURE *signature);

TSS2_RC Tss2_Sys_GetSessionAuditDigest(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_RH_ENDORSEMENT privacyAdminHandle,
    TPMI_DH_OBJECT signHandle,
    TPMI_SH_HMAC sessionHandle,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    const TPM2B_DATA *qualifyingData,
    const TPMT_SIG_SCHEME *inScheme,
    TPM2B_ATTEST *auditInfo,
    TPMT_SIGNATURE *signature,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_GetCommandAuditDigest_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_RH_ENDORSEMENT privacyHandle,
    TPMI_DH_OBJECT signHandle,
    const TPM2B_DATA *qualifyingData,
    const TPMT_SIG_SCHEME *inScheme);

TSS2_RC Tss2_Sys_GetCommandAuditDigest_Complete(
    TSS2_SYS_CONTEXT *sysContext,
    TPM2B_ATTEST *auditInfo,
    TPMT_SIGNATURE *signature);

TSS2_RC Tss2_Sys_GetCommandAuditDigest(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_RH_ENDORSEMENT privacyHandle,
    TPMI_DH_OBJECT signHandle,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    const TPM2B_DATA *qualifyingData,
    const TPMT_SIG_SCHEME *inScheme,
    TPM2B_ATTEST *auditInfo,
    TPMT_SIGNATURE *signature,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_GetTime_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_RH_ENDORSEMENT privacyAdminHandle,
    TPMI_DH_OBJECT signHandle,
    const TPM2B_DATA *qualifyingData,
    const TPMT_SIG_SCHEME *inScheme);

TSS2_RC Tss2_Sys_GetTime_Complete(
    TSS2_SYS_CONTEXT *sysContext,
    TPM2B_ATTEST *timeInfo,
    TPMT_SIGNATURE *signature);

TSS2_RC Tss2_Sys_GetTime(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_RH_ENDORSEMENT privacyAdminHandle,
    TPMI_DH_OBJECT signHandle,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    const TPM2B_DATA *qualifyingData,
    const TPMT_SIG_SCHEME *inScheme,
    TPM2B_ATTEST *timeInfo,
    TPMT_SIGNATURE *signature,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_Commit_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_DH_OBJECT signHandle,
    const TPM2B_ECC_POINT *P1,
    const TPM2B_SENSITIVE_DATA *s2,
    const TPM2B_ECC_PARAMETER *y2);

TSS2_RC Tss2_Sys_Commit_Complete(
    TSS2_SYS_CONTEXT *sysContext,
    TPM2B_ECC_POINT *K,
    TPM2B_ECC_POINT *L,
    TPM2B_ECC_POINT *E,
    UINT16 *counter);

TSS2_RC Tss2_Sys_Commit(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_DH_OBJECT signHandle,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    const TPM2B_ECC_POINT *P1,
    const TPM2B_SENSITIVE_DATA *s2,
    const TPM2B_ECC_PARAMETER *y2,
    TPM2B_ECC_POINT *K,
    TPM2B_ECC_POINT *L,
    TPM2B_ECC_POINT *E,
    UINT16 *counter,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_EC_Ephemeral_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_ECC_CURVE curveID);

TSS2_RC Tss2_Sys_EC_Ephemeral_Complete(
    TSS2_SYS_CONTEXT *sysContext,
    TPM2B_ECC_POINT *Q,
    UINT16 *counter);

TSS2_RC Tss2_Sys_EC_Ephemeral(
    TSS2_SYS_CONTEXT *sysContext,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    TPMI_ECC_CURVE curveID,
    TPM2B_ECC_POINT *Q,
    UINT16 *counter,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_VerifySignature_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_DH_OBJECT keyHandle,
    const TPM2B_DIGEST *digest,
    const TPMT_SIGNATURE *signature);

TSS2_RC Tss2_Sys_VerifySignature_Complete(
    TSS2_SYS_CONTEXT *sysContext,
    TPMT_TK_VERIFIED *validation);

TSS2_RC Tss2_Sys_VerifySignature(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_DH_OBJECT keyHandle,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    const TPM2B_DIGEST *digest,
    const TPMT_SIGNATURE *signature,
    TPMT_TK_VERIFIED *validation,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_Sign_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_DH_OBJECT keyHandle,
    const TPM2B_DIGEST *digest,
    const TPMT_SIG_SCHEME *inScheme,
    const TPMT_TK_HASHCHECK *validation);

TSS2_RC Tss2_Sys_Sign_Complete(
    TSS2_SYS_CONTEXT *sysContext,
    TPMT_SIGNATURE *signature);

TSS2_RC Tss2_Sys_Sign(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_DH_OBJECT keyHandle,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    const TPM2B_DIGEST *digest,
    const TPMT_SIG_SCHEME *inScheme,
    const TPMT_TK_HASHCHECK *validation,
    TPMT_SIGNATURE *signature,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_SetCommandCodeAuditStatus_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_RH_PROVISION auth,
    TPMI_ALG_HASH auditAlg,
    const TPML_CC *setList,
    const TPML_CC *clearList);

TSS2_RC Tss2_Sys_SetCommandCodeAuditStatus_Complete(
    TSS2_SYS_CONTEXT *sysContext);

TSS2_RC Tss2_Sys_SetCommandCodeAuditStatus(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_RH_PROVISION auth,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    TPMI_ALG_HASH auditAlg,
    const TPML_CC *setList,
    const TPML_CC *clearList,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_PCR_Extend_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_DH_PCR pcrHandle,
    const TPML_DIGEST_VALUES *digests);

TSS2_RC Tss2_Sys_PCR_Extend_Complete(
    TSS2_SYS_CONTEXT *sysContext);

TSS2_RC Tss2_Sys_PCR_Extend(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_DH_PCR pcrHandle,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    const TPML_DIGEST_VALUES *digests,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_PCR_Event_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_DH_PCR pcrHandle,
    const TPM2B_EVENT *eventData);

TSS2_RC Tss2_Sys_PCR_Event_Complete(
    TSS2_SYS_CONTEXT *sysContext,
    TPML_DIGEST_VALUES *digests);

TSS2_RC Tss2_Sys_PCR_Event(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_DH_PCR pcrHandle,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    const TPM2B_EVENT *eventData,
    TPML_DIGEST_VALUES *digests,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_PCR_Read_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    const TPML_PCR_SELECTION *pcrSelectionIn);

TSS2_RC Tss2_Sys_PCR_Read_Complete(
    TSS2_SYS_CONTEXT *sysContext,
    UINT32 *pcrUpdateCounter,
    TPML_PCR_SELECTION *pcrSelectionOut,
    TPML_DIGEST *pcrValues);

TSS2_RC Tss2_Sys_PCR_Read(
    TSS2_SYS_CONTEXT *sysContext,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    const TPML_PCR_SELECTION *pcrSelectionIn,
    UINT32 *pcrUpdateCounter,
    TPML_PCR_SELECTION *pcrSelectionOut,
    TPML_DIGEST *pcrValues,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_PCR_Allocate_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_RH_PLATFORM authHandle,
    const TPML_PCR_SELECTION *pcrAllocation);

TSS2_RC Tss2_Sys_PCR_Allocate_Complete(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_YES_NO *allocationSuccess,
    UINT32 *maxPCR,
    UINT32 *sizeNeeded,
    UINT32 *sizeAvailable);

TSS2_RC Tss2_Sys_PCR_Allocate(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_RH_PLATFORM authHandle,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    const TPML_PCR_SELECTION *pcrAllocation,
    TPMI_YES_NO *allocationSuccess,
    UINT32 *maxPCR,
    UINT32 *sizeNeeded,
    UINT32 *sizeAvailable,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_PCR_SetAuthPolicy_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_RH_PLATFORM authHandle,
    const TPM2B_DIGEST *authPolicy,
    TPMI_ALG_HASH hashAlg,
    TPMI_DH_PCR pcrNum);

TSS2_RC Tss2_Sys_PCR_SetAuthPolicy_Complete(
    TSS2_SYS_CONTEXT *sysContext);

TSS2_RC Tss2_Sys_PCR_SetAuthPolicy(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_RH_PLATFORM authHandle,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    const TPM2B_DIGEST *authPolicy,
    TPMI_ALG_HASH hashAlg,
    TPMI_DH_PCR pcrNum,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_PCR_SetAuthValue_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_DH_PCR pcrHandle,
    const TPM2B_DIGEST *auth);

TSS2_RC Tss2_Sys_PCR_SetAuthValue_Complete(
    TSS2_SYS_CONTEXT *sysContext);

TSS2_RC Tss2_Sys_PCR_SetAuthValue(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_DH_PCR pcrHandle,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    const TPM2B_DIGEST *auth,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_PCR_Reset_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_DH_PCR pcrHandle);

TSS2_RC Tss2_Sys_PCR_Reset_Complete(
    TSS2_SYS_CONTEXT *sysContext);

TSS2_RC Tss2_Sys_PCR_Reset(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_DH_PCR pcrHandle,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_PolicySigned_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_DH_OBJECT authObject,
    TPMI_SH_POLICY policySession,
    const TPM2B_NONCE *nonceTPM,
    const TPM2B_DIGEST *cpHashA,
    const TPM2B_NONCE *policyRef,
    INT32 expiration,
    const TPMT_SIGNATURE *auth);

TSS2_RC Tss2_Sys_PolicySigned_Complete(
    TSS2_SYS_CONTEXT *sysContext,
    TPM2B_TIMEOUT *timeout,
    TPMT_TK_AUTH *policyTicket);

TSS2_RC Tss2_Sys_PolicySigned(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_DH_OBJECT authObject,
    TPMI_SH_POLICY policySession,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    const TPM2B_NONCE *nonceTPM,
    const TPM2B_DIGEST *cpHashA,
    const TPM2B_NONCE *policyRef,
    INT32 expiration,
    const TPMT_SIGNATURE *auth,
    TPM2B_TIMEOUT *timeout,
    TPMT_TK_AUTH *policyTicket,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_PolicySecret_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_DH_ENTITY authHandle,
    TPMI_SH_POLICY policySession,
    const TPM2B_NONCE *nonceTPM,
    const TPM2B_DIGEST *cpHashA,
    const TPM2B_NONCE *policyRef,
    INT32 expiration);

TSS2_RC Tss2_Sys_PolicySecret_Complete(
    TSS2_SYS_CONTEXT *sysContext,
    TPM2B_TIMEOUT *timeout,
    TPMT_TK_AUTH *policyTicket);

TSS2_RC Tss2_Sys_PolicySecret(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_DH_ENTITY authHandle,
    TPMI_SH_POLICY policySession,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    const TPM2B_NONCE *nonceTPM,
    const TPM2B_DIGEST *cpHashA,
    const TPM2B_NONCE *policyRef,
    INT32 expiration,
    TPM2B_TIMEOUT *timeout,
    TPMT_TK_AUTH *policyTicket,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_PolicyTicket_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_SH_POLICY policySession,
    const TPM2B_TIMEOUT *timeout,
    const TPM2B_DIGEST *cpHashA,
    const TPM2B_NONCE *policyRef,
    const TPM2B_NAME *authName,
    const TPMT_TK_AUTH *ticket);

TSS2_RC Tss2_Sys_PolicyTicket_Complete(
    TSS2_SYS_CONTEXT *sysContext);

TSS2_RC Tss2_Sys_PolicyTicket(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_SH_POLICY policySession,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    const TPM2B_TIMEOUT *timeout,
    const TPM2B_DIGEST *cpHashA,
    const TPM2B_NONCE *policyRef,
    const TPM2B_NAME *authName,
    const TPMT_TK_AUTH *ticket,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_PolicyOR_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_SH_POLICY policySession,
    const TPML_DIGEST *pHashList);

TSS2_RC Tss2_Sys_PolicyOR_Complete(
    TSS2_SYS_CONTEXT *sysContext);

TSS2_RC Tss2_Sys_PolicyOR(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_SH_POLICY policySession,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    const TPML_DIGEST *pHashList,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_PolicyPCR_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_SH_POLICY policySession,
    const TPM2B_DIGEST *pcrDigest,
    const TPML_PCR_SELECTION *pcrs);

TSS2_RC Tss2_Sys_PolicyPCR_Complete(
    TSS2_SYS_CONTEXT *sysContext);

TSS2_RC Tss2_Sys_PolicyPCR(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_SH_POLICY policySession,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    const TPM2B_DIGEST *pcrDigest,
    const TPML_PCR_SELECTION *pcrs,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_PolicyLocality_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_SH_POLICY policySession,
    TPMA_LOCALITY locality);

TSS2_RC Tss2_Sys_PolicyLocality_Complete(
    TSS2_SYS_CONTEXT *sysContext);

TSS2_RC Tss2_Sys_PolicyLocality(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_SH_POLICY policySession,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    TPMA_LOCALITY locality,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_PolicyNV_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_RH_NV_AUTH authHandle,
    TPMI_RH_NV_INDEX nvIndex,
    TPMI_SH_POLICY policySession,
    const TPM2B_OPERAND *operandB,
    UINT16 offset,
    TPM2_EO operation);

TSS2_RC Tss2_Sys_PolicyNV_Complete(
    TSS2_SYS_CONTEXT *sysContext);

TSS2_RC Tss2_Sys_PolicyNV(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_RH_NV_AUTH authHandle,
    TPMI_RH_NV_INDEX nvIndex,
    TPMI_SH_POLICY policySession,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    const TPM2B_OPERAND *operandB,
    UINT16 offset,
    TPM2_EO operation,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_PolicyCounterTimer_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_SH_POLICY policySession,
    const TPM2B_OPERAND *operandB,
    UINT16 offset,
    TPM2_EO operation);

TSS2_RC Tss2_Sys_PolicyCounterTimer_Complete(
    TSS2_SYS_CONTEXT *sysContext);

TSS2_RC Tss2_Sys_PolicyCounterTimer(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_SH_POLICY policySession,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    const TPM2B_OPERAND *operandB,
    UINT16 offset,
    TPM2_EO operation,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_PolicyCommandCode_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_SH_POLICY policySession,
    TPM2_CC code);

TSS2_RC Tss2_Sys_PolicyCommandCode_Complete(
    TSS2_SYS_CONTEXT *sysContext);

TSS2_RC Tss2_Sys_PolicyCommandCode(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_SH_POLICY policySession,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    TPM2_CC code,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_PolicyPhysicalPresence_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_SH_POLICY policySession);

TSS2_RC Tss2_Sys_PolicyPhysicalPresence_Complete(
    TSS2_SYS_CONTEXT *sysContext);

TSS2_RC Tss2_Sys_PolicyPhysicalPresence(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_SH_POLICY policySession,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_PolicyCpHash_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_SH_POLICY policySession,
    const TPM2B_DIGEST *cpHashA);

TSS2_RC Tss2_Sys_PolicyCpHash_Complete(
    TSS2_SYS_CONTEXT *sysContext);

TSS2_RC Tss2_Sys_PolicyCpHash(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_SH_POLICY policySession,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    const TPM2B_DIGEST *cpHashA,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_PolicyNameHash_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_SH_POLICY policySession,
    const TPM2B_DIGEST *nameHash);

TSS2_RC Tss2_Sys_PolicyNameHash_Complete(
    TSS2_SYS_CONTEXT *sysContext);

TSS2_RC Tss2_Sys_PolicyNameHash(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_SH_POLICY policySession,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    const TPM2B_DIGEST *nameHash,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_PolicyDuplicationSelect_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_SH_POLICY policySession,
    const TPM2B_NAME *objectName,
    const TPM2B_NAME *newParentName,
    TPMI_YES_NO includeObject);

TSS2_RC Tss2_Sys_PolicyDuplicationSelect_Complete(
    TSS2_SYS_CONTEXT *sysContext);

TSS2_RC Tss2_Sys_PolicyDuplicationSelect(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_SH_POLICY policySession,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    const TPM2B_NAME *objectName,
    const TPM2B_NAME *newParentName,
    TPMI_YES_NO includeObject,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_PolicyAuthorize_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_SH_POLICY policySession,
    const TPM2B_DIGEST *approvedPolicy,
    const TPM2B_NONCE *policyRef,
    const TPM2B_NAME *keySign,
    const TPMT_TK_VERIFIED *checkTicket);

TSS2_RC Tss2_Sys_PolicyAuthorize_Complete(
    TSS2_SYS_CONTEXT *sysContext);

TSS2_RC Tss2_Sys_PolicyAuthorize(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_SH_POLICY policySession,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    const TPM2B_DIGEST *approvedPolicy,
    const TPM2B_NONCE *policyRef,
    const TPM2B_NAME *keySign,
    const TPMT_TK_VERIFIED *checkTicket,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_PolicyAuthValue_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_SH_POLICY policySession);

TSS2_RC Tss2_Sys_PolicyAuthValue_Complete(
    TSS2_SYS_CONTEXT *sysContext);

TSS2_RC Tss2_Sys_PolicyAuthValue(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_SH_POLICY policySession,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_PolicyPassword_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_SH_POLICY policySession);

TSS2_RC Tss2_Sys_PolicyPassword_Complete(
    TSS2_SYS_CONTEXT *sysContext);

TSS2_RC Tss2_Sys_PolicyPassword(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_SH_POLICY policySession,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_PolicyGetDigest_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_SH_POLICY policySession);

TSS2_RC Tss2_Sys_PolicyGetDigest_Complete(
    TSS2_SYS_CONTEXT *sysContext,
    TPM2B_DIGEST *policyDigest);

TSS2_RC Tss2_Sys_PolicyGetDigest(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_SH_POLICY policySession,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    TPM2B_DIGEST *policyDigest,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_PolicyNvWritten_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_SH_POLICY policySession,
    TPMI_YES_NO writtenSet);

TSS2_RC Tss2_Sys_PolicyNvWritten_Complete(
    TSS2_SYS_CONTEXT *sysContext);

TSS2_RC Tss2_Sys_PolicyNvWritten(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_SH_POLICY policySession,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    TPMI_YES_NO writtenSet,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_CreatePrimary_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_RH_HIERARCHY primaryHandle,
    const TPM2B_SENSITIVE_CREATE *inSensitive,
    const TPM2B_PUBLIC *inPublic,
    const TPM2B_DATA *outsideInfo,
    const TPML_PCR_SELECTION *creationPCR);

TSS2_RC Tss2_Sys_CreatePrimary_Complete(
    TSS2_SYS_CONTEXT *sysContext,
    TPM2_HANDLE *objectHandle,
    TPM2B_PUBLIC *outPublic,
    TPM2B_CREATION_DATA *creationData,
    TPM2B_DIGEST *creationHash,
    TPMT_TK_CREATION *creationTicket,
    TPM2B_NAME *name);

TSS2_RC Tss2_Sys_CreatePrimary(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_RH_HIERARCHY primaryHandle,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    const TPM2B_SENSITIVE_CREATE *inSensitive,
    const TPM2B_PUBLIC *inPublic,
    const TPM2B_DATA *outsideInfo,
    const TPML_PCR_SELECTION *creationPCR,
    TPM2_HANDLE *objectHandle,
    TPM2B_PUBLIC *outPublic,
    TPM2B_CREATION_DATA *creationData,
    TPM2B_DIGEST *creationHash,
    TPMT_TK_CREATION *creationTicket,
    TPM2B_NAME *name,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_HierarchyControl_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_RH_HIERARCHY authHandle,
    TPMI_RH_ENABLES enable,
    TPMI_YES_NO state);

TSS2_RC Tss2_Sys_HierarchyControl_Complete(
    TSS2_SYS_CONTEXT *sysContext);

TSS2_RC Tss2_Sys_HierarchyControl(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_RH_HIERARCHY authHandle,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    TPMI_RH_ENABLES enable,
    TPMI_YES_NO state,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_SetPrimaryPolicy_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_RH_HIERARCHY_AUTH authHandle,
    const TPM2B_DIGEST *authPolicy,
    TPMI_ALG_HASH hashAlg);

TSS2_RC Tss2_Sys_SetPrimaryPolicy_Complete(
    TSS2_SYS_CONTEXT *sysContext);

TSS2_RC Tss2_Sys_SetPrimaryPolicy(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_RH_HIERARCHY_AUTH authHandle,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    const TPM2B_DIGEST *authPolicy,
    TPMI_ALG_HASH hashAlg,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_ChangePPS_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_RH_PLATFORM authHandle);

TSS2_RC Tss2_Sys_ChangePPS_Complete(
    TSS2_SYS_CONTEXT *sysContext);

TSS2_RC Tss2_Sys_ChangePPS(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_RH_PLATFORM authHandle,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_ChangeEPS_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_RH_PLATFORM authHandle);

TSS2_RC Tss2_Sys_ChangeEPS_Complete(
    TSS2_SYS_CONTEXT *sysContext);

TSS2_RC Tss2_Sys_ChangeEPS(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_RH_PLATFORM authHandle,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_Clear_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_RH_CLEAR authHandle);

TSS2_RC Tss2_Sys_Clear_Complete(
    TSS2_SYS_CONTEXT *sysContext);

TSS2_RC Tss2_Sys_Clear(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_RH_CLEAR authHandle,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_ClearControl_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_RH_CLEAR auth,
    TPMI_YES_NO disable);

TSS2_RC Tss2_Sys_ClearControl_Complete(
    TSS2_SYS_CONTEXT *sysContext);

TSS2_RC Tss2_Sys_ClearControl(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_RH_CLEAR auth,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    TPMI_YES_NO disable,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_HierarchyChangeAuth_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_RH_HIERARCHY_AUTH authHandle,
    const TPM2B_AUTH *newAuth);

TSS2_RC Tss2_Sys_HierarchyChangeAuth_Complete(
    TSS2_SYS_CONTEXT *sysContext);

TSS2_RC Tss2_Sys_HierarchyChangeAuth(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_RH_HIERARCHY_AUTH authHandle,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    const TPM2B_AUTH *newAuth,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_DictionaryAttackLockReset_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_RH_LOCKOUT lockHandle);

TSS2_RC Tss2_Sys_DictionaryAttackLockReset_Complete(
    TSS2_SYS_CONTEXT *sysContext);

TSS2_RC Tss2_Sys_DictionaryAttackLockReset(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_RH_LOCKOUT lockHandle,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_DictionaryAttackParameters_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_RH_LOCKOUT lockHandle,
    UINT32 newMaxTries,
    UINT32 newRecoveryTime,
    UINT32 lockoutRecovery);

TSS2_RC Tss2_Sys_DictionaryAttackParameters_Complete(
    TSS2_SYS_CONTEXT *sysContext);

TSS2_RC Tss2_Sys_DictionaryAttackParameters(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_RH_LOCKOUT lockHandle,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    UINT32 newMaxTries,
    UINT32 newRecoveryTime,
    UINT32 lockoutRecovery,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_PP_Commands_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_RH_PLATFORM auth,
    const TPML_CC *setList,
    const TPML_CC *clearList);

TSS2_RC Tss2_Sys_PP_Commands_Complete(
    TSS2_SYS_CONTEXT *sysContext);

TSS2_RC Tss2_Sys_PP_Commands(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_RH_PLATFORM auth,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    const TPML_CC *setList,
    const TPML_CC *clearList,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_SetAlgorithmSet_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_RH_PLATFORM authHandle,
    UINT32 algorithmSet);

TSS2_RC Tss2_Sys_SetAlgorithmSet_Complete(
    TSS2_SYS_CONTEXT *sysContext);

TSS2_RC Tss2_Sys_SetAlgorithmSet(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_RH_PLATFORM authHandle,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    UINT32 algorithmSet,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_FieldUpgradeStart_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_RH_PLATFORM authorization,
    TPMI_DH_OBJECT keyHandle,
    TPM2B_DIGEST const *fuDigest,
    TPMT_SIGNATURE const *manifestSignature);

TSS2_RC Tss2_Sys_FieldUpgradeStart_Complete(
    TSS2_SYS_CONTEXT *sysContext);

TSS2_RC Tss2_Sys_FieldUpgradeStart(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_RH_PLATFORM authorization,
    TPMI_DH_OBJECT keyHandle,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    TPM2B_DIGEST const *fuDigest,
    TPMT_SIGNATURE const *manifestSignature,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_FieldUpgradeData_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPM2B_MAX_BUFFER const *fuData);

TSS2_RC Tss2_Sys_FieldUpgradeData_Complete(
    TSS2_SYS_CONTEXT *sysContext,
    TPMT_HA *nextDigest,
    TPMT_HA *firstDigest);

TSS2_RC Tss2_Sys_FieldUpgradeData(
    TSS2_SYS_CONTEXT *sysContext,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    TPM2B_MAX_BUFFER const *fuData,
    TPMT_HA *nextDigest,
    TPMT_HA *firstDigest,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_FirmwareRead_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    UINT32 sequenceNumber);

TSS2_RC Tss2_Sys_FirmwareRead_Complete(
    TSS2_SYS_CONTEXT *sysContext,
    TPM2B_MAX_BUFFER *fuData);

TSS2_RC Tss2_Sys_FirmwareRead(
    TSS2_SYS_CONTEXT *sysContext,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    UINT32 sequenceNumber,
    TPM2B_MAX_BUFFER *fuData,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_ContextSave_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_DH_CONTEXT saveHandle);

TSS2_RC Tss2_Sys_ContextSave_Complete(
    TSS2_SYS_CONTEXT *sysContext,
    TPMS_CONTEXT *context);

TSS2_RC Tss2_Sys_ContextSave(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_DH_CONTEXT saveHandle,
    TPMS_CONTEXT *context);

TSS2_RC Tss2_Sys_ContextLoad_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    const TPMS_CONTEXT *context);

TSS2_RC Tss2_Sys_ContextLoad_Complete(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_DH_CONTEXT *loadedHandle);

TSS2_RC Tss2_Sys_ContextLoad(
    TSS2_SYS_CONTEXT *sysContext,
    const TPMS_CONTEXT *context,
    TPMI_DH_CONTEXT *loadedHandle);

TSS2_RC Tss2_Sys_FlushContext_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_DH_CONTEXT flushHandle);

TSS2_RC Tss2_Sys_FlushContext_Complete(
    TSS2_SYS_CONTEXT *sysContext);

TSS2_RC Tss2_Sys_FlushContext(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_DH_CONTEXT flushHandle);

TSS2_RC Tss2_Sys_EvictControl_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_RH_PROVISION auth,
    TPMI_DH_OBJECT objectHandle,
    TPMI_DH_PERSISTENT persistentHandle);

TSS2_RC Tss2_Sys_EvictControl_Complete(
    TSS2_SYS_CONTEXT *sysContext);

TSS2_RC Tss2_Sys_EvictControl(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_RH_PROVISION auth,
    TPMI_DH_OBJECT objectHandle,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    TPMI_DH_PERSISTENT persistentHandle,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_ReadClock_Prepare(
    TSS2_SYS_CONTEXT *sysContext);

TSS2_RC Tss2_Sys_ReadClock_Complete(
    TSS2_SYS_CONTEXT *sysContext,
    TPMS_TIME_INFO *currentTime);

TSS2_RC Tss2_Sys_ReadClock(
    TSS2_SYS_CONTEXT *sysContext,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    TPMS_TIME_INFO *currentTime,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_ClockSet_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_RH_PROVISION auth,
    UINT64 newTime);

TSS2_RC Tss2_Sys_ClockSet_Complete(
    TSS2_SYS_CONTEXT *sysContext);

TSS2_RC Tss2_Sys_ClockSet(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_RH_PROVISION auth,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    UINT64 newTime,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_ClockRateAdjust_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_RH_PROVISION auth,
    TPM2_CLOCK_ADJUST rateAdjust);

TSS2_RC Tss2_Sys_ClockRateAdjust_Complete(
    TSS2_SYS_CONTEXT *sysContext);

TSS2_RC Tss2_Sys_ClockRateAdjust(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_RH_PROVISION auth,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    TPM2_CLOCK_ADJUST rateAdjust,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_GetCapability_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPM2_CAP capability,
    UINT32 property,
    UINT32 propertyCount);

TSS2_RC Tss2_Sys_GetCapability_Complete(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_YES_NO *moreData,
    TPMS_CAPABILITY_DATA *capabilityData);

TSS2_RC Tss2_Sys_GetCapability(
    TSS2_SYS_CONTEXT *sysContext,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    TPM2_CAP capability,
    UINT32 property,
    UINT32 propertyCount,
    TPMI_YES_NO *moreData,
    TPMS_CAPABILITY_DATA *capabilityData,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_TestParms_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    const TPMT_PUBLIC_PARMS *parameters);

TSS2_RC Tss2_Sys_TestParms_Complete(
    TSS2_SYS_CONTEXT *sysContext);

TSS2_RC Tss2_Sys_TestParms(
    TSS2_SYS_CONTEXT *sysContext,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    const TPMT_PUBLIC_PARMS *parameters,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_NV_DefineSpace_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_RH_PROVISION authHandle,
    const TPM2B_AUTH *auth,
    const TPM2B_NV_PUBLIC *publicInfo);

TSS2_RC Tss2_Sys_NV_DefineSpace_Complete(
    TSS2_SYS_CONTEXT *sysContext);

TSS2_RC Tss2_Sys_NV_DefineSpace(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_RH_PROVISION authHandle,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    const TPM2B_AUTH *auth,
    const TPM2B_NV_PUBLIC *publicInfo,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_NV_UndefineSpace_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_RH_PROVISION authHandle,
    TPMI_RH_NV_INDEX nvIndex);

TSS2_RC Tss2_Sys_NV_UndefineSpace_Complete(
    TSS2_SYS_CONTEXT *sysContext);

TSS2_RC Tss2_Sys_NV_UndefineSpace(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_RH_PROVISION authHandle,
    TPMI_RH_NV_INDEX nvIndex,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_NV_UndefineSpaceSpecial_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_RH_NV_INDEX nvIndex,
    TPMI_RH_PLATFORM platform);

TSS2_RC Tss2_Sys_NV_UndefineSpaceSpecial_Complete(
    TSS2_SYS_CONTEXT *sysContext);

TSS2_RC Tss2_Sys_NV_UndefineSpaceSpecial(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_RH_NV_INDEX nvIndex,
    TPMI_RH_PLATFORM platform,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_NV_ReadPublic_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_RH_NV_INDEX nvIndex);

TSS2_RC Tss2_Sys_NV_ReadPublic_Complete(
    TSS2_SYS_CONTEXT *sysContext,
    TPM2B_NV_PUBLIC *nvPublic,
    TPM2B_NAME *nvName);

TSS2_RC Tss2_Sys_NV_ReadPublic(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_RH_NV_INDEX nvIndex,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    TPM2B_NV_PUBLIC *nvPublic,
    TPM2B_NAME *nvName,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_NV_Write_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_RH_NV_AUTH authHandle,
    TPMI_RH_NV_INDEX nvIndex,
    const TPM2B_MAX_NV_BUFFER *data,
    UINT16 offset);

TSS2_RC Tss2_Sys_NV_Write_Complete(
    TSS2_SYS_CONTEXT *sysContext);

TSS2_RC Tss2_Sys_NV_Write(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_RH_NV_AUTH authHandle,
    TPMI_RH_NV_INDEX nvIndex,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    const TPM2B_MAX_NV_BUFFER *data,
    UINT16 offset,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_NV_Increment_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_RH_NV_AUTH authHandle,
    TPMI_RH_NV_INDEX nvIndex);

TSS2_RC Tss2_Sys_NV_Increment_Complete(
    TSS2_SYS_CONTEXT *sysContext);

TSS2_RC Tss2_Sys_NV_Increment(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_RH_NV_AUTH authHandle,
    TPMI_RH_NV_INDEX nvIndex,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_NV_Extend_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_RH_NV_AUTH authHandle,
    TPMI_RH_NV_INDEX nvIndex,
    const TPM2B_MAX_NV_BUFFER *data);

TSS2_RC Tss2_Sys_NV_Extend_Complete(
    TSS2_SYS_CONTEXT *sysContext);

TSS2_RC Tss2_Sys_NV_Extend(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_RH_NV_AUTH authHandle,
    TPMI_RH_NV_INDEX nvIndex,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    const TPM2B_MAX_NV_BUFFER *data,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_NV_SetBits_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_RH_NV_AUTH authHandle,
    TPMI_RH_NV_INDEX nvIndex,
    UINT64 bits);

TSS2_RC Tss2_Sys_NV_SetBits_Complete(
    TSS2_SYS_CONTEXT *sysContext);

TSS2_RC Tss2_Sys_NV_SetBits(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_RH_NV_AUTH authHandle,
    TPMI_RH_NV_INDEX nvIndex,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    UINT64 bits,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_NV_WriteLock_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_RH_NV_AUTH authHandle,
    TPMI_RH_NV_INDEX nvIndex);

TSS2_RC Tss2_Sys_NV_WriteLock_Complete(
    TSS2_SYS_CONTEXT *sysContext);

TSS2_RC Tss2_Sys_NV_WriteLock(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_RH_NV_AUTH authHandle,
    TPMI_RH_NV_INDEX nvIndex,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_NV_GlobalWriteLock_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_RH_PROVISION authHandle);

TSS2_RC Tss2_Sys_NV_GlobalWriteLock_Complete(
    TSS2_SYS_CONTEXT *sysContext);

TSS2_RC Tss2_Sys_NV_GlobalWriteLock(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_RH_PROVISION authHandle,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_NV_Read_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_RH_NV_AUTH authHandle,
    TPMI_RH_NV_INDEX nvIndex,
    UINT16 size,
    UINT16 offset);

TSS2_RC Tss2_Sys_NV_Read_Complete(
    TSS2_SYS_CONTEXT *sysContext,
    TPM2B_MAX_NV_BUFFER *data);

TSS2_RC Tss2_Sys_NV_Read(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_RH_NV_AUTH authHandle,
    TPMI_RH_NV_INDEX nvIndex,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    UINT16 size,
    UINT16 offset,
    TPM2B_MAX_NV_BUFFER *data,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_NV_ReadLock_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_RH_NV_AUTH authHandle,
    TPMI_RH_NV_INDEX nvIndex);

TSS2_RC Tss2_Sys_NV_ReadLock_Complete(
    TSS2_SYS_CONTEXT *sysContext);

TSS2_RC Tss2_Sys_NV_ReadLock(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_RH_NV_AUTH authHandle,
    TPMI_RH_NV_INDEX nvIndex,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_NV_ChangeAuth_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_RH_NV_INDEX nvIndex,
    const TPM2B_AUTH *newAuth);

TSS2_RC Tss2_Sys_NV_ChangeAuth_Complete(
    TSS2_SYS_CONTEXT *sysContext);

TSS2_RC Tss2_Sys_NV_ChangeAuth(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_RH_NV_INDEX nvIndex,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    const TPM2B_AUTH *newAuth,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_NV_Certify_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_DH_OBJECT signHandle,
    TPMI_RH_NV_AUTH authHandle,
    TPMI_RH_NV_INDEX nvIndex,
    const TPM2B_DATA *qualifyingData,
    const TPMT_SIG_SCHEME *inScheme,
    UINT16 size,
    UINT16 offset);

TSS2_RC Tss2_Sys_NV_Certify_Complete(
    TSS2_SYS_CONTEXT *sysContext,
    TPM2B_ATTEST *certifyInfo,
    TPMT_SIGNATURE *signature);

TSS2_RC Tss2_Sys_NV_Certify(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_DH_OBJECT signHandle,
    TPMI_RH_NV_AUTH authHandle,
    TPMI_RH_NV_INDEX nvIndex,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    const TPM2B_DATA *qualifyingData,
    const TPMT_SIG_SCHEME *inScheme,
    UINT16 size,
    UINT16 offset,
    TPM2B_ATTEST *certifyInfo,
    TPMT_SIGNATURE *signature,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_Vendor_TCG_Test_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    const TPM2B_DATA *inputData);

TSS2_RC Tss2_Sys_Vendor_TCG_Test_Complete(
    TSS2_SYS_CONTEXT *sysContext,
    TPM2B_DATA *outputData);

TSS2_RC Tss2_Sys_Vendor_TCG_Test(
    TSS2_SYS_CONTEXT *sysContext,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    const TPM2B_DATA *inputData,
    TPM2B_DATA *outputData,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_AC_GetCapability_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_RH_AC ac,
    TPM_AT capability,
    UINT32 count);

TSS2_RC Tss2_Sys_AC_GetCapability_Complete(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_YES_NO *moreData,
    TPML_AC_CAPABILITIES *capabilityData);

TSS2_RC Tss2_Sys_AC_GetCapability(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_RH_AC ac,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    TPM_AT capability,
    UINT32 count,
    TPMI_YES_NO *moreData,
    TPML_AC_CAPABILITIES *capabilityData,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_AC_Send_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_DH_OBJECT sendObject,
    TPMI_RH_NV_AUTH authHandle,
    TPMI_RH_AC ac,
    TPM2B_MAX_BUFFER *acDataIn);

TSS2_RC Tss2_Sys_AC_Send_Complete(
    TSS2_SYS_CONTEXT *sysContext,
    TPMS_AC_OUTPUT *acDataOut);

TSS2_RC Tss2_Sys_AC_Send(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_DH_OBJECT sendObject,
    TPMI_RH_NV_AUTH authHandle,
    TPMI_RH_AC ac,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    TPM2B_MAX_BUFFER *acDataIn,
    TPMS_AC_OUTPUT *acDataOut,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_Policy_AC_SendSelect_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_SH_POLICY policySession,
    TPM2B_NAME *objectName,
    TPM2B_NAME *authHandleName,
    TPM2B_NAME *acName,
    TPMI_YES_NO includeObject);

TSS2_RC Tss2_Sys_Policy_AC_SendSelect_Complete(
    TSS2_SYS_CONTEXT *sysContext);

TSS2_RC Tss2_Sys_Policy_AC_SendSelect(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_SH_POLICY policySession,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    TPM2B_NAME *objectName,
    TPM2B_NAME *authHandleName,
    TPM2B_NAME *acName,
    TPMI_YES_NO includeObject,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_ACT_SetTimeout_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_RH_ACT actHandle,
    UINT32 startTimeout);

TSS2_RC Tss2_Sys_ACT_SetTimeout_Complete(
    TSS2_SYS_CONTEXT *sysContext);

TSS2_RC Tss2_Sys_ACT_SetTimeout(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_RH_ACT actHandle,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    UINT32 startTimeout,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_PolicyTemplate_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_SH_POLICY policySession,
    const TPM2B_DIGEST *templateHash);

TSS2_RC Tss2_Sys_PolicyTemplate_Complete(
    TSS2_SYS_CONTEXT *sysContext);

TSS2_RC Tss2_Sys_PolicyTemplate(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_SH_POLICY policySession,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    const TPM2B_DIGEST *templateHash,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_CreateLoaded_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_RH_HIERARCHY parentHandle,
    const TPM2B_SENSITIVE_CREATE *inSensitive,
    const TPM2B_TEMPLATE *inPublic);

TSS2_RC Tss2_Sys_CreateLoaded_Complete(
    TSS2_SYS_CONTEXT *sysContext,
    TPM2_HANDLE *objectHandle,
    TPM2B_PRIVATE *outPrivate,
    TPM2B_PUBLIC *outPublic,
    TPM2B_NAME *name);

TSS2_RC Tss2_Sys_CreateLoaded(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_RH_HIERARCHY parentHandle,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    const TPM2B_SENSITIVE_CREATE *inSensitive,
    const TPM2B_TEMPLATE *inPublic,
    TPM2_HANDLE *objectHandle,
    TPM2B_PRIVATE *outPrivate,
    TPM2B_PUBLIC *outPublic,
    TPM2B_NAME *name,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

TSS2_RC Tss2_Sys_PolicyAuthorizeNV_Prepare(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_RH_NV_AUTH authHandle,
    TPMI_RH_NV_INDEX nvIndex,
    TPMI_SH_POLICY policySession);

TSS2_RC Tss2_Sys_PolicyAuthorizeNV_Complete(
    TSS2_SYS_CONTEXT *sysContext);

TSS2_RC Tss2_Sys_PolicyAuthorizeNV(
    TSS2_SYS_CONTEXT *sysContext,
    TPMI_RH_NV_AUTH authHandle,
    TPMI_RH_NV_INDEX nvIndex,
    TPMI_SH_POLICY policySession,
    TSS2L_SYS_AUTH_COMMAND const *cmdAuthsArray,
    TSS2L_SYS_AUTH_RESPONSE *rspAuthsArray);

#ifdef __cplusplus
}
#endif
#endif /* TSS2_SYS_H */
