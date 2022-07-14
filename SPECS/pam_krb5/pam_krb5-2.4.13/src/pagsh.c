/*
 * Copyright 2004,2005,2006 Red Hat, Inc.
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
#include <paths.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#include KRB5_H

#include <security/pam_appl.h>

#include "logstdio.h"
#include "options.h"
#include "stash.h"
#include "minikafs.h"
#include "xstr.h"

struct _pam_krb5_options;
extern char *log_progname;

int
main(int argc, char **argv)
{
	const char *shell, *shellbase;
	char **new_argv;
	int i;

	memset(&log_options, 0, sizeof(log_options));
#ifdef IN_UNPAGSH
	log_progname = "unpagsh";
#else
	log_progname = "pagsh";
#endif

	shell = getenv("SHELL");
	if ((shell == NULL) || (strlen(shell) == 0)) {
		shell = _PATH_BSHELL;
	}
	if (strchr(shell, '/')) {
		shellbase = strrchr(shell, '/') + 1;
	} else {
		shellbase = shell;
	}

	if (argc == 2) {
		if ((strcmp(argv[1], "--help") == 0) ||
		    (strcmp(argv[1], "-h") == 0)) {
			fprintf(stdout,
				"Usage: %s\n"
				"       %s [ -c command ]\n"
				"       %s [ arguments for %s ]\n",
				log_progname, log_progname, log_progname,
				shellbase);
			return 0;
		}
	}

	new_argv = malloc(sizeof(char*) * (argc + 1));
	if (new_argv == NULL) {
		fprintf(stderr, "%s: out of memory\n", log_progname);
		return 1;
	}
	memset(new_argv, 0, sizeof(char*) * (argc + 1));

	new_argv[0] = xstrdup(shell);
	for (i = 1; i < argc; i++) {
		new_argv[i] = argv[i];
	}

	if (minikafs_has_afs()) {
#ifdef IN_UNPAGSH
		if (minikafs_unpag() != 0) {
			fprintf(stderr, "%s: error leaving PAG\n",
				log_progname);
		}
#else
		if (minikafs_setpag() != 0) {
			fprintf(stderr, "%s: error creating new PAG\n",
				log_progname);
		}
#endif
	}

	execvp(new_argv[0], new_argv);
	fprintf(stderr, "%s: exec() failed: %s\n", log_progname,
		strerror(errno));

	return 1;
}
