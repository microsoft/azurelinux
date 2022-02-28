#
# /etc/kshrc is sourced in interactive shells.  It
# should contain commands to set up aliases, functions,
# options, key bindings, etc.
#

# Set prompts
#PROMPT='[%n@%m]%~%# '    # default prompt
#RPROMPT=' %~'     # prompt for right side of screen

_src_etc_profile_d()
{
    # from zshrc, with ksh fixes
    if [[ ! -o login ]]; then # We're not a login shell
        for i in /etc/profile.d/*.sh; do
	    if [ -r "$i" ]; then
	        . $i
	    fi
        done
        unset i
    fi
}

pathmunge () {
case ":${PATH}:" in
*:"$1":*)
    ;;
*)
    if [ "$2" = "after" ]; then
        PATH=$PATH:$1
    else
        PATH=$1:$PATH
    fi
esac
}

_src_etc_profile_d

unset -f _src_etc_profile_d
unset -f pathmunge

# key bindings - make Delete, Home, End,... work
keybd_trap () {
  case ${.sh.edchar} in
    $'\e[1~') .sh.edchar=$'\001';; # Home = beginning-of-line
    $'\e[F')  .sh.edchar=$'\005';; # End = end-of-line
    $'\e[5~') .sh.edchar=$'\e>';; # PgUp = history-previous
    $'\e[6~') .sh.edchar=$'\e<';; # PgDn = history-next
    $'\e[3~') .sh.edchar=$'\004';; # Delete = delete-char
  esac
}
trap keybd_trap KEYBD

