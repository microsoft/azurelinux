/* SPDX-License-Identifier: BSD-2-Clause */
#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <inttypes.h>

#include "tss2_sys.h"
#include "tss2_mu.h"

#define LOGMODULE test
#include "util/log.h"
#include "test-options.h"
#include "context-util.h"

#define TAB_SIZE(x) (sizeof(x)/sizeof(x[0]))

/* NOTE: CAP_PCRS and CAP_HANDLES->HR_PCR do not change until a reboot is
  triggered. This should be improved if an approach is found. */
struct {
    TPM2_CAP cap;
    UINT32 prop;
    UINT32 count;
} capabilities[] = {
    { TPM2_CAP_PCRS, 0, 10 },
    { TPM2_CAP_HANDLES, TPM2_HR_PCR, TPM2_MAX_CAP_HANDLES },
    { TPM2_CAP_HANDLES, TPM2_HR_HMAC_SESSION, TPM2_MAX_CAP_HANDLES },
    { TPM2_CAP_HANDLES, TPM2_HR_POLICY_SESSION, TPM2_MAX_CAP_HANDLES },
    { TPM2_CAP_HANDLES, TPM2_HR_TRANSIENT, TPM2_MAX_CAP_HANDLES },
    { TPM2_CAP_HANDLES, TPM2_HR_PERSISTENT, TPM2_MAX_CAP_HANDLES },
    { TPM2_CAP_HANDLES, TPM2_HR_NV_INDEX, TPM2_MAX_CAP_HANDLES },
};

int
main (int argc, char *argv[])
{
    TSS2_RC rc;
    TSS2_SYS_CONTEXT *sys_context;
    TSS2L_SYS_AUTH_COMMAND auth_cmd = {
        .auths = {{ .sessionHandle = TPM2_RH_PW }},
        .count = 1
    };
    TPMI_RH_NV_INDEX nvIndex;

    if (argv[1])
        nvIndex = strtol(argv[1], NULL, 16);
    else
        nvIndex = 0x01c00002;

    TPM2B_AUTH nv_auth = { 0 };
    TPM2B_NV_PUBLIC public_info = {
        .nvPublic = {
            .nameAlg = TPM2_ALG_SHA1,
            .attributes = TPMA_NV_PPWRITE | TPMA_NV_AUTHREAD | TPMA_NV_OWNERREAD |
                TPMA_NV_PLATFORMCREATE | TPMA_NV_NO_DA,
            .dataSize = 0,
            .nvIndex = nvIndex,
        },
    };

    TSS2L_SYS_AUTH_RESPONSE auth_rsp = {
        .count = 0
    };
    TPM2B_MAX_NV_BUFFER buf1 = { 0 };
    TPM2B_MAX_NV_BUFFER buf2 = { 0 };

    buf1.size += fread(&buf1.buffer[buf1.size], sizeof(buf1.buffer[0]),
                       sizeof(buf1.buffer) - buf1.size, stdin);
    if (buf1.size >= sizeof(buf1.buffer)) {
        LOG_ERROR("input to large");
        exit(1);
    }

    test_opts_t opts = {
        .tcti_type      = TCTI_DEFAULT,
        .device_file    = DEVICE_PATH_DEFAULT,
        .socket_address = HOSTNAME_DEFAULT,
        .socket_port    = PORT_DEFAULT,
    };

    get_test_opts_from_env (&opts);
    if (sanity_check_test_opts (&opts) != 0)
        exit (1);

    sys_context = sys_init_from_opts (&opts);
    if (sys_context == NULL)
        exit (1);

    /* First make sure that not EK certificate is currently loaded */
    LOG_WARNING("Cert input size is %"PRIu16, buf1.size);
    public_info.nvPublic.dataSize = buf1.size;

    LOG_WARNING("Define NV cert with nv index: %x", public_info.nvPublic.nvIndex);

    rc = Tss2_Sys_NV_DefineSpace(sys_context, TPM2_RH_PLATFORM, &auth_cmd,
                                 &nv_auth, &public_info, &auth_rsp);
    if (rc != TSS2_RC_SUCCESS) {
        LOG_ERROR("TPM NV DefineSpace FAILED: 0x%"PRIx32, rc);
        exit(1);
    }

    /* Split the input buffer into 2 chunks */
    buf2.size = buf1.size;
    buf1.size /= 2;
    buf2.size -= buf1.size;
    memcpy(&buf2.buffer[0], &buf1.buffer[buf1.size], buf2.size);

    rc = Tss2_Sys_NV_Write(sys_context, TPM2_RH_PLATFORM, nvIndex, &auth_cmd,
                           &buf1, 0, &auth_rsp);
    if (rc != TSS2_RC_SUCCESS) {
        LOG_ERROR("TPM NV Write FAILED: 0x%"PRIx32, rc);
        exit(1);
    }

    rc = Tss2_Sys_NV_Write(sys_context, TPM2_RH_PLATFORM, nvIndex, &auth_cmd,
                           &buf2, buf1.size, &auth_rsp);
    if (rc != TSS2_RC_SUCCESS) {
        LOG_ERROR("TPM NV Write FAILED: 0x%"PRIx32, rc);
        exit(1);
    }

    sys_teardown_full (sys_context);

    return 0;
}
