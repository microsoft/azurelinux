# /etc/profile

# System wide environment and startup programs, for login setup
# Functions and aliases go in /etc/bashrc

# It's NOT a good idea to change this file unless you know what you
# are doing. It's much better to create a custom.sh shell script in
# /etc/profile.d/ to make custom changes to your environment, as this
# will prevent the need for merging in future updates.

pathmunge () {
    # If the path is a compat symlink, do nothing.
    [ -h "$1" ] && return

    case ":${PATH}:" in
        *:"$1":*)
            ;;
        *)
            if [ "$2" = "after" ] ; then
                PATH=$PATH:$1
            else
                PATH=$1:$PATH
            fi
    esac
}


if [ -x /usr/bin/id ]; then
    if [ -z "$EUID" ]; then
        # ksh workaround
        EUID=`/usr/bin/id -u`
        UID=`/usr/bin/id -ru`
    fi
    USER="`/usr/bin/id -un`"
    LOGNAME=$USER
    MAIL="/var/spool/mail/$USER"
fi

# Path manipulation
if [ "$EUID" = "0" ]; then
    pathmunge /usr/sbin
    pathmunge /usr/local/sbin
else
    pathmunge /usr/local/sbin after
    pathmunge /usr/sbin after
fi

HOSTNAME=$(/usr/bin/hostnamectl --transient 2>/dev/null) || \
HOSTNAME=$(/usr/bin/hostname 2>/dev/null) || \
HOSTNAME=$(/usr/bin/uname -n)

if [ -z "$HISTSIZE" ] ; then
    HISTSIZE=1000
fi

if [ "$HISTCONTROL" = "ignorespace" ] ; then
    export HISTCONTROL=ignoreboth
else
    export HISTCONTROL=ignoredups
fi

export PATH USER LOGNAME MAIL HOSTNAME HISTSIZE HISTCONTROL

for i in /etc/profile.d/*.sh /etc/profile.d/sh.local ; do
    if [ -r "$i" ]; then
        if [ "${-#*i}" != "$-" ]; then
            . "$i"
        else
            . "$i" >/dev/null
        fi
    fi
done

unset i
unset -f pathmunge

# Source global bash config, when interactive but not posix or sh mode
if test "$BASH" &&\
   test -z "$POSIXLY_CORRECT" &&\
   test "${0#-}" != sh &&\
   test -r /etc/bashrc
then
   # Bash login shells run only /etc/profile
   # Bash non-login shells run only /etc/bashrc
   # Check for double sourcing is done in /etc/bashrc.
   . /etc/bashrc
fi
