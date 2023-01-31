/* SPDX-License-Identifier: BSD-2-Clause */

#ifndef TCTI_CMD_H
#define TCTI_CMD_H

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <limits.h>

#include "tcti-common.h"
#include "util/io.h"

#define TCTI_CMD_NAME "tcti-cmd"
#define TCTI_CMD_DESCRIPTION "TCTI module for using a process to send and receive data."
#define TCTI_CMD_HELP "string used as command, passed to " \
                "execl(\"/bin/sh\", \"sh\", \"-c\", command, (char *) 0);."

#define TCTI_CMD_MAGIC 0xf05b04cd9f02728dULL

typedef struct TSS2_TCTI_CMD_CONTEXT TSS2_TCTI_CMD_CONTEXT;
struct TSS2_TCTI_CMD_CONTEXT {
    TSS2_TCTI_COMMON_CONTEXT common;
    /* stdin of the subprocess */
    FILE *sink;
    /* stdout of the subprocess */
    FILE *source;
    pid_t child_pid;
};

/*
 * create some wrapper functions so we don't have to mock syscalls with wrap.
 * This can lead to issues with things other than this code making said syscalls,
 * like code coverage. We make them weak functions so we can overide them at link
 * time with wrapped definitions from the unit test main code.
 */
#ifdef UNIT
#define WEAK __attribute__((weak))

WEAK int tcti_cmd_pipe (int pipefd[2]);
WEAK int tcti_cmd_fork (void);
WEAK FILE *tcti_cmd_fdopen (int fd, const char *mode);
WEAK int tcti_cmd_sigprocmask (int how, const sigset_t *set, sigset_t *oldset);
WEAK size_t tcti_cmd_fwrite (const void *ptr, size_t size, size_t nmemb,
        FILE *stream);
WEAK size_t tcti_cmd_fread (void *ptr, size_t size, size_t nmemb, FILE *stream);
WEAK int tcti_cmd_ferror (FILE *stream);
#endif

#endif /* TCTI_CMD_H */
