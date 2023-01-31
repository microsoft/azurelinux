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
#include <string.h>
#include <setjmp.h>
#include <cmocka.h>
#include <stdio.h>
#include "tss2_mu.h"
#include "util/tss2_endian.h"

/*
 * Success case
 */
static void
tpml_marshal_success(void **state)
{
    TPML_HANDLE hndl = {0};
    TPML_PCR_SELECTION sel = {0};
    uint8_t buffer[sizeof(hndl) + sizeof(sel)] = { 0 };
    size_t  buffer_size = sizeof(buffer);
    TPML_HANDLE *ptr;
    TSS2_RC rc;

    hndl.count = 2;
    hndl.handle[0] = 0x81000001;
    hndl.handle[1] = 0x81000002;

    ptr = (TPML_HANDLE *) buffer;

    rc = Tss2_MU_TPML_HANDLE_Marshal(&hndl, buffer, buffer_size, NULL);
    assert_int_equal (rc, TSS2_RC_SUCCESS);
    assert_int_equal (ptr->count, HOST_TO_BE_32(2));
    assert_int_equal (ptr->handle[0], HOST_TO_BE_32(0x81000001));
    assert_int_equal (ptr->handle[1], HOST_TO_BE_32(0x81000002));

    sel.count = 2;
    sel.pcrSelections[0].hash = TPM2_ALG_SHA1;
    sel.pcrSelections[0].sizeofSelect = 3;
    sel.pcrSelections[0].pcrSelect[0] = 0xaa;
    sel.pcrSelections[0].pcrSelect[1] = 0xbb;
    sel.pcrSelections[0].pcrSelect[2] = 0xcc;
    sel.pcrSelections[1].hash = TPM2_ALG_SHA256;
    sel.pcrSelections[1].sizeofSelect = 2;
    sel.pcrSelections[1].pcrSelect[0] = 0xdd;
    sel.pcrSelections[1].pcrSelect[1] = 0xee;

    rc = Tss2_MU_TPML_PCR_SELECTION_Marshal(&sel, buffer, buffer_size, NULL);
    assert_int_equal (rc, TSS2_RC_SUCCESS);

    uint8_t expect [] = {
        0, 0, 0, 2,
        0, 0x04, /* TPM2_ALG_SHA1 */
        3,
        0xaa, 0xbb, 0xcc,
        0, 0x0b, /* TPM2_ALG_SHA256 */
        2,
        0xdd, 0xee};

    assert_memory_equal(buffer, &expect[0], sizeof(expect));
}

/*
 * Success case with a valid offset
 */
static void
tpml_marshal_success_offset(void **state)
{
    TPML_HANDLE hndl = {0};
    TPML_PCR_SELECTION sel = {0};
    uint8_t buffer[sizeof(hndl) + sizeof(sel) + 10] = { 0 };
    size_t  buffer_size = sizeof(buffer);
    TPML_HANDLE *ptr;
    size_t offset = 10;
    TSS2_RC rc;

    hndl.count = 2;
    hndl.handle[0] = 0x81000001;
    hndl.handle[1] = 0x81000002;

    ptr = (TPML_HANDLE *) (buffer + 10);

    rc = Tss2_MU_TPML_HANDLE_Marshal(&hndl, buffer, buffer_size, &offset);
    assert_int_equal (rc, TSS2_RC_SUCCESS);
    assert_int_equal (ptr->count, HOST_TO_BE_32(2));
    assert_int_equal (ptr->handle[0], HOST_TO_BE_32(0x81000001));
    assert_int_equal (ptr->handle[1], HOST_TO_BE_32(0x81000002));
    assert_int_equal (offset, 10 + 4 + 4 + 4);

    sel.count = 2;
    sel.pcrSelections[0].hash = TPM2_ALG_SHA1;
    sel.pcrSelections[0].sizeofSelect = 3;
    sel.pcrSelections[0].pcrSelect[0] = 0xaa;
    sel.pcrSelections[0].pcrSelect[1] = 0xbb;
    sel.pcrSelections[0].pcrSelect[2] = 0xcc;
    sel.pcrSelections[1].hash = TPM2_ALG_SHA256;
    sel.pcrSelections[1].sizeofSelect = 2;
    sel.pcrSelections[1].pcrSelect[0] = 0xdd;
    sel.pcrSelections[1].pcrSelect[1] = 0xee;

    rc = Tss2_MU_TPML_PCR_SELECTION_Marshal(&sel, buffer, buffer_size, &offset);
    assert_int_equal (rc, TSS2_RC_SUCCESS);

    uint8_t expect [] = {
        0, 0, 0, 2,
        0, 0x04, /* TPM2_ALG_SHA1 */
        3,
        0xaa, 0xbb, 0xcc,
        0, 0x0b, /* TPM2_ALG_SHA256 */
        2,
        0xdd, 0xee};

    assert_memory_equal((buffer + 10 + 4 + 4 + 4), &expect[0], sizeof(expect));

    assert_int_equal (offset, 10 + 4 + 4 + 4 + 4 + 2 + 1 + 1 + 1 + 1 + 2 + 1 + 1 + 1);
}

/*
 * Success case with a null buffer
 */
static void
tpml_marshal_buffer_null_with_offset(void **state)
{
    TPML_HANDLE hndl = {0};
    TPML_PCR_SELECTION sel = {0};
    TPML_DIGEST dgst = {0};
    TPML_DIGEST_VALUES dgst_vals = {0};
    size_t  buffer_size = sizeof(hndl) + sizeof(sel) + sizeof(dgst) + 99;
    size_t offset = 99;
    TSS2_RC rc;

    hndl.count = 2;
    hndl.handle[0] = 0x81000001;
    hndl.handle[1] = 0x81000002;

    rc = Tss2_MU_TPML_HANDLE_Marshal(&hndl, NULL, buffer_size, &offset);
    assert_int_equal (rc, TSS2_RC_SUCCESS);
    assert_int_equal (offset, 99 + 4 + 4 + 4);

    sel.count = 2;
    sel.pcrSelections[0].hash = TPM2_ALG_SHA1;
    sel.pcrSelections[0].sizeofSelect = 3;
    sel.pcrSelections[0].pcrSelect[0] = 0xaa;
    sel.pcrSelections[0].pcrSelect[1] = 0xbb;
    sel.pcrSelections[0].pcrSelect[2] = 0xcc;
    sel.pcrSelections[1].hash = TPM2_ALG_SHA256;
    sel.pcrSelections[1].sizeofSelect = 2;
    sel.pcrSelections[1].pcrSelect[0] = 0xdd;
    sel.pcrSelections[1].pcrSelect[1] = 0xee;

    rc = Tss2_MU_TPML_PCR_SELECTION_Marshal(&sel, NULL, buffer_size, &offset);
    assert_int_equal (rc, TSS2_RC_SUCCESS);
    assert_int_equal (offset, 99 + 4 + 4 + 4 + 4 + 2 + 1 + 1 + 1 + 1 + 2 + 1 + 1 + 1);

    offset = 99;
    dgst.count = 2;
    dgst.digests[0].size = TPM2_SHA1_DIGEST_SIZE;
    dgst.digests[1].size = TPM2_SHA512_DIGEST_SIZE;
    rc = Tss2_MU_TPML_DIGEST_Marshal(&dgst, NULL, buffer_size, &offset);
    assert_int_equal (rc, TSS2_RC_SUCCESS);
    assert_int_equal (offset, 99 + sizeof(UINT32) + 2*sizeof(UINT16) +
                      TPM2_SHA1_DIGEST_SIZE + TPM2_SHA512_DIGEST_SIZE);

    offset = 99;
    dgst_vals.count = 2;
    dgst_vals.digests[0].hashAlg = TPM2_ALG_SHA1;
    dgst_vals.digests[1].hashAlg = TPM2_ALG_SHA512;
    rc = Tss2_MU_TPML_DIGEST_VALUES_Marshal(&dgst_vals, NULL, buffer_size, &offset);
    assert_int_equal (rc, TSS2_RC_SUCCESS);
    assert_int_equal (offset, 99 + sizeof(UINT32) + 2*sizeof(TPMI_ALG_HASH) +
                      TPM2_SHA1_DIGEST_SIZE + TPM2_SHA512_DIGEST_SIZE);
}

/*
 * Invalid case with a null buffer and a null offset
 */
static void
tpml_marshal_buffer_null_offset_null(void **state)
{
    TPML_HANDLE hndl = {0};
    TPML_PCR_SELECTION sel = {0};
    TSS2_RC rc;

    hndl.count = 2;
    hndl.handle[0] = 0x81000001;
    hndl.handle[1] = 0x81000002;

    rc = Tss2_MU_TPML_HANDLE_Marshal(&hndl, NULL, sizeof(hndl), NULL);
    assert_int_equal (rc, TSS2_MU_RC_BAD_REFERENCE);

    rc = Tss2_MU_TPML_PCR_SELECTION_Marshal(&sel, NULL, sizeof(sel), NULL);
    assert_int_equal (rc, TSS2_MU_RC_BAD_REFERENCE);
}

/*
 * Invalid case with not big enough buffer
 */
static void
tpml_marshal_buffer_size_lt_data_nad_lt_offset(void **state)
{
    TPML_HANDLE hndl = {0};
    TPML_PCR_SELECTION sel = {0};
    uint8_t buffer[sizeof(hndl) + sizeof(sel) + 10] = { 0 };
    size_t  buffer_size = 3 * 4;
    size_t offset = 10;
    TSS2_RC rc;

    hndl.count = 2;
    hndl.handle[0] = 0x81000001;
    hndl.handle[1] = 0x81000002;

    rc = Tss2_MU_TPML_HANDLE_Marshal(&hndl, buffer, buffer_size, &offset);
    assert_int_equal (rc, TSS2_MU_RC_INSUFFICIENT_BUFFER);
    assert_int_equal (offset, 10);

    sel.count = 2;
    sel.pcrSelections[0].hash = TPM2_ALG_SHA1;
    sel.pcrSelections[0].sizeofSelect = 3;
    sel.pcrSelections[0].pcrSelect[0] = 0xaa;
    sel.pcrSelections[0].pcrSelect[1] = 0xbb;
    sel.pcrSelections[0].pcrSelect[2] = 0xcc;
    sel.pcrSelections[1].hash = TPM2_ALG_SHA256;
    sel.pcrSelections[1].sizeofSelect = 2;
    sel.pcrSelections[1].pcrSelect[0] = 0xdd;
    sel.pcrSelections[1].pcrSelect[1] = 0xee;

    offset = 2;
    buffer_size = 4 + 2 + 4 + 2 + 2;
    rc = Tss2_MU_TPML_PCR_SELECTION_Marshal(&sel, buffer, buffer_size, &offset);
    assert_int_equal (rc, TSS2_MU_RC_INSUFFICIENT_BUFFER);
    assert_int_equal (offset, 2);
}

/*
 * Invalid case with too big count
 */
static void
tpml_marshal_invalid_count(void **state)
{
    TPML_HANDLE hndl = {0};
    TPML_PCR_SELECTION sel = {0};
    uint8_t buffer[sizeof(hndl) + sizeof(sel)] = { 0 };
    size_t  buffer_size = sizeof(buffer);
    TSS2_RC rc;

    hndl.count = TPM2_MAX_CAP_HANDLES + 2;
    hndl.handle[0] = 0x81000001;
    hndl.handle[1] = 0x81000002;

    rc = Tss2_MU_TPML_HANDLE_Marshal(&hndl, buffer, buffer_size, NULL);
    assert_int_equal (rc, TSS2_SYS_RC_BAD_VALUE);

    sel.count = TPM2_NUM_PCR_BANKS + 2;
    sel.pcrSelections[0].hash = TPM2_ALG_SHA1;
    sel.pcrSelections[0].sizeofSelect = 3;
    sel.pcrSelections[0].pcrSelect[0] = 0xaa;
    sel.pcrSelections[0].pcrSelect[1] = 0xbb;
    sel.pcrSelections[0].pcrSelect[2] = 0xcc;
    sel.pcrSelections[1].hash = TPM2_ALG_SHA256;
    sel.pcrSelections[1].sizeofSelect = 2;
    sel.pcrSelections[1].pcrSelect[0] = 0xdd;
    sel.pcrSelections[1].pcrSelect[1] = 0xee;

    rc = Tss2_MU_TPML_PCR_SELECTION_Marshal(&sel, buffer, buffer_size, NULL);
    assert_int_equal (rc, TSS2_SYS_RC_BAD_VALUE);
}

/*
 * Success case
 */
static void
tpml_unmarshal_success(void **state)
{
    TPML_HANDLE hndl = {0};
    TPML_PCR_SELECTION sel = {0};
    uint8_t buffer[sizeof(hndl) + sizeof(sel) + 10] = { 0 };
    size_t  buffer_size = sizeof(buffer);
    TPML_HANDLE *ptr;
    size_t offset = 0;
    TSS2_RC rc;

    ptr = (TPML_HANDLE *) (buffer);
    ptr->count = HOST_TO_BE_32(2);
    ptr->handle[0] = HOST_TO_BE_32(0x81000001);
    ptr->handle[1] = HOST_TO_BE_32(0x81000002);

    rc = Tss2_MU_TPML_HANDLE_Unmarshal(buffer, buffer_size, &offset, &hndl);
    assert_int_equal (rc, TSS2_RC_SUCCESS);
    assert_int_equal (hndl.count, 2);
    assert_int_equal (hndl.handle[0], 0x81000001);
    assert_int_equal (hndl.handle[1], 0x81000002);
    assert_int_equal (offset, 4 + 4 + 4);

    uint8_t data [] = {
        0, 0, 0, 2,
        0, 0x04, /* TPM2_ALG_SHA1 */
        3,
        0xaa, 0xbb, 0xcc,
        0, 0x0b, /* TPM2_ALG_SHA256 */
        2,
        0xdd, 0xee};

    memcpy(buffer + 4 + 4 + 4, &data[0], sizeof(data));

    rc = Tss2_MU_TPML_PCR_SELECTION_Unmarshal(buffer, buffer_size, &offset, &sel);
    assert_int_equal (rc, TSS2_RC_SUCCESS);
    assert_int_equal (sel.count, 2);
    assert_int_equal (sel.pcrSelections[0].hash, TPM2_ALG_SHA1);
    assert_int_equal (sel.pcrSelections[0].sizeofSelect, 3);
    assert_int_equal (sel.pcrSelections[0].pcrSelect[0], 0xaa);
    assert_int_equal (sel.pcrSelections[0].pcrSelect[1], 0xbb);
    assert_int_equal (sel.pcrSelections[0].pcrSelect[2], 0xcc);
    assert_int_equal (sel.pcrSelections[1].hash, TPM2_ALG_SHA256);
    assert_int_equal (sel.pcrSelections[1].sizeofSelect, 2);
    assert_int_equal (sel.pcrSelections[1].pcrSelect[0], 0xdd);
    assert_int_equal (sel.pcrSelections[1].pcrSelect[1], 0xee);
    assert_int_equal (offset, 4 + 4 + 4 + 4 + 2 + 1 + 1 + 1 + 1 + 2 + 1 + 1 + 1);
}

/*
 * Invalid test case with buffer null and dest null
 */
static void
tpml_unmarshal_dest_null_buff_null(void **state)
{
    size_t offset = 1;
    TSS2_RC rc;

    rc = Tss2_MU_TPML_HANDLE_Unmarshal(NULL, 120, &offset, NULL);
    assert_int_equal (rc, TSS2_MU_RC_BAD_REFERENCE);
    assert_int_equal (offset, 1);

    rc = Tss2_MU_TPML_PCR_SELECTION_Unmarshal(NULL, 120, &offset, NULL);
    assert_int_equal (rc, TSS2_MU_RC_BAD_REFERENCE);
    assert_int_equal (offset, 1);
}

/*
 * Invalid test case with offset null and dest null
 */
static void
tpml_unmarshal_buffer_null_offset_null(void **state)
{
    uint8_t buffer[sizeof(TPML_HANDLE) + sizeof(TPML_PCR_SELECTION)] = { 0 };
    size_t  buffer_size = sizeof(buffer);
    TSS2_RC rc;

    rc = Tss2_MU_TPML_HANDLE_Unmarshal(buffer, buffer_size, NULL, NULL);
    assert_int_equal (rc, TSS2_MU_RC_BAD_REFERENCE);

    rc = Tss2_MU_TPML_PCR_SELECTION_Unmarshal(buffer, buffer_size, NULL, NULL);
    assert_int_equal (rc, TSS2_MU_RC_BAD_REFERENCE);
}

/*
 * Test case ensures the offset is updated when dest is NULL
 * and offset is valid
 */
static void
tpml_unmarshal_dest_null_offset_valid(void **state)
{
    uint8_t buffer[sizeof(TPML_HANDLE) + sizeof(TPML_PCR_SELECTION) + 10] = { 0 };
    size_t  buffer_size = sizeof(buffer);
    TPML_HANDLE *ptr;
    size_t offset = 0;
    TSS2_RC rc;

    ptr = (TPML_HANDLE *) (buffer);
    ptr->count = HOST_TO_BE_32(2);
    ptr->handle[0] = HOST_TO_BE_32(0x81000001);
    ptr->handle[1] = HOST_TO_BE_32(0x81000002);

    rc = Tss2_MU_TPML_HANDLE_Unmarshal(buffer, buffer_size, &offset, NULL);
    assert_int_equal (rc, TSS2_RC_SUCCESS);
    assert_int_equal (offset, 4 + 4 + 4);

    uint8_t data [] = {
        0, 0, 0, 2,
        0, 0x04, /* TPM2_ALG_SHA1 */
        3,
        0xaa, 0xbb, 0xcc,
        0, 0x0b, /* TPM2_ALG_SHA256 */
        2,
        0xdd, 0xee};

    memcpy(buffer + 4 + 4 + 4, &data[0], sizeof(data));

    rc = Tss2_MU_TPML_PCR_SELECTION_Unmarshal(buffer, buffer_size, &offset, NULL);
    assert_int_equal (rc, TSS2_RC_SUCCESS);
    assert_int_equal (offset, 4 + 4 + 4 + 4 + 2 + 1 + 1 + 1 + 1 + 2 + 1 + 1 + 1);
}

/*
 * Invalid case with not big enough buffer. Make sure offest is untouched.
 */
static void
tpml_unmarshal_buffer_size_lt_data_nad_lt_offset(void **state)
{
    uint8_t buffer[sizeof(TPML_HANDLE) + sizeof(TPML_PCR_SELECTION)] = { 0 };
    TPML_HANDLE *ptr;
    size_t offset = 2;
    TSS2_RC rc;

    ptr = (TPML_HANDLE *) (buffer + 2);
    ptr->count = HOST_TO_BE_32(2);
    ptr->handle[0] = HOST_TO_BE_32(0x81000001);
    ptr->handle[1] = HOST_TO_BE_32(0x81000002);

    rc = Tss2_MU_TPML_HANDLE_Unmarshal(buffer, 3 * 4, &offset, NULL);
    assert_int_equal (rc, TSS2_MU_RC_INSUFFICIENT_BUFFER);
    assert_int_equal (offset, 2);

    uint8_t data [] = {
        0, 0, 0, 2,
        0, 0x04, /* TPM2_ALG_SHA1 */
        3,
        0xaa, 0xbb, 0xcc,
        0, 0x0b, /* TPM2_ALG_SHA256 */
        2,
        0xdd, 0xee};

    memcpy(buffer + 2, &data[0], sizeof(data));

    rc = Tss2_MU_TPML_PCR_SELECTION_Unmarshal(buffer, 4 + 2 + 1 + 1 + 1 + 1 + 2 + 1 + 1 + 1, &offset, NULL);
    assert_int_equal (rc, TSS2_MU_RC_INSUFFICIENT_BUFFER);
    assert_int_equal (offset, 2);
}

/*
 * Invalid case with too big count
 */
static void
tpml_unmarshal_invalid_count(void **state)
{
    TPML_HANDLE hndl = {0};
    TPML_PCR_SELECTION sel = {0};
    uint8_t buffer[sizeof(hndl) + sizeof(sel) + 10] = { 0 };
    size_t  buffer_size = sizeof(buffer);
    TPML_HANDLE *ptr;
    TPML_PCR_SELECTION *ptr2;
    size_t offset = 0;
    TSS2_RC rc;

    ptr = (TPML_HANDLE *) (buffer);
    ptr->count = HOST_TO_BE_32(TPM2_MAX_CAP_HANDLES + 2);
    ptr->handle[0] = HOST_TO_BE_32(0x81000001);
    ptr->handle[1] = HOST_TO_BE_32(0x81000002);

    rc = Tss2_MU_TPML_HANDLE_Unmarshal(buffer, buffer_size, &offset, &hndl);
    assert_int_equal (rc, TSS2_SYS_RC_MALFORMED_RESPONSE);

    ptr2 = (TPML_PCR_SELECTION *)(buffer + 4 + 4 + 4);
    ptr2->count = HOST_TO_BE_32(TPM2_NUM_PCR_BANKS + 2);
    ptr2->pcrSelections[0].hash = HOST_TO_BE_16(TPM2_ALG_SHA1);
    ptr2->pcrSelections[0].sizeofSelect = 3;
    ptr2->pcrSelections[0].pcrSelect[0] = 0xaa;
    ptr2->pcrSelections[0].pcrSelect[1] = 0xbb;
    ptr2->pcrSelections[0].pcrSelect[2] = 0xcc;
    ptr2->pcrSelections[1].hash = HOST_TO_BE_16(TPM2_ALG_SHA256);
    ptr2->pcrSelections[1].sizeofSelect = 2;
    ptr2->pcrSelections[1].pcrSelect[0] = 0xdd;
    ptr2->pcrSelections[1].pcrSelect[1] = 0xee;

    rc = Tss2_MU_TPML_PCR_SELECTION_Unmarshal(buffer, buffer_size, &offset, &sel);
    assert_int_equal (rc, TSS2_SYS_RC_MALFORMED_RESPONSE);
}

#ifndef DISABLE_VENDOR
static void
tpml_intel_ptt_marshal_unmarshal(void **state)
{

    TPM2B_MAX_CAP_BUFFER buf = {
        .size = 8,
        .buffer = {
            0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x03
        }
    };

    TPML_INTEL_PTT_PROPERTY dest = { 0 };
    size_t offset = 0;

    TSS2_RC r =  Tss2_MU_TPML_INTEL_PTT_PROPERTY_Unmarshal(
        buf.buffer,
        buf.size,
        &offset,
        &dest);
    assert_int_equal(r, TSS2_RC_SUCCESS);
    assert_int_equal(dest.count, 1);
    assert_int_equal(dest.property[0], 0x3);

    TPM2B_MAX_CAP_BUFFER buf2 = { 0 };
    offset = 0;
    r = Tss2_MU_TPML_INTEL_PTT_PROPERTY_Marshal(
        &dest,
        buf2.buffer,
        sizeof(buf2.buffer),
        &offset);
        buf2.size = offset;
    assert_int_equal(r, TSS2_RC_SUCCESS);
    assert_memory_equal(&buf, &buf2, sizeof(buf));
}
#endif

int main(void) {
    const struct CMUnitTest tests[] = {
        cmocka_unit_test (tpml_marshal_success),
        cmocka_unit_test (tpml_marshal_success_offset),
        cmocka_unit_test (tpml_marshal_buffer_null_with_offset),
        cmocka_unit_test (tpml_marshal_buffer_null_offset_null),
        cmocka_unit_test (tpml_marshal_buffer_size_lt_data_nad_lt_offset),
        cmocka_unit_test (tpml_marshal_invalid_count),
        cmocka_unit_test (tpml_unmarshal_success),
        cmocka_unit_test (tpml_unmarshal_dest_null_buff_null),
        cmocka_unit_test (tpml_unmarshal_buffer_null_offset_null),
        cmocka_unit_test (tpml_unmarshal_dest_null_offset_valid),
        cmocka_unit_test (tpml_unmarshal_buffer_size_lt_data_nad_lt_offset),
        cmocka_unit_test (tpml_unmarshal_invalid_count),
#ifndef DISABLE_VENDOR
        cmocka_unit_test (tpml_intel_ptt_marshal_unmarshal)
#endif
    };
    return cmocka_run_group_tests(tests, NULL, NULL);
}
