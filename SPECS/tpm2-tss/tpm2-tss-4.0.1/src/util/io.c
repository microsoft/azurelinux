/* SPDX-License-Identifier: BSD-2-Clause */
/*
 * Copyright (c) 2015 - 2018 Intel Corporation
 * All rights reserved.
 */
#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <errno.h>
#include <fcntl.h>
#include <inttypes.h>
#include <limits.h>
#include <string.h>
#include <stdio.h>

#ifndef _WIN32
#include <poll.h>
#include <netdb.h>
#include <netinet/in.h>
#include <unistd.h>
#endif

#include "tss2_tpm2_types.h"

#include "io.h"
#define LOGMODULE tcti
#include "util/log.h"

#define MAX_PORT_STR_LEN    sizeof("65535")

/* sockaddr_un::sun_path is documented as char[108], but it seems safer to let
 * the compiler (or rather, the headers) derive this for us. (Cast to int to
 * avoid signed/unsigned comparison warnings.) */
#define MAX_SADDR_UN_PATH  (int)sizeof(((struct sockaddr_un *)0)->sun_path)

/*
 * The 'read_all' function attempts to read all of the 'size' bytes requested
 * from the 'fd' provided into the buffer 'data'. This function will continue
 * to retry after temporary failures and "short reads". It will only stop
 * once all of the requested data has been read, an error occurs, or EOF.
 * On error or EOF, the number of bytes read (if any) will be returned.
 */
ssize_t
read_all (
    SOCKET fd,
    uint8_t *data,
    size_t size)
{
    ssize_t recvd;
    size_t recvd_total = 0;

    LOG_DEBUG ("reading %zu bytes from fd %d to buffer at 0x%" PRIxPTR,
               size, fd, (uintptr_t)data);
    do {
#ifdef _WIN32
        TEMP_RETRY (recvd, recv (fd, (char *) &data [recvd_total], size, 0));
        if (recvd < 0) {
            LOG_WARNING ("read on fd %d failed with errno %d: %s",
                         fd, WSAGetLastError(), strerror (WSAGetLastError()));
            return recvd_total;
        }
#else
        TEMP_RETRY (recvd, read (fd, &data [recvd_total], size));
        if (recvd < 0) {
            LOG_WARNING ("read on fd %d failed with errno %d: %s",
                         fd, errno, strerror (errno));
            return recvd_total;
        }
#endif
        if (recvd == 0) {
            LOG_WARNING ("Attempted read %zu bytes from fd %d, but EOF "
                         "returned", size, fd);
            return recvd_total;
        }
        LOGBLOB_DEBUG (&data [recvd_total], recvd, "read %zd bytes from fd %d:", recvd, fd);
        recvd_total += recvd;
        size -= recvd;
    } while (size > 0);

    return recvd_total;
}

ssize_t
write_all (
    SOCKET fd,
    const uint8_t *buf,
    size_t size)
{
    ssize_t written = 0;
    size_t written_total = 0;

    do {
        LOG_DEBUG("writing %zu bytes starting at 0x%" PRIxPTR " to fd %d",
                  size - written_total,
                  (uintptr_t)(buf + written_total),
                  fd);
#ifdef _WIN32
        TEMP_RETRY (written, send (fd,
                                   (const char*)&buf [written_total],
                                   size - written_total, 0));
#else
         TEMP_RETRY (written, write (fd,
                                     (const char*)&buf [written_total],
                                     size - written_total));
#endif
        if (written >= 0) {
            LOG_DEBUG ("wrote %zd bytes to fd %d", written, fd);
            written_total += (size_t)written;
        } else {
#ifdef _WIN32
            LOG_ERROR ("failed to write to fd %d: %s", fd, strerror (WSAGetLastError()));
#else
            LOG_ERROR ("failed to write to fd %d: %s", fd, strerror (errno));
#endif
            return written_total;
        }
    } while (written_total < size);

    return (ssize_t)written_total;
}

ssize_t
socket_recv_buf (
    SOCKET sock,
    uint8_t *data,
    size_t size)
{
    return read_all (sock, data, size);
}

TSS2_RC
socket_xmit_buf (
    SOCKET sock,
    const void *buf,
    size_t size)
{
    int ret;

    LOGBLOB_DEBUG (buf, size, "Writing %zu bytes to socket %d:", size, sock);
    ret = write_all (sock, buf, size);
    if (ret < (ssize_t) size) {
#ifdef _WIN32
        LOG_ERROR ("write to fd %d failed, errno %d: %s", sock, WSAGetLastError(), strerror (WSAGetLastError()));
#else
        LOG_ERROR ("write to fd %d failed, errno %d: %s", sock, errno, strerror (errno));
#endif
        return TSS2_TCTI_RC_IO_ERROR;
    }
    return TSS2_RC_SUCCESS;
}

TSS2_RC
socket_close (
    SOCKET *socket)
{
    int ret;

    if (socket == NULL) {
        return TSS2_TCTI_RC_BAD_REFERENCE;
    }
    if (*socket == INVALID_SOCKET) {
        return TSS2_RC_SUCCESS;
    }
#ifdef _WIN32
    ret = closesocket (*socket);
    WSACleanup();
    if (ret == SOCKET_ERROR) {
        LOG_WARNING ("Failed to close SOCKET %d. errno %d: %s",
                     *socket, WSAGetLastError(), strerror (WSAGetLastError()));
        return TSS2_TCTI_RC_IO_ERROR;
    }
#else
    ret = close (*socket);
    if (ret == SOCKET_ERROR) {
        LOG_WARNING ("Failed to close SOCKET %d. errno %d: %s",
                     *socket, errno, strerror (errno));
        return TSS2_TCTI_RC_IO_ERROR;
    }
#endif
    *socket = INVALID_SOCKET;

    return TSS2_RC_SUCCESS;
}

TSS2_RC
socket_connect (
    const char *hostname,
    uint16_t port,
    int control,
    SOCKET *sock)
{
    static const struct addrinfo hints = { .ai_socktype = SOCK_STREAM,
        .ai_family = AF_UNSPEC, .ai_protocol = IPPROTO_TCP};
    struct addrinfo *retp = NULL;
    struct addrinfo *p;
    char port_str[MAX_PORT_STR_LEN];
    int ret = 0;
#ifdef _WIN32
    char host_buff[_HOST_NAME_MAX];
    const char *h = hostname;
    WSADATA wsaData;
    int iResult;
    iResult = WSAStartup(MAKEWORD(2, 2), &wsaData);
    if (iResult != 0) {
        LOG_WARNING("WSAStartup failed: %d", iResult);
        return TSS2_TCTI_RC_IO_ERROR;
    }
#else
    char host_buff[_HOST_NAME_MAX] __attribute__((unused));
    const char *h __attribute__((unused)) = hostname;
#endif

    if (hostname == NULL || sock == NULL) {
        return TSS2_TCTI_RC_BAD_REFERENCE;
    }

    if (control)
        port++;

    ret = snprintf(port_str, sizeof(port_str), "%u", port);
    if (ret < 0)
        return TSS2_TCTI_RC_BAD_VALUE;


    LOG_DEBUG ("Resolving host %s", hostname);
    ret = getaddrinfo (hostname, port_str, &hints, &retp);
    if (ret != 0) {
        LOG_WARNING ("Host %s does not resolve to a valid address: %d: %s",
            hostname, ret, gai_strerror(ret));
        return TSS2_TCTI_RC_IO_ERROR;
    }

    for (p = retp; p != NULL; p = p->ai_next) {
        *sock = socket (p->ai_family, SOCK_STREAM, 0);
        void *sockaddr;

        if (*sock == INVALID_SOCKET)
            continue;

        if (p->ai_family == AF_INET)
            sockaddr = &((struct sockaddr_in*)p->ai_addr)->sin_addr;
        else
            sockaddr = &((struct sockaddr_in6*)p->ai_addr)->sin6_addr;

        h = inet_ntop(p->ai_family, sockaddr, host_buff, sizeof(host_buff));

        if (h == NULL)
            h = hostname;

        LOG_DEBUG ("Attempting TCP connection to host %s, port %s", h, port_str);
        if (connect (*sock, p->ai_addr, p->ai_addrlen) != SOCKET_ERROR)
            break; /* socket connected OK */
        socket_close (sock);
    }
    freeaddrinfo (retp);
    if (p == NULL) {
#ifdef _WIN32
        LOG_WARNING ("Failed to connect to host %s, port %s: errno %d: %s",
                      h, port_str, WSAGetLastError(), strerror (WSAGetLastError()));
#else
        LOG_WARNING ("Failed to connect to host %s, port %s: errno %d: %s",
                     h, port_str, errno, strerror (errno));
#endif

        return TSS2_TCTI_RC_IO_ERROR;
    }

    return TSS2_RC_SUCCESS;
}

TSS2_RC
socket_connect_unix (
    const char *path,
    int control,
    SOCKET *sock)
{
#ifdef _WIN32
    return TSS2_TCTI_RC_BAD_REFERENCE;
#else
    struct sockaddr_un saddr;

    if (path == NULL)
        return TSS2_TCTI_RC_BAD_REFERENCE;

    saddr.sun_family = AF_UNIX;

    if (snprintf(saddr.sun_path, MAX_SADDR_UN_PATH,
                 control ? "%s.ctrl" : "%s", path) >= MAX_SADDR_UN_PATH) {
        LOG_ERROR ("Socket %s%s is too long for AF_UNIX",
                   path, control ? ".ctrl" : "");
        return TSS2_TCTI_RC_BAD_VALUE;
    }

    *sock = socket (AF_UNIX, SOCK_STREAM, 0);

    if (*sock == INVALID_SOCKET) {
        LOG_WARNING ("Failed to create AF_UNIX socket");
        return TSS2_TCTI_RC_IO_ERROR;
    }

    LOG_DEBUG ("Attempting UNIX connection to %s", saddr.sun_path);
    if (connect (*sock, (struct sockaddr *)&saddr, sizeof(saddr)) == SOCKET_ERROR) {
        LOG_WARNING ("Failed to connect to %s", saddr.sun_path);
        return TSS2_TCTI_RC_IO_ERROR;
    }

    return TSS2_RC_SUCCESS;
#endif
}

TSS2_RC
socket_set_nonblock (SOCKET sock)
{
#ifndef _WIN32
    int flgs;

    flgs = fcntl(sock, F_GETFL);
    if (flgs == -1)
        return TSS2_TCTI_RC_IO_ERROR;

    flgs |= O_NONBLOCK;
    if (fcntl(sock, F_SETFL, flgs) != 0)
        return TSS2_TCTI_RC_IO_ERROR;
#endif
    return TSS2_RC_SUCCESS;
}

TSS2_RC
socket_poll (SOCKET sock, int timeout)
{
#ifndef _WIN32
    struct pollfd fds;
    int rc_poll, nfds = 1;

    fds.fd = sock;
    fds.events = POLLIN;

    /* Timeout of 0 ie return immediately is not
     * well handled throughout the upper layers currenty
     * cousing the integration tests to hang randomly.
     * Make the poll to waint to at least 10 ms */
    if (timeout == 0)
        timeout = 10;

    rc_poll = poll(&fds, nfds, timeout);
    if (rc_poll < 0) {
        LOG_ERROR ("Failed to poll for response from fd %d, got errno %d: %s",
                   sock, errno, strerror(errno));
        return TSS2_TCTI_RC_IO_ERROR;
    } else if (rc_poll == 0) {
        LOG_INFO ("Poll timed out on fd %d.", sock);
        return TSS2_TCTI_RC_TRY_AGAIN;
    } else if (fds.revents == POLLIN) {
        return TSS2_RC_SUCCESS;
    }
#endif
    return TSS2_RC_SUCCESS;
}
