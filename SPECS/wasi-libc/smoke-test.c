// SPDX-FileCopyrightText: 2023 Jan Staněk <jstanek@redhat.com>
//
// SPDX-License-Identifier: MIT
//
// Basic string manipulation and IO to test that wasi-libc works at all.

#define _POSIX_C_SOURCE 200809L

#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static const size_t MAX_MESSAGE_LEN = 32;
static const char * const MESSAGE = "smoke-test-ok";

int main(void) {
    errno = 0;

    char *buffer = calloc(strnlen(MESSAGE, MAX_MESSAGE_LEN), sizeof(char));
    if (!buffer) {
        errno = 255;
        goto cleanup;
    }

    strncpy(buffer, MESSAGE, MAX_MESSAGE_LEN);
    printf("%s\n", buffer);

cleanup:
    free(buffer), buffer = NULL;
    return errno;
}
