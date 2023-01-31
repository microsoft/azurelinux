/* SPDX-License-Identifier: BSD-2-Clause */
/***********************************************************************;
 * Copyright (c) 2022, Infineon Technologies AG
 * All rights reserved.
 ***********************************************************************/

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <inttypes.h>
#include <limits.h>
#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include <setjmp.h>
#include <cmocka.h>

#include "tss2_tcti.h"
#include "tss2_tcti_spi_helper.h"

#include "tss2-tcti/tcti-common.h"
#include "tss2-tcti/tcti-spi-helper.h"
#include "util/key-value-parse.h"

#define DUMMY_PLATFORM_DATA "my platform data"

typedef enum {
    TPM_DID_VID_HEAD = 0,
    TPM_DID_VID_BODY,
    TPM_ACCESS_HEAD,
    TPM_ACCESS_BODY,
    TPM_STS_HEAD,
    TPM_STS_BODY,
    TPM_RID_HEAD,
    TPM_RID_BODY
} tpm_state_t;

static const unsigned char TPM_DID_VID_0[] = {0x83, 0xd4, 0x0f, 0x00, 0xd1, 0x15, 0x1b, 0x00};
static const unsigned char TPM_ACCESS_0[] = {0x80, 0xd4, 0x00, 0x00, 0xa1};
static const unsigned char TPM_STS_0[] = {0x83, 0xd4, 0x00, 0x18, 0x40, 0x00, 0x00, 0x00};
static const unsigned char TPM_RID_0[] = {0x80, 0xd4, 0x0f, 0x04, 0x00};

TSS2_RC platform_sleep_ms (void* user_data, int32_t milliseconds)
{
    (void) milliseconds;
    assert_string_equal ((const char *) user_data, DUMMY_PLATFORM_DATA);
    return TSS2_RC_SUCCESS;
}

TSS2_RC platform_start_timeout (void* user_data, int32_t milliseconds)
{
    (void) milliseconds;
    assert_string_equal ((const char *) user_data, DUMMY_PLATFORM_DATA);
    return TSS2_RC_SUCCESS;
}

TSS2_RC platform_timeout_expired (void* user_data, bool *is_timeout_expired)
{
    assert_string_equal ((const char *) user_data, DUMMY_PLATFORM_DATA);
    *is_timeout_expired = true;
    return TSS2_RC_SUCCESS;
}

TSS2_RC platform_spi_acquire (void* user_data)
{
    (void) user_data;
    return TSS2_RC_SUCCESS;
}

TSS2_RC platform_spi_release (void* user_data)
{
    (void) user_data;
    return TSS2_RC_SUCCESS;
}

TSS2_RC platform_spi_transfer_no_wait_state (void* user_data, const void *data_out, void *data_in, size_t cnt)
{
    static tpm_state_t tpm_state = TPM_DID_VID_HEAD;

    assert_string_equal ((const char *) user_data, DUMMY_PLATFORM_DATA);

    switch (tpm_state) {
    case TPM_DID_VID_HEAD:
        assert_int_equal (cnt, 8);
        assert_true (!memcmp (data_out, TPM_DID_VID_0, 4));
        memcpy (data_in, TPM_DID_VID_0, sizeof (TPM_DID_VID_0));
        break;
    case TPM_ACCESS_HEAD:
        assert_int_equal (cnt, 5);
        assert_true (!memcmp (data_out, TPM_ACCESS_0, 4));
        memcpy (data_in, TPM_ACCESS_0, sizeof (TPM_ACCESS_0));
        break;
    case TPM_STS_HEAD:
        assert_int_equal (cnt, 8);
        assert_true (!memcmp (data_out, TPM_STS_0, 4));
        memcpy (data_in, TPM_STS_0, sizeof (TPM_STS_0));
        break;
    case TPM_RID_HEAD:
        assert_int_equal (cnt, 5);
        assert_true (!memcmp (data_out, TPM_RID_0, 4));
        memcpy (data_in, TPM_RID_0, sizeof (TPM_RID_0));
        break;
    default:
        assert_true (false);
    }

    tpm_state += 2;

    return TSS2_RC_SUCCESS;
}

TSS2_RC platform_spi_transfer_with_wait_state (void* user_data, const void *data_out, void *data_in, size_t cnt)
{
    static tpm_state_t tpm_state = TPM_DID_VID_HEAD;

    assert_string_equal ((const char *) user_data, DUMMY_PLATFORM_DATA);

    switch (tpm_state++) {
    case TPM_DID_VID_HEAD:
        assert_int_equal (cnt, 4);
        assert_true (!memcmp (data_out, TPM_DID_VID_0, 4));
        memcpy (data_in, TPM_DID_VID_0, 4);
        ((unsigned char *)data_in)[3] |= 0x01;
        break;
    case TPM_DID_VID_BODY:
        assert_int_equal (cnt, sizeof (TPM_DID_VID_0) - 4);
        memcpy (data_in, TPM_DID_VID_0 + 4, sizeof (TPM_DID_VID_0) - 4);
        break;
    case TPM_ACCESS_HEAD:
        assert_int_equal (cnt, 4);
        assert_true (!memcmp (data_out, TPM_ACCESS_0, 4));
        memcpy (data_in, TPM_ACCESS_0, 4);
        ((unsigned char *)data_in)[3] |= 0x01;
        break;
    case TPM_ACCESS_BODY:
        assert_int_equal (cnt, sizeof (TPM_ACCESS_0) - 4);
        memcpy (data_in, TPM_ACCESS_0 + 4, sizeof (TPM_ACCESS_0) - 4);
        break;
    case TPM_STS_HEAD:
        assert_int_equal (cnt, 4);
        assert_true (!memcmp (data_out, TPM_STS_0, 4));
        memcpy (data_in, TPM_STS_0, 4);
        ((unsigned char *)data_in)[3] |= 0x01;
        break;
    case TPM_STS_BODY:
        assert_int_equal (cnt, sizeof (TPM_STS_0) - 4);
        memcpy (data_in, TPM_STS_0 + 4, sizeof (TPM_STS_0) - 4);
        break;
    case TPM_RID_HEAD:
        assert_int_equal (cnt, 4);
        assert_true (!memcmp (data_out, TPM_RID_0, 4));
        memcpy (data_in, TPM_RID_0, 4);
        ((unsigned char *)data_in)[3] |= 0x01;
        break;
    case TPM_RID_BODY:
        assert_int_equal (cnt, sizeof (TPM_RID_0) - 4);
        memcpy (data_in, TPM_RID_0 + 4, 1);
        break;
    default:
        assert_true (false);
    }

    return TSS2_RC_SUCCESS;
}

void platform_finalize(void* user_data)
{
    assert_string_equal ((const char *) user_data, DUMMY_PLATFORM_DATA);
    free(user_data);
}

TSS2_TCTI_SPI_HELPER_PLATFORM create_tcti_spi_helper_platform (bool wait_state)
{
    TSS2_TCTI_SPI_HELPER_PLATFORM platform = {};

    // Create dummy platform user data
    char *platform_data = malloc (sizeof (DUMMY_PLATFORM_DATA));
    memcpy (platform_data, DUMMY_PLATFORM_DATA, sizeof (DUMMY_PLATFORM_DATA));

    // Create TCTI SPI platform struct with custom platform methods
    platform.user_data = platform_data;
    platform.sleep_ms = platform_sleep_ms;
    platform.start_timeout = platform_start_timeout;
    platform.timeout_expired = platform_timeout_expired;
    if (wait_state) {
        platform.spi_acquire = platform_spi_acquire;
        platform.spi_release = platform_spi_release;
        platform.spi_transfer = platform_spi_transfer_with_wait_state;
    } else {
        platform.spi_acquire = NULL;
        platform.spi_release = NULL;
        platform.spi_transfer = platform_spi_transfer_no_wait_state;
    }
    platform.finalize = platform_finalize;

    return platform;
}

/*
 * The test will invoke Tss2_Tcti_Spi_Helper_Init() and subsequently
 * it will start reading TPM_DID_VID, claim locality, read TPM_STS,
 * and finally read TPM_RID before exiting the Init function.
 * For testing purpose, the TPM responses are hardcoded.
 * SPI wait state is not supported in this test.
 */
static void
tcti_spi_no_wait_state_success_test (void **state)
{
    TSS2_RC rc;
    size_t size;
    TSS2_TCTI_SPI_HELPER_PLATFORM tcti_platform = {};
    TSS2_TCTI_CONTEXT* tcti_ctx;

    // Get requested TCTI context size
    rc = Tss2_Tcti_Spi_Helper_Init (NULL, &size, &tcti_platform);
    assert_int_equal (rc, TSS2_RC_SUCCESS);

    // Allocate TCTI context size
    tcti_ctx = (TSS2_TCTI_CONTEXT*) calloc (1, size);
    assert_non_null (tcti_ctx);

    // Initialize TCTI context
    tcti_platform = create_tcti_spi_helper_platform (false);
    rc = Tss2_Tcti_Spi_Helper_Init (tcti_ctx, &size, &tcti_platform);
    assert_int_equal (rc, TSS2_RC_SUCCESS);

    free (tcti_platform.user_data);
    free (tcti_ctx);
}

/*
 * Similar to tcti_spi_no_wait_state_success_test
 * except wait state is supported here.
 */
static void
tcti_spi_with_wait_state_success_test (void **state)
{
    TSS2_RC rc;
    size_t size;
    TSS2_TCTI_SPI_HELPER_PLATFORM tcti_platform = {};
    TSS2_TCTI_CONTEXT* tcti_ctx;

    // Get requested TCTI context size
    rc = Tss2_Tcti_Spi_Helper_Init (NULL, &size, &tcti_platform);
    assert_int_equal (rc, TSS2_RC_SUCCESS);

    // Allocate TCTI context size
    tcti_ctx = (TSS2_TCTI_CONTEXT*) calloc (1, size);
    assert_non_null (tcti_ctx);

    // Initialize TCTI context
    tcti_platform = create_tcti_spi_helper_platform (true);
    rc = Tss2_Tcti_Spi_Helper_Init (tcti_ctx, &size, &tcti_platform);
    assert_int_equal (rc, TSS2_RC_SUCCESS);

    free (tcti_platform.user_data);
    free (tcti_ctx);
}

static void
tcti_spi_with_bad_callbacks_test (void **state)
{
    TSS2_RC rc;
    size_t size;
    TSS2_TCTI_SPI_HELPER_PLATFORM tcti_platform = {};
    TSS2_TCTI_CONTEXT* tcti_ctx;

    // Get requested TCTI context size
    rc = Tss2_Tcti_Spi_Helper_Init (NULL, &size, &tcti_platform);
    assert_int_equal (rc, TSS2_RC_SUCCESS);

    // Allocate TCTI context size
    tcti_ctx = (TSS2_TCTI_CONTEXT*) calloc (1, size);
    assert_non_null (tcti_ctx);

    // Initialize TCTI context
    tcti_platform = create_tcti_spi_helper_platform (false);
    tcti_platform.sleep_ms = NULL;
    rc = Tss2_Tcti_Spi_Helper_Init (tcti_ctx, &size, &tcti_platform);
    assert_int_equal (rc, TSS2_TCTI_RC_BAD_VALUE);

    free (tcti_platform.user_data);
    free (tcti_ctx);
}

static void
tcti_spi_with_wait_state_bad_callbacks_test (void **state)
{
    TSS2_RC rc;
    size_t size;
    TSS2_TCTI_SPI_HELPER_PLATFORM tcti_platform = {};
    TSS2_TCTI_CONTEXT* tcti_ctx;

    // Get requested TCTI context size
    rc = Tss2_Tcti_Spi_Helper_Init (NULL, &size, &tcti_platform);
    assert_int_equal (rc, TSS2_RC_SUCCESS);

    // Allocate TCTI context size
    tcti_ctx = (TSS2_TCTI_CONTEXT*) calloc (1, size);
    assert_non_null (tcti_ctx);

    // Initialize TCTI context
    tcti_platform = create_tcti_spi_helper_platform (true);
    tcti_platform.spi_acquire = NULL;
    rc = Tss2_Tcti_Spi_Helper_Init (tcti_ctx, &size, &tcti_platform);
    assert_int_equal (rc, TSS2_TCTI_RC_BAD_VALUE);

    free (tcti_platform.user_data);
    free (tcti_ctx);
}

int
main (int   argc,
      char *argv[])
{
    const struct CMUnitTest tests[] = {
        cmocka_unit_test (tcti_spi_no_wait_state_success_test),
        cmocka_unit_test (tcti_spi_with_wait_state_success_test),
        cmocka_unit_test (tcti_spi_with_bad_callbacks_test),
        cmocka_unit_test (tcti_spi_with_wait_state_bad_callbacks_test)
    };
    return cmocka_run_group_tests (tests, NULL, NULL);
}
