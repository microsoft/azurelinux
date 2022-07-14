/*
 * Copyright 2003,2004,2005,2006,2007,2008,2009,2010,2011,2014 Red Hat, Inc.
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
#define PAM_SM_ACCT_MGMT
#include <security/pam_modules.h>
#endif

#include <errno.h>
#include <stdlib.h>
#include <string.h>

#include KRB5_H

#include "init.h"
#include "kuserok.h"
#include "log.h"
#include "options.h"
#include "prompter.h"
#include "stash.h"
#include "tokens.h"
#include "userinfo.h"
#include "v5.h"

int
pam_sm_acct_mgmt(pam_handle_t *pamh, int flags,
		 int argc, PAM_KRB5_MAYBE_CONST char **argv)
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

	/* Get information about the user and the user's principal name. */
	userinfo = _pam_krb5_user_info_init(ctx, user, options);
	if (userinfo == NULL) {
		if (options->ignore_unknown_principals == 0) {
			retval = PAM_IGNORE;
		} else {
			warn("error getting information about '%s'", user);
			retval = PAM_USER_UNKNOWN;
		}
		_pam_krb5_options_free(pamh, ctx, options);
		_pam_krb5_free_ctx(ctx);
		return retval;
	}

	/* Check the minimum UID argument. */
	if ((options->user_check) &&
	    (options->minimum_uid != (uid_t) -1) &&
	    (userinfo->uid < options->minimum_uid)) {
		if (options->debug) {
			debug("ignoring '%s' -- uid below minimum = %lu", user,
			      (unsigned long) options->minimum_uid);
		}
		_pam_krb5_user_info_free(ctx, userinfo);
		_pam_krb5_options_free(pamh, ctx, options);
		_pam_krb5_free_ctx(ctx);
		return PAM_IGNORE;
	}

	/* Get the stash for this user. */
	stash = _pam_krb5_stash_get(pamh, user, userinfo, options);
	if (stash == NULL) {
		_pam_krb5_user_info_free(ctx, userinfo);
		_pam_krb5_options_free(pamh, ctx, options);
		_pam_krb5_free_ctx(ctx);
		return PAM_SERVICE_ERR;
	}

	/* If we haven't previously attempted to authenticate this user, make
	 * a quick check to screen out unknown users. */
	if (stash->v5attempted == 0) {
		/* We didn't participate in authentication, so stand back. */
		if (options->ignore_unknown_principals) {
			retval = PAM_IGNORE;
		} else {
			retval = PAM_USER_UNKNOWN;
		}
		if (options->debug) {
			debug("user '%s' was not authenticated by " PACKAGE
			      ", returning \"%s\"", user,
			      pam_strerror(pamh, retval));
		}
	} else {
		/* Check what happened when we asked for initial credentials. */
		switch (stash->v5result) {
		case 0:
			if (options->debug) {
				debug("account management succeeds for '%s'",
				      user);
			}
			retval = PAM_SUCCESS;
			break;
		case KRB5KDC_ERR_PREAUTH_FAILED:
		case KRB5KRB_AP_ERR_BAD_INTEGRITY:
			if (options->debug) {
				debug("authentication failed, but no account "
				      "management error was indicated; "
				      "account management succeeds for '%s'",
				      user);
			}
			retval = PAM_SUCCESS;
			break;
		case KRB5KDC_ERR_C_PRINCIPAL_UNKNOWN:
		case KRB5KDC_ERR_NAME_EXP:
			if (options->ignore_unknown_principals) {
				debug("account checks fail for '%s': "
				      "user is unknown or account expired "
				      "(ignoring)", user);
				retval = PAM_IGNORE;
			} else {
				notice("account checks fail for '%s': "
				       "user is unknown or account expired",
				       user);
				retval = PAM_USER_UNKNOWN;
			}
			break;
		case KRB5KDC_ERR_KEY_EXP:
			notice("account checks fail for '%s': "
			       "password has expired", user);
			retval = PAM_NEW_AUTHTOK_REQD;
			break;
		case EAGAIN:
		case KRB5_REALM_CANT_RESOLVE:
			notice("account checks fail for '%s': "
			       "can't resolve KDC addresses", user);
			retval = PAM_AUTHINFO_UNAVAIL;
			break;
		case KRB5_KDC_UNREACH:
			notice("account checks fail for '%s': "
			       "KDCs are unreachable", user);
			retval = PAM_AUTHINFO_UNAVAIL;
			break;
		case KRB5KDC_ERR_CLIENT_REVOKED:
			if (options->ignore_unknown_principals) {
				notice("account checks fail for '%s': "
				       "account is locked (ignoring)", user);
				retval = PAM_IGNORE;
			} else {
				notice("account checks fail for '%s': "
				       "account is locked", user);
				retval = PAM_USER_UNKNOWN;
			}
			break;
		default:
			notice("account checks fail for '%s': "
			       "unknown reason %d (%s)", user, stash->v5result,
			       v5_error_message(stash->v5result));
			retval = PAM_SERVICE_ERR;
			break;
		}
	}

	/* If we got this far, check the target user's .k5login file. */
	if ((retval == PAM_SUCCESS) && options->user_check &&
	    (options->ignore_k5login == 0)) {
		if (_pam_krb5_kuserok(ctx, stash, options, userinfo, user,
				      userinfo->uid, userinfo->gid) != TRUE) {
			notice("account checks fail for '%s': user disallowed "
			       "by .k5login file for '%s'",
			       userinfo->unparsed_name, user);
			retval = PAM_PERM_DENIED;
		} else {
			if (options->debug) {
				debug("'%s' passes .k5login check for '%s'",
				      userinfo->unparsed_name, user);
			}
		}
	}

	/* Catch any USER_UNKNOWN errors which we're supposed to suppress. */
	if ((retval == PAM_USER_UNKNOWN) &&
	    (options->ignore_unknown_principals)) {
		retval = PAM_IGNORE;
	}

	/* Clean up. */
	if (options->debug) {
		debug("pam_acct_mgmt returning %d (%s)", retval,
		      pam_strerror(pamh, retval));
	}
	_pam_krb5_options_free(pamh, ctx, options);
	_pam_krb5_user_info_free(ctx, userinfo);
	_pam_krb5_free_ctx(ctx);

	return retval;
}
