/*
 * SPDX-License-Identifier: BSD-2-Clause
 * Copyright (c) 2019, Intel Corporation
 */

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <assert.h>
#include <inttypes.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "tss2_sys.h"

#include "context-util.h"
#include "sys-util.h"
#include "util/aux_util.h"
#define LOGMODULE test
#include "util/log.h"

#define NV_INDEX 0x01800003
#define NV_SIZE 96

#define TPM2B_SIZE_MAX(type) (sizeof (type) - 2)

/*
 * This test creates an NV index governed by a policy and then performs
 * several operations on the NV region to exercise this policy. The NV
 * region created is modeled after the TXT AUX region as defined by the
 * Intel TXT software developers guide:
 * https://www.intel.com/content/dam/www/public/us/en/documents/guides/intel-txt-software-development-guide.pdf
 * Read is controlled by authValue and is unrestricted since authValue is
 * set to emptyBuffer.
 * Write is controlled by policy that allows writes from locality 3 and 4.
 */
/*
 * This function creates a policy session asserting that the locality is
 * either 3 or 4. If this policy is used when executing a command and the
 * policy is not satisfied (locality is not 3 or 4) then the command will
 * fail.
 */
static TSS2_RC
create_policy_session (TSS2_SYS_CONTEXT *sys_ctx,
                       TPMI_SH_AUTH_SESSION *handle)
{
    TPMA_LOCALITY locality = TPMA_LOCALITY_TPM2_LOC_THREE |
        TPMA_LOCALITY_TPM2_LOC_FOUR;
    TPM2B_NONCE nonce = { .size = GetDigestSize (TPM2_ALG_SHA1), };
    TPM2B_NONCE nonce_tpm = { 0, };
    TSS2_RC rc;
    TPM2B_ENCRYPTED_SECRET salt = { 0, };
    TPMT_SYM_DEF symmetric = { .algorithm = TPM2_ALG_NULL, };

    rc = Tss2_Sys_StartAuthSession (sys_ctx,
                                    TPM2_RH_NULL,
                                    TPM2_RH_NULL,
                                    0,
                                    &nonce,
                                    &salt,
                                    TPM2_SE_POLICY,
                                    &symmetric,
                                    TPM2_ALG_SHA1,
                                    handle,
                                    &nonce_tpm,
                                    0);
    return_if_error (rc, "Tss2_Sys_StartAuthSession");

    rc = Tss2_Sys_PolicyLocality (sys_ctx,
                                  *handle,
                                  0,
                                  locality,
                                  0);
    return_if_error (rc, "Tss2_Sys_PolicyLocality");
    return rc;
}
/*
 * This function creates the NV region used in this test. The appropriate
 * attributes are applied using the nvPublic member of the TPM2B_NV_PUBLIC
 * structure.
 */
static TSS2_RC
setup_nv (TSS2_SYS_CONTEXT *sys_ctx)
{
    TSS2_RC rc;
    TPMI_SH_AUTH_SESSION auth_handle = 0;
    TPM2B_DIGEST policy_hash = { 0, };
    TPM2B_AUTH nv_auth = { 0, };
    TSS2L_SYS_AUTH_RESPONSE auth_rsp = { 0, };
    TPM2B_NV_PUBLIC public_info = {
        .nvPublic = {
            .attributes = TPMA_NV_AUTHREAD | TPMA_NV_POLICYWRITE |
                TPMA_NV_PLATFORMCREATE, /* POLICYDELETE? */
            .authPolicy = { .size = GetDigestSize (TPM2_ALG_SHA1), },
            .dataSize = NV_SIZE,
            .nameAlg = TPM2_ALG_SHA1,
            .nvIndex = NV_INDEX,
        },
    };
    const TSS2L_SYS_AUTH_COMMAND auth_cmd = {
        .count = 1,
        .auths= {
            {
                .sessionHandle = TPM2_RH_PW,
            }
        }
    };

    rc = create_policy_session (sys_ctx, &auth_handle);
    return_if_error (rc, "create_policy_session");

    rc = Tss2_Sys_PolicyGetDigest (sys_ctx,
                                   auth_handle,
                                   0,
                                   &policy_hash,
                                   0);
    return_if_error (rc, "Tss2_Sys_PolicyGetDigest");

    LOGBLOB_DEBUG (policy_hash.buffer, policy_hash.size, "policy_hash");
    memcpy (public_info.nvPublic.authPolicy.buffer,
            policy_hash.buffer,
            policy_hash.size);

    rc = Tss2_Sys_NV_DefineSpace (sys_ctx,
                                  TPM2_RH_PLATFORM,
                                  &auth_cmd,
                                  &nv_auth,
                                  &public_info,
                                  &auth_rsp);
    Tss2_Sys_FlushContext (sys_ctx, auth_handle);
    return_if_error (rc, "Tss2_Sys_NV_DefineSpace");

    return rc;
}

static TSS2_RC
teardown_nv (TSS2_SYS_CONTEXT *sys_ctx)
{
    TSS2_RC rc;
    const TSS2L_SYS_AUTH_COMMAND auth_cmd = {
        .count = 1,
        .auths = {
            {
                .sessionHandle = TPM2_RH_PW,
            },
        },
    };
    TSS2L_SYS_AUTH_RESPONSE auth_rsp = { 0, };

    rc = Tss2_Sys_NV_UndefineSpace (sys_ctx,
                                    TPM2_RH_PLATFORM,
                                    NV_INDEX,
                                    &auth_cmd,
                                    &auth_rsp);
    return_if_error (rc, "Tss2_Sys_NV_UndefineSpace");

    return rc;
}

/*
 * This function performs a single write operation to the NV region. This
 * requires we first create a policy session that satisfies the policy
 * governing the region. If the write fails we must manually flush the
 * session since the continueSession flag only guarantees the policy is
 * flushed after successful command execution.
 */
static TSS2_RC
nv_write (TSS2_SYS_CONTEXT *sys_ctx)
{
    TSS2_RC rc;
    TSS2L_SYS_AUTH_COMMAND auth_cmd = {
        .count = 1,
    };
    TSS2L_SYS_AUTH_RESPONSE auth_rsp = { 0, };
    TPM2B_MAX_NV_BUFFER write_data = {
        .size = 4,
        .buffer = { 0xff, 0xfe, 0xfd, 0xfc, },
    };

    rc = create_policy_session (sys_ctx,
                                &auth_cmd.auths[0].sessionHandle);
    return_if_error (rc, "create_policy_session");

    rc = Tss2_Sys_NV_Write (sys_ctx,
                            NV_INDEX,
                            NV_INDEX,
                            &auth_cmd,
                            &write_data,
                            0,
                            &auth_rsp);
    Tss2_Sys_FlushContext (sys_ctx, auth_cmd.auths [0].sessionHandle);
    return_if_error (rc, "Tss2_Sys_NV_Write");

    return rc;
}
/*
 * This function executes a write operation on the NV region from each
 * locality. Per the policy applied to the region @ provisioning, the
 * write command will fail for all localities except 3 and 4.
 */
static TSS2_RC
nv_write_test (TSS2_SYS_CONTEXT *sys_ctx)
{
    TSS2_RC rc;
    uint8_t locality;
    TSS2_TCTI_CONTEXT *tcti_ctx;

    LOG_INFO ("TPM NV write with locality policy test");

    rc = Tss2_Sys_GetTctiContext (sys_ctx, &tcti_ctx);
    return_if_error (rc, "Tss2_Sys_GetTctiContext");

    for (locality = 0; locality < 5; ++locality)
    {
        LOG_INFO ("%s: writing NV from locality %" PRIu8, __func__, locality);
        rc = Tss2_Tcti_SetLocality (tcti_ctx, locality);
        if (rc == TSS2_TCTI_RC_NOT_IMPLEMENTED) {
            return 77;
        }
        return_if_error (rc, "Tss2_Tcti_SetLocality");

        rc = nv_write (sys_ctx);
        switch (locality) {
            case 0:
            case 1:
            case 2:
                if (rc != TPM2_RC_LOCALITY) {
                    LOG_ERROR ("nv_write: Expecting TPM2_RC_LOCALITY, got "
                               "0x%08" PRIu32, rc);
                    return 1;
                }
                break;
            case 3:
            case 4:
                return_if_error (rc, "nv_write");
                break;
            default: /* locality can only be 0-4 */
                assert (false);
                break;
        }
    }
    return TSS2_RC_SUCCESS;
}
/*
 * This function executes a read command on the NV region from each
 * locality providing the required auth value (empty). Per the policy
 * defined a provisioning all should succeed.
 */
static TSS2_RC
nv_read_test (TSS2_SYS_CONTEXT *sys_ctx)
{
    TSS2_RC rc;
    uint8_t locality;
    TPM2B_MAX_NV_BUFFER nv_buf;
    TSS2_TCTI_CONTEXT *tcti_ctx;
    TSS2L_SYS_AUTH_RESPONSE auth_rsp = { 0, };
    const TSS2L_SYS_AUTH_COMMAND auth_cmd = {
        .count = 1,
        .auths = {
            {
                .sessionHandle = TPM2_RH_PW,
            },
        },
    };

    rc = Tss2_Sys_GetTctiContext (sys_ctx, &tcti_ctx);
    return_if_error (rc, "Tss2_Sys_GetTctiContext");

    LOG_INFO ("TPM NV read with auth test");
    for (locality = 0; locality < 5; ++locality)
    {
        rc = Tss2_Tcti_SetLocality (tcti_ctx, locality);
        return_if_error (rc, "Tss2_Tcti_SetLocality");

        nv_buf.size = TPM2B_SIZE_MAX (nv_buf);
        rc = TSS2_RETRY_EXP (Tss2_Sys_NV_Read (sys_ctx,
                                               NV_INDEX,
                                               NV_INDEX,
                                               &auth_cmd,
                                               4,
                                               0,
                                               &nv_buf,
                                               &auth_rsp));
        return_if_error (rc, "Tss2_Sys_NV_Read");
    }

    rc = Tss2_Tcti_SetLocality (tcti_ctx, 3);
    return_if_error (rc, "Tss2_Tcti_SetLocality");

    return rc;
}

int
test_invoke (TSS2_SYS_CONTEXT *sys_ctx)
{
    TSS2_RC rc, rc_teardown;

    rc = setup_nv (sys_ctx);
    return_if_error (rc, "setup_nv");
    rc = nv_write_test (sys_ctx);
    goto_if_error (rc, "nv_write_test", teardown);
    rc = nv_read_test (sys_ctx);
    goto_if_error (rc, "nv_read_test", teardown);
teardown:
    rc_teardown = teardown_nv (sys_ctx);
    return_if_error (rc, "NV policy locality test failed");
    return_if_error (rc_teardown, "teardown_nv");

    return rc;
}
