/* SPDX-License-Identifier: BSD-2-Clause */
/*******************************************************************************
 * Copyright 2018-2019, Fraunhofer SIT sponsored by Infineon Technologies AG
 * All rights reserved.
 ******************************************************************************/
#ifndef IFAPI_POLICY_JSON_DESERIALIZE_H
#define IFAPI_POLICY_JSON_DESERIALIZE_H

#include <stdbool.h>
#include <json-c/json.h>
#include <json-c/json_util.h>

#include "tss2_tpm2_types.h"
#include "fapi_int.h"

TSS2_RC
ifapi_json_TPMI_POLICYTYPE_deserialize(json_object *jso, TPMI_POLICYTYPE *out);

TSS2_RC
ifapi_json_TPMI_POLICYTYPE_deserialize_txt(json_object *jso,
        TPMI_POLICYTYPE *out);

TSS2_RC
ifapi_json_TPMS_POLICYSIGNED_deserialize(json_object *jso,
        TPMS_POLICYSIGNED *out);

TSS2_RC
ifapi_json_TPMS_POLICYSECRET_deserialize(json_object *jso,
        TPMS_POLICYSECRET *out);

TSS2_RC
ifapi_json_TPMS_POLICYLOCALITY_deserialize(json_object *jso,
        TPMS_POLICYLOCALITY *out);

TSS2_RC
ifapi_json_TPMS_POLICYNV_deserialize(json_object *jso, TPMS_POLICYNV *out);

TSS2_RC
ifapi_json_TPMS_POLICYCOUNTERTIMER_deserialize(json_object *jso,
        TPMS_POLICYCOUNTERTIMER *out);

TSS2_RC
ifapi_json_TPMS_POLICYCOMMANDCODE_deserialize(json_object *jso,
        TPMS_POLICYCOMMANDCODE *out);

TSS2_RC
ifapi_json_TPMS_POLICYPHYSICALPRESENCE_deserialize(json_object *jso,
        TPMS_POLICYPHYSICALPRESENCE *out);

TSS2_RC
ifapi_json_TPMS_POLICYCPHASH_deserialize(json_object *jso,
        TPMS_POLICYCPHASH *out);

TSS2_RC
ifapi_json_TPMS_POLICYNAMEHASH_deserialize(json_object *jso,
        TPMS_POLICYNAMEHASH *out);

TSS2_RC
ifapi_json_TPMS_POLICYDUPLICATIONSELECT_deserialize(json_object *jso,
        TPMS_POLICYDUPLICATIONSELECT *out);

TSS2_RC
ifapi_json_TPMS_POLICYAUTHORIZE_deserialize(json_object *jso,
        TPMS_POLICYAUTHORIZE *out);

TSS2_RC
ifapi_json_TPMS_POLICYAUTHVALUE_deserialize(json_object *jso,
        TPMS_POLICYAUTHVALUE *out);

TSS2_RC
ifapi_json_TPMS_POLICYPASSWORD_deserialize(json_object *jso,
        TPMS_POLICYPASSWORD *out);

TSS2_RC
ifapi_json_TPMS_POLICYNVWRITTEN_deserialize(json_object *jso,
        TPMS_POLICYNVWRITTEN *out);

TSS2_RC
ifapi_json_TPMS_POLICYTEMPLATE_deserialize(json_object *jso,
        TPMS_POLICYTEMPLATE *out);

TSS2_RC
ifapi_json_TPMS_POLICYAUTHORIZENV_deserialize(json_object *jso,
        TPMS_POLICYAUTHORIZENV *out);

TSS2_RC
ifapi_json_TPMS_POLICYACTION_deserialize(json_object *jso,
        TPMS_POLICYACTION *out);

TSS2_RC
ifapi_json_TPMS_PCRVALUE_deserialize(json_object *jso, TPMS_PCRVALUE *out);

TSS2_RC
ifapi_json_TPML_PCRVALUES_deserialize(json_object *jso, TPML_PCRVALUES **out);

TSS2_RC
ifapi_json_TPMS_POLICYPCR_deserialize(json_object *jso, TPMS_POLICYPCR *out);

TSS2_RC
ifapi_json_TPMS_POLICYAUTHORIZATION_deserialize(json_object *jso,
        TPMS_POLICYAUTHORIZATION *out);

TSS2_RC
ifapi_json_TPML_POLICYAUTHORIZATIONS_deserialize(json_object *jso,
        TPML_POLICYAUTHORIZATIONS **out);

TSS2_RC
ifapi_json_TPMS_POLICYBRANCH_deserialize(json_object *jso,
        TPMS_POLICYBRANCH *out);

TSS2_RC
ifapi_json_TPML_POLICYBRANCHES_deserialize(json_object *jso,
        TPML_POLICYBRANCHES **out);

TSS2_RC
ifapi_json_TPMS_POLICYOR_deserialize(json_object *jso, TPMS_POLICYOR *out);

TSS2_RC
ifapi_json_TPMU_POLICYELEMENT_deserialize(UINT32 selector, json_object *jso,
        TPMU_POLICYELEMENT *out);

TSS2_RC
ifapi_json_TPMT_POLICYELEMENT_deserialize(json_object *jso,
        TPMT_POLICYELEMENT *out);

TSS2_RC
ifapi_json_TPML_POLICYELEMENTS_deserialize(json_object *jso,
        TPML_POLICYELEMENTS **out);

TSS2_RC
ifapi_json_TPMS_POLICY_deserialize(json_object *jso,
        TPMS_POLICY *out);

#endif /* IFAPI_POLICY_JSON_DESERIALIZE_H */
