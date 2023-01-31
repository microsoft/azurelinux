/*
 * SPDX-License-Identifier: BSD-2-Clause
 * Copyright (c) 2019, Intel Corporation
 */

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <inttypes.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "tss2_sys.h"

#include "context-util.h"
#include "sys-util.h"
#include "session-util.h"
#define LOGMODULE test
#include "util/log.h"

#define TPM20_INDEX_PASSWORD_TEST       0x01500020

#define NV_DATA_SIZE 4
#define NV_DATA { 0x00, 0xff, 0x55, 0xaa }
#define SECRET_SIZE 13
#define SECRET_DATA { 's', 'h', 'a', 'r', 'e', 'd', ' ', \
                      's', 'e', 'c', 'r', 'e', 't', }

TSS2_RC
create_policy (TSS2_SYS_CONTEXT *sys_ctx,
               TPM2B_DIGEST *authPolicy)
{
    TSS2_RC rc;
    SESSION *trialPolicySession = NULL;
    TPM2B_NONCE nonceCaller = { 0, };
    TPM2B_ENCRYPTED_SECRET encryptedSalt = { 0, };
    TPMT_SYM_DEF symmetric = {
        .algorithm = TPM2_ALG_NULL,
    };
    TSS2_TCTI_CONTEXT *tcti_ctx;

    rc = Tss2_Sys_GetTctiContext (sys_ctx, &tcti_ctx);
    if (rc != TSS2_RC_SUCCESS || tcti_ctx == NULL) {
        LOG_ERROR("InitSysContext failed, exiting...");
        return rc;
    }

    rc = create_auth_session (&trialPolicySession,
                              TPM2_RH_NULL,
                              0,
                              TPM2_RH_NULL,
                              0,
                              &nonceCaller,
                              &encryptedSalt,
                              TPM2_SE_TRIAL,
                              &symmetric,
                              TPM2_ALG_SHA256,
                              tcti_ctx);
    if (rc != TSS2_RC_SUCCESS) {
        LOG_ERROR ("create_auth_session failed with rc: 0x%x", rc);
        return rc;
    }
    rc = Tss2_Sys_PolicyAuthValue (sys_ctx,
                                   trialPolicySession->sessionHandle,
                                   0,
                                   0);
    if (rc != TSS2_RC_SUCCESS) {
        LOG_ERROR ("Tss2_Sys_PolicyAuthValue failed with rc: 0x%x", rc);
        return rc;
    }
    rc = Tss2_Sys_PolicyGetDigest (sys_ctx,
                                   trialPolicySession->sessionHandle,
                                   0,
                                   authPolicy,
                                   0);
    if (rc != TSS2_RC_SUCCESS) {
        LOG_ERROR ("Tss2_Sys_PolicyGetDigest failed with rc: 0x%x", rc);
        return rc;
    }

    rc = Tss2_Sys_FlushContext (sys_ctx,
                                trialPolicySession->sessionHandle);
    if (rc != TSS2_RC_SUCCESS) {
        LOG_ERROR ("Tss2_Sys_FlushContext failed with rc: 0x%x", rc);
        return rc;
    }

    end_auth_session (trialPolicySession);
    return rc;
}

TSS2_RC
nv_rw_with_session (
    TSS2_SYS_CONTEXT *sys_ctx,
    const TPM2B_DIGEST *authPolicy,
    TPMA_NV nvAttributes,
    TPM2_SE session_type)
{
    TSS2_RC rc;
    TPM2B_AUTH  nvAuth = {
        .size = SECRET_SIZE,
        .buffer = SECRET_DATA,
    };
    SESSION *nvSession = NULL;
    TPM2B_NAME nvName;
    TPM2B_NONCE nonceCaller = { 0, };
    TPM2B_MAX_NV_BUFFER nvWriteData = {
        .size = NV_DATA_SIZE,
        .buffer = NV_DATA,
    };
    TPM2B_MAX_NV_BUFFER nvReadData = { .size = TPM2B_SIZE (nvReadData), };
    TPM2B_ENCRYPTED_SECRET encryptedSalt = { 0, };
    TPMT_SYM_DEF symmetric = {
        .algorithm = TPM2_ALG_NULL,
    };
    TSS2_TCTI_CONTEXT *tcti_ctx;
    TSS2L_SYS_AUTH_RESPONSE nvRspAuths;
    TSS2L_SYS_AUTH_COMMAND nvCmdAuths = {
        .count = 1,
        .auths= {
            {
                .nonce = {
                    .size = 1,
                    .buffer = { 0xa5, },
                },
                .sessionHandle = TPM2_RH_PW,
                .sessionAttributes = TPMA_SESSION_CONTINUESESSION,
            }
        }
    };
    const TSS2L_SYS_AUTH_COMMAND auth_cmd_null_pwd = {
        .count = 1,
        .auths = {
            {
                .sessionHandle = TPM2_RH_PW,
            },
        },
    };


    rc = Tss2_Sys_GetTctiContext (sys_ctx, &tcti_ctx);
    if (rc != TSS2_RC_SUCCESS || tcti_ctx == NULL) {
        LOG_ERROR ("Failed to get TCTI from Sys context, got RC: 0x%x", rc);
        return TSS2_SYS_RC_GENERAL_FAILURE;
    }

    rc = DefineNvIndex (sys_ctx,
                        TPM2_RH_PLATFORM,
                        &nvAuth,
                        authPolicy,
                        TPM20_INDEX_PASSWORD_TEST,
                        TPM2_ALG_SHA256,
                        nvAttributes,
                        32);
    if (rc != TSS2_RC_SUCCESS) {
        LOG_ERROR ("DefineNvIndex failed with RC: 0x%x", rc);
        return rc;
    }

    /*
     * Add index and associated authorization value to
     * entity table.  This helps when we need
     * to calculate HMACs.
     */
    rc = AddEntity(TPM20_INDEX_PASSWORD_TEST, &nvAuth);
    if (rc != TSS2_RC_SUCCESS) {
        LOG_ERROR ("AddEntity failed with RC: 0x%x", rc);
        return rc;
    }

    /* Get the name of the NV index. */
    rc = tpm_handle_to_name (tcti_ctx,
                             TPM20_INDEX_PASSWORD_TEST,
                             &nvName);
    if (rc != TSS2_RC_SUCCESS) {
        LOG_ERROR ("tpm_handle_to_name failed with RC: 0x%x", rc);
        return rc;
    }

    /*
     * Start HMAC or real (non-trial) policy authorization session:
     * it's an unbound and unsalted session, no symmetric
     * encryption algorithm, and SHA256 is the session's
     * hash algorithm.
     */
    rc = create_auth_session (&nvSession,
                              TPM2_RH_NULL,
                              0,
                              TPM2_RH_NULL,
                              0,
                              &nonceCaller,
                              &encryptedSalt,
                              session_type,
                              &symmetric,
                              TPM2_ALG_SHA256,
                              tcti_ctx);
    if (rc != TSS2_RC_SUCCESS) {
        LOG_ERROR ("create_auth_session failed with RC: 0x%x", rc);
        return rc;
    }

    /* set handle in command auth */
    nvCmdAuths.auths[0].sessionHandle = nvSession->sessionHandle;

    /*
     * Get the name of the session and save it in
     * the nvSession structure.
     */
    rc = tpm_handle_to_name (tcti_ctx,
                             nvSession->sessionHandle,
                             &nvSession->name);
    if (rc != TSS2_RC_SUCCESS) {
        LOG_ERROR ("tpm_handle_to_name failed with RC: 0x%x", rc);
        return rc;
    }

    /*
     * Now setup for writing the NV index.
     */
    if (session_type == TPM2_SE_POLICY) {
        rc = Tss2_Sys_PolicyAuthValue (sys_ctx,
                                       nvSession->sessionHandle,
                                       0,
                                       0);
        if (rc != TSS2_RC_SUCCESS) {
            LOG_ERROR ("Tss2_Sys_PolicyAuthValue failed with RC: 0x%x", rc);
            return rc;
        }
    }
    /* First call prepare in order to create cpBuffer. */
    rc = Tss2_Sys_NV_Write_Prepare (sys_ctx,
                                    TPM20_INDEX_PASSWORD_TEST,
                                    TPM20_INDEX_PASSWORD_TEST,
                                    &nvWriteData,
                                    0);
    if (rc != TSS2_RC_SUCCESS) {
        LOG_ERROR ("Tss2_Sys_NV_Write_Prepare failed with RC: 0x%x", rc);
        return rc;
    }

    /* Roll nonces for command */
    roll_nonces (nvSession, &nvCmdAuths.auths[0].nonce);

    /*
     * Complete command authorization area, by computing
     * HMAC and setting it in nvCmdAuths.
     */
    rc = compute_command_hmac(sys_ctx,
                              TPM20_INDEX_PASSWORD_TEST,
                              TPM20_INDEX_PASSWORD_TEST,
                              TPM2_RH_NULL,
                              &nvCmdAuths);
    if (rc != TSS2_RC_SUCCESS) {
        LOG_ERROR ("compute_command_hmac failed with RC: 0x%x", rc);
        return rc;
    }

    /*
     * Finally!!  Write the data to the NV index.
     * If the command is successful, the command
     * HMAC was correct.
     */
    rc = TSS2_RETRY_EXP (Tss2_Sys_NV_Write (sys_ctx,
                            TPM20_INDEX_PASSWORD_TEST,
                            TPM20_INDEX_PASSWORD_TEST,
                            &nvCmdAuths,
                            &nvWriteData,
                            0,
                            &nvRspAuths));
    if (rc != TSS2_RC_SUCCESS) {
        LOG_ERROR ("Tss2_Sys_NV_Write failed with RC: 0x%x", rc);
        return rc;
    }


    /* Roll nonces for response */
    roll_nonces (nvSession, &nvRspAuths.auths[0].nonce);

    /*
     * If the command was successful, check the
     * response HMAC to make sure that the
     * response was received correctly.
     */
    rc = check_response_hmac (sys_ctx,
                              &nvCmdAuths,
                              TPM20_INDEX_PASSWORD_TEST,
                              TPM20_INDEX_PASSWORD_TEST,
                              TPM2_RH_NULL,
                              &nvRspAuths);
    if (rc != TSS2_RC_SUCCESS) {
        LOG_ERROR ("check_response_hmac failed with RC: 0x%x", rc);
        return rc;
    }

    if (session_type == TPM2_SE_POLICY) {
        rc = Tss2_Sys_PolicyAuthValue (sys_ctx,
                                       nvSession->sessionHandle,
                                       0,
                                       0);
        if (rc != TSS2_RC_SUCCESS) {
            LOG_ERROR ("Tss2_Sys_PolicyAuthValue failed with RC: 0x%x", rc);
            return rc;
        }
    }
    /* First call prepare in order to create cpBuffer. */
    rc = Tss2_Sys_NV_Read_Prepare (sys_ctx,
                                   TPM20_INDEX_PASSWORD_TEST,
                                   TPM20_INDEX_PASSWORD_TEST,
                                   NV_DATA_SIZE,
                                   0);
    if (rc != TSS2_RC_SUCCESS) {
        LOG_ERROR ("Tss2_Sys_NV_Read_Prepare failed with RC: 0x%x", rc);
        return rc;
    }

    roll_nonces (nvSession, &nvCmdAuths.auths[0].nonce);
    /* End the session after next command. */
    nvCmdAuths.auths[0].sessionAttributes &= ~TPMA_SESSION_CONTINUESESSION;

    /*
     * Complete command authorization area, by computing
     * HMAC and setting it in nvCmdAuths.
     */
    rc = compute_command_hmac (sys_ctx,
                               TPM20_INDEX_PASSWORD_TEST,
                               TPM20_INDEX_PASSWORD_TEST,
                               TPM2_RH_NULL,
                               &nvCmdAuths);
    if (rc != TSS2_RC_SUCCESS) {
        LOG_ERROR ("compute_command_hmac failed with RC: 0x%x", rc);
        return rc;
    }

    /*
     * And now read the data back.
     * If the command is successful, the command
     * HMAC was correct.
     */
    rc = Tss2_Sys_NV_Read (sys_ctx,
                           TPM20_INDEX_PASSWORD_TEST,
                           TPM20_INDEX_PASSWORD_TEST,
                           &nvCmdAuths,
                           NV_DATA_SIZE,
                           0,
                           &nvReadData,
                           &nvRspAuths);
    if (rc != TSS2_RC_SUCCESS) {
        LOG_ERROR ("Tss2_Sys_NV_Read failed with RC: 0x%x", rc);
        return rc;
    }

    /* Roll nonces for response */
    roll_nonces (nvSession, &nvRspAuths.auths[0].nonce);

    /*
     * If the command was successful, check the
     * response HMAC to make sure that the
     * response was received correctly.
     */
    rc = check_response_hmac (sys_ctx,
                              &nvCmdAuths,
                              TPM20_INDEX_PASSWORD_TEST,
                              TPM20_INDEX_PASSWORD_TEST,
                              TPM2_RH_NULL,
                              &nvRspAuths);
    if (rc != TSS2_RC_SUCCESS) {
        LOG_ERROR ("check_response_hmac failed with RC: 0x%x", rc);
        return rc;
    }

    /* Check that write and read data are equal. */
    if (memcmp ((void *)&nvReadData.buffer[0],
                (void *)&nvWriteData.buffer[0],
                nvReadData.size))
    {
        LOG_ERROR ("Data read not equal to data written.");
        return 1;
    }

    /*
     * Now cleanup:  undefine the NV index and delete
     * the NV index's entity table entry.
     */

    /* Undefine the NV index. */
    rc = Tss2_Sys_NV_UndefineSpace (sys_ctx,
                                    TPM2_RH_PLATFORM,
                                    TPM20_INDEX_PASSWORD_TEST,
                                    &auth_cmd_null_pwd,
                                    0);
    if (rc != TSS2_RC_SUCCESS) {
        LOG_ERROR ("Tss2_Sys_NV_UndefineSpace failed with RC: 0x%x", rc);
        return rc;
    }

    /* Delete the NV index's entry in the entity table. */
    DeleteEntity (TPM20_INDEX_PASSWORD_TEST);

    /* Remove the real session from sessions table. */
    end_auth_session (nvSession);
    return rc;
}

int
test_invoke (TSS2_SYS_CONTEXT *sys_ctx)
{
    TSS2_RC rc;
    TPM2B_DIGEST authPolicy = { 0, };
    TPMA_NV nvAttributes;

    LOG_INFO ("HMAC session test");
    nvAttributes = TPMA_NV_AUTHREAD | TPMA_NV_AUTHWRITE | TPMA_NV_PLATFORMCREATE;
    rc = nv_rw_with_session (sys_ctx, &authPolicy, nvAttributes, TPM2_SE_HMAC);
    if (rc != TSS2_RC_SUCCESS)
        return rc;

    LOG_INFO ("Policy session test");
    authPolicy.size = TPM2B_SIZE (authPolicy);
    rc = create_policy (sys_ctx, &authPolicy);
    if (rc != TSS2_RC_SUCCESS)
        return rc;
    nvAttributes = TPMA_NV_POLICYREAD | TPMA_NV_POLICYWRITE | TPMA_NV_PLATFORMCREATE;
    rc = nv_rw_with_session (sys_ctx, &authPolicy, nvAttributes, TPM2_SE_POLICY);
    if (rc != TSS2_RC_SUCCESS)
        return rc;

    return TSS2_RC_SUCCESS;
}
