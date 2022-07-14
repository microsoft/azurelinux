/*
 * Copyright 2003,2004,2005,2006,2007 Red Hat, Inc.
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
#include <stdlib.h>
#include <string.h>

#ifdef HAVE_SECURITY_PAM_APPL_H
#include <security/pam_appl.h>
#endif

#ifdef HAVE_SECURITY_PAM_MODULES_H
#include <security/pam_modules.h>
#endif

#include KRB5_H

#include "init.h"
#include "log.h"
#include "v5.h"

static int
set_realm(krb5_context ctx, int argc, PAM_KRB5_MAYBE_CONST char **argv)
{
	int i;
	for (i = argc - 1; i >= 0; i--) {
		if (strncmp(argv[i], "realm=", 6) == 0) {
			return krb5_set_default_realm(ctx, argv[i] + 6);
		}
	}
	return 0;
}

int
_pam_krb5_init_ctx(krb5_context *ctx,
		   int argc, PAM_KRB5_MAYBE_CONST char **argv)
{
	int try_secure = 1, i;
	for (i = 0; i < argc; i++) {
		if (strcmp(argv[i], "unsecure_for_debugging_only") == 0) {
			try_secure = 0;
		}
	}
	*ctx = NULL;
#ifdef HAVE_KRB5_INIT_SECURE_CONTEXT
	if (try_secure) {
		i = krb5_init_secure_context(ctx);
		if (i != 0) {
			warn("error initializing kerberos: %d (%s)", i,
			     v5_error_message(i));
		}
		if (i == 0) {
			i = set_realm(*ctx, argc, argv);
			if (i != 0) {
				_pam_krb5_free_ctx(*ctx);
				*ctx = NULL;
			}
		}
		return i;
	}
#endif
	i = krb5_init_context(ctx);
	if (i != 0) {
		warn("error initializing kerberos: %d (%s)", i,
		     v5_error_message(i));
	}
	if (i == 0) {
		i = set_realm(*ctx, argc, argv);
		if (i != 0) {
			_pam_krb5_free_ctx(*ctx);
			*ctx = NULL;
		}
	}
	return i;
}

void
_pam_krb5_free_ctx(krb5_context ctx)
{
#ifdef HAVE_KRB5_SET_TRACE_CALLBACK
	krb5_set_trace_callback(ctx, NULL, NULL);
#endif
	krb5_free_context(ctx);
}
