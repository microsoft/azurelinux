#!/bin/bash

# Import the RPM Metadata Key
rpm --import /etc/pki/rpm-gpg/MICROSOFT-METADATA-GPG-KEY

# Import the RPM GPG Key
rpm --import /etc/pki/rpm-gpg/MICROSOFT-RPM-GPG-KEY
