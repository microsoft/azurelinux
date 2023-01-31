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
#include <unistd.h>

#include <openssl/evp.h>
#include <openssl/rsa.h>
#include <openssl/engine.h>
#include <openssl/pem.h>

#include "tss2_fapi.h"

#include "test-fapi.h"

#define LOGMODULE test
#include "util/log.h"
#include "util/aux_util.h"

#define SIZE 128

const char *priv_pem =
    "-----BEGIN PRIVATE KEY-----\n"
    "MIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQCgYvoisJIDOeYg\n"
    "jMF6ywiZbu085TLvy5ZMhq5vfYqdgefvwpemutnfKSnpYOs5B4yO/gAD7XiYluDv\n"
    "tqlVhfISeQV04xrWGzNImenpwm/HsgueAu8VTHNtWSL96G+BLedGTrs2NqX6cxN7\n"
    "yGl7dQpB5X8iP4XSvpjP3Vb7gs+adwCJR6xFkt60jYFmwrAdhEzOeakhimi5rU21\n"
    "LxCkRdEyaxS57X15L9dEA+aYJ+dvkFfZOfTqIKmTrA75F8yj161xflwtIC4hgRBg\n"
    "K9Xb/RdN8TDrTu+20E3RjngutU4qejW9Fd3mzHJGV8HRYvjYXhUblN9wmjm7Veru\n"
    "T2b0rnvzAgMBAAECggEBAIwHvoJ5DRJ6A50Zp3dROxHTEphfOEi6xF/OGxBGWLbK\n"
    "C7l+eS9d5gj8BJa5QsXI/IR/6X2EYQ1AdeV04oVD7CUKuqPiALU8jFrv3pV0aGm+\n"
    "3nu37gv3crPe5jkvLeNoM4tkA/oCXom63SDuyoG6nxkHiSdatLlaJUse4em3vRAL\n"
    "QivziZIMyswcleMe0xAoMi7LO+nUFFxBS8/xGya0vsU0dsMQEl1SRITv1VCXmPQD\n"
    "T4dEI4+1cufv6Ax0EDbFKmnjyiGTjOeQKrGIqETUSQolbg5PgL1XZehaaxM822OY\n"
    "Qpnp5T0XhUEmVrOb2Wrboj+dC/2tgAN/fWXjAAxnm2ECgYEA02UTZuZ+QnD6tqo3\n"
    "/y3n5kaM9uA2mdOIqgECI9psGF1IBIC/iP2diKyuvmQL8hzymComb5YzZl3TOAga\n"
    "WHQYbIeU3JhnYTG75/Dv5Zh32H4NjkIJHT2/8LUM25Ove9u6QAniVgIQpBZ47LjX\n"
    "9jHjTYCW5n79qNSfu0egYJUvypECgYEAwjqWzzEINqnX/xIVCoB4XpuDuSdkM0JW\n"
    "MZDIH9xHjZPp07/5XYEoITylk6Zwbh+djvWDNP4gzPtuK26VsqrNxoWMsFZeXn6U\n"
    "xSOYL2UNCZiOgchdZCOr+6r8LRUuo8xHjbawVoJVK1+tZ2WsR3ilt3Gw34O8Z5ep\n"
    "f4v7GOXw+EMCgYAUHjFrgJIRhqkFi0uK+HZyXtJ5iDsKBqyh6Tin6tiQtQfujcYs\n"
    "pl5ArJZwvhq47vJTcud3hSbdHh7E3ViMhHfylDChkct833vPhgl+ozT8oHpvyG8P\n"
    "nlnO8ZwIpZR0yCOAhrBImSe2RgE6HhlHb9X/ATbbNsizMZEGBLoJlwkWUQKBgQCy\n"
    "4U7fh2LvJUF+82JZh7RUPZn1Pmg0JVZI0/TcEv37UEy77kR1b2xMIBTGhTVq1sc/\n"
    "ULIEbkA7SR1P9sr7//8AZSMLjJ/hG2dcoMmabNCzE8O7l5MblRbh87nIs4d+57bG\n"
    "t4h0RBi4l6eWYLdoI59L8fNaB3PPXIiIpZ0eczeZDQKBgQC2vuFYpUZqDb9CaJsn\n"
    "Luee6P6n5v3ZBTAT4E+GG1kWS28BiebcCuLKNAY4ZtLo08ozaTWcMxooOTeka2ux\n"
    "fQDE4M/LTNpam8QOJ2hqECF5a0uBYNcbmaGtfA9KwIgwCZZYuwb5IDq/DRPuR690\n"
    "i8Kp6jR2wY0suObmZHKvbCB1Dw==\n"
    "-----END PRIVATE KEY-----\n";

const char *pub_pem =
    "-----BEGIN PUBLIC KEY-----\n"
    "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAoGL6IrCSAznmIIzBessI\n"
    "mW7tPOUy78uWTIaub32KnYHn78KXprrZ3ykp6WDrOQeMjv4AA+14mJbg77apVYXy\n"
    "EnkFdOMa1hszSJnp6cJvx7ILngLvFUxzbVki/ehvgS3nRk67Njal+nMTe8hpe3UK\n"
    "QeV/Ij+F0r6Yz91W+4LPmncAiUesRZLetI2BZsKwHYRMznmpIYpoua1NtS8QpEXR\n"
    "MmsUue19eS/XRAPmmCfnb5BX2Tn06iCpk6wO+RfMo9etcX5cLSAuIYEQYCvV2/0X\n"
    "TfEw607vttBN0Y54LrVOKno1vRXd5sxyRlfB0WL42F4VG5TfcJo5u1Xq7k9m9K57\n"
    "8wIDAQAB\n"
    "-----END PUBLIC KEY-----\n";

#define RSA_SIG_SCHEME RSA_PKCS1_PSS_PADDING

char *userDataTest = "test";

#define chknull(X) if (!X) { LOG_ERROR(str(X) "should not be null"); \
                             r = TSS2_FAPI_RC_GENERAL_FAILURE; \
                             goto error_cleanup; }

static  uint8_t *global_signature = NULL;

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
    UNUSED(description);
    UNUSED(publicKey);
    UNUSED(publicKeyHint);
    uint8_t *aux_signature = NULL;

    if (strcmp(objectPath, "P_RSA/HS/SRK/myRsaCryptKey") != 0) {
        return_error(TSS2_FAPI_RC_BAD_VALUE, "Unexpected path");
    }

    if (userData != userDataTest) {
        LOG_ERROR("userData is not correct, %p != %p", userData, userDataTest);
        return TSS2_FAPI_RC_GENERAL_FAILURE;
    }

    if (hashAlg != TPM2_ALG_SHA256) {
        LOG_ERROR("hashAlg is not correct, %u != %u", hashAlg, TPM2_ALG_SHA256);
        return TSS2_FAPI_RC_GENERAL_FAILURE;
    }

    TSS2_RC r = TSS2_RC_SUCCESS;
    EVP_PKEY *priv_key = NULL;
    BIO *bufio = NULL;
    EVP_MD_CTX *mdctx =NULL;
    EVP_PKEY_CTX *pctx = NULL;

    const EVP_MD *ossl_hash = EVP_sha256();
    chknull(ossl_hash);

    LOGBLOB_DEBUG(dataToSign, dataToSignSize, "Data to be signed");

    bufio = BIO_new_mem_buf((void *)priv_pem, strlen(priv_pem));
    priv_key = PEM_read_bio_PrivateKey(bufio, NULL, NULL, NULL);
    chknull(priv_key);

    mdctx = EVP_MD_CTX_create();
    chknull(mdctx);

    if (1 != EVP_DigestSignInit(mdctx, &pctx, ossl_hash, NULL, priv_key)) {
        goto_error(r, TSS2_FAPI_RC_GENERAL_FAILURE, "OSSL sign init.",
                   error_cleanup);
    }
    if (EVP_PKEY_base_id(priv_key) == EVP_PKEY_RSA) {
        int signing_scheme = RSA_SIG_SCHEME;
        if (1 != EVP_PKEY_CTX_set_rsa_padding(pctx, signing_scheme)) {
            goto_error(r, TSS2_FAPI_RC_GENERAL_FAILURE, "OSSL set RSA padding.",
                       error_cleanup);
        }
    }
    if (1 != EVP_DigestSignUpdate(mdctx, dataToSign, dataToSignSize)) {
        goto_error(r, TSS2_FAPI_RC_GENERAL_FAILURE, "OSSL sign update.",
                   error_cleanup);
    }
    if (1 != EVP_DigestSignFinal(mdctx, NULL, signatureSize)) {
        goto_error(r, TSS2_FAPI_RC_GENERAL_FAILURE, "OSSL sign final.",
                   error_cleanup);
    }
    aux_signature = malloc(*signatureSize);
    global_signature = aux_signature;

    chknull(aux_signature);
    if (1 != EVP_DigestSignFinal(mdctx, aux_signature, signatureSize)) {
        goto_error(r, TSS2_FAPI_RC_GENERAL_FAILURE, "OSSL sign final.",
                   error_cleanup);
    }
    *signature = aux_signature;

    if (priv_key)
        EVP_PKEY_free(priv_key);
    if (mdctx)
        EVP_MD_CTX_destroy(mdctx);
    if (bufio)
        BIO_free(bufio);
    return r;

 error_cleanup:
    if (priv_key)
        EVP_PKEY_free(priv_key);
    if (mdctx)
        EVP_MD_CTX_destroy(mdctx);
    if (bufio)
        BIO_free(bufio);
    return r;
}

/** Test the FAPI functions for encryption and decryption.
 *
 * Tested FAPI commands:
 *  - Fapi_Provision()
 *  - Fapi_Import()
 *  - Fapi_CreateKey()
 *  - Fapi_SetSignCB()
 *  - Fapi_Encrypt()
 *  - Fapi_Decrypt()
 *  - Fapi_Free()
 *
 * Tested Policies:
 *  - PolicySigned
 *
 * @param[in,out] context The FAPI_CONTEXT.
 * @retval EXIT_FAILURE
 * @retval EXIT_SUCCESS
 */
int
test_fapi_data_crypt(FAPI_CONTEXT *context)
{

    TSS2_RC r;
    long policy_size;
    const char *policy_name = "/policy/pol_signed";
    const char *policy_file = TOP_SOURCEDIR "/test/data/fapi/policy/pol_signed.json";
    FILE *stream = NULL;
    char *json_policy = NULL;

    uint8_t *cipherText = NULL;
    size_t cipherTextSize;

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

#ifdef PERSISTENT
    r = Fapi_CreateKey(context, "HS/SRK/myRsaCryptKey", "decrypt,0x81000004",
                       policy_name, NULL);
#else
    r = Fapi_CreateKey(context, "HS/SRK/myRsaCryptKey", "decrypt",
                       policy_name, NULL);
#endif
    goto_if_error(r, "Error Fapi_CreateKey", error);

    uint8_t  plainText[SIZE];
    int i;

    for (i = 0; i < SIZE; i++)
        plainText[i] = i % 256;

    r = Fapi_SetSignCB(context, signatureCallback, userDataTest);
    goto_if_error(r, "Error SetPolicySignatureCallback", error);

    r = Fapi_Encrypt(context, "HS/SRK/myRsaCryptKey", &plainText[0],
                     SIZE, &cipherText, &cipherTextSize);

    if (r == TSS2_FAPI_RC_NOT_IMPLEMENTED) {
        goto skip;
    }

    goto_if_error(r, "Error Fapi_Encrypt", error);

    uint8_t *plainText2 = NULL;
    size_t plainText2_size = 0;

    r = Fapi_Decrypt(context, "HS/SRK/myRsaCryptKey", cipherText, cipherTextSize,
                     &plainText2, &plainText2_size);
    goto_if_error(r, "Error Fapi_Encrypt", error);

    if (plainText2_size != SIZE ||
            memcmp(plainText, plainText2, plainText2_size) != 0) {
        LOG_ERROR("Error: decrypted text not  equal to origin");
        goto error;
    }

    Fapi_Free(cipherText);
    Fapi_Free(plainText2);
    Fapi_Free(json_policy);
    Fapi_Delete(context, "/");
    SAFE_FREE(global_signature);

    return EXIT_SUCCESS;

error:
    Fapi_Delete(context, "/");
    Fapi_Free(cipherText);
    Fapi_Free(json_policy);
    Fapi_Delete(context, "/");
    SAFE_FREE(global_signature);

    return EXIT_FAILURE;

 skip:
    Fapi_Delete(context, "/");
    Fapi_Free(json_policy);
    Fapi_Delete(context, "/");
    SAFE_FREE(global_signature);

    return EXIT_SKIP;
}

int
test_invoke_fapi(FAPI_CONTEXT *fapi_context)
{
    return test_fapi_data_crypt(fapi_context);
}
