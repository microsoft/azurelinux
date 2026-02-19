# Azure Linux

Azure Linux is an internal Linux distribution for Microsoft’s cloud infrastructure and edge products and services. Azure Linux is designed to provide a consistent platform for these devices and services and will enhance Microsoft’s ability to stay current on Linux updates. This initiative is part of Microsoft’s increasing investment in a wide range of Linux technologies, such as [SONiC](https://azure.microsoft.com/en-us/blog/sonic-the-networking-switch-software-that-powers-the-microsoft-global-cloud/) and [Windows Subsystem for Linux (WSL)](https://docs.microsoft.com/en-us/windows/wsl/about). Azure Linux is being shared publicly as part of Microsoft’s commitment to Open Source and to contribute back to the Linux community. Azure Linux does not change our approach or commitment to any existing third-party Linux distribution offerings.

Azure Linux has been engineered with the notion that a small common core set of packages can address the universal needs of first party cloud and edge services while allowing individual teams to layer additional packages on top of the common core to produce images for their workloads. This is made possible by a simple build system that enables:

- **Package Generation:** This produces the desired set of RPM packages from SPEC files and source files.
- **Image Generation:** This produces the desired image artifacts like ISOs or VHDs from a given set of packages.

Whether deployed as a container or a container host, Azure Linux consumes limited disk and memory resources. The lightweight characteristics of Azure Linux also provides faster boot times and a minimal attack surface. By focusing the features in the core image to just what is needed for our internal cloud customers there are fewer services to load, and fewer attack vectors.

When security vulnerabilities arise, Azure Linux supports both a package-based update model and an image based update model.  Leveraging the common [RPM Package Manager](https://rpm.org/) system, Azure Linux makes the latest security patches and fixes available for download with the goal of fast turn-around times.

## Getting Started with Azure Linux

NOTE: Looking for CBL-Mariner 2.0 Source?  Click [here](https://github.com/microsoft/azurelinux/tree/2.0)

### Build

Instructions for building Azure Linux 3.0 may be found here: [Toolkit Documentation](./toolkit/README.md).

### ISO

To try Azure Linux Download the ISO here: [Azure Linux 3.0 x86_64 ISO](https://aka.ms/azurelinux-3.0-x86_64.iso) / [Azure Linux 3.0 aarch64 ISO](https://aka.ms/azurelinux-3.0-aarch64.iso)

Before using a downloaded ISO, [verify the checksum and signature of the image](toolkit/docs/security/iso-image-verification.md).

After downloading the ISO, use [the quickstart instructions](toolkit/docs/quick_start/quickstart.md) to install and use the image in a Hyper-V VM.

Note: Support for the ISO is community based. Before filing a new bug or feature request, please search the list of Github Issues. If you are unable to find a matching issue, please report new bugs by clicking [here](https://github.com/microsoft/azurelinux/issues) or create a new feature request by clicking [here](https://github.com/microsoft/azurelinux/issues/new). For additional information refer to the [support.md](https://github.com/microsoft/azurelinux/blob/3.0/SUPPORT.md) file.

### OCI

There are also Azure Linux OCI images available to use or create your own images by referencing `mcr.microsoft.com/azurelinux/base/core:3.0` in your Containerfile. 

See [here](https://mcr.microsoft.com/en-us/artifact/mar/azurelinux/base/core/about) which other tags are available.


## Getting Help
- Bugs, feature requests and questions can be filed as GitHub issues.
- We are starting a public community call for Azure Linux users to get together and discuss new features, provide feedback, and learn more about how others are using Azure Linux. In each session, we will feature a new demo. The schedule for the upcoming community calls are:
- 7/24/2025 from 8-9am (PST) [Click to join](https://teams.microsoft.com/l/meetup-join/19%3ameeting_ZDcyZjRkYWMtOWQxYS00OTk3LWFhNmMtMTMwY2VhMTA4OTZi%40thread.v2/0?context=%7b%22Tid%22%3a%2272f988bf-86f1-41af-91ab-2d7cd011db47%22%2c%22Oid%22%3a%2271a6ce92-58a5-4ea0-96f4-bd4a0401370a%22%7d)
- 9/25/2025 from 8-9am (PST) [Click to join](https://teams.microsoft.com/l/meetup-join/19%3ameeting_ZDcyZjRkYWMtOWQxYS00OTk3LWFhNmMtMTMwY2VhMTA4OTZi%40thread.v2/0?context=%7b%22Tid%22%3a%2272f988bf-86f1-41af-91ab-2d7cd011db47%22%2c%22Oid%22%3a%2271a6ce92-58a5-4ea0-96f4-bd4a0401370a%22%7d)
- 11/20/2025 from 8-9am (PST) [Click to join](https://teams.microsoft.com/l/meetup-join/19%3ameeting_ZDcyZjRkYWMtOWQxYS00OTk3LWFhNmMtMTMwY2VhMTA4OTZi%40thread.v2/0?context=%7b%22Tid%22%3a%2272f988bf-86f1-41af-91ab-2d7cd011db47%22%2c%22Oid%22%3a%2271a6ce92-58a5-4ea0-96f4-bd4a0401370a%22%7d)
- 1/22/2026 from 8-9am (PST) [Click to join](https://teams.microsoft.com/l/meetup-join/19%3ameeting_ZDcyZjRkYWMtOWQxYS00OTk3LWFhNmMtMTMwY2VhMTA4OTZi%40thread.v2/0?context=%7b%22Tid%22%3a%2272f988bf-86f1-41af-91ab-2d7cd011db47%22%2c%22Oid%22%3a%2271a6ce92-58a5-4ea0-96f4-bd4a0401370a%22%7d)
- 3/26/2026 from 8-9am (PST) [Click to join](https://teams.microsoft.com/l/meetup-join/19%3ameeting_ZDcyZjRkYWMtOWQxYS00OTk3LWFhNmMtMTMwY2VhMTA4OTZi%40thread.v2/0?context=%7b%22Tid%22%3a%2272f988bf-86f1-41af-91ab-2d7cd011db47%22%2c%22Oid%22%3a%2271a6ce92-58a5-4ea0-96f4-bd4a0401370a%22%7d)

## Trademarks

This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft trademarks or logos is subject to and must follow [Microsoft's Trademark & Brand Guidelines](https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks/usage/general). Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship. Any use of third-party trademarks or logos are subject to those third-party's policies.

## Acknowledgments

Any Linux distribution, including Azure Linux, benefits from contributions by the open software community. We gratefully acknowledge all contributions made from the broader open source community, in particular:

1) [GNU](https://www.gnu.org/) and the [Free Software Foundation](https://www.fsf.org/)

2) [The Fedora Project](https://start.fedoraproject.org/) for SPEC files, particularly with respect to Qt, DNF and content in the SPECS-EXTENDED folder.

3) The [Photon OS Project](https://vmware.github.io/photon/) for SPEC files originating from the Photon distribution.

4) [Linux from Scratch](http://www.linuxfromscratch.org)

5) And other open source projects as referenced [here](LICENSES-AND-NOTICES/SPECS/LICENSES-MAP.md)
