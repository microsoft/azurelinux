/* SPDX-License-Identifier: BSD-2-Clause */
/***********************************************************************
 * Copyright 2017-2018, Fraunhofer SIT sponsored by Infineon Technologies AG
 * Copyright (c) 2017-2018, Intel Corporation
 *
 * All rights reserved.
 ***********************************************************************/
#ifdef HAVE_CONFIG_H
#include <config.h>
#endif
#include <assert.h>
#include <json-c/json.h>
#include <json-c/json_util.h>
#include <string.h>
#include <stdbool.h>
#include <stdio.h>
#include "tss2_fapi.h"

#define EXIT_SKIP 77
#define EXIT_ERROR 99

#define ASSERT_SIZE 10 /* sanity check value for string outputs of Fapi commands  */


#define ASSERT(EXPR)                          \
    if (!(EXPR)) { \
        LOG_ERROR("Failed assertion: " #EXPR);              \
        goto error; \
    }

/*
 * Based on a list of keys (FIELD_LIST) a json sub object of the
 * json object represented by JSON_STRING will be determined.
 * If an json array is part of the list of sub objects an element
 * of the array can be selected by a value from '0' to '9'.
 * If SUBSTRING is "" the check is ok if the sub object was found.
 * Otherwise it will be checked whether SUBSTRING does occur
 * in the string representing the sub object.
 */
#define CHECK_JSON_FIELDS(JSON_STRING, FIELD_LIST, SUBSTRING, LABEL)    \
   { \
        json_object *jso = NULL; \
        json_object *jso1 = NULL; \
        json_object *jso2 = NULL; \
        size_t i, n; \
        n = sizeof(FIELD_LIST) / sizeof(FIELD_LIST[0]); \
        jso = json_tokener_parse(JSON_STRING); \
        if (!jso) { \
            LOG_ERROR("Invalid JSON"); \
            goto error; \
        } \
        jso1 = jso; \
        for (i = 0; i < n; i++) { \
            if (strlen(FIELD_LIST[i]) == 1 && \
                FIELD_LIST[i][0] >= '0' && FIELD_LIST[i][0] <= '9') { \
                jso2 = json_object_array_get_idx(jso1, FIELD_LIST[i][0]  - '0'); \
                ASSERT(jso2); \
            } \
            else if (!jso1 || !json_object_object_get_ex(jso1, FIELD_LIST[i],  &jso2)) { \
                json_object_put(jso); \
                LOG_ERROR("%s not found.", FIELD_LIST[i]); \
                goto error; \
            } \
            jso1 = jso2; \
        } \
        if (strlen(SUBSTRING) > 0 && !strstr( json_object_get_string(jso1), SUBSTRING)) { \
            json_object_put(jso); \
            LOG_ERROR("Sub string %s not found.", SUBSTRING); \
            goto error; \
        } \
        json_object_put(jso); \
    }

/* It will be checked whether two json objects are equal. */
#define CHECK_JSON(JSON1, JSON2, LABEL) \
        { \
            json_object *jso1 = NULL; \
            json_object *jso2 = NULL; \
            jso1 = json_tokener_parse(JSON1) ; \
            ASSERT(jso1) ; \
            if (!jso1) { \
                LOG_ERROR("Invalid JSON") ;\
                goto LABEL ;\
            }                                        \
            jso2 = json_tokener_parse(JSON2) ;\
            ASSERT(jso2) ;\
            if (!jso2) { \
                LOG_ERROR("Invalid JSON") ;\
                goto LABEL ;\
            }                                        \
            if (!cmp_jso(jso1, jso2)) { \
                json_object_put(jso1) ; \
                json_object_put(jso2) ; \
                goto LABEL; \
            } \
            json_object_put(jso1); \
            json_object_put(jso2); \
        }

/* It will be checked whether a json object is included in a list
   of json objects. */
#define CHECK_JSON_LIST(LIST, JSO_STRING, LABEL) \
    { \
        size_t i, n; \
        n = sizeof(LIST) / sizeof(LIST[0]); \
        json_object *jso1 = json_tokener_parse(JSO_STRING); \
        ASSERT(jso1); \
        json_object *jso2 = NULL; \
        for (i = 0; i < n; i++) { \
             jso2 = json_tokener_parse(LIST[i]); \
             ASSERT(jso2); \
             if (cmp_jso(jso1, jso2)) { \
                break; \
             } \
             json_object_put(jso2); \
        } \
        if (i >=  n) { \
            json_object_put(jso1); \
            LOG_ERROR("Mismatch" ); \
            goto LABEL; \
        } \
       json_object_put(jso1); \
       json_object_put(jso2); \
    }

#define goto_error_if_not_failed(rc,msg,label)                          \
    if (rc == TSS2_RC_SUCCESS) {                                        \
        LOG_ERROR("Error %s (%x) in Line %i: \n", msg, __LINE__, rc);   \
        goto label; }

#ifndef FAPI_PROFILE
#define FAPI_PROFILE DEFAULT_TEST_FAPI_PROFILE
#endif /* FAPI_PROFILE */

/* This variable is set to the same value in order to allow usage in if-statements etc. */
extern char *fapi_profile;

#define FAPI_POLICIES TOP_SOURCEDIR "/test/data/fapi"

TSS2_RC
pcr_extend(FAPI_CONTEXT *context, UINT32 pcr, TPML_DIGEST_VALUES *digest_values);

TSS2_RC
pcr_reset(FAPI_CONTEXT *context, UINT32 pcr);

bool cmp_strtokens(char* string1, char *string2, char *delimiter);

char * normalize_string(const char *string);

bool cmp_jso(json_object *jso1, json_object *jso2);

/*
 * This is the prototype for all integration tests in the tpm2-tss
 * project. Integration tests are intended to exercise the combined
 * components in the software stack. This typically means executing some
 * SAPI function using the socket TCTI to communicate with a software
 * TPM2 simulator.
 * Return values:
 * A successful test will return 0, any other value indicates failure.
 */


int test_invoke_fapi(FAPI_CONTEXT * fapi_context);

int init_fapi(char *fapi_profile, FAPI_CONTEXT **fapi_context);
