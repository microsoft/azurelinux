/* SPDX-License-Identifier: BSD-2-Clause */
#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <stdbool.h>
#include <stdlib.h>
#include <inttypes.h>

#include "tss2_sys.h"

#define LOGMODULE test
#include "util/log.h"
#include "test-options.h"
#include "context-util.h"

#define TAB_SIZE(x) (sizeof(x)/sizeof(x[0]))

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

    TPMS_CAPABILITY_DATA caps;

    rc = Tss2_Sys_GetCapability(sys_context, NULL, TPM2_CAP_HANDLES,
                                TPM2_HR_TRANSIENT,
                                TAB_SIZE(caps.data.handles.handle), NULL,
                                &caps, NULL);
    if (rc != TSS2_RC_SUCCESS) {
        LOG_ERROR("TPM GetCapabilities FAILED! Response Code : 0x%"PRIx32, rc);
        exit(1);
    }


    sys_teardown_full (sys_context);

    if (caps.data.handles.count) {
        LOG_ERROR("TPM contains transient entries");
        for (UINT32 i = 0; i < caps.data.handles.count; i++)
            LOG_ERROR("Handle %"PRIx32, caps.data.handles.handle[i]);
        return 1;
    }

    return 0;
}
