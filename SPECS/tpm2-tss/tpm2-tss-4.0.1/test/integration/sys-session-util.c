/* SPDX-License-Identifier: BSD-2-Clause */
/***********************************************************************
 * Copyright (c) 2017-2018, Intel Corporation
 *
 * All rights reserved.
 ***********************************************************************/
#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <inttypes.h>

#include "session-util.h"
#include "sys-util.h"
#include "context-util.h"
#include "util/tss2_endian.h"
#define LOGMODULE test
#include "util/log.h"

static SESSION *sessions = NULL;

SESSION *
get_session(TPMI_SH_AUTH_SESSION hndl)
{
    SESSION *s;

    HASH_FIND_INT(sessions, &hndl, s);
    return s;
}

static TSS2_RC
start_auth_session(
    SESSION *session,
    TSS2_TCTI_CONTEXT *tctiContext)
{
    TSS2_RC rval;
    TPM2B_ENCRYPTED_SECRET key;
    char label[] = "ATH";
    TSS2_SYS_CONTEXT *tmp_context;
    UINT16 bytes;

    key.size = 0;

    tmp_context = sys_init_from_tcti_ctx(tctiContext);
    if (tmp_context == NULL)
        return TSS2_SYS_RC_GENERAL_FAILURE;

    if (session->nonceOlder.size == 0)
        session->nonceOlder.size = GetDigestSize(session->authHash);

    memset(session->nonceOlder.buffer, '\0', session->nonceOlder.size);
    session->nonceNewer.size = session->nonceOlder.size;
    session->nonceTpmDecrypt.size = 0;
    session->nonceTpmEncrypt.size = 0;

    rval = Tss2_Sys_StartAuthSession(
            tmp_context, session->tpmKey, session->bind, 0,
            &session->nonceOlder, &session->encryptedSalt,
            session->sessionType, &session->symmetric,
            session->authHash, &session->sessionHandle,
            &session->nonceNewer, 0);
    if (rval != TPM2_RC_SUCCESS)
        goto out;

    if (session->tpmKey == TPM2_RH_NULL)
        session->salt.size = 0;

    if (session->bind == TPM2_RH_NULL)
        session->authValueBind.size = 0;

    session->sessionKey.size = 0;
    if (session->tpmKey == TPM2_RH_NULL && session->bind == TPM2_RH_NULL)
        goto out;

    /* Generate the key used as input to the KDF. */
    rval = ConcatSizedByteBuffer((TPM2B_MAX_BUFFER *)&key,
            (TPM2B *)&session->authValueBind);
    if (rval != TPM2_RC_SUCCESS) {
        Tss2_Sys_FlushContext(tmp_context, session->sessionHandle);
        goto out;
    }

    rval = ConcatSizedByteBuffer((TPM2B_MAX_BUFFER *)&key,
            (TPM2B *)&session->salt);
    if (rval != TPM2_RC_SUCCESS) {
        Tss2_Sys_FlushContext(tmp_context, session->sessionHandle);
        goto out;
    }

    bytes = GetDigestSize(session->authHash) * 8;

    rval = KDFa(session->authHash, (TPM2B *)&key, label,
                (TPM2B *)&session->nonceNewer,
                (TPM2B *)&session->nonceOlder,
                bytes, (TPM2B_MAX_BUFFER *)&session->sessionKey);
out:
    sys_teardown(tmp_context);
    return rval;
}

static TSS2_RC
compute_session_auth(
    TSS2_SYS_CONTEXT *sysContext,
    SESSION *session,
    TPMS_AUTH_COMMAND *pSessionDataIn,
    bool command,
    TPM2_HANDLE handle1,
    TPM2_HANDLE handle2,
    TPM2_HANDLE handle3,
    TPM2B_MAX_BUFFER *hmacKey)
{
    TPM2B_DIGEST *buffer_list[7];
    TPM2B_DIGEST pHash = TPM2B_DIGEST_INIT;
    TPM2B_DIGEST sessionAttributesByteBuffer = {
        .size = 1,
        .buffer = { pSessionDataIn->sessionAttributes, }
    };
    UINT16 i;
    TSS2_RC rval;
    TPM2_CC cmdCode;

    rval = tpm_calc_phash(sysContext, handle1, handle2, handle3,
                        session->authHash, command, &pHash);
    if (rval != TPM2_RC_SUCCESS)
        return rval;

    rval = Tss2_Sys_GetCommandCode(sysContext, (UINT8 *)&cmdCode);
    if (rval != TPM2_RC_SUCCESS)
        return rval;

    /* cmdCode comes back as BigEndian; not suited for comparisons below. */
    cmdCode = BE_TO_HOST_32(cmdCode);
    LOGBLOB_DEBUG(hmacKey->buffer, hmacKey->size, "hmacKey=");

    i = 0;
    buffer_list[i++] = (TPM2B_DIGEST *)&pHash;
    buffer_list[i++] = (TPM2B_DIGEST *)&session->nonceNewer;
    buffer_list[i++] = (TPM2B_DIGEST *)&session->nonceOlder;
    buffer_list[i++] = (TPM2B_DIGEST *)&session->nonceTpmDecrypt;
    buffer_list[i++] = (TPM2B_DIGEST *)&session->nonceTpmEncrypt;
    buffer_list[i++] = (TPM2B_DIGEST *)&sessionAttributesByteBuffer;
    buffer_list[i++] = 0;

    for (int j = 0; buffer_list[j] != 0; j++) {
            LOGBLOB_DEBUG(&buffer_list[j]->buffer[0],
                    buffer_list[j]->size, "bufferlist[%d]:", j);
            ;
    }

    rval = hmac(session->authHash, hmacKey->buffer,
            hmacKey->size, buffer_list,
            (TPM2B_DIGEST *)&pSessionDataIn->hmac);

    if (rval != TPM2_RC_SUCCESS) {
        LOGBLOB_ERROR(pSessionDataIn->hmac.buffer,
                      pSessionDataIn->hmac.size,
                      "HMAC Failed rval = %d !!!", rval);
        return rval;
    }
    return rval;
}

TSS2_RC
compute_command_hmac(
    TSS2_SYS_CONTEXT *sysContext,
    TPM2_HANDLE handle1,
    TPM2_HANDLE handle2,
    TPM2_HANDLE handle3,
    TSS2L_SYS_AUTH_COMMAND *pSessionsDataIn)
{
    TPM2_HANDLE handles[3] = {handle1, handle2, handle3};
    ENTITY *entity;
    SESSION *session;
    TPM2B_MAX_BUFFER hmac_key;
    TSS2_RC rval = TPM2_RC_SUCCESS;
    unsigned int i;
    unsigned int count = pSessionsDataIn->count;

    if (count > 3) {
        LOG_ERROR("Bad value for session count: %" PRIu16, count);
        return TSS2_SYS_RC_GENERAL_FAILURE;
    }

    for (i = 0; i < count; i++) {
        if (handles[i] == TPM2_RH_NULL)
            break;

        entity = GetEntity(handles[i]);
        if (!entity)
            return TSS2_SYS_RC_GENERAL_FAILURE;

        session = get_session(pSessionsDataIn->auths[i].sessionHandle);
        if (!session)
            return TPM2_RC_SUCCESS;

        CopySizedByteBuffer((TPM2B *)&hmac_key, (TPM2B *)&session->sessionKey);

        if (handles[i] != session->bind || handles[i] == TPM2_RH_NULL)
            ConcatSizedByteBuffer(&hmac_key, (TPM2B *)&entity->entityAuth);

        rval = compute_session_auth(sysContext,
                session,
                &pSessionsDataIn->auths[i],
                true,
                handle1,
                handle2,
                handle3,
                &hmac_key);
        if (rval != TPM2_RC_SUCCESS)
            break;
    }
    return rval;
}

TSS2_RC check_response_hmac(
        TSS2_SYS_CONTEXT *sysContext,
        TSS2L_SYS_AUTH_COMMAND *pSessionsDataIn,
        TPM2_HANDLE handle1,
        TPM2_HANDLE handle2,
        TPM2_HANDLE handle3,
        TSS2L_SYS_AUTH_RESPONSE *pSessionsDataOut)
{
    TPM2_HANDLE handles[3] = {handle1, handle2, handle3};
    ENTITY *entity;
    SESSION *session;
    TPM2B_MAX_BUFFER hmac_key;
    TSS2_RC rval = TPM2_RC_SUCCESS;
    unsigned int i;
    unsigned int count = pSessionsDataIn->count;

    if (count > 3) {
        LOG_ERROR("Bad value for session count: %" PRIu16, count);
        return TSS2_SYS_RC_GENERAL_FAILURE;
    }

    for (i = 0; i < count; i++) {
        if (handles[i] == TPM2_RH_NULL)
            break;

        entity = GetEntity(handles[i]);
        if (!entity)
            return TSS2_SYS_RC_GENERAL_FAILURE;

        session = get_session(pSessionsDataIn->auths[i].sessionHandle);
        if (!session)
            return TPM2_RC_SUCCESS;

        CopySizedByteBuffer((TPM2B *)&hmac_key, (TPM2B *)&session->sessionKey);

        if (handles[i] != session->bind)
            ConcatSizedByteBuffer(&hmac_key, (TPM2B *)&entity->entityAuth);

        rval = compute_session_auth(sysContext,
                    session,
                    &pSessionsDataIn->auths[i],
                    false,
                    handle1,
                    handle2,
                    handle3,
                    &hmac_key);

        if (rval != TPM2_RC_SUCCESS)
            return rval;

        rval = CompareSizedByteBuffer((TPM2B *)&pSessionsDataIn->auths[i].hmac,
                                      (TPM2B *)&pSessionsDataOut->auths[i].hmac);
        if (rval != TPM2_RC_SUCCESS)
            return TSS2_SYS_RC_GENERAL_FAILURE;
    }
    return rval;
}

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
    TSS2_TCTI_CONTEXT *tctiContext)
{
    TSS2_RC rval;
    SESSION *session, *tmp;

    if (psession == NULL)
        return TSS2_SYS_RC_BAD_REFERENCE;

    session = calloc(1, sizeof(SESSION));

    if (!session)
        return TSS2_SYS_RC_GENERAL_FAILURE;

    session->bind = bind;
    session->tpmKey = tpmKey;
    CopySizedByteBuffer((TPM2B *)&session->nonceOlder, (TPM2B *)nonceCaller);
    CopySizedByteBuffer((TPM2B *)&session->encryptedSalt, (TPM2B *)encryptedSalt);
    session->sessionType = sessionType;
    session->symmetric.algorithm = symmetric->algorithm;
    session->symmetric.keyBits.sym = symmetric->keyBits.sym;
    session->symmetric.mode.sym = symmetric->mode.sym;
    session->authHash = algId;
    if (bindAuth != NULL)
        CopySizedByteBuffer((TPM2B *)&session->authValueBind, (TPM2B *)bindAuth);

    if (session->tpmKey != TPM2_RH_NULL)
        CopySizedByteBuffer((TPM2B *)&session->salt, (TPM2B *)salt);

    rval = start_auth_session(session, tctiContext);
    if (rval != TSS2_RC_SUCCESS) {
        free(session);
        return rval;
    }
    /* Make sure this session handle is not already in the table */
    HASH_FIND_INT(sessions, &session->sessionHandle, tmp);
    if (tmp)
        HASH_DEL(sessions, tmp);

    HASH_ADD_INT(sessions, sessionHandle, session);
    *psession = session;
    return TSS2_RC_SUCCESS;
}

void end_auth_session(SESSION *session)
{
    HASH_DEL(sessions, session);
    free(session);
}

void roll_nonces(SESSION *session, TPM2B_NONCE *new_nonce)
{
    session->nonceOlder = session->nonceNewer;
    session->nonceNewer = *new_nonce;
}

TSS2_RC
tpm_calc_phash(
    TSS2_SYS_CONTEXT *sysContext,
    TPM2_HANDLE handle1,
    TPM2_HANDLE handle2,
    TPM2_HANDLE handle3,
    TPMI_ALG_HASH authHash,
    bool command,
    TPM2B_DIGEST *pHash)
{
    TSS2_RC rval = TPM2_RC_SUCCESS;
    TSS2_TCTI_CONTEXT *tcti_context;
    UINT32 i;
    TPM2B_NAME name1, name2, name3;
    TPM2B_MAX_BUFFER hashInput;
    UINT8 *hashInputPtr;
    size_t parametersSize;
    const uint8_t *startParams;
    TPM2_CC cmdCode;

    name1.size = 0;
    name2.size = 0;
    name3.size = 0;
    hashInput.size = 0;

    rval = Tss2_Sys_GetTctiContext(sysContext, &tcti_context);
    if (rval != TPM2_RC_SUCCESS)
        return rval;

    if (command) {
        rval = tpm_handle_to_name(tcti_context, handle1, &name1);
        if (rval != TPM2_RC_SUCCESS)
                return rval;

        rval = tpm_handle_to_name(tcti_context, handle2, &name2);
        if (rval != TPM2_RC_SUCCESS)
            return rval;

        rval = tpm_handle_to_name(tcti_context, handle3, &name3);
        if (rval != TPM2_RC_SUCCESS)
            return rval;

        rval = Tss2_Sys_GetCpBuffer(sysContext, &parametersSize, &startParams);
        if (rval != TPM2_RC_SUCCESS)
            return rval;
    } else {
        rval = Tss2_Sys_GetRpBuffer(sysContext, &parametersSize, &startParams);
        if (rval != TPM2_RC_SUCCESS)
            return rval;

        hashInputPtr = &(hashInput.buffer[hashInput.size]);
        /* This is response code. Assuming 0 (success) */
        *(UINT32 *)hashInputPtr = 0;
        hashInput.size += 4;
    }

    rval = Tss2_Sys_GetCommandCode(sysContext, (UINT8 *)&cmdCode);
    if (rval != TPM2_RC_SUCCESS)
        return rval;

    hashInputPtr = &(hashInput.buffer[hashInput.size]);
    *(UINT32 *)hashInputPtr = cmdCode;
    hashInput.size += 4;

    rval = ConcatSizedByteBuffer(&hashInput, (TPM2B *)&name1);
    if (rval != TPM2_RC_SUCCESS)
        return rval;

    rval = ConcatSizedByteBuffer(&hashInput, (TPM2B *)&name2);
    if (rval != TPM2_RC_SUCCESS)
        return rval;

    rval = ConcatSizedByteBuffer(&hashInput, (TPM2B *)&name3);
    if (rval != TPM2_RC_SUCCESS)
        return rval;

    if (hashInput.size + parametersSize > sizeof(hashInput.buffer))
        return TSS2_SYS_RC_INSUFFICIENT_BUFFER;

    for(i = 0; i < parametersSize; i++)
        hashInput.buffer[hashInput.size + i ] = startParams[i];

    hashInput.size += (UINT16)parametersSize;
    LOGBLOB_DEBUG(&hashInput.buffer[0], hashInput.size, "PHASH input bytes=");

    if (hashInput.size > sizeof(hashInput.buffer))
        return TSS2_SYS_RC_INSUFFICIENT_BUFFER;

    rval = hash(authHash, hashInput.buffer, hashInput.size, pHash);
    if (rval != TPM2_RC_SUCCESS)
        return rval;

    LOGBLOB_DEBUG(&pHash->buffer[0], pHash->size, "PHASH =");
    return rval;
}

UINT32 tpm_handle_to_name(
    TSS2_TCTI_CONTEXT *tcti_context,
    TPM2_HANDLE handle,
    TPM2B_NAME *name)
{
    TSS2_RC rval;
    TPM2B_NAME qualified_name = TPM2B_NAME_INIT;
    TPM2B_PUBLIC public;
    TPM2B_NV_PUBLIC nvPublic;
    TSS2_SYS_CONTEXT *sysContext;
    UINT8 *namePtr;

    if (!tcti_context || !name)
        return TSS2_SYS_RC_BAD_VALUE;

    namePtr = name->name;

    if (handle == TPM2_RH_NULL) {
        name->size = 0;
        return TSS2_RC_SUCCESS;
    }

    switch(handle >> TPM2_HR_SHIFT)
    {
        case TPM2_HT_NV_INDEX:
            sysContext = sys_init_from_tcti_ctx(tcti_context);
            if (sysContext == NULL)
                return TSS2_SYS_RC_GENERAL_FAILURE;

            nvPublic.size = 0;
            rval = Tss2_Sys_NV_ReadPublic(sysContext, handle, 0,
                                          &nvPublic, name, 0);
            sys_teardown(sysContext);
            break;

        case TPM2_HT_TRANSIENT:
        case TPM2_HT_PERSISTENT:
            sysContext = sys_init_from_tcti_ctx(tcti_context);
            if (sysContext == NULL)
                return TSS2_SYS_RC_GENERAL_FAILURE;

            public.size = 0;
            rval = Tss2_Sys_ReadPublic(sysContext, handle, 0,
                                       &public, name, &qualified_name, 0);
            sys_teardown(sysContext);
            break;

        default:
            rval = TPM2_RC_SUCCESS;
            name->size = sizeof(TPM2_HANDLE);
            *(TPM2_HANDLE *)namePtr = BE_TO_HOST_32(handle);
    }
    return rval;
}

TSS2_RC
KDFa(
    TPMI_ALG_HASH hash,
    TPM2B *key,
    const char *label,
    TPM2B *contextU,
    TPM2B *contextV,
    UINT16 bits,
    TPM2B_MAX_BUFFER *result_key)
{
    TPM2B_DIGEST digest;
    TPM2B_DIGEST tpm2blabel, tpm2bbits, tpm2bctr;
    TPM2B_DIGEST *buffer_list[8];
    UINT32 counter;
    TSS2_RC rval;
    int i, j;
    UINT16 bytes = bits / 8;

    result_key->size = 0;
    tpm2bctr.size = 4;
    tpm2bbits.size = 4;
    counter = BE_TO_HOST_32(bits);
    memcpy(tpm2bbits.buffer, &counter, 4);
    tpm2blabel.size = strlen(label) + 1;
    memcpy(tpm2blabel.buffer, label, tpm2blabel.size);

    LOG_DEBUG("KDFA, hash = %4.4x", hash);
    LOGBLOB_DEBUG(&key->buffer[0], key->size, "KDFA, key =");
    LOGBLOB_DEBUG(&tpm2blabel.buffer[0], tpm2blabel.size, "KDFA, tpm2blabel =");
    LOGBLOB_DEBUG(&contextU->buffer[0], contextU->size, "KDFA, contextU =");
    LOGBLOB_DEBUG(&contextV->buffer[0], contextV->size, "KDFA, contextV =");

    for (i = 1, j = 0; result_key->size < bytes; j = 0) {
        counter = BE_TO_HOST_32(i++);
        memcpy(tpm2bctr.buffer, &counter, 4);
        buffer_list[j++] = (TPM2B_DIGEST *)&tpm2bctr;
        buffer_list[j++] = (TPM2B_DIGEST *)&tpm2blabel;
        buffer_list[j++] = (TPM2B_DIGEST *)contextU;
        buffer_list[j++] = (TPM2B_DIGEST *)contextV;
        buffer_list[j++] = (TPM2B_DIGEST *)&tpm2bbits;
        buffer_list[j++] = NULL;

        for (j = 0; buffer_list[j] != NULL; j++) {
            LOGBLOB_DEBUG(&buffer_list[j]->buffer[0], buffer_list[j]->size, "bufferlist[%d]:", j);
            ;
        }

        rval = hmac(hash, key->buffer, key->size, buffer_list, &digest);
        if (rval != TPM2_RC_SUCCESS) {
            LOGBLOB_ERROR(digest.buffer, digest.size, "HMAC Failed rval = %d", rval);
            return rval;
        }

        ConcatSizedByteBuffer(result_key, (TPM2B *)&digest);
    }

    /* Truncate the result to the desired size. */
    result_key->size = bytes;
    LOGBLOB_DEBUG(result_key->buffer, result_key->size, "KDFA, key = ");
    return TPM2_RC_SUCCESS;
}

static TSS2_RC
gen_session_key(
    SESSION *session,
    TPM2B_MAX_BUFFER *session_key,
    TPM2B_IV *iv,
    TPM2B_AUTH *auth_value)
{
    TSS2_RC rval = TSS2_RC_SUCCESS;
    UINT32 aes_block_size = 16;
    TPM2B_MAX_BUFFER key, sessionValue;

    if (iv == NULL || session_key == NULL)
        return TSS2_SYS_RC_BAD_VALUE;

    CopySizedByteBuffer((TPM2B *)&sessionValue, (TPM2B *)&session->sessionKey);
    CatSizedByteBuffer((TPM2B *)&sessionValue, (TPM2B *)auth_value);

    rval = KDFa (session->authHash,
                 (TPM2B *)&sessionValue,
                 "CFB",
                 (TPM2B *)&session->nonceNewer,
                 (TPM2B *)&session->nonceOlder,
                 session->symmetric.keyBits.sym + aes_block_size * 8,
                 &key);
    if (rval != TSS2_RC_SUCCESS)
        return rval;

    if (key.size != (session->symmetric.keyBits.sym / 8) + aes_block_size)
        return TSS2_SYS_RC_GENERAL_FAILURE;

    iv->size = aes_block_size;
    session_key->size = (session->symmetric.keyBits.sym) / 8;
    UINT16 total_size = session_key->size + iv->size;
    if (iv->size > sizeof (iv->buffer) ||
         (total_size) > TPM2_MAX_DIGEST_BUFFER)
        return TSS2_SYS_RC_GENERAL_FAILURE;

    memcpy (iv->buffer, &key.buffer[session_key->size], iv->size);
    memcpy (session_key->buffer, key.buffer, session_key->size);
    return rval;
}

static TSS2_RC
encrypt_param_cfb(
    SESSION *session,
    TPM2B_MAX_BUFFER *encrypted_data,
    TPM2B_MAX_BUFFER *clear_data,
    TPM2B_AUTH *auth_value)
{
    TSS2_RC rval = TSS2_RC_SUCCESS;
    TPM2B_MAX_BUFFER encryptKey = TPM2B_MAX_BUFFER_INIT;
    TPM2B_IV iv = TPM2B_IV_INIT;

    rval = gen_session_key(session, &encryptKey, &iv, auth_value);
    if (rval)
        return rval;

    return encrypt_cfb(encrypted_data, clear_data, &encryptKey, &iv);
}

static TSS2_RC
decrypt_param_cfb(
    SESSION *session,
    TPM2B_MAX_BUFFER *clear_data,
    TPM2B_MAX_BUFFER *encrypted_data,
    TPM2B_AUTH *auth_value)
{
    TSS2_RC rval = TSS2_RC_SUCCESS;
    TPM2B_MAX_BUFFER encryptKey = TPM2B_MAX_BUFFER_INIT;
    TPM2B_IV iv = TPM2B_IV_INIT;

    rval = gen_session_key(session, &encryptKey, &iv, auth_value);
    if (rval)
        return rval;

    return decrypt_cfb(clear_data, encrypted_data, &encryptKey, &iv);
}

static TSS2_RC
encrypt_decrypt_xor(
    SESSION *session,
    TPM2B_MAX_BUFFER *output_data,
    TPM2B_MAX_BUFFER *input_data,
    TPM2B_AUTH *auth_value)
{
    TSS2_RC rval = TSS2_RC_SUCCESS;
    TPM2B_MAX_BUFFER key;
    TPM2B_MAX_BUFFER mask = { .size = 0, .buffer = 0 };
    UINT16 i;
    UINT16 size = input_data->size;

    if (size > TPM2_MAX_DIGEST_BUFFER) {
        LOG_ERROR("Bad value for inputData size: %" PRIu16, size);
        return TSS2_SYS_RC_GENERAL_FAILURE;
    }

    CopySizedByteBuffer((TPM2B *)&key, (TPM2B *)&session->sessionKey);
    CatSizedByteBuffer((TPM2B *)&key, (TPM2B *)auth_value);

    rval = KDFa(session->authHash,
            (TPM2B *)&key,
            "XOR",
            (TPM2B *)&session->nonceNewer,
            (TPM2B *)&session->nonceOlder,
            input_data->size * 8, &mask);

    if (rval)
        return rval;

    for (i = 0; i < size; i++)
        output_data->buffer[i] = input_data->buffer[i] ^ mask.buffer[i];

    output_data->size = size;

    return rval;
}

TSS2_RC
encrypt_command_param(
    SESSION *session,
    TPM2B_MAX_BUFFER *encrypted_data,
    TPM2B_MAX_BUFFER *clear_data,
    TPM2B_AUTH *auth_value)
{
    return session->symmetric.algorithm == TPM2_ALG_AES ?
        encrypt_param_cfb(session, encrypted_data, clear_data, auth_value) :
        encrypt_decrypt_xor(session, encrypted_data, clear_data, auth_value);
}

TSS2_RC
decrypt_response_param(
    SESSION *session,
    TPM2B_MAX_BUFFER *clear_data,
    TPM2B_MAX_BUFFER *encrypted_data,
    TPM2B_AUTH *auth_value)
{
    return session->symmetric.algorithm == TPM2_ALG_AES ?
        decrypt_param_cfb(session, clear_data, encrypted_data, auth_value) :
        encrypt_decrypt_xor(session, clear_data, encrypted_data, auth_value);
}
