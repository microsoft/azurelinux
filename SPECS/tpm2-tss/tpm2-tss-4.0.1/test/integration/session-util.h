/* SPDX-License-Identifier: BSD-2-Clause */
/***********************************************************************
 * Copyright (c) 2017-2018, Intel Corporation
 *
 * All rights reserved.
 ***********************************************************************/
#ifndef _SESSION_UTIL_H_
#define _SESSION_UTIL_H_

#include <stdbool.h>
#include <uthash.h>
#include "tss2_tpm2_types.h"
#include "tss2_sys.h"
#include "util/tpm2b.h"

typedef struct {
    TPMI_DH_OBJECT tpmKey;
    TPMI_DH_ENTITY bind;
    TPM2B_ENCRYPTED_SECRET encryptedSalt;
    TPM2B_MAX_BUFFER salt;
    TPM2_SE sessionType;
    TPMT_SYM_DEF symmetric;
    TPMI_ALG_HASH authHash;
    TPMI_SH_AUTH_SESSION sessionHandle;
    TPM2B_NONCE nonceTPM;
    TPM2B_DIGEST sessionKey;
    TPM2B_DIGEST authValueBind;
    TPM2B_NONCE nonceNewer;
    TPM2B_NONCE nonceOlder;
    TPM2B_NONCE nonceTpmDecrypt;
    TPM2B_NONCE nonceTpmEncrypt;
    TPM2B_NAME name;
    void *hmacPtr;
    UT_hash_handle hh;
} SESSION;

typedef struct{
    TPM2_HANDLE entityHandle;
    TPM2B_AUTH entityAuth;
    UT_hash_handle hh;
} ENTITY;

/*
 * Helper function used to calculate cpHash and rpHash
 * if command is true cpHash is calculated,
 * otherwise rpHash rpHash is calculated.
 */
TSS2_RC
tpm_calc_phash(
    TSS2_SYS_CONTEXT *sysContext,
    TPM2_HANDLE handle1,
    TPM2_HANDLE handle2,
    TPM2_HANDLE handle3,
    TPMI_ALG_HASH auth_hash,
    bool command,
    TPM2B_DIGEST *result);

UINT32
tpm_handle_to_name(
    TSS2_TCTI_CONTEXT *tcti_context,
    TPM2_HANDLE handle,
    TPM2B_NAME *name);

void
roll_nonces(
    SESSION *session,
    TPM2B_NONCE *new_nonce);

TSS2_RC
KDFa(TPMI_ALG_HASH hash,
     TPM2B *key,
     const char *label,
     TPM2B *contextU,
     TPM2B *contextV,
     UINT16 bits,
     TPM2B_MAX_BUFFER *resultKey );

SESSION *
get_session(TPMI_SH_AUTH_SESSION hndl);

TSS2_RC create_auth_session(
    SESSION **psession,
    TPMI_DH_OBJECT tpmKey,
    TPM2B_MAX_BUFFER *salt,
    TPMI_DH_ENTITY bind,
    TPM2B_AUTH *bindAuth,
    TPM2B_NONCE *nonceCaller,
    TPM2B_ENCRYPTED_SECRET *encryptedSalt,
    TPM2_SE sessionType,
    TPMT_SYM_DEF *symmetric,
    TPMI_ALG_HASH algId,
    TSS2_TCTI_CONTEXT *tctiContext);

TSS2_RC
compute_command_hmac(
    TSS2_SYS_CONTEXT *sysContext,
    TPM2_HANDLE handle1,
    TPM2_HANDLE handle2,
    TPM2_HANDLE handle3,
    TSS2L_SYS_AUTH_COMMAND *pSessionsDataIn);

TSS2_RC
check_response_hmac(
    TSS2_SYS_CONTEXT *sysContext,
    TSS2L_SYS_AUTH_COMMAND *pSessionsDataIn,
    TPM2_HANDLE handle1,
    TPM2_HANDLE handle2,
    TPM2_HANDLE handle3,
    TSS2L_SYS_AUTH_RESPONSE *pSessionsDataOut);

void
end_auth_session(SESSION *session);

int
AddEntity(TPM2_HANDLE handle, TPM2B_AUTH *auth);

void
DeleteEntity(TPM2_HANDLE handle);

int
GetEntityAuth(TPM2_HANDLE handle, TPM2B_AUTH *auth);

ENTITY *
GetEntity(TPM2_HANDLE handle);

TSS2_RC
encrypt_command_param(
    SESSION *session,
    TPM2B_MAX_BUFFER *encryptedData,
    TPM2B_MAX_BUFFER *clearData,
    TPM2B_AUTH *authValue);

TSS2_RC
decrypt_response_param(
    SESSION *session,
    TPM2B_MAX_BUFFER *clearData,
    TPM2B_MAX_BUFFER *encryptedData,
    TPM2B_AUTH *authValue);

#endif
