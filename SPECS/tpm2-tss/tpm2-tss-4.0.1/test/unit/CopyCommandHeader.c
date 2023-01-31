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
#include <arpa/inet.h>

#include <setjmp.h>
#include <cmocka.h>

#include "tss2_sys.h"
#include "sysapi_util.h"

#define MAX_SIZE_CTX 4096
/**
 *
 */
static int
CopyCommandHeader_sys_setup (void **state)
{
    _TSS2_SYS_CONTEXT_BLOB *sys_ctx;
    UINT32 size_ctx;

    size_ctx = Tss2_Sys_GetContextSize (MAX_SIZE_CTX);
    sys_ctx = calloc (1, size_ctx);
    assert_non_null (sys_ctx);
    /**
     *  This is the important part: the CopyCommandHeader function builds up
     *  the command buffer in the memory pointed to by tpmInitBuffPtr. This
     *  must point to the data after the context structure.
     */
    sys_ctx->cmdBuffer = (UINT8*) (sys_ctx + sizeof (_TSS2_SYS_CONTEXT_BLOB));
    InitSysContextFields (sys_ctx);
    InitSysContextPtrs (sys_ctx, size_ctx);

    *state = sys_ctx;
    return 0;
}

static int
CopyCommandHeader_sys_teardown (void **state)
{
    TSS2_SYS_CONTEXT *sys_ctx = (TSS2_SYS_CONTEXT*)*state;

    if (sys_ctx)
        free (sys_ctx);

    return 0;
}

/**
 *  CopyCommandHeader creates the standard TPM command header (tag, size,
 *  command_code) to the data buffer in the context structure. It also
 *  advances the 'nextData' pointer to the address after the header. This
 *  test will fail if the nextData pointer isn't set as expected
 */
static void
CopyCommandHeader_nextData_unit (void **state)
{
    _TSS2_SYS_CONTEXT_BLOB *sys_ctx = (_TSS2_SYS_CONTEXT_BLOB *)*state;
    TPM2_CC cc = TPM2_CC_GetCapability;

    CopyCommandHeader (sys_ctx, cc);
    assert_int_equal (sys_ctx->nextData, sizeof (TPM20_Header_In));
}

/**
 * After a call to CopyCommandHeader the tag in the TPM20_Header_In portion of
 * the cmdBuffer member of the sys context should be TPM2_ST_NO_SESSIONS
 * transformed into network byte order.
 */
static void
CopyCommandHeader_tag_unit (void **state)
{
    _TSS2_SYS_CONTEXT_BLOB *sys_ctx = (_TSS2_SYS_CONTEXT_BLOB*)*state;
    TPM2_CC cc = TPM2_CC_GetCapability;
    TPM20_Header_In *header = (TPM20_Header_In*)sys_ctx->cmdBuffer;
    /* The TSS code uses a custom function to convert stuff to network byte
     * order but we can just use htons. Not sure why we don't use htons/l
     * everywhere.
     */
    TPMI_ST_COMMAND_TAG tag_net = htons (TPM2_ST_NO_SESSIONS);

    CopyCommandHeader (sys_ctx, cc);
    assert_int_equal (tag_net, header->tag);
}
/**
 * After a call to CopyCommandHeader the commandCode in the TPM20_Header_In
 * portion of the cmdBuffer member of the sys context should be the command
 * code parameter in network byte order.
 */
static void
CopyCommandHeader_commandcode_unit (void **state)
{
    _TSS2_SYS_CONTEXT_BLOB *sys_ctx = (_TSS2_SYS_CONTEXT_BLOB*)*state;
    TPM2_CC cc = TPM2_CC_GetCapability;
    TPM2_CC cc_net = htonl (cc);
    TPM20_Header_In *header = (TPM20_Header_In*)sys_ctx->cmdBuffer;

    CopyCommandHeader (sys_ctx, cc);
    assert_int_equal (cc_net, header->commandCode);
}

int
main (int argc, char* argv[])
{
    const struct CMUnitTest tests[] = {
        cmocka_unit_test_setup_teardown (CopyCommandHeader_nextData_unit,
                                  CopyCommandHeader_sys_setup,
                                  CopyCommandHeader_sys_teardown),
        cmocka_unit_test_setup_teardown (CopyCommandHeader_tag_unit,
                                  CopyCommandHeader_sys_setup,
                                  CopyCommandHeader_sys_teardown),
        cmocka_unit_test_setup_teardown (CopyCommandHeader_commandcode_unit,
                                  CopyCommandHeader_sys_setup,
                                  CopyCommandHeader_sys_teardown),
    };
    return cmocka_run_group_tests (tests, NULL, NULL);
}
