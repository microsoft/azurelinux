# color-grep initialization

/usr/libexec/grepconf.sh -c || return

alias grep='grep --color=auto' 2>/dev/null
alias egrep='grep -E --color=auto' 2>/dev/null
alias fgrep='grep -F --color=auto' 2>/dev/null
