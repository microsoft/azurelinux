#!/bin/sh

case "$1" in
    -c | --interactive-color)
        ! grep -qsi "^COLOR.*none" /etc/GREP_COLORS
        ;;
    *)
        echo >&2 "Invalid / no option passed, so far only -c | --interactive-color is supported."
        exit 1
        ;;
esac
