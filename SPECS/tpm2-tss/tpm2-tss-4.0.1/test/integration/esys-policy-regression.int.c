/* SPDX-License-Identifier: BSD-2-Clause */
/*******************************************************************************
 * Copyright 2017-2018, Fraunhofer SIT sponsored by Infineon Technologies AG
 * All rights reserved.
 *******************************************************************************/

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include "tss2_esys.h"
#include "tss2_mu.h"

#include "esys_iutil.h"
#include "test-esys.h"
#define LOGMODULE test
#include "util/log.h"
#include "util/aux_util.h"

#define FLUSH true
#define NOT_FLUSH false

/*
 * Function to compare policy digest with expected digest.
 * The digest is computed with Esys_PolicyGetDigest.
 */
bool
cmp_policy_digest(ESYS_CONTEXT * esys_context,
                  ESYS_TR * session,
                  TPM2B_DIGEST * expected_digest,
                  char *comment, bool flush_session)
{

    TSS2_RC r;
    TPM2B_DIGEST *policyDigest;

    r = Esys_PolicyGetDigest(esys_context,
                             *session,
                             ESYS_TR_NONE,
                             ESYS_TR_NONE, ESYS_TR_NONE, &policyDigest);
    goto_if_error(r, "Error: PolicyGetDigest", error);

    LOGBLOB_DEBUG(&policyDigest->buffer[0], policyDigest->size,
                  "POLICY DIGEST");

    if (policyDigest->size != 32
        || memcmp(&policyDigest->buffer[0], &expected_digest->buffer[0],
                  policyDigest->size)) {
        free(policyDigest);
        LOG_ERROR("Error: Policy%s digest did not match expected policy.",
                  comment);
        return false;
    }
    free(policyDigest);
    if (flush_session) {
        r = Esys_FlushContext(esys_context, *session);
        goto_if_error(r, "Error: PolicyGetDigest", error);
        *session = ESYS_TR_NONE;
    }

    return true;

 error:
    return false;
}

/** This test is intended to test the ESYS policy commands, not tested
 *  in other test cases.
 *  When possoble the commands are tested with a
 * trial session and the policy digest is compared with the expected digest.
 *
 * Tested ESYS commands:
 *  - Esys_FlushContext() (M)
 *  - Esys_NV_DefineSpace() (M)
 *  - Esys_NV_UndefineSpace() (M)
 *  - Esys_PolicyCounterTimer() (M)
 *  - Esys_PolicyDuplicationSelect() (M)
 *  - Esys_PolicyGetDigest() (M)
 *  - Esys_PolicyNV() (M)
 *  - Esys_PolicyNameHash() (M)
 *  - Esys_PolicyNvWritten() (M)
 *  - Esys_PolicyOR() (M)
 *  - Esys_PolicyPCR() (M)
 *  - Esys_PolicyPhysicalPresence() (O)
 *  - Esys_PolicyRestart() (M)
 *  - Esys_SetPrimaryPolicy() (M)
 *  - Esys_StartAuthSession() (M)
 *
 * @param[in,out] esys_context The ESYS_CONTEXT.
 * @retval EXIT_FAILURE
 * @retval EXIT_SKIP
 * @retval EXIT_SUCCESS
 */
int
test_esys_policy_regression(ESYS_CONTEXT * esys_context)
{
    TSS2_RC r;
    int failure_return = EXIT_FAILURE;
    ESYS_TR nvHandle = ESYS_TR_NONE;
    ESYS_TR sessionTrialNV = ESYS_TR_NONE;
    ESYS_TR sessionTrialPCR = ESYS_TR_NONE;

    /* Dummy parameters for trial sessoin  */
    ESYS_TR sessionTrial = ESYS_TR_NONE;
    TPMT_SYM_DEF symmetricTrial = {.algorithm = TPM2_ALG_AES,
        .keyBits = {.aes = 128},
        .mode = {.aes = TPM2_ALG_CFB}
    };
    TPM2B_NONCE nonceCallerTrial = {
        .size = 32,
        .buffer = { 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,11, 12, 13, 14, 15, 16, 17,
                    18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32 }
    };

    /*
     * Test PolicyPCR
     */
    r = Esys_StartAuthSession(esys_context, ESYS_TR_NONE, ESYS_TR_NONE,
                              ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE,
                              &nonceCallerTrial,
                              TPM2_SE_TRIAL, &symmetricTrial, TPM2_ALG_SHA256,
                              &sessionTrial);
    goto_if_error(r, "Error: During initialization of policy trial session",
                  error);

    sessionTrialPCR = sessionTrial;
    TPML_PCR_SELECTION pcrSelection = {
        .count = 1,
        .pcrSelections = {
                          {.hash = TPM2_ALG_SHA256,
                           .sizeofSelect = 3,
                           .pcrSelect = {00, 00, 01},
                           },
                          }
    };
    /* SHA256 digest for PCR register */
    TPM2B_DIGEST pcr_digest_zero = {
        .size = 32,
        .buffer = { 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,11, 12, 13, 14, 15, 16, 17,
                    18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32}
    };

    r = Esys_PolicyPCR(esys_context,
                       sessionTrial,
                       ESYS_TR_NONE,
                       ESYS_TR_NONE,
                       ESYS_TR_NONE, &pcr_digest_zero, &pcrSelection);
    goto_if_error(r, "Error: pcr digest can not be computed.", error);

    TPM2B_DIGEST expectedPolicyPCR = {
        .size = 32,
        .buffer = { 0xd0, 0x0d, 0x71, 0x64, 0xc2, 0x38, 0xc0, 0xec, 0x47, 0x87, 0x3d,
                    0x71, 0x2d, 0x1e, 0xd8, 0x78, 0xb0, 0x62, 0xd1, 0x36, 0x9e, 0xe8,
                    0x3b, 0xc4, 0x8c, 0xdf, 0x05, 0x3f, 0x6b, 0x8e, 0xd9, 0x53 }
    };

    if (!cmp_policy_digest(esys_context, &sessionTrial, &expectedPolicyPCR,
                           "PCR", NOT_FLUSH))
        goto error;

    /* Create valid NV handle */
    TPM2B_AUTH auth = {.size = 20,
        .buffer = {10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
                   20, 21, 22, 23, 24, 25, 26, 27, 28, 29}
    };

    TPM2B_NV_PUBLIC publicInfo = {
        .size = 0,
        .nvPublic = {
                     .nvIndex = TPM2_NV_INDEX_FIRST,
                     .nameAlg = TPM2_ALG_SHA256,
                     .attributes = (TPMA_NV_OWNERWRITE |
                                    TPMA_NV_AUTHWRITE |
                                    TPMA_NV_WRITE_STCLEAR |
                                    TPMA_NV_READ_STCLEAR |
                                    TPMA_NV_AUTHREAD | TPMA_NV_OWNERREAD),
                     .authPolicy = {
                                    .size = 0,
                                    .buffer = {}
                                    ,
                                    }
                     ,
                     .dataSize = 32,
                     }
    };

    r = Esys_NV_DefineSpace(esys_context,
                            ESYS_TR_RH_OWNER,
                            ESYS_TR_PASSWORD,
                            ESYS_TR_NONE,
                            ESYS_TR_NONE, &auth, &publicInfo, &nvHandle);

    goto_if_error(r, "Error esys define nv space", error);

    /*
     * Test PolicyNV
     */
    r = Esys_StartAuthSession(esys_context, ESYS_TR_NONE, ESYS_TR_NONE,
                              ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE,
                              &nonceCallerTrial,
                              TPM2_SE_TRIAL, &symmetricTrial, TPM2_ALG_SHA256,
                              &sessionTrial);
    goto_if_error(r, "Error: During initialization of policy trial session",
                  error);

    sessionTrialNV = sessionTrial;
    UINT16 offset = 0;
    TPM2_EO operation = TPM2_EO_EQ;
    TPM2B_OPERAND operandB = {
        .size = 8,
        .buffer = {0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x08, 0x09}
    };

    r = Esys_PolicyNV(esys_context,
                      ESYS_TR_RH_OWNER,
                      nvHandle,
                      sessionTrial,
                      ESYS_TR_PASSWORD,
                      ESYS_TR_NONE, ESYS_TR_NONE, &operandB, offset, operation);
    goto_if_error(r, "Error: PolicyNV", error);

    TPM2B_DIGEST expectedPolicyNV = {
        .size = 32,
        .buffer = { 0xe3, 0x60, 0x27, 0x10, 0xe7, 0x58, 0x18, 0xc5, 0x96, 0xed, 0xf4,
                    0x32, 0x6a, 0x84, 0x06, 0x65, 0x85, 0x8e, 0x67, 0x8b, 0x0c, 0xb7,
                    0x0f, 0x60, 0x85, 0xc9, 0xa6, 0xc5, 0xb1, 0x4e, 0x22, 0x45 }
    };

    if (!cmp_policy_digest(esys_context, &sessionTrial, &expectedPolicyNV,
                           "NV", NOT_FLUSH))
        goto error;

    /*
     * Test PolicyOR
     */

    r = Esys_StartAuthSession(esys_context, ESYS_TR_NONE, ESYS_TR_NONE,
                              ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE,
                              &nonceCallerTrial,
                              TPM2_SE_TRIAL, &symmetricTrial, TPM2_ALG_SHA256,
                              &sessionTrial);
    goto_if_error(r, "Error: During initialization of policy trial session",
                  error);

    TPML_DIGEST pHashList = {
        .count = 2,
        .digests = {
                    expectedPolicyPCR,
                    expectedPolicyNV}
    };

    r = Esys_PolicyOR(esys_context,
                      sessionTrial,
                      ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE, &pHashList);

    goto_if_error(r, "Error: PolicyOR", error);

    TPM2B_DIGEST expectedPolicyOR = {
        .size = 32,
        .buffer = { 0x87, 0x92, 0xce, 0xbb, 0x01, 0x65, 0x1e, 0x20, 0x5a, 0x18, 0x67,
                    0x18, 0x4c, 0x93, 0x26, 0x6e, 0xa1, 0x15, 0x12, 0xc1, 0xfe, 0x3f,
                    0x02, 0x6d, 0x90, 0x7d, 0x14, 0xb4, 0x6a, 0xae, 0x80, 0x5d }
    };

    if (!cmp_policy_digest(esys_context, &sessionTrial, &expectedPolicyOR,
                           "OR", FLUSH))
        goto error;

    r = Esys_FlushContext(esys_context, sessionTrialPCR);
    goto_if_error(r, "Error: FlushContext", error);
    sessionTrialPCR = ESYS_TR_NONE;

    r = Esys_FlushContext(esys_context, sessionTrialNV);
    goto_if_error(r, "Error: FlushContext", error);
    sessionTrial = ESYS_TR_NONE;

    /*
     * Test PolicyCounterTimer
     */
    r = Esys_StartAuthSession(esys_context, ESYS_TR_NONE, ESYS_TR_NONE,
                              ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE,
                              &nonceCallerTrial,
                              TPM2_SE_TRIAL, &symmetricTrial, TPM2_ALG_SHA256,
                              &sessionTrial);
    goto_if_error(r, "Error: During initialization of policy trial session",
                  error);

    r = Esys_PolicyCounterTimer(esys_context,
                                sessionTrial,
                                ESYS_TR_NONE,
                                ESYS_TR_NONE,
                                ESYS_TR_NONE, &operandB, offset, operation);
    goto_if_error(r, "Error: PolicyCounterTimer", error);

    TPM2B_DIGEST expectedPolicyCounterTimer = {
        .size = 32,
        .buffer = { 0x47, 0x47, 0xae, 0xce, 0xa4, 0x17, 0x9c, 0x60, 0xdd, 0x82, 0xfc, 0x18,
                    0xc5, 0xa7, 0x58, 0xad, 0xa0, 0xe8, 0xa7, 0x19, 0xc8, 0x61, 0xac, 0xa3,
                    0xf4, 0xca, 0x85, 0xcf, 0xf6, 0x32, 0x6d, 0x64 }
    };

    if (!cmp_policy_digest
        (esys_context, &sessionTrial, &expectedPolicyCounterTimer,
         "CounterTimter", NOT_FLUSH))
        goto error;

    /*
     * Test PolicyRestart
     */
    r = Esys_PolicyRestart(esys_context,
                           sessionTrial,
                           ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE);
    goto_if_error(r, "Error: PolicyRestart", error);

    TPM2B_DIGEST expectedPolicyRestart = {
        .size = 0,
        .buffer = {0}
    };

    if (!cmp_policy_digest(esys_context, &sessionTrial, &expectedPolicyRestart,
                           "Restart", FLUSH))
        goto error;

    /*
     * Test PolicyNameHash
     */
    r = Esys_StartAuthSession(esys_context, ESYS_TR_NONE, ESYS_TR_NONE,
                              ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE,
                              &nonceCallerTrial,
                              TPM2_SE_TRIAL, &symmetricTrial, TPM2_ALG_SHA256,
                              &sessionTrial);
    goto_if_error(r, "Error: During initialization of policy trial session",
                  error);

    TPM2B_DIGEST nameHash = {
        .size = 32,
        .buffer = { 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,11, 12, 13, 14, 15, 16, 17,
                    18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32}
    };

    r = Esys_PolicyNameHash(esys_context,
                            sessionTrial,
                            ESYS_TR_NONE,
                            ESYS_TR_NONE, ESYS_TR_NONE, &nameHash);
    goto_if_error(r, "Error: PolicyNameHash", error);

    TPM2B_DIGEST expectedPolicyNameHash = {
        .size = 32,
        .buffer = { 0xeb, 0xc8, 0x0e, 0xb9, 0xb6, 0x6d, 0xb3, 0xc4, 0xee, 0x55, 0x53,
                    0xa4, 0xbc, 0x87, 0xbd, 0xa4, 0x0f, 0x2e, 0x9e, 0xc2, 0xa6, 0x76,
                    0xa7, 0x05, 0x70, 0x4b, 0x4d, 0x15, 0x31, 0x50, 0xdf, 0xa9 }
    };

    if (!cmp_policy_digest(esys_context, &sessionTrial, &expectedPolicyNameHash,
                           "NameHash", FLUSH))
        goto error;

    /*
     * Test PolicyDuplicationSelect
     */
    r = Esys_StartAuthSession(esys_context, ESYS_TR_NONE, ESYS_TR_NONE,
                              ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE,
                              &nonceCallerTrial,
                              TPM2_SE_TRIAL, &symmetricTrial, TPM2_ALG_SHA256,
                              &sessionTrial);
    goto_if_error(r, "Error: During initialization of policy trial session",
                  error);

    TPM2B_NAME name1 = {
        .size = 32,
        .name = { 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,11, 12, 13, 14, 15, 16, 17,
                  18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32}

    };

    TPM2B_NAME name2 = {
        .size = 32,
        .name = { 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56,
                  57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72 }
    };

    r = Esys_PolicyDuplicationSelect(esys_context,
                                     sessionTrial,
                                     ESYS_TR_NONE,
                                     ESYS_TR_NONE,
                                     ESYS_TR_NONE, &name1, &name2, 0);
    goto_if_error(r, "Error: PolicyDuplicationSelect", error);

    TPM2B_DIGEST expectedPolicyDuplicationSelect = {
        .size = 32,
        .buffer = { 0x2b, 0xfb, 0xc1, 0x37, 0x3e, 0xa9, 0x86, 0xc6, 0xb7, 0x90, 0x7d,
                    0x0d, 0xcd, 0x8c, 0xad, 0x71, 0x6b, 0x73, 0x4f, 0xd6, 0xbb, 0x86,
                    0xe2, 0x27, 0xe2, 0x81, 0x11, 0x14, 0x8a, 0x92, 0x1, 0x6e }
    };

    if (!cmp_policy_digest
        (esys_context, &sessionTrial, &expectedPolicyDuplicationSelect,
         "PolicyDuplicationSelect", FLUSH))
        goto error;

    goto_if_error(r, "Error: FlushContext", error);

    /*
     * Test PolicyNvWritten
     */
    r = Esys_StartAuthSession(esys_context, ESYS_TR_NONE, ESYS_TR_NONE,
                              ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE,
                              &nonceCallerTrial,
                              TPM2_SE_TRIAL, &symmetricTrial, TPM2_ALG_SHA256,
                              &sessionTrial);
    goto_if_error(r, "Error: During initialization of policy trial session",
                  error);

    r = Esys_PolicyNvWritten(esys_context,
                             sessionTrial,
                             ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE, 0);
    goto_if_error(r, "Error: PolicyNvWritten", error);

    TPM2B_DIGEST expectedPolicyNvWritten = {
        .size = 32,
        .buffer = { 0x3c, 0x32, 0x63, 0x23, 0x67, 0x0e, 0x28, 0xad, 0x37, 0xbd, 0x57,
                    0xf6, 0x3b, 0x4c, 0xc3, 0x4d, 0x26, 0xab, 0x20, 0x5e, 0xf2, 0x2f,
                    0x27, 0x5c, 0x58, 0xd4, 0x7f, 0xab, 0x24, 0x85, 0x46, 0x6e }
    };

    if (!cmp_policy_digest(esys_context, &sessionTrial, &expectedPolicyNvWritten,
                           "NvWritten", FLUSH))
        goto error;

    /*
     * Space not needed for further tests.
     */

    r = Esys_NV_UndefineSpace(esys_context,
                              ESYS_TR_RH_OWNER,
                              nvHandle,
                              ESYS_TR_PASSWORD,
                              ESYS_TR_NONE,
                              ESYS_TR_NONE
                              );
    goto_if_error(r, "Error: NV_UndefineSpace", error);
    nvHandle = ESYS_TR_NONE;

    /*
     * Test PolicySetPrimaryPolicy
     */

    TPM2B_DIGEST authPolicy = {
        .size = 32,
        .buffer = { 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,11, 12, 13, 14, 15, 16, 17,
                    18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32}

    };

    r = Esys_SetPrimaryPolicy(esys_context,
                              ESYS_TR_RH_OWNER,
                              ESYS_TR_PASSWORD,
                              ESYS_TR_NONE, ESYS_TR_NONE,
                              &authPolicy,
                              TPM2_ALG_SHA256);

    if ((r == TPM2_RC_COMMAND_CODE) ||
        (r == (TPM2_RC_COMMAND_CODE | TSS2_RESMGR_RC_LAYER)) ||
        (r == (TPM2_RC_COMMAND_CODE | TSS2_RESMGR_TPM_RC_LAYER))) {
        LOG_WARNING("Command TPM2_SetPrimaryPolicy  not supported by TPM.");
    } else {
        goto_if_error(r, "Error: SetPrimaryPolicy", error);
    }

    return EXIT_SUCCESS;

 error:

    if (sessionTrial != ESYS_TR_NONE) {
        if (Esys_FlushContext(esys_context, sessionTrial) != TSS2_RC_SUCCESS) {
            LOG_ERROR("Cleanup sessionTrial failed.");
        }
    }

    if (sessionTrialPCR != ESYS_TR_NONE) {
        if (Esys_FlushContext(esys_context, sessionTrialPCR) != TSS2_RC_SUCCESS) {
            LOG_ERROR("Cleanup sessionTrialPCR failed.");
        }
    }

    if (nvHandle != ESYS_TR_NONE) {
        if (Esys_NV_UndefineSpace(esys_context,
                                  ESYS_TR_RH_OWNER,
                                  nvHandle,
                                  ESYS_TR_PASSWORD,
                                  ESYS_TR_NONE,
                                  ESYS_TR_NONE) != TSS2_RC_SUCCESS) {
             LOG_ERROR("Cleanup nvHandle failed.");
        }
    }

    return failure_return;
}

int
test_invoke_esys(ESYS_CONTEXT * esys_context) {
    return test_esys_policy_regression(esys_context);
}
