/* SPDX-License-Identifier: BSD-2-Clause */
/*
 * Copyright (c) 2015 - 2018, Intel Corporation
 * All rights reserved.
 */
#ifndef TCTI_SOCKET_H
#define TCTI_SOCKET_H

#include "tss2_tcti.h"

/*
 * Command codes that may be sent to simulator through out of band command
 * channel (aka "the other socket").
 */
#define MS_SIM_POWER_ON         1
#define MS_SIM_POWER_OFF        2
#define MS_SIM_TPM_SEND_COMMAND 8
#define MS_SIM_CANCEL_ON        9
#define MS_SIM_CANCEL_OFF       10
#define MS_SIM_NV_ON            11
#define TPM_SESSION_END         20

#ifdef __cplusplus
extern "C" {
#endif

TSS2_RC tcti_platform_command(
    TSS2_TCTI_CONTEXT *tctiContext,
    UINT32 cmd);

TSS2_RC Tss2_Tcti_Mssim_Init (
    TSS2_TCTI_CONTEXT *tctiContext,
    size_t *size,
    const char *conf);

#ifdef __cplusplus
}
#endif

#endif /* TCTI_SOCKET_H */
