/*
 * Copyright 2003,2004,2005,2006,2009,2012 Red Hat, Inc.
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
#include "initopts.h"
#include "log.h"
#include "options.h"

void
_pam_krb5_set_init_opts(krb5_context ctx, krb5_get_init_creds_opt *k5_options,
			struct _pam_krb5_options *options)
{
#ifdef HAVE_KRB5_GET_INIT_CREDS_OPT_SET_CHANGE_PASSWORD_PROMPT
	/* We want to handle password expiration ourselves, if we can. */
	krb5_get_init_creds_opt_set_change_password_prompt(k5_options,
							   options->chpw_prompt);
#endif
#ifdef HAVE_KRB5_GET_INIT_CREDS_OPT_SET_CANONICALIZE
	if (options->canonicalize != -1) {
#ifdef KRB5_GET_INIT_CREDS_OPT_SET_CANONICALIZE_TAKES_3_ARGS
		krb5_get_init_creds_opt_set_canonicalize(ctx,
							 k5_options,
							 options->canonicalize);
#else
		krb5_get_init_creds_opt_set_canonicalize(k5_options,
							 options->canonicalize);
#endif
	}
#endif
}

void
_pam_krb5_set_init_opts_for_pwchange(krb5_context ctx,
				     krb5_get_init_creds_opt *k5_options,
				     struct _pam_krb5_options *options)
{
	krb5_get_init_creds_opt_set_tkt_life(k5_options, 5 * 60);
	krb5_get_init_creds_opt_set_renew_life(k5_options, 0);
	krb5_get_init_creds_opt_set_forwardable(k5_options, 0);
	krb5_get_init_creds_opt_set_proxiable(k5_options, 0);
#ifdef HAVE_KRB5_GET_INIT_CREDS_OPT_SET_CANONICALIZE
	if (options->canonicalize != -1) {
#ifdef KRB5_GET_INIT_CREDS_OPT_SET_CANONICALIZE_TAKES_3_ARGS
		krb5_get_init_creds_opt_set_canonicalize(ctx,
							 k5_options,
							 options->canonicalize);
#else
		krb5_get_init_creds_opt_set_canonicalize(k5_options,
							 options->canonicalize);
#endif
	}
#endif
}

void
_pam_krb5_set_init_opts_for_armor(krb5_context ctx,
				  krb5_get_init_creds_opt *k5_options,
				  struct _pam_krb5_options *options)
{
	krb5_get_init_creds_opt_set_tkt_life(k5_options, 10 * 60);
	krb5_get_init_creds_opt_set_renew_life(k5_options, 0);
	krb5_get_init_creds_opt_set_forwardable(k5_options, 0);
	krb5_get_init_creds_opt_set_proxiable(k5_options, 0);
#ifdef HAVE_KRB5_GET_INIT_CREDS_OPT_SET_CANONICALIZE
#ifdef KRB5_GET_INIT_CREDS_OPT_SET_CANONICALIZE_TAKES_3_ARGS
	krb5_get_init_creds_opt_set_canonicalize(ctx, k5_options, 1);
#else
	krb5_get_init_creds_opt_set_canonicalize(k5_options, 1);
#endif
#endif
}
