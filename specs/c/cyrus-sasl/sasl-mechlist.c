#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#include "sasl.h"

static int
my_getopt(void *context, const char *plugin_name,
	  const char *option, const char **result, unsigned *len)
{
	if (result) {
		*result = NULL;
#if 0
		fprintf(stderr, "Getopt plugin=%s%s%s/option=%s%s%s -> ",
			plugin_name ? "\"" : "",
			plugin_name ? plugin_name : "(null)",
			plugin_name ? "\"" : "",
			option ? "\"" : "",
			option ? option : "(null)",
			option ? "\"" : "");
		fprintf(stderr, "'%s'.\n", *result ? *result : "");
#endif
	}
	if (len) {
		*len = 0;
	}
	return 0;
}

int
main(int argc, char **argv)
{
	int ret, i;
	const char *mechs, **globals;
	sasl_callback_t callbacks[] = {
		{SASL_CB_GETOPT, (int (*)(void)) my_getopt, NULL},
		{SASL_CB_LIST_END},
	};
	sasl_conn_t *connection;
	char hostname[512];

	if ((argc > 1) && (argv[1][0] == '-')) {
		fprintf(stderr, "Usage: %s [appname [hostname] ]\n", argv[0]);
		return 0;
	}

	ret = sasl_server_init(callbacks, argc > 1 ? argv[1] : "sasl-mechlist");
	if (ret != SASL_OK) {
		fprintf(stderr, "Error in sasl_server_init(): %s\n",
			sasl_errstring(ret, NULL, NULL));
	}

	connection = NULL;
	strcpy(hostname, "localhost");
	gethostname(hostname, sizeof(hostname));
	ret = sasl_server_new(argc > 2 ? argv[2] : "host",
			      hostname,
			      NULL,
			      NULL,
			      NULL,
			      callbacks,
			      0,
			      &connection);
	if (ret != SASL_OK) {
		fprintf(stderr, "Error in sasl_server_new(): %s\n",
			sasl_errstring(ret, NULL, NULL));
	}

	ret = sasl_listmech(connection,
			    getenv("USER") ? getenv("USER") : "root",
			    "Available mechanisms: ",
			    ",",
			    "\n",
			    &mechs,
			    NULL,
			    NULL);
	if (ret != SASL_OK) {
		fprintf(stderr, "Error in sasl_listmechs(): %s\n",
			sasl_errstring(ret, NULL, NULL));
	} else {
		fprintf(stdout, "%s", mechs);
	}

	globals = sasl_global_listmech();
	for (i = 0; (globals != NULL) && (globals[i] != NULL); i++) {
		if (i == 0) {
			fprintf(stdout, "Library supports: ");
		}
		fprintf(stdout, "%s", globals[i]);
		if (globals[i + 1] != NULL) {
			fprintf(stdout, ",");
		} else {
			fprintf(stdout, "\n");
		}
	}

	return 0;
}
