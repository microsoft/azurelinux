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

#include <sys/types.h>
#include <sys/stat.h>

#ifdef HAVE_SECURITY_PAM_APPL_H
#include <security/pam_appl.h>
#endif

#ifdef HAVE_SECURITY_PAM_MODULES_H
#define PAM_SM_PASSWORD
#include <security/pam_modules.h>
#endif

#include <limits.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include KRB5_H

#include "conv.h"
#include "init.h"
#include "initopts.h"
#include "items.h"
#include "log.h"
#include "options.h"
#include "prompter.h"
#include "stash.h"
#include "userinfo.h"
#include "v5.h"
#include "xstr.h"

int
pam_sm_chauthtok(pam_handle_t *pamh, int flags,
		 int argc, PAM_KRB5_MAYBE_CONST char **argv)
{
	PAM_KRB5_MAYBE_CONST char *user;
	char prompt[LINE_MAX], prompt2[LINE_MAX], *password, *password2;
	krb5_context ctx;
	krb5_creds pwc_creds;
	struct _pam_krb5_options *options;
	struct _pam_krb5_user_info *userinfo;
	struct _pam_krb5_stash *stash;
	krb5_get_init_creds_opt *gic_options, *tmp_gicopts;
	int tmp_result, prelim_attempted;
	int i, retval, use_third_pass;
	char *pwhelp;
	struct stat st;
	FILE *fp;
	struct pam_message message;

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
					 _pam_krb5_option_role_chauthtok);
	if (options == NULL) {
		warn("error parsing options (shouldn't happen)");
		v5_free_get_init_creds_opt(ctx, gic_options);
		_pam_krb5_free_ctx(ctx);
		return PAM_SERVICE_ERR;
	}
	_pam_krb5_set_init_opts(ctx, gic_options, options);

	/* Get information about the user and the user's principal name. */
	userinfo = _pam_krb5_user_info_init(ctx, user, options);
	if (userinfo == NULL) {
		if (options->ignore_unknown_principals) {
			retval = PAM_IGNORE;
		} else {
			warn("error getting information about '%s'", user);
			retval = PAM_USER_UNKNOWN;
		}
		_pam_krb5_options_free(pamh, ctx, options);
		v5_free_get_init_creds_opt(ctx, gic_options);
		_pam_krb5_free_ctx(ctx);
		return retval;
	}

	/* Check the minimum UID argument. */
	if ((options->user_check) &&
	    (options->minimum_uid != (uid_t)-1) &&
	    (userinfo->uid < options->minimum_uid)) {
		if (options->debug) {
			debug("ignoring '%s' -- uid below minimum = %lu", user,
			      (unsigned long) options->minimum_uid);
		}
		_pam_krb5_user_info_free(ctx, userinfo);
		_pam_krb5_options_free(pamh, ctx, options);
		v5_free_get_init_creds_opt(ctx, gic_options);
		_pam_krb5_free_ctx(ctx);
		return PAM_IGNORE;
	}

	/* Get the stash of credentials.  If we are interactively prompting
	 * the user for information, we're not expected to ask for the user's
	 * current password more than once, so we use it to get a changepw
	 * ticket during the first pass, and we store that for use in the
	 * second pass.  It should have a low lifetime, so we needn't free it
	 * just now. */
	retval = PAM_AUTH_ERR;
	stash = _pam_krb5_stash_get(pamh, user, userinfo, options);

	/* If this is the first pass, just check the user's password by
	 * obtaining a password-changing initial ticket. */
	if (flags & PAM_PRELIM_CHECK) {
		retval = PAM_AUTH_ERR;
		prelim_attempted = 0;

		/* Ideally we're only going to let libkrb5 ask questions once,
		 * and after that we intend to lie to it. */
		use_third_pass = options->use_third_pass;

		/* Set up options for getting password-changing creds. */
		i = v5_alloc_get_init_creds_opt(ctx, &tmp_gicopts);
		if (i == 0) {
			/* Set hard-coded defaults for password-changing creds
			 * which might not match generally-used options. */
			_pam_krb5_set_init_opts_for_pwchange(ctx,
							     tmp_gicopts,
							     options);
		} else {
			/* Try library defaults. */
			tmp_gicopts = NULL;
		}

		/* Display password help text. */
		if ((options->pwhelp != NULL) && (options->pwhelp[0] != '\0')) {
			fp = fopen(options->pwhelp, "r");
			if (fp != NULL) {
				if (options->debug) {
					debug("opened help file '%s'",
					      options->pwhelp);
				}
				if (fstat(fileno(fp), &st) != -1) {
					pwhelp = malloc(st.st_size + 1);
					if (pwhelp == NULL) {
						memset(prompt, '\0',
						       sizeof(prompt));
						i = fread(prompt, 1,
							  sizeof(prompt) -1,
							  fp);
						pwhelp = prompt;
					} else {
						memset(pwhelp, '\0',
						       st.st_size + 1);
						i = fread(pwhelp, 1,
							  st.st_size, fp);
						if (options->debug) {
							debug("read %d bytes",
							      (int) st.st_size);
						}
					}
				} else {
					memset(prompt, '\0', sizeof(prompt));
					i = fread(prompt, 1,
						  sizeof(prompt) - 1, fp);
					pwhelp = prompt;
				}
				if (i > 0) {
					message.msg = pwhelp;
					message.msg_style = PAM_TEXT_INFO;
					_pam_krb5_conv_call(pamh, &message, 1,
							    NULL);
				}
				if (pwhelp != prompt) {
					xstrfree(pwhelp);
				}
				fclose(fp);
			} else {
				if (options->debug) {
					debug("failed to open help file '%s'",
					      options->pwhelp);
				}
			}
		}

		/* Obtain the current password. */
		password = NULL;
		if (options->use_first_pass) {
			/* Read the stored password. */
			password = NULL;
			i = _pam_krb5_get_item_text(pamh, PAM_OLDAUTHTOK,
						    &password);
			/* Duplicate the password so that we can free it later
			 * without corrupting the heap. */
			if ((password != NULL) && (i == PAM_SUCCESS)) {
				password = xstrdup(password);
			}
		}
		if ((password != NULL) && (i == PAM_SUCCESS)) {
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
			/* We have a password, so try to obtain initial
			 * credentials using the password. */
			i = v5_get_creds(stash->v5ctx, pamh,
					 &stash->v5ccache,
					 &stash->v5armorccache,
					 user, userinfo,
					 options,
					 PASSWORD_CHANGE_PRINCIPAL,
					 password, tmp_gicopts,
					 use_third_pass ?
					 _pam_krb5_normal_prompter :
					 _pam_krb5_previous_prompter,
					 NULL,
					 &tmp_result);
			prelim_attempted = 1;
			use_third_pass = 0;
			if (options->debug) {
				debug("Got %d (%s) acquiring credentials for "
				      "%s: %s.",
				      tmp_result, v5_error_message(tmp_result),
				      PASSWORD_CHANGE_PRINCIPAL,
				      pam_strerror(pamh, i));
			}
			if (i != PAM_SUCCESS) {
				/* No joy. */
				xstrfree(password);
				password = NULL;
			}
			retval = i;
		}
		if ((retval != PAM_SUCCESS) &&
		    (password == NULL) &&
		    options->use_second_pass) {
			/* Ask the user for a password. */
			sprintf(prompt, Y_("%s%sPassword: "),
				options->banner,
				strlen(options->banner) > 0 ? " " : "");
			i = _pam_krb5_prompt_for(pamh, prompt, &password);
			/* Save the old password for possible use by other
			 * modules. */
			if ((password != NULL) && (i == PAM_SUCCESS)) {
				pam_set_item(pamh, PAM_OLDAUTHTOK, password);
			}
		}
		/* We have a second password, so try to obtain initial
		 * credentials using the password. */
		if ((retval != PAM_SUCCESS) &&
		    ((password != NULL) && (i == PAM_SUCCESS))) {
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
			i = v5_get_creds(stash->v5ctx, pamh,
					 &stash->v5ccache,
					 &stash->v5armorccache,
					 user, userinfo,
					 options,
					 PASSWORD_CHANGE_PRINCIPAL,
					 password, tmp_gicopts,
					 use_third_pass ?
					 _pam_krb5_normal_prompter :
					 _pam_krb5_always_fail_prompter,
					 NULL,
					 &tmp_result);
			prelim_attempted = 1;
			use_third_pass = 0;
			if (options->debug) {
				debug("Got %d (%s) acquiring credentials for "
				      "%s.",
				      tmp_result, v5_error_message(tmp_result),
				      PASSWORD_CHANGE_PRINCIPAL);
			}
			retval = i;
		}
		/* We haven't tried anything yet, so if it's allowed, try to
		 * obtain initial credentials, letting libkrb5 ask the
		 * questions. */
		if ((retval != PAM_SUCCESS) &&
		    (prelim_attempted == 0) &&
		    use_third_pass) {
			if (options->debug) {
				debug("not using an entered password for '%s', "
				      "allowing libkrb5 to prompt", user);
			}
			i = v5_get_creds(stash->v5ctx, pamh,
					 &stash->v5ccache,
					 &stash->v5armorccache,
					 user, userinfo,
					 options,
					 PASSWORD_CHANGE_PRINCIPAL,
					 NULL, tmp_gicopts,
					 options->permit_password_callback ?
					 _pam_krb5_always_prompter :
					 _pam_krb5_normal_prompter,
					 NULL,
					 &tmp_result);
			prelim_attempted = 1;
			use_third_pass = 0;
			if (options->debug) {
				debug("Got %d (%s) acquiring credentials for "
				      "%s.",
				      tmp_result, v5_error_message(tmp_result),
				      PASSWORD_CHANGE_PRINCIPAL);
			}
			retval = i;
		}

		/* Clean up the password-changing options. */
		v5_free_get_init_creds_opt(ctx, tmp_gicopts);
		/* Free [the copy of] the password. */
		xstrfree(password);
	}

	/* If this is the second pass, get the new password, use the
	 * credentials which we obtained and stashed in the first pass to set
	 * the user's password, and then use the new password to obtain a TGT.
	 * (If we're changing an expired password, then we'll need it to create
	 * a ccache file later.) */
	if (flags & PAM_UPDATE_AUTHTOK) {
		retval = PAM_AUTHTOK_ERR;
		password = NULL;

		/* If our preliminary check succeeded, then we'll have
		 * password-changing credentials. */
		if (v5_ccache_has_pwc(ctx, stash->v5ccache, NULL) == 0) {
			/* The new password (if it's already been requested by
			 * a previously-called module) is stored as the
			 * PAM_AUTHTOK item.  The old one is stored as the
			 * PAM_OLDAUTHTOK item, but we don't use it here. */
			i = _pam_krb5_get_item_text(pamh, PAM_AUTHTOK,
						    &password);

			/* Duplicate the password, as above. */
			if ((password != NULL) && (i == PAM_SUCCESS)) {
				password = xstrdup(password);
			} else {
				/* Indicate that we didn't get a satisfactory
				 * password, but we can ask the user. */
				retval = PAM_AUTHTOK_ERR;
				password = NULL;
			}

			/* If there wasn't a previously-entered password, and
			 * we can't ask the user, then return an error. */
			if ((password == NULL) && (options->use_authtok)) {
				retval = PAM_AUTHTOK_RECOVER_ERR;
			}
		} else {
			/* If we didn't pass the preliminary check, then stand
			 * back and let whichever module it was that told the
			 * calling application it was okay to continue to do
			 * its thing. */
			if (options->ignore_unknown_principals) {
				debug("no password-changing credentials for "
				      "'%s' obtained, ignoring user",
				      userinfo->unparsed_name);
				retval = PAM_IGNORE;
			} else {
				debug("no password-changing credentials for "
				      "'%s' obtained, user not known",
				      userinfo->unparsed_name);
				retval = PAM_USER_UNKNOWN;
			}
		}

		/* If there wasn't a previously-entered password, and we are
		 * okay with that, ask for one. */
		if ((password == NULL) && (retval == PAM_AUTHTOK_ERR)) {
			/* Ask for the new password twice. */
			sprintf(prompt, Y_("New %s%sPassword: "),
				options->banner,
				strlen(options->banner) > 0 ? " " : "");
			sprintf(prompt2, Y_("Repeat New %s%sPassword: "),
				options->banner,
				strlen(options->banner) > 0 ? " " : "");
			i = _pam_krb5_prompt_for_2(pamh, prompt, &password,
						   prompt2, &password2);
			/* If they're not the same, return PAM_TRY_AGAIN. */
			if (strcmp(password, password2) != 0) {
				i = PAM_TRY_AGAIN;
				retval = PAM_TRY_AGAIN;
			}
			/* Save the password for possible use by other
			 * modules. */
			if (i == PAM_SUCCESS) {
				pam_set_item(pamh, PAM_AUTHTOK, password);
			}
			/* Free the second password, we only need one copy. */
			xstrfree(password2);
			password2 = NULL;
		}

		/* We have the new password, so attempt to change the user's
		 * password using the previously-acquired password-changing
		 * ticket. */
		memset(&pwc_creds, 0, sizeof(pwc_creds));
		if ((password != NULL) &&
		    (retval == PAM_AUTHTOK_ERR) &&
		    (v5_ccache_has_pwc(ctx, stash->v5ccache, &pwc_creds) == 0)) {
			int result_code;
			krb5_data result_code_string, result_string;
			result_code = -1;
			result_string.length = 0;
			result_string.data = NULL;
			result_code_string.length = 0;
			result_code_string.data = NULL;
			i = v5_change_password(ctx, &pwc_creds, password,
					       &result_code,
					       &result_code_string,
					       &result_string);
			krb5_free_cred_contents(ctx, &pwc_creds);
			if ((i == 0) && (result_code == 0)) {
				notice("password changed for %s",
				       userinfo->unparsed_name);
				retval = PAM_SUCCESS;
			} else {
				if (i != 0) {
					notice("password change failed for "
					       "%s: %s",
					       userinfo->unparsed_name,
					       v5_error_message(i));
				} else {
					notice("password change failed for "
					       "%s: %s: %.*s %s%.*s%s",
					       userinfo->unparsed_name,
					       v5_passwd_error_message(result_code),
					       (int) result_code_string.length,
					       (char *) result_code_string.data,
					       result_string.length ? "(" : "",
					       (int) result_string.length,
					       (char *) result_string.data,
					       result_string.length ? ")" : "");
				}
				if ((result_string.length > 0) ||
				    (result_code_string.length > 0)) {
					notice_user(pamh, "%s: %.*s %s%.*s%s\n",
						    v5_passwd_error_message(result_code),
						    (int) result_code_string.length,
						    (const char *) result_code_string.data,
						    result_string.length ?
						    "(" : "",
						    (int) result_string.length,
						    (const char *) result_string.data,
						    result_string.length ?
						    ")" : "");
				}
			}
		}

		/* If we succeeded, obtain a new TGT using the new password. */
		if (retval == PAM_SUCCESS) {
			if (options->debug) {
				debug("obtaining credentials using new "
				      "password for '%s'",
				      userinfo->unparsed_name);
			}
			i = v5_get_creds(stash->v5ctx, pamh, &stash->v5ccache,
					 &stash->v5armorccache,
					 user, userinfo, options,
					 KRB5_TGS_NAME,
					 password, gic_options,
					 _pam_krb5_always_fail_prompter,
					 NULL,
					 &stash->v5result);
			stash->v5attempted = 1;
			if (i == PAM_SUCCESS) {
				if (options->use_shmem) {
					_pam_krb5_stash_shm_write(pamh, stash,
								  options,
								  user, userinfo);
				}
			}
		}

		/* Free the new password. */
		if (password != NULL) {
			xstrfree(password);
		}
	}

	/* Clean up. */
	if (options->debug) {
		debug("pam_chauthtok (%s) returning %d (%s)",
		      (flags & PAM_PRELIM_CHECK) ?
		      "preliminary check" :
		      ((flags & PAM_UPDATE_AUTHTOK) ?
		       "updating authtok":
		       "unknown phase"),
		      retval, pam_strerror(pamh, retval));
	}
	_pam_krb5_user_info_free(ctx, userinfo);
	_pam_krb5_options_free(pamh, ctx, options);
	v5_free_get_init_creds_opt(ctx, gic_options);
	_pam_krb5_free_ctx(ctx);
	return retval;
}
