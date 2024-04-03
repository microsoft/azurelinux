#!/usr/bin/python3
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

from pyrpm.spec import Spec

import re

VALID_SOURCE_ATTRIBUTIONS = {
    "Microsoft":                      r'\n-\s+(Original version for (CBL-Mariner|Azure Linux)|Initial (CBL-Mariner|Azure Linux) import from Azure)( \(license: MIT\))?(\.|\n|$)',
    "CentOS":                         r'\n-\s+Initial (CBL-Mariner|Azure Linux) import from CentOS \d+ \(license: MIT\)(\.|\n|$)',
    "Ceph source":                    r'\n-\s+Initial (CBL-Mariner|Azure Linux) import from Ceph source \(license: LGPLv2.1\)(\.|\n|$)',
    "Debian":                         r'\n-\s+Initial (CBL-Mariner|Azure Linux) import from Debian source package \(license: MIT\)(\.|\n|$)',
    "Netplan source":                 r'\n-\s+Initial (CBL-Mariner|Azure Linux) import from Netplan source \(license: GPLv3\)(\.|\n|$)',
    "Fedora":                         r'\n-\s+Initial (CBL-Mariner|Azure Linux) import from Fedora \d+ \(license: MIT\)(\.|\n|$)',
    "Fedora (Copyright Remi Collet)": r'\n-\s+Initial (CBL-Mariner|Azure Linux) import from Fedora \d+ \(license: CC-BY-SA\)(\.|\n|$)',
    "Fedora (ISC)":                   r'\n-\s+Initial (CBL-Mariner|Azure Linux) import from Fedora \d+ \(license: ISC\)(\.|\n|$)',
    "Magnus Edenhill Open Source":    r'\n-\s+Initial (CBL-Mariner|Azure Linux) import from Magnus Edenhill Open Source \(license: BSD\)(\.|\n|$)',
    "NVIDIA":                         r'\n-\s+Initial (CBL-Mariner|Azure Linux) import from NVIDIA \(license: (ASL 2\.0|GPLv2)\)(\.|\n|$)',
    "OpenEuler":                      r'\n-\s+Initial (CBL-Mariner|Azure Linux) import from OpenEuler \(license: BSD\)(\.|\n|$)',
    "OpenMamba":                      r'\n-\s+Initial (CBL-Mariner|Azure Linux) import from OpenMamba(\.|\n|$)',
    "OpenSUSE":                       r'\n-\s+Initial (CBL-Mariner|Azure Linux) import from openSUSE \w+ \(license: same as "License" tag\)(\.|\n|$)',
    "Photon":                         r'\n-\s+Initial (CBL-Mariner|Azure Linux) import from Photon \(license: Apache2\)(\.|\n|$)',
    "Sysbench source":                r'\n-\s+Initial (CBL-Mariner|Azure Linux) import from Sysbench source \(license: GPLv2\+\)(\.|\n|$)',
    "RPM software management source": r'\n-\s+Initial (CBL-Mariner|Azure Linux) import from RPM software management source \(license: GPLv2\+\)(\.|\n|$)',
    "Source project":                 r'\n-\s+Initial Azure Linux import from the source project \(license: same as "License" tag\)(\.|\n|$)',           
}

KNOWN_SOURCE_ORIGINS = VALID_SOURCE_ATTRIBUTIONS.keys()

valid_source_attributions_regex = { key : re.compile(value) for key, value in VALID_SOURCE_ATTRIBUTIONS.items() }

def get_spec_source(spec_path):
    spec = Spec.from_file(spec_path)

    for source, attribution_regex in valid_source_attributions_regex.items():
        if attribution_regex.findall(spec.changelog):
            return source

    return None
