# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Disable mangling shebangs for dracut module files as it breaks initramfs
%global __brp_mangle_shebangs_exclude_from ^%{_prefix}/lib/dracut/modules.d/.*$

%global desc \
The KIWI Image System provides an operating system image builder \
for Linux supported hardware platforms as well as for virtualization \
and cloud systems like Xen, KVM, VMware, EC2 and more.

%if 0%{?rhel} && 0%{?rhel} < 10
%bcond check 0
%else
%bcond check 1
%endif


Name:           kiwi
Version:        10.2.37
Release: 4%{?dist}
URL:            http://osinside.github.io/kiwi/
Summary:        Flexible operating system image builder
License:        GPL-3.0-or-later
# We must use the version uploaded to pypi, as it contains all the required files.
Source0:        https://files.pythonhosted.org/packages/source/k/%{name}/%{name}-%{version}.tar.gz
# qemu-img dependency is not available
ExcludeArch:    %{ix86}

# Backports from upstream
## Fix unit tests for aarch64 and ppc64le
Patch0001:      https://github.com/OSInside/kiwi/pull/2937.patch

# Proposed upstream
## https://github.com/OSInside/kiwi/pull/2944
## Fix crash when dracut doesn't have --printconfig error
Patch0500:      0001-initrd-format-detection-make-dracut-printconfig-opti.patch

# Fedora-specific patches
## Use buildah instead of umoci by default for OCI image builds
## TODO: Consider getting umoci into Fedora?
Patch1001:      1001-Use-buildah-by-default-for-OCI-image-builds.patch
## Use isomd5sum instead of checkmedia by default for tagging ISO files
## TODO: Consider getting checkmedia into Fedora?
Patch1002:      1002-Use-isomd5sum-by-default-for-tagging-ISO-files.patch


BuildRequires:  bash-completion
BuildRequires:  dracut
BuildRequires:  fdupes
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros
BuildRequires:  shadow-utils
# doc build requirements
BuildRequires:  python3dist(sphinx)
BuildRequires:  python3dist(sphinx-rtd-theme)
%if %{with check}
# for tests
BuildRequires:  python3dist(pytest) >= 7
%if 0%{?fedora}
BuildRequires:  python3dist(pytest-xdist)
%endif
%endif

%description %{desc}


%package systemdeps-core
Summary:        KIWI - Core host system dependencies
Provides:       kiwi-image-tbz-requires = %{version}-%{release}
Obsoletes:      kiwi-image-tbz-requires < %{version}-%{release}
Provides:       kiwi-image:tbz
# tools used by kiwi
# For building Fedora, RHEL/CentOS, and Mageia based images
%if 0%{?fedora} >= 39 || 0%{?rhel} >= 11
Requires:       dnf5
Provides:       kiwi-packagemanager:dnf5
%endif
%if 0%{?fedora} || (0%{?rhel} >= 8 && 0%{?rhel} < 11)
%if 0%{?rhel}
# Backward compatibility for OBS
Requires:       dnf
%endif
Provides:       kiwi-packagemanager:dnf
Provides:       kiwi-packagemanager:dnf4
Provides:       kiwi-packagemanager:yum
%endif
%if (0%{?rhel} >= 8 && 0%{?rhel} < 11)
# For building Fedora, RHEL/CentOS, and Mageia based minimal images
Requires:       microdnf
Provides:       kiwi-packagemanager:microdnf
%endif
# Offers GPG public keys for various RPM distros and third party repositories
Recommends:     distribution-gpg-keys
%if 0%{?fedora} || 0%{?rhel} >= 8
# For building Debian/Ubuntu based images
Recommends:     apt
Recommends:     dpkg
Recommends:     gnupg2
# Keyrings for bootstrap
Recommends:     debian-keyring
Recommends:     ubu-keyring
%endif
%if 0%{?fedora}
# For building Arch based images
Recommends:     pacman
Recommends:     archlinux-keyring
%endif
Requires:       file
Requires:       lsof
Requires:       mtools
Requires:       rsync
Requires:       sed
Requires:       screen
Requires:       tar >= 1.2.7
Requires:       openssl
Requires:       xz
# Python 2 module is no longer available
Obsoletes:      python2-%{name} < %{version}-%{release}
# legacy kiwi initramfs tools are no longer available
Obsoletes:      %{name}-tools < %{version}-%{release}

%description systemdeps-core
This metapackage installs the necessary system dependencies
to run KIWI.

%if 0%{?fedora}
%package systemdeps-pkgmgr-zypper
Summary:        KIWI - Zypper package manager support
# For building (open)SUSE based images
Requires:       zypper
Provides:       kiwi-packagemanager:zypper
Requires:       %{name}-systemdeps-core = %{version}-%{release}

%description systemdeps-pkgmgr-zypper
This metapackage exposes support for Zypper as a package
manager for image builds in KIWI.
%endif

%ifnarch ppc64 %{ix86}
%package systemdeps-containers
Summary:        KIWI - host requirements for container images
Provides:       kiwi-image:docker
Provides:       kiwi-image:oci
Provides:       kiwi-image:appx
Provides:       kiwi-image:wsl
Provides:       kiwi-image-docker-requires = %{version}-%{release}
Obsoletes:      kiwi-image-docker-requires < %{version}-%{release}
Provides:       kiwi-image-wsl-requires = %{version}-%{release}
Obsoletes:      kiwi-image-wsl-requires < %{version}-%{release}
Requires:       buildah
Requires:       skopeo
Requires:       appx-util

%description systemdeps-containers
Host setup helper to pull in all packages required/useful on
the build host to build container images e.g docker, wsl.
%endif

%if 0%{?fedora}
%package systemdeps-enclaves
Summary:        KIWI - host requirements for enclave images
Provides:       kiwi-image:enclave
Requires:       eif_build

%description systemdeps-enclaves
Host setup helper to pull in all packages required/useful on
the build host to build secure enclave images (e.g. AWS Nitro).
%endif

%package systemdeps-iso-media
Summary:        KIWI - host requirements for live and install iso images
Provides:       kiwi-image:iso
Provides:       kiwi-image-iso-requires = %{version}-%{release}
Obsoletes:      kiwi-image-iso-requires < %{version}-%{release}
Requires:       xorriso
Requires:       isomd5sum
%ifarch %{ix86} x86_64
# Pull in syslinux when it's x86
%if 0%{?fedora} || 0%{?rhel} >= 8
Requires:       syslinux-nonlinux
%endif
Requires:       syslinux
%endif
%ifarch x86_64
Requires:       grub2-efi-x64-cdboot
%if ! 0%{?rhel}
Requires:       grub2-efi-ia32-cdboot
%endif
%endif
%ifarch aarch64
Requires:       grub2-efi-aa64-cdboot
%endif
%if ! 0%{?rhel}
%ifarch %{arm}
Requires:       grub2-efi-arm-cdboot
%endif
%endif
Requires:       kiwi-systemdeps-core = %{version}-%{release}
Requires:       kiwi-systemdeps-filesystems = %{version}-%{release}
Requires:       kiwi-systemdeps-bootloaders = %{version}-%{release}

%description systemdeps-iso-media
Host setup helper to pull in all packages required/useful on
the build host to build live and install iso images.

%package systemdeps-bootloaders
Summary:        KIWI - host requirements for configuring bootloaders
%if ! 0%{?rhel}
%ifarch %{arm} aarch64
Requires:       uboot-tools
%endif
%endif
%ifnarch s390 s390x
# grub isn't available on s390(x) systems
Requires:       grub2-tools
Requires:       grub2-tools-extra
Requires:       grub2-tools-minimal
%endif
%ifarch x86_64
Requires:       grub2-tools-efi
%endif
%ifarch x86_64
Requires:       grub2-efi-x64
Requires:       grub2-efi-x64-modules
%if ! 0%{?rhel}
Requires:       grub2-efi-ia32
Requires:       grub2-efi-ia32-modules
%endif
%endif
%ifarch %{ix86} x86_64
Requires:       grub2-pc
Requires:       grub2-pc-modules
%endif
%ifarch aarch64
Requires:       grub2-efi-aa64-modules
%endif
%if ! 0%{?rhel}
# grub-efi for armv7hl is not available in RHEL
%ifarch %{arm}
Requires:       grub2-efi-arm
Requires:       grub2-efi-arm-modules
%endif
%endif
%ifarch s390 s390x
Requires:       s390utils
%endif
Requires:       kiwi-systemdeps-core = %{version}-%{release}

%description systemdeps-bootloaders
Host setup helper to pull in all packages required/useful on
the build host for configuring bootloaders on images.

%package systemdeps-filesystems
Summary:        KIWI - host requirements for filesystems
Provides:       kiwi-image:pxe
Provides:       kiwi-image:kis
Provides:       kiwi-image:erofs
%if ! (0%{?rhel} >= 8)
Provides:       kiwi-filesystem:btrfs
%endif
Provides:       kiwi-filesystem:erofs
Provides:       kiwi-filesystem:ext2
Provides:       kiwi-filesystem:ext3
Provides:       kiwi-filesystem:ext4
Provides:       kiwi-filesystem:squashfs
Provides:       kiwi-filesystem:xfs
Provides:       kiwi-image-pxe-requires = %{version}-%{release}
Obsoletes:      kiwi-image-pxe-requires < %{version}-%{release}
Provides:       kiwi-filesystem-requires = %{version}-%{release}
Obsoletes:      kiwi-filesystem-requires < %{version}-%{release}
Requires:       dosfstools
Requires:       e2fsprogs
Requires:       erofs-utils
Requires:       xfsprogs
%if ! (0%{?rhel} >= 8)
Requires:       btrfs-progs
%endif
Requires:       squashfs-tools
Requires:       qemu-img
Requires:       kiwi-systemdeps-core = %{version}-%{release}

%description systemdeps-filesystems
Host setup helper to pull in all packages required/useful on
the build host to build filesystem images

%package systemdeps-disk-images
Summary:        KIWI - host requirements for disk images
Provides:       kiwi-image:oem
Provides:       kiwi-image:vmx
Provides:       kiwi-image-oem-requires = %{version}-%{release}
Obsoletes:      kiwi-image-oem-requires < %{version}-%{release}
Provides:       kiwi-image-vmx-requires = %{version}-%{release}
Obsoletes:      kiwi-image-vmx-requires < %{version}-%{release}
Requires:       kiwi-systemdeps-filesystems = %{version}-%{release}
Requires:       kiwi-systemdeps-bootloaders = %{version}-%{release}
Requires:       kiwi-systemdeps-iso-media = %{version}-%{release}
Requires:       gdisk
Requires:       lvm2
Requires:       parted
Requires:       kpartx
Requires:       cryptsetup
Requires:       mdadm
Requires:       open-vmdk
Requires:       util-linux

%description systemdeps-disk-images
Host setup helper to pull in all packages required/useful on
the build host to build disk images

%package systemdeps-image-validation
Summary:        KIWI - host requirements for handling image descriptions better
%if 0%{?fedora} || 0%{?rhel} >= 8
Recommends:     jing
%endif
%if 0%{?fedora} || 0%{?rhel} >= 8
Requires:       python3-solv
%endif
%if ! (0%{?rhel} && 0%{?rhel} < 8)
Recommends:     python3-anymarkup
%endif

%description systemdeps-image-validation
Host setup helper to pull in all packages required/useful on
the build host to handling image descriptions better. This also
includes reading of image descriptions for different markup
languages

%package systemdeps
Summary:        KIWI - Host system dependencies
Requires:       kiwi-systemdeps-core = %{version}-%{release}
Requires:       kiwi-systemdeps-bootloaders = %{version}-%{release}
%ifnarch ppc64 %{ix86}
# buildah isn't available on ppc64 or x86_32
Requires:       kiwi-systemdeps-containers = %{version}-%{release}
%endif
Requires:       kiwi-systemdeps-filesystems = %{version}-%{release}
Requires:       kiwi-systemdeps-disk-images = %{version}-%{release}
Requires:       kiwi-systemdeps-iso-media = %{version}-%{release}
%if ! 0%{?rhel}
Requires:       kiwi-systemdeps-image-validation = %{version}-%{release}
%endif
%if 0%{?fedora}
Requires:       kiwi-systemdeps-enclaves = %{version}-%{release}
Recommends:     kiwi-systemdeps-pkgmgr-zypper = %{version}-%{release}
%endif

%description systemdeps
Host setup helper to pull in all packages required/useful to
leverage all functionality in KIWI.


%package -n python3-%{name}
Summary:        KIWI - Python 3 implementation
# Only require core dependencies, and allow OBS to pull the rest through magic Provides
Requires:       kiwi-systemdeps-core = %{version}-%{release}
# Retain default expectation for local installations
Recommends:     kiwi-systemdeps = %{version}-%{release}
# Enable support for alternative markups
Recommends:     python%{python3_version}dist(anymarkup-core) >= 0.8.0
Recommends:     python%{python3_version}dist(xmltodict) >= 0.12.0

BuildArch:      noarch
%{?python_provide:%python_provide python3-%{name}}

%description -n python3-%{name}
Python 3 library of the KIWI Image System. Provides an operating system
image builder for Linux supported hardware platforms as well as for
virtualization and cloud systems like Xen, KVM, VMware, EC2 and more.

%ifarch %{ix86} x86_64
%package pxeboot
Summary:        KIWI - PXE boot structure
Requires:       syslinux
Requires:       tftp-server

%description pxeboot
This package contains the basic PXE directory structure which is
needed to serve kiwi built images via PXE.
%endif

%package -n dracut-kiwi-lib
Summary:        KIWI - Dracut kiwi Library
Requires:       bc
# btrfs-progs is not available on RHEL 8+
%if ! (0%{?rhel} >= 8)
Requires:       btrfs-progs
%endif
Requires:       coreutils
Requires:       cryptsetup
Requires:       curl
Requires:       device-mapper
Requires:       dialog
Requires:       dracut
Requires:       e2fsprogs
Requires:       gdisk
Requires:       grep
Requires:       kpartx
Requires:       lvm2
Requires:       mdadm
Requires:       parted
Requires:       pv
Requires:       util-linux
Requires:       xfsprogs
Requires:       xz
BuildArch:      noarch

%description -n dracut-kiwi-lib
This package contains a collection of methods to provide a library
for tasks done in other kiwi dracut modules

%package -n dracut-kiwi-oem-repart
Summary:        KIWI - Dracut module for oem(repart) image type
Requires:       dracut-kiwi-lib = %{version}-%{release}
BuildArch:      noarch

%description -n dracut-kiwi-oem-repart
This package contains the kiwi-repart dracut module which is
used to repartition the oem disk image to the current disk
geometry according to the setup in the kiwi image configuration

%package -n dracut-kiwi-oem-dump
Summary:        KIWI - Dracut module for oem(install) image type
Requires:       dracut-kiwi-lib = %{version}-%{release}
Requires:       gawk
Requires:       kexec-tools
BuildArch:      noarch

%description -n dracut-kiwi-oem-dump
This package contains the kiwi-dump and kiwi-dump-reboot dracut
modules which is used to install an oem image onto a target disk.
It implements a simple installer which allows for user selected
target disk or unattended installation to target. The source of
the image to install could be either from media(CD/DVD/USB) or
from remote.

%package -n dracut-kiwi-live
Summary:        KIWI - Dracut module for iso(live) image type
Requires:       dracut-kiwi-lib = %{version}-%{release}
Requires:       dracut-network
Requires:       device-mapper
Requires:       dialog
Requires:       dracut
Requires:       e2fsprogs
Requires:       util-linux
Requires:       xfsprogs
Requires:       parted
BuildArch:      noarch

%description -n dracut-kiwi-live
This package contains the kiwi-live dracut module which is used
for booting iso(live) images built with KIWI.

%package -n dracut-kiwi-overlay
Summary:        KIWI - Dracut module for vmx(+overlay) image type
Requires:       dracut-kiwi-lib = %{version}-%{release}
Requires:       dracut
Requires:       util-linux
BuildArch:      noarch

%description -n dracut-kiwi-overlay
This package contains the kiwi-overlay dracut module which is used
for booting vmx images built with KIWI and configured to use an
overlay root filesystem.

%package -n dracut-kiwi-verity
Summary:        KIWI - Dracut module for disk with embedded verity metadata
Requires:       dracut-kiwi-lib = %{version}-%{release}
Requires:       dracut

%description -n dracut-kiwi-verity
This package contains the kiwi-verity dracut module which is used
for booting oem images built with KIWI and configured to use an
embedded verity metadata block via the embed_verity_metadata
type attribute.

%package cli
Summary:        Flexible operating system appliance image builder
Provides:       kiwi-schema = 8.2
# So we can reference it by the source package name while permitting this to be noarch
Provides:       %{name} = %{version}-%{release}
Requires:       python3-%{name} = %{version}-%{release}
Requires:       bash-completion
BuildArch:      noarch

%description cli %{desc}


%prep
%autosetup -p1

# Temporarily switch things back to docopt for everything but Fedora 41+
# FIXME: Drop this hack as soon as we can...
%if ! (0%{?fedora} >= 41 || 0%{?rhel} >= 10)
sed -e 's/docopt-ng.*/docopt = ">=0.6.2"/' -i pyproject.toml
%endif

# Drop shebang for kiwi/xml_parse.py, as we don't intend to use it as an independent script
sed -e "s|#!/usr/bin/env python||" -i kiwi/xml_parse.py


%generate_buildrequires
%pyproject_buildrequires


%build
# Required for some parts
%set_build_flags

%pyproject_wheel

# Build man pages
make -C doc man


%install
# Required for some parts
%set_build_flags

%pyproject_install

# Install man-pages, completion and kiwi default configuration (yes, the slash is needed!)
make buildroot=%{buildroot}/ install

# Install dracut modules (yes, the slash is needed!)
make buildroot=%{buildroot}/ install_dracut

# Get rid of unnecessary doc files
rm -rf %{buildroot}%{_docdir}/packages

# Rename unversioned binaries
mv %{buildroot}%{_bindir}/kiwi-ng %{buildroot}%{_bindir}/kiwi-ng-3

# Create symlinks for correct binaries
ln -sr %{buildroot}%{_bindir}/kiwi-ng %{buildroot}%{_bindir}/kiwi
ln -sr %{buildroot}%{_bindir}/kiwi-ng-3 %{buildroot}%{_bindir}/kiwi-ng

# kiwi pxeboot directory structure to be packed in kiwi-pxeboot
%ifarch %{ix86} x86_64
for i in KIWI pxelinux.cfg image upload boot; do \
    mkdir -p %{buildroot}%{_sharedstatedir}/tftpboot/$i ;\
done
%fdupes %{buildroot}%{_sharedstatedir}/tftpboot
%endif


%post cli
if [ -x /usr/sbin/semanage -a -x /usr/sbin/restorecon ]; then
    # file contexts
    semanage fcontext --add --type install_exec_t        '%{_bindir}/kiwi'               2> /dev/null || :
    semanage fcontext --add --type install_exec_t        '%{_bindir}/kiwi-ng(.*)'        2> /dev/null || :
    restorecon -r %{_bindir}/kiwi %{_bindir}/kiwi-ng* || :
fi

%postun cli
if [ $1 -eq 0 ]; then
    if [ -x /usr/sbin/semanage ]; then
        # file contexts
        semanage fcontext --delete --type install_exec_t        '%{_bindir}/kiwi'               2> /dev/null || :
        semanage fcontext --delete --type install_exec_t        '%{_bindir}/kiwi-ng(.*)'        2> /dev/null || :
    fi
fi


%if %{with check}
%check
# Check section disabled: Disabling checks for initial set of failures.
exit 0

pushd test/unit
# skipped tests require anymarkup which was retired from Fedora
# we patch the code of default ISO tagging method, hence skip test_config_sections_* too
%pytest %{?fedora:-n auto} --ignore markup/any_test.py -k \
  "not test_process_image_info_print_yaml and not test_process_image_info_print_toml \
   and not test_config_sections_defaults and not test_config_sections_invalid"
popd
%endif


%files -n python3-%{name}
%license LICENSE
%{_bindir}/kiwi-ng-3*
%{python3_sitelib}/kiwi*/
%dir %{_datadir}/kiwi
%{_datadir}/kiwi/xsl_to_v74/

%files cli
%{_bindir}/kiwi
%{_bindir}/kiwi-ng
%{_datadir}/bash-completion/completions/kiwi-ng
%{_mandir}/man8/kiwi*
%config(noreplace) %{_sysconfdir}/kiwi.yml

%ifarch %{ix86} x86_64
%files pxeboot
%license LICENSE
%{_sharedstatedir}/tftpboot/*
%endif

%files -n dracut-kiwi-lib
%license LICENSE
%{_prefix}/lib/dracut/modules.d/59kiwi-lib/

%files -n dracut-kiwi-oem-repart
%license LICENSE
%{_prefix}/lib/dracut/modules.d/55kiwi-repart/

%files -n dracut-kiwi-oem-dump
%license LICENSE
%{_prefix}/lib/dracut/modules.d/55kiwi-dump/
%{_prefix}/lib/dracut/modules.d/59kiwi-dump-reboot/

%files -n dracut-kiwi-live
%license LICENSE
%{_prefix}/lib/dracut/modules.d/55kiwi-live/

%files -n dracut-kiwi-overlay
%license LICENSE
%{_prefix}/lib/dracut/modules.d/55kiwi-overlay/

%files -n dracut-kiwi-verity
%{_usr}/lib/dracut/modules.d/50kiwi-verity
%{_bindir}/kiwi-parse-verity

%files systemdeps-core
# Empty metapackage

%if 0%{?fedora}
%files systemdeps-pkgmgr-zypper
# Empty metapackage
%endif

%files systemdeps-bootloaders
# Empty metapackage

%ifnarch ppc64 %{ix86}
%files systemdeps-containers
# Empty metapackage
%endif

%if 0%{?fedora}
%files systemdeps-enclaves
# Empty metapackage
%endif

%files systemdeps-iso-media
# Empty metapackage

%files systemdeps-filesystems
# Empty metapackage

%files systemdeps-disk-images
# Empty metapackage

%files systemdeps-image-validation
# Empty metapackage

%files systemdeps
# Empty metapackage


%changelog
* Mon Feb 02 2026 Adam Williamson <awilliam@redhat.com> - 10.2.37-3
- Backport fix for crash when dracut doesn't have --printconfig option

* Mon Jan 26 2026 Neal Gompa <ngompa@fedoraproject.org> - 10.2.37-2
- Backport fix for aarch64 and ppc64le tests

* Mon Jan 26 2026 Neal Gompa <ngompa@fedoraproject.org> - 10.2.37-1
- Update to 10.2.37

* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 10.2.33-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Fri Nov 14 2025 Daniel P. Berrangé <berrange@redhat.com> - 10.2.33-3
- Add ExcludeArch to remove dep on i686 QEMU

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 10.2.33-2
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Sep 12 2025 Neal Gompa <ngompa@fedoraproject.org> - 10.2.33-1
- Update to 10.2.33

* Fri Aug 15 2025 Neal Gompa <ngompa@fedoraproject.org> - 10.2.32-1
- Update to 10.2.32

* Fri Aug 15 2025 Neal Gompa <ngompa@fedoraproject.org> - 10.2.31-3
- Backport fix for setting up live filesystems correctly

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 10.2.31-2
- Rebuilt for Python 3.14.0rc2 bytecode

* Sat Aug 02 2025 Neal Gompa <ngompa@fedoraproject.org> - 10.2.31-1
- Update to 10.2.31
- Turn check section off by default

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 10.2.27-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jul 10 2025 Neal Gompa <ngompa@fedoraproject.org> - 10.2.27-1
- Update to 10.2.27

* Mon Jun 16 2025 Neal Gompa <ngompa@fedoraproject.org> - 10.2.24-3
- Backport support for running on overlayfs and allowing /boot as a subvolume

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 10.2.24-2
- Rebuilt for Python 3.14

* Wed May 28 2025 Neal Gompa <ngompa@fedoraproject.org> - 10.2.24-1
- Update to 10.2.24

* Fri May 16 2025 Neal Gompa <ngompa@fedoraproject.org> - 10.2.22-1
- Update to 10.2.22

* Thu May 01 2025 Neal Gompa <ngompa@fedoraproject.org> - 10.2.19-1
- Update to 10.2.19

* Tue Apr 29 2025 Neal Gompa <ngompa@fedoraproject.org> - 10.2.18-1
- Update to 10.2.18

* Tue Apr 22 2025 Neal Gompa <ngompa@fedoraproject.org> - 10.2.17-1
- Update to 10.2.17
- Drop all upstream patches

* Wed Apr 16 2025 Neal Gompa <ngompa@fedoraproject.org> - 10.2.16-4
- Add kiwi-image:oci provides for OBS compatibility
- Backport fix for filename extension for container images
- Refresh patch with upstreamed version for allowing C locale in images
- Backport support for filtering files from embedded ESP images

* Sat Mar 29 2025 Neal Gompa <ngompa@fedoraproject.org> - 10.2.16-3
- Add patch to allow the C locale in images

* Fri Mar 28 2025 Neal Gompa <ngompa@fedoraproject.org> - 10.2.16-2
- Apply install_exec_t SELinux file context to kiwi executables

* Tue Mar 25 2025 Neal Gompa <ngompa@fedoraproject.org> - 10.2.16-1
- Update to 10.2.16

* Fri Feb 28 2025 Neal Gompa <ngompa@fedoraproject.org> - 10.2.12-1
- Update to 10.2.12
- Backport fix to configure CHRP properly for ppc64le live images

* Tue Feb 25 2025 Neal Gompa <ngompa@fedoraproject.org> - 10.2.11-1
- Update to 10.2.11
- Backport fix to configure grub2 properly for ppc64le live images

* Mon Feb 03 2025 Neal Gompa <ngompa@fedoraproject.org> - 10.2.9-1
- Update to 10.2.9

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 10.2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Dec 14 2024 Neal Gompa <ngompa@fedoraproject.org> - 10.2.4-1
- Update to 10.2.4

* Wed Dec 04 2024 Neal Gompa <ngompa@fedoraproject.org> - 10.2.3-1
- Update to 10.2.3

* Thu Nov 21 2024 Neal Gompa <ngompa@fedoraproject.org> - 10.2.0-1
- Update to 10.2.0

* Thu Sep 26 2024 Neal Gompa <ngompa@fedoraproject.org> - 10.1.13-1
- Update to 10.1.13

* Tue Sep 17 2024 Neal Gompa <ngompa@fedoraproject.org> - 10.1.12-1
- Update to 10.1.12

* Fri Sep 13 2024 Neal Gompa <ngompa@fedoraproject.org> - 10.1.11-1
- Update to 10.1.11

* Mon Sep 02 2024 Neal Gompa <ngompa@fedoraproject.org> - 10.1.3-1
- Update to 10.1.3
- Drop patches part of this release

* Mon Aug 26 2024 Neal Gompa <ngompa@fedoraproject.org> - 10.1.2-4
- Backport support for using isomd5sum for tagging ISO files
- Refresh patch stack

* Sat Aug 24 2024 Neal Gompa <ngompa@fedoraproject.org> - 10.1.2-3
- Add fixes for live media creation

* Sat Aug 24 2024 Neal Gompa <ngompa@fedoraproject.org> - 10.1.2-2
- Reconcile dependency information with upstream

* Fri Aug 23 2024 Neal Gompa <ngompa@fedoraproject.org> - 10.1.2-1
- Update to 10.1.2
- Backport various fixes queued for the next release

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 10.0.24-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jul 12 2024 Neal Gompa <ngompa@fedoraproject.org> - 10.0.24-1
- Update to 10.0.24
- Backport support for Application ID in ISOs

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 10.0.21-2
- Rebuilt for Python 3.13

* Wed Jun 05 2024 Neal Gompa <ngompa@fedoraproject.org> - 10.0.21-1
- Update to 10.0.21

* Fri May 10 2024 Romain Geissler <romain.geissler@amadeus.com> - 10.0.11-5
- Backport "Add support for stopsignal in containerconfig" (RH#2278884)

* Thu May 09 2024 Romain Geissler <romain.geissler@amadeus.com> - 10.0.11-4
- Backport upstream removing the leaking versionlock.conf (RH#2270364)

* Thu May 09 2024 Adam Williamson <awilliam@redhat.com> - 10.0.11-3
- Backport PR #2549 to fix dnf5 config settings

* Fri Apr 26 2024 Adam Williamson <awilliam@redhat.com> - 10.0.11-2
- Backport PR #2546 to fix package removal with dnf5

* Thu Apr 04 2024 Neal Gompa <ngompa@fedoraproject.org> - 10.0.11-1
- Update to 10.0.11

* Thu Mar 28 2024 Neal Gompa <ngompa@fedoraproject.org> - 10.0.10-1
- Update to 10.0.10

* Sat Mar 23 2024 Neal Gompa <ngompa@fedoraproject.org> - 10.0.8-1
- Update to 10.0.8

* Wed Mar 20 2024 Neal Gompa <ngompa@fedoraproject.org> - 10.0.7-1
- Update to 10.0.7
- Drop fixes included in this release

* Wed Mar 13 2024 Neal Gompa <ngompa@fedoraproject.org> - 10.0.4-5
- Add dependency on xz

* Wed Mar 13 2024 Neal Gompa <ngompa@fedoraproject.org> - 10.0.4-4
- Add one more fix for s390x image builds

* Tue Mar 12 2024 Neal Gompa <ngompa@fedoraproject.org> - 10.0.4-3
- Backport fixes for s390x images

* Mon Mar 11 2024 Neal Gompa <ngompa@fedoraproject.org> - 10.0.4-2
- Fix kiwi-schema provides

* Mon Mar 11 2024 Neal Gompa <ngompa@fedoraproject.org> - 10.0.4-1
- Update to 10.0.4

* Wed Mar 06 2024 Neal Gompa <ngompa@fedoraproject.org> - 10.0.2-1
- Rebase to 10.0.2

* Sat Feb 17 2024 Neal Gompa <ngompa@fedoraproject.org> - 9.25.21-5
- Break out Zypper support into a subpackage

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 9.25.21-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 9.25.21-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Dec 29 2023 Neal Gompa <ngompa@fedoraproject.org> - 9.25.21-2
- Backport fix for detecting setfiles properly

* Tue Dec 19 2023 Neal Gompa <ngompa@fedoraproject.org> - 9.25.21-1
- Update to 9.25.21 (RH#2244597)

* Mon Oct 16 2023 Neal Gompa <ngompa@fedoraproject.org> - 9.25.16-1
- Update to 9.25.16 (RH#2242745)

* Thu Aug 24 2023 Neal Gompa <ngompa@fedoraproject.org> - 9.25.13-1
- Update to 9.25.13 (RH#2234381)

* Wed Aug 09 2023 Neal Gompa <ngompa@fedoraproject.org> - 9.25.12-1
- Update to 9.25.12 (RH#2227909)

* Mon Jul 31 2023 Neal Gompa <ngompa@fedoraproject.org> - 9.25.7-2
- Add patches to fix building man pages from source

* Mon Jul 31 2023 Neal Gompa <ngompa@fedoraproject.org> - 9.25.7-1
- Update to 9.25.7 (RH#2227830)

* Mon Jul 31 2023 Neal Gompa <ngompa@fedoraproject.org> - 9.25.6-1
- Update to 9.25.6 (RH#2227830)

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 9.25.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jul 14 2023 Neal Gompa <ngompa@fedoraproject.org> - 9.25.5-1
- Rebase to 9.25.5 (RH#2195943)

* Thu Jun 29 2023 Python Maint <python-maint@redhat.com> - 9.24.59-2
- Rebuilt for Python 3.12

* Sat May 06 2023 Igor Raits <igor.raits@gmail.com> - 9.24.59-1
- Update to 9.24.59

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 9.24.52-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Dec 01 2022 Neal Gompa <ngompa@fedoraproject.org> - 9.24.52-1
- Update to 9.24.52 (RH#2149347)

* Tue Nov 29 2022 Neal Gompa <ngompa@fedoraproject.org> - 9.24.50-1
- Update to 9.24.50 (RH#2137048)
- Drop patch included in this release

* Sat Oct 22 2022 Igor Raits <igor@gooddata.com> - 9.24.48-2
- Backport patch for being able to build OCI containers in Mock (nspawn)

* Wed Sep 14 2022 Neal Gompa <ngompa@fedoraproject.org> - 9.24.48-1
- Update to 9.24.48 (RH#2106248)

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 9.24.44-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jun 24 2022 Neal Gompa <ngompa@fedoraproject.org> - 9.24.44-1
- Update to 9.24.44 (RH#2100806)

* Tue Jun 14 2022 Neal Gompa <ngompa@fedoraproject.org> - 9.24.43-1
- Update to 9.24.43 (RH#2097038)

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 9.24.42-2
- Rebuilt for Python 3.11

* Mon Jun 13 2022 Neal Gompa <ngompa@fedoraproject.org> - 9.24.42-1
- Update to 9.24.42 (RH#2082967)

* Sat May 07 2022 Igor Raits <igor.raits@gmail.com> - 9.24.34-1
- Update to 9.24.34

* Sun Mar 27 2022 Neal Gompa <ngompa@fedoraproject.org> - 9.24.29-2
- Drop uboot-tools as a dependency for RHEL for now

* Sun Mar 27 2022 Neal Gompa <ngompa@fedoraproject.org> - 9.24.29-1
- Update to 9.24.29 (RH#2058900)
- Backport fix to allow Btrfs and XFS for boot partitions

* Tue Feb 22 2022 Neal Gompa <ngompa@fedoraproject.org> - 9.24.24-1
- Update to 9.24.24 (RH#2049000)

* Sun Jan 30 2022 Neal Gompa <ngompa@fedoraproject.org> - 9.24.20-1
- Update to 9.24.20 (RH#2048171)

* Sat Jan 29 2022 Neal Gompa <ngompa@fedoraproject.org> - 9.24.19-2
- Backport fix for handling xattrs in container image builds

* Tue Jan 25 2022 Neal Gompa <ngompa@fedoraproject.org> - 9.24.19-1
- Update to 9.24.19

* Tue Jan 25 2022 Neal Gompa <ngompa@datto.com> - 9.24.18-2
- Add proposed patch to ensure SELinux policies are correctly applied

* Mon Jan 24 2022 Neal Gompa <ngompa@fedoraproject.org> - 9.24.18-1
- Update to 9.24.18 (RH#2040932)

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 9.24.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Jan 11 2022 Neal Gompa <ngompa@fedoraproject.org> - 9.24.16-1
- Update to 9.24.16 (RH#2039206)

* Tue Jan 04 2022 Neal Gompa <ngompa@fedoraproject.org> - 9.24.15-3
- Rework conditionals for grub2-efi packages
  + Drop grub2-efi-ia32 dependencies for RHEL for now (RH#1997734)
  + Convert Fedora conditionals to "not RHEL" conditionals

* Sun Jan 02 2022 Neal Gompa <ngompa@fedoraproject.org> - 9.24.15-2
- Add missing util-linux dependency for Koji build environments
- Add missing dracut-network dependency for dracut-kiwi-live package

* Tue Dec 21 2021 Neal Gompa <ngompa@fedoraproject.org> - 9.24.15-1
- Update to 9.24.15 (RH#2029340)

* Mon Nov 29 2021 Neal Gompa <ngompa@fedoraproject.org> - 9.24.13-1
- Update to 9.24.13 (RH#2027379)

* Sat Nov 27 2021 Neal Gompa <ngompa@fedoraproject.org> - 9.24.12-1
- Update to 9.24.12 (RH#2025734)
- Add Recommends for various keyring packages

* Mon Nov 22 2021 Neal Gompa <ngompa@fedoraproject.org> - 9.24.8-1
- Update to 9.24.8 (RH#2025641)

* Tue Nov 16 2021 Neal Gompa <ngompa@fedoraproject.org> - 9.24.7-1
- Update to 9.24.7 (RH#2022404)

* Thu Nov 04 2021 Neal Gompa <ngompa@fedoraproject.org> - 9.24.3-1
- Update to 9.24.3 (RH#2014436)

* Thu Oct 07 2021 Neal Gompa <ngompa@fedoraproject.org> - 9.24.0-1
- Rebase to 9.24.0 (RH#1991954)

* Tue Aug 03 2021 Neal Gompa <ngompa@fedoraproject.org> - 9.23.49-1
- Update to 9.23.49 (RH#1977396)
- Drop backports included in this release

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 9.23.39-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jun 29 2021 Neal Gompa <ngompa13@gmail.com> - 9.23.39-2
- Backport fixes from upstream
  + Fix building images using newer dracut
  + Stop using /tmp for large temporary files

* Mon Jun 21 2021 Neal Gompa <ngompa13@gmail.com> - 9.23.39-1
- Update to 9.23.39 (RH#1968128)

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 9.23.34-2
- Rebuilt for Python 3.10

* Mon May 24 2021 Neal Gompa <ngompa13@gmail.com> - 9.23.34-1
- Update to 9.23.34 (RH#1963158)
- Enable support for creating WSL images

* Fri May 21 2021 Neal Gompa <ngompa13@gmail.com> - 9.23.32-1
- Update to 9.23.32 (RH#1946214)

* Mon Mar 29 2021 Neal Gompa <ngompa13@gmail.com> - 9.23.22-1
- Update to 9.23.22 (RH#1941503)

* Wed Mar 17 2021 Neal Gompa <ngompa13@gmail.com> - 9.23.20-3
- Update kiwi-schema provides to match the current schema version
- Sync systemdeps dependencies from upstream

* Wed Mar 10 2021 Neal Gompa <ngompa13@gmail.com> - 9.23.20-2
- Remove grub2-tools-efi dependency on aarch64 as it's not built there

* Mon Mar 08 2021 Neal Gompa <ngompa13@gmail.com> - 9.23.20-1
- Update to 9.23.20 (RH#1904111)
- Sync systemdeps subpackage structure from upstream for OBS compatibility

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 9.21.26-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Nov 20 2020 Neal Gompa <ngompa13@gmail.com> - 9.21.26-2
- Add weak dependency for pacman to enable Arch image builds

* Fri Nov 20 2020 Neal Gompa <ngompa13@gmail.com> - 9.21.26-1
- Upgrade to 9.21.26 (RH#1876191)

* Sat Aug 15 2020 Neal Gompa <ngompa13@gmail.com> - 9.21.7-1
- Upgrade to 9.21.7 (RH#1820679)

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 9.21.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sun Jul 12 2020 Neal Gompa <ngompa13@gmail.com> - 9.21.5-1
- Upgrade to 9.21.5 (RH#1820679)

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 9.20.5-2
- Rebuilt for Python 3.9

* Fri Mar 27 2020 Neal Gompa <ngompa13@gmail.com> - 9.20.5-1
- Upgrade to 9.20.5 (RH#1798896)
- Fix installation of dracut modules on RHEL 8

* Wed Feb 05 2020 Neal Gompa <ngompa13@gmail.com> - 9.19.15-1
- Upgrade to 9.19.15 (RH#1779818)

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 9.19.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Dec 02 2019 Neal Gompa <ngompa13@gmail.com> - 9.19.5-1
- Upgrade to 9.19.5 (RH#1772452)

* Mon Nov 11 2019 Neal Gompa <ngompa13@gmail.com> - 9.18.31-1
- Upgrade to 9.18.31 (RH#1755472)
- Rebase patch to use buildah by default for OCI image builds

* Sat Sep 21 2019 Neal Gompa <ngompa13@gmail.com> - 9.18.17-1
- Upgrade to 9.18.17 (RH#1742734)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 9.18.9-2
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Neal Gompa <ngompa13@gmail.com> - 9.18.9-1
- Upgrade to 9.18.9

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 9.18.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jul 22 2019 Neal Gompa <ngompa13@gmail.com> - 9.18.6-1
- Upgrade to 9.18.6
- Add skopeo as a requirement for container builds

* Thu Jul 04 2019 Neal Gompa <ngompa13@gmail.com> - 9.17.41-1
- Upgrade to 9.17.41 (RH#1713612)
- Switch to requiring grub2 tools and modules instead of grub2-efi
- Do not require grub2 on s390x
- Drop spec cruft for pre Fedora 29

* Mon Apr 22 2019 Neal Gompa <ngompa13@gmail.com> - 9.17.38-1
- Upgrade to 9.17.38 (RH#1698619)

* Sun Mar 31 2019 Neal Gompa <ngompa13@gmail.com> - 9.17.34-2
- Do not require buildah on x86_32 and ppc64

* Sun Mar 31 2019 Neal Gompa <ngompa13@gmail.com> - 9.17.34-1
- Upgrade to 9.17.34 (RH#1688338)
- Patch to use buildah by default instead of umoci for OCI image builds

* Sun Mar 10 2019 Neal Gompa <ngompa13@gmail.com> - 9.17.27-1
- Upgrade to 9.17.27 (RH#1680084)

* Sun Feb 17 2019 Neal Gompa <ngompa13@gmail.com> - 9.17.19-1
- Upgrade to 9.17.19

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 9.16.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Aug 26 2018 Neal Gompa <ngompa13@gmail.com> - 9.16.12-1
- Upgrade to 9.16.12 (RH#1591056)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 9.16.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 9.16.0-2
- Rebuilt for Python 3.7

* Wed Jun 06 2018 Neal Gompa <ngompa13@gmail.com> - 9.16.0-1
- Upgrade to 9.16.0 (RH#1578808)
- Drop Python 2 subpackage for F29+

* Wed May 09 2018 Neal Gompa <ngompa13@gmail.com> - 9.15.1-1
- Upgrade to 9.15.1 (RH#1570222)

* Thu Apr 12 2018 Neal Gompa <ngompa13@gmail.com> - 9.14.2-1
- Upgrade to 9.14.2 (RH#1565110)

* Sat Mar 24 2018 Neal Gompa <ngompa13@gmail.com> - 9.14.0-1
- Upgrade to 9.14.0 (RH#1560120)

* Sat Mar 17 2018 Neal Gompa <ngompa13@gmail.com> - 9.13.7-2
- Add Conflicts for flumotion < 0.11.0.1-9 on python2-kiwi

* Sat Mar 17 2018 Neal Gompa <ngompa13@gmail.com> - 9.13.7-1
- Initial import into Fedora (RH#1483339)

* Fri Mar 16 2018 Neal Gompa <ngompa13@gmail.com> - 9.13.7-0.4
- Drop useless python shebang in a source file
- Swap python BRs for python2 ones

* Fri Mar 16 2018 Neal Gompa <ngompa13@gmail.com> - 9.13.7-0.3
- Fix invocations of python_provide macro to work with noarch subpackages
- Add BuildRequires for kiwi-tools

* Fri Mar 16 2018 Neal Gompa <ngompa13@gmail.com> - 9.13.7-0.2
- More small cleanups
- Reorder Req/Prov declarations

* Fri Mar 16 2018 Neal Gompa <ngompa13@gmail.com> - 9.13.7-0.1
- Update to 9.13.7
- Cleanups to packaging per review
- Adapt kiwi-pxeboot to match how tftp-server is packaged

* Sun Feb 25 2018 Neal Gompa <ngompa13@gmail.com> - 9.13.0-0.3
- Rename source package from python-kiwi to kiwi
- Rename kiwi subpackage to kiwi-cli
- Merge kiwi-man-pages into kiwi-cli

* Wed Feb 21 2018 Neal Gompa <ngompa13@gmail.com> - 9.13.0-0.2
- Update proposed change based on PR changes

* Tue Feb 20 2018 Neal Gompa <ngompa13@gmail.com> - 9.13.0-0.1
- Update to 9.13.0
- Add proposed change to fix yum vs yum-deprecated lookup in chroot

* Mon Feb 12 2018 Neal Gompa <ngompa13@gmail.com> - 9.12.8-0.4
- Switch to autosetup to actually apply patch

* Mon Feb 12 2018 Neal Gompa <ngompa13@gmail.com> - 9.12.8-0.3
- Patch to use pyxattr in setuptools data

* Fri Feb 09 2018 Neal Gompa <ngompa13@gmail.com> - 9.12.8-0.2
- Fix broken dependency on pyxattr

* Thu Feb 08 2018 Neal Gompa <ngompa13@gmail.com> - 9.12.8-0.1
- Update to 9.12.8

* Mon Jan 15 2018 Neal Gompa <ngompa13@gmail.com> - 9.11.30-0.1
- Update to 9.11.30

* Thu Dec 21 2017 Neal Gompa <ngompa13@gmail.com> - 9.11.19-0.1
- Update to 9.11.19

* Wed Sep 06 2017 Neal Gompa <ngompa13@gmail.com> - 9.10.7-0.1
- Update to 9.10.7

* Wed Aug 23 2017 Neal Gompa <ngompa13@gmail.com> - 9.10.6-0.1
- Update to 9.10.6
- Address review feedback

* Sun Aug 20 2017 Neal Gompa <ngompa13@gmail.com> - 9.10.4-0.1
- Initial packaging

