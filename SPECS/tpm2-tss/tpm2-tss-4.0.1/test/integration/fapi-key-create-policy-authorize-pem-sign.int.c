/* SPDX-License-Identifier: BSD-2-Clause */
/*******************************************************************************
 * Copyright 2017-2018, Fraunhofer SIT sponsored by Infineon Technologies AG
 * All rights reserved.
 *******************************************************************************/

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <stdbool.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <errno.h>
#include <fcntl.h>
#include <unistd.h>

#include "tss2_fapi.h"

#include "test-fapi.h"

#define LOGMODULE test
#include "util/log.h"
#include "util/aux_util.h"

#define OBJECT_PATH "HS/SRK/mySignKey"
#define USER_DATA "my user data"
#define DESCRIPTION "PolicyAuthorize"

/** Test the FAPI functions for PolicyAuthoirze with signing.
 *
 * Tested FAPI commands:
 *  - Fapi_Provision()
 *  - Fapi_SetBranchCB()
 *  - Fapi_Import()
 *  - Fapi_CreateKey()
 *  - Fapi_Sign()
 *  - Fapi_List()
 *  - Fapi_Delete()
 *
 * Tested Policies:
 *  - PolicyNameHash
 *  - PolicyAuthorize
 *  - PolicyCpHash (Not entered, only as alternative branch)
 *
 * @param[in,out] context The FAPI_CONTEXT.
 * @retval EXIT_FAILURE
 * @retval EXIT_SUCCESS
 */
int
test_fapi_key_create_policy_authorize_pem_sign(FAPI_CONTEXT *context)
{
    TSS2_RC r;
    char *policy_pcr = "/policy/pol_pcr";
    char *policy_file_pcr;
    char *policy_file_authorize;
    char *policy_name_authorize = "/policy/pol_authorize";
    // uint8_t policyRef[] = { 1, 2, 3, 4, 5 };
    FILE *stream = NULL;
    char *json_policy = NULL;
    long policy_size;

    uint8_t *signature = NULL;
    char *publicKey = NULL;
    char *pathList = NULL;

#ifdef TEST_ECC
    if (strcmp(FAPI_PROFILE, "P_ECC") == 0) {
        policy_file_authorize = TOP_SOURCEDIR "/test/data/fapi/policy/pol_authorize_ecc_pem.json";
        policy_file_pcr = TOP_SOURCEDIR "/test/data/fapi/policy/pol_pcr16_0_ecc_authorized.json";
    } else if (strcmp(FAPI_PROFILE, "P_ECC384") == 0) {
        policy_file_authorize = TOP_SOURCEDIR "/test/data/fapi/policy/pol_authorize_ecc_pem_sha384.json";
        policy_file_pcr = TOP_SOURCEDIR "/test/data/fapi/policy/pol_pcr16_0_ecc_authorized_sha384.json";
    }
#else
    policy_file_pcr = TOP_SOURCEDIR "/test/data/fapi/policy/pol_pcr16_0_rsa_authorized.json";
    policy_file_authorize = TOP_SOURCEDIR "/test/data/fapi/policy/pol_authorize_rsa_pem.json";
#endif

    r = Fapi_Provision(context, NULL, NULL, NULL);
    goto_if_error(r, "Error Fapi_Provision", error);

    r = pcr_reset(context, 16);
    goto_if_error(r, "Error pcr_reset", error);

    /* Read in the first policy */
    stream = fopen(policy_file_pcr, "r");
    if (!stream) {
        LOG_ERROR("File %s does not exist", policy_file_pcr);
        goto error;
    }
    fseek(stream, 0L, SEEK_END);
    policy_size = ftell(stream);
    fclose(stream);
    json_policy = malloc(policy_size + 1);
    goto_if_null(json_policy,
            "Could not allocate memory for the JSON policy",
            TSS2_FAPI_RC_MEMORY, error);
    stream = fopen(policy_file_pcr, "r");
    ssize_t ret = read(fileno(stream), json_policy, policy_size);
    if (ret != policy_size) {
        LOG_ERROR("IO error %s.", policy_file_pcr);
        goto error;
    }
    json_policy[policy_size] = '\0';

    r = Fapi_Import(context, policy_pcr, json_policy);
    SAFE_FREE(json_policy);
    goto_if_error(r, "Error Fapi_List", error);

    /* Read in the authorize policy */
    stream = fopen(policy_file_authorize, "r");
    if (!stream) {
        LOG_ERROR("File %s does not exist", policy_file_authorize);
        goto error;
    }
    fseek(stream, 0L, SEEK_END);
    policy_size = ftell(stream);
    fclose(stream);
    json_policy = malloc(policy_size + 1);
    goto_if_null(json_policy,
            "Could not allocate memory for the JSON policy",
            TSS2_FAPI_RC_MEMORY, error);
    stream = fopen(policy_file_authorize, "r");
    ret = read(fileno(stream), json_policy, policy_size);
    if (ret != policy_size) {
        LOG_ERROR("IO error %s.", policy_file_authorize);
        goto error;
    }
    json_policy[policy_size] = '\0';

    r = Fapi_Import(context, policy_name_authorize, json_policy);
    SAFE_FREE(json_policy);
    goto_if_error(r, "Error Fapi_Import", error);

    /* Create key and use them to authorize the policy */
    r = Fapi_CreateKey(context, "HS/SRK/myPolicySignKey", "sign,noDa",
                       "", NULL);
    goto_if_error(r, "Error Fapi_CreateKey", error);

    /* Create the actual key */
    r = Fapi_CreateKey(context, OBJECT_PATH, "sign, noda",
                       policy_name_authorize, NULL);
    goto_if_error(r, "Error Fapi_CreateKey", error);

    /* Use the key */
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

    r = Fapi_Sign(context, OBJECT_PATH, NULL,
                  &digest.buffer[0], digest.size, &signature, &signatureSize,
                  &publicKey, NULL);
    goto_if_error(r, "Error Fapi_Sign", error);
    ASSERT(signature != NULL);
    ASSERT(publicKey != NULL);
    LOG_INFO("PublicKey: %s", publicKey);
    ASSERT(strstr(publicKey, "BEGIN PUBLIC KEY"));

    /* Cleanup */
    r = Fapi_Delete(context, "/");
    goto_if_error(r, "Error Fapi_Delete", error);

    SAFE_FREE(signature);
    SAFE_FREE(publicKey);

    return EXIT_SUCCESS;

error:
    Fapi_Delete(context, "/");
    SAFE_FREE(json_policy);
    SAFE_FREE(signature);
    SAFE_FREE(publicKey);
    SAFE_FREE(pathList);
    Fapi_Delete(context, "/");
    return EXIT_FAILURE;
}

int
test_invoke_fapi(FAPI_CONTEXT *fapi_context)
{
    return test_fapi_key_create_policy_authorize_pem_sign(fapi_context);
}
