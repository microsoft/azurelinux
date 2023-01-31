/* SPDX-License-Identifier: BSD-2-Clause */
#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <stdbool.h>
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

    for (size_t i = 0; i < TAB_SIZE(capabilities); i++) {
        TPMS_CAPABILITY_DATA caps;
        uint8_t buffer[sizeof(caps)];
        size_t off = 0;

        rc = Tss2_Sys_GetCapability(sys_context, NULL, capabilities[i].cap,
                                    capabilities[i].prop,
                                    capabilities[i].count, NULL,
                                    &caps, NULL);
        if (rc != TSS2_RC_SUCCESS) {
            LOG_ERROR("TPM GetCapabilities FAILED: 0x%"PRIx32, rc);
            exit(1);
        }

        rc = Tss2_MU_TPMS_CAPABILITY_DATA_Marshal(&caps, &buffer[off],
                                                  sizeof(buffer) - off - 1,
                                                  &off);
        if (rc != TSS2_RC_SUCCESS) {
            LOG_ERROR("Marshaling FAILED: 0x%"PRIx32, rc);
            exit(1);
        }

        buffer[off++] = '\0';

        printf("cap%zi: ", i);
        for (size_t j = 0; j < off; j++)
            printf("%02"PRIx8, buffer[j]);
        printf("\n");
    }

    sys_teardown_full (sys_context);

    return 0;
}
