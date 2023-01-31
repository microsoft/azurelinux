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
#include <stdio.h>

#include "tss2_fapi.h"

#define LOGMODULE test
#include "util/log.h"
#include "util/aux_util.h"
#include "test-fapi.h"

#define PASSWORD "abc"
#define USER_DATA "my user data"
#define DESCRIPTION "my description"
#define OBJECT_PATH "HS/SRK/mySignKey"

static TSS2_RC
auth_callback(
    char const *objectPath,
    char const *description,
    const char **auth,
    void *userData)
{
    UNUSED(description);
    UNUSED(userData);

    char *profile_path;

    ASSERT(description != NULL);
    ASSERT(userData != NULL);

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

    *auth = PASSWORD;
    return TSS2_RC_SUCCESS;

 error:
    exit(EXIT_FAILURE);
}


/** Test the FAPI function for changing key authorizations.
 *
 * The setting of the authorization callback and usage of the
 * key with Fapi_Sign afterwards is also tested.
 *
 * Tested FAPI commands:
 *  - Fapi_Provision()
 *  - Fapi_CreateKey()
 *  - Fapi_ChangeAuth()
 *  - Fapi_SetAuthCB()
 *  - Fapi_Sign()
 *  - Fapi_Delete()
 *
 * @param[in,out] context The FAPI_CONTEXT.
 * @retval EXIT_FAILURE
 * @retval EXIT_SUCCESS
 */
int
test_fapi_key_change_auth(FAPI_CONTEXT *context)
{

    TSS2_RC r;
    uint8_t *signature = NULL;
    char    *publicKey = NULL;
    char    *certificate = NULL;

    r = Fapi_Provision(context, NULL, NULL, NULL);

    goto_if_error(r, "Error Fapi_Provision", error);

    r = Fapi_CreateKey(context, OBJECT_PATH, "sign,noDa", "", NULL);
    goto_if_error(r, "Error Fapi_CreateKey", error);

    r = Fapi_SetDescription(context, OBJECT_PATH, DESCRIPTION);
    goto_if_error(r, "Error Fapi_SetDescription", error);

    r = Fapi_SetCertificate(context, OBJECT_PATH, "-----BEGIN "\
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

    r = Fapi_ChangeAuth(context, OBJECT_PATH, PASSWORD);
    goto_if_error(r, "Error Fapi_Provision", error);

    r = Fapi_SetAuthCB(context, auth_callback, USER_DATA);
    goto_if_error(r, "Error SetPolicyAuthCallback", error);

    r = Fapi_Sign(context, OBJECT_PATH, NULL,
                  &digest.buffer[0], digest.size, &signature, &signatureSize,
                  &publicKey, &certificate);
    goto_if_error(r, "Error Fapi_Provision", error);
    ASSERT(signature != NULL);
    ASSERT(publicKey != NULL);
    ASSERT(certificate != NULL);
    ASSERT(strstr(publicKey, "BEGIN PUBLIC KEY"));
    ASSERT(strstr(certificate, "BEGIN CERTIFICATE"));

    Fapi_Free(publicKey);

    r = Fapi_Delete(context, "/");
    goto_if_error(r, "Error Fapi_Delete", error);

    SAFE_FREE(signature);
    SAFE_FREE(certificate);
    return EXIT_SUCCESS;

error:
    Fapi_Delete(context, "/");
    SAFE_FREE(signature);
    SAFE_FREE(certificate);
    return EXIT_FAILURE;
}

int
test_invoke_fapi(FAPI_CONTEXT *fapi_context)
{
    return test_fapi_key_change_auth(fapi_context);
}
