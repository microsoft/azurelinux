/* SPDX-License-Identifier: BSD-2-Clause */
/*******************************************************************************
 * Copyright 2017-2018, Fraunhofer SIT sponsored by Infineon Technologies AG
 * All rights reserved.
 *******************************************************************************/
#ifndef TSS2_FAPI_H
#define TSS2_FAPI_H

#include <stddef.h>
#include <stdint.h>

#include "tss2_tcti.h"

#ifdef __cplusplus
extern "C" {
#endif

/* Type definitions */

typedef struct FAPI_CONTEXT FAPI_CONTEXT;


/* Defines for blob type of Fapi_GetEsysBlob */

#define FAPI_ESYSBLOB_CONTEXTLOAD 1
#define FAPI_ESYSBLOB_DESERIALIZE 2

/* Context functions */

TSS2_RC Fapi_Initialize(
    FAPI_CONTEXT  **context,
    char     const *uri);

TSS2_RC Fapi_Initialize_Async(
    FAPI_CONTEXT  **context,
    char     const *uri);

TSS2_RC Fapi_Initialize_Finish(
    FAPI_CONTEXT  **context);

void Fapi_Finalize(
    FAPI_CONTEXT  **context);

TSS2_RC Fapi_GetTcti(
    FAPI_CONTEXT       *context,
    TSS2_TCTI_CONTEXT **tcti);

void Fapi_Free(
    void           *ptr);

#if defined(__linux__) || defined(__unix__) || defined(__APPLE__) || defined (__QNXNTO__) || defined (__VXWORKS__)
#if defined (__VXWORKS__)
#include <sys/poll.h>
#else
#include <poll.h>
#endif
typedef struct pollfd FAPI_POLL_HANDLE;
#elif defined(_WIN32)
#include <windows.h>
typedef HANDLE FAPI_POLL_HANDLE;
#else
typedef void FAPI_POLL_HANDLE;
#ifndef FAPI_SUPPRESS_POLL_WARNINGS
#pragma message "Info: Platform not supported for FAPI_POLL_HANDLES"
#endif
#endif

TSS2_RC Fapi_GetPollHandles(
    FAPI_CONTEXT      *context,
    FAPI_POLL_HANDLE **handles,
    size_t            *num_handles);

TSS2_RC Fapi_GetInfo(
    FAPI_CONTEXT   *context,
    char          **info);

TSS2_RC Fapi_GetInfo_Async(
    FAPI_CONTEXT   *context);

TSS2_RC Fapi_GetInfo_Finish(
    FAPI_CONTEXT   *context,
    char          **info);

/* General functions */

TSS2_RC Fapi_Provision(
    FAPI_CONTEXT   *context,
    char     const *authValueEh,
    char     const *authValueSh,
    char     const *authValueLockout);

TSS2_RC Fapi_Provision_Async(
    FAPI_CONTEXT   *context,
    char     const *authValueEh,
    char     const *authValueSh,
    char     const *authValueLockout);

TSS2_RC Fapi_Provision_Finish(
    FAPI_CONTEXT   *context);

TSS2_RC Fapi_GetPlatformCertificates(
    FAPI_CONTEXT   *context,
    uint8_t       **certificates,
    size_t         *certificatesSize);

TSS2_RC Fapi_GetPlatformCertificates_Async(
    FAPI_CONTEXT   *context);

TSS2_RC Fapi_GetPlatformCertificates_Finish(
    FAPI_CONTEXT   *context,
    uint8_t       **certificates,
    size_t         *certificatesSize);

TSS2_RC Fapi_GetRandom(
    FAPI_CONTEXT   *context,
    size_t          numBytes,
    uint8_t       **data);

TSS2_RC Fapi_GetRandom_Async(
    FAPI_CONTEXT   *context,
    size_t          numBytes);

TSS2_RC Fapi_GetRandom_Finish(
    FAPI_CONTEXT   *context,
    uint8_t       **data);

TSS2_RC Fapi_Import(
    FAPI_CONTEXT   *context,
    char     const *path,
    char     const *importData);

TSS2_RC Fapi_Import_Async(
    FAPI_CONTEXT   *context,
    char     const *path,
    char     const *importData);

TSS2_RC Fapi_Import_Finish(
    FAPI_CONTEXT   *context);

TSS2_RC Fapi_List(
    FAPI_CONTEXT   *context,
    char     const *searchPath,
    char          **pathList);

TSS2_RC Fapi_List_Async(
    FAPI_CONTEXT   *context,
    char     const *searchPath);

TSS2_RC Fapi_List_Finish(
    FAPI_CONTEXT   *context,
    char          **pathList);

TSS2_RC Fapi_Delete(
    FAPI_CONTEXT   *context,
    char     const *path);

TSS2_RC Fapi_Delete_Async(
    FAPI_CONTEXT   *context,
    char     const *path);

TSS2_RC Fapi_Delete_Finish(
    FAPI_CONTEXT   *context);

TSS2_RC Fapi_GetEsysBlob(
    FAPI_CONTEXT   *context,
    char     const *path,
    uint8_t        *type,
    uint8_t       **data,
    size_t         *length);

TSS2_RC Fapi_GetEsysBlob_Async(
    FAPI_CONTEXT   *context,
    char     const *path);

TSS2_RC Fapi_GetEsysBlob_Finish(
    FAPI_CONTEXT   *context,
    uint8_t        *type,
    uint8_t       **data,
    size_t         *length);

TSS2_RC Fapi_ChangeAuth(
    FAPI_CONTEXT   *context,
    char     const *entityPath,
    char     const *authValue);

TSS2_RC Fapi_ChangeAuth_Async(
    FAPI_CONTEXT   *context,
    char     const *entityPath,
    char     const *authValue);

TSS2_RC Fapi_ChangeAuth_Finish(
    FAPI_CONTEXT   *context);

TSS2_RC Fapi_SetDescription(
    FAPI_CONTEXT   *context,
    char     const *path,
    char     const *description);

TSS2_RC Fapi_SetDescription_Async(
    FAPI_CONTEXT   *context,
    char     const *path,
    char     const *description);

TSS2_RC Fapi_SetDescription_Finish(
    FAPI_CONTEXT   *context);

TSS2_RC Fapi_GetDescription(
    FAPI_CONTEXT   *context,
    char     const *path,
    char          **description);

TSS2_RC Fapi_GetDescription_Async(
    FAPI_CONTEXT   *context,
    char     const *path);

TSS2_RC Fapi_GetDescription_Finish(
    FAPI_CONTEXT   *context,
    char          **description);

TSS2_RC Fapi_SetAppData(
    FAPI_CONTEXT   *context,
    char     const *path,
    uint8_t  const *appData,
    size_t          appDataSize);

TSS2_RC Fapi_SetAppData_Async(
    FAPI_CONTEXT   *context,
    char     const *path,
    uint8_t  const *appData,
    size_t          appDataSize);

TSS2_RC Fapi_SetAppData_Finish(
    FAPI_CONTEXT   *context);

TSS2_RC Fapi_GetAppData(
    FAPI_CONTEXT   *context,
    char     const *path,
    uint8_t       **appData,
    size_t         *appDataSize);

TSS2_RC Fapi_GetAppData_Async(
    FAPI_CONTEXT   *context,
    char     const *path);

TSS2_RC Fapi_GetAppData_Finish(
    FAPI_CONTEXT   *context,
    uint8_t       **appData,
    size_t         *appDataSize);

TSS2_RC Fapi_GetTpmBlobs(
    FAPI_CONTEXT   *context,
    char     const *path,
    uint8_t       **tpm2bPublic,
    size_t         *tpm2bPublicSize,
    uint8_t       **tpm2bPrivate,
    size_t         *tpm2bPrivateSize,
    char          **policy);

TSS2_RC Fapi_GetTpmBlobs_Async(
    FAPI_CONTEXT   *context,
    char     const *path);

TSS2_RC Fapi_GetTpmBlobs_Finish(
    FAPI_CONTEXT   *context,
    uint8_t       **tpm2bPublic,
    size_t         *tpm2bPublicSize,
    uint8_t       **tpm2bPrivate,
    size_t         *tpm2bPrivateSize,
    char          **policy);

/* Key functions */

TSS2_RC Fapi_CreateKey(
    FAPI_CONTEXT   *context,
    char     const *path,
    char     const *type,
    char     const *policyPath,
    char     const *authValue);

TSS2_RC Fapi_CreateKey_Async(
    FAPI_CONTEXT   *context,
    char     const *path,
    char     const *type,
    char     const *policyPath,
    char     const *authValue);

TSS2_RC Fapi_CreateKey_Finish(
    FAPI_CONTEXT   *context);

TSS2_RC Fapi_Sign(
    FAPI_CONTEXT   *context,
    char     const *keyPath,
    char     const *padding,
    uint8_t  const *digest,
    size_t          digestSize,
    uint8_t       **signature,
    size_t         *signatureSize,
    char          **publicKey,
    char          **certificate);

TSS2_RC Fapi_Sign_Async(
    FAPI_CONTEXT   *context,
    char     const *keyPath,
    char     const *padding,
    uint8_t  const *digest,
    size_t         digestSize);

TSS2_RC Fapi_Sign_Finish(
    FAPI_CONTEXT   *context,
    uint8_t       **signature,
    size_t         *signatureSize,
    char          **publicKey,
    char          **certificate);

TSS2_RC Fapi_VerifySignature(
    FAPI_CONTEXT   *context,
    char     const *keyPath,
    uint8_t  const *digest,
    size_t          digestSize,
    uint8_t  const *signature,
    size_t          signatureSize);

TSS2_RC Fapi_VerifySignature_Async(
    FAPI_CONTEXT   *context,
    char     const *keyPath,
    uint8_t  const *digest,
    size_t          digestSize,
    uint8_t  const *signature,
    size_t          signatureSize);

TSS2_RC Fapi_VerifySignature_Finish(
    FAPI_CONTEXT   *context);

TSS2_RC Fapi_Encrypt(
    FAPI_CONTEXT   *context,
    char     const *keyPath,
    uint8_t  const *plainText,
    size_t          plainTextSize,
    uint8_t       **cipherText,
    size_t         *cipherTextSize);

TSS2_RC Fapi_Encrypt_Async(
    FAPI_CONTEXT   *context,
    char     const *keyPath,
    uint8_t  const *plainText,
    size_t          plainTextSize);

TSS2_RC Fapi_Encrypt_Finish(
    FAPI_CONTEXT   *context,
    uint8_t       **cipherText,
    size_t         *cipherTextSize );

TSS2_RC Fapi_Decrypt(
    FAPI_CONTEXT   *context,
    char     const *keyPath,
    uint8_t  const *cipherText,
    size_t          cipherTextSize,
    uint8_t       **plainText,
    size_t         *plainTextSize);

TSS2_RC Fapi_Decrypt_Async(
    FAPI_CONTEXT   *context,
    char     const *keyPath,
    uint8_t  const *cipherText,
    size_t          cipherTextSize);

TSS2_RC Fapi_Decrypt_Finish(
    FAPI_CONTEXT   *context,
    uint8_t       **plainText,
    size_t         *plainTextSize);

TSS2_RC Fapi_SetCertificate(
    FAPI_CONTEXT   *context,
    char     const *path,
    char     const *x509certData);

TSS2_RC Fapi_SetCertificate_Async(
    FAPI_CONTEXT   *context,
    char     const *path,
    char     const *x509certData);

TSS2_RC Fapi_SetCertificate_Finish(
    FAPI_CONTEXT   *context);

TSS2_RC Fapi_GetCertificate(
    FAPI_CONTEXT   *context,
    char     const *path,
    char          **x509certData);

TSS2_RC Fapi_GetCertificate_Async(
    FAPI_CONTEXT   *context,
    char     const *path);

TSS2_RC Fapi_GetCertificate_Finish(
    FAPI_CONTEXT   *context,
    char          **x509certData);

TSS2_RC Fapi_ExportKey(
    FAPI_CONTEXT   *context,
    char     const *pathOfKeyToDuplicate,
    char     const *pathToPublicKeyOfNewParent,
    char          **exportedData);

TSS2_RC Fapi_ExportKey_Async(
    FAPI_CONTEXT   *context,
    char     const *pathOfKeyToDuplicate,
    char     const *pathToPublicKeyOfNewParent);

TSS2_RC Fapi_ExportKey_Finish(
    FAPI_CONTEXT   *context,
    char          **exportedData);

/* Seal functions */

TSS2_RC Fapi_CreateSeal(
    FAPI_CONTEXT   *context,
    char     const *path,
    char     const *type,
    size_t          size,
    char     const *policyPath,
    char     const *authValue,
    uint8_t  const *data);

TSS2_RC Fapi_CreateSeal_Async(
    FAPI_CONTEXT   *context,
    char     const *path,
    char     const *type,
    size_t          size,
    char     const *policyPath,
    char     const *authValue,
    uint8_t  const *data);

TSS2_RC Fapi_CreateSeal_Finish(
    FAPI_CONTEXT   *context);

TSS2_RC Fapi_Unseal(
    FAPI_CONTEXT   *context,
    char     const *path,
    uint8_t       **data,
    size_t         *size);

TSS2_RC Fapi_Unseal_Async(
    FAPI_CONTEXT   *context,
    char     const *path);

TSS2_RC Fapi_Unseal_Finish(
    FAPI_CONTEXT   *context,
    uint8_t       **data,
    size_t         *size);

/* Policy functions */

TSS2_RC Fapi_ExportPolicy(
    FAPI_CONTEXT   *context,
    char     const *path,
    char          **jsonPolicy);

TSS2_RC Fapi_ExportPolicy_Async(
    FAPI_CONTEXT   *context,
    char     const *path);

TSS2_RC Fapi_ExportPolicy_Finish(
    FAPI_CONTEXT   *context,
    char          **jsonPolicy);

TSS2_RC Fapi_AuthorizePolicy(
    FAPI_CONTEXT   *context,
    char     const *policyPath,
    char     const *keyPath,
    uint8_t  const *policyRef,
    size_t          policyRefSize);

TSS2_RC Fapi_AuthorizePolicy_Async(
    FAPI_CONTEXT   *context,
    char     const *policyPath,
    char     const *keyPath,
    uint8_t  const *policyRef,
    size_t          policyRefSize);

TSS2_RC Fapi_AuthorizePolicy_Finish(
    FAPI_CONTEXT   *context);

TSS2_RC Fapi_WriteAuthorizeNv(
    FAPI_CONTEXT   *context,
    char     const *nvPath,
    char     const *policyPath);

TSS2_RC Fapi_WriteAuthorizeNv_Async(
    FAPI_CONTEXT   *context,
    char     const *nvPath,
    char     const *policyPath);

TSS2_RC Fapi_WriteAuthorizeNv_Finish(
    FAPI_CONTEXT   *context);

/* Attestation functions */

TSS2_RC Fapi_PcrRead(
    FAPI_CONTEXT   *context,
    uint32_t        pcrIndex,
    uint8_t       **pcrValue,
    size_t         *pcrValueSize,
    char          **pcrLog);

TSS2_RC Fapi_PcrRead_Async(
    FAPI_CONTEXT   *context,
    uint32_t        pcrIndex);

TSS2_RC Fapi_PcrRead_Finish(
    FAPI_CONTEXT   *context,
    uint8_t       **pcrValue,
    size_t         *pcrValueSize,
    char          **pcrLog);

TSS2_RC Fapi_PcrExtend(
    FAPI_CONTEXT   *context,
    uint32_t        pcr,
    uint8_t  const *data,
    size_t          dataSize,
    char     const *logData);

TSS2_RC Fapi_PcrExtend_Async(
    FAPI_CONTEXT   *context,
    uint32_t        pcr,
    uint8_t  const *data,
    size_t          dataSize,
    char     const *logData);

TSS2_RC Fapi_PcrExtend_Finish(
    FAPI_CONTEXT   *context);


TSS2_RC Fapi_Quote(
    FAPI_CONTEXT   *context,
    uint32_t       *pcrList,
    size_t          pcrListSize,
    char     const *keyPath,
    char     const *quoteType,
    uint8_t  const *qualifyingData,
    size_t          qualifyingDataSize,
    char          **quoteInfo,
    uint8_t       **signature,
    size_t         *signatureSize,
    char          **pcrLog,
    char          **certificate);

TSS2_RC Fapi_Quote_Async(
    FAPI_CONTEXT   *context,
    uint32_t       *pcrList,
    size_t          pcrListSize,
    char     const *keyPath,
    char     const *quoteType,
    uint8_t  const *qualifyingData,
    size_t          qualifyingDataSize);

TSS2_RC Fapi_Quote_Finish(
    FAPI_CONTEXT  *context,
    char         **quoteInfo,
    uint8_t      **signature,
    size_t        *signatureSize,
    char          **pcrLog,
    char          **certificate);

TSS2_RC Fapi_VerifyQuote(
    FAPI_CONTEXT   *context,
    char     const *publicKeyPath,
    uint8_t  const *qualifyingData,
    size_t          qualifyingDataSize,
    char     const *quoteInfo,
    uint8_t  const *signature,
    size_t          signatureSize,
    char     const *pcrLog);

TSS2_RC Fapi_VerifyQuote_Async(
    FAPI_CONTEXT   *context,
    char     const *publicKeyPath,
    uint8_t  const *qualifyingData,
    size_t          qualifyingDataSize,
    char     const *quoteInfo,
    uint8_t  const *signature,
    size_t          signatureSize,
    char     const *pcrLog);

TSS2_RC Fapi_VerifyQuote_Finish(
    FAPI_CONTEXT   *context);

/* NV functions */

TSS2_RC Fapi_CreateNv(
    FAPI_CONTEXT *context,
    char   const *path,
    char   const *type,
    size_t        size,
    char   const *policyPath,
    char   const *authValue);

TSS2_RC Fapi_CreateNv_Async(
    FAPI_CONTEXT *context,
    char   const *path,
    char   const *type,
    size_t        size,
    char   const *policyPath,
    char   const *authValue);

TSS2_RC Fapi_CreateNv_Finish(
    FAPI_CONTEXT *context);

TSS2_RC Fapi_NvRead(
    FAPI_CONTEXT   *context,
    char     const *path,
    uint8_t      **data,
    size_t        *size,
    char         **logData);

TSS2_RC Fapi_NvRead_Async(
    FAPI_CONTEXT   *context,
    char     const *path);

TSS2_RC Fapi_NvRead_Finish(
    FAPI_CONTEXT   *context,
    uint8_t       **data,
    size_t         *size,
    char          **logData);

TSS2_RC Fapi_NvWrite(
    FAPI_CONTEXT  *context,
    char    const *path,
    uint8_t const *data,
    size_t         size);

TSS2_RC Fapi_NvWrite_Async(
    FAPI_CONTEXT  *context,
    char    const *path,
    uint8_t const *data,
    size_t         size);

TSS2_RC Fapi_NvWrite_Finish(
    FAPI_CONTEXT   *context);

TSS2_RC Fapi_NvExtend(
    FAPI_CONTEXT  *context,
    char    const *path,
    uint8_t const *data,
    size_t         size,
    char    const *logData);

TSS2_RC Fapi_NvExtend_Async(
    FAPI_CONTEXT  *context,
    char    const *path,
    uint8_t const *data,
    size_t         size,
    char    const *logData);

TSS2_RC Fapi_NvExtend_Finish(
    FAPI_CONTEXT  *context);

TSS2_RC Fapi_NvIncrement(
    FAPI_CONTEXT   *context,
    char     const *path);

TSS2_RC Fapi_NvIncrement_Async(
    FAPI_CONTEXT   *context,
    char     const *path);

TSS2_RC Fapi_NvIncrement_Finish(
    FAPI_CONTEXT   *context);

TSS2_RC Fapi_NvSetBits(
    FAPI_CONTEXT   *context,
    char     const *path,
    uint64_t        bitmap);

TSS2_RC Fapi_NvSetBits_Async(
    FAPI_CONTEXT   *context,
    char     const *path,
    uint64_t        bitmap);

TSS2_RC Fapi_NvSetBits_Finish(
    FAPI_CONTEXT   *context);

typedef TSS2_RC (*Fapi_CB_Auth)(
    char     const *objectPath,
    char     const *description,
    char    const **auth,
    void           *userData);

TSS2_RC Fapi_SetAuthCB(
    FAPI_CONTEXT   *context,
    Fapi_CB_Auth    callback,
    void           *userData);

typedef TSS2_RC (*Fapi_CB_Branch)(
    char     const *objectPath,
    char     const *description,
    char    const **branchNames,
    size_t          numBranches,
    size_t         *selectedBranch,
    void           *userData);

TSS2_RC Fapi_SetBranchCB(
    FAPI_CONTEXT   *context,
    Fapi_CB_Branch  callback,
    void           *userData);

typedef TSS2_RC (*Fapi_CB_Sign)(
    char     const *objectPath,
    char     const *description,
    char     const *publicKey,
    char     const *publicKeyHint,
    uint32_t        hashAlg,
    uint8_t  const *dataToSign,
    size_t          dataToSignSize,
    uint8_t const **signature,
    size_t         *signatureSize,
    void           *userData);

TSS2_RC Fapi_SetSignCB(
    FAPI_CONTEXT   *context,
    Fapi_CB_Sign    callback,
    void           *userData);

typedef TSS2_RC (*Fapi_CB_PolicyAction)(
    char     const *objectPath,
    char     const *action,
    void           *userData);

TSS2_RC Fapi_SetPolicyActionCB(
    FAPI_CONTEXT        *context,
    Fapi_CB_PolicyAction callback,
    void                *userData);

#ifdef __cplusplus
}
#endif

#endif /* TSS2_FAPI_H */
