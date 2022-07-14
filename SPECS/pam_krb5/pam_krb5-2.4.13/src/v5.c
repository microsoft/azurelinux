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

#include <errno.h>
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

#ifndef HAVE_ERROR_MESSAGE_DECL
#ifdef HAVE_COM_ERR_H
#include <com_err.h>
#elif defined(HAVE_ET_COM_ERR_H)
#include <et/com_err.h>
#endif
#endif

#include "conv.h"
#include "initopts.h"
#include "log.h"
#include "perms.h"
#include "prompter.h"
#include "sly.h"
#include "stash.h"
#include "userinfo.h"
#include "v5.h"
#include "xstr.h"

#ifndef KRB5_KPASSWD_ACCESSDENIED
#define KRB5_KPASSWD_ACCESSDENIED 5
#endif
#ifndef KRB5_KPASSWD_BAD_VERSION
#define KRB5_KPASSWD_BAD_VERSION  6
#endif
#ifndef KRB5_KPASSWD_INITIAL_FLAG_NEEDED
#define KRB5_KPASSWD_INITIAL_FLAG_NEEDED 7
#endif

const char *
v5_error_message(krb5_error_code error)
{
	return error_message(error);
}
const char *
v5_passwd_error_message(int error)
{
	switch (error) {
	case KRB5_KPASSWD_SUCCESS:
		return "Success";
		break;
	case KRB5_KPASSWD_MALFORMED:
		return "Malformed request";
		break;
	case KRB5_KPASSWD_HARDERROR:
		return "Password change failed";
		break;
	case KRB5_KPASSWD_AUTHERROR:
		return "Authentication error";
		break;
	case KRB5_KPASSWD_SOFTERROR:
		return "Password change rejected";
		break;
	case KRB5_KPASSWD_ACCESSDENIED:
		return "Access denied";
		break;
	case KRB5_KPASSWD_BAD_VERSION:
		return "Bad version";
		break;
	case KRB5_KPASSWD_INITIAL_FLAG_NEEDED:
		return "Attempted to authenticate using non-initial credentials";
		break;
	}
	return "Unknown error";
}

krb5_error_code
v5_alloc_get_init_creds_opt(krb5_context ctx, krb5_get_init_creds_opt **opt)
{
#ifdef HAVE_KRB5_GET_INIT_CREDS_OPT_ALLOC_FREE
	/* Do NOT call krb5_get_init_creds_opt_init(), which in both Heimdal
	 * and MIT Kerberos cause the structure to be marked as not having
	 * extended data members which are used to store preauth and pkinit
	 * settings. */
	*opt = NULL;
	return krb5_get_init_creds_opt_alloc(ctx, opt);
#else
	*opt = malloc(sizeof(**opt));
	if (*opt != NULL) {
		memset(*opt, 0, sizeof(**opt));
		krb5_get_init_creds_opt_init(*opt);
		return 0;
	} else {
		return ENOMEM;
	}
#endif
}

void
v5_free_get_init_creds_opt(krb5_context ctx, krb5_get_init_creds_opt *opt)
{
#ifdef HAVE_KRB5_GET_INIT_CREDS_OPT_ALLOC_FREE
#ifdef KRB5_GET_INIT_CREDS_OPT_ALLOC_FREE_TAKES_2_ARGS
	krb5_get_init_creds_opt_free(ctx, opt);
#else
	krb5_get_init_creds_opt_free(opt);
#endif
#else
	free(opt);
#endif
}

krb5_error_code
v5_parse_name(krb5_context ctx, struct _pam_krb5_options *options,
	      const char *name, krb5_principal *principal)
{
#if defined(HAVE_KRB5_PARSE_NAME_FLAGS) && defined(HAVE_KRB5_GET_INIT_CREDS_OPT_SET_CANONICALIZE)
	int flags;
	flags = 0;
	if (options->canonicalize == 1) {
		flags |= KRB5_PRINCIPAL_PARSE_ENTERPRISE;
	}
	return krb5_parse_name_flags(ctx, name, flags, principal);
#else
	return krb5_parse_name(ctx, name, principal);
#endif
}

char *
v5_user_info_subst(krb5_context ctx,
		   const char *user,
		   struct _pam_krb5_user_info *userinfo,
		   struct _pam_krb5_options *options,
		   const char *template_value)
{
	char *ret;
	int i, j, len;

	ret = NULL;
	len = strlen(template_value);
	for (i = 0; template_value[i] != '\0'; i++) {
		switch (template_value[i]) {
		case '%':
			switch (template_value[i + 1]) {
			case 'p':
				len += strlen(userinfo->unparsed_name);
				i++;
				break;
			case 'u':
				len += strlen(user);
				i++;
				break;
			case 'U':
#ifdef HAVE_LONG_LONG
				len += sizeof(unsigned long long) * 4;
#else
				len += sizeof(unsigned long) * 4;
#endif
				i++;
				break;
			case 'P':
				len += sizeof(pid_t) * 4;
				i++;
				break;
			case 'r':
				len += strlen(userinfo->realm);
				i++;
				break;
			case 'h':
				len += strlen(userinfo->homedir ?
					      userinfo->homedir :
					      "/");
				i++;
			case 'd':
				len += strlen(options->ccache_dir);
				i++;
				break;
			case '{':
				if (strncasecmp(template_value + i + 1,
						"{uid}", 5) == 0) {
#ifdef HAVE_LONG_LONG
					len += sizeof(unsigned long long) * 4;
#else
					len += sizeof(unsigned long) * 4;
#endif
					i += 5;
				} else
				if (strncasecmp(template_value + i + 1,
						"{euid}", 6) == 0) {
#ifdef HAVE_LONG_LONG
					len += sizeof(unsigned long long) * 4;
#else
					len += sizeof(unsigned long) * 4;
#endif
					i += 6;
				} else
				if (strncasecmp(template_value + i + 1,
						"{userid}", 8) == 0) {
#ifdef HAVE_LONG_LONG
					len += sizeof(unsigned long long) * 4;
#else
					len += sizeof(unsigned long) * 4;
#endif
					i += 8;
				} else
				if (strncasecmp(template_value + i + 1,
						"{username}", 10) == 0) {
					len += strlen(user);
					i += 10;
				}
				break;
			default:
			case '%':
				break;
			}
		default:
			break;
		}
	}
	ret = malloc(len + 1);
	if (ret == NULL) {
		return NULL;
	}
	memset(ret, '\0', len + 1);
	for (i = 0, j = 0; template_value[i] != '\0'; i++) {
		switch (template_value[i]) {
		case '%':
			switch (template_value[i + 1]) {
			case 'p':
				strcat(ret, userinfo->unparsed_name);
				i++;
				j = strlen(ret);
				break;
			case 'u':
				strcat(ret, user);
				i++;
				j = strlen(ret);
				break;
			case 'U':
#ifdef HAVE_LONG_LONG
				sprintf(ret + j, "%llu",
					options->user_check ?
					(unsigned long long) userinfo->uid :
					(unsigned long long) getuid());
#else
				sprintf(ret + j, "%lu",
					options->user_check ?
					(unsigned long) userinfo->uid :
					(unsigned long) getuid());
#endif
				i++;
				j = strlen(ret);
				break;
			case 'P':
				sprintf(ret + j, "%ld", (long) getpid());
				i++;
				j = strlen(ret);
				break;
			case 'r':
				strcat(ret, userinfo->realm);
				i++;
				j = strlen(ret);
				break;
			case 'h':
				strcat(ret,
				       userinfo->homedir ?
				       userinfo->homedir : "/");
				i++;
				j = strlen(ret);
				break;
			case 'd':
				strcat(ret, options->ccache_dir);
				i++;
				j = strlen(ret);
				break;
			case '{':
				if (strncasecmp(template_value + i + 1,
						"{uid}", 5) == 0) {
#ifdef HAVE_LONG_LONG
				sprintf(ret + j, "%llu",
					options->user_check ?
					(unsigned long long) userinfo->uid :
					(unsigned long long) getuid());
#else
				sprintf(ret + j, "%lu",
					options->user_check ?
					(unsigned long) userinfo->uid :
					(unsigned long) getuid());
#endif
					i += 5;
					j = strlen(ret);
				} else
				if (strncasecmp(template_value + i + 1,
						"{euid}", 6) == 0) {
#ifdef HAVE_LONG_LONG
				sprintf(ret + j, "%llu",
					options->user_check ?
					(unsigned long long) userinfo->uid :
					(unsigned long long) geteuid());
#else
				sprintf(ret + j, "%lu",
					options->user_check ?
					(unsigned long) userinfo->uid :
					(unsigned long) geteuid());
#endif
					i += 6;
					j = strlen(ret);
				} else
				if (strncasecmp(template_value + i + 1,
						"{userid}", 8) == 0) {
#ifdef HAVE_LONG_LONG
				sprintf(ret + j, "%llu",
					options->user_check ?
					(unsigned long long) userinfo->uid :
					(unsigned long long) getuid());
#else
				sprintf(ret + j, "%lu",
					options->user_check ?
					(unsigned long) userinfo->uid :
					(unsigned long) getuid());
#endif
					i += 8;
					j = strlen(ret);
				} else
				if (strncasecmp(template_value + i + 1,
						"{username}", 10) == 0) {
					strcat(ret, user);
					i += 10;
					j = strlen(ret);
				}
				break;
			case '%':
				strcat(ret, "%");
				i++;
				j = strlen(ret);
				break;
			default:
				strcat(ret, "%");
				j = strlen(ret);
				break;
			}
			break;
		default:
			ret[j++] = template_value[i];
			break;
		}
	}
	ret[j] = '\0';
	return ret;
}

#ifdef HAVE_KRB5_XFREE
void
v5_free_unparsed_name(krb5_context ctx, char *name)
{
	krb5_xfree(name);
}
#elif defined(HAVE_KRB5_FREE_UNPARSED_NAME)
void
v5_free_unparsed_name(krb5_context ctx, char *name)
{
	krb5_free_unparsed_name(ctx, name);
}
#else
void
v5_free_unparsed_name(krb5_context ctx, char *name)
{
#ifdef HAVE_KRB5_FREE_STRING
	krb5_free_string(ctx, name);
#else
	xstrfree(name);
#endif
}
#endif

#ifdef HAVE_KRB5_FREE_DEFAULT_REALM
void
v5_free_default_realm(krb5_context ctx, char *realm)
{
	krb5_free_default_realm(ctx, realm);
}
#else
void
v5_free_default_realm(krb5_context ctx, char *realm)
{
#ifdef HAVE_KRB5_FREE_STRING
	krb5_free_string(ctx, realm);
#else
	xstrfree(realm);
#endif
}
#endif

static int
v5_cc_get_full_name(krb5_context ctx, krb5_ccache ccache, char **name)
{
#ifdef HAVE_KRB5_CC_GET_FULL_NAME
	return krb5_cc_get_full_name(ctx, ccache, name);
#else
	const char *ctype, *cname;
	ctype = krb5_cc_get_type(ctx, ccache);
	cname = krb5_cc_get_name(ctx, ccache);
	if ((ctype == NULL) || (cname == NULL)) {
		return ENOENT;
	}
	*name = malloc(strlen(ctype) + 1 + strlen(cname) + 1);
	if (*name == NULL) {
		return ENOMEM;
	}
	sprintf(*name, "%s:%s", ctype, cname);
	return 0;
#endif
}

static void
v5_free_cc_full_name(krb5_context ctx, char *name)
{
#ifdef HAVE_KRB5_FREE_STRING
	krb5_free_string(ctx, name);
#else
	xstrfree(name);
#endif
}

#ifdef HAVE_KRB5_SET_PRINCIPAL_REALM
int
v5_set_principal_realm(krb5_context ctx, krb5_principal *principal,
		       const char *realm)
{
	return krb5_set_principal_realm(ctx, *principal, realm);
}
#else
int
v5_set_principal_realm(krb5_context ctx, krb5_principal *principal,
		       const char *realm)
{
	char *unparsed, *tmp;
	int i;
	if (krb5_unparse_name(ctx, *principal, &unparsed) == 0) {
		tmp = malloc(strlen(unparsed) + 1 + strlen(realm) + 1);
		if (tmp != NULL) {
			strcpy(tmp, unparsed);
			if (strrchr(tmp, '@') != NULL) {
				strcpy(strrchr(tmp, '@') + 1, realm);
			} else {
				strcat(tmp, "@");
				strcat(tmp, realm);
			}
			i = krb5_parse_name(ctx, tmp, principal);
			v5_free_unparsed_name(ctx, unparsed);
			xstrfree(tmp);
			return i;
		}
	}
	return KRB5KRB_ERR_GENERIC;
}
#endif

#if defined(HAVE_KRB5_PRINCIPAL_DATA) && defined(HAVE_KRB5_PRINCIPAL_DATA_REALM_LENGTH) && defined(HAVE_KRB5_PRINCIPAL_DATA_REALM_DATA) && defined(HAVE_KRB5_PRINCIPAL_DATA_LENGTH) && defined(HAVE_KRB5_PRINCIPAL_DATA_DATA)
int
v5_princ_component_count(krb5_principal princ)
{
	return princ->length;
}
int
v5_princ_component_length(krb5_principal princ, int i)
{
	return princ->data[i].length;
}
const char *
v5_princ_component_contents(krb5_principal princ, int i)
{
	return princ->data[i].data;
}
int
v5_princ_realm_length(krb5_principal princ)
{
	return princ->realm.length;
}
const char *
v5_princ_realm_contents(krb5_principal princ)
{
	return princ->realm.data;
}
#elif defined(HAVE_KRB5_PRINCIPAL_DATA) && defined(HAVE_KRB5_PRINCIPAL_DATA_REALM) && defined(HAVE_KRB5_PRINCIPAL_DATA_NAME_NAME_STRING_LEN) && defined(HAVE_KRB5_PRINCIPAL_DATA_NAME_NAME_STRING_VAL)
int
v5_princ_component_count(krb5_principal princ)
{
	return princ->name.name_string.len;
}
int
v5_princ_component_length(krb5_principal princ, int i)
{
	return strlen(princ->name.name_string.val[i]);
}
const char *
v5_princ_component_contents(krb5_principal princ, int i)
{
	return princ->name.name_string.val[i];
}
int
v5_princ_realm_length(krb5_principal princ)
{
	return strlen(princ->realm);
}
const char *
v5_princ_realm_contents(krb5_principal princ)
{
	return princ->realm;
}
#else
#error "Don't know how to read principal name components!"
#endif

/* Compare everything except the realms. */
static int
v5_principal_compare_no_realm(krb5_context ctx, krb5_principal princ,
			      const char *name)
{
	int i;
	krb5_principal temp;
	temp = NULL;
	if ((i = krb5_parse_name(ctx, name, &temp)) != 0) {
		return i;
	}
	if (v5_princ_component_count(princ) != v5_princ_component_count(temp)) {
		krb5_free_principal(ctx, temp);
		return 1;
	}
	for (i = 0; i < v5_princ_component_count(princ); i++) {
		if ((v5_princ_component_length(princ, i) !=
		     v5_princ_component_length(temp, i)) ||
		    (memcmp(v5_princ_component_contents(princ, i),
			    v5_princ_component_contents(temp, i),
			    v5_princ_component_length(princ, i)) != 0)) {
			break;
		}
	}
	krb5_free_principal(ctx, temp);
	if (i == v5_princ_component_count(princ)) {
		return 0;
	}
	return 1;
}

#if defined(HAVE_KRB5_CREDS_KEYBLOCK) && defined(HAVE_KRB5_KEYBLOCK_ENCTYPE) && defined(HAVE_KRB5_KEYBLOCK_LENGTH) && defined(HAVE_KRB5_KEYBLOCK_CONTENTS)
krb5_keyblock *
v5_creds_get_key(krb5_creds *creds)
{
	return &creds->keyblock;
}
int
v5_creds_get_etype(krb5_creds *creds)
{
	return creds->keyblock.enctype;
}
void
v5_creds_set_etype(krb5_context ctx, krb5_creds *creds, int etype)
{
	creds->keyblock.enctype = etype;
}
int
v5_creds_check_initialized(krb5_context ctx, krb5_creds *creds)
{
	return ((creds->client != NULL) &&
		(creds->server != NULL) &&
		(creds->keyblock.length > 0) &&
		(creds->ticket.length > 0)) ? 0 : 1;
}
int
v5_creds_check_initialized_pwc(krb5_context ctx, krb5_creds *creds)
{
	return ((creds->client != NULL) &&
		(creds->server != NULL) &&
		(creds->keyblock.length > 0) &&
		(creds->ticket.length > 0) &&
		(creds->server->length >= 2) &&
		(v5_principal_compare_no_realm(ctx, creds->server,
					       PASSWORD_CHANGE_PRINCIPAL) == 0)) ? 0 : 1;
}
krb5_keyblock *
v5_creds_key(krb5_creds *creds)
{
	return &creds->keyblock;
}
int
v5_creds_key_type(krb5_creds *creds)
{
	return creds->keyblock.enctype;
}
int
v5_creds_key_length(krb5_creds *creds)
{
	return creds->keyblock.length;
}
const unsigned char *
v5_creds_key_contents(krb5_creds *creds)
{
	return creds->keyblock.contents;
}
#elif defined(HAVE_KRB5_CREDS_SESSION) && defined(HAVE_KRB5_KEYBLOCK_KEYTYPE) && defined(HAVE_KRB5_KEYBLOCK_KEYVALUE)
krb5_keyblock *
v5_creds_get_key(krb5_creds *creds)
{
	return &creds->session;
}
int
v5_creds_get_etype(krb5_creds *creds)
{
	return creds->session.keytype;
}
void
v5_creds_set_etype(krb5_context ctx, krb5_creds *creds, int etype)
{
	creds->session.keytype = etype;
}
int
v5_creds_check_initialized(krb5_context ctx, krb5_creds *creds)
{
	return (creds->session.keyvalue.length > 0) ? 0 : 1;
}
int
v5_creds_check_initialized_pwc(krb5_context ctx, krb5_creds *creds)
{
	return ((creds->session.keyvalue.length > 0) &&
		(v5_principal_compare_no_realm(ctx, creds->server,
					       PASSWORD_CHANGE_PRINCIPAL) == 0)) ? 0 : 1;
}
krb5_keyblock *
v5_creds_key(krb5_creds *creds)
{
	return &creds->session;
}
int
v5_creds_key_type(krb5_creds *creds)
{
	return creds->session.keytype;
}
int
v5_creds_key_length(krb5_creds *creds)
{
	return creds->session.keyvalue.length;
}
const unsigned char *
v5_creds_key_contents(krb5_creds *creds)
{
	return creds->session.keyvalue.data;
}
#else
#error "Don't know how to read/write key types for your Kerberos implementation!"
#endif

#if defined(HAVE_KRB5_ADDRESSES) && defined(HAVE_KRB5_ADDRESS_ADDR_TYPE) && defined(HAVE_KRB5_ADDRESS_ADDRESS)
int
v5_creds_address_count(krb5_creds *creds)
{
	return creds->addresses.len;
}
int
v5_creds_address_type(krb5_creds *creds, int i)
{
	return creds->addresses.val[i].addr_type;
}
int
v5_creds_address_length(krb5_creds *creds, int i)
{
	return creds->addresses.val[i].address.length;
}
const unsigned char *
v5_creds_address_contents(krb5_creds *creds, int i)
{
	return creds->addresses.val[i].address.data;
}
#elif defined(HAVE_KRB5_ADDRESS_ADDRTYPE) && defined(HAVE_KRB5_ADDRESS_LENGTH) && defined(HAVE_KRB5_ADDRESS_CONTENTS)
int
v5_creds_address_count(krb5_creds *creds)
{
	int i;
	for (i = 0;
	     (creds->addresses != NULL) && (creds->addresses[i] != NULL);
	     i++) {
		continue;
	}
	return i;
}
int
v5_creds_address_type(krb5_creds *creds, int i)
{
	return creds->addresses ? creds->addresses[i]->addrtype : 0;
}
int
v5_creds_address_length(krb5_creds *creds, int i)
{
	return creds->addresses ? creds->addresses[i]->length : 0;
}
const unsigned char *
v5_creds_address_contents(krb5_creds *creds, int i)
{
	return creds->addresses ? creds->addresses[i]->contents : NULL;
}
#else
#error "Don't know how to read addresses for your Kerberos implementation!"
#endif

#if defined(HAVE_KRB5_AUTHDATA_VAL)
int
v5_creds_authdata_count(krb5_creds *creds)
{
	return creds->authdata.len;
}
int
v5_creds_authdata_type(krb5_creds *creds, int i)
{
	return creds->authdata.val[i].ad_type;
}
int
v5_creds_authdata_length(krb5_creds *creds, int i)
{
	return creds->authdata.val[i].ad_data.length;
}
const unsigned char *
v5_creds_authdata_contents(krb5_creds *creds, int i)
{
	return creds->authdata.val[i].ad_data.data;
}
#elif defined(HAVE_KRB5_AUTHDATA_AD_TYPE) && defined(HAVE_KRB5_AUTHDATA_LENGTH) && defined(HAVE_KRB5_AUTHDATA_CONTENTS)
int
v5_creds_authdata_count(krb5_creds *creds)
{
	int i;
	for (i = 0;
	     (creds->authdata != NULL) && (creds->authdata[i] != NULL);
	     i++) {
		continue;
	}
	return i;
}
int
v5_creds_authdata_type(krb5_creds *creds, int i)
{
	return creds->authdata ? creds->authdata[i]->ad_type : 0;
}
int
v5_creds_authdata_length(krb5_creds *creds, int i)
{
	return creds->authdata ? creds->authdata[i]->length : 0;
}
const unsigned char *
v5_creds_authdata_contents(krb5_creds *creds, int i)
{
	return creds->authdata ? creds->authdata[i]->contents : NULL;
}
#else
#error "Don't know how to read authdata for your Kerberos implementation!"
#endif

#if defined(HAVE_KRB5_CREDS_IS_SKEY)
krb5_boolean
v5_creds_get_is_skey(krb5_creds *creds)
{
	return creds->is_skey;
}
#else
krb5_boolean
v5_creds_get_is_skey(krb5_creds *creds)
{
	return 0;
}
#endif

#if defined(HAVE_KRB5_CREDS_FLAGS_I)
krb5_flags
v5_creds_get_flags(krb5_creds *creds)
{
	return creds->flags.i;
}
#elif defined(HAVE_KRB5_CREDS_TICKET_FLAGS)
krb5_flags
v5_creds_get_flags(krb5_creds *creds)
{
	return creds->ticket_flags;
}
#else
#error "Don't know how to read ticket flags for your Kerberos implementation!"
#endif

#if defined(HAVE_KRB5_AUTH_CON_SETUSERUSERKEY)
krb5_error_code
v5_auth_con_setuserkey(krb5_context ctx, krb5_auth_context auth_con,
		       krb5_keyblock *key)
{
	return krb5_auth_con_setuseruserkey(ctx, auth_con, key);
}
#elif defined(HAVE_KRB5_AUTH_CON_SETUSERKEY)
krb5_error_code
v5_auth_con_setuserkey(krb5_context ctx, krb5_auth_context auth_con,
		       krb5_keyblock *key)
{
	return krb5_auth_con_setuserkey(ctx, auth_con, key);
}
#else
#error "Don't know how to set user-to-user key for your Kerberos implementation!"
#endif

#if defined(HAVE_KRB5_TICKET_ENC_PART2)
krb5_principal
v5_ticket_get_client(krb5_ticket *ticket)
{
	return ticket->enc_part2->client;
}
#elif defined(HAVE_KRB5_TICKET_CLIENT)
krb5_principal
v5_ticket_get_client(krb5_ticket *ticket)
{
	return ticket->client;
}
#else
#error "Don't know how to read ticket client for your Kerberos implementation!"
#endif

#ifdef HAVE_KRB5_CONST_REALM
void
v5_appdefault_string(krb5_context ctx,
		     const char *realm, const char *option,
		     const char *default_value, char **ret_value)
{
	char *tmp;

	*ret_value = tmp = xstrdup(default_value);
	krb5_appdefault_string(ctx, PAM_KRB5_APPNAME, realm, option,
			       default_value, ret_value);
	if (*ret_value != tmp) {
		xstrfree(tmp);
	}
}
void
v5_appdefault_boolean(krb5_context ctx,
		      const char *realm, const char *option,
		      krb5_boolean default_value, krb5_boolean *ret_value)
{
	*ret_value = default_value;
	krb5_appdefault_boolean(ctx, PAM_KRB5_APPNAME, realm, option,
				default_value, ret_value);
}
#else
static krb5_data *
data_from_string(const char *s)
{
	krb5_data *ret;
	ret = malloc(sizeof(krb5_data));
	if (ret == NULL) {
		return ret;
	}
	memset(ret, 0, sizeof(krb5_data));
	ret->length = xstrlen(s);
	ret->data = xstrdup(s);
	return ret;
}
static void
data_free(krb5_data *data)
{
	memset(data->data, 0, data->length);
	free(data->data);
	free(data);
}
void
v5_appdefault_string(krb5_context ctx,
		     const char *realm, const char *option,
		     const char *default_value, char **ret_value)
{
	krb5_data *realm_data;
	char *tmp;

	realm_data = data_from_string(realm);
	*ret_value = tmp = xstrdup(default_value);
	if (realm_data != NULL) {
		krb5_appdefault_string(ctx, PAM_KRB5_APPNAME, realm_data,
				       option, default_value, ret_value);
		data_free(realm_data);
	} else {
		*ret_value = xstrdup(default_value);
	}
	if (*ret_value != tmp) {
		xstrfree(tmp);
	}
}
void
v5_appdefault_boolean(krb5_context ctx,
		      const char *realm, const char *option,
		      krb5_boolean default_value, krb5_boolean *ret_value)
{
	krb5_data *realm_data;
	int tmp;

	*ret_value = default_value;

	realm_data = data_from_string(realm);
	if (realm_data != NULL) {
		krb5_appdefault_boolean(ctx, PAM_KRB5_APPNAME, realm_data,
					option, default_value, &tmp);
		*ret_value = tmp;
		data_free(realm_data);
	}
}
#endif

static int
v5_validate_using_ccache(krb5_context ctx, krb5_creds *creds,
			 struct _pam_krb5_user_info *userinfo,
			 const struct _pam_krb5_options *options)
{
	krb5_ccache ccache;
	krb5_ticket *ticket;
	krb5_creds mcreds, *ocreds, *ucreds;
	krb5_auth_context auth_con;
	krb5_data req;
	krb5_flags flags;
	krb5_error_code ret;
	char ccname[PATH_MAX];
	static int counter = 0;

	if (options->debug) {
		debug("attempting to verify credentials using user-to-user "
		      "auth to ccache '%s'", krb5_cc_default_name(ctx));
	}

	/* Open the default ccache and see if it has creds that look like the
	 * ones we're checking, but which use a different key (i.e., don't
	 * bother if the creds are the ones we have already). */
	ccache = NULL;
	ret = krb5_cc_default(ctx, &ccache);
	if (ret != 0) {
		warn("error opening default ccache: %s", v5_error_message(ret));
		return PAM_SERVICE_ERR;
	}

	memset(&mcreds, 0, sizeof(mcreds));
	mcreds.client = creds->client;
	mcreds.server = creds->server;
	ocreds = NULL;
	ret = krb5_get_credentials(ctx, KRB5_GC_CACHED, ccache,
				   &mcreds, &ocreds);
	if (ret != 0) {
		warn("error getting cached creds for the same client/server "
		     "pair: %s", v5_error_message(ret));
		krb5_cc_close(ctx, ccache);
		return PAM_SERVICE_ERR;
	}
	if (options->debug) {
		debug("found previously-obtained credentials in ccache");
	}
	if ((v5_creds_get_etype(creds) == v5_creds_get_etype(ocreds)) &&
	    (v5_creds_key_length(creds) == v5_creds_key_length(ocreds)) &&
	    (memcmp(v5_creds_key_contents(creds),
		    v5_creds_key_contents(ocreds),
		    v5_creds_key_length(creds)) == 0)) {
		warn("internal error - previously-obtained credentials have "
		     "the same key as the ones we're attempting to verify");
		krb5_free_creds(ctx, ocreds);
		krb5_cc_close(ctx, ccache);
		return PAM_SERVICE_ERR;
	}
	krb5_cc_close(ctx, ccache);

	/* Create a temporary ccache to hold the creds we're validating and the
	 * user-to-user creds we'll be obtaining to validate them. */
	snprintf(ccname, sizeof(ccname), "MEMORY:_pam_krb5_val_s_%s-%d",
		 userinfo->unparsed_name, counter++);
	ccache = NULL;
	ret = krb5_cc_resolve(ctx, ccname, &ccache);
	if (ret != 0) {
		warn("internal error creating in-memory ccache: %s",
		     v5_error_message(ret));
		krb5_free_creds(ctx, ocreds);
		return PAM_SERVICE_ERR;
	}
	ret = krb5_cc_initialize(ctx, ccache, creds->client);
	if (ret != 0) {
		warn("internal error initializing in-memory ccache: %s",
		     v5_error_message(ret));
		krb5_cc_destroy(ctx, ccache);
		krb5_free_creds(ctx, ocreds);
		return PAM_SERVICE_ERR;
	}
	ret = krb5_cc_store_cred(ctx, ccache, creds);
	if (ret != 0) {
		warn("internal error storing creds to in-memory ccache: %s",
		     v5_error_message(ret));
		krb5_cc_destroy(ctx, ccache);
		krb5_free_creds(ctx, ocreds);
		return PAM_SERVICE_ERR;
	}

	/* Go get the user-to-user creds for use in authenticating to the
	 * holder of the previously-obtained TGT. */
	memset(&mcreds, 0, sizeof(mcreds));
	mcreds.client = creds->client;
	mcreds.server = creds->client;
	mcreds.second_ticket = ocreds->ticket;
	ucreds = NULL;
	ret = krb5_get_credentials(ctx, KRB5_GC_USER_USER, ccache,
				   &mcreds, &ucreds);
	if (ret != 0) {
		warn("error obtaining user-to-user creds to '%s': %s",
		     userinfo->unparsed_name, v5_error_message(ret));
		notice("TGT failed verification using previously-obtained "
		       "credentials in '%s': %s", krb5_cc_default_name(ctx),
		       v5_error_message(ret));
		krb5_cc_destroy(ctx, ccache);
		krb5_free_creds(ctx, ocreds);
		return PAM_AUTH_ERR;
	}
	krb5_cc_destroy(ctx, ccache);

	/* Create an auth context and use it to generate a user-to-user auth
	 * request to the old TGT. */
	memset(&auth_con, 0, sizeof(auth_con));
	ret = krb5_auth_con_init(ctx, &auth_con);
	if (ret != 0) {
		warn("error initializing auth context: %s",
		     v5_error_message(ret));
		krb5_free_creds(ctx, ucreds);
		krb5_free_creds(ctx, ocreds);
		return PAM_SERVICE_ERR;
	}
	if (options->debug) {
		debug("creating user-to-user authentication request to '%s'",
		      userinfo->unparsed_name);
	}
	memset(&req, 0, sizeof(req));
	ret = krb5_mk_req_extended(ctx, &auth_con, AP_OPTS_USE_SESSION_KEY,
				   NULL, ucreds, &req);
	if (ret != 0) {
		warn("error generating user-to-user AP request to '%s': %s",
		     userinfo->unparsed_name, v5_error_message(ret));
		notice("TGT failed verification using previously-obtained "
		       "credentials in '%s': %s", krb5_cc_default_name(ctx),
		       v5_error_message(ret));
		krb5_auth_con_free(ctx, auth_con);
		krb5_free_creds(ctx, ucreds);
		krb5_free_creds(ctx, ocreds);
		return PAM_AUTH_ERR;
	}
	krb5_free_creds(ctx, ucreds);
	krb5_auth_con_free(ctx, auth_con);

	/* Create an auth context and use it to "receive" the user-to-user
	 * auth request using the session key from the previously-obtained
	 * credentials. */
	ret = krb5_auth_con_init(ctx, &auth_con);
	if (ret != 0) {
		warn("error initializing auth context: %s",
		     v5_error_message(ret));
		krb5_free_data_contents(ctx, &req);
		krb5_free_creds(ctx, ocreds);
		return PAM_SERVICE_ERR;
	}
	ret = v5_auth_con_setuserkey(ctx, auth_con,
				     v5_creds_get_key(ocreds));
	krb5_free_creds(ctx, ocreds);
	if (ret != 0) {
		warn("error setting up to receive user-to-user AP request: %s",
		     v5_error_message(ret));
		krb5_free_data_contents(ctx, &req);
		krb5_auth_con_free(ctx, auth_con);
		return PAM_SERVICE_ERR;
	}
	if (options->debug) {
		debug("receiving user-to-user authentication request");
	}
	ticket = NULL;
	ret = krb5_rd_req(ctx, &auth_con, &req, NULL, NULL, &flags, &ticket);
	krb5_free_data_contents(ctx, &req);
	if (ret != 0) {
		warn("error receiving user-to-user AP request: %s",
		     v5_error_message(ret));
		notice("TGT failed verification using previously-obtained "
		       "credentials in '%s': %s", krb5_cc_default_name(ctx),
		       v5_error_message(ret));
		krb5_auth_con_free(ctx, auth_con);
		return PAM_AUTH_ERR;
	}
	if (options->debug) {
		debug("checking that the client and server names still match");
	}
	if (krb5_principal_compare(ctx, v5_ticket_get_client(ticket),
				   creds->client) == 0) {
		warn("client in user-to-user request was changed");
		notice("TGT failed verification using previously-obtained "
		       "credentials in '%s': client name mismatch",
		       krb5_cc_default_name(ctx));
		krb5_free_ticket(ctx, ticket);
		krb5_auth_con_free(ctx, auth_con);
		return PAM_AUTH_ERR;
	}
	if (krb5_principal_compare(ctx, ticket->server, creds->client) == 0) {
		warn("server in user-to-user request was changed");
		notice("TGT failed verification using previously-obtained "
		       "credentials in '%s': server name mismatch",
		       krb5_cc_default_name(ctx));
		krb5_free_ticket(ctx, ticket);
		krb5_auth_con_free(ctx, auth_con);
		return PAM_AUTH_ERR;
	}

	krb5_free_ticket(ctx, ticket);
	krb5_auth_con_free(ctx, auth_con);
	notice("TGT verified using previously-obtained credentials in '%s'",
	       krb5_cc_default_name(ctx));
	return PAM_SUCCESS;
}

/* Try to free the entry's contents, using krb5_free_keytab_entry_contents(),
 * if it's available, or krb5_kt_free_entry(), which despite the name, doesn't
 * tend to try to free the entry. */
static void
v5_free_keytab_entry_contents(krb5_context ctx, krb5_keytab_entry *entry)
{
#ifdef HAVE_KRB5_FREE_KEYTAB_ENTRY_CONTENTS
	krb5_free_keytab_entry_contents(ctx, entry);
#else
	krb5_kt_free_entry(ctx, entry);
#endif
}

/* Select the principal name of the service to use when validating the creds in
 * question. */
static int
v5_select_keytab_service(krb5_context ctx, krb5_principal client,
			 const char *ktname,
			 krb5_principal *service)
{
	krb5_principal host, princ;
	krb5_keytab keytab;
	krb5_kt_cursor cursor;
	krb5_keytab_entry entry;
	int i, score;

	*service = NULL;

	/* Figure out what the local host service is named -- we're mainly
	 * interested in the second component, which is the local hostname. */
	host = NULL;
	i = krb5_sname_to_principal(ctx, NULL, "host", KRB5_NT_SRV_HST, &host);
	if (i != 0) {
		crit("error guessing name of local host principal");
		return PAM_SERVICE_ERR;
	}

	/* Open the keytab. */
	memset(&keytab, 0, sizeof(keytab));
	if (ktname != NULL) {
		i = krb5_kt_resolve(ctx, ktname, &keytab);
	} else {
		i = krb5_kt_default(ctx, &keytab);
	}
	if (i != 0) {
		if (ktname != NULL) {
			warn("error resolving keytab '%s'", ktname);
		} else {
			warn("error resolving default keytab");
		}
		krb5_free_principal(ctx, host);
		return PAM_SERVICE_ERR;
	}

	/* Set up to walk the keytab. */
	memset(&cursor, 0, sizeof(cursor));
	i = krb5_kt_start_seq_get(ctx, keytab, &cursor);
	if (i != 0) {
		if (ktname != NULL) {
			warn("error reading keytab '%s'", ktname);
		} else {
			warn("error reading default keytab");
		}
		krb5_kt_close(ctx, keytab);
		krb5_free_principal(ctx, host);
		return PAM_SERVICE_ERR;
	}

	/* Walk the keytab, looking for a good service key.  Prefer a "host" in
	 * the client's realm, or a (hopefully) host-based service in the
	 * client's realm (even better, if the instance matches the local
	 * host's name), or anything from the client's realm, but try the first
	 * one if we don't find a suitable host key.  If we're being called
	 * from a non-"host" service, hopefully this will let us try to do
	 * validation using that service's keytab.  */
	princ = NULL;
	score = 0;
	while ((i = krb5_kt_next_entry(ctx, keytab, &entry, &cursor)) == 0) {
		/* First entry? */
		if (princ == NULL) {
			i = krb5_copy_principal(ctx, entry.principal, &princ);
			if (i != 0) {
				warn("internal error copying principal name");
				v5_free_keytab_entry_contents(ctx, &entry);
				krb5_kt_end_seq_get(ctx, keytab, &cursor);
				krb5_kt_close(ctx, keytab);
				krb5_free_principal(ctx, host);
				return PAM_SERVICE_ERR;
			}
		}
		/* Better entry (anything in the client's realm)? */
		if ((score < 1) &&
		    krb5_realm_compare(ctx, entry.principal, client)) {
			if (princ != NULL) {
				krb5_free_principal(ctx, princ);
			}
			i = krb5_copy_principal(ctx, entry.principal, &princ);
			if (i != 0) {
				warn("internal error copying principal name");
				v5_free_keytab_entry_contents(ctx, &entry);
				krb5_kt_end_seq_get(ctx, keytab, &cursor);
				krb5_kt_close(ctx, keytab);
				krb5_free_principal(ctx, host);
				return PAM_SERVICE_ERR;
			}
			score = 1;
		}
		/* Even better entry (hopefully a host-based service in the
		 * client's realm)? */
		if ((score < 2) &&
		    (v5_princ_component_count(entry.principal) == 2) &&
		    krb5_realm_compare(ctx, entry.principal, client)) {
			if (princ != NULL) {
				krb5_free_principal(ctx, princ);
			}
			i = krb5_copy_principal(ctx, entry.principal, &princ);
			if (i != 0) {
				warn("internal error copying principal name");
				v5_free_keytab_entry_contents(ctx, &entry);
				krb5_kt_end_seq_get(ctx, keytab, &cursor);
				krb5_kt_close(ctx, keytab);
				krb5_free_principal(ctx, host);
				return PAM_SERVICE_ERR;
			}
			score = 2;
		}
		/* Better entry ("host" with what should be a hostname as the
		 * instance, in the client's realm)? */
		if ((score < 3) &&
		    (v5_princ_component_count(entry.principal) == 2) &&
		    krb5_realm_compare(ctx, entry.principal, client) &&
		    (v5_princ_component_length(entry.principal, 0) == 4) &&
		    (memcmp(v5_princ_component_contents(entry.principal, 0),
			    "host", 4) == 0)) {
			if (princ != NULL) {
				krb5_free_principal(ctx, princ);
			}
			i = krb5_copy_principal(ctx, entry.principal, &princ);
			if (i != 0) {
				warn("internal error copying principal name");
				v5_free_keytab_entry_contents(ctx, &entry);
				krb5_kt_end_seq_get(ctx, keytab, &cursor);
				krb5_kt_close(ctx, keytab);
				krb5_free_principal(ctx, host);
				return PAM_SERVICE_ERR;
			}
			score = 3;
		}
		/* Better entry (a service with the local hostname as the
		 * instance, in the client's realm)? */
		if ((score < 4) &&
		    (host != NULL) &&
		    (v5_princ_component_count(entry.principal) == 2) &&
		    krb5_realm_compare(ctx, entry.principal, client) &&
		    (v5_princ_component_length(entry.principal, 1) ==
		     v5_princ_component_length(host, 1)) &&
		    (memcmp(v5_princ_component_contents(entry.principal, 1),
			    v5_princ_component_contents(host, 1),
			    v5_princ_component_length(host, 1)) == 0)) {
			if (princ != NULL) {
				krb5_free_principal(ctx, princ);
			}
			i = krb5_copy_principal(ctx, entry.principal, &princ);
			if (i != 0) {
				warn("internal error copying principal name");
				v5_free_keytab_entry_contents(ctx, &entry);
				krb5_kt_end_seq_get(ctx, keytab, &cursor);
				krb5_kt_close(ctx, keytab);
				krb5_free_principal(ctx, host);
				return PAM_SERVICE_ERR;
			}
			score = 4;
		}
		/* Favorite entry ("host" with the local hostname as the
		 * instance, in the client's realm)? */
		if ((score < 5) &&
		    (host != NULL) &&
		    (v5_princ_component_count(entry.principal) == 2) &&
		    krb5_realm_compare(ctx, entry.principal, client) &&
		    (v5_princ_component_length(entry.principal, 1) ==
		     v5_princ_component_length(host, 1)) &&
		    (memcmp(v5_princ_component_contents(entry.principal, 1),
			    v5_princ_component_contents(host, 1),
			    v5_princ_component_length(host, 1)) == 0) &&
		    (v5_princ_component_length(entry.principal, 0) == 4) &&
		    (memcmp(v5_princ_component_contents(entry.principal, 0),
			    "host", 4) == 0)) {
			if (princ != NULL) {
				krb5_free_principal(ctx, princ);
			}
			i = krb5_copy_principal(ctx, entry.principal, &princ);
			if (i != 0) {
				warn("internal error copying principal name");
				v5_free_keytab_entry_contents(ctx, &entry);
				krb5_kt_end_seq_get(ctx, keytab, &cursor);
				krb5_kt_close(ctx, keytab);
				krb5_free_principal(ctx, host);
				return PAM_SERVICE_ERR;
			}
			score = 5;
		}
		v5_free_keytab_entry_contents(ctx, &entry);
	}

	krb5_kt_end_seq_get(ctx, keytab, &cursor);
	krb5_kt_close(ctx, keytab);
	krb5_free_principal(ctx, host);

	*service = princ;

	return PAM_SUCCESS;
}

static int
v5_validate_using_keytab(krb5_context ctx,
			 krb5_creds *creds, krb5_ccache ccache,
			 const struct _pam_krb5_options *options, int *krberr)
{
	int i;
	char *principal;
	krb5_principal princ;
	krb5_keytab keytab;
	krb5_verify_init_creds_opt opt;

	/* Try to figure out the name of a suitable service. */
	princ = NULL;
	v5_select_keytab_service(ctx, creds->client, options->keytab, &princ);

	/* Try to get a text representation of the principal to which the key
	 * belongs, for logging purposes. */
	principal = NULL;
	if (princ != NULL) {
		i = krb5_unparse_name(ctx, princ, &principal);
	}

	/* Try to open the keytab. */
	keytab = NULL;
	if (options->keytab != NULL) {
		i = krb5_kt_resolve(ctx, options->keytab, &keytab);
		if (i != 0) {
			warn("error resolving keytab '%s'", options->keytab);
		}
	} else {
		i = krb5_kt_default(ctx, &keytab);
		if (i != 0) {
			warn("error resolving default keytab");
		}
	}

	/* Perform the verification checks using the service's key, assuming we
	 * have some idea of what the service's name is, and that we can read
	 * the key. */
	krb5_verify_init_creds_opt_init(&opt);
	i = krb5_verify_init_creds(ctx, creds, princ, keytab, &ccache, &opt);
	*krberr = i;
	if (keytab != NULL) {
		krb5_kt_close(ctx, keytab);
	}
	if (princ != NULL) {
		krb5_free_principal(ctx, princ);
	}

	/* Log success or failure. */
	if (i == 0) {
		if (principal != NULL) {
			notice("TGT verified using key for '%s'", principal);
			v5_free_unparsed_name(ctx, principal);
		} else {
			notice("TGT verified");
		}
		return PAM_SUCCESS;
	} else {
		if (principal != NULL) {
			crit("TGT failed verification using keytab and "
			     "key for '%s': %s",
			     principal, v5_error_message(i));
			v5_free_unparsed_name(ctx, principal);
		} else {
			crit("TGT failed verification using keytab: %s",
			     v5_error_message(i));
		}
		return PAM_AUTH_ERR;
	}
}

static int
v5_validate(krb5_context ctx, krb5_creds *creds, krb5_ccache ccache,
	    struct _pam_krb5_user_info *userinfo,
	    const struct _pam_krb5_options *options)
{
	int ret, krberr;
	/* Obtain creds for a service for which we have keys in the keytab and
	 * then just authenticate to it. */
	krberr = 0;
	ret = v5_validate_using_keytab(ctx, creds, ccache, options, &krberr);
	switch (ret) {
	case PAM_AUTH_ERR:
		switch (krberr) {
		case EACCES:
		case ENOENT:
		case KRB5_KT_NOTFOUND:
			/* We weren't able to read the keytab. */
			if (options->validate_user_user &&
			    (_pam_krb5_sly_looks_unsafe() == 0)) {
				/* If it looks safe, see if we have an
				 * already-issued TGT that we can use to
				 * perform user-to-user authentication. It's
				 * not ideal, but it tells us that the KDC that
				 * issued this set of creds was the one that
				 * issued the older set, and validating those
				 * was some other process's problem. */
				switch (v5_validate_using_ccache(ctx, creds,
								 userinfo,
								 options)) {
				case PAM_SUCCESS:
					ret = PAM_SUCCESS;
					break;
				default:
					break;
				}
			}
			break;
		default:
			break;
		}
		break;
	default:
		break;
	}
	return ret;
}

#if defined(HAVE_KRB5_GET_INIT_CREDS_OPT_SET_FAST_CCACHE) && \
    defined(HAVE_KRB5_GET_INIT_CREDS_OPT_SET_FAST_FLAGS)
static void
v5_setup_armor_ccache_keytab(krb5_context ctx,
			     struct _pam_krb5_options *options,
			     const char *realm,
			     krb5_creds *creds,
			     krb5_ccache *armor_ccache)
{
	krb5_get_init_creds_opt *gicopts;
	krb5_keytab keytab;
	krb5_principal guess_client;
	char *unparsed;
	int i;

	/* See if we can use the keytab first. */
	keytab = NULL;
	if (options->keytab != NULL) {
		i = krb5_kt_resolve(ctx, options->keytab, &keytab);
		if (i != 0) {
			warn("unable to resolve keytab \"%s\" for armor",
			     options->keytab);
			return;
		}
	} else {
		i = krb5_kt_default(ctx, &keytab);
		if (i != 0) {
			warn("unable to resolve default keytab for armor");
			return;
		}
	}
	/* Make sure we can set options. */
	gicopts = NULL;
	i = v5_alloc_get_init_creds_opt(ctx, &gicopts);
	if (i != 0) {
		/* Take our chances. */
		gicopts = NULL;
	} else {
		/* Set hard-coded defaults for armor tickets which might not
		 * match generally-used options. */
		_pam_krb5_set_init_opts_for_armor(ctx,
						  gicopts,
						  options);
	}
	/* Make an initial client name guess. */
	i = krb5_sname_to_principal(ctx, NULL, "host", KRB5_NT_SRV_HST,
				    &guess_client);
	if (i != 0) {
		crit("error guessing name of a principal in keytab for armor");
		if (gicopts != NULL) {
			v5_free_get_init_creds_opt(ctx, gicopts);
		}
		krb5_kt_close(ctx, keytab);
		return;
	}
	v5_set_principal_realm(ctx, &guess_client, realm);
	/* Try to select a more suitable client name. */
	if (creds->client != NULL) {
		krb5_free_principal(ctx, creds->client);
		creds->client = NULL;
	}
	i = v5_select_keytab_service(ctx, guess_client, options->keytab,
				     &creds->client);
	krb5_free_principal(ctx, guess_client);
	if (creds->client == NULL) {
		warn("unable to select an armor service from keytab: %d (%s)",
		     i, v5_error_message(i));
	} else {
#ifdef HAVE_KRB5_GET_INIT_CREDS_OPT_SET_OUT_CCACHE
		if (armor_ccache != NULL) {
			krb5_get_init_creds_opt_set_out_ccache(ctx, gicopts,
							       *armor_ccache);
		}
#endif
		/* Try to use the keytab to get a TGT. */
		i = krb5_get_init_creds_keytab(ctx,
					       creds,
					       creds->client,
					       keytab,
					       0,
					       NULL,
					       gicopts);
		if (options->debug) {
			unparsed = NULL;
			krb5_unparse_name(ctx, creds->client, &unparsed);
			if (unparsed != NULL) {
				debug("krb5_get_init_creds_keytab(%s) "
				      "for armor returned %d (%s)",
				      unparsed,
				      i, v5_error_message(i));
				v5_free_unparsed_name(ctx, unparsed);
			} else {
				debug("krb5_get_init_creds_keytab() "
				      "for armor returned %d (%s)",
				      i, v5_error_message(i));
			}
		}
		if (i != 0) {
			warn("error getting armor ticket via keytab: %d (%s)",
			     i, v5_error_message(i));
		}
	}
	if (gicopts != NULL) {
		v5_free_get_init_creds_opt(ctx, gicopts);
	}
	krb5_kt_close(ctx, keytab);
}

static void
v5_setup_armor_ccache_pkinit(krb5_context ctx,
			     struct _pam_krb5_options *options,
			     const char *realm,
			     krb5_creds *creds,
			     krb5_ccache *armor_ccache)
{
	krb5_get_init_creds_opt *gicopts;
	char *unparsed;
	int i;
#ifdef KRB5_WELLKNOWN_NAMESTR
	const char *wellknown = KRB5_WELLKNOWN_NAMESTR;
#else
	const char *wellknown = "WELLKNOWN";
#endif
#ifdef KRB5_ANONYMOUS_PRINCSTR
	const char *anonymous = KRB5_ANONYMOUS_PRINCSTR;
#else
	const char *anonymous = "ANONYMOUS";
#endif

	/* Make sure we can set options. */
	gicopts = NULL;
	i = v5_alloc_get_init_creds_opt(ctx, &gicopts);
	if (i != 0) {
		/* Need to be able to force PKINIT only. */
		return;
	}
	/* Set hard-coded defaults for armor tickets which might not
	 * match generally-used options. */
	_pam_krb5_set_init_opts_for_armor(ctx,
					  gicopts,
					  options);
	/* Force the client name. */
	if (creds->client != NULL) {
		krb5_free_principal(ctx, creds->client);
		creds->client = NULL;
	}
	if (krb5_build_principal(ctx, &creds->client,
				 strlen(realm),
				 realm,
				 wellknown,
				 anonymous,
				 NULL) == 0) {
		/* Force PKINIT. */
#ifdef HAVE_KRB5_GET_INIT_CREDS_OPT_SET_PREAUTH_LIST
		krb5_preauthtype pkinit;
		pkinit = KRB5_PADATA_PK_AS_REQ;
		krb5_get_init_creds_opt_set_preauth_list(gicopts, &pkinit, 1);
#endif
#ifdef HAVE_KRB5_GET_INIT_CREDS_OPT_SET_PKINIT
		krb5_get_init_creds_opt_set_pkinit(ctx,
						   gicopts,
						   creds->client,
						   NULL,
						   NULL,
#ifdef KRB5_GET_INIT_CREDS_OPT_SET_PKINIT_TAKES_11_ARGS
						   NULL,
						   NULL,
#endif
						   options->pkinit_flags,
						   _pam_krb5_always_fail_prompter,
						   NULL,
						   NULL);
#endif
#ifdef HAVE_KRB5_GET_INIT_CREDS_OPT_SET_OUT_CCACHE
		if (armor_ccache != NULL) {
			krb5_get_init_creds_opt_set_out_ccache(ctx, gicopts,
							       *armor_ccache);
		}
#endif
		/* Hopefully we're only going to contact the KDC if things are
		 * set up on our end. */
		i = krb5_get_init_creds_password(ctx,
						 creds,
						 creds->client,
						 NULL,
						 _pam_krb5_always_fail_prompter,
						 NULL,
						 0,
						 NULL,
						 gicopts);
		if (options->debug) {
			unparsed = NULL;
			krb5_unparse_name(ctx, creds->client, &unparsed);
			if (unparsed != NULL) {
				debug("krb5_get_init_creds_password(%s) "
				      "for armor returned %d (%s)",
				      unparsed,
				      i, v5_error_message(i));
				v5_free_unparsed_name(ctx, unparsed);
			} else {
				debug("krb5_get_init_creds_password() "
				      "for armor returned %d (%s)",
				      i, v5_error_message(i));
			}
		}
		if (i != 0) {
			warn("error getting armor ticket via "
			     "anonymous pkinit: %d (%s)",
			     i, v5_error_message(i));
		}
	}
	v5_free_get_init_creds_opt(ctx, gicopts);
}

static void
v5_setup_armor_ccache(krb5_context ctx,
		      struct _pam_krb5_options *options,
		      const char *realm,
		      krb5_ccache *armor_ccache)
{
	krb5_creds creds;
	char ccname[LINE_MAX];
	const char *p;
	int i;
	unsigned int u, len;
	struct {
		const char *name;
		void (*fn)(krb5_context,
			   struct _pam_krb5_options *,
			   const char *,
			   krb5_creds *,
			   krb5_ccache *);
	} methods[] = {
		{"keytab", v5_setup_armor_ccache_keytab},
		{"pkinit", v5_setup_armor_ccache_pkinit},
	};

	if (armor_ccache == NULL) {
		return;
	}
	memset(&creds, 0, sizeof(creds));
	i = krb5_build_principal(ctx, &creds.server,
				 strlen(realm),
				 realm,
				 KRB5_TGS_NAME,
				 realm,
				 NULL);
	if (i != 0) {
		return;
	}
	/* Build a minimal ccache. */
	snprintf(ccname, sizeof(ccname), "MEMORY:%p", armor_ccache);
	if (krb5_cc_resolve(ctx, ccname, armor_ccache) != 0) {
		krb5_free_principal(ctx, creds.server);
		return;
	}
	/* Use the methods in the configured order. */
	p = options->armor_strategy;
	while (*p != '\0') {
		len = strcspn(p, ",");
		for (u = 0; u < sizeof(methods) / sizeof(methods[0]); u++) {
			if (v5_creds_check_initialized(ctx, &creds) == 0) {
				break;
			}
			if (strlen(methods[u].name) != len) {
				continue;
			}
			if (memcmp(p, methods[u].name, len) == 0) {
				(*(methods[u].fn))(ctx, options, realm, &creds,
						   armor_ccache);
			}
		}
		p += len;
		p += strspn(p, ",");
	}
	/* If we got creds, and they weren't stored in the ccache for us, set
	 * up the armor ccache directly. */
	if (v5_creds_check_initialized(ctx, &creds) == 0) {
		if (v5_ccache_has_tgt(ctx, *armor_ccache,
				      realm, NULL) != 0) {
			if (krb5_cc_initialize(ctx, *armor_ccache,
					       creds.client) != 0) {
				krb5_free_cred_contents(ctx, &creds);
				krb5_cc_destroy(ctx, *armor_ccache);
				*armor_ccache = NULL;
				return;
			}
			if (krb5_cc_store_cred(ctx, *armor_ccache, &creds) != 0) {
				krb5_free_cred_contents(ctx, &creds);
				krb5_cc_destroy(ctx, *armor_ccache);
				*armor_ccache = NULL;
				return;
			}
		}
		krb5_free_cred_contents(ctx, &creds);
	}
	/* Now if we still haven't got suitable creds, abandon this. */
	if ((*armor_ccache != NULL) &&
	    (v5_ccache_has_tgt(ctx, *armor_ccache,
			       realm, NULL) != 0)) {
		krb5_cc_destroy(ctx, *armor_ccache);
		*armor_ccache = NULL;
	}
}
#endif

int
v5_get_creds(krb5_context ctx,
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
	     int *result)
{
	int i;
	char realm_service[LINE_MAX];
	char *opt;
	struct pam_message message;
	struct _pam_krb5_prompter_data prompter_data;
	krb5_creds creds;
	krb5_get_init_creds_opt *tmp_gicopts;
	char ccname[LINE_MAX];

	/* In case we already have creds, get rid of them. */
	if (*ccache != NULL) {
		krb5_cc_destroy(ctx, *ccache);
		*ccache = NULL;
	}
	snprintf(ccname, sizeof(ccname), "MEMORY:%p", ccache);
	if (krb5_cc_resolve(ctx, ccname, ccache) != 0) {
		return PAM_SERVICE_ERR;
	}
	memset(&creds, 0, sizeof(creds));

	/* Check some string lengths. */
	if (strlen(service) + 1 +
	    strlen(userinfo->realm) + 1 +
	    strlen(userinfo->realm) + 1 >= sizeof(realm_service)) {
		return PAM_SERVICE_ERR;
	}

	/* Cheap hack.  Appends the realm name to a service to generate a
	 * more full service name. */
	if (strchr(service, '/') != NULL) {
		strcpy(realm_service, service);
	} else {
		strcpy(realm_service, service);
		strcat(realm_service, "/");
		strcat(realm_service, userinfo->realm);
	}
	if (strchr(realm_service, '@') != NULL) {
		strcpy(strchr(realm_service, '@') + 1, userinfo->realm);
	} else {
		strcat(realm_service, "@");
		strcat(realm_service, userinfo->realm);
	}
	if (options->debug) {
		debug("authenticating '%s' to '%s'",
		      userinfo->unparsed_name, realm_service);
	}
	/* Get creds. */
	prompter_data.ctx = ctx;
	prompter_data.pamh = pamh;
	prompter_data.previous_password = password;
	prompter_data.options = options;
	prompter_data.userinfo = userinfo;
	if (options->debug && options->debug_sensitive) {
		debug("attempting with password=%s%s%s",
		      password ? "\"" : "",
		      password ? password : "(null)",
		      password ? "\"" : "");
	}
#ifdef HAVE_KRB5_GET_INIT_CREDS_OPT_SET_PKINIT
	opt = v5_user_info_subst(ctx, user, userinfo, options,
				 options->pkinit_identity);
	if (opt != NULL) {
		if (strlen(opt) > 0) {
			if (options->debug) {
				debug("resolved pkinit identity to "
				      "\"%s\"", opt);
			}
			krb5_get_init_creds_opt_set_pkinit(ctx,
							   gic_options,
							   userinfo->principal_name,
							   opt,
							   NULL,
#ifdef KRB5_GET_INIT_CREDS_OPT_SET_PKINIT_TAKES_11_ARGS
							   NULL,
							   NULL,
#endif
							   options->pkinit_flags,
							   prompter,
							   &prompter_data,
							   password);
		} else {
			if (options->debug) {
				debug("pkinit identity has no "
				      "contents, ignoring");
			}
		}
		free(opt);
	} else {
		warn("error resolving pkinit identity template \"%s\" "
		     "to a useful value", options->pkinit_identity);
	}
#endif
#ifdef HAVE_KRB5_GET_INIT_CREDS_OPT_SET_PA
	for (i = 0;
	     (options->preauth_options != NULL) &&
	     (options->preauth_options[i] != NULL);
	     i++) {
		opt = v5_user_info_subst(ctx, user, userinfo, options,
					 options->preauth_options[i]);
		if (opt != NULL) {
			char *val;
			val = strchr(opt, '=');
			if (val != NULL) {
				*val++ = '\0';
				if (options->debug) {
					debug("setting preauth option "
					      "\"%s\" = \"%s\"",
					      opt, val);
				}
				if (krb5_get_init_creds_opt_set_pa(ctx,
								   gic_options,
								   opt,
								   val) != 0) {
					warn("error setting preauth "
					     "option \"%s\"", opt);
				}
			}
			free(opt);
		} else {
			warn("error resolving preauth option \"%s\" "
			     "to a useful value",
			     options->preauth_options[i]);
		}
	}
#endif
#if defined(HAVE_KRB5_GET_INIT_CREDS_OPT_SET_FAST_CCACHE) && \
    defined(HAVE_KRB5_GET_INIT_CREDS_OPT_SET_FAST_FLAGS)
	if ((options->armor) && (armor_ccache != NULL)) {
		if (*armor_ccache == NULL) {
			v5_setup_armor_ccache(ctx, options, userinfo->realm,
					      armor_ccache);
		}
		if (*armor_ccache != NULL) {
			opt = NULL;
			krb5_get_init_creds_opt_set_fast_ccache(ctx,
								gic_options,
								*armor_ccache);
			if (v5_cc_get_full_name(ctx, *armor_ccache,
						&opt) == 0) {
				char envstr[LINE_MAX];
				if (options->test_environment) {
					snprintf(envstr, sizeof(envstr),
						 "%s=%s",
						 PACKAGE "_armor_ccache",
						 opt);
					pam_putenv(pamh, envstr);
				}
				v5_free_cc_full_name(ctx, opt);
			}
		}
	}
#endif
#ifdef HAVE_KRB5_GET_INIT_CREDS_OPT_SET_OUT_CCACHE
	krb5_get_init_creds_opt_set_out_ccache(ctx, gic_options, *ccache);
#endif
	i = krb5_get_init_creds_password(ctx,
					 &creds,
					 userinfo->principal_name,
					 password,
					 prompter,
					 &prompter_data,
					 0,
					 realm_service,
					 gic_options);
	/* Let the caller see the krb5 result code. */
	if (options->debug) {
		debug("krb5_get_init_creds_password(%s) returned %d (%s)",
		      realm_service, i, v5_error_message(i));
	}
	if (result != NULL) {
		*result = i;
	}
	/* Interpret the return code. */
	switch (i) {
	case 0:
		/* Flat-out success.  Initialize the ccache, store the creds to
		 * it, and validate the TGT if it's actually a TGT, and if we
		 * have something we can use to do so. */
		if (v5_ccache_has_tgt(ctx, *ccache,
				      userinfo->realm, NULL) != 0) {
			krb5_cc_initialize(ctx, *ccache,
					   userinfo->principal_name);
			krb5_cc_store_cred(ctx, *ccache, &creds);
		}
		if ((options->validate == 1) &&
		    (strcmp(service, KRB5_TGS_NAME) == 0)) {
			if (options->debug) {
				debug("validating credentials");
			}
			switch (v5_validate(ctx, &creds, *ccache,
					    userinfo, options)) {
			case PAM_AUTH_ERR:
				return PAM_AUTH_ERR;
				break;
			default:
				break;
			}
		}
		krb5_free_cred_contents(ctx, &creds);
		return PAM_SUCCESS;
		break;
	case KRB5KDC_ERR_CLIENT_REVOKED:
		/* There's an entry on the KDC, but it's disabled.  We'll try
		 * to treat that as we would a "principal unknown error". */
		if (options->warn) {
			message.msg = "Error: account is locked.";
			message.msg_style = PAM_TEXT_INFO;
			_pam_krb5_conv_call(pamh, &message, 1, NULL);
		}
		/* fall through */
	case KRB5KDC_ERR_C_PRINCIPAL_UNKNOWN:
	case KRB5KDC_ERR_NAME_EXP:
		/* The user is unknown or a principal has expired. */
		if (options->ignore_unknown_principals) {
			return PAM_IGNORE;
		} else {
			return PAM_USER_UNKNOWN;
		}
		break;
	case KRB5KDC_ERR_KEY_EXP:
		/* The user's key (password) is expired.  We get this error
		 * even if the supplied password is incorrect, so we try to
		 * get a password-changing ticket, which we should be able
		 * to get with an expired password. */
		snprintf(realm_service, sizeof(realm_service),
			 PASSWORD_CHANGE_PRINCIPAL "@%s", userinfo->realm);
		if (options->debug) {
			debug("key is expired. attempting to verify password "
			      "by obtaining credentials for %s", realm_service);
		}
		prompter_data.ctx = ctx;
		prompter_data.pamh = pamh;
		prompter_data.previous_password = password;
		prompter_data.options = options;
		prompter_data.userinfo = userinfo;
		memset(&creds, 0, sizeof(creds));
		if (options->debug && options->debug_sensitive) {
			debug("attempting with password=%s%s%s",
			      password ? "\"" : "",
			      password ? password : "(null)",
			      password ? "\"" : "");
		}
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
		i = krb5_get_init_creds_password(ctx,
						 &creds,
						 userinfo->principal_name,
						 password,
						 prompter,
						 &prompter_data,
						 0,
						 realm_service,
						 tmp_gicopts);
		v5_free_get_init_creds_opt(ctx, tmp_gicopts);
		krb5_free_cred_contents(ctx, &creds);
		switch (i) {
		case 0:
			/* Got password-changing creds, so warn about the
			 * expired password and continue. */
			if (expired) {
				*expired = 1;
			}
			if (options->warn == 1) {
				message.msg = "Warning: password has expired.";
				message.msg_style = PAM_TEXT_INFO;
				_pam_krb5_conv_call(pamh, &message, 1, NULL);
			}
			if (options->debug) {
				debug("attempt to obtain credentials for %s "
				      "succeeded", realm_service);
			}
			return PAM_SUCCESS;
			break;
		}
		if (options->debug) {
			debug("attempt to obtain credentials for %s "
			      "failed: %s", realm_service, v5_error_message(i));
		}
		if (result) {
			*result = i;
		}
		return PAM_AUTH_ERR;
		break;
	case EAGAIN:
	case KRB5_REALM_CANT_RESOLVE:
	case KRB5_KDC_UNREACH:
		return PAM_AUTHINFO_UNAVAIL;
	default:
		return PAM_AUTH_ERR;
	}
}

static int
v5_save(krb5_context ctx,
	struct _pam_krb5_stash *stash,
	const char *ccname_template,
	int preserve_existing_ccaches,
	const char *user,
	struct _pam_krb5_user_info *userinfo,
	struct _pam_krb5_options *options,
	const char **ccname)
{
	if (ccname != NULL) {
		*ccname = NULL;
	}

	/* Ensure that we have credentials for saving. */
	if (v5_ccache_has_tgt(ctx, stash->v5ccache,
			      userinfo->realm, NULL) != 0) {
		if (options->debug) {
			debug("credentials not initialized");
		}
		return PAM_IGNORE;
	}

	/* Derive the ccache name from the supplied template and create one. */
	_pam_krb5_stash_push(ctx, stash,
			     options,
			     ccname_template,
			     preserve_existing_ccaches,
			     user, userinfo,
			     options->user_check ? userinfo->uid : getuid(),
			     options->user_check ? userinfo->gid : getgid());
	if ((ccname != NULL) && (stash->v5ccnames != NULL)) {
		*ccname = stash->v5ccnames->name;
		return PAM_SUCCESS;
	} else {
		return PAM_SESSION_ERR;
	}
}

int
v5_save_for_user(krb5_context ctx,
		 struct _pam_krb5_stash *stash,
		 const char *user,
		 struct _pam_krb5_user_info *userinfo,
		 struct _pam_krb5_options *options,
		 const char **ccname)
{
	return v5_save(ctx, stash, options->ccname_template, FALSE,
		       user, userinfo, options, ccname);
}

int
v5_save_for_kuserok(krb5_context ctx,
		    struct _pam_krb5_stash *stash,
		    const char *user,
		    struct _pam_krb5_user_info *userinfo,
		    struct _pam_krb5_options *options,
		    const char **ccname)
{
	return v5_save(ctx, stash, "FILE:%d/krb5cc_%U_XXXXXX", TRUE,
		       user, userinfo, options, ccname);
}

void
v5_destroy(krb5_context ctx, struct _pam_krb5_stash *stash,
	   struct _pam_krb5_options *options)
{
	if (stash->v5ccnames != NULL) {
		if (_pam_krb5_stash_pop(ctx, stash, options) != 0) {
			warn("error destroying ccache '%s'",
			     stash->v5ccnames->name);
		}
	}
}

int
v5_cc_retrieve_match(void)
{
#if defined(KRB5_TC_MATCH_KTYPE)
	return KRB5_TC_MATCH_KTYPE;
#elif defined(KRB5_TC_MATCH_KEYTYPE)
	return KRB5_TC_MATCH_KEYTYPE;
#else
#error "Don't know how to search ccaches!"
#endif
}

#if defined(HAVE_KRB5_CHANGE_PASSWORD)
int
v5_change_password(krb5_context ctx, krb5_creds *creds, char *password,
		   int *result_code,
		   krb5_data *result_code_string,
		   krb5_data *result_string)
{
	return krb5_change_password(ctx, creds, password,
				    result_code,
				    result_code_string, result_string);
}
#elif defined(HAVE_KRB5_SET_PASSWORD)
int
v5_change_password(krb5_context ctx, krb5_creds *creds, char *password,
		   int *result_code,
		   krb5_data *result_code_string,
		   krb5_data *result_string)
{
	return krb5_set_password(ctx, creds, password, creds->client,
				 result_code,
				 result_code_string, result_string);
}
#else
#error "Don't know how to change passwords!"
#endif

int
v5_enctype_to_string(krb5_context ctx, krb5_enctype enctype,
		     char *buf, size_t length)
{
#ifdef KRB5_ENCTYPE_TO_STRING_TAKES_A_SIZE_THIRD
	return krb5_enctype_to_string(enctype, buf, length);
#else
	int i;
	char *tmp;
	tmp = NULL;
	i = krb5_enctype_to_string(ctx, enctype, &tmp);
	if (tmp != NULL) {
		snprintf(buf, length, "%s", tmp);
		free(tmp);
		return i;
	}
	if (i == 0) {
		return -1;
	}
	return i;
#endif
}

static krb5_error_code
v5_ccache_has_cred(krb5_context ctx, krb5_ccache ccache, krb5_creds *creds,
		   const char *first, const char *second)
{
	krb5_creds match, matched;
	krb5_error_code err;
	const char *realm;
	int rlength;

	if (ccache == NULL) {
		return KRB5_FCC_NOFILE;
	}

	memset(&match, 0, sizeof(match));
	memset(&matched, 0, sizeof(matched));
	err = krb5_cc_get_principal(ctx, ccache, &match.client);
	if (err != 0) {
		return err;
	}
	realm = v5_princ_realm_contents(match.client);
	rlength = v5_princ_realm_length(match.client);
	if (second == NULL) {
		err = krb5_build_principal_ext(ctx, &match.server,
					       rlength, realm,
					       strlen(first), first,
					       rlength, realm,
					       0);
	} else {
		err = krb5_build_principal(ctx, &match.server,
					   rlength, realm,
					   first, second, NULL);
	}
	if (creds == NULL) {
		creds = &matched;
	}
	err = krb5_cc_retrieve_cred(ctx, ccache, KRB5_TC_MATCH_SRV_NAMEONLY,
				    &match, creds);
	if (creds == &matched) {
		krb5_free_cred_contents(ctx, creds);
	}
	krb5_free_cred_contents(ctx, &match);
	return err;
}

krb5_error_code
v5_ccache_has_tgt(krb5_context ctx, krb5_ccache ccache,
		  const char *tgs_realm, krb5_creds *creds)
{
	return v5_ccache_has_cred(ctx, ccache, creds, KRB5_TGS_NAME, tgs_realm);
}

krb5_error_code
v5_ccache_has_pwc(krb5_context ctx, krb5_ccache ccache, krb5_creds *creds)
{
	return v5_ccache_has_cred(ctx, ccache, creds, "kadmin", "changepw");
}

krb5_error_code
v5_cc_copy(krb5_context ctx, const char *tgt_realm,
	   krb5_ccache occache, krb5_ccache *nccache)
{
	krb5_creds tgt;
	krb5_error_code err;
	char ccname[LINE_MAX];

	if (nccache == NULL) {
		return -1;
	}

	if (*nccache == NULL) {
		snprintf(ccname, sizeof(ccname), "MEMORY:%p", nccache);
		if ((err = krb5_cc_resolve(ctx, ccname, nccache)) != 0) {
			return err;
		}
	}

	memset(&tgt, 0, sizeof(tgt));
	if (v5_ccache_has_tgt(ctx, occache, tgt_realm, &tgt) != 0) {
		memset(&tgt, 0, sizeof(tgt));
		if (krb5_cc_get_principal(ctx, occache, &tgt.client) != 0) {
			return -1;
		}
	}

#ifdef HAVE_KRB5_CC_COPY_CREDS
	if (krb5_cc_initialize(ctx, *nccache, tgt.client) != 0) {
		krb5_free_cred_contents(ctx, &tgt);
		return -1;
	}
	err = krb5_cc_copy_creds(ctx, occache, *nccache);
	if (err != 0) {
#else
	{
#endif
		krb5_creds creds;
		krb5_cc_cursor cursor;
		if (krb5_cc_initialize(ctx, *nccache, tgt.client) != 0) {
			krb5_free_cred_contents(ctx, &tgt);
			return -1;
		}
		if (krb5_cc_start_seq_get(ctx, occache, &cursor) != 0) {
			krb5_free_cred_contents(ctx, &tgt);
			return -1;
		}
		memset(&creds, 0, sizeof(creds));
		while (krb5_cc_next_cred(ctx, occache, &cursor, &creds) == 0) {
			krb5_cc_store_cred(ctx, *nccache, &creds);
			krb5_free_cred_contents(ctx, &creds);
			memset(&creds, 0, sizeof(creds));
		}
		krb5_cc_end_seq_get(ctx, occache, &cursor);
	}
	krb5_free_cred_contents(ctx, &tgt);
	return 0;
}
