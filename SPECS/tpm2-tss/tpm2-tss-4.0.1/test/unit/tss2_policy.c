/* SPDX-License-Identifier: BSD-2-Clause */
/*******************************************************************************
 * Copyright 2017-2018, Fraunhofer SIT sponsored by Infineon Technologies AG
 * All rights reserved.
 *******************************************************************************/

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <limits.h>
#include <stdarg.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <setjmp.h>
#include <cmocka.h>

#if defined(__linux__)
#include <linux/limits.h>
#endif

#include "tss2_policy.h"

#define LOGMODULE test
#include "util/log.h"

#include "test/data/test-fapi-policies.h"
#include "util/aux_util.h"

#define TEST_LAYER        TSS2_RC_LAYER(19)
#define TSS2_RC_TEST_NOT_SUPPORTED ((TSS2_RC)(TEST_LAYER | \
                            TSS2_BASE_RC_NOT_SUPPORTED))

static char *read_all(const char *path) {
    FILE *f = fopen(path, "rb");
    if (!f) {
        return NULL;
    }

    fseek(f, 0, SEEK_END);
    long fsize = ftell(f);
    rewind(f);

    char *buffer = calloc(1, fsize + 1);
    if (!buffer) {
        fclose(f);
        return NULL;
    }

    size_t count_read = fread(buffer, fsize, 1, f);
    fclose(f);
    if (count_read != 1) {
        return NULL;
    }

    return buffer;
}

TSS2_RC policy_cb_pcr (
    TSS2_POLICY_PCR_SELECTION *pcr_selection,
    TPML_PCR_SELECTION *out_pcr_selection,
    TPML_DIGEST *out_pcr_digests,
    void *ctx)
{
    TPML_PCR_SELECTION in_pcr_selection = { 0 };
    TPML_DIGEST pcr_digests = { 0 };

    /* Raw selector without bank specifier, figure out bank and copy
     * the raw selector over to the input selector */
    if (pcr_selection->type == TSS2_POLICY_PCR_SELECTOR_PCR_SELECT) {
        /* Only one bank will be used. A default algorithm of TPM2_ALG_SHA256 */
        in_pcr_selection.pcrSelections[0].hash = TPM2_ALG_SHA256;
        in_pcr_selection.count = 1;
        memcpy(in_pcr_selection.pcrSelections[0].pcrSelect,
                pcr_selection->selections.pcr_select.pcrSelect,
                sizeof(pcr_selection->selections.pcr_select.pcrSelect));
        in_pcr_selection.pcrSelections[0].sizeofSelect =
                pcr_selection->selections.pcr_select.sizeofSelect;
    } else {
        /* we have specified selection with bank, so just copy it. */
        in_pcr_selection = pcr_selection->selections.pcr_selection;
    }

    /* This is in place of something like an ESYS_PCR_Read() */
    /* For each bank */
    UINT32 count;
    for (count = 0; count < in_pcr_selection.count; count++) {

        /* Get the selection */
        TPMS_PCR_SELECTION pcr_select = in_pcr_selection.pcrSelections[count];

        /* for each selection byte */
        UINT32 i;
        for (i = 0; i < pcr_select.sizeofSelect; i++) {

            UINT8 j;
            /* for each selection bit in the byte */
            for (j = 0; j < sizeof(pcr_select.pcrSelect[i]) * 8; j++) {
                if (pcr_select.pcrSelect[i] & 1 << j) {

                    /* fake a read */
                    if (pcr_select.hash == TPM2_ALG_SHA256) {
                        pcr_digests.digests[pcr_digests.count].size = 32;
                    } else {
                        LOG_ERROR("Only SHA256 is supported, got: 0x%x", pcr_select.hash);
                        return TSS2_RC_TEST_NOT_SUPPORTED;
                    }

                    memset(pcr_digests.digests[pcr_digests.count].buffer, 0,
                            pcr_digests.digests[pcr_digests.count].size);
                    pcr_digests.count++;
                }
            }
        }
    }

    /* copy to caller */
    *out_pcr_selection = in_pcr_selection;
    *out_pcr_digests = pcr_digests;

    return TSS2_RC_SUCCESS;
}

TSS2_RC policy_cb_nvpublic (
    const char *path,
    TPMI_RH_NV_INDEX nv_index,
    TPMS_NV_PUBLIC *nv_public,
    void *userdata)
{
    UNUSED(path);
    UNUSED(nv_index);
    UNUSED(nv_public);
    UNUSED(userdata);

    LOG_ERROR("Policy NV Public Callback Not Supported");

    return TSS2_RC_TEST_NOT_SUPPORTED;
}

static void bin2hex (
    const unsigned char *bin,
    size_t len,
    char *out)
{
    size_t i;

    if (bin == NULL || len == 0) {
        return;
    }

    for (i = 0; i < len; i++) {
        out[i * 2] = "0123456789abcdef"[bin[i] >> 4];
        out[i * 2 + 1] = "0123456789abcdef"[bin[i] & 0x0F];
    }
    out[len * 2] = '\0';
}

static void test_policy_instantiate (
    void **state)
{
    TSS2_POLICY_CALC_CALLBACKS callbacks = {
        .cbpcr      = policy_cb_pcr,
        .cbnvpublic = policy_cb_nvpublic
    };

    unsigned i;
    for (i = 0; i < ARRAY_LEN(_test_fapi_policy_policies); i++) {
        policy_digests *p = &_test_fapi_policy_policies[i];

        char abs_path[PATH_MAX];
        snprintf(abs_path, sizeof(abs_path),
                TOP_SOURCEDIR"/test/data/fapi%s.json", p->path);

        fprintf(stderr, "Calculating policy (%u): %s\n", i, p->path);

        unsigned expected_hash_size = 0;
        char hexdigest[32 + 32 + 1] = { 0 };
        TPM2B_DIGEST digest = { 0 };
        TSS2_POLICY_CTX *ctx = NULL;

        /* for each hash alg set... */
        TPM2_ALG_ID halgs[] = {
            TPM2_ALG_SHA1,
            TPM2_ALG_SHA256
        };

        unsigned j;
        for (j = 0; j < ARRAY_LEN(halgs); j++) {
            TPM2_ALG_ID halg = halgs[j];

            if (halg == TPM2_ALG_SHA1) {
                if (!p->sha1) {
                    continue;
                }
                expected_hash_size = 20;
            } else if (halg == TPM2_ALG_SHA256) {
                if (!p->sha256) {
                    continue;
                }
                expected_hash_size = 32;
            }

            char *json = read_all(abs_path);
            assert_non_null(json);

            TSS2_RC rc = Tss2_PolicyInit(json, halg, &ctx);
            SAFE_FREE(json);
            assert_int_equal(rc, TSS2_RC_SUCCESS);

            rc = Tss2_PolicySetCalcCallbacks(ctx, &callbacks);
            assert_int_equal(rc, TSS2_RC_SUCCESS);

            rc = Tss2_PolicyCalculate(ctx);
            assert_int_equal(rc, TSS2_RC_SUCCESS);

            rc = Tss2_PolicyGetCalculatedDigest(ctx, &digest);
            assert_int_equal(rc, TSS2_RC_SUCCESS);
            assert_int_equal(digest.size, expected_hash_size);

            if (halg == TPM2_ALG_SHA1) {
                bin2hex(digest.buffer, digest.size, hexdigest);
                assert_string_equal(p->sha1, hexdigest);
            } else if (halg == TPM2_ALG_SHA256) {
                bin2hex(digest.buffer, digest.size, hexdigest);
                assert_string_equal(p->sha256, hexdigest);
            }

            /* Get the calculated policy digest */
            char *buffer = NULL;
            size_t size = 0;
            rc = Tss2_PolicyGetCalculatedJSON(
                    ctx,
                    NULL,
                    &size);
            assert_int_equal(rc, TSS2_RC_SUCCESS);

            buffer = calloc(1, size);
            assert_non_null(buffer);

            rc = Tss2_PolicyGetCalculatedJSON(
                    ctx,
                    buffer,
                    &size);
            assert_int_equal(rc, TSS2_RC_SUCCESS);

            /* done with that policy */
            Tss2_PolicyFinalize(&ctx);

            /* create one from calculated JSON */
            rc = Tss2_PolicyInit(
                buffer,
                halg,
                &ctx);
            assert_int_equal(rc, TSS2_RC_SUCCESS);

            rc = Tss2_PolicyCalculate(ctx);
            assert_int_equal(rc, TSS2_RC_SUCCESS);

            rc = Tss2_PolicyGetCalculatedDigest(ctx, &digest);
            assert_int_equal(rc, TSS2_RC_SUCCESS);
            assert_int_equal(digest.size, expected_hash_size);

            if (halg == TPM2_ALG_SHA1) {
                bin2hex(digest.buffer, digest.size, hexdigest);
                assert_string_equal(p->sha1, hexdigest);
            } else if (halg == TPM2_ALG_SHA256) {
                bin2hex(digest.buffer, digest.size, hexdigest);
                assert_string_equal(p->sha256, hexdigest);
            }

            SAFE_FREE(json);
            SAFE_FREE(buffer);
            Tss2_PolicyFinalize(&ctx);
        } /* end for each hash algorithm */
    } /* end for each policy file */
} /* end of cmocka test */

int main (
    int argc,
    char *argv[])
{
    UNUSED(argc);
    UNUSED(argv);

    const struct CMUnitTest tests[] = {
        cmocka_unit_test(test_policy_instantiate)
    };

    return cmocka_run_group_tests(tests, NULL, NULL);
}
