/* SPDX-License-Identifier: BSD-2-Clause */
/*
 * Copyright (c) 2020 Infineon Technologies AG
 * All rights reserved.
 */
#ifndef TCTI_PCAP_BUILDER_H
#define TCTI_PCAP_BUILDER_H

#include <stddef.h>

#define PCAP_DIR_HOST_TO_TPM 0
#define PCAP_DIR_TPM_TO_HOST 1

#define ENV_PCAP_FILE     "TCTI_PCAP_FILE"
#define DEFAULT_PCAP_FILE "tpm2_log.pcap"

typedef struct {
    int fd;
    uint32_t ip_host;
    uint32_t ip_tpm;
    uint32_t tcp_sequence_no_host;
    uint32_t tcp_sequence_no_tpm;
} pcap_buider_ctx;

int
pcap_init (pcap_buider_ctx *ctx);
int
pcap_print (
    pcap_buider_ctx *ctx,
    const void* payload,
    size_t payload_len,
    int direction);
void
pcap_deinit (pcap_buider_ctx *ctx);

#endif /* TCTI_PCAP_BUILDER_H */
