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
#include <string.h>
#include <inttypes.h>

#include "tss2_fapi.h"

#include "test-fapi.h"
#include "ifapi_eventlog.h"
#define LOGMODULE test
#include "util/log.h"
#include "util/aux_util.h"

#define EVENT_SIZE 10

/* This is a list of expected value from the test. Possible returns (for different PCR bank
   configurations) are concatenated into a long string and the test uses strstr() to find a match.*/
const char *log_exp[] = {
"[\n\
  {\n\
    \"recnum\":0,\n\
    \"pcr\":16,\n\
    \"digests\":[\n\
      {\n\
        \"hashAlg\":\"sha1\",\n\
        \"digest\":\"494179714a6cd627239dfededf2de9ef994caf03\"\n\
      },\n\
      {\n\
        \"hashAlg\":\"sha256\",\n\
        \"digest\":\"1f825aa2f0020ef7cf91dfa30da4668d791c5d4824fc8e41354b89ec05795ab3\"\n\
      },\n\
      {\n\
        \"hashAlg\":\"sha384\",\n\
        \"digest\":\"182e95266adff49059e706c61483478fe0688150c8d08b95fab5cfde961f12d903aaf44104af4ce72ba6a4bf20302b2e\"\n\
      },\n\
      {\n\
        \"hashAlg\":\"sha512\",\n\
        \"digest\":\"0f89ee1fcb7b0a4f7809d1267a029719004c5a5e5ec323a7c3523a20974f9a3f202f56fadba4cd9e8d654ab9f2e96dc5c795ea176fa20ede8d854c342f903533\"\n\
      },\n\
      {\n\
        \"hashAlg\":\"SM3_256\",\n\
        \"digest\":\"24c898bdb4d258f9bebb2e820d4ed478a7c013b37bd9e5006515730c18a70416\"\n\
      }\n\
    ],\n\
    \"type\":\"tss2\",\n\
    \"sub_event\":{\n\
      \"data\":\"00010203040506070809\",\n\
      \"event\":{\n\
        \"test\":\"myfile\"\n\
      }\n\
    }\n\
  }\n\
]",
"[\n\
  {\n\
    \"recnum\":0,\n\
    \"pcr\":16,\n\
    \"digests\":[\n\
      {\n\
        \"hashAlg\":\"sha1\",\n\
        \"digest\":\"494179714a6cd627239dfededf2de9ef994caf03\"\n\
      },\n\
      {\n\
        \"hashAlg\":\"sha256\",\n\
        \"digest\":\"1f825aa2f0020ef7cf91dfa30da4668d791c5d4824fc8e41354b89ec05795ab3\"\n\
      },\n\
      {\n\
        \"hashAlg\":\"sha384\",\n\
        \"digest\":\"182e95266adff49059e706c61483478fe0688150c8d08b95fab5cfde961f12d903aaf44104af4ce72ba6a4bf20302b2e\"\n\
      },\n\
      {\n\
        \"hashAlg\":\"sha512\",\n\
        \"digest\":\"0f89ee1fcb7b0a4f7809d1267a029719004c5a5e5ec323a7c3523a20974f9a3f202f56fadba4cd9e8d654ab9f2e96dc5c795ea176fa20ede8d854c342f903533\"\n\
      }\n\
    ],\n\
    \"" CONTENT_TYPE "\":\"tss2\",\n\
    \"" CONTENT "\":{\n\
      \"data\":\"00010203040506070809\",\n\
      \"event\":{\n\
        \"test\":\"myfile\"\n\
      }\n\
    }\n\
  }\n\
]",
"[\n\
  {\n\
    \"recnum\":0,\n\
    \"pcr\":16,\n\
    \"digests\":[\n\
      {\n\
        \"hashAlg\":\"sha1\",\n\
        \"digest\":\"494179714a6cd627239dfededf2de9ef994caf03\"\n\
      },\n\
      {\n\
        \"hashAlg\":\"sha256\",\n\
        \"digest\":\"1f825aa2f0020ef7cf91dfa30da4668d791c5d4824fc8e41354b89ec05795ab3\"\n\
      },\n\
      {\n\
        \"hashAlg\":\"sha384\",\n\
        \"digest\":\"182e95266adff49059e706c61483478fe0688150c8d08b95fab5cfde961f12d903aaf44104af4ce72ba6a4bf20302b2e\"\n\
      }\n\
    ],\n\
    \"" CONTENT_TYPE "\":\"tss2\",\n\
    \"" CONTENT "\":{\n\
      \"data\":\"00010203040506070809\",\n\
      \"event\":{\n\
        \"test\":\"myfile\"\n\
      }\n\
    }\n\
  }\n\
]",
"[\n\
  {\n\
    \"recnum\":0,\n\
    \"pcr\":16,\n\
    \"digests\":[\n\
      {\n\
        \"hashAlg\":\"sha1\",\n\
        \"digest\":\"494179714a6cd627239dfededf2de9ef994caf03\"\n\
      },\n\
      {\n\
        \"hashAlg\":\"sha256\",\n\
        \"digest\":\"1f825aa2f0020ef7cf91dfa30da4668d791c5d4824fc8e41354b89ec05795ab3\"\n\
      }\n\
    ],\n\
    \"" CONTENT_TYPE "\":\"tss2\",\n\
    \"" CONTENT "\":{\n\
      \"data\":\"00010203040506070809\",\n\
      \"event\":{\n\
        \"test\":\"myfile\"\n\
      }\n\
    }\n\
  }\n\
]",
"[\n\
  {\n\
    \"recnum\":0,\n\
    \"pcr\":16,\n\
    \"digests\":[\n\
      {\n\
        \"hashAlg\":\"sha1\",\n\
        \"digest\":\"494179714a6cd627239dfededf2de9ef994caf03\"\n\
      }\n\
    ],\n\
    \"" CONTENT_TYPE "\":\"tss2\",\n\
    \"" CONTENT "\":{\n\
      \"data\":\"00010203040506070809\",\n\
      \"event\":{\n\
        \"test\":\"myfile\"\n\
      }\n\
    }\n\
  }\n\
]",
"[\n\
  {\n\
    \"recnum\":1,\n\
    \"pcr\":16,\n\
    \"digests\":[\n\
      {\n\
        \"hashAlg\":\"sha256\",\n\
        \"digest\":\"1f825aa2f0020ef7cf91dfa30da4668d791c5d4824fc8e41354b89ec05795ab3\"\n\
      }\n\
    ],\n\
    \"" CONTENT_TYPE "\":\"tss2\",\n\
    \"" CONTENT "\":{\n\
      \"data\":\"00010203040506070809\",\n\
      \"event\":{\n\
        \"test\":\"myfile\"\n\
      }\n\
    }\n\
  }\n\
]" };

/** Test the FAPI function FAPI_PcrExtend and Read.
 *
 * Tested FAPI commands:
 *  - Fapi_Provision()
 *  - Fapi_PcrExtend()
 *  - Fapi_PcrRead()
 *  - Fapi_Delete()
 *
 * @param[in,out] context The FAPI_CONTEXT.
 * @retval EXIT_FAILURE
 * @retval EXIT_SUCCESS
 */
int
test_fapi_pcr_test(FAPI_CONTEXT *context)
{
    TSS2_RC r;
    size_t i;
    uint8_t data[EVENT_SIZE] = { 0, 1, 2, 3, 4, 5, 6, 7, 8, 9};
    size_t pcr_digest_size;
    uint8_t *pcr_digest = NULL;
    char *log = NULL;

    r = Fapi_Provision(context, NULL, NULL, NULL);
    goto_if_error(r, "Error Fapi_Provision", error);

    r = pcr_reset(context, 16);
    goto_if_error(r, "Error pcr_reset", error);

    r = Fapi_PcrExtend(context, 16, data, EVENT_SIZE, "{ \"test\": \"myfile\" }");
    goto_if_error(r, "Error Fapi_PcrExtend", error);

    r = Fapi_PcrRead(context, 16, &pcr_digest,
                     &pcr_digest_size, &log);
    goto_if_error(r, "Error Fapi_PcrRead", error);
    ASSERT(pcr_digest != NULL);
    ASSERT(log != NULL);
    ASSERT(strlen(log) > ASSERT_SIZE);

    size_t number_of_test_values = sizeof(log_exp) / sizeof(log_exp[0]);

    for (i = 0; i < number_of_test_values; i++)
        if (strcmp(log_exp[i], log) == 0)
            break;
    if (i >= number_of_test_values) {
        LOG_ERROR("Log mismatch. Received: %s", log);
        goto error;
    }
    CHECK_JSON_LIST(log_exp, log, error);
    fprintf(stderr, "\nEvent Log:\n%s\n", log);

    SAFE_FREE(pcr_digest);
    SAFE_FREE(log);
    r = pcr_reset(context, 16);
    goto_if_error(r, "Error pcr_reset", error);

    pcr_digest = NULL;
    log = NULL;
    r = Fapi_PcrRead(context, 16, &pcr_digest,
                     &pcr_digest_size, &log);
    goto_if_error(r, "Error Fapi_PcrRead", error);
    ASSERT(pcr_digest != NULL);
    ASSERT(log != NULL);
    ASSERT(strlen(log) > ASSERT_SIZE);
    LOG_INFO("\nTEST_JSON\nLog:\n%s\nEND_JSON", log);


    r = Fapi_Delete(context, "/");
    goto_if_error(r, "Error Fapi_Delete", error);

    SAFE_FREE(pcr_digest);
    SAFE_FREE(log);
    return EXIT_SUCCESS;

error:
    Fapi_Delete(context, "/");
    SAFE_FREE(pcr_digest);
    SAFE_FREE(log);
    return EXIT_FAILURE;
}

int
test_invoke_fapi(FAPI_CONTEXT *context)
{
    return test_fapi_pcr_test(context);
}
