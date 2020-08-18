# CBL-Mariner

CBL-Mariner is an internal Linux distribution for Microsoft’s cloud infrastructure and edge products and services. CBL-Mariner is designed to provide a consistent platform for these devices and services and will enhance Microsoft’s ability to stay current on Linux updates. This initiative is part of Microsoft’s increasing investment in a wide range of Linux technologies, such as [SONiC](https://azure.microsoft.com/en-us/blog/sonic-the-networking-switch-software-that-powers-the-microsoft-global-cloud/), [Azure Sphere OS](https://docs.microsoft.com/en-us/azure-sphere/product-overview/what-is-azure-sphere) and [Windows Subsystem for Linux (WSL)](https://docs.microsoft.com/en-us/windows/wsl/about). CBL-Mariner is being shared publicly as part of Microsoft’s commitment to Open Source and to contribute back to the Linux community. CBL-Mariner is not being offered commercially as a solution for servers, PCs, or IoT devices nor is it included as an IaaS offering. CBL-Mariner does not change our approach or commitment to any existing third-party Linux distribution offerings. 

CBL-Mariner has been engineered with the notion that a small common core set of packages can address the universal needs of first party cloud and edge services while allowing individual teams to layer additional packages on top of the common core to produce images for their workloads. This is made possible by a simple build system that enables:

- **Package Generation:** This produces the desired set of RPM packages from SPEC files and source files. 
- **Image Generation:** This produces the desired image artifacts like ISOs or VHDs from a given set of packages. 

Whether deployed as a container or a container host, CBL-Mariner consumes limited disk and memory resources. The lightweight characteristics of CBL-Mariner also provides faster boot times and a minimal attack surface. By focusing the features in the core image to just what is needed for our internal cloud customers there are fewer services to load, and fewer attack vectors. 

When security vulnerabilities arise, CBL-Mariner supports both a package-based update model and an image based update model.  Leveraging the common [RPM Package Manager](https://rpm.org/) system, CBL-Mariner makes the latest security patches and fixes available for download with the goal of fast turn-around times.   

# Getting Started with CBL-Mariner: 

CBL-Mariner is not released for commercial use, but we understand developers may be interested to examine what we have built.  Instructions for building CBL-Mariner may be found here: [Toolkit Documentation](./toolkit/README.md)

# Acknowledgments 

Any Linux distribution, including CBL-Mariner, benefits from contributions by the open software community. We gratefully acknowledge all contributions made from the broader open source community, in particular:

1) The [Photon OS Project](https://vmware.github.io/photon/) for SPEC files originating from the Photon distribution.   

2) [The Fedora Project](https://start.fedoraproject.org/) for SPEC files, particularly with respect to QT, DNF and several of their dependencies. 

3) [GNU](https://www.gnu.org/) and the [Free Software Foundation](https://www.fsf.org/)

4) [Linux from Scratch](http://www.linuxfromscratch.org)

