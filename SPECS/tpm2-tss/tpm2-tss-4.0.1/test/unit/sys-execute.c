/* SPDX-License-Identifier: BSD-2-Clause */
/*******************************************************************************
 * Copyright 2019, Intel Corporation
 *
 * All rights reserved.
 ******************************************************************************/

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <stdarg.h>
#include <inttypes.h>
#include <string.h>
#include <stdlib.h>
#include <setjmp.h>
#include <cmocka.h>

#include "tss2_sys.h"
#include "sysapi_util.h"
#include "tss2-tcti/tcti-common.h"


#define LOGMODULE test
#include "util/log.h"

/**
 * Test calls Tss2_Sys_Execute() many times after receiving TPM2_RC_RETRY
 */

const uint8_t ok_response[] = {
    0x80, 0x01,                 /* TPM_ST_NO_SESSION */
    0x00, 0x00, 0x00, 0x2C,     /* Response Size 10 + 2 + 32 */
    0x00, 0x00, 0x00, 0x00,     /* TPM_RC_SUCCESS */
    0x00, 0x20,                 /* size of buffer */
    0xde, 0xad, 0xbe, 0xef,
    0xde, 0xad, 0xbe, 0xef,
    0xde, 0xad, 0xbe, 0xef,
    0xde, 0xad, 0xbe, 0xef,
    0xde, 0xad, 0xbe, 0xef,
    0xde, 0xad, 0xbe, 0xef,
    0xde, 0xad, 0xbe, 0xef,
    0xde, 0xad, 0xbe, 0xef,
};

const uint8_t retry_response[] = {
    0x80, 0x01,                 /* TPM_ST_NO_SESSION */
    0x00, 0x00, 0x00, 0x0A,     /* Response Size 10 */
    0x00, 0x00, 0x09, 0x22      /* TPM2_RC_RETRY */
};

static TSS2_RC
tcti_transmit(
    TSS2_TCTI_CONTEXT *tctiContext,
    size_t size,
    uint8_t const *command)
{
    TSS2_RC r = 0;
    tpm_header_t hdr;

    LOG_DEBUG ("%s: transmiting %zu bytes", __func__, size);
    r = header_unmarshal (command, &hdr);
    if (r)
        return r;

    LOG_DEBUG ("%s request_hdr.tag  = %x", __func__, hdr.tag);
    LOG_DEBUG ("%s request_hdr.size  = %x", __func__, hdr.size);
    LOG_DEBUG ("%s request_hdr.code  = %x", __func__, hdr.code);

    if (hdr.tag != TPM2_ST_NO_SESSIONS || hdr.size != 0xC || hdr.code != 0x17B)
        return TSS2_TCTI_RC_BAD_VALUE;

    return r;
}

#define NUM_OF_RETRIES 4

static TSS2_RC
tcti_receive(
    TSS2_TCTI_CONTEXT *tctiContext,
    size_t *size,
    uint8_t *response,
    int32_t timeout)
{
    static int i;

    LOG_DEBUG ("%s: receiving response, size %zu, buff %p",
               __func__, sizeof(ok_response), response);

    if (response == NULL) {
        *size = sizeof(ok_response);
        return TPM2_RC_SUCCESS;
    }

    if (i++ < NUM_OF_RETRIES) {
        LOG_DEBUG ("%s: return RC_RETRY", __func__);
        memcpy(response, retry_response, sizeof(retry_response));
        *size = sizeof(retry_response);
        return TPM2_RC_SUCCESS;
    }
    memcpy(response, ok_response, sizeof(ok_response));
    *size = sizeof(ok_response);
    return TPM2_RC_SUCCESS;
}

static TSS2_ABI_VERSION ver = TSS2_ABI_VERSION_CURRENT;
static TSS2_TCTI_CONTEXT_COMMON_V1 _tcti_v1_ctx;

static int
setup(void **state)
{
    TSS2_SYS_CONTEXT  *sys_ctx;
    TSS2_TCTI_CONTEXT *tcti_ctx = (TSS2_TCTI_CONTEXT *) &_tcti_v1_ctx;
    UINT32 size_ctx;
    TSS2_RC r;

    size_ctx = Tss2_Sys_GetContextSize(0);
    sys_ctx = calloc (1, size_ctx);
    assert_non_null (sys_ctx);
    _tcti_v1_ctx.version = 1;
    _tcti_v1_ctx.transmit = tcti_transmit;
    _tcti_v1_ctx.receive = tcti_receive;

    r = Tss2_Sys_Initialize(sys_ctx, size_ctx, tcti_ctx, &ver);
    assert_int_equal (r, TSS2_RC_SUCCESS);

    *state = sys_ctx;

    return 0;
}

static int
teardown(void **state)
{
    TSS2_SYS_CONTEXT *sys_ctx = (TSS2_SYS_CONTEXT *)*state;

    if (sys_ctx)
        free (sys_ctx);

    return 0;
}

static void
test_resubmit(void **state)
{
    TSS2_RC r = 0;
    TSS2_SYS_CONTEXT *sys_ctx = (TSS2_SYS_CONTEXT *)*state;
    int ctr = 0;

    r = Tss2_Sys_GetRandom_Prepare(sys_ctx, 32);
    assert_int_equal(r, TSS2_RC_SUCCESS);
    do {
        r = Tss2_Sys_Execute(sys_ctx);
    } while (r == TPM2_RC_RETRY && ctr++ < 10);

    assert_int_equal(r, TSS2_RC_SUCCESS);
    assert_int_equal(ctr, NUM_OF_RETRIES);
    return;
}

int
main(int argc, char *argv[])
{
    const struct CMUnitTest tests[] = {
        cmocka_unit_test_setup_teardown(test_resubmit, setup, teardown),
    };
    return cmocka_run_group_tests(tests, NULL, NULL);
}
