/*
 * Copyright 2004,2005,2006,2007,2008,2009,2010,2012,2014,2015,2016 Red Hat, Inc.
 * Copyright 2004 Kungliga Tekniska Högskolan
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

 /*
  * A miniature afslog implementation.  Requires cells served by OpenAFS 1.2.8
  * or later in combination with MIT Kerberos 1.2.6 or later.
  *
  * References:
  *   http://grand.central.org/numbers/pioctls.html
  *   http://www.afsig.se/afsig/space/rxgk-client-integration
  *   auth/afs_token.xg
  *   http://lists.openafs.org/pipermail/afs3-standardization/2013-July/002738.html
  */

#include "../config.h"

#include <sys/types.h>
#include <sys/ioctl.h>
#include <sys/syscall.h>
#ifdef HAVE_SYS_IOCCOM_H
#include <sys/ioccom.h>
#endif
#include <ctype.h>
#include <errno.h>
#include <fcntl.h>
#ifdef HAVE_INTTYPES_H
#include <inttypes.h>
#endif
#include <limits.h>
#include <netdb.h>
#include <signal.h>
#include <stdio.h>
#ifdef HAVE_STDINT_H
#include <stdint.h>
#endif
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

#include "init.h"
#include "log.h"
#include "minikafs.h"
#include "v5.h"
#include "xstr.h"

#ifndef KRB_TICKET_GRANTING_TICKET
#ifdef KRB5_TGS_NAME
#define KRB_TICKET_GRANTING_TICKET KRB5_TGS_NAME
#else
#define KRB_TICKET_GRANTING_TICKET "krbtgt"
#endif
#endif

#define HOSTNAME_SIZE NI_MAXHOST

#define OPENAFS_AFS_IOCTL_FILE  "/proc/fs/openafs/afs_ioctl"
#define ARLA_AFS_IOCTL_FILE     "/proc/fs/nnpfs/afs_ioctl"

#ifdef sun
#ifndef __NR_afs_syscall
#define __NR_afs_syscall 65
#endif
#endif

/* Global(!) containing the path to the file/device/whatever in /proc which we
 * can use to get the effect of the AFS syscall.  If we ever need to be
 * thread-safe, we'll have to lock around accesses to this. */
static const char *minikafs_procpath = NULL;

#define VIOCTL_SYSCALL ((unsigned int) _IOW('C', 1, void *))
#define VIOCTL_FN(id)  ((unsigned int) _IOW('V', (id), struct minikafs_ioblock))
#define CIOCTL_FN(id)  ((unsigned int) _IOW('C', (id), struct minikafs_ioblock))
#define OIOCTL_FN(id)  ((unsigned int) _IOW('O', (id), struct minikafs_ioblock))
#define AIOCTL_FN(id)  ((unsigned int) _IOW('A', (id), struct minikafs_ioblock))

/* A structure specifying parameters to the VIOCTL_SYSCALL ioctl.  An array
 * would do as well, but this makes the order of items clearer. */
struct minikafs_procdata {
	long param4;
	long param3;
	long param2;
	long param1;
	long function;
};

/* A structure specifying input/output buffers to pioctl functions. */
struct minikafs_ioblock {
	char *in, *out;
	uint16_t insize, outsize;
};

/* The portion of a token which includes our own key and other bookkeeping
 * stuff.  Along with a magic blob used by rxkad, the guts of rxkad tokens. */
struct minikafs_plain_token {
	uint32_t kvno;
	char key[8];
	uint32_t uid;
	uint32_t start, end; /* must be odd (?) */
};

/* Functions called through minikafs_syscall().  Might not port to your system. */
enum minikafs_subsys {
	minikafs_subsys_pioctl = 20,
	minikafs_subsys_setpag = 21,
};

/* Subfunctions called through minikafs_pioctl(). */
enum minikafs_pioctl_fn {
	minikafs_pioctl_bogus = VIOCTL_FN(0),
	minikafs_pioctl_settoken = VIOCTL_FN(3),
	minikafs_pioctl_flush = VIOCTL_FN(6),
	minikafs_pioctl_gettoken = VIOCTL_FN(8),
	minikafs_pioctl_unlog = VIOCTL_FN(9),
	minikafs_pioctl_whereis = VIOCTL_FN(14),
	minikafs_pioctl_unpag = VIOCTL_FN(21),
	minikafs_pioctl_getcelloffile = VIOCTL_FN(30),
	minikafs_pioctl_getwscell = VIOCTL_FN(31),
	minikafs_pioctl_gettoken2 = CIOCTL_FN(7),
	minikafs_pioctl_settoken2 = CIOCTL_FN(8),
	minikafs_pioctl_getprop = CIOCTL_FN(10),
	minikafs_pioctl_setprop = CIOCTL_FN(11),
};

/* Forward declarations. */
static int minikafs_5settoken2(const char *cell, krb5_creds *creds, int32_t id);

/* Call AFS using an ioctl. Might not port to your system. */
static int
minikafs_ioctlcall(long function, long arg1, long arg2, long arg3, long arg4)
{
	int fd, ret, saved_errno;
	struct minikafs_procdata data;
	fd = open(minikafs_procpath, O_RDWR);
	if (fd == -1) {
		errno = EINVAL;
		return -1;
	}
	data.function = function;
	data.param1 = arg1;
	data.param2 = arg2;
	data.param3 = arg3;
	data.param4 = arg4;
	ret = ioctl(fd, VIOCTL_SYSCALL, &data);
	saved_errno = errno;
	close(fd);
	errno = saved_errno;
	return ret;
}

/* Call the AFS syscall. Might not port to your system. */
static int
minikafs_syscall(long function, long arg1, long arg2, long arg3, long arg4)
{
#ifdef __NR_afs_syscall
	return syscall(__NR_afs_syscall, function, arg1, arg2, arg3, arg4);
#else
	errno = ENOSYS;
	return -1;
#endif
}

/* Call into AFS, somehow. */
static int
minikafs_call(long function, long arg1, long arg2, long arg3, long arg4)
{
	if (minikafs_procpath != NULL) {
		return minikafs_ioctlcall(function, arg1, arg2, arg3, arg4);
	}
	return minikafs_syscall(function, arg1, arg2, arg3, arg4);
}

/* Make an AFS pioctl. Might not port to your system. */
static int
minikafs_pioctl(char *file, enum minikafs_pioctl_fn subfunction,
		struct minikafs_ioblock *iob)
{
	return minikafs_call(minikafs_subsys_pioctl, (long) file,
			     subfunction, (long) iob, 0);
}

/* Determine in which cell a given file resides.  Returns 0 on success. */
int
minikafs_cell_of_file(const char *file, char *cell, size_t length)
{
	struct minikafs_ioblock iob;
	char *wfile;
	int i;

	wfile = xstrdup(file ? file : "/afs");

	memset(&iob, 0, sizeof(iob));
	iob.in = wfile;
	iob.insize = strlen(wfile) + 1;
	iob.out = cell;
	iob.outsize = length;

	i = minikafs_pioctl(wfile, minikafs_pioctl_getcelloffile, &iob);

	xstrfree(wfile);
	return i;
}

/* Do minikafs_cell_of_file, but if we can't find out, walk up the filesystem
 * tree until we either get an answer or hit the root directory. */
int
minikafs_cell_of_file_walk_up(const char *file, char *cell, size_t length)
{
	char *p, dir[PATH_MAX + 1];
	int i;

	snprintf(dir, sizeof(dir), "%s", file);
	do {
		memset(cell, '\0', length);
		i = minikafs_cell_of_file(dir, cell, length);
		if (i != 0) {
			p = strrchr(dir, '/');
			if (p != NULL) {
				*p = '\0';
			} else {
				strcpy(dir, "");
			}
		}
	} while ((i != 0) && (strlen(dir) > 0));
	return i;
}

/* Determine if AFS is running. Unlike most other functions, return 0 on
 * FAILURE. */
int
minikafs_has_afs(void)
{
	char cell[PATH_MAX];
	int fd, i, ret;
	struct sigaction news, olds;

	fd = -1;

#ifdef OPENAFS_AFS_IOCTL_FILE
	if (fd == -1) {
		fd = open(OPENAFS_AFS_IOCTL_FILE, O_RDWR);
		if (fd != -1) {
			minikafs_procpath = OPENAFS_AFS_IOCTL_FILE;
			close(fd);
			return 1;
		}
	}
#endif
#ifdef ARLA_AFS_IOCTL_FILE
	if (fd == -1) {
		fd = open(ARLA_AFS_IOCTL_FILE, O_RDWR);
		if (fd != -1) {
			minikafs_procpath = ARLA_AFS_IOCTL_FILE;
			close(fd);
			return 1;
		}
	}
#endif
	if (fd == -1) {
		return 0;
	}

	memset(&news, 0, sizeof(news));
	news.sa_handler = SIG_IGN;
	i = sigaction(SIGSYS, &news, &olds);
	if (i != 0) {
		return 0;
	}

	ret = 0;
	i = minikafs_cell_of_file(NULL, cell, sizeof(cell));
	if ((i == 0) || ((i == -1) && (errno != ENOSYS))) {
		ret = 1;
	}

	sigaction(SIGSYS, &olds, NULL);

	return ret;
}

/* Determine in which realm a cell exists.  We do this by obtaining the address
 * of the fileserver which holds /afs/cellname (assuming that the root.cell
 * volume from the cell is mounted there), converting the address to a host
 * name, and then asking libkrb5 to tell us to which realm the host belongs. */
static int
minikafs_realm_of_cell_with_ctx(krb5_context ctx,
				struct _pam_krb5_options *options,
				const char *cell,
				char *realm, size_t length)
{
	struct minikafs_ioblock iob;
	struct sockaddr_in sin;
	in_addr_t *address;
	krb5_context use_ctx;
	char *path, host[HOSTNAME_SIZE], **realms;
	int i, n_addresses, ret;

	if (cell) {
		path = malloc(strlen(cell) + 6);
	} else {
		path = malloc(5);
	}
	if (path == NULL) {
		return -1;
	}
	if (cell) {
		sprintf(path, "/afs/%s", cell);
	} else {
		sprintf(path, "/afs");
	}

	n_addresses = 16;
	do {
		/* allocate the output buffer for the address [list] */
		address = malloc(n_addresses * sizeof(address[0]));
		if (address == NULL) {
			ret = -1;
			break;
		}
		memset(address, 0, n_addresses * sizeof(address[0]));
		memset(&iob, 0, sizeof(iob));
		iob.in = path;
		iob.insize = strlen(path) + 1;
		iob.out = (char*) &address[0];
		iob.outsize = n_addresses * sizeof(address[0]);
		ret = minikafs_pioctl(path, minikafs_pioctl_whereis, &iob);
		/* if we failed, free the address [list], and if the error was
		 * E2BIG, increase the size we'll use next time, up to a
		 * hard-coded limit */
		if (ret != 0) {
			if (options->debug) {
				debug("error during whereis pioctl: %s",
				      strerror(errno));
			}
			free(address);
			address = NULL;
			if (errno == E2BIG) {
				if (n_addresses > 256) {
					if (options->debug) {
						debug("giving up");
					}
					break;
				}
				if (options->debug) {
					debug("retrying");
				}
				n_addresses *= 2;
			}
		}
	} while ((ret != 0) && (errno == E2BIG));

	if (ret != 0) {
		if (options->debug) {
			debug("got error %d (%s) determining file server for "
			      "\"%s\"", errno, v5_error_message(errno), path);
		}
		free(path);
		return ret;
	}
	free(path);

	sin.sin_family = AF_INET;
	if (options->debug) {
		for (i = 0; (i < n_addresses) && (address[i] != 0); i++) {
			debug("file server for \"/afs/%s\" is %u.%u.%u.%u",
			      cell,
			      (address[i] >>  0) & 0xff,
			      (address[i] >>  8) & 0xff,
			      (address[i] >> 16) & 0xff,
			      (address[i] >> 24) & 0xff);
		}
	}

	if (ctx == NULL) {
		if (_pam_krb5_init_ctx(&use_ctx, 0, NULL) != 0) {
			free(address);
			return -1;
		}
	} else {
		use_ctx = ctx;
	}

	for (i = 0; (i < n_addresses) && (address[i] != 0); i++) {
		memcpy(&sin.sin_addr, &address[i], sizeof(address[i]));
		if (getnameinfo((const struct sockaddr*) &sin, sizeof(sin),
				host, sizeof(host), NULL, 0,
				NI_NAMEREQD) == 0) {
			if (options->debug) {
				debug("file server %d.%d.%d.%d has name %s",
				      (address[i] >>  0) & 0xff,
				      (address[i] >>  8) & 0xff,
				      (address[i] >> 16) & 0xff,
				      (address[i] >> 24) & 0xff,
				      host);
			}
			if (krb5_get_host_realm(use_ctx, host, &realms) == 0) {
				strncpy(realm, realms[0], length - 1);
				realm[length - 1] = '\0';
				krb5_free_host_realm(use_ctx, realms);
				if (options->debug) {
					debug("%s is in realm \"%s\"",
					      host, realm);
				}
				i = 0;
				break;
			}
		} else {
			if (options->debug) {
				debug("error %d(%s) determining realm for %s",
				      i, v5_error_message(i), host);
			}
		}
	}

	if (use_ctx != ctx) {
		_pam_krb5_free_ctx(use_ctx);
	}

	free(address);

	return i;
}

/* Create a new PAG. */
int
minikafs_setpag(void)
{
	return minikafs_call(minikafs_subsys_setpag, 0, 0, 0, 0);
}

#if 0
/* Leave any PAG. It turns out this results in an unlog(), which is not what we
 * wanted here. */
static int
minikafs_unpag(void)
{
	struct minikafs_ioblock iob;
	char wfile[] = "/afs";
	int i;

	memset(&iob, 0, sizeof(iob));
	iob.in = wfile;
	iob.insize = sizeof(wfile);
	iob.out = wfile;
	iob.outsize = sizeof(wfile);

	i = minikafs_pioctl(wfile, minikafs_pioctl_unpag, &iob);
	return i;
}
#endif

/* Determine which cell is the default on this workstation. */
int
minikafs_ws_cell(char *cell, size_t length)
{
	struct minikafs_ioblock iob;
	char wfile[] = "/afs";
	int i;

	memset(&iob, 0, sizeof(iob));
	iob.in = wfile;
	iob.insize = strlen(wfile) + 1;
	iob.out = cell;
	iob.outsize = length - 1;
	memset(cell, '\0', length);

	i = minikafs_pioctl(wfile, minikafs_pioctl_getwscell, &iob);
	
	return i;
}

/* Stuff a ticket and DES key into the kernel. */
static int
minikafs_settoken(const void *ticket, uint32_t ticket_size,
		  int kvno, const unsigned char *key,
		  uint32_t uid, uint32_t start, uint32_t end, uint32_t flags,
		  const char *cell)
{
	char *buffer;
	struct minikafs_plain_token plain_token;
	struct minikafs_ioblock iob;
	uint32_t size;
	int i;

	/* Allocate the input buffer. */
	buffer = malloc(4 + ticket_size +
			4 + sizeof(struct minikafs_plain_token) +
			4 +
			strlen(cell) + 1);
	if (buffer == NULL) {
		return -1;
	}

	/* their copy of the session key, encrypted with their key */
	size = ticket_size;
	memcpy(buffer, &size, 4);
	memcpy(buffer + 4, ticket, size);

	/* our copy of the session key, plus housekeeping */
	plain_token.kvno = kvno;
	memcpy(&plain_token.key, key, 8);
	plain_token.uid = uid;
	plain_token.start = start;
	plain_token.end = end;
	if (((end - start) % 2) != 0) {
		plain_token.end--;
	}

	size = sizeof(plain_token);
	memcpy(buffer + 4 + ticket_size, &size, 4);
	memcpy(buffer + 4 + ticket_size + 4, &plain_token, size);

	/* flags */
	size = flags;
	memcpy(buffer + 4 + ticket_size + 4 + sizeof(plain_token), &size, 4);

	/* the name of the cell */
	memcpy(buffer + 4 + ticket_size + 4 + sizeof(plain_token) + 4,
	       cell, strlen(cell) + 1);

	/* the regular stuff */
	memset(&iob, 0, sizeof(iob));
	iob.in = buffer;
	iob.insize = 4 + ticket_size +
		     4 + sizeof(struct minikafs_plain_token) +
		     4 + strlen(cell) + 1;
	iob.out = NULL;
	iob.outsize = 0;

	i = minikafs_pioctl(NULL, minikafs_pioctl_settoken, &iob);
	free(buffer);
	return i;
}

/* Check if a 64-bit key is one of the known weak or semi-weak DES keys. */
krb5_boolean
minikafs_key_is_weak(const unsigned char *key)
{
	unsigned int i, j;
	const unsigned char weak[][8] = {
		/* weak keys */
		{0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01},
		{0xfe, 0xfe, 0xfe, 0xfe, 0xfe, 0xfe, 0xfe, 0xfe},
		{0xe0, 0xe0, 0xe0, 0xe0, 0xf1, 0xf1, 0xf1, 0xf1},
		{0x1f, 0x1f, 0x1f, 0x1f, 0x0e, 0x0e, 0x0e, 0x0e},
		/* semi-weak keys */
		{0x01, 0x1f, 0x01, 0x1f, 0x01, 0x0e, 0x01, 0x0e},
		{0x1f, 0x01, 0x1f, 0x01, 0x0e, 0x01, 0x0e, 0x01},
		{0x01, 0xe0, 0x01, 0xe0, 0x01, 0xf1, 0x01, 0xf1},
		{0xe0, 0x01, 0xe0, 0x01, 0xf1, 0x01, 0xf1, 0x01},
		{0x01, 0xfe, 0x01, 0xfe, 0x01, 0xfe, 0x01, 0xfe},
		{0xfe, 0x01, 0xfe, 0x01, 0xfe, 0x01, 0xfe, 0x01},
		{0x1f, 0xe0, 0x1f, 0xe0, 0x0e, 0xf1, 0x0e, 0xf1},
		{0xe0, 0x1f, 0xe0, 0x1f, 0xf1, 0x0e, 0xf1, 0x0e},
		{0x1f, 0xfe, 0x1f, 0xfe, 0x0e, 0xfe, 0x0e, 0xfe},
		{0xfe, 0x1f, 0xfe, 0x1f, 0xfe, 0x0e, 0xfe, 0x0e},
		{0xe0, 0xfe, 0xe0, 0xfe, 0xf1, 0xfe, 0xf1, 0xfe},
		{0xfe, 0xe0, 0xfe, 0xe0, 0xfe, 0xf1, 0xfe, 0xf1},
	};
	for (i = 0; i < sizeof(weak) / sizeof(weak[0]); i++) {
		/* We could use memcmp() to do this, but since the lowest bit
		 * is a parity bit, and the values we're checking against might
		 * have them set correctly, or not, do it bytewise. */
		for (j = 0; j < 8; j++) {
			if ((key[j] & 0xfe) != (weak[i][j] & 0xfe)) {
				break;
			}
		}
		/* All eight bytes match up, more or less, so it's weak. */
		if (j == 8) {
			return 1;
		}
	}
	return 0;
}

/* Check if the random-to-key derivation for a given enctype is just "use it
 * as-is", because that and DES-style key-to-random is all we know how to do. */
krb5_boolean
minikafs_r2k_is_identity(krb5_context ctx, krb5_enctype etype)
{
	int result = -1;
	size_t kbytes, klength;
	krb5_data rdata;
	krb5_keyblock rkey, key;

	memset(&rkey, 0, sizeof(rkey));
	memset(&key, 0, sizeof(key));
	memset(&rdata, 0, sizeof(rdata));
	kbytes = 0;
	klength = 0;
	if (krb5_c_keylengths(ctx, etype, &kbytes, &klength) != 0) {
		result = 0;
		goto done;
	}
	if ((klength == 0) || (kbytes != klength)) {
		result = 0;
		goto done;
	}
	key.contents = malloc(klength);
	key.length = klength;
	key.enctype = etype;
	if (key.contents == NULL) {
		result = 0;
		goto done;
	}
	if (krb5_c_make_random_key(ctx, etype, &rkey) != 0) {
		result = 0;
		goto done;
	}
	rdata.data = (char *) rkey.contents;
	rdata.length = rkey.length;
	if (krb5_c_random_to_key(ctx, etype, &rdata, &key) != 0) {
		result = 0;
		goto done;
	}
	result = (rdata.length == key.length) && (memcmp(rdata.data, key.contents, key.length) == 0);
done:
	if (rkey.contents != NULL) {
		krb5_free_keyblock_contents(ctx, &rkey);
	}
	free(key.contents);
	return result == 1;
}

/* The basic building block of our KD PRF - compute an MD5 HMAC over "in" using
 * "kd" as the key. */
int
minikafs_hmac_md5(krb5_context ctx, const unsigned char *kd, size_t kd_size,
		  krb5_data *in, krb5_data *out)
{
	int ret = -1;
	unsigned int i;
	krb5_data input;
	krb5_checksum kcksum, icksum, ocksum;
	unsigned char *inner = NULL, *outer = NULL, *kd_tmp = NULL;
	const unsigned char *kd_use = NULL;
	const size_t ibsize = 64, obsize = 16;

	memset(out, 0, sizeof(*out));
	memset(&input, 0, sizeof(input));
	memset(&kcksum, 0, sizeof(kcksum));
	memset(&icksum, 0, sizeof(icksum));
	memset(&ocksum, 0, sizeof(ocksum));
	/* Hash down the key, if we need to do so in order to make it fit. */
	if (kd_size > ibsize) {
		input.data = (char *) kd;
		input.length = kd_size;
		if (krb5_c_make_checksum(ctx, CKSUMTYPE_RSA_MD5, NULL, 0,
					 &input, &kcksum) != 0) {
			goto done;
		}
		kd_tmp = malloc(kcksum.length);
		if (kd_tmp == NULL) {
			goto done;
		}
		memcpy(kd_tmp, kcksum.contents, kcksum.length);
		kd_use = (const unsigned char *) kd_tmp;
		kd_size = kcksum.length;
	} else {
		kd_use = kd;
	}
	/* Set up the inner buffer: the key with padding, plus the text. */
	inner = malloc(ibsize + in->length);
	if (inner == NULL) {
		goto done;
	}
	memset(inner, 0, ibsize + in->length);
	memcpy(inner, kd_use, kd_size);
	for (i = 0; i < ibsize; i++) {
		inner[i] ^= 0x36; /* ipad */
	}
	memcpy(inner + ibsize, in->data, in->length);
	/* Inner hash. */
	input.data = (char *) inner;
	input.length = ibsize + in->length;
	if (krb5_c_make_checksum(ctx, CKSUMTYPE_RSA_MD5, NULL, 0, &input,
				 &icksum) != 0) {
		goto done;
	}
	/* Check that we were right about sizes. */
	if (icksum.length != obsize) {
		goto done;
	}
	/* Set up the outer buffer: the key with padding, plus the inner result. */
	outer = malloc(ibsize + obsize);
	if (outer == NULL) {
		goto done;
	}
	memset(outer, 0, ibsize + obsize);
	memcpy(outer, kd_use, kd_size);
	memcpy(outer + ibsize, icksum.contents, icksum.length);
	for (i = 0; i < ibsize; i++) {
		outer[i] ^= 0x5c; /* opad */
	}
	/* Now the outer hash. */
	input.data = (char *) outer;
	input.length = ibsize + obsize;
	if (krb5_c_make_checksum(ctx, CKSUMTYPE_RSA_MD5, NULL, 0, &input,
				 &ocksum) != 0) {
		goto done;
	}
	/* Copy the result out. */
	if ((out->data == NULL) || (out->length < ocksum.length)) {
		free(out->data);
		out->data = malloc(ocksum.length);
		if (out->data == NULL) {
			goto done;
		}
	}
	memcpy(out->data, ocksum.contents, ocksum.length);
	out->length = ocksum.length;
	ret = 0;
done:
	if (kcksum.contents != NULL) {
		krb5_free_checksum_contents(ctx, &kcksum);
	}
	if (icksum.contents != NULL) {
		krb5_free_checksum_contents(ctx, &icksum);
	}
	if (ocksum.contents != NULL) {
		krb5_free_checksum_contents(ctx, &ocksum);
	}
	free(inner);
	free(outer);
	free(kd_tmp);
	return ret;
}

/* Derive a 64-bit key from a larger one, per
 * http://lists.openafs.org/pipermail/afs3-standardization/2013-July/002738.html
 * Given original randomly-generated bits that we've recovered from a key,
 * generate an MD5 HMAC using the key as the key, over a plaintext included in
 * the document.  Then use the initial portion of the HMAC value as random
 * input for generating a DES key. */
int
minikafs_kd_derive(krb5_context ctx, const unsigned char *kd, size_t kd_size,
		   unsigned char *key)
{
	krb5_data in, out;
	unsigned char indata[11] = {0, 'r', 'x', 'k', 'a', 'd', 0, 0, 0, 0, 64};
	unsigned int i, j, k, p;

	memset(&in, 0, sizeof(in));
	in.data = (char *) indata;
	in.length = 11;
	for (i = 1; i < 256; i++) {
		indata[0] = i;
		memset(&out, 0, sizeof(out));
		if (minikafs_hmac_md5(ctx, kd, kd_size, &in, &out) == 0) {
			if (out.length < 8) {
				return -1;
			}
			for (j = 0; j < 8; j++) {
				key[j] = out.data[j];
				key[j] &= 0xfe;
				p = 1;
				for (k = 1; k < 8; k++) {
					p ^= ((key[j] >> k) & 1);
				}
				key[j] |= p;
			}
			if (!minikafs_key_is_weak(key)) {
				return 0;
			}
			free(out.data);
		}
	}
	return -1;
}

/* Undo the random-to-key transformation for triple-DES keys.
 * The transformation collects the lower bits of the seven random bytes and
 * maps them into the eighth byte, the first byte's in bit 1, the second byte's
 * in bit 2, and so on, and replaces them with parity bits, including bit 0 in
 * the last byte of the key.
 * Undoing that means replacing the parity (low) bit in the first seven bytes
 * with their corresponding original random bits from the last byte in the key
 * block. */
void
minikafs_des3_k2r(const unsigned char *k, unsigned char *r)
{
	unsigned int i, j;
	unsigned char p, b;

	for (i = 0; i < 3; i++) {
		for (j = 0; j < 7; j++) {
			b = k[i * 8 + j];
			p = (k[i * 8 + 7]) >> (j + 1);
			r[i * 7 + j] = (b & 0xfe) | (p & 1);
		}
	}
}

/* Stuff the ticket and key from a credentials structure into the kernel. */
static int
minikafs_5settoken(krb5_context ctx, const char *cell, krb5_creds *creds,
		   uid_t uid)
{
	unsigned char key[8], key3[21];
	const unsigned char *kd = NULL, *tmp = NULL;
	size_t kd_size = 0;
	int ret;

	/* How we do this depends on the session key type. */
	switch (v5_creds_key_type(creds)) {
	/* Keys of these types are not suitable. */
	case ENCTYPE_NULL:
	case ENCTYPE_DES_CBC_RAW:
	case ENCTYPE_DES3_CBC_RAW:
	case ENCTYPE_DES_HMAC_SHA1:
#ifdef ENCTYPE_DSA_SHA1_CMS
	case ENCTYPE_DSA_SHA1_CMS:
#endif
#ifdef ENCTYPE_MD5_RSA_CMS
	case ENCTYPE_MD5_RSA_CMS:
#endif
#ifdef ENCTYPE_SHA1_RSA_CMS
	case ENCTYPE_SHA1_RSA_CMS:
#endif
#ifdef ENCTYPE_RC2_CBC_ENV
	case ENCTYPE_RC2_CBC_ENV:
#endif
#ifdef ENCTYPE_RSA_ENV
	case ENCTYPE_RSA_ENV:
#endif
#ifdef ENCTYPE_RSA_ES_OAEP_ENV
	case ENCTYPE_RSA_ES_OAEP_ENV:
#endif
#ifdef ENCTYPE_DES3_CBC_ENV
	case ENCTYPE_DES3_CBC_ENV:
#endif
		/* Key not random, per draft-kaduk-afs3-rxkad-kdf-03. */
		return -1;
	case ENCTYPE_DES_CBC_CRC:
	case ENCTYPE_DES_CBC_MD4:
	case ENCTYPE_DES_CBC_MD5:
		/* Single DES: use as-is. */
		memcpy(key, v5_creds_key_contents(creds), 8);
		break;
	case ENCTYPE_DES3_CBC_SHA:
	case ENCTYPE_DES3_CBC_SHA1:
		/* Triple DES: recover the lowest bits of the first 7 bytes of
		 * each 8 bytes of key to get the original bits. */
		tmp = v5_creds_key_contents(creds);
		memset(key3, 0, sizeof(key3));
		minikafs_des3_k2r(tmp, key3);
		kd = key3;
		kd_size = 21;
		break;
	default:
		/* For everything else, if the random-to-key procedure is to
		 * just use the random bits as-is, then we know what to do. */
		if (minikafs_r2k_is_identity(ctx, v5_creds_key_type(creds))) {
			/* kd as-is. */
			kd = v5_creds_key_contents(creds);
			kd_size = v5_creds_key_length(creds);
		} else {
			/* ... otherwise, we don't. */
			return -1;
		}
	}
	if (kd != NULL) {
		if (minikafs_kd_derive(ctx, kd, kd_size, key) != 0) {
			return -1;
		}
	}
	ret = minikafs_settoken(creds->ticket.data,
				creds->ticket.length,
				0x100, /* magic number, signals OpenAFS 1.2.8 and
					* later that the ticket is actually a v5
					* ticket */
				key,
				uid,
				creds->times.starttime,
				creds->times.endtime,
				0,
				cell);
	memset(key, 0, sizeof(key));
	return ret;
}

/* Clear our tokens. */
int
minikafs_unlog(void)
{
	return minikafs_pioctl(NULL, minikafs_pioctl_unlog, NULL);
}

/* Ask the kernel which ciphers it supports for use with rxk5. */
static int
minikafs_get_property(const char *property, char *value, int length)
{
	struct minikafs_ioblock iob;
	int i;

	iob.in = property ? (char *) property : "*";
	iob.insize = strlen(property) + 1;
	iob.out = value;
	iob.outsize = length;
	i = minikafs_pioctl(NULL, minikafs_pioctl_getprop, &iob);
	return i;
}

static int
minikafs_get_rxk5_enctypes(krb5_enctype *etypes, int n_etypes)
{
	int n;
	uint32_t i;
	long l;
	const char *property = "rxk5.enctypes", *p, *v;
	char enctypes[1024], *q;
	n = -1;
	memset(enctypes, '\0', sizeof(enctypes));
	if (minikafs_get_property(property,
				  enctypes, sizeof(enctypes) - 1) == 0) {
		p = enctypes;
		n = 0;
		while ((p != NULL) && (*p != '\0') && (n < n_etypes)) {
			v = p + strlen(p) + 1;
			if (strcmp(p, property) == 0) {
				p = v;
				while ((p != NULL) && (*p != '\0') &&
				       (n < n_etypes)) {
					l = strtol(p, &q, 10);
					if ((q != NULL) &&
					    ((*q == ' ') || (*q == '\0'))) {
						i = l & 0xffffffff;
						if (i != 0) {
							etypes[n++] = i;
						}
						p = q + strcspn(q,
								"0123456789");
					} else {
						break;
					}
				}
			}
			p = v + strlen(v) + 1;
		}
	}
	return n;
}

/* Try to set a token for the given cell using creds for the named principal. */
static int
minikafs_5log_with_principal(krb5_context ctx,
			     struct _pam_krb5_options *options,
			     krb5_ccache ccache,
			     const char *cell,
			     const char *principal,
			     uid_t uid,
			     int use_rxk5,
			     int use_v5_2b)
{
	krb5_principal server, client;
	krb5_creds mcreds, creds, *new_creds;
	char *unparsed_client;
	krb5_enctype rxk5_enctypes[16];
	krb5_enctype *etypes;
	int i, n_etypes;
	int tmp;

	memset(&client, 0, sizeof(client));
	memset(&server, 0, sizeof(server));
	if (use_rxk5) {
		n_etypes = minikafs_get_rxk5_enctypes(rxk5_enctypes,
						      sizeof(rxk5_enctypes) /
						      sizeof(rxk5_enctypes[0]) -
						      1);
#if 1
		n_etypes = 0;
#endif
		if (n_etypes > 0) {
			etypes = rxk5_enctypes;
			rxk5_enctypes[n_etypes] = 0;
		} else {
			etypes = NULL;
			n_etypes = 1; /* hack: we want to try at least once */
		}
	} else
	if (use_v5_2b) {
#ifdef HAVE_KRB5_ALLOW_WEAK_CRYPTO
		if (krb5_allow_weak_crypto(ctx, TRUE) != 0) { /* XXX */
			warn("error enabling weak crypto (DES), continuing");
		}
#endif
		etypes = NULL;
		n_etypes = 1; /* hack: we want to try at least once */
	} else {
		etypes = NULL;
		n_etypes = 1; /* hack: we want to try at least once */
	}

	if (krb5_cc_get_principal(ctx, ccache, &client) != 0) {
		if (options->debug) {
			debug("error determining default principal name "
			      "for ccache");
		}
		return -1;
	}
	unparsed_client = NULL;
	if (krb5_unparse_name(ctx, client, &unparsed_client) != 0) {
		warn("error unparsing client principal name from ccache");
		krb5_free_principal(ctx, client);
		return -1;
	}
	if (v5_parse_name(ctx, options, principal, &server) != 0) {
		warn("error parsing principal name '%s'", principal);
		v5_free_unparsed_name(ctx, unparsed_client);
		krb5_free_principal(ctx, client);
		return -1;
	}

	/* Check if we already have a suitable credential. */
	for (i = 0; i < n_etypes; i++) {
		memset(&mcreds, 0, sizeof(mcreds));
		memset(&creds, 0, sizeof(creds));
		mcreds.client = client;
		mcreds.server = server;
		if (etypes != NULL) {
#ifdef HAVE_KRB5_ENCTYPE_ENABLE
			if (krb5_enctype_enable(ctx, etypes[i]) != 0) {
				char etype[32];
				/* Whether or not enctype_to_string
				 * nul-terminates varies between
				 * implementations and versions. */
				memset(etype, '\0', sizeof(etype));
				if (v5_enctype_to_string(ctx, etypes[i], etype,
							 sizeof(etype) - 1) != 0) {
					warn("error enabling enctype %d, "
					     "continuing", etypes[i]);
				} else {
					warn("error enabling enctype %s "
					     "continuing", etype);
				}
			}
#endif
			v5_creds_set_etype(ctx, &mcreds, etypes[i]);
		}
		if (krb5_cc_retrieve_cred(ctx, ccache, v5_cc_retrieve_match(),
					  &mcreds, &creds) == 0) {
			if (use_rxk5 &&
			    (minikafs_5settoken2(cell, &creds, uid) == 0)) {
				krb5_free_cred_contents(ctx, &creds);
				v5_free_unparsed_name(ctx, unparsed_client);
				krb5_free_principal(ctx, client);
				krb5_free_principal(ctx, server);
				return 0;
			} else
			if (use_v5_2b &&
			    (minikafs_5settoken(ctx, cell, &creds, uid) == 0)) {
				krb5_free_cred_contents(ctx, &creds);
				v5_free_unparsed_name(ctx, unparsed_client);
				krb5_free_principal(ctx, client);
				krb5_free_principal(ctx, server);
				return 0;
			}
			krb5_free_cred_contents(ctx, &creds);
		}
	}

	/* Try to obtain a suitable credential. */
	for (i = 0; i < n_etypes; i++) {
		memset(&mcreds, 0, sizeof(mcreds));
		mcreds.client = client;
		mcreds.server = server;
		if (etypes != NULL) {
			v5_creds_set_etype(ctx, &mcreds, etypes[i]);
		}
		new_creds = NULL;
		tmp = krb5_get_credentials(ctx, 0, ccache,
					   &mcreds, &new_creds);
		if (tmp == 0) {
			if (use_rxk5 &&
			    (minikafs_5settoken2(cell, new_creds, uid) == 0)) {
				krb5_free_creds(ctx, new_creds);
				v5_free_unparsed_name(ctx, unparsed_client);
				krb5_free_principal(ctx, client);
				krb5_free_principal(ctx, server);
				return 0;
			} else
			if (use_v5_2b &&
			    (minikafs_5settoken(ctx, cell, new_creds, uid) == 0)) {
				krb5_free_creds(ctx, new_creds);
				v5_free_unparsed_name(ctx, unparsed_client);
				krb5_free_principal(ctx, client);
				krb5_free_principal(ctx, server);
				return 0;
			}
			krb5_free_creds(ctx, new_creds);
		} else {
			if (options->debug) {
				if (etypes != NULL) {
					debug("error obtaining credentials for "
					      "'%s' (enctype=%d) on behalf of "
					      "'%s': %s",
					      principal, etypes[i],
					      unparsed_client,
					      v5_error_message(tmp));
				} else {
					debug("error obtaining credentials for "
					      "'%s' on behalf of "
					      "'%s': %s",
					      principal,
					      unparsed_client,
					      v5_error_message(tmp));
				}
			}
		}
	}

	v5_free_unparsed_name(ctx, unparsed_client);
	krb5_free_principal(ctx, client);
	krb5_free_principal(ctx, server);

	return -1;
}

/* Try to obtain tokens for the named cell using the default ccache and
 * configuration settings. */
static int
minikafs_5log(krb5_context context, krb5_ccache ccache,
	      struct _pam_krb5_options *options,
	      const char *cell, const char *hint_principal,
	      uid_t uid, int use_rxk5, int use_v5_2b)
{
	krb5_context ctx;
	krb5_ccache use_ccache;
	int ret;
	unsigned int i;
	char *principal, *defaultrealm, realm[PATH_MAX];
	size_t principal_size, base_size;
	const char *base_rxkad[] = {"afs", "afsx"};
	const char *base_rxk5[] = {"afs-k5"};
	const char **base;

	if (context == NULL) {
		if (_pam_krb5_init_ctx(&ctx, 0, NULL) != 0) {
			return -1;
		}
	} else {
		ctx = context;
	}

	if (use_rxk5) {
		base = base_rxk5;
		base_size = sizeof(base_rxk5) / sizeof(base_rxk5[0]);
	} else {
		base = base_rxkad;
		base_size = sizeof(base_rxkad) / sizeof(base_rxkad[0]);
	}

	memset(&use_ccache, 0, sizeof(use_ccache));
	if (ccache != NULL) {
		use_ccache = ccache;
	} else {
		if (krb5_cc_default(ctx, &use_ccache) != 0) {
			if (ctx != context) {
				_pam_krb5_free_ctx(ctx);
			}
			return -1;
		}
	}

	/* If we were given a principal name, try it. */
	if ((hint_principal != NULL) && (strlen(hint_principal) > 0)) {
		if (options->debug) {
			debug("attempting to obtain tokens for \"%s\" "
			      "(hint \"%s\")",
			      cell, hint_principal);
		}
		ret = minikafs_5log_with_principal(ctx, options, use_ccache,
						   cell, hint_principal, uid,
						   use_rxk5, use_v5_2b);
		if (ret == 0) {
			if (use_ccache != ccache) {
				krb5_cc_close(ctx, use_ccache);
			}
			if (ctx != context) {
				_pam_krb5_free_ctx(ctx);
			}
			return 0;
		}
	}

	defaultrealm = NULL;
	if (krb5_get_default_realm(ctx, &defaultrealm) != 0) {
		defaultrealm = NULL;
	}

	if (options->debug) {
		debug("attempting to determine realm for \"%s\"", cell);
	}
	if (minikafs_realm_of_cell_with_ctx(ctx, options, cell,
					    realm, sizeof(realm)) != 0) {
		strncpy(realm, cell, sizeof(realm));
		realm[sizeof(realm) - 1] = '\0';
		for (i = 0; i < sizeof(realm); i++) {
			realm[i] = toupper(realm[i]);
		}
	}

	principal_size = strlen("/@") + 1;
	ret = -1;
	for (i = 0; (ret != 0) && (i < base_size); i++) {
		principal_size += strlen(base[i]);
	}
	principal_size += strlen(cell);
	principal_size += strlen(realm);
	if (defaultrealm != NULL) {
		principal_size += strlen(defaultrealm);
	}
	principal = malloc(principal_size);
	if (principal == NULL) {
		if (use_ccache != ccache) {
			krb5_cc_close(ctx, use_ccache);
		}
		if (defaultrealm != NULL) {
			v5_free_default_realm(ctx, defaultrealm);
		}
		if (ctx != context) {
			_pam_krb5_free_ctx(ctx);
		}
		return -1;
	}

	for (i = 0; (ret != 0) && (i < base_size); i++) {
		/* If the realm name and cell name are similar, and null_afs
		 * is set, try the NULL instance. */
		if ((strcasecmp(realm, cell) == 0) && options->null_afs_first) {
			snprintf(principal, principal_size, "%s@%s",
				 base[i], realm);
			if (options->debug) {
				debug("attempting to obtain tokens for \"%s\" "
				      "(\"%s\")", cell, principal);
			}
			ret = minikafs_5log_with_principal(ctx, options,
							   use_ccache,
							   cell, principal, uid,
							   use_rxk5, use_v5_2b);
		}
		if (ret == 0) {
			break;
		}
		/* Try the cell instance in the cell's realm. */
		snprintf(principal, principal_size, "%s/%s@%s",
			 base[i], cell, realm);
		if (options->debug) {
			debug("attempting to obtain tokens for \"%s\" (\"%s\")",
			      cell, principal);
		}
		ret = minikafs_5log_with_principal(ctx, options, use_ccache,
						   cell, principal, uid,
						   use_rxk5, use_v5_2b);
		if (ret == 0) {
			break;
		}
		/* If the realm name and cell name are similar, and null_afs
		 * is not set, try the NULL instance. */
		if ((strcasecmp(realm, cell) == 0) &&
		    !options->null_afs_first) {
			snprintf(principal, principal_size, "%s@%s",
				 base[i], realm);
			if (options->debug) {
				debug("attempting to obtain tokens for \"%s\" "
				      "(\"%s\")", cell, principal);
			}
			ret = minikafs_5log_with_principal(ctx, options,
							   use_ccache,
							   cell, principal, uid,
							   use_rxk5, use_v5_2b);
		}
		if (ret == 0) {
			break;
		}
		/* Repeat the last two attempts, but using the default realm. */
		if ((defaultrealm != NULL) &&
		    (strcmp(defaultrealm, realm) != 0)) {
			/* If the default realm name and cell name are similar,
			 * and null_afs is set, try the NULL instance. */
			if ((strcasecmp(defaultrealm, cell) == 0) &&
			    options->null_afs_first) {
				snprintf(principal, principal_size, "%s@%s",
					 base[i], defaultrealm);
				if (options->debug) {
					debug("attempting to obtain tokens for "
					      "\"%s\" (\"%s\")",
					      cell, principal);
				}
				ret = minikafs_5log_with_principal(ctx, options,
								   use_ccache,
								   cell,
								   principal,
								   uid,
								   use_rxk5,
								   use_v5_2b);
			}
			if (ret == 0) {
				break;
			}
			/* Try the cell instance in the default realm. */
			snprintf(principal, principal_size, "%s/%s@%s",
				 base[i], cell, defaultrealm);
			if (options->debug) {
				debug("attempting to obtain tokens for \"%s\" "
				      "(\"%s\")", cell, principal);
			}
			ret = minikafs_5log_with_principal(ctx, options,
							   use_ccache,
							   cell, principal, uid,
							   use_rxk5, use_v5_2b);
			if (ret == 0) {
				break;
			}
			/* If the default realm name and cell name are similar,
			 * and null_afs isn't set, try the NULL instance. */
			if ((strcasecmp(defaultrealm, cell) == 0) &&
			    !options->null_afs_first) {
				snprintf(principal, principal_size, "%s@%s",
					 base[i], defaultrealm);
				if (options->debug) {
					debug("attempting to obtain tokens for "
					      "\"%s\" (\"%s\")",
					      cell, principal);
				}
				ret = minikafs_5log_with_principal(ctx, options,
								   use_ccache,
								   cell,
								   principal,
								   uid,
								   use_rxk5,
								   use_v5_2b);
			}
			if (ret == 0) {
				break;
			}
		}
	}

	if (use_ccache != ccache) {
		krb5_cc_close(ctx, use_ccache);
	}
	if (defaultrealm != NULL) {
		v5_free_default_realm(ctx, defaultrealm);
	}
	if (ctx != context) {
		_pam_krb5_free_ctx(ctx);
	}
	free(principal);

	return ret;
}

/* Try to get tokens for the named cell using every available mechanism. */
int
minikafs_log(krb5_context ctx, krb5_ccache ccache,
	     struct _pam_krb5_options *options,
	     const char *cell, const char *hint_principal,
	     uid_t uid, const int *methods, int n_methods)
{
	int i, method;
	if (n_methods == -1) {
		for (i = 0; methods[i] != 0; i++) {
			continue;
		}
		n_methods = i;
	}
	for (method = 0; method < n_methods; method++) {
		i = -1;
		switch (methods[method]) {
		case MINIKAFS_METHOD_V5_2B:
			if (options->debug) {
				debug("trying with ticket (2b)");
			}
			i = minikafs_5log(ctx, ccache, options, cell,
					  hint_principal, uid, 0, 1);
			if (i != 0) {
				if (options->debug) {
					debug("afslog (2b) failed to \"%s\"",
					      cell);
				}
			}
			break;
		case MINIKAFS_METHOD_RXK5:
			if (options->debug) {
				debug("trying with ticket (rxk5)");
			}
			i = minikafs_5log(ctx, ccache, options, cell,
					  hint_principal, uid, 1, 0);
			if (i != 0) {
				if (options->debug) {
					debug("afslog (rxk5) failed to \"%s\"",
					      cell);
				}
			}
			break;
		default:
			break;
		}
		if (i == 0) {
			break;
		}
	}
	if (method < n_methods) {
		if (options->debug) {
			debug("got tokens for cell \"%s\"", cell);
		}
		return 0;
	} else {
		return -1;
	}
}

/* We do the XDR here to avoid deps on what might not be a standard part of
 * glibc, and we don't need the decode or free functionality. */
static int
encode_int32(char *buffer, int32_t num)
{
	int32_t net;
	if (buffer) {
		net = ntohl(num);
		memcpy(buffer, &net, 4);
	}
	return 4;
}
static int
encode_boolean(char *buffer, krb5_boolean b)
{
	return encode_int32(buffer, b ? 1 : 0);
}
static int
encode_uint64(char *buffer, uint64_t num)
{
	int32_t net;
	if (buffer) {
		net = ntohl(num >> 32);
		memcpy(buffer + 0, &net, 4);
		net = ntohl(num & 0xffffffff);
		memcpy(buffer + 4, &net, 4);
	}
	return 8;
}
static int
encode_bytes(char *buffer, const char *bytes, int32_t num)
{
	int32_t pad;
	pad = (num % 4) ? (4 - (num % 4)) : 0;
	if (buffer) {
		if (bytes && num) {
			memcpy(buffer, bytes, num);
			memset(buffer + num, 0, pad);
		}
	}
	return num + pad;
}
static int
encode_ubytes(char *buffer, const unsigned char *bytes, int32_t num)
{
	int32_t pad;
	pad = (num % 4) ? (4 - (num % 4)) : 0;
	if (buffer) {
		if (bytes && num) {
			memcpy(buffer, bytes, num);
			memset(buffer + num, 0, pad);
		}
	}
	return num + pad;
}
#define encode_fixed(_op, _buffer, _item) \
	{ \
		int _length; \
		_length = _op(_buffer, _item); \
		if (_buffer) { \
			_buffer += _length; \
		} \
		total += _length; \
	}
#define encode_fixed_with_arg(_op, _buffer, _item, _size) \
	{ \
		int _length; \
		_length = _op(_buffer, _item, _size); \
		if (_buffer) { \
			_buffer += _length; \
		} \
		total += _length; \
	}
#define encode_variable(_op, _buffer, _item, _size) \
	{ \
		int _length; \
		_length = _op(_buffer, _item, _size); \
		if (_buffer) { \
			_buffer += _length; \
		} \
		total += _length; \
	}
#define encode_opaque(_op, _buffer, _item, _size) \
	encode_fixed(encode_int32, _buffer, _size) \
	encode_variable(_op, _buffer, _item, _size)
static int
encode_data(char *buffer, krb5_data *data)
{
	int32_t total = 0;
	encode_opaque(encode_bytes, buffer, data->data, data->length);
	return total;
}
static int
encode_string(char *buffer, const char *string, ssize_t length)
{
	int32_t total = 0;
	if (length == -1) {
		length = strlen(string);
	}
	encode_opaque(encode_bytes, buffer, string, length);
	return total;
}
static int
encode_creds_keyblock(char *buffer, krb5_creds *creds)
{
	int32_t total = 0;
	encode_fixed(encode_int32, buffer, v5_creds_get_etype(creds));
	encode_opaque(encode_ubytes, buffer, v5_creds_key_contents(creds),
		      v5_creds_key_length(creds));
	return total;
}
static int
encode_principal(char *buffer, krb5_principal princ)
{
	int32_t total = 0;
	int i;
	encode_fixed(encode_int32, buffer, v5_princ_component_count(princ));
	for (i = 0; i < v5_princ_component_count(princ); i++) {
		encode_opaque(encode_bytes, buffer,
			      v5_princ_component_contents(princ, i),
			      v5_princ_component_length(princ, i));
	}
	encode_opaque(encode_bytes, buffer,
		      v5_princ_realm_contents(princ),
		      v5_princ_realm_length(princ));
	return total;
}
static int
encode_token_rxkad(char *buffer, krb5_creds *creds, int32_t viceid)
{
	int32_t total = 0;

	encode_fixed(encode_int32, buffer, viceid);
	encode_fixed(encode_int32, buffer, 0x100 - 0x2b);
	encode_opaque(encode_ubytes, buffer, v5_creds_key_contents(creds),
		      v5_creds_key_length(creds));
	encode_fixed(encode_int32, buffer, creds->times.starttime);
	encode_fixed(encode_int32, buffer, creds->times.endtime);
	encode_fixed(encode_boolean, buffer, 0);
	encode_fixed(encode_data, buffer, &creds->ticket);
	return total;
}
static int
encode_token_rxk5(char *buffer, krb5_creds *creds)
{
	int32_t total = 0;
	int i; 

	encode_fixed(encode_principal, buffer, creds->client);
	encode_fixed(encode_principal, buffer, creds->server);
	encode_fixed(encode_creds_keyblock, buffer, creds);
	encode_fixed(encode_uint64, buffer, creds->times.authtime);
	encode_fixed(encode_uint64, buffer, creds->times.starttime);
	encode_fixed(encode_uint64, buffer, creds->times.endtime);
	encode_fixed(encode_uint64, buffer, creds->times.renew_till);
	encode_fixed(encode_boolean, buffer, v5_creds_get_is_skey(creds));
	encode_fixed(encode_int32, buffer, v5_creds_get_flags(creds));

	encode_fixed(encode_int32, buffer, v5_creds_address_count(creds));
	for (i = 0; i < v5_creds_address_count(creds); i++) {
		encode_fixed(encode_int32, buffer,
			     v5_creds_address_type(creds, i));
		encode_opaque(encode_ubytes, buffer,
			      v5_creds_address_contents(creds, i),
			      v5_creds_address_length(creds, i));
	}

	encode_fixed(encode_data, buffer, &creds->ticket);
	encode_fixed(encode_data, buffer, &creds->second_ticket);

	encode_fixed(encode_int32, buffer, v5_creds_authdata_count(creds));
	for (i = 0; i < v5_creds_authdata_count(creds); i++) {
		encode_fixed(encode_int32, buffer,
			     v5_creds_authdata_type(creds, i));
		encode_opaque(encode_ubytes, buffer,
			      v5_creds_authdata_contents(creds, i),
			      v5_creds_authdata_length(creds, i));
	}
	return total;
}
#define AFSTOKEN_UNION_NOAUTH	0
#define AFSTOKEN_UNION_NONE	AFSTOKEN_UNION_NOAUTH
#define AFSTOKEN_UNION_KAD	2
#define AFSTOKEN_UNION_RXKAD	AFSTOKEN_UNION_KAD
#define AFSTOKEN_UNION_RXGK	4
#define AFSTOKEN_UNION_GK	AFSTOKEN_UNION_RXGK
#define AFSTOKEN_UNION_RXK5	5
#define AFSTOKEN_UNION_K5	AFSTOKEN_UNION_RXK5
static int
encode_token_union(char *buffer, krb5_creds *creds, int token_union_type,
		   int32_t uid)
{
	int32_t total = 0;
	encode_fixed(encode_int32, buffer, token_union_type);
	switch (token_union_type) {
	case AFSTOKEN_UNION_RXKAD:
		encode_fixed_with_arg(encode_token_rxkad, buffer, creds, uid);
		break;
	case AFSTOKEN_UNION_RXK5:
		encode_fixed(encode_token_rxk5, buffer, creds);
		break;
	default:
		break;
	}
	return total;
}

/* Stuff a ticket and keyblock into the kernel. */
#define AFSTOKEN_EX_SETPAG	0x00000001 /* not supported */
#define AFSTOKEN_EX_ADD		0x00000002
static int
minikafs_5settoken2(const char *cell, krb5_creds *creds, int32_t uid)
{
	struct minikafs_ioblock iob;
	int i, bufsize, token_union_size;
	char *buffer, *bufptr;

	token_union_size = encode_token_union(NULL, creds, AFSTOKEN_UNION_K5,
					      uid);
	bufsize = encode_int32(NULL, 0) +
		  encode_string(NULL, cell, -1) +
		  encode_int32(NULL, 1) +
		  encode_int32(NULL, token_union_size) +
		  token_union_size;
	buffer = malloc(bufsize);
	i = -1;
	if (buffer != NULL) {
		bufptr = buffer;
		bufptr += encode_int32(bufptr, 0); /* flags - AFSTOKEN_EX_... */
		bufptr += encode_string(bufptr, cell, -1); /* cell */
		bufptr += encode_int32(bufptr, 1); /* number of tokens */
		bufptr += encode_int32(bufptr, token_union_size); /* size of token */
		bufptr += encode_token_union(bufptr, creds, AFSTOKEN_UNION_K5,
					     uid); /* token */
		iob.in = buffer;
		iob.insize = bufptr - buffer;
		iob.out = NULL;
		iob.outsize = 0;
		i = minikafs_pioctl(NULL, minikafs_pioctl_settoken2, &iob);
		free(buffer);
	}
	return i;
}
