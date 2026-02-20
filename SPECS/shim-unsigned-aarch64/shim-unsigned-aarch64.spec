%global pesign_vre 0.106-1
%global openssl_vre 1.0.2j
%global shim_commit_id afc49558b34548644c1cd0ad1b6526a9470182ed

# For prereleases, % global prerelease rc2, and downpatch Makefile
%if %{defined prerelease}
%global dashpre -%{prerelease}
%global dotpre .%{prerelease}
%global tildepre ~%{prerelease}
%global zdpd 0%{dotpre}.
%endif

%global efidir azurelinux
%global shimrootdir %{_datadir}/shim/
%global shimversiondir %{shimrootdir}/%{version}
%global efiarch aa64
%global shimdir %{shimversiondir}/%{efiarch}

%global debug_package %{nil}
%global __debug_package 1
%global _binaries_in_noarch_packages_terminate_build 0
%global __debug_install_post %{SOURCE100} %{efiarch}
%undefine _debuginfo_subpackages

# currently here's what's in our dbx: nothing
%global dbxfile %{nil}

Name:		shim-unsigned-aarch64
# This package *should* be named shim-unsigned-%%{efiarch} instead of
# shim-unsigned-%%{_arch}, maybe in the future we'll rename it (also
# would be good if Fedora would correct the name). Until then, let's
# just Provide: the proper name.
Provides:       shim-unsigned-%{efiarch}

Version:	16.1
Release:	1%{?dist}
Summary:	First-stage UEFI bootloader
ExclusiveArch:	aarch64
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

%package debuginfo
Summary:	Debug information for shim-unsigned-aarch64
AutoReqProv:	0
BuildArch:	noarch

%description debuginfo
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
cp %{SOURCE3} data/

%build
COMMIT_ID=%{shim_commit_id}
MAKEFLAGS="TOPDIR=.. -f ../Makefile COMMIT_ID=${COMMIT_ID} "
MAKEFLAGS+="EFIDIR=%{efidir} PKGNAME=shim "
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

%install
COMMIT_ID=%{shim_commit_id}
MAKEFLAGS="TOPDIR=.. -f ../Makefile COMMIT_ID=${COMMIT_ID} "
MAKEFLAGS+="EFIDIR=%{efidir} PKGNAME=shim "
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

%files debuginfo -f build-%{efiarch}/debugfiles.list

%files debugsource -f build-%{efiarch}/debugsource.list

%changelog
* Thu Feb 19 2026 Lynsey Rydberg <lyrydber@microsoft.com> - 16.1-1
- Update to shim 16.1

* Thu Nov 28 2024 Chris Co <chrco@microsoft.com> - 15.8-5
- Bump to match shim release

* Tue Nov 26 2024 Chris Co <chrco@microsoft.com> - 15.8-4
- Bump to match shim release

* Tue Mar 12 2024 Dan Streetman <ddstreet@microsoft.com> - 15.8-3
- Initial CBL-Mariner import from Fedora 40 (license: MIT).
- license verified

* Thu Mar 07 2024 Peter Jones <pjones@redhat.com> - 15.8-2
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
  Resolves: rhbz#2259264

* Thu Jul 07 2022 Robbie Harwood <rharwood@redhat.com> - 15.6-2
- Add pjones's aarch64 relocation fix
- Resolves: #2101248

* Wed Jun 15 2022 Peter Jones <pjones@redhat.com> - 15.6-1
- Update to shim-15.6
  Resolves: CVE-2022-28737

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

* Tue Sep 19 2017 Peter Jones <pjones@redhat.com> - 13-3
- Actually update to the *real* 13 final.
  Related: rhbz#1489604

* Thu Aug 31 2017 Peter Jones <pjones@redhat.com> - 13-2
- Actually update to 13 final.

* Mon Aug 21 2017 Peter Jones <pjones@redhat.com> - 13-0.1
- Update to shim-13 test release.

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu May 12 2016 Peter Jones <pjones@redhat.com> - - 0.9-1
- Initial split up of -aarch64
