#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

"""Run with python3 -m unittest discover -s .pipelines/containerSourceData/scripts/tests."""

import os
from pathlib import Path
import shlex
import subprocess
import tempfile
import unittest


SCRIPTS = Path(__file__).resolve().parents[1]
GOLDEN_SCRIPT = (SCRIPTS / "BuildGoldenContainer.sh").read_text()
COMMON_SCRIPT = shlex.quote(str(SCRIPTS / "BuildContainerCommonSteps.sh"))
GOLDEN_FUNCTIONS = GOLDEN_SCRIPT[
    GOLDEN_SCRIPT.index("function print_inputs"):
    GOLDEN_SCRIPT.index('\nsource "$CONTAINER_SRC_DIR/scripts/BuildContainerCommonSteps.sh"')
]
GOLDEN_ARGUMENTS = GOLDEN_SCRIPT[:GOLDEN_SCRIPT.index('echo "+++ Create temp folder"')]


class GoldenImageTagTests(unittest.TestCase):
    def run_bash(self, script, *, env=None, args=()):
        environment = os.environ.copy()
        environment.pop("BUILD_BUILDNUMBER", None)
        environment.update(env or {})
        return subprocess.run(
            ["bash", "-c", script, "test", *args],
            env=environment,
            text=True,
            capture_output=True,
            check=False,
        )

    def setup_script(self, build_number, arch="amd64", base_version="3.0"):
        build_number_assignment = (
            "" if build_number is None
            else f"RELEASE_BUILD_NUMBER={shlex.quote(build_number)}"
        )
        return f"""
set -e
source {COMMON_SCRIPT}
{GOLDEN_FUNCTIONS}
BASE_IMAGE_NAME_FULL=mcr.microsoft.com/azurelinux/base/core:{base_version}.20261022-{arch}
ACR=example
REPO_PREFIX=public/azurelinux
REPOSITORY=base/python
PUBLISHING_LEVEL=preview
{build_number_assignment}
initialization
set_release_image_tag
"""

    def test_recorded_stage6_and_bridge_trigger_inputs(self):
        cases = (
            (
                "stage6",
                "3.0.20261022-fasttrack-1232578",
                "cblmarineracr2mcrpreview.azurecr.io/public/azurelinux/base/core",
                "3.12.15-1",
                "20261022",
            ),
            (
                "bridge",
                "3.0.20261025-fasttrack-1236358",
                "mcr.microsoft.com/azurelinux/base/core",
                "3.12.15-3",
                "20261025",
            ),
        )
        for trigger, number, base_name, component_version, expected_date in cases:
            for arch in ("amd64", "arm64"):
                with self.subTest(trigger=trigger, arch=arch):
                    base_image = f"{base_name}:3.0.20261022-{arch}"
                    setup = self.setup_script(None, arch).replace(
                        f"mcr.microsoft.com/azurelinux/base/core:3.0.20261022-{arch}",
                        base_image,
                    )
                    result = self.run_bash(
                        GOLDEN_ARGUMENTS + setup + f"""
docker() {{
    case "$1" in
        run) echo test-container ;;
        exec) echo {component_version} ;;
    esac
}}
VERSION_EXTRACT_CMD=version
IS_HCI_IMAGE=false
set_image_tag
printf 'RESULT:%s|%s\\n' "$CONTAINER_IMAGE_NAME_FINAL" "$BASE_IMAGE_NAME_FULL"
""",
                        env={"BUILD_BUILDNUMBER": number},
                    )
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertIn(
                        "RESULT:example.azurecr.io/public/azurelinux/base/python:"
                        f"{component_version}-azl3.0.{expected_date}-{arch}|{base_image}",
                        result.stdout,
                    )

    def test_upstream_date_replaces_only_the_output_date(self):
        for arch in ("amd64", "arm64"):
            for build_number in (
                "3.0.20261025-fasttrack-1236358",
                "3.0.20261025-3.0",
                "3.0.20261025",
                "3.0.20261025.1",
                "3.0.20261025-dev-1236358",
            ):
                with self.subTest(arch=arch, build_number=build_number):
                    result = self.run_bash(self.setup_script(build_number, arch) + """
printf 'RESULT:%s|%s|%s|%s\\n' "$CONTAINER_IMAGE_TAG" "$BASE_IMAGE_NAME_FULL" "$BASE_IMAGE_TAG" "$AZURE_LINUX_VERSION"
""")
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertIn(
                        f"RESULT:3.0.20261025-{arch}|"
                        f"mcr.microsoft.com/azurelinux/base/core:3.0.20261022-{arch}|"
                        f"3.0.20261022-{arch}|3.0",
                        result.stdout,
                    )

    def test_azure_linux_two_and_leap_day(self):
        result = self.run_bash(
            self.setup_script("2.0.20240229-fasttrack-123", base_version="2.0")
            + 'printf "RESULT:%s\\n" "$CONTAINER_IMAGE_TAG"'
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("RESULT:2.0.20240229-amd64", result.stdout)

    def test_fresh_base_keeps_the_existing_tag_shape(self):
        result = self.run_bash(
            self.setup_script("3.0.20261022-3.0")
            + 'printf "RESULT:%s\\n" "$CONTAINER_IMAGE_TAG"'
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("RESULT:3.0.20261022-amd64", result.stdout)

    def test_missing_or_invalid_release_fails_without_falling_back(self):
        for build_number in (
            "", "20261025.1", "3.0", "3.0.2026102", "3.0.202610250",
            "3.0.20260230-fasttrack-123", "3.0.20261301", "3.0.20250229",
            "2.0.20261025-fasttrack-123",
        ):
            with self.subTest(build_number=build_number):
                result = self.run_bash(self.setup_script(build_number))
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("Error -", result.stderr)
                self.assertNotIn("Container Build Tag", result.stdout)

    def test_invalid_base_tag_fails(self):
        for tag in ("3.0", "3.0.20261022", "3.0.20261022-s390x"):
            with self.subTest(tag=tag):
                script = self.setup_script("3.0.20261025").replace(
                    "core:3.0.20261022-amd64", f"core:{tag}"
                )
                result = self.run_bash(script)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("Error - Base image tag", result.stderr)

    def test_pipeline_build_number_and_standalone_override(self):
        cases = (
            ({"BUILD_BUILDNUMBER": "3.0.20261025-fasttrack-1236358"}, (), "3.0.20261025-fasttrack-1236358"),
            ({}, ("-x", "3.0.20261025-3.0"), "3.0.20261025-3.0"),
            ({"BUILD_BUILDNUMBER": "3.0.20261022"}, ("-x", "3.0.20261025"), "3.0.20261025"),
        )
        for env, args, expected in cases:
            with self.subTest(env=env, args=args):
                result = self.run_bash(
                    GOLDEN_ARGUMENTS + '\nprintf "RESULT:%s\\n" "$RELEASE_BUILD_NUMBER"',
                    env=env,
                    args=args,
                )
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn(f"RESULT:{expected}", result.stdout)
        result = self.run_bash(GOLDEN_ARGUMENTS, args=("-x",))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("requires an argument", result.stderr)

    def test_standard_and_hci_tags_and_artifact_list(self):
        for arch in ("amd64", "arm64"):
            for hci in ("true", "false"):
                with self.subTest(arch=arch, hci=hci), tempfile.TemporaryDirectory() as output:
                    result = self.run_bash(
                        self.setup_script("3.0.20261025-fasttrack-1236358", arch)
                        + f"""
docker() {{
    case "$1" in
        run) echo test-container ;;
        exec) echo 3.12.15-3 ;;
    esac
}}
VERSION_EXTRACT_CMD=version
IS_HCI_IMAGE={hci}
IMAGE=python
OUTPUT_DIR={shlex.quote(output)}
PUBLISH_TO_ACR=false
CREATE_SBOM=false
set_image_tag
finalize
"""
                    )
                    self.assertEqual(result.returncode, 0, result.stderr)
                    separator = "." if hci == "true" else "-azl"
                    self.assertEqual(
                        (Path(output) / "PublishedContainers-python.txt").read_text().strip(),
                        f"example.azurecr.io/public/azurelinux/base/python:"
                        f"3.12.15-3{separator}3.0.20261025-{arch}",
                    )

    def test_all_distroless_variants_preserve_the_base_image(self):
        for arch in ("amd64", "arm64"):
            with self.subTest(arch=arch), tempfile.TemporaryDirectory() as work:
                work_path = Path(work)
                output = work_path / "output"
                output.mkdir()
                result = self.run_bash(
                    self.setup_script("3.0.20261025-fasttrack-1236358", arch)
                    + f"""
source {shlex.quote(str(SCRIPTS / "BuildGoldenDistrolessContainer.sh"))}
WORK_DIR={shlex.quote(work)}
OUTPUT_DIR={shlex.quote(str(output))}
CONTAINER_SRC_DIR={shlex.quote(str(SCRIPTS.parent))}
IMAGE=python
PACKAGE_FILE=python.pkg
COMPONENT_VERSION=3.12.15-3
PUBLISH_TO_ACR=false
git() {{
    mkdir -p "$3/dockerfiles"
    printf 'FROM original as builder\\n' > "$3/dockerfiles/dockerfile-new-image"
}}
DockerBuild() {{ printf 'BUILD:%s\\n' "$1"; }}
create_distroless_container
"""
                )
                self.assertEqual(result.returncode, 0, result.stderr)
                expected = [
                    "example.azurecr.io/public/azurelinux/distroless/python:"
                    f"3.12.15-3{variant}-azl3.0.20261025-{arch}"
                    for variant in ("", "-debug", "-nonroot", "-debug-nonroot")
                ]
                self.assertEqual(
                    (output / "PublishedContainers-python.txt").read_text().splitlines(),
                    expected,
                )
                self.assertIn(
                    f"FROM mcr.microsoft.com/azurelinux/marinara:3.0.20261022-{arch} as builder",
                    (work_path / "marinara-src/dockerfiles/dockerfile-new-image").read_text(),
                )

    def test_sbom_uses_release_date_without_changing_other_callers(self):
        for golden in (True, False):
            with self.subTest(golden=golden), tempfile.TemporaryDirectory() as work:
                work_path = Path(work)
                sbom_script = work_path / "sbom.sh"
                sbom_script.write_text(
                    'printf "%s\\n" "$@" > "$OUTPUT_DIR/sbom-arguments.txt"\n'
                    'mkdir -p "$1/_manifest/spdx_2.2"\n'
                    'touch "$1/_manifest/spdx_2.2/manifest.spdx.json"\n'
                )
                setup = self.setup_script("3.0.20261025")
                if not golden:
                    setup = setup.removesuffix("set_release_image_tag\n")
                result = self.run_bash(setup + f"""
export OUTPUT_DIR={shlex.quote(work)}
CREATE_SBOM=true
COMPONENT=python3
COMPONENT_VERSION=3.12.15-3
CONTAINER_IMAGE_NAME_FINAL=example.azurecr.io/base/python:example
SBOM_SCRIPT={shlex.quote(str(sbom_script))}
SBOM_TOOL_PATH=tool
sudo() {{ "$@"; }}
generate_image_sbom
""")
                self.assertEqual(result.returncode, 0, result.stderr)
                arguments = (work_path / "sbom-arguments.txt").read_text().splitlines()
                date = "20261025" if golden else "20261022"
                self.assertEqual(arguments[-1], f"3.12.15-3-azl3.0.{date}-amd64")
                self.assertEqual(
                    arguments[-2], "mcr.microsoft.com/azurelinux/base/core-python3"
                )


if __name__ == "__main__":
    unittest.main()
