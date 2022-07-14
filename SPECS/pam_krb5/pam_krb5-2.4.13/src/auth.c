/*
 * Copyright 2003,2004,2005,2006,2007,2008,2009,2010,2012,2013,2014 Red Hat, Inc.
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
#include <errno.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#ifdef HAVE_SECURITY_PAM_APPL_H
#include <security/pam_appl.h>
#endif

#ifdef HAVE_SECURITY_PAM_MODULES_H
#define PAM_SM_AUTH
#define PAM_SM_SESSION
#include <security/pam_modules.h>
#endif

#include KRB5_H

#include "conv.h"
#include "init.h"
#include "initopts.h"
#include "items.h"
#include "kuserok.h"
#include "log.h"
#include "options.h"
#include "prompter.h"
#include "session.h"
#include "sly.h"
#include "stash.h"
#include "tokens.h"
#include "userinfo.h"
#include "v5.h"
#include "xstr.h"

int
pam_sm_authenticate(pam_handle_t *pamh, int flags,
		    int argc, PAM_KRB5_MAYBE_CONST char **argv)
{
	PAM_KRB5_MAYBE_CONST char *user;
	krb5_context ctx;
	struct _pam_krb5_options *options;
	struct _pam_krb5_user_info *userinfo;
	struct _pam_krb5_stash *stash;
	krb5_get_init_creds_opt *gic_options;
	int i, retval, use_third_pass, prompted, prompt_result;
	char *first_pass, *second_pass;

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
	i = v5_alloc_get_init_creds_opt(ctx, &gic_options);
	if (i != 0) {
		warn("error initializing options (shouldn't happen)");
		_pam_krb5_free_ctx(ctx);
		return PAM_SERVICE_ERR;
	}
	options = _pam_krb5_options_init(pamh, argc, argv, ctx,
					 _pam_krb5_option_role_general);
	if (options == NULL) {
		warn("error parsing options (shouldn't happen)");
		v5_free_get_init_creds_opt(ctx, gic_options);
		_pam_krb5_free_ctx(ctx);
		return PAM_SERVICE_ERR;
	}
	if (options->debug) {
		debug("called to authenticate '%s', configured realm '%s'",
		      user, options->realm);
	}
	_pam_krb5_set_init_opts(ctx, gic_options, options);

	/* Prompt for the password, as we might need to. */
	prompted = 0;
	prompt_result = PAM_ABORT;
	second_pass = NULL;
	if (options->use_second_pass) {
		first_pass = NULL;
		i = _pam_krb5_get_item_text(pamh, PAM_AUTHTOK, &first_pass);
		if ((i != PAM_SUCCESS) || (first_pass == NULL)) {
			/* Nobody's asked for a password yet. */
			prompt_result = _pam_krb5_prompt_for(pamh,
							     Y_("Password: "),
							     &second_pass);
			prompted = 1;
		}
	}

	/* Get information about the user and the user's principal name. */
	userinfo = _pam_krb5_user_info_init(ctx, user, options);
	if (userinfo == NULL) {
		if (options->ignore_unknown_principals) {
			retval = PAM_IGNORE;
		} else {
			warn("error getting information about '%s'", user);
			retval = PAM_USER_UNKNOWN;
		}
		if (prompted && (prompt_result == 0) && (second_pass != NULL)) {
			if (options->debug) {
				debug("saving newly-entered "
				      "password for use by "
				      "other modules");
			}
			pam_set_item(pamh, PAM_AUTHTOK, second_pass);
		}
		/* Clean up and return. */
		_pam_krb5_options_free(pamh, ctx, options);
		v5_free_get_init_creds_opt(ctx, gic_options);
		_pam_krb5_free_ctx(ctx);
		return retval;
	}
	if (options->debug) {
		debug("authenticating '%s'", userinfo->unparsed_name);
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
		if (prompted && (prompt_result == 0) && (second_pass != NULL)) {
			if (options->debug) {
				debug("saving newly-entered "
				      "password for use by "
				      "other modules");
			}
			pam_set_item(pamh, PAM_AUTHTOK, second_pass);
		}
		_pam_krb5_options_free(pamh, ctx, options);
		v5_free_get_init_creds_opt(ctx, gic_options);
		_pam_krb5_free_ctx(ctx);
		return PAM_IGNORE;
	}

	/* Get the stash for this user. */
	stash = _pam_krb5_stash_get(pamh, user, userinfo, options);
	if (stash == NULL) {
		warn("error retrieving stash for '%s' (shouldn't happen)",
		     user);
		_pam_krb5_user_info_free(ctx, userinfo);
		if (prompted && (prompt_result == 0) && (second_pass != NULL)) {
			if (options->debug) {
				debug("saving newly-entered "
				      "password for use by "
				      "other modules");
			}
			pam_set_item(pamh, PAM_AUTHTOK, second_pass);
		}
		_pam_krb5_options_free(pamh, ctx, options);
		v5_free_get_init_creds_opt(ctx, gic_options);
		_pam_krb5_free_ctx(ctx);
		return PAM_SERVICE_ERR;
	}

	/* If we've been called before, then the stash is more or less stale,
	 * so reset things for applications which call pam_authenticate() more
	 * than once with the same library context. */
	stash->v5attempted = 0;

	retval = PAM_AUTH_ERR;

	/* Ideally we're only going to let libkrb5 ask questions once, and
	 * after that we intend to lie to it. */
	use_third_pass = options->use_third_pass;

	/* Try with the stored password, if we've been told to use just that
	 * value. */
	first_pass = NULL;
	if ((retval != PAM_SUCCESS) && options->use_first_pass) {
		i = _pam_krb5_get_item_text(pamh, PAM_AUTHTOK, &first_pass);
		if ((i == PAM_SUCCESS) &&
		    (flags & PAM_DISALLOW_NULL_AUTHTOK) &&
		    (first_pass != NULL) &&
		    (strlen(first_pass) == 0)) {
			warn("disallowing NULL authtok for '%s'", user);
			retval = PAM_AUTH_ERR;
			i = PAM_AUTH_ERR;
		}
		if ((i == PAM_SUCCESS) &&
		    (first_pass != NULL) &&
		    (strlen(first_pass) > 0)) {
			if (options->debug) {
				if (use_third_pass) {
					debug("trying previously-entered "
					      "password for '%s', allowing "
					      "libkrb5 to prompt for more",
					      user);
				} else {
					debug("trying previously-entered "
					      "password for '%s'", user);
				}
			}
			retval = v5_get_creds(stash->v5ctx, pamh,
					      &stash->v5ccache,
					      &stash->v5armorccache,
					      user, userinfo,
					      options,
					      KRB5_TGS_NAME,
					      first_pass,
					      gic_options,
					      use_third_pass ?
					      _pam_krb5_normal_prompter :
					      _pam_krb5_previous_prompter,
					      &stash->v5expired,
					      &stash->v5result);
			use_third_pass = 0;
			stash->v5external = 0;
			stash->v5attempted = 1;
			if (options->debug) {
				debug("got result %d (%s)", stash->v5result,
				      v5_error_message(stash->v5result));
			}
		}
		if ((retval == PAM_SUCCESS) &&
		    (options->ignore_afs == 0) &&
		    (options->tokens == 1) &&
		    tokens_useful()) {
			tokens_obtain(ctx, stash, options, userinfo, 1);
		}
	}

	/* If that didn't work, and we're allowed to ask for a new password, do
	 * so in preparation for another attempt. */
	if ((retval != PAM_SUCCESS) &&
	    (retval != PAM_USER_UNKNOWN) &&
	    options->use_second_pass) {
		/* The "second_pass" variable already contains a value if we
		 * asked for one. */
		if (!prompted) {
			prompt_result = _pam_krb5_prompt_for(pamh,
							     Y_("Password: "),
							     &second_pass);
			prompted = 1;
		}
		i = prompt_result;
		if ((i == PAM_SUCCESS) &&
		    (flags & PAM_DISALLOW_NULL_AUTHTOK) &&
		    (second_pass != NULL) &&
		    (strlen(second_pass) == 0)) {
			warn("disallowing NULL authtok for '%s'", user);
			retval = PAM_AUTH_ERR;
			i = PAM_AUTH_ERR;
		}
		if ((i == PAM_SUCCESS) &&
		    (second_pass != NULL) &&
		    (strlen(second_pass) > 0)) {
			/* Save the password for the next module. */
			if (options->debug) {
				debug("saving newly-entered "
				      "password for use by "
				      "other modules");
			}
			pam_set_item(pamh, PAM_AUTHTOK, second_pass);
			if (options->debug) {
				if (use_third_pass) {
					debug("trying newly-entered "
					      "password for '%s', allowing "
					      "libkrb5 to prompt for more",
					      user);
				} else {
					debug("trying newly-entered "
					      "password for '%s'", user);
				}
			}
			retval = v5_get_creds(stash->v5ctx, pamh,
					      &stash->v5ccache,
					      &stash->v5armorccache,
					      user, userinfo,
					      options,
					      KRB5_TGS_NAME,
					      second_pass,
					      gic_options,
					      use_third_pass ?
					      _pam_krb5_normal_prompter :
					      _pam_krb5_always_fail_prompter,
					      &stash->v5expired,
					      &stash->v5result);
			use_third_pass = 0;
			stash->v5external = 0;
			stash->v5attempted = 1;
			if (options->debug) {
				debug("got result %d (%s)", stash->v5result,
				      v5_error_message(stash->v5result));
			}
		}
		if ((retval == PAM_SUCCESS) &&
		    (options->ignore_afs == 0) &&
		    (options->tokens == 1) &&
		    tokens_useful()) {
			tokens_obtain(ctx, stash, options, userinfo, 1);
		}
	}

	/* If we didn't use the first password (because it wasn't set), and we
	 * didn't ask for a password (due to the "no_initial_prompt" flag,
	 * probably), and we can let libkrb5 ask questions (no
	 * "no_subsequent_prompt"), then let libkrb5 have another go. */
	if ((retval != PAM_SUCCESS) &&
	    (retval != PAM_USER_UNKNOWN) &&
	    use_third_pass) {
		if (options->debug) {
			debug("not using an entered password for '%s', "
			      "allowing libkrb5 to prompt for more", user);
		}
		retval = v5_get_creds(stash->v5ctx, pamh,
				      &stash->v5ccache,
				      &stash->v5armorccache,
				      user, userinfo,
				      options,
				      KRB5_TGS_NAME,
				      NULL,
				      gic_options,
				      options->permit_password_callback ?
				      _pam_krb5_always_prompter :
				      _pam_krb5_normal_prompter,
				      &stash->v5expired,
				      &stash->v5result);
		stash->v5external = 0;
		stash->v5attempted = 1;
		if (options->debug) {
			debug("got result %d (%s)", stash->v5result,
			      v5_error_message(stash->v5result));
		}
		if ((retval == PAM_SUCCESS) &&
		    (options->ignore_afs == 0) &&
		    (options->tokens == 1) &&
		    tokens_useful()) {
			tokens_obtain(ctx, stash, options, userinfo, 1);
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

	/* Log the authentication status, optionally saving the credentials in
	 * a piece of shared memory. */
	if (retval == PAM_SUCCESS) {
		if (options->use_shmem) {
			_pam_krb5_stash_shm_write(pamh, stash, options,
						  user, userinfo);
		}
		notice("authentication succeeds for '%s' (%s)", user,
		       userinfo->unparsed_name);
	} else {
		if ((retval == PAM_USER_UNKNOWN) &&
		    options->ignore_unknown_principals) {
			retval = PAM_IGNORE;
		} else {
			notice("authentication fails for '%s' (%s): %s (%s)",
			       user,
			       userinfo->unparsed_name,
			       pam_strerror(pamh, retval),
			       v5_error_message(stash->v5result));
		}
	}

	/* Clean up. */
	if (options->debug) {
		debug("pam_authenticate returning %d (%s)", retval,
		      pam_strerror(pamh, retval));
	}
	v5_free_get_init_creds_opt(ctx, gic_options);
	_pam_krb5_options_free(pamh, ctx, options);
	_pam_krb5_user_info_free(ctx, userinfo);
	_pam_krb5_free_ctx(ctx);

	return retval;
}

int
pam_sm_setcred(pam_handle_t *pamh, int flags,
	       int argc, PAM_KRB5_MAYBE_CONST char **argv)
{
	const char *why = "";
	if (flags & PAM_ESTABLISH_CRED) {
		return _pam_krb5_open_session(pamh, flags, argc, argv,
					      "pam_setcred(PAM_ESTABLISH_CRED)",
					      _pam_krb5_session_caller_setcred);
	}
	if (flags & (PAM_REINITIALIZE_CRED | PAM_REFRESH_CRED)) {
		if (flags & PAM_REINITIALIZE_CRED) {
			why = "pam_setcred(PAM_REINITIALIZE_CRED)";
			if (flags & PAM_REFRESH_CRED) {
				why = "pam_setcred(PAM_REINITIALIZE_CRED|PAM_REFRESH_CRED)";
			}
		} else {
			why = "pam_setcred(PAM_REFRESH_CRED)";
		}
		if (_pam_krb5_sly_looks_unsafe() == 0) {
			return _pam_krb5_sly_maybe_refresh(pamh, flags, why,
							   argc, argv);
		} else {
			return PAM_IGNORE;
		}
	}
	if (flags & PAM_DELETE_CRED) {
		return _pam_krb5_close_session(pamh, flags, argc, argv,
					       "pam_setcred(PAM_DELETE_CRED)",
					       _pam_krb5_session_caller_setcred);
	}
	warn("pam_setcred() called with no flags");
	return PAM_SERVICE_ERR;
}
