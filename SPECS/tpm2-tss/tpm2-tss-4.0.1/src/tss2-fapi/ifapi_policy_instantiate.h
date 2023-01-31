/* SPDX-License-Identifier: BSD-2-Clause */
/*******************************************************************************
 * Copyright 2018-2019, Fraunhofer SIT sponsored by Infineon Technologies AG
 * All rights reserved.
 *******************************************************************************/
#ifndef FAPI_POLICY_INSTANTIATE_H
#define FAPI_POLICY_INSTANTIATE_H

#include <stdint.h>
#include <stdarg.h>
#include <stdbool.h>
#include <sys/stat.h>
#include <json-c/json.h>
#include <json-c/json_util.h>

#include "tss2_esys.h"
#include "tss2_fapi.h"
#include "tss2_policy.h"
//#include "fapi_int.h"
//#include "fapi_policy.h"
//#include "ifapi_keystore.h"

/** Type for representing the context for policy instantiation.
 */
typedef struct {
    TPMS_POLICY                         *policy; /**< The policy to be instantiated */
    NODE_OBJECT_T              *policy_elements; /** The policy elements to be instantiated */
    TSS2_POLICY_CALC_CALLBACKS          callbacks;
} IFAPI_POLICY_EVAL_INST_CTX;

TSS2_RC
ifapi_policyeval_instantiate_async(
    IFAPI_POLICY_EVAL_INST_CTX *context, /* For re-entry after try_again for offsets and such */
    TPMS_POLICY *policy);                /* in */
TSS2_RC

ifapi_policyeval_instantiate_finish(
    IFAPI_POLICY_EVAL_INST_CTX *context);

#endif /* FAPI_POLICY_INSTANTIATE_H */
