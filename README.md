# CBL-Mariner

CBL-Mariner is an internal Linux distribution for Microsoft’s cloud infrastructure and edge products and services. CBL-Mariner is designed to provide a consistent platform for these devices and services and will enhance Microsoft’s ability to stay current on Linux updates. This initiative is part of Microsoft’s increasing investment in a wide range of Linux technologies, such as [SONiC](https://azure.microsoft.com/en-us/blog/sonic-the-networking-switch-software-that-powers-the-microsoft-global-cloud/) and [Windows Subsystem for Linux (WSL)](https://docs.microsoft.com/en-us/windows/wsl/about). CBL-Mariner is being shared publicly as part of Microsoft’s commitment to Open Source and to contribute back to the Linux community. CBL-Mariner does not change our approach or commitment to any existing third-party Linux distribution offerings.

CBL-Mariner has been engineered with the notion that a small common core set of packages can address the universal needs of first party cloud and edge services while allowing individual teams to layer additional packages on top of the common core to produce images for their workloads. This is made possible by a simple build system that enables:

- **Package Generation:** This produces the desired set of RPM packages from SPEC files and source files.
- **Image Generation:** This produces the desired image artifacts like ISOs or VHDs from a given set of packages.

Whether deployed as a container or a container host, CBL-Mariner consumes limited disk and memory resources. The lightweight characteristics of CBL-Mariner also provides faster boot times and a minimal attack surface. By focusing the features in the core image to just what is needed for our internal cloud customers there are fewer services to load, and fewer attack vectors.

When security vulnerabilities arise, CBL-Mariner supports both a package-based update model and an image based update model.  Leveraging the common [RPM Package Manager](https://rpm.org/) system, CBL-Mariner makes the latest security patches and fixes available for download with the goal of fast turn-around times.

## Getting Started with CBL-Mariner

### Build

Instructions for building CBL-Mariner may be found here: [Toolkit Documentation](./toolkit/README.md).

### ISO

You can try CBL-Mariner with the following ISO images:

- [Mariner 2.0 x86_64 ISO](https://aka.ms/mariner-2.0-x86_64-iso).

Before using a downloaded ISO, [verify the checksum and signature of the image](toolkit/docs/security/iso-image-verification.md).

After downloading the ISO, use [the quickstart instructions](toolkit/docs/quick_start/quickstart.md) to install and use the image in a Hyper-V VM.

Note: Support for the ISO is community based. Before filing a new bug or feature request, please search the list of Github Issues. If you are unable to find a matching issue, please report new bugs by clicking [here](https://github.com/microsoft/CBL-Mariner/issues) or create a new feature request by clicking [here](https://github.com/microsoft/CBL-Mariner/issues/new). For additional information refer to the [support.md](https://github.com/microsoft/CBL-Mariner/blob/2.0/SUPPORT.md) file.


## Getting Help
- Bugs, feature requests and questions can be filed as GitHub issues.
- We are starting a public community call for Mariner users to get together and discuss new features, provide feedback, and learn more about how others are using Mariner. In each session, we will feature a new demo. The schedule for the upcoming community calls are:
- 1/25/24 from 8-9am (PST) [Click to join](https://teams.microsoft.com/l/meetup-join/19%3ameeting_NGM1YWZiMDMtYWZkZi00NzBmLWExNjgtM2RkMjFmYTNiYmU2%40thread.v2/0?context=%7b%22Tid%22%3a%2272f988bf-86f1-41af-91ab-2d7cd011db47%22%2c%22Oid%22%3a%2230697089-15b8-4c68-b67e-7db9cd4f02ea%22%7d) 
- 3/28/24 from 8-9am (PST) [Click to join](https://teams.microsoft.com/l/meetup-join/19%3ameeting_NGM1YWZiMDMtYWZkZi00NzBmLWExNjgtM2RkMjFmYTNiYmU2%40thread.v2/0?context=%7b%22Tid%22%3a%2272f988bf-86f1-41af-91ab-2d7cd011db47%22%2c%22Oid%22%3a%2230697089-15b8-4c68-b67e-7db9cd4f02ea%22%7d) 
- 5/23/24 from 8-9am (PST) [Click to join](https://teams.microsoft.com/l/meetup-join/19%3ameeting_NGM1YWZiMDMtYWZkZi00NzBmLWExNjgtM2RkMjFmYTNiYmU2%40thread.v2/0?context=%7b%22Tid%22%3a%2272f988bf-86f1-41af-91ab-2d7cd011db47%22%2c%22Oid%22%3a%2230697089-15b8-4c68-b67e-7db9cd4f02ea%22%7d) 
- 7/25/24 from 8-9am (PST) [Click to join](https://teams.microsoft.com/l/meetup-join/19%3ameeting_NGM1YWZiMDMtYWZkZi00NzBmLWExNjgtM2RkMjFmYTNiYmU2%40thread.v2/0?context=%7b%22Tid%22%3a%2272f988bf-86f1-41af-91ab-2d7cd011db47%22%2c%22Oid%22%3a%2230697089-15b8-4c68-b67e-7db9cd4f02ea%22%7d) 
- 9/26/24 from 8-9am (PST) [Click to join](https://teams.microsoft.com/l/meetup-join/19%3ameeting_NGM1YWZiMDMtYWZkZi00NzBmLWExNjgtM2RkMjFmYTNiYmU2%40thread.v2/0?context=%7b%22Tid%22%3a%2272f988bf-86f1-41af-91ab-2d7cd011db47%22%2c%22Oid%22%3a%2230697089-15b8-4c68-b67e-7db9cd4f02ea%22%7d)

## Trademarks

This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft trademarks or logos is subject to and must follow [Microsoft's Trademark & Brand Guidelines](https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks/usage/general). Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship. Any use of third-party trademarks or logos are subject to those third-party's policies.

## Acknowledgments

Any Linux distribution, including CBL-Mariner, benefits from contributions by the open software community. We gratefully acknowledge all contributions made from the broader open source community, in particular:

1) The [Photon OS Project](https://vmware.github.io/photon/) for SPEC files originating from the Photon distribution.

2) [The Fedora Project](https://start.fedoraproject.org/) for SPEC files, particularly with respect to Qt, DNF and content in the SPECS-EXTENDED folder.

3) [GNU](https://www.gnu.org/) and the [Free Software Foundation](https://www.fsf.org/)

4) [Linux from Scratch](http://www.linuxfromscratch.org)

5) [Openmamba](https://openmamba.org/en/) for SPEC files
