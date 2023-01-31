/* SPDX-License-Identifier: BSD-2-Clause */
/*******************************************************************************
 * Copyright 2017-2018, Fraunhofer SIT sponsored by Infineon Technologies AG
 * All rights reserved.
 *******************************************************************************/

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <stdlib.h>

#include "tss2_fapi.h"
#include "tss2_esys.h"

#include "test-fapi.h"
#include "fapi_util.h"
#include "fapi_int.h"

#include "esys_iutil.h"
#define LOGMODULE test
#include "util/log.h"
#include "util/aux_util.h"
#include "tss2_mu.h"

#define PASSWORD "abc"
#define SIGN_TEMPLATE  "sign,noDa"


json_object *
get_json_hex_string(const uint8_t *buffer, size_t size)
{

    char hex_string[size * 2 + 1];

    for (size_t i = 0, off = 0; i < size; i++, off += 2) {
        sprintf(&hex_string[off], "%02x", buffer[i]);
    }
    hex_string[(size) * 2] = '\0';
    json_object *jso = json_object_new_string(hex_string);
    return jso;
}

static TSS2_RC
auth_callback(
    char const *objectPath,
    char const *description,
    const char **auth,
    void *userData)
{
    UNUSED(description);
    UNUSED(userData);

    if (!objectPath) {
        return_error(TSS2_FAPI_RC_BAD_VALUE, "No path.");
    }

    *auth = PASSWORD;
    return TSS2_RC_SUCCESS;
}

/** Test the FAPI functions for TpmBlobs and certificates.
 *
 * Tested FAPI commands:
 *  - Fapi_Provision()
 *  - Fapi_SetAuthCB()
 *  - Fapi_CreateKey()
 *  - Fapi_GetEsysBlob()
 *  - Fapi_ChangeAuth()
 *  - Fapi_Delete()
 *
 * @param[in,out] context The FAPI_CONTEXT.
 * @retval EXIT_FAILURE
 * @retval EXIT_SUCCESS
 */
int
test_fapi_get_esys_blobs(FAPI_CONTEXT *context)
{
    TSS2_RC r;
    char          *publicKey = NULL;
    uint8_t       *publicblob = NULL;
    uint8_t       *privateblob = NULL;
    char          *path_list = NULL;
    json_object   *jso = NULL;
    char          *nvPath = "/nv/Owner/myNV";
    uint8_t       *data = NULL;
    size_t         data_size;
    TPMS_CONTEXT   key_context;
    size_t         offset = 0;
    ESYS_TR        esys_handle;
    uint8_t        type;

    /* We need to reset the passwords again, in order to not brick physical TPMs */
    r = Fapi_Provision(context, NULL, NULL, NULL);
    goto_if_error(r, "Error Fapi_Provision", error);

    r = Fapi_SetAuthCB(context, auth_callback, NULL);
    goto_if_error(r, "Error SetPolicyAuthCallback", error);

    /* Password set and noda set */
    r = Fapi_CreateNv(context, nvPath, "", 10, "", PASSWORD);
    goto_if_error(r, "Error Fapi_CreateNv", error);

    /* Create ESAPI NV object from path */
    r = Fapi_GetEsysBlob(context,nvPath, &type,
                         &data, &data_size);
    goto_if_error(r, "Error Fapi_GetEsysBlob", error);
    ASSERT(data != NULL);

    if (type != FAPI_ESYSBLOB_DESERIALIZE) {
        LOG_ERROR("Invalid type");
        goto error;
    }
    r = Esys_TR_Deserialize(context->esys, data, data_size, &esys_handle);
    goto_if_error(r, "Object deserializs", error);

    SAFE_FREE(data);
    r = Fapi_Delete(context, nvPath);
    goto_if_error(r, "Error Fapi_NV_Undefine", error);

    r = Fapi_CreateKey(context, "HS/SRK/mySignKey", SIGN_TEMPLATE, "",
                       PASSWORD);
    goto_if_error(r, "Error Fapi_CreateKey_Async", error);

    /* Create ESAPI key object from path */
    data = NULL;
    r = Fapi_GetEsysBlob(context, "HS/SRK/mySignKey", &type,
                         &data, &data_size);
    goto_if_error(r, "Error Fapi_GetEsysBlob", error);
    ASSERT(data != NULL);

    if (type != FAPI_ESYSBLOB_CONTEXTLOAD) {
        LOG_ERROR("Invalid type");
        goto error;
    }

    r = Tss2_MU_TPMS_CONTEXT_Unmarshal(data, data_size, &offset, &key_context);
    goto_if_error(r, "Context unmarshal", error);

    r = Esys_ContextLoad(context->esys, &key_context, &esys_handle);
    goto_if_error(r, "Context load", error);

    /* Variables for signing test */
    TPM2B_DIGEST pcr_digest_zero = {
        .size = 32,
        .buffer = { 0 }
    };

    TPMT_SIG_SCHEME inScheme = { .scheme = TPM2_ALG_ECDSA,
                                 .details.ecdsa = TPM2_ALG_SHA256 };

    TPMT_TK_HASHCHECK hash_validation = {
        .tag = TPM2_ST_HASHCHECK,
        .hierarchy = TPM2_RH_OWNER,
        .digest = {0}
    };

    TPM2B_AUTH authValue = {
        .size = sizeof(PASSWORD),
        .buffer = { 0 }
    };

    memcpy(&authValue.buffer[0], PASSWORD, sizeof(PASSWORD));

    TPMT_SIGNATURE *signature = NULL;

    r = Esys_TR_SetAuth(context->esys, esys_handle, &authValue);
    goto_if_error(r, "Error: TR_SetAuth", error);

    /* Check whether ESYS key can be used for signing. */
    r = Esys_Sign(
        context->esys,
        esys_handle,
        ESYS_TR_PASSWORD,
        ESYS_TR_NONE,
        ESYS_TR_NONE,
        &pcr_digest_zero,
        &inScheme,
        &hash_validation,
        &signature);
    goto_if_error(r, "Error: Sign", error);

    SAFE_FREE(signature);

    r = Esys_FlushContext(context->esys, esys_handle);
    goto_if_error(r, "Flush Context", error);

    SAFE_FREE(data);

    /* Create ESAPI persistent key object from path */
    data = NULL;
    r = Fapi_GetEsysBlob(context, "HS/SRK", &type,
                         &data, &data_size);
    goto_if_error(r, "Error Fapi_GetEsysBlob", error);
    ASSERT(data != NULL);

    if (type != FAPI_ESYSBLOB_DESERIALIZE) {
        LOG_ERROR("Invalid type");
        goto error;
    }

    r = Esys_TR_Deserialize(context->esys, data, data_size, &esys_handle);
    goto_if_error(r, "Object deserializs", error);

    TPM2B_PUBLIC inPublic = {
        .size = 0,
        .publicArea = {
            .type = TPM2_ALG_ECC,
            .nameAlg = TPM2_ALG_SHA256,
            .objectAttributes = (TPMA_OBJECT_USERWITHAUTH |
                                 TPMA_OBJECT_RESTRICTED |
                                 TPMA_OBJECT_SIGN_ENCRYPT |
                                 TPMA_OBJECT_FIXEDTPM |
                                 TPMA_OBJECT_FIXEDPARENT |
                                 TPMA_OBJECT_SENSITIVEDATAORIGIN),
            .authPolicy = {
                .size = 0,
            },
            .parameters.eccDetail = {
                .symmetric = {
                    .algorithm = TPM2_ALG_NULL,
                    .keyBits.aes = 128,
                    .mode.aes = TPM2_ALG_CFB,
                },
                .scheme = {
                    .scheme = TPM2_ALG_ECDSA,
                    .details = {
                        .ecdsa = {.hashAlg  = TPM2_ALG_SHA256}},
                },
                .curveID = TPM2_ECC_NIST_P256,
                .kdf = {
                    .scheme = TPM2_ALG_NULL,
                    .details = {}}
            },
            .unique.ecc = {
                .x = {.size = 0,.buffer = {}},
                .y = {.size = 0,.buffer = {}},
            },
        },
    };

    TPM2B_SENSITIVE_CREATE inSensitive = {
        .size = 0,
        .sensitive = {
            .userAuth = {
                .size = 0,
                .buffer = {0}
            },
            .data = {
                .size = 0,
                .buffer = {}
            }
        }
    };

    TPM2B_DATA outsideInfo = {
        .size = 0,
        .buffer = {}
        ,
    };

    TPML_PCR_SELECTION creationPCR = {
        .count = 0,
    };

    TPM2B_PUBLIC *outPublic = NULL;
    TPM2B_PRIVATE *outPrivate = NULL;

    r = Esys_Create(context->esys,
                    esys_handle,
                    ESYS_TR_PASSWORD, ESYS_TR_NONE, ESYS_TR_NONE,
                    &inSensitive,
                    &inPublic,
                    &outsideInfo,
                    &creationPCR,
                    &outPrivate,
                    &outPublic,
                    NULL,NULL, NULL);
    goto_if_error(r, "Error esys create ", error);

    SAFE_FREE(outPublic);
    SAFE_FREE(outPrivate);

    r = Fapi_Delete(context, "/");
    goto_if_error(r, "Error Fapi_Delete", error);

    json_object_put(jso);
    SAFE_FREE(data);
    SAFE_FREE(path_list);
    SAFE_FREE(publicblob);
    SAFE_FREE(privateblob);
    SAFE_FREE(publicKey);
    return EXIT_SUCCESS;

error:
    if (jso)
        json_object_put(jso);
    SAFE_FREE(data);
    Fapi_Delete(context, "/");
    SAFE_FREE(path_list);
    SAFE_FREE(publicblob);
    SAFE_FREE(privateblob);
    SAFE_FREE(publicKey);
    return EXIT_FAILURE;
}

int
test_invoke_fapi(FAPI_CONTEXT *fapi_context)
{
    return test_fapi_get_esys_blobs(fapi_context);
}
