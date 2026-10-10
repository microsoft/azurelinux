# Azure Linux: prefer uutils (Rust coreutils) over GNU coreutils. (csh/tcsh)
#
# Companion to uutils-coreutils.sh for csh/tcsh login shells. PATH-only: the
# GNU coreutils files at /usr/bin are never touched. Remove this file to fall
# back to GNU coreutils.
if ( -d /usr/lib/uutils/bin ) then
    if ( $?PATH ) then
        if ( ":${PATH}:" !~ *:/usr/lib/uutils/bin:* ) then
            setenv PATH /usr/lib/uutils/bin:${PATH}
        endif
    else
        setenv PATH /usr/lib/uutils/bin
    endif
endif
