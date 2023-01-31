/* SPDX-License-Identifier: BSD-2-Clause */
/*
 * Copyright (c) 2015 - 2018 Intel Corporation
 * All rights reserved.
 */
#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <inttypes.h>
#include <limits.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <unistd.h>
#include <signal.h>

#if defined (__FreeBSD__)
#include <sys/procctl.h>
#else
#include <sys/prctl.h>
#endif
#include <sys/types.h>
#include <sys/wait.h>
#include <sys/time.h>

#include "tss2_tcti_cmd.h"

#include "tcti-cmd.h"
#include "tcti-common.h"
#define LOGMODULE tcti
#include "util/log.h"

#define PIPE_READ_END  0
#define PIPE_WRITE_END 1

/* do this as a macro **on one line** so LINENO and everything is preserved */
#define close_fd(fd) do { if (close (fd)) { LOG_WARNING ("Could not close fd (%d): %s", fd, strerror (errno)); } } while (0)

typedef enum child_behavior child_behavior;
enum child_behavior {
    child_behavior_good,
    child_behavior_bad,
    child_behavior_error
};

/*
 * create some wrapper functions so we don't have to mock syscalls with wrap.
 * This can lead to issues with things other than this code making said syscalls,
 * like code coverage.
 */
#ifdef UNIT
/* if not not debug, ie debug */
#define TEST_VISIBILITY
#else
/* production */
#define TEST_VISIBILITY static
#define WEAK
#endif

TEST_VISIBILITY WEAK
int tcti_cmd_pipe (int pipefd[2])
{
    return pipe (pipefd);
}

TEST_VISIBILITY WEAK
int tcti_cmd_fork (void)
{
    return fork ();
}

TEST_VISIBILITY WEAK
FILE * tcti_cmd_fdopen (int fd, const char *mode)
{
    return fdopen (fd, mode);
}

TEST_VISIBILITY WEAK
int tcti_cmd_sigprocmask (int how, const sigset_t *set, sigset_t *oldset)
{
    return sigprocmask (how, set, oldset);
}

TEST_VISIBILITY WEAK
size_t tcti_cmd_fwrite (const void *ptr, size_t size, size_t nmemb,
        FILE *stream)
{
    return fwrite (ptr, size, nmemb, stream);
}

TEST_VISIBILITY WEAK
size_t tcti_cmd_fread (void *ptr, size_t size, size_t nmemb, FILE *stream)
{
    return fread (ptr, size, nmemb, stream);
}

TEST_VISIBILITY WEAK
int tcti_cmd_ferror (FILE *stream)
{
    return ferror (stream);
}

static int
disable_sigchld (void)
{
    sigset_t mask;
    sigemptyset (&mask);
    sigaddset (&mask, SIGCHLD);

    int rc = tcti_cmd_sigprocmask (SIG_BLOCK, &mask, NULL);
    if (rc) {
        rc = errno;
        LOG_ERROR ("sigprocmask failed: %s", strerror (errno));
    }

    return rc;
}

static int
enable_sigchld (void)
{
    sigset_t mask;
    sigemptyset (&mask);
    sigaddset (&mask, SIGCHLD);

    int rc = tcti_cmd_sigprocmask (SIG_UNBLOCK, &mask, NULL);
    if (rc) {
        rc = errno;
        LOG_ERROR ("sigprocmask failed: %s", strerror (errno));
    }

    return rc;
}

static void reap_child (pid_t child_pid)
{
    /* The process may have died, so attempt to reap */
    int wstatus = 0;
    pid_t reaped = waitpid (child_pid, &wstatus, WNOHANG);
    if (reaped > 0) {
        goto reaped_out;
    } else if (reaped < 0) {
        if (errno == ECHILD) {
            /* nothing to reap */
            goto out;
        }
        LOG_WARNING ("Error getting wstatus of pid (%u): %s", reaped,
                strerror (errno));
        /* We'll just try the kill logic anyways */
    }

    /* Ask the process nicely to shut down via SIGTERM, we don't need to reall do anything else
     * but waitpid since shell always does this nicely.
     */
    int rc = kill (child_pid, SIGTERM);
    if (rc < 0) {
        /* can't kill it, why? */
        LOG_ERROR ("Error shutting down pid (%u): %s", child_pid,
                strerror (errno));
        goto out;
    }

    reaped = waitpid (child_pid, &wstatus, 0);
    if (reaped < 0) {
        if (errno != ECHILD) {
            LOG_WARNING ("Could not reap child: %s", strerror (errno));
        }
        /* well we tried, just keep going */
    }

reaped_out:
    LOG_TRACE ("Reaped: %ld", (long int)reaped);

out:
    /* always restore this signal when done, ignore return value */
    (void)enable_sigchld ();
}

static void pipe_close (int pipefd[2])
{
    int rc = errno;
    close (pipefd[0]);
    close (pipefd[1]);
    errno = rc;
}

#if defined (__FreeBSD__)
static int set_exit_with_parent (void)
{
    const int sig = SIGTERM;
    return procctl (P_PID, 0, PROC_PDEATHSIG_CTL, (void *)&sig);
}
#else
static int set_exit_with_parent (void)
{
    return prctl (PR_SET_PDEATHSIG, SIGTERM);
}
#endif

static void __attribute__((__noreturn__))
setup_child_and_exec (int stdin_pipefd[2], int stdout_pipefd[2],
        const char *cmd)
{
    bool close_stdin = false;
    bool close_stdout = false;

    /* ask kernel to deliver SIGTERM in case the parent dies */
    int rc = set_exit_with_parent ();
    if (rc) {
        LOG_ERROR ("Error prctl (PR_SET_PDEATHSIG, SIGTERM): %s",
                strerror (errno));
        goto error;
    }

    rc = enable_sigchld ();
    if (rc) {
        /* Error logged by enable_sigchld () */
        goto error;
    }

    /*
     *  Dup the FD's which sets the stdin and stdout file
     *  descriptors of the child process which will be
     *  inherited across execlp (3).
     */
    rc = dup2(stdin_pipefd[PIPE_READ_END], STDIN_FILENO);
    if (rc < 0) {
        LOG_ERROR ("Error dup2 STDIN: %s", strerror (errno));
        goto error;
    }
    close_stdin = true;

    rc = dup2(stdout_pipefd[PIPE_WRITE_END], STDOUT_FILENO);
    if (rc < 0) {
        LOG_ERROR ("Error dup2 STDOUT: %s", strerror (errno));
        goto error;
    }
    close_stdout = true;

    /*
     * Close unused file descriptor ends
     * The child DOESN't:
     *   - write to stdin
     *   - read from stdout.
     */
    close_fd (stdin_pipefd[PIPE_WRITE_END]);
    close_fd (stdout_pipefd[PIPE_READ_END]);

    /*
     * Modeled after system (3)
     * if this works, execution does not return
     */
    execlp ("/bin/sh", "sh", "-c", cmd, NULL);

    LOG_ERROR (
            "Error execlp (\"/bin/sh\", \"sh\", \"-c\", \"%s\"," " (char*) NULL): %s",
            cmd, strerror (errno));

error:
    /* on error close the std file descriptors as the runtime won't do it */
    close_fd (close_stdin ? STDIN_FILENO : stdin_pipefd[PIPE_READ_END]);
    close_fd (close_stdout ? STDOUT_FILENO : stdout_pipefd[PIPE_WRITE_END]);

    exit (1);
}

/*
 * Returns 0 on success or errno on error.
 */
static int popen_w_pipes (const char *cmd, pid_t *pid, FILE **sink,
        FILE **source)
{

    pid_t _pid = 0;
    int stdout_pipefd[2];
    int stdin_pipefd[2];

    int rc = tcti_cmd_pipe (stdin_pipefd);
    if (rc) {
        rc = errno;
        LOG_ERROR ("Could not open stderr pipe (): %s", strerror (errno));
        return rc;
    }

    rc = tcti_cmd_pipe (stdout_pipefd);
    if (rc) {
        rc = errno;
        LOG_ERROR ("Could not open stderr pipe (): %s", strerror (errno));
        goto error_close_stdin;
    }

    rc = disable_sigchld ();
    if (rc) {
        /* error logged by disable_sigchld () */
        goto error_close_stdin;
    }

    _pid = tcti_cmd_fork ();
    if (_pid == 0) {
        LOG_DEBUG ("Forked child pid: %d", getpid());
        setup_child_and_exec (stdin_pipefd, stdout_pipefd, cmd);
    } else if (_pid < 0) {
        rc = errno;
        LOG_ERROR ("Could not fork (): %s", strerror (errno));
        goto error_close_all;
    }

    /* parent process, fork success */

    /*
     * close the ends of the pipe not used by the parent
     * The parent doesn't need to write to the childs stdout
     * and it doesn't need to read from the
     * stdin stream. So close the proper side of the pipes.
     */
    close_fd (stdin_pipefd[PIPE_READ_END]);
    close_fd (stdout_pipefd[PIPE_WRITE_END]);

    /*
     * make them stdio.h file streams so we don't have to worry
     * about low level IO details.
     */
    *sink = tcti_cmd_fdopen (stdin_pipefd[1], "wb");
    if (!*sink) {
        rc = errno;
        LOG_ERROR ("Could not fdopen sink: %s", strerror (errno));
        goto error_close_all;
    }

    *source = tcti_cmd_fdopen (stdout_pipefd[0], "rb");
    if (!*source) {
        rc = errno;
        LOG_ERROR ("Could not fdopen source: %s", strerror (errno));
        fclose (*sink);
        goto error_close_all;
    }

    rc = setvbuf (*sink, NULL, _IONBF, 0);
    if (rc) {
        LOG_WARNING ("Could not set stdin child pipe to non-buffering: %s",
                strerror (errno));
    }

    rc = setvbuf (*source, NULL, _IONBF, 0);
    if (rc) {
        LOG_WARNING ("Could not set stdout child pipe to non-buffering: %s",
                strerror (errno));
    }

    *pid = _pid;

    /* parent */
    return rc;

error_close_all:
    pipe_close (stdout_pipefd);
error_close_stdin:
    pipe_close (stdin_pipefd);

    *sink = *source = NULL;

    /* The parent had an issue, so reap the child */
    if (_pid > 0) {
        reap_child (_pid);
    }

    return rc;
}

/*
 * This function wraps the "up-cast" of the opaque TCTI context type to the
 * type for the command TCTI context. If passed a NULL context the function
 * returns a NULL ptr. The function doesn't check magic number anymore
 * It should checked by the appropriate tcti_common_checks.
 */
TSS2_TCTI_CMD_CONTEXT*
tcti_cmd_context_cast (TSS2_TCTI_CONTEXT *tcti_ctx)
{
    if (tcti_ctx == NULL)
        return NULL;

    return (TSS2_TCTI_CMD_CONTEXT*) tcti_ctx;
}
/*
 * This function down-casts the cmd TCTI context to the common context
 * defined in the tcti-common module.
 */
TSS2_TCTI_COMMON_CONTEXT*
tcti_cmd_down_cast (TSS2_TCTI_CMD_CONTEXT *tcti_cmd)
{
    if (tcti_cmd == NULL) {
        return NULL;
    }
    return &tcti_cmd->common;
}

TSS2_RC tcti_cmd_transmit (TSS2_TCTI_CONTEXT *tcti_ctx, size_t size,
        const uint8_t *cmd_buf)
{
    TSS2_TCTI_CMD_CONTEXT *tcti_cmd = tcti_cmd_context_cast (tcti_ctx);
    TSS2_TCTI_COMMON_CONTEXT *tcti_common = tcti_cmd_down_cast (tcti_cmd);

    TSS2_RC rc = tcti_common_transmit_checks (tcti_common, cmd_buf,
            TCTI_CMD_MAGIC);
    if (rc != TSS2_RC_SUCCESS) {
        return rc;
    }

    size_t bytes = tcti_cmd_fwrite (cmd_buf, 1, size, tcti_cmd->sink);
    if (tcti_cmd_ferror (tcti_cmd->sink) || bytes != size) {
        LOG_ERROR ("Transmitting to subprocess failed: %s", strerror (errno));
        return TSS2_TCTI_RC_IO_ERROR;
    }

    fflush (tcti_cmd->sink);

    tcti_common->state = TCTI_STATE_RECEIVE;

    return rc;
}

TSS2_RC tcti_cmd_get_poll_handles (TSS2_TCTI_CONTEXT *tctiContext,
        TSS2_TCTI_POLL_HANDLE *handles, size_t *num_handles)
{
    TSS2_TCTI_CMD_CONTEXT *cmd_tcti = tcti_cmd_context_cast (tctiContext);

    if (num_handles == NULL || cmd_tcti == NULL) {
        return TSS2_TCTI_RC_BAD_REFERENCE;
    }

    if (handles != NULL && *num_handles < 1) {
        LOG_ERROR("No handles");
        return TSS2_TCTI_RC_INSUFFICIENT_BUFFER;
    }

    *num_handles = 1;
    if (handles != NULL) {
        handles->fd = fileno (cmd_tcti->source);
        if (handles->fd < 0) {
            LOG_ERROR ("Could not get fileno: %s", strerror (errno));
            return TSS2_TCTI_RC_IO_ERROR;
        }
        handles->events = POLLIN | POLLOUT;
    }

    return TSS2_RC_SUCCESS;
}

void tcti_cmd_finalize (TSS2_TCTI_CONTEXT *tctiContext)
{
    TSS2_TCTI_CMD_CONTEXT *tcti_cmd = tcti_cmd_context_cast (tctiContext);

    if (tcti_cmd == NULL) {
        return;
    }

    reap_child (tcti_cmd->child_pid);

    fclose (tcti_cmd->source);
    fclose (tcti_cmd->sink);
}

TSS2_RC tcti_cmd_receive (TSS2_TCTI_CONTEXT *tctiContext, size_t *response_size,
        unsigned char *response_buffer, int32_t timeout)
{
#ifdef TEST_FAPI_ASYNC
    /* Used for simulating a timeout. */
    static int wait = 0;
#endif
    TSS2_TCTI_CMD_CONTEXT *tcti_cmd = tcti_cmd_context_cast (tctiContext);
    TSS2_TCTI_COMMON_CONTEXT *tcti_common = tcti_cmd_down_cast (tcti_cmd);
    TSS2_RC rc;

    rc = tcti_common_receive_checks (tcti_common, response_size,
    TCTI_CMD_MAGIC);
    if (rc != TSS2_RC_SUCCESS) {
        return rc;
    }

    if (timeout != TSS2_TCTI_TIMEOUT_BLOCK) {
        LOG_TRACE ("Asynchronous I/O not actually implemented.");
#ifdef TEST_FAPI_ASYNC
        if (wait < 1) {
            LOG_TRACE ("Simulating Async by requesting another invocation.");
            wait += 1;
            return TSS2_TCTI_RC_TRY_AGAIN;
        } else {
            LOG_TRACE ("Sending the actual result.");
            wait = 0;
        }
#endif /* TEST_FAPI_ASYNC */
    }

    if (!response_buffer) {
        *response_size = 4096;
        return TSS2_RC_SUCCESS;
    }

    /* block until we have a header or the child closes the pipe */
    size_t size = tcti_cmd_fread (response_buffer, 1, TPM_HEADER_SIZE, tcti_cmd->source);
    rc = tcti_cmd_ferror (tcti_cmd->source);
    if (rc) {
        LOG_ERROR ("Reading from command TCTI: %s", strerror (errno));
        rc = TSS2_TCTI_RC_IO_ERROR;
        goto out;
    }

    if (size != TPM_HEADER_SIZE) {
        LOG_ERROR ("Read was not size of header, got %zu expected %zu",
                size, TPM_HEADER_SIZE);
        rc = TSS2_TCTI_RC_MALFORMED_RESPONSE;
        goto out;
    }

    /*
     * we have a header, get the size field to compute the rest of
     * the data.
     */
    rc = header_unmarshal (response_buffer, &tcti_common->header);
    if (rc) {
        goto out;
    }

    if (tcti_common->header.size < TPM_HEADER_SIZE) {
        LOG_ERROR ("Header response size is less than TPM_HEADER_SIZE,"
                " got %" PRIu32 " expected greater than or equal to %zu",
                tcti_common->header.size, TPM_HEADER_SIZE);
        rc = TSS2_TCTI_RC_MALFORMED_RESPONSE;
        goto out;
    }

    /*
     * Read the remaining data that is past the header size
     */
    size_t data_size = tcti_common->header.size - TPM_HEADER_SIZE;

    size = tcti_cmd_fread (&response_buffer[TPM_HEADER_SIZE], 1, data_size,
            tcti_cmd->source);
    rc = tcti_cmd_ferror (tcti_cmd->source);
    if (rc) {
        rc = errno == EFAULT ?
                TSS2_TCTI_RC_INSUFFICIENT_BUFFER : TSS2_TCTI_RC_IO_ERROR;
        LOG_ERROR ("Reading from command TCTI: %s", strerror (errno));
        goto out;
    }

    if (size != data_size) {
        LOG_ERROR ("Command response body read was not for expected size, "
                "got %zu expected %zu", size, data_size);
        rc = TSS2_TCTI_RC_MALFORMED_RESPONSE;
        goto out;
    }

    *response_size = tcti_common->header.size;

    /*
     * Executing code beyond this point transitions the state machine to
     * TRANSMIT. Another call to this function will not be possible until
     * another command is sent to the TPM.
     */
out:
    tcti_common->header.size = 0;
    tcti_common->state = TCTI_STATE_TRANSMIT;

    return rc;
}

void tcti_cmd_init_context_data (TSS2_TCTI_COMMON_CONTEXT *tcti_common)
{
    TSS2_TCTI_MAGIC (tcti_common) = TCTI_CMD_MAGIC;
    TSS2_TCTI_VERSION (tcti_common) = TCTI_VERSION;
    TSS2_TCTI_TRANSMIT (tcti_common) = tcti_cmd_transmit;
    TSS2_TCTI_RECEIVE (tcti_common) = tcti_cmd_receive;
    TSS2_TCTI_FINALIZE (tcti_common) = tcti_cmd_finalize;
    TSS2_TCTI_GET_POLL_HANDLES (tcti_common) = tcti_cmd_get_poll_handles;
    TSS2_TCTI_MAKE_STICKY (tcti_common) = tcti_make_sticky_not_implemented;
    tcti_common->state = TCTI_STATE_TRANSMIT;
    tcti_common->locality = 0;
    memset (&tcti_common->header, 0, sizeof (tcti_common->header));
}

/*
 * This is an implementation of the standard TCTI initialization function for
 * this module.
 */
TSS2_RC Tss2_Tcti_Cmd_Init (TSS2_TCTI_CONTEXT *tctiContext, size_t *size,
        const char *conf)
{
    TSS2_TCTI_CMD_CONTEXT *tcti_command =
            (TSS2_TCTI_CMD_CONTEXT*) tctiContext;
    TSS2_TCTI_COMMON_CONTEXT *tcti_common = tcti_cmd_down_cast (tcti_command);

    if (size == NULL || conf == NULL) {
        return TSS2_TCTI_RC_BAD_VALUE;
    }

    if (tctiContext == NULL) {
        *size = sizeof (TSS2_TCTI_CMD_CONTEXT);
        return TSS2_RC_SUCCESS;
    }

    LOG_DEBUG ("Initializing command TCTI with command: %s", conf);

    tcti_command->sink = NULL;
    tcti_command->source = NULL;
    tcti_command->child_pid = -1;

    int rc = popen_w_pipes (conf, &tcti_command->child_pid, &tcti_command->sink,
            &tcti_command->source);
    if (rc != 0) {
        LOG_ERROR ("Open subprocess command \"%s\", failed with: %s", conf,
                strerror (rc));
        return TSS2_TCTI_RC_GENERAL_FAILURE;
    }

    tcti_cmd_init_context_data (tcti_common);

    return TSS2_RC_SUCCESS;
}

/* public info structure */
const TSS2_TCTI_INFO tss2_tcti_info = {
        .version = TCTI_VERSION,
        .name = TCTI_CMD_NAME,
        .description = TCTI_CMD_DESCRIPTION,
        .config_help = TCTI_CMD_HELP,
        .init = Tss2_Tcti_Cmd_Init,
};

const TSS2_TCTI_INFO*
Tss2_Tcti_Info (void)
{
    return &tss2_tcti_info;
}
