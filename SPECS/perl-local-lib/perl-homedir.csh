# invoke local::lib

# default -- invoke local::lib for all users
setenv PERL_HOMEDIR 1

# load our configs, aka opportunities to set PERL_HOMEDIR=0
if (-f /etc/sysconfig/perl-homedir) then
	eval `sed -ne 's|^[[:blank:]]*\([^#=]\{1,\}\)=\([^=]*\)|setenv \1 \2;|p' /etc/sysconfig/perl-homedir`
endif
if (-f "$HOME/.perl-homedir") then
	eval `sed -ne 's|^[[:blank:]]*\([^#=]\{1,\}\)=\([^=]*\)|setenv \1 \2;|p' "$HOME/.perl-homedir"`
endif

alias perlll 'eval "`perl -Mlocal::lib`"'

# if system default
if ("x$PERL_HOMEDIR" == "x1") then
	eval "`perl -Mlocal::lib`"
endif

