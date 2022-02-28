#!/bin/bash
#
#	/etc/rc.d/init.d/dovecot
#
# Starts the dovecot daemon
#
# chkconfig: - 65 35
# description: Dovecot Imap Server
# processname: dovecot
# config: /etc/dovecot.conf
# config: /etc/sysconfig/dovecot
# pidfile: /var/run/dovecot/master.pid

### BEGIN INIT INFO
# Provides: dovecot
# Required-Start: $local_fs $network
# Required-Stop: $local_fs $network
# Should-Start: $remote_fs
# Should-Stop: $remote_fs
# Default-Start: 
# Default-Stop: 0 1 2 3 4 5 6
# Short-Description: start and stop Dovecot Imap server
# Description: Dovecot is an IMAP server for Linux/UNIX-like systems,
#              written with security primarily in mind.  It also contains
#              a small POP3 server.
### END INIT INFO

# Source function library.
. /etc/init.d/functions

if [ -f /etc/sysconfig/dovecot -a $UID -eq 0 ]; then
    . /etc/sysconfig/dovecot
fi

RETVAL=0
prog="Dovecot Imap"
exec="/usr/sbin/dovecot"
config="/etc/dovecot/dovecot.conf"
pidfile="/var/run/dovecot/master.pid"
lockfile="/var/lock/subsys/dovecot"

start() {
	[ $UID -eq 0 ] || exit 4
	[ -x $exec ] || exit 5
	[ -f $config ] || exit 6

        echo -n $"Starting $prog: "
	daemon --pidfile $pidfile $exec $OPTIONS
	RETVAL=$?
	[ $RETVAL -eq 0 ] && touch  $lockfile
	echo
}

stop() {
	[ $UID -eq 0 ] || exit 4
	echo -n $"Stopping $prog: "
	killproc -p $pidfile $exec
	RETVAL=$?
	[ $RETVAL -eq 0 ] && rm -f $lockfile
	echo
}

reload() {
	[ $UID -eq 0 ] || exit 4
	echo -n $"Reloading $prog: "
	killproc -p $pidfile $exec -HUP
	RETVAL=$?
	echo
}

#
#	See how we were called.
#
case "$1" in
  start)
	start
	;;
  stop)
	stop
	;;
  reload)
	reload
	;;
  force-reload|restart)
	stop
	sleep 1
	start
	RETVAL=$?
	;;
  condrestart|try-restart)
	if [ -f $lockfile ]; then
	    stop
	    sleep 3
	    start
	fi
	;;
  status)
	status -p $pidfile $exec
	RETVAL=$?
	;;
  *)
	echo $"Usage: $0 {condrestart|try-restart|start|stop|restart|reload|force-reload|status}"
	RETVAL=2
	[ "$1" = 'usage' ] && RETVAL=0
esac

exit $RETVAL

