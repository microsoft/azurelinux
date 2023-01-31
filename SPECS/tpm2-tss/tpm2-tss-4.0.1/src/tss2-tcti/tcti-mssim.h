/* SPDX-License-Identifier: BSD-2-Clause */
/*
 * Copyright (c) 2018 Intel Corporation
 * All rights reserved.
 */

#ifndef TCTI_MSSIM_H
#define TCTI_MSSIM_H

#include <limits.h>

#include "tcti-common.h"
#include "util/io.h"

/*
 * longest possible conf string:
 * HOST_NAME_MAX + max char uint16 (5) + strlen ("host=,port=") (11)
 */
#define TCTI_MSSIM_CONF_MAX (_HOST_NAME_MAX + 16)
#define TCTI_MSSIM_DEFAULT_HOST "localhost"
#define TCTI_MSSIM_DEFAULT_PORT 2321
#define TCTI_MSSIM_DEFAULT_PATH NULL
#define MSSIM_CONF_DEFAULT_INIT { \
    .host = TCTI_MSSIM_DEFAULT_HOST, \
    .port = TCTI_MSSIM_DEFAULT_PORT, \
    .path = TCTI_MSSIM_DEFAULT_PATH, \
}

#define TCTI_MSSIM_MAGIC 0xf05b04cd9f02728dULL

typedef struct {
    char *host;
    uint16_t port;
    /* if path is NULL, we use host/port */
    char *path;
} mssim_conf_t;

typedef struct {
    TSS2_TCTI_COMMON_CONTEXT common;
    SOCKET platform_sock;
    SOCKET tpm_sock;
/* Flag indicating if a command has been cancelled.
 * This is a temporary flag, which will be changed into
 * a tcti state when support for asynch operation will be added */
    bool cancel;
} TSS2_TCTI_MSSIM_CONTEXT;

#endif /* TCTI_MSSIM_H */
