/* SPDX-License-Identifier: BSD-2-Clause */
/*******************************************************************************
 * Copyright 2018-2019, Fraunhofer SIT sponsored by Infineon Technologies AG
 * All rights reserved.
 *******************************************************************************/

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <json-c/json.h>
#include <json-c/json_util.h>

#include "util/aux_util.h"
#include "ifapi_config.h"
#include "ifapi_json_deserialize.h"
#include "tpm_json_deserialize.h"
#include "ifapi_json_serialize.h"
#include "tpm_json_serialize.h"
#include "ifapi_helpers.h"

#define LOGMODULE fapi
#include "util/log.h"

/**
 * The path of the default config file
 */
#define DEFAULT_CONFIG_FILE (SYSCONFDIR "/tpm2-tss/fapi-config.json")

/** Deserializes a configuration JSON object.
 *
 * @param[in]  jso The JSON object to be deserialized
 * @param[out] out The deserialized configuration object
 *
 * @retval TSS2_RC_SUCCESS on success
 * @retval TSS2_FAPI_RC_BAD_REFERENCE if jso or out is NULL
 * @retval TSS2_FAPI_RC_BAD_VALUE if the JSON object cannot be deserialized
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 */
static TSS2_RC
ifapi_json_IFAPI_CONFIG_deserialize(json_object *jso, IFAPI_CONFIG *out)
{
    /* Check for NULL parameters */
    return_if_null(out, "out is NULL", TSS2_FAPI_RC_BAD_REFERENCE);
    return_if_null(jso, "jso is NULL", TSS2_FAPI_RC_BAD_REFERENCE);

    memset(out, 0, sizeof(IFAPI_CONFIG));

    /* Deserialize the JSON object) */
    json_object *jso2;
    TSS2_RC r;
    LOG_TRACE("call");

    if (ifapi_get_sub_object(jso, "profile_dir", &jso2)) {
        r = ifapi_json_char_deserialize(jso2, &out->profile_dir);
        return_if_error(r, "Bad value for field \"profile_dir\".");
    }

    if (ifapi_get_sub_object(jso, "user_dir", &jso2)) {
        r = ifapi_json_char_deserialize(jso2, &out->user_dir);
        return_if_error(r, "Bad value for field \"user_dir\".");
    }

    if (ifapi_get_sub_object(jso, "system_dir", &jso2)) {
        r = ifapi_json_char_deserialize(jso2, &out->keystore_dir);
        return_if_error(r, "Bad value for field \"keystore_dir\".");
    }

    if (!ifapi_get_sub_object(jso, "log_dir", &jso2)) {
        out->log_dir = strdup(DEFAULT_LOG_DIR);
        return_if_null(jso, "Out of memory.", TSS2_FAPI_RC_MEMORY);
    } else {
        r = ifapi_json_char_deserialize(jso2, &out->log_dir);
        return_if_error(r, "Bad value for field \"log_dir\".");
    }

    if (!ifapi_get_sub_object(jso, "profile_name", &jso2)) {
        LOG_ERROR("Field \"profile_name\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_char_deserialize(jso2, &out->profile_name);
    return_if_error(r, "Bad value for field \"profile_name\".");
    if (!ifapi_get_sub_object(jso, "tcti", &jso2)) {
        LOG_ERROR("Field \"tcti\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_char_deserialize(jso2, &out->tcti);
    return_if_error(r, "Bad value for field \"tcti\".");

    if (!ifapi_get_sub_object(jso, "system_pcrs", &jso2)) {
        LOG_ERROR("Field \"system_pcrs\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPML_PCR_SELECTION_deserialize(jso2, &out->system_pcrs);
    return_if_error(r, "Bad value for field \"system_pcrs\".");

    if (ifapi_get_sub_object(jso, "ek_cert_file", &jso2)) {
        r = ifapi_json_char_deserialize(jso2, &out->ek_cert_file);
        return_if_error(r, "Bad value for field \"ek_cert_file\".");
    }

    if (ifapi_get_sub_object(jso, "ek_cert_less", &jso2)) {
        r = ifapi_json_TPMI_YES_NO_deserialize(jso2, &out->ek_cert_less);
        return_if_error(r, "Bad value for field \"ek_cert_less\".");

    } else {
        out->ek_cert_less = TPM2_NO;
    }

    if (ifapi_get_sub_object(jso, "ek_fingerprint", &jso2)) {
        r = ifapi_json_TPMT_HA_deserialize(jso2, &out->ek_fingerprint);
        return_if_error(r, "Bad value for field \"ek_fingerprint\".");
    } else {
        out->ek_fingerprint.hashAlg = 0;
    }

    if (ifapi_get_sub_object(jso, "intel_cert_service", &jso2)) {
        r = ifapi_json_char_deserialize(jso2, &out->intel_cert_service);
        return_if_error(r, "Bad value for field \"intel_cert_service\".");
    }

    if (!ifapi_get_sub_object(jso, "firmware_log_file", &jso2)) {
        out->firmware_log_file = NULL;
    } else {
        r = ifapi_json_char_deserialize(jso2, &out->firmware_log_file);
        return_if_error(r, "BAD VALUE");
    }

    if (!ifapi_get_sub_object(jso, "ima_log_file", &jso2)) {
        out->ima_log_file = NULL;
    } else {
        r = ifapi_json_char_deserialize(jso2, &out->ima_log_file);
        return_if_error(r, "BAD VALUE");
    }

    LOG_TRACE("true");
    return TSS2_RC_SUCCESS;
}

/**
 * Starts the initialization of the FAPI configuration.
 *
 * @param[in] io An IO object for file system access
 *
 * @retval TSS2_RC_SUCCESS on success
 * @retval TSS2_FAPI_RC_BAD_REFERENCE if io is NULL
 * @retval TSS2_FAPI_RC_IO_ERROR if an error occurred while accessing the
 *         object store.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 */
TSS2_RC
ifapi_config_initialize_async(IFAPI_IO *io)
{
    /* Check for NULL parameters */
    return_if_null(io, "io is NULL", TSS2_FAPI_RC_BAD_REFERENCE);

    /* Determine the location of the configuration file */
    const char *configFile = getenv(ENV_FAPI_CONFIG);
    if (!configFile) {
        /* No config file given, falling back to the default */
        configFile = DEFAULT_CONFIG_FILE;
    }

    /* Start reading the config file */
    TSS2_RC r = ifapi_io_read_async(io, configFile);
    return_if_error(r, "Could not read config file ");
    return TSS2_RC_SUCCESS;
}

/**
 * Expand user symbol in path.
 *
 * "~" and "$HOME" will be replaces by the value of the HOME environment
 * variable.
 *
 * @param[in, out] The path.
 * @retval TSS2_RC_SUCCESS on success
 * @retval TSS2_FAPI_RC_BAD_VALUE if path is NULL.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 * @retval TSS2_FAPI_RC_BAD_PATH if the home directory can't be determined.
 */

static TSS2_RC
expand_home(char **path) {
    size_t startPos = 0;
    TSS2_RC r;

    return_if_null(path, "Null passed for path", TSS2_FAPI_RC_BAD_VALUE);

    /* Check whether usage of home directory in pathname */
    if (strncmp("~", *path, 1) == 0) {
        startPos = 1;
    } else if (strncmp("$HOME", *path, 5) == 0) {
        startPos = 5;
    }

    /* Replace home abbreviation in path. */
    char *newPath = NULL;
    if (startPos != 0) {
        LOG_DEBUG("Expanding path %s to user's home", *path);
        char *homeDir = getenv("HOME");
        return_if_null(homeDir, "Home directory can't be determined.",
                       TSS2_FAPI_RC_BAD_PATH);
        if (strncmp(&(*path)[startPos], IFAPI_FILE_DELIM, strlen(IFAPI_FILE_DELIM)) == 0) {
            startPos += strlen(IFAPI_FILE_DELIM);
        }
        r = ifapi_asprintf(&newPath, "%s%s%s", homeDir, IFAPI_FILE_DELIM,
                           &(*path)[startPos]);
        return_if_error(r, "Out of memory.");

        SAFE_FREE(*path);
        *path = newPath;
    }
    return TSS2_RC_SUCCESS;
}

/**
 * Finishes the initialization of the FAPI configuration.
 * @param[in]  io An IO object for file system access
 * @param[out] config The configuration that is initialized
 *
 * @retval TSS2_RC_SUCCESS on success
 * @retval TSS2_FAPI_RC_BAD_REFERENCE if config or io is NULL
 * @retval TSS2_FAPI_RC_BAD_VALUE if the read configuration file does not hold
 *         a valid configuration
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE if JSON parsing fails
 * @retval TSS2_FAPI_RC_BAD_PATH if the configuration path is invalid
 * @retval TSS2_FAPI_RC_TRY_AGAIN if an I/O operation is not finished yet and
 *         this function needs to be called again.
 * @retval TSS2_FAPI_RC_IO_ERROR if an error occurred while accessing the
 *         object store.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 */
TSS2_RC
ifapi_config_initialize_finish(IFAPI_IO *io, IFAPI_CONFIG *config)
{
    /* Check for NULL parameters */
    return_if_null(config, "config is NULL", TSS2_FAPI_RC_BAD_REFERENCE);
    return_if_null(io, "io is NULL", TSS2_FAPI_RC_BAD_REFERENCE);

    /* Definitions that must be listed here for the cleanup to work */
    json_object *jso = NULL;

    /* Finish reading operation */
    uint8_t *configFileContent = NULL;
    size_t configFileContentSize = 0;
    TSS2_RC r = ifapi_io_read_finish(io, &configFileContent, &configFileContentSize);
    return_try_again(r);
    goto_if_error(r, "Could not finish read operation", error);
    if (configFileContent == NULL || configFileContentSize == 0) {
        LOG_ERROR("Config file is empty");
        r = TSS2_FAPI_RC_BAD_VALUE;
        goto error;
    }

    /* Parse and deserialize the configuration file */
    jso = ifapi_parse_json((char *)configFileContent);
    goto_if_null(jso, "Could not parse JSON objects",
            TSS2_FAPI_RC_GENERAL_FAILURE, error);
    r = ifapi_json_IFAPI_CONFIG_deserialize(jso, config);
    goto_if_error(r, "Could not deserialize configuration", error);

    /* Check, if the values of the configuration are valid */
    goto_if_null(config->profile_dir, "No profile directory defined in config file",
                 TSS2_FAPI_RC_BAD_VALUE, error);
    goto_if_null(config->user_dir, "No user directory defined in config file",
                 TSS2_FAPI_RC_BAD_VALUE, error);
    goto_if_null(config->keystore_dir, "No system directory defined in config file",
                 TSS2_FAPI_RC_BAD_VALUE, error);
    goto_if_null(config->profile_name, "No default profile defined in config file.",
                 TSS2_FAPI_RC_BAD_VALUE, error);

    /* Check whether usage of home directory is provided in config file */
    r = expand_home(&config->user_dir);
    goto_if_error(r, "Expand home directory.", error);

    r = expand_home(&config->keystore_dir);
    goto_if_error(r, "Expand home directory.", error);

    r = expand_home(&config->log_dir);
    goto_if_error(r, "Expand home directory.", error);

    r = expand_home(&config->profile_dir);
    goto_if_error(r, "Expand home directory.", error);

    /* Log the contents of the configuration */
    LOG_DEBUG("Configuration profile directory: %s", config->profile_dir);
    LOG_DEBUG("Configuration user directory: %s", config->user_dir);
    LOG_DEBUG("Configuration key storage directory: %s", config->keystore_dir);
    LOG_DEBUG("Configuration profile name: %s", config->profile_name);
    LOG_DEBUG("Configuration TCTI: %s", config->tcti);
    LOG_DEBUG("Configuration log directory: %s", config->log_dir);

    SAFE_FREE(configFileContent);
    if (jso != NULL) {
        json_object_put(jso);
    }
    return r;

 error:
    SAFE_FREE(config->profile_dir);
    SAFE_FREE(config->user_dir);
    SAFE_FREE(config->keystore_dir);
    SAFE_FREE(config->profile_name);
    SAFE_FREE(config->tcti);
    SAFE_FREE(config->log_dir);
    SAFE_FREE(config->ek_cert_file);
    SAFE_FREE(config->intel_cert_service);
    SAFE_FREE(configFileContent);
    if (jso != NULL) {
        json_object_put(jso);
    }
    return r;
}
