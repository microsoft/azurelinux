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
#include "tss2_esys.h"
#include "tss2_tcti.h"

#include "test-fapi.h"

#define LOGMODULE test
#define LOGDEFAULT LOGLEVEL_INFO
#include "util/log.h"
#include "util/aux_util.h"

#define NV_SIZE 34
#define PASSWORD ""
#define SIGN_TEMPLATE  "sign"

static TSS2_RC
check_tpm_cmd(FAPI_CONTEXT *context, TPM2_CC command_code)
{
    TSS2_RC r;
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys;
    TPMS_CAPABILITY_DATA *cap_data;

    r = Fapi_GetTcti(context, &tcti);
    goto_if_error(r, "Error Fapi_GetTcti", error);

    r = Esys_Initialize(&esys, tcti, NULL);
    goto_if_error(r, "Error Fapi_GetTcti", error);

    r = Esys_GetCapability(esys,
                           ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE,
                           TPM2_CAP_COMMANDS, command_code, 1, NULL, &cap_data);
    Esys_Finalize(&esys);
    return_if_error(r, "Error: GetCapabilities");

    if ((cap_data->data.command.commandAttributes[0] & TPMA_CC_COMMANDINDEX_MASK) ==
            command_code) {
        free(cap_data);
        return TSS2_RC_SUCCESS;
    } else {
        free(cap_data);
        return TSS2_FAPI_RC_NOT_IMPLEMENTED;
    }

error:
    return r;
}

static char *
read_policy(FAPI_CONTEXT *context, char *policy_name)
{
    FILE *stream = NULL;
    long policy_size;
    char *json_policy = NULL;
    char policy_file[1024];

    if (snprintf(&policy_file[0], 1023, TOP_SOURCEDIR "/test/data/fapi%s.json", policy_name) < 0)
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
    stream = fopen(policy_file, "r");
    ssize_t ret = read(fileno(stream), json_policy, policy_size);
    if (ret != policy_size) {
        LOG_ERROR("IO error %s.", policy_file);
        return NULL;
    }
    json_policy[policy_size] = '\0';
    return json_policy;
}

/** Test the FAPI key signing with PolicyAuthorizeNV.
 *
 * Tested FAPI commands:
 *  - Fapi_GetTcti()
 *  - Fapi_Provision()
 *  - Fapi_CreateNv()
 *  - Fapi_Import()
 *  - Fapi_WriteAuthorizeNv()
 *  - Fapi_CreateKey()
 *  - Fapi_Sign()
 *  - Fapi_Delete()
 *
 * Tested Policies:
 *  - PolicyAuthorizeNv
 *
 * @param[in,out] context The FAPI_CONTEXT.
 * @retval EXIT_FAILURE
 * @retval EXIT_SUCCESS
 */

#ifndef POLICY_AUTHORIZE_NV
#define POLICY_AUTHORIZE_NV "/policy/pol_authorize_nv"
#endif


int
test_fapi_key_create_policy_authorize_nv(FAPI_CONTEXT *context)

{
    TSS2_RC r;
    char *nvPathPolicy = "/nv/Owner/myNV";
    char *policy_authorize_nv;
    char extended_name[1024];
    char *policy_pcr2 = "/policy/pol_pcr16_0";
    char *json_policy = NULL;

    uint8_t *signature = NULL;
    char    *publicKey = NULL;
    char    *certificate = NULL;
    size_t  policy_nv_auth_size;

    if (check_tpm_cmd(context, TPM2_CC_PolicyAuthorizeNV) != TPM2_RC_SUCCESS) {
        LOG_WARNING("Command PolicyAuthorizeNV not available.");
        return EXIT_SKIP;
    }

    if (strcmp(FAPI_PROFILE, "P_ECC384") == 0) {
        if (snprintf(&extended_name[0], 1023, "%s_sha384", POLICY_AUTHORIZE_NV) < 0) {
            LOG_ERROR("snprint failed");
            return EXIT_FAILURE;
        }
        policy_authorize_nv = &extended_name[0];
    } else {
        policy_authorize_nv = POLICY_AUTHORIZE_NV;
    }

    LOG_INFO("Policy File: %s", policy_authorize_nv);

    r = Fapi_Provision(context, NULL, NULL, NULL);
    goto_if_error(r, "Error Fapi_Provision", error);

     if (strcmp(FAPI_PROFILE, "P_ECC") == 0) {
        policy_nv_auth_size = 34;
    } else if (strcmp(FAPI_PROFILE, "P_ECC384") == 0) {
        policy_nv_auth_size = 50;
    } else {
        LOG_ERROR("No appropriate policy file exists!");
        return EXIT_FAILURE;
    }

    /* Create NV object for storing the policy */
    r = Fapi_CreateNv(context, nvPathPolicy, "noda", policy_nv_auth_size, "", "");
    goto_if_error(r, "Error Fapi_CreateNv", error);

    r = pcr_reset(context, 16);
    goto_if_error(r, "Error pcr_reset", error);

    json_policy = read_policy(context, policy_authorize_nv);
    if (!json_policy)
        goto error;

    r = Fapi_Import(context, policy_authorize_nv, json_policy);
    goto_if_error(r, "Error Fapi_Import", error);
    SAFE_FREE(json_policy);

    json_policy = read_policy(context, policy_pcr2);
    if (!json_policy)
        goto error;

    r = Fapi_Import(context, policy_pcr2, json_policy);
    goto_if_error(r, "Error Fapi_Import", error);

    r = Fapi_WriteAuthorizeNv(context,nvPathPolicy, policy_pcr2);
    goto_if_error(r, "Error Fapi_WriteAuthorizeNv", error);

    r = Fapi_CreateKey(context, "/HS/SRK/myPolicySignKey", "sign",
                       "", PASSWORD);
    goto_if_error(r, "Error Fapi_CreateKey", error);

    r = Fapi_CreateKey(context, "/HS/SRK/mySignKey", SIGN_TEMPLATE,
                       policy_authorize_nv, PASSWORD);
    goto_if_error(r, "Error Fapi_CreateKey", error);

    r = Fapi_SetCertificate(context, "HS/SRK/mySignKey", "-----BEGIN "\
        "CERTIFICATE-----[...]-----END CERTIFICATE-----");
    goto_if_error(r, "Error Fapi_CreateKey", error);

    size_t signatureSize = 0;

    TPM2B_DIGEST digest = {
        .size = 20,
        .buffer = {
            0x67, 0x68, 0x03, 0x3e, 0x21, 0x64, 0x68, 0x24, 0x7b, 0xd0,
            0x31, 0xa0, 0xa2, 0xd9, 0x87, 0x6d, 0x79, 0x81, 0x8f, 0x8f,
            0x31, 0xa0, 0xa2, 0xd9, 0x87, 0x6d, 0x79, 0x81, 0x8f, 0x8f,
            0x41, 0x42
        }
    };

    r = Fapi_Sign(context, "/HS/SRK/mySignKey", NULL,
                  &digest.buffer[0], digest.size, &signature, &signatureSize,
                  &publicKey, &certificate);
    goto_if_error(r, "Error Fapi_Sign", error);
    ASSERT(signature);
    ASSERT(publicKey);
    ASSERT(certificate);

    ASSERT(strstr(publicKey, "BEGIN PUBLIC KEY"));
    ASSERT(strstr(certificate, "BEGIN CERTIFICATE"));

    r = Fapi_Delete(context, policy_authorize_nv);
    goto_if_error(r, "Error Fapi_Delete", error);

    r = Fapi_Delete(context, nvPathPolicy);
    goto_if_error(r, "Error Fapi_NV_Undefine", error);

    r = Fapi_Delete(context, "/");
    goto_if_error(r, "Error Fapi_Delete", error);

    SAFE_FREE(json_policy);
    SAFE_FREE(signature);
    SAFE_FREE(publicKey);
    SAFE_FREE(certificate);
    return EXIT_SUCCESS;

error:
    Fapi_Delete(context, "/");
    SAFE_FREE(json_policy);
    SAFE_FREE(signature);
    SAFE_FREE(publicKey);
    SAFE_FREE(certificate);
    return EXIT_FAILURE;
}

int
test_invoke_fapi(FAPI_CONTEXT *context)
{
    return test_fapi_key_create_policy_authorize_nv(context);
}
