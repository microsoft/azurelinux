#include "../../config.h"
#include <sys/types.h>
#include <stdio.h>
#include <string.h>
#include <krb5.h>
int
main(int argc, char **argv)
{
	krb5_context ctx;
	krb5_error_code ret;
	const char *ccname;

	ctx = NULL;
	ret = krb5_init_context(&ctx);
	if (ret != 0) {
		printf("Error initializing Kerberos.\n");
		return ret;
	}
	ccname = krb5_cc_default_name(ctx);
	printf("%s\n", ccname);
	krb5_free_context(ctx);
	return 0;
}
