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

static bool cb_called = false;

#define OBJECT_PATH "HS/SRK/mySignKey"
#define USER_DATA "my user data"
#define DESCRIPTION "PolicyAuthorize"

static TSS2_RC
branch_callback(
    char   const *objectPath,
    char   const *description MAYBE_UNUSED,
    char  const **branchNames MAYBE_UNUSED,
    size_t        numBranches,
    size_t       *selectedBranch,
    void         *userData MAYBE_UNUSED)
{
    char *profile_path;

    ASSERT(description != NULL);
    ASSERT(userData != NULL);
    ASSERT(branchNames != NULL);

    if (!objectPath) {
        return_error(TSS2_FAPI_RC_BAD_VALUE, "No path.");
    }

    int size = asprintf (&profile_path, "%s/%s", fapi_profile, OBJECT_PATH);
    if (size == -1)
        return TSS2_FAPI_RC_MEMORY;

    ASSERT(strlen(objectPath) == strlen(profile_path));
    free(profile_path);
    ASSERT(strlen(userData) == strlen((char*)USER_DATA));
    ASSERT(strlen(description) == strlen(DESCRIPTION));

    if (numBranches != 2) {
        LOG_ERROR("Wrong number of branches");
        return TSS2_FAPI_RC_GENERAL_FAILURE;
    }

    if (!strcmp(branchNames[0], "/policy/pol_name_hash"))
        *selectedBranch = 0;
    else if (!strcmp(branchNames[1], "/policy/pol_name_hash"))
        *selectedBranch = 1;
    else {
        LOG_ERROR("BranchName not found. Got \"%s\" and \"%s\"",
                  branchNames[0], branchNames[1]);
        return TSS2_FAPI_RC_GENERAL_FAILURE;
    }

    cb_called = true;

    return TSS2_RC_SUCCESS;

 error:
    exit(EXIT_FAILURE);
}

/** Test the FAPI functions for PolicyAuthoirze with signing.
 *
 * Tested FAPI commands:
 *  - Fapi_Provision()
 *  - Fapi_SetBranchCB()
 *  - Fapi_Import()
 *  - Fapi_CreateKey()
 *  - Fapi_AuthorizePolicy()
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
test_fapi_key_create_policy_authorize_sign(FAPI_CONTEXT *context)
{
    TSS2_RC r;
    char *policy_name_hash = "/policy/pol_name_hash";
    char *policy_file_name_hash = TOP_SOURCEDIR "/test/data/fapi/policy/pol_name_hash.json";

    /* This policy cannot succeed, but that's the intention. We authorize it but then choose
       the other policy from branch selection. */
    char *policy_cphash = "/policy/pol_cphash";
    char *policy_file_cphash = TOP_SOURCEDIR "/test/data/fapi/policy/pol_cphash.json";
    char *policy_name_authorize = "/policy/pol_authorize";
    char *policy_file_authorize = TOP_SOURCEDIR "/test/data/fapi/policy/pol_authorize.json";
    char *policy_name_authorize_outer = "/policy/pol_authorize_outer";
    char *policy_file_authorize_outer = TOP_SOURCEDIR
                                        "/test/data/fapi/policy/pol_authorize_outer.json";
    uint8_t policyRef[] = { 1, 2, 3, 4, 5 };
    FILE *stream = NULL;
    char *json_policy = NULL;
    long policy_size;

    uint8_t *signature = NULL;
    char *publicKey = NULL;
    char *certificate = NULL;
    char *pathList = NULL;

    r = Fapi_List(context, "/", &pathList);
    if (r != TSS2_FAPI_RC_NOT_PROVISIONED) {
        LOG_ERROR("It was not detected that provisioning was not made");
        goto error;
    }

    r = Fapi_Provision(context, NULL, NULL, NULL);
    goto_if_error(r, "Error Fapi_Provision", error);

    r = Fapi_List(context, "/P_DOES_NOT_EXIST", &pathList);
    if (r != TSS2_FAPI_RC_NOT_PROVISIONED) {
        LOG_ERROR("It was not detected that provisioning was not made");
        goto error;
    }

    r = Fapi_List(context, "/SRK/DOES_NOT_EXIST", &pathList);
    if (r != TSS2_FAPI_RC_PATH_NOT_FOUND) {
        LOG_ERROR("It was not detected that provisioning was not made");
        goto error;
    }

    r = pcr_reset(context, 16);
    goto_if_error(r, "Error pcr_reset", error);

    r = Fapi_SetBranchCB(context, branch_callback, USER_DATA);
    goto_if_error(r, "Error SetPolicybranchselectioncallback", error);

    /* Read in the first policy */
    stream = fopen(policy_file_name_hash, "r");
    if (!stream) {
        LOG_ERROR("File %s does not exist", policy_file_name_hash);
        goto error;
    }
    fseek(stream, 0L, SEEK_END);
    policy_size = ftell(stream);
    fclose(stream);
    json_policy = malloc(policy_size + 1);
    goto_if_null(json_policy,
            "Could not allocate memory for the JSON policy",
            TSS2_FAPI_RC_MEMORY, error);
    stream = fopen(policy_file_name_hash, "r");
    ssize_t ret = read(fileno(stream), json_policy, policy_size);
    if (ret != policy_size) {
        LOG_ERROR("IO error %s.", policy_file_name_hash);
        goto error;
    }
    json_policy[policy_size] = '\0';

    r = Fapi_Import(context, policy_name_hash, json_policy);
    SAFE_FREE(json_policy);
    goto_if_error(r, "Error Fapi_List", error);

    /* Read in the second policy */
    stream = fopen(policy_file_cphash, "r");
    if (!stream) {
        LOG_ERROR("File %s does not exist", policy_file_name_hash);
        goto error;
    }
    fseek(stream, 0L, SEEK_END);
    policy_size = ftell(stream);
    fclose(stream);
    json_policy = malloc(policy_size + 1);
    goto_if_null(json_policy,
            "Could not allocate memory for the JSON policy",
            TSS2_FAPI_RC_MEMORY, error);
    stream = fopen(policy_file_cphash, "r");
    ret = read(fileno(stream), json_policy, policy_size);
    if (ret != policy_size) {
        LOG_ERROR("IO error %s.", policy_file_name_hash);
        goto error;
    }
    json_policy[policy_size] = '\0';

    r = Fapi_Import(context, policy_cphash, json_policy);
    SAFE_FREE(json_policy);
    goto_if_error(r, "Error Fapi_List", error);

    /* Read in the third policy */
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

    /* Read in the fourth policy */
    stream = fopen(policy_file_authorize_outer, "r");
    if (!stream) {
        LOG_ERROR("File %s does not exist", policy_file_authorize_outer);
        goto error;
    }
    fseek(stream, 0L, SEEK_END);
    policy_size = ftell(stream);
    fclose(stream);
    json_policy = malloc(policy_size + 1);
    goto_if_null(json_policy,
            "Could not allocate memory for the JSON policy",
            TSS2_FAPI_RC_MEMORY, error);
    stream = fopen(policy_file_authorize_outer, "r");
    ret = read(fileno(stream), json_policy, policy_size);
    if (ret != policy_size) {
        LOG_ERROR("IO error %s.", policy_file_authorize_outer);
        goto error;
    }
    json_policy[policy_size] = '\0';

    r = Fapi_Import(context, policy_name_authorize_outer, json_policy);
    SAFE_FREE(json_policy);
    goto_if_error(r, "Error Fapi_Import", error);

    /* Create keys and use them to authorize the authorize policy */
    r = Fapi_CreateKey(context, "HS/SRK/myPolicySignKeyOuter", "sign,noDa",
                       "", NULL);
    goto_if_error(r, "Error Fapi_CreateKey", error);

    /* Create keys and use them to authorize policies */
    r = Fapi_CreateKey(context, "HS/SRK/myPolicySignKey", "sign,noDa",
                       "", NULL);
    goto_if_error(r, "Error Fapi_CreateKey", error);

    /* Create the actual key */
    r = Fapi_CreateKey(context, OBJECT_PATH, "sign, noda",
                       policy_name_authorize_outer, NULL);
    goto_if_error(r, "Error Fapi_CreateKey", error);

    /* Authorize the policies in sequence. */
    r = Fapi_AuthorizePolicy(context, policy_name_authorize,
                             "HS/SRK/myPolicySignKeyOuter", NULL, 0);
    goto_if_error(r, "Authorize policy", error);

    r = Fapi_AuthorizePolicy(context, policy_name_hash,
                             "HS/SRK/myPolicySignKey", policyRef, sizeof(policyRef));
    goto_if_error(r, "Authorize policy", error);

    r = Fapi_AuthorizePolicy(context, policy_cphash,
                             "HS/SRK/myPolicySignKey", policyRef, sizeof(policyRef));
    goto_if_error(r, "Authorize policy", error);

    /* The policy is authorized twice with idfferent keys in order to test the code that
       stores multiple authorizations inside the policy statements. */
    r = Fapi_CreateKey(context, "HS/SRK/myPolicySignKey2", "sign,noDa",
                       "", NULL);
    goto_if_error(r, "Error Fapi_CreateKey", error);

    r = Fapi_SetCertificate(context, OBJECT_PATH, "-----BEGIN "\
        "CERTIFICATE-----[...]-----END CERTIFICATE-----");
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
                  &publicKey, &certificate);
    goto_if_error(r, "Error Fapi_Sign", error);
    ASSERT(signature != NULL);
    ASSERT(publicKey != NULL);
    ASSERT(certificate != NULL);
    LOG_INFO("Public key: %s", publicKey);
    ASSERT(strstr(publicKey, "BEGIN PUBLIC KEY"));
    LOG_INFO("Certificate: %s", certificate);
    ASSERT(strstr(certificate, "BEGIN CERTIFICATE"));

    r = Fapi_List(context, "/", &pathList);
    goto_if_error(r, "Error Fapi_List", error);
    ASSERT(pathList != NULL);
    LOG_INFO("Pathlist: %s", pathList);
    char *check_pathList1 =
        "/" FAPI_PROFILE "/HS/SRK:/" FAPI_PROFILE "/HS:/" FAPI_PROFILE "/LOCKOUT:/"
        FAPI_PROFILE "/HE/EK:/" FAPI_PROFILE "/HE:/" FAPI_PROFILE "/HN:/policy/pol_name_hash:"
        "/policy/pol_cphash:/policy/pol_authorize_outer:/policy/pol_authorize:/" FAPI_PROFILE
        "/HS/SRK/myPolicySignKey2:/" FAPI_PROFILE "/HS/SRK/myPolicySignKey:/" FAPI_PROFILE
        "/HS/SRK/mySignKey:/" FAPI_PROFILE "/HS/SRK/myPolicySignKeyOuter";
    ASSERT(cmp_strtokens(pathList, check_pathList1, ":"));

    SAFE_FREE(pathList);

    pathList = NULL;
    r = Fapi_List(context, "/SRK/", &pathList);
    goto_if_error(r, "Error Fapi_List", error);
    ASSERT(pathList != NULL);
    LOG_INFO("Pathlist: %s", pathList);
    char *check_pathList2 =
        "/" FAPI_PROFILE "/HS/SRK:/" FAPI_PROFILE "/HS/SRK/myPolicySignKey2:/" FAPI_PROFILE
        "/HS/SRK/myPolicySignKey:/" FAPI_PROFILE "/HS/SRK/mySignKey:/" FAPI_PROFILE
        "/HS/SRK/myPolicySignKeyOuter";
    ASSERT(cmp_strtokens(pathList, check_pathList2, ":"));
    SAFE_FREE(pathList);

    pathList = NULL;
    r = Fapi_List(context, "/HS/", &pathList);
    goto_if_error(r, "Error Fapi_List", error);
    ASSERT(pathList != NULL);
    LOG_INFO("Pathlist: %s", pathList);
    char *check_pathList3 =
        "/" FAPI_PROFILE "/HS/SRK:/" FAPI_PROFILE "/HS:/" FAPI_PROFILE"/HS/SRK/myPolicySignKey2:/"
        FAPI_PROFILE "/HS/SRK/myPolicySignKey:/" FAPI_PROFILE "/HS/SRK/mySignKey:/" FAPI_PROFILE
        "/HS/SRK/myPolicySignKeyOuter";
    ASSERT(cmp_strtokens(pathList, check_pathList3, ":"));
    SAFE_FREE(pathList);

    LOG_WARNING("Next is a failure-test, and we expect errors in the log");
    pathList = NULL;
    r = Fapi_List(context, "XXX", &pathList);
    if (r == TSS2_RC_SUCCESS) {
        LOG_ERROR("Path XXX was found");
        goto error;
    }
    ASSERT(pathList == NULL);
    SAFE_FREE(pathList);

    pathList = NULL;
    r = Fapi_List(context, "/policy/", &pathList);
    goto_if_error(r, "Error Fapi_List", error);
    ASSERT(pathList != NULL);
    ASSERT(strlen(pathList) > ASSERT_SIZE);
    LOG_INFO("Pathlist: %s", pathList);
    char *check_pathList4 =
        "/policy/pol_name_hash:/policy/pol_cphash:/policy/pol_authorize_outer:/policy/pol_authorize";
    ASSERT(cmp_strtokens(pathList, check_pathList4, ":"));
    SAFE_FREE(pathList);

    /* Cleanup */
    r = Fapi_Delete(context, "/");
    goto_if_error(r, "Error Fapi_Delete", error);

    SAFE_FREE(signature);
    SAFE_FREE(publicKey);
    SAFE_FREE(certificate);

    if (!cb_called) {
        LOG_ERROR("Branch selection callback was not called.");
        return EXIT_FAILURE;
    }

    return EXIT_SUCCESS;

error:
    Fapi_Delete(context, "/");
    SAFE_FREE(json_policy);
    SAFE_FREE(signature);
    SAFE_FREE(publicKey);
    SAFE_FREE(certificate);
    SAFE_FREE(pathList);
    Fapi_Delete(context, "/");
    return EXIT_FAILURE;
}

int
test_invoke_fapi(FAPI_CONTEXT *fapi_context)
{
    return test_fapi_key_create_policy_authorize_sign(fapi_context);
}
