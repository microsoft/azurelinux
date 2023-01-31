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
tpmt_marshal_success(void **state)
{
    TPMT_TK_CREATION tkt = {0};
    TPMT_PUBLIC pub = {0};
    uint8_t buffer[sizeof(tkt) + sizeof(pub)] = { 0 };
    size_t  buffer_size = sizeof(buffer);
    TPMT_TK_CREATION *ptr;
    TPMI_RH_HIERARCHY *ptr2;
    TPM2B_DIGEST *ptr3;
    TPMT_PUBLIC *ptr4;
    TPMU_PUBLIC_PARMS *ptr5;
    TSS2_RC rc;

    tkt.tag = 0xbeef;
    tkt.hierarchy = TPM2_RH_OWNER;
    tkt.digest.size = 4;
    tkt.digest.buffer[0] = 0xde;
    tkt.digest.buffer[1] = 0xad;
    tkt.digest.buffer[2] = 0xbe;
    tkt.digest.buffer[3] = 0xef;
    rc = Tss2_MU_TPMT_TK_CREATION_Marshal(&tkt, buffer, buffer_size, NULL);
    assert_int_equal (rc, TSS2_RC_SUCCESS);

    ptr = (TPMT_TK_CREATION *)buffer;
    ptr2 = (TPMI_RH_HIERARCHY *)(buffer + sizeof(tkt.tag));
    ptr3 = (TPM2B_DIGEST *)(buffer + sizeof(tkt.tag) + sizeof(tkt.hierarchy));

    assert_int_equal (ptr->tag, HOST_TO_BE_16(0xbeef));
    assert_int_equal (*ptr2, HOST_TO_BE_32(TPM2_RH_OWNER));
    assert_int_equal (ptr3->size, HOST_TO_BE_16(4));
    assert_int_equal (ptr3->buffer[0], 0xde);
    assert_int_equal (ptr3->buffer[1], 0xad);
    assert_int_equal (ptr3->buffer[2], 0xbe);
    assert_int_equal (ptr3->buffer[3], 0xef);

    pub.type = TPM2_ALG_RSA;
    pub.nameAlg = TPM2_ALG_SHA1;
    pub.parameters.symDetail.sym.algorithm = TPM2_ALG_NULL;
    pub.parameters.rsaDetail.scheme.scheme = TPM2_ALG_NULL;
    pub.parameters.rsaDetail.symmetric.algorithm = TPM2_ALG_AES;
    pub.parameters.rsaDetail.symmetric.keyBits.aes = 128;
    pub.parameters.rsaDetail.symmetric.mode.aes = TPM2_ALG_CBC;
    rc = Tss2_MU_TPMT_PUBLIC_Marshal(&pub, buffer, buffer_size, NULL);
    assert_int_equal (rc, TSS2_RC_SUCCESS);
    ptr4 = (TPMT_PUBLIC *)buffer;
    ptr5 = (TPMU_PUBLIC_PARMS *)(buffer + sizeof(TPMI_ALG_PUBLIC) + sizeof(TPMI_ALG_HASH) + sizeof(TPMA_OBJECT) + 2);
    assert_int_equal (ptr4->type, HOST_TO_BE_16(TPM2_ALG_RSA));
    assert_int_equal (ptr5->rsaDetail.symmetric.algorithm, HOST_TO_BE_16(TPM2_ALG_AES));
    assert_int_equal (ptr5->rsaDetail.symmetric.keyBits.aes, HOST_TO_BE_16(128));
    assert_int_equal (ptr5->rsaDetail.symmetric.mode.aes, HOST_TO_BE_16(TPM2_ALG_CBC));
}
/*
 * Success case with a valid offset
 */
static void
tpmt_marshal_success_offset(void **state)
{
    TPMT_TK_CREATION tkt = {0};
    TPMT_PUBLIC_PARMS pub = {0};
    uint8_t buffer[sizeof(tkt) + sizeof(pub) + 10] = { 0 };
    size_t  buffer_size = sizeof(buffer);
    TPMT_TK_CREATION *ptr;
    TPMI_RH_HIERARCHY *ptr2;
    TPM2B_DIGEST *ptr3;
    TPMT_PUBLIC_PARMS *ptr4;
    TPMS_KEYEDHASH_PARMS *ptr5;
    size_t offset = 10;
    TSS2_RC rc;

    tkt.tag = 0xbeef;
    tkt.hierarchy = TPM2_RH_OWNER;
    tkt.digest.size = 4;
    tkt.digest.buffer[0] = 0xde;
    tkt.digest.buffer[1] = 0xad;
    tkt.digest.buffer[2] = 0xbe;
    tkt.digest.buffer[3] = 0xef;
    rc = Tss2_MU_TPMT_TK_CREATION_Marshal(&tkt, buffer, buffer_size, &offset);
    assert_int_equal (rc, TSS2_RC_SUCCESS);

    ptr = (TPMT_TK_CREATION *)(buffer + 10);
    ptr2 = (TPMI_RH_HIERARCHY *)(buffer + 10 + sizeof(tkt.tag));
    ptr3 = (TPM2B_DIGEST *)(buffer + 10 + sizeof(tkt.tag) + sizeof(tkt.hierarchy));

    assert_int_equal (ptr->tag, HOST_TO_BE_16(0xbeef));
    assert_int_equal (*ptr2, HOST_TO_BE_32(TPM2_RH_OWNER));
    assert_int_equal (ptr3->size, HOST_TO_BE_16(4));
    assert_int_equal (ptr3->buffer[0], 0xde);
    assert_int_equal (ptr3->buffer[1], 0xad);
    assert_int_equal (ptr3->buffer[2], 0xbe);
    assert_int_equal (ptr3->buffer[3], 0xef);
    assert_int_equal (offset, 10 + 2 + 4 + 2 + 1 + 1 + 1 + 1);

    offset = 10;
    pub.type = TPM2_ALG_KEYEDHASH;
    pub.parameters.keyedHashDetail.scheme.scheme = TPM2_ALG_HMAC;
    pub.parameters.keyedHashDetail.scheme.details.hmac.hashAlg = TPM2_ALG_SHA256;

    rc = Tss2_MU_TPMT_PUBLIC_PARMS_Marshal(&pub, buffer, buffer_size, &offset);
    assert_int_equal (rc, TSS2_RC_SUCCESS);
    ptr4 = (TPMT_PUBLIC_PARMS *)(buffer + 10);
    ptr5 = (TPMS_KEYEDHASH_PARMS *)(buffer + 10 + 2);
    assert_int_equal (ptr4->type, HOST_TO_BE_16(TPM2_ALG_KEYEDHASH));
    assert_int_equal (ptr5->scheme.scheme, HOST_TO_BE_16(TPM2_ALG_HMAC));
    assert_int_equal (ptr5->scheme.details.hmac.hashAlg, HOST_TO_BE_16(TPM2_ALG_SHA256));
    assert_int_equal (offset, 10 + 2 + 2 + 2);
}

/*
 * Success case with a null buffer
 */
static void
tpmt_marshal_buffer_null_with_offset(void **state)
{
    TPMT_TK_CREATION tkt = {0};
    TPMT_PUBLIC_PARMS pub = {0};
    size_t  buffer_size = sizeof(tkt) + sizeof(pub) + 10;
    size_t offset = 10;
    TSS2_RC rc;

    tkt.tag = 0xbeef;
    tkt.hierarchy = TPM2_RH_OWNER;
    tkt.digest.size = 4;
    tkt.digest.buffer[0] = 0xde;
    tkt.digest.buffer[1] = 0xad;
    tkt.digest.buffer[2] = 0xbe;
    tkt.digest.buffer[3] = 0xef;
    rc = Tss2_MU_TPMT_TK_CREATION_Marshal(&tkt, NULL, buffer_size, &offset);
    assert_int_equal (rc, TSS2_RC_SUCCESS);
    assert_int_equal (offset, 10 + 2 + 4 + 2 + 1 + 1 + 1 + 1);

    offset = 10;
    pub.type = TPM2_ALG_KEYEDHASH;
    pub.parameters.keyedHashDetail.scheme.scheme = TPM2_ALG_HMAC;
    pub.parameters.keyedHashDetail.scheme.details.hmac.hashAlg = TPM2_ALG_SHA256;

    rc = Tss2_MU_TPMT_PUBLIC_PARMS_Marshal(&pub, NULL, buffer_size, &offset);
    assert_int_equal (rc, TSS2_RC_SUCCESS);
    assert_int_equal (offset, 10 + 2 + 2 + 2);
}

/*
 * Invalid case with a null buffer and a null offset
 */
static void
tpmt_marshal_buffer_null_offset_null(void **state)
{
    TPMT_TK_CREATION tkt = {0};
    TPMT_PUBLIC_PARMS pub = {0};
    TSS2_RC rc;

    rc = Tss2_MU_TPMT_TK_CREATION_Marshal(&tkt, NULL, sizeof(tkt), NULL);
    assert_int_equal (rc, TSS2_MU_RC_BAD_REFERENCE);

    rc = Tss2_MU_TPMT_PUBLIC_PARMS_Marshal(&pub, NULL, sizeof(pub), NULL);
    assert_int_equal (rc, TSS2_MU_RC_BAD_REFERENCE);
}

/*
 * Invalid case with not big enough buffer
 */
static void
tpmt_marshal_buffer_size_lt_data_nad_lt_offset(void **state)
{
    TPMT_TK_CREATION tkt = {0};
    TPMT_PUBLIC_PARMS pub = {0};
    uint8_t buffer[sizeof(tkt) + sizeof(pub) + 10] = { 0 };
    size_t offset = 10;
    TSS2_RC rc;

    tkt.tag = 0xbeef;
    tkt.hierarchy = TPM2_RH_OWNER;
    tkt.digest.size = 4;
    tkt.digest.buffer[0] = 0xde;
    tkt.digest.buffer[1] = 0xad;
    tkt.digest.buffer[2] = 0xbe;
    tkt.digest.buffer[3] = 0xef;
    rc = Tss2_MU_TPMT_TK_CREATION_Marshal(&tkt, buffer, 10, &offset);
    assert_int_equal (rc, TSS2_MU_RC_INSUFFICIENT_BUFFER);
    assert_int_equal (offset, 10);

    pub.type = TPM2_ALG_KEYEDHASH;
    pub.parameters.keyedHashDetail.scheme.scheme = TPM2_ALG_HMAC;
    pub.parameters.keyedHashDetail.scheme.details.hmac.hashAlg = TPM2_ALG_SHA256;

    rc = Tss2_MU_TPMT_PUBLIC_PARMS_Marshal(&pub, buffer, 8, &offset);
    assert_int_equal (rc, TSS2_MU_RC_INSUFFICIENT_BUFFER);
    assert_int_equal (offset, 10);
}

/*
 * Success case
 */
static void
tpmt_unmarshal_success(void **state)
{
    TPMT_TK_CREATION tkt = {0};
    TPMT_PUBLIC_PARMS pub = {0};
    uint8_t buffer[sizeof(tkt) + sizeof(pub)] = { 0 };
    size_t  buffer_size = sizeof(buffer);
    TPMT_TK_CREATION *ptr;
    TPMI_RH_HIERARCHY *ptr2;
    TPM2B_DIGEST *ptr3;
    TPMT_PUBLIC_PARMS *ptr4;
    TPMS_KEYEDHASH_PARMS *ptr5;
    size_t offset = 0;
    TSS2_RC rc;

    ptr = (TPMT_TK_CREATION *)(buffer);
    ptr2 = (TPMI_RH_HIERARCHY *)(buffer + sizeof(tkt.tag));
    ptr3 = (TPM2B_DIGEST *)(buffer + sizeof(tkt.tag) + sizeof(tkt.hierarchy));

    ptr->tag = HOST_TO_BE_16(0xbeef);
    *ptr2 = HOST_TO_BE_32(TPM2_RH_OWNER);
    ptr3->size = HOST_TO_BE_16(4);
    ptr3->buffer[0] = 0xde;
    ptr3->buffer[1] = 0xad;
    ptr3->buffer[2] = 0xbe;
    ptr3->buffer[3] = 0xef;

    rc = Tss2_MU_TPMT_TK_CREATION_Unmarshal(buffer, buffer_size, &offset, &tkt);
    assert_int_equal (rc, TSS2_RC_SUCCESS);
    assert_int_equal (tkt.tag, 0xbeef);
    assert_int_equal (tkt.hierarchy, TPM2_RH_OWNER);
    assert_int_equal (tkt.digest.size, 4);
    assert_int_equal (tkt.digest.buffer[0], 0xde);
    assert_int_equal (tkt.digest.buffer[1], 0xad);
    assert_int_equal (tkt.digest.buffer[2], 0xbe);
    assert_int_equal (tkt.digest.buffer[3], 0xef);
    assert_int_equal (offset, 2 + 4 + 2 + 1 + 1 + 1 + 1);

    offset = 0;
    ptr4 = (TPMT_PUBLIC_PARMS *)(buffer);
    ptr5 = (TPMS_KEYEDHASH_PARMS *)(buffer + 2);
    ptr4->type = HOST_TO_BE_16(TPM2_ALG_KEYEDHASH);
    ptr5->scheme.scheme = HOST_TO_BE_16(TPM2_ALG_HMAC);
    ptr5->scheme.details.hmac.hashAlg = HOST_TO_BE_16(TPM2_ALG_SHA256);

    rc = Tss2_MU_TPMT_PUBLIC_PARMS_Unmarshal(buffer, buffer_size, &offset, &pub);
    assert_int_equal (rc, TSS2_RC_SUCCESS);
    assert_int_equal (pub.type, TPM2_ALG_KEYEDHASH);
    assert_int_equal (pub.parameters.keyedHashDetail.scheme.scheme, TPM2_ALG_HMAC);
    assert_int_equal (pub.parameters.keyedHashDetail.scheme.details.hmac.hashAlg, TPM2_ALG_SHA256);
    assert_int_equal (offset, 2 + 2 + 2);
}

/*
 * Invalid test case with buffer null and dest null
 */
static void
tpmt_unmarshal_dest_null_buff_null(void **state)
{
    size_t offset = 1;
    TSS2_RC rc;

    rc = Tss2_MU_TPMT_TK_CREATION_Unmarshal(NULL, 120, &offset, NULL);
    assert_int_equal (rc, TSS2_MU_RC_BAD_REFERENCE);
    assert_int_equal (offset, 1);

    rc = Tss2_MU_TPMT_PUBLIC_PARMS_Unmarshal(NULL, 120, &offset, NULL);
    assert_int_equal (rc, TSS2_MU_RC_BAD_REFERENCE);
    assert_int_equal (offset, 1);
}

/*
 * Invalid test case with offset null and dest null
 */
static void
tpmt_unmarshal_buffer_null_offset_null(void **state)
{
    uint8_t buffer[sizeof(TPMT_TK_CREATION) + sizeof(TPMT_PUBLIC_PARMS)] = { 0 };
    size_t  buffer_size = sizeof(buffer);
    TSS2_RC rc;

    rc = Tss2_MU_TPMT_TK_CREATION_Unmarshal(buffer, buffer_size, NULL, NULL);
    assert_int_equal (rc, TSS2_MU_RC_BAD_REFERENCE);

    rc = Tss2_MU_TPMT_PUBLIC_PARMS_Unmarshal(buffer, buffer_size, NULL, NULL);
    assert_int_equal (rc, TSS2_MU_RC_BAD_REFERENCE);
}

/*
 * Test case ensures the offset is updated when dest is NULL
 * and offset is valid
 */
static void
tpmt_unmarshal_dest_null_offset_valid(void **state)
{
    TPMT_TK_CREATION tkt;
    uint8_t buffer[sizeof(tkt) + sizeof(TPMT_PUBLIC_PARMS)] = { 0 };
    size_t  buffer_size = sizeof(buffer);
    TPMT_TK_CREATION *ptr;
    TPMI_RH_HIERARCHY *ptr2;
    TPM2B_DIGEST *ptr3;
    TPMT_PUBLIC_PARMS *ptr4;
    TPMS_KEYEDHASH_PARMS *ptr5;
    size_t offset = 0;
    TSS2_RC rc;

    ptr = (TPMT_TK_CREATION *)(buffer);
    ptr2 = (TPMI_RH_HIERARCHY *)(buffer + sizeof(tkt.tag));
    ptr3 = (TPM2B_DIGEST *)(buffer + sizeof(tkt.tag) + sizeof(tkt.hierarchy));

    ptr->tag = HOST_TO_BE_16(0xbeef);
    *ptr2 = HOST_TO_BE_32(TPM2_RH_OWNER);
    ptr3->size = HOST_TO_BE_16(4);
    ptr3->buffer[0] = 0xde;
    ptr3->buffer[1] = 0xad;
    ptr3->buffer[2] = 0xbe;
    ptr3->buffer[3] = 0xef;

    rc = Tss2_MU_TPMT_TK_CREATION_Unmarshal(buffer, buffer_size, &offset, NULL);
    assert_int_equal (rc, TSS2_RC_SUCCESS);
    assert_int_equal (offset, 2 + 4 + 2 + 1 + 1 + 1 + 1);

    offset = 0;
    ptr4 = (TPMT_PUBLIC_PARMS *)(buffer);
    ptr5 = (TPMS_KEYEDHASH_PARMS *)(buffer + 2);
    ptr4->type = HOST_TO_BE_16(TPM2_ALG_KEYEDHASH);
    ptr5->scheme.scheme = HOST_TO_BE_16(TPM2_ALG_HMAC);
    ptr5->scheme.details.hmac.hashAlg = HOST_TO_BE_16(TPM2_ALG_SHA256);

    rc = Tss2_MU_TPMT_PUBLIC_PARMS_Unmarshal(buffer, buffer_size, &offset, NULL);
    assert_int_equal (rc, TSS2_RC_SUCCESS);
    assert_int_equal (offset, 2 + 2 + 2);
}

/*
 * Invalid case with not big enough buffer. Make sure offest is untouched.
 */
static void
tpmt_unmarshal_buffer_size_lt_data_nad_lt_offset(void **state)
{
    TPMT_TK_CREATION tkt;
    uint8_t buffer[sizeof(tkt) + sizeof(TPMT_PUBLIC_PARMS)] = { 0 };
    TPMT_TK_CREATION *ptr;
    TPMI_RH_HIERARCHY *ptr2;
    TPM2B_DIGEST *ptr3;
    TPMT_PUBLIC_PARMS *ptr4;
    TPMS_KEYEDHASH_PARMS *ptr5;
    size_t offset = 5;
    TSS2_RC rc;

    ptr = (TPMT_TK_CREATION *)(buffer);
    ptr2 = (TPMI_RH_HIERARCHY *)(buffer + sizeof(tkt.tag));
    ptr3 = (TPM2B_DIGEST *)(buffer + sizeof(tkt.tag) + sizeof(tkt.hierarchy));

    ptr->tag = HOST_TO_BE_16(0xbeef);
    *ptr2 = HOST_TO_BE_32(TPM2_RH_OWNER);
    ptr3->size = HOST_TO_BE_16(4);
    ptr3->buffer[0] = 0xde;
    ptr3->buffer[1] = 0xad;
    ptr3->buffer[2] = 0xbe;
    ptr3->buffer[3] = 0xef;
    rc = Tss2_MU_TPMT_TK_CREATION_Unmarshal(buffer, 15, &offset, NULL);
    assert_int_equal (rc, TSS2_MU_RC_INSUFFICIENT_BUFFER);
    assert_int_equal (offset, 5);

    offset = 5;
    ptr4 = (TPMT_PUBLIC_PARMS *)(buffer);
    ptr5 = (TPMS_KEYEDHASH_PARMS *)(buffer + 2);
    ptr4->type = HOST_TO_BE_16(TPM2_ALG_KEYEDHASH);
    ptr5->scheme.scheme = HOST_TO_BE_16(TPM2_ALG_HMAC);
    ptr5->scheme.details.hmac.hashAlg = HOST_TO_BE_16(TPM2_ALG_SHA256);

    rc = Tss2_MU_TPMT_PUBLIC_PARMS_Unmarshal(buffer, 6, &offset, NULL);
    assert_int_equal (rc, TSS2_MU_RC_INSUFFICIENT_BUFFER);
    assert_int_equal (offset, 5);
}

static void
tpmt_marshal_unmarshal_sig_invalid_selector(void **state)
{
    TPMT_SIGNATURE sig = {0};
    uint8_t buf[256] = {0};
    size_t size = 256, offset = 0;
    TPM2_ALG_ID invalid_id = HOST_TO_BE_16(0xbeef);
    TPM2_RC rc;

    sig.sigAlg = invalid_id;

    /* Marshal with invalid selector case */
    rc = Tss2_MU_TPMT_SIGNATURE_Marshal(&sig, buf, sizeof(sig), &offset);
    assert_int_equal (rc, TSS2_MU_RC_BAD_VALUE);
    assert_int_equal (offset, 0);

    /* Unarshal with invalid selector case */
    rc = Tss2_MU_TPMT_SIGNATURE_Unmarshal(buf, size, &offset, &sig);
    assert_int_equal (rc, TSS2_MU_RC_BAD_VALUE);
    assert_int_equal (offset, 0);
}

int main(void) {
    const struct CMUnitTest tests[] = {
        cmocka_unit_test (tpmt_marshal_success),
        cmocka_unit_test (tpmt_marshal_success_offset),
        cmocka_unit_test (tpmt_marshal_buffer_null_with_offset),
        cmocka_unit_test (tpmt_marshal_buffer_null_offset_null),
        cmocka_unit_test (tpmt_marshal_buffer_size_lt_data_nad_lt_offset),
        cmocka_unit_test (tpmt_marshal_unmarshal_sig_invalid_selector),
        cmocka_unit_test (tpmt_unmarshal_success),
        cmocka_unit_test (tpmt_unmarshal_dest_null_buff_null),
        cmocka_unit_test (tpmt_unmarshal_buffer_null_offset_null),
        cmocka_unit_test (tpmt_unmarshal_dest_null_offset_valid),
        cmocka_unit_test (tpmt_unmarshal_buffer_size_lt_data_nad_lt_offset),
    };
    return cmocka_run_group_tests(tests, NULL, NULL);
}
