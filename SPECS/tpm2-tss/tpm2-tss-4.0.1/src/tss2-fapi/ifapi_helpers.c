/* SPDX-License-Identifier: BSD-2-Clause */
/*******************************************************************************
 * Copyright 2018-2019, Fraunhofer SIT sponsored by Infineon Technologies AG
 * All rights reserved.
 *******************************************************************************/

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <stdio.h>
#include <string.h>
#include <stdarg.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <ctype.h>
#include <dirent.h>

#include "tss2_mu.h"
#include "fapi_util.h"
#include "fapi_policy.h"
#include "fapi_crypto.h"
#include "ifapi_helpers.h"
#include "ifapi_json_serialize.h"
#include "ifapi_json_deserialize.h"
#include "tpm_json_deserialize.h"
#include "ifapi_eventlog.h"
#define LOGMODULE fapi
#include "util/log.h"
#include "util/aux_util.h"

/** Create template for key creation based on type flags.
 *
 * Based on passed flags the TPM2B_PUBLIC data which is used for key
 * creation will be adapted.
 *
 * @param[in] type The flags describing the key type.
 * @param[in] policy The flag whether a policy is used.
 * @param[out] template The template including the TPM2B_PUBLIC which will
 *             be used for key creation.
 * @retval TSS2_RC_SUCCESS if the template can be generated.
 * @retval TSS2_FAPI_RC_BAD_VALUE If an invalid combination of flags was used.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 */
TSS2_RC
ifapi_set_key_flags(const char *type, bool policy, IFAPI_KEY_TEMPLATE *template)
{
    TSS2_RC r = TSS2_RC_SUCCESS;
    char *type_dup = NULL;
    TPMA_OBJECT attributes = 0;
    UINT32 handle;
    int pos;
    bool exportable = false;

    memset(template, 0, sizeof(IFAPI_KEY_TEMPLATE));
    type_dup = strdup(type);
    return_if_null(type_dup, "Out of memory.", TSS2_FAPI_RC_MEMORY);

    char *saveptr;
    char *flag = strtok_r(type_dup, ", ", &saveptr);

    /* The default store will be the user directory */
    template->system = TPM2_NO;

    /* Loop over all comma or space separated flags */
    while (flag != NULL) {
        if (strcasecmp(flag, "system") == 0) {
            template->system = TPM2_YES;
        } else if (strcasecmp(flag, "sign") == 0) {
            attributes |= TPMA_OBJECT_SIGN_ENCRYPT;
        } else if (strcasecmp(flag, "user") == 0) {
	    attributes |= TPMA_OBJECT_USERWITHAUTH;
        } else if (strcasecmp(flag, "decrypt") == 0) {
            attributes |= TPMA_OBJECT_DECRYPT;
        } else if (strcasecmp(flag, "restricted") == 0) {
            attributes |= TPMA_OBJECT_RESTRICTED;
        } else if (strcasecmp(flag, "exportable") == 0) {
            /* TPMA_OBJECT_ENCRYPTEDDUPLICATION will not be set because no inner
               symmetric encryption will be used */
            exportable = true;
        } else if (strcasecmp(flag, "noda") == 0) {
            attributes |= TPMA_OBJECT_NODA;
        } else if (strncmp(flag, "0x", 2) == 0) {
            sscanf(&flag[2], "%"SCNx32 "%n", &handle, &pos);
            if ((size_t)pos != strlen(flag) - 2) {
                goto_error(r, TSS2_FAPI_RC_BAD_VALUE, "Invalid flag: %s",
                           error, flag);
            }
            template->persistent_handle = handle;
            template->persistent = TPM2_YES;
        } else {
            goto_error(r, TSS2_FAPI_RC_BAD_VALUE, "Invalid flag: %s",
                       error, flag);
        }
        flag = strtok_r(NULL, " ,", &saveptr);
    }
    if (exportable) {
        /* Clear flags preventing duplication */
        attributes &= ~TPMA_OBJECT_FIXEDTPM;
        attributes &= ~TPMA_OBJECT_FIXEDPARENT;
    } else {
        attributes |= TPMA_OBJECT_FIXEDTPM;
        attributes |= TPMA_OBJECT_FIXEDPARENT;
    }
    /* Set default flags */
    attributes |= TPMA_OBJECT_SENSITIVEDATAORIGIN;
    if (!policy)
        attributes |= TPMA_OBJECT_USERWITHAUTH;
    else
        attributes |= TPMA_OBJECT_ADMINWITHPOLICY;

    /* Check whether flags are appropriate for restricted keys */
    if (attributes & TPMA_OBJECT_RESTRICTED &&
        ((attributes & TPMA_OBJECT_SIGN_ENCRYPT &&
          attributes & TPMA_OBJECT_DECRYPT)
         || (!(attributes & TPMA_OBJECT_SIGN_ENCRYPT) &&
             !(attributes & TPMA_OBJECT_DECRYPT)))) {
        goto_error(r, TSS2_FAPI_RC_BAD_VALUE,
                   "Exactly either sign or decrypt must be set.",
                   error);
    }

    template->public.publicArea.objectAttributes = attributes;
    SAFE_FREE(type_dup);
    return TSS2_RC_SUCCESS;

error:
    SAFE_FREE(type_dup);
    return r;
}

/** Create template for nv object  creation based on type flags.
 *
 * Based on passed flags the TPM2B_NV_PUBLIC data which is used for key
 * creation will be adapted.
 * @param[in] type The flags describing the nv object type.
 * @param[in] policy The flag whether a policy is used.
 * @param[out] template The template including the TPM2B_NV_PUBLIC which will
 *             be used for nv object creation.
 * @retval TSS2_RC_SUCCESS if the template can be generated.
 * @retval TSS2_FAPI_RC_BAD_VALUE If an invalid combination of flags was used.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 */
TSS2_RC
ifapi_set_nv_flags(const char *type, IFAPI_NV_TEMPLATE *template,
                   const char *policy)
{
    TSS2_RC r = TSS2_RC_SUCCESS;
    char *type_dup = NULL;
    TPMA_NV attributes = 0;
    UINT32 handle;
    int pos;
    UINT32 size = 0;
    size_t type_count = 0;

    memset(template, 0, sizeof(IFAPI_NV_TEMPLATE));
    type_dup = strdup(type);
    return_if_null(type_dup, "Out of memory.", TSS2_FAPI_RC_MEMORY);
    /* The default store will be the user directory */
    template->system = TPM2_NO;

    char *saveptr;
    char *flag = strtok_r(type_dup, ", ", &saveptr);

    /* Loop over all comma or space separated flags */
    while (flag != NULL) {
        if (strcasecmp(flag, "system") == 0) {
            template->system = TPM2_YES;
        } else if (strcasecmp(flag, "bitfield") == 0) {
            attributes |= TPM2_NT_BITS << TPMA_NV_TPM2_NT_SHIFT;
            type_count += 1;
        } else if (strcasecmp(flag, "counter") == 0) {
            attributes |= TPM2_NT_COUNTER << TPMA_NV_TPM2_NT_SHIFT;
            type_count += 1;
        } else if (strcasecmp(flag, "pcr") == 0) {
            attributes |= TPM2_NT_EXTEND << TPMA_NV_TPM2_NT_SHIFT;
            type_count += 1;
        } else if (strcasecmp(flag, "noda") == 0) {
            attributes |= TPMA_NV_NO_DA;
        } else if (strncmp(flag, "0x", 2) == 0) {
            sscanf(&flag[2], "%"SCNx32 "%n", &handle, &pos);
            if ((size_t)pos != strlen(flag) - 2) {
                goto_error(r, TSS2_FAPI_RC_BAD_VALUE, "Invalid flag: %s",
                           error, flag);
            }
            template->public.nvIndex = handle;
        } else {
            goto_error(r, TSS2_FAPI_RC_BAD_VALUE, "Invalid flag: %s",
                       error, flag);
        }
        flag = strtok_r(NULL, " ,", &saveptr);
    }
    if (type_count > 1) {
        goto_error(r, TSS2_FAPI_RC_BAD_VALUE,
                   "Only one type of NV object can be set.", error);
    }
    if (type_count == 0) {
        /* Normal NV space will be defined */
        attributes |= TPM2_NT_ORDINARY << TPMA_NV_TPM2_NT_SHIFT;
        if (size == 0)
            size = 64;
    }
    /* If type extend is used the size will be set during the merging of the crypto
       profile depending on the nameHashAlg stored in the profile.
       The size of counter and bitfield will be determined by the TPM. */

    if (policy && strlen(policy) > 0) {
        attributes |= TPMA_NV_POLICYWRITE;
        attributes |= TPMA_NV_POLICYREAD;
    } else {
        attributes |= TPMA_NV_AUTHREAD;
        attributes |= TPMA_NV_AUTHWRITE;
    }

    attributes |= TPMA_NV_READ_STCLEAR;
    attributes |= TPMA_NV_WRITE_STCLEAR;
    template->public.attributes = attributes;
    template->hierarchy = TPM2_RH_OWNER;
    template->public.dataSize = size;

    SAFE_FREE(type_dup);
    return TSS2_RC_SUCCESS;

error:
    SAFE_FREE(type_dup);
    return r;
}

/**  Determine whether path is of certain type.
 *
 * @param[in] path The path to be checked.
 * @param[in] type sub-string at the beginning of the path to be checked.
 *
 * @retval true if the path name starts with type.
 * @retval false if not.
 */
bool
ifapi_path_type_p(const char *path, const char *type)
{
    size_t pos = 0;
    char *end;
    int end_pos;

    if (strncmp("/", path, 1) == 0)
        pos = 1;
    if (strcmp(&path[pos], type) == 0)
        return true;

    end = strchr(&path[pos], IFAPI_FILE_DELIM_CHAR);
    if (!end)
        /* No meaningful path */
        return false;
    end_pos = (int)(end - path);

    /* Check sub-string and following delimiter. */
    if (strlen(path) - pos >= 3 &&
            strncasecmp(type, &path[pos], strlen(type)) == 0 && end &&
            strncmp(IFAPI_FILE_DELIM, &path[end_pos], 1) == 0)
        return true;
    return false;
}

/** Get ESYS handle for a hierarchy path.
 *
 * @param[in] path The path to be checked.
 *
 * @retval The ESAPI handle for the hierarchy defined in path.
 * @retval 0 if not handle can be assigned.
 */
ESYS_TR
ifapi_get_hierary_handle(const char *path)
{
    int pos = 0;

    if (strncmp("/", path, 1) == 0)
        pos = 1;
    if (strcmp(&path[pos], "HE") == 0) {
        return ESYS_TR_RH_ENDORSEMENT;
    }
    if (strcmp(&path[pos], "HS") == 0) {
        return ESYS_TR_RH_OWNER;
    }
    if (strcmp(&path[pos], "HN") == 0) {
        return  ESYS_TR_RH_NULL ;
    }
    if (strcmp(&path[pos], "LOCKOUT") == 0) {
        return ESYS_TR_RH_LOCKOUT;
    }
    return 0;
}

/** Determine whether path is a primary in the null hierarchy.
 *
 * @param[in] path The path to be checked.
 *
 * @retval true if the path describes a null hierarchy primary.
 * @retval false if not.
 */
bool
ifapi_null_primary_p(const char *path)
{
    size_t pos1 = 0;
    size_t pos2 = 0;
    char *start;

    if (strncmp("/", path, 1) == 0)
        pos1 = 1;
    /* Skip profile if it does exist in path */
    if (strncmp("P_", &path[pos1], 2) == 0) {
        start = strchr(&path[pos1], IFAPI_FILE_DELIM_CHAR);
        if (start) {
            pos2 = (int)(start - &path[pos1]);
            if (strncmp("/", &path[pos1 + pos2], 1) == 0)
                pos2 += 1;
            if (strncmp("/", &path[pos1 + pos2], 1) == 0)
                pos2 += 1;
        }
    }
    /* Check whether there is only one name after the hiearchy. */
    if (strncasecmp(&path[pos1 + pos2], "HN/", 3) == 0 &&
        !strchr(&path[pos1 + pos2 + 3], IFAPI_FILE_DELIM_CHAR)) {
        return true;
    } else {
        return false;
    }
}

/** Determine whether path describes a hierarchy object.
 *
 * It will be checked whether the path describes a hierarch. A key path
 * with a hierarchy will not deliver true.
 *
 * @param[in] path The path to be checked.
 *
 * @retval true if the path describes a hierarchy.
 * @retval false if not.
 */
bool
ifapi_hierarchy_path_p(const char *path)
{
    size_t pos1 = 0;
    size_t pos2 = 0;
    char *start;

    if (strncmp("/", path, 1) == 0)
        pos1 = 1;
    /* Skip profile if it does exist in path */
    if (strncmp("P_", &path[pos1], 2) == 0) {
        start = strchr(&path[pos1], IFAPI_FILE_DELIM_CHAR);
        if (start) {
            pos2 = (int)(start - &path[pos1]);
            if (strncmp("/", &path[pos1 + pos2], 1) == 0)
                pos2 += 1;
            if (strncmp("/", &path[pos1 + pos2], 1) == 0)
                pos2 += 1;
        }
    }
    /* Check whether only hierarchy is specified in path */
    if ((strncasecmp(&path[pos1 + pos2], "HS", 2) == 0 ||
         strncasecmp(&path[pos1 + pos2], "HE", 2) == 0 ||
         strncasecmp(&path[pos1 + pos2], "HN", 2) == 0)
        && (strlen(path) == pos1 + pos2 + 2 ||
            (strlen(path) == pos1 + pos2 + 3 &&
             path[pos1 + pos2 + 2] == IFAPI_FILE_DELIM_CHAR))){
        return true;
    } else if (strncasecmp(&path[pos1 + pos2], "LOCKOUT", 7) == 0
               && (strlen(path) == pos1 + pos2 + 7 ||
                   (strlen(path) == pos1 + pos2 + 8 &&
                    path[pos1 + pos2 + 7] == IFAPI_FILE_DELIM_CHAR))) {
        return true;
    }
    return false;
}

/** Compare two variables of type TPM2B_ECC_PARAMETER.
 *
 * @param[in] in1 variable to be compared with in2.
 * @param[in] in2 variable to be compared with in1.
 *
 * @retval true if the variables are equal.
 * @retval false if not.
 */
bool
ifapi_TPM2B_ECC_PARAMETER_cmp(TPM2B_ECC_PARAMETER *in1,
                              TPM2B_ECC_PARAMETER *in2)
{

    if (in1->size != in2->size)
        return false;

    return memcmp(&in1->buffer[0], &in2->buffer[0], in1->size) == 0;
}

/** Compare two variables of type TPMS_ECC_POINT.
 *
 * @param[in] in1 variable to be compared with in2.
 * @param[in] in2 variable to be compared with in1.
 *
 * @retval true if the variables are equal.
 * @retval false if not.
 */
bool
ifapi_TPMS_ECC_POINT_cmp(TPMS_ECC_POINT *in1, TPMS_ECC_POINT *in2)
{
    LOG_TRACE("call");

    if (!ifapi_TPM2B_ECC_PARAMETER_cmp(&in1->x, &in2->x))
        return false;

    if (!ifapi_TPM2B_ECC_PARAMETER_cmp(&in1->y, &in2->y))
        return false;

    return true;
}

/**  Compare two variables of type TPM2B_DIGEST.
 *
 * @param[in] in1 variable to be compared with in2.
 * @param[in] in2 variable to be compared with in1.
 *
 * @retval true if the variables are equal.
 * @retval false if not.
 */
bool
ifapi_TPM2B_DIGEST_cmp(TPM2B_DIGEST *in1, TPM2B_DIGEST *in2)
{

    if (in1->size != in2->size)
        return false;

    return memcmp(&in1->buffer[0], &in2->buffer[0], in1->size) == 0;
}

/** Compare two variables of type TPM2B_PUBLIC_KEY_RSA.
 *
 * @param[in] in1 variable to be compared with in2
 * @param[in] in2 variable to be compared with in1
 *
 * @retval true if the variables are equal.
 * @retval false if not.
 */
bool
ifapi_TPM2B_PUBLIC_KEY_RSA_cmp(TPM2B_PUBLIC_KEY_RSA *in1,
                               TPM2B_PUBLIC_KEY_RSA *in2)
{

    if (in1->size != in2->size)
        return false;

    return memcmp(&in1->buffer[0], &in2->buffer[0], in1->size) == 0;
}

/**  Compare two variables of type TPMU_PUBLIC_ID.
 *
 * @param[in] in1 variable to be compared with in2.
 * @param[in] selector1 key type of first key.
 * @param[in] in2 variable to be compared with in1.
 * @param[in] selector2 key type of second key.
 *
 * @result true if variables are equal.
 * @result false if not.
 */
bool
ifapi_TPMU_PUBLIC_ID_cmp(TPMU_PUBLIC_ID *in1, UINT32 selector1,
                         TPMU_PUBLIC_ID *in2, UINT32 selector2)
{

    if (selector1 != selector2)
        return false;

    switch (selector1) {
    case TPM2_ALG_KEYEDHASH:
        if (!ifapi_TPM2B_DIGEST_cmp(&in1->keyedHash, &in2->keyedHash))
            return false;
        break;
    case TPM2_ALG_SYMCIPHER:
        if (!ifapi_TPM2B_DIGEST_cmp(&in1->sym, &in2->sym))
            return false;
        break;
    case TPM2_ALG_RSA:
        if (!ifapi_TPM2B_PUBLIC_KEY_RSA_cmp(&in1->rsa, &in2->rsa))
            return false;
        break;
    case TPM2_ALG_ECC:
        if (!ifapi_TPMS_ECC_POINT_cmp(&in1->ecc, &in2->ecc))
            return false;
        break;
    default:
        return false;
    };
    return true;
}

/**
 * Compare the PUBLIC_ID stored in two  TPMT_PUBLIC structures.
 * @param[in] in1 the public data with the unique data to be compared with:
 * @param[in] in2
 *
 * @retval true if the variables are equal.
 * @retval false if not.
 */
bool
ifapi_TPMT_PUBLIC_cmp(TPMT_PUBLIC *in1, TPMT_PUBLIC *in2)
{

    if (!ifapi_TPMU_PUBLIC_ID_cmp(&in1->unique, in1->type, &in2->unique, in2->type))
        return false;

    return true;
}

/** Print to allocated string.
 *
 * A list of parameters will be printed to an allocated string according to the
 * format description in the first parameter.
 *
 * @param[out] str The allocated output string.
 * @param[in] fmt The format string (printf formats can be used.)
 * @param[in] args The list of objects to be printed.
 *
 * @retval int The size of the string ff the printing was successful.
 * @retval -1 if not enough memory can be allocated.
 */
int
vasprintf(char **str, const char *fmt, va_list args)
{
    int size = 0;
    va_list tmpa;
    char *dmy = NULL;
    va_copy(tmpa, args);
    size = vsnprintf(dmy, size, fmt, tmpa);
    va_end(tmpa);
    if (size < 0) {
        return -1;
    }
    *str = (char *) malloc(size + 1);
    if (NULL == *str) {
        return -1;
    }
    size = vsprintf(*str, fmt, args);
    return size;
}

/** Print to allocated string.
 *
 * A list of parameters will be printed to an allocated string according to the
 * format description in the first parameter.
 *
 * @param[out] str The allocated output string.
 * @param[in] fmt The format string (printf formats can be used.)
 * @param[in] ... The list of objects to be printed.
 *
 * @retval TSS2_RC_SUCCESS If the printing was successful.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 */
TSS2_RC
ifapi_asprintf(char **str, const char *fmt, ...)
{
    int size = 0;
    va_list args;
    va_start(args, fmt);
    size = vasprintf(str, fmt, args);
    va_end(args);
    if (size == -1)
        return TSS2_FAPI_RC_MEMORY;
    return TSS2_RC_SUCCESS;
}

/** Divides str into substrings based on a delimiter.
 *
 * @param[in] string the string to split.
 * @param[in] delimiter the delimiter.
 *
 * @retval The linked list of substrings.
 * @retval NULL if the list cannot be created.
 */
NODE_STR_T *
split_string(const char *string, char *delimiter)
{
    NODE_STR_T *node = NULL;
    NODE_STR_T *start_node = NULL;
    char *strtok_save = NULL;
    char *stringdup = NULL;
    char *substr = NULL;
    if (string == NULL)
        return NULL;

    stringdup = strdup(string);
    if (stringdup == NULL) {
        LOG_ERROR("%s", "Out of memory.");
        goto error_cleanup;
    }
    char *stringdup_tokenized = strtok_r(stringdup, delimiter, &strtok_save);
    if (stringdup_tokenized != NULL) {
        substr = strdup(stringdup_tokenized);
    } else {
        substr = strdup(stringdup);
    }
    if (substr == NULL) {
        LOG_ERROR("%s", "Out of memory.");
        goto error_cleanup;
    }
    do {
        if (node == NULL) {
            node = malloc(sizeof(NODE_STR_T));
            if (node == NULL) {
                LOG_ERROR("%s", "Out of memory.");
                goto error_cleanup;
            }
            node->next = NULL;
            node->free_string = true;
            start_node = node;
        } else {
            node->next = malloc(sizeof(NODE_STR_T));
            if (node->next == NULL) {
                LOG_ERROR("%s", "Out of memory.");
                goto error_cleanup;
            }
            node = node->next;
            node->next = NULL;
            node->free_string = true;
        }
        node->str = substr;
        substr = strtok_r(NULL, delimiter, &strtok_save);
        if (substr) {
            substr = strdup(substr);
            if (substr == NULL) {
                LOG_ERROR("%s", "Out of memory.");
                goto error_cleanup;
            }
        }
    } while (substr != NULL);

    SAFE_FREE(stringdup);
    return start_node;
error_cleanup:
    SAFE_FREE(start_node);
    SAFE_FREE(substr);
    SAFE_FREE(stringdup);
    return NULL;
}

/** Free linked list of strings.
 *
 * @param[in] node the first node of the linked list.
 */
void
free_string_list(NODE_STR_T *node)
{
    NODE_STR_T *next;
    if (node == NULL)
        return;
    while (node != NULL) {
        if (node->free_string)
            free(node->str);
        next = node->next;
        free(node);
        node = next;
    }
}

/** Free linked list of IFAPI objects.
 *
 * @param[in] node the first node of the linked list.
 */
void
ifapi_free_object_list(NODE_OBJECT_T *node)
{
    NODE_OBJECT_T *next;
    if (node == NULL)
        return;
    while (node != NULL) {
        ifapi_cleanup_ifapi_object((IFAPI_OBJECT *)node->object);
        SAFE_FREE(node->object);
        next = node->next;
        free(node);
        node = next;
    }
}

/** Free linked list of IFAPI objects (link nodes only).
 *
 * @param[in] node the first node of the linked list.
 */
void
ifapi_free_node_list(NODE_OBJECT_T *node)
{
    NODE_OBJECT_T *next;
    if (node == NULL)
        return;
    while (node != NULL) {
        next = node->next;
        free(node);
        node = next;
    }
}

/** Compute the number on nodes in a linked list.
 *
 * @param[in] node the first node of the linked list.
 *
 * @retval the number on nodes.
 */
size_t
ifapi_path_length(NODE_STR_T *node)
{
    size_t length = 0;
    if (node == NULL)
        return 0;
    while (node != NULL) {
        length += 1;
        node = node->next;
    }
    return length;
}

/** Compute the size of a concatenated string.
 *
 * @param[in] node the first node of the linked string list.
 * @param[in] delim_length the size of the delimiter used for the concatenation.
 *
 * @retval the size of the string.
 */
static size_t
path_str_length(NODE_STR_T *node, int delim_length)
{
    size_t size = 0;
    if (node == NULL)
        return 0;
    while (node != NULL) {
        size += strlen(node->str);
        if (node->next != NULL)
            size = size + delim_length;
        node = node->next;
    }
    return size;
}

/** Compute a pathname based on a linked list of strings.
 *
 * @param[out] dest The pointer to the generated pathname (callee allocated).
 * @param[in]  supdir A sup directory will be the prefix of the pathname.
 * @param[in]  node The linked list.
 * @param[in]  name A name which is appended to the result if not NULL.
 *
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY if the memory for the pathname can't be allocated.
 */
TSS2_RC
ifapi_path_string(char **dest, const char *supdir, NODE_STR_T *node, char *name)
{
    size_t length = 1 + path_str_length(node,
                                        1) + ((supdir == NULL) ? 0 : strlen(supdir) + 1)
                    + ((name == NULL) ? 0 : strlen(name) + 1);
    *dest = malloc(length);
    if (*dest == NULL) {
        LOG_ERROR("Out of memory");
        return TSS2_FAPI_RC_MEMORY;
    }
    *dest[0] = '\0';
    if (supdir != NULL) {
        strcat(*dest, supdir);
        strcat(*dest, IFAPI_FILE_DELIM);
    }
    for (; node != NULL; node = node->next) {
        strcat(*dest, node->str);
        if (node->next != NULL) {
            strcat(*dest, IFAPI_FILE_DELIM);
        }
    }
    if (name != NULL) {
        strcat(*dest, IFAPI_FILE_DELIM);
        strcat(*dest, name);
    }
    return TSS2_RC_SUCCESS;
}


/** Compute a pathname based on the first n elements of a linked list of strings.
 *
 * @param[out] dest the pointer to the pathname (callee allocated).
 * @param[in]  supdir a sup directory will be the prefix of the pathname.
 *                    (can be NULL).
 * @param[in]  node the linked list.
 * @param[in]  name  the filename (can be NULL).
 * @param[in]  n the number of the first elements which will bes used for concatenation.
 * @retval TSS2_RC_SUCCESS if the function call was a success.
 * @retval TSS2_FAPI_RC_MEMORY if the memory for the pathname can't be allocated.
 */
TSS2_RC
ifapi_path_string_n(char **dest, const char *supdir, NODE_STR_T *node, char *name,
                    size_t n)
{
    size_t length = 1 + path_str_length(node,
                                        1) + ((supdir == NULL) ? 0 : strlen(supdir) + 1)
                    + ((name == NULL) ? 0 : strlen(name) + 1);
    *dest = malloc(length);
    size_t i;
    if (*dest == NULL) {
        LOG_ERROR("Out of memory");
        return TSS2_FAPI_RC_MEMORY;
    }
    *dest[0] = '\0';
    if (supdir != NULL) {
        strcat(*dest, supdir);
        strcat(*dest, IFAPI_FILE_DELIM);
    }
    for (i = 1; node != NULL && i <= n; i++, node = node->next) {
        strcat(*dest, node->str);
        if (node->next != NULL) {
            strcat(*dest, IFAPI_FILE_DELIM);
        }
    }
    if (name != NULL) {
        strcat(*dest, IFAPI_FILE_DELIM);
        strcat(*dest, name);
    }
    return TSS2_RC_SUCCESS;
}

/** Initialize a linked list of strings.
 *
 * free string in the list object will be set to true.
 * If the list will be extended by sub-string which are part
 * of this strin free_string has to be set to false.
 *
 * @param[in] string The string for the first element.
 *
 * @retval the initial node of the linked list.
 * @retval NULL if the list cannot be created.
 */
NODE_STR_T *
init_string_list(const char *string)
{
    NODE_STR_T *result = malloc(sizeof(NODE_STR_T));
    if (result == NULL)
        return NULL;
    result->next = NULL;
    result->str = strdup(string);
    if (result->str == NULL) {
        LOG_ERROR("Out of memory");
        free(result);
        return NULL;
    }
    result->free_string = true;
    return result;
}

/** Add string to the last element of a linked list of strings.
 *
 * A duplicate of the passed string will be added.
 *
 * @param[in,out] str_list The linked list.
 * @param[in] string The string to be added.
 *
 * @retval true if the string was added to the list.
 * @retval false if the list could not be extended.
 */
bool
add_string_to_list(NODE_STR_T *str_list, char *string)
{
    if (str_list == NULL)
        return NULL;
    NODE_STR_T *last = malloc(sizeof(NODE_STR_T));
    if (last == NULL)
        return false;
    while (str_list->next != NULL)
        str_list = str_list->next;
    str_list->next = last;
    last->next = NULL;
    last->str = strdup(string);
    return_if_null(last->str, "Out of memory.", false);
    last->free_string = true;
    return true;
}

/** Add a object as first element to a linked list.
 *
 * @param[in] object The object to be added.
 * @param[in,out] object_list The linked list to be extended.
 *
 * @retval TSS2_RC_SUCCESS if the object was added.
 * @retval TSS2_FAPI_RC_MEMORY If memory for the list extension cannot
 *         be allocated.
 */
TSS2_RC
push_object_to_list(void *object, NODE_OBJECT_T **object_list)
{
    NODE_OBJECT_T *first = calloc(1, sizeof(NODE_OBJECT_T));
    return_if_null(first, "Out of space.", TSS2_FAPI_RC_MEMORY);
    first->object = object;
    if (*object_list)
        first->next = *object_list;
    *object_list = first;
    return TSS2_RC_SUCCESS;
}

/** Add a object as last element to a linked list.
 *
 * @param[in] object The object to be added.
 * @param[in,out] object_list The linked list to be extended.
 *
 * @retval TSS2_RC_SUCCESS if the object was added.
 * @retval TSS2_FAPI_RC_MEMORY If memory for the list extension cannot
 *         be allocated.
 */
TSS2_RC
append_object_to_list(void *object, NODE_OBJECT_T **object_list)
{
    NODE_OBJECT_T *list, *last = calloc(1, sizeof(NODE_OBJECT_T));
    return_if_null(last, "Out of space.", TSS2_FAPI_RC_MEMORY);
    last->object = object;
    if (!*object_list) {
        *object_list = last;
        return TSS2_RC_SUCCESS;
    }
    list = *object_list;
    while (list->next)
        list = list->next;
    list->next = last;
    return TSS2_RC_SUCCESS;
}

/**  Compute the name of a hierarchy object.
 *
 * The TPM handle will be computed from the esys handle and the name
 * will be computed from the TPM handle.
 *
 * @param[in,out] hierarchy The hierarchy object.
 */
static void
set_name_hierarchy_object(IFAPI_OBJECT *object)
{
    TPM2_HANDLE handle = 0;
    size_t offset = 0;
    switch (object->public.handle) {
    case ESYS_TR_RH_NULL:
        handle = TPM2_RH_NULL;
        break;
    case ESYS_TR_RH_OWNER:
        handle = TPM2_RH_OWNER;
        break;
    case ESYS_TR_RH_ENDORSEMENT:
        handle = TPM2_RH_ENDORSEMENT;
        break;
    case ESYS_TR_RH_LOCKOUT:
        handle = TPM2_RH_LOCKOUT;
        break;
    case ESYS_TR_RH_PLATFORM:
        handle = TPM2_RH_PLATFORM;
        break;
    case ESYS_TR_RH_PLATFORM_NV:
        handle = TPM2_RH_PLATFORM_NV;
        break;
    }
    Tss2_MU_TPM2_HANDLE_Marshal(handle,
                                &object->misc.hierarchy.name.name[0], sizeof(TPM2_HANDLE),
                                &offset);
    object->misc.hierarchy.name.size = offset;
}

/** Initialize the internal representation of a FAPI hierarchy object.
 *
 * The object will be cleared and the type of the general fapi object will be
 * set to hierarchy.
 *
 * @param[in,out] hierarchy The caller allocated hierarchy object. The name of the
 *                object will be computed.
 * @param[in] esys_handle The ESAPI handle of the hierarchy which will be added to
 *            to the object.
 */
void
ifapi_init_hierarchy_object(
    IFAPI_OBJECT *hierarchy,
    ESYS_TR esys_handle)
{
    memset(hierarchy, 0, sizeof(IFAPI_OBJECT));
    hierarchy->system = TPM2_YES;
    hierarchy->objectType = IFAPI_HIERARCHY_OBJ;
    hierarchy->public.handle = esys_handle;
    hierarchy->misc.hierarchy.esysHandle = esys_handle;
    set_name_hierarchy_object(hierarchy);
}

/**  Initialize a hierarchy object read from a file.
 *
 * The esys handles will be set depending on the object path and the
 * object name will be computed.
 *
 * @param[in,out] hierarchy The caller allocated hierarchy object.
 * @retval TSS2_RC_SUCCESS if the hierarchy could be initialized.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE For an invalid hierarchy path.
 */
TSS2_RC
ifapi_set_name_hierarchy_object(IFAPI_OBJECT *object)
{
    const char *path = object->rel_path;
    size_t pos = 0, pos2;
    if (path) {
        /* Determine esys handle from pathname. */
        if (strncmp("/", &path[0], 1) == 0)
            pos += 1;
        /* Skip profile if it does exist in path */
        if (strncmp("P_", &path[pos], 2) == 0) {
            char *  start = strchr(&path[pos], IFAPI_FILE_DELIM_CHAR);
            if (start) {
                pos2 = (int)(start - &path[pos]);
                pos = pos2 + 2;
            } else {
                return_error(TSS2_FAPI_RC_GENERAL_FAILURE, "Invalid path.");
            }
        }
        if (strcmp(&path[pos], "HS") == 0) {
            object->public.handle = ESYS_TR_RH_OWNER;
            object->misc.hierarchy.esysHandle = ESYS_TR_RH_OWNER;
        } else if (strcmp(&path[pos], "HE") == 0) {
            object->public.handle = ESYS_TR_RH_ENDORSEMENT;
            object->misc.hierarchy.esysHandle = ESYS_TR_RH_ENDORSEMENT;
        } else if (strcmp(&path[pos], "LOCKOUT") == 0) {
            object->public.handle = ESYS_TR_RH_LOCKOUT;
            object->misc.hierarchy.esysHandle = ESYS_TR_RH_LOCKOUT;
        } else  if (strcmp(&path[pos], "HN") == 0) {
            object->public.handle = ESYS_TR_RH_NULL;
            object->misc.hierarchy.esysHandle = ESYS_TR_RH_NULL;
        }
    }
    set_name_hierarchy_object(object);
    return TSS2_RC_SUCCESS;
}

/** Create a directory and all sub directories.
 *
 * @param[in] supdir The sup directory were the directories will be created.
 * @param[in] dir_list A linked list with the directory strings.
 * @param[in] mode The creation mode for the directory which will be used
 *            for the mkdir function.
 * @retval TSS2_RC_SUCCESS on success.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 */
static TSS2_RC
create_dirs(const char *supdir, NODE_STR_T *dir_list, mode_t mode)
{
    char *new_dir;
    for (size_t i = 1; i <= ifapi_path_length(dir_list); i++) {
        TSS2_RC r = ifapi_path_string_n(&new_dir, supdir, dir_list, NULL, i);
        return_if_error(r, "Create path string");
        LOG_TRACE("Check file: %s", new_dir);
        int rc = mkdir(new_dir, mode);
        if (rc != 0 && errno != EEXIST) {
            LOG_ERROR("mkdir not possible: %i %s", rc, new_dir);
            free(new_dir);
            return TSS2_FAPI_RC_BAD_VALUE;
        }
        free(new_dir);
    }
    return TSS2_RC_SUCCESS;
}

/** Create sub-directories in a certain directory.
 *
 * @param[in] supdir The directory in which the new directories shall be created.
 * @param[in] path The path containing one or more sub-directories.
 *
 * @retval TSS2_RC_SUCCESS: If the directories were created.
 * @retval TSS2_FAPI_RC_MEMORY: If the linked list with the sub-directories
 *                              cannot be allocated.
 * @retval TSS2_FAPI_RC_BAD_VALUE: If a directory cannot be created.
 */
TSS2_RC
ifapi_create_dirs(const char *supdir, const char *path)
{
    TSS2_RC r;
    NODE_STR_T *path_list = split_string(path, IFAPI_FILE_DELIM);
    return_if_null(path_list, "Out of memory.", TSS2_FAPI_RC_MEMORY);

    r = create_dirs(supdir, path_list, 0777);
    goto_if_error2(r, "Create directories for %s", error_cleanup, path);
    free_string_list(path_list);
    return TSS2_RC_SUCCESS;

error_cleanup:
    free_string_list(path_list);
    return r;
}

/** Determine whether authentication with an auth value is needed ro an object..
 *
 * In the key store the information whether an auth value was provided for an
 * object is saved. Thus the it is possible to decide whether the auth value
 * callback is required for authentication.
 *
 * @param[in] object The object which has to be checked..
 *
 * @retval true: If an auth value was provided.
 * @retval false: If not.
 */
bool
object_with_auth(IFAPI_OBJECT *object)
{
    switch (object->objectType) {
    case IFAPI_KEY_OBJ:
        return (object->misc.key.with_auth == TPM2_YES);
    case IFAPI_NV_OBJ:
        return (object->misc.nv.with_auth == TPM2_YES);
    case IFAPI_HIERARCHY_OBJ:
        return (object->misc.hierarchy.with_auth == TPM2_YES);
    default:
        return false;
    }
}

/** Free memory allocated during deserialization of a policy element.
 *
 * Depending on the element type the fields of a policy element are freed.
 *
 * @param[in] policy The policy element.
 */
static void
cleanup_policy_element(TPMT_POLICYELEMENT *policy)
{
        switch (policy->type) {
        case POLICYSECRET:
            SAFE_FREE(policy->element.PolicySecret.objectPath);
            break;
        case POLICYAUTHORIZE:
            SAFE_FREE(policy->element.PolicyAuthorize.keyPath);
            SAFE_FREE(policy->element.PolicyAuthorize.keyPEM);
            break;
        case POLICYAUTHORIZENV:
            SAFE_FREE( policy->element.PolicyAuthorizeNv.nvPath);
            SAFE_FREE( policy->element.PolicyAuthorizeNv.policy_buffer);
            break;
        case POLICYSIGNED:
            SAFE_FREE(policy->element.PolicySigned.keyPath);
            SAFE_FREE(policy->element.PolicySigned.keyPEM);
            SAFE_FREE(policy->element.PolicySigned.publicKeyHint);
            break;
        case POLICYPCR:
            SAFE_FREE(policy->element.PolicyPCR.pcrs);
            break;
        case POLICYNV:
            SAFE_FREE(policy->element.PolicyNV.nvPath);
            break;
        case POLICYDUPLICATIONSELECT:
            SAFE_FREE(policy->element.PolicyDuplicationSelect.newParentPath);
            break;
        case POLICYNAMEHASH:
            for (size_t i = 0; i < 3; i++) {
                SAFE_FREE(policy->element.PolicyNameHash.namePaths[i]);
            }
            break;
        case POLICYACTION:
            SAFE_FREE(policy->element.PolicyAction.action);
            break;
        }
}

/** Free memory allocated during deserialization of a a policy element list.
 *
 * All elements of a policy element list are freed.
 *
 * @param[in] policy The policy element list.
 */
static void
cleanup_policy_elements(TPML_POLICYELEMENTS *policy)
{
    size_t i, j;
    if (policy != NULL) {
        for (i = 0; i < policy->count; i++) {
            if (policy->elements[i].type == POLICYOR) {
                /* Policy with sub policies */
                TPML_POLICYBRANCHES *branches = policy->elements[i].element.PolicyOr.branches;
                for (j = 0; j < branches->count; j++) {
                    SAFE_FREE(branches->authorizations[j].name);
                    SAFE_FREE(branches->authorizations[j].description);
                    cleanup_policy_elements(branches->authorizations[j].policy);
                }
                SAFE_FREE(branches);
            } else {
                cleanup_policy_element(&policy->elements[i]);
            }
        }
        SAFE_FREE(policy);
    }
}

/** Free memory allocated during deserialization of policy.
 *
 * The object will not be freed (might be declared on the stack).
 *
 * @param[in] policy The policy to be cleaned up.
 *
 */
void
ifapi_cleanup_policy(TPMS_POLICY *policy)
{
    if (policy) {
        SAFE_FREE(policy->description);
        if (policy->policyAuthorizations) {
            for (size_t i = 0; i < policy->policyAuthorizations->count; i++) {
                if (strcmp(policy->policyAuthorizations->authorizations[i].type, "pem") == 0) {
                    SAFE_FREE(policy->policyAuthorizations->authorizations[i].keyPEM);
                    SAFE_FREE(policy->policyAuthorizations->authorizations[i].pemSignature.buffer);
                }
                SAFE_FREE(policy->policyAuthorizations->authorizations[i].type);
            }
        }
        SAFE_FREE(policy->policyAuthorizations);
        cleanup_policy_elements(policy->policy);
    }
}

static TPML_POLICYELEMENTS *
copy_policy_elements(const TPML_POLICYELEMENTS *from_policy);

/** Copy policy structure.
 *
 * @param[in] src The policy structure to be copied.
 * @param[out] dest The destination policy structure.
 * @retval TSS2_RC_SUCCESS on success.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
static TSS2_RC
copy_policy(TPMS_POLICY * dest,
        const TPMS_POLICY * src) {
    /* Check for NULL references */
    if (dest == NULL || src == NULL) {
        return TSS2_FAPI_RC_MEMORY;
    }

    TSS2_RC r = TSS2_RC_SUCCESS;
    dest->description = NULL;
    strdup_check(dest->description, src->description, r, error_cleanup);
    dest->policy = copy_policy_elements(src->policy);
    goto_if_null2(dest->policy, "Out of memory", r, TSS2_FAPI_RC_MEMORY,
            error_cleanup);

    return r;
error_cleanup:
    ifapi_cleanup_policy(dest);
    return r;
}

/** Copy policy branches.
 *
 * @param[in] src The policy branches to be copied.
 * @param[out] dest The destination policy branches.
 * @retval TSS2_RC_SUCCESS on success.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
static TPML_POLICYBRANCHES *
copy_policy_branches(const TPML_POLICYBRANCHES *from_branches)
{
    TPML_POLICYBRANCHES *to_branches;
    size_t j;

    to_branches = calloc(1, sizeof(TPML_POLICYBRANCHES) +
                         from_branches->count * sizeof(TPMS_POLICYBRANCH));
    if (!to_branches)
        return NULL;
    to_branches->count = from_branches->count;
    for (j = 0; j < from_branches->count; j++) {
        to_branches->authorizations[j].name = strdup(from_branches->authorizations[j].name);
        if (!to_branches->authorizations[j].name)
            goto error;
        to_branches->authorizations[j].description =
            strdup(from_branches->authorizations[j].description);
        if (!to_branches->authorizations[j].description)
            goto error;
        to_branches->authorizations[j].policy =
            copy_policy_elements(from_branches->authorizations[j].policy);
        if (to_branches->authorizations[j].policy == NULL
            && from_branches->authorizations[j].policy != NULL) {
            LOG_ERROR("Out of memory.");
            goto error;
        }
        to_branches->authorizations[j].policyDigests =
            from_branches->authorizations[j].policyDigests;
    }
    return to_branches;

error:
    for (j = 0; j < to_branches->count; j++) {
        SAFE_FREE(to_branches->authorizations[j].name);
        SAFE_FREE(to_branches->authorizations[j].description);
        cleanup_policy_elements(to_branches->authorizations[j].policy);
    }
    SAFE_FREE(to_branches);
    return NULL;
}

/** Create a copy of a policy element.
 *
 * Depending on the type of a poliy element a copy with newly allocated memory will be
 * created.
 *
 * @param[in]  from_policy The policy to be copied.
 * @param[out] to_policy The new policy element.
 *
 * @retval TSS2_RC_SUCCESS: if copying was successful.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE: If no from policy or no to policy was passed.
 * @retval TSS2_FAPI_RC_MEMORY: If not enough memory can be allocated.
 */
static TSS2_RC
copy_policy_element(const TPMT_POLICYELEMENT *from_policy, TPMT_POLICYELEMENT *to_policy)
{
    if (from_policy == NULL || to_policy == NULL) {
        return TSS2_FAPI_RC_BAD_REFERENCE;
    }
    TSS2_RC r = TSS2_RC_SUCCESS;

    *to_policy = *from_policy;
    size_t i;

    switch (from_policy->type) {
    case POLICYSECRET:
        strdup_check(to_policy->element.PolicySecret.objectPath,
                     from_policy->element.PolicySecret.objectPath, r, error);
        break;
    case POLICYAUTHORIZE:
        strdup_check(to_policy->element.PolicyAuthorize.keyPath,
                     from_policy->element.PolicyAuthorize.keyPath, r, error);
        strdup_check(to_policy->element.PolicyAuthorize.keyPEM,
                     from_policy->element.PolicyAuthorize.keyPEM, r, error);
        break;
    case POLICYAUTHORIZENV:
        strdup_check(to_policy->element.PolicyAuthorizeNv.nvPath,
                     from_policy->element.PolicyAuthorizeNv.nvPath, r, error);
        break;
    case POLICYSIGNED:
        strdup_check(to_policy->element.PolicySigned.keyPath,
                     from_policy->element.PolicySigned.keyPath, r, error);
        strdup_check(to_policy->element.PolicySigned.keyPEM,
                     from_policy->element.PolicySigned.keyPEM, r, error);
        strdup_check(to_policy->element.PolicySigned.publicKeyHint,
                     from_policy->element.PolicySigned.publicKeyHint, r, error);
        break;
    case POLICYPCR:
        to_policy->element.PolicyPCR.pcrs =
            calloc(1, sizeof(TPML_PCRVALUES) +
                   from_policy->element.PolicyPCR.pcrs->count + sizeof(TPMS_PCRVALUE));
        goto_if_null2(to_policy->element.PolicyPCR.pcrs, "Out of memory.",
                      r, TSS2_FAPI_RC_MEMORY, error);
        to_policy->element.PolicyPCR.pcrs->count
            = from_policy->element.PolicyPCR.pcrs->count;
        for (i = 0; i < to_policy->element.PolicyPCR.pcrs->count; i++)
            to_policy->element.PolicyPCR.pcrs->pcrs[i]
                = from_policy->element.PolicyPCR.pcrs->pcrs[i];
        break;
    case POLICYNV:
        strdup_check(to_policy->element.PolicyNV.nvPath,
                     from_policy->element.PolicyNV.nvPath, r, error);
        break;
    case POLICYDUPLICATIONSELECT:
        strdup_check(to_policy->element.PolicyDuplicationSelect.newParentPath,
                     from_policy->element.PolicyDuplicationSelect.newParentPath,
                     r, error);
        break;
    case POLICYACTION:
        strdup_check(to_policy->element.PolicyAction.action,
                     from_policy->element.PolicyAction.action, r, error);
        break;
    case POLICYNAMEHASH:
        for (size_t i = 0; i < from_policy->element.PolicyNameHash.count; i++) {
            strdup_check(to_policy->element.PolicyNameHash.namePaths[i],
                    from_policy->element.PolicyNameHash.namePaths[i],
                    r, error);
        }
        break;
    }
    return TSS2_RC_SUCCESS;

error:
    return r;
}

/** Copy a list of policy elements
 *
 * @param[in] form_policy The policy list to be copied.
 * @retval NULL If the policy cannot be copied.
 * @retval TPML_POLICYELEMENTS The copy of the policy list.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
static TPML_POLICYELEMENTS *
copy_policy_elements(const TPML_POLICYELEMENTS *from_policy)
{
    if (from_policy == NULL) {
        return NULL;
    }
    TSS2_RC r;
    size_t i;
    TPML_POLICYELEMENTS *to_policy = NULL;

    to_policy = calloc(1, sizeof(TPML_POLICYELEMENTS) +
                       from_policy->count * sizeof(TPMT_POLICYELEMENT));
    to_policy->count = from_policy->count;
    for (i = 0; i < from_policy->count; i++) {
        if (from_policy->elements[i].type == POLICYOR) {
            to_policy->elements[i].type = POLICYOR;
            /* Policy with sub policies */
            TPML_POLICYBRANCHES *branches = from_policy->elements[i].element.PolicyOr.branches;
            to_policy->elements[i].element.PolicyOr.branches = copy_policy_branches(branches);
            if (to_policy->elements[i].element.PolicyOr.branches == NULL) {
                LOG_ERROR("Out of memory");
                SAFE_FREE(to_policy);
                return NULL;
            }
        } else {
            r = copy_policy_element(&from_policy->elements[i], &to_policy->elements[i]);
            if (r != TSS2_RC_SUCCESS) {
                cleanup_policy_elements(to_policy);
                return NULL;
            }
        }
    }
    return to_policy;
}

/** Copy policy.
 *
 * @param[in] from_policy the policy to be copied.
 * @retval The new policy or NULL if not enough memory was available.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TPMS_POLICY *
ifapi_copy_policy(
    const TPMS_POLICY *from_policy)
{
    if (from_policy == NULL) {
        return NULL;
    }
    TPMS_POLICY *to_policy = calloc(1, sizeof(TPMS_POLICY));
    if (to_policy == NULL) {
        return NULL;
    }
    to_policy->description = NULL;
    TSS2_RC r = copy_policy(to_policy, from_policy);
    if (r != TSS2_RC_SUCCESS) {
        SAFE_FREE(to_policy);
        return NULL;
    } else {
        return to_policy;
    }
}

/** Compute the name of a TPM transient or persistent object.
 *
 * @param[in] publicInfo The public information of the TPM object.
 * @param[out] name The computed name.
 * @retval TPM2_RC_SUCCESS  or one of the possible errors TSS2_FAPI_RC_BAD_VALUE,
 * TSS2_FAPI_RC_MEMORY, TSS2_FAPI_RC_GENERAL_FAILURE.
 * or return codes of SAPI errors.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE if an internal error occurred.
 */
TSS2_RC
ifapi_get_name(TPMT_PUBLIC *publicInfo, TPM2B_NAME *name)
{
    BYTE buffer[sizeof(TPMT_PUBLIC)];
    size_t offset = 0;
    size_t len_alg_id = sizeof(TPMI_ALG_HASH);
    size_t size = sizeof(TPMU_NAME) - sizeof(TPMI_ALG_HASH);
    IFAPI_CRYPTO_CONTEXT_BLOB *cryptoContext;

    if (publicInfo->nameAlg == TPM2_ALG_NULL) {
        name->size = 0;
        return TSS2_RC_SUCCESS;
    }
    TSS2_RC r;
    r = ifapi_crypto_hash_start(&cryptoContext, publicInfo->nameAlg);
    return_if_error(r, "crypto hash start");

    r = Tss2_MU_TPMT_PUBLIC_Marshal(publicInfo,
                                    &buffer[0], sizeof(TPMT_PUBLIC), &offset);
    if (r) {
        LOG_ERROR("Marshaling TPMT_PUBLIC");
        ifapi_crypto_hash_abort(&cryptoContext);
        return r;
    }

    r = ifapi_crypto_hash_update(cryptoContext, &buffer[0], offset);
    if (r) {
        LOG_ERROR("crypto hash update");
        ifapi_crypto_hash_abort(&cryptoContext);
        return r;
    }

    r = ifapi_crypto_hash_finish(&cryptoContext, &name->name[len_alg_id],
                                 &size);
    if (r) {
        LOG_ERROR("crypto hash finish");
        ifapi_crypto_hash_abort(&cryptoContext);
        return r;
    }

    offset = 0;
    r = Tss2_MU_TPMI_ALG_HASH_Marshal(publicInfo->nameAlg,
                                      &name->name[0], sizeof(TPMI_ALG_HASH),
                                      &offset);
    return_if_error(r, "Marshaling TPMI_ALG_HASH");

    name->size = size + len_alg_id;
    return TSS2_RC_SUCCESS;
}

/** Compute the name from the public data of a NV index.
 *
 * The name of a NV index is computed as follows:
 *   name = nameAlg||Hash(nameAlg,marshal(publicArea))
 * @param[in] publicInfo The public information of the NV index.
 * @param[out] name The computed name.
 * @retval TSS2_RC_SUCCESS on success.
 * @retval TSS2_FAPI_RC_MEMORY Memory can not be allocated.
 * @retval TSS2_FAPI_RC_BAD_VALUE for invalid parameters.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE for unexpected NULL pointer parameters.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE for errors of the crypto library.
 * @retval TSS2_SYS_RC_* for SAPI errors.
 */
TSS2_RC
ifapi_nv_get_name(TPMS_NV_PUBLIC *publicInfo, TPM2B_NAME *name)
{
    BYTE buffer[sizeof(TPMS_NV_PUBLIC)];
    size_t offset = 0;
    size_t size = sizeof(TPMU_NAME) - sizeof(TPMI_ALG_HASH);
    size_t len_alg_id = sizeof(TPMI_ALG_HASH);
    IFAPI_CRYPTO_CONTEXT_BLOB *cryptoContext;

    if (publicInfo->nameAlg == TPM2_ALG_NULL) {
        name->size = 0;
        return TSS2_RC_SUCCESS;
    }
    TSS2_RC r;

    /* Initialize the hash computation with the nameAlg. */
    r = ifapi_crypto_hash_start(&cryptoContext, publicInfo->nameAlg);
    return_if_error(r, "Crypto hash start");

    /* Get the marshaled data of the public area. */
    r = Tss2_MU_TPMS_NV_PUBLIC_Marshal(publicInfo,
                                       &buffer[0], sizeof(TPMS_NV_PUBLIC),
                                       &offset);
    if (r) {
        LOG_ERROR("Marshaling TPMS_NV_PUBLIC");
        ifapi_crypto_hash_abort(&cryptoContext);
        return r;
    }

    r = ifapi_crypto_hash_update(cryptoContext, &buffer[0], offset);
    if (r) {
        LOG_ERROR("crypto hash update");
        ifapi_crypto_hash_abort(&cryptoContext);
        return r;
    }

    /* The hash will be stored after the nameAlg.*/
    r = ifapi_crypto_hash_finish(&cryptoContext, &name->name[len_alg_id],
                                 &size);
    if (r) {
        LOG_ERROR("crypto hash finish");
        ifapi_crypto_hash_abort(&cryptoContext);
        return r;
    }

    offset = 0;
    /* Store the nameAlg in the result. */
    r = Tss2_MU_TPMI_ALG_HASH_Marshal(publicInfo->nameAlg,
                                      &name->name[0], sizeof(TPMI_ALG_HASH),
                                      &offset);
    return_if_error(r, "Marshaling TPMI_ALG_HASH");

    name->size = size + len_alg_id;
    return TSS2_RC_SUCCESS;
}

/** Check whether a nv or key object has a certain name.
 *
 * @param[in] object The object (has to be checked whether it's a key).
 * @param[in] name The name to be compared.
 * @param[out] equal If the two names are equal.
 * @retval TSS2_RC_SUCCESSS if name of object can be deserialized.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE if an internal error occurred.
 */
TSS2_RC
ifapi_object_cmp_name(IFAPI_OBJECT *object, void *name, bool *equal)
{
    TSS2_RC r;
    *equal = false;
    TPM2B_NAME *obj_name;
    TPM2B_NAME nv_name;

    switch (object->objectType) {
    case IFAPI_HIERARCHY_OBJ:
        obj_name = &object->misc.hierarchy.name;
        break;
    case IFAPI_KEY_OBJ:
        obj_name = &object->misc.key.name;
        break;
    case IFAPI_NV_OBJ:
        r = ifapi_nv_get_name(&object->misc.nv.public.nvPublic, &nv_name);
        return_if_error(r, "Get NV name.");

        obj_name = &nv_name;
        break;
    default:
        return TSS2_RC_SUCCESS;
    }
    if (obj_name->size != ((TPM2B_NAME *)name)->size)
        return TSS2_RC_SUCCESS;
    if (memcmp(&obj_name->name[0], &((TPM2B_NAME *)name)->name[0], obj_name->size))
        /* The names are not equal */
        return TSS2_RC_SUCCESS;
    /* The two names are equal */
    *equal = true;
    return TSS2_RC_SUCCESS;
}

/** Check whether a nv object has a certain public info.
 *
 * @param[in] object The object (has to be checked whether it's a key).
 * @param[in] nv_public The NV public data with the NV index.
 * @param[out] equal If the two names are equal.
 * @retval TSS2_RC_SUCCESSS if name of object can be deserialized.
 */
TSS2_RC
ifapi_object_cmp_nv_public(IFAPI_OBJECT *object, void *nv_public, bool *equal)
{
    *equal = false;

    switch (object->objectType) {
        break;
    case IFAPI_NV_OBJ:
        if (object->misc.nv.public.nvPublic.nvIndex
            == ((TPM2B_NV_PUBLIC *)nv_public)->nvPublic.nvIndex)
            *equal = true;
        break;
    default:
        return TSS2_RC_SUCCESS;
    }
    return TSS2_RC_SUCCESS;
}

/** Compute signature as byte array and signature size in DER format.
 *
 * For ECC signatures the conversion to DER is necessary, for RSA the
 * buffer of the TPM2B has already DER format.
 * parameters.
 * @param[in] sig_key_object The signing key.
 * @param[in] tpm_signature the signature in TPM format.
 * @param[out] signature The byte array of the signature (callee allocated).
 * @param[out] signatureSize The size of the byte array.
 *
 * @retval TSS2_RC_SUCCESSS if the conversion was successful.
 * @retval TSS2_FAPI_RC_MEMORY: if not enough memory can be allocated.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE If an internal error occurs, which is
 *         not covered by other return codes (e.g. a unexpected openssl
 *         error).
 * @retval TSS2_FAPI_RC_BAD_VALUE if an invalid value was passed into
 *         the function.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_tpm_to_fapi_signature(
    IFAPI_OBJECT *sig_key_object,
    TPMT_SIGNATURE *tpm_signature,
    uint8_t **signature,
    size_t *signatureSize)
{
    TSS2_RC r;

    *signature = NULL;
    TPMT_SIG_SCHEME *sig_scheme = &sig_key_object->misc.key.signing_scheme;

    if (sig_key_object->misc.key.public.publicArea.type == TPM2_ALG_RSA) {
        /* Signature is already in DER format. */

        if (sig_scheme->scheme == TPM2_ALG_RSAPSS) {
            *signatureSize = tpm_signature->signature.rsapss.sig.size;
            *signature = malloc(*signatureSize);
            goto_if_null(*signature, "Out of memory.", TSS2_FAPI_RC_MEMORY, error_cleanup);

            memcpy(*signature,
                   &tpm_signature->signature.rsapss.sig.buffer[0],
                   *signatureSize);
        } else if (sig_scheme->scheme == TPM2_ALG_RSASSA) {
            *signatureSize = tpm_signature->signature.rsassa.sig.size;
            *signature = malloc(*signatureSize);
            goto_if_null(*signature, "Out of memory.", TSS2_FAPI_RC_MEMORY, error_cleanup);

            memcpy(*signature,
                   &tpm_signature->signature.rsassa.sig.buffer[0],
                   *signatureSize);
        }
    } else if (sig_key_object->misc.key.public.publicArea.type == TPM2_ALG_ECC &&
               sig_scheme->scheme == TPM2_ALG_ECDSA) {
        /* For ECC signatures the TPM signaute has to be converted to DER. */
        r = ifapi_tpm_ecc_sig_to_der(tpm_signature,
                                     signature, signatureSize);
        goto_if_error(r, "Conversion to DER failed", error_cleanup);
    } else {
        goto_error(r, TSS2_FAPI_RC_BAD_VALUE, "Unknown signature scheme", error_cleanup);
    }
    return TSS2_RC_SUCCESS;

error_cleanup:
    SAFE_FREE(*signature);
    return r;
}

/** Compute the JSON representation of quote information.
 *
 * The attest generated by a TPM quote will be converted into a
 * JSON representation together with the signature scheme of the
 * key used for the quote.
 *
 * @param[in]  sig_key_object The key object which was used for the quote.
 * @param[in]  tpm_quoted: The attest produced by the quote.
 * @param[out] quoteInfo The character string with the JSON representation of the
 *             attest together with the signing schemed.
 *
 * @retval TSS2_RC_SUCCESS: If the conversion was successful.
 * @retval TSS2_FAPI_RC_MEMORY: if not enough memory can be allocated.
 * @retval TSS2_FAPI_RC_BAD_VALUE: If an invalid value is detected during
 *         serialisation.
 * @retval Possible error codes of the unmarshaling function.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE if an internal error occurred.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_compute_quote_info(
    IFAPI_OBJECT *sig_key_object,
    TPM2B_ATTEST *tpm_quoted,
    char **quoteInfo)
{
    json_object *jso = NULL;
    TSS2_RC r;
    size_t offset = 0;
    TPMS_ATTEST attest_struct;
    FAPI_QUOTE_INFO fapi_quote_info;

    /* The TPM2B_ATTEST contains the marshaled TPMS_ATTEST structure. */
    r = Tss2_MU_TPMS_ATTEST_Unmarshal((const uint8_t *)
                                      &tpm_quoted->attestationData[0],
                                      tpm_quoted->size, &offset, &attest_struct);
    return_if_error(r, "Unmarshal TPMS_ATTEST.");

    fapi_quote_info.attest = attest_struct;
    /* The signate scheme will be taken from the key used for qoting. */
    fapi_quote_info.sig_scheme = sig_key_object->misc.key.signing_scheme;
    r = ifapi_json_FAPI_QUOTE_INFO_serialize(&fapi_quote_info, &jso);
    return_if_error(r, "Conversion to TPM2B_ATTEST to JSON.");

    /* The intermediate structure of type FAPI_QOTE_INFO will be serialized. */
    const char *quote_json = json_object_to_json_string_ext(jso,
                             JSON_C_TO_STRING_PRETTY);
    goto_if_null(quote_json, "Conversion attest to json.",
                 TSS2_FAPI_RC_GENERAL_FAILURE, cleanup);

    *quoteInfo = strdup(quote_json);
    goto_if_null(*quoteInfo, "Out of memory.", TSS2_FAPI_RC_MEMORY, cleanup);

cleanup:
    json_object_put(jso);
    return r;
}

/** Deserialize the JSON representation of FAPI quote information.
 *
 * The JSON representation of FAPI quote information will be
 * deserialized to a FAPI_QUOTE_INFO structure and also the TPM2B
 * version of the attest will be created.
 *
 * @param[in]  quoteInfo The JSON representation if the quote
 *             information.
 * @param[out] tpm_quoted: The marhaled version of the attest structure.
 * @param[out] fapi_quote_info The quote information structure used by
 *             FAPI.
 *
 * @retval TSS2_RC_SUCCESS: If the deserialization was successful.
 * @retval TSS2_FAPI_RC_BAD_VALUE: If an invalid value is detected during
 *         deserialisation.
 * @retval Possible error codes of the marshaling function.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 */
TSS2_RC
ifapi_get_quote_info(
    char const *quoteInfo,
    TPM2B_ATTEST *tpm_quoted,
    FAPI_QUOTE_INFO *fapi_quote_info)
{
    json_object *jso = NULL;
    TSS2_RC r;
    size_t offset = 0;

    jso = ifapi_parse_json(quoteInfo);
    return_if_null(jso, "Json error.", TSS2_FAPI_RC_BAD_VALUE);

    memset(&fapi_quote_info->attest.attested.quote.pcrSelect, 0,
           sizeof(TPML_PCR_SELECTION));

    r = ifapi_json_FAPI_QUOTE_INFO_deserialize(jso, fapi_quote_info);
    goto_if_error(r, "Conversion to JSON of TPM2S_ATTEST.", cleanup);

    offset = 0;
    r = Tss2_MU_TPMS_ATTEST_Marshal(&fapi_quote_info->attest,
                                    (uint8_t *)&tpm_quoted->attestationData[0],
                                    sizeof(TPMS_ATTEST), &offset);
    LOGBLOB_TRACE(&tpm_quoted->attestationData[0],
                  offset,
                  "Attest");
    tpm_quoted-> size = offset;
    goto_if_error(r, "Marshal attest.", cleanup);

cleanup:
    if (jso)
        json_object_put(jso);
    return r;
}

/** Determine start index for NV object depending on type.
 *
 * The value will be determined based on e TCG handle registry.
 *
 * @param[in]  path The path used for the NV object.
 * @param[out] start_nv_index The first possible NV index for this type.
 *
 * @retval TSS2_RC_SUCCESS If the index for the path can be determined.
 * @retval TSS2_FAPI_RC_BAD_PATH If no handle can be assigned.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 */
TSS2_RC
ifapi_get_nv_start_index(const char *path, TPM2_HANDLE *start_nv_index)
{
    NODE_STR_T *dir_list = split_string(path, IFAPI_FILE_DELIM);

    *start_nv_index = 0;

    return_if_null(dir_list, "Out of memory.", TSS2_FAPI_RC_MEMORY);
    if (dir_list->next && strcmp(dir_list->str, "nv") == 0) {
        if (strcmp(dir_list->next->str, "TPM") == 0)
            *start_nv_index = 0x01000000;
        else if (strcmp(dir_list->next->str, "Platform") == 0)
            *start_nv_index = 0x01400000;
        else if (strcmp(dir_list->next->str, "Owner") == 0)
            *start_nv_index = 0x01800000;
        else if (strcmp(dir_list->next->str, "Endorsement_Certificate") == 0)
            *start_nv_index = 0x01c00000;
        else if (strcmp(dir_list->next->str, "Platform_Certificate") == 0)
            *start_nv_index = 0x01c08000;
        else if (strcmp(dir_list->next->str, "Component_OEM") == 0)
            *start_nv_index = 0x01c10000;
        else if (strcmp(dir_list->next->str, "TPM_OEM") == 0)
            *start_nv_index = 0x01c20000;
        else if (strcmp(dir_list->next->str, "Platform_OEM") == 0)
            *start_nv_index = 0x01c30000;
        else if (strcmp(dir_list->next->str, "PC-Client") == 0)
            *start_nv_index = 0x01c40000;
        else if (strcmp(dir_list->next->str, "Server") == 0)
            *start_nv_index = 0x01c50000;
        else if (strcmp(dir_list->next->str, "Virtualized_Platform") == 0)
            *start_nv_index = 0x01c60000;
        else if (strcmp(dir_list->next->str, "MPWG") == 0)
            *start_nv_index = 0x01c70000;
        else if (strcmp(dir_list->next->str, "Embedded") == 0)
            *start_nv_index = 0x01c80000;
    }
    free_string_list(dir_list);
    if (*start_nv_index)
        return TSS2_RC_SUCCESS;

    return_error2(TSS2_FAPI_RC_BAD_PATH, "Invalid NV path: %s", path);
}

/** Check whether NV index is appropriate for NV path.
 *
 * The value will be checked  based on e TCG handle registry.
 *
 * @param[in]  path The path used for the NV object.
 * @param[out] nv_index The NV index to be used.
 *
 * @retval TSS2_RC_SUCCESS If the index for the path can be determined.
 * @retval TSS2_FAPI_RC_BAD_PATH If the path is not valid.
 * @retval TSS2_FAPI_RC_BAD_VALUE If the nv index is not appropriate for the path.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 */
TSS2_RC
ifapi_check_nv_index(const char *path, TPM2_HANDLE nv_index)
{
    TSS2_RC r;
    NODE_STR_T *dir_list = split_string(path, IFAPI_FILE_DELIM);

    return_if_null(dir_list, "Out of memory.", TSS2_FAPI_RC_MEMORY);
    if (dir_list->next && strcmp(dir_list->str, "nv") == 0 && dir_list->next->str) {
        if (strcmp(dir_list->next->str, "TPM") == 0) {
            if (nv_index < 0x01000000 || nv_index > 0x013fffff)
                goto_error(r, TSS2_FAPI_RC_BAD_VALUE,
                           "NV TPM handle not in the range 0x01000000:0x013fffff",
                           error_cleanup);
        } else if (strcmp(dir_list->next->str, "Platform") == 0) {
            if (nv_index < 0x01400000 || nv_index > 0x017fffff)
                goto_error(r, TSS2_FAPI_RC_BAD_VALUE,
                           "NV Platform handle not in the range 0x01400000:0x017fffff",
                           error_cleanup);
        } else if (strcmp(dir_list->next->str, "Owner") == 0) {
            if (nv_index < 0x01800000 || nv_index > 0x01bfffff)
            goto_error(r, TSS2_FAPI_RC_BAD_VALUE,
                       "NV Owner handle not in the range 0x01800000:0x01bfffff",
                       error_cleanup);
        } else if (strcmp(dir_list->next->str, "Endorsement_Certificate") == 0) {
            if (nv_index <  0x01c00000 || nv_index > 0x01c07fff)
            goto_error(r, TSS2_FAPI_RC_BAD_VALUE,
                       "NV Endorsement Certificate handle not in the range "
                       "0x01c00000:0x01c07fff",
                       error_cleanup);
        } else if (strcmp(dir_list->next->str, "Platform_Certificate") == 0) {
            if (nv_index <  0x01c08000 || nv_index > 0x01c0ffff)
            goto_error(r, TSS2_FAPI_RC_BAD_VALUE,
                       "NV  Platform Certificate handle not in the range "
                       "0x01c08000:0x01c0ffff",
                       error_cleanup);
        } else if (strcmp(dir_list->next->str, "Component_OEM") == 0) {
            if (nv_index <  0x01c10000 || nv_index > 0x01c1ffff)
            goto_error(r, TSS2_FAPI_RC_BAD_VALUE,
                       "NV Component OEM handle not in the range "
                       "0x01c10000:0x01c1ffff",
                       error_cleanup);
        } else if (strcmp(dir_list->next->str, "TPM_OEM") == 0) {
            if (nv_index < 0x01c20000 || nv_index > 0x01c2ffff)
            goto_error(r, TSS2_FAPI_RC_BAD_VALUE,
                       "NV TPM OEM handle not in the range "
                       "0x01c20000:0x01c2ffff",
                       error_cleanup);
        } else if (strcmp(dir_list->next->str, "Platform_OEM") == 0) {
            if (nv_index < 0x01c30000 || nv_index > 0x01c3ffff)
            goto_error(r, TSS2_FAPI_RC_BAD_VALUE,
                       "NV Platform OEM handle not in the range "
                       "0x01c30000:0x01c3ffff",
                       error_cleanup);
        } else if (strcmp(dir_list->next->str, "PC-Client") == 0) {
            if (nv_index < 0x01c40000 || nv_index > 0x01c4ffff)
            goto_error(r, TSS2_FAPI_RC_BAD_VALUE,
                       "NV PC-Client handle not in the range "
                       "0x01c40000:0x01c4ffff",
                       error_cleanup);
        } else if (strcmp(dir_list->next->str, "Server") == 0) {
            if (nv_index < 0x01c50000 || nv_index > 0x01c5ffff)
            goto_error(r, TSS2_FAPI_RC_BAD_VALUE,
                       "NV PC-Client handle not in the range "
                       "0x01c50000:0x01c5ffff",
                       error_cleanup);
        } else if (strcmp(dir_list->next->str, "Virtualized_Platform") == 0) {
            if (nv_index < 0x01c60000 || nv_index > 0x01c6ffff)
            goto_error(r, TSS2_FAPI_RC_BAD_VALUE,
                       "NV PC-Client handle not in the range "
                       "0x01c60000:0x016cffff",
                       error_cleanup);
        } else if (strcmp(dir_list->next->str, "MPWG") == 0) {
            if (nv_index < 0x01c70000 || nv_index > 0x01c7ffff)
            goto_error(r, TSS2_FAPI_RC_BAD_VALUE,
                       "NV PC-Client handle not in the range "
                       "0x01c70000:0x017cffff",
                       error_cleanup);
        } else if (strcmp(dir_list->next->str, "Embedded") == 0) {
            if (nv_index < 0x01c80000 || nv_index >  0x01c8ffff)
            goto_error(r, TSS2_FAPI_RC_BAD_VALUE,
                       "NV PC-Client handle not in the range "
                       "0x01c80000:0x018cffff",
                       error_cleanup);
        } else {
            goto_error(r, TSS2_FAPI_RC_BAD_PATH, "Invalid nv path: %s", error_cleanup, path);
        }
    } else {
        goto_error(r, TSS2_FAPI_RC_BAD_PATH, "Invalid nv path: %s", error_cleanup, path);
    }
    free_string_list(dir_list);
    return TSS2_RC_SUCCESS;;

 error_cleanup:
    free_string_list(dir_list);
    return r;
}

/** Compute new PCR value from a part of an event list.
 *
 * @param[in,out] vpcr The old and the new PCR value.
 * @param[in] bank The bank corresponding to value of the event list
 *                 which will be used for computation.
 * @param[in] event The event list with the values which were extended
 *                  for a certain bank.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the bank was not found in the event list.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE if an error occurs in the crypto library
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 */
TSS2_RC
ifapi_extend_vpcr(
    TPM2B_DIGEST *vpcr,
    TPMI_ALG_HASH bank,
    const IFAPI_EVENT *event)
{
    TSS2_RC r;
    size_t i, j;
    size_t event_size, size;
    IFAPI_CRYPTO_CONTEXT_BLOB *cryptoContext;
    bool zero_digest = false;

    LOGBLOB_TRACE(&vpcr->buffer[0], vpcr->size, "Old vpcr value");
    for (i = 0; i < event->digests.count; i++) {
        if (event->digests.digests[i].hashAlg == bank) {
            event_size = ifapi_hash_get_digest_size(event->digests.digests[i].hashAlg);

            LOGBLOB_TRACE(&event->digests.digests[i].digest.sha512[0], event_size,
                          "Extending with");

            zero_digest = true;
            for (j = 0; j < event_size; j++) {
                if (event->digests.digests[i].digest.sha512[j]) {
                    zero_digest = false;
                }
            }
            if (zero_digest)
                continue;

            r = ifapi_crypto_hash_start(&cryptoContext, bank);
            return_if_error(r, "crypto hash start");

            HASH_UPDATE_BUFFER(cryptoContext, &vpcr->buffer[0], vpcr->size, r, error_cleanup);
            HASH_UPDATE_BUFFER(cryptoContext, &event->digests.digests[i].digest.sha512[0],
                               event_size, r, error_cleanup);
            r = ifapi_crypto_hash_finish(&cryptoContext, &vpcr->buffer[0], &size);
            return_if_error(r, "crypto hash finish");
            vpcr->size = size;
            break;
        }
    }
    if (event->digests.count > 0 && i == event->digests.count && !zero_digest) {
        LOG_ERROR("No digest for bank %"PRIu16" found in event", bank);
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    LOGBLOB_TRACE(&vpcr->buffer[0], vpcr->size, "New vpcr value");

    return TSS2_RC_SUCCESS;

error_cleanup:
    ifapi_crypto_hash_abort(&cryptoContext);
    return r;
}

/** Compute new PCR value from PCR value and event digest.
 *
 * @param[in] alg The hash algorithm used for the PCR register.
 * @param[in,out] pcr The old and the new PCR value.
 * @param[in] digest The digest used for PCR extension.
 * @retval TSS2_FAPI_RC_BAD_VALUE if the bank was not found in the event list.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE if an error occurs in the crypto library
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 */
TSS2_RC
ifapi_extend_pcr(
    TPMI_ALG_HASH alg,
    uint8_t *pcr,
    const uint8_t *digest,
    size_t alg_size)
{
    TSS2_RC r;
    IFAPI_CRYPTO_CONTEXT_BLOB *cryptoContext;

    LOGBLOB_TRACE(pcr, alg_size, "Old pcr value");
    LOGBLOB_TRACE(digest, alg_size, "Extend with");

    r = ifapi_crypto_hash_start(&cryptoContext, alg);
    return_if_error(r, "crypto hash start");

    HASH_UPDATE_BUFFER(cryptoContext, pcr, alg_size, r, error_cleanup);
    HASH_UPDATE_BUFFER(cryptoContext, digest, alg_size, r, error_cleanup);
    r = ifapi_crypto_hash_finish(&cryptoContext, pcr, &alg_size);
    return_if_error(r, "crypto hash finish");

    LOGBLOB_TRACE(pcr, alg_size, "New vpcr value");

    return TSS2_RC_SUCCESS;

error_cleanup:
    ifapi_crypto_hash_abort(&cryptoContext);
    return r;
}


/** Check whether a event list corresponds to a certain quote information.
 *
 * The event list is used to compute the PCR values corresponding
 * to this event list. The PCR digest for these PCRs is computed and compared
 * with the attest passed with quote_info.
 *
 * @param[in]  jso_event_list The event list in JSON representation.
 * @param[in]  quote_info The information structure with the attest.
 * @param[out] pcr_digest The computed pcr_digest for the PCRs uses by FAPI.
 *
 * @retval TSS2_RC_SUCCESS: If the PCR digest from the event list matches
 *         the PCR digest passed with the quote_info.
 * @retval TSS2_FAPI_RC_SIGNATURE_VERIFICATION_FAILED: If the digest computed
 *         from event list does not match the attest
 * @retval TSS2_FAPI_RC_BAD_VALUE: If inappropriate values are detected in the
 *         input data.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE if an internal error occurred.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 */
TSS2_RC
ifapi_calculate_pcr_digest(
    json_object *jso_event_list,
    const FAPI_QUOTE_INFO *quote_info,
    TPM2B_DIGEST *pcr_digest)
{
    TSS2_RC r;
    IFAPI_CRYPTO_CONTEXT_BLOB *cryptoContext = NULL;

    struct {
        TPMI_ALG_HASH bank;
        TPM2_HANDLE pcr;
        TPM2B_DIGEST value;
    } pcrs[TPM2_MAX_PCRS];
    size_t i, pcr, i_evt, hash_size, n_pcrs = 0, n_events = 0;

    json_object *jso;
    IFAPI_EVENT event;

    const TPML_PCR_SELECTION *pcr_selection;
    TPMI_ALG_HASH pcr_digest_hash_alg;

    /* Get some data from the quote info for easier access */
    pcr_selection = &quote_info->attest.attested.quote.pcrSelect;
    pcr_digest->size = quote_info->attest.attested.quote.pcrDigest.size;

    switch (quote_info->sig_scheme.scheme) {
    case TPM2_ALG_RSAPSS:
        pcr_digest_hash_alg = quote_info->sig_scheme.details.rsapss.hashAlg;
        break;
    case TPM2_ALG_RSASSA:
        pcr_digest_hash_alg = quote_info->sig_scheme.details.rsassa.hashAlg;
        break;
    case TPM2_ALG_ECDSA:
        pcr_digest_hash_alg = quote_info->sig_scheme.details.ecdsa.hashAlg;
        break;
    case TPM2_ALG_SM2:
        pcr_digest_hash_alg = quote_info->sig_scheme.details.sm2.hashAlg;
        break;
    default:
        LOG_ERROR("Unknown sig scheme");
        return TSS2_FAPI_RC_BAD_VALUE;
    }

    /* Initialize used pcrs */
    for (i = 0; i < pcr_selection->count; i++) {
        for (pcr = 0; pcr < TPM2_MAX_PCRS; pcr++) {
            uint8_t byte_idx = pcr / 8;
            uint8_t flag = 1 << (pcr % 8);
            if (flag & pcr_selection->pcrSelections[i].pcrSelect[byte_idx]) {
                hash_size = ifapi_hash_get_digest_size(pcr_selection->pcrSelections[i].hash);
                pcrs[n_pcrs].pcr = pcr;
                pcrs[n_pcrs].bank = pcr_selection->pcrSelections[i].hash;
                pcrs[n_pcrs].value.size = hash_size;
                memset(&pcrs[n_pcrs].value.buffer[0], 0, hash_size);
                n_pcrs += 1;
            }
        }
    }

    /* Compute pcr values based on event list */
    if (jso_event_list) {
        n_events = json_object_array_length(jso_event_list);
        for (i_evt = 0; i_evt < n_events; i_evt++) {
            jso = json_object_array_get_idx(jso_event_list, i_evt);
            r = ifapi_json_IFAPI_EVENT_deserialize(jso, &event, DIGEST_CHECK_WARNING);
            goto_if_error(r, "Error serialize policy", error_cleanup);
            LOG_TRACE("Deserialized Event for PCR %u", event.pcr);

            for (i = 0; i < n_pcrs; i++) {
                if (pcrs[i].pcr == event.pcr) {
                    LOG_DEBUG("Extend PCR %uz", pcrs[i].pcr);
                    r = ifapi_extend_vpcr(&pcrs[i].value, pcrs[i].bank, &event);
                    goto_if_error2(r, "Extending vpcr %"PRIu32, error_cleanup, pcrs[i].pcr);
                }
            }
            ifapi_cleanup_event(&event);
        }
    }

    /* Compute digest for the used pcrs */
    r = ifapi_crypto_hash_start(&cryptoContext, pcr_digest_hash_alg);
    return_if_error(r, "crypto hash start");

    for (i = 0; i < n_pcrs; i++) {
        HASH_UPDATE_BUFFER(cryptoContext, &pcrs[i].value.buffer, pcrs[i].value.size,
                           r, error_cleanup);
    }
    r = ifapi_crypto_hash_finish(&cryptoContext,
                                 (uint8_t *) &pcr_digest->buffer[0],
                                 &hash_size);
    return_if_error(r, "crypto hash finish");
    pcr_digest->size = hash_size;

    /* Compare the digest from the event list with the digest from the attest */
    if (memcmp(&pcr_digest->buffer[0], &quote_info->attest.attested.quote.pcrDigest.buffer[0],
               pcr_digest->size) != 0) {
        goto_error(r, TSS2_FAPI_RC_SIGNATURE_VERIFICATION_FAILED,
                   "The digest computed from event list does not match the attest.",
                   error_cleanup);
    }

error_cleanup:
    if (cryptoContext)
        ifapi_crypto_hash_abort(&cryptoContext);
    ifapi_cleanup_event(&event);
    return r;
}

/** Check whether profile PCR capabilities are a subset of TPM PCR capabilities.
 *
 * It has to be checked that every hash alg from the profile is available and
 * whether the selected PCRs are available.
 * @param[in] pcr_profile The pcr profile to use as basis for the selection.
 * @param[in] pcr_capablity The PCR capabilities  available for TPM.
 * @retval TSS2_RC_SUCCESSS if the conversion was successful.
 * @retval TSS2_FAPI_RC_BAD_VALUE if profile is not subset of capabilities.
 */
TSS2_RC
ifapi_check_profile_pcr_selection(
    const TPML_PCR_SELECTION *pcr_profile,
    const TPML_PCR_SELECTION *pcr_capablity)
{
    size_t i, j, k;

    for (i = 0; i < pcr_profile->count; i++) {
        bool hash_found = false;
        for (j = 0; j < pcr_capablity->count; j++) {
            if (pcr_capablity->pcrSelections[j].hash ==
                    pcr_profile->pcrSelections[i].hash) {
                /* Hash algorithm found, check PCRs */
                hash_found = true;
                if (pcr_profile->pcrSelections[i].sizeofSelect >
                        pcr_capablity->pcrSelections[j].sizeofSelect) {
                    return_error(TSS2_FAPI_RC_BAD_VALUE, "Invalid size of PCR select.");
                }

                for (k = 0;
                        k < pcr_profile->pcrSelections[i].sizeofSelect;
                        k++) {
                    /* Check whether all selected PCRs are available */
                    if ((pcr_profile->pcrSelections[i].pcrSelect[k] &
                            pcr_capablity->pcrSelections[j].pcrSelect[k])
                            != pcr_profile->pcrSelections[i].pcrSelect[k]) {
                        return_error(TSS2_FAPI_RC_BAD_VALUE, "Invalid PCR selection.");

                    }
                }
            }
        }
        if (!hash_found) {
            return_error(TSS2_FAPI_RC_BAD_VALUE,
                         "Hash alg for PCR selection not available.");
        }
    }
    return TSS2_RC_SUCCESS;
}

/** Reduce a PCR selection to a single pcr.
 *
 * This includes two steps: clearing all bits but the selected and clearing empty hashalg lines.
 *
 * @param[in,out] pcr_selection The pcr selection to be filtered.
 * @param[in] pcr_index The only PCR to remain selected.
 * @param[in]  pcr_count The size of the pcr list.
 *
 * @retval TSS2_RC_SUCCESS if the filtering was successful.
 * @retval TSS2_FAPI_RC_BAD_VALUE if no pcr remain selected or the pcr selection is malformed.
 */
TSS2_RC
ifapi_filter_pcr_selection_by_index(
    TPML_PCR_SELECTION *pcr_selection,
    const TPM2_HANDLE *pcr_index,
    size_t pcr_count)
{
    UINT32 bank, j;
    UINT16 select;
    size_t i;
    UINT8 selection[] = { 0, 0, 0, 0 };

    for (i = 0; i < pcr_count; i++) {
        selection[0] |= (1 << pcr_index[i]) % 256;
        selection[1] |= (1 << (pcr_index[i] - 8)) % 256;
        selection[2] |= (1 << (pcr_index[i] - 16)) % 256;
        selection[3] |= (1 << (pcr_index[i] - 24)) % 256;
    };

    /* Remove unselected PCRs */
    for (bank = 0; bank < pcr_selection->count; bank++) {
        if (pcr_selection->pcrSelections[bank].sizeofSelect > 4) {
            LOG_ERROR("pcrSelection's sizeofSelect exceeds allowed value of 4, is %"PRIu16,
                      pcr_selection->pcrSelections[bank].sizeofSelect);
            return TSS2_FAPI_RC_BAD_VALUE;
        }
        for (select = 0; select < pcr_selection->pcrSelections[bank].sizeofSelect; select++) {
            pcr_selection->pcrSelections[bank].pcrSelect[select] &= selection[select];
        }
    }

    /* Remove empty banks */
    for (bank = 0; bank < pcr_selection->count; ) {
        for (select = 0; select < pcr_selection->pcrSelections[bank].sizeofSelect; select++) {
            if (pcr_selection->pcrSelections[bank].pcrSelect[select])
                break;
        }
        if (select < pcr_selection->pcrSelections[bank].sizeofSelect) {
            /* Bank contains selections */
            bank ++;
            continue;
        }

        /* Bank contains no selections, move all other banks one up */
        pcr_selection->count -= 1;
        for (j = bank; j < pcr_selection->count; j++) {
            pcr_selection->pcrSelections[j] = pcr_selection->pcrSelections[j+1];
        }
    }

    if (pcr_selection->count == 0) {
        LOGBLOB_WARNING((void*)pcr_index, pcr_count * sizeof(*pcr_index),
                        "pcr index %"PRIi32" is not part of the pcr selection", *pcr_index);
        return TSS2_FAPI_RC_BAD_VALUE;
    }
    return TSS2_RC_SUCCESS;
}

/** Compute PCR selection and a PCR digest for a PCR value list.
 *
 * @param[in]  pcrs The list of PCR values.
 * @param[out] pcr_selection The selection computed based on the
 *             list of PCR values.
 * @param[in]  hash_alg The hash algorithm which is used for the policy computation.
 * @param[out] pcr_digest The computed PCR digest corresponding to the passed
 *             PCR value list.
 *
 * @retval TSS2_RC_SUCCESS if the PCR selection and the PCR digest could be computed..
 * @retval TSS2_FAPI_RC_BAD_VALUE: If inappropriate values are detected in the
 *         input data.
 * @retval TSS2_FAPI_RC_BAD_REFERENCE a invalid null pointer is passed.
 * @retval TSS2_FAPI_RC_MEMORY if not enough memory can be allocated.
 * @retval TSS2_FAPI_RC_GENERAL_FAILURE if an internal error occurred.
 */
TSS2_RC
ifapi_compute_policy_digest(
    TPML_PCRVALUES *pcrs,
    TPML_PCR_SELECTION *pcr_selection,
    TPMI_ALG_HASH hash_alg,
    TPM2B_DIGEST *pcr_digest)
{
    TSS2_RC r = TSS2_RC_SUCCESS;
    size_t i, j;
    IFAPI_CRYPTO_CONTEXT_BLOB *cryptoContext = NULL;
    size_t hash_size;
    UINT32 pcr;
    UINT32 max_pcr = 0;

    memset(pcr_selection, 0, sizeof(TPML_PCR_SELECTION));

    /* Compute PCR selection */
    pcr_selection->count = 0;
    for (i = 0; i < pcrs->count; i++) {
        for (j = 0; j < pcr_selection->count; j++) {
            if (pcrs->pcrs[i].hashAlg ==
                pcr_selection->pcrSelections[j].hash) {
                break;
            }
        }
        if (j == pcr_selection->count) {
            /* New hash alg */
            pcr_selection->count += 1;
            if (pcr_selection->count > TPM2_NUM_PCR_BANKS) {
                return_error(TSS2_FAPI_RC_BAD_VALUE,
                             "More hash algs than banks.");
            }
            pcr_selection->pcrSelections[j].hash =
                pcrs->pcrs[i].hashAlg;
            pcr_selection->pcrSelections[j].sizeofSelect = 3;
        }
        UINT32 pcrIndex = pcrs->pcrs[i].pcr;
        if (pcrIndex + 1 > max_pcr)
            max_pcr = pcrIndex + 1;
        pcr_selection->pcrSelections[j].pcrSelect[pcrIndex / 8] |=
            1 << pcrIndex % 8;
        if ((pcrIndex / 8) + 1 > pcr_selection->pcrSelections[j].sizeofSelect)
            pcr_selection->pcrSelections[j].sizeofSelect = (pcrIndex / 8) + 1;
    }
    /* Compute digest for current pcr selection */
    r = ifapi_crypto_hash_start(&cryptoContext, hash_alg);
    return_if_error(r, "crypto hash start");

    if (!(pcr_digest->size = ifapi_hash_get_digest_size(hash_alg))) {
        goto_error(r, TSS2_FAPI_RC_BAD_VALUE,
                   "Unsupported hash algorithm (%" PRIu16 ")", cleanup,
                   hash_alg);
    }

    for (i = 0; i < pcr_selection->count; i++) {
        TPMS_PCR_SELECTION selection = pcr_selection->pcrSelections[i];
        TPMI_ALG_HASH hashAlg = selection.hash;
        if (!(hash_size = ifapi_hash_get_digest_size(hashAlg))) {
            goto_error(r, TSS2_FAPI_RC_BAD_VALUE,
                       "Unsupported hash algorithm (%" PRIu16 ")", cleanup,
                       hashAlg);
        }
        for (pcr = 0; pcr < max_pcr; pcr++) {
            if ((selection.pcrSelect[pcr / 8]) & (1 << (pcr % 8))) {
                /* pcr selected */
                for (j = 0; j < pcrs->count; j++) {
                    if (pcrs->pcrs[j].pcr == pcr) {
                        r = ifapi_crypto_hash_update(cryptoContext,
                                                     (const uint8_t *)&pcrs->
                                                     pcrs[j].digest,
                                                     hash_size);
                        goto_if_error(r, "crypto hash update", cleanup);
                    }
                }
            }
        }
    }
    r = ifapi_crypto_hash_finish(&cryptoContext,
                                 (uint8_t *) & pcr_digest->buffer[0],
                                 &hash_size);
cleanup:
    if (cryptoContext)
        ifapi_crypto_hash_abort(&cryptoContext);
    return r;
}

/** Compare two public keys.
 *
 * @param[in] key1 The first key.
 * @param[in] key2 The second key.
 * @retval true if equal false if not.
 */
bool
ifapi_cmp_public_key(
    TPM2B_PUBLIC *key1,
    TPM2B_PUBLIC *key2)
{
    if (key1->publicArea.type != key2->publicArea.type)
        return false;
    switch (key1->publicArea.type) {
    case TPM2_ALG_RSA:
        if (key1->publicArea.unique.rsa.size != key2->publicArea.unique.rsa.size) {
            return false;
        }
        LOGBLOB_TRACE(&key1->publicArea.unique.rsa.buffer[0],
                      key1->publicArea.unique.rsa.size, "Key 1");
        LOGBLOB_TRACE(&key2->publicArea.unique.rsa.buffer[0],
                      key2->publicArea.unique.rsa.size, "Key 2");
        if (memcmp(&key1->publicArea.unique.rsa.buffer[0],
                   &key2->publicArea.unique.rsa.buffer[0],
                   key1->publicArea.unique.rsa.size) == 0)
            return true;
        else
            return false;
        break;
    case TPM2_ALG_ECC:
        if (key1->publicArea.unique.ecc.x.size != key2->publicArea.unique.ecc.x.size) {
            return false;
        }
        LOGBLOB_TRACE(&key1->publicArea.unique.ecc.x.buffer[0],
                      key1->publicArea.unique.ecc.x.size, "Key 1 x");
        LOGBLOB_TRACE(&key2->publicArea.unique.ecc.x.buffer[0],
                      key2->publicArea.unique.ecc.x.size, "Key 2 x");
        if (memcmp(&key1->publicArea.unique.ecc.x.buffer[0],
                   &key2->publicArea.unique.ecc.x.buffer[0],
                   key1->publicArea.unique.ecc.x.size) != 0)
            return false;
        if (key1->publicArea.unique.ecc.y.size != key2->publicArea.unique.ecc.y.size) {
            return false;
        }
        LOGBLOB_TRACE(&key1->publicArea.unique.ecc.y.buffer[0],
                      key1->publicArea.unique.ecc.y.size, "Key 1 x");
        LOGBLOB_TRACE(&key2->publicArea.unique.ecc.y.buffer[0],
                      key2->publicArea.unique.ecc.y.size, "Key 2 x");
        if (memcmp(&key1->publicArea.unique.ecc.y.buffer[0],
                   &key2->publicArea.unique.ecc.y.buffer[0],
                   key1->publicArea.unique.ecc.y.size) != 0)
            return false;
        else
            return true;
        break;

    default:
        return false;
    }
}

/** Check valid keys of a json object.
 *
 * @param[in]  jso The json object.
 * @param[out] field_tab the array of strings with allowed fields.
 * @param[out] size_of_tab The number of allowed fields.
 *
 * If a unexpected field occurs a warning will be displayed.
 */
void
ifapi_check_json_object_fields(
    json_object *jso,
    char** field_tab,
    size_t size_of_tab)
{
    enum json_type type;
    bool found;
    size_t i;

    type = json_object_get_type(jso);
    if (type == json_type_object) {
        /* Object with keys. */
        json_object_object_foreach(jso, key, val) {
            UNUSED(val);
            found = false;
            for (i = 0; i < size_of_tab; i++) {
                if (strcmp(key, field_tab[i]) == 0) {
                    found = true;
                    break;
                }
            }
            if (!found) {
                LOG_WARNING("Invalid field: %s", key);
            }
        }
    }
}

TSS2_RC ifapi_pcr_selection_to_pcrvalues(
        TPML_PCR_SELECTION *pcr_selection,
        TPML_DIGEST *pcr_digests,
        TPML_PCRVALUES **out) {

    /* Count pcrs */
    UINT32 i = 0, pcr = 0, n_pcrs = 0, i_pcr = 0;
    for (i = 0; i < pcr_selection->count; i++) {
        for (pcr = 0; pcr < TPM2_MAX_PCRS; pcr++) {
            uint8_t byte_idx = pcr / 8;
            uint8_t flag = 1 << (pcr % 8);
            /* Check whether PCR is used. */
            if (flag & pcr_selection->pcrSelections[i].pcrSelect[byte_idx])
                n_pcrs += 1;
        }
    }


    TPML_PCRVALUES *pcr_values = calloc(1, sizeof(TPML_PCRVALUES) + n_pcrs* sizeof(TPMS_PCRVALUE));
    return_if_null(pcr_values, "Out of memory.", TSS2_FAPI_RC_MEMORY);
    /* Initialize digest list with pcr values from TPM */
    i_pcr = 0;
    pcr_values->count = pcr_digests->count;
    for (i = 0; i < pcr_selection->count; i++) {
        for (pcr = 0; pcr < TPM2_MAX_PCRS; pcr++) {
            uint8_t byte_idx = pcr / 8;
            uint8_t flag = 1 << (pcr % 8);
            /* Check whether PCR is used. */
            if (flag & pcr_selection->pcrSelections[i].pcrSelect[byte_idx]) {
                pcr_values->pcrs[i_pcr].pcr = pcr;
                pcr_values->pcrs[i_pcr].hashAlg = pcr_selection->pcrSelections[i].hash;
                memcpy(&pcr_values->pcrs[i_pcr].digest,
                       &pcr_digests->digests[i_pcr].buffer[0],
                       pcr_digests->digests[i_pcr].size);
                i_pcr += 1;
            }
        }
    }

    *out = pcr_values;

    return TSS2_RC_SUCCESS;
}

void ifapi_helper_init_policy_pcr_selections (TSS2_POLICY_PCR_SELECTION *s,
        TPMT_POLICYELEMENT *pol_element)
{
    if (pol_element->element.PolicyPCR.currentPCRs.sizeofSelect > 0) {
        s->type = TSS2_POLICY_PCR_SELECTOR_PCR_SELECT;
        s->selections.pcr_select = pol_element->element.PolicyPCR.currentPCRs;
    } else {
        s->type = TSS2_POLICY_PCR_SELECTOR_PCR_SELECTION;
        s->selections.pcr_selection =
                pol_element->element.PolicyPCR.currentPCRandBanks;
    }
}
