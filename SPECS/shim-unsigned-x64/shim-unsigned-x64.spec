%global pesign_vre 0.106-1
%global openssl_vre 1.0.2j

# For prereleases, % global prerelease rc2, and downpatch Makefile
%if %{defined prerelease}
%global dashpre -%{prerelease}
%global dotpre .%{prerelease}
%global tildepre ~%{prerelease}
%global zdpd 0%{dotpre}.
%endif

%bcond altarch 0

%global efidir azurelinux
%global shimrootdir %{_datadir}/shim/
%global shimversiondir %{shimrootdir}/%{version}
%global efiarch x64
%global shimdir %{shimversiondir}/%{efiarch}
%if %{with altarch}
%global efialtarch ia32
%global shimaltdir %{shimversiondir}/%{efialtarch}
%endif

%global debug_package %{nil}
%global __debug_package 1
%global _binaries_in_noarch_packages_terminate_build 0
%if %{with altarch}
%global __debug_install_post %{SOURCE100} %{efiarch} %{efialtarch}
%else
%global __debug_install_post %{SOURCE100} %{efiarch}
%endif
%undefine _debuginfo_subpackages

# currently here's what's in our dbx: nothing
%global dbxfile %{nil}

Name:		shim-unsigned-%{efiarch}
Version:	15.8
Release:	3%{?dist}
Summary:	First-stage UEFI bootloader
ExclusiveArch:	x86_64
License:	BSD
Vendor:		Microsoft Corporation
Distribution:	Azure Linux
URL:		https://github.com/rhboot/shim
Source0:	https://github.com/rhboot/shim/releases/download/%{version}%{?dashpre}/shim-%{version}%{?dotpre}.tar.bz2
Source1:	azurelinux-ca-20230216.der
%if 0%{?dbxfile}
Source2:	%{dbxfile}
%endif
Source3:	sbat.azurelinux.csv
Source4:	shim.patches

Source100:	shim-find-debuginfo.sh

%include %{SOURCE4}

BuildRequires:	gcc make
BuildRequires:	elfutils-libelf-devel
BuildRequires:	git openssl-devel openssl
BuildRequires:	pesign >= %{pesign_vre}
BuildRequires:	dos2unix findutils
BuildRequires:	vim-extra

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

%if %{with altarch}
%package -n shim-unsigned-%{efialtarch}
Summary:	First-stage UEFI bootloader (unsigned data)
Provides:	bundled(openssl) = %{openssl_vre}

%description -n shim-unsigned-%{efialtarch}
%desc
%endif

%package debuginfo
Summary:	Debug information for shim-unsigned-%{efiarch}
AutoReqProv:	0
BuildArch:	noarch

%description debuginfo
%debug_desc

%if %{with altarch}
%package -n shim-unsigned-%{efialtarch}-debuginfo
Summary:	Debug information for shim-unsigned-%{efialtarch}
AutoReqProv:	0
BuildArch:	noarch

%description -n shim-unsigned-%{efialtarch}-debuginfo
%debug_desc
%endif

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
%if %{with altarch}
mkdir build-%{efialtarch}
%endif
cp %{SOURCE3} data/

%build
COMMITID=$(cat commit)
MAKEFLAGS="TOPDIR=.. -f ../Makefile COMMITID=${COMMITID} "
MAKEFLAGS+="EFIDIR=%{efidir} PKGNAME=shim "
MAKEFLAGS+="ENABLE_SHIM_HASH=true "
MAKEFLAGS+="%{_smp_mflags}"
if [ -f "%{SOURCE1}" ]; then
	MAKEFLAGS="$MAKEFLAGS VENDOR_CERT_FILE=%{SOURCE1}"
fi
%if 0%{?dbxfile}
if [ -f "%{SOURCE2}" ]; then
	MAKEFLAGS="$MAKEFLAGS VENDOR_DBX_FILE=%{SOURCE2}"
fi
%endif

cd build-%{efiarch}
make ${MAKEFLAGS} \
	DEFAULT_LOADER='\\\\grub%{efiarch}.efi' \
	all
cd ..

%if %{with altarch}
cd build-%{efialtarch}
setarch linux32 -B make ${MAKEFLAGS} \
	ARCH=%{efialtarch} \
	DEFAULT_LOADER='\\\\grub%{efialtarch}.efi' \
	all
cd ..
%endif

%install
COMMITID=$(cat commit)
MAKEFLAGS="TOPDIR=.. -f ../Makefile COMMITID=${COMMITID} "
MAKEFLAGS+="EFIDIR=%{efidir} PKGNAME=shim "
MAKEFLAGS+="ENABLE_SHIM_HASH=true "
if [ -f "%{SOURCE1}" ]; then
	MAKEFLAGS="$MAKEFLAGS VENDOR_CERT_FILE=%{SOURCE1}"
fi
%if 0%{?dbxfile}
if [ -f "%{SOURCE2}" ]; then
	MAKEFLAGS="$MAKEFLAGS VENDOR_DBX_FILE=%{SOURCE2}"
fi
%endif

cd build-%{efiarch}
make ${MAKEFLAGS} \
	DEFAULT_LOADER='\\\\grub%{efiarch}.efi' \
	DESTDIR=${RPM_BUILD_ROOT} \
	install-as-data install-debuginfo install-debugsource
install -m 0644 BOOT*.CSV "${RPM_BUILD_ROOT}/%{shimdir}/"
cd ..

%if %{with altarch}
cd build-%{efialtarch}
setarch linux32 make ${MAKEFLAGS} \
	ARCH=%{efialtarch} \
	DEFAULT_LOADER='\\\\grub%{efialtarch}.efi' \
	DESTDIR=${RPM_BUILD_ROOT} \
	install-as-data install-debuginfo install-debugsource
install -m 0644 BOOT*.CSV "${RPM_BUILD_ROOT}/%{shimaltdir}/"
cd ..
%endif

%check
HASH=$(cat %{buildroot}%{shimdir}/shim%{efiarch}.hash | cut -d ' ' -f 1)
# Verify the shim hash is correct
[[ $HASH = $(pesign -h -i %{buildroot}%{shimdir}/shim%{efiarch}.efi | cut -d ' ' -f 1) ]]

%files
%license COPYRIGHT
%dir %{shimrootdir}
%dir %{shimversiondir}
%dir %{shimdir}
%{shimdir}/*.efi
%{shimdir}/*.hash
%{shimdir}/*.CSV

%if %{with altarch}
%files -n shim-unsigned-%{efialtarch}
%license COPYRIGHT
%dir %{shimrootdir}
%dir %{shimversiondir}
%dir %{shimaltdir}
%{shimaltdir}/*.efi
%{shimaltdir}/*.hash
%{shimaltdir}/*.CSV
%endif

%files debuginfo -f build-%{efiarch}/debugfiles.list

%if %{with altarch}
%files -n shim-unsigned-%{efialtarch}-debuginfo -f build-%{efialtarch}/debugfiles.list
%endif

%files debugsource -f build-%{efiarch}/debugsource.list

%changelog
* Thu Feb 08 2024 Dan Streetman <ddstreet@microsoft.com> - 15.8-3
- Initial CBL-Mariner import from Fedora 40 (license: MIT).
- license verified

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
