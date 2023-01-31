/* SPDX-License-Identifier: BSD-2-Clause */
/***********************************************************************
 * Copyright (c) 2017-2018, Intel Corporation
 *
 * All rights reserved.
 ***********************************************************************/
#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <inttypes.h>

#include "tss2_sys.h"
#include "context-util.h"
#include "sys-util.h"
#include "session-util.h"
#define LOGMODULE test
#include "util/log.h"
#include "test.h"

#define TEST_DATA "test data to encrypt"
#define TEST_DATA_LEN 21

int
test_invoke (TSS2_SYS_CONTEXT *sys_context)
{
    TSS2_RC rc, rc2;
    SESSION *session;
    TSS2_TCTI_CONTEXT *tcti_ctx;
    TPM2B_MAX_NV_BUFFER data_to_write, data_read;
    TPM2B_MAX_BUFFER encrypted_param, decrypted_param;
    TPMI_RH_NV_INDEX nv_index = TPM2_HR_NV_INDEX | 0x01;
    size_t decrypt_param_size, encrypt_param_size;
    const uint8_t *decrypt_param_ptr, *encrypt_param_ptr;
    TPM2B_AUTH nv_auth;
    TPM2B_NV_PUBLIC nv_public;
    TPM2B_DIGEST policy_auth;
    TPMA_NV nv_attribs;
    TPM2B_NONCE nonce_caller;
    TPMT_SYM_DEF symmetric;
    TSS2L_SYS_AUTH_COMMAND req_auth = {
        .auths = {{ .sessionHandle = TPM2_RH_PW }},
        .count = 1
    };
    TSS2L_SYS_AUTH_RESPONSE resp_auth = {
        .count = 0
    };

    nv_attribs = TPMA_NV_AUTHREAD |
                 TPMA_NV_AUTHWRITE |
                 TPMA_NV_ORDERLY;

    nonce_caller.size = 0;
    policy_auth.size = 0;
    nv_auth.size = 0;

    LOG_INFO("param-encrypt-decrypt test");

    rc = Tss2_Sys_GetTctiContext(sys_context, &tcti_ctx);
    if (rc) {
        LOG_ERROR("Tss2_Sys_GetTctiContext failed 0x%" PRIx32, rc);
        return rc;
    }

    nv_public.size = 0;
    nv_public.nvPublic.attributes = nv_attribs;
    CopySizedByteBuffer((TPM2B *)&nv_public.nvPublic.authPolicy, (TPM2B *)&policy_auth);
    nv_public.nvPublic.dataSize = TEST_DATA_LEN;
    nv_public.nvPublic.nvIndex = nv_index;
    nv_public.nvPublic.nameAlg = TPM2_ALG_SHA256;

    rc = Tss2_Sys_NV_DefineSpace(sys_context, TPM2_RH_OWNER, &req_auth,
                                 &nv_auth, &nv_public, &resp_auth);
    if (rc) {
        LOG_ERROR("Tss2_Sys_NV_DefineSpace failed 0x%" PRIx32, rc);
        return rc;
    }

    symmetric.algorithm = TPM2_ALG_AES;
    symmetric.keyBits.aes = 128;
    symmetric.mode.aes = TPM2_ALG_CFB;

retry:
    rc = create_auth_session(&session, TPM2_RH_NULL, 0,
                TPM2_RH_NULL, 0, &nonce_caller, 0, TPM2_SE_POLICY,
                &symmetric, TPM2_ALG_SHA256, tcti_ctx);
    if (rc) {
        LOG_ERROR("create_auth_session failed 0x%" PRIx32, rc);
        goto clean;
    }

    memcpy(data_to_write.buffer, TEST_DATA, TEST_DATA_LEN);
    data_to_write.size = TEST_DATA_LEN;

    rc = Tss2_Sys_NV_Write_Prepare(sys_context, nv_index, nv_index,
                                   &data_to_write, 0);
    if (rc) {
        LOG_ERROR("Tss2_Sys_NV_Write_Prepare failed 0x%" PRIx32, rc);
        goto clean;
    }

    req_auth.count = 2;
    /* Set up auth session structure */
    req_auth.auths[0].sessionHandle = TPM2_RH_PW;
    req_auth.auths[0].nonce.size = 0;
    req_auth.auths[0].sessionAttributes = 0;
    req_auth.auths[0].hmac.size = nv_auth.size;
    memcpy(req_auth.auths[0].hmac.buffer, nv_auth.buffer,
           req_auth.auths[0].hmac.size);

    /* Set up encrypt/decrypt session structure */
    req_auth.auths[1].sessionHandle = session->sessionHandle;
    req_auth.auths[1].nonce.size = 0;
    req_auth.auths[1].sessionAttributes = TPMA_SESSION_CONTINUESESSION | TPMA_SESSION_DECRYPT;
    req_auth.auths[1].hmac.size = 0;

    rc = Tss2_Sys_SetCmdAuths(sys_context, &req_auth);
    if (rc) {
        LOG_ERROR("Tss2_Sys_SetCmdAuths failed 0x%" PRIx32, rc);
        goto clean;
    }

    rc = Tss2_Sys_GetDecryptParam(sys_context, &decrypt_param_size, &decrypt_param_ptr);
    if (rc) {
        LOG_ERROR("Tss2_Sys_GetDecryptParam failed 0x%" PRIx32, rc);
        goto clean;
    }

    if (decrypt_param_size != TEST_DATA_LEN) {
        rc = 99;
        LOG_ERROR("Invalid decrypt_param_size %d", (int)decrypt_param_size);
        goto clean;
    }

    roll_nonces(session, &req_auth.auths[1].nonce);

    rc = encrypt_command_param(session, &encrypted_param,
                               (TPM2B_MAX_BUFFER *)&data_to_write, &nv_auth);
    if (rc) {
        LOG_ERROR("encrypt_command_param failed 0x%" PRIx32, rc);
        goto clean;
    }

    rc = Tss2_Sys_SetDecryptParam(sys_context, encrypted_param.size,
                                  encrypted_param.buffer);
    if (rc) {
        LOG_ERROR("Tss2_Sys_SetDecryptParam failed 0x%" PRIx32, rc);
        goto clean;
    }

    rc = Tss2_Sys_Execute(sys_context);
    if (rc) {
        if ((rc & 0x0000ffff) == TPM2_RC_RETRY) {
            LOG_INFO("Tss2_Sys_Execute returned retry 0x%" PRIx32, rc);
            Tss2_Sys_FlushContext(sys_context, session->sessionHandle);
            end_auth_session(session);
            goto retry;
        }

        LOG_ERROR("Tss2_Sys_Execute failed 0x%" PRIx32, rc);
        goto clean;
    }

    rc = Tss2_Sys_GetRspAuths(sys_context, &resp_auth);
    if (rc) {
        LOG_ERROR("Tss2_Sys_GetRspAuths failed 0x%" PRIx32, rc);
        goto clean;
    }

    /* Roll the nonces for response */
    roll_nonces(session, &resp_auth.auths[1].nonce);

    /* Roll the nonces for next command */
    roll_nonces(session, &req_auth.auths[1].nonce);

    req_auth.count = 1;

    rc = Tss2_Sys_NV_Read(sys_context, nv_index, nv_index, &req_auth,
                          TEST_DATA_LEN, 0, &data_read, &resp_auth);
    if (rc) {
        LOG_ERROR("Tss2_Sys_NV_Read failed 0x%" PRIx32, rc);
        goto clean;
    }

    roll_nonces(session, &resp_auth.auths[1].nonce);

    if (memcmp(data_read.buffer, data_to_write.buffer, data_read.size)) {
        LOG_ERROR("Read data not equal to written data");
        LOGBLOB_ERROR(data_to_write.buffer, data_to_write.size, "written");
        LOGBLOB_ERROR(data_read.buffer, data_read.size, "read");
        rc = 99;
        goto clean;
    }

    rc = Tss2_Sys_NV_Read_Prepare(sys_context, nv_index, nv_index, TEST_DATA_LEN, 0);
    if (rc) {
        LOG_ERROR("Tss2_Sys_NV_Read_Prepare failed 0x%" PRIx32, rc);
        goto clean;
    }

    roll_nonces(session, &req_auth.auths[1].nonce);

    req_auth.count = 2;
    req_auth.auths[1].sessionAttributes &= ~TPMA_SESSION_DECRYPT;
    req_auth.auths[1].sessionAttributes |= TPMA_SESSION_ENCRYPT;
    req_auth.auths[1].sessionAttributes |= TPMA_SESSION_CONTINUESESSION;

    rc = Tss2_Sys_SetCmdAuths(sys_context, &req_auth);
    if (rc) {
        LOG_ERROR("Tss2_Sys_SetCmdAuths failed 0x%" PRIx32, rc);
        goto clean;
    }

    rc = Tss2_Sys_Execute(sys_context);
    if (rc) {
        LOG_ERROR("Tss2_Sys_Execute failed 0x%" PRIx32, rc);
        goto clean;
    }

    rc = Tss2_Sys_GetEncryptParam(sys_context, &encrypt_param_size, &encrypt_param_ptr);
    if (rc) {
        LOG_ERROR("Tss2_Sys_GetEncryptParam failed 0x%" PRIx32, rc);
        goto clean;
    }

    rc = Tss2_Sys_GetRspAuths(sys_context, &resp_auth);
    if (rc) {
        LOG_ERROR("Tss2_Sys_GetRspAuths failed 0x%" PRIx32, rc);
        goto clean;
    }

    roll_nonces(session, &resp_auth.auths[1].nonce);

    encrypted_param.size = encrypt_param_size;
    memcpy(encrypted_param.buffer, encrypt_param_ptr, encrypt_param_size);

    rc = decrypt_response_param(session, &decrypted_param,
                                &encrypted_param, &nv_auth);
    if (rc) {
        LOG_ERROR("decrypt_response_param failed 0x%" PRIx32, rc);
        goto clean;
    }

    roll_nonces(session, &resp_auth.auths[1].nonce);

    rc = Tss2_Sys_SetEncryptParam(sys_context, decrypted_param.size,
                                  decrypted_param.buffer);
    if (rc) {
        LOG_ERROR("Tss2_Sys_SetEncryptParam failed 0x%" PRIx32, rc);
        goto clean;
    }

    rc = Tss2_Sys_NV_Read_Complete(sys_context, &data_read);
    if (rc) {
        LOG_ERROR("Tss2_Sys_NV_Read_Complete failed 0x%" PRIx32, rc);
        goto clean;
    }

    LOGBLOB_DEBUG(data_read.buffer, (UINT32)data_read.size, "Decrypted read data = ");

    if (memcmp(data_read.buffer, data_to_write.buffer, data_read.size)) {
        LOG_ERROR("Read data not equal to written data");
        rc = 99;
        goto clean;
    }

    rc = Tss2_Sys_FlushContext(sys_context, session->sessionHandle);
    if (rc)
        LOG_ERROR("Tss2_Sys_FlushContext failed 0x%" PRIx32, rc);

    end_auth_session(session);

clean:
    req_auth.count = 1;
    req_auth.auths[0].sessionHandle = TPM2_RH_PW;

    rc2 = Tss2_Sys_NV_UndefineSpace(sys_context, TPM2_RH_OWNER,
                                    nv_index, &req_auth, 0);
    if (rc2)
        LOG_ERROR("Tss2_Sys_NV_UndefineSpace failed 0x%" PRIx32, rc);

    if (rc == 0)
        LOG_INFO("param-encrypt-decrypt test PASSED");

    return rc;
}
