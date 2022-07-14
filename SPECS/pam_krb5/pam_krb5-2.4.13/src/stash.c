/*
 * Copyright 2003,2004,2005,2006,2007,2009,2011,2012,2013 Red Hat, Inc.
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

#include "cchelper.h"
#include "init.h"
#include "log.h"
#include "shmem.h"
#include "stash.h"
#include "userinfo.h"
#include "v5.h"
#include "xstr.h"

#define PAM_KRB5_STASH_TEMPLATE			"_pam_krb5_stash_%s_%s_%s_%d"
#define PAM_KRB5_STASH_TEMPLATE_SHM_SUFFIX	"_shm"

static void
_pam_krb5_stash_name_with_suffix(struct _pam_krb5_options *options,
				 const char *user, const char *suffix,
				 char **name)
{
	int i;
	*name = malloc(strlen(PAM_KRB5_STASH_TEMPLATE) +
		       strlen(user) + strlen(options->realm) +
		       (options->mappings_s ? strlen(options->mappings_s) : 0) +
		       3 +
		       (suffix ? strlen(suffix) : 0) +
		       1);
	if (*name != NULL) {
		sprintf(*name, PAM_KRB5_STASH_TEMPLATE "%s",
			user, options->realm,
		        options->mappings_s ? options->mappings_s : NULL,
			options->user_check,
			suffix ? suffix : "");
		for (i = 0; (*name)[i] != '\0'; i++) {
			if (strchr("= ", (*name)[i]) != NULL) {
				(*name)[i] = '_';
			}
		}
	}
}

void
_pam_krb5_stash_name(struct _pam_krb5_options *options,
		     const char *user, char **name)
{
	return _pam_krb5_stash_name_with_suffix(options, user, NULL, name);
}

void
_pam_krb5_stash_shm_var_name(struct _pam_krb5_options *options,
			     const char *user, char **name)
{
	return _pam_krb5_stash_name_with_suffix(options, user,
						PAM_KRB5_STASH_TEMPLATE_SHM_SUFFIX,
						name);
}

static int
_pam_krb5_get_data_stash(pam_handle_t *pamh, const char *key,
			 struct _pam_krb5_stash **stash)
{
	return pam_get_data(pamh, key, (PAM_KRB5_MAYBE_CONST void**) stash);
}

/* Clean up a stash.  This includes freeing any dynamically-allocated bits and
 * then freeing the stash itself. */
static void
_pam_krb5_stash_cleanup(pam_handle_t *pamh, void *data, int error)
{
	struct _pam_krb5_stash *stash = data;
	struct _pam_krb5_ccname_list *node;
	if (stash->v5armorccache != NULL) {
		krb5_cc_destroy(stash->v5ctx, stash->v5armorccache);
	};
	if (stash->v5ccache != NULL) {
		krb5_cc_destroy(stash->v5ctx, stash->v5ccache);
	}
	free(stash->key);
	while (stash->v5ccnames != NULL) {
		if (stash->v5ccnames->name != NULL) {
			xstrfree(stash->v5ccnames->name);
		}
		node = stash->v5ccnames;
		stash->v5ccnames = node->next;
		free(node);
	}
	krb5_free_context(stash->v5ctx);
	memset(stash, 0, sizeof(struct _pam_krb5_stash));
	free(stash);
}

/* Read state from the shared memory blob. */
static void
_pam_krb5_stash_shm_read_v5(pam_handle_t *pamh, struct _pam_krb5_stash *stash,
			    struct _pam_krb5_options *options,
			    const char *location, int key,
			    void *blob, size_t blob_size)
{
	char tktfile[PATH_MAX + 6], envstr[PATH_MAX];
	unsigned char *blob_creds;
	ssize_t blob_creds_size;
	int fd;
	krb5_ccache ccache;

	/* Sanity checks. */
	if (blob_size < sizeof(int) * 3) {
		warn("saved creds too small: %d bytes, need at least %d bytes",
		     (int) blob_size, (int) (sizeof(int) * 3));
		return;
	}
	blob_creds = blob;
	blob_creds += sizeof(int) * 4;
	blob_creds_size = ((int*)blob)[0];
	if (blob_creds_size + sizeof(int) * 4 > blob_size) {
		warn("saved creds too small: %d bytes, need %d bytes",
		     (int) blob_size,
		     (int) (blob_creds_size + sizeof(int) * 3));
		return;
	}

	/* Create a temporary ccache file. */
	snprintf(tktfile, sizeof(tktfile),
		 "FILE:%s/pam_krb5_tmp_XXXXXX", options->ccache_dir);
	fd = mkstemp(tktfile + 5);
	if (fd == -1) {
		warn("error creating temporary file \"%s\": %s",
		     tktfile + 5, strerror(errno));
		return;
	}

	/* Store the blob's contents in the file. */
	if (_pam_krb5_write_with_retry(fd,
				       blob_creds,
				       blob_creds_size) != blob_creds_size) {
		warn("error writing temporary file \"%s\": %s",
		     tktfile + 5, strerror(errno));
		unlink(tktfile + 5);
		close(fd);
		return;
	}

	/* Read the credentials from the file. */
	if (krb5_cc_resolve(stash->v5ctx, tktfile, &ccache) != 0) {
		warn("error creating ccache in \"%s\"", tktfile + 5);
		unlink(tktfile + 5);
		close(fd);
		return;
	}

	/* If we have an error reading the credential, there's nothing we can
	 * do at this point to recover from it. */
	if (v5_cc_copy(stash->v5ctx, options->realm,
		       ccache, &stash->v5ccache) == 0) {
		/* Read other variables. */
		stash->v5attempted = ((int*)blob)[1];
		stash->v5result = ((int*)blob)[2];
		stash->v5external = ((int*)blob)[3];
		if (options->debug) {
			debug("recovered credentials from shared memory "
			      "segment %d", key);
		}
		if (options->test_environment) {
			/* Store this here so that we can check for it
			 * in a self-test. */
			snprintf(envstr, sizeof(envstr),
				 PACKAGE "_read_shm_segment=%s", location);
			pam_putenv(pamh, envstr);
		}
	}

	/* Clean up. */
	krb5_cc_destroy(stash->v5ctx, ccache);
	close(fd);
}

/* Save state to the shared memory segment. */
static void
_pam_krb5_stash_shm_write_v5(pam_handle_t *pamh, struct _pam_krb5_stash *stash,
			     struct _pam_krb5_options *options,
			     const char *user,
			     struct _pam_krb5_user_info *userinfo)
{
	char variable[PATH_MAX + 6], *segname, envstr[PATH_MAX];
	void *blob;
	int *intblob;
	size_t blob_size;
	int fd, key;
	krb5_ccache ccache;

	/* Sanity check. */
	if ((stash->v5attempted == 0) || (stash->v5result != 0)) {
		return;
	}

	/* Create a temporary ccache file. */
	snprintf(variable, sizeof(variable),
		 "FILE:%s/pam_krb5_tmp_XXXXXX", options->ccache_dir);
	fd = mkstemp(variable + 5);
	if (fd == -1) {
		warn("error creating temporary ccache file \"%s\"",
		     variable + 5);
		return;
	}

	/* Write the credentials to that file. */
	if (krb5_cc_resolve(stash->v5ctx, variable, &ccache) != 0) {
		warn("error opening credential cache file \"%s\" for writing",
		     variable + 5);
		unlink(variable + 5);
		close(fd);
		return;
	}
	if (v5_cc_copy(stash->v5ctx, options->realm,
		       stash->v5ccache, &ccache) != 0) {
		warn("error writing to credential cache file \"%s\"",
		     variable + 5);
		krb5_cc_close(stash->v5ctx, ccache);
		unlink(variable + 5);
		close(fd);
		return;
	}

	/* Read the entire file. */
	key = _pam_krb5_shm_new_from_file(pamh, sizeof(int) * 4,
					  variable + 5, &blob_size, &blob,
					  options->debug);
	if ((key != -1) && (blob != NULL)) {
		intblob = blob;
		intblob[0] = blob_size;
		intblob[1] = stash->v5attempted;
		intblob[2] = stash->v5result;
		intblob[3] = stash->v5external;
	}
	if (blob != NULL) {
		blob = _pam_krb5_shm_detach(blob);
	}

	/* Clean up. */
	krb5_cc_destroy(stash->v5ctx, ccache);
	close(fd);

	if (key != -1) {
		segname = NULL;
		_pam_krb5_stash_shm_var_name(options, user, &segname);
		if (segname != NULL) {
			snprintf(variable, sizeof(variable),
				 "%s=%d/%ld",
				 segname, key, (long) getpid());
			free(segname);
			pam_putenv(pamh, variable);
			if (options->debug) {
				debug("saved credentials to shared memory "
				      "segment %d (creator pid %ld)", key,
				      (long) getpid());
				debug("set '%s' in environment", variable);
			}
			if (options->test_environment) {
				/* Store this here so that we can check for it
				 * in a self-test. */
				snprintf(envstr, sizeof(envstr),
					 PACKAGE "_write_shm_segment%s",
					 variable + strcspn(variable, "="));
				pam_putenv(pamh, envstr);
			}
			stash->v5shm = key;
			stash->v5shm_owner = getpid();
		}
	} else {
		warn("error saving credential state to shared "
		     "memory segment");
	}
}

/* Retrieve credentials from the shared memory segments named by the PAM
 * environment variables which begin with partial_key. */
void
_pam_krb5_stash_shm_read(pam_handle_t *pamh, const char *partial_key,
			 struct _pam_krb5_stash *stash,
			 struct _pam_krb5_options *options,
			 const char *user,
			 struct _pam_krb5_user_info *userinfo)
{
	int key;
	pid_t owner;
	long l;
	char *variable, *p, *q;
	const char *value;
	void *blob;
	size_t blob_size;

	/* Construct the name of a variable. */
	_pam_krb5_stash_shm_var_name(options, user, &variable);
	if (variable == NULL) {
		return;
	}

	/* Read the variable and extract a shared memory identifier. */
	value = pam_getenv(pamh, variable);
	key = -1;
	owner = -1;
	if (value != NULL) {
		l = strtol(value, &p, 0);
		if ((p != NULL) && (*p == '/')) {
			if ((l < INT_MAX) && (l > INT_MIN)) {
				key = l;
			}
			q = NULL;
			l = strtol(p + 1, &q, 0);
			if ((q != NULL) && (*q == '\0') && (q > p + 1)) {
				owner = l;
			}
		}
		if ((key != -1) && (owner != -1)) {
			if (options->debug) {
				debug("found shm segment %d owned by UID %lu",
				      key, (unsigned long) owner);
			}
		} else {
			warn("error parsing \"%s\"=\"%s\" for "
			     "segment ID and owner", variable, value);
		}
	} else {
		if (options->debug) {
			debug("no value for \"%s\" set, no credentials "
			      "recovered from shared memory", variable);
		}
	}

	/* Get a copy of the contents of the shared memory segment. */
	if ((stash->v5shm == -1) && (owner != -1)) {
		stash->v5shm = key;
		stash->v5shm_owner = owner;
	}
	if (key != -1) {
		_pam_krb5_blob_from_shm(key, &blob, &blob_size);
		if ((blob == NULL) || (blob_size == 0)) {
			warn("no segment with specified identifier %d", key);
		} else {
			/* Pull credentials from the blob, which contains a
			 * ccache file.  Cross our fingers and hope it's
			 * useful. */
			_pam_krb5_stash_shm_read_v5(pamh, stash,
						    options, value, key,
						    blob, blob_size);
			free(blob);
		}
	}

	free(variable);
}

/* Store credentials in new shared memory segments and set PAM environment
 * variables to their identifiers. */
void
_pam_krb5_stash_shm_write(pam_handle_t *pamh, struct _pam_krb5_stash *stash,
			  struct _pam_krb5_options *options,
			  const char *user,
			  struct _pam_krb5_user_info *userinfo)
{
	_pam_krb5_stash_shm_write_v5(pamh, stash, options, user, userinfo);
}

/* Check for KRB5CCNAME in the PAM environment.  If it's set, incorporate
 * contents of the named ccache into the stash. */
static void
_pam_krb5_stash_external_read(pam_handle_t *pamh, struct _pam_krb5_stash *stash,
			      const char *user,
			      struct _pam_krb5_user_info *userinfo,
			      struct _pam_krb5_options *options)
{
	krb5_ccache ccache;
	krb5_principal princ;
	int i, read_default_principal;
	const char *ccname;
	char *unparsed, envstr[PATH_MAX];

	/* Read a TGT from $KRB5CCNAME. */
	if (options->debug) {
		debug("checking for externally-obtained credentials");
	}
	ccname = pam_getenv(pamh, "KRB5CCNAME");
	if ((ccname != NULL) && (strlen(ccname) > 0)) {
		if (options->debug) {
			debug("KRB5CCNAME is set to \"%s\"", ccname);
		}
		ccache = NULL;
		read_default_principal = 0;
		i = krb5_cc_resolve(stash->v5ctx, ccname, &ccache);
		if (i != 0) {
			warn("error opening ccache \"%s\", ignoring", ccname);
		} else {
			princ = NULL;
			/* Read the name of the default principal from the
			 * ccache. */
			if (krb5_cc_get_principal(stash->v5ctx, ccache, &princ) != 0) {
				warn("error reading ccache's default principal "
				     "name from \"%s\", not reading "
				     "externally-provided creds", ccname);
			} else {
				read_default_principal++;
				/* If they're different, update the userinfo
				 * structure with the new principal name. */
				if (krb5_principal_compare(stash->v5ctx, princ,
							   userinfo->principal_name)) {
					if (options->debug) {
						debug("ccache matches current principal");
					}
					krb5_free_principal(stash->v5ctx, princ);
					princ = NULL;
				} else {
					if (options->debug) {
						debug("ccache is for a new or different principal, updating");
					}
					/* Unparse the name. */
					unparsed = NULL;
					if (krb5_unparse_name(stash->v5ctx, princ, &unparsed) != 0) {
						warn("error unparsing ccache's default principal name, discarding");
						krb5_free_principal(stash->v5ctx, princ);
						princ = NULL;
					} else {
						if (options->debug) {
							debug("updated user principal from '%s' to '%s'",
							      userinfo->unparsed_name,
							      unparsed);
						}
						/* Save the unparsed name. */
						v5_free_unparsed_name(stash->v5ctx, userinfo->unparsed_name);
						userinfo->unparsed_name = unparsed;
						unparsed = NULL;
						/* Save the principal name. */
						krb5_free_principal(stash->v5ctx, userinfo->principal_name);
						userinfo->principal_name = princ;
						princ = NULL;
					}
				}
			}
			/* If we were able to read the default principal, then
			 * copy the ccache's contents. */
			if (read_default_principal) {
				i = v5_cc_copy(stash->v5ctx, options->realm,
					       ccache, &stash->v5ccache);
				if (i != 0) {
					if (options->debug) {
						debug("failed to copy "
						      "credentials from \"%s\" "
						      "for \"%s\"",
						      ccname,
						      userinfo->unparsed_name);
					}
				} else {
					stash->v5attempted = 1;
					stash->v5result = 0;
					stash->v5external = 1;
					if (options->debug) {
						debug("copied credentials from "
						      "\"%s\" for \"%s\"",
						      ccname,
						      userinfo->unparsed_name);
					}
					if (options->test_environment) {
						/* Store this here so that we
						 * can check for it in a
						 * self-test. */
						snprintf(envstr,
							 sizeof(envstr),
							 PACKAGE
							 "_external_ccache=%s",
							 ccname);
						pam_putenv(pamh, envstr);
					}
				}
			}
			krb5_cc_close(stash->v5ctx, ccache);
		}
	} else {
		if (options->debug) {
			debug("KRB5CCNAME is not set, none found");
		}
	}
}

/* Get the stash of lookaside data we keep about this user.  If we don't
 * already have one, we need to create it.  We use a data name which includes
 * the principal name to allow checks within multiple realms to work, and we
 * store the key in the stash because older versions of libpam stored the
 * pointer instead of making their own copy of the key, which could lead to
 * crashes if we then deallocated the string. */
struct _pam_krb5_stash *
_pam_krb5_stash_get(pam_handle_t *pamh, const char *user,
		    struct _pam_krb5_user_info *info,
		    struct _pam_krb5_options *options)
{
	krb5_context ctx;
	struct _pam_krb5_stash *stash;
	char *key;

	/* Check for a previously-created stash. */
	key = NULL;
	stash = NULL;
	_pam_krb5_stash_name(options, user, &key);
	if ((key != NULL) &&
	    (_pam_krb5_get_data_stash(pamh, key, &stash) == PAM_SUCCESS) &&
	    (stash != NULL)) {
		free(key);
		if ((options->external == 1) && (stash->v5attempted == 0)) {
			_pam_krb5_stash_external_read(pamh, stash,
						      user, info, options);
		}
		return stash;
	}

	/* Build a new one. */
	if (_pam_krb5_init_ctx(&ctx, options->argc,
			       options->argv) != PAM_SUCCESS) {
		warn("error initializing kerberos");
		return NULL;
	}
#ifdef HAVE_KRB5_SET_TRACE_CALLBACK
	if (options->trace) {
		krb5_set_trace_callback(ctx, &trace, NULL);
	}
#endif

	stash = malloc(sizeof(struct _pam_krb5_stash));
	if (stash == NULL) {
		free(key);
		_pam_krb5_free_ctx(ctx);
		return NULL;
	}
	memset(stash, 0, sizeof(struct _pam_krb5_stash));

	stash->key = key;
	stash->v5ctx = ctx;
	stash->v5attempted = 0;
	stash->v5result = KRB5KRB_ERR_GENERIC;
	stash->v5expired = 0;
	stash->v5external = 0;
	stash->v5ccnames = NULL;
	stash->v5setenv = 0;
	stash->v5shm = -1;
	stash->v5shm_owner = -1;
	stash->v5ccache = NULL;
	stash->v5armorccache = NULL;
	stash->afspag = 0;
	if (options->use_shmem) {
		_pam_krb5_stash_shm_read(pamh, key, stash, options, user, info);
	}
	if (options->external &&
	    ((stash->v5attempted == 0) ||
	     ((stash->v5external == 1) && (stash->v5result == 0)))) {
		_pam_krb5_stash_external_read(pamh, stash, user, info, options);
	}
	pam_set_data(pamh, key, stash, _pam_krb5_stash_cleanup);

	return stash;
}

void
_pam_krb5_stash_push(krb5_context ctx,
		     struct _pam_krb5_stash *stash,
		     struct _pam_krb5_options *options,
		     const char *ccname_template,
		     int preserve_existing_ccaches,
		     const char *user,
		     struct _pam_krb5_user_info *userinfo,
		     uid_t uid, gid_t gid)
{
	char *newname;
	struct _pam_krb5_ccname_list *node;

	/* Allocate space in the list of ccaches.  Do it now while an error is
	 * a simple matter. */
	node = malloc(sizeof(*node));
	if (node == NULL) {
		return;
	}
	newname = NULL;
	if (_pam_krb5_cchelper_create(ctx, stash, options,
				      ccname_template, user, userinfo,
				      uid, gid, &newname) == 0) {
		/* If we're not doing multiple ccaches, chuck the others we've
		 * previously created. */
		if ((options->multiple_ccaches == 0) &&
		    (preserve_existing_ccaches == 0)) {
			struct _pam_krb5_ccname_list *list = stash->v5ccnames;
			while (list != NULL) {
				_pam_krb5_stash_pop(ctx, stash, options);
				if (list == stash->v5ccnames) {
					/* if we fail here, don't loop */
					break;
				}
				list = stash->v5ccnames;
			}
		}
		/* Save the name of this ccache. */
		node->name = newname;
		node->next = stash->v5ccnames;
		node->session_specific =
			(strstr(ccname_template, "XXXXXX") != NULL);
		stash->v5ccnames = node;
	} else {
		/* Log an error. */
		warn("error creating ccache for user \"%s\"", user);
		free(node);
	}
}

int
_pam_krb5_stash_pop(krb5_context ctx,
		    struct _pam_krb5_stash *stash,
		    struct _pam_krb5_options *options)
{
	struct _pam_krb5_ccname_list *node, **list = &stash->v5ccnames;

	if (*list != NULL) {
		node = *list;
		if (node->session_specific) {
			if (_pam_krb5_cchelper_destroy(ctx, stash, options,
						       node->name) != 0) {
				warn("error destroying ccache \"%s\"",
				     node->name);
				return -1;
			}
		} else {
			if (options->debug) {
				if (((node->next == NULL) ||
				     (node->next->name == NULL) ||
				     (strcmp(node->name,
					      node->next->name) != 0))) {
					debug("leaving ccache \"%s\" to "
					      "potentially linger", node->name);
				}
			}
		}
		xstrfree(node->name);
		node->name = NULL;
		*list = node->next;
		free(node);
		return 0;
	} else {
		return 0;
	}
}
