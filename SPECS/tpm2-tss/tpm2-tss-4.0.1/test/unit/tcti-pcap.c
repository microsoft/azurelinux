/* SPDX-License-Identifier: BSD-2-Clause */
/*
 * Copyright (c) 2020 Infineon Technologies AG
 * All rights reserved.
 */

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <inttypes.h>
#include <limits.h>
#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <sys/stat.h>
#include <netinet/in.h>

#include <setjmp.h>
#include <cmocka.h>

#include "tss2_tcti.h"
#include "tss2_tcti_pcap.h"

#include "tss2-tcti/tcti-common.h"
#include "tss2-tcti/tcti-pcap.h"

#if (__BYTE_ORDER__ == __ORDER_BIG_ENDIAN__)
#define _LE32TOH(a,b,c,d) d,c,b,a
#define _LE16TOH(a,b) b,a
#else
#define _LE32TOH(a,b,c,d) a,b,c,d
#define _LE16TOH(a,b) a,b
#endif

#define TCTI_STUB_CONF      "stub"
#define TCTI_PCAP_ENV_VAR   "pcap_env_var"
#define TCTI_PCAP_FILE      "pcap_file"
#define TCTI_PCAP_FD        0x01234567
#define TCTI_PCAP_IP_HOST   0x01, 0x02, 0x03, 0x04
#define TCTI_PCAP_IP_TPM    0x05, 0x06, 0x07, 0x08
#define TCTI_PCAP_IP_HOST_L 0x0102
#define TCTI_PCAP_IP_HOST_H 0x0304
#define TCTI_PCAP_IP_TPM_L  0x0506
#define TCTI_PCAP_IP_TPM_H  0x0708
#define TCTI_PCAP_TCP_SEQ_HOST     0x00, 0x11, 0x22, 0x33
#define TCTI_PCAP_TCP_SEQ_TPM      0xaa, 0xbb, 0xcc, 0xdd
#define TCTI_PCAP_TCP_SEQ_HOST_INT 0x00112233
#define TCTI_PCAP_TCP_SEQ_TPM_INT  0xaabbccdd
#define TCTI_PCAP_HOST_PORT_BYTES  0xcd, 0xef
#define TCTI_PCAP_TIMESTAMP_SEC    ((uint64_t) 0x0001020304050607 / 1000000)
#define TCTI_PCAP_TIMESTAMP_NSEC   (((uint64_t) 0x0001020304050607 % 1000000) * 1000)
#define TCTI_PCAP_TIMESTAMP_BYTES  _LE32TOH(0x03, 0x02, 0x01, 0x00),  _LE32TOH(0x07, 0x06, 0x05, 0x04)

static const uint8_t pcap_header[] = {
    /* section header block */
    _LE32TOH(0x0a, 0x0d, 0x0d, 0x0a),
    _LE32TOH(0x1c, 0x00, 0x00, 0x00),
    _LE32TOH(0x4d, 0x3c, 0x2b, 0x1a),
    _LE16TOH(0x01, 0x00),
    0x00, 0x00,
    0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
    _LE32TOH(0x1c, 0x00, 0x00, 0x00),
    /* interface description block */
    _LE32TOH(0x01, 0x00, 0x00, 0x00),
    _LE32TOH(0x14, 0x00, 0x00, 0x00),
    _LE16TOH(0xE4, 0x00),
    0x00, 0x00,
    0x00, 0x00, 0x00, 0x00,
    _LE32TOH(0x14, 0x00, 0x00, 0x00)
};

static uint8_t pcap_rx_epb_data[] = {
    /* enhanced packet block header */
    _LE32TOH(0x06, 0x00, 0x00, 0x00),
    _LE32TOH(0x4c, 0x00, 0x00, 0x00),
    0x00, 0x00, 0x00, 0x00,
    TCTI_PCAP_TIMESTAMP_BYTES,
    _LE32TOH(0x2b, 0x00, 0x00, 0x00),
    _LE32TOH(0x2b, 0x00, 0x00, 0x00),
    /* ipv4 header */
    0x45,
    0x00,
    0x00, 0x2b,
    0x00, 0x00,
    0x40, 0x00,
    0xff,
    0x06,
    0x00, 0x00,
    TCTI_PCAP_IP_TPM,
    TCTI_PCAP_IP_HOST,
    /* tcp header */
    0x09, 0x11,
    0xc3, 0x50,
    TCTI_PCAP_TCP_SEQ_TPM,
    TCTI_PCAP_TCP_SEQ_HOST,
    0x50, 0x10,
    0xff, 0xff,
    0x00, 0x00,
    0x00, 0x00,
    /* data */
    0x00, 0x01, 0x02,
    /* epb padding */
    0x00,
    /* epb footer */
    _LE32TOH(0x4c, 0x00, 0x00, 0x00)
};

static uint8_t pcap_tx_epb_data[] = {
    /* enhanced packet block header */
    _LE32TOH(0x06, 0x00, 0x00, 0x00),
    _LE32TOH(0x4c, 0x00, 0x00, 0x00),
    0x00, 0x00, 0x00, 0x00,
    TCTI_PCAP_TIMESTAMP_BYTES,
    _LE32TOH(0x2b, 0x00, 0x00, 0x00),
    _LE32TOH(0x2b, 0x00, 0x00, 0x00),
    /* ipv4 header */
    0x45,
    0x00,
    0x00, 0x2b,
    0x00, 0x00,
    0x40, 0x00,
    0xff,
    0x06,
    0x00, 0x00,
    TCTI_PCAP_IP_HOST,
    TCTI_PCAP_IP_TPM,
    /* tcp header */
    0xc3, 0x50,
    0x09, 0x11,
    TCTI_PCAP_TCP_SEQ_HOST,
    TCTI_PCAP_TCP_SEQ_TPM,
    0x50, 0x10,
    0xff, 0xff,
    0x00, 0x00,
    0x00, 0x00,
    /* data */
    0x00, 0x01, 0x02,
    /* epb padding */
    0x00,
    /* epb footer */
    _LE32TOH(0x4c, 0x00, 0x00, 0x00)
};

typedef struct {
    TSS2_TCTI_COMMON_CONTEXT common;
} TSS2_TCTI_STUB_CONTEXT;

TSS2_RC
tcti_stub_transmit (
    TSS2_TCTI_CONTEXT *tcti_ctx,
    size_t size,
    const uint8_t *cmd_buf)
{
    ssize_t ret = mock_type (ssize_t);
    size_t expected_size = mock_type (int);
    uint8_t *expected_buf = mock_type (uint8_t*);

    assert_int_equal (expected_size, size);
    assert_memory_equal (expected_buf, cmd_buf, size);

    return ret;
}

TSS2_RC
tcti_stub_receive (
    TSS2_TCTI_CONTEXT *tctiContext,
    size_t *response_size,
    uint8_t *response_buffer,
    int32_t timeout)
{
    ssize_t ret = mock_type (ssize_t);
    *response_size = mock_type (int);
    uint8_t *buf_in;

    /* partial read */
    if (response_buffer == NULL) {
        return ret;
    }

    buf_in = mock_type (uint8_t*);
    memcpy (response_buffer, buf_in, *response_size);

    return ret;
}

TSS2_RC
tcti_stub_cancel (
    TSS2_TCTI_CONTEXT *tctiContext)
{
    return mock_type (ssize_t);
}

TSS2_RC
tcti_stub_set_locality (
    TSS2_TCTI_CONTEXT *tctiContext,
    uint8_t locality)
{
    ssize_t ret = mock_type (ssize_t);
    uint8_t expected_locality = mock_type (int);

    assert_int_equal (expected_locality, locality);

    return ret;
}

TSS2_RC
tcti_stub_get_poll_handles (
    TSS2_TCTI_CONTEXT *tctiContext,
    TSS2_TCTI_POLL_HANDLE *handles,
    size_t *num_handles)
{
    ssize_t ret = mock_type (ssize_t);

    return ret;
}

TSS2_RC
Tss2_TctiLdr_Initialize (const char *nameConf,
                         TSS2_TCTI_CONTEXT **tctiContext)
{
    TSS2_TCTI_STUB_CONTEXT *tcti_pcap;
    TSS2_TCTI_COMMON_CONTEXT *tcti_common;

    *tctiContext = NULL;

    if (nameConf != NULL && strcmp (nameConf, TCTI_STUB_CONF) == 0) {
        /* create and return stub tcti */
        tcti_pcap =  calloc (1, sizeof (TSS2_TCTI_STUB_CONTEXT));
        tcti_common =  (TSS2_TCTI_COMMON_CONTEXT*) tcti_pcap;

        TSS2_TCTI_MAGIC (tcti_common) = TCTI_PCAP_MAGIC;
        TSS2_TCTI_VERSION (tcti_common) = TCTI_VERSION;
        TSS2_TCTI_TRANSMIT (tcti_common) = tcti_stub_transmit;
        TSS2_TCTI_RECEIVE (tcti_common) = tcti_stub_receive;
        TSS2_TCTI_FINALIZE (tcti_common) = NULL;
        TSS2_TCTI_CANCEL (tcti_common) = tcti_stub_cancel;
        TSS2_TCTI_GET_POLL_HANDLES (tcti_common) = tcti_stub_get_poll_handles;
        TSS2_TCTI_SET_LOCALITY (tcti_common) = tcti_stub_set_locality;
        TSS2_TCTI_MAKE_STICKY (tcti_common) = NULL;
        tcti_common->state = TCTI_STATE_TRANSMIT;

        *tctiContext = (TSS2_TCTI_CONTEXT *) tcti_pcap;

        return TPM2_RC_SUCCESS;
    } else {
        /* return mocked rc */
        return mock_type (int);
    }
}

void
Tss2_TctiLdr_Finalize (TSS2_TCTI_CONTEXT **tctiContext)
{
    free (*tctiContext);
}

char *
__real_getenv (const char *name);

char *
__wrap_getenv (const char *name)
{
    if (name != NULL && strcmp(name, ENV_PCAP_FILE) == 0) {
        return TCTI_PCAP_FILE;
    }

    return __real_getenv(name);
}

int
__wrap_rand (void)
{
    return mock_type (int);
}

int
__wrap_clock_gettime (clockid_t clk_id, struct timespec *tp)
{
    if (clk_id == CLOCK_REALTIME) {
        tp->tv_sec = TCTI_PCAP_TIMESTAMP_SEC;
        tp->tv_nsec = TCTI_PCAP_TIMESTAMP_NSEC;
        return EXIT_SUCCESS;
    }

    return EXIT_FAILURE;
}

int
__wrap___clock_gettime64 (clockid_t clk_id, struct timespec *tp)
{
    return __wrap_clock_gettime(clk_id, tp);
}

int
__real_open (const char *pathname, int flags, mode_t mode);

int
__wrap_open (const char *pathname, int flags, mode_t mode)
{
    if (pathname != NULL && strcmp (pathname, TCTI_PCAP_FILE) == 0) {
        return mock_type (int);
    } else {
        return __real_open(pathname, flags, mode);
    }
}

ssize_t
__real_read (int fd, void *buffer, size_t buffer_size);

ssize_t
__wrap_read (int fd, void *buffer, size_t buffer_size)
{
    uint8_t *buf_in;
    ssize_t ret;

    if (fd == TCTI_PCAP_FD) {
        ret = mock_type (ssize_t);
        buf_in = mock_type (uint8_t*);

        memcpy (buffer, buf_in, ret);
        return ret;
    } else {
        return __real_read(fd, buffer, buffer_size);
    }
}

int
__real_close(int fd);

int
__wrap_close(int fd)
{
    if (fd == TCTI_PCAP_FD) {
        return mock_type (int);
    } else {
        return __real_close (fd);
    }
}

ssize_t
__real_write (int fd, void *buffer, size_t buffer_size);

ssize_t
__wrap_write (int fd, void *buffer, size_t buffer_size)
{
    size_t expected_size;
    uint8_t *expected_buffer;
    ssize_t ret;

    if (fd == TCTI_PCAP_FD) {
        ret = mock_type (int);
        expected_size = mock_type (int);
        expected_buffer = mock_type (uint8_t*);

        fprintf(stderr, "exp: ");
        for (size_t i = 0; i < expected_size; i++)
            fprintf(stderr, "%02x", ((uint8_t *) expected_buffer)[i]);
        fprintf(stderr, "\n");

        fprintf(stderr, "got: ");
        for (size_t i = 0; i < buffer_size; i++)
            fprintf(stderr, "%02x", ((uint8_t *) buffer)[i]);
        fprintf(stderr, "\n");

        assert_int_equal (expected_size, buffer_size);
        assert_memory_equal (expected_buffer, buffer, buffer_size);

        return ret;
    } else {
        return __real_write (fd, buffer, buffer_size);
    }
}

static void
update_tcp_seq (void* data, uint32_t size)
{
    const size_t offset = 52;
    uint32_t seq_no;

    seq_no =  *((uint32_t*) (data + offset));

    seq_no = ntohl (seq_no);
    seq_no += size;
    seq_no = htonl (seq_no);

    *((uint32_t*) (data + offset)) = seq_no;
}

static void
tcti_pcap_init_context_and_size_null_test (void **state)
{
    TSS2_RC rc;

    rc = Tss2_Tcti_Pcap_Init (NULL, NULL, NULL);
    assert_int_equal (rc, TSS2_TCTI_RC_BAD_VALUE);
}

static void
tcti_pcap_init_size_test (void **state)
{
    size_t tcti_size = 0;
    TSS2_RC rc;

    rc = Tss2_Tcti_Pcap_Init (NULL, &tcti_size, NULL);
    assert_int_equal (rc, TSS2_RC_SUCCESS);
    assert_int_equal (tcti_size, sizeof (TSS2_TCTI_PCAP_CONTEXT));
}

static void
tcti_pcap_init_tctildr_fail_test (void **state)
{
    size_t tcti_size = 0;
    TSS2_TCTI_PCAP_CONTEXT tcti_pcap = {0};
    TSS2_TCTI_CONTEXT *tcti = (TSS2_TCTI_CONTEXT*) &tcti_pcap;
    TSS2_RC rc = TSS2_RC_SUCCESS;

    will_return (Tss2_TctiLdr_Initialize, TSS2_TCTI_RC_MEMORY);
    rc = Tss2_Tcti_Pcap_Init (tcti, &tcti_size, NULL);
    assert_int_equal (rc, TSS2_TCTI_RC_MEMORY);
    assert_int_equal (tcti_pcap.pcap_builder.fd, 0);
}

static void
tcti_pcap_init_open_fail_test (void **state)
{
    size_t tcti_size = 0;
    TSS2_RC ret = TSS2_RC_SUCCESS;
    TSS2_TCTI_CONTEXT *tcti = NULL;
    TSS2_RC rc = TSS2_RC_SUCCESS;

    ret = Tss2_Tcti_Pcap_Init (NULL, &tcti_size, NULL);
    assert_true (ret == TSS2_RC_SUCCESS);

    tcti = calloc (1, tcti_size);
    assert_non_null (tcti);

    will_return (__wrap_rand, 0); /* host ip */
    will_return (__wrap_rand, 0);
    will_return (__wrap_rand, 0); /* tpm ip */
    will_return (__wrap_rand, 0);
    will_return (__wrap_rand, 0); /* host sequence no */
    will_return (__wrap_rand, 0); /* tpm sequence no */
    will_return (__wrap_open, -1);
    rc = Tss2_Tcti_Pcap_Init (tcti, &tcti_size, TCTI_STUB_CONF);
    assert_int_equal (rc, TSS2_TCTI_RC_IO_ERROR);

    free (tcti);
}

static void
tcti_pcap_init_write_fail_test (void **state)
{
    size_t tcti_size = 0;
    TSS2_RC ret = TSS2_RC_SUCCESS;
    TSS2_TCTI_CONTEXT *tcti = NULL;
    TSS2_RC rc = TSS2_RC_SUCCESS;

    ret = Tss2_Tcti_Pcap_Init (NULL, &tcti_size, NULL);
    assert_true (ret == TSS2_RC_SUCCESS);

    tcti = calloc (1, tcti_size);
    assert_non_null (tcti);

    will_return (__wrap_rand, 0); /* host ip */
    will_return (__wrap_rand, 0);
    will_return (__wrap_rand, 0); /* tpm ip */
    will_return (__wrap_rand, 0);
    will_return (__wrap_rand, 0); /* host sequence no */
    will_return (__wrap_rand, 0); /* tpm sequence no */
    will_return (__wrap_open, TCTI_PCAP_FD);
    will_return (__wrap_write, -1);
    will_return (__wrap_write, sizeof(pcap_header));
    will_return (__wrap_write, pcap_header);
    will_return (__wrap_close, 0); /* close pcap */
    rc = Tss2_Tcti_Pcap_Init (tcti, &tcti_size, TCTI_STUB_CONF);
    assert_int_equal (rc, TSS2_TCTI_RC_IO_ERROR);

    free (tcti);
}

/* Setup functions to create the context for the pcap TCTI */
static int
tcti_pcap_setup (void **state)
{
    size_t tcti_size = 0;
    TSS2_RC ret = TSS2_RC_SUCCESS;
    TSS2_TCTI_CONTEXT *tcti = NULL;

    ret = Tss2_Tcti_Pcap_Init (NULL, &tcti_size, NULL);
    assert_true (ret == TSS2_RC_SUCCESS);

    tcti = calloc (1, tcti_size);
    assert_non_null (tcti);

    will_return (__wrap_rand, TCTI_PCAP_IP_HOST_L); /* host ip */
    will_return (__wrap_rand, TCTI_PCAP_IP_HOST_H);
    will_return (__wrap_rand, TCTI_PCAP_IP_TPM_L);  /* tpm ip */
    will_return (__wrap_rand, TCTI_PCAP_IP_TPM_H);
    will_return (__wrap_rand, TCTI_PCAP_TCP_SEQ_HOST_INT); /* host sequence no */
    will_return (__wrap_rand, TCTI_PCAP_TCP_SEQ_TPM_INT);  /* tpm sequence no */
    will_return (__wrap_open, TCTI_PCAP_FD);
    will_return (__wrap_write, sizeof(pcap_header));
    will_return (__wrap_write, sizeof(pcap_header));
    will_return (__wrap_write, pcap_header);
    ret = Tss2_Tcti_Pcap_Init (tcti, &tcti_size, TCTI_STUB_CONF);
    assert_true (ret == TSS2_RC_SUCCESS);

    *state = tcti;
    return 0;
}

static int
tcti_pcap_teardown (void **state)
{
    TSS2_TCTI_CONTEXT *tcti = (TSS2_TCTI_CONTEXT*)*state;

    will_return (__wrap_close, EXIT_SUCCESS);
    Tss2_Tcti_Finalize (tcti);
    free (tcti);

    return 0;

}

static void
tcti_pcap_receive_test (void **state)
{
    TSS2_TCTI_CONTEXT *ctx = (TSS2_TCTI_CONTEXT*)*state;
    TSS2_TCTI_COMMON_CONTEXT *tcti_common = tcti_common_context_cast (ctx);
    size_t partial_read_size = 123;
    uint8_t mock_response_buffer[] = {0x00, 0x01, 0x02};
    size_t mock_response_size = sizeof(mock_response_buffer);
    uint8_t response_buffer[100] = {0};
    size_t response_size = sizeof(response_buffer);
    TSS2_RC rc;

    tcti_common->state = TCTI_STATE_RECEIVE;

    /* have tcti_common_receive_checks fail */
    rc = Tss2_Tcti_Receive (ctx,
                            NULL,
                            NULL,
                            TSS2_TCTI_TIMEOUT_BLOCK);
    assert_int_equal (rc, TSS2_TCTI_RC_BAD_REFERENCE);

    /* partial read: give back response_size of 123 */
    will_return (tcti_stub_receive, TSS2_RC_SUCCESS);
    will_return (tcti_stub_receive, partial_read_size);
    rc = Tss2_Tcti_Receive (ctx,
                            &response_size,
                            NULL, /* NULL buffer */
                            TSS2_TCTI_TIMEOUT_BLOCK);
    assert_int_equal (rc, TSS2_RC_SUCCESS);
    assert_int_equal (response_size, partial_read_size);

    /* underlying read fails */
    will_return (tcti_stub_receive, TSS2_TCTI_RC_IO_ERROR);
    will_return (tcti_stub_receive, 0);
    will_return (tcti_stub_receive, NULL);
    /* receive fails, it will not log to pcap */
    rc = Tss2_Tcti_Receive (ctx,
                            &response_size,
                            response_buffer,
                            TSS2_TCTI_TIMEOUT_BLOCK);
    assert_int_equal (rc, TSS2_TCTI_RC_IO_ERROR);

    /* read successfully  */
    will_return (tcti_stub_receive, TSS2_RC_SUCCESS);
    will_return (tcti_stub_receive, mock_response_size);
    will_return (tcti_stub_receive, mock_response_buffer);
    will_return (__wrap_write, sizeof(pcap_rx_epb_data));
    will_return (__wrap_write, sizeof(pcap_rx_epb_data));
    will_return (__wrap_write, pcap_rx_epb_data);
    rc = Tss2_Tcti_Receive (ctx,
                            &response_size,
                            response_buffer,
                            TSS2_TCTI_TIMEOUT_BLOCK);
    assert_int_equal (rc, TSS2_RC_SUCCESS);
    assert_int_equal (response_size, mock_response_size);
    assert_memory_equal (response_buffer, mock_response_buffer, response_size);

    /* read successfully, but fail to write to pcap  */
    tcti_common->state = TCTI_STATE_RECEIVE;
    update_tcp_seq (pcap_rx_epb_data, mock_response_size);
    will_return (tcti_stub_receive, TSS2_RC_SUCCESS);
    will_return (tcti_stub_receive, mock_response_size);
    will_return (tcti_stub_receive, mock_response_buffer);
    will_return (__wrap_write, -1); /* fail to write to pcap */
    will_return (__wrap_write, sizeof(pcap_rx_epb_data));
    will_return (__wrap_write, pcap_rx_epb_data);
    rc = Tss2_Tcti_Receive (ctx,
                            &response_size,
                            response_buffer,
                            TSS2_TCTI_TIMEOUT_BLOCK);
    assert_int_equal (rc, TSS2_RC_SUCCESS);
    assert_int_equal (response_size, mock_response_size);
    assert_memory_equal (response_buffer, mock_response_buffer, response_size);
}

static void
tcti_pcap_transmit_test (void **state)
{
    TSS2_TCTI_CONTEXT *ctx = (TSS2_TCTI_CONTEXT*)*state;
    TSS2_TCTI_COMMON_CONTEXT *tcti_common = tcti_common_context_cast (ctx);
    uint8_t mock_transmit_buffer[] = {0x00, 0x01, 0x02};
    size_t mock_transmit_size = sizeof(mock_transmit_buffer);
    TSS2_RC rc;

    tcti_common->state = TCTI_STATE_TRANSMIT;

    /* have tcti_common_transmit_checks fail (cmd_buf = NULL) */
    rc = Tss2_Tcti_Transmit (ctx,
                             0,
                             NULL);
    assert_int_equal (rc, TSS2_TCTI_RC_BAD_REFERENCE);

    /* underlying tranmit fails*/
    will_return (tcti_stub_transmit, TSS2_TCTI_RC_IO_ERROR);
    will_return (tcti_stub_transmit, mock_transmit_size); /* assert size */
    will_return (tcti_stub_transmit, mock_transmit_buffer); /* assert buf */
    /* transmit fails, but it still logs to pcap */
    will_return (__wrap_write, sizeof(pcap_tx_epb_data));
    will_return (__wrap_write, sizeof(pcap_tx_epb_data));
    will_return (__wrap_write, pcap_tx_epb_data);
    rc = Tss2_Tcti_Transmit (ctx,
                             mock_transmit_size,
                             mock_transmit_buffer); /* have tcti_common_transmit_checks fail */
    assert_int_equal (rc, TSS2_TCTI_RC_IO_ERROR);

    /* transmit successfully */
    update_tcp_seq (pcap_tx_epb_data, mock_transmit_size);
    will_return (tcti_stub_transmit, TSS2_RC_SUCCESS);
    will_return (tcti_stub_transmit, mock_transmit_size); /* assert size */
    will_return (tcti_stub_transmit, mock_transmit_buffer); /* assert buf */
    will_return (__wrap_write, sizeof(pcap_tx_epb_data));
    will_return (__wrap_write, sizeof(pcap_tx_epb_data));
    will_return (__wrap_write, pcap_tx_epb_data);
    rc = Tss2_Tcti_Transmit (ctx,
                             mock_transmit_size,
                             mock_transmit_buffer);
    assert_int_equal (rc, TSS2_RC_SUCCESS);

    /* transmit successfully, but fail to write to pcap */
    tcti_common->state = TCTI_STATE_TRANSMIT;
    update_tcp_seq (pcap_tx_epb_data, mock_transmit_size);
    will_return (tcti_stub_transmit, TSS2_RC_SUCCESS);
    will_return (tcti_stub_transmit, mock_transmit_size); /* assert size */
    will_return (tcti_stub_transmit, mock_transmit_buffer); /* assert buf */
    will_return (__wrap_write, -1); /* fail to write to pcap */
    will_return (__wrap_write, sizeof(pcap_tx_epb_data));
    will_return (__wrap_write, pcap_tx_epb_data);
    rc = Tss2_Tcti_Transmit (ctx,
                             mock_transmit_size,
                             mock_transmit_buffer);
    assert_int_equal (rc, TSS2_RC_SUCCESS);
}

static void
tcti_pcap_cancel_test (void **state)
{
    TSS2_TCTI_CONTEXT *ctx = (TSS2_TCTI_CONTEXT*)*state;
    TSS2_TCTI_COMMON_CONTEXT *tcti_common = tcti_common_context_cast (ctx);
    TSS2_RC rc;

    tcti_common->state = TCTI_STATE_RECEIVE;

    /* have tcti_common_cancel_checks fail */
    rc = Tss2_Tcti_Cancel (NULL);
    assert_int_equal (rc, TSS2_TCTI_RC_BAD_REFERENCE);

    /* cancel successfully */
    will_return (tcti_stub_cancel, TSS2_RC_SUCCESS);
    /* cancel will not write to pcap */
    rc = Tss2_Tcti_Cancel (ctx);
    assert_int_equal (rc, TSS2_RC_SUCCESS);
}

static void
tcti_pcap_set_locality_test (void **state)
{
    TSS2_TCTI_CONTEXT *ctx = (TSS2_TCTI_CONTEXT*)*state;
    TSS2_TCTI_COMMON_CONTEXT *tcti_common = tcti_common_context_cast (ctx);
    uint8_t mock_locality = 3;
    TSS2_RC rc;

    tcti_common->state = TCTI_STATE_TRANSMIT;

    /* have tcti_common_set_locality_checks fail */
    rc = Tss2_Tcti_SetLocality (NULL, 0);
    assert_int_equal (rc, TSS2_TCTI_RC_BAD_REFERENCE);

    /* set_locality successfully */
    will_return (tcti_stub_set_locality, TSS2_RC_SUCCESS);
    will_return (tcti_stub_set_locality, mock_locality);
    /* set_locality will not write to pcap */
    rc = Tss2_Tcti_SetLocality (ctx, mock_locality);
    assert_int_equal (rc, TSS2_RC_SUCCESS);
}

static void
tcti_pcap_get_poll_handles_test (void **state)
{
    TSS2_TCTI_CONTEXT *ctx = (TSS2_TCTI_CONTEXT*)*state;
    TSS2_TCTI_COMMON_CONTEXT *tcti_common = tcti_common_context_cast (ctx);
    TSS2_TCTI_POLL_HANDLE handles [5] = {0};
    size_t num_handles = sizeof(handles);
    TSS2_RC rc;

    tcti_common->state = TCTI_STATE_TRANSMIT;

    /* have tcti_common_get_poll_handles_checks fail */
    rc = Tss2_Tcti_GetPollHandles (NULL, NULL, 0);
    assert_int_equal (rc, TSS2_TCTI_RC_BAD_REFERENCE);

    /* get_poll_handles successfully */
    will_return (tcti_stub_get_poll_handles, TSS2_RC_SUCCESS);
    /* get_poll_handles will not write to pcap */
    rc = Tss2_Tcti_GetPollHandles (ctx, handles, &num_handles);
    assert_int_equal (rc, TSS2_RC_SUCCESS);
}

int
main (int   argc,
      char *argv[])
{
    const struct CMUnitTest tests[] = {
        cmocka_unit_test (tcti_pcap_init_context_and_size_null_test),
        cmocka_unit_test (tcti_pcap_init_size_test),
        cmocka_unit_test (tcti_pcap_init_tctildr_fail_test),
        cmocka_unit_test (tcti_pcap_init_open_fail_test),
        cmocka_unit_test (tcti_pcap_init_write_fail_test),
        cmocka_unit_test_setup_teardown (tcti_pcap_receive_test,
                                         tcti_pcap_setup,
                                         tcti_pcap_teardown),
        cmocka_unit_test_setup_teardown (tcti_pcap_transmit_test,
                                         tcti_pcap_setup,
                                         tcti_pcap_teardown),
        cmocka_unit_test_setup_teardown (tcti_pcap_cancel_test,
                                         tcti_pcap_setup,
                                         tcti_pcap_teardown),
        cmocka_unit_test_setup_teardown (tcti_pcap_set_locality_test,
                                         tcti_pcap_setup,
                                         tcti_pcap_teardown),
        cmocka_unit_test_setup_teardown (tcti_pcap_get_poll_handles_test,
                                         tcti_pcap_setup,
                                         tcti_pcap_teardown),
    };
    return cmocka_run_group_tests (tests, NULL, NULL);
}
