/* SPDX-License-Identifier: BSD-2-Clause */
/*******************************************************************************
 * Copyright 2018-2019, Fraunhofer SIT sponsored by Infineon Technologies AG
 * All rights reserved.
 ******************************************************************************/
#ifndef FAPI_INT_H
#define FAPI_INT_H

#include "fapi_types.h"
#include "ifapi_policy_types.h"
#include "ifapi_policy_instantiate.h"
#include "ifapi_eventlog.h"
#include "ifapi_io.h"
#include "ifapi_profiles.h"
#include "ifapi_macros.h"
#include "ifapi_keystore.h"
#include "ifapi_policy_store.h"
#include "ifapi_config.h"

#include <stdlib.h>
#include <stdint.h>
#include <unistd.h>
#include <string.h>
#include <inttypes.h>
#include <stdarg.h>
#include <stdbool.h>
#include <sys/stat.h>
#include <stdio.h>
#include <errno.h>
#include <fcntl.h>
#include <json-c/json.h>
#include <poll.h>

#include "tss2_esys.h"
#include "tss2_fapi.h"

#define DEFAULT_LOG_DIR "/run/tpm2_tss"
#define IFAPI_PCR_LOG_FILE "pcr.log"
#define IFAPI_OBJECT_TYPE ".json"
#define IFAPI_OBJECT_FILE "object.json"
#define IFAPI_SRK_KEY_PATH "/HS/SRK"
#define IFAPI_EK_KEY_PATH "/HE/EK"
#define IFAPI_HS_PATH "/HS"
#define IFAPI_HE_PATH "/HE"
#define IFAPI_HN_PATH "/HN"
#define IFAPI_LOCKOUT_PATH "/LOCKOUT"
#define IFAPI_SRK_OBJECT_PATH "/HS/SRK/object.json"
#define IFAPI_HS_OBJECT_PATH "/HS/object.json"

typedef UINT32 TSS2_KEY_TYPE;
#define TSS2_SRK 2
#define TSS2_EK 3
#define MIN_EK_CERT_HANDLE 0x1c00000
#define MIN_PLATFORM_CERT_HANDLE 0x01C08000
#define MAX_PLATFORM_CERT_HANDLE 0x01C0FFFF

typedef UINT8 IFAPI_SESSION_TYPE;
#define IFAPI_SESSION_GENEK 0x01
#define IFAPI_SESSION1      0x02
#define IFAPI_SESSION2      0x04

#define IFAPI_POLICY_PATH "policy"
#define IFAPI_NV_PATH "nv"
#define IFAPI_EXT_PATH "ext"
#define IFAPI_FILE_DELIM "/"
#define IFAPI_LIST_DELIM ":"
#define IFAPI_FILE_DELIM_CHAR '/'
#define IFAPI_PUB_KEY_DIR "ext"
#define IFAPI_POLICY_DIR "policy"
#define IFAPI_PEM_PUBLIC_STRING "-----BEGIN PUBLIC KEY-----"
#define IFAPI_PEM_PRIVATE_KEY "-----PRIVATE KEY-----"
#define IFAPI_JSON_TAG_POLICY "policy"
#define IFAPI_JSON_TAG_OBJECT_TYPE "objectType"
#define IFAPI_JSON_TAG_DUPLICATE "public_parent"

#define FAPI_WRITE W_OK
#define FAPI_READ R_OK

#if TPM2_MAX_NV_BUFFER_SIZE > TPM2_MAX_DIGEST_BUFFER
#define IFAPI_MAX_BUFFER_SIZE TPM2_MAX_NV_BUFFER_SIZE
#else
#define IFAPI_MAX_BUFFER_SIZE TPM2_MAX_DIGEST_BUFFER
#endif

#define IFAPI_FLUSH_PARENT true
#define IFAPI_NOT_FLUSH_PARENT false

/* Definition of FAPI buffer for TPM2B transmission */
typedef struct {
    UINT16 size;
    BYTE buffer[IFAPI_MAX_BUFFER_SIZE];
} IFAPI_MAX_BUFFER;

#define OSSL_FREE(S,TYPE) if((S) != NULL) {TYPE##_free((void*) (S)); (S)=NULL;}


#define FAPI_COPY_DIGEST(dest_buffer, dest_size, src, src_size) \
    if (src_size > sizeof(TPMU_HA)) { \
        return_error(TSS2_FAPI_RC_BAD_VALUE, "Digest size too large."); \
    } \
    memcpy(dest_buffer, (src), (src_size));  \
    dest_size = src_size

#define HASH_UPDATE(CONTEXT, TYPE, OBJECT, R, LABEL)    \
    { \
        uint8_t buffer[sizeof(TYPE)]; \
        size_t offset = 0; \
        R = Tss2_MU_ ## TYPE ## _Marshal(OBJECT, \
                                         &buffer[0], sizeof(TYPE), &offset); \
        goto_if_error(R, "Marshal for hash update", LABEL); \
        R = ifapi_crypto_hash_update(CONTEXT, \
                                     (const uint8_t *) &buffer[0], \
                                     offset);                     \
        goto_if_error(R, "crypto hash update", LABEL); }

#define HASH_UPDATE_BUFFER(CONTEXT, BUFFER, SIZE, R, LABEL) \
    R = ifapi_crypto_hash_update(CONTEXT, \
                                 (const uint8_t *) BUFFER, SIZE) ; \
    goto_if_error(R, "crypto hash update", LABEL);

#define FAPI_SYNC(r,msg,label, ...)             \
    if (base_rc(r) == TSS2_BASE_RC_TRY_AGAIN) \
        return TSS2_FAPI_RC_TRY_AGAIN; \
    if (r != TSS2_RC_SUCCESS) { \
        LOG_ERROR(TPM2_ERROR_FORMAT " " msg, TPM2_ERROR_TEXT(r), ## __VA_ARGS__); \
        goto label;  \
    }

/** The states for the FAPI's object authorization state*/
enum IFAPI_GET_CERT_STATE {
    GET_CERT_INIT = 0,
    GET_CERT_WAIT_FOR_GET_CAP,
    GET_CERT_GET_CERT_NV,
    GET_CERT_GET_CERT_NV_FINISH,
    GET_CERT_GET_CERT_READ_PUBLIC,
    GET_CERT_GET_CERT_READ_HIERARCHY,
    GET_CERT_READ_CERT
};

/** The states for the FAPI's cleanup after successful command execution*/
enum IFAPI_CLEANUP_STATE {
    CLEANUP_INIT = 0,
    CLEANUP_SESSION1,
    CLEANUP_SESSION2,
    CLEANUP_SRK
};

/** The states for the FAPI's reading nv public*/
enum IFAPI_READ_NV_PUBLIC_STATE {
    READ_NV_PUBLIC_INIT = 0,
    READ_NV_PUBLIC_GET_ESYS_TR,
    READ_NV_PUBLIC_GET_PUBLIC
};

#define IFAPI_MAX_CAP_INFO 17

typedef struct {
    char                                  *description;
    TPMS_CAPABILITY_DATA                   *capability;
} IFAPI_CAP_INFO;

typedef struct {
    char                                 *fapi_version;    /**< The version string of FAPI */
    IFAPI_CONFIG                           fapi_config;    /**< The configuration information */
    IFAPI_CAP_INFO             cap[IFAPI_MAX_CAP_INFO];
} IFAPI_INFO;

/** Type for representing FAPI template for keys
 */
typedef struct {
    TPMI_YES_NO                                  system;    /**< Store the object in the system wide
                                                                 directory */
    TPMI_YES_NO                              persistent;    /**< Store key persistent in NV ram. */
    UINT32                            persistent_handle;    /**< < Persistent handle which should be used */
    TPM2B_PUBLIC                                 public;    /**< Template for public data */
} IFAPI_KEY_TEMPLATE;

/** Type for representing template for NV objects
 */
typedef struct {
    TPMI_YES_NO                                  system;    /**< Store the object in the system wide
                                                                 directory */
    TPMI_RH_HIERARCHY                         hierarchy;    /**< Hierarchy for NV object. */
    char                                   *description;    /**< Description of template. */
    TPMS_NV_PUBLIC                               public;    /**< Template for public data */
} IFAPI_NV_TEMPLATE;

/** Type for representing a external public key
 */
typedef struct {
    TPMT_SIG_SCHEME                          sig_scheme;    /**< Signature scheme used for quote. */
    TPMS_ATTEST                                  attest;    /**< Attestation data from Quote */
} FAPI_QUOTE_INFO;


/** The states for the FAPI's NV read state */
enum _FAPI_STATE_NV_READ {
    NV_READ_INIT = 0,
    NV_READ_AUTHORIZE,
    NV_READ_AUTHORIZE2,
    NV_READ_AUTH_SENT,
    NV_READ_CHECK_HANDLE,
    NV_READ_GET_CAPABILITY,
    NV_READ_GET_ESYS_HANDLE,
    NV_READ_GET_NV_PUBLIC
};

/** The states for the FAPI's NV write state */
enum _FAPI_STATE_NV_WRITE {
    NV2_WRITE_INIT = 0,
    NV2_WRITE_READ,
    NV2_WRITE_WAIT_FOR_SESSSION,
    NV2_WRITE_NULL_AUTH_SENT,
    NV2_WRITE_AUTH_SENT,
    NV2_WRITE_WRITE_PREPARE,
    NV2_WRITE_WRITE,
    NV2_WRITE_AUTHORIZE,
    NV2_WRITE_AUTHORIZE2
};

/** The data structure holding internal state of Fapi NV commands.
 */
typedef struct {
    char *nvPath ;              /**< The name of the file for object serialization */
    char *policyPath;           /**< The name of the policy file */
    TPM2B_NV_PUBLIC public;     /**< The public info of the NV object. */
    ESYS_TR esys_auth_handle;   /**< The ESAPI handle for the NV auth object */
    ESYS_TR esys_handle;        /**< The ESAPI handle for the NV object */
    TPM2_HANDLE tpm_handle;     /**< The TPM nv index */
    size_t numBytes;            /**< The number of bytes of a ESYS request */
    UINT16 bytesRequested;      /**< Bytes currently requested from TPM */
    UINT16 offset;              /**< Offset in TPM memory TPM */
    size_t data_idx;            /**< Offset in the read buffer */
    const uint8_t *data;        /**< Buffer for data to be written */
    uint8_t *rdata;             /**< Buffer for data to be read */
    size_t size;                /**< size of rdata */
    IFAPI_OBJECT auth_object;   /**< Object used for authentication */
    IFAPI_OBJECT nv_object;     /**< Deserialized NV object */
    TPM2B_AUTH auth;            /**< The Password */
    IFAPI_NV nv_obj;            /**< The NV Object */
    ESYS_TR auth_index;         /**< The ESAPI handle of the authorization object */
    uint64_t bitmap;            /**< The bitmask for the SetBits command */
    IFAPI_NV_TEMPLATE public_templ; /**< The template for nv creation, adjusted
                                         appropriate by the passed flags */
    enum _FAPI_STATE_NV_READ nv_read_state; /**< The current state of NV read */
    enum _FAPI_STATE_NV_WRITE nv_write_state; /**< The current state of NV write*/
    uint8_t *write_data;
    char *logData;               /**< The event log for NV objects of type pcr */
    json_object *jso_event_log;  /**< logData in JSON format */
    TPMI_RH_NV_INDEX maxNvIndex; /**< Max index for search for free index  */
    IFAPI_EVENT pcr_event;       /**< Event to be added to log */
    TPML_DIGEST_VALUES digests;  /**< Digest for the event data of an extend */
    bool skip_policy_computation; /**< switch whether policy needs to be computed */
} IFAPI_NV_Cmds;

/** The data structure holding internal state of Fapi_Initialize command.
 */
typedef struct {
    TPMS_CAPABILITY_DATA *capability; /* TPM capability data to check available algs */
    char **pathlist;                  /**< The array with all keystore objects */
    size_t numPaths;                  /**< Size of array with all keystore objects */
    size_t numNullPrimaries;         /**< Number of NULL hierarchy primaries
                                          stored in keystore */
    size_t primary_idx;              /**< Index to the current primary */
    size_t path_idx;                 /**< Index of array with the object paths */
    IFAPI_OBJECT *null_primaries;    /**< Array of the NULL hierarchy primaries. */
} IFAPI_INITIALIZE;

/** The data structure holding internal state of Fapi_PCR commands.
 */
typedef struct {
    TPML_DIGEST_VALUES digest_list;    /**< The digest list computed for the event  */
    TPML_DIGEST_VALUES *event_digests; /**< The digest list computed by TPM2_Event  */
    ESYS_TR PCR;                       /**< The handle of the PCR register to be extended */
    TPML_PCR_SELECTION pcr_selection;  /**< Selection used for Read and Quote */
    TPML_PCR_SELECTION *pcr_selection_out; /**< Selection returned by PCR_Read  */
    UINT32 update_count;
    TPML_DIGEST *pcrValues;            /* The values returned by PCR_Read */
    TPM2_HANDLE pcrIndex;
    TPMI_ALG_HASH hashAlg;
    const char *keyPath;              /**< The implicit key path for PCR_Quote */
    ESYS_TR handle;                   /**< The ESYS handle of the signing key */
    IFAPI_OBJECT *key_object;         /**< The IPAPI object of the signing key */
    TPMS_CAPABILITY_DATA *capabilityData; /* TPM capability data to check available algs */
    uint32_t *pcrList;                 /**< Array of PCR numbers */
    size_t pcrListSize;                /**< Size of PCR array */
    TPM2B_DATA qualifyingData;         /**< Nonce for quote command */
    uint8_t  const *eventData;
    TPM2B_EVENT event;
    size_t eventDataSize;
    uint32_t const *hashAlgs;
    uint32_t *hashAlgs2;
    size_t numHashAlgs;
    char    const *quoteInfo;
    TPM2B_ATTEST *tpm_quoted;
    TPMT_SIGNATURE *tpm_signature;
    uint8_t *signature;
    size_t signatureSize;
    char const *logData;
    char *pcrLog;
    IFAPI_EVENT pcr_event;
    json_object *event_list;
    FAPI_QUOTE_INFO fapi_quote_info;
    uint8_t *pcrValue;
    size_t pcrValueSize;
    char *event_log_file;
} IFAPI_PCR;

/** The data structure holding internal state of Fapi_SetDescription.
 */
typedef struct {
    char *description;             /**< The description of the object */
    UINT8_ARY appData;             /**< Application data to be stored in object store. */
    IFAPI_OBJECT object;           /**< The IPAPI object to store the info*/
    char *object_path;             /**< The realative path to the object */
    json_object *jso;              /**< JSON object for storing the AppData */
    char *jso_string;              /**< JSON deserialized buffer */
} IFAPI_Path_SetDescription;

/** The data structure holding internal state of Fapi_GetRandom.
 */
typedef struct {
    size_t numBytes;              /**< The number of random bytes to be generated */
    size_t idx;                   /**< Current position in output buffer.  */
    UINT16 bytesRequested;        /**< Byted currently requested from TPM */
    uint8_t *data;                /**< The buffer for the random data */
    uint8_t *ret_data;            /**< The result buffer. */
} IFAPI_GetRandom;

/** The data structure holding internal state of Fapi_Key_Setcertificate.
 */
typedef struct {
    const char *pem_cert;        /**< The certifificate in pem or format */
    char *pem_cert_dup;          /**< The allocate certifificate */
    const char *key_path;        /**< The absolute key path */
    NODE_STR_T *path_list;       /**< The computed explicit path */
    IFAPI_OBJECT key_object;     /**< The IPAPI object for the certified key */
} IFAPI_Key_SetCertificate;

/** The states for the FAPI's key creation */
enum IFAPI_KEY_CREATE_STATE {
    KEY_CREATE_INIT = 0,
    KEY_CREATE_WAIT_FOR_SESSION,
    KEY_CREATE_WAIT_FOR_PARENT,
    KEY_CREATE_AUTH_SENT,
    KEY_CREATE_WAIT_FOR_LOAD_AUTHORIZATION,
    KEY_CREATE_WAIT_FOR_KEY,
    KEY_CREATE_WAIT_FOR_HIERARCHY,
    KEY_CREATE_AUTHORIZE_HIERARCHY,
    KEY_CREATE_WAIT_FOR_EVICT_CONTROL,
    KEY_CREATE_WRITE_PREPARE,
    KEY_CREATE_WRITE,
    KEY_CREATE_FLUSH1,
    KEY_CREATE_FLUSH2,
    KEY_CREATE_CALCULATE_POLICY,
    KEY_CREATE_PRIMARY_CALCULATE_POLICY,
    KEY_CREATE_WAIT_FOR_AUTHORIZATION,
    KEY_CREATE_CLEANUP,
    KEY_CREATE_WAIT_FOR_RANDOM,
    KEY_CREATE_PRIMARY_INIT,
    KEY_CREATE_PRIMARY_WAIT_FOR_SESSION,
    KEY_CREATE_PRIMARY_WAIT_FOR_HIERARCHY,
    KEY_CREATE_PRIMARY_WAIT_FOR_AUTHORIZE1,
    KEY_CREATE_PRIMARY_WAIT_FOR_AUTHORIZE2,
    KEY_CREATE_PRIMARY_WAIT_FOR_PRIMARY,
    KEY_CREATE_PRIMARY_WAIT_FOR_EVICT_CONTROL,
    KEY_CREATE_PRIMARY_FLUSH,
    KEY_CREATE_PRIMARY_WRITE_PREPARE,
    KEY_CREATE_PRIMARY_WRITE,
    KEY_CREATE_PRIMARY_CLEANUP
};

/** The data structure holding internal state of Fapi_CreateKey.
 */
typedef struct {
    enum IFAPI_KEY_CREATE_STATE state;
    const char *keyPath;         /**< The pathname from the application */
    NODE_STR_T *path_list;       /**< The computed explicit path */
    IFAPI_OBJECT parent;         /**< The parent of the key for used for creation. */
    IFAPI_OBJECT object;          /**< The current object. */
    IFAPI_KEY_TEMPLATE public_templ;  /**< The template for the keys public data */
    TPM2B_PUBLIC public;         /**< The public data of the key */
    IFAPI_OBJECT hierarchy;     /**< The current used hierarchy for CreatePrimary */
    TPM2B_SENSITIVE_CREATE inSensitive;
    TPM2B_DATA outsideInfo;
    TPML_PCR_SELECTION creationPCR;
    ESYS_TR handle;
    const char *authValue;
    const char *policyPath;
    const IFAPI_PROFILE *profile;
    bool gen_sensitive_random;   /**< Switch whether sensitive ransom data
                                      has to be created. */
} IFAPI_Key_Create;

/** The data structure holding internal state of Fapi_EncryptDecrypt.
 */
typedef struct {
    char const *keyPath;            /**< The implicit key path */
    uint8_t const *in_data;
    size_t in_dataSize;
    IFAPI_OBJECT *key_object;       /**< The IPAPI object for the encryption key */
    ESYS_TR key_handle;                 /**< The ESYS handle of the encryption key */
    size_t numBytes;                /**< The number of bytes of a ESYS request */
    size_t decrypt;                 /**< Switch whether to encrypt or decrypt */
    UINT16 bytesRequested;          /**< Bytes currently requested from TPM */
    TPMT_RSA_DECRYPT rsa_scheme;
    ESYS_TR object_handle;
    char *policy_path;
    ESYS_TR auth_session;
    const IFAPI_PROFILE *profile;
    uint8_t *plainText;
    size_t plainTextSize;
    uint8_t *cipherText;
    size_t cipherTextSize;
} IFAPI_Data_EncryptDecrypt;

/** The states for signing  */
enum FAPI_SIGN_STATE {
    SIGN_INIT = 0,
    SIGN_WAIT_FOR_SESSION,
    SIGN_WAIT_FOR_KEY,
    SIGN_AUTH_SENT,
    SIGN_WAIT_FOR_FLUSH
};

/** The data structure holding internal state of Fapi_Sign.
 */
typedef struct {
    enum FAPI_SIGN_STATE state;          /**< The state of the signing operation */
    const char *keyPath;            /**< The implicit key path */
    ESYS_TR handle;                 /**< The ESYS handle of the signing key */
    TPM2B_DIGEST digest;            /**< The digest to be signed */
    TPMT_SIG_SCHEME scheme;         /**< The signature scheme from profile */
    IFAPI_OBJECT *key_object;       /**< The IPAPI object of the signing key */
    TPMT_SIGNATURE *tpm_signature;  /**< The signature in TPM format */
    TPMI_YES_NO decrypt;            /**< Switch for symmetric algs */
    TPMT_SIGNATURE *signature;      /**< Produced TPM singature */
    char const *padding;            /**< Optional padding parameter for key sign. */
    char *certificate;              /**< Certificate of the signing key. */
    uint8_t *ret_signature;         /**< Result signature */
    size_t signatureSize;
    char *publicKey;                /**< Public key of the signing key. */
} IFAPI_Key_Sign;

/** The data structure holding internal state of Fapi_Unseal.
 */
typedef struct {
    const char *keyPath;            /**< The implicit key path */
    IFAPI_OBJECT *object;           /**< The IPAPI object storing the data to be unsealed */
    TPM2B_SENSITIVE_DATA *unseal_data; /** The result of the esys unseal operation */
} IFAPI_Unseal;


/** The data structure holding internal state of Fapi_GetInfo.
 */
typedef struct {
    TPMS_CAPABILITY_DATA *capability_data;   /**< The TPM capability for one property */
    TPMS_CAPABILITY_DATA *fetched_data;       /**< The data fetched in one TPM command */
    size_t idx_info_cap;
    IFAPI_INFO  info_obj;
    UINT32 property_count;
    UINT32 property;
} IFAPI_GetInfo;

/** The states for the FAPI's hierarchy authorization state*/
enum IFAPI_HIERACHY_AUTHORIZATION_STATE {
    HIERARCHY_CHANGE_AUTH_INIT = 0,
    HIERARCHY_CHANGE_AUTH_NULL_AUTH_SENT,
    HIERARCHY_CHANGE_AUTH_AUTH_SENT
};

/** The states for the FAPI's change policy authorization state*/
enum IFAPI_HIERACHY_POLICY_AUTHORIZATION_STATE {
    HIERARCHY_CHANGE_POLICY_INIT = 0,
    HIERARCHY_CHANGE_POLICY_NULL_AUTH_SENT,
    HIERARCHY_CHANGE_POLICY_AUTHORIZE,
    HIERARCHY_CHANGE_POLICY_AUTH_SENT
};

/** The data structure holding internal state of Fapi_ChangeAuth.
 */
typedef struct {
    const char *entityPath;         /**< The implicit key path */
    ESYS_TR handle;                 /**< The ESYS handle of the key */
    IFAPI_OBJECT *key_object;       /**< The IPAPI object of the key */
    const char  *authValue;         /**< The new auth value */
    TPM2B_AUTH newAuthValue;        /**< The new auth value */
    TPM2B_PRIVATE *newPrivate;      /**< New private data created by parend */
    IFAPI_OBJECT object;            /**< Deserialized NV object or hierarchy */
    IFAPI_OBJECT hiearchy_object;   /**< Used for copying a hierarchy   */
    ESYS_TR nv_index;               /**< NV handle of the object to be changed */
    ESYS_TR hierarchy_handle;       /**< NV handle of the hierarchy to be changed */
    char **pathlist;                /**< The array with all keystore objects */
    size_t numPaths;                /**< Size of array with all keystore objects */
    size_t numPathsCleanup;         /**< Size of array with all keystore objects */
} IFAPI_Entity_ChangeAuth;

/** The data structure holding internal state of Fapi_AuthorizePolicy.
 */
typedef struct {
    const char *policyPath;           /**< Policy with Policy to be authorized */
    const char *signingKeyPath;       /**< Key for policy signing */
    TPM2B_DIGEST policyRef;
    TPMS_POLICYAUTHORIZATION  authorization;
} IFAPI_Fapi_AuthorizePolicy;

/** The data structure holding internal state of Fapi_WriteAuthorizeNv.
 */
typedef struct {
    const char *policyPath;            /**< Policy with Policy to be authorized */
    TPMI_ALG_HASH *hash_alg;           /**< The hash alg used for digest computation */
    size_t hash_size;                  /**< The digest size */
    size_t digest_idx;                 /**< The index of the digest in the policy */
} IFAPI_api_WriteAuthorizeNv;

/** The data structure holding internal state of Provisioning.
 */
typedef struct {
    IFAPI_OBJECT hierarchy_lockout; /**< The lockout hierarchy */
    IFAPI_OBJECT hierarchy_hs;      /**< The storage hierarchy */
    IFAPI_OBJECT hierarchy_he;      /**< The endorsement hierarchy */
    IFAPI_OBJECT hierarchy_hn;      /**< The null hierarchy */
    IFAPI_OBJECT *hierarchy;         /**< The current hierarchy */
    TPMS_POLICY *hierarchy_policy;  /**< Policy of the current used hierarchy. */
    IFAPI_KEY_TEMPLATE public_templ;  /**< The basic template for the keys public data */
    TPM2B_PUBLIC public;       /**< The public info of the created primary */
    char **pathlist;                /**< The array with all keystore objects */
    size_t numPaths;                /**< Size of array with all keystore objects */
    size_t numHierarchyObjects;      /**< Number of hierarchies stored in keystore */
    size_t hiearchy_idx;            /**< Index to the current hierarchy */
    size_t path_idx;                /**< Index of array with the object paths */
    IFAPI_OBJECT *hierarchies;     /**< Array of the hierarchies stored in keystore. */
    TPM2B_SENSITIVE_CREATE inSensitive;
    TPM2B_DATA outsideInfo;
    TPML_PCR_SELECTION creationPCR;
    ESYS_TR handle;
    const char *authValueLockout;
    const char *authValueEh;
    const char *policyPathEh;
    const char *authValueSh;
    const char *policyPathSh;
    size_t digest_idx;
    size_t hash_size;
    TPM2_HANDLE cert_nv_idx;
    TPM2B_NV_PUBLIC *nvPublic;
    ESYS_TR esys_nv_cert_handle;
    char *pem_cert;
    TPM2_ALG_ID cert_key_type;
    size_t cert_count;
    size_t cert_idx;
    TPMS_CAPABILITY_DATA *capabilityData;
    IFAPI_OBJECT hierarchy_object;
    TPM2B_AUTH hierarchy_auth;
    TPM2B_DIGEST policy_digest;
    char *intermed_crt;
    char *root_crt;
    TPMA_PERMANENT auth_state;
    ESYS_TR srk_esys_handle;
    ESYS_TR ek_esys_handle;
    ESYS_TR srk_tpm_handle;
    ESYS_TR ek_tpm_handle;
    bool srk_exists;
    TPM2_HANDLE template_nv_index;
    TPM2_HANDLE nonce_nv_index;
} IFAPI_Provision;

/** The data structure holding internal state of regenerate primary key.
 */
typedef struct {
    char *path;                   /**< Path of the primary (starting with hierarchy)  */
    IFAPI_OBJECT hierarchy;     /**< The current used hierarchy for CreatePrimary */
    IFAPI_OBJECT pkey_object;
    TPM2B_SENSITIVE_CREATE inSensitive;
    TPM2B_DATA outsideInfo;
    TPML_PCR_SELECTION creationPCR;
    ESYS_TR handle;
    TPMI_DH_PERSISTENT persistent_handle;
    TPMS_CAPABILITY_DATA *capabilityData;
} IFAPI_CreatePrimary;

/** The data structure holding internal state of key verify signature.
 */
typedef struct {
    const char    *keyPath;
    uint8_t const *signature;
    size_t         signatureSize;
    uint8_t const *digest;
    size_t         digestSize;
    IFAPI_OBJECT   key_object;
} IFAPI_Key_VerifySignature;

/** The states for the FAPI's policy loading */
enum IFAPI_STATE_POLICY {
    POLICY_INIT = 0,
    POLICY_READ,
    POLICY_READ_FINISH,
    POLICY_INSTANTIATE_PREPARE,
    POLICY_INSTANTIATE,
    POLICY_EXECUTE_PREPARE,
    POLICY_EXECUTE,
    POLICY_FLUSH
};

typedef struct IFAPI_POLICY_EXEC_CTX IFAPI_POLICY_EXEC_CTX;
typedef struct IFAPI_POLICYUTIL_STACK IFAPI_POLICYUTIL_STACK;

/** The states for session creation */
enum FAPI_CREATE_SESSION_STATE {
    CREATE_SESSION_INIT = 0,
    CREATE_SESSION,
    WAIT_FOR_CREATE_SESSION
};

/** The data structure holding internal policy state.
 */
typedef struct {
    enum IFAPI_STATE_POLICY state;
    struct TPMS_POLICY policy;
    size_t digest_idx;
    size_t hash_size;
    char **pathlist;                  /**< The array of all objects  in the search path */
    TPMI_ALG_HASH hash_alg;
    IFAPI_POLICY_EXEC_CTX *policy_stack; /**< The stack used for storing current policy information.
                                           e.g. for retry the current index of policy elements hash
                                           to be stored. */
    IFAPI_POLICYUTIL_STACK *util_current_policy;
    IFAPI_POLICYUTIL_STACK *policyutil_stack;
                                      /**< The stack used for storing current policy information.
                                            e.g. for retry the current index of policy elements hash
                                           to be stored. */
    ESYS_TR session;                  /**< Auxiliary variable to store created policy session.
                                           The value will also be stored in the policy stack */
    enum FAPI_CREATE_SESSION_STATE create_session_state;
    char *path;
    IFAPI_POLICY_EVAL_INST_CTX eval_ctx;
} IFAPI_POLICY_CTX;

/** The states for the IFAPI's policy loading */
enum IFAPI_STATE_FILE_SEARCH {
    FSEARCH_INIT = 0,
    FSEARCH_READ,
    FSEARCH_OBJECT
};

/** The data structure holding internal policy state.
 */
typedef struct {
    enum IFAPI_STATE_FILE_SEARCH state;
    char **pathlist;                /**< The array of all objects  in the search path */
    size_t path_idx;                /**< Index of array of objects to be searched */
    size_t numPaths;                /**< Number of all objects in data store */
    char *current_path;
} IFAPI_FILE_SEARCH_CTX;

/** The states for the FAPI's prepare key loading */
enum _FAPI_STATE_PREPARE_LOAD_KEY {
    PREPARE_LOAD_KEY_INIT = 0,
    PREPARE_LOAD_KEY_WAIT_FOR_SESSION,
    PREPARE_LOAD_KEY_INIT_KEY,
    PREPARE_LOAD_KEY_WAIT_FOR_KEY
};

/** The states for the FAPI's key loading */
enum _FAPI_STATE_LOAD_KEY {
    LOAD_KEY_GET_PATH = 0,
    LOAD_KEY_READ_KEY,
    LOAD_KEY_WAIT_FOR_PRIMARY,
    LOAD_KEY_LOAD_KEY,
    LOAD_KEY_AUTH,
    LOAD_KEY_AUTHORIZE
};

/** The data structure holding internal state of export key.
 */
typedef struct {
    char   const *pathOfKeyToDuplicate;          /**< The relative path of the key to be exported */
    char   const *pathToPublicKeyOfNewParent;    /**<  The relative path of the new parent */
    TPM2B_PUBLIC public_parent;                  /**< The public key of the new parent */
    IFAPI_OBJECT *key_object;                    /**< The IPAPI object of the key to be duplicated */
    IFAPI_OBJECT export_tree;                    /**< The complete tree to be exported */
    IFAPI_OBJECT pub_key;                        /**< The public part of the new parent */
    IFAPI_OBJECT dup_key;                        /**< The key to be duplicated or exported  */
    struct TPMS_POLICY policy;
    ESYS_TR handle_ext_key;
    char *exportedData;
} IFAPI_ExportKey;

/** The data structure holding internal state of export policy.
 */
typedef struct {
    char   const  *path;                          /**< Path of the object with the policy to be
                                                       exported */
    IFAPI_OBJECT  object;                         /**< Object corresponding to path */
    TPMS_POLICY   policy;                         /**< Policy from store be exported */
    TPMI_ALG_HASH hashAlg;                        /**< Index of profile used for digest computation. */
    size_t        profile_idx;                    /**< hashAlg used for policy digest computation. */
    bool         compute_policy;                  /**< Switch whether computation of the
                                                       policy for the default name hash alg
                                                       is needed. */
} IFAPI_ExportPolicy;

/** The data structure holding internal state of import key.
 */
typedef struct {
    IFAPI_OBJECT object;
    TPM2B_NAME parent_name;
    IFAPI_OBJECT *parent_object;
    IFAPI_OBJECT new_object;
    char *parent_path;
    char *out_path;
    TPM2B_PRIVATE *private;
    char *jso_string;
    const IFAPI_PROFILE *profile;
} IFAPI_ImportKey;


/** The data structure holding internal state of loading keys.
 */
typedef struct {
    enum _FAPI_STATE_LOAD_KEY state;   /**< The current state of key  loading */
    enum  _FAPI_STATE_PREPARE_LOAD_KEY prepare_state;
    NODE_STR_T *path_list;        /**< The current used hierarchy for CreatePrimary */
    NODE_OBJECT_T *key_list;
    IFAPI_OBJECT auth_object;
    size_t position;
    ESYS_TR handle;
    ESYS_TR parent_handle;
    bool parent_handle_persistent;
    IFAPI_OBJECT *key_object;
    char *key_path;
    char const *path;
} IFAPI_LoadKey;

/** The data structure holding internal state of entity delete.
 */
typedef struct {
    bool is_key;                    /**< Entity to be deleted is a key */
    bool is_persistent_key;         /**< Entity to be deleted is a key */
    ESYS_TR new_object_handle;
    TPM2_HANDLE permanentHandle;    /**< The TPM permanent handle */
    IFAPI_OBJECT auth_object;       /**< Object used for authentication */
    ESYS_TR auth_index;             /**< The ESAPI handle of the nv authorization object */
    char *path;                     /**< The name of the file to be deleted */
    IFAPI_OBJECT object;            /**< Deserialized object */
    char **pathlist;                /**< The array with the object files to be deleted */
    size_t numPaths;                /**< Size of array with the object files to be deleted */
    size_t path_idx;                /**< Index of array with the object files to be deleted */
} IFAPI_Entity_Delete;

/** The data structure holding internal state of esys get blob.
 */
typedef struct {
    uint8_t type;                   /**< type of blob to be returned */
    uint8_t *data;                   /**< data of the blob to be returned */
    size_t length;                  /**< The size of the data to be returned */
    bool is_key;                    /**< Object is a key */
    bool is_persistent_key;         /**< Object is a persistent key */
    ESYS_TR new_object_handle;
    TPM2_HANDLE permanentHandle;    /**< The TPM permanent handle */
    IFAPI_OBJECT auth_object;       /**< Object used for authentication */
    ESYS_TR auth_index;             /**< The ESAPI handle of the nv authorization object */
    char *path;                     /**< The path of the object */
    IFAPI_OBJECT object;            /**< Deserialized object */
    IFAPI_OBJECT *key_object;       /**< Loaded key object */
} IFAPI_GetEsysBlob;

/** The data structure holding internal state of list entities.
 */
typedef struct {
    const char *searchPath;               /**< The path to searched for objectws */
} IFAPI_Entities_List;

/** Union for all input parameters.
 *
 * The input parameters of a command need to be stored in order to enable
 * resubmission. This type provides the corresponding facilities.
 */
typedef union {
    IFAPI_Provision Provision;
    IFAPI_Key_Create Key_Create;
    IFAPI_Key_SetCertificate Key_SetCertificate;
    IFAPI_Entity_ChangeAuth Entity_ChangeAuth;
    IFAPI_Entity_Delete Entity_Delete;
    IFAPI_GetEsysBlob GetEsysBlob;
    IFAPI_Entities_List Entities_List;
    IFAPI_Key_VerifySignature Key_VerifySignature;
    IFAPI_Data_EncryptDecrypt Data_EncryptDecrypt;
    IFAPI_PCR pcr;
    IFAPI_INITIALIZE Initialize;
    IFAPI_Path_SetDescription path_set_info;
    IFAPI_Fapi_AuthorizePolicy Policy_AuthorizeNewPolicy;
    IFAPI_api_WriteAuthorizeNv WriteAuthorizeNV;
    IFAPI_ExportKey ExportKey;
    IFAPI_ImportKey ImportKey;
    IFAPI_Unseal Unseal;
    IFAPI_GetInfo GetInfo;
    IFAPI_ExportPolicy ExportPolicy;
} IFAPI_CMD_STATE;

/** The states for the FAPI's primary key regeneration */
enum _FAPI_STATE_PRIMARY {
    PRIMARY_INIT = 0,
    PRIMARY_READ_KEY,
    PRIMARY_READ_HIERARCHY,
    PRIMARY_READ_HIERARCHY_FINISH,
    PRIMARY_AUTHORIZE_HIERARCHY,
    PRIMARY_GET_AUTH_VALUE,
    PRIMARY_WAIT_FOR_PRIMARY,
    PRIMARY_HAUTH_SENT,
    PRIMARY_CREATED,
    PRIMARY_VERIFY_PERSISTENT,
    PRIMARY_GET_CAP
};

/** The states for the FAPI's primary key regeneration */
enum _FAPI_STATE_SESSION {
    SESSION_INIT = 0,
    SESSION_WAIT_FOR_PRIMARY,
    SESSION_CREATE_SESSION,
    SESSION_WAIT_FOR_SESSION1,
    SESSION_WAIT_FOR_SESSION2
};

/** The states for the FAPI's get random  state */
enum _FAPI_STATE_GET_RANDOM {
    GET_RANDOM_INIT = 0,
    GET_RANDOM_SENT
};

/** The states for flushing objects */
enum _FAPI_FLUSH_STATE {
    FLUSH_INIT = 0,
    WAIT_FOR_FLUSH
};

/** The states for the FAPI's internal state machine */
enum _FAPI_STATE {
    _FAPI_STATE_INIT = 0,         /**< The initial state after creation or after
                                     finishing a command. A new command can only
                                     be issued in this state. */
    _FAPI_STATE_INTERNALERROR,     /**< A non-recoverable error occurred within the
                                      ESAPI code. */
    INITIALIZE_READ,
    INITIALIZE_INIT_TCTI,
    INITIALIZE_GET_CAP,
    INITIALIZE_WAIT_FOR_CAP,
    INITIALIZE_READ_PROFILE,
    INITIALIZE_READ_PROFILE_INIT,
    INITIALIZE_READ_TIME,
    INITIALIZE_CHECK_NULL_PRIMARY,
    INITIALIZE_READ_NULL_PRIMARY,
    PROVISION_WAIT_FOR_GET_CAP_AUTH_STATE,
    PROVISION_WAIT_FOR_GET_CAP0,
    PROVISION_WAIT_FOR_GET_CAP1,
    PROVISION_INIT_GET_CAP2,
    PROVISION_WAIT_FOR_GET_CAP2,
    PROVISION_GET_CERT_NV,
    PROVISION_GET_CERT_NV_FINISH,
    PROVISION_GET_CERT_READ_PUBLIC,
    PROVISION_READ_CERT,
    PROVISION_PREPARE_READ_ROOT_CERT,
    PROVISION_READ_ROOT_CERT,
    PROVISION_PREPARE_READ_INT_CERT,
    PROVISION_READ_INT_CERT,
    PROVISION_INIT,
    PROVISION_INIT_SRK,
    PROVISION_WAIT_FOR_EK_SESSION,
    PROVISION_WAIT_FOR_SRK_SESSION,
    PROVISION_AUTH_EK_NO_AUTH_SENT,
    PROVISION_AUTH_EK_AUTH_SENT,
    PROVISION_AUTH_SRK_NO_AUTH_SENT,
    PROVISION_AUTH_SRK_AUTH_SENT,
    PROVISION_CLEAN_EK_SESSION,
    PROVISION_CLEAN_SRK_SESSION,
    PROVISION_EK_WRITE_PREPARE,
    PROVISION_EK_WRITE,
    PROVISION_EK_CHECK_CERT,
    PROVISION_SRK_WRITE_PREPARE,
    PROVISION_SRK_WRITE,
    PROVISION_WAIT_FOR_EK_PERSISTENT,
    PROVISION_WAIT_FOR_SRK_PERSISTENT,
    PROVISION_CHANGE_LOCKOUT_AUTH,
    PROVISION_CHANGE_EH_CHECK,
    PROVISION_CHANGE_EH_AUTH,
    PROVISION_CHANGE_SH_CHECK,
    PROVISION_CHANGE_SH_AUTH,
    PROVISION_EH_CHANGE_POLICY,
    PROVISION_SH_CHANGE_POLICY,
    PROVISION_LOCKOUT_CHANGE_POLICY,
    PROVISION_FINISHED,
    PROVISION_WRITE_SH,
    PROVISION_WRITE_EH,
    PROVISION_PREPARE_NULL,
    PROVISION_WRITE_NULL,
    PROVISION_WRITE_LOCKOUT,
    PROVISION_WRITE_LOCKOUT_PARAM,
    PROVISION_PREPARE_LOCKOUT_PARAM,
    PROVISION_AUTHORIZE_LOCKOUT,
    PROVISION_FLUSH_SRK,
    PROVISION_FLUSH_EK,
    PROVISION_CHECK_FOR_VENDOR_CERT,
    PROVISION_GET_VENDOR,
    PROVISION_GET_HIERARCHIES,
    PROVISION_READ_HIERARCHIES,
    PROVISION_READ_HIERARCHY,
    PROVISION_WRITE_HIERARCHIES,
    PROVISION_WRITE_HIERARCHY,
    PROVISION_PREPARE_GET_CAP_AUTH_STATE,
    PROVISION_SRK_GET_PERSISTENT_NAME,
    PROVISION_CHECK_SRK_EVICT_CONTROL,
    PROVISION_AUTHORIZE_HS_FOR_EK_EVICT,
    PROVISION_PREPARE_EK_EVICT,
    PROVISION_READ_EK_TEMPLATE,
    PROVISION_READ_EK_NONCE,

    KEY_CREATE,
    KEY_CREATE_PRIMARY,

    CREATE_SEAL,

    KEY_SET_CERTIFICATE_READ,
    KEY_SET_CERTIFICATE_WRITE,

    KEY_GET_CERTIFICATE_READ,

    GET_RANDOM_WAIT_FOR_SESSION,
    GET_RANDOM_WAIT_FOR_RANDOM,
    GET_RANDOM_CLEANUP,

    NV_CREATE_READ_PROFILE,
    NV_CREATE_READ_HIERARCHY,
    NV_CREATE_AUTHORIZE_HIERARCHY,
    NV_CREATE_GET_INDEX,
    NV_CREATE_FIND_INDEX,
    NV_CREATE_WAIT_FOR_SESSION,

    NV_CREATE_AUTH_SENT,
    NV_CREATE_WRITE,
    NV_CREATE_CALCULATE_POLICY,

    NV_WRITE_READ,
    NV_WRITE_WRITE,
    NV_WRITE_CLEANUP,

    NV_EXTEND_READ,
    NV_EXTEND_WAIT_FOR_SESSION,
    NV_EXTEND_AUTHORIZE,
    NV_EXTEND_AUTH_SENT,
    NV_EXTEND_WRITE,
    NV_EXTEND_CLEANUP,

    NV_INCREMENT_READ,
    NV_INCREMENT_WAIT_FOR_SESSION,
    NV_INCREMENT_AUTHORIZE,
    NV_INCREMENT_AUTH_SENT,
    NV_INCREMENT_WRITE,
    NV_INCREMENT_CLEANUP,

    NV_SET_BITS_READ,
    NV_SET_BITS_WAIT_FOR_SESSION,
    NV_SET_BITS_AUTHORIZE,
    NV_SET_BITS_AUTH_SENT,
    NV_SET_BITS_WRITE,
    NV_SET_BITS_CLEANUP,

    NV_READ_READ,
    NV_READ_WAIT,
    NV_READ_WAIT_FOR_SESSION,
    NV_READ_CLEANUP,

    ENTITY_DELETE_GET_FILE,
    ENTITY_DELETE_READ,
    ENTITY_DELETE_WAIT_FOR_SESSION,
    ENTITY_DELETE_NULL_AUTH_SENT_FOR_KEY,
    ENTITY_DELETE_AUTH_SENT_FOR_KEY,
    ENTITY_DELETE_NULL_AUTH_SENT_FOR_NV,
    ENTITY_DELETE_AUTH_SENT_FOR_NV,
    ENTITY_DELETE_KEY,
    ENTITY_DELETE_KEY_WAIT_FOR_HIERARCHY,
    ENTITY_DELETE_KEY_WAIT_FOR_AUTHORIZATION,
    ENTITY_DELETE_AUTHORIZE_NV,
    ENTITY_DELETE_FILE,
    ENTITY_DELETE_POLICY,
    ENTITY_DELETE_REMOVE_DIRS,
    ENTITY_DELETE_CLEANUP,
    ENTITY_DELETE_READ_HIERARCHY,

    GET_ESYS_BLOB_GET_FILE,
    GET_ESYS_BLOB_READ,
    GET_ESYS_BLOB_NULL_AUTH_SENT_FOR_KEY,
    GET_ESYS_BLOB_AUTH_SENT_FOR_KEY,
    GET_ESYS_BLOB_NULL_AUTH_SENT_FOR_NV,
    GET_ESYS_BLOB_AUTH_SENT_FOR_NV,
    GET_ESYS_BLOB_KEY,
    GET_ESYS_BLOB_WAIT_FOR_KEY,
    GET_ESYS_BLOB_WAIT_FOR_CONTEXT_SAVE,
    GET_ESYS_BLOB_SERIALIZE,
    GET_ESYS_BLOB_FILE,
    GET_ESYS_BLOB_WAIT_FOR_FLUSH,
    GET_ESYS_BLOB_CLEANUP,

    ENTITY_GET_TPM_BLOBS_READ,

    KEY_SIGN_WAIT_FOR_KEY,
    KEY_SIGN_WAIT_FOR_SIGN,
    KEY_SIGN_CLEANUP,

    ENTITY_CHANGE_AUTH_WAIT_FOR_SESSION,
    ENTITY_CHANGE_AUTH_WAIT_FOR_KEY,
    ENTITY_CHANGE_AUTH_AUTH_SENT,
    ENTITY_CHANGE_AUTH_WAIT_FOR_FLUSH,
    ENTITY_CHANGE_AUTH_WRITE_PREPARE,
    ENTITY_CHANGE_AUTH_WRITE,
    ENTITY_CHANGE_AUTH_WAIT_FOR_KEY_AUTH,
    ENTITY_CHANGE_AUTH_WAIT_FOR_NV_READ,
    ENTITY_CHANGE_AUTH_WAIT_FOR_NV_AUTH,
    ENTITY_CHANGE_AUTH_WAIT_FOR_NV_CHANGE_AUTH,
    ENTITY_CHANGE_AUTH_HIERARCHY_CHANGE_AUTH,
    ENTITY_CHANGE_AUTH_HIERARCHY_READ,
    ENTITY_CHANGE_AUTH_HIERARCHY_AUTHORIZE,
    ENTITY_CHANGE_AUTH_SAVE_HIERARCHIES_PREPARE,
    ENTITY_CHANGE_AUTH_SAVE_HIERARCHIES_FINISH,
    ENTITY_CHANGE_AUTH_CLEANUP,

    DATA_ENCRYPT_WAIT_FOR_PROFILE,
    DATA_ENCRYPT_WAIT_FOR_SESSION,
    DATA_ENCRYPT_WAIT_FOR_KEY,
    DATA_ENCRYPT_WAIT_FOR_FLUSH,
    DATA_ENCRYPT_WAIT_FOR_RSA_ENCRYPTION,
    DATA_ENCRYPT_CLEAN,

    DATA_DECRYPT_WAIT_FOR_PROFILE,
    DATA_DECRYPT_WAIT_FOR_SESSION,
    DATA_DECRYPT_WAIT_FOR_KEY,
    DATA_DECRYPT_WAIT_FOR_FLUSH,
    DATA_DECRYPT_WAIT_FOR_RSA_DECRYPTION,
    DATA_DECRYPT_AUTHORIZE_KEY,
    DATA_DECRYPT_CLEANUP,

    PCR_EXTEND_WAIT_FOR_SESSION,
    PCR_EXTEND_WAIT_FOR_GET_CAP,
    PCR_EXTEND_READ_EVENT_LOG,
    PCR_EXTEND_APPEND_EVENT_LOG,
    PCR_EXTEND_FINISH,
    PCR_EXTEND_CLEANUP,

    PCR_READ_READ_PCR,
    PCR_READ_READ_EVENT_LIST,

    PCR_QUOTE_WAIT_FOR_GET_CAP,
    PCR_QUOTE_WAIT_FOR_SESSION,
    PCR_QUOTE_WAIT_FOR_KEY,
    PCR_QUOTE_AUTH_SENT,
    PCR_QUOTE_AUTHORIZE,
    PCR_QUOTE_WAIT_FOR_FLUSH,
    PCR_QUOTE_READ_EVENT_LIST,
    PCR_QUOTE_CLEANUP,

    PATH_SET_DESCRIPTION_READ,
    PATH_SET_DESCRIPTION_WRITE,

    PATH_GET_DESCRIPTION_READ,

    APP_DATA_SET_READ,
    APP_DATA_SET_WRITE,

    AUTHORIZE_NEW_CALCULATE_POLICY,
    AUTHORIZE_NEW_LOAD_KEY,
    AUTHORIZE_NEW_KEY_SIGN_POLICY,
    AUTHORIZE_NEW_WRITE_POLICY_PREPARE,
    AUTHORIZE_NEW_WRITE_POLICY,
    AUTHORIZE_NEW_CLEANUP,

    WRITE_AUTHORIZE_NV_READ_NV,
    WRITE_AUTHORIZE_NV_CALCULATE_POLICY,
    WRITE_AUTHORIZE_NV_WRITE_NV_RAM_PREPARE,
    WRITE_AUTHORIZE_NV_WRITE_NV_RAM,
    WRITE_AUTHORIZE_NV_WRITE_OBJCECT,
    WRITE_AUTHORIZE_NV_WRITE_POLICY_PREPARE,
    WRITE_AUTHORIZE_NV_WRITE_POLICY,
    WRITE_AUTHORIZE_NV_CLEANUP,

    EXPORT_KEY_READ_PUB_KEY,
    EXPORT_KEY_READ_PUB_KEY_PARENT,
    EXPORT_KEY_WAIT_FOR_KEY,
    EXPORT_KEY_WAIT_FOR_DUPLICATE,
    EXPORT_KEY_WAIT_FOR_EXT_KEY,
    EXPORT_KEY_WAIT_FOR_AUTHORIZATON,
    EXPORT_KEY_WAIT_FOR_FLUSH1,
    EXPORT_KEY_WAIT_FOR_FLUSH2,
    EXPORT_KEY_CLEANUP,

    IMPORT_KEY_WRITE_POLICY,
    IMPORT_KEY_WRITE,
    IMPORT_KEY_SEARCH,
    IMPORT_KEY_LOAD_PARENT,
    IMPORT_KEY_AUTHORIZE_PARENT,
    IMPORT_KEY_IMPORT,
    IMPORT_KEY_WAIT_FOR_FLUSH,
    IMPORT_KEY_WRITE_OBJECT_PREPARE,
    IMPORT_KEY_WRITE_OBJECT,
    IMPORT_KEY_CLEANUP,
    IMPORT_WAIT_FOR_SESSION,
    IMPORT_WAIT_FOR_PARENT,
    IMPORT_WAIT_FOR_AUTHORIZATION,
    IMPORT_WAIT_FOR_KEY,
    IMPORT_WRITE,
    IMPORT_FLUSH_PARENT,
    IMPORT_FLUSH_KEY,
    IMPORT_CLEANUP,

    UNSEAL_WAIT_FOR_KEY,
    UNSEAL_AUTHORIZE_OBJECT,
    UNSEAL_WAIT_FOR_UNSEAL,
    UNSEAL_WAIT_FOR_FLUSH,
    UNSEAL_CLEANUP,

    GET_PLATFORM_CERTIFICATE,

    POLICY_EXPORT_READ_OBJECT,
    POLICY_EXPORT_READ_OBJECT_FINISH,
    POLICY_EXPORT_READ_POLICY,
    POLICY_EXPORT_READ_POLICY_FINISH,
    POLICY_EXPORT_CHECK_DIGEST,
    POLICY_EXPORT_COMPUTE_POLICY_DIGEST,

    VERIFY_QUOTE_READ,

    GET_INFO_GET_CAP,
    GET_INFO_GET_CAP_MORE,
    GET_INFO_WAIT_FOR_CAP
};

/** Structure holding FAPI callbacks and userData
 *
 * This structure holds the callback pointers and corresponding userData pointers for each of the
 * three callback types of FAPI. They are set using Fapi_SetAuthCB, Fapi_SetBranchCB and
 * Fapi_SetSignCB.
 */
struct IFAPI_CALLBACKS {
    Fapi_CB_Auth auth;
    void *authData;
    Fapi_CB_Branch branch;
    void *branchData;
    Fapi_CB_Sign sign;
    void *signData;
    Fapi_CB_PolicyAction action;
    void *actionData;
};

/** The data structure holding internal state information.
 *
 * Each FAPI_CONTEXT respresents a logically independent connection to the TPM.
 * It stores meta data information about object in order to calculate session
 * auths and similar things.
 */
struct FAPI_CONTEXT {
    ESYS_CONTEXT *esys;              /**< The ESYS context used internally to talk to
                                          the TPM. */
    struct IFAPI_CALLBACKS callbacks;       /**< Callbacks for user interaction from FAPI */
    struct IFAPI_IO io;
    struct IFAPI_EVENTLOG eventlog;
    struct IFAPI_KEYSTORE keystore;
    struct IFAPI_POLICY_STORE pstore;
    struct IFAPI_PROFILES profiles;
    TPMS_TIME_INFO init_time;        /**< The current time during FAPI initialization. **/

    enum _FAPI_STATE state;          /**< The current state of the command execution */
    enum _FAPI_STATE_PRIMARY primary_state; /**< The current state of the primary regeneration */
    enum _FAPI_STATE_SESSION session_state; /**< The current state of the session creation */
    enum _FAPI_STATE_GET_RANDOM get_random_state; /**< The current state of get random */
    enum IFAPI_HIERACHY_AUTHORIZATION_STATE hierarchy_state;
    enum IFAPI_HIERACHY_POLICY_AUTHORIZATION_STATE hierarchy_policy_state;
    enum IFAPI_GET_CERT_STATE get_cert_state;
    enum _FAPI_FLUSH_STATE flush_object_state;  /**< The current state of a flush operation */
    enum IFAPI_CLEANUP_STATE cleanup_state;     /**< The state of cleanup after command execution */
    enum IFAPI_READ_NV_PUBLIC_STATE read_nv_public_state;
    IFAPI_CONFIG config;             /**< The profile independent configuration data */
    UINT32 nv_buffer_max;            /**< The maximal size for transfer of nv buffer content */
    IFAPI_CMD_STATE cmd;             /**< The state information of the currently executed
                                          command */
    IFAPI_NV_Cmds nv_cmd;
    IFAPI_GetRandom get_random;
    IFAPI_CreatePrimary createPrimary;
    IFAPI_LoadKey loadKey;
    ESYS_TR session1;                /**< The first session used by FAPI  */
    ESYS_TR session2;                /**< The second session used by FAPI  */
    ESYS_TR policy_session;          /**< The policy session used by FAPI  */
    ESYS_TR ek_handle;
    ESYS_TR srk_handle;
    TPMI_DH_PERSISTENT ek_persistent;
    TPMI_DH_PERSISTENT srk_persistent;
    IFAPI_SESSION_TYPE session_flags;
    TPMA_SESSION session1_attribute_flags;
    TPMA_SESSION session2_attribute_flags;
    IFAPI_MAX_BUFFER aux_data; /**< tpm2b data to be transferred */
    IFAPI_POLICY_CTX policy;  /**< The context of current policy. */
    IFAPI_FILE_SEARCH_CTX fsearch;  /**< The context for object search in key/policy store */
    IFAPI_Key_Sign Key_Sign; /**< State information for key signing */
    enum IFAPI_IO_STATE io_state;
    NODE_OBJECT_T *object_list;
    IFAPI_OBJECT *duplicate_key; /**< Will be needed for policy execution */
    IFAPI_OBJECT *current_auth_object;
};

#define VENDOR_IFX  0x49465800
#define VENDOR_INTC 0x494E5443
#define VEDNOR_IBM  0x49424D20

#endif /* FAPI_INT_H */
