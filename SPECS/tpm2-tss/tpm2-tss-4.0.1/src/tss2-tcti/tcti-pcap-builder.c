/* SPDX-License-Identifier: BSD-2-Clause */
/*
 * Copyright (c) 2020 Infineon Technologies AG
 * All rights reserved.
 */

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <time.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <errno.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/types.h>
#include <netinet/in.h>

#include "tss2_common.h"
#include "tcti-pcap-builder.h"
#include "util/io.h"
#define LOGMODULE tcti
#include "util/log.h"

#ifdef __FreeBSD__
#define CLOCK_MONOTONIC_RAW CLOCK_MONOTONIC
#endif

/* constants used */
#define PCAP_MAJOR                          0x0001
#define PCAP_MINOR                          0x0000
#define PCAP_BLOCK_TYPE_SHB                 0x0A0D0D0A
#define PCAP_BLOCK_TYPE_IDB                 0x00000001
#define PCAP_BLOCK_TYPE_EPB                 0x00000006
#define PCAP_SHB_BYTE_ORDER_MAGIC           0x1A2B3C4D
#define PCAP_SHB_SECTION_LEN_NOT_SPECIFIED  0xFFFFFFFFFFFFFFFFUL
#define PCAP_IDB_LINKTYPE_IPv4              0x00E4
#define PCAP_IDB_SNAP_LEN_NO_LIMIT          0x0000
#define PCAP_EPB_INTERFACE_ID               0x00000000

#define IPv4_VERSION                0x4
#define IPv4_TOS_BEST_EFFORT        0x00
#define IPv4_ID_UNUSED              0x0000
#define IPv4_FLAGS_DONT_FRAGMENT    0x2
#define IPv4_FRAGMENT_OFFSET_UNUSED 0x0000
#define IPv4_TIME_TO_LIVE_MAX       0xFF
#define IPv4_PROTOCOL_TCP           0x06
#define IPv4_CHECKSUM_UNUSED        0x0000
#define TCP_HOST_PORT               50000
#define TCP_TPM_PORT                2321 /* required by TPM 2.0 dissector */
#define TCP_FLAGS_ACK               0x10
#define TCP_WINDOW_SIZE_MAX         0xFFFF
#define TCP_CHECKSUM_UNUSED         0x0000
#define TCP_URGENT_PTR_UNUSED       0x0000

#define SIZEOF_IN_OCTETS(x)         (sizeof (x)/sizeof (uint32_t))
#define TO_MULTIPLE_OF_4_BYTE(x)    (((x)-1)/4*4+4) * !!(x)

/*
 * complies to pcap-ng (IETF RFC draft-tuexen-opsawg-pcapng-01)
 * https://tools.ietf.org/id/draft-tuexen-opsawg-pcapng-01.html
 *
 * pcap-ng file stucture:
 *
 *  * section header block          (shb)           |<-- file header
 *  * interface statistics block    (idb)           |
 *
 *  * - enhanced packet block       (epb)           |<-- single tpm req. or rsp.
 *    | * header                    (epb_header)    |
 *    | * - ip package                              |
 *    |   | * header                (ip_header)     |
 *    |   | * - tcp package                         |
 *    |   |   | * header            (tcp_header)    |
 *    |   -   - * tpm req. or resp.                 |
 *    - * footer                    (epb_footer)    |
 */

/* section header block */
typedef struct __attribute__((packed)) {
    uint32_t block_type;
    uint32_t block_len;
    uint32_t byte_order_magic;
    uint16_t major_version;
    uint16_t minor_version;
    uint64_t section_len;
    /* options (optional) */
    uint32_t block_len_cp;
} shb;

/* interface description block */
typedef struct __attribute__((packed)) {
    uint32_t block_type;
    uint32_t block_len;
    uint16_t link_type;
    uint16_t reserved;
    uint32_t snap_len;
    /* options (optional) */
    uint32_t block_len_cp;
} idb;


/* enhanced packet block */
typedef struct __attribute__((packed)) {
    uint32_t block_type;
    uint32_t block_len;
    uint32_t interface_id;
    uint32_t timestamp_high;
    uint32_t timestamp_low;
    uint32_t captured_packet_len;
    uint32_t original_packet_len;
} epb_header;

typedef struct __attribute__((packed)) {
    /* options (optional) */
    uint32_t block_len_cp;
} epb_footer;

/* ipv4 packet */
typedef struct __attribute__((packed)) {
    uint8_t version_header_len;
    uint8_t type_of_service;
    uint16_t packet_len;
    uint16_t id;
    uint16_t flags;
    uint8_t time_to_live;
    uint8_t protocol;
    uint16_t checksum;
    uint32_t source;
    uint32_t destination;
    /* options (optional) */
} ip_header;

/* tcp segment */
typedef struct __attribute__((packed)) {
    uint16_t source_port;
    uint16_t destination_port;
    uint32_t seq_no;
    uint32_t ack_no;
    uint16_t header_len_flags;
    uint16_t window_size;
    uint16_t checksum;
    uint16_t urgent_ptr;
    /* options (optional) */
} tcp_header;

static int
pcap_write_section_header_block (
    pcap_buider_ctx *ctx,
    void *buf,
    size_t buf_len);

static int
pcap_write_interface_description_block (
    pcap_buider_ctx *ctx,
    void *buf,
    size_t buf_len);

static int
pcap_write_enhanced_packet_block (
    pcap_buider_ctx *ctx,
    void* buf,
    size_t buf_len,
    const void* payload,
    size_t payload_len,
    int direction);

static int
pcap_write_ip_packet (
    pcap_buider_ctx *ctx,
    void* buf,
    size_t buf_len,
    const void* payload,
    size_t payload_len,
    int direction);

static int
pcap_write_tcp_segment (
    pcap_buider_ctx *ctx,
    void* buf,
    size_t buf_len,
    const void* payload,
    size_t payload_len,
    int direction);

int
pcap_init (pcap_buider_ctx *ctx)
{
    char *filename = getenv (ENV_PCAP_FILE);
    struct timespec time;
    size_t buf_len;
    size_t offset;
    size_t uret;
    int ret;

    if (filename == NULL) {
        LOG_TRACE (ENV_PCAP_FILE " not set. Using default PCAP file: "
                   DEFAULT_PCAP_FILE);
        filename = DEFAULT_PCAP_FILE;
    }

    clock_gettime(CLOCK_MONOTONIC_RAW, &time);
    srand (time.tv_nsec);

    /* random ips to associate unique connection with this tcti instance */
    ctx->ip_host = (rand() << 16) | rand();
    ctx->ip_tpm = (rand() << 16) | rand();

    /* random sequence numbers */
    ctx->tcp_sequence_no_host = rand();
    ctx->tcp_sequence_no_tpm = rand();

    if (!strcmp (filename, "stdout") || !strcmp (filename, "-")) {
        ctx->fd = STDOUT_FILENO;
    } else if (!strcmp (filename, "stderr")) {
        ctx->fd = STDERR_FILENO;
    } else {
        ctx->fd = open (filename, O_WRONLY | O_APPEND | O_CREAT | O_NONBLOCK, 0644);
        if(ctx->fd < 0) {
            LOG_ERROR ("Failed to open file %s: %s", filename, strerror (errno));
            goto error;
        }
    }

    uint8_t buf[sizeof (shb) + sizeof (idb)];
    buf_len = sizeof (buf);
    offset = 0;

    ret = pcap_write_section_header_block (ctx, buf, buf_len);
    if (ret < 0) {
        return ret;
    }
    offset += ret;

    ret = pcap_write_interface_description_block (ctx,
                                                  buf + offset,
                                                  buf_len - offset);
    if (ret < 0) {
        return ret;
    }
    offset += ret;

    /* write file header: SHB and IDB (can be written multiple times to same file) */
    uret = write_all (ctx->fd, buf, offset);
    if (uret != offset) {
        LOG_ERROR ("Failed to write to file %s: %s", filename, strerror (errno));
        goto error;
    }

    return 0;

error:
    pcap_deinit (ctx);
    return -1;
}

int
pcap_print (
    pcap_buider_ctx *ctx,
    const void* payload,
    size_t payload_len,
    int direction)
{
    size_t pdu_len;
    size_t uret;
    int ret;

    if (!payload) {
        return -1;
    }

    /* get required buffer size */
    ret = pcap_write_enhanced_packet_block (ctx, NULL, 0,
                                            payload, payload_len, direction);
    if (ret < 0) {
        return ret;
    }
    pdu_len = ret;

    uint8_t *buf = malloc (pdu_len);
    if (!buf) {
        LOG_ERROR ("Out of memory");
        return -1;
    }

    ret = pcap_write_enhanced_packet_block (ctx, buf, pdu_len,
                                            payload, payload_len, direction);
    if (ret < 0) {
        goto cleanup;
    }
    pdu_len = ret;

    uret = write_all (ctx->fd, buf, pdu_len);
    if (uret != pdu_len) {
        LOG_ERROR ("Failed to write to file: %s", strerror (errno));
        ret = -1;
        goto cleanup;
    }

    ret = 0;

cleanup:
    free (buf);
    return ret;
}

void
pcap_deinit (pcap_buider_ctx *ctx)
{
    int ret;

    if (ctx->fd != STDOUT_FILENO && ctx->fd != STDERR_FILENO) {
        ret = close (ctx->fd);
        if (ret != 0) {
            LOG_WARNING ("Failed to close file: %s", strerror (errno));
        }
    }
}

static int
pcap_write_section_header_block (
    pcap_buider_ctx *ctx,
    void *buf,
    size_t buf_len)
{
    UNUSED (ctx);

    if (buf) {
        if (buf_len < sizeof (shb)) {
            return -1;
        }

        shb section_header = {
            .block_type = PCAP_BLOCK_TYPE_SHB,
            .block_len = sizeof (shb),
            .byte_order_magic = PCAP_SHB_BYTE_ORDER_MAGIC,
            .major_version = PCAP_MAJOR,
            .minor_version = PCAP_MINOR,
            .section_len = PCAP_SHB_SECTION_LEN_NOT_SPECIFIED,
            .block_len_cp = sizeof (shb),
        };

        memcpy (buf, &section_header, sizeof (shb));
    }

    return sizeof (shb);
}

static int
pcap_write_interface_description_block (
    pcap_buider_ctx *ctx,
    void *buf,
    size_t buf_len)
{
    UNUSED (ctx);

    if (buf) {
        if (buf_len < sizeof (idb)) {
            return -1;
        }

        idb interface_description = {
            .block_type = PCAP_BLOCK_TYPE_IDB,
            .block_len = sizeof (idb),
            .link_type = PCAP_IDB_LINKTYPE_IPv4,
            .reserved = 0,
            .snap_len = PCAP_IDB_SNAP_LEN_NO_LIMIT,
            .block_len_cp = sizeof (idb),
        };

        memcpy (buf, &interface_description, sizeof (idb));
    }

    return sizeof (ip_header);
}

static int
pcap_write_enhanced_packet_block (
    pcap_buider_ctx *ctx,
    void* buf,
    size_t buf_len,
    const void* payload,
    size_t payload_len,
    int direction)
{
    UNUSED (ctx);

    size_t pdu_len, sdu_len, sdu_padded_len;
    struct timespec ts;
    uint64_t timestamp;
    int ret;

    ret = clock_gettime (CLOCK_REALTIME, &ts);
    if (ret != 0) {
        LOG_WARNING ("Failed to get time: %s", strerror (errno));
        ts.tv_sec = 0;
        ts.tv_nsec = 0;
    }
    timestamp = (uint64_t) ts.tv_sec*1000000 + ts.tv_nsec/1000;

    /* get ip packet size */
    sdu_len = pcap_write_ip_packet (ctx, NULL, 0,
                                         payload, payload_len,
                                         direction);

    /* apply padding (multiple of 4 bytes) */
    sdu_padded_len = TO_MULTIPLE_OF_4_BYTE (sdu_len);

    pdu_len = sizeof (epb_header) + sdu_padded_len + sizeof (epb_footer);

    epb_header header = {
        .block_type = PCAP_BLOCK_TYPE_EPB,
        .block_len = pdu_len,
        .interface_id = PCAP_EPB_INTERFACE_ID,
        .timestamp_high = (timestamp >> 32) & 0xFFFFFFFF,
        .timestamp_low = timestamp & 0xFFFFFFFF,
        .captured_packet_len = sdu_len,
        .original_packet_len = sdu_len,
    };

    epb_footer footer = {
        .block_len_cp = pdu_len,
    };

    if (buf) {
        if (buf_len < pdu_len) {
            return -1;
        }

        memcpy (buf, &header, sizeof (epb_header));
        buf += sizeof (epb_header);
        pcap_write_ip_packet (ctx, buf, sdu_len,
                              payload, payload_len,
                              direction);
        buf += sdu_len;
        memset (buf, 0x00, sdu_padded_len - sdu_len);
        buf += (sdu_padded_len - sdu_len);
        memcpy (buf, &footer, sizeof (epb_footer));
    }

    return pdu_len;
}

static int
pcap_write_ip_packet (
    pcap_buider_ctx *ctx,
    void* buf,
    size_t buf_len,
    const void* payload,
    size_t payload_len,
    int direction)
{
    size_t pdu_len, sdu_len;

    /* get tcp frame size */
    sdu_len = pcap_write_tcp_segment (ctx, NULL, 0,
                                      payload, payload_len,
                                      direction);

    pdu_len = sizeof (ip_header) + sdu_len;

    ip_header header = {
        .version_header_len = (IPv4_VERSION << 4) | SIZEOF_IN_OCTETS (ip_header),
        .type_of_service = htons (IPv4_TOS_BEST_EFFORT),
        .packet_len = htons (pdu_len),
        .id = htons (IPv4_ID_UNUSED),
        .flags = htons (IPv4_FLAGS_DONT_FRAGMENT << 13 | IPv4_FRAGMENT_OFFSET_UNUSED),
        .time_to_live = IPv4_TIME_TO_LIVE_MAX,
        .protocol = IPv4_PROTOCOL_TCP,
        .checksum = htons (IPv4_CHECKSUM_UNUSED),
    };

    if (direction == PCAP_DIR_HOST_TO_TPM) {
        header.source = htonl (ctx->ip_host);
        header.destination = htonl (ctx->ip_tpm);
    } else if (direction == PCAP_DIR_TPM_TO_HOST) {
        header.source = htonl (ctx->ip_tpm);
        header.destination = htonl (ctx->ip_host);
    }

    if (buf) {
        if (buf_len < pdu_len) {
            return -1;
        }

        memcpy (buf, &header, sizeof (ip_header));
        buf += sizeof (ip_header);
        pcap_write_tcp_segment (ctx, buf, sdu_len,
                                payload, payload_len,
                                direction);
    }

    return pdu_len;
}

static int
pcap_write_tcp_segment (
    pcap_buider_ctx *ctx,
    void* buf,
    size_t buf_len,
    const void* payload,
    size_t payload_len,
    int direction)
{
    size_t pdu_len;

    pdu_len = sizeof (tcp_header) + payload_len;

    tcp_header header = {
        .header_len_flags = htons ((SIZEOF_IN_OCTETS (tcp_header) << 12) | TCP_FLAGS_ACK),
        .window_size = htons (TCP_WINDOW_SIZE_MAX),
        .checksum = htons (TCP_CHECKSUM_UNUSED),
        .urgent_ptr = htons (TCP_URGENT_PTR_UNUSED),
    };

    if (direction == PCAP_DIR_HOST_TO_TPM) {
        header.source_port = htons (TCP_HOST_PORT);
        header.destination_port = htons (TCP_TPM_PORT);
        header.seq_no = htonl (ctx->tcp_sequence_no_host);
        header.ack_no = htonl (ctx->tcp_sequence_no_tpm);
    } else if (direction == PCAP_DIR_TPM_TO_HOST) {
        header.source_port = htons (TCP_TPM_PORT);
        header.destination_port = htons (TCP_HOST_PORT);
        header.seq_no = htonl (ctx->tcp_sequence_no_tpm);
        header.ack_no = htonl (ctx->tcp_sequence_no_host);
    }

    if (buf) {
        if (buf_len < pdu_len) {
            return -1;
        }
        if (payload_len > 0 && payload == NULL) {
            return -1;
        }

        memcpy (buf, &header, sizeof (tcp_header));
        buf += sizeof (tcp_header);
        memcpy (buf, payload, payload_len);

        if (direction == PCAP_DIR_HOST_TO_TPM) {
            ctx->tcp_sequence_no_host += payload_len;
            /* SYN, FIN flags would increment the seq. no. but are not implemented */
        } else if (direction == PCAP_DIR_TPM_TO_HOST) {
            ctx->tcp_sequence_no_tpm += payload_len;
            /* SYN, FIN flags would increment the seq. no. but are not implemented */
        }
    }

    return pdu_len;
}
