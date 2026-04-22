#!/usr/bin/bash

# The pure GTK build of emacs is not supported on X11, so try to avoid
# using it there if there is another alternative.

preferred="$(readlink -f /usr/bin/emacs)"

if [[ $XDG_SESSION_TYPE == 'x11' ]]; then
    case "$preferred" in
    *-pgtk)
        for variant in gtk+x11 lucid; do
            if type "emacs-$variant" >/dev/null; then
                exec -a emacs "emacs-$variant" "$@"
            fi
        done
        ;;
    */emacs-desktop)
        # If this wrapper script is itself the preferred alternative,
        # select something suitable from the options available.
        for variant in gtk+x11 lucid pgtk nw; do
            if type "emacs-$variant" >/dev/null; then
                exec -a emacs "emacs-$variant" "$@"
            fi
        done
        exit 2
        ;;
    esac
else
    case "$preferred" in
    */emacs-desktop)
        for variant in pgtk gtk+x11 lucid nw; do
            if type "emacs-$variant" >/dev/null; then
                exec -a emacs "emacs-$variant" "$@"
            fi
        done
        exit 2
        ;;
    esac
fi

exec emacs "$@"
