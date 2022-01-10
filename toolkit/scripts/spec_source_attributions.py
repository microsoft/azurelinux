#!/usr/bin/python3
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

from pyrpm.spec import Spec

import re

VALID_SOURCE_ATTRIBUTIONS = {
    "Microsoft":                    r'\n-\s+(Original version for CBL-Mariner|Initial CBL-Mariner import from Azure)( \(license: MIT\))?(\.|\n|$)',
    "CentOS":                       r'\n-\s+Initial CBL-Mariner import from CentOS \d+ \(license: MIT\)(\.|\n|$)',
    "Ceph source":                  r'\n-\s+Initial CBL-Mariner import from Ceph source \(license: LGPLv2.1\)(\.|\n|$)',
    "Fedora":                       r'\n-\s+Initial CBL-Mariner import from Fedora \d+ \(license: MIT\)(\.|\n|$)',
    "Magnus Edenhill Open Source":  r'\n-\s+Initial CBL-Mariner import from Magnus Edenhill Open Source \(license: BSD\)(\.|\n|$)',
    "NVIDIA":                       r'\n-\s+Initial CBL-Mariner import from NVIDIA \(license: ASL 2\.0\)(\.|\n|$)',
    "OpenMamba":                    r'\n-\s+Initial CBL-Mariner import from OpenMamba(\.|\n|$)',
    "OpenSUSE":                     r'\n-\s+Initial CBL-Mariner import from openSUSE \w+ \(license: same as "License" tag\)(\.|\n|$)',
    "Photon":                       r'\n-\s+Initial CBL-Mariner import from Photon \(license: Apache2\)(\.|\n|$)'
}

KNOWN_SOURCE_ORIGINS = VALID_SOURCE_ATTRIBUTIONS.keys()

valid_source_attributions_regex = { key : re.compile(value) for key, value in VALID_SOURCE_ATTRIBUTIONS.items() }

def get_spec_source(spec_path):
    spec = Spec.from_file(spec_path)

    for source, attribution_regex in valid_source_attributions_regex.items():
        if attribution_regex.findall(spec.changelog):
            return source

    return None
