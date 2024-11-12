#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import argparse
import dataclasses
import json
import logging
import multiprocessing
import os
import subprocess
import sys
import time

from typing import Sequence

logger = logging.getLogger(__name__)
self_path = os.path.abspath(__file__)
script_dir_path = os.path.dirname(self_path)
toolkit_dir_path = os.path.dirname(script_dir_path)
repo_root_dir_path = os.path.dirname(toolkit_dir_path)
build_dir_path = os.path.join(repo_root_dir_path, "build")
test_results_path = os.path.join(build_dir_path, "pkg_artifacts", "test_results.json")
logs_dir_path = os.path.join(build_dir_path, "logs")
ptest_logs_dir_path = os.path.join(logs_dir_path, "pkggen", "rpmbuilding")

parser = argparse.ArgumentParser(description="Run package tests")
parser.add_argument("-s", "--spec", dest="specs", action="append", help="Names of base specs to run tests for")
parser.add_argument("-e", "--extended-spec", dest="extended_specs", action="append", help="Names of extended specs to run tests for")
parser.add_argument("-v", "--verbose", dest="verbose", action="store_true", help="Enable verbose output")
parser.add_argument("--markdown-report", dest="markdown_report", help="Path to output markdown report of test results")

args = parser.parse_args()

if args.verbose:
    log_level = logging.DEBUG
else:
    log_level = logging.INFO

logging.basicConfig(format="%(levelname)s: %(message)s", level=log_level)

if not os.path.isfile(os.path.join(toolkit_dir_path, "Makefile")):
    logger.error("can't find toolkit path")
    sys.exit(1)


def run_ptests(spec_names: Sequence[str], specs_dir_path: str):
    toolkit_log_level = "info" if args.verbose else "warn"

    # N.B. We do *not* use TEST_RUN_LIST or TEST_RERUN_LIST, because those
    # fail in undesirable ways on specs with no %check sections. We instead
    # just set RUN_CHECK=y and figure out after the fact what happened.
    cmd = [
        "sudo",
        "make",
        "build-packages",
        "-j",
        str(multiprocessing.cpu_count()),
        "REBUILD_TOOLS=y",
        f"SPECS_DIR={specs_dir_path}",
        f"LOG_LEVEL={toolkit_log_level}",
        f"SRPM_PACK_LIST={' '.join(spec_names)}",
        f"PACKAGE_REBUILD_LIST={' '.join(spec_names)}",
        "RUN_CHECK=y",
        "DAILY_BUILD_ID=lkg"
    ]

    start_time = time.time()

    result = subprocess.run(cmd, cwd=toolkit_dir_path)
    if result.returncode != 0:
        logger.error("build tools invocation failed")
        sys.exit(1)

    elapsed_time = time.time() - start_time

    logger.info(f"Ran tests in {elapsed_time:.2f}s.")

class ReadableTestReporter:
    def on_skipped(self, name: str):
        print(f"⏩ {name}: SKIPPED")

    def on_blocked(self, name: str):
        print(f"🚫 {name}: BLOCKED")

    def on_failed(self, name: str, expected_failure: bool, log_path: str):
        if expected_failure:
            print(f"🟡 {name}: FAILED (expected)")
        else:
            print(f"❌ {name}: FAILED")
            print(f"    Log: {log_path}")

    def on_succeeded(self, name: str, expected_failure: bool):
        if expected_failure:
            print(f"🔴 {name}: PASSED (unexpected)")
        else:
            print(f"✅ {name}: PASSED")

    def on_unknown_result(self, name: str, result: str):
        print(f"❓ {name}: {result}")

class MarkdownTestReporter:
    def __init__(self, report_path: str):
        self._report_file = open(report_path, "w")

    def close(self):
        self._report_file.close()

    def on_skipped(self, name: str):
        self._test_heading(name)
        self._write_line(f"⏩ {name}: SKIPPED")
        self._write_line("")

    def on_blocked(self, name: str):
        self._test_heading(name)
        self._write_line(f"🚫 {name}: BLOCKED")
        self._write_line("")

    def on_failed(self, name: str, expected_failure: bool, log_path: str):
        self._test_heading(name)

        if expected_failure:
            self._write_line(f"🟡 {name}: FAILED (expected)")
        else:
            self._write_line(f"❌ {name}: FAILED")

        LINES_TO_SHOW = 100

        self._write_line("")
        self._write_line(f"Last {LINES_TO_SHOW} lines of test output:\n")

        self._write_line("```")
        with open(log_path, "r") as log_file:
            for line in log_file.readlines()[-LINES_TO_SHOW:]:
                self._report_file.write(line)
        self._write_line("```")
        self._write_line("")

    def on_succeeded(self, name: str, expected_failure: bool):
        self._test_heading(name)

        if expected_failure:
            self._write_line(f"🔴 {name}: PASSED (unexpected)")
        else:
            self._write_line(f"✅ {name}: PASSED")

        self._write_line("")

    def on_unknown_result(self, name: str, result: str):
        self._test_heading(name)
        self._write_line(f"❓ {name}: {result}")
        self._write_line("")

    def _test_heading(self, name: str):
        self._write_line(f"## `{name}`\n\n")

    def _write_line(self, line: str):
        self._report_file.write(line)
        self._report_file.write("\n")


@dataclasses.dataclass
class Results:
    unexpected_fail_count: int = 0
    expected_fail_count: int = 0
    skip_count: int = 0
    block_count: int = 0
    expected_success_count: int = 0
    unexpected_success_count: int = 0


def analyze_test_results(reporters, results):
    logger.debug(f"Analyzing test results: {test_results_path}")

    with open(test_results_path, "r") as test_results:
        test_results_text = test_results.read()
        test_results = json.loads(test_results_text)

    #
    # Report results.
    #

    # TODO: Figure out which components didn't *have* any checks to run.
    for srpm_name, srpm_results in test_results.items():
        result = srpm_results["Result"]
        expected_failure = srpm_results["ExpectedFailure"]

        if result == "skipped":
            for reporter in reporters:
                reporter.on_skipped(srpm_name)
            results.skip_count += 1
        elif result == "blocked":
            for reporter in reporters:
                reporter.on_blocked(srpm_name)
            results.block_count += 1
        elif result == "failed":
            if expected_failure:
                results.expected_fail_count += 1
            else:
                results.unexpected_fail_count += 1  
            for reporter in reporters:
                reporter.on_failed(srpm_name, expected_failure, srpm_results["LogPath"])
        elif result == "succeeded":
            if expected_failure:
                results.unexpected_success_count += 1
            else:
                results.expected_success_count += 1
            for reporter in reporters:
                reporter.on_succeeded(srpm_name, expected_failure)
        else:
            for reporter in reporters:
                reporter.on_unknown_result(srpm_name, result)


#
# Run tests
#

if not args.specs and not args.extended_specs:
    logger.error("no specs provided")
    sys.exit(1)

results = Results()

reporters = [ReadableTestReporter()]

markdown_reporter = None
if args.markdown_report:
    logger.debug(f"Writing markdown report to: {args.markdown_report}")
    markdown_reporter = MarkdownTestReporter(args.markdown_report)
    reporters.append(markdown_reporter)

if args.specs:
    logger.debug("Running ptests against base specs")
    run_ptests(args.specs, os.path.join(repo_root_dir_path, "SPECS"))
    analyze_test_results(reporters, results)

if args.extended_specs:
    logger.debug("Running ptests against extended specs")
    run_ptests(args.extended_specs, os.path.join(repo_root_dir_path, "SPECS-EXTENDED"))
    analyze_test_results(reporters, results)

if markdown_reporter:
    logger.debug(f"Saving markdown report")
    markdown_reporter.close()


#
# Display a readable summary.
#

print("")
if results.expected_success_count > 0:
    print(f"Tests succeeded:              {results.expected_success_count}")
if results.unexpected_success_count > 0:
    print(f"Tests succeeded unexpectedly: {results.unexpected_success_count}")
if results.expected_fail_count > 0:
    print(f"Tests expected to fail:       {results.expected_fail_count}")
if results.unexpected_fail_count > 0:
    print(f"Tests failed:                 {results.unexpected_fail_count}")
if results.block_count > 0:
    print(f"Tests blocked:                {results.block_count}")
if results.skip_count > 0:
    print(f"Tests skipped:                {results.skip_count}")

if results.unexpected_fail_count > 0 or results.block_count > 0:
    logger.error("One or more tests were failed or blocked; exiting with error.")
    sys.exit(1)
