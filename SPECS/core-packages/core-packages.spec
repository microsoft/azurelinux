Summary:        Metapackage with core sets of packages
Name:           core-packages
Version:        0.1
Release:        27%{?dist}
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
Requires:       dnf
Requires:       dnf-utils
Requires:       file
Requires:       gdbm
Requires:       iana-etc
Requires:       iproute
Requires:       iptables
Requires:       iputils
Requires:       irqbalance
Requires:       lvm2
Requires:       openssh-clients
Requires:       procps-ng
Requires:       rpm
Requires:       tzdata
Requires:       which

%description    base-image
%{summary}

%package        container
Summary:        Metapackage to install the basic set of packages used by all image types.
Requires:       bash
Requires:       bzip2
Requires:       ca-certificates-base
Requires:       curl
Requires:       e2fsprogs
Requires:       elfutils-libelf
Requires:       expat
Requires:       filesystem
Requires:       findutils
Requires:       grep
Requires:       gzip
Requires:       libtool
Requires:       lz4
Requires:       mariner-release
Requires:       mariner-repos
%ifarch x86_64
# Temporarily exclude aarch64 from including the microsoft repo until content is available in the repo
Requires:       mariner-repos-microsoft
%endif
Requires:       mariner-rpm-macros
Requires:       ncurses-libs
Requires:       net-tools
Requires:       nspr
Requires:       nss-libs
Requires:       openssl
Requires:       pkg-config
Requires:       readline
Requires:       rpm
Requires:       rpm-libs
Requires:       sed
Requires:       sqlite-libs
Requires:       sudo
Requires:       systemd
Requires:       tar
Requires:       tdnf
Requires:       tdnf-plugin-repogpgcheck
Requires:       util-linux
Requires:       vim
Requires:       wget
Requires:       xz
Requires:       zlib

%description    container
%{summary}

%prep

%build

%files base-image

%files container

%changelog
* Tue Dec 20 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.1-27
- Making sure 'rpm' is always part of the base image.

* Wed Dec 15 2021 Chris Co <chrco@microsoft.com> - 0.1-26
- Remove check-restart and dnf-automatic from core set of packages

* Wed Aug 11 2021 Neha Agarwal <nehaagarwal@microsoft.com> - 0.1-25
- Add check-restart to the base image

* Wed Aug 11 2021 Neha Agarwal <nehaagarwal@microsoft.com> - 0.1-24
- Add dnf-automatic and dnf-utils to the base image.

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
