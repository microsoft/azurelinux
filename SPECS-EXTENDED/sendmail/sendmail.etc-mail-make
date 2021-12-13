#!/bin/sh
# Generate db and cf files if necessary. This used to be handled by
# /etc/mail/Makefile.

teste() {
  if ! test -e "$1"; then
    echo "$1 doesn't exist"
    exit 2
  fi
}

makedb() {
  teste "${1%.db}"

  if [ -z "$SM_FORCE_DBREBUILD" ]; then
    test "${1%.db}" -nt "$1" || return 0
  fi

  if [ "$1" = userdb.db ]; then
    makemap btree "$1" < "${1%.db}"
  else
    makemap hash "$1" < "${1%.db}"
  fi
}

makealiasesdb() {
  uptodate=1

  if [ -z "$SM_FORCE_DBREBUILD" ]; then
    files=$(grep '^O AliasFile=' sendmail.cf |
      while read a; do echo ${a#*=}; done)

    for a in $files; do
      if [ "$a" = /etc/aliases ]; then
        # /etc/aliases.db may be used by other MTA, make sure nothing
        # has touched it since our last newaliases call
        test "$a" -nt "${a}.db" ||
          test aliasesdb-stamp -nt "${a}.db" ||
          test aliasesdb-stamp -ot "${a}.db" || continue
      else
        test "$a" -nt "${a}.db" || continue
      fi

      uptodate=0
      break
    done
  else
    uptodate=0
  fi

  [ $uptodate = 1 ] && return 0

  # check if alternatives is configured to sendmail
  if [ "$(readlink -e /usr/bin/newaliases)" = /usr/sbin/sendmail.sendmail ]
  then
    /usr/bin/newaliases > /dev/null
    touch -r /etc/aliases.db aliasesdb-stamp 2> /dev/null
  else
    rm -f aliasesdb-stamp
  fi
}

makecf() {
  mc=${1%.cf}.mc

  teste "$mc"

  if [ -z "$SM_FORCE_CFREBUILD" ]; then
    test "$mc" -nt "$1" || return 0
  fi

  if test -f /usr/share/sendmail-cf/m4/cf.m4; then
    umask 022
    [ -e "$1" ] && mv -f "$1" "$1".bak
    m4 "$mc" > "$1"
  else
    echo "WARNING: '$mc' is modified. Please install package sendmail-cf to update your configuration."
    exit 15
  fi
}

makeall() {
  # These could be used by sendmail, but are not part of the default install.
  # To use them you will have to generate your own sendmail.cf with
  # FEATURE('whatever')
  test -f bitdomain && makedb bitdomain.db
  test -f uudomain && makedb uudomain.db
  test -f genericstable && makedb genericstable.db
  test -f userdb && makedb userdb.db
  test -f authinfo && makedb authinfo.db

  makedb virtusertable.db
  makedb access.db
  makedb domaintable.db
  makedb mailertable.db

  makecf sendmail.cf
  makecf submit.cf
}

cd /etc/mail || exit 1

[ $# -eq 0 ] && makeall

for target; do
  case "$target" in
    *.db)
      makedb "$target"
      ;;
    *.cf)
      makecf "$target"
      ;;
    all)
      makeall
      ;;
    aliases)
      makealiasesdb
      ;;
    clean)
      rm -f *.db *~ aliasesdb-stamp
      ;;
    start|stop|restart)
      service sendmail "$target"
      ;;
    *)
      echo "Don't know how to make $target"
      exit 2
  esac
done
