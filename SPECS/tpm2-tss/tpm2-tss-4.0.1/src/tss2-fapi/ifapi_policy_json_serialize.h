/* SPDX-License-Identifier: BSD-2-Clause */
/*******************************************************************************
 * Copyright 2018-2019, Fraunhofer SIT sponsored by Infineon Technologies AG
 * All rights reserved.
 ******************************************************************************/
#ifndef IFAPI_POLICY_JSON_SERIALIZE_H
#define IFAPI_POLICY_JSON_SERIALIZE_H

#include <stdbool.h>
#include <json-c/json.h>
#include <json-c/json_util.h>

#include "tss2_tpm2_types.h"
#include "fapi_int.h"

TSS2_RC
ifapi_json_TPMI_POLICYTYPE_serialize(const TPMI_POLICYTYPE in,
                                     json_object **jso);

TSS2_RC
ifapi_json_TPMI_POLICYTYPE_serialize_txt(const TPMI_POLICYTYPE in,
        json_object **jso);

TSS2_RC
ifapi_json_TPMS_POLICYSIGNED_serialize(const TPMS_POLICYSIGNED *in,
                                       json_object **jso);

TSS2_RC
ifapi_json_TPMS_POLICYSECRET_serialize(const TPMS_POLICYSECRET *in,
                                       json_object **jso);

TSS2_RC
ifapi_json_TPMS_POLICYLOCALITY_serialize(const TPMS_POLICYLOCALITY *in,
        json_object **jso);

TSS2_RC
ifapi_json_TPMS_POLICYNV_serialize(const TPMS_POLICYNV *in, json_object **jso);

TSS2_RC
ifapi_json_TPMS_POLICYCOUNTERTIMER_serialize(const TPMS_POLICYCOUNTERTIMER *in,
        json_object **jso);

TSS2_RC
ifapi_json_TPMS_POLICYCOMMANDCODE_serialize(const TPMS_POLICYCOMMANDCODE *in,
        json_object **jso);

TSS2_RC
ifapi_json_TPMS_POLICYPHYSICALPRESENCE_serialize(const
        TPMS_POLICYPHYSICALPRESENCE *in, json_object **jso);

TSS2_RC
ifapi_json_TPMS_POLICYCPHASH_serialize(const TPMS_POLICYCPHASH *in,
                                       json_object **jso);

TSS2_RC
ifapi_json_TPMS_POLICYNAMEHASH_serialize(const TPMS_POLICYNAMEHASH *in,
        json_object **jso);

TSS2_RC
ifapi_json_TPMS_POLICYDUPLICATIONSELECT_serialize(const
        TPMS_POLICYDUPLICATIONSELECT *in, json_object **jso);

TSS2_RC
ifapi_json_TPMS_POLICYAUTHORIZE_serialize(const TPMS_POLICYAUTHORIZE *in,
        json_object **jso);

TSS2_RC
ifapi_json_TPMS_POLICYAUTHVALUE_serialize(const TPMS_POLICYAUTHVALUE *in,
        json_object **jso);

TSS2_RC
ifapi_json_TPMS_POLICYPASSWORD_serialize(const TPMS_POLICYPASSWORD *in,
        json_object **jso);

TSS2_RC
ifapi_json_TPMS_POLICYNVWRITTEN_serialize(const TPMS_POLICYNVWRITTEN *in,
        json_object **jso);

TSS2_RC
ifapi_json_TPMS_POLICYTEMPLATE_serialize(const TPMS_POLICYTEMPLATE *in,
        json_object **jso);

TSS2_RC
ifapi_json_TPMS_POLICYAUTHORIZENV_serialize(const TPMS_POLICYAUTHORIZENV *in,
        json_object **jso);

TSS2_RC
ifapi_json_TPMS_POLICYACTION_serialize(const TPMS_POLICYACTION *in,
                                       json_object **jso);

TSS2_RC
ifapi_json_TPMS_PCRVALUE_serialize(const TPMS_PCRVALUE *in, json_object **jso);

TSS2_RC
ifapi_json_TPML_PCRVALUES_serialize(const TPML_PCRVALUES *in,
                                    json_object **jso);

TSS2_RC
ifapi_json_TPMS_POLICYPCR_serialize(const TPMS_POLICYPCR *in,
                                    json_object **jso);

TSS2_RC
ifapi_json_TPMS_POLICYAUTHORIZATION_serialize(const TPMS_POLICYAUTHORIZATION
        *in, json_object **jso);

TSS2_RC
ifapi_json_TPML_POLICYAUTHORIZATIONS_serialize(const TPML_POLICYAUTHORIZATIONS
        *in, json_object **jso);

TSS2_RC
ifapi_json_TPMS_POLICYBRANCH_serialize(const TPMS_POLICYBRANCH *in,
                                       json_object **jso);

TSS2_RC
ifapi_json_TPML_POLICYBRANCHES_serialize(const TPML_POLICYBRANCHES *in,
        json_object **jso);

TSS2_RC
ifapi_json_TPMS_POLICYOR_serialize(const TPMS_POLICYOR *in, json_object **jso);

TSS2_RC
ifapi_json_TPMU_POLICYELEMENT_serialize(const TPMU_POLICYELEMENT *in,
                                        UINT32 selector, json_object **jso);

TSS2_RC
ifapi_json_TPMT_POLICYELEMENT_serialize(const TPMT_POLICYELEMENT *in,
                                        json_object **jso);

TSS2_RC
ifapi_json_TPML_POLICYELEMENTS_serialize(const TPML_POLICYELEMENTS *in,
        json_object **jso);

TSS2_RC
ifapi_json_TPMS_POLICY_serialize(const TPMS_POLICY *in,
        json_object **jso);

#endif /* IFAPI_POLICY_JSON_SERIALIZE_H */
