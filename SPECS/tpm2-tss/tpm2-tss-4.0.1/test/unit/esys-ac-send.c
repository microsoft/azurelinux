/* SPDX-License-Identifier: BSD-2-Clause */
/*******************************************************************************
 * Copyright 2017-2018, Fraunhofer SIT sponsored by Infineon Technologies AG All
 * rights reserved.
 ******************************************************************************/

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <stdarg.h>
#include <inttypes.h>
#include <string.h>
#include <stdlib.h>

#include <setjmp.h>
#include <cmocka.h>

#include "tss2_esys.h"
#include "tss2-tcti/tcti-common.h"

#define LOGMODULE tests
#include "util/log.h"

#define TCTI_FAKE_MAGIC 0x46414b4500000000ULL        /* 'FAKE\0' */
#define TCTI_FAKE_VERSION 0x1

const uint8_t yielded_response[] = {
    0x80, 0x01,                 /* TPM_ST_NO_SESSION */
    0x00, 0x00, 0x00, 0x0A,     /* Response Size 10 */
    0x00, 0x00, 0x00, 0x00      /* TPM_RC_YIELDED */
};

typedef struct {
    uint64_t magic;
    uint32_t version;
    TSS2_TCTI_TRANSMIT_FCN transmit;
    TSS2_TCTI_RECEIVE_FCN receive;
    TSS2_RC(*finalize) (TSS2_TCTI_CONTEXT * tctiContext);
    TSS2_RC(*cancel) (TSS2_TCTI_CONTEXT * tctiContext);
    TSS2_RC(*getPollHandles) (TSS2_TCTI_CONTEXT * tctiContext,
                           TSS2_TCTI_POLL_HANDLE * handles,
                           size_t * num_handles);
    TSS2_RC(*setLocality) (TSS2_TCTI_CONTEXT * tctiContext, uint8_t locality);
} TSS2_TCTI_CONTEXT_FAKE;

static TSS2_RC
tcti_fake_ac_send_transmit (
    TSS2_TCTI_CONTEXT *tcti_ctx,
    size_t size,
    const uint8_t *cmd_buf)
{
    UNUSED(tcti_ctx);

    TSS2_RC rc;
    tpm_header_t header;
    rc = header_unmarshal (cmd_buf, &header);
    if (rc != TSS2_RC_SUCCESS) {
        return rc;
    }

    assert_int_equal(header.code, TPM2_CC_AC_Send);

    return TSS2_RC_SUCCESS;
}

static TSS2_RC
tcti_fake_ac_send_receive (
    TSS2_TCTI_CONTEXT * tctiContext,
    size_t * response_size,
    uint8_t * response_buffer, int32_t timeout)
{
    UNUSED(tctiContext);
    UNUSED(timeout);

    *response_size = sizeof(yielded_response);
    if (response_buffer != NULL)
        memcpy(response_buffer, &yielded_response[0], sizeof(yielded_response));

    return TSS2_RC_SUCCESS;
}

static void
tcti_fake_ac_send_finalize (TSS2_TCTI_CONTEXT * tctiContext)
{
    UNUSED(tctiContext);
}

static TSS2_RC
tcti_fake_initialize(TSS2_TCTI_CONTEXT * tctiContext, size_t * contextSize)
{
    TSS2_TCTI_CONTEXT_FAKE *tcti_fake =
        (TSS2_TCTI_CONTEXT_FAKE *) tctiContext;

    if (tctiContext == NULL && contextSize == NULL) {
        return TSS2_TCTI_RC_BAD_VALUE;
    } else if (tctiContext == NULL) {
        *contextSize = sizeof(*tcti_fake);
        return TSS2_RC_SUCCESS;
    }

    /* Init TCTI context */
    memset(tcti_fake, 0, sizeof(*tcti_fake));
    TSS2_TCTI_MAGIC(tctiContext) = TCTI_FAKE_MAGIC;
    TSS2_TCTI_VERSION(tctiContext) = TCTI_FAKE_VERSION;
    TSS2_TCTI_TRANSMIT(tctiContext) = tcti_fake_ac_send_transmit;
    TSS2_TCTI_RECEIVE(tctiContext) = tcti_fake_ac_send_receive;
    TSS2_TCTI_FINALIZE(tctiContext) = tcti_fake_ac_send_finalize;
    TSS2_TCTI_CANCEL(tctiContext) = NULL;
    TSS2_TCTI_GET_POLL_HANDLES(tctiContext) = NULL;
    TSS2_TCTI_SET_LOCALITY(tctiContext) = NULL;

    return TSS2_RC_SUCCESS;
}

static int
setup(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *ectx;
    size_t size = sizeof(TSS2_TCTI_CONTEXT_FAKE);
    TSS2_TCTI_CONTEXT *tcti = malloc(size);

    r = tcti_fake_initialize(tcti, &size);
    if (r)
        return (int)r;
    r = Esys_Initialize(&ectx, tcti, NULL);
    *state = (void *)ectx;
    return (int)r;
}

static int
teardown(void **state)
{
    TSS2_TCTI_CONTEXT *tcti;
    ESYS_CONTEXT *ectx = (ESYS_CONTEXT *) * state;
    Esys_GetTcti(ectx, &tcti);
    Esys_Finalize(&ectx);
    free(tcti);
    return 0;
}

static void
test_ac_send(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *ectx = (ESYS_CONTEXT *) * state;

    r = Esys_AC_Send(ectx, 0, 0, ESYS_TR_NONE,
                     ESYS_TR_NONE, ESYS_TR_NONE, 0, NULL, NULL);

    assert_int_equal(r, TSS2_RC_SUCCESS);
}

int
main(int argc, char *argv[])
{
    UNUSED(argc);
    UNUSED(argv);
    const struct CMUnitTest tests[] = {
        cmocka_unit_test_setup_teardown(test_ac_send, setup, teardown),
    };
    return cmocka_run_group_tests(tests, NULL, NULL);
}
