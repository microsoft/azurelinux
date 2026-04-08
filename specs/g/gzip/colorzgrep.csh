test -f /usr/libexec/grepconf.sh
if ( $status == 1 ) exit

/usr/libexec/grepconf.sh -c
if ( $status == 1 ) exit

alias zgrep 'zgrep --color=auto'
alias zfgrep 'zfgrep --color=auto'
alias zegrep 'zegrep --color=auto'
