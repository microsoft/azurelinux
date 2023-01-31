/* SPDX-License-Identifier: BSD-2-Clause */
/*
 * Copyright (c) 2018 Intel Corporation
 * All rights reserved.
 */
 /* Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved. */
#ifndef TCTI_TBS_H
#define TCTI_TBS_H

#include "tcti-common.h"

#define TCTI_TBS_MAGIC 0xfbf2afa3761e188aULL

typedef struct {
    TSS2_TCTI_COMMON_CONTEXT common;
    void *hContext;
    PBYTE commandBuffer;
    UINT32 commandSize;
} TSS2_TCTI_TBS_CONTEXT;



#endif /* TCTI_TBS_H */
