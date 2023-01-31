/* SPDX-License-Identifier: BSD-2-Clause */
#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <string.h>
#include <stdio.h>
#include <stdarg.h>
#include <stdlib.h>
#include <ctype.h>
#include <errno.h>

#define LOGMODULE log
#include "log.h"

#if !defined(_MSC_VER) || defined(__INTEL_COMPILER)
#define likely(x)       __builtin_expect(!!(x), 1)
#define unlikely(x)     __builtin_expect(!!(x), 0)
#else
/* Microsoft Visual Studio gives internal error C1001 with _builtin_expect */
#define likely(x)       (x)
#define unlikely(x)     (x)
#endif

#if MAXLOGLEVEL != LOGL_NONE

static const char *log_strings[] = {
    "none",
    "(unused)",
    "ERROR",
    "WARNING",
    "info",
    "debug",
    "trace"
};

/**
 * Compares two strings byte by byte and ignores the
 * character's case. Stops at the n-th byte of both
 * strings.
 *
 * This is basically a replacement of the POSIX-function
 * _strncasecmp_. Since tpm2-tss is supposed to be compatible
 * with ISO C99 and not with POSIX, _strncasecmp_ had to be
 * replaced. This function creates lowercase representations
 * of the strings and compares them bytewise.
 *
 * @param string1 The first of the two strings to compare
 * @param string2 The second of the two strings to compare
 * @param n The maximum number of bytes to compare
 * @return 0 if both strings are equal (case insensitive),
 *  an integer greater than zero if string1 is greater than
 *  string 2 and an integer smaller than zero if string1 is
 *  smaller than string2
 *
 */
static int
case_insensitive_strncmp(const char *string1,
        const char *string2,
        size_t n)
{
    if ((string1 == NULL) && (string2 == NULL)) {
        return 0;
    }
    if ((string1 == NULL) && (string2 != NULL)) {
        return -1;
    }
    if ((string1 != NULL) && (string2 == NULL)) {
        return 1;
    }
    if (n == 0) { // Zero bytes are always equal
        return 0;
    }
    if (string1 == string2) { // return equal if they point to same location
        return 0;
    }

    int result;
    do {
        result = tolower((unsigned char) *string1) - tolower((unsigned char) *string2);
        if (result != 0) {
                break;
        }
    } while (*string1++ != '\0' && *string2++ != '\0' && --n );
    return result;
}

static log_level
getLogLevel(const char *module, log_level logdefault);

static FILE *
getLogFile(void)
{
#ifdef LOG_FILE_ENABLED
    const char *envpath;
    static FILE *file = NULL;

    if (file) {
        return file;
    }

    envpath = getenv("TSS2_LOGFILE");
    if (envpath == NULL  || !case_insensitive_strncmp(envpath, "stderr", 7)) {
        file = stderr;
    } else if (!strcmp(envpath, "-") || !case_insensitive_strncmp(envpath, "stdout", 7)) {
        file = stdout;
    } else {
        file = fopen(envpath, "a+");
        if (file == NULL) {
            file = stderr;
            fprintf(file, "Failed to open logging file %s: %s\n", envpath, strerror(errno));
            fflush(file);
        }
    }

    return file;
#else
    return stderr;
#endif
}

void
doLogBlob(log_level loglevel, const char *module, log_level logdefault,
           log_level *status,
           const char *file, const char *func, int line,
           const uint8_t *blob, size_t size, const char *fmt, ...)
{
    FILE *logfile;
    if (unlikely(*status == LOGLEVEL_UNDEFINED))
        *status = getLogLevel(module, logdefault);
    if (loglevel > *status)
        return;

    va_list vaargs;
    va_start(vaargs, fmt);
    /* TODO: Unfortunately, vsnprintf(NULL, 0, ...) do not behave the same as
       snprintf(NULL, 0, ...). Until there is an alternative, messages on
       logblob are restricted to 255 characters
    int msg_len = vsnprintf(NULL, 0, fmt, vaargs); */
    int msg_len = 255;
    char msg[msg_len+1];
    vsnprintf(msg, sizeof(msg), fmt, vaargs);
    va_end(vaargs);

    if (!blob) {
        doLog(loglevel, module, logdefault, status, file, func, line,
              "%s (size=%zi): (null)", msg, size);
	return;
    }

    doLog(loglevel, module, logdefault, status, file, func, line,
          "%s (size=%zi):", msg, size);

    unsigned int i, y, x, off, off2;
    unsigned int width = 16;
#define LINE_LEN 64
    char buffer[LINE_LEN];

    for (i = 1, off = 0, off2 = 0; i <= size; i++) {
        if (i == 1) {
            sprintf(&buffer[off], "%04x: ", i - 1);
            off += 6;
        }

        /* data output */
        sprintf(&buffer[off], "%02x", blob[i-1]);
        off += 2;

        /* ASCII output */
        if ((i % width == 0 && i > 1) || i == size) {
            sprintf(&buffer[off], "  ");
            off += 2;
            /* Align to the right */
            for (x = off; x < width * 2 + 8; x++) {
                sprintf(&buffer[off], " ");
                off++;
            }

            /* Account for a line that is not 'full' */
            unsigned int less = width - (i % width);
            if (less == width)
                less = 0;

            for (y = 0; y < width - less; y++) {
                if (isgraph(blob[off2 + y])) {
                    sprintf(&buffer[y + off], "%c", blob[off2 + y]);
                } else {
                    sprintf(&buffer[y + off], "%c", '.');
                }
            }
            /* print the line and restart */
            logfile = getLogFile();
            fprintf (logfile, "%s\n", buffer);
            fflush(logfile);
            off2 = i;
            off = 0;
            memset(buffer, '\0', LINE_LEN);
            sprintf(&buffer[off], "%04x: ", i);
            off += 6;
        }
    }
}

void
doLog(log_level loglevel, const char *module, log_level logdefault,
           log_level *status,
           const char *file, const char *func, int line,
           const char *msg, ...)
{
    FILE *logfile;
    if (unlikely(*status == LOGLEVEL_UNDEFINED))
        *status = getLogLevel(module, logdefault);

    if (loglevel > *status)
        return;

    int size = snprintf(NULL, 0, "%s:%s:%s:%d:%s() %s \n",
                log_strings[loglevel], module, file, line, func, msg);
    char fmt[size+1];
    snprintf(fmt, sizeof(fmt), "%s:%s:%s:%d:%s() %s \n",
                log_strings[loglevel], module, file, line, func, msg);

    va_list vaargs;
    va_start(vaargs, msg);
    logfile = getLogFile();
    vfprintf (logfile, fmt,
        /* log_strings[loglevel], module, file, func, line, */
        vaargs);
    fflush(logfile);
    va_end(vaargs);
}

static log_level
log_stringlevel(const char *n)
{
    log_level i;
    for(i = 0; i < sizeof(log_strings)/sizeof(log_strings[0]); i++) {
        if (case_insensitive_strncmp(log_strings[i], n, strlen(log_strings[i])) == 0) {
            return i;
        }
    }
    return LOGLEVEL_UNDEFINED;
}

static log_level
getLogLevel(const char *module, log_level logdefault)
{
    log_level loglevel = logdefault;
    const char *envlevel = getenv("TSS2_LOG");
    const char *i = envlevel;
    if (envlevel == NULL)
        return loglevel;
    while ((i = strchr(i, '+')) != NULL) {
        if ((envlevel <= i - strlen("all") &&
	     case_insensitive_strncmp(i - 3, "all", 3) == 0) ||
            (envlevel <= i - strlen(module) &&
             case_insensitive_strncmp(i - strlen(module), module, strlen(module)) == 0)) {
            log_level tmp = log_stringlevel(i+1);
            if (tmp != LOGLEVEL_UNDEFINED)
                loglevel = tmp;
        }
        i = i + 1;
    }
    return loglevel;
}
#endif
