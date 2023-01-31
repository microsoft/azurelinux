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

#include "test-fapi.h"
#include "fapi_util.h"
#include "fapi_int.h"

#include "esys_iutil.h"
#define LOGMODULE test
#include "util/log.h"
#include "util/aux_util.h"

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

/** Test creation of a primary in the NULL hiearchy and directly it the hierarchy.
 *
 * Tested FAPI commands:
 *  - Fapi_Provision()
 *  - Fapi_SetAuthCB()
 *  - Fapi_CreateKey()
 *  - Fapi_Sign()
 *  - Fapi_VerifySignature()
 *  - Fapi_Delete()
 *
 * @param[in,out] context The FAPI_CONTEXT.
 * @retval EXIT_FAILURE
 * @retval EXIT_SUCCESS
 */
int
test_fapi_key_create_null_sign(FAPI_CONTEXT *context)
{
    TSS2_RC        r;
    char          *sigscheme = NULL;
    uint8_t       *signature = NULL;
    char          *publicKey = NULL;
    char          *path_list = NULL;

    if (strncmp("P_ECC", fapi_profile, 5) != 0)
        sigscheme = "RSA_PSS";

    r = Fapi_Provision(context, NULL, NULL, NULL);
    goto_if_error(r, "Error Fapi_Provision", error);

    r = Fapi_SetAuthCB(context, auth_callback, NULL);
    goto_if_error(r, "Error SetPolicyAuthCallback", error);

    r = Fapi_CreateKey(context, "HN/myNullPrimary", "noDa,0x81000004", "",
                       PASSWORD);

    if (r == TSS2_RC_SUCCESS) {
        goto_if_error(r, "Persistent handle not allowed.", error);
    }
    if (r != TSS2_FAPI_RC_BAD_VALUE) {
        goto_if_error(r, "Wrong check persistent.", error);
    }

    r = Fapi_CreateKey(context, "HN/myNullPrimary", "restricted,decrypt,noDa", "",
                       NULL);

    goto_if_error(r, "Error Fapi_CreateKey", error);

    r = Fapi_CreateKey(context, "HN/myNullPrimary/myNullSignKey", SIGN_TEMPLATE ",0x81000004", "",
                       PASSWORD);

    if (r == TSS2_RC_SUCCESS) {
        goto_if_error(r, "Wrong authentication.", error);
    }
    if (r != TSS2_FAPI_RC_BAD_VALUE) {
        goto_if_error(r, "Wrong check persistent.", error);
    }

    r = Fapi_CreateKey(context, "HN/myNullPrimary/myNullSignKey", SIGN_TEMPLATE, "",
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

    r = Fapi_Sign(context, "HN/myNullPrimary/myNullSignKey", sigscheme,
                  &digest.buffer[0], digest.size, &signature, &signatureSize,
                  &publicKey, NULL);
    goto_if_error(r, "Error Fapi_Sign", error);

    r = Fapi_VerifySignature(context, "HN/myNullPrimary/myNullSignKey",
                  &digest.buffer[0], digest.size, signature, signatureSize);
    goto_if_error(r, "Error Fapi_VerifySignature", error);

    Fapi_Finalize(&context);
    int rc = init_fapi(fapi_profile, &context);
    if (rc)
        goto error;

    /* Test the creation of a primary in the storage hierarchy. */
    r = Fapi_CreateKey(context, "HS/myPrimary", "noDa", "",
                        PASSWORD);
    goto_if_error(r, "Error Fapi_CreateKey", error);

    r = Fapi_Delete(context, "HS/myPrimary");
    goto_if_error(r, "Error Fapi_Delete", error);

    /* Test the creation of a primary in the storage hierarchy with a policy. */

    char *policy_name = "/policy/pol_pcr16_0";
    const char *json_policy =
        "{"                                         \
        "\"description\":\"Description pol_16_0\"," \
        "\"policy\":[" \
        "{" \
            "\"type\":\"POLICYPCR\"," \
            "\"pcrs\":[" \
                "{" \
                    "\"pcr\":16," \
                    "\"hashAlg\":\"TPM2_ALG_SHA256\"," \
                    "\"digest\":\"00000000000000000000000000000000000000000000000000000000000000000\"" \
                "}" \
               "]" \
             "}" \
           "]" \
        "}";

    r = Fapi_Import(context, policy_name, json_policy);
    goto_if_error(r, "Error Fapi_Import", error);

    r = Fapi_CreateKey(context, "HS/myPrimary", "noDa", policy_name,
                       NULL);
    goto_if_error(r, "Error Fapi_CreateKey", error);

    r = Fapi_Delete(context, "HS/myPrimary");
    goto_if_error(r, "Error Fapi_Delete", error);

    /* Test the creation of a primary in the endorsement hierarchy. */
    r = Fapi_CreateKey(context, "HE/myPrimary", "noDa", "",
                        PASSWORD);
    goto_if_error(r, "Error Fapi_CreateKey", error);

    r = Fapi_Delete(context, "HE/myPrimary");
    goto_if_error(r, "Error Fapi_Delete", error);


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
    return test_fapi_key_create_null_sign(fapi_context);
}
