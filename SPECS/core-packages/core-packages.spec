Summary:        Metapackage with core sets of packages
Name:           core-packages
Version:        2.0
Release:        8%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Base
URL:            https://aka.ms/mariner

%description
Metapackage holding sets of core packages for different applications.

%package        base-image
Summary:        Metapackage defining the basic set of packages (no kernel) used by images such as VHDs, VHDXs and ISOs.
Requires:       %{name}-container = %{version}-%{release}
Requires:       bc
Requires:       bridge-utils
Requires:       chrony
Requires:       cpio
Requires:       cracklib-dicts
Requires:       cryptsetup
Requires:       dbus
Requires:       e2fsprogs
Requires:       file
Requires:       gdbm
Requires:       iana-etc
Requires:       libtool
Requires:       iproute
Requires:       iptables
Requires:       iputils
Requires:       irqbalance
Requires:       lvm2
Requires:       lz4
Requires:       mariner-rpm-macros
Requires:       net-tools
Requires:       openssh-clients
Requires:       pkg-config
Requires:       procps-ng
Requires:       sudo
Requires:       systemd
Requires:       tar
Requires:       tzdata
Requires:       util-linux
Requires:       which

%description    base-image
%{summary}

%package        container
Summary:        Metapackage to install the basic set of packages used all image types.
Requires:       bash
Requires:       bzip2
Requires:       ca-certificates-base
Requires:       curl
Requires:       elfutils-libelf
Requires:       expat
Requires:       filesystem
Requires:       findutils
Requires:       grep
Requires:       gzip
Requires:       mariner-release
Requires:       mariner-repos
Requires:       mariner-repos-extras
Requires:       mariner-repos-microsoft
Requires:       ncurses-libs
Requires:       openssl
Requires:       readline
Requires:       rpm
Requires:       rpm-libs
Requires:       sed
Requires:       sqlite-libs
Requires:       tdnf
Requires:       tdnf-plugin-repogpgcheck
Requires:       xz
Requires:       zlib

%description    container
%{summary}

%prep

%build

%files base-image

%files container

%changelog
* Wed Jun 28 2023 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.0-8
- Moving 'curl' and 'grep' to the 'core-packages-container' package.

* Fri Jun 17 2022 Olivia Crain <oliviacrain@microsoft.com> - 2.0-7
- Remove nspr, nss-libs from base container image

* Tue May 24 2022 Jon Slobodzian <joslobo@microsoft.com> - 2.0-6
- Add rpm to base container image

* Wed May 04 2022 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 2.0-5
- Add gzip and sed to base container image

* Tue Apr 19 2022 Jon Slobodzian <joslobo@microsoft.com> - 2.0-4
- Provision official Repos for Official Release

* Wed Apr 13 2022 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 2.0-3
- Reduce container image size

* Wed Feb 23 2022 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 2.0-2
- Update Mariner Core base and container images to remove dnf vim wget by default.
- License verified

* Mon Dec 13 2021 Jon Slobodzian <joslobo@microsoft.com> - 2.0-1
- Update core-package to include new repositories for default Mariner 2.0 Preview Images

* Sat Jul 24 2021 Jon Slobodzian <joslobo@microsoft.com> - 0.1-23
- Include new Microsoft repo for x86_64 architectures (temporarily exclude from aarch64)

* Thu Mar 04 2021 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 0.1-22
- Remove bootloader packages to reduce disk footprint in core images.

* Tue Feb 16 2021 Henry Beberman <henry.beberman@microsoft.com> 0.1-21
- Explicitly add lz4 to container subpackage for systemd dependency.

* Wed Sep 02 2020 Mateusz Malisz <mamalisz@microsoft.com> 0.1-20
- Add chrony package to the base-image.

* Thu Jul 23 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 0.1-19
- Removing 'ca-certificates' from container subpackage.

* Fri Jul 17 2020 Andrew Phelps <anphel@microsoft.com> 0.1-18
- Add ca-certificates to container subpackage.

* Wed Jun 17 2020 Nicolas Ontiveros <niontive@microsoft.com> 0.1-17
- Add 'lvm2' to base-image Requires.

* Mon Jun 15 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 0.1-16
- Removing 'dnf' from core containter packages.

* Fri Jun 05 2020 Paul Monson <paulmon@microsoft.com> 0.1-15
- Require openssh-clients but not openssh-server

* Fri May 29 2020 Nicolas Ontiveros <niontive@microsoft.com> 0.1-14
- Add 'cryptsetup' to base-image Requires.

* Thu May 28 2020 Ruying Chen <v-ruyche@microsoft.com> 0.1-13
- Add 'mariner-rpm-macros'.

* Wed May 20 2020 Andrew Phelps <anphel@microsoft.com> 0.1-12
- Remove cloud-init.

* Tue May 19 2020 Emre Girgin <mrgirgin@microsoft.com> 0.1-11
- Add 'tdnf-plugin-repogpgcheck' as a dependency.

* Wed May 13 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 0.1-10
- Renaming package to 'core-packages'.
- Created separate core sub-packages: '-base-image', '-container'.

* Wed May 13 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 0.1-9
- Adding "dnf" to the set of required packages.

* Mon Apr 13 2020 Emre Girgin <mrgirgin@microsoft.com> 0.1-8
- Rename iproute2 to iproute. License updated.

* Mon Apr 13 2020 Nicolas Ontiveros <niontive@microsoft.com> 0.1-7
- Remove iana-etc and motd from Requires.

* Mon Mar 30 2020 Jon Slobodzian <joslobo@microsoft.com> 0.1-6
- Add irqbalance

* Wed Feb 26 2020 Mateusz Malisz <mamalisz@microsoft.com> 0.1-5
- Add sudo

* Wed Oct 23 2019 Andrew Phelps <anphel@microsoft.com> 0.1-4
- Add grub2-efi and grub2-pc for x86_64

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 0.1-3
- Initial CBL-Mariner import from Photon (license: Apache2).

* Thu Nov 15 2018 Alexey Makhalov <amakhalov@vmware.com> 0.1-2
- Add open-vm-tools as requires only for x86_64

* Tue Oct 30 2018 Anish Swaminathan <anishs@vmware.com> 0.1-1
- Initial packaging
