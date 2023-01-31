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
#include <string.h>

#include "tss2_sys.h"

#define LOGMODULE test
#include "util/log.h"
#include "test.h"
#include "sys-util.h"
#define PCR_8   8
/**
 * This program contains integration test for SYS Tss2_Sys_PCR_Read
 * and Tss2_Sys_PCR_Extend. This is an use case scenario on PCR extend.
 * First, we will get the list of PCR available through getcapability
 * SYS. Then, PCR_Read SYS is called to list out the PCR value and
 * PCR_Extend SYS is called next to update the PCR value. Last,
 * PCR_Read SYS is called again to check the PCR values are changed.
 */
int
test_invoke (TSS2_SYS_CONTEXT *sys_context)
{
    TSS2_RC rc;
    TPMI_YES_NO more_data;
    TPMS_CAPABILITY_DATA capability_data;
    UINT16 i, digest_size;
    TPML_PCR_SELECTION  pcr_selection;
    UINT32 pcr_update_counter_before_extend;
    UINT32 pcr_update_counter_after_extend;
    UINT8 pcr_before_extend[20];
    UINT8 pcr_after_extend[20];
    TPML_DIGEST pcr_values;
    TPML_DIGEST_VALUES digests;
    TPML_PCR_SELECTION pcr_selection_out;

    TSS2L_SYS_AUTH_COMMAND sessions_data = {
        .count = 1,
        .auths = {{.sessionHandle = TPM2_RH_PW,
            .sessionAttributes = 0,
            .nonce={.size=0},
            .hmac={.size=0}}}};

    LOG_INFO("PCR Extension tests started.");
    rc = Tss2_Sys_GetCapability(sys_context, 0, TPM2_CAP_PCR_PROPERTIES, TPM2_PT_PCR_COUNT, 1, &more_data, &capability_data, 0);
    if (rc != TSS2_RC_SUCCESS) {
        LOG_ERROR("GetCapability FAILED! Response Code : 0x%x", rc);
        exit(1);
    }
    digests.count = 1;
    digests.digests[0].hashAlg = TPM2_ALG_SHA1;
    digest_size = GetDigestSize( digests.digests[0].hashAlg );

    for( i = 0; i < digest_size; i++ )
    {
        digests.digests[0].digest.sha1[i] = (UINT8)(i % 256);
    }
    pcr_selection.count = 1;
    pcr_selection.pcrSelections[0].hash = TPM2_ALG_SHA1;
    pcr_selection.pcrSelections[0].sizeofSelect = 3;
    pcr_selection.pcrSelections[0].pcrSelect[0] = 0;
    pcr_selection.pcrSelections[0].pcrSelect[1] = 0;
    pcr_selection.pcrSelections[0].pcrSelect[2] = 0;
    pcr_selection.pcrSelections[0].pcrSelect[PCR_8 / 8] = 1 << (PCR_8 % 8);

    rc = Tss2_Sys_PCR_Read(sys_context, 0, &pcr_selection, &pcr_update_counter_before_extend, &pcr_selection_out, &pcr_values, 0);
    if (rc != TSS2_RC_SUCCESS) {
        LOG_ERROR("PCR_Read FAILED! Response Code : 0x%x", rc);
        exit(1);
    }
    memcpy(&(pcr_before_extend[0]), &(pcr_values.digests[0].buffer[0]), pcr_values.digests[0].size);

    rc = Tss2_Sys_PCR_Extend(sys_context, PCR_8, &sessions_data, &digests, 0);
    if (rc != TSS2_RC_SUCCESS) {
        LOG_ERROR("PCR_Extend FAILED! Response Code : 0x%x", rc);
        exit(1);
    }
    rc = Tss2_Sys_PCR_Read(sys_context, 0, &pcr_selection, &pcr_update_counter_after_extend, &pcr_selection_out, &pcr_values, 0);
    if (rc != TSS2_RC_SUCCESS) {
        LOG_ERROR("PCR_Read FAILED! Response Code : 0x%x", rc);
        exit(1);
    }
    memcpy(&(pcr_after_extend[0]), &(pcr_values.digests[0].buffer[0]), pcr_values.digests[0].size);

    if(pcr_update_counter_before_extend == pcr_update_counter_after_extend) {
        LOG_ERROR("ERROR!! pcr_update_counter didn't change value");
        exit(1);
    }
    if(memcmp(&(pcr_before_extend[0]), &(pcr_after_extend[0]), 20) == 0) {
        LOG_ERROR("ERROR!! PCR didn't change value");
        exit(1);
    }
    LOG_INFO("PCR Extension Test Passed!");
    return 0;
}
