/*
 * SPDX-License-Identifier: BSD-2-Clause
 * Copyright (c) 2019, Intel Corporation
 */

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <inttypes.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "tss2_sys.h"

#include "context-util.h"
#include "sys-util.h"
#include "session-util.h"
#include "util/aux_util.h"
#define LOGMODULE test
#include "util/log.h"

#define NV_PS_INDEX_SIZE 34
#define INDEX_LCP_OWN 0x01400001
#define INDEX_LCP_SUP 0x01800001

#define TPM2B_SIZE_MAX(type) (sizeof (type) - 2)

const TSS2L_SYS_AUTH_COMMAND auth_cmd_null_pwd = {
    .count = 1,
    .auths = {
        {
            .sessionHandle = TPM2_RH_PW,
        },
    },
};

static TSS2_RC
create_policy_session (
    TSS2_SYS_CONTEXT *sys_ctx,
    TPMI_SH_AUTH_SESSION *handle)
{
    TSS2_RC rc;
    TPM2B_ENCRYPTED_SECRET salt = { 0 };
    TPM2B_NONCE nonce = {
        .size = GetDigestSize (TPM2_ALG_SHA1),
    };
    TPM2B_NONCE nonce_tpm = { 0, };
    TPMT_SYM_DEF symmetric = {
        .algorithm = TPM2_ALG_NULL,
    };

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
    return TSS2_RC_SUCCESS;
}

static TSS2_RC
setup_nv (TSS2_SYS_CONTEXT *sys_ctx,
          TPMI_RH_NV_INDEX index)
{
    TSS2_RC rc;
    TPMI_SH_AUTH_SESSION auth_handle;
    TPM2B_DIGEST  policy_hash = {
        .size = TPM2B_SIZE_MAX (policy_hash),
    };
    TPM2B_AUTH  nv_auth = { 0, };
    TSS2L_SYS_AUTH_RESPONSE auth_rsp;
    TPM2B_NV_PUBLIC public_info = {
        .nvPublic = {
            .nameAlg = TPM2_ALG_SHA1,
            .attributes = TPMA_NV_AUTHREAD | TPMA_NV_AUTHWRITE |
                TPMA_NV_PLATFORMCREATE | TPMA_NV_WRITEDEFINE | TPMA_NV_ORDERLY,
            .dataSize = NV_PS_INDEX_SIZE,
            .nvIndex = index,
        },
    };

    rc = create_policy_session (sys_ctx, &auth_handle);
    return_if_error (rc, "create_policy_session");

    rc = Tss2_Sys_PolicyGetDigest (sys_ctx, auth_handle, 0, &policy_hash, 0);
    return_if_error (rc, "Tss2_Sys_PolicyGetDigest");
    LOGBLOB_INFO (policy_hash.buffer, policy_hash.size, "policy_hash");

    rc = Tss2_Sys_NV_DefineSpace (sys_ctx,
                                  TPM2_RH_PLATFORM,
                                  &auth_cmd_null_pwd,
                                  &nv_auth,
                                  &public_info,
                                  &auth_rsp);
    return_if_error (rc, "Tss2_Sys_NV_DefineSpace");

    rc = Tss2_Sys_FlushContext (sys_ctx, auth_handle);
    return_if_error (rc, "Tss2_Sys_FlushContext");

    return TSS2_RC_SUCCESS;
}

static TSS2_RC
nv_write_read_test (TSS2_SYS_CONTEXT *sys_ctx,
                    TPMI_RH_NV_INDEX index)
{
    TSS2_RC rc;
    TPM2B_MAX_NV_BUFFER write_data = {
        .size = 4,
        .buffer = { 0xde, 0xad, 0xbe, 0xef },
    };
    TPM2B_MAX_NV_BUFFER nv_buf = { 0, };
    TSS2L_SYS_AUTH_RESPONSE auth_resp = { 0, };

    rc = TSS2_RETRY_EXP (Tss2_Sys_NV_Write (sys_ctx,
                                            index,
                                            index,
                                            &auth_cmd_null_pwd,
                                            &write_data,
                                            0,
                                            &auth_resp));
    return_if_error (rc, "Tss2_Sys_NV_Write");

    rc = Tss2_Sys_NV_Read (sys_ctx,
                           index,
                           index,
                           &auth_cmd_null_pwd,
                           4,
                           0,
                           &nv_buf,
                           &auth_resp);
    return_if_error (rc, "Tss2_Sys_NV_Read");

    if (memcmp (nv_buf.buffer, write_data.buffer, write_data.size) != 0) {
        LOG_ERROR ("%s: data read from NV is different from data written",
                   __func__);
        LOGBLOB_DEBUG (write_data.buffer, write_data.size, "write_data");
        LOGBLOB_DEBUG (nv_buf.buffer, nv_buf.size, "nv_buf");
        return 1;
    }

    return TSS2_RC_SUCCESS;
}

static TSS2_RC
teardown_nv (TSS2_SYS_CONTEXT *sys_ctx,
             TPMI_RH_NV_INDEX index)
{
    TSS2_RC rc;
    TSS2L_SYS_AUTH_RESPONSE auth_resp = { 0, };

    rc = Tss2_Sys_NV_UndefineSpace (sys_ctx,
                                    TPM2_RH_PLATFORM,
                                    index,
                                    &auth_cmd_null_pwd,
                                    &auth_resp);
    return_if_error (rc, "Tss2_Sys_NV_UndefineSpace");

    return TSS2_RC_SUCCESS;
}

int
test_invoke (TSS2_SYS_CONTEXT *sys_ctx)
{
    TSS2_RC rc, rc_teardown;

    rc = setup_nv (sys_ctx, INDEX_LCP_OWN);
    return_if_error (rc, "setup_nv for INDEX_LCP_OWN");
    rc = nv_write_read_test (sys_ctx, INDEX_LCP_OWN);
    LOG_ERROR ("nv_write_read_test for INDEX_LCP_OWN");
    rc_teardown = teardown_nv (sys_ctx, INDEX_LCP_OWN);
    return_if_error (rc, "INDEX_LCP_OWN test");
    return_if_error (rc_teardown, "teardown_nv for INDEX_LCP_OWN");

    rc = setup_nv (sys_ctx, INDEX_LCP_SUP);
    return_if_error (rc, "setup_nv for INDEX_LCP_SUP");
    rc = nv_write_read_test (sys_ctx, INDEX_LCP_SUP);
    LOG_ERROR ("nv_write_read_test for INDEX_LCP_SUP");
    rc_teardown = teardown_nv (sys_ctx, INDEX_LCP_SUP);
    return_if_error (rc, "INDEX_LCP_SUP test");
    return_if_error (rc_teardown, "teardown_nv for INDEX_LCP_SUP");

    return 0;
}
