#!/bin/sh
#
# Turns on or off the nss-sysinit module db by editing the
# global PKCS #11 congiguration file. Displays the status.
#
# This script can be invoked by the user as super user.
# It is invoked at nss-sysinit post install time with argument on.
#
usage()
{
  cat <<EOF
Usage: setup-nsssysinit [on|off]
  on     - turns on nsssysinit
  off    - turns off nsssysinit
  status - reports whether nsssysinit is turned on or off
EOF
  exit $1
}

# validate
if [ $# -eq 0 ]; then
  usage 1 1>&2
fi

# the system-wide configuration file
p11conf="/etc/pki/nssdb/pkcs11.txt"
# must exist, otherwise report it and exit with failure
if [ ! -f $p11conf ]; then
  echo "Could not find ${p11conf}"
  exit 1
fi

# check if nsssysinit is currently enabled or disabled
sysinit_enabled()
{
  grep -q '^library=libnsssysinit' ${p11conf}
}

umask 022
case "$1" in
  on | ON )
    if sysinit_enabled; then 
      exit 0 
    fi
    cat ${p11conf} | \
    sed -e 's/^library=$/library=libnsssysinit.so/' \
        -e '/^NSS/s/\(Flags=internal\)\(,[^m]\)/\1,moduleDBOnly\2/' > \
        ${p11conf}.on
    mv ${p11conf}.on ${p11conf}
    ;;
  off | OFF )
    if ! sysinit_enabled; then
      exit 0
    fi
    cat ${p11conf} | \
    sed -e 's/^library=libnsssysinit.so/library=/' \
        -e '/^NSS/s/Flags=internal,moduleDBOnly/Flags=internal/' > \
        ${p11conf}.off
    mv ${p11conf}.off ${p11conf}
    ;;
  status )
    echo -n 'NSS sysinit is '
    sysinit_enabled && echo 'enabled' || echo 'disabled'
    ;;
  * )
    usage 1 1>&2
    ;;
esac
