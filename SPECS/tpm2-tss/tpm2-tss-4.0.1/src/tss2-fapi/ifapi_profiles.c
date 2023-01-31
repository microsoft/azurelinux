/* SPDX-License-Identifier: BSD-2-Clause */
/*******************************************************************************
 * Copyright 2018-2019, Fraunhofer SIT sponsored by Infineon Technologies AG
 * All rights reserved.
 *******************************************************************************/

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <stdint.h>
#include <stdlib.h>
#include <string.h>

#include "tss2_common.h"

#include "ifapi_profiles.h"

#include "tpm_json_deserialize.h"
#include "ifapi_policy_json_deserialize.h"
#include "ifapi_json_deserialize.h"
#include "ifapi_helpers.h"
#define LOGMODULE fapi
#include "util/log.h"
#include "util/aux_util.h"
#include "ifapi_macros.h"

#define PROFILES_EXTENSION ".json"
#define PROFILES_PREFIX "P_"

static TSS2_RC
ifapi_profile_json_deserialize(
    json_object *jso,
    IFAPI_PROFILE *profile);

static TSS2_RC
ifapi_profile_checkpcrs(const TPML_PCR_SELECTION *pcr_profile);

/** Initialize the profiles information in the context in an asynchronous way
 *
 * Load the profile information from disk, fill the dictionary of loaded profiles and fill
 * the default profile information into the context.
 *
 * Call ifapi_profiles_initialize_finish to complete the operation.
 *
 * @param[in,out] profiles The context for the profiles information.
 * @param[in,out] io The input/output context being used for file I/O.
 * @param[in] profilesdir The directory to load profile information from.
 * @param[in] defaultprofile The name of the default profile to use.
 * @retval TSS2_RC_SUCCESS on success.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE if NULL pointers were passed in.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the profilesdir does not exist or is empty.
 * @retval TSS2_FAPI_RC_IO_ERROR if creation of log_dir failed or log_dir is not writable.
 * @retval TSS2_FAPI_RC_MEMORY if memory allocation failed.
 */
TSS2_RC
ifapi_profiles_initialize_async(
    IFAPI_PROFILES *profiles,
    IFAPI_IO *io,
    const char *profilesdir,
    const char *defaultprofile)
{
    TSS2_RC r;
    char *tmp;
    size_t i, j;
    check_not_null(profiles);
    check_not_null(profilesdir);

    memset(profiles, 0, sizeof(*profiles));

    profiles->default_name = strdup(defaultprofile);
    check_oom(profiles->default_name);

    r = ifapi_io_dirfiles(profilesdir, &profiles->filenames, &profiles->num_profiles);
    return_if_error(r, "Reading profiles from profiles dir");

    profiles->profiles = calloc(profiles->num_profiles, sizeof(profiles->profiles[0]));
    check_oom(profiles->profiles);

    /* Clean up list of files to only include those that match our filename pattern
       Expand the filenames with the directory
       Set the names in the dictionary */
    for (i = 0; i < profiles->num_profiles; ) {
        char *ext = strstr(profiles->filenames[i], PROFILES_EXTENSION);
        /* Path the filename with the expected pattern */
        if (ext != NULL && strlen(ext) == strlen(PROFILES_EXTENSION) &&
                strncmp(profiles->filenames[i], PROFILES_PREFIX, strlen(PROFILES_PREFIX)) == 0)
        {
            LOG_TRACE("Using file %s in profiles directory", profiles->filenames[i]);
            /* Add the profile name */
            profiles->profiles[i].name = strndup(profiles->filenames[i],
                                                 ext - profiles->filenames[i]);
            check_oom(profiles->profiles[i].name);
            /* Expand the filename with the directory */
            tmp = profiles->filenames[i];
            r = ifapi_asprintf(&profiles->filenames[i], "%s/%s", profilesdir, tmp);
            return_if_error(r, "Out of memory");

            LOG_TRACE("Added profile-entry %s for file %s based on direntry %s",
                      profiles->profiles[i].name, profiles->filenames[i], tmp);

            /* Cleanup and continue */
            free(tmp);
            i++;
        } else {
            LOG_TRACE("Skipping file %s in profiles directory", profiles->filenames[i]);
            free(profiles->filenames[i]);
            profiles->num_profiles -= 1;
            for (j = i; j < profiles->num_profiles; j++) {
                profiles->filenames[j] = profiles->filenames[j + 1];
            }
        }
    }

    if (profiles->num_profiles == 0) {
        LOG_ERROR("No files found in profile dir %s that match the pattern %s*%s",
                  profilesdir, PROFILES_PREFIX, PROFILES_EXTENSION);
        return TSS2_FAPI_RC_BAD_VALUE;
    }
#ifdef HAVE_REALLOCARRAY
    profiles->profiles = reallocarray(profiles->profiles, profiles->num_profiles,
                                      sizeof(profiles->profiles[0]));
    profiles->filenames = reallocarray(profiles->filenames, profiles->num_profiles,
                                      sizeof(profiles->filenames[0]));
#else /* HAVE_REALLOCARRAY */
    profiles->profiles = realloc(profiles->profiles, profiles->num_profiles *
                                      sizeof(profiles->profiles[0]));
    profiles->filenames = realloc(profiles->filenames, profiles->num_profiles *
                                      sizeof(profiles->filenames[0]));
#endif /* HAVE_REALLOCARRAY */
    /* No need for OOM checks, since num_profiles may only have become smaller */

    r = ifapi_io_read_async(io, profiles->filenames[profiles->profiles_idx]);
    return_if_error2(r, "Reading profile %s", profiles->filenames[profiles->profiles_idx]);

    return TSS2_RC_SUCCESS;
}

/** Initialize the profiles information in the context in an asynchronous way
 *
 * Call after ifapi_profiles_initialize_async to complete the operation.
 *
 * @param[in,out] profiles The context for the profiles information.
 * @param[in,out] io The input/output context being used for file I/O.
 * @retval TSS2_RC_SUCCESS on success.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE if NULL pointers were passed in.
 * @retval TSS2_FAPI_RC_BAD_VALUE if a profile could not be loaded.
 * @retval TSS2_FAPI_RC_IO_ERROR if creation of log_dir failed or log_dir is not writable.
 * @retval TSS2_FAPI_RC_MEMORY if memory allocation failed.
 * @retval TSS2_FAPI_RC_TRY_AGAIN if the I/O operation is not finished yet and this function needs
 *         to be called again.
 */
TSS2_RC
ifapi_profiles_initialize_finish(
    IFAPI_PROFILES *profiles,
    IFAPI_IO *io)
{
    TSS2_RC r;
    uint8_t *buffer;
    size_t i;
    json_object *jso;
    check_not_null(profiles);
    check_not_null(io);

    r = ifapi_io_read_finish(io, &buffer, NULL);
    return_if_error(r, "Reading profile failed");

    jso = ifapi_parse_json((char *) buffer);
    free(buffer);
    if (jso == NULL) {
        LOG_ERROR("Failed to parse profile %s", profiles->filenames[profiles->profiles_idx]);
        r = TSS2_FAPI_RC_BAD_VALUE;
        goto error;
    }

    r = ifapi_profile_json_deserialize(jso,
            &profiles->profiles[profiles->profiles_idx].profile);
    json_object_put(jso);
    goto_if_error2(r, "Parsing profile %s failed", error,
                   profiles->filenames[profiles->profiles_idx]);

    r = ifapi_profile_checkpcrs(&profiles->profiles[profiles->profiles_idx].profile.pcr_selection);
    goto_if_error2(r, "Malformed profile pcr selection for profile %s", error,
                   profiles->filenames[profiles->profiles_idx]);

    profiles->profiles_idx += 1;

    if (profiles->profiles_idx < profiles->num_profiles) {
        r = ifapi_io_read_async(io, profiles->filenames[profiles->profiles_idx]);
        goto_if_error2(r, "Reading profile %s", error,
                       profiles->filenames[profiles->profiles_idx]);

        return TSS2_FAPI_RC_TRY_AGAIN;
    }

    /* Get the data of the default profile into the respective variable */
    for (i = 0; i < profiles->num_profiles; i++) {
        if (strcmp(profiles->default_name, profiles->profiles[i].name) == 0) {
            profiles->default_profile = profiles->profiles[i].profile;
            break;
        }
    }
    if (i == profiles->num_profiles) {
        LOG_ERROR("Default profile %s not in the list of loaded profiles",
                  profiles->default_name);
        r = TSS2_FAPI_RC_BAD_VALUE;
        goto error;
    }

    for (i = 0; i < profiles->num_profiles; i++) {
        free(profiles->filenames[i]);
    }
    SAFE_FREE(profiles->filenames);

    return TSS2_RC_SUCCESS;

 error:
    for (i = 0; i < profiles->num_profiles; i++) {
        SAFE_FREE(profiles->filenames[i]);
    }
    SAFE_FREE(profiles->filenames);
    ifapi_profiles_finalize(profiles);
    return r;
}

/** Return the profile data for a given profile name.
 *
 * Returns a (const, not to be free'd) pointer to the profile data for a requested profile.
 * If a NULL profile is requesten, then the default profile is returned.
 * If a keypath is passed in, then the prefix is analysed. If that keypath starts with a profile
 * then this profile is returned. Otherwise the default profile is returned.
 *
 * @param[in] profiles The profiles context
 * @param[in] name The name of the profile or the keypath
 * @param[out] profile The pointer to the profile data.
 * @retval TSS2_RC_SUCCESS on success.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE if NULL pointers were passed in.
 * @retval TSS2_FAPI_RC_BAD_VALUE if a profile is not found.
 */
TSS2_RC
ifapi_profiles_get(
    const IFAPI_PROFILES *profiles,
    const char *name,
    const IFAPI_PROFILE **profile)
{
    check_not_null(profiles);
    check_not_null(name);
    check_not_null(profile);
    char *split;
    size_t len;

    /* if no name or nor profile prefix is given, use the default profile */
    if (!name || !(strncmp(name, "P_", 2) == 0 || strncmp(name, "/P_", 3) == 0)) {
        *profile = &profiles->default_profile;
        return TSS2_RC_SUCCESS;
    }

    /* Search for path delimiter */
    split = index(name, IFAPI_FILE_DELIM_CHAR);

    /* If the path beging with delimiters, skip over those */
    if (name == split) {
        name += 1;
        split = index(name, IFAPI_FILE_DELIM_CHAR);
    }
    if (split == NULL)
        len = strlen(name);
    else
        len = split - name;

    for (size_t i = 0; i < profiles->num_profiles; i++) {
        if (len == strlen(profiles->profiles[i].name) &&
                strncmp(name, profiles->profiles[i].name, len) == 0) {
            *profile = &profiles->profiles[i].profile;
            return TSS2_RC_SUCCESS;
        }
    }
    LOG_ERROR("Profile %s not in the list of loaded profiles", name);
    return TSS2_FAPI_RC_BAD_VALUE;
}

/** Sanitizes and frees internal data structures of loaded profiles' information.
 *
 * @param[in,out] profiles The context for the profiles information.
 */
void
ifapi_profiles_finalize(
    IFAPI_PROFILES *profiles)
{
    size_t i;
    if (!profiles) {
        LOG_ERROR("Called with bad reference");
        return;
    }

    SAFE_FREE(profiles->default_name);

    for (i = 0; i < profiles->num_profiles; i++) {
        IFAPI_PROFILE_ENTRY * entry = &profiles->profiles[i];
        SAFE_FREE(profiles->profiles[i].name);

        IFAPI_PROFILE * profile = &entry->profile;

        SAFE_FREE(profile->srk_template);
        SAFE_FREE(profile->ek_template);

        SAFE_FREE(profile->srk_description);
        SAFE_FREE(profile->ek_description);

        ifapi_cleanup_policy(profile->eh_policy);
        SAFE_FREE(profile->eh_policy);

        ifapi_cleanup_policy(profile->ek_policy);
        SAFE_FREE(profile->ek_policy);

        ifapi_cleanup_policy(profile->sh_policy);
        SAFE_FREE(profile->sh_policy);
    }
    SAFE_FREE(profiles->profiles);

    memset(profiles, 0, sizeof(*profiles));
}

/** Deserialize a IFAPI_KEY_PROFILE json object.
 *
 * @param[in]  jso the json object to be deserialized.
 * @param[out] out the deserialzed binary object.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the json object can't be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_IO_ERROR if an error occurred while accessing the
 *         object store.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 */
static TSS2_RC
ifapi_profile_json_deserialize(
    json_object *jso,
    IFAPI_PROFILE *out)
{
    json_object *jso2;
    TSS2_RC r;

    const TPMT_SYM_DEF session_symmetric_default = {
        .algorithm = TPM2_ALG_AES,
        .keyBits = {.aes = 128},
        .mode = {.aes = TPM2_ALG_CFB}
    };

    LOG_TRACE("call");
    memset(out, 0, sizeof(IFAPI_PROFILE));
    return_if_null(out, "Bad reference.", TSS2_FAPI_RC_BAD_REFERENCE);

    if (!ifapi_get_sub_object(jso, "type", &jso2)) {
        LOG_ERROR("Field \"type\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPMI_ALG_PUBLIC_deserialize(jso2, &out->type);
    return_if_error(r, "Bad value for field \"type\".");

    if (!ifapi_get_sub_object(jso, "srk_template", &jso2)) {
        LOG_ERROR("Field \"srk_template\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    out->srk_template = strdup(json_object_get_string(jso2));
    return_if_null(out->srk_template, "Out of memory.", TSS2_FAPI_RC_MEMORY);

    if (!ifapi_get_sub_object(jso, "srk_description", &jso2)) {
        out->srk_description = NULL;
    } else {
        out->srk_description = strdup(json_object_get_string(jso2));
        return_if_null(out->srk_description, "Out of memory.", TSS2_FAPI_RC_MEMORY);
    }

    if (!ifapi_get_sub_object(jso, "ek_template", &jso2)) {
        LOG_ERROR("Field \"ek_template\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    out->ek_template = strdup(json_object_get_string(jso2));
    return_if_null(out->ek_template, "Out of memory.", TSS2_FAPI_RC_MEMORY);

    if (!ifapi_get_sub_object(jso, "ek_description", &jso2)) {
        out->ek_description = NULL;
    } else {
        out->ek_description = strdup(json_object_get_string(jso2));
        return_if_null(out->ek_description, "Out of memory.", TSS2_FAPI_RC_MEMORY);
    }

    if (!ifapi_get_sub_object(jso, "ecc_signing_scheme", &jso2)) {
        memset(&out->ecc_signing_scheme, 0, sizeof(TPMT_SIG_SCHEME));
    } else {
        r = ifapi_json_TPMT_SIG_SCHEME_deserialize(jso2, &out->ecc_signing_scheme);
        return_if_error(r, "Bad value for field \"ecc_signing_scheme\".");
    }

    if (!ifapi_get_sub_object(jso, "rsa_signing_scheme", &jso2)) {
        memset(&out->rsa_signing_scheme, 0, sizeof(TPMT_SIG_SCHEME));
    } else {
        r = ifapi_json_TPMT_SIG_SCHEME_deserialize(jso2, &out->rsa_signing_scheme);
        return_if_error(r, "Bad value for field \"rsa_signing_scheme\".");
    }

    if (!ifapi_get_sub_object(jso, "rsa_decrypt_scheme", &jso2)) {
        memset(&out->rsa_decrypt_scheme, 0, sizeof(TPMT_RSA_DECRYPT));
    } else {
        r = ifapi_json_TPMT_RSA_DECRYPT_deserialize(jso2, &out->rsa_decrypt_scheme);
        return_if_error(r, "Bad value for field \"rsa_decrypt_scheme\".");
    }

    if (!ifapi_get_sub_object(jso, "sym_mode", &jso2)) {
        LOG_ERROR("Field \"sym_mode\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPMI_ALG_CIPHER_MODE_deserialize(jso2, &out->sym_mode);
    return_if_error(r, "Bad value for field \"sym_mode\".");

    if (!ifapi_get_sub_object(jso, "sym_parameters", &jso2)) {
        LOG_ERROR("Field \"sym_parameters\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPMT_SYM_DEF_OBJECT_deserialize(jso2, &out->sym_parameters);
    return_if_error(r, "Bad value for field \"sym_parameters\".");

    if (!ifapi_get_sub_object(jso, "sym_block_size", &jso2)) {
        LOG_ERROR("Field \"sym_block_size\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_UINT16_deserialize(jso2, &out->sym_block_size);
    return_if_error(r, "Bad value for field \"sym_block_size\".");

    if (!ifapi_get_sub_object(jso, "pcr_selection", &jso2)) {
        LOG_ERROR("Field \"pcr_selection\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPML_PCR_SELECTION_deserialize(jso2, &out->pcr_selection);
    return_if_error(r, "Bad value for field \"pcr_selection\".");

    if (!ifapi_get_sub_object(jso, "nameAlg", &jso2)) {
        LOG_ERROR("Field \"nameAlg\" not found.");
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    r = ifapi_json_TPMI_ALG_HASH_deserialize(jso2, &out->nameAlg);
    return_if_error(r, "Bad value for field \"nameAlg\".");

    if (out->type == TPM2_ALG_RSA) {
        if (!ifapi_get_sub_object(jso, "exponent", &jso2)) {
            LOG_ERROR("Field \"exponent\" not found.");
            return TSS2_FAPI_RC_BAD_VALUE;
        }
        r = ifapi_json_UINT32_deserialize(jso2, &out->exponent);
        return_if_error(r, "Bad value for field \"exponent\".");
        if (!ifapi_get_sub_object(jso, "keyBits", &jso2)) {
            LOG_ERROR("Field \"keyBits\" not found.");
            return TSS2_FAPI_RC_BAD_VALUE;

        }
        r = ifapi_json_TPMI_RSA_KEY_BITS_deserialize(jso2, &out->keyBits);
        return_if_error(r, "Bad value for field \"keyBits\".");

    } else if (out->type == TPM2_ALG_ECC) {
        if (!ifapi_get_sub_object(jso, "curveID", &jso2)) {
            LOG_ERROR("Field \"curveID\" not found.");
            return TSS2_FAPI_RC_BAD_VALUE;
        }
        r = ifapi_json_TPMI_ECC_CURVE_deserialize(jso2, &out->curveID);
        return_if_error(r, "Bad value for field \"curveID\".");
    }

    if (!ifapi_get_sub_object(jso, "session_symmetric", &jso2)) {
        out->session_symmetric = session_symmetric_default;
    } else {
        r = ifapi_json_TPMT_SYM_DEF_deserialize(jso2, &out->session_symmetric);
        return_if_error(r, "Bad value for field \"session_symmetric\".");
    }

    if (ifapi_get_sub_object(jso, "eh_policy", &jso2)) {
        out->eh_policy = calloc(1, sizeof(TPMS_POLICY));
        goto_if_null2(out->eh_policy, "Out of memory.", r, TSS2_FAPI_RC_MEMORY,
                      cleanup);

        r = ifapi_json_TPMS_POLICY_deserialize(jso2, out->eh_policy);
        goto_if_error(r, "Deserialize policy.", cleanup);
    }

    if (ifapi_get_sub_object(jso, "sh_policy", &jso2)) {
        out->sh_policy = calloc(1, sizeof(TPMS_POLICY));
        goto_if_null2(out->sh_policy, "Out of memory.", r, TSS2_FAPI_RC_MEMORY,
                      cleanup);

        r = ifapi_json_TPMS_POLICY_deserialize(jso2, out->sh_policy);
        goto_if_error(r, "Deserialize policy.", cleanup);
    }

    if (ifapi_get_sub_object(jso, "ek_policy", &jso2)) {
        out->ek_policy = calloc(1, sizeof(TPMS_POLICY));
        goto_if_null2(out->ek_policy, "Out of memory.", r, TSS2_FAPI_RC_MEMORY,
                      cleanup);

        r = ifapi_json_TPMS_POLICY_deserialize(jso2, out->ek_policy);
        goto_if_error(r, "Deserialize policy.", cleanup);
    }

    if (ifapi_get_sub_object(jso, "srk_policy", &jso2)) {
        out->srk_policy = calloc(1, sizeof(TPMS_POLICY));
        goto_if_null2(out->srk_policy, "Out of memory.", r, TSS2_FAPI_RC_MEMORY,
                      cleanup);

        r = ifapi_json_TPMS_POLICY_deserialize(jso2, out->srk_policy);
        goto_if_error(r, "Deserialize policy.", cleanup);
    }

    if (ifapi_get_sub_object(jso, "lockout_policy", &jso2)) {
        out->lockout_policy = calloc(1, sizeof(TPMS_POLICY));
        goto_if_null2(out->lockout_policy, "Out of memory.", r, TSS2_FAPI_RC_MEMORY,
                      cleanup);

        r = ifapi_json_TPMS_POLICY_deserialize(jso2, out->lockout_policy);
        goto_if_error(r, "Deserialize policy.", cleanup);
    }

    if (!ifapi_get_sub_object(jso, "newMaxTries", &jso2)) {
        out->newMaxTries = 5;
    } else {
        r = ifapi_json_UINT32_deserialize(jso2, &out->newMaxTries);
        return_if_error(r, "Bad value for field \"newMaxTries\".");
    }

    if (!ifapi_get_sub_object(jso, "newRecoveryTime", &jso2)) {
        out->newRecoveryTime = 1000;
    } else {
        r = ifapi_json_UINT32_deserialize(jso2, &out->newRecoveryTime);
        return_if_error(r, "Bad value for field \"newRecoveryTime\".");
    }

    if (!ifapi_get_sub_object(jso, "lockoutRecovery", &jso2)) {
        out->lockoutRecovery = 1000;
    } else {
        r = ifapi_json_UINT32_deserialize(jso2, &out->lockoutRecovery);
        return_if_error(r, "Bad value for field \"lockoutRecovery\".");
    }

    if (ifapi_get_sub_object(jso, "ignore_ek_template", &jso2)) {
        r = ifapi_json_TPMI_YES_NO_deserialize(jso2, &out->ignore_ek_template);
        return_if_error(r, "Bad value for field \"ignore_ek_template\".");

    } else {
        out->ignore_ek_template = TPM2_NO;
    }


    LOG_TRACE("true");
    return TSS2_RC_SUCCESS;

cleanup:
    SAFE_FREE(out->eh_policy);
    return r;
}

/**
  * Check whether PCRs with muliple banks are defined in profile.
  *
  * This case is not allowed by FAPI.
  */
static TSS2_RC
ifapi_profile_checkpcrs(const TPML_PCR_SELECTION *pcr_profile)
{
    size_t i, j, byte_idx;

    for (i = 0; i < pcr_profile->count - 1; i++) {
        for (j = i + 1; j <  pcr_profile->count; j++) {
            for (byte_idx = 0; byte_idx < 3; byte_idx++) {
                /* Check whether a PCR register flag does occur in two different banks. */
                if (pcr_profile->pcrSelections[i].pcrSelect[byte_idx] &
                        pcr_profile->pcrSelections[j].pcrSelect[byte_idx]) {
                    return_error2(TSS2_FAPI_RC_BAD_VALUE,
                                  "More than one bank selected for a PCR register.");
                }
            }
        }
    }
    return TSS2_RC_SUCCESS;
}
