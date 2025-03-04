# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import argparse
import os
import subprocess
import sys
import tomllib
from enum import Enum

from colorama import Fore, Style


class VendorType(Enum):
    '''VendorType enum contains vendor types'''
    GO = "go"
    CARGO = "cargo"
    CUSTOM = "custom"


class PipelineLogging:
    '''PipelineLogging class contains logging formatting functions used for pipelines'''
    @staticmethod
    def output_warning(message: str, log_warning: bool = False):
        '''Prints a warning with yellow color message to the console'''
        log_format = '##vso[task.logissue type=warning]' if log_warning else '##[warning]'
        print(f"{log_format}{Fore.YELLOW}Warning: {message}{Style.RESET_ALL}")

    @staticmethod
    def output_error(message: str, log_error: bool = False):
        '''Prints an error with red color message to the console'''
        log_format = '##vso[task.logissue type=error]' if log_error else '##[error]'
        print(f"{log_format}{Fore.RED}Error: {message}{Style.RESET_ALL}")

    @staticmethod
    def output_log_error(message: str):
        '''Prints an error with red color message to the console and log it as an error in the pipeline'''
        PipelineLogging.output_error(message, True)

    @staticmethod
    def output_log_error_and_exit(message: str):
        '''
        Prints an error with red color message to the console and log it as an error in the pipeline
        and exit with error code 1
        '''
        PipelineLogging.output_error(message, True)
        sys.exit(1)

    @staticmethod
    def output_success(message: str):
        '''Prints an message with green color message to the console'''
        print(f"##[debug]{Fore.GREEN}{message}{Style.RESET_ALL}")

    @staticmethod
    def output_debug(message: str):
        '''Prints a debug with magenta color message to the console'''
        print(f"##[debug]{Fore.MAGENTA}{message}{Style.RESET_ALL}")


vendor_script_mapping = {
    VendorType.GO: "build_go_vendor.sh",
    VendorType.CARGO: "build_cargo_vendor.sh",
    VendorType.CUSTOM: "generate_source_tarball.sh"
}


class VendorProcessor:
    '''VendorProcessor class contains functions to process vendor files'''

    def __init__(self, pkg_name: str, pkg_path: str, src_tarball: str, out_folder: str, pkg_version: str, vendor_version: str):
        self.pkg_name = pkg_name
        self.pkg_path = pkg_path
        self.src_tarball = src_tarball
        self.out_folder = out_folder
        self.pkg_version = pkg_version
        self.vendor_version = vendor_version

    @staticmethod
    def get_toml_name(pkg_name: str) -> str:
        '''Get the toml file name from the package name'''
        return f"{pkg_name}.component.toml"

    @staticmethod
    def read_toml_file(toml_file_path: str) -> dict:
        '''Read the toml file and return the data as a dictionary'''
        toml_data: dict = None

        try:
            with open(toml_file_path, "rb") as f:
                toml_data = tomllib.load(f)
        except Exception as e:
            PipelineLogging.output_log_error_and_exit(
                f"Failed to read {toml_file_path} file: {e}")

        return toml_data

    def __raiseException(self, message):
        '''Raise an exception and log it as an error in the pipeline'''
        PipelineLogging.output_log_error(message)
        raise Exception(message)

    def process_toml_file(self):
        '''Process the toml file and run the vendor scripts'''

        toml_name = self.get_toml_name(self.pkg_name)
        toml_file_path = f"{self.pkg_path}/{toml_name}"

        toml_data = self.read_toml_file(toml_file_path)
        package_data: dict = toml_data['components'][self.pkg_name]
        vendor_types: list = package_data['vendors']['vendor_types']

        for vendor_type in vendor_types:
            vendor_type = VendorType(vendor_type)
            self.process_vendor_type(vendor_type)

    def process_vendor_type(self, vendor_type: VendorType):
        '''Process the vendor type and run the vendor script'''
        vendor_script_name = vendor_script_mapping.get(vendor_type)

        PipelineLogging.output_debug(
            f"Processing vendor type: '{vendor_type.value}', script name mapped to '{vendor_script_name}'")

        # get the script path as other scripts should live in same root folder
        working_directory = os.path.dirname(os.path.realpath(__file__))
        script_directory = working_directory

        # custom vendors store the script in the package folder
        if vendor_type == vendor_type.CUSTOM:
            script_directory = self.pkg_path

        vendor_script_path = os.path.join(
            script_directory, vendor_script_name)

        PipelineLogging.output_debug(
            f"Vendor script path: {vendor_script_path}")

        # run the script
        proc = subprocess.Popen([
            vendor_script_path,
            "--srcTarball", self.src_tarball,
            "--outFolder", self.out_folder,
            "--pkgVersion", self.pkg_version,
            "--vendorVersion", self.vendor_version],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True)

        stdout, stderr = proc.communicate()

        if proc.returncode != 0:
            # if stderr is empty, stdout contains the error message
            self.__raiseException(stdout if stderr == "" else stderr)

        PipelineLogging.output_success(
            f"Successfully processed vendor type: '{vendor_type.value}'")

        PipelineLogging.output_debug(f"Script output: \n{stdout}")


# parse arguments
# ----------------

parser = argparse.ArgumentParser()
parser.add_argument('--pkgName', help='package name', required=True)
parser.add_argument('--pkgPath', help='package path', required=True)
parser.add_argument('--srcTarball',
                    help='path to src tarball file or name. If unable to find, will attempt to download from blob store', required=True)
parser.add_argument('--outFolder',
                    help='folder where to copy the new tarball(s)', required=True)
parser.add_argument('--pkgVersion',
                    help='package version', required=True)
parser.add_argument('--vendorVersion',
                    help='vendor version', required=True)
parser.add_argument('--pipelineEnviroment', required=False,
                    type=lambda x: (str(x).lower() == 'true'), default=False, help='True if running in pipeline environment')
args = parser.parse_args()


def main():

    src_tarball = args.srcTarball
    out_folder = args.outFolder
    pkg_version = args.pkgVersion
    vendor_version = args.vendorVersion
    pipeline_env = args.pipelineEnviroment
    pkg_name = args.pkgName
    pkg_path = args.pkgPath

    PipelineLogging.output_debug(
        f"Src tarball path: {src_tarball}")
    PipelineLogging.output_debug(
        f"Out folder path: {out_folder}")
    PipelineLogging.output_debug(
        f"Package version: {pkg_version}")
    PipelineLogging.output_debug(
        f"Vendor version: {vendor_version}")
    PipelineLogging.output_debug(
        f"Pipeline environment: {pipeline_env}")
    PipelineLogging.output_debug(
        f"Package name: {pkg_name}")
    PipelineLogging.output_debug(
        f"Package path: {pkg_path}")

    vendor_processor = VendorProcessor(
        pkg_name, pkg_path, src_tarball, out_folder, pkg_version, vendor_version)

    vendor_processor.process_toml_file()


if __name__ == "__main__":
    main()
