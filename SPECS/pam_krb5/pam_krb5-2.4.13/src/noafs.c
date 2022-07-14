/*
 * Copyright 2005,2006 Red Hat, Inc.
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

#ifdef HAVE_SECURITY_PAM_APPL_H
#include <security/pam_appl.h>
#endif

#ifdef HAVE_SECURITY_PAM_MODULES_H
#include <security/pam_modules.h>
#endif
 
#include KRB5_H

#include "log.h"
#include "options.h"
#include "minikafs.h"
#include "tokens.h"

int
minikafs_has_afs(void)
{
	return 0;
}

int
minikafs_cell_of_file(const char *file, char *cell, size_t length)
{
	return -1;
}

int
minikafs_realm_of_cell(struct _pam_krb5_options *options,
		       const char *cell, char *realm, size_t length)
{
	return -1;
}

int
minikafs_setpag(void)
{
	return -1;
}

int
minikafs_unlog(void)
{
	return -1;
}

int
minikafs_log(krb5_context ctx, krb5_ccache ccache,
	     struct _pam_krb5_options *options,
	     const char *cell, const char *hint_principal,
	     uid_t uid, const int *methods, int n_methods)
{
	return -1;
}

int
tokens_useful()
{
	return 0;
}

int
tokens_obtain(krb5_context context, struct _pam_krb5_stash *stash,
	      struct _pam_krb5_options *options,
	      struct _pam_krb5_user_info *info, int newpag)
{
	return -1;
}

int
tokens_release(struct _pam_krb5_stash *stash,
	       struct _pam_krb5_options *options)
{
	return -1;
}
