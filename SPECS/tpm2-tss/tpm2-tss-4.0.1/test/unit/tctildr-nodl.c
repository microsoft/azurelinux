/*
 * SPDX-License-Identifier: BSD-2-Clause
 * Copyright 2018, Fraunhofer SIT sponsored by Infineon Technologies AG
 * Copyright 2019, Intel Corporation
 * All rights reserved.
 */
#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <stdio.h>
#include <stddef.h>
#include <stdlib.h>

#include <dlfcn.h>

#include <setjmp.h>
#include <cmocka.h>

#include "tss2_tcti.h"

#include "tss2-tcti/tctildr-interface.h"
#include "tss2-tcti/tctildr-nodl.h"
#define LOGMODULE test
#include "util/log.h"

TSS2_RC
__wrap_Tss2_Tcti_Device_Init(TSS2_TCTI_CONTEXT *tctiContext, size_t *size,
                             const char *config)
{
    return TSS2_RC_SUCCESS;
}

TSS2_RC
__wrap_Tss2_Tcti_Mssim_Init(TSS2_TCTI_CONTEXT *tctiContext, size_t *size,
                            const char *config)
{
   return TSS2_RC_SUCCESS;
}

TSS2_RC
__wrap_tcti_from_init(TSS2_TCTI_INIT_FUNC init,
                      const char* conf,
                      TSS2_TCTI_CONTEXT **tcti)
{
    if (tcti != NULL)
        *tcti = mock_type (TSS2_TCTI_CONTEXT*);
    return mock_type (TSS2_RC);
}
void
test_tctildr_get_default_null_param (void **state)
{
    TSS2_RC rc;

    rc = tctildr_get_default (NULL, NULL);
    assert_int_equal (rc, TSS2_TCTI_RC_BAD_REFERENCE);
}
void
test_tctildr_get_default_all_fail (void **state)
{
    TSS2_RC rc;
    TSS2_TCTI_CONTEXT *tcti_ctx = NULL;

#define TEST_RC 0x65203563
    /* device:/dev/tpm0 */
    will_return (__wrap_tcti_from_init, tcti_ctx);
    will_return (__wrap_tcti_from_init, TEST_RC);
    /* device:/dev/tpmrm0 */
    will_return (__wrap_tcti_from_init, tcti_ctx);
    will_return (__wrap_tcti_from_init, TEST_RC);
    /* swtpm */
    will_return (__wrap_tcti_from_init, tcti_ctx);
    will_return (__wrap_tcti_from_init, TEST_RC);
#if defined (TCTI_MSSIM) && defined (TCTI_SWTPM)
    /* second swtpm if enabled */
    will_return (__wrap_tcti_from_init, tcti_ctx);
    will_return (__wrap_tcti_from_init, TEST_RC);
#endif
    rc = tctildr_get_default (&tcti_ctx, NULL);
    assert_int_equal (rc, TSS2_TCTI_RC_IO_ERROR);

}
static TSS2_TCTI_CONTEXT_COMMON_V2 test_ctx = { 0, };
void
test_get_tcti_null_tcti (void **state)
{
    TSS2_RC rc = tctildr_get_tcti (NULL, NULL, NULL, NULL);
    assert_int_equal (rc, TSS2_TCTI_RC_BAD_REFERENCE);
}

void
test_get_tcti_default_success (void **state)
{
    TSS2_RC rc;
    TSS2_TCTI_CONTEXT *tcti_ctx = NULL;

    will_return (__wrap_tcti_from_init, &test_ctx);
    will_return (__wrap_tcti_from_init, TSS2_RC_SUCCESS);
    rc = tctildr_get_tcti (NULL, NULL, &tcti_ctx, NULL);
    assert_int_equal (rc, TSS2_RC_SUCCESS);
    assert_ptr_equal (tcti_ctx, &test_ctx);
}
void
test_get_tcti_match_second (void **state)
{
    TSS2_RC rc;
    TSS2_TCTI_CONTEXT *tcti_ctx = NULL;

    will_return (__wrap_tcti_from_init, &test_ctx);
    will_return (__wrap_tcti_from_init, TSS2_RC_SUCCESS);
    rc = tctildr_get_tcti ("libtss2-tcti-device.so", NULL, &tcti_ctx, NULL);
    assert_int_equal (rc, TSS2_RC_SUCCESS);
    assert_ptr_equal (tcti_ctx, &test_ctx);
}
void
test_get_tcti_match_none (void **state)
{
    TSS2_RC rc;
    TSS2_TCTI_CONTEXT *tcti_ctx = NULL;

    rc = tctildr_get_tcti ("foo", NULL, &tcti_ctx, NULL);
    assert_int_equal (rc, TSS2_TCTI_RC_IO_ERROR);
 }
void
test_finalize_data (void **state)
{
    tctildr_finalize_data (NULL);
}
void
test_get_info (void **state)
{
    TSS2_RC rc = tctildr_get_info (NULL, NULL, NULL);
    assert_int_equal (rc, TSS2_TCTI_RC_NOT_SUPPORTED);
}
int
main(void)
{
    const struct CMUnitTest tests[] = {
        cmocka_unit_test (test_tctildr_get_default_null_param),
        cmocka_unit_test (test_tctildr_get_default_all_fail),
        cmocka_unit_test (test_get_tcti_null_tcti),
        cmocka_unit_test (test_get_tcti_default_success),
        cmocka_unit_test (test_get_tcti_match_second),
        cmocka_unit_test (test_get_tcti_match_none),
        cmocka_unit_test (test_finalize_data),
        cmocka_unit_test (test_get_info),
    };
    return cmocka_run_group_tests (tests, NULL, NULL);
}
