/* SPDX-License-Identifier: BSD-2-Clause */
/*******************************************************************************
 * Copyright 2018-2019, Fraunhofer SIT sponsored by Infineon Technologies AG
 * All rights reserved.
 ******************************************************************************/

#ifndef IFAPI_PROFILES_H
#define IFAPI_PROFILES_H

#include "ifapi_io.h"
#include "ifapi_policy_types.h"

/** Internal structure for FAPI profiles
 */
typedef struct IFAPI_PROFILE {
    TPMI_ALG_PUBLIC                                type;    /**< The algorithm used for key creation */
    char                                  *srk_template;    /**< SRK template */
    char                                   *ek_template;    /**< EK template */
    char                               *srk_description;    /**< SRK description */
    char                                *ek_description;    /**< EK description */
    TPMT_SIG_SCHEME                  ecc_signing_scheme;    /**< Signing scheme for the ECC key. */
    TPMT_SIG_SCHEME                  rsa_signing_scheme;    /**< Signing scheme for the RSA key. */
    TPMT_RSA_DECRYPT                 rsa_decrypt_scheme;    /**< Decrypt scheme for the RSA key. */
    TPMI_ALG_CIPHER_MODE                       sym_mode;    /**< Mode for symmectric encryption. */
    TPMT_SYM_DEF_OBJECT                  sym_parameters;    /**< Parameters for symmectric encryption. */
    UINT16                               sym_block_size;    /**< Block size for symmectric encryption. */
    TPML_PCR_SELECTION                    pcr_selection;    /**< Parameters for symmectric encryption. */
    TPMI_ALG_HASH                               nameAlg;
    TPMI_RSA_KEY_BITS                           keyBits;
    UINT32                                     exponent;
    TPMI_ECC_CURVE                              curveID;
    TPMT_SYM_DEF                      session_symmetric;
    TPMS_POLICY                              *eh_policy;
    TPMS_POLICY                              *sh_policy;
    TPMS_POLICY                              *ek_policy;
    TPMS_POLICY                             *srk_policy;
    TPMS_POLICY                         *lockout_policy;
    UINT32                                  newMaxTries;
    UINT32                              newRecoveryTime;
    UINT32                              lockoutRecovery;
    TPMI_YES_NO                      ignore_ek_template;
} IFAPI_PROFILE;

/* An entry for the dictionary of loaded profiles */
typedef struct IFAPI_PROFILE_ENTRY {
    /** Name of a profile */
    char *name;
    /** Values for a profile */
    struct IFAPI_PROFILE profile;
} IFAPI_PROFILE_ENTRY;

typedef struct IFAPI_PROFILES {
    char *default_name;
    struct IFAPI_PROFILE default_profile;
    /* Dictionary of loaded profiles */
    struct IFAPI_PROFILE_ENTRY *profiles;
    char **filenames;
    /* Size of the loaded profiles dictionary */
    size_t num_profiles;
    size_t profiles_idx;
} IFAPI_PROFILES;

TSS2_RC
ifapi_profiles_initialize_async(
    IFAPI_PROFILES *profiles,
    IFAPI_IO *io,
    const char *profilesdir,
    const char *defaultprofile);

TSS2_RC
ifapi_profiles_initialize_finish(
    IFAPI_PROFILES *profiles,
    IFAPI_IO *io);

TSS2_RC
ifapi_profiles_get(
    const IFAPI_PROFILES *profiles,
    const char *name,
    const IFAPI_PROFILE **profile);

void
ifapi_profiles_finalize(
    IFAPI_PROFILES *profiles);

#endif /* IFAPI_OBJECT_H */
