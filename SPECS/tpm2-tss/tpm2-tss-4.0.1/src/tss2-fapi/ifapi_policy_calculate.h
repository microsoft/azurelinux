/* SPDX-License-Identifier: BSD-2-Clause */
/*******************************************************************************
 * Copyright 2018-2019, Fraunhofer SIT sponsored by Infineon Technologies AG
 * All rights reserved.
 *******************************************************************************/
#ifndef FAPI_POLICY_CALCULATE_H
#define FAPI_POLICY_CALCULATE_H

#include <stdint.h>
#include <stdarg.h>
#include <stdbool.h>
#include <sys/stat.h>
#include <json-c/json.h>
#include <json-c/json_util.h>

#include "tss2_esys.h"
#include "tss2_fapi.h"
#include "fapi_int.h"
//#include "fapi_policy.h"
//#include "ifapi_keystore.h"

TSS2_RC
ifapi_calculate_policy(
    TPML_POLICYELEMENTS *policy,
    TPML_DIGEST_VALUES *policyDigests,
    TPMI_ALG_HASH hash_alg,
    size_t hash_size,
    size_t digest_idx);

#endif /* FAPI_POLICY_CALCULATE_H */
