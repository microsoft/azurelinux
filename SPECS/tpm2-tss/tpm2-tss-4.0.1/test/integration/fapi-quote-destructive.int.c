/* SPDX-License-Identifier: BSD-2-Clause */
/*******************************************************************************
 * Copyright 2017-2018, Fraunhofer SIT sponsored by Infineon Technologies AG
 * All rights reserved.
 *******************************************************************************/

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif
#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>

#include "tss2_fapi.h"

#include "test-fapi.h"
#define LOGMODULE test
#include "util/log.h"
#include "util/aux_util.h"

#define EVENT_SIZE 10

/** Test the FAPI functions for quote commands.
 *
 * Tested FAPI commands:
 *  - Fapi_Provision()
 *  - Fapi_CreateKey()
 *  - Fapi_PcrExtend()
 *  - Fapi_Quote()
 *  - Fapi_VerifyQuote()
 *  - Fapi_List()
 *  - Fapi_Delete()
 *
 * @param[in,out] context The FAPI_CONTEXT.
 * @retval EXIT_FAILURE
 * @retval EXIT_SUCCESS
 */
int
test_fapi_quote_destructive(FAPI_CONTEXT *context)
{
    TSS2_RC r;
    char *pubkey_pem = NULL;
    uint8_t *signature = NULL;
    char *quoteInfo = NULL;
    char *pcrEventLog = NULL;
    char *certificate = NULL;
    char *export_data = NULL;
    uint8_t *pcr_digest = NULL;
    char *log = NULL;
    char *pathlist = NULL;

    uint8_t data[EVENT_SIZE] = { 0, 1, 2, 3, 4, 5, 6, 7, 8, 9};
    size_t signatureSize = 0;
    uint32_t pcrList[2] = { 11, 16 };

    r = Fapi_Provision(context, NULL, NULL, NULL);

    goto_if_error(r, "Error Fapi_Provision", error);

    r = Fapi_CreateKey(context, "HS/SRK/mySignKey", "sign,noDa", "", NULL);
    goto_if_error(r, "Error Fapi_CreateKey", error);

   r = Fapi_SetCertificate(context, "HS/SRK/mySignKey", "-----BEGIN "  \
        "CERTIFICATE-----[...]-----END CERTIFICATE-----");
    goto_if_error(r, "Error Fapi_SetCertificate", error);

    uint8_t qualifyingData[20] = {
        0x67, 0x68, 0x03, 0x3e, 0x21, 0x64, 0x68, 0x24, 0x7b, 0xd0,
        0x31, 0xa0, 0xa2, 0xd9, 0x87, 0x6d, 0x79, 0x81, 0x8f, 0x8f
    };

    r = pcr_reset(context, 16);
    goto_if_error(r, "Error pcr_reset", error);

    r = Fapi_PcrExtend(context, 16, data, EVENT_SIZE, "{ \"test\": \"myfile\" }");
    goto_if_error(r, "Error Fapi_PcrExtend", error);

    r = Fapi_PcrExtend(context, 16, data, EVENT_SIZE, "{ \"test\": \"myfile\" }");
    goto_if_error(r, "Error Fapi_PcrExtend", error);

    r = Fapi_PcrExtend(context, 16, data, EVENT_SIZE, "{ \"test\": \"myfile\" }");
    goto_if_error(r, "Error Fapi_PcrExtend", error);

    r = Fapi_Quote(context, pcrList, 2, "HS/SRK/mySignKey",
                   "TPM-Quote",
                   qualifyingData, 20,
                   &quoteInfo,
                   &signature, &signatureSize,
                   &pcrEventLog, &certificate);
    goto_if_error(r, "Error Fapi_Quote", error);
    ASSERT(quoteInfo != NULL);
    ASSERT(signature != NULL);
    ASSERT(pcrEventLog != NULL);
    ASSERT(certificate != NULL);
    ASSERT(strlen(quoteInfo) > ASSERT_SIZE);
    ASSERT(strlen(pcrEventLog) > ASSERT_SIZE);
    ASSERT(strlen(certificate) > ASSERT_SIZE);

    LOG_INFO("\npcrEventLog: %s\n", pcrEventLog);

    r = Fapi_VerifyQuote(context, "HS/SRK/mySignKey",
                         qualifyingData, 20,  quoteInfo,
                         signature, signatureSize, pcrEventLog);
    goto_if_error(r, "Error Fapi_Verfiy_Quote", error);

    r = Fapi_List(context, "/", &pathlist);
    goto_if_error(r, "Pathlist", error);
    ASSERT(pathlist != NULL);
    ASSERT(strlen(pathlist) > ASSERT_SIZE);

    r = pcr_reset(context, 16);
    goto_if_error(r, "Error pcr_reset", error);

    r = Fapi_Delete(context, "/");
    goto_if_error(r, "Error Fapi_Delete", error);

    SAFE_FREE(pubkey_pem);
    SAFE_FREE(signature);
    SAFE_FREE(quoteInfo);
    SAFE_FREE(pcrEventLog);
    SAFE_FREE(certificate);
    SAFE_FREE(export_data);
    SAFE_FREE(pcr_digest);
    SAFE_FREE(log);
    SAFE_FREE(pathlist);
    return EXIT_SUCCESS;

error:
    Fapi_Delete(context, "/");
    SAFE_FREE(pubkey_pem);
    SAFE_FREE(signature);
    SAFE_FREE(quoteInfo);
    SAFE_FREE(pcrEventLog);
    SAFE_FREE(certificate);
    SAFE_FREE(export_data);
    SAFE_FREE(pcr_digest);
    SAFE_FREE(log);
    SAFE_FREE(pathlist);
    return EXIT_FAILURE;
}

int
test_invoke_fapi(FAPI_CONTEXT *fapi_context)
{
    return test_fapi_quote_destructive(fapi_context);
}
