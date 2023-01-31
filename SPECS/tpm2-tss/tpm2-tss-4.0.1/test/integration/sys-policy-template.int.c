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

#include "tss2_mu.h"
#include "tss2_sys.h"

#define LOGMODULE test
#include "util/log.h"
#include "test.h"
#include "sys-util.h"

int
test_invoke (TSS2_SYS_CONTEXT *sys_context)
{
    TSS2_RC rc;
    TPM2B_SENSITIVE_CREATE  in_sensitive    = { 0 };
    TPM2B_PUBLIC            in_public       = { 0 };
    TPM2B_DATA              outside_info    = { 0 };
    TPML_PCR_SELECTION      creation_pcr    = { 0 };
    TPM2B_PUBLIC            out_public      = { 0 };
    TPM2B_CREATION_DATA     creation_data   = { 0 };
    TPM2B_DIGEST            creation_hash   = TPM2B_DIGEST_INIT;
    TPMT_TK_CREATION        creation_ticket = { 0 };
    TPM2B_NAME              name            = TPM2B_NAME_INIT;
    TPM2B_NONCE             nonce_caller = {
        .size   = TPM2_SHA256_DIGEST_SIZE,
        .buffer = { 0 }
    };
    TPM2B_NONCE nonce_tpm = {
        .size   = TPM2_SHA256_DIGEST_SIZE,
        .buffer = { 0 }
    };

    TPM2B_ENCRYPTED_SECRET encrypted_salt = { 0 };
    TPMI_SH_AUTH_SESSION   session_handle = 0;
    TPMT_SYM_DEF           symmetric      = { .algorithm = TPM2_ALG_NULL };
    TPM2B_DIGEST templ_dgst = { 0 };
    TPM2_HANDLE object_handle = 0;
    TSS2L_SYS_AUTH_COMMAND cmd_auth = { 0 };
    TSS2L_SYS_AUTH_RESPONSE rsp_auth = { 0 };
    TPM2B_DIGEST policy_digest;
    size_t template_size = 0;
    uint8_t tmp_buff[sizeof(in_public)] = { 0 };
    static uint8_t auth[32];

    memset(auth, 's', 32);

    LOG_INFO("StartAuthSession for TPM2_SE_POLICY (policy session)");
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
        LOG_ERROR("Tss2_Sys_StartAuthSession failed: 0x%" PRIx32, rc);
        exit(1);
    }
    LOG_INFO("StartAuthSession for TPM2_SE_POLICY success! Session handle: "
             "0x%" PRIx32, session_handle);

    in_public.publicArea.type = TPM2_ALG_RSA;
    in_public.publicArea.nameAlg = TPM2_ALG_SHA256;
    in_public.publicArea.objectAttributes = TPMA_OBJECT_RESTRICTED;
    in_public.publicArea.objectAttributes |= TPMA_OBJECT_USERWITHAUTH;
    in_public.publicArea.objectAttributes |= TPMA_OBJECT_DECRYPT;
    in_public.publicArea.objectAttributes |= TPMA_OBJECT_FIXEDTPM;
    in_public.publicArea.objectAttributes |= TPMA_OBJECT_FIXEDPARENT;
    in_public.publicArea.objectAttributes |= TPMA_OBJECT_SENSITIVEDATAORIGIN;
    in_public.publicArea.parameters.rsaDetail.symmetric.algorithm = TPM2_ALG_AES;
    in_public.publicArea.parameters.rsaDetail.symmetric.keyBits.aes = 128;
    in_public.publicArea.parameters.rsaDetail.symmetric.mode.aes = TPM2_ALG_CFB;
    in_public.publicArea.parameters.rsaDetail.scheme.scheme = TPM2_ALG_NULL;
    in_public.publicArea.parameters.rsaDetail.keyBits = 2048;

    in_public.publicArea.authPolicy.size = sizeof(auth);
    memcpy(in_public.publicArea.authPolicy.buffer, auth, sizeof(auth));

    cmd_auth.auths[0].sessionHandle = session_handle;
    cmd_auth.auths[0].sessionAttributes |= TPMA_SESSION_CONTINUESESSION;
    cmd_auth.auths[0].hmac.size = sizeof(auth);
    memcpy(cmd_auth.auths[0].hmac.buffer, auth, sizeof(auth));

    /* Calculate the digest of the public param template */
    rc = Tss2_MU_TPM2B_PUBLIC_Marshal(&in_public, tmp_buff,
                                      sizeof(in_public), &template_size);
    if (rc != TSS2_RC_SUCCESS) {
        LOG_ERROR("Marshal in_public failed");
        exit(1);
    }

    LOG_INFO("Calculating template digest size of in_public: %d", (int)template_size - 2);

    rc = hash(in_public.publicArea.nameAlg, tmp_buff + 2,
              template_size - 2, &templ_dgst);


    if (rc != TSS2_RC_SUCCESS) {
        LOG_ERROR("Failed calculating template hash");
        exit(1);
    }
    LOGBLOB_DEBUG(tmp_buff + 2, template_size - 2, "%s", "in_public:");
    LOGBLOB_DEBUG(templ_dgst.buffer, templ_dgst.size, "%s", "template digest:");

    /* Set the template digest on the session.
     * After that all objects created for this session will be limited
     * to this particular template
     */
    LOG_INFO("Calling Tss2_Sys_PolicyTemplate");
    rc = Tss2_Sys_PolicyTemplate (sys_context,
                                  session_handle,
                                  NULL,
                                  &templ_dgst,
                                  NULL);
    if (rc != TSS2_RC_SUCCESS) {
        LOG_ERROR("Tss2_Sys_PolicyTemplate failed: 0x%" PRIx32, rc);
        exit(1);
    }

    /* Need to set the policy auth value */
    rc = Tss2_Sys_PolicyGetDigest(sys_context, session_handle,
                                  0, &policy_digest, 0);

    if (rc != TSS2_RC_SUCCESS) {
        LOG_ERROR("Tss2_Sys_PolicyGetDigest failed: 0x%" PRIx32, rc);
        exit(1);
    }

    LOGBLOB_DEBUG(policy_digest.buffer, policy_digest.size, "%s", "policy digest:");

    cmd_auth.count = 1;
    cmd_auth.auths[0].sessionHandle = TPM2_RH_PW;
    cmd_auth.auths[0].nonce.size = 0;
    cmd_auth.auths[0].hmac.size = 0;

    rc = Tss2_Sys_SetPrimaryPolicy(sys_context,
                                   TPM2_RH_OWNER,
                                   &cmd_auth,
                                   &policy_digest,
                                   TPM2_ALG_SHA256,
                                   &rsp_auth);
    if (rc == TPM2_RC_SUCCESS) {
        LOG_INFO("Tss2_Sys_SetPrimaryPolicy success");
    } else {
        LOG_ERROR("Tss2_Sys_SetPrimaryPolicy FAILED! Response Code : 0x%x", rc);
        exit(1);
    }

    cmd_auth.auths[0].sessionHandle = session_handle;
    cmd_auth.auths[0].sessionAttributes |= TPMA_SESSION_CONTINUESESSION;

    /* Create an object using the valid template */
    LOG_INFO("Creating an object using a correct template");
    rc = Tss2_Sys_CreatePrimary (sys_context,
                                 TPM2_RH_OWNER,
                                 &cmd_auth,
                                 &in_sensitive,
                                 &in_public,
                                 &outside_info,
                                 &creation_pcr,
                                 &object_handle,
                                 &out_public,
                                 &creation_data,
                                 &creation_hash,
                                 &creation_ticket,
                                 &name,
                                 &rsp_auth
                                 );

    if (rc == TPM2_RC_SUCCESS) {
        LOG_INFO("Creating object: 0x%" PRIx32 " success", object_handle);
    } else {
        LOG_ERROR("CreatePrimary FAILED! Response Code : 0x%x", rc);
        exit(1);
    }

    rc = Tss2_Sys_FlushContext(sys_context, object_handle);
    if (rc != TSS2_RC_SUCCESS) {
        LOG_ERROR("Tss2_Sys_FlushContext failed with 0x%"PRIx32, rc);
        return 99; /* fatal error */
    }

    object_handle = 0;
    TPM2B_DATA              outside_info2    = { 0 };
    TPML_PCR_SELECTION      creation_pcr2    = { 0 };
    TPM2B_PUBLIC            out_public2      = { 0 };
    TPM2B_CREATION_DATA     creation_data2   = { 0 };
    TPM2B_DIGEST            creation_hash2   = TPM2B_DIGEST_INIT;
    TPMT_TK_CREATION        creation_ticket2 = { 0 };
    TPM2B_NAME              name2            = TPM2B_NAME_INIT;

    /* Changing the template value */
    in_public.publicArea.parameters.rsaDetail.symmetric.keyBits.aes = 256;

    /* Create an object using an invalid template. This should fail */
    LOG_INFO("Creating an object using an incorrect template");
    rc = Tss2_Sys_CreatePrimary (sys_context,
                                 TPM2_RH_OWNER,
                                 &cmd_auth,
                                 &in_sensitive,
                                 &in_public,
                                 &outside_info2,
                                 &creation_pcr2,
                                 &object_handle,
                                 &out_public2,
                                 &creation_data2,
                                 &creation_hash2,
                                 &creation_ticket2,
                                 &name2,
                                 &rsp_auth
                                 );
    if (rc != TPM2_RC_1 + TPM2_RC_S + TPM2_RC_POLICY_FAIL) {
        LOG_ERROR("Error: CreatePrimary with invalid template succeeded!"
                  "Response Code: 0x%x expected: 0x%x", rc,
                  TPM2_RC_1 + TPM2_RC_S + TPM2_RC_POLICY_FAIL);
        exit(1);
    }

    rc = Tss2_Sys_FlushContext (sys_context, session_handle);
    if (rc != TSS2_RC_SUCCESS) {
        LOG_ERROR("Tss2_Sys_FlushContext failed: 0x%" PRIx32, rc);
        exit(1);
    }
    LOG_INFO("Flushed context for session handle: 0x%" PRIx32 " success!",
               session_handle);
    return 0;
}
