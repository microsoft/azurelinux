/* SPDX-License-Identifier: BSD-2-Clause */
/*******************************************************************************
 * Copyright 2017-2018, Fraunhofer SIT sponsored by Infineon Technologies AG
 * All rights reserved.
 *******************************************************************************/

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <openssl/evp.h>
#include <openssl/aes.h>
#include <openssl/rsa.h>
#include <openssl/engine.h>
#include <openssl/pem.h>
#include <stdio.h>
#include <stddef.h>
#include <string.h>
#include <inttypes.h>

#include "tss2_fapi.h"

#define LOGMODULE test
#include "util/log.h"
#include "util/aux_util.h"
#include "test-fapi.h"

/** Test the FAPI functions use an external public key for signature and quote verify without TPM.
 *
 * Tested FAPI commands:
 *  - Fapi_Import()
 *  - Fapi_VerifySignature()
 *  - Fapi_SetCertificate()
 *  - Fapi_GetCertificate()
 *  - Fapi_List()
 *  - Fapi_VerifyQuote()
 *  - Fapi_Delete()
 *
 * @param[in,out] context The FAPI_CONTEXT.
 * @retval EXIT_FAILURE
 * @retval EXIT_SUCCESS
 */
int
test_fapi_ext_public_key(FAPI_CONTEXT *context)
{

    TSS2_RC r;
    BIO *bufio = NULL;

    EVP_PKEY *evp_key = NULL;
    EVP_PKEY_CTX *ctx = NULL;

    /* Key will be used for non TPM signature verfication. */
    char *pubkey_pem =
        "-----BEGIN PUBLIC KEY-----\n"
        "MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEUymzBzI3LcxRpqJkiP0Ks7qp1UZH\n"
        "93mYpmfUJBjK6anQawTyy8k87MteUdP5IPy47gzsO7sFcbWCoVZ8LvoQUw==\n"
        "-----END PUBLIC KEY-----\n";

    /* Quote info will be used for non TPM signature verfication. */
    const char *quote_info =
        "{\n"
        "  \"sig_scheme\":{\n"
        "    \"scheme\":\"ECDSA\",\n"
        "    \"details\":{\n"
        "      \"hashAlg\":\"SHA256\"\n"
        "    }\n"
        "  },\n"
        "  \"attest\":{\n"
        "    \"magic\":\"VALUE\",\n"
        "    \"type\":\"ATTEST_QUOTE\",\n"
        "    \"qualifiedSigner\":\"000b6f2f5ee244f7af20dbdfdf0a7dd21ef28afd9c3f377758f9ace6e29e64fc0ccf\",\n"
        "    \"extraData\":\"6768033e216468247bd031a0a2d9876d79818f8f\",\n"
        "    \"clockInfo\":{\n"
        "      \"clock\":4607,\n"
        "      \"resetCount\":2327013047,\n"
        "      \"restartCount\":1164757112,\n"
        "      \"safe\":\"YES\"\n"
        "    },\n"
        "    \"firmwareVersion\":[\n"
        "      635916457,\n"
        "      1185938286\n"
        "    ],\n"
        "    \"attested\":{\n"
        "      \"pcrSelect\":[\n"
        "        {\n"
        "          \"hash\":\"SHA256\",\n"
        "          \"pcrSelect\":[\n"
        "            16\n"
        "          ]\n"
        "        }\n"
        "      ],\n"
        "      \"pcrDigest\":\"224eb2f4e5625ecb4a31cb7df43282ef6293c97a840a33415a3afe069535fa9b\"\n"
        "    }\n"
        "  }\n"
        "}\n";

    /* Test signature will be used for non TPM signature verfication. */
    size_t test_signature_size = 71;
    const uint8_t test_signature[71] = {
      0x30, 0x45, 0x02, 0x21, 0x00, 0x8a, 0x00, 0x01,
      0x6b, 0x79, 0xe2, 0x50, 0x84, 0x52, 0xc3, 0x40,
      0xbb, 0x6c, 0xb4, 0xcb, 0x31, 0x42, 0xa2, 0xe5,
      0x8b, 0x36, 0x35, 0x46, 0x8d, 0x8c, 0x3e, 0x59,
      0xda, 0x0e, 0x83, 0x7e, 0x3b, 0x02, 0x20, 0x77,
      0xb1, 0xe6, 0xa8, 0xab, 0x0e, 0x5f, 0x72, 0x28,
      0x3e, 0x35, 0xe5, 0x91, 0x5b, 0x13, 0x35, 0xfe,
      0x44, 0x54, 0xa4, 0x79, 0x63, 0x2a, 0x94, 0xd5,
      0xaa, 0x07, 0xce, 0xba, 0xc6, 0x56, 0x85
     };

     /* Qualifying data will be used for non TPM signature verfication. */
    uint8_t qualifying_data[20] = {
        0x67, 0x68, 0x03, 0x3e, 0x21, 0x64, 0x68, 0x24, 0x7b, 0xd0,
        0x31, 0xa0, 0xa2, 0xd9, 0x87, 0x6d, 0x79, 0x81, 0x8f, 0x8f
    };

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

    const char *cert =
        "-----BEGIN CERTIFICATE-----\n"
        "MIIDBjCCAe4CCQDcvXBOEVM0UTANBgkqhkiG9w0BAQsFADBFMQswCQYDVQQGEwJE\n"
        "RTETMBEGA1UECAwKU29tZS1TdGF0ZTEhMB8GA1UECgwYSW50ZXJuZXQgV2lkZ2l0\n"
        "cyBQdHkgTHRkMB4XDTE5MDIyODEwNDkyM1oXDTM1MDgyNzEwNDkyM1owRTELMAkG\n"
        "A1UEBhMCREUxEzARBgNVBAgMClNvbWUtU3RhdGUxITAfBgNVBAoMGEludGVybmV0\n"
        "IFdpZGdpdHMgUHR5IEx0ZDCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEB\n"
        "AKBi+iKwkgM55iCMwXrLCJlu7TzlMu/LlkyGrm99ip2B5+/Cl6a62d8pKelg6zkH\n"
        "jI7+AAPteJiW4O+2qVWF8hJ5BXTjGtYbM0iZ6enCb8eyC54C7xVMc21ZIv3ob4Et\n"
        "50ZOuzY2pfpzE3vIaXt1CkHlfyI/hdK+mM/dVvuCz5p3AIlHrEWS3rSNgWbCsB2E\n"
        "TM55qSGKaLmtTbUvEKRF0TJrFLntfXkv10QD5pgn52+QV9k59OogqZOsDvkXzKPX\n"
        "rXF+XC0gLiGBEGAr1dv9F03xMOtO77bQTdGOeC61Tip6Nb0V3ebMckZXwdFi+Nhe\n"
        "FRuU33CaObtV6u5PZvSue/MCAwEAATANBgkqhkiG9w0BAQsFAAOCAQEAcamUPe8I\n"
        "nMOHcv9x5lVN1joihVRmKc0QqNLFc6XpJY8+U5rGkZvOcDe9Da8L97wDNXpKmU/q\n"
        "pprj3rT8l3v0Z5xs8Vdr8lxS6T5NhqQV0UCsn1x14gZJcE48y9/LazYi6Zcar+BX\n"
        "Am4vewAV3HmQ8X2EctsRhXe4wlAq4slIfEWaaofa8ai7BzO9KwpMLsGPWoNetkB9\n"
        "19+SFt0lFFOj/6vDw5pCpSd1nQlo1ug69mJYSX/wcGkV4t4LfGhV8jRPDsGs6I5n\n"
        "ETHSN5KV1XCPYJmRCjFY7sIt1x4zN7JJRO9DVw+YheIlduVfkBiF+GlQgLlFTjrJ\n"
        "VrpSGMIFSu301A==\n"
        "-----END CERTIFICATE-----\n";

    char *cert2 = NULL;
    char *path_list = NULL;

    r = Fapi_Import(context, "myExtPubKey", pub_pem);
    goto_if_error(r, "Error Fapi_Import", error);

    bufio = BIO_new_mem_buf((void *)priv_pem, strlen(priv_pem));
    evp_key = PEM_read_bio_PrivateKey(bufio, NULL, NULL, NULL);

    if (!bufio || !evp_key) {
        LOG_ERROR("Generation of test key failed.");
        goto error;
    }

    uint8_t digest[20] = {
        0xa9, 0x99, 0x3e, 0x36, 0x47, 0x06, 0x81, 0x6a, 0xba, 0x3e,
        0x25, 0x71, 0x78, 0x50, 0xc2, 0x6c, 0x9c, 0xd0, 0xd8, 0x9d
    };
    uint8_t signature[256];
    size_t  signatureLength = 256;

    if ((ctx = EVP_PKEY_CTX_new(evp_key, NULL)) == NULL) {
        LOG_ERROR("Test EVP_PKEY_CTX_new failed.");
        goto error;
    }
    if (EVP_PKEY_sign_init(ctx) <= 0
            || EVP_PKEY_CTX_set_rsa_padding(ctx, RSA_PKCS1_PADDING) <= 0
            || EVP_PKEY_CTX_set_signature_md(ctx, EVP_sha1()) <= 0) {
        LOG_ERROR("Test EVP_PKEY_sign_init failed.");
        goto error;
    }
    if (EVP_PKEY_sign(ctx, signature, &signatureLength, digest, 20) <= 0) {
        LOG_ERROR("Test EVP_PKEY_sign failed.");
        goto error;
    }

    r = Fapi_VerifySignature(context, "/ext/myExtPubKey", digest, 20,
                             signature, 256);
    goto_if_error(r, "Error Fapi_VerifySignature", error);

    r = Fapi_SetCertificate(context, "/ext/myExtPubKey", cert);
    goto_if_error(r, "Error Fapi_SetCertificate", error);

    r = Fapi_GetCertificate(context, "/ext/myExtPubKey", &cert2);
    goto_if_error(r, "Error Fapi_SetCertificate", error);
    ASSERT(cert2 != NULL);
    ASSERT(strlen(cert2) > ASSERT_SIZE);

    if (strcmp(cert, cert2) != 0) {
        goto_if_error(r, "Different certificates", error);
    }

    r = Fapi_List(context, "", &path_list);
    LOG_INFO("Pathlist: %s", path_list);
    goto_if_error(r, "Error Fapi_List", error);
    ASSERT(path_list != NULL);
    ASSERT(strcmp(path_list, "/ext/myExtPubKey") == 0);

    r = Fapi_Delete(context, "/ext/myExtPubKey");
    goto_if_error(r, "Error Fapi_Delete", error);

    /* Test VerfiyQuote in non TPM mode. */
    r = Fapi_Import(context, "/ext/myExtPubKey", pubkey_pem);
    goto_if_error(r, "Error Fapi_Import", error);

    r = Fapi_VerifyQuote(context, "/ext/myExtPubKey",
                         qualifying_data, 20,  quote_info,
                         test_signature, test_signature_size, NULL);
    goto_if_error(r, "Error Fapi_Verfiy_Quote", error);

    fprintf(stderr, "\nPathList:\n%s\n", path_list);

    r = Fapi_Delete(context, "/ext");
    goto_if_error(r, "Error Fapi_Delete", error);
    if (bufio) {
        BIO_free(bufio);
    }
    EVP_PKEY_CTX_free(ctx);
    EVP_PKEY_free(evp_key);
    SAFE_FREE(path_list);
    SAFE_FREE(cert2);
    return EXIT_SUCCESS;

error:
    Fapi_Delete(context, "/");
    if (bufio) {
        BIO_free(bufio);
    }
    EVP_PKEY_CTX_free(ctx);
    EVP_PKEY_free(evp_key);
    SAFE_FREE(path_list);
    SAFE_FREE(cert2);
    return EXIT_FAILURE;
}

int
test_invoke_fapi(FAPI_CONTEXT *fapi_context)
{
    return test_fapi_ext_public_key(fapi_context);
}
