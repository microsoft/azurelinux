/*
 * Copyright 2001,2002,2003,2012 Red Hat, Inc.
 *
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Library General Public
 * License as published by the Free Software Foundation; either
 * version 2 of the License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * Library General Public License for more details.
 *
 * You should have received a copy of the GNU Library General Public
 * License along with this program; if not, write to the Free
 * Software Foundation, Inc., 59 Temple Place - Suite 330, Boston,
 * MA 02111-1307, USA
 *
 */

#ifndef HAVE_CONFIG_H
#include "../../config.h"
#endif

#include <sys/stat.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <dlfcn.h>
#include <errno.h>
#include <grp.h>
#include <limits.h>
#include <pwd.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <security/pam_appl.h>
#include <security/pam_modules.h>

/* Copy the PAM environment into the main environment. */
static void
pull_pam_environment(pam_handle_t *pamh)
{
	char **env = pam_getenvlist(pamh);
	int i;
	for (i = 0; env && env[i]; i++) {
		putenv(env[i]);
	}
}

/* A conversation function which uses static strings to supply modules with
 * responses. */
static int
converse(int num_msgs,
	 const struct pam_message **msg,
	 struct pam_response **resp,
	 void *appdata_ptr)
{
	char **argv = appdata_ptr;
	static int used = 0;
	int i;
	if (appdata_ptr == NULL) {
		return PAM_CONV_ERR;
	}
	*resp = malloc(sizeof(struct pam_response) * num_msgs);
	for (i = 0; i < num_msgs; i++) {
		memset(&((*resp)[i]), 0, sizeof(struct pam_response));
		switch (msg[i]->msg_style) {
		case PAM_PROMPT_ECHO_ON:
		case PAM_PROMPT_ECHO_OFF:
			if ((argv != NULL) && (argv[used] != NULL)) {
				(*resp)[i].resp = strdup(argv[used++]);
			} else {
#ifdef BROKENAPP
				(*resp)[i].resp = NULL;
#else
				(*resp)[i].resp = strdup("");
#endif
			}
			(*resp)[i].resp_retcode = PAM_SUCCESS;
			printf("`%s' -> `%s'\n", msg[i]->msg,
			       (*resp)[i].resp ?: "");
			fflush(NULL);
			break;
		case PAM_ERROR_MSG:
		case PAM_TEXT_INFO:
			(*resp)[i].resp_retcode = PAM_SUCCESS;
			printf("`%s'\n", msg[i]->msg);
			fflush(NULL);
			break;
		default:
			fprintf(stderr, "Unknown message type "
				"(shouldn't happen)!\n");
			fflush(NULL);
			exit(255);
		}
	}
	return PAM_SUCCESS;
}

#define call_fn(name,tag,flags) do { \
	fn = dlsym(dlhandle, name); \
	if (fn == NULL) { \
		printf("Error locating symbol `%s': %s.\n", name, dlerror()); \
		fflush(NULL); \
		return 255; \
	} \
	ret = fn(pamh, flags, argcount, &argv[args]); \
	printf(tag"\t%d\t%s\n", ret, pam_strerror(pamh, ret)); \
	fflush(NULL); } while (0)
#define call_stack(fn,tag,flags) do { \
	ret = fn(pamh, flags); \
	printf(tag"\t%d\t%s\n", ret, pam_strerror(pamh, ret)); \
	fflush(NULL); } while (0)

int
main(int argc, char **argv)
{
	void *dlhandle;
	int doauth, doaccount, dosession, dosetcred, dochauthtok, doprompt;
	int dofork, dorefresh;
	int noreentrancy;
	int i, ret, responses, args, argcount;
	const char *user, *module, *envvar;
	pam_handle_t *pamh;
	struct pam_partial_handle {
		char *authtok;
		unsigned caller;
	} *partial = NULL;
	struct pam_conv conv;
	char *tty, *ruser, *rhost, *authtok, *oldauthtok, *run, *prompt;

	struct passwd *pwd;
	uid_t pw_uid;
	struct group *grp;
	gid_t pw_gid, gr_gid;

	if (argc < 4) {
		printf("Usage: %s\n"
		       "       [-auth | -account | -session | -setcred | "
		       "-chauthtok | -refreshcred ]\n"
		       "       [-tty tty] [-ruser ruser] [-rhost rhost] "
		       "[-authtok tok] [-oldauthtok tok]\n"
		       "       [-setenv VAR=VAL]\n"
		       "       [-prompt string] [-showprompt] [-run command] "
		       "[-noreentrancy] [-fork]\n"
		       "       user [module [arg ...]| stack] "
		       "[-- response ...]\n",
		       strchr(argv[0], '/') ?
		       strrchr(argv[0], '/') + 1 :
		       argv[0]);
		return 255;
	}

	user = module = NULL;
	doauth = doaccount = dosession = dosetcred = dochauthtok = doprompt = 0;
	dofork = dorefresh = 0;
	noreentrancy = 0;
	args = argcount = responses = 0;
	tty = ruser = rhost = authtok = oldauthtok = run = prompt = NULL;
	envvar = NULL;
	for (i = 1; i < argc; i++) {
		if (strcmp(argv[i], "-auth") == 0) {
			doauth++;
			continue;
		}
		if (strcmp(argv[i], "-account") == 0) {
			doaccount++;
			continue;
		}
		if (strcmp(argv[i], "-session") == 0) {
			dosession++;
			continue;
		}
		if (strcmp(argv[i], "-setcred") == 0) {
			dosetcred++;
			continue;
		}
		if (strcmp(argv[i], "-refreshcred") == 0) {
			dorefresh++;
			continue;
		}
		if (strcmp(argv[i], "-chauthtok") == 0) {
			dochauthtok++;
			continue;
		}
		if (strcmp(argv[i], "-showprompt") == 0) {
			doprompt++;
			continue;
		}
		if (strcmp(argv[i], "-noreentrancy") == 0) {
			noreentrancy++;
			continue;
		}
		if (strcmp(argv[i], "-fork") == 0) {
			dofork++;
			continue;
		}
		if (strcmp(argv[i], "-tty") == 0) {
			tty = argv[++i];
			continue;
		}
		if (strcmp(argv[i], "-rhost") == 0) {
			rhost = argv[++i];
			continue;
		}
		if (strcmp(argv[i], "-authtok") == 0) {
			authtok = argv[++i];
			continue;
		}
		if (strcmp(argv[i], "-oldauthtok") == 0) {
			oldauthtok = argv[++i];
			continue;
		}
		if (strcmp(argv[i], "-run") == 0) {
			run = argv[++i];
			continue;
		}
		if (strcmp(argv[i], "-prompt") == 0) {
			prompt = argv[++i];
			continue;
		}
		if (strcmp(argv[i], "-ruser") == 0) {
			ruser = argv[++i];
			continue;
		}
		if (strcmp(argv[i], "-setenv") == 0) {
			envvar = argv[++i];
			continue;
		}
		if (user == NULL) {
			user = argv[i];
			continue;
		}
		if (module == NULL) {
			module = argv[i];
			continue;
		}
		if (strcmp(argv[i], "--") == 0) {
			if (responses == 0) responses = i + 1;
		}
		if (args == 0) {
			args = i;
		}
	}
	/* Find the beginning of the response list. */
	if (responses == 0) {
		responses = argc;
	}
	/* Count the number of non-response arguments we have. */
	if (args != 0) {
		argcount = 0;
		for (i = args;
		    (argv[i] != NULL) && (strcmp(argv[i], "--") != 0);
		    i++) {
			argcount++;
		}
	}

	/* Bail on invocation errors. */
	if ((user == NULL) || (module == NULL)) {
		printf("Not enough arguments.\n");
		return 255;
	}
	if ((doauth | doaccount | dosession | dosetcred | dorefresh | 
	     dochauthtok) == 0) {
		printf("No action requested.\n");
		return 255;
	}

	/* Set up the conversation structure to point to our conversation
	 * function and the list of responses we've gotten. */
	memset(&conv, 0, sizeof(conv));
	conv.conv = converse;
	conv.appdata_ptr = argv + responses;

	/* Check if the module screws with static buffers.  The docs say
	 * it's allowed, but I consider it bad practice, because there's
	 * no way we can fix all of the broken apps out there. */
	for (pw_uid = 1, pwd = NULL; pwd == NULL; pw_uid++) {
		if (pw_uid == 0) {
			fprintf(stderr, "No groups.\n");
			exit(255);
		}
		pwd = getpwuid(pw_uid);
	}
	for (gr_gid = 1, grp = NULL; grp == NULL; gr_gid++) {
		if (gr_gid == 0) {
			fprintf(stderr, "No groups.\n");
			exit(255);
		}
		grp = getgrgid(gr_gid);
	}
	pw_uid = pwd->pw_uid;
	pw_gid = pwd->pw_gid;
	gr_gid = grp->gr_gid;

	/* Hack: if the name of the "module" argument starts with "pam_",
	 * assume it's a module, and use "login" as the service name. */
	if ((strchr(module, '/') == NULL) &&
	    (strncmp(module, "pam_", 4) != 0)) {
		i = pam_start(module, user, &conv, &pamh);
		if (i != PAM_SUCCESS) {
			printf("Error initializing PAM for `%s'.\n", module);
			return 255;
		}
	} else {
		i = pam_start("login", user, &conv, &pamh);
		if (i != PAM_SUCCESS) {
			printf("Error initializing PAM for `%s'.\n", "login");
			return 255;
		}
	}

	/* Set ITEMs. */
	if (envvar) {
		i = pam_putenv(pamh, envvar);
		if (i != PAM_SUCCESS) {
			printf("Error setting PAM environment `%s'.\n", envvar);
			return 255;
		}
	}
	if (tty) {
		i = pam_set_item(pamh, PAM_TTY, tty);
		if (i != PAM_SUCCESS) {
			printf("Error setting TTY item `%s'.\n", tty);
			return 255;
		}
	}
	if (rhost) {
		i = pam_set_item(pamh, PAM_RHOST, rhost);
		if (i != PAM_SUCCESS) {
			printf("Error setting RHOST item `%s'.\n", rhost);
			return 255;
		}
	}
	if (ruser) {
		i = pam_set_item(pamh, PAM_RUSER, ruser);
		if (i != PAM_SUCCESS) {
			printf("Error setting RUSER item `%s'.\n", ruser);
			return 255;
		}
	}
	if (authtok) {
		/* Hackeroo.  Linux-PAM 0.75 and later don't like it when we
		 * do this sort of thing. */
		partial = (struct pam_partial_handle*)pamh;
		partial->caller = 1;

		i = pam_set_item(pamh, PAM_AUTHTOK, authtok);
		if (i != PAM_SUCCESS) {
			printf("Error setting AUTHTOK item `%s'.\n", authtok);
			return 255;
		}

		partial->caller = 0;
	}
	if (oldauthtok) {
		/* Hackeroo.  Linux-PAM 0.75 and later don't like it when we
		 * do this sort of thing. */
		partial = (struct pam_partial_handle*)pamh;
		partial->caller = 1;

		i = pam_set_item(pamh, PAM_OLDAUTHTOK, oldauthtok);
		if (i != PAM_SUCCESS) {
			printf("Error setting OLDAUTHTOK item `%s'.\n",
			       oldauthtok);
			return 255;
		}

		partial->caller = 0;
	}
	if (prompt) {
		i = pam_set_item(pamh, PAM_USER_PROMPT, prompt);
		if (i != PAM_SUCCESS) {
			printf("Error setting USER_PROMPT item `%s'.\n",
			       prompt);
			return 255;
		}
	}

	/* Hack: if the name of the "module" argument doesn't start with "pam_",
	 * assume it's the stack name, and run with it. */
	if ((strchr(module, '/') == NULL) &&
	    (strncmp(module, "pam_", 4) != 0)) {
		printf("Calling stack `%s'.\n", module);
		if (dofork) {
			int fds[2];
			pid_t pid;
			if (pipe(fds) == -1) {
				printf("Error creating pipe: %s\n",
				       strerror(errno));
				return 255;
			}
			if ((pid = fork()) == 0) {
				char **env;
				int i, j;
				if (doauth) {
					call_stack(pam_authenticate,
						   "AUTH", 0);
				}
				if (doprompt) {
					const void *prmpt;
					if (pam_get_item(pamh, PAM_USER_PROMPT,
							 &prmpt) ==
							 PAM_SUCCESS) {
						printf("Prompt = `%s'.\n",
						       (const char*)prmpt);
					} else {
						printf("Error reading "
						       "USER_PROMPT item.\n");
						return 255;
					}
				}
				if (doaccount) {
					call_stack(pam_acct_mgmt, "ACCT", 0);
				}
				close(fds[0]);
				env = pam_getenvlist(pamh);
				for (i = 0; env && env[i]; i++) {
					printf("Sending environment = `%s'.\n",
					       env[i]);
					j = write(fds[1], env[i],
						  strlen(env[i]));
					j = write(fds[1], "\n", 1);
					j++;
				}
				close(fds[1]);
				exit(0);
			} else {
				char buf[LINE_MAX];
				FILE *fp;
				close(fds[1]);
				fp = fdopen(fds[0], "r");
				while (fgets(buf, sizeof(buf), fp) != NULL) {
					buf[strcspn(buf, "\r\n")] = '\0';
					printf("Environment = `%s'.\n", buf);
					pam_putenv(pamh, strdup(buf));
				}
				fclose(fp);
				waitpid(pid, NULL, 0);
			}
		} else {
			if (doauth) {
				call_stack(pam_authenticate, "AUTH", 0);
			}
			if (doprompt) {
				const void *prmpt;
				if (pam_get_item(pamh, PAM_USER_PROMPT,
						 &prmpt) == PAM_SUCCESS) {
					printf("Prompt = `%s'.\n",
					       (const char*)prmpt);
				} else {
					printf("Error reading USER_PROMPT "
					       "item.\n");
					return 255;
				}
			}
			if (doaccount) {
				call_stack(pam_acct_mgmt, "ACCT", 0);
			}
		}
		if (dorefresh) {
			call_stack(pam_setcred, "REINITCRED",
				   PAM_REINITIALIZE_CRED);
		}
		if (dosetcred) {
			call_stack(pam_setcred, "ESTCRED", PAM_ESTABLISH_CRED);
		}
		if (dosession) {
			call_stack(pam_open_session, "OPENSESS", 0);
		}
		if (run) {
			pid_t pid;
			if ((pid = fork()) == 0) {
				pull_pam_environment(pamh);
				i = setregid(getegid(), getegid());
				i = setreuid(geteuid(), geteuid());
				execlp(run, run, NULL);
				_exit(0);
			} else {
				waitpid(pid, NULL, 0);
			}
		}
		if (dosession) {
			call_stack(pam_close_session, "CLOSESESS", 0);
		}
		if (dosetcred) {
			call_stack(pam_setcred, "DELCRED", PAM_DELETE_CRED);
		}
		if (dochauthtok) {
			call_stack(pam_chauthtok, "CHAUTHTOK", 0);
		}
	} else {
		/* Hack: if the name of the "module" argument starts with
		 * "pam_", assume it's a module name, open it, and run the
		 * function. */
		char path[PATH_MAX];
		struct stat st;
		int (*fn)(pam_handle_t *pamh, int flags, int argc, char **argv);
		if (strchr(module, '/') != NULL) {
			snprintf(path, sizeof(path), "%s", module);
		} else {
			snprintf(path, sizeof(path), "/lib/security/%s.so",
				 module);
		}
		dlhandle = dlopen(path, RTLD_NOW);
		if ((dlhandle == NULL) && (strchr(module, '/') == NULL)) {
			if (stat("/lib64/security", &st) == 0) {
				snprintf(path, sizeof(path),
					 "/lib64/security/%s.so", module);
				dlhandle = dlopen(path, RTLD_NOW);
			}
		}
		if (dlhandle == NULL) {
			printf("Error opening module: %s\n", dlerror());
			return 255;
		}
		printf("Calling module `%s'.\n", module);

		/* Hackeroo.  Linux-PAM 0.75 and later don't like it when we
		 * do this sort of thing. */
		partial = (struct pam_partial_handle*)pamh;
		partial->caller = 1;

		if (dofork) {
			int fds[2];
			pid_t pid;
			if (pipe(fds) == -1) {
				printf("Error creating pipe: %s\n",
				       strerror(errno));
				return 255;
			}
			if ((pid = fork()) == 0) {
				char **env;
				int i, j;
				if (doauth) {
					call_fn("pam_sm_authenticate",
						"AUTH", 0);
				}
				if (doprompt) {
					const void *prmpt;
					if (pam_get_item(pamh, PAM_USER_PROMPT,
							 &prmpt) ==
							 PAM_SUCCESS) {
						printf("Prompt = `%s'.\n",
						       (const char*)prmpt);
					} else {
						printf("Error reading "
						       "USER_PROMPT item.\n");
						return 255;
					}
				}
				if (doaccount) {
					call_fn("pam_sm_acct_mgmt", "ACCT", 0);
				}
				close(fds[0]);
				env = pam_getenvlist(pamh);
				for (i = 0; env && env[i]; i++) {
					printf("Sending environment = `%s'.\n",
					       env[i]);
					j = write(fds[1], env[i],
						  strlen(env[i]));
					j = write(fds[1], "\n", 1);
					j++;
				}
				close(fds[1]);
				exit(0);
			} else {
				char buf[LINE_MAX];
				FILE *fp;
				close(fds[1]);
				fp = fdopen(fds[0], "r");
				while (fgets(buf, sizeof(buf), fp) != NULL) {
					buf[strcspn(buf, "\r\n")] = '\0';
					printf("Environment = `%s'.\n", buf);
					pam_putenv(pamh, strdup(buf));
				}
				fclose(fp);
				waitpid(pid, NULL, 0);
			}
		} else {
			if (doauth) {
				call_fn("pam_sm_authenticate", "AUTH", 0);
			}
			if (doprompt) {
				const void *prmpt;
				if (pam_get_item(pamh, PAM_USER_PROMPT,
						 &prmpt) == 0) {
					printf("Prompt = `%s'.\n",
					       (const char*)prmpt);
				} else {
					printf("Error reading USER_PROMPT "
					       "item.\n");
					return 255;
				}
			}
			if (doaccount) {
				call_fn("pam_sm_acct_mgmt", "ACCT", 0);
			}
		}
		if (dochauthtok) {
			if (oldauthtok) {
				if (pam_set_item(pamh, PAM_AUTHTOK,
						 oldauthtok) != 0) {
					printf("Error setting AUTHTOK item.\n");
					return 255;
				}
			}
			call_fn("pam_sm_chauthtok", "CHAUTHTOK1",
				PAM_PRELIM_CHECK);
			if (oldauthtok) {
				if (pam_set_item(pamh, PAM_OLDAUTHTOK,
						 oldauthtok) != PAM_SUCCESS) {
					printf("Error setting OLDAUTHTOK "
					       "item.\n");
					return 255;
				}
			}
			if (authtok) {
				if (pam_set_item(pamh, PAM_AUTHTOK,
						 authtok) != PAM_SUCCESS) {
					printf("Error setting AUTHTOK "
					       "item.\n");
					return 255;
				}
			}
			call_fn("pam_sm_chauthtok", "CHAUTHTOK2",
				PAM_UPDATE_AUTHTOK);
		}
		if (dorefresh) {
			call_fn("pam_sm_setcred", "REINITCRED",
				PAM_REINITIALIZE_CRED);
		}
		if (dosetcred) {
			call_fn("pam_sm_setcred", "ESTCRED",
				PAM_ESTABLISH_CRED);
		}
		if (dosession) {
			call_fn("pam_sm_open_session", "OPENSESS", 0);
		}
		if (run) {
			pid_t pid;
			if ((pid = fork()) == 0) {
				pull_pam_environment(pamh);
				i = setregid(getegid(), getegid());
				i = setreuid(geteuid(), geteuid());
				execlp(run, run, NULL);
				_exit(0);
			} else {
				waitpid(pid, NULL, 0);
			}
		}
		if (dosession) {
			call_fn("pam_sm_close_session", "CLOSESESS", 0);
		}
		if (dosetcred) {
			call_fn("pam_sm_setcred", "DELCRED",
				PAM_DELETE_CRED);
		}
	}

	pam_end(pamh, PAM_SUCCESS);

	if (!noreentrancy) {
		/* Check if the buffer's been changed. */
		if ((pwd->pw_uid != pw_uid) || (pwd->pw_gid != pw_gid)) {
			printf("Module calls getpw functions (%s).\n",
			       pwd->pw_name);
			printf("UID before: %d, after: %d.\n",
			       pw_uid, pwd->pw_uid);
			printf("GID before: %d, after: %d.\n",
			       pw_gid, pwd->pw_gid);
		}
		if (grp->gr_gid != gr_gid) {
			printf("Module calls getgr functions (%s).\n",
			       grp->gr_name);
			printf("GID before: %d, after: %d.\n",
			       gr_gid, grp->gr_gid);
		}
	}

	return 0;
}
