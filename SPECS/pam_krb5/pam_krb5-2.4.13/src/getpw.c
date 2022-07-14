/*
 * Copyright 2012 Red Hat, Inc.
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
#include <errno.h>
#include <limits.h>
#include <pwd.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#include "getpw.h"
#include "xstr.h"

#if defined(HAVE_GETPWNAM_R) || defined(HAVE___POSIX_GETPWNAM_R)
#define CHUNK_SIZE 128
/* Convert a name to a UID/GID pair. */
static int
_get_pw_nam(const char *name, long id, uid_t *uid, gid_t *gid, char **homedir)
{
	struct passwd passwd, *pwd;
	char *buffer;
	int size, i;

	size = CHUNK_SIZE;
	do {
		/* Allocate a temporary buffer to hold the string data. */
		buffer = malloc(size);
		if (buffer == NULL) {
			return 1;
		}
		memset(buffer, '\0', size);

		/* Give it a shot. */
		pwd = NULL;
#if defined(HAVE_GETPWNAM_R) && !defined(sun)
		if (name != NULL) {
			i = getpwnam_r(name, &passwd, buffer, size, &pwd);
		} else {
			i = getpwuid_r(id, &passwd, buffer, size, &pwd);
		}
#else
		if (name != NULL) {
			i = __posix_getpwnam_r(name, &passwd,
					       buffer, size, &pwd);
		} else {
			i = __posix_getpwuid_r(id, &passwd,
					       buffer, size, &pwd);
		}
#endif

		/* If we got 0 back, AND pwd now points to the passwd
		 * structure, then we succeeded. */
		if ((i == 0) && (pwd == &passwd)) {
			break;
		}

		/* Free the buffer -- we'll reallocate it later. */
		xstrfree(buffer);
		buffer = NULL;

		/* We need to use more space if we got ERANGE back, so bail on
		 * any other condition. */
		if (i != ERANGE) {
			return 1;
		}

		/* Increase the size of the buffer. */
		size += CHUNK_SIZE;
	} while (size > 0);

	/* If we exited successfully, then pull out the UID/GID. */
	if ((i == 0) && (pwd != NULL) && (buffer != NULL)) {
		*uid = pwd->pw_uid;
		*gid = pwd->pw_gid;
		if (homedir != NULL) {
			*homedir = xstrdup(pwd->pw_dir);
		}
		free(buffer);
		return 0;
	}

	/* Failed. */
	if (buffer != NULL) {
		free(buffer);
	}
	return 1;
}
#else
static int
_get_pw_nam(const char *name, long id, uid_t *uid, gid_t *gid, char **homedir)
{
	struct passwd *pwd;
	if (name != NULL) {
		pwd = getpwnam(name);
	} else {
		pwd = getpwuid(id);
	}
	if (pwd != NULL) {
		*uid = pwd->pw_uid;
		*gid = pwd->pw_gid;
		if (homedir != NULL) {
			*homedir = xstrdup(pwd->pw_dir);
		}
		return 0;
	}
	return 1;
}
#endif

int
_pam_krb5_get_pw_ids(const char *name, long id, uid_t *uid, gid_t *gid)
{
	return _get_pw_nam(name, id, uid, gid, NULL);
}

int
_pam_krb5_get_pw_info(const char *name, long id, uid_t *uid, gid_t *gid,
		      char **homedir)
{
	return _get_pw_nam(name, id, uid, gid, homedir);
}
