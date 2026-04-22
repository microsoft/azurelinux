# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global pesign_vre 0.106-1
%global openssl_vre 1.0.2j

# For prereleases, % global prerelease rc2, and downpatch Makefile
%if %{defined prerelease}
%global dashpre -%{prerelease}
%global dotpre .%{prerelease}
%global tildepre ~%{prerelease}
%global zdpd 0%{dotpre}.
%endif

%global efidir %(eval echo $(grep ^ID= /etc/os-release | sed -e 's/^ID=//' -e 's/rhel/redhat/'))
%global shimrootdir %{_datadir}/shim/
%global shimversiondir %{shimrootdir}/%{version}-%{release}
%global efiarch x64
%global shimdir %{shimversiondir}/%{efiarch}
%global efialtarch ia32
%global shimaltdir %{shimversiondir}/%{efialtarch}

%global debug_package %{nil}
%global __debug_package 1
%global _binaries_in_noarch_packages_terminate_build 0
%global __debug_install_post %{SOURCE100} %{efiarch} %{efialtarch}
%undefine _debuginfo_subpackages

# currently here's what's in our dbx: nothing
%global dbxfile %{nil}

Name:		shim-unsigned-%{efiarch}
Version:	15.8
Release: 3%{?dist}
Summary:	First-stage UEFI bootloader
ExclusiveArch:	x86_64
License:	BSD-2-Clause AND OpenSSL
URL:		https://github.com/rhboot/shim
Source0:	https://github.com/rhboot/shim/releases/download/%{version}%{?dashpre}/shim-%{version}%{?dotpre}.tar.bz2
Source1:	fedora-ca-20200709.cer
%if 0%{?dbxfile}
Source2:	%{dbxfile}
%endif
Source3:	sbat.redhat.csv
Source4:	shim.patches

Source100:	shim-find-debuginfo.sh

%include %{SOURCE4}

BuildRequires:	gcc make
BuildRequires:	elfutils-libelf-devel
BuildRequires:	git openssl-devel openssl
BuildRequires:	pesign >= %{pesign_vre}
BuildRequires:	dos2unix findutils

# Shim uses OpenSSL, but cannot use the system copy as the UEFI ABI is not
# compatible with SysV (there's no red zone under UEFI) and there isn't a
# POSIX-style C library.
# BuildRequires:	OpenSSL
Provides:	bundled(openssl) = %{openssl_vre}

%global desc \
Initial UEFI bootloader that handles chaining to a trusted full \
bootloader under secure boot environments.
%global debug_desc \
This package provides debug information for package %{expand:%%{name}} \
Debug information is useful when developing applications that \
use this package or when debugging this package.

%description
%desc

%package -n shim-unsigned-%{efialtarch}
Summary:	First-stage UEFI bootloader (unsigned data)
Provides:	bundled(openssl) = %{openssl_vre}

%description -n shim-unsigned-%{efialtarch}
%desc

%package debuginfo
Summary:	Debug information for shim-unsigned-%{efiarch}
AutoReqProv:	0
BuildArch:	noarch

%description debuginfo
%debug_desc

%package -n shim-unsigned-%{efialtarch}-debuginfo
Summary:	Debug information for shim-unsigned-%{efialtarch}
AutoReqProv:	0
BuildArch:	noarch

%description -n shim-unsigned-%{efialtarch}-debuginfo
%debug_desc

%package debugsource
Summary:	Debug Source for shim-unsigned
AutoReqProv:	0
BuildArch:	noarch

%description debugsource
%debug_desc

%prep
%autosetup -S git_am -n shim-%{version}
git config --unset user.email
git config --unset user.name
mkdir build-%{efiarch}
mkdir build-%{efialtarch}
cp %{SOURCE3} data/

%build
COMMIT_ID=5914984a1ffeab841f482c791426d7ca9935a5e6
MAKEFLAGS="TOPDIR=.. -f ../Makefile COMMIT_ID=${COMMIT_ID} "
MAKEFLAGS+="EFIDIR=%{efidir} PKGNAME=shim RELEASE=%{release} "
MAKEFLAGS+="ENABLE_SHIM_HASH=true "
MAKEFLAGS+=" %{_smp_mflags} "
if [ -f "%{SOURCE1}" ]; then
	MAKEFLAGS="$MAKEFLAGS VENDOR_CERT_FILE=%{SOURCE1} "
fi
%if 0%{?dbxfile}
if [ -f "%{SOURCE2}" ]; then
	MAKEFLAGS="$MAKEFLAGS VENDOR_DBX_FILE=%{SOURCE2} "
fi
%endif

cd build-%{efiarch}
make ${MAKEFLAGS} \
	DEFAULT_LOADER='\\\\grub%{efiarch}.efi' \
	all
cd ..

cd build-%{efialtarch}
setarch linux32 -B make ${MAKEFLAGS} \
	ARCH=%{efialtarch} \
	DEFAULT_LOADER='\\\\grub%{efialtarch}.efi' \
	all
cd ..

%install
COMMIT_ID=5914984a1ffeab841f482c791426d7ca9935a5e6
MAKEFLAGS="TOPDIR=.. -f ../Makefile COMMIT_ID=${COMMIT_ID} "
MAKEFLAGS+="EFIDIR=%{efidir} PKGNAME=shim RELEASE=%{release} "
MAKEFLAGS+="ENABLE_SHIM_HASH=true "
if [ -f "%{SOURCE1}" ]; then
	MAKEFLAGS="$MAKEFLAGS VENDOR_CERT_FILE=%{SOURCE1} "
fi
%if 0%{?dbxfile}
if [ -f "%{SOURCE2}" ]; then
	MAKEFLAGS="$MAKEFLAGS VENDOR_DBX_FILE=%{SOURCE2} "
fi
%endif

cd build-%{efiarch}
make ${MAKEFLAGS} \
	DEFAULT_LOADER='\\\\grub%{efiarch}.efi' \
	DESTDIR=${RPM_BUILD_ROOT} \
	install-as-data install-debuginfo install-debugsource
install -m 0644 BOOT*.CSV "${RPM_BUILD_ROOT}/%{shimdir}/"
cd ..

cd build-%{efialtarch}
setarch linux32 make ${MAKEFLAGS} \
	ARCH=%{efialtarch} \
	DEFAULT_LOADER='\\\\grub%{efialtarch}.efi' \
	DESTDIR=${RPM_BUILD_ROOT} \
	install-as-data install-debuginfo install-debugsource
install -m 0644 BOOT*.CSV "${RPM_BUILD_ROOT}/%{shimaltdir}/"
cd ..

ln -s %{version}-%{release} %{buildroot}%{_datadir}/shim/%{version}-2
%files
%license COPYRIGHT
%dir %{shimrootdir}
%dir %{shimversiondir}
%dir %{shimdir}
%{shimdir}/*.efi
%{shimdir}/*.hash
%{shimdir}/*.CSV

%{_datadir}/shim/%{version}-2
%files -n shim-unsigned-%{efialtarch}
%license COPYRIGHT
%dir %{shimrootdir}
%dir %{shimversiondir}
%dir %{shimaltdir}
%{shimaltdir}/*.efi
%{shimaltdir}/*.hash
%{shimaltdir}/*.CSV

%files debuginfo -f build-%{efiarch}/debugfiles.list

%files -n shim-unsigned-%{efialtarch}-debuginfo -f build-%{efialtarch}/debugfiles.list

%files debugsource -f build-%{efiarch}/debugsource.list

%changelog
* Fri Mar 22 2024 Nicolas Frayer <nfrayer@redhat.com>
- Migrate to SPDX license
- Please refer to https://fedoraproject.org/wiki/Changes/SPDX_Licenses_Phase_2

* Tue Feb 20 2024 Peter Jones <pjones@redhat.com> - 15.8-2
- Fix some minor problems caught in review.

* Mon Dec 11 2023 Peter Jones <pjones@redhat.com> - 15.8-1
- Update to shim-15.8
  Resolves: CVE-2023-40546
  Resolves: CVE-2023-40547
  Resolves: CVE-2023-40548
  Resolves: CVE-2023-40549
  Resolves: CVE-2023-40550
  Resolves: CVE-2023-40551
  Resolves: rhbz#2113005
  Resolves: rhbz#2189197
  Resolves: rhbz#2238884

* Tue Jun 07 2022 Peter Jones <pjones@redhat.com> - 15.6-1
- Update to shim-15.6
  Resolves: CVE-2022-28737

* Thu Mar 10 2022 Peter Jones <pjones@redhat.com> - 15.5-1
- Update to shim 15.5
  - lots of minor fixes

* Tue Mar 30 2021 Peter Jones <pjones@redhat.com> - 15.4-1
- Update to shim 15.4
  - Support for revocations via the ".sbat" section and SBAT EFI variable
  - A new unit test framework and a bunch of unit tests
  - No external gnu-efi dependency
  - Better CI
  Resolves: CVE-2020-14372
  Resolves: CVE-2020-25632
  Resolves: CVE-2020-25647
  Resolves: CVE-2020-27749
  Resolves: CVE-2020-27779
  Resolves: CVE-2021-20225
  Resolves: CVE-2021-20233

* Wed Mar 24 2021 Peter Jones <pjones@redhat.com> - 15.3-0~1
- Update to shim 15.3
  - Support for revocations via the ".sbat" section and SBAT EFI variable
  - A new unit test framework and a bunch of unit tests
  - No external gnu-efi dependency
  - Better CI
  Resolves: CVE-2020-14372
  Resolves: CVE-2020-25632
  Resolves: CVE-2020-25647
  Resolves: CVE-2020-27749
  Resolves: CVE-2020-27779
  Resolves: CVE-2021-20225
  Resolves: CVE-2021-20233

* Thu Apr 05 2018 Peter Jones <pjones@redhat.com> - 15-1
- Update to shim 15
- better checking for bad linker output
- flicker-free console if there's no error output
- improved http boot support
- better protocol re-installation
- dhcp proxy support
- tpm measurement even when verification is disabled
- REQUIRE_TPM build flag
- more reproducable builds
- measurement of everything verified through shim_verify()
- coverity and scan-build checker make targets
- misc cleanups

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 13-0.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Aug 18 2017 Peter Jones <pjones@redhat.com> - 13-0.1
- Make a new shim-unsigned-x64 package like the shim-unsigned-aarch64 one.
- This will (eventually) supersede what's in the "shim" package so we can
  make "shim" hold the signed one, which will confuse fewer people.
