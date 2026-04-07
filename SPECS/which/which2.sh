# shellcheck shell=sh
# Initialization script for bash, sh, mksh and ksh

if [ -r /proc/$$/exe ]; then
    SHELLNAME=$(basename $(readlink /proc/$$/exe))
else
    SHELLNAME="unknown"
fi
case "$SHELLNAME" in
*ksh*|zsh)
    alias which='alias | /usr/bin/which --tty-only --read-alias --show-tilde --show-dot'
    ;;
bash|sh)
    alias which='(alias; declare -f) | /usr/bin/which --tty-only --read-alias --read-functions --show-tilde --show-dot'
    ;;
*)
    ;;
esac
