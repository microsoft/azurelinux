/* SPDX-License-Identifier: BSD-2-Clause */
/*******************************************************************************
 * Copyright 2017-2018, Fraunhofer SIT sponsored by Infineon Technologies AG
 * All rights reserved.
 *******************************************************************************/

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <errno.h>
#include <fcntl.h>
#include <unistd.h>

#include <openssl/evp.h>
#include <openssl/hmac.h>
#include <openssl/engine.h>
#include <openssl/pem.h>

#include "tss2_fapi.h"

#include "test-fapi.h"
#define LOGMODULE test
#include "util/log.h"
#include "util/aux_util.h"


char *userDataTest = "test";

#define chknull(X) if (!X) { LOG_ERROR(str(X) "should not be null"); \
                             r = TSS2_FAPI_RC_GENERAL_FAILURE; \
                             goto error_cleanup; }

static uint8_t *global_signature = NULL;
static char* hmac_key = "secret";
static int hmac_key_size = 7;

static TSS2_RC
signatureCallback(
    char    const  *objectPath,
    char    const  *description,
    char    const  *publicKey,
    char    const  *publicKeyHint,
    uint32_t        hashAlg,
    uint8_t const  *dataToSign,
    size_t          dataToSignSize,
    uint8_t const **signature,
    size_t         *signatureSize,
    void           *userData)
{
    uint8_t *aux_signature = NULL;
    UNUSED(description);
    UNUSED(publicKey);
    UNUSED(publicKeyHint);
    const EVP_MD* md = NULL;
    TSS2_RC r;
    unsigned char hash[SHA512_DIGEST_LENGTH];
    size_t hash_size;
    EVP_MD_CTX *sha_ctx = NULL;
#if OPENSSL_VERSION_NUMBER >= 0x30000000L
    EVP_MAC *mac = NULL;
    EVP_MAC_CTX *mac_ctx = NULL;
#else
    HMAC_CTX *hmac_ctx = NULL;
#endif
    char *sha;

    if (!objectPath) {
        return_error(TSS2_FAPI_RC_BAD_VALUE, "No path.");
    }

    if (userData != userDataTest) {
        LOG_ERROR("userData is not correct, %p != %p", userData, userDataTest);
        return TSS2_FAPI_RC_GENERAL_FAILURE;
    }

    switch (hashAlg) {
    case TPM2_ALG_SHA1:
        md = EVP_sha1();
        sha = "SHA1";
        hash_size = 32;
        break;
    case TPM2_ALG_SHA256:
        md = EVP_sha256();
        sha = "SHA256";
        hash_size = 32;
        break;
    case TPM2_ALG_SHA384:
        md = EVP_sha384();
        sha = "SHA384";
        hash_size = 48;
        break;
    case TPM2_ALG_SHA512:
        md = EVP_sha512();
        sha = "SHA512";
        hash_size = 64;
        break;
    default:
        LOG_ERROR("Unsupported hash algorithm (%"PRIu16")", hashAlg);
        return TSS2_ESYS_RC_BAD_VALUE;
    }

    *signatureSize = hash_size;

    sha_ctx =  EVP_MD_CTX_new();
    return_if_null(sha_ctx, "Out of memory.", TSS2_FAPI_RC_MEMORY);

    if (!EVP_DigestInit(sha_ctx, md) ||
        !EVP_DigestUpdate(sha_ctx, dataToSign, dataToSignSize) ||
        !EVP_DigestFinal(sha_ctx, hash, NULL)) {
        goto_error(r, TSS2_FAPI_RC_GENERAL_FAILURE, "EVP_DigestFinal",
                   error_cleanup);
    }

    EVP_MD_CTX_free(sha_ctx);

    aux_signature = malloc(*signatureSize);
    goto_if_null(aux_signature, "Out of memory.", TSS2_FAPI_RC_MEMORY, error_cleanup);

    global_signature = aux_signature;

#if OPENSSL_VERSION_NUMBER >= 0x30000000L
    OSSL_PARAM params[2];
    mac = EVP_MAC_fetch(NULL, "HMAC", NULL);
    mac_ctx = EVP_MAC_CTX_new(mac);
    goto_if_null(mac_ctx, "Out of memory", TSS2_FAPI_RC_MEMORY, error_cleanup);
    EVP_MAC_free(mac);
    mac = NULL;
    params[0] = OSSL_PARAM_construct_utf8_string("digest", sha, 0);
    params[1] = OSSL_PARAM_construct_end();
    if (!EVP_MAC_init(mac_ctx, (unsigned char *)hmac_key, hmac_key_size, params) ||
        !EVP_MAC_update(mac_ctx, hash, hash_size) ||
        !EVP_MAC_final(mac_ctx, (unsigned char *)aux_signature,  signatureSize, hash_size)) {
        goto_error(r, TSS2_FAPI_RC_GENERAL_FAILURE, "EVP hmac error", error_cleanup);
    }
    EVP_MAC_CTX_free(mac_ctx);
#else
    UNUSED(sha);
    hmac_ctx = HMAC_CTX_new();
    if (!hmac_ctx ||
        !HMAC_Init_ex(hmac_ctx, hmac_key, hmac_key_size, md, NULL) ||
        !HMAC_Update(hmac_ctx, hash, hash_size) ||
        !HMAC_Final(hmac_ctx, aux_signature, (unsigned int *)signatureSize)) {
        goto_error(r, TSS2_FAPI_RC_GENERAL_FAILURE, "HMAC error.",
                   error_cleanup);
    }
    HMAC_CTX_free(hmac_ctx);
#endif

    *signature = aux_signature;
    return TSS2_RC_SUCCESS;

 error_cleanup:
     if (sha_ctx)
         EVP_MD_CTX_free(sha_ctx);
#if OPENSSL_VERSION_NUMBER >= 0x30000000L
     if (mac)
         EVP_MAC_free(mac);
     if (mac_ctx)
         EVP_MAC_CTX_free(mac_ctx);
#else
     if(hmac_ctx)
         HMAC_CTX_free(hmac_ctx);
#endif
    if (signature)
        SAFE_FREE(signature);
    return r;
}

#define PASSWORD NULL

#define SIGN_TEMPLATE  "sign,noDa"

/** Test the FAPI functions for key creation and usage with a PolicySigned.
 *
 * Tested FAPI commands:
 *  - Fapi_Provision()
 *  - Fapi_Import()
 *  - Fapi_CreateKey()
 *  - Fapi_SetSignCB()
 *  - Fapi_Sign()
 *  - Fapi_Delete()
 *  - Fapi_List()
 *
 * Tested Policies:
 *  - PolicySigned
 *
 * @param[in,out] context The FAPI_CONTEXT.
 * @retval EXIT_FAILURE
 * @retval EXIT_SUCCESS
 */
int
test_fapi_key_create_policy_signed(FAPI_CONTEXT *context)
{
    TSS2_RC r;
    char *policy_name = "/policy/pol_signed_keyedhash";
    char *policy_file = TOP_SOURCEDIR "/test/data/fapi/policy/pol_signed_keyedhash.json";
    FILE *stream = NULL;
    char *json_policy = NULL;
    long policy_size;

    uint8_t *signature = NULL;
    char    *publicKey = NULL;
    char    *certificate = NULL;

    r = Fapi_Provision(context, NULL, NULL, NULL);
    goto_if_error(r, "Error Fapi_Provision", error);

    r = pcr_reset(context, 16);
    goto_if_error(r, "Error pcr_reset", error);

    stream = fopen(policy_file, "r");
    if (!stream) {
        LOG_ERROR("File %s does not exist", policy_file);
        goto error;
    }
    fseek(stream, 0L, SEEK_END);
    policy_size = ftell(stream);
    fclose(stream);
    json_policy = malloc(policy_size + 1);
    goto_if_null(json_policy,
                 "Could not allocate memory for the JSON policy",
                 TSS2_FAPI_RC_MEMORY, error);
    stream = fopen(policy_file, "r");
    ssize_t ret = read(fileno(stream), json_policy, policy_size);
    if (ret != policy_size) {
        LOG_ERROR("IO error %s.", policy_file);
        goto error;
    }
    json_policy[policy_size] = '\0';

    r = Fapi_Import(context, policy_name, json_policy);
    goto_if_error(r, "Error Fapi_Import", error);

    r = Fapi_CreateSeal(context, "/SRK/sym_sign_key", SIGN_TEMPLATE,
                        hmac_key_size, NULL, NULL, (uint8_t *)hmac_key);
    goto_if_error(r, "Error Fapi_CreateSeal", error);


    r = Fapi_CreateKey(context, "/HS/SRK/mySignKey", SIGN_TEMPLATE,
                       policy_name, PASSWORD);
    goto_if_error(r, "Error Fapi_CreateKey", error);

    r = Fapi_SetCertificate(context, "HS/SRK/mySignKey", "-----BEGIN "\
        "CERTIFICATE-----[...]-----END CERTIFICATE-----");
    goto_if_error(r, "Error Fapi_CreateKey", error);

    size_t signatureSize = 0;

    TPM2B_DIGEST digest = {
        .size = 20,
        .buffer = {
            0x67, 0x68, 0x03, 0x3e, 0x21, 0x64, 0x68, 0x24, 0x7b, 0xd0,
            0x31, 0xa0, 0xa2, 0xd9, 0x87, 0x6d, 0x79, 0x81, 0x8f, 0x8f
        }
    };

    r = Fapi_SetSignCB(context, signatureCallback, userDataTest);
    goto_if_error(r, "Error SetPolicySignatureCallback", error);

    r = Fapi_Sign(context, "/HS/SRK/mySignKey", NULL,
                  &digest.buffer[0], digest.size, &signature, &signatureSize,
                  &publicKey, &certificate);
    goto_if_error(r, "Error Fapi_Sign", error);
    ASSERT(signature != NULL);
    ASSERT(publicKey != NULL);
    ASSERT(certificate != NULL);
    ASSERT(strstr(publicKey, "BEGIN PUBLIC KEY"));
    ASSERT(strstr(certificate, "BEGIN CERTIFICATE"));

    r = Fapi_Delete(context, "/");
    goto_if_error(r, "Error Fapi_Delete", error);

    fclose(stream);
    SAFE_FREE(publicKey);
    SAFE_FREE(json_policy);
    SAFE_FREE(signature);
    SAFE_FREE(certificate);
    SAFE_FREE(global_signature);
    return EXIT_SUCCESS;

error:
    Fapi_Delete(context, "/");
    SAFE_FREE(publicKey);
    SAFE_FREE(json_policy);
    SAFE_FREE(signature);
    SAFE_FREE(certificate);
    SAFE_FREE(global_signature);
    return EXIT_FAILURE;
}

int
test_invoke_fapi(FAPI_CONTEXT *fapi_context)
{
    return test_fapi_key_create_policy_signed(fapi_context);
}
