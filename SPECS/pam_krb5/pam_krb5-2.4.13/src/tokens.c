/*
 * Copyright 2003,2004,2005,2006,2007,2008,2012,2013 Red Hat, Inc.
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

#include "log.h"
#include "minikafs.h"
#include "options.h"
#include "stash.h"
#include "tokens.h"
#include "userinfo.h"
#include "v5.h"
#include "xstr.h"

int
tokens_useful(void)
{
	if (minikafs_has_afs()) {
		return 1;
	}
	return 0;
}

static int
cell_is_in_option_list(struct _pam_krb5_options *options, const char *cell)
{
	int i;
	for (i = 0; i < options->n_afs_cells; i++) {
		if (strcmp(cell, options->afs_cells[i].cell) == 0) {
			return 1;
		}
	}
	return 0;
}

int
tokens_obtain(krb5_context context,
	      struct _pam_krb5_stash *stash,
	      struct _pam_krb5_options *options,
	      struct _pam_krb5_user_info *info, int newpag)
{
	int i, ret;
	unsigned int n;
	char localcell[LINE_MAX], homecell[LINE_MAX], homedir[LINE_MAX],
	     lnk[LINE_MAX];
	struct stat st;
	uid_t uid;
	const struct {
		const char *name; int method;
	} method_names[] = {
		{"2b", MINIKAFS_METHOD_V5_2B},
		{"rxk5", MINIKAFS_METHOD_RXK5}
	};
	int *methods, n_methods;
	const char *p, *q;

	if (options->debug) {
		debug("obtaining afs tokens");
	}
	uid = options->user_check ? info->uid : getuid();

	/* Check if AFS is running.  If it isn't, no other calls to minikafs
	 * will work, or even be safe to call. */
	if (!minikafs_has_afs()) {
		if (stat("/afs", &st) == 0) {
			warn("afs not running");
		} else {
			if (options->debug) {
				debug("afs not running");
			}
		}
		return PAM_SUCCESS;
	}

	/* Create a PAG. */
	if (newpag) {
		if (options->debug) {
			debug("creating new PAG");
		}
		minikafs_setpag();
		stash->afspag = 1;
	}

	/* Parse the token_strategy option. */
	methods = malloc((strlen(options->token_strategy) + 1) * sizeof(int));
	if (methods == NULL) {
		return PAM_BUF_ERR;
	}
	memset(methods, 0, (strlen(options->token_strategy) + 1) * sizeof(int));
	n_methods = 0;
	p = options->token_strategy;
	while (strlen(p) > 0) {
		q = p + strcspn(p, ",");
		for (n = 0;
		     n < sizeof(method_names) / sizeof(method_names[0]);
		     n++) {
			if (strncmp(p, method_names[n].name,
				    strlen(method_names[n].name)) == 0) {
				methods[n_methods++] = method_names[n].method;
			}
		}
		p = q + strspn(q, ",");
	}

	/* Get the name of the local cell.  The root.afs volume which is
	 * mounted in /afs is mounted from the local cell, so we'll use that
	 * to determine which cell is considered the local cell.  Avoid getting
	 * tripped up by dynamic root support in clients. */
	memset(localcell, '\0', sizeof(localcell));
	if ((minikafs_ws_cell(localcell, sizeof(localcell) - 1) == 0) &&
	    (strcmp(localcell, "dynroot") != 0) &&
	    (!cell_is_in_option_list(options, localcell))) {
		if (options->debug) {
			debug("obtaining tokens for local cell '%s'",
			      localcell);
		}
		ret = minikafs_log(context, stash->v5ccache, options,
				   localcell, NULL, uid,
				   methods, n_methods);
		if (ret != 0) {
			if (stash->v5attempted != 0) {
				warn("got error %d (%s) while obtaining "
				     "tokens for %s",
				     ret, v5_error_message(ret), localcell);
			} else {
				if (options->debug) {
					debug("got error %d (%s) while "
					      "obtaining tokens for %s",
					      ret, v5_error_message(ret),
					      localcell);
				}
			}
		}
	}
	/* Get the name of the cell which houses the user's home directory.  In
	 * case intervening directories aren't readable by system:anyuser
	 * (which gives us an error), keep walking the directory chain until we
	 * either succeed or run out of path components to remove.  And try to
	 * avoid doing the same thing twice. */
	strncpy(homedir, info->homedir ? info->homedir : "/afs",
		sizeof(homedir) - 1);
	homedir[sizeof(homedir) - 1] = '\0';
	/* A common configuration is to have the home directory be a symlink
	 * into /afs.  If the homedir is a symlink, chase it, *once*. */
	if (lstat(homedir, &st) == 0) {
		if (st.st_mode & S_IFLNK) {
			/* Read the link. */
			memset(lnk, '\0', sizeof(lnk));
			if (readlink(homedir, lnk, sizeof(lnk) - 1) == 0) {
				/* If it's an absolute link, then we should
				 * ask about the link destination instead. */
				if ((strlen(lnk) > 0) && (lnk[0] == '/')) {
					strcpy(homedir, lnk);
				}
			}
		}
	}
	i = minikafs_cell_of_file_walk_up(homedir, homecell,
					  sizeof(homecell) - 1);
	if ((i == 0) &&
	    (strcmp(homecell, "dynroot") != 0) &&
	    (strcmp(homecell, localcell) != 0) &&
	    (!cell_is_in_option_list(options, homecell))) {
		if (options->debug) {
			debug("obtaining tokens for home cell '%s'", homecell);
		}
		ret = minikafs_log(context, stash->v5ccache, options,
				   homecell, NULL, uid,
				   methods, n_methods);
		if (ret != 0) {
			if (stash->v5attempted != 0) {
				warn("got error %d (%s) while obtaining "
				     "tokens for %s",
				     ret, v5_error_message(ret), homecell);
			} else {
				if (options->debug) {
					debug("got error %d (%s) while "
					      "obtaining tokens for %s",
					      ret, v5_error_message(ret),
					      homecell);
				}
			}
		}
	}

	/* If there are no additional cells configured, stop here. */
	if (options->afs_cells == NULL) {
		if (options->debug) {
			debug("no additional afs cells configured");
		}
		return PAM_SUCCESS;
	}

	/* Iterate through the list of other cells. */
	for (i = 0; i < options->n_afs_cells; i++) {
		if (options->debug) {
			if (options->afs_cells[i].principal_name != NULL) {
				debug("obtaining tokens for '%s' ('%s')",
				      options->afs_cells[i].cell,
				      options->afs_cells[i].principal_name);
			} else {
				debug("obtaining tokens for '%s'",
				      options->afs_cells[i].cell);
			}
		}
		ret = minikafs_log(context, stash->v5ccache, options,
				   options->afs_cells[i].cell,
				   options->afs_cells[i].principal_name, uid,
				   methods, n_methods);
		if (ret != 0) {
			if (stash->v5attempted != 0) {
				warn("got error %d (%s) while obtaining "
				     "tokens for %s",
				     ret, v5_error_message(ret),
				     options->afs_cells[i].cell);
			} else {
				if (options->debug) {
					debug("got error %d (%s) while "
					      "obtaining tokens for %s",
					      ret, v5_error_message(ret),
					      options->afs_cells[i].cell);
				}
			}
		}
	}

	/* Suppress all errors. */
	return PAM_SUCCESS;
}

int
tokens_release(struct _pam_krb5_stash *stash, struct _pam_krb5_options *options)
{
	struct stat st;

	/* Check if AFS is running.  If it isn't, no other calls to libkrbafs
	 * will work, or even be safe to call. */
	if (!minikafs_has_afs()) {
		if (stat("/afs", &st) == 0) {
			warn("afs not running");
		} else {
			if (options->debug) {
				debug("afs not running");
			}
		}
		return PAM_SUCCESS;
	}

	/* Destroy all tokens. */
	if (stash->afspag != 0) {
		if (options->debug) {
			debug("releasing afs tokens");
		}
		minikafs_unlog();
		stash->afspag = 0;
	}

	/* Suppress all errors. */
	return PAM_SUCCESS;
}
