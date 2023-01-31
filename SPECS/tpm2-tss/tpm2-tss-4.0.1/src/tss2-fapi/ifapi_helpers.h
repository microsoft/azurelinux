/* SPDX-License-Identifier: BSD-2-Clause */
/*******************************************************************************
 * Copyright 2018-2019, Fraunhofer SIT sponsored by Infineon Technologies AG
 * All rights reserved.
 *******************************************************************************/
#ifndef IFAPI_HELPERS_H
#define IFAPI_HELPERS_H

#include <stdint.h>
#include <stdarg.h>
#include <stdbool.h>
#include <sys/stat.h>
#include <json-c/json.h>
#include <json-c/json_util.h>

#include "tss2_esys.h"
#include "tss2_fapi.h"
#include "fapi_int.h"

TSS2_RC
ifapi_create_dirs(const char *supdir, const char *path);

TSS2_RC
ifapi_set_key_flags(const char *type, bool policy, IFAPI_KEY_TEMPLATE *template);

TSS2_RC
ifapi_set_nv_flags(const char *type, IFAPI_NV_TEMPLATE *template,
                   const char *policy);

bool
ifapi_path_type_p(const char *path, const char *type);

ESYS_TR
ifapi_get_hierary_handle(const char *path);

bool
ifapi_null_primary_p(const char *path);

bool
ifapi_hierarchy_path_p(const char *path);

bool
ifapi_TPMT_PUBLIC_cmp(TPMT_PUBLIC *in1, TPMT_PUBLIC *in2);

void
ifapi_init_hierarchy_object(
    IFAPI_OBJECT *hierarchy,
    ESYS_TR esys_handle);

TSS2_RC
ifapi_set_name_hierarchy_object(
    IFAPI_OBJECT *hierarchy);

char *
get_description(IFAPI_OBJECT *object);

size_t
ifapi_path_length(NODE_STR_T *node);

void
ifapi_free_object_list(NODE_OBJECT_T *node);

void
ifapi_free_node_list(NODE_OBJECT_T *node);

TSS2_RC
ifapi_path_string(char **dest, const char *supdir, NODE_STR_T *node, char *name);

TSS2_RC
ifapi_path_string_n(
    char **dest,
    const char *supdir,
    NODE_STR_T *node,
    char *name,
    size_t n);

TSS2_RC
ifapi_asprintf(char **str, const char *fmt, ...);

NODE_STR_T *
split_string(const char *string, char *delimiter);

NODE_STR_T *
init_string_list(const char *string);

bool
add_string_to_list(NODE_STR_T *str_list, char *string);

void
free_string_list(NODE_STR_T *node);

void
ifapi_cleanup_policy(
    TPMS_POLICY *policy);

TPMS_POLICY *
ifapi_copy_policy(
    const TPMS_POLICY *from_policy);

TSS2_RC
ifapi_get_name(
    TPMT_PUBLIC *publicInfo,
    TPM2B_NAME *name);

TSS2_RC
ifapi_nv_get_name(
    TPMS_NV_PUBLIC *publicInfo,
    TPM2B_NAME *name);

TSS2_RC
ifapi_object_cmp_name(
    IFAPI_OBJECT *object,
    void *name,
    bool *equal);

TSS2_RC
ifapi_object_cmp_nv_public(
    IFAPI_OBJECT *object,
    void *nv_public,
    bool *equal);

TSS2_RC
ifapi_tpm_to_fapi_signature(
    IFAPI_OBJECT *sig_key_object,
    TPMT_SIGNATURE *tpm_signature,
    uint8_t **signature,
    size_t *signatureSize);

TSS2_RC
ifapi_compute_quote_info(
    IFAPI_OBJECT *sig_key_object,
    TPM2B_ATTEST *tpm_quoted,
    char **quoteInfo);

TSS2_RC
ifapi_get_quote_info(
    char const *quoteInfo,
    TPM2B_ATTEST *tpm_quoted,
    FAPI_QUOTE_INFO *fapi_quote_ingo);

TSS2_RC
push_object_to_list(void *object, NODE_OBJECT_T **object_list);

TSS2_RC
append_object_to_list(void *object, NODE_OBJECT_T **object_list);

bool
object_with_auth(IFAPI_OBJECT *object);

TSS2_RC
ifapi_get_nv_start_index(const char *path, TPM2_HANDLE *start_nv_index);

TSS2_RC
ifapi_check_nv_index(const char *path, TPM2_HANDLE nv_index);

TSS2_RC
ifapi_check_profile_pcr_selection(
    const TPML_PCR_SELECTION *pcr_profile,
    const TPML_PCR_SELECTION *pcr_capablity);

TSS2_RC
ifapi_filter_pcr_selection_by_index(
    TPML_PCR_SELECTION *pcr_selection,
    const TPM2_HANDLE *pcr_index,
    size_t pcr_count);

TSS2_RC ifapi_calculate_pcr_digest(
    json_object *jso_event_list,
    const FAPI_QUOTE_INFO *quote_info,
    TPM2B_DIGEST *pcr_digest);

TSS2_RC
ifapi_compute_policy_digest(
    TPML_PCRVALUES *pcrs,
    TPML_PCR_SELECTION *pcr_selection,
    TPMI_ALG_HASH hash_alg,
    TPM2B_DIGEST *pcr_digest);

bool
ifapi_cmp_public_key(
    TPM2B_PUBLIC *key1,
    TPM2B_PUBLIC *key2);

void
ifapi_check_json_object_fields(
    json_object *jso,
    char** field_tab,
    size_t size_of_tab);

TSS2_RC
ifapi_extend_pcr(
    TPMI_ALG_HASH alg,
    uint8_t *pcr,
    const uint8_t *digest,
    size_t alg_size);

TSS2_RC ifapi_pcr_selection_to_pcrvalues(
        TPML_PCR_SELECTION *pcr_selection,
        TPML_DIGEST *pcr_digests,
        TPML_PCRVALUES **out);

void
ifapi_helper_init_policy_pcr_selections(
        TSS2_POLICY_PCR_SELECTION *s,
        TPMT_POLICYELEMENT *pol_element);

#endif /* IFAPI_HELPERS_H */
