/*
 * Copyright 2003,2005,2006,2008,2009,2010,2011,2012,2013,2014 Red Hat, Inc.
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

#ifndef pam_krb5_options_h
#define pam_krb5_options_h

struct _pam_krb5_options {
	int debug;
	int argc;
	PAM_KRB5_MAYBE_CONST char **argv;

#ifdef HAVE_KRB5_ANAME_TO_LOCALNAME
	int always_allow_localname;
#endif
#if defined(HAVE_KRB5_GET_INIT_CREDS_OPT_SET_FAST_CCACHE) && \
    defined(HAVE_KRB5_GET_INIT_CREDS_OPT_SET_FAST_FLAGS)
	int armor;
	char *armor_strategy;
#endif
#ifdef HAVE_KRB5_GET_INIT_CREDS_OPT_SET_CANONICALIZE
	int canonicalize;
#endif
	int chpw_prompt;
	int cred_session;
	int debug_sensitive;
	int external;
	int ignore_afs;
	int ignore_k5login;
	int ignore_unknown_principals;
	int multiple_ccaches;
	int null_afs_first;
	int permit_password_callback;
	int test_environment;
	int tokens;
#ifdef HAVE_KRB5_SET_TRACE_CALLBACK
	int trace;
#endif
	int user_check;
	int use_authtok;
	int use_first_pass;
	int use_second_pass;
	int use_third_pass;
	int use_shmem;
	int validate;
	int validate_user_user;
	int warn;

	uid_t minimum_uid;

	char *banner;
	char *ccache_dir;
	char *cchelper_path;
	char *ccname_template;
	char *keytab;
	char *pwhelp;
	char *realm;
	char *token_strategy;
	char **hosts;

#ifdef HAVE_KRB5_GET_INIT_CREDS_OPT_SET_PKINIT
	char *pkinit_identity;
	int pkinit_flags;
#endif
#ifdef HAVE_KRB5_GET_INIT_CREDS_OPT_SET_PA
	char **preauth_options;
#endif

	struct afs_cell {
		char *cell, *principal_name;
	} *afs_cells;
	int n_afs_cells;

	char *mappings_s;
	struct name_mapping {
		char *pattern, *replacement;
	} *mappings;
	int n_mappings;
};

enum _pam_krb5_option_role {
	_pam_krb5_option_role_general,
	_pam_krb5_option_role_chauthtok,
};

struct _pam_krb5_options *_pam_krb5_options_init(pam_handle_t *pamh,
						 int argc,
						 PAM_KRB5_MAYBE_CONST char **argv,
						 krb5_context ctx,
						 enum _pam_krb5_option_role role);
void _pam_krb5_options_free(pam_handle_t *pamh,
			    krb5_context ctx,
			    struct _pam_krb5_options *options);

#endif
