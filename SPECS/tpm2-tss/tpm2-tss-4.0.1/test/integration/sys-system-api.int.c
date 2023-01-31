/* SPDX-License-Identifier: BSD-2-Clause */
/***********************************************************************
 * Copyright (c) 2017-2018, Intel Corporation
 *
 * All rights reserved.
 ***********************************************************************/
#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <stdio.h>
#include <stdlib.h>

#include "tss2_sys.h"

#define LOGMODULE test
#include "util/log.h"
#include "test.h"
#include "sys-util.h"

/*
 * System API tests including invalid cases
 */
int
test_invoke (TSS2_SYS_CONTEXT *sys_context)
{
    TPM2B_MAX_BUFFER    outData = TPM2B_NAMED_INIT(TPM2B_MAX_BUFFER, buffer);
    TPM2B_PUBLIC        outPublic;
    TPM2B_NAME          name = TPM2B_NAME_INIT;
    TPM2B_NAME          qualifiedName;
    TPM2_HANDLE          handle = 0;
    TPM2_CC              commandCode;
    size_t              rpBufferUsedSize;
    const uint8_t      *rpBuffer;
    TSS2_RC             rc;

    LOG_INFO("System API test");
    /* Test for bad reference. */
    rc = Tss2_Sys_GetTestResult_Prepare(0);
    if (rc != TSS2_SYS_RC_BAD_REFERENCE) {
        LOG_ERROR("Invalid prepare test FAILED! Response Code : 0x%x", rc);
        exit(1);
    }

    /* Test for bad sequence:  after ExecuteAsync */
    rc = Tss2_Sys_GetTestResult_Prepare(sys_context);
    if (rc != TSS2_RC_SUCCESS) {
        LOG_ERROR("Prepare test FAILED! Response Code : 0x%x", rc);
        exit(1);
    }

    rc = Tss2_Sys_ExecuteAsync(sys_context);
    if (rc != TSS2_RC_SUCCESS) {
        LOG_ERROR("Prepare test FAILED! Response Code : 0x%x", rc);
        exit(1);
    }

    rc = Tss2_Sys_GetTestResult_Prepare(sys_context);
    if (rc != TSS2_SYS_RC_BAD_SEQUENCE) {
        LOG_ERROR("Invalid prepare test FAILED! Response Code : 0x%x", rc);
        exit(1);
    }

    rc = Tss2_Sys_ExecuteFinish(sys_context, -1);
    if (rc != TSS2_RC_SUCCESS) {
        LOG_ERROR("Prepare test FAILED! Response Code : 0x%x", rc);
        exit(1);
    }

    /* Test for bad sequence:  after Execute */
    rc = Tss2_Sys_GetTestResult_Prepare(sys_context);
    if (rc != TSS2_RC_SUCCESS) {
        LOG_ERROR("Prepare test FAILED! Response Code : 0x%x", rc);
        exit(1);
    }

    rc = Tss2_Sys_Execute(sys_context);
    if (rc != TSS2_RC_SUCCESS) {
        LOG_ERROR("Prepare test FAILED! Response Code : 0x%x", rc);
        exit(1);
    }

    rc = Tss2_Sys_GetTestResult_Prepare(sys_context);
    if (rc != TSS2_RC_SUCCESS) {
        LOG_ERROR("Prepare test FAILED! Response Code : 0x%x", rc);
        exit(1);
    }

    rc = Tss2_Sys_GetTestResult_Prepare(sys_context);
    if (rc != TSS2_RC_SUCCESS) {
        LOG_ERROR("Prepare test FAILED! Response Code : 0x%x", rc);
        exit(1);
    }

    /* Test for other NULL params */
    rc = Tss2_Sys_Create_Prepare(sys_context, 0xffffffff, 0, 0, 0, 0);
    if (rc != TSS2_SYS_RC_BAD_REFERENCE) {
        LOG_ERROR("Invalid prepare test FAILED! Response Code : 0x%x", rc);
        exit(1);
    }

    rc = Tss2_Sys_GetTestResult(sys_context, 0, &outData, &rc, 0);
    if (rc != TSS2_RC_SUCCESS) {
        LOG_ERROR("GetTestResult test FAILED! Response Code : 0x%x", rc);
        exit(1);
    }

    /* Check for BAD_SEQUENCE error. */
    rc = Tss2_Sys_ExecuteAsync(sys_context);
    if (rc != TSS2_SYS_RC_BAD_SEQUENCE) {
        LOG_ERROR("SYS invalid test FAILED! Response Code : 0x%x", rc);
        exit(1);
    }

    /* Check for BAD_SEQUENCE error. */
    rc = Tss2_Sys_Execute(sys_context);
    if (rc != TSS2_SYS_RC_BAD_SEQUENCE) {
        LOG_ERROR("SYS invalid test FAILED! Response Code : 0x%x", rc);
        exit(1);
    }

    /* Test the synchronous, non-one-call interface. */
    rc = Tss2_Sys_GetTestResult_Prepare(sys_context);
    if (rc != TSS2_RC_SUCCESS) {
        LOG_ERROR("SYS test FAILED! Response Code : 0x%x", rc);
        exit(1);
    }

    /* Check for BAD_REFERENCE error. */
    rc = Tss2_Sys_Execute(0);
    if (rc != TSS2_SYS_RC_BAD_REFERENCE) {
        LOG_ERROR("SYS invalid test FAILED! Response Code : 0x%x", rc);
        exit(1);
    }

    /* Execute the command synchronously. */
    rc = Tss2_Sys_Execute(sys_context);
    if (rc != TSS2_RC_SUCCESS) {
        LOG_ERROR("SYS test FAILED! Response Code : 0x%x", rc);
        exit(1);
    }

    /* Check for BAD_SEQUENCE error. */
    rc = Tss2_Sys_Execute(sys_context);
    if (rc != TSS2_SYS_RC_BAD_SEQUENCE) {
        LOG_ERROR("SYS invalid test FAILED! Response Code : 0x%x", rc);
        exit(1);
    }

    /* Check for BAD_SEQUENCE error. */
    rc = Tss2_Sys_ExecuteAsync(sys_context);
    if (rc != TSS2_SYS_RC_BAD_SEQUENCE) {
        LOG_ERROR("SYS invalid test FAILED! Response Code : 0x%x", rc);
        exit(1);
    }

    /* Now test the asynchronous, non-one-call interface. */
    rc = Tss2_Sys_GetTestResult_Prepare(sys_context);
    if (rc != TSS2_RC_SUCCESS) {
        LOG_ERROR("SYS test FAILED! Response Code : 0x%x", rc);
        exit(1);
    }

    rc = Tss2_Sys_GetTestResult_Complete(sys_context, &outData, &rc);
    if (rc != TSS2_SYS_RC_BAD_SEQUENCE) {
        LOG_ERROR("SYS invalid test FAILED! Response Code : 0x%x", rc);
        exit(1);
    }

    /* Check for BAD_REFERENCE error. */
    rc = Tss2_Sys_ExecuteAsync(0);
    if (rc != TSS2_SYS_RC_BAD_REFERENCE) {
        LOG_ERROR("SYS invalid test FAILED! Response Code : 0x%x", rc);
        exit(1);
    }

    /* Test ExecuteFinish for BAD_SEQUENCE */
    rc = Tss2_Sys_ExecuteFinish(sys_context, TSS2_TCTI_TIMEOUT_BLOCK);
    if (rc != TSS2_SYS_RC_BAD_SEQUENCE) {
        LOG_ERROR("SYS invalid test FAILED! Response Code : 0x%x", rc);
        exit(1);
    }

    /* Execute the command asynchronously. */
    rc = Tss2_Sys_ExecuteAsync(sys_context);
    if (rc != TSS2_RC_SUCCESS) {
        LOG_ERROR("SYS test FAILED! Response Code : 0x%x", rc);
        exit(1);
    }

    /* Check for BAD_SEQUENCE error. */
    rc = Tss2_Sys_ExecuteAsync(sys_context);
    if (rc != TSS2_SYS_RC_BAD_SEQUENCE) {
        LOG_ERROR("SYS invalid test FAILED! Response Code : 0x%x", rc);
        exit(1);
    }

    /* Check for BAD_SEQUENCE error. */
    rc = Tss2_Sys_Execute(sys_context);
    if (rc != TSS2_SYS_RC_BAD_SEQUENCE) {
        LOG_ERROR("SYS invalid test FAILED! Response Code : 0x%x", rc);
        exit(1);
    }

    /* Test ExecuteFinish for BAD_REFERENCE */
    rc = Tss2_Sys_ExecuteFinish(0, TSS2_TCTI_TIMEOUT_BLOCK);
    if (rc != TSS2_SYS_RC_BAD_REFERENCE) {
        LOG_ERROR("SYS invalid test FAILED! Response Code : 0x%x", rc);
        exit(1);
    }

    /* Test XXXX_Complete for bad sequence:  after _Prepare
     * and before ExecuteFinish */
    rc = Tss2_Sys_GetTestResult_Complete(sys_context, &outData, &rc);
    if (rc != TSS2_SYS_RC_BAD_SEQUENCE) {
        LOG_ERROR("SYS invalid test FAILED! Response Code : 0x%x", rc);
        exit(1);
    }

    /* Get the command response. Wait a maximum of 20ms
     * for response. */
    rc = Tss2_Sys_ExecuteFinish(sys_context, TSS2_TCTI_TIMEOUT_BLOCK);
    if (rc != TSS2_RC_SUCCESS) {
        LOG_ERROR("SYS test FAILED! Response Code : 0x%x", rc);
        exit(1);
    }

    rc = Tss2_Sys_ExecuteFinish(sys_context, TSS2_TCTI_TIMEOUT_BLOCK);
    if (rc != TSS2_SYS_RC_BAD_SEQUENCE) {
        LOG_ERROR("SYS invalid test FAILED! Response Code : 0x%x", rc);
        exit(1);
    }

    /* Check for BAD_SEQUENCE error. */
    rc = Tss2_Sys_ExecuteAsync(sys_context);
    if (rc != TSS2_SYS_RC_BAD_SEQUENCE) {
        LOG_ERROR("SYS invalid test FAILED! Response Code : 0x%x", rc);
        exit(1);
    }

    /* Test _Complete for bad reference cases. */
    rc = Tss2_Sys_GetTestResult_Complete(0, &outData, &rc);
    if (rc != TSS2_SYS_RC_BAD_REFERENCE) {
        LOG_ERROR("SYS invalid test FAILED! Response Code : 0x%x", rc);
        exit(1);
    }

    rc = Tss2_Sys_ReadPublic_Prepare(sys_context, handle);
    if (rc != TSS2_RC_SUCCESS) {
        LOG_ERROR("SYS test FAILED! Response Code : 0x%x", rc);
        exit(1);
    }

    /* Execute the command synchronously. */
    rc = Tss2_Sys_ExecuteAsync(sys_context);
    if (rc != TSS2_RC_SUCCESS) {
        LOG_ERROR("SYS test FAILED! Response Code : 0x%x", rc);
        exit(1);
    }

    /* Test _Complete for bad sequence case when ExecuteFinish has never
     * been done on a context. */
    rc = Tss2_Sys_ReadPublic_Complete(sys_context, &outPublic, &name, &qualifiedName);
    if (rc != TSS2_SYS_RC_BAD_SEQUENCE) {
        LOG_ERROR("SYS invalid test FAILED! Response Code : 0x%x", rc);
        exit(1);
    }

    rc = Tss2_Sys_GetRpBuffer(sys_context, &rpBufferUsedSize, &rpBuffer);
    if (rc != TSS2_SYS_RC_BAD_SEQUENCE) {
        LOG_ERROR("SYS invalid test FAILED! Response Code : 0x%x", rc);
        exit(1);
    }
    /* CheckFailed(rc, TSS2_SYS_RC_BAD_SEQUENCE); */

    /* Execute the command synchronously. */
    rc = Tss2_Sys_ExecuteFinish(sys_context, TSS2_TCTI_TIMEOUT_BLOCK);
    if (rc != TPM2_RC_VALUE + TPM2_RC_1) {
        LOG_ERROR("SYS test FAILED! Response Code : 0x%x", rc);
        exit(1);
    }

    /* Test one-call for null sys_context pointer. */
    rc = Tss2_Sys_Startup(0, TPM2_SU_CLEAR);
    if (rc != TSS2_SYS_RC_BAD_REFERENCE) {
        LOG_ERROR("SYS invalid test FAILED! Response Code : 0x%x", rc);
        exit(1);
    }

    /* Test one-call for NULL input parameter that should be a pointer. */
    rc = Tss2_Sys_Create(sys_context, 0xffffffff, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);
    if (rc != TSS2_SYS_RC_BAD_REFERENCE) {
        LOG_ERROR("SYS invalid test FAILED! Response Code : 0x%x", rc);
        exit(1);
    }

    /* Test GetCommandCode for bad reference */
    rc = Tss2_Sys_GetCommandCode(0, (UINT8 *)&commandCode);
    if (rc != TSS2_SYS_RC_BAD_REFERENCE) {
        LOG_ERROR("SYS invalid test FAILED! Response Code : 0x%x", rc);
        exit(1);
    }

    rc = Tss2_Sys_GetCommandCode(sys_context, NULL);
    if (rc != TSS2_SYS_RC_BAD_REFERENCE) {
        LOG_ERROR("SYS invalid test FAILED! Response Code : 0x%x", rc);
        exit(1);
    }

    LOG_INFO("System API test Passed!");
    return 0;
}
