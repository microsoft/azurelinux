/* SPDX-License-Identifier: BSD-2-Clause */
#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <string.h>

#include <curl/curl.h>
#include <openssl/x509v3.h>
#include <openssl/err.h>
#include <openssl/pem.h>

#include "fapi_certificates.h"
#include "fapi_util.h"
#include "util/aux_util.h"
#include "ifapi_curl.h"
#define LOGMODULE fapi
#include "util/log.h"

static X509
*get_cert_from_buffer(unsigned char *cert_buffer, size_t cert_buffer_size)
{
    unsigned char *buffer = cert_buffer;
    X509 *cert = NULL;

    unsigned const char* tmp_ptr1 = buffer;
    unsigned const char** tmp_ptr2 = &tmp_ptr1;

    if (!d2i_X509(&cert, tmp_ptr2, cert_buffer_size))
        return NULL;
    return cert;
}

/** Convert PEM certificate to OSSL format.
 *
 * @param[in] pem_cert Certificate in PEM format.
 * @retval X509 OSSL certificate object.
 * @retval NULL If the conversion fails.
 */
static X509
*get_X509_from_pem(const char *pem_cert)
{
    if (!pem_cert) {
        return NULL;
    }
    BIO *bufio = NULL;
    X509 *cert = NULL;

    /* Use BIO for conversion */
    size_t pem_length = strlen(pem_cert);
    bufio = BIO_new_mem_buf((void *)pem_cert, pem_length);
    if (!bufio)
        return NULL;
    /* Convert the certificate */
    cert = PEM_read_bio_X509(bufio, NULL, NULL, NULL);
    BIO_free(bufio);
    return cert;
}

/**
 * Get url to download crl from certificate.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE if an internal error occurred.
 * @retval TSS2_FAPI_RC_NO_CERT if an error did occur during certificate downloading.
 */
static TSS2_RC
get_crl_from_cert(X509 *cert, X509_CRL **crl)
{
    TSS2_RC r = TSS2_RC_SUCCESS;
    unsigned char* url = NULL;
    unsigned char *crl_buffer = NULL;
    size_t crl_buffer_size;
    int nid = NID_crl_distribution_points;
    STACK_OF(DIST_POINT) * dist_points = (STACK_OF(DIST_POINT) *)X509_get_ext_d2i(cert, nid, NULL, NULL);
    int curl_rc;

    *crl = NULL;
    for (int i = 0; i < sk_DIST_POINT_num(dist_points); i++)
    {
        DIST_POINT *dp = sk_DIST_POINT_value(dist_points, i);
        DIST_POINT_NAME    *distpoint = dp->distpoint;
        if (distpoint->type==0)
        {
            for (int j = 0; j < sk_GENERAL_NAME_num(distpoint->name.fullname); j++)
            {
                GENERAL_NAME *gen_name = sk_GENERAL_NAME_value(distpoint->name.fullname, j);
                ASN1_IA5STRING *asn1_str = gen_name->d.uniformResourceIdentifier;
                SAFE_FREE(url);
                url = (unsigned char *)strdup((char *)asn1_str->data);
                goto_if_null2(url, "Out of memory", r, TSS2_FAPI_RC_MEMORY, cleanup);
            }
        }
    }

    /* No CRL dist point in the cert is legitimate */
    if (url == NULL) {
        goto cleanup;
    }

    curl_rc = ifapi_get_curl_buffer(url, &crl_buffer, &crl_buffer_size);
    if (curl_rc != 0) {
        goto_error(r, TSS2_FAPI_RC_NO_CERT, "Get crl.", cleanup);
    }

    unsigned const char* tmp_ptr1 = crl_buffer;
    unsigned const char** tmp_ptr2 = &tmp_ptr1;

    if (!d2i_X509_CRL(crl, tmp_ptr2, crl_buffer_size)) {
        goto_error(r, TSS2_FAPI_RC_BAD_VALUE, "Can't convert crl.", cleanup);
    }

cleanup:
    SAFE_FREE(crl_buffer);
    CRL_DIST_POINTS_free(dist_points);
    SAFE_FREE(url);
    return r;
}

/**
 * Verify EK certificate read from TPM.
 *
 * @param[in] root_cert_pem The vendor root certificate.
 * @param[in] intermed_cert_pem The vendor intermediate certificate.
 * @param[in] ek_cert_pem The ek certificate from TPM.
 *
 * @retval TSS2_RC_SUCCESS on success
 * @retval TSS2_FAPI_RC_BAD_VALUE if the verification was no successful.
 * @retval TSS2_FAPI_RC_NO_CERT if an error did occur during certificate downloading.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE if an internal error occurred.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 */
TSS2_RC
ifapi_curl_verify_ek_cert(
    char* root_cert_pem,
    char* intermed_cert_pem,
    char* ek_cert_pem)
{
    TSS2_RC r = TSS2_RC_SUCCESS;
    X509 *root_cert = NULL;
    X509 *intermed_cert = NULL;
    X509 *ek_cert = NULL;
    X509_STORE *store = NULL;
    X509_STORE_CTX *ctx = NULL;
    X509_CRL *crl_intermed = NULL;
    X509_CRL *crl_ek = NULL;
    int i;
    size_t ui;
    AUTHORITY_INFO_ACCESS *info = NULL;
    ASN1_IA5STRING *uri = NULL;
    unsigned char * url;
    unsigned char *cert_buffer = NULL;
    size_t cert_buffer_size;
    int curl_rc;

    LOG_DEBUG("EK Certificate: %s", ek_cert_pem);

    ek_cert = get_X509_from_pem(ek_cert_pem);
    goto_if_null2(ek_cert, "Failed to convert PEM certificate to DER.",
                  r, TSS2_FAPI_RC_BAD_VALUE, cleanup);

    if (intermed_cert_pem) {
        intermed_cert = get_X509_from_pem(intermed_cert_pem);
        goto_if_null2(intermed_cert, "Failed to convert PEM certificate to DER.",
                      r, TSS2_FAPI_RC_BAD_VALUE, cleanup);
    } else {
        /* Get uri for ek intermediate certificate. */
        info = X509_get_ext_d2i(ek_cert, NID_info_access, NULL, NULL);

        for (i = 0; i < sk_ACCESS_DESCRIPTION_num(info); i++) {
            ACCESS_DESCRIPTION *ad = sk_ACCESS_DESCRIPTION_value(info, i);
            if (ad->location->type != GEN_URI) {
                continue;
            }
            uri = ad->location->d.uniformResourceIdentifier;
            url = uri->data;
            curl_rc = ifapi_get_curl_buffer(url, &cert_buffer, &cert_buffer_size);
            if (curl_rc != 0) {
                goto_error(r, TSS2_FAPI_RC_NO_CERT, "Get certificate.", cleanup);
            }
            goto_if_null2(cert_buffer, "No certificate downloaded", r,
                          TSS2_FAPI_RC_NO_CERT, cleanup);
            LOGBLOB_DEBUG(cert_buffer, cert_buffer_size, "Intermediate certificate:");
        }
        goto_if_null2(cert_buffer, "No certificate downloaded", r,
                      TSS2_FAPI_RC_NO_CERT, cleanup);

        intermed_cert = get_cert_from_buffer(cert_buffer, cert_buffer_size);
        if (!intermed_cert) {
            LOGBLOB_ERROR(cert_buffer, cert_buffer_size,
                          "Failed to convert intermediate certificate to X509 format.");
            r = TSS2_FAPI_RC_GENERAL_FAILURE;
            goto cleanup;
        }

         /* Get Certificate revocation list for Intermediate certificate */
        r = get_crl_from_cert(intermed_cert, &crl_intermed);
        goto_if_error(r, "Get crl for intermediate certificate.", cleanup);

        /* Get Certificate revocation list for EK certificate */
        r = get_crl_from_cert(ek_cert, &crl_ek);
        goto_if_error(r, "Get crl for ek certificate.", cleanup);
    }

    /* Prepare X509 certificate store */

    store = X509_STORE_new();

    goto_if_null2(store, "Failed to create X509 store.",
                  r, TSS2_FAPI_RC_GENERAL_FAILURE, cleanup);

    /* Add Certificate revocation list for EK certificate if one exists. */
    if (crl_ek) {
        /* Set the flags of the store to use CRLs. */
        X509_STORE_set_flags(store, X509_V_FLAG_CRL_CHECK | X509_V_FLAG_CRL_CHECK_ALL);
        if (1 != X509_STORE_add_crl(store, crl_ek)) {
            goto_error(r, TSS2_FAPI_RC_GENERAL_FAILURE,
                       "Failed to add intermediate crl.", cleanup);
        }
    }

    /* Add Certificate revocation list for intermediate certificate if one exists. */
    if (crl_intermed) {
        /* Set the flags of the store to use CRLs. */
        X509_STORE_set_flags(store, X509_V_FLAG_CRL_CHECK | X509_V_FLAG_CRL_CHECK_ALL);
        if (1 != X509_STORE_add_crl(store, crl_intermed)) {
            goto_error(r, TSS2_FAPI_RC_GENERAL_FAILURE,
                       "Failed to add intermediate crl.", cleanup);
        }
    }

    /* Add stored root certificates */
    for (ui = 0; ui < sizeof(root_cert_list) / sizeof(char *); ui++) {
         root_cert = get_X509_from_pem(root_cert_list[ui]);
         goto_if_null2(root_cert, "Failed to convert PEM certificate to DER.",
                       r, TSS2_FAPI_RC_BAD_VALUE, cleanup);
         if (1 != X509_STORE_add_cert(store, root_cert)) {
             goto_error(r, TSS2_FAPI_RC_GENERAL_FAILURE,
                        "Failed to add root certificate", cleanup);
        }
        OSSL_FREE(root_cert, X509);
    }

    /* Create root cert if passed as parameter */
    if (root_cert_pem) {
        root_cert = get_X509_from_pem(root_cert_pem);
        goto_if_null2(root_cert, "Failed to convert PEM certificate to DER.",
                      r, TSS2_FAPI_RC_BAD_VALUE, cleanup);

        if (1 != X509_STORE_add_cert(store, root_cert)) {
            goto_error(r, TSS2_FAPI_RC_GENERAL_FAILURE,
                       "Failed to add root certificate", cleanup);
        }
        OSSL_FREE(root_cert, X509);
    }

    /* Verify intermediate certificate */
    ctx = X509_STORE_CTX_new();
    goto_if_null2(ctx, "Failed to create X509 store context.",
                  r, TSS2_FAPI_RC_GENERAL_FAILURE, cleanup);
    if (1 != X509_STORE_CTX_init(ctx, store, intermed_cert, NULL)) {
        goto_error(r, TSS2_FAPI_RC_GENERAL_FAILURE,
                   "Failed to initialize X509 context.", cleanup);
    }
    if (1 != X509_verify_cert(ctx)) {
        LOG_ERROR("%s", X509_verify_cert_error_string(X509_STORE_CTX_get_error(ctx)));
        goto_error(r, TSS2_FAPI_RC_GENERAL_FAILURE,
                   "Failed to verify intermediate certificate", cleanup);
    }
    if (1 != X509_STORE_add_cert(store, intermed_cert)) {
        goto_error(r, TSS2_FAPI_RC_GENERAL_FAILURE,
                   "Failed to add intermediate certificate", cleanup);
    }

    X509_STORE_CTX_cleanup(ctx);
    X509_STORE_CTX_free(ctx);
    ctx = NULL;
    ctx = X509_STORE_CTX_new();
    goto_if_null2(ctx, "Failed to create X509 store context.",
                  r, TSS2_FAPI_RC_GENERAL_FAILURE, cleanup);

    if (1 != X509_STORE_CTX_init(ctx, store, ek_cert, NULL)) {
        goto_error(r, TSS2_FAPI_RC_GENERAL_FAILURE,
                   "Failed to initialize X509 context.", cleanup);
    }
    /* Verify the EK certificate. */
    if (1 != X509_verify_cert(ctx)) {
        LOG_ERROR("%s", X509_verify_cert_error_string(X509_STORE_CTX_get_error(ctx)));
        goto_error(r, TSS2_FAPI_RC_GENERAL_FAILURE,
                   "Failed to verify EK certificate", cleanup);
    }

cleanup:
    if (ctx) {
        X509_STORE_CTX_cleanup(ctx);
        X509_STORE_CTX_free(ctx);
    }
    if (store)
        X509_STORE_free(store);
    SAFE_FREE(cert_buffer);
    OSSL_FREE(root_cert, X509);
    OSSL_FREE(intermed_cert, X509);
    OSSL_FREE(ek_cert, X509);
    OSSL_FREE(crl_intermed, X509_CRL);
    OSSL_FREE(crl_ek, X509_CRL);
    OSSL_FREE(info, AUTHORITY_INFO_ACCESS);
    return r;
}

struct CurlBufferStruct {
  unsigned char *buffer;
  size_t size;
};

/** Callback for copying received curl data to a buffer.
 *
 * The buffer will be reallocated according to the size of retrieved data.
 *
 * @param[in]  contents The retrieved content.
 * @param[in]  size the block size in the content.
 * @param[in]  nmemb The number of blocks.
 * @retval realsize The byte size of the data.
 */
static size_t
write_curl_buffer_cb(void *contents, size_t size, size_t nmemb, void *userp)
{
    size_t realsize = size * nmemb;
    struct CurlBufferStruct *curl_buf = (struct CurlBufferStruct *)userp;

    unsigned char *tmp_ptr = realloc(curl_buf->buffer, curl_buf->size + realsize + 1);
    if (tmp_ptr == NULL) {
        LOG_ERROR("Can't allocate memory in CURL callback.");
        return 0;
    }
    curl_buf->buffer = tmp_ptr;
    memcpy(&(curl_buf->buffer[curl_buf->size]), contents, realsize);
    curl_buf->size += realsize;
    curl_buf->buffer[curl_buf->size] = 0;

    return realsize;
}

/** Get byte buffer from file system or web via curl.
 *
 * @param[in]  url The url of the resource.
 * @param[out] buffer The buffer retrieved via the url.
 * @param[out] buffer_size The size of the retrieved object.
 *
 * @retval 0 if buffer could be retrieved.
 * @retval -1 if an error did occur
 */
int
ifapi_get_curl_buffer(unsigned char * url, unsigned char ** buffer,
                          size_t *buffer_size) {
    int ret = -1;
    struct CurlBufferStruct curl_buffer = { .size = 0, .buffer = NULL };
    long http_code;
#ifdef CURLU_ALLOW_SPACE
    CURLU *urlp = NULL;
#endif

    CURLcode rc = curl_global_init(CURL_GLOBAL_DEFAULT);
    if (rc != CURLE_OK) {
        LOG_ERROR("curl_global_init failed: %s", curl_easy_strerror(rc));
        goto out_memory;
    }

    CURL *curl = curl_easy_init();
    if (!curl) {
        LOG_ERROR("curl_easy_init failed");
        goto out_global_cleanup;
    }

#ifdef CURLU_ALLOW_SPACE
    urlp = curl_url();
    if (!urlp) {
        LOG_ERROR("curl_url failed.");
        goto out_easy_cleanup;
    }
    CURLUcode url_rc;
    url_rc = curl_url_set(urlp, CURLUPART_URL, (const char *)url, CURLU_ALLOW_SPACE | CURLU_URLENCODE);
    if (url_rc) {
#ifdef HAVE_CURL_URL_STRERROR
        LOG_ERROR("curl_url_set for CURUPART_URL failed: %s",
                  curl_url_strerror(url_rc));
#else
        LOG_ERROR("curl_url_set for CURUPART_URL failed: %u", url_rc);
#endif
        goto out_easy_cleanup;
    }
    rc = curl_easy_setopt(curl, CURLOPT_CURLU, urlp);
#else
    rc = curl_easy_setopt(curl, CURLOPT_URL, url);
#endif

    if (rc != CURLE_OK) {
        LOG_ERROR("curl_easy_setopt for CURLOPT_URL failed: %s",
                curl_easy_strerror(rc));
        goto out_easy_cleanup;
    }

    rc = curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION,
                          write_curl_buffer_cb);
    if (rc != CURLE_OK) {
        LOG_ERROR("curl_easy_setopt for CURLOPT_URL failed: %s",
                curl_easy_strerror(rc));
        goto out_easy_cleanup;
    }

    rc = curl_easy_setopt(curl, CURLOPT_WRITEDATA,
                          (void *)&curl_buffer);
    if (rc != CURLE_OK) {
        LOG_ERROR("curl_easy_setopt for CURLOPT_URL failed: %s",
                curl_easy_strerror(rc));
        goto out_easy_cleanup;
    }

    rc = curl_easy_setopt(curl, CURLOPT_FOLLOWLOCATION, 1);
    if (rc != CURLE_OK) {
        LOG_ERROR("curl_easy_setopt for CURLOPT_FOLLOWLOCATION failed: %s",
                  curl_easy_strerror(rc));
        goto out_easy_cleanup;
    }

    if (LOGMODULE_status == LOGLEVEL_TRACE) {
        if (CURLE_OK != curl_easy_setopt(curl, CURLOPT_VERBOSE, 1L)) {
            LOG_WARNING("Curl easy setopt verbose failed");
        }
    }

    rc = curl_easy_perform(curl);
    if (rc != CURLE_OK) {
        LOG_ERROR("curl_easy_perform() failed: %s", curl_easy_strerror(rc));
        goto out_easy_cleanup;
    }

    curl_easy_getinfo(curl, CURLINFO_RESPONSE_CODE, &http_code);
    if (http_code >= 400) {
        LOG_ERROR("curl http return code %li", http_code);
        goto out_easy_cleanup;
    }

    *buffer = curl_buffer.buffer;
    *buffer_size = curl_buffer.size;

    ret = 0;

out_easy_cleanup:
#ifdef CURLU_ALLOW_SPACE
    if (urlp)
        curl_url_cleanup(urlp);
#endif
    if (ret != 0)
        free(curl_buffer.buffer);
    curl_easy_cleanup(curl);
out_global_cleanup:
    curl_global_cleanup();
out_memory:
    return ret;
}
