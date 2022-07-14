/*
 * Copyright 2003,2004,2006,2011 Red Hat, Inc.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 * 1. Redistributions of source code must retain the above copyright
 *    notice, and the entire permission notice in its entirety,
 *    including the disclaimer of warranties.
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 * 3. The name of the author may not be used to endorse or promote
 *    products derived from this software without specific prior
 *    written permission.
 *
 * ALTERNATIVELY, this product may be distributed under the terms of the
 * GNU Lesser General Public License, in which case the provisions of the
 * LGPL are required INSTEAD OF the above restrictions.
 *
 * THIS SOFTWARE IS PROVIDED ``AS IS'' AND ANY EXPRESS OR IMPLIED
 * WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
 * MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.  IN
 * NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT,
 * INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
 * NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF
 * USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
 * ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
 * THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */

#include "../config.h"
#include <sys/types.h>
#include <limits.h>
#include <stdarg.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <syslog.h>
#include <unistd.h>

#ifdef HAVE_SECURITY_PAM_APPL_H
#include <security/pam_appl.h>
#endif

#ifdef HAVE_SECURITY_PAM_MODULES_H
#include <security/pam_modules.h>
#endif

#include KRB5_H

#include "conv.h"
#include "log.h"

#ifndef PACKAGE
#ifdef PACKAGE_NAME
#define PACKAGE PACKAGE_NAME
#endif
#endif

#if defined(LOG_AUTHPRIV)
#define PACKAGE_FACILITY LOG_AUTHPRIV
#elif defined(LOG_AUTH)
#define PACKAGE_FACILITY LOG_AUTH
#else
#define PACKAGE_FACILITY 0
#endif

static int
llen(unsigned long l)
{
	int ret = 1;
	while (l != 0) {
		ret++;
		l /= 10;
	}
	return ret;
}

void
debug(const char *fmt, ...)
{
	va_list args;
	char *fmt2;

	va_start(args, fmt);

	fmt2 = malloc(strlen(PACKAGE) + 4 + llen(getpid()) + strlen(fmt) + 1);
	if (fmt2 != NULL) {
		sprintf(fmt2, "%s[%lu]: %s", PACKAGE,
			(unsigned long) getpid(), fmt);
		vsyslog(PACKAGE_FACILITY | LOG_DEBUG, fmt2, args);
		free(fmt2);
	} else {
		vsyslog(PACKAGE_FACILITY | LOG_DEBUG, fmt, args);
	}

	va_end(args);
}

#ifdef HAVE_KRB5_SET_TRACE_CALLBACK
void
#if defined(HAVE_STRUCT__KRB5_TRACE_INFO)
trace(krb5_context ctx, const struct _krb5_trace_info *info, void *data)
#elif defined(HAVE_STRUCT_KRB5_TRACE_INFO)
trace(krb5_context ctx, const struct krb5_trace_info *info, void *data)
#endif
{
	int len;
	if (info != NULL) {
		len = strlen(info->message);
		while ((len > 0) &&
		       (strchr("\r\n", info->message[len - 1]) != NULL)) {
			len--;
		}
		debug("libkrb5 trace message: %.*s", len, info->message);
	}
}
#endif

void
warn(const char *fmt, ...)
{
	va_list args;
	char *fmt2;

	va_start(args, fmt);

	fmt2 = malloc(strlen(PACKAGE) + 4 + llen(getpid()) + strlen(fmt) + 1);
	if (fmt2 != NULL) {
		sprintf(fmt2, "%s[%lu]: %s", PACKAGE,
			(unsigned long) getpid(), fmt);
		vsyslog(PACKAGE_FACILITY | LOG_WARNING, fmt2, args);
		free(fmt2);
	} else {
		vsyslog(PACKAGE_FACILITY | LOG_WARNING, fmt, args);
	}

	va_end(args);
}

void
notice(const char *fmt, ...)
{
	va_list args;
	char *fmt2;

	va_start(args, fmt);

	fmt2 = malloc(strlen(PACKAGE) + 4 + llen(getpid()) + strlen(fmt) + 1);
	if (fmt2 != NULL) {
		sprintf(fmt2, "%s[%lu]: %s", PACKAGE,
			(unsigned long) getpid(), fmt);
		vsyslog(PACKAGE_FACILITY | LOG_NOTICE, fmt2, args);
		free(fmt2);
	} else {
		vsyslog(PACKAGE_FACILITY | LOG_NOTICE, fmt, args);
	}

	va_end(args);
}

void
crit(const char *fmt, ...)
{
	va_list args;
	char *fmt2;

	va_start(args, fmt);

	fmt2 = malloc(strlen(PACKAGE) + 4 + llen(getpid()) + strlen(fmt) + 1);
	if (fmt2 != NULL) {
		sprintf(fmt2, "%s[%lu]: %s", PACKAGE,
			(unsigned long) getpid(), fmt);
		vsyslog(PACKAGE_FACILITY | LOG_CRIT, fmt2, args);
		free(fmt2);
	} else {
		vsyslog(PACKAGE_FACILITY | LOG_CRIT, fmt, args);
	}

	va_end(args);
}

void
notice_user(pam_handle_t *pamh, const char *fmt, ...)
{
	va_list args;
	struct pam_message message;
	struct pam_response *responses;
	char buf[LINE_MAX];

	va_start(args, fmt);

	vsnprintf(buf, sizeof(buf), fmt, args);
	memset(&message, 0, sizeof(message));
	message.msg_style = PAM_ERROR_MSG;
	message.msg = buf;

	responses = NULL;
	_pam_krb5_conv_call(pamh, &message, 1, &responses);

	va_end(args);
}
