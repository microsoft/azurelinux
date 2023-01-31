#!/bin/false This script should be sourced by the other log-compilers
#;**********************************************************************;
# SPDX-License-Identifier: BSD-2-Clause
#
# Copyright (c) 2017 - 2020, Intel Corporation
# Copyright (c) 2018 - 2020, Fraunhofer SIT sponsored by Infineon Technologies AG
#
# All rights reserved.
#;**********************************************************************;
set -u

usage_error ()
{
    echo "$0: $*" >&2
    print_usage >&2
    exit 2
}
print_usage ()
{
    cat <<END
Usage:
    `basename "$0"` TEST-SCRIPT [TEST-SCRIPT-ARGUMENTS]
END
}
while test $# -gt 0; do
    case $1 in
    --help) print_usage; exit $?;;
    --) shift; break;;
    -*) usage_error "invalid option: '$1'";;
     *) break;;
    esac
    shift
done

OS=$(uname)
sock_tool="unknown"
sock_tool_params=""

if [ "$OS" == "Linux" ]; then
    sock_tool="ss"
    sock_tool_params="-lntp4"
elif [ "$OS" == "FreeBSD" ]; then
    sock_tool="sockstat"
    sock_tool_params="-l4"
fi

simulator_bin=""
INTEGRATION_TCTI=$1
TPM20TEST_DEVICE_FILE=""
TPM20TEST_TCTI_NAME=""
TPM20TEST_TCTI=""
TPM20TEST_SOCKET_PORT=""
TPM20TEST_SOCKET_ADDRESS=""
SIM_PORT_DATA=""

case ${INTEGRATION_TCTI} in
 "swtpm")
   simulator_bin="swtpm"
   TPM20TEST_TCTI_NAME="swtpm"
   TPM20TEST_SOCKET_ADDRESS="127.0.0.1"
   ;;
 "mssim")
   simulator_bin="tpm_server"
   TPM20TEST_TCTI_NAME="socket"
   TPM20TEST_SOCKET_ADDRESS="127.0.0.1"

   ;;
 "device")
   simulator_bin=""
   TPM20TEST_TCTI_NAME="device"
   DEVICE_FILE=$2
   TPM20TEST_DEVICE_FILE=${DEVICE_FILE:9}
   TPM20TEST_TCTI="${TPM20TEST_TCTI_NAME}:${TPM20TEST_DEVICE_FILE}"
   ;;
 *)
  echo "Wrong INTEGRATION_TCTI exiting.."
  exit 1;
  ;;
esac

# Verify the running shell and OS environment is sufficient to run these tests.
sanity_test ()
{
    # Check special file
    if [ ! -e /dev/urandom ]; then
        echo  "Missing file /dev/urandom; exiting"
        exit 1
    fi

    if [ -z "$(which ${sock_tool})" ]; then
        echo "ss not on PATH; exiting"
        exit 1
    fi

    if [[ ! -z ${simulator_bin} && -z "$(which ${simulator_bin})" ]]; then
        echo "${simulator_bin} not on PATH; exiting"
        exit 1
    fi
}

# This function takes a PID as a parameter and determines whether or not the
# process is currently running. If the daemon is running 0 is returned. Any
# other value indicates that the daemon isn't running.
daemon_status ()
{
    local pid=$1

    if [ $(kill -0 "${pid}" 2> /dev/null) ]; then
        echo "failed to detect running daemon with PID: ${pid}";
        return 1
    fi
    return 0
}

# This is a generic function to start a daemon, setup the environment
# variables, redirect output to a log file, store the PID of the daemon
# in a file and disconnect the daemon from the parent shell.
daemon_start ()
{
    local daemon_bin="$1"
    local daemon_opts="$2"
    local daemon_log_file="$3"
    local daemon_pid_file="$4"
    local daemon_env="$5"

    env ${daemon_env} stdbuf -o0 -e0 ${daemon_bin} ${daemon_opts} > ${daemon_log_file} 2>&1 &
    local ret=$?
    local pid=$!
    if [ ${ret} -ne 0 ]; then
        echo "failed to start daemon: \"${daemon_bin}\" with env: \"${daemon_env}\""
        exit ${ret}
    fi
    sleep 1
    daemon_status "${pid}"
    if [ $? -ne 0 ]; then
        echo "daemon died after successfully starting in background, check " \
             "log file: ${daemon_log_file}"
        return 1
    fi
    echo ${pid} > ${daemon_pid_file}
    disown ${pid}
    echo "successfully started daemon: ${daemon_bin} with PID: ${pid}"
    return 0
}
# function to start the simulator
# This also that we have a private place to store the NVChip file. Since we
# can't tell the simulator what to name this file we must generate a random
# directory under /tmp, move to this directory, start the simulator, then
# return to the old pwd.
simulator_start ()
{
    local sim_bin="$1"
    local sim_port="$2"
    local sim_log_file="$3"
    local sim_pid_file="$4"
    local sim_tmp_dir="$5"
    # simulator port is a random port between 1024 and 65535

    cd ${sim_tmp_dir}
    if [ "${INTEGRATION_TCTI}" == "mssim" ]; then
        daemon_start "${sim_bin}" "-port ${sim_port}" "${sim_log_file}" \
            "${sim_pid_file}" ""
    elif [ "${INTEGRATION_TCTI}" == "swtpm" ]; then
        daemon_start "${sim_bin}" "socket --tpm2 -p ${sim_port} --ctrl type=tcp,port=$((${sim_port}+1)) --log fd=1,level=5 --flags not-need-init --tpmstate dir=${sim_tmp_dir} --locality allow-set-locality" \
            "${sim_log_file}" "${sim_pid_file}" ""
    else
        cd -
	return -1
    fi

    local ret=$?
    cd -
    return $ret
}
# function to stop a running daemon
# This function takes a single parameter: a file containing the PID of the
# process to be killed. The PID is extracted and the daemon killed.
daemon_stop ()
{
    local pid_file=$1
    local pid=0
    local ret=0

    if [ ! -f ${pid_file} ]; then
        echo "failed to stop daemon, no pid file: ${pid_file}"
        return 1
    fi
    pid=$(cat ${pid_file})
    daemon_status "${pid}"
    ret=$?
    if [ ${ret} -ne 0 ]; then
        echo "failed to detect running daemon with PID: ${pid}";
        return ${ret}
    fi
    kill ${pid}
    ret=$?
    if [ ${ret} -ne 0 ]; then
        echo "failed to kill daemon process with PID: ${pid}"
    fi
    return ${ret}
}

# Once option processing is done, $@ should be the name of the test executable
# followed by all of the options passed to the test executable.
TEST_BIN=$(realpath "${@: -1}")
TEST_DIR=$(dirname "${@: -1}")
TEST_NAME=$(basename "${TEST_BIN}")

# start an instance of the simulator for the test, have it use a random port
SIM_LOG_FILE=${TEST_BIN}_simulator.log
SIM_PID_FILE=${TEST_BIN}_simulator.pid
SIM_TMP_DIR=$(mktemp -d /tmp/tpm_simulator_XXXXXX)
PORT_MIN=1024
PORT_MAX=65534
BACKOFF_FACTOR=2
BACKOFF_MAX=6
BACKOFF=1

try_simulator_start ()
{
    for i in $(seq ${BACKOFF_MAX}); do
        SIM_PORT_DATA=$(od -A n -N 2 -t u2 /dev/urandom | awk -v min=${PORT_MIN} -v max=${PORT_MAX} '{print ($1 % (max - min)) + min}')
        if [ $(expr ${SIM_PORT_DATA} % 2) -eq 1 ]; then
            SIM_PORT_DATA=$((${SIM_PORT_DATA}-1))
        fi
        SIM_PORT_CMD=$((${SIM_PORT_DATA}+1))
        echo "Starting simulator on port ${SIM_PORT_DATA}"
        simulator_start ${simulator_bin} ${SIM_PORT_DATA} ${SIM_LOG_FILE} ${SIM_PID_FILE} ${SIM_TMP_DIR}
        sleep 1 # give daemon time to bind to ports
        if [ ! -s ${SIM_PID_FILE} ] ; then
            echo "Simulator PID file is empty or missing. Giving up."
            exit 1
        fi
        PID=$(cat ${SIM_PID_FILE})
        echo "simulator PID: ${PID}";
        ${sock_tool} ${sock_tool_params} 2> /dev/null | grep "${PID}" | grep "${SIM_PORT_DATA}"
        ret_data=$?
        ${sock_tool} ${sock_tool_params} 2> /dev/null | grep "${PID}" | grep "${SIM_PORT_CMD}"
        ret_cmd=$?
        if test $ret_data -eq 0 && test $ret_cmd -eq 0; then
            echo "Simulator with PID ${PID} bound to port ${SIM_PORT_DATA} and " \
                 "${SIM_PORT_CMD} successfully.";
            break
        fi
        echo "Port conflict? Cleaning up PID: ${PID}"
        kill "${PID}"
        BACKOFF=$((${BACKOFF}*${BACKOFF_FACTOR}))
        echo "Failed to start simulator: port ${SIM_PORT_DATA} or " \
             "${SIM_PORT_CMD} probably in use. Retrying in ${BACKOFF}."
        sleep ${BACKOFF}
        if [ $i -eq 10 ]; then
            echo "Failed to start simulator after $i tries. Giving up.";
            exit 1
        fi
    done
}
