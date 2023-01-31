/* SPDX-License-Identifier: BSD-2-Clause */

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <curl/curl.h>
#include <openssl/buffer.h>
#include <openssl/evp.h>
#include <openssl/sha.h>
#include <json-c/json.h>

#include "fapi_crypto.h"
#include "ifapi_curl.h"
#include "ifapi_helpers.h"
#include "tpm_json_deserialize.h"

#define LOGMODULE fapi
#include "util/log.h"
#include "util/aux_util.h"

typedef struct tpm_getekcertificate_ctx tpm_getekcertificate_ctx;
struct tpm_getekcertificate_ctx {
    char *ec_cert_path;
    FILE *ec_cert_file_handle;
    char *ek_server_addr;
    unsigned int SSL_NO_VERIFY;
    char *ek_path;
    bool verbose;
    bool is_tpm2_device_active;
    TPM2B_PUBLIC *out_public;
};

static tpm_getekcertificate_ctx ctx = {
    .is_tpm2_device_active = true,
};

/** Compute the SHA256 hash from the public key of an EK.
 *
 * @param[in]  ek_public The public information of the EK.
 * @retval unsigned_char* The hash value.
 * @retval NULL If the computation of the hash fails.
 */
static unsigned char *hash_ek_public(TPM2B_PUBLIC *ek_public) {

    unsigned char *hash = (unsigned char *)malloc(SHA256_DIGEST_LENGTH);
    if (!hash) {
        LOG_ERROR("OOM");
        return NULL;
    }

    EVP_MD_CTX *sha256ctx = EVP_MD_CTX_new();
    if (!sha256ctx) {
        LOG_ERROR("EVP_MD_CTX_new failed");
        goto err;
    }

    int is_success = EVP_DigestInit(sha256ctx, EVP_sha256());
    if (!is_success) {
        LOG_ERROR("EVP_DigestInit failed");
        goto err;
    }

    switch (ek_public->publicArea.type) {
    case TPM2_ALG_RSA:
        /* Add public key to the hash. */
        is_success = EVP_DigestUpdate(sha256ctx,
                                      ek_public->publicArea.unique.rsa.buffer,
                                      ek_public->publicArea.unique.rsa.size);
        if (!is_success) {
            LOG_ERROR("EVP_DigestUpdate failed");
            goto err;
        }

        /* Add exponent to the hash. */
        if (ek_public->publicArea.parameters.rsaDetail.exponent != 0) {
            LOG_ERROR("non-default exponents unsupported");
            goto err;
        }
        /* Exponent 65537 will be added. */
        BYTE buf[3] = { 0x1, 0x00, 0x01 };
        is_success = EVP_DigestUpdate(sha256ctx, buf, sizeof(buf));
        if (!is_success) {
            LOG_ERROR("EVP_DigestUpdate failed");
            goto err;
        }
        break;

    case TPM2_ALG_ECC:
        is_success = EVP_DigestUpdate(sha256ctx,
                                      ek_public->publicArea.unique.ecc.x.buffer,
                                      ek_public->publicArea.unique.ecc.x.size);
        if (!is_success) {
            LOG_ERROR("EVP_DigestUpdate failed");
            goto err;
        }

        /* Add public key to the hash. */
        is_success = EVP_DigestUpdate(sha256ctx,
                                      ek_public->publicArea.unique.ecc.y.buffer,
                                      ek_public->publicArea.unique.ecc.y.size);
        if (!is_success) {
            LOG_ERROR("EVP_DigestUpdate failed");
            goto err;
        }
        break;

    default:
        LOG_ERROR("unsupported EK algorithm");
        goto err;
    }

    is_success = EVP_DigestFinal_ex(sha256ctx, hash, NULL);
    if (!is_success) {
        LOG_ERROR("SHA256_Final failed");
        goto err;
    }

    EVP_MD_CTX_free(sha256ctx);
    LOG_TRACE("public-key-hash:");
    LOG_TRACE("  sha256: ");
    LOGBLOB_TRACE(&hash[0], SHA256_DIGEST_LENGTH, "Hash");
    return hash;
err:
    EVP_MD_CTX_free(sha256ctx);
    free(hash);
    return NULL;
}

/** Calculate the base64 encoding of the hash of the Endorsement Public Key.
 *
 * @param[in] buffer The hash of the endorsement public key.
 * @retval char* The base64 encoded string.
 * @retval NULL if the encoding fails.
 */
static char *
base64_encode(const unsigned char* buffer)
{
    BIO *bio, *b64;
    BUF_MEM *buffer_pointer;

    LOG_INFO("Calculating the base64_encode of the hash of the Endorsement"
             "Public Key:");

    if (buffer == NULL) {
        LOG_ERROR("hash_ek_public returned null");
        return NULL;
    }

    b64 = BIO_new(BIO_f_base64());
    bio = BIO_new(BIO_s_mem());
    bio = BIO_push(b64, bio);
    BIO_set_flags(bio, BIO_FLAGS_BASE64_NO_NL);
    BIO_write(bio, buffer, SHA256_DIGEST_LENGTH);
    (void)(BIO_flush(bio));
    BIO_get_mem_ptr(bio, &buffer_pointer);

    /* these are not NULL terminated */
    char *b64text = buffer_pointer->data;
    size_t len = buffer_pointer->length;

    size_t i;
    for (i = 0; i < len; i++) {
        if (b64text[i] == '+') {
            b64text[i] = '-';
        }
        if (b64text[i] == '/') {
            b64text[i] = '_';
        }
    }

    char *final_string = NULL;

    CURL *curl = curl_easy_init();
    if (curl) {
        char *output = curl_easy_escape(curl, b64text, len);
        if (output) {
            final_string = strdup(output);
            curl_free(output);
        }
    }
    curl_easy_cleanup(curl);
    curl_global_cleanup();
    BIO_free_all(bio);

    /* format to a proper NULL terminated string */
    return final_string;
}

/** Decode a base64 encoded certificate into binary form.
 *
 * @param[in]  buffer The base64 encoded certificate.
 * @param[in]  len The length of the encoded certificate.
 * @param[out] new_len The lenght of the binary certificate.
 * @retval char* The binary data of the certificate.
 * @retval NULL if the decoding fails.
 */
static char *
base64_decode(unsigned char* buffer, size_t len, size_t *new_len)
{
    size_t i, r;
    int unescape_len = 0;
    char *binary_data = NULL, *unescaped_string = NULL;

    LOG_INFO("Decoding the base64 encoded cert into binary form");

    if (buffer == NULL) {
        LOG_ERROR("Cert buffer is null");
        return NULL;
    }

    for (i = 0; i < len; i++) {
        if (buffer[i] == '-') {
            buffer[i] = '+';
        }
        if (buffer[i] == '_') {
            buffer[i] = '/';
        }
    }

    CURL *curl = curl_easy_init();
    if (curl) {
        /* Convert URL encoded string to a "plain string" */
        char *output = curl_easy_unescape(curl, (char *)buffer,
                                          len, &unescape_len);
        if (output) {
            unescaped_string = strdup(output);
            curl_free(output);
        } else {
            LOG_ERROR("curl_easy_unescape failed.");
        }
    } else {
        LOG_ERROR("curl_easy_init failed.");
        return NULL;
    }
    curl_easy_cleanup(curl);
    curl_global_cleanup();
    if (unescaped_string == NULL) {
        LOG_ERROR("Computation of unescaped string failed.");
        return NULL;
    }

    binary_data = calloc(1, unescape_len);
    if (binary_data == NULL) {
        free (unescaped_string);
        LOG_ERROR("Allocation of data for certificate failed.");
        return NULL;
    }

    BIO *bio, *b64;
    bio = BIO_new_mem_buf(unescaped_string, -1);
    b64 = BIO_new(BIO_f_base64());
    bio = BIO_push(b64, bio);
    BIO_set_flags(bio, BIO_FLAGS_BASE64_NO_NL);

    if ((r = BIO_read(bio, binary_data, unescape_len)) <= 0) {
        LOG_ERROR("BIO_read base64 encoded cert failed");
        free(binary_data);
        binary_data = NULL;
    }
    *new_len = r;

    free (unescaped_string);
    BIO_free_all(bio);
    return binary_data;
}

/** Get endorsement certificate from the WEB.
 *
 * The base64 encoded public endorsement key will be added to the INTEL
 * server address and used as URL to retrieve the certificate.
 * The certificate will be retrieved via curl.
 *
 * @param[in]  b64h The base64 encoded public key.
 * @param[out] buffer The json encoded certificate.
 * @param[out] cert_size The size of the certificate.
 */
int retrieve_endorsement_certificate(char *b64h, unsigned char ** buffer,
                                     size_t *cert_size) {
    int ret = -1;

    size_t len = 1 + strlen(b64h) + strlen(ctx.ek_server_addr);
    char *weblink = (char *) malloc(len);

    if (!weblink) {
        LOG_ERROR("oom");
        return ret;
    }

    snprintf(weblink, len, "%s%s", ctx.ek_server_addr, b64h);

    CURLcode rc =  ifapi_get_curl_buffer((unsigned char *)weblink,
                                         buffer, cert_size);
    free(weblink);
    return rc;
}

/** Get INTEL certificate for EK
 *
 * Using the base64 encoded public endorsement key the JSON encoded certificate
 * will be downloaded.
 * The JSON certificate will be parsed and the base64 encoded certificate
 * will be converted into binary format.
 *
 *
 * @param[in] context The FAPI context with the configuration data.
 * @param[in] ek_public The out public data of the EK.
 * @param[out] cert_buffer the der encoded certificate.
 * @param[out] cert_size The size of the certificate buffer.
 *
 * @retval TSS2_RC_SUCCESS on success.
 * @retval TSS2_FAPI_RC_NO_CERT If an error did occur during certificate downloading.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE if an internal error occured.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 */
TSS2_RC
ifapi_get_intl_ek_certificate(FAPI_CONTEXT *context, TPM2B_PUBLIC *ek_public,
                              unsigned char ** cert_buffer, size_t *cert_size)
{
    int rc = 1;
    unsigned char *hash = hash_ek_public(ek_public);
    char *cert_ptr = NULL;
    char *cert_start = NULL, *cert_bin = NULL;
    char *b64 = base64_encode(hash);
    *cert_buffer = NULL;

    if (!b64) {
        LOG_ERROR("base64_encode returned null");
        goto out;
    }
    if (context->config.intel_cert_service)
        ctx.ek_server_addr = context->config.intel_cert_service;
    else
        ctx.ek_server_addr = "https://ekop.intel.com/ekcertservice/";

    LOG_INFO("%s", b64);

    /* Download the JSON encoded certificate. */
    rc = retrieve_endorsement_certificate(b64, cert_buffer, cert_size);
    free(b64);
    goto_if_error(rc, "Retrieve endorsement certificate", out);
    cert_ptr = (char *)*cert_buffer;
    LOGBLOB_DEBUG((uint8_t *)cert_ptr, *cert_size, "%s", "Certificate");

    /* Parse certificate data out of the json structure */
    struct json_object *jso_cert, *jso = ifapi_parse_json(cert_ptr);
    if (jso == NULL)
        goto_error(rc, TSS2_FAPI_RC_GENERAL_FAILURE,
                   "Failed to parse EK cert data", out_free_json);

    if (!json_object_object_get_ex(jso, "certificate", &jso_cert))
        goto_error(rc, TSS2_FAPI_RC_GENERAL_FAILURE,
                   "Could not find cert object", out_free_json);

    if (!json_object_is_type(jso_cert, json_type_string))
        goto_error(rc, TSS2_FAPI_RC_GENERAL_FAILURE,
                   "Invalid EK cert data", out_free_json);

    cert_start = strdup(json_object_get_string(jso_cert));
    if (!cert_start) {
        SAFE_FREE(cert_ptr);
        goto_error(rc, TSS2_FAPI_RC_MEMORY,
                   "Failed to duplicate cert", out_free_json);
    }

    *cert_size = strlen(cert_start);

    /* Base64 decode buffer into binary PEM format */
    cert_bin = base64_decode((unsigned char *)cert_start,
                             *cert_size, cert_size);
    SAFE_FREE(cert_ptr);
    SAFE_FREE(cert_start);

    if (cert_bin == NULL) {
        goto_error(rc, TSS2_FAPI_RC_GENERAL_FAILURE,
                   "Invalid EK cert data", out_free_json);
    }
    LOG_DEBUG("Binary cert size %zu", *cert_size);
    *cert_buffer = (unsigned char *)cert_bin;

out_free_json:
    json_object_put(jso);

out:
    free(hash);
    if (rc == 0) {
        return TSS2_RC_SUCCESS;
    } else {
        SAFE_FREE(cert_bin);
        SAFE_FREE(cert_ptr);
        LOG_ERROR("Get INTEL EK certificate.");
        return TSS2_FAPI_RC_NO_CERT;
    }
}
