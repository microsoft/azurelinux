/* SPDX-License-Identifier: BSD-2-Clause */
/*******************************************************************************
 * Copyright 2018-2019, Fraunhofer SIT sponsored by Infineon Technologies AG
 * All rights reserved.
 *******************************************************************************/
#ifndef IFAPI_CONFIG_H
#define IFAPI_CONFIG_H

#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include "tss2_tpm2_types.h"
#include "ifapi_io.h"

#define ENV_FAPI_CONFIG "TSS2_FAPICONF"

/**
 * Type for storing FAPI configuration
 */
typedef struct {
    /** Path for profile directory */
    char                *profile_dir;
    /** Directory storing NV objects */
    char                *user_dir;
    /** Directory storing key and NV objects */
    char                *keystore_dir;
    /** Name the used profile */
    char                *profile_name;
    /** The used tcti interface */
    char                *tcti;
    /** The directory for event logs */
    char                *log_dir;
    /** The PCRs used by IMA etc. */
    TPML_PCR_SELECTION   system_pcrs;
    /** Fingerprint of EK */
    TPMT_HA              ek_fingerprint;
    /* URL for EC certificate */
    char                *ek_cert_file;
     /* Switch whether certificate validation will done */
    TPMI_YES_NO         ek_cert_less;
    /** Certificate service for Intel TPMs */
    char                *intel_cert_service;
    /* File with firmware measurements. */
    char                *firmware_log_file;
    /* File with ima measurements. */
    char                *ima_log_file;

} IFAPI_CONFIG;

TSS2_RC
ifapi_config_initialize_async(
    IFAPI_IO            *io
        );

TSS2_RC
ifapi_config_initialize_finish(
    IFAPI_IO            *io,
    IFAPI_CONFIG        *config
    );

#endif /* IFAPI_CONFIG_H */
