/* SPDX-License-Identifier: BSD-2-Clause */
#ifndef LOG_H
#define LOG_H

#include <stdint.h>
#include <stddef.h>
#include "util/aux_util.h"

#ifndef LOGMODULE
#error "LOGMODULE must be set before including log/log.h"
#endif

#ifndef LOGDEFAULT
#define LOGDEFAULT LOGLEVEL_WARNING
#endif

#define LOGL_NONE    0
#define LOGL_ERROR   2
#define LOGL_WARNING 3
#define LOGL_INFO    4
#define LOGL_DEBUG   5
#define LOGL_TRACE   6
#define LOGL_UNDEF   0xFF

typedef enum {
    LOGLEVEL_NONE      = LOGL_NONE,
    LOGLEVEL_ERROR     = LOGL_ERROR,
    LOGLEVEL_WARNING   = LOGL_WARNING,
    LOGLEVEL_INFO      = LOGL_INFO,
    LOGLEVEL_DEBUG     = LOGL_DEBUG,
    LOGLEVEL_TRACE     = LOGL_TRACE,
    LOGLEVEL_UNDEFINED = LOGL_UNDEF
} log_level;

#define xstr(s) str(s)
#define str(s) #s

static log_level LOGMODULE_status COMPILER_ATTR(unused) = LOGLEVEL_UNDEFINED;

#ifndef MAXLOGLEVEL
#error "MAXLOGLEVEL undefined"
#endif

#if MAXLOGLEVEL > LOGL_TRACE || MAXLOGLEVEL < LOGL_ERROR
    #if MAXLOGLEVEL != LOGL_NONE
        #error "Unknown MAXLOGLEVEL"
    #endif
#endif

/* MAXLOGLEVEL is Error or "higher" */
#if MAXLOGLEVEL >= LOGL_ERROR
#define LOG_ERROR(FORMAT, ...) doLog(LOGLEVEL_ERROR, \
                                     xstr(LOGMODULE), LOGDEFAULT, \
                                     &LOGMODULE_status, \
                                     __FILE__, __func__, __LINE__, \
                                     FORMAT, ## __VA_ARGS__)
#define LOGBLOB_ERROR(BUFFER, SIZE, FORMAT, ...) doLogBlob(LOGLEVEL_ERROR, \
                                             xstr(LOGMODULE), LOGDEFAULT, \
                                             &LOGMODULE_status, \
                                             __FILE__, __func__, __LINE__, \
                                             BUFFER, SIZE, \
                                             FORMAT, ## __VA_ARGS__)
#else /* MAXLOGLEVEL is not Error or "higher" */
#define LOG_ERROR(FORMAT, ...) {}
#define LOGBLOB_ERROR(FORMAT, ...) {}
#endif

/* MAXLOGLEVEL is Warning or "higher" */
#if MAXLOGLEVEL >= LOGL_WARNING
#define LOG_WARNING(FORMAT, ...) doLog(LOGLEVEL_WARNING, \
                                     xstr(LOGMODULE), LOGDEFAULT, \
                                     &LOGMODULE_status, \
                                     __FILE__, __func__, __LINE__, \
                                     FORMAT, ## __VA_ARGS__)
#define LOGBLOB_WARNING(BUFFER, SIZE, FORMAT, ...) doLogBlob(LOGLEVEL_WARNING, \
                                                 xstr(LOGMODULE), LOGDEFAULT, \
                                                 &LOGMODULE_status, \
                                                 __FILE__, __func__, __LINE__, \
                                                 BUFFER, SIZE, \
                                                 FORMAT, ## __VA_ARGS__)
#else /* MAXLOGLEVEL is not Warning or "higher" */
#define LOG_WARNING(FORMAT, ...) {}
#define LOGBLOB_WARNING(FORMAT, ...) {}
#endif

/* MAXLOGLEVEL is Info or "higher" */
#if MAXLOGLEVEL >= LOGL_INFO
#define LOG_INFO(FORMAT, ...) doLog(LOGLEVEL_INFO, \
                                     xstr(LOGMODULE), LOGDEFAULT, \
                                     &LOGMODULE_status, \
                                     __FILE__, __func__, __LINE__, \
                                     FORMAT, ## __VA_ARGS__)
#define LOGBLOB_INFO(BUFFER, SIZE, FORMAT, ...) doLogBlob(LOGLEVEL_INFO, \
                                     xstr(LOGMODULE), LOGDEFAULT, \
                                     &LOGMODULE_status, \
                                     __FILE__, __func__, __LINE__, \
                                     BUFFER, SIZE, \
                                     FORMAT, ## __VA_ARGS__)
#else /* MAXLOGLEVEL is not Info or "higher" */
#define LOG_INFO(FORMAT, ...) {}
#define LOGBLOB_INFO(FORMAT, ...) {}
#endif

/* MAXLOGLEVEL is Debug or "higher" */
#if MAXLOGLEVEL >= LOGL_DEBUG
#define LOG_DEBUG(FORMAT, ...) doLog(LOGLEVEL_DEBUG, \
                                     xstr(LOGMODULE), LOGDEFAULT, \
                                     &LOGMODULE_status, \
                                     __FILE__, __func__, __LINE__, \
                                     FORMAT, ## __VA_ARGS__)
#define LOGBLOB_DEBUG(BUFFER, SIZE, FORMAT, ...) doLogBlob(LOGLEVEL_DEBUG, \
                                             xstr(LOGMODULE), LOGDEFAULT, \
                                             &LOGMODULE_status, \
                                             __FILE__, __func__, __LINE__, \
                                             BUFFER, SIZE, \
                                             FORMAT, ## __VA_ARGS__)
#else /* MAXLOGLEVEL is not Debug or "higher" */
#define LOG_DEBUG(FORMAT, ...) {}
#define LOGBLOB_DEBUG(FORMAT, ...) {}
#endif

/* MAXLOGLEVEL is Trace */
#if MAXLOGLEVEL >= LOGL_TRACE
#define LOG_TRACE(FORMAT, ...) doLog(LOGLEVEL_TRACE, \
                                     xstr(LOGMODULE), LOGDEFAULT, \
                                     &LOGMODULE_status, \
                                     __FILE__, __func__, __LINE__, \
                                     FORMAT, ## __VA_ARGS__)
#define LOGBLOB_TRACE(BUFFER, SIZE, FORMAT, ...) doLogBlob(LOGLEVEL_TRACE, \
                                             xstr(LOGMODULE), LOGDEFAULT, \
                                             &LOGMODULE_status, \
                                             __FILE__, __func__, __LINE__, \
                                             BUFFER, SIZE, \
                                             FORMAT, ## __VA_ARGS__)
#else /* MAXLOGLEVEL is not Trace */
#define LOG_TRACE(FORMAT, ...) {}
#define LOGBLOB_TRACE(FORMAT, ...) {}
#endif

void
doLog(log_level loglevel, const char *module, log_level logdefault,
       log_level *status,
       const char *file, const char *func, int line,
       const char *msg, ...)
    COMPILER_ATTR(unused, format (printf, 8, 9));

void
doLogBlob(log_level loglevel, const char *module, log_level logdefault,
          log_level *status,
          const char *file, const char *func, int line,
          const uint8_t *buffer, size_t size, const char *msg, ...)
    COMPILER_ATTR(unused, format (printf, 10, 11));

#endif /* LOG_H */
