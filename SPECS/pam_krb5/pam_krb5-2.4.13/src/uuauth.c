/*
 * Copyright 2010 Red Hat, Inc.
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
#include "init.h"
#include "initopts.h"
#include "log.h"
#include "options.h"
#include "perms.h"
#include "prompter.h"
#include "stash.h"
#include "userinfo.h"
#include "v5.h"
#include "xstr.h"

extern char *log_progname;

int
main(int argc, const char **argv)
{
	krb5_context ctx;
	krb5_ccache ccache, occache;
	krb5_principal client, tgs;
	krb5_ticket *ticket;
	krb5_creds mcreds, *creds, ocreds;
	krb5_keyblock *key;
	krb5_auth_context auth_con, oauth_con;
	krb5_data req;
	krb5_flags flags;
	krb5_error_code ret;

	log_progname = "uucheck";

	ctx = NULL;
	ret = _pam_krb5_init_ctx(&ctx, argc, argv);
	if (ret != 0) {
		crit("Error initializing Kerberos: %s.", v5_error_message(ret));
		return ret;
	}

	ccache = NULL;
	ret = krb5_cc_default(ctx, &ccache);
	if (ret != 0) {
		crit("Error opening ccache: %s.", v5_error_message(ret));
		return ret;
	}
	occache = NULL;
	if (argc > 1) {
		ret = krb5_cc_resolve(ctx, argv[1], &occache);
		if (ret != 0) {
			crit("Error opening ccache %s: %s.",
			     argv[1], v5_error_message(ret));
			return ret;
		}
	} else {
		occache = ccache;
	}

	client = NULL;
	ret = krb5_cc_get_principal(ctx, ccache, &client);
	if (ret != 0) {
		crit("Error determining client principal name: %s.",
		     v5_error_message(ret));
		return ret;
	}

	tgs = NULL;
	ret = krb5_build_principal_ext(ctx, &tgs,
				       v5_princ_realm_length(client),
				       v5_princ_realm_contents(client),
				       KRB5_TGS_NAME_SIZE,
				       KRB5_TGS_NAME,
				       v5_princ_realm_length(client),
				       v5_princ_realm_contents(client),
				       0);
	if (ret != 0) {
		crit("Error building TGS principal name: %s.",
		     v5_error_message(ret));
		return ret;
	}

	memset(&mcreds, 0, sizeof(mcreds));
	mcreds.client = client;
	mcreds.server = tgs;

	memset(&ocreds, 0, sizeof(ocreds));
	ret = krb5_cc_retrieve_cred(ctx, occache, 0, &mcreds, &ocreds);
	if (ret != 0) {
		crit("Error getting old creds: %s.",
		     v5_error_message(ret));
		return ret;
	}
	key = v5_creds_get_key(&ocreds);

	creds = NULL;
	mcreds.server = client;
	mcreds.second_ticket = ocreds.ticket;
	ret = krb5_get_credentials(ctx, KRB5_GC_USER_USER, ccache,
				   &mcreds, &creds);
	if (ret != 0) {
		crit("Error getting creds: %s.",
		     v5_error_message(ret));
		return ret;
	}

	memset(&auth_con, 0, sizeof(auth_con));
	ret = krb5_auth_con_init(ctx, &auth_con);
	if (ret != 0) {
		crit("Error initializing auth context: %s.",
		     v5_error_message(ret));
		return ret;
	}

	memset(&req, 0, sizeof(req));
	ret = krb5_mk_req_extended(ctx, &auth_con, AP_OPTS_USE_SESSION_KEY,
				   NULL, creds, &req);
	if (ret != 0) {
		crit("Error generating AP request: %s.",
		     v5_error_message(ret));
		return ret;
	}

	memset(&oauth_con, 0, sizeof(oauth_con));
	ret = krb5_auth_con_init(ctx, &oauth_con);
	if (ret != 0) {
		crit("Error initializing auth context: %s.",
		     v5_error_message(ret));
		return ret;
	}
	ret = v5_auth_con_setuserkey(ctx, oauth_con, key);

	flags = 0;
	ticket = NULL;
	ret = krb5_rd_req(ctx, &oauth_con, &req, NULL, NULL, &flags, &ticket);
	if (ret != 0) {
		crit("Error receiving AP request: %s.",
		     v5_error_message(ret));
		return ret;
	}
	if (krb5_principal_compare(ctx, v5_ticket_get_client(ticket),
				   client) == 0) {
		crit("Client in request differs from expected client.");
		return ret;
	}

	errno = 0;
	warn("OK");

	krb5_free_ticket(ctx, ticket);
	krb5_free_data_contents(ctx, &req);
	krb5_auth_con_free(ctx, auth_con);
	krb5_auth_con_free(ctx, oauth_con);
	krb5_free_cred_contents(ctx, &ocreds);
	krb5_free_creds(ctx, creds);
	krb5_free_principal(ctx, tgs);
	krb5_free_principal(ctx, client);
	if (ccache != occache) {
		krb5_cc_close(ctx, occache);
	}
	krb5_cc_close(ctx, ccache);
	_pam_krb5_free_ctx(ctx);

	return 0;
}
