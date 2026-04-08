
# color-grep initialization

/usr/libexec/grepconf.sh -c
if ( $status == 1 ) then
    exit
endif

alias grep 'grep --color=auto'
alias egrep 'grep -E --color=auto'
alias fgrep 'grep -F --color=auto'
