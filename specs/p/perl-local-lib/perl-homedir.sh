# invoke local::lib

# default -- invoke local::lib for all users
PERL_HOMEDIR=1

# load our configs, aka opportunities to set PERL_HOMEDIR=0
[ -f /etc/sysconfig/perl-homedir ] && . /etc/sysconfig/perl-homedir
[ -f $HOME/.perl-homedir         ] && . $HOME/.perl-homedir

alias perlll='eval `perl -Mlocal::lib`'

# if system default
if [ "x$PERL_HOMEDIR" = "x1" ] ; then

    eval `perl -Mlocal::lib`
fi
