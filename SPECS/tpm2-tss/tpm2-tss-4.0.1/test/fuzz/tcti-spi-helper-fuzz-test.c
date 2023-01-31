/* SPDX-License-Identifier: BSD-2-Clause */

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <stdbool.h>
#include <stdlib.h>

#define LOGMODULE test
#include "tss2_sys.h"
#include "tss2_tcti.h"
#include "tss2/tss2_tcti_spi_helper.h"
#include "util/log.h"
#include "test.h"
#include "test-options.h"
#include "context-util.h"
#include "tss2-sys/sysapi_util.h"
#include "tcti/tcti-fuzzing.h"

typedef struct fuzz_user_data fuzz_user_data;
struct fuzz_user_data {
    size_t len;
    const uint8_t *fuzz_data;
};

typedef enum {
    TPM_DID_VID_HEAD = 0,
    TPM_DID_VID_BODY,
    TPM_ACCESS_HEAD,
    TPM_ACCESS_BODY,
    TPM_STS_HEAD,
    TPM_STS_BODY,
    TPM_RID_HEAD,
    TPM_RID_BODY
} tpm_state_t;

static const unsigned char TPM_DID_VID_0[] = {0x83, 0xd4, 0x0f, 0x00, 0xd1, 0x15, 0x1b, 0x00};
static const unsigned char TPM_ACCESS_0[] = {0x80, 0xd4, 0x00, 0x00, 0xa1};
static const unsigned char TPM_STS_0[] = {0x83, 0xd4, 0x00, 0x18, 0x40, 0x00, 0x00, 0x00};
static const unsigned char TPM_RID_0[] = {0x80, 0xd4, 0x0f, 0x04, 0x00};

static bool is_init = true;

TSS2_RC platform_sleep_ms (void* user_data, int32_t milliseconds)
{
    UNUSED(user_data);
    UNUSED(milliseconds);
    return TSS2_RC_SUCCESS;
}

TSS2_RC platform_start_timeout (void* user_data, int32_t milliseconds)
{
    UNUSED(user_data);
    UNUSED(milliseconds);
    return TSS2_RC_SUCCESS;
}

TSS2_RC platform_timeout_expired (void* user_data, bool *is_timeout_expired)
{
    UNUSED(user_data);
    *is_timeout_expired = true;
    return TSS2_RC_SUCCESS;
}

TSS2_RC platform_spi_acquire (void* user_data)
{
    UNUSED(user_data);
    return TSS2_RC_SUCCESS;
}

TSS2_RC platform_spi_release (void* user_data)
{
    UNUSED(user_data);
    return TSS2_RC_SUCCESS;
}

TSS2_RC platform_spi_transfer_with_wait_state (void* user_data, const void *data_out, void *data_in, size_t cnt)
{
    UNUSED(user_data);
    UNUSED(data_out);
    UNUSED(cnt);

    static tpm_state_t tpm_state = TPM_DID_VID_HEAD;

    switch (tpm_state++) {
    case TPM_DID_VID_HEAD:
        memcpy (data_in, TPM_DID_VID_0, 4);
        ((unsigned char *)data_in)[3] |= 0x01;
        break;
    case TPM_DID_VID_BODY:
        memcpy (data_in, TPM_DID_VID_0 + 4, sizeof (TPM_DID_VID_0) - 4);
        break;
    case TPM_ACCESS_HEAD:
        memcpy (data_in, TPM_ACCESS_0, 4);
        ((unsigned char *)data_in)[3] |= 0x01;
        break;
    case TPM_ACCESS_BODY:
        memcpy (data_in, TPM_ACCESS_0 + 4, sizeof (TPM_ACCESS_0) - 4);
        break;
    case TPM_STS_HEAD:
        memcpy (data_in, TPM_STS_0, 4);
        ((unsigned char *)data_in)[3] |= 0x01;
        break;
    case TPM_STS_BODY:
        memcpy (data_in, TPM_STS_0 + 4, sizeof (TPM_STS_0) - 4);
        break;
    case TPM_RID_HEAD:
        memcpy (data_in, TPM_RID_0, 4);
        ((unsigned char *)data_in)[3] |= 0x01;
        break;
    case TPM_RID_BODY:
        memcpy (data_in, TPM_RID_0 + 4, 1);
        break;
    default:
        return TSS2_TCTI_RC_IO_ERROR;
    }

    return TSS2_RC_SUCCESS;
}

TSS2_RC platform_spi_transfer_fuzz (void* user_data, const void *data_out, void *data_in, size_t cnt)
{
    UNUSED(data_out);

    fuzz_user_data *udata = (fuzz_user_data *)user_data;
    /* libfuzzer input might only be 2 bytes, but cnt might be 32 */
    size_t min = cnt > udata->len ? cnt : udata->len;
    memcpy(data_in, udata->fuzz_data, min);

    return TSS2_RC_SUCCESS;
}

TSS2_RC platform_spi_transfer (void* user_data, const void *data_out, void *data_in, size_t cnt)
{

    /*
     * Use if we're past init to start fuzzing
     */
    return is_init ?
            platform_spi_transfer_with_wait_state(user_data, data_out, data_in, cnt) :
            platform_spi_transfer_fuzz(user_data, data_out, data_in, cnt);
}


void platform_finalize(void* user_data)
{
    UNUSED(user_data);
}

int
LLVMFuzzerTestOneInput (
        const uint8_t *fuzz_data,
        size_t size)
{
    if (!fuzz_data) {
        return -1;
    }

    TSS2_TCTI_CONTEXT *tcti_ctx = NULL;
    TSS2_SYS_CONTEXT *sapi_ctx = NULL;

    fuzz_user_data udata = {
        .len = size,
        .fuzz_data = fuzz_data
    };

    TSS2_TCTI_SPI_HELPER_PLATFORM conf = {
        .user_data = &udata,
        .sleep_ms = platform_sleep_ms,
        .start_timeout = platform_start_timeout,
        .timeout_expired = platform_timeout_expired,
        .spi_acquire = platform_spi_acquire,
        .spi_release = platform_spi_release,
        .spi_transfer = platform_spi_transfer,
        .finalize = platform_finalize
    };

    size_t tcti_size = 0;
    TSS2_RC rc = Tss2_Tcti_Spi_Helper_Init (
            NULL, &tcti_size, &conf);
    if (rc != TSS2_RC_SUCCESS) {
        LOG_ERROR("Tss2_Tcti_Spi_Helper_Init failed 0x%x", rc);
        return EXIT_FAILURE;
    }

    tcti_ctx = (TSS2_TCTI_CONTEXT *)calloc(1, tcti_size);
    if (!tcti_ctx) {
        LOG_ERROR("OOM allocating TCTI");
        goto error;
    }

    rc = Tss2_Tcti_Spi_Helper_Init (
            tcti_ctx, &tcti_size, &conf);
    if (rc != TSS2_RC_SUCCESS) {
        LOG_ERROR("Tss2_Tcti_Spi_Helper_Init failed 0x%x", rc);
        goto error;
    }

    is_init = false;

    size_t sapi_size = Tss2_Sys_GetContextSize(0);

    sapi_ctx = (TSS2_SYS_CONTEXT *)calloc(1, sapi_size);
    if (!sapi_ctx) {
        LOG_ERROR("OOM allocating SAPI");
        goto error;
    }

    rc = Tss2_Sys_Initialize(sapi_ctx, sapi_size, tcti_ctx, NULL);
    if (rc != TSS2_RC_SUCCESS) {
        LOG_ERROR("Tss2_Sys_Initialize failed 0x%x", rc);
        goto error;
    }

    /*
     * ignore the RC (we expect jibberish from the TCTI)
     * but this should get the TCTI firing through transfer.
     */
    TPM2B_DIGEST buf = { 0 };
    UNUSED(Tss2_Sys_GetRandom(sapi_ctx, NULL, 4, &buf, NULL));

error:
    Tss2_Sys_Finalize(sapi_ctx);
    free(sapi_ctx);

    Tss2_Tcti_Finalize(tcti_ctx);
    free(tcti_ctx);

    return 0;
}
