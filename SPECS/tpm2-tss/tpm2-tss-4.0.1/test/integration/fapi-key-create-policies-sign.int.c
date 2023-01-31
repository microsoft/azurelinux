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

#include "tss2_fapi.h"

#define LOGMODULE test
#include "util/log.h"
#include "util/aux_util.h"
#include "test-fapi.h"

#ifdef TEST_PASSWORD
#define PASSWORD "abc"
#else
#define PASSWORD ""
#endif

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
#define SIGN_TEMPLATE  "sign,noDa"

/** Test several FAPI policies by usage of signing key.
 *
 * Which test case will be executed is determined by the compiler switches:
 *   TEST_POLICY_PASSWORD, TEST_POLICY_AUTH_VALUE, TEST_POLICY_LOCALITY
 *   TEST_POLICY_PHYSICAL_PRESENCE, TEST_POLICY_COMMAND_CODE, TEST_POLICY_COUNTERTIMER.
 *
 * Tested FAPI commands:
 *  - Fapi_Provision()
 *  - Fapi_Import()
 *  - Fapi_CreateKey()
 *  - Fapi_SetAuthCB()
 *  - Fapi_Sign()
 *  - Fapi_Delete()
 *
 * Tested Policies:
 *  - PolicyPassword
 *  - PolicyAuthValue
 *  - PolicyLocality
 *  - PolicyPhysicalPresence
 *  - PolicyCommandCode
 *  - PolicyCounterTimer
 *
 * @param[in,out] context The FAPI_CONTEXT.
 * @retval EXIT_FAILURE
 * @retval EXIT_SUCCESS
 */
int
test_fapi_key_create_policies_sign(FAPI_CONTEXT *context)
{
    TSS2_RC r;

#if defined(TEST_POLICY_PASSWORD)
    char *policy_name = "/policy/pol_password";
    char *policy_file = FAPI_POLICIES "/policy/pol_password.json";
#elif defined(TEST_POLICY_AUTH_VALUE)
    char *policy_name = "/policy/pol_auth_value";
    char *policy_file = FAPI_POLICIES "/policy/pol_auth_value.json";
#elif defined(TEST_POLICY_LOCALITY)
    char *policy_name = "/policy/pol_locality";
    char *policy_file = FAPI_POLICIES "/policy/pol_locality.json";
#elif defined(TEST_POLICY_PHYSICAL_PRESENCE)
    char *policy_name = "/policy/pol_physical_presence";
    char *policy_file = FAPI_POLICIES "/policy/pol_physical_presence.json";
#elif defined(TEST_POLICY_COMMAND_CODE)
    char *policy_name = "/policy/pol_command_code";
    char *policy_file = FAPI_POLICIES "/policy/pol_command_code.json";
#elif defined(TEST_POLICY_COUNTERTIMER)
    char *policy_name = "/policy/pol_countertimer";
    char *policy_file = FAPI_POLICIES "/policy/pol_countertimer.json";
#else
#error "Please define POLICY_PASSWORD,_AUTH_VALUE,_LOCALITY,_PHYSICAL_PRESENCE,_COMMAND_CODE,_COUNTERTIMER"
#endif

    FILE *stream = NULL;
    uint8_t *signature =NULL;
    char    *publicKey = NULL;
    char    *certificate = NULL;
    char *json_policy = NULL;
    long policy_size;

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

    r = Fapi_CreateKey(context, "HS/SRK/mySignKey", SIGN_TEMPLATE,
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

    r = Fapi_SetAuthCB(context, auth_callback, "");
    goto_if_error(r, "Error SetPolicyAuthCallback", error);

    r = Fapi_Sign(context, "HS/SRK/mySignKey", NULL,
                  &digest.buffer[0], digest.size, &signature, &signatureSize,
                  &publicKey, &certificate);

#if defined(TEST_POLICY_PHYSICAL_PRESENCE)
    if (number_rc(r) == TPM2_RC_PP) {
        LOG_WARNING("Test requires physical presence.");
        goto skip;
    } else if (r == TPM2_RC_COMMAND_CODE) {
        LOG_WARNING("Command not supported, probably PolicyPhysicalPresence");
        goto skip;
    }
#endif /* TEST_POLICY_PHYSICAL_PRESENCE */
    goto_if_error(r, "Error Fapi_Sign", error);
    ASSERT(signature != NULL);
    ASSERT(publicKey != NULL);
    ASSERT(certificate != NULL);
    ASSERT(strstr(publicKey, "BEGIN PUBLIC KEY"));
    ASSERT(strstr(certificate, "BEGIN CERTIFICATE"));

    r = Fapi_Delete(context, "/HS/SRK/mySignKey");
    goto_if_error(r, "Error Fapi_Delete", error);

    r = Fapi_Delete(context, "/");
    goto_if_error(r, "Error Fapi_Delete", error);

    SAFE_FREE(json_policy);
    SAFE_FREE(signature);
    SAFE_FREE(publicKey);
    SAFE_FREE(certificate);
    return EXIT_SUCCESS;

#if defined(TEST_POLICY_PHYSICAL_PRESENCE)
    r = Fapi_Delete(context, "/HS/SRK/mySignKey");
    goto_if_error(r, "Error Fapi_Delete", error);

    r = Fapi_Delete(context, "/");
    goto_if_error(r, "Error Fapi_Delete", error);

skip:
    Fapi_Delete(context, "/");
    SAFE_FREE(json_policy);
    SAFE_FREE(signature);
    SAFE_FREE(publicKey);
    SAFE_FREE(certificate);
    return EXIT_SKIP;
#endif /* TEST_POLICY_PHYSICAL_PRESENCE */

error:
    Fapi_Delete(context, "/");

    SAFE_FREE(json_policy);
    SAFE_FREE(signature);
    SAFE_FREE(publicKey);
    SAFE_FREE(certificate);
    return EXIT_FAILURE;
}

int
test_invoke_fapi(FAPI_CONTEXT *fapi_context)
{
    return test_fapi_key_create_policies_sign(fapi_context);
}
