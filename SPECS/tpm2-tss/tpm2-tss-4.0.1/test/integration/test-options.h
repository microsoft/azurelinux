/* SPDX-License-Identifier: BSD-2-Clause */
/***********************************************************************
 * Copyright (c) 2017-2018, Intel Corporation
 *
 * All rights reserved.
 ***********************************************************************/
#ifndef TEST_OPTIONS_H
#define TEST_OPTIONS_H

#include <stdint.h>

/* Default TCTI */
#define TCTI_DEFAULT      SOCKET_TCTI
#define TCTI_DEFAULT_STR  "socket"

/* Defaults for Device TCTI */
#define DEVICE_PATH_DEFAULT "/dev/tpm0"

/* Defaults for Socket TCTI connections */
#define HOSTNAME_DEFAULT "127.0.0.1"
#define PORT_DEFAULT     2321

/* environment variables holding TCTI config */
#define ENV_TCTI_NAME      "TPM20TEST_TCTI_NAME"
#define ENV_DEVICE_FILE    "TPM20TEST_DEVICE_FILE"
#define ENV_SOCKET_ADDRESS "TPM20TEST_SOCKET_ADDRESS"
#define ENV_SOCKET_PORT    "TPM20TEST_SOCKET_PORT"

typedef enum {
    UNKNOWN_TCTI,
    DEVICE_TCTI,
    SOCKET_TCTI,
    SWTPM_TCTI,
    FUZZING_TCTI,
    N_TCTI,
} TCTI_TYPE;

typedef struct {
    TCTI_TYPE tcti_type;
    const char *device_file;
    const char *socket_address;
    uint16_t socket_port;
} test_opts_t;

/* functions to get test options from the user and to print helpful stuff */
const char *tcti_name_from_type(TCTI_TYPE tcti_type);
TCTI_TYPE tcti_type_from_name(char const *tcti_str);
int get_test_opts_from_env(test_opts_t * opts);
int sanity_check_test_opts(test_opts_t * opts);
void dump_test_opts(test_opts_t * opts);

#endif                          /* TEST_OPTIONS_H */
