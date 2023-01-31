/* SPDX-License-Identifier: BSD-2-Clause */
/*******************************************************************************
 * Copyright 2017-2018, Fraunhofer SIT sponsored by Infineon Technologies AG
 * All rights reserved.
 *******************************************************************************/

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <stdlib.h>

#include "tss2_esys.h"
#include "tss2_fapi.h"

#include "test-fapi.h"
#include "fapi_util.h"

#define LOGMODULE test
#include "util/log.h"
#include "util/aux_util.h"

#define MIN_PLATFORM_CERT_HANDLE 0x01C08000
#define CERTIFICATE_SIZE 15

/** Test the FAPI functions for platform certificates.
 *
 * Tested FAPI commands:
 *  - Fapi_Provision()
 *  - Fapi_GetPlatformCertificates()
 *  - Fapi_Delete()
 *
 * @param[in,out] context The FAPI_CONTEXT.
 * @retval EXIT_FAILURE
 * @retval EXIT_SUCCESS
 */
int
test_fapi_platform_certificates(FAPI_CONTEXT *context)
{
    TSS2_RC r;
    ESYS_TR nvHandle = ESYS_TR_NONE;
    uint8_t *certs = NULL;
    size_t certsSize = 0;
    /* In case NV was already defined, do not delete it in clean up */
    bool nv_already_defined = false;
    bool nv_newly_defined = false;
    size_t nv_size = CERTIFICATE_SIZE;

    r = Fapi_Provision(context, NULL, NULL, NULL);
    goto_if_error(r, "Error Fapi_Provision", error);

    TPM2_CAP capability = TPM2_CAP_HANDLES;
    INT32 property = 0x1000000;

    UINT32 propertyCount = 254;
    TPMI_YES_NO moreDataAvailable;
    TPMS_CAPABILITY_DATA *capabilityData;

    capabilityData = NULL;
    r = Esys_GetCapability(context->esys,
        ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE,
        capability, property,
        propertyCount,
        &moreDataAvailable,
        &capabilityData);
    goto_if_error(r, "Error Esys_GetCapability", error);

    int count = capabilityData->data.handles.count;
    for(int i = 0; i < count; i++){
        if(capabilityData->data.handles.handle[i] == MIN_PLATFORM_CERT_HANDLE){
            nv_already_defined = true;
            break;
        }
    }
    SAFE_FREE(capabilityData);

    if(nv_already_defined){
        TPM2B_NV_PUBLIC *nvPublic = NULL;
        TPM2B_NAME *nvName = NULL;

        r = Esys_TR_FromTPMPublic(context->esys,
                                  MIN_PLATFORM_CERT_HANDLE,
                                  ESYS_TR_NONE,
                                  ESYS_TR_NONE,
                                  ESYS_TR_NONE,
                                  &nvHandle);
        goto_if_error(r, "Error: TR from TPM public", error);

        r = Esys_NV_ReadPublic(context->esys,
                               nvHandle,
                               ESYS_TR_NONE,
                               ESYS_TR_NONE,
                               ESYS_TR_NONE,
                               &nvPublic,
                               &nvName);
        goto_if_error(r, "Error: nv read public", error);

        LOG_INFO("nvPublic Size %d\n", nvPublic->nvPublic.dataSize);

        nv_size = nvPublic->nvPublic.dataSize;
        LOG_INFO("NV size: %zu", nv_size);
    }

    if(!nv_already_defined){

        TPM2B_AUTH auth = { 0 };

        TPM2B_NV_PUBLIC publicInfo = {
            .nvPublic = {
                .nameAlg = TPM2_ALG_SHA256,
                .attributes = TPMA_NV_PPWRITE | TPMA_NV_AUTHREAD |
                    TPMA_NV_OWNERREAD | TPMA_NV_PLATFORMCREATE | TPMA_NV_NO_DA,
                .dataSize = CERTIFICATE_SIZE,
                .nvIndex = MIN_PLATFORM_CERT_HANDLE,
            },
        };

        r = Esys_NV_DefineSpace(context->esys,
                                ESYS_TR_RH_PLATFORM,
                                ESYS_TR_PASSWORD,
                                ESYS_TR_NONE,
                                ESYS_TR_NONE,
                                &auth,
                                &publicInfo,
                                &nvHandle);

        if (number_rc(r) == TPM2_RC_BAD_AUTH ||
            number_rc(r) == TPM2_RC_HIERARCHY) {
            /* Platform authorization not possible test will be skipped */
            LOG_WARNING("Platform authorization not possible.");
            goto skip;
        }

        goto_if_error(r, "Error Esys_NV_DefineSpace", error);

        nv_newly_defined = true;

        TPM2B_MAX_NV_BUFFER nv_test_data = { .size = CERTIFICATE_SIZE,
                                             .buffer={0x61, 0x61, 0x61, 0x61, 0x61,
                                                0x61, 0x61, 0x61, 0x61, 0x61, 0x61,
                                                0x61, 0x61, 0x61, 0x61}};

        r = Esys_NV_Write(context->esys,
                      ESYS_TR_RH_PLATFORM,
                      nvHandle,
                      ESYS_TR_PASSWORD,
                      ESYS_TR_NONE,
                      ESYS_TR_NONE,
                      &nv_test_data,
                      0);
        goto_if_error(r, "Error Esys_NV_Write", error);
    }

    r = Fapi_GetPlatformCertificates(context, &certs, &certsSize);
    if (r == TSS2_FAPI_RC_NO_CERT)
        goto skip;
    goto_if_error(r, "Error Fapi_GetPlatformCertificates", error);
    ASSERT(certs != NULL);
    ASSERT(certsSize == nv_size);

    Fapi_Free(certs);

    if(nv_newly_defined){
        r = Esys_NV_UndefineSpace(context->esys,
                              ESYS_TR_RH_PLATFORM,
                              nvHandle,
                              ESYS_TR_PASSWORD,
                              ESYS_TR_NONE,
                              ESYS_TR_NONE
                              );
        goto_if_error(r, "Error: NV_UndefineSpace", error);
    }

    /* Cleanup */
    r = Fapi_Delete(context, "/");
    goto_if_error(r, "Error Fapi_Delete", error);

    return EXIT_SUCCESS;

error:
    if(nv_newly_defined){
        Esys_NV_UndefineSpace(context->esys,
            ESYS_TR_RH_PLATFORM, nvHandle,
            ESYS_TR_PASSWORD, ESYS_TR_NONE,
            ESYS_TR_NONE);
    }
    Fapi_Delete(context, "/");
    return EXIT_FAILURE;

 skip:
    if(nv_newly_defined){
        Esys_NV_UndefineSpace(context->esys,
            ESYS_TR_RH_PLATFORM, nvHandle,
            ESYS_TR_PASSWORD, ESYS_TR_NONE,
            ESYS_TR_NONE);
    }
    Fapi_Delete(context, "/");
    return EXIT_SKIP;
}

int
test_invoke_fapi(FAPI_CONTEXT *fapi_context)
{
    return test_fapi_platform_certificates(fapi_context);
}
