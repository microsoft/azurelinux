/*
 * Copyright 2003,2007,2009,2011,2012 Red Hat, Inc.
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

#ifndef pam_krb5_stash_h
#define pam_krb5_stash_h

#include "userinfo.h"

struct _pam_krb5_ccname_list {
	char *name;
	int session_specific;
	struct _pam_krb5_ccname_list *next;
};

struct _pam_krb5_stash {
	char *key;
	krb5_context v5ctx;
	int v5attempted, v5result, v5expired, v5external;
	struct _pam_krb5_ccname_list *v5ccnames;
	krb5_ccache v5ccache, v5armorccache;
	int v5setenv;
	int v5shm;
	pid_t v5shm_owner;
	int afspag;
};

struct _pam_krb5_stash *_pam_krb5_stash_get(pam_handle_t *pamh,
					    const char *user,
					    struct _pam_krb5_user_info *info,
					    struct _pam_krb5_options *options);
void _pam_krb5_stash_push(krb5_context ctx, struct _pam_krb5_stash *stash,
			  struct _pam_krb5_options *options,
			  const char *ccname_template,
			  int preserve_existing_ccaches,
			  const char *user,
			  struct _pam_krb5_user_info *userinfo,
			  uid_t uid, gid_t gid);
int _pam_krb5_stash_pop(krb5_context ctx, struct _pam_krb5_stash *stash,
			struct _pam_krb5_options *options);
void _pam_krb5_stash_shm_read(pam_handle_t *pamh,
			      const char *partial_key,
			      struct _pam_krb5_stash *stash,
			      struct _pam_krb5_options *options,
			      const char *user,
			      struct _pam_krb5_user_info *userinfo);
void _pam_krb5_stash_shm_write(pam_handle_t *pamh,
			       struct _pam_krb5_stash *stash,
			       struct _pam_krb5_options *options,
			       const char *user,
			       struct _pam_krb5_user_info *userinfo);
void _pam_krb5_stash_name(struct _pam_krb5_options *options,
			  const char *user, char **name);
void _pam_krb5_stash_shm_var_name(struct _pam_krb5_options *options,
				  const char *user, char **name);

#endif
