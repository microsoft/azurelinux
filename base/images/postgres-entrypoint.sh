#!/bin/bash

set -Eeuo pipefail

file_env() {
    local name="$1"
    local default_value="${2:-}"
    local file_name="${name}_FILE"

    if [[ -n "${!name:-}" && -n "${!file_name:-}" ]]; then
        echo "ERROR: ${name} and ${file_name} are mutually exclusive" >&2
        exit 1
    fi

    if [[ -n "${!file_name:-}" ]]; then
        [[ -r "${!file_name}" ]] || {
            echo "ERROR: cannot read ${file_name} path: ${!file_name}" >&2
            exit 1
        }
        printf -v "${name}" '%s' "$(< "${!file_name}")"
    elif [[ -z "${!name:-}" ]]; then
        printf -v "${name}" '%s' "${default_value}"
    fi

    export "${name}"
    unset "${file_name}"
}

as_postgres() {
    if (( EUID == 0 )); then
        env HOME=/var/lib/pgsql USER=postgres LOGNAME=postgres \
            setpriv --reuid=postgres --regid=postgres --init-groups -- "$@"
    else
        env HOME=/var/lib/pgsql USER=postgres LOGNAME=postgres "$@"
    fi
}

file_env POSTGRES_PASSWORD
file_env POSTGRES_USER postgres
file_env POSTGRES_DB "${POSTGRES_USER}"

PGDATA="${PGDATA:-/var/lib/pgsql/data}"
if [[ "${PGDATA}" != /* ]]; then
    echo "ERROR: PGDATA must be an absolute path: ${PGDATA}" >&2
    exit 1
fi
PGDATA="$(realpath -m -- "${PGDATA}")"
case "${PGDATA}" in
    / | /bin | /boot | /dev | /etc | /home | /lib | /lib64 | /media | /mnt | /opt | /proc | /root | /run | /sbin | /srv | /sys | /tmp | /usr | /var | /var/lib | /var/lib/pgsql)
        echo "ERROR: refusing unsafe PGDATA path: ${PGDATA}" >&2
        exit 1
        ;;
esac

POSTGRES_HOST_AUTH_METHOD="${POSTGRES_HOST_AUTH_METHOD:-scram-sha-256}"
POSTGRES_SOCKET_DIR="/var/lib/pgsql/run"
export PGDATA

case "${POSTGRES_HOST_AUTH_METHOD}" in
    md5 | scram-sha-256 | trust) ;;
    *)
        echo "ERROR: unsupported POSTGRES_HOST_AUTH_METHOD: ${POSTGRES_HOST_AUTH_METHOD}" >&2
        exit 1
        ;;
esac

if (( EUID == 0 )); then
    install -d -m 0700 -o postgres -g postgres "${PGDATA}"
    install -d -m 3775 -o postgres -g postgres "${POSTGRES_SOCKET_DIR}"
    find "${PGDATA}" \( ! -user postgres -o ! -group postgres \) \
        -exec chown -h postgres:postgres {} +
else
    if [[ ! -d "${PGDATA}" || ! -w "${PGDATA}" ]]; then
        echo "ERROR: PGDATA must exist and be writable by postgres: ${PGDATA}" >&2
        echo "Use a named volume or pre-own the bind mount for the postgres user." >&2
        exit 1
    fi
    if [[ ! -d "${POSTGRES_SOCKET_DIR}" || ! -w "${POSTGRES_SOCKET_DIR}" ]]; then
        echo "ERROR: ${POSTGRES_SOCKET_DIR} is not writable by postgres" >&2
        exit 1
    fi
fi

password_file=""
temp_server_started=false
initializing_marker="${PGDATA}/.azurelinux-initializing"
initialized_marker="${PGDATA}/.azurelinux-initialized"
cleanup() {
    if [[ "${temp_server_started}" == "true" ]]; then
        as_postgres pg_ctl -D "${PGDATA}" -m fast -w stop || true
    fi
    [[ -z "${password_file}" ]] || rm -f "${password_file}"
}
trap cleanup EXIT

if [[ ! -s "${PGDATA}/PG_VERSION" ]]; then
    if [[ -z "${POSTGRES_PASSWORD}" && "${POSTGRES_HOST_AUTH_METHOD}" != "trust" ]]; then
        echo "ERROR: POSTGRES_PASSWORD is required for a new database" >&2
        echo "Set POSTGRES_HOST_AUTH_METHOD=trust only for explicitly unsecured deployments." >&2
        exit 1
    fi

    initdb_args=(
        --pgdata="${PGDATA}"
        --username="${POSTGRES_USER}"
        --encoding=UTF8
        --locale=C
        --auth-local=trust
        --auth-host="${POSTGRES_HOST_AUTH_METHOD}"
    )

    if [[ -n "${POSTGRES_PASSWORD}" ]]; then
        password_file="$(mktemp)"
        printf '%s\n' "${POSTGRES_PASSWORD}" > "${password_file}"
        chmod 0600 "${password_file}"
        if (( EUID == 0 )); then
            chown postgres:postgres "${password_file}"
        fi
        initdb_args+=(--pwfile="${password_file}")
    fi

    as_postgres initdb "${initdb_args[@]}"
    as_postgres touch "${initializing_marker}"
    echo "host all all all ${POSTGRES_HOST_AUTH_METHOD}" >> "${PGDATA}/pg_hba.conf"
fi

if [[ ! -e "${initialized_marker}" ]]; then
    as_postgres touch "${initializing_marker}"
    as_postgres pg_ctl \
        -D "${PGDATA}" \
        -o "-c listen_addresses='' -c unix_socket_directories=${POSTGRES_SOCKET_DIR}" \
        -w start
    temp_server_started=true

    if [[ "${POSTGRES_DB}" != "postgres" ]]; then
        database_exists=false
        while IFS='|' read -r database_name _; do
            if [[ "${database_name}" == "${POSTGRES_DB}" ]]; then
                database_exists=true
                break
            fi
        done < <(
            as_postgres psql \
                --host="${POSTGRES_SOCKET_DIR}" \
                --username="${POSTGRES_USER}" \
                --dbname=postgres \
                --tuples-only \
                --no-align \
                --command='\list'
        )
        if [[ "${database_exists}" != "true" ]]; then
            as_postgres createdb \
                --host="${POSTGRES_SOCKET_DIR}" \
                --username="${POSTGRES_USER}" \
                -- "${POSTGRES_DB}"
        fi
    fi

    as_postgres pg_ctl -D "${PGDATA}" -m fast -w stop
    temp_server_started=false
    as_postgres rm -f "${initializing_marker}"
    as_postgres touch "${initialized_marker}"
fi

trap - EXIT
cleanup
unset POSTGRES_PASSWORD

if (( EUID == 0 )); then
    exec env \
        HOME=/var/lib/pgsql \
        USER=postgres \
        LOGNAME=postgres \
        setpriv \
        --reuid=postgres \
        --regid=postgres \
        --init-groups \
        -- postgres \
        -D "${PGDATA}" \
        -c "listen_addresses=*" \
        -c "unix_socket_directories=${POSTGRES_SOCKET_DIR}"
else
    exec env \
        HOME=/var/lib/pgsql \
        USER=postgres \
        LOGNAME=postgres \
        postgres \
        -D "${PGDATA}" \
        -c "listen_addresses=*" \
        -c "unix_socket_directories=${POSTGRES_SOCKET_DIR}"
fi
