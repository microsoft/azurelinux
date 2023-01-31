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
#include <unistd.h>

#include "tss2_fapi.h"
#include "tss2_esys.h"

#include "test-fapi.h"
#define LOGMODULE test
#include "util/log.h"
#include "util/aux_util.h"

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

/** Test the FAPI PolicyCpHash but means of AuthorizeNv.
 *
 * Tested FAPI commands:
 *  - Fapi_GetTcti()
 *  - Fapi_Provision()
 *  - Fapi_Import()
 *  - Fapi_CreateNv()
 *  - Fapi_WriteAuthorizeNv
 *  - Fapi_NvWrite()
 *
 * Tested Policies:
 *  - PolicyAuthorize
 *  - PolicyCpHash
 *
 * @param[in,out] context The FAPI_CONTEXT.
 * @retval EXIT_FAILURE
 * @retval EXIT_SUCCESS
 */
int
test_fapi_nv_authorizenv_cphash(FAPI_CONTEXT *context)
{
    TSS2_RC r;
    ssize_t ret;
    uint8_t data[] = { 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 };
    char *policy1_name = "/policy/pol_authorize_nv";
    char *policy1_file = TOP_SOURCEDIR "/test/data/fapi/policy/pol_authorize_nv.json";
    char *policy2_name;
    char *policy2_file;
    size_t policy_nv_auth_size;
    FILE *stream = NULL;
    char json[1024];
    char *policy = NULL;

    if (check_tpm_cmd(context, TPM2_CC_PolicyAuthorizeNV) != TPM2_RC_SUCCESS) {
        LOG_WARNING("Command PolicyAuthorizeNV not available.");
        goto error;
    }

    r = Fapi_Provision(context, NULL, NULL, NULL);
    goto_if_error(r, "Error Fapi_Provision", error);

    if (strcmp(FAPI_PROFILE, "P_ECC384") == 0) {
        policy2_name = "/policy/pol_cphash_sha384";
        policy2_file = TOP_SOURCEDIR "/test/data/fapi/policy/pol_cphash_sha384.json";
        policy_nv_auth_size = 50;
    } else {
        policy2_name = "/policy/pol_cphash";
        policy2_file = TOP_SOURCEDIR "/test/data/fapi/policy/pol_cphash.json";
        policy_nv_auth_size = 34;
    }

    memset(&json[0], 0, sizeof(json));
    stream = fopen(policy1_file, "r");
    ret = read(fileno(stream), &json[0], sizeof(json));
    fclose(stream);
    if (ret < 0) {
        LOG_ERROR("IO error %s.", policy1_file);
        goto error;
    }
    json[ret] = '\0';
    r = Fapi_Import(context, policy1_name, json);
    goto_if_error(r, "Error Fapi_Import", error);

    memset(&json[0], 0, sizeof(json));
    stream = fopen(policy2_file, "r");
    ret = read(fileno(stream), &json[0], sizeof(json));
    fclose(stream);
    if (ret < 0) {
        LOG_ERROR("IO error %s.", policy2_file);
        goto error;
    }
    json[ret] = '\0';
    r = Fapi_Import(context, policy2_name, json);
    goto_if_error(r, "Error Fapi_Import", error);

    /* Start the test */

    r = Fapi_CreateNv(context, "/nv/Owner/myNV", "", policy_nv_auth_size, "", "");
    goto_if_error(r, "Error Fapi_CreateNv", error);

    r = Fapi_CreateNv(context, "/nv/Owner/myNV2", "", sizeof(data), policy1_name, "");
    goto_if_error(r, "Error Fapi_CreateNv", error);

    r = Fapi_ExportPolicy(context, "/nv/Owner/myNV2", &policy);
    goto_if_error(r, "Error Fapi_ExportPolicy", error);
    ASSERT(policy != NULL);
    LOG_INFO("Policy authorize nv: %s", policy);
    char *fields_policy_authorize[] =  { "policy", "0", "type" };
    CHECK_JSON_FIELDS(policy, fields_policy_authorize, "POLICYAUTHORIZENV", error);

    r = Fapi_WriteAuthorizeNv(context, "/nv/Owner/myNV", policy2_name);
    goto_if_error(r, "Error Fapi_WriteAuthorizeNv", error);

    LOG_ERROR("XXXX Write");
    r = Fapi_NvWrite(context, "/nv/Owner/myNV2", &data[0], sizeof(data));
    goto_if_error(r, "Error Fapi_NvWrite", error);

    /* Cleanup */

    SAFE_FREE(policy);

    r = Fapi_Delete(context, "/nv/Owner/myNV");
    goto_if_error(r, "Error Fapi_NV_Undefine", error);

    r = Fapi_Delete(context, "/nv/Owner/myNV2");
    goto_if_error(r, "Error Fapi_NV_Undefine", error);

    r = Fapi_Delete(context, "/");
    goto_if_error(r, "Error Fapi_Delete", error);

    return EXIT_SUCCESS;

error:
    if (policy) {
        SAFE_FREE(policy);
    }
    Fapi_Delete(context, "/");
    return EXIT_FAILURE;
}

int
test_invoke_fapi(FAPI_CONTEXT *context)
{
    return test_fapi_nv_authorizenv_cphash(context);
}
