/* SPDX-License-Identifier: BSD-2-Clause */
/*******************************************************************************
 * Copyright 2018-2019, Fraunhofer SIT sponsored by Infineon Technologies AG
 * All rights reserved.
 ******************************************************************************/

#ifndef IFAPI_KEYSTORE_H
#define IFAPI_KEYSTORE_H

#include <stdlib.h>

#include "tss2_common.h"
#include "tss2_tpm2_types.h"
#include "fapi_types.h"
#include "ifapi_policy_types.h"
#include "tss2_esys.h"
#include "tss2_policy.h"

typedef UINT32 IFAPI_OBJECT_TYPE_CONSTANT;
#define IFAPI_OBJ_NONE                 0    /**< Tag for key resource */
#define IFAPI_KEY_OBJ                  1    /**< Tag for key resource */
#define IFAPI_NV_OBJ                   2    /**< Tag for NV Ram resource */
#define IFAPI_EXT_PUB_KEY_OBJ          3    /**< Tag for key resource */
#define IFAPI_HIERARCHY_OBJ            4    /**< Tag for other resources, e.g. PCR register, hierarchies */
#define IFAPI_DUPLICATE_OBJ            5    /**< Tag for key duplication object */

/** Type for representing a FAPI key
 */
typedef struct {
    UINT32                            persistent_handle;    /**< Persistent TPM Handle */
    TPM2B_PUBLIC                                 public;    /**< The wrapped public portion of the object */
    UINT8_ARY                             serialization;    /**< None */
    UINT8_ARY                                   private;    /**< None */
    char                                *policyInstance;    /**<  Keys policy */
    TPM2B_DIGEST                            creationHash;   /**< Hash create by Create or CreatePrimary */
    TPM2B_CREATION_DATA                    creationData;    /**< None */
    TPMT_TK_CREATION                     creationTicket;    /**< None */
    char                                   *description;    /**< Human readable description of key */
    UINT8_ARY                                   appData;    /**< Application data */
    char                                   *certificate;    /**< Keys certificate (if any) */
    TPMT_SIG_SCHEME                      signing_scheme;    /**< Signing scheme for the key */
    TPM2B_NAME                                     name;    /**< Name of the key */
    TPMI_YES_NO                               with_auth;    /**< Authorization provided during creation */
    UINT32                                  reset_count;    /**< The TPM reset count during key creation */
    TPMI_YES_NO                       delete_prohibited;    /**< Persistent object should not be deleted.  */
    TPMI_YES_NO                              ek_profile;    /**< Has to be set if EK is created according
                                                                 to EK credential profile: */
    TPM2B_DIGEST                                  nonce;    /**< Nonce used to initialize uniqe data */
} IFAPI_KEY;

/** Type for representing a external public key
 */
typedef struct {
    char                                *pem_ext_public;    /**< Public key in PEM format */
    char                                   *certificate;    /**< Keys certificate (if any) */
    TPM2B_PUBLIC                                 public;    /**< The pulic information in TPM format */
} IFAPI_EXT_PUB_KEY;

/** Type for representing hierarchy
 */
typedef struct {
    TPMI_YES_NO                               with_auth;    /**< Authorization provided */
    char                                   *description;    /**< Human readable description of hierarchy */
    TPM2B_DIGEST                             authPolicy;
    ESYS_TR                                  esysHandle;
    bool                                      authorized;   /**< Switch whether hiearchy is authorized. */
    TPM2B_NAME                                     name;    /**< Name of the hierarchy */
} IFAPI_HIERARCHY;

/** Type for representing a FAPI NV object
 */
typedef struct {
    TPM2B_NV_PUBLIC                              public;    /**< The wrapped public portion of the object */
    UINT8_ARY                             serialization;    /**< None */
    UINT32                                    hierarchy;    /**< The hierarchy used for NV object creation */
    char                                *policyInstance;    /**<  Keys policy */
    char                                   *description;    /**< Human readable description of key */
    UINT8_ARY                                   appData;    /**< Application data */
    TPMI_YES_NO                               with_auth;    /**< Authorization provided during creation */
    char*                                     event_log;    /**< The event log if NV type is pcr */
} IFAPI_NV;

/** Type for representing a FAPI object for key duplication.
 */
typedef struct {

    TPM2B_PRIVATE                             duplicate; /**< The duplicate of the key to export*/
    TPM2B_ENCRYPTED_SECRET               encrypted_seed; /**< Encrypted seed needed for key import */
    TPM2B_PUBLIC                                 public; /**< The public information of the key to be duplicated */
    TPM2B_PUBLIC                          public_parent; /**< The public information of the new parent key */
    char                                   *certificate; /**< The certificate of the key to be duplicated */
    TPMS_POLICY                                 *policy; /**< The policy of the key to be duplicated */
} IFAPI_DUPLICATE;

/** type for representing public info of a TPM-Resource
 */
typedef union {
    IFAPI_EXT_PUB_KEY                       ext_pub_key;    /**< Public info for external key. */
    IFAPI_KEY                                       key;    /**< Public info for key objects */
    IFAPI_NV                                         nv;    /**< Public info for NV ram objects */
    IFAPI_DUPLICATE                            key_tree;    /**< Information for key duplication */
    IFAPI_HIERARCHY                           hierarchy;    /**< Information related to hierarchies */
} IFAPI_OBJECT_UNION;

/** The states for key searching */
enum FAPI_SEARCH_STATE {
    KSEARCH_INIT = 0,
    KSEARCH_SEARCH_OBJECT,
    KSEARCH_READ
};

/** The data structure holding internal state for key searching.
 */
typedef struct {
    size_t path_idx;                /**< Index of array of objects to be searched */
    size_t numPaths;                /**< Number of all objects in data store */
    char **pathlist;                /**< The array of all objects  in the search path */
    enum FAPI_SEARCH_STATE state;
} IFAPI_KEY_SEARCH;

typedef struct IFAPI_KEYSTORE {
    char *systemdir;
    char *userdir;
    char *defaultprofile;
    IFAPI_KEY_SEARCH key_search;
    const char* rel_path;
} IFAPI_KEYSTORE;


/** The states for the FAPI's object authorization state*/
enum IFAPI_AUTHORIZATION_STATE {
    AUTH_INIT = 0,
    AUTH_CHECK_POLICY,
    AUTH_CREATE_SESSION,
    AUTH_EXEC_POLICY,
    AUTH_FLUSH_OLD_POLICY,
    AUTH_DONE
};

/** The states for the FAPI's object write/read state*/
enum IFAPI_IO_STATE {
    IO_INIT = 0,
    IO_ACTIVE,
};

#define TSS2_OBJECT_TO_IFAPI_OBJECT(p) ((IFAPI_OBJECT *)p)

/** Type for representing TPM-Resource
 */
typedef struct _IFAPI_OBJECT {
    /* TSS2_OBJECT MUST GO FIRST. In C pointer of first element
     * is equal to pointer of base type, use this to hide data by
     * only passing pointer to public in callbacks, however, internal
     * FAPI code can do a simple upcast it back to the original.
     *
     * **NOTE**: One could use offset of, and play the same trick
     * the linux kernel linked list uses with container_of, but
     * since offsetof isn't C99, we won't use it here.
     */
    TSS2_OBJECT                                  public;    /**< public fields of an IFAPI_OBJECT */
    TPMS_POLICY                                 *policy;
    IFAPI_OBJECT_TYPE_CONSTANT               objectType;    /**< Selector for object type */
    IFAPI_OBJECT_UNION                             misc;    /**< Resource specific information */
    TPMI_YES_NO                                  system;    /**< Store the object in the system wide
                                                             directory */
    enum IFAPI_AUTHORIZATION_STATE  authorization_state;    /**< State of object authorization state machine */
    enum IFAPI_IO_STATE                           state;
    const char                                *rel_path;    /**< The relative path in keystore. */

} IFAPI_OBJECT;

TSS2_RC
ifapi_check_valid_path(const char *path);

TSS2_RC
ifapi_keystore_initialize(
    IFAPI_KEYSTORE *keystore,
    const char *config_systemdir,
    const char *config_userdir,
    const char *config_defaultprofile);

TSS2_RC
ifapi_keystore_load_async(
    IFAPI_KEYSTORE *keystore,
    IFAPI_IO *io,
    const char *path);

TSS2_RC
ifapi_keystore_load_finish(
    IFAPI_KEYSTORE *keystore,
    IFAPI_IO *io,
    IFAPI_OBJECT *object);

TSS2_RC
ifapi_keystore_object_does_not_exist(
    IFAPI_KEYSTORE *keystore,
    const char *path,
    const IFAPI_OBJECT *object);

TSS2_RC
ifapi_keystore_store_async(
    IFAPI_KEYSTORE *keystore,
    IFAPI_IO *io,
    const char *path,
    const IFAPI_OBJECT *object);

TSS2_RC
ifapi_keystore_store_finish(
    IFAPI_IO *io);

TSS2_RC
ifapi_keystore_list_all(
    IFAPI_KEYSTORE *keystore,
    const char *searchpath,
    char ***results,
    size_t *numresults);

TSS2_RC
ifapi_keystore_delete(
     IFAPI_KEYSTORE *keystore,
     char *path);

TSS2_RC
ifapi_keystore_remove_directories(
    IFAPI_KEYSTORE *keystore,
    const char *dir_name);

TSS2_RC
ifapi_keystore_search_obj(
    IFAPI_KEYSTORE *keystore,
    IFAPI_IO *io,
    TPM2B_NAME *name,
    char **found_path);

TSS2_RC
ifapi_keystore_search_nv_obj(
    IFAPI_KEYSTORE *keystore,
    IFAPI_IO *io,
    TPM2B_NV_PUBLIC *nv_public,
    char **found_path);

TSS2_RC
ifapi_keystore_check_overwrite(
    IFAPI_KEYSTORE *keystore,
    const char *path);

TSS2_RC
ifapi_keystore_check_writeable(
    IFAPI_KEYSTORE *keystore,
    const char *path);

TSS2_RC
ifapi_copy_ifapi_key(
    IFAPI_KEY * dest,
    const IFAPI_KEY * src);

TSS2_RC
ifapi_copy_ifapi_hierarchy(
    IFAPI_HIERARCHY * dest,
    const IFAPI_HIERARCHY * src);

TSS2_RC
ifapi_copy_ifapi_key_object(
    IFAPI_OBJECT * dest,
    const IFAPI_OBJECT * src);

TSS2_RC
ifapi_copy_ifapi_hierarchy_object(
    IFAPI_OBJECT * dest,
    const IFAPI_OBJECT * src);


void ifapi_cleanup_ifapi_key(
    IFAPI_KEY * key);

void ifapi_cleanup_ifapi_ext_pub_key(
    IFAPI_EXT_PUB_KEY * key);

void ifapi_cleanup_ifapi_hierarchy(
    IFAPI_HIERARCHY * hierarchy);

void ifapi_cleanup_ifapi_nv(
    IFAPI_NV * nv);

void ifapi_cleanup_ifapi_duplicate(
    IFAPI_DUPLICATE * duplicate);

void ifapi_cleanup_ifapi_key_search(
    IFAPI_KEY_SEARCH * key_search);

void ifapi_cleanup_ifapi_keystore(
    IFAPI_KEYSTORE * keystore);

void
ifapi_cleanup_ifapi_object(
    IFAPI_OBJECT *object);

TSS2_RC
ifapi_check_provisioned(
    IFAPI_KEYSTORE *keystore,
    const char *rel_path,
    bool *ok);

#endif /* IFAPI_KEYSTORE_H */
