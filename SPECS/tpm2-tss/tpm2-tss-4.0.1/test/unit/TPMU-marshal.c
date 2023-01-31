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
tpmu_marshal_success(void **state)
{
    TPMU_HA ha = {0};
    TPMU_SIGNATURE sig = {0};
    uint8_t buffer[sizeof(ha) + sizeof(sig)] = { 0 };
    size_t  buffer_size = sizeof(buffer);
    TPMS_SIGNATURE_ECDSA *ptr;
    TPM2B_ECC_PARAMETER *ptr2;
    TSS2_RC rc;

    memset(ha.sha512, 'a', TPM2_SHA512_DIGEST_SIZE);
    rc = Tss2_MU_TPMU_HA_Marshal(&ha, TPM2_ALG_SHA512, buffer, buffer_size, NULL);
    assert_int_equal (rc, TSS2_RC_SUCCESS);
    assert_int_equal (memcmp(buffer, ha.sha512, TPM2_SHA512_DIGEST_SIZE), 0);

    sig.ecdsa.hash = TPM2_ALG_SHA1;
    sig.ecdsa.signatureR.size = 4;
    sig.ecdsa.signatureR.buffer[0] = 'a';
    sig.ecdsa.signatureR.buffer[1] = 'b';
    sig.ecdsa.signatureR.buffer[2] = 'c';
    sig.ecdsa.signatureR.buffer[3] = 'd';
    sig.ecdsa.signatureS.size = 4;
    sig.ecdsa.signatureS.buffer[0] = 'e';
    sig.ecdsa.signatureS.buffer[1] = 'd';
    sig.ecdsa.signatureS.buffer[2] = 'f';
    sig.ecdsa.signatureS.buffer[3] = 'g';

    rc = Tss2_MU_TPMU_SIGNATURE_Marshal(&sig, TPM2_ALG_ECDSA, buffer, buffer_size, NULL);
    assert_int_equal (rc, TSS2_RC_SUCCESS);
    ptr = (TPMS_SIGNATURE_ECDSA *) buffer;
    assert_int_equal (ptr->hash, HOST_TO_BE_16(TPM2_ALG_SHA1));
    assert_int_equal (ptr->signatureR.size, HOST_TO_BE_16(4));
    assert_int_equal (ptr->signatureR.buffer[0], 'a');
    assert_int_equal (ptr->signatureR.buffer[1], 'b');
    assert_int_equal (ptr->signatureR.buffer[2], 'c');
    assert_int_equal (ptr->signatureR.buffer[3], 'd');
    ptr2 = (TPM2B_ECC_PARAMETER *) (buffer + 8);
    assert_int_equal (ptr2->size, HOST_TO_BE_16(4));
    assert_int_equal (ptr2->buffer[0], 'e');
    assert_int_equal (ptr2->buffer[1], 'd');
    assert_int_equal (ptr2->buffer[2], 'f');
    assert_int_equal (ptr2->buffer[3], 'g');

}
/*
 * Success case with a valid offset
 */
static void
tpmu_marshal_success_offset(void **state)
{
    TPMU_HA ha = {0};
    TPMU_SIGNATURE sig = {0};
    uint8_t buffer[sizeof(ha) + sizeof(sig) + 10] = { 0 };
    size_t  buffer_size = sizeof(buffer);
    TPMS_SIGNATURE_ECDSA *ptr;
    TPM2B_ECC_PARAMETER *ptr2;
    size_t offset = 10;
    TSS2_RC rc;

    memset(ha.sha512, 'a', TPM2_SHA512_DIGEST_SIZE);
    rc = Tss2_MU_TPMU_HA_Marshal(&ha, TPM2_ALG_SHA512, buffer, buffer_size, &offset);
    assert_int_equal (rc, TSS2_RC_SUCCESS);
    assert_int_equal (memcmp(buffer + 10, ha.sha512, TPM2_SHA512_DIGEST_SIZE), 0);
    assert_int_equal (offset, 10 + TPM2_SHA512_DIGEST_SIZE);

    sig.ecdsa.hash = TPM2_ALG_SHA1;
    sig.ecdsa.signatureR.size = 4;
    sig.ecdsa.signatureR.buffer[0] = 'a';
    sig.ecdsa.signatureR.buffer[1] = 'b';
    sig.ecdsa.signatureR.buffer[2] = 'c';
    sig.ecdsa.signatureR.buffer[3] = 'd';
    sig.ecdsa.signatureS.size = 4;
    sig.ecdsa.signatureS.buffer[0] = 'e';
    sig.ecdsa.signatureS.buffer[1] = 'd';
    sig.ecdsa.signatureS.buffer[2] = 'f';
    sig.ecdsa.signatureS.buffer[3] = 'g';

    rc = Tss2_MU_TPMU_SIGNATURE_Marshal(&sig, TPM2_ALG_ECDSA, buffer, buffer_size, &offset);
    assert_int_equal (rc, TSS2_RC_SUCCESS);
    ptr = (TPMS_SIGNATURE_ECDSA *) (buffer + 10 + TPM2_SHA512_DIGEST_SIZE);
    assert_int_equal (ptr->hash, HOST_TO_BE_16(TPM2_ALG_SHA1));
    assert_int_equal (ptr->signatureR.size, HOST_TO_BE_16(4));
    assert_int_equal (ptr->signatureR.buffer[0], 'a');
    assert_int_equal (ptr->signatureR.buffer[1], 'b');
    assert_int_equal (ptr->signatureR.buffer[2], 'c');
    assert_int_equal (ptr->signatureR.buffer[3], 'd');
    ptr2 = (TPM2B_ECC_PARAMETER *) (buffer + 10 + TPM2_SHA512_DIGEST_SIZE + 8);
    assert_int_equal (ptr2->size, HOST_TO_BE_16(4));
    assert_int_equal (ptr2->buffer[0], 'e');
    assert_int_equal (ptr2->buffer[1], 'd');
    assert_int_equal (ptr2->buffer[2], 'f');
    assert_int_equal (ptr2->buffer[3], 'g');
    assert_int_equal (offset, 10 + TPM2_SHA512_DIGEST_SIZE + 2 + ((2 + 1 + 1 + 1 + 1) * 2));
}

/*
 * Success case with a null buffer
 */
static void
tpmu_marshal_buffer_null_with_offset(void **state)
{
    TPMU_HA ha = {0};
    TPMU_SIGNATURE sig = {0};
    size_t  buffer_size = sizeof(ha) + sizeof(sig) + 10;
    size_t offset = 10;
    TSS2_RC rc;

    memset(ha.sha512, 'a', TPM2_SHA512_DIGEST_SIZE);
    rc = Tss2_MU_TPMU_HA_Marshal(&ha, TPM2_ALG_SHA512, NULL, buffer_size, &offset);
    assert_int_equal (rc, TSS2_RC_SUCCESS);
    assert_int_equal (offset, 10 + TPM2_SHA512_DIGEST_SIZE);

    sig.ecdsa.hash = TPM2_ALG_SHA1;
    sig.ecdsa.signatureR.size = 4;
    sig.ecdsa.signatureR.buffer[0] = 'a';
    sig.ecdsa.signatureR.buffer[1] = 'b';
    sig.ecdsa.signatureR.buffer[2] = 'c';
    sig.ecdsa.signatureR.buffer[3] = 'd';
    sig.ecdsa.signatureS.size = 4;
    sig.ecdsa.signatureS.buffer[0] = 'e';
    sig.ecdsa.signatureS.buffer[1] = 'd';
    sig.ecdsa.signatureS.buffer[2] = 'f';
    sig.ecdsa.signatureS.buffer[3] = 'g';

    rc = Tss2_MU_TPMU_SIGNATURE_Marshal(&sig, TPM2_ALG_ECDSA, NULL, buffer_size, &offset);
    assert_int_equal (rc, TSS2_RC_SUCCESS);
    assert_int_equal (offset, 10 + TPM2_SHA512_DIGEST_SIZE + 2 + ((2 + 1 + 1 + 1 + 1) * 2));
}

/*
 * Invalid case with a null buffer and a null offset
 */
static void
tpmu_marshal_buffer_null_offset_null(void **state)
{
    TPMU_HA ha = {0};
    TPMU_SIGNATURE sig = {0};
    TSS2_RC rc;

    rc = Tss2_MU_TPMU_HA_Marshal(&ha, TPM2_ALG_SHA512, NULL, sizeof(ha), NULL);
    assert_int_equal (rc, TSS2_MU_RC_BAD_REFERENCE);

    rc = Tss2_MU_TPMU_SIGNATURE_Marshal(&sig, TPM2_ALG_ECDSA, NULL, sizeof(sig), NULL);
    assert_int_equal (rc, TSS2_MU_RC_BAD_REFERENCE);
}

/*
 * Invalid case with not big enough buffer
 */
static void
tpmu_marshal_buffer_size_lt_data_nad_lt_offset(void **state)
{
    TPMU_HA ha = {0};
    TPMU_SIGNATURE sig = {0};
    uint8_t buffer[sizeof(ha) + sizeof(sig) + 10] = { 0 };
    size_t offset = 10;
    TSS2_RC rc;

    memset(ha.sha512, 'a', TPM2_SHA512_DIGEST_SIZE);
    rc = Tss2_MU_TPMU_HA_Marshal(&ha, TPM2_ALG_SHA512, buffer, TPM2_SHA512_DIGEST_SIZE - 1, &offset);
    assert_int_equal (rc, TSS2_MU_RC_INSUFFICIENT_BUFFER);
    assert_int_equal (offset, 10);

    sig.ecdsa.hash = TPM2_ALG_SHA1;
    sig.ecdsa.signatureR.size = 4;
    sig.ecdsa.signatureR.buffer[0] = 'a';
    sig.ecdsa.signatureR.buffer[1] = 'b';
    sig.ecdsa.signatureR.buffer[2] = 'c';
    sig.ecdsa.signatureR.buffer[3] = 'd';
    sig.ecdsa.signatureS.size = 4;
    sig.ecdsa.signatureS.buffer[0] = 'e';
    sig.ecdsa.signatureS.buffer[1] = 'd';
    sig.ecdsa.signatureS.buffer[2] = 'f';
    sig.ecdsa.signatureS.buffer[3] = 'g';

    rc = Tss2_MU_TPMU_SIGNATURE_Marshal(&sig, TPM2_ALG_ECDSA, buffer, 12, &offset);
    assert_int_equal (rc, TSS2_MU_RC_INSUFFICIENT_BUFFER);
    assert_int_equal (offset, 10);
}

/*
 * Success case
 */
static void
tpmu_unmarshal_success(void **state)
{
    TPMU_HA ha = {0};
    TPMU_SIGNATURE sig = {0};
    uint8_t buffer[sizeof(ha) + sizeof(sig)] = { 0 };
    size_t  buffer_size = sizeof(buffer);
    TPMS_SIGNATURE_ECDSA *ptr;
    TPM2B_ECC_PARAMETER *ptr2;
    size_t offset = 0;
    TSS2_RC rc;

    memset(buffer, 'a', TPM2_SHA512_DIGEST_SIZE);
    rc = Tss2_MU_TPMU_HA_Unmarshal(buffer, buffer_size, &offset, TPM2_ALG_SHA512, &ha);
    assert_int_equal (rc, TSS2_RC_SUCCESS);
    assert_int_equal (offset, TPM2_SHA512_DIGEST_SIZE);
    assert_int_equal (memcmp(buffer, ha.sha512, TPM2_SHA512_DIGEST_SIZE), 0);

    offset = 0;
    ptr = (TPMS_SIGNATURE_ECDSA *) buffer;
    ptr2 = (TPM2B_ECC_PARAMETER *) (buffer + 8);
    ptr->hash = HOST_TO_BE_16(TPM2_ALG_SHA1);
    ptr->signatureR.size = HOST_TO_BE_16(4);
    ptr->signatureR.buffer[0] = 'a';
    ptr->signatureR.buffer[1] = 'b';
    ptr->signatureR.buffer[2] = 'c';
    ptr->signatureR.buffer[3] = 'd';
    ptr2->size = HOST_TO_BE_16(4);
    ptr2->buffer[0] = 'e';
    ptr2->buffer[1] = 'd';
    ptr2->buffer[2] = 'f';
    ptr2->buffer[3] = 'g';

    rc = Tss2_MU_TPMU_SIGNATURE_Unmarshal(buffer, buffer_size, &offset, TPM2_ALG_ECDSA, &sig);
    assert_int_equal (rc, TSS2_RC_SUCCESS);
    assert_int_equal (offset, 14);
    assert_int_equal (sig.ecdsa.hash, TPM2_ALG_SHA1);
    assert_int_equal (sig.ecdsa.signatureR.size, 4);
    assert_int_equal (sig.ecdsa.signatureR.buffer[0], 'a');
    assert_int_equal (sig.ecdsa.signatureR.buffer[1], 'b');
    assert_int_equal (sig.ecdsa.signatureR.buffer[2], 'c');
    assert_int_equal (sig.ecdsa.signatureR.buffer[3], 'd');
    assert_int_equal (sig.ecdsa.signatureS.size, 4);
    assert_int_equal (sig.ecdsa.signatureS.buffer[0], 'e');
    assert_int_equal (sig.ecdsa.signatureS.buffer[1], 'd');
    assert_int_equal (sig.ecdsa.signatureS.buffer[2], 'f');
    assert_int_equal (sig.ecdsa.signatureS.buffer[3], 'g');
}

/*
 * Invalid test case with buffer null and dest null
 */
static void
tpmu_unmarshal_dest_null_buff_null(void **state)
{
    size_t offset = 1;
    TSS2_RC rc;

    rc = Tss2_MU_TPMU_HA_Unmarshal(NULL, TPM2_SHA512_DIGEST_SIZE, &offset, TPM2_ALG_SHA512, NULL);
    assert_int_equal (rc, TSS2_MU_RC_BAD_REFERENCE);
    assert_int_equal (offset, 1);

    rc = Tss2_MU_TPMU_SIGNATURE_Unmarshal(NULL, 32, &offset, TPM2_ALG_ECDSA, NULL);
    assert_int_equal (rc, TSS2_MU_RC_BAD_REFERENCE);
    assert_int_equal (offset, 1);
}

/*
 * Invalid test case with offset null and dest null
 */
static void
tpmu_unmarshal_buffer_null_offset_null(void **state)
{
    uint8_t buffer[sizeof(TPMU_HA) + sizeof(TPMU_SIGNATURE)] = { 0 };
    size_t  buffer_size = sizeof(buffer);
    TSS2_RC rc;

    rc = Tss2_MU_TPMU_HA_Unmarshal(buffer, buffer_size, NULL, TPM2_ALG_SHA512, NULL);
    assert_int_equal (rc, TSS2_MU_RC_BAD_REFERENCE);

    rc = Tss2_MU_TPMU_SIGNATURE_Unmarshal(buffer, buffer_size, NULL, TPM2_ALG_ECDSA, NULL);
    assert_int_equal (rc, TSS2_MU_RC_BAD_REFERENCE);
}

/*
 * Test case ensures the offset is updated when dest is NULL
 * and offset is valid
 */
static void
tpmu_unmarshal_dest_null_offset_valid(void **state)
{
    uint8_t buffer[sizeof(TPMU_HA) + sizeof(TPMU_SIGNATURE)] = { 0 };
    size_t  buffer_size = sizeof(buffer);
    TPMS_SIGNATURE_ECDSA *ptr;
    TPM2B_ECC_PARAMETER *ptr2;
    size_t offset = 0;
    TSS2_RC rc;

    memset(buffer, 'a', TPM2_SHA512_DIGEST_SIZE);
    rc = Tss2_MU_TPMU_HA_Unmarshal(buffer, buffer_size, &offset, TPM2_ALG_SHA512, NULL);
    assert_int_equal (rc, TSS2_RC_SUCCESS);
    assert_int_equal (offset, TPM2_SHA512_DIGEST_SIZE);

    offset = 0;
    ptr = (TPMS_SIGNATURE_ECDSA *) buffer;
    ptr2 = (TPM2B_ECC_PARAMETER *) (buffer + 8);
    ptr->hash = HOST_TO_BE_16(TPM2_ALG_SHA1);
    ptr->signatureR.size = HOST_TO_BE_16(4);
    ptr->signatureR.buffer[0] = 'a';
    ptr->signatureR.buffer[1] = 'b';
    ptr->signatureR.buffer[2] = 'c';
    ptr->signatureR.buffer[3] = 'd';
    ptr2->size = HOST_TO_BE_16(4);
    ptr2->buffer[0] = 'e';
    ptr2->buffer[1] = 'd';
    ptr2->buffer[2] = 'f';
    ptr2->buffer[3] = 'g';

    rc = Tss2_MU_TPMU_SIGNATURE_Unmarshal(buffer, buffer_size, &offset, TPM2_ALG_ECDSA, NULL);
    assert_int_equal (rc, TSS2_RC_SUCCESS);
    assert_int_equal (offset, 14);
}

/*
 * Invalid case with not big enough buffer. Make sure offest is untouched.
 */
static void
tpmu_unmarshal_buffer_size_lt_data_nad_lt_offset(void **state)
{
    TPMU_HA ha = {0};
    TPMU_SIGNATURE sig = {0};
    uint8_t buffer[sizeof(ha) + sizeof(sig)] = { 0 };
    TPMS_SIGNATURE_ECDSA *ptr;
    TPM2B_ECC_PARAMETER *ptr2;
    size_t offset = 5;
    TSS2_RC rc;

    memset(buffer, 'a', TPM2_SHA512_DIGEST_SIZE);
    rc = Tss2_MU_TPMU_HA_Unmarshal(buffer, TPM2_SHA512_DIGEST_SIZE - 1, &offset, TPM2_ALG_SHA512, &ha);
    assert_int_equal (rc, TSS2_MU_RC_INSUFFICIENT_BUFFER);
    assert_int_equal (offset, 5);

    ptr = (TPMS_SIGNATURE_ECDSA *) buffer;
    ptr2 = (TPM2B_ECC_PARAMETER *) (buffer + 8);
    ptr->hash = HOST_TO_BE_16(TPM2_ALG_SHA1);
    ptr->signatureR.size = HOST_TO_BE_16(4);
    ptr->signatureR.buffer[0] = 'a';
    ptr->signatureR.buffer[1] = 'b';
    ptr->signatureR.buffer[2] = 'c';
    ptr->signatureR.buffer[3] = 'd';
    ptr2->size = HOST_TO_BE_16(4);
    ptr2->buffer[0] = 'e';
    ptr2->buffer[1] = 'd';
    ptr2->buffer[2] = 'f';
    ptr2->buffer[3] = 'g';

    rc = Tss2_MU_TPMU_SIGNATURE_Unmarshal(buffer, 14, &offset, TPM2_ALG_ECDSA, &sig);
    assert_int_equal (rc, TSS2_MU_RC_INSUFFICIENT_BUFFER);
    assert_int_equal (offset, 5);
}

static void
tpmu_name_marshal(void **state)
{
    TPMU_NAME name = {0};
    TPMT_HA ha = {0};
    uint8_t buf[256] = {0};
    TPM2_HANDLE hdl = TPM2_RH_PW;
    TPM2_HANDLE hdl_expected = HOST_TO_BE_32(TPM2_RH_PW);
    TPM2_ALG_ID id_expected = HOST_TO_BE_16(TPM2_ALG_SHA1);
    size_t size = sizeof(hdl), offset = 0;
    const char digest[] = {0xa, 0xb, 0xc, 0xd, 0xe, 0xf, 0x01, 0x02,
                           0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09,
                           0x10, 0x11, 0x12, 0x13, 0x14};
    TPM2_RC rc;

    /* Handle case */
    size = sizeof(hdl);
    name.handle = hdl;

    rc = Tss2_MU_TPMU_NAME_Marshal(&name, size, buf, sizeof(hdl), &offset);
    assert_int_equal (rc, TSS2_RC_SUCCESS);
    assert_int_equal (offset, sizeof(hdl));
    assert_memory_equal ((void *) buf, &hdl_expected, sizeof(hdl));

    /* Digest case */
    offset = 0;
    size = sizeof(TPM2_ALG_ID) + TPM2_SHA1_DIGEST_SIZE;
    ha.hashAlg = TPM2_ALG_SHA1;
    memcpy(&ha.digest, digest, TPM2_SHA1_DIGEST_SIZE);
    memcpy(&name.digest, &ha, sizeof(ha));
    rc = Tss2_MU_TPMU_NAME_Marshal(&name, size, buf, TPM2_SHA1_DIGEST_SIZE + 2, &offset);
    assert_int_equal (rc, TSS2_RC_SUCCESS);
    assert_int_equal (offset, TPM2_SHA1_DIGEST_SIZE + 2);
    assert_memory_equal (buf, &id_expected, sizeof(TPM2_ALG_ID));
    assert_memory_equal (buf + 2, digest, TPM2_SHA1_DIGEST_SIZE);
}

int main(void) {
    const struct CMUnitTest tests[] = {
        cmocka_unit_test (tpmu_marshal_success),
        cmocka_unit_test (tpmu_marshal_success_offset),
        cmocka_unit_test (tpmu_marshal_buffer_null_with_offset),
        cmocka_unit_test (tpmu_marshal_buffer_null_offset_null),
        cmocka_unit_test (tpmu_marshal_buffer_size_lt_data_nad_lt_offset),
        cmocka_unit_test (tpmu_unmarshal_success),
        cmocka_unit_test (tpmu_unmarshal_dest_null_buff_null),
        cmocka_unit_test (tpmu_unmarshal_buffer_null_offset_null),
        cmocka_unit_test (tpmu_unmarshal_dest_null_offset_valid),
        cmocka_unit_test (tpmu_unmarshal_buffer_size_lt_data_nad_lt_offset),
        cmocka_unit_test (tpmu_name_marshal),
    };
    return cmocka_run_group_tests(tests, NULL, NULL);
}
