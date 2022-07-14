/*
 * Copyright 2005,2006,2007,2009 Red Hat, Inc.
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
#include <sys/wait.h>
#include <limits.h>
#include <pwd.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#ifdef HAVE_SECURITY_PAM_APPL_H
#include <security/pam_appl.h>
#endif

#ifdef HAVE_SECURITY_PAM_MODULES_H
#define PAM_SM_AUTH
#define PAM_SM_ACCOUNT
#define PAM_SM_SESSION
#define PAM_SM_PASSWORD
#include <security/pam_modules.h>
#endif
#ifdef HAVE_SECURITY_PAM_MISC_H
#include <security/pam_misc.h>
#endif

#include KRB5_H

#include "logstdio.h"
#include "options.h"

#include "xstr.h"

struct linux_pam_handle {
	char *authtok;
	int caller;
};

static int
local_conv(int num_msg, const struct pam_message **msgm,
	   struct pam_response **response, void *appdata_ptr)
{
	int i, abi_flag;
	const struct pam_message *msg;
	char buffer[LINE_MAX];
	*response = malloc(num_msg * sizeof(struct pam_response));
	if (*response == NULL) {
		return PAM_BUF_ERR;
	}
	memset(*response, 0, num_msg * sizeof(struct pam_response));
	abi_flag = (appdata_ptr != NULL) ? *(int*)appdata_ptr : 0;
	for (i = 0; i < num_msg; i++) {
		if (abi_flag) {
			/* array of pointers to structs */
			msg = msgm[i];
		} else {
			/* pointer to array of structs */
			msg = &((*msgm)[i]);
		}
		switch (msg->msg_style) {
		case PAM_TEXT_INFO:
		case PAM_ERROR_MSG:
		case PAM_PROMPT_ECHO_ON:
		case PAM_PROMPT_ECHO_OFF:
			printf("%s", msg->msg ? msg->msg : "(null)");
			break;
		default:
			free(*response);
			*response = NULL;
			return PAM_CONV_ERR;
			break;
		}
		switch (msg->msg_style) {
		case PAM_TEXT_INFO:
		case PAM_ERROR_MSG:
			printf("\n");
			fflush(stdout);
			(*response)[i].resp_retcode = 0;
			break;
		case PAM_PROMPT_ECHO_ON:
		case PAM_PROMPT_ECHO_OFF:
			fflush(stdout);
			(*response)[i].resp_retcode = 0;
			if (msg->msg_style == PAM_PROMPT_ECHO_OFF) {
				strcpy(buffer, getpass(""));
			} else {
				if (fgets(buffer, sizeof(buffer),
					  stdin) == NULL) {
					memset(buffer, '\0', sizeof(buffer));
				}
			}
			(*response)[i].resp = xstrndup(buffer,
						       strcspn(buffer, "\r\n"));
			break;
		default:
			free(*response);
			*response = NULL;
			return PAM_CONV_ERR;
			break;
		}
		
	}
	return 0;
}

#ifndef HAVE_MISC_CONV
static int
misc_conv(int num_msg, const struct pam_message **msgm,
	  struct pam_response **response, void *appdata_ptr)
{
	return local_conv(num_msg, msgm, response, appdata_ptr);
}
#endif

static int
gather_args(int argc, char **argv, int start, int *pargc, const char ***pargv)
{
	int i;
	for (i = start; i < argc; i++) {
		if (strncmp(argv[i], "--", 2) == 0) {
			break;
		}
	}
	*pargc = i - start;
	switch (*pargc) {
	case 0:
		*pargv = NULL;
		break;
	default:
		*pargv = malloc((*pargc + 1) * sizeof(char*));
		if (*pargv == NULL) {
			*pargc = 0;
			return 0;
		}
		for (i = 0; i < *pargc; i++) {
			(*pargv)[i] = xstrdup(argv[start + i]);
		}
		(*pargv)[i] = NULL;
	}
	return *pargc;
}
static void
free_args(int *pargc, const char ***pargv)
{
	int i;
	for (i = 0; i < *pargc; i++) {
		free((char*) (*pargv)[i]);
	}
	if (*pargv != NULL) {
		free(*pargv);
	}
	*pargv = NULL;
	*pargc = 0;
}

int
main(int argc, char **argv)
{
	int i, ret, abi_flag, pargc;
	const char *user, *service, *authtok, *old_authtok, **pargv;
	char **envlist;
	struct passwd *pwd;
	struct pam_conv conv;
	pam_handle_t *pamh;

	if (argc < 2) {
		fprintf(stderr, "Usage: %s [flags]\n"
			"\t--debug\n"
			"\t--toggle-abi\n"
			"\t--setservice SERVICE\n"
			"\t--setuser USER\n"
			"\t--setauthtok AUTHTOK\n"
			"\t--setoldauthtok OLD_AUTHTOK\n"
			"\t--restart\n"
			"\t--run [cmd]\n"
			"\t--auth [args...]\n"
			"\t--open-session [args...]\n"
			"\t--setcred-establish [args...]\n"
			"\t--setcred-reinitialize [args...]\n"
			"\t--setcred-delete [args...]\n"
			"\t--close-session [args...]\n"
			"\t--acct-mgmt [args...]\n"
			"\t--chauthtok-prelim [args...]\n"
			"\t--chauthtok-update [args...]\n",
			argv[0]);
		return 1;
	}

	pwd = getpwuid(getuid());
	if (pwd == NULL) {
		fprintf(stderr, "Unable to determine name of current user!\n");
		return 1;
	}
	user = pwd->pw_name;
	service = "login";
	authtok = NULL;
	old_authtok = NULL;
	ret = 0;
	pamh = NULL;

	memset(&conv, 0, sizeof(conv));
	conv.conv = local_conv;
	abi_flag = 0;
	conv.appdata_ptr = &abi_flag;
	pargc = 0;
	pargv = NULL;

	for (i = 1; i < argc; i++) {
		fflush(stdout);
		if (strcmp(argv[i], "--debug") == 0) {
			log_options.debug++;
			continue;
		}
		if (strcmp(argv[i], "--toggle-abi") == 0) {
			abi_flag = !abi_flag;
			continue;
		}
		if (strcmp(argv[i], "--setservice") == 0) {
			service = argv[i + 1];
			i++;
			continue;
		}
		if (strcmp(argv[i], "--setuser") == 0) {
			user = argv[i + 1];
			i++;
			continue;
		}
		if (strcmp(argv[i], "--setauthtok") == 0) {
			authtok = argv[i + 1];
			i++;
			continue;
		}
		if (strcmp(argv[i], "--setoldauthtok") == 0) {
			old_authtok = argv[i + 1];
			i++;
			continue;
		}
		if (pamh == NULL) {
			ret = pam_start(service, user, &conv, &pamh);
			printf("start: %d\n", ret);
#ifdef __LINUX_PAM__
			/* Linux-PAM *actively* tries to break us. */
			((struct linux_pam_handle*)pamh)->caller = 1;
#endif
			if (authtok != NULL) {
				ret = pam_set_item(pamh, PAM_AUTHTOK, authtok);
				printf("set authtok: %d%s %s\n", ret,
				       ret ? ":" : "",
				       ret ? pam_strerror(pamh, ret) : "");
			}
			if (old_authtok != NULL) {
				ret = pam_set_item(pamh, PAM_OLDAUTHTOK,
						   old_authtok);
				printf("set old authtok: %d%s %s\n", ret,
				       ret ? ":" : "",
				       ret ? pam_strerror(pamh, ret) : "");
			}
		}
		if (strcmp(argv[i], "--restart") == 0) {
#ifdef __LINUX_PAM__
			/* Linux-PAM *actively* tries to break us. */
			((struct linux_pam_handle*)pamh)->caller = 2;
#endif
			ret = pam_end(pamh, 0);
			printf("end: %d\n", ret);
			pamh = NULL;
			ret = pam_start(service, user, &conv, &pamh);
			printf("start: %d\n", ret);
#ifdef __LINUX_PAM__
			/* Linux-PAM *actively* tries to break us. */
			((struct linux_pam_handle*)pamh)->caller = 1;
#endif
			continue;
		}
		if (strcmp(argv[i], "--auth") == 0) {
			i += gather_args(argc, argv, i + 1, &pargc, &pargv);
			ret = pam_sm_authenticate(pamh, 0, pargc, pargv);
			free_args(&pargc, &pargv);
			printf("authenticate: %d%s %s\n", ret,
			       ret ? ":" : "",
			       ret ? pam_strerror(pamh, ret) : "");
			continue;
		}
		if (strcmp(argv[i], "--run") == 0) {
			envlist = pam_getenvlist(pamh);
			if (envlist != NULL) {
				while (*envlist != NULL) {
					putenv(*envlist);
					envlist++;
				}
			}
			ret = system(argv[i + 1]);
			printf("run(\"%s\"): %d%s %s\n", argv[i + 1],
			       WEXITSTATUS(ret),
			       WEXITSTATUS(ret) ? ":" : "",
			       WEXITSTATUS(ret) ?
			       strerror(WEXITSTATUS(ret)) :
			       "");
			i++;
			continue;
		}
		if (strcmp(argv[i], "--open-session") == 0) {
			i += gather_args(argc, argv, i + 1, &pargc, &pargv);
			ret = pam_sm_open_session(pamh, 0, pargc, pargv);
			free_args(&pargc, &pargv);
			printf("open session: %d%s %s\n", ret,
			       ret ? ":" : "",
			       ret ? pam_strerror(pamh, ret) : "");
			continue;
		}
		if (strcmp(argv[i], "--setcred-establish") == 0) {
			i += gather_args(argc, argv, i + 1, &pargc, &pargv);
			ret = pam_sm_setcred(pamh, PAM_ESTABLISH_CRED,
					     pargc, pargv);
			free_args(&pargc, &pargv);
			printf("setcred: %d%s %s\n", ret,
			       ret ? ":" : "",
			       ret ? pam_strerror(pamh, ret) : "");
			continue;
		}
		if (strcmp(argv[i], "--setcred-reinitialize") == 0) {
			i += gather_args(argc, argv, i + 1, &pargc, &pargv);
			ret = pam_sm_setcred(pamh, PAM_REINITIALIZE_CRED,
					     pargc, pargv);
			free_args(&pargc, &pargv);
			printf("setcred: %d%s %s\n", ret,
			       ret ? ":" : "",
			       ret ? pam_strerror(pamh, ret) : "");
			continue;
		}
		if (strcmp(argv[i], "--setcred-delete") == 0) {
			i += gather_args(argc, argv, i + 1, &pargc, &pargv);
			ret = pam_sm_setcred(pamh, PAM_DELETE_CRED,
					     pargc, pargv);
			free_args(&pargc, &pargv);
			printf("setcred: %d%s %s\n", ret,
			       ret ? ":" : "",
			       ret ? pam_strerror(pamh, ret) : "");
			continue;
		}
		if (strcmp(argv[i], "--close-session") == 0) {
			i += gather_args(argc, argv, i + 1, &pargc, &pargv);
			ret = pam_sm_close_session(pamh, 0, pargc, pargv);
			free_args(&pargc, &pargv);
			printf("close session: %d%s %s\n", ret,
			       ret ? ":" : "",
			       ret ? pam_strerror(pamh, ret) : "");
			continue;
		}
		if (strcmp(argv[i], "--acct-mgmt") == 0) {
			i += gather_args(argc, argv, i + 1, &pargc, &pargv);
			ret = pam_sm_acct_mgmt(pamh, 0, pargc, pargv);
			free_args(&pargc, &pargv);
			printf("acct mgmt: %d%s %s\n", ret,
			       ret ? ":" : "",
			       ret ? pam_strerror(pamh, ret) : "");
			continue;
		}
		if (strcmp(argv[i], "--chauthtok-prelim") == 0) {
			i += gather_args(argc, argv, i + 1, &pargc, &pargv);
			ret = pam_sm_chauthtok(pamh, PAM_PRELIM_CHECK,
					       pargc, pargv);
			free_args(&pargc, &pargv);
			printf("chauthtok-prelim: %d%s %s\n", ret,
			       ret ? ":" : "",
			       ret ? pam_strerror(pamh, ret) : "");
			continue;
		}
		if (strcmp(argv[i], "--chauthtok-update") == 0) {
			i += gather_args(argc, argv, i + 1, &pargc, &pargv);
			ret = pam_sm_chauthtok(pamh, PAM_UPDATE_AUTHTOK,
					       pargc, pargv);
			free_args(&pargc, &pargv);
			printf("chauthtok-update: %d%s %s\n", ret,
			       ret ? ":" : "",
			       ret ? pam_strerror(pamh, ret) : "");
			continue;
		}
		fprintf(stderr, "Unrecognized argument: %s\n", argv[i]);
		break;
	}
	if (pamh != NULL) {
#ifdef __LINUX_PAM__
		/* Linux-PAM *actively* tries to break us. */
		((struct linux_pam_handle*)pamh)->caller = 2;
#endif
		ret = pam_end(pamh, 0);
		printf("end: %d\n", ret);
		pamh = NULL;
	}
	return ret;
}
