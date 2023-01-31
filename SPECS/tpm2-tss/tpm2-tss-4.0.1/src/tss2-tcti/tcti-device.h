/* SPDX-License-Identifier: BSD-2-Clause */
/*
 * Copyright (c) 2018 Intel Corporation
 * All rights reserved.
 */
#ifndef TCTI_DEVICE_H
#define TCTI_DEVICE_H

#include "tcti-common.h"

#define TCTI_DEVICE_MAGIC 0x89205e72e319e5bbULL

typedef struct {
    TSS2_TCTI_COMMON_CONTEXT common;
    int fd;
} TSS2_TCTI_DEVICE_CONTEXT;

#endif /* TCTI_DEVICE_H */
