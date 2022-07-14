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
#include <sys/ipc.h>
#include <sys/shm.h>
#include <sys/stat.h>
#include <errno.h>
#include <fcntl.h>
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
#include "log.h"
#include "shmem.h"
#include "stash.h"
#include "userinfo.h"
#include "xstr.h"

/* A record of a shared memory segment's key, and the name under which the
 * structure was saved by libpam. */
struct _pam_krb5_shm_rec {
	char *name;
	pid_t pid;
	int key;
	int debug;
};

/* Release a shared memory segment. */
void
_pam_krb5_shm_remove(pid_t pid, int key, int log_debug)
{
	struct shmid_ds ds;
	if (pid != -1) {
		if (shmctl(key, IPC_STAT, &ds) == 0) {
			if (ds.shm_cpid == pid) {
				if (log_debug) {
					debug("cleanup function removing "
					      "shared memory segment %d "
					      "belonging to process %ld", key,
					      (long) pid);
				}
				shmctl(key, IPC_RMID, NULL);
			} else {
				warn("shared memory segment %d belongs to a "
				     "process other than %ld (%ld), not "
				     "removing",
				     key, (long) pid, (long) ds.shm_cpid);
			}
		}
	} else {
		if (log_debug) {
			debug("cleanup function removing "
			      "shared memory segment %d", key);
		}
		shmctl(key, IPC_RMID, NULL);
	}
}

/* Clean up a shared memory segment and its record. */
static void
_pam_krb5_shm_cleanup(pam_handle_t *pamh, void *data, int status)
{
	struct _pam_krb5_shm_rec *rec;
	rec = data;
	_pam_krb5_shm_remove(rec->pid, rec->key, rec->debug);
	free(rec->name);
	free(rec);
}

/* Create a new shared memory segment, of at least the given size, which will
 * be cleaned up automatically by libpam.  If address is not NULL, attach to
 * the segment and return its address (which must be subsequently detached). */
int
_pam_krb5_shm_new(pam_handle_t *pamh, size_t size, void **address, int debug)
{
	int key;
	struct _pam_krb5_shm_rec *rec;

	/* In case of error, return NULL. */
	if (address != NULL) {
		*address = NULL;
	}

	/* Allocate space for the record-keeping structure. */
	rec = malloc(sizeof(struct _pam_krb5_shm_rec));
	if (rec == NULL) {
		return -1;
	}
	rec->name = malloc(strlen("_pam_krb5_shm_") + sizeof(key) * 8);
	if (rec->name == NULL) {
		free(rec);
		return -1;
	}
	rec->pid = getpid();
	rec->debug = debug;

	/* Handle minimum size requirements on shared memory segments. */
#ifdef SHMMIN
	if (size < SHMMIN) {
		size = SHMMIN;
	}
#endif

	/* Create the segment. */
	key = shmget(IPC_PRIVATE, size, IPC_CREAT | S_IRUSR | S_IWUSR);
	if (key != -1) {
		/* Get a local handle to the segment. */
		if (address != NULL) {
			*address = shmat(key, NULL, 0);
			if (*address == (void *) -1) {
				warn("failed to attach to shmem segment %d",
				     key);
				shmctl(key, IPC_RMID, NULL);
				key = -1;
			}
		}
		/* Save the segment. */
		if (key != -1) {
			sprintf(rec->name, "_pam_krb5_shm_%d", key);
			rec->key = key;
			pam_set_data(pamh, rec->name, rec,
				     _pam_krb5_shm_cleanup);
		}
	}

	if (key == -1) {
		free(rec->name);
		free(rec);
	}

	return key;
}

/* Create a new segment, copying the given source data into the segment at a
 * specified offset.  If address is given, attach to the segment and return the
 * address, which must be detached by the caller. */
int
_pam_krb5_shm_new_from_blob(pam_handle_t *pamh, size_t lead,
			    void *source, size_t size, void **address,
			    int debug)
{
	int key;
	void *block;
	block = NULL;
	/* Create the segment and attach to it here. */
	key = _pam_krb5_shm_new(pamh, size + lead, &block, debug);
	/* Copy in the caller's data. */
	if ((key != -1) && (block != (void *) -1)) {
		if (lead > 0) {
			memset((unsigned char*)block, 0, lead);
		}
		memmove(((unsigned char*)block) + lead, source, size);
	}
	/* Either detach from the memory or return its address to our caller. */
	if (address != NULL) {
		*address = block;
	} else {
		if (block != NULL) {
			block = _pam_krb5_shm_detach(block);
		}
	}
	return key;
}

/* Create a new segment, copying the contents of the given file into the
 * segment at a specified offset.  If address is given, attach to the segment
 * and return the address, which must be detached by the caller. */
int
_pam_krb5_shm_new_from_file(pam_handle_t *pamh, size_t lead,
			    const char *file, size_t *file_size, void **address,
			    int debug)
{
	int key, fd;
	struct stat st;
	unsigned char *p;
	void *block;

	/* Attempt to open the file for reading. */
	key = -1;
	if (address != NULL) {
		*address = NULL;
	}
	if (file_size != NULL) {
		*file_size = 0;
	}
	fd = open(file, O_RDONLY);
	if ((fd != -1) &&
	    (fstat(fd, &st) != -1) &&
	    (S_ISREG(st.st_mode)) &&
	    (st.st_size < 0x10000)) {
		/* Create a shared memory segment in which to store the file. */
		key = _pam_krb5_shm_new(pamh, st.st_size + lead, &block, debug);
		if ((key != -1) && (block != (void *) -1)) {
			p = block;
			if (lead > 0) {
				memset(p, 0, lead);
			}
			if (_pam_krb5_read_with_retry(fd, p + lead,
						      st.st_size) != st.st_size) {
				block = _pam_krb5_shm_detach(block);
				key = -1;
			}
			if (key != -1) {
				if (file_size != NULL) {
					*file_size = st.st_size;
				}
				if (address != NULL) {
					*address = block;
				} else {
					block = _pam_krb5_shm_detach(block);
				}
			}
		}
	}
	if (fd != -1) {
		close(fd);
	}

	return key;
}

/* Attach to a segment, returning the address where it was mapped, and the size
 * of the segment.  The caller will need to detach it. */
void *
_pam_krb5_shm_attach(int key, size_t *size)
{
	void *address;
	struct shmid_ds ds;

	if (size != NULL) {
		*size = 0;
	}
	address = shmat(key, NULL, 0);
	if (address == (void*) -1) {
		return NULL;
	}
	if (shmctl(key, IPC_STAT, &ds) == -1) {
		address = _pam_krb5_shm_detach(address);
		return NULL;
	}
	if (size != NULL) {
		*size = ds.shm_segsz;
	}
	return address;
}

/* Detach from a segment, returning NULL. */
void *
_pam_krb5_shm_detach(void *address)
{
	if ((address != NULL) && (address != (void*) -1)) {
		shmdt(address);
	}
	return NULL;
}

/* Copy the contents of a shared memory segment into a chunk of memory on the
 * heap, returning the allocated size. */
void
_pam_krb5_blob_from_shm(int key, void **block, size_t *block_size)
{
	void *address;
	struct shmid_ds ds;

	*block = NULL;
	*block_size = 0;

	/* Attach to the segment and make sure that "we" own it. */
	address = _pam_krb5_shm_attach(key, NULL);
	if (address != NULL) {
		if ((shmctl(key, IPC_STAT, &ds) == -1) ||
		    (ds.shm_segsz < 16)|| (ds.shm_segsz > 0xffff) ||
		    (ds.shm_perm.cuid != getuid()) ||
		    (ds.shm_perm.cuid != geteuid())) {
			address = _pam_krb5_shm_detach(address);
			if (block_size != NULL) {
				*block_size = 0;
			}
		}
		/* Make a copy of the memory. */
		if (address != NULL) {
			*block = malloc(ds.shm_segsz);
			if (*block != NULL) {
				memcpy(*block, address, ds.shm_segsz);
				*block_size = ds.shm_segsz;
			}
		}
		/* Detach from the segment if we haven't already. */
		address = _pam_krb5_shm_detach(address);
	}
}
