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
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <openssl/rand.h>

#include "tss2_mu.h"
#include "tss2_sys.h"

#define LOGMODULE test
#include "util/log.h"
#include "test-esys.h"
#include "test.h"
#include "sys-util.h"

int
test_invoke (TSS2_SYS_CONTEXT *sys_context)
{
    TSS2_RC rc;
    TPM2B_ENCRYPTED_SECRET encrypted_salt = { 0 };
    TPMI_SH_AUTH_SESSION   session_handle = 0;
    TPMT_SYM_DEF           symmetric = { .algorithm = TPM2_ALG_NULL };
    TSS2L_SYS_AUTH_COMMAND cmd_auth = {
        .count = 1,
        .auths = {{
            .sessionHandle = TPM2_RH_PW,
        }},
    };
    TSS2L_SYS_AUTH_RESPONSE rsp_auth = { 0 };
    TPM2B_NONCE nonce_caller = {
        .size   = TPM2_SHA256_DIGEST_SIZE,
        .buffer = { 0 }
    };
    TPM2B_NONCE nonce_tpm = {
        .size   = TPM2_SHA256_DIGEST_SIZE,
        .buffer = { 0 }
    };

    /* First start a policy session */
    LOG_INFO("Calling StartAuthSession policy session");
    rc = Tss2_Sys_StartAuthSession (sys_context,
                                    TPM2_RH_NULL,     /* tpmKey */
                                    TPM2_RH_NULL,     /* bind */
                                    NULL,             /* cmdAuthsArray */
                                    &nonce_caller,    /* nonceCaller */
                                    &encrypted_salt,  /* encryptedSalt */
                                    TPM2_SE_POLICY,   /* sessionType */
                                    &symmetric,       /* symmetric */
                                    TPM2_ALG_SHA256,  /* authHash */
                                    &session_handle,  /* sessionHandle */
                                    &nonce_tpm,       /* nonceTPM */
                                    NULL              /* rspAuthsArray */
                                    );
    if (rc != TSS2_RC_SUCCESS) {
        LOG_ERROR("StartAuthSession failed: 0x%" PRIx32, rc);
        exit(1);
    }
    LOG_INFO("StartAuthSession TPM2_SE_POLICY success! Session handle: "
             "0x%" PRIx32, session_handle);

    /*
     * Then create an NV space where the digest required for PolicyAuthorizeNV
     * will be stored.
     */
    TPM2B_NV_PUBLIC nv_public = { 0 };
    TPM2B_AUTH  nv_auth = {
        .size = TPM2_SHA256_DIGEST_SIZE,
    };
    TPMI_RH_NV_INDEX nv_index = TPM2_HR_NV_INDEX | 0x01;

    nv_public.nvPublic.nvIndex = nv_index;
    nv_public.nvPublic.nameAlg = TPM2_ALG_SHA256;
    nv_public.nvPublic.attributes = TPMA_NV_PPREAD;
    nv_public.nvPublic.attributes |= TPMA_NV_PPWRITE;
    nv_public.nvPublic.attributes |= TPMA_NV_WRITE_STCLEAR;
    nv_public.nvPublic.attributes |= TPMA_NV_ORDERLY;
    nv_public.nvPublic.attributes |= TPMA_NV_OWNERREAD;
    nv_public.nvPublic.attributes |= TPMA_NV_OWNERWRITE;
    nv_public.nvPublic.authPolicy.size = 0;
    nv_public.nvPublic.dataSize = sizeof(TPMT_HA);
    cmd_auth.count = 1;
    cmd_auth.auths[0].sessionHandle = TPM2_RH_PW;
    cmd_auth.auths[0].hmac.size = 0;

    LOG_INFO("Calling NV_DefineSpace");
    rc = Tss2_Sys_NV_DefineSpace (sys_context,
                                  TPM2_RH_OWNER,
                                  &cmd_auth,
                                  &nv_auth,
                                  &nv_public,
                                  &rsp_auth);
    if (rc != TSS2_RC_SUCCESS) {
        LOG_ERROR("NV_DefineSpace failed: 0x%" PRIx32, rc);
        exit(1);
    }
    LOG_INFO("NV_DefineSpace success!, NV_index: 0x%x", nv_index);

    TPM2B_MAX_NV_BUFFER nv_data = { .size = 32 + 2, };
    rc = Tss2_MU_INT16_Marshal(TPM2_ALG_SHA256, nv_data.buffer,
                               TPM2_MAX_DIGEST_BUFFER, NULL);


    if (rc != TSS2_RC_SUCCESS) {
        LOG_ERROR("Tss2_MU_INT16_Marshal failed: 0x%" PRIx32, rc);
        exit(1);
    }

    /* Write the empty policy session to the NV index */
    LOG_INFO("Calling NV_Write");
    rc = Tss2_Sys_NV_Write(sys_context,
                           TPM2_RH_OWNER,
                           nv_index,
                           &cmd_auth,
                           &nv_data,
                           0,
                           &rsp_auth);
    if (rc != TPM2_RC_SUCCESS) {
        LOG_ERROR("Sys_NV_Write FAILED! Response Code : 0x%x", rc);
        exit(1);
    }
    LOG_INFO("Sys_NV_Write success!");

    /* Authorize the policy using the NV index */
    LOG_INFO("Calling PolicyAuthorizeNV");
    rc = Tss2_Sys_PolicyAuthorizeNV(sys_context,
                                    TPM2_RH_OWNER,
                                    nv_index,
                                    session_handle,
                                    &cmd_auth,
                                    &rsp_auth);
    if (rc != TPM2_RC_SUCCESS) {
        LOG_ERROR("PolicyAuthorizeNV FAILED! Response Code : 0x%x", rc);
        exit(1);
    }
    LOG_INFO("PolicyAuthorizeNV success!");

    /* Create a symmetric encryption key using the password session */
    TPM2B_SENSITIVE_CREATE  in_sensitive    = { 0 };
    TPMT_PUBLIC             in_public       = { 0 };
    TPM2B_TEMPLATE          public_template = { 0 };
    TPM2B_PRIVATE           out_private     = { 0 };
    TPM2B_PUBLIC            out_public      = { 0 };
    TPM2B_NAME              name            = TPM2B_NAME_INIT;
    TPM2_HANDLE             object_handle   = 0;

    /* Use precomputed authPolicy for simplicity */
    char auth[] = {0x06, 0x3a, 0x24, 0xdc, 0x2f, 0xc9, 0x32, 0xc3,
                   0xb8, 0xa0, 0x85, 0xca, 0x67, 0x27, 0x3c, 0x03,
                   0xa6, 0x7c, 0x11, 0x39, 0x8f, 0x2a, 0x4a, 0x13,
                   0xbd, 0x05, 0x37, 0xf8, 0x5f, 0x47, 0x56, 0xcb};
    memcpy(in_public.authPolicy.buffer, auth, TPM2_SHA256_DIGEST_SIZE);
    in_public.type = TPM2_ALG_SYMCIPHER;
    in_public.nameAlg = TPM2_ALG_SHA256;
    in_public.objectAttributes |= TPMA_OBJECT_USERWITHAUTH;
    in_public.objectAttributes |= TPMA_OBJECT_DECRYPT;
    in_public.objectAttributes |= TPMA_OBJECT_SIGN_ENCRYPT;
    in_public.objectAttributes |= TPMA_OBJECT_FIXEDTPM;
    in_public.objectAttributes |= TPMA_OBJECT_FIXEDPARENT;
    in_public.objectAttributes |= TPMA_OBJECT_SENSITIVEDATAORIGIN;
    in_public.parameters.symDetail.sym.algorithm = TPM2_ALG_AES;
    in_public.parameters.symDetail.sym.keyBits.sym = 128;
    in_public.parameters.symDetail.sym.mode.sym = TPM2_ALG_CFB;
    in_public.authPolicy.size = TPM2_SHA256_DIGEST_SIZE;

    uint8_t public_buf[sizeof(in_public)] = {0};
    size_t offset = 0;

    rc = Tss2_MU_TPMT_PUBLIC_Marshal(&in_public, public_buf,
                                     sizeof(in_public), &offset);
    if (rc != TPM2_RC_SUCCESS) {
        LOG_ERROR("Tss2_MU_TPMT_PUBLIC_Marshal FAILED! Response Code: 0x%x", rc);
        exit(1);
    }
    public_template.size = offset;
    memcpy(public_template.buffer, public_buf, offset);
    cmd_auth.count = 1;
    cmd_auth.auths[0].sessionHandle = TPM2_RH_PW;
    cmd_auth.auths[0].hmac.size = TPM2_SHA256_DIGEST_SIZE;

    /* Create a symmetric encryption key using the password session */
    LOG_INFO("Calling CreateLoaded");
    rc = Tss2_Sys_CreateLoaded (sys_context,
                                TPM2_RH_OWNER,
                                &cmd_auth,
                                &in_sensitive,
                                &public_template,
                                &object_handle,
                                &out_private,
                                &out_public,
                                &name,
                                &rsp_auth);
    if (rc != TPM2_RC_SUCCESS) {
        LOG_ERROR("CreateLoaded FAILED! Response Code: 0x%x", rc);
        exit(1);
    }
    LOG_INFO("success object handle: 0x%x", object_handle);

    TPM2B_MAX_BUFFER data_in = TPM2B_MAX_BUFFER_INIT;
    TPM2B_MAX_BUFFER data_out = TPM2B_MAX_BUFFER_INIT;
    TPM2B_IV iv_in = TPM2B_IV_INIT;
    TPM2B_IV iv_out = TPM2B_IV_INIT;

    if (RAND_bytes(data_in.buffer, TPM2_MAX_DIGEST_BUFFER) != 1) {
        LOG_ERROR("RAND_bytes FAILED!");
        exit(1);
    }

    /* Call encrypt using the key object using the password session */
    LOG_INFO("Calling EncryptDecrypt using password session 0x%x", TPM2_RH_PW);
    LOGBLOB_DEBUG(data_in.buffer, 32, "%s", "First 32 bytes of plain text:");
    rc = TSS2_RETRY_EXP(Tss2_Sys_EncryptDecrypt (sys_context,
                                                 object_handle,
                                                 &cmd_auth,
                                                 NO, /* encrypt */
                                                 TPM2_ALG_NULL,
                                                 &iv_in,
                                                 &data_in,
                                                 &data_out,
                                                 &iv_out,
                                                 &rsp_auth));
    if (rc == TPM2_RC_COMMAND_CODE) {
        LOG_WARNING("Encrypt/Decrypt not supported by TPM");
        rc = Tss2_Sys_NV_UndefineSpace(sys_context,
                                       TPM2_RH_OWNER,
                                       nv_index,
                                       &cmd_auth,
                                       &rsp_auth);
        if (rc != TSS2_RC_SUCCESS) {
            LOG_ERROR("Tss2_Sys_NV_UndefineSpace failed: 0x%"PRIx32, rc);
            return 99; /* fatal error */
        }
        rc = Tss2_Sys_FlushContext(sys_context, object_handle);
        if (rc != TSS2_RC_SUCCESS) {
            LOG_ERROR("Tss2_Sys_FlushContext failed with 0x%"PRIx32, rc);
            return 99; /* fatal error */
        }
        rc = Tss2_Sys_FlushContext(sys_context, session_handle);
        if (rc != TSS2_RC_SUCCESS) {
            LOG_ERROR("Tss2_Sys_FlushContext failed with 0x%"PRIx32, rc);
            return 99; /* fatal error */
        }
        return EXIT_SKIP;
    }

    if (rc != TPM2_RC_SUCCESS) {
        LOG_ERROR("EncryptDecrypt FAILED! Response Code : 0x%x", rc);
        exit(1);
    }
    LOG_INFO("EncryptDecrypt success!");

    LOGBLOB_DEBUG(data_out.buffer, 32, "%s", "First 32 bytes of cypher text:");

    cmd_auth.auths[0].sessionAttributes |= TPMA_SESSION_CONTINUESESSION;
    cmd_auth.auths[0].sessionHandle = session_handle;
    cmd_auth.auths[0].hmac.size = 0;
    memset(data_out.buffer, '\0', TPM2_MAX_DIGEST_BUFFER);

    /* Call encrypt using the key object using the policy session
     * This should pass because we allowed it with the PolicyAuthorizeNV call */
    LOG_INFO("Calling EncryptDecrypt using policy session 0x%x", session_handle);
    rc = TSS2_RETRY_EXP(Tss2_Sys_EncryptDecrypt (sys_context,
                                                 object_handle,
                                                 &cmd_auth,
                                                 NO, /* encrypt */
                                                 TPM2_ALG_NULL,
                                                 &iv_in,
                                                 &data_in,
                                                 &data_out,
                                                 &iv_out,
                                                 &rsp_auth));
    if (rc != TPM2_RC_SUCCESS) {
        LOG_INFO("EncryptDecrypt Failed rc: 0x%x", rc);
        exit(1);
    }
    LOG_INFO("EncryptDecrypt success!");

    cmd_auth.auths[0].sessionHandle = TPM2_RH_PW;
    cmd_auth.auths[0].hmac.size = 0;

    /* Kill the NV index - this should invalidate the policy */
    rc = Tss2_Sys_NV_UndefineSpace(sys_context,
                                   TPM2_RH_OWNER,
                                   nv_index,
                                   &cmd_auth,
                                   &rsp_auth);
    if (rc != TSS2_RC_SUCCESS) {
        LOG_ERROR("Tss2_Sys_NV_UndefineSpace failed: 0x%" PRIx32, rc);
        exit(1);
    }
    LOG_INFO("Tss2_Sys_NV_UndefineSpace for NV index 0x%" PRIx32 " success!",
             nv_index);

    /* Call encrypt using the key object using the policy session again.
     * This should fail because the NV index is destroyed */
    cmd_auth.auths[0].sessionHandle = session_handle;
    memset(data_out.buffer, '\0', TPM2_MAX_DIGEST_BUFFER);
    LOG_INFO("Calling EncryptDecrypt again with policy session after destroying"
             " the NV index This should fail with RC_POLICY_FAIL");
    rc = TSS2_RETRY_EXP(Tss2_Sys_EncryptDecrypt(sys_context,
                                                object_handle,
                                                &cmd_auth,
                                                NO, /* encrypt */
                                                TPM2_ALG_NULL,
                                                &iv_in,
                                                &data_in,
                                                &data_out,
                                                &iv_out,
                                                &rsp_auth));
    if (rc != TPM2_RC_1 + TPM2_RC_S + TPM2_RC_POLICY_FAIL) {
        LOG_INFO("EncryptDecrypt passes unexpectedly rc: 0x%x", rc);
        exit(1);
    }
    LOG_INFO("EncryptDecrypt failed as expected!");

    /* Clean up the session and key*/
    rc = Tss2_Sys_FlushContext (sys_context, object_handle);
    if (rc != TSS2_RC_SUCCESS) {
        LOG_ERROR("Tss2_Sys_FlushContext failed: 0x%" PRIx32, rc);
        exit(1);
    }
    LOG_INFO("Flushed context for object handle: 0x%" PRIx32 " success!",
               object_handle);

    rc = Tss2_Sys_FlushContext (sys_context, session_handle);
    if (rc != TSS2_RC_SUCCESS) {
        LOG_ERROR("Tss2_Sys_FlushContext failed: 0x%" PRIx32, rc);
        exit(1);
    }
    LOG_INFO("Flushed context for session handle: 0x%" PRIx32 " success!",
               session_handle);

    return 0;
}
