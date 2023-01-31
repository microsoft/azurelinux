/* SPDX-License-Identifier: BSD-2-Clause */
/*******************************************************************************
 * Copyright 2017, Fraunhofer SIT sponsored by Infineon Technologies AG
 * All rights reserved.
 *******************************************************************************/
#ifndef ESYS_INT_H
#define ESYS_INT_H

#include <stdint.h>
#include "esys_crypto.h"
#include "esys_types.h"

#ifdef __cplusplus
extern "C" {
#endif

/** Linked list type for object meta data.
 *
 * This structure represents a linked list to store meta data information of
 * type IESYS_RESOURCE.
 */
typedef struct RSRC_NODE_T {
    ESYS_TR esys_handle;        /**< The ESYS_TR handle used by the application
                                     to reference this entry. */
    TPM2B_AUTH auth;            /**< The authValue for this resource object. */
    IESYS_RESOURCE rsrc;        /**< The meta data for this resource object. */
    struct RSRC_NODE_T * next;  /**< The next object in the linked list. */
} RSRC_NODE_T;

typedef struct {
    ESYS_TR tpmKey;
    ESYS_TR bind;
    TPM2_SE sessionType;
    TPMI_ALG_HASH authHash;
    TPM2B_NONCE *nonceCaller;
    TPM2B_NONCE nonceCallerData;
    TPMT_SYM_DEF *symmetric;
    TPMT_SYM_DEF symmetricData;
} StartAuthSession_IN;

typedef struct {
    TPM2B_SENSITIVE_CREATE *inSensitive;
    TPM2B_SENSITIVE_CREATE inSensitiveData;
} CreatePrimary_IN;

typedef struct {
    TPM2B_SENSITIVE_CREATE *inSensitive;
    TPM2B_SENSITIVE_CREATE inSensitiveData;
} Create_IN;

typedef struct {
    ESYS_TR saveHandle;
} ContextSave_IN;

typedef struct {
    TPMS_CONTEXT *context;
    TPMS_CONTEXT contextData;
} ContextLoad_IN;

typedef struct {
    TPM2B_PUBLIC *inPublic;
    TPM2B_PUBLIC inPublicData;
} Load_IN;

typedef struct {
    TPM2B_PUBLIC *inPublic;
    TPM2B_PUBLIC inPublicData;
} LoadExternal_IN;

typedef struct {
    TPM2B_SENSITIVE_CREATE *inSensitive;
    TPM2B_SENSITIVE_CREATE inSensitiveData;
    TPM2B_TEMPLATE *inPublic;
    TPM2B_TEMPLATE inPublicData;
} CreateLoaded_IN;

typedef struct {
    ESYS_TR objectHandle;
    TPMI_DH_PERSISTENT persistentHandle;
} EvictControl_IN;

typedef struct {
    TPM2B_AUTH authData;
} HMAC_Start_IN;

typedef HMAC_Start_IN MAC_Start_IN;

typedef struct {
    ESYS_TR authHandle;
    TPM2B_AUTH newAuth;
} HierarchyChangeAuth_IN;

typedef struct {
    ESYS_TR sequenceHandle;
} SequenceComplete_IN;

typedef struct {
    ESYS_TR policySession;
} Policy_IN;

typedef struct {
    ESYS_TR nvIndex;
    TPM2B_AUTH authData;
    TPM2B_NV_PUBLIC *publicInfo;
    TPM2B_NV_PUBLIC publicInfoData;
} NV_IN;

typedef struct {
    ESYS_TR flushHandle;
} FlushContext_IN;

typedef struct {
    ESYS_TR pcrHandle;
    TPM2B_AUTH authData;
} PCR_IN;

/** Union for input parameters.
 *
 * The input parameters of a command need to be stored if they are needed
 * in corresponding _Finish() function.
 */
typedef union {
    StartAuthSession_IN StartAuthSession;
    CreatePrimary_IN CreatePrimary;
    Create_IN Create;
    ContextSave_IN ContextSave;
    ContextLoad_IN ContextLoad;
    Load_IN Load;
    LoadExternal_IN LoadExternal;
    CreateLoaded_IN CreateLoaded;
    EvictControl_IN EvictControl;
    HMAC_Start_IN HMAC_Start;
    MAC_Start_IN MAC_Start;
    HierarchyChangeAuth_IN HierarchyChangeAuth;
    SequenceComplete_IN SequenceComplete;
    Policy_IN Policy;
    NV_IN NV;
    FlushContext_IN FlushContext;
    PCR_IN PCR;
} IESYS_CMD_IN_PARAM;

/** The states for the ESAPI's internal state machine */
enum _ESYS_STATE {
    _ESYS_STATE_INIT = 0,     /**< The initial state after creation or after
                                   finishing a command. A new command can only
                                   be issued in this state. */
    _ESYS_STATE_SENT,         /**< The state after sending a command to the TPM
                                   before receiving a response. */
    _ESYS_STATE_RESUBMISSION, /**< The state after receiving a response from the
                                   TPM that requires resending of the command.*/
    _ESYS_STATE_INTERNALERROR /**< A non-recoverable error occured within the
                                   ESAPI code. */
};

/** The data structure holding internal state information.
 *
 * Each ESYS_CONTEXT respresents a logically independent connection to the TPM.
 * It stores meta data information about object in order to calculate session
 * auths and similar things.
 */
struct ESYS_CONTEXT {
    enum _ESYS_STATE state;      /**< The current state of the ESAPI context. */
    TSS2_SYS_CONTEXT *sys;       /**< The SYS context used internally to talk to
                                      the TPM. */
    ESYS_TR esys_handle_cnt;     /**< The next free ESYS_TR number. */
    RSRC_NODE_T *rsrc_list;      /**< The linked list of all ESYS_TR objects. */
    int32_t timeout;             /**< The timeout to be used during
                                      Tss2_Sys_ExecuteFinish. */
    ESYS_TR session_type[3];     /**< The list of TPM session handles in the
                                      current command execution. */
    RSRC_NODE_T *session_tab[3]; /**< The list of TPM session meta data in the
                                      current command execution. */
    int encryptNonceIdx;         /**< The index of the encrypt session. */
    TPM2B_NONCE *encryptNonce;   /**< The nonce of the encrypt session, or NULL
                                      if no encrypt session exists. */
    int authsCount;              /**< The number of session provided during the
                                      command. */
    int submissionCount;         /**< The current number of submissions of this
                                      command to the TPM. */
    TPM2B_DATA salt;             /**< The salt used during a StartAuthSession.*/
    IESYS_CMD_IN_PARAM in;       /**< Temporary storage for Input parameters
                                      needed in corresponding _Finish function*/
    ESYS_TR esys_handle;         /**< Temporary storage for the object's TPM
                                      handle during Esys_TR_FromTPMPublic. */
    TSS2_TCTI_CONTEXT *tcti_app_param;/**< The TCTI context provided by the
                                           application during Esys_Initialize()
                                           to be returned from Esys_GetTcti().*/
    void *dlhandle;              /**< The handle of dlopen if the tcti was
                                      automatically loaded. */
    IESYS_SESSION *enc_session;  /**< Ptr to the enc param session.
                                      Used to restore session attributes */
    ESYS_TR sav_session1;        /**< Used to store session for cases where call
                                      with ESYS_TR_NONE is needed to determine object
                                      name */
    ESYS_TR sav_session2;
    ESYS_TR sav_session3;

    ESYS_CRYPTO_CALLBACKS crypto_backend; /**< The backend function pointers to use
                                              for crypto operations */
};

/** The number of authomatic resubmissions.
 *
 * The number of resubmissions before a TPM's TPM2_RC_YIELDED is forwarded to
 * the application.
 */
#define _ESYS_MAX_SUBMISSIONS 5

/** Makro testing parameters against null.
 */
#define _ESYS_ASSERT_NON_NULL(x) \
    if (x == NULL) { \
        LOG_ERROR(str(x) " == NULL."); \
        return TSS2_ESYS_RC_BAD_REFERENCE; \
    }

#ifdef __cplusplus
}
#endif
#endif /* ESYS_INT_H */
