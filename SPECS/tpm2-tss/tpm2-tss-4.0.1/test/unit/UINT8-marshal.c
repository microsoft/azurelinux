/* SPDX-License-Identifier: BSD-2-Clause */
/***********************************************************************
 * Copyright (c) 2017-2018, Intel Corporation
 *
 * All rights reserved.
 ***********************************************************************/
#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <stdlib.h>
#include <stdio.h>

#include <setjmp.h>
#include <cmocka.h>

#include "tss2_mu.h"

/*
 * Test case for successful UINT8 marshaling with NULL offset.
 */
void
UINT8_marshal_success (void **state)
{
    UINT8   src = 0x1a;
    uint8_t buffer [1] = { 0 };
    size_t  buffer_size = sizeof (buffer);
    TSS2_RC rc;

    rc = Tss2_MU_UINT8_Marshal (src, buffer, buffer_size, NULL);

    assert_int_equal (rc, TSS2_RC_SUCCESS);
    assert_int_equal (src, buffer [0]);
}
/*
 * Test case for successful UINT8 marshaling with offset.
 */
void
UINT8_marshal_success_offset (void **state)
{
    UINT8 src = 0x1a;
    uint8_t buffer [2] = { 0 };
    size_t  buffer_size = sizeof (buffer);
    size_t  offset = 1;
    TSS2_RC rc;

    rc = Tss2_MU_UINT8_Marshal (src, buffer, buffer_size, &offset);

    assert_int_equal (rc, TSS2_RC_SUCCESS);
    assert_int_equal (src, buffer [1]);
    assert_int_equal (offset, sizeof (buffer));
}
/*
 * Test case passing NULL buffer and non-NULL offset. Test to be sure offset
 * is updated to the size of the src parameter.
 */
void
UINT8_marshal_buffer_null_with_offset (void **state)
{
    UINT8 src = 0x1a;
    size_t offset = 100;
    TSS2_RC rc;

    rc = Tss2_MU_UINT8_Marshal (src, NULL, 2, &offset);

    assert_int_equal (rc, TSS2_RC_SUCCESS);
    assert_int_equal (offset, 100 + sizeof (src));
}
/*
 * Test case passing NULL buffer and NULL offset. This
 */
void
UINT8_marshal_buffer_null_offset_null (void **state)
{
    UINT8 src = 0x1a;
    TSS2_RC rc;

    rc = Tss2_MU_UINT8_Marshal (src, NULL, sizeof (src), NULL);

    assert_int_equal (rc, TSS2_MU_RC_BAD_REFERENCE);
}
/*
 * Test failing case where buffer_size - offset (size of available space
 * in buffer) is less than sizeof (UINT8). Also check offset is unchanged.
 */
void
UINT8_marshal_buffer_size_lt_data (void **state)
{
    UINT8   src = 0x1a;
    uint8_t buffer [2] = { 0 };
    size_t  offset = 2;
    TSS2_RC rc;

    rc = Tss2_MU_UINT8_Marshal (src, buffer, sizeof (src), &offset);

    assert_int_equal (rc, TSS2_MU_RC_INSUFFICIENT_BUFFER);
    assert_int_equal (offset, 2);
}
/*
 * Test failing case where buffer_size is less than the offset value.
 * This should return INSUFFICIENT_BUFFER and the offset should be unchanged.
 */
void
UINT8_marshal_buffer_size_lt_offset (void **state)
{
    UINT8   src = 0x1a;
    uint8_t buffer [2] = { 0 };
    size_t  buffer_size = sizeof (buffer);
    size_t  offset = sizeof (buffer) + 1;
    TSS2_RC rc;

    rc = Tss2_MU_UINT8_Marshal (src, buffer, buffer_size, &offset);

    assert_int_equal (rc, TSS2_MU_RC_INSUFFICIENT_BUFFER);
    assert_int_equal (offset, sizeof (buffer) + 1);
}
/*
 * Test case for successful UINT8 unmarshaling.
 */
void
UINT8_unmarshal_success (void **state)
{
    uint8_t buffer [1] = { 0xa1 };
    uint8_t buffer_size = sizeof (buffer);
    UINT8   dest = 0;
    TSS2_RC rc;

    rc = Tss2_MU_UINT8_Unmarshal (buffer, buffer_size, NULL, &dest);

    assert_int_equal (rc, TSS2_RC_SUCCESS);
    assert_int_equal (buffer [0], dest);
}
/*
 * Test case for successful UINT8 unmarshaling with offset.
 */
void
UINT8_unmarshal_success_offset (void **state)
{
    UINT8   dest = 0;
    uint8_t buffer [2] = { 0x00, 0xa1 };
    size_t  buffer_size = sizeof (buffer);
    size_t  offset = 1;
    TSS2_RC rc;

    rc = Tss2_MU_UINT8_Unmarshal (buffer, buffer_size, &offset, &dest);

    assert_int_equal (rc, TSS2_RC_SUCCESS);
    assert_int_equal (buffer [1], dest);
    assert_int_equal (offset, 2);
}
/*
 * Test case ensures a NULL buffer parameter produces a BAD_REFERENCE RC.
 */
void
UINT8_unmarshal_buffer_null (void **state)
{
    TSS2_RC rc;

    rc = Tss2_MU_UINT8_Unmarshal (NULL, 1, NULL, NULL);

    assert_int_equal (rc, TSS2_MU_RC_BAD_REFERENCE);
}
/*
 * Test case ensures a NULL dest and offset parameters produce an
 * INSUFFICIENT_BUFFER RC.
 */
void
UINT8_unmarshal_dest_null (void **state)
{
    uint8_t buffer [1] = { 0 };
    TSS2_RC rc;

    rc = Tss2_MU_UINT8_Unmarshal (buffer, sizeof (buffer), NULL, NULL);

    assert_int_equal (rc, TSS2_MU_RC_BAD_REFERENCE);
}
/*
 * Test case ensures the offset is updated when dest is NULL
 * and offset is valid
 */
void
UINT8_unmarshal_dest_null_offset_valid (void **state)
{
    uint8_t buffer [2] = { 0 };
    size_t  offset = 1;
    TSS2_RC rc;

    rc = Tss2_MU_UINT8_Unmarshal (buffer, sizeof (buffer), &offset, NULL);

    assert_int_equal (rc, TSS2_RC_SUCCESS);
    assert_int_equal (offset, 2);
}

/*
 * Test case ensures that INSUFFICIENT_BUFFER is returned when buffer_size
 * is less than the provided offset.
 */
void
UINT8_unmarshal_buffer_size_lt_offset (void **state)
{
    UINT8   dest = 0;
    uint8_t buffer [1] = { 0 };
    size_t  offset = sizeof (buffer) + 1;
    TSS2_RC rc;

    rc = Tss2_MU_UINT8_Unmarshal (buffer, sizeof (buffer), &offset, &dest);

    assert_int_equal (rc, TSS2_MU_RC_INSUFFICIENT_BUFFER);
    assert_int_equal (offset, sizeof (buffer) + 1);
    assert_int_equal (dest, 0);
}
/*
 * Test case ensures that INSUFFICIENT_BUFFER is returned when buffer_size -
 * local_offset is less than dest (the destination type).
 */
void
UINT8_unmarshal_buffer_size_lt_dest (void **state)
{
    UINT8   dest = 0;
    uint8_t buffer [1] = { 0 };
    size_t  offset = sizeof (buffer);
    TSS2_RC rc;

    rc = Tss2_MU_UINT8_Unmarshal (buffer, sizeof (buffer), &offset, &dest);

    assert_int_equal (rc, TSS2_MU_RC_INSUFFICIENT_BUFFER);
    assert_int_equal (offset, sizeof (buffer));
    assert_int_equal (dest, 0);
}
int
main (void)
{
    const struct CMUnitTest tests [] = {
        cmocka_unit_test (UINT8_marshal_success),
        cmocka_unit_test (UINT8_marshal_success_offset),
        cmocka_unit_test (UINT8_marshal_buffer_null_with_offset),
        cmocka_unit_test (UINT8_marshal_buffer_null_offset_null),
        cmocka_unit_test (UINT8_marshal_buffer_size_lt_data),
        cmocka_unit_test (UINT8_marshal_buffer_size_lt_offset),
        cmocka_unit_test (UINT8_unmarshal_success),
        cmocka_unit_test (UINT8_unmarshal_success_offset),
        cmocka_unit_test (UINT8_unmarshal_buffer_null),
        cmocka_unit_test (UINT8_unmarshal_dest_null),
        cmocka_unit_test (UINT8_unmarshal_dest_null_offset_valid),
        cmocka_unit_test (UINT8_unmarshal_buffer_size_lt_offset),
        cmocka_unit_test (UINT8_unmarshal_buffer_size_lt_dest),
    };
    return cmocka_run_group_tests (tests, NULL, NULL);
}
