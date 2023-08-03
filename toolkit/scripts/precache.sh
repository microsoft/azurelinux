#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Usage: precache.sh </path/to/snapshot.json> <cache_working_dir> <cache_dir> <downloaded_files.txt> <repo_base_urls>...
snapshot_path="$1"
[[ -z "$snapshot_path" ]] && echo "snapshot_path is required" && exit 1
shift

cache_working_dir="$1"
[[ -z "$cache_working_dir" ]] && echo "cache_working_dir is required" && exit 1
shift

cache_dir="$1"
[[ -z "$cache_dir" ]] && echo "cache_dir is required" && exit 1
shift

downloaded_files="$1"
[[ -z "$downloaded_files" ]] && echo "downloaded_files is required" && exit 1
shift

base_urls=("$@")
[[ ${#base_urls[@]} -eq 0 ]] && echo "base_urls is required" && exit 1

mkdir -p "$cache_working_dir"
mkdir -p "$cache_dir"
rm -f "$downloaded_files"

. /etc/os-release
if [[ "$ID" == "mariner" ]]; then
    REPOQUERY_OS_ARGS="-y -q --disablerepo=*"
else
    REPOQUERY_OS_ARGS="--show-duplicates --tempcache"
fi

skipped_file="$cache_working_dir/skipped.txt"
repo_summary_file="$cache_working_dir/repo.txt"

# Init the cache
mkdir -p "$cache_working_dir"
mkdir -p "$cache_dir"
rm -f "$downloaded_files"
rm -f "$skipped_file"

# For each base url, pull the meta data and write it to the repo summary file
echo "" > $repo_summary_file
for base_url in "${base_urls[@]}"; do
    repo_unique="repo-$(echo $(((RANDOM%99999)+10000)))"
    repo_name="mariner-precache-$repo_unique"
    echo "Querying repo $base_url via 'repoquery $REPOQUERY_OS_ARGS --repofrompath=$repo_name,$base_url -a --qf="%{location}" >> $repo_summary_file'"
    if [[ "$ID" == "mariner" ]]; then
        # Mariner version doesn't prepend the full URL, so add manually via sed on every line
        prefix="$base_url/"
    else
        prefix=""
    fi
    repoquery $REPOQUERY_OS_ARGS --repofrompath=$repo_name,$base_url -a --qf="%{location}" | sed "s|^|$prefix|" >> $repo_summary_file || exit 1
done

# For each package in the snapshot summary, find the latest version of package $1 in the repo summary file $2 and print the url
function get_url() {
    local name="$1"
    local repo_summary_file="$2"
    rpm_name="$name.rpm"
    # '/' is important here, otherwise we might match a similarly named package. The '/' guarantees we match the start of the name.
    rpm_url=$(grep "/$rpm_name" "$repo_summary_file" | head -n 1)
    if [[ -z "$rpm_url" ]]; then
        echo "PRE-CACHE: Repos do not contain $rpm_name, skipping" >&2
        return
    fi
    echo "$rpm_url"
}

touch "$downloaded_files"
touch "$skipped_file"
function download_rpm() {
    local rpm_url="$1"
    local cache_dir="$2"
    local downloaded_files="$3"
    local skipped_file="$4"
    rpm_name=$(basename "$rpm_url")
    # We can't use -O with wget since that resets the timestamp. We want to use -N to only download if the file is newer so we
    # need to use cd to the cache directory and then wget the file.
    if ! output=$(cd "$cache_dir" && wget -nv -N --tries=4 --waitretry=10 "$rpm_url" 2>&1); then
        echo "Failed to pre-cache $rpm_url"
        rm -f "$cache_dir/$rpm_name"
        return
    else
        # Output will contain the url + path only if it is downloaded. If it is not downloaded, it will be an empty string. Write all files we
        # successfully downloaded to the downloaded_files file.
        if [[ -n "$output" ]]; then
            echo "$output" >> "$downloaded_files"
        else
            echo "$rpm_url" >> "$skipped_file"
        fi
    fi
}

# For each rpm in the snapshot .json file, download it to the cache directory. We format the output as "Name-Version.Distribution.Architecture"
# Export the functions so we can use them in parallel via xargs. We can run the grep fully in parallel since it is just a string match, but we want to
# limit the number of concurrent downloads to avoid overloading the network.
export -f get_url
export -f download_rpm
max_concurrent_downloads=30
jq -r '.Repo[] | "\(.Name)-\(.Version).\(.Distribution).\(.Architecture)"' "$snapshot_path" | sort -u | \
    xargs -I {} bash -c "get_url '{}' '$repo_summary_file'" | \
    xargs -P $max_concurrent_downloads -I {} bash -c "download_rpm '{}' '$cache_dir' '$downloaded_files' '$skipped_file'"

# Calculate the expected number of packages in the snapshot we were expecting to download
expected_count=$(jq -r '.Repo[] | .Name' "$snapshot_path" | wc -l)
echo "Pre-cached $(wc -l < "$downloaded_files") packages out of $expected_count total packages"
