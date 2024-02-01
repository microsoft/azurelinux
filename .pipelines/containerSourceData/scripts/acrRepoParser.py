#!/usr/bin/python3
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

"""
This script is used to parse the ACR repo config file and set ADO variables based on the input parameters.

Required input parameters:
    --config-file-path
    --image-name

Optional input parameters:
    --git-branch
    --publishing-level
    --output-file-path

Sets the following ADO variables:
    1. data_is_core_image
    2. data_is_golden_image
    3. data_is_hci_golden_image
    4. data_architecture_to_build
    5. data_repo_prefix
    6. data_can_build_for_branch
    7. data_target_acr

With only image name, you can get ADO variables from 1 - 5 set.
With git branch, you can get ADO variable 6 set.
With git branch and publishing level, you can get ADO variable 7 set.

If --output-file-path is provided, the ADO variables will be written to the file in JSON format.

Unset variables will default to either False for bool type and empty string for str type.
"""

import argparse
import json
from pathlib import PosixPath


# String constants
GOLDEN_IMAGES_KEY = "goldenImages"
HCI_IMAGES_KEY = "hciGoldenImages"
CORE_IMAGES_KEY = "coreImages"
TARGET_ACR_KEY = "targetACRs"
BRANCHES_KEY = "allowedBranches"
ARCHITECTURE_KEY = "architecture"
REPO_PREFIX_KEY = "repoPrefix"
DEV_PUBLISH_KEY = "development"
HCI_REDIRECT_KEY = "hciRedirect"
PREVIEW_PUBLISH_KEY = "preview"
PROD_PUBLISH_KEY = "production"
GOLDEN_IMAGE_BRANCHES_KEY = "GoldenImageAllowedBranches"
HCI_IMAGE_BRANCHES_KEY = "HciImageAllowedBranches"
CORE_IMAGE_BRANCHES_KEY = "CoreImageAllowedBranches"


class ADORepoData:
    def __init__(self) -> None:
        self.data_is_core_image: bool
        self.data_is_golden_image: bool
        self.data_is_hci_golden_image: bool
        self.data_architecture_to_build: str
        self.data_repo_prefix: str
        self.data_can_build_for_branch: bool
        self.data_target_acr: str


class ACRRepoConfig:
    def __init__(self, config_file_path: PosixPath):
        if not config_file_path.exists():
            raise ValueError(f"config file {config_file_path} not found")

        self.__config_dict: dict = {}

        with open(config_file_path, "r") as config_file:
            config = json.load(config_file)

            for key in config.keys():
                if key == GOLDEN_IMAGES_KEY:
                    self.__config_dict[GOLDEN_IMAGES_KEY] = config[GOLDEN_IMAGES_KEY]
                elif key == HCI_IMAGES_KEY:
                    self.__config_dict[HCI_IMAGES_KEY] = config[HCI_IMAGES_KEY]
                elif key == CORE_IMAGES_KEY:
                    self.__config_dict[CORE_IMAGES_KEY] = config[CORE_IMAGES_KEY]
                elif key == TARGET_ACR_KEY:
                    self.__config_dict[TARGET_ACR_KEY] = config[TARGET_ACR_KEY]

            for key in config[GOLDEN_IMAGES_KEY]:
                if key == BRANCHES_KEY:
                    self.__config_dict[GOLDEN_IMAGE_BRANCHES_KEY] = config[
                        GOLDEN_IMAGES_KEY
                    ][key]
                else:
                    self.__config_dict[key] = config[GOLDEN_IMAGES_KEY][key]

            for key in config[HCI_IMAGES_KEY]:
                if key == BRANCHES_KEY:
                    self.__config_dict[HCI_IMAGE_BRANCHES_KEY] = config[HCI_IMAGES_KEY][
                        key
                    ]
                else:
                    self.__config_dict[key] = config[HCI_IMAGES_KEY][key]

            for key in config[CORE_IMAGES_KEY]:
                if key == BRANCHES_KEY:
                    self.__config_dict[CORE_IMAGE_BRANCHES_KEY] = config[
                        CORE_IMAGES_KEY
                    ][key]
                else:
                    self.__config_dict[key] = config[CORE_IMAGES_KEY][key]

    def is_core_image(self, image_name) -> bool:
        return image_name in self.__config_dict.get(CORE_IMAGES_KEY)

    def is_golden_image(self, image_name) -> bool:
        golden_images = self.__config_dict.get(GOLDEN_IMAGES_KEY)
        hci_golden_images = self.__config_dict.get(HCI_IMAGES_KEY)
        return image_name in golden_images or image_name in hci_golden_images

    def is_hci_golden_image(self, image_name) -> bool:
        return image_name in self.__config_dict.get(HCI_IMAGES_KEY)

    def get_architecture_to_build(self, image_name) -> str:
        if not image_name in self.__config_dict:
            return ""

        image_data = self.__config_dict.get(image_name)

        if not image_data is None and ARCHITECTURE_KEY in image_data:
            return image_data[ARCHITECTURE_KEY]

        return ""

    def get_repo_prefix(self, image_name) -> str:
        if not image_name in self.__config_dict:
            return ""

        image_data = self.__config_dict.get(image_name)

        if not image_data is None and REPO_PREFIX_KEY in image_data:
            return image_data[REPO_PREFIX_KEY]

        return ""

    def is_branch_allowed_to_build(self, image_name, git_branch) -> bool:
        if not git_branch or len(git_branch) < 1:
            return False

        if not image_name in self.__config_dict:
            return False

        if self.is_core_image(image_name):
            return git_branch in self.__config_dict.get(CORE_IMAGE_BRANCHES_KEY)

        if self.is_hci_golden_image(image_name):
            return git_branch in self.__config_dict.get(HCI_IMAGE_BRANCHES_KEY)

        if self.is_golden_image(image_name):
            return git_branch in self.__config_dict.get(GOLDEN_IMAGE_BRANCHES_KEY)

        return False

    def get_target_acr(self, image_name, git_branch, publishing_level) -> str:
        if not image_name in self.__config_dict:
            return ""

        if not self.is_branch_allowed_to_build(image_name, git_branch):
            return ""

        target_acr = self.__config_dict.get(TARGET_ACR_KEY)
        if not target_acr is None and git_branch in target_acr:
            acr_data = target_acr.get(git_branch)
            if (
                self.is_hci_golden_image(image_name)
                and publishing_level == DEV_PUBLISH_KEY
                and HCI_REDIRECT_KEY in acr_data
            ):
                return acr_data.get(HCI_REDIRECT_KEY)

            return acr_data.get(publishing_level)

        return ""


def read_args():
    parser = argparse.ArgumentParser(
        description="Reads arguments to get ACR repo mapping data.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--config-file-path",
        required=True,
        type=str,
        help="Path to ACR repo config file (e.g., ./acrRepo.json).",
    )
    parser.add_argument(
        "--image-name",
        required=True,
        type=str,
        help="Container image name (e.g., base, nodejs, python, etc.).",
    )
    parser.add_argument(
        "--git-branch",
        required=False,
        type=str,
        help="CBL-Mariner Core repo branch name (e.g., 2.0, 3.0, main, 3.0-dev, topic, etc.).",
    )
    parser.add_argument(
        "--publishing-level",
        required=False,
        type=str,
        help="Publishing level (e.g., production, preview, development).",
    )
    parser.add_argument(
        "--output-file-path",
        required=False,
        type=str,
        help="Output file path to write the ACR repo mapping data (e.g., ./output.json).",
    )
    return parser.parse_args()


def print_args(args):
    print(f"ACR Repo File Path: {args.config_file_path}")
    print(f"Git Branch Name:    {args.git_branch}")
    print(f"Publishing Level:   {args.publishing_level}")
    print(f"Image Name:         {args.image_name}")
    print(f"Output File Path:   {args.output_file_path}")


def set_ado_variables(ado_repo: ADORepoData):
    print(
        f"##vso[task.setvariable variable=data_is_core_image;isoutput=true]{ado_repo.data_is_core_image}"
    )
    print(
        f"##vso[task.setvariable variable=data_is_golden_image;isoutput=true]{ado_repo.data_is_golden_image}"
    )
    print(
        f"##vso[task.setvariable variable=data_is_hci_golden_image;isoutput=true]{ado_repo.data_is_hci_golden_image}"
    )
    print(
        f"##vso[task.setvariable variable=data_architecture_to_build;isoutput=true]{ado_repo.data_architecture_to_build}"
    )
    print(
        f"##vso[task.setvariable variable=data_repo_prefix;isoutput=true]{ado_repo.data_repo_prefix}"
    )
    print(
        f"##vso[task.setvariable variable=data_can_build_for_branch;isoutput=true]{ado_repo.data_can_build_for_branch}"
    )
    print(
        f"##vso[task.setvariable variable=data_target_acr;isoutput=true]{ado_repo.data_target_acr}"
    )


def write_to_output_file(ado_repo: ADORepoData):
    with open(args.output_file_path, "w") as output_file:
        output_file.write(json.dumps(ado_repo.__dict__))


""" Main execution begins here """
if __name__ == "__main__":
    args = read_args()
    print_args(args)
    acr_repo_config = ACRRepoConfig(PosixPath(args.config_file_path))
    ado_repo = ADORepoData()
    ado_repo.data_is_core_image = acr_repo_config.is_core_image(args.image_name)
    ado_repo.data_is_golden_image = acr_repo_config.is_golden_image(args.image_name)
    ado_repo.data_is_hci_golden_image = acr_repo_config.is_hci_golden_image(
        args.image_name
    )
    ado_repo.data_architecture_to_build = acr_repo_config.get_architecture_to_build(
        args.image_name
    )
    ado_repo.data_repo_prefix = acr_repo_config.get_repo_prefix(args.image_name)
    ado_repo.data_can_build_for_branch = acr_repo_config.is_branch_allowed_to_build(
        args.image_name, args.git_branch
    )
    ado_repo.data_target_acr = acr_repo_config.get_target_acr(
        args.image_name, args.git_branch, args.publishing_level
    )

    set_ado_variables(ado_repo)

    if args.output_file_path:
        write_to_output_file(ado_repo)
