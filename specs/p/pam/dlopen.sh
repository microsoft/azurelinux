#!/bin/sh

tempdir=`mktemp -d /tmp/dlopenXXXXXX`
test -n "$tempdir" || exit 1
cat >> $tempdir/dlopen.c << _EOF
#include <dlfcn.h>
#include <stdio.h>
#include <limits.h>
#include <sys/stat.h>
/* Simple program to see if dlopen() would succeed. */
int main(int argc, char **argv)
{
	int i;
	struct stat st;
	char buf[PATH_MAX];
	for (i = 1; i < argc; i++) {
		if (dlopen(argv[i], RTLD_NOW)) {
			fprintf(stdout, "dlopen() of \"%s\" succeeded.\n",
				argv[i]);
		} else {
			snprintf(buf, sizeof(buf), "./%s", argv[i]);
			if ((stat(buf, &st) == 0) && dlopen(buf, RTLD_NOW)) {
				fprintf(stdout, "dlopen() of \"./%s\" "
					"succeeded.\n", argv[i]);
			} else {
				fprintf(stdout, "dlopen() of \"%s\" failed: "
					"%s\n", argv[i], dlerror());
				return 1;
			}
		}
	}
	return 0;
}
_EOF

for arg in $@ ; do
	case "$arg" in
	"")
		;;
	-I*|-D*|-f*|-m*|-g*|-O*|-W*)
		cflags="$cflags $arg"
		;;
	-l*|-L*)
		ldflags="$ldflags $arg"
		;;
	/*)
		modules="$modules $arg"
		;;
	*)
		modules="$modules $arg"
		;;
	esac
done

${CC:-gcc} $RPM_OPT_FLAGS $CFLAGS -o $tempdir/dlopen $cflags $tempdir/dlopen.c $ldflags -ldl

retval=0
for module in $modules ; do
	case "$module" in
	"")
		;;
	/*)
		$tempdir/dlopen "$module"
		retval=$?
		;;
	*)
		$tempdir/dlopen ./"$module"
		retval=$?
		;;
	esac
done

rm -f $tempdir/dlopen $tempdir/dlopen.c
rmdir $tempdir
exit $retval
