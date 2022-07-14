/*
 * Copyright 2010,2013 Red Hat, Inc.
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

#include KRB5_H

#ifndef HAVE_ERROR_MESSAGE_DECL
#ifdef HAVE_COM_ERR_H
#include <com_err.h>
#elif defined(HAVE_ET_COM_ERR_H)
#include <et/com_err.h>
#endif
#endif

#ifdef HAVE_SECURITY_PAM_APPL_H
#include <security/pam_appl.h>
#endif

#include "init.h"
#include "log.h"
#include "options.h"
#include "v5.h"

int
main(int argc, const char **argv)
{
	krb5_context ctx;
	krb5_ccache ccache;
	krb5_auth_context cctx, sctx;
	krb5_creds mcreds, creds, *ncreds;
	krb5_keytab keytab;
	krb5_ticket *ticket;
	krb5_principal server;
	krb5_verify_init_creds_opt opts;
	krb5_flags ap_opts;
	krb5_data req, transited;
	int ret;
	unsigned int i;

	ctx = NULL;
	ret = krb5_init_context(&ctx);
	if (ret != 0) {
		crit("error initializing Kerberos: %s", v5_error_message(ret));
		return ret;
	}

	ccache = NULL;
	ret = krb5_cc_default(ctx, &ccache);
	if (ret != 0) {
		crit("error resolving ccache: %s", v5_error_message(ret));
		return ret;
	}

	keytab = NULL;
	ret = krb5_kt_default(ctx, &keytab);
	if (ret != 0) {
		crit("error resolving keytab: %s", v5_error_message(ret));
		return ret;
	}

	server = NULL;
	memset(&mcreds, 0, sizeof(mcreds));
	ret = krb5_cc_get_principal(ctx, ccache, &mcreds.client);
	if (ret != 0) {
		crit("error reading client name from ccache: %s",
		     v5_error_message(ret));
		return ret;
	}

	if (argc > 1) {
		ret = krb5_parse_name(ctx, argv[1], &server);
		if (ret != 0) {
			crit("error parsing principal name %s: %s", argv[1],
			     v5_error_message(ret));
		}
		mcreds.server = server;
		ret = krb5_get_credentials(ctx, 0, ccache, &mcreds, &ncreds);
		if (ret != 0) {
			crit("error getting creds: %s", v5_error_message(ret));
			return ret;
		}
		memset(&cctx, 0, sizeof(cctx));
		ret = krb5_mk_req_extended(ctx, &cctx, 0, NULL, ncreds, &req);
		if (ret != 0) {
			crit("error making AP-REQ: %s", v5_error_message(ret));
			return ret;
		}
		memset(&sctx, 0, sizeof(sctx));
		ap_opts = 0;
		ticket = NULL;
		ret = krb5_rd_req(ctx, &sctx, &req, server, keytab, &ap_opts,
				  &ticket);
		if (ret != 0) {
			crit("error parsing AP-REQ: %s", v5_error_message(ret));
			return ret;
		}
#ifdef HAVE_KRB5_TICKET_ENC_PART2
		if (ticket->enc_part2 != NULL) {
			printf("transited: \"");
			transited = ticket->enc_part2->transited.tr_contents;
			for (i = 0; i < transited.length; i++) {
				unsigned char u;
				u = transited.data[i];
				if (u > 32 && u < 126) {
					printf("%c", u);
				} else {
					printf("\%02x", u);
				}
			}
			printf("\"\n");
		}
#endif
#ifdef HAVE_KRB5_TICKET_TICKET_TRANSITED_CONTENTS
		if (ticket->ticket.transited.contents.length > 0) {
			printf("transited: \"");
			for (i = 0;
			     i < ticket->ticket.transited.contents.length;
			     i++) {
				unsigned char *pu, u;
				pu = ticket->ticket.transited.contents.data;
				u = pu[i];
				if (u > 32 && u < 126) {
					printf("%c", u);
				} else {
					printf("\%02x", u);
				}
			}
			printf("\"\n");
		}
#endif
		printf("OK (%s)\n", argv[1]);
	} else {
		ret = krb5_build_principal_ext(ctx, &mcreds.server,
					       v5_princ_realm_length(mcreds.client),
					       v5_princ_realm_contents(mcreds.client),
					       KRB5_TGS_NAME_SIZE,
					       KRB5_TGS_NAME,
					       v5_princ_realm_length(mcreds.client),
					       v5_princ_realm_contents(mcreds.client),
					       0);
		if (ret != 0) {
			crit("error building ticket granting server name: %s",
			     v5_error_message(ret));
			return ret;
		}

		ret = krb5_cc_retrieve_cred(ctx, ccache, 0, &mcreds, &creds);
		if (ret != 0) {
			crit("error reading ccache: %s", v5_error_message(ret));
			return ret;
		}
		krb5_verify_init_creds_opt_init(&opts);
		ret = krb5_verify_init_creds(ctx, &creds,
					     server, keytab, NULL,
					     &opts);
		if (ret != 0) {
			crit("error verifying creds: %s",
			     v5_error_message(ret));
		} else {
			printf("OK\n");
		}
	}

	_pam_krb5_free_ctx(ctx);

	return ret;
}
