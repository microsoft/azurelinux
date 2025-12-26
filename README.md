# Azure Linux

Azure Linux is an internal Linux distribution for Microsoft’s cloud infrastructure and edge products and services. Azure Linux is designed to provide a consistent platform for these devices and services and will enhance Microsoft’s ability to stay current on Linux updates. This initiative is part of Microsoft’s increasing investment in a wide range of Linux technologies, such as [SONiC](https://azure.microsoft.com/en-us/blog/sonic-the-networking-switch-software-that-powers-the-microsoft-global-cloud/) and [Windows Subsystem for Linux (WSL)](https://docs.microsoft.com/en-us/windows/wsl/about). Azure Linux is being shared publicly as part of Microsoft’s commitment to Open Source and to contribute back to the Linux community. Azure Linux does not change our approach or commitment to any existing third-party Linux distribution offerings.

Azure Linux has been engineered with the notion that a small common core set of packages can address the universal needs of first party cloud and edge services while allowing individual teams to layer additional packages on top of the common core to produce images for their workloads. This is made possible by a simple build system that enables:

- **Package Generation:** This produces the desired set of RPM packages from SPEC files and source files.
- **Image Generation:** This produces the desired image artifacts like ISOs or VHDs from a given set of packages.

Whether deployed as a container or a container host, Azure Linux consumes limited disk and memory resources. The lightweight characteristics of Azure Linux also provides faster boot times and a minimal attack surface. By focusing the features in the core image to just what is needed for our internal cloud customers there are fewer services to load, and fewer attack vectors.

When security vulnerabilities arise, Azure Linux supports both a package-based update model and an image based update model.  Leveraging the common [RPM Package Manager](https://rpm.org/) system, Azure Linux makes the latest security patches and fixes available for download with the goal of fast turn-around times.
