# Azure Linux: prefer uutils (Rust coreutils) over GNU coreutils. (fish)
#
# Vendor conf.d snippet, sourced automatically by fish. PATH-only: the GNU
# coreutils files at /usr/bin are never touched. Remove this file to fall back
# to GNU coreutils.
if test -d /usr/lib/uutils/bin
    if not contains /usr/lib/uutils/bin $PATH
        set -gx PATH /usr/lib/uutils/bin $PATH
    end
end
