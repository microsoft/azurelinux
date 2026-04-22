# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           mokutil
Version:        0.7.2
Release: 3%{?dist}
Epoch:          2
Summary:        Tool to manage UEFI Secure Boot MoK Keys
License:        GPL-3.0-or-later
URL:            https://github.com/lcp/mokutil
Source0:        https://github.com/lcp/mokutil/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        mokutil.patches
ExclusiveArch:  %{ix86} x86_64 aarch64 %{arm}

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  efivar-devel >= 31-1
BuildRequires:  gcc
BuildRequires:  git
BuildRequires:  gnu-efi
BuildRequires:  keyutils-libs-devel
BuildRequires:  make
BuildRequires:  openssl
BuildRequires:  openssl-devel
BuildRequires:  libxcrypt-devel
Conflicts:      shim < 0.8-1%{?dist}
Obsoletes:      mokutil < 0.2.0

%include %{SOURCE1}

%description
mokutil provides a tool to manage keys for Secure Boot through the MoK
("Machine's Own Keys") mechanism.

%prep
%autosetup -S git_am -b 0 -T

%build
./autogen.sh
%configure
%{make_build}

%install
%{make_install}

%files
%license COPYING
%doc README
%{_bindir}/mokutil
%{_mandir}/man1/*
%{_datadir}/bash-completion/completions/mokutil

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Apr 29 2025 Leo Sandoval <lsandova@redhat.com> - 0.7.2-1
- Bump version to 0.7.2 upstream tag
- Incorporate patch with enables --help on non-supported systems

* Tue Mar 04 2025 Nicolas Frayer <nfrayer@redhat.com> 0.7.1-5
- mokutil: remove unused int_to_b64()
- Resolves: #2340875

* Sat Feb 01 2025 Björn Esser <besser82@fedoraproject.org>
- Add explicit BR: libxcrypt-devel

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Mar 10 2024 Peter Robinson <pbrobinson@fedoraproject.org>
- Update to 0.7.1

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Dec 13 2023 Nicolas Frayer <nfrayer@redhat.com>
- Migrate to SPDX license
- Please refer to https://fedoraproject.org/wiki/Changes/SPDX_Licenses_Phase_2

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 06 2022 Robbie Harwood <rharwood@redhat.com> - 0.6.0-4
- Fix unused -s option and pull leak fixes

* Wed May 25 2022 Peter Jones <pjones@redhat.com> - 0.6.0-3
- Fix patch application in the spec file...
- Resolves: #2087066

* Mon May 23 2022 Robbie Harwood <rharwood@redhat.com> - 2:0.6.0-2
- Fix abort on unknown argument
- Resolves: #2087066

* Sat May 07 2022 Peter Robinson <pbrobinson@fedoraproject.org> - 2:0.6.0-1
- Update to 0.6.0 release

* Mon Mar 28 2022 Robbie Harwood <rharwood@redhat.com> - 2:0.5.0-3
- Add ability to change fallback verbose mode

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2:0.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Nov 18 2021 Javier Martinez Canillas <javierm@redhat.com> - 2:0.5.0-1
- Update to 0.5.0 release

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 2:0.4.0-7
- Rebuilt with OpenSSL 3.0.0

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2:0.4.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sat Mar 20 2021 Peter Robinson <pbrobinson@fedoraproject.org> - 2:0.4.0-5
- Minor spec cleanups, build on ARMv7

* Wed Mar 17 2021 Javier Martinez Canillas <javierm@redhat.com> - 0.4.0-4
- Add SBAT and mok-variables support

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2:0.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2:0.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jun 11 2020 Javier Martinez Canillas <javierm@redhat.com> - 0.4.0-1
- Update to 0.4.0 release

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2:0.3.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Nov 12 2019 Peter Jones <pjones@redhat.com> - 0.3.0-14
- Pull one more upstream patch to keep this in sync with the f31 build.

* Thu Oct 24 2019 Leigh Scott <leigh123linux@googlemail.com> - 1:0.3.0-14
- Apply upstream commits to fix FTBFS

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.3.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.3.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 14 2019 Björn Esser <besser82@fedoraproject.org> - 1:0.3.0-11
- Rebuilt for libcrypt.so.2 (#1666033)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.3.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.3.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Jan 20 2018 Björn Esser <besser82@fedoraproject.org> - 1:0.3.0-8
- Rebuilt for switch to libxcrypt

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.3.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.3.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Jul 08 2017 Peter Jones <pjones@redhat.com> - 0.3.0-5
- Rebuild for efivar-31-1.fc26
  Related: rhbz#1468841

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Aug 17 2016 Peter Jones <pjones@redhat.com> - 0.3.0-3
- Rebuild for newer efivar again.

* Wed Aug 10 2016 Peter Jones <pjones@redhat.com> - 0.3.0-2
- Update for newer efivar.

* Tue Jun 14 2016 Peter Jones <pjones@redhat.com> - 0.3.0-1
- Update to 0.3.0 release.
  Resolves: rhbz#1334628

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 1:0.2.0-2
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Mon Oct 06 2014 Peter Jones <pjones@redhat.com> - 0.2.0-1
- First independent package.
