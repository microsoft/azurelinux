/* SPDX-License-Identifier: BSD-2-Clause */
/*******************************************************************************
 * Copyright (c) 2020, Intel Corporation
 * Copyright 2020, Fraunhofer SIT sponsored by Infineon Technologies AG
 * All rights reserved.
 *******************************************************************************/

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <stdlib.h>

#include "tss2_esys.h"

#include "esys_iutil.h"
#include "test-esys.h"
#define LOGMODULE test
#include "util/log.h"
#include "util/aux_util.h"

/** This test is intended to test the command Esys_CertifyX509.
 *
 * We create a RSA primary signing key which will be used as signing key
 * and as object for the certify command.
 *
 * Tested ESYS commands:
 *  - Esys_CertifyX509() (M)
 *  - Esys_CreatePrimary() (M)
 *  - Esys_FlushContext() (M)
 *
 * @param[in,out] esys_contextx509 The ESYS_CONTEXT.
 * @retval EXIT_FAILURE
 * @retval EXIT_SKIP
 * @retval EXIT_SUCCESS
 */

int
test_esys_certifyx509(ESYS_CONTEXT * esys_context)
{
    TSS2_RC r;
    ESYS_TR signHandle = ESYS_TR_NONE;
    TPM2B_PUBLIC *outPublic = NULL;
    TPM2B_CREATION_DATA *creationData = NULL;
    TPM2B_DIGEST *creationHash = NULL;
    TPMT_TK_CREATION *creationTicket = NULL;
    TPMT_SIGNATURE *signature = NULL;
    TPM2B_MAX_BUFFER *addedToCertificate = NULL;
    TPM2B_DIGEST *tbsDigest = NULL;
    TPM2B_DATA reserved = {0};
    TPM2B_AUTH authValuePrimary = {
        .size = 5,
        .buffer = {1, 2, 3, 4, 5}
    };

    TPM2B_SENSITIVE_CREATE inSensitivePrimary = {
        .size = 0,
        .sensitive = {
            .userAuth = {
                 .size = 0,
                 .buffer = {0},
             },
            .data = {
                 .size = 0,
                 .buffer = {0},
             },
        },
    };

    inSensitivePrimary.sensitive.userAuth = authValuePrimary;

    TPM2B_PUBLIC inPublic = {
        .size = 0,
        .publicArea = {
            .type = TPM2_ALG_RSA,
            .nameAlg = TPM2_ALG_SHA256,
            .objectAttributes = (
                    TPMA_OBJECT_FIXEDTPM |
                    TPMA_OBJECT_USERWITHAUTH |
                    TPMA_OBJECT_RESTRICTED |
                    TPMA_OBJECT_SIGN_ENCRYPT |
#if defined INTEGRATION_TCTI_MSSIM
                    TPMA_OBJECT_X509SIGN | /* This requires mssim >= v1628 Other simulators
                                              that do not implement 1.59 spec return 0x000002e1
                                              tpm:parameter(2):reserved bits not set to zero as required
                                            */
#endif
                    TPMA_OBJECT_FIXEDTPM |
                    TPMA_OBJECT_FIXEDPARENT |
                    TPMA_OBJECT_SENSITIVEDATAORIGIN),
            .authPolicy = {
                    .size = 0,
                    .buffer = {0},
            },
            .parameters.rsaDetail = {
                .symmetric = {
                    .algorithm = TPM2_ALG_NULL,
                    .keyBits.aes = 0,
                    .mode.aes = TPM2_ALG_NULL,
                },
                .scheme = {
                     .scheme = TPM2_ALG_RSASSA,
                     .details = { .rsassa = { .hashAlg = TPM2_ALG_SHA256 }},
                },
                .keyBits = 2048,
                .exponent = 0,
            },
            .unique.rsa = {
                .size = 0,
                .buffer = {0},
            },
        },
    };

    TPM2B_AUTH authValue = {
        .size = 0,
        .buffer = {0}
    };

    TPM2B_DATA outsideInfo = {
        .size = 0,
        .buffer = {0},
    };

    TPML_PCR_SELECTION creationPCR = {
        .count = 0,
    };

    TPMT_SIG_SCHEME inScheme = {
        .scheme = TPM2_ALG_RSASSA,
        .details.rsassa = TPM2_ALG_SHA256
    };

    LOG_INFO("\nRSA key will be created.");
    r = Esys_TR_SetAuth(esys_context, ESYS_TR_RH_OWNER, &authValue);
    goto_if_error(r, "Error: TR_SetAuth", error);

    r = Esys_CreatePrimary(esys_context, ESYS_TR_RH_OWNER, ESYS_TR_PASSWORD,
                           ESYS_TR_NONE, ESYS_TR_NONE, &inSensitivePrimary,
                           &inPublic, &outsideInfo, &creationPCR,
                           &signHandle, &outPublic, &creationData,
                           &creationHash, &creationTicket);
    goto_if_error(r, "Error esys create primary", error);

    /* For the partial cert we need these fields:
     * 1) Signature Algorithm Identifier (optional)
       2) Issuer (mandatory)
       3) Validity (mandatory)
       4) Subject Name (mandatory)
       5) Extensions (mandatory only KeyUsage, can take tcg-tpmaObject, but it's optional)
       Cert data generated with tpm2-certifyX509_gen_partial_cert util from the tpm2-tools project.
    */
    TPM2B_MAX_BUFFER partialCertificate = {
        .size = 199,
        .buffer = { 0x30, 0x81, 0xc4, 0x30, 0x4d, 0x31, 0x0b, 0x30, 0x09, 0x06, 0x03, 0x55, 0x04, 0x06, 0x13, 0x02,
                    0x55, 0x53, 0x31, 0x11, 0x30, 0x0f, 0x06, 0x03, 0x55, 0x04, 0x0a, 0x0c, 0x08, 0x54, 0x53, 0x53,
                    0x20, 0x54, 0x45, 0x53, 0x54, 0x31, 0x10, 0x30, 0x0e, 0x06, 0x03, 0x55, 0x04, 0x0b, 0x0c, 0x07,
                    0x52, 0x6f, 0x6f, 0x74, 0x20, 0x43, 0x41, 0x31, 0x19, 0x30, 0x17, 0x06, 0x03, 0x55, 0x04, 0x03,
                    0x0c, 0x10, 0x54, 0x53, 0x53, 0x20, 0x54, 0x45, 0x53, 0x54, 0x20, 0x52, 0x6f, 0x6f, 0x74, 0x20,
                    0x43, 0x41, 0x30, 0x1e, 0x17, 0x0d, 0x32, 0x30, 0x30, 0x37, 0x32, 0x38, 0x32, 0x31, 0x30, 0x33,
                    0x32, 0x32, 0x5a, 0x17, 0x0d, 0x33, 0x30, 0x30, 0x34, 0x32, 0x37, 0x32, 0x31, 0x30, 0x33, 0x32,
                    0x32, 0x5a, 0x30, 0x38, 0x31, 0x0b, 0x30, 0x09, 0x06, 0x03, 0x55, 0x04, 0x06, 0x13, 0x02, 0x55,
                    0x53, 0x31, 0x11, 0x30, 0x0f, 0x06, 0x03, 0x55, 0x04, 0x0a, 0x0c, 0x08, 0x54, 0x53, 0x53, 0x20,
                    0x54, 0x45, 0x53, 0x54, 0x31, 0x16, 0x30, 0x14, 0x06, 0x03, 0x55, 0x04, 0x03, 0x0c, 0x0d, 0x54,
                    0x53, 0x53, 0x20, 0x54, 0x45, 0x53, 0x54, 0x20, 0x68, 0x6f, 0x73, 0x74, 0x30, 0x05, 0x30, 0x00,
                    0x03, 0x01, 0x00, 0xa3, 0x12, 0x30, 0x10, 0x30, 0x0e, 0x06, 0x03, 0x55, 0x1d, 0x0f, 0x01, 0x01,
                    0xff, 0x04, 0x04, 0x03, 0x02, 0x01, 0x86 }
    };

    r = Esys_CertifyX509 (
        esys_context,
        signHandle,
        signHandle,
        ESYS_TR_PASSWORD,
        ESYS_TR_PASSWORD,
        ESYS_TR_NONE,
        &reserved,
        &inScheme,
        &partialCertificate,
        &addedToCertificate,
        &tbsDigest,
        &signature);
    goto_if_error(r, "Error: CertifyX509", error);

    r = Esys_FlushContext(esys_context,signHandle);
    goto_if_error(r, "Error: FlushContext", error);

    Esys_Free(outPublic);
    Esys_Free(creationData);
    Esys_Free(creationHash);
    Esys_Free(creationTicket);
    Esys_Free(signature);
    Esys_Free(addedToCertificate);
    Esys_Free(tbsDigest);
    return EXIT_SUCCESS;

 error:

    if (signHandle != ESYS_TR_NONE) {
        if (Esys_FlushContext(esys_context, signHandle) != TSS2_RC_SUCCESS) {
            LOG_ERROR("Cleanup signHandle failed.");
        }
    }
    if (outPublic)
        Esys_Free(outPublic);

    if (creationData)
        Esys_Free(creationData);

    if (creationHash)
        Esys_Free(creationHash);

    if (creationTicket)
        Esys_Free(creationTicket);

    if (signature)
        Esys_Free(signature);

    if (addedToCertificate)
        Esys_Free(addedToCertificate);

    if (tbsDigest)
        Esys_Free(tbsDigest);

    /* If the TPM doesn't support it return skip */
    if (r == TPM2_RC_COMMAND_CODE)
        return EXIT_SKIP;
    else
        return EXIT_FAILURE;
}

int
test_invoke_esys(ESYS_CONTEXT * esys_context) {
    return test_esys_certifyx509(esys_context);
}
