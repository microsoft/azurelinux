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
tpms_marshal_success(void **state)
{
    TPMS_ALG_PROPERTY alg = {0};
    TPMS_CAPABILITY_DATA cap = {0};
    uint8_t buffer[sizeof(alg)] = { 0 };
    size_t  buffer_size = sizeof(buffer);
    uint8_t buffer2[sizeof(cap)] = { 0 };
    size_t  buffer_size2 = sizeof(buffer2);
    uint16_t *alg_ptr;
    uint32_t *alg_properties_ptr;
    TPMS_CAPABILITY_DATA *ptr2;
    uint16_t alg_expected = HOST_TO_BE_16(TPM2_ALG_ECDSA);
    uint32_t algprop_expected = HOST_TO_BE_32(TPMA_ALGORITHM_ASYMMETRIC | TPMA_ALGORITHM_SIGNING);
    uint32_t capability = HOST_TO_BE_32(TPM2_CAP_ECC_CURVES);
    TSS2_RC rc;

    alg.alg = TPM2_ALG_ECDSA;
    alg.algProperties |= TPMA_ALGORITHM_ASYMMETRIC;
    alg.algProperties |= TPMA_ALGORITHM_SIGNING;
    alg_ptr = (uint16_t *)buffer;
    alg_properties_ptr = (uint32_t *)(buffer + sizeof(uint16_t));
    rc = Tss2_MU_TPMS_ALG_PROPERTY_Marshal(&alg, buffer, buffer_size, NULL);
    assert_int_equal (rc, TSS2_RC_SUCCESS);
    assert_int_equal (*alg_ptr, alg_expected);
    assert_int_equal (*alg_properties_ptr, algprop_expected);

    cap.capability = TPM2_CAP_ECC_CURVES;
    cap.data.eccCurves.count = 3;
    cap.data.eccCurves.eccCurves[0] = TPM2_ECC_NIST_P256;
    cap.data.eccCurves.eccCurves[1] = TPM2_ECC_NIST_P384;
    cap.data.eccCurves.eccCurves[2] = TPM2_ECC_NIST_P521;
    ptr2 = (TPMS_CAPABILITY_DATA *)buffer2;

    rc = Tss2_MU_TPMS_CAPABILITY_DATA_Marshal(&cap, buffer2, buffer_size2, NULL);
    assert_int_equal (rc, TSS2_RC_SUCCESS);
    assert_int_equal (ptr2->capability, capability);
    assert_int_equal (ptr2->data.eccCurves.count, HOST_TO_BE_32(3));
    assert_int_equal (ptr2->data.eccCurves.eccCurves[0], HOST_TO_BE_16(TPM2_ECC_NIST_P256));
    assert_int_equal (ptr2->data.eccCurves.eccCurves[1], HOST_TO_BE_16(TPM2_ECC_NIST_P384));
    assert_int_equal (ptr2->data.eccCurves.eccCurves[2], HOST_TO_BE_16(TPM2_ECC_NIST_P521));
}

/*
 * Success case with a valid offset
 */
static void
tpms_marshal_success_offset(void **state)
{
    TPMS_ALG_PROPERTY alg = {0};
    TPMS_CAPABILITY_DATA cap = {0};
    uint8_t buffer[sizeof(alg) + sizeof(cap) + 10] = { 0 };
    size_t  buffer_size = sizeof(buffer);
    uint16_t *alg_ptr;
    uint32_t *alg_properties_ptr;
    TPMS_CAPABILITY_DATA *ptr2;
    uint16_t alg_expected = HOST_TO_BE_16(TPM2_ALG_ECDSA);
    uint32_t algprop_expected = HOST_TO_BE_32(TPMA_ALGORITHM_ASYMMETRIC | TPMA_ALGORITHM_SIGNING);
    uint32_t capability = HOST_TO_BE_32(TPM2_CAP_ECC_CURVES);
    size_t offset = 10;
    TSS2_RC rc;

    alg.alg = TPM2_ALG_ECDSA;
    alg.algProperties |= TPMA_ALGORITHM_ASYMMETRIC;
    alg.algProperties |= TPMA_ALGORITHM_SIGNING;
    alg_ptr = (uint16_t *)(buffer + 10);
    alg_properties_ptr = (uint32_t *)(buffer + sizeof(*alg_ptr) + 10);

    rc = Tss2_MU_TPMS_ALG_PROPERTY_Marshal(&alg, buffer, buffer_size, &offset);
    assert_int_equal (rc, TSS2_RC_SUCCESS);
    assert_int_equal (*alg_ptr, alg_expected);
    assert_int_equal (*alg_properties_ptr, algprop_expected);

    cap.capability = TPM2_CAP_ECC_CURVES;
    cap.data.eccCurves.count = 3;
    cap.data.eccCurves.eccCurves[0] = TPM2_ECC_NIST_P256;
    cap.data.eccCurves.eccCurves[1] = TPM2_ECC_NIST_P384;
    cap.data.eccCurves.eccCurves[2] = TPM2_ECC_NIST_P521;
    ptr2 = (TPMS_CAPABILITY_DATA *)(buffer + 10 + sizeof(*alg_ptr) + sizeof(*alg_properties_ptr));

    rc = Tss2_MU_TPMS_CAPABILITY_DATA_Marshal(&cap, buffer, buffer_size, &offset);
    assert_int_equal (rc, TSS2_RC_SUCCESS);
    assert_int_equal (ptr2->capability, capability);
    assert_int_equal (ptr2->data.eccCurves.count, HOST_TO_BE_32(3));
    assert_int_equal (ptr2->data.eccCurves.eccCurves[0], HOST_TO_BE_16(TPM2_ECC_NIST_P256));
    assert_int_equal (ptr2->data.eccCurves.eccCurves[1], HOST_TO_BE_16(TPM2_ECC_NIST_P384));
    assert_int_equal (ptr2->data.eccCurves.eccCurves[2], HOST_TO_BE_16(TPM2_ECC_NIST_P521));
    assert_int_equal (offset, 10 + sizeof(*alg_ptr) + sizeof(*alg_properties_ptr) + sizeof(capability) + 4 + (3 * 2));
}

/*
 * Success case with a null buffer
 */
static void
tpms_marshal_buffer_null_with_offset(void **state)
{
    TPMS_ALG_PROPERTY alg = {0};
    TPMS_CAPABILITY_DATA cap = {0};
    uint16_t *alg_ptr;
    uint32_t *alg_properties_ptr;
    size_t offset = 100;
    TSS2_RC rc;

    alg.alg = TPM2_ALG_ECDSA;
    alg.algProperties |= TPMA_ALGORITHM_ASYMMETRIC;
    alg.algProperties |= TPMA_ALGORITHM_SIGNING;

    rc = Tss2_MU_TPMS_ALG_PROPERTY_Marshal(&alg, NULL, sizeof(alg), &offset);
    assert_int_equal (rc, TSS2_RC_SUCCESS);
    assert_int_equal (offset, 100 + sizeof(*alg_ptr) + sizeof(*alg_properties_ptr));

    cap.capability = TPM2_CAP_ECC_CURVES;
    cap.data.eccCurves.count = 3;
    cap.data.eccCurves.eccCurves[0] = TPM2_ECC_NIST_P256;
    cap.data.eccCurves.eccCurves[1] = TPM2_ECC_NIST_P384;
    cap.data.eccCurves.eccCurves[2] = TPM2_ECC_NIST_P521;

    rc = Tss2_MU_TPMS_CAPABILITY_DATA_Marshal(&cap, NULL, sizeof(cap), &offset);
    assert_int_equal (rc, TSS2_RC_SUCCESS);
    assert_int_equal (offset, 100 + sizeof(*alg_ptr) + sizeof(*alg_properties_ptr) + 4 + 4 + (3 * 2));
}

/*
 * Invalid case with a null buffer and a null offset
 */
static void
tpms_marshal_buffer_null_offset_null(void **state)
{
    TPMS_ALG_PROPERTY alg = {0};
    TPMS_CAPABILITY_DATA cap = {0};
    TSS2_RC rc;

    rc = Tss2_MU_TPMS_ALG_PROPERTY_Marshal(&alg, NULL, sizeof(alg), NULL);
    assert_int_equal (rc, TSS2_MU_RC_BAD_REFERENCE);

    rc = Tss2_MU_TPMS_CAPABILITY_DATA_Marshal(&cap, NULL, sizeof(cap), NULL);
    assert_int_equal (rc, TSS2_MU_RC_BAD_REFERENCE);
}

/*
 * Invalid case with not big enough buffer
 */
static void
tpms_marshal_buffer_size_lt_data_nad_lt_offset(void **state)
{
    TPMS_ALG_PROPERTY alg = {0};
    TPMS_CAPABILITY_DATA cap = {0};
    uint8_t buffer[sizeof(alg) + sizeof(cap)] = { 0 };
    size_t  buffer_size = sizeof(alg);
    size_t offset = 10;
    TSS2_RC rc;

    alg.alg = TPM2_ALG_ECDSA;
    alg.algProperties |= TPMA_ALGORITHM_ASYMMETRIC;
    alg.algProperties |= TPMA_ALGORITHM_SIGNING;
    rc = Tss2_MU_TPMS_ALG_PROPERTY_Marshal(&alg, buffer, buffer_size, &offset);
    assert_int_equal (rc, TSS2_MU_RC_INSUFFICIENT_BUFFER);
    assert_int_equal (offset, 10);

    buffer_size = 4;
    offset = 2;
    cap.capability = TPM2_CAP_ECC_CURVES;
    cap.data.eccCurves.count = 3;
    cap.data.eccCurves.eccCurves[0] = TPM2_ECC_NIST_P256;
    cap.data.eccCurves.eccCurves[1] = TPM2_ECC_NIST_P384;
    cap.data.eccCurves.eccCurves[2] = TPM2_ECC_NIST_P521;
    rc = Tss2_MU_TPMS_CAPABILITY_DATA_Marshal(&cap, buffer, buffer_size, &offset);
    assert_int_equal (rc, TSS2_MU_RC_INSUFFICIENT_BUFFER);
    assert_int_equal (offset, 2);
}

/*
 * Success case
 */
static void
tpms_unmarshal_success(void **state)
{
    TPMS_ALG_PROPERTY alg = {0};
    TPMS_CAPABILITY_DATA cap = {0};
    uint8_t buffer[sizeof(alg) + sizeof(cap)] = { 0 };
    size_t  buffer_size = sizeof(buffer);
    uint16_t *alg_ptr;
    uint32_t *alg_properties_ptr;
    TPMS_CAPABILITY_DATA *ptr2;
    uint16_t alg_expected = TPM2_ALG_ECDSA;
    uint32_t algprop_expected = TPMA_ALGORITHM_ASYMMETRIC | TPMA_ALGORITHM_SIGNING;
    uint32_t capability = TPM2_CAP_ECC_CURVES;
    size_t offset = 0;
    TSS2_RC rc;

    alg_ptr = (uint16_t *) buffer;
    *alg_ptr = HOST_TO_BE_16(TPM2_ALG_ECDSA);
    alg_properties_ptr = (uint32_t *) (buffer + sizeof(*alg_ptr));
    *alg_properties_ptr = HOST_TO_BE_32(TPMA_ALGORITHM_ASYMMETRIC | TPMA_ALGORITHM_SIGNING);

    rc = Tss2_MU_TPMS_ALG_PROPERTY_Unmarshal(buffer, buffer_size, &offset, &alg);
    assert_int_equal (rc, TSS2_RC_SUCCESS);
    assert_int_equal (alg.alg, alg_expected);
    assert_int_equal (alg.algProperties, algprop_expected);

    ptr2 = (TPMS_CAPABILITY_DATA *)(buffer + sizeof(alg));
    ptr2->capability = HOST_TO_BE_32(TPM2_CAP_ECC_CURVES);
    ptr2->data.eccCurves.count = HOST_TO_BE_32(3);
    ptr2->data.eccCurves.eccCurves[0] = HOST_TO_BE_16(TPM2_ECC_NIST_P256);
    ptr2->data.eccCurves.eccCurves[1] = HOST_TO_BE_16(TPM2_ECC_NIST_P384);
    ptr2->data.eccCurves.eccCurves[2] = HOST_TO_BE_16(TPM2_ECC_NIST_P521);

    offset = sizeof(alg);
    rc = Tss2_MU_TPMS_CAPABILITY_DATA_Unmarshal(buffer, buffer_size, &offset, &cap);
    assert_int_equal (rc, TSS2_RC_SUCCESS);
    assert_int_equal (cap.capability, capability);
    assert_int_equal (cap.data.eccCurves.count, 3);
    assert_int_equal (cap.data.eccCurves.eccCurves[0], TPM2_ECC_NIST_P256);
    assert_int_equal (cap.data.eccCurves.eccCurves[1], TPM2_ECC_NIST_P384);
    assert_int_equal (cap.data.eccCurves.eccCurves[2], TPM2_ECC_NIST_P521);
    assert_int_equal (offset, sizeof(alg) + sizeof(capability) + 4 + (3 * 2));
}

/*
 * Invalid test case with buffer null and dest null
 */
static void
tpms_unmarshal_dest_null_buff_null(void **state)
{
    size_t offset = 1;
    TSS2_RC rc;

    rc = Tss2_MU_TPMS_ALG_PROPERTY_Unmarshal(NULL, 120, &offset, NULL);
    assert_int_equal (rc, TSS2_MU_RC_BAD_REFERENCE);
    assert_int_equal (offset, 1);

    rc = Tss2_MU_TPMS_CAPABILITY_DATA_Unmarshal(NULL, 120, &offset, NULL);
    assert_int_equal (rc, TSS2_MU_RC_BAD_REFERENCE);
    assert_int_equal (offset, 1);
}

/*
 * Invalid test case with offset null and dest null
 */
static void
tpms_unmarshal_buffer_null_offset_null(void **state)
{
    uint8_t buffer[sizeof(TPMS_ALG_PROPERTY) + sizeof(TPMS_CAPABILITY_DATA)] = { 0 };
    size_t  buffer_size = sizeof(buffer);
    TSS2_RC rc;

    rc = Tss2_MU_TPMS_ALG_PROPERTY_Unmarshal(buffer, buffer_size, NULL, NULL);
    assert_int_equal (rc, TSS2_MU_RC_BAD_REFERENCE);

    rc = Tss2_MU_TPMS_CAPABILITY_DATA_Unmarshal(buffer, buffer_size, NULL, NULL);
    assert_int_equal (rc, TSS2_MU_RC_BAD_REFERENCE);
}

/*
 * Test case ensures the offset is updated when dest is NULL
 * and offset is valid
 */
static void
tpms_unmarshal_dest_null_offset_valid(void **state)
{
    uint8_t buffer[sizeof(TPMS_ALG_PROPERTY) + sizeof(TPMS_CAPABILITY_DATA)] = { 0 };
    size_t  buffer_size = sizeof(buffer);
    uint16_t *alg_ptr;
    uint32_t *alg_properties_ptr;
    TPMS_CAPABILITY_DATA *ptr2;
    size_t offset = 0;
    TSS2_RC rc;

    alg_ptr = (uint16_t *) buffer;
    *alg_ptr = HOST_TO_BE_16(TPM2_ALG_ECDSA);
    alg_properties_ptr = (uint32_t *) (buffer + sizeof(*alg_ptr));
    *alg_properties_ptr = HOST_TO_BE_32(TPMA_ALGORITHM_ASYMMETRIC | TPMA_ALGORITHM_SIGNING);

    rc = Tss2_MU_TPMS_ALG_PROPERTY_Unmarshal(buffer, buffer_size, &offset, NULL);
    assert_int_equal (rc, TSS2_RC_SUCCESS);
    assert_int_equal (offset, sizeof(*alg_ptr) + sizeof(*alg_properties_ptr));

    ptr2 = (TPMS_CAPABILITY_DATA *)(buffer + sizeof(TPMS_ALG_PROPERTY));
    ptr2->capability = HOST_TO_BE_32(TPM2_CAP_ECC_CURVES);
    ptr2->data.eccCurves.count = HOST_TO_BE_32(3);
    ptr2->data.eccCurves.eccCurves[0] = HOST_TO_BE_16(TPM2_ECC_NIST_P256);
    ptr2->data.eccCurves.eccCurves[1] = HOST_TO_BE_16(TPM2_ECC_NIST_P384);
    ptr2->data.eccCurves.eccCurves[2] = HOST_TO_BE_16(TPM2_ECC_NIST_P521);

    offset = sizeof(TPMS_ALG_PROPERTY);
    rc = Tss2_MU_TPMS_CAPABILITY_DATA_Unmarshal(buffer, buffer_size, &offset, NULL);
    assert_int_equal (rc, TSS2_RC_SUCCESS);
    assert_int_equal (offset, sizeof(TPMS_ALG_PROPERTY) + 4 + 4 + (3 * 2));
}

/*
 * Invalid case with not big enough buffer. Make sure offest is untouched.
 */
static void
tpms_unmarshal_buffer_size_lt_data_nad_lt_offset(void **state)
{
    TPMS_ALG_PROPERTY alg = {0};
    TPMS_CAPABILITY_DATA cap = {0};
    uint8_t buffer[sizeof(alg) + sizeof(cap) + 3] = { 0 };
    TPMS_ALG_PROPERTY *ptr;
    TPMS_CAPABILITY_DATA *ptr2;
    size_t offset = 3;
    TSS2_RC rc;

    ptr = (TPMS_ALG_PROPERTY *) buffer;
    ptr->alg = HOST_TO_BE_16(TPM2_ALG_ECDSA);
    ptr->algProperties = HOST_TO_BE_32(TPMA_ALGORITHM_ASYMMETRIC | TPMA_ALGORITHM_SIGNING);
    rc = Tss2_MU_TPMS_ALG_PROPERTY_Unmarshal(buffer, sizeof(alg), &offset, &alg);
    assert_int_equal (rc, TSS2_MU_RC_INSUFFICIENT_BUFFER);
    assert_int_equal (offset, 3);

    offset = sizeof(alg);
    ptr2 = (TPMS_CAPABILITY_DATA *)(buffer + sizeof(alg) + 3);
    ptr2->capability = HOST_TO_BE_32(TPM2_CAP_ECC_CURVES);
    ptr2->data.eccCurves.count = HOST_TO_BE_32(3);
    ptr2->data.eccCurves.eccCurves[0] = HOST_TO_BE_16(TPM2_ECC_NIST_P256);
    ptr2->data.eccCurves.eccCurves[1] = HOST_TO_BE_16(TPM2_ECC_NIST_P384);
    ptr2->data.eccCurves.eccCurves[2] = HOST_TO_BE_16(TPM2_ECC_NIST_P521);
    rc = Tss2_MU_TPMS_CAPABILITY_DATA_Unmarshal(buffer, 14, &offset, &cap);
    assert_int_equal (rc, TSS2_MU_RC_INSUFFICIENT_BUFFER);
    assert_int_equal (offset, sizeof(alg));
}

static void
tpms_capability_data_intel_ptt_marshal_unmarshal(void **state)
{
    uint8_t const buf[] = {
        /* TPMS_CAPABILITY_DATA */
        0x00, 0x00, 0x01, 0x00, /* capability */
        /* TPMU_CAPABILITY_DATA */
        0x00, 0x08,             /* UINT16 size */
        0x00, 0x00, 0x00, 0x01, /* property */
        0x00, 0x00, 0x00, 0x03  /* value */
    };

    TPMS_CAPABILITY_DATA dest;

    size_t offset = 0;
    TSS2_RC rc = Tss2_MU_TPMS_CAPABILITY_DATA_Unmarshal(
        buf,
        sizeof(buf),
        &offset,
        &dest);
    assert_int_equal(rc, TSS2_RC_SUCCESS);
    assert_int_equal(dest.capability, TPM2_CAP_VENDOR_PROPERTY);
    assert_int_equal(dest.data.vendor.size, 8);
    assert_memory_equal(dest.data.vendor.buffer, &buf[6], dest.data.vendor.size);

    uint8_t buf2[sizeof(buf)] = {0};
    offset = 0;
    rc = Tss2_MU_TPMS_CAPABILITY_DATA_Marshal(
            &dest,
            buf2,
            sizeof(buf2),
            &offset);
    assert_int_equal(rc, TSS2_RC_SUCCESS);
    assert_memory_equal(buf, buf2, sizeof(buf2));
}

int main(void) {
    const struct CMUnitTest tests[] = {
        cmocka_unit_test (tpms_marshal_success),
        cmocka_unit_test (tpms_marshal_success_offset),
        cmocka_unit_test (tpms_marshal_buffer_null_with_offset),
        cmocka_unit_test (tpms_marshal_buffer_null_offset_null),
        cmocka_unit_test (tpms_marshal_buffer_size_lt_data_nad_lt_offset),
        cmocka_unit_test (tpms_unmarshal_success),
        cmocka_unit_test (tpms_unmarshal_dest_null_buff_null),
        cmocka_unit_test (tpms_unmarshal_buffer_null_offset_null),
        cmocka_unit_test (tpms_unmarshal_dest_null_offset_valid),
        cmocka_unit_test (tpms_unmarshal_buffer_size_lt_data_nad_lt_offset),
        cmocka_unit_test (tpms_capability_data_intel_ptt_marshal_unmarshal)
    };
    return cmocka_run_group_tests(tests, NULL, NULL);
}
