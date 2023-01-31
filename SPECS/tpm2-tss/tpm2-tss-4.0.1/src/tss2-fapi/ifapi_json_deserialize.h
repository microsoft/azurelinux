/* SPDX-License-Identifier: BSD-2-Clause */
/*******************************************************************************
 * Copyright 2018-2019, Fraunhofer SIT sponsored by Infineon Technologies AG
 * All rights reserved.
 ******************************************************************************/
#ifndef IFAPI_JSON_DESERIALIZE_H
#define IFAPI_JSON_DESERIALIZE_H

#include <stdbool.h>
#include <json-c/json.h>
#include <json-c/json_util.h>

#include "tss2_tpm2_types.h"
#include "ifapi_keystore.h"
#include "fapi_int.h"
#include "ifapi_eventlog_system.h"

#define YES 1
#define NO 0

#define GET_OPTIONAL(name, json_name, type) \
    if (!ifapi_get_sub_object(jso, json_name, &jso2)) { \
        memset(&out->name, 0, sizeof(type)); \
    } else { \
        r =  ifapi_json_ ## type ## _deserialize (jso2, &out->name); \
        return_if_error2(r, "Bad value for field \"%s\".", json_name);  \
    }


/*
 * Deserialize an embedded structure of an complex TPM2B.
 * To achieve backward compatibility both JSON representations, of the complex
 * TPM2B, and of the embedded structure will be allowed.
 */
#define GET_CONDITIONAL_TPM2B(name, json_name, tpm2b_type, type, field_name, cond_cnt) \
    if (!ifapi_get_sub_object(jso, json_name, &jso2)) { \
        memset(&out->name, 0, sizeof(type)); \
    } else { \
        cond_cnt++; \
        json_object* jso_size; \
        if (ifapi_get_sub_object(jso2, "size", &jso_size)) { \
            tpm2b_type tmp = { 0 }; \
            r =  ifapi_json_ ## tpm2b_type ## _deserialize (jso2, &tmp); \
            return_if_error2(r, "Bad value for field \"%s\".", json_name); \
            out->name = tmp.field_name; \
        } else { \
            r =  ifapi_json_ ## type ## _deserialize (jso2, &out->name); \
            return_if_error2(r, "Bad value for field \"%s\".", json_name); \
        } \
    }

bool
ifapi_get_sub_object(json_object *jso, char *name, json_object **sub_jso);

TSS2_RC
ifapi_json_char_deserialize(json_object *jso, char **out);

TSS2_RC
ifapi_json_IFAPI_KEY_deserialize(json_object *jso, IFAPI_KEY *out);

TSS2_RC
ifapi_json_import_IFAPI_KEY_deserialize(json_object *jso, IFAPI_KEY *out);

TSS2_RC
ifapi_json_IFAPI_EXT_PUB_KEY_deserialize(json_object *jso,
        IFAPI_EXT_PUB_KEY *out);

TSS2_RC
ifapi_json_IFAPI_NV_deserialize(json_object *jso, IFAPI_NV *out);

TSS2_RC
ifapi_json_IFAPI_HIERARCHY_deserialize(json_object *jso,  IFAPI_HIERARCHY *out);

TSS2_RC
ifapi_json_IFAPI_OBJECT_deserialize(json_object *jso, IFAPI_OBJECT *out);

TSS2_RC
ifapi_json_FAPI_QUOTE_INFO_deserialize(json_object *jso, FAPI_QUOTE_INFO *out);

TSS2_RC
ifapi_json_IFAPI_EVENT_TYPE_deserialize(json_object *jso,
                                        IFAPI_EVENT_TYPE *out);

TSS2_RC
ifapi_json_IFAPI_EVENT_TYPE_deserialize_txt(json_object *jso,
        IFAPI_EVENT_TYPE *out);

TSS2_RC
ifapi_json_IFAPI_TSS_EVENT_deserialize(json_object *jso,
                                       IFAPI_TSS_EVENT *out);

TSS2_RC
ifapi_json_IFAPI_EVENT_UNION_deserialize(
    UINT32 selector,
    json_object *jso,
    IFAPI_EVENT_UNION *out,
    bool *verify);

enum IFAPI_EVENT_ERROR_HANDLING {
    DIGEST_CHECK_WARNING = 0,
    DIGEST_CHECK_ERROR,
    DO_NOT_CHECK_DIGEST
};

TSS2_RC
ifapi_json_IFAPI_EVENT_deserialize(json_object *jso, IFAPI_EVENT *out,
                                   enum IFAPI_EVENT_ERROR_HANDLING error_handling);

TSS2_RC
ifapi_json_TPMS_EVENT_CELMGT_deserialize(json_object *jso,  TPMS_EVENT_CELMGT *out);

#endif /* IFAPI_JSON_DESERIALIZE_H */
