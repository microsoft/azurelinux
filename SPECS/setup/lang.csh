# /etc/profile.d/lang.csh - exports environment variables, and provides fallback
#                          for CJK languages that can't be displayed in console.
#                          Resets the locale if unavailable.

unset LANG_backup

# If unavailable, reset to the default. Do this before reading in any
# explicit user configuration. We simply check if locale emits any
# warnings, and assume that the settings are invalid if it does.
set locale_error=`(/usr/bin/locale >/dev/null) |& cat`
if ("${locale_error}" != "") then
    if (${?LANG}) then
        setenv LANG C.UTF-8
    endif
    unsetenv LC_ALL
    setenv LC_CTYPE C.UTF-8
    setenv LC_NUMERIC C.UTF-8
    setenv LC_TIME C.UTF-8
    setenv LC_COLLATE C.UTF-8
    setenv LC_MONETARY C.UTF-8
    setenv LC_MESSAGES C.UTF-8
    setenv LC_PAPER C.UTF-8
    setenv LC_NAME C.UTF-8
    setenv LC_ADDRESS C.UTF-8
    setenv LC_TELEPHONE C.UTF-8
    setenv LC_MEASUREMENT C.UTF-8
    setenv LC_IDENTIFICATION C.UTF-8
else
    if (${?LANG}) then
        set LANG_backup=${LANG}
    endif
endif

foreach config (/etc/locale.conf "${HOME}/.i18n")
    if (-f "${config}") then
        # NOTE: We are using eval & sed here to avoid invoking of any commands & functions from those files.
        eval `/usr/bin/sed -r -e 's/^[[:blank:]]*([[:upper:]_]+)=([[:print:][:digit:]\._-]+|"[[:print:][:digit:]\._-]+")/setenv \1 \2;/;t;d' ${config}`
    endif
end

if (${?LANG_backup}) then
    setenv LANG "${LANG_backup}"
endif

unset LANG_backup config locale_error

# ----------------------------------------------

# The LC_ALL is not supposed to be set in /etc/locale.conf according to 'man 5 locale.conf'.
# If it is set, then we expect it is user's explicit override (most likely from ~/.i18n file).
# See 'man 7 locale' for more info about LC_ALL.
if (${?LC_ALL}) then
    if (${?LANG}) then
        if (${LC_ALL} != ${LANG}) then
            setenv LC_ALL
        else
            unsetenv LC_ALL
        endif
    else
        unsetenv LC_ALL
    endif
endif

# The ${LANG} manipulation is necessary only in virtual terminal (a.k.a. console - /dev/tty*):
set in_console=`/usr/bin/tty | /usr/bin/grep -vc -e '/dev/tty'`

if (${?LANG} && ${?TERM}) then
    if (${TERM} == 'linux' && $in_console == 0) then
        set utf8_used=`echo ${LANG} | /usr/bin/grep -vc -E -i -e '^.+\.utf-?8$'`

        if (${utf8_used} == 0) then
            switch (${LANG})
                case en_IN*:
                    breaksw
                case ja*:
                case ko*:
                case si*:
                case zh*:
                case ar*:
                case fa*:
                case he*:
                case *_IN*:
                    setenv LANG en_US.UTF-8
                    breaksw
            endsw
        else
            switch (${LANG})
                case en_IN*:
                    breaksw
                case ja*:
                case ko*:
                case si*:
                case zh*:
                case ar*:
                case fa*:
                case he*:
                case *_IN*:
                    setenv LANG en_US
                    breaksw
            endsw
        endif

        # NOTE: We are not exporting the ${LANG} here again on purpose.
        #       If user starts GUI session from console manually, then
        #       the previously set LANG should be okay to use.
    endif
endif

unset in_console utf8_used
