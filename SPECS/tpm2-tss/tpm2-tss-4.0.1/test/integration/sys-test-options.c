/* SPDX-License-Identifier: BSD-2-Clause */
/***********************************************************************
 * Copyright (c) 2017-2018, Intel Corporation
 *
 * All rights reserved.
 ***********************************************************************/
#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "test-options.h"

/*
 * A structure to map a string name to an element in the TCTI_TYPE
 * enumeration.
 */
typedef struct {
    char *name;
    TCTI_TYPE type;
} tcti_map_entry_t;
/*
 * A table of tcti_map_entry_t structures. This is how we map a string
 * provided on the command line to the enumeration.
 */
tcti_map_entry_t tcti_map_table[] = {
    {
     .name = "device",
     .type = DEVICE_TCTI,
     },
    {
     .name = "socket",
     .type = SOCKET_TCTI,
     },
    {
     .name = "swtpm",
     .type = SWTPM_TCTI,
     },
    {
     .name = "fuzzing",
     .type = FUZZING_TCTI,
     },
    {
     .name = "unknown",
     .type = UNKNOWN_TCTI,
     },
};

/*
 * Convert from a string to an element in the TCTI_TYPE enumeration.
 * An unknown name / string will map to UNKNOWN_TCTI.
 */
TCTI_TYPE
tcti_type_from_name(char const *tcti_str)
{
    int i;
    for (i = 0; i < N_TCTI; ++i)
        if (strcmp(tcti_str, tcti_map_table[i].name) == 0)
            return tcti_map_table[i].type;
    fprintf(stderr, "Unknown tcti %s.\n", tcti_str);
    return UNKNOWN_TCTI;
}

/*
 * Convert from an element in the TCTI_TYPE enumeration to a string
 * representation.
 */
const char *
tcti_name_from_type(TCTI_TYPE tcti_type)
{
    int i;
    for (i = 0; i < N_TCTI; ++i)
        if (tcti_type == tcti_map_table[i].type)
            return tcti_map_table[i].name;
    return NULL;
}

/*
 * return 0 if sanity test passes
 * return 1 if sanity test fails
 */
int
sanity_check_test_opts(test_opts_t * opts)
{
    switch (opts->tcti_type) {
    case DEVICE_TCTI:
        if (opts->device_file == NULL) {
            fprintf(stderr, "device-path is NULL, check env\n");
            return 1;
        }
        break;
    case SOCKET_TCTI:
        if (opts->socket_address == NULL || opts->socket_port == 0) {
            fprintf(stderr,
                    "socket_address or socket_port is NULL, check env\n");
            return 1;
        }
        break;
    case SWTPM_TCTI:
        if (opts->socket_address == NULL || opts->socket_port == 0) {
            fprintf(stderr,
                    "socket_address or socket_port is NULL, check env\n");
            return 1;
        }
        break;
    case FUZZING_TCTI:
        break;
    default:
        fprintf(stderr, "unknown TCTI type, check env\n");
        return 1;
    }
    return 0;
}

/*
 * Parse command line options from argv extracting test options. These are
 * returned to the caller in the provided options structure.
 */
int
get_test_opts_from_env(test_opts_t * test_opts)
{
    char *env_str, *end_ptr;

    if (test_opts == NULL)
        return 1;
    env_str = getenv(ENV_TCTI_NAME);
    if (env_str != NULL)
        test_opts->tcti_type = tcti_type_from_name(env_str);
    env_str = getenv(ENV_DEVICE_FILE);
    if (env_str != NULL)
        test_opts->device_file = env_str;
    env_str = getenv(ENV_SOCKET_ADDRESS);
    if (env_str != NULL)
        test_opts->socket_address = env_str;
    env_str = getenv(ENV_SOCKET_PORT);
    if (env_str != NULL)
        test_opts->socket_port = strtol(env_str, &end_ptr, 10);
    return 0;
}

/*
 * Dump the contents of the test_opts_t structure to stdout.
 */
void
dump_test_opts(test_opts_t * opts)
{
    printf("test_opts_t:\n");
    printf("  tcti_type:      %s\n", tcti_name_from_type(opts->tcti_type));
    printf("  device_file:    %s\n", opts->device_file);
    printf("  socket_address: %s\n", opts->socket_address);
    printf("  socket_port:    %d\n", opts->socket_port);
}
