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
#include <inttypes.h>
#include <string.h>
#include <errno.h>
#include <fcntl.h>
#include <unistd.h>


#include "tss2_fapi.h"

#include "test-fapi.h"

#define LOGMODULE test
#include "util/log.h"
#include "util/aux_util.h"

#define NV_SIZE 34
#define PASSWORD "abc"
#define SIGN_TEMPLATE "sign"

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

static char *
read_policy(FAPI_CONTEXT *context, char *policy_name)
{
    FILE *stream = NULL;
    long policy_size;
    char *json_policy = NULL;
    char policy_file[1024];

    if (snprintf(&policy_file[0], 1023, TOP_SOURCEDIR "/test/data/fapi/%s.json", policy_name) < 0)
        return NULL;

    stream = fopen(policy_file, "r");
    if (!stream) {
        LOG_ERROR("File %s does not exist", policy_file);
        return NULL;
    }
    fseek(stream, 0L, SEEK_END);
    policy_size = ftell(stream);
    fclose(stream);
    json_policy = malloc(policy_size + 1);
    return_if_null(json_policy,
            "Could not allocate memory for the JSON policy",
            NULL);
    stream = fopen(policy_file, "r");
    ssize_t ret = read(fileno(stream), json_policy, policy_size);
    if (ret != policy_size) {
        LOG_ERROR("IO error %s.", policy_file);
        return NULL;
    }
    json_policy[policy_size] = '\0';
    return json_policy;
}

/** Test the FAPI PolicySecret and PolicyAuthValue handling.
 *
 * Tested FAPI commands:
 *  - Fapi_Provision()
 *  - Fapi_Import()
 *  - Fapi_CreateNv()
 *  - Fapi_CreateKey()
 *  - Fapi_Sign()
 *  - Fapi_SetAuthCB()
 *  - Fapi_Delete()
 *
 * Tested Policies:
 *  - PolicySecret
 *  - PolicyAuthValue
 *
 * @param[in,out] context The FAPI_CONTEXT.
 * @retval EXIT_FAILURE
 * @retval EXIT_SUCCESS
 */
int
test_fapi_key_create_policy_secret_nv_sign(FAPI_CONTEXT *context)
{
    TSS2_RC r;
    char *nv_path_auth_object = "/nv/Owner/myNV";
    char *policy_nv = "/policy/pol_auth_value";
    char *policy_secret = "/policy/pol_secret";
    char *sign_key = "/HS/SRK/mySignkey";
    char *json_policy = NULL;

    uint8_t *signature = NULL;
    char    *publicKey = NULL;
    char    *certificate = NULL;

    r = Fapi_Provision(context, NULL, NULL, NULL);
    goto_if_error(r, "Error Fapi_Provision", error);

    json_policy = read_policy(context, policy_nv);
    if (!json_policy)
        goto error;

    r = Fapi_Import(context, policy_nv, json_policy);
    goto_if_error(r, "Error Fapi_Import", error);

    /* Create NV Object with policy which will be used for key authorization */
    r = Fapi_CreateNv(context, nv_path_auth_object, "noda", 34, policy_nv, PASSWORD);
    goto_if_error(r, "Error Fapi_CreateNv", error);

    SAFE_FREE(json_policy);

    json_policy = read_policy(context, policy_secret);
    if (!json_policy)
        goto error;

    r = Fapi_Import(context, policy_secret, json_policy);
    goto_if_error(r, "Error Fapi_Import", error);

    r = Fapi_CreateKey(context, sign_key, SIGN_TEMPLATE,
                       policy_secret, "");
    goto_if_error(r, "Error Fapi_CreateKey", error);

    r = Fapi_SetCertificate(context, sign_key, "-----BEGIN "\
        "CERTIFICATE-----[...]-----END CERTIFICATE-----");
    goto_if_error(r, "Error Fapi_CreateKey", error);

    size_t signatureSize = 0;

    TPM2B_DIGEST digest = {
        .size = 32,
        .buffer = {
            0x67, 0x68, 0x03, 0x3e, 0x21, 0x64, 0x68, 0x24, 0x7b, 0xd0,
            0x31, 0xa0, 0xa2, 0xd9, 0x87, 0x6d, 0x79, 0x81, 0x8f, 0x8f,
            0x31, 0xa0, 0xa2, 0xd9, 0x87, 0x6d, 0x79, 0x81, 0x8f, 0x8f,
            0x41, 0x42
        }
    };

    LOG_ERROR("***** START TEST ERROR ******");
    r = Fapi_Sign(context, sign_key, NULL,
                  &digest.buffer[0], digest.size, &signature, &signatureSize,
                  &publicKey, &certificate);

    LOG_ERROR("***** END TEST ERROR ******");

    if (r == TSS2_RC_SUCCESS)
        goto error;

    ASSERT(signature == NULL);
    ASSERT(publicKey == NULL);
    ASSERT(certificate == NULL);

    r = Fapi_SetAuthCB(context, auth_callback, "");
    goto_if_error(r, "Error SetPolicyAuthCallback", error);

    signature = NULL;
    publicKey = NULL;
    certificate = NULL;
    r = Fapi_Sign(context, sign_key, NULL,
                  &digest.buffer[0], digest.size, &signature, &signatureSize,
                  &publicKey, &certificate);
    goto_if_error(r, "Error Fapi_Sign", error);
    ASSERT(signature != NULL);
    ASSERT(publicKey != NULL);
    ASSERT(certificate != NULL);
    ASSERT(strstr(publicKey, "BEGIN PUBLIC KEY"));
    ASSERT(strstr(certificate, "BEGIN CERTIFICATE"));


    r = Fapi_Delete(context, nv_path_auth_object);
    goto_if_error(r, "Error Fapi_NV_Undefine", error);

    r = Fapi_Delete(context, "/");
    goto_if_error(r, "Error Fapi_Delete", error);

    SAFE_FREE(signature);
    SAFE_FREE(publicKey);
    SAFE_FREE(certificate);
    SAFE_FREE(json_policy);
    return EXIT_SUCCESS;

error:
    Fapi_Delete(context, "/");
    SAFE_FREE(signature);
    SAFE_FREE(publicKey);
    SAFE_FREE(certificate);
    SAFE_FREE(json_policy);
    return EXIT_FAILURE;
}

int
test_invoke_fapi(FAPI_CONTEXT *context)
{
    return test_fapi_key_create_policy_secret_nv_sign(context);
}
