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

#include "tss2_tcti.h"
#include "tss2_sys.h"

#define LOGMODULE test
#include "util/log.h"
#include "test.h"
#include "sys-util.h"
/**
 * This program contains integration test for asymmetric encrypt and
 * decrypt use case that has SYSs Tss2_Sys_CreatePrimary,
 * Tss2_Sys_Create, Tss2_Sys_Load, Tss2_Sys_RSA_Encrypt and
 * Tss2_Sys_RSA_Decrypt. First, the program creates the object and load
 * it in TPM. Then, it performs encryption based on the loaded
 * object. The object will be verified if it is encrypted.
 * If the verification is passed, it performs decryption and the
 * program will check if the decrypted value is the same as
 * the value before encryption.
 */
int
test_invoke (TSS2_SYS_CONTEXT *sys_context)
{
    TSS2_RC rc;
    TPM2B_SENSITIVE_CREATE  in_sensitive;
    TPM2B_PUBLIC            in_public = {0};
    TPM2B_DATA              outside_info = {0,};
    TPML_PCR_SELECTION      creation_pcr;
    TPM2B_NAME name = {sizeof(TPM2B_NAME)-2,};
    TPM2B_PRIVATE out_private = {sizeof(TPM2B_PRIVATE)-2,};
    TPM2B_PUBLIC out_public = {0,};
    TPM2B_CREATION_DATA creation_data = {0,};
    TPM2B_DIGEST creation_hash = {sizeof(TPM2B_DIGEST)-2,};
    TPMT_TK_CREATION creation_ticket = {0,};
    TPM2_HANDLE loaded_sym_handle;
    TPM2_HANDLE sym_handle;
    const char message[] = "my message";
    TPMT_RSA_DECRYPT in_scheme;
    TPM2B_PUBLIC_KEY_RSA input_message = {sizeof(TPM2B_PUBLIC_KEY_RSA)-2,};
    TPM2B_PUBLIC_KEY_RSA output_message = {sizeof(TPM2B_PUBLIC_KEY_RSA)-2,};
    TPM2B_PUBLIC_KEY_RSA output_data = {sizeof(TPM2B_PUBLIC_KEY_RSA)-2,};

    TSS2L_SYS_AUTH_RESPONSE sessions_data_out;
    TSS2L_SYS_AUTH_COMMAND sessions_data = {
        .count = 1,
        .auths = {{.sessionHandle = TPM2_RH_PW,
            .nonce={.size=0},
            .hmac={.size=0}}}};

    in_sensitive.size = 0;
    in_sensitive.sensitive.userAuth.size = 0;
    in_sensitive.sensitive.data.size = 0;

    in_public.publicArea.type = TPM2_ALG_RSA;
    in_public.publicArea.nameAlg = TPM2_ALG_SHA256;
    *(UINT32 *)&(in_public.publicArea.objectAttributes) = 0;
    in_public.publicArea.objectAttributes |= TPMA_OBJECT_RESTRICTED;
    in_public.publicArea.objectAttributes |= TPMA_OBJECT_USERWITHAUTH;
    in_public.publicArea.objectAttributes |= TPMA_OBJECT_DECRYPT;
    in_public.publicArea.objectAttributes |= TPMA_OBJECT_FIXEDTPM;
    in_public.publicArea.objectAttributes |= TPMA_OBJECT_FIXEDPARENT;
    in_public.publicArea.objectAttributes |= TPMA_OBJECT_SENSITIVEDATAORIGIN;

    in_public.publicArea.authPolicy.size = 0;

    in_public.publicArea.parameters.rsaDetail.symmetric.algorithm = TPM2_ALG_AES;
    in_public.publicArea.parameters.rsaDetail.symmetric.keyBits.aes = 128;
    in_public.publicArea.parameters.rsaDetail.symmetric.mode.aes = TPM2_ALG_CFB;
    in_public.publicArea.parameters.rsaDetail.scheme.scheme = TPM2_ALG_NULL;
    in_public.publicArea.parameters.rsaDetail.keyBits = 2048;
    in_public.publicArea.parameters.rsaDetail.exponent = 0;

    in_public.publicArea.unique.rsa.size = 0;

    outside_info.size = 0;
    creation_pcr.count = 0;
    out_public.size = 0;
    creation_data.size = 0;

    LOG_INFO("Asymmetric Encryption and Decryption Tests started.");
    rc = Tss2_Sys_CreatePrimary(sys_context, TPM2_RH_OWNER, &sessions_data, &in_sensitive, &in_public, &outside_info, &creation_pcr, &sym_handle, &out_public, &creation_data, &creation_hash, &creation_ticket, &name, &sessions_data_out);
    if (rc != TPM2_RC_SUCCESS) {
        LOG_ERROR("CreatePrimary FAILED! Response Code : 0x%x", rc);
        exit(1);
    }
    LOG_INFO("New key successfully created.  Handle: 0x%8.8x", sym_handle);

    in_public.publicArea.type = TPM2_ALG_RSA;
    in_public.publicArea.parameters.rsaDetail.symmetric.algorithm = TPM2_ALG_NULL;
    in_public.publicArea.parameters.rsaDetail.scheme.scheme = TPM2_ALG_NULL;
    in_public.publicArea.parameters.rsaDetail.keyBits = 2048;
    in_public.publicArea.parameters.rsaDetail.exponent = 0;
    in_public.publicArea.unique.rsa.size = 0;

    /* First clear attributes bit field. */
    *(UINT32 *)&(in_public.publicArea.objectAttributes) = 0;
    in_public.publicArea.objectAttributes &= ~TPMA_OBJECT_RESTRICTED;
    in_public.publicArea.objectAttributes |= TPMA_OBJECT_USERWITHAUTH;
    in_public.publicArea.objectAttributes |= TPMA_OBJECT_DECRYPT;
    in_public.publicArea.objectAttributes |= TPMA_OBJECT_SIGN_ENCRYPT;
    in_public.publicArea.objectAttributes |= TPMA_OBJECT_FIXEDTPM;
    in_public.publicArea.objectAttributes |= TPMA_OBJECT_FIXEDPARENT;
    in_public.publicArea.objectAttributes |= TPMA_OBJECT_SENSITIVEDATAORIGIN;

    outside_info.size = 0;
    out_public.size = 0;
    creation_data.size = 0;
    sessions_data.auths[0].hmac.size = 0;

    rc = TSS2_RETRY_EXP (Tss2_Sys_Create(sys_context, sym_handle, &sessions_data, &in_sensitive, &in_public, &outside_info, &creation_pcr, &out_private, &out_public, &creation_data, &creation_hash, &creation_ticket, &sessions_data_out));
    if (rc != TPM2_RC_SUCCESS) {
        LOG_ERROR("Create FAILED! Response Code : 0x%x", rc);
        exit(1);
    }
    rc = Tss2_Sys_Load(sys_context, sym_handle, &sessions_data, &out_private, &out_public, &loaded_sym_handle, &name, &sessions_data_out);
    if (rc != TPM2_RC_SUCCESS) {
        LOG_ERROR("Load FAILED! Response Code : 0x%x", rc);
        exit(1);
    }
    LOG_INFO( "Loaded key handle:  %8.8x", loaded_sym_handle );

    input_message.size = strlen(message);
    memcpy(input_message.buffer, message, input_message.size);
    in_scheme.scheme = TPM2_ALG_RSAES;
    outside_info.size = 0;
    rc = Tss2_Sys_RSA_Encrypt(sys_context, loaded_sym_handle, 0, &input_message, &in_scheme, &outside_info, &output_data, 0);
    if(rc != TPM2_RC_SUCCESS) {
        LOG_ERROR("RSA_Encrypt FAILED! Response Code : 0x%x", rc);
        exit(1);
    }
    LOG_INFO("Encrypt successful.");

    rc = Tss2_Sys_RSA_Decrypt(sys_context, loaded_sym_handle, &sessions_data, &output_data, &in_scheme, &outside_info, &output_message, &sessions_data_out);
    if(rc != TPM2_RC_SUCCESS) {
        LOG_ERROR("RSA_Decrypt FAILED! Response Code : 0x%x", rc);
        exit(1);
    }
    LOG_INFO("Decrypt successful.");

    LOG_INFO("Asymmetric Encryption and Decryption Test Passed!");

    rc = Tss2_Sys_FlushContext(sys_context, sym_handle);
    if (rc != TSS2_RC_SUCCESS) {
        LOG_ERROR("Tss2_Sys_FlushContext failed with 0x%"PRIx32, rc);
        return 99; /* fatal error */
    }
    rc = Tss2_Sys_FlushContext(sys_context, loaded_sym_handle);
    if (rc != TSS2_RC_SUCCESS) {
        LOG_ERROR("Tss2_Sys_FlushContext failed with 0x%"PRIx32, rc);
        return 99; /* fatal error */
    }
    return 0;
}
