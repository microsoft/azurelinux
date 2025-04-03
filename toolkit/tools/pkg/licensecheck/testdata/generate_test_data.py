#!/usr/bin/python3

# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import concurrent.futures
import json
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

def get_all_files(out_file: str, filter_list: list[str]) -> list[str]:
    all_files_and_dirs = query_rpm_url(out_file, ["-q", "--qf", "[%{FILEMODES:perms} %{FILENAMES}\n]"])
    # Each line will be in the format "drwxr-xr-x /a/directory" or "-rw-r--r-- /a/directory/a_file", remove the
    # directories and keep the files, then drop the permissions part of the string.
    all_files = [file.split(' ', 1)[1] for file in all_files_and_dirs if file[0] != "d"]
    filter_set = set(filter_list)
    filtered_files = [file for file in all_files if file not in filter_set]
    return filtered_files

# get_files_for_url() returns a result object with the URL, license files, and doc files for a given URL.
def get_files_for_url(url: str) -> dict:
    # Get a tempdir to hold the rpm in so we can query it
    with tempfile.TemporaryDirectory() as tempdir:
        # Download the file to the tempdir
        out_file = os.path.join(tempdir, "pkg.rpm")
        urllib.request.urlretrieve(url, out_file)
        license_files = get_license_files(out_file)
        doc_files = get_doc_files(out_file)
        all_other_files = get_all_files(out_file, license_files + doc_files)
        res = {
            "url": url,
            "pkg_name": get_name(out_file)[0],
            "license_files": license_files,
            "doc_files": doc_files,
            "all_other_files": all_other_files

        }
    return res

# Corresponding go structs for the output of this script:

# type testData struct {
# 	UniqueFiles     int
# 	UniquePackages  int
# 	TestDataEntries []testDataEntry
# }

# type testDataEntry struct {
# 	Pkg  string `json:"Pkg"`
# 	Path string `json:"Path"`
# }

# Write the results to a file.
def write_to_file(file_list: list[(str,list[str])], output_file: str):
    print(f"Writing to {output_file}")
    file_list.sort()

    testDataEntires = []
    for pkg_name, files in file_list:
        for file in files:
            testDataEntires.append({
                "Pkg": pkg_name,
                "Path": file
            })
        # Count the unique packages
    test_data = {
        "UniqueFiles": len(testDataEntires),
        "UniquePackages": len([pkg_name for pkg_name, files in file_list if files]), # Only packages with files are counted
        "TestDataEntries": testDataEntires
    }

    with open(output_file, "w") as f:
        json.dump(test_data, f, indent=0)

def main():
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
    all_other_files=[]
    with concurrent.futures.ProcessPoolExecutor(max_workers=num_processes) as executor:
        results = [executor.submit(get_files_for_url, url) for url in jobs]
        total_processed = 0
        start_time = time.time()
        for future in concurrent.futures.as_completed(results):
            res = future.result()
            license_files.append((res["pkg_name"], res["license_files"]))
            doc_files.append((res["pkg_name"],res["doc_files"]))
            all_other_files.append((res["pkg_name"],res["all_other_files"]))
            total_processed += 1

            # Estimated time remaining
            elapsed_time = time.time() - start_time
            time_per_file = elapsed_time / total_processed
            remaining_files = len(jobs) - total_processed
            remaining_time = time_per_file * remaining_files

            percent_done = (total_processed / len(jobs)) * 100
            base_name = res["url"].split("/")[-1]
            print(f"~{remaining_time:.0f}s remaining ({total_processed}/{len(jobs)} ({percent_done:.2f}%))... {base_name} ")

    # Write the results to 'all_licenses_<date>.json' and 'all_docs_<date>.json'
    date = time.strftime('%Y%m%d')
    license_file_path=f"all_licenses_{date}.json"
    doc_file_path=f"all_docs_{date}.json"
    all_other_file_path=f"all_other_files_{date}.json"
    write_to_file(license_files, license_file_path)
    write_to_file(doc_files, doc_file_path)
    write_to_file(all_other_files, all_other_file_path)

if __name__ == "__main__":
    main()
