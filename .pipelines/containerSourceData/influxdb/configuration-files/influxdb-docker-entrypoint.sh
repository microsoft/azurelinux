#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

set -eo pipefail


## READ ME
##
## This script handles a few use-cases:
##   1. Running arbitrary shell commands other than `influxd`
##   2. Running subcommands of `influxd` other than `run`
##   3. Running `influxd run` with no auto-setup or auto-upgrade behavior
##   4. Running `influxd` with automated setup of a fresh 2.x DB
##   5. Running `influxd` with automated upgrade from a 1.x DB
##
## Use-cases 4 and 5 both optionally support running user-mounted scripts against the
## initialized DB to perform arbitrary setup logic.
##
## Use-case 1 runs as root (the container's default user). All other use-cases
## run as a non-root user. To support this, the script attempts to handle chown-ing
## the data directories specified in config/env/CLI flags. We do this even for
## use-case 2 so that commands like `influxd inspect` which modify files in the data
## directory don't create files will later be inaccessible to the main `influxd run`
## process.
##
## Use-case 4 requires booting a temporary instance of `influxd` so we can access the
## server's HTTP API. This script handles tracking the PID of that instance and shutting
## it down appropriately. The instance is booted on a port other than what's specified in
## config. We do this so:
##   1. We can ignore any TLS settings in config while performing initial setup calls
##   2. We don't have to worry about users accessing the DB before it's fully initialized
##
## Use-case 5 requires booting a temporary instance only when the user has mounted setup scripts.
## If no scripts are present, we can `upgrade` and then immediately boot the server on the
## user-configured port.


# Do our best to match the logging requested by the user running the container.
declare -rA LOG_LEVELS=([error]=0 [warn]=1 [info]=2 [debug]=3)
declare LOG_LEVEL=error

# Mimic the structured logging used by InfluxDB.
# Usage: log <level> <msg> [<key> <val>]...
function log () {
    local -r level=$1 msg=$2
    shift 2

    if [ "${LOG_LEVELS[${level}]}" -gt "${LOG_LEVELS[${LOG_LEVEL}]}" ]; then
        return
    fi

    local attrs='"system": "docker"'
    while [ "$#" -gt 1 ]; do
        attrs="${attrs}, \"$1\": \"$2\""
        shift 2
    done

    local -r logtime="$(date --utc +'%FT%T.%NZ')"
    1>&2 echo -e "${logtime}\t${level}\t${msg}\t{${attrs}}"
}

# Set the global log-level for the entry-point to match the config passed to influxd.
function set_global_log_level () {
    local level
    level="$(influxd print-config --key-name log-level "${@}")"
    if [ -z "${level}" ] || [ -z "${LOG_LEVELS[${level}]}" ]; then
        return 1
    fi
    LOG_LEVEL=${level}
}

# Look for standard config names in the volume configured in our Dockerfile.
declare -r CONFIG_VOLUME=/etc/influxdb
declare -ra CONFIG_NAMES=(config.json config.toml config.yaml config.yml)

# Search for a V2 config file, and export its path into the env for influxd to use.
function set_config_path () {
    local config_path=/etc/defaults/influxdb/config.yml

    if [ -n "$INFLUXD_CONFIG_PATH" ]; then
        config_path="${INFLUXD_CONFIG_PATH}"
    else
        for name in "${CONFIG_NAMES[@]}"; do
            if [ -f "${CONFIG_VOLUME}/${name}" ]; then
                config_path="${CONFIG_VOLUME}/${name}"
                break
            fi
        done
    fi

    export INFLUXD_CONFIG_PATH="${config_path}"
}

function set_data_paths () {
    BOLT_PATH="$(influxd print-config --key-name bolt-path "${@}")"
    ENGINE_PATH="$(influxd print-config --key-name engine-path "${@}")"
    export BOLT_PATH ENGINE_PATH
}

# Ensure all the data directories needed by influxd exist with the right permissions.
function create_directories () {
    log info "creating folders with the right permissions"
    local -r bolt_dir="$(dirname "${BOLT_PATH}")"
    local user
    user=$(id -u)

    if [ "$(id -u)" != 0 ]; then
        log warn "cannot create folders as non-root"
        return
    fi

    mkdir -p "${bolt_dir}" "${ENGINE_PATH}"
    chmod 700 "${bolt_dir}" "${ENGINE_PATH}" || :

    mkdir -p "${CONFIG_VOLUME}" || :
    chmod 775 "${CONFIG_VOLUME}" || :

    if [ ${user} = 0 ]; then
        find "${bolt_dir}" \! -user influxdb -exec chown influxdb '{}' +
        find "${ENGINE_PATH}" \! -user influxdb -exec chown influxdb '{}' +
        find "${CONFIG_VOLUME}" \! -user influxdb -exec chown influxdb '{}' +
    fi
}

# Read password and username from file to avoid unsecure env variables
if [ -n "${DOCKER_INFLUXDB_INIT_PASSWORD_FILE}" ]; then [ -e "${DOCKER_INFLUXDB_INIT_PASSWORD_FILE}" ] && DOCKER_INFLUXDB_INIT_PASSWORD=$(cat "${DOCKER_INFLUXDB_INIT_PASSWORD_FILE}") || echo "DOCKER_INFLUXDB_INIT_PASSWORD_FILE defined, but file not existing, skipping."; fi
if [ -n "${DOCKER_INFLUXDB_INIT_USERNAME_FILE}" ]; then [ -e "${DOCKER_INFLUXDB_INIT_USERNAME_FILE}" ] && DOCKER_INFLUXDB_INIT_USERNAME=$(cat "${DOCKER_INFLUXDB_INIT_USERNAME_FILE}") || echo "DOCKER_INFLUXDB_INIT_USERNAME_FILE defined, but file not existing, skipping."; fi

# List of env vars required to auto-run setup or upgrade processes.
declare -ra REQUIRED_INIT_VARS=(DOCKER_INFLUXDB_INIT_USERNAME DOCKER_INFLUXDB_INIT_PASSWORD DOCKER_INFLUXDB_INIT_ORG DOCKER_INFLUXDB_INIT_BUCKET)

# Ensure all env vars required to run influx setup or influxd upgrade are set in the env.
function ensure_init_vars_set () {
    local missing_some=0
    for var in "${REQUIRED_INIT_VARS[@]}"; do
        if [ -z "${!var}" ]; then
            log error "missing parameter, cannot init InfluxDB" parameter ${var}
            missing_some=1
        fi
    done
    if [ ${missing_some} = 1 ]; then
        exit 1
    fi
}

# If exiting on error, delete all bolt and engine files.
# If we didn't do this, the container would see the boltdb file on reboot and assume
# the DB is already full set up.
function cleanup_influxd () {
    log warn "cleaning bolt and engine files to prevent conflicts on retry" bolt_path "${BOLT_PATH}" engine_path "${ENGINE_PATH}"
    rm -rf "${BOLT_PATH}" "${ENGINE_PATH}/"*
}

# Upgrade V1 data into the V2 format using influxd upgrade.
# The process will use either a V1 config file or a V1 data dir to drive
# the upgrade, with precedence order:
#   1. Config file pointed to by DOCKER_INFLUXDB_INIT_UPGRADE_V1_CONFIG env var
#   2. Data dir pointed to by DOCKER_INFLUXDB_INIT_UPGRADE_V1_DIR env var
#   3. Config file at /etc/influxdb/influxdb.conf
#   4. Data dir at /var/lib/influxdb
function upgrade_influxd () {
    local -a upgrade_args=(
        --force
        --username "${DOCKER_INFLUXDB_INIT_USERNAME}"
        --password "${DOCKER_INFLUXDB_INIT_PASSWORD}"
        --org "${DOCKER_INFLUXDB_INIT_ORG}"
        --bucket "${DOCKER_INFLUXDB_INIT_BUCKET}"
        --v2-config-path "${CONFIG_VOLUME}/config.toml"
        --influx-configs-path "${INFLUX_CONFIGS_PATH}"
        --continuous-query-export-path "${CONFIG_VOLUME}/v1-cq-export.txt"
        --log-path "${CONFIG_VOLUME}/upgrade.log"
        --log-level "${LOG_LEVEL}"
        --bolt-path "${BOLT_PATH}"
        --engine-path "${ENGINE_PATH}"
        --overwrite-existing-v2
    )
    if [ -n "${DOCKER_INFLUXDB_INIT_RETENTION}" ]; then
        upgrade_args=("${upgrade_args[@]}" --retention "${DOCKER_INFLUXDB_INIT_RETENTION}")
    fi
    if [ -n "${DOCKER_INFLUXDB_INIT_ADMIN_TOKEN}" ]; then
        upgrade_args=("${upgrade_args[@]}" --token "${DOCKER_INFLUXDB_INIT_ADMIN_TOKEN}")
    fi

    if [[ -n "${DOCKER_INFLUXDB_INIT_UPGRADE_V1_CONFIG}" && -f "${DOCKER_INFLUXDB_INIT_UPGRADE_V1_CONFIG}" ]]; then
        upgrade_args=("${upgrade_args[@]}" --config-file "${DOCKER_INFLUXDB_INIT_UPGRADE_V1_CONFIG}")
    elif [[ -n "${DOCKER_INFLUXDB_INIT_UPGRADE_V1_DIR}" && -d "${DOCKER_INFLUXDB_INIT_UPGRADE_V1_DIR}" ]]; then
        upgrade_args=("${upgrade_args[@]}" --v1-dir "${DOCKER_INFLUXDB_INIT_UPGRADE_V1_DIR}")
    elif [ -f /etc/influxdb/influxdb.conf ]; then
        upgrade_args=("${upgrade_args[@]}" --config-file /etc/influxdb/influxdb.conf)
    elif [ -d /var/lib/influxdb ]; then
        upgrade_args=("${upgrade_args[@]}" --v1-dir /var/lib/influxdb)
    else
        log error "failed to autodetect usable V1 config or data dir, aborting upgrade"
        exit 1
    fi

    influxd upgrade "${upgrade_args[@]}"

    # Reset global influxd config to pick up new file written by the upgrade process.
    set_config_path
}

# Ping influxd until it responds or crashes.
# Used to block execution until the server is ready to process setup requests.
function wait_for_influxd () {
    local -r influxd_pid=$1
    local ping_count=0
    while kill -0 "${influxd_pid}" && [ ${ping_count} -lt ${INFLUXD_INIT_PING_ATTEMPTS} ]; do
        sleep 1
        log info "pinging influxd..." ping_attempt ${ping_count}
        ping_count=$((ping_count+1))
        if influx ping &> /dev/null; then
            log info "got response from influxd, proceeding" total_pings ${ping_count}
            return
        fi
    done
    if [ ${ping_count} -eq ${INFLUXD_INIT_PING_ATTEMPTS} ]; then
        log error "influxd took too long to start up" total_pings ${ping_count}
    else
        log error "influxd crashed during startup" total_pings ${ping_count}
    fi
    exit 1
}

# Create an initial user/org/bucket in the DB using the influx CLI.
function setup_influxd () {
    local -a setup_args=(
        --force
        --username "${DOCKER_INFLUXDB_INIT_USERNAME}"
        --password "${DOCKER_INFLUXDB_INIT_PASSWORD}"
        --org "${DOCKER_INFLUXDB_INIT_ORG}"
        --bucket "${DOCKER_INFLUXDB_INIT_BUCKET}"
        --name "${DOCKER_INFLUXDB_INIT_CLI_CONFIG_NAME}"
    )
    if [ -n "${DOCKER_INFLUXDB_INIT_RETENTION}" ]; then
        setup_args=("${setup_args[@]}" --retention "${DOCKER_INFLUXDB_INIT_RETENTION}")
    fi
    if [ -n "${DOCKER_INFLUXDB_INIT_ADMIN_TOKEN}" ]; then
        setup_args=("${setup_args[@]}" --token "${DOCKER_INFLUXDB_INIT_ADMIN_TOKEN}")
    fi

    influx setup "${setup_args[@]}"
}

# Get the IDs of the initial user/org/bucket created during setup, and export them into the env.
# We do this to help with arbitrary user scripts, since many influx CLI commands only take IDs.
function set_init_resource_ids () {
    DOCKER_INFLUXDB_INIT_USER_ID="$(influx user list -n "${DOCKER_INFLUXDB_INIT_USER}" --hide-headers | cut -f 1)"
    DOCKER_INFLUXDB_INIT_ORG_ID="$(influx org list -n "${DOCKER_INFLUXDB_INIT_ORG}" --hide-headers | cut -f 1)"
    DOCKER_INFLUXDB_INIT_BUCKET_ID="$(influx bucket list -n "${DOCKER_INFLUXDB_INIT_BUCKET}" --hide-headers | cut -f 1)"
    export DOCKER_INFLUXDB_INIT_USER_ID DOCKER_INFLUXDB_INIT_ORG_ID DOCKER_INFLUXDB_INIT_BUCKET_ID
}

# Allow users to mount arbitrary startup scripts into the container,
# for execution after initial setup/upgrade.
declare -r USER_SCRIPT_DIR=/docker-entrypoint-initdb.d

# Check if user-defined setup scripts have been mounted into the container.
function user_scripts_present () {
    if [ ! -d ${USER_SCRIPT_DIR} ]; then
        return 1
    fi
    test -n "$(find ${USER_SCRIPT_DIR} -name "*.sh" -type f -executable)"
}

# Execute all shell files mounted into the expected path for user-defined startup scripts.
function run_user_scripts () {
    if [ -d ${USER_SCRIPT_DIR} ]; then
        log info "Executing user-provided scripts" script_dir ${USER_SCRIPT_DIR}
        run-parts ${USER_SCRIPT_DIR}
    fi
}

# Helper used to propagate signals received during initialization to the influxd
# process running in the background.
function handle_signal () {
    kill -${1} ${2}
    wait ${2}
}

# Perform initial setup on the InfluxDB instance, either by setting up fresh metadata
# or by upgrading existing V1 data.
function init_influxd () {
    if [[ "${DOCKER_INFLUXDB_INIT_MODE}" != setup && "${DOCKER_INFLUXDB_INIT_MODE}" != upgrade ]]; then
        log error "found invalid DOCKER_INFLUXDB_INIT_MODE, valid values are 'setup' and 'upgrade'" DOCKER_INFLUXDB_INIT_MODE "${DOCKER_INFLUXDB_INIT_MODE}"
        exit 1
    fi
    ensure_init_vars_set
    trap "cleanup_influxd" EXIT

    # The upgrade process needs to run before we boot the server, otherwise the
    # boltdb file will be generated and cause conflicts.
    if [ "${DOCKER_INFLUXDB_INIT_MODE}" = upgrade ]; then
        upgrade_influxd
    fi

    # Short-circuit if using upgrade mode and user didn't define any custom scripts,
    # to save startup time from booting & shutting down the server.
    if [ "${DOCKER_INFLUXDB_INIT_MODE}" = upgrade ] && ! user_scripts_present; then
        trap - EXIT
        return
    fi

    local -r final_bind_addr="$(influxd print-config --key-name http-bind-address "${@}")"
    local -r init_bind_addr=":${INFLUXD_INIT_PORT}"
    if [ "${init_bind_addr}" = "${final_bind_addr}" ]; then
      log warn "influxd setup binding to same addr as final config, server will be exposed before ready" addr "${init_bind_addr}"
    fi
    local final_host_scheme="http"
    if [ "$(influxd print-config --key-name tls-cert "${@}")" != '""' ] && [ "$(influxd print-config --key-name tls-key "${@}")" != '""' ]; then
        final_host_scheme="https"
    fi

    # Generate a config file with a known HTTP port, and TLS disabled.
    local -r init_config=/tmp/config.yml
    influxd print-config "${@}" | \
        sed -e "s#${final_bind_addr}#${init_bind_addr}#" -e '/^tls/d' > \
        "${init_config}"

    # Start influxd in the background.
    log info "booting influxd server in the background"
    INFLUXD_CONFIG_PATH="${init_config}" INFLUXD_HTTP_BIND_ADDRESS="${init_bind_addr}" INFLUXD_TLS_CERT='' INFLUXD_TLS_KEY='' influxd &
    local -r influxd_init_pid="$!"
    trap "handle_signal TERM ${influxd_init_pid}" TERM
    trap "handle_signal INT ${influxd_init_pid}" INT

    export INFLUX_HOST="http://localhost:${INFLUXD_INIT_PORT}"
    wait_for_influxd "${influxd_init_pid}"

    # Use the influx CLI to create an initial user/org/bucket.
    if [ "${DOCKER_INFLUXDB_INIT_MODE}" = setup ]; then
        setup_influxd
    fi

    set_init_resource_ids
    run_user_scripts

    log info "initialization complete, shutting down background influxd"
    kill -TERM "${influxd_init_pid}"
    wait "${influxd_init_pid}" || true
    trap - EXIT INT TERM

    # Rewrite the ClI configs to point at the server's final HTTP address.
    local -r final_port="$(echo "${final_bind_addr}" | sed -E 's#[^:]*:(.*)#\1#')"
    sed -i "s#http://localhost:${INFLUXD_INIT_PORT}#${final_host_scheme}://localhost:${final_port}#g" "${INFLUX_CONFIGS_PATH}"
}

# Check if the --help or -h flag is set in a list of CLI args.
function check_help_flag () {
  for arg in "${@}"; do
      if [ "${arg}" = --help ] || [ "${arg}" = -h ]; then
          return 0
      fi
  done
  return 1
}

function main () {
    # Ensure INFLUXD_CONFIG_PATH is set.
    # We do this even if we're not running the main influxd server so subcommands
    # (i.e. print-config) still find the right config values.
    set_config_path

    local run_influxd=false
    if [[ $# = 0 || "$1" = run || "${1:0:1}" = '-' ]]; then
        run_influxd=true
    elif [[ "$1" = influxd && ($# = 1 || "$2" = run || "${2:0:1}" = '-') ]]; then
        run_influxd=true
        shift 1
    fi

    if ! ${run_influxd}; then
      exec "${@}"
    fi

    if [ "$1" = run ]; then
        shift 1
    fi

    if ! check_help_flag "${@}"; then
        # Configure logging for our wrapper.
        set_global_log_level "${@}"
        # Configure data paths used across functions.
        set_data_paths "${@}"
        # Ensure volume directories exist w/ correct permissions.
        create_directories
    fi

    if [ -f "${BOLT_PATH}" ]; then
        log info "found existing boltdb file, skipping setup wrapper" bolt_path "${BOLT_PATH}"
    elif [ -z "${DOCKER_INFLUXDB_INIT_MODE}" ]; then
        log warn "boltdb not found at configured path, but DOCKER_INFLUXDB_INIT_MODE not specified, skipping setup wrapper" bolt_path "${bolt_path}"
    else
        init_influxd "${@}"
        # Set correct permission on volume directories again. This is necessary so that if the container was run as the
        # root user, the files from the automatic upgrade/initialization will be correctly set when stepping down to the
        # influxdb user.
        create_directories
    fi

    if [ "$(id -u)" = 0 ]; then
        exec setpriv --reuid=influxdb --regid=influxdb --init-groups --inh-caps=-all "$BASH_SOURCE" "$@"
    fi

    # Run influxd.
    exec influxd "$@"
}

main "$@"