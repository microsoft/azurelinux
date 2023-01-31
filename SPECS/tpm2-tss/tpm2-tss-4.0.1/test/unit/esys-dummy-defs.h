/* SPDX-License-Identifier: BSD-2-Clause */
/*******************************************************************************
 * Copyright 2020, Intel
 * Copyright 2020, Fraunhofer SIT sponsored by Infineon Technologies AG All
 * rights reserved.
 ******************************************************************************/
#ifndef ESYS_DUMMY_DEFS_H
#define ESYS_DUMMY_DEFS_H

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include "tss2_esys.h"
#include "tss2-esys/esys_iutil.h"

/*
 * Esys handles for dummy session and key objects, and initialization values for
 * other objects, which can be used in ESAPI test calls
 */

#define DUMMY_TR_HANDLE_POLICY_SESSION  ESYS_TR_MIN_OBJECT
#define DUMMY_TR_HANDLE_KEY ESYS_TR_MIN_OBJECT+1
#define DUMMY_TR_HANDLE_NV_INDEX ESYS_TR_MIN_OBJECT+2
#define DUMMY_TR_HANDLE_HIERARCHY_OWNER ESYS_TR_MIN_OBJECT+3
#define DUMMY_TR_HANDLE_HIERARCHY_PLATFORM ESYS_TR_MIN_OBJECT+4
#define DUMMY_TR_HANDLE_PRIVACY_ADMIN ESYS_TR_MIN_OBJECT+5
#define DUMMY_TR_HANDLE_HMAC_SESSION  ESYS_TR_MIN_OBJECT+6
#define DUMMY_TR_HANDLE_LOCKOUT ESYS_TR_MIN_OBJECT+7
#define DUMMY_IN_PUBLIC_DATA { \
        .size = 0, \
        .publicArea = { \
            .type = TPM2_ALG_ECC, \
            .nameAlg = TPM2_ALG_SHA256, \
            .objectAttributes = (TPMA_OBJECT_USERWITHAUTH | \
                                 TPMA_OBJECT_RESTRICTED | \
                                 TPMA_OBJECT_SIGN_ENCRYPT | \
                                 TPMA_OBJECT_FIXEDTPM | \
                                 TPMA_OBJECT_FIXEDPARENT | \
                                 TPMA_OBJECT_SENSITIVEDATAORIGIN), \
            .authPolicy = { \
                 .size = 0, \
             }, \
            .parameters.eccDetail = { \
                 .symmetric = { \
                     .algorithm = \
                     TPM2_ALG_AES, \
                     .keyBits.aes = \
                     128, \
                     .mode.aes = \
                     TPM2_ALG_ECB, \
                 }, \
                 .scheme = { \
                      .scheme = \
                      TPM2_ALG_ECDSA, \
                      .details = { \
                          .ecdsa = \
                          {. \
                           hashAlg \
                           = \
                           TPM2_ALG_SHA256}}, \
                  }, \
                 .curveID = TPM2_ECC_NIST_P256, \
                 .kdf = { \
                      .scheme = TPM2_ALG_KDF1_SP800_56A, \
                      .details = {}} \
             }, \
            .unique.ecc = { \
                 .x = {.size = 0,.buffer = {}}, \
                 .y = {.size = 0,.buffer = {}}, \
             }, \
        }, \
    }

#define DUMMY_TPMT_PUBLIC_PARAMS { \
        .type = TPM2_ALG_ECC, \
            .parameters.eccDetail = { \
            .symmetric = { \
                 .algorithm = \
                 TPM2_ALG_AES, \
                 .keyBits.aes = \
                 128, \
                 .mode.aes = \
                 TPM2_ALG_ECB, \
             }, \
            .scheme = { \
                 .scheme = \
                 TPM2_ALG_ECDSA, \
                 .details = { \
                     .ecdsa = \
                     {. \
                      hashAlg \
                      = \
                      TPM2_ALG_SHA256}}, \
             }, \
            .curveID = TPM2_ECC_NIST_P256, \
            .kdf = { \
                 .scheme = TPM2_ALG_KDF1_SP800_56A, \
                 .details = {}} \
        } \
    }

#define DUMMY_2B_DATA(NAME)  { \
        .size = 20, \
        NAME = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, \
                   11, 12, 13, 14, 15, 16, 17, 18, 19, 20} \
    }

#define DUMMY_2B_DATA16(NAME)  { \
        .size = 16, \
        NAME = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, \
                   11, 12, 13, 14, 15, 16 } \
    }

#define DUMMY_2B_DATA0 { \
        .size = 0, \
        .buffer = {}, \
    }

#define DUMMY_SYMMETRIC {.algorithm = TPM2_ALG_AES, \
        .keyBits = {.aes = 128}, \
        .mode = {.aes = TPM2_ALG_CFB} \
    }

#define DUMMY_TPMT_TK_AUTH { .tag = TPM2_ST_AUTH_SIGNED , .hierarchy = TPM2_RH_OWNER, .digest = {0} }

#define DUMMY_TPMT_TK_CREATION { .tag = TPM2_ST_CREATION , .hierarchy = TPM2_RH_OWNER, .digest = {0} }

#define DUMMY_TPMT_TK_VERIFIED { .tag = TPM2_ST_VERIFIED , .hierarchy = TPM2_RH_OWNER, .digest = {0} }

#define DUMMY_TPMT_TK_HASHCHECK { .tag = TPM2_ST_HASHCHECK , .hierarchy = TPM2_RH_OWNER, .digest = {0} }

#define DUMMY_RSA_DECRYPT { .scheme = TPM2_ALG_RSAPSS }

#define DUMMY_TPMT_SIGNATURE { \
        .sigAlg = TPM2_ALG_RSAPSS, \
        .signature = { \
            .rsapss = { \
                 .hash = TPM2_ALG_SHA1, .sig= {0} \
             } \
        } \
    };
#endif
