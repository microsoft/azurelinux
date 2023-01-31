/* SPDX-License-Identifier: BSD-2-Clause */
/*
 * Copyright (c) 2020 Infineon Technologies AG
 * All rights reserved.
 */

#ifndef TCTI_PCAP_H
#define TCTI_PCAP_H

#include "tcti-pcap-builder.h"

#include "tss2_tcti.h"
#include "tcti-common.h"

#define TCTI_PCAP_MAGIC 0x9cf45c5d7d9d0d3fULL

typedef struct {
    const char *child_tcti;
} tcti_pcap_conf_t;

typedef struct {
    TSS2_TCTI_COMMON_CONTEXT common;
    pcap_buider_ctx pcap_builder;
    TSS2_TCTI_CONTEXT *tcti_child;
} TSS2_TCTI_PCAP_CONTEXT;

#endif /* TCTI_PCAP_H */
