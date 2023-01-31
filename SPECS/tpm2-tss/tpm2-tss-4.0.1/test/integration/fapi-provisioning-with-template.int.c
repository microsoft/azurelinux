/* SPDX-License-Identifier: BSD-2-Clause */
#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <stdlib.h>

#include "tss2_esys.h"
#include "tss2_fapi.h"
#include "tss2_mu.h"

#include "test-fapi.h"
#include "esys_iutil.h"
#define LOGMODULE test
#define LOGDEFAULT LOGLEVEL_INFO
#include "util/log.h"
#include "util/aux_util.h"

/** This test is intended to test Fapi_Provision with a template and a nonce
 *  stored in NV ram.
 *
 * The default template for RSA2048 or ECC_NIST_P256 will be stored in NV ram.
 * The provisioning should work with this template.
 * Afterwards a nonce which will be used for EK generation is stored in NV ram.
 * With this nonce an EK which is not appropriate to the certificate will be
 * generated. The provisioning should fail.
 *
 * @param[in,out] esys_context The ESYS_CONTEXT.
 * @retval EXIT_FAILURE
 * @retval EXIT_SUCCESS
 * @retval EXIT_SKIP
 *
 */
int
test_fapi_provision_template(FAPI_CONTEXT *context)
{
    size_t offset = 0;
    UINT16 offset_nv = 0;
     TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *esys_ctx;
    ESYS_TR nv_handle_template = ESYS_TR_NONE;
    ESYS_TR nv_handle_nonce = ESYS_TR_NONE;
    TPM2_HANDLE nv_template_idx;
    TPM2_RC r;
    TPM2_HANDLE nv_nonce_idx;
    TPM2_HANDLE ecc_nv_nonce_idx = 0x01c0000b;
    TPM2_HANDLE ecc_nv_template_idx = 0x01c0000c;
    TPMT_PUBLIC in_public;
    TPMT_PUBLIC ecc_in_public =
        {
         .type = TPM2_ALG_ECC,
         .nameAlg = TPM2_ALG_SHA256,
         .objectAttributes = (TPMA_OBJECT_RESTRICTED |
                              TPMA_OBJECT_DECRYPT |
                              TPMA_OBJECT_FIXEDTPM |
                              TPMA_OBJECT_FIXEDPARENT |
                              TPMA_OBJECT_ADMINWITHPOLICY |
                              TPMA_OBJECT_SENSITIVEDATAORIGIN),
         .authPolicy =
         {
          .size = 32,
          .buffer = { 0x83, 0x71, 0x97, 0x67, 0x44, 0x84, 0xb3, 0xf8, 0x1a, 0x90,
                      0xcc, 0x8d, 0x46, 0xa5, 0xd7, 0x24, 0xfd, 0x52, 0xd7, 0x6e,
                      0x06, 0x52, 0x0b, 0x64, 0xf2, 0xa1, 0xda, 0x1b, 0x33, 0x14,
                      0x69, 0xaa }
         },
         .parameters.eccDetail =
         {
          .symmetric = {
                        .algorithm = TPM2_ALG_AES,
                        .keyBits.aes = 128,
                        .mode.aes = TPM2_ALG_CFB,
                        },
          .scheme = { .scheme = TPM2_ALG_NULL,
                      .details = {}
                     },
          .curveID = TPM2_ECC_NIST_P256,
          .kdf = { .scheme = TPM2_ALG_NULL,
                   .details = {}
                  }
         },
         .unique.ecc = {
                        .x = {.size = 32, .buffer = {}},
                        .y = {.size = 32, .buffer = {}}
                        }
        };
    TPM2_HANDLE rsa_nv_nonce_idx = 0x01c00003;
    TPM2_HANDLE rsa_nv_template_idx = 0x01c00004;
    TPMT_PUBLIC rsa_in_public =
        {
         .type = TPM2_ALG_RSA,
         .nameAlg = TPM2_ALG_SHA256,
         .objectAttributes = (TPMA_OBJECT_RESTRICTED |
                              TPMA_OBJECT_DECRYPT |
                              TPMA_OBJECT_FIXEDTPM |
                              TPMA_OBJECT_FIXEDPARENT |
                              TPMA_OBJECT_ADMINWITHPOLICY |
                              TPMA_OBJECT_SENSITIVEDATAORIGIN),
         .authPolicy =
         {
          .size = 32,
          .buffer = { 0x83, 0x71, 0x97, 0x67, 0x44, 0x84, 0xb3, 0xf8, 0x1a, 0x90,
                      0xcc, 0x8d, 0x46, 0xa5, 0xd7, 0x24, 0xfd, 0x52, 0xd7, 0x6e,
                      0x06, 0x52, 0x0b, 0x64, 0xf2, 0xa1, 0xda, 0x1b, 0x33, 0x14,
                      0x69, 0xaa }
         },
         .parameters.rsaDetail =
         {
          .symmetric = {
                        .algorithm = TPM2_ALG_AES,
                        .keyBits.aes = 128,
                        .mode.aes = TPM2_ALG_CFB,
                        },
          .scheme = {
                     .scheme = TPM2_ALG_NULL,
                     .details = {}
                     },
          .keyBits = 2048,
          .exponent = 0,
         },
         .unique.rsa = {
                        .size = 256,
                        .buffer = {}
                        }
        };

    TPM2B_NV_PUBLIC nv_public_info = {
        .size = 0,
        .nvPublic = {
            .nvIndex = 0,
            .nameAlg = TPM2_ALG_SHA256,
            .attributes = (
                TPMA_NV_OWNERWRITE |
                TPMA_NV_AUTHWRITE |
                TPMA_NV_WRITE_STCLEAR |
                TPMA_NV_READ_STCLEAR |
                TPMA_NV_AUTHREAD |
                TPMA_NV_OWNERREAD
                ),
            .authPolicy = {
                 .size = 0,
                 .buffer = {},
             },
            .dataSize = 0,
        }
    };

    TPM2B_AUTH auth = { .size = 0, .buffer = {} };
    TPM2B_MAX_NV_BUFFER nv_data;

    if (strcmp(FAPI_PROFILE, "P_ECC") == 0) {
        nv_template_idx = ecc_nv_template_idx;
        nv_nonce_idx = ecc_nv_nonce_idx;
        in_public = ecc_in_public;
    } else if (strcmp(FAPI_PROFILE, "P_RSA") == 0) {
        nv_template_idx = rsa_nv_template_idx;
        nv_nonce_idx = rsa_nv_nonce_idx;
        in_public = rsa_in_public;
     } else {
        return EXIT_SKIP;
    }

    r = Fapi_GetTcti(context, &tcti);
    goto_if_error(r, "Error Fapi_GetTcti", error);

    r = Esys_Initialize(&esys_ctx, tcti, NULL);
    goto_if_error(r, "Error Esys_Initialize", error);

     /*
     * Store template (marshaled TPMT_PUBLIC) in NV ram.
     */
    r = Tss2_MU_TPMT_PUBLIC_Marshal(&in_public, &nv_data.buffer[0],
                                    sizeof(in_public), &offset);
    goto_if_error(r, "Tss2_MU_TPMT_PUBLIC_Marshal", error);

    nv_public_info.nvPublic.nvIndex = nv_template_idx;
    nv_public_info.nvPublic.dataSize = offset;
    nv_data.size = offset;

    r = Esys_NV_DefineSpace(esys_ctx,
                            ESYS_TR_RH_OWNER,
                            ESYS_TR_PASSWORD,
                            ESYS_TR_NONE,
                            ESYS_TR_NONE,
                            &auth,
                            &nv_public_info,
                            &nv_handle_template);
    goto_if_error(r, "Error esys define nv space", error);

    r = Esys_NV_Write(esys_ctx,
                      nv_handle_template,
                      nv_handle_template,
                      ESYS_TR_PASSWORD,
                      ESYS_TR_NONE,
                      ESYS_TR_NONE,
                      &nv_data,
                      offset_nv);
    goto_if_error(r, "Error esys nv write successful", error);

    r = Fapi_Provision(context, NULL, NULL, NULL);
    goto_if_error(r, "Error Fapi_Provision", error);

    r = Esys_NV_UndefineSpace(esys_ctx,
                              ESYS_TR_RH_OWNER,
                              nv_handle_template,
                              ESYS_TR_PASSWORD,
                              ESYS_TR_NONE, ESYS_TR_NONE);
    goto_if_error(r, "Error Esys_NV_UndefineSpace", error);
    nv_handle_template = ESYS_TR_NONE;

    r = Fapi_Delete(context, "/");
    goto_if_error(r, "Error Fapi_Delete", error);

    /*
     * Store nonce in NV ram to check whether provisioning fails because the
     * appropriate certificate was not found.
     */
    nv_public_info.nvPublic.nvIndex = nv_nonce_idx;
    nv_public_info.nvPublic.dataSize = 1;
    nv_data.size = 1;
    nv_data.buffer[0] = 1;

    r = Esys_NV_DefineSpace(esys_ctx,
                            ESYS_TR_RH_OWNER,
                            ESYS_TR_PASSWORD,
                            ESYS_TR_NONE,
                            ESYS_TR_NONE,
                            &auth,
                            &nv_public_info,
                            &nv_handle_nonce);
    goto_if_error(r, "Error esys define nv space", error);

    r = Esys_NV_Write(esys_ctx,
                      nv_handle_nonce,
                      nv_handle_nonce,
                      ESYS_TR_PASSWORD,
                      ESYS_TR_NONE,
                      ESYS_TR_NONE,
                      &nv_data,
                      offset_nv);
    goto_if_error(r, "Error esys nv write successful", error);

    r = Fapi_Provision(context, NULL, NULL, NULL);
    if (r != TSS2_FAPI_RC_NO_CERT) {
        LOG_ERROR("Provisioning with nonce did not fail.");
        goto error;
    }

    r = Esys_NV_UndefineSpace(esys_ctx,
                              ESYS_TR_RH_OWNER,
                              nv_handle_nonce,
                              ESYS_TR_PASSWORD,
                              ESYS_TR_NONE, ESYS_TR_NONE);
    goto_if_error(r, "Error Esys_NV_UndefineSpace", error);
    nv_handle_nonce = ESYS_TR_NONE;
    Esys_Finalize(&esys_ctx);

    return EXIT_SUCCESS;

 error:
    if (nv_handle_template != ESYS_TR_NONE) {
        if (Esys_NV_UndefineSpace(esys_ctx,
                                  ESYS_TR_RH_OWNER,
                                  nv_handle_template,
                                  ESYS_TR_PASSWORD,
                                  ESYS_TR_NONE,
                                  ESYS_TR_NONE) != TSS2_RC_SUCCESS) {
            LOG_ERROR("Cleanup nv_handle_template failed.");
        }
    }
     if (nv_handle_nonce != ESYS_TR_NONE) {
        if (Esys_NV_UndefineSpace(esys_ctx,
                                  ESYS_TR_RH_OWNER,
                                  nv_handle_nonce,
                                  ESYS_TR_PASSWORD,
                                  ESYS_TR_NONE,
                                  ESYS_TR_NONE) != TSS2_RC_SUCCESS) {
            LOG_ERROR("Cleanup nv_handle_nonce failed.");
        }
    }
     Esys_Finalize(&esys_ctx);
    return EXIT_FAILURE;
}
int
test_invoke_fapi(FAPI_CONTEXT *fapi_context)
{
    return test_fapi_provision_template(fapi_context);
}
