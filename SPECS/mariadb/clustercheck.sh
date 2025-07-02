#!/bin/bash
#
# Script to make a proxy (ie HAProxy) capable of monitoring Galera cluster nodes properly
#
# Author: Olaf van Zandwijk <olaf.vanzandwijk@nedap.com>
# Author: Raghavendra Prabhu <raghavendra.prabhu@percona.com>
# Author: Ryan O'Hara <rohara@redhat.com>
#
# Documentation and download: https://github.com/olafz/percona-clustercheck
#
# Based on the original script from Unai Rodriguez
#

if [ -f @INSTALL_SYSCONFDIR@/sysconfig/clustercheck ]; then
    . @INSTALL_SYSCONFDIR@/sysconfig/clustercheck
fi

MYSQL_USERNAME="${MYSQL_USERNAME-clustercheckuser}"
MYSQL_PASSWORD="${MYSQL_PASSWORD-clustercheckpassword!}"
MYSQL_HOST="${MYSQL_HOST:-127.0.0.1}"
MYSQL_PORT="${MYSQL_PORT:-3306}"
ERR_FILE="${ERR_FILE:-/dev/null}"
AVAILABLE_WHEN_DONOR=${AVAILABLE_WHEN_DONOR:-0}
AVAILABLE_WHEN_READONLY=${AVAILABLE_WHEN_READONLY:-1}
DEFAULTS_EXTRA_FILE=${DEFAULTS_EXTRA_FILE:-@INSTALL_SYSCONFDIR@/my.cnf}

#Timeout exists for instances where mysqld may be hung
TIMEOUT=10

if [[ -r $DEFAULTS_EXTRA_FILE ]];then
    MYSQL_CMDLINE="mysql --defaults-extra-file=$DEFAULTS_EXTRA_FILE -nNE \
                    --connect-timeout=$TIMEOUT \
                    --user=${MYSQL_USERNAME} --password=${MYSQL_PASSWORD} \
                    --host=${MYSQL_HOST} --port=${MYSQL_PORT}"
else
    MYSQL_CMDLINE="mysql -nNE --connect-timeout=$TIMEOUT \
                    --user=${MYSQL_USERNAME} --password=${MYSQL_PASSWORD} \
                    --host=${MYSQL_HOST} --port=${MYSQL_PORT}"
fi
#
# Perform the query to check the wsrep_local_state
#
WSREP_STATUS=$($MYSQL_CMDLINE -e "SHOW STATUS LIKE 'wsrep_local_state';" \
    2>${ERR_FILE} | tail -1 2>>${ERR_FILE})

if [[ "${WSREP_STATUS}" == "4" ]] || [[ "${WSREP_STATUS}" == "2" && ${AVAILABLE_WHEN_DONOR} == 1 ]]
then
    # Check only when set to 0 to avoid latency in response.
    if [[ $AVAILABLE_WHEN_READONLY -eq 0 ]];then
        READ_ONLY=$($MYSQL_CMDLINE -e "SHOW GLOBAL VARIABLES LIKE 'read_only';" \
                    2>${ERR_FILE} | tail -1 2>>${ERR_FILE})

        if [[ "${READ_ONLY}" == "ON" ]];then
            # Galera cluster node local state is 'Synced', but it is in
            # read-only mode. The variable AVAILABLE_WHEN_READONLY is set to 0.
            # => return HTTP 503
            # Shell return-code is 1
            echo -en "HTTP/1.1 503 Service Unavailable\r\n"
            echo -en "Content-Type: text/plain\r\n"
            echo -en "Connection: close\r\n"
            echo -en "Content-Length: 35\r\n"
            echo -en "\r\n"
            echo -en "Galera cluster node is read-only.\r\n"
            sleep 0.1
            exit 1
        fi
    fi
    # Galera cluster node local state is 'Synced' => return HTTP 200
    # Shell return-code is 0
    echo -en "HTTP/1.1 200 OK\r\n"
    echo -en "Content-Type: text/plain\r\n"
    echo -en "Connection: close\r\n"
    echo -en "Content-Length: 32\r\n"
    echo -en "\r\n"
    echo -en "Galera cluster node is synced.\r\n"
    sleep 0.1
    exit 0
else
    # Galera cluster node local state is not 'Synced' => return HTTP 503
    # Shell return-code is 1
    echo -en "HTTP/1.1 503 Service Unavailable\r\n"
    echo -en "Content-Type: text/plain\r\n"
    echo -en "Connection: close\r\n"
    echo -en "Content-Length: 36\r\n"
    echo -en "\r\n"
    echo -en "Galera cluster node is not synced.\r\n"
    sleep 0.1
    exit 1
fi
