/*
 * Copyright 2003,2006,2009 Red Hat, Inc.
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

#ifndef pam_krb5_prompter_h
#define pam_krb5_prompter_h

struct _pam_krb5_prompter_data {
	krb5_context ctx;
	pam_handle_t *pamh;
	const char *previous_password;
	struct _pam_krb5_user_info *userinfo;
	struct _pam_krb5_options *options;
};

/* Ask the user. */
krb5_error_code
_pam_krb5_always_prompter(krb5_context context, void *data,
			  const char *name, const char *banner,
			  int num_prompts, krb5_prompt prompts[]);

/* Ask the user, except for the password. */
krb5_error_code
_pam_krb5_normal_prompter(krb5_context context, void *data,
			  const char *name, const char *banner,
			  int num_prompts, krb5_prompt prompts[]);

/* Always pretend we couldn't get anything. */
krb5_error_code
_pam_krb5_always_fail_prompter(krb5_context context, void *data,
			       const char *name, const char *banner,
			       int num_prompts, krb5_prompt prompts[]);

/* Always return the previous_password stored in the data item, which is a
 * _pam_krb5_prompter_data structure. */
krb5_error_code
_pam_krb5_previous_prompter(krb5_context context, void *data,
			    const char *name, const char *banner,
			    int num_prompts, krb5_prompt prompts[]);

/* Wrap calls to the PAM conversation function. */
int _pam_krb5_prompt_for(pam_handle_t *pamh,
			 const char *prompt, char **response);
int _pam_krb5_prompt_for_2(pam_handle_t *pamh,
			   const char *prompt, char **response,
			   const char *prompt2, char **response2);
void _pam_krb5_maybe_free_responses(struct pam_response *responses,
				    int n_responses);

#endif
