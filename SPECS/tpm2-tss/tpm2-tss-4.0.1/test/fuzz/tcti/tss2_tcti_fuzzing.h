/* SPDX-License-Identifier: BSD-2-Clause */
/*
 * Copyright (c) 2018, Intel Corporation
 * All rights reserved.
 */
#ifndef TSS2_TCTI_FUZZING_H
#define TSS2_TCTI_FUZZING_H

#include "tss2_tcti.h"

#ifdef __cplusplus
extern "C" {
#endif

TSS2_RC Tss2_Tcti_Fuzzing_Init (
    TSS2_TCTI_CONTEXT *tcti_ctx,
    size_t *size,
    const char *conf);

#ifdef __cplusplus
}
#endif

#endif /* TSS2_TCTI_FUZZING_H */
