#!/bin/python3

# Tool to inspect the Mariner rpm build log to collect
# the package test status and generate the CSV report

import argparse
import os
import re
import csv
import inspect
from dateutil.parser import parse
from junit_xml import TestSuite, TestCase
MARINER_PKG_TEST_TABLENAME="Mariner_Package_Test"
PKG_TEST_COMPOSITE_KEY = ["BuildID", "PackageName", "Version"]

PKGTEST_TOOL_PREFIX="PKGTEST::"

# Markers of package test for detecting pass/fail
PACKAGE_TEST_IGNORE_ID  = "echo"
PACKAGE_TEST_END_ID     = "====== CHECK DONE"
PACKAGE_TEST_START_ID   = "====== CHECK START"
PACKAGE_TEST_SKIP_ID    = "====== SKIPPING CHECK"

# CSV header for package test report
report_header = ["BuildID", "PackageName", "Version", "ExecutionTime", "Results"]

class dlogger:
    '''
    '''
    def __init__(self, verbose):
        self.verbose = verbose

    def print_debug_logs(self, msg):
        '''
        Debug logger for pkgtest utility
        '''
        if self.verbose == False:
            return
        current_frame = inspect.currentframe()
        caller_frame = inspect.getouterframes(current_frame, 2)
        caller = caller_frame[1][3]
        caller_log = "%s::" % (caller)
        print(PKGTEST_TOOL_PREFIX, caller_log, msg)

#class db:

class pkgtest:
    '''
    Package test class to expose all the required functionality for parsing
    the Mariner package build logs.
    '''
    def __init__(self, logger):
        self.debug_log = logger


    def _get_pkg_details(self, filename):
        '''
        Fetch the package details from the log filename
        '''
        g = re.search(r'(.*/)*(.*)-(.*)-(.*?)(\.src.rpm.test.log)', filename)
        pkgname  = g.groups()[1]
        version = g.groups()[2] + "-" + g.groups()[3]
        self.debug_log.print_debug_logs("Package: %s  Version: %s" % (pkgname, version))

        return pkgname, version

    def _get_timestamp(self, log):
        '''
        Get the timestamp from the log. Time is converted to epoch time
        '''
        try:
            timestamp = parse((log.split(" ")[0].split("=")[1]).replace('"', ''))
        except ValueError as err:
            self.debug_log.print_debug_logs("Timestamp parsing failed, line: \"%s\". Error: \"%s\"" % (log, str(err)))
            return None
        # return epoch time
        return timestamp.timestamp()

    def _get_test_status(self, line):
        '''
        Get the test status from the log
        '''
        status = int((line.split("EXIT STATUS ")[1]).replace('"', ''))
        self.debug_log.print_debug_logs("STATUS => %d" % status)
        if status == 0:
            return "Pass"
        return "Fail"

    def _check_test_status(self, fp):
        '''
        Check the package test status
        '''
        start_time = end_time = None
        status = "Not Supported"
        for line in fp:
            line = line.strip("\n")
            if re.search(PACKAGE_TEST_IGNORE_ID, line):
                    continue

            if re.search(PACKAGE_TEST_START_ID, line):
                self.debug_log.print_debug_logs(line)
                start_time = self._get_timestamp(line)
            if re.search(PACKAGE_TEST_END_ID, line):
                self.debug_log.print_debug_logs(line)
                end_time = self._get_timestamp(line)
                status = self._get_test_status(line)
                break
            if re.search(PACKAGE_TEST_SKIP_ID, line):
                self.debug_log.print_debug_logs(line)
                status = "Skipped"
                break
        if start_time != None and end_time == None:
            status = "Aborted"
        return status, start_time, end_time

    def _analyze_pkg_test_log(self, filename):
        '''
        Scrape the pkg test log and detect the different status of
        test like pass/fail/skipped/aborted/not supported
        '''
        start_time = end_time = status = None
        elapsed_time = 0
        with open(filename, 'r') as fp:
            status, start_time, end_time = self._check_test_status(fp)
        if start_time != None and end_time != None:
            elapsed_time = end_time - start_time

        dbg_msg = "status: %s start time: %s end time: %s" % (status, start_time, end_time)
        self.debug_log.print_debug_logs(dbg_msg)
        fp.close()
        return status,elapsed_time

    def _get_failure_log(self, fpath):
        '''
        '''
        start_log = False
        contents = []
        with open(fpath, 'r') as fp:
            for line in fp:
                if re.search(PACKAGE_TEST_IGNORE_ID, line):
                    continue
                if start_log:
                    contents.append(line)
                if re.search(PACKAGE_TEST_START_ID, line):
                    contents.append(line)
                    start_log = True
                if re.search(PACKAGE_TEST_END_ID, line):
                    contents.append(line)
                    break
            fp.close()
        return(" ".join(contents))

    def _get_junit_test_status(self, pkgname, version, status, time, fpath, testname):
        '''
        '''
        if status == "Fail":
            stdout = self._get_failure_log(fpath)
            stderr = None
        else:
            stdout = stderr = None
        tc = TestCase(pkgname, testname, time, stdout, stderr)

        if status == "Pass":
            return tc
        elif status == "Fail":
            tc.add_failure_info("TEST FAILED. CHECK ATTACHMENTS TAB FOR FAILURE LOG")
        elif status == "Skipped":
            tc.add_skipped_info("PACKAGE TEST SKIPPED")
        elif status == "Not Supported":
            tc.add_skipped_info("PACKAGE TEST NOT SUPPORTED")
        else:
            tc.add_error_info(status)
        return tc


    def scan_pkg_test_logs(self, path, junit_xml_filename, test_name):
        '''
        Scan the rpm build log folder and generate the package test report.
        '''
        testcases = []
        with open(junit_xml_filename, "w") as junit_fd:
            with os.scandir(path) as dentry:
                for file in dentry:
                    if file.is_file() and file.name.endswith('src.rpm.test.log'):
                        self.debug_log.print_debug_logs("Processing : %s" % file.name)
                        fpath = "%s/%s" % (path, file.name)
                        pkgname, version = self._get_pkg_details(file.name)
                        status, time = self._analyze_pkg_test_log(fpath)
                        testcases.append(self._get_junit_test_status(pkgname, version, status, time, fpath, test_name))
                        dbg_msg = "pkgname: %s version: %s test status: %s duration: %s\n" % (pkgname, version, status, time)
                        self.debug_log.print_debug_logs(dbg_msg)
            testsuite = TestSuite(test_name, testcases)
            TestSuite.to_file(junit_fd, [testsuite], prettyprint=True)


# Entry point
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    requires_args = parser.add_argument_group('mandatory arguments')

    parser.add_argument('-j', '--junit', action='store', required=False,
                        default="pkgtest_report_junit.xml", help="junit xml (default: pkgtest_report_junit.xml)")
    requires_args.add_argument('-p', '--path', action='store', required=True,
                        help="path of rpmbuild log directory")
    parser.add_argument('-t', '--testname', action='store', required=False,
                        default="Package-Test", help="High-level test name for display")
    parser.add_argument('-v', '--verbose', action='store_true',
                        help="enable verbose")

    args = parser.parse_args()

    # Custom logger for ptest to log debug messages
    logger = dlogger(args.verbose)
    logger.print_debug_logs("Path: %s" % args.path)

    # Instantiate the ptest object and process the package test logs
    ptest = pkgtest(logger)
    ptest.scan_pkg_test_logs(args.path, args.junit, args.testname)

