/*
 * Copyright 2006,2008,2012,2014 Red Hat, Inc.
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

#ifdef HAVE_SECURITY_PAM_APPL_H
#include <security/pam_appl.h>
#endif

#ifdef HAVE_SECURITY_PAM_MODULES_H
#define PAM_SM_SESSION
#include <security/pam_modules.h>
#endif

#include <limits.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#include KRB5_H

#include "init.h"
#include "log.h"
#include "minikafs.h"
#include "options.h"
#include "prompter.h"
#include "shmem.h"
#include "stash.h"
#include "tokens.h"
#include "userinfo.h"
#include "v5.h"
#include "xstr.h"

static int
maybe_setpag(const char *fn, pam_handle_t *pamh, int flags,
	     int argc, PAM_KRB5_MAYBE_CONST char **argv)
{
	krb5_context ctx;
	struct _pam_krb5_options *options;
	int i, ret;

	/* Initialize Kerberos. */
	if (_pam_krb5_init_ctx(&ctx, argc, argv) != 0) {
		warn("error initializing Kerberos");
		return PAM_SERVICE_ERR;
	}

	/* Read our options. */
	options = _pam_krb5_options_init(pamh, argc, argv, ctx,
					 _pam_krb5_option_role_general);
	if (options == NULL) {
		warn("error parsing options (shouldn't happen)");
		_pam_krb5_free_ctx(ctx);
		return PAM_SERVICE_ERR;
	}

	if (options->ignore_afs) {
		/* Do what we were told. */
		ret = PAM_IGNORE;
	} else {
		if (!minikafs_has_afs()) {
			/* Do nothing. */
			if (options->debug) {
				debug("%s did not detect AFS, "
				      "not creating new PAG", fn);
			}
			ret = PAM_IGNORE;
		} else {
			/* Create a PAG. */
			if (options->debug) {
				debug("%s detects AFS, creating new PAG", fn);
			}
			i = minikafs_setpag();
			if (i != 0) {
				if (options->debug) {
					debug("error creating new PAG: %s",
					      strerror(i));
				}
				ret = PAM_SERVICE_ERR;
			} else {
				ret = PAM_SUCCESS;
			}
		}
	}

	if (options->debug) {
		debug("%s returning %d (%s)",
		      fn,
		      ret,
		      pam_strerror(pamh, ret));
	}
	_pam_krb5_options_free(pamh, ctx, options);
	_pam_krb5_free_ctx(ctx);
	return ret;
}

int
pam_sm_authenticate(pam_handle_t *pamh, int flags,
		    int argc, PAM_KRB5_MAYBE_CONST char **argv)
{
	return PAM_IGNORE;
}

int
pam_sm_setcred(pam_handle_t *pamh, int flags,
	       int argc, PAM_KRB5_MAYBE_CONST char **argv)
{
	if (flags & PAM_ESTABLISH_CRED) {
		return maybe_setpag("pam_setcred", pamh, flags, argc, argv);
	}
	return PAM_IGNORE;
}

int
pam_sm_open_session(pam_handle_t *pamh, int flags,
		    int argc, PAM_KRB5_MAYBE_CONST char **argv)
{
	return maybe_setpag("pam_open_session", pamh, flags, argc, argv);
}

int
pam_sm_close_session(pam_handle_t *pamh, int flags,
		     int argc, PAM_KRB5_MAYBE_CONST char **argv)
{
	return PAM_SUCCESS;
}
