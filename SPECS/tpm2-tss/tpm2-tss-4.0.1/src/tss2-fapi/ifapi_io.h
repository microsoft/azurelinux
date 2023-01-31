/* SPDX-License-Identifier: BSD-2-Clause */
/*******************************************************************************
 * Copyright 2018-2019, Fraunhofer SIT sponsored by Infineon Technologies AG
 * All rights reserved.
 ******************************************************************************/

#ifndef IFAPI_IO_H
#define IFAPI_IO_H

#include <stdio.h>
#include <stdbool.h>
#include "tss2_common.h"
#include "tss2_fapi.h"

typedef struct IFAPI_IO {
    FILE *stream;
    short pollevents;
    const char *char_buffer;
    char *char_rbuffer;
    size_t buffer_length;
    size_t buffer_idx;
} IFAPI_IO;

#ifdef TEST_FAPI_ASYNC
#define _IFAPI_IO_RETRIES 1
#else /* TEST_FAPI_ASYNC */
#define _IFAPI_IO_RETRIES 0
#endif /* TEST_FAPI_ASYNC */

static int _ifapi_io_retry __attribute__((unused)) = _IFAPI_IO_RETRIES;

#define IFAPI_IO_STREAM context->io.stream
#define IFAPI_IO_BUFF context->io.char_buffer
#define IFAPI_IO_RBUFF context->io.char_rbuffer
#define IFAPI_IO_BUFFLEN context->io.buffer_length
#define IFAPI_IO_BUFFIDX context->io.buffer_idx

TSS2_RC
ifapi_io_read_async(
    struct IFAPI_IO *io,
    const char *filename);

TSS2_RC
ifapi_io_read_finish(
    struct IFAPI_IO *io,
    uint8_t **buffer,
    size_t *length);

TSS2_RC
ifapi_io_write_async(
    struct IFAPI_IO *io,
    const char *filename,
    const uint8_t *buffer,
    size_t length);

TSS2_RC
ifapi_io_write_finish(
    struct IFAPI_IO *io);

TSS2_RC
ifapi_io_check_file_writeable(
    const char *file);

TSS2_RC
ifapi_io_check_create_dir(
    const char *dirname, int mode);

TSS2_RC
ifapi_io_remove_file(
    const char *file);

TSS2_RC
ifapi_io_remove_directories(
    const char *dirname,
    const char *keystore_path,
    const char *sub_dir);

TSS2_RC
ifapi_io_dirfiles(
    const char *dirname,
    char ***files,
    size_t *numfiles);

TSS2_RC
ifapi_io_dirfiles_all(
    const char *searchPath,
    char ***pathlist,
    size_t *numPaths);

bool
ifapi_io_path_exists(const char *path);

TSS2_RC
ifapi_io_poll(IFAPI_IO * io);

TSS2_RC
ifapi_io_poll_handles(IFAPI_IO *io, FAPI_POLL_HANDLE **handles, size_t *num_handles);

#endif /* IFAPI_IO_H */
