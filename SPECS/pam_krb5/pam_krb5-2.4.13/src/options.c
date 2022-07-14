/*
 * Copyright 2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014 Red Hat, Inc.
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
#include <sys/types.h>
#include <ctype.h>
#include <errno.h>
#include <pwd.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#ifdef HAVE_SECURITY_PAM_APPL_H
#include <security/pam_appl.h>
#endif

#ifdef HAVE_SECURITY_PAM_MODULES_H
#include <security/pam_modules.h>
#endif

#include KRB5_H

#ifdef HAVE_PROFILE_H
#include <profile.h>
#endif

#include "items.h"
#include "log.h"
#include "options.h"
#include "userinfo.h"
#include "v5.h"
#include "xstr.h"

#define LIST_SEPARATORS " \t,"

static char **option_l(int argc, PAM_KRB5_MAYBE_CONST char **argv,
		       krb5_context ctx, const char *realm,
		       const char *s, const char *def);
static char ** option_l_from_s(const char *o);
static void free_l(char **l);

static int
option_b(int argc, PAM_KRB5_MAYBE_CONST char **argv,
	 krb5_context ctx, const char *realm,
	 const char *service,
	 const char *default_services, const char *default_notservices,
	 const char *s, int default_value)
{
	int i, j, ret;
	unsigned int n;
	krb5_boolean retbool;
	char **list, *nots;
	const char *prefix[] = {"not", "dont", "no", "not_", "dont_", "no_"};

	for (i = 0; i < argc; i++) {
		/* boolean yes */
		if (strcmp(argv[i], s) == 0) {
			return 1;
		}
		/* boolean no */
		for (n = 0; n < (sizeof(prefix) / sizeof(prefix[0])); n++) {
			if ((strncmp(argv[i], prefix[n],
				     strlen(prefix[n])) == 0) &&
			    (strcmp(argv[i] + strlen(prefix[n]), s) == 0)) {
				return 0;
			}
		}
	}

	ret = -1;

	/* configured service yes */
	if ((ret == -1) && (realm != NULL) &&
	    (service != NULL) && (strlen(service) > 0)) {
		list = option_l(argc, argv, ctx, realm, s, "");
		if (list != NULL) {
			for (i = 0;
			     ((list != NULL) && (list[i] != NULL));
			     i++) {
				if (strcmp(list[i], service) == 0) {
					ret = 1;
					break;
				}
			}
			free_l(list);
		}
	}

	/* configured service no */
	if ((ret == -1) && (realm != NULL) &&
	    (service != NULL) && (strlen(service) > 0)) {
		for (n = 0; n < (sizeof(prefix) / sizeof(prefix[0])); n++) {
			nots = malloc(strlen(prefix[n]) + strlen(s) + 1);
			if (nots != NULL) {
				sprintf(nots, "%s%s", prefix[n], s);
				list = option_l(argc, argv, ctx, realm,
						nots, "");
				if (list != NULL) {
					for (j = 0; list[j] != NULL; j++) {
						if (strcmp(list[j],
							   service) == 0) {
							ret = 0;
							break;
						}
					}
					free_l(list);
				}
				free(nots);
			}
			if (ret != -1) {
				break;
			}
		}
	}

	/* configured boolean */
	if ((ret == -1) && (realm != NULL)) {
		v5_appdefault_boolean(ctx, realm, s, -1, &retbool);
		ret = retbool;
	}

	/* compile-time default service yes */
	if ((ret == -1) && (default_services != NULL)) {
		list = option_l_from_s(default_services);
		for (i = 0; ((list != NULL) && (list[i] != NULL)); i++) {
			if (strcmp(list[i], service) == 0) {
				ret = 1;
				break;
			}
		}
		free_l(list);
	}

	/* compile-time default service no */
	if ((ret == -1) && (default_notservices != NULL)) {
		list = option_l_from_s(default_notservices);
		for (i = 0; ((list != NULL) && (list[i] != NULL)); i++) {
			if (strcmp(list[i], service) == 0) {
				ret = 0;
				break;
			}
		}
		free_l(list);
	}

	/* hard-coded default */
	switch (ret) {
	case -1:
		retbool = default_value;
		break;
	default:
		retbool = ret;
		break;
	}
	return retbool;
}

static char *
option_s(int argc, PAM_KRB5_MAYBE_CONST char **argv,
	 krb5_context ctx, const char *realm, const char *s,
	 const char *default_value)
{
	int i;
	char *o;

	for (i = 0; i < argc; i++) {
		if ((strncmp(argv[i], s, strlen(s)) == 0) &&
		    (argv[i][strlen(s)] == '=')) {
			return xstrdup(argv[i] + strlen(s) + 1);
		}
	}

	v5_appdefault_string(ctx, realm, s, default_value, &o);

	return o;
}
static void
free_s(char *s)
{
	xstrfree(s);
}
#ifdef HAVE_LONG_LONG
static long long
#else
static long
#endif
option_i(int argc, PAM_KRB5_MAYBE_CONST char **argv,
	 krb5_context ctx, const char *realm, const char *s)
{
	char *tmp, *p;
#ifdef HAVE_LONG_LONG
	long long i;
#else
	long i;
#endif

	tmp = option_s(argc, argv, ctx, realm, s, "");

#ifdef HAVE_STRTOLL
	i = strtoll(tmp, &p, 10);
#else
	i = strtol(tmp, &p, 10);
#endif
	if ((p == NULL) || (p == tmp) || (*p != '\0')) {
		i = -1;
	}
	free_s(tmp);

	return i;
}
#if 0
static krb5_deltat
option_t(int argc, PAM_KRB5_MAYBE_CONST char **argv,
	 krb5_context ctx, const char *realm, const char *s)
{
	char *tmp, *p;
	krb5_deltat d;
	long i;

	tmp = option_s(argc, argv, ctx, realm, s, "");

	i = strtol(tmp, &p, 10);
	if ((p == NULL) || (p == tmp) || (*p != '\0')) {
		i = -1;
		if (krb5_string_to_deltat(tmp, &d) == 0) {
			free_s(tmp);
			return d;
		}
	}
	free_s(tmp);

	return i;
}
#endif
static char **
option_l(int argc, PAM_KRB5_MAYBE_CONST char **argv,
	 krb5_context ctx, const char *realm, const char *s, const char *def)
{
	char *o, **list;

	o = option_s(argc, argv, ctx, realm, s, def ? def : "");
	list = option_l_from_s(o);
	free_s(o);
	return list;
}

static char **
option_l_from_s(const char *o)
{
	int i;
	char **list;
	const char *p, *q;

	list = malloc((strlen(o) + 1) * sizeof(char*));
	if (list == NULL) {
		return NULL;
	}
	memset(list, 0, (strlen(o) + 1) * sizeof(char*));

	i = 0;
	p = q = o;
	do {
		q = p + strcspn(p, LIST_SEPARATORS);
		if (p != q) {
			list[i++] = xstrndup(p, q - p);
		}
		p = q + strspn(q, LIST_SEPARATORS);
	} while (*p != '\0');

	if (list[0] == NULL) {
		free(list);
		list = NULL;
	}
	return list;
}

static void
free_l(char **l)
{
	int i;
	if (l != NULL) {
		for (i = 0; l[i] != NULL; i++) {
			free_s(l[i]);
			l[i] = NULL;
		}
		free(l);
	}
}

struct _pam_krb5_options *
_pam_krb5_options_init(pam_handle_t *pamh, int argc,
		       PAM_KRB5_MAYBE_CONST char **argv,
		       krb5_context ctx,
		       enum _pam_krb5_option_role role)
{
	struct _pam_krb5_options *options;
	int try_first_pass, use_first_pass, initial_prompt, subsequent_prompt;
	int i;
	char *default_realm, *default_ccname, **list;
	char *service;

	options = malloc(sizeof(struct _pam_krb5_options));
	if (options == NULL) {
		return NULL;
	}
	memset(options, 0, sizeof(struct _pam_krb5_options));
	options->argc = argc;
	options->argv = argv;

	service = NULL;
	if (pamh != NULL) {
		_pam_krb5_get_item_text(pamh, PAM_SERVICE, &service);
	}

	/* command-line option */
	options->debug = option_b(argc, argv, ctx, NULL,
				  service, NULL, NULL,
				  "debug", 0);

	for (i = 0; i < argc; i++) {
		if (strncmp(argv[i], "realm=", 6) == 0) {
			if (options->realm != NULL) {
				xstrfree(options->realm);
			}
			options->realm = xstrdup(argv[i] + 6);
		}
	}
	if (krb5_get_default_realm(ctx, &default_realm) == 0) {
		if (options->debug) {
			debug("default/local realm '%s'", default_realm);
		}
		if (options->realm == NULL) {
			options->realm = xstrdup(default_realm);
		}
		v5_free_default_realm(ctx, default_realm);
	}
	if (options->realm == NULL) {
		options->realm = xstrdup(DEFAULT_REALM);
	}
	if (strlen(options->realm) > 0) {
		krb5_set_default_realm(ctx, options->realm);
		if (options->debug) {
			debug("configured realm '%s'", options->realm);
		}
	}

	/* parsing debugging */
	for (i = 0; i < argc; i++) {
		if (strcmp(argv[i], "debug_parser") == 0) {
			char *s, **l;
			i = option_b(argc, argv, ctx, options->realm,
				     service, NULL, NULL,
				     "boolean_parameter_1", -1);
			debug("boolean_parameter_1 = %d", i);
			i = option_b(argc, argv, ctx, options->realm,
				     service, NULL, NULL,
				     "boolean_parameter_2", 0);
			debug("boolean_parameter_2 = %d", i);
			i = option_b(argc, argv, ctx, options->realm,
				     service, NULL, NULL,
				     "boolean_parameter_3", 1);
			debug("boolean_parameter_3 = %d", i);
			s = option_s(argc, argv,
				     ctx, options->realm, "string_parameter_1",
				     "default_string_value");
			debug("string_parameter_1 = '%s'", s ? s : "(null)");
			free_s(s);
			s = option_s(argc, argv,
				     ctx, options->realm, "string_parameter_2",
				     "default_string_value");
			debug("string_parameter_2 = '%s'", s ? s : "(null)");
			free_s(s);
			s = option_s(argc, argv,
				     ctx, options->realm, "string_parameter_3",
				     "default_string_value");
			debug("string_parameter_3 = '%s'", s ? s : "(null)");
			free_s(s);
			l = option_l(argc, argv,
				     ctx, options->realm, "list_parameter_1",
				     "");
			for (i = 0; (l != NULL) && (l[i] != NULL); i++) {
				debug("list_parameter_1[%d] = '%s'", i, l[i]);
			}
			free_l(l);
			break;
		}
	}

	/* private option */
	options->debug = option_b(argc, argv, ctx, options->realm,
				  service, NULL, NULL,
				  "debug", 0);
	if (options->debug) {
		debug("flag: debug");
	}

#ifdef HAVE_KRB5_SET_TRACE_CALLBACK
	options->trace = option_b(argc, argv, ctx, options->realm,
				  service, NULL, NULL,
				  "trace", 0);
	if (options->trace) {
		debug("flag: trace");
		krb5_set_trace_callback(ctx, &trace, NULL);
	}
#endif

	/* undocumented private option */
	options->test_environment = option_b(argc, argv, ctx, options->realm,
					     service, NULL, NULL,
					     "test_environment", 0);
	if (options->test_environment) {
		debug("flag: test_environment");
	}

#if defined(HAVE_KRB5_GET_INIT_CREDS_OPT_SET_FAST_CCACHE) && \
    defined(HAVE_KRB5_GET_INIT_CREDS_OPT_SET_FAST_FLAGS)
	/* private options */
	options->armor = option_b(argc, argv, ctx, options->realm,
				  service, NULL, NULL,
				  "armor", 0);
	if (options->armor) {
		debug("flag: armor");
	}
	options->armor_strategy = option_s(argc, argv,
					   ctx, options->realm, "armor_strategy",
					   DEFAULT_ARMOR_STRATEGY);
#endif

	/* private option */
	options->debug_sensitive = option_b(argc, argv, ctx, options->realm,
					    service, NULL, NULL,
					    "debug_sensitive", 0);
	if (options->debug && options->debug_sensitive) {
		debug("flag: debug_sensitive");
	}

	/* undocumented private option */
	options->cchelper_path = option_s(argc, argv,
					  ctx, options->realm, "cchelper_path",
					  PKGSECURITYDIR "/pam_krb5_cchelper");

#ifdef HAVE_KRB5_GET_INIT_CREDS_OPT_SET_CANONICALIZE
	options->canonicalize = option_b(argc, argv,
					 ctx, options->realm,
					 service, NULL, NULL,
					 "canonicalize", -1);
	if (options->debug && (options->canonicalize == 1)) {
		debug("flag: canonicalize");
	}
	if (options->debug && (options->canonicalize == 0)) {
		debug("flag: don't canonicalize");
	}
#endif

#ifdef HAVE_KRB5_ANAME_TO_LOCALNAME
	/* private option */
	options->always_allow_localname = option_b(argc, argv,
						   ctx, options->realm,
						   service, NULL, NULL,
						   "always_allow_localname",
						   0);
	if (options->debug && (options->always_allow_localname == 1)) {
		debug("flag: always_allow_localname");
	}
	if (options->debug && (options->always_allow_localname == 0)) {
		debug("flag: don't always_allow_localname");
	}
#endif
#ifdef HAVE_AFS
	/* private option */
	options->ignore_afs = option_b(argc, argv,
				       ctx, options->realm,
				       service, NULL, NULL, "ignore_afs", 0);
	if (options->debug && (options->ignore_afs == 1)) {
		debug("flag: ignore_afs");
	}
	if (options->debug && (options->ignore_afs == 0)) {
		debug("flag: no ignore_afs");
	}

	/* private option */
	options->null_afs_first = option_b(argc, argv,
					   ctx, options->realm,
					   service, NULL, NULL, "null_afs", -1);
	if (options->null_afs_first == -1) {
		options->null_afs_first = option_b(argc, argv,
						   ctx, options->realm,
						   service, NULL, NULL,
						   "nullafs", 0);
	}
	if (options->debug && (options->null_afs_first == 1)) {
		debug("flag: null_afs");
	}
	if (options->debug && (options->null_afs_first == 0)) {
		debug("flag: no null_afs");
	}

	/* private option */
	options->tokens = option_b(argc, argv, ctx, options->realm,
				   service, NULL, NULL, "tokens", 0);
	if (options->debug && options->tokens) {
		debug("flag: tokens");
	}
#else
	options->ignore_afs = 1;
	options->tokens = 0;
#endif

	/* private option */
	options->cred_session = option_b(argc, argv,
					 ctx, options->realm,
					 service, NULL, DEFAULT_NO_CRED_SESSION,
					 "cred_session", 1);
	if (options->debug && (options->cred_session == 1)) {
		debug("flag: cred_session");
	}
	if (options->debug && (options->cred_session == 0)) {
		debug("flag: no cred_session");
	}

	/* private option */
	options->ignore_k5login = option_b(argc, argv,
					   ctx, options->realm,
					   service, NULL, NULL,
					   "ignore_k5login", 0);
	if (options->debug && (options->ignore_k5login == 1)) {
		debug("flag: ignore_k5login");
	}
	if (options->debug && (options->ignore_k5login == 0)) {
		debug("flag: no ignore_k5login");
	}

#ifdef HAVE_KRB5_GET_INIT_CREDS_OPT_SET_PKINIT
	/* option specific to the Heimdal implementation */
	options->pkinit_identity = option_s(argc, argv, ctx, options->realm,
					    "pkinit_identity",
					    DEFAULT_PKINIT_IDENTITY);
	if (options->debug && options->pkinit_identity) {
		debug("pkinit_identity(template): %s",
		      options->pkinit_identity);
	}
	options->pkinit_flags = option_i(argc, argv,
					 ctx, options->realm, "pkinit_flags");
	if (options->pkinit_flags == -1) {
		options->pkinit_flags = 0;
	}
	if (options->debug) {
		debug("pkinit_flags: %d", options->pkinit_flags);
	}
#endif
#ifdef HAVE_KRB5_GET_INIT_CREDS_OPT_SET_PA
	/* option specific to the MIT implementation */
	options->preauth_options = option_l(argc, argv, ctx, options->realm,
					    "preauth_options",
					    DEFAULT_PREAUTH_OPTIONS);
	if (options->debug && options->preauth_options) {
		int i;
		for (i = 0; options->preauth_options[i] != NULL; i++) {
			debug("preauth_options(template): %s",
			      options->preauth_options[i]);
		}
	}
#endif
#ifdef HAVE_KRB5_GET_INIT_CREDS_OPT_SET_CHANGE_PASSWORD_PROMPT
	/* library option */
	options->chpw_prompt = option_b(argc, argv,
				        ctx, options->realm,
				        service,
					DEFAULT_CHPW_PROMPT, "",
					"chpw_prompt", 0);
	if (options->debug && options->user_check) {
		debug("flag: chpw_prompt");
	}
#endif

	/* private option */
	options->user_check = option_b(argc, argv,
				       ctx, options->realm,
				       service, NULL, NULL, "user_check", 1);
	if (options->debug && options->user_check) {
		debug("flag: user_check");
	}

	/* private option */
	options->use_authtok = option_b(argc, argv,
					ctx, options->realm,
					service, NULL, NULL, "use_authtok", 0);
	if (options->debug && options->use_authtok) {
		debug("flag: use_authtok");
	}

	/* private option */
	options->use_first_pass = 1;
	options->use_second_pass = 1;
	options->use_third_pass = (role != _pam_krb5_option_role_chauthtok);
	options->permit_password_callback = 0;
	use_first_pass = option_b(argc, argv,
				  ctx, options->realm,
				  service, NULL, NULL, "use_first_pass", -1);
	try_first_pass = option_b(argc, argv,
				  ctx, options->realm,
				  service, NULL, NULL, "try_first_pass", -1);
	initial_prompt = option_b(argc, argv,
				  ctx, options->realm,
				  service, NULL, NULL, "initial_prompt", -1);
	subsequent_prompt = option_b(argc, argv,
				     ctx, options->realm,
				     service, NULL, NULL,
				     "subsequent_prompt", -1);
	if (initial_prompt != -1) {
		options->use_second_pass = initial_prompt;
		options->permit_password_callback = !initial_prompt;
	}
	if (subsequent_prompt != -1) {
		options->use_third_pass = subsequent_prompt;
	}
	if (use_first_pass == 1) {
		options->use_second_pass = 0;
	}
	if (try_first_pass == 1) {
		options->use_second_pass = 1;
	}
	if (options->debug) {
		if (options->use_first_pass == 1) {
			debug("will try previously set password first");
		}
		if (options->use_second_pass == 1) {
			if (options->use_first_pass == 1) {
				debug("will ask for a password if that fails");
			} else {
				debug("will ask for a password");
			}
		}
		if (options->use_third_pass == 1) {
			debug("will let libkrb5 ask questions");
		} else {
			debug("will not let libkrb5 ask questions");
		}
	}

	/* private option */
	options->use_shmem = option_b(argc, argv,
				      ctx, options->realm,
				      service, DEFAULT_USE_SHMEM, NULL,
				      "use_shmem", 0);
	if (options->debug && (options->use_shmem == 1)) {
		debug("flag: use_shmem");
	}
	if (options->debug && (options->use_shmem == 0)) {
		debug("flag: no use_shmem");
	}

	/* private option */
	options->external = option_b(argc, argv,
				     ctx, options->realm,
				     service, DEFAULT_EXTERNAL, "",
				     "external", 0);
	if (options->debug && (options->external == 1)) {
		debug("flag: external");
	}
	if (options->debug && (options->external == 0)) {
		debug("flag: no external");
	}

	/* private option */
	options->multiple_ccaches = option_b(argc, argv,
					     ctx, options->realm,
					     service,
					     DEFAULT_MULTIPLE_CCACHES, "",
					     "multiple_ccaches", 0);
	if (options->debug && (options->multiple_ccaches == 1)) {
		debug("flag: multiple_ccaches");
	}
	if (options->debug && (options->multiple_ccaches == 0)) {
		debug("flag: no multiple_ccaches");
	}

	/* private option */
	options->validate = option_b(argc, argv,
				     ctx, options->realm,
				     service, NULL, NULL,
				     "validate", 1);
	if (options->debug && (options->validate == 1)) {
		debug("flag: validate");
	}
	options->validate_user_user = option_b(argc, argv,
					       ctx, options->realm,
					       service, NULL, NULL,
					       "validate_user_user", 0);
	if (options->debug && (options->validate_user_user == 1)) {
		debug("flag: validate_user_user");
	}

	options->warn = option_b(argc, argv,
				 ctx, options->realm,
				 service, NULL, NULL, "warn", 1);
	if (options->debug && (options->warn == 1)) {
		debug("flag: warn");
	}

	/* private option */
	options->minimum_uid = option_i(argc, argv,
					ctx, options->realm, "minimum_uid");
	if (options->debug && (options->minimum_uid != (uid_t) -1)) {
		debug("minimum uid: %d", options->minimum_uid);
	}

	/* private options */
	options->banner = option_s(argc, argv,
				   ctx, options->realm, "banner",
				   "Kerberos 5");
	if (options->debug && options->banner) {
		debug("banner: %s", options->banner);
	}
	options->ccache_dir = option_s(argc, argv,
				       ctx, options->realm, "ccache_dir",
				       DEFAULT_CCACHE_DIR);
	if (strlen(options->ccache_dir) == 0) {
		xstrfree(options->ccache_dir);
		options->ccache_dir = xstrdup(DEFAULT_CCACHE_DIR);
	}
	if (options->debug && options->ccache_dir) {
		debug("ccache dir: %s", options->ccache_dir);
	}
	default_ccname = NULL;
#ifdef DEFAULT_CCNAME_FROM_LIBKRB5
	{
		profile_t profile;
		if (krb5_get_profile(ctx, &profile) == 0) {
			char *profile_value = NULL;
			if (profile_get_string(profile,
					       "libdefaults",
					       "default_ccache_name",
					       NULL,
					       NULL,
					       &profile_value) == 0) {
				if (profile_value != NULL) {
					if (strlen(profile_value) > 0) {
						default_ccname =
							xstrdup(profile_value);
					}
					profile_release_string(profile_value);
				}
			}
			profile_release(profile);
		}
	}
#endif
	options->ccname_template = option_s(argc, argv,
					    ctx, options->realm,
					    "ccname_template",
					    default_ccname ?
					    default_ccname :
					    DEFAULT_CCNAME_TEMPLATE);
	xstrfree(default_ccname);
	if (strlen(options->ccname_template) == 0) {
		xstrfree(options->ccname_template);
		options->ccname_template = xstrdup(DEFAULT_CCNAME_TEMPLATE);
	}
	if (options->debug && options->ccname_template) {
		debug("ccname template: %s", options->ccname_template);
	}

	if (service != NULL) {
		list = option_l(argc, argv, ctx, options->realm,
				"keytab", DEFAULT_KEYTAB_LOCATION);
		for (i = 0; (list != NULL) && (list[i] != NULL); i++) {
			if ((strncmp(list[i], service, strlen(service)) == 0) &&
			    (list[i][strlen(service)] == '=')) {
				options->keytab = xstrdup(list[i] +
							  strlen(service) + 1);
				break;
			}
		}
		if ((list != NULL) && (i > 0) && (list[i] == NULL)) {
			for (i = 0; (list != NULL) && (list[i] != NULL); i++) {
				if (strchr(list[i], '=') == NULL) {
					options->keytab = xstrdup(list[i]);
					break;
				}
			}
		}
		free_l(list);
	}
	if (strlen(options->keytab) == 0) {
		xstrfree(options->keytab);
		options->keytab = xstrdup(DEFAULT_KEYTAB_LOCATION);
	}
	if (options->debug && options->keytab) {
		debug("keytab: %s", options->keytab);
	}

	options->pwhelp = option_s(argc, argv,
				   ctx, options->realm, "pwhelp",
				   "");
	if (strlen(options->pwhelp) == 0) {
		xstrfree(options->pwhelp);
		options->pwhelp = NULL;
	}
	if (options->debug && options->pwhelp) {
		debug("pwhelp: %s", options->pwhelp);
	}

	options->token_strategy = option_s(argc, argv,
					   ctx, options->realm,
					   "token_strategy", "");
	if (strlen(options->token_strategy) == 0) {
		xstrfree(options->token_strategy);
		options->token_strategy = xstrdup(DEFAULT_TOKEN_STRATEGY);
	}
	if (options->debug && options->token_strategy) {
		debug("token strategy: %s", options->token_strategy);
	}

	options->ignore_unknown_principals = option_b(argc, argv, ctx,
						      options->realm,
						      service, NULL, NULL,
						      "ignore_unknown_principals", -1);
	if (options->ignore_unknown_principals == -1) {
		options->ignore_unknown_principals = option_b(argc, argv, ctx,
							      options->realm,
							      service,
							      NULL, NULL,
							      "ignore_unknown_spn",
							      -1);
	}
	if (options->ignore_unknown_principals == -1) {
		options->ignore_unknown_principals = option_b(argc, argv, ctx,
							      options->realm,
							      service,
							      NULL, NULL,
							      "ignore_unknown_upn",
							      -1);
	}
	if (options->ignore_unknown_principals == -1) {
		options->ignore_unknown_principals = 0;
	}

	/* If /afs is on a different device from /, this suggests that AFS is
	 * running.  Set up to get tokens for the local cell and attempt to
	 * get that cell's name if we're not ignoring AFS altogether. */
	if (!options->ignore_afs) {
		list = option_l(argc, argv, ctx, options->realm, "afs_cells",
				"");
		if ((list != NULL) && (list[0] != NULL)) {
			int i;
			char *p;
			/* count the number of cells */
			for (i = 0; list[i] != NULL; i++) {
				continue;
			}
			/* allocate the cell data array */
			options->afs_cells = malloc(sizeof(struct afs_cell) *
						    i);
			if (options->afs_cells != NULL) {
				memset(options->afs_cells, 0,
				       sizeof(struct afs_cell) * i);
				options->n_afs_cells = i;
				for (i = 0; i < options->n_afs_cells; i++) {
					/* everything up to an "=", if there is
					 * one, is the cell name */
					p = list[i];
					options->afs_cells[i].cell =
						xstrndup(p, strcspn(p, "="));
					p += strcspn(p, "=");
					p += strspn(p, "=");
					if (strlen(p) > 0) {
						options->afs_cells[i].principal_name =
							xstrdup(p);
					}
				}
			}
			free_l(list);
		}
		if (options->debug && options->afs_cells) {
			int i;
			for (i = 0; i < options->n_afs_cells; i++) {
				if (options->afs_cells[i].principal_name != NULL) {
					debug("afs cell: %s (%s)",
					      options->afs_cells[i].cell,
					      options->afs_cells[i].principal_name);
				} else {
					debug("afs cell: %s",
					      options->afs_cells[i].cell);
				}
			}
		}
	}

	options->mappings_s = option_s(argc, argv,
				       ctx, options->realm, "mappings", "");
	list = option_l(argc, argv, ctx, options->realm, "mappings", "");
	for (i = 0; (list != NULL) && (list[i] != NULL); i++) {
		/* nothing */
	}
	if ((i == 0) || ((i % 2) != 0)) {
		options->n_mappings = 0;
		options->mappings = NULL;
	} else {
		options->n_mappings = i / 2;
		options->mappings = malloc(sizeof(struct name_mapping) *
					   options->n_mappings);
		if (options->mappings == NULL) {
			options->n_mappings = 0;
		}
		for (i = 0; i < options->n_mappings; i++) {
			options->mappings[i].pattern = xstrdup(list[i * 2]);
			options->mappings[i].replacement =
				xstrdup(list[i * 2 + 1]);
			if (options->debug) {
				debug("mapping: \"%s\" to \"%s\"",
				      options->mappings[i].pattern,
				      options->mappings[i].replacement);
			}
		}
	}
	free_l(list);

	return options;
}
void
_pam_krb5_options_free(pam_handle_t *pamh, krb5_context ctx,
		       struct _pam_krb5_options *options)
{
	int i;
#ifdef HAVE_KRB5_GET_INIT_CREDS_OPT_SET_PKINIT
	free_s(options->pkinit_identity);
	options->pkinit_identity = NULL;
#endif
#ifdef HAVE_KRB5_GET_INIT_CREDS_OPT_SET_PA
	free_l(options->preauth_options);
	options->preauth_options = NULL;
#endif
	free_s(options->banner);
	options->banner = NULL;
	free_s(options->ccache_dir);
	options->ccache_dir = NULL;
	free_s(options->ccname_template);
	options->ccname_template = NULL;
	free_s(options->keytab);
	options->keytab = NULL;
	free_s(options->pwhelp);
	options->pwhelp = NULL;
	free_s(options->token_strategy);
	options->token_strategy = NULL;
#if defined(HAVE_KRB5_GET_INIT_CREDS_OPT_SET_FAST_CCACHE) && \
    defined(HAVE_KRB5_GET_INIT_CREDS_OPT_SET_FAST_FLAGS)
	free_s(options->armor_strategy);
	options->armor_strategy = NULL;
#endif
	free_s(options->cchelper_path);
	options->cchelper_path = NULL;
	free_s(options->realm);
	options->realm = NULL;
	free_l(options->hosts);
	options->hosts = NULL;
	for (i = 0; i < options->n_afs_cells; i++) {
		xstrfree(options->afs_cells[i].cell);
		xstrfree(options->afs_cells[i].principal_name);
	}
	free(options->afs_cells);
	options->afs_cells = NULL;
	for (i = 0; i < options->n_mappings; i++) {
		xstrfree(options->mappings[i].pattern);
		xstrfree(options->mappings[i].replacement);
	}
	free(options->mappings);
	options->mappings = NULL;
	free(options->mappings_s);
	options->mappings_s = NULL;
	free(options);
};
