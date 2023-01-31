/* SPDX-License-Identifier: BSD-2-Clause */

#include <stdarg.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <setjmp.h>
#include <cmocka.h>

#include "tss2_rc.h"
#include "util/aux_util.h"

#define TPM2_ERROR_TSS2_RC_LAYER_COUNT (TSS2_RC_LAYER_MASK >> TSS2_RC_LAYER_SHIFT)

#define assert_string_prefix(str, prefix) \
    assert_memory_equal(str, prefix, strlen(prefix))

static void
test_layers(void **state)
{
    UNUSED(state);

    static const char *known_layers[TPM2_ERROR_TSS2_RC_LAYER_COUNT] = {
        "tpm:",
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        "fapi:",
        "esapi:",
        "sys:",
        "mu:",
        "tcti:",
        "rmt",
        "rm",
        "policy",
    };

    UINT8 layer;
    for (layer = 0; layer < TPM2_ERROR_TSS2_RC_LAYER_COUNT; layer++) {
        TSS2_RC rc = TSS2_RC_LAYER(layer);

        const char *got = Tss2_RC_Decode(rc);

        char buf[256];
        snprintf(buf, sizeof(buf), "%u:", layer);

        const char *expected = known_layers[layer] ? known_layers[layer] : buf;
        assert_string_prefix(got, expected);
    }
}

static void
test_tpm_format_0_version2_0_error(void **state)
{
    (void) state;

    const char *m = Tss2_RC_Decode(TPM2_RC_SEQUENCE);
    assert_string_equal(m, "tpm:error(2.0): improper use of a sequence"
            " handle");
}

static void test_tpm_format_0_version2_0_warn(void **state)
{
    (void) state;

    const char *m = Tss2_RC_Decode(TPM2_RC_REFERENCE_H0);
    assert_string_equal(m,
            "tpm:warn(2.0): the 1st handle in the handle area references a"
                    " transient object or session that is not loaded");
}

static void
test_tpm2_format_0_unknown(void **state)
{
    (void) state;

    const char *m = Tss2_RC_Decode(TPM2_RC_NOT_USED + 0x80);
    assert_string_equal(m, "tpm:parameter(1):unknown error num: 0x3F");
}

static void
test_tpm_format_1_unk_handle(void **state)
{
    (void) state;

    const char *m = Tss2_RC_Decode(TPM2_RC_HASH);
    assert_string_equal(m,
            "tpm:handle(unk):hash algorithm not supported or not appropriate");
}

static void
test_tpm_format_1_unk_parameter(void **state)
{
    (void) state;

    const char *m = Tss2_RC_Decode(TPM2_RC_HASH + TPM2_RC_P);
    assert_string_equal(m,
            "tpm:parameter(unk):hash algorithm not supported or not appropriate");
}

static void
test_tpm_format_1_unk_session(void **state)
{
    (void) state;

    const char *m = Tss2_RC_Decode(TPM2_RC_HASH + TPM2_RC_S);
    assert_string_equal(m,
            "tpm:session(unk):hash algorithm not supported or not appropriate");
}

static void
test_tpm_format_1_5_handle(void **state)
{
    (void) state;

    const char *m = Tss2_RC_Decode(TPM2_RC_HASH + TPM2_RC_5);
    assert_string_equal(m,
            "tpm:handle(5):hash algorithm not supported or not appropriate");
}

static void
test_tpm2_format_1_unknown(void **state)
{
    (void) state;

    const char *m = Tss2_RC_Decode(TPM2_RC_NOT_USED + 0x80);
    assert_string_equal(m, "tpm:parameter(1):unknown error num: 0x3F");
}

static void
test_tpm2_format_1_success(void **state)
{
    (void) state;

    const char *m = Tss2_RC_Decode(TPM2_RC_SUCCESS);
    assert_string_equal(m, "tpm:success");
}

static const char *
custom_err_handler(TSS2_RC rc)
{

    static const char *err_map[] = { "error 1", "error 2", "error 3" };

    if (rc - 1u >= ARRAY_LEN(err_map)) {
        return NULL;
    }

    return err_map[rc - 1];
}

static void
test_custom_handler(void **state)
{
    (void) state;

    /*
     * Test registering a custom handler
     */
    TSS2_RC_HANDLER old = Tss2_RC_SetHandler(1, "cstm", custom_err_handler);
    assert_null(old);

    /*
     * Test getting error strings
     */
    unsigned i;
    for (i = 1; i < 4; i++) {
        // Make a layer 1 error with an error number of i.
        TSS2_RC rc = TSS2_RC_LAYER(1) | i;
        char buf[256];
        snprintf(buf, sizeof(buf), "cstm:error %u", i);

        const char *e = Tss2_RC_Decode(rc);
        assert_string_equal(e, buf);
    }

    TSS2_RC rc = TSS2_RC_LAYER(1) | 42;

    /*
     * Test an unknown error
     */
    const char *e = Tss2_RC_Decode(rc);
    assert_string_equal(e, "cstm:0x2A");

    /*
     * Test clearing a handler
     */
    old = Tss2_RC_SetHandler(1, "cstm", NULL);
    assert_ptr_equal(old, custom_err_handler);

    /*
     * Test an unknown layer
     */
    e = Tss2_RC_Decode(rc);
    assert_string_equal(e, "1:0x100");
}

static void
test_zero_length_name(void **state)
{
    (void) state;

    TSS2_RC_HANDLER old = Tss2_RC_SetHandler(TSS2_TPM_RC_LAYER, "",
            custom_err_handler);
    assert_non_null(old);

    old = Tss2_RC_SetHandler(TSS2_TPM_RC_LAYER, "",
            custom_err_handler);
    assert_ptr_equal(old, custom_err_handler);
}

static void
test_over_length_name(void **state)
{
    (void) state;

    TSS2_RC_HANDLER old = Tss2_RC_SetHandler(1, "way to long of name", custom_err_handler);
    assert_null(old);

    old = Tss2_RC_SetHandler(1, "way to long of name", custom_err_handler);
    assert_ptr_equal(old, custom_err_handler);
}

static void
test_null_name(void **state)
{
    (void) state;

    TSS2_RC_HANDLER old = Tss2_RC_SetHandler(1,
    NULL, custom_err_handler);
    assert_ptr_equal(old, custom_err_handler);

    old = Tss2_RC_SetHandler(1,
                             NULL, custom_err_handler);
    assert_ptr_equal(old, custom_err_handler);
}

static void
test_sys(void **state)
{
    (void) state;

    const char *e = Tss2_RC_Decode(TSS2_SYS_RC_ABI_MISMATCH);
    assert_string_equal(e,
            "sys:Passed in ABI version doesn't match called module's ABI version");
}

static void
test_esys(void **state)
{
    (void) state;

    const char *e = Tss2_RC_Decode(TSS2_ESYS_RC_BAD_VALUE);
    assert_string_equal(e,
            "esapi:A parameter has a bad value");
}

static void
test_mu(void **state)
{
    (void) state;

    const char *e = Tss2_RC_Decode(TSS2_MU_RC_BAD_REFERENCE);
    assert_string_equal(e,
            "mu:A pointer is NULL that isn't allowed to be NULL.");

}

static void
test_tcti(void **state)
{
    (void) state;

    const char *e = Tss2_RC_Decode(TSS2_TCTI_RC_NO_CONNECTION);
    assert_string_equal(e, "tcti:Fails to connect to next lower layer");
}

static void
test_info_fmt0(void **state)
{
    TSS2_RC_INFO info = { 1, 2, 3, 4, 5, 6 };
    TSS2_RC test_rc = TSS2_MU_RC_LAYER | TPM2_RC_SESSION_HANDLES;
    TSS2_RC r = Tss2_RC_DecodeInfo(test_rc, &info);
    assert_int_equal(info.layer, 9);
    assert_int_equal(info.format, 0);
    assert_int_equal(info.error, TPM2_RC_SESSION_HANDLES);
    assert_int_equal(info.parameter, 0);
    assert_int_equal(info.handle, 0);
    assert_int_equal(info.session, 0);
    assert_int_equal(r, TSS2_RC_SUCCESS);
}

static void
test_info_fmt1_parameter(void **state)
{
    TSS2_RC_INFO info;
    TSS2_RC test_rc = TSS2_SYS_RC_LAYER | TPM2_RC_ASYMMETRIC | TPM2_RC_P | TPM2_RC_1;
    TSS2_RC r = Tss2_RC_DecodeInfo(test_rc, &info);
    assert_int_equal(info.layer, 8);
    assert_int_equal(info.format, 1);
    assert_int_equal(info.error, TPM2_RC_ASYMMETRIC);
    assert_int_equal(info.parameter, 1);
    assert_int_equal(info.handle, 0);
    assert_int_equal(info.session, 0);
    assert_int_equal(r, TSS2_RC_SUCCESS);
}

static void
test_info_fmt1_handle(void **state)
{
    TSS2_RC_INFO info;
    TSS2_RC test_rc = TSS2_ESAPI_RC_LAYER | TPM2_RC_HANDLE | TPM2_RC_H | TPM2_RC_2;
    TSS2_RC r = Tss2_RC_DecodeInfo(test_rc, &info);
    assert_int_equal(info.layer, 7);
    assert_int_equal(info.error, TPM2_RC_HANDLE);
    assert_int_equal(info.parameter, 0);
    assert_int_equal(info.handle, 2);
    assert_int_equal(info.session, 0);
    assert_int_equal(r, TSS2_RC_SUCCESS);
}

static void
test_info_fmt1_session(void **state)
{
    TSS2_RC_INFO info;
    TSS2_RC test_rc = TSS2_FEATURE_RC_LAYER | TPM2_RC_EXPIRED | TPM2_RC_S | TPM2_RC_3;
    TSS2_RC r = Tss2_RC_DecodeInfo(test_rc, &info);
    assert_int_equal(info.layer, 6);
    assert_int_equal(info.error, TPM2_RC_EXPIRED);
    assert_int_equal(info.parameter, 0);
    assert_int_equal(info.handle, 0);
    assert_int_equal(info.session, 3);
    assert_int_equal(r, TSS2_RC_SUCCESS);
}

static void
test_info_null(void **state)
{
    TSS2_RC r = Tss2_RC_DecodeInfo(TSS2_RC_SUCCESS, NULL);
    assert_int_equal(r, TSS2_BASE_RC_BAD_REFERENCE);
}

static void
test_info_str_fmt1(void **state)
{
    TSS2_RC_INFO info = {
        .error = TPM2_RC_EXPIRED,
        .format = 1,
    };
    const char *m = Tss2_RC_DecodeInfoError(&info);
    assert_string_equal(m, "the policy has expired");
}

static void
test_info_str_fmt1_ff(void **state)
{
    TSS2_RC_INFO info = {
        .error = 0xFF,
        .format = 1,
    };
    const char *m = Tss2_RC_DecodeInfoError(&info);
    assert_string_equal(m, "0xFF");
}

static void
test_info_str_fmt0_err(void **state)
{
    TSS2_RC_INFO info = {
        .error = TPM2_RC_COMMAND_CODE,
        .format = 0,
    };
    const char *m = Tss2_RC_DecodeInfoError(&info);
    assert_string_equal(m, "command code not supported");
}

static void
test_info_str_fmt0_warn(void **state)
{
    TSS2_RC_INFO info = {
        .error = TPM2_RC_TESTING,
        .format = 0,
    };
    const char *m = Tss2_RC_DecodeInfoError(&info);
    assert_string_equal(m, "TPM is performing selftests");
}

static void
test_info_str_fmt0_ff(void **state)
{
    TSS2_RC_INFO info = {
        .error = 0xFF,
        .format = 0,
    };
    const char *m = Tss2_RC_DecodeInfoError(&info);
    assert_string_equal(m, "0xFF");
}

static void
test_info_str_null(void **state)
{
    const char *m = Tss2_RC_DecodeInfoError(NULL);
    assert_null(m);
}

static void
test_all_FFs(void **state)
{
    (void) state;

    const char *e = Tss2_RC_Decode(0xFFFFFFFF);
    assert_string_equal(e, "255:0xFFFFFF");
}

static void
test_all_FFs_set_handler(void **state)
{
    (void) state;
    Tss2_RC_SetHandler(0xFF, "garbage", custom_err_handler);
    Tss2_RC_SetHandler(0xFF, NULL, NULL);
}

/* link required symbol, but tpm2_tool.c declares it AND main, which
 * we have a main below for cmocka tests.
 */
bool output_enabled = true;

int
main(int argc, char* argv[])
{
    (void) argc;
    (void) argv;

    const struct CMUnitTest tests[] = {
            /* Layer tests */
            cmocka_unit_test(test_layers),
            cmocka_unit_test(test_tpm_format_0_version2_0_error),
            cmocka_unit_test(test_tpm_format_0_version2_0_warn),
            cmocka_unit_test(test_tpm2_format_0_unknown),
            cmocka_unit_test(test_tpm_format_1_unk_handle),
            cmocka_unit_test(test_tpm_format_1_unk_parameter),
            cmocka_unit_test(test_tpm_format_1_unk_session),
            cmocka_unit_test(test_tpm_format_1_5_handle),
            cmocka_unit_test(test_tpm2_format_1_unknown),
            cmocka_unit_test(test_tpm2_format_1_success),
            cmocka_unit_test(test_custom_handler),
            cmocka_unit_test(test_zero_length_name),
            cmocka_unit_test(test_over_length_name),
            cmocka_unit_test(test_null_name),
            cmocka_unit_test(test_sys),
            cmocka_unit_test(test_esys),
            cmocka_unit_test(test_mu),
            cmocka_unit_test(test_tcti),
            cmocka_unit_test(test_info_fmt0),
            cmocka_unit_test(test_info_fmt1_parameter),
            cmocka_unit_test(test_info_fmt1_handle),
            cmocka_unit_test(test_info_fmt1_session),
            cmocka_unit_test(test_info_null),
            cmocka_unit_test(test_info_str_fmt1),
            cmocka_unit_test(test_info_str_fmt1_ff),
            cmocka_unit_test(test_info_str_fmt0_err),
            cmocka_unit_test(test_info_str_fmt0_warn),
            cmocka_unit_test(test_info_str_fmt0_ff),
            cmocka_unit_test(test_info_str_null),
            cmocka_unit_test(test_all_FFs),
            cmocka_unit_test(test_all_FFs_set_handler)
    };

    return cmocka_run_group_tests(tests, NULL, NULL);
}
