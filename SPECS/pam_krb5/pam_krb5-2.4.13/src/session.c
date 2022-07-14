/*
 * Copyright 2003,2004,2005,2006,2007,2008,2009,2011,2014 Red Hat, Inc.
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
#include "options.h"
#include "prompter.h"
#include "session.h"
#include "shmem.h"
#include "stash.h"
#include "tokens.h"
#include "userinfo.h"
#include "v5.h"
#include "xstr.h"

int
_pam_krb5_open_session(pam_handle_t *pamh, int flags,
		       int argc, PAM_KRB5_MAYBE_CONST char **argv,
		       const char *caller,
		       enum _pam_krb5_session_caller caller_type)
{
	PAM_KRB5_MAYBE_CONST char *user;
	char envstr[PATH_MAX + 20], *segname;
	const char *ccname;
	krb5_context ctx;
	struct _pam_krb5_options *options;
	struct _pam_krb5_user_info *userinfo;
	struct _pam_krb5_stash *stash;
	int i, retval;

	/* Initialize Kerberos. */
	if (_pam_krb5_init_ctx(&ctx, argc, argv) != 0) {
		warn("error initializing Kerberos");
		return PAM_SERVICE_ERR;
	}

	/* Get the user's name. */
	i = pam_get_user(pamh, &user, NULL);
	if ((i != PAM_SUCCESS) || (user == NULL)) {
		warn("could not identify user name");
		_pam_krb5_free_ctx(ctx);
		return i;
	}

	/* Read our options. */
	options = _pam_krb5_options_init(pamh, argc, argv, ctx,
					 _pam_krb5_option_role_general);
	if (options == NULL) {
		warn("error parsing options (shouldn't happen)");
		_pam_krb5_free_ctx(ctx);
		return PAM_SERVICE_ERR;
	}

	/* If we're in a no-cred-session situation, return. */
	if ((!options->cred_session) &&
	    (caller_type == _pam_krb5_session_caller_setcred)) {
		_pam_krb5_options_free(pamh, ctx, options);
		_pam_krb5_free_ctx(ctx);
		return PAM_SUCCESS;
	}

	/* Get information about the user and the user's principal name. */
	userinfo = _pam_krb5_user_info_init(ctx, user, options);
	if (userinfo == NULL) {
		if (options->debug) {
			debug("no user info for '%s'", user);
		}
		if (options->ignore_unknown_principals) {
			retval = PAM_IGNORE;
		} else {
			retval = PAM_USER_UNKNOWN;
		}
		if (options->debug) {
			debug("%s returning %d (%s)", caller,
			      retval,
			      pam_strerror(pamh, retval));
		}
		_pam_krb5_options_free(pamh, ctx, options);
		_pam_krb5_free_ctx(ctx);
		return retval;
	}
	if ((options->user_check) &&
	    (options->minimum_uid != (uid_t)-1) &&
	    (userinfo->uid < options->minimum_uid)) {
		if (options->debug) {
			debug("ignoring '%s' -- uid below minimum = %lu", user,
			      (unsigned long) options->minimum_uid);
		}
		_pam_krb5_user_info_free(ctx, userinfo);
		if (options->debug) {
			debug("%s returning %d (%s)", caller, PAM_IGNORE,
			      pam_strerror(pamh, PAM_IGNORE));
		}
		_pam_krb5_options_free(pamh, ctx, options);
		_pam_krb5_free_ctx(ctx);
		return PAM_IGNORE;
	}

	/* Get the stash for this user. */
	stash = _pam_krb5_stash_get(pamh, user, userinfo, options);
	if (stash == NULL) {
		warn("no stash for '%s' (shouldn't happen)", user);
		_pam_krb5_user_info_free(ctx, userinfo);
		if (options->debug) {
			debug("%s returning %d (%s)", caller,
			      PAM_SERVICE_ERR,
			      pam_strerror(pamh, PAM_SERVICE_ERR));
		}
		_pam_krb5_options_free(pamh, ctx, options);
		_pam_krb5_free_ctx(ctx);
		return PAM_SERVICE_ERR;
	}

	/* We don't need the shared memory segments any more, so we can get rid
	 * of them now.  (Depending on the application, we may not get a chance
	 * to do it later.) */
	if (options->use_shmem) {
		if ((stash->v5shm != -1) && (stash->v5shm_owner != -1)) {
			if (options->debug) {
				debug("removing shared memory segment %d"
				      " creator pid %ld",
				      stash->v5shm, (long) stash->v5shm_owner);
			}
			_pam_krb5_shm_remove(stash->v5shm_owner, stash->v5shm,
					     options->debug);
			stash->v5shm = -1;
			_pam_krb5_stash_shm_var_name(options, user, &segname);
			if (segname != NULL) {
				pam_putenv(pamh, segname);
				free(segname);
			}
		}
	}

	/* If we don't have any credentials, then we're done. */
	if ((stash->v5attempted == 0) || (stash->v5result != 0)) {
		if (options->debug) {
			debug("no creds for user '%s', "
			      "skipping session setup", user);
		}
		_pam_krb5_user_info_free(ctx, userinfo);
		if (options->debug) {
			debug("%s returning %d (%s)", caller, PAM_SUCCESS,
			      pam_strerror(pamh, PAM_SUCCESS));
		}
		_pam_krb5_options_free(pamh, ctx, options);
		_pam_krb5_free_ctx(ctx);
		return PAM_SUCCESS;
	}

	/* Obtain tokens, if necessary. */
	if ((i == PAM_SUCCESS) &&
	    (options->ignore_afs == 0) &&
	    tokens_useful()) {
		tokens_obtain(ctx, stash, options, userinfo, 1);
	}

	/* Create the user's credential cache, but only if we didn't pick them
	 * up from our calling process. */
	if (!stash->v5external) {
		if (options->debug) {
#ifdef HAVE_LONG_LONG
			debug("creating ccache for '%s', uid=%llu, gid=%llu",
			      user,
			      options->user_check ?
			      (unsigned long long) userinfo->uid :
			      (unsigned long long) getuid(),
			      options->user_check ?
			      (unsigned long long) userinfo->gid :
			      (unsigned long long) getgid());
#else
			debug("creating ccache for '%s', uid=%lu, gid=%lu",
			      user,
			      options->user_check ?
			      (unsigned long) userinfo->uid :
			      (unsigned long) getuid(),
			      options->user_check ?
			      (unsigned long) userinfo->gid :
			      (unsigned long) getgid());
#endif
		}
		i = v5_save_for_user(ctx, stash, user, userinfo,
				     options, &ccname);
		if ((i == PAM_SUCCESS) && (strlen(ccname) > 0)) {
			sprintf(envstr, "KRB5CCNAME=%s", ccname);
			pam_putenv(pamh, envstr);
			stash->v5setenv = 1;
		} else {
			if (options->debug) {
				debug("failed to create ccache for '%s'", user);
			}
		}
	}

	/* If we didn't create ccache files because we couldn't, just
	 * pretend everything's fine. */
	if ((i != PAM_SUCCESS) &&
	    (v5_ccache_has_tgt(ctx, stash->v5ccache,
			       options->realm, NULL) != 0)) {
		i = PAM_SUCCESS;
	}

	/* Clean up. */
	if (options->debug) {
		debug("%s returning %d (%s)", caller, i,
		      pam_strerror(pamh, i));
	}
	_pam_krb5_options_free(pamh, ctx, options);
	_pam_krb5_user_info_free(ctx, userinfo);


	_pam_krb5_free_ctx(ctx);
	return i;
}

int
_pam_krb5_close_session(pam_handle_t *pamh, int flags,
			int argc, PAM_KRB5_MAYBE_CONST char **argv,
		        const char *caller,
		        enum _pam_krb5_session_caller caller_type)
{
	PAM_KRB5_MAYBE_CONST char *user;
	krb5_context ctx;
	struct _pam_krb5_options *options;
	struct _pam_krb5_user_info *userinfo;
	struct _pam_krb5_stash *stash;
	int i, retval;

	/* Initialize Kerberos. */
	if (_pam_krb5_init_ctx(&ctx, argc, argv) != 0) {
		warn("error initializing Kerberos");
		return PAM_SERVICE_ERR;
	}

	/* Get the user's name. */
	i = pam_get_user(pamh, &user, NULL);
	if (i != PAM_SUCCESS) {
		warn("could not determine user name");
		_pam_krb5_free_ctx(ctx);
		return i;
	}

	/* Read our options. */
	options = _pam_krb5_options_init(pamh, argc, argv, ctx,
					 _pam_krb5_option_role_general);
	if (options == NULL) {
		_pam_krb5_free_ctx(ctx);
		return PAM_SERVICE_ERR;
	}

	/* If we're in a no-cred-session situation, return. */
	if ((!options->cred_session) &&
	    (caller_type == _pam_krb5_session_caller_setcred)) {
		_pam_krb5_options_free(pamh, ctx, options);
		_pam_krb5_free_ctx(ctx);
		return PAM_SUCCESS;
	}

	/* Get information about the user and the user's principal name. */
	userinfo = _pam_krb5_user_info_init(ctx, user, options);
	if (userinfo == NULL) {
		if (options->ignore_unknown_principals) {
			retval = PAM_IGNORE;
		} else {
			warn("no user info for %s (shouldn't happen)", user);
			retval = PAM_USER_UNKNOWN;
		}
		if (options->debug) {
			debug("%s returning %d (%s)", caller,
			      retval,
			      pam_strerror(pamh, retval));
		}
		_pam_krb5_options_free(pamh, ctx, options);
		_pam_krb5_free_ctx(ctx);
		return retval;
	}

	/* Check the minimum UID argument. */
	if ((options->user_check) &&
	    (options->minimum_uid != (uid_t)-1) &&
	    (userinfo->uid < options->minimum_uid)) {
		if (options->debug) {
			debug("ignoring '%s' -- uid below minimum", user);
		}
		_pam_krb5_user_info_free(ctx, userinfo);
		if (options->debug) {
			debug("%s returning %d (%s)", caller, PAM_IGNORE,
			      pam_strerror(pamh, PAM_IGNORE));
		}
		_pam_krb5_options_free(pamh, ctx, options);
		_pam_krb5_free_ctx(ctx);
		return PAM_IGNORE;
	}

	/* Get the stash for this user. */
	stash = _pam_krb5_stash_get(pamh, user, userinfo, options);
	if (stash == NULL) {
		warn("no stash for user %s (shouldn't happen)", user);
		_pam_krb5_user_info_free(ctx, userinfo);
		if (options->debug) {
			debug("%s returning %d (%s)", caller,
			      PAM_SERVICE_ERR,
			      pam_strerror(pamh, PAM_SERVICE_ERR));
		}
		_pam_krb5_options_free(pamh, ctx, options);
		_pam_krb5_free_ctx(ctx);
		return PAM_SERVICE_ERR;
	}

	/* If we didn't obtain any credentials, then we're done. */
	if ((stash->v5attempted == 0) || (stash->v5result != 0)) {
		if (options->debug) {
			debug("no creds for user '%s', "
			      "skipping session cleanup",
			      user);
		}
		_pam_krb5_user_info_free(ctx, userinfo);
		if (options->debug) {
			debug("%s returning %d (%s)", caller,
			      PAM_SUCCESS,
			      pam_strerror(pamh, PAM_SUCCESS));
		}
		_pam_krb5_options_free(pamh, ctx, options);
		_pam_krb5_free_ctx(ctx);
		return PAM_SUCCESS;
	}

	if (options->ignore_afs == 0) {
		tokens_release(stash, options);
	}

	if (!stash->v5external) {
		if (stash->v5ccnames != NULL) {
			v5_destroy(ctx, stash, options);
			if (stash->v5setenv) {
				pam_putenv(pamh, "KRB5CCNAME");
				stash->v5setenv = 0;
			}
		}
	} else {
		if (options->debug) {
			debug("leaving external ccache for '%s'", user);
		}
	}

	_pam_krb5_user_info_free(ctx, userinfo);
	if (options->debug) {
		debug("%s returning %d (%s)", caller,
		      PAM_SUCCESS,
		      pam_strerror(pamh, PAM_SUCCESS));
	}
	_pam_krb5_options_free(pamh, ctx, options);
	_pam_krb5_free_ctx(ctx);
	return PAM_SUCCESS;
}

int
pam_sm_open_session(pam_handle_t *pamh, int flags,
		    int argc, PAM_KRB5_MAYBE_CONST char **argv)
{
	return _pam_krb5_open_session(pamh, flags, argc, argv,
				      "pam_sm_open_session",
				      _pam_krb5_session_caller_session);
}

int
pam_sm_close_session(pam_handle_t *pamh, int flags,
		     int argc, PAM_KRB5_MAYBE_CONST char **argv)
{
	return _pam_krb5_close_session(pamh, flags, argc, argv,
				       "pam_sm_close_session",
				       _pam_krb5_session_caller_session);
}
