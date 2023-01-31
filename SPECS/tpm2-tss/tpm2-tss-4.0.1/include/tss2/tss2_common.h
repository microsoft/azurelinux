/* SPDX-License-Identifier: BSD-2-Clause */
/***********************************************************************;
 * Copyright (c) 2015-2018, Intel Corporation
 *
 * Copyright 2015, Andreas Fuchs @ Fraunhofer SIT
 *
 * All rights reserved.
 ***********************************************************************/

#ifndef TSS2_COMMON_H
#define TSS2_COMMON_H
#define TSS2_API_VERSION_1_2_1_108

#include <stdint.h>
/*
 * Type definitions
 */
typedef uint8_t     UINT8;
typedef uint8_t     BYTE;
typedef int8_t      INT8;
typedef int         BOOL;
typedef uint16_t    UINT16;
typedef int16_t     INT16;
typedef uint32_t    UINT32;
typedef int32_t     INT32;
typedef uint64_t    UINT64;
typedef int64_t     INT64;

/*
 * ABI runtime negotiation definitions
 */
typedef struct TSS2_ABI_VERSION TSS2_ABI_VERSION;
struct TSS2_ABI_VERSION {
    uint32_t tssCreator;
    uint32_t tssFamily;
    uint32_t tssLevel;
    uint32_t tssVersion;
};

#define TSS2_ABI_VERSION_CURRENT {1, 2, 1, 108}

/*
 * Return Codes
 */
/* The return type for all TSS2 functions */
typedef uint32_t TSS2_RC;

/* For return values other than SUCCESS, the second most significant
 * byte of the return value is a layer code indicating the software
 * layer that generated the error.
 */
#define TSS2_RC_LAYER_SHIFT      (16)
#define TSS2_RC_LAYER(level)     ((TSS2_RC)level << TSS2_RC_LAYER_SHIFT)
#define TSS2_RC_LAYER_MASK       TSS2_RC_LAYER(0xff)

/* These layer codes are reserved for software layers defined in the TCG
 * specifications.
 */
#define TSS2_TPM_RC_LAYER             TSS2_RC_LAYER(0)
#define TSS2_FEATURE_RC_LAYER         TSS2_RC_LAYER(6)
#define TSS2_ESAPI_RC_LAYER           TSS2_RC_LAYER(7)
#define TSS2_SYS_RC_LAYER             TSS2_RC_LAYER(8)
#define TSS2_MU_RC_LAYER              TSS2_RC_LAYER(9)
#define TSS2_TCTI_RC_LAYER            TSS2_RC_LAYER(10)
#define TSS2_RESMGR_RC_LAYER          TSS2_RC_LAYER(11)
#define TSS2_RESMGR_TPM_RC_LAYER      TSS2_RC_LAYER(12)

/* Base return codes.
 * These base codes indicate the error that occurred. They are
 * logical-ORed with a layer code to produce the TSS2 return value.
 */
#define TSS2_BASE_RC_GENERAL_FAILURE            1U /* Catch all for all errors not otherwise specified */
#define TSS2_BASE_RC_NOT_IMPLEMENTED            2U /* If called functionality isn't implemented */
#define TSS2_BASE_RC_BAD_CONTEXT                3U /* A context structure is bad */
#define TSS2_BASE_RC_ABI_MISMATCH               4U /* Passed in ABI version doesn't match called module's ABI version */
#define TSS2_BASE_RC_BAD_REFERENCE              5U /* A pointer is NULL that isn't allowed to be NULL. */
#define TSS2_BASE_RC_INSUFFICIENT_BUFFER        6U /* A buffer isn't large enough */
#define TSS2_BASE_RC_BAD_SEQUENCE               7U /* Function called in the wrong order */
#define TSS2_BASE_RC_NO_CONNECTION              8U /* Fails to connect to next lower layer */
#define TSS2_BASE_RC_TRY_AGAIN                  9U /* Operation timed out; function must be called again to be completed */
#define TSS2_BASE_RC_IO_ERROR                  10U /* IO failure */
#define TSS2_BASE_RC_BAD_VALUE                 11U /* A parameter has a bad value */
#define TSS2_BASE_RC_NOT_PERMITTED             12U /* Operation not permitted. */
#define TSS2_BASE_RC_INVALID_SESSIONS          13U /* Session structures were sent, but command doesn't use them or doesn't use the specifed number of them */
#define TSS2_BASE_RC_NO_DECRYPT_PARAM          14U /* If function called that uses decrypt parameter, but command doesn't support crypt parameter. */
#define TSS2_BASE_RC_NO_ENCRYPT_PARAM          15U /* If function called that uses encrypt parameter, but command doesn't support encrypt parameter. */
#define TSS2_BASE_RC_BAD_SIZE                  16U /* If size of a parameter is incorrect */
#define TSS2_BASE_RC_MALFORMED_RESPONSE        17U /* Response is malformed */
#define TSS2_BASE_RC_INSUFFICIENT_CONTEXT      18U /* Context not large enough */
#define TSS2_BASE_RC_INSUFFICIENT_RESPONSE     19U /* Response is not long enough */
#define TSS2_BASE_RC_INCOMPATIBLE_TCTI         20U /* Unknown or unusable TCTI version */
#define TSS2_BASE_RC_NOT_SUPPORTED             21U /* Functionality not supported. */
#define TSS2_BASE_RC_BAD_TCTI_STRUCTURE        22U /* TCTI context is bad. */
#define TSS2_BASE_RC_MEMORY                    23U /* memory allocation failed */
#define TSS2_BASE_RC_BAD_TR                    24U /* invalid ESYS_TR handle */
#define TSS2_BASE_RC_MULTIPLE_DECRYPT_SESSIONS 25U /* More than one session with TPMA_SESSION_DECRYPT bit set */
#define TSS2_BASE_RC_MULTIPLE_ENCRYPT_SESSIONS 26U /* More than one session with TPMA_SESSION_ENCRYPT bit set */
#define TSS2_BASE_RC_RSP_AUTH_FAILED           27U /* Response HMAC from TPM did not verify */
#define TSS2_BASE_RC_NO_CONFIG                 28U
#define TSS2_BASE_RC_BAD_PATH                  29U
#define TSS2_BASE_RC_NOT_DELETABLE             30U
#define TSS2_BASE_RC_PATH_ALREADY_EXISTS       31U
#define TSS2_BASE_RC_KEY_NOT_FOUND             32U
#define TSS2_BASE_RC_SIGNATURE_VERIFICATION_FAILED 33U
#define TSS2_BASE_RC_HASH_MISMATCH             34U
#define TSS2_BASE_RC_KEY_NOT_DUPLICABLE        35U
#define TSS2_BASE_RC_PATH_NOT_FOUND            36U
#define TSS2_BASE_RC_NO_CERT                   37U
#define TSS2_BASE_RC_NO_PCR                    38U
#define TSS2_BASE_RC_PCR_NOT_RESETTABLE        39U
#define TSS2_BASE_RC_BAD_TEMPLATE              40U
#define TSS2_BASE_RC_AUTHORIZATION_FAILED      41U
#define TSS2_BASE_RC_AUTHORIZATION_UNKNOWN     42U
#define TSS2_BASE_RC_NV_NOT_READABLE           43U
#define TSS2_BASE_RC_NV_TOO_SMALL              44U
#define TSS2_BASE_RC_NV_NOT_WRITEABLE          45U
#define TSS2_BASE_RC_POLICY_UNKNOWN            46U
#define TSS2_BASE_RC_NV_WRONG_TYPE             47U
#define TSS2_BASE_RC_NAME_ALREADY_EXISTS       48U
#define TSS2_BASE_RC_NO_TPM                    49U
#define TSS2_BASE_RC_BAD_KEY                   50U
#define TSS2_BASE_RC_NO_HANDLE                 51U
#define TSS2_BASE_RC_NOT_PROVISIONED           52U
#define TSS2_BASE_RC_ALREADY_PROVISIONED       53U
#define TSS2_BASE_RC_CALLBACK_NULL             54U

/* Base return codes in the range 0xf800 - 0xffff are reserved for
 * implementation-specific purposes.
 */
#define TSS2_LAYER_IMPLEMENTATION_SPECIFIC_OFFSET 0xf800
#define TSS2_LEVEL_IMPLEMENTATION_SPECIFIC_SHIFT 11

/* Success is the same for all software layers */
#define TSS2_RC_SUCCESS ((TSS2_RC) 0)

/* TCTI error codes */
#define TSS2_TCTI_RC_GENERAL_FAILURE            ((TSS2_RC)(TSS2_TCTI_RC_LAYER | \
                                                    TSS2_BASE_RC_GENERAL_FAILURE))
#define TSS2_TCTI_RC_NOT_IMPLEMENTED            ((TSS2_RC)(TSS2_TCTI_RC_LAYER | \
                                                    TSS2_BASE_RC_NOT_IMPLEMENTED))
#define TSS2_TCTI_RC_BAD_CONTEXT                ((TSS2_RC)(TSS2_TCTI_RC_LAYER | \
                                                     TSS2_BASE_RC_BAD_CONTEXT))
#define TSS2_TCTI_RC_ABI_MISMATCH               ((TSS2_RC)(TSS2_TCTI_RC_LAYER | \
                                                     TSS2_BASE_RC_ABI_MISMATCH))
#define TSS2_TCTI_RC_BAD_REFERENCE              ((TSS2_RC)(TSS2_TCTI_RC_LAYER | \
                                                     TSS2_BASE_RC_BAD_REFERENCE))
#define TSS2_TCTI_RC_INSUFFICIENT_BUFFER        ((TSS2_RC)(TSS2_TCTI_RC_LAYER | \
                                                     TSS2_BASE_RC_INSUFFICIENT_BUFFER))
#define TSS2_TCTI_RC_BAD_SEQUENCE               ((TSS2_RC)(TSS2_TCTI_RC_LAYER |  \
                                                     TSS2_BASE_RC_BAD_SEQUENCE))
#define TSS2_TCTI_RC_NO_CONNECTION              ((TSS2_RC)(TSS2_TCTI_RC_LAYER | \
                                                     TSS2_BASE_RC_NO_CONNECTION))
#define TSS2_TCTI_RC_TRY_AGAIN                  ((TSS2_RC)(TSS2_TCTI_RC_LAYER | \
                                                     TSS2_BASE_RC_TRY_AGAIN))
#define TSS2_TCTI_RC_IO_ERROR                   ((TSS2_RC)(TSS2_TCTI_RC_LAYER | \
                                                     TSS2_BASE_RC_IO_ERROR))
#define TSS2_TCTI_RC_BAD_VALUE                  ((TSS2_RC)(TSS2_TCTI_RC_LAYER | \
                                                     TSS2_BASE_RC_BAD_VALUE))
#define TSS2_TCTI_RC_NOT_PERMITTED              ((TSS2_RC)(TSS2_TCTI_RC_LAYER | \
                                                     TSS2_BASE_RC_NOT_PERMITTED))
#define TSS2_TCTI_RC_MALFORMED_RESPONSE         ((TSS2_RC)(TSS2_TCTI_RC_LAYER | \
                                                     TSS2_BASE_RC_MALFORMED_RESPONSE))
#define TSS2_TCTI_RC_NOT_SUPPORTED              ((TSS2_RC)(TSS2_TCTI_RC_LAYER | \
                                                     TSS2_BASE_RC_NOT_SUPPORTED))
#define TSS2_TCTI_RC_MEMORY                     ((TSS2_RC)(TSS2_TCTI_RC_LAYER | \
                                                     TSS2_BASE_RC_MEMORY))
/* SAPI error codes */
#define TSS2_SYS_RC_GENERAL_FAILURE            ((TSS2_RC)(TSS2_SYS_RC_LAYER | \
                                                    TSS2_BASE_RC_GENERAL_FAILURE))
#define TSS2_SYS_RC_ABI_MISMATCH                ((TSS2_RC)(TSS2_SYS_RC_LAYER | \
                                                     TSS2_BASE_RC_ABI_MISMATCH))
#define TSS2_SYS_RC_BAD_REFERENCE               ((TSS2_RC)(TSS2_SYS_RC_LAYER | \
                                                     TSS2_BASE_RC_BAD_REFERENCE))
#define TSS2_SYS_RC_INSUFFICIENT_BUFFER         ((TSS2_RC)(TSS2_SYS_RC_LAYER | \
                                                     TSS2_BASE_RC_INSUFFICIENT_BUFFER))
#define TSS2_SYS_RC_BAD_SEQUENCE                ((TSS2_RC)(TSS2_SYS_RC_LAYER | \
                                                     TSS2_BASE_RC_BAD_SEQUENCE))
#define TSS2_SYS_RC_BAD_VALUE                   ((TSS2_RC)(TSS2_SYS_RC_LAYER | \
                                                     TSS2_BASE_RC_BAD_VALUE))
#define TSS2_SYS_RC_INVALID_SESSIONS            ((TSS2_RC)(TSS2_SYS_RC_LAYER | \
                                                     TSS2_BASE_RC_INVALID_SESSIONS))
#define TSS2_SYS_RC_NO_DECRYPT_PARAM            ((TSS2_RC)(TSS2_SYS_RC_LAYER | \
                                                     TSS2_BASE_RC_NO_DECRYPT_PARAM))
#define TSS2_SYS_RC_NO_ENCRYPT_PARAM            ((TSS2_RC)(TSS2_SYS_RC_LAYER | \
                                                     TSS2_BASE_RC_NO_ENCRYPT_PARAM))
#define TSS2_SYS_RC_BAD_SIZE                    ((TSS2_RC)(TSS2_SYS_RC_LAYER | \
                                                     TSS2_BASE_RC_BAD_SIZE))
#define TSS2_SYS_RC_MALFORMED_RESPONSE          ((TSS2_RC)(TSS2_SYS_RC_LAYER | \
                                                     TSS2_BASE_RC_MALFORMED_RESPONSE))
#define TSS2_SYS_RC_INSUFFICIENT_CONTEXT        ((TSS2_RC)(TSS2_SYS_RC_LAYER | \
                                                     TSS2_BASE_RC_INSUFFICIENT_CONTEXT))
#define TSS2_SYS_RC_INSUFFICIENT_RESPONSE       ((TSS2_RC)(TSS2_SYS_RC_LAYER | \
                                                     TSS2_BASE_RC_INSUFFICIENT_RESPONSE))
#define TSS2_SYS_RC_INCOMPATIBLE_TCTI           ((TSS2_RC)(TSS2_SYS_RC_LAYER | \
                                                     TSS2_BASE_RC_INCOMPATIBLE_TCTI))
#define TSS2_SYS_RC_BAD_TCTI_STRUCTURE          ((TSS2_RC)(TSS2_SYS_RC_LAYER | \
                                                     TSS2_BASE_RC_BAD_TCTI_STRUCTURE))

/* MUAPI error codes */
#define TSS2_MU_RC_GENERAL_FAILURE              ((TSS2_RC)(TSS2_MU_RC_LAYER | \
                                                     TSS2_BASE_RC_GENERAL_FAILURE))
#define TSS2_MU_RC_BAD_REFERENCE                ((TSS2_RC)(TSS2_MU_RC_LAYER | \
                                                     TSS2_BASE_RC_BAD_REFERENCE))
#define TSS2_MU_RC_BAD_SIZE                     ((TSS2_RC)(TSS2_MU_RC_LAYER | \
                                                     TSS2_BASE_RC_BAD_SIZE))
#define TSS2_MU_RC_BAD_VALUE                    ((TSS2_RC)(TSS2_MU_RC_LAYER | \
                                                     TSS2_BASE_RC_BAD_VALUE))
#define TSS2_MU_RC_INSUFFICIENT_BUFFER          ((TSS2_RC)(TSS2_MU_RC_LAYER | \
                                                     TSS2_BASE_RC_INSUFFICIENT_BUFFER))

/* ESAPI Error Codes */
#define TSS2_ESYS_RC_GENERAL_FAILURE             ((TSS2_RC)(TSS2_ESAPI_RC_LAYER | \
                                                      TSS2_BASE_RC_GENERAL_FAILURE))
#define TSS2_ESYS_RC_NOT_IMPLEMENTED             ((TSS2_RC)(TSS2_ESAPI_RC_LAYER | \
                                                      TSS2_BASE_RC_NOT_IMPLEMENTED))
#define TSS2_ESYS_RC_ABI_MISMATCH                ((TSS2_RC)(TSS2_ESAPI_RC_LAYER | \
                                                      TSS2_BASE_RC_ABI_MISMATCH))
#define TSS2_ESYS_RC_BAD_REFERENCE               ((TSS2_RC)(TSS2_ESAPI_RC_LAYER | \
                                                      TSS2_BASE_RC_BAD_REFERENCE))
#define TSS2_ESYS_RC_INSUFFICIENT_BUFFER         ((TSS2_RC)(TSS2_ESAPI_RC_LAYER | \
                                                      TSS2_BASE_RC_INSUFFICIENT_BUFFER))
#define TSS2_ESYS_RC_BAD_SEQUENCE                ((TSS2_RC)(TSS2_ESAPI_RC_LAYER | \
                                                      TSS2_BASE_RC_BAD_SEQUENCE))
#define TSS2_ESYS_RC_INVALID_SESSIONS            ((TSS2_RC)(TSS2_ESAPI_RC_LAYER | \
                                                      TSS2_BASE_RC_INVALID_SESSIONS))
#define TSS2_ESYS_RC_TRY_AGAIN                   ((TSS2_RC)(TSS2_ESAPI_RC_LAYER | \
                                                      TSS2_BASE_RC_TRY_AGAIN))
#define TSS2_ESYS_RC_IO_ERROR                    ((TSS2_RC)(TSS2_ESAPI_RC_LAYER | \
                                                      TSS2_BASE_RC_IO_ERROR))
#define TSS2_ESYS_RC_BAD_VALUE                   ((TSS2_RC)(TSS2_ESAPI_RC_LAYER | \
                                                      TSS2_BASE_RC_BAD_VALUE))
#define TSS2_ESYS_RC_NO_DECRYPT_PARAM            ((TSS2_RC)(TSS2_ESAPI_RC_LAYER | \
                                                      TSS2_BASE_RC_NO_DECRYPT_PARAM))
#define TSS2_ESYS_RC_NO_ENCRYPT_PARAM            ((TSS2_RC)(TSS2_ESAPI_RC_LAYER | \
                                                      TSS2_BASE_RC_NO_ENCRYPT_PARAM))
#define TSS2_ESYS_RC_BAD_SIZE                    ((TSS2_RC)(TSS2_ESAPI_RC_LAYER | \
                                                      TSS2_BASE_RC_BAD_SIZE))
#define TSS2_ESYS_RC_MALFORMED_RESPONSE          ((TSS2_RC)(TSS2_ESAPI_RC_LAYER | \
                                                      TSS2_BASE_RC_MALFORMED_RESPONSE))
#define TSS2_ESYS_RC_INSUFFICIENT_CONTEXT        ((TSS2_RC)(TSS2_ESAPI_RC_LAYER | \
                                                      TSS2_BASE_RC_INSUFFICIENT_CONTEXT))
#define TSS2_ESYS_RC_INSUFFICIENT_RESPONSE       ((TSS2_RC)(TSS2_ESAPI_RC_LAYER | \
                                                      TSS2_BASE_RC_INSUFFICIENT_RESPONSE))
#define TSS2_ESYS_RC_INCOMPATIBLE_TCTI           ((TSS2_RC)(TSS2_ESAPI_RC_LAYER | \
                                                      TSS2_BASE_RC_INCOMPATIBLE_TCTI))
#define TSS2_ESYS_RC_BAD_TCTI_STRUCTURE          ((TSS2_RC)(TSS2_ESAPI_RC_LAYER | \
                                                      TSS2_BASE_RC_BAD_TCTI_STRUCTURE))
#define TSS2_ESYS_RC_MEMORY                      ((TSS2_RC)(TSS2_ESAPI_RC_LAYER | \
                                                      TSS2_BASE_RC_MEMORY))
#define TSS2_ESYS_RC_BAD_TR                      ((TSS2_RC)(TSS2_ESAPI_RC_LAYER | \
                                                        TSS2_BASE_RC_BAD_TR))
#define TSS2_ESYS_RC_MULTIPLE_DECRYPT_SESSIONS   ((TSS2_RC)(TSS2_ESAPI_RC_LAYER | \
                                                        TSS2_BASE_RC_MULTIPLE_DECRYPT_SESSIONS))
#define TSS2_ESYS_RC_MULTIPLE_ENCRYPT_SESSIONS   ((TSS2_RC)(TSS2_ESAPI_RC_LAYER | \
                                                        TSS2_BASE_RC_MULTIPLE_ENCRYPT_SESSIONS))
#define TSS2_ESYS_RC_NOT_SUPPORTED               ((TSS2_RC)(TSS2_ESAPI_RC_LAYER | \
                                                        TSS2_BASE_RC_NOT_SUPPORTED))
#define TSS2_ESYS_RC_RSP_AUTH_FAILED             ((TSS2_RC)(TSS2_ESAPI_RC_LAYER | \
                                                        TSS2_BASE_RC_RSP_AUTH_FAILED))
#define TSS2_ESYS_RC_CALLBACK_NULL               ((TSS2_RC)(TSS2_ESAPI_RC_LAYER | \
                                                        TSS2_BASE_RC_CALLBACK_NULL))
/* FAPI Error Codes */

#define TSS2_FAPI_RC_GENERAL_FAILURE             ((TSS2_RC)(TSS2_FEATURE_RC_LAYER | \
                                                      TSS2_BASE_RC_GENERAL_FAILURE))
#define TSS2_FAPI_RC_NOT_IMPLEMENTED             ((TSS2_RC)(TSS2_FEATURE_RC_LAYER | \
                                                      TSS2_BASE_RC_NOT_IMPLEMENTED))
#define TSS2_FAPI_RC_BAD_REFERENCE               ((TSS2_RC)(TSS2_FEATURE_RC_LAYER | \
                                                      TSS2_BASE_RC_BAD_REFERENCE))
#define TSS2_FAPI_RC_BAD_SEQUENCE                ((TSS2_RC)(TSS2_FEATURE_RC_LAYER | \
                                                      TSS2_BASE_RC_BAD_SEQUENCE))
#define TSS2_FAPI_RC_IO_ERROR                    ((TSS2_RC)(TSS2_FEATURE_RC_LAYER | \
                                                      TSS2_BASE_RC_IO_ERROR))
#define TSS2_FAPI_RC_BAD_VALUE                   ((TSS2_RC)(TSS2_FEATURE_RC_LAYER | \
                                                      TSS2_BASE_RC_BAD_VALUE))
#define TSS2_FAPI_RC_NO_DECRYPT_PARAM            ((TSS2_RC)(TSS2_FEATURE_RC_LAYER | \
                                                      TSS2_BASE_RC_NO_DECRYPT_PARAM))
#define TSS2_FAPI_RC_NO_ENCRYPT_PARAM            ((TSS2_RC)(TSS2_FEATURE_RC_LAYER | \
                                                      TSS2_BASE_RC_NO_ENCRYPT_PARAM))
#define TSS2_FAPI_RC_MEMORY                      ((TSS2_RC)(TSS2_FEATURE_RC_LAYER | \
                                                      TSS2_BASE_RC_MEMORY))
#define TSS2_FAPI_RC_BAD_CONTEXT                 ((TSS2_RC)(TSS2_FEATURE_RC_LAYER | \
                                                        TSS2_BASE_RC_BAD_CONTEXT))
#define TSS2_FAPI_RC_NO_CONFIG                   ((TSS2_RC)(TSS2_FEATURE_RC_LAYER | \
                                                        TSS2_BASE_RC_NO_CONFIG))
#define TSS2_FAPI_RC_BAD_PATH                    ((TSS2_RC)(TSS2_FEATURE_RC_LAYER | \
                                                        TSS2_BASE_RC_BAD_PATH))
#define TSS2_FAPI_RC_NOT_DELETABLE               ((TSS2_RC)(TSS2_FEATURE_RC_LAYER | \
                                                        TSS2_BASE_RC_NOT_DELETABLE))
#define TSS2_FAPI_RC_PATH_ALREADY_EXISTS         ((TSS2_RC)(TSS2_FEATURE_RC_LAYER | \
                                                        TSS2_BASE_RC_PATH_ALREADY_EXISTS))
#define TSS2_FAPI_RC_KEY_NOT_FOUND               ((TSS2_RC)(TSS2_FEATURE_RC_LAYER | \
                                                        TSS2_BASE_RC_KEY_NOT_FOUND))
#define TSS2_FAPI_RC_SIGNATURE_VERIFICATION_FAILED ((TSS2_RC)(TSS2_FEATURE_RC_LAYER | \
                                                        TSS2_BASE_RC_SIGNATURE_VERIFICATION_FAILED))
#define TSS2_FAPI_RC_HASH_MISMATCH               ((TSS2_RC)(TSS2_FEATURE_RC_LAYER | \
                                                        TSS2_BASE_RC_HASH_MISMATCH))
#define TSS2_FAPI_RC_KEY_NOT_DUPLICABLE          ((TSS2_RC)(TSS2_FEATURE_RC_LAYER | \
                                                        TSS2_BASE_RC_KEY_NOT_DUPLICABLE))
#define TSS2_FAPI_RC_PATH_NOT_FOUND              ((TSS2_RC)(TSS2_FEATURE_RC_LAYER | \
                                                        TSS2_BASE_RC_PATH_NOT_FOUND))
#define TSS2_FAPI_RC_NO_CERT                     ((TSS2_RC)(TSS2_FEATURE_RC_LAYER | \
                                                        TSS2_BASE_RC_NO_CERT))
#define TSS2_FAPI_RC_NO_PCR                      ((TSS2_RC)(TSS2_FEATURE_RC_LAYER | \
                                                        TSS2_BASE_RC_NO_PCR))
#define TSS2_FAPI_RC_PCR_NOT_RESETTABLE          ((TSS2_RC)(TSS2_FEATURE_RC_LAYER | \
                                                        TSS2_BASE_RC_PCR_NOT_RESETTABLE))
#define TSS2_FAPI_RC_BAD_TEMPLATE                ((TSS2_RC)(TSS2_FEATURE_RC_LAYER | \
                                                        TSS2_BASE_RC_BAD_TEMPLATE))
#define TSS2_FAPI_RC_AUTHORIZATION_FAILED        ((TSS2_RC)(TSS2_FEATURE_RC_LAYER | \
                                                        TSS2_BASE_RC_AUTHORIZATION_FAILED))
#define TSS2_FAPI_RC_AUTHORIZATION_UNKNOWN       ((TSS2_RC)(TSS2_FEATURE_RC_LAYER | \
                                                        TSS2_BASE_RC_AUTHORIZATION_UNKNOWN))
#define TSS2_FAPI_RC_NV_NOT_READABLE             ((TSS2_RC)(TSS2_FEATURE_RC_LAYER | \
                                                        TSS2_BASE_RC_NV_NOT_READABLE))
#define TSS2_FAPI_RC_NV_TOO_SMALL                ((TSS2_RC)(TSS2_FEATURE_RC_LAYER | \
                                                        TSS2_BASE_RC_NV_TOO_SMALL))
#define TSS2_FAPI_RC_NV_NOT_WRITEABLE            ((TSS2_RC)(TSS2_FEATURE_RC_LAYER | \
                                                        TSS2_BASE_RC_NV_NOT_WRITEABLE))
#define TSS2_FAPI_RC_POLICY_UNKNOWN              ((TSS2_RC)(TSS2_FEATURE_RC_LAYER | \
                                                        TSS2_BASE_RC_POLICY_UNKNOWN))
#define TSS2_FAPI_RC_NV_WRONG_TYPE               ((TSS2_RC)(TSS2_FEATURE_RC_LAYER | \
                                                        TSS2_BASE_RC_NV_WRONG_TYPE))
#define TSS2_FAPI_RC_NAME_ALREADY_EXISTS         ((TSS2_RC)(TSS2_FEATURE_RC_LAYER | \
                                                        TSS2_BASE_RC_NAME_ALREADY_EXISTS))
#define TSS2_FAPI_RC_NO_TPM                      ((TSS2_RC)(TSS2_FEATURE_RC_LAYER | \
                                                        TSS2_BASE_RC_NO_TPM))
#define TSS2_FAPI_RC_TRY_AGAIN                   ((TSS2_RC)(TSS2_FEATURE_RC_LAYER | \
                                                        TSS2_BASE_RC_TRY_AGAIN))
#define TSS2_FAPI_RC_BAD_KEY                     ((TSS2_RC)(TSS2_FEATURE_RC_LAYER | \
                                                        TSS2_BASE_RC_BAD_KEY))
#define TSS2_FAPI_RC_NO_HANDLE                   ((TSS2_RC)(TSS2_FEATURE_RC_LAYER | \
                                                        TSS2_BASE_RC_NO_HANDLE))
#define TSS2_FAPI_RC_NOT_PROVISIONED             ((TSS2_RC)(TSS2_FEATURE_RC_LAYER | \
                                                        TSS2_BASE_RC_NOT_PROVISIONED))
#define TSS2_FAPI_RC_ALREADY_PROVISIONED         ((TSS2_RC)(TSS2_FEATURE_RC_LAYER | \
                                                        TSS2_BASE_RC_ALREADY_PROVISIONED))
#define TSS2_FAPI_RC_NULL_CALLBACK               ((TSS2_RC)(TSS2_FEATURE_RC_LAYER | \
                                                      TSS2_BASE_RC_CALLBACK_NULL))
#endif /* TSS2_COMMON_H */
