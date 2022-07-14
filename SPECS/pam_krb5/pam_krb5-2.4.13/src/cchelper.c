/*
 * Copyright 2012,2013 Red Hat, Inc.
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
#include <sys/select.h>
#include <sys/stat.h>
#include <sys/wait.h>
#include <errno.h>
#include <fcntl.h>
#include <grp.h>
#include <limits.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#include KRB5_H

#ifdef HAVE_SECURITY_PAM_APPL_H
#include <security/pam_appl.h>
#endif

#ifdef HAVE_SECURITY_PAM_MODULES_H
#include <security/pam_modules.h>
#endif

#include "cchelper.h"
#include "log.h"
#include "mkdir.h"
#include "options.h"
#include "stash.h"
#include "userinfo.h"
#include "v5.h"
#include "xstr.h"

ssize_t
_pam_krb5_write_with_retry(int fd, const unsigned char *buffer, ssize_t len)
{
	ssize_t length, ret;
	fd_set fds;
	length = 0;
	while (len > length) {
		ret = write(fd, buffer + length, len - length);
		switch (ret) {
		case 0:
			return length;
			break;
		case -1:
			switch (errno) {
			case EINTR:
			case EAGAIN:
				FD_ZERO(&fds);
				FD_SET(fd, &fds);
				select(fd + 1, NULL, &fds, &fds, NULL);
				if (FD_ISSET(fd, &fds)) {
					continue;
				}
				break;
			}
			return length;
			break;
		default:
			length += ret;
			break;
		}
	}
	return length;
}

ssize_t
_pam_krb5_read_with_retry(int fd, unsigned char *buffer, ssize_t len)
{
	ssize_t length, ret;
	fd_set fds;
	length = 0;
	while (len > length) {
		ret = read(fd, buffer + length, len - length);
		switch (ret) {
		case 0:
			return length;
			break;
		case -1:
			switch (errno) {
			case EINTR:
			case EAGAIN:
				FD_ZERO(&fds);
				FD_SET(fd, &fds);
				select(fd + 1, &fds, NULL, &fds, NULL);
				if (FD_ISSET(fd, &fds)) {
					continue;
				}
				break;
			}
			return length;
			break;
		default:
			length += ret;
			break;
		}
	}
	return length;
}

/* Pipe the specified data in to the specified helper and capture its exit
 * status and output. */
static int
_pam_krb5_cchelper_run(const char *helper, const char *flag, const char *ccname,
		       uid_t uid, gid_t gid,
		       const unsigned char *stdin_data, ssize_t stdin_data_len,
		       unsigned char *stdout_data, size_t stdout_data_max_len,
		       ssize_t *stdout_data_len)
{
	int i;
	int inpipe[2], outpipe[2], dummy[3], status;
	char uidstr[100], gidstr[100];
	pid_t child;
	struct sigaction saved_sigchld_handler, saved_sigpipe_handler;
	struct sigaction ignore_handler, default_handler;
	for (i = 0; i < 3; i++) {
		dummy[i] = open("/dev/null", O_RDONLY);
	}
	if (pipe(inpipe) == -1) {
		for (i = 0; i < 3; i++) {
			close(dummy[i]);
		}
		return -1;
	}
	if (pipe(outpipe) == -1) {
		for (i = 0; i < 3; i++) {
			close(dummy[i]);
		}
		close(inpipe[0]);
		close(inpipe[1]);
		return -1;
	}
	/* Set signal handlers here.  We used to do it later, but that turns
	 * out to be a race if the child decides to exit immediately. */
	memset(&default_handler, 0, sizeof(default_handler));
	default_handler.sa_handler = SIG_DFL;
	if (sigaction(SIGCHLD, &default_handler, &saved_sigchld_handler) != 0) {
		close(inpipe[0]);
		close(inpipe[1]);
		close(outpipe[0]);
		close(outpipe[1]);
		return -1;
	}
	memset(&ignore_handler, 0, sizeof(ignore_handler));
	ignore_handler.sa_handler = SIG_IGN;
	if (sigaction(SIGPIPE, &ignore_handler, &saved_sigpipe_handler) != 0) {
		sigaction(SIGCHLD, &saved_sigchld_handler, NULL);
		close(inpipe[0]);
		close(inpipe[1]);
		close(outpipe[0]);
		close(outpipe[1]);
		return -1;
	}
	switch (child = fork()) {
	case -1:
		sigaction(SIGCHLD, &saved_sigchld_handler, NULL);
		sigaction(SIGPIPE, &saved_sigpipe_handler, NULL);
		for (i = 0; i < 3; i++) {
			close(dummy[i]);
		}
		close(inpipe[0]);
		close(inpipe[1]);
		close(outpipe[0]);
		close(outpipe[1]);
		return -1;
		break;
	case 0:
		/* We're the child. */
		close(inpipe[1]);
		close(outpipe[0]);
		for (i = 0; i < sysconf(_SC_OPEN_MAX); i++) {
			if ((i != inpipe[0]) && (i != outpipe[1]) &&
			    (i != STDERR_FILENO)) {
				close(i);
			}
		}
		dup2(outpipe[1], STDOUT_FILENO);
		dup2(inpipe[0], STDIN_FILENO);
#ifdef HAVE_LONG_LONG
		snprintf(uidstr, sizeof(uidstr), "%llu",
			 (unsigned long long) uid);
		snprintf(gidstr, sizeof(gidstr), "%llu",
			 (unsigned long long) gid);
#else
		snprintf(uidstr, sizeof(uidstr), "%lu", (unsigned long) uid);
		snprintf(gidstr, sizeof(gidstr), "%lu", (unsigned long) gid);
#endif
		if ((strlen(uidstr) > sizeof(uidstr) - 2) ||
		    (strlen(gidstr) > sizeof(gidstr) - 2)) {
			_exit(-1);
		}
		if (uid == 0) {
			setgroups(0, NULL);
		}
		/* Now, attempt to assume the desired uid/gid pair.  Note that
		 * if we're not root, this is allowed to fail. */
		if ((gid != getgid()) || (gid != getegid())) {
			i = setregid(gid, gid);
		}
		if ((uid != getuid()) || (uid != geteuid())) {
			i = setreuid(uid, uid);
		}
		execl(helper, helper, flag, ccname, uidstr, gidstr, NULL);
		warn("error running helper \"%s\": %s", helper,
		     strerror(errno));
		_exit(-1);
		break;
	default:
		/* parent */
		for (i = 0; i < 3; i++) {
			close(dummy[i]);
		}
		close(inpipe[0]);
		close(outpipe[1]);
		if (_pam_krb5_write_with_retry(inpipe[1],
					       stdin_data,
					       stdin_data_len) == stdin_data_len) {
			close(inpipe[1]);
			if (stdout_data != NULL) {
				memset(stdout_data, '\0', stdout_data_max_len);
				i = _pam_krb5_read_with_retry(outpipe[0],
							      stdout_data,
							      stdout_data_max_len);
				*stdout_data_len = i;
			}
		} else {
			close(inpipe[1]);
			if (stdout_data != NULL) {
				memset(stdout_data, '\0', stdout_data_max_len);
				*stdout_data_len = 0;
			}
		}
		waitpid(child, &status, 0);
		close(outpipe[0]);
		sigaction(SIGCHLD, &saved_sigchld_handler, NULL);
		sigaction(SIGPIPE, &saved_sigpipe_handler, NULL);
		return WIFEXITED(status) ? WEXITSTATUS(status) : -1;
		break;
	}
	abort(); /* not reached */
}

static int
_pam_krb5_cchelper_cred_blob(krb5_context ctx, struct _pam_krb5_stash *stash,
			     struct _pam_krb5_options *options,
			     const char *realm,
			     unsigned char **blob, ssize_t *blob_size)
{
	krb5_ccache fccache, mccache;
	char ccname[PATH_MAX];
	struct stat st;
	int fd;

	*blob = NULL;
	*blob_size = 0;
	/* Check that we have creds. */
	if ((stash->v5ccache == NULL) ||
	    (v5_ccache_has_tgt(ctx, stash->v5ccache,
			       realm, NULL) != 0)) {
		warn("no creds to save");
		return -1;
	}
	/* Create a temporary memory cache. */
	snprintf(ccname, sizeof(ccname), "MEMORY:%p", &mccache);
	if (krb5_cc_resolve(stash->v5ctx, ccname, &mccache) != 0) {
		warn("error creating temporary credential cache");
		return -1;
	}
	if (v5_cc_copy(stash->v5ctx, realm,
		       stash->v5ccache, &mccache) != 0) {
		warn("error writing to temporary credential cache \"%s\"",
		     ccname);
		krb5_cc_destroy(stash->v5ctx, mccache);
		return -1;
	}
	/* Create a temporary ccache file. */
	snprintf(ccname, sizeof(ccname),
		 "FILE:%s/pam_krb5_tmp_XXXXXX", options->ccache_dir);
	fd = mkstemp(ccname + 5);
	if (fd == -1) {
		warn("error creating temporary ccache file \"%s\"", ccname + 5);
		krb5_cc_destroy(stash->v5ctx, mccache);
		return -1;
	}
	/* Write the credentials to that file. */
	fccache = NULL;
	if (krb5_cc_resolve(stash->v5ctx, ccname, &fccache) != 0) {
		warn("error opening credential cache file \"%s\" for writing",
		     ccname + 5);
		unlink(ccname + 5);
		close(fd);
		krb5_cc_destroy(stash->v5ctx, mccache);
		return -1;
	}
	if (v5_cc_copy(stash->v5ctx, realm,
		       mccache, &fccache) != 0) {
		warn("error writing to credential cache file \"%s\"",
		     ccname + 5);
		krb5_cc_close(stash->v5ctx, fccache);
		unlink(ccname + 5);
		close(fd);
		krb5_cc_destroy(stash->v5ctx, mccache);
		return -1;
	}
	krb5_cc_close(stash->v5ctx, fccache);
	krb5_cc_destroy(stash->v5ctx, mccache);
	/* Read the file's size. */
	if (lstat(ccname + 5, &st) != 0) {
		warn("error lstat()ing credential cache file \"%s\": %s",
		     ccname + 5, strerror(errno));
		krb5_cc_close(stash->v5ctx, fccache);
		unlink(ccname + 5);
		close(fd);
		return -1;
	}
	/* Allocate space. */
	*blob = malloc(st.st_size);
	if (*blob == NULL) {
		warn("out of memory reading \"%s\"", ccname + 5);
		krb5_cc_close(stash->v5ctx, fccache);
		unlink(ccname + 5);
		close(fd);
		return -1;
	}
	*blob_size = st.st_size;
	close(fd);
	/* Slurp up the file contents. */
	fd = open(ccname + 5, O_RDONLY);
	if (fd == -1) {
		warn("error opening \"%s\": %s", ccname + 5, strerror(errno));
		close(fd);
		krb5_cc_close(stash->v5ctx, fccache);
		unlink(ccname + 5);
		free(*blob);
		*blob = NULL;
		*blob_size = 0;
		return -1;
	}
	if (_pam_krb5_read_with_retry(fd, *blob, *blob_size) != *blob_size) {
		warn("error reading \"%s\": %s", ccname + 5, strerror(errno));
		close(fd);
		krb5_cc_close(stash->v5ctx, fccache);
		unlink(ccname + 5);
		free(*blob);
		*blob = NULL;
		*blob_size = 0;
		return -1;
	}
	/* Done. */
	close(fd);
	unlink(ccname + 5);
	return 0;
}

int
_pam_krb5_cchelper_create(krb5_context ctx, struct _pam_krb5_stash *stash,
			  struct _pam_krb5_options *options,
			  const char *ccname_template,
			  const char *user,
			  struct _pam_krb5_user_info *userinfo,
			  uid_t uid, gid_t gid,
			  char **ccname)
{
	unsigned char *cred_blob, output[PATH_MAX];
	char *ccpattern;
	const char *residual;
	int i;
	ssize_t cred_blob_size, osize;

	ccpattern = v5_user_info_subst(ctx, user, userinfo, options,
				       ccname_template);
	if (ccpattern == NULL) {
		return -1;
	}

	cred_blob = NULL;
	if (_pam_krb5_cchelper_cred_blob(ctx, stash, options, userinfo->realm,
					 &cred_blob, &cred_blob_size) != 0) {
		free(ccpattern);
		return -1;
	}

	residual = strchr(ccpattern, ':');
	if (residual != NULL) {
		residual++;
		if (_pam_krb5_leading_mkdir(residual, options) != 0) {
			if (options->debug) {
				debug("error ensuring directory for \"%s\"",
				      residual);
			}
		}
	}

	i = _pam_krb5_cchelper_run(options->cchelper_path, "-c", ccpattern,
				   uid, gid, cred_blob, cred_blob_size,
				   output, sizeof(output), &osize);
	free(cred_blob);
	if (i == 0) {
		*ccname = xstrndup((const char *) output, osize);
		if (*ccname == NULL) {
			free(ccpattern);
			return -1;
		} else {
			(*ccname)[strcspn(*ccname, "\r\n")] = '\0';
			if (options->debug) {
				debug("created ccache \"%s\"", *ccname);
			}
		}
	} else {
		warn("error creating ccache using pattern \"%s\"", ccpattern);
	}
	free(ccpattern);
	return i;
}

int
_pam_krb5_cchelper_update(krb5_context ctx, struct _pam_krb5_stash *stash,
			  struct _pam_krb5_options *options,
			  const char *user,
			  struct _pam_krb5_user_info *userinfo,
			  uid_t uid, gid_t gid,
			  const char *ccname)
{
	unsigned char *cred_blob, output[PATH_MAX];
	int i;
	ssize_t cred_blob_size, osize;

	cred_blob = NULL;
	if (_pam_krb5_cchelper_cred_blob(ctx, stash, options, userinfo->realm,
					 &cred_blob, &cred_blob_size) != 0) {
		return -1;
	}
	i = _pam_krb5_cchelper_run(options->cchelper_path, "-u", ccname,
				   uid, gid, cred_blob, cred_blob_size,
				   output, sizeof(output), &osize);
	if (i == 0) {
		if (options->debug) {
			debug("updated ccache \"%s\"", ccname);
		}
	} else {
		warn("error updating ccache \"%s\"", ccname);
	}
	free(cred_blob);
	return i;
}

int
_pam_krb5_cchelper_destroy(krb5_context ctx, struct _pam_krb5_stash *stash,
			   struct _pam_krb5_options *options,
			   const char *ccname)
{
	unsigned char output[PATH_MAX];
	ssize_t osize;
	int i;

	i = _pam_krb5_cchelper_run(options->cchelper_path, "-d", ccname,
				   -1, -1, NULL, 0,
				   output, sizeof(output), &osize);
	if (i == 0) {
		if (options->debug) {
			debug("destroyed ccache \"%s\"", ccname);
		}
	} else {
		warn("error destroying ccache \"%s\"", ccname);
	}
	return i;
}
