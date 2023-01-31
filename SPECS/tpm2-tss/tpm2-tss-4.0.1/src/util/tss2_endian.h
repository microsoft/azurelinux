/* SPDX-License-Identifier: BSD-2-Clause */
/***********************************************************************;
 * Copyright (c) 2015 - 2017, Intel Corporation
 *
 * All rights reserved.
 ***********************************************************************/

#ifndef TSS2_ENDIAN_H
#define TSS2_ENDIAN_H

#if defined(__linux__) || defined(__unix__)
#if defined(__FreeBSD__)
#include <sys/endian.h>
#else
#include <endian.h>
#endif

#define HOST_TO_BE_16(value) htobe16(value)
#define HOST_TO_BE_32(value) htobe32(value)
#define HOST_TO_BE_64(value) htobe64(value)
#define BE_TO_HOST_16(value) be16toh(value)
#define BE_TO_HOST_32(value) be32toh(value)
#define BE_TO_HOST_64(value) be64toh(value)

#else /* linux || unix */

#if defined(WORDS_BIGENDIAN)

#define HOST_TO_BE_16(value) (value)
#define HOST_TO_BE_32(value) (value)
#define HOST_TO_BE_64(value) (value)
#define BE_TO_HOST_16(value) (value)
#define BE_TO_HOST_32(value) (value)
#define BE_TO_HOST_64(value) (value)

#else
#include <stdint.h>

static inline uint16_t endian_conv_16(uint16_t value)
{
    return ((value & (0xff))      << 8) | \
           ((value & (0xff << 8)) >> 8);
}

static inline uint32_t endian_conv_32(uint32_t value)
{
    return ((value & (0xff))       << 24) | \
           ((value & (0xff << 8))  << 8)  | \
           ((value & (0xff << 16)) >> 8)  | \
           ((value & (0xff << 24)) >> 24);
}

static inline uint64_t endian_conv_64(uint64_t value)
{
    return ((value & (0xffULL))       << 56) | \
           ((value & (0xffULL << 8))  << 40) | \
           ((value & (0xffULL << 16)) << 24) | \
           ((value & (0xffULL << 24)) << 8)  | \
           ((value & (0xffULL << 32)) >> 8)  | \
           ((value & (0xffULL << 40)) >> 24) | \
           ((value & (0xffULL << 48)) >> 40) | \
           ((value & (0xffULL << 56)) >> 56);
}

#define HOST_TO_BE_16(value) endian_conv_16(value)
#define HOST_TO_BE_32(value) endian_conv_32(value)
#define HOST_TO_BE_64(value) endian_conv_64(value)
#define BE_TO_HOST_16(value) endian_conv_16(value)
#define BE_TO_HOST_32(value) endian_conv_32(value)
#define BE_TO_HOST_64(value) endian_conv_64(value)

#endif /* WORDS_BIGENDIAN */
#endif /* linux || unix */
#endif /* TSS2_ENDIAN_H */
