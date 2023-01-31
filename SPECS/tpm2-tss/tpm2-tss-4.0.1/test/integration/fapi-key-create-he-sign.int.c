/* SPDX-License-Identifier: BSD-2-Clause */
/*******************************************************************************
 * Copyright 2017-2018, Fraunhofer SIT sponsored by Infineon Technologies AG
 * All rights reserved.
 *******************************************************************************/

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <stdlib.h>
#include <string.h>

#include "tss2_fapi.h"

#include "test-fapi.h"
#include "fapi_util.h"
#include "fapi_int.h"

#include "esys_iutil.h"
#define LOGMODULE test
#include "util/log.h"
#include "util/aux_util.h"

#define PASSWORD "abc"
#define SIGN_TEMPLATE  "sign,noDa"

static bool cb_called = false;

static TSS2_RC
branch_callback(
    char   const *objectPath,
    char   const *description,
    char  const **branchNames,
    size_t        numBranches,
    size_t       *selectedBranch,
    void         *userData)
{
    UNUSED(description);
    UNUSED(userData);

    if (numBranches != 2) {
        LOG_ERROR("Wrong number of branches");
        return TSS2_FAPI_RC_GENERAL_FAILURE;
    }

    /* The policy branch A A will be used. */

    if (!strcmp(branchNames[0], "A"))
        *selectedBranch = 0;
    else if (!strcmp(branchNames[1], "B"))
        *selectedBranch = 1;
    else {
        LOG_ERROR("BranchName not found. Got \"%s\" and \"%s\"",
                  branchNames[0], branchNames[1]);
        return TSS2_FAPI_RC_GENERAL_FAILURE;
    }

    cb_called = true;
    return TSS2_RC_SUCCESS;
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

/** Test creation of a signing key in the endorsement hierarchy.
 *
 * Tested FAPI commands:
 *  - Fapi_Provision()
 *  - Fapi_SetAuthCB()
 *  - Fapi_CreateKey()
 *  - Fapi_Sign()
 *  - Fapi_VerifySignature()
 *  - Fapi_List()
 *  - Fapi_Delete()
 *
 * @param[in,out] context The FAPI_CONTEXT.
 * @retval EXIT_FAILURE
 * @retval EXIT_SUCCESS
 */
int
test_fapi_key_create_he_sign(FAPI_CONTEXT *context)
{
    TSS2_RC r;
    char *sigscheme = NULL;

    uint8_t       *signature = NULL;
    char          *publicKey = NULL;
    char          *path_list = NULL;

    if (strncmp("P_ECC", fapi_profile, 5) != 0)
        sigscheme = "RSA_PSS";

    /* We need to reset the passwords again, in order to not brick physical TPMs */
    r = Fapi_Provision(context, NULL, NULL, NULL);
    goto_if_error(r, "Error Fapi_Provision", error);

    r = Fapi_SetBranchCB(context, branch_callback, NULL);
    goto_if_error(r, "Error SetPolicybranchselectioncallback", error);

    r = Fapi_SetAuthCB(context, auth_callback, NULL);
    goto_if_error(r, "Error SetPolicyAuthCallback", error);

    r = Fapi_CreateKey(context, "HE/EK/mySignKey", SIGN_TEMPLATE , "",
                       PASSWORD);

    goto_if_error(r, "Error Fapi_CreateKey", error);
    size_t signatureSize = 0;

    TPM2B_DIGEST digest = {
        .size = 32,
        .buffer = {
            0x67, 0x68, 0x03, 0x3e, 0x21, 0x64, 0x68, 0x24, 0x7b, 0xd0,
            0x31, 0xa0, 0xa2, 0xd9, 0x87, 0x6d, 0x79, 0x81, 0x8f, 0x8f,
            0x31, 0xa0, 0xa2, 0xd9, 0x87, 0x6d, 0x79, 0x81, 0x8f, 0x8f,
            0x67, 0x68
        }
    };


    r = Fapi_Sign(context, "HE/EK/mySignKey", sigscheme,
                  &digest.buffer[0], digest.size, &signature, &signatureSize,
                  &publicKey, NULL);
    goto_if_error(r, "Error Fapi_Sign", error);
    ASSERT(signature != NULL);
    ASSERT(publicKey != NULL);
    ASSERT(strlen(publicKey) > ASSERT_SIZE);

    r = Fapi_VerifySignature(context, "HE/EK/mySignKey",
                  &digest.buffer[0], digest.size, signature, signatureSize);
    goto_if_error(r, "Error Fapi_VerifySignature", error);

     r = Fapi_Delete(context, "/");
    goto_if_error(r, "Error Fapi_Delete", error);

    SAFE_FREE(path_list);
    SAFE_FREE(publicKey);
    SAFE_FREE(signature);
    return EXIT_SUCCESS;

error:
    Fapi_Delete(context, "/");
    SAFE_FREE(path_list);
    SAFE_FREE(publicKey);
    SAFE_FREE(signature);
    return EXIT_FAILURE;
}

int
test_invoke_fapi(FAPI_CONTEXT *fapi_context)
{
    return test_fapi_key_create_he_sign(fapi_context);
}
