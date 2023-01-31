/* SPDX-License-Identifier: BSD-2-Clause */
/***********************************************************************
 * Copyright (c) 2017-2018, Intel Corporation
 *
 * All rights reserved.
 ***********************************************************************/
#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <inttypes.h>
#include <stdlib.h>
#include <string.h>

#include "tss2_mu.h"
#include "tss2_sys.h"

#define LOGMODULE test
#include "util/log.h"
#include "sys-util.h"

TSS2_RC
test_invoke (TSS2_SYS_CONTEXT *sys_context)
{
    TSS2_RC                 rc              = TSS2_RC_SUCCESS;
    TPM2B_SENSITIVE_CREATE  in_sensitive    = { 0 };
    TPMT_PUBLIC             in_public       = { 0 };
    TPM2B_TEMPLATE          public_template = { 0 };
    TPM2B_PRIVATE           out_private     = { 0 };
    TPM2B_PUBLIC            out_public      = { 0 };
    TPM2B_NAME              name            = TPM2B_NAME_INIT;
    TPM2B_NAME              qualified_name  = TPM2B_NAME_INIT;
    TPM2_HANDLE             object_handle   = 0;
    TSS2L_SYS_AUTH_COMMAND  auth_cmd = {
        .auths = {{ .sessionHandle = TPM2_RH_PW }},
        .count = 1
    };
    TSS2L_SYS_AUTH_RESPONSE auth_rsp = {
        .count = 0
    };

    if (sys_context == NULL)
        return TSS2_RC_LAYER_MASK | TSS2_BASE_RC_BAD_REFERENCE;

    in_public.type = TPM2_ALG_RSA;
    in_public.nameAlg = TPM2_ALG_SHA256;
    in_public.objectAttributes |= TPMA_OBJECT_RESTRICTED;
    in_public.objectAttributes |= TPMA_OBJECT_USERWITHAUTH;
    in_public.objectAttributes |= TPMA_OBJECT_DECRYPT;
    in_public.objectAttributes |= TPMA_OBJECT_FIXEDTPM;
    in_public.objectAttributes |= TPMA_OBJECT_FIXEDPARENT;
    in_public.objectAttributes |= TPMA_OBJECT_SENSITIVEDATAORIGIN;
    in_public.parameters.rsaDetail.symmetric.algorithm = TPM2_ALG_AES;
    in_public.parameters.rsaDetail.symmetric.keyBits.aes = 128;
    in_public.parameters.rsaDetail.symmetric.mode.aes = TPM2_ALG_CFB;
    in_public.parameters.rsaDetail.scheme.scheme = TPM2_ALG_NULL;
    in_public.parameters.rsaDetail.keyBits = 2048;

    uint8_t public_buf[sizeof(in_public)] = {0};
    size_t offset = 0;

    rc = Tss2_MU_TPMT_PUBLIC_Marshal(&in_public, public_buf,
                                     sizeof(in_public), &offset);
    if (rc != TPM2_RC_SUCCESS) {
        LOG_ERROR("Tss2_MU_TPMT_PUBLIC_Marshal FAILED! Response Code: 0x%x", rc);
        exit(1);
    }
    public_template.size = offset;
    memcpy(public_template.buffer, public_buf, offset);
    /* Create an object using CreateLoaded.
     * The result should be that the created object
     * stays in the TPM
     */
    LOG_INFO("Calling CreateLoaded");
    rc = Tss2_Sys_CreateLoaded (sys_context,
                                TPM2_RH_OWNER,
                                &auth_cmd,
                                &in_sensitive,
                                &public_template,
                                &object_handle,
                                &out_private,
                                &out_public,
                                &name,
                                &auth_rsp);
    if (rc == TPM2_RC_SUCCESS) {
        LOG_INFO("success object handle: 0x%x", object_handle);
    } else {
        LOG_ERROR("CreateLoaded FAILED! Response Code : 0x%x", rc);
        exit(1);
    }

    memset(&out_public, '\0', sizeof(out_public));
    memset(&name, '\0', sizeof(name));

    /* Check if the object is really loaded by accessing its
     * public area */
    LOG_INFO("Calling ReadPublic");
    rc = Tss2_Sys_ReadPublic (sys_context,
                              object_handle,
                              NULL,
                              &out_public,
                              &name,
                              &qualified_name,
                              NULL);
    if (rc == TPM2_RC_SUCCESS) {
        LOG_INFO("success! Object's qualified name is:");
        LOGBLOB_INFO(qualified_name.name, qualified_name.size, "%s", "name:");
    } else {
        LOG_ERROR("Tss2_Sys_ReadPublic FAILED! Response Code : 0x%x", rc);
        exit(1);
    }

    rc = Tss2_Sys_FlushContext (sys_context, object_handle);
    if (rc != TSS2_RC_SUCCESS) {
        LOG_ERROR("Tss2_Sys_FlushContext failed: 0x%" PRIx32, rc);
        exit(1);
    }

    return rc;
}
