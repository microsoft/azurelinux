%global security_hardening none
Summary:        Simple kernel loader which boots from a FAT filesystem
Name:           syslinux
Version:        6.04
Release:        10%{?dist}
License:        GPLv2+
URL:            https://www.syslinux.org
Group:          Applications/System
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        https://www.kernel.org/pub/linux/utils/boot/%{name}/Testing/%{version}/%{name}-%{version}-pre1.tar.xz
Patch0:         0001-Add-install-all-target-to-top-side-of-HAVE_FIRMWARE.patch
Patch1:         0006-Replace-builtin-strlen-that-appears-to-get-optimized.patch
Patch2:         syslinux-6.04_pre1-fcommon.patch
ExclusiveArch:  x86_64
BuildRequires:  gcc >= 11.2.0
BuildRequires:  nasm
BuildRequires:  util-linux-devel
Requires:       util-linux

%description
SYSLINUX is a suite of bootloaders, currently supporting DOS FAT
filesystems, Linux ext2/ext3 filesystems (EXTLINUX), PXE network boots
(PXELINUX), or ISO 9660 CD-ROMs (ISOLINUX).  It also includes a tool,
MEMDISK, which loads legacy operating systems from these media.

%package devel
Summary: Headers and libraries for syslinux development.
Group: Development/Libraries
Provides: %{name}-static = %{version}-%{release}
%description devel
Headers and libraries for syslinux development.

%prep
%setup -q -n %{name}-%{version}-pre1
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
# gcc 11.2.0 and above produce error: "cc1: error: '-fcf-protection' is not compatible with this target"
OPTFLAGS="`echo " %{optflags} " |  sed 's/-fcf-protection//g'`"
CFLAGS="`echo " %{build_cflags} " | sed 's/-fcf-protection//g'`"
CXXFLAGS="`echo " %{build_cxxflags} " | sed 's/-fcf-protection//g'`"
export CFLAGS
export CXXFLAGS

# Remove build-wide ldflags
export LDFLAGS=""

#make some fixes required by glibc-2.28:
sed -i '/unistd/a #include <sys/sysmacros.h>' extlinux/main.c
make bios clean all
%install
make bios install-all \
	INSTALLROOT=%{buildroot} BINDIR=%{_bindir} SBINDIR=%{_sbindir} \
	LIBDIR=%{_prefix}/lib DATADIR=%{_datadir} \
	MANDIR=%{_mandir} INCDIR=%{_includedir} \
	LDLINUX=ldlinux.c32 \
	CFLAGS="$CFLAGS" \
	OPTFLAGS="$OPTFLAGS"
rm -rf %{buildroot}/boot
rm -rf %{buildroot}/tftpboot
# remove it unless provide perl(Crypt::PasswdMD5)
rm %{buildroot}/%{_bindir}/md5pass
# remove it unless provide perl(Digest::SHA1)
rm %{buildroot}/%{_bindir}/sha1pass
%files
%defattr(-,root,root)
%license COPYING
%{_bindir}/*
%{_sbindir}/*
%{_datadir}/*
%exclude %{_datadir}/syslinux/com32
%exclude %{_libdir}/debug

%files devel
%defattr(-,root,root)
%{_datadir}/syslinux/com32/*

%changelog
* Thu Nov 11 2021 Nicolas Guibourge <nicolasg@microsoft.com> 6.04-10
- Fix build issue triggered by gcc 11.2.0 usage.
* Thu Jun 11 2020 Henry Beberman <henry.beberman@microsoft.com> 6.04-9
- Disable hardened ldflags to fix build.
* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 6.04-8
- Added %%license line automatically
* Mon May 04 2020 Emre Girgin <mrgirgin@microsoft.com> 6.04-7
- Replace BuildArch with ExclusiveArch
* Tue Mar 24 2020 Paul Monson <paulmon@microsoft.com> 6.04-6
- Add cflags. License verified.
* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 6.04-5
- Initial CBL-Mariner import from Photon (license: Apache2).
* Mon Oct 22 2018 Ajay Kaher <akaher@vmware.com> 6.04-4
- Adding BuildArch
* Wed Sep 19 2018 Alexey Makhalov <amakhalov@vmware.com> 6.04-3
- Fix compilation issue against glibc-2.28
* Wed Oct 25 2017 Alexey Makhalov <amakhalov@vmware.com> 6.04-2
- Remove md5pass and sha1pass tools
* Tue Oct 17 2017 Alexey Makhalov <amakhalov@vmware.com> 6.04-1
- Initial version