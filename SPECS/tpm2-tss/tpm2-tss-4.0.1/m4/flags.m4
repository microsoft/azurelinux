dnl ADD_COMPILER_FLAG:
dnl   A macro to add a CFLAG to the EXTRA_CFLAGS variable. This macro will
dnl   check to be sure the compiler supports the flag. Flags can be made
dnl   mandatory (configure will fail).
dnl $1: C compiler flag to add to EXTRA_CFLAGS.
dnl $2: Set to "required" to cause configure failure if flag not supported.
AC_DEFUN([ADD_COMPILER_FLAG],[
    AX_CHECK_COMPILE_FLAG([$1],[
        EXTRA_CFLAGS="$EXTRA_CFLAGS $1"
        AC_SUBST([EXTRA_CFLAGS])],[
        AS_IF([test x$2 != xrequired],[
            AC_MSG_WARN([Optional CFLAG "$1" not supported by your compiler, continuing.])],[
            AC_MSG_ERROR([Required CFLAG "$1" not supported by your compiler, aborting.])]
        )],[
        -Wall -Werror]
    )]
)
dnl ADD_PREPROC_FLAG:
dnl   Add the provided preprocessor flag to the EXTRA_CFLAGS variable. This
dnl   macro will check to be sure the preprocessor supports the flag.
dnl   The flag can be made mandatory by providing the string 'required' as
dnl   the second parameter.
dnl $1: Preprocessor flag to add to EXTRA_CFLAGS.
dnl $2: Set to "required" t ocause configure failure if preprocesor flag
dnl     is not supported.
AC_DEFUN([ADD_PREPROC_FLAG],[
    AX_CHECK_PREPROC_FLAG([$1],[
        EXTRA_CFLAGS="$EXTRA_CFLAGS $1"
        AC_SUBST([EXTRA_CFLAGS])],[
        AS_IF([test x$2 != xrequired],[
            AC_MSG_WARN([Optional preprocessor flag "$1" not supported by your compiler, continuing.])],[
            AC_MSG_ERROR([Required preprocessor flag "$1" not supported by your compiler, aborting.])]
        )],[
        -Wall -Werror]
    )]
)
dnl ADD_LINK_FLAG:
dnl   A macro to add a LDLAG to the EXTRA_LDFLAGS variable. This macro will
dnl   check to be sure the linker supports the flag. Flags can be made
dnl   mandatory (configure will fail).
dnl $1: linker flag to add to EXTRA_LDFLAGS.
dnl $2: Set to "required" to cause configure failure if flag not supported.
AC_DEFUN([ADD_LINK_FLAG],[
    AX_CHECK_LINK_FLAG([$1],[
        EXTRA_LDFLAGS="$EXTRA_LDFLAGS $1"
        AC_SUBST([EXTRA_LDFLAGS])],[
        AS_IF([test x$2 != xrequired],[
            AC_MSG_WARN([Optional LDFLAG "$1" not supported by your linker, continuing.])],[
            AC_MSG_ERROR([Required LDFLAG "$1" not supported by your linker, aborting.])]
        )]
    )]
)
dnl ADD_FUZZING_FLAG:
dnl   A macro to add a CFLAG to the EXTRA_CFLAGS variable.
dnl $1: C++ linker flag to add to FUZZ_LDFLAGS.
AC_DEFUN([ADD_FUZZING_FLAG],[
    FUZZ_LDFLAGS="$FUZZ_LDFLAGS $1"
    AC_SUBST([FUZZ_LDFLAGS])
])
