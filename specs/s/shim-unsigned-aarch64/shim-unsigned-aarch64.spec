# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global upstream_version_release 16.1-1

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

%global efidir %(eval echo $(grep ^ID= /etc/os-release | sed -e 's/^ID=//' -e 's/rhel/redhat/'))
%global shimrootdir %{_datadir}/shim/
%global shimversiondir %{shimrootdir}/%{version}-%{release}
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
Version:	16.1
Release: 2%{?dist}
Summary:	First-stage UEFI bootloader
ExclusiveArch:	aarch64
License:	BSD-2-Clause AND OpenSSL
URL:		https://github.com/rhboot/shim
Source0:	https://github.com/rhboot/shim/releases/download/%{version}%{?dashpre}/shim-%{version}%{?dotpre}.tar.bz2
Source1:	azurelinux-ca-20230216.der
%if 0%{?dbxfile}
Source2:	%{dbxfile}
%endif
Source3:	sbat.azurelinux.csv.in
Source4:	shim.patches

Source100:	shim-find-debuginfo.sh

%include %{SOURCE4}

BuildRequires:	gcc make
BuildRequires:	elfutils-libelf-devel
BuildRequires:	git openssl-devel openssl
BuildRequires:	pesign >= %{pesign_vre}
BuildRequires:	dos2unix findutils
BuildRequires:	sed

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
sed -e 's/@@VERSION@@/%{version}/g' \
    -e 's/@@RELEASE@@/%{release}/g' \
    -e 's/@@UPSTREAM_VERSION_RELEASE@@/%{upstream_version_release}/g' \
    < %{SOURCE3} > data/sbat.redhat.csv

%build
COMMIT_ID=%{shim_commit_id}
MAKEFLAGS="TOPDIR=.. -f ../Makefile COMMIT_ID=${COMMIT_ID} "
MAKEFLAGS+="EFIDIR=%{efidir} PKGNAME=shim RELEASE=%{release} "
MAKEFLAGS+="ENABLE_SHIM_HASH=true "
MAKEFLAGS+="SBAT_AUTOMATIC_DATE=2025021800 "
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

cd build-%{efiarch}
for efi in shim%{efiarch} mm%{efiarch} fb%{efiarch}; do
    cp ${efi}.efi ${efi}.nx.efi
    ./post-process-pe -n -x ${efi}.nx.efi
done
pesign -i shim%{efiarch}.nx.efi -P -h > shim%{efiarch}.nx.hash
cd ..
%install
COMMIT_ID=%{shim_commit_id}
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

cd build-%{efiarch}
for efi in shim%{efiarch} mm%{efiarch} fb%{efiarch}; do
    install -m 0644 ${efi}.nx.efi ${RPM_BUILD_ROOT}/%{shimdir}/
done
install -m 0644 shim%{efiarch}.nx.hash ${RPM_BUILD_ROOT}/%{shimdir}/
cd ..
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
* Mon Aug 24 2026 Lynsey Rydberg <lyrydber@microsoft.com> - 16.1-2
- Update shim-unsigned packages to 16.1
- Enforce the grub,5 SBAT generation baseline
- Remove obsolete %{version}-2 compatibility symlinks
- Add Azure Linux SBAT provenance
- Embed the Azure Linux vendor certificate
- Add NX-compatible EFI variants

* Wed Sep 03 2025 Peter Jones <pjones@redhat.com> - 16.1-1
- Update to shim-16.1

* Fri Mar 22 2024 Nicolas Frayer <nfrayer@redhat.com>
- Migrate to SPDX license
- Please refer to https://fedoraproject.org/wiki/Changes/SPDX_Licenses_Phase_2

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
