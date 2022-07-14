/*
 * Copyright 2003,2006,2007,2009,2011,2012 Red Hat, Inc.
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

#ifndef pam_krb5_v5_h
#define pam_krb5_v5_h

#include "options.h"
#include "stash.h"
#include "userinfo.h"

#define PAM_KRB5_PRINCIPAL_COMPONENT_SEPARATORS ",/@"

int v5_get_creds(krb5_context ctx,
		 pam_handle_t *pamh,
		 krb5_ccache *ccache,
		 krb5_ccache *armor_ccache,
		 const char *user,
		 struct _pam_krb5_user_info *userinfo,
		 struct _pam_krb5_options *options,
		 char *service,
		 char *password,
		 krb5_get_init_creds_opt *gic_options,
		 krb5_error_code prompter(krb5_context,
					  void *,
					  const char *,
					  const char *,
					  int,
					  krb5_prompt[]),
		 int *expired,
		 int *result);

int v5_save_for_user(krb5_context ctx,
		     struct _pam_krb5_stash *stash,
		     const char *user,
		     struct _pam_krb5_user_info *userinfo,
		     struct _pam_krb5_options *options,
		     const char **ccname);
int v5_save_for_kuserok(krb5_context ctx,
			struct _pam_krb5_stash *stash,
			const char *user,
			struct _pam_krb5_user_info *userinfo,
			struct _pam_krb5_options *options,
			const char **ccname);
void v5_destroy(krb5_context ctx, struct _pam_krb5_stash *stash,
	        struct _pam_krb5_options *options);

krb5_error_code v5_ccache_has_tgt(krb5_context ctx, krb5_ccache ccache,
				  const char *tgs_realm, krb5_creds *creds);
krb5_error_code v5_ccache_has_pwc(krb5_context ctx, krb5_ccache ccache,
				  krb5_creds *creds);
krb5_error_code v5_cc_copy(krb5_context ctx, const char *tgt_realm,
			   krb5_ccache occache, krb5_ccache *nccache);
int v5_creds_check_initialized(krb5_context ctx, krb5_creds *creds);
int v5_creds_check_initialized_pwc(krb5_context ctx, krb5_creds *creds);
int v5_creds_get_etype(krb5_creds *creds);
void v5_creds_set_etype(krb5_context ctx, krb5_creds *creds, int etype);
krb5_keyblock *v5_creds_get_key(krb5_creds *creds);
int v5_enctype_to_string(krb5_context ctx, krb5_enctype enctype,
			 char *buf, size_t length);

krb5_principal v5_ticket_get_client(krb5_ticket *ticket);
krb5_error_code v5_auth_con_setuserkey(krb5_context ctx,
				       krb5_auth_context auth_con,
				       krb5_keyblock *key);

void v5_free_unparsed_name(krb5_context ctx, char *name);
void v5_free_default_realm(krb5_context ctx, char *realm);
void v5_appdefault_string(krb5_context context,
			  const char *realm,
			  const char *option,
			  const char *default_value,
			  char **ret_value);
void v5_appdefault_boolean(krb5_context context,
			   const char *realm,
			   const char *option,
			   krb5_boolean default_value,
			   krb5_boolean *ret_value);

const char *v5_error_message(int error);
const char *v5_passwd_error_message(int error);

int v5_set_principal_realm(krb5_context ctx, krb5_principal *principal,
			   const char *realm);

int v5_cc_retrieve_match(void);

krb5_keyblock *v5_creds_key(krb5_creds *creds);
int v5_creds_key_type(krb5_creds *creds);
int v5_creds_key_length(krb5_creds *creds);
const unsigned char *v5_creds_key_contents(krb5_creds *creds);
krb5_flags v5_creds_get_flags(krb5_creds *creds);
krb5_boolean v5_creds_get_is_skey(krb5_creds *creds);
int v5_creds_address_count(krb5_creds *creds);
int v5_creds_address_type(krb5_creds *creds, int i);
int v5_creds_address_length(krb5_creds *creds, int i);
const unsigned char *v5_creds_address_contents(krb5_creds *creds, int i);
int v5_creds_authdata_count(krb5_creds *creds);
int v5_creds_authdata_type(krb5_creds *creds, int i);
int v5_creds_authdata_length(krb5_creds *creds, int i);
const unsigned char *v5_creds_authdata_contents(krb5_creds *creds, int i);
int v5_princ_component_count(krb5_principal princ);
int v5_princ_component_type(krb5_principal princ, int i);
int v5_princ_component_length(krb5_principal princ, int i);
const char *v5_princ_component_contents(krb5_principal princ, int i);
int v5_princ_realm_length(krb5_principal princ);
const char *v5_princ_realm_contents(krb5_principal princ);

krb5_error_code v5_parse_name(krb5_context ctx,
			      struct _pam_krb5_options *options,
			      const char *name,
			      krb5_principal *principal);
krb5_error_code v5_alloc_get_init_creds_opt(krb5_context ctx,
					    krb5_get_init_creds_opt **opt);
void v5_free_get_init_creds_opt(krb5_context ctx,
				krb5_get_init_creds_opt *opt);
char *v5_user_info_subst(krb5_context ctx,
			 const char *user,
			 struct _pam_krb5_user_info *userinfo,
			 struct _pam_krb5_options *options,
			 const char *template_value);
int v5_change_password(krb5_context ctx, krb5_creds *creds, char *password,
		       int *result_code, krb5_data *result_code_string,
		       krb5_data *result_string);
#endif
