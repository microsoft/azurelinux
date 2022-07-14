/*
 * Copyright 2008,2013 Red Hat, Inc.
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

#include <sys/types.h>
#include <stdlib.h>
#include <unistd.h>
#include "perms.h"

struct _pam_krb5_perms {
	uid_t ruid, euid;
	gid_t rgid, egid;
};

struct _pam_krb5_perms *
_pam_krb5_switch_perms(void)
{
	struct _pam_krb5_perms *ret;
	ret = malloc(sizeof(*ret));
	if (ret != NULL) {
		ret->ruid = getuid();
		ret->euid = geteuid();
		ret->rgid = getgid();
		ret->egid = getegid();
		if (ret->ruid == ret->euid) {
			ret->ruid = -1;
			ret->euid = -1;
		}
		if (ret->rgid == ret->egid) {
			ret->rgid = -1;
			ret->egid = -1;
		}
		if (setregid(ret->egid, ret->rgid) == -1) {
			free(ret);
			ret = NULL;
		} else {
			if (setreuid(ret->euid, ret->ruid) == -1) {
				int i;
				i = setregid(ret->rgid, ret->egid);
				i++;
				free(ret);
				ret = NULL;
			}
		}
	}
	return ret;
}

int
_pam_krb5_restore_perms(struct _pam_krb5_perms *saved)
{
	int ret = -1;
	if (saved != NULL) {
		if ((setreuid(saved->ruid, saved->euid) == 0) &&
		    (setregid(saved->rgid, saved->egid) == 0)) {
			ret = 0;
		}
		free(saved);
	}
	return ret;
}
