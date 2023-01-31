/* SPDX-License-Identifier: BSD-2-Clause */
/***********************************************************************
 * Copyright (c) 2017-2018, Intel Corporation
 *
 * All rights reserved.
 ***********************************************************************/
#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <stdarg.h>
#include <stddef.h>
#include <setjmp.h>
#include <cmocka.h>
#include <stdio.h>
#include "tss2_mu.h"
#include "util/tss2_endian.h"

/*
 * Success case
 */
static void
tpma_marshal_success(void **state)
{
    TPMA_ALGORITHM alg = {0}, *ptr;
    TPMA_SESSION session = {0}, *ptr2;
    uint8_t buffer[sizeof(alg)] = { 0 };
    size_t  buffer_size = sizeof(buffer);
    uint8_t buffer2[sizeof(session)] = { 0 };
    size_t  buffer_size2 = sizeof(buffer2);
    uint32_t alg_expected = HOST_TO_BE_32(TPMA_ALGORITHM_ASYMMETRIC | TPMA_ALGORITHM_SIGNING);
    uint8_t session_expected = TPMA_SESSION_AUDIT | TPMA_SESSION_AUDITRESET | TPMA_SESSION_DECRYPT;
    TSS2_RC rc;

    alg |= TPMA_ALGORITHM_ASYMMETRIC;
    alg |= TPMA_ALGORITHM_SIGNING;
    ptr = (TPMA_ALGORITHM *)buffer;

    rc = Tss2_MU_TPMA_ALGORITHM_Marshal(alg, buffer, buffer_size, NULL);
    assert_int_equal (rc, TSS2_RC_SUCCESS);
    assert_int_equal (*ptr, alg_expected);

    session |= TPMA_SESSION_AUDIT;
    session |= TPMA_SESSION_DECRYPT;
    session |= TPMA_SESSION_AUDITRESET;
    ptr2 = (TPMA_SESSION *)buffer2;

    rc = Tss2_MU_TPMA_SESSION_Marshal(session, buffer2, buffer_size2, NULL);
    assert_int_equal (rc, TSS2_RC_SUCCESS);
    assert_int_equal (*ptr2, session_expected);
}

/*
 * Success case with a valid offset
 */
static void
tpma_marshal_success_offset(void **state)
{
    TPMA_ALGORITHM alg = {0}, *ptr;
    TPMA_SESSION session = {0}, *ptr2;
    uint8_t buffer[sizeof(alg) + 10] = { 0 };
    size_t  buffer_size = sizeof(buffer);
    uint8_t buffer2[sizeof(session) + 14] = { 0 };
    size_t  buffer_size2 = sizeof(buffer2);
    size_t offset = 10;
    uint32_t alg_expected = HOST_TO_BE_32(TPMA_ALGORITHM_ASYMMETRIC | TPMA_ALGORITHM_SIGNING);
    uint8_t session_expected = TPMA_SESSION_AUDIT | TPMA_SESSION_AUDITRESET | TPMA_SESSION_DECRYPT;
    TSS2_RC rc;

    alg |= TPMA_ALGORITHM_ASYMMETRIC;
    alg |= TPMA_ALGORITHM_SIGNING;
    ptr = (TPMA_ALGORITHM *)&buffer[10];

    rc = Tss2_MU_TPMA_ALGORITHM_Marshal(alg, buffer, buffer_size, &offset);
    assert_int_equal (rc, TSS2_RC_SUCCESS);
    assert_int_equal (*ptr, alg_expected);
    assert_int_equal (offset, sizeof (buffer));

    session |= TPMA_SESSION_AUDIT;
    session |= TPMA_SESSION_DECRYPT;
    session |= TPMA_SESSION_AUDITRESET;
    ptr2 = (TPMA_SESSION *)&buffer2[14];

    rc = Tss2_MU_TPMA_SESSION_Marshal(session, buffer2, buffer_size2, &offset);
    assert_int_equal (rc, TSS2_RC_SUCCESS);
    assert_int_equal (*ptr2, session_expected);
    assert_int_equal (offset, sizeof (buffer2));
}

/*
 * Success case with a null buffer
 */
static void
tpma_marshal_buffer_null_with_offset(void **state)
{
    TPMA_ALGORITHM alg = {0};
    TPMA_SESSION session = {0};
    size_t offset = 100;
    TSS2_RC rc;

    alg |= TPMA_ALGORITHM_ASYMMETRIC;
    alg |= TPMA_ALGORITHM_SIGNING;

    rc = Tss2_MU_TPMA_ALGORITHM_Marshal(alg, NULL, sizeof(alg), &offset);
    assert_int_equal (rc, TSS2_RC_SUCCESS);
    assert_int_equal (offset, 100 + sizeof(alg));

    session |= TPMA_SESSION_AUDIT;
    session |= TPMA_SESSION_DECRYPT;
    session |= TPMA_SESSION_AUDITRESET;
    offset = 100;

    rc = Tss2_MU_TPMA_SESSION_Marshal(session, NULL, sizeof(session), &offset);
    assert_int_equal (rc, TSS2_RC_SUCCESS);
    assert_int_equal (offset, 100 + sizeof(session));
}

/*
 * Invalid case with a null buffer and a null offset
 */
static void
tpma_marshal_buffer_null_offset_null(void **state)
{
    TPMA_ALGORITHM alg = {0};
    TPMA_SESSION session = {0};
    TSS2_RC rc;

    alg |= TPMA_ALGORITHM_ASYMMETRIC;
    alg |= TPMA_ALGORITHM_SIGNING;

    rc = Tss2_MU_TPMA_ALGORITHM_Marshal(alg, NULL, sizeof(alg), NULL);
    assert_int_equal (rc, TSS2_MU_RC_BAD_REFERENCE);

    session |= TPMA_SESSION_AUDIT;
    session |= TPMA_SESSION_DECRYPT;
    session |= TPMA_SESSION_AUDITRESET;

    rc = Tss2_MU_TPMA_SESSION_Marshal(session, NULL, sizeof(session), NULL);
    assert_int_equal (rc, TSS2_MU_RC_BAD_REFERENCE);
}

/*
 * Invalid case with not big enough buffer
 */
static void
tpma_marshal_buffer_size_lt_data_nad_lt_offset(void **state)
{
    TPMA_ALGORITHM alg = {0};
    TPMA_SESSION session = {0};
    uint8_t buffer[sizeof(alg)] = { 0 };
    size_t  buffer_size = sizeof(buffer);
    uint8_t buffer2[sizeof(session)] = { 0 };
    size_t  buffer_size2 = sizeof(buffer2);
    size_t offset = 2;
    TSS2_RC rc;

    alg |= TPMA_ALGORITHM_ASYMMETRIC;
    alg |= TPMA_ALGORITHM_SIGNING;

    rc = Tss2_MU_TPMA_ALGORITHM_Marshal(alg, buffer, buffer_size, &offset);
    assert_int_equal (rc, TSS2_MU_RC_INSUFFICIENT_BUFFER);
    assert_int_equal (offset, 2);

    session |= TPMA_SESSION_AUDIT;
    session |= TPMA_SESSION_DECRYPT;
    session |= TPMA_SESSION_AUDITRESET;

    rc = Tss2_MU_TPMA_SESSION_Marshal(session, buffer2, buffer_size2, &offset);
    assert_int_equal (rc, TSS2_MU_RC_INSUFFICIENT_BUFFER);
    assert_int_equal (offset, 2);
}

/*
 * Success case
 */
static void
tpma_unmarshal_success(void **state)
{
    TPMA_ALGORITHM alg = {0};
    TPMA_SESSION session = {0};
    uint8_t buffer[sizeof(alg) + sizeof(session)] = { 0 };
    size_t buffer_size = sizeof(buffer);
    size_t offset = 0;
    uint32_t alg_expected = HOST_TO_BE_32(TPMA_ALGORITHM_ASYMMETRIC | TPMA_ALGORITHM_SIGNING);
    uint8_t session_expected = TPMA_SESSION_AUDIT | TPMA_SESSION_AUDITRESET | TPMA_SESSION_DECRYPT;
    uint32_t *ptr;
    uint8_t *ptr2;
    TSS2_RC rc;

    ptr = (uint32_t *)buffer;
    ptr2 = (uint8_t *)ptr + 4;

    *ptr = alg_expected;
    *ptr2 = session_expected;

    rc = Tss2_MU_TPMA_ALGORITHM_Unmarshal(buffer, buffer_size, &offset, &alg);
    assert_int_equal (rc, TSS2_RC_SUCCESS);
    assert_int_equal (alg, BE_TO_HOST_32(alg_expected));
    assert_int_equal (offset, 4);


    rc = Tss2_MU_TPMA_SESSION_Unmarshal(buffer, buffer_size, &offset, &session);
    assert_int_equal (rc, TSS2_RC_SUCCESS);
    assert_int_equal (session, session_expected);
    assert_int_equal (offset, 5);
}

/*
 * Invalid test case with buffer null and dest null
 */
static void
tpma_unmarshal_dest_null_buff_null(void **state)
{
    size_t offset = 0;
    TSS2_RC rc;

    rc = Tss2_MU_TPMA_ALGORITHM_Unmarshal(NULL, 20, &offset, NULL);
    assert_int_equal (rc, TSS2_MU_RC_BAD_REFERENCE);
    assert_int_equal (offset, 0);


    rc = Tss2_MU_TPMA_SESSION_Unmarshal(NULL, 20, &offset, NULL);
    assert_int_equal (rc, TSS2_MU_RC_BAD_REFERENCE);
    assert_int_equal (offset, 0);
}

/*
 * Invalid test case with offset null and dest null
 */
static void
tpma_unmarshal_buffer_null_offset_null(void **state)
{
    TPMA_ALGORITHM alg = {0};
    TPMA_SESSION session = {0};
    uint8_t buffer[sizeof(alg) + sizeof(session)] = { 0 };
    size_t buffer_size = sizeof(buffer);
    TSS2_RC rc;

    rc = Tss2_MU_TPMA_ALGORITHM_Unmarshal(buffer, buffer_size, NULL, NULL);
    assert_int_equal (rc, TSS2_MU_RC_BAD_REFERENCE);


    rc = Tss2_MU_TPMA_SESSION_Unmarshal(buffer, buffer_size, NULL, NULL);
    assert_int_equal (rc, TSS2_MU_RC_BAD_REFERENCE);
}
/*
 * Test case ensures the offset is updated when dest is NULL
 * and offset is valid
 */
static void
tpma_unmarshal_dest_null_offset_valid(void **state)
{
    TPMA_SESSION session = {0};
    uint8_t buffer[sizeof(TPMA_ALGORITHM) + sizeof(session)] = { 0 };
    size_t buffer_size = sizeof(buffer);
    size_t offset = 0;
    uint32_t alg_expected = HOST_TO_BE_32(TPMA_ALGORITHM_ASYMMETRIC | TPMA_ALGORITHM_SIGNING);
    uint8_t session_expected = TPMA_SESSION_AUDIT | TPMA_SESSION_AUDITRESET | TPMA_SESSION_DECRYPT;
    uint32_t *ptr;
    uint8_t *ptr2;
    TSS2_RC rc;

    ptr = (uint32_t *)buffer;
    ptr2 = (uint8_t *)ptr + 4;

    *ptr = alg_expected;
    *ptr2 = session_expected;

    rc = Tss2_MU_TPMA_ALGORITHM_Unmarshal(buffer, buffer_size, &offset, NULL);
    assert_int_equal (rc, TSS2_RC_SUCCESS);
    assert_int_equal (offset, sizeof(TPMA_ALGORITHM));

    rc = Tss2_MU_TPMA_SESSION_Unmarshal(buffer, buffer_size, &offset, NULL);
    assert_int_equal (rc, TSS2_RC_SUCCESS);
    assert_int_equal (offset, sizeof(buffer));
}
/*
 * Invalid case with not big enough buffer
 */
static void
tpma_unmarshal_buffer_size_lt_data_nad_lt_offset(void **state)
{
    TPMA_ALGORITHM alg = {0};
    TPMA_SESSION session = {0};
    uint8_t buffer[sizeof(alg) + sizeof(session)] = { 0 };
    size_t offset = 1;
    TSS2_RC rc;

    alg |= TPMA_ALGORITHM_ASYMMETRIC;
    alg |= TPMA_ALGORITHM_SIGNING;

    rc = Tss2_MU_TPMA_ALGORITHM_Unmarshal(buffer, sizeof(alg), &offset, &alg);
    assert_int_equal (rc, TSS2_MU_RC_INSUFFICIENT_BUFFER);
    assert_int_equal (offset, 1);

    session |= TPMA_SESSION_AUDIT;
    session |= TPMA_SESSION_DECRYPT;
    session |= TPMA_SESSION_AUDITRESET;

    rc = Tss2_MU_TPMA_SESSION_Unmarshal(buffer, 1, &offset, &session);
    assert_int_equal (rc, TSS2_MU_RC_INSUFFICIENT_BUFFER);
    assert_int_equal (offset, 1);
}

int main(void) {
    const struct CMUnitTest tests[] = {
        cmocka_unit_test (tpma_marshal_success),
        cmocka_unit_test (tpma_marshal_success_offset),
        cmocka_unit_test (tpma_marshal_buffer_null_with_offset),
        cmocka_unit_test (tpma_marshal_buffer_null_offset_null),
        cmocka_unit_test (tpma_marshal_buffer_size_lt_data_nad_lt_offset),
        cmocka_unit_test (tpma_unmarshal_success),
        cmocka_unit_test (tpma_unmarshal_dest_null_buff_null),
        cmocka_unit_test (tpma_unmarshal_buffer_null_offset_null),
        cmocka_unit_test (tpma_unmarshal_dest_null_offset_valid),
        cmocka_unit_test (tpma_unmarshal_buffer_size_lt_data_nad_lt_offset),
    };
    return cmocka_run_group_tests(tests, NULL, NULL);
}
