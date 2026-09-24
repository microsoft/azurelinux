# Azure Linux: prefer uutils (Rust coreutils) over GNU coreutils.
#
# uutils installs plain-named symlinks (ls, cp, mv, ...) under
# /usr/lib/uutils/bin. The GNU coreutils utilities remain untouched at
# /usr/bin. Prepending the uutils directory to PATH makes uutils the default
# for name-resolved lookups in interactive/login shells, while absolute paths
# (e.g. /usr/bin/ls) and scripts with hardcoded paths keep using GNU coreutils.
#
# To fall back to GNU coreutils, remove this file (or move the directory to the
# end of PATH). This selection is PATH-only and never touches /usr/bin.
if [ -d /usr/lib/uutils/bin ] ; then
    case ":${PATH}:" in
        *:/usr/lib/uutils/bin:*) ;;
        *) PATH="/usr/lib/uutils/bin${PATH:+:${PATH}}" ;;
    esac
    export PATH
fi
