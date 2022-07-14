/*
 * Copyright 2008,2009,2010,2012,2015 Red Hat, Inc.
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
#include <sys/select.h>
#include <sys/stat.h>
#include <sys/wait.h>
#include <errno.h>
#include <fcntl.h>
#include <grp.h>
#include <limits.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#ifdef HAVE_SECURITY_PAM_APPL_H
#include <security/pam_appl.h>
#endif

#ifdef HAVE_SECURITY_PAM_MODULES_H
#include <security/pam_modules.h>
#endif

#include KRB5_H

#include "cchelper.h"
#include "init.h"
#include "log.h"
#include "options.h"
#include "stash.h"
#include "tokens.h"
#include "userinfo.h"
#include "v5.h"

#include "kuserok.h"

/* Use a helper to perform the kuserok check using the user's credentials,
 * in case we're in a root-squashed or needs-authentication situation with
 * a remotely-stored file. */
krb5_boolean
_pam_krb5_kuserok(krb5_context ctx,
                  struct _pam_krb5_stash *stash,
		  struct _pam_krb5_options *options,
		  struct _pam_krb5_user_info *userinfo,
		  const char *user,
		  uid_t uid, gid_t gid)
{
	int outpipe[2];
	int i;
	krb5_boolean allowed;
	krb5_error_code err;
	unsigned char result;
	pid_t child;
	struct sigaction saved_sigchld_handler, saved_sigpipe_handler;
	struct sigaction ignore_handler, default_handler;
	char envstr[PATH_MAX + 20], localname[PATH_MAX];
	const char *ccname;

	if (pipe(outpipe) == -1) {
		return -1;
	}
	/* Set signal handlers here.  We used to do it later, but that turns
	 * out to be a race if the child decides to exit immediately. */
	memset(&default_handler, 0, sizeof(default_handler));
	default_handler.sa_handler = SIG_DFL;
	if (sigaction(SIGCHLD, &default_handler, &saved_sigchld_handler) != 0) {
		close(outpipe[0]);
		close(outpipe[1]);
		return -1;
	}
	memset(&ignore_handler, 0, sizeof(ignore_handler));
	ignore_handler.sa_handler = SIG_IGN;
	if (sigaction(SIGPIPE, &ignore_handler, &saved_sigpipe_handler) != 0) {
		sigaction(SIGCHLD, &saved_sigchld_handler, NULL);
		close(outpipe[0]);
		close(outpipe[1]);
		return -1;
	}
	switch (child = fork()) {
	case -1:
		sigaction(SIGCHLD, &saved_sigchld_handler, NULL);
		sigaction(SIGPIPE, &saved_sigpipe_handler, NULL);
		close(outpipe[0]);
		close(outpipe[1]);
		return -1;
		break;
	case 0:
		/* We're the child. */
		close(outpipe[0]);
		setgroups(0, NULL);
		/* Now, attempt to assume the desired uid/gid pair.  Note that
		 * if we're not root, this is allowed to fail. */
		if ((gid != getgid()) || (gid != getegid())) {
			i = setregid(gid, gid);
		}
		if ((uid != getuid()) || (uid != geteuid())) {
			i = setreuid(uid, uid);
		}
		/* Try to get tokens. */
		if ((options->ignore_afs == 0) && tokens_useful()) {
			tokens_obtain(ctx, stash, options, userinfo, 1);
		}
		/* Set up the user's Kerberos 5 creds, too. If the naming
		 * services (for example, nss_ldap in sasl mode) or an
		 * out-of-process filesystem helper (rpc.gssd) needs the user's
		 * creds, we probably need to provide them. */
		ccname = NULL;
		i = v5_save_for_kuserok(ctx, stash, user, userinfo, options,
					&ccname);
		if ((i == PAM_SUCCESS) && (strlen(ccname) > 0)) {
			if (options->debug) {
				debug("created ccache '%s' for '%s'",
				      ccname, user);
			}
			sprintf(envstr, "KRB5CCNAME=%s", ccname);
			putenv(envstr);
		}
		/* Actually check, now that we have a shot at being able to
		 * read the user's .k5login file. */
		allowed = krb5_kuserok(ctx, userinfo->principal_name, user);
		if (options->debug) {
			debug("krb5_kuserok() says \"%s\" for (\"%s\",\"%s\")",
			      allowed ? "true" : "false",
			      userinfo->unparsed_name, user);
		}
#ifdef HAVE_KRB5_ANAME_TO_LOCALNAME
		if (!allowed && options->always_allow_localname) {
			memset(&localname, '\0', sizeof(localname));
			err = krb5_aname_to_localname(ctx,
						      userinfo->principal_name,
						      sizeof(localname),
						      localname);
			if (err != 0) {
				if (options->debug) {
					debug("krb5_aname_to_localname "
					      "failed: %s",
					      v5_error_message(err));
				}
			} else {
				if (strcmp(localname, user) == 0) {
					if (options->debug) {
						debug("krb5_aname_to_localname "
						      "returned '%s' for '%s', "
						      "allowing access",
						      localname,
						      userinfo->unparsed_name);
					}
					allowed = 1;
				}
			}
		}
#endif
		/* Clean up. */
		if (ccname != NULL) {
			v5_destroy(ctx, stash, options);
		}
		result = (allowed == 1);
		_pam_krb5_write_with_retry(outpipe[1], &result, 1);
		_exit(0);
		break;
	default:
		/* parent */
		close(outpipe[1]);
		if (_pam_krb5_read_with_retry(outpipe[0], &result, 1) == 1) {
			allowed = result;
		} else {
			allowed = FALSE;
		}
		waitpid(child, NULL, 0);
		sigaction(SIGCHLD, &saved_sigchld_handler, NULL);
		sigaction(SIGPIPE, &saved_sigpipe_handler, NULL);
		close(outpipe[0]);
		return allowed;
		break;
	}
	abort(); /* not reached */
}
