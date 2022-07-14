/*
 * Copyright 2003,2004,2006 Red Hat, Inc.
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

#include <stdlib.h>
#include <string.h>

#ifdef HAVE_SECURITY_PAM_APPL_H
#include <security/pam_appl.h>
#endif

#ifdef HAVE_SECURITY_PAM_MODULES_H
#include <security/pam_modules.h>
#endif

#include KRB5_H
#include "conv.h"
#include "items.h"
#include "prompter.h"

/* A PAM conversation function takes as its input a pointer to a pointer to a
 * message structure.  This adds an ambiguity -- is it a pointer to an array,
 * or an array of pointers?  (Basically, is the second message at
 * (*messages)[2] or at *(messages[2])?)  If we call the conversation function
 * through this function, both should work, and we make sure that the
 * conversation function gets the proper appdata pointer as well, so that's one
 * less thing about which we have to worry. */
int
_pam_krb5_conv_call(pam_handle_t *pamh,
		    PAM_KRB5_MAYBE_CONST struct pam_message *messages,
		    int n_prompts,
		    struct pam_response **responses)
{
	struct pam_conv *conv;
	int i;
	struct pam_response *drop_responses;
	PAM_KRB5_MAYBE_CONST struct pam_message **message_array;

	/* Get the address of the conversation structure provided by the
	 * application. */
	conv = NULL;
	i = _pam_krb5_get_item_conv(pamh, &conv);
	if (i != PAM_SUCCESS) {
		return i;
	}
	if (conv == NULL) {
		return PAM_BAD_ITEM;
	}

	/* Allocate the array for storing pointers to elements in the array
	 * which we were passed. */
	message_array = malloc(sizeof(struct pam_message*) * n_prompts);
	if (message_array == NULL) {
		return PAM_BUF_ERR;
	}
	memset(message_array, 0, sizeof(struct pam_message*) * n_prompts);

	/* Initialize the array so that each element holds a pointer to a
	 * corresponding element in the passed-in array. */
	for (i = 0; i < n_prompts; i++) {
		message_array[i] = &(messages[i]);
	}

	/* Call the converation function. */
	if (responses == NULL) {
		responses = &drop_responses;
		drop_responses = NULL;
	}
	i = conv->conv(n_prompts, message_array, responses, conv->appdata_ptr);
	if (responses == &drop_responses) {
		_pam_krb5_maybe_free_responses(drop_responses, n_prompts);
	}

	/* Clean up. */
	memset(message_array, 0, sizeof(struct pam_message*) * n_prompts);
	free(message_array);

	return i;
}
