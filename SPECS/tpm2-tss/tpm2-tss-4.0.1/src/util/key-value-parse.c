/* SPDX-License-Identifier: BSD-2-Clause */
/*
 * Copyright (c) 2018, Intel Corporation
 * All rights reserved.
 */
#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <inttypes.h>
#include <stdbool.h>
#include <string.h>

#include "tss2_tpm2_types.h"

#include "util/key-value-parse.h"
#define LOGMODULE tcti
#include "util/log.h"

/*
 * Parse the provided string containing a key / value pair separated by the
 * '=' character.
 * NOTE: The 'kv_str' parameter is not 'const' and this function will modify
 * it as part of the parsing process. The key_value structure will be updated
 * with references pointing to the appropriate location in the key_value_str
 * parameter.
 */
bool
parse_key_value (char *key_value_str,
                 key_value_t *key_value)
{
    const char *delim = "=";
    char *tok, *state;

    LOG_TRACE ("key_value_str: \"%s\" and key_value_t: 0x%" PRIxPTR,
               key_value_str, (uintptr_t)key_value);
    if (key_value_str == NULL || key_value == NULL) {
        LOG_WARNING ("received a NULL parameter, all are required");
        return false;
    }
    tok = strtok_r (key_value_str, delim, &state);
    if (tok == NULL) {
        LOG_WARNING ("key / value string is null.");
        return false;
    }
    key_value->key = tok;

    tok = strtok_r (NULL, delim, &state);
    if (tok == NULL) {
        LOG_WARNING ("key / value string is invalid");
        return false;
    }
    key_value->value = tok;

    return true;
}
/*
 * This function parses the provided configuration string extracting the
 * key/value pairs. Each key/value pair extracted is stored in a key_value_t
 * structure and then passed to the provided callback function for processing.
 *
 * NOTE: The 'kv_str' parameter is not 'const' and this function will modify
 * it as part of the parsing process.
 */
TSS2_RC
parse_key_value_string (char *kv_str,
                        KeyValueFunc callback,
                        void *user_data)
{
    const char *delim = ",";
    char *state, *tok;
    key_value_t key_value = KEY_VALUE_INIT;
    TSS2_RC rc = TSS2_RC_SUCCESS;

    LOG_TRACE ("kv_str: \"%s\", callback: 0x%" PRIxPTR ", user_data: 0x%"
               PRIxPTR, kv_str, (uintptr_t)callback,
               (uintptr_t)user_data);
    if (kv_str == NULL || callback == NULL || user_data == NULL) {
        LOG_WARNING ("all parameters are required");
        return TSS2_TCTI_RC_BAD_VALUE;
    }
    for (tok = strtok_r (kv_str, delim, &state);
         tok;
         tok = strtok_r (NULL, delim, &state)) {
        LOG_DEBUG ("parsing key/value: %s", tok);
        if (parse_key_value (tok, &key_value) != true) {
            return TSS2_TCTI_RC_BAD_VALUE;
        }
        rc = callback (&key_value, user_data);
        if (rc != TSS2_RC_SUCCESS) {
            goto out;
        }
    }
out:
    return rc;
}
