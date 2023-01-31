/* SPDX-License-Identifier: BSD-2-Clause */
/*******************************************************************************
 * Copyright 2019, Fraunhofer SIT, Infineon Technologies AG, Intel Corporation
 * All rights reserved.
 ******************************************************************************/

#ifndef TCTI_SWTPM_H
#define TCTI_SWTPM_H

#include <limits.h>

#include "tcti-common.h"
#include "util/io.h"

/*
 * longest possible conf string:
 * HOST_NAME_MAX + max char uint16 (5) + strlen ("host=,port=") (11)
 */
#define TCTI_SWTPM_CONF_MAX (_HOST_NAME_MAX + 16)
#define TCTI_SWTPM_DEFAULT_HOST "localhost"
#define TCTI_SWTPM_DEFAULT_PORT 2321
#define TCTI_SWTPM_DEFAULT_PATH NULL
#define SWTPM_CONF_DEFAULT_INIT { \
    .host = TCTI_SWTPM_DEFAULT_HOST, \
    .port = TCTI_SWTPM_DEFAULT_PORT, \
    .path = TCTI_SWTPM_DEFAULT_PATH, \
}

#define TCTI_SWTPM_MAGIC 0x496E66696E656F6EULL

/*
 * Maximum length of control channel requests/responses
 * There are very long ones, but here 64 bytes should suffice
 */
#define SWTPM_CTRL_REQ_MAX_LEN       64
#define SWTPM_CTRL_RESP_MAX_LEN      64

typedef struct {
    char *host;
    uint16_t port;
    /* if path is NULL, we use host/port */
    char *path;
} swtpm_conf_t;

typedef struct {
    TSS2_TCTI_COMMON_CONTEXT common;
    SOCKET ctrl_sock;
    SOCKET tpm_sock;
    char *conf_copy;
    swtpm_conf_t swtpm_conf;
} TSS2_TCTI_SWTPM_CONTEXT;

#endif /* TCTI_SWTPM_H */
