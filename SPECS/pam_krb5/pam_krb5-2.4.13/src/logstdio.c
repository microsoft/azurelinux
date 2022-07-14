/*
 * Copyright 2004,2006,2010,2011 Red Hat, Inc.
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
#include <unistd.h>

#include KRB5_H

#include <security/pam_appl.h>

#include "log.h"
#include "options.h"
#include "stash.h"
#include "minikafs.h"

struct _pam_krb5_options log_options;
char *log_progname = "pam_krb5";
pid_t log_pid = -1;

static void
maybe_setup_log_pid(void)
{
	char *tmp;
	size_t l;
	if (log_pid == -1) {
		log_pid = getpid();
	}
	if (log_pid != getpid()) {
		l = strlen(log_progname) + sizeof(log_pid) * 3;
		tmp = malloc(l + 3);
		if (tmp != NULL) {
			snprintf(tmp, l + 3, "pam_krb5[%ld]", (long) log_pid);
			log_progname = tmp;
		}
	}
}

void
debug(const char *fmt, ...)
{
	va_list va;
	char *fmt2;
	maybe_setup_log_pid();
	fmt2 = malloc(strlen(fmt) + strlen(log_progname) + strlen(": \n") + 1);
	if (fmt2 == NULL) {
		return;
	}
	sprintf(fmt2, "%s: %s\n", log_progname, fmt);
	if (log_options.debug > 0) {
		va_start(va, fmt);
		vfprintf(stderr, fmt2, va);
		va_end(va);
	}
	free(fmt2);
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
		fprintf(stderr, "libkrb5 trace message: %.*s\n", len, info->message);
	}
}
#endif

void
warn(const char *fmt, ...)
{
	va_list va;
	char *fmt2;
	maybe_setup_log_pid();
	fmt2 = malloc(strlen(fmt) + strlen(log_progname) + strlen(": \n") + 1);
	if (fmt2 == NULL) {
		return;
	}
	sprintf(fmt2, "%s: %s\n", log_progname, fmt);
	va_start(va, fmt);
	vfprintf(stderr, fmt2, va);
	va_end(va);
	free(fmt2);
}

void
notice(const char *fmt, ...)
{
	va_list va;
	char *fmt2;
	maybe_setup_log_pid();
	fmt2 = malloc(strlen(fmt) + strlen(log_progname) + strlen(": \n") + 1);
	if (fmt2 == NULL) {
		return;
	}
	sprintf(fmt2, "%s: %s\n", log_progname, fmt);
	va_start(va, fmt);
	vfprintf(stderr, fmt2, va);
	va_end(va);
	free(fmt2);
}

void
crit(const char *fmt, ...)
{
	va_list va;
	char *fmt2;
	maybe_setup_log_pid();
	fmt2 = malloc(strlen(fmt) + strlen(log_progname) + strlen(": \n") + 1);
	if (fmt2 == NULL) {
		return;
	}
	sprintf(fmt2, "%s: %s\n", log_progname, fmt);
	va_start(va, fmt);
	vfprintf(stderr, fmt2, va);
	va_end(va);
	free(fmt2);
}

void
notice_user(pam_handle_t *pamh, const char *fmt, ...)
{
	va_list args;

	va_start(args, fmt);

	vfprintf(stderr, fmt, args);

	va_end(args);
}
