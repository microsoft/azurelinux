#!/usr/bin/python3

# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import concurrent.futures
import os
import random
import tempfile
import time
import subprocess
import urllib.request

# generate_test_data.py generates a pair of files that contain all the license and doc files for all RPMs in the repository.
# The intent is to use this data to test the licensecheck tool for false positives/negatives.

# This tool should be run in an azl-like environment, specifically the 'repoquery' tool must be available, and it must
# be able to pull rpms from a representitive repo that contains all RPMs to measure (ie PMC).

# get_all_rpms() returns a list of URLs to each RPM in the default repos. It only looks at the latest version of each RPM.
def get_all_rpms() -> list[str]:
    cmd = ["repoquery", "-y", "--latest-limit=1", "--all", "--location"]
    output = subprocess.check_output(cmd, text=True, stderr=subprocess.DEVNULL)

    # Clean the output:
    # - Split into a list
    # - Remove anything that is *.src.rpm (some environemnts will give us the source RPMs as well)
    # - Remove any empty strings after stirpping
    output = output.split("\n")
    output = [url.strip() for url in output if not url.endswith(".src.rpm")]
    output = [url for url in output if url]

    return output

# query_rpm_url() runs the 'rpm' command with the given query and URL. It returns a list of files based on the query.
def query_rpm_url(out_file: str, args: list[str]) -> list[str]:
    cmd = ["rpm"] + args + [out_file]
    # Run the bash script and capture the output.
    output = subprocess.check_output(cmd, text=True, stderr=subprocess.DEVNULL)

    # If the output has the string '(contains no files)', then there are no files to list
    if "(contains no files)" in output:
        return []

    output = output.split("\n")
    output = [file for file in output if file]
    return output

def get_name(out_file: str) -> str:
    return query_rpm_url(out_file, ["-q", "--qf", "%{NAME}\n"])

def get_license_files(out_file: str) -> list[str]:
    return query_rpm_url(out_file, ["-qL"])

def get_doc_files(out_file: str) -> list[str]:
    return query_rpm_url(out_file, ["-qd"])

# get_files_for_url() returns a result object with the URL, license files, and doc files for a given URL.
def get_files_for_url(url: str) -> dict:
    # Get a tempdir to hold the rpm in so we can query it
    with tempfile.TemporaryDirectory() as tempdir:
        # Download the file to the tempdir
        out_file = os.path.join(tempdir, "pkg.rpm")
        urllib.request.urlretrieve(url, out_file)
        res = {
            "url": url,
            "pkg_name": get_name(out_file)[0],
            "license_files": get_license_files(out_file),
            "doc_files": get_doc_files(out_file)
        }
    return res

# Write the results to a file.
def write_to_file(file_list: list[(str,str)], output_file: str):
    print(f"Writing to {output_file}")
    file_list.sort()
    with open(output_file, "w") as f:
        for pkg_name, full_path_list  in file_list:
            for full_path in full_path_list:
                f.write(f"{pkg_name}`{full_path}\n")

# Put the debug info packages first since they tend to be really big,
#     then the remaining URLs,
# Randomize the lists to even out the load
all_urls = get_all_rpms()
debug_urls = [url for url in all_urls if "debuginfo" in url]
other_urls = [url for url in all_urls if "debuginfo" not in url]
random.shuffle(debug_urls)
random.shuffle(other_urls)
jobs = debug_urls + other_urls

# Queue each URL to be processed in parallel
num_processes = 4 * os.cpu_count()
license_files=[]
doc_files=[]
with concurrent.futures.ProcessPoolExecutor(max_workers=num_processes) as executor:
    results = [executor.submit(get_files_for_url, url) for url in jobs]
    total_processed = 0
    start_time = time.time()
    for future in concurrent.futures.as_completed(results):
        res = future.result()
        license_files.append((res["pkg_name"], res["license_files"]))
        doc_files.append((res["pkg_name"],res["doc_files"]))
        total_processed += 1

        # Estimated time remaining
        elapsed_time = time.time() - start_time
        time_per_file = elapsed_time / total_processed
        remaining_files = len(jobs) - total_processed
        remaining_time = time_per_file * remaining_files

        percent_done = (total_processed / len(jobs)) * 100
        base_name = res["url"].split("/")[-1]
        print(f"~{remaining_time:.0f}s remaining ({total_processed}/{len(jobs)} ({percent_done:.2f}%))... {base_name} ")

# Write the results to 'all_licenses_<date>.txt' and 'all_docs_<date>.txt'
date = time.strftime('%Y%m%d')
license_file_path=f"all_licenses_{date}.txt"
doc_file_path=f"all_docs_{date}.txt"
write_to_file(license_files, license_file_path)
write_to_file(doc_files, doc_file_path)
