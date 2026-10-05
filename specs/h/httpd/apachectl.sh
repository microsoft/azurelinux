#!/usr/bin/sh
#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

###
### NOTE: This is a replacement version of the "apachectl" script with
### some differences in behaviour to the version distributed with
### Apache httpd.  Please read the apachectl(8) man page for more
### information.
###

if [ "x$1" = "x-k" ]; then
    shift
fi

ACMD="$1"
ARGV="$@"
SVC='httpd.service'
HTTPD='@HTTPDBIN@'

if [ "x$2" != "x" ] ; then
    echo Passing arguments to httpd using apachectl is no longer supported.
    echo You can only start/stop/restart httpd using this script.
    echo To pass extra arguments to httpd, see the $SVC'(8)'
    echo man page.
    exit 1
fi

case $ACMD in
start|stop|restart|status)
    /usr/bin/systemctl --no-pager $ACMD $SVC
    ERROR=$?
    ;;
graceful)
    if /usr/bin/systemctl -q is-active $SVC; then
        /usr/bin/systemctl kill --signal=SIGUSR1 --kill-who=main $SVC
    else
        /usr/bin/systemctl start $SVC
    fi
    ERROR=$?
    ;;
graceful-stop)
    /usr/bin/systemctl kill --signal=SIGWINCH --kill-who=main $SVC
    ERROR=$?
    ;;
configtest|-t)
    $HTTPD -t
    ERROR=$?
    ;;
-v|-V)
    $HTTPD $ACMD
    ERROR=$?
    ;;
*)
    echo apachectl: The \"$ACMD\" option is not supported. 1>&2
    ERROR=2
    ;;
esac

exit $ERROR

