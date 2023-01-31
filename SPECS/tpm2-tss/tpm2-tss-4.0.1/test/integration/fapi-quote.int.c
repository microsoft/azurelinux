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
#include <json-c/json.h>
#include <json-c/json_util.h>
#include <json-c/json_tokener.h>

#include "tss2_fapi.h"

#include "test-fapi.h"
#include "ifapi_eventlog.h"
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
 *  - Fapi_ExportKey()
 *  - Fapi_Import()
 *  - Fapi_PcrRead()
 *  - Fapi_VerifyQuote()
 *  - Fapi_List()
 *  - Fapi_Delete()
 *
 * @param[in,out] context The FAPI_CONTEXT.
 * @retval EXIT_FAILURE
 * @retval EXIT_SUCCESS
 */
int
test_fapi_quote(FAPI_CONTEXT *context)
{
    TSS2_RC r;
    json_object *jso = NULL;
    char *pubkey_pem = NULL;
    uint8_t *signature = NULL;
    char *quoteInfo = NULL;
    char *pcrEventLog = NULL;
    char *certificate = NULL;
    char *export_data = NULL;
    json_object *jso_public = NULL;
    uint8_t *pcr_digest = NULL;
    char *log = NULL;
    char *pathlist = NULL;

    uint8_t data[EVENT_SIZE] = { 0, 1, 2, 3, 4, 5, 6, 7, 8, 9};
    size_t signatureSize = 0;
    uint32_t pcrList[1] = { 16 };
    size_t pcr_digest_size = 0;

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

    r = Fapi_Quote(context, pcrList, 1, "HS/SRK/mySignKey",
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

    LOG_INFO("Quote Info:\n%s\n", quoteInfo);
    char *field_list_quote_info[] = { "attest", "attested", "pcrDigest" };
    CHECK_JSON_FIELDS(quoteInfo, field_list_quote_info, "", error);

    r = Fapi_ExportKey(context, "HS/SRK/mySignKey", NULL, &export_data);
    goto_if_error(r, "Export.", error);
    ASSERT(export_data != NULL);
    ASSERT(strlen(export_data) > ASSERT_SIZE);

    jso = json_tokener_parse(export_data);
    LOG_INFO("\nExported: %s\n", export_data);

    char *fields_export[] = { "pem_ext_public" };
    CHECK_JSON_FIELDS(export_data, fields_export, "BEGIN PUBLIC KEY", error);

    if (!jso || !json_object_object_get_ex(jso, "pem_ext_public",  &jso_public)) {
        LOG_ERROR("No public key eyported.");
        goto error;
    }
    pubkey_pem = strdup(json_object_get_string(jso_public));
    if (!pubkey_pem) {
        LOG_ERROR("Out of memory.");
        goto error;
    }

    r = Fapi_Import(context, "/ext/myExtPubKey", pubkey_pem);
    goto_if_error(r, "Error Fapi_Import", error);

    r = Fapi_PcrRead(context, 16, &pcr_digest,
                     &pcr_digest_size, &log);
    goto_if_error(r, "Error Fapi_PcrRead", error);
    ASSERT(pcr_digest != NULL);
    ASSERT(log != NULL);
    ASSERT(strlen(log) > ASSERT_SIZE);

    LOG_INFO("\nTEST_JSON\nLog:\n%s\nEND_JSON", log);
    LOG_INFO("Quote Info:\n%s\n", quoteInfo);

    const char *log_check_list[] =
        {
         "["
         "  {"
         "    \"recnum\":0,"
         "    \"pcr\":16,"
         "    \"digests\":["
         "      {"
         "        \"hashAlg\":\"sha1\","
         "        \"digest\":\"494179714a6cd627239dfededf2de9ef994caf03\""
         "      },"
         "      {"
         "        \"hashAlg\":\"sha256\","
         "        \"digest\":\"1f825aa2f0020ef7cf91dfa30da4668d791c5d4824fc8e41354b89ec05795ab3\""
         "      },"
         "      {"
         "        \"hashAlg\":\"sha384\","
         "        \"digest\":\"182e95266adff49059e706c61483478fe0688150c8d08b95fab5cfde961f12d903aaf44104af4ce72ba6a4bf20302b2e\""
         "      },"
         "      {"
         "        \"hashAlg\":\"sha512\","
         "        \"digest\":\"0f89ee1fcb7b0a4f7809d1267a029719004c5a5e5ec323a7c3523a20974f9a3f202f56fadba4cd9e8d654ab9f2e96dc5c795ea176fa20ede8d854c342f903533\""
         "      },"
         "      {"
         "        \"hashAlg\":\"SM3_256\","
         "        \"digest\":\"24c898bdb4d258f9bebb2e820d4ed478a7c013b37bd9e5006515730c18a70416\""
         "      }"
         "    ],"
         "    \"type\":\"tss2\","
         "    \"sub_event\":{"
         "      \"data\":\"00010203040506070809\","
         "      \"event\":{"
         "        \"test\":\"myfile\""
         "      }"
         "    }"
         "  }"
         "]",
         "["
         "  {"
         "    \"recnum\":0,"
         "    \"pcr\":16,"
         "    \"digests\":["
         "      {"
         "        \"hashAlg\":\"sha1\","
         "        \"digest\":\"494179714a6cd627239dfededf2de9ef994caf03\""
         "      },"
         "      {"
         "        \"hashAlg\":\"sha256\","
         "        \"digest\":\"1f825aa2f0020ef7cf91dfa30da4668d791c5d4824fc8e41354b89ec05795ab3\""
         "      },"
         "      {"
         "        \"hashAlg\":\"sha384\","
         "        \"digest\":\"182e95266adff49059e706c61483478fe0688150c8d08b95fab5cfde961f12d903aaf44104af4ce72ba6a4bf20302b2e\""
         "      },"
         "      {"
         "        \"hashAlg\":\"sha512\","
         "        \"digest\":\"0f89ee1fcb7b0a4f7809d1267a029719004c5a5e5ec323a7c3523a20974f9a3f202f56fadba4cd9e8d654ab9f2e96dc5c795ea176fa20ede8d854c342f903533\""
         "      }"
         "    ],"
         "    \"" CONTENT_TYPE "\":\"tss2\","
         "    \"" CONTENT "\":{"
         "      \"data\":\"00010203040506070809\","
         "      \"event\":{"
         "        \"test\":\"myfile\""
         "      }"
         "    }"
         "  }"
         "]",
         "["
         "  {"
         "    \"recnum\":0,"
         "    \"pcr\":16,"
         "    \"digests\":["
         "      {"
         "        \"hashAlg\":\"sha1\","
         "        \"digest\":\"494179714a6cd627239dfededf2de9ef994caf03\""
         "      },"
         "      {"
         "        \"hashAlg\":\"sha256\","
         "        \"digest\":\"1f825aa2f0020ef7cf91dfa30da4668d791c5d4824fc8e41354b89ec05795ab3\""
         "      },"
         "      {"
         "        \"hashAlg\":\"sha384\","
         "        \"digest\":\"182e95266adff49059e706c61483478fe0688150c8d08b95fab5cfde961f12d903aaf44104af4ce72ba6a4bf20302b2e\""
         "      }"
         "    ],"
         "    \"" CONTENT_TYPE "\":\"tss2\","
         "    \"" CONTENT "\":{"
         "      \"data\":\"00010203040506070809\","
         "      \"event\":{"
         "        \"test\":\"myfile\""
         "      }"
         "    }"
         "  }"
         "]",
         "["
         "  {"
         "    \"recnum\":0,"
         "    \"pcr\":16,"
         "    \"digests\":["
         "      {"
         "        \"hashAlg\":\"sha1\","
         "        \"digest\":\"494179714a6cd627239dfededf2de9ef994caf03\""
         "      },"
         "      {"
         "        \"hashAlg\":\"sha256\","
         "        \"digest\":\"1f825aa2f0020ef7cf91dfa30da4668d791c5d4824fc8e41354b89ec05795ab3\""
         "      }"
         "    ],"
         "    \"" CONTENT_TYPE "\":\"tss2\","
         "    \"" CONTENT "\":{"
         "      \"data\":\"00010203040506070809\","
         "      \"event\":{"
         "        \"test\":\"myfile\""
         "      }"
         "    }"
         "  }"
         "]",
         "["
         "  {"
         "    \"recnum\":0,"
         "    \"pcr\":16,"
         "    \"digests\":["
         "      {"
         "        \"hashAlg\":\"sha1\","
         "        \"digest\":\"494179714a6cd627239dfededf2de9ef994caf03\""
         "      }"
         "    ],"
         "    \"" CONTENT_TYPE "\":\"tss2\","
         "    \"" CONTENT "\":{"
         "      \"data\":\"00010203040506070809\","
         "      \"event\":{"
         "        \"test\":\"myfile\""
         "      }"
         "    }"
         "  }"
         "]"
        };
    CHECK_JSON_LIST(log_check_list, log, error);

    r = Fapi_VerifyQuote(context, "HS/SRK/mySignKey",
                         qualifyingData, 20,  quoteInfo,
                         signature, signatureSize, log);
    goto_if_error(r, "Error Fapi_Verfiy_Quote", error);

    LOG_INFO("\nVerifyQuote log: %s\n", log);
    CHECK_JSON_LIST(log_check_list, log, error);

    r = Fapi_List(context, "/", &pathlist);
    goto_if_error(r, "Pathlist", error);
    ASSERT(pathlist != NULL);
    ASSERT(strlen(pathlist) > ASSERT_SIZE);
    LOG_INFO("\nPathlist: %s\n", pathlist);
    char *check_pathlist =
        "/" FAPI_PROFILE "/HS/SRK:/" FAPI_PROFILE "/HS:/" FAPI_PROFILE "/LOCKOUT:/"
        FAPI_PROFILE "/HE/EK:/" FAPI_PROFILE "/HE:/" FAPI_PROFILE "/HN:/" FAPI_PROFILE
        "/HS/SRK/mySignKey:/ext/myExtPubKey";
    ASSERT(cmp_strtokens(pathlist, check_pathlist, ":"));
    LOG_INFO("\nPathlist: %s\n", check_pathlist);

    /* Invalidate qualifying data */
    qualifyingData[0] = 0;

    r = Fapi_VerifyQuote(context, "HS/SRK/mySignKey",
                         qualifyingData, 20,  quoteInfo,
                         signature, signatureSize, log);
    if (r == TPM2_RC_SUCCESS) {
        LOG_ERROR("Invalid qualifying data was not detected.");
        goto error;
    }

    r = Fapi_Delete(context, "/");
    goto_if_error(r, "Error Fapi_Delete", error);

    json_object_put(jso);
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
    if (jso)
        json_object_put(jso);
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
    return test_fapi_quote(fapi_context);
}
