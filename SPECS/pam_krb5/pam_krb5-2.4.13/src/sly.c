/*
 * Copyright 2003,2004,2005,2006,2007,2008,2009,2012,2013,2014 Red Hat, Inc.
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

#include <sys/stat.h>
#include <sys/wait.h>
#include <errno.h>
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
#include "sly.h"
#include "stash.h"
#include "tokens.h"
#include "userinfo.h"
#include "v5.h"

/* Store the TGT in $KRB5CCNAME.  Use a child process to possibly drop
 * privileges while we're doing it. */
static int
sly_v5(krb5_context ctx, const char *ccname,
       struct _pam_krb5_options *options,
       const char *user, struct _pam_krb5_user_info *userinfo,
       uid_t uid, gid_t gid,
       struct _pam_krb5_stash *stash)
{
	int i;
	i = _pam_krb5_cchelper_update(ctx, stash, options,
				      user, userinfo, uid, gid,
				      ccname);
	return (i == 0) ? PAM_SUCCESS : PAM_SYSTEM_ERR;
}

/* Inexpensive checks. */
int
_pam_krb5_sly_looks_unsafe(void)
{
	if (getenv("SUDO_COMMAND") != NULL) {
		return 1;
	}
	if (getuid() != geteuid()) {
		return 2;
	}
	if (getgid() != getegid()) {
		return 3;
	}
	return 0;
}

int
_pam_krb5_sly_maybe_refresh(pam_handle_t *pamh, int flags, const char *why,
			    int argc, PAM_KRB5_MAYBE_CONST char **argv)
{
	PAM_KRB5_MAYBE_CONST char *user;
	krb5_context ctx;
	struct _pam_krb5_options *options;
	struct _pam_krb5_user_info *userinfo;
	struct _pam_krb5_stash *stash;
	struct stat st;
	int i, retval;
	uid_t uid;
	gid_t gid;
	const char *v5ccname, *v5pathname;

	/* Inexpensive checks. */
	switch (_pam_krb5_sly_looks_unsafe()) {
	case 0:
		/* nothing: everything's okay */
		break;
	case 1:
		warn("won't refresh credentials while running under sudo");
		return PAM_SERVICE_ERR;
		break;
	case 2:
		warn("won't refresh credentials while running setuid");
		return PAM_SERVICE_ERR;
		break;
	case 3:
		warn("won't refresh credentials while running setgid");
		return PAM_SERVICE_ERR;
		break;
	default:
		warn("not safe to refresh credentials");
		return PAM_SERVICE_ERR;
		break;
	}

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
	if (options->debug) {
		debug("called to update credentials for '%s'", user);
	}

	/* Get information about the user and the user's principal name. */
	userinfo = _pam_krb5_user_info_init(ctx, user, options);
	if (userinfo == NULL) {
		if (options->ignore_unknown_principals) {
			retval = PAM_IGNORE;
		} else {
			warn("error getting information about '%s' "
			     "(shouldn't happen)", user);
			retval = PAM_USER_UNKNOWN;
		}
		_pam_krb5_options_free(pamh, ctx, options);
		_pam_krb5_free_ctx(ctx);
		return retval;
	}

	if ((options->user_check) &&
	    (options->minimum_uid != (uid_t)-1) &&
	    (userinfo->uid < options->minimum_uid)) {
		if (options->debug) {
			debug("ignoring '%s' -- uid below minimum", user);
		}
		_pam_krb5_user_info_free(ctx, userinfo);
		_pam_krb5_options_free(pamh, ctx, options);
		_pam_krb5_free_ctx(ctx);
		return PAM_IGNORE;
	}

	/* Get the stash for this user. */
	stash = _pam_krb5_stash_get(pamh, user, userinfo, options);
	if (stash == NULL) {
		warn("error retrieving stash for '%s' (shouldn't happen)",
		     user);
		_pam_krb5_user_info_free(ctx, userinfo);
		_pam_krb5_options_free(pamh, ctx, options);
		_pam_krb5_free_ctx(ctx);
		return PAM_SERVICE_ERR;
	}

	retval = PAM_SERVICE_ERR;

	/* Save credentials in the right places. */
	v5ccname = pam_getenv(pamh, "KRB5CCNAME");
	if (v5ccname == NULL) {
		v5ccname = krb5_cc_default_name(ctx);
	}
	v5pathname = NULL;
	if (v5ccname == NULL) {
		/* This should never happen, but all we can do is tell libpam
		 * to ignore us.  We have nothing to do. */
		if (options->debug) {
			debug("ignoring '%s' -- no default ccache name", user);
		}
		retval = PAM_IGNORE;
	} else {
		if (strncmp(v5ccname, "FILE:", 5) == 0) {
			v5pathname = v5ccname + 5;
			if (options->debug) {
				debug("ccache is a file named '%s'",
				      v5pathname);
			}
		} else
		if (strncmp(v5ccname, "DIR:", 4) == 0) {
			v5pathname = v5ccname + 4;
			if (options->debug) {
				debug("ccache is a directory named '%s'",
				      v5pathname);
			}
		} else {
			if (options->debug) {
				debug("ccache '%s' is not a file or directory",
				      v5ccname);
			}
		}
	}

	uid = options->user_check ? userinfo->uid : getuid();
	gid = options->user_check ? userinfo->gid : getgid();

	if (v5_ccache_has_tgt(ctx, stash->v5ccache,
			      options->realm, NULL) == 0) {
		if ((options->ignore_afs == 0) && tokens_useful()) {
			tokens_obtain(ctx, stash, options, userinfo, 0);
		}
		if (v5pathname != NULL) {
			/* Check the permissions on the ccache. */
			if ((access(v5pathname, R_OK | W_OK) == 0) &&
			    (lstat(v5pathname, &st) == 0)) {
				if (!(S_ISREG(st.st_mode) ||
				      S_ISDIR(st.st_mode))) {
					if (options->debug) {
						debug("ccache '%s' for '%s' "
						      "is not a regular file "
						      "or directory",
						      v5ccname, user);
					}
					retval = PAM_SUCCESS;
				} else
				if (!(((st.st_mode & S_IRWXG) == 0) &&
				      ((st.st_mode & S_IRWXO) == 0))) {
					if (options->debug) {
						debug("ccache '%s' for '%s' "
						      "is group or world "
						      "accessible",
						      v5ccname, user);
					}
					retval = PAM_SUCCESS;
				} else
				if (!((st.st_uid == uid) &&
				      (st.st_gid == gid))) {
					if (options->debug) {
						debug("ccache '%s' for '%s' "
						      "is owned by a another "
						      "user or group",
						      v5ccname, user);
					}
					retval = PAM_SUCCESS;
				} else {
					if (options->debug) {
						debug("updating ccache '%s' "
						      "for '%s'",
						      v5ccname, user);
					}
					retval = sly_v5(ctx, v5ccname, options,
							user, userinfo,
							uid, gid, stash);
				}
			} else {
				if (errno == ENOENT) {
					/* We have nothing to do. */
					retval = PAM_SUCCESS;
				}
			}
		} else {
			if (v5ccname != NULL) {
				/* Go ahead and update the current
				 * not-on-the-filesystem ccache. */
				if (options->debug) {
					debug("updating ccache '%s' for '%s'",
					      v5ccname, user);
				}
				retval = sly_v5(ctx, v5ccname, options,
						user, userinfo,
						uid, gid, stash);
			}
		}
	} else {
		if (options->debug) {
			debug("no credentials available to store in '%s'",
			      v5ccname);
		}
		retval = PAM_SUCCESS;
	}

	if (options->debug) {
		debug("%s returning %d (%s)", why, retval,
		      pam_strerror(pamh, retval));
	}

	_pam_krb5_user_info_free(ctx, userinfo);
	_pam_krb5_options_free(pamh, ctx, options);
	_pam_krb5_free_ctx(ctx);

	return retval;
}
