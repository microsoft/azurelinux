# Workload container images

Azure Linux workload containers package a single application or runtime with
an OCI default command. Unlike `container-base`, these images are intended to
run directly rather than serve as general-purpose build bases.

The workload images run as dedicated non-root users and do not include DNF,
RPM, or repository configuration. Use `container-base` when runtime package
installation is required.

| Image | Default command | Notes |
| --- | --- | --- |
| `microsoft/azurelinux/workload/busybox:4.0` | `/usr/sbin/busybox sh` | Minimal BusyBox shell environment |
| `microsoft/azurelinux/workload/nginx:4.0` | `/usr/sbin/nginx -c /etc/nginx/nginx-workload.conf -g "daemon off;"` | Runs nginx as `nginx` on port 8080 |
| `microsoft/azurelinux/workload/postgres:4.0` | `/usr/local/bin/postgres-entrypoint.sh` | Initializes an empty data directory, then starts PostgreSQL |
| `microsoft/azurelinux/workload/telegraf:4.0` | `/usr/bin/telegraf` | Requires a valid configuration supplied at runtime |
| `microsoft/azurelinux/workload/python:4.0` | `/usr/bin/python3` | Starts the Python interpreter |
| `microsoft/azurelinux/workload/nodejs:4.0` | `/usr/bin/node` | Starts the Node.js interpreter |
| `microsoft/azurelinux/workload/pytorch:4.0` | `/usr/bin/python3` | Starts Python with PyTorch installed |

## nginx

The nginx image listens on unprivileged port 8080:

```bash
podman run --rm --publish 8080:8080 \
  microsoft/azurelinux/workload/nginx:4.0
```

## Telegraf configuration

The Telegraf image follows the upstream container convention: callers supply
a configuration file at `/etc/telegraf/telegraf.conf`. The configuration must
enable at least one input and one output plugin.

For example, create `telegraf.conf`:

```toml
[[inputs.cpu]]

[[outputs.file]]
  files = ["stdout"]
```

Then mount it read-only when starting the container:

```bash
podman run --rm \
  --volume "$PWD/telegraf.conf:/etc/telegraf/telegraf.conf:ro,Z" \
  microsoft/azurelinux/workload/telegraf:4.0
```

Telegraf configuration can reference environment variables such as
`${INFLUX_TOKEN}`. Pass those values with the container runtime's environment
options rather than storing credentials in the image or configuration file.

## PostgreSQL initialization

The PostgreSQL image initializes an empty `PGDATA` directory before starting
the server. A new database requires `POSTGRES_PASSWORD`; `POSTGRES_USER` and
`POSTGRES_DB` default to `postgres`. The corresponding `_FILE` variables can
read these values from mounted secret files.

During initialization, the entrypoint adds a host authentication rule using
`POSTGRES_HOST_AUTH_METHOD`. PostgreSQL listens on all interfaces, so other
containers on the same container network can connect to port 5432 using the
configured user, password, and database. `PGDATA` must be an absolute path and
cannot point at a system directory whose recursive ownership change could
damage the container.

Create a private network and mount `/var/lib/pgsql/data` to preserve the
database. Named volumes are initialized with the correct ownership. For a bind
mount, pre-own the directory for the image's `postgres` user (UID 26), or use
Podman's `:U` volume option to shift ownership:

```bash
podman network create postgres-app
printf '%s\n' 'replace-with-a-strong-password' \
  | podman secret create postgres-password -

podman run --detach \
  --name postgres \
  --network postgres-app \
  --env POSTGRES_PASSWORD_FILE=/run/secrets/postgres-password \
  --secret postgres-password,type=mount \
  --volume postgres-data:/var/lib/pgsql/data \
  microsoft/azurelinux/workload/postgres:4.0

podman run --rm \
  --network postgres-app \
  --secret postgres-password,type=mount \
  --entrypoint bash \
  microsoft/azurelinux/workload/postgres:4.0 \
  -c '
    export PGPASSWORD="$(cat /run/secrets/postgres-password)"
    attempt=0
    until pg_isready --host=postgres --username=postgres --dbname=postgres; do
      attempt=$((attempt + 1))
      if [ "$attempt" -ge 30 ]; then
        echo "PostgreSQL did not become ready" >&2
        exit 1
      fi
      sleep 1
    done
    exec psql "$@"
  ' -- \
    --host=postgres \
    --username=postgres \
    --dbname=postgres \
    --command='SELECT 1;'
```

Set `POSTGRES_HOST_AUTH_METHOD=trust` only for intentionally unsecured
development environments. The image does not configure TLS, and merely
enabling PostgreSQL TLS does not force clients to use it because the generated
`host` rule accepts encrypted and unencrypted connections. Use a trusted
private container network by default. Before exposing port 5432 outside that
network, configure PostgreSQL certificates and replace the generated rule with
rules that reject non-TLS connections and require TLS:

```text
hostnossl all all all reject
hostssl   all all all scram-sha-256
```

## Interactive runtime images

The BusyBox, Python, Node.js, and PyTorch images start a shell or interpreter
as their default command. Run them with an interactive terminal:

```bash
podman run --rm -it microsoft/azurelinux/workload/busybox:4.0
podman run --rm -it microsoft/azurelinux/workload/python:4.0
podman run --rm -it microsoft/azurelinux/workload/nodejs:4.0
podman run --rm -it microsoft/azurelinux/workload/pytorch:4.0
```

The PyTorch workload image contains the precompiled PyTorch and ROCm runtime
libraries, but intentionally omits static libraries, headers, compiler
frontends, and build metadata. Use a development image when compiling native
extensions or generating ROCm code inside the container.

Without an interactive terminal or input, these commands reach end-of-file and
exit normally. For non-interactive use, select the executable explicitly and
supply a script or expression:

```bash
podman run --rm \
  --entrypoint python3 \
  microsoft/azurelinux/workload/python:4.0 \
  -c 'print("hello from Python")'

podman run --rm \
  --entrypoint node \
  microsoft/azurelinux/workload/nodejs:4.0 \
  -e 'console.log("hello from Node.js")'
```
