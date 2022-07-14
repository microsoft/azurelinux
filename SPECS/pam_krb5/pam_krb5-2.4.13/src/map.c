/*
 * Copyright 2003,2004,2005,2006 Red Hat, Inc.
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
#include <limits.h>
#include <regex.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#ifdef HAVE_SECURITY_PAM_APPL_H
#include <security/pam_appl.h>
#endif

#ifdef HAVE_SECURITY_PAM_MODULES_H
#include <security/pam_modules.h>
#endif

#include KRB5_H

#include "log.h"
#include "map.h"
#include "options.h"

#define SEPARATOR '$'

static int
map_single(const char *pattern, const char *replacement,
	   const char *input, char *output, size_t output_len)
{
	regex_t re;
	regmatch_t *matches;
	const char *specifiers = "0123456789", *p;
	size_t n_matches;
	unsigned int i, j;
	int k, match;

	/* Limit the length of the match array. */
	n_matches = strlen(input) * 2;
	if (n_matches > 100) {
		return -1;
	}
	if (n_matches < strlen(specifiers)) {
		n_matches = strlen(specifiers) * 2;
	}
	matches = malloc(n_matches * sizeof(regmatch_t));
	if (matches == NULL) {
		return -1;
	}

	for (i = 0; i < n_matches; i++) {
		matches[i].rm_so = -1;
		matches[i].rm_eo = -1;
	}

	/* Build the pattern and check for a match. */
	i = regcomp(&re, pattern, REG_EXTENDED);
	if (i != 0) {
		free(matches);
		return -1;
	}
	i = regexec(&re, input, n_matches, matches, 0);
	if (i != 0) {
		free(matches);
		regfree(&re);
		return -1;
	}
	if ((matches[0].rm_so == -1) && (matches[0].rm_eo != -1)) {
		free(matches);
		regfree(&re);
		return -1;
	}
	regfree(&re);

	/* Build the output string. */
	for (i = j = 0; (replacement[i] != '\0') && (j < output_len - 1); i++) {
		switch (replacement[i]) {
		case SEPARATOR:
			i++;
			if (replacement[i] == SEPARATOR) {
				output[j++] = replacement[i];
			} else {
				/* Decide which match to insert here. */
				p = strchr(specifiers, replacement[i]);
				if (p != NULL) {
					match = p - specifiers;
				} else {
					match = -1;
				}
				/* Only bother if we have a match. */
				if ((match != -1) &&
				    (matches[match].rm_so != -1) &&
				    (matches[match].rm_eo != -1)) {
					k = matches[match].rm_so;
					while ((k < matches[match].rm_eo) &&
					       (j < output_len - 1)) {
						output[j++] = input[k++];
					}
				}
			}
			break;
		default:
			output[j++] = replacement[i];
			break;
		}
	}
	free(matches);
	output[j] = '\0';
	/* Check for unexpected truncation. */
	if (replacement[i] != '\0') {
		return -1;
	}
	return 0;
}

int
map_lname_aname(const struct name_mapping *mappings, int n_mappings,
		const char *lname,
		char *principal, size_t principal_len)
{
	int i, status;

	/* Iterate through the maps. */
	for (i = 0; i < n_mappings; i++) {
		status = map_single(mappings[i].pattern,
				    mappings[i].replacement,
				    lname,
				    principal,
				    principal_len);
		if (status == 0) {
			return 0;
		}
	}
	return -1;
}

#if 0
int
main(int argc, char **argv)
{
	char output[LINE_MAX];
	int i;

	if (argc < 4) {
		printf("Usage: %s pattern replacment data\n", argv[0]);
		return 1;
	}
	i = map_single(argv[1], argv[2], argv[3],
		       output, sizeof(output));
	if (i == 0) {
		printf("Match: \"%s\" -> \"%s\"\n", argv[3], output);
	} else {
		printf("No match: \"%s\"\n", argv[3]);
	}
	return 0;
}
#endif
