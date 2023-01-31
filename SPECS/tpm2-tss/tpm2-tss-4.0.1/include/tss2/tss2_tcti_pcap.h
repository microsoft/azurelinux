/* SPDX-License-Identifier: BSD-2-Clause */
/*
 * Copyright (c) 2020 Infineon Technologies AG
 * All rights reserved.
 */
#ifndef TSS2_TCTI_PCAP_H
#define TSS2_TCTI_PCAP_H

#include "tss2_tcti.h"

#ifdef __cplusplus
extern "C" {
#endif

TSS2_RC Tss2_Tcti_Pcap_Init (
    TSS2_TCTI_CONTEXT *tctiContext,
    size_t *size,
    const char *conf);

#ifdef __cplusplus
}
#endif

#endif /* TSS2_TCTI_PCAP_H */
