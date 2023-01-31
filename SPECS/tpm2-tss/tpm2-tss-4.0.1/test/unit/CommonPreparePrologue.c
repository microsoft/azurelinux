/* SPDX-License-Identifier: BSD-2-Clause */
/***********************************************************************
 * Copyright (c) 2017-2018, Intel Corporation
 *
 * All rights reserved.
 ***********************************************************************/
#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <stdlib.h>
#include <stdio.h>

#include <setjmp.h>
#include <cmocka.h>

#include "tss2_sys.h"
#include "sysapi_util.h"

#define MAX_SIZE_CTX 4096

/**
 * Pass CommonPreparePrologue a NULL TSS2_SYS_CONTEXT.
 */
static void
CommonPreparePrologue_null_sys_context_unit (void **state)
{
    TSS2_RC rc;

    rc = CommonPreparePrologue (NULL, 0);
    assert_int_equal (rc, TSS2_SYS_RC_BAD_REFERENCE);
}

/**
 * Accessing the _TSS2_SYS_CONTEXT_BLOB directly like this isn't allowed
 * in normal code. Use the opaque TSS2_SYS_CONTEXT in user space
 * applications. In the test cases we do this to induce error conditions.
 */
static int
CommonPreparePrologue_sys_setup (void **state)
{
    _TSS2_SYS_CONTEXT_BLOB  *sys_ctx;
    UINT32 size_ctx;

    size_ctx = Tss2_Sys_GetContextSize (MAX_SIZE_CTX);
    sys_ctx = calloc (1, size_ctx);
    assert_non_null (sys_ctx);

    *state = sys_ctx;
    return 0;
}

static int
CommonPreparePrologue_sys_teardown (void **state)
{
    _TSS2_SYS_CONTEXT_BLOB *sys_ctx = (_TSS2_SYS_CONTEXT_BLOB*)*state;

    if (sys_ctx)
        free (sys_ctx);

    return 0;
}

/**
 * CommonPrepareProlog must be passed a sys context with previousStage
 * set to either CMD_STAGE_INITIALIZE, CMD_STAGE_RECEIVE_RESPONSE or
 * CMD_STAGE_PREPARE.
 */
static void
CommonPreparePrologue_previous_stage_initialize (void **state)
{
    _TSS2_SYS_CONTEXT_BLOB *sys_ctx = (_TSS2_SYS_CONTEXT_BLOB*)*state;
    TSS2_RC rc;

    sys_ctx->previousStage |= ~CMD_STAGE_INITIALIZE;
    rc = CommonPreparePrologue (sys_ctx, 0);
    assert_int_equal (rc, TSS2_SYS_RC_BAD_SEQUENCE);
}
static void
CommonPreparePrologue_previous_stage_prepare (void **state)
{
    _TSS2_SYS_CONTEXT_BLOB *sys_ctx = (_TSS2_SYS_CONTEXT_BLOB*)*state;
    TSS2_RC rc;

    sys_ctx->previousStage |= ~CMD_STAGE_RECEIVE_RESPONSE;
    rc = CommonPreparePrologue (sys_ctx, 0);
    assert_int_equal (rc, TSS2_SYS_RC_BAD_SEQUENCE);
}
static void
CommonPreparePrologue_previous_stage_response (void **state)
{
    _TSS2_SYS_CONTEXT_BLOB *sys_ctx = (_TSS2_SYS_CONTEXT_BLOB*)*state;
    TSS2_RC rc;

    sys_ctx->previousStage |= ~CMD_STAGE_PREPARE;
    rc = CommonPreparePrologue (sys_ctx, 0);
    assert_int_equal (rc, TSS2_SYS_RC_BAD_SEQUENCE);
}
int
main (int argc, char* arvg[])
{
    const struct CMUnitTest tests[] = {
        cmocka_unit_test(CommonPreparePrologue_null_sys_context_unit),
        cmocka_unit_test_setup_teardown (CommonPreparePrologue_previous_stage_initialize,
                                  CommonPreparePrologue_sys_setup,
                                  CommonPreparePrologue_sys_teardown),
        cmocka_unit_test_setup_teardown (CommonPreparePrologue_previous_stage_prepare,
                                  CommonPreparePrologue_sys_setup,
                                  CommonPreparePrologue_sys_teardown),
        cmocka_unit_test_setup_teardown (CommonPreparePrologue_previous_stage_response,
                                  CommonPreparePrologue_sys_setup,
                                  CommonPreparePrologue_sys_teardown),
    };
    return cmocka_run_group_tests (tests, NULL, NULL);
}
