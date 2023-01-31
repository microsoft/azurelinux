/* SPDX-License-Identifier: BSD-2-Clause */
/*
 * Copyright (c) 2015 - 2018, Intel Corporation
 * All rights reserved.
 */
#ifndef TSS2_TCTI_DEVICE_H
#define TSS2_TCTI_DEVICE_H

#include "tss2_tcti.h"

#ifdef __cplusplus
extern "C" {
#endif

TSS2_RC Tss2_Tcti_Device_Init (
    TSS2_TCTI_CONTEXT *tctiContext,
    size_t *size,
    const char *conf);

#ifdef __cplusplus
}
#endif

#endif /* TSS2_TCTI_DEVICE_H */
