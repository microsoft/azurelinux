#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
#
# Builds Bazel's self-contained bootstrap source distribution from the pinned
# upstream commit. This requires an existing Bazel 7.7.0 executable; the output
# archive can then be consumed by compile.sh to bootstrap another Bazel binary.

set -euo pipefail

readonly BAZEL_VERSION="7.7.0"
readonly BAZEL_COMMIT="c87a789d5d9e9b51b2284a923a76539887486331"
readonly BAZEL_REPOSITORY="https://github.com/bazelbuild/bazel.git"
readonly GENERATED_SHA256="5d6545b74406841b037429e04f6351927af0ec8318162e9054c3a7d54c030179"
readonly OFFICIAL_SHA256="277946818c77fff70be442864cecc41faac862b6f2d0d37033e2da0b1fee7e0f"
readonly ARCHIVE_NAME="bazel-${BAZEL_VERSION}-dist.zip"

usage() {
    cat <<EOF
Usage: ${0##*/} [OUTPUT_DIRECTORY]

Build ${ARCHIVE_NAME} from Bazel commit ${BAZEL_COMMIT}.

Requirements:
  - bazel ${BAZEL_VERSION}
  - gcc and g++
  - git
  - OpenJDK 25
  - python3
  - unzip

The build fetches Bazel's external repositories from the network. Its temporary
checkout and Bazel caches are created below OUTPUT_DIRECTORY and removed on
success. OUTPUT_DIRECTORY defaults to the current directory.

Set VERIFY_OFFICIAL_HASH=1 to require byte-for-byte identity with the official
Bazel release archive in addition to validating the generated archive's contents.
Set KEEP_WORK_DIRECTORY=1 to retain the temporary checkout and Bazel caches.
EOF
}

if [ "$#" -gt 1 ]; then
    usage >&2
    exit 2
fi

if [ "${1:-}" = "-h" ] || [ "${1:-}" = "--help" ]; then
    usage
    exit 0
fi

for command in bazel gcc g++ git java javac python3 sha256sum unzip; do
    if ! command -v "${command}" >/dev/null 2>&1; then
        echo "Error: required command not found: ${command}" >&2
        exit 1
    fi
done

readonly OUTPUT_DIRECTORY="$(realpath -m "${1:-.}")"
readonly OUTPUT_ARCHIVE="${OUTPUT_DIRECTORY}/${ARCHIVE_NAME}"
readonly WORK_DIRECTORY="${OUTPUT_DIRECTORY}/.bazel-${BAZEL_VERSION}-dist-work.$$"

mkdir -p "${OUTPUT_DIRECTORY}"
if [ -e "${OUTPUT_ARCHIVE}" ]; then
    echo "Error: output archive already exists: ${OUTPUT_ARCHIVE}" >&2
    exit 1
fi
if [ -e "${WORK_DIRECTORY}" ]; then
    echo "Error: work directory already exists: ${WORK_DIRECTORY}" >&2
    exit 1
fi

cleanup() {
    if [ "${KEEP_WORK_DIRECTORY:-0}" = "1" ]; then
        printf 'Retained work directory: %s\n' "${WORK_DIRECTORY}" >&2
        return
    fi
    if [ -n "${WORK_DIRECTORY:-}" ] &&
       [ "${WORK_DIRECTORY}" != "/" ] &&
       [ -d "${WORK_DIRECTORY}" ]; then
        rm -rf -- "${WORK_DIRECTORY}"
    fi
}
trap cleanup EXIT

mkdir -p "${WORK_DIRECTORY}/source"

version_output="$(
    bazel \
        --batch \
        --output_user_root="${WORK_DIRECTORY}/version-output-user-root" \
        version
)"
printf '%s\n' "${version_output}"
if ! printf '%s\n' "${version_output}" |
     grep -Fqx "Build label: ${BAZEL_VERSION}"; then
    echo "Error: Bazel ${BAZEL_VERSION} is required to build the distribution archive." >&2
    exit 1
fi

java_version="$(java -version 2>&1 | sed -n '1p')"
printf 'Java runtime: %s\n' "${java_version}"
if ! printf '%s\n' "${java_version}" | grep -Eq 'version "25([.-]|")'; then
    echo "Error: OpenJDK 25 is required." >&2
    exit 1
fi

git -C "${WORK_DIRECTORY}/source" init --quiet
git -C "${WORK_DIRECTORY}/source" remote add origin "${BAZEL_REPOSITORY}"
git -C "${WORK_DIRECTORY}/source" fetch \
    --quiet \
    --depth=1 \
    origin \
    "${BAZEL_COMMIT}"
git -C "${WORK_DIRECTORY}/source" checkout --quiet --detach FETCH_HEAD

actual_commit="$(git -C "${WORK_DIRECTORY}/source" rev-parse HEAD)"
if [ "${actual_commit}" != "${BAZEL_COMMIT}" ]; then
    echo "Error: checked-out commit does not match the pinned Bazel commit." >&2
    echo "  expected: ${BAZEL_COMMIT}" >&2
    echo "  actual:   ${actual_commit}" >&2
    exit 1
fi

mkdir -p "${WORK_DIRECTORY}/jdk25_toolchain"
cat > "${WORK_DIRECTORY}/jdk25_toolchain/BUILD.bazel" <<'EOF'
load(
    "@rules_java//toolchains:default_java_toolchain.bzl",
    "VANILLA_TOOLCHAIN_CONFIGURATION",
    "default_java_toolchain",
)

# Bazel 7's prebuilt Java 21 toolchain cannot read JDK 25 module metadata.
# The vanilla toolchain retains Java 21 source/target compatibility while
# running javac from Azure Linux's local JDK 25.
default_java_toolchain(
    name = "toolchain",
    configuration = VANILLA_TOOLCHAIN_CONFIGURATION,
    java_runtime = "@local_jdk//:jdk",
    source_version = "21",
    target_version = "21",
)
EOF
touch "${WORK_DIRECTORY}/jdk25_toolchain/WORKSPACE"

export JAVA_HOME="$(dirname "$(dirname "$(readlink -f "$(command -v javac)")")")"

pushd "${WORK_DIRECTORY}/source" >/dev/null
bazel \
    --batch \
    --output_user_root="${WORK_DIRECTORY}/output-user-root" \
    build \
    --extra_toolchains=@remotejdk11_win_arm64//:toolchain_definition \
    --host_javacopt=-Acom.google.auto.value.AutoBuilderIsUnstable \
    --java_language_version=21 \
    --java_runtime_version=local_jdk \
    --javacopt=-Acom.google.auto.value.AutoBuilderIsUnstable \
    --override_repository=rules_java~~toolchains~remotejdk11_win_arm64="${WORK_DIRECTORY}/jdk25_toolchain" \
    --tool_java_language_version=21 \
    --tool_java_runtime_version=local_jdk \
    //:bazel-distfile
popd >/dev/null

readonly BUILT_ARCHIVE="${WORK_DIRECTORY}/source/bazel-bin/bazel-distfile.zip"
if [ ! -f "${BUILT_ARCHIVE}" ]; then
    echo "Error: Bazel did not produce ${BUILT_ARCHIVE}." >&2
    exit 1
fi

unzip -qt "${BUILT_ARCHIVE}"
for required_path in \
    compile.sh \
    derived/repository_cache/README.md \
    src/main/java/com/google/devtools/build/lib/bazel/Bazel.java; do
    if ! unzip -Z1 "${BUILT_ARCHIVE}" |
         grep -Fx "${required_path}" >/dev/null; then
        echo "Error: generated archive is missing ${required_path}." >&2
        exit 1
    fi
done

actual_sha256="$(sha256sum "${BUILT_ARCHIVE}" | awk '{print $1}')"
printf 'Generated SHA-256: %s\n' "${actual_sha256}"

if [ "${actual_sha256}" != "${GENERATED_SHA256}" ]; then
    echo "Error: generated archive is not reproducible with the pinned JDK 25 recipe." >&2
    echo "  expected: ${GENERATED_SHA256}" >&2
    echo "  actual:   ${actual_sha256}" >&2
    exit 1
fi

if [ "${VERIFY_OFFICIAL_HASH:-0}" = "1" ] &&
   [ "${actual_sha256}" != "${OFFICIAL_SHA256}" ]; then
    echo "Error: generated archive differs from the official Bazel ${BAZEL_VERSION} archive." >&2
    echo "  expected: ${OFFICIAL_SHA256}" >&2
    echo "  actual:   ${actual_sha256}" >&2
    exit 1
fi

install -m 0644 "${BUILT_ARCHIVE}" "${OUTPUT_ARCHIVE}"
printf 'Created %s\n' "${OUTPUT_ARCHIVE}"
