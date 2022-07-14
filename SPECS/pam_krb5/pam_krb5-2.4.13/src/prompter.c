/*
 * Copyright 2003,2004,2005,2006,2009 Red Hat, Inc.
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
#include <stdio.h>
#include "conv.h"
#include "log.h"
#include "options.h"
#include "prompter.h"
#include "userinfo.h"
#include "xstr.h"

void
_pam_krb5_maybe_free_responses(struct pam_response *responses, int n_responses)
{
#ifndef LEAKY_BUT_SAFER
	int i;
	if (responses != NULL) {
		for (i = 0; i < n_responses; i++) {
			if (responses[i].resp != NULL) {
				xstrfree(responses[i].resp);
			}
			responses[i].resp = NULL;
		}
		free(responses);
	}
#endif
}

static int
_pam_krb5_prompt_default_is_password(krb5_prompt *prompt,
				     struct _pam_krb5_prompter_data *pdata)
{
	size_t length;
	if (pdata == NULL) {
		return 0;
	}
	if (pdata->previous_password != NULL) {
		length = strlen(pdata->previous_password);
		if (prompt->reply->length == length) {
			if (memcmp(prompt->reply->data,
				   pdata->previous_password,
				   length) == 0) {
				return 1;
			}
		}
	}
	return 0;
}

static krb5_prompt_type
_pam_krb5_prompt_type(krb5_context ctx, krb5_prompt *prompt, int prompt_index)
{
#if defined(HAVE_KRB5_GET_PROMPT_TYPES)
	krb5_prompt_type *prompt_types;
	prompt_types = krb5_get_prompt_types(ctx);
	if (prompt_types != NULL) {
		return prompt_types[prompt_index];
	}
#elif defined(HAVE_KRB5_PROMPT_PROMPT_TYPE)
	if (prompt != NULL) {
		return prompt[prompt_index].prompt_type;
	}
#endif
	return -1;
}

static int
_pam_krb5_prompt_is_for_password(krb5_prompt *prompt,
				 struct _pam_krb5_prompter_data *pdata,
				 int prompt_index)
{
	char *expected;
	const char *p;
	/* The easy way. */
	if (_pam_krb5_prompt_type(pdata->ctx, prompt, prompt_index) ==
	    KRB5_PROMPT_TYPE_PASSWORD) {
		return 1;
	}
	/* The hard way. */
	expected = malloc(strlen(pdata->userinfo->unparsed_name) + 32);
	if (expected != NULL) {
		/* Simple */
		sprintf(expected, "Password");
		if (strcmp(prompt->prompt, expected) == 0) {
			free(expected);
			return 1;
		}
		if (strncmp(prompt->prompt, expected, strlen(expected)) == 0) {
			p = prompt->prompt + strlen(expected);
			if (strspn(p, ": \t\r\n") == strlen(p)) {
				free(expected);
				return 1;
			}
		}
		/* MIT */
		sprintf(expected, "Password for %s",
			pdata->userinfo->unparsed_name);
		if (strcmp(prompt->prompt, expected) == 0) {
			free(expected);
			return 1;
		}
		if (strncmp(prompt->prompt, expected, strlen(expected)) == 0) {
			p = prompt->prompt + strlen(expected);
			if (strspn(p, ": \t\r\n") == strlen(p)) {
				free(expected);
				return 1;
			}
		}
		/* Heimdal */
		sprintf(expected, "%s's Password",
			pdata->userinfo->unparsed_name);
		if (strcmp(prompt->prompt, expected) == 0) {
			free(expected);
			return 1;
		}
		if (strncmp(prompt->prompt, expected, strlen(expected)) == 0) {
			p = prompt->prompt + strlen(expected);
			if (strspn(p, ": \t\r\n") == strlen(p)) {
				free(expected);
				return 1;
			}
		}
		free(expected);
	}
	return 0;
}

krb5_error_code
_pam_krb5_always_fail_prompter(krb5_context context, void *data,
			       const char *name, const char *banner,
			       int num_prompts, krb5_prompt prompts[])
{
	struct _pam_krb5_prompter_data *pdata = data;
	int i;
	krb5_error_code ret;

	ret = 0;
	if ((name != NULL) || (banner != NULL)) {
		_pam_krb5_normal_prompter(context, data, name, banner, 0, NULL);
	}
	for (i = 0; i < num_prompts; i++) {
		if (_pam_krb5_prompt_default_is_password(&prompts[i], pdata)) {
			if (pdata->options->debug &&
			    pdata->options->debug_sensitive) {
				debug("libkrb5 asked for \"%s\", "
				      "default value \"%.*s\", skipping",
				      prompts[i].prompt,
				      (int)
				      (prompts[i].reply ?
				       prompts[i].reply->length : 0),
				      (const char *)
				      (prompts[i].reply ?
				       prompts[i].reply->data : ""));
			}
			continue;
		}
		if (pdata->options->debug && pdata->options->debug_sensitive) {
			debug("libkrb5 asked for \"%s\", "
			      "default value \"%.*s\"",
			      prompts[i].prompt,
			      (int)
			      (prompts[i].reply ? prompts[i].reply->length : 0),
			      (const char *)
			      (prompts[i].reply ? prompts[i].reply->data : ""));
			debug("returning password-reading error to libkrb5");
		}
		ret = KRB5_LIBOS_CANTREADPWD;
		break;
	}

	return ret;
}

krb5_error_code
_pam_krb5_previous_prompter(krb5_context context, void *data,
			    const char *name, const char *banner,
			    int num_prompts, krb5_prompt prompts[])
{
	struct _pam_krb5_prompter_data *pdata = data;
	int i;

	if ((name != NULL) || (banner != NULL)) {
		_pam_krb5_normal_prompter(context, data, name, banner, 0, NULL);
	}
	if (pdata->previous_password == NULL) {
		return KRB5_LIBOS_CANTREADPWD;
	}
	/* Provide it as the answer to every question. */
	for (i = 0; i < num_prompts; i++) {
		if (_pam_krb5_prompt_default_is_password(&prompts[i], pdata)) {
			if (pdata->options->debug &&
			    pdata->options->debug_sensitive) {
				debug("libkrb5 asked for \"%s\", "
				      "default value \"%.*s\", skipping",
				      prompts[i].prompt,
				      (int)
				      (prompts[i].reply ?
				       prompts[i].reply->length : 0),
				      (const char *)
				      (prompts[i].reply ?
				       prompts[i].reply->data : ""));
			}
			continue;
		}
		if (prompts[i].reply->length <=
		    strlen(pdata->previous_password)) {
			return KRB5_LIBOS_CANTREADPWD;
		}
		if (pdata->options->debug && pdata->options->debug_sensitive) {
			debug("libkrb5 asked for \"%s\", "
			      "default value \"%.*s\"",
			      prompts[i].prompt,
			      (int)
			      (prompts[i].reply ? prompts[i].reply->length : 0),
			      (const char *)
			      (prompts[i].reply ? prompts[i].reply->data : ""));
			debug("returning \"%s\"", pdata->previous_password);
		}
		strcpy(prompts[i].reply->data, pdata->previous_password);
		prompts[i].reply->length = strlen(pdata->previous_password);
	}
	return 0;
}

static krb5_error_code
_pam_krb5_generic_prompter(krb5_context context, void *data,
			   const char *name, const char *banner,
			   int num_prompts, krb5_prompt prompts[],
			   int suppress_password_prompts)
{
	struct pam_message *messages;
	struct pam_response *responses;
	int headers, i, j, ret, num_msgs;
	char *tmp;
	struct _pam_krb5_prompter_data *pdata = data;
	krb5_data *pw1, *pw2;

	/* If we have a name or banner, we need to make space for it in the
	 * messages structure, so keep track of the number of non-prompts which
	 * we'll be throwing at the user. */
	if ((name != NULL) && (strlen(name) > 0)) {
		headers = 1;
	} else {
		headers = 0;
	}
	if ((banner != NULL) && (strlen(banner) > 0)) {
		headers++;
	}

	/* Allocate space for the prompts. */
	messages = malloc(sizeof(struct pam_message) * (num_prompts + headers));
	if (messages == NULL) {
		return KRB5_LIBOS_CANTREADPWD;
	}
	memset(messages, 0,
	       sizeof(struct pam_message) * (num_prompts + headers));

	/* If the name and/or banner were given, make them the first prompts. */
	if ((name != NULL) && (strlen(name) > 0)) {
		messages[0].msg = name;
		messages[0].msg_style = PAM_TEXT_INFO;
	}
	if ((banner != NULL) && (strlen(banner) > 0)) {
		if ((name != NULL) && (strlen(name) > 0)) {
			messages[1].msg = banner;
			messages[1].msg_style = PAM_TEXT_INFO;
		} else {
			messages[0].msg = banner;
			messages[0].msg_style = PAM_TEXT_INFO;
		}
	}
	/* Copy the prompt strings over. */
	for (i = j = 0; i < num_prompts; i++) {
		/* Skip any prompt for which the supplied default answer is the
		 * previously-entered password -- it's just a waste of the
		 * user's time.  */
		if (_pam_krb5_prompt_default_is_password(&prompts[i], pdata)) {
			if (pdata->options->debug &&
			    pdata->options->debug_sensitive) {
				debug("libkrb5 asked for \"%s\", "
				      "default value \"%.*s\", skipping",
				      prompts[i].prompt,
				      (int)
				      (prompts[i].reply ?
				       prompts[i].reply->length : 0),
				      (const char *)
				      (prompts[i].reply ?
				       prompts[i].reply->data : ""));
			}
			continue;
		}
		/* If we're just asking for the password again, also skip it,
		 * if we were told to. */
		if (_pam_krb5_prompt_is_for_password(&prompts[i], pdata, i)) {
			if (suppress_password_prompts) {
				/* We're told to suppress this prompt. */
				continue;
			} else {
				if (pdata->options->debug) {
					debug("libkrb5 asked for long-term "
					      "password, replacing prompt text "
					      "with generic prompt");
				}
				tmp = xstrdup(Y_("Password: "));
			}
		} else
		if (_pam_krb5_prompt_type(pdata->ctx, prompts, i) ==
		    KRB5_PROMPT_TYPE_NEW_PASSWORD) {
			if (pdata->options->debug) {
				debug("libkrb5 asked for a new long-term "
				      "password, replacing prompt text "
				      "with generic prompt");
			}
			tmp = malloc(strlen(Y_("New %s%sPassword: ")) +
				     strlen(pdata->options->banner) + 2);
			if (tmp != NULL) {
				sprintf(tmp, Y_("New %s%sPassword: "),
					pdata->options->banner,
					strlen(pdata->options->banner) > 0 ?
					" " : "");
			}
		} else
		if (_pam_krb5_prompt_type(pdata->ctx, prompts, i) ==
		    KRB5_PROMPT_TYPE_NEW_PASSWORD_AGAIN) {
			if (pdata->options->debug) {
				debug("libkrb5 asked for a new long-term "
				      "password again, replacing prompt text "
				      "with generic prompt");
			}
			tmp = malloc(strlen(Y_("Repeat New %s%sPassword: ")) +
				     strlen(pdata->options->banner) + 2);
			if (tmp != NULL) {
				sprintf(tmp, Y_("Repeat New %s%sPassword: "),
					pdata->options->banner,
					strlen(pdata->options->banner) > 0 ?
					" " : "");
			}
		} else {
			tmp = malloc(strlen(prompts[i].prompt) + 3);
			if (tmp != NULL) {
				sprintf(tmp, "%s: ", prompts[i].prompt);
			}
		}
		messages[j + headers].msg = tmp;
		messages[j + headers].msg_style = prompts[i].hidden ?
						  PAM_PROMPT_ECHO_OFF :
						  PAM_PROMPT_ECHO_ON;
		j++;
	}
	num_msgs = j + headers;

	/* Get some responses. */
	responses = NULL;
	ret = _pam_krb5_conv_call(pdata->pamh, messages, num_msgs, &responses);

	/* We can discard the messages now. */
	for (i = j = 0; i < num_prompts; i++) {
		if (_pam_krb5_prompt_default_is_password(&prompts[i], pdata)) {
			continue;
		}
		free((char*) messages[j + headers].msg);
		messages[j + headers].msg = NULL;
		j++;
	}
	free(messages);
	messages = NULL;

	/* If we failed, and we asked questions, bail now. */
	if ((ret != PAM_SUCCESS) ||
	    ((j > 0) && (responses == NULL))) {
		return KRB5_LIBOS_CANTREADPWD;
	}

	/* Check for successfully-read responses. */
	for (i = j = 0; i < num_prompts; i++) {
		if (_pam_krb5_prompt_default_is_password(&prompts[i], pdata)) {
			continue;
		}
		if (_pam_krb5_prompt_is_for_password(&prompts[i], pdata, i)) {
			if (suppress_password_prompts) {
				continue;
			}
		}
		/* If the conversation function failed to read anything. */
		if (responses[j + headers].resp_retcode != PAM_SUCCESS) {
			_pam_krb5_maybe_free_responses(responses, num_msgs);
			return KRB5_LIBOS_CANTREADPWD;
		}
		/* Or it claimed it could but didn't. */
		if (responses[j + headers].resp == NULL) {
			_pam_krb5_maybe_free_responses(responses, num_msgs);
			return KRB5_LIBOS_CANTREADPWD;
		}
		/* Or it did and we have no space for the answer. */
		if ((unsigned int)xstrlen(responses[j + headers].resp) >= prompts[i].reply->length) {
			_pam_krb5_maybe_free_responses(responses, num_msgs);
			return KRB5_LIBOS_CANTREADPWD;
		}
		j++;
	}

	/* Gather up the results. */
	pw1 = NULL;
	pw2 = NULL;
	for (i = j = 0; i < num_prompts; i++) {
		if (_pam_krb5_prompt_default_is_password(&prompts[i], pdata)) {
			/* We never prompted for this. */
			continue;
		}
		if (_pam_krb5_prompt_is_for_password(&prompts[i], pdata, i)) {
			if (suppress_password_prompts) {
				/* We decided to suppress this prompt, so it
				 * gets its default answer. */
				continue;
			}
		}
		/* Double-check for NULL here.  We should have caught it above
		 * if that was the case, but it doesn't hurt. */
		if (responses[j + headers].resp == NULL) {
			_pam_krb5_maybe_free_responses(responses, num_msgs);
			return KRB5_LIBOS_CANTREADPWD;
		}
		/* Save the response text. */
		if (pdata->options->debug && pdata->options->debug_sensitive) {
			debug("libkrb5 asked for \"%s\", default was \"%.*s\", "
			      "returning \"%s\"",
			      prompts[i].prompt,
			      (int)
			      (prompts[i].reply ?  prompts[i].reply->length : 0),
			      (const char *)
			      (prompts[i].reply ?  prompts[i].reply->data : ""),
			      responses[j + headers].resp);
		}
		strcpy(prompts[i].reply->data, responses[j + headers].resp);
		prompts[i].reply->length = strlen(responses[j + headers].resp);
		/* If it's a prompt for a new password, make note of it. */
		if (_pam_krb5_prompt_type(pdata->ctx, prompts, i) ==
		    KRB5_PROMPT_TYPE_NEW_PASSWORD) {
			pw1 = prompts[i].reply;
		}
		if (_pam_krb5_prompt_type(pdata->ctx, prompts, i) ==
		    KRB5_PROMPT_TYPE_NEW_PASSWORD_AGAIN) {
			pw2 = prompts[i].reply;
		}
		j++;
	}
	/* If we were called as part of a password-change operation, then
	 * we've captured both the new password and its confirmation.  Save the
	 * new password as the PAM_AUTHTOK for other modules. */
	if ((pw1 != NULL) && (pw2 != NULL) &&
	    (strcmp(pw1->data, pw2->data) == 0)) {
		if (pdata->options->debug) {
			debug("saving newly-entered password for use by "
			      "other modules");
		}
		pam_set_item(pdata->pamh, PAM_AUTHTOK, pw1->data);
	}

	_pam_krb5_maybe_free_responses(responses, num_msgs);
	return 0; /* success! */
}

krb5_error_code
_pam_krb5_normal_prompter(krb5_context context, void *data,
			  const char *name, const char *banner,
			  int num_prompts, krb5_prompt prompts[])
{
	return _pam_krb5_generic_prompter(context, data,
					  name, banner,
					  num_prompts, prompts, 1);
}

krb5_error_code
_pam_krb5_always_prompter(krb5_context context, void *data,
			  const char *name, const char *banner,
			  int num_prompts, krb5_prompt prompts[])
{
	return _pam_krb5_generic_prompter(context, data,
					  name, banner,
					  num_prompts, prompts, 0);
}

int
_pam_krb5_prompt_for(pam_handle_t *pamh, const char *prompt, char **response)
{
	struct pam_message message;
	struct pam_response *responses;
	int i;

	memset(&message, 0, sizeof(message));
	message.msg = prompt;
	message.msg_style = PAM_PROMPT_ECHO_OFF;
	responses = NULL;

	i = _pam_krb5_conv_call(pamh,
				&message, 1,
				&responses);
	if ((i == 0) && (responses != NULL)) {
		*response = xstrdup(responses[0].resp);
	}

	_pam_krb5_maybe_free_responses(responses, 1);

	return i;
}

int
_pam_krb5_prompt_for_2(pam_handle_t *pamh,
		       const char *prompt, char **response,
		       const char *prompt2, char **response2)
{
	struct pam_message messages[2];
	struct pam_response *responses;
	int i;

	memset(&messages, 0, sizeof(messages));
	messages[0].msg = prompt;
	messages[0].msg_style = PAM_PROMPT_ECHO_OFF;
	messages[1].msg = prompt2;
	messages[1].msg_style = PAM_PROMPT_ECHO_OFF;
	responses = NULL;

	i = _pam_krb5_conv_call(pamh,
				messages, 2,
				&responses);
	if ((i == 0) && (responses != NULL)) {
		*response = xstrdup(responses[0].resp);
		*response2 = xstrdup(responses[1].resp);
	}

	_pam_krb5_maybe_free_responses(responses, 2);

	return i;
}
