/* SPDX-License-Identifier: BSD-2-Clause */
/***********************************************************************
 * Copyright (c) 2015 - 2017, Intel Corporation
 *
 * All rights reserved.
 ***********************************************************************/

#ifndef MARSHAL_H
#define MARSHAL_H

#include <stdlib.h>
#include "tss2_common.h"
#include "tss2_tpm2_types.h"

#ifndef TSS2_API_VERSION_1_2_1_108
#error Version mismatch among TSS2 header files.
#endif  /* TSS2_API_VERSION_1_2_1_108 */

#ifdef __cplusplus
extern "C" {
#endif

TSS2_RC
Tss2_MU_INT8_Marshal(
    INT8            src,
    uint8_t         buffer[],
    size_t          buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_INT8_Unmarshal(
    uint8_t const   buffer[],
    size_t          buffer_size,
    size_t         *offset,
    INT8           *dest);

TSS2_RC
Tss2_MU_INT16_Marshal(
    INT16           src,
    uint8_t         buffer[],
    size_t          buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_INT16_Unmarshal(
    uint8_t const   buffer[],
    size_t          buffer_size,
    size_t         *offset,
    INT16          *dest);

TSS2_RC
Tss2_MU_INT32_Marshal(
    INT32           src,
    uint8_t         buffer[],
    size_t          buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_INT32_Unmarshal(
    uint8_t const   buffer[],
    size_t          buffer_size,
    size_t         *offset,
    INT32          *dest);

TSS2_RC
Tss2_MU_INT64_Marshal(
    INT64           src,
    uint8_t         buffer[],
    size_t          buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_INT64_Unmarshal(
    uint8_t const   buffer[],
    size_t          buffer_size,
    size_t         *offset,
    INT64          *dest);

TSS2_RC
Tss2_MU_UINT8_Marshal(
    UINT8           src,
    uint8_t         buffer[],
    size_t          buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_UINT8_Unmarshal(
    uint8_t const   buffer[],
    size_t          buffer_size,
    size_t         *offset,
    UINT8          *dest);

TSS2_RC
Tss2_MU_UINT16_Marshal(
    UINT16          src,
    uint8_t         buffer[],
    size_t          buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_UINT16_Unmarshal(
    uint8_t const   buffer[],
    size_t          buffer_size,
    size_t         *offset,
    UINT16         *dest);

TSS2_RC
Tss2_MU_UINT32_Marshal(
    UINT32          src,
    uint8_t         buffer[],
    size_t          buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_UINT32_Unmarshal(
    uint8_t const   buffer[],
    size_t          buffer_size,
    size_t         *offset,
    UINT32         *dest);

TSS2_RC
Tss2_MU_UINT64_Marshal(
    UINT64          src,
    uint8_t         buffer[],
    size_t          buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_UINT64_Unmarshal(
    uint8_t const   buffer[],
    size_t          buffer_size,
    size_t         *offset,
    UINT64         *dest);

TSS2_RC
Tss2_MU_TPM2_CC_Marshal(
    TPM2_CC          src,
    uint8_t         buffer[],
    size_t          buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPM2_CC_Unmarshal(
    uint8_t const   buffer[],
    size_t          buffer_size,
    size_t         *offset,
    TPM2_CC         *dest);

TSS2_RC
Tss2_MU_TPM2_ST_Marshal(
    TPM2_ST          src,
    uint8_t         buffer[],
    size_t          buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPM2_ST_Unmarshal(
    uint8_t const   buffer[],
    size_t          buffer_size,
    size_t         *offset,
    TPM2_ST         *dest);

TSS2_RC
Tss2_MU_TPMA_ALGORITHM_Marshal(
    TPMA_ALGORITHM  src,
    uint8_t         buffer[],
    size_t          buffer_size,
    size_t          *offset);

TSS2_RC
Tss2_MU_TPMA_ALGORITHM_Unmarshal(
    uint8_t const   buffer[],
    size_t          buffer_size,
    size_t         *offset,
    TPMA_ALGORITHM *dest);

TSS2_RC
Tss2_MU_TPMA_CC_Marshal(
    TPMA_CC         src,
    uint8_t         buffer[],
    size_t          buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPMA_CC_Unmarshal(
    uint8_t const   buffer[],
    size_t          buffer_size,
    size_t         *offset,
    TPMA_CC        *dest);

TSS2_RC
Tss2_MU_TPMA_LOCALITY_Marshal(
    TPMA_LOCALITY   src,
    uint8_t         buffer[],
    size_t          buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPMA_LOCALITY_Unmarshal(
    uint8_t const   buffer[],
    size_t          buffer_size,
    size_t         *offset,
    TPMA_LOCALITY  *dest);
TSS2_RC

Tss2_MU_TPMA_NV_Marshal(
    TPMA_NV         src,
    uint8_t         buffer[],
    size_t          buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPMA_NV_Unmarshal(
    uint8_t const   buffer[],
    size_t          buffer_size,
    size_t         *offset,
    TPMA_NV        *dest);

TSS2_RC
Tss2_MU_TPMA_OBJECT_Marshal(
    TPMA_OBJECT     src,
    uint8_t         buffer[],
    size_t          buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPMA_OBJECT_Unmarshal(
    uint8_t const   buffer[],
    size_t          buffer_size,
    size_t         *offset,
    TPMA_OBJECT    *dest);

TSS2_RC
Tss2_MU_TPMA_PERMANENT_Marshal(
    TPMA_PERMANENT  src,
    uint8_t         buffer[],
    size_t          buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPMA_PERMANENT_Unmarshal(
    uint8_t const   buffer[],
    size_t          buffer_size,
    size_t         *offset,
    TPMA_PERMANENT *dest);

TSS2_RC
Tss2_MU_TPMA_SESSION_Marshal(
    TPMA_SESSION    src,
    uint8_t         buffer[],
    size_t          buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPMA_SESSION_Unmarshal(
    uint8_t const   buffer[],
    size_t          buffer_size,
    size_t         *offset,
    TPMA_SESSION   *dest);

TSS2_RC
Tss2_MU_TPMA_STARTUP_CLEAR_Marshal(
    TPMA_STARTUP_CLEAR src,
    uint8_t         buffer[],
    size_t          buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPMA_STARTUP_CLEAR_Unmarshal(
    uint8_t const   buffer[],
    size_t          buffer_size,
    size_t         *offset,
    TPMA_STARTUP_CLEAR *dest);

TSS2_RC
Tss2_MU_TPM2B_DIGEST_Marshal(
    TPM2B_DIGEST const *src,
    uint8_t         buffer[],
    size_t          buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPM2B_DIGEST_Unmarshal(
    uint8_t const   buffer[],
    size_t          buffer_size,
    size_t         *offset,
    TPM2B_DIGEST   *dest);

TSS2_RC
Tss2_MU_TPM2B_ATTEST_Marshal(
    TPM2B_ATTEST const *src,
    uint8_t         buffer[],
    size_t          buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPM2B_ATTEST_Unmarshal(
    uint8_t const   buffer[],
    size_t          buffer_size,
    size_t         *offset,
    TPM2B_ATTEST   *dest);

TSS2_RC
Tss2_MU_TPM2B_NAME_Marshal(
    TPM2B_NAME const *src,
    uint8_t         buffer[],
    size_t          buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPM2B_NAME_Unmarshal(
    uint8_t const   buffer[],
    size_t          buffer_size,
    size_t         *offset,
    TPM2B_NAME     *dest);

TSS2_RC
Tss2_MU_TPM2B_MAX_NV_BUFFER_Marshal(
    TPM2B_MAX_NV_BUFFER const *src,
    uint8_t         buffer[],
    size_t          buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPM2B_MAX_NV_BUFFER_Unmarshal(
    uint8_t const   buffer[],
    size_t          buffer_size,
    size_t         *offset,
    TPM2B_MAX_NV_BUFFER *dest);

TSS2_RC
Tss2_MU_TPM2B_SENSITIVE_DATA_Marshal(
    TPM2B_SENSITIVE_DATA const *src,
    uint8_t         buffer[],
    size_t          buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPM2B_SENSITIVE_DATA_Unmarshal(
    uint8_t const   buffer[],
    size_t          buffer_size,
    size_t         *offset,
    TPM2B_SENSITIVE_DATA *dest);

TSS2_RC
Tss2_MU_TPM2B_ECC_PARAMETER_Marshal(
    TPM2B_ECC_PARAMETER const *src,
    uint8_t         buffer[],
    size_t          buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPM2B_ECC_PARAMETER_Unmarshal(
    uint8_t const   buffer[],
    size_t          buffer_size,
    size_t         *offset,
    TPM2B_ECC_PARAMETER *dest);

TSS2_RC
Tss2_MU_TPM2B_PUBLIC_KEY_RSA_Marshal(
    TPM2B_PUBLIC_KEY_RSA const *src,
    uint8_t         buffer[],
    size_t          buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPM2B_PUBLIC_KEY_RSA_Unmarshal(
    uint8_t const   buffer[],
    size_t          buffer_size,
    size_t         *offset,
    TPM2B_PUBLIC_KEY_RSA *dest);

TSS2_RC
Tss2_MU_TPM2B_PRIVATE_KEY_RSA_Marshal(
    TPM2B_PRIVATE_KEY_RSA const *src,
    uint8_t         buffer[],
    size_t          buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPM2B_PRIVATE_KEY_RSA_Unmarshal(
    uint8_t const   buffer[],
    size_t          buffer_size,
    size_t         *offset,
    TPM2B_PRIVATE_KEY_RSA *dest);

TSS2_RC
Tss2_MU_TPM2B_PRIVATE_Marshal(
    TPM2B_PRIVATE const *src,
    uint8_t         buffer[],
    size_t          buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPM2B_PRIVATE_Unmarshal(
    uint8_t const   buffer[],
    size_t          buffer_size,
    size_t         *offset,
    TPM2B_PRIVATE  *dest);

TSS2_RC
Tss2_MU_TPM2B_CONTEXT_SENSITIVE_Marshal(
    TPM2B_CONTEXT_SENSITIVE const *src,
    uint8_t         buffer[],
    size_t          buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPM2B_CONTEXT_SENSITIVE_Unmarshal(
    uint8_t const   buffer[],
    size_t          buffer_size,
    size_t         *offset,
    TPM2B_CONTEXT_SENSITIVE *dest);

TSS2_RC
Tss2_MU_TPM2B_CONTEXT_DATA_Marshal(
    TPM2B_CONTEXT_DATA const *src,
    uint8_t         buffer[],
    size_t          buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPM2B_CONTEXT_DATA_Unmarshal(
    uint8_t const   buffer[],
    size_t          buffer_size,
    size_t         *offset,
    TPM2B_CONTEXT_DATA *dest);

TSS2_RC
Tss2_MU_TPM2B_DATA_Marshal(
    TPM2B_DATA      const *src,
    uint8_t         buffer[],
    size_t          buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPM2B_DATA_Unmarshal(
    uint8_t const   buffer[],
    size_t          buffer_size,
    size_t         *offset,
    TPM2B_DATA     *dest);

TSS2_RC
Tss2_MU_TPM2B_SYM_KEY_Marshal(
    TPM2B_SYM_KEY   const *src,
    uint8_t         buffer[],
    size_t          buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPM2B_SYM_KEY_Unmarshal(
    uint8_t const   buffer[],
    size_t          buffer_size,
    size_t         *offset,
    TPM2B_SYM_KEY  *dest);

TSS2_RC
Tss2_MU_TPM2B_ECC_POINT_Marshal(
    TPM2B_ECC_POINT const *src,
    uint8_t         buffer[],
    size_t          buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPM2B_ECC_POINT_Unmarshal(
    uint8_t const   buffer[],
    size_t          buffer_size,
    size_t          *offset,
    TPM2B_ECC_POINT *dest);

TSS2_RC
Tss2_MU_TPM2B_NV_PUBLIC_Marshal(
    TPM2B_NV_PUBLIC const *src,
    uint8_t         buffer[],
    size_t          buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPM2B_NV_PUBLIC_Unmarshal(
    uint8_t const   buffer[],
    size_t          buffer_size,
    size_t          *offset,
    TPM2B_NV_PUBLIC *dest);

TSS2_RC
Tss2_MU_TPM2B_SENSITIVE_Marshal(
    TPM2B_SENSITIVE const *src,
    uint8_t         buffer[],
    size_t          buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPM2B_SENSITIVE_Unmarshal(
    uint8_t const   buffer[],
    size_t          buffer_size,
    size_t          *offset,
    TPM2B_SENSITIVE *dest);

TSS2_RC
Tss2_MU_TPM2B_SENSITIVE_CREATE_Marshal(
    TPM2B_SENSITIVE_CREATE const *src,
    uint8_t         buffer[],
    size_t          buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPM2B_SENSITIVE_CREATE_Unmarshal(
    uint8_t const   buffer[],
    size_t          buffer_size,
    size_t          *offset,
    TPM2B_SENSITIVE_CREATE *dest);

TSS2_RC
Tss2_MU_TPM2B_CREATION_DATA_Marshal(
    TPM2B_CREATION_DATA const *src,
    uint8_t         buffer[],
    size_t          buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPM2B_CREATION_DATA_Unmarshal(
    uint8_t const   buffer[],
    size_t          buffer_size,
    size_t          *offset,
    TPM2B_CREATION_DATA *dest);

TSS2_RC
Tss2_MU_TPM2B_PUBLIC_Marshal(
    TPM2B_PUBLIC    const *src,
    uint8_t         buffer[],
    size_t          buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPM2B_PUBLIC_Unmarshal(
    uint8_t const   buffer[],
    size_t          buffer_size,
    size_t          *offset,
    TPM2B_PUBLIC    *dest);

TSS2_RC
Tss2_MU_TPM2B_ENCRYPTED_SECRET_Marshal(
    TPM2B_ENCRYPTED_SECRET  const *src,
    uint8_t         buffer[],
    size_t          buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPM2B_ENCRYPTED_SECRET_Unmarshal(
    uint8_t const  buffer[],
    size_t          buffer_size,
    size_t          *offset,
    TPM2B_ENCRYPTED_SECRET *dest);

TSS2_RC
Tss2_MU_TPM2B_ID_OBJECT_Marshal(
    TPM2B_ID_OBJECT const *src,
    uint8_t         buffer[],
    size_t          buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPM2B_ID_OBJECT_Unmarshal(
    uint8_t const  buffer[],
    size_t          buffer_size,
    size_t          *offset,
    TPM2B_ID_OBJECT *dest);

TSS2_RC
Tss2_MU_TPM2B_IV_Marshal(
    TPM2B_IV const *src,
    uint8_t         buffer[],
    size_t          buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPM2B_IV_Unmarshal(
    uint8_t const  buffer[],
    size_t          buffer_size,
    size_t          *offset,
    TPM2B_IV        *dest);

TSS2_RC
Tss2_MU_TPM2B_AUTH_Marshal(
    TPM2B_AUTH const *src,
    uint8_t         buffer[],
    size_t          buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPM2B_AUTH_Unmarshal(
    uint8_t const  buffer[],
    size_t          buffer_size,
    size_t          *offset,
    TPM2B_AUTH      *dest);

TSS2_RC
Tss2_MU_TPM2B_EVENT_Marshal(
    TPM2B_EVENT const *src,
    uint8_t         buffer[],
    size_t          buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPM2B_EVENT_Unmarshal(
    uint8_t const  buffer[],
    size_t          buffer_size,
    size_t          *offset,
    TPM2B_EVENT     *dest);

TSS2_RC
Tss2_MU_TPM2B_MAX_BUFFER_Marshal(
    TPM2B_MAX_BUFFER const *src,
    uint8_t         buffer[],
    size_t          buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPM2B_MAX_BUFFER_Unmarshal(
    uint8_t const   buffer[],
    size_t          buffer_size,
    size_t          *offset,
    TPM2B_MAX_BUFFER *dest);

TSS2_RC
Tss2_MU_TPM2B_NONCE_Marshal(
    TPM2B_NONCE const *src,
    uint8_t         buffer[],
    size_t          buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPM2B_NONCE_Unmarshal(
    uint8_t const   buffer[],
    size_t          buffer_size,
    size_t          *offset,
    TPM2B_NONCE     *dest);

TSS2_RC
Tss2_MU_TPM2B_OPERAND_Marshal(
    TPM2B_OPERAND const *src,
    uint8_t         buffer[],
    size_t          buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPM2B_OPERAND_Unmarshal(
    uint8_t const   buffer[],
    size_t          buffer_size,
    size_t          *offset,
    TPM2B_OPERAND   *dest);

TSS2_RC
Tss2_MU_TPM2B_TIMEOUT_Marshal(
    TPM2B_TIMEOUT const *src,
    uint8_t         buffer[],
    size_t          buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPM2B_TIMEOUT_Unmarshal(
    uint8_t const   buffer[],
    size_t          buffer_size,
    size_t          *offset,
    TPM2B_TIMEOUT   *dest);

TSS2_RC
Tss2_MU_TPM2B_TEMPLATE_Marshal(
    TPM2B_TEMPLATE  const *src,
    uint8_t         buffer[],
    size_t          buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPM2B_TEMPLATE_Unmarshal(
    uint8_t const   buffer[],
    size_t          buffer_size,
    size_t          *offset,
    TPM2B_TEMPLATE  *dest);

TSS2_RC
Tss2_MU_TPMS_CONTEXT_Marshal(
    TPMS_CONTEXT    const *src,
    uint8_t         buffer[],
    size_t          buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPMS_CONTEXT_Unmarshal(
    uint8_t const   buffer[],
    size_t          buffer_size,
    size_t         *offset,
    TPMS_CONTEXT   *dest);

TSS2_RC
Tss2_MU_TPMS_TIME_INFO_Marshal(
    TPMS_TIME_INFO  const *src,
    uint8_t         buffer[],
    size_t          buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPMS_TIME_INFO_Unmarshal(
    uint8_t const   buffer[],
    size_t          buffer_size,
    size_t         *offset,
    TPMS_TIME_INFO *dest);

TSS2_RC
Tss2_MU_TPMS_ECC_POINT_Marshal(
    TPMS_ECC_POINT  const *src,
    uint8_t         buffer[],
    size_t          buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPMS_ECC_POINT_Unmarshal(
    uint8_t const   buffer[],
    size_t          buffer_size,
    size_t         *offset,
    TPMS_ECC_POINT *dest);

TSS2_RC
Tss2_MU_TPMS_NV_PUBLIC_Marshal(
    TPMS_NV_PUBLIC  const *src,
    uint8_t         buffer[],
    size_t          buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPMS_NV_PUBLIC_Unmarshal(
    uint8_t const   buffer[],
    size_t          buffer_size,
    size_t         *offset,
    TPMS_NV_PUBLIC *dest);

TSS2_RC
Tss2_MU_TPMS_ALG_PROPERTY_Marshal(
    TPMS_ALG_PROPERTY  const *src,
    uint8_t         buffer[],
    size_t          buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPMS_ALG_PROPERTY_Unmarshal(
    uint8_t const   buffer[],
    size_t          buffer_size,
    size_t         *offset,
    TPMS_ALG_PROPERTY *dest);

TSS2_RC
Tss2_MU_TPMS_TAGGED_PROPERTY_Marshal(
    TPMS_TAGGED_PROPERTY  const *src,
    uint8_t         buffer[],
    size_t          buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPMS_TAGGED_PROPERTY_Unmarshal(
    uint8_t const   buffer[],
    size_t          buffer_size,
    size_t         *offset,
    TPMS_TAGGED_PROPERTY *dest);

TSS2_RC
Tss2_MU_TPMS_TAGGED_POLICY_Marshal(
    TPMS_TAGGED_POLICY  const *src,
    uint8_t         buffer[],
    size_t          buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPMS_TAGGED_POLICY_Unmarshal(
    uint8_t const   buffer[],
    size_t          buffer_size,
    size_t         *offset,
    TPMS_TAGGED_POLICY *dest);

TSS2_RC
Tss2_MU_TPMS_CLOCK_INFO_Marshal(
    TPMS_CLOCK_INFO  const *src,
    uint8_t         buffer[],
    size_t          buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPMS_CLOCK_INFO_Unmarshal(
    uint8_t const   buffer[],
    size_t          buffer_size,
    size_t         *offset,
    TPMS_CLOCK_INFO *dest);

TSS2_RC
Tss2_MU_TPMS_TIME_ATTEST_INFO_Marshal(
    TPMS_TIME_ATTEST_INFO  const *src,
    uint8_t         buffer[],
    size_t          buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPMS_TIME_ATTEST_INFO_Unmarshal(
    uint8_t const   buffer[],
    size_t          buffer_size,
    size_t         *offset,
    TPMS_TIME_ATTEST_INFO *dest);

TSS2_RC
Tss2_MU_TPMS_CERTIFY_INFO_Marshal(
    TPMS_CERTIFY_INFO  const *src,
    uint8_t         buffer[],
    size_t          buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPMS_CERTIFY_INFO_Unmarshal(
    uint8_t const   buffer[],
    size_t          buffer_size,
    size_t         *offset,
    TPMS_CERTIFY_INFO *dest);

TSS2_RC
Tss2_MU_TPMS_COMMAND_AUDIT_INFO_Marshal(
    TPMS_COMMAND_AUDIT_INFO  const *src,
    uint8_t         buffer[],
    size_t          buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPMS_COMMAND_AUDIT_INFO_Unmarshal(
    uint8_t const   buffer[],
    size_t          buffer_size,
    size_t         *offset,
    TPMS_COMMAND_AUDIT_INFO *dest);

TSS2_RC
Tss2_MU_TPMS_SESSION_AUDIT_INFO_Marshal(
    TPMS_SESSION_AUDIT_INFO  const *src,
    uint8_t         buffer[],
    size_t          buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPMS_SESSION_AUDIT_INFO_Unmarshal(
    uint8_t const   buffer[],
    size_t          buffer_size,
    size_t         *offset,
    TPMS_SESSION_AUDIT_INFO *dest);

TSS2_RC
Tss2_MU_TPMS_CREATION_INFO_Marshal(
    TPMS_CREATION_INFO  const *src,
    uint8_t         buffer[],
    size_t          buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPMS_CREATION_INFO_Unmarshal(
    uint8_t const   buffer[],
    size_t          buffer_size,
    size_t         *offset,
    TPMS_CREATION_INFO *dest);

TSS2_RC
Tss2_MU_TPMS_NV_CERTIFY_INFO_Marshal(
    TPMS_NV_CERTIFY_INFO  const *src,
    uint8_t         buffer[],
    size_t          buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPMS_NV_CERTIFY_INFO_Unmarshal(
    uint8_t const   buffer[],
    size_t          buffer_size,
    size_t         *offset,
    TPMS_NV_CERTIFY_INFO *dest);

TSS2_RC
Tss2_MU_TPMS_AUTH_COMMAND_Marshal(
    TPMS_AUTH_COMMAND  const *src,
    uint8_t         buffer[],
    size_t          buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPMS_AUTH_COMMAND_Unmarshal(
    uint8_t const   buffer[],
    size_t          buffer_size,
    size_t         *offset,
    TPMS_AUTH_COMMAND *dest);

TSS2_RC
Tss2_MU_TPMS_AUTH_RESPONSE_Marshal(
    TPMS_AUTH_RESPONSE  const *src,
    uint8_t         buffer[],
    size_t          buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPMS_AUTH_RESPONSE_Unmarshal(
    uint8_t const   buffer[],
    size_t          buffer_size,
    size_t         *offset,
    TPMS_AUTH_RESPONSE *dest);

TSS2_RC
Tss2_MU_TPMS_SENSITIVE_CREATE_Marshal(
    TPMS_SENSITIVE_CREATE  const *src,
    uint8_t         buffer[],
    size_t          buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPMS_SENSITIVE_CREATE_Unmarshal(
    uint8_t const   buffer[],
    size_t          buffer_size,
    size_t         *offset,
    TPMS_SENSITIVE_CREATE *dest);

TSS2_RC
Tss2_MU_TPMS_SCHEME_HASH_Marshal(
    TPMS_SCHEME_HASH  const *src,
    uint8_t         buffer[],
    size_t          buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPMS_SCHEME_HASH_Unmarshal(
    uint8_t const   buffer[],
    size_t          buffer_size,
    size_t         *offset,
    TPMS_SCHEME_HASH *dest);

TSS2_RC
Tss2_MU_TPMS_SCHEME_ECDAA_Marshal(
    TPMS_SCHEME_ECDAA  const *src,
    uint8_t         buffer[],
    size_t          buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPMS_SCHEME_ECDAA_Unmarshal(
    uint8_t const   buffer[],
    size_t          buffer_size,
    size_t         *offset,
    TPMS_SCHEME_ECDAA *dest);

TSS2_RC
Tss2_MU_TPMS_SCHEME_XOR_Marshal(
    TPMS_SCHEME_XOR  const *src,
    uint8_t         buffer[],
    size_t          buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPMS_SCHEME_XOR_Unmarshal(
    uint8_t const   buffer[],
    size_t          buffer_size,
    size_t         *offset,
    TPMS_SCHEME_XOR *dest);

TSS2_RC
Tss2_MU_TPMS_SIGNATURE_RSA_Marshal(
    TPMS_SIGNATURE_RSA  const *src,
    uint8_t         buffer[],
    size_t          buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPMS_SIGNATURE_RSA_Unmarshal(
    uint8_t const   buffer[],
    size_t          buffer_size,
    size_t         *offset,
    TPMS_SIGNATURE_RSA *dest);

TSS2_RC
Tss2_MU_TPMS_SIGNATURE_ECC_Marshal(
    TPMS_SIGNATURE_ECC  const *src,
    uint8_t         buffer[],
    size_t          buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPMS_SIGNATURE_ECC_Unmarshal(
    uint8_t const   buffer[],
    size_t          buffer_size,
    size_t         *offset,
    TPMS_SIGNATURE_ECC *dest);

TSS2_RC
Tss2_MU_TPMS_NV_PIN_COUNTER_PARAMETERS_Marshal(
    TPMS_NV_PIN_COUNTER_PARAMETERS  const *src,
    uint8_t         buffer[],
    size_t          buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPMS_NV_PIN_COUNTER_PARAMETERS_Unmarshal(
    uint8_t const   buffer[],
    size_t          buffer_size,
    size_t         *offset,
    TPMS_NV_PIN_COUNTER_PARAMETERS *dest);

TSS2_RC
Tss2_MU_TPMS_CONTEXT_DATA_Marshal(
    TPMS_CONTEXT_DATA  const *src,
    uint8_t         buffer[],
    size_t          buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPMS_CONTEXT_DATA_Unmarshal(
    uint8_t const   buffer[],
    size_t          buffer_size,
    size_t         *offset,
    TPMS_CONTEXT_DATA *dest);

TSS2_RC
Tss2_MU_TPMS_PCR_SELECT_Marshal(
    TPMS_PCR_SELECT  const *src,
    uint8_t         buffer[],
    size_t          buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPMS_PCR_SELECT_Unmarshal(
    uint8_t const   buffer[],
    size_t          buffer_size,
    size_t         *offset,
    TPMS_PCR_SELECT *dest);

TSS2_RC
Tss2_MU_TPMS_PCR_SELECTION_Marshal(
    TPMS_PCR_SELECTION  const *src,
    uint8_t         buffer[],
    size_t          buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPMS_PCR_SELECTION_Unmarshal(
    uint8_t const   buffer[],
    size_t          buffer_size,
    size_t         *offset,
    TPMS_PCR_SELECTION *dest);

TSS2_RC
Tss2_MU_TPMS_TAGGED_PCR_SELECT_Marshal(
    TPMS_TAGGED_PCR_SELECT  const *src,
    uint8_t         buffer[],
    size_t          buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPMS_TAGGED_PCR_SELECT_Unmarshal(
    uint8_t const   buffer[],
    size_t          buffer_size,
    size_t         *offset,
    TPMS_TAGGED_PCR_SELECT *dest);

TSS2_RC
Tss2_MU_TPMS_QUOTE_INFO_Marshal(
    TPMS_QUOTE_INFO  const *src,
    uint8_t         buffer[],
    size_t          buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPMS_QUOTE_INFO_Unmarshal(
    uint8_t const   buffer[],
    size_t          buffer_size,
    size_t         *offset,
    TPMS_QUOTE_INFO *dest);

TSS2_RC
Tss2_MU_TPMS_CREATION_DATA_Marshal(
    TPMS_CREATION_DATA  const *src,
    uint8_t         buffer[],
    size_t          buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPMS_CREATION_DATA_Unmarshal(
    uint8_t const   buffer[],
    size_t          buffer_size,
    size_t         *offset,
    TPMS_CREATION_DATA *dest);

TSS2_RC
Tss2_MU_TPMS_ECC_PARMS_Marshal(
    TPMS_ECC_PARMS  const *src,
    uint8_t         buffer[],
    size_t          buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPMS_ECC_PARMS_Unmarshal(
    uint8_t const   buffer[],
    size_t          buffer_size,
    size_t         *offset,
    TPMS_ECC_PARMS *dest);

TSS2_RC
Tss2_MU_TPMS_ATTEST_Marshal(
    TPMS_ATTEST     const *src,
    uint8_t         buffer[],
    size_t          buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPMS_ATTEST_Unmarshal(
    uint8_t const   buffer[],
    size_t          buffer_size,
    size_t         *offset,
    TPMS_ATTEST *dest);

TSS2_RC
Tss2_MU_TPMS_ALGORITHM_DETAIL_ECC_Marshal(
    TPMS_ALGORITHM_DETAIL_ECC const *src,
    uint8_t         buffer[],
    size_t          buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPMS_ALGORITHM_DETAIL_ECC_Unmarshal(
    uint8_t const   buffer[],
    size_t          buffer_size,
    size_t         *offset,
    TPMS_ALGORITHM_DETAIL_ECC *dest);

TSS2_RC
Tss2_MU_TPMS_CAPABILITY_DATA_Marshal(
    TPMS_CAPABILITY_DATA const *src,
    uint8_t         buffer[],
    size_t          buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPMS_CAPABILITY_DATA_Unmarshal(
    uint8_t const   buffer[],
    size_t          buffer_size,
    size_t         *offset,
    TPMS_CAPABILITY_DATA *dest);

TSS2_RC
Tss2_MU_TPMS_KEYEDHASH_PARMS_Marshal(
    TPMS_KEYEDHASH_PARMS const *src,
    uint8_t         buffer[],
    size_t          buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPMS_KEYEDHASH_PARMS_Unmarshal(
    uint8_t const   buffer[],
    size_t          buffer_size,
    size_t         *offset,
    TPMS_KEYEDHASH_PARMS *dest);

TSS2_RC
Tss2_MU_TPMS_RSA_PARMS_Marshal(
    TPMS_RSA_PARMS  const *src,
    uint8_t         buffer[],
    size_t          buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPMS_RSA_PARMS_Unmarshal(
    uint8_t const   buffer[],
    size_t          buffer_size,
    size_t         *offset,
    TPMS_RSA_PARMS *dest);

TSS2_RC
Tss2_MU_TPMS_SYMCIPHER_PARMS_Marshal(
    TPMS_SYMCIPHER_PARMS const *src,
    uint8_t         buffer[],
    size_t          buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPMS_SYMCIPHER_PARMS_Unmarshal(
    uint8_t const   buffer[],
    size_t          buffer_size,
    size_t         *offset,
    TPMS_SYMCIPHER_PARMS *dest);

TSS2_RC
Tss2_MU_TPMS_AC_OUTPUT_Marshal(
    TPMS_AC_OUTPUT  const *src,
    uint8_t         buffer[],
    size_t          buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPMS_AC_OUTPUT_Unmarshal(
    uint8_t const   buffer[],
    size_t          buffer_size,
    size_t         *offset,
    TPMS_AC_OUTPUT *dest);

TSS2_RC
Tss2_MU_TPMS_ID_OBJECT_Marshal(
    TPMS_ID_OBJECT  const *src,
    uint8_t         buffer[],
    size_t          buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPMS_ID_OBJECT_Unmarshal(
    uint8_t const   buffer[],
    size_t          buffer_size,
    size_t         *offset,
    TPMS_ID_OBJECT *dest);

TSS2_RC
Tss2_MU_TPMS_ACT_DATA_Marshal(
    TPMS_ACT_DATA   const *src,
    uint8_t         buffer[],
    size_t          buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPMS_ACT_DATA_Unmarshal(
    uint8_t const   buffer[],
    size_t          buffer_size,
    size_t         *offset,
    TPMS_ACT_DATA  *dest);

TSS2_RC
Tss2_MU_TPMS_NV_DIGEST_CERTIFY_INFO_Marshal(
    TPMS_NV_DIGEST_CERTIFY_INFO const *src,
    uint8_t         buffer[],
    size_t          buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPMS_NV_DIGEST_CERTIFY_INFO_Unmarshal(
    uint8_t const   buffer[],
    size_t          buffer_size,
    size_t         *offset,
    TPMS_NV_DIGEST_CERTIFY_INFO *dest);

TSS2_RC
Tss2_MU_TPML_CC_Marshal(
    TPML_CC const *src,
    uint8_t      buffer[],
    size_t       buffer_size,
    size_t      *offset);

TSS2_RC
Tss2_MU_TPML_CC_Unmarshal(
    uint8_t const   buffer[],
    size_t          buffer_size,
    size_t         *offset,
    TPML_CC        *dest);

TSS2_RC
Tss2_MU_TPML_CCA_Marshal(
    TPML_CCA const *src,
    uint8_t      buffer[],
    size_t       buffer_size,
    size_t      *offset);

TSS2_RC
Tss2_MU_TPML_CCA_Unmarshal(
    uint8_t const   buffer[],
    size_t          buffer_size,
    size_t         *offset,
    TPML_CCA       *dest);

TSS2_RC
Tss2_MU_TPML_ALG_Marshal(
    TPML_ALG const *src,
    uint8_t      buffer[],
    size_t       buffer_size,
    size_t      *offset);

TSS2_RC
Tss2_MU_TPML_ALG_Unmarshal(
    uint8_t const   buffer[],
    size_t          buffer_size,
    size_t         *offset,
    TPML_ALG       *dest);

TSS2_RC
Tss2_MU_TPML_HANDLE_Marshal(
    TPML_HANDLE const *src,
    uint8_t      buffer[],
    size_t       buffer_size,
    size_t      *offset);

TSS2_RC
Tss2_MU_TPML_HANDLE_Unmarshal(
    uint8_t const   buffer[],
    size_t          buffer_size,
    size_t         *offset,
    TPML_HANDLE    *dest);

TSS2_RC
Tss2_MU_TPML_DIGEST_Marshal(
    TPML_DIGEST const *src,
    uint8_t      buffer[],
    size_t       buffer_size,
    size_t      *offset);

TSS2_RC
Tss2_MU_TPML_DIGEST_Unmarshal(
    uint8_t const   buffer[],
    size_t          buffer_size,
    size_t         *offset,
    TPML_DIGEST    *dest);

TSS2_RC
Tss2_MU_TPML_DIGEST_VALUES_Marshal(
    TPML_DIGEST_VALUES const *src,
    uint8_t      buffer[],
    size_t       buffer_size,
    size_t      *offset);

TSS2_RC
Tss2_MU_TPML_DIGEST_VALUES_Unmarshal(
    uint8_t const   buffer[],
    size_t          buffer_size,
    size_t         *offset,
    TPML_DIGEST_VALUES *dest);

TSS2_RC
Tss2_MU_TPML_PCR_SELECTION_Marshal(
    TPML_PCR_SELECTION const *src,
    uint8_t      buffer[],
    size_t       buffer_size,
    size_t      *offset);

TSS2_RC
Tss2_MU_TPML_PCR_SELECTION_Unmarshal(
    uint8_t const   buffer[],
    size_t          buffer_size,
    size_t         *offset,
    TPML_PCR_SELECTION *dest);

TSS2_RC
Tss2_MU_TPML_ALG_PROPERTY_Marshal(
    TPML_ALG_PROPERTY const *src,
    uint8_t      buffer[],
    size_t       buffer_size,
    size_t      *offset);

TSS2_RC
Tss2_MU_TPML_ALG_PROPERTY_Unmarshal(
    uint8_t const   buffer[],
    size_t          buffer_size,
    size_t         *offset,
    TPML_ALG_PROPERTY *dest);

TSS2_RC
Tss2_MU_TPML_ECC_CURVE_Marshal(
    TPML_ECC_CURVE const *src,
    uint8_t      buffer[],
    size_t       buffer_size,
    size_t      *offset);

TSS2_RC
Tss2_MU_TPML_ECC_CURVE_Unmarshal(
    uint8_t const   buffer[],
    size_t          buffer_size,
    size_t         *offset,
    TPML_ECC_CURVE *dest);

TSS2_RC
Tss2_MU_TPML_TAGGED_PCR_PROPERTY_Marshal(
    TPML_TAGGED_PCR_PROPERTY const *src,
    uint8_t      buffer[],
    size_t       buffer_size,
    size_t      *offset);

TSS2_RC
Tss2_MU_TPML_TAGGED_PCR_PROPERTY_Unmarshal(
    uint8_t const   buffer[],
    size_t          buffer_size,
    size_t         *offset,
    TPML_TAGGED_PCR_PROPERTY *dest);

TSS2_RC
Tss2_MU_TPML_TAGGED_TPM_PROPERTY_Marshal(
    TPML_TAGGED_TPM_PROPERTY const *src,
    uint8_t      buffer[],
    size_t       buffer_size,
    size_t      *offset);

TSS2_RC
Tss2_MU_TPML_TAGGED_TPM_PROPERTY_Unmarshal(
    uint8_t const   buffer[],
    size_t          buffer_size,
    size_t         *offset,
    TPML_TAGGED_TPM_PROPERTY *dest);

TSS2_RC
Tss2_MU_TPML_AC_CAPABILITIES_Marshal(
    TPML_AC_CAPABILITIES const *src,
    uint8_t      buffer[],
    size_t       buffer_size,
    size_t      *offset);

TSS2_RC
Tss2_MU_TPML_AC_CAPABILITIES_Unmarshal(
    uint8_t const   buffer[],
    size_t          buffer_size,
    size_t         *offset,
    TPML_AC_CAPABILITIES *dest);

TSS2_RC
Tss2_MU_TPML_TAGGED_POLICY_Marshal(
    TPML_TAGGED_POLICY const *src,
    uint8_t      buffer[],
    size_t       buffer_size,
    size_t      *offset);

TSS2_RC
Tss2_MU_TPML_TAGGED_POLICY_Unmarshal(
    uint8_t const   buffer[],
    size_t          buffer_size,
    size_t         *offset,
    TPML_TAGGED_POLICY *dest);

TSS2_RC
Tss2_MU_TPML_ACT_DATA_Marshal(
    TPML_ACT_DATA const *src,
    uint8_t      buffer[],
    size_t       buffer_size,
    size_t      *offset);

TSS2_RC
Tss2_MU_TPML_ACT_DATA_Unmarshal(
    uint8_t const   buffer[],
    size_t          buffer_size,
    size_t         *offset,
    TPML_ACT_DATA *dest);

TSS2_RC
Tss2_MU_TPMU_HA_Marshal(
    TPMU_HA const *src,
    uint32_t       selector_value,
    uint8_t        buffer[],
    size_t         buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPMU_HA_Unmarshal(
    uint8_t const  buffer[],
    size_t         buffer_size,
    size_t        *offset,
    uint32_t       selector_value,
    TPMU_HA       *dest);

TSS2_RC
Tss2_MU_TPMU_CAPABILITIES_Marshal(
    TPMU_CAPABILITIES const *src,
    uint32_t       selector_value,
    uint8_t        buffer[],
    size_t         buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPMU_CAPABILITIES_Unmarshal(
    uint8_t const  buffer[],
    size_t         buffer_size,
    size_t        *offset,
    uint32_t       selector_value,
    TPMU_CAPABILITIES *dest);

TSS2_RC
Tss2_MU_TPMU_ATTEST_Marshal(
    TPMU_ATTEST const *src,
    uint32_t       selector_value,
    uint8_t        buffer[],
    size_t         buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPMU_ATTEST_Unmarshal(
    uint8_t const  buffer[],
    size_t         buffer_size,
    size_t        *offset,
    uint32_t       selector_value,
    TPMU_ATTEST *dest);

TSS2_RC
Tss2_MU_TPMU_SYM_KEY_BITS_Marshal(
    TPMU_SYM_KEY_BITS const *src,
    uint32_t       selector_value,
    uint8_t        buffer[],
    size_t         buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPMU_SYM_KEY_BITS_Unmarshal(
    uint8_t const  buffer[],
    size_t         buffer_size,
    size_t        *offset,
    uint32_t       selector_value,
    TPMU_SYM_KEY_BITS *dest);

TSS2_RC
Tss2_MU_TPMU_SYM_MODE_Marshal(
    TPMU_SYM_MODE const *src,
    uint32_t       selector_value,
    uint8_t        buffer[],
    size_t         buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPMU_SYM_MODE_Unmarshal(
    uint8_t const  buffer[],
    size_t         buffer_size,
    size_t        *offset,
    uint32_t       selector_value,
    TPMU_SYM_MODE *dest);

TSS2_RC
Tss2_MU_TPMU_SIG_SCHEME_Marshal(
    TPMU_SIG_SCHEME const *src,
    uint32_t       selector_value,
    uint8_t        buffer[],
    size_t         buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPMU_SIG_SCHEME_Unmarshal(
    uint8_t const  buffer[],
    size_t         buffer_size,
    size_t        *offset,
    uint32_t       selector_value,
    TPMU_SIG_SCHEME *dest);

TSS2_RC
Tss2_MU_TPMU_KDF_SCHEME_Marshal(
    TPMU_KDF_SCHEME const *src,
    uint32_t       selector_value,
    uint8_t        buffer[],
    size_t         buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPMU_KDF_SCHEME_Unmarshal(
    uint8_t const  buffer[],
    size_t         buffer_size,
    size_t        *offset,
    uint32_t       selector_value,
    TPMU_KDF_SCHEME *dest);

TSS2_RC
Tss2_MU_TPMU_ASYM_SCHEME_Marshal(
    TPMU_ASYM_SCHEME const *src,
    uint32_t       selector_value,
    uint8_t        buffer[],
    size_t         buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPMU_ASYM_SCHEME_Unmarshal(
    uint8_t const  buffer[],
    size_t         buffer_size,
    size_t        *offset,
    uint32_t       selector_value,
    TPMU_ASYM_SCHEME *dest);

TSS2_RC
Tss2_MU_TPMU_SCHEME_KEYEDHASH_Marshal(
    TPMU_SCHEME_KEYEDHASH const *src,
    uint32_t       selector_value,
    uint8_t        buffer[],
    size_t         buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPMU_SCHEME_KEYEDHASH_Unmarshal(
    uint8_t const  buffer[],
    size_t         buffer_size,
    size_t        *offset,
    uint32_t       selector_value,
    TPMU_SCHEME_KEYEDHASH *dest);

TSS2_RC
Tss2_MU_TPMU_SIGNATURE_Marshal(
    TPMU_SIGNATURE const *src,
    uint32_t       selector_value,
    uint8_t        buffer[],
    size_t         buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPMU_SIGNATURE_Unmarshal(
    uint8_t const  buffer[],
    size_t         buffer_size,
    size_t        *offset,
    uint32_t       selector_value,
    TPMU_SIGNATURE *dest);

TSS2_RC
Tss2_MU_TPMU_SENSITIVE_COMPOSITE_Marshal(
    TPMU_SENSITIVE_COMPOSITE const *src,
    uint32_t       selector_value,
    uint8_t        buffer[],
    size_t         buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPMU_SENSITIVE_COMPOSITE_Unmarshal(
    uint8_t const  buffer[],
    size_t         buffer_size,
    size_t        *offset,
    uint32_t       selector_value,
    TPMU_SENSITIVE_COMPOSITE *dest);

TSS2_RC
Tss2_MU_TPMU_ENCRYPTED_SECRET_Marshal(
    TPMU_ENCRYPTED_SECRET const *src,
    uint32_t       selector_value,
    uint8_t        buffer[],
    size_t         buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPMU_ENCRYPTED_SECRET_Unmarshal(
    uint8_t const  buffer[],
    size_t         buffer_size,
    size_t        *offset,
    uint32_t       selector_value,
    TPMU_ENCRYPTED_SECRET *dest);

TSS2_RC
Tss2_MU_TPMU_PUBLIC_PARMS_Marshal(
    TPMU_PUBLIC_PARMS const *src,
    uint32_t       selector_value,
    uint8_t        buffer[],
    size_t         buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPMU_PUBLIC_PARMS_Unmarshal(
    uint8_t const  buffer[],
    size_t         buffer_size,
    size_t        *offset,
    uint32_t       selector_value,
    TPMU_PUBLIC_PARMS *dest);

TSS2_RC
Tss2_MU_TPMU_PUBLIC_ID_Marshal(
    TPMU_PUBLIC_ID const *src,
    uint32_t       selector_value,
    uint8_t        buffer[],
    size_t         buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPMU_PUBLIC_ID_Unmarshal(
    uint8_t const  buffer[],
    size_t         buffer_size,
    size_t        *offset,
    uint32_t       selector_value,
    TPMU_PUBLIC_ID *dest);

TSS2_RC
Tss2_MU_TPMU_NAME_Marshal(
    TPMU_NAME      const *src,
    uint32_t       selector_value,
    uint8_t        buffer[],
    size_t         buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPMU_NAME_Unmarshal(
    uint8_t const  buffer[],
    size_t         buffer_size,
    size_t        *offset,
    uint32_t       selector_value,
    TPMU_NAME     *dest);

TSS2_RC
Tss2_MU_TPMT_HA_Marshal(
    TPMT_HA const *src,
    uint8_t        buffer[],
    size_t         buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPMT_HA_Unmarshal(
    uint8_t const  buffer[],
    size_t         buffer_size,
    size_t        *offset,
    TPMT_HA *dest);

TSS2_RC
Tss2_MU_TPMT_SYM_DEF_Marshal(
    TPMT_SYM_DEF const *src,
    uint8_t        buffer[],
    size_t         buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPMT_SYM_DEF_Unmarshal(
    uint8_t const  buffer[],
    size_t         buffer_size,
    size_t        *offset,
    TPMT_SYM_DEF  *dest);

TSS2_RC
Tss2_MU_TPMT_SYM_DEF_OBJECT_Marshal(
    TPMT_SYM_DEF_OBJECT const *src,
    uint8_t        buffer[],
    size_t         buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPMT_SYM_DEF_OBJECT_Unmarshal(
    uint8_t const  buffer[],
    size_t         buffer_size,
    size_t        *offset,
    TPMT_SYM_DEF_OBJECT *dest);

TSS2_RC
Tss2_MU_TPMT_KEYEDHASH_SCHEME_Marshal(
    TPMT_KEYEDHASH_SCHEME const *src,
    uint8_t        buffer[],
    size_t         buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPMT_KEYEDHASH_SCHEME_Unmarshal(
    uint8_t const  buffer[],
    size_t         buffer_size,
    size_t        *offset,
    TPMT_KEYEDHASH_SCHEME *dest);

TSS2_RC
Tss2_MU_TPMT_SIG_SCHEME_Marshal(
    TPMT_SIG_SCHEME const *src,
    uint8_t        buffer[],
    size_t         buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPMT_SIG_SCHEME_Unmarshal(
    uint8_t const  buffer[],
    size_t         buffer_size,
    size_t        *offset,
    TPMT_SIG_SCHEME *dest);

TSS2_RC
Tss2_MU_TPMT_KDF_SCHEME_Marshal(
    TPMT_KDF_SCHEME const *src,
    uint8_t        buffer[],
    size_t         buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPMT_KDF_SCHEME_Unmarshal(
    uint8_t const  buffer[],
    size_t         buffer_size,
    size_t        *offset,
    TPMT_KDF_SCHEME *dest);

TSS2_RC
Tss2_MU_TPMT_ASYM_SCHEME_Marshal(
    TPMT_ASYM_SCHEME const *src,
    uint8_t        buffer[],
    size_t         buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPMT_ASYM_SCHEME_Unmarshal(
    uint8_t const  buffer[],
    size_t         buffer_size,
    size_t        *offset,
    TPMT_ASYM_SCHEME *dest);

TSS2_RC
Tss2_MU_TPMT_RSA_SCHEME_Marshal(
    TPMT_RSA_SCHEME const *src,
    uint8_t        buffer[],
    size_t         buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPMT_RSA_SCHEME_Unmarshal(
    uint8_t const  buffer[],
    size_t         buffer_size,
    size_t        *offset,
    TPMT_RSA_SCHEME *dest);

TSS2_RC
Tss2_MU_TPMT_RSA_DECRYPT_Marshal(
    TPMT_RSA_DECRYPT const *src,
    uint8_t        buffer[],
    size_t         buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPMT_RSA_DECRYPT_Unmarshal(
    uint8_t const  buffer[],
    size_t         buffer_size,
    size_t        *offset,
    TPMT_RSA_DECRYPT *dest);

TSS2_RC
Tss2_MU_TPMT_ECC_SCHEME_Marshal(
    TPMT_ECC_SCHEME const *src,
    uint8_t        buffer[],
    size_t         buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPMT_ECC_SCHEME_Unmarshal(
    uint8_t const  buffer[],
    size_t         buffer_size,
    size_t        *offset,
    TPMT_ECC_SCHEME *dest);

TSS2_RC
Tss2_MU_TPMT_SIGNATURE_Marshal(
    TPMT_SIGNATURE const *src,
    uint8_t        buffer[],
    size_t         buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPMT_SIGNATURE_Unmarshal(
    uint8_t const  buffer[],
    size_t         buffer_size,
    size_t        *offset,
    TPMT_SIGNATURE *dest);

TSS2_RC
Tss2_MU_TPMT_SENSITIVE_Marshal(
    TPMT_SENSITIVE const *src,
    uint8_t        buffer[],
    size_t         buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPMT_SENSITIVE_Unmarshal(
    uint8_t const  buffer[],
    size_t         buffer_size,
    size_t        *offset,
    TPMT_SENSITIVE *dest);

TSS2_RC
Tss2_MU_TPMT_PUBLIC_Marshal(
    TPMT_PUBLIC    const *src,
    uint8_t        buffer[],
    size_t         buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPMT_PUBLIC_Unmarshal(
    uint8_t const  buffer[],
    size_t         buffer_size,
    size_t        *offset,
    TPMT_PUBLIC   *dest);

TSS2_RC
Tss2_MU_TPMT_PUBLIC_PARMS_Marshal(
    TPMT_PUBLIC_PARMS const *src,
    uint8_t        buffer[],
    size_t         buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPMT_PUBLIC_PARMS_Unmarshal(
    uint8_t const  buffer[],
    size_t         buffer_size,
    size_t        *offset,
    TPMT_PUBLIC_PARMS *dest);

TSS2_RC
Tss2_MU_TPMT_TK_CREATION_Marshal(
    TPMT_TK_CREATION const *src,
    uint8_t        buffer[],
    size_t         buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPMT_TK_CREATION_Unmarshal(
    uint8_t const  buffer[],
    size_t         buffer_size,
    size_t        *offset,
    TPMT_TK_CREATION *dest);

TSS2_RC
Tss2_MU_TPMT_TK_VERIFIED_Marshal(
    TPMT_TK_VERIFIED const *src,
    uint8_t        buffer[],
    size_t         buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPMT_TK_VERIFIED_Unmarshal(
    uint8_t const  buffer[],
    size_t         buffer_size,
    size_t        *offset,
    TPMT_TK_VERIFIED *dest);

TSS2_RC
Tss2_MU_TPMT_TK_AUTH_Marshal(
    TPMT_TK_AUTH   const *src,
    uint8_t        buffer[],
    size_t         buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPMT_TK_AUTH_Unmarshal(
    uint8_t const  buffer[],
    size_t         buffer_size,
    size_t        *offset,
    TPMT_TK_AUTH  *dest);

TSS2_RC
Tss2_MU_TPMT_TK_HASHCHECK_Marshal(
    TPMT_TK_HASHCHECK const *src,
    uint8_t        buffer[],
    size_t         buffer_size,
    size_t         *offset);

TSS2_RC
Tss2_MU_TPMT_TK_HASHCHECK_Unmarshal(
    uint8_t const  buffer[],
    size_t         buffer_size,
    size_t        *offset,
    TPMT_TK_HASHCHECK *dest);

TSS2_RC
Tss2_MU_TPM2_HANDLE_Marshal(
    TPM2_HANDLE     in,
    uint8_t         *buffer,
    size_t          size,
    size_t          *offset);

TSS2_RC
Tss2_MU_TPM2_HANDLE_Unmarshal(
    uint8_t const   buffer[],
    size_t          size,
    size_t          *offset,
    TPM2_HANDLE     *out);

TSS2_RC
Tss2_MU_TPMI_ALG_HASH_Marshal(
    TPMI_ALG_HASH   in,
    uint8_t         *buffer,
    size_t          size,
    size_t          *offset);

TSS2_RC
Tss2_MU_TPMI_ALG_HASH_Unmarshal(
    uint8_t const   buffer[],
    size_t          size,
    size_t          *offset,
    TPMI_ALG_HASH   *out);

TSS2_RC
Tss2_MU_BYTE_Marshal(
    BYTE            in,
    uint8_t         *buffer,
    size_t          size,
    size_t          *offset);

TSS2_RC
Tss2_MU_BYTE_Unmarshal(
    uint8_t const   buffer[],
    size_t          size,
    size_t          *offset,
    BYTE            *out);

TSS2_RC
Tss2_MU_TPM2_SE_Marshal(
    TPM2_SE         in,
    uint8_t         *buffer,
    size_t          size,
    size_t          *offset);

TSS2_RC
Tss2_MU_TPM2_SE_Unmarshal(
    uint8_t const   buffer[],
    size_t          size,
    size_t          *offset,
    TPM2_SE         *out);

TSS2_RC
Tss2_MU_TPM2_NT_Marshal(
    TPM2_NT         in,
    uint8_t         *buffer,
    size_t          size,
    size_t          *offset);

TSS2_RC
Tss2_MU_TPM2_NT_Unmarshal(
    uint8_t const   buffer[],
    size_t          size,
    size_t          *offset,
    TPM2_NT         *out);

TSS2_RC
Tss2_MU_TPMS_EMPTY_Marshal(
    TPMS_EMPTY const *in,
    uint8_t         *buffer,
    size_t          size,
    size_t          *offset);

TSS2_RC
Tss2_MU_TPMS_EMPTY_Unmarshal(
    uint8_t const   buffer[],
    size_t          size,
    size_t          *offset,
    TPMS_EMPTY      *out);

TSS2_RC
Tss2_MU_TPM2B_MAX_CAP_BUFFER_Marshal(
    TPM2B_MAX_CAP_BUFFER const *src,
    uint8_t                    buffer[],
    size_t                     buffer_size,
    size_t                     *offset);

TSS2_RC
Tss2_MU_TPM2B_MAX_CAP_BUFFER_Unmarshal(
        uint8_t const        buffer[],
        size_t               buffer_size,
        size_t               *offset,
        TPM2B_MAX_CAP_BUFFER *dest);

#ifndef DISABLE_VENDOR
TSS2_RC
Tss2_MU_TPML_INTEL_PTT_PROPERTY_Marshal(
    TPML_INTEL_PTT_PROPERTY const *src,
    uint8_t      buffer[],
    size_t       buffer_size,
    size_t      *offset);

TSS2_RC
Tss2_MU_TPML_INTEL_PTT_PROPERTY_Unmarshal(
    uint8_t const   buffer[],
    size_t          buffer_size,
    size_t         *offset,
    TPML_INTEL_PTT_PROPERTY *dest);
#endif /* NOT defined DISABLE_VENDOR */

#ifdef __cplusplus
}
#endif

#endif /* MARSHAL_H */
