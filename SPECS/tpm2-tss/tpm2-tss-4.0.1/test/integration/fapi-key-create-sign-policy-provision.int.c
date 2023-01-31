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
#define LOGMODULE test
#include "util/log.h"
#include "util/aux_util.h"

#define PASSWORD NULL
#define SIGN_TEMPLATE  "sign,noDa"

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

    char *pw = PASSWORD;
    if (!pw)
        return TSS2_FAPI_RC_GENERAL_FAILURE;

    *auth = pw;
    return TSS2_RC_SUCCESS;
}

/** Test the FAPI functions for key creation and usage.
 *
 * Tested FAPI commands:
 *  - Fapi_Provision()
 *  - Fapi_SetAuthCB()
 *  - Fapi_CreateKey()
 *  - Fapi_GetTpmBlobs()
 *  - Fapi_Sign()
 *  - Fapi_SetCertificate()
 *  - Fapi_List()
 *  - Fapi_Delete()
 *
 * @param[in,out] context The FAPI_CONTEXT.
 * @retval EXIT_FAILURE
 * @retval EXIT_SUCCESS
 */
int
test_fapi_key_create_sign_policy_provision(FAPI_CONTEXT *context)
{
    TSS2_RC r;
    char *sigscheme = NULL;
    uint8_t *publicblob = NULL;
    uint8_t *privateblob = NULL;
    char *policy = NULL;
    uint8_t *signature = NULL;
    char *publicKey = NULL;
    char *certificate = NULL;
    char *path_list = NULL;

    const char *cert =
        "-----BEGIN CERTIFICATE-----\n"
        "MIIDBjCCAe4CCQDcvXBOEVM0UTANBgkqhkiG9w0BAQsFADBFMQswCQYDVQQGEwJE\n"
        "RTETMBEGA1UECAwKU29tZS1TdGF0ZTEhMB8GA1UECgwYSW50ZXJuZXQgV2lkZ2l0\n"
        "cyBQdHkgTHRkMB4XDTE5MDIyODEwNDkyM1oXDTM1MDgyNzEwNDkyM1owRTELMAkG\n"
        "A1UEBhMCREUxEzARBgNVBAgMClNvbWUtU3RhdGUxITAfBgNVBAoMGEludGVybmV0\n"
        "IFdpZGdpdHMgUHR5IEx0ZDCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEB\n"
        "AKBi+iKwkgM55iCMwXrLCJlu7TzlMu/LlkyGrm99ip2B5+/Cl6a62d8pKelg6zkH\n"
        "jI7+AAPteJiW4O+2qVWF8hJ5BXTjGtYbM0iZ6enCb8eyC54C7xVMc21ZIv3ob4Et\n"
        "50ZOuzY2pfpzE3vIaXt1CkHlfyI/hdK+mM/dVvuCz5p3AIlHrEWS3rSNgWbCsB2E\n"
        "TM55qSGKaLmtTbUvEKRF0TJrFLntfXkv10QD5pgn52+QV9k59OogqZOsDvkXzKPX\n"
        "rXF+XC0gLiGBEGAr1dv9F03xMOtO77bQTdGOeC61Tip6Nb0V3ebMckZXwdFi+Nhe\n"
        "FRuU33CaObtV6u5PZvSue/MCAwEAATANBgkqhkiG9w0BAQsFAAOCAQEAcamUPe8I\n"
        "nMOHcv9x5lVN1joihVRmKc0QqNLFc6XpJY8+U5rGkZvOcDe9Da8L97wDNXpKmU/q\n"
        "pprj3rT8l3v0Z5xs8Vdr8lxS6T5NhqQV0UCsn1x14gZJcE48y9/LazYi6Zcar+BX\n"
        "Am4vewAV3HmQ8X2EctsRhXe4wlAq4slIfEWaaofa8ai7BzO9KwpMLsGPWoNetkB9\n"
        "19+SFt0lFFOj/6vDw5pCpSd1nQlo1ug69mJYSX/wcGkV4t4LfGhV8jRPDsGs6I5n\n"
        "ETHSN5KV1XCPYJmRCjFY7sIt1x4zN7JJRO9DVw+YheIlduVfkBiF+GlQgLlFTjrJ\n"
        "VrpSGMIFSu301A==\n"
        "-----END CERTIFICATE-----\n";

    if (strncmp("P_ECC", fapi_profile, 5) != 0)
        sigscheme = "RSA_PSS";

    /* We need to reset the passwords again, in order to not brick physical TPMs */
    r = Fapi_Provision(context, NULL, PASSWORD, NULL);
    goto_if_error(r, "Error Fapi_Provision", error);

    r = Fapi_SetAuthCB(context, auth_callback, NULL);
    goto_if_error(r, "Error SetPolicyAuthCallback", error);

    r = Fapi_CreateKey(context, "HS/SRK/mySignKey", SIGN_TEMPLATE, "",
                       PASSWORD);

    goto_if_error(r, "Error Fapi_CreateKey", error);
    size_t signatureSize = 0;

    TPM2B_DIGEST digest = {
        .size = 20,
        .buffer = {
            0x67, 0x68, 0x03, 0x3e, 0x21, 0x64, 0x68, 0x24, 0x7b, 0xd0,
            0x31, 0xa0, 0xa2, 0xd9, 0x87, 0x6d, 0x79, 0x81, 0x8f, 0x8f
        }
    };

    size_t         publicsize;
    size_t         privatesize;

    r = Fapi_GetTpmBlobs(context,  "HS/SRK/mySignKey", &publicblob,
                         &publicsize,
                         &privateblob, &privatesize, &policy);
    goto_if_error(r, "Error Fapi_GetTpmBlobs", error);
    ASSERT(publicblob != NULL);
    ASSERT(privateblob != NULL);
    ASSERT(policy != NULL);
    ASSERT(strlen(policy) == 0);

    r = Fapi_SetCertificate(context, "HS/SRK/mySignKey", cert);
    goto_if_error(r, "Error Fapi_SetCertificate", error);


    r = Fapi_Sign(context, "HS/SRK/mySignKey", sigscheme,
                  &digest.buffer[0], digest.size, &signature, &signatureSize,
                  &publicKey, &certificate);
    goto_if_error(r, "Error Fapi_Sign", error);
    ASSERT(signature != NULL);
    ASSERT(publicKey != NULL);
    ASSERT(certificate != NULL);
    ASSERT(strlen(publicKey) > ASSERT_SIZE);
    ASSERT(strlen(certificate) > ASSERT_SIZE);

    r = Fapi_List(context, "/", &path_list);
    goto_if_error(r, "Error Fapi_Delete", error);
    ASSERT(path_list != NULL);
    ASSERT(strlen(path_list) > ASSERT_SIZE);

    LOG_INFO("\nPathList:\n%s\n", path_list);

    r = Fapi_Delete(context, "/");
    goto_if_error(r, "Error Fapi_Delete", error);

    SAFE_FREE(publicblob);
    SAFE_FREE(privateblob);
    SAFE_FREE(policy);
    SAFE_FREE(signature);
    SAFE_FREE(publicKey);
    SAFE_FREE(certificate);
    SAFE_FREE(path_list);
    return EXIT_SUCCESS;

error:
    Fapi_Delete(context, "/");
    SAFE_FREE(publicblob);
    SAFE_FREE(privateblob);
    SAFE_FREE(policy);
    SAFE_FREE(signature);
    SAFE_FREE(publicKey);
    SAFE_FREE(certificate);
    SAFE_FREE(path_list);
    return EXIT_FAILURE;
}

int
test_invoke_fapi(FAPI_CONTEXT *fapi_context)
{
    return test_fapi_key_create_sign_policy_provision(fapi_context);
}
