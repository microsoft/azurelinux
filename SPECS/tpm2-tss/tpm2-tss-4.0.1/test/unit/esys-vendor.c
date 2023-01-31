/* SPDX-License-Identifier: BSD-2-Clause */

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <ctype.h>
#include <stdarg.h>
#include <inttypes.h>
#include <string.h>
#include <stdlib.h>

#include <setjmp.h>
#include <cmocka.h>

#include "tss2_esys.h"

#define LOGMODULE tests
#include "util/log.h"

typedef struct vendor_tests vendor_tests;
struct vendor_tests {
    const char *id; /* name this to the name of the test function */
    char *resp;     /* The response buffer of the TPM as a hex string */
    char *expected; /* The expected data to check in the test as a hex string */
};

vendor_tests tests[] =
{
    {
        .id = "ptt_property_1_count_1024",
        .resp = "8001000000170000000001000001000000000100000003",
        .expected = "0000000100000003"
    },
};

/* This passes the function name to TCTI Recieve function where a lookup of function name
 * to response buffer occurs. This SHOULD be called for tests expecting to use the
 * the tests[] array above before any calls to ESAPI, etc occur.
 */
#define TEST_MOCK_SETUP will_return_always(tcti_fake_recv, __func__)

static void
unhex(const char *hexstr, uint8_t *buf, size_t *len)
{
    /* should always be even in length ie bit index 0 unset */
    size_t l = strlen(hexstr);
    assert_false(l & 0x1);

    /* div 2 */
    *len = l >> 1;

    size_t i;
    for (i = 0; i < *len; i++) {
        char tmp_str[4] = {0};
        tmp_str[0] = hexstr[i * 2];
        tmp_str[1] = hexstr[i * 2 + 1];
        buf[i] = strtol(tmp_str, NULL, 16);
    }
}

#define get_expected(buf) _get_expected(__func__, (buf)->buffer, &(buf)->size)
static void _get_expected(const char *id, uint8_t *resp_buf, UINT16 *resp_len)
{

    size_t i;
    for (i = 0; i < sizeof(tests) / sizeof(tests[0]); i++) {
        vendor_tests *t = &tests[i];
        if (!strcmp(t->id, id)) {
            size_t len;
            unhex(t->expected, resp_buf, &len);
            *resp_len = (UINT16)len;
            return;
        }
    }
    assert_true(false);

}

static void get_response(const char *id, uint8_t *resp_buf, size_t *resp_len)
{

    if (!resp_buf) {
        *resp_len = 4096;
        return;
    }

    size_t i;
    for (i = 0; i < sizeof(tests) / sizeof(tests[0]); i++) {
        vendor_tests *t = &tests[i];
        if (!strcmp(t->id, id)) {
            unhex(t->resp, resp_buf, resp_len);
            return;
        }
    }
    assert_true(false);
}

#define TCTI_FAKE_MAGIC 0x46414b4500000000ULL        /* 'FAKE\0' */
#define TCTI_FAKE_VERSION 0x1

typedef TSS2_TCTI_CONTEXT_COMMON_V1 TSS2_TCTI_CONTEXT_FAKE;

void
tcti_fake_finalize(TSS2_TCTI_CONTEXT *tctiContext)
{
    UNUSED(tctiContext);
}

static TSS2_RC tcti_fake_transmit(
        TSS2_TCTI_CONTEXT *tctiContext,
        size_t size,
        uint8_t const *command)
{

    UNUSED(tctiContext);
    UNUSED(size);
    UNUSED(command);
    return TSS2_RC_SUCCESS;
}

static TSS2_RC tcti_fake_recv(
        TSS2_TCTI_CONTEXT *tctiContext,
        size_t *size,
        uint8_t *response,
        int32_t timeout)
{
    UNUSED(tctiContext);
    UNUSED(timeout);

    const char *id = (const char*)mock();

    get_response(id, response, size);
    return TSS2_RC_SUCCESS;
}

TSS2_RC
Tss2_FAKE_TCTI_Initialize(const char *nameConf,
        TSS2_TCTI_CONTEXT **tcti)
{
    if (tcti == NULL)
        return TSS2_BASE_RC_GENERAL_FAILURE;

    /* This is to calm down scan-build */
    TSS2_TCTI_CONTEXT_FAKE **faketcti = (TSS2_TCTI_CONTEXT_FAKE**)tcti;

    *faketcti = calloc(1, sizeof(TSS2_TCTI_CONTEXT_FAKE));
    TSS2_TCTI_MAGIC(*faketcti) = TCTI_FAKE_MAGIC;
    TSS2_TCTI_VERSION(*faketcti) = TCTI_FAKE_VERSION;
    TSS2_TCTI_TRANSMIT(*faketcti) = tcti_fake_transmit;
    TSS2_TCTI_RECEIVE(*faketcti) = tcti_fake_recv;
    TSS2_TCTI_FINALIZE(*faketcti) = tcti_fake_finalize;
    TSS2_TCTI_CANCEL(*faketcti) = NULL;
    TSS2_TCTI_GET_POLL_HANDLES(*faketcti) = NULL;
    TSS2_TCTI_SET_LOCALITY(*faketcti) = NULL;

    return TSS2_RC_SUCCESS;
}

static int test_setup(void **state)
{
    Tss2_FAKE_TCTI_Initialize(NULL,
            (TSS2_TCTI_CONTEXT**)state);
    return 0;
}

static int test_teardown(void **state)
{
    free(*state);
    *state = NULL;
    return 0;
}

static void
ptt_property_1_count_1024(void **state)
{
    TSS2_RC r;
    ESYS_CONTEXT *ectx;

    TEST_MOCK_SETUP;

    r = Esys_Initialize(&ectx, (TSS2_TCTI_CONTEXT*)*state, NULL);
    assert_int_equal(r, TSS2_RC_SUCCESS);

    TPMI_YES_NO more_data;
    TPMS_CAPABILITY_DATA *cap_data = NULL;
    r = Esys_GetCapability(ectx, ESYS_TR_NONE, ESYS_TR_NONE, ESYS_TR_NONE,
        TPM2_CAP_VENDOR_PROPERTY, 1, 1024, &more_data, &cap_data);
    assert_int_equal(r, TSS2_RC_SUCCESS);
    assert_int_equal(cap_data->capability, TPM2_CAP_VENDOR_PROPERTY);

    TPM2B_MAX_CAP_BUFFER expected = {0};
    get_expected(&expected);
    assert_int_equal(cap_data->data.vendor.size, expected.size);
    assert_memory_equal(cap_data->data.vendor.buffer, expected.buffer,
            expected.size);

    Esys_Free(cap_data);
    Esys_Finalize(&ectx);
}

int
main(int argc, char *argv[])
{
    const struct CMUnitTest tests[] = {
    cmocka_unit_test_setup_teardown(ptt_property_1_count_1024,
            test_setup, test_teardown),
    };
    return cmocka_run_group_tests(tests, NULL, NULL);
}
