#!/bin/sh
exec grep -q -E '(commencing operation|started)' "$*" 2> /dev/null
